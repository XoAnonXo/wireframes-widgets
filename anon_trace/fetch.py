#!/usr/bin/env python3
"""Fetch full enhanced transaction history for an address from Helius and cache to disk."""
import sys, json, os, time, urllib.request, urllib.error

KEY = "e04f2d3a-6d17-4a5c-94c3-ad4004bafa85"
DATA = os.path.join(os.path.dirname(__file__), "data")

def fetch_all(address):
    out = []
    before = None
    while True:
        url = f"https://api.helius.xyz/v0/addresses/{address}/transactions?api-key={KEY}&limit=100"
        if before:
            url += f"&before={before}"
        for attempt in range(5):
            try:
                req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"})
                with urllib.request.urlopen(req, timeout=60) as r:
                    batch = json.load(r)
                break
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    time.sleep(2 * (attempt + 1)); continue
                print("HTTP", e.code, e.read()[:200]);
                if attempt == 4: raise
                time.sleep(2)
            except Exception as e:
                print("err", e); time.sleep(2*(attempt+1))
                if attempt == 4: raise
        if not batch:
            break
        out.extend(batch)
        before = batch[-1]["signature"]
        print(f"  {address[:6]}.. fetched {len(out)} (last ts {batch[-1].get('timestamp')})", flush=True)
        if len(batch) < 100:
            break
        time.sleep(0.3)
    return out

if __name__ == "__main__":
    addr = sys.argv[1]
    path = os.path.join(DATA, f"{addr}.json")
    if os.path.exists(path) and os.path.getsize(path) > 2:
        print(f"cached {addr}")
        sys.exit(0)
    txs = fetch_all(addr)
    with open(path, "w") as f:
        json.dump(txs, f)
    print(f"saved {len(txs)} txs for {addr}")
