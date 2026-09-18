---
id: experiment:a00-100e3671-735bc3
mint_id: 327f79b724e54c2c82bec99eae9e84be
type: experiment
parents:
  - hypothesis:l4-a-named-env-key-reaches-a-spawned-kid-through-a-config-forward-env-list-read-from-the-main-env-at-spawn-never-a-literal-never-the-dispatcher-environ
next_edges: []
confidence: 0.88
edited_by: a00-100e3671
evidence_runs:
  - experiment:a00-100e3671-735bc3
line_ceiling: 40
loop: hypothesis:l4-a-named-env-key-reaches-a-spawned-kid-through-a-config-forward-env-list-read-from-the-main-env-at-spawn-never-a-literal-never-the-dispatcher-environ@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 51
profile: balanced
role: kid
scaffold_hash: 0c2bb277f5130e02
season: 2
title: Forward a config forward_env NAME list from the MAIN .env into every spawned kid env (one adapter child_env seam)
town: core
verdict: inconclusive_lean_proved:88
---
<!-- BODY:BEGIN -->
# experiment:a00-100e3671-735bc3

## Experiment

g15 BUILD ORDER, not a measurement: reproduce enough to prove the gap, then
implement the fix. Measured first on the pre-fix bytes (by symbol, not line):

  - `extensions/agi/bin/adapters/pi_adapter.py::child_env` was
    `env = {**base, **{k: str(v) for k, v in extra.items()}}` -- `harness["env"]`
    LITERALS only, merged over `dispatch.scrubbed_env()`. No `.env` read.
  - `envfile.read_env` had no caller on the spawn path
    (`grep -rn 'read_env' extensions/agi/bin` -> envfile.py + tests only).
  - `dispatch.scrubbed_env()` is the DISPATCHER environ minus
    `ENV_VARS_TO_SCRUB`. driver.sh sources the MAIN `.env` with `set -a`, so a
    driver-dispatched kid already inherits those keys; a POST-SESSION director
    round (shell never sourced) does not. That is the gap.
  - Result: `harnesses.<h>.forward_env` did not exist; `TYPESAFE_KEY` in the
    MAIN `.env` was invisible to every parent/kid.

## Fix (ONE seam, every adapter)

`harnesses.<h>.forward_env: [NAMES]` -- names only, never values. New
`adapters.forward_named_env(env, harness)` reads each named key from the
MAIN-root `.env` (`envfile.resolve()` climbs through
`locations.shared_project_root`, so a worktree never reads its own `.env`) and
injects it into `env`. Every adapter's `child_env` now returns
`adapters.forward_named_env(adapters.drop_unneeded_credential(env, harness), harness)`
-- the same one-function-every-adapter shape as `drop_unneeded_credential`, so
main dispatch, the dry-run mirror AND adapter `restart` all reach it. Editing
only `dispatch.py` was the near miss the brief named; it is not needed at all.

Rules honoured:
  - ADDS, never removes: a name already in `env` (the dispatcher environ, or a
    `harness['env']` literal) is left byte-identical. driver.sh kids keep
    every key they get today; `harness.env` literals keep today's merge order.
  - A listed name absent from `.env` is skipped with ONE named notice on
    stderr -- no exception, no partial env.
  - `forward_named_env` registers each injected NAME in
    `adapters._FORWARDED_NAMES`; `dispatch._looks_like_secret` consults it, so
    `_redact_env_map` redacts the value in `spawn.json` even when the name has
    no KEY/TOKEN/SECRET/PASSWORD substring (the name-shape half alone would
    leak it).

No config change: `forward_env` is optional and absent from this project's
`.agi/config.json` (left alone -- shared file, merge hazard).

## Evidence

`python3 -m pytest extensions/agi/tests/test_dispatch_forward_env.py -q`
-> 9 passed (test 1 parametrised over pi/claude_code/copilot_cli; 2 absent-name
notice; 3 environ key preserved; 4 literal still merges and wins; 5 value
redacted under a non-secret-shaped name; 6 shell-never-sourced still reaches
the child).

`python3 -m pytest extensions/agi/tests/ -q -k 'dispatch or adapter'`
-> 377 passed, 5134 deselected.

Production lines measured `git diff --numstat` (read-only): 51 added over the
five production files; `line_ceiling` 40, so 1.28x -- recorded, not re-briefed
(below the 2x stop line). Test file excluded.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version. The brief offered `dispatch.py` or the adapter seam; I put the
resolver in the adapter seam (`forward_named_env`, called from every
`child_env`) because that is the one place main dispatch, the dry-run mirror
and adapter `restart` all funnel through -- the exact precedent
`drop_unneeded_credential` set when two ad-hoc pops in dispatch.py left the
restart path leaking a key. Putting it only in dispatch.py would have looked
correct on the main path and silently missed restarts, which is the near miss
the brief named aloud.

Two judgement calls, both recorded here because the claim does not dictate
them:

  1. ADDS, never OVERWRITES. When a listed name is already in `env` (the
     dispatcher environ, or a `harness['env']` literal) the existing value is
     kept. The brief says forward_env never REMOVES a passthrough key and that
     literals keep today's behaviour; "literal wins over forwarded" is what
     test (4) pins. A same-value refresh from `.env` would be a behaviour
     change on the driver.sh path with no claim asking for it.
  2. The scrubber registration is a process-global set
     (`adapters._FORWARDED_NAMES`) rather than a parameter threaded into
     `_redact_env_map`. The registry is populated by the same call that
     injects the value and read at spawn.json time in the same process, and it
     avoids changing `_looks_like_secret`'s signature for a fact only the
     forwarder knows. The test clears it around each case so the global cannot
     make a case pass vacuously.

The notice goes to stderr and names the key and the `.env` path it looked in;
a skip is loud but never fatal, per the claim's (c) falsifier.
<!-- THOUGHT:END -->

## Agent Notes
Built harnesses.<h>.forward_env: ONE seam adapters.forward_named_env called from every adapter child_env reads MAIN-root .env names (envfile.resolve -> shared_project_root), adds never removes, skips an absent name with one notice, registers injected names with dispatch._looks_like_secret for spawn.json redaction; 9 new tests + 377 spawn-path tests green; 51 production lines vs 40 ceiling (1.28x, recorded not re-briefed).
