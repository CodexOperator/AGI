---
id: doc:card-thought-master
mint_id: 7762cf2104eb4f54a190dd5f622cdf4f
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: thought-master-new
model: claude-opus-5-5
role: director
scaffold_hash: 8511ca269efcc3ca
season: 2
title: Card thought master
town: core
---
# doc:card-thought-master-new

thought-master-new · v5 post (unit agi-post@thought-master-new) · Opus 5.5 high · RESEARCH LOOP of town:local-maxxing (successor lane of doc:card-thought-master; old TM on STANDBY) · trunk local-maxxing/season2/main · worktree <home>/t, branch posts/thought-master-new · template doc:unified-director-brief + HEAD doc:unified-head

## §0 State (22:3xZ 10-01; box rebooted 22:18Z; owner "go" in this session 22:3xZ = the go for the next round)
| | |
|---|---|
| lane | research loop: town:local-maxxing board, goal:g5.22-g5.31, round placement (belam 12:44Z; owner 07:5xZ) |
| run | owner 15:1xZ: keep going until goal:g7.16.1.11.1-.10 complete · COMMS = DIRECT session messages (SendMessage, names from ListAgents), not inbox dms (owner 18:1xZ) · belam = belam-S2-L5-I · SM lands my merge-ups (a v5 post cannot write MAIN) |
| directors | director-thought-1: ORDERED 22:3xZ (SendMessage, delivery unconfirmed) to build the FREQ-ABLATION round · director-thought-2: DOWN after the reboot until the owner says |
| subagents | Sonnet 5.5 for every subagent; me Opus 5.5 |
| LANDED | SEEDS x3 + FAIR P4 (both DISPROVED): a6ac4d92e = 67680d223 on local-maxxing/season2/main, pushed by SM (suite 7876 passed / 1 = the trunk red; links 5670/0; grid commit --all run by SM, 31 versions). Trunk merged back into my branch 6d8bb6265 |
| ROUND OUT | FREQ-ABLATION = hypothesis:lm-neuron-periodicity-every-family-frequency-is-load-bearing-in-logit-space (minted d05c57e81): logit-space ablation of each family frequency vs an EXHAUSTIVE non-key-frequency null (C1) + family direct-logit energy >= 0.5 in its own frequency (C2); builder DT-1, expected experiment:dt1-neuron-period-freqabl-1001 |
| PARKED | L4 r5 = hypothesis:lm-l4-direct-head-windows-hold-on-the-served-9b: needs MemAvailable >= 8 GB held + a docker-capable user (v5 has none); resume steps in its THOUGHT |

## §1 Plan
```
DONE   self-poke toy line LANDED a001a3c61 · guard-leak fix LANDED 0376b07da (goal:g7.33.19 row 80) · seeds x3 reviewed + merged, merge-up queued
DONE   FAIR P4 reviewed CONFIRMED_DISPROVED + recorded + merged (dc1504bba) + gated + [merge-up] a6ac4d92e to SM
DONE   SM landed 67680d223; trunk merged back 6d8bb6265
NOW    (1) FREQ-ABLATION round out to DT-1; await its ONE return line (tip sha, verdict, C1/C2 per seed)
NEXT   (2) adversarial ONE-process Sonnet review recomputing from raw (brief as the FAIR P4 one: ulimit -v 4000000, PSI gate, 40 min) -> THOUGHT + board g5.28 + merge DT-1 -> gate -> [merge-up] to SM
BLOCKED L4 r5 (memory + docker) · stage-2 SELF-POKE on an LLM (HELD: no multi-digit-token model resident = a download, BANKED)
```

## §2 Landed
- 20:5xZ LANDED 67680d223 (SM, supersedes 165f57b0f); trunk merged back 6d8bb6265
- 20:2xZ FAIR P4 review CONFIRMED_DISPROVED (one process, peak RSS 0.7 GB; one supplementary run started at PSI 7.19, over its gate -- disclosed to SM); merged DT-2 dc1504bba; residue text 9bfaa48aa..0d4116d54; hypothesis c5b2d8e04; board a6ac4d92e; links 5661/0; p4fair test 8/8
- 19:4xZ seated after rotation; keys file host comment reverted; FAIR P4 review re-launched one-process; 165f57b0f still NOT on local-maxxing/season2/main
- 19:4xZ CUT my reviewer's 8 workers on belam's [red] (PSI full avg60 36-39 vs the 40 reboot line); belam told; scratch removed
- 19:3xZ FAIR P4 minted c6bc7db49 -> DT-2 -> DISPROVED · 19:0xZ SEEDS x3 DISPROVED reviewed + DH.1 text, board row 3201a0277, DT-2 key comment + card paths fixed (165f57b0f)
- 18:2xZ guard-leak fix LANDED 0376b07da (row 80 beside DG3's 78/79 after a renumber) · comms switched to SendMessage
- 16:3xZ self-poke toy line LANDED a001a3c61 (PROVED; C5b demoted: not beyond size) · findings to DG3: v5 strace tracer (16x slow), comms ACLs lost at reboot

## 🔴 Where it stops
```
DT-1 RETURNED a352fc937: experiment:dt1-neuron-period-freqabl-1001 DISPROVED by C1 (s0 k=34, s1 k=3, s2 k=17 drop ~0), C2 12/12; one-process Sonnet review RUNNING (also loss deltas + sufficiency arm). My error: the hypothesis said 57-dim basis, it is 113 dims (57 components) -- fix in the hypothesis THOUGHT
next command if silent > 60 min: ListAgents, then git log --oneline -5 posts/director-thought-1 (reconcile by branch, never by inbox alone)
```

## §4 Traps
- a reviewer subagent FANS OUT unless forbidden: every compute brief says ONE process, no pools, ulimit -v, a PSI start gate (19:4xZ near-reboot)
- write a sha into a brief only after reading it from git (19:2xZ: an invented tip had to be corrected mid-review)
- MY METER: newest usage in ~/.claude/projects/*/<session>.jsonl (input + cache_read + cache_creation) / 1,000,000; line 0.47; rotate = card whole + commit + touch ~/.fresh; kill $PPID ($PPID = claude in the Bash tool)
- v5: no systemd user manager (long runs = setsid nohup inside the unit cgroup, MemoryHigh 4 GiB, KillMode control-group) · every child is a tracee of the unit strace until the unit restarts onto the -b execve wrap (check TracerPid of a fresh python3)
- a stop / rotation of a v5 unit DELETES RUNTIME_DIRECTORY (/run/agi-<post>) until G8 is projected: never keep work there
- MAIN is not writable by a v5 user: SM lands; datasets/osc-band in MAIN too -> out dirs resolve under the builder's tree
- before a merge-up: grep added lines for the host name + absolute home paths (.agi/keys/* ssh comments; cards) and fix them on my branch
- a findings row number is claimed only at landing: on a conflict keep theirs verbatim, renumber mine + every reference (write.py sub!)
- anonymize.py and provisioning.py die on MAIN .env (G2) -- grep by hand instead
- tests: NO pytest anywhere on the box -> scratch shim (pytest.py with importorskip/approx/mark.parametrize + a runner) on PYTHONPATH with /data/ml/scratch/osc03/pylib, run by /data/ml/.venv/bin/python3; never pip install
- import torch needs ulimit -v >= 4000000 (2000000 fails to map); brief subagents with 4000000
- git push fails (no creds for a v5 user); grid.py commit --all fails (MAIN .grid.lock) -- SM does both at landing
- write.py `thought` takes the TEXT inline ("thought $(cat f)"), not a path
- send.py from me arrives UNSIGNED (a v5 post has no seat key; key work HELD) -- direct session messages are the route
- write.py create on a town node: --actor thought-master-new, NO --role; a card write: --role director

## §5 Verification
- every round: an adversarial Sonnet review recomputes the verdict from the raw files; my own test run from the repo root; evidence dry-run []; links 0 broken (5648 resolved at 17:5xZ)

## §6 BANKED
- L4 r5 on the 9B: (a) run when the owner thins the live posts (RECOMMENDED) · (b) lower the 8 GB gate = OOM risk · (c) a smaller-model rung first; + a docker grant for v5 users
- an LLM periodicity / self-poke test needs a model whose tokenizer holds multi-digit numbers as one token = a download (owner call)
- next-round design: per-frequency logit lens MINTED d05c57e81 on the owner's go (22:3xZ); path patching stays the fallback lens if it is disproved

## Skills
agi-send · agi-node-write · agi-goal · agi-workflow · agi-verify · agi-rotate · agi-dispatch · agi-memory-guard · agi-master-gate
