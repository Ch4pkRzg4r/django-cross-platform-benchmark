"""Reproduce the new descriptive carriers from the unchanged canonical dataset.

Usage: python chapter4_descriptive_supplement.py --master master_runs.csv --out outputs
No hypothesis test or primary-result replacement is performed.
"""
from pathlib import Path
import argparse,hashlib,json
import numpy as np
import pandas as pd

EXPECTED='710b3a7a79d794425ac04254caba892419ad78f56cf4c174843e3c417c5ebde7'
PLANNED={'A_browse':36000,'B_mixed':27000,'C_checkout':18000,'D_burst':32100}
PRICES={'01_apache_modwsgi':96.98,'02_nginx_uwsgi':96.98,'03_django_gunicorn':96.98,'07_iis_waitress':173.71,'04_aca':157.68,'05_koyeb':21.43,'06_flyio':11.39}

def compute(master,out):
    master=Path(master);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    digest=hashlib.sha256(master.read_bytes()).hexdigest();assert digest==EXPECTED
    d=pd.read_csv(master);assert d.shape==(280,39) and d.run_id.nunique()==280
    assert d.groupby(['platform','scenario']).size().eq(10).all()
    run=d[['run_id','platform','scenario','k6_iterations']].copy()
    run['planned_starts']=run.scenario.map(PLANNED)
    run['shortfall_pct']=100*np.maximum(run.planned_starts-run.k6_iterations,0)/run.planned_starts
    run.to_csv(out/'delivery_shortfall_280_runs.csv',index=False)
    cells=run.groupby(['platform','scenario']).agg(n=('run_id','size'),median_shortfall_pct=('shortfall_pct','median'),maximum_shortfall_pct=('shortfall_pct','max'),over_one_percent=('shortfall_pct',lambda x:int((x>1).sum())),at_least_five_percent=('shortfall_pct',lambda x:int((x>=5).sum()))).reset_index()
    cells.to_csv(out/'delivery_shortfall_28_cells.csv',index=False)
    cost=d.groupby(['platform','scenario']).goodput_rps.median().rename('median_goodput').reset_index()
    cost['monthly_usd']=cost.platform.map(PRICES)
    cost['cost_per_million']=cost.monthly_usd*1e6/(cost.median_goodput*2628000)
    cost=cost[['platform','scenario','monthly_usd','median_goodput','cost_per_million']]
    cost.to_csv(out/'scenario_specific_cost_28.csv',index=False)
    rates=100*d.groupby(['platform','scenario']).error_rate.median().unstack()
    rates['H4_descriptive_supported']=(rates.D_burst>rates.A_browse)&(rates.D_burst>rates.B_mixed)&(rates.D_burst>rates.C_checkout)
    rates.to_csv(out/'H4_seven_platform_rules.csv')
    summary={'canonical_sha256':digest,'runs':len(run),'platform_scenario_cells':len(cells),'runs_shortfall_over_1_percent':int((run.shortfall_pct>1).sum()),'runs_shortfall_at_least_5_percent':int((run.shortfall_pct>=5).sum()),'H4_configurations_meeting_rule':rates.index[rates.H4_descriptive_supported].tolist(),'cost_model_month_seconds':2628000,'scope':'Descriptive views of the retained canonical runs. Fixed model prices; no additional inferential test.'}
    (out/'supplement_calculation_summary.json').write_text(json.dumps(summary,indent=2))
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--master',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    print(json.dumps(compute(a.master,a.out),indent=2))
