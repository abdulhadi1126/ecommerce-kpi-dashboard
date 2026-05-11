# ============================================================
#  E-Commerce KPI Dashboard — Python Visualization
#  Author  : Abdul Hadi
#  GitHub  : github.com/abdulhadi1126
#  Tools   : Python, Pandas, Matplotlib, Seaborn, NumPy
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
import warnings
warnings.filterwarnings('ignore')

# ── Color Palette ────────────────────────────────────────────
BG       = '#070b14'
SURFACE  = '#0d1424'
SURFACE2 = '#111c30'
BORDER   = '#1e2d47'
TEXT     = '#e2e8f4'
MUTED    = '#4a6080'
GREEN    = '#00e5a0'
BLUE     = '#2979ff'
YELLOW   = '#ffd000'
PURPLE   = '#b96dff'
RED      = '#ff4560'
ORANGE   = '#ff7043'

PALETTE  = [GREEN, BLUE, YELLOW, PURPLE, RED, ORANGE]

plt.rcParams.update({
    'figure.facecolor':  BG,
    'axes.facecolor':    SURFACE,
    'axes.edgecolor':    BORDER,
    'axes.labelcolor':   MUTED,
    'xtick.color':       MUTED,
    'ytick.color':       MUTED,
    'text.color':        TEXT,
    'grid.color':        SURFACE2,
    'grid.linewidth':    0.6,
    'font.family':       'monospace',
    'axes.spines.top':   False,
    'axes.spines.right': False,
})

# ── Generate Sample Data ─────────────────────────────────────
np.random.seed(42)

# Daily data for 30 days
dates   = pd.date_range('2024-12-01', periods=30, freq='D')
revenue = np.cumsum(np.random.normal(9500, 2000, 30)).clip(5000) + np.linspace(0, 40000, 30)
orders  = (revenue / np.random.uniform(55, 65, 30)).astype(int)
visitors= orders * np.random.randint(20, 35, 30)
aov     = revenue / orders

categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Beauty', 'Food']
cat_rev    = [34, 26, 18, 12, 6, 4]

regions    = ['N. America', 'Europe', 'Asia Pac.', 'Middle East', 'Latam']
reg_rev    = [42, 28, 18, 8, 4]

products   = ['Wireless Headphones', 'Smart Watch X', 'Running Shoes', 'Laptop Stand', 'BT Speaker']
prod_rev   = [48200, 38600, 29400, 22100, 18800]

funnel_stages = ['Visitors\n125,400', 'Product\nViews\n68,200', 'Add to\nCart\n18,900', 'Checkout\n6,820', 'Purchased\n4,821']
funnel_vals   = [125400, 68200, 18900, 6820, 4821]

# ── Figure Setup ─────────────────────────────────────────────
fig = plt.figure(figsize=(22, 16), facecolor=BG)
fig.suptitle(
    'E-COMMERCE KPI DASHBOARD  |  Abdul Hadi  |  Data Analyst & Dashboard Designer',
    fontsize=13, color=TEXT, y=0.98, fontweight='bold', fontfamily='monospace'
)

gs = gridspec.GridSpec(4, 4, figure=fig, hspace=0.55, wspace=0.4,
                       top=0.94, bottom=0.04, left=0.05, right=0.97)

# ── KPI Cards (top row) ──────────────────────────────────────
kpis = [
    ('TOTAL REVENUE',   '$284.6K', '▲ 18.4%', GREEN),
    ('TOTAL ORDERS',    '4,821',   '▲ 12.1%', BLUE),
    ('AVG ORDER VALUE', '$59.04',  '▲ 5.7%',  YELLOW),
    ('CONV. RATE',      '3.84%',   '▼ 0.3%',  PURPLE),
]
for i, (label, val, chg, color) in enumerate(kpis):
    ax = fig.add_subplot(gs[0, i])
    ax.set_facecolor(SURFACE)
    for spine in ax.spines.values():
        spine.set_edgecolor(BORDER)
    ax.set_xticks([]); ax.set_yticks([])

    # top accent bar
    ax.axhline(y=0.92, xmin=0, xmax=1, color=color, linewidth=3,
               transform=ax.transAxes, clip_on=False)

    ax.text(0.08, 0.72, label, transform=ax.transAxes,
            fontsize=7, color=MUTED, fontfamily='monospace')
    ax.text(0.08, 0.38, val, transform=ax.transAxes,
            fontsize=22, color=color, fontweight='bold', fontfamily='monospace')
    chg_color = GREEN if '▲' in chg else RED
    ax.text(0.08, 0.12, chg + ' vs prev period', transform=ax.transAxes,
            fontsize=7, color=chg_color, fontfamily='monospace')

# ── Revenue & Orders Trend ───────────────────────────────────
ax_rev = fig.add_subplot(gs[1, :3])
ax_rev.set_facecolor(SURFACE)
ax2 = ax_rev.twinx()

bars = ax_rev.bar(dates, revenue, color=GREEN + '25', edgecolor=GREEN,
                  linewidth=0.8, width=0.8)
line, = ax2.plot(dates, orders, color=BLUE, linewidth=2,
                 marker='o', markersize=3, markerfacecolor=BLUE)

ax_rev.set_title('DAILY REVENUE & ORDERS TREND', color=TEXT,
                 fontsize=9, pad=8, loc='left', fontfamily='monospace')
ax_rev.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x/1000:.0f}k'))
ax_rev.tick_params(axis='x', rotation=30, labelsize=7)
ax_rev.tick_params(axis='y', labelsize=7, colors=GREEN)
ax2.tick_params(axis='y', labelsize=7, colors=BLUE)
ax2.set_ylabel('Orders', color=BLUE, fontsize=7)
ax_rev.set_ylabel('Revenue ($)', color=GREEN, fontsize=7)
ax_rev.grid(axis='y', alpha=0.4)

legend_elements = [
    mpatches.Patch(facecolor=GREEN+'44', edgecolor=GREEN, label='Revenue'),
    plt.Line2D([0], [0], color=BLUE, linewidth=2, marker='o', markersize=4, label='Orders')
]
ax_rev.legend(handles=legend_elements, loc='upper left',
              facecolor=SURFACE2, edgecolor=BORDER, labelcolor=TEXT, fontsize=7)

# ── Category Donut ───────────────────────────────────────────
ax_cat = fig.add_subplot(gs[1, 3])
ax_cat.set_facecolor(SURFACE)
wedges, texts, autotexts = ax_cat.pie(
    cat_rev, labels=categories,
    colors=[c + '66' for c in PALETTE],
    autopct='%1.0f%%',
    startangle=90,
    wedgeprops={'width': 0.55, 'edgecolor': BG, 'linewidth': 2},
    pctdistance=0.75,
    textprops={'fontsize': 6, 'color': MUTED, 'fontfamily': 'monospace'}
)
for at, color in zip(autotexts, PALETTE):
    at.set_color(color); at.set_fontsize(6)
ax_cat.set_title('CATEGORY SHARE', color=TEXT, fontsize=9,
                 pad=8, loc='left', fontfamily='monospace')

# center text
ax_cat.text(0, 0, '$284.6K\nREVENUE', ha='center', va='center',
            fontsize=8, color=GREEN, fontfamily='monospace', linespacing=1.4)

# ── Top Products ─────────────────────────────────────────────
ax_prod = fig.add_subplot(gs[2, :2])
ax_prod.set_facecolor(SURFACE)
y_pos = range(len(products))
colors_p = PALETTE[:len(products)]
bars_p = ax_prod.barh(y_pos, prod_rev,
                      color=[c + '33' for c in colors_p],
                      edgecolor=colors_p, linewidth=1.2, height=0.55)
ax_prod.set_yticks(y_pos)
ax_prod.set_yticklabels(products, fontsize=8)
ax_prod.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x/1000:.0f}k'))
ax_prod.set_title('TOP PRODUCTS BY REVENUE', color=TEXT,
                  fontsize=9, pad=8, loc='left', fontfamily='monospace')
ax_prod.grid(axis='x', alpha=0.3)
for bar, color, val in zip(bars_p, colors_p, prod_rev):
    ax_prod.text(bar.get_width() + 300, bar.get_y() + bar.get_height()/2,
                 f'${val/1000:.1f}k', va='center', fontsize=7,
                 color=color, fontfamily='monospace')

# ── Regional Revenue ─────────────────────────────────────────
ax_geo = fig.add_subplot(gs[2, 2])
ax_geo.set_facecolor(SURFACE)
bars_g = ax_geo.bar(regions, reg_rev,
                    color=[c + '33' for c in PALETTE],
                    edgecolor=PALETTE, linewidth=1.2, width=0.6)
ax_geo.set_title('REVENUE BY REGION (%)', color=TEXT,
                 fontsize=9, pad=8, loc='left', fontfamily='monospace')
ax_geo.tick_params(axis='x', labelsize=7, rotation=15)
ax_geo.set_ylabel('%', fontsize=7)
ax_geo.grid(axis='y', alpha=0.3)
for bar, val in zip(bars_g, reg_rev):
    ax_geo.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{val}%', ha='center', fontsize=7,
                color=TEXT, fontfamily='monospace')

# ── Conversion Funnel ─────────────────────────────────────────
ax_fun = fig.add_subplot(gs[2, 3])
ax_fun.set_facecolor(SURFACE)
ax_fun.set_xlim(-1, 1); ax_fun.set_ylim(-0.5, len(funnel_vals) - 0.5)
ax_fun.axis('off')
ax_fun.set_title('CONVERSION FUNNEL', color=TEXT,
                 fontsize=9, pad=8, loc='left', fontfamily='monospace')

max_val = funnel_vals[0]
fun_colors = [BLUE, PURPLE, YELLOW, ORANGE, GREEN]
for i, (stage, val, color) in enumerate(zip(funnel_stages, funnel_vals, fun_colors)):
    width = (val / max_val) * 1.6
    y = len(funnel_vals) - 1 - i
    rect = FancyBboxPatch((-width/2, y - 0.3), width, 0.55,
                          boxstyle='round,pad=0.02',
                          facecolor=color + '33', edgecolor=color, linewidth=1.2)
    ax_fun.add_patch(rect)
    pct = val / max_val * 100
    ax_fun.text(0, y, f'{pct:.1f}%', ha='center', va='center',
                fontsize=8, color=color, fontweight='bold', fontfamily='monospace')
    ax_fun.text(-0.98, y, stage.replace('\n', ' '),
                ha='left', va='center', fontsize=6, color=MUTED, fontfamily='monospace')

# ── AOV Trend ────────────────────────────────────────────────
ax_aov = fig.add_subplot(gs[3, :2])
ax_aov.set_facecolor(SURFACE)
ax_aov.fill_between(dates, aov, alpha=0.15, color=YELLOW)
ax_aov.plot(dates, aov, color=YELLOW, linewidth=2)
ax_aov.axhline(aov.mean(), color=YELLOW, linewidth=1, linestyle='--', alpha=0.5)
ax_aov.text(dates[-1], aov.mean(), f'  AVG ${aov.mean():.0f}',
            va='center', fontsize=7, color=YELLOW, fontfamily='monospace')
ax_aov.set_title('AVERAGE ORDER VALUE TREND (30 DAYS)', color=TEXT,
                 fontsize=9, pad=8, loc='left', fontfamily='monospace')
ax_aov.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:.0f}'))
ax_aov.tick_params(axis='x', rotation=30, labelsize=7)
ax_aov.tick_params(axis='y', labelsize=7)
ax_aov.grid(axis='y', alpha=0.3)

# ── Monthly Goals ─────────────────────────────────────────────
ax_goals = fig.add_subplot(gs[3, 2:])
ax_goals.set_facecolor(SURFACE)
ax_goals.axis('off')
ax_goals.set_title('MONTHLY GOAL PROGRESS', color=TEXT,
                   fontsize=9, pad=8, loc='left', fontfamily='monospace')

goals = [
    ('REVENUE TARGET',    84, GREEN),
    ('ORDER TARGET',      91, BLUE),
    ('NEW USERS TARGET',  67, YELLOW),
    ('RETENTION TARGET',  78, PURPLE),
]
for i, (label, pct, color) in enumerate(goals):
    y = 0.82 - i * 0.22
    ax_goals.text(0.02, y + 0.07, label, transform=ax_goals.transAxes,
                  fontsize=7, color=MUTED, fontfamily='monospace')
    # track
    ax_goals.add_patch(FancyBboxPatch((0.02, y - 0.02), 0.72, 0.08,
                                      transform=ax_goals.transAxes,
                                      boxstyle='round,pad=0',
                                      facecolor=BORDER, edgecolor='none'))
    # fill
    ax_goals.add_patch(FancyBboxPatch((0.02, y - 0.02), 0.72 * pct/100, 0.08,
                                      transform=ax_goals.transAxes,
                                      boxstyle='round,pad=0',
                                      facecolor=color + '88', edgecolor=color,
                                      linewidth=0.8))
    ax_goals.text(0.76, y + 0.02, f'{pct}%', transform=ax_goals.transAxes,
                  fontsize=9, color=color, fontweight='bold', fontfamily='monospace')

# ── Save ─────────────────────────────────────────────────────
plt.savefig('ecommerce_kpi_dashboard.png', dpi=150,
            bbox_inches='tight', facecolor=BG)
plt.show()
print("✅ Dashboard saved as 'ecommerce_kpi_dashboard.png'")
print("   Author: Abdul Hadi | github.com/abdulhadi1126")
