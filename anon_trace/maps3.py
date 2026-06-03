#!/usr/bin/env python3
import graphviz

# ---------- MAP 3: per-wallet acquisition + PnL ----------
# data: (W, addr, seed, mint, bought, buycost, claims, sold_proceeds, net_pnl, holds_usd)
rows = [
 ("W1","9smQRa…",49000,60699,7462,4161,18221,110,-4051,13158),
 ("W2","5N9Za6…",50000,0,598,315,9637,202,-113,277),
 ("W3","Bzog5A…",50000,50000,6594,4864,7972,114,-4750,99),
 ("W4","AX9Yne…",50000,0,1055,563,9869,131,-432,489),
 ("W5","Fb2fQL…",50000,0,0,0,15218,465,465,0),
 ("W6","DsgCAF…",50000,0,211,113,14234,588,475,98),
 ("W7","4CNJAV…",317210,0,7812,3755,0,32286,28530,0),
 ("W8","DNSG6z…",50000,0,631,338,14114,588,250,292),
 ("W9","DBGRA4…",50000,0,908,488,0,589,101,421),
]
g = graphviz.Digraph("pnl", format="png")
g.attr(rankdir="LR", bgcolor="white", fontname="Helvetica",
       label="\nHOW EACH WALLET ACQUIRED ANON  +  PnL    (marks: SOL $75.11, ANON $0.4631)",
       labelloc="t", fontsize="20")
g.attr("node", fontname="Helvetica", style="filled", fontsize="10", shape="box")

g.node("src","ANON SOURCES", shape="box", fillcolor="#ffd966", fontsize="13")
g.node("seed","① SEED transfer\nfrom hub 6LY1Jz\n(bridged-origin)", fillcolor="#f9cb9c")
g.node("mint","② DIRECT bridge-MINT\nfrom Sonic", fillcolor="#c9daf8")
g.node("buy","③ BOUGHT on DEX\n(paid SOL/USDC)", fillcolor="#d9ead3")
g.node("claim","④ LP-fee / reward\nCLAIMS (free)", fillcolor="#e6e6e6")
for n in ["seed","mint","buy","claim"]: g.edge("src",n)

for (w,addr,seed,mint,bought,cost,claims,proc,pnl,hold) in rows:
    col = "#d9ead3" if pnl>=0 else "#f4cccc"
    label = (f"{w}  {addr}\n"
             f"seed {seed:,}  | mint {mint:,}\n"
             f"bought {bought:,} (cost ${cost:,})\n"
             f"claims {claims:,} | holds ${hold:,}\n"
             f"── net DEX PnL ${pnl:,} ──")
    g.node(w, label, fillcolor=col, penwidth=("2" if abs(pnl)>3000 else "1"))
    g.edge("seed", w, style="dashed", color="#b45f06")
    if mint>0: g.edge("mint", w, color="#1155cc", penwidth="2")
    if bought>0: g.edge("buy", w, color="#38761d")
    if claims>0: g.edge("claim", w, style="dotted")

g.node("tot","CLUSTER TOTALS\nBought 25,270 ANON for $14,598\nSold for $35,073 → realized +$20,475\n(≈ all from W7)\nInventory held $14,834\nMint(bridged) 110,699 | Seed ~716,210 (free)",
       shape="box", fillcolor="#fff2cc", fontsize="11", penwidth="2")

g.render("/home/user/wireframes-widgets/anon_trace/map3_pnl", cleanup=True)
print("map3 done")
