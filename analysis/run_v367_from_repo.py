#!/usr/bin/env python3
"""Current entry point: unchanged v360 release carriers, then v367 H4/figure fixes."""
from pathlib import Path
import argparse
import subprocess
import sys

def main():
    analysis=Path(__file__).resolve().parent
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--master',type=Path)
    parser.add_argument('--out-dir',type=Path)
    parser.add_argument('--run-v330',action='store_true')
    parser.add_argument('--docker-stats',type=Path)
    parser.add_argument('--figure-reference-dir',type=Path)
    parser.add_argument('--verify-against-v329',action='store_true')
    parsed=parser.parse_args()
    args=sys.argv[1:]
    # Forward existing full-base and controlled-input options to the v360 runner.
    subprocess.check_call([sys.executable,str(analysis/'run_v360_from_repo.py'),*args])
    current=[]
    for option,value in [('--master',parsed.master),('--out-dir',parsed.out_dir)]:
        if value is not None:current.extend([option,str(value.resolve())])
    subprocess.check_call([sys.executable,str(analysis/'v367_release_corrections.py'),*current])
    return 0

if __name__=='__main__':
    raise SystemExit(main())
