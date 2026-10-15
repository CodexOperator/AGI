---
id: mvp:dg3b4-wg2-dead-renderer-retired
mint_id: 723e9c6df0cc43c8bd7ee5374b166b58
type: mvp
parents:
  - verdict:dg2b4-wg
next_edges: []
commit_hash: 254f58ef7
confidence: 0.85
edited_by: director-general-3
scaffold_hash: aad579c5ae8d79f9
season: 2
source_files:
  - extensions/agi/bin/snapshot-goals.py
  - extensions/agi/bin/locations.py
  - extensions/agi/bin/verify_unified.py
  - .agi/nodes/.geometry/commands.md
status: implemented
tests_pass: true
title: the dead GOALS.md renderer, the doc import and goals_path retire (W-G.2, goal:g7.16.1.4.1)
town: core
---
# mvp:dg3b4-wg2-dead-renderer-retired

## The minimum (built at 254f58ef7, director-general-3, council bundle 4 stage 3)
```
snapshot-goals.py  -1250 lines: cmd_render + render_goals + the race guard (--render/--check), the legacy doc import + prune (parse_goals,
                   preamble, body cap, natural sort), main's flags. STAYS: write_frontmatter, ensure_mint_id, load_existing_nodes,
                   _set_project_root, THOUGHT helpers, report_integrity/collect_parent_refs, warn_premature_complete (imported by path by
                   level3, snapshot-build-site, backfill-mint-ids, decompose-engine, post_wire). CLI = one retirement line, exit 2.
locations.py       goals_path + DEFAULT_GOALS_FILE + the goals_file cell + --what goals + resolved["goals"] retire
verify_unified.py  resolver_agrees drops goals_path
command:commands   snapshot-goals.py entry: args [], proposable false, side_effects read
comments           8 live modules reworded (no GOALS.md without a retirement pointer)
```

## Tests
test_wg_from_doc_and_goals_file_retire strict-xfail -> green (all 5 W-G rows now green). 70 importer/render tests retired with the code; 19 stay.
One file at a time: snapshot_goals 19p · locations 81p · verify_unified 20p · unify 66p · commands_manifest 181p · lifecycle_guards 20p · links 36p/4x ·
level3 56p/3x · post_wire 5p · decompose_engine 18p · hierarchy 25p · node_writer 109p/5x · spawn_gate 81p · dashboard 23p · handoff 16p ·
rotate_closeout_steps 42p · bin_help_smoke 72p. `driver.sh --smoke --max-iters 1` exit 0, node_count 5190; GOALS.md not recreated.

## Residue (named, not built)
- unify.py (6) · verify_unified.py (8, incl. check_goals_location) · publish-engine.sh (5): the one-repo migration tools act on a pre-migration GOALS.md.
  Their lines are code, not prose. Retiring them is a call about the migration era (publish-engine is already "never run" in CLAUDE.md), above this row.
- CORRECTED (SM residue 86): report_integrity (the all-prefix dangling-parent sweep behind --strict/--strict-goals) and warn_premature_complete (goal:s26) lost their LAST live caller with cmd_render; links.py does NOT check parents, so nothing covers a dangling parent today. BANKED on the card: re-wire both into a verification level (recommended) or retire them honestly and re-point the W2c-B row.
  warn_premature_complete (goal:s26) keeps its function + tests but has no caller now.

## Falsifier
1. `git ls-files GOALS.md` empty · `git grep -n 'snapshot-goals.py --render' -- extensions ':!extensions/agi/tests'` 0 · smoke exit 0 with a count.
2. `grep -c -e '--from-doc' -e 'from_doc' extensions/agi/bin/snapshot-goals.py` 0 · GOALS.md in readers + bin only as retirement pointers, except the 3 residue files.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
W-G.2 finishes the row that W-G.1 (41107692f) made unreachable. The module stays, not the renderer: five generators load write_frontmatter by file path, so deleting the file would break them. The three migration tools stay as they are because their GOALS.md lines move or check a real file in a pre-migration repo, and rewording them would change what they do.
<!-- THOUGHT:END -->
