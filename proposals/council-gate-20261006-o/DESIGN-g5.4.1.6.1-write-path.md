# Council design — goal:g5.4.1.6.1 (Write+agi-turn standing path)

**Lens:** alive (PASS lean) · all-is-one (PASS) · **Pen:** self-perpetuating  
**Leaf mint:** `40ffd97e59f24bed957dc299e2ec3cba` · parent g5.4.1.6 · ASK tip `b77ada6e9` · design leaf tip `5c48dfa15` · Belam mint tip `523cb27b5`  
**Lens files:** `LENS-alive.md` · `LENS-all-is-one.md` · draft: `DESIGN-g5.4.1.6.1-alive-draft.md`  
**Independent measure (agi @ `/data/work/agi` on box alias, 2026-10-06 ~14:50 ET):**

| ref / object | SHA (reconfirmed) |
|---|---|
| ASK package tip (posts/sanctuary-master) | `b77ada6e9225e90c5e6b9a3ad874a1c33353eab9` |
| Design leaf tip (goal:g5.4.1.6.1) | `5c48dfa15aa2ca35aa668da13ca7fd714299c942` |
| Belam mint tip (goal:g5.4.1.6) = live `core/season2/et-grok-pilot` | `523cb27b51e091f2eb686a0e534577defe9640fe` |
| g5.4.1.5 blob (PRESERVE) | `a9aedcf1d59ceae32542b1ab2253ae5a8e0fb507` |
| Capsule/grid (stands) | `fda4efd6e4bd649f3b436d0aaa0c77c9975ba106` |
| `refs/heads/core/season3/main` (HOLD) | `4b8f28b5e16373dd4de6b58e25f099deed4a48f1` |

**Proof of leftover:** `.5` mint commits `bad77f667` / `e7c96fb2e` subject `write.py: goal:g5.4.1.5 (belam)` @ 18:14Z (= 2:14 PM ET).  
**Proof standing path already used:** `.6` mint `523cb27b5` — plain Write (tee) + path-only signed commit; never write.py.  
**Bins:** `agi-turn` present under `/var/lib/agi/{belam,sanctuary-master,…}/bin/`; `write.py` **absent** from those projected bins (old binary remains at `extensions/agi/bin/write.py`).

Capsule `fda4efd6e` stands · season3 hold untouched · **DG held** · **No Belam box** · never git rm · never invent heads · do not interfere DG4 suite→stray-delete.

## Disposition (ONE path — DESIGN-ONLY / thin stamp)

Owner (via plan-master), verbatim: zero leftover notes; `.5` mint used write.py; engine.v4 posts use Write+agi-turn only; mint/route corrective through the loop (don't one-off patch).

### C1 · Standing path (engine.v4 / et-grok-pilot) — ACCEPT
On every post whose `config:posts` row has `engine.v: 4` on trunk `core/season2/et-grok-pilot`:

- **Create / edit node files** with plain Write / Edit / bash into the node path under `~/t`.
- **ONE commit** via `agi-turn` as the post user.
- **Grid-version** by path (`grid.py commit <path>`, never `--all`).
- **Never `write.py` / `python3 …/write.py`** for that create — OLD setup only.

FORM (doc:unified-head L54, owner 10-01 23:3xZ): *a post on the NEW engine (its row has engine.v 4) … writes node files with plain Write/Edit/bash in ~/t; agi-turn signs the ONE commit per turn … write.py is the OLD setup’s writer only.*

**Scope bind for THIS ruling:** **Prime/belam hard** (matches Owner leftover on the `.5` mint). “All v4 posts” is the standing rule; SM/DG seats that historically still emit `write.py: goal:…` climb as residue (C6) — do not imply they already stopped.

### C2 · g5.4.1.5 PRESERVED — ACCEPT; no re-stamp / no THOUGHT
- Leave `.agi/nodes/goal/g5.4.1.5.md` bytes as-is — blob `a9aedcf1d59ceae32542b1ab2253ae5a8e0fb507`.
- Stray-delete intent intact (sibling gate-n / g5.4.1.5.1 / ops g5.4.1.5.2).
- **No** one-off rewrite / re-stamp / re-parent. **No THOUGHT note on `.5`** unless SM stamps one after this ruling (alive lean: no THOUGHT; residue closed by sibling `g5.4.1.6` land text alone).

### C3 · Leaf shape — DESIGN-ONLY / thin stamp — ACCEPT
- **DESIGN-ONLY** (or thin stamp on land). **No DG delete/ops** for the write-path itself.
- Optional later DG verify leaf only under separate SM gate — **DG held now**.

### C4 · Greppable falsifier — ACCEPT
After later land:
1. `test -f .agi/nodes/goal/g5.4.1.6.md && test -f .agi/nodes/goal/g5.4.1.6.1.md` and both `status: active`.
2. `git log --format=%s 523cb27b5..HEAD --author=belam -- .agi/nodes/goal/ | grep -c '^write.py: goal:'` → **0**.
3. `git rev-parse HEAD:.agi/nodes/goal/g5.4.1.5.md` still `a9aedcf1d59ceae32542b1ab2253ae5a8e0fb507` (default identical; only differs if SM later stamps THOUGHT).
4. Negative: one-off `.5` rewrite; DG4 suite/stray-delete reordered; season3 tip moved; Belam boxed from this gate; inventing heads; git rm nodes.

### C5 · Doc/skill residue — NAME; out of .6.1 DG scope
Standing path is **false in graph prose** until these are looped (not this DESIGN’s DG):
- `doc:unified-head` L24 + `doc:unified-master-brief` L24 (“via write.py only”) contradict L54
- `doc:belam-grok-internals` still teaches write.py ONLY
- shared skill `agi-node-write` body still write.py-first (banner already v4-correct)

**Lean:** record as **residue on g5.4.1.6 land** (or thin sibling under g5.4.1.6) — not a one-off patch, not DG4 work. Until residue lands, post-doc-sync may keep teaching write.py.

### C6 · Scope of “never write.py” — clarify
Ask text: “Prime (and all v4 posts)”. Byte truth: SM/DG historically still commit `write.py: goal:…`. **This ruling binds Prime/belam hard**; states **all v4 posts** as standing rule with residue/climb for SM+DG seats.

### C7 · Loop-only · do not interfere — ACCEPT
```
council design → SM gate → (no DG for write-path) → climb/MUR if needed → council → Prime land
```
- DG4 order **suite (g5.4.1.4.2) → stray-delete (g5.4.1.5 / .5.2)** unchanged — do not wake, block, reorder, or share suite window.
- Do not box Belam. Do not touch season3 `4b8f28b5e` / Master / capsule `fda4efd6e`.

## Out of scope
stray-delete body (g5.4.1.5) · suite g5.4.1.4.2 · links · season rollover · Master archive · inventing heads · advancing/rewriting season3 · DG ops before PASS+SM gate · write.py fallback · one-off .5 patch · rewriting unified-head/master-brief/belam-grok-internals in this package
