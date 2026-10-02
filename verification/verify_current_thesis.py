#!/usr/bin/env python3
"""Verify current carriers against retained reviewed references and source identities."""
from pathlib import Path
import argparse, base64, csv, gzip, hashlib, json
import pandas as pd

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out-dir',type=Path)
    a=p.parse_args();repo=Path(__file__).resolve().parents[1]
    out=(a.out_dir or repo/'.current-thesis-run/release').resolve()
    record=json.loads((repo/'documentation/thesis_alignment_2026-10-02.json').read_text())
    assert digest(repo/'data/canonical/master_runs.csv')==record['canonical_sha256']
    encoded=''.join((repo/'analysis/v330-payload'/f'payload_{i:02d}.b64').read_text().strip() for i in range(1,6))
    assert hashlib.sha256(gzip.decompress(base64.b64decode(encoded))).hexdigest()==record['frozen_v330_sha256']
    for path,h in record['protected_source_sha256'].items():assert digest(repo/path)==h,path
    manifest=json.loads((out/'release_manifest.json').read_text())
    assert manifest['canonical_sha256']==record['canonical_sha256']
    assert manifest['primary_inference_changed'] is False
    for path,h in manifest['output_sha256'].items():assert digest(out/path)==h,path
    refs=repo/'results/current-thesis/release-2026-10-01'
    checked=[]
    for rel in record['descriptive_carriers']:
        before=pd.read_csv(refs/rel);after=pd.read_csv(out/rel)
        pd.testing.assert_frame_equal(before,after,check_exact=False,rtol=1e-12,atol=1e-12)
        checked.append(rel)
    d=pd.read_csv(out/'supplement/delivery_shortfall_280_runs.csv')
    assert len(d)==280 and d.run_id.nunique()==280
    assert (d.shortfall_pct>1).sum()==28 and (d.shortfall_pct>=5).sum()==10
    profile=pd.read_csv(out/'profile_panels/profile_336_cells.csv',keep_default_na=False)
    assert len(profile)==336 and (profile.marker!='').sum()==104
    h4=pd.read_csv(out/'supplement/H4_seven_platform_rules.csv')
    assert set(h4.loc[h4.H4_descriptive_supported,'platform'])=={'03_django_gunicorn','07_iis_waitress'}
    figure_map=pd.read_csv(repo/'results/current-thesis/figure_map_2026-10-01.csv')
    assert list(figure_map.Figure)==[f'4.{i}' for i in range(1,9)]+[f'4.9{c}' for c in 'abcdef']
    rows=list(csv.DictReader((repo/'MANIFEST_2026-10-02_SHA256.csv').open(newline='')))
    assert len({x['path'] for x in rows})==len(rows)
    for row in rows:
        f=repo/row['path'];assert f.stat().st_size==int(row['bytes']),row['path']
        assert digest(f)==row['sha256'],row['path']
    print(f'PASS {len(checked)} reviewed descriptive carriers; 336 profile cells; 104 markers; 280 runs; protected source identities; current file/output manifests.')
    return 0
if __name__=='__main__':raise SystemExit(main())
