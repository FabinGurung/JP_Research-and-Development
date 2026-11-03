import runpy
from pathlib import Path
g=runpy.run_path(str(Path(__file__).with_name('redraw_seq067.py')));globals().update({k:v for k,v in g.items() if not k.startswith('__')})
from matplotlib.patches import Rectangle,FancyBboxPatch,Arc

def clusters(v):return [float(a.mean()) for a in np.split(v,np.where(np.diff(v)>3)[0]+1) if len(a)]
def tsv(path):
    txt=subprocess.check_output(['tesseract',str(path),'stdout','--psm','11','tsv'],stderr=subprocess.DEVNULL).decode()
    return list(csv.DictReader(io.StringIO(txt),delimiter='\t'))
def xcal(path,ybottom):
    pts=[]
    for r in tsv(path):
        s=r['text'].strip()
        if re.fullmatch(r'\d+(?:\.\d+)?',s) and ybottom+20<int(r['top'])<ybottom+90:
            v=float(s)
            if v<=200:pts.append((int(r['left'])+int(r['width'])/2,v))
    assert len(pts)>=2,(path,pts)
    a,b=np.polyfit([p[0] for p in pts],[p[1] for p in pts],1)
    return a,b,pts
def raster_axes(path,yticks,kind,name):
    a=np.array(Image.open(path).convert('RGB'));dark=a.max(2)<100
    x0=int(dark.sum(0).argmax());rr=dark[:,x0:].sum(1)
    yy=np.where(rr>.7*(a.shape[1]-x0))[0];yb=int(yy.max());yt=int(np.where(dark[:,x0])[0].min());x1=int(np.where(dark[yb])[0].max())
    tickcenters=clusters(np.where(dark[:,x0-12:x0-2].sum(1)>6)[0])
    assert len(tickcenters)==len(yticks),(name,tickcenters,yticks)
    sy,by=np.polyfit(tickcenters,yticks,1)
    if kind=='pga':
        color=(a.max(2)-a.min(2)>40)&(a.min(2)<220)
        cc=clusters(np.where(color[yt:yb].sum(0)>40)[0])
        assert len(cc)==12,(name,cc)
        sx,bx=np.polyfit(cc,range(12),1)
    else:sx,bx,_=xcal(path,yb)
    crop=a[yt+2:yb-1,x0+2:x1-1].copy()
    colored=(crop.max(2)-crop.min(2)>40)&(crop.min(2)<220)
    # Remove grayscale raster text and axes only. Original coloured curve/bar pixels are retained exactly.
    crop[~colored]=255
    if kind=='spectra':
        # The source legend sits in the empty top-right region, above the response curves.
        crop[:480,2300-x0:]=255
    extent=[sx*(x0+2)+bx,sx*(x1-1)+bx,sy*(yb-1)+by,sy*(yt+2)+by]
    h=4.6 if kind=='spectra' else 4.0 if kind=='pga' else 3.15
    fig,ax=axes(h,legend=kind=='spectra')
    if kind=='pga':fig.subplots_adjust(bottom=.43)
    if kind=='spectra':fig.subplots_adjust(bottom=.42)
    ax.imshow(crop,extent=extent,aspect='auto',interpolation='none',zorder=2)
    ax.set_xlim(extent[0],extent[1]);ax.set_ylim(extent[2],extent[3]);ax.set_yticks(yticks)
    if kind=='pga':
        names=['Chi-Chi','Friuli','Hollister','Imperial Valley','Kobe','Kocaeli','Landers','Loma Prieta','Northridge','San Fernando','Trinidad','Gorkha']
        ax.set_xticks(range(12),names,rotation=60,ha='right');ax.set_xlabel('Ground-motion record');ax.set_ylabel('Peak ground acceleration (g)')
    elif kind=='spectra':
        ax.set_xticks(np.arange(0,5.1,1));ax.set_xlabel('Period, T (s)');ax.set_ylabel('Spectral acceleration (g)')
        names=['Chi-Chi','Friuli','Hollister','Imperial Valley','Kobe','Kocaeli','Landers','Loma Prieta','Northridge','San Fernando','Trinidad']
        # Original source uses the tab10 cycle: Trinidad repeats the first blue.
        colors=[plt.cm.tab10(i%10) for i in range(11)]
        ax.legend([Line2D([],[],color=c,lw=1.3) for c in colors],names,loc='upper center',bbox_to_anchor=(.5,-.28),ncol=3,frameon=False,columnspacing=.8,handlelength=1.2)
    else:
        ax.set_xlabel('Time (s)');ax.set_ylabel('Acceleration (m/s²)');ax.axhline(0,color='#d5d5d5',lw=.6,zorder=1)
    save(fig,name,str(path.relative_to(P)),str(path.relative_to(P)),{'method':'Existing coloured plotted pixels retained; grayscale text/axes replaced','source_plot_box_px':[x0,yt,x1,yb],'source_curve_raster_sha256':hashlib.sha256(crop.tobytes()).hexdigest(),'extent':extent,'y_tick_values':yticks})

ys=[[2,1,0,-1,-2,-3],[3,2,1,0,-1,-2],[2,1.5,1,.5,0,-.5,-1],[3,2,1,0,-1,-2,-3],[3,2,1,0,-1,-2],[2,1,0,-1,-2,-3],[6,4,2,0,-2,-4,-6,-8],[3,2,1,0,-1,-2,-3],[6,4,2,0,-2],[.2,.1,0,-.1,-.2],[2,1.5,1,.5,0,-.5,-1,-1.5],[.75,.5,.25,0,-.25,-.5,-.75]]
hist=[f for f in sorted((P/'figures/appendix/ground_motion_time_histories').glob('*.png')) if 'thm' not in f.name]
for f,y in zip(hist,ys):raster_axes(f,y,'history',f.stem)
raster_axes(P/'figures/ch4/seq40_part1/ground_motion_12eq_pga_selected_gorkha_component.png',list(np.arange(.8,-.01,-.1)),'pga','ground_motion_12eq_pga')
raster_axes(P/'figures/ch4/part01/ground_motion_11eq_psa.png',[3,2.5,2,1.5,1,.5,0],'spectra','ground_motion_11eq_psa')

# Two explanatory diagrams: same statements and topology, larger Times New Roman text.
fig,ax=plt.subplots(figsize=(W,5.0));fig.subplots_adjust(0,0,1,1);ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
def box(x,y,w,h,text):
    ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle='round,pad=0.008',fc='#f3f5f8',ec='#777777',lw=.7));ax.text(x,y,text,ha='center',va='center',fontsize=12)
def arrow(x1,y1,x2,y2):ax.annotate('',(x2,y2),(x1,y1),arrowprops={'arrowstyle':'->','color':'#666666','lw':.8})
box(.5,.92,.88,.08,'Six-block G+4 hospital structural model')
box(.5,.76,.92,.10,'Four support assumptions:\nfixed, hard, medium, soft');arrow(.5,.87,.5,.82)
for x,t in [(.17,'Modal and\nresponse-spectrum\nRS-X / RS-Y'),(.5,'Foundation settlement\nand gravitational\nmember forces'),(.83,'Ground motions\nand fragility\ncurves')]:
    box(x,.51,.30,.19,t);arrow(.5,.70,x,.615);arrow(x,.405,.5,.315)
box(.5,.25,.94,.12,'Within-block comparison of periods,\ndrifts, forces and fragility')
box(.5,.07,.90,.08,'Results, discussion and conclusions');arrow(.5,.185,.5,.115)
save(fig,'analysis_flowchart','Existing methodology diagram, text and topology preserved','figures/ch3/analysis_flowchart_seq057.pdf')
fig,ax=plt.subplots(figsize=(W,3.4));fig.subplots_adjust(0,0,1,1);ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
ax.text(.25,.88,'Winkler local reaction model',ha='center',fontsize=12)
ax.text(.25,.73,'Rigid footing',ha='center',fontsize=12)
ax.add_patch(Rectangle((.055,.55),.39,.045,fc='#aaaaaa',ec='#555555'))
for x in np.linspace(.08,.42,6):
    xx=[x];yy=[.55]
    for j in range(12):xx.append(x+(.012 if j%2 else -.012));yy.append(.54-j*.012)
    xx.append(x);yy.append(.38);ax.plot(xx,yy,color='#666666',lw=.8)
ax.plot([.04,.46],[.36,.36],color='#777777',lw=.9);ax.text(.25,.24,'Independent vertical springs',ha='center',fontsize=12)
ax.text(.76,.88,'Equivalent 6-DOF restraint',ha='center',fontsize=12)
ax.add_patch(Rectangle((.57,.47),.38,.045,fc='#aaaaaa',ec='#555555'));ax.plot([.55,.97],[.36,.36],color='#777777',lw=.9)
ax.annotate('',(.76,.73),(.76,.52),arrowprops={'arrowstyle':'->','lw':1});ax.text(.79,.70,'Kz',fontsize=12)
ax.annotate('',(.99,.49),(.95,.49),arrowprops={'arrowstyle':'->','lw':1});ax.text(.76,.25,'Kx, Ky',ha='center',fontsize=12)
ax.add_patch(Arc((.60,.58),.12,.21,theta1=90,theta2=300,lw=.8));ax.text(.59,.76,'Kθx, Kθy, Kt',ha='center',fontsize=12)
save(fig,'winkler_gazetas_schematic','Existing Winkler and six-component restraint schematic','figures/ch2/winkler_gazetas_schematic.pdf')

fig,ax=plt.subplots(figsize=(W,.38));fig.subplots_adjust(0,0,1,1);ax.axis('off')
ax.legend([Line2D([],[],color=plt.cm.tab10(j),lw=1.3) for j in range(4)],['IO','LS','CP','C'],ncol=4,loc='center',frameon=False,fontsize=12)
save(fig,'fragility_damage_state_key','Shared legend for the four original damage-state curves')

# Apply only figure paths, exact physical inclusion sizes, and panel identifiers; scientific prose stays unchanged.
for texfile in ['22_literaturereview.tex','23_methodology.tex','24_resultanddiscussion.tex','28_appendices.tex','31_fragility_original_figures_seq064.tex']:
    text=(P/texfile).read_text()
    def repl(m):
        old=m[2]
        if old not in replacements:return m[0]
        new=replacements[old]
        if texfile=='24_resultanddiscussion.tex' and 'fragility_seq057' in old:
            new=new.removesuffix('.pdf')+'_panel.pdf';return '\\includegraphics[width=\\linewidth]{'+new+'}'
        return '\\includegraphics[width=\\textwidth]{'+new+'}'
    text=re.sub(r'\\includegraphics\[([^\]]*)\]\{([^}]+)\}',repl,text)
    text=text.replace('{\\footnotesize Soft support\\par}','{\\fontsize{12}{14}\\selectfont Soft support\\par}').replace('{\\footnotesize Medium support\\par}','{\\fontsize{12}{14}\\selectfont Medium support\\par}').replace('{\\footnotesize Hard support\\par}','{\\fontsize{12}{14}\\selectfont Hard support\\par}').replace('{\\footnotesize Fixed support\\par}','{\\fontsize{12}{14}\\selectfont Fixed support\\par}')
    if texfile=='24_resultanddiscussion.tex':
        anchor='\\caption{X-direction fragility response illustrations for hospital Block 1'
        pos=text.index(anchor)
        if 'includegraphics[width=\\textwidth]{figures/seq067/B1_fragility_all_supports.pdf}' not in text:
            text=text[:pos]+'\\includegraphics[width=\\textwidth]{figures/seq067/B1_fragility_all_supports.pdf}\n'+text[pos:]
        text=text.replace('X-direction fragility response illustrations for hospital Block 1 under fixed, hard-, medium- and soft-support conditions.','X-direction fragility response illustrations for hospital Block 1 under fixed, hard-, medium- and soft-support conditions; the fifth panel overlays all sixteen curves using colour for damage state and line style for support condition.')
        for b in range(2,7):
            anchor=f'\\caption{{X-direction fragility response illustrations for hospital Block {b}'
            start=text.index(anchor);old=text[max(0,start-150):start]
            if 'fragility_damage_state_key.pdf' not in old:
                text=text[:start]+'\\includegraphics[width=\\textwidth]{figures/seq067/fragility_damage_state_key.pdf}\n'+text[start:]
    (P/texfile).write_text(text)

(P/'SEQ067_FIGURE_ASSET_MAP.json').write_text(json.dumps({'release':'LATEX_SEQ067','base':'LATEX_SEQ066','replacement_map':replacements,'figures':records,'cad_annotation_hold':'Six embedded raster block plans and one submitted architectural plan retain their original annotation geometry/size pending a faithful technical-drawing redraw; these are explicitly excluded from the chart font PASS.'},indent=2))
print('Final assets',len(records))
