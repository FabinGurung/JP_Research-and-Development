#!/usr/bin/env python3
"""Rupesh GIS V02.3 thesis atlas: distinct ward color key; source-only static PNG.

Inputs are GOVERNED aggregate ward counts from V02.0 and cartographic DISPLAY
geometry cache V02.1. No private individual coordinates in this script.
Boundary source is Kathmandu Living Labs / OSM historical 33 wards, not certified.
Known 50 source/spatial ward conflicts & one manual Ward 33 include remain open.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPolygon, Rectangle, FancyBboxPatch, FancyArrowPatch
from matplotlib.colors import to_hex
import matplotlib.patheffects as pe
from shapely.geometry import Polygon as SPolygon
from matplotlib import colormaps

BG='#FFFFFF'; DARK='#17283B'; MUTED='#5A6D7E'; BLUE='#185EA8'; ORANGE='#D35D22'; LINE='#8095AA'
NONQUAL='#E9EDF1'; PANEL='#F5F8FB'

# Public-domain country outline from world.geo.json (Nepal); geographic locator
# geometry only, never used to compute ward counts or municipal extent.
NEPAL=[
[88.120441,27.876542],[88.043133,27.445819],[88.174804,26.810405],[88.060238,26.414615],
[87.227472,26.397898],[86.024393,26.630985],[85.251779,26.726198],[84.675018,27.234901],
[83.304249,27.364506],[81.999987,27.925479],[81.057203,28.416095],[80.088425,28.79447],
[80.476721,29.729865],[81.111256,30.183481],[81.525804,30.422717],[82.327513,30.115268],
[83.337115,29.463732],[83.898993,29.320226],[84.23458,28.839894],[85.011638,28.642774],
[85.823320,28.203576],[86.954517,27.974262],[88.120441,27.876542]
]

def load_counts(path):
    with Path(path).open(newline='',encoding='utf-8-sig') as f:
        rows={int(r['ward']):r for r in csv.DictReader(f)}
    assert sorted(rows)==list(range(1,34))
    for v in rows.values():
        for k in ['spatial_engineered','spatial_non_engineered','source_spatial_disagreements','manual_location_exception']:
            v[k]=int(v[k])
    assert sum(r['spatial_engineered'] for r in rows.values())==150
    assert sum(r['spatial_non_engineered'] for r in rows.values())==116
    assert sum(r['source_spatial_disagreements'] for r in rows.values())==50
    assert sum(r['manual_location_exception'] for r in rows.values())==1
    return rows

def load_shapes(path):
    m=json.loads(Path(path).read_text())
    assert m['geometry_kind']=='cartographic_display_only_from_v0.2.0_svg'
    assert len(m['wards'])==33
    return {int(w):np.array([(float(x),730-float(y)) for x,y in coords]) for w,coords in m['wards'].items()},m

def swatch_color(idx):
    # 27 reproducible qualitative colors; distinct hues + separated brightness.
    # Numbered labels in the legend disambiguate nearby color shades in print.
    h=(idx*0.61803398875+0.083)%1
    # hsv controlled light/pastel for dark ward numbers; all nominally distinct.
    import colorsys
    s=(0.34,0.45,0.37)[idx%3]
    v=(0.92,0.83,0.94)[(idx//3)%3]
    return to_hex(colorsys.hsv_to_rgb(h,s,v))

def compute_frame(shapes,m):
    pts=np.concatenate(list(shapes.values()))
    x0,y0=np.min(pts,axis=0); x1,y1=np.max(pts,axis=0)
    units_km=m['source_frame_side_km']/m['source_frame_px']
    gap=5/units_km
    cx,cy=(x0+x1)/2,(y0+y1)/2
    half=max((x1-x0)/2,(y1-y0)/2)+gap
    extent=[cx-half,cx+half,cy-half,cy+half]
    return extent,2*half*units_km,units_km

def anchor(shapes):
    return {w:SPolygon(v).representative_point().coords[0] for w,v in shapes.items()}

def output_hash(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()

def draw(shapes,counts,m,out):
    qualified=sorted(w for w,r in counts.items() if r['spatial_engineered']>0 and r['spatial_non_engineered']>0)
    assert len(qualified)==27
    colors={w:swatch_color(i) for i,w in enumerate(qualified)}
    extent,side_km,km_per_pixel=compute_frame(shapes,m)
    plt.rcParams.update({'font.family':'DejaVu Sans','savefig.facecolor':'white','figure.facecolor':'white'})
    fig=plt.figure(figsize=(16.54,11.69),facecolor='white')
    fig.text(.048,.965,'RUPESH MAN PRADHAN  /  GIS THESIS FIGURES',size=10.0,color='#127B88',weight='bold')
    fig.text(.048,.937,'Distribution of building survey categories across Pokhara wards',size=18.4,color=DARK,weight='bold')
    fig.text(.048,.914,'Ward color-keyed publication plate   |   Only wards represented in both categories   |   5 km offset square extent',size=9.6,color=MUTED)
    fig.text(.964,.955,'PLATE  V02.3',size=9.8,color=DARK,weight='bold',ha='right')
    # Map area deliberately square in PHYSICAL dimensions: aspect=equal supported.
    ax=fig.add_axes([.045,.145,.638,.730])
    ax.set_xlim(extent[0],extent[1]);ax.set_ylim(extent[2],extent[3]);ax.set_aspect('equal')
    ax.set_facecolor('#F7F9FB');ax.set_xticks([]);ax.set_yticks([])
    for spine in ax.spines.values():spine.set_color('#B6C7D5');spine.set_linewidth(1)
    # Ward polys (non-qual = neutral)
    for w,p in sorted(shapes.items()):
        face=colors[w] if w in colors else NONQUAL
        ax.add_patch(MPolygon(p,closed=True,facecolor=face,edgecolor='#FDFEFE',linewidth=1.6,zorder=2))
        ax.plot(np.r_[p[:,0],p[0,0]],np.r_[p[:,1],p[0,1]],color='#8499AB',lw=.65,zorder=3)
    ax.text(.027,.975,'POKHARA  •  METROPOLITAN WARDS',transform=ax.transAxes,ha='left',va='top',size=10.0,weight='bold',color=DARK,
            bbox=dict(fc='white',ec='none',alpha=.94,boxstyle='round,pad=.40'),zorder=12)
    ax.annotate('N',xy=(.943,.927),xytext=(.943,.843),xycoords='axes fraction',textcoords='axes fraction',size=10,weight='bold',color=DARK,ha='center',
                arrowprops=dict(arrowstyle='-|>',lw=1.5,color=DARK))
    # true 5km scale bar from source projected page units
    dx=5/km_per_pixel;x=extent[0]+(extent[1]-extent[0])*.052;y=extent[2]+(extent[3]-extent[2])*.061
    bh=(extent[3]-extent[2])*.011
    ax.add_patch(Rectangle((x,y),dx/2,bh,fc=DARK,ec=DARK,zorder=11));ax.add_patch(Rectangle((x+dx/2,y),dx/2,bh,fc='white',ec=DARK,zorder=11))
    ax.text(x,y+bh*2.2,'0',ha='center',size=8,weight='bold',color=DARK)
    ax.text(x+dx,y+bh*2.2,'5 km',ha='center',size=8,weight='bold',color=DARK)
    # Ward numbers only, no stacked category-count labels on geographic polygons.
    anchors=anchor(shapes)
    # Direct for wards with enough polygon display area, outside callouts for dense core wards.
    congested=[1,2,3,4,6,7,8,9,10,11,12,13]
    for w in qualified:
        if w in congested:continue
        px,py=anchors[w]
        ax.text(px,py,f'{w:02}',size=9.25,weight='bold',color=DARK,ha='center',va='center',zorder=11,
                path_effects=[pe.withStroke(linewidth=2.8,foreground='white')])
    # Small crowded inner-city polygons use two well-spaced outside callout rails.
    # These are map annotations (numbers), connected by leader lines.
    x_left=extent[0]+(extent[1]-extent[0])*.105
    x_right=extent[0]+(extent[1]-extent[0])*.87
    ytop=extent[3]-(extent[3]-extent[2])*.16
    spacing=(extent[3]-extent[2])*.048
    rail_left=[1,2,3,4,6,7]
    rail_right=[8,9,10,11,12,13]
    for rail,rx in [(rail_left,x_left),(rail_right,x_right)]:
        for k,w in enumerate(rail):
            yy=ytop-k*spacing
            ax.plot([anchors[w][0],rx],[anchors[w][1],yy],lw=.85,color='#687C8D',alpha=.85,zorder=6)
            ax.scatter([anchors[w][0]],[anchors[w][1]],s=7,color='#687C8D',zorder=7)
            # capsule keyed to the same fill as the polygon
            ax.text(rx,yy,f'{w:02}',ha='center',va='center',size=8.5,weight='bold',color=DARK,zorder=12,
                   bbox=dict(boxstyle='round,pad=.22',fc=colors[w],ec='white',lw=.75))
    # Right-column Nepal locator using real country outline (coarse Natural Earth-derived polygon)
    ia=fig.add_axes([.728,.706,.233,.174]);ia.set_facecolor('white')
    for s in ia.spines.values():s.set_edgecolor('#C5D3DF');s.set_linewidth(.8)
    country=np.asarray(NEPAL)
    ia.fill(country[:,0],country[:,1],facecolor='#E6EEF4',edgecolor='#55758E',lw=1.15,zorder=2)
    ia.set_xlim(79.55,88.65);ia.set_ylim(26.1,30.65);ia.set_aspect('equal',adjustable='box');ia.set_xticks([]);ia.set_yticks([])
    ia.text(.03,.97,'NEPAL  /  STUDY-AREA LOCATOR',transform=ia.transAxes,ha='left',va='top',size=9.0,weight='bold',color=DARK,zorder=5,
            bbox=dict(fc='white',ec='none',alpha=.92,pad=2))
    # Pokhara location and approximate 5km square-frame footprint at country scale
    ia.scatter([83.99],[28.21],s=33,c='#C93E43',edgecolors='white',linewidths=.6,zorder=6)
    ia.add_patch(Rectangle((83.99-.23,28.21-.2),.46,.40,fill=False,ec='#C93E43',lw=1.65,zorder=7))
    ia.annotate('Pokhara',xy=(83.99,28.21),xytext=(84.6,27.15),color='#B62E34',size=8.3,weight='bold',
                arrowprops=dict(arrowstyle='-',color='#B62E34',lw=.8),zorder=6)
    # Legend values table, two tall columns: 27 swatches with ward ID and E/NE counts.
    leg=fig.add_axes([.707,.179,.271,.49]);leg.axis('off')
    leg.add_patch(FancyBboxPatch((.008,.003),.984,.991,boxstyle='round,pad=.012,rounding_size=.018',fc='white',ec='#C5D3DF',lw=.85))
    leg.text(.055,.963,'WARD COLOR KEY  /  BUILDING COUNTS',size=9.6,weight='bold',color=DARK,va='top')
    leg.text(.055,.924,'E = engineered',size=8.2,weight='bold',color=BLUE)
    leg.text(.52,.924,'NE = non-engineered',size=8.2,weight='bold',color=ORANGE)
    leg.plot([.05,.95],[.903,.903],color='#D6E0E8',lw=.85)
    for idx,w in enumerate(qualified):
        column=0 if idx<14 else 1
        rank=idx if idx<14 else idx-14
        left=.055 if column==0 else .530
        yy=.866-rank*.0548
        if rank%2==0:
            leg.add_patch(Rectangle((left-.011,yy-.018),.438,.044,fc='#F6F8FB',ec='none'))
        leg.add_patch(Rectangle((left,yy-.011),.042,.027,fc=colors[w],ec='#64748B',lw=.65))
        leg.text(left+.058,yy,f'{w:02}',size=8.7,color=DARK,weight='bold',va='center')
        leg.text(left+.144,yy,f"{counts[w]['spatial_engineered']:02d}",size=8.7,color=BLUE,weight='bold',va='center')
        leg.text(left+.28,yy,f"{counts[w]['spatial_non_engineered']:02d}",size=8.7,color=ORANGE,weight='bold',va='center')
    leg.add_patch(Rectangle((.058,.049),.039,.025,fc=NONQUAL,ec=LINE,lw=.8))
    leg.text(.112,.061,'Other wards (not both categories)',size=7.8,color=MUTED,va='center')
    leg.text(.055,.019,'Ward color ↔ key row ↔ blue/orange count',size=7.65,color=MUTED,style='italic')
    # Lower metadata / sources, inside page frame not webpage card
    fig.lines.append(plt.Line2D([.052,.95],[.116,.116],transform=fig.transFigure,lw=.9,color='#CBD8E2'))
    fig.text(.055,.100,f'GEOGRAPHIC FRAME:  fixed square extent ~{side_km:.1f} × {side_km:.1f} km  |  Pokhara + 5 km minimum margin  |  EPSG:32645',size=8.3,color=DARK,weight='bold')
    fig.text(.055,.081,'INPUT: Rupesh Man Pradhan survey (266 records); source-ward and polygon-ward QA from V02.0.',size=8.0,color=MUTED)
    fig.text(.055,.063,'BOUNDARIES: Kathmandu Living Labs / OSM historic Pokhara 33 wards (generalized for display); Nepal locator: world.geo.json/NPL.',size=7.75,color=MUTED)
    fig.text(.055,.045,'QA LIMITATIONS: 50 field-label / spatial-ward conflicts; Ward 33 manual inclusion; boundary authority pending. Figure is for research review.',size=7.75,color='#99523A')
    fig.text(.953,.038,'STATIC PLATE • V02.3',ha='right',size=7.9,color=MUTED)
    fig.savefig(out,dpi=300,facecolor=BG)
    plt.close(fig)
    return {'png':str(out),'side_km':round(side_km,3),'qualifying':qualified,'colors':colors,'n_qualifying':len(qualified)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--counts',type=Path,required=True)
    p.add_argument('--geometry',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();args.output.parent.mkdir(parents=True,exist_ok=True)
    counts=load_counts(args.counts);shapes,m=load_shapes(args.geometry)
    details=draw(shapes,counts,m,args.output)
    receipt={
        'edition':'RMP_GIS_V02.3_WARD_COLOR_KEY_THESIS_PLATE',
        'status':'THESIS_REVIEW_FIGURE_QA_PENDING',
        'parent_milestone':'rupesh-gis/v0.1.4-source',
        'parent_source_commit':'c5be5a6ccc8912abc8bdda86e91a1dcda6fa403c',
        'source_geometry':'V02.1 generalized display geometry (not for GIS joins)',
        'source_counts':'V02.0 full-resolution spatial point-in-polygon counts (provisional)',
        'input_sha256':{f.name:output_hash(f) for f in [args.geometry,args.counts]},
        'figure_png_sha256':output_hash(args.output),
        'width_px':round(16.54*300),'height_px':round(11.69*300),
        'map_frame_side_km':details['side_km'],
        'qualifying_wards':details['qualifying'],
        'legend_mapping':details['colors'],
        'count_totals':{'engineered':150,'non_engineered':116,'source_spatial_conflicts':50,'manual_ward33_inclusion':1},
        'privacy':'No individual building locations; aggregated ward only',
        'country_inset':'world.geo.json / countries / NPL coarse Nepal boundary; locator only',
        'scientific_caveat':'Historical ward polygons; not certified. 50 ward assignment conflicts remain.',
        'out_png':args.output.name,
    }
    receipt_path=args.output.with_name('RMP_GIS_V02_3_RELEASE_QA_RECEIPT.json')
    receipt_path.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'png':str(args.output),'receipt':str(receipt_path),'qa':{'wards':len(details['qualifying']), 'side_km':details['side_km']}},indent=2))

if __name__=='__main__':main()
