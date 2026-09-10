---
id: mvp:unified-verification-command
mint_id: a73a3eb362384348a4cfaf5e0e7e7546
type: mvp
parents:
  - hypothesis:l4-unified-verification
next_edges: []
confidence: 0.7
edited_by: sanctuary-director
scaffold_hash: e8a2c12a788a2111
season: 2
status: open
thought_session: sanctuary-director-genIII-L4
title: "What verification.py must satisfy: one resolved entry point, three levels, an opt-in suite, and a node count compared rather than printed"
---
<!-- BODY:BEGIN -->
# mvp:unified-verification-command

**The contract `extensions/agi/bin/verification.py` must satisfy.** Design, not
code — the code is the build node minted from the file once it exists.

## The interface it fixes

```
verification.py [--level quick|rotation|full] [--suite] [--json] [--verbose]
commands.py run verify            # the declared entry point a successor types
```

`--level` defaults to `rotation`. `--suite` is orthogonal to `--level`, never
implied by one. Exit status is 0 only when every selected check passed.

## The minimum behaviour

| # | Requirement | Falsifier |
|---|---|---|
| 1 | **Every check is resolved through `commands.py` from `command:commands`.** A check the node does not yet declare is ADDED to the node, never inlined. | An argv already declared in `.geometry/commands.md` appears literally in `verification.py`. |
| 2 | `quick` = links + goals-check + write-guard. No dispatch, no smoke. | `quick` runs the smoke pass or pytest. |
| 3 | `rotation` = quick + smoke + viewport-verify + dispatch-help + budget. | A successor still has to type a second command to be safe to dispatch. |
| 4 | `full` = rotation + schema + credentials + secrets + crons. | A level runs pytest without `--suite`. |
| 5 | **The node count is COMPARED, not printed.** The active/deprecated/total triple is recorded under `.agi/sessions/`; a run whose active count is BELOW the recorded value FAILS and names the drop. First run records, passes, and says it had no baseline. | A shrinking graph exits 0. |
| 6 | **One summary block.** Per check: PASS/FAIL, elapsed, and the number that check exists to produce. Per-check stdout suppressed unless it FAILS or `--verbose`. `--json` carries the same facts. | The successor reads four scrollbacks, which is the token cost the round exists to remove. |
| 7 | The four-command list at `briefs/prime-director-successor.md` line 7 names ONE command, edited through `write.py … "replace payload N:M -"`. | The brief file is hand-edited, or still lists four tools. |

## Explicitly out of scope

- **`rotate.py` and `cli.py`.** Not touched by this build at all.
- **`bin/verify_unified.py`** — the `goal:g11` migration checker, a different
  thing one keystroke away. Not extended, imported, renamed or deleted. The new
  module's docstring must say which is which in its first paragraph.
- Running the full pytest suite by default. The suite window is granted by the
  Prime, one runner at a time; a verification tool that takes it unasked turns
  a safety check into a scheduling conflict.
- Fixing anything a check reports. `verification.py` reports; it never repairs.

## The falsifier a later reader should apply

Grep `verification.py` for any argv string that `.geometry/commands.md` already
declares. If one is there, this MVP was not discharged, however green the tests
are — the whole point of `goal:g1.10` is that there is exactly one copy, and a
tool everybody trusts is the worst place to put a second.
What does it produce?

## Agent Notes
REMAINDER, ruled by the Prime 2026-09-10: `--suite` is opt-in only WHILE `test_send.py` still nudges real tmux panes. When L4.10 lands, `--level full` folds the suite in and `verification.py` holds a file lock under `.agi/sessions/` so two suite runs can never overlap -- closing trap 0e by mechanism instead of by memory. Until then the lock is welcome but not required, and the fold-in is NOT to be implemented. This is what the file owes, recorded here so the next successor inherits the debt rather than rediscovering the reason.
