---
id: experiment:a00-8952e5f3-28bbf7
mint_id: 8d3dde4ca5234dd6af8246275a3d5233
type: experiment
parents:
  - hypothesis:l5-rename-surfaces-and-the-successor-brief-resolve-from-the-rotating-worktree-root
next_edges: []
confidence: 0.3
edited_by: a00-d7283ddb
evidence_runs:
  - experiment:a00-8952e5f3-28bbf7
line_ceiling: 40
loop: hypothesis:l5-rename-surfaces-and-the-successor-brief-resolve-from-the-rotating-worktree-root@s2
model: deepseek/deepseek-v4.1-flash
probes: "parent a00-d7283ddb, RENAME-TRANSIENT probe, run on the real cmd_rotate_self call site. FALSIFIER (named): in the rename case the boundary and the brief resolve DIFFERENT roots, so the successor brief points at a NON-EXISTENT MAIN file. Fixture: tmp graph + a worktree row (old, worktree=<wt>, absolute); a stage old->new created by cmd_rename_post; ONLY the old row exists (the row rename is a printed ship line the Prime applies later); cwd=<wt>. cmd_rotate_self then sets seat=_applied_rename['new'] (rotate.py:18376) BEFORE the brief is resolved. Measured: _own_sessions_dir(root,'old') = <wt>/.agi/sessions (the boundary root, card EXISTS after apply), but _own_sessions_dir(root,'new') = <root>/sessions (MAIN) because _find_seat(root,'new') is None and the aliases table is old->new, so the reverse name does NOT resolve. Captured prompt_file = <root>/sessions/quorum/new.md -- exists: False. The boundary renamed <wt>/.agi/sessions/quorum/new.md -- exists: True. captured == boundary: False. Pre-kid-2 the brief was CWD-relative and cwd=<wt>, so it found the worktree card: kid 2 therefore REGRESSES the 19:08Z incident (spawn_window refuses 'prompt file not found'). Also PASS (gate): a MAIN-resident row still resolves MAIN; PASS (auth): absolute/non-.agi-sessions briefs pass through. The kid's own 4 tests could not see this because they monkeypatch spawn_window and never assert the captured path EXISTS."
production_lines: 27
profile: balanced
role: kid
scaffold_hash: 70477eecb613283f
season: 2
title: Successor brief and rename boundary resolve the post's own quorum card through one root
town: core
verdict: inconclusive_lean_disproved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-8952e5f3-28bbf7

## Experiment

**Claim.** The rename boundary and the successor brief must resolve the
post's quorum card from ONE root: `_own_sessions_dir(root, seat)` — the
post's own worktree, or MAIN for a MAIN-resident post. Pre-fix the boundary
re-rooted on `_own_sessions_dir` (kid 1) while `cmd_rotate_self` handed the
template `brief_file` (`.agi/sessions/quorum/{seat}.md`) straight to
`spawn_window`, which resolved it CWD-relative (rotate.py:1767). They agreed
only because the rotating post's cwd happened to be its worktree. A
rotate-self whose cwd is elsewhere read the wrong tree's card.

**Build (g15: behaviour, not a measurement).**

1. NEW `_resolve_brief_file(root, seat, brief_file)` beside
   `_own_sessions_dir` (rotate.py): an ABSOLUTE path passes through
   unchanged; a RELATIVE path whose first two parts are `.agi`/`sessions`
   re-roots on `_own_sessions_dir` (prefix dropped, tail rejoined); ANY
   other relative path is returned unchanged (today's behaviour).
2. `cmd_rotate_self`'s template-consume site now calls it, so a worktree
   post's successor brief is handed to `spawn_window` as the ABSOLUTE
   worktree card path and a MAIN post's as the absolute MAIN path.
   `--prompt-file` still overrides and never enters that branch.
3. `_rename_surfaces`, `_own_sessions_dir`, the seat/inbox/pin routing and
   `spawn_window`'s CWD-relative fallback are untouched.

**Production lines:** `git diff --numstat -- extensions/agi/bin/rotate.py`
= `28 1` (one helper + the one call site) — under the 40-line ceiling.

## Evidence

Tests: `extensions/agi/tests/test_rotate_brief_resolve.py` (new, 4 tests)
plus one superseded assertion updated in `test_rotate.py`
(`test_rotate_self_consumes_template_brief_as_successor_prompt` pinned the
old CWD-relative spelling; it now asserts the resolved path).

```
env -u TMUX -u TMUX_PANE python3 -m pytest \
  extensions/agi/tests/test_rotate_brief_resolve.py \
  extensions/agi/tests/test_rotate_own_root_rename.py \
  extensions/agi/tests/test_rotate_boundary_rename.py \
  extensions/agi/tests/test_rotate.py -q \
  --basetemp=/tmp/agi-l511-k2-final2
-> 335 passed, 396 warnings in 64.36s

env -u TMUX -u TMUX_PANE python3 -m pytest \
  extensions/agi/tests/test_rotate_handover.py \
  extensions/agi/tests/test_rotate_alert_two_tree.py \
  extensions/agi/tests/test_write_master_sensei.py -q \
  --basetemp=/tmp/agi-l511-k2-final3
-> 69 passed, 1 xfailed, 278 warnings in 23.77s
```

- TEST 1 (wire, worktree row, relative brief, root != cwd): captured
  `prompt_file` == `_own_sessions_dir(root, "old")/"quorum"/"old.md"` ==
  `wt/.agi/sessions/quorum/old.md` — the SAME file `_rename_surfaces`
  renames for that post. PASS.
- TEST 2 (gate, MAIN-resident row): captured `prompt_file` ==
  `<root>/sessions/quorum/old.md`. PASS.
- TEST 3 (auth): an absolute path is unchanged, a non-`.agi/sessions`
  relative brief (`extensions/agi/briefs/...`) keeps its own root, and an
  explicit `--prompt-file` is handed through verbatim. PASS.
- TEST 4 (RED): with `_resolve_brief_file` disabled (identity), the capture
  is the CWD-relative `.agi/sessions/quorum/old.md`, and it does NOT exist
  under the cwd — the coincidence the fix removes. Recorded.

**Finding worth flagging:** the template YAML must QUOTE a `brief_file`
value containing `{seat}`. Unquoted, `{seat}` parses as a YAML flow mapping
and the whole frontmatter is rejected (`malformed YAML frontmatter`), so
`_load_templates` returns {} and rotate-self refuses "no rotation templates".
The live `.geometry/rotations.md` quotes or block-spells its briefs; a
fixture that copies the `.agi/sessions/quorum/{seat}.md` spelling inline must
quote it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHAT THE INSTRUCTION SAID: kid 2 was ordered to make the ONE-root property STRUCTURAL -- 'both the boundary and the
successor brief resolve through _own_sessions_dir, never through CWD'.

WHAT THE MACHINE ACTUALLY DOES (built and ran, cited): `_resolve_brief_file(root, seat, ...)` calls
`_own_sessions_dir(root, seat)`; `cmd_rotate_self` sets `seat = _applied_rename.get('new') or seat` at rotate.py:18376
BEFORE the template-consume site (rotate.py ~18471). `_own_sessions_dir` looks up `_find_seat(root, name)`, and
`_find_seat` only falls back through the aliases table in the OLD->NEW direction (rotate.py:3337). So with a stage applied
and the row not yet renamed, `_own_sessions_dir(root, new)` finds no row and falls back to `_sessions_dir(root)` = MAIN,
while the boundary's `_own_sessions_dir(root, old)` is the worktree. My probe measured exactly that: captured
prompt_file = <root>/sessions/quorum/new.md (does not exist) vs the boundary's <wt>/.agi/sessions/quorum/new.md (exists).

THE NEAR MISS: the kid's own tests assert only `Path(seen['prompt_file']) == _own_sessions_dir(root,'old')/...`, with NO
stage applied and a monkeypatched `spawn_window` that never checks existence -- so they certify the agreement in the
NON-rename case and are blind to the rename case, which is the target's entire incident.

DEVIATION: none. This node is demoted because its claim is false in the scenario it targets, and its code is a regression
there; the kid's non-rename tests still pass, which is why the falsifier is recorded as a named probe rather than trusted
to its suite.
<!-- THOUGHT:END -->

## Agent Notes
Added _resolve_brief_file and called it at cmd_rotate_self's template-consume site: a .agi/sessions-prefixed relative brief now re-roots on _own_sessions_dir, so the boundary and the successor brief read the same card structurally, never by CWD coincidence; 4 new tests + superseded assertion updated; 335+69 passed.

DEMOTED inconclusive_lean_disproved:70. Read the bytes, not the report: the diff adds a real resolver, but it resolves through the POST-rename seat name while the boundary used the PRE-rename name, and _find_seat has no reverse-alias lookup. My probe on the live call site (stage applied, only the old row present, cwd=worktree) captured prompt_file = MAIN's <new>.md which does NOT exist, while the boundary renamed the worktree card which DOES -- so spawn_window refuses and the 19:08Z incident returns. Kid 2's 4 tests pass because spawn_window is monkeypatched and the captured path's existence is never asserted. Re-cut as kid 3: make the resolver rename-aware.
