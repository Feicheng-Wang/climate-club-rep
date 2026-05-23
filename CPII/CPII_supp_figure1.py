import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from itertools import combinations

# ==== Jenks natural breaks ====
def jenks_breaks(data, n_classes):
    """Compute Jenks natural breaks for 1-D data."""
    data = sorted(data)
    n = len(data)
    best_gvf = 0
    best_breaks = None
    best_classes = None
    for breaks in combinations(range(1, n), n_classes - 1):
        classes = []
        prev = 0
        for b in breaks:
            classes.append(data[prev:b])
            prev = b
        classes.append(data[prev:])
        # Goodness of Variance Fit
        overall_mean = np.mean(data)
        sdam = sum((v - overall_mean) ** 2 for v in data)
        sdcm = sum((v - np.mean(cls)) ** 2 for cls in classes for v in cls)
        gvf = (sdam - sdcm) / sdam
        if gvf > best_gvf:
            best_gvf = gvf
            best_breaks = breaks
            best_classes = classes
    thresholds = [(data[b - 1] + data[b]) / 2 for b in best_breaks]
    return thresholds, best_gvf


# ==== Style ====
BASE_FONT_FAMILY = 'Arial'
mpl.rcParams.update({
    'font.family': BASE_FONT_FAMILY,
    'font.size': 8,
    'axes.labelsize': 8,
    'axes.titlesize': 9,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 8,
    'axes.unicode_minus': False,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'axes.linewidth': 0.5,
    'xtick.major.width': 0.5,
    'ytick.major.width': 0.5,
    'xtick.major.size': 2.0,
    'ytick.major.size': 2.0,
})

MM_TO_INCH = 1 / 25.4
COLOR_PALETTE = {
    'ECON': '#f1dede',
    'POL':  '#d496a7',
    'ECO':  '#5d576b',
}

def get_plot_font(size=8):
    return fm.FontProperties(family=BASE_FONT_FAMILY, size=size)


# ==== Data ====
file_path = 'CPII.xlsx'
sheet_name = 'Sheet1'
df = pd.read_excel(file_path, sheet_name=sheet_name)
df = df[['region', 'ECON_z', 'ECO_z', 'POL_z']].copy()

# Region names
region_labels = {
    'CAN': 'Canada', 'CHN': 'China', 'EU': 'EU', 'IND': 'India',
    'MEX': 'Mexico', 'RUS': 'Russia', 'ANNEX I': 'Rest of Annex I',
    'USA': 'United States', 'OILEX': 'Oil exporters', 'ROW': 'Rest of World'
}

# Weighting schemes: (ECON weight, POL weight, Vuln weight)
weight_sets = {
    '6:3:1': (0.6, 0.3, 0.1),
    '6:2:2': (0.6, 0.2, 0.2),
    '5:4:1': (0.5, 0.4, 0.1),
    '5:3:2 (baseline)': (0.5, 0.3, 0.2),
    '4:3:3': (0.4, 0.3, 0.3),
    '4:4:2': (0.4, 0.4, 0.2),
}

# ==== Figure: 2x3 panel, max width 180 mm ====
fig, axes = plt.subplots(2, 3, figsize=(180 * MM_TO_INCH, 120 * MM_TO_INCH), sharex=False)
axes = axes.flatten()

for ax, (label, (we, wp, wv)) in zip(axes, weight_sets.items()):
    scenario = df.copy()
    scenario['ECON'] = scenario['ECON_z'] * we
    scenario['POL']  = scenario['POL_z']  * wp
    scenario['ECO']  = scenario['ECO_z']  * wv
    scenario['Total'] = scenario['ECON'] + scenario['POL'] + scenario['ECO']
    scenario['region_label'] = scenario['region'].map(region_labels)
    scenario = scenario.sort_values(by='Total', ascending=True)

    regions   = scenario['region_label']
    econ_vals = scenario['ECON']
    pol_vals  = scenario['POL']
    eco_vals  = scenario['ECO']

    ax.barh(regions, econ_vals, color=COLOR_PALETTE['ECON'],
            label='Economy', height=0.7)
    ax.barh(regions, pol_vals, left=econ_vals, color=COLOR_PALETTE['POL'],
            label='Politics', height=0.7)
    ax.barh(regions, eco_vals, left=econ_vals + pol_vals, color=COLOR_PALETTE['ECO'],
            label='Climate Vulnerability', height=0.7)

    # ---- Jenks threshold lines for this panel ----
    scores = scenario['Total'].tolist()
    thresholds, gvf = jenks_breaks(scores, 3)
    for t in thresholds:
        ax.axvline(x=t, color='#888888', linestyle=':', linewidth=0.8, alpha=0.7)

    ax.set_title(f'Econ:Pol:Vuln = {label}', fontproperties=get_plot_font(size=8))
    ax.set_xlabel('CPII', fontproperties=get_plot_font(size=8))

    for spine in ax.spines.values():
        spine.set_linewidth(0.5)
    ax.tick_params(width=0.5, length=2)

# Consistent x-axis
for ax in axes:
    ax.set_xlim(0, 2.2)
    ax.set_xticks([0, 0.5, 1.0, 1.5, 2.0])

# Shared legend at the bottom
handles, labels_legend = axes[-1].get_legend_handles_labels()
fig.legend(
    handles,
    ['Economy', 'Politics', 'Climate Vulnerability'],
    loc='lower center',
    ncol=3,
    frameon=False,
    prop=get_plot_font(size=9),
    bbox_to_anchor=(0.5, -0.01),
)

plt.tight_layout(rect=[0, 0.06, 1, 0.98])

plt.savefig('gcpi_stackedbar_comparison.pdf', dpi=1000, bbox_inches='tight')
plt.savefig('gcpi_stackedbar_comparison.svg', dpi=350, bbox_inches='tight')
plt.savefig('gcpi_stackedbar_comparison.png', dpi=350, bbox_inches='tight')

plt.show()

# ==== Verification: print Jenks thresholds and group assignments ====
print("\nJenks thresholds and group assignments per weighting scheme:\n")
for label, (we, wp, wv) in weight_sets.items():
    scores_df = df.copy()
    scores_df['CPII'] = scores_df['ECON_z'] * we + scores_df['ECO_z'] * wv + scores_df['POL_z'] * wp
    scores_df['region_label'] = scores_df['region'].map(region_labels)

    score_list = scores_df['CPII'].tolist()
    thresholds, gvf = jenks_breaks(score_list, 3)

    leaders = scores_df[scores_df['CPII'] > thresholds[1]].sort_values('CPII', ascending=False)
    swings  = scores_df[(scores_df['CPII'] > thresholds[0]) & (scores_df['CPII'] <= thresholds[1])].sort_values('CPII', ascending=False)
    opps    = scores_df[scores_df['CPII'] <= thresholds[0]].sort_values('CPII', ascending=False)

    print(f"  {label:22s}  thresholds=[{thresholds[0]:.3f}, {thresholds[1]:.3f}]  GVF={gvf:.3f}")
    print(f"    Leaders:   {', '.join(leaders['region_label'].tolist())}")
    print(f"    Swings:    {', '.join(swings['region_label'].tolist())}")
    print(f"    Opponents: {', '.join(opps['region_label'].tolist())}")
    print()