---
id: hypothesis:rotate-status-record-latest-gains-wait
mint_id: 2f69cb63f1fb4d2cb7105279c7b9c2a2
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 69456ae8e9944918
season: 2
testable_claim: "OWNER 2026-09-11 12:4xZ ('add to his rotation config'; '72 commands and counting'), master-sensei gen I proposal 2, grounded on two independent wakes: sanctuary-director gen XIV F1 ('ONE call proves it... never ps/tmux by hand') and belam gen IX calls 10-12 (18x hand-poll + sleep 20 on the SAME `status --record latest` line, the single biggest waste in that wake, measured this session by a forked read of b7205ab1-b47a-422d-80da-7da168eeebe1.jsonl). CLAIM: `rotate.py status --seat <seat> --record latest` (cmd_status, rotate.py:1547) prints the record + sequence + row exactly once and returns 0 regardless of whether the record's `s12_self_reap` section is still absent/non-terminal; a caller that needs the terminal result has no engine-provided way to wait for it and hand-rolls a sleep+reinvoke loop instead. Add `--wait N` (seconds, only meaningful with `--record latest`): re-read the record file at a short fixed interval (<=2s) until `s12_self_reap` is present, or N seconds elapse; print the same output as today on success, and on timeout print the last-seen record plus `ERR: still not terminal after Ns` and exit 2. FALSIFIER: a `--wait N` call that either sleeps past a record already terminal on its first read, or returns 0 without `s12_self_reap` present after N seconds elapse. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/rotate.py (cmd_status + its argparse wiring only) + its tests in extensions/agi/tests/test_rotate*.py."
thought_session: master-sensei-gen1
title: rotate.py status --record latest gains a --wait flag instead of a hand-poll loop
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:rotate-status-record-latest-gains-wait

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
DIRECTOR HARVEST L4.233 (sanctuary-director gen XV, 2026-09-11 13:58Z). Parent a00-56f534f7 accepted the kid's proved (0.9). Landed on the seat as a merge of `loop/hypothesis-rotate-status-record--a00-56f534f7@s2`: rotate.py (+52: `_record_is_terminal`, `_poll_record_terminal`, the `--wait` branch in `cmd_status`, the argparse flag), test_rotate_templates.py (+102, 3 tests), the kid's experiment node. Read the bytes: the poll fixes `latest = files[-1]` once and re-reads THAT file, so a newer record appearing mid-wait is not followed — the intended "same record" semantics, worth knowing. Ran with neighbours from the seat: `pytest test_rotate_templates.py test_rotate_startup.py test_rotate_selfreap.py test_rotate_complete.py -q` -> 91 passed in 40.9s. Real-tree probe: `rotate.py status --seat sanctuary-director --record latest --wait 1` on the live latest record (gen XIV's `success`, `s12_self_reap` present) -> rc=0 in 0.18s, empty stderr; `_poll_record_terminal(<live latest>, 30)` -> terminal=True in 0.00s. Counterfactual: a copy of that record with `s12_self_reap` deleted (jq) under a scratch root -> `_poll_record_terminal(copy, 1)` = terminal=False at 1.00s, and `cmd_status(Namespace(record='latest', wait=1), <scratch root>)` -> rc=2 at 1.00s with the last-seen record on stdout. Observation, not a defect of this round: the parent's `done:` commit subject says `verdict=pending` while the node it commits carries `verdict: proved` (same on L4.231's `aadd60b99`) — the subject is minted before the review's verdict lands; a candidate one-liner for the prime, not a round.
