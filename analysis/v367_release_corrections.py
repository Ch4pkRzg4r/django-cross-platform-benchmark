#!/usr/bin/env python3
"""v367: thesis-defined descriptive H4 rule and legible Figure 4.3.

The v330 statistical source, canonical data and v360 estimands are unchanged.
This H4 predicate supersedes the frozen helper's median-of-A/B/C comparison.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.text import Text

FROZEN_SHA256 = '710b3a7a79d794425ac04254caba892419ad78f56cf4c174843e3c417c5ebde7'
SCENARIOS = ['A_browse', 'B_mixed', 'C_checkout', 'D_burst']
SELF_MANAGED = ['01_apache_modwsgi', '02_nginx_uwsgi', '03_django_gunicorn', '07_iis_waitress']
PROVIDER_MANAGED = ['04_aca', '05_koyeb', '06_flyio']

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def h4_by_platform(df):
    """Strictly D>A AND D>B AND D>C; no cross-scenario significance test."""
    med = df.groupby(['platform', 'scenario']).error_rate.median().unstack()
    rows = []
    for platform in SELF_MANAGED + PROVIDER_MANAGED:
        a, b, c, d = [float(med.loc[platform, s]) for s in SCENARIOS]
        rows.append(dict(platform=platform, A_median=a, B_median=b, C_median=c,
                         D_median=d, D_gt_A=d>a, D_gt_B=d>b, D_gt_C=d>c,
                         supported=d>a and d>b and d>c,
                         historical_median_ABC_rule=d>float(np.median([a,b,c]))))
    return pd.DataFrame(rows)

def _consistent_h4_supported(df):
    return bool(h4_by_platform(df).supported.all())

def family_gap(df):
    """Same Figure 4.3 estimand: median of platform cell medians per family."""
    med = df.groupby(['platform', 'scenario']).goodput_rps.median()
    rows = []
    for scenario in SCENARIOS:
        t = float(np.median([med.loc[p,scenario] for p in SELF_MANAGED]))
        m = float(np.median([med.loc[p,scenario] for p in PROVIDER_MANAGED]))
        rows.append(dict(scenario=scenario, self_managed_median=t,
                         provider_managed_median=m, relative_gap_pct=100*(m-t)/t))
    return pd.DataFrame(rows)

def draw_figure(gaps, out):
    # Exactly 450 pt wide: DOCX placement therefore does not reduce font sizes.
    plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':10.5,
                         'axes.labelsize':10.5, 'xtick.labelsize':10.5,
                         'ytick.labelsize':10.5, 'pdf.fonttype':42,
                         'svg.fonttype':'none'})
    fig, ax = plt.subplots(figsize=(450/72, 270/72), dpi=300)
    fig.subplots_adjust(left=.145, right=.985, bottom=.15, top=.81)
    vals = gaps.relative_gap_pct.to_numpy()
    ax.bar(range(4), vals, color='#1f77b4', width=.66)
    ax.axhline(0, color='#1f77b4', lw=.8)
    ax.set_ylim(-.75, .90)
    ax.set_yticks(np.arange(-.6, .81, .2))
    ax.set_axisbelow(True)
    ax.grid(axis='y', alpha=.22)
    ax.set_xticks(range(4), ['A. Browse', 'B. Mixed', 'C. Cart-path\nGET', 'D. Burst'])
    ax.set_ylabel('Relative goodput gap (%)')
    fig.suptitle('Relative callback-qualified goodput gap\nProvider-managed versus self-managed paths',
                 fontsize=11.5, fontweight='bold', y=.98)
    for i,v in enumerate(vals):
        # Preserve the thesis's one-decimal display, suppressing signed zero.
        label='0.0%' if round(float(v),1)==0 else f'{v:+.1f}%'
        ax.text(i, v+(.045 if v>=0 else -.045), label, ha='center',
                va='bottom' if v>=0 else 'top', fontsize=10.5, weight='bold')
    fig.canvas.draw()
    fonts=[]
    for obj in fig.findobj(Text):
        if obj.get_visible() and obj.get_text():
            box=obj.get_window_extent(fig.canvas.get_renderer())
            if box.x0 < -1 or box.y0 < -1 or box.x1 > fig.bbox.width+1 or box.y1 > fig.bbox.height+1:
                raise ValueError(f'Text outside figure canvas: {obj.get_text()}')
            fonts.append({'text':obj.get_text(), 'placed_font_pt':obj.get_fontsize()})
    assert min(x['placed_font_pt'] for x in fonts)>=10
    for ext in ['png','pdf','svg']:
        # Do not use bbox_inches=tight: it would change the physical scaling.
        fig.savefig(out/f'Figure_4_3_v367.{ext}', dpi=300)
    plt.close(fig)
    return {'placed_width_pt':450, 'placed_height_pt':270,
            'minimum_font_pt':min(x['placed_font_pt'] for x in fonts), 'text_objects':fonts}

def main():
    ap=argparse.ArgumentParser()
    repo=Path(__file__).resolve().parents[1]
    ap.add_argument('--master', type=Path, default=repo/'data/canonical/master_runs.csv')
    ap.add_argument('--out-dir', type=Path, default=repo/'.v367-run/release')
    args=ap.parse_args()
    if sha256(args.master)!=FROZEN_SHA256:
        raise SystemExit('Canonical SHA-256 mismatch; v367 requires the frozen thesis input.')
    df=pd.read_csv(args.master)
    assert df.shape==(280,39) and df.run_id.nunique()==280
    assert set(df.platform)==set(SELF_MANAGED+PROVIDER_MANAGED)
    assert set(df.scenario)==set(SCENARIOS)
    assert (df.groupby(['platform','scenario']).size()==10).all()
    out=args.out_dir;out.mkdir(parents=True,exist_ok=True)
    h4=h4_by_platform(df);gaps=family_gap(df)
    h4.to_csv(out/'v367_h4_descriptive.csv',index=False)
    gaps.to_csv(out/'v367_figure4_3_goodput_gap.csv',index=False)
    font_check=draw_figure(gaps,out)
    manifest={'release':'v367','canonical_sha256':FROZEN_SHA256,'canonical_shape':[280,39],
              'h4_rule':'For every platform, median(D)>median(A), median(D)>median(B), and median(D)>median(C).',
              'h4_overall_supported':_consistent_h4_supported(df),
              'historical_h4_overall_supported':bool(h4.historical_median_ABC_rule.all()),
              'platform_flags_changed':h4.loc[h4.supported!=h4.historical_median_ABC_rule,'platform'].tolist(),
              'figure_4_3_estimand':'100*(median_provider(cell medians)-median_self(cell medians))/median_self(cell medians)',
              'figure_font_check':font_check,'outputs':{}}
    for name in ['v367_h4_descriptive.csv','v367_figure4_3_goodput_gap.csv',
                 'Figure_4_3_v367.png','Figure_4_3_v367.pdf','Figure_4_3_v367.svg']:
        manifest['outputs'][name]={'sha256':sha256(out/name),'bytes':(out/name).stat().st_size}
    (out/'v367_release_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:v for k,v in manifest.items() if k not in ['outputs','figure_font_check']},indent=2))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
