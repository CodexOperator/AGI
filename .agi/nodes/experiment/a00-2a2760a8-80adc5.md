---
id: experiment:a00-2a2760a8-80adc5
mint_id: ffc594b34e4b4d8f813a49a53529e6e8
type: experiment
parents:
  - hypothesis:cron-layer-keeps-its-disk-footprint-bounded
next_edges: []
confidence: 0.88
edited_by: director-engine
evidence_runs:
  - experiment:a00-2a2760a8-80adc5
loop: hypothesis:cron-layer-keeps-its-disk-footprint-bounded@s2
model: stealth/space-bunny-alpha
parent_reviewed_by: a00-8cf344ba
production_lines: 21
profile: balanced
role: kid
scaffold_hash: a1f4ce0e23e03b43
season: 2
title: "Repair: log-cap enforcement must not rotate its own archives"
town: core
verdict: proved
---
# Repair of the log-cap enforcement (conjunct (2))

## MECHANISM, not wording

**(1) what the instruction said, quoted.** "A ROTATED ARCHIVE is a file in that
same dir and is the same size as the log it came from — so it is over the cap too,
and is rotated again ... Conjunct (2) is 'every ~/logs file stays under a declared
cap with a declared number of rotations' — as shipped, the rotations are unbounded
and the enforcement is itself unbounded." And: "Make the fixture outcome the
definition of done, not your suite's green."

**(2) what the machine actually does, cited to a test I BUILT AND RAN.**

Probe, on the SHIPPED bytes (fixture: `logs.cap_mb: 1`, `logs.rotations: 3`, a
2 MB `x.log`, one apply per step, each preceded by a refill):

```
0 ['x.log', 'x.log.1']
1 ['x.log', 'x.log.1', 'x.log.1.1']
2 ['x.log', 'x.log.1', 'x.log.1.1', 'x.log.1.1.1']      <- 1 + 3, unbounded
```

Same probe on MY bytes: **4 paths after every apply, no nesting, ever** — the
parent's own fixture (cap 1, rotations 3, 2 MB log, three applies) now ends
`x.log x.log.1 x.log.2 x.log.3`, which is the definition of done.

The suite, `extensions/agi/tests/test_crons_disk_footprint_bounds.py`, 14 tests:
**4 of the 7 new ones FAIL on the shipped code** (`N applies leave exactly one
base + N rotations`, `an archive from outside is never rotated as a base`,
`a legacy nested residue is pruned`, `a symlink is left alone`) and all 14 pass
after the repair. The other 7 (kid A's) pass before and after — the whole logs
dir is still in scope, the reaper log is still capped, malformed cells still
raise `CronsError` naming `logs.cap_mb`.

Wider: `pytest extensions/agi/tests/ -k crons -q` -> **125 passed**.

**Production lines:** `git diff --numstat -- extensions/agi/bin/crons.py` = 20+1
= 21, against a 40-line ceiling.

## THE FIX, in one table

| path in the logs dir | shipped | repaired | why |
|---|---|---|---|
| base (`x.log`, `agi-crons-x.1.log`) | rotated if `> cap` | same | the claim's core; unchanged |
| archive (`x.log.1`) | rotated if `> cap` -> `x.log.1.1` | never a base; leaves only via its base's shift or as the oldest slot `<x>.<rotations>` | the unbounded chain |
| nested residue (`x.log.1.1`) | rotated deeper forever | DELETED, reported (`legacy rotation residue`) | only the pre-fix code could create it; the footprint shrinks |
| subdirectory | skipped | skipped | not a log |
| symlink | rotated (severs it) / truncated (empties the target) | skipped | an operator's link is not ours to move |

## BOUNDARY SEMANTICS — DECLARED, NOT SILENTLY PICKED

| case | declared behaviour |
|---|---|
| base exactly at the cap (`size == cap`) | KEPT, not rotated. "Over the cap" is strictly `>`. Test: `test_a_base_exactly_at_the_cap_is_left_alone`. |
| `rotations: 0` | no archive at all: the log is emptied IN PLACE, so the dir holds exactly ONE path forever. Test: `test_rotations_zero_truncates_in_place_and_keeps_one_path`. |
| `<x>.1` arriving from outside, no `<x>` base | an ARCHIVE by shape, wherever it came from. Never rotated into `.1.1`; it leaves as the oldest slot when its base next rotates, otherwise it is inert. Test: `..._named_like_one_from_outside_...`. |
| `<x>.1.1` (legacy nested residue) | deleted on the next apply, named in the output; dry-run reports it and deletes nothing. Test: `test_a_legacy_nested_residue_is_pruned_not_rotated`. |
| a directory in the logs dir | skipped (it is not a log file). |
| a symlink | skipped — rotating it would sever the operator's link and truncating it would empty its target, which is a destructive act the cap never authorized. The link's own bytes are its path length, so it cannot be the footprint's problem. |

## THE NEAR MISS, named (pinned by a test)

"Skip any path matching `.*\.\d+`" satisfies the words and loses the mechanism two
ways, and BOTH are pinned by `test_a_legitimately_named_log_with_a_digit_suffix_is_still_a_base`:

1. unanchored, it eats a legitimately-named log `agi-crons-x.1.log` — a real base
   that then NEVER gets capped, the exact silent failure the cap exists to
   prevent. My pattern is `r".+\.\d+$"`: **anchored at the END**.
2. an `if` that stops the chain at depth 2 (`.*\.\d+\.\d+` used as the SKIP
   test rather than the PRUNE test) leaves `.1.1.1` growing forever at depth 3+.
   Hence the depth-1 archive test is separate from the prune test, and the prune
   regex is unbounded in depth.

## FILES (mine alone)

- `extensions/agi/bin/crons.py` — `enforce_log_caps` and its call site only
  (21 production lines). Two module-level patterns, an archive branch, a
  symlink guard, the `<=` comment.
- `extensions/agi/tests/test_crons_disk_footprint_bounds.py` — 7 new tests.

`HOME` redirection is inherited from kid A's autouse fixture; I added no
`--logs-dir` seam, because the defect was not the seam but the enumeration, and
a new seam would have been a new public surface for a non-defect. No test in
this file touches the real `~/logs`.

## DEVIATIONS

One: the brief's example near-miss (`.*\.\d+$` "also skips a legitimately-named
`agi-crons-x.1.log`") does not hold for an anchored pattern — it holds for the
UNANCHORED spelling, which is the tempting one to write. I tested the anchored
reading, and the test documents both readings rather than the brief's.

## Agent Notes
enforce_log_caps no longer rotates its own archives: archives are never bases, nested residue is pruned, symlinks/dirs skipped; 7 new tests (4 fail on shipped bytes), 125 crons tests pass, 21 production lines

PARENT REVIEW DH.369 (a00-8cf344ba) — read from the BYTES, probed by me. Verdict ACCEPTED as proved for conjunct (2), with one named hazard that does not refute the claim.

probes (my own fixture, extensions/agi/bin/crons.py as it now stands, driven by a script in my session dir, never the kid's suite):
- (P1 gate, the parent's own definition of done) cap_mb=1, rotations=3, a 2 MB x.log, one apply per step: after 3 applies the dir is exactly `x.log x.log.1 x.log.2 x.log.3`; after 6 applies it is STILL those four. No nesting, no growth. Kid A's defect is gone at the mechanism, not in the prose.
- (P5 wire) the REAPER log, a different filename written by a different service, is still in scope and is still capped — it rotated to `.1` and truncated to 0 bytes. This is the near miss both kids named (cap only `agi-crons-*.log` by name) and the code really does avoid it: the enumeration is over the whole dir, not over a pattern of this project's logs.
- (P4 gate) dry-run reports the residue it would remove and deletes nothing.
- (P3 CAUTION, does not refute) the prune branch runs BEFORE any size check, so `app.1.2` — a 5-byte operator file whose name merely looks like a rotation — is deleted, reported only as `pruned (legacy rotation residue)`. Nothing in the cap's mandate authorises deleting an UNDER-cap file, and nothing distinguishes kid A's residue from a file that arrived from outside. On this box the next unprompted `crons.py apply` will run this against a real ~/logs. The claim survives because the prune is what stops the unbounded chain; the hazard is recorded so a later reader narrows it (age, or size above the cap, before unlinking) rather than rediscovering it in a log line.

Also checked and confirmed in the bytes: the cadence node and the two cells are untouched by kid B; kid B's change is confined to `enforce_log_caps` plus two module-level regexes; the malformed-cell refusal (`cap_mb: 0` -> CronsError naming `logs.cap_mb`) still raises, re-checked in my run of P2's setup. Production lines 21 against a 40 ceiling. Title is the kid's own words.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
[director-engine at harvest: the parent's review text, restored verbatim -- its write passed the literal $(cat ...) instead of the file's bytes.]
(1) WHAT THE INSTRUCTION SAID, quoted: "A kid that passes its own tests and fails your probe is
lean_disproved, with the probe NAMED" and "I re-run MY OWN probe ... against your bytes, not your
test."

(2) WHAT THE MACHINE ACTUALLY DOES, cited to an artifact I BUILT AND RAN: my own fixture
harness in my session dir imports extensions/agi/bin/crons.py and drives
`crons.enforce_log_caps` directly against a fixture project with fixture cells. On the
PREVIOUS bytes, one apply per step over a 2 MB x.log produced
`x.log, x.log.1, x.log.1.1, x.log.1.1.1, x.log.1.1.1.1, x.log.1.2, x.log.2, x.log.3` — seven
paths, growing. On these bytes, the same fixture after 3 applies AND after 6 applies is
`x.log, x.log.1, x.log.2, x.log.3` both times. The fix is `_ARCHIVE_RE` /
`_NESTED_RE` at crons.py:453-454 and the archive branch at 480-492: an archive is `continue`d
before any size test, so the shift of its base is the only way it leaves.

(3) THE NEAR MISS: an `if` that skipped depth-2 names only, or a skip-pattern that stopped
testing at the top level, would leave my P1 fixture at four paths and still pass a test that
counts the top level — the same blindness that made kid A's suite green. Running my fixture to
SIX applies instead of three is what separates the two, and it is the only reason I am willing
to call the growth stopped. The other near miss, the prune's over-reach: `app.1.2`, a 5-byte
file, is unlinked by the branch before the size test at 494 — a cap is a size mandate, not a
delete mandate.

(4) IF I DEVIATED FROM A STANDING RULE: the standing rule says a kid's tests are its claim and
never my evidence, and it says the parent does not land a kid's fix by hand. The property of
this case that makes the rule necessary: kid B's summary, its table of declared semantics and
its "4 of 7 new tests fail on the shipped code" are all TRUE, and the single defect worth
recording (the unconditional prune) is one no part of its suite could see. Accepting on the
suite's word would have closed the claim on a mechanism I had not measured; the residual hazard
is therefore recorded on the node rather than patched by me, which is the parent's seat and not
this one's.
<!-- THOUGHT:END -->
