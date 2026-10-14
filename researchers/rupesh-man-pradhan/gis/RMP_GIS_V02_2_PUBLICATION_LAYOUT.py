import json, pandas as pd, numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Polygon as MplPolygon, Rectangle, FancyBboxPatch
from shapely.geometry import Polygon

BLUE='#2A6FDB'
ORANGE='#D97706'
DARK='#1F2937'
MUTED='#5F7286'
BG='#FCFDFE'
QUAL='#D8EAF3'
NONQUAL='#EFF2F5'
BOUND='#97AEC3'
ACCENT='#C53E3E'

base=Path('/mnt/data')
counts=pd.read_csv(base/'rmp_ward_summary_v0_2_0'/'RMP_WARD_COUNTS_SPATIAL_VS_RECORDED_v0.2.0.csv')
geo=json.load(open(base/'rmp_ward_summary_v0_2_1'/'RMP_WARD_DISPLAY_GEOMETRY_CACHE_v0.2.1.json'))
ward_geom={int(k):np.array([[float(x),730-float(y)] for x,y in poly],dtype=float) for k,poly in geo['wards'].items()}
counts=counts.set_index('ward')
qual=[w for w,r in counts.iterrows() if r.spatial_engineered>0 and r.spatial_non_engineered>0]
allx=np.hstack([pts[:,0] for pts in ward_geom.values()]); ally=np.hstack([pts[:,1] for pts in ward_geom.values()])
xmin,ymin,xmax,ymax=allx.min(),ally.min(),allx.max(),ally.max()
# same 5 km square frame from v0.2.1
five_km=5/(geo['source_frame_side_km']/730)
center=((xmin+xmax)/2,(ymin+ymax)/2)
half=max((xmax-xmin)/2,(ymax-ymin)/2)+five_km
frame=(center[0]-half,center[1]-half,center[0]+half,center[1]+half)
side_km=2*half*(geo['source_frame_side_km']/730)
unit=geo['source_frame_side_km']/730

def rep_point(pts):
    p=Polygon(pts)
    rp=p.representative_point()
    return rp.x,rp.y,p.area
centers={w:rep_point(pts) for w,pts in ward_geom.items()}

# callout positions manual
callouts={
    1:(-17,2),2:(-19,18),3:(-8,20),4:(-19,9),7:(-11,-10),8:(-8,14),9:(8,16),10:(17,7),12:(17,-5),15:(12,-12)
}

fig=plt.figure(figsize=(16.5,11.7),facecolor=BG) # A3 landscape-ish
fig.text(0.05,0.965,'RUPESH MAN PRADHAN THESIS  |  POKHARA METROPOLITAN CITY',fontsize=11.5,color='#0E7490',weight='bold')
fig.text(0.05,0.936,'Ward-wise distribution of engineered and non-engineered buildings',fontsize=22,color=DARK,weight='bold')
fig.text(0.05,0.912,'Static thesis publication layout  |  Qualifying wards only (both categories present)  |  5 km square map-frame margin',fontsize=10.5,color=MUTED)
fig.text(0.95,0.957,'FIGURE 4.x',ha='right',fontsize=11,color=DARK,weight='bold')
fig.text(0.95,0.936,'RESEARCH REVIEW CANDIDATE',ha='right',fontsize=9.5,color=MUTED)

# Main map
ax=fig.add_axes([0.05,0.17,0.63,0.70])
ax.set_xlim(frame[0],frame[2]); ax.set_ylim(frame[1],frame[3]); ax.set_aspect('equal'); ax.set_xticks([]); ax.set_yticks([])
ax.set_facecolor('#F4F8FB')
for s in ax.spines.values(): s.set_edgecolor('#C7D6E2'); s.set_linewidth(1.2)
# polygons
for w,pts in sorted(ward_geom.items()):
    q=w in qual
    patch=MplPolygon(pts,closed=True,facecolor=QUAL if q else NONQUAL,edgecolor='white',linewidth=1.2,zorder=2)
    ax.add_patch(patch)
    ax.plot(np.r_[pts[:,0],pts[0,0]],np.r_[pts[:,1],pts[0,1]],color=BOUND,lw=0.8,zorder=3)

# title chip on map
ax.text(0.02,0.98,'01  MAIN MAP  •  POKHARA WARDS',transform=ax.transAxes,va='top',ha='left',fontsize=11,weight='bold',color=DARK,
        bbox=dict(boxstyle='round,pad=0.45',fc='white',ec='none',alpha=0.94))
# north arrow
ax.annotate('N', xy=(0.95,0.93), xytext=(0.95,0.83), xycoords='axes fraction', textcoords='axes fraction',
            ha='center', va='center', fontsize=10, color=DARK, weight='bold',
            arrowprops=dict(arrowstyle='-|>', lw=1.5, color=DARK))
# scale bar 5 km
bar_len=5/unit
bx=frame[0]+(frame[2]-frame[0])*0.05; by=frame[1]+(frame[3]-frame[1])*0.05; h=(frame[3]-frame[1])*0.012
ax.add_patch(Rectangle((bx,by),bar_len/2,h,facecolor=DARK,edgecolor=DARK,zorder=8))
ax.add_patch(Rectangle((bx+bar_len/2,by),bar_len/2,h,facecolor='white',edgecolor=DARK,zorder=8))
ax.text(bx,by+h*2.4,'0',fontsize=8,color=DARK,ha='center',weight='bold')
ax.text(bx+bar_len,by+h*2.4,'5 km',fontsize=8,color=DARK,ha='center',weight='bold')

# helper for labels
def draw_label(ax, x, y, ward, eng, non, external=False):
    width=8.5; height=6.2
    # alignment center around x,y
    left=x-width/2; bottom=y-height/2
    box=FancyBboxPatch((left,bottom),width,height,boxstyle='round,pad=0.18,rounding_size=0.7',
                       facecolor='white',edgecolor='#D5DEE8',linewidth=0.8,zorder=10,alpha=0.96)
    ax.add_patch(box)
    ax.text(x,bottom+height-1.25,f'W{ward:02d}',ha='center',va='center',fontsize=8.7,weight='bold',color=DARK,zorder=11,
            path_effects=[pe.withStroke(linewidth=1.8,foreground='white')])
    ax.text(x,bottom+height-2.9,f'E {eng:02d}',ha='center',va='center',fontsize=8.1,weight='bold',color=BLUE,zorder=11,
            path_effects=[pe.withStroke(linewidth=1.5,foreground='white')])
    ax.text(x,bottom+height-4.55,f'NE {non:02d}',ha='center',va='center',fontsize=8.1,weight='bold',color=ORANGE,zorder=11,
            path_effects=[pe.withStroke(linewidth=1.5,foreground='white')])

for w in qual:
    eng=int(counts.loc[w,'spatial_engineered']); non=int(counts.loc[w,'spatial_non_engineered'])
    rx,ry,area=centers[w]
    if w in callouts:
        dx,dy=callouts[w]
        lx,ly=rx+dx,ry+dy
        ax.plot([rx,lx],[ry,ly],color='#6B7F92',lw=0.9,zorder=9)
        ax.scatter([rx],[ry],s=12,color='#6B7F92',zorder=9)
        draw_label(ax,lx,ly,w,eng,non,external=True)
    else:
        draw_label(ax,rx,ry,w,eng,non)

# Locator inset: Nepal schematic + extent indicator
inset=fig.add_axes([0.73,0.66,0.22,0.20])
inset.set_xticks([]); inset.set_yticks([]); inset.set_facecolor('white')
for s in inset.spines.values(): s.set_edgecolor('#D7E1EA'); s.set_linewidth(1.0)
inset.text(0.04,0.97,'02  NATIONAL LOCATOR',transform=inset.transAxes,ha='left',va='top',fontsize=10.5,weight='bold',color=DARK)
# rough Nepal polygon in lon/lat-like coordinates (schematic locator only)
nepal=np.array([
    [80.0,28.1],[80.3,29.0],[80.1,29.6],[80.2,30.1],[80.7,30.3],[81.3,30.4],[81.9,30.5],[82.6,30.4],[83.2,30.2],[84.0,30.1],
    [84.7,30.3],[85.3,30.5],[86.0,30.2],[86.8,30.1],[87.5,29.8],[88.0,29.5],[88.2,28.9],[88.0,28.0],[87.4,27.6],[86.6,27.4],
    [85.6,27.6],[84.8,27.7],[84.0,27.8],[83.2,27.7],[82.4,27.8],[81.6,27.7],[80.9,27.8],[80.3,27.9],[80.0,28.1]
])
inset.fill(nepal[:,0],nepal[:,1],color='#EEF2F6',ec='#92A7BB',lw=1.0)
inset.set_xlim(79.7,88.5); inset.set_ylim(27.2,30.8)
# indicator around Pokhara approx 83.99,28.21
pokx,poky=83.99,28.21
inset.add_patch(Rectangle((pokx-0.18,poky-0.18),0.36,0.36,fill=False,ec=ACCENT,lw=1.6))
inset.scatter([pokx],[poky],s=18,color=ACCENT,zorder=4)
inset.text(pokx+0.23,poky-0.03,'Pokhara',fontsize=8.2,color=ACCENT,weight='bold')
inset.text(0.04,0.04,'Schematic Nepal inset for locator context',transform=inset.transAxes,fontsize=7.5,color=MUTED)

# Legend and metadata panel
leg=fig.add_axes([0.71,0.33,0.25,0.28]); leg.axis('off')
leg.add_patch(FancyBboxPatch((0,0),1,1,boxstyle='round,pad=0.02,rounding_size=0.03',fc='white',ec='#D7E1EA',lw=1.0))
leg.text(0.05,0.94,'03  LEGEND / MAP ELEMENTS',fontsize=10.5,weight='bold',color=DARK,va='top')
# symbology patches
leg.add_patch(Rectangle((0.06,0.78),0.06,0.05,fc=QUAL,ec=BOUND,lw=0.8)); leg.text(0.15,0.805,'Qualifying ward (engineered > 0 and non-engineered > 0)',fontsize=8.5,color=DARK,va='center')
leg.add_patch(Rectangle((0.06,0.70),0.06,0.05,fc=NONQUAL,ec=BOUND,lw=0.8)); leg.text(0.15,0.725,'Other ward',fontsize=8.5,color=DARK,va='center')
leg.text(0.07,0.60,'E 08',fontsize=9.2,color=BLUE,weight='bold'); leg.text(0.18,0.60,'Engineered building count',fontsize=8.5,color=DARK,va='center')
leg.text(0.07,0.52,'NE 05',fontsize=9.2,color=ORANGE,weight='bold'); leg.text(0.18,0.52,'Non-engineered building count',fontsize=8.5,color=DARK,va='center')
leg.plot([0.06,0.12],[0.43,0.47],color='#6B7F92',lw=1.0); leg.text(0.18,0.45,'Leader line / callout for congested labels',fontsize=8.5,color=DARK,va='center')
leg.add_patch(Rectangle((0.06,0.34),0.06,0.05,fill=False,ec=ACCENT,lw=1.3)); leg.text(0.18,0.365,'Pokhara locator extent on Nepal inset',fontsize=8.5,color=DARK,va='center')
leg.text(0.05,0.23,'Projection:',fontsize=8.6,color=MUTED,weight='bold')
leg.text(0.28,0.23,'WGS 84 / UTM Zone 45N (EPSG:32645)',fontsize=8.6,color=DARK)
leg.text(0.05,0.15,'Map frame:',fontsize=8.6,color=MUTED,weight='bold')
leg.text(0.28,0.15,f'Fixed square extent; ~{side_km:.1f} km per side',fontsize=8.6,color=DARK)
leg.text(0.05,0.07,'Buffer rule:',fontsize=8.6,color=MUTED,weight='bold')
leg.text(0.28,0.07,'Pokhara boundary + 5 km minimum offset',fontsize=8.6,color=DARK)

# Notes panel
notes=fig.add_axes([0.71,0.17,0.25,0.12]); notes.axis('off')
notes.add_patch(FancyBboxPatch((0,0),1,1,boxstyle='round,pad=0.02,rounding_size=0.03',fc='#F4F8FB',ec='#D7E1EA',lw=1.0))
notes.text(0.05,0.88,'04  SOURCES / QA NOTE',fontsize=10.3,weight='bold',color=DARK,va='top')
notes.text(0.05,0.63,'Ward boundary display geometry: generalized cartographic cache derived',fontsize=8.15,color=DARK)
notes.text(0.05,0.48,'from the preserved V02.0 output, using Kathmandu Living Labs / OSM',fontsize=8.15,color=DARK)
notes.text(0.05,0.33,'historical 33-ward polygons. Counts shown here are spatial ward counts.',fontsize=8.15,color=DARK)
notes.text(0.05,0.18,'Known QA: 50 source-vs-spatial ward conflicts; 1 user-approved',fontsize=8.15,color='#9A4F2F')
notes.text(0.05,0.05,'Ward 33 location exception. No individual coordinates displayed.',fontsize=8.15,color='#9A4F2F')

# Footer source credits
fig.text(0.05,0.08,'Source credits: Rupesh Man Pradhan field dataset (266 records) • KLL/OSM historical ward layer • Author-generated static cartographic layout',fontsize=8.5,color=MUTED)
fig.text(0.05,0.055,'This figure is a thesis publication-style review layout. It excludes interactive elements and individual building point coordinates.',fontsize=8.5,color=MUTED)

outdir=base/'rmp_ward_summary_v0_2_2'
outdir.mkdir(exist_ok=True)
out=outdir/'RMP_POKHARA_WARD_SUMMARY_5KM_PUBLICATION_LAYOUT_v0.2.2.png'
fig.savefig(out,dpi=300,facecolor=BG)
print(out)
