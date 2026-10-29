import pandas as pd, numpy as np, os, shutil, json
import matplotlib.pyplot as plt
root=os.path.dirname(os.path.abspath(__file__))
src=os.path.join(root,'source_inputs_seq39','gorkha.xlsx')
outdir=os.path.join(root,'figures','ch4','seq39')
appdir=os.path.join(root,'figures','appendix','ground_motion_time_histories')
os.makedirs(outdir,exist_ok=True); os.makedirs(appdir,exist_ok=True)
raw=pd.read_excel(src,sheet_name='THM1505120705',header=None)
pairs=[]
for c in range(raw.shape[1]-1):
    if str(raw.iloc[0,c]).startswith('Time') and 'Acceleration' in str(raw.iloc[0,c+1]):
        t=pd.to_numeric(raw.iloc[1:,c],errors='coerce'); a=pd.to_numeric(raw.iloc[1:,c+1],errors='coerce')
        m=t.notna() & a.notna(); pairs.append((t[m].to_numpy(float),a[m].to_numpy(float),c))
fig,axes=plt.subplots(3,1,figsize=(12,8),sharex=True)
for i,(t,a,c) in enumerate(pairs,1):
    axes[i-1].plot(t,a,linewidth=0.7)
    axes[i-1].set_ylabel(f'Ch. {i}\n(cm/s$^2$)')
    axes[i-1].grid(True,alpha=0.25)
    pga=np.max(np.abs(a))/981.0
    axes[i-1].text(0.99,0.88,f'PGA = {pga:.4f} g',transform=axes[i-1].transAxes,ha='right',va='top',fontsize=9)
axes[-1].set_xlabel('Time (s)')
fig.suptitle('2015 Gorkha Earthquake - THM Station Workbook Acceleration Channels')
fig.tight_layout(rect=[0,0,1,0.96])
gf=os.path.join(outdir,'gorkha_thm_3channel_acceleration_time_history.png')
fig.savefig(gf,dpi=220,bbox_inches='tight'); plt.close(fig)
shutil.copy2(gf,os.path.join(appdir,'12_gorkha_thm__acceleration_time_history.png'))
labels=['Chi-Chi','Friuli','Hollister','Imperial Valley','Kobe','Kocaeli','Landers','Loma Prieta','Northridge','San Fernando','Trinidad','Gorkha (THM)']
pgas=[0.3610,0.3513,0.1948,0.3152,0.3447,0.3490,0.7803,0.3674,0.5683,0.02576,0.1936,max(np.max(np.abs(a))/981.0 for _,a,_ in pairs)]
fig,ax=plt.subplots(figsize=(14,8)); ax.bar(range(len(labels)),pgas); ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels,rotation=50,ha='right'); ax.set_ylabel('PGA (g)'); ax.set_xlabel('Ground-motion record label'); ax.set_title('PGA of the 12 Supplied Records with Explicit Acceleration and Time Units'); ax.grid(axis='y',alpha=0.25); fig.tight_layout()
pf=os.path.join(outdir,'ground_motion_12eq_pga_with_gorkha_thm.png'); fig.savefig(pf,dpi=220,bbox_inches='tight'); plt.close(fig)
summary={'source':'gorkha.xlsx','sheet':'THM1505120705','channels':[], 'reported_table_pga_g':float(max(np.max(np.abs(a))/981.0 for _,a,_ in pairs)), 'reported_table_dt_s':0.01, 'note':'Emergency submission patch uses maximum absolute PGA across the three explicitly supplied THM acceleration channels; orientation labels are not inferred from the workbook.'}
for i,(t,a,c) in enumerate(pairs,1): summary['channels'].append({'channel':i,'source_columns':[int(c),int(c+1)],'n':int(len(t)),'dt_s':float(t[1]-t[0]),'pga_g':float(np.max(np.abs(a))/981.0),'max_cm_s2':float(np.max(a)),'min_cm_s2':float(np.min(a))})
with open(os.path.join(root,'source_inputs_seq39','gorkha_thm_extraction_summary.json'),'w') as f: json.dump(summary,f,indent=2)
print(json.dumps(summary,indent=2))
