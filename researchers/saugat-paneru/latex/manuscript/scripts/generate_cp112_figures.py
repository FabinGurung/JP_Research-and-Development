from pathlib import Path
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / 'figures' / 'ch4' / 'cp112_generated'
OUT.mkdir(parents=True, exist_ok=True)

# Governed Saugat sources used to freeze this CP112 candidate:
# - Max Storey Drift.xlsx (Drive 13c68Hs3SwyUF3V7tk5yq-VgGlf3b4QId)
# - CP111 admitted first-peak pushover summary
# - CP111 / per-shape performance-point workbooks
# - Centre of Mass and Rigidity.xlsx (Drive 1z46jmALMByZ5lpOk7g3F_z4zH0ZxOOkP)
# - SAUGAT_DISCUSSION_ANALYSIS__CURRENT geometry/GII register
# No cross-researcher values are used.

models = ['Regular','L','L1','L2','T','U','Non-Parallel']
gii = [0.00,16.67,33.33,33.33,33.33,16.67,22.22]
max_drift = [0.004784,0.004758,0.004570,0.004025,0.004618,0.004954,0.004041]
cmcr = [0.398,0.581,0.640,1.186,0.475,0.424,1.237]
peak_push = [1836.338,1800.120,1606.250,1804.152,1640.715,1882.070,1827.694]
pp_shear = [456.253,407.295,340.753,370.935,343.488,435.084,399.636]
pp_disp = [26.053,25.900,24.592,21.171,24.802,27.072,21.328]

drift_profiles = {
 'Regular': ([0.003211,0.004784,0.003606,0.002691],[0.002953,0.004414,0.003410,0.002310]),
 'L': ([0.003160,0.004758,0.003630,0.002703],[0.002919,0.004341,0.003363,0.002292]),
 'L1': ([0.002996,0.004570,0.003550,0.002682],[0.002802,0.004134,0.003264,0.002263]),
 'L2': ([0.002711,0.004025,0.003178,0.002436],[0.002422,0.003479,0.002610,0.001828]),
 'T': ([0.003015,0.004597,0.003559,0.002664],[0.002901,0.004618,0.003804,0.002596]),
 'U': ([0.003219,0.004954,0.003844,0.002913],[0.002843,0.004288,0.003342,0.002296]),
 'Non-Parallel': ([0.002756,0.004041,0.003023,0.002367],[0.002466,0.003527,0.002637,0.001826]),
}

for model,(x,y) in drift_profiles.items():
    fig, ax = plt.subplots(figsize=(5.0,3.1))
    stories = [1,2,3,4]
    ax.plot(x, stories, marker='o', label='X')
    ax.plot(y, stories, marker='s', linestyle='--', label='Y')
    ax.set_xlim(0,0.006)
    ax.set_xticks([0,0.002,0.004,0.006])
    ax.set_yticks(stories, ['Story 1','Story 2','Story 3','Story 4'])
    ax.set_xlabel('ULS drift ratio')
    ax.set_title(model)
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    fn=model.lower().replace('-','_').replace(' ','_')
    fig.savefig(OUT/f'drift_{fn}.png',dpi=220,bbox_inches='tight')
    plt.close(fig)

def categorical(values, ylabel, title, filename):
    fig, ax = plt.subplots(figsize=(7.0,3.4))
    ax.plot(models, values, marker='o')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, axis='y')
    ax.tick_params(axis='x', rotation=35)
    fig.tight_layout()
    fig.savefig(OUT/filename,dpi=220,bbox_inches='tight')
    plt.close(fig)

categorical(pp_shear,'PP base shear (kN)','Performance-point base shear','pp_base_shear.png')
categorical(pp_disp,'PP roof displacement (mm)','Performance-point displacement','pp_displacement.png')

def scatter(values, ylabel, title, filename):
    fig, ax = plt.subplots(figsize=(5.3,3.6))
    ax.scatter(gii, values)
    for x,y,n in zip(gii,values,models):
        ax.annotate(n,(x,y),xytext=(4,4),textcoords='offset points',fontsize=8)
    ax.set_xlabel('GII (%)')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(OUT/filename,dpi=220,bbox_inches='tight')
    plt.close(fig)

scatter(max_drift,'ULS drift ratio','GII vs maximum ULS drift','gii_max_drift.png')
scatter(cmcr,'CM–CR separation (m)','GII vs maximum CM–CR separation','gii_cmcr.png')
scatter(peak_push,'Peak base shear (kN)','GII vs peak pushover base shear','gii_peak_pushover.png')
scatter(pp_disp,'PP roof displacement (mm)','GII vs performance-point displacement','gii_pp_displacement.png')
scatter(pp_shear,'PP base shear (kN)','GII vs performance-point base shear','gii_pp_shear.png')
