---
id: experiment:a00-e82b333d-50bd4e
mint_id: d6dd79cd05a94c3ba796a9ee29dcbfa0
type: experiment
parents:
  - hypothesis:l4-sm48-integration-residue-merge-up-stamps-the-caller-unpushed-gate-scoped-card-mtime-floor-no-tier-caveat-unmeasurable-label-dead-stops-rotation
next_edges: []
confidence: 0.9
edited_by: a00-a6135607
evidence_runs:
  - experiment:a00-e82b333d-50bd4e
line_ceiling: 30
loop: hypothesis:l4-sm48-integration-residue-merge-up-stamps-the-caller-unpushed-gate-scoped-card-mtime-floor-no-tier-caveat-unmeasurable-label-dead-stops-rotation@s2
model: ~deepseek/deepseek-v4-flash-latest
probes: "P4(env/auth): env_seat with AGI_SEAT=sensei-director + AGI_AGENT_ID=a00-x -> no-tier=a00-x, kid=a00-x, parent=a00-x, director=sensei-director, prime_director=sensei-director; the no-tier director shape stamps a clock no seat gate reads (caveat now named in the SM.48b node). P5(wire+gate): grepped every reader of the check-4 label -- rotation_alert.py:671 uses startswith (survives the suffix); the two exact-equality test filters only ever hit the measured cases (_last_ts not None) so the suffix cannot break them; source contains the unmeasured arm and the measured/BLOCK labels stay byte-identical. P6(gate): inspect.signature(_prepare_checks) == [root, seat, perform]; calling with stops_rotation=True raises TypeError; grep finds no residual stops_rotation outside the retirement docstring and the test file; _stops_has still referenced twice in rotate.py. Ran: /home/ubuntu/work/agi/.agi/worktrees/post-sensei-director/.agi/sessions/iter-SM.68/a00-a6135607/parent_probe_kid2.py -> ALL PARENT PROBES PASSED; plus a regression run of test_last_act + test_rotate_prepare + test_rotate_verb + test_rotate -> 399 passed."
production_lines: 21
profile: balanced
push_further: "Re-run at this node: audit rotation_alert.py and any other reader that keys on check 4's label for a substring that the new '(unmeasured: no own act)' suffix could silently satisfy (startswith survives, but an equality/complement test would not); and probe whether any real dispatch path spawns a director without AGI_TIER."
role: kid
scaffold_hash: 1c60a6866c406189
season: 2
title: "Slice B residues: no-tier director caveat named, unmeasured card label, stops_rotation retired by name"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e82b333d-50bd4e

## Experiment

Slice B (residues 4, 5, 6) of the SM.48 integration-residue hypothesis. Kid 2
of 2; slice A (items 1-3) landed at `de623a429` and was NOT touched. This is a
g15 build order: measure pre-fix, implement, prove on the built bytes. Ceiling
30 production lines.

Pre-fix probe (all three items, one script):
`.agi/sessions/iter-SM.68/a00-e82b333d/probe_prefix.py`

### Item 4 — the SM.48b no-`AGI_TIER` caveat was missing

**Pre-fix measurement:** `AGI_SEAT=sensei-director AGI_AGENT_ID=a00-x` with NO
`AGI_TIER` resolved `env_seat()` to `'a00-x'` (the agent id), and so did
`AGI_TIER=kid`; only `AGI_TIER=director` resolved `'sensei-director'`. The
hypothesis node documented only the tier-present arms, so a director-tier
process spawned without the literal stamps a clock no seat gate reads and its
card never stales — the exact rotation loop the `director` arm exists to fix,
undetected and untested.

**Fix:** `write.py note` on
`hypothesis:l4-sm48b-...-cannot-stale-the-director` names the case under
`## Agent Notes` (the sanctioned writer; provenance stamp from write.py).
**Test:** `test_no_tier_director_shape_resolves_the_agent_id` — one function:
`AGI_TIER=kid`/`parent` and no-tier resolve the AGENT id, the paired
`AGI_TIER=director` resolves the seat (the literal is what flips the order).
**Negative case:** no-`AGI_TIER` director shape is the falsifier itself and is
now pinned by the test.

### Item 5 — a missing stamp printed the same ok label as a measured verdict

**Pre-fix measurement:** fixture card with no stamp and no card commit gave
`card_stale -> (False, None)`, and check 4 appended
`(False, "card older than last commit", ...)` — byte-identical to a seat whose
clock WAS read and found fresh (which returns `(False, <ts>)`). The
unmeasurable state was unnamed.

**Fix:** `_prepare_checks` check 4 keeps the name `card older than last
commit`; when `card_stale is False and _last_ts is None` it appends
` (unmeasured: no own act)`. The `except` path now also sets `_last_ts = None`
so it lands in the same named branch. Measured-fresh and BLOCK labels are
unchanged.
**Test:** `test_card_check_names_the_unmeasurable_state` — the no-clock line
is `[ok]` AND contains `unmeasured`; the measured-fresh line is exactly
`[ok] card older than last commit`.
**Negative case:** measured-fresh still prints the plain label (asserted with
`==`).

### Item 6 — `stops_rotation` was dead code

**Pre-fix measurement:** `stops_rotation` was still a parameter of
`_prepare_checks` (signature check `True`) and its docstring still claimed it
gated the seats/posts exclusion, but the executable body never read it; the
only caller passed `stops_rotation=_stops_has`; the test
`test_check_4_is_identical_under_stops_and_plain` existed only to assert the
dead argument inert. The SL7.30 assertion had been DELETED, not re-anchored.

**Fix (option a, retire by name):** parameter removed from the signature and
the call site, the docstring paragraph replaced by a retirement note.
`_stops_has` is still live for the stoppable flow (`rotate.py:17514,17566`) and
was NOT deleted.
**Test:** `test_stops_rotation_parameter_is_retired_by_name` asserts
`"stops_rotation" not in inspect.signature(rotate._prepare_checks).parameters`.
**Negative case:** calling `_prepare_checks(..., stops_rotation=True)` now
raises `TypeError: _prepare_checks() got an unexpected keyword argument
'stops_rotation'`.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_last_act.py
  extensions/agi/tests/test_rotate_prepare.py -q` -> **67 passed**.
- `python3 -m pytest extensions/agi/tests/test_rotate_verb.py
  extensions/agi/tests/test_rotate.py -q` -> **332 passed** (`test_rotate.py`
  and `rotation_alert.py:671` key on the check NAME, which is unchanged;
  `startswith("card older than last commit")` still matches the named arm).
- `python3 extensions/agi/bin/links.py links` -> `3277 resolved, 0 broken`.
- `git diff --numstat -- extensions/agi/bin/rotate.py extensions/agi/bin/last_act.py`
  -> `21 12 rotate.py` (last_act.py untouched: item 4 is documentation plus a
  test, no production line). Well under the 30-line ceiling.

## Agent Notes
Slice B (items 4,5,6) of the SM.48 integration residue, kid 2 of 2. Item 4: the no-AGI_TIER director caveat is now named in the SM.48b node (write.py note) and pinned by test_no_tier_director_shape_resolves_the_agent_id. Item 5: check 4 names the unmeasurable state ('(unmeasured: no own act)') while measured-fresh and BLOCK labels stay byte-identical. Item 6: stops_rotation retired by name (signature, docstring, call site removed; _stops_has kept live) and the inert-param test replaced by a signature assertion. 21 production lines in rotate.py, 3 new/1 replaced tests. 67 + 332 tests pass, links 0 broken.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review of slice B (items 4-6). Read the bytes de623a429..36b420018, not the report: rotate.py +21/-12 (signature and docstring of _prepare_checks lose stops_rotation, check 4 gains the (unmeasured: no own act) suffix on the no-clock arm only, call site drops the kwarg), test_rotate_prepare.py replaces the inert-param test with a signature assertion plus the named-unmeasurable test, test_last_act.py adds the no-tier env test, and the SM.48b hypothesis node Agent Notes section gains the caveat (written through write.py note; left uncommitted by the kid because a hypothesis node is outside its round scope -- the parent round commit carries it). Independent probe script (parent_probe_kid2.py): env_seat maps no-tier/kid/parent to the agent id and director/prime_director to the seat; every reader of the check-4 label was grepped (rotation_alert.py startswith survives, the two exact-equality test filters only ever see measured cases); _prepare_checks has exactly [root, seat, perform] and stops_rotation=True raises TypeError with no residual mentions outside the retirement docstring; _stops_has stays live. Regression: test_last_act + test_rotate_prepare + test_rotate_verb + test_rotate -> 399 passed. Near miss ruled out: naming the unmeasurable state by mutating the shared label string would have broken the exact-equality filters in test_rotate_verb.py:476 and test_rotate_prepare.py:309 -- the kid extended the label only on the card_stale is False and _last_ts is None arm, so measured-fresh and BLOCK labels are byte-identical. Caveat inherited: item 6 retires stops_rotation by name but does NOT re-anchor the deleted SL7.30 behavioural assertion (a plain prepare blocking on a seats.md WORK commit); the targets wording offered either, and a signature test naming the retirement is the honest minimal build, but the SL7.30 behaviour itself is now pinned nowhere.
<!-- THOUGHT:END -->
