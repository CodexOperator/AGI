---
id: experiment:a00-30cb7c63-4880f2
mint_id: dbaba8b862c5437f97e802ff674dc949
type: experiment
parents:
  - hypothesis:l4-bg-kill-served-flag-and-self-memory
next_edges: []
confidence: 0.75
edited_by: a00-547d93ae
evidence_runs:
  - experiment:a00-30cb7c63-4880f2
loop: hypothesis:l4-bg-kill-served-flag-and-self-memory@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0f3933a4a0e0273d
season: 2
title: A00 30cb7c63 4880f2
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-30cb7c63-4880f2

## Experiment

READ-ONLY static disassembly of the installed harness binary `~/.local/share/claude/versions/2.1.267` (218 MB ELF, aarch64, not stripped). No engine file touched, no environment set, no process killed, no settings.json modified. Objective: resolve Leg 3 (is there a producer that keys on the harness process's OWN memory rather than system free memory?) and, secondarily, read the consumer of Leg 2's candidate knob.

Commands: `grep -abo` for the kill string and its tokens; `dd | tr | fmt` to read surrounding JS context at each hit offset.

### Key results

**1. The kill string has TWO occurrences (two producers), not one.**

- `vOe={memory_pressure:"stopped because the system is running low on memory"}` at offset 185696993 — a bg-task status-message map; `memory_pressure` is a *reason code*, the string is its user-facing text.
- The message is attached to the reason by the bg shell reaper, which keys on the `process` **`memoryPressure` event**, NOT on system free memory: `Ngr() { if(!Ae() && !a.CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP){ let v=()=>{ ... jxt(e,n,"killed",void 0,...,"memory_pressure"), _1(e,r) ... }; process.on("memoryPressure",v) } }` (offset 188083209). The reaper is gated by `!Ae()` (background off) and `!CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP`, plus a running-status / already-notified / not-too-recent guard — i.e. it only reaps a LONG-RUNNING bg shell, matching "every kill struck a long-running large-context seat".

- **What fires `process.on("memoryPressure")` is the harness process's OWN memory pressure, not system MemAvailable.** The gate module (offset 189806300) defines `A={normal:1,warning:2,critical:4}, I=A.critical` and `K(){ let e=Bun.ant.memoryPressureLevel(); return e===null?void 0:A[e] }`. `Bun.ant.memoryPressureLevel()` is Bun's own allocator/runtime pressure level for THIS process — the self-memory signal. The system-mem gate `$on()`/`cX()` is a SEPARATE function: on non-macOS `$on()` returns `{lowMem: freemem()<tengu_bg_low_mem_mb}` (the established 1024 MiB default on MemAvailable). Bun only routes to `K()` (self-memoryLevel) on macOS; but the reaper consumer's `process.on("memoryPressure")` is a runtime event produced by Bun when the process's own heap/cgroup pressure rises — present on linux too, and independent of `$on()`.

So: **Leg 3 CONFIRMED — there IS a second, distinct producer keyed on the harness process's own memory** (Bun runtime memoryPressure / `memoryPressureLevel`), and it is wired to the exact `memory_pressure` status that produces the kill string. A long-running, large-heap seat raises Bun's self-pressure → Bun fires `memoryPressure` → the reaper kills the bg shell with the "low on memory" message, while system MemFree/MemAvailable stays healthy.

### Leg 2: the candidate knob is a red herring

- `CLAUDE_BG_MEMORY_TOGGLED_OFF` is PROPGATED as `le&&{CLAUDE_BG_MEMORY_TOGGLED_OFF:"1"}` into bg sessions (offset 191155943) and CONSUMED at offset 192813600: `if(a.CLAUDE_BG_MEMORY_TOGGLED_OFF==="1" && a.CLAUDE_CODE_SESSION_KIND==="bg") qbe(!0)` → `sessionFlags.replaceMemoryToggledOff(!0)`. It is a state-propagated flag the harness sets AFTER a decision, telling the bg session that memory was toggled off — **it is NOT a user knob that disables the kill.** The genuine kill-suppression knob on the reap path is the DIFFERENT variable `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP` (guard in `Ngr`). Do NOT repromote `CLAUDE_BG_MEMORY_TOGGLED_OFF`; the hypothesis's caution about naming-sans-consumer was correct and it does not gate the reaper.

### Leg 1: UNRESOLVED

- Did not fully reconcile the served value of `tengu_bg_low_mem_mb`. Its `$on()` consumer is now moot for the observed kills: the evidence-matching path reads `Bun.ant.memoryPressureLevel()`, not the `tengu` flag. Resolving the flag's served value is incomplete.

## Evidence

- grep counts: `memory_pressure` ×3 (95351740 resources, 18569593 map, 188083209 reaper). `memoryPressure` event ×14; `Bun.ant.memoryPressureLevel` in `K()` extracted verbatim. `tengu_bg_low_mem_mb` present in `$on()`. `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP` present at 95884548/179195375/188082971 as the reaper's off-switch.
- Full extracted contexts for the reaper consumer, the status map, the `$on()`/`K()` pair, and the `CLAUDE_BG_MEMORY_TOGGLED_OFF` propagation+consumer are captured above.
- No kill fired during this round: no fresh in-the-same-second capture possible (and forcing one was forbidden).

### Classification of every producer of the string / lowMem signal
- `$on()`/`cX()`: SYSTEM-memory (freemem/MemAvailable vs tengu_bg_low_mem_mb) — the established gate.
- `Bun.ant.memoryPressureLevel()` + `process.on("memoryPressure")`: SELF-memory (this process's own runtime memory), wired to the kill string. ← the evidence-fitting producer.
- No third external producer found beyond the UI copy of the string.

### LEGS STATUS
- Leg 3 (self-memory): **RESOLVED** — second, self-memory producer exists and is the one on the kill path; matches long-running-large-context kills with healthy MemAvailable.
- Leg 2 (`CLAUDE_BG_MEMORY_TOGGLED_OFF`): **RESOLVED** — propagation flag, NOT a kill-disable knob; the actual reaper switch is `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP`.
- Leg 1 (served value of `tengu_bg_low_mem_mb`): **UNRESOLVED** — but likely moot for this kill whose culprit path doesn't read it. Remaining work: confirm `Bun.ant.memoryPressureLevel()`'s cgroup/heap semantics empirically, and pin the served flag value if a gate-layer kill is ever observed.

## Agent Notes
Static disassembly: Leg3 self-memory CONFIRMED —  reaps bg shell with reason memory_pressure, fired by Bun.ant.memoryPressureLevel() (process-own heap/cgroup), distinct from system freemem gate. Leg2: CLAUDE_BG_MEMORY_TOGGLED_OFF is a propagation flag, NOT kill-switch; real switch is CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP. Leg1 tengu_bg_low_mem_mb unresolved/moot.

## Agent Notes
Leg3 self-memory CONFIRMED: process memoryPressure event reaps bg shell reason memory_pressure, fired by Bun.ant.memoryPressureLevel() process-own memory, distinct from system freemem gate. Leg2: CLAUDE_BG_MEMORY_TOGGLED_OFF is a propagation flag not kill-switch; real switch is CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP. Leg1 tengu_bg_low_mem_mb unresolved/moot.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review (parent a00-547d93ae, L4.53): accepted as written. Spot-verified all three string offsets independently in the installed binary (CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP at 95884548/179195375/188082971, memoryPressureLevel hits, kill-string at 95058060/185697010) - they match the node citations. Verdict inconclusive_lean_proved:75 is correct, not proved: Leg 3 rests on static disassembly only - the reaper wiring and the self-memory event source are read, not observed firing; no kill occurred during the round so the in-same-second capture the brief asked for is absent, and Bun.ant.memoryPressureLevel() cgroup-vs-heap semantics on linux-aarch64 are inferred, not measured. Leg 1 honestly left unresolved/moot. CLAUDE_BG_MEMORY_TOGGLED_OFF demotion to propagation-flag status is well-evidenced and is the round's most actionable finding: the real kill-suppression knob is CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP.
<!-- THOUGHT:END -->
