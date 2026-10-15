---
id: experiment:dg2g6-c-recheck
mint_id: ef0533c05cf94a929c7f221e91b97791
type: experiment
parents:
  - hypothesis:anonymize-check-refuses-the-home-path
  - experiment:dg2-c1-home-path-baseline
next_edges: []
edited_by: director-general-2
scaffold_hash: df31f1fe958fe383
season: 2
title: "C re-run from the hypothesis's own falsifiers at 4d1f9167f: check refuses a staged home path (rc 1), 0 nodes carry it, one token list and one checker; home-regex census 3 definitions"
town: core
---
# experiment:dg2g6-c-recheck

# experiment: C re-verdict from its OWN falsifiers (goal:g7.16.1.1.6)

Parent: hypothesis:anonymize-check-refuses-the-home-path. Supersedes nothing: experiment:dg2-c1-home-path-baseline (trunk 59ad74144) stays as the baseline.
Run by director-general-2's kid, MAIN at 4d1f9167f, 2026-09-29T23:57Z, read-only (probes in a scratch git repo under /tmp; tests on MAIN's files, PYTHONDONTWRITEBYTECODE=1, behind /tmp/dg2b3/pytest.lock).
No falsifier moved: anonymize.py, test_anonymize_guard.py and the `.agi/nodes` scope are where the hypothesis wrote them; nothing re-pointed.

## FALSIFIERS, as written
| # | falsifier | command | observed | fires? |
|---|---|---|---|---|
| F1 | `check` on a staged file carrying the home path exits 0 | scratch repo (`.agi/config.json`, `git init`), `git add` a file holding `$HOME/x.md`, `anonymize.py check --root <scratch>` | `REFUSED: text carries home`, rc **1** | no |
| F1b | same, HOME set to a tmp dir OUTSIDE the generic `/home` shape (so only the box_tokens HOME token can catch it) | `HOME=<scratch>/fh/user1 anonymize.py check`, staged text holding that path | REFUSED, rc **1** | no |
| F1c | control: placeholders `<home>/x.md`, `~/x.md` staged | same | `anonymize: ok`, rc **0** | (guard not over-broad) |
| F2 | any node still carries the path: `git grep -lF "$HOME" -- .agi/nodes \| wc -l` > 0 | worktree / `HEAD` / live-only (`:!.agi/nodes/deprecated`) | **0 / 0 / 0** | no |
| F2b | the generic class over the same scope (bundle 2/3 widening) | `git grep -lP "$(anonymize.HOME_PATH_RE.pattern)" -- .agi/nodes \| wc -l`; `HEAD` over the four scrub scopes | **0**; **0** | no |
| F3 | a second token list or a second checker appears (the diff adds a function that scans for paths outside `box_tokens`) | read anonymize.py whole (180 lines); `git log` of anonymize.py since bundle 1 | ONE token list (`box_tokens` :56-89, HOME appended on BOTH the fixture :66 and live :89 returns); ONE checker (`scan` :90-97, called only by `cmd_check` :138). Bundle 2 R3 (df26adc55) added `HOME_PATH_RE.search` INSIDE `scan`, not a new function; no function scanning for paths was added outside box_tokens/scan | no (see census finding) |

## CLAIM conjuncts
| # | conjunct | TRUE/FALSE | command |
|---|---|---|---|
| (1) | `box_tokens` returns the box user's home path as one more token (class `home`), so `check` refuses staged text carrying it | **TRUE** | `CLASSES` (anonymize.py:12) holds `home`; box_tokens :62/:66/:89; F1, F1b rc 1; `test_check_refuses_the_home_path`, `test_the_live_path_carries_the_home_token` pass |
| (2) | one committed test row feeds `scan` a text holding a tmp home and asserts the hit | **TRUE** | test_anonymize_guard.py:283 (tmp HOME, asserts `scan == ['home']`, `cmd_check == 1`, value never printed); strict xfail dropped. `flock /tmp/dg2b3/pytest.lock env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_anonymize_guard.py -q --basetemp /tmp/dg2g6/c/bt -p no:cacheprovider -rs` -> **30 passed**, 0 skipped (the HEAD scrub-scope row ran) |
| (3) | the 13 nodes rewritten to `<home>`; `git grep -lF "$HOME" -- .agi/nodes` empty | **TRUE** | F2: 0 |

## Census finding (goal part 2; NOT a falsifier of this hypothesis)
The home-path class has ONE home in the guard (anonymize.py:19 `HOME_PATH_RE`, code, not a config cell) but THREE regex definitions across extensions/ skills/:
- extensions/agi/bin/anonymize.py:19 `HOME_PATH_RE` -- the refusal's class (`/home` or `/Users`, user-name segment); reused by `home_relative` :26, `scan` :95, rotation_record.py:33, test_anonymize_guard.py:422, and named (not copied) by skills/agi-master-gate/SKILL.md:64.
- extensions/agi/bin/paths.py:10 `HOME_RE` -- paths.py audit's `home` class (added 266b24054, 2026-09-18, BEFORE bundle 1). Disagrees: no `/Users`, and a dot segment (`/home/.cache`) matches here but not in anonymize. It also folds in `~/`, `$HOME`, `expanduser` (source-literal audit, a wider class).
- extensions/agi/tests/test_no_home_literal.py:26 `_HOME_LITERAL` -- goal:g15.29.2's engine-literal test (8a2ed480e, 2026-09-23); no `/Users`.
- .agi/nodes/.geometry: 0.
F3 is scoped to "the diff adds", and both copies predate the row, so it does not fire; but a one-source census row for this class would FAIL today at 3 (2 outside tests).

## Side observation
MAIN's common git dir has no `pre-commit` hook (samples only): the refusal reaches commits through `commands.py run verify` (verification.py:1267 `check_anonymize`, the quick set), not a hook. The hypothesis claims `check`, not the hook, so this is not a conjunct.
