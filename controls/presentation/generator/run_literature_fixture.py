"""Non-scientific synthetic render comparison: never use for a thesis release."""
from pathlib import Path
import json,hashlib,subprocess,sys
from PIL import Image,ImageDraw
from test_a9_literature_table import case
HERE=Path(__file__).resolve().parent
out=HERE/'literature_fixture_output';out.mkdir(exist_ok=True)
logo=out/'generated_test_logo.png'
im=Image.new('RGB',(200,200),'white');d=ImageDraw.Draw(im);d.rectangle((4,4,195,195),outline='black',width=4);d.text((24,95),'FIXTURE',fill='black');im.save(logo)
for cols in (3,4):
 c,m=case(n=5,columns=cols)
 c['metadata'].update({'title':'Synthetic literature table renderer test','researcher':'DEMO TEST ONLY','date':'October 2026',
   'program':'Software QA fixture only','logo':str(logo),'logo_sha256':hashlib.sha256(logo.read_bytes()).hexdigest(),
   'supervisor_available':True,'supervisor':{'name':'DEMO SUPERVISOR'},'co_supervisors_available':False})
 c['slides'].insert(0,{'type':'title','title':'Synthetic Literature Layout Test','subtitle':'No real study referenced', 'scientific_role':'NON_SCIENTIFIC'})
 c['slides'].append({'type':'closing','title':'Test Complete','subtitle':'QA only', 'scientific_role':'NON_SCIENTIFIC'})
 theme=json.loads((HERE/'theme.default.json').read_text())
 theme['branding']['canonical_logo_sha256']=c['metadata']['logo_sha256']
 for name,obj in [('content',c),('theme',theme),('evidence_map',m)]:
  (out/f'{name}_{cols}.json').write_text(json.dumps(obj,indent=2))
 cmd=[sys.executable,str(HERE/'build.py'),'--content',str(out/f'content_{cols}.json'),'--theme',str(out/f'theme_{cols}.json'),
    '--out-dir',str(out/f'{cols}col'),'--evidence-map',str(out/f'evidence_map_{cols}.json')]
 cp=subprocess.run(cmd,capture_output=True,text=True)
 if cp.returncode:
  print(cp.stdout,cp.stderr,file=sys.stderr);sys.exit(cp.returncode)
 report=json.loads((out/f'{cols}col'/'release_manifest.json').read_text())
 print(f'{cols}-column PASS pages={report["render_count"]} literature={report["literature_matrix_pages"]}')
