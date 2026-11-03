from pathlib import Path
import json,re,hashlib,zipfile,sys,subprocess,csv,io
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.lines import Line2D
from PIL import Image
import fitz
from scipy.special import ndtr

P=Path(__file__).resolve().parents[1]
ROOT=P/'.seq067_rebuild'
ROOT.mkdir(exist_ok=True)
with zipfile.ZipFile(P/'source_originals_20261029/RESULT PLOT nabin bista .zip') as z:
    z.extractall(ROOT/'original_results')
OUT=P/'figures/seq067';OUT.mkdir(parents=True,exist_ok=True)
FONT=Path(fm.findfont(fm.FontProperties(family='Times New Roman'),fallback_to_default=False)).parent
for f in FONT.glob('*.ttf'): fm.fontManager.addfont(str(f))
assert fm.FontProperties(fname=str(FONT/'times.ttf')).get_name()=='Times New Roman'
plt.rcParams.update({'font.family':'Times New Roman','font.size':12,'axes.labelsize':12,'axes.titlesize':12,'xtick.labelsize':12,'ytick.labelsize':12,'legend.fontsize':12,'pdf.fonttype':42,'ps.fonttype':42,'axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False,'mathtext.fontset':'custom','mathtext.rm':'Times New Roman','mathtext.it':'Times New Roman:italic','mathtext.bf':'Times New Roman:bold'})
W=(210-30-25)/25.4
replacements={};records=[]
def save(fig,name,source,old=None,details=None):
    # The PDF media box is the exact intended LaTeX size; do not tight-crop it.
    for ax in fig.axes:
        ax.set_title('')
    for ext in ['pdf','png']:
        buf=io.BytesIO();fig.savefig(buf,format=ext,dpi=300)
        data=buf.getvalue();assert len(data)>1000,(name,ext)
        (OUT/(name+'.'+ext)).write_bytes(data)
    row={'name':name,'source':source,'text_font':'Times New Roman','text_size_pt':12,'internal_title':False,'path':f'figures/seq067/{name}.pdf','details':details}
    records.append(row)
    if old:replacements[old]=row['path']
    plt.close(fig)
    return row['path']
def axes(h=3.0,w=W,legend=False):
    fig,ax=plt.subplots(figsize=(w,h))
    fig.subplots_adjust(left=.19 if w<4 else .16,right=.97,top=.94,bottom=.36 if legend else .24)
    ax.grid(True,color='#e6e6e6',lw=.5);ax.set_axisbelow(True)
    return fig,ax
def table_rows(label):
    tex=(P/'24_resultanddiscussion.tex').read_text()
    start=tex.index('\\label{'+label+'}')
    section=tex[start:tex.index('\\end{longtable}',start)]
    return [[s.strip() for s in l.strip().removesuffix('\\\\').split('&')] for l in section.splitlines() if re.match(r'^\s*\d\s*&',l)]
def num(v):
    m=re.search(r'-?\d+(?:,\d{3})*(?:\.\d+)?',v)
    return float(m[0].replace(',','')) if m else np.nan

labels={
'fundamental_period':'First-mode period (s)','modal_mass_90':'First qualifying mode number',
'roof_disp_x':'Uppermost-storey\ndisplacement (mm)','roof_disp_y':'Uppermost-storey\ndisplacement (mm)',
'max_drift_x':'Maximum drift (%)','max_drift_y':'Maximum drift (%)',
'base_shear_x':'Base shear (kN)','story_shear_x':'Maximum storey shear (kN)','story_shear_y':'Maximum storey shear (kN)',
'foundation_settlement':'Maximum vertical\nsettlement (mm)',
'beam_shear_envelope':'Maximum |V₂| (kN)','beam_moment_envelope':'Maximum |M₃| (kN·m)',
'column_axial_envelope':'Maximum |P| (kN)','column_moment_envelope':'Maximum |M₃| (kN·m)'}
srcmap=json.loads((P/'SEQ058_FIGURE_SOURCE_MAP.json').read_text())
for row in srcmap['charts']:
    key=row['figure']
    if key=='foundation_reaction':continue
    vals=np.array(row['values'],dtype=float)
    # Use current SEQ066 table precision and preserve its unresolved values.
    if key in ['story_shear_x','story_shear_y','foundation_settlement']:
        label='tab:seq54_storyshear' if key.startswith('story') else 'tab:seq54_foundation'
        col=3 if key.endswith('_y') else 2
        for r in table_rows(label):vals[int(r[0])-1,['Fixed','Hard','Medium','Soft'].index(r[1])]=num(r[col])
    fig,ax=axes(3.6,legend=True);fig.subplots_adjust(bottom=.40)
    for i,v in enumerate(vals):ax.plot(range(4),v,marker=['o','s','D','^','v','P'][i],lw=1.3,ms=4,label=f'Block {i+1}')
    ax.set_xticks(range(4),['Fixed','Hard','Medium','Soft']);ax.set_xlabel('Foundation support condition');ax.set_ylabel(labels[key])
    ax.legend(loc='upper center',bbox_to_anchor=(.5,-.30),ncol=3,frameon=False,columnspacing=1)
    save(fig,key,'Existing SEQ066 tables and preserved SEQ058 source map',row['path'],{'values':vals.tolist()})
fig,ax=axes(3.6,legend=True);fig.subplots_adjust(bottom=.40)
rx=json.loads((P/'SEQ066_SOURCE_REVIEW_AUDIT.json').read_text())['reaction_cases']
vals=np.zeros((6,4))
for r in rx:
    # Actual keys are checked at execution, no invented value fallback.
    vals[r['block']-1,['fixed','hard','medium','soft'].index(r['support'].lower())]=r['maxFZ']
for j,s in enumerate(['Fixed','Hard','Medium','Soft']):ax.plot(range(1,7),vals[:,j],marker='osD^'[j],lw=1.3,label=s)
ax.set_xticks(range(1,7));ax.set_xlabel('Hospital block');ax.set_ylabel('Maximum support\nreaction (kN)');ax.legend(loc='upper center',bbox_to_anchor=(.5,-.30),ncol=4,frameon=False,columnspacing=1)
save(fig,'max_joint_reaction','SEQ066 joint-reaction workbook audit','figures/ch4/seq066/max_joint_reaction.pdf',{'values':vals.tolist()})

NS={'c':'http://schemas.openxmlformats.org/drawingml/2006/chart'}
def chart_series(path,chart):
    with zipfile.ZipFile(path) as z:root=ET.fromstring(z.read(chart))
    result=[]
    for ser in root.findall('.//c:ser',NS):
        def pts(tag):
            el=ser.find('c:'+tag,NS)
            if el is None:return []
            return [(int(n.attrib['idx']),float(n.find('c:v',NS).text)) for n in el.findall('.//c:pt',NS) if n.find('c:v',NS) is not None]
        x=dict(pts('xVal'));y=dict(pts('yVal'))
        if not x:x=dict(pts('cat'))
        if not y:y=dict(pts('val'))
        ids=sorted(x.keys()&y.keys());result.append(([x[i] for i in ids],[y[i] for i in ids]))
    return result
lineage=json.loads((P/'seq051_assets/SOURCE_CHART_LINEAGE.json').read_text())['records']
frag={}
params={(r['block'],r['support']):r['states'] for r in json.loads((P/'SEQ066_SOURCE_REVIEW_AUDIT.json').read_text())['fragility_reconstruction']}
for row in lineage:
    if 'latex_path' not in row:continue
    src=ROOT/'original_results'/row['source_workbook']
    series=chart_series(src,row['chart_file']);b=row['block_folder'];kind=row['chart_kind'].lower()
    if kind=='fragility':
        n=int(re.search(r'chart(\d+)',row['chart_file'])[1]);name=f'B{b}_fragility_{n}'
        support=['soft','medium','hard','fixed'][n-1]
        original_series=series;series=[];errors=[]
        for j,(x,y) in enumerate(original_series):
            theta=params[(b,support)][j]['theta_workbook_g'];beta=params[(b,support)][j]['beta_total']
            def cdf(xx):
                xx=np.asarray(xx);out=np.zeros_like(xx,dtype=float);nz=xx>0;out[nz]=ndtr(np.log(xx[nz]/theta)/beta);return out
            err=float(np.max(np.abs(cdf(x)-np.array(y))));assert err<1e-12,(b,n,j,err);errors.append(err)
            smooth=np.linspace(0,1,1001);series.append((smooth.tolist(),cdf(smooth).tolist()))
        for small in [False,True]:
            fig,ax=axes(2.22 if small else 3.15,w=W*.48 if small else W,legend=not small)
            if small:fig.subplots_adjust(left=.31,right=.94,top=.92,bottom=.34)
            for j,(x,y) in enumerate(series):ax.plot(x,y,lw=1.15,label=['IO','LS','CP','C'][j])
            ax.set_xlim(0,1);ax.set_ylim(0,1);ax.set_xticks(np.arange(0,1.01,.2));ax.set_yticks(np.arange(0,1.01,.2))
            ax.set_xlabel('Peak ground\nacceleration (PGA)' if small else 'Peak ground acceleration (PGA)')
            ax.set_ylabel('Damage-state\nexceedance\nprobability' if small else 'Damage-state\nexceedance probability')
            if not small:ax.legend(ncol=4,loc='upper center',bbox_to_anchor=(.5,-.27),frameon=False)
            new=save(fig,name+('_panel' if small else ''),row['source_workbook']+' '+row['chart_file'],details={'cached_series':original_series,'support':row['source_sheet'],'max_source_probability_error':max(errors),'rendering':'Existing workbook CDF; no new fit'})
            if not small:
                replacements[row['latex_path']]=new;replacements[row['latex_path'].replace('seq051_assets/source_plots','figures/fragility_seq057')]=new
        frag[(b,n)]=series
    else:
        fig,ax=axes(3.0,legend=True)
        for j,(x,y) in enumerate(series):ax.plot(x,y,lw=1.3,label=['Fixed','Hard','Medium','Soft'][j])
        ax.set_xlabel('Storey displacement (mm)' if 'displacement' in kind else 'Inter-storey drift ratio');ax.set_ylabel('Elevation (m)')
        ax.legend(loc='upper center',bbox_to_anchor=(.5,-.30),ncol=4,frameon=False,columnspacing=.8)
        save(fig,Path(row['latex_path']).stem,row['source_workbook']+' '+row['chart_file'],row['latex_path'],{'cached_series':series})

# B1 and B2 profile images were already derived from the ETABS table, rather than chart caches.
sys.path.insert(0,str(P/'seq054_evidence'))
from xlsx_xml_source_reader import parse_xlsx
for b in [1,2]:
    for typ in ['disp','drift']:
        fname=next((ROOT/f'original_results/RESULT PLOT/BLOCK {b}').glob('STORY '+('DISPLACEMENT' if typ=='disp' else 'DRIFT')+'*.xlsx'))
        sheets=parse_xlsx(fname)
        sn,rows=next(iter(sheets.items()))
        col,ec,vc=(6,7,9) if typ=='disp' else (2,3,5)
        marks=[(rn,r[col]) for rn,r in rows if isinstance(r.get(col),str) and 'TABLE:' in r[col] and 'Story Response' in r[col]]
        fig,ax=axes(3.0,legend=True);details=[]
        for j,(rn,title) in enumerate(marks):
            stop=marks[j+1][0] if j+1<len(marks) else 10**9
            support=next(s for s in ['fixed','hard','medium','soft'] if s in title.lower())
            data=sorted([(float(r[vc]),float(r[ec])) for n,r in rows if rn<n<stop and isinstance(r.get(ec),(int,float)) and isinstance(r.get(vc),(int,float)) and str(r.get(ec+1,'')).lower()=='top'],key=lambda xy:xy[1])
            assert len(data)>=5
            ax.plot([v[0] for v in data],[v[1] for v in data],lw=1.3,label=support.capitalize())
            details.append({'support':support,'sheet':sn,'xy':data})
        ax.set_xlabel('Displacement (mm)' if typ=='disp' else 'Drift ratio');ax.set_ylabel('Elevation (m)')
        ax.legend(ncol=4,loc='upper center',bbox_to_anchor=(.5,-.30),frameon=False,columnspacing=.8)
        save(fig,f'B{b}_{typ}_table_derived',str(fname.relative_to(ROOT)),f'figures/appendix/B{b}_{typ}_seq057_table_derived.png',details)

# Fifth panel: overlay all four damage-state curves for every support, using exactly the original cached points.
fig,ax=axes(3.3,legend=True);fig.subplots_adjust(bottom=.39,left=.16)
styles=[':', '-.', '--','-'];supports=['Soft','Medium','Hard','Fixed'];colors=plt.rcParams['axes.prop_cycle'].by_key()['color']
for n in range(1,5):
    for j,(x,y) in enumerate(frag[(1,n)]):ax.plot(x,y,color=colors[j],ls=styles[n-1],lw=1.2)
ax.set_xlim(0,1);ax.set_ylim(0,1);ax.set_xlabel('Peak ground acceleration (PGA)');ax.set_ylabel('Damage-state\nexceedance probability');ax.set_xticks(np.arange(0,1.01,.2));ax.set_yticks(np.arange(0,1.01,.2))
l1=ax.legend([Line2D([],[],color=colors[j],lw=1.3) for j in range(4)],['IO','LS','CP','C'],ncol=4,loc='upper center',bbox_to_anchor=(.5,-.30),frameon=False)
ax.add_artist(l1);ax.legend([Line2D([],[],color='black',ls=styles[j],lw=1.3) for j in range(4)],supports,ncol=4,loc='upper center',bbox_to_anchor=(.5,-.46),frameon=False,columnspacing=1)
save(fig,'B1_fragility_all_supports','All sixteen cached series from original Block 1 charts 1–4',details={'damage_states':4,'support_conditions':4,'curve_count':16,'new_fitting':False})

(P/'SEQ067_FIGURE_ASSET_MAP.json').write_text(json.dumps({'release':'LATEX_SEQ067','base':'LATEX_SEQ066','replacement_map':replacements,'figures':records},indent=2))
print('Rendered',len(records),'figure assets')
