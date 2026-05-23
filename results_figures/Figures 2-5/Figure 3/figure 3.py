import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import TwoSlopeNorm

# ---- Global style (Nature-like) ----
plt.rcParams.update({
    'font.family': 'Arial',          # Nature journals prefer sans-serif (e.g. Arial)
    'font.size': 9,                  # Slightly smaller, compact
    'axes.unicode_minus': False,
    'axes.linewidth': 0.5,           # Thin axes lines
    'xtick.major.width': 0.4,
    'ytick.major.width': 0.4,
})

# 文件路径
file_path = 'clubresults0322.xlsx'
sheet_name = 'C_CO2'

# 读取数据
raw_df = pd.read_excel(
    file_path,
    sheet_name=sheet_name,
    index_col=0,
    usecols="A:K",
    nrows=7
)
raw_df = raw_df.round(2)
df = raw_df.copy()

# ✅ 重新排序情景顺序、列顺序（国家）
desired_columns = ['EU', 'ANNEX I', 'CAN', 'USA', 'CHN', 'IND', 'MEX', 'ROW', 'OILEX', 'RUS']
df = df[desired_columns]
desired_order = ['CLUB-0', 'CLUB-0-R', 'CLUB-1', 'CLUB-1-R', 'CLUB-2', 'CLUB-2-R', 'CLUB-G']
df = df.reindex(desired_order)

# 国家颜色设置（用于 x 轴标签）
column_colors = {
    'EU': '#393d3f',
    'ANNEX I': '#1a659e',
    'CAN': '#1a659e',
    'USA': '#1a659e',
    'MEX': '#2c6e49',
    'CHN': '#2c6e49',
    'IND': '#2c6e49',
    'ROW': '#8d0801',
    'RUS': '#8d0801',
    'OILEX': '#8d0801'
}
col_colors = [column_colors.get(col, 'black') for col in df.columns]

# ---- Colour normalisation: symmetric around zero (for changes) ----
vmin = df.min().min()
vmax = df.max().max()
lim = max(abs(vmin), abs(vmax))
norm = TwoSlopeNorm(vmin=-lim, vcenter=0, vmax=lim)

# 绘图
fig, ax = plt.subplots(figsize=(5.5, 3.8))  # Compact, journal-style size

heatmap = sns.heatmap(
    df,
    annot=False,
    fmt=".2f",
    cmap='RdYlGn_r',          # Diverging, works for +/- changes
    norm=norm,
    linewidths=0.3,       # thin grid lines
    linecolor=(1, 1, 1, 0.35),  # semi-transparent white lines (RGBA)
    cbar=False,
    square=True,
    mask=df.isnull()
)

# 手动添加 colorbar（放在左边，略短一些）
sm = plt.cm.ScalarMappable(cmap='RdYlGn_r', norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, fraction=0.04, pad=0.13, location='left', shrink=0.8)
cbar.set_label(
    r"ΔCO$_2$ (%) vs baseline",
    fontsize=9
)
cbar.ax.tick_params(labelsize=8, length=2.5, width=0.3)
# 让刻度和标签都在左侧
cbar.ax.yaxis.set_ticks_position('left')
cbar.ax.yaxis.set_label_position('left')

# 横着写情景名（黑色）
ax.set_yticklabels(df.index, rotation=0, fontsize=8, color='black')

# 国家列标签（全部黑色 + 旋转一点）
ax.set_xticklabels(df.columns, rotation=45, ha='right', fontsize=8)
for ticklabel in ax.get_xticklabels():
    ticklabel.set_color('black')

# 去掉刻度线，画面更干净
ax.tick_params(axis='both', which='both', length=0)

# 手动标注数字（更小的字体，更轻）
for i in range(df.shape[0]):
    for j in range(df.shape[1]):
        value = df.iloc[i, j]
        if pd.isnull(value):
            continue
        # 一位小数，更像期刊图
        display_text = f"{value:.1f}"

        # 根据背景深浅调整字体颜色
        text_color = 'white' if abs(value) > 0.75 * lim else 'black'

        ax.text(
            j + 0.5,
            i + 0.5,
            display_text,
            ha='center',
            va='center',
            fontsize=8,
            color=text_color
        )

# 左侧对齐标题（Nature 常见风格）
ax.set_title(
    'Change in CO$_2$ emissions relative to the baseline scenario (%)',
    loc='left',
    fontsize=9,
    fontweight='bold',
    pad=8
)

# 去掉外框线，让图更干净
for spine in ax.spines.values():
    spine.set_visible(False)

# 美化
ax.set_xlabel('')
ax.set_ylabel('')

plt.tight_layout()

# 高分辨率输出，适合投稿
plt.savefig('heatmap_co2_2040.tiff', dpi=600, bbox_inches='tight')
plt.savefig('heatmap_co2_2040.pdf', bbox_inches='tight')
plt.show()
