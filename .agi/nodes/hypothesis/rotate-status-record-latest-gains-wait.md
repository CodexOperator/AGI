---
id: hypothesis:rotate-status-record-latest-gains-wait
mint_id: 2f69cb63f1fb4d2cb7105279c7b9c2a2
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: master-sensei
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
