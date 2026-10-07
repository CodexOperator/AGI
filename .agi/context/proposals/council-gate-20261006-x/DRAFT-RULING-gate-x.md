# DRAFT ruling — gate-x (council-gate-20261006-x) — DESIGN g5.4.1.4.13

**Pen:** self-perpetuating · **Lenses:** alive (**PASS lean** · `LENS-alive.md` · box `32f383389`) · all-is-one (**pending**)  
**Designs:** `DESIGN-g5.4.1.4.13-suite-window-envfile.md` (mint `5e5886f44ca24db68a70b9cf62a12726`) · `DESIGN-batch-gate-x.md`  
**ASK/SM tip (SoT):** `779ab9b12` (`779ab9b12120111f2805f6cd4685b6a882e5f8eb`) · **Live pilot:** `2ba49b5df` (`2ba49b5dfb5875f701413a0892c46a47246ab6cf`; tip^1=`f9515d8fa`) · SM ASK box tip `9ac935925`  
**Ask:** `sm-council-ask-20261006-x.md`

## Draft verdict (not final — do not ready-for-gate until BOTH lenses PASS)

**LEAN PASS** pending aio fold — design sufficient for SM gate on X1 once aio PASS|lean. **ACCEPT** standing path: (X1) ONE suite window via council DESIGN → SM gate → **SM ASK Belam for ONE suite grant** → operate (`verification.py` window → one-file/named pytest under GRANT **citing `envfile.py`** → `commands.py run verify`) until `bin-suite-fresh` PASS. **Never invent GRANT** from this package. **Never self-grant.** **Do not reopen** `.4.2` / `.4.7` / `.4.9` / `.4.10` / `.4.11` / `.4.12`. KEEP ACL lean A. **DG held** until SM PASS. **Do not box Belam.** Season3 `4b8f28b5e` / capsule `fda4efd6e` stand. OWNER pytest ALLOWED — never strip. Writer Write+agi-turn — never write.py.

## Must-carry (short) — ONE leaf

### X1 — g5.4.1.4.13 ONE suite window clear bin-suite-fresh (envfile.py)
1. Clear bin-suite-fresh mtime residue (`envfile.py` newer than suite stamp after gate-w DG3 BUILD) via ONE suite window after SM PASS + **SM ASK Belam GRANT**.
2. Never self-grant; never invent GRANT; never reopen `.4.9`/`.4.12`/`.4.2`/`.4.7`/`.4.10`/`.4.11`; never strip pytest; never git rm; never waive-as-footnote.
3. Path: `verification.py window` → one-file/named pytest under grant citing `envfile.py` → `commands.py run verify`.
4. Falsifier: `bin-suite-fresh` PASS; lock free MAIN + all post worktrees; `getfacl -p .env` still lean A.

## Measured (pen · 2026-10-06 ~20:12 ET)
- Live pilot `2ba49b5df` (ff; tip^1=`f9515d8fa`)
- SM tip `779ab9b12` · leaf `.4.13` active mint `5e5886f44…` (absent live)
- `.4.12`/`.4.12.1`/`.4.9`/`.4.10`/`.4.11`/`.4.7` COMPLETE @ SM — do not reopen
- MAIN `.env` ACL `group:agi:r--` KEEP
- bin-suite-fresh FAIL — SUITE REQUIRED: envfile.py (mtime 23:59:17Z > suite 22:45:30Z); only envfile.py newer
- MAIN signingkey unset · season3/capsule stand · no GRANT invented

## Holds
Belam HOLD · DG held · no suite grant · keep ACL lean A · never reopen leave-alones · never write.py · never git rm · never strip pytest · season3/capsule stand
