---
id: hypothesis:a-capture-latch-is-keyed-by-session-and-never-swallows-the-imperative
mint_id: ad684f1804ba466f849fac9e54619435
type: hypothesis
parents:
  - goal:g7.33.15
next_edges: []
edited_by: director-engine
scaffold_hash: 212543673ab92521
season: 2
testable_claim: The captured stamp is keyed by session so a successor is never latched by its predecessor capture, and a latched capture still lets main() print the over-line rotate-now imperative.
title: "a capture latch is keyed by the session that captured and never swallows the over-line imperative (assigned: director-engine)"
town: core
---
# hypothesis:a-capture-latch-is-keyed-by-session-and-never-swallows-the-imperative

# hypothesis:a-capture-latch-is-keyed-by-session-and-never-swallows-the-imperative

## Measured (thought-master TMM.225, 2026-09-26 13:21Z; read against rotation_alert.py)
- The capture latch is per SEAT, not per seating: `capture-<seat>.json` holds `{"captured": ts}` with no session;
  `_force_capture` (~L866) returns `capture-latched` on it, and `main()` (~L1496, EF.22) re-stamps only when a NAMED old
  session differs -> every successor of a captured seat is latched from birth.
- `_captive_rotate` (~L938) returns True on `capture-latched`, so `main()` returns BEFORE the over-line IMPERATIVE: a
  latched director above 0.40 sees only `[meter]`, never "rotate now". director-engine gen 24 and director-thought gen 34
  were both latched; TM renamed the stamps by hand 13:20Z (`*.stale-20260926T1320Z`, reversible).

## CLAIM
The capture latch is keyed by the SESSION that captured (EF.22's rule applied to the `captured` stamp): a new session
of the same seat is never latched by its predecessor's capture; and a latched capture never suppresses the over-line
imperative -- `_captive_rotate` returning on `capture-latched` still lets `main()` print the rotate-now line.

## Falsifiers
1. A stamp `{"captured": ts, "session": "old"}` + a hook run as session "new" at f >= 0.85 x line returns `capture-latched` -> disproved.
2. A stamp with NO session (legacy) latches a new session -> disproved.
3. A latched session above the line gets no imperative line on stdout -> disproved.
4. test_rotation_alert*.py regress -> disproved. (AGI_HOOK_NO_SPAWN + tmp AGI_ROTATION_STATE_DIR only.)
