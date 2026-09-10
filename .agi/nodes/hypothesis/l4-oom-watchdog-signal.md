---
id: hypothesis:l4-oom-watchdog-signal
mint_id: 6b6b9b9673af450ba8928076eeb968bc
type: hypothesis
parents:
  - idea:l4-oom-watchdog-signal
next_edges: []
confidence: 0.6
edited_by: sanctuary-helper
scaffold_hash: bedb2428f77fb592
season: 2
tags:
  - hypothesis
testable_claim: "The harness's background-task watchdog keys its low-memory kill decision on MemFree (e.g. Node's os.freemem(), which excludes reclaimable page cache) rather than MemAvailable, so a background task can be killed and reported as \"stopped because the system is running low on memory\" while `free -h` shows many GB of MemAvailable, because a large page cache leaves MemFree low even when the system is not actually under memory pressure. Falsifiable: if the watchdog instead reads MemAvailable (or an equivalent cgroup/cgroup-aware figure), the hypothesis is false and the kill must be explained some other way (a hard per-process RSS/VSZ cap, a cgroup limit, an OS-level OOM killer invocation, or a fixed task-count/wall-clock cap unrelated to memory at all)."
thought_session: sanctuary-helper-05
title: The kill watchdog keys on MemFree, not MemAvailable
---
<!-- BODY:BEGIN -->
# hypothesis:l4-oom-watchdog-signal

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## L4.46 brief -- why background tasks get killed under "low memory" that isn't

Assigned by sanctuary-director gen III (seat-sanctuary-director-4e), owner's
ask verbatim at doc:l4-owner-decisions:485. Runs in parallel with L4.44/L4.45
(both touch rotate.py; this round touches neither).

FIRST-HAND EVIDENCE, mine, from earlier this session -- a SECOND real
occurrence, distinct from L4.37 (which gen III has already ruled OUT as an
instance of this: L4.37 was SIGTERM'd by the director one second before its
own next write, not reaped):

I started a trivial background bash loop (task id bps80b619, a `ps -p`
liveness poll on 15s intervals, negligible memory footprint) while 6 of my
own dispatched pi-harness parent processes were concurrently live (each
~260-270MB RSS per a later `ps` check, ~1.6GB total for mine alone, plus
other seats' concurrent rounds at the time). The task printed exactly ONE
status line -- "01:09:41 check 1: 6/6 dispatched parents still alive" --
then was killed with no further output. The harness's own notification
read: "Background command ... was stopped because the system is running
low on memory", status=killed. A `free -h` I ran AFTER noticing the kill
(not at the kill instant) showed: total 23Gi, used 7.9Gi, free 5.3Gi,
buff/cache 10Gi, available 15Gi, swap 667Mi/4Gi used. That free -h is
AFTER-THE-FACT evidence only -- it does not by itself settle what MemFree
vs MemAvailable read AT THE KILL INSTANT, which is exactly item (2) below.
Treat my incident as a second real data point and a candidate reproduction
window (many concurrent pi processes + a lightweight monitored background
task), not as proof on its own.

ITEMS:

(1) THE KILL ITSELF: find the exact source of the kill decision (search the
harness/runtime for the literal string "running low on memory" or its
template) -- name the file, the threshold/condition it checks, and which
signal it sends (SIGTERM, SIGKILL, or a supervisor-level stop that never
reaches the process as a signal at all). Read-only investigation.

(2) REPRODUCE: start a harness-tracked background task, deliberately inflate
page cache (e.g. reading/writing large files to grow buff/cache while
MemAvailable stays high), and log BOTH `MemFree` and `MemAvailable` (read
directly from /proc/meminfo, once per second) until either the task is
killed or you stop the experiment. The reproduction IS the artifact: a
timeseries (a simple text table or small chart) of both numbers with the
kill instant marked, if a kill occurs. If you cannot trigger a kill in a
reasonable window, say so plainly -- a non-reproduction is still evidence,
just weaker, and must not be written up as if it settled the question.

(3) CLOSED, DO NOT SPEND A KID ON IT -- state plainly in the claim/body:
L4.37 is NOT an instance of this phenomenon. Its pi session log shows the
parent writing at 03:16:43Z and creating kid 3 at 03:16:42Z -- one second
before the director SIGTERM'd it. It was killed by the director, not
reaped by any watchdog. The honest evidence set for THIS hypothesis is
traps 0ai, 0ai-b, 0p, my own bps80b619 incident above, and the rotate-self
kill only -- do not fold L4.37 into the count.

(4) THE REMEDY: name the harness setting if one exists to change the
watchdog's memory signal or threshold. If none exists, restate the
standing rule -- long-running work goes in the FOREGROUND with a long
timeout (400000ms) rather than backgrounded -- WITH THE MECHANISM NAMED:
say exactly why `nohup`/backgrounding does not protect a process from
this kill (it is the HARNESS's own supervisor stopping the task, not the
shell's job control or the kernel OOM killer, so nothing at the process
level shields it).

CONSTRAINTS: kid ceiling stated in the node (2 is likely right -- one for
items 1+3, one for items 2+4, or one kid doing all four if it moves fast;
your call, but say which). The assignment IS this hypothesis's own
testable_claim (trap 0ak) -- do not let a kid write a verdict ABOUT the
claim's wording instead of testing it. Commit AND PUSH before dispatching
(trap 0an). Verify the BYTES after any node write, never trust the
`updated:`/report line (trap 0ah). One kill is never a stop -- sweep
`spawn_budget.py status` until TWO consecutive clean reads before treating
anything as fully stopped. Run only the tests this round could BREAK (if
any -- this is read-only measurement plus possibly a small fixture, so
likely none need running) -- never the full suite. Read-only measurement
against live state; nothing destructive.

REPORT: write one experiment node whose parents is this hypothesis, with
the kill-source citation (item 1), the reproduction timeseries or the
honest non-reproduction (item 2), the L4.37 exclusion stated plainly
(item 3), and the remedy (item 4). evidence_runs must resolve to real
node ids; your own experiment counts once it exists.
