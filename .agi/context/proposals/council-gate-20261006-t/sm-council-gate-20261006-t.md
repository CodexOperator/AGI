# SM council gate — gate-t (council-gate-20261006-t) — SM PASS

**Verdict:** SM **PASS** · binding lean **RETIRE / C2 thin-native-box-only** · 2026-10-06-t  
**Pen:** self-perpetuating · **Lenses:** alive **PASS lean** (`LENS-alive.md` · box `9f740dbd1`) · all-is-one **PASS** (`LENS-all-is-one.md`)  
**Belam reopen tip (SoT):** `552024994` (`5520249948dd12d334f11efa5178895b0c40d9aa`)  
**SM ASK tip:** `31f34d1e2` (`31f34d1e2ce8f2c2c6fb2e89bf01e6a4123a2f79`)  
**SM PASS tip:** `27ee6bac8` (posts/sanctuary-master) · content tip cited in Agent Notes  
**Prior KEEP-SHIM (superseded):** posts/sanctuary-master `aabb58c2f` / content `278abffe7` — **overruled by OWNER GO** (historical only)  
**Leaf:** `goal:g7.16.1.11.11.2.1` · mint_id `e690d994fd604963819f1589c49eafe7` · parent `goal:g7.16.1.11.11.2` · **active** (stays active until DG MOVE falsifier MET; do **not** stamp complete yet)  
**Land tip `4d5ba094c` OUT OF SCOPE** · season3 `4b8f28b5e` · capsule `fda4efd6e` · gate-r / bin-suite-fresh / g5.34.6.4 **OOS**  
**Package:** `.agi/context/proposals/council-gate-20261006-t/` (+ mirror `proposals/…` · `council-design/gate-t/`)  
**RULING:** `RULING-gate-t.md` · **Batch:** `DESIGN-batch-gate-t.md` · **ASK:** `sm-council-ask-20261006-t.md`

## Binding lean (ONE leaf) + DG BUILD child

| leaf | lean (binding) | mint | status after SM PASS | assignee |
|---|---|---|---|---|
| g7.16.1.11.11.2.1 retire live send.py | **C2 RETIRE / thin-native-box-only** — OWNER GO overruled keep-shim; MOVE live `extensions/agi/bin/send.py` (never git rm); deprecated STAYS; SoT mail=`box` only | `e690d994fd604963819f1589c49eafe7` | `active` (await DG MOVE) | sanctuary-master (DESIGN closed) |
| g7.16.1.11.11.2.1.1 BUILD MOVE live shim | MOVE live bin shim out; deprecated PRESENT; optional fail-closed stub→box; SoT=`box`; never git rm | `f5b44185d7014344ad0d84b5f55e0454` | `active` **RELEASED** | **director-general-4** |

## OWNER GO (binding), verbatim

> Retire live send.py — box only. Owner overruled keep-shim on g7.16.1.11.11.2.1. Route amend/reopen through usual loop: live bin shim gone; box SoT only; deprecated copy stays (never git rm).

## Measured (alive + aio independent, pre-MOVE)

- live `extensions/agi/bin/send.py` = **27 lines / 1029 B** AA1 shim (still present; expected until DG MOVE)
- deprecated `extensions/agi/deprecated/bin/send.py` = **6515 lines / 317788 B PRESENT** (never git rm; STAYS)
- Team SoT mail = **`box` only**

## DG RELEASE

- **goal:g7.16.1.11.11.2.1.1** → **director-general-4** (TM→DG4 bin lineage; match prior bin-suite leaves)
- Falsifier for child COMPLETE: live absent OR fail-closed stub→box; deprecated PRESENT; SoT=`box`; never git rm
- Parent COMPLETE waits for BUILD PASS + falsifier MET
- Wake: box thought-master + director-general-4 · TM agent `14d7a396-4744-48f9-ab8a-2a51044a41af` · **Do NOT wake Belam**

## Holds (hard)

- **NO Belam box/wake**
- **NO land** · **NO suite grant ask** · **NO re-land** of `4d5ba094c`
- season3 `4b8f28b5e` · capsule `fda4efd6e` untouched
- gate-r / bin-suite-fresh (todo 130) / g5.34.6.4 **OOS** (do not conflate)
- Writer: Write+agi-turn — never write.py · **never git rm** · never strip pytest
- Never re-assert keep-shim against OWNER GO · never silent SM-only restamp without council
- Parent leaf stays **active** until DG MOVE falsifier MET (do not stamp complete at this gate)

## Docs in package

`RULING-gate-t.md` · `LENS-alive.md` · `LENS-all-is-one.md` · `DESIGN-batch-gate-t.md` · `DESIGN-g7.16.1.11.11.2.1-retire-send.md` · `DRAFT-RULING-gate-t.md` · `sm-council-ask-20261006-t.md` · this PASS stamp
