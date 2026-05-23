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
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12  # Panel titles
plt.rcParams['axes.labelsize'] = 10  # X and Y labels
plt.rcParams['xtick.labelsize'] = 7   # X-axis tick labels
plt.rcParams['ytick.labelsize'] = 7   # Y-axis tick labels
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
        cmap='PuOr',
        center=0,
        linewidths=0.5,
        ax=ax,
        cbar=False,
        vmin=vmin,
        vmax=vmax,
    )

    # --- Manual annotation so numbers never disappear ---
    rows, cols = df.shape
    for i in range(rows):
        for j in range(cols):
            value = df.iloc[i, j]
            if pd.isna(value):
                continue
            ax.text(
                j + 0.5, i + 0.5,
                f"{value:.1f}",
                ha='center', va='center',
                fontsize=7,
                color='black',
                zorder=10
            )
        
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    ax.set_xlabel('Importer', labelpad=5)
    ax.set_ylabel('Exporter', labelpad=5)
    ax.set_title(title)

    # Return the underlying QuadMesh (the first collection), which is a ScalarMappable
    return ax.collections[0]

# --- 4. Figure Creation and Plotting ---

# Create a 4x2 grid
fig, axes = plt.subplots(4, 2, figsize=(12, 16))
axes_flat = axes.flatten()

# List for panel labels (a, b, c...)
panel_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
mappable = None  # To store the last mappable object for the colorbar

# Plot the first 6 heatmaps
for i in range(6):
    ax = axes_flat[i]
    draw_heatmap(ax, data_frames[i], files_titles[i][1])
    
    # Add panel label
    ax.text(-0.1, 1.05, panel_labels[i], transform=ax.transAxes,
            size=16, weight='bold')

# Plot the 7th (CLUB-G) heatmap
ax_clubg = axes_flat[6]
mappable = draw_heatmap(ax_clubg, data_frames[6], 'CLUB-G')

# Add panel label for the 7th plot
ax_clubg.text(-0.1, 1.05, panel_labels[6], transform=ax_clubg.transAxes,
             size=16, weight='bold')

# --- 5. Colorbar and Final Layout ---

# Turn off the 8th (unused) subplot
axes_flat[7].axis('off')

# Use the 8th subplot's space to draw the colorbar
# This is a clean way to place the colorbar inside the grid
divider = make_axes_locatable(axes_flat[7])
# Adjust size and padding for the colorbar axis
cax = divider.append_axes("left", size="5%", pad=0.2)

# Add the colorbar using the mappable from the last plot
cb = fig.colorbar(mappable, cax=cax, orientation='vertical')
cb.set_label("Change in trade flows (%)\nfor energy-intensive products", fontsize=11)

# --- 6. Final Layout Adjustment and Export ---

# Use tight_layout to clean up spacing, adding padding
plt.tight_layout(pad=1.5, h_pad=2.0)

# Save as SVG (vector format) with a high DPI
# Note: DPI is technically for raster, but some viewers use it
plt.savefig('tradeflow_7clubs_refined.svg', format='svg', bbox_inches='tight', dpi=300)

print("Refined figure 'tradeflow_7clubs_refined.svg' saved.")
plt.show() # Uncomment to display the plot