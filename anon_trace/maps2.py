#!/usr/bin/env python3
import graphviz

# ---------- MAP 2: Sonic -> Solana bridge -> hub -> 9 wallets ----------
g = graphviz.Digraph("bridge", format="png")
g.attr(rankdir="TB", bgcolor="white", fontname="Helvetica",
       label="\nANON FLOW — Sonic secondary market → LayerZero bridge → Solana cluster",
       labelloc="t", fontsize="20")
g.attr("node", fontname="Helvetica", style="filled", fontsize="11")

g.node("sec","SONIC secondary market\nSilo Finance 0xe453c128… + AMM pools",
       shape="box", fillcolor="#fff2cc", color="#bf9000", penwidth="2")
g.node("op","BRIDGE-OPERATOR EOAs (Sonic)\n0xd3f62c…  0x6fdb03…  0xeec654…\n(buy/borrow ANON, then bridge)",
       shape="box", fillcolor="#fce5cd")
g.node("lz","LayerZero OFT send\nSonic EID 30332 → Solana EID 30168\nOFT 0x79bbf4… (HeyAnon)",
       shape="box", fillcolor="#d9d2e9", color="#674ea7", penwidth="2")
g.node("rcv","SOLANA OFT mint (bridge-in)\nprog A1oayh35… · mint-auth 5AAcqak…\nreceivers: 7Mad6X… · 3Ea1u3vw…",
       shape="box", fillcolor="#c9daf8", color="#1155cc", penwidth="2")
g.node("mm","Solana MM relay\nFWznb… · EFE3j1… · 26hBWMo…", shape="box", fillcolor="#cfe2f3")
g.node("hub","HUB  6LY1Jz…\n408,772 SOL whale · ~3.3M ANON throughput\n(consolidates, then seeds)",
       shape="box", fillcolor="#f9cb9c", color="#b45f06", penwidth="2")

g.edge("sec","op"); g.edge("op","lz", label="OFT send")
g.edge("lz","rcv", penwidth="2", color="#674ea7"); g.edge("rcv","mm"); g.edge("mm","hub")

# 9 wallets
with g.subgraph(name="cluster_w") as c:
    c.attr(label="THE 9 WALLETS (MM / LP cluster)", color="#999999", style="dashed", fontsize="13")
    for w,addr in [("W1","9smQRa…"),("W2","5N9Za6…"),("W3","Bzog5A…"),("W4","AX9Yne…"),
                   ("W5","Fb2fQL…"),("W6","DsgCAF…"),("W7","4CNJAV…"),("W8","DNSG6z…"),("W9","DBGRA4…")]:
        c.node(w, f"{w}\n{addr}", shape="box", fillcolor="#d9ead3")

g.edge("hub","W1", label="49k + 60.7k MINT", fontsize="9")
g.edge("hub","W7", label="317k (sell leg)", fontsize="9", color="#cc0000", penwidth="2")
for w in ["W2","W3","W4","W5","W6","W8","W9"]:
    g.edge("hub", w, label="50k seed\n2026-03-23", fontsize="8")
g.node("note","All seeds dated 2026-03-23 (~19:00 UTC, 40-min window)\nW1 & W3 also received DIRECT bridge-mints (60.7k / 50k)",
       shape="note", fillcolor="#fff2cc", fontsize="10")

g.render("/home/user/wireframes-widgets/anon_trace/map2_bridge", cleanup=True)
print("map2 done")
