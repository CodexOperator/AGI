---
id: verdict:schema-registry-r8-by-citation
mint_id: fe9dc6b193894bcc935b30ea441da734
type: verdict
parents:
  - hyp:schema-registry-r8
next_edges: []
confidence: 0.8
edited_by: season.py
evidence_runs:
  - build:src-schema-registry-active-set
  - build:src-schema-registry-loader
  - build:tests-schema-registry-test-brackets
  - build:tests-schema-registry-test-schema-files
scaffold_hash: 5ebbba7949c2c2f6
season: 1
supports:
  - hyp:schema-registry-r8
tags:
  - schema-registry
  - R8
  - l1.09
  - by-citation
thought_session: season
title: "schema-registry/R8: closed by citation"
verdict: inconclusive_lean_proved:80
---
# verdict:schema-registry-r8-by-citation

## Verdict

`inconclusive_lean_proved:80` — **closed by citation, not by a run** (L1.09, 2026-09-03).

## Evidence

`hyp:schema-registry-r8` — *Built-In Schemas for Autoresearch Types* — was specified by the cavekit build-site and never reached a verdict there. The real, non-build-site tree already carries what it asked for:

- `build:src-schema-registry-active-set` → `extensions/agi/src/schema_registry/active_set.py`
- `build:src-schema-registry-loader` → `extensions/agi/src/schema_registry/loader.py`
- `build:tests-schema-registry-test-brackets` → `extensions/agi/tests/schema_registry/test_brackets.py`
- `build:tests-schema-registry-test-schema-files` → `extensions/agi/tests/schema_registry/test_schema_files.py`

Grounds: `.agi/context/schemas/[*].md` is the real built-in schema set (a superset of the fictional eight, adapted to this project's taxonomy); bracket override is `active_set.py` and `loader.py::_generic_schema()` is the fallback for a missing schema.

Survey: `.agi/sessions/L1.09-mining/report.md` §C. Nothing was executed for this verdict; the suites named above are the ones `commands.py run tests` already runs.

## Confidence

0.8 — the citations are real files with real test suites, but this verdict cites them rather than running them, which is why it is `inconclusive_lean_proved:80` and not `proved`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Written 2026-09-03 in L1.09 to close `hyp:schema-registry-r8` by citation per the build-site survey (§C); the hypothesis is deprecated in the same pass with its `origin: build-site` cohort (goal:s18), and this verdict is the live record of where its claim is actually satisfied.
<!-- THOUGHT:END -->