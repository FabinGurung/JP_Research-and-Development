from pathlib import Path
import fitz, csv, json, hashlib, re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
root=Path(__file__).resolve().parents[1]
source_pdf='/mnt/data/nbc205_2012__draft_final_ready_to_use_guideline.pdf'
# Keep font binaries OUTSIDE thesis ZIP/source tree.
import os
fontpath=os.environ.get('PU_TNR_FONT_PATH') or font_manager.findfont(font_manager.FontProperties(family='Times New Roman'))
font_manager.fontManager.addfont(fontpath)
fontname=font_manager.FontProperties(fname=fontpath).get_name()
plt.rcParams.update({'font.family':fontname,'font.size':13,'axes.labelsize':13.5,'xtick.labelsize':12,'ytick.labelsize':11,'pdf.fonttype':42,'ps.fonttype':42,'axes.titlesize':11})
models=['Regular','L','L1','L2','T','U']
cases=[('C',0.25,[.00894,.00940,.00837,.00968,.00819,.00951]),('C',0.30,[.00968,.01203,.01003,.01163,.00945,.01100]),('C',0.35,[.01409,.01558,.01123,.01175,.01192,.01438]),('C',0.40,[.01564,.01513,.01100,.01558,.01318,.01593]),('D',0.35,[.01089,.01261,.00917,.01054,.00991,.01152])]
plotdir=root/'figures/ch4/seq034_torsion'
plotdir.mkdir(parents=True,exist_ok=True)
markers=['o','s','^','D','v','P']
styles=['-','--','-.',':','--','-']
rows=[]
for idx,(soil,Z,vals) in enumerate(cases,5):
    fig,ax=plt.subplots(figsize=(3.65,2.6),dpi=200)
    xi=list(range(len(models)))
    ax.plot(xi,vals,color='#364966',linewidth=1.5,zorder=1)
    for j,(model,value) in enumerate(zip(models,vals)):
        ax.scatter([j],[value],marker=markers[j],s=70,color=['#25446c','#c1554b','#5f7c45','#845d8f','#b07835','#61788c'][j],zorder=4,label=model,edgecolor='black',linewidth=.45)
        rows.append((idx,soil,Z,model,value))
    ax.set_xticks(xi,models)
    ax.set_xlabel('Building model')
    ax.set_ylabel('Rotation (degrees)')
    ax.set_ylim(0,max(vals)*1.24)
    ax.grid(True,axis='y',linewidth=.55,alpha=.42)
    for spine in ['top','right']:ax.spines[spine].set_visible(False)
    fig.tight_layout(pad=1.2)
    fig.savefig(plotdir/f'fig_4_{idx}_max_rotation.pdf',bbox_inches='tight')
    fig.savefig(plotdir/f'fig_4_{idx}_max_rotation.png',bbox_inches='tight',dpi=180)
    plt.close(fig)
with (plotdir/'source_label_transcriptions.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['chapter_figure','soil_type','zone_factor','building_model','original_printed_max_rotation_deg']);w.writerows(rows)
(plotdir/'SOURCE_PROVENANCE.md').write_text('SEQ034. The 30 numerical values were transcribed from the printed five-decimal degree labels in preserved SEQ033 originals figures/ch4/authority_exact/fig_4_10 through fig_4_14_CP110_exact_clip.pdf, retaining model order Regular, L, L1, L2, T, U. These are MAXIMUM TORSIONAL ROTATION ANGLES in degrees, NOT code torsional-irregularity ratios, and NOT six-storey per-storey records. Lines connect categorical models for presentation only, not model interpolation. Original source PDF figures remain unchanged and included in ZIP. No ETABS values or scientific analysis were added.\n',encoding='utf8')