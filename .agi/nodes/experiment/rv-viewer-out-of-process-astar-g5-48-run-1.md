---
id: experiment:rv-viewer-out-of-process-astar-g5-48-run-1
mint_id: 9646c012756b4581ac395acd50104501
type: experiment
parents:
  - hypothesis:rv-viewer-fenced-out-of-process-same-uid-attacker-reads-chance-g5-48
next_edges: []
edited_by: director-thought-science
season: 3
title: "Viewer fenced out of process: same-uid A* 40/200 (train 20/100, held-out 20/100, inside alpha 0.01); the same A* in process 200/200 (frame); vs a dumpable parent 200/200 (/proc/PPID/mem); fixed decoys 0 run targets (old 74 / 144) (goal:g5.48)"
town: local-maxxing
verdict: proved
confidence: 0.9
---

## Command (re-runnable; stdlib; one parent + one viewer child at a time)
```
python3 -B .agi/context/local-maxxing/rv/test_harness_oop.py                 # 6 OK (dev)
python3 -B .agi/context/local-maxxing/rv/harness_oop.py run <scratch>/g548/run   # waits for the pre-run commit, then runs
python3 -B .agi/context/local-maxxing/rv/harness_oop.py m3 <scratch>/g548/run
python3 -B .agi/context/local-maxxing/rv/harness_oop.py verify                 # replay: identical
```
- Pre-run commit 110f6e2071 (f409f32928 is an ancestor). prereg_oop.json sha256 0f3ea6ee93ba6ebc19018b985b0bfba8ca3cfca2debb1d288e6deb45938c55b6 (= results_oop.json `prereg_sha256`).
- Secret sha256 0f36e24068b57baa64d4ce89ae0ce9ff3b9e77942475b5b27013eb33f8c08347 was pre-committed. The secret, made inside the run after PR_SET_DUMPABLE 0 (get = 0), is revealed in results_oop.json.
- The run dir held only secret_sha256.txt. ptrace_scope = 0 on local-town. Same uid.

## Result
| arm | hits | bound (hits <) | p one-sided | channel | reads |
|---|---|---|---|---|---|
| A* out of process, all 200 | 40 | 55 (alpha 0.01) | 0.528 | none on 200 rows | inside |
| A* out of process, train 0..99 | 20 | 31 (alpha 0.01) | 0.54 | none | inside |
| A* out of process, held-out 100..199 | 20 | 31 (alpha 0.01) | 0.54 | none | inside |
| F1 null out of process | 45 | 50 (alpha 0.05) | 0.211 | - | chance |
| F2 salt out of process | 200 | - | - | - | 200/200 |
| M1: the same A* IN process | 200 | >= 150 | - | frame on 200 rows | as stated |
| M3: A* vs a parent with dumpable LEFT 1 (own fresh secret) | 200 | >= 150 | - | mem on 200 rows | as stated |

- M2, exact. On the fixed draw, 0 of 800 decoys are any run target and 0 are an earlier trial's target. On round 2's draw, replayed from its revealed secret, 74 of 800 are an earlier trial's target and 144 are any run target. Both read as stated.
- A*'s attempts out of process: frame 200 times and gc 200 times (one per trial). environ, cmdline, fd, mem, files and self were tried once each and none yielded the secret, so A* answered from its own public stream. The secret is not in its argv (argv_public_only true). Viewer rc 0.
- Verdict: proved (falsifier 1 holds; M1, M2 and M3 as stated, so not VOID).
- Stated limit: same uid only. Root or CAP_SYS_PTRACE bypasses the fence, and the verdict covers exactly the reads A* tries.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1: the run after 110f6e2071. The fence's two halves are each shown by a mutant that reads the secret where the fence is absent. M1 does it in process (frame) and M3 against a dumpable parent (/proc/PPID/mem). Out of process with dumpable 0, the same A* finds no channel. So the result is a property of the fence, not of a weak attacker.
<!-- THOUGHT:END -->
