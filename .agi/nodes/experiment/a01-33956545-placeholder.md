---
id: experiment:a01-33956545-placeholder
mint_id: f3e32af025164202b3332597095e99d8
type: experiment
parents:
  - hypothesis:a01-33956545-9fc0bb
next_edges: []
confidence: 0.73
edited_by: director
evidence_runs:
  - experiment:a01-33956545-placeholder
link_ref: extensions/agi/tests/test_commands.py::test_render_table_preserves_placeholders
payload_ref: extensions/agi/tests/test_commands.py
scaffold_hash: a99c9ac57ec33d59
thought_session: L1.12
title: Derived command tables stay placeholder-safe
verdict: proved
---
# experiment:a01-33956545-placeholder

## Experiment

**Goal:** prove the renderer that feeds every operator-facing doc (CLAUDE.md,
QUICKSTART.md, SKILL.md) now emits the `<engine>` / `<root>` placeholders
verbatim even though the resolver substitutes real paths at execution time.

Steps:

1. Extend `commands.Command` to carry both substituted (`argv`, `cwd`) and raw
   (`raw_argv`, `raw_cwd`) values while keeping runtime behaviour unchanged.
2. Teach `Command.shell(placeholders=True)` to format the raw argv so renderers
   can stay clone-agnostic, while default behaviour still shows runnable argv.
3. Update `commands.render_for_injection` and `derive-commands.py` to call
   `shell(placeholders=True)` so both the injected brief and the prose tables
   render the placeholders.
4. Add regression coverage:
   - `test_commands_resolve_from_the_node` now sees the extra command
     introduced solely to exercise `<root>`.
   - `test_argv_is_a_list_so_nothing_is_reparsed_by_a_shell` asserts raw vs
     substituted argv diverge.
   - New `test_render_table_preserves_placeholders` imports the renderer via
     `SourceFileLoader` and asserts `<engine>`/`<root>` survive while absolute
     paths do not.
5. Run `derive-commands.py --all` to rewrite CLAUDE.md, QUICKSTART.md, and
   SKILL.md from the updated renderer.
6. Run the repo tests: `python3 -m pytest extensions/agi/tests/ -q` ⇒ **1471
   passed**.

## Evidence

- `python3 extensions/agi/bin/derive-commands.py --check --all` ⇒ detected all
  three docs stale, then clean after `--all`.
- `python3 -m pytest extensions/agi/tests/ -q` ⇒ `1471 passed` (new tests
  included).
- CLAUDE.md, QUICKSTART.md, and SKILL.md COMMANDS blocks now read
  `` `bash '<engine>/extensions/agi/driver.sh' ...` `` rather than literal
  `/home/ubuntu/...`.
- `extensions/agi/tests/test_commands.py::test_render_table_preserves_placeholders`
  asserts `<engine>` / `<root>` visibility and absence of absolute paths.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
"Director hygiene fix at close of L1.12: the kid wrote payload_ref with a ::test-name suffix, which is not a path; links.py counted it broken. The test name it meant is test_render_table_preserves_placeholders."
<!-- THOUGHT:END -->
