import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.font_manager import FontProperties
from mpl_toolkits.axes_grid1 import make_axes_locatable

# --- 1. Global Plotting Settings (Nature-style) ---
# Use Arial font, a standard for many publications
plt.rcParams['font.family'] = 'Arial'
# Set base font sizes. Adjust as needed.
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 12  # Panel titles
plt.rcParams['axes.labelsize'] = 12  # X and Y labels
plt.rcParams['xtick.labelsize'] = 10   # X-axis tick labels
plt.rcParams['ytick.labelsize'] = 10  # Y-axis tick labels
# Ensure correct rendering of minus signs
plt.rcParams['axes.unicode_minus'] = False


# --- 2. Data Loading and Preparation ---

# File names and titles
files_titles = [
    ('club1.xls', 'CLUB-0'),
    ('club1rt.xls', 'CLUB-0-R'),
    ('club4.xls', 'CLUB-1'),
    ('club4rt.xls', 'CLUB-1-R'),
    ('club7.xls', 'CLUB-2'),
    ('club7rt.xls', 'CLUB-2-R'),
    ('club10.xls', 'CLUB-G')
]

# Country order
order = ['EU', 'ANNEX I', 'CAN', 'USA', 'CHN', 'IND', 'MEX', 'ROW', 'OILEX', 'RUS']

# Pre-read all data to calculate global min/max for a unified color scale
vmin, vmax = float('inf'), float('-inf')
data_frames = []

for fname, _ in files_titles:
    df_tmp = pd.read_excel(fname, sheet_name='CBA_flow_com', index_col=0)
    df_tmp.replace('Undf', np.nan, inplace=True)
    df_tmp = df_tmp.astype(float)
    df_tmp = df_tmp.loc[order, order]
    data_frames.append(df_tmp)
    # Update global min/max
    vmin = min(vmin, df_tmp.min().min())
    vmax = max(vmax, df_tmp.max().max())

# --- 3. Refined Plotting Function ---

def draw_heatmap(ax, df, title):
    """
    Draws a single heatmap on the provided axes.
    Font sizes are controlled by plt.rcParams.
    Returns the QuadMesh (ScalarMappable) for colorbar creation.
    """
    hm = sns.heatmap(
        df,
        annot=False,          # turn off seaborn annot to avoid disappearing text
        cmap='RdBu',
        center=0,
        linewidths=0.5,
        ax=ax,
        cbar=False,
        vmin=vmin,
        vmax=vmax,
    )

    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    ax.set_xlabel('Importer', labelpad=0)
    ax.set_ylabel('Exporter', labelpad=0)
    ax.set_title(title)

    # Return the underlying QuadMesh (the first collection), which is a ScalarMappable
    return ax.collections[0]

# --- 4. Figure Creation and Plotting ---

# Create a 2x4 grid
fig, axes = plt.subplots(2, 4, figsize=(14, 7))
axes_flat = axes.flatten()

# List for panel labels (a, b, c...)
panel_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
mappable = None  # To store the last mappable object for the colorbar

# Fill the first 7 panels: positions 0–6 in a 2×4 grid
for i in range(7):
    ax = axes_flat[i]
    mappable = draw_heatmap(ax, data_frames[i], files_titles[i][1])
    ax.text(-0.1, 1.1, panel_labels[i], transform=ax.transAxes,
            size=12, weight='bold')

# --- 5. Colorbar and Final Layout ---

# Turn off the 8th (unused) subplot
axes_flat[7].axis('off')

# Use the 8th subplot's space to draw the colorbar
# This is a clean way to place the colorbar inside the grid
divider = make_axes_locatable(axes_flat[7])
cax = divider.append_axes("left", size="10%", pad=0.4)
cb = fig.colorbar(mappable, cax=cax, orientation='vertical')
cb.set_label("Change in trade flows of\n energy-intensive products (%)", fontsize=12)

# --- 6. Final Layout Adjustment and Export ---

# Use tight_layout to clean up spacing, adding padding
plt.tight_layout(pad=1.0, h_pad=1.0, w_pad=1.2)

# Save as SVG (vector format) with a high DPI
# Note: DPI is technically for raster, but some viewers use it
plt.savefig('Figure 5.svg', format='svg', bbox_inches='tight', dpi=1000)

print("Refined figure 'Figure 5.svg' saved.")
plt.show() # Uncomment to display the plot