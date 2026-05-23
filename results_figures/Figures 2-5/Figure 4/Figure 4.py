import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors  # <-- MODIFIED: Import the full colors module

# --- Removed custom ThreeQuarterNormalize class ---
# We will build a custom colormap instead.

# Set global plotting parameters
plt.rcParams.update({
    'font.family': 'Arial',      # Nature-style sans-serif
    'font.size': 9,
    'axes.unicode_minus': False,
    'axes.linewidth': 0.5,
    'xtick.major.width': 0.3,
    'ytick.major.width': 0.3,
})

# File paths
file_path = 'clubresults0322.xlsx'
sheet_name = 'C_GDP'

# Read and process data
try:
    df = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        index_col=0,
        usecols="A:K",
        nrows=7
    )
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    # Create dummy data for demonstration if file is missing
    indices = ['CLUB-0', 'CLUB-0-R', 'CLUB-1', 'CLUB-1-R', 'CLUB-2', 'CLUB-2-R', 'CLUB-G']
    columns = ['EU', 'ANNEX I', 'CAN', 'USA', 'CHN', 'IND', 'MEX', 'ROW', 'OILEX', 'RUS']
    data = np.random.uniform(-3, 1, size=(len(indices), len(columns)))
    df = pd.DataFrame(data, index=indices, columns=columns)
    print("Using dummy data for demonstration.")


# Retain two decimal places
df = df.round(2)

# Reorder columns (countries)
desired_columns = ['EU', 'ANNEX I', 'CAN', 'USA', 'CHN', 'IND', 'MEX', 'ROW', 'OILEX', 'RUS']
# Filter to only columns that exist in the dataframe to avoid errors
existing_columns = [col for col in desired_columns if col in df.columns]
df = df[existing_columns]

# Reorder rows (scenarios)
desired_order = ['CLUB-0', 'CLUB-0-R', 'CLUB-1', 'CLUB-1-R', 'CLUB-2', 'CLUB-2-R', 'CLUB-G']
# Filter to only indices that exist in the dataframe to avoid errors
existing_indices = [idx for idx in desired_order if idx in df.index]
df = df.reindex(existing_indices)

# ---- Colour normalisation: min = -3, max = 1 ----
vmin, vmax = -3, 1
# Threshold for text color. Values with magnitude > 0.75 will be on darker colors
lim = 1

# <-- MODIFIED: Create custom colormap with white at 0.75 position -->
# 1. Define the colormap stops: (position, color)
# We'll use the original script's colors (Green for low, Red for high)
colors = [
    (0.0, '#d7263d'),   # 0.0 position (maps to vmin = -3)
    (0.75, 'white'),  # 0.75 position (physical 75% mark)
    (1.0, '#247ba0')      # 1.0 position (maps to vmax = 1)
]

# 2. Create the colormap object
cmap_name = mcolors.LinearSegmentedColormap.from_list('my_custom_map', colors)

# 3. Use a standard Linear Normalization
# This maps vmin -> 0.0 and vmax -> 1.0
norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

# Plotting
fig, ax = plt.subplots(figsize=(5.5, 3.8))

# (The 'Define the colormap' section from the old script is no longer needed)

heatmap = sns.heatmap(
    df,
    annot=False,          # We will add annotations manually for color control
    fmt=".2f",            # Format string (though not used by annot=False)
    cmap=cmap_name,       # <-- MODIFIED: Use our new custom map
    norm=norm,            # <-- MODIFIED: Use our new linear norm
    linewidths=0.3,
    linecolor=(1, 1, 1, 0.35),
    cbar=False,           # We will add the colorbar manually
    square=True,
    mask=df.isnull()
)

# Manually add colorbar (left side, slightly shorter)
sm = plt.cm.ScalarMappable(cmap=cmap_name, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, fraction=0.04, pad=0.13, location='left', shrink=0.8)
cbar.set_label(
    r"ΔGDP (%) vs baseline",
    fontsize=9
)
cbar.ax.tick_params(labelsize=7, length=2.5, width=0.2)
cbar.ax.yaxis.set_ticks_position('left')
cbar.ax.yaxis.set_label_position('left')

# Set scenario names (y-axis)
ax.set_yticklabels(df.index, rotation=0, fontsize=8, color='black')

# Set country names (x-axis)
ax.set_xticklabels(df.columns, rotation=45, ha='right', fontsize=8)
for ticklabel in ax.get_xticklabels():
    ticklabel.set_color('black')

# Clean up ticks
ax.tick_params(axis='both', which='both', length=0)

# Manually add annotations with custom text color
for i in range(df.shape[0]):
    for j in range(df.shape[1]):
        value = df.iloc[i, j]
        if pd.isnull(value):
            continue
        display_text = f"{value:.1f}"
        text_color = 'white' if abs(value) > 0.75 * lim else 'black'

        ax.text(
            j + 0.5,
            i + 0.5,
            display_text,
            ha='center',
            va='center',
            fontsize=7,
            color=text_color
        )

# Add left-aligned title
ax.set_title(
    'Change in global GDP relative to the baseline scenario (%)',
    loc='left',
    fontsize=9,
    fontweight='bold',
    pad=8
)

# Remove outer frame
for spine in ax.spines.values():
    spine.set_visible(False)

# Remove axis labels
ax.set_xlabel('')
ax.set_ylabel('')

plt.tight_layout()

# Save high-resolution outputs
plt.savefig('heatmap_gdp_2040.tiff', dpi=600, bbox_inches='tight')
plt.savefig('heatmap_gdp_2040.pdf', bbox_inches='tight')

plt.show()