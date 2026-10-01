"""Replot the verified 336 rank cells with the current Figure 4.9a–f titles.

This draws new scientific charts from the canonical numbers. No source raster
is retouched. Dimensions and axes bounds retain the established exhibit geometry.
"""
from pathlib import Path
import json
import pandas as pd
import numpy as np
from scipy.stats import rankdata
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def build(master,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    df=pd.read_csv(master);df['ratio']=df.latency_p99/df.latency_p50
    med=df.groupby(['platform','scenario']).median(numeric_only=True)
    order=['01_apache_modwsgi','02_nginx_uwsgi','03_django_gunicorn','07_iis_waitress','04_aca','05_koyeb','06_flyio']
    labels=['Apache','Nginx','Gunicorn','IIS','ACA','Koyeb','Fly.io']
    scenarios=['A_browse','B_mixed','C_checkout','D_burst']
    families=[('Latency and variability',['latency_p50','latency_p95','latency_p99','latency_p999','latency_cv','ratio'],['p50','p95','p99','p99.9','CV','p99/p50']),('Delivery and experience',['goodput_rps','error_rate','apdex_t500_f2000'],['Goodput','Failure','Apdex']),('Request-path and transfer',['waiting_p50','waiting_p95','bandwidth_rx_bps'],['Waiting\np50','Waiting\np95','Received-data\nrate'])]
    plt.rcParams.update({'font.family':'Nimbus Roman','font.size':10,'pdf.fonttype':42})
    carrier=[];panel=0
    for title,metrics,xticks in families:
        for ss in [scenarios[:2],scenarios[2:]]:
            matrix=np.zeros((14,len(metrics)));glyph=np.full(matrix.shape,'',dtype='<U1')
            for si,s in enumerate(ss):
                for ci,c in enumerate(metrics):
                    vals=np.array([med.loc[(p,s),c] for p in order])
                    ranks=(rankdata(vals,method='average')-1)/6
                    for pi,p in enumerate(order):
                        row=si*7+pi;matrix[row,ci]=ranks[pi]
                        glyph[row,ci]='H' if vals[pi]==vals.max() else 'L' if vals[pi]==vals.min() else ''
                        carrier.append({'panel':chr(97+panel),'platform':p,'scenario':s,'metric':c,'cell_median':float(vals[pi]),'scaled_rank':float(ranks[pi]),'marker':glyph[row,ci]})
            fig=plt.figure(figsize=(6.25,1604/300),dpi=300)
            ax=fig.add_axes([441/1875,(1604-1370)/1604,(1651-441)/1875,(1370-184)/1604])
            im=ax.imshow(matrix,cmap='viridis',vmin=0,vmax=1,aspect='auto',interpolation='nearest')
            ax.set_xticks(range(len(metrics)),xticks,fontsize=10)
            ax.set_yticks(range(14),[f'{s[0]} | {label}' for s in ss for label in labels],fontsize=10)
            ax.tick_params(which='both',length=0,pad=4)
            ax.set_xticks(np.arange(-.5,len(metrics),1),minor=True)
            ax.set_yticks(np.arange(-.5,14,1),minor=True)
            ax.grid(which='minor',color='#d0d0d0',linewidth=.35)
            ax.axhline(6.5,color='white',lw=1.2)
            for spine in ax.spines.values():spine.set_visible(False)
            for ri,ci in zip(*np.where(glyph!='')):
                ax.text(ci,ri,glyph[ri,ci],ha='center',va='center',fontsize=10,fontweight='bold',color='#151515',bbox={'boxstyle':'square,pad=0.06','facecolor':'white','edgecolor':'#aaaaaa','linewidth':.35})
            ca=fig.add_axes([.90,.205,.014,.57]);cb=fig.colorbar(im,cax=ca,ticks=[0,.5,1]);cb.ax.tick_params(labelsize=10,length=2)
            cb.outline.set_linewidth(.35)
            fig.text(.54,.967,f'Figure 4.9{chr(97+panel)}  {title}',ha='center',va='top',fontweight='bold',fontsize=11)
            fig.text(.54,.925,f'Scenarios {ss[0][0]}–{ss[1][0]}',ha='center',va='top',fontsize=10)
            fig.text(.54,.034,'Within-scenario rank: 0 = lower; 1 = higher magnitude',ha='center',va='center',fontsize=10)
            fig.savefig(out/f'image{22+panel}.png',dpi=300)
            fig.savefig(out/f'Figure_4_9{chr(97+panel)}.pdf')
            plt.close(fig);panel+=1
    pd.DataFrame(carrier).to_csv(out/'profile_336_cells.csv',index=False)
    assert len(carrier)==336 and sum(bool(x['marker']) for x in carrier)==104
    (out/'profile_redraw_summary.json').write_text(json.dumps({'panels':6,'cells':336,'high_low_markers':104,'font':'Nimbus Roman','minimum_font_pt':10,'width_in':6.25,'height_in':1604/300,'axes_pixels':[441,184,1651,1370],'basis':'Canonical unrounded cell medians and average ranks. Figure 4.9 numbering.'},indent=2))
    return out

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--master',required=True,type=Path)
    p.add_argument('--out',required=True,type=Path)
    args=p.parse_args()
    print(build(args.master,args.out))
