#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ch4_evidence_pipeline.py -- Chapter 4 final-thesis mirror exhibit renderer (v154)
=============================================================================

This is the final thesis-mirror renderer for Chapter 4.  It replaces the older
v131 exhibit style with the final submission style used in the DOCX thesis:

* Tables keep the full platform-by-scenario evidence matrix but add a clear
  platform-family grouping (Traditional WSGI vs Managed container-based).
* Matrix metrics use annotated heatmaps where this is the clearest presentation.
* Group-level contrasts use grouped bar charts rather than older dumbbell plots.
* Error-rate, warm-up, burst, and post-idle figures use simpler summary-first
  designs that match the final thesis figures, including Table 4.7 summary and Tables 4.10-4.11.

Inputs for full reproducible mode:
    master_runs.csv                 280 rows x 39 fields
    warmup_transient.csv            steady scenario warm-up summaries
    timeseries_burst_recovery.csv   Scenario D per-second trace evidence
    coldstart_raw.csv               optional post-idle probe file

Fallback / preview mode:
    If master_runs.csv is unavailable but out_ch4_v131/exhibits/Table_4_*.csv
    exists, the script rebuilds the current-style figures from those existing
    exhibit tables. This is useful for checking presentation style, but the full
    reproducible run should use master_runs.csv.

Usage:
    python scripts/ch4_evidence_pipeline.py --data .
    python scripts/ch4_evidence_pipeline.py --data . --output out_ch4_v153
    python scripts/ch4_evidence_pipeline.py --from-existing-exhibits out_ch4_v131/exhibits
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import os
import sys
import textwrap
import warnings
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

# Windows UTF-8 safety ------------------------------------------------------
os.environ.setdefault("PYTHONUTF8", "1")
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize

try:
    from scipy import stats
    HAVE_SCIPY = True
except Exception:
    stats = None
    HAVE_SCIPY = False

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# Thesis constants and final display labels
# ---------------------------------------------------------------------------
SEED, NBOOT      = 20260603, 10_000
CENSOR_MS        = 59_000.0
APDEX_T, APDEX_F = 500, 2000
APDEX_THRESHOLD  = 0.85

RAW_PLATFORM_MAP = {
    "01_apache_modwsgi": "Apache + mod_wsgi",
    "02_nginx_uwsgi": "Nginx + uWSGI",
    "03_django_gunicorn": "Django + Gunicorn",
    "07_iis_waitress": "IIS + Waitress",
    "04_aca": "Azure Container Apps",
    "05_koyeb": "Koyeb",
    "06_flyio": "Fly.io",
    # also accept already-short platform names
    "Apache": "Apache + mod_wsgi",
    "Nginx": "Nginx + uWSGI",
    "Django": "Django + Gunicorn",
    "Gunicorn": "Django + Gunicorn",
    "IIS": "IIS + Waitress",
    "ACA": "Azure Container Apps",
    "Azure Container Apps": "Azure Container Apps",
    "Koyeb": "Koyeb",
    "Fly.io": "Fly.io",
    # legacy output labels
    "Apache+mod_wsgi": "Apache + mod_wsgi",
    "Nginx+uWSGI": "Nginx + uWSGI",
    "IIS+Waitress": "IIS + Waitress",
}
ORDER = [
    "Apache + mod_wsgi", "Nginx + uWSGI", "Django + Gunicorn", "IIS + Waitress",
    "Azure Container Apps", "Koyeb", "Fly.io"
]
TRAD = ORDER[:4]
MANAGED = ORDER[4:]
FAMILY = {p: "Traditional WSGI configurations" for p in TRAD}
FAMILY.update({p: "Managed container-based platforms" for p in MANAGED})
SCEN = ["A_browse", "B_mixed", "C_checkout", "D_burst"]
SC_SHORT = {"A_browse": "A", "B_mixed": "B", "C_checkout": "C", "D_burst": "D"}
SC_LABEL = {"A_browse": "A: Browse", "B_mixed": "B: Mixed", "C_checkout": "C: Cart-path GET", "D_burst": "D: Burst"}

# Final calm thesis palette -------------------------------------------------
NAVY = "#1f3a5b"
BLUE = "#2f6da3"
ORANGE = "#d9822b"
GREEN = "#3b8c3b"
RED = "#c33d3d"
PURPLE = "#7761a7"
BROWN = "#8c6d5a"
PINK = "#d76fb3"
TEAL = "#2b8c7e"
GREY = "#6f7b8a"
PLATFORM_COLOURS = {
    "Apache + mod_wsgi": BLUE,
    "Nginx + uWSGI": ORANGE,
    "Django + Gunicorn": GREEN,
    "IIS + Waitress": RED,
    "Azure Container Apps": PURPLE,
    "Koyeb": BROWN,
    "Fly.io": PINK,
}
SCEN_COLOURS = {"A_browse": BLUE, "B_mixed": ORANGE, "C_checkout": GREEN, "D_burst": PURPLE}

plt.rcParams.update({
    "figure.dpi": 140,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "font.family": "DejaVu Sans",
    "font.size": 10.5,
    "axes.titlesize": 12.5,
    "axes.labelsize": 11,
    "legend.fontsize": 9.5,
    "xtick.labelsize": 9.5,
    "ytick.labelsize": 9.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.linestyle": "-",
    "grid.color": "#d9d9d9",
    "grid.alpha": 0.75,
})

MANIFEST: List[Dict[str, str]] = []

# ---------------------------------------------------------------------------
# General helpers
# ---------------------------------------------------------------------------
def platform_display(x: str) -> str:
    return RAW_PLATFORM_MAP.get(str(x), str(x))

def scenario_sort_key(s: pd.Series) -> pd.Series:
    return s.map({v: i for i, v in enumerate(SCEN)}).fillna(999)

def platform_sort_key(s: pd.Series) -> pd.Series:
    return s.map({v: i for i, v in enumerate(ORDER)}).fillna(999)

def add_family_column(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "platform" in out.columns:
        out["platform"] = out["platform"].map(platform_display)
        fam = out["platform"].map(FAMILY).fillna("Other / derived summary")
        if "platform_family" in out.columns:
            out["platform_family"] = fam
        else:
            out.insert(0, "platform_family", fam)
    return out

def grouped_sort(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "scenario" in out.columns and "platform" in out.columns:
        out["platform"] = out["platform"].map(platform_display)
        return out.sort_values(["scenario", "platform"], key=lambda s: platform_sort_key(s) if s.name == "platform" else scenario_sort_key(s))
    if "platform" in out.columns:
        out["platform"] = out["platform"].map(platform_display)
        return out.sort_values("platform", key=platform_sort_key)
    return out

def note(kind: str, name: str, section: str, rq: str, source: str, purpose: str):
    MANIFEST.append({"exhibit": name, "kind": kind, "thesis_section": section,
                     "RQ_or_H": rq, "data_source": source, "purpose": purpose})

def md_grouped_table(df: pd.DataFrame, caption: str = "") -> str:
    work = df.copy()
    if caption:
        caption = f"**{caption}**\n\n"
    if "platform_family" not in work.columns:
        return caption + work.to_markdown(index=False)
    parts = [caption] if caption else []
    for fam, sub in work.groupby("platform_family", sort=False):
        parts.append(f"**{fam}**\n")
        sub = sub.drop(columns=["platform_family"])
        parts.append(sub.to_markdown(index=False))
        parts.append("\n")
    return "\n".join(parts).strip() + "\n"

def write_table(df: pd.DataFrame, name: str, out_dir: Path, section: str, rq: str,
                source: str, purpose: str, caption: str = "", group_platforms: bool = False):
    exhibits = out_dir / "exhibits"
    exhibits.mkdir(parents=True, exist_ok=True)
    work = df.copy()
    if group_platforms and "platform" in work.columns:
        work = add_family_column(work)
    work.to_csv(exhibits / f"{name}.csv", index=False, encoding="utf-8-sig")
    (exhibits / f"{name}.md").write_text(md_grouped_table(work, caption), encoding="utf-8")
    note("Table", name, section, rq, source, purpose)
    print(f"  [T] {name} ({len(work)} rows)")

def write_figure(fig: plt.Figure, name: str, out_dir: Path, section: str, rq: str,
                 source: str, purpose: str):
    exhibits = out_dir / "exhibits"
    exhibits.mkdir(parents=True, exist_ok=True)
    fig.savefig(exhibits / f"{name}.png")
    fig.savefig(exhibits / f"{name}.pdf")
    plt.close(fig)
    note("Figure", name, section, rq, source, purpose)
    print(f"  [F] {name}")

# ---------------------------------------------------------------------------
# Statistical helpers
# ---------------------------------------------------------------------------
def eps2_tomczak(H, k, n):
    return (H - k + 1) / (n - k)

def holm(p):
    p = np.asarray(p, float); m = len(p)
    idx = np.argsort(p); out = np.empty(m); run = 0.0
    for r, i in enumerate(idx):
        run = max(run, (m - r) * p[i]); out[i] = min(1.0, run)
    return out

def bh_fdr(p):
    p = np.asarray(p, float); m = len(p)
    idx = np.argsort(p); out = np.empty(m); prev = 1.0
    for r in range(m - 1, -1, -1):
        i = idx[r]; prev = min(prev, p[i] * m / (r + 1)); out[i] = prev
    return out

def dunn_pairwise(groups: Dict[str, np.ndarray]):
    if not HAVE_SCIPY:
        raise RuntimeError("scipy is required for Dunn/Holm inference tables")
    labels = list(groups)
    allv = np.concatenate([groups[g] for g in labels])
    N = len(allv)
    ranks = stats.rankdata(allv)
    pos, rbar, nn = 0, {}, {}
    for g in labels:
        n = len(groups[g]); rbar[g] = ranks[pos:pos+n].mean(); nn[g] = n; pos += n
    _, counts = np.unique(allv, return_counts=True)
    tie = ((counts ** 3 - counts).sum()) / (12.0 * (N - 1))
    base = N * (N + 1) / 12.0 - tie
    out = {}
    for i, a in enumerate(labels):
        for b in labels[i+1:]:
            se = math.sqrt(base * (1 / nn[a] + 1 / nn[b]))
            z = (rbar[a] - rbar[b]) / se
            out[(a, b)] = (z, 2 * stats.norm.sf(abs(z)))
    return out

def cliffs(a, b):
    if not HAVE_SCIPY:
        return np.nan
    u, _ = stats.mannwhitneyu(a, b, alternative="two-sided")
    return 2.0 * u / (len(a) * len(b)) - 1.0

def cliff_mag(d):
    ad = abs(float(d))
    return "negligible" if ad < 0.147 else "small" if ad < 0.33 else "medium" if ad < 0.474 else "large"

def boot_med_ci(x, seed_shift=0):
    rng = np.random.default_rng(SEED + seed_shift)
    x = np.asarray(x, float)
    m = np.median(rng.choice(x, size=(NBOOT, len(x)), replace=True), axis=1)
    return float(np.median(x)), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))

# ---------------------------------------------------------------------------
# Final thesis figure functions
# ---------------------------------------------------------------------------
def _format_value(v: float, fmt: str) -> str:
    if abs(v) >= 10000 and ("f" in fmt or "0" in fmt):
        return f"{v/1000:.1f}k"
    return fmt.format(v)

def annotated_heatmap(mat: pd.DataFrame, fmt: str, title: str, cbar_label: str,
                      log: bool = False, cmap: str = "Blues", mark: Optional[pd.DataFrame] = None,
                      vmin=None, vmax=None, footnote: str = "") -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10.3, 5.9))
    vals = mat.values.astype(float)
    if log:
        positive = vals[vals > 0]
        norm = LogNorm(vmin=vmin or max(positive.min(), 1e-9), vmax=vmax or positive.max())
    else:
        norm = Normalize(vmin=vmin if vmin is not None else np.nanmin(vals),
                         vmax=vmax if vmax is not None else np.nanmax(vals))
    im = ax.imshow(vals, aspect="auto", cmap=cmap, norm=norm)
    ax.set_xticks(range(mat.shape[1])); ax.set_xticklabels(mat.columns)
    ax.set_yticks(range(mat.shape[0])); ax.set_yticklabels(mat.index)
    ax.grid(False)
    ax.set_title(title, fontweight="bold", pad=12)
    ax.axhline(len(TRAD) - 0.5, color="#777777", lw=1.4)
    ax.text(-0.9, 1.5, "Traditional", rotation=90, va="center", ha="center", fontsize=9.3, fontweight="bold", color="#555555")
    ax.text(-0.9, 5.0, "Managed", rotation=90, va="center", ha="center", fontsize=9.3, fontweight="bold", color="#555555")
    for i in range(vals.shape[0]):
        for j in range(vals.shape[1]):
            v = vals[i, j]
            s = _format_value(v, fmt)
            if mark is not None and bool(mark.iloc[i, j]):
                s += "*"
            rgba = im.cmap(im.norm(v))
            lum = 0.299*rgba[0] + 0.587*rgba[1] + 0.114*rgba[2]
            ax.text(j, i, s, ha="center", va="center", fontsize=8.8,
                    fontweight="bold", color="black" if lum > 0.55 else "white")
    cb = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
    cb.set_label(cbar_label)
    if footnote:
        fig.text(0.5, 0.012, footnote, ha="center", va="bottom", fontsize=8.5)
        fig.tight_layout(rect=(0.045, 0.045, 0.98, 0.96))
    else:
        fig.tight_layout(rect=(0.045, 0.02, 0.98, 0.96))
    return fig

def grouped_contrast_bar(table9: pd.DataFrame, outcome: str, title: str, y_label: str,
                         value_fmt: str = "{:.1f}", suffix: str = "") -> plt.Figure:
    tcol = [c for c in table9.columns if c.startswith("Traditional")][0]
    mcol = [c for c in table9.columns if c.startswith("Managed")][0]
    sub = table9[table9["Outcome"] == outcome].copy()
    x = np.arange(len(sub))
    w = 0.34
    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    ax.bar(x - w/2, sub[tcol], width=w, color=BLUE, label="Traditional WSGI")
    ax.bar(x + w/2, sub[mcol], width=w, color=TEAL, label="Managed container")
    for xx, val in zip(x - w/2, sub[tcol]):
        ax.text(xx, val, value_fmt.format(val) + suffix, ha="center", va="bottom", fontsize=8.8)
    for xx, val in zip(x + w/2, sub[mcol]):
        ax.text(xx, val, value_fmt.format(val) + suffix, ha="center", va="bottom", fontsize=8.8)
    ax.set_xticks(x); ax.set_xticklabels([f"Scenario {s}" for s in sub["Scen."]])
    ax.set_ylabel(y_label)
    ax.set_title(title, fontweight="bold")
    ax.legend(frameon=False, ncol=2, loc="upper center")
    ax.grid(axis="y"); ax.set_axisbelow(True)
    fig.tight_layout()
    return fig

def error_rate_scenario_bars(T3: pd.DataFrame) -> plt.Figure:
    T3 = T3.copy(); T3["platform"] = T3["platform"].map(platform_display)
    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.8), sharex=True)
    axes = axes.ravel()
    xmax = max(T3["error_%"].max() * 1.18, 0.1)
    for ax, sc in zip(axes, SCEN):
        sub = T3[T3["scenario"] == sc].sort_values("platform", key=platform_sort_key)
        colours = [PLATFORM_COLOURS[p] for p in sub["platform"]]
        y = np.arange(len(sub))
        ax.barh(y, sub["error_%"], color=colours)
        ax.set_yticks(y); ax.set_yticklabels(sub["platform"])
        ax.invert_yaxis(); ax.set_xlim(0, xmax)
        ax.set_title(SC_LABEL[sc], fontsize=11, fontweight="bold")
        ax.axhline(3.5, color="#808080", lw=0.8)
        for yi, v in zip(y, sub["error_%"]):
            ax.text(v + xmax*0.012, yi, f"{v:.3f}%", va="center", fontsize=8.4)
        ax.grid(axis="x"); ax.set_axisbelow(True)
    fig.suptitle("Median callback-defined error rate by scenario", fontweight="bold", y=0.995)
    fig.text(0.5, 0.015, "Error rate (%)", ha="center", fontsize=10)
    fig.tight_layout(rect=(0.02, 0.035, 0.98, 0.96))
    return fig

def warmup_two_panel(T5: pd.DataFrame) -> plt.Figure:
    T5 = T5.copy(); T5["platform"] = T5["platform"].map(platform_display)
    fig, axes = plt.subplots(1, 2, figsize=(12.2, 5.3), sharex=True)
    for ax, group, title in [(axes[0], TRAD, "Traditional WSGI configurations"), (axes[1], MANAGED, "Managed container-based platforms")]:
        sub = T5[T5["platform"].isin(group)]
        y = np.arange(len(group))
        h = 0.24
        for idx, sc in enumerate(["A_browse", "B_mixed", "C_checkout"]):
            vals = []
            for p in group:
                match = sub[(sub["platform"] == p) & (sub["scenario"] == sc)]["ratio_first30s_over_later"]
                vals.append(float(match.iloc[0]) if len(match) else np.nan)
            yy = y + (idx - 1)*h
            ax.barh(yy, vals, height=h, color=SCEN_COLOURS[sc], label=SC_LABEL[sc])
            for v, yv in zip(vals, yy):
                ax.text(v + 0.015, yv, f"{v:.1f}", va="center", ha="left", fontsize=8.4)
        ax.set_yticks(y); ax.set_yticklabels(group)
        ax.invert_yaxis()
        ax.axvline(1.0, color="#333333", lw=1.2, linestyle="--")
        ax.grid(axis="x"); ax.set_axisbelow(True)
        ax.set_xlim(0, 1.28)
        ax.set_title(title, fontweight="bold")
    axes[0].set_xlabel("Warm-up ratio = first 30 s p95 / later p95")
    axes[1].set_xlabel("Warm-up ratio = first 30 s p95 / later p95")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 1.02))
    fig.suptitle("Warm-up ratio by platform across steady scenarios A–C", fontweight="bold", y=1.08)
    fig.tight_layout(rect=(0.02, 0.02, 0.98, 0.96))
    return fig

def burst_phase_summary(T6: pd.DataFrame) -> plt.Figure:
    """Final thesis Figure 4.9: line-based phase summary, not grouped bars.

    This mirrors the final DOCX design: Traditional and managed platform families
    are separated into two stacked panels; each platform is a line across four
    phase-level values from Table 4.6.
    """
    T6 = T6.copy(); T6["platform"] = T6["platform"].map(platform_display)
    base_col = [c for c in T6.columns if c.startswith("baseline_p95")][0]
    peak_col = [c for c in T6.columns if c.startswith("peak_phase_p95")][0]
    max_col = [c for c in T6.columns if c.startswith("peak_phase_max")][0]
    post_col = [c for c in T6.columns if c.startswith("post_ramp")][0]
    phases = [(base_col, "Baseline p95"), (peak_col, "Peak p95"), (max_col, "Peak max p95"), (post_col, "Post-ramp p95")]
    x = np.arange(len(phases))
    markers = ["o", "s", "^", "D", "P", "X", "v"]
    fig, axes = plt.subplots(2, 1, figsize=(10.6, 5.6), sharex=True, sharey=True)
    for ax, group, title, letter in [(axes[0], TRAD, "Traditional platforms", "A"), (axes[1], MANAGED, "Managed platforms", "B")]:
        sub = T6[T6["platform"].isin(group)].sort_values("platform", key=platform_sort_key)
        for idx, (_, r) in enumerate(sub.iterrows()):
            p = r["platform"]
            vals = [float(r[c]) for c, _ in phases]
            ax.plot(x, vals, marker=markers[(ORDER.index(p)) % len(markers)], lw=2.0,
                    ms=6.0, color=PLATFORM_COLOURS.get(p, "#444444"), label=p)
        ax.set_yscale("log")
        ax.grid(axis="y", which="major", color="#d0d0d0", linewidth=0.9)
        ax.grid(axis="y", which="minor", color="#ececec", linewidth=0.6, alpha=0.55)
        ax.grid(axis="x", visible=False)
        ax.text(0.0, 1.10, f"{letter}  {title}", transform=ax.transAxes,
                fontsize=13.5, fontweight="bold", va="bottom")
        ax.legend(frameon=False, ncol=len(group), loc="upper right", bbox_to_anchor=(1.0, 1.17))
        ax.set_axisbelow(True)
    axes[1].set_xticks(x); axes[1].set_xticklabels([lab for _, lab in phases])
    fig.supylabel("p95 latency (ms, log scale)", x=0.015, fontsize=11.5)
    fig.suptitle("Scenario D burst phase-level p95 summary", fontweight="bold", fontsize=15.5, y=0.995)
    # Emphasise the same two maxima highlighted in the thesis figure.
    try:
        g = T6[T6["platform"] == "Django + Gunicorn"].iloc[0]
        axes[0].annotate(f"Gunicorn peak max\n{float(g[max_col]):,.0f} ms", xy=(2, float(g[max_col])), xytext=(1.25, float(g[max_col])*0.65),
                         arrowprops=dict(arrowstyle="->", color=PLATFORM_COLOURS["Django + Gunicorn"], lw=1.4),
                         fontsize=9.2, color=PLATFORM_COLOURS["Django + Gunicorn"], ha="center")
    except Exception:
        pass
    try:
        f = T6[T6["platform"] == "Fly.io"].iloc[0]
        axes[1].annotate(f"Fly.io peak max\n{float(f[max_col]):,.0f} ms", xy=(2, float(f[max_col])), xytext=(2.55, float(f[max_col])*1.6),
                         arrowprops=dict(arrowstyle="->", color=PLATFORM_COLOURS["Fly.io"], lw=1.4),
                         fontsize=9.2, color=PLATFORM_COLOURS["Fly.io"], ha="center")
    except Exception:
        pass
    fig.text(0.5, 0.012,
             'Exact values are from Table 4.6. “Peak max p95” is the largest observed per-second p95 in the peak window; Table 4.6 separately retains seconds with p95 > 1 s.',
             ha="center", fontsize=8.7)
    fig.tight_layout(rect=(0.04, 0.055, 0.98, 0.95))
    return fig

def _as_float_maybe(x) -> float:
    if pd.isna(x):
        return float("nan")
    s = str(x).replace(",", "").replace("x", "").replace("×", "").strip()
    try:
        return float(s)
    except Exception:
        return float("nan")

def _fmt1_half_up(x: float) -> str:
    from decimal import Decimal, ROUND_HALF_UP
    if pd.isna(x):
        return ""
    d = Decimal(str(float(x))).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    return f"{d:,.1f}"

def post_idle_summary_table(T7_raw: pd.DataFrame) -> pd.DataFrame:
    """Final thesis Table 4.7: one summary row per managed platform.

    Accepts either the raw 15-attempt table (attempt, first_after_idle_ms,
    immediate_warm_repeat_ms, valid) or an already summarised thesis-style table.
    """
    T = T7_raw.copy()
    # Already summary-style from the final thesis.
    if "Attempted / valid pairs" in T.columns:
        return T[["Platform", "Attempted / valid pairs", "First request p50 (ms)", "Warm repeat p50 (ms)", "Median paired multiplier", "Boundary"]]
    T["platform"] = T["platform"].map(platform_display)
    if "valid" not in T.columns:
        T["valid"] = True
    T["valid_bool"] = T["valid"].astype(str).str.lower().isin(["true", "1", "yes"])
    rows = []
    short = {"Azure Container Apps": "ACA", "Koyeb": "Koyeb", "Fly.io": "Fly.io"}
    for p in MANAGED:
        g = T[T["platform"] == p]
        if len(g) == 0:
            continue
        gv = g[g["valid_bool"]]
        attempted, valid = len(g), len(gv)
        first = float(gv["first_after_idle_ms"].median()) if len(gv) else float("nan")
        warm = float(gv["immediate_warm_repeat_ms"].median()) if len(gv) else float("nan")
        mult = float((gv["first_after_idle_ms"].astype(float) / gv["immediate_warm_repeat_ms"].astype(float)).median()) if len(gv) else float("nan")
        if valid == attempted:
            boundary = "All valid pairs: first > warm"
        else:
            boundary = "One failed pair; all valid first > warm"
        rows.append({
            "Platform": short.get(p, p),
            "Attempted / valid pairs": f"{attempted} / {valid}",
            "First request p50 (ms)": _fmt1_half_up(first),
            "Warm repeat p50 (ms)": _fmt1_half_up(warm),
            "Median paired multiplier": f"{_fmt1_half_up(mult)}x",
            "Boundary": boundary,
        })
    return pd.DataFrame(rows)

def post_idle_grouped_bars(T7: pd.DataFrame) -> plt.Figure:
    """Final thesis Figure 4.10: grouped median bars from the summary table."""
    S = post_idle_summary_table(T7)
    if S.empty:
        fig, ax = plt.subplots(figsize=(9.6, 5.0)); ax.text(0.5,0.5,"No post-idle probe data",ha="center"); return fig
    labels = [f"{r['Platform']} ({r['Attempted / valid pairs']})" for _, r in S.iterrows()]
    first = np.array([_as_float_maybe(v) for v in S["First request p50 (ms)"]], dtype=float)
    warm = np.array([_as_float_maybe(v) for v in S["Warm repeat p50 (ms)"]], dtype=float)
    mult = list(S["Median paired multiplier"])
    fig, ax = plt.subplots(figsize=(10.2, 6.0))
    y = np.arange(len(S)); h = 0.32
    ax.barh(y + h/2, first, height=h, color="#c96f29", label="First request p50")
    ax.barh(y - h/2, warm, height=h, color=BLUE, label="Immediate warm repeat p50")
    ax.set_xscale("log")
    ax.set_yticks(y); ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel("Latency (ms, log scale)")
    ax.set_title("Post-idle first-request probe: platform-level median latencies", fontweight="bold")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="x"); ax.set_axisbelow(True)
    xmax = max(np.nanmax(first)*1.8, 3000)
    ax.set_xlim(max(80, np.nanmin(warm)*0.65), xmax)
    for yi, f, w, m in zip(y, first, warm, mult):
        ax.text(f*1.05, yi + h/2, f"{f:,.1f} ms", va="center", fontsize=8.6, color="#c96f29")
        ax.text(w*1.08, yi - h/2, f"{w:,.1f} ms", va="center", fontsize=8.6, color=BLUE)
        ax.text(max(f, w)*1.45, yi, m, va="center", fontsize=9.6, fontweight="bold", color="#333333")
    fig.text(0.5, 0.012,
             "Bars summarise Table 4.7: median first request after the 360-second no-probe interval versus the immediate warm repeat. The rightmost label shows the median paired multiplier.",
             ha="center", fontsize=8.5)
    fig.tight_layout(rect=(0.02, 0.045, 0.98, 0.96))
    return fig

def bootstrap_ci_figure(ci_rows: pd.DataFrame) -> plt.Figure:
    fig, axes = plt.subplots(2, 2, figsize=(11.8, 7.4), sharey=True)
    axes = axes.ravel()
    for ax, sc in zip(axes, ["A", "B", "C", "D"]):
        sub = ci_rows[ci_rows["Scen."] == sc].copy()
        sub["platform"] = sub["platform"].map(platform_display)
        sub = sub.sort_values("platform", key=platform_sort_key)
        x = np.arange(len(sub))
        y = sub["median_p95_ms"].astype(float).values
        lo = sub["ci_low"].astype(float).values
        hi = sub["ci_high"].astype(float).values
        colours = [PLATFORM_COLOURS[p] for p in sub["platform"]]
        ax.errorbar(x, y, yerr=[y-lo, hi-y], fmt="o", color="#333333", ecolor="#555555", capsize=3)
        ax.scatter(x, y, s=45, c=colours, zorder=3)
        ax.set_xticks(x); ax.set_xticklabels(sub["platform"], rotation=35, ha="right", fontsize=8)
        ax.set_title(f"Scenario {sc}", fontweight="bold")
        ax.set_yscale("log")
        ax.grid(axis="y")
    axes[0].set_ylabel("p95 median latency (ms, log scale)\n95% bootstrap CI")
    axes[2].set_ylabel("p95 median latency (ms, log scale)\n95% bootstrap CI")
    fig.suptitle(f"Replication-level p95 medians with 95% percentile bootstrap CIs (R = {NBOOT:,})", fontweight="bold")
    fig.tight_layout(rect=(0.02, 0.02, 0.98, 0.94))
    return fig

# ---------------------------------------------------------------------------
# Full mode from raw master files
# ---------------------------------------------------------------------------

def final_table_410(out_dir: Path) -> pd.DataFrame:
    """Final thesis Table 4.10 values retained as scoped Linux Docker-statistics summary."""
    T10 = pd.DataFrame([
        ["Apache + mod_wsgi", 7.3, 10.3, 162, "7.9%"],
        ["Nginx + uWSGI", 7.1, 10.4, 185, "9.0%"],
        ["Django + Gunicorn", 8.9, 12.8, 129, "6.3%"],
    ], columns=["Platform", "Median run-average CPU (%)", "Median run p95 CPU (%)", "Median run-average memory (MiB)", "Memory share of 2 GiB cap"])
    write_table(T10, "Table_4_10", out_dir, "4.7", "RQ5", "docker_stats retained Linux trio summary", "Scoped Linux container resource summary", "Table 4.10. Scoped Linux container resource summary across 40 retained runs per configuration (descriptive; no cross-platform resource comparison).")
    return T10

def final_table_411(out_dir: Path) -> pd.DataFrame:
    """Final thesis Table 4.11 values: stated warm-cost model."""
    T11 = pd.DataFrame([
        ["Fly.io", "11.39", "18.75", "0.231", "Modelled warm-cost input; not current invoice data."],
        ["Koyeb", "21.43", "17.83", "0.457", "Modelled warm-cost input; current pricing must be revalidated."],
        ["Nginx + uWSGI", "96.98", "18.92", "1.951", "Azure VM plus storage model."],
        ["Django + Gunicorn", "96.98", "18.57", "1.987", "Azure VM plus storage model."],
        ["Apache + mod_wsgi", "96.98", "17.63", "2.094", "Azure VM plus storage model; saturated cells require caution."],
        ["Azure Container Apps", "157.68", "18.60", "3.225", "Warm 24/7 model; provider billing/lifecycle not independently verified."],
        ["IIS + Waitress", "173.71", "18.88", "3.500", "Windows VM plus storage model."],
    ], columns=["Platform", "Monthly USD", "Median goodput", "USD / 1M successful", "Scope boundary"])
    write_table(T11, "Table_4_11", out_dir, "4.7", "RQ6,H3", "stated 2026 warm-cost assumptions", "Warm-cost efficiency model", "Table 4.11. Modelled warm-cost efficiency under stated 2026 assumptions (USD ex-VAT; conditional decision-support evidence).")
    return T11

def run_full(data_dir: Path, out_dir: Path):
    print("\n=== FULL REPRODUCIBLE MODE: raw CSVs -> final thesis exhibits ===")
    out_dir.mkdir(parents=True, exist_ok=True)
    for sub in ["exhibits", "evidence", "templates"]:
        (out_dir / sub).mkdir(exist_ok=True)

    df = pd.read_csv(data_dir / "master_runs.csv")
    df["platform"] = df["platform"].map(platform_display)
    df = df[df["platform"].isin(ORDER)].copy()
    df["error_pct"] = 100 * df["error_rate"]
    df["censored"] = (df["latency_p99"] >= CENSOR_MS).astype(int)
    df["tail_ratio_p99_p50"] = df["latency_p99"] / df["latency_p50"]

    wu = pd.read_csv(data_dir / "warmup_transient.csv")
    wu["platform"] = wu["platform"].map(platform_display)
    ts = pd.read_csv(data_dir / "timeseries_burst_recovery.csv")
    ts["platform"] = ts["platform"].map(platform_display)

    probe_path = None
    for c in ["coldstart_raw.csv", "postidle_probe.csv", "post_idle_probe.csv", "postidle_raw.csv"]:
        if (data_dir / c).exists():
            probe_path = data_dir / c
            break
    probe = None
    if probe_path:
        probe = pd.read_csv(probe_path)
        probe["platform"] = probe["platform"].map(platform_display)
        print(f"  post-idle probe file: {probe_path.name}")

    cellmed = df.groupby(["scenario", "platform"], as_index=False).median(numeric_only=True)

    # Table 4.1 ----------------------------------------------------------------
    T1 = pd.DataFrame([
        ["Retained design", "280 observations; 7 configurations × 4 scenarios × 10 replications", "Primary evidence base for Chapters 4–6."],
        ["Primary endpoints", "p95 latency, callback-defined goodput, error rate and Apdex", "Scenario-stratified descriptive and inferential analysis."],
        ["Tail endpoints", "p99 secondary; p99.9 appendix-only", "p99 is flagged where timeout-censoring occurs."],
        ["Diagnostic transport fields", "DNS unavailable; TLS non-discriminating; TCP limited", "Not reported as primary comparative outcomes."],
        ["Temporal summaries", f"Warm-up: {len(wu[wu.scenario != 'D_burst'])} A–C summaries; burst: {len(ts):,} second-level trace rows", "Descriptive evidence only; not replication-level inference."],
        ["Post-idle health-probe data", f"{len(probe) if probe is not None else 0} attempted pairs" if probe is not None else "not present in this run", "Supplementary descriptive H2 evidence; separate from the 280-run matrix."],
        ["Execution chronology", "Platform runs collected in time blocks over the study window", "Residual time/provider variation cannot be fully separated from configuration effects."],
    ], columns=["Evidence component", "Retained record", "Use in this chapter"])
    write_table(T1, "Table_4_01", out_dir, "4.1", "scope", "design", "Retained evidence design and analytical comparison boundaries", "Table 4.1. Retained evidence design and analytical comparison boundaries.")

    # Table 4.2 + Figs 4.1-4.3 -----------------------------------------------
    rows = []
    for (sc, pl), g in df.groupby(["scenario", "platform"]):
        rows.append({"scenario": sc, "platform": pl,
                     "p50_ms": g.latency_p50.median(),
                     "p95_ms": g.latency_p95.median(),
                     "p95_IQR": g.latency_p95.quantile(.75) - g.latency_p95.quantile(.25),
                     "p99_ms": g.latency_p99.median(),
                     "p99/p50": g.tail_ratio_p99_p50.median(),
                     "censored_reps_of_10": int(g.censored.sum())})
    T2 = grouped_sort(pd.DataFrame(rows)).round({"p50_ms": 1, "p95_ms": 1, "p95_IQR": 1, "p99_ms": 1, "p99/p50": 1})
    write_table(T2, "Table_4_02", out_dir, "4.2", "RQ1", "master_runs latency columns", "Category I latency and tail matrix", "Table 4.2. Category I matrix: median latency and tail indicators from 10 retained replications per platform-scenario cell. Rows are grouped by platform family.", True)
    make_latency_figures(T2, out_dir)

    # Table 4.3 + Figs 4.4-4.7 ------------------------------------------------
    rows = []
    for (sc, pl), g in df.groupby(["scenario", "platform"]):
        rows.append({"scenario": sc, "platform": pl,
                     "goodput_RPS": g.goodput_rps.median(),
                     "actual_RPS": g.rps_actual.median(),
                     "error_%": g.error_pct.median(),
                     "apdex": g.apdex_t500_f2000.median(),
                     "apdex_margin_vs_0.85": g.apdex_t500_f2000.median() - APDEX_THRESHOLD})
    T3 = grouped_sort(pd.DataFrame(rows)).round({"goodput_RPS": 2, "actual_RPS": 2, "error_%": 3, "apdex": 4, "apdex_margin_vs_0.85": 4})
    write_table(T3, "Table_4_03", out_dir, "4.3", "RQ2,RQ3,RQ4", "master_runs delivery/reliability/Apdex columns", "Category II delivery, reliability and Apdex matrix", "Table 4.3. Category II matrix: delivery, callback-defined reliability and Apdex from 10 retained replications per platform-scenario cell. Rows are grouped by platform family.", True)
    make_delivery_figures(T3, T2, out_dir)

    # Table 4.4 ----------------------------------------------------------------
    dAC = df[df.scenario != "D_burst"]
    rows = []
    for (sc, pl), g in dAC.groupby(["scenario", "platform"]):
        rows.append({"scenario": sc, "platform": pl,
                     "waiting_p50_ms": g.waiting_p50.median(),
                     "waiting_p95_ms": g.waiting_p95.median(),
                     "latency_CV": g.latency_cv.median(),
                     "transfer_p50_ms(p50−waiting_p50)": (g.latency_p50 - g.waiting_p50).median(),
                     "bandwidth_rx_kbps": g.bandwidth_rx_bps.median() / 1000})
    T4 = grouped_sort(pd.DataFrame(rows)).round(2)
    write_table(T4, "Table_4_04", out_dir, "4.4", "diagnostic", "master_runs waiting_*, latency_cv, bandwidth columns", "Client-path diagnostic matrix", "Table 4.4. Category III client-path diagnostic matrix: retained waiting, variability and transfer fields. Rows are grouped by platform family.", True)

    # Table 4.5 + Figure 4.8 --------------------------------------------------
    T5 = (wu[wu.scenario != "D_burst"].rename(columns={"p95_first30s": "p95_first_30s_ms", "p95_steady": "p95_later_ms", "warmup_ratio": "ratio_first30s_over_later"}))
    T5 = grouped_sort(T5).round(2)
    write_table(T5, "Table_4_05", out_dir, "4.5", "RQ5", "warmup_transient.csv", "Warm-up first-30 s vs later p95", "Table 4.5. Warm-up evidence for steady scenarios A–C: first-30-second p95 compared with later retained p95 summary. Rows are grouped by platform family.", True)
    write_figure(warmup_two_panel(T5), "Figure_4_08", out_dir, "4.5", "RQ5", "Table 4.5", "Two-panel warm-up ratio summary")

    # Table 4.6 + Figure 4.9 --------------------------------------------------
    rows = []
    for pl, g in ts.groupby("platform"):
        g = g.sort_values("second").set_index("second")
        base = g.loc[60:300, "p95_ms"]
        peak = g.loc[360:960, "p95_ms"]
        post = g.loc[1020:, "p95_ms"]
        rows.append({"platform": pl,
                     "baseline_p95_ms(60–300s)": base.median(),
                     "peak_phase_p95_ms(360–960s)": peak.median(),
                     "peak_phase_max_p95_ms": peak.max(),
                     "post_ramp_p95_ms(≥1020s)": post.median(),
                     "seconds_p95>1000ms(whole run)": int((g.p95_ms > 1000).sum()),
                     "peak_rate_RPS(360–960s)": g.loc[360:960, "rps"].median()})
    T6 = grouped_sort(pd.DataFrame(rows)).round(1)
    write_table(T6, "Table_4_06", out_dir, "4.5", "RQ5,H4", "timeseries_burst_recovery.csv", "Scenario D burst trace summary", "Table 4.6. Scenario D burst trace summary (descriptive second-level evidence; extreme tails retained, not clipped). Rows are grouped by platform family.", True)
    write_figure(burst_phase_summary(T6), "Figure_4_09", out_dir, "4.5", "RQ5,H4", "Table 4.6", "Scenario D phase-level burst summary")

    # Table 4.7 + Figure 4.10 -------------------------------------------------
    if probe is not None:
        probe["valid"] = (probe.cold_ms > 0) & (probe.warm_ms > 0)
        T7_raw = probe.rename(columns={"sample": "attempt", "cold_ms": "first_after_idle_ms", "warm_ms": "immediate_warm_repeat_ms", "penalty": "ratio_first/warm"})
        T7_raw = T7_raw[["platform", "attempt", "first_after_idle_ms", "immediate_warm_repeat_ms", "ratio_first/warm", "valid"]]
        T7 = post_idle_summary_table(T7_raw)
        write_table(T7, "Table_4_07", out_dir, "4.5", "H2", str(probe_path.name), "Supplementary post-idle first-request probe", "Table 4.7. Supplementary post-idle first-request probe for managed platforms (paired /health/ requests).")
        write_figure(post_idle_grouped_bars(T7), "Figure_4_10", out_dir, "4.5", "H2", "Table 4.7", "Grouped median post-idle probe summary")
        # Retain raw attempts as evidence, without giving them a main-table number.
        (out_dir / "evidence").mkdir(exist_ok=True)
        T7_raw.round(3).to_csv(out_dir / "evidence" / "E5_post_idle_probe_raw_attempts.csv", index=False, encoding="utf-8-sig")
        note("Evidence", "E5_post_idle_probe_raw_attempts", "4.5", "H2", str(probe_path.name), "Raw post-idle paired attempts backing Table 4.7 and Figure 4.10")

    # Inference tables and Figure 4.11 ---------------------------------------
    if HAVE_SCIPY:
        build_inference_and_synthesis(df, T2, T3, out_dir)
    else:
        print("  [warn] scipy not available; inference tables/Figure 4.11 not regenerated")

    write_manifest_and_report(out_dir, mode="full")

# ---------------------------------------------------------------------------
# Figures and inference sections shared by full/preview mode
# ---------------------------------------------------------------------------
def make_latency_figures(T2: pd.DataFrame, out_dir: Path):
    base = T2.copy(); base["platform"] = base["platform"].map(platform_display)
    piv95 = base.pivot(index="platform", columns="scenario", values="p95_ms").reindex(ORDER)[SCEN]
    piv95.columns = [SC_LABEL[c] for c in piv95.columns]
    write_figure(annotated_heatmap(piv95, "{:.1f}", "Median p95 latency by platform and scenario", "Latency (ms, log scale)", log=True, cmap="Blues", footnote="Annotated values are exact medians; colour intensity uses a log scale for the wide latency range."), "Figure_4_01", out_dir, "4.2", "RQ1", "Table 4.2 p95 column", "Primary latency endpoint matrix")
    piv99 = base.pivot(index="platform", columns="scenario", values="p99_ms").reindex(ORDER)[SCEN]
    cens = base.pivot(index="platform", columns="scenario", values="censored_reps_of_10").reindex(ORDER)[SCEN] > 0
    piv99.columns = cens.columns = [SC_LABEL[c] for c in SCEN]
    write_figure(annotated_heatmap(piv99, "{:.1f}", "Median p99 latency by platform and scenario", "Latency (ms, log scale)", log=True, cmap="Purples", mark=cens, footnote="* indicates one or more timeout-censored replications; displayed p99 is therefore a lower-bound indicator."), "Figure_4_02", out_dir, "4.2", "RQ1", "Table 4.2 p99 + censor flags", "Secondary tail endpoint with censoring markers")

    T9 = compute_group_contrast_from_tables(T2, None)
    write_figure(grouped_contrast_bar(T9, "p95 latency (ms)", "Balanced descriptive p95 contrast by scenario", "Balanced median p95 latency (ms)", "{:.1f}"), "Figure_4_03", out_dir, "4.2", "RQ1", "cell medians (Table 4.2)", "Group-level descriptive p95 contrast")

def make_delivery_figures(T3: pd.DataFrame, T2: Optional[pd.DataFrame], out_dir: Path):
    base = T3.copy(); base["platform"] = base["platform"].map(platform_display)
    piv = base.pivot(index="platform", columns="scenario", values="goodput_RPS").reindex(ORDER)[SCEN]
    piv.columns = [SC_LABEL[c] for c in SCEN]
    write_figure(annotated_heatmap(piv, "{:.2f}", "Median callback-defined goodput by platform and scenario", "Goodput (requests/s)", cmap="Greens", footnote="Goodput counts successful callback-defined requests per second."), "Figure_4_04", out_dir, "4.3", "RQ2", "Table 4.3 goodput_RPS", "Goodput endpoint matrix")
    write_figure(error_rate_scenario_bars(base), "Figure_4_05", out_dir, "4.3", "RQ3", "Table 4.3 error_%", "Scenario-wise callback-defined error-rate summary")
    piv = base.pivot(index="platform", columns="scenario", values="apdex").reindex(ORDER)[SCEN]
    piv.columns = [SC_LABEL[c] for c in SCEN]
    write_figure(annotated_heatmap(piv, "{:.3f}", "Median Apdex by platform and scenario", "Apdex", cmap="YlGnBu", vmin=0.93, vmax=1.0, footnote=f"Study thresholds: T = {APDEX_T} ms and F = {APDEX_F} ms; operational boundary = {APDEX_THRESHOLD}."), "Figure_4_06", out_dir, "4.3", "RQ4", "Table 4.3 apdex", "Apdex endpoint matrix")
    T9 = compute_group_contrast_from_tables(T2, T3) if T2 is not None else compute_group_contrast_from_tables(None, T3)
    write_figure(grouped_contrast_bar(T9, "Callback-defined goodput (RPS)", "Balanced descriptive goodput contrast by scenario", "Balanced median goodput (requests/s)", "{:.2f}"), "Figure_4_07", out_dir, "4.3", "RQ2", "cell medians (Table 4.3)", "Group-level goodput contrast")

def compute_group_contrast_from_tables(T2: Optional[pd.DataFrame], T3: Optional[pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for sc in SCEN:
        if T2 is not None:
            sub = T2[T2["scenario"] == sc].copy(); sub["platform"] = sub["platform"].map(platform_display)
            rows.append({"Scen.": SC_SHORT[sc], "Outcome": "p95 latency (ms)",
                         "Traditional (median of 4 cell medians)": sub[sub.platform.isin(TRAD)]["p95_ms"].median(),
                         "Managed (median of 3 cell medians)": sub[sub.platform.isin(MANAGED)]["p95_ms"].median()})
        if T3 is not None:
            sub = T3[T3["scenario"] == sc].copy(); sub["platform"] = sub["platform"].map(platform_display)
            for col, outcome in [("goodput_RPS", "Callback-defined goodput (RPS)"), ("error_%", "Error rate"), ("apdex", f"Apdex (T={APDEX_T} ms; F={APDEX_F} ms)")]:
                rows.append({"Scen.": SC_SHORT[sc], "Outcome": outcome,
                             "Traditional (median of 4 cell medians)": sub[sub.platform.isin(TRAD)][col].median(),
                             "Managed (median of 3 cell medians)": sub[sub.platform.isin(MANAGED)][col].median()})
    out = pd.DataFrame(rows)
    if len(out):
        out["Δ (Trad − Managed)"] = out["Traditional (median of 4 cell medians)"] - out["Managed (median of 3 cell medians)"]
    return out

def build_inference_and_synthesis(df: pd.DataFrame, T2: pd.DataFrame, T3: pd.DataFrame, out_dir: Path):
    outcomes = [("latency_p95", "p95 latency (ms)"), ("goodput_rps", "Callback-defined goodput (RPS)"), ("error_rate", "Error rate"), ("apdex_t500_f2000", f"Apdex (T={APDEX_T} ms; F={APDEX_F} ms)"), ("latency_cv", "Latency CV")]
    kw_rows, pair_rows = [], []
    for sc in SCEN:
        sub = df[df.scenario == sc]
        for col, lab in outcomes:
            groups = {pl: sub.loc[sub.platform == pl, col].dropna().values for pl in ORDER}
            if any(len(v) == 0 for v in groups.values()):
                continue
            H, p = stats.kruskal(*groups.values())
            n = sum(len(v) for v in groups.values())
            kw_rows.append({"Scen.": SC_SHORT[sc], "Outcome": lab, "n": n, "H": round(H, 2), "p": f"{p:.2e}", "eps2": round(eps2_tomczak(H, len(groups), n), 3)})
            dz = dunn_pairwise(groups)
            pairs = list(dz.keys())
            praw = np.array([dz[k][1] for k in pairs])
            ph, q = holm(praw), bh_fdr(praw)
            for k, h_, q_ in zip(pairs, ph, q):
                a, b = k
                da = cliffs(groups[a], groups[b])
                pair_rows.append({"scenario": sc, "Scen.": SC_SHORT[sc], "outcome": col, "Outcome": lab, "A": a, "B": b,
                                  "median_A": float(np.median(groups[a])), "median_B": float(np.median(groups[b])),
                                  "z": round(dz[k][0], 3), "p_raw": dz[k][1], "p_holm": h_, "q_BH": q_,
                                  "cliffs_delta_(A−B)": da, "magnitude": cliff_mag(da)})
    T8 = pd.DataFrame(kw_rows)
    write_table(T8, "Table_4_08", out_dir, "4.6", "all RQs", "Kruskal-Wallis tests", "Omnibus non-parametric evidence", "Table 4.8. Kruskal-Wallis omnibus evidence by scenario and outcome.")
    E1 = pd.DataFrame(pair_rows)
    (out_dir / "evidence").mkdir(exist_ok=True)
    E1.to_csv(out_dir / "evidence" / "E1_pairwise_dunn_holm_cliffs_ALL.csv", index=False, encoding="utf-8-sig")
    note("Evidence", "E1_pairwise_dunn_holm_cliffs_ALL", "4.6", "all RQs", "Dunn/Holm + Cliff's delta", "Full pairwise non-parametric evidence grid")

    T9 = compute_group_contrast_from_tables(T2, T3).round(3)
    write_table(T9, "Table_4_09", out_dir, "4.6", "descriptive", "cell medians", "Balanced family contrast summary", "Table 4.9. Balanced descriptive traditional-versus-managed contrast using median of platform cell medians.")

    # Figure 4.11 + E2
    ci_rows = []
    seed_shift = 0
    for sc in SCEN:
        sub = df[df.scenario == sc]
        for pl in ORDER:
            x = sub.loc[sub.platform == pl, "latency_p95"].dropna().values
            if len(x):
                med, lo, hi = boot_med_ci(x, seed_shift); seed_shift += 1
                ci_rows.append({"Scen.": SC_SHORT[sc], "scenario": sc, "platform": pl, "median_p95_ms": med, "ci_low": lo, "ci_high": hi})
    E2 = pd.DataFrame(ci_rows).round(3)
    E2.to_csv(out_dir / "evidence" / "E2_bootstrap_CI_p95_cells.csv", index=False, encoding="utf-8-sig")
    note("Evidence", "E2_bootstrap_CI_p95_cells", "4.6", "RQ1", f"bootstrap R={NBOOT}, seed={SEED}", "CI backing Figure 4.11")
    write_figure(bootstrap_ci_figure(E2), "Figure_4_11", out_dir, "4.6", "RQ1", "E2 bootstrap", "Uncertainty of cell medians")

    # Tables 4.10-4.11: final thesis resource/cost summaries ------------------
    # These are scope-qualified decision-support tables retained in the thesis;
    # they are intentionally not seven-platform resource telemetry claims.
    final_table_410(out_dir)
    final_table_411(out_dir)

    # Table 4.12-4.14 synthesis
    T12 = pd.DataFrame([
        ["RQ1 Latency", "Table 4.2; Figures 4.1–4.3; Table 4.8", "Leadership and observed tail inflation rotate by scenario; no universal latency winner.", "End-to-end deployment outcome; p99/p50 is censoring-aware."],
        ["RQ2 Throughput/goodput", "Table 4.3; Figures 4.4 and 4.7", "Actual rate, goodput and error rate interpreted together.", "Delivery diagnostics do not prove every scheduled iteration was delivered."],
        ["RQ3 Reliability", "Table 4.3; Figure 4.5; Table 4.8", "Callback-defined error rates differ across configurations and scenarios.", "Application-boundary outcome; no internal failure mechanism inferred."],
        ["RQ4 User experience", "Table 4.3; Figure 4.6", f"All cell medians exceed the author-defined {APDEX_THRESHOLD} Apdex threshold; margins differ.", "T/F are author-defined operational targets."],
        ["RQ5 Elasticity/resources", "Tables 4.5–4.6, 4.10; Figures 4.8–4.9", "Burst response heterogeneous; resource data scoped to the retained evidence.", "Temporal evidence descriptive; probe informs H2 only."],
        ["RQ6 Cost-efficiency", "Table 4.11", "Modelled USD per 1M successful requests differs under stated inputs.", "Conditional model; not invoices or TCO."],
        ["H1 Apache lowest C p95", "Tables 4.2, 4.13, 4.14", "NOT SUPPORTED.", "Apache C tails include timeout censoring."],
        ["H2 post-idle first-request delay", "Table 4.7; Figure 4.10", "Descriptively supported: valid pairs slower after idle.", "Dedicated small probe; no lifecycle state verified."],
        ["H3 cost differs", "Table 4.11", "Supported within stated model only.", "Not an invoice/TCO finding."],
        ["H4 burst raises error", "Tables 4.3, 4.6", "NOT SUPPORTED as a consistent cross-platform claim.", "No aggregate cross-scenario inferential test claimed."]
    ], columns=["Question / hypothesis", "Primary evidence", "Evidence-bounded verdict", "Caveat"])
    write_table(T12, "Table_4_12", out_dir, "4.8", "all", "auto-linked exhibit pointers", "RQ & hypothesis evidence matrix", "Table 4.12. Research-question and hypothesis evidence matrix.")

    rows = []
    for sc in SCEN:
        s2 = T2[T2.scenario == sc].set_index("platform")
        s3 = T3[T3.scenario == sc].set_index("platform")
        leader = s2["p95_ms"].idxmin(); bestg = s3["goodput_RPS"].idxmax(); worst = s2["p95_ms"].idxmax()
        cens = s2[s2["censored_reps_of_10"] > 0]
        cens_note = "; censored: " + ", ".join([f"{idx} {int(r.censored_reps_of_10)}/10" for idx, r in cens.iterrows()]) if len(cens) else ""
        rows.append({"Scenario": SC_SHORT[sc], "Lowest observed median p95": f"{leader} — {s2.loc[leader,'p95_ms']:.1f} ms",
                     "Delivery / reliability context": f"{bestg}: {s3.loc[bestg,'goodput_RPS']:.2f} RPS goodput; {s3.loc[bestg,'error_%']:.3f}% error. Highest p95: {worst} ({s2.loc[worst,'p95_ms']:.1f} ms)" + cens_note,
                     "Main evidence boundary": "End-to-end deployment outcome under the stated topology."})
    T13 = pd.DataFrame(rows)
    write_table(T13, "Table_4_13", out_dir, "4.8", "synthesis", "auto-computed from cell medians + censor flags", "Scenario-specific synthesis", "Table 4.13. Descriptive scenario-specific evidence synthesis (not an overall platform ranking).")

    focus = E1[(E1.scenario == "C_checkout") & (E1.outcome == "latency_p95")].copy()
    target = "Apache + mod_wsgi"
    out_rows = []
    for _, r in focus.iterrows():
        if r.A == target:
            comp, ap_med, comp_med, delta = r.B, r.median_A, r.median_B, r["cliffs_delta_(A−B)"]
        elif r.B == target:
            comp, ap_med, comp_med, delta = r.A, r.median_B, r.median_A, -r["cliffs_delta_(A−B)"]
        else:
            continue
        if comp in ["Nginx + uWSGI", "Django + Gunicorn", "Azure Container Apps", "IIS + Waitress"]:
            out_rows.append({"Comparator": comp, "Apache_p95_median_ms": ap_med, "Comparator_p95_median_ms": comp_med, "Holm_adjusted_p": r.p_holm, "Cliffs_delta_(Apache−comparator)": delta, "magnitude": cliff_mag(delta)})
    T14 = pd.DataFrame(out_rows).set_index("Comparator").reindex(["Nginx + uWSGI", "Django + Gunicorn", "Azure Container Apps", "IIS + Waitress"]).reset_index().round({"Apache_p95_median_ms": 1, "Comparator_p95_median_ms": 1, "Holm_adjusted_p": 4, "Cliffs_delta_(Apache−comparator)": 2})
    write_table(T14, "Table_4_14", out_dir, "4.8", "H1", "subset of E1", "Focused Scenario C pairwise evidence", "Table 4.14. Focused Scenario C p95 pairwise evidence for H1 (Dunn/Holm and Cliff's delta).")

    # E3/E4 appendix grids
    df[["run_id", "platform", "scenario", "replication", "latency_p99", "censored"]].to_csv(out_dir / "evidence" / "E3_per_replication_censor_flags.csv", index=False, encoding="utf-8-sig")
    num_cols = [c for c in df.select_dtypes(include=[np.number]).columns if c not in ["replication", "censored"]]
    E4 = df.groupby(["scenario", "platform"])[num_cols].median().round(3).reset_index()
    E4 = grouped_sort(E4)
    E4.to_csv(out_dir / "evidence" / "E4_appendix_full_metric_grid.csv", index=False, encoding="utf-8-sig")
    note("Evidence", "E3_per_replication_censor_flags", "4.2", "RQ1", f"rule: latency_p99 >= {CENSOR_MS:.0f} ms", "Replication-level censoring audit")
    note("Evidence", "E4_appendix_full_metric_grid", "Appendix", "coverage", "median of every numeric master column per cell", "Full metric grid coverage")

# ---------------------------------------------------------------------------
# Preview mode from existing exhibit tables
# ---------------------------------------------------------------------------
def run_from_existing_exhibits(exhibits_dir: Path, out_dir: Path):
    print("\n=== PREVIEW MODE: existing Table_4_*.csv -> current-style figures/tables ===")
    out_dir.mkdir(parents=True, exist_ok=True)
    for sub in ["exhibits", "evidence", "templates"]:
        (out_dir / sub).mkdir(exist_ok=True)
    def R(n):
        p = exhibits_dir / f"Table_4_{n:02d}.csv"
        if not p.exists():
            raise FileNotFoundError(p)
        return pd.read_csv(p)

    # Copy/regroup all available CSV/MD tables
    for p in sorted(exhibits_dir.glob("Table_4_*.csv")):
        df = pd.read_csv(p)
        if "platform" in df.columns:
            df = grouped_sort(df)
        group = "platform" in df.columns
        write_table(df, p.stem, out_dir, "preview", "preview", str(p), "Current-style regrouped table", f"{p.stem.replace('_',' ')}. Current-style exported table.", group)

    T2 = R(2); T2["platform"] = T2["platform"].map(platform_display)
    T3 = R(3); T3["platform"] = T3["platform"].map(platform_display)
    T5 = R(5); T5["platform"] = T5["platform"].map(platform_display)
    T6 = R(6); T6["platform"] = T6["platform"].map(platform_display)
    make_latency_figures(T2, out_dir)
    make_delivery_figures(T3, T2, out_dir)
    write_figure(warmup_two_panel(T5), "Figure_4_08", out_dir, "4.5", "RQ5", "Table 4.5", "Two-panel warm-up ratio summary")
    write_figure(burst_phase_summary(T6), "Figure_4_09", out_dir, "4.5", "RQ5,H4", "Table 4.6", "Scenario D phase-level burst summary")
    p7 = exhibits_dir / "Table_4_07.csv"
    if p7.exists():
        T7_in = pd.read_csv(p7)
        T7 = post_idle_summary_table(T7_in)
        write_table(T7, "Table_4_07", out_dir, "4.5", "H2", str(p7), "Supplementary post-idle first-request probe", "Table 4.7. Supplementary post-idle first-request probe for managed platforms (paired /health/ requests).")
        write_figure(post_idle_grouped_bars(T7), "Figure_4_10", out_dir, "4.5", "H2", "Table 4.7", "Grouped median post-idle probe summary")
    final_table_410(out_dir)
    final_table_411(out_dir)
    # If old Figure 4.11 exists, copy it for preview continuity.
    for ext in ["png", "pdf"]:
        old = exhibits_dir / f"Figure_4_11.{ext}"
        if old.exists():
            import shutil
            shutil.copyfile(old, out_dir / "exhibits" / f"Figure_4_11.{ext}")
            note("Figure", "Figure_4_11", "4.6", "RQ1", str(old), "Copied preview bootstrap CI figure")
    write_manifest_and_report(out_dir, mode="preview")

# ---------------------------------------------------------------------------
def write_manifest_and_report(out_dir: Path, mode: str):
    pd.DataFrame(MANIFEST).to_csv(out_dir / "MANIFEST.csv", index=False, encoding="utf-8-sig")
    report = [
        "Chapter 4 final-submission exhibit pipeline report",
        "==================================================",
        f"mode: {mode}",
        f"output: {out_dir}",
        "",
        "Final v153 style rules applied:",
        "- Detailed tables grouped by platform family where platform rows are present.",
        "- Heatmaps retained for platform-by-scenario matrices.",
        "- Group contrasts rendered as grouped bar charts.",
        "- Warm-up rendered as a two-panel horizontal grouped bar chart.",
        "- Scenario D burst evidence rendered as the final thesis phase-level line summary.",
        "- Post-idle probe rendered as final thesis Table 4.7 summary and grouped median bars with log-scale latency.",
        "",
        f"manifest entries: {len(MANIFEST)}",
    ]
    (out_dir / "VERIFY_report.txt").write_text("\n".join(report), encoding="utf-8")
    print("\n=== DONE ===")
    print(f"  outputs: {out_dir}")
    print(f"  manifest: {out_dir / 'MANIFEST.csv'}")
    print(f"  report: {out_dir / 'VERIFY_report.txt'}")

# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Render Chapter 4 exhibits in the final v154 thesis-mirror style")
    ap.add_argument("--data", default=".", help="folder containing master_runs.csv and related input CSVs")
    ap.add_argument("--output", default="out_ch4_v153_final_style", help="output folder")
    ap.add_argument("--from-existing-exhibits", default=None, help="existing exhibits folder containing Table_4_*.csv; creates a style-preview rebuild")
    args = ap.parse_args()

    data_dir = Path(args.data).resolve()
    out_dir = Path(args.output).resolve()

    if args.from_existing_exhibits:
        run_from_existing_exhibits(Path(args.from_existing_exhibits).resolve(), out_dir)
        return

    if (data_dir / "master_runs.csv").exists():
        missing = [f for f in ["warmup_transient.csv", "timeseries_burst_recovery.csv"] if not (data_dir / f).exists()]
        if missing:
            raise SystemExit(f"Missing required input(s) for full mode: {missing}")
        run_full(data_dir, out_dir)
        return

    fallback = data_dir / "out_ch4_v131" / "exhibits"
    if fallback.exists():
        print("master_runs.csv not found; using existing-exhibits preview mode from", fallback)
        run_from_existing_exhibits(fallback, out_dir)
        return

    raise SystemExit("No master_runs.csv found and no existing exhibits folder found. Provide --data with raw CSVs or --from-existing-exhibits.")

if __name__ == "__main__":
    main()
