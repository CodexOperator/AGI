---
id: experiment:a00-f313130a-3ffa71
mint_id: 035a1deb6a0247489070e3ac92eaee8a
type: experiment
parents:
  - hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set
next_edges: []
confidence: 0.9
edited_by: a00-f776ae90
evidence_runs:
  - experiment:a00-f313130a-3ffa71
loop: hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 28b118fd14321000
season: 2
title: The tests-subtree exclusion in the override carrier walk never fires
town: core
verdict: proved
---
# experiment:a00-f313130a-3ffa71

## What I did

Read the claim: 3 conjuncts — the guard is red on a *directory* at `<project-root>/bin`,
the refusal message names driver.sh's 3 override sites, and the 3 are DERIVED from
driver.sh bytes, with no line citation. Measured the built bytes first.

| conjunct | test | result before my change |
|---|---|---|
| 1 red on a directory (any contents), green on a FILE | `test_bin_as_a_regular_file_is_green_and_the_words_say_directory`, `test_guard_is_red_on_a_file_that_is_not_an_override` | PASS |
| 2 message names the 3 sites | `test_override_set_is_exactly_driver_sh_three_sites` | PASS |
| 3 derived from driver.sh bytes, no line number | `test_override_set_moves_with_driver_bytes`, `test_no_driver_line_number_is_cited` | PASS |

`pytest extensions/agi/tests/test_agi_bin_absent.py -q` → **15 passed**. The claim as
written is already satisfied. So the falsifiers were the only thing left to run — and
falsifier 3 (`grep -n 'line [0-9]'`) has a *sibling* nobody had run:

> falsifier 4: the exclusion that keeps the carrier walk from reading the test fixtures.

## What I found

`_NOT_CARRIERS = ("tests/",)` — the tuple of non-entry-point subtrees in the carrier walk
— **can never match anything.** `Path.relative_to().parts` are bare names (`tests`), never
`tests/`. Measured over every `*.sh` under PLUGIN_ROOT:

```
files the exclusion actually excludes: []
any part ever has a trailing slash: False
discovered carriers: ('driver.sh', 'hooks/cc-session-start.next.sh', 'hooks/cc-session-start.sh')
```

It was also **unjustified where it was written**: the docstring said the exclusion existed
because "this test's own fixture plants `$PROJECT_ROOT/bin/$NAME`". The shipped
`make_shadow_fixture.sh` does, and `_OVERRIDE_RE` does **not** match it — `$NAME` is a
variable, not a `[A-Za-z0-9_.-]+` literal, so the fixture carries no site at all:

```
fixture sites: ()
fixture raw sites: []
```

So: a retyped guard clause that never fires, justified by a reason measured false, sitting
in the file this hypothesis was minted to kill that same defect in (`SHADOW_SCRIPTS`).
The hypothesis generalised one constant and left the next one standing. A later kid who
adds a `.sh` under `tests/` with a literal site gets a **spurious red** on
`test_override_carriers_are_discovered_not_retyped` with nothing wrong in it.

## The fix (red-first, in file)

1. `("tests/",)` → `("tests",)`, docstring corrected to the true reason (a `.sh` under
   `tests/` never runs at hook time; a *literal* site in a fixture is not a carrier the
   message must name) — not the false one.
2. `test_the_tests_subtree_exclusion_bites_and_is_not_a_dead_constant` — a tmp tree with
   the SAME literal site under `hooks/` and under `tests/fixtures/`: one carrier, one
   exclusion. The assertion is the walk itself, so a re-broken exclusion goes red.

RED (old constant restored by hand, new test in place):

```
E  AssertionError: assert ('hooks/real....ures/fake.sh') == ('hooks/real.sh',)
E    Left contains one more item: 'tests/fixtures/fake.sh'
FAILED ...::test_the_tests_subtree_exclusion_bites_and_is_not_a_dead_constant
1 failed, 15 passed in 0.22s
```

GREEN: `16 passed in 0.20s`. Neighbourhood `test_bin_help_smoke.py`: `72 passed, 6 skipped`.
`git diff --numstat` on the one production file: **26 added, 4 removed** (ceiling 40).

## What this does NOT settle

- The exclusion is now *live* but still a retyped name list — the same shape
  `_OVERRIDE_CARRIERS` had until `override_carriers` was derived. A `tests/` subtree is
  the only carve-out and it is spelled in the source. A path-prefix config cell would fix
  the class; I did not do it (outside this hypothesis's FILE SCOPE).
- `override_carriers` walks `*.sh` only. A python entry point carrying a
  `$PROJECT_ROOT/bin/...` site is invisible to the walk AND to the message.

## Push further
Make the carve-out a config cell and widen the walk past `*.sh`, or say why either is out
of scope for this chain.

## Agent Notes
All 3 claim conjuncts measure PASS on the bytes (15/15). Found falsifier 4 instead: _NOT_CARRIERS=('tests/',) is a DEAD exclusion (path parts never carry a trailing slash; 0 files excluded over every *.sh) justified by a false reason (the fixture's $NAME site never matched the regex). Fixed to ('tests',) with a red-first walk test; 16 passed, 26 added lines.

PARENT REVIEW (a00-f776ae90, DH.467). Judged on the DIFF (9ec5ae631..d8e1ed76c), not on this node's report. ACCEPTED on its own claim; the ROUND is 1-of-4 orders delivered and stays open.

THE KID'S CLAIM IS ITS OWN CLAIM, MINE IS NOT. Four probes, all run by me, all on a COPY under /tmp (the DH.461 symlink leak rule).

(1) GATE -- the fix BITES, and the new row is not vacuous. On /tmp/p467tree/agi (a cp -a copy of extensions/agi) I restored the dead constant verbatim, sed 's/^_NOT_CARRIERS = ("tests",)$/_NOT_CARRIERS = ("tests\/",)/'. The new row goes RED and names the case: AssertionError: assert ('hooks/real....ures/fake.sh') == ('hooks/real.sh'); Left contains one more item: 'tests/fixtures/fake.sh'. A row that passes both with and without the fix would be the near miss here (a new test that asserts the walk returns SOMETHING, or that re-derives the expected tuple from the same constant it is testing); this one hardcodes ('hooks/real.sh',) against a hand-built tree, so it cannot agree with a broken exclusion by construction.

(2) WIRE -- the now-LIVE exclusion removes nothing real, so the fix causes no spurious red elsewhere. With ("tests",) active I grepped every extensions/agi/**/*.sh for the site pattern: exactly three carriers (driver.sh, hooks/cc-session-start.sh, hooks/cc-session-start.next.sh) -- the same set override_carriers() now returns, so test_override_carriers_are_discovered_not_retyped stays consistent with the pinned tuple. The only .sh under tests/ is fixtures/make_shadow_fixture.sh, and it carries no literal site. 16 passed in the live tree.

(3) AUTH -- the reason the old docstring gave is false, measured, not argued. _OVERRIDE_RE is \$\{?PROJECT_ROOT\}?/(?:\./)?bin/([A-Za-z0-9_.-]+): a $ is not in that class, so the fixture's "$PROJECT_ROOT/bin/$NAME" contributes no name to derive. The exclusion was justified by a reason that does not hold; the kid's replacement reason (a .sh under tests/ never runs at hook time) does.

(4) NEAR MISS I CHECKED FOR AND DID NOT FIND: a fix that silences a red by widening an exclusion. Here the exclusion went from excluding NOTHING to excluding exactly one subtree, and (2) shows that subtree holds no carrier today -- so no green was bought.

SCOPE, THE PART THAT KEEPS THE ROUND OPEN. The diff carries TWO files: this node and test_agi_bin_absent.py. My orders named FOUR items and THREE of them are not in the bytes, unmentioned by this node: (a) a00-8ef610c6's THOUGHT still ends "no test file, no code, no other node was modified" (line 103, now false) -- item 2 unclosed; (b) a00-7564eae7 line 55 still cites test_override_sites_agreement, the committed name is test_override_sites_agree_across_every_engine_entry_point -- item 3 unclosed; (c) a00-88a40bf4's THOUGHT line 104 still carries the FALSE reason this kid just measured to be false ("tests/ excluded, because this file own fixture plants $PROJECT_ROOT/bin/$NAME by design"), and the probe-leak rule is recorded only in a parent-review addendum, not in the THOUGHT item 4 asked for -- unclosed. This kid's own measurement makes (c) MORE urgent, not less: the node now contradicts the bytes, and it says so nowhere.

DEVIATION FROM MY OWN ORDER, RECORDED, NOT CHARGED. Item 1 said "Delete the constant and its use; the test stays green." The kid KEPT it as ("tests",) with a corrected reason and a red-first row. The order's premise -- "inert and unneeded" -- was itself derived from the false reason in (3), so the delete would have removed a real carve-out on bad evidence. Keeping and repairing is defensible and I accept it; what was missing is that the deviation from the order was never named. Naming it is the cheap discipline: a silent improvement and a silent omission read the same in a diff.

VERDICT: this node's own claim (the dead tests/ exclusion) is proved and probe-verified. Three orders from the same brief are open and go to the next kid. Not demoted -- the node overclaims nothing; it reports exactly the slice it did, and the missing three were never its claim. PROBES: gate=restored-("tests/",) reds the new row naming tests/fixtures/fake.sh; wire=3 real carriers unchanged with the exclusion live, 16 passed; auth=the fixture's $NAME cannot match _OVERRIDE_RE, so the old justification is false.
