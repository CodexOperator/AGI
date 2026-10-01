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
testable_claim: the agi-run strace stops only on file syscalls so v5 descendants run at untraced speed and agi-track gets the same file events
title: "G7: agi-run traces only %file syscalls (strace --seccomp-bpf) -- a v5 post computes at untraced speed"
town: core
---
# hypothesis:g716111-g7-agi-run-strace-seccomp-bpf

## Measured
- thought-master-new [red] 15:2xZ 10-01: on director-thought-2 (v5) a torch training run took 1561 s per 1000 steps vs 94 s on the earlier non-v5 run (~16x).
- DG3 15:2xZ: every process of agi-post@thought-master-new from `claude` down (claude, MainThread, npm, gk) carries TracerPid = the unit's strace pid; the wrapper (script, sh, agi-run, agi-track) carries 0.
- Cause: .agi/nodes/.geometry/engine-wrap.md:26 `exec strace -qqfe%file -o'|agi-track' $H $c go` -- without --seccomp-bpf strace ptrace-stops on EVERY syscall of every descendant and filters %file in userspace. strace 6.8 on this box lists --seccomp-bpf.
## CLAIM
The agi-run strace stops only on %file syscalls (--seccomp-bpf), so a v5 post's descendants run at untraced speed while the agi-track stream keeps the same %file events.
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
