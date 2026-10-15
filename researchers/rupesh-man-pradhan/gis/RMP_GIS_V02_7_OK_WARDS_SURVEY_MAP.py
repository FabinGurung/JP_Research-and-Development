#!/usr/bin/env python3
"""Render a non-interactive Pokhara ward/building map from preserved GIS sources.
No coordinates are generated or moved; all point inclusion uses pre-validated spatial ward joins.
"""
import argparse, json, hashlib, re
from pathlib import Path
import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely.affinity import affine_transform
from pyproj import Transformer
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

PALETTE=['#4e79a7','#f28e2b','#59a14f','#e15759','#76b7b2','#edc948','#b07aa1','#ff9da7','#9c755f','#86bcb6','#af7aa1']
CRS='EPSG:32645'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def generate(xlsx,points_csv,join_csv,municipality_shp,ward_display_json,output_dir):
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
    original=pd.read_excel(xlsx,sheet_name='Non_Engineered_Building_Coordin',header=None)
    ok=[]
    for _,r in original.iterrows():
        if pd.isna(r.iloc[1]):continue
        m=re.search(r'ward\s*(?:no\.?\s*)?(\d+)',str(r.iloc[1]),re.I)
        if m and str(r.iloc[0]).strip().upper()=='OK':ok.append(int(m.group(1)))
    ok=sorted(set(ok));assert ok==[11,21,24,25,26,27,29,30,31,32,33],ok
    pts=pd.read_csv(points_csv);joins=pd.read_csv(join_csv)
    assert len(pts)==len(joins)==266 and pts.point_id.is_unique and joins.point_id.is_unique
    assert set(pts.point_id)==set(joins.point_id)
    assert pts.category.value_counts().to_dict()=={'Engineered':150,'Non-engineered':116}
    joined=pts.merge(joins[['point_id','spatial_ward','status']],on='point_id',validate='one_to_one')
    active=joined[joined.spatial_ward.isin(ok)].copy()
    excluded=joined[~joined.spatial_ward.isin(ok)].copy()
    assert len(active)==104 and active.category.value_counts().to_dict()=={'Engineered':57,'Non-engineered':47}
    assert active.latitude.between(28,28.5).all()
    mun=gpd.read_file(municipality_shp)
    assert len(mun)==777
    city=mun[mun['GaPa_NaPa'].str.contains('Pokhara Lekhnath',case=False,na=False)]
    assert len(city)==1
    city_utm=city.to_crs(CRS).geometry.iloc[0]
    country=mun.to_crs('EPSG:4326').geometry.union_all()
    cache=json.loads(Path(ward_display_json).read_text());assert len(cache['wards'])==33
    ward_px={int(w):Polygon([(x,730-y) for x,y in v]).buffer(0) for w,v in cache['wards'].items()}
    px_union=unary_union(list(ward_px.values()))
    meters_per_px=float(cache['source_frame_side_km'])*1000/float(cache['source_frame_px'])
    a=(px_union.bounds[0]+px_union.bounds[2])/2;b=(px_union.bounds[1]+px_union.bounds[3])/2
    c=(city_utm.bounds[0]+city_utm.bounds[2])/2;d=(city_utm.bounds[1]+city_utm.bounds[3])/2
    transform=[meters_per_px,0,0,meters_per_px,c-meters_per_px*a,d-meters_per_px*b]
    ward={w:affine_transform(g,transform) for w,g in ward_px.items()}
    rendered_union=unary_union(list(ward.values()))
    iou=city_utm.intersection(rendered_union).area/city_utm.union(rendered_union).area
    assert iou>.97
    loc=gpd.GeoDataFrame(active,geometry=gpd.points_from_xy(active.longitude,active.latitude),crs='EPSG:4326').to_crs(CRS)
    inside_mask=np.array([p.within(ward[int(w)]) for p,w in zip(loc.geometry,loc.spatial_ward)])
    held_display=loc.loc[~inside_mask,['point_id','category','spatial_ward','recorded_ward' if 'recorded_ward' in loc.columns else 'ward']].copy()
    held_display.to_csv(out/'RMP_GIS_V02_7_DISPLAY_BOUNDARY_HOLD.csv',index=False)
    loc=loc.loc[inside_mask].copy()
    inside=len(loc)
    assert inside==95,inside
    xmin,ymin,xmax,ymax=city_utm.bounds
    midx=(xmin+xmax)/2;midy=(ymin+ymax)/2
    half=max((xmax-xmin)/2,(ymax-ymin)/2)+5000
    box=(midx-half,midx+half,midy-half,midy+half)
    fig=plt.figure(figsize=(16.54,11.69),dpi=300,facecolor='white')
    ax=fig.add_axes([.065,.085,.652,.815])
    ax.set_aspect('equal');ax.set_xlim(box[0],box[1]);ax.set_ylim(box[2],box[3])
    for w in range(1,34):
        p=ward[w];x,y=p.exterior.xy
        fc=PALETTE[ok.index(w)] if w in ok else '#d8dcdf'
        ax.fill(x,y,fc=fc,ec='#6d7883',lw=.65,alpha=.83 if w in ok else .72,zorder=2)
    x,y=city_utm.exterior.xy;ax.plot(x,y,color='#1e344c',lw=1.5,zorder=3)
    for category,color,marker,size in [('Non-engineered','#e87722','o',28),('Engineered','#1763ce','^',31)]:
        df=loc[loc.category==category]
        ax.scatter(df.geometry.x,df.geometry.y,c=color,marker=marker,s=size,edgecolors='white',linewidths=.5,zorder=5)
    # Graticule transforms longitude/latitude lines into UTM metres.
    fwd=Transformer.from_crs('EPSG:4326',CRS,always_xy=True)
    inv=Transformer.from_crs(CRS,'EPSG:4326',always_xy=True)
    lon,lat=inv.transform([box[0],box[1],box[0],box[1]],[box[2],box[2],box[3],box[3]])
    for ll in np.arange(np.floor(min(lon)/.05)*.05,max(lon)+.05,.05):
        xx,yy=fwd.transform(np.full(150,ll),np.linspace(min(lat)-.1,max(lat)+.1,150))
        ax.plot(xx,yy,ls='--',lw=.5,color='#bfcbd6',zorder=1)
    for la in np.arange(np.floor(min(lat)/.05)*.05,max(lat)+.05,.05):
        xx,yy=fwd.transform(np.linspace(min(lon)-.1,max(lon)+.1,150),np.full(150,la))
        ax.plot(xx,yy,ls='--',lw=.5,color='#bfcbd6',zorder=1)
    ax.set_xticks(np.arange(np.ceil(box[0]/5000)*5000,box[1],5000));ax.set_yticks(np.arange(np.ceil(box[2]/5000)*5000,box[3],5000))
    ax.ticklabel_format(style='plain');ax.tick_params(labelsize=8)
    ax.set_xlabel('Easting (m), UTM Zone 45N',fontsize=10);ax.set_ylabel('Northing (m), UTM Zone 45N',fontsize=10)
    ax.plot([box[0]+2500,box[0]+7500],[box[2]+2800]*2,lw=2.8,c='#1a2732',zorder=9)
    for xx in [box[0]+2500,box[0]+5000,box[0]+7500]:ax.plot([xx,xx],[box[2]+2550,box[2]+3050],c='#1a2732',lw=1.4,zorder=9)
    ax.text(box[0]+5000,box[2]+3300,'5 km',fontsize=10,ha='center')
    ax.annotate('',xy=(.965,.915),xytext=(.965,.835),xycoords='axes fraction',arrowprops=dict(arrowstyle='-|>',lw=1.5,color='#1a2732'))
    ax.text(.965,.922,'N',transform=ax.transAxes,ha='center',fontsize=11,weight='bold')
    fig.text(.07,.945,'Surveyed building locations in selected wards of Pokhara',weight='bold',fontsize=19)
    # Nepal national outline is dissolved from the user's local-unit shapefile, not drawn artistically.
    locator=fig.add_axes([.76,.67,.21,.225]);gpd.GeoSeries([country],crs='EPSG:4326').plot(ax=locator,fc='#e5ebf0',ec='#41586b',lw=1.0)
    study=gpd.GeoSeries([city_utm],crs=CRS).to_crs('EPSG:4326').geometry.iloc[0]
    x,y=study.exterior.xy;locator.plot(x,y,c='#ae2435',lw=1.5)
    l,b,r,t=study.bounds;locator.add_patch(Rectangle((l,b),r-l,t-b,fill=False,ec='#ae2435',lw=1.4))
    locator.set_xlim(79.7,88.6);locator.set_ylim(26.0,30.9)
    locator.set_xticks([80,82,84,86,88]);locator.set_yticks([27,29]);locator.tick_params(labelsize=8)
    locator.grid(alpha=.35,ls=':');locator.set_title('Nepal — study area',fontsize=11)
    legend=fig.add_axes([.755,.075,.22,.55]);legend.axis('off')
    legend.text(.02,.96,'Legend',fontsize=13,weight='bold',transform=legend.transAxes)
    legend.text(.02,.9,'Wards labelled OK',fontsize=10,transform=legend.transAxes)
    for i,w in enumerate(ok):
        col=0 if i<6 else 1;row=i if i<6 else i-6
        x=.04 if col==0 else .54;y=.83-row*.102
        legend.add_patch(Rectangle((x,y),.09,.05,transform=legend.transAxes,fc=PALETTE[i],ec='#6d7883',lw=.5))
        legend.text(x+.12,y+.006,f'Ward {w}',fontsize=9.5,transform=legend.transAxes)
    legend.add_patch(Rectangle((.04,.185),.09,.05,transform=legend.transAxes,fc='#d8dcdf',ec='#6d7883',lw=.5))
    legend.text(.17,.191,'Other wards (no points)',fontsize=9,transform=legend.transAxes)
    legend.scatter([.075],[.12],marker='^',s=78,c='#1763ce',transform=legend.transAxes)
    legend.text(.17,.108,f"Engineered ({sum(loc.category=='Engineered')})",fontsize=9.7,transform=legend.transAxes)
    legend.scatter([.075],[.054],marker='o',s=72,c='#e87722',transform=legend.transAxes)
    legend.text(.17,.04,f"Non-engineered ({sum(loc.category=='Non-engineered')})",fontsize=9.7,transform=legend.transAxes)
    png=out/'RMP_POKHARA_OK_WARDS_BUILDING_LOCATIONS_v0.2.7.png';fig.savefig(png,facecolor='white');plt.close(fig)
    receipt={'edition':'0.2.7','source_sha256':{Path(n).name:sha(n) for n in [xlsx,points_csv,join_csv,municipality_shp,ward_display_json]},
      'output_png':png.name,'output_sha256':sha(png),'ok_wards':ok,'spatially_eligible_total':len(active),'plotted_total':len(loc),
      'engineered_plotted':sum(loc.category=='Engineered'),'non_engineered_plotted':sum(loc.category=='Non-engineered'),
      'excluded_total':len(excluded),'display_cache_to_municipality_polygon_iou':iou,
      'display_ward_contains_point_count':int(inside),'display_ward_contains_point_total':len(active),'held_display_boundary_points':len(held_display),
      'map_crs':CRS,'municipal_source_crs':'NepalDD / Everest 1830','square_extent_side_m':half*2,
      'points_spatial_assignment':'Full-resolution KLL ward spatial join QA V02.0. Ward geometry displayed from a generalized GIS-derived cache, registered to the municipal boundary.',
      'scientific_limit':'Generalized historical ward boundaries; nine spatially eligible records withheld because their precise coordinate plots across the rendered ward border. Not certified as official municipal ward demarcation.',
      'one_unlocated_record':'RMP-ENG-W33-R207: latitude 21.138118. Preserved, not plotted.'}
    r=out/'RMP_GIS_V02_7_RUN_RECEIPT.json';r.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2));return png
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for key in ['xlsx','points_csv','join_csv','municipality_shp','ward_display_json','output_dir']:p.add_argument('--'+key,required=True)
    a=p.parse_args();generate(**vars(a))
