"""
PHASE 3 — INFERENTIAL STATISTICS
Thesis: Benchmarking Traditional Web Servers vs Serverless (E-Commerce)

Decision branch (pre-registered from Phase 2):
- 18/28 cells reject normality (Shapiro-Wilk)
- 3/4 scenarios reject homoscedasticity (Levene)
→ Use NON-PARAMETRIC: Kruskal-Wallis + Dunn post-hoc

Hypotheses (pre-registered):
- H_omnibus per scenario: At least one platform differs significantly on p95 latency
- H_pairwise: Which specific platform pairs differ (Dunn + Holm-Bonferroni)
- Effect sizes: Cliff's δ for pairwise comparisons
- 95% CIs: BCa bootstrap, 10,000 resamples, seed = 20260603

Multiple testing correction:
- Within each scenario: Holm-Bonferroni across the 21 pairwise tests (7 platforms = C(7,2))
- Across the 4-scenario family: Holm-Bonferroni on omnibus p-values
"""

import pandas as pd
import numpy as np
from scipy import stats
import scikit_posthocs as sp
from statsmodels.stats.multitest import multipletests
import json
from itertools import combinations

SEED = 20260603
N_BOOT = 10000

# Load validated data
df = pd.read_csv('master_runs_VALIDATED.csv')

PLATFORM_LABEL = {
    '01_apache_modwsgi': 'Apache+mod_wsgi',
    '02_nginx_uwsgi': 'Nginx+uWSGI',
    '03_django_gunicorn': 'Django+Gunicorn',
    '04_aca': 'Azure Container Apps',
    '05_koyeb': 'Koyeb',
    '06_flyio': 'Fly.io',
    '07_iis_waitress': 'IIS+Waitress'
}

SCENARIOS = ['A_browse', 'B_mixed', 'C_checkout', 'D_burst']
PLATFORMS = sorted(df['platform'].unique())

print("=" * 70)
print("PHASE 3 — INFERENTIAL STATISTICS")
print("Pre-registered: Kruskal-Wallis + Dunn (Holm-Bonferroni)")
print("Seed:", SEED, "| Bootstrap resamples:", N_BOOT)
print("=" * 70)

# ===================================================================
# 3.1 OMNIBUS TESTS — Kruskal-Wallis per scenario per metric
# ===================================================================
print("\n[3.1] KRUSKAL-WALLIS OMNIBUS TESTS")
print("-" * 70)

METRICS = ['latency_p50', 'latency_p95', 'latency_p99', 'goodput_rps',
           'error_rate', 'apdex_t500_f2000']

omnibus_results = []

for metric in METRICS:
    for sc in SCENARIOS:
        sub = df[df['scenario'] == sc]
        groups = [g[metric].values for _, g in sub.groupby('platform')]
        try:
            stat, pv = stats.kruskal(*groups)
            # eta-squared (rank-based) effect size
            n = sum(len(g) for g in groups)
            k = len(groups)
            eta_sq = (stat - k + 1) / (n - k) if (n - k) > 0 else np.nan
            omnibus_results.append({
                'metric': metric,
                'scenario': sc,
                'kruskal_H': stat,
                'df': k - 1,
                'p_value': pv,
                'eta_squared': max(0, eta_sq),  # clip to >=0
                'n_total': n
            })
        except Exception as e:
            print(f"  Error on {metric}/{sc}: {e}")

omnibus_df = pd.DataFrame(omnibus_results)

# Holm-Bonferroni correction across the 6 metrics × 4 scenarios = 24-test family
omnibus_df = omnibus_df.sort_values(['metric', 'scenario']).reset_index(drop=True)
_, p_adj, _, _ = multipletests(omnibus_df['p_value'].values, alpha=0.05, method='holm')
omnibus_df['p_adj_holm'] = p_adj
omnibus_df['significant_after_holm'] = p_adj < 0.05

print(omnibus_df.round(6).to_string(index=False))
omnibus_df.to_csv('phase3_omnibus_kruskal.csv', index=False)
print(f"\nSaved: phase3_omnibus_kruskal.csv")
print(f"Significant after Holm (α=0.05): {omnibus_df['significant_after_holm'].sum()}/{len(omnibus_df)}")

# ===================================================================
# 3.2 PAIRWISE DUNN POST-HOC (per scenario, focal metric = p95)
# ===================================================================
print("\n[3.2] DUNN PAIRWISE POST-HOC (focal metric: latency_p95)")
print("-" * 70)

all_pairwise = []

for sc in SCENARIOS:
    print(f"\n--- Scenario: {sc} ---")
    sub = df[df['scenario'] == sc].copy()
    # Run Dunn's test using scikit-posthocs
    posthoc = sp.posthoc_dunn(sub, val_col='latency_p95', group_col='platform',
                              p_adjust='holm')
    # Save matrix
    posthoc.to_csv(f'phase3_dunn_{sc}_p95.csv')
    print(posthoc.round(4))
    # Extract pairwise into long format
    for p1, p2 in combinations(PLATFORMS, 2):
        if p1 in posthoc.index and p2 in posthoc.columns:
            pv = posthoc.loc[p1, p2]
            all_pairwise.append({
                'scenario': sc,
                'metric': 'latency_p95',
                'platform_a': p1,
                'platform_b': p2,
                'p_adj_holm': pv,
                'significant': pv < 0.05
            })

pairwise_df = pd.DataFrame(all_pairwise)
pairwise_df.to_csv('phase3_pairwise_dunn_long.csv', index=False)

# ===================================================================
# 3.3 EFFECT SIZES — Cliff's delta for each pair
# ===================================================================
print("\n[3.3] CLIFF'S DELTA EFFECT SIZES (pairwise)")
print("-" * 70)

def cliffs_delta(x, y):
    """Cliff's delta: non-parametric effect size, range [-1, +1].
    Magnitude thresholds (Romano et al. 2006):
      |d| < 0.147  : negligible
      |d| < 0.33   : small
      |d| < 0.474  : medium
      |d| >= 0.474 : large
    """
    x, y = np.asarray(x), np.asarray(y)
    n_x, n_y = len(x), len(y)
    gt = sum(xi > yj for xi in x for yj in y)
    lt = sum(xi < yj for xi in x for yj in y)
    return (gt - lt) / (n_x * n_y)

def cliff_magnitude(d):
    ad = abs(d)
    if ad < 0.147: return 'negligible'
    if ad < 0.33: return 'small'
    if ad < 0.474: return 'medium'
    return 'large'

effect_rows = []
for sc in SCENARIOS:
    sub = df[df['scenario'] == sc]
    for p1, p2 in combinations(PLATFORMS, 2):
        v1 = sub[sub['platform'] == p1]['latency_p95'].values
        v2 = sub[sub['platform'] == p2]['latency_p95'].values
        d = cliffs_delta(v1, v2)
        effect_rows.append({
            'scenario': sc,
            'platform_a': p1,
            'platform_b': p2,
            'median_a': float(np.median(v1)),
            'median_b': float(np.median(v2)),
            'median_diff_a_minus_b': float(np.median(v1) - np.median(v2)),
            'cliffs_delta': d,
            'magnitude': cliff_magnitude(d)
        })

effect_df = pd.DataFrame(effect_rows)
effect_df.to_csv('phase3_cliffs_delta.csv', index=False)
print(f"Computed {len(effect_df)} pairwise Cliff's δ values")
print(f"\nMagnitude distribution:")
print(effect_df['magnitude'].value_counts().to_string())

# ===================================================================
# 3.4 BCa BOOTSTRAP CONFIDENCE INTERVALS for cell medians
# ===================================================================
print("\n[3.4] BCa BOOTSTRAP 95% CIs FOR CELL MEDIANS (10,000 resamples)")
print("-" * 70)

rng = np.random.default_rng(SEED)
ci_rows = []

for metric in ['latency_p95', 'latency_p99', 'goodput_rps', 'apdex_t500_f2000']:
    for p in PLATFORMS:
        for sc in SCENARIOS:
            vals = df[(df['platform'] == p) & (df['scenario'] == sc)][metric].values
            if len(vals) < 2 or vals.std() == 0:
                ci_rows.append({
                    'metric': metric, 'platform': p, 'scenario': sc,
                    'n': len(vals),
                    'median': float(np.median(vals)) if len(vals) > 0 else np.nan,
                    'ci_low': np.nan, 'ci_high': np.nan, 'note': 'degenerate'
                })
                continue
            try:
                res = stats.bootstrap(
                    (vals,), np.median,
                    n_resamples=N_BOOT,
                    method='BCa',
                    confidence_level=0.95,
                    random_state=rng
                )
                ci_rows.append({
                    'metric': metric, 'platform': p, 'scenario': sc,
                    'n': len(vals),
                    'median': float(np.median(vals)),
                    'ci_low': float(res.confidence_interval.low),
                    'ci_high': float(res.confidence_interval.high),
                    'note': 'ok'
                })
            except Exception as e:
                ci_rows.append({
                    'metric': metric, 'platform': p, 'scenario': sc,
                    'n': len(vals),
                    'median': float(np.median(vals)),
                    'ci_low': np.nan, 'ci_high': np.nan,
                    'note': str(e)[:50]
                })

ci_df = pd.DataFrame(ci_rows)
ci_df.to_csv('phase3_bootstrap_ci_medians.csv', index=False)
print(f"  Computed BCa CIs for {len(ci_df)} cell × metric combinations")
print(f"  Successful CIs: {(ci_df['note'] == 'ok').sum()}/{len(ci_df)}")

# ===================================================================
# 3.5 SUMMARY: Top 5 most significant pairwise differences on p95
# ===================================================================
print("\n[3.5] TOP-5 STRONGEST PAIRWISE p95 DIFFERENCES PER SCENARIO")
print("-" * 70)

# Combine pairwise p-values with Cliff's δ
combined = pairwise_df.merge(effect_df, on=['scenario','platform_a','platform_b'])
combined = combined.sort_values(['scenario', 'p_adj_holm'])

for sc in SCENARIOS:
    print(f"\n--- {sc} ---")
    top = combined[combined['scenario'] == sc].nsmallest(5, 'p_adj_holm')
    for _, r in top.iterrows():
        p1 = PLATFORM_LABEL.get(r['platform_a'], r['platform_a'])
        p2 = PLATFORM_LABEL.get(r['platform_b'], r['platform_b'])
        sig = "***" if r['p_adj_holm'] < 0.001 else ("**" if r['p_adj_holm'] < 0.01 else ("*" if r['p_adj_holm'] < 0.05 else "ns"))
        print(f"  {p1[:20]:<20s} vs {p2[:20]:<20s}: "
              f"p={r['p_adj_holm']:.4f} {sig:4s} δ={r['cliffs_delta']:+.3f} ({r['magnitude']})")

# ===================================================================
# 3.6 H4-style Friedman test: D_burst vs steady scenarios on error_rate
# ===================================================================
print("\n[3.6] H4: Friedman test — error_rate across the 4 scenarios")
print("-" * 70)
# Build wide format: each row = (platform, replication), each col = scenario
wide = df.pivot_table(index=['platform','replication'], columns='scenario',
                     values='error_rate', aggfunc='first')
wide = wide.dropna()
if len(wide) > 0:
    f_stat, f_p = stats.friedmanchisquare(
        wide['A_browse'], wide['B_mixed'], wide['C_checkout'], wide['D_burst']
    )
    print(f"  Friedman χ² = {f_stat:.3f}, p = {f_p:.6f}")
    print(f"  Median error_rate per scenario:")
    for sc in SCENARIOS:
        print(f"    {sc}: {wide[sc].median():.4f}")
    # Wilcoxon paired tests: D_burst vs each steady scenario
    print(f"\n  Wilcoxon signed-rank, D_burst vs each steady:")
    wilcox_results = []
    for sc in ['A_browse', 'B_mixed', 'C_checkout']:
        try:
            w_stat, w_p = stats.wilcoxon(wide['D_burst'], wide[sc])
            wilcox_results.append({'comparison': f'D_burst vs {sc}',
                                  'wilcoxon_W': w_stat, 'p_value': w_p})
        except Exception as e:
            print(f"    {sc}: {e}")
    # Holm correction
    if wilcox_results:
        wdf = pd.DataFrame(wilcox_results)
        _, p_adj_w, _, _ = multipletests(wdf['p_value'].values, alpha=0.05, method='holm')
        wdf['p_adj_holm'] = p_adj_w
        wdf['significant'] = p_adj_w < 0.05
        print(wdf.round(6).to_string(index=False))
        wdf.to_csv('phase3_h4_wilcoxon.csv', index=False)

# ===================================================================
# 3.7 SUMMARY REPORT
# ===================================================================
summary = {
    'seed': SEED,
    'bootstrap_resamples': N_BOOT,
    'omnibus_tests': len(omnibus_df),
    'omnibus_significant_after_holm': int(omnibus_df['significant_after_holm'].sum()),
    'pairwise_tests': len(pairwise_df),
    'pairwise_significant_after_holm': int(pairwise_df['significant'].sum()),
    'effect_size_distribution': effect_df['magnitude'].value_counts().to_dict(),
    'bootstrap_cis_computed': int((ci_df['note'] == 'ok').sum()),
    'friedman_h4': {'statistic': float(f_stat), 'p_value': float(f_p)} if len(wide) > 0 else None
}

with open('phase3_summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

print("\n" + "=" * 70)
print("✓ PHASE 3 COMPLETE")
print("=" * 70)
print(f"  Omnibus tests (Kruskal-Wallis): {len(omnibus_df)}")
print(f"  Significant after Holm:         {omnibus_df['significant_after_holm'].sum()}")
print(f"  Pairwise tests (Dunn):          {len(pairwise_df)}")
print(f"  Significant pairwise:           {pairwise_df['significant'].sum()}")
print(f"  Bootstrap CIs computed:         {(ci_df['note'] == 'ok').sum()}")
print(f"  Files saved:")
print(f"    - phase3_omnibus_kruskal.csv")
print(f"    - phase3_pairwise_dunn_long.csv")
print(f"    - phase3_dunn_*.csv (4 scenario-specific matrices)")
print(f"    - phase3_cliffs_delta.csv")
print(f"    - phase3_bootstrap_ci_medians.csv")
print(f"    - phase3_h4_wilcoxon.csv")
print(f"    - phase3_summary.json")
