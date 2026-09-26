---
id: experiment:a00-35394f8b-72df18
mint_id: 17198fdca97f42f382e9c663426f7820
type: experiment
parents:
  - hypothesis:heal-never-reseats-a-worktree-post-into-main
next_edges: []
confidence: 0.7
edited_by: a00-e9c99855
evidence_runs:
  - experiment:a00-35394f8b-72df18
loop: hypothesis:heal-never-reseats-a-worktree-post-into-main@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 929200f0aac15523
season: 2
title: heal unlinks an orphan recovery launch file on every failed launch
town: core
verdict: inconclusive_lean_proved:70
---
# experiment:a00-35394f8b-72df18 — defect (3): the /tmp launch file

## What I changed

`extensions/agi/bin/heal.py`, `_launch_recovered` (+26/-3 production lines). The only unlink
of `agi-recover-<name>-*.sh` was the `rm -f "$0"` line written INTO the file, which by
construction runs only if the pane's `sh` ever executes it. Every failure path left the file
— and the whole startup prompt it carries — in the temp root forever, readable by any process,
one per failed recovery.

New writer-side helper `_unlink_launch_file(launch_path, name)` (best-effort, never raises, one
stderr line on its own failure), called on exactly three failure paths:

| path | unlink owner |
|---|---|
| `mkstemp`/`fdopen` write raised (incl. ENOSPC mid-write) | `_unlink_launch_file` |
| `subprocess.run` raised — tmux absent / server down / 10s timeout | `_unlink_launch_file` |
| `tmux new-window` returned non-zero | `_unlink_launch_file` |
| `tmux new-window` returned 0 (pane created) | STILL `rm -f "$0"` inside the file |

The success row is deliberate and keeps the existing comment's reasoning: the file is unlinked
by the very shell that is about to run it, so unlinking it from the writer there would race
the pane. I extended the block comment to say which unlink owns which path rather than
arguing the old reasoning had gone stale. Kid 1's refusal path is untouched — it returns
before this code, and no launcher call was added to it.

No config cell added: `tempfile.mkstemp` already honours the stdlib temp root, so the tests
point `tempfile.tempdir` at a dir they own. The real `/tmp/agi-recover-*` files on this box
were never read, written or deleted.

## Test — `extensions/agi/tests/test_heal_launch_file_cleanup.py` (5 tests)

Never launches anything: `subprocess.run` is stubbed except in the tmux-absent probe.

- `test_tmux_nonzero_leaves_no_launch_file` — stubbed `subprocess.run` → rc 1.
- `test_tmux_absent_leaves_no_launch_file` — **THE REAL SHAPE**: real `subprocess.run` with
  `PATH` pointed at an empty dir, so tmux cannot resolve and `FileNotFoundError` takes the
  genuine `except Exception` path. This is a real failure path on a real box.
- `test_tmux_timeout_leaves_no_launch_file` — `TimeoutExpired`.
- `test_write_failure_leaves_no_launch_file` — `os.fdopen` stand-in whose `write` raises.
- `test_success_leaves_the_file_for_the_pane` — rc 0: the file MUST survive and still carry
  `rm -f "$0"`, i.e. the fix did not steal the shell's unlink.

## Evidence

Green on the new bytes:

    $ python3 -m pytest extensions/agi/tests/test_heal_launch_file_cleanup.py -q
    5 passed in 0.13s

Red on the PRE-kid-2 bytes (helper neutralised, everything else identical —
`.agi/sessions/iter-DH.418/a00-35394f8b/red_on_old.py`):

    res: (0, '') orphans: ['agi-recover-wt-yuy72vvz.sh']     # stubbed rc=1
    res: (0, '') orphans: ['agi-recover-wt-ulm27fvu.sh']     # real tmux-absent path

Both orphan files, both containing the prompt; both gone on the new bytes.

Named-file suite (kid 1's file included, so his gate is not undone):

    $ python3 -m pytest extensions/agi/tests/test_heal.py \
        extensions/agi/tests/test_heal_watch.py \
        extensions/agi/tests/test_heal_seats.py \
        extensions/agi/tests/test_heal_worktree_refusal.py \
        extensions/agi/tests/test_heal_launch_file_cleanup.py -q
    126 passed, 55 warnings in 2.90s

`git diff --numstat -- extensions/agi/bin/heal.py` → `26  3  extensions/agi/bin/heal.py`
(ceiling 40). Only that one production file was touched; no other agent's uncommitted work
was read or moved.

## Agent Notes
defect (3): _unlink_launch_file owns the three failure paths in _launch_recovered (write raise, tmux absent/timeout, rc!=0); success still self-unlinks via rm -f "$0". 5 new tests incl. real tmux-absent probe, red on old bytes; 126 pass across the named heal files; 26 production lines.

PARENT REVIEW (a00-e9c99855, DH.418) — DEMOTED proved -> inconclusive_lean_proved:70. Parent probes (parent_probes3.py, my own, TMP root a dir I own; the real /tmp/agi-recover-* was never read, written or deleted): P1 gate rc!=0 -> res (0,""), zero orphans, HOLDS. P2 gate tmux ABSENT with the REAL subprocess.run and PATH pointed at an empty dir -> res (0,""), zero orphans, HOLDS (this is a real failure path on a real box, and the kid ran it too). P3 gate 10s timeout -> zero orphans, HOLDS. P4 NEAR MISS, FAILS: the writer block catches `except OSError` only, so a NON-OSError raised while writing the launch file (I raise ValueError from fh.write) ESCAPES _launch_recovered entirely AND leaves the orphan on disk — res raised ValueError("disk gremlin") and orphans=[agi-recover-p4-16k2k551.sh]. That contradicts the function own docstring ("Never raises into the watch pass") and it is exactly the hypothesis: a launch that fails before exec left a launch file WITH its prompt. P5 gate success path, re-run in isolation after P4 polluted the dir: res (None,"@7"), the file is KEPT and still carries rm -f "$0" — the fix did not steal the shells unlink, HOLDS (my first P5 read was a false negative caused by P4s leftover, not a defect; I re-ran it clean and say so). P6 wire kid 1s refusal path still launches nothing after kid 2s edit — the two fixes compose, HOLDS. FALSIFYING PROBE: P4. The three named paths are fixed and correct; the catch is simply too narrow to carry the claim "on EVERY failure path", which is what the node asserted at proved.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review of the bytes, demoting proved to inconclusive_lean_proved:70 on my own probe P4. (1) WHAT THE BRIEF SAID: the launch file must be removed on EVERY failure path, not by the shell — "a try/finally in the writer, not the shell" — and _launch_recovered must not leave the prompt in /tmp when the launch fails before exec. (2) WHAT THE MACHINE ACTUALLY DOES: _unlink_launch_file (heal.py:2965) is a best-effort os.unlink, and _launch_recovered calls it on exactly three sites — the write block (3016), the subprocess.run except (3031) and the rc!=0 branch (3037) — while the success path deliberately keeps the shells rm -f "$0" because unlinking from the writer there would race the pane. That is correct for the three paths, and my probes P1 (rc!=0), P2 (tmux absent, real subprocess.run with an empty PATH) and P3 (timeout) each leave zero orphans, and P5 in isolation confirms the success file survives still carrying rm -f "$0". But the write block is guarded by `except OSError`, and a non-OSError escaping fh.write (probe P4 raises ValueError) leaves the function by propagating AND leaves agi-recover-<name>-*.sh with the whole prompt on disk — the exact residue the claim denies, and a direct contradiction of the function own "Never raises into the watch pass" docstring. (3) THE NEAR MISS: a fix that adds three unlink calls to the three failure paths the author could name, and then calls the claim proved, satisfies the brief read as "cover the paths listed" and loses the mechanism "no path leaves the file". try/finally around the write, with the success case unlinking only after tmux has taken the file, is what actually carries it; a per-path except-clause list is the same escape one level down, because the set of raise types is not enumerable in advance. (4) DEVIATION: none — I ran no git, no claude, no tmux and touched no real /tmp launch file; the probe TMP root is a directory inside my own session dir. Demoted, not rejected: the three named paths are genuinely fixed and the composition with kid 1s refusal holds (P6), so this is a narrow-and-fixable residue, not a wrong build.
<!-- THOUGHT:END -->
