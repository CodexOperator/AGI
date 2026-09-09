---
id: experiment:a00-616ba934-61e934
mint_id: 9801b7b670844a0080d39f765a9ae9fd
type: experiment
parents:
  - hypothesis:l3w4-seat-rotation-loops
next_edges: []
confidence: 0.7
edited_by: a00-402cda8d
evidence_runs:
  - experiment:a00-616ba934-61e934
loop: hypothesis:l3w4-seat-rotation-loops@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d92d6996b62d0654
season: 2
title: A00 616ba934 61e934
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-616ba934-61e934

## Experiment

SD.16 assignment: (1) name `handoff.py` in `brief.py` (discoverability), (2) fold the read-then-hunk recipe in one line, (3) fix three measured friction points on `handoff.py`, (4) fixture-prove what the rotation claim (`hypothesis:l3w4-seat-rotation-loops`) is still missing, without duplicating existing tests. Survival mode (owner order) bans launching any seat, so the live half of the rotation claim stays banked honestly.

**1+2. brief.py — the `_kid` template** (extends SD.14's write.py partial-verbs segment). Added two segments at lines 1144 and 1150:
- discoverability: `HANDOFF SECTIONS: ...handoff.py sections` lists claimable sections; `... claim --seat <S> <sec>` claims one; `... read <sec>` serves just that slice (83x cheaper than the file).
- read-then-hunk recipe: `To patch a node body: write.py <id> 'read body N:M' first and build the hunk from those exact bytes` (the applier's body view is offset one from a naive split on BODY:BEGIN; `read body` shares it).

**3. handoff.py — three friction fixes, each with a test:**
- (a) `norm_section()` strips a leading `## ` so the tool's own `sections` output is copy-pasteable into `claim`/`read`/`write` (was: `claim` refused the printed form).
- (b) `_holder_opts()` adds `--seat` as an alias for `--holder` on claim/release/read/write (every other seat-aware entry point spells it `--seat`).
- (c) omitting the holder now prints WHICH flag is missing — `REFUSED: read needs --holder <seat> (or --prime / --whole)`, `write needs --holder <seat> (or --prime)`, `claim needs --holder <seat> (or --seat)` — instead of `REFUSED: None does not hold a claim ...`.

Verified live (temp dir): `claim '## §5 Verify' --seat me` returns claimed; bare `read`/`write`/`claim` each return 1 naming `--holder`.

**4. Rotation claim fixture audit.** Read `test_rotate.py` (81 tests) before writing, per instruction. Every clause of the claim's mechanism is ALREADY fixture-proved; adding copies would lie in the count. Covered: `test_alarms_once_holds_below_threshold` (no dm below), `test_alarms_once_dms_holder_when_due_then_stops` (exactly ONE dm at/over), `test_rotate_self_dry_run_reuses_plain_name_no_roman` (plain seat name, never a Roman numeral, gen N+1), `test_rotate_self_renames_window_before_respawn`, `test_rotate_self_kills_own_window_after_continue`, `test_seat_handoff_generation_bumps_on_rotation`, `test_rotate_self_cursor_ignores_stale_predecessor_continue` (L3.31 cursor — a planted stale `continue` does not falsely confirm), `test_rotate_self_refuses_when_successor_window_absent` (L3.33 false-success fix). Added ZERO new rotation tests on purpose.

**Fixture threshold note.** Existing tests drive the ladder at 0.25 (fake_ladder fixture), not the real `director_rotate_at` 0.35. The crossing mechanism is identical; the threshold is data. So the boundary behaviour (none below / exactly one at-and-over) is fixture-proved; 0.35 specifically is a config value the fixtures do not exercise.

## Evidence

- Full suite: `python3 -m pytest extensions/agi/tests/ -q` → **2254 passed, 1 skipped** (baseline 2249 + 5 new handoff tests). Duration 02:02.
- `links.py links` → 1760 resolved, **0 broken**. `grid_coverage_check.py` → clean, exit 0. `write_guard.py check` → silent, exit 0.
- New tests in `test_handoff.py` (all green): `test_norm_section_strips_printed_prefix`, `test_cli_claim_accepts_printed_form_and_seat_alias`, `test_cli_read_with_seat_alias_serves_section`, `test_cli_read_missing_holder_names_the_flag`, `test_cli_write_missing_holder_names_the_flag`.
- Manual CLI run confirmed all three friction fixes against a temp handoff.
- `snapshot-goals.py --render --check` abstained (exit 1: refusal to write an empty GOALS.md) — worktree-env quirk: `PROJECT_ROOT` env points at the checkout root, the tool treats it as the graph root and finds no `nodes/goal`. It is the safe guard refusing an empty write; I touched no goal nodes and no GOALS.md.

**Live-only (banked, not claimed):** a real rotation — successor spawned into a real tmux window under a reused plain name, answering `continue`, predecessor window renamed and killed only after the read-back — is the remaining evidence and the owner's standing gate (HANDOFF section 6 item 47). It could not be run this round: owner survival-mode order bans launching any seat. So: fixture-proved, live half banked.

## Agent Notes
brief.py names handoff.py + read-then-hunk recipe; handoff.py 3 friction fixes (norm_section accepts printed ## form, --seat alias for --holder, missing-flag msgs); 5 new tests; rotation claim fixture-audited (all clauses already covered, 0 dupes), live half banked by survival-mode order; suite 2254 passed 1 skipped, links 0 broken, grid_coverage + write_guard exit 0.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent SD.16 review: accepted at lean_proved:70. Verified bytes, not the report: brief.py:1144 names handoff.py, :1150 carries the read-then-hunk recipe; handoff.py has norm_section prefix-strip, --seat alias, and refusals that name the missing flag; test_handoff.py 14 passed live in this worktree. Zero duplicate rotation tests is correct — the seven claim tests already exist in test_rotate.py. The 70 not higher is exactly right: the live tmux rotation is banked by owner survival-mode order, not proved.
<!-- THOUGHT:END -->

SD.16 review: ACCEPTED at 70. brief.py discoverability + hunk recipe, handoff.py 3 friction fixes, 5 new tests, all verified by byte-grep and live test run by parent. Live rotation half honestly banked per survival-mode order.
