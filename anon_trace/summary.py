#!/usr/bin/env python3
import json, os
from collections import defaultdict
from analyze import WALLETS, LABEL, ANON, USDC, analyze, ds

# Aggregate ANON inflow/outflow by counterparty for each wallet
def agg(r):
    inn = defaultdict(lambda:[0.0,0,None,None])  # cp -> [amt, count, firstts, lastts]
    out = defaultdict(lambda:[0.0,0,None,None])
    buy = [0.0,0]   # anon, count
    sell = [0.0,0]
    for (ts,k,src,anon,ps,pu,cp,sig) in r['acquisitions']:
        if k=="BUY":
            buy[0]+=anon; buy[1]+=1
        else:
            e=inn[cp]; e[0]+=anon; e[1]+=1
            e[2]=ts if e[2] is None else min(e[2],ts); e[3]=ts if e[3] is None else max(e[3],ts)
    for (ts,k,src,anon,gs,gu,cp,sig) in r['disposals']:
        if k=="SELL":
            sell[0]+=anon; sell[1]+=1
        else:
            e=out[cp]; e[0]+=anon; e[1]+=1
            e[2]=ts if e[2] is None else min(e[2],ts); e[3]=ts if e[3] is None else max(e[3],ts)
    return inn,out,buy,sell

results = {}
for label,W in WALLETS.items():
    results[label]=analyze(label,W)

all_sources = set()
for label,W in WALLETS.items():
    r=results[label]
    inn,out,buy,sell=agg(r)
    print(f"\n{'='*72}\n{label}  {W}")
    if buy[1]: print(f"  MARKET BUYS : {buy[0]:14.2f} ANON in {buy[1]} swaps  (paid {r['sol_spent']:.2f} SOL + {r['usdc_spent']:.0f} USDC)")
    if sell[1]:print(f"  MARKET SELLS: {sell[0]:14.2f} ANON in {sell[1]} swaps (got  {r['sol_recv']:.2f} SOL + {r['usdc_recv']:.0f} USDC)")
    print(f"  --- ANON RECEIVED from wallets (transfer-in) ---")
    for cp,(amt,cnt,f,l) in sorted(inn.items(),key=lambda x:-x[1][0]):
        all_sources.add(cp)
        print(f"     {amt:14.2f} ANON  x{cnt:<3} from {LABEL.get(cp,cp)}  ({ds(f)}..{ds(l)})")
    print(f"  --- ANON SENT to wallets (transfer-out) ---")
    for cp,(amt,cnt,f,l) in sorted(out.items(),key=lambda x:-x[1][0]):
        print(f"     {amt:14.2f} ANON  x{cnt:<3} to   {LABEL.get(cp,cp)}  ({ds(f)}..{ds(l)})")

print("\n\nEXTERNAL SOURCE WALLETS to trace deeper:")
for s in sorted(all_sources):
    if s not in LABEL:
        print("  ",s)
