#!/usr/bin/env python3
"""Read-only all-owner governance/semantic inventory; never a science certificate."""
import collections
import hashlib
import json
import subprocess
from pathlib import Path
import check_engine_enrollment as enrollment
import check_authorial_voice as voice
import researcher_sequence as sequence


def audit():
    root = enrollment.ROOT
    enrollment.check()
    people = enrollment.load('registry/researchers.json')['researchers']
    ledger = enrollment.load(sequence.LEDGER)
    rows = []
    for owner in people:
        slug = owner['slug']
        files = voice.sources(root, slug)
        warnings = [hit for path in files for hit in voice.inspect_text(path.read_text(), path.relative_to(root).as_posix())]
        baseline = next(r for r in ledger['researchers'] if r['slug'] == slug)
        rows.append({
            'researcher_id': owner['researcher_id'], 'slug': slug,
            'governance': 'PASS_SOURCE_ROUTING_ONLY',
            'entrypoint': owner['governance']['read_first'],
            'sequence_baseline': baseline['baseline']['status'],
            'sequence_highwater': max([baseline['baseline']['last_historical_sequence'] or 0] + [r['sequence'] for r in baseline.get('observed_out_of_band_versions', [])]) or None,
            'reservations': len(baseline['reservations']),
            'source_files_scanned': len(files),
            'source_inventory': [{'path': p.relative_to(root).as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in files],
            'semantic_status': 'ADVISORY_SCAN_ONLY' if files else 'NO_LOCAL_MANUSCRIPT__NOT_TESTED',
            'advisory_counts': dict(collections.Counter(w['rule'] for w in warnings)),
            'advisory_findings': warnings,
            'drive_root_pointer': 'REGISTERED_REQUIRES_PROVIDER_READ' if owner['drive'].get('project_root_drive_id') else 'HOLD_NO_VERIFIED_ROOT',
            'scientific_truth': 'NOT_CERTIFIED', 'production_pdf': 'NOT_TESTED_OR_CHANGED',
        })
    return {
        'base_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
        'scope': 'Public Git governance routing and advisory source lint only; no private scientific data or PDF audit',
        'shared_style_blob': subprocess.check_output(['git','hash-object',sequence.STYLE],cwd=root,text=True).strip(),
        'policy_version': enrollment.load('controls/latex/authorial-voice-policy.json')['version'],
        'researchers': rows,
        'limitations': ['Source lint does not establish scientific truth.', 'Zero local source files means not tested, never a pass.', 'Drive metadata is not byte/content readback.', 'No live reservation write test or real sequence allocation.', 'No automatic update to other chat threads.'],
    }


if __name__ == '__main__':
    # Enrollment check emits a brief PASS; JSON is separate for script consumers.
    import contextlib
    import io
    with contextlib.redirect_stdout(io.StringIO()):
        result = audit()
    print(json.dumps(result, indent=2))
