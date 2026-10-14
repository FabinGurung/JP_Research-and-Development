#!/usr/bin/env python3
"""Rupesh GIS V02.1: deterministic static ward atlas; no Colab, tiles, or user GPS in Git.

Uses the 33-ward generalized DISPLAY geometry reprojected into the retained V02.0
square-display coordinates and the PREVIOUS full-resolution spatial join count CSV.
Source and official geometric authority caveats MUST remain visible in figure.

python RMP_GIS_V02_1_STATIC_WARD_ATLAS.py --geometry ward_display_cache.json \
  --counts RMP_WARD_COUNTS_SPATIAL_VS_RECORDED_v0.2.0.csv --out output_folder

If ward boundary authority or full-resolution source-join changes, rerun V02.0
spatial-join pipeline first and supply updated approved aggregate data. This script
DOES NOT perform a spatial join or accept private point coordinates.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as effects
from matplotlib.patches import Polygon, Rectangle, FancyBboxPatch, ConnectionPatch
import numpy as np

BLUE='#2569BF'; ORANGE='#D96A30'; DARK='#14243B'; MUTED='#54677D'; BG='#F7F9FC'


def load_counts(path: Path):
    with path.open(encoding='utf-8-sig',newline='') as stream:
        out=[{k: (int(v) if k in ('ward','spatial_engineered','spatial_non_engineered','recorded_engineered','recorded_non_engineered','source_spatial_disagreements','manual_location_exception') else v) for k,v in row.items()} for row in csv.DictReader(stream)]
    assert len(out)==33 and sorted(x['ward'] for x in out)==list(range(1,34))
    assert sum(x['spatial_engineered'] for x in out)==150
    assert sum(x['spatial_non_engineered'] for x in out)==116
    assert len([x for x in out if x['spatial_engineered']>0 and x['spatial_non_engineered']>0])==27
    assert sum(x['source_spatial_disagreements'] for x in out)==50
    assert sum(x['manual_location_exception'] for x in out)==1
    return {x['ward']:x for x in out}


def load_shapes(path:Path):
    data=json.loads(path.read_text(encoding='utf-8'))
    assert data['geometry_kind']=='cartographic_display_only_from_v0.2.0_svg'
    assert len(data['wards'])==33
    assert data['source_frame_side_km']==234.15
    return {int(k): np.array([[float(x),730-float(y)] for x,y in poly],dtype=float) for k,poly in data['wards'].items()}, data


def draw_main_map(ax,ward_geometry,counts,frame,kwal):
    ax.set_xlim(frame[0],frame[2]);ax.set_ylim(frame[1],frame[3]);ax.set_aspect('equal')
    ax.set_facecolor('#EBF2F7');ax.set_xticks([]);ax.set_yticks([])
    for s in ax.spines.values():s.set_edgecolor('#C5D8E6');s.set_linewidth(1.25)
    for w,pts in sorted(ward_geometry.items()):
        r=counts[w];qualified=r['spatial_engineered']>0 and r['spatial_non_engineered']>0
        face='#D9EAF4' if qualified else '#EEF0F3'
        patch=Polygon(pts,closed=True,edgecolor='white',facecolor=face,linewidth=1.1,zorder=2)
        ax.add_patch(patch)
        ax.plot(np.append(pts[:,0],pts[0,0]),np.append(pts[:,1],pts[0,1]),color='#9FB4C8',lw=.72,zorder=3)
    # Put clear ward numbers directly on the polygons; detailed E/NE values live in the panel.
    from shapely.geometry import Polygon as SPolygon
    for w,pts in sorted(ward_geometry.items()):
        if w not in kwal:continue
        p=SPolygon(pts)
        if not p.is_valid:p=p.buffer(0)
        if p.is_empty:continue
        rp=p.representative_point()
        ax.text(rp.x,rp.y,str(w).zfill(2),fontsize=8.5,ha='center',va='center',weight='bold',color='#1A466B',zorder=5,
                path_effects=[effects.withStroke(linewidth=2.2,foreground='white')])
    ax.text(.03,.965,'01   POKHARA  /  WARD BOUNDARIES',transform=ax.transAxes,ha='left',va='top',fontsize=11,color=DARK,weight='bold',zorder=8,
            bbox=dict(facecolor='#F7FAFD',alpha=.94,edgecolor='none',boxstyle='round,pad=.55'))
    # north arrow; projected WGS 84 / UTM zone 45N
    ax.annotate('N',xy=(.945,.94),xytext=(.945,.84),xycoords='axes fraction',textcoords='axes fraction',ha='center',va='center',fontsize=10,
                weight='bold',color=DARK,arrowprops={'arrowstyle':'-|>','lw':1.6,'color':DARK})
    # Scale bar: 5 km; source-pixel coordinates derive from original 234.15 km / 730 px map
    unit=234.15/730
    distance=5/unit
    bx=frame[0]+(frame[2]-frame[0])*.06;by=frame[1]+(frame[3]-frame[1])*.077
    h=(frame[3]-frame[1])*.009
    ax.add_patch(Rectangle((bx,by),distance/2,h,facecolor=DARK,edgecolor=DARK,zorder=8))
    ax.add_patch(Rectangle((bx+distance/2,by),distance/2,h,facecolor='white',edgecolor=DARK,zorder=8))
    ax.text(bx,by+h*2.7,'0',fontsize=8,color=DARK,ha='center',weight='bold',zorder=8)
    ax.text(bx+distance,by+h*2.7,'5 km',fontsize=8,color=DARK,ha='center',weight='bold',zorder=8)


def plot_atlas(geometry,counts,meta,out):
    os_wards=sorted(w for w,r in counts.items() if r['spatial_engineered']>0 and r['spatial_non_engineered']>0)
    allx=np.hstack([pts[:,0] for pts in geometry.values()]);ally=np.hstack([pts[:,1] for pts in geometry.values()])
    xmin,ymin,xmax,ymax=float(allx.min()),float(ally.min()),float(allx.max()),float(ally.max())
    # +5km outward offset on EVERY SIDE, then envelope expanded to a proper square.
    # 1 cached SVG-unit = 234.15/730 km (historical square extent).
    five_km=5/(meta['source_frame_side_km']/730)
    centre=((xmin+xmax)/2,(ymin+ymax)/2)
    half=max((xmax-xmin)/2,(ymax-ymin)/2)+five_km
    frame=(centre[0]-half,centre[1]-half,centre[0]+half,centre[1]+half)
    side_km=2*half*(meta['source_frame_side_km']/730)
    assert np.isclose(frame[2]-frame[0],frame[3]-frame[1]); assert len(os_wards)==27

    plt.rcParams.update({'font.family':'DejaVu Sans','savefig.facecolor':BG})
    fig=plt.figure(figsize=(19.2,13.0),facecolor=BG)
    fig.text(.047,.958,'RUPESH MAN PRADHAN  |  STRUCTURAL ENGINEERING RESEARCH',fontsize=12.5,color='#117C85',weight='bold')
    fig.text(.047,.916,'Pokhara  •  Engineered and non-engineered buildings',fontsize=24.0,color=DARK,weight='bold')
    fig.text(.047,.881,'Ward-level distribution  ·  27 wards with both building categories  ·  static thesis-review figure',fontsize=12,color=MUTED)
    fig.text(.950,.956,'GIS / V02.1',fontsize=11.5,color=DARK,weight='bold',ha='right')
    fig.text(.950,.930,'5 km OFFSET  •  SQUARE FRAME',fontsize=9,color=MUTED,ha='right')
    ax=fig.add_axes([.045,.205,.60,.639]);draw_main_map(ax,geometry,counts,frame,os_wards)
    # adjacent annotated ward summary table; blue/orange counts with readable typographic hierarchy
    x0=.69;w=.267
    fig.text(x0,.838,'02   WARD ANNOTATIONS',fontsize=13.3,color=DARK,weight='bold')
    fig.text(x0,.813,'Both scopes present (E > 0 and NE > 0)',fontsize=9.7,color=MUTED)
    fig.text(x0,.784,'WARD',fontsize=9.6,color=MUTED,weight='bold')
    fig.text(x0+.11,.784,'ENGINEERED',fontsize=9.2,color=BLUE,weight='bold')
    fig.text(x0+.215,.784,'NON-ENG.',fontsize=9.2,color=ORANGE,weight='bold')
    # 27 rows in 3 groups of 9; first group left inside panel, next group under? vertical layout right hand side only 27 rows fits if row step .019
    for j,ward in enumerate(os_wards):
        r=counts[ward];yy=.760-j*.0183
        if j%2==0:
            fig.patches.append(Rectangle((x0-.008,yy-.004),w+.015,.017,transform=fig.transFigure,facecolor='#EBF2F7',edgecolor='none',zorder=1))
        fig.text(x0,yy,f'WARD {ward:02d}',fontsize=9.0,color=DARK,weight='bold',zorder=3)
        fig.text(x0+.131,yy,str(r['spatial_engineered']).zfill(2),fontsize=9.0,color=BLUE,weight='bold',zorder=3)
        fig.text(x0+.236,yy,str(r['spatial_non_engineered']).zfill(2),fontsize=9.0,color=ORANGE,weight='bold',zorder=3)
        if r['source_spatial_disagreements'] or r['manual_location_exception']:
            fig.text(x0+.275,yy,'•',color='#A46E33',fontsize=10,ha='right',zorder=3)
    fig.text(x0,.239,'•  Recorded-ward vs polygon-ward mismatch,',fontsize=8.5,color='#996437')
    fig.text(x0+.015,.219,'or user-approved geometry exception.',fontsize=8.5,color='#996437')
    # lower full-width interpretation and evidence boundary / official cartographic terminology
    fig.patches.append(Rectangle((.046,.080),.906,.090,transform=fig.transFigure,facecolor='#E9F2F7',edgecolor='#D9E6EF',linewidth=.7,zorder=0))
    fig.text(.063,.143,'MAP FRAME',fontsize=9.7,color=DARK,weight='bold')
    fig.text(.063,.121,f'Square bounding extent ≈ {side_km:.1f} × {side_km:.1f} km',fontsize=10.0,color=DARK)
    fig.text(.063,.099,'EPSG:32645  |  buffered municipality envelope + 5 km minimum offset',fontsize=8.6,color=MUTED)
    fig.text(.535,.143,'DATA QUALITY',fontsize=9.7,color=DARK,weight='bold')
    fig.text(.535,.121,'266 included  •  150 engineered  •  116 non-engineered',fontsize=9.8,color=DARK)
    fig.text(.535,.099,'50 recorded-ward conflicts; Ward 33 manual inclusion; review pending',fontsize=8.6,color='#A45136')
    fig.text(.047,.050,'BOUNDARY  Kathmandu Living Labs / OSM (historical 33-ward polygons)  |  SOURCE  Rupesh researcher records; full-resolution V02.0 point-in-polygon QA',fontsize=8.8,color=MUTED)
    fig.text(.047,.030,'Geometry here: generalized/cartographic V02.0 display cache. Ward counts remain provisional pending boundary authority and source-ward reconciliation. No individual points shown.',fontsize=8.45,color=MUTED)
    fn=out/'RMP_POKHARA_WARD_SUMMARY_5KM_SQUARE_STATIC_v0.2.1.png'
    fig.savefig(fn,dpi=210,facecolor=BG,bbox_inches=None)
    plt.close(fig)
    return fn,frame,side_km,os_wards


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--geometry',type=Path,required=True,help='Approved generalized polygon cache from V02.0; does NOT contain any points')
    p.add_argument('--counts',type=Path,required=True,help='Full-resolution V02.0 point-in-polygon reconciled ward counts CSV')
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    shapes,meta=load_shapes(args.geometry);counts=load_counts(args.counts)
    fn,frame,side,wards=plot_atlas(shapes,counts,meta,args.out)
    trace={
      'edition':'RMP_GIS_V02.1_STATIC_THESIS_WARD_ATLAS',
      'parent_git_milestone':'rupesh-gis/v0.1.4-source',
      'parent_rupesh_v02_source_commit':'3964b4dee18789f2d68ebb8c908ec66f35255a73',
      'status':'RESEARCH_PREVIEW_BOUNDARY_AND_WARD_ASSIGNMENTS_QA_OPEN',
      'map_type':'STATIC_PNG_ONLY',
      'map_frame':'5km buffered municipality boundary then square bounding extent, planar UTM45N',
      'map_extent_side_km_approx':round(side,3),
      'wards_with_both_categories':wards,
      'qa':{'input_records':266,'engineered':150,'non_engineered':116,'spatial_source_conflicts':50,'manual_ward33_inclusions':1},
      'display_geometry':'generalized map-only shapes derived from the preserved V02.0 SVG output; previous full-resolution spatial join counts are not recalculated here',
      'input_hashes':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in (args.geometry,args.counts)},
      'output':{'png':fn.name,'sha256':hashlib.sha256(fn.read_bytes()).hexdigest()},
      'boundary_authority':'KLL/OSM historical; NOT a certified municipal boundary; scientific QA open',
      'privacy':'No building point coordinates drawn or embedded',
    }
    receipt=args.out/'RMP_GIS_V02_1_STATIC_RUN_RECEIPT.json';receipt.write_text(json.dumps(trace,indent=2)+'\n')
    print(json.dumps({'png':str(fn),'receipt':str(receipt),'side_km':round(side,3),'count_qualifying':len(wards),'png_bytes':fn.stat().st_size},indent=2))

if __name__=='__main__':main()