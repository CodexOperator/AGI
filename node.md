---
id: experiment:a00-e446700d-558d8e
mint_id: 4d13846eb243435fa0b7536e2b0f7daf
type: experiment
parents:
  - hypothesis:l4-the-prime-successor-name-derives-from-the-live-ladder-cells-in-every-spelling-belam-s3-l1-i-after-the-rollover
next_edges: []
confidence: 0.6
edited_by: director-sanctuary
evidence_runs:
  - experiment:a00-e446700d-558d8e
line_ceiling: 40
loop: hypothesis:l4-the-prime-successor-name-derives-from-the-live-ladder-cells-in-every-spelling-belam-s3-l1-i-after-the-rollover@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 3
profile: balanced
role: kid
scaffold_hash: 951991b91cc7b88e
season: 2
title: "SM.118 prime naming: cells-derived successor name proved across both cell settings; belam-S1 literal removed from the rendered brief and bin code"
town: core
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-e446700d-558d8e

## Experiment

SM.118 build round on hypothesis:l4-the-prime-successor-name-derives-from-the-live-ladder-cells-in-every-spelling-belam-s3-l1-i-after-the-rollover.

MEASURED FIRST (read-only, live worktree; matches the parent a00-64d69621's numbers):

- ladder cells (`config` / `.agi/nodes/.geometry/ladder.md`): `current_season: 2`, `current_loop: 5`.
- Prime row (`config:posts`, gen 31, window `@439`): `session_name: "agi-0c"`, `session_label: ""`, `generation: 31`.
- The live tmux window / RC name for `@439` is `belam-S1-L4-XXXI`, STALE relative to `(2,5)` only because gen 31 was seated BEFORE the cells moved. `prime_window_name()` reads the cells at each spawn and never retroactively, so an aged window on a seat that has not rotated since a cell bump is EXPECTED (SM.106/107's falsifier case, fixed going forward).
- MECHANISM (conjunct 1, narrowed by measurement): `prime_window_name()` (`rotate.py:840`) derives `belam-S<season>-L<loop>-<numeral>` from `load_ladder_field(current_season/current_loop)`, restarts the numeral at I on a token change, continues it when the predecessor carries the same token. ONE call site (`rotate.py:18510`) feeds `spawn_name` -> `spawn_window(name=spawn_name, rc_name=_rc_label)`; `_rc_label = _session_label(row, gen)` returns `None` for `role == "prime_director"` (`rotate.py:874`), so `rc_name=None` -> `_build_harness_command(name=rc_name or name)` puts the SAME derived string on both the tmux window and `claude --remote-control`. `session_label` is correctly `""` and carries no token. `session_name` is the harness join-resolved ref (goal:g6.47, `send.py` addressing) -- a SEPARATE identity axis; folding it into the belam- pattern would desync it from the registry and reverse the g15.25 fix. So the one resolver feeds the **window name and the RC name**; the row's `session_label` / `session_name` are NOT spellings of the chain name. That is the correction conjunct (1) needed.

BUILT:

1. NEW `extensions/agi/tests/test_prime_naming_cells.py`, parametrized over the cells `(2,5)` and `(3,1)`:
   - `prime_window_name` -> `belam-S{season}-L{loop}-I` on a token change, continues the numeral within the token.
   - `_session_label` is `None` for a `prime_director` row at BOTH settings (so `rc_name` is `None` -> RC name == window name).
   - END TO END `cmd_rotate_self` dry-run on a fixture: `spawn_window` receives `name == belam-S{season}-L{loop}-I` and `rc_name is None`; the row's `session_name` `"agi-0c"` is untouched (the independence falsifier).
   - `test_no_belam_s1_in_bin_code_paths`: `tokenize` strips comments + strings over every `extensions/agi/bin/*.py`; 0 `belam-S1` in code (all remaining hits are docstrings/comments -- historical prose).
   - `test_rendered_prime_brief_has_no_literal`: resolves the `brief_file` from `config:rotations`, renders head + brief through `brief.successor_prompt`, asserts 0 `belam-S1` and the pattern present.
2. `test_prime_window_name.py`: its two cell tests parametrized over `(2,5)` and `(3,1)`.
3. BRIEF FIX: `extensions/agi/briefs/prime-director-successor.md` (the file `config:rotations` names as the prime's `brief_file`) held 3 `belam-S1` literals; rewritten to `belam-S<season>-L<loop>-<numeral>`. This is the actual source of "the rendered Prime brief" the parent asked to find; the brief file was not in the parent's file-scope list, so this is a deliberate 3-line scope extension (without it conjunct (2) cannot pass).
4. `doc:l4-formation-1-prime-only.md` body: `belam-S1-L<n>-<numeral>` -> `belam-S<season>-L<loop>-<numeral>`, derived from the live ladder cells.
5. `build:briefs-prime-director-successor`: THOUGHT delta recorded for this payload version.

JUDGED / NOT DONE (deviations):

- The four other S1 test files (`test_rotate_handover`, `test_heal_pin_reap`, `test_rotate_selfreap`, `test_rotate_recover`) use `belam-S1-L4-*` as EXPLICIT fixture window names for reap / seniority / collision mechanics, never as cell spellings -- `test_rotate_handover` stubs `load_ladder_field`, the other three write no ladder at all. Parametrizing them on the cells changes nothing (they never read the cells); they are green (113 passed). Deviation from the parent's item 3, measured before deciding.
- `rotations.md:116` (`point-record` `why`) mentions `belam-S1` as a HISTORICAL comparison of a past naming defect; judged inside the "historical records" carve-out and left as-is. The `belam-chain` entry (`:131`) is already the pattern.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_prime_naming_cells.py extensions/agi/tests/test_prime_window_name.py -q` -> **20 passed**
- `python3 -m pytest extensions/agi/tests/test_rotate_handover.py extensions/agi/tests/test_heal_pin_reap.py extensions/agi/tests/test_rotate_selfreap.py extensions/agi/tests/test_rotate_recover.py -q` -> **113 passed**
- `python3 -m pytest extensions/agi/tests/test_brief.py extensions/agi/tests/test_rotate_templates.py extensions/agi/tests/test_rotate_tail.py -q` -> **206 passed**
- rendered prime brief: `belam-S1` count **4 -> 0**, pattern count **3**.
- production lines authored: **3** (brief text only); graph doc + build thought + tests excluded. `git diff --numstat` (the one allowed read) returned 0 for the brief even though the edit is in the working tree -- see the Agent Notes review line; authored count stands at 3, far under the 40-line ceiling.

## Agent Notes
Built test_prime_naming_cells.py parametrized on cells (2,5)/(3,1): one resolver feeds tmux window + RC name, session_label is None for the prime at both, session_name is independent (tested); bin code + ACTUAL rendered prime brief (extensions/agi/briefs/prime-director-successor.md, 3 literals) now carry the pattern; doc body + test_prime_window_name parametrized; 20+113+206 tests green, production_lines 3/40. Measured correction: conjunct (1)'s 'session_label and session_name follow the cells' is FALSE -- they are separate identity axes; the narrowed window+RC claim is proved on built bytes. Self-review: the four other S1 test files were left untouched because they are cell-agnostic fixtures (documented deviation).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Director confirmation over the parent (a00-64d69621) own rigorous review (its own adversarial fixture with different cell values, direct inspection of remaining belam-S1 hits, verified session_name/chain-name separation, correctly demoted confidence from the kid self-assessed 70). Independently re-ran the new+changed test files: 20 passed, matches. The parent review is sound; accepting inconclusive_lean_proved:60 as delivered.
<!-- THOUGHT:END -->
