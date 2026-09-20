---
id: hypothesis:a00-e0ab0dcc-d7d5f1
mint_id: 11b20dc8e28245648cb61ea5d4774074
type: hypothesis
parents:
  - goal:g17.14.1
next_edges: []
confidence: 0.5
edited_by: a00-e0ab0dcc
evidence_runs:
  - experiment:grok-bot-adapter-corrective-committed-evidence
loop: goal:g17.14.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 46298018341e148d
season: 2
testable_claim: "**Testable claim.** The corrective for `goal:g17.14.1` lands on this branch as a byte-honest upgrade of committed work, not a re-design:"
title: "grok-bot adapter corrective: committed bytes, superset tests, real respawn probe"
town: core
verdict: pending
---
# hypothesis:a00-e0ab0dcc-d7d5f1

## Hypothesis

**Testable claim.** The corrective for `goal:g17.14.1` lands on this branch as a
byte-honest upgrade of committed work, not a re-design:

1. `extensions/agi/bin/adapters/grok_bot_adapter.py` carries the DT.14
   (`e554c440c`) bytes verbatim — 162 lines, `NAME="grok-bot"`, bare
   `DEFAULT_BIN`, `resolve_bin`, `model_args` raising `KeyError` by tier name,
   `child_env`, stub `build_command` = `<bin> [--model M] -p <context_file>`,
   real detached `restart`, `is_alive`, and explicit `needs_credential` -> `False`.
2. The `harnesses.grok-bot` row is present in `.agi/config.json` exactly as the
   live-config line (`ca330ac35`) has it. **This row is `goal:g17.14.2`'s
   deliverable**, carried here only as a dependency so the live-config tests can
   run; this node does not claim its authorship.
3. `extensions/agi/tests/test_grok_bot_adapter.py` is a **superset**: BOTH the
   restart tests (`e554c440c`) AND the live-config tests (`ca330ac35`), with
   `_project_root()` and the `live_cfg` fixture present exactly once.
4. A REAL unmocked `subprocess.Popen` respawn probe is committed in-tree at
   `extensions/agi/tests/probes/probe_grok_bot_restart.py` with its real stdout
   beside it — clearing residue R1 (the DT.14 probe lived under gitignored
   `.agi/sessions/...`).
5. `extensions/agi/bin/dispatch.py` carries zero `grok` hits.

**What proves it.** `test_grok_bot_adapter.py` (15 tests) and
`test_adapters.py` (35 tests) both green; the committed `.out` showing a live
pid plus `is_alive True`; `grep -in grok extensions/agi/bin/dispatch.py` exiting 1.

**What disproves it.** Any silently dropped test (either set), a hand-written
probe transcript, a config row that does not resolve, or a `dispatch.py` grok hit.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Why this version: DT.14 returned accept_with_residue on three points -- probe evidence under gitignored sessions, production_lines measured from an uncommitted diff, and a test file that was not a superset. This version re-adds the e554c440c adapter verbatim (sha-identical), carries the ca330ac35 config row as a g17.14.2 dependency, merges BOTH test sets into one file, and commits a real unmocked respawn probe in-tree so the claim is backed by a merge-target-resolvable artifact.
<!-- THOUGHT:END -->

## Agent Notes
grok_bot_adapter (162 lines, sha-identical to e554c440c) + grok-bot config row (12 lines, g17.14.2 dependency) + superset test file (15 tests: restart+live-config) + committed real respawn probe. pytest 15/35 green, dispatch.py zero grok hits. production_lines 174 > 2x ceiling 80 -> rebrief_request filed, pending parent authorization.
