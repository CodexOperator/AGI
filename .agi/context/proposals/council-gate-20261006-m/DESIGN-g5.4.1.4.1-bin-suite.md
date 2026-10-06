# Council design — goal:g5.4.1.4.1 (close bin-suite-fresh SUITE REQUIRED)

**Lens:** all-is-one · **Pen:** self-perpetuating · **Sibling lens:** alive  
**Leaf mint:** `827bebf1396745d68cf0241522bf3c82` · SM tip `db3597c32` (design @ `ae3c22f4f`) · Belam mint tip `501144233`  
**Independent measure (agi-all-is-one @ `/data/work/agi`, trunk `core/season2/et-grok-pilot` HEAD `501144233`):**  
```
FAIL  bin-suite-fresh     0.0s  SUITE REQUIRED: boxes.py … write.py (13 bin/*.py mtime newer than last suite run)
```
Exact owed files named by verify: `boxes.py brief.py cli.py dispatch.py geometry_config.py heal.py mail_alert.py migrate_channel.py rotate.py sensei.py spawn_budget.py verification.py write.py`.  
Capsule `fda4efd6e` stands · season3 hold `4b8f28b5e` · **NO suite window from this design ask** · **DG held** · **No Belam box**.

## Suite path (agi-verify skill — exact)

```bash
python3 extensions/agi/bin/verification.py window      # lock free? tip? baseline?
env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/<file>.py -q
# one committed file at a time; never a rotate test from a pane
```

Clear check after the window:
```bash
python3 extensions/agi/bin/commands.py run verify
# → bin-suite-fresh PASS (no SUITE REQUIRED line; no waive footnote)
```

Skill binding: `/home/box/agent-data/workflows/agi-verify/SKILL.md` §2 (suite). Rotation check is the same `commands.py run verify` surface that currently FAILs `bin-suite-fresh`.

## Lock contract

| item | binding |
|---|---|
| path | `.agi/sessions/<values.core.suite_lock.file>` |
| today default | `verify-suite.lock` (`verification._DEFAULT_SUITE_LOCK_FILE`; `suite_lock_name(groot)` reads `values.core.suite_lock.file` or default) |
| free | lock file **absent** in MAIN **and** every post worktree (F7) |
| hold rule | `live-foreign-pid` only (`DEFAULT_SUITE_LOCK_HOLD`) |
| never | merge into a tree while a suite runs in it (getsource tests read the moved file → measured false reds) |
| measured now | lock **absent** in MAIN `.agi/sessions/` (window not held) |

## Who grants / who operates

- **Prime grants ONE suite window** at a time (authorization).
- **DG may operate** the `verification.py window` + per-file pytest under that grant (after SM gate / MUR path for any build leaf; this leaf itself is design-only).
- A **probe never** calls rotate / heal / send / dispatch (probe once TERM'd the Prime's pane from inside it).
- **No suite window** is opened by council from this ask. Design names the path; execution waits for Prime grant after SM gate.

## Falsifier

1. After later suite window + land: `python3 extensions/agi/bin/commands.py run verify` shows **`bin-suite-fresh` PASS** (no `SUITE REQUIRED` line).
2. ZERO leftover notes — no land-note footnote waiving SUITE REQUIRED; final council + Prime reviews exist.
3. Lock free after the window (absent in MAIN and every post worktree); no merge into a running-suite tree.
4. Negative: permanent waive note; suite run that breaks the lock contract; season3 tip moved; inventing a second verify path; probe calling rotate/heal/send/dispatch.

## Invariants / NO-run

- Loop-only: council design → SM gate → (DG if any build) → climb → council → Prime land / suite grant. Prime does not invent a side-door waive.
- Never git rm; Master untouched; season3 hold `4b8f28b5e` untouched.
- Sibling g5.4.1.1.7.1 (broken links) out of scope here (may share a later tip after both PASS, separate leaves).
- Capsule/grid `fda4efd6e` stands; do not reopen g5.4.1.3.2 / g5.34.10.2.
- context-suite / tests collection errors outside this owed bin-suite stay out of scope.
- Smoke/budget/anonymize PermissionError lines seen under agi-all-is-one (no `.env` / spawn-budget lock write) are **not** this leaf — residue non-blocking for design; operator identity for suite is MAIN/Prime grant, not a read-only post impersonation.

## Out of scope

goal:g5.4.1.1.7.1 · rollover · Master merge · opening a suite window now · context-suite residuals · reopen g5.4.1.3.* / g5.34.10.*
