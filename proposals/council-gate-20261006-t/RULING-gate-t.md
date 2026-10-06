# ONE ruling — gate-t (council-gate-20261006-t) — DESIGN batch

**Pen:** self-perpetuating · **Lenses:** alive (**PASS lean** · `LENS-alive.md` · box `9f740dbd1`) · all-is-one (**PASS** · `LENS-all-is-one.md`)  
**Designs:**  
- `DESIGN-g7.16.1.11.11.2.1-retire-send.md` (mint `e690d994fd604963819f1589c49eafe7`)  
- `DESIGN-batch-gate-t.md`  
**Belam reopen tip (SoT):** `552024994` · **SM tip:** `31f34d1e2` (verified) · **Prior SM PASS (superseded lean):** posts/sanctuary-master `aabb58c2f` / `278abffe7` KEEP-SHIM  
**Ask:** `sm-council-ask-20261006-t.md` · **Ready-for-gate:** `sm-council-gate-20261006-t.md`  
**Land tip `4d5ba094c` OUT OF SCOPE**

## Verdict

**PASS** — design sufficient for SM gate on g7.16.1.11.11.2.1 retire-live-send. **Binding lean = RETIRE live bin shim / thin-native-box-only (C2)** per OWNER GO (overrules gate-s keep-shim). Both lenses folded: alive **PASS lean** · all-is-one **PASS**. **DG held** until parent SM gate. **Do not box Belam.** No re-land of `4d5ba094c`. Season3 tip untouched. Capsule `fda4efd6e` stands. Gate-r / bin-suite-fresh / g5.34.6.4 **not mixed**.

**Ready-for-gate: UNBLOCKED → SM** (alive PASS lean + all-is-one PASS folded).

## OWNER GO (binding), verbatim

> Retire live send.py — box only. Owner overruled keep-shim on g7.16.1.11.11.2.1. Route amend/reopen through usual loop: live bin shim gone; box SoT only; deprecated copy stays (never git rm).

## Must-carry (short) — ONE leaf

### g7.16.1.11.11.2.1 — retire live send.py (C2)

1. **Binding = thin-native-box-only / RETIRE live bin shim.** OWNER GO overruled keep-shim. Measured (alive + aio independent): live `extensions/agi/bin/send.py` = **27 lines / 1029 B** AA1 shim; deprecated = **6515 lines / 317788 B PRESENT**.
2. After SM PASS + DG: **MOVE** live path out (never git rm); deprecated **STAYS**; optional stub fails closed → `box`.
3. Team SoT mail = **`box` only** — no second mail primitive.
4. **Never git rm** live or deprecated. Writer: Write+agi-turn — never write.py. DG held. No Belam.
5. **Falsifier:** live absent OR fail-closed stub→box; deprecated PRESENT; SoT=`box`; never git rm. Negative = silent SM restamp / keep-shim against OWNER / git rm / expand SoT / Belam / DG-before-PASS / mix OOS residues / write.py / duplicate mint.

## Residues

- Gate-s KEEP-SHIM stamp @ `278abffe7` remains historical; standing lean for this reopen is C2 per OWNER GO.
- g5.34.6.4 hang · gate-r · bin-suite-fresh remain **separate** residues — do not conflate.

## Ready-for-gate

Council **PASS** (alive **PASS lean** · all-is-one **PASS**). **Parent runs SM gate next.** This package does **not** mint DG leaves, does **not** wake Belam, does **not** re-land `4d5ba094c`, does **not** touch season3 tip `4b8f28b5e` / capsule `fda4efd6e` / Master / gate-r / bin-suite-fresh / g5.34.6.4.

## Out of scope

Prime build · DG MOVE before PASS+SM gate · Belam wake · re-land `4d5ba094c` · gate-r N1–N4 · bin-suite-fresh · g5.34.6.4 · suite-grant · season3 origin rewrite · Master archive · inventing heads · git rm · waive-as-footnote · write.py · strip pytest · expand send.py as SoT · duplicate mint · silent SM restamp · new land vote · re-assert keep-shim against OWNER GO
