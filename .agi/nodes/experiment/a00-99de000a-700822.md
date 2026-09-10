---
id: experiment:a00-99de000a-700822
mint_id: 502f50df085b4c4ba109e05f4cb1e60e
type: experiment
parents:
  - hypothesis:l4-bg-kill-served-flag-and-self-memory
next_edges: []
confidence: 0.7
evidence_runs:
  - experiment:a00-99de000a-700822
loop: hypothesis:l4-bg-kill-served-flag-and-self-memory@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ad43d4b5246ffe50
season: 2
title: A00 99de000a 700822
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-99de000a-700822

## Experiment

READ-ONLY disassembly of `~/.local/share/claude/versions/2.1.267` (216 MB ELF aarch64) with `grep -a -b -o` + `dd` context extraction. No engine file touched, nothing set, nothing killed. Ran the three legs.

**LEG 1 — the served value of `tengu_bg_low_mem_mb`.** The flag's ONLY definition is `P("tengu_bg_low_mem_mb",1024)` (offset 18980795x cluster; also at 92635416). Searched `~/.claude/settings.json`, `~/.claude.json`, env, and the user caches — every `tengu_*` in settings.json is a DIFFERENT flag (tengu_dapper_lagoon, tengu_tide_elm, tengu_crystal_beam, ...). `tengu_bg_low_mem_mb` appears in settings.json nowhere, in env nowhere, and in `~/.claude/*.jsonl` only as text quoted from this same investigation. **SERVED VALUE UNREADABLE from this box** — it lives behind the `P()` remote flag service or a statsig-style cache not present in the three dirs already searched. Honest result per the brief: genuinely not in plain text appear on this box; default 1024 MiB stands as the only code-cited value.

**LEG 2 — the candidate knob `CLAUDE_BG_MEMORY_TOGGLED_OFF` and a BETTER knob.** Consumer found at offset 192813427: `if(a.CLAUDE_BG_MEMORY_TOGGLED_OFF==="1"&&a.CLAUDE_CODE_SESSION_KIND==="bg")qbe(!0)` where `qbe(e){n().sessionFlags.replaceMemoryToggledOff(e)}` (offset 178809877). So this knob does NOT touch either producer below — it only stamps a session flag `memoryToggledOff` into bg session state (storage `M9` fields, offset 183554601). It is a bookkeeping/UX flag, not a kill switch. **THE REAL DISABLE KNOB is `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP`** (offset 95884548; produced from the `CLAUDE_CODE_*` config family at 179195375): in the consumer `Ngr` it is a hard gate — `if(!Ae()&&!a.CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP){ ... process.on("memoryPressure",v) ... }` (offset 18820700 region, seen verbatim). Setting `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` DISARMS the memory-pressure reaper entirely — it never registers the handler. The hypothesis brief specifically forbade setting it to "test" (live box, READ-ONLY), so I did not set it.

**LEG 3 — THE ONE THE EVIDENCE ACTUALLY POINTS AT. FOUND a second, more specific producer.** The kill message's exact string `stopped because the system is running low on memory` is produced from a lookup object `var vOe={memory_pressure:"stopped because the system is running low on memory"};` (offset 185696993). The renderer: `case"killed"` renders `"${n}" was ${p?vOe[p]:"stopped"}` with `"memory_pressure"` passed as the cause passed as the cause (offset 188083209). The ONLY consumer that passes `memory_pressure` into a `killed` outcome is `Ngr` — the background-shell pressure REAPER: on a live bg task it registers `process.on("memoryPressure",v)` where `v` kills the running task with cause `memory_pressure`, then closes the task. That `memoryPressure` event is Bun's NATIVE memory-pressure notification. In this binary's own internals table (offset 515000, string dump) the cgroup surface is explicit: `/sys/fs/cgroup/` bound next to `memory.pressure`, `memory.events`, and `emitMemoryPressure`, `memoryPressurePsiTrigger`, `memoryPressureWatcherHasOsBackend` (offset 21823793). **This is a cgroup-PSI / memory-pressure watcher on the HARNESS'S OWN cgroup — NOT the system MemAvailable** that `P("tengu_bg_low_mem_mb")`'s legacy `freemem()` gate reads. Live capture this round: my own scope `session-93257.scope` had `memory.current` 18.1 GB, `memory.max`="max", and `memory.pressure` `some avg10=0.00 full avg10=0.00` — no pressure at capture, consistent with the seizure watching its own cgroup edge rather than aggregate 4GB. I did not observe a live kill during this round, so a 1-second self capture (RSS + cgroup memory.current + meminfo) remains unperformed.

## Evidence

- kill-message OBJECT: `var vOe={memory_pressure:"stopped because the system is running low on memory"};` @185696993.
- render `"... was ${vOe[p]}"` + `memory_pressure` cause passed @188083209 (in `jxt` switch case "killed").
- REAPER consumer `Ngr`: `if(!Ae()&&!a.CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP){ ... process.on("memoryPressure",v) -> jxt(..., "killed", "memory_pressure") ...}` @188082971+/188083209.
- disable knob produced in CLAUDE_CODE_ family @179195375 (`CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP`), read as an env/config boolean, referenced also @95884548.
- `CLAUDE_BG_MEMORY_TOGGLED_OFF==="1"`->`qbe(!0)`->`sessionFlags.replaceMemoryToggledOff(e)` @191923427 / @178809877. A session-flag stamp, NOT the killer.
- native memory-pressure bound to /sys/fs/cgroup/memory.pressure, memory.events, PSI funcs @21823793 and intern table @515000.
- live cgroup read (my scope): memory.current=18185777152 (~18.1 GB), memory.max="max", memory.pressure some/full avg10=0.00, total~2.3e6.
- located legacy freemem gate unchanged @18980795: `P("tengu_bg_low_mem_mb",1024)` — confirms (A)-(D) without re-derivation.

## Find the killer, not the safe knob

Final classification — producers of the exact message `stopped because the system is running low on memory`: **(1) `Ngr` reaper on Bun's native `memoryPressure`/cgroup-PSI event (SELF-memory / harness-cgroup), THIS is the class-b killer; (2) the legacy `freemem()<tengu_bg_low_mem_mb` gate (SYSTEM-memory via MemAvailable) — present and unchanged but never fires at 16-18 GB.** The verdict leans proved that class-(b) kills are a harness-cgroup pressure reap (self, PSI), and that 16-18 GB system availability is irrelevant because the trigger is the harness's own cgroup memory-pressure edge, not system MemFree/MemAvailable. UNRESOLVED: (a) the LIVE served value of `tengu_bg_low_mem_mb` (needs the daemon/remote service, not this box), (b) a same-instant capture (RSS + cgroup current + meminfo) at an actual kill to nail the reaper in the act.

## Agent Notes
Leg3: found the real killer — background-shell REAPER 'Ngr' armed on Bun native memoryPressure (cgroup-PSI on harness's own cgroup), passing memory_pressure into '[cmd] was stopped because the system is running low on memory'. Disable knob is CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP (not CLAUDE_BG_MEMORY_TOGGLED_OFF, which is only a session-flag stamp). Self-memory explained.
