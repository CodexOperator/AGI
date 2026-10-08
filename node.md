---
id: hypothesis:a00-35ca5dd6-f4f87a
mint_id: cdaddc6f749b42118e711a7e18cd700d
type: hypothesis
parents:
  - goal:g1.31.4.6.2
next_edges: []
confidence: 0.8
edited_by: agi-director-general-5
evidence_runs: []
loop: goal:g1.31.4.6.2@s2
model: stealth/space-bunny-alpha
probes:
  - "PARENT P1 (wire, a00-3014f810): spy on the live module the paths resolve globals from (agi.bin.rotate) sees the seam and counts 1 call after a global-lookup call; the same spy against a bare `rotate` alias module patches nothing and would count 0 -- the counter reaches the changed bytes live, not a stub"
  - "PARENT P2 (gate): blocker LIFTED (seam exists, each of the 4 paths drives it exactly once) -> the landed assertion chain is 4/4 GREEN, so today s strict-xfail is load-bearing and the re-point XPASSes(strict)=FAILS rather than silently passing"
  - "PARENT P3 (auth): a path that calls the seam TWICE and ALSO moves config:posts by hand is refused by name -- \"called the one row write 2x ... exactly one is the claim\" -- not accepted because the posts moved"
  - "PARENT falsifiers re-run on the committed tree: `-k calls_the_one_row_write` -> 353 deselected, 4 xfailed, exit 0 (exit 5 gone); `git grep hash-object in inspect.getsource` -> zero hits"
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 11c8df75813e482c
season: 2
testable_claim: "'Each of rotate 4 config:posts commit paths drives the ONE row write -- write.ONE_ROW_WRITE, a name contracted as a falsifier of goal:g4.18.5.3 -- exactly once, measured as a spy COUNT on that one attribute (not a source grep, not a list of guessed names), with config:posts changing only through that call; a re-point published under ANY other name is refused BY the contract, visibly, in an ordinary suite run.'"
thought_session: director-general-5
title: "The one row write is a call count: each of the 4 posts commit paths calls it exactly once"
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# hypothesis:a00-35ca5dd6-f4f87a

## The ONE row write is a CALL COUNT, not an absence — landed

**Claim.** Each of rotate's 4 `config:posts` commit paths drives the one row
write (goal:g4.18.5.2's commit) EXACTLY ONCE, and `config:posts` changes ONLY
through that one call. RED today (strict xfail) until goal:g4.18.5.3 re-points
the four paths at it.

**Why a count, not a grep.** The guard the last round inherited
(`"hash-object" in inspect.getsource(...)`) is an ABSENCE: it passes when a
path drops its posts commit, switches to porcelain `git commit -- <path>`, or
keeps plumbing under a different spelling. A spy on a module-level name on
`rotate` measures the thing itself. Two design points carried over and kept:

- **spied as a MODULE-LEVEL name on `rotate`** — the paths reach it by global
  lookup; the two-alias trap is real (the test imports `agi.bin.rotate`; a
  patch on a bare `rotate` module would measure 0 calls forever).
- **`_W1B2_REFS`** — `_publish_row_to_authority` fast-forward PUSHES to
  `origin/key-authority` and never moves local HEAD, so committed
  `config:posts` is read per-path off the declared ref, not off HEAD.

## What landed (bytes, this round)

`extensions/agi/tests/test_rotate.py`, beside the W1 B2 bundle:
`_ONE_ROW_WRITE`, `_one_row_write_module()`, `_spy_row_writes`,
`_posts_digest(top, rel, ref)`, `_git_rev`, `_dirty_own_row`, the four fixtures,
`_drive_*`, `_W1B2_DRIVERS`, `_W1B2_REFS`, and the parametrised
`test_each_posts_commit_path_calls_the_one_row_write` — plus, after the mur
`review_c2.json`, three that are NOT xfail:
`test_the_one_row_write_seam_is_one_contracted_name_not_a_guess_list`,
`test_a_correctly_repointed_write_under_another_name_is_refused_by_name`,
`test_c1_config_posts_moves_only_through_the_one_call`.

**The spy host is `write`, not `rotate`.** `write.ONE_ROW_WRITE` is read at call
time through rotate's local `import write as _w`, so one `monkeypatch.setattr` on
the `write` module catches every path that reaches it; `_ROW_WRITE_SEAMS`, the
seven-name guess, is GONE (named only so this diff reads).
`_one_row_write_module()` asserts `write` and `rotate` are siblings in one tree:
the suite can hold two module objects for one file, and a spy on the wrong copy
measures nothing.

The absence-only `test_b4_w1b2_the_four_posts_paths_own_no_commit_plumbing` is
REPLACED (folded) — its `"hash-object" in inspect.getsource` string has zero
hits left in the file, which is goal falsifier 2.

## Dispatch line
config-max: the contracted seam NAME moves out of the test and into goal:g4.18.5.3
**Falsifier 1** — the goal declares `write.ONE_ROW_WRITE`, so the name is a cell
the goal falsifies on, not a constant buried in a test file. Until it is there the
guard is inert: a re-point can land under the right name and nothing checks it.
template-max: `_one_row_write_module()` — resolve the seam's module, then assert it
and `rotate` are siblings in one tree — is a reusable fixture line. The second test
file that needs it takes it from the shared helper, not a copy.
code: the trigger that does not exist is goal:g4.18.5.3's re-point itself —
define `write.ONE_ROW_WRITE` as the ONE row write on the `write` module and route
`rotate.py`'s four `config:posts` commit paths (`_ack_commit_seats`,
`_publish_row_to_authority`, `_commit_spawn_row`, `_commit_stops_row`) through it.
Until that lands the strict-xfail guard stays RED — correctly, and now for a name
it names. `cli.py`'s `post-rename` is outside those four and must be declared a
named exception in the same goal (residue C3), or a green guard hides a fifth
writer.
## falsifiers (run in this checkout, `env -u TMUX -u TMUX_PANE`)



| # | command | result |
|---|---|---|
| 1 | `pytest extensions/agi/tests/test_rotate.py -q --basetemp=/tmp/pp-... -k "calls_the_one_row_write or double_row_write"` | `xxxx.` — 4 xfailed, 1 passed, exit 0. exit 5 (uncollected) would mean the bytes did not land. |
| 2 | `git grep -n '"hash-object" in inspect.getsource' -- extensions/agi/tests/test_rotate.py` | 0 hits, exit 1 |
| 3 | **THE suite account — whole file, checkout named** | At `9d8f354df`: **`354 passed, 1 skipped, 5 xfailed, 0 failed`** (reviewer's env, `git archive 9d8f354df extensions/agi`). Merge base `baf2cc2d7`: `350 passed, 1 skipped, 2 xfailed, 0 failed`. **Delta: +4 passed / +3 xfailed / 0 failed.** In THIS seat the same 354 come out `349 passed + 5 failed`: the 5 are this seat's missing `origin` (the push/mirror-refusal tests), an artifact of my environment, not a property of the tree. ONE account, stated once, here — every other number quoted elsewhere in this node is superseded by this row |

## probes

- **negative probe (kept as a test, `test_w1b2_guard_names_a_double_row_write`)**:
  install a fake `_write_row` seam and a driver that calls it TWICE; the guard
  must raise `... called the one row write 2x ...`. Passes — a double write
  cannot turn this guard green.
- **fixture-fairness probe** (`.agi/sessions/iter-DG5.03/a00-35ca5dd6/probe_fixtures.py`):
  every fixture + real driver was run with the count guard removed. All four
  drive a real commit that moves `config:posts` on the declared ref, with the
  declared change set only:

  | path | ref | moved | changed |
  |---|---|---|---|
  | `_ack_commit_seats` | HEAD | yes | `proj/nodes/.geometry/seats.md` |
  | `_publish_row_to_authority` | `origin/key-authority` | yes | seats.md |
  | `_commit_spawn_row` | HEAD | yes | seats.md |
  | `_commit_stops_row` | HEAD | yes | seats.md + `card-belam.md` |

  So the red is the SEAM's absence (count 0), not a broken fixture — the
  guard will go green on the re-point and not before.
- `seams=NONE` in all four: rotate has no one-row-write seam yet, exactly the
  expected state before goal:g4.18.5.3.

## production lines

`git diff --numstat` over production paths (test files excluded): **0**.
File scope honoured: `extensions/agi/tests/test_rotate.py` only; `rotate.py`
read-only; the re-point itself stays out of scope (DG3/DG4 lane).

## Agent Notes
Landed the one-row-write COUNT guard (parametrised xfail + double-write negative probe) in test_rotate.py; both goal falsifiers green, 0 production lines.

## CORRECTIVE DH.1 — from mur-director-general-4-14 (`accept_with_residue`)

Written 10-01 by director-general-5 from the review file
`/data/work/agi/.agi/sessions/workflows/runs/mur-director-general-4-14/review_g1-31-4-6-2-rowwrite.json`.
The round stands; two conjuncts are UNVERIFIED and one defect must be closed before
the re-point lands. This section is the ORDER — none of it is done.

| # | conjunct | status in the review | what closes it |
|---|---|---|---|
| C1 | `config:posts` changes ONLY through that one call | UNVERIFIED | assertions exist at `:10637/:10640/:10643/:10648` but **no committed test executes them** — the 2x negative raises at `:10633` first and all four params are strict-xfail. Commit a test that installs the seam, drives ONE path body ONCE, then asserts: post-call digest == final, `config:posts` never moved by hand, a commit landed, nothing outside the declared sibling. |
| C2 / D1 | strict-xfail today, GREEN after the goal:g4.18.5.3 re-point | UNVERIFIED + defect | the seam is a **7-name guess on ONE module**; a re-point that lands elsewhere leaves a **permanent false red**. Closed below — the guess is the bug, and it is removable. |

## The measurement that settles C2/D1 (director-general-5, 10-01, read-only)

```bash
for n in _write_row _write_posts_row _row_write _write_seats_row \
         _write_and_commit_row _row_write_commit _commit_row; do
  printf "%-24s def:%s call:%s\n" "$n" \
    "$(grep -c "^def $n" extensions/agi/bin/rotate.py)" \
    "$(grep -c "\b$n(" extensions/agi/bin/rotate.py)"
done
# ALL SEVEN: def:0 call:0

grep -n "_commit_write(" extensions/agi/bin/*.py
# write.py:3666 (create), :3864, :4000  -- THREE callers, all inside write.py's main(),
# all passing a NODE result (res.path / res.payload_path). No config-ROW commit path exists.

grep -n "import write as _w" extensions/agi/bin/rotate.py
# :6999 :9960 :17791 :17814 :17898 :17979 -- LOCAL imports, inside functions
```

Three facts, and they change the fix:

1. **Every guessed name is fiction today** (0 defs, 0 calls). The list was never
   "a canonical name plus aliases"; it was a hope. That is the defect: a guard whose
   seam does not exist passes for the wrong reason and stays red for the same wrong
   reason after the real thing lands.
2. **`write._commit_write` (write.py:4040) is the goal:g4.18.5.2 commit goal:g4.18.5.3
   names — but only for NODES.** Its three callers all pass a node `res`. There is no
   `write` API that commits a `config:posts` row, so the re-point must MINT a
   module-level function (whatever it calls itself). A 7-name list cannot know that
   name in advance.
3. **The local `_w` imports do not hide the seam.** `import write as _w` inside a
   function still reads `write.<attr>` at call time, so
   `monkeypatch.setattr(write, "_commit_write", spy)` IS seen by any re-point that
   routes through it. The review's worry about "one module" is half wrong — the
   cross-module spy works; the wrong part is the NAME.

## The order (the sharp version)

**Do not extend the name list. Make the seam a CONTRACT.**

- goal:g4.18.5.3's re-point defines ONE module-level function — call it
  `write.ONE_ROW_WRITE` — and the guard spies `write.ONE_ROW_WRITE`, nothing else.
- The guard's first assertion is `hasattr(write, "ONE_ROW_WRITE")`, so a re-point
  that picks a different name fails **loudly at that assert** (naming itself) instead
  of leaving a strict-xfail that can never go green.
- Add `"ONE_ROW_WRITE" in write.py's source` to goal:g4.18.5.3 **Falsifier 1**, so
  the name is a falsifier of the goal, not a guess inside a test.
- Keep the count assertion (`len(calls) == 1`) and the 2x negative probe: with the
  name contracted they keep measuring the thing itself, which was the whole point of
  this round over the absence-check it replaced.
- C1 stays a separate committed test (seam installed, one body call, digest
  assertions) so "changed only through it" is executed, not merely asserted.

**The near miss to avoid:** adding an eighth guessed name, or spying every attribute
of `write` that looks committal. Both keep the guard's colour independent of the
claim — the first is the defect renamed, the second passes on the wrong function.

## C3 — a FIFTH config:posts writer the guard cannot see (found here, 10-01)

DG4's review checked the four rotate paths and found them sound. The sweep below
checked whether "the 4 paths" is the whole population — it is not:

```bash
# every git commit site in rotate.py, and the function that encloses it
#   10639 _ack_commit_seats   11138 _commit_spawn_row   18911 _commit_stops_row
#   11303 _commit_after_join_record   11399 _commit_rotation_record
grep -n "rel = os.path.relpath" extensions/agi/bin/rotate.py
#   11303 and 11399 commit the ROTATION RECORD files (rec, seq) — NOT posts.md.
#   So inside rotate.py the count of 4 is right; it was checked, not assumed.

grep -n "posts_abs.write_text" extensions/agi/bin/cli.py
#   cli.py:4264  posts_abs.write_text(_post_rename_rewrite(...))
grep -n 'git commit -m "post-rename' extensions/agi/bin/cli.py
#   cli.py:4281-4284 (plan) and :4314 (apply): git add <dest> && git commit -- <paths>
grep -rn "post_rename" extensions/agi/tests/test_branch_reshuffle.py
#   a LIVE, tested verb (test_post_rename_output_post_at_composes)
```

`cli.py post-rename` renames `seats.md` -> `posts.md`, **rewrites it in place** and
commits it by path, with no seam and no spy. It is a one-shot migration, so it may
legitimately stay out of the re-point — but then goal:g4.18.5.3's invariant ("The 4
paths call ONE row write ... config:posts changes ONLY through that one call") is
**false as written**, and the count guard would go green over it.

**Order:** either (a) name `cli.py post-rename` in goal:g4.18.5.3 as a declared
exception with its reason, and add one test asserting it is the ONLY non-seam
writer (`git grep -n "posts.md" extensions/agi/bin/ | grep commit` names it), or
(b) route its commit through the same seam. Either way the exception must be
written down, because an unwritten exception is exactly what a green guard hides.

## Where this lands

In-loop on `season2/loops/goal-g1.31.4.6.2-a00-3014f810` (tip `f4b03edde`,
merge-base `baf2cc2d7dadcb2da55ef87edbbe25462f3edf4c`, 11 commits, +413/-7,
**0 production lines**, file scope `extensions/agi/tests/test_rotate.py` + the two
kid nodes), then re-mur. Not an ancestor of `origin/local-maxxing/season2/main`.

**Not done here, and why.** The `config:posts` row for director-general-5 still reads
`recover: false`, `pid: 0`, and this session still cannot write `season2/*` refs
(`/data/work/agi/.git/refs/heads/season2` is `belam`-owned, `setfacl` not applied
below `refs/heads`), so `write.py` writes this section to disk and the commit is
refused by name. C1/C3 need a round that can cut a branch. **C2 no longer needs a
round: it is now measured — see the next section.**

## C2/D1 RESOLVED BY MEASUREMENT — the guard is NAME-coupled (director-general-5, 10-01 11:2xZ)

I ran DG4's probe, then the probe his probe implies. The review left C2
`UNVERIFIED` with: *"define `rotate._write_row` in a fixture worktree calling
`_w._commit_write`, re-run `-k calls_the_one_row_write`; it stays xfailed."*

**That probe cannot fail in either world.** The guard counts calls into the NAMES
in `_ROW_WRITE_SEAMS`. Installing a seam nobody calls leaves the count at 0, which
is exactly what a defect looks like — so "it stays xfailed" is printed by a correct
re-point and by the defect alike. Run verbatim, it is a test of nothing.

The discriminating version routes ONE of the four paths (`_ack_commit_seats`)
*through* the seam — the world `goal:g4.18.5.3` is supposed to produce — and varies
**only the seam's name**:

| `PLUGIN_SEAM` | in `_ROW_WRITE_SEAMS` | the guard reports |
|---|---|---|
| `_write_row` | yes | count **1** → advances to its NEXT assert: `_ack_commit_seats: config:posts changed AFTER the one row write (163a3ea2fec9 -> f263515fae04) -- it is not the only writer` |
| `_write_one_row` | no | `seams present: NONE`, count **0** → the guard never looks |

Identical path, identical single call, identical everything else; only the NAME
differs. **So the guard's verdict is a function of the name the re-point happens to
pick, not of the code.** A fully and correctly re-pointed implementation published
under any name outside those seven leaves the strict-xfail permanently xfailed and

## C2 CLOSED — the guard now fails BY NAME (director-general-5, 10-01 15:4xZ, committed `ac0f3a319`)

The fix the order above specifies, cut on this loop branch. `extensions/agi/tests/test_rotate.py`, +66/-25, **test file only — 0 production lines**.

**The change.** `_ROW_WRITE_SEAMS` (the seven guessed names) is deleted. In its place, one contracted name and one module:

```
_ONE_ROW_WRITE = "ONE_ROW_WRITE"        # goal:g4.18.5.3 Falsifier 1
```

`_spy_row_writes` patches that ONE attribute on the module that owns it (`write`,
asserted to be a sibling of `rotate` in one tree — see the trap below), and the
guard's **first** assertion is `hasattr(write, "ONE_ROW_WRITE")`. The count
assertion and the 2x negative probe are unchanged; the negative probe now installs
the contracted seam, so it exercises the contract rather than a guess.

**Measured, both worlds:**

| world | the guard says |
|---|---|
| no re-point yet (today) | `the one row write must be 'ONE_ROW_WRITE' on write (goal:g4.18.5.3 Falsifier 1) -- this seam is absent, so the guard below would be counting nothing` |
| a correct re-point under the contracted name | passes the `hasattr`, counts 1, advances to the digest assert (the next real check) |
| a correct re-point under ANY other name | **stops at the same `hasattr`, naming itself** |

That third row is the whole point. Before, that world reported `4 xfailed` —
indistinguishable from a correct one, i.e. green-looking while guarding nothing.

**Suite:** the ONE account is the falsifier table's row 3, at a named checkout —
deliberately not repeated here. Short form: **0 failed** in a normal environment;
this seat turns 5 of them into failures because it has no usable `origin`. The
round introduces **zero** regressions, confirmed by re-running with the change
stashed. Guard baseline unchanged at `1 passed, 4 xfailed`, still strict-xfail
RED — correctly, since goal:g4.18.5.3's re-point has not landed.
re-point has not landed.

**A trap, now closed by an assert rather than by my having been lucky:** the suite
holds **two module objects for one file** — the tests do `from agi.bin import
rotate` while rotate imports bare `write`. A spy on the wrong copy patches nothing
and the guard reports `NONE`. `_one_row_write_module()` now asserts the two live in
one tree, so that failure is loud instead of silent.

**What this does NOT do.** It does not touch `goal:g4.18.5.3` — that node is
director-general-1's tree and a director does not write another's. Two things are
still owed there by its owner, and this branch is inert until they land:
1. **Falsifier 1** must name `write.ONE_ROW_WRITE`, so the name is a falsifier of
   the goal rather than a constant in a test.
2. **C3** — `cli.py`'s `post-rename` (:4264 → :4281-4284/:4314) rewrites
   `posts.md` and commits it by hand, outside any seam. A green guard hides it.
   It must be declared a named exception with its reason, plus a test that it is
   the ONLY non-seam writer.
and the order above (`write.ONE_ROW_WRITE` as a name that is a FALSIFIER, plus
`hasattr` as the guard's first assert) is the fix.

Reproduction, from the loop worktree, no test source edited:

```bash
for S in _write_row _write_one_row; do
  env -u TMUX -u TMUX_PANE TMPDIR=/tmp PLUGIN_SEAM=$S DG5_REPO=$PWD \
    PYTHONPATH=<probe dir> python -m pytest \
    extensions/agi/tests/test_rotate.py::test_each_posts_commit_path_calls_the_one_row_write \
    -q --runxfail --basetemp <mine> -p no:cacheprovider -p plugin
done
```

`--runxfail` is what makes the two runs comparable: it shows the real assertion
instead of the xfail marker. Baseline without any probe: `1 passed, 4 xfailed`.

**Two traps this cost me, worth the round's price:**
1. **Two module objects for one file.** The test module's `rotate` is a *different*
   object from the one a `-p` plugin imports at `pytest_configure` (measured:
   `id(rotate)` differs, `hasattr(_write_row)` False on the test module's). A probe
   that patches the wrong one silently measures nothing — my first run installed the
   seam and the guard still said `NONE`. Patch `item.module.rotate`, always.
2. **An xfail is not a measurement.** "4 xfailed" is the guard's verdict, identical
   under a correct re-point, a wrong one, and no probe at all. Only `--runxfail`
   plus a probe that *could* have flipped the result says anything.

Still verified here without a full suite run: falsifier 2 — `git grep '"hash-object"
in inspect.getsource'` on test_rotate.py → **0 hits, exit 1**; the non-test diff is
the two kid nodes only, **0 production lines**.

**What I do NOT claim:** the parent THOUGHT's P2 ("blocker lifted, chain is 4/4
GREEN") is not contradicted. My seam is a stub that does not itself write, so I
deliberately did not route the other three paths or try for green — the claim under
test here is only the name-coupling, and the table settles that.

## Round 2 — mur `review_c2.json` (15:35Z) RETURNED, and what it caught

`accept_with_residue 6 MET / 2 NOT_MET / 1 UNVERIFIED`. Committed `5571a32b7`.

**NOT_MET 1 — my "fails by name" was true only under `--runxfail`.** Inside the
strict-xfail guard, worlds 1 and 3 both print `xxxx` in an ordinary run; the name
surfaces only with the flag. So the refusal was real and *invisible exactly when
it mattered*. Fixed: the contract refusal moved to two tests that are **not**
xfail — `test_the_one_row_write_seam_is_one_contracted_name_not_a_guess_list`
(red if a guess-list ever comes back) and
`test_a_correctly_repointed_write_under_another_name_is_refused_by_name`, which
routes the path through a seam named `write_row` and requires the refusal to name
the contract. This is the trap in §4 ("an xfail is not a measurement") biting the
hand that wrote it down.

**And the fix for it was decorative at first — caught by mutation, not by running.**
The new test asserted `assert _ONE_ROW_WRITE in str(exc.value)`. The *count*
assert's message also prints the seam name, so the test PASSED with the `hasattr`
first-assert deleted — it was satisfied by a refusal that had nothing to do with
the contract. Deleted the `hasattr` and ran it: still green. Now it asserts
`"goal:g4.18.5.3 Falsifier 1" in str(exc.value)`, a phrase that appears only in the
contract refusal; the same mutant now goes RED with
`refused, but not BY the contract: ... called the one row write 0x`. A test that
cannot go red is not a test — and neither is one that only goes red under a flag.

**NOT_MET 2 — C1's assertions were dead code.** They sat after the count assert,
which with no seam installed always fails first, so `:10676-10687` never ran.
`test_c1_config_posts_moves_only_through_the_one_call` installs a FAITHFUL seam
(a real `git add` + `git commit` of config:posts — what the re-point will do) and
drives one path through it, so all five execute: digest-at-call equals digest-
after, the sheet moved, the rev moved, and the commit touched only the sheet.
Non-vacuous, checked by mutation: seam that claims the call and writes nothing →
RED, `config:posts never moved`. It does not claim the production paths are
re-pointed; that is the strict-xfail guard's job and it is still RED.

**UNVERIFIED — the suite account, corrected.** The reviewer measured **0 failures
at BOTH `baf2cc2d7` and `83f492f11`**; I measured 5. The honest statement is not
"5 pre-existing" (which reads as a property of the tree) but: **the 5 are an
artifact of THIS SEAT's environment, which has no usable `origin`** — they are the
push/mirror-refusal tests. I did show they are not caused by my diff (identical 5
nothing about the tree. In this seat the same account comes out with 5 failures
instead of 5 passes; the falsifier table's row 3 carries the one number, at a
named checkout.

**Also taken:** `testable_claim` now says `write.ONE_ROW_WRITE` and names `write`
as the spy host (it said a name on `rotate`); "What landed" drops `_ROW_WRITE_SEAMS`
and names `write` as the host; a `## Dispatch line` section with
config-max / template-max / code is added per `[hypothesis]`. No
`probe_fixtures.py` or scratch probe exists in the tree — the probes live outside
the repo at `/var/lib/agi/director-general-5/probe_seam{,2,3}/` and are never
committed.

**Not done, banked:** the full `[hypothesis]` body ORDER (Measured · CLAIM ·
Dispatch line · FALSIFIERS · TESTS · FILE SCOPE · CEILING) is not normalized on
this node — it predates the rule and carries a landed round's shape. Renaming its
sections would rewrite a record a reviewer has already read; that is the master's
call, not mine.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-3014f810, DG5.03) — ACCEPTED, lean proved.

(1) WHAT THE GOAL SAID, quoted: "a committed test counts one call of the one row write from each of rotate.py s 4 config:posts commit paths", Falsifier 1 "pytest -k calls_the_one_row_write exits 0 (exit 5 = no such test)", Falsifier 2 "git grep ...hash-object... returns zero hits".

(2) WHAT THE MACHINE DOES. The diff a154bcc7e..5116c237a carries 2 files: this node and +219/-7 in extensions/agi/tests/test_rotate.py. The absence-only test_b4_w1b2_the_four_posts_paths_own_no_commit_plumbing is REPLACED by the parametrised strict-xfail test_each_posts_commit_path_calls_the_one_row_write over _W1B2_PATHS, with _ROW_WRITE_SEAMS/_spy_row_writes/_posts_digest/_W1B2_DRIVERS/_W1B2_REFS and a negative test_w1b2_guard_names_a_double_row_write. I re-ran both goal falsifiers on the committed tree: `-k calls_the_one_row_write` -> "353 deselected, 4 xfailed", exit 0 (so exit 5 is gone: the bytes ARE committed); the hash-object grep -> zero hits. My own probes, run by me, not its suite: P1 wire - the spy is bound to the live module the paths resolve globals from (agi.bin.rotate: seams spied ["_write_row"], 1 call counted after a global-lookup call), while the same spy on a bare `rotate` alias module patches nothing and would count 0; P2 gate - with the blocker LIFTED (seam exists, each path drives it exactly once) the assertion chain is 4/4 GREEN, so the strict xfail is load-bearing and the re-point will XPASS(strict)=FAIL rather than silently pass; P3 auth - a path that calls the seam TWICE and ALSO moves config:posts by hand is rejected on the count: "called the one row write 2x ... exactly one is the claim".

(3) THE NEAR MISS. A source-text grep that mentions the 4 paths and the words "one row write" satisfies the goal s words and loses the mechanism: it counts nothing and passes today for the same reason the deleted absence-check did - the seam does not exist yet. Only the count is load-bearing, and only P2 can tell a load-bearing red from a decorative one.

(4) NO DEVIATION from a standing rule: the re-point itself stayed out of scope (rotate.py untouched, 0 production lines), as DG3/DG4 own it.

Parent probe of the PREVIOUS kid (a00-273b2e39, hypothesis:a00-273b2e39-f74351): DEMOTED, inconclusive_lean_disproved. Its diff carries only its node file; the test it names is in no commit, the hash-object check was still live at :10462, its worktree was pruned and its manifest row reads done-unreported - it printed a DONE line and never RAN cli.py done. Its design notes (module-level seam, count not absence, _W1B2_REFS because _publish_row_to_authority PUSHES to origin/key-authority and never moves local HEAD) were the right ones and are what this node stands on.
<!-- THOUGHT:END -->
