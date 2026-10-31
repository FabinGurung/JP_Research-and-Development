"""Saugat-only illustration/plot improvements requested in own-comments DOCX.
All quantitative points come from the preserved CP112 source generator or FF CSVs.
Requires privately provided Times New Roman fonts in build environment; never package fonts.
"""
from pathlib import Path
import ast, csv, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import Rectangle, Polygon, FancyBboxPatch
ROOT=Path(__file__).resolve().parents[1]
for face in ('times.ttf','timesbd.ttf','timesi.ttf','timesbi.ttf'):
    q=Path('/mnt/data')/face
    if q.exists(): fm.fontManager.addfont(str(q))
plt.rcParams.update({'font.family':'Times New Roman','font.size':11,'axes.titlesize':11,'axes.labelsize':11,'xtick.labelsize':10,'ytick.labelsize':10,'legend.fontsize':10,'savefig.bbox':'tight','pdf.fonttype':42,'ps.fonttype':42})
# 6: repeat existing documented mechanism, but remove redundant top title and eliminate collisions.
out=ROOT/'figures/ch2/seismic_vulnerability_rc_building.png'
fig,ax=plt.subplots(figsize=(11.1,5.0)); ax.set_xlim(0,15.5);ax.set_ylim(0,6.6);ax.axis('off')
# RC frame at left
for x in [0.7,1.65,2.6,3.55]: ax.plot([x,x],[1.2,5.6],c='#292929',lw=1.4)
for y in [1.2,2.65,4.1,5.55]:ax.plot([.7,3.55],[y,y],c='#292929',lw=1.4)
ax.text(2.13,5.95,'Three-storey RC frame',ha='center',fontsize=11,weight='bold')
for y,l in [(2.65,'F'),(4.1,'F'),(5.55,'F')]:
 ax.annotate('',xy=(4.0,y),xytext=(3.55,y),arrowprops={'arrowstyle':'->','lw':1.4});ax.text(4.05,y,l,va='center')
ax.text(2.1,.56,'Lateral earthquake demand',ha='center')
# L plan in middle, one clear label outside the plan.
poly=[(5.15,1.25),(9.65,1.25),(9.65,3.25),(8.3,3.25),(8.3,5.35),(5.15,5.35)]
ax.add_patch(Polygon(poly,closed=True,fill=False,lw=1.8,ec='#333'))
ax.plot([8.3],[3.25],marker='o',ms=6,c='#333')
ax.annotate('Re-entrant corner',xy=(8.3,3.25),xytext=(8.65,4.65),fontsize=10,arrowprops={'arrowstyle':'->','lw':1})
ax.text(7.35,5.95,'Illustrative plan irregularity',ha='center',fontsize=11,weight='bold')
ax.text(7.25,.56,'Plan geometry / stiffness distribution',ha='center')
# Three separate outcome boxes; avoid previous overlaps.
for i,(t,detail) in enumerate([('Configuration','Mass–stiffness eccentricity'),('Construction','Material and detailing quality'),('Seismic response','Drift and torsional concentration')]):
 y=5.15-i*1.67; ax.add_patch(FancyBboxPatch((10.4,y-0.65),4.55,1.3,boxstyle='round,pad=0.12',lw=1,fill=False))
 ax.text(12.68,y+.24,t,ha='center',weight='bold');ax.text(12.68,y-.26,detail,ha='center',fontsize=10)
ax.annotate('',xy=(10.32,3.4),xytext=(9.7,3.4),arrowprops={'arrowstyle':'->','lw':1.2})
fig.savefig(out,dpi=320);plt.close(fig)
# 7: five individual conceptual theoretical illustrations, no numerical data.
fdir=ROOT/'figures/ch2/comment31';fdir.mkdir(parents=True,exist_ok=True)
for no,kind in enumerate(['equivalent_static','response_spectrum','nonlinear_pushover','performance_point','plastic_hinge'],start=1):
 fig,ax=plt.subplots(figsize=(6.9,3.5));ax.set_xlim(0,10);ax.set_ylim(0,5.2);ax.axis('off')
 if kind=='equivalent_static':
  for x in [2,4]: ax.plot([x,x],[1,4.2],lw=1.7,c='#333')
  for y in [1,2,3,4.2]: ax.plot([1.7,4.3],[y,y],lw=1.7,c='#333')
  for y,dx in [(2,1.2),(3,1.65),(4.2,2.0)]:ax.annotate('',xy=(4+dx,y),xytext=(4,y),arrowprops={'arrowstyle':'->','lw':1.5})
  ax.text(4.5,.3,'Idealized heightwise lateral-force distribution',ha='center')
 elif kind=='response_spectrum':
  ax.annotate('',xy=(9.1,.8),xytext=(1,.8),arrowprops={'arrowstyle':'->','lw':1.4})
  ax.annotate('',xy=(1,4.65),xytext=(1,.8),arrowprops={'arrowstyle':'->','lw':1.4})
  ax.plot([1.15,1.5,2.4,3.6,4.6,6.0,7.9,8.8],[1.1,2.9,4,4,3.4,2.6,1.65,1.3],lw=2,c='#333')
  ax.set_title('Illustrative spectral acceleration versus period',fontsize=11)
  ax.text(9.1,.45,'Period',ha='right');ax.text(.4,4.45,'$S_a$',ha='center')
 elif kind=='nonlinear_pushover':
  ax.annotate('',xy=(9.1,.8),xytext=(1,.8),arrowprops={'arrowstyle':'->','lw':1.4})
  ax.annotate('',xy=(1,4.65),xytext=(1,.8),arrowprops={'arrowstyle':'->','lw':1.4})
  ax.plot([1.1,2.7,4.4,6.1,7.5,8.8],[.9,2.1,3.2,4.0,3.72,3.3],c='#333',lw=2)
  ax.text(8.9,.45,'Roof displacement',ha='right');ax.text(.65,4.5,'Base shear',rotation=90,ha='center')
 elif kind=='performance_point':
  ax.annotate('',xy=(9.1,.8),xytext=(1,.8),arrowprops={'arrowstyle':'->','lw':1.4});ax.annotate('',xy=(1,4.65),xytext=(1,.8),arrowprops={'arrowstyle':'->','lw':1.4})
  ax.plot([1.2,3.2,5.0,7.1,8.8],[1.0,2.8,3.8,3.9,3.5],lw=2,c='#333',label='Illustrative capacity')
  ax.plot([1.2,3.3,5.3,7.5,8.8],[4.4,3.95,3.15,2.2,1.65],ls='--',lw=1.7,c='#555',label='Illustrative demand')
  ax.scatter([5.15],[3.38],c='black',marker='s');ax.text(5.3,3.55,'Demand–capacity intersection',fontsize=10)
  ax.legend(loc='lower left',frameon=False)
 else:
  for x in [2.2,4.6]:ax.plot([x,x],[1,4.2],lw=1.8,c='#333')
  for y in [1,2.1,3.2,4.2]: ax.plot([2,4.8],[y,y],lw=1.8,c='#333')
  for x,y in [(2.2,2.1),(4.6,3.2),(2.2,4.2)]:ax.plot(x,y,marker='o',ms=9,mfc='white',mec='#333',mew=1.6)
  ax.text(6.3,3.6,'Example hinge locations',fontsize=11);ax.text(6.3,2.6,'Possible hinge regions',fontsize=10)
 fig.savefig(fdir/(kind+'.pdf'));plt.close(fig)
# 11/13: governing genuine drift profiles embedded in prior admitted source generator, plus display-only zero base anchor.
py=ast.parse((ROOT/'scripts/generate_cp112_figures.py').read_text())
vals={}
for node in py.body:
 if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id in ('drift_profiles','models','gii','pp_shear','pp_disp'):
  vals[node.targets[0].id]=ast.literal_eval(node.value)
assert len(vals['drift_profiles'])==7
for model,(x,y) in vals['drift_profiles'].items():
 assert len(x)==4 and len(y)==4
outdir=ROOT/'figures/ch4/comment31';outdir.mkdir(parents=True,exist_ok=True)
fig,ax=plt.subplots(figsize=(8.7,5.1)); style=['o','s','^','D','v','P','X']
for i,(model,(x,y)) in enumerate(vals['drift_profiles'].items()):
 ax.plot([0]+list(x),[0,3,6,9,12],marker=style[i],lw=1.5,ms=5,label=model)
ax.set_xlabel('ULS inter-storey drift ratio, X direction');ax.set_ylabel('Elevation (m)')
ax.set_xlim(0,.006);ax.set_ylim(0,12.8);ax.set_yticks([0,3,6,9,12],['Base','Story 1','Story 2','Story 3','Stair cover'])
ax.grid(True,ls=':',alpha=.4);ax.legend(loc='upper right',fontsize=10,ncol=2,frameon=False)
fig.text(.08,.03,'Base at (0, 0) is a plotting reference, not a measured base-storey drift.',fontsize=9)
fig.savefig(outdir/'uls_drift_profile_X_source_backed.pdf');plt.close(fig)
# 12: chart plots authentic Storey force values, with complete box/upper frame line, no invented return-to-zero.
records=list(csv.DictReader((ROOT/'figures/ch4/final_final_generated/ff_storey_shear_C040_data.csv').open()))
fig,ax=plt.subplots(figsize=(8.3,5.0))
for i,model in enumerate(vals['models']):
 rr=[r for r in records if r['model']==model]
 assert len(rr)==5 and rr[0]['story']=='Base'
 xs=[float(r['abs_x_shear_kn']) for r in rr]; ys=[float(r['elevation_m']) for r in rr]
 # Do not linearly interpolate story shear; show recorded levels only.
 ax.plot(xs[1:],ys[1:],marker=style[i],lw=1.4,label=model)
ax.set_xlim(left=0);ax.set_ylim(0,12.7);ax.set_yticks([0,3,6,9,12],['Base','Story 1','Story 2','Story 3','Stair cover'])
ax.set_xlabel('Absolute EQx storey shear (kN)');ax.set_ylabel('Elevation (m)')
for spine in ax.spines.values():spine.set_visible(True)
ax.grid(True,linestyle=':',alpha=.3);ax.legend(loc='upper right',frameon=False,ncol=2,fontsize=9.4)
fig.savefig(outdir/'story_shear_levels_source_backed.pdf');plt.close(fig)
# 18: different markers, colors and line formats; categorical GII repeated values remain separate points.
model=vals['models'];gii=vals['gii']
for key,title,unit,name in [('pp_shear','Performance-point base shear','kN','gii_pp_base_shear_distinct_markers.pdf'),('pp_disp','Performance-point roof displacement','mm','gii_pp_roof_displacement_distinct_markers.pdf')]:
 fig,ax=plt.subplots(figsize=(8.1,4.6))
 colors=['#222222','#23548b','#9a4a20','#6f5886','#2f7b57','#b13d52','#8a6b26']
 for i,(m,g,y) in enumerate(zip(model,gii,vals[key])):
  ax.scatter([g],[y],s=82,marker=style[i],c=[colors[i]],linewidths=1.1,edgecolors='black',label=m)
 ax.set_xlabel('Geometric Irregularity Index (%)');ax.set_ylabel(f'{title} ({unit})');ax.grid(True,ls=':',alpha=.35)
 ax.legend(loc='upper center',bbox_to_anchor=(.5,-.20),ncol=4,frameon=False,fontsize=10)
 fig.savefig(outdir/name);plt.close(fig)
print('created',len(list(fdir.glob('*.pdf')))+len(list(outdir.glob('*.pdf')))+1,'images')
