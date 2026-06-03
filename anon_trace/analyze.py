#!/usr/bin/env python3
import json, os, sys

DATA = os.path.join(os.path.dirname(__file__), "data")
ANON = "9McvH6w97oewLmPxqQEoHUAv3u5iYMyQ9AeZZhguYf1T"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
WSOL = "So11111111111111111111111111111111111111112"

WALLETS = {
 "W1":"9smQRavJ9RLKcLEMhTVm79ZexSxiJvQV4kEuA9Vps1Az",
 "W2":"5N9Za6GeatULoJnJVNrpo2G1PPasN8xkVwNuycZKgDAL",
 "W3":"Bzog5AyPJHGEfv4X9tzBVo9kLtQZ1oBg3reCLKNMDVTS",
 "W4":"AX9YneaRtp32kLyWXichKC4jWq9VE3p9bXpv3ZAYaapn",
 "W5":"Fb2fQLWgFsWkehmBFQHjyxfo4PXc7MUJfrZq9zyQ5vUq",
 "W6":"DsgCAFYGZ7sPmxzbz4JP25FyezmAwL3PKrb9qJJ1kZ2L",
 "W7":"4CNJAVg6q4DTaVmw26V4ZEUPhueEH5sKC4zrfCEtLCjL",
 "W8":"DNSG6zxzA7VHdo5MYqMKZ7qpr7zcZuigdmZ1dtxTMddo",
 "W9":"DBGRA4erWgaR7fdNGgBpwWW8BUfAeEpZVoj7VG7G4yVu",
}
LABEL = {v:k for k,v in WALLETS.items()}

def net_changes(t, W):
    """Return (sol_change, token_changes dict) for wallet W in tx t."""
    sol = 0
    for ad in t.get("accountData", []):
        if ad.get("account") == W:
            sol += ad.get("nativeBalanceChange", 0)
    tok = {}
    for ad in t.get("accountData", []):
        for tb in ad.get("tokenBalanceChanges", []) or []:
            if tb.get("userAccount") == W:
                m = tb.get("mint")
                raw = tb.get("rawTokenAmount", {})
                amt = int(raw.get("tokenAmount", 0)) / (10 ** int(raw.get("decimals", 0)))
                tok[m] = tok.get(m, 0) + amt
    return sol / 1e9, tok

def anon_counterparties(t, W, incoming):
    """For a transfer, find counterparties moving ANON to/from W (by ATA owner)."""
    cps = []
    for tt in t.get("tokenTransfers", []):
        if tt.get("mint") != ANON:
            continue
        f, to = tt.get("fromUserAccount"), tt.get("toUserAccount")
        if incoming and to == W and f != W:
            cps.append((f, tt.get("tokenAmount")))
        if not incoming and f == W and to != W:
            cps.append((to, tt.get("tokenAmount")))
    return cps

def analyze(label, W):
    txs = json.load(open(os.path.join(DATA, f"{W}.json")))
    txs = [t for t in txs if not t.get("transactionError")]
    txs.sort(key=lambda t: t.get("timestamp", 0))
    acquisitions, disposals = [], []
    sol_spent=sol_recv=usdc_spent=usdc_recv=0.0
    anon_in_swap=anon_out_swap=anon_in_xfer=anon_out_xfer=0.0
    for t in txs:
        sol, tok = net_changes(t, W)
        anon = tok.get(ANON, 0)
        if abs(anon) < 1e-9:
            continue
        usdc = tok.get(USDC, 0)
        typ, src = t.get("type"), t.get("source")
        ts = t.get("timestamp")
        sig = t.get("signature")
        is_swap = typ == "SWAP" or (t.get("events") or {}).get("swap")
        if anon > 0:  # acquired
            if is_swap:
                paid_sol = -sol if sol < 0 else 0
                paid_usdc = -usdc if usdc < 0 else 0
                sol_spent += paid_sol; usdc_spent += paid_usdc
                anon_in_swap += anon
                acquisitions.append((ts, "BUY", src, anon, paid_sol, paid_usdc, None, sig))
            else:
                cps = anon_counterparties(t, W, True)
                anon_in_xfer += anon
                cp = cps[0][0] if cps else "?"
                acquisitions.append((ts, typ, src, anon, 0,0, cp, sig))
        else:  # disposed
            a = -anon
            if is_swap:
                got_sol = sol if sol > 0 else 0
                got_usdc = usdc if usdc > 0 else 0
                sol_recv += got_sol; usdc_recv += got_usdc
                anon_out_swap += a
                disposals.append((ts, "SELL", src, a, got_sol, got_usdc, None, sig))
            else:
                cps = anon_counterparties(t, W, False)
                anon_out_xfer += a
                cp = cps[0][0] if cps else "?"
                disposals.append((ts, typ, src, a, 0,0, cp, sig))
    return dict(label=label, W=W, acquisitions=acquisitions, disposals=disposals,
        sol_spent=sol_spent, sol_recv=sol_recv, usdc_spent=usdc_spent, usdc_recv=usdc_recv,
        anon_in_swap=anon_in_swap, anon_out_swap=anon_out_swap,
        anon_in_xfer=anon_in_xfer, anon_out_xfer=anon_out_xfer)

import datetime
def ds(ts): return datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d") if ts else "?"

if __name__ == "__main__":
    results = {}
    for label, W in WALLETS.items():
        results[label] = analyze(label, W)
    json.dump(results, open(os.path.join(DATA,"_analysis.json"),"w"), default=str)
    for label, W in WALLETS.items():
        r = results[label]
        print(f"\n{'='*70}\n{label}  {W}")
        print(f"  ANON acquired: swap={r['anon_in_swap']:.2f}  transfer-in={r['anon_in_xfer']:.2f}")
        print(f"  ANON disposed: swap={r['anon_out_swap']:.2f}  transfer-out={r['anon_out_xfer']:.2f}")
        print(f"  SOL spent={r['sol_spent']:.3f} recv={r['sol_recv']:.3f} | USDC spent={r['usdc_spent']:.2f} recv={r['usdc_recv']:.2f}")
        print(f"  --- ACQUISITIONS ({len(r['acquisitions'])}) ---")
        for (ts,k,src,anon,ps,pu,cp,sig) in r['acquisitions']:
            extra = f"paid {ps:.3f}SOL/{pu:.2f}USDC" if k=="BUY" else f"FROM {LABEL.get(cp,cp)}"
            print(f"    {ds(ts)} {k:6} {anon:14.3f} ANON  {extra}  [{src}]")
        print(f"  --- DISPOSALS ({len(r['disposals'])}) ---")
        for (ts,k,src,anon,gs,gu,cp,sig) in r['disposals']:
            extra = f"got {gs:.3f}SOL/{gu:.2f}USDC" if k=="SELL" else f"TO {LABEL.get(cp,cp)}"
            print(f"    {ds(ts)} {k:6} {anon:14.3f} ANON  {extra}  [{src}]")
