#!/usr/bin/env python3
"""Validate live routing for every enrolled identity; never admits thesis content."""
import json
import subprocess
import sys
from pathlib import Path
from researcher_sequence import validate, reservation_delta, LEDGER
ROOT = Path(__file__).resolve().parents[2]
def load(p): return json.loads((ROOT / p).read_text())
EVIDENCE_MARKER = '## Evidence-first execution'
def check(root=ROOT):
    def read(p): return json.loads((root / p).read_text())
    enrolled = read('registry/researchers.json')['researchers']
    inheritance = read('registry/latex-inheritance.json')['researchers']
    ledger = read(LEDGER)
    validate(ledger, enrolled)
    def identities(rows, slug='slug'):
        ids=[r['researcher_id'] for r in rows]; slugs=[r[slug] for r in rows]
        assert len(ids)==len(set(ids)) and len(slugs)==len(set(slugs)), 'Duplicate owner identity'
        return set(zip(ids,slugs))
    expected=identities(enrolled)
    assert expected == identities(inheritance), 'Inheritance enrollment mismatch'
    profiles=read('registry/latex-build-profiles.json')['profiles']
    assert expected == identities(profiles,'researcher_slug'), 'Build profile enrollment mismatch'
    tower=read('controls/latex/tower.json')
    policy=read(tower['rules']['semantic'])
    assert policy['canonical_owner']=='controls/latex/tower.json'
    assert {'RD-LTX-SEM-002','RD-LTX-SEM-005','RD-LTX-SEM-007','RD-LTX-SEM-011','RD-LTX-SEM-012','RD-LTX-SEM-013'} <= {x['id'] for x in policy['rules']}
    for path in [tower['template_entry'], *tower['rules']['dependencies']]:
        assert (root/path).is_file(), 'Missing shared dependency: '+path
    extensions=read('controls/latex/extension-registry.json')['registered']
    assert len({e['extension_id'] for e in extensions})==len(extensions)
    for row in enrolled:
        entry = f"researchers/{row['slug']}/AGENTS.md"
        assert row['governance']['read_first'] == entry
        assert (root / entry).is_file()
        text=(root/entry).read_text()
        assert f"{row['researcher_id']} / {row['slug']}" in text, 'Entrypoint owner mismatch'
        assert EVIDENCE_MARKER in text and 'docs/RESEARCHER_ENGINE_READ_FIRST.md' in text, 'Evidence-first routing absent'
        assert row['governance']['engine_protocol']=='docs/RESEARCHER_ENGINE_READ_FIRST.md'
        assert row['governance']['inheritance_registry']=='registry/latex-inheritance.json'
        assert row['governance']['sequence_register']==LEDGER
        inherited = next(x for x in inheritance if x['slug'] == row['slug'])
        assert inherited['engine_entrypoint'] == entry
        assert inherited['engine_protocol'] == 'docs/RESEARCHER_ENGINE_READ_FIRST.md'
        assert inherited['semantic_policy_version'] == policy['version']
        assert inherited['tower'] == 'controls/latex/tower.json'
        assert inherited['template']==tower['template_entry'] and inherited['no_local_base_copy'] is True
        assert inherited['semantic_policy']==tower['rules']['semantic']
        assert inherited['semantic_checker']==tower['rules']['validation']
        if inherited['local_configuration']:
            path=inherited['local_configuration']
            assert path.startswith(f"researchers/{row['slug']}/") and (root/path).is_file()
        for ext_id in inherited['unique_extension_ids']:
            ext=next(e for e in extensions if e['extension_id']==ext_id)
            assert ext['researcher_id']==row['researcher_id'] and ext['owner']==row['slug'], 'Extension owner mismatch'
            assert ext['path'].startswith(f"researchers/{row['slug']}/latex/extensions/") and (root/ext['path']).is_file()
        profile=next(p for p in profiles if p['researcher_id']==row['researcher_id'])
        assert profile['source_root']==f"researchers/{row['slug']}/latex/manuscript"
        assert profile['entrypoint'].startswith(profile['source_root']+'/')
        assert profile['compile_on_push'] is False and profile['production_permission']=='NOT_GRANTED'
        assert not list((root/f"researchers/{row['slug']}").rglob('pumlsc-shared.sty')), 'Cloned shared template'
    print(f'ENGINE_ENROLLMENT_PASS {len(enrolled)} owners; no manuscript certification')
if __name__ == '__main__':
    check()
    if len(sys.argv) > 1:
        base, head, branch = sys.argv[1:]
        files = subprocess.check_output(['git','diff','--name-only',base+'...'+head],cwd=ROOT,text=True).splitlines()
        if branch.startswith('reservation/latex/'):
            assert files == [LEDGER], 'Reservation PR may only change ledger'
            before = json.loads(subprocess.check_output(['git','show',base+':'+LEDGER],cwd=ROOT,text=True))
            reservation_delta(before, load(LEDGER), branch)
            print('RESERVATION_APPEND_GATE_PASS')
        elif LEDGER in files:
            before = json.loads(subprocess.check_output(['git','show',base+':'+LEDGER],cwd=ROOT,text=True))
            after = load(LEDGER)
            assert {r['slug']:r['reservations'] for r in before['researchers']} == {r['slug']:r['reservations'] for r in after['researchers']}, 'Reservation changes require a dedicated reservation PR'
