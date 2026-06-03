#!/usr/bin/env python3
"""Render ANON origination mind maps to PNG via graphviz."""
import graphviz

# ---------- MAP 1: Origination on Sonic (genesis -> distribution) ----------
g = graphviz.Digraph("origination", format="png")
g.attr(rankdir="TB", bgcolor="white", fontname="Helvetica",
       label="\nANON ORIGINATION — Sonic genesis (2024-12-14)  •  total supply 21,000,000",
       labelloc="t", fontsize="20")
g.attr("node", fontname="Helvetica", style="filled", fontsize="11")

g.node("mint", "GENESIS MINT\n21,000,000 ANON\nblock 406,529 · 2024-12-14\ntx 0xf1369d28…",
       shape="box", fillcolor="#ffd966", color="#bf9000", penwidth="2")
g.node("dep", "Deployer EOA\n0x8054a4fb…", shape="box", fillcolor="#f4cccc")
g.node("tre", "HeyAnon TREASURY (Safe)\n0xb3fc32de…  (= token owner)\nholds 7.10M reserve",
       shape="box", fillcolor="#d9ead3", color="#38761d", penwidth="2")

g.node("sale", "SALE CONTRACT\n0xca420d5e…\n10,500,000 ANON (50%)\nsold @ $1 vs user deposits",
       shape="box", fillcolor="#c9daf8", color="#1155cc", penwidth="2")
g.node("buyers", "558 PUBLIC-SALE BUYERS\n(deposited ≈ $10.5M)\nlots of 60k–569k ANON each",
       shape="box", fillcolor="#cfe2f3")
g.node("safe2", "Team Safe\n0xa930ed3e…\n1,050,000", shape="box", fillcolor="#fce5cd")
g.node("dex", "INITIAL DEX LIQUIDITY\npool/router 0x297000941…\n259,419", shape="box", fillcolor="#ead1dc")
g.node("team", "Team / MM / investor wallets\n~12 addresses · 100k–150k each", shape="box", fillcolor="#fce5cd")
g.node("burn", "Bridged out (burn → 0x0)\n161,300 → other chains", shape="box", fillcolor="#efefef")

g.edge("mint","dep", label="minted to self")
g.edge("dep","tre", label="21,000,000 (100%)", penwidth="2")
g.edge("tre","sale", label="10.5M")
g.edge("sale","buyers", label="@ $1")
g.edge("tre","safe2", label="1.05M")
g.edge("tre","dex", label="259k")
g.edge("tre","team", label="~1.2M")
g.edge("tre","burn", label="161k")

# link to secondary market / bridge path
g.node("sec", "SECONDARY MARKET (Sonic)\nSilo Finance ANON market 0xe453c128…\n+ Sonic AMM pools",
       shape="box", fillcolor="#fff2cc", color="#bf9000")
g.edge("dex","sec", label="provides\nliquidity", style="dashed")
g.edge("buyers","sec", label="sell / LP", style="dashed")
g.node("brg", "▶ continues to BRIDGE MAP\n(operators buy/borrow here,\nbridge to Solana)", shape="box",
       fillcolor="#d9d2e9", color="#674ea7", penwidth="2")
g.edge("sec","brg", penwidth="2", color="#674ea7")

g.render("/home/user/wireframes-widgets/anon_trace/map1_origination", cleanup=True)
print("map1 done")
