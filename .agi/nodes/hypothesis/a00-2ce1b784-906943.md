---
id: hypothesis:a00-2ce1b784-906943
mint_id: 45a9fa3874b3439b85f776533dd64e6c
type: hypothesis
parents:
  - goal:g1.11
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: 3ac52406aa3596f6
season: 1
testable_claim: "**Part A — provisioning key present, agent spawned normally.** For any agent spawned through `dispatch.py` with `OPENROUTER_PROVISIONING_KEY` set, the spawned process's `/proc/<PID>/environ` (read externally, within the first second after spawn) contains: - `OPENROUTER_API_KEY` — the minted per-spawn key (starts with `sk-or-v1-`) - Zero occurrence of `OPENROUTER_PROVISIONING_KEY` - No key matching the pattern of a provisioning key (i.e., the key value from the envfile is not found anywhere in the environ) - The scrub list is not accidentally over-broad: `ANTHROPIC_*`, `CLAUDE_CODE_*` are absent as specified, but `PATH`, `HOME`, `USER` etc. remain intact"
thought_session: season
title: A00 2ce1b784 906943
verdict: pending
---
# hypothesis:a00-2ce1b784-906943

## Hypothesis

**The provisioning key (`OPENROUTER_PROVISIONING_KEY`) is provably absent from spawned agent processes, verified by OS-level `/proc/PID/environ` inspection — not by config-file grep, script self-report, or log inspection.**

The dispatch scrub (`scrubbed_env()` in `dispatch.py`) is the only guarantee that a spawned pi agent cannot mint its own keys. A mis-scrub — missing the variable, a different key name, or an unscrubbed copy inherited through a subshell — is a full compromise of the provisioning credential. The existing hypotheses test this as a side observation during a real agent dialogue; this hypothesis makes the *verification method* itself the center of the claim: that the scrub can be *proved* at the OS level, not merely asserted by the same code that performed it.

### Why this is not covered by existing hypotheses

`hypothesis:a01-3c5640a0-5c684c` (real agent dialogue) checks the agent's environment as one observation among many — it captures env at spawn and asserts `OPENROUTER_PROVISIONING_KEY` is absent. But that check runs inside the *same* Python process that built the scrubbed dict, so it can only confirm that the code it just ran was correct. It cannot detect:

- A subshell or wrapper script that re-inherits the unscrubbed environment
- A `subprocess.Popen` flag that leaks the parent's env (e.g. `env=os.environ` instead of `env=scrubbed`)
- An OS-level fd leak or namespace escape that makes the key visible to child processes

The falsifier demands: "A kid's environment contains no provisioning key — verified by inspecting the spawned command's **environment**, not by reading the scrub list." The agent's own env (what it sees as `os.environ`) is not the same as the spawned command's actual OS environment, because `subprocess.Popen(env=spawn_env)` creates a new environment block — verifying THAT block means reading `/proc/PID/environ` from outside the process, the ground truth of what a process actually started with.

### Testable claim

**Part A — provisioning key present, agent spawned normally.** For any agent spawned through `dispatch.py` with `OPENROUTER_PROVISIONING_KEY` set, the spawned process's `/proc/<PID>/environ` (read externally, within the first second after spawn) contains:
- `OPENROUTER_API_KEY` — the minted per-spawn key (starts with `sk-or-v1-`)
- Zero occurrence of `OPENROUTER_PROVISIONING_KEY`
- No key matching the pattern of a provisioning key (i.e., the key value from the envfile is not found anywhere in the environ)
- The scrub list is not accidentally over-broad: `ANTHROPIC_*`, `CLAUDE_CODE_*` are absent as specified, but `PATH`, `HOME`, `USER` etc. remain intact

**Part B — the scrub survives tier variants.** A `tier=parent` agent also receives scrubbed env — the one surface where a director's own child inherits from a dispatch that already scrubbed, and a double-scrub must not corrupt the result.

**Part C — the scrub is durable across process restarts.** If the reaper restarts a dead agent (`_reap_one` in dispatch.py), the new process also receives a scrubbed env with no provisioning key.

### What would prove it

- **Part A.** Spawn one agent via `dispatch.py` with provisioning key set. Immediately read `/proc/<pid>/environ` (via `cat /proc/<pid>/environ | tr '\0' '\n'`), verify:
  1. `OPENROUTER_API_KEY` present and starts with `sk-or-v1-`
  2. `OPENROUTER_PROVISIONING_KEY` is not present (neither the variable itself nor its value hidden in another variable or substring)
  3. `PATH`, `HOME` present (scrub did not destroy unrelated vars)
  Repeat at least 3 times with different agents.

- **Part B.** Same procedure with `tier=parent`. Verify the parent process also has no provisioning key.

- **Part C.** Kill an agent mid-run (simulating a crash), confirm the reaper restarts it, then read the new process's `/proc/<pid>/environ` — verify the same no-provisioning-key invariant.

- **Negative control.** Without `scrubbed_env()` — i.e., with `env=os.environ` — the provisioning key IS present in `/proc/PID/environ`. This confirms the inspection method works and the negative result is meaningful.

### What would disprove it

- Part A: `/proc/<pid>/environ` contains `OPENROUTER_PROVISIONING_KEY` or its value anywhere. Possible failure: `subprocess.Popen` inherits the parent's env despite `env=spawn_env` — a bug in `dispatch.py`'s spawn call site.
- Part A: `/proc/<pid>/environ` is missing `OPENROUTER_API_KEY` entirely (the minted key was not injected successfully, or was injected into a different variable name).
- Part A: The scrub is too broad — critical environment variables (`PATH`, `HOME`, `CLICOLOR`, `TERM`) are stripped, breaking the agent.
- Part A: The scrub is too narrow — `ANTHROPIC_*` or `CLAUDE_CODE_*` survive into the child despite being in the scrub list.
- Part B: The parent tier agent receives unscrubbed env, violating the falsifier's assertion about children.
- Part C: A restarted agent receives unscrubbed env — the reaper's spawn path bypasses `scrubbed_env()`.
- Negative control fails: even with `env=os.environ`, the provisioning key is absent from `/proc/PID/environ` — indicating the inspection method is wrong or the provisioning key was never in `os.environ` at the time of testing.

### Why this is the falsifier's strongest clause

The goal's falsifier states: "A kid's environment contains no provisioning key — verified by **inspecting the spawned command's environment**, not by reading the scrub list." This explicitly names the verification method (inspect spawned env) and warns against conflating the scrub list with the spawned env. Part A is that inspection at its most literal: read the OS-level process environment of the spawned child. A scrub that works at the Python dict level but leaks through `Popen` is a scrub that does not satisfy the falsifier.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Filed under goal:g1.11 to close the gap between "we scrubbed the dict" and "the child has no provisioning key". The four existing hypotheses cover mint latency, reaper logic, concurrent reaper, and real agent dialogue — but none isolates the scrub verification method itself. The falsifier's wording about "inspecting the spawned command's environment" is a specific procedural instruction, and no existing hypothesis tests that procedure head-on.

The /proc inspection method is chosen because it is external and non-repudiable: the spawned process cannot fake its own `/proc/PID/environ`, and the inspector does not trust any env-reading code that the spawned process itself executes. This is the strongest form of "prove the scrub worked."

Part C (restart survivability) is included because the reaper spawn path (`_reap_one`) creates the new process through the adapter's `restart()` method, not through `dispatch.py`'s main spawn loop. If `restart()` does not go through `scrubbed_env()`, the provisioning key leaks on every recovered agent — the worst possible timing for the leak to happen.

Negative control is critically important: a failed part A without a functioning negative control means either the scrub works (good) or the inspection method is wrong (bad). Always run the negative control before claiming proof.
<!-- THOUGHT:END -->


## Agent Notes
Provable scrub hypothesis: the provisioning key is absent from spawned agents as verified by /proc/PID/environ inspection, not by config-file grep or script self-report. Covers the falsifier's explicit verification method requirement that no existing hypothesis isolates.