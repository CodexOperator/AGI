---
id: doc:card-all-is-one
mint_id: f3ab702d3c454a6aab2d41c2e88533d2
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: all-is-one
scaffold_hash: 15b137cded6cbf1b
season: 2
title: Card all is one
town: core
---
# doc:card-all-is-one — all-is-one's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (23:00Z 09-29 — STOPPED on belam's relay of the owner's stop; IDLE)
| | |
|---|---|
| post | all-is-one |
| stage | council — you embody vision:all-is-one ONLY (read it whole first); every review speaks from that vision alone, never alive or self-perpetuating |
| protocol | doc:council-loop (read it first) · goal:g7.16.1 (the owner's words) |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high · gen 2 (re-seated 17:33Z crash-recovery respawn), CC session agi-86 / 081012 |
| peers | session names change per run: ListAgents / posts row session_ref first (alive was agi-13 this run) |
| skills | agi-node-write · agi-send · agi-workflow · agi-rotate · agi-post |

## §1 Plan
```
done   bundle 1 (g7.16.1.1) + bundle 2 (g7.16.1.2): converged, SM clean, council mur + lens reviews sent (see git history of this node)
done   17:3xZ row G couplings sent: closeout --check gate · --from-doc unlink · node_writer goal-type reason
done   18:1xZ write/render split = bundle 4 (g4.18.5 -> .6 -> .7), not folded into 3; conditions: read-via-render lives in g4.18.7 only · g4.19 resolved in row 0 · g4.18.3 gate invariant carried into g4.18.5 · `read` leaves VERBS in the same row as the 23-file repoint
done   18:2xZ row R (g6.41.1 recovery) into bundle 3 after H4g: one launcher (tmux ensure in _launch_window, scope in _shell_cmd) · leaf Out-of-scope/assignee fix · R falsifier = cgls negative + one-post kill · P5 via memory_alarm.read_psi
done   18:3xZ row G -> bundle 4 as W-G (verified unbuilt at 9966e3050); now LANDED per CLAUDE.md (goal:g7.16.1.4.1, GOALS.md retired)
done   18:4xZ bundle-3 lens review (9181cee26^..9966e3050) to alive: BETTER; 8 test files 367 passed / 6 skipped
         owed before close: C1 write.py:2376 unpark GrepError exits 0 (fail closed) · C2 _cutover_plan/_cutover_to_scopes 0 callers -> "built, not wired" in g6.41.1 body · C3 ensure_tmux_session = 3rd systemd-run builder, no usable-check
         bundle-4 inputs: B1 heal._launch_recovered copies _launch_window · B2 4 config:posts commit paths in rotate.py -> g4.18.5 one row write · B3 grep_live/parked_carriers homed in rotation_record · B4 heal's own config.json reader
open   no reply seen from alive on C1-C3 placement or the council mur (mur-data-work-agi-council-bundle-3) before the stop
```
Lens questions for every bundle: two paths for one act? · a role-only verb or flag? · a copy of a rule (one source)? · an overbuilt branch?

## 🔴 Where it stops
23:00Z 09-29 stopped idle on the owner's stop; bundle-3 lens review sent, C1-C3 placement unanswered
```
on resume: python3 extensions/agi/bin/send.py --from all-is-one read all-is-one ; tail the room .agi/comms/season-2/room/council-loop.md
then check C1-C3 in the bytes at the bundle-3 close tip: git show <tip>:extensions/agi/bin/write.py | sed -n 2370,2385p (unpark failure must not exit 0)
bundle 4 is live (DG3 residue 96 at 389afc3e1): lens review its range against B1-B4 when SM returns it clean
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN <sha> -- <paths>` |
| `send.py read all-is-one` without `--from` | exits 2 (whoami = unknown): always `send.py --from all-is-one ...` |
| town:local-maxxing board | ring-gated (owner/prime only): the measure line goes to room council-loop as [measure] |
| tests | `git archive <tip> extensions .agi/context/schemas` under /tmp (schemas too: formation_readback copies them), `--basetemp` under /tmp; check `.agi/sessions/verify-suite.lock` first |
| write.py `sub` | a `\n` in a single-quoted script lands LITERAL: build the arg with python3 -c print(...) |
| ack refused "own row dirty" | another post's ack is mid-write in posts.md: wait for it to commit, never touch its row |
| .agi/sessions/quorum/all-is-one.md | a STALE tracked regular file (09-18 brief), not a link to this node — do not read it as the card; not mine to re-point |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken (GOALS.md render check retired, goal:g7.16.1.4.1)

## §6 BANKED
(none)
