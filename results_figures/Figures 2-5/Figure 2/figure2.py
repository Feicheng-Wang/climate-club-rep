import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.lines import Line2D

# ── Global style ──────────────────────────────────────────────────────────────
mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 7,
    'axes.labelsize': 7,
    'axes.titlesize': 7,
    'xtick.labelsize': 6.5,
    'ytick.labelsize': 6.5,
    'legend.fontsize': 6.2,
    'axes.unicode_minus': False,
    'axes.linewidth': 0.6,
    'xtick.major.width': 0.6,
    'ytick.major.width': 0.6,
    'xtick.major.size': 2.5,
    'ytick.major.size': 2.5,
    'xtick.direction': 'out',
    'ytick.direction': 'out',
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
})

MM = 1 / 25.4
file_path = 'clubresults0322.xlsx'

# Three club tiers, each with a base color; retaliation = dashed, darker shade
SCENARIOS = {
    'CLUB-0':    dict(color='#0072B2', ls='-',  lw=1.5, label='CLUB-0 (EU only)'),
    'CLUB-1':    dict(color='#009E73', ls='-',  lw=1.5, label='CLUB-1 (Leaders)'),
    'CLUB-2':    dict(color='#D55E00', ls='-',  lw=1.5, label='CLUB-2 (+ Swing states)'),
    'CLUB-0-R':  dict(color='#0072B2', ls='--', lw=1.1, label='CLUB-0-R'),
    'CLUB-1-R':  dict(color='#009E73', ls='--', lw=1.1, label='CLUB-1-R'),
    'CLUB-2-R':  dict(color='#D55E00', ls='--', lw=1.1, label='CLUB-2-R'),
}

# Endpoint values at 2040 for annotation boxes
ENDPOINT_GDP = {
    'CLUB-0':   '+0.04%', 'CLUB-1':   '−0.05%', 'CLUB-2':   '−0.63%',
    'CLUB-G':   '−0.69%',
    'CLUB-0-R': '−0.02%', 'CLUB-1-R': '−0.24%', 'CLUB-2-R': '−0.87%',
}
ENDPOINT_CO2 = {
    'CLUB-0':   '−0.3%',  'CLUB-1':   '−1.4%',  'CLUB-2':   '−13.5%',
    'CLUB-G':   '−17.6%',
    'CLUB-0-R': '−0.3%',  'CLUB-1-R': '−1.7%',  'CLUB-2-R': '−13.9%',
}

LABEL_Y_GDP = {
    'CLUB-0': 0.04,
    'CLUB-0-R': -0.02,
    'CLUB-1': -0.09,
    'CLUB-1-R': -0.25,
    'CLUB-2': -0.64,
    'CLUB-2-R': -0.87,
    'CLUB-G': -0.74,
}

LABEL_Y_CO2 = {
    'CLUB-0': 0.50,
    'CLUB-0-R': -0.38,
    'CLUB-1': -1.20,
    'CLUB-1-R': -1.85,
    'CLUB-2': -13.20,
    'CLUB-2-R': -14.10,
    'CLUB-G': -17.55,
}

def load_sheet(sheet):
    years_row = pd.read_excel(file_path, sheet_name=sheet, header=None,
                              usecols='B:Y', nrows=1)
    years = years_row.iloc[0].tolist()
    df = pd.read_excel(file_path, sheet_name=sheet, header=None,
                       usecols='A:Y', nrows=8)
    return years, df

def plot_panel(ax, sheet, ylabel, endpoint_labels, label_y, add_clubG=True):
    years, df = load_sheet(sheet)

    for i in range(1, len(df)):
        scen = str(df.iloc[i, 0])
        vals = df.iloc[i, 1:].values.astype(float)
        if scen not in SCENARIOS:
            continue

        s = SCENARIOS[scen]
        ax.plot(years, vals, color=s['color'], ls=s['ls'], lw=s['lw'], zorder=3)
        end_text = endpoint_labels.get(scen, '')
        label_text = f"{scen} ({end_text})" if end_text else scen
        y_text = label_y.get(scen, vals[-1])
        ax.text(2040.42, y_text, label_text,
                fontsize=5.4, va='center', ha='left', color=s['color'])

    # Add CLUB-G as a benchmark line
    if add_clubG:
        yrs2, df2 = load_sheet(sheet)
        for i in range(1, len(df2)):
            if str(df2.iloc[i, 0]) == 'CLUB-G':
                vals_g = df2.iloc[i, 1:].values.astype(float)
                ax.plot(yrs2, vals_g, color='#7A7A7A', ls=':', lw=1.1, zorder=2)
                end_text = endpoint_labels.get('CLUB-G', '')
                label_text = f"CLUB-G ({end_text})" if end_text else 'CLUB-G'
                y_text = label_y.get('CLUB-G', vals_g[-1])
                ax.text(2040.42, y_text, label_text,
                        fontsize=5.4, va='center', ha='left', color='#666666')

    ax.set_xlim(2018, 2047.2)
    ax.set_xticks(range(2020, 2041, 5))
    ax.set_xlabel('Year', fontsize=7)
    ax.set_ylabel(ylabel, fontsize=7)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(0.6)
    ax.spines['bottom'].set_linewidth(0.6)
    ax.tick_params(axis='both', which='both', direction='out', length=2.5, width=0.6, pad=2)
    ax.grid(False)

    # In-panel note
    box_txt = (
        "Membership scenarios\n"
        "CLUB-0: EU only\n"
        "CLUB-1: + Annex I, CAN, USA\n"
        "CLUB-2: + CHN, IND, MEX\n"
        "CLUB-G: Global benchmark\n"
        "-R: Retaliation"
    )
    ax.text(0.03, 0.25, box_txt, transform=ax.transAxes,
            fontsize=5.2, va='top', ha='left',
            bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='none', alpha=0.92))

# ── Build figure ──────────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2,
                                figsize=(180 * MM, 68 * MM),
                                constrained_layout=False)
fig.subplots_adjust(left=0.08, right=0.86, wspace=0.28, bottom=0.22, top=0.92)

# Panel labels
for ax, lbl in zip([ax1, ax2], ['a', 'b']):
    ax.text(-0.10, 1.02, lbl, transform=ax.transAxes,
            fontsize=8, fontweight='bold', va='bottom', ha='left')

plot_panel(ax1, 'GLOBAL GDP',  'Global GDP change (%)',  ENDPOINT_GDP, LABEL_Y_GDP)
plot_panel(ax2, 'GLOBAL CO2', 'Global CO2 change (%)', ENDPOINT_CO2, LABEL_Y_CO2)

# ── Shared legend (top of figure) ────────────────────────────────────────────
legend_elements = [
    Line2D([0], [0], color='#0072B2', lw=1.5, ls='-',  label='CLUB-0'),
    Line2D([0], [0], color='#009E73', lw=1.5, ls='-',  label='CLUB-1'),
    Line2D([0], [0], color='#D55E00', lw=1.5, ls='-',  label='CLUB-2'),
    Line2D([0], [0], color='#7A7A7A', lw=1.1, ls=':',  label='CLUB-G'),
    Line2D([0], [0], color='black',   lw=1.1, ls='--', label='Retaliation case (-R)'),
]
fig.legend(handles=legend_elements, loc='lower center',
           ncol=5, frameon=False,
           bbox_to_anchor=(0.50, 0.04),
           handlelength=2.4, columnspacing=1.2, handletextpad=0.5)

plt.savefig('Figure2.pdf', bbox_inches='tight', dpi=600)
print("Figure 2 saved in PDF and PNG formats.")
