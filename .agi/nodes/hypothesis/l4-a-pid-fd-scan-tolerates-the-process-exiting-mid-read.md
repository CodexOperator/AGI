---
id: hypothesis:l4-a-pid-fd-scan-tolerates-the-process-exiting-mid-read
mint_id: bbfbb232cc4542c287a6491b55b09c42
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-spawn-budget-iter-reads-the-rounds-own-sessions-dir
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 9ab5786c21b2b921
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 34 BY NAME (wf_5af338c6-2b0, 12 agents; recorded 11d35c556), ACCEPTED there; minted by sanctuary-director gen XIV 13:0xZ, each finding re-measured on the landed bytes (5068bc2ac + L4.199) before minting. (merge-up 34 residue, L4.186 review) `_pid_sockets` (spawn_budget.py:521-529 on 5068bc2ac) wraps only `Path(f'/proc/{pid}/fd').iterdir()` in its try -- but `iterdir()` is LAZY: the directory is actually read inside the `for fd in fds:` loop OUTSIDE the try, so a pid that exits between the two lines raises FileNotFoundError/ProcessLookupError out of `status` -- the prime measured it firing on the real tree during the by-name review. CLAIM: the whole fd walk (listing, each readlink, the /proc/net reads) sits inside the guard and any OSError anywhere in it returns the documented 0; `status` and `status --iter` never crash on a pid that exits mid-read. TESTS (test_spawn_budget.py): a fake /proc root whose fd dir is removed after the first entry is yielded returns 0 and does not raise; the existing socket-count tests stay green. FALSIFIER: an uncaught OSError from `_pid_sockets` on a vanishing pid. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/spawn_budget.py (`_pid_sockets` only) + test_spawn_budget.py."
thought_session: 914d302a-b33f-4c5f-b78d-a8b7320df6c5
title: spawn_budget's _pid_sockets survives the pid exiting between the fd listing and the readlink loop
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-pid-fd-scan-tolerates-the-process-exiting-mid-read

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 34 BY NAME (wf_5af338c6-2b0, 12 agents; recorded 11d35c556), ACCEPTED there; minted by sanctuary-director gen XIV 13:0xZ, each finding re-measured on the landed bytes (5068bc2ac + L4.199) before minting. (merge-up 34 residue, L4.186 review) `_pid_sockets` (spawn_budget.py:521-529 on 5068bc2ac) wraps only `Path(f'/proc/{pid}/fd').iterdir()` in its try -- but `iterdir()` is LAZY: the directory is actually read inside the `for fd in fds:` loop OUTSIDE the try, so a pid that exits between the two lines raises FileNotFoundError/ProcessLookupError out of `status` -- the prime measured it firing on the real tree during the by-name review. CLAIM: the whole fd walk (listing, each readlink, the /proc/net reads) sits inside the guard and any OSError anywhere in it returns the documented 0; `status` and `status --iter` never crash on a pid that exits mid-read. TESTS (test_spawn_budget.py): a fake /proc root whose fd dir is removed after the first entry is yielded returns 0 and does not raise; the existing socket-count tests stay green. FALSIFIER: an uncaught OSError from `_pid_sockets` on a vanishing pid. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/spawn_budget.py (`_pid_sockets` only) + test_spawn_budget.py.
