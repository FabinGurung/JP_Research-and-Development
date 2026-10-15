#!/usr/bin/env python3
"""Private input JSON -> LaTeX DRAFT. Layout engine only, not FE solver/engineering approval."""
import argparse, json, re, shutil, subprocess
from pathlib import Path

TEMPLATE=Path(__file__).resolve().parents[2]/'templates/enterprise/structural-analysis-report/v0.1/main.tex'
STATUS={'UNVERIFIED_SOURCE_CLAIM','SOLVER_RESULT_UNCHECKED','HOLD','VALIDATED_WITH_EVIDENCE'}
NEEDED={'result_id','run_id','model_sha256','source_authority_id','validation_id'}

def tex(value):
    s=str(value)
    return ''.join({'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}.get(c,c) for c in s)

def validate(data):
    if data.get('schema')!='jp.structural-report.input.v0.1':raise ValueError('Unrecognized input schema')
    meta=data.get('metadata')
    if not isinstance(meta,dict):raise ValueError('Missing metadata')
    for key in ('report_id','project_id','title','building_usage','revision','authority_id'):
        if not isinstance(meta.get(key),str) or not meta[key].strip():raise ValueError('Missing metadata.'+key)
    secs=data.get('sections')
    if not isinstance(secs,list) or not secs:raise ValueError('Missing sections')
    seen=set()
    for s in secs:
        if not isinstance(s,dict) or not re.fullmatch(r'[a-z][a-z0-9_]*',str(s.get('id',''))):raise ValueError('Invalid section id')
        if s['id'] in seen:raise ValueError('Duplicate section id')
        seen.add(s['id'])
        if not isinstance(s.get('title'),str):raise ValueError('Missing section title')
        for c in s.get('claims',[]):
            if c.get('status') not in STATUS:raise ValueError('Unrecognized claim status')
            if c['status']=='VALIDATED_WITH_EVIDENCE':
                if any(not c.get(k) for k in NEEDED):raise ValueError('Missing evidence for validated claim')
                if c.get('source')=='ETABS_SCREENSHOT':raise ValueError('Screenshot alone cannot validate a result')
    return data

def render(data):
    validate(data)
    m=data['metadata']
    out=[r'{\Huge\bfseries '+tex(m['title'])+'}',r'\par\bigskip',
       r'\colorbox{yellow!20}{\parbox{0.95\linewidth}{\textbf{DRAFT - ENGINEERING ACCEPTANCE HOLD.} Compiling this document does not establish model correctness, NBC compliance, project approval or an engineer\textquotesingle s signature.}}',
       r'\bigskip',r'\begin{longtable}{@{}p{.35\linewidth}p{.61\linewidth}@{}}']
    for f in ('report_id','project_id','building_usage','revision','authority_id'):
        out.append(r'\textbf{'+tex(f.replace('_',' ').title())+'} & '+tex(m[f])+r'\\')
    out.extend([r'\end{longtable}',r'\tableofcontents',r'\clearpage'])
    for section in data['sections']:
        out.append(r'\section{'+tex(section['title'])+'}')
        out.append(tex(section.get('narrative','')))
        if section.get('claims'):
            out.append(r'\small\begin{longtable}{@{}p{.27\linewidth}p{.18\linewidth}p{.16\linewidth}p{.30\linewidth}@{}}')
            out.append(r'\toprule Item & Value & Status & Traceability \\ \midrule')
            for c in section['claims']:
                trace='; '.join(str(c[k]) for k in ('result_id','run_id','model_sha256','source_authority_id','validation_id') if c.get(k)) or 'NOT ESTABLISHED'
                out.append('{} & {} & {} & {} \\\\'.format(tex(c.get('label','')),tex(str(c.get('value',''))+' '+str(c.get('unit',''))),tex(c['status']),tex(trace)))
            out.append(r'\bottomrule\end{longtable}\normalsize')
    out.append(r'\section*{Evidence and professional gate}')
    out.append('Unverified entries remain on HOLD. Independent model/input checks, adopted code edition, member design, and professional review are required before construction use.')
    return '\n'.join(out)+'\n'

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True);p.add_argument('--out',required=True);p.add_argument('--compile',action='store_true')
    args=p.parse_args()
    d=json.loads(Path(args.input).read_text(encoding='utf-8'))
    dest=Path(args.out);dest.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(TEMPLATE,dest/'main.tex')
    (dest/'project_content.tex').write_text(render(d),encoding='utf-8')
    (dest/'qa.json').write_text(json.dumps({'status':'DRAFT_NOT_ENGINEERING_CERTIFIED','claims':sum(len(s.get('claims',[])) for s in d['sections'])},indent=2)+'\n')
    if args.compile:
        if shutil.which('pdflatex') is None:raise SystemExit('pdflatex unavailable')
        for _ in range(2):
            subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'],cwd=dest,check=True,stdout=subprocess.DEVNULL)
    print('REPORT_DRAFT_WRITTEN',dest)
if __name__=='__main__':main()
