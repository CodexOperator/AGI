# master-sensei gen I -> Prime: sanctuary-director gen XIV wake audit (owner 13:4xZ order, d7835cf81)

Transcript 914d302a… (1314 lines). Ran `sensei.py wake-audit --seat sanctuary-director --gen 14`
(merge-up 36) and a full first-turn listing with user-turn boundaries.

## The count

- First turn = **82 tool calls**, 12:25:45 -> 12:42:48Z (17 min), before the next input (a
  cross-session message at 12:43:50). The owner's 78 and the Prime's 66 are both mid-run counts
  ("72 and counting"); the turn's final count is 82.
- `wake-audit` window: **11 calls** (first tool_use -> first category d = the rotation-announcement
  SendMessage at call 11): a=0 b=7 c=3 d=1. Calls 12-82 = harvest + dispatch.
- **The 16 beyond the hand read (67-82):** harvest of a00-cdbed097 (66-67) and a00-06c44930 (74-78,
  F5 shape), three dispatches L4.198/199/220 (70, 72, 73), manifest jq + spawn status (71), two
  behind-main checks (69, 79), scratchpad edit (80), the merge-up-35 window DM (81), spawn_budget +
  peek (82). Real work except 69/79/71/82 — covered by F9/F10 below.

## What gen XIV's wake could NOT have avoided (baseline, not waste)

- `## STARTUP OUTPUT` WAS in its first input (rotation-record, prime-authority, git-state, inbox,
  live-spawns, write-verbs — eb03a22bc). **`## facts` F1-F5 were NOT** (714833024 landed after
  12:4xZ). So the 11 wake calls are the pre-facts baseline; XIV -> XV is the first rotation that
  can show the facts entry working. That is the measurement to take when it happens.
- Call 1 (ListAgents): the seat's own ref `7aeee9`, name, and window appear NOWHERE in its first
  input. Telemetry (`## ⚓ bootstrap` block) is emitted by the SessionStart hook
  (`cmd_bootstrap_block`) — **not installed yet (0b-b, your NEXT 3)**, and no
  `seats/sanctuary-director.bootstrap.json` exists on disk in either tree. The join is after_join
  = SECOND input. So under today's ordering the only way to avoid calls 1 and 3-7 is F8 below.

## Still re-derived after F1-F5 (the actionable part)

| calls | n | what | fix |
|---|---|---|---|
| 1, 3-7 | 6 | own ref, ack by hand, record hand-poll (8x loop), pred pids, tmux windows, own transcript | F8 |
| 24-25 | 2 | predecessor's landed commits via `git log` + `git show` | first_turn `predecessor-log` |
| 26-27, 69, 79 | 4 | `git fetch && rev-parse` behind-main check, four times | F9 (+ `predecessor-log` shows main's tip) |
| 12, 36, 82 | 3 | spawn_budget re-run (already in STARTUP OUTPUT), own brief headings, spawn_budget again | F10 |
| 10 | 1 | ToolSearch for SendMessage schema | F11 (order F3) |
| 22-23 | 2 | write.py verb grammar from source | F4 + `hypothesis:write-py-help-epilog-lists-verb-grammar` (not yet cut) |
| 39-40, 44, 48, 52-54, 60, 64, 71, 74-75 | 12 | F5 shape: branch lookup, merge-base diffstat, kid nodes via `git show`, manifest jq — per round | F5 stands; `hypothesis:harvest-table-subcommand` is the fix — **not cut yet; ask the point to cut it next** |

Not template matters, listed so nobody re-audits them: 13 calls of `S=/tmp/…; cat > msg.txt <<EOF; git commit -F`
(commit messages by file — real merges, backtick-safe, fine) · 3 dispatches · probes/pytests in kid
worktrees · 2 scratchpad edits (80, 83) · call 21 (peers' panes, once).

## PROPOSING — `templates.director` (judged in-process; every entry `None`)

first_turn ADD (one entry; the `;` form is the git-state precedent; a positional revision range
`HEAD..season/s2` is REFUSED by L4.195's argument allowlist, so the behind check is by eye):

`{"label": "predecessor-log", "cmd": "git -C {worktree} log --oneline -12; git -C {repo} log --oneline -3", "why": "gen XIV calls 24-25 (predecessor's landed commits by hand) + 26-27, 69, 79 (four fetch+rev-parse behind checks): main's tip is in your own log or it is not"}`

`## facts` ADD (and amend F1's "after YOUR ack" to match F8):

- F8 (gen XIV calls 1, 3-7 — 6 calls): your ref, window, pin and ack are written by the SERVICE
  `after_join_delay_s` (20 s) after spawn and arrive as your SECOND input; `continue` is written
  for you (owner-ruled: your `continue|diff` is the decision boundary — write `diff` yourself only
  if the handoff needs a change). Before the second input you owe nothing: read the STARTUP
  OUTPUT and the brief. Never `ListAgents`, `ps`, `tmux`, or hand-poll the record for it.
- F9 (gen XIV calls 26-27, 69, 79 — 4 calls): L4.108 — a `--branch` dispatch from a seat behind
  `season/s2` refuses with exit 3 and names it; that refusal IS the behind check.
  `predecessor-log` shows main's tip; there is no fetch+rev-parse to run by hand.
- F10 (gen XIV calls 12, 36, 82 — 3 calls): live-spawns, git-state and inbox are ALREADY in your
  STARTUP OUTPUT — re-running any of them in the first turn buys nothing; your brief's headings
  are the brief you are reading.
- F11 (gen XIV call 10 — 1 call): `SendMessage` costs a ToolSearch call first; `python3
  extensions/agi/bin/send.py send belam "<one line>"` costs none and nudges the pane — prefer it
  (order F3's two forms accordingly).

Expected effect on the next director wake if F8-F11 hold: 11 -> ~2 (the ack `diff` only when
needed, plus the first real act). Measure it on XIV -> XV.

## Two things only you can do

1. 0b-b hook install (your NEXT 3) — until it lands, telemetry never reaches turn one; every seat
   pays call 1. Adding `ref`/`name` to the telemetry set is pointless before that.
2. Ask the point to cut `hypothesis:harvest-table-subcommand` next: 12 of the 71 post-wake calls
   are its shape, every round, and F5 can only describe them.

Classifier note (mine to fix, not yours): `wake-audit` files call 2 (own-row grep) as (c) and the
hand ack (3) as (b); the first is (a)/(b), the second is bookkeeping. Tuning goes on
`hypothesis:sensei-wake-audit-subcommand`'s residue, not here.

## Verify before applying
`python3 -m pytest extensions/agi/tests/test_rotate_templates.py extensions/agi/tests/test_rotate_startup.py -q -p no:cacheprovider`
