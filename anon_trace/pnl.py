#!/usr/bin/env python3
import json, os
from analyze import WALLETS

PSOL=75.10954
PANON=0.46311364
BAL={  # current ANON balances (from getTokenAccountsByOwner)
 "W1":28412.631393638,"W2":597.93484531,"W3":212.766283379,"W4":1055.701942863,
 "W5":0.258378059,"W6":211.633020419,"W7":0.0,"W8":631.089187082,"W9":908.029484034}

r=json.load(open(os.path.join(os.path.dirname(__file__),"data","_analysis.json")))
tot={}
print(f"{'W':<3}{'buys$':>11}{'sells$':>11}{'swapPnL$':>11}{'holdANON':>13}{'holdVal$':>11}{'netPnL$':>11}")
print("-"*71)
agg=[0,0,0,0]
for label in WALLETS:
    d=r[label]
    buys = float(d['sol_spent'])*PSOL + float(d['usdc_spent'])
    sells= float(d['sol_recv'])*PSOL + float(d['usdc_recv'])
    swappnl = sells-buys
    hold = BAL[label]
    holdval = hold*PANON
    net = swappnl + holdval
    print(f"{label:<3}{buys:>11.0f}{sells:>11.0f}{swappnl:>11.0f}{hold:>13.2f}{holdval:>11.0f}{net:>11.0f}")
    agg[0]+=buys; agg[1]+=sells; agg[2]+=holdval; agg[3]+=net
print("-"*71)
print(f"{'SUM':<3}{agg[0]:>11.0f}{agg[1]:>11.0f}{agg[1]-agg[0]:>11.0f}{'':>13}{agg[2]:>11.0f}{agg[3]:>11.0f}")
print(f"\nPrices used: SOL=${PSOL:.2f}  ANON=${PANON:.4f}")
print("buys$/sells$ = cash spent/received via DEX swaps only (excludes free intra-cluster transfers)")
print("netPnL$ = swap cashflow + current ANON inventory value at mark")
