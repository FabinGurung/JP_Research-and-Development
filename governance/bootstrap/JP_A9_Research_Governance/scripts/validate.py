#!/usr/bin/env python3
"""Validate schema, sequence lineage, receipt closure and immutable history."""
import argparse
import json
from pathlib import Path
import re
import subprocess
from jsonschema import Draft202012Validator, FormatChecker
from a9 import history, check_close, check_evidence, load

ROOT = Path(__file__).resolve().parents[1]

def validate(root, public=True):
    errors = []
    def restricted(value):
        if isinstance(value, dict):
            return value.get('visibility') == 'RESTRICTED' or any(restricted(v) for v in value.values())
        return isinstance(value, list) and any(restricted(v) for v in value)
    def check(path, name):
        try:
            Draft202012Validator(load(root/'schemas'/name), format_checker=FormatChecker()).validate(load(path))
        except Exception as error:
            errors.append(f'{path.relative_to(root)}: {error}')
    for schema in (root/'schemas').glob('*.json'):
        try:
            Draft202012Validator.check_schema(load(schema))
        except Exception as error:
            errors.append(str(error))
    ids = set()
    for project in (root/'projects').iterdir():
        if not project.is_dir():
            continue
        check(project/'project.json', 'project.schema.json')
        check(project/'debt.json', 'debt.schema.json')
        check(project/'drive_pointers.json', 'drive-pointer.schema.json')
        index = load(project/'current.json')
        identity = load(project/'project.json')['project_id']
        if index['project_id'] != identity:
            errors.append('Project routing index identity mismatch')
        for seq in (project/'sequences').glob('*.json'):
            check(seq, 'sequence.schema.json')
        for lane in (project/'lanes').iterdir():
            try:
                check(lane/'CURRENT.json', 'current.schema.json')
                current = load(lane/'CURRENT.json')
                if current['project_id'] != identity or index['lanes'].get(lane.name) != f'lanes/{lane.name}/CURRENT.json':
                    raise ValueError('Project routing or lane identity mismatch')
                debt = load(project/'debt.json')['items']
                if sorted(current['open_debt']) != sorted(item['description'] for item in debt if item['lane'] == lane.name and item['status'] == 'OPEN'):
                    raise ValueError('Project debt register and lane CURRENT disagree')
                events = history(lane)
                parent = None
                sequence = 0
                latest_closed = None
                for event in events:
                    check(lane/'events'/f"{events.index(event)+1:06d}.json", 'event.schema.json')
                    if event['event_id'] in ids:
                        raise ValueError('Duplicate event ID')
                    ids.add(event['event_id'])
                    if event['parent_event'] != parent:
                        raise ValueError('Broken parent lineage')
                    if event['project_id'] != current['project_id'] or event['project'] != project.name or event['lane'] != lane.name:
                        raise ValueError('Cross-project/lane identity mismatch')
                    if event['operation'] == 'PRE':
                        if sequence and prior['status'] != 'CLOSED':
                            raise ValueError('PRE replayed before previous close')
                        sequence += 1
                        if not event['pre_commit'] or not event['pre_snapshots']:
                            raise ValueError('PRE lacks evidence')
                    elif sequence == 0 or prior['status'] == 'CLOSED':
                        raise ValueError('Operation without open PRE')
                    if event['sequence'] != sequence:
                        raise ValueError('Sequence gap or mismatch')
                    check_evidence(root, event)
                    if event['status'] == 'CLOSED' and event['operation'] != 'CLOSE':
                        raise ValueError('Only verified CLOSE can close a sequence')
                    if event['operation'] == 'CLOSE':
                        check_close(root, events[:events.index(event)], event)
                        latest_closed = event['event_id']
                    if event['operation'] in ['SUPERSEDE','ROLLBACK_POINTER']:
                        targets = [e for e in events[:events.index(event)] if e['event_id'] == event['supersedes']]
                        if not targets or (event['operation'] == 'ROLLBACK_POINTER' and targets[0]['status'] != 'CLOSED'):
                            raise ValueError('Invalid correction/rollback target')
                    parent = event['event_id']
                    prior = event
                if current['latest_event'] != parent or current['latest_closed_event'] != latest_closed or current['sequence'] != sequence:
                    raise ValueError('CURRENT/event lineage mismatch')
                if events and any(current[k] != events[-1][k] for k in ['status','open_debt','next_boundary']):
                    raise ValueError('CURRENT status/debt differs from latest event')
            except Exception as error:
                errors.append(f'{lane.relative_to(root)}: {error}')
    for receipt in (root/'receipts').glob('*.json'):
        check(receipt, 'receipt.schema.json')
    forbidden = {'.pdf','.zip','.ttf','.otf','.woff','.woff2','.exe','.xlsx','.docx'}
    for path in root.rglob('*'):
        if not path.is_file() or '.git' in path.parts or '__pycache__' in path.parts or '.venv' in path.parts:
            continue
        if path.suffix.lower() in forbidden:
            errors.append(f'Forbidden scientific binary or private font: {path.relative_to(root)}')
        if path.suffix == '.json':
            content = path.read_text()
            if public and restricted(json.loads(content)):
                errors.append(f'Restricted pointer in public repository: {path.relative_to(root)}')
        if path.suffix in ['.json','.jsonl','.md','.txt']:
            content = path.read_text()
            if re.search(r'gh[pousr]_[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----', content):
                errors.append(f'Credential marker: {path.relative_to(root)}')
    return errors

def immutable_history(root, base_ref):
    prefix = Path(subprocess.check_output(['git','rev-parse','--show-prefix'],cwd=root,text=True).strip())
    paths = subprocess.check_output(['git','ls-tree','-r','--name-only',base_ref],cwd=root,text=True).splitlines()
    errors=[]
    for path in paths:
        local = Path(path)
        if prefix.parts and not local.is_relative_to(prefix):
            continue
        local = local.relative_to(prefix) if prefix.parts else local
        if ('events' not in local.parts and 'releases' not in local.parts and 'receipts' not in local.parts) or local.suffix != '.json':
            continue
        old = subprocess.check_output(['git','show',f'{base_ref}:{path}'],cwd=root)
        target = root/local
        if not target.is_file() or target.read_bytes() != old:
            errors.append(f'Immutable committed history changed: {local}')
    return errors

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--private',action='store_true',help='Use only after repository visibility is independently verified.')
    parser.add_argument('--base-ref')
    args=parser.parse_args()
    errors=validate(ROOT, public=not args.private)
    if args.base_ref:
        errors+=immutable_history(ROOT,args.base_ref)
    for error in errors:
        print(error)
    if errors:
        raise SystemExit(1)
    print('A9 schemas, lineage, closure and privacy validation: PASS')

if __name__=='__main__':
    main()
