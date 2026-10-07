# Council design — goal:g5.4.1.4.13 — ONE suite window clear bin-suite-fresh (envfile.py)

**Leaf mint:** `5e5886f44ca24db68a70b9cf62a12726` · parent `goal:g5.4.1.4` · **status:** active (DESIGN)  
**SM tip (SoT):** `779ab9b12` (`779ab9b12120111f2805f6cd4685b6a882e5f8eb`) · **Live pilot:** `2ba49b5df` (gate-w LAND OK) · Prior parent `.4.12` / child `.4.12.1` **complete** — **do not reopen `.4.12`/`.4.10`/`.4.7`/`.4.2`/`.4.11`**  
**Pen:** self-perpetuating · **Lenses:** alive + all-is-one (pending)  
**DG held** until SM PASS · **No Belam box** · **No suite grant from this package** · season3 `4b8f28b5e` · capsule `fda4efd6e`  
**Writer:** Write+agi-turn — never write.py · **OWNER pytest ALLOWED — never strip** · KEEP ACL lean A

## Problem (measured)

| object | measured |
|---|---|
| `commands.py run verify` → bin-suite-fresh | **FAIL — SUITE REQUIRED** after gate-w LAND: `extensions/agi/bin/envfile.py` mtime newer than last suite run (expected — DG3 BUILD gate-w touched envfile.py for SOFT_SKIP expect-600); **no suite window granted** on land |
| Belam LAND OK | tip `2ba49b5df` (ff; tip^1=`f9515d8fa`; N1 ok; anonymize PASS; smoke PASS; links broken=0; labeled SOFT_SKIPs) — verify FAIL **1/13** = this residue only |
| parent `g5.4.1.4.12` | SM COMPLETE after land — **do not reopen** |
| prior suite leaf `.4.9` | COMPLETE (boxes.py/rotate.py/send.py window closed) — new leaf for **envfile.py** mtime, not reopen `.4.9` |

Owner zero leftover notes → real DESIGN leaf under `g5.4.1.4` (sibling of `.4.12`; not footnote).

## Standing path (ONE lean — ACCEPT)

**Route ONE suite window** via usual path: council DESIGN → SM gate → **SM ASK Belam for ONE suite grant** → operate (`verification.py` window → one-file / named pytest under grant citing `envfile.py` → `commands.py run verify`) until `bin-suite-fresh` PASS.

### Scope (binding)
1. Name exact ONE suite-window operate path in RULING (files / commands; cite `envfile.py`).
2. **Never** open suite window from this DESIGN package or from mint alone; **never invent GRANT**.
3. **Never** strip pytest. Never `git rm`. Never waive by footnote on `.4.12`/`.4.9`/`.4.2`.
4. After grant+operate: `bin-suite-fresh` PASS on live pilot tip; lock absent in MAIN and every post worktree.
5. KEEP ACL lean A (`group:agi:r--`).

### Rejected
- Self-grant / Belam grant before SM ASK / invent window without Belam GRANT after SM PASS.
- Reopening `.4.12` / `.4.9` / `.4.2` / `.4.7` / `.4.10` / `.4.11` as dump.
- Permanent waive footnote.

## Must-carry
1. Council+SM name ONE suite-window path citing envfile.py.
2. SM ASK Belam grant only after SM PASS.
3. `bin-suite-fresh` PASS post-operate; ZERO leftover notes.
4. Write+agi-turn; never write.py; never strip pytest; never git rm; KEEP ACL lean A.

## Falsifiers (for later operate / COMPLETE)
1. `python3 extensions/agi/bin/commands.py run verify` → `bin-suite-fresh` PASS under GRANT citing envfile.py (no SUITE REQUIRED).
2. Lock absent in MAIN and every post worktree after window.
3. **Negative:** invent window without Belam GRANT; permanent waive; strip pytest; reopen `.4.2`/`.4.7`/`.4.10`/`.4.11`/`.4.12`; season3 tip moved; write.py; git rm; Belam grant before SM ASK.

## Out of scope
Granting suite from this package · smoke .env/loop.log (closed by `.4.12.1`) · V3 pin · reopen `.4.12`/`.4.9`/`.4.2` · strip ACL · Master
