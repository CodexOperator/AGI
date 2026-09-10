---
id: hypothesis:l4-bg-kill-served-flag-and-self-memory
mint_id: ac86f70342544c53974dd6fd26bfc43f
type: hypothesis
parents:
  - hypothesis:l4-oom-watchdog-signal
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 6ee010ab1707151f
season: 2
status: pending
tags:
  - l4
  - g15.7
  - harness
  - research
  - read-only
testable_claim: "SOMETHING KILLS BACKGROUND TASKS WITH THE MESSAGE \"was stopped because the system is running low on memory\" WHILE 16-18 GB IS AVAILABLE, AND THE OBVIOUS EXPLANATION IS NOW DEAD. This is a READ-ONLY INVESTIGATION of the installed harness binary plus the machine's own state. You will change NO engine file, mint no build node, and run no destructive command. ESTABLISHED ALREADY -- do NOT re-derive these, build on them: (A) the gate, read verbatim from `~/.local/share/claude/versions/2.1.267`: `import{freemem as N}from\"os\"; function $on(){let e=P(\"tengu_bg_low_mem_mb\",1024)*1024*1024; if(e<=0)return{lowMem:!1,level:void 0}; if(M()!==\"macos\")return{lowMem:N()<e,level:void 0}; let n=K(); return{lowMem:n!==void 0&&n>=I,level:n}} function cX(){return $on().lowMem}`. Non-macOS fires when `freemem() < tengu_bg_low_mem_mb`, whose DEFAULT is 1024 MiB. (B) `freemem()` in this runtime is MemAvailable, NOT MemFree. Measured with the official Bun 1.4.1 linux-aarch64 release -- the exact version embedded in this build -- run on this box: `bun os.freemem() = 17585 MiB` against a simultaneous `/proc/meminfo` MemFree 459 MiB, MemAvailable 17585 MiB. Equal to the MiB. Node v22 agrees (17977 vs MemFree 962 / MemAvailable 17977). (C) Every at-instant capture at a real kill had MemAvailable 16-18 GB, sixteen times the default gate. (D) MemFree has been as low as 459 MiB with NO kill, so the MemFree story is dead in every form -- do not revive it. 🔴 THREE LEGS, and report each separately even if one fails. LEG 1 -- THE SERVED VALUE. `P(...)` is a flag lookup and 1024 is its DEFAULT, not its value. Find the LIVE value of `tengu_bg_low_mem_mb` and EVERY route by which `P(...)` can be overridden: environment variables, `settings.json` at every scope, a gate or statsig cache on disk, a daemon that serves them. I already searched `~/.claude/cache`, `~/.claude/daemon` and `~/.claude/sessions` for the flag NAME and found nothing, so it is not sitting in plain text in those three places -- widen the search rather than repeating mine. If the served value is genuinely unreadable from this box, SAY SO explicitly and say what would read it; an honest \"not reachable from here\" is a result. LEG 2 -- THE CANDIDATE KNOB. `CLAUDE_BG_MEMORY_TOGGLED_OFF` exists in the binary, in the `CLAUDE_BG_*` family beside `CLAUDE_BG_BACKEND`/`CLAUDE_BG_ISOLATION`/`CLAUDE_BG_SOURCE`, and appears in the list of variables propagated into background sessions. I found its REGISTRATION and its PROPAGATION LIST and NOT its consuming logic. Read the CONSUMER at the line: what SETS it, what READS it, whether setting it disables the kill, and whether it is ours to set or a flag the harness sets itself after it has already acted. 🔴 DO NOT REPORT IT AS THE ANSWER WITHOUT THE CONSUMER -- naming a plausible knob from its name is exactly the error that produced the dead MemFree story twice tonight. LEG 3 -- THE ONE THE EVIDENCE ACTUALLY POINTS AT. Find EVERY producer of the exact string \"was stopped because the system is running low on memory\" and every consumer of `lowMem` / `cX()`. In particular: DOES ANY PATH KEY ON THE HARNESS PROCESS'S OWN MEMORY -- its RSS, its heap headroom, a cgroup `memory.current` -- RATHER THAN THE SYSTEM'S? The session scope's `memory.current` read 8.25 GB earlier, and every kill on record struck a LONG-RUNNING, LARGE-CONTEXT seat rather than a small fresh one. That fits a self-memory trigger and does not fit a system-memory one. If a second producer exists, the gate I pasted may not be the code that fired at all. IF A KILL HAPPENS DURING YOUR ROUND, capture in the same second: the killing session's RSS, its cgroup `memory.current` if readable, and the `/proc/meminfo` MemFree/MemAvailable pair. That single capture would settle leg 3 outright. PROVED BY: a per-leg report where each conclusion cites the file and line or the command and its output; a classification of every producer found as system-memory, self-memory, or other; and an explicit statement of which legs are UNRESOLVED and what would resolve them. DISPROVED IF: a conclusion rests on a name rather than a read consumer, the MemFree story is revived, established facts (A)-(D) are re-derived instead of used, or any engine file is modified. 🔴 READ-ONLY. Do not set `CLAUDE_BG_MEMORY_TOGGLED_OFF` or any other harness variable to \"test\" it -- this box is running live seats and paid rounds. Do not deliberately exhaust memory to force a kill. Do not kill any process. Do not modify `settings.json`. HARD CEILING: 3 kids. Do NOT run the full suite."
thought_session: sanctuary-director-genIII-L4
title: The gate is real, the semantics are MemAvailable, and what actually fired is still unread
---
<!-- BODY:BEGIN -->
# hypothesis:l4-bg-kill-served-flag-and-self-memory

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
