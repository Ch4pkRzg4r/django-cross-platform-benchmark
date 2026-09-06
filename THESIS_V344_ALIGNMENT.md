# Thesis v344 repository alignment

This note records the relationship between the submitted thesis document revision and the retained research-artefact repository.

## Controlling states

- Thesis document revision reviewed for submission: **v344**.
- Controlling numerical/statistical analysis: **v330 calibrated end-to-end pipeline**.
- Canonical analytical dataset: `data/canonical/master_runs.csv` (**280 run-level rows × 39 fields**).
- Repository: `https://github.com/Ch4pkRzg4r/django-cross-platform-benchmark`.
- Repository visibility at this stage: **private thesis/examination repository**; public release remains subject to supervisor/college approval.

The changes from the v330 analytical state to thesis document v344 are editorial, notation, labelling, redaction and document-QA corrections. They do **not** change the frozen canonical dataset, the declared inferential estimands, or the numerical Chapter 4 results.

## Artefacts present in this repository

The repository contains the publishable/auditable research artefacts needed to inspect the benchmark and rerun the retained analytical workflow, including:

- benchmark-time `orchestrator.ps1`;
- the four k6 scenario scripts;
- `parse_k6_output.py`;
- the retained Django application/source capture and Docker/runtime files, with credential-templated derivatives where required;
- redacted/safe deployment and scenario configuration records;
- the canonical 280 × 39 dataset and data dictionary;
- supplementary post-idle, warm-up and burst-recovery analytical carriers;
- the controlling v330 analysis materialiser/runner and analysis dependency record;
- Chapter 4 analytical table/figure carriers and verification records;
- provenance, data-availability, licensing, security/redaction and SHA-256 manifest records.

## Controlled evidence intentionally outside ordinary Git history

The repository is **not** represented as containing every historical raw byte. The following remain controlled outside ordinary Git history, with availability/integrity boundaries documented in `DATA_AVAILABILITY.md` and the raw-archive manifests:

- the complete original per-run k6 JSON/CSV archive;
- the 280 retained run logs;
- the complete 120-run Docker resource-telemetry archive required for exact Table 4.11 reproduction;
- exact frozen-reference publication assets used only as regression oracles;
- sensitive originals such as credentials, private endpoints/provider identifiers, private histories and other restricted evidence.

Accordingly, the repository supports code/configuration inspection, canonical-data audit and controlled analytical rerunning, but it does not claim public byte-for-byte reconstruction of the historical managed-cloud campaign.

## v344 presentation alignment note

Thesis v344 introduced a **presentation-only clarification** to the Table 4.6 column headings (for example, distinguishing baseline/peak/post-ramp median p95 and the whole-run descriptors). The underlying numerical values and analytical carrier are unchanged from the validated v330 result. Repository v330 table carriers therefore remain the controlling numerical evidence; the v344 thesis wording is the clearer presentation label.

Other v344 changes such as Apdex notation clarification, endpoint redaction wording, Eq. 3.1 typesetting, post-idle notation and Appendix E presentation cleanup likewise do not modify the frozen analytical inputs or numerical conclusions.
