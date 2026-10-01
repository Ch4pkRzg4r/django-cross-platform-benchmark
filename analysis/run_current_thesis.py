#!/usr/bin/env python3
"""Regenerate the current descriptive release over unchanged v360/v367 layers.

Primary v330 execution is optional and requires its controlled historical inputs.
"""
from pathlib import Path
import argparse, hashlib, importlib.metadata, json, os, subprocess, sys, tempfile

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--master',type=Path)
    parser.add_argument('--out-dir',type=Path)
    parser.add_argument('--run-v330',action='store_true')
    parser.add_argument('--docker-stats',type=Path)
    parser.add_argument('--figure-reference-dir',type=Path)
    parser.add_argument('--verify-against-v329',action='store_true')
    args=parser.parse_args()
    repo=Path(__file__).resolve().parents[1]
    master=(args.master or repo/'data/canonical/master_runs.csv').resolve()
    expected='710b3a7a79d794425ac04254caba892419ad78f56cf4c174843e3c417c5ebde7'
    if hashlib.sha256(master.read_bytes()).hexdigest()!=expected:
        raise SystemExit('This release requires the unchanged frozen canonical dataset.')
    out=(args.out_dir or repo/'.current-thesis-run/release').resolve()
    out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='thesis-release-',dir=out.parent) as tmp:
        stage=Path(tmp)
        base=[sys.executable,str(repo/'analysis/run_v367_from_repo.py'),
              '--master',str(master),'--out-dir',str(stage/'base_layers')]
        if args.run_v330:base.append('--run-v330')
        if args.verify_against_v329:base.append('--verify-against-v329')
        for opt,value in [('--docker-stats',args.docker_stats),('--figure-reference-dir',args.figure_reference_dir)]:
            if value is not None:base.extend([opt,str(value.resolve())])
        subprocess.run(base,check=True,cwd=repo)
        scripts=repo/'analysis/current-thesis'
        def run(name,*params):
            subprocess.run([sys.executable,str(scripts/name),*map(str,params)],check=True,cwd=repo)
        run('chapter4_descriptive_supplement.py','--master',master,'--out',stage/'supplement')
        run('render_completed_delivery.py','--carrier',stage/'supplement/delivery_shortfall_280_runs.csv','--out',stage/'delivery_figure')
        run('regenerate_profile_panels.py','--master',master,'--out',stage/'profile_panels')
        files={str(p.relative_to(stage)):hashlib.sha256(p.read_bytes()).hexdigest()
               for p in sorted(stage.rglob('*')) if p.is_file()}
        manifest={'release':'2026-10-01','canonical_sha256':expected,
                  'v330_executed':args.run_v330,'primary_inference_changed':False,
                  'python':sys.version.split()[0],
                  'packages':{n:importlib.metadata.version(n) for n in ['numpy','pandas','scipy','matplotlib']},
                  'output_sha256':files,
                  'scope':'Descriptive carriers, unchanged v360/v367 layers, Figures 4.3, 4.4 and 4.9. No complete campaign rerun or complete thesis-rendering claim.'}
        (stage/'release_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        # Publish only files from this successful staging run; the manifest is last.
        out.mkdir(parents=True,exist_ok=True)
        for rel in [*files,'release_manifest.json']:
            target=out/rel;target.parent.mkdir(parents=True,exist_ok=True)
            os.replace(stage/rel,target)
    print('PASS current thesis release: '+str(out))
    return 0

if __name__=='__main__':raise SystemExit(main())
