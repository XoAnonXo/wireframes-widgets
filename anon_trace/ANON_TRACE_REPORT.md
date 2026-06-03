# ANON Token On-Chain Investigation — 9 Wallets

**Token:** HeyAnon — symbol **ANON** — mint `9McvH6w97oewLmPxqQEoHUAv3u5iYMyQ9AeZZhguYf1T` (9 decimals)
**Date of analysis:** 2026-06-03 · **Data source:** Helius RPC + Enhanced Transactions API
**Marks used:** SOL = $75.11, ANON = $0.4631 (Helius price feed; internally consistent with on-chain swap ratios)

---

## 1. Executive summary

The 9 wallets are **one coordinated cluster acting as market-makers / LPs for ANON**, not independent holders. The evidence:

- **Every wallet was seeded with ~50,000 ANON on the exact same day — 2026-03-23 — from a single wallet `6LY1Jz…`** (within a ~40-minute window that evening, ~19:00–19:40 UTC).
- They all interact with the **same three venues**: the **Raydium CLMM ANON pool** (`EYy5nw…`), the **ANON DAO governance/vote-staking escrow** (`Dab466…`), and they all market-buy small amounts on **Jupiter/Raydium**.
- They shuffle ANON among themselves and back to `6LY1Jz`.

**Where the ANON came from (the trail):**

```
ANON launch / treasury (early–mid 2025)
        │
        ▼
  MM / ops network  ── FWznb…, 26hBWMo…, EFE3j1…, 7Mad6X…, 2vMBmeEp…, 3Ea1u3vw… (active since Feb 2025)
        │
        ▼
  6LY1Jz…  ← THE HUB (whale: 408,772 SOL; ~3.3M ANON throughput since Sep 2025)
        │  seeds 50,000 ANON to each of the 9 wallets on 2026-03-23 (W7 got far more, from Feb 2026)
        ▼
  W1 W2 W3 W4 W5 W6 W7 W8 W9   ← the 9 target wallets
        │
        ▼  (then they: buy on Jupiter/Raydium, LP into Raydium CLMM pool EYy5, stake in governance Dab466)
```

**Bottom line on the source question:** the proximate source for all 9 is **`6LY1JzAFVZsP2a2xKrtU6znQMQ5h4i7tocWdgrkZzkzF`**. That hub in turn was fed by a market-making/operations cluster (FWznb, 26hBWMo, EFE3j1, …) whose own ANON traces back to the token's launch in early 2025.

---

## 2. Where each wallet got its ANON

All amounts in ANON. "Seed" = the 50k transfer from `6LY1Jz` on 2026-03-23. "Pool `EYy5`" = Raydium CLMM (LP add/remove + swaps, large bidirectional). "Gov `Dab466`" = governance stake/unstake (round-trip, same-day in≈out).

| W | Address | Initial source(s) | Market buys | Current ANON |
|---|---------|-------------------|-------------|--------------|
| W1 | `9smQRavJ9RLKcLEMhTVm79ZexSxiJvQV4kEuA9Vps1Az` | **50k seed** from 6LY1Jz (via 49k relay 6LY1Jz→…), + 43k from Dab466 (gov), + 101k from pool EYy5, + drip 6.9k from `4DXheh8` | 25,683 in 121 swaps (1.5 SOL + 4,047 USDC) | **28,412.6** |
| W2 | `5N9Za6GeatULoJnJVNrpo2G1PPasN8xkVwNuycZKgDAL` | **50k seed** from 6LY1Jz, + 41.5k pool EYy5, + 41.3k gov Dab466 | 10,234 in 101 swaps (4.2 SOL) | 597.9 |
| W3 | `Bzog5AyPJHGEfv4X9tzBVo9kLtQZ1oBg3reCLKNMDVTS` | **50k seed** from 6LY1Jz, + 93k pool EYy5, + 43k gov Dab466 | 14,565 in 120 swaps (1.5 SOL + 4,751 USDC) | 212.8 |
| W4 | `AX9YneaRtp32kLyWXichKC4jWq9VE3p9bXpv3ZAYaapn` | **50k seed** from 6LY1Jz, + 41.2k pool EYy5, + 41k gov Dab466 | 10,925 in 101 swaps (7.5 SOL) | 1,055.7 |
| W5 | `Fb2fQLWgFsWkehmBFQHjyxfo4PXc7MUJfrZq9zyQ5vUq` | **50k seed** from 6LY1Jz, + 37.3k pool EYy5, + 36.7k gov Dab466 | 15,218 in 153 swaps | 0.26 |
| W6 | `DsgCAFYGZ7sPmxzbz4JP25FyezmAwL3PKrb9qJJ1kZ2L` | **50k seed** from 6LY1Jz, + 37.3k pool EYy5, + 36.6k gov Dab466 | 14,446 in 154 swaps (1.5 SOL) | 211.6 |
| W7 | `4CNJAVg6q4DTaVmw26V4ZEUPhueEH5sKC4zrfCEtLCjL` | **317k** from 6LY1Jz (4 tx, **from 2026-02-03** — earlier & far larger than the others) + 311k from pool EYy5 | 7,812 in 1 swap (50 SOL) | **0** (fully sold) |
| W8 | `DNSG6zxzA7VHdo5MYqMKZ7qpr7zcZuigdmZ1dtxTMddo` | **50k seed** from 6LY1Jz, + 37.3k pool EYy5, + 36.6k gov Dab466 | 14,744 in 151 swaps (4.5 SOL) | 631.1 |
| W9 | `DBGRA4erWgaR7fdNGgBpwWW8BUfAeEpZVoj7VG7G4yVu` | **50k seed** from 6LY1Jz, + 37.3k pool EYy5, + 36.6k gov Dab466 | 908 in 2 swaps (6.5 SOL) | 908.0 |

**W7 is the odd one out / sub-distributor:** it started receiving ANON from `6LY1Jz` on **2026-02-03** (≈7 weeks before the others), handled ~317k, and is the only one that **sold heavily** (317k ANON → 55 SOL + 28k USDC). It looks like the cluster's primary "sell leg," while W1/W3 are the "accumulate/inventory" legs.

---

## 3. The hub: `6LY1Jz…` (deep trace)

`6LY1JzAFVZsP2a2xKrtU6znQMQ5h4i7tocWdgrkZzkzF` — system-owned **real wallet**, holds **408,772 SOL** (~$30M) and **~345,600 ANON** today. Its ANON token account alone has **7,100+ transactions** dating to **Sep 2025**. Total ANON throughput ≈ **3.33M in / 2.98M out** — i.e. a high-volume operations/market-maker wallet, not a personal holder.

On **2026-03-23 evening** it simultaneously (a) *received* large ANON chunks from many wallets (88k from `H4utVsb…`, 75k from `2Ld8TH…`, 66k from `r6piJC…`, 59k from `7ihJNk…`, 55k from `EGNK7Z…`, 54k from `Fp3FUZ…`) and (b) *sent out* the 50k seeds to the 9 targets — a coordinated reshuffle.

**Top sources that fed `6LY1Jz` its ANON:**

| Source | ANON in | # tx | First seen | Note |
|--------|--------:|-----:|-----------|------|
| `26hBWMoVyxyF4oho4acyMeSVkAHuZtUxTfVgtkPgL7s2` | 907,328 | 2,242 | 2025-09-26 | primary MM counterparty (bidirectional) |
| `EFE3j1pcSP1paUzA86zW7989ZjsFP2J7ginyUqo4ewqR` | 492,196 | 78 | 2025-09-30 | real wallet, 20,972 SOL; holds 424k ANON |
| `7Mad6XFBMpSyQEwAJFcUpHYwuJVb221zBTRmMh5qoLhY` | 446,153 | 7 | 2025-10-11 | |
| `FWznbcNXWQuHTawe9RxvQ2LdCENssh12dsznf4RiouN5` | 226,830 | 3 | **2025-09-26** | **earliest funder** (see §4) |
| `DV2jugDHDeFpPQxEuofsMPyNkrDRUHy1mobzdLwH9Zte` | 121,492 | 413 | 2026-04-07 | |
| `6Hqw4zLdk7bkGotQ4KvtFuroQUbwAeaDNgE9ffPCh9Em` | 100,362 | 334 | 2026-02-12 | |

---

## 4. One level deeper: `FWznb…` (closest to origin)

`FWznbcNXWQuHTawe9RxvQ2LdCENssh12dsznf4RiouN5` was 6LY1Jz's earliest funder. Its own ANON account has **3,424 tx dating back to 2025-02-24** — essentially the **ANON launch window** (HeyAnon launched early 2025). Its top inflows come from yet more MM wallets — `2vMBmeEp…` (348k), `3Ea1u3vw…` (314k), and again `26hBWMo…` (280k, 1,433 tx) — a tightly interlinked market-making web. At this depth the trail converges on the **token's initial distribution / treasury and its market-making infrastructure** rather than any single external wallet.

**Conclusion of the trace:** the ANON ultimately originates from the **HeyAnon token launch/treasury (early 2025)**, flowed through a **market-making/operations cluster** (FWznb → 26hBWMo/EFE3j1/7Mad6X → 6LY1Jz), and `6LY1Jz` is the wallet that directly funded all 9 targets.

---

## 5. Key counterparties (reference)

| Address | What it is |
|---------|-----------|
| `9McvH6w97oewLmPxqQEoHUAv3u5iYMyQ9AeZZhguYf1T` | **ANON mint** (HeyAnon) |
| `6LY1JzAFVZsP2a2xKrtU6znQMQ5h4i7tocWdgrkZzkzF` | **The hub** — funded all 9 wallets (whale, 408k SOL) |
| `EYy5nwcFQHfSCKrrALgMB2DbU2vhszWHjuEdDFgAvfpu` | **Raydium CLMM ANON pool** (owner `CAMMCzo5…`) — LP/swap, not a peer wallet |
| `Dab466PKkN59FfANKX2KN3RDbUstuxYPZ6SKGsTXKx8U` | **ANON governance / vote-staking escrow** (owner `GovER5L…`) |
| `GpMZbSM2GgvTKHJirzeGfMFoaZ8UR2X7F4v8vHTvxFbL` | Real wallet / MM bot (1,274 SOL; holds ~174k ANON) — appears in swap routes |
| `4DXheh8P3X2jFWFwcVcqEqkNK7QV7vRdSA5kY337yYqs` | Drip-distributor to W1 (now closed) |
| `26hBWMo…`, `EFE3j1…`, `FWznb…`, `7Mad6X…` | Upstream MM/ops network feeding the hub |

---

## 6. PnL

Two views. **"Swap PnL"** = realized cash from DEX swaps only — cash received selling ANON minus cash spent buying it (it *excludes* the free intra-cluster transfers and the 50k seeds, which had no cash cost to these wallets). **"Net PnL"** adds the current ANON inventory marked to market.

| W | Bought ($) | Sold ($) | Swap PnL ($) | Holdings (ANON) | Holdings ($) | **Net PnL ($)** |
|---|----------:|---------:|-------------:|----------------:|-------------:|----------------:|
| W1 | 4,161 | 110 | −4,051 | 28,412.6 | 13,158 | **+9,107** |
| W2 | 315 | 202 | −113 | 597.9 | 277 | +164 |
| W3 | 4,864 | 114 | −4,750 | 212.8 | 99 | **−4,652** |
| W4 | 563 | 131 | −432 | 1,055.7 | 489 | +57 |
| W5 | 0 | 465 | +465 | 0.3 | 0 | +465 |
| W6 | 113 | 588 | +475 | 211.6 | 98 | +573 |
| W7 | 3,755 | 32,286 | +28,530 | 0 | 0 | **+28,530** |
| W8 | 338 | 588 | +250 | 631.1 | 292 | +542 |
| W9 | 488 | 589 | +101 | 908.0 | 421 | +522 |
| **SUM** | **14,598** | **35,073** | **+20,475** | — | **14,834** | **+35,308** |

**Interpretation:**
- The cluster's realized swap PnL is **+$20.5k**, driven almost entirely by **W7 (+$28.5k)**, the sell leg.
- **W1 and W3 are "buy/accumulate" legs** — they spent the most cash buying (W1 $4.2k, W3 $4.9k, partly with USDC) and W1 still sits on **28.4k ANON ($13.2k)** inventory.
- **Important caveat:** these wallets received ~**450k ANON for free** as seeds from `6LY1Jz` plus large amounts via pool/governance. That inventory was largely cycled back into the Raydium pool (LP) and back to the hub. So the PnL above is the **trading-cashflow PnL of these individual wallets**; the seeds themselves were the hub's capital, not these wallets' earned profit. Viewed as a unit, this is MM/LP operations on top of hub-supplied inventory rather than directional retail profit.

---

## 7. The bridge: ANON enters Solana from Sonic via LayerZero (cross-chain origin)

The ANON in this cluster did **not** originate natively on Solana — it was **bridged in from Sonic via the LayerZero OFT**, and the Solana mint is a mint-and-burn OFT.

**Solana-side OFT infrastructure (confirmed on-chain):**
- ANON mint authority `5AAcqakSbTFjXhRDfrczyn1Gz12EcKPkrJZHgfEANprv` is a **1-of-1 SPL multisig** whose sole signer is the PDA `8SQ1Uj92fSiKnu7Ydo81CMEWx1DkrubLrRYL9HqPh2oq`, owned by the **LayerZero OFT program `A1oayh35gLkRG8fHcXtfdGJmbsubAeJA7URVVET3h8MZ`**. Every Solana bridge-in **mints** new ANON to the recipient (that PDA is also the LayerZero `receiver`). The mint authority account has **48,061 transactions** — i.e. tens of thousands of bridge-in mints.
- Filtering those mints to our cluster shows the seeds were **bridge-minted**, not created on Solana:
  - **`7Mad6X…`** received **446,153 ANON via OFT mints on 2025-10-11/12**, then forwarded the *exact same* 446,153 to the hub `6LY1Jz` — a 1:1 bridge→hub relay.
  - **`3Ea1u3vw…`** was bridge-minted ~330k ANON (Jun–Jul 2025) → fed `FWznb` → hub.
  - **`W1` itself** received a **60,699 ANON bridge-mint on 2026-04-11** (this is the "unresolved/blank source" flagged in §2).

**LayerZero pathway (from LayerZero Scan):**
- **Source chain EID `30332` = Sonic** → **Destination EID `30168` = Solana**, status `DELIVERED`.
- Source OFT contract on Sonic: **`0x79bbf4508b1391af3a0f4b30bb5fc4aa9ab0e07c`** (symbol `Anon`, "HeyAnon").
- Example matched messages (Solana mint ⇐ Sonic `send`):

| Solana mint → | Sonic source tx | Sonic sender (EOA) |
|---|---|---|
| 7Mad6X 100k (2025-10-12) | `0x33e34c67…646ae4` | `0xd3f62ccbe87abf905c6611a524d76e6069883350` |
| 3Ea1u3vw 60k (2025-07-05) | `0x2d024865…bdc8e0` | `0x6fdb03ec52932c0bbb48f1367c7739480e78b785` |
| W1 60,699 (2026-04-11) | `0x63448db2…879abc` | `0xeec6547e1fd30b1b995c63c4937c58c73603c47c` |

## 8. EVM (Sonic) side — where the bridged ANON came from

Tracing the three Sonic senders' incoming ANON ERC-20 transfers (chunked `eth_getLogs` on Sonic, chainId 146):

- **`0xd3f62c…`** (→ 7Mad6X): received **5.46M ANON** total, dominated by **`0xe453c128f9fa860960913f40ef975b1fe5621e9e` = Silo Finance** ("Borrowable Anon Deposit, SiloId 27" / `bAnon-27`) — i.e. an ANON **lending market**.
- **`0x6fdb03…`** (→ 3Ea1u3vw): received **~3.6M ANON**, again #1 from **Silo Finance** (1.30M), plus large amounts from Sonic **AMM pool/router contracts** (`0x34fee989…`, `0xb0d458bf…`, `0x4c73dcbc…`, `0x297000941…` — all the same 44,224-byte AMM bytecode).
- **`0xeec654…`** (→ W1): received ANON again #1 from **Silo Finance** (100k) + a DEX pool.

All three Sonic senders also show some **OFT mints from `0x0`** (ANON bridged *into* Sonic from another chain by the same operators), but the **dominant, recurring source is the native HeyAnon DeFi stack on Sonic — Silo Finance lending markets and Sonic AMM pools/routers**.

**Full origin chain (both sides):**

```
SONIC (EVM, chainId 146)
  Silo Finance ANON market 0xe453c128…  +  Sonic AMM pools/routers (0x2970…, 0x34fee9…, 0xb0d458…)
        │  (borrow / swap ANON)
        ▼
  bridge-operator EOAs  0xd3f62c… , 0x6fdb03… , 0xeec654…
        │  LayerZero OFT send  (OFT 0x79bbf4…, srcEID 30332 → dstEID 30168)
        ▼
SOLANA  — OFT mint (program A1oayh35…, mint-auth multisig 5AAcqak…)
  bridge-receivers  7Mad6X… , 3Ea1u3vw… , (W1 directly)
        │  SPL transfer
        ▼
  MM network  FWznb… / EFE3j1… / 26hBWMo…
        │
        ▼
  HUB  6LY1Jz…  ──(50k seed each, 2026-03-23)──►  W1…W9
```

**So the user's premise is confirmed:** the cluster's ANON **originates on Sonic**, where it was sourced through HeyAnon's own DeFi (Silo lending + Sonic DEXes), then **bridged to Solana over LayerZero** (Sonic→Solana OFT), minted to a handful of bridge-receiver wallets, consolidated at the `6LY1Jz` hub, and seeded out to the 9 wallets.

## 10. Definitive per-wallet acquisition: MINTED vs BOUGHT vs TRANSFERRED — and buy PnL

For every wallet, each ANON **inflow** was classified at the instruction level into one of four buckets. Crucially, two "sources" turned out to be **not genuine inflows**: (a) the **governance escrow nets to 0** (same-day stake→unstake round-trip on 2026-04-19), and (b) the **Raydium CLMM pool nets negative for every wallet** (each wallet is a *net LP provider* — the pool is a sink, so "received from pool" is just the wallet withdrawing its own ANON / collecting fees). Also, ~1,000 of the "swaps" were actually **zero-cost LP-fee/reward claims** (Helius labels them `SWAP`); only swaps where the wallet *paid* SOL/USDC are counted as **BOUGHT**.

So the only **genuine origins** of each wallet's ANON are: **(1) hub seed** (a transfer, but the ANON itself was bridged from Sonic), **(2) direct bridge-mint** from Sonic, **(3) genuine DEX buys**, and **(4) LP-fee/reward claims**.

| W | Seed from hub `6LY1Jz` (transfer; bridged-origin) | Direct bridge-MINT (Sonic→Solana) | BOUGHT on DEX | Buy cost | LP-fee CLAIMS (free) | Sold on DEX → proceeds | **Net DEX cash (PnL)** | Holds now | Holds $ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **W1** | 49,000 | **60,699** | 7,462 | **$4,161** | 18,221 | 102 → $110 | **−$4,051** | 28,413 | $13,158 |
| **W2** | 50,000 | 0 | 598 | $315 | 9,637 | 229 → $202 | −$113 | 598 | $277 |
| **W3** | 50,000 | **50,000** | 6,594 | **$4,864** | 7,972 | 128 → $114 | **−$4,750** | 213 | $99 |
| **W4** | 50,000 | 0 | 1,055 | $563 | 9,869 | 151 → $131 | −$432 | 1,056 | $489 |
| **W5** | 50,000 | 0 | 0 | $0 | 15,218 | 550 → $465 | +$465 | 0 | $0 |
| **W6** | 50,000 | 0 | 211 | $113 | 14,234 | 675 → $588 | +$475 | 212 | $98 |
| **W7** | 317,210 | 0 | 7,812 | $3,755 | 0 | 317,469 → $32,286 | **+$28,530** | 0 | $0 |
| **W8** | 50,000 | 0 | 631 | $338 | 14,114 | 675 → $588 | +$250 | 631 | $292 |
| **W9** | 50,000 | 0 | 908 | $488 | 0 | 675 → $589 | +$101 | 908 | $421 |
| **SUM** | ~716,210 | **110,699** | 25,270 | **$14,598** | 89,265 | → $35,073 | **+$20,475** | — | $14,834 |

**Answers to "bought or minted or transferred?":**
- **Transferred (then bridged-origin):** the dominant route. ~716k ANON arrived as the hub seed; that ANON was itself **bridge-minted from Sonic** (hub fed by bridge-receivers 7Mad6X / 3Ea1u3vw). So it is *transferred to the wallet, minted at origin.*
- **Minted directly to the wallet (bridge from Sonic):** only **W1 (60,699 on 2026-04-11)** and **W3 (50,000 on 2026-04-11)**. No other wallet received a direct bridge-mint.
- **Bought (genuine DEX purchase):** small for everyone — cluster total **25,270 ANON for $14,598**. Biggest single buyer is **W7 (7,812 ANON for 50 SOL / $3,755)**; W1 and W3 also spent ~$4–5k (largely in USDC).
- **LP-fee/reward claims (free):** ~89k ANON across the wallets — this is what the "100–150 tiny swaps" actually were.

**Buy PnL (DEX cash flow = sell proceeds − buy cost):**
- **W7: +$28,530** — the cluster's sell leg. Bought 7,812 for $3,755, sold 317k (its seed) for $32,286.
- **W5/W6/W8/W9: small positive** (+$101 to +$475) — sold a bit more than they bought.
- **W1: −$4,051 and W3: −$4,750** — net *accumulators*; they spent cash buying and barely sold. W1 still holds 28,413 ANON ($13.2k) so it is up on an unrealized basis; W3 sold/sent most of its inventory so its cash position is a genuine drawdown.
- **W2/W4: small negative** (−$113 / −$432) — minor net buyers.
- **Cluster net realized DEX cash: +$20,475**, almost entirely W7. Including the $14,834 of ANON still held, mark-to-market net is ~+$35.3k — but remember the bulk of inventory was **free** (bridged seed + mints + LP fees), not purchased.

## 9. Methodology & caveats

- Pulled full Enhanced (parsed) transaction history for all 9 wallets and for the key upstream ANON token accounts via Helius. Net ANON/SOL/USDC per transaction computed from `accountData.nativeBalanceChange` + `tokenBalanceChanges` (owner-resolved), which correctly nets multi-hop Jupiter routes.
- "Transfer" counterparties are resolved to the **owner** account; flows to/from `EYy5` (Raydium CLMM) and `Dab466` (governance) are protocol interactions, not peer wallets.
- A few transfers showed an unresolved counterparty (token-account-level, no owner in the parsed payload) — these are pool/program internal legs and don't change the conclusions.
- Prices are spot marks at analysis time; realized swap PnL is computed at the actual SOL/USDC amounts exchanged, so it is not sensitive to the current SOL mark.
- The upstream MM network is densely interconnected and could be traced further, but it converges on ANON's launch-era distribution rather than a distinct external origin.
