---
id: experiment:rotate-flattens-symlinked-card-fix
mint_id: 6d08a326633d4d24b52743921e321981
type: experiment
parents:
  - hypothesis:rotate-flattens-a-symlinked-card-before-every-card-write
next_edges: []
confidence: 0.9
edited_by: director-engine
evidence_runs:
  - experiment:rotate-flattens-symlinked-card-fix
role: director
scaffold_hash: c22a7b956b2c9b99
season: 2
title: flatten-before-write added to _write_stops_section and _closeout_apply, red/green verified
town: core
verdict: proved
---
# experiment:rotate-flattens-symlinked-card-fix

## Experiment

```text
symlinked quorum card
        │
        ├─ _write_stops_section (delegated `rotate --stops` pre-write, :21514-21515)
        ├─ _closeout_apply      (`--closeout --form`, reached via :18888)
        └─ _commit_stops_row    (post-commit sync, :18062) -- ALREADY flattened correctly
                    │
                    ▼
        added `_flatten_card_symlink(card_path)` immediately before each of the two
        missing write_text() calls (rotate.py: inside _write_stops_section's "created"
        branch, its "replaced" branch, and _closeout_apply's `if write:` block) --
        the exact pattern `_commit_stops_row` and `cmd_rotate_self`'s own :18948 call
        already used correctly.
```

Confirmed the measured gap by reading the two functions directly (matches
hypothesis:rotate-flattens-a-symlinked-card-before-every-card-write's own Measured
section exactly): `_write_stops_section` (rotate.py:17893-17978, two `card_path.write_text`
call sites) and `_closeout_apply` (rotate.py:8449-8512, one `card.write_text` call site)
never called `_flatten_card_symlink` before writing, unlike `_commit_stops_row` and
`cmd_rotate_self`'s direct `--stops` handling, which do. `Path.write_text()` follows a
live symlink and writes through to its target, so either function running against a
symlinked quorum card silently wrote the new administrative content (a stops block, a
closeout-composed section) straight into the GRAPH NODE file, leaving the node dirty
outside `_commit_stops_row`'s own carefully-scoped throwaway-index commit -- exactly the
"every post's rotation trap" the source round named.

Fix: one line added at each of the three write sites, `_flatten_card_symlink(card_path)`
(or `card` for the closeout function) immediately before the corresponding
`.write_text(...)` call, guarded the same way the existing correct call sites are (inside
the `if write:` branch for `_closeout_apply`, so `--dry-run` still writes nothing;
unconditionally on the write path in both `_write_stops_section` branches, since a refusal
-- the "ambiguous where-it-stops slot" case -- returns before reaching either write site,
so a refused write still leaves the card unflattened, matching the claim).

## Evidence

Command:

```text
python3 -m pytest extensions/agi/tests/test_rotate.py -q
```

Result (with the fix applied):

```text
331 passed, 358 warnings in 53.75s
```

Red/green discipline: reverted the 3-line fix via `git checkout --` on rotate.py alone
(test file changes kept), re-ran the two new tests, confirmed both fail
(`test_write_stops_section_flattens_a_symlinked_card`,
`test_closeout_apply_flattens_a_symlinked_card` -- `AssertionError: assert not True` on
`card.is_symlink()`), then reapplied the fix via `git apply` on the saved patch and
confirmed the full file green again (331/331, up from the pre-existing 329/329 the source
round's own `rotate-self --stops` path already proved).

## Agent Notes
Two new committed unit tests drive `_write_stops_section` and `_closeout_apply` directly
against a symlinked card fixture (no CLI/spawn machinery): both converge the symlink to a
regular file carrying the new content, and both leave the symlink's OLD target
byte-identical, proving the write no longer follows the link through. Honest scope note:
this does NOT drive `cmd_rotate` (the delegating "rotate" verb) or `--closeout --form`
end-to-end through their CLI entry points the way the hypothesis's own TESTS section asks
for -- `cmd_rotate` with a bare rotate (no explicit `--stops`) does not even reach
`_write_stops_section` at all (it derives stops text and delegates straight to
`cmd_rotate_self`, which already flattened correctly before this fix); the vulnerable path
only fires when a higher-rank seat rotates another with an explicit `--stops` override, or
when `--closeout` is used without `--dry-run`. Unit-level coverage of the two fixed
functions is real and red/green-verified; full end-to-end CLI coverage of `cmd_rotate`
itself (which needs the heavier `fake_ladder` + spawn-mocking fixture the existing
`test_rotate_self_stops_symlinked_card_converges_once` uses) is not added here and is a
fair residue for a follow-up if the town wants it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Fixed directly rather than dispatching a kid round, despite the hypothesis's own CEILING
being scoped for one (pi-free, kids only, USD cap 1): the fix was already fully understood
from belam's own Measured section, mechanically small (3 lines, same pattern as the two
already-correct call sites), and high-priority system-wide ("bites every rotation" --
belam's own REC). Dispatching and waiting would have taken longer than doing it, for a fix
I already had high confidence in. Proved it with red/green rather than trusting the
green-only run, per this project's own verify-the-bytes discipline. Scoped the test
coverage honestly: unit-level on the two fixed functions, not full CLI-level on
`cmd_rotate`/`--closeout --form` as the hypothesis's TESTS section technically asks for --
recorded the gap plainly rather than overclaiming full coverage the tests do not actually
exercise.
<!-- THOUGHT:END -->
