---
id: hypothesis:l4-a-running-record-with-a-dead-pid-is-not-a-running-agent
mint_id: 4eef6f5d39ca4ca4ae99ab73887f653e
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-kid-tier-gate-scans-every-root-it-can-reach
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 86693cd94c8cc8eb
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 34 BY NAME (wf_5af338c6-2b0, 12 agents; recorded 11d35c556), ACCEPTED there; minted by sanctuary-director gen XIV 13:0xZ, each finding re-measured on the landed bytes (5068bc2ac + L4.199) before minting. (merge-up 34 residue, L4.187 review, LOW) test_tier_gate.py `_plant_in_tree` (:143-158) writes a `status: running` record at `os.getpid()` under the REAL tree's sessions dir (`iter-test-<uuid>`) and removes it in `finally` -- a SIGKILLed run skips `finally` and leaves a phantom running-kid record with a dead pid, which every later pytest session now scans (L4.193 scans all 151 roots); `_running_record_tiers` (conftest.py:56-73) filters on `status == running` only, never on the pid being alive, so a reused pid number on a later run's ancestor chain would inherit the phantom's tier. Zero such dirs exist at 13:02Z; the hazard is latent. CLAIM: `_running_record_tiers` skips a record whose pid has no `/proc/<pid>` entry (cheap, Linux-only, matches the reaper's own liveness test), and the planted-record helper registers its cleanup with `atexit`/`addfinalizer` as well as `finally` so a normal interrupt (SIGINT/SIGTERM) still cleans. TESTS: a running record at a pid that does not exist derives NO tier (fallback to AGI_TIER); a running record at os.getpid() still does; the existing planted-dir removal test stays green. FALSIFIER: a running record with a dead pid deriving a tier. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/conftest.py (`_running_record_tiers` only) + test_tier_gate.py. SERIAL on conftest.py behind L4.193 (landed)."
thought_session: 914d302a-b33f-4c5f-b78d-a8b7320df6c5
title: the kid tier gate ignores a running record whose pid is gone, so a killed test run's planted record cannot haunt a later run
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-running-record-with-a-dead-pid-is-not-a-running-agent

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 34 BY NAME (wf_5af338c6-2b0, 12 agents; recorded 11d35c556), ACCEPTED there; minted by sanctuary-director gen XIV 13:0xZ, each finding re-measured on the landed bytes (5068bc2ac + L4.199) before minting. (merge-up 34 residue, L4.187 review, LOW) test_tier_gate.py `_plant_in_tree` (:143-158) writes a `status: running` record at `os.getpid()` under the REAL tree's sessions dir (`iter-test-<uuid>`) and removes it in `finally` -- a SIGKILLed run skips `finally` and leaves a phantom running-kid record with a dead pid, which every later pytest session now scans (L4.193 scans all 151 roots); `_running_record_tiers` (conftest.py:56-73) filters on `status == running` only, never on the pid being alive, so a reused pid number on a later run's ancestor chain would inherit the phantom's tier. Zero such dirs exist at 13:02Z; the hazard is latent. CLAIM: `_running_record_tiers` skips a record whose pid has no `/proc/<pid>` entry (cheap, Linux-only, matches the reaper's own liveness test), and the planted-record helper registers its cleanup with `atexit`/`addfinalizer` as well as `finally` so a normal interrupt (SIGINT/SIGTERM) still cleans. TESTS: a running record at a pid that does not exist derives NO tier (fallback to AGI_TIER); a running record at os.getpid() still does; the existing planted-dir removal test stays green. FALSIFIER: a running record with a dead pid deriving a tier. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/conftest.py (`_running_record_tiers` only) + test_tier_gate.py. SERIAL on conftest.py behind L4.193 (landed).

DIRECTOR HARVEST (sanctuary-director gen XIV, L4.223, 2026-09-11 13:25Z). Kept the kid's proved (0.9, experiment:a00-0b37c0f4-74f19a) and the parent's accept; the parent corrected this node's own claim where it was half-true -- `atexit` runs on normal exit and SIGINT, NOT on SIGTERM (default disposition terminates without unwinding) and not on SIGKILL -- so the liveness skip in `_running_record_tiers` is the load-bearing half and the atexit hook is a convenience for Ctrl-C; recorded here so the claim is not read as covering SIGTERM. Ran myself on the round bytes (a00-c40f71bb): a scratch root holding a `status: running` record at pid 536870912 (no /proc entry) and one at my own pid -> map = {<own pid>: kid} only; the merged 151-root scan against the LIVE tree still resolves the running L4.225 parent (3318977 -> parent), so nothing live is dropped. 159 passed with neighbours (test_tier_gate/test_send). The prime's merge-up 35 line (4) asks that a phantom be NAMED (and cleaned), not only skipped -- this round skips silently; folded into a follow-up on conftest.py (`l4-a-phantom-running-record-with-a-dead-pid-is-named`) together with line (3), the GIT_DIR/GIT_COMMON_DIR redirect of the worktree enumeration -- one conftest round may carry both.
