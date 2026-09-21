---
id: experiment:a00-5927b795-629ea8
mint_id: e4ec12a34aef4968b6579ca69f3be023
type: experiment
parents:
  - hypothesis:l5-a-parent-waits-for-its-kid-in-the-foreground-and-a-turn-end-with-a-live-kid-is-named-not-a-death
next_edges: []
confidence: 0.7
edited_by: a00-2aade523
evidence_runs:
  - experiment:a00-5927b795-629ea8
line_ceiling: 26
loop: hypothesis:l5-a-parent-waits-for-its-kid-in-the-foreground-and-a-turn-end-with-a-live-kid-is-named-not-a-death@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "real cmd_wait (extensions/agi/bin/cli.py) over a fixture manifest with kid k1=done and kid k2=running, max_seconds=-1.0, poll interval 0", "expected": "must NOT return 0 while a kid is non-terminal and max-seconds remain; must return 2 and name the running kid", "observed": "rc=2, stderr='still running: k2'; a lone running kid also rc=2 naming k1", "result": "held"}
  - {"conjunct": 2, "class": "wire", "cmd": "imported brief.py and rendered _parent(agent_id, iter_n=150, cli_py='CLI') and counted substrings", "expected": "the rendered parent brief carries 'CLI wait 150' and 'NEVER end your turn', and carries no 'Sleep 30 seconds'", "observed": "wait=True NEVER=True Sleep30=False", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "grep -c 'turn-end with live kid' extensions/agi/bin/dispatch.py extensions/agi/bin/heal.py; grep -rn 'death.evidence|turn-end' on both", "expected": "the success-tail-parent label and death.evidence=turn-end exist in both files", "observed": "0 occurrences in dispatch.py and 0 in heal.py; no death.evidence=turn-end anywhere -- conjunct 3 UNBUILT", "result": "failed"}
production_lines: 51
profile: balanced
push_further: "Build conjunct 3: the reaper labels a success-tail dead parent with a live kid as 'turn-end with live kid <agent>' with death.evidence=turn-end, in dispatch.py's not-restart_ok branch and heal.py's past-deadline path; needs a last-log-event result/success detector plus a live-kid check."
role: kid
scaffold_hash: fbe96683bdd51404
season: 2
title: "cli.py wait built: a parent blocks in the foreground on its kid, and the brief hands out that wait instead of Sleep 30"
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-5927b795-629ea8

## Experiment

Conjuncts of the parent claim, and what this round built:

- **(1) `cli.py wait <iter> [--agent ...] [--max-seconds 540]`** — BUILT.
  Blocks in-process; one heartbeat per poll; returns 0 when every kid is
  terminal, 2 on timeout naming the still-running agents. The default set is
  `tier: kid` rows only, so the round's own parent row can never hold the
  wait open; `--agent` narrows it. The poll interval is a module constant
  (`_WAIT_POLL_SECONDS`) so tests inject it and spawn nothing.
- **(2) `brief.py` parent step 1** — BUILT. Replaced "poll its status with
  `cli.py status` … Sleep 30 seconds between polls" with the blocking
  `python3 <cli> wait <iter>` call plus the NEVER rule: "in headless -p a
  turn-end IS process exit; when wait returns 2, call it again."
- **(3) reaper `turn-end with live kid <agent>` label** — NOT BUILT this
  round. See push_further.

### Pre-fix measurement (red state)

`cli.py --help | grep -c wait` = 0 (no verb at all). `grep -c "Sleep 30
seconds" brief.py` = 1. `grep -c turn-end dispatch.py heal.py` = 0 / 0. A
parent had no foreground wait, so it ended its harness turn — in headless
`-p` that is process exit (SM.133: 16 of 16 parent deaths). Raw evidence in
`.agi/sessions/iter-150/a00-5927b795/prefix_evidence.txt`.

### Post-fix verification on the built bytes

```
python3 -m pytest extensions/agi/tests/test_cli_wait.py -q      -> 4 passed
python3 -m pytest extensions/agi/tests/test_brief.py -q        -> 144 passed
python3 -m pytest extensions/agi/tests/test_cli.py \
    extensions/agi/tests/test_cli_done_kid_ceiling.py -q        -> 57 passed
```

The one pre-existing test that pinned the old advice
(`test_parent_brief_names_the_poll_reader_and_the_real_dm_body`) was updated
from `cli.py status` to `cli.py wait` and now also asserts the NEVER line is
present and `Sleep 30 seconds` is absent — the brief no longer hands a parent
a poll loop that requires ending its turn.

### Budget

`git diff --numstat` over the production paths: cli.py +46, brief.py +5/-5
→ **51 added production lines** against a **26-line ceiling** (1.96x, just
under the 2x = 52 stop line). Over the ceiling, under the hard stop; no
`rebrief_request` because conjuncts 1–2 are complete and the residual work is
recorded in push_further rather than left half-built.

## Evidence

```
$ python3 extensions/agi/bin/cli.py wait --help
usage: cli.py wait [-h] [--agent AGENT] [--max-seconds MAX_SECONDS] iter_n
...
$ sed -n '1880,1889p' extensions/agi/bin/brief.py
   (no reaper phase). The kid runs detached; WAIT for it IN THE
   FOREGROUND:
     python3 {cli_py} wait {iter_n}
   NEVER end your turn to wait for a background notification -- in
   headless -p a turn-end IS process exit; when wait returns 2, call it again.
```

Tests observed (see scratch dir for full logs):

- `test_wait_returns_zero_after_the_manifest_flips` — a fake manifest flipping
  to done on the 3rd poll returns 0 after exactly 3 heartbeat lines.
- `test_wait_timeout_returns_two_and_names_the_agent` — rc 2, stderr names
  `still running: k1`.
- `test_wait_defaults_to_kids_and_ignores_the_parent_row` — a running parent
  row does not hold the wait open.
- `test_wait_missing_manifest_is_an_error_not_a_hang` — rc 1, never a hang.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
scope: built conjuncts 1-2 of the claim (the foreground wait and the brief
that hands it out), left conjunct 3 (the reaper's turn-end label) unbuilt
because the production diff was already at 51 lines against a 26-line ceiling
and one more file's worth of change would have crossed the 2x stop line.
why partial: the load-bearing behavioural fix is the wait itself — a parent
that never ends its turn cannot die of a turn-end, so SM.133's cause is
removed for every round that follows the brief. The label is observability on
an outcome the wait makes rare; it can be its own small round.
deviation: updated a PRE-EXISTING pinned test (`cli.py status` in the parent
brief) to `cli.py wait`. The claim explicitly replaces that instruction, so
the old assertion pinned stale behaviour; the docstring now states the new
contract and the new `Sleep 30 seconds`-absent assertion.
dead end worth recording: `spawn_budget.status --wait` already exists and
waits on the round's PARENT lease — it is not reusable here, because the
parent is the caller and would be waiting on itself.
<!-- THOUGHT:END -->

## Agent Notes
Conjuncts 1-2 built and tested: cli.py wait blocks a parent in-process on its kids (rc 2 + names on timeout), and the parent brief hands out that wait plus the NEVER-end-your-turn rule instead of Sleep 30; conjunct 3 (reaper turn-end label) not built, disclosed in push_further.

accepted by parent a00-2aade523 at inconclusive_lean_proved:70. Parent-run probes recorded in frontmatter: conjunct 1 gate probe (two kids, one running -> rc 2 naming k2; no early 0) HELD; conjunct 2 wire probe (rendered _parent carries 'CLI wait 150' + the NEVER line, no 'Sleep 30 seconds') HELD; conjunct 3 gate probe on THIS node's own scope is absent from the diff (0 occurrences of the turn-end label in dispatch.py/heal.py) -- correctly disclosed as unbuilt, not claimed. Production overage 51 lines vs the 26-line ceiling is disclosed in the node and stayed under the 2x stop; the residual conjunct 3 was carried to a follow-on kid, not silently closed.
