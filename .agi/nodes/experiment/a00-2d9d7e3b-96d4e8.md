---
id: experiment:a00-2d9d7e3b-96d4e8
mint_id: 68c743946b354e4389a0fe52a300c059
type: experiment
parents:
  - hypothesis:heal-lands-a-reseat-after-a-tmux-server-restart
next_edges: []
confidence: 0.8
edited_by: a00-2d9d7e3b
evidence_runs:
  - experiment:a00-2d9d7e3b-96d4e8
loop: hypothesis:heal-lands-a-reseat-after-a-tmux-server-restart@s2
model: stealth/space-bunny-alpha
production_lines: 26
profile: balanced
role: kid
scaffold_hash: 5161a567bc39ebba
season: 2
title: "both conjuncts of the reseat claim land on one tree: the launch file where tmux is called, the card from the seat own geometry"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-2d9d7e3b-96d4e8

## What: both conjuncts (a)+(b) of hypothesis:heal-lands-a-reseat-after-a-tmux-server-restart on ONE tree

Two accepted kids each fixed one conjunct on divergent branches off de9dced85.
Neither alone satisfies the claim. This lands both, taking (a) from branch B
(`experiment:a00-2d8528b1-92a0f7`) and (b) from branch A
(`experiment:a00-2843b444-f3a5f2`).

| conjunct | where | shape |
|---|---|---|
| (a) no inline prompt to tmux | `_launch_recovered` (heal.py) — where tmux is INVOKED, so every caller is covered | `tempfile.mkstemp` -> write shell line -> tmux gets `cd <tree> && sh <file>`; OSError -> `return 0, ""` (refuse loudly, tmux never called) |
| (b) card resolves in its own tree | `_recover_seat` (heal.py) | `card = _seat_geometry_dir(root, row) / "sessions" / "quorum" / f"{seat}.md"` (was `_rotate._sessions_dir(root)/quorum/`) |

Branch A's (a) is REJECTED and not carried: it wrote a second launch file in
`_recover_seat` and fell back to the 81859-char inline prompt on OSError while
recording `respawned=True` — the `command too long` bug wearing a success
record. ONE launch file, ONE place.

**The /tmp leak (the free ~4 lines).** The launch file deletes ITSELF:
`rm -f "$0" 2>/dev/null || true` is the last line of the file. The obvious
alternative — `os.unlink` after the tmux call returns — is a RACE, not free:
tmux forks the pane and returns the window id before the pane's `sh` has even
`exec`ed, let alone opened the script, so unlinking here can win and leave the
successor with a script that does not exist. `$0` inside `sh <file>` is the
script path, and an unlinked-but-open file stays valid, so the self-delete is
safe at any point the shell reaches it. If the recovered command `exec`s a
long-running agent the file lives exactly as long as that seat.

## Evidence — three tests, all on the built bytes

`extensions/agi/tests/test_rotate_recover.py` (3 new):

1. `test_launch_recovered_never_hands_tmux_the_prompt_inline` — a 100 000-char
   shell line: every argv element < 4096, no prompt bytes in the argv, the
   launch file carries the whole line verbatim, it RUNS under `sh` (rc 0,
   stdout `start…`) and is GONE afterwards. (the branch-B chain probe, plus the
   cleanup assertion)
2. `test_launch_recovered_refuses_loudly_when_no_launch_file` — `mkstemp`
   raising `OSError(28)`: `_launch_recovered` returns `(0, "")` and
   `subprocess.run` is NEVER called. Branch A fails this one.
3. `test_worktree_seat_card_resolves_in_its_own_worktree` — MAIN + linked
   worktree, each with its own `sessions/quorum/wt.md` (`GEN-OLD-main` vs
   `GEN-NEW-worktree`): the recorded launch command carries GEN-NEW-worktree
   and not GEN-OLD-main.

```
python3 -m pytest extensions/agi/tests/test_rotate_recover.py -q     -> 26 passed
python3 -m pytest extensions/agi/tests/test_heal_watch.py extensions/agi/tests/test_heal_seats.py -q -> 90 passed
python3 -m pytest extensions/agi/tests/test_heal.py -q                -> 18 passed
python3 -m pytest extensions/agi/tests/test_heal_sweep.py extensions/agi/tests/test_heal_ack_rotation.py \
    extensions/agi/tests/test_heal_late_reap_bound.py extensions/agi/tests/test_heal_pin_reap.py -q -> 63 passed
```

`git diff --numstat extensions/agi/bin/heal.py` -> 26 added / 2 removed
production lines (ceiling 40).

## Not done here
Conjuncts (c) (liveness never by @id alone) and (d) (every local row carries
`box`) are other kids' conjuncts, untouched.

## Caveat
The self-delete appends a line to a generated shell line. Safe for any
well-formed one (a trailing `\` continuation or an unterminated heredoc would
swallow it) — `spawn_window`'s dry-run output is a plain command, and a
swallowed line would have to survive a real 100k-char prompt to show up.

## Agent Notes
Merged both conjuncts on one tree: (a) launch file written in _launch_recovered (tmux gets 'sh <file>', OSError refuses loudly, file self-deletes via $0), (b) _recover_seat reads the card from _seat_geometry_dir; 26 production lines, 3 new tests, 197 heal tests pass.
