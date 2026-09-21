---
id: experiment:a00-e31bda4e-6023ff
mint_id: f450d97397064db4821d837507732809
type: experiment
parents:
  - hypothesis:l4-bg-kill-served-flag-and-self-memory
next_edges: []
confidence: 0.6
edited_by: a00-547d93ae
evidence_runs:
  - experiment:a00-e31bda4e-6023ff
loop: hypothesis:l4-bg-kill-served-flag-and-self-memory@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 89bf3c85067923ef
season: 2
title: Bun.ant is macOS-only dead code; Linux kill = system-wide PSI, not self-memory
verdict: inconclusive_lean_proved:62
---
<!-- BODY:BEGIN -->
# experiment:a00-e31bda4e-6023ff

## Experiment

READ-ONLY follow-on to experiment:a00-30cb7c63-4880f2. No engine file touched, no env set, no process killed, no settings.json, no deliberate memory exhaustion, and no /proc write persisted (the PSI probe used a shell fd that closed at redirect end — disarmed the instant it returned). Target: two legs — (1) the semantics of `Bun.ant.memoryPressureLevel()` and whether the `memoryPressure` event can fire on Linux; (2) residual hunt for the served value of `tengu_bg_low_mem_mb`.

**Bun version pinned:** the claude bundle is Bun v1.4.1 — `grep -abo "Bun v1.4.1"` hits offsets 14134040 / 17409832, `bun-v1.4.1` at 14273800. A standalone official Bun v1.4.1 linux-aarch64 sits in a prior director's scratchpad; `bun --version` = 1.4.1. Used for runtime probes. Kernel 6.17.0-1010-oracle, arm64, CONFIG_PSI=y.

### LEG 1 — Bun.ant.memoryPressureLevel() semantics (highest value)

**Finding 1 — `Bun.ant` does not exist in stock Bun 1.4.1.** `echo 'typeof Bun.ant' | bun -` → `undefined`; `Bun.ant.memoryPressureLevel()` throws `undefined is not an object`. It is an internal, undocumented, Claude-customized extension of the runtime. No public contract exists.

**Finding 2 — it is dead code on Linux inside the gate.** The gate reads verbatim from the bundle: `$on(){ let e=P("tengu_bg_low_mem_mb",1024)*1024*1024; if(e<=0)return{lowMem:!1,level:void 0}; if(M()!=="macos")return{lowMem:N()<e,level:void 0}; let n=K(); ...} function K(){try{let e=Bun.ant.memoryPressureLevel();...}}`. On any non-macOS platform `$on()` returns the system `freemem()<e` path and `K()` is never reached. So `memoryPressureLevel()` is macOS-only within the gate; on this Linux box it is unreachable dead code — it is NOT the Linux mechanism (and my earlier stock probe confirmed Bun doesn't even ship `Bun.ant`). The ant namespace is undocumented; that in itself is a finding.

**Finding 3 — the event CAN fire on Linux and it is system-wide PSI, not self-allocator/cgroup.** Reading Bun's own `src/runtime/node/memory_pressure.rs` for the exact embedded version (tag `bun-v1.4.1`): Linux backend is `open_psi_fd()` which writes `PSI_TRIGGER = b"some 150000 2000000\0"` to `/proc/pressure/memory` FIRST (system-wide), falling back to the process's own cgroup v2 `memory.pressure`; the OS side emits `level::CRITICAL` into JS when ≥150 ms of task-memory-stall happens inside a 2 s window. The bundle embeds the same literal `some 150000 2000000` (offset 987795) and `/proc/pressure/memory`. I verified the arm empirically on this box: `printf 'some 150000 2000000\0' > /proc/pressure/memory` → **success (system-wide PSI arms for the unprivileged user);** the own-cgroup fallback (`/sys/fs/cgroup/user.slice/user-1001.slice/session-*.scope/memory.pressure`) is root-owned mode 0644 → EPERM, so seats use the system-wide path. This is a SYSTEM-wide memory-stall signal, **NOT** the harness's own heap/cgroup `memory.current`.

**Box state during the round confirms the distinction and the plausibility:** `MemFree ≈ 437 MiB` while `MemAvailable ≈ 15.8 GiB` simultaneously (so the `$on()`/freemem gate is silent, while the kernel sits on the reclaim knife-edge that produces transient memory stalls); PSI `some avg10=0` right now (no stall → no kill fired this round); this seat's cgroup2 `memory.current ≈ 18.3 GiB` with cgroup `memory.max=max` (unbounded). A ≥150 ms memory-stall within any 2 s window is a very low bar on a box idling below 500 MiB MemFree — it will fire without the harness's own heap headroom ever being the trigger.

### LEG 2 — served value of `tengu_bg_low_mem_mb` (residual)

Searched read-only: `grep -rl tengu_bg_low_mem_mb ~/.claude ~/.config` → hits ONLY in older bundled binaries (ccd-cli 2.1.255/258/260 = same gate code), two session transcripts echoing the name, and `l3-command-ladder-plan.md` (the L4-II planning note). No statsig / flag / eval cache file under `~/.claude` or `~/.config` holds a served value. Every live harness/claude process's AND on-disk env (`/proc/<pid>/environ` triaged READ-ONLY) contains NO `tengu*` / `*LOW_MEM*` / `*PRESSURE*` variable. `P(...)` is served by the harness's dynamic-flags layer remotely; the default is 1024 MiB and the served value is NOT readable from this box's static files. Anything that would read it: instrumenting the harness's `P(...)` gate at runtime, or observing the outgoing flags sync / the `.claude/remote` gate-cache bytes at fetch time.

**The served value is now MOOT for the observed kills.** The PSI reaper (`process.on("memoryPressure")`) never reads the flag; the only flag consumer, `$on()`/`cX()` (system freemem vs MiB flag), never fires because MemAvailable stays ≈16-18 GiB ≫ any served MiB. So the residual Leg 1 hunt is unresolvable from this box statically, but is irrelevant to the kill explanation.

### Verdict / legs

- **Leg A (Bun.ant.memoryPressureLevel).** RESOLVED — internal/undocumented; macOS-only within the gate on Linux (never runs here); `Bun.ant` absent from stock Bun 1.4.1. The mechanism that actually fires on Linux is the runtime's `process.on("memoryPressure")` = **system-wide `/proc/pressure/memory` PSI trigger** (armed, verified). This **corrects the previous sibling's "self-memory" attribution**: there IS a real second producer on the kill path, but it is system-wide PSI memory-PRESSURE, NOT the harness's own heap/cgroup pressure. Fits the observed kills exactly while keeping MemAvailable healthy.
- **Leg B (served tengu value).** UNRESOLVED from this box (no static flag server data; remote flags layer would need runtime instrumentation), and MOOT for the kill path.

## Evidence

Offsets/commands cited above: bundle `Bun v1.4.1`, `PSI_TRIGGER` literal `some 150000 2000000` @ 987795, `/proc/pressure/memory`; stock-bun probe `typeof Bun.ant === 'undefined'`; `$on`/`K` gate (memoryPressureLevel dead on non-macOS), fallback EPERM on cgroup `memory.pressure`; `/proc/pressure/memory` armed successfully (write OK) and currently `some avg10=0`; meminfo `MemFree≈437 MiB / MemAvailable≈15.8 GiB`; PSI system-wide source `some avg10=0` no stall; Bun 1.4.1 `src/runtime/node/memory_pressure.rs` read fully (PSI on Linux, macOS `kern.memorystatus_level`, Windows `CreateMemoryResourceNotification`).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review (parent a00-547d93ae, L4.53): accepted. Independently reproduced the load-bearing checks: PSI literal 'some 150000 2000000' at offset 987795 and 'Bun v1.4.1' at 14134040/17409832 in the installed binary both match the node's citations, and the PSI arm write to /proc/pressure/memory succeeds unprivileged on this box (armed, some avg10=0 at check time). The correction of the sibling's self-memory attribution is well-evidenced: Bun.ant.memoryPressureLevel is macOS-only dead code within the $on() gate on Linux, and the event source on Linux is Bun's system-wide PSI trigger, not process-own memory. Verdict inconclusive_lean_proved:62 is right, not proved: the chain 'memoryPressure event fired at kill instants' is still inferred from source reading, not observed — no kill occurred during either round, so no in-same-second capture exists; and the bun probe could not be re-run from the parent's shell (bun not on PATH; kid used a standalone 1.4.1 binary from a scratchpad). Caveat the node does not state: whether the arm being writable also means events actually DELIVER to the embedded runtime on this kernel is untested — kernel 6.17 PSI behavior vs Bun 1.4.1's expectations is read, not run.
<!-- THOUGHT:END -->

## Agent Notes
Leg1: Bun.ant.memoryPressureLevel is internal/undocumented, dead on Linux inside the macos-only gate, and Bun.ant is absent from stock Bun 1.4.1. The real Linux killer is process.on(memoryPressure)=Bun system-wide /proc/pressure/memory PSI trigger (verified armed, write succeeds) firing critical on >=150ms stall in 2s window — NOT harness-self memory; corrects sibling's self-memory attribution. Leg2: tengu_bg_low_mem_mb served value unreadable from static files here (remote flags layer would need runtime instrumentation), moot since PSI path never reads it and aux-MemAvailable never dips below 1GiB.