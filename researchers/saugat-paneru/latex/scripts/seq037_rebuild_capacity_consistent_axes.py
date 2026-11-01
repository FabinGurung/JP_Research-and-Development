"""SEQ037: vector chart layout-only rebuild from the unchanged original seven workbooks.
No ETABS replay; stop each recorded series at the first global maximum base shear.
Physical typesetting: at full \linewidth (~6.0in) labels are >=11pt Times New Roman.
"""
import glob,re,os,json,math
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties,fontManager

BASE=Path(__file__).resolve().parents[1]
EXCEL=BASE/'qa/seq035_original_capacity_excels'
OUT=BASE/'figures/ch4/seq037'
OUT.mkdir(parents=True,exist_ok=True)
FONT=os.environ.get("SAUGAT_TNR_FONT_PATH", "/mnt/data/times.ttf")
if not os.path.exists(FONT): raise SystemExit('Exact TNR source required; do not use Tinos silently')
fontManager.addfont(FONT)
# Explicit font files stay private on build machine, never in source ZIP.
plt.rcParams.update({'font.family':'Times New Roman','font.size':12.3,'axes.labelsize':12.3,'xtick.labelsize':12.2,'ytick.labelsize':12.2,'legend.fontsize':11.8,'pdf.fonttype':42,'ps.fonttype':42,'axes.titlesize':12.3,'axes.unicode_minus':False,'figure.facecolor':'white'})
labels=[('C',0.25),('C',0.30),('C',0.35),('C',0.40),('D',0.35)]
colors=['#236a9f','#b4762c','#449451','#9d455b','#76509a']
markers=['o','s','^','D','v']
name_key={ 'Regular':'regular','L Shape':'l','L1 Shape':'l1','L2 Shape':'l2','T Shape':'t','U Shape':'u','NP':'non_parallel'}
source={}
allmax=[]
for f in EXCEL.glob('*.xlsx'):
    base=f.name.replace('Pushover Results ','')
    name=next((v for k,v in name_key.items() if base.startswith(k+' ') or base.startswith(k+'(')),None)
    if name is None: raise ValueError(f'Unknown source {f.name}')
    for direction in ('X','Y'):
        df=pd.read_excel(f,sheet_name=f'Pushover {direction}',header=None)
        sections={}; current=None; values=[]
        def flush():
            nonlocal_placeholder=None
            if current is None or not values:return
            vals=np.array(values, dtype=float)
            # Keep original order, truncate at first global peak.
            maxv=float(np.max(vals[:,1])); first=int(np.flatnonzero(np.isclose(vals[:,1],maxv))[0]); truncated=vals[:first+1,:]
            if truncated.shape[0]>0 and truncated[0,0]!=0 and truncated[0,1]!=0:raise ValueError('missing recorded origin')
            sections[current]=truncated
        for _,row in df.iterrows():
            a=str(row.iloc[0]); b=str(row.iloc[1])
            if re.search(r'Type\s+[CD]\b',a,re.I) and re.search(r'z\s*=\s*(?:0\.)?\d+',b,re.I):
                flush(); m=re.search(r'Type\s+([CD])\b',a,re.I); n=re.search(r'z\s*=\s*(\d+\.?\d*)',b,re.I)
                current=(m.group(1).upper(),round(float(n.group(1)),2));values=[]
            elif current is not None:
                try:
                    step=float(row.iloc[0]);x=float(row.iloc[1]);y=float(row.iloc[2]);
                    if math.isfinite(step) and math.isfinite(x) and math.isfinite(y) and x>=0 and y>=0:values.append((x,y))
                except (TypeError,ValueError):pass
        flush()
        source[(name,direction)]=sections
        for arr in sections.values():allmax.append((max(arr[:,0]),max(arr[:,1])))
if len(source)!=14:raise ValueError(f'Need 14 model-direction sets, got {len(source)}')
print('allmax x y',max(x for x,y in allmax),max(y for x,y in allmax))
# Consistent limits grounded in all 69 displayed series, not clipped by figure bounds.
xmax=math.ceil(max(x for x,y in allmax)/25)*25
ymax=math.ceil(max(y for x,y in allmax)/250)*250
results=[]; total=0
for (name, direction), curves in sorted(source.items()):
    fig,ax=plt.subplots(figsize=(6.13,4.12),dpi=160)
    for i,key in enumerate(labels):
        if key not in curves:continue
        a=curves[key];total+=1
        ax.plot(a[:,0],a[:,1],color=colors[i],marker=markers[i],markersize=3.4,lw=1.65,markevery=max(1,len(a)//9),label=f'Soil {key[0]}, Z = {key[1]:.2f}')
    ax.set(xlim=(0,xmax),ylim=(0,ymax),xlabel='Monitored roof displacement (mm)',ylabel='Base shear (kN)')
    ax.set_xticks(np.arange(0,xmax+.01,25 if xmax<=250 else 50))
    ax.set_yticks(np.arange(0,ymax+.01,250))
    ax.margins(x=0,y=0)
    ax.spines['top'].set_visible(False);ax.spines['right'].set_visible(False)
    ax.grid(True,alpha=.23,linewidth=.55)
    ax.tick_params(direction='out',length=3.3,pad=2.5)
    # Legend (indexes) at bottom-right of plot in whitespace; no internal title.
    ax.legend(loc='lower right',bbox_to_anchor=(.994,.016),frameon=True,facecolor='white',edgecolor='#bbbbbb',framealpha=.93,ncol=1,handlelength=1.5,handletextpad=.4,borderpad=.3,labelspacing=.28)
    fig.subplots_adjust(left=.155,right=.977,bottom=.167,top=.973)
    o=OUT/f'pushover_{name}_{direction.lower()}_data.pdf';fig.savefig(o,format='pdf',transparent=False)
    plt.close(fig)
    results.append({'file':str(o.relative_to(BASE)),'model':name,'direction':direction,'source_cases':len(curves),'points':sum(len(a) for a in curves.values()),'shared_limits':[xmax,ymax]})
assert total==70,(total,len(results))
summary={'existing_original_workbooks':7,'figures':14,'series':total,'shared_x_limits_mm':[0,xmax],'shared_y_limits_kN':[0,ymax],'font':'Times New Roman','nominal_figure_font_pt':12.3,'missing_case':None,'results':results}
(BASE/'SEQ037_FIGURE_QA.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='results'},indent=2))
