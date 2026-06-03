#!/usr/bin/env python3
import json, os, datetime
from collections import defaultdict

DATA = os.path.join(os.path.dirname(__file__), "data")
ANON="9McvH6w97oewLmPxqQEoHUAv3u5iYMyQ9AeZZhguYf1T"
USDC="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
WSOL="So11111111111111111111111111111111111111112"
OFT="A1oayh35gLkRG8fHcXtfdGJmbsubAeJA7URVVET3h8MZ"
ENDPOINT="76y77prsiCMvXMjuoZ5VRrhG5qYBrUMYTE5WgHqgjEn6"
PSOL=75.10954; PANON=0.46311364

WALLETS={"W1":"9smQRavJ9RLKcLEMhTVm79ZexSxiJvQV4kEuA9Vps1Az","W2":"5N9Za6GeatULoJnJVNrpo2G1PPasN8xkVwNuycZKgDAL",
 "W3":"Bzog5AyPJHGEfv4X9tzBVo9kLtQZ1oBg3reCLKNMDVTS","W4":"AX9YneaRtp32kLyWXichKC4jWq9VE3p9bXpv3ZAYaapn",
 "W5":"Fb2fQLWgFsWkehmBFQHjyxfo4PXc7MUJfrZq9zyQ5vUq","W6":"DsgCAFYGZ7sPmxzbz4JP25FyezmAwL3PKrb9qJJ1kZ2L",
 "W7":"4CNJAVg6q4DTaVmw26V4ZEUPhueEH5sKC4zrfCEtLCjL","W8":"DNSG6zxzA7VHdo5MYqMKZ7qpr7zcZuigdmZ1dtxTMddo",
 "W9":"DBGRA4erWgaR7fdNGgBpwWW8BUfAeEpZVoj7VG7G4yVu"}
LABEL={v:k for k,v in WALLETS.items()}
BAL={"W1":28412.631393638,"W2":597.93484531,"W3":212.766283379,"W4":1055.701942863,
 "W5":0.258378059,"W6":211.633020419,"W7":0.0,"W8":631.089187082,"W9":908.029484034}
# known counterparty roles (resolved earlier)
ROLE={
 "6LY1JzAFVZsP2a2xKrtU6znQMQ5h4i7tocWdgrkZzkzF":"HUB 6LY1Jz (bridged from Sonic via 7Mad6X/3Ea1u3vw)",
 "EYy5nwcFQHfSCKrrALgMB2DbU2vhszWHjuEdDFgAvfpu":"Raydium CLMM pool (LP/swap)",
 "Dab466PKkN59FfANKX2KN3RDbUstuxYPZ6SKGsTXKx8U":"ANON governance escrow",
 "GpMZbSM2GgvTKHJirzeGfMFoaZ8UR2X7F4v8vHTvxFbL":"GpMZb MM wallet",
 "4DXheh8P3X2jFWFwcVcqEqkNK7QV7vRdSA5kY337yYqs":"4DXheh8 drip distributor (closed)",
}
def ds(ts): return datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d") if ts else "?"
def progs(t):
    s=set()
    for i in t.get("instructions",[]):
        s.add(i.get("programId"))
        for inner in i.get("innerInstructions",[]) or []: s.add(inner.get("programId"))
    return s
def net_anon(t,W):
    n=0
    for ad in t.get("accountData",[]):
        for tb in ad.get("tokenBalanceChanges",[]) or []:
            if tb.get("userAccount")==W and tb.get("mint")==ANON:
                r=tb["rawTokenAmount"]; n+=int(r["tokenAmount"])/10**int(r["decimals"])
    return n
def net_mint(t,m,W):
    n=0
    for ad in t.get("accountData",[]):
        for tb in ad.get("tokenBalanceChanges",[]) or []:
            if tb.get("userAccount")==W and tb.get("mint")==m:
                r=tb["rawTokenAmount"]; n+=int(r["tokenAmount"])/10**int(r["decimals"])
    return n

def classify(W):
    txs=[t for t in json.load(open(os.path.join(DATA,f"{W}.json"))) if not t.get("transactionError")]
    txs.sort(key=lambda t:t.get("timestamp",0))
    mint=[0.0,0,None,None]            # bridged-in mints
    buy=[0.0,0,0.0,0.0]              # anon, n, sol_spent, usdc_spent
    claim=[0.0,0]                    # zero-cost LP-fee / reward claims
    xin=defaultdict(lambda:[0.0,0,None,None])
    sell=[0.0,0,0.0,0.0]            # anon, n, sol_recv, usdc_recv
    xout=defaultdict(lambda:[0.0,0])
    for t in txs:
        a=net_anon(t,W)
        if abs(a)<1e-9: continue
        p=progs(t); is_swap = t.get("type")=="SWAP" or (t.get("events") or {}).get("swap")
        # mint detection
        minted = any((tt.get("mint")==ANON and (tt.get("fromUserAccount") in (None,"")) and tt.get("toUserAccount")==W) for tt in t.get("tokenTransfers",[])) or (OFT in p) or (ENDPOINT in p)
        if a>0:
            if minted and not is_swap:
                mint[0]+=a; mint[1]+=1
                mint[2]=t["timestamp"] if mint[2] is None else min(mint[2],t["timestamp"]); mint[3]=max(mint[3] or 0,t["timestamp"])
            elif is_swap:
                solc=0
                for ad in t.get("accountData",[]):
                    if ad.get("account")==W: solc+=ad.get("nativeBalanceChange",0)/1e9
                solc+=net_mint(t,WSOL,W)  # include wrapped SOL leg
                usdc=net_mint(t,USDC,W)
                paid_sol=(-solc if solc<0 else 0); paid_usdc=(-usdc if usdc<0 else 0)
                cost_usd=paid_sol*PSOL+paid_usdc
                if cost_usd>0.5:   # genuine purchase
                    buy[0]+=a; buy[1]+=1; buy[2]+=paid_sol; buy[3]+=paid_usdc
                else:              # zero-cost inflow = LP fee / reward claim
                    claim[0]+=a; claim[1]+=1
            else:
                cp="?"
                for tt in t.get("tokenTransfers",[]):
                    if tt.get("mint")==ANON and tt.get("toUserAccount")==W and tt.get("fromUserAccount") not in (None,"",W): cp=tt["fromUserAccount"];break
                e=xin[cp]; e[0]+=a; e[1]+=1
                e[2]=t["timestamp"] if e[2] is None else min(e[2],t["timestamp"]); e[3]=max(e[3] or 0,t["timestamp"])
        else:
            aa=-a
            if is_swap:
                solc=0
                for ad in t.get("accountData",[]):
                    if ad.get("account")==W: solc+=ad.get("nativeBalanceChange",0)/1e9
                solc+=net_mint(t,WSOL,W)  # include wrapped SOL leg
                usdc=net_mint(t,USDC,W)
                sell[0]+=aa; sell[1]+=1; sell[2]+=(solc if solc>0 else 0); sell[3]+=(usdc if usdc>0 else 0)
            else:
                cp="?"
                for tt in t.get("tokenTransfers",[]):
                    if tt.get("mint")==ANON and tt.get("fromUserAccount")==W and tt.get("toUserAccount") not in (None,"",W): cp=tt["toUserAccount"];break
                xout[cp][0]+=aa; xout[cp][1]+=1
    return mint,buy,claim,xin,sell,xout

print(f"{'='*78}\nPER-WALLET ANON ACQUISITION: MINTED vs BOUGHT vs TRANSFERRED-IN\n{'='*78}")
SUM=defaultdict(float)
rows=[]
for lb,W in WALLETS.items():
    mint,buy,claim,xin,sell,xout=classify(W)
    tin=sum(v[0] for v in xin.values())
    print(f"\n### {lb}  {W}")
    print(f"  MINTED (bridged from Sonic) : {mint[0]:13.2f} ANON  ({mint[1]} mints, {ds(mint[2])}..{ds(mint[3])})")
    print(f"  BOUGHT (DEX swaps)          : {buy[0]:13.2f} ANON  ({buy[1]} swaps; paid {buy[2]:.3f} SOL + {buy[3]:.0f} USDC = ${buy[2]*PSOL+buy[3]:,.0f})")
    print(f"  CLAIMED (LP fees/rewards)   : {claim[0]:13.2f} ANON  ({claim[1]} zero-cost claims)")
    print(f"  TRANSFERRED-IN              : {tin:13.2f} ANON")
    for cp,(amt,cnt,f,l) in sorted(xin.items(),key=lambda x:-x[1][0]):
        role=ROLE.get(cp, LABEL.get(cp, "external "+cp[:8]))
        print(f"        {amt:13.2f} x{cnt:<3} from {role}  ({ds(f)}..{ds(l)})")
    sold=sell[0]; proceeds=sell[2]*PSOL+sell[3]; cost=buy[2]*PSOL+buy[3]
    realized=proceeds-cost
    invent=BAL[lb]*PANON
    print(f"  SOLD (DEX)                  : {sold:13.2f} ANON  -> got {sell[2]:.3f} SOL + {sell[3]:.0f} USDC = ${proceeds:,.0f}")
    print(f"  -- BOUGHT PnL: cost ${cost:,.0f}, sell proceeds ${proceeds:,.0f}, realized ${realized:,.0f}; current inventory {BAL[lb]:.0f} ANON = ${invent:,.0f}")
    SUM["mint"]+=mint[0]; SUM["buy"]+=buy[0]; SUM["claim"]+=claim[0]; SUM["tin"]+=tin; SUM["cost"]+=cost; SUM["proceeds"]+=proceeds; SUM["invent"]+=invent
print(f"\n{'='*78}\nCLUSTER TOTALS")
print(f"  Minted(bridged): {SUM['mint']:.0f} ANON | Bought: {SUM['buy']:.0f} ANON | Transferred-in: {SUM['tin']:.0f} ANON")
print(f"  Buy cost ${SUM['cost']:,.0f} | Sell proceeds ${SUM['proceeds']:,.0f} | Realized ${SUM['proceeds']-SUM['cost']:,.0f} | Inventory ${SUM['invent']:,.0f}")
print(f"  Prices: SOL ${PSOL:.2f}, ANON ${PANON:.4f}")
