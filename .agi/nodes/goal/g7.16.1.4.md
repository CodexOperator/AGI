---
id: goal:g7.16.1.4
mint_id: 11bb853511b54358ade2d89ae72f9b47
type: goal
parents:
  - goal:g7.16.1
next_edges: []
confidence: 0.75
edited_by: alive
goal_id: G7.16.1.4
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: d910b9051143108f
season: 2
seeds: []
status: active
tags:
  - formation
  - council-loop
  - bundle-4
  - local-maxxing
  - write-path
  - render-path
title: "G7.16.1.4: COUNCIL BUNDLE 4 -- the write/render split: W-G GOALS.md retired -> W0 one live goal per act (g4.19) -> W1 g4.18.5 rows + a write is a commit -> W2 g4.18.6 links are mint ids -> W3 g4.18.7 read leaves write.py, one render path"
town: core
---
# goal:g7.16.1.4

## OWNER 2026-09-29 18:0xZ, verbatim (Prime pane, relayed by belam-S2-L5-XVI to the council)
"Write shouldn't need a read path. We should only need a render path. Add it to bundle if needed I've been meaning to improve the way the graph is rendered for agents for a while. Unify everything into the correct slots. Read doesn't belong to write semantically im surprised the council didn't catch it"

## Why this exists
goal:g7.16.1 (the council loop): the Prime handed the council three owner orders from 17:2xZ-18:0xZ as ONE bundle, "the write/render split", and asked the council to place it. Council placement 17:5xZ-18:0xZ (alive · all-is-one · self-perpetuating, all three agree): its OWN bundle after bundle 3, NOT folded in. Bundle 3 (goal:g7.16.1.3) is mid-build with DG2 since 17:56Z, and its H1 (goal:g4.18.3) edits write.py, while goal:g4.18.5 rewrites write.py's core write path. goal:g4.18.7 addresses rows by goal:g4.18.5's index and resolves names through goal:g4.18.6, hence the order.

## Target end-state
Rows in council order. A row closes when its line holds in the bytes.
- **Base.** Cut from bundle 3's FINAL clean tip 1f39ffb1c (SM re-confirmed 21:1xZ after the council batch C1 + CM1-CM10 closed; replaces ddea3a61f and 9966e3050), never 900a4017a; the build HOLD was lifted at 21:1xZ, so goal:g4.18.3's authorship-gate test already stands when the write path is rewritten under it. Core's write.py +125 (the bundle-5 file list) is read as INPUT: each hunk is absorbed or rejected by name, so bundle 5 never ports onto a dead shape.
- **W-G · GOALS.md is retired** (moved UNBUILT from bundle 3 row G, council 20:2xZ; OWNER 17:3xZ 09-29, verbatim on goal:g7.16.1: "Go ahead and retire GOALS.md. We don't need it anymore stop bothering with it or the render byte round trip script"). ONE row: the live render callers (driver.sh:240 on every --smoke, the rotation closeout, the review gates), the same-row couplings (retire --from-doc + its unlink, the closeout --check gate, node_writer's goal-type reason, the goals_file cell) CLAUDE.md's "Read YOUR goal by id" line, its --check table row and its "GOALS.md is derived" convention move together (every --smoke rewrites GOALS.md in MAIN today, leaving it dirty); goals are then read through W3's render path (goal:g4.18.7): GOALS.md is a second read surface, so W-G and W3 are one act. No half-retire: until W-G lands the render and --check stay live and a red --check is W-G's by name, never waived. --smoke still reports a node count after the render goes (the Prime's [red] 18:00Z: the node-count floor never goes blind).
- **W0 · one live goal per act.** goal:g4.19 (its title routes Read THROUGH write.py) is retitled under the owner's 18:0xZ line or parked by the tag `parked:g4.18.7`; no two live goals route one act opposite ways.
- **W1 · rows, and a write is a commit.** goal:g4.18.5, carrying goal:g4.18.3's invariant verbatim: "One authorship gate for every write.py verb that writes a node; no verb returns ahead of it." Input (DG4 L2a(a), alive ruling 22:3xZ): config:commands rows nested under frontmatter `manifest:` (commands.md ~2600, ~3019) cannot be removed -- unset drops only a top-level key and set manifest re-serialises ~2400 lines -- so W1's one-row verb must address a NESTED row (unset/replace manifest.<key>); DG4 retires unify.py + verify_unified.py files, nodes AND rows together after W1 lands (never a half-retire). Input (DG2 §6): the writer stamps town: core for local-town posts -- fix inside the one row write, never beside it. Input B2 (all-is-one lens on bundle 3): config:posts has 4 commit paths in rotate.py (_ack_commit_seats, _publish_row_to_authority, _commit_spawn_row, _commit_stops_row), each hand-given _posts_load_error; the one row write absorbs all 4, and _posts_load_error's content.split frontmatter + _row_names (a 2nd row parser beside _own_row_line) go to node_writer's one parser.
- **W2 · links are mint ids.** goal:g4.18.6, minus its end-state bullet 2's read routing (one home: goal:g4.18.7). Couplings, in the SAME row: CLAUDE.md's renumber rule ("re-point every reference in the SAME commit") and the agi-goal skill's matching renumber text retire, since no link ever needs re-pointing.
- **W3 · read leaves write.py.** Input B3 (all-is-one): grep_live / parked_carriers (a node search + the park tag) live in rotation_record, so write.py imports rotation_record to unpark; they move beside node_writer when W2/W3 reshape reads. goal:g4.18.7: `read` leaves VERBS in the same row that repoints every teaching file (8 files / 13 lines, director-general-1 at db3e22e55) (the agi-node-write skill grammar and CLAUDE.md included). No alias, never two read paths.
- **Hygiene when touched:** goal:g4.18.3 / .5 / .6 bodies carry a doubled `# goal:<id>` H1; the row that next edits each fixes it by `replace body`.

## Invariants
- No parent/kid dispatch (goal:g7.16.1). Every node is written through write.py. Nothing is deleted. Nothing is written on core/season2/main or core/main.
- One director works the bundle at a time: DG1 -> DG2 -> DG3 -> sanctuary-master -> council. Tests run ONE file at a time while a PASS runs on this box.
- The viewport never gains a write path (goal:g9); `viewport.py --verify` exits 0.

## Falsifier
1. goal:g4.18.5, goal:g4.18.6 and goal:g4.18.7 read complete, with their own falsifiers run; `python3 extensions/agi/bin/viewport.py --verify` exits 0.
2. Negative: `git grep -n '"read":' -- extensions/agi/bin/write.py` prints nothing; `git grep -n "re-point every reference" -- CLAUDE.md skills` prints nothing; goal:g4.19's title no longer names Read routed through write.py.

## Out of scope
goal:g7.16.1.3 (bundle 3, and its row R: goal:g6.41.1 P1+P6, P5) · bundle 5 = goal:g6.41.1 P2-P4 + its Falsifier 1 (RESUMED) + [RE-PLACED 23:4xZ, alive: the launch-path items below ride goal:g7.16.1.7 (the spawn line, now); the write-path items follow this bundle with goal:g7.16.1.6] council inputs from the bundle-3 lenses (C3 one scope-argv builder through mem_cap with a plain tmux fallback: ensure_tmux_session's inline argv at rotate.py:1756 skips systemd_run_usable; B1 one launcher: heal._launch_recovered calls rotate._launch_window, ensure_tmux_session called once; B4 one config reader: heal._recovery_psi_max_pct beside rotate._config_json / mem_cap._spawn_block, and the dump_record alias; R2-alert: N consecutive deferred recoveries -> ONE [red] to belam naming the seat + avg10, blind PSI its own [red]) + council mur c2 inputs (SCRUB_SCOPES path literals at test_anonymize_guard.py:405 -> a config cell; a mechanical scrub NAMES ITSELF in each THOUGHT (its ~374 edited_by = director-general-3 stamps are true last-editor stamps, prior editors in the grid; see the DG4 L2b ruling 22:2xZ); the anonymize guard reads HEAD so a fresh leak is caught one commit late; horizon goal:g7.16.1.4.1.1 RE-PLACED to director-general-4's LEFTOVERS lane (alive 22:1xZ, on the Prime's DG4 formation: leftover cleanup with no bundle dependency; first placed here at 21:5xZ): unify.py / verify_unified.py / publish-engine.sh still name GOALS.md but sit on NO live path (crontab 0 hits; crons.md:199 past tense; verification.py:4 is not verify_unified; they are goal:g11 one-repo migration tools, done) -- shape = RETIRE, not patch (verify_unified check 6 goals_at_repo_root now fails if run). CORRECTED 22:2xZ on DG4's finding: publish-engine.sh is still WIRED, dormant (the SessionStart hook g7.10 publish alarm cc-session-start.sh:119, grid.py cron --publish-engine :1836, crons.py publish_engine :926), so the leaf SPLITS: (a) unify.py + verify_unified.py, no wiring, first; (b) publish-engine.sh + its g7.10 alarm + cron flag, the hook every session runs, its own careful round. DG4 L2b ruling (alive 22:2xZ): edited_by = the scrubber, the scrub named in each THOUGHT -- edited_by records the LAST editor, which a scrub truly is, and every prior edited_by lives in the grid; "preserve edited_by" (my 22:1xZ brief) would claim a write the node did not get, so it is withdrawn; council mur c1: the row-park grammar has no template line -- [goal].md / [hypothesis].md carry only the TAG form) + horizon goal:g7.16.1.5 (round worktrees on a capped RAM disk) GATED on W1 landing -- its premise is "once every write is a commit", which is W1 + SM's 7 next-bundle candidates (inbox 20:05Z) + core's edits to EXISTING files (write.py +125 after W-input, dispatch.py +86, boxes.py +87, provisioning.py, rotate.py) + profile_sync · the season-2 close.

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by alive (council convener) 18:0xZ 09-29 on the Prime belam-S2-L5-XVI [owner] relay (the write/render split, placed AFTER bundle 3 by all three lenses; conditions on W1-W3 as in the body). This version (20:0xZ) adds row W-G: bundle 3 row G was NEVER BUILT -- 30f4db55f + e662637ac edit only goal/g7.16.1.3.md, driver.sh is untouched in 9181cee26^..9966e3050 and driver.sh:240 at 9966e3050 still runs --render --strict-goals (verified by alive, all-is-one and self-perpetuating), which is why SM clean handoff carried a red render --check. GOALS.md is a second read surface for goals and W3 makes viewport the one, so W-G and W3 are one act (all-is-one). Couplings move with it as ONE row (all-is-one 1, self-perpetuating b); no half-retire (all-is-one 2).
<!-- THOUGHT:END -->
