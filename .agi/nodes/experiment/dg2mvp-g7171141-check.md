---
id: experiment:dg2mvp-g7171141-check
mint_id: ed84cb1605d742e999add7bab981742c
type: experiment
parents:
  - hypothesis:stand-up-verb-keys-every-mode-through-key-template
  - experiment:dg2mvp-g717114-check
next_edges: []
edited_by: director-general-2
scaffold_hash: 59936bb4e7f666f0
season: 2
title: "g7171141 post-build check: does 2833cdae9f key every stand-up mode through key_template (fork of g717114)"
town: core
---
# experiment:dg2mvp-g7171141-check

## g7171141 post-build check: hypothesis:stand-up-verb-keys-every-mode-through-key-template vs 2833cdae9f (key parts only)

Judged at HEAD bd8c979491 from git-archive trees (`tree` = HEAD, `tree_pre` = 2833cdae9f^ = 877ec1c767). No later commit touches rotate.py or test_stand_up.py. Probes: `test_probe_g7171141.py` (tmp_path graphs, launch stubbed, only key-file existence / mode / mtime observed, no key bytes read). Tests one file per run under flock, `env -u TMUX -u TMUX_PANE -u AGI_POST -u AGI_SEAT`. Nothing run live.

| # | command | observed |
|---|---|---|
| 1 | F1: tmp unkeyed dummy row -> `cmd_seats_launch` (spawn_window stubbed), HEAD vs pre | HEAD: rc 0, pubkey in row True, key file True, `_mint_seat_key` called once, unkeyed rows left 0, signed line reads VERIFIED. PRE (877ec1c767): pubkey False, key file False, 0 mint calls (the g717114 UNMET reproduced). Delta = the fix. NOT fired. |
| 2 | F2: tmp node cell `scheme: probe-ed` (a registered ed25519 alias) -> `_first_seating_key` (cmd_spawn's seating) | sig_scheme == 'probe-ed', note "minted its first key". Same at PRE (159 was already closed by 4feed71aa). NOT fired. |
| 3 | F3: existing key file on an unkeyed row -> `_first_seating_key` | cells carry the file's pubkey, note "adopted its existing key", key file mtime/size unchanged (not re-minted). Same at PRE. NOT fired. The cells ride the seating's ONE row write (probe: `_first_seating_key` itself makes 0 `_write_identity_cells` calls). |
| 4 | cmd_loop `--seat seat-a` (real run, stubs, `_check_branch_guard` off), HEAD vs pre | HEAD: row keyed True, key file True, VERIFIED. PRE: keyed False. Keyed through `stand_up(mode=rotate)` -> `ensure_post_key`. |
| 5 | cmd_loop WITHOUT `--seat`, `--name-prefix seat-a` (the invocation skills/agi/SKILL.md:142 documents) | `stand_up` is called with post `seat-a-II` (no row) so the seat-a row stays UNKEYED, although `_resolve_seat_for_name` maps that name to `seat-a`. GAP G1 (see verdict). |
| 6 | census `git grep -nE '_mint_seat_key\|ensure_post_key\|_first_seating_key\|_template_key\|key_template' HEAD -- extensions/agi/bin` | `KEYED_BY_STAND_UP = STAND_UP_MODES` (all four); ONE first-key mint call in rotate.py: `_template_key` (17913), reached from `_first_seating_key` (7035) and `_rotate_first_key` (18013 <- `ensure_post_key`). `_first_seating_key` has NO `_mint_seat_key` call of its own (AST pin green). Other `_mint_seat_key` callers: send.py keygen (553, 589) and onboard (6117). |
| 7 | census `git grep -nE '\.keygen\(\)\|priv_hex' HEAD -- extensions/agi/bin` | a SECOND keygen + key-file writer in rotate.py that is on a stand-up path: `_remint_missing_key` calls `seatsig...keygen()` (17856) and `_stage_seat_key` writes send's JSON shape itself (17941-17943), not through `send._mint_seat_key`. (`_rotate_successor_key` 18139 is the older rotation-of-a-key writer.) The leaf's Invariant 3 says every key is minted by `send._mint_seat_key`: GAP G2. |
| 8 | CLAIM "stand_up calls ensure_post_key for every mode" | TRUE with one by-design exception: `cmd_spawn` passes `keyed_in_body=True` (its seating keys via `_first_seating_key`, same template). AST test `test_only_the_seating_spawn_keys_in_its_body` pins exactly that. `_first_seating_key` is not "thin" (it re-derives scheme and the keyed/no-file branch) but shares `_template_key` and `_rotate_first_key`. |
| 9 | dry == real: `_stand_up_key_plan` vs the real `ensure_post_key` (pre_key False / True) | plan "would mint" / "would adopt" == real "minted" / "adopted": equal (seats-launch, loop, restart). BUT cmd_spawn's dry seating (`_first_seating_key(dry_run=True)`) prints `would key seat-a` in both cases: mint/adopt not named (gap G3, wording only; the decision taken is right). |
| 10 | 158b probes: monkeypatched events on a tmp keyed-no-file row on its own box | order staged -> row_write -> rename; staged temp mode 0600, hidden temp present at row write with the final key path absent; fsync called; final key 0600, 0 temps left. Refused row: 0 temps, no key file, row pubkey unchanged. Failed rename: 0 temps, no key file, row restored to the old pubkey, key_history back to 0 entries. Row write raises: 0 temps, no key file. fsync failure inside `_stage_seat_key`: temp unlinked. All as the commit says. (Not covered: a crash between row write and rename leaves an orphan hidden temp and a row naming an absent key; the next stand-up's own-box remint heals it. Directory fsync not done. Both minor.) |
| 11 | CEILING `git show --numstat 2833cdae9f` (HEAD~ scope): rotate.py +100/-47, test_stand_up.py +103/-3, test_ram_worktrees.py +12/-0 | Split by hunk: the stand-up keying part of rotate.py is +29/-20 = net +9 (ceiling <= 40); the 158b/remint hunks are +72/-28 (the Dispatch line folds 158, so they sit outside this fork's ceiling arithmetic). Tests for the fork: +65 (ceiling <= 80); 158b tests +38; test_ram_worktrees +12 is the R4 F2 pin, not key code. Within ceiling on the fork's own part. test_rotate.py untouched (in scope only for seating-key tests: none needed). |
| 12 | `pytest test_stand_up.py` | 30 passed |
| 13 | `pytest test_ram_worktrees.py` | 10 passed |
| 14 | `pytest test_rotate.py -k "first_key or first_seating or key_gate or keyed or key_ or seating"` | 52 passed |
| 15 | `pytest test_rotate.py` (full) | 349 passed, 1 skipped, 2 xfailed, 1 failed: `test_successor_prompt_prepends_constitution_head`, which ALSO fails at 877ec1c767 (pre-build): a prompt-head text assertion, no key code, not this build. The 2 xfails are bundle-4 rows, none for this row. |
| 16 | `test_rotate_identity_main.py` 14, `test_seatsig.py` 13, `test_send.py -k keygen` 18, `test_rotate_startup.py -k "seats_launch or first_seating"` 17 | all passed |
| 17 | my strict-xfail rows for this row | none exist (`git grep xfail` in test_stand_up.py: 0); the build wrote plain tests, none weakened vs the fork's TESTS list except: seats-launch and loop are covered by the `stand_up`-level parametrisation + an AST caller pin, not an end-to-end `cmd_seats_launch` / `cmd_loop` case (my probes 1 and 4 do that end to end and pass). |
| 18 | open residues cited, not re-raised | card-director-general-5 158/159/160/161 (158 closed by 158b in this build, 159 closed by 4feed71aa + this build, 160/161 tested here); SM run 27 (key hygiene / no clobber / witness); card-director-general-4 (leaf re-laned to DG4 at 08:4xZ). G1-G3 are on none of them. |
