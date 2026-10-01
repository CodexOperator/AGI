---
id: doc:card-thought-master-new
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
title: Card thought master new
town: core
---
# doc:card-thought-master-new

thought-master-new · v5 post (unit agi-post@thought-master-new) · Opus 5.5 high · RESEARCH LOOP of town:local-maxxing (successor lane of doc:card-thought-master; old TM on STANDBY) · trunk local-maxxing/season2/main · worktree <home>/t, branch posts/thought-master-new · template doc:unified-director-brief + HEAD doc:unified-head

## §0 State (19:4xZ 10-01, read from date -u) -- successor seated after the 0.40 rotation (belam meters me; my agi-meter is blind until G10 + a restart)
| | |
|---|---|
| lane | research loop: town:local-maxxing board, goal:g5.22-g5.31, round placement (belam 12:44Z; owner 07:5xZ) |
| run | owner 15:1xZ: keep going until goal:g7.16.1.11.1-.10 complete · COMMS = DIRECT session messages (SendMessage, names from ListAgents), not inbox dms (owner 18:1xZ) · belam = belam-S2-L5-I · SM lands my merge-ups (a v5 post cannot write MAIN) |
| directors | director-thought-1 (successor after its 18:2xZ rotation): HOLD, no order · director-thought-2: idle after FAIR P4 |
| subagents | Sonnet 5.5 for every subagent; me Opus 5.5 |
| PENDING REVIEW | FAIR P4 = hypothesis:lm-neuron-periodicity-fair-p4-every-seed-has-a-load-bearing-family; experiment:dt2-neuron-period-p4fair-1001 DISPROVED (posts/director-thought-2 e7d25a5ec, results 2e6238e08): only seed 0 has a load-bearing family (k=45, pU 100 / pN 99.5); seeds 1 + 2 none; seed 0 k=5 misses N q99 by 0.008. First Sonnet review CUT 19:4xZ (belam [red]: 8 python workers x 650 MB). RE-LAUNCHED 19:4xZ (PSI full avg60 3.3, MemAvailable 9.6 GB): ONE Sonnet 5.5 subagent, ONE process, ulimit -v 2000000, threads 1, PSI gate per run, 40 min compute cap, tip e7d25a5ec -- RUNNING |
| QUEUED LANDING | SEEDS x3 DISPROVED, [merge-up] 165f57b0f queued by SM 19:05Z (its successor gates after the urgent G10) |
| PARKED | L4 r5 = hypothesis:lm-l4-direct-head-windows-hold-on-the-served-9b: needs MemAvailable >= 8 GB held + a docker-capable user (v5 has none); resume steps in its THOUGHT |

## §1 Plan
```
DONE   self-poke toy line LANDED a001a3c61 · guard-leak fix LANDED 0376b07da (goal:g7.33.19 row 80) · seeds x3 reviewed + merged, merge-up queued
NOW    (1) FAIR P4 review RUNNING (one-process brief, launched 19:4xZ) -- await its verdict; if it is lost with a rotation, re-launch the same brief
NEXT   (2) on its verdict: THOUGHT on the hypothesis + board row g5.28 (append to the SEEDS x3 text) -> merge posts/director-thought-2 -> gate -> [merge-up] to SM by SendMessage
       (3) when SM lands 165f57b0f: git merge local-maxxing/season2/main into my branch
BLOCKED L4 r5 (memory + docker) · stage-2 SELF-POKE on an LLM (HELD: no multi-digit-token model resident = a download, BANKED)
```

## §2 Landed
- 19:4xZ seated after rotation; keys file host comment reverted; FAIR P4 review re-launched one-process; 165f57b0f still NOT on local-maxxing/season2/main
- 19:4xZ CUT my reviewer's 8 workers on belam's [red] (PSI full avg60 36-39 vs the 40 reboot line); belam told; scratch removed
- 19:3xZ FAIR P4 minted c6bc7db49 -> DT-2 -> DISPROVED · 19:0xZ SEEDS x3 DISPROVED reviewed + DH.1 text, board row 3201a0277, DT-2 key comment + card paths fixed (165f57b0f)
- 18:2xZ guard-leak fix LANDED 0376b07da (row 80 beside DG3's 78/79 after a renumber) · comms switched to SendMessage
- 16:3xZ self-poke toy line LANDED a001a3c61 (PROVED; C5b demoted: not beyond size) · findings to DG3: v5 strace tracer (16x slow), comms ACLs lost at reboot

## 🔴 Where it stops
```
FAIR P4 review running (one-process Sonnet subagent, tip e7d25a5ec); on its verdict: THOUGHT + board g5.28 + merge DT-2 + merge-up
next command (if this session died): cat /proc/pressure/memory, then re-launch the review (Agent, model sonnet, ONE-process brief, tip e7d25a5ec)
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
- tests: PYTHONPATH=/data/ml/scratch/osc03/pylib:<a venv site-packages with pytest>; the ml venv has no pytest; never pip install system-wide
- send.py from me arrives UNSIGNED (a v5 post has no seat key; key work HELD) -- direct session messages are the route
- write.py create on a town node: --actor thought-master-new, NO --role; a card write: --role director

## §5 Verification
- every round: an adversarial Sonnet review recomputes the verdict from the raw files; my own test run from the repo root; evidence dry-run []; links 0 broken (5648 resolved at 17:5xZ)

## §6 BANKED
- L4 r5 on the 9B: (a) run when the owner thins the live posts (RECOMMENDED) · (b) lower the 8 GB gate = OOM risk · (c) a smaller-model rung first; + a docker grant for v5 users
- an LLM periodicity / self-poke test needs a model whose tokenizer holds multi-digit numbers as one token = a download (owner call)
- next-round design (from the seeds + fair-P4 reviews): single-family ablation is not a reliable causal map here; a per-frequency logit attribution or a path-patching probe is the candidate next lens

## Skills
agi-send · agi-node-write · agi-goal · agi-workflow · agi-verify · agi-rotate · agi-dispatch · agi-memory-guard · agi-master-gate
