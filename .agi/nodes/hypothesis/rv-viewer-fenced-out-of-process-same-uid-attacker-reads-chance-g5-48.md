---
id: hypothesis:rv-viewer-fenced-out-of-process-same-uid-attacker-reads-chance-g5-48
mint_id: 6738a2dd17fa47b9b4b0de492416ea8b
type: hypothesis
parents:
  - goal:g5.48
next_edges: []
edited_by: director-thought-science
season: 3
testable_claim: "With the viewer as its own process (fork + exec, close_fds, scrubbed env, public argv, pipes only) and the parent non-dumpable before its secret exists, a same-uid attacker viewer A* that tries the caller frame, a gc walk, /proc/PPID environ, cmdline, fd and mem, every file under the run and rv dirs, and its own env and argv scores inside chance (alpha 0.01) over all 200 trials, train and held-out; the null and salt viewers out of process reproduce chance and 200/200; the same A* in process scores >= 150 (M1), the fixed decoy draw has 0 run targets vs 74 earlier-trial targets on round 2's draw (M2), and A* reads /proc/PPID/mem when the parent is left dumpable (M3)."
title: "The remote-viewing viewer fenced out of process: a same-uid attacker A* reads chance, while the same A* in process or against a dumpable parent reads the secret (goal:g5.48, lap 5)"
town: local-maxxing
verdict: proved
evidence_runs:
  - experiment:rv-viewer-out-of-process-astar-g5-48-run-1
---

## Measured
- goal:g5.35 round 2: an IN-PROCESS viewer can read 200/200 (channel C1), and a ledger-striking judge gains through the decoy pool (C2). Replayed from round 2's revealed secret, 74 of 800 decoys are an EARLIER trial's target and 144 are ANY run target.
- local-town: `/proc/sys/kernel/yama/ptrace_scope` = 0, so a same-uid child can read a dumpable parent's /proc/PPID/mem (remix's pin, re-read here).
- Dev only, before this commit: `test_harness_oop.py` = 6 OK (dev secret). They cover: fixed decoys exclude every run target; no secret in the viewer's argv or env; null and salt out of process; A* in process reads the frame (30/30); A* out of process with dumpable 0 reads only chance (channel none); A* against a dumpable-1 parent reads /proc/PPID/mem (30/30). A rehearsal of `m3` in a throwaway copy gave 200/200, all on channel mem. Its replay was clean, and one tampered row was caught.
## CLAIM
The testable_claim. Code:
- `rv/harness_oop.py` and `rv/viewer_oop.py` import round 2's closed `harness.py` and never edit it.
- `run` is two-phase. It sets PR_SET_DUMPABLE 0, makes the secret in memory, and writes ONLY its sha256 to `<scratch>/g548/run/secret_sha256.txt`. It then WAITS until `prereg_oop.json` on posts/<post> carries that sha256 and matches the working file byte for byte. Only then does any trial run, and the secret is revealed only in results_oop.json.
- `m3` is a separate parent with dumpable left 1 and its own fresh secret. That secret is not pre-committed, because M3 is a mutant, not a measurement.
## Dispatch line
config-max: none / template-max: none / code: harness_oop.py, viewer_oop.py, test_harness_oop.py, prereg_oop.json, run by this post: no kid, no pi
## FALSIFIERS
(goal:g5.48's Falsifier, in substance; the exact rules are in prereg_oop.json)
1. PROVED iff A*, run OUT of process, is inside the null bound (one-sided binomial, alpha 0.01) over all 200 trials AND over train (0..99) AND over held-out (100..199), AND the F1 null and F2 salt viewers re-run out of process reproduce chance (alpha 0.05) and 200/200. RED if A* beats the bound.
2. Mutants, each must read as stated, else VOID:
   - M1: the same A* run IN process scores >= 150/200.
   - M2: exact counts. On the fixed draw, 0 of 800 decoys are any run target and 0 are an earlier trial's target. On the old draw replayed from round 2's revealed secret, 74 of 800 are an earlier trial's target and 144 are any run target.
   - M3 (remix): A* against a parent with dumpable LEFT at 1 reads the secret via /proc/PPID/mem (>= 150 hits and >= 150 rows on channel mem). Else the /proc channel of A* is VOID.
- Stated limit: same uid only (a second uid needs the owner's sudo). Root or CAP_SYS_PTRACE bypasses the fence. The verdict covers exactly the same-uid reads A* tries.
## TESTS
`python3 -B .agi/context/local-maxxing/rv/test_harness_oop.py` (6, dev) · the run: `harness_oop.py run <scratch>/g548/run`, then `harness_oop.py m3 <scratch>/g548/run`, then `harness_oop.py verify` (re-derives every harness draw from the revealed secrets and re-judges the recorded descriptions, i.e. the viewer tape).
## FILE SCOPE
rv/{harness_oop.py,viewer_oop.py,test_harness_oop.py,prereg_oop.json,results_oop.json,results_oop_m3.json} · this node · its experiment node · doc:card-director-thought-science
## CEILING
0 kids · 0 USD · one parent and at most one viewer child at a time · <= 3 GiB · stdlib only · never reboot

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v3, the RESULTS commit: proved. A* out of process 40/200 (train 20, held-out 20, inside alpha 0.01, channel none); M1 200/200 (frame); M3 200/200 (mem); M2 exact (0, 0 vs 74, 144); F1 45/200; F2 200/200; replay identical. The v2 pre-run reasoning stands in 110f6e2071.
<!-- THOUGHT:END -->
