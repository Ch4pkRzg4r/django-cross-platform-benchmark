#!/usr/bin/env python3
"""Verify only the affected v367 outputs; primary inference remains frozen."""
from pathlib import Path
import argparse,csv,hashlib,json,statistics

def main():
    repo=Path(__file__).resolve().parents[1]
    ap=argparse.ArgumentParser()
    ap.add_argument('--master',type=Path,default=repo/'data/canonical/master_runs.csv')
    ap.add_argument('--out-dir',type=Path,default=repo/'.v367-run/release')
    args=ap.parse_args()
    canonical=args.master.read_bytes()
    assert hashlib.sha256(canonical).hexdigest()=='710b3a7a79d794425ac04254caba892419ad78f56cf4c174843e3c417c5ebde7'
    with args.master.open(encoding='utf-8-sig',newline='')as f:runs=list(csv.DictReader(f))
    with (args.out_dir/'v367_h4_descriptive.csv').open(newline='')as f:flags=list(csv.DictReader(f))
    assert len(flags)==7
    supported=[]
    for row in flags:
        p=row['platform'];med={}
        for s in ['A_browse','B_mixed','C_checkout','D_burst']:
            vals=[float(x['error_rate'])for x in runs if x['platform']==p and x['scenario']==s]
            assert len(vals)==10;med[s]=statistics.median(vals)
        expected=all(med['D_burst']>med[s]for s in ['A_browse','B_mixed','C_checkout'])
        assert (row['supported'].lower()=='true')==expected
        supported.append(expected)
    assert sum(supported)==2 and not all(supported)
    manifest=json.loads((args.out_dir/'v367_release_manifest.json').read_text())
    assert manifest['h4_overall_supported'] is False
    assert manifest['platform_flags_changed']==['04_aca']
    assert manifest['figure_font_check']['minimum_font_pt']>=10
    for name,identity in manifest['outputs'].items():
        assert hashlib.sha256((args.out_dir/name).read_bytes()).hexdigest()==identity['sha256'],name
    print('PASS v367 strict H4 rule, canonical identity, placed font sizes and output hashes')
    return 0

if __name__=='__main__':raise SystemExit(main())
