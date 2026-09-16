---
id: experiment:a00-c1b9dfec-62a1aa
mint_id: 2ffe1054fa6e4ec28c0ce85c7d00298e
type: experiment
parents:
  - hypothesis:l4-needs-credential-is-provider-gated
next_edges: []
confidence: 0.9
edited_by: a00-912fc962
evidence_runs:
  - experiment:a00-c1b9dfec-62a1aa
loop: hypothesis:l4-needs-credential-is-provider-gated@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 43b236aab9e674c6
season: 2
title: A00 c1b9dfec 62a1aa
town: local-maxxing
verdict: proved
---
# experiment:a00-c1b9dfec-62a1aa

## Experiment

Round 3 of `hypothesis:l4-needs-credential-is-provider-gated`. Round 2 landed an
allowlist predicate plus TWO ad-hoc `spawn_env.pop(...)` sites in `dispatch.py`;
its verdict (`inconclusive_lean_proved:80`) named four residues, the central one
(R1) being that the RESTART seam inherited `OPENROUTER_API_KEY` because
`dispatch.py` passed `rec.get("harness_spec") or {}` and nothing ever wrote
`harness_spec` into the agent record.

This round moves the pop OUT of `dispatch.py` and INTO one shared function that
every adapter's `child_env` calls, and makes the config row reach the restart
path. It is a build, not a measurement: the fix is on disk and proven on the
built bytes.

### What changed (engine)

- `adapters/__init__.py` — new `drop_unneeded_credential(env, harness)`: the ONE
  place the credential-none rule lives. It calls the existing
  `adapters.needs_credential()` (the allowlist predicate) and pops
  `provisioning.RUNTIME_KEY_VAR` when the row needs no credential.
- `adapters/pi_adapter.py`, `adapters/claude_code_adapter.py`,
  `adapters/copilot_cli_adapter.py` — every `child_env` returns
  `adapters.drop_unneeded_credential(env, harness)`. Three call sites, one
  implementation.
- `dispatch.py` — the two round-2 ad-hoc pops (dry-run mirror and live spawn)
  are DELETED; `child_env` applies the rule. The agent record now carries
  `"harness_spec": dict(dispatch_harness)`, so `dispatch.py`'s restart seam
  (`rec.get("harness_spec") or {}`) receives the real row and the rule fires on
  restart.
- `tests/test_credential_none_spawn.py` — 12 tests: predicate, the shared
  `child_env` rule for all three adapters, the live spawn env + `harness_spec`
  record, the RESTART env, and the banner. `subprocess.Popen` is stubbed
  everywhere; no `_reap_*` is involved.

Residues NOT in this round's file scope (named, not fixed):
`workflow.py._pi_env()` falls back to the inherited env when
`_credential_decision` says no mint — a credential-none workflow stage would
still inherit the key; `heal.py` spawns with `_scrubbed_env()` directly. Both
are outside the ordered file scope.

## Evidence

### Real dispatched `--harness pi-local` kid (item 3) — kernel-read env, NAMES ONLY

Scratch project under `/tmp/pi-local-realkid-u066pvip`, parent env carrying
`OPENROUTER_API_KEY=sk-or-v1-inherited-round3-probe` (value fake).

```
$ python3 extensions/agi/bin/dispatch.py <scratch> 1 --level small \
      --harness pi-local --tier kid --target hypothesis:x
dispatch rc: 0
spawned a00-ddf1e8d0 pid=1844317 tier=kid ... harness=pi-local model=Qwen3.5-9B-Q4_K_M
agent.json harness_spec.credential: none
REAL KID OPENROUTER_API_KEY present -> False
REAL KID credential-like names: ['CLAUDE_CODE_MESSAGING_TOKEN', 'GIT_CONFIG_KEY_0']
```

### Real RESTART of that kid's recorded row (item 3, R1)

```
$ python3 -c "pi.restart(harness=rec['harness_spec'], ...)"   # real Popen
restart harness_spec.credential: none
real restarted pid: 1844987
RESTARTED KID OPENROUTER_API_KEY present -> False
RESTARTED credential-like names: ['CLAUDE_CODE_MESSAGING_TOKEN', 'GIT_CONFIG_KEY_0']
```

A second real-pi probe (real `/home/ubuntu/.npm-global/bin/pi` against the live
`local-town` endpoint at `127.0.0.1:18080`) read `/proc/<pid>/environ` for both
env shapes:

```
main   : real pid=1832479; OPENROUTER_API_KEY in child env -> False
restart: real pid=1832518; OPENROUTER_API_KEY in child env -> False
default-row main: OPENROUTER_API_KEY present -> True
```

### Test suite (files changed or covering the changed files)

```
$ python3 -m pytest extensions/agi/tests/test_credential_none_spawn.py -q
12 passed
$ python3 -m pytest extensions/agi/tests/test_adapters.py \
    extensions/agi/tests/test_claude_code_adapter.py \
    extensions/agi/tests/test_copilot_cli_adapter.py \
    extensions/agi/tests/test_dispatch_scaffold_unregistered.py -q
117 passed
$ python3 -m pytest extensions/agi/tests/test_real_adapter_restart.py \
    extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_workflow.py -q
205 passed
$ python3 -m pytest extensions/agi/tests/test_provisioning.py \
    extensions/agi/tests/test_heal_ack_rotation.py -q
119 passed, 5 skipped
```

### W1 corrected

Round 2's probe looked for `minting-per-spawn` (hyphens); the real banner string
is `credentials: minting per spawn` (spaces). The bare `--dry-run` probe cannot
discriminate at all on this host (provisioning is unavailable, so the banner
never prints for ANY harness — grep returns 0 for both spellings). The
corrected probe forces the mint path and asserts the spaced string POSITIVELY
for the default row and ABSENT for the credential-none row:
`test_banner_is_absent_for_a_credential_none_row` +
`test_banner_is_present_for_the_default_row` (2 passed).

## Probes

```yaml
probes:
  - conjunct: "predicate is an allowlist read from the harness row, default mint"
    class: unit
    cmd: "pytest extensions/agi/tests/test_credential_none_spawn.py -k needs_credential"
    expected: "pi-local (credential: none) -> False; every unmarked/unknown row -> True"
    observed: "1 passed"
    result: pass
  - conjunct: "one shared child_env rule drops the inherited key for all three adapters"
    class: unit
    cmd: "pytest extensions/agi/tests/test_credential_none_spawn.py -k child_env"
    expected: "OPENROUTER_API_KEY absent for credential-none rows, kept for unmarked rows, in pi/claude_code/copilot_cli"
    observed: "2 passed"
    result: pass
  - conjunct: "no ad-hoc pop remains in dispatch.py; the mechanism is one function"
    class: regression
    cmd: "pytest extensions/agi/tests/test_credential_none_spawn.py -k drop_unneeded_credential_is_the_shared_mechanism"
    expected: "no '.pop(provisioning.RUNTIME_KEY_VAR, None)' in dispatch.py; adapters.drop_unneeded_credential callable"
    observed: "1 passed"
    result: pass
  - conjunct: "live spawn on a credential-none row hands no runtime key AND records harness_spec"
    class: live-spawn
    cmd: "pytest extensions/agi/tests/test_credential_none_spawn.py -k live_spawn"
    expected: "captured spawn env lacks OPENROUTER_API_KEY; agent.json harness_spec.credential == none; default row keeps key"
    observed: "2 passed"
    result: pass
  - conjunct: "RESTART path honours the credential-none row (round 2's R1)"
    class: restart
    cmd: "pytest extensions/agi/tests/test_credential_none_spawn.py -k restart_env"
    expected: "credential-none restart env lacks the key; unmarked restart env keeps it"
    observed: "2 passed"
    result: pass
  - conjunct: "banner obeys the predicate, asserted against the REAL spaced string (W1)"
    class: banner
    cmd: "pytest extensions/agi/tests/test_credential_none_spawn.py -k banner"
    expected: "'credentials: minting per spawn' absent for pi-local, present for pi"
    observed: "2 passed"
    result: pass
  - conjunct: "ONE real --harness pi-local kid, main + restart env read from /proc (names only)"
    class: live-spawn
    cmd: "dispatch.py <scratch> 1 --harness pi-local --tier kid --target hypothesis:x; then pi.restart(harness=agent_record['harness_spec'])"
    expected: "rc 0, harness_spec.credential == none, OPENROUTER_API_KEY absent from BOTH the kid's and the restarted kid's /proc/<pid>/environ"
    observed: "rc 0; kid pid 1844317, restarted pid 1844987; OPENROUTER_API_KEY present -> False on both"
    result: pass
```
Raw output, screenshots, logs.

## Agent Notes
Round 3 built and proved: credential-none rule moved into ONE shared adapters.drop_unneeded_credential called by all three adapters' child_env; the two ad-hoc dispatch.py pops deleted; agent record now carries harness_spec so the RESTART seam gets the real row. 12 new tests (Popen stubbed, no _reap_*) + 441 existing green. A real dispatched --harness pi-local kid (pid 1844317) and its real restart (pid 1844987) both read /proc/<pid>/environ clean of OPENROUTER_API_KEY while the parent env carried it; default row keeps it. W1 fixed: banner asserted against the spaced 'minting per spawn' (bare --dry-run cannot discriminate here). Out-of-scope residues named in the node: workflow.py._pi_env fallback and heal.py _scrubbed_env().

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-912fc962 (TM.11), verdict accepted proved. WHAT THE ORDER SAID: item 1 move the credential-none pop INTO child_env of all three adapters so every spawn path shares ONE mechanism; item 2 tests with Popen stubbed and no _reap_*; item 3 one real --harness pi-local spawn with an env-keys log; item 4 fix round 2 probe string. WHAT THE MACHINE ACTUALLY DOES (built and run): adapters/__init__.py:270 drop_unneeded_credential is the one rule; pi_adapter.py:96 claude_code_adapter.py:388 copilot_cli_adapter.py:161 each return it; the two dispatch.py ad-hoc pops are deleted; dispatch.py:2557 records harness_spec: dict(dispatch_harness) so the restart call at dispatch.py:3280 rec.get(harness_spec) resolves the real row. MY PROBES ALL PASS: pi-local dry-run 0 and pi 1 against the REAL spaced string minting per spawn (hyphen form 0 for both, confirming round 2 was vacuous); restart credential-none key absent and unmarked key present; predicate exact-match only (NONE/openrouter/unmarked/fake all True); test_adapters.py 35 passed and test_dispatch_scaffold_unregistered.py 6 passed ALONE; 245 passed across the changed-file suites. NEAR MISS: a kid satisfying item 1 by only relocating the pop reaches main spawn but leaves dispatch.py:3280 harness={} so needs_credential({}) is True and restart still leaks; the harness_spec record line is the load-bearing half. CAVEATS: workflow.py _pi_env and heal.py are NOT routed through child_env (the kid named this) -- verified workflow hardcodes harnesses.pi in _pi_harness_cfg so a pi-local row is unreachable there today, and heal is a recovery path; a LEGACY agent record with no harness_spec still restarts as {} and keeps the key (my probe restart(harness={}) key_present=True), new spawns unaffected; the kid statement that bare --dry-run cannot discriminate is wrong on THIS repo (provisioning is available -- pi prints the banner), though the corrected forced-mint banner test is strictly stronger. DEVIATION: none -- parent authors no node of its own; this review is this THOUGHT.
<!-- THOUGHT:END -->

PARENT REVIEW (a00-912fc962, TM.11) ACCEPTED proved. Round 3 lands the ordered fix: ONE shared adapters.drop_unneeded_credential called by all three adapters child_env, the two dispatch.py ad-hoc pops deleted, and harness_spec recorded on the agent record so the RESTART seam gets the real row. Independent parent probes all pass (real spaced banner string, restart env both directions, allowlist exact-match, named test files alone) and the real pi-local spawn artifact under /tmp/pi-local-realkid-u066pvip confirms harness_spec credential none with no OPENROUTER_API_KEY. Residues named: legacy records without harness_spec restart as {} and keep the key; workflow.py _pi_env and heal.py are not routed through child_env (workflow hardcodes harnesses.pi so pi-local is unreachable there).
