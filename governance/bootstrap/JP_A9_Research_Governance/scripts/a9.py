#!/usr/bin/env python3
"""Prepare append-only A9 worktree state; never infer provider truth."""
from __future__ import annotations
import argparse
import hashlib
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SAFE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
OPERATIONS = ['PRE', 'SNAPSHOT', 'DUPLICATE', 'ENUMERATE', 'ARCHIVE', 'MUTATE', 'HASH', 'POST',
              'PROVIDER_READBACK', 'ACK', 'REGISTER', 'TAG', 'RELEASE', 'SUPERSEDE', 'ROLLBACK_POINTER', 'DEBT_REGISTER', 'CLOSE']

def load(path):
    return json.loads(path.read_text())

def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    with temporary.open('w') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)

def safe(value):
    if not SAFE.fullmatch(value):
        raise ValueError('Unsafe project/lane identifier')
    return value

def lane_root(root, project, lane):
    return root / 'projects' / safe(project) / 'lanes' / safe(lane)

@contextmanager
def lock(root):
    path = root / '.a9.lock'
    descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        yield
    finally:
        os.close(descriptor)
        path.unlink()

def history(directory):
    return [load(p) for p in sorted((directory / 'events').glob('*.json'))]

def check_receipt(root, reference):
    if not reference:
        raise ValueError('PASS evidence requires an existing provider/QA receipt')
    path = (root / reference).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError('Receipt missing or outside repository')
    return load(path)

def check_evidence(root, evidence):
    for key in ['qa', 'readback', 'ack', 'registration']:
        result = evidence.get(key, {})
        if result.get('status') == 'PASS':
            receipt = check_receipt(root, result.get('receipt'))
            from jsonschema import Draft202012Validator, FormatChecker
            Draft202012Validator(load(root / 'schemas/receipt.schema.json'), format_checker=FormatChecker()).validate(receipt)
            if receipt.get('result') != 'PASS':
                raise ValueError('Evidence receipt does not prove PASS')

def check_close(root, events, candidate):
    seq = [event for event in events if event['sequence'] == candidate['sequence']]
    required = {'PRE': None, 'POST': 'qa', 'PROVIDER_READBACK': 'readback', 'ACK': 'ack', 'REGISTER': 'registration'}
    for operation, field in required.items():
        rows = [e for e in seq if e['operation'] == operation]
        if not rows or (field and rows[-1][field]['status'] != 'PASS'):
            raise ValueError(f'CLOSE requires verified {operation}')
        if operation == 'POST' and not rows[-1]['post_snapshots']:
            raise ValueError('POST requires scientific snapshot or code tree pointers')
    if candidate['open_debt']:
        raise ValueError('CLOSE blocked by open debt')
    for event in seq:
        check_evidence(root, event)
        for artifact in event['artifacts']:
            if artifact['sha256'] is None or artifact['bytes'] is None or not artifact['reverse_reference_receipt']:
                raise ValueError('Scientific artifact hash, size and reverse reference must be verified')
            check_receipt(root, artifact['reverse_reference_receipt'])

def init(root, project, project_id, lane):
    authority = load(root / 'CURRENT.json')
    repository = authority.get('repository', {})
    if authority.get('status') != 'ACTIVE' or not repository.get('provider_id') or repository.get('visibility') not in ['PUBLIC', 'PRIVATE']:
        raise ValueError('Repository not provisioned/verified; live lane initialization is blocked')
    if not re.fullmatch(r'PROJ-[0-9]{6}', project_id):
        raise ValueError('Project identity must be a permanent PROJ ID')
    directory = lane_root(root, project, lane)
    if (directory / 'CURRENT.json').exists():
        raise ValueError('Lane already exists; resume instead of replaying initialization')
    project_root = directory.parents[1]
    project_path = project_root / 'project.json'
    if project_path.exists() and load(project_path)['project_id'] != project_id:
        raise ValueError('Permanent project identity mismatch')
    with lock(root):
        if not project_path.exists():
            save(project_path, dict(project_id=project_id, slug=project, label=project.replace('-', ' ').title(),
                 scientific_authority='GOOGLE_DRIVE', public_projection=False))
            save(project_root / 'debt.json', dict(project_id=project_id, items=[]))
            save(project_root / 'drive_pointers.json', dict(project_id=project_id, artifacts=[]))
            (project_root / 'artifact_edges.jsonl').write_text('')
            (project_root / 'sequences').mkdir(exist_ok=True)
            (project_root / 'releases').mkdir(exist_ok=True)
        index = load(project_root / 'current.json') if (project_root / 'current.json').exists() else dict(project_id=project_id, lanes={})
        index['lanes'][lane] = f'lanes/{lane}/CURRENT.json'
        save(project_root / 'current.json', index)
        save(directory / 'CURRENT.json', dict(schema_version='1.0.0', project_id=project_id, project=project,
             lane=lane, sequence=0, latest_event=None, latest_closed_event=None, status='UNVERIFIED',
             open_debt=[], next_boundary='Read live authorities and record PRE before mutation.'))
        current = load(root / 'CURRENT.json')
        if project not in current['projects']:
            current['projects'].append(project)
        save(root / 'CURRENT.json', current)

def append(root, project, lane, operation, evidence):
    if operation not in OPERATIONS:
        raise ValueError('Unsupported operation')
    directory = lane_root(root, project, lane)
    with lock(root):
        current = load(directory / 'CURRENT.json')
        events = history(directory)
        if (events[-1]['event_id'] if events else None) != current['latest_event']:
            raise ValueError('History/CURRENT mismatch: reconcile interrupted write before continuing')
        if operation == 'PRE':
            if current['status'] in ['OPEN', 'BLOCKED']:
                raise ValueError('Existing sequence is unfinished; do not replay PRE')
            if not evidence.get('pre_commit') or not evidence.get('pre_snapshots'):
                raise ValueError('PRE requires commit anchor and snapshot pointers')
            sequence = current['sequence'] + 1
        else:
            if current['status'] not in ['OPEN', 'BLOCKED']:
                raise ValueError('Start a new sequence with PRE')
            sequence = current['sequence']
        check_evidence(root, evidence)
        ordinal = len(events) + 1
        unknown = dict(status='UNKNOWN', receipt=None)
        event = dict(schema_version='1.0.0', event_id=f'{project}/{lane}/{sequence:06d}/{ordinal:06d}',
                     project_id=current['project_id'], project=project, lane=lane, sequence=sequence,
                     parent_event=current['latest_event'], timestamp=datetime.now(timezone.utc).isoformat(),
                     actor=evidence.get('actor', 'operator'), tool=evidence.get('tool', 'a9-cli'), operation=operation,
                     pre_commit=evidence.get('pre_commit'), pre_snapshots=evidence.get('pre_snapshots', []),
                     post_snapshots=evidence.get('post_snapshots', []), artifacts=evidence.get('artifacts', []),
                     readback=evidence.get('readback', unknown.copy()), qa=evidence.get('qa', unknown.copy()),
                     ack=evidence.get('ack', unknown.copy()), registration=evidence.get('registration', unknown.copy()),
                     release=evidence.get('release'), supersedes=evidence.get('supersedes'),
                     status='CLOSED' if operation == 'CLOSE' else 'OPEN',
                     open_debt=evidence.get('open_debt', current['open_debt']),
                     next_boundary=evidence.get('next_boundary', 'Continue the same bounded sequence.'))
        if operation in ['SUPERSEDE', 'ROLLBACK_POINTER']:
            matches = [e for e in events if e['event_id'] == event['supersedes']]
            if not matches:
                raise ValueError('Correction target must exist in this lane')
            if operation == 'ROLLBACK_POINTER':
                if matches[0]['status'] != 'CLOSED':
                    raise ValueError('Rollback target must be previously closed')
                event['open_debt'] = list(dict.fromkeys(event['open_debt'] + ['Verify rollback pointer and provider state']))
                event['status'] = 'BLOCKED'
        from jsonschema import Draft202012Validator, FormatChecker
        Draft202012Validator(load(root / 'schemas/event.schema.json'), format_checker=FormatChecker()).validate(event)
        if operation == 'CLOSE':
            check_close(root, events, event)
        if operation in ['TAG', 'RELEASE']:
            check_close(root, events, event)
            if not event['release']:
                raise ValueError('Milestone operation requires an actual tag/release reference')
        save(directory / 'events' / f'{ordinal:06d}.json', event)
        current.update(sequence=sequence, latest_event=event['event_id'], status=event['status'],
                       open_debt=event['open_debt'], next_boundary=event['next_boundary'])
        if operation == 'CLOSE':
            current['latest_closed_event'] = event['event_id']
        save(directory / 'CURRENT.json', current)
        sequence_path = directory.parents[1] / 'sequences' / f'{lane}-{sequence:06d}.json'
        seq = load(sequence_path) if sequence_path.exists() else dict(project_id=current['project_id'], lane=lane,
                sequence=sequence, pre_event=event['event_id'], close_event=None, status='OPEN')
        if operation == 'CLOSE':
            seq.update(close_event=event['event_id'], status='CLOSED')
        save(sequence_path, seq)
        project_root = directory.parents[1]
        debt = load(project_root / 'debt.json')
        for item in debt['items']:
            if item['lane'] == lane and item['status'] == 'OPEN' and item['description'] not in event['open_debt']:
                item.update(status='RESOLVED', resolution_event=event['event_id'])
        for description in event['open_debt']:
            debt_id = hashlib.sha256(f'{lane}:{description}'.encode()).hexdigest()[:16]
            item = next((item for item in debt['items'] if item['debt_id'] == debt_id), None)
            if item:
                item.update(status='OPEN', resolution_event=None)
            else:
                debt['items'].append(dict(debt_id=debt_id, lane=lane, status='OPEN', description=description, resolution_event=None))
        save(project_root / 'debt.json', debt)
        if operation == 'CLOSE':
            root_current = load(root / 'CURRENT.json')
            root_current['latest_closed_event'] = event['event_id']
            save(root / 'CURRENT.json', root_current)
        return event

def resume(root, project, lane):
    current = load(lane_root(root, project, lane) / 'CURRENT.json')
    return dict(authorities='Drive scientific artifacts; GitHub governance; A7 identity/routing.',
                current=f'projects/{project}/lanes/{lane}/CURRENT.json', latest_closed_event=current['latest_closed_event'],
                status=current['status'], open_debt=current['open_debt'], next_boundary=current['next_boundary'],
                do_not_replay=['Do not rerun a PRE for an unfinished sequence.', 'Read live scientific authorities on demand.',
                               'Local receipts alone do not establish remote provider readback.'])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['init', 'append', 'resume'])
    parser.add_argument('--project', required=True)
    parser.add_argument('--lane', required=True)
    parser.add_argument('--project-id')
    parser.add_argument('--operation', choices=OPERATIONS)
    parser.add_argument('--evidence', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'init':
            init(ROOT, args.project, args.project_id or '', args.lane)
        elif args.command == 'append':
            if not args.operation or not args.evidence:
                parser.error('append requires --operation and --evidence')
            print(json.dumps(append(ROOT, args.project, args.lane, args.operation, load(args.evidence)), indent=2))
        else:
            print(json.dumps(resume(ROOT, args.project, args.lane), indent=2))
    except (ValueError, FileNotFoundError, FileExistsError) as error:
        parser.exit(1, f'A9 BLOCKED: {error}\n')

if __name__ == '__main__':
    main()
