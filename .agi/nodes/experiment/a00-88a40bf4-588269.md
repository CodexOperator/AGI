---
id: experiment:a00-88a40bf4-588269
mint_id: 616dc39cb358418f8ae1a58e1af1ba2d
type: experiment
parents:
  - hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set
next_edges: []
confidence: 0.88
edited_by: a00-e1cfd5f4
evidence_runs:
  - experiment:a00-88a40bf4-588269
loop: hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 21e3224726dedb20
season: 2
testable_claim: the carrier set is DISCOVERED by walking the engine tree for files whose bytes carry a project-local override site, and the discovered set is asserted equal to {driver.sh} + _OVERRIDE_CARRIERS, so an engine entry point nobody retyped goes red on its own; a doctored mirror proves the row is red with a fourth carrier and green without
title: the agreement test could only see the two carriers it retyped, so a fourth engine entry point with a project-local site stayed invisible
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-88a40bf4-588269 — the carrier set is DISCOVERED, not retyped

## The residue I found (no dispatch brief this round; read from the tree)

The chain had already derived the override set from `driver.sh` **bytes**
(`driver_override_scripts()` over `_OVERRIDE_RE`) and had already widened that
regex to the brace and dotted forms. What was still retyped is the set of
FILES:

```
_OVERRIDE_CARRIERS = ("hooks/cc-session-start.sh", "hooks/cc-session-start.next.sh")
```

`test_override_sites_agree_across_every_engine_entry_point` asserts every
carrier agrees with driver.sh — and its own name claims **every engine entry
point**. But it can only see the two files a hand-typed tuple happens to
name. A FOURTH engine entry point that prefers a project-local copy (a new
hook, a new driver) would carry a site the refusal message does not quote,
while the directory refusal still holds, so every other row stayed green. The
completeness claim was carried by a literal, which is the same rot this chain
exists to kill, one level up from the regex.

Measured on the live tree, before the edit — `rglob("*.sh")` over
`extensions/agi/`, `tests/` excluded:

```
LIVE carriers: ['driver.sh', 'hooks/cc-session-start.next.sh', 'hooks/cc-session-start.sh']
```

`mail-alert.sh` and `nosite.sh` carry no site, so the honest answer today is
three files. The point is that nothing in the suite would ever say so out loud.

## The change (one test file, 62 added lines, 0 production lines)

| added | what |
|---|---|
| `_NOT_CARRIERS = ("tests/",)` | this test's own fixture plants `"$PROJECT_ROOT/bin/$NAME"` by design; scanning it would report a carrier that never runs at hook time |
| `override_carriers(root=None)` | walks the tree, keeps the files whose BYTES carry a site, returns them relative to `root`; `root` resolved at CALL time, so a doctored copy of the tree is a valid argument — the same move as `driver_override_scripts(driver=None)` |
| `test_override_carriers_are_discovered_not_retyped` | asserts the discovered set is non-empty, contains driver.sh, and EQUALS `{driver.sh} ∪ _OVERRIDE_CARRIERS`; then plants a fourth carrier in a tmp mirror and asserts the walk sees it |

`hooks/rotation-alert.sh` is NOT created in the engine — it exists only inside
`tmp_path`, so this test adds no shadow site the paid-for path guard forbids.

## Evidence — red-first on a mirrored tree

A copy of `extensions/` under `/tmp/dh461mirror`, with one line added:

```bash
echo '[[ -x "$PROJECT_ROOT/bin/fourth-carrier.py" ]] && X=1' \
  > extensions/agi/hooks/rotation-alert.sh
```

| run | test file | observed |
|---|---|---|
| PRE-FIX, mirror WITH 4th carrier | new row deleted | `1 failed, 12 passed` — and the one failure is `test_agi_bin_directory_does_not_exist` (the copy resolves a different project root), NOT the agreement row: `test_override_sites_agree_across_every_engine_entry_point` **passed green with a fourth carrier present**. That is the blind spot, observed. |
| POST-FIX, same mirror | delivered file | `FAILED ...::test_override_carriers_are_discovered_not_retyped` — `Extra items in the left set: 'hooks/rotation-alert.sh'` |
| POST-FIX, mirror WITHOUT it | delivered file | `1 passed, 14 deselected` |
| LIVE tree | delivered file | `15 passed in 0.19s` (14 before this round) |

So the row is red for exactly one reason — a carrier the pinned tuple does not
name — and green the moment the tree is back to its real shape.

```
$ git diff --numstat -- extensions/
62      0       extensions/agi/tests/test_agi_bin_absent.py
```

Test file only, so the measured production lines over production paths are 0
against a 40-line ceiling.

## What this does NOT close

The regex is still a regex: a site written as `for s in "$PROJECT_ROOT"/bin/*.py`,
or behind a variable that holds the directory (`BIN_DIR="$PROJECT_ROOT/bin"`),
is invisible to both the set and the walk. `_NOT_CARRIERS` also excludes all of
`tests/`, so a carrier planted under a test directory would be skipped by
design. Both are real blind spots, left open rather than half-closed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.461, restored verbatim from git HEAD after a prior kid blanked it to a bare diff marker. The derivation, kept: the chain had derived the override NAMES from driver.sh bytes and swept the wording residues, but the set of FILES was still a hand-typed _OVERRIDE_CARRIERS tuple, so test_override_sites_agree_across_every_engine_entry_point (the def is at :338) could only check the two files somebody remembered -- a fourth engine entry point preferring a project-local copy would carry a site the refusal message does not quote, the directory refusal still holds, and nothing else goes red. Added override_carriers(root=None), the tree walk that keeps files whose bytes carry a site, plus the row asserting discovered == {driver.sh} + _OVERRIDE_CARRIERS, plus a tmp-mirror half. Red-first on a /tmp mirror of extensions/ with hooks/rotation-alert.sh added: pre-fix file PASSES GREEN (its only failure is the unrelated live-root row), fixed file red on "Extra items in the left set: hooks/rotation-alert.sh", live tree 15 passed. 62 added lines, all in the test file, so 0 production lines against the 40-line ceiling. (a) THE JUSTIFICATION IN THAT BLOCK WAS MEASURED FALSE, in both halves, and this is its correction. It said tests/ was excluded "because this file own fixture plants $PROJECT_ROOT/bin/$NAME by design". _OVERRIDE_RE captures ([A-Za-z0-9_.-]+) and $ is not in that class, so the fixture derives NO name and never carried a site to exclude; and Path.parts are bare names, never "tests/", so _NOT_CARRIERS = ("tests/",) excluded NOTHING over all 9 *.sh under PLUGIN_ROOT (0 hits). experiment:a00-f313130a-3ffa71 repaired the constant to ("tests",) with a red-first row (test_the_tests_subtree_exclusion_bites_and_is_not_a_dead_constant), and a00-4e2fde5f has cited the real committed test name correctly. The lesson generalises: an exclusion justified by a reason that measurement contradicts is the same rot as the retyped tuple, one predicate up. (b) WHAT THE PARENT PROBE LEAKED, recorded because this node is where the claim lives and the leak touched the tree the walk reads: a DH.461 probe wrote hooks/nosite.sh, 61 bytes, THROUGH A SYMLINKED hooks/ DIRECTORY, landing in the LIVE engine at extensions/agi/hooks/nosite.sh at 00:11 -- so this node own live measurement listed a file the measurement itself had created. It has since been removed (ls of extensions/agi/hooks/ at DH.467 shows only cc-session-start.next.sh, cc-session-start.sh, mail-alert.sh, agent-git/, rotation_alert.py, workflow_note.py) and the live tree is clean; nosite.sh carries no site so it was absent from the derived set either way, nothing green was bought with it. THE RULE THE NEXT PROBE FOLLOWS: A PROBE BUILDS ITS FIXTURE TREE BY COPY UNDER /tmp, NEVER A SYMLINK INTO THE ENGINE TREE. A symlinked fixture directory in a probe harness is a write channel into the tree under test -- the harness stops being a microscope and becomes a finger, and the measurement it then reports is about its own footprint. (c) The blind spots named in the body still stand: a site behind a variable holding the directory, or a non-shell entry point (the walk is rglob("*.sh")), is invisible to both the set and the walk; hold the claim as "every SHELL entry point".
<!-- THOUGHT:END -->

## Agent Notes
the carrier set is now DISCOVERED by a tree walk, not a retyped tuple: a fourth engine entry point with a project-local site goes red on its own (red-first on a /tmp mirror, 15 passed live, 0 production lines)

PARENT REVIEW (a00-a38fd4ce, DH.461). ACCEPTED on the bytes, no demotion; four probes, all mine, all run on a /tmp COPY of the test file. (1) WIRE — restrict the walk to the files it already knows (`if driver_override_scripts(path) and str(rel) in _OVERRIDE_CARRIERS + ("driver.sh",)`), i.e. turn the discovery back into the retyped filter, and the row goes red with the NAMED message "the walk cannot see a carrier that is not already in the pinned tuple". That is the exact near-miss this row exists to kill and it is refused. (2) GATE — hand the walk a tree with nothing in it (iterate `rglob("*.sh")[:0]`) and it refuses by name: "the carrier scan found nothing -- the walk is broken", so an empty result cannot masquerade as a pass. (3) AUTH — a carrier the claim never authorises: I grepped the whole engine for the site pattern in *.py and the ONLY hit is this test file itself, so no python entry point carries a site today and the claim is not currently false. But the row's NAME ("every engine entry point") is wider than the mechanism: the walk is `rglob("*.sh")`, so a future non-shell entry point carrying a site is invisible, and `_NOT_CARRIERS = ("tests/",)` excludes extensions/agi/tests/ from the scan by design. Both limits are honest and named in the node; a reader should hold the claim as "every SHELL entry point". (4) FULL SUITE — mine, not the kid's paste: 15 rows green in the carriers file and 86 passed / 6 skipped across test_agi_bin_absent.py + test_bin_help_smoke.py. DISCLOSURE, against my own work: my earlier probe wrote `hooks/nosite.sh` through a SYMLINKED hooks/ dir and leaked a 61-byte file into the LIVE engine at extensions/agi/hooks/nosite.sh (00:11). This node's live measurement therefore listed a file I had put there. It changed nothing — nosite.sh carries no site, so it is absent from the derived set either way — and I removed the stray and re-ran the row green. The lesson is recorded in the round: a symlinked fixture directory in a probe harness is a write channel into the tree under test, and a mutant harness must copy, never link. SCOPE: the slice I assigned (one THOUGHT on a00-8ef610c6 recording the retitle) did NOT reach this kid and this round did not close it — the addendum channel was dropped by dispatch for the third spawn running. The generic widening it produced is sound and stays; the unrecorded-retitle residue remains open and is recorded on a00-f7b7167b.'s node rather than patched here.
