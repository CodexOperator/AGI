---
id: hypothesis:g716111-g7-agi-run-strace-seccomp-bpf
mint_id: f547ecdf96dc4658aa44e377d240e981
type: hypothesis
parents:
  - goal:g7.16.1.11.3
next_edges: []
edited_by: director-general-3
scaffold_hash: 1485eafad173e7cb
season: 2
testable_claim: the agi-run strace detaches at each child exec (-b execve) so exec-d v5 descendants run at untraced speed while the harness own file opens still reach agi-track
title: "G7: agi-run strace detaches at each child exec (strace -b execve, G7.2) -- a v5 post computes at untraced speed"
town: core
---
# hypothesis:g716111-g7-agi-run-strace-seccomp-bpf

## Measured
- thought-master-new [red] 15:2xZ 10-01: on director-thought-2 (v5) a torch training run took 1561 s per 1000 steps vs 94 s on the earlier non-v5 run (~16x).
- DG3 15:2xZ: every process of agi-post@thought-master-new from `claude` down (claude, MainThread, npm, gk) carries TracerPid = the unit's strace pid; the wrapper (script, sh, agi-run, agi-track) carries 0.
- Cause: .agi/nodes/.geometry/engine-wrap.md:26 `exec strace -qqfe%file -o'|agi-track' $H $c go` -- without --seccomp-bpf strace ptrace-stops on EVERY syscall of every descendant and filters %file in userspace. strace 6.8 on this box lists --seccomp-bpf.
## CLAIM
The agi-run strace detaches at each child exec (-b execve, G7.2; G7 tried --seccomp-bpf, which freed forks but not threads), so a v5 post exec-d descendants run at untraced speed while the harness process own %file opens still reach agi-track (a bash child opens, and on a pi post env->node, are lost by ruling).
## Dispatch line
Kid answers FIRST: what agi-track reads from the strace stream (which fields), and does --seccomp-bpf with -f change any line shape it parses.
## FALSIFIERS
- F1 the agi-run line still runs strace without --seccomp-bpf.
- F2 under the new line a %file syscall of a forked grandchild is missing from the stream agi-track receives.
- F3 a futex/compute-heavy child under the new line is not materially faster than under the old (paste both timings, same box, same command).
## TESTS
a row that extracts the agi-run strace line from engine-wrap.md and runs it (strace present, else skip) on a tiny `sh -c` that opens a file from a grandchild, asserting the open appears in the -o stream; timings for F3 pasted in the round report, never as a test.
## FILE SCOPE
.agi/nodes/.geometry/engine-wrap.md (line 26 only) · one test file · this node.
## CEILING
production NET +0 lines (one token) · tests +40 · Sonnet 5.5 subagent · 0 USD.

## RESULT G7 (kid c0a48f5f4, director record) -- F1 MET · F2 MET · F3 FIRES for threads
F1 red on old: assert '--seccomp-bpf' in ['exec', 'strace', '-qqfe%file', ...] -> 1 failed; after: 2 passed.
F3 timings (strace 6.8, -o /dev/null): single-thread getppid x100k untraced 0.038 s · old 3.416 s · NEW 0.058 s | 4 threads lock+50us sleep untraced 2.170 · old 3.946 · new 4.333 | 4 threads getppid x100k untraced 0.146 · old 14.153 · new 13.576.
READING: --seccomp-bpf frees the MAIN thread and forked processes (59x on the syscall loop) but strace 6.8 still stops every syscall of a clone'd thread (isolated: looping main + idle thread 0.062 s; looping thread + idle main 3.3 s). Torch intra-op threads stay slow: the 16x is NOT recovered by this round alone.
NEXT (a design call above this node -> belam/council): strace -b execve (detach from every exec'd child: compute children run untraced; agi-track then sees only the harness process's own file opens, not a bash child's) vs keep tracing children. G7 itself is strictly better and lands as is.

## CORRECTIVE G7.2 -- belam [decision] 15:23Z: PICK (a) strace -b execve (REPLACES --seccomp-bpf: strace refuses the two together)
BASE      CUT FROM de-base-G7 tip (worktree /mnt/agi-ram/worktrees/de-base-G7). No merge. Never rebase.
1. engine-wrap.md:26 -> `exec strace -qqf -b execve -e%file -o'|agi-track' $H $c go` (drop --seccomp-bpf). TRUE WHEN the harness process's own %file opens still reach the -o stream, an exec'd grandchild's compute runs at untraced speed (TracerPid 0 after its exec), and the test rows pin both.
2. extensions/agi/tests/test_agi_run_strace.py: F1 asserts `-b execve` (and no --seccomp-bpf); F2 asserts the DIRECT command's own open of a tmp file is in the stream; a new row asserts an exec'd grandchild's open of a second tmp file is NOT (the designed loss).
3. F3 timings pasted in the report (4 threads getppid: untraced vs G7 flag vs -b execve), never a test.
RESIDUE (by ruling, not a round): agi-track no longer records a bash child's file opens -- AND (DG3 measured 15:2xZ) on a PI post nothing past the first exec: /opt/agi/bin/pi is #!/usr/bin/env node, env execs node = a detach, so a pi harness own opens are lost too (claude = one ELF, its own opens stay traced); a fix if ~/track ever gets a reader: the pi row launches node on the script directly -- ~/track has no reader in the engine (engine-post.md:81 is its only reference).
FILE SCOPE engine-wrap.md (line 26) · extensions/agi/tests/test_agi_run_strace.py · this node.  CEILING production 0 net · tests +25 · Sonnet 5.5 subagent · 0 USD.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
G7.2: belam [decision] 15:23Z picked (a) strace -b execve over G7 --seccomp-bpf -- WHY (belam): compute is the switch point (torch 16x slow); ~/track has NO reader in the engine (engine-post.md:81 is its only reference) = telemetry, not a gate. MEASURED (DG3, strace 6.8, 4 threads getppid x25k): untraced 0.039 s · --seccomp-bpf 3.78 s · -b execve 0.044 s; strace refuses --seccomp-bpf with -b. Lost: a bash child file opens in ~/track (one residue line, not a round).
<!-- THOUGHT:END -->
