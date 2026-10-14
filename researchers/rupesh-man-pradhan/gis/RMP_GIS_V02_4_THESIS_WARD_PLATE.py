#!/usr/bin/env python3
"""Reproduce Rupesh Man Pradhan's static Pokhara ward-count thesis plate.

Inputs are source-derived aggregate ward counts (full-resolution spatial join)
and cartographically generalized ward display geometry from the preceding
GIS editions. A genuine Natural Earth country polygon is used as the Nepal
locator. No individual building coordinates are read into the figure.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

import geopandas as gpd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as effects
import numpy as np
import pandas as pd
from matplotlib.patches import Polygon as MapPolygon, Rectangle, FancyBboxPatch
from shapely.geometry import Polygon
from pyproj import Transformer

BLUE = '#1866C9'
ORANGE = '#CB580F'
NAVY = '#17324D'
SLATE = '#53677C'
MARGIN_KM = 5.0
# Distinguishable fills correspond to ward IDs in the figure key, not a metric.
COLORS = ['#F5C77B','#A6B7F0','#99E1AF','#EFB2CF','#9BD3EA','#F3B98B',
          '#B8A3DC','#E8D882','#EEA2BD','#A9DCD7','#A7C6E8','#EDD09A',
          '#D9B3DD','#A6DDE0','#E6AE7C','#C1DE8A','#B0D5F2','#D7D8ED',
          '#A6D8B3','#BCACE9','#8FE2B1','#EE9CA6','#A3C9F3','#DDE995',
          '#E8A4E4','#9BDECF','#D5AA91','#B8A6DF','#91A4E0','#AAD58E',
          '#EFA5C5','#91D5E6','#F1E491']


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def color_for(ward: int) -> str:
    return COLORS[ward-1]


def label_chip(ax, pos, count_e: int, count_n: int, scale: float):
    x, y = pos
    halo = [effects.withStroke(linewidth=2.7, foreground='white')]
    dy = scale * 0.010
    ax.text(x,y+dy, str(count_e), ha='center',va='center',fontsize=8.4,
            weight='bold',color=BLUE,path_effects=halo,zorder=9)
    ax.text(x,y-dy,str(count_n),ha='center',va='center',fontsize=8.4,
            weight='bold',color=ORANGE,path_effects=halo,zorder=9)


def create(input_counts: Path, input_geometry: Path, nepal_geojson: Path,
           output_png: Path, receipt_path: Path):
    records=pd.read_csv(input_counts).set_index('ward')
    data=json.loads(input_geometry.read_text('utf-8'))
    assert len(data['wards']) == 33
    assert len(records) == 33
    assert records.spatial_engineered.sum()==150
    assert records.spatial_non_engineered.sum()==116
    qualifying=[w for w in range(1,34) if int(records.loc[w,'spatial_engineered'])>0
                and int(records.loc[w,'spatial_non_engineered'])>0]
    assert len(qualifying)==27
    # Source map projected to 730-pixel square with side 234.15 km. Invert SVG y.
    wards={int(w):np.array([(x,730.0-y) for x,y in pts],dtype=float)
           for w,pts in data['wards'].items()}
    source_side_km=float(data['source_frame_side_km'])
    km_per_unit=source_side_km/float(data['source_frame_px'])
    arr=np.vstack(list(wards.values()))
    xmin,ymin=np.min(arr,axis=0); xmax,ymax=np.max(arr,axis=0)
    xmid,ymid=(xmin+xmax)/2,(ymin+ymax)/2
    half=max((xmax-xmin)/2,(ymax-ymin)/2)+(MARGIN_KM/km_per_unit)
    frame=(xmid-half,xmid+half,ymid-half,ymid+half)
    side=2*half*km_per_unit
    assert 44<side<45

    nepal=gpd.read_file(nepal_geojson)
    nepal=nepal.to_crs('EPSG:4326')
    # GeoJSON is a copied Natural Earth / Nepal boundary; robustly select all polygons.
    if 'name' in nepal.columns:
        n=nepal[nepal['name'].astype(str).str.lower().eq('nepal')]
        if not n.empty: nepal=n
    assert len(nepal)>0
    outline=nepal.geometry.union_all()
    assert outline.bounds[0]<81 and outline.bounds[2]>87

    # Plotting-only style: A3 landscape, 300 DPI, no webpage furniture.
    fig=plt.figure(figsize=(16.54,11.69),facecolor='white')
    fig.text(.048,.956,'RUPESH MAN PRADHAN  |  STRUCTURAL ENGINEERING THESIS',
             size=10.5,weight='bold',color='#17788C')
    fig.text(.048,.917,'Spatial distribution of building survey categories across Pokhara wards',
             size=19.5,weight='bold',color=NAVY)
    fig.text(.048,.891,'Ward-wise counts of engineered and non-engineered buildings  ·  Pokhara Metropolitan City',
             size=9.7,color=SLATE)
    # City panel
    ax=fig.add_axes([.048,.180,.620,.664]); ax.set_aspect('equal');ax.set_facecolor('#F8FAFC')
    ax.set_xlim(frame[0],frame[1]); ax.set_ylim(frame[2],frame[3]);ax.set_xticks([]);ax.set_yticks([])
    for s in ax.spines.values(): s.set_color('#BACAD6');s.set_linewidth(.85)
    ax.text(.023,.976,'POKHARA  /  WARD COUNT MAP',ha='left',va='top',transform=ax.transAxes,
            fontsize=10,weight='bold',color=NAVY)
    polys={}
    for w,p in sorted(wards.items()):
        pol=Polygon(p).buffer(0)
        polys[w]=pol
        ax.add_patch(MapPolygon(p,closed=True,edgecolor='#778D9D',linewidth=.8,
                    facecolor=color_for(w) if w in qualifying else '#EEF0F2',zorder=2))
    # Small wards: selective callouts; data labels contain counts only.
    # Offset in plot-units; each line starts on the actual polygon.
    callouts={1:(-8,11),2:(-4,13),3:(4,12),4:(10,13),5:(0,0),6:(-9,6),
              7:(-10,-3),8:(10,-4),9:(11,-2),10:(-10,-8),11:(9,-9),12:(11,2),13:(13,-6)}
    width=frame[1]-frame[0]
    anchors={w:polys[w].representative_point() for w in polys}
    for w in qualifying:
        anchor=anchors[w]
        x,y=anchor.x,anchor.y
        if w in callouts:
            dx,dy=callouts[w]
            dest=(x+dx,y+dy)
            ax.plot([x,dest[0]],[y,dest[1]],color='#61788A',lw=.68,zorder=7)
            ax.scatter([x],[y],s=8,color='#61788A',zorder=8)
        else: dest=(x,y)
        label_chip(ax,dest,int(records.loc[w,'spatial_engineered']),
                   int(records.loc[w,'spatial_non_engineered']),width)
    # North arrow
    ax.annotate('',xy=(.952,.928),xytext=(.952,.830),xycoords='axes fraction',
                arrowprops=dict(arrowstyle='-|>',color=NAVY,lw=1.5))
    ax.text(.952,.944,'N',transform=ax.transAxes,ha='center',weight='bold',fontsize=10,color=NAVY)
    # Scale bar: geometric scaling to map projected units, 5km exactly.
    sx=frame[0]+width*.065;sy=frame[2]+width*.063;bar=5/km_per_unit
    ax.add_patch(Rectangle((sx,sy),bar/2,width*.008,facecolor=NAVY,edgecolor=NAVY,zorder=11))
    ax.add_patch(Rectangle((sx+bar/2,sy),bar/2,width*.008,facecolor='white',edgecolor=NAVY,zorder=11))
    ax.text(sx,sy+width*.025,'0',fontsize=7.6,color=NAVY,ha='center')
    ax.text(sx+bar,sy+width*.025,'5 km',fontsize=7.6,color=NAVY,ha='center')

    # REAL Nepal locator from Natural Earth: lon/lat coordinates + pyproj extent.
    loc=fig.add_axes([.70,.645,.260,.197]);loc.set_aspect('equal');loc.set_facecolor('#FAFCFE')
    for s in loc.spines.values():s.set_color('#C0CFDA');s.set_linewidth(.8)
    for part in (outline.geoms if hasattr(outline,'geoms') else [outline]):
        lons,lats=part.exterior.xy
        loc.fill(lons,lats,color='#E6EEF5',edgecolor='#4C647C',lw=.75)
    loc.set_xlim(79.6,88.5);loc.set_ylim(26.1,31.2);loc.set_xticks([]);loc.set_yticks([])
    loc.text(.03,.97,'NEPAL  /  STUDY AREA',transform=loc.transAxes,va='top',fontsize=9.8,color=NAVY,weight='bold')
    # Mark the Pokhara-centered 5km square extent using a true projected CRS conversion.
    transformer=Transformer.from_crs('EPSG:4326','EPSG:32645',always_xy=True)
    inv=Transformer.from_crs('EPSG:32645','EPSG:4326',always_xy=True)
    C=transformer.transform(83.9856,28.2096)
    hh=side*1000/2
    ring=[(C[0]-hh,C[1]-hh),(C[0]+hh,C[1]-hh),(C[0]+hh,C[1]+hh),
          (C[0]-hh,C[1]+hh),(C[0]-hh,C[1]-hh)]
    rlon=[inv.transform(x,y)[0] for x,y in ring]
    rlat=[inv.transform(x,y)[1] for x,y in ring]
    loc.plot(rlon,rlat,color='#D64B4D',lw=1.25,zorder=5)
    loc.scatter([83.9856],[28.2096],s=17,color='#B83239',zorder=7)
    loc.annotate('Pokhara',xy=(83.9856,28.2096),xytext=(85.15,29.0),
                 color='#B83239',fontsize=8.3,weight='bold',
                 arrowprops=dict(arrowstyle='-',lw=.8,color='#B83239'))
    loc.text(.035,.12,'India',transform=loc.transAxes,fontsize=7.5,color=SLATE)
    loc.text(.71,.85,'China',transform=loc.transAxes,fontsize=7.5,color=SLATE)
    loc.text(.035,.035,'Natural Earth 1:110m · Nepal country boundary',
             transform=loc.transAxes,fontsize=6.4,color=SLATE)
    # Legend, 27 ward rows. No ward IDs written inside polygons.
    l=fig.add_axes([.70,.182,.260,.448]);l.set_xlim(0,1);l.set_ylim(0,1);l.axis('off')
    l.add_patch(FancyBboxPatch((.008,.005),.984,.990,boxstyle='round,pad=.004',
                facecolor='#FBFCFD',edgecolor='#CBD7E2',linewidth=.85))
    l.text(.055,.955,'WARD COLOR KEY  /  BUILDING COUNTS',color=NAVY,weight='bold',fontsize=10.2)
    l.text(.055,.908,'Engineered',color=BLUE,weight='bold',fontsize=8.7)
    l.text(.390,.908,'Non-engineered',color=ORANGE,weight='bold',fontsize=8.7)
    per=14;step=.052
    for i,w in enumerate(qualifying):
        col=0 if i<per else 1;j=i if col==0 else i-per
        left=.050 if col==0 else .535
        y=.845-j*step
        l.add_patch(Rectangle((left,y-.014),.045,.028,facecolor=color_for(w),edgecolor='#7A91A3',lw=.4))
        l.text(left+.062,y,f'{w:02d}',color=NAVY,fontsize=8.3,weight='bold',va='center')
        l.text(left+.145,y,str(int(records.loc[w,'spatial_engineered'])),
               color=BLUE,fontsize=8.6,weight='bold',va='center')
        l.text(left+.240,y,str(int(records.loc[w,'spatial_non_engineered'])),
               color=ORANGE,fontsize=8.6,weight='bold',va='center')
    l.text(.052,.077,'Ward ID = fill color; numbers on the map = counts.',fontsize=8.0,color=SLATE)
    l.add_patch(Rectangle((.052,.035),.037,.023,facecolor='#EEF0F2',edgecolor='#7A91A3',lw=.5))
    l.text(.105,.046,'Ward outside the two-category scope',fontsize=7.7,color=SLATE,va='center')
    # Publication-only footer: factual source attribution without internal review language.
    fig.text(.05,.131,'MAP FRAME   Square extent · 5 km minimum outward margin · WGS 84 / UTM Zone 45N (EPSG:32645)',
             fontsize=9,color=NAVY,weight='bold')
    fig.text(.05,.105,'DATA   Rupesh Man Pradhan building survey; 150 engineered and 116 non-engineered locations (n = 266).',
             fontsize=8.4,color=SLATE)
    fig.text(.05,.081,'WARD LAYER   Kathmandu Living Labs / OpenStreetMap, historical Pokhara 33-ward polygons; generalized display geometry.',
             fontsize=8.4,color=SLATE)
    fig.text(.05,.057,'LOCATOR   Natural Earth 1:110m national boundary; Pokhara study-area extent shown approximately.',
             fontsize=8.4,color=SLATE)
    fig.text(.96,.044,'FIGURE  |  RMP-GIS-02.4',ha='right',fontsize=8.7,weight='bold',color=NAVY)
    output_png.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(output_png,dpi=300,facecolor='white')
    plt.close(fig)
    receipt={
        'edition':'RMP_GIS_V02_4_SPATIAL_WARD_PUBLICATION_PLATE',
        'preceding_git_edition':'V02.3',
        'parent_milestone':'rupesh-gis/v0.1.4-source',
        'input_geometry_sha256':sha256(input_geometry),
        'input_counts_sha256':sha256(input_counts),
        'input_nepal_geojson_sha256':sha256(nepal_geojson),
        'static_png_sha256':sha256(output_png),
        'counts_method':'Full-resolution source V02.0 spatial-ward assignment; spatial ward authoritative; one Ward 33 user-approved original-label inclusion retained because coordinate is outside GIS polygons',
        'source_vs_spatial_reassignments':50,
        'source_count':266,'engineered':150,'non_engineered':116,
        'qualifying_wards':qualifying,'qualifying_count':27,
        'frame_side_km':side,'buffer_margin_km':MARGIN_KM,
        'projection':'EPSG:32645',
        'display_geometry':'Generalized 730-unit source map geometry; no new point-in-polygon performed here',
        'nepal_outline':'Natural Earth 1:110m administered country outline, not schematic art',
        'locator_extent':'Approximate study-area rectangle centered on Pokhara, 44-km projected square; not a cadastral locator',
        'thesis_figure_text':'Publication-oriented static cartography and source attribution',
        'individual_points_in_publication_png':False,
        'png_pixels':[4962,3507],
        'output_file':output_png.name
    }
    receipt_path.write_text(json.dumps(receipt,indent=2)+'\n','utf-8')
    print(json.dumps({'figure':str(output_png),'sha256':receipt['static_png_sha256'],
                      'km_side':round(side,3),'qualifying_wards':len(qualifying),'output_bytes':output_png.stat().st_size}))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--counts',type=Path,required=True)
    p.add_argument('--geometry',type=Path,required=True)
    p.add_argument('--nepal',type=Path,required=True)
    p.add_argument('--png',type=Path,required=True)
    p.add_argument('--receipt',type=Path,required=True)
    a=p.parse_args()
    create(a.counts,a.geometry,a.nepal,a.png,a.receipt)
