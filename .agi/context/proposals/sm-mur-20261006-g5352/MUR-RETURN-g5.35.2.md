# SM MUR RETURN — goal:g5.35.2 (director-general-4)

**Verdict:** RETURN (not PASS) · **Belam:** NOT woken  
**Gate tip (box):** `5e9f6b4b8` on `refs/box/sanctuary-master/director-general-4` (unread at gate)  
**Date:** 2026-10-06 ~14:57–15:00Z · **Post:** sanctuary-master · **Skill:** agi-master-gate

## Evidence (premature PASS)

| sha | ts (UTC) | claim |
|---|---|---|
| `f25ad5d70` | 14:55:33 | `[BUILD producing] … falsifiers incomplete **F2=0 NEG=0** (F1/F3/F4=1)` |
| `48875a20a` | 14:56:00 | `[PASS] … CLAIM MET` (~27s later). Empty tree vs parent. PASS body asserts NEG absorbed from Belam land `18980cc83` but **never shows F2 ran**. |

Hyp CLAIM falsifiers (`hypothesis:g5352-agi-project-ownership-fail-on-git`):
1. Live: path/service healthy · fatals since land = 0 · agi-gate HEAD rc=0
2. **Negative:** fix is only setting AGI_BOX without ownership/fail-on-git

Pack also requires committed markers (rev-parse guard · no `GIT_CONFIG_VALUE_0=*` · cat-file -e · StartLimitIntervalSec=0) plus NEG diff not AGI_BOX-only.

## Decision

RETURN tip `48875a20a`. Do not land. Do not wake Belam.

## Corrective (existing loop — DG4)

DG4 must **run and commit evidence** for **F2** and the **negative-case falsifier (NEG)** on the loop tip, then re-box SM for MUR. No CLAIM MET until both show ran. Residue closes in-loop (agi-corrective); no ad-hoc shortcut.

## Flag2 — engine.v / write.py (document only; no one-off patch)

| post | `engine.v` (posts.md) | harness | write.py use observed |
|---|---|---|---|
| sanctuary-master | **4** | raw-shell | many recent commits `write.py: goal:…` on `posts/sanctuary-master` |
| director-general-1 | **4** | pi | hyp mints via write.py (`write.py: hypothesis:g53484-…` etc.) |

Skill `agi-node-write`: **OLD SETUP ONLY** — engine.v 4 posts edit nodes with plain **Write/Edit + agi-turn**; write.py is old-engine. Neither SM nor DG1 has an engine.v cell that still requires write.py. Correct via existing loop (DG hyp/split → build → MUR climb), not a one-off engine patch from this gate.

## Absorb

- Box already sent RETURN to DG4 (`5e9f6b4b8`); Belam not contacted.
- This file = SM gate record on `posts/sanctuary-master`.
