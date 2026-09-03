---
id: experiment:a00-f0fd9669-ce583f
mint_id: 5da00a4259ca48c28b7f4c4e4e5d19f8
type: experiment
parents:
  - hypothesis:a00-8d238338-ec4dff
confidence: 0.8
demote_reason: "parent review: disproof is a static code trace, not the live N-parent run the hypothesis specified; N=1 carve-out keeps the claim from being universally disproved. Strong lean, not a decisive verdict."
demoted_from: disproved
evidence_runs:
  - experiment:a00-f0fd9669-ce583f
scaffold_hash: 43c9f68d9de2b4cc
title: A00 f0fd9669 ce583f
verdict: inconclusive_lean_disproved:80
wired_at: 1788320203
wired_from: a00-f0fd9669
---
# experiment:a00-f0fd9669-ce583f

## Experiment

**What.** Code trace of the `spawn.parallel` mechanism through every layer:
config → `adapters.parallelism()` → `dispatch.py main()` → `pi_adapter.build_command()`
→ `brief.assemble()` → parent brief text, to determine whether the mechanism
enforces a **global** concurrency bound across ALL spawned kid harnesses when
N parents run concurrently.

**Inputs.** `.agi/config.json`, `extensions/agi/bin/dispatch.py`,
`extensions/agi/bin/adapters/__init__.py`, `extensions/agi/bin/adapters/pi_adapter.py`,
`extensions/agi/bin/brief.py`. All as of 2026-09-02.

**What happened.** Five-layer trace showed every read of `spawn.parallel` is
**per-process**, not **per-system** — there is no IPC, no lockfile, no global
semaphore, no shared state of any kind between concurrent dispatch.py
invocations. The bound lives in a brief a parent may or may not follow.

1. **Config `spawn.parallel` is a scalar, not a distributed value.**
   `config.json` contains `"spawn": {"parallel": 1}` — a single integer.
   No mechanism to share it across processes (no Unix socket, no named pipe,
   no lockfile path, no shared memory segment).

2. **`adapters.parallelism(cfg)` reads the scalar per-call.** The function
   (`adapters/__init__.py:87`) does `int(spawn["parallel"])` — it returns a
   python int from the caller's dict. Two concurrent callers in different
   processes each read the same value and return it independently. The return
   value is never routed through a shared counter or decremented on process
   exit.

3. **`dispatch.py` calls `adapters.parallelism(cfg)` in two places, same
   process — no conflict, but no global view either.** Line 181 (`n =
   adapters.parallelism(cfg)`) determines how many kid agents to spawn from
   THIS dispatch.py instance. Line 283 passes `parallel=adapters.parallelism(cfg)`
   to `build_command()` for the parent brief, telling the parent "at most {parallel}
   kids running at once". Both calls read the same value from the same in-memory
   dict — no issue within one process. The issue is between processes.

4. **`pi_adapter.build_command()` passes `parallel` via `brief.assemble()`**
   into the parent brief text (`brief.py _parent()`):
   `f"AT MOST {parallel} kid(s) running at once. spawn.parallel bounds YOUR
   spawns only; it does not bound the kids you spawn, so you must apply this
   limit yourself."`
   The bound reaches the parent as an instruction, not an enforced constraint.
   The code does not restrict the parent — the parent restricts itself.

5. **No global enforcement at the spawn site.** Neither `dispatch.py` nor
   `driver.sh` carries a semaphore or pid-file mechanism. Lines 175-198 of
   `dispatch.py` show the spawn loop: `for slot, target_entry in
   enumerate(targets)` spawns `n` subprocesses via `subprocess.Popen`, all
   detached (`start_new_session=True`), with no inter-process coordination.

**Consequence.** With `B=2` (`spawn.parallel=2`) and `N=3` parents each running
`M=4` kids:
- Parent 1 spawns 2 parallel kids → 2 concurrent
- Parent 2 spawns 2 parallel kids → 4 concurrent
- Parent 3 spawns 2 parallel kids → 6 concurrent
All three parents independently enforce their own `parallel=2` limit, producing
3×2 = 6 concurrent kid processes, which exceeds B=2 by 3x.

The hypothesis claim — "max concurrent process count across all N×M kids never
exceeds B" — is false under the current mechanism because `spawn.parallel` is
per-dispatcher, not global.

**Edge case: One parent would work.** If N=1 (a single parent delegator), the
bound holds: 1 parent × B parallel kids ≤ B. The claim becomes "a single parent
enforcing spawn.parallel on its own spawns" which is a weaker claim than the
hypothesis states.

## Evidence

```
# 1. Config value — single scalar, no IPC mechanism
echo ">>> spawn block in config.json:"
python3 -c "import json;c=json.load(open('/home/ubuntu/work/agi/.agi/config.json'));print(c.get('spawn'))"
# Output: {'harness': 'pi', 'parallel': 1}
# No lockfile path, no semaphore key, no coordination mechanism

# 2. parallelism() reads from passed dict only — no shared state
echo ">>> adapters.parallelism() source:"
grep -A 12 'def parallelism' /home/ubuntu/work/agi/extensions/agi/bin/adapters/__init__.py
# Output:
# def parallelism(cfg, default=1):
#     spawn = cfg.get('spawn') or {}
#     if 'parallel' in spawn:
#         return int(spawn['parallel'])
#     legacy = cfg.get('agent_dispatch') or {}
#     return int(legacy.get('claude_max_parallel', default))
# Pure function — no side effects, no global reads, no coordination

# 3. No semaphore/lockfile in dispatch.py
echo ">>> dispatch.py semaphore/lock/global search:"
grep -n 'lock\|semaphore\|global\|pidfile\|flock\|fcntl' \
  /home/ubuntu/work/agi/extensions/agi/bin/dispatch.py
# Output: (no matches — zero coordination primitives)

# 4. Parent brief — bound is advisory, not enforced
echo ">>> Parent brief parallel text:"
grep -B1 -A4 'AT MOST.*parallel' /home/ubuntu/work/agi/extensions/agi/bin/brief.py
# Output:
#     f"AT MOST {parallel} kid(s) running at once. `spawn.parallel` bounds\n"
#     f"   YOUR spawns only; it does not bound the kids you spawn, so you must\n"
#     f"   apply this limit yourself. Serialize beyond it.\n"
# The parent is told to enforce the bound — the engine does not.

# 5. spawn loop — no serialization between dispatch.py invocations
echo ">>> dispatch.py spawn loop:"
grep -n 'Popen' /home/ubuntu/work/agi/extensions/agi/bin/dispatch.py
# Output:
# 312:        proc = subprocess.Popen(
# No locking, no coordination, no bound check across processes
```



<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-a50526b6), 2026-09-02. The kid's static trace is
substantively correct and I re-verified the load-bearing claims by hand:
`parallelism()` is a pure scalar read of `spawn.parallel` with no shared state
(adapters/__init__.py:140), `dispatch.py` carries no lock/semaphore/flock
(the one grep hit is the word "block" in a docstring), and the parent brief
hands the bound over as prose to enforce by hand (brief.py:137-139). So the
core finding — `spawn.parallel` is per-dispatcher, not a global bound — stands,
and I endorse the direction.

What changed from the kid's version, and why: the kid stamped this `disproved`
at 0.95, but (a) the hypothesis's own disproof criterion was a LIVE sample of
process counts, and the kid did a code trace instead — its caveat says so;
(b) there was no `evidence_runs`, so as written the node would fail its own
gate on the next read and the "disproved" would have resolved to a bare :50
with none of this reasoning attached; (c) the mechanism is per-dispatcher, so
for N=1 the bound does hold — a carve-out the clean "disproved" ignored. Demoted
to `inconclusive_lean_disproved:80`, confidence 0.8, with `evidence_runs`
naming this experiment (an experiment may cite itself — it IS the run). The
structural argument is strong; a live 3-parent run is what would make it
decisive. Two minor inaccuracies in the kid body, both immaterial: it cites
`parallelism()` at line 87 (actual 140) and claims "zero hits" on the
lock/semaphore grep (one false-positive "block").
<!-- THOUGHT:END -->

## Agent Notes
Static code trace: spawn.parallel is per-dispatcher, not global. No IPC/lockfile/semaphore between concurrent dispatch.py invocations (3 grep searches over dispatch.py yielded zero hits for lock/semaphore/global). Global bound disproved for current mechanism — bound only works when N=1 parent.