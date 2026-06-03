#!/usr/bin/env python3
"""Trace incoming/outgoing ANON ERC20 transfers on Sonic via chunked eth_getLogs."""
import sys, json, urllib.request, time

RPCS = ["https://sonic-rpc.publicnode.com","https://rpc.soniclabs.com","https://sonic.drpc.org"]
ANON = "0x79bbf4508b1391af3a0f4b30bb5fc4aa9ab0e07c"
TRANSFER = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
ZERO = "0x0000000000000000000000000000000000000000"

def rpc(method, params):
    body = json.dumps({"jsonrpc":"2.0","id":1,"method":method,"params":params}).encode()
    last=None
    for r in RPCS:
        for attempt in range(2):
            try:
                req=urllib.request.Request(r, data=body, headers={"Content-Type":"application/json","User-Agent":"Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=40) as resp:
                    d=json.load(resp)
                if "error" in d: last=d["error"]; break
                return d["result"]
            except Exception as e:
                last=str(e); time.sleep(1)
    raise RuntimeError(last)

def pad(addr): return "0x"+"0"*24+addr.lower()[2:]

def get_transfers(direction, addr, from_blk, to_blk, chunk=200000):
    """direction 'in' -> topic2=addr ; 'out' -> topic1=addr"""
    topics=[TRANSFER, None, None]
    if direction=="in": topics[2]=pad(addr)
    else: topics[1]=pad(addr)
    out=[]
    b=from_blk
    while b<=to_blk:
        e=min(b+chunk-1,to_blk)
        try:
            logs=rpc("eth_getLogs",[{"fromBlock":hex(b),"toBlock":hex(e),"address":ANON,"topics":topics}])
        except RuntimeError as ex:
            if chunk>2000:
                # subdivide
                for sb in range(b,e+1, chunk//5):
                    se=min(sb+chunk//5-1,e)
                    logs=rpc("eth_getLogs",[{"fromBlock":hex(sb),"toBlock":hex(se),"address":ANON,"topics":topics}])
                    for l in logs: out.append(parse(l))
                b=e+1; continue
            else: raise
        for l in logs: out.append(parse(l))
        b=e+1
    return out

def parse(l):
    return dict(blk=int(l["blockNumber"],16),
                frm="0x"+l["topics"][1][26:], to="0x"+l["topics"][2][26:],
                amt=int(l["data"],16)/1e18, tx=l["transactionHash"])

if __name__=="__main__":
    direction=sys.argv[1]; addr=sys.argv[2]
    fb=int(sys.argv[3]); tb=int(sys.argv[4])
    ts=get_transfers(direction,addr,fb,tb)
    ts.sort(key=lambda x:x["blk"])
    from collections import defaultdict
    agg=defaultdict(lambda:[0.0,0])
    for t in ts:
        cp = t["frm"] if direction=="in" else t["to"]
        agg[cp][0]+=t["amt"]; agg[cp][1]+=1
    print(f"{direction} ANON for {addr}: {len(ts)} transfers, blocks {fb}-{tb}")
    for cp,(amt,cnt) in sorted(agg.items(),key=lambda x:-x[1][0]):
        tag=" (MINT/burn)" if cp==ZERO else ""
        print(f"  {amt:16.2f} ANON x{cnt:<4} {'from' if direction=='in' else 'to'} {cp}{tag}")
