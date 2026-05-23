import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ==== Style ====
BASE_FONT_FAMILY = 'Arial'
mpl.rcParams.update({
    'font.family': BASE_FONT_FAMILY,
    'font.size': 10,
    'axes.labelsize': 9,
    'axes.titlesize': 9,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 10,
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

# ==== Data ====
file_path = 'CPII.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')

df = df[['region', 'ECON_z', 'ECO_z', 'POL_z']].copy()

# Weights: E=50%, P=30%, Eco=20% 
df['ECON'] = df['ECON_z'] * 0.5
df['POL']  = df['POL_z']  * 0.3    
df['ECO']  = df['ECO_z']  * 0.2   
df['Total'] = df['ECON'] + df['POL'] + df['ECO']

# Region names
region_labels = {
    'CAN': 'Canada', 'CHN': 'China', 'EU': 'EU', 'IND': 'India',
    'MEX': 'Mexico', 'RUS': 'Russia', 'ANNEX I': 'Rest of Annex I',
    'USA': 'United States', 'OILEX': 'Oil exporters', 'ROW': 'Rest of the World'
}
df['region_label'] = df['region'].map(region_labels)
df_sorted = df.sort_values(by='Total', ascending=True)

regions = df_sorted['region_label']
econ_vals = df_sorted['ECON']
pol_vals  = df_sorted['POL']
eco_vals  = df_sorted['ECO']

# ==== Figure 1 ====
fig_width_mm = 150
fig_height_mm = 100
fig, ax = plt.subplots(figsize=(fig_width_mm * MM_TO_INCH, fig_height_mm * MM_TO_INCH))

ax.barh(regions, econ_vals, color=COLOR_PALETTE['ECON'],
        label='Economy (50%)', height=0.5)
ax.barh(regions, pol_vals, left=econ_vals, color=COLOR_PALETTE['POL'],
        label='Politics (30%)', height=0.5)
ax.barh(regions, eco_vals, left=econ_vals + pol_vals, color=COLOR_PALETTE['ECO'],
        label='Climate (20%)', height=0.5)

# Jenks threshold lines
ax.axvline(x=0.562, color='grey', linestyle=':', linewidth=0.8, alpha=0.7)
ax.axvline(x=1.626, color='grey', linestyle=':', linewidth=0.8, alpha=0.7)
ax.text(0.5, 10.3, 'Opponents | Swing', fontsize=9, ha='center', color='grey')
ax.text(1.66, 10.3, 'Swing | Leaders', fontsize=9, ha='center', color='grey')

ax.legend(
    loc='lower right',
    prop=fm.FontProperties(family=BASE_FONT_FAMILY, size=10),
    frameon=False,
    ncol=1
)

ax.set_xlabel('Carbon Pricing Incentive Index',
              fontproperties=fm.FontProperties(family=BASE_FONT_FAMILY, size=10))
ax.set_ylabel('Regions',
              fontproperties=fm.FontProperties(family=BASE_FONT_FAMILY, size=10))

for spine in ax.spines.values():
    spine.set_linewidth(0.5)
ax.tick_params(width=0.5, length=2)

plt.tight_layout()

plt.savefig('gcpi_stacked_horizontalbar.pdf', dpi=1000, bbox_inches='tight')
plt.savefig('gcpi_stacked_horizontalbar.svg', dpi=350, bbox_inches='tight')
plt.savefig('gcpi_stacked_horizontalbar.png', dpi=350, bbox_inches='tight')

plt.show()

# Print verification
print("\nVerification — CPII scores (should match Appendix A Table A3):")
for _, row in df_sorted.iterrows():
    total = row['Total']
    cat = "LEADER" if total > 1.626 else ("SWING" if total > 0.562 else "OPPONENT")
    print(f"  {row['region_label']:20s}  CPII = {total:.3f}  [{cat}]")
