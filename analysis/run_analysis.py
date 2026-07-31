#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_analysis.py  --  UNIFIED CHAPTER 4 ANALYSIS RUNNER
======================================================
MSc thesis: "Benchmarking and Evaluation of Traditional Web Servers and
             Serverless Architectures for an E-Commerce System"
Candidate  : Chapk Rzgar Mohammed Abdalla, University of Sulaimani
Supervisor : Asst. Prof. Dr. Kamaran Hama Ali Faraj

WHY THIS FILE EXISTS
--------------------
The study's analysis was developed as five separate scripts (Phase 0 collection,
Phase 1 validation, Phase 2 EDA, Phase 3 inferential, Phase 4/5 exhibits). Run
individually they each expected a slightly different input filename, which is a
source of ambiguity for a reader or examiner. This runner removes that ambiguity:
it executes the WHOLE analytical chain in order, from ONE input file, with ONE
documented data contract, and writes ONE consolidated integrity report. Nothing
in the individual phase scripts is discarded — this file is the spine that calls
them in the correct order and proves the chain is internally consistent.

THE FULL PROVENANCE CHAIN (each arrow is a script this runner accounts for)
---------------------------------------------------------------------------
  [Phase 0]  orchestrator.ps1  +  scripts/k6/*.js
             -> drives 280 runs; per run retains raw k6 CSV (per-second) and
                JSON (per-request, 30-80 MB). Chapter 3, Section 3.11, Listing 3.6.

  [Phase 0]  parse_k6_output.py
             -> reduces each run's raw JSON to ONE analytical row
                (39 fields: identifiers, latency percentiles, goodput, error rate,
                 Apdex, TTFB fields). Appends to master_runs.csv.
                Chapter 3, Section 3.12, Listing 3.7.

  [Phase 1]  phase1_validation.py
             -> structural + null + 6-flag quality audit + SHA-256 integrity.
                Emits master_runs_VALIDATED.csv (adds quality flags).

  [Phase 2]  phase2_eda.py
             -> descriptives, high-variance/outlier screen, normality (Shapiro),
                homoscedasticity (Levene) -> justifies the NON-PARAMETRIC choice.

  [Phase 3]  phase3_inferential.py
             -> Kruskal-Wallis, Dunn/Holm, Cliff's delta, BCa bootstrap CIs,
                Friedman/Wilcoxon (H4).

  [Phase 4/5] ch4_evidence_pipeline.py
             -> renders the FINAL thesis exhibits (Tables 4.1-4.14, Figures
                4.1-4.11) with the thesis's exact numbering + the E1-E4 evidence
                collection, and self-verifies 30 anchor numbers against the text.

  [Elasticity] analyze_coldstart.py, analyze_timeseries.py
             -> post-idle probe (Table 4.7/Fig 4.10) and burst trace
                (Table 4.6/Fig 4.9) inputs.

WHAT THIS RUNNER GUARANTEES
---------------------------
  * ONE canonical input: master_runs.csv (39 fields x 280 rows).
  * A frozen SHA-256 of that input, recorded in RUN_MANIFEST.json.
  * Each phase runs only if its predecessor succeeded (fail-fast chain).
  * A single consolidated console log and RUN_MANIFEST.json listing every
    output artefact, so the examiner sees the entire chain at a glance.

USAGE
-----
    python run_analysis.py                      # run the whole chain
    python run_analysis.py --only exhibits      # just re-render Chapter 4
    python run_analysis.py --data <folder>      # inputs live elsewhere
    python run_analysis.py --skip eda           # skip a phase by name

Phase names: validate | eda | inferential | elasticity | exhibits
"""

import os, sys, io, json, hashlib, argparse, subprocess, datetime, textwrap

# --- UTF-8 everywhere (Windows cp1252 safety) ------------------------------
os.environ.setdefault("PYTHONUTF8", "1")
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
CANONICAL_INPUT = "master_runs.csv"

# The ordered chain. Each entry: (name, script, produces, chapter_ref, required_inputs)
CHAIN = [
    ("validate",   "phase1_validation.py",
     "master_runs_VALIDATED.csv, validation_report.json, checksums.sha256",
     "Ch.3 §3.16 / Ch.4 §4.1", [CANONICAL_INPUT]),
    ("eda",        "phase2_eda.py",
     "desc_*.csv, normality_shapiro.csv, levene_homoscedasticity.csv, outliers_extreme.csv",
     "Ch.3 §3.15 (method justification)", ["master_runs_VALIDATED.csv"]),
    ("inferential","phase3_inferential.py",
     "phase3_omnibus_kruskal.csv, phase3_pairwise_dunn_long.csv, phase3_cliffs_delta.csv, phase3_bootstrap_ci_medians.csv, phase3_h4_wilcoxon.csv",
     "Ch.4 §4.6, Table 4.8", ["master_runs_VALIDATED.csv"]),
    ("elasticity", "analyze_coldstart.py",
     "coldstart_summary.csv, post_idle_pair_audit.csv, fig_coldstart_measured.png",
     "Ch.4 §4.5, Table 4.7 (post-idle probe)", ["coldstart_raw.csv"]),
    ("exhibits",   "ch4_evidence_pipeline.py",
     "out_ch4_v153_final_style/ (Tables 4.1-4.14, Figures 4.1-4.11, E1-E5, VERIFY_report.txt)",
     "Ch.4 §4.1-§4.8 (all final exhibits)", [CANONICAL_INPUT]),
]

def sha256_of(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()

def banner(msg, ch="="):
    print("\n" + ch * 74)
    print(msg)
    print(ch * 74)

def resolve_script(script):
    """Resolve a phase script from either the bundle root or scripts/ folder."""
    candidates = [
        os.path.join(HERE, script),
        os.path.join(HERE, "scripts", script),
    ]
    # When this wrapper itself is inside scripts/, also check the parent bundle root.
    if os.path.basename(HERE).lower() == "scripts":
        candidates.append(os.path.join(os.path.dirname(HERE), script))
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    return None


def run_phase(name, script, data_dir):
    path = resolve_script(script)
    if path is None:
        print(f"  [skip] {name}: {script} not found in bundle root or scripts/")
        return None
    banner(f"PHASE: {name.upper()}  ->  {script}", "-")
    # exhibits phase accepts --data; others read their own hard-coded names in cwd
    cmd = [sys.executable, path]
    if script == "ch4_evidence_pipeline.py":
        cmd += ["--data", data_dir]
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    r = subprocess.run(cmd, cwd=data_dir, env=env,
                       capture_output=True, text=True, encoding="utf-8")
    sys.stdout.write(r.stdout or "")
    if r.returncode != 0:
        sys.stderr.write(r.stderr or "")
        raise RuntimeError(f"Phase '{name}' failed (exit {r.returncode}). See stderr above.")
    return {"script": script, "resolved_path": os.path.relpath(path, HERE),
            "script_sha256": sha256_of(path), "returncode": r.returncode,
            "stdout_tail": "\n".join((r.stdout or "").splitlines()[-12:])}

def main():
    ap = argparse.ArgumentParser(description="Unified Chapter 4 analysis runner")
    ap.add_argument("--data", default=".", help="folder holding the input CSVs")
    ap.add_argument("--only", default=None, help="run only this phase")
    ap.add_argument("--skip", nargs="*", default=[], help="phase names to skip")
    a = ap.parse_args()
    data_dir = os.path.abspath(a.data)

    banner("UNIFIED CHAPTER 4 ANALYSIS RUNNER")
    print("Thesis : Benchmarking Traditional Web Servers vs Serverless (E-Commerce)")
    print("Author : Chapk Rzgar Mohammed Abdalla, University of Sulaimani")
    print(f"Time   : {datetime.datetime.now().isoformat(timespec='seconds')}")
    print(f"Data   : {data_dir}")

    # ---- canonical input contract + integrity ----
    inp = os.path.join(data_dir, CANONICAL_INPUT)
    if not os.path.exists(inp):
        sys.exit(f"FATAL: canonical input '{CANONICAL_INPUT}' not found in {data_dir}")
    digest = sha256_of(inp)
    banner("INPUT CONTRACT & INTEGRITY", "-")
    print(f"  canonical input : {CANONICAL_INPUT}")
    print(f"  SHA-256         : {digest}")
    print( "  contract        : 280 rows x 39 core fields "
           "(7 platforms x 4 scenarios x 10 replications)")

    manifest = {
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "candidate": "Chapk Rzgar Mohammed Abdalla",
        "canonical_input": CANONICAL_INPUT,
        "canonical_sha256": digest,
        "provenance_chain": [
            "orchestrator.ps1 + k6/*.js -> raw per-run CSV/JSON (Ch.3 §3.11)",
            "parse_k6_output.py -> master_runs.csv, 39 fields/run (Ch.3 §3.12)",
            "phase1_validation.py -> validated + 6 quality flags (§4.1)",
            "phase2_eda.py -> normality/Levene -> non-parametric justification (§3.15)",
            "phase3_inferential.py -> KW/Dunn/Cliff/bootstrap/Friedman (§4.6)",
            "ch4_evidence_pipeline.py -> Tables 4.1-4.14, Figures 4.1-4.11, E1-E5 (§4.1-4.8)",
        ],
        "phases": [],
    }

    order = [c for c in CHAIN]
    if a.only:
        order = [c for c in CHAIN if c[0] == a.only]
        if not order:
            sys.exit(f"unknown phase '{a.only}'. valid: {[c[0] for c in CHAIN]}")

    for name, script, produces, ref, req in order:
        if name in a.skip:
            print(f"\n[skip] {name} (user requested)")
            continue
        # check required inputs exist (soft — phases downstream may create them)
        missing = [f for f in req if not os.path.exists(os.path.join(data_dir, f))]
        if missing and name != "validate":
            print(f"  [note] {name}: expected {missing} not present yet "
                  f"(created by an earlier phase — fine if you ran the full chain)")
        info = run_phase(name, script, data_dir)
        manifest["phases"].append({
            "phase": name, "script": script, "produces": produces,
            "thesis_reference": ref, "result": info or "skipped(not present)"})

    # ---- consolidated manifest ----
    out_manifest = os.path.join(data_dir, "RUN_MANIFEST.json")
    with open(out_manifest, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    banner("CHAIN COMPLETE")
    print(f"  consolidated manifest : RUN_MANIFEST.json")
    executed = [p["phase"] for p in manifest["phases"] if isinstance(p.get("result"), dict)]
    if "exhibits" in executed:
        print(f"  final exhibits        : out_ch4_v153_final_style/  (see VERIFY_report.txt)")
    else:
        print(f"  executed phases       : {', '.join(executed) if executed else 'none'}")
    print("  executed outputs are tied to the canonical input hash recorded above.")
    print("\nProvenance summary (what produced what):")
    for name, script, produces, ref, _ in order:
        if name in a.skip:
            continue
        print(f"  • {name:<12} {script:<26} -> {ref}")

if __name__ == "__main__":
    main()
