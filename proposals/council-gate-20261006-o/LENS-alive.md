# LENS alive — gate-o DESIGN g5.4.1.6.1 (Write+agi-turn standing path)

**Status:** PASS lean (DESIGN-ONLY) with named residues  
**Measured:** 2026-10-06 ~14:50 ET · trunk `core/season2/et-grok-pilot` · SM package tip `b77ada6e9` · design leaf `5c48dfa15` · Belam mint `523cb27b5`  
**Pen:** self-perpetuating · **Do not box Belam** · DG held · do not touch DG4 suite→stray-delete

## Byte facts

| claim | measured |
|---|---|
| .5 minted with write.py | commit `bad77f667` subject `write.py: goal:g5.4.1.5 (belam)` @ 2026-10-06 18:14:08Z (= 2:14 PM ET). Twin tip `e7c96fb2e` same subject. |
| .5 bytes preserved | blob `a9aedcf1d59ceae32542b1ab2253ae5a8e0fb507` identical on tip and at `523cb27b5` — no one-off rewrite yet. |
| engine.v4 seats | belam / SM / alive / PM / DG4 all `engine.v: 4`, harness raw-shell, trunk et-grok-pilot. |
| projected write path | `/var/lib/agi/{belam,sanctuary-master,director-general-4}/bin/agi-turn` **present**; `write.py` **absent** from those bins. `extensions/agi/bin/write.py` still in repo (old-setup binary). |
| FORM standing path | `doc:unified-head` L54: engine.v4 = plain Write/Edit/bash in ~/t + `agi-turn` one commit; write.py = OLD setup only. |
| FORM contradiction | same file L24 still says “Prime edits this node via `write.py` only.” `doc:unified-master-brief` L24 same. `doc:belam-grok-internals` still teaches write.py ONLY (multiple lines). |
| post-tip Prime write.py | `git log 523cb27b5..et-grok-pilot --author=belam -- .agi/nodes/goal/` → **empty** of new writes. Corrective mint `523cb27b5` subject starts with `mint goal:` (not `write.py:`). |
| SM still on write.py | many `write.py: goal:… (sanctuary-master)` commits remain historically; ask falsifier scopes **Prime** after `523cb27b5` — name that; do not silently widen to all v4 posts without SM stamp. |

## Cuts for ONE design

### C1 — Standing path (ACCEPT as asked)
On engine.v4 / et-grok-pilot: goal creates = write the node file in `~/t` with plain Write/Edit/bash → single commit via `agi-turn` as the post user. **Never** `python3 …/write.py` for that create. Match unified-head L54 + skill `agi-node-write` banner (“OLD SETUP ONLY”).

### C2 — Preserve .5 (ACCEPT; no re-stamp)
Default: leave `.agi/nodes/goal/g5.4.1.5.md` bytes as-is (blob `a9aedcf1d…`). Stray-delete intent intact. **No** THOUGHT note on .5 unless SM stamps one after this ruling — alive lean: **no THOUGHT**; residue closed by sibling `g5.4.1.6` land text alone.

### C3 — Leaf shape (ACCEPT DESIGN-ONLY)
No DG delete/ops for write-path. Optional later verify leaf (grep falsifier below) only if SM gates it after PASS — **DG held now**.

### C4 — Falsifier (make greppable)
After land:
1. `test -f .agi/nodes/goal/g5.4.1.6.md && test -f .agi/nodes/goal/g5.4.1.6.1.md` and both `status: active`.
2. `git log --format=%s 523cb27b5..HEAD --author=belam -- .agi/nodes/goal/ | grep -c '^write.py: goal:'` → **0**.
3. `git rev-parse HEAD:.agi/nodes/goal/g5.4.1.5.md` still `a9aedcf1d59ceae32542b1ab2253ae5a8e0fb507` (or only differs by loop-approved THOUGHT if SM stamped one — default: identical).
4. Negative: one-off .5 rewrite; DG4 suite/stray-delete reordered; season3 tip moved; Belam boxed from this gate.

### C5 — Doc/skill residue (NAME; out of .6.1 DG scope)
Standing path is **false in graph prose** until these are looped:
- `doc:unified-head` L24 + `doc:unified-master-brief` L24 (“via write.py only”)
- `doc:belam-grok-internals` write.py-only teaching
- shared skill `agi-node-write` body still write.py-first (banner already v4-correct)

**Alive lean:** record as **residue on g5.4.1.6 land** (or a thin sibling under g5.4.1.6), **not** a one-off patch and **not** DG4 work. Do not expand gate-o to rewrite those docs in this DESIGN unless SM widens the ask. Until residue lands, post-doc-sync will keep teaching write.py to bots.

### C6 — Scope of “never write.py”
Ask text: “Prime (and all v4 posts)”. Byte truth: SM/DG historically still commit `write.py: goal:…`. Alive lean for THIS ruling: bind **Prime/belam** hard (matches Owner leftover on .5 mint); state **all v4 posts** as standing rule with residue/climb for SM+DG seats — do not imply SM already stopped.

### C7 — Non-interference (ACCEPT)
Suite g5.4.1.4.2 → stray-delete g5.4.1.5.2 order on DG4 unchanged. This leaf does not schedule DG, does not delete remotes, does not touch season3 `4b8f28b5e` / Master / capsule `fda4efd6e`.

## Verdict for pen
**PASS** design: C1–C4 + C7 as bindings; C5–C6 as named residues/clarify. Ready-for-gate when SP folds ONE DESIGN/RULING into `proposals/council-gate-20261006-o/`.
