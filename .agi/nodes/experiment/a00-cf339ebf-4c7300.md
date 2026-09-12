---
id: experiment:a00-cf339ebf-4c7300
mint_id: 65c78420458a41ec89775e0fb6aef47f
type: experiment
parents:
  - hypothesis:l4-the-label-authority-falls-back-to-mains-committed-row-and-every-key-cell-writer-commits-and-pushes-its-own-row
next_edges: []
confidence: 0.9
edited_by: a00-4a8d98b3
evidence_runs:
  - experiment:a00-cf339ebf-4c7300
loop: hypothesis:l4-the-label-authority-falls-back-to-mains-committed-row-and-every-key-cell-writer-commits-and-pushes-its-own-row@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 29ab75d15cabaae8
season: 2
title: label authority falls back to MAIN committed key; key-cell writers commit+push own-row
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-cf339ebf-4c7300

## Experiment

**Build order (g15.26, hyp:l4-the-label-authority-falls-back-to-mains-committed-row-and-every-key-cell-writer-commits-and-pushes-its-own-row).** Measured the pre-fix state, IMPLEMENTED all three clauses, proved on the built bytes with real-git / bare-remote fixtures.

**Pre-fix (measured):** send.py `_load_rows` returned the pushed ref's rows wholesale — a pushed row for a seat that existed but named NO pubkey/sig_scheme WON over MAIN's committed row that did (defect in clause 1). `_commit_spawn_row` committed but never pushed (docstring "never a push"); keygen and the rotate mint functions wrote key cells and stopped — a freshly minted/rotated post's signed dms read UNKEYED/FORGED to every reader until the hourly push.

**Implemented:**
- **send.py clause (1):** `_load_rows` now runs pushed rows through `_merge_main_committed_keys` (new), which for each pushed row naming no `pubkey`/`sig_scheme` inherits the SAME seat's key cells from `_seats_committed_rows` (new) — `git show HEAD:<posts|seats.md>` at the shared graph root via `_shared_seats_path`, never the dirty working copy, never `_locally_loaded_rows`. A pushed row WITH a key stays authoritative (never overridden by a stale MAIN key). The inheriting row is tagged `_main_committed`. `_in_git_repo` (new) is a filesystem-only probe so a gitless fixture never spawns git (the send test guard forbids non-tmux subprocesses).
- **send.py clause (3):** the label site `_verify_block` appends `, main-committed` INSIDE the scheme parens when a tagged row verifies (`VERIFIED <seat> (<scheme>, main-committed)`). `_label_for_sig` verdict logic (SL6.03) untouched.
- **rotate.py clause (2):** new `_push_season_branch(root)` pushes MAIN's checked-out branch to `origin` — best-effort, prints exactly ONE line to stderr naming the remote error on failure, never raises. `_commit_spawn_row` resolves the seats file through `_ack_seats_path`/geometry_config (post-rename posts.md-safe, never the literal seats.md) and now calls `_push_season_branch` after a successful commit. `_rotate_first_key` commits+pushes its first-mint key-cell write through `_commit_spawn_row` (best-effort).
- **send.py keygen:** single AND `--all-live` now commit+push through a new `_commit_push_seat_row` → `rotate._commit_spawn_row` (SL6.01's helper by name, no second copy); a refused commit or failed push prints one note line and never fails the mint.

**Tests added (real git + bare remote fixtures, fake tmux):**
- `test_falsifier1_rotation_alert_verifies_main_committed_under_enforcing` (send.py): first-mint keys the row and commits it onto MAIN's HEAD; origin's pushed row is still UNKEYED; the signed rotation-alert reads `VERIFIED seat-a (ed25519, main-committed)` under `comms.verify=enforcing` on the RECIPIENT side — never UNKEYED, never FORGED, never REFUSED, never withheld.
- `test_falsifier2_pushed_key_stays_authoritative_over_stale_main` (send.py): pushed row keyed with A + MAIN HEAD keyed with B → a sig under B reads FORGED (A wins), no `main-committed` tag.
- `test_keygen_commits_and_pushes_own_row_to_bare_remote` (send.py): after keygen, `origin/season/s2`'s row carries the pubkey and MAIN's tree is clean.
- `test_keygen_mint_survives_a_failed_push` (send.py): no-origin push → mint still returns the key path; `push: FAILED --` printed to stderr.
- `test_rotate_first_key_commits_and_pushes_first_key_to_bare_remote` (rotate.py): rotate first-mint pushes the pubkey onto origin; MAIN clean.
- `test_commit_spawn_row_pushes_successor_row_to_bare_remote` (rotate.py): spawn/successor row commit pushes to origin; MAIN clean.

## Evidence

`python3 -m pytest extensions/agi/tests/test_send.py extensions/agi/tests/test_rotate.py -q` → **422 passed** (416 pre-existing + 6 new).

Broader coverage of changed files (test_send.py + all test_rotate*.py + test_seatsig.py + test_heal_seats.py): **730 passed**.

Key observed label output (falsifier 1): `VERIFIED seat-a (ed25519, main-committed)` with the alert body printed in full, no REFUSED, no withheld. Falsifier 2 observed `FORGED`. Bare-remote tests observed `origin/season/s2` / `origin/master` rows carrying the pubkey after keygen / rotate-first-mint / spawn-row commit, and `push: OK` in stderr.

**Caveats:** the rotation-alert fixture drives the same label-authority path on a freshly first-minted rotated seat, not a full `cmd_rotate_self` run (which needs the tmux/spawn machinery); the alert's guaranteeing behavior — a signed alert reads VERIFIED/RETIRED, never FORGED, immediately after the key flip — is exactly what clause-1's per-seat committed-row fallback delivers.

## Agent Notes
Built all 3 clauses: _load_rows falls back per-seat to MAIN's committed key via git show HEAD (never dirty copy); pushed keyed row stays authoritative (falsifier 2 FORGED); every key-cell writer (keygen single+--all-live, _rotate_first_key, spawn-successor commit) commits own-row through _commit_spawn_row (now geometry_config-resolved) and pushes via new _push_season_branch (one-line error, never fails mint). Label VERIFIED <seat> (<scheme>, main-committed). 422 pass in test_send+test_rotate; 730 across rotate family.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (parent a00-4a8d98b3, SL6.05). WHAT THE BRIEF SAID (the target hypothesis testable_claim): clause (1) _load_rows resolves the from-seat row pushed-first and, when that pushed row names no pubkey/sig_scheme, falls back per-seat to MAIN\x27s COMMITTED row (git show HEAD:<seats.md> at _shared_graph_root, never the dirty copy); a pushed row WITH a key stays authoritative. Clause (2) every key-cell writer (keygen single + --all-live, _rotate_first_key, _rotate_successor_key) commits its own-row hunk through SL6.01\x27s helper then pushes; a push failure prints one line and never fails the mint/rotation. Clause (3) the label names its authority. WHAT THE MACHINE ACTUALLY DOES (read the staged diff AND re-ran it): send.py _load_rows now routes a non-empty pushed row set through _merge_main_committed_keys (send.py, new), which inherits pubkey/sig_scheme/enc_scheme/key_history per-seat from _seats_committed_rows (git show HEAD:<rel> at the shared graph root, guarded by the filesystem-only _in_git_repo so a gitless fixture spawns no git) and tags the row _main_committed; a pushed row already naming a key is returned untouched. _verify_block appends \", main-committed\" inside the scheme parens only when label.startswith(\"VERIFIED\"), leaving _label_for_sig\x27s verdict logic (SL6.03) untouched. rotate.py _push_season_branch is new (best-effort, one stderr line push: OK/FAILED/SKIPPED, never raises); _commit_spawn_row now resolves seats via _ack_seats_path (post-rename-safe) and calls _push_season_branch after a successful commit; _rotate_first_key commits+pushes when _row_keyed; _rotate_successor_key rides the same spawn-row commit+push. send.py keygen (single and --all-live) commits+pushes via _commit_push_seat_row -> rotate._commit_spawn_row. RAN IT: python3 -m pytest extensions/agi/tests/test_send.py extensions/agi/tests/test_rotate.py -q -> 422 passed, including the 6 new tests and every pre-existing FORGED/enforcing/ack test. NEAR MISS: a plausible implementation satisfies the words of clause (2) by pushing only from _commit_spawn_row but leaving send.py keygen and _rotate_first_key as bare writers — the claim names all four writers, and keygen/--all-live would then still read UNKEYED to every reader until the hourly push exactly at the moment the channel matters; the artifact wires all four. SECOND NEAR MISS: merging MAIN\x27s key into a pushed row that ALSO carries a foreign key_history would let a stale MAIN retirement shadow origin; the merge only fills cells that are empty, so a pushed key_history is never overwritten. DEVIATION OF NOTE, recorded not rejected: on a pushed ref that exists but yields ZERO rows, _load_rows now falls through to _locally_loaded_rows (dirty working tree) instead of returning None — the brief\x27s own prose (\"the working-tree rows only when the pushed ref yields NO rows at all\") describes that fallback, but it is a wider authority than the committed-row clause alone and is worth a reader\x27s eye; no test pins the empty-pushed case either way. CAVEAT: the rotation-alert fixture drives the first-mint + committed-row label path rather than a full cmd_rotate_self (tmux/spawn machinery), so the end-to-end alert is inferred from the clause-1 path, not run through rotate-self. Reviewed and accepted as proved.
<!-- THOUGHT:END -->
