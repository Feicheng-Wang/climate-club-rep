import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd

# 1. Create Sample Data
# (Replace this with your actual 'df')
np.random.seed(42)
data = np.random.rand(10, 10) * 100
df = pd.DataFrame(data)

# 2. Define the Custom Colormap
# We define a list of (position, color) tuples.
# The positions must go from 0.0 to 1.0.
colors = [
    (0.0, 'blue'),    # At the very bottom (0.0), use blue
    (0.25, 'white'),  # At the 1/4 mark (0.25), use white
    (1.0, 'red')      # At the very top (1.0), use red
]

# Create the colormap object
cmap_name = mcolors.LinearSegmentedColormap.from_list('my_custom_map', colors)

# 3. Plot the Heatmap
# IMPORTANT: Use a standard normalization.
# We are *not* using TwoSlopeNorm here.
# We just use the 'norm' your original code was already using.
vmin = df.min().min()
vmax = df.max().max()
norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

plt.figure(figsize=(9, 8))
heatmap = sns.heatmap(
    df,
    annot=True,           # Set to True to see the values
    fmt=".1f",            
    cmap=cmap_name,       # Use our new custom colormap
    norm=norm,            # Use a standard linear normalization
    linewidths=0.3,
    linecolor=(1, 1, 1, 0.35),
    cbar=True,            # Set to True to see the colorbar
    square=True,
    mask=df.isnull()
)

plt.title("Heatmap with Colorbar White at 25% Position")
plt.show()