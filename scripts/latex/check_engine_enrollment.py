#!/usr/bin/env python3
"""Validate live routing for every enrolled identity; never admits thesis content."""
import json
import subprocess
import sys
from pathlib import Path
from researcher_sequence import validate, reservation_delta, LEDGER
ROOT = Path(__file__).resolve().parents[2]
def load(p): return json.loads((ROOT / p).read_text())
def check():
    enrolled = load('registry/researchers.json')['researchers']
    inheritance = load('registry/latex-inheritance.json')['researchers']
    ledger = load(LEDGER)
    validate(ledger, enrolled)
    assert {(r['researcher_id'],r['slug']) for r in enrolled} == {(r['researcher_id'],r['slug']) for r in inheritance}
    for row in enrolled:
        entry = f"researchers/{row['slug']}/AGENTS.md"
        assert row['governance']['read_first'] == entry
        assert (ROOT / entry).is_file()
        inherited = next(x for x in inheritance if x['slug'] == row['slug'])
        assert inherited['engine_entrypoint'] == entry
        assert inherited['engine_protocol'] == 'docs/RESEARCHER_ENGINE_READ_FIRST.md'
        assert inherited['semantic_policy_version'] == load('controls/latex/authorial-voice-policy.json')['version']
        assert inherited['tower'] == 'controls/latex/tower.json'
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
