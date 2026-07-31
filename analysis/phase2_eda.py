"""
PHASE 2 — EXPLORATORY DATA ANALYSIS
Thesis: Benchmarking Traditional Web Servers vs Serverless (E-Commerce)
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import json

# Set publication-quality style
sns.set_theme(context="paper", style="ticks", palette="colorblind", font_scale=0.95)
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'

df = pd.read_csv('master_runs_VALIDATED.csv')

# Map of pretty platform names for plotting
PLATFORM_LABEL = {
    '01_apache_modwsgi':   'Apache+mod_wsgi',
    '02_nginx_uwsgi':      'Nginx+uWSGI',
    '03_django_gunicorn':  'Django+Gunicorn',
    '04_aca':              'Azure Container Apps',
    '05_koyeb':            'Koyeb',
    '06_flyio':            'Fly.io',
    '07_iis_waitress':     'IIS+Waitress'
}

# Add a 'platform_pretty' column for plots
df['platform_label'] = df['platform'].map(PLATFORM_LABEL)

print("=" * 70)
print("PHASE 2 — EXPLORATORY DATA ANALYSIS")
print("=" * 70)

# ===================================================================
# 2.1 DESCRIPTIVE STATISTICS PER CELL
# ===================================================================
print("\n[2.1] DESCRIPTIVE STATISTICS PER CELL")
print("-" * 70)

METRICS = ['latency_p50', 'latency_p95', 'latency_p99',
           'rps_actual', 'goodput_rps', 'error_rate', 'apdex_t500_f2000']

def cell_stats(series):
    s = series.dropna()
    if len(s) == 0:
        return pd.Series({k: np.nan for k in
                         ['n', 'mean', 'sd', 'median', 'min', 'max', 'cv_pct']})
    mean = s.mean()
    sd = s.std(ddof=1)
    return pd.Series({
        'n': len(s),
        'mean': mean,
        'sd': sd,
        'median': s.median(),
        'min': s.min(),
        'max': s.max(),
        'cv_pct': (100 * sd / mean) if mean else np.nan,
    })

# Build all descriptive tables
desc_tables = {}
for m in METRICS:
    table = df.groupby(['platform', 'scenario'])[m].apply(cell_stats).unstack()
    desc_tables[m] = table
    print(f"\n=== {m} ===")
    print(table[['median', 'cv_pct', 'min', 'max']].round(3).to_string())
    # Save
    table.round(4).to_csv(f'desc_{m}.csv')

# ===================================================================
# 2.2 HIGH-VARIANCE CELLS (CV > 15%) on latency_p95
# ===================================================================
print("\n[2.2] HIGH-VARIANCE CELLS (CV > 15% on latency_p95)")
print("-" * 70)
hv_p95 = desc_tables['latency_p95'][desc_tables['latency_p95']['cv_pct'] > 15]
print(hv_p95[['median', 'cv_pct', 'min', 'max']].round(2).to_string())

print(f"\nNumber of HIGH-VARIANCE cells (CV>15%): {len(hv_p95)} / 28")

# ===================================================================
# 2.3 OUTLIER DETECTION (Tukey 3×IQR)
# ===================================================================
print("\n[2.3] OUTLIER DETECTION (Tukey 3×IQR on latency_p95)")
print("-" * 70)
outliers_list = []
for (p, sc), g in df.groupby(['platform', 'scenario']):
    s = g['latency_p95']
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    lo, hi = q1 - 3 * iqr, q3 + 3 * iqr
    mask = (s < lo) | (s > hi)
    for _, r in g[mask].iterrows():
        outliers_list.append({
            'platform': p,
            'scenario': sc,
            'replication': int(r['replication']),
            'latency_p95': r['latency_p95'],
            'fence_low': lo,
            'fence_high': hi,
            'cell_median': s.median(),
        })

outliers_df = pd.DataFrame(outliers_list)
if len(outliers_df) > 0:
    print(f"Extreme outliers found: {len(outliers_df)}")
    print(outliers_df.round(2).to_string(index=False))
    outliers_df.to_csv('outliers_extreme.csv', index=False)
else:
    print("No extreme outliers found.")

# ===================================================================
# 2.4 TIME-OF-DAY EFFECTS
# ===================================================================
print("\n[2.4] TIME-OF-DAY EFFECTS")
print("-" * 70)
df['start_dt'] = pd.to_datetime(df['start_time'])
df['hour'] = df['start_dt'].dt.hour
df['date'] = df['start_dt'].dt.date

# Spearman correlation between hour and p95 per cell
tod_corr = []
for (p, sc), g in df.groupby(['platform', 'scenario']):
    if g['hour'].nunique() >= 5:  # need enough variability
        rho, pv = stats.spearmanr(g['hour'], g['latency_p95'])
        tod_corr.append({
            'platform': p,
            'scenario': sc,
            'spearman_rho': rho,
            'p_value': pv,
            'significant_at_10pct': pv < 0.10
        })

tod_df = pd.DataFrame(tod_corr)
sig_tod = tod_df[tod_df['p_value'] < 0.10]
if len(sig_tod) > 0:
    print(f"Cells with time-of-day correlation (p < 0.10): {len(sig_tod)}")
    print(sig_tod.round(3).to_string(index=False))
else:
    print("No significant time-of-day correlations (p < 0.10)")

tod_df.to_csv('time_of_day_correlations.csv', index=False)

# ===================================================================
# 2.5 NORMALITY DIAGNOSTICS
# ===================================================================
print("\n[2.5] NORMALITY DIAGNOSTICS (Shapiro-Wilk per cell)")
print("-" * 70)
print("Note: With n=10 per cell, this has LOW power. Result is informational.")

norm_results = []
for (p, sc), g in df.groupby(['platform', 'scenario']):
    s = g['latency_p95']
    if s.nunique() > 2:
        try:
            stat, pv = stats.shapiro(s)
            norm_results.append({
                'platform': p,
                'scenario': sc,
                'shapiro_w': stat,
                'p_value': pv,
                'rejects_normality': pv < 0.05
            })
        except Exception:
            pass

norm_df = pd.DataFrame(norm_results)
n_reject = norm_df['rejects_normality'].sum()
n_total = len(norm_df)
print(f"Cells rejecting normality (p<0.05): {n_reject}/{n_total}")
norm_df.to_csv('normality_shapiro.csv', index=False)

# ===================================================================
# 2.6 HOMOSCEDASTICITY (Levene per scenario, across 7 platforms)
# ===================================================================
print("\n[2.6] HOMOSCEDASTICITY (Levene/Brown-Forsythe per scenario)")
print("-" * 70)
levene_results = []
for sc, g in df.groupby('scenario'):
    samples = [grp['latency_p95'].values for _, grp in g.groupby('platform')]
    stat, pv = stats.levene(*samples, center='median')  # Brown-Forsythe variant
    levene_results.append({
        'scenario': sc,
        'levene_W': stat,
        'p_value': pv,
        'rejects_homoscedasticity': pv < 0.05
    })

lev_df = pd.DataFrame(levene_results)
print(lev_df.round(4).to_string(index=False))
lev_df.to_csv('levene_homoscedasticity.csv', index=False)

# Decision: if normality FAILS in most cells OR homoscedasticity FAILS,
# we use NON-PARAMETRIC tests in Phase 3.
print(f"\nDecision: With {n_reject}/{n_total} cells non-normal and "
      f"{lev_df['rejects_homoscedasticity'].sum()}/4 scenarios heteroscedastic, "
      f"Phase 3 will branch to Kruskal-Wallis + Dunn (non-parametric).")

# ===================================================================
# 2.7 KEY VISUALIZATIONS
# ===================================================================
print("\n[2.7] GENERATING EXPLORATORY VISUALIZATIONS")
print("-" * 70)

# Boxplot of p95 latency per platform × scenario (LOG SCALE — recommended for skewed data)
g = sns.catplot(
    data=df, x='platform_label', y='latency_p95',
    col='scenario', col_wrap=2, kind='box',
    sharey=False, height=3.5, aspect=1.3,
    palette='colorblind'
)
for ax in g.axes.flat:
    ax.set_yscale('log')
    ax.tick_params(axis='x', rotation=30)
    ax.set_xlabel('')
    ax.set_ylabel('p95 latency (ms, log scale)')
    ax.grid(True, which='both', linestyle='--', alpha=0.3)
plt.suptitle('p95 Latency by Platform × Scenario (log scale)', y=1.02)
g.savefig('eda_box_p95_log.png', dpi=200)
plt.close()
print("  ✓ eda_box_p95_log.png")

# Violin plot of p95 latency per scenario, colored by platform
fig, axes = plt.subplots(2, 2, figsize=(14, 8), sharey=False)
for ax, sc in zip(axes.flat, ['A_browse', 'B_mixed', 'C_checkout', 'D_burst']):
    d = df[df['scenario'] == sc].copy()
    sns.boxplot(data=d, x='platform_label', y='latency_p95', ax=ax,
                palette='colorblind', showfliers=True)
    sns.stripplot(data=d, x='platform_label', y='latency_p95', ax=ax,
                  color='black', size=2.5, alpha=0.6)
    ax.set_yscale('log')
    ax.set_title(f'Scenario {sc} — p95 Latency (10 reps each)')
    ax.set_xlabel('')
    ax.set_ylabel('p95 latency (ms)')
    ax.tick_params(axis='x', rotation=30)
    ax.grid(True, which='both', linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig('eda_box_per_scenario.png', dpi=200)
plt.close()
print("  ✓ eda_box_per_scenario.png")

# Heatmap of CV per platform × scenario
fig, ax = plt.subplots(figsize=(8, 5))
cv_matrix = desc_tables['latency_p95']['cv_pct'].unstack()
cv_matrix.index = [PLATFORM_LABEL.get(p, p) for p in cv_matrix.index]
sns.heatmap(cv_matrix, annot=True, fmt='.1f', cmap='YlOrRd',
            cbar_kws={'label': 'CV (%)'}, ax=ax, vmin=0, vmax=80)
ax.set_title('Replication CV (%) of p95 Latency — flagged > 15%')
ax.set_xlabel('Scenario')
ax.set_ylabel('Platform')
plt.tight_layout()
plt.savefig('eda_heatmap_cv.png', dpi=200)
plt.close()
print("  ✓ eda_heatmap_cv.png")

# Apdex heatmap
fig, ax = plt.subplots(figsize=(8, 5))
apdex_matrix = df.groupby(['platform', 'scenario'])['apdex_t500_f2000'].median().unstack()
apdex_matrix.index = [PLATFORM_LABEL.get(p, p) for p in apdex_matrix.index]
sns.heatmap(apdex_matrix, annot=True, fmt='.3f', cmap='RdYlGn',
            cbar_kws={'label': 'Apdex (T=500ms)'}, ax=ax, vmin=0.5, vmax=1.0)
ax.set_title('Median Apdex per Platform × Scenario (T=500ms, F=2000ms)')
ax.set_xlabel('Scenario')
ax.set_ylabel('Platform')
plt.tight_layout()
plt.savefig('eda_heatmap_apdex.png', dpi=200)
plt.close()
print("  ✓ eda_heatmap_apdex.png")

# Median p95 heatmap
fig, ax = plt.subplots(figsize=(8, 5))
p95_matrix = desc_tables['latency_p95']['median'].unstack()
p95_matrix.index = [PLATFORM_LABEL.get(p, p) for p in p95_matrix.index]
sns.heatmap(p95_matrix, annot=True, fmt='.0f', cmap='YlOrRd',
            cbar_kws={'label': 'p95 latency (ms)'}, ax=ax, norm=matplotlib.colors.LogNorm())
ax.set_title('Median p95 Latency per Platform × Scenario (ms, log color)')
ax.set_xlabel('Scenario')
ax.set_ylabel('Platform')
plt.tight_layout()
plt.savefig('eda_heatmap_p95.png', dpi=200)
plt.close()
print("  ✓ eda_heatmap_p95.png")

# ===================================================================
# 2.8 INITIAL WINNERS/LOSERS NARRATIVE
# ===================================================================
print("\n[2.8] INITIAL WINNERS PER METRIC (median across 10 reps)")
print("-" * 70)
for sc in ['A_browse', 'B_mixed', 'C_checkout', 'D_burst']:
    print(f"\n--- Scenario {sc} (target {df[df.scenario==sc].target_rps.iloc[0]} RPS) ---")
    sub = df[df['scenario'] == sc]
    cell_medians = sub.groupby('platform_label').agg(
        p95_median=('latency_p95', 'median'),
        p95_iqr=('latency_p95', lambda x: x.quantile(0.75) - x.quantile(0.25)),
        goodput_med=('goodput_rps', 'median'),
        err_med=('error_rate', 'median'),
        apdex_med=('apdex_t500_f2000', 'median'),
    )
    print(cell_medians.sort_values('p95_median').round(3).to_string())

# ===================================================================
# 2.9 SAVE SUMMARY REPORT
# ===================================================================
eda_summary = {
    'metrics_analyzed': METRICS,
    'high_variance_cells': len(hv_p95),
    'extreme_outliers': len(outliers_df),
    'cells_rejecting_normality': int(n_reject),
    'cells_tested_normality': int(n_total),
    'scenarios_heteroscedastic': int(lev_df['rejects_homoscedasticity'].sum()),
    'phase3_decision': 'non-parametric (Kruskal-Wallis + Dunn)',
    'figures_generated': [
        'eda_box_p95_log.png',
        'eda_box_per_scenario.png',
        'eda_heatmap_cv.png',
        'eda_heatmap_apdex.png',
        'eda_heatmap_p95.png',
    ],
}

with open('phase2_eda_summary.json', 'w') as f:
    json.dump(eda_summary, f, indent=2, default=str)

print("\n" + "=" * 70)
print("✓ PHASE 2 EDA COMPLETE")
print("=" * 70)
print(f"  High-variance cells (CV>15%): {len(hv_p95)} / 28")
print(f"  Extreme outliers (3×IQR):     {len(outliers_df)}")
print(f"  Non-normal cells:             {n_reject} / {n_total}")
print(f"  Heteroscedastic scenarios:    {int(lev_df['rejects_homoscedasticity'].sum())} / 4")
print(f"  Phase 3 branch:               NON-PARAMETRIC (Kruskal-Wallis + Dunn)")
print(f"  Figures saved:                5 PNG files")
print(f"  Tables saved:                 7 CSV files")
