---
id: experiment:a00-55d14104-a06d58
mint_id: aab80ba728c446669f1713084db7b622
type: experiment
parents:
  - hypothesis:sensei-wake-audit-subcommand
next_edges: []
confidence: 0.8
edited_by: a00-5580112e
evidence_runs:
  - experiment:a00-55d14104-a06d58
loop: hypothesis:sensei-wake-audit-subcommand@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 4826f47fc17ec281
season: 2
title: A00 55d14104 a06d58
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-55d14104-a06d58

## Experiment

BUILD ORDER (hypothesis:sensei-wake-audit-subcommand is a g15 build order, not
a measurement — hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement).
I implemented `sensei.py wake-audit` and its tests, then ran it on a real
transcript and compared against the hand classification the hypothesis names.

### What was built (FILE SCOPE: extensions/agi/bin/sensei.py + tests only)

Added to `extensions/agi/bin/sensei.py`:

    sensei.py wake-audit --seat <seat> --gen <n> [--transcript PATH]

- **Transcript resolution reuses `rotate.resolve_transcript`** — `--transcript`
  explicit wins; otherwise the seat's `.meter` pin / CC-slug rules. Imported
  lazily with the same `from . import` / plain-import fallback the file already
  uses for `locations`/`node_writer`/`send`, so it loads under both the package
  and the bare-script/test import.
- **Live config read, never hardcoded**: `config:rotations` is located via
  `node_writer.find_node_file(root, "config:rotations")` (the `.geometry`
  address) and its `templates.<role>.startup.first_turn` list is parsed fresh
  every run by a dedicated line parser (`_extract_first_turn`). The seat's role
  comes from `config:seats` via the existing `sensei.load_seats`. If no
  template exists for that role it prints a named error and exits 2 — it never
  falls back to another role's template.
- **Four-category classifier** (`classify_call`, pure and unit-tested):
  (a) re-runs a first_turn `cmd` (label matched, `{seat}`/`{...}` placeholders
  bound to one token, piped `| head -N` display tails drained) → re-derives a
  first_turn output; (b) hand read/action a template entry could pre-run —
  ps/tmux process checks, listing sessions/rotations, reading records, the
  ListAgents join, `rotate.py ack` / `meter --pin` (after_join actions the
  service already performs), grepping the seat-registry config node; (c)
  protocol learning — `-h`/`--help` or grep/sed over a SOURCE file (.py/.sh/
  .log) or an engine script; (d) everything else = real work.
- **Window**: from the first assistant `tool_use` to (and cutting at) the first
  category-d call; d itself is the cut call, only a/b/c span the wake window.

New tests in `extensions/agi/tests/test_sensei_wake_audit.py` exercise the
classifier and the end-to-end `wake_audit` on a SYNTHETIC CC JSONL fixture with
a synthetic `config:seats` + `config:rotations` + transcript (a first_turn rerun
→ a, a by-hand read → b, a `-h` → c, real work → d), asserting the window cut
and the per-category counts. 22 tests pass
(`python3 -m pytest extensions/agi/tests/test_sensei_wake_audit.py
extensions/agi/tests/test_sensei.py -q`).

### Real-transcript run (evidence 2)

Command:

    python3 extensions/agi/bin/sensei.py wake-audit --seat sanctuary-director \
      --gen 14 --transcript \
      /home/ubuntu/.claude/projects/-home-ubuntu-work-agi--agi-worktrees-seat-sanctuary-director/914d302a-b33f-4c5f-b78d-a8b7320df6c5.jsonl

(the live sanctuary-director gen-XIV transcript). Real output:

    sensei.py wake-audit --seat sanctuary-director --gen 14 (role director)
    window: first assistant tool_use -> first real work (11 calls scanned, cut at the first category d)
    counts: a=0 b=7 c=3 d=1
      (d counts the cut call itself; only a/b/c span the wake window)
       1 [b] ListAgents: {}
       2 [c] Bash: {"command": "grep -o '\"name\": \"sanctuary-director\"[^}]*' .agi/nodes/.geometry/seats.md; echo \"---\"; ls -…
       3 [b] Bash: {"command": "python3 extensions/agi/bin/rotate.py ack --seat sanctuary-director --gen 14 --ref 7aeee9 continue…
       4 [b] Bash: {"command": "n=0; until [ $n -ge 8 ]; do r=$(ls -t /home/ubuntu/work/agi/.agi/sessions/rotations/sanctuary-dir…
       5 [b] Bash: {"command": "ps -o pid,ppid,etimes,stat,comm -p 2151405,2151413,2151417 2>/dev/null; echo \"---\"; tmux list-p…
       6 [b] Bash: {"command": "tmux list-windows -a -F '#{session_name} #{window_id} #{window_name} #{window_panes} #{window_act…
       7 [b] Bash: {"command": "ls -la /home/ubuntu/.claude/projects/-home-ubuntu-work-agi--agi-worktrees-seat-sanctuary-director…
       8 [c] Bash: {"command": "python3 extensions/agi/bin/send.py -h 2>&1 | head -40", "description": "Show send.py usage"}
       9 [c] Bash: {"command": "python3 extensions/agi/bin/send.py send -h 2>&1 | head -30; echo \"--- how did XIII address IX (g…
      10 [b] ToolSearch: {"max_results": 1, "query": "select:SendMessage"}
      11 [d] SendMessage: {"content": "sanctuary-director rotated XIII\u2192XIV: new address …

The window cut at 11 calls — reproducing exactly the "11 wake calls" count the
`config:rotations` `## facts` section records for gen XIV ("66 calls in 12 min,
11 wake + 55 harvest"). A second real run against belam (prime_director role,
its live b7205ab1 transcript) also parsed cleanly: 2 calls, cut at the first
real work (`wc -c HANDOFF.md && sed -n 1,140p HANDOFF.md`).

### FALSIFIER (evidence 3, and its honest limit)

The hypothesis names a hand classification ("belam gen IX, hand-classified by
the seat"); the actual hand data in the repo lives in `config:rotations`: the
Prime's Agent Notes on the gen-X wake (first 16 calls, prose) and the `## facts`
F1–F5 (call groups measured on gen XIV). **No exact call-by-call a/b/c/d table
for any single transcript is available.** Cross-checking against it:

- **PARTIAL AGREEMENT (strong signal):** my subcommand's 11-call wake window on
  the real gen-XIV transcript equals the `## facts` "11 wake calls" count for
  that same generation, and the split is overwhelmingly category-b by-hand
  reads (7 of 10 wake-span calls) — exactly the class of waste the owner's
  order ("too many calls, fold it into the rotation") is about.
- **DISAGREEMENT RECORDED:** the gen-XIV transcript I ran on has 151 assistant
  tool_use total, but `## facts` measures gen XIV at 66 calls — the facts were
  measured on a *different* gen-XIV session than the one currently live, so the
  F1–F5 call groups (calls 2,4–7 as `rotate.py status --record`, calls
  22–23/26–30) do not appear at those indices in my transcript and cannot be
  compared index-for-index. I did NOT claim those comparisons passed.
- **No independent clean hand table existed**, so the falsifier technically
  could not run call-by-call. That is a real limit on the evidence, stated
  plainly rather than papered over.

Verdict logic per the build-order rule: the subcommand is implemented and its
tests are green (22 passed), and it runs on real transcripts, and its gen-XIV
wake window reproduces the hand-measured wake-call count — but the named
call-by-call falsifier (hand table vs subcommand on one transcript) could not
be run because no such table exists in this tree. This is the
`inconclusive_lean_proved` condition the directive names ("implemented and
tested but the falsifier could not be run").

## Evidence

- `python3 -m pytest extensions/agi/tests/test_sensei_wake_audit.py
  extensions/agi/tests/test_sensei.py -q` → **22 passed**.
- Real-transcript run output (above): 11-call window, counts a=0 b=7 c=3 d=1.
- The classifier reads `config:rotations` from the LIVE node each run
  (`node_writer.find_node_file(root, "config:rotations")` → `.geometry/rotations.md`)
  and the seat role from `config:seats` via `sensei.load_seats` — an edit to
  the rotations node changes the classification on the next run, demonstrated
  indirectly by the synthetic-fixture tests and by the live run resolving the
  real director template fresh.

## Agent Notes
Implemented sensei.py wake-audit --seat --gen [--transcript]; reuses rotate.resolve_transcript; reads config:rotations fresh via node_writer, role from config:seats; 4-category classifier; 22 tests pass; real gen-XIV run cut an 11-call window reproducing the measured '11 wake calls' count; named call-by-call falsifier unavailable so lean_proved.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW L4.225 (parent a00-5580112e). INSTRUCTION: "THIS KID MUST IMPLEMENT THE FIX... a g15 claim is behaviour to build, not a hypothesis to measure" and the kid brief I sent: "Verdict: proved only with the real-transcript run AND the test run as evidence... If the subcommand is implemented and tested but the falsifier could not be run, use inconclusive_lean_proved:80".
WHAT I VERIFIED, BY RUNNING: (a) implementation exists at sensei.py:243-536 (wake_audit at :450, classify_call at :395, _extract_first_turn at :283, cmd_wake_audit at :506, subparser at :657); (b) python3 -m pytest extensions/agi/tests/test_sensei_wake_audit.py extensions/agi/tests/test_sensei.py -q -> 22 passed; (c) I re-ran the cited real command myself, sensei.py wake-audit --seat sanctuary-director --gen 14 --transcript <live gen-XIV jsonl>, and reproduced window=11 calls, counts a=0 b=7 c=3 d=1 with the per-call list.
NEAR MISS: a kid that adds a wake-audit subcommand with the four categories HARDCODED, or the first_turn list embedded as a literal, satisfies "the subcommand exists" and loses the load-bearing property the owner ordered -- that classification follows the LIVE rotation template. Verified it does not: _read_rotations (:266) resolves config:rotations through node_writer.find_node_file each run and _extract_first_turn parses templates.<role>.startup.first_turn fresh; an absent role template refuses at :476-481 rather than silently falling back to another role.
NEAR MISS 2: category d is the cut call, so a naive scan that excluded d from the window would report zero real work and an unbounded window; :496-503 appends d then breaks.
FALSIFIER LIMIT ACCEPTED: the named call-by-call hand table for belam gen IX does not exist in the tree (grep .agi/nodes: only the proposal prose and the F1-F5 aggregate groups, which are measured on a different gen-XIV session than the live one). The kid recorded the disagreement rather than claiming a pass. That is the honest :80 the brief prescribed, not a demotion.
DEVIATION: none. One kid, file scope respected (sensei.py + a new test file), no git run.
ROUND DISPOSITION: build order met; verdict stands at inconclusive_lean_proved:80.
<!-- THOUGHT:END -->
