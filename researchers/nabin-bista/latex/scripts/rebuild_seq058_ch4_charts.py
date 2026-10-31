from pathlib import Path
import re,json,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
ROOT=Path(__file__).resolve().parents[1]
tex=(ROOT/'24_resultanddiscussion.tex').read_text()
S=['Fixed','Hard','Medium','Soft']
labels=['1','2','3','4','5','6']
plot_dir=ROOT/'figures/ch4/seq058';plot_dir.mkdir(parents=True,exist_ok=True)

def rows_for(label):
 pat=r'\\begin\{longtable\}.*?\\caption\{.*?\\label\{'+re.escape(label)+r'\}\\\\(.*?)\\end\{longtable\}'
 m=re.search(pat,tex,re.S)
 if not m:raise ValueError('missing '+label)
 out=[]
 for line in m.group(1).splitlines():
  l=line.strip();
  if not re.match(r'^\d\s*&',l):continue
  if l.endswith(r'\\'):l=l[:-2]
  vals=[v.strip() for v in l.split('&')]
  out.append(vals)
 return out

def number(x):
 m=re.search(r'-?\d+(?:,\d{3})*(?:\.\d+)?',x)
 if not m:return float('nan')
 return float(m.group(0).replace(',',''))

def grouped(label, keys):
 a=rows_for(label); out={}
 for metric, col in keys.items():
  v=np.full((6,4),np.nan)
  for row in a:
   block=int(row[0])-1
   if label == 'tab:seq54_modal':
    for i in range(4):v[block,i]=number(row[1+i])
    continue
   if label=='tab:seq54_mass':
    for i in range(4):v[block,i]=number(row[1+i])
    continue
   supp=row[1].capitalize();index=S.index(supp)
   v[block,index]=number(row[col])
  out[metric]=v
 return out

all_data={}
all_data.update(grouped('tab:seq54_modal',{'fundamental_period':1}))
all_data.update(grouped('tab:seq54_mass',{'modal_mass_90':1}))
all_data.update(grouped('tab:seq54_disp',{'roof_disp_x':2,'roof_disp_y':3}))
all_data.update(grouped('tab:seq54_drift',{'max_drift_x':2,'max_drift_y':3}))
all_data.update(grouped('tab:seq54_baseshear',{'base_shear_x':2}))
all_data.update(grouped('tab:seq54_storyshear',{'story_shear_x':2,'story_shear_y':3}))
all_data.update(grouped('tab:seq54_foundation',{'foundation_settlement':2,'foundation_reaction':3}))
all_data.update(grouped('tab:seq54_force',{'beam_shear_envelope':2,'beam_moment_envelope':3,'column_axial_envelope':4,'column_moment_envelope':6}))
# Exclude provenance-flagged foundation reaction entries; do not silently invent numeric substitutes.
all_data['foundation_reaction'][4,1]=np.nan
all_data['foundation_reaction'][2,0]=np.nan

sources={
'fundamental_period':('Fundamental period','First-mode period (s)'),
'modal_mass_90':('90% participating mass','First qualifying mode number'),
'roof_disp_x':('Response-spectrum displacement · X','Uppermost-storey displacement (mm)'),
'roof_disp_y':('Response-spectrum displacement · Y','Uppermost-storey displacement (mm)'),
'max_drift_x':('Response-spectrum inter-storey drift · X','Maximum drift (%)'),
'max_drift_y':('Response-spectrum inter-storey drift · Y','Maximum drift (%)'),
'base_shear_x':('Response-spectrum base shear · X','Base shear (kN)'),
'story_shear_x':('Response-spectrum storey shear · X','Maximum storey shear (kN)'),
'story_shear_y':('Response-spectrum storey shear · Y','Maximum storey shear (kN)'),
'foundation_settlement':('Foundation movement · gravity combination','Maximum vertical settlement (mm)'),
'foundation_reaction':('Foundation reaction · gravity combination','Vertical reaction (kN)'),
'beam_shear_envelope':('Beam shear envelope · gravity combination','Maximum |V₂| (kN)'),
'beam_moment_envelope':('Beam moment envelope · gravity combination','Maximum |M₃| (kN·m)'),
'column_axial_envelope':('Column axial envelope · gravity combination','Maximum |P| (kN)'),
'column_moment_envelope':('Column moment envelope · gravity combination','Maximum |M₃| (kN·m)'),
}

plt.rcParams.update({'font.family':'DejaVu Serif','font.size':9,'axes.labelsize':10,'axes.titlesize':11,'xtick.labelsize':8,'ytick.labelsize':9,'pdf.fonttype':42,'axes.spines.right':False,'axes.spines.top':False})
files=[]
for key,data in all_data.items():
 title,ylabel=sources[key]
 fig,ax=plt.subplots(figsize=(8.8,4.2),dpi=200)
 handles=[]
 for i,block in enumerate(labels):
  v=data[i].copy()
  if key in ('max_drift_x','max_drift_y'):v*=1 # already percentage in Table 4.4
  if np.all(np.isnan(v)):continue
  # Real four-case comparisons (not fictional intermediate storey-profile data).
  h=ax.plot(range(4),v,marker=['o','s','D','^','v','P'][i],linewidth=1.6,markersize=5.8,label='Block '+block)[0]
  handles.append(h)
 ax.set_xticks(range(4),S)
 ax.set_xlim(-0.1,3.1)
 ax.grid(axis='y',alpha=.2,linewidth=.7)
 ax.set_axisbelow(True)
 ax.set_title(title,loc='left',pad=13,fontweight='semibold')
 ax.set_xlabel('Foundation support condition')
 ax.set_ylabel(ylabel)
 ax.legend(handles=handles,loc='upper center',bbox_to_anchor=(.5,-.21),ncol=6,frameon=False,fontsize=8)
 fig.subplots_adjust(left=.13,right=.97,top=.87,bottom=.30)
 out=plot_dir/(key+'.pdf');fig.savefig(out);fig.savefig(plot_dir/(key+'.png'),dpi=180);plt.close(fig)
 files.append({'figure':key,'path':str(out.relative_to(ROOT)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'values':[[None if np.isnan(x) else float(x) for x in a]for a in data]})
# Replace only asset references and captions in current chapter; preserve tables and paragraphs verbatim.
new=tex
for key in all_data:
 if key=='story_shear_y':p='figures/ch4/seq055/story_shear_y.png'
 else:p='figures/ch4/seq055/'+key+'.pdf'
 newp='figures/ch4/seq058/'+key+'.pdf'
 if p in new:new=new.replace(p,newp)
 elif newp not in new:raise AssertionError(p)
# Scope caption changes only on the 15 previously existing chapter 4 figures.
caps={
'fig:seq55_fundamental_period':'First-mode period for each hospital block under fixed, hard-, medium- and soft-support conditions (source: modal-analysis values in Table~\\ref{tab:seq54_modal}).',
'fig:seq55_modal_mass_90':'Earliest mode satisfying 90\\% cumulative participation in both horizontal directions for each block (source: modal-analysis values in Table~\\ref{tab:seq54_mass}).',
'fig:seq55_roof_disp_x':'Uppermost-storey displacement, X-direction response-spectrum case; comparison by block and foundation support (source: Table~\\ref{tab:seq54_disp}).',
'fig:seq55_roof_disp_y':'Uppermost-storey displacement, Y-direction response-spectrum case; comparison by block and foundation support (source: Table~\\ref{tab:seq54_disp}).',
'fig:seq55_max_drift_x':'Maximum inter-storey drift, X-direction response-spectrum case (source: Table~\\ref{tab:seq54_drift}).',
'fig:seq55_max_drift_y':'Maximum inter-storey drift, Y-direction response-spectrum case (source: Table~\\ref{tab:seq54_drift}).',
'fig:seq55_base_shear_x':'X-direction response-spectrum base shear by block and foundation condition (source: Table~\\ref{tab:seq54_baseshear}).',
'fig:seq55_story_shear_x':'Maximum X-direction response-spectrum storey shear by block and foundation condition (source: Table~\\ref{tab:seq54_storyshear}).',
'fig:seq55_story_shear_y':'Maximum Y-direction response-spectrum storey shear by block and foundation condition (source: Table~\\ref{tab:seq54_storyshear}).',
'fig:seq55_foundation_settlement':'Maximum foundation settlement under the $1.2DL+1.5LL$ combination (source: Table~\\ref{tab:seq54_foundation}).',
'fig:seq55_foundation_reaction':'Vertical foundation reaction under $1.2DL+1.5LL$; provenance-flagged entries excluded (source: Table~\\ref{tab:seq54_foundation}).',
'fig:seq55_beam_shear_envelope':'Maximum absolute beam shear $|V_2|$ under $1.2DL+1.5LL$ (source: Table~\\ref{tab:seq54_force}).',
'fig:seq55_beam_moment_envelope':'Maximum absolute beam bending moment $|M_3|$ under $1.2DL+1.5LL$ (source: Table~\\ref{tab:seq54_force}).',
'fig:seq55_column_axial_envelope':'Maximum absolute column axial force $|P|$ under $1.2DL+1.5LL$ (source: Table~\\ref{tab:seq54_force}).',
'fig:seq55_column_moment_envelope':'Maximum absolute column moment $|M_3|$ under $1.2DL+1.5LL$ (source: Table~\\ref{tab:seq54_force}).',
}
for label,caption in caps.items():
 pat=r'\\caption\{([^{}]*)\}\\label\{'+re.escape(label)+r'\}'
 # Old captions may include math braces; instead find simple line containing label.
 lines=new.splitlines(keepends=True);found=False
 for j,line in enumerate(lines):
  if '\\label{'+label+'}' in line and '\\caption{' in line:
   lines[j]='\\caption{'+caption+'}\\label{'+label+'}\n';found=True;break
 if found:new=''.join(lines)
# Y-direction plot did not have label in R3; update just line after includegraphics.
pat=r'(\\includegraphics\[[^\n]*\]\{figures/ch4/seq058/story_shear_y.pdf\}\n)\\caption\{[^\n]*\}'
new,n=re.subn(pat,lambda m:m.group(1)+'\\caption{'+caps['fig:seq55_story_shear_y']+'}',new,count=1)
assert n==1,n
(ROOT/'24_resultanddiscussion.tex').write_text(new)
(ROOT/'SEQ058_FIGURE_SOURCE_MAP.json').write_text(json.dumps({'base':'LATEX_SEQ057_R3','planned':'LATEX_SEQ058','source':'Existing Nabin Table 4.1-4.8 literal rows','charts':files,'excluded_source_flags':['Block3 fixed vertical reaction','Block5 hard vertical reaction'],'no_researcher_data_from_SEQ049':True},indent=2)+'\n')
print('Generated',len(files),'source-derived figure PDFs and replaced existing chapter figure references and captions')
