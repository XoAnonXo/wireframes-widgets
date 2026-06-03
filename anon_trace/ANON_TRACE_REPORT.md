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

## 7. Methodology & caveats

- Pulled full Enhanced (parsed) transaction history for all 9 wallets and for the key upstream ANON token accounts via Helius. Net ANON/SOL/USDC per transaction computed from `accountData.nativeBalanceChange` + `tokenBalanceChanges` (owner-resolved), which correctly nets multi-hop Jupiter routes.
- "Transfer" counterparties are resolved to the **owner** account; flows to/from `EYy5` (Raydium CLMM) and `Dab466` (governance) are protocol interactions, not peer wallets.
- A few transfers showed an unresolved counterparty (token-account-level, no owner in the parsed payload) — these are pool/program internal legs and don't change the conclusions.
- Prices are spot marks at analysis time; realized swap PnL is computed at the actual SOL/USDC amounts exchanged, so it is not sensitive to the current SOL mark.
- The upstream MM network is densely interconnected and could be traced further, but it converges on ANON's launch-era distribution rather than a distinct external origin.
