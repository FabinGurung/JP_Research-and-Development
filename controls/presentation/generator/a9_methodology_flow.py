"""A9 shared academic methodology flow, researcher-neutral.

Validates research process lineage, then paginates horizontal left-to-right
flows without changing their scientific meaning. It cannot certify whether a
procedure actually occurred at a research site.
"""
from __future__ import annotations
from copy import deepcopy
import re

METHOD_TYPE = 'methodology_flow'
LAYOUT = 'horizontal_linear'
ALLOWED_CATEGORIES = {'INPUT', 'PREPARATION', 'FIELD', 'SCREENING', 'VERIFICATION', 'ANALYSIS', 'OUTPUT'}
ADMITTED = {'ADMITTED_CURRENT', 'APPROVED_CURRENT'}
NUM_PER_SLIDE = 6  # 10 x 7.5-in academic landscape: do not reduce font to fit 7+
UNSUPPORTED_ASSERTION = re.compile(r'\b(?:proven causes?|confirmed rework cases?|citywide rework rate|measured financial losses?)\b', re.I)


def _t(value):
    return value.strip() if isinstance(value, str) else ''


def validate_methodology(content, evidence_map=None, *, fixture=False):
    errors, warnings = [], []
    slides = content.get('slides') if isinstance(content, dict) else []
    slides = slides if isinstance(slides, list) else []
    flows = [(i, s) for i, s in enumerate(slides, 1)
             if isinstance(s, dict) and s.get('type') == METHOD_TYPE]
    if not flows:
        return {'ok': True, 'errors': [], 'warnings': [], 'flow_count': 0, 'stages': 0}
    if not fixture and not isinstance(evidence_map, dict):
        errors.append('methodology_flow requires current project-specific evidence_map')
    admitted = {}
    if isinstance(evidence_map, dict):
        for src in evidence_map.get('sources', []):
            if isinstance(src, dict) and _t(src.get('source_id')):
                admitted[src['source_id']] = src.get('admission_status')
    total = 0
    for i, flow in flows:
        loc = f'slide {i} methodology_flow'
        if flow.get('scientific_role') != 'METHOD':
            errors.append(f'{loc}: scientific_role must be METHOD')
        if flow.get('layout', LAYOUT) != LAYOUT:
            errors.append(f'{loc}: only implemented layout is {LAYOUT}')
        if flow.get('direction', 'left_to_right') != 'left_to_right':
            errors.append(f'{loc}: direction must be left_to_right')
        steps = flow.get('stages')
        if not isinstance(steps, list) or len(steps) < 3:
            errors.append(f'{loc}: require at least 3 non-empty stages')
            continue
        if len(steps) > 24:
            errors.append(f'{loc}: maximum 24 stages across automatically paginated slides')
        max_per_slide = flow.get('max_stages_per_slide', NUM_PER_SLIDE)
        if not isinstance(max_per_slide, int) or isinstance(max_per_slide, bool) or not 3 <= max_per_slide <= NUM_PER_SLIDE:
            errors.append(f'{loc}: max_stages_per_slide must be 3..{NUM_PER_SLIDE}')
        ids = []
        for j, stage in enumerate(steps, 1):
            total += 1
            tag = f'{loc} stage {j}'
            if not isinstance(stage, dict):
                errors.append(f'{tag}: expected object'); continue
            sid = _t(stage.get('stage_id'))
            if not sid or sid in ids or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]{0,23}', sid):
                errors.append(f'{tag}: stage_id must be unique and machine-stable')
            ids.append(sid)
            for field, maxlen in [('title', 38), ('description', 100), ('output', 95)]:
                v = _t(stage.get(field))
                if not v or len(v) > maxlen:
                    errors.append(f'{tag}: {field} required, 1..{maxlen} chars')
                if UNSUPPORTED_ASSERTION.search(v):
                    errors.append(f'{tag}: unqualified scientific confirmation/cost assertion; revise wording')
            if stage.get('category') not in ALLOWED_CATEGORIES:
                errors.append(f'{tag}: category invalid')
            if not _t(stage.get('manuscript_locator')):
                errors.append(f'{tag}: manuscript_locator is required')
            refs = stage.get('evidence_refs')
            if not isinstance(refs, list) or not refs or any(not _t(x) for x in refs):
                errors.append(f'{tag}: evidence_refs must name actual source ID(s)')
            elif not fixture:
                for ref in refs:
                    if admitted.get(ref) not in ADMITTED:
                        errors.append(f'{tag}: source {ref} not present/admitted in evidence_map')
            if j == len(steps) and stage.get('category') == 'OUTPUT' and 'finding' in _t(stage.get('title')).lower():
                warnings.append(f'{tag}: check output does not imply completed empirical findings')
        connectors = flow.get('connectors')
        if connectors is not None:
            expected = [(ids[j], ids[j+1]) for j in range(len(ids)-1)]
            supplied = [(x.get('from'), x.get('to')) if isinstance(x, dict) else (None, None)
                        for x in connectors] if isinstance(connectors, list) else []
            if supplied != expected:
                errors.append(f'{loc}: horizontal_linear connectors must be exact adjacent stages, without cycles or omissions')
        if len(steps) > NUM_PER_SLIDE:
            warnings.append(f'{loc}: auto-pagination across {((len(steps)-1)//NUM_PER_SLIDE)+1} slides')
    return {'ok': not errors, 'errors': errors, 'warnings': warnings,
            'flow_count': len(flows), 'stages': total}


def expand_methodology_flows(content):
    out = deepcopy(content)
    rendered = []
    for slide in out.get('slides', []):
        if slide.get('type') != METHOD_TYPE:
            rendered.append(slide); continue
        steps = slide['stages']
        n = slide.get('max_stages_per_slide', NUM_PER_SLIDE)
        pages = [steps[j:j+n] for j in range(0, len(steps), n)]
        for index, subset in enumerate(pages, 1):
            item = {k: v for k, v in slide.items() if k not in {'stages', 'connectors'}}
            item['stages'] = deepcopy(subset)
            item['page_in_section'] = index
            item['page_total'] = len(pages)
            if len(pages) > 1:
                item['title'] = f"{slide.get('title', 'Methodology')} ({index}/{len(pages)})"
            rendered.append(item)
    out['slides'] = rendered
    return out
