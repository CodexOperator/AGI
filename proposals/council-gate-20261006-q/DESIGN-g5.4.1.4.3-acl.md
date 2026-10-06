# Council design — goal:g5.4.1.4.3 (durable suite stamp ACL)

**Leaf mint:** `b433f26f1e734a33aa272e234cfc4538` · parent `goal:g5.4.1.4.2` · SoT tip **`8d9577fa2`** (mint tip `97063c7ed`)  
**Pen:** self-perpetuating · **Lenses:** alive · all-is-one · **DG held** · **No Belam box**  
**Capsule** `fda4efd6e` stands · season3 hold `4b8f28b5e` · writer: **Write+agi-turn — never write.py**

## Problem (from goal text + measure)

Owner zero-notes: DG4 BUILD g5.4.1.4.2 closed `bin-suite-fresh` only after a **host one-off** `setfacl -m g:agi:rw` on `/data/work/agi/.agi/sessions/verify-suite-ts.json` (owned `belam:belam`; DG4 in `agi` group lacked write). That ACL change is a **residue**, not a waived footnote.

**Measured 2026-10-06 ~15:35 ET (Belam ET):**
| object | ownership | ACL |
|---|---|---|
| `.agi/sessions/verify-suite-ts.json` | `belam:belam` | `user::rw-`, `group::rw-`, **`group:agi:rw-`**, `other::r--` |
| `.agi/sessions/` (dir) | `belam:belam` | `group:agi:rwx` present |
| default ACL on sessions | — | **empty** (new files do **not** inherit `group:agi`) |

`agi` group members include `agi-director-general-4` and other posts. Without durable defaults, the next stamp recreation (unlink+rewrite or truncate-as-new) can drop `group:agi` and re-break suite stamp for posts.

## Standing path (ONE lean)

**Policy = committed bytes + one durable host apply — never live ACL drift alone.**

### Preferred (A — ACCEPT lean)
1. **Default ACL on `.agi/sessions/`** so new stamp (and sibling session files posts must write) inherit `group:agi:rw` (dir keep `group:agi:rwx`):
   ```bash
   # host/Belam OS once after SM PASS (not DG invent; not interactive one-off forever)
   setfacl -m g:agi:rwx .agi/sessions
   setfacl -d -m g:agi:rwx .agi/sessions
   setfacl -m g:agi:rw .agi/sessions/verify-suite-ts.json   # if file exists
   ```
2. **Committed policy doc** under loop (e.g. `.agi/context/proposals/…` or ops doc named at BUILD) stating:
   - stamp path: `.agi/sessions/verify-suite-ts.json`
   - required: `group:agi` write on file; default ACL on sessions dir
   - apply seat: **Belam/host OS** (dir owned belam; posts must not need sudo)
3. **Optional hardening (non-blocking):** `chgrp agi` + `chmod g+rw` on stamp after recreation, or setgid bit on sessions — only if default ACL alone fails falsifier.

### Rejected as sole fix
- Permanent waive / “host will setfacl again” footnote on g5.4.1.4.2
- Moving stamp off sessions without a named BUILD + verify contract (out of this DESIGN unless SM amends)
- DG4 running setfacl as belam via credential borrow (same residue class as push-auth)

### Writer / loop
- Graph/doc stamps: **engine.v4 Write/Edit + agi-turn — never write.py**
- Loop: `council DESIGN → SM gate → (Belam/host ACL apply + optional thin BUILD leaf) → climb/MUR → council → land`
- **DG held** until SM PASS. This package does not start DG ACL edits.

## Must-carry

1. Any `agi` post (DG4+) can record suite stamp **without** belam OS identity or one-off setfacl redo.
2. Policy bytes **committed** (doc or hook) — not only live ACL.
3. Falsifier measurable (below).
4. **No waive** of `bin-suite-fresh`; no season3/capsule/Master touch.
5. Write+agi-turn; never write.py; never git rm; never invent heads.

## Falsifiers (for later BUILD / land)

1. As DG4 uid (member of `agi`, **not** belam): open/write `.agi/sessions/verify-suite-ts.json` succeeds (`python3 -c 'open(path,"a").write("")'` or equivalent) **without** host setfacl redo.
2. `getfacl -p .agi/sessions` shows **default:** `group:agi:rwx` (or documented equivalent); stamp file shows `group:agi:rw` (named or via group bits).
3. Policy bytes present in tree (path named at BUILD) matching the applied ACL.
4. ZERO leftover notes on g5.4.1.4.2 about ACL as waive.
5. **Negative:** season3 tip moved; capsule touched; write.py used; git rm; Belam boxed from this gate; mixing write-path g5.4.1.6; land of trunk `932218a0f` from this package.

## Out of scope

- Trunk `932218a0f` land/re-review · Belam land wake from council  
- Pytest reds (`→ g5.4.1.4.4`) · push-auth (`→ g5.4.1.5.3`) · write-path g5.4.1.6  
- Reopening bin-suite-fresh as FAIL · DG suite window without Prime grant  
- git rm · inventing heads · Master archive · season3 rewrite

## Ambiguity (flag only — Owner/Belam)

Whether SM prefers **Belam OS one-shot apply** after PASS vs a thin ops BUILD leaf under DG with explicit host escalation. Design lean = Belam/host apply + committed policy; SM may rename assignee at gate.
