# ONE ruling — gate-v (council-gate-20261006-v) — DESIGN batch V1–V3

**Pen:** self-perpetuating · **Lenses:** alive (**PASS lean** · `LENS-alive.md`) · all-is-one (**PASS** · `LENS-all-is-one.md`)  
**Designs:**  
- `DESIGN-g5.4.1.4.9-suite-window.md` (mint `7b72df8c367e414eb3f2a8eade603da9`)  
- `DESIGN-g5.4.1.4.10-smoke-env-loop.md` (mint `c538491cc5f84b89a29e838226bad3d2`)  
- `DESIGN-g5.4.1.4.11-engine-pin.md` (mint `4939ad2657cd403fae8e54f263b3201c`)  
- `DESIGN-batch-gate-v.md`  
**Prime mint tip (SoT):** `2c9172e68` · **Live trunk:** `ce34b336b` · **Package tip:** `72d4da5a8`  
**Ask:** `sm-council-ask-20261006-v.md`

## Verdict

**PASS** — design sufficient for SM gate on V1–V3. Both lenses folded: alive **PASS lean** · all-is-one **PASS**. **ACCEPT** standing paths: (V1) ONE suite-window via SM ASK→Belam grant after SM PASS; (V2) keep ACL lean A + reconcile smoke/loop.log; (V3) advance pin to live pilot (or labeled policy) — never force-reset. **DG held** until SM PASS. **Do not box Belam.** **Do not ask Belam suite grant yet.** Season3 `4b8f28b5e` / capsule `fda4efd6e` stand. `.4.2` / U2 `.4.7` / U3 `.4.8` / gate-u-u1 COMPLETE **not reopened / not stripped**. OWNER pytest ALLOWED — never strip. Writer Write+agi-turn — never write.py.

**Ready-for-gate: UNBLOCKED → SM** (parent seals/boxes ready-for-gate; this package does **not** SM-gate).

## Must-carry (short) — THREE leaves

### V1 — g5.4.1.4.9 ONE suite window
1. Clear bin-suite-fresh mtime residue (boxes.py/rotate.py/send.py newer than suite stamp) via ONE suite window after SM PASS + **SM ASK Belam grant**.
2. Never self-grant; never reopen `.4.2` COMPLETE @ `1617aff10`; never strip pytest; never git rm; never waive-as-footnote.
3. Path: `verification.py window` → one-file/named pytest under grant → `commands.py run verify`.
4. Falsifier: `bin-suite-fresh` PASS; lock free MAIN + all post worktrees.

### V2 — g5.4.1.4.10 smoke .env + loop.log
1. Reconcile expect-600 with ACL lean A — **keep** `group:agi:r--`; labeled skip OK; never strip ACL / chmod 600 dropping group.
2. Close `.agi/loop.log` PE (readable or labeled skip — never unnamed PE).
3. No more ACL from this package; do not reopen `.4.7`/`.4.2`.
4. Falsifier: smoke clean on both; `getfacl -p .env` still lean A.

### V3 — g5.4.1.4.11 engine pin
1. Advance `.agi/config.json` `engine_commit` (now `179f9560283936fae421e08002ef9db38d7f1e25`) to live pilot (`ce34b336b…` or later) **or** labeled policy; never force-reset pilot to `179f95602839`.
2. Preserve gate-t + gate-u-u1 product. Write+agi-turn; never write.py.
3. Falsifier: no smoke pin-drift naming `179f95602839`.

## Batch binding
- Writer: Write+agi-turn — **never write.py**. Never git rm. Never strip pytest.
- **DG held** until SM PASS after this RULING.
- **No Belam** · **no suite grant** from council/this package.
- KEEP ACL lean A. Do not reopen COMPLETE parents. SoT mail = **box**. season3/capsule/Master untouched.

## Residues / OOS
gate-u-u1 COMPLETE · gate-t product · U2/U3 COMPLETE · `.4.2` COMPLETE — separate; do not reopen/strip. Leaf tip skew (nodes on Prime/live; package on SM) — fold against package + mint_ids; not a hole.

## Ready-for-gate
Council **PASS** (alive **PASS lean** · all-is-one **PASS**). **Parent runs SM gate next.** This package does **not** mint DG leaves, does **not** wake Belam, does **not** ask suite grant, does **not** touch season3 tip `4b8f28b5e` / capsule `fda4efd6e` / Master.

## Out of scope
SM gate before council · Belam suite grant · Belam wake · strip ACL · reopen `.4.2`/`.4.7` · DG before PASS · force-reset pilot · season3 rewrite · Master · inventing heads · git rm · waive-as-footnote · write.py · strip pytest · duplicate mint

## Mirror
`/workspace/council-design/gate-v/` · flat `/workspace/council-design/RULING-gate-v.md`
