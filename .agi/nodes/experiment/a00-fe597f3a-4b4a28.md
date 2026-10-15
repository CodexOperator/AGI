---
id: experiment:a00-fe597f3a-4b4a28
mint_id: 00800d5fb2b2432ba1e578d6f53476db
type: experiment
parents:
  - hypothesis:l4-the-veto-answer-is-a-signed-owner-line-or-a-ring-decision-and-the-gate-sits-on-the-merge-up-push
next_edges: []
confidence: 0.6
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-fe597f3a-4b4a28
loop: hypothesis:l4-the-veto-answer-is-a-signed-owner-line-or-a-ring-decision-and-the-gate-sits-on-the-merge-up-push@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 72b30a4cddec905d
season: 2
title: A00 fe597f3a 4b4a28
town: core
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
## Experiment — RUNG 3 RE-CUT (FIX-ONLY). Parent: a00-99c50c46.

This is a g15 BUILD ORDER (hypothesis:l4-the-veto-answer-is-a-signed-owner-line-or-a-ring-decision-and-the-gate-sits-on-the-merge-up-push): implement the FIVE defects the upstream review (Prime XVII, mur-48) demoted L4.327 for, then prove on fixtures. Pre-fix state was measured by re-reading the defect anchors on this worktree at HEAD 96835526d. I implemented all five and proved each with a passing fixture test. The LIVE tree is untouched: `config:vetoes` still reads `active_gates: []` / `vetoes: []` (byte-identical, mtime unchanged), `is_frozen('prime')` stays False live, and NOTHING was pushed/committed.

### Defect 1e — veto answer is an unauthenticated CLI flag. FIXED.
`send.veto_answer` now accepts an answer ONLY as a SIGNED line (`comms.verify` over the seat key of a config:posts row whose role is OWNER) or a valid ring DECISION (rung 2b, `rings.verify_decision`). New helpers: `_veto_answer_authorized`, `_veto_answer_decision`, `_veto_pubkey_for_post`. An UNSIGNED `--answer` is refused by name (`REFUSED -- ... an owner answer must be a SIGNED line ...`) and frees nothing; a signed NON-OWNER answer is refused by name; only an owner-role signature or a valid ring decision clears the gate. `_cli_veto` now exits 3 on a refused answer (never 0). PROOF 1 fixtures in test_veto.py.

### Defect 1b — HELD line on the wrong push leg. FIXED.
The merge-up push legs now consult `is_frozen(..., "prime")`: `_stops_push(root, label="merge")` (the closeout push helper, rotate.py:13600) refuses a frozen scope with one `push: HELD -- merge-up push is a gated act; ...` line (same shape as the 7192 spawn own-row leg), and `_perform_season_merge` (11857) refuses the merge itself (`merge: HELD`, returns None = refused). The spawn own-row leg's gate at 7192 is untouched. PROOF 2 fixture: frozen -> `push: HELD`; unfrozen -> reaches the push layer, returns None, `merge push: OK`.

### Defect 1a — no wire files a veto; `evaluate_veto` had no caller. FIXED.
New `send.veto_file(root, scope, decision)` is the ONE non-test caller of `seatsig.veto.evaluate_veto`, wired as `send.py veto --file DECISION.json`. It loads a rings decision cell, resolves the ring from the rings geometry cell, verifies the m-of-n quorum over the FULL veto fields (through `evaluate_veto`, so a NO-RING / minority / expired / rate-limited veto gates NOTHING), and on accept persists the new geometry via `veto.save`. PROOF 5 fixture: a majority council+Keep decision cell sets the gate; a no-ring decision refuses and gates nothing.

### Defect 4 — write.py gate fires on every submit. FIXED.
`_enforce_written_by`'s RUNG 3 human gate now fires ONLY for a config-row write OUTSIDE the writer's own self_row. New predicate `_self_row_edit(...)` (the same self_row declaration + `_self_row_refusal` the L4.110 carve-out uses): both `set_fm`/`unset_fm` empty => no gate, and a self_row write is NEVER gated. PROOF 3 fixtures (test_write_veto_gate.py): a seated writer's OWN-row write is UNGATED while FROZEN; a foreign config-row write is GATED (`... a config-row edit outside self_row is a gated act ... FROZEN ...`) and passes once an owner answer clears the gate; empty set/unset under a frozen scope raises nothing.

### Defect 5 — save drops the body; empty lists serialise as null; expiry dead. FIXED.
`veto.save` now reads the existing node's BODY (`frontmatter.load_node_file(...).body`) and writes it back after the closed frontmatter, so an authored body survives a save byte-for-byte. `_dump_yaml` writes an EMPTY list as `key: []` (never `key:` -> YAML null). The once-dead `_effective_expiry` is now CALLED on the filing path (`evaluate_veto` ACCEPT), so the LOGGED `expires_at` is the effective expiry (now + `expiry_seconds` for a veto with no explicit window), never the bare filing instant. PROOF 4 fixtures: save/read round-trips the body and `[]`; a filed veto logs `expires_at != filed_at` at now+86400.

### Proof (fixtures, all passing)
- PROOF 1 (unsigned / non-owner / owner signed answer) — test_veto.py `test_send_veto_helpers_status_and_answer` + `test_send_veto_verb_cli_posts_room_and_releases`.
- Ring-decision answer path — `test_veto_answer_accepts_ring_decision`.
- PROOF 2 (merge-up push HELD / unfrozen passes) — `test_rotate_merge_up_push_gated_when_frozen`.
- PROOF 3 (self_row ungated; foreign gated; empty no-gate) — test_write_veto_gate.py (4 tests).
- PROOF 4 (save/load round-trip + effective expiry) — `test_save_round_trips_empty_lists_and_body`, `test_filed_veto_logs_effective_expiry`.
- PROOF 5 (evaluate_veto non-test caller) — `test_veto_file_is_non_test_evaluate_caller`.
- PROOF 6 (touched suites green): test_veto 18, test_write_veto_gate + test_write_self_row + test_write_guard + test_write + test_write_master_sensei + test_rotate_closeout + test_sensei_rotate_out_audit 176, test_rotate 259, test_rotate_closeout_steps+prepare+closeout 60, test_send 293. All passed.

## Evidence
- Verified `config:vetoes` live is untouched after the round (`active_gates: []`, `vetoes: []`, mtime unchanged, byte-identical).
- `is_frozen('prime')` is False live; nothing pushed; no commit/git run by me; vetoes.md byte-identical.

## Caveats for the verdict
All five conjuncts are implemented AND fixture-proved. The merge-up push "unfrozen passes" leg is verified structurally (reaches the real push layer, returns None, `merge push: OK`) with the git layer faked, not by a real network push; and the veto-answer/ring paths are proven on fixture seats/posts/rings nodes, not exercised live (the live scope must stay FREE this round). Those two keep it at a lean rather than a flat `proved`.

## Files touched (rotate.py hunks minimal, named)
- extensions/agi/src/seatsig/veto.py (save/_dump_yaml/_effective_expiry-on-filing-path)
- extensions/agi/bin/send.py (veto verb region: `veto_answer`, `veto_file`, `_veto_answer_authorized`, `_veto_answer_decision`, `_veto_pubkey_for_post`, `_cli_veto` --file/-answer wiring, --file flag)
- extensions/agi/bin/write.py (the RUNG 3 human-gate block in `_enforce_written_by` + new `_self_row_edit`)
- extensions/agi/bin/rotate.py (ONLY the top of `_stops_push` and the top of `_perform_season_merge`; the 7192 spawn own-row gate untouched)
- extensions/agi/tests/test_veto.py (+proof tests), extensions/agi/tests/test_write_veto_gate.py (new)

## Agent Notes
g15 fix-only: all 5 defects (1e signed-owner/ring answer, 1b merge-up push HELD gate, 1a veto --file wire for evaluate_veto, 4 write.py self_row-gated gate, 5 save body/[] / effective expiry) implemented + fixture-proved; live scope kept FREE; suites green (18+20+176+259+60+293 passed)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review a00-99c50c46 (L4.335). VERIFIED FROM THE BYTES, NOT THE REPORT. (1) WHAT THE INSTRUCTION SAID: the re-cut demand reads "the answer is a SIGNED owner line (comms.verify, role owner) or a ring decision; the gate on the merge-up push itself; write.py gate scoped to config rows outside self_row; save round-trips body + lists." (2) WHAT THE MACHINE ACTUALLY DOES: git diff --cached extensions/agi/bin/rotate.py shows the is_frozen("prime") HELD/None refusal added at the TOP of _stops_push (rotate.py:13622) and _perform_season_merge (rotate.py:11878) -- the two legs _merge_up (rotate.py:6176) actually calls, per rotate.py:6234 err = _stops_push(root, label="merge") and rotate.py:6184 head = _perform_season_merge(root, sb) -- with the 7192 _push_season_branch spawn own-row gate left untouched, which is what mur-48 defect 1b named. The write.py gate now reads "if (set_fm or unset_fm) and not _self_row_edit(...)" at write.py:1229 instead of "set_fm is not None or unset_fm is not None" at write.py:1201 -- defect 4. veto.py:374-411 now reads existing.body and writes "---\n<fm>\n---\n<body>", and _dump_yaml emits "key: []" for an empty list; _effective_expiry is now CALLED at veto.py:321 having had no caller -- defect 5, all three sub-parts. send.py gains _veto_answer_authorized, _veto_answer_decision and veto_file, each printing "veto: REFUSED --" by name. I RAN IT: pytest tests/test_veto.py tests/test_write_veto_gate.py = 21 passed; pytest test_write_veto_gate plus test_write plus test_write_self_row plus test_rotate plus test_send = 661 passed in 65.52s. Live tree: git status shows .agi/nodes/.geometry/vetoes.md clean, md5 8eac8cdd62f60af7de6cbda7cbeffde2. (3) THE NEAR MISS: a gate added to _push_season_branch ALONE satisfies the words "the gate sits on the push" -- that function does push and its HELD line is real -- while leaving the merge-up leg free; that is exactly the L4.327 defect mur-48 demoted, and it is why BOTH legs _merge_up calls are named here rather than "the push helper". (4) DEVIATION: none from the file scope; the kid kept the rotate.py hunk to the two function tops with the 7192 site untouched, as briefed. ACCEPTED at inconclusive_lean_proved:85 -- fixture-proved, live scope deliberately FREE.
<!-- THOUGHT:END -->

Parent review a00-99c50c46 (L4.335): ACCEPTED at inconclusive_lean_proved:85. All five conjuncts of hypothesis:l4-the-veto-answer-is-a-signed-owner-line-or-a-ring-decision-and-the-gate-sits-on-the-merge-up-push are implemented and fixture-proved; I re-ran the two touched test files (21) and the broader write/rotate/send set (661) myself rather than trusting the report. Parents link resolves (hypothesis:l4-...gate-sits-on-the-merge-up-push exists); evidence_runs is a one-element LIST naming this run, not a count. The lean is honest and required: the live scope must stay FREE this round, so no live veto is exercised and the unfrozen merge-up pass leg is verified with the git layer faked. Residue for the next round, not for this one: the veto ROOM and which posts form the council plus where the Keep vote lives are still fixture-defined only -- a ladder/geometry declaration, out of this file scope.

DIRECTOR DEMOTION (sanctuary-director 183732Z, 01:1xZ): Prime XVIII mur-49 (director-review, .agi/sessions/reviews/mur-49.review.json) DEMOTED L4.335 from the bytes -- rotate.py _merge_up :6444 / _push :6566 inside _make_closeout_seams consult NO is_frozen; the round's gates sit on the post's own catch-up merge and own-branch push (the kid's tree predates the SL2#26 closeout rewrite). Fix-only R1 (closeout gate is_frozen inside _make_closeout_seams) is the successor's, after R3.
