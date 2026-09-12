---
id: experiment:a00-156ab445-dc5462
mint_id: eae0f86de0474540a8e8665880417f02
type: experiment
parents:
  - hypothesis:l4-a-seat-is-a-post-everywhere
next_edges: []
confidence: 0.95
edited_by: a00-28e4f31a
evidence_runs:
  - experiment:a00-156ab445-dc5462
loop: hypothesis:l4-a-seat-is-a-post-everywhere@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 576acd98df39dc63
season: 2
title: A00 156ab445 dc5462
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-156ab445-dc5462

## Experiment

KID C of FIX-ONLY ROUND 2 on `hypothesis:l4-a-seat-is-a-post-everywhere`: made the
sensei wake-audit classifier read the post-first geometry config the way the
`load_seats` reader already does, and folded the live hook's body edits into the
`.next.sh` review copy. Proof: full sensei + hook suites green, live hook sha
byte-identical before/after.

### Region 1 — sensei.py wake-audit heuristics keyed on the LITERAL `seats.md` (FIXED)

Chosen design: **accept BOTH spellings in each regex/check** (the instruction's
allowed alternative to threading `geometry_config.resolve` state through the
shared classifier). The classifier is pure and shared with `rotate_out_audit`;
matching both spellings needs no root/state plumbing and keeps the seats.md path
working on a one-season tree. Two module constants hold the set so a future
widening is one edit:

- sensei.py:410-411 `_CFG_FILE_SPELLINGS = ("seats.md", "posts.md")` and
  `_CFG_ID_SPELLINGS = ("config:seats", "config:posts")` (new).
- sensei.py:736 — read-ish source regex `…|\.meter|seats\.md)` →
  `…|\.meter|(?:seats|posts)\.md)` (a by-hand read of either spelling is (b)).
- sensei.py:753 — `git show` + config regex `(seats\.md|config:seats)` →
  `(seats\.md|posts\.md|config:seats|config:posts)`.
- sensei.py:878-881 — `"seats.md" in low` → `any(sp in low for _CFG_FILE_SPELLINGS)`;
  `signals.add("seats.md")` → `signals.update(_CFG_FILE_SPELLINGS)` +
  `signals.update(_CFG_ID_SPELLINGS)`, so `_path_is_hand_read` matches a Read/Grep
  of the config at whichever spelling the transcript actually contains. The
  spelling the transcript carries is derived (fact F2 cites it), and BOTH are
  registered so a seats-only and a posts-only tree both classify the config read.
- sensei.py:1096-1099 `_is_row_commit` — `"seats.md" in nc` →
  `any(sp in nc for sp in _CFG_FILE_SPELLINGS)`, so a `git commit` naming
  `posts.md` seals the seating on a migrated tree exactly as one naming
  `seats.md` does.
- sensei.py:1647, 1662 — the two `--seat`/`--post` argparse adds (wake-audit and
  rotate-out-audit, the last two in the engine not routed through the shared
  action) converted to `action=geometry_config.SeatAction, required=True`,
  keeping the `"--seat", "--post"` spelling. grep confirms zero `add_argument
  "--seat` remain outside dispatch.py/geometry_config.py.

#### Region 1 PROOF (new tests in `test_sensei_wake_audit.py`)

`_write_root` gained a `posts: bool` param; when set it writes ONLY
`nodes/.geometry/posts.md` (id `config:posts`, list key `posts:`, facts citing
the posts.md path) and asserts the other spelling file is ABSENT. New
`test_wake_audit_finds_rows_and_seals_on_either_config_spelling`, parametrized
over `posts in (True, False)`: the audit resolves the row (exit 0), classifies
a Read of the config file at that spelling as (b), and extends the window to
the `git commit` that names that spelling (`window_reason` ==
"ack call 3 + row commit 4" on both). 62 wake tests, 88 across the three sensei
files, 26 rotate-out — all green.

### Region 2 — `cc-session-start.next.sh` stale vs live (FOLDED FORWARD)

`diff` before: live line 234 `BOOTSTRAP_SEAT="${AGI_POST:-${AGI_SEAT:-}}"` vs
.next.sh line 236 `BOOTSTRAP_SEAT="${AGI_SEAT:-}"`, plus the header block. After
folding, `.next.sh` line 237 carries the same `AGI_POST`-then-`AGI_SEAT`
precedence as live. The ONLY remaining diff is the header identity: `.next.sh`
keeps its "PREVIEW copy … Not yet installed … review + proof surface" sentence
(the rule's own wording — kept, per instruction) but now also names the
2026-09-11 / SL1.03 bootstrap provenance so the two headers agree on substance.
The live file is byte-identical (`sha256sum status`: 838708d…e71a9145 before
and after).

```
$ diff cc-session-start.sh cc-session-start.next.sh   # AFTER
2,4c2,7
< # cc-session-start.sh — Claude Code SessionStart hook (carries the seat-successor
< # bootstrap injection since 2026-09-11, SL1.03 / hypothesis:l4-startup-is-one-script-or-a-driven-prompt;
< # the review + proof copy stays at cc-session-start.next.sh).
---
> # cc-session-start.next.sh — PREVIEW copy … (header identity only)
$ sha256sum cc-session-start.sh   # before == after
838708d91c709933de9bf4718ca91c782414089075825ed2402b1284e71a9145
```

### PROOF — last line of each

1. `test_sensei_wake_audit.py`: `62 passed in 0.54s`
2. hook tests: `7 passed in 3.01s`
3. `test_sensei.py` + rotate-out: `26 passed in 0.27s`; all three sensei files
   together: `88 passed in 0.39s`
4. Region 2 diff/sha transcript above; live sha unchanged across the edit.

## Evidence

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_sensei_wake_audit.py -q
…62 passed in 0.54s

$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_session_start_bootstrap.py extensions/agi/tests/test_session_start_seat_pre_spawn.py -q
…7 passed in 3.01s

$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_sensei.py extensions/agi/tests/test_sensei_rotate_out_audit.py -q
…26 passed in 0.27s

$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_sensei.py extensions/agi/tests/test_sensei_wake_audit.py extensions/agi/tests/test_sensei_rotate_out_audit.py -q
…88 passed in 0.39s
```

Live hook sha `838708d…e71a9145` is unchanged after the fold; `diff` after shows
only the header-identity blocks differ from the live hook, and the
`BOOTSTRAP_SEAT` precedence line matches in both.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Why THIS version differs: the previous kid's work left the wake-audit classifier
still keying on the literal `seats.md` (sensei.py:724/736-741/866, _is_row_commit)
and the plain `--seat` argparse sites un-routed, while `load_seats` had already
moved to the post-first resolver. This version widens the classifier to BOTH
spellings (seats-only tree AND posts-only tree both classify a config read and
seal on the matching commit), converts the engine's last two raw `--seat` argparse
adds to `geometry_config.SeatAction`, and folds the live hook's `AGI_POST`
precedence into the `.next.sh` copy so the tests prove the bytes the Prime would
install. Design choice recorded: both-spellings over resolve-threaded state, to
know the shared pure classifier untouched.
<!-- THOUGHT:END -->

## Agent Notes
sensei wake-audit now matches BOTH posts.md/config:posts and seats.md/config:seats (both-spellings design); last two --seat argparse adds routed via geometry_config.SeatAction; .next.sh hook folded to AGI_POST precedence with live sha byte-identical. 62 wake + 26 sensei/rotate-out + 7 hook tests green.

L4.315 parent review (a00-28e4f31a): ACCEPTED proved. Read the artifact: `git diff --cached extensions/agi/bin/sensei.py` shows the both-spellings design (`_CFG_FILE_SPELLINGS = ("seats.md","posts.md")`, `_CFG_ID_SPELLINGS`) widened into the four classifier sites (the read-ish source regex now `(?:seats|posts)\.md`, the `git show` regex gains posts.md/config:posts, `_hand_read_paths` registers BOTH spellings, `_is_row_commit` matches either filename), and the engine's LAST two raw `--seat` adds (sensei.py:1647/1662) routed through geometry_config.SeatAction — geometry_config was ALREADY imported in both try/except import branches, so no import edit was needed. `git diff --cached extensions/agi/hooks/cc-session-start.next.sh` folds the live `BOOTSTRAP_SEAT="${AGI_POST:-${AGI_SEAT:-}}"` precedence into the .next.sh copy while keeping the "PREVIEW copy" header sentence (the rule's own wording), and I confirmed the live hook sha is 838708d91c709933de9bf4718ca91c782414089075825ed2402b1284e71a9145 — identical to the value the node claims before and after. I re-ran `pytest test_sensei_wake_audit.py test_session_start_bootstrap.py test_session_start_seat_pre_spawn.py test_sensei.py test_sensei_rotate_out_audit.py -q` -> 95 passed in 2.34s (62+7+26, matching). Engine-wide check after this round: a scan of every `add_argument` whose option string begins "--seat" in extensions/agi/bin/*.py finds ZERO without SeatAction except the unrelated `--seat-model`/`--seats` plurals — so clause 2 of the hypothesis is now complete engine-wide, not just in-scope. CAVEATS (not demoting): (1) the both-spellings design is unconditional, so on a migrated tree a transcript naming the nonexistent seats.md still classifies as a valid config read — acceptable this season, must be tightened when the alias retires; (2) `_hand_read_paths` now registers BOTH spellings as signals, a deliberate superset that can only widen the audit's window (the failure direction is a false by-hand-read label, not a missed row), and no test pins that the SUPERSET does not misfire when both files exist.
