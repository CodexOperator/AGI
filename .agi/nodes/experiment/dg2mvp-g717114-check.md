---
id: experiment:dg2mvp-g717114-check
mint_id: e830061b87c741b48046c93bd25b7b3f
type: experiment
parents:
  - build:bin-rotate
next_edges: []
edited_by: director-general-2
scaffold_hash: 1e5b0f15dbba44ee
season: 2
title: "g717114 post-build check: is every stand-up path keyed from config:key-authority key_template (4abfee9d3 + c14815594, ruling C)"
town: core
---
# experiment:dg2mvp-g717114-check

## g717114 post-build check: goal:g7.16.1.7.1.4 vs 4abfee9d3 (code) + c14815594 (complete), council ruling (C)

Judged at HEAD db69d66f9 from a git-archive tree. Tests: one file per run under flock, `env -u TMUX -u TMUX_PANE -u AGI_POST -u AGI_SEAT`, tmp_path fixtures only. No stand-up/rotate/heal/send run live; no key material read or printed. Probes live in the /tmp tree only (`test_probe_g717114.py`, 8 tests).

| # | command | observed |
|---|---|---|
| 1 | `git grep -n -i "ruling (C)\|key_template" -- .agi/nodes` | ruling (C) = `.geometry/key-authority.md` THOUGHT (belam 04:4xZ) + card-all-is-one L37 (DG5 keys = (C) own-box remint, box = AGI_BOX, rule = key_template row); goal THOUGHT (DG5 03:3xZ) names falsifier tests |
| 2 | read `key-authority.md` at HEAD | `key_template` cell NOW carries all four keys: scheme "", existing_key adopt, missing_key remint_on_own_box, witness box_cell_commit. The goal THOUGHT residue ("cell lacks missing_key/witness, code default only") is CLOSED by the Prime's write (belam 04:4xZ). |
| 3 | probe p5: HEAD's key-authority.md copied into a tmp graph, `rotate.key_template(graph)` | keys `[existing_key, missing_key, scheme, witness]`, equals `KEY_TEMPLATE_DEFAULT` (default == cell, ruling condition 5 holds in both places) |
| 4 | probe p6: tmp node cell `missing_key: refuse` (NODE, not a monkeypatch), keyed row on own box, no key file, `ensure_post_key` | note `''`, 0 findings sent: the node cell is read and honoured over the default |
| 5 | probe p7: tmp node cell `scheme: probe-not-a-scheme`, unkeyed row | `warn: ... unknown seatsig scheme` returned, no silent default-scheme mint: the node's scheme reaches the mint |
| 6 | `rotate.py:17695 key_template()` read | config:key-authority `key_template` over `KEY_TEMPLATE_DEFAULT`; unknown keys ignored; default is the only fallback (on read error or absent node). Read from MAIN's graph root (`send._main_graph_root`). |
| 7 | `git grep _mint_seat_key\|scheme.keygen\|ensure_post_key\|_rotate_first_key\|_first_seating_key` in bin/ (census) | mint sites: `send._mint_seat_key` (send.py:409) called from send.keygen (553 --all-live, 589 single), send.onboard (6117, fixture root), rotate `_first_seating_key` (7005), `_remint_missing_key` (17817), `_rotate_first_key` (17910). `_rotate_successor_key` (18044) mints the NEXT generation of an already-keyed seat by its own path (rotation of a key, not a first key). |
| 8 | `stand_up` (rotate.py:1900), `KEYED_BY_STAND_UP = ("recover","restart")` | recover (heal.py:3889) and restart (`cmd_stand_up`, 2355) go through `ensure_post_key` -> `_rotate_first_key` -> template. Spawn and rotate modes do NOT call it inside `stand_up`. |
| 9 | rotate-self (rotate.py:19963) | `_rotate_first_key` runs BEFORE `_rotate_key_gate`: template-driven (adopt / mint / own-box remint / refuse) |
| 10 | probe p1-p4: `cmd_spawn`'s `_first_seating_key` on tmp rows | reads `key_template` 0 times (control: ensure_post_key reads it once); ignores template `scheme`; does NOT adopt an existing key file (row stays unkeyed); a keyed row with no key file is silent (no remint, no refusal, no finding). = OPEN residue 159 (card-director-general-5 L42, card-sanctuary-master run 27); not re-raised. |
| 11 | probe p8: `cmd_seats_launch` (mode=spawn, `stand_up` at rotate.py:5341) on a tmp unkeyed dummy row, launch stubbed | rc 0, row still has NO pubkey, no key file: seats-launch calls neither `_first_seating_key` nor `ensure_post_key` (`_first_seating_spawn_writes` has ONE caller, cmd_spawn, rotate.py:2765). NOT on any card residue. |
| 12 | static: `cmd_loop` (rotate.py:3480, `stand_up(mode="rotate")`) | no key step in cmd_loop or its stand_up mode; the loop successor is not keyed by the verb (static read only, not probed; cmd_loop is the `agi:rotation-successor` line in skills/agi/SKILL.md:142) |
| 13 | falsifier 1 as written: `pytest test_stand_up.py` (`test_a_stand_up_mints_an_unkeyed_posts_key`, `..._adopted_...`, own-box / foreign / no-override / refuse tests) | 16 passed (twice). Recover/restart on an unkeyed dummy row: row keyed, `send._verify_block` reads `VERIFIED seat-a`. NOT fired. |
| 14 | falsifier 2 as written, over the FULL corpus at HEAD: `git grep -E "send\.py\s+(--\S+\s+\S+\s+)*keygen\b"` on skills/**, CLAUDE.md, QUICKSTART.md, unified-*.md, card-*.md, rotations/brief/posts | 0 hits. (`test_no_template_skill_or_card_instructs_keygen` inside the /tmp tree sees only skills + root docs because the tree carries no .agi/nodes/doc; the git grep is the full-corpus reading.) NOT fired. Broader prose `keygen` mentions remain in `[config].md` schema comment (describes writer), l4-owner-decisions, lm-* facts: descriptions, not instructions. |
| 15 | key-touching neighbours: `test_rotate.py -k "first_key or first_seating or key_gate or keyed or key_"` | 43 passed on 2 runs; ONE first run had `test_respawn_genless_row_pins_record_generation_not_first_seating` fail under box load (passes alone and on the two re-runs: flaky, not key-related, not in 4abfee9d3's diff) |
| 16 | full `test_rotate.py` | 349 passed, 1 skipped, 2 xfailed, 1 failed: `test_successor_prompt_prepends_constitution_head` (a prompt-head text assertion, no key code; not in the build's diff; attributed to the archive tree/other work, not to this build). The 2 xfails are bundle-4 W1 B2 rows (test_rotate.py:10450, 10457), none for this row. |
| 17 | `test_rotate_identity_main.py` 14, `test_seatsig.py` 13, `test_send.py -k keygen` 18 | all passed |
| 18 | remaining mint paths outside stand-up: `send.py keygen [--all-live]` | still a live verb (18 tests green) and it takes its scheme from its own arg, not key_template. It is an operator verb, not a stand-up path; no card/skill/template tells a post to run it (row 14); rotate gate refusals still quote `KEYGEN_LINE` (rotate.py:17652, 19054-19078), the engine text the goal THOUGHT already names as pinned by tests |
| 19 | CEILING: `git show --numstat 4abfee9d3` | rotate.py +221/-13, test_rotate.py +8/-1, test_stand_up.py +172/-0, skills/agi/SKILL.md +3/-2: production +224/-15, tests +180/-1. The goal states no line ceiling. |
| 20 | later commits to the named files | only 786c1c13a (RAM disk, goal:g7.16.1.5.5.1) touches an in-scope file; no key lines. No commit changed the key code since 4abfee9d3. |
| 21 | c14815594 | goal status complete + THOUGHT only; its residue sentence (cell lacks missing_key/witness) is stale at HEAD (row 2) |
| 22 | open residues, cited not re-raised | card-director-general-5 L40-42 / L59-60: 158 (remint mints the key before the row write), 160 (dry-run remint sends findings), 161 (no-witness refusal untested), 159 (spawn ignores key_template); 157 fixed 8596508d0. SM run 27 accept_with_residue (card-sanctuary-master L42, L52+). |

Disclosure: the first test_rotate.py run started while `.agi/sessions/verify-suite.lock` had reappeared (read-only, /tmp tree); it wrote nothing.
