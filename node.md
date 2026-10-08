---
id: experiment:a00-f046ea4a-623440
mint_id: 755bfb22fe6941f6a352071aeb29e6b8
type: experiment
parents:
  - hypothesis:every-adapter-restart-spawns-from-the-scrubbed-env
next_edges: []
confidence: 0.8
edited_by: a00-301fe6aa
evidence_runs:
  - experiment:a00-f046ea4a-623440
loop: hypothesis:every-adapter-restart-spawns-from-the-scrubbed-env@s2
model: stealth/space-bunny-alpha
production_lines: 36
profile: balanced
role: kid
scaffold_hash: edbb3194157f42b1
season: 2
title: every adapter restart builds its child env from dispatch.scrubbed_env()
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-f046ea4a-623440

# experiment:a00-f046ea4a-623440

Parent claim: every adapter's `restart()` builds its child env from the same
scrubbed base as the first spawn. Measured pre-fix, fixed, re-measured.

## 1. Pre-fix wire probe (Popen stubbed, no real harness spawns)

`AGI_MODEL_SLOT_LOCK=/tmp/a-squatted.lock ANTHROPIC_API_KEY=sk-ant-squatted python3 -`
over `adapters.load(x).restart(harness=..., sess_dir=...)`, capturing `kwargs["env"]`:

| adapter | AGI_MODEL_SLOT_LOCK | ANTHROPIC_API_KEY |
|---|---|---|
| pi | `/tmp/a-squatted.lock` LEAK | `sk-ant-squatted` LEAK |
| claude_code | LEAK | LEAK |
| copilot_cli | (probe stopped at the gh-token subprocess; same `child_env(base=dict(os.environ))` line at copilot_cli_adapter.py:373) |
| grok_bot | LEAK | LEAK |

## 2. The fix -- one source, no second scrub list

| file | change |
|---|---|
| adapters/__init__.py | NEW `scrubbed_base(explicit=None)`: an explicit base from the caller wins, else a LAZY `import dispatch; dispatch.scrubbed_env()` (lazy because dispatch imports this package) |
| pi / claude_code / copilot_cli / grok_bot `_adapter.py` | `restart()` takes `base_env: dict | None = None`; the one env line reads `base=adapters.scrubbed_base(base_env)` -- no `os.environ` base left |
| dispatch.py:3633 | the reaper passes `base_env=scrubbed_env()`, the env it scrubbed for the first spawn |

`ENV_VARS_TO_SCRUB` stays the single list; nothing adapter-local was added.

## 3. Post-fix probe (all names of ENV_VARS_TO_SCRUB + the provisioning key set)

| adapter | MODEL_SLOT_LOCK | ANTHROPIC_API_KEY | ORDERS_TEXT | PROVISIONING_KEY | KEEP_ME |
|---|---|---|---|---|---|
| pi | None | None | None | None | `yes` |
| claude_code | None | `sk-ant-squatted` (by design, see 4) | None | None | `yes` |
| copilot_cli | None | None | None | None | `yes` |
| grok_bot | None | None | None | None | `yes` |

## 4. The one honest exception -- claude_code's own keys

`claude_code_adapter.child_env` re-adds `ANTHROPIC_*` / `CLAUDE_CODE_*` /
`CLAUDECODE` from the inherited env (`RESTORED_PREFIXES`, line 137) -- the CLI
needs them, and it does so on the FIRST spawn too, from the same scrubbed base.
So the parent claim read literally ("lacks EVERY scrubbed key, all four
adapters") is false for those 8 names on claude_code; the rule that HOLDS is
the one the dispatch line states: restart and first spawn are built from the
same base. The test asserts exactly that (agreement, not absence).

## 5. Tests -- `extensions/agi/tests/test_restart_scrubbed_env.py` (new, 9 pass)

1. `test_restart_child_lacks_every_scrubbed_key[4 adapters]` -- falsifier 1.
2. `test_restart_child_matches_the_first_spawn_for_claude_code_keys[4]` -- the
   agreement rule of 4, so a future divergence between the two paths is red.
3. `test_no_adapter_carries_a_second_scrub_list` -- falsifier 2 (no
   `base=dict(os.environ)` in any adapter; `scrubbed_base` explicit-wins and
   default-scrubs).

FALSIFIER CHECK: reverting only pi's one env line to `base=dict(os.environ)`
turns 3 tests red (`...scrubbed_key[pi]`, `...claude_code_keys[pi]`,
`...second_scrub_list`) -- the test bites.

Neighbourhood, all green after the change (falsifier 3):
`test_credential_none_spawn.py test_dispatch.py test_heal_ack_rotation.py`
-> 160 passed; `test_dispatch_restart_render.py test_real_adapter_restart.py
test_claude_code_adapter.py test_adapters.py test_copilot_cli_adapter.py
test_grok_bot_adapter.py test_harness_dispatch_shapes.py` -> 170 passed.

## 6. Cost

`git diff --numstat` over the six production files = **36 added / 3 removed**
(ceiling 40). No real pi / claude / copilot / grok process was started; the
probe stubs `subprocess.Popen`. Pi-free, 0 USD.

## Evidence

Raw probe output: `.agi/sessions/iter-DH.388/a00-f046ea4a/probe_prefix.txt`
(pre-fix, leak rows) and `.../probe_postfix.txt` (post-fix table 3).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review DH.388. (1) INSTRUCTION: the target hypothesis said every adapter restart() builds the child env from dispatch.scrubbed_env(), never raw os.environ. (2) WHAT THE MACHINE DOES, measured by the bytes and by probes I built and ran (stubbed subprocess.Popen, four scrub keys set in os.environ, restart(base_env=None)): pi/grok/copilot leak {}; claude_code leaks {ANTHROPIC_API_KEY} -- and that one is RESTORED_NAMES in child_env (claude_code_adapter.py:378), restored on the FIRST spawn identically, so it is a harness policy, not a restart regression. No restart() reads os.environ for a base any more; dispatch.py:3637 passes base_env=scrubbed_env(). (3) NEAR MISS: scrubbed_base(explicit) returns dict(explicit) verbatim, so the scrub is trusted-by-discipline at the adapter seam. My auth probe -- restart(base_env=dict(os.environ)) -- makes copilot hand the child AGI_MODEL_SLOT_LOCK, ANTHROPIC_API_KEY, AGI_ORDERS_TEXT and OPENROUTER_PROVISIONING_KEY, the key that MINTS keys (goal:g1.11). No in-tree caller passes raw, so nothing leaks live, but heal.py -- named in scrubbed_env own docstring as the second spawner -- is exactly the caller that would. (4) DEVIATION: I do not demote this kid to lean_disproved: the fix it delivered is the mechanism the claim is about, and the surviving hole is at the seam it introduced, carried to the next kid as the named step.
<!-- THOUGHT:END -->

## Agent Notes
All four adapters' restart() now build from dispatch.scrubbed_env() (one scrub list, adapters.scrubbed_base + base_env= at the reaper); 9 new tests, falsifier-verified, 330 neighbourhood tests green. Literal 'lacks EVERY scrubbed key' is false only for claude_code's own 8 ANTHROPIC_*/CLAUDE_CODE_* names, which its child_env restores on the FIRST spawn too -- so the tested rule is base-AGREEMENT between spawn and restart.

PROBES (parent-run, not the kid suite): wire -- four scrub keys set in os.environ, Popen stubbed, restart(base_env=None): pi {} / grok {} / copilot {} / claude_code {ANTHROPIC_API_KEY} (RESTORED_NAMES, same on first spawn, accepted as by design). auth -- restart(base_env=dict(os.environ)): copilot leaks AGI_MODEL_SLOT_LOCK, ANTHROPIC_API_KEY, AGI_ORDERS_TEXT, OPENROUTER_PROVISIONING_KEY; claude leaks the first three. FAILS the never-raw reading at the adapter seam; no in-tree caller triggers it. gate -- grep: zero os.environ bases left in the four restart()s; the only surviving read is claude_code:378 restore source. ACCEPTED with the auth probe named; the hardening it implies is kid 2 (experiment:a00-5571040e-f3cd53).
