---
id: experiment:a00-deae9b09-fb6c31
mint_id: 4d4cc13b1e1b40edbf167a6a1a1292eb
type: experiment
parents:
  - hypothesis:l4-the-rotation-alert-hook-checks-the-project-first-prints-no-fraction-without-a-post-estimates-from-the-prompt-field-and-imports-rotate-lazily
next_edges: []
confidence: 0.85
edited_by: a00-3f04daac
evidence_runs:
  - experiment:a00-deae9b09-fb6c31
loop: hypothesis:l4-the-rotation-alert-hook-checks-the-project-first-prints-no-fraction-without-a-post-estimates-from-the-prompt-field-and-imports-rotate-lazily@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 1716dfdb4bb85e57
season: 2
title: "FIX-ONLY g15.25: four edits to rotation_alert.py (project-first P7, no fraction without a post, prompt-field estimate, lazy rotate import) proved on the built bytes"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-deae9b09-fb6c31

## Experiment

This is a **FIX-ONLY, build-order** round (g15.25 line (7), claim (1)-(4)). The
target node MEASURED the four defects on the pre-fix bytes; this round
IMPLEMENTED the claim and proved it on the built bytes, per
hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement.

### The four edits, all in `extensions/agi/hooks/rotation_alert.py`

**(1) P7 outside-project check runs FIRST** (`main`). Moved `root =
_project_root(cwd); if root is None: return 0` ABOVE the rc-3 no-transcript
refusal. Outside an agi project the hook now exits 0 and prints NOTHING
whatever the payload; the rc-3 `no-transcript-path` refusal (stderr)
fires only INSIDE a project, unchanged in shape.

**(2) No post resolved = NO fraction** (pin_missing). Was
`pin_missing = bool(seat) and (_canonical_pin(root, seat) is None)` — with
seat None the conjunction was False, so an UNRESOLVED seat printed a
fraction. Now `pin_missing = not seat or (_canonical_pin(root, seat) is
None)` — pin_missing keys on PIN-PATH COMPUTABILITY, never on bool(seat)
alone. `_meter` distinguishes the reason: a resolved post with an
uncomputable pin prints `post=<post> no-pin`; NO post resolved prints the
unresolved label `post=n/a no-post` — never a decimal.

**(3) Turn-1 estimate counts the PROMPT field, not the envelope** (`seen ==
0` branch). Was `est = int((len(raw) + transcript_bytes) / 4)` where `raw`
is the whole stdin JSON envelope. Now
`est = int((len(payload.get('prompt') or '') + transcript_bytes) / 4)`. A
20 KB envelope + 10-char prompt estimates from the 10 chars.

**(4) `import rotate` deferred off the pin-only path** (`_canonical_pin`).
Was `import rotate` → `rotate._sessions_dir(root)`, so EVERY per-prompt
meter homed the 11k-line rotate module. Now `import locations` →
`locations.shared_sessions_dir(root)` — the exact resolver that
`rotate._sessions_dir` is a one-line delegate to (rotate.py:293), so there
is no private copy of a path rule and no divergence; the pin-only prompt
imports geometry_config + locations but NEVER rotate. The over-line gate
helpers (:514/:525/:535/:642/:666) keep their lazy `import rotate` — those
are "the paths that need it" (only reached at threshold).

### Why three EXISTING tests were amended (not just appended)

Claim (2) makes "a fraction printed with seat None" the FALSIFIER, which is
exactly what three pre-existing meter tests asserted with the seat-less
`agi_project` fixture. They were updated (one line each) to
`monkeypatch.setenv("AGI_SEAT", "meter-director")` so a post resolves and a
computable pin lets the D1/D2/D3 fraction print — the fraction now belongs
to a RESOLVED post. Without this the fix itself reds them
(3 failed after the edit, 40 passed; verified). Claims tests (b) (rc-3
inside a project) and (f) (known seat, pin absent -> `no-pin`) already
existed unchanged as `test_b_missing_transcript_fails_closed` and
`test_missing_pin_prints_refusal_reason_not_fraction`.

### Five new tests appended to `extensions/agi/tests/test_rotation_alert.py`

- `test_a1_outside_project_no_transcript_is_silent` — outside a project, no
  transcript_path -> `rc 0`, empty stdout (FALSIFIER: any stdout outside a
  project). Fails pre-fix (was rc 3 + refusal).
- `test_a2_inside_project_no_transcript_refuses` — same payload inside a
  project -> `rc 3` + the keeper refusal on stderr, no command.
- `test_c2_no_post_prints_unresolved_label_no_fraction` — seat None ->
  `[meter] post=n/a no-post`, no digit where a fraction would go. Fails
  pre-fix (printed a fraction).
- `test_d2_est_counts_prompt_field_not_envelope` — turn-1 estimate =
  `int((len(prompt) + transcript_bytes) / 4)` asserted from a KNOWN prompt
  length (37) and KNOWN transcript byte size against the `(<est>/100000)`
  hole in the [meter] line. Fails pre-fix (counted the envelope).
- `test_e2_poisoned_rotate_import_still_prints_pin_only` — poisons
  `sys.modules['rotate'] = None` (next `import rotate` raises ImportError);
  a below-band resolved-post prompt still prints a REAL fraction.
  Fails pre-fix (broke into a `no-pin` refusal).

## Evidence

Test counts run on this base:

- `python3 -m pytest extensions/agi/tests/test_rotation_alert.py -q`
  -- **48 passed** (43 pre-existing + 5 new) in 4.3s.
- Neighbourhood
  `test_rotation_alert.py test_session_start_bootstrap.py
  test_session_start_seat_pre_spawn.py test_bin_help_smoke.py`
  -- **116 passed, 3 skipped** in 12.3s.
- Full engine suite `extensions/agi/tests/test_*.py` -- 3997 passed,
  14 skipped, 1 xfailed, 2 failed. The two failures are OUT OF SCOPE and
  pre-existing on this shared tree: `test_real_adapter_restart`
  (real-subprocess pi-adapter reaper test, unrelated) and
  `test_seat_alias_notice::test_static_scan_reports_site_count_and_names`
  (AST scan of `--seat` add_argument sites across rotate.py/send.py/etc;
  rotation_alert.py appears in NONE of the 22 sites — this is another
  worktree's in-flight edit to rotate.py, per this round's own EXCLUDED
  note). Neither test imports or references `rotation_alert`; the hook's
  scope is green.

The 3-test pre-fix red (all claim-(2) meter tests) was observed directly:
`[meter] post=n/a no-post` replaced the old fraction, exactly the FALSIFIER
the claim names. No git was run; `cli.py done` owns the commit.

## Agent Notes
FIX-ONLY: all four g15.25 edits landed in rotation_alert.py (P7 project-first, no fraction without a post, prompt-field estimate, rotate import deferred to the over-line path via locations.shared_sessions_dir). 5 new tests + 3 amended meter tests seat a post; neighbourhood 116 passed. Full suite's 2 failures are out-of-scope pre-existing (rotate.py/send.py --seat sites; adapter reaper).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-3f04daac, SL7.94), mechanism-not-wording. (1) WHAT THE INSTRUCTION SAID: the target claim demanded four edits — "the P7 outside-project check runs FIRST … outside a project the hook exits 0 and prints nothing whatever the payload"; "with no post resolved the [meter] line prints the unresolved label and NO fraction, and pin_missing keys on pin-path computability … never on bool(seat) alone"; "the turn-1 estimate counts len(payload.get(prompt)) + the transcript bytes, never len(raw)"; "import rotate is deferred to the code paths that need it … NOT executed on a prompt that resolves entirely from the pin file". (2) WHAT THE MACHINE ACTUALLY DOES, verified by me on this checkout, not by reading: hooks/rotation_alert.py main() now calls _project_root(cwd) before the transcript check; pin_missing = not seat or (_canonical_pin(root, seat) is None) and _meter picks reason "no-post"/"no-pin"; est = int((len(payload.get("prompt") or "") + transcript_bytes) / 4); _canonical_pin imports `locations` and returns locations.shared_sessions_dir(root)/f"{seat}.meter" — identical to rotate._sessions_dir, which rotate.py:316 reduces to exactly locations.shared_sessions_dir(root). Ran: pytest test_rotation_alert.py = 48 passed; neighbourhood (rotation_alert + session_start_bootstrap + session_start_seat_pre_spawn + bin_help_smoke) = 116 passed, 3 skipped. I re-ran the 5 new + 3 amended tests against a REVERTED copy of the file in /tmp (all four edits reversed, original import restored): 8 failed, 1 passed — so the new tests are real falsifiers, not tests that pass on both versions. Pre-fix failure modes matched the claim: rc 3 + refusal outside a project, a fraction printed with seat None, envelope-counted est, and a no-pin refusal from the poisoned rotate import. (3) THE NEAR MISS: claim (4) as written is satisfied by a version that merely MOVES `import rotate` below the transcript early-returns — that fragment loses the mechanism, because a pin-only below-band prompt still executes the import inside _canonical_pin, which is exactly where the per-prompt cost lives. The kid instead removed rotate from the pin path entirely by calling its one-line delegate. (4) DEVIATION: none from a standing rule; the two pre-existing full-suite failures the kid reported (test_real_adapter_restart, test_seat_alias_notice::test_static_scan_reports_site_count_and_names, 21 vs 22 --seat sites) are not from this round: I confirmed the seat-alias one is an AST census of bin/*.py, which this round did not touch.
<!-- THOUGHT:END -->
