---
id: goal:g1.31.5.3
mint_id: 3eaa9c12ea4943a0ab7463f3eeb6b39e
type: goal
parents:
  - goal:g1.31.5
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.5.3
goal_kind: subgoal
origin: goals-doc
scaffold_hash: d7dc31bfeb8a8f0d
season: 2
seeds: []
status: active
tags:
  - engine
  - pass
  - pass-b3
  - missed
  - rotate
  - heal
title: "G1.31.5.3: rotate.py + heal.py -- announce sees every post session, cut/prompt/worktree/model from cells, true heal comments, 3 strict xfails green"
town: core
---
# goal:g1.31.5.3

## Why this exists
goal:g1.31.5: 6 PASS B3 `missed` rows whose fix lands in rotate.py or heal.py (DG5 lane; n107 moved here by SM 09-30 because the second posts parser lives in rotate.py). Verify files are under `.agi/sessions/workflows/runs/`. Re-read at HEAD d4b7ead17:
```
n    sev      round (verify file)                                                          HEAD cite
33   residue  l3w4-rotation-announces-itself (mur-pb3chunk14of20)                          rotate.py:5796 _observed_windows
129  residue  l4-the-window-reply-and-harvest-or-cut-are-captive-steps (mur-pb3chunk9of20)  :17624-17625 · :4222-4223 · :17423 · :22142-22143
130  nit      l4-the-window-reply-and-harvest-or-cut-are-captive-steps (mur-pb3chunk9of20)  :17600
139  nit      l3w0-rotate-roles (mur-pb3retry20s)                                          :118-135 DEFAULT_CC_ROLES
76   nit      engine-delta-2 (mur-pb3chunk1of20)                                           heal.py:892 · :915 · :1073
107  residue  l4-the-predecessor-hands-over-authority (mur-pb3chunk6of20)                   test_rotate.py:10450,10457 · test_rotate_templates.py:1424
```
```
_observed_windows(one tmux session) --names--> live_names (:3581, :21282) --> _announce_rotation (:6482)
   --> _derive_receivers (:6424) keeps receivers ∩ live   => a post seated in agi-master* or the Prime's session is dropped as dead
   (rotate.py status already reads those sessions: :3802)
worktrees_root cell = paths.core.worktrees_root (.agi/config.json:226); 0 readers in rotate.py; 5 literal lines
3 × @pytest.mark.xfail(strict=True, "RED until DG3 ...") => suite green while the requirement is unwritten
   rotate.py:10808 _posts_load_error · :10820 _row_names  (the 2nd posts parser)
   rotate.py:13934 facts_body_ranges vs .geometry/rotations.md:76,115  'read body 37:57' (not the render's --range)
```

## Target end-state
- n33: the announce's live set is read from EVERY post session (the post session + `agi-master*` + the Prime's sessions, the same reader `rotate.py status` uses at :3802). A live post seated in another session is a receiver, and only a post absent from all of them is dropped.
- n129: the first-decision `cut` line (rotate.py:17624-17625) takes the dispatch path and `--level` from cells, and every post worktree path (:4222-4223, :17423, :22142-22143) derives from `paths.core.worktrees_root`. No `.agi/worktrees/post-` literal is left.
- n130: the bounded `harvest | cut | hold` prompt (:17600) is a template or config line, not an f-string in engine code.
- n139: `DEFAULT_CC_ROLES` (:118-135) carries no model literal. A role with no row reads the ladder roles cell or refuses by name.
- n76: the heal.py docstring (:892) and comments (:915, :1073) name the pinned mechanism: a RAISING `dump_record` propagates and only `OSError` is swallowed (test_heal_late_reap_bound.py). There is no "missing module" claim.
- n107: rotate.py has ONE `config:posts` parser (`_posts_load_error` and `_row_names` are gone, their callers on the one parser), and the 4 posts commit paths own no hash-object plumbing. `facts_body_ranges` parses the render's `--range`, and `config:rotations` (.geometry/rotations.md:76, :115, edited through `write.py`) uses it. The 3 tests pass with the `strict=True` xfail markers removed.

## Invariants
- A residue is closed by a reviewed round, never by a note.
- No test validates against the live `REPO/.agi` (the round rule quoted in n108; that test's live read is goal:g1.31.5.4.2's).
- Probes never call rotate, heal, send or dispatch functions against live panes. Tests run under `env -u TMUX -u TMUX_PANE`.

## Falsifier
1. From /data/work/agi (rc 1 at HEAD d4b7ead17, measured: all 5 grep conjuncts fail):
```bash
bash -c 'R=extensions/agi/bin/rotate.py; T=extensions/agi/tests
! git grep -qnE -- "--level small|bin/dispatch.py \{main\}|f\"\.agi/worktrees/post-|\"worktrees\" / f\"post-|prompt: harvest|\"model\": \"claude-" -- $R &&
! git grep -qnE "def (_row_names|_posts_load_error)" -- $R &&
! git grep -qn "RED until DG3" -- $T/test_rotate.py $T/test_rotate_templates.py &&
! grep -q "read body 37:57" .agi/nodes/.geometry/rotations.md &&
! git grep -qnE "a missing module stays loud|a broken serializer import does" -- extensions/agi/bin/heal.py &&
env -u TMUX -u TMUX_PANE python3 -m pytest $T/test_rotate.py -q -k "announce and other_session" --basetemp /tmp/g13153'
```
2. Negative: `git grep -nE '"model": "claude-|--level small' -- extensions/agi/bin/rotate.py` returns zero hits (4 at HEAD: :121 :128 :135 :17625).

## Out of scope
goal:g1.31.4.2.1 (harvest, copilot and status items upheld on rotate.py) · goal:g1.31.5.4.2 (n108: the same xfail test's live-checkout read) · goal:g1.31.5.1 · goal:g1.31.5.2 · goal:g1.31.5.4 · goal:g1.31.5.5 · goal:g1.31.1-.4 · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-5**.
n107 and n108 touch the same test (`test_w3c_...`, test_rotate_templates.py:1426). Land n108's fix (fixture instead of the live file) in the same round or first, so there is one writer per test.
