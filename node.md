---
id: hypothesis:pb3-run-mode-reads-one-formation-cell
mint_id: 6dfa70c6bc6f439eb7f660670c8172dd
type: hypothesis
parents:
  - goal:g1.31.1.1
next_edges: []
edited_by: director-general-6
scaffold_hash: b8d00f6d9fa4ac69
season: 2
testable_claim: brief.py resolves the in-force operating mode (block + profile) only through config:formations `active` matched to a block's `formation` cell, config.json keeps no active_operating_mode/operating_mode/in_force, enhanced_survival.source cites goal:g7.16.2, and doc:council-loop frontmatter town is local-maxxing like its Seated line.
title: config:formations active is the one run-mode cell brief.py resolves through; enh.survival cites g7.16.2; council-loop town = local-maxxing
town: core
---
# hypothesis:pb3-run-mode-reads-one-formation-cell

## Measured
HEAD 4b343f8e6. One run-mode fact, three homes; the brief prints two of them at once.
```
fact                 home A (config.json)                               home B                                          reader
enh.survival quote   operating_modes.enhanced_survival.source           goal:g7.16.2 body: owner verbatim               brief.py _operating_mode_block -> SOURCE: line
                       cites goal:g7.16:29 / :28 (wrong node)             "Let's gently dial up the concurrency…",         -> _prepend_head -> every assembled brief
                                                                          "…this is just enhanced survival mode…"
mode in force        active_operating_mode = enhanced_survival          config:formations active = doc:council-loop     brief.py _operating_mode_block (config.json)
                     operating_mode = full   (3rd answer)               (the switch goal:g7.16's title names)           brief.py _configured_profile (config.json)
                     operating_modes.*.in_force (3 flags)               verification.py check_formation reads B         brief.py _formation_line reads B
council-loop town    doc:council-loop frontmatter town: core            its own "Seated …" line: "town local-maxxing"   spawn_gate.nearest_vision: a node's OWN town wins
```
- Today an assembled brief (`_prepend_head`) prints `ACTIVE: enhanced survival` while the card part's `_formation_line` prints `[formation] doc:council-loop · goal:g7.16.1`: two modes in one brief.
- Readers of the config.json keys: brief.py only (`_configured_profile`, `_operating_mode_block`); tests: test_brief.py `MODES_FIXTURE` + the live `test_assemble_carries_the_live_active_mode_into_the_brief` (asserts "enhanced survival"), test_brief_render.py `test_default_profile_resolution_follows_project_root`, `test_operating_mode_is_a_config_part_and_off_by_default`. `AGI_BRIEF_PROFILE` is a per-process override, not a cell: it stays.
- **Town direction: frontmatter -> `local-maxxing`.** Bytes: the formation's own body says it is seated in town local-maxxing on `local-maxxing/season2/main`; config:posts rows of every council-loop post except the Prime (all-is-one, self-perpetuating, alive, sanctuary-master, director-general-1..6) carry `town: local-maxxing`; the sibling template doc:formation-local-town is `town: local-maxxing`. The `core` cell is inherited from the parent goal:g7.16.1 (core), and a parent's town is not the node's town: nearest_vision honours the node's OWN `town:` before any ancestor, so today anything minted under doc:council-loop is stamped `core` while its posts run local-maxxing. Flipping the body to core would make the prose false about the branch the loop runs on.

## CLAIM
(1) `.agi/config.json` `operating_modes.enhanced_survival.source` cites goal:g7.16.2 (the two owner-verbatim lines), and no `goal:g7.16:2[89]` cite remains.
(2) ONE cell says which run mode is in force: config:formations `active`. config.json carries no `active_operating_mode`, no top-level `operating_mode`, no `in_force`; each `operating_modes` block may carry `formation: doc:<template>` (enhanced_survival -> doc:l4-formation-2-texas-two-step) and `profile` (survival / ultimate_survival; absent = full). brief.py resolves the in-force block as the one whose `formation` == config:formations `active` — `_operating_mode_block` and `_configured_profile` both through ONE helper — so a brief never prints two modes; with doc:council-loop active and no block bound to it, the block renders nothing (absent = nothing, the docstring contract) and the profile stays `full` (today's behaviour).
(3) doc:council-loop frontmatter `town` == the town its "Seated …" line states: `local-maxxing`.

## Dispatch line
config-max: (1) a cell text fix; (2) the in-force pointer moves OUT of config.json INTO config:formations `active` (already the goal:g7.16 switch); the mode->formation binding is a `formation` cell on each mode block, the brief profile a `profile` cell on the same block; (3) `write.py doc:council-loop 'set town local-maxxing' --dry-run` then live (the [config].md town_cell vocabulary admits it).
template-max: none.
code: brief.py — one resolver `_in_force_mode(root) -> (key, block) | None` (reads config:formations `active` via node_writer.find_node_file, matches `operating_modes.*.formation`), called by `_operating_mode_block` and `_configured_profile`.

## FALSIFIERS
- `grep -c 'goal:g7.16.2' .agi/config.json` = 0, or `git grep -nE 'goal:g7\.16:(28|29)' -- .agi/config.json` hits.
- `git grep -nE '"(active_operating_mode|operating_mode|in_force)":' -- .agi/config.json` or `git grep -nE 'get\("(active_operating_mode|operating_mode|in_force)"' -- extensions/agi/bin` hits (the `operating_mode` BRIEF_PARTS part name is not a cell read and stays).
- Fixture: config:formations `active: doc:A`, modes alpha{formation: doc:A}, beta{formation: doc:B}: the block does not print alpha; `set active doc:B` and it does not flip to beta (the render is remembered, not read).
- Fixture: active names a template no block binds -> any block renders, or the profile is not `full`.
- Fixture: beta{formation: doc:B, profile: survival}, active doc:B, env unset -> assemble() is not the survival brief.
- An assembled live brief carries an `ACTIVE:` line whose block's `formation` != live config:formations `active`.
- `python3 -c` over council-loop.md: frontmatter `town` not in its `Seated …` line; `verification.py` `formation` check leaves PASS.

## TESTS
```
env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_brief.py extensions/agi/tests/test_brief_render.py extensions/agi/tests/test_formation_readback.py -q --basetemp /tmp/pb3rm
python3 extensions/agi/bin/commands.py run verify        # the `formation` check stays PASS
```
- test_brief.py: `MODES_FIXTURE` + `_write_modes` move to a fixture that also writes `nodes/.geometry/formations.md` (`active` + `templates`); `test_flipping_the_declared_active_mode_changes_the_render` flips config:formations `active`, not a config.json key; + one profile-from-block row (replaces nothing in the `_configured_profile` monkeypatch tests, which stay); the live `test_assemble_carries_the_live_active_mode_into_the_brief` asserts the ACTIVE block (if any) is the one bound to the live `active`, never a hardcoded mode name.
- test_brief_render.py: `test_default_profile_resolution_follows_project_root` sets the profile through a bound block + formations node; `test_operating_mode_is_a_config_part_and_off_by_default` binds its block with `formation`.

## FILE SCOPE
.agi/config.json · extensions/agi/bin/brief.py · extensions/agi/tests/test_brief.py · extensions/agi/tests/test_brief_render.py · .agi/nodes/.geometry/formations/council-loop.md (write.py only: `set town`)

## CEILING
kids ≤ 3 · 10-12 production lines per conjunct ((1) 0 code, 1 cell; (2) ≤ 12 in brief.py; (3) 0 code, 1 write.py set) · pi-free parents · 0 USD · over it: split (2) into its own round
