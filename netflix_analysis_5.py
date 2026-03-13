"""
Netflix Content Intelligence
=============================
Dataset : netflix_movies__1_.csv  (8,807 titles)
Output  : netflix_analysis.png
Requires: pandas, matplotlib
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import FuncFormatter
from collections import Counter
import numpy as np

# ─────────────────────────────────────────────────
# 1. LOAD & CLEAN
# ─────────────────────────────────────────────────
df = pd.read_csv('netflix_movies__1_.csv')

df['date_added']   = pd.to_datetime(df['date_added'].str.strip(), errors='coerce')
df['year_added']   = df['date_added'].dt.year
df['month_added']  = df['date_added'].dt.month

movies = df[df['type'] == 'Movie'].copy()
shows  = df[df['type'] == 'TV Show'].copy()

movies['mins']    = movies['duration'].str.extract(r'(\d+)').astype(float)
shows['seasons']  = shows['duration'].str.extract(r'(\d+)').astype(float)

# ─────────────────────────────────────────────────
# 2. GENRE HELPERS
# ─────────────────────────────────────────────────
def get_genres(sub_df):
    genres = []
    for row in sub_df['listed_in'].dropna():
        genres.extend([x.strip() for x in row.split(',')])
    return Counter(genres)

movie_genres = get_genres(movies)
show_genres  = get_genres(shows)
top_movie_g  = dict(movie_genres.most_common(10))
top_show_g   = dict(show_genres.most_common(10))

# ─────────────────────────────────────────────────
# 3. TREND DATA
# ─────────────────────────────────────────────────
trend = (
    df.groupby(['year_added', 'type'])
    .size()
    .unstack(fill_value=0)
)
trend = trend[trend.index >= 2015]

# ─────────────────────────────────────────────────
# 4. PLOT THEME
# ─────────────────────────────────────────────────
BG     = '#0f0f0f'
CARD   = '#161616'
BORDER = '#282828'
RED    = '#e50914'
GOLD   = '#e5b014'
TEAL   = '#00b4d8'
TEXT   = '#e8e8e8'
MUTED  = '#888888'

plt.rcParams.update({
    'figure.facecolor':  BG,
    'axes.facecolor':    CARD,
    'axes.edgecolor':    BORDER,
    'axes.labelcolor':   TEXT,
    'xtick.color':       MUTED,
    'ytick.color':       MUTED,
    'text.color':        TEXT,
    'grid.color':        BORDER,
    'grid.alpha':        1,
    'font.family':       'DejaVu Sans',
    'font.size':         10,
    'axes.spines.top':   False,
    'axes.spines.right': False,
})

# ─────────────────────────────────────────────────
# 5. FIGURE & GRID
# ─────────────────────────────────────────────────
fig = plt.figure(figsize=(20, 24), facecolor=BG)
gs  = gridspec.GridSpec(4, 12, figure=fig,
                        left=0.05, right=0.97,
                        top=0.93,  bottom=0.04,
                        hspace=0.6, wspace=0.4)

# Title
fig.text(0.05, 0.965, 'Netflix Content Intelligence',
         fontsize=28, fontweight='bold', color=TEXT, va='top')
fig.text(0.05, 0.952,
         f'{len(df):,} titles  ·  Movies & TV Shows  ·  '
         f'{df["release_year"].min()}–{df["release_year"].max()}',
         fontsize=12, color=MUTED, va='top')
fig.add_artist(plt.Line2D(
    [0.05, 0.95], [0.945, 0.945],
    transform=fig.transFigure,
    color=RED, linewidth=1.2, alpha=0.6
))


# ══════════════════════════════════════════════════
# ROW 1 — Movies vs TV Shows
# ══════════════════════════════════════════════════

# ── 1a. Type split donut ──
ax1 = fig.add_subplot(gs[0, 0:3])
ax1.set_aspect('equal')
wedges, _ = ax1.pie(
    [len(movies), len(shows)],
    colors=[RED, TEAL],
    startangle=90,
    wedgeprops=dict(width=0.52, edgecolor=BG, linewidth=2),
)
ax1.text(0, 0.15, f'{len(movies):,}',
         ha='center', va='center',
         fontsize=20, fontweight='bold', color=RED)
ax1.text(0, -0.18, 'Movies', ha='center', fontsize=9, color=MUTED)
ax1.set_title('Content Split', fontsize=11, fontweight='bold', color=TEXT, pad=12)
ax1.legend(
    [f'Movies  {len(movies):,}  (69.6%)',
     f'TV Shows  {len(shows):,}  (30.4%)'],
    loc='lower center', bbox_to_anchor=(0.5, -0.18),
    fontsize=8.5, frameon=False, labelcolor=TEXT,
)

# ── 1b. Rating distribution ──
ax2 = fig.add_subplot(gs[0, 3:7])
ratings_order = ['TV-Y','TV-Y7','TV-G','G','PG','TV-PG','PG-13','TV-14','TV-MA','R','NR']
r_data = (
    df[df['rating'].isin(ratings_order)]
    .groupby(['rating', 'type'])
    .size()
    .unstack(fill_value=0)
    .reindex([r for r in ratings_order if r in df['rating'].values])
)
bar_w = 0.38
x2    = np.arange(len(r_data))
ax2.bar(x2 - bar_w/2, r_data.get('Movie',   0), bar_w, color=RED,  alpha=0.85, label='Movie',   zorder=3)
ax2.bar(x2 + bar_w/2, r_data.get('TV Show', 0), bar_w, color=TEAL, alpha=0.85, label='TV Show', zorder=3)
ax2.set_xticks(x2)
ax2.set_xticklabels(r_data.index, rotation=30, ha='right', fontsize=8.5)
ax2.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{int(v):,}'))
ax2.set_title('Content by Rating', fontsize=11, fontweight='bold', color=TEXT, pad=8)
ax2.legend(frameon=False, fontsize=8.5, labelcolor=TEXT)
ax2.grid(axis='y', alpha=0.3); ax2.set_axisbelow(True)

# ── 1c. Movie duration histogram ──
ax3 = fig.add_subplot(gs[0, 7:10])
m_clean = movies.dropna(subset=['mins'])
n, bins, patches = ax3.hist(
    m_clean['mins'], bins=40,
    color=RED, alpha=0.8, edgecolor=BG, linewidth=0.4, zorder=3,
)
for p, b in zip(patches, bins):          # highlight sweet-spot band
    if 80 <= b <= 120:
        p.set_facecolor(GOLD)
ax3.axvline(m_clean['mins'].median(), color=GOLD, linewidth=1.5,
            linestyle='--', label=f"Median: {m_clean['mins'].median():.0f} min")
ax3.set_xlabel('Duration (minutes)', fontsize=9)
ax3.set_title('Movie Duration Distribution', fontsize=11, fontweight='bold', color=TEXT, pad=8)
ax3.legend(frameon=False, fontsize=8.5, labelcolor=TEXT)
ax3.grid(axis='y', alpha=0.3); ax3.set_axisbelow(True)

# ── 1d. TV show seasons ──
ax4 = fig.add_subplot(gs[0, 10:12])
sc   = shows.dropna(subset=['seasons'])['seasons'].value_counts().sort_index().head(8)
bars = ax4.barh(sc.index.astype(int), sc.values,
                color=TEAL, alpha=0.85, edgecolor=BG, linewidth=0.4,
                zorder=3)
ax4.set_xlabel('Shows',   fontsize=9)
ax4.set_ylabel('Seasons', fontsize=9)
ax4.set_title('TV Show Seasons', fontsize=11, fontweight='bold', color=TEXT, pad=8)
ax4.grid(axis='x', alpha=0.3); ax4.set_axisbelow(True)
for bar in bars:
    ax4.text(bar.get_width() + 8,
             bar.get_y() + bar.get_height() / 2,
             f'{int(bar.get_width())}', va='center', fontsize=8, color=MUTED)


# ══════════════════════════════════════════════════
# ROW 2 — Most Popular Genres
# ══════════════════════════════════════════════════

# ── 2a. Top 10 Movie Genres ──
ax5 = fig.add_subplot(gs[1, 0:5])
mg_labels = list(top_movie_g.keys())[::-1]
mg_vals   = list(top_movie_g.values())[::-1]
palette   = plt.cm.RdYlBu_r(np.linspace(0.15, 0.75, len(mg_labels)))
bars5     = ax5.barh(mg_labels, mg_vals, color=palette, alpha=0.9,
                     edgecolor=BG, linewidth=0.3, zorder=3, height=0.65)
ax5.set_title('Top 10 Movie Genres', fontsize=11, fontweight='bold', color=TEXT, pad=8)
ax5.grid(axis='x', alpha=0.3); ax5.set_axisbelow(True)
ax5.tick_params(axis='y', labelsize=8.5)
for bar in bars5:
    ax5.text(bar.get_width() + 20,
             bar.get_y() + bar.get_height() / 2,
             f'{int(bar.get_width()):,}', va='center', fontsize=8, color=MUTED)

# ── 2b. Top 10 TV Show Genres ──
ax6 = fig.add_subplot(gs[1, 5:10])
sg_labels = list(top_show_g.keys())[::-1]
sg_vals   = list(top_show_g.values())[::-1]
palette2  = plt.cm.PuBuGn(np.linspace(0.25, 0.85, len(sg_labels)))
bars6     = ax6.barh(sg_labels, sg_vals, color=palette2, alpha=0.9,
                     edgecolor=BG, linewidth=0.3, zorder=3, height=0.65)
ax6.set_title('Top 10 TV Show Genres', fontsize=11, fontweight='bold', color=TEXT, pad=8)
ax6.grid(axis='x', alpha=0.3); ax6.set_axisbelow(True)
ax6.tick_params(axis='y', labelsize=8.5)
for bar in bars6:
    ax6.text(bar.get_width() + 10,
             bar.get_y() + bar.get_height() / 2,
             f'{int(bar.get_width()):,}', va='center', fontsize=8, color=MUTED)

# ── 2c. Genre overlap (shared genres) ──
ax7 = fig.add_subplot(gs[1, 10:12])
shared   = ['Dramas', 'Comedies', 'Documentaries',
            'Action & Adventure', 'Thrillers', 'Horror Movies']
m_vals_s = [movie_genres.get(g, 0) for g in shared]
s_vals_s = [show_genres.get(g,  0) for g in shared]
x7 = np.arange(len(shared)); w = 0.36
ax7.bar(x7 - w/2, m_vals_s, w, color=RED,  alpha=0.85, label='Movies',   zorder=3)
ax7.bar(x7 + w/2, s_vals_s, w, color=TEAL, alpha=0.85, label='TV Shows', zorder=3)
ax7.set_xticks(x7)
ax7.set_xticklabels([g.split(' ')[0] for g in shared],
                    rotation=25, ha='right', fontsize=7.5)
ax7.set_title('Genre Overlap', fontsize=11, fontweight='bold', color=TEXT, pad=8)
ax7.legend(frameon=False, fontsize=7.5, labelcolor=TEXT)
ax7.grid(axis='y', alpha=0.3); ax7.set_axisbelow(True)


# ══════════════════════════════════════════════════
# ROW 3 — Content Release Trends
# ══════════════════════════════════════════════════

# ── 3a. Stacked area — titles added by year ──
ax8  = fig.add_subplot(gs[2, 0:7])
yrs  = trend.index.astype(int)
mv   = trend.get('Movie',   pd.Series(0, index=trend.index)).values
tv   = trend.get('TV Show', pd.Series(0, index=trend.index)).values
ax8.stackplot(yrs, mv, tv,
              labels=['Movies', 'TV Shows'],
              colors=[RED, TEAL], alpha=0.85, zorder=3)
ax8.set_xlim(yrs[0], yrs[-1])
ax8.set_title('Content Added to Netflix Per Year',
              fontsize=12, fontweight='bold', color=TEXT, pad=10)
ax8.set_xlabel('Year',          fontsize=9)
ax8.set_ylabel('Titles Added',  fontsize=9)
ax8.legend(frameon=False, fontsize=9, labelcolor=TEXT, loc='upper left')
ax8.grid(axis='y', alpha=0.3); ax8.set_axisbelow(True)
ax8.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{int(v):,}'))
# Annotate peak year
peak_yr  = trend.sum(axis=1).idxmax()
peak_val = int(trend.sum(axis=1).max())
ax8.annotate(
    f'Peak: {int(peak_yr)}\n{peak_val:,} titles',
    xy=(int(peak_yr), peak_val),
    xytext=(int(peak_yr) - 1.5, peak_val + 80),
    fontsize=8.5, color=GOLD,
    arrowprops=dict(arrowstyle='->', color=GOLD, lw=1.2),
)

# ── 3b. Production year line (2000–2021) ──
ax9  = fig.add_subplot(gs[2, 7:12])
ry_m = movies.groupby('release_year').size()
ry_s = shows.groupby('release_year').size()
ry_m = ry_m[(ry_m.index >= 2000) & (ry_m.index <= 2021)]
ry_s = ry_s[(ry_s.index >= 2000) & (ry_s.index <= 2021)]
ax9.plot(ry_m.index, ry_m.values, color=RED,  lw=2.5,
         marker='o', markersize=4, label='Movies',   zorder=3)
ax9.plot(ry_s.index, ry_s.values, color=TEAL, lw=2.5,
         marker='s', markersize=4, label='TV Shows', zorder=3)
ax9.fill_between(ry_m.index, ry_m.values, alpha=0.12, color=RED)
ax9.fill_between(ry_s.index, ry_s.values, alpha=0.12, color=TEAL)
ax9.set_title('Content by Production Year (2000–2021)',
              fontsize=11, fontweight='bold', color=TEXT, pad=8)
ax9.set_xlabel('Release Year', fontsize=9)
ax9.set_ylabel('Titles',       fontsize=9)
ax9.legend(frameon=False, fontsize=9, labelcolor=TEXT)
ax9.grid(alpha=0.3); ax9.set_axisbelow(True)
ax9.tick_params(axis='x', labelsize=8.5, rotation=20)


# ══════════════════════════════════════════════════
# ROW 4 — Deep Dives
# ══════════════════════════════════════════════════

# ── 4a. Titles added by month ──
ax10 = fig.add_subplot(gs[3, 0:4])
month_avg    = df.groupby('month_added').size()
months_lbl   = ['Jan','Feb','Mar','Apr','May','Jun',
                 'Jul','Aug','Sep','Oct','Nov','Dec']
bar_colors10 = [RED if v == month_avg.max() else '#3a3a3a'
                for v in month_avg.values]
ax10.bar(month_avg.index, month_avg.values,
         color=bar_colors10, edgecolor=BG, linewidth=0.3, zorder=3)
ax10.set_xticks(range(1, 13))
ax10.set_xticklabels(months_lbl, fontsize=8.5)
ax10.set_title('Titles Added by Month (all years)',
               fontsize=11, fontweight='bold', color=TEXT, pad=8)
ax10.grid(axis='y', alpha=0.3); ax10.set_axisbelow(True)

# ── 4b. Top 10 producing countries ──
ax11 = fig.add_subplot(gs[3, 4:8])
countries = []
for c in df['country'].dropna():
    countries.extend([x.strip() for x in c.split(',')])
top_c      = Counter(countries).most_common(10)
c_labels   = [x[0] for x in top_c][::-1]
c_vals     = [x[1] for x in top_c][::-1]
c_colors11 = [RED if l == 'United States' else '#3a3a3a' for l in c_labels]
brs        = ax11.barh(c_labels, c_vals, color=c_colors11, alpha=0.9,
                        edgecolor=BG, linewidth=0.3, zorder=3, height=0.65)
ax11.set_title('Top 10 Content Producing Countries',
               fontsize=11, fontweight='bold', color=TEXT, pad=8)
ax11.grid(axis='x', alpha=0.3); ax11.set_axisbelow(True)
ax11.tick_params(axis='y', labelsize=8.5)
for bar in brs:
    ax11.text(bar.get_width() + 15,
              bar.get_y() + bar.get_height() / 2,
              f'{int(bar.get_width()):,}', va='center', fontsize=8, color=MUTED)

# ── 4c. YoY growth rate ──
ax12 = fig.add_subplot(gs[3, 8:12])
total_per_year = trend.sum(axis=1)
growth         = total_per_year.pct_change() * 100
growth         = growth.dropna()
growth_colors  = [RED if g >= 0 else TEAL for g in growth.values]
ax12.bar(growth.index.astype(int), growth.values,
         color=growth_colors, alpha=0.85, edgecolor=BG, linewidth=0.3, zorder=3)
ax12.axhline(0, color=BORDER, linewidth=0.8)
ax12.set_title('YoY Content Growth Rate (%)',
               fontsize=11, fontweight='bold', color=TEXT, pad=8)
ax12.set_xlabel('Year', fontsize=9)
ax12.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:.0f}%'))
ax12.grid(axis='y', alpha=0.3); ax12.set_axisbelow(True)
ax12.tick_params(axis='x', labelsize=8.5, rotation=20)
for yr, val in zip(growth.index.astype(int), growth.values):
    ax12.text(yr, val + (3 if val >= 0 else -5), f'{val:.0f}%',
              ha='center', fontsize=7.5,
              color=GOLD if abs(val) > 50 else MUTED)


# ─────────────────────────────────────────────────
# 6. SAVE
# ─────────────────────────────────────────────────
OUTPUT = 'netflix_analysis.png'
plt.savefig(OUTPUT, dpi=160, bbox_inches='tight', facecolor=BG)
print(f"✅  Saved → {OUTPUT}")
