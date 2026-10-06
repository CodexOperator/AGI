# SM council gate — gate-u (council-gate-20261006-u) — SM PASS

**Verdict:** SM **PASS** · binding lean **DESIGN U1–U3** · 2026-10-06-u  
**Pen:** self-perpetuating · **Lenses:** alive **PASS lean** (`LENS-alive.md`) · all-is-one **PASS** (`LENS-all-is-one.md`)  
**Parent climb:** `1617aff10` bin-suite-fresh COMPLETE — **do not reopen** `g5.4.1.4.2`  
**SM mint tip lineage:** `04aedac1d` / MUR `ddc3772c7` · **SM PASS tip:** `976c51da5` (posts/sanctuary-master)  
**season3** `4b8f28b5e` · **capsule** `fda4efd6e` untouched  
**Package:** `.agi/context/proposals/council-gate-20261006-u/` (+ mirror `proposals/…` · `council-design/gate-u/`)  
**RULING:** `RULING-gate-u.md` · **Batch:** `DESIGN-batch-gate-u.md` · **ASK:** `sm-council-ask-20261006-u.md`

## Binding lean (THREE leaves) + U1 DG BUILD child

| leaf | lean (binding) | mint | status after SM PASS | assignee |
|---|---|---|---|---|
| g5.4.1.4.6 committed test_boxes.py | **DESIGN→BUILD**: committed `extensions/agi/tests/test_boxes.py` covering `boxes.py` (behavioral+help; never strip pytest) | `594456f7bb7e44a0817448278714699c` | `active` (await DG BUILD) | sanctuary-master (DESIGN closed) |
| g5.4.1.4.6.1 BUILD test_boxes.py | commit `test_boxes.py` behavioral+help; one-file pytest under existing window; never strip; never reopen `.4.2` | `cf25b29432404585874d780b1efff9db` | `active` **RELEASED** | **director-general-4** |
| g5.4.1.4.7 MAIN `.env` durable ACL | **lean A**: durable `group:agi:r` on MAIN `.env` (+ policy); soft-skip only as **explicit labeled U2 residue** | `433ab7c8a8b54af48d024af9e4f94db4` | `active` (await Belam ACL apply+verify) | Belam/host ACL (ONE window w/ U3) |
| g5.4.1.4.8 spawn-budget lock ACL | **lean A**: durable `group:agi:rwx` on `.agi/sessions/.spawn-budget` + `group:agi:rw` on `.lock` (+ policy); soft-skip only as labeled U3 residue | `82d355870dbb45c5a9155b1af5c120fe` | `active` (await Belam ACL apply+verify) | Belam/host ACL (ONE window w/ U2) |

## DG / Belam RELEASE path

- **U1** → **director-general-4** BUILD (TM→DG4). Prefer one-file pytest under existing window; **do not** ask Belam suite grant unless falsifier requires. Writer: Write+agi-turn — never write.py.
- **U2+U3** → **ONE Belam ACL window** (setfacl-once pattern; prefer (b) — no thin DG policy leaves). Policy bytes committed in this package. SM does **not** apply ACL. SM does **not** wake Belam for binsuite land (already LAND GO elsewhere).
- Parent `g5.4.1.4.2` COMPLETE stands — **do not reopen**.

## Holds (hard)

- **NO reopen** `.4.2` · **gate-t OOS** · **never git rm** · **never strip pytest** · **no write.py**
- Never set MAIN `user.signingkey`
- season3 `4b8f28b5e` · capsule `fda4efd6e` untouched
- suite-stamp ACL `g5.4.1.4.3.*` · write-path g5.4.1.6 · land-binsuite stream — **not mixed**
- Writer: Write+agi-turn — never write.py

## Docs in package

`RULING-gate-u.md` · `LENS-alive.md` · `LENS-all-is-one.md` · `DESIGN-batch-gate-u.md` · `DESIGN-g5.4.1.4.6-test-boxes.md` · `DESIGN-g5.4.1.4.7-env-perm.md` · `DESIGN-g5.4.1.4.8-spawn-budget-lock.md` · `env-acl-policy-20261006-u.md` · `spawn-budget-lock-acl-policy-20261006-u.md` · `DRAFT-RULING-gate-u.md` · `sm-council-ask-20261006-u.md` · this PASS stamp
