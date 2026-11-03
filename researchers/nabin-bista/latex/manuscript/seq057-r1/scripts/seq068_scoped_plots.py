"""Source-preserving targeted SEQ068 plots. No statistical fitting or ETABS execution."""
from pathlib import Path
import json,zipfile,io,xml.etree.ElementTree as ET
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.lines import Line2D
from scipy.special import ndtr
import fitz
P=Path(__file__).resolve().parents[1]
O=P/'figures'/'seq068';O.mkdir(exist_ok=True)
font_files=[Path('/home/oai/.local/share/fonts')/n for n in ['times.ttf','timesbd.ttf','timesi.ttf','timesbi.ttf']]
for p in font_files:fm.fontManager.addfont(str(p))
assert fm.FontProperties(fname=str(font_files[0])).get_name()=='Times New Roman'
plt.rcParams.update({'font.family':'Times New Roman','font.size':12,'axes.labelsize':12,
 'xtick.labelsize':12,'ytick.labelsize':12,'legend.fontsize':12,
 'pdf.fonttype':42,'ps.fonttype':42,'axes.unicode_minus':False,
 'axes.spines.top':False,'axes.spines.right':False})
NS={'c':'http://schemas.openxmlformats.org/drawingml/2006/chart'}
def series(path,part):
    with zipfile.ZipFile(path) as z:root=ET.fromstring(z.read(part))
    out=[]
    for ser in root.findall('.//c:ser',NS):
        def points(tag):
            el=ser.find('c:'+tag,NS)
            if el is None:return {}
            return {int(n.attrib['idx']):float(n.find('c:v',NS).text) for n in el.findall('.//c:pt',NS) if n.find('c:v',NS)is not None}
        x=points('xVal') or points('cat'); y=points('yVal') or points('val')
        keys=sorted(x.keys() & y.keys());out.append(([x[k] for k in keys],[y[k] for k in keys]))
    return out
params={(x['block'],x['support']):x['states'] for x in json.loads((P/'SEQ066_SOURCE_REVIEW_AUDIT.json').read_text())['fragility_reconstruction']}
lineage=json.loads((P/'seq051_assets/SOURCE_CHART_LINEAGE.json').read_text())['records']
lines=[]
labels=['IO','LS','CP','C']; supports=['Soft','Medium','Hard','Fixed']
styles=[':', '-.', '--','-']
colors=['#0072b2','#e69f00','#009e73','#cc79a7']
sourcezip=P/'source_originals_20261029/RESULT PLOT nabin bista .zip'
for block in range(2,7):
    fig,ax=plt.subplots(figsize=(6.10,3.30))
    fig.subplots_adjust(left=.16,right=.96,top=.95,bottom=.39)
    cached_maxdiff=0.0;counts=[]
    for idx,support in enumerate(supports,1):
        row=next(r for r in lineage if r.get('block_folder')==block and r.get('latex_path') and r.get('chart_kind','').lower()=='fragility' and r.get('chart_file','').endswith(f'chart{idx}.xml'))
        with zipfile.ZipFile(sourcezip) as z:
            raw=z.read(row['source_workbook'])
        original=series(io.BytesIO(raw),row['chart_file'])
        assert len(original)==4,(block,idx,len(original))
        for j,(x0,y0) in enumerate(original):
            par=params[(block,support.lower())][j];theta=par['theta_workbook_g'];beta=par['beta_total']
            x0=np.array(x0,float);y0=np.array(y0,float)
            predicted=np.zeros_like(x0);mask=x0>0
            predicted[mask]=ndtr(np.log(x0[mask]/theta)/beta)
            err=float(np.max(np.abs(predicted-y0)));cached_maxdiff=max(cached_maxdiff,err)
            assert err<1e-12,(block,idx,j,err)
            x=np.linspace(0,1,1001);y=np.zeros_like(x);m=x>0;y[m]=ndtr(np.log(x[m]/theta)/beta)
            ax.plot(x,y,color=colors[j],linestyle=styles[idx-1],linewidth=1.25)
            counts.append(len(x0))
    ax.set_xlim(0,1);ax.set_ylim(0,1);ax.set_xticks(np.arange(0,1.01,.2));ax.set_yticks(np.arange(0,1.01,.2));ax.grid(color='#e4e4e4',linewidth=.5)
    ax.set_xlabel('Peak ground acceleration (PGA)')
    ax.set_ylabel('Damage-state\nexceedance probability')
    legend1=ax.legend([Line2D([],[],color=colors[j],lw=1.4) for j in range(4)],labels,ncol=4,loc='upper center',bbox_to_anchor=(.5,-.27),frameon=False)
    ax.add_artist(legend1)
    ax.legend([Line2D([],[],color='black',linestyle=styles[j],lw=1.4) for j in range(4)],supports,ncol=4,loc='upper center',bbox_to_anchor=(.5,-.44),frameon=False)
    name=f'B{block}_fragility_all_supports'
    for ext in ['pdf','png']:
        fig.savefig(O/(name+'.'+ext),dpi=300)
    plt.close(fig)
    lines.append({'name':name,'block':block,'support_conditions':supports,'damage_states':labels,'curves':16,'source':'original 67-workbook chart caches + SEQ066 admitted theta/beta values','max_cached_probability_difference':cached_maxdiff,'font':'Times New Roman','font_size_pt':12})
# Older SEQ049 prototype pushover data, extracted from the original included XLSX, NOT six-block predictions.
series2=json.loads(Path('/mnt/data/seq049_pushover_verified_series.json').read_text())
fig,axes=plt.subplots(4,1,figsize=(6.10,7.30),sharex=True)
for ax,(support,sdata) in zip(axes,series2.items()):
    for direction,color in [('push-x',colors[0]),('push-y',colors[1])]:
        xy=np.array(sdata[direction],float)
        ax.plot(xy[:,0],xy[:,1],marker='.',markersize=2,linewidth=1.2,label='Push X' if direction=='push-x' else 'Push Y',color=color)
    ax.set_xlim(0,.90);ax.set_ylim(0,57000);ax.set_yticks([0,20000,40000]);ax.grid(True,color='#e4e4e4',linewidth=.5)
    ax.set_ylabel('Base shear (kN)');ax.annotate(support+' support',(.04,.88),xycoords='axes fraction',fontsize=12)
    ax.legend(loc='lower right',frameon=False,ncol=2)
axes[-1].set_xlabel('Roof displacement (m)')
fig.subplots_adjust(left=.17,right=.97,top=.97,bottom=.09,hspace=.22)
for ext in ['pdf','png']:fig.savefig(O/('SEQ049_prototype_pushover_XY_recovered.'+ext),dpi=300)
plt.close(fig)
lines.append({'name':'SEQ049_prototype_pushover_XY_recovered','source':'source_inputs_seq30/Pushover Capacity Curve (chapter4.8).xlsx','status':'original legacy prototype, separate from current six-block nonlinear analyses','curves':8,'font':'Times New Roman','font_size_pt':12})
for r in lines:
 d=fitz.open(O/(r['name']+'.pdf'))
 f=[(span['font'],round(span['size'],3)) for span in d[0].get_text('dict')['blocks'] if 'lines' in span for line in span['lines'] for span in line['spans']]
 # x0=0 text etc; no font fallback
 assert f and all('TimesNewRoman' in n.replace(' ','') and size>=11 for n,size in f),(r['name'],f[:20])
 r['embedded_font_min_point_size']=min(s for _,s in f)
(P/'SEQ068_PLOTS_LINEAGE.json').write_text(json.dumps(lines,indent=2))
print(json.dumps(lines,indent=2))
