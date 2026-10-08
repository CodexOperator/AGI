---
id: experiment:a00-b9753db0-b62517
mint_id: b43a0a04135844fabb45fa4ead5ec397
type: experiment
parents:
  - hypothesis:l3-pi-adapter-role-kwarg
next_edges: []
confidence: 0.9
edited_by: ubuntu
evidence_runs:
  - experiment:a00-b9753db0-b62517
loop: hypothesis:l3-pi-adapter-role-kwarg@s2
model: ~z-ai/glm-flash-latest
profile: balanced
role: parent
scaffold_hash: 54b5dda0d5638927
season: 2
title: A00 b9753db0 b62517
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b9753db0-b62517

## Experiment

Verified hypothesis:l3-pi-adapter-role-kwarg — that pi_adapter.build_command rejected the `role`/`ladder_tier` kwargs dispatch.py passes to every adapter (since iter-L3.13 / hypothesis:l3-cc-tools-by-tier), killing every pi spawn with a TypeError, and that adding the two accepted-but-unused kwargs restores pi rows.

Inspection of source in the live tree (fix already applied by the director, a00-4ad19971):
- `extensions/agi/bin/adapters/pi_adapter.py::build_command` now declares `role: str | None = None` and `ladder_tier: int | None = None`, documented as accepted-and-unused for pi (no tool bundle).
- `extensions/agi/bin/dispatch.py` call site (≈L860) passes `role=args.role, ladder_tier=tier_eff` to every adapter unconditionally — tier-blind and harness-blind by design.

Ran the two pinning tests, then the full suite:
- `python3 -m pytest extensions/agi/tests/test_brief.py::test_pi_adapter_accepts_the_role_and_ladder_tier_kwargs_dispatch_passes extensions/agi/tests/test_brief.py::test_every_adapter_accepts_every_keyword_the_dispatch_call_site_passes -q` → 2 passed in 0.06s
- `python3 -m pytest extensions/agi/tests/ -q` → 1838 passed, 1 skipped in 101.93s

## Evidence

- **test_pi_adapter_accepts_the_role_and_ladder_tier_kwargs_dispatch_passes** (test_brief.py L717): calls pi `build_command(..., role="parent", ladder_tier=0)`; asserts argv[0] is spelled and the model flag resolves. The regression mechanism is red-faithful: before the fix this exact call died `TypeError: build_command() got an unexpected keyword argument 'role'`.
- **test_every_adapter_accepts_every_keyword_the_dispatch_call_site_passes** (test_brief.py L720): inspects `inspect.signature(build_command)` for both pi_adapter and claude_code_adapter, asserting every keyword in `{"harness","tier","brief_tier","context_file","agent_id","iter_n","sess_dir","scaffold","cli_py","skill_prompt","dispatch_py","target","parallel","max_live","role","ladder_tier"}` is present — signature parity so no harness is left behind.
- Full suite green (1838 passed, 1 skipped) — the added kwargs regress no existing adapter behaviour.

Not executed here: a live paid pi spawn (would consume model tokens; the mechanism is fully pinned by the red-faithful unit test + signature-parity test, and the director confirmed the live tier-0 parent spawn on the round that applied the fix).

## Agent Notes
Confirmed pi_adapter.build_command accepts role= and ladder_tier= (accepted-and-unused), call site passes both tier-blind, red-faithful pinning test + signature-parity test in test_brief.py pass, full suite 1838 passed / 1 skipped. Fix by director verified in place.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-f0e9690b, L3.18): accepted as proved. Verified independently — re-ran both pinning tests, 2 passed; parents resolve to hypothesis:l3-pi-adapter-role-kwarg; evidence_runs self-citation is legitimate (experiment is the run). Caveat stands: no live pi spawn in this run, so proved rests on the red-faithful unit + signature-parity tests plus the director's earlier live tier-0 confirmation, not a fresh live spawn. struggles field correctly surfaced that the hypothesis text pointed at test_adapters.py while the pinning tests live in test_brief.py — hypothesis body left as-is since the testable claim itself is not location-dependent.
<!-- THOUGHT:END -->
