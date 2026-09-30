---
id: experiment:a00-619731a3-9d4779
mint_id: aa7a2dc32e044bc5a1a0b15e354ad5f8
type: experiment
parents:
  - hypothesis:a-rounds-own-path-set-never-fails-open
next_edges: []
confidence: 0.85
edited_by: a00-c1408ac0
evidence_runs:
  - experiment:a00-619731a3-9d4779
loop: hypothesis:a-rounds-own-path-set-never-fails-open@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 7cd861ebcfded2fa
season: 2
title: "the AGI_CLI_PY RED-proof seam is closed: a set-but-stripped var skips instead of going green on the live cli.py"
town: core
verdict: proved
---
# experiment:a00-619731a3-9d4779 — the AGI_CLI_PY seam, closed

## What this round was

A CORRECTIVE round on four experiment nodes and one test file, on the chain
`hypothesis:a-rounds-own-path-set-never-fails-open`. The one claim I set out to
turn from an assertion into a measurement: **a RED proof routed through
`AGI_CLI_PY` and run from inside `extensions/agi/tests` cannot tell you it is
testing the live tree** — and a documented dead branch is a trap the next round
re-steps in, so it had to become loud.

## The claim, and the measurement that settles it

`extensions/agi/conftest.py:54 _strip_agi_env` deletes every `AGI_*` key at first
test setup. `AGI_CLI_PY` is `AGI_*`. The DH.578 round documented this in six
lines of docstring and **kept the branch anyway**, which is exactly the residue
the parent measured.

The tell nobody had: **the strip is a session fixture, so it runs AFTER
collection.** Module import is therefore the only moment the var is still
readable from inside the tests tree. That single fact is the whole fix — it is
what makes "set but stripped" *detectable* at all.

Method: a FULL copy of `extensions/agi/bin` with the DH.552 leg 1 re-widened
(`r.get("dispatch_node_id") or r.get("node_id")`). Any honest RED proof must
fail on it. Same copy, two run locations, before and after.

```
### BEFORE -- run from INSIDE extensions/agi/tests, AGI_CLI_PY -> the mutated copy:
........                                                                 [100%]
8 passed in 0.10s

### CONTROL -- the SAME mutated copy, test file run from OUTSIDE extensions/agi/tests:
FAILED test_round_own_path_set_fails_closed.py::test_only_dispatch_node_id_widens_the_set_never_the_node_id_line
1 failed, 7 passed in 20.44s

### AFTER -- the seam is closed. Same command, same mutated copy, from INSIDE the tests tree:
SKIPPED [1] test_round_own_path_set_fails_closed.py:85: AGI_CLI_PY was set at collection and is gone now: extensions/agi/conftest.py:54 _strip_agi_env deleted every AGI_* key session-wide, so this run would silently test the LIVE cli.py. Run this file from a copy OUTSIDE extensions/agi/tests (named copy: cli.py)
8 skipped in 0.09s

### AFTER -- control: the live bytes, no AGI_CLI_PY set at all (the ordinary green):
........                                                                 [100%]
8 passed in 2.58s

### AFTER -- the same file copied OUTSIDE the tests tree, mutated copy under test: still a real RED
FAILED test_round_own_path_set_fails_closed.py::test_only_dispatch_node_id_widens_the_set_never_the_node_id_line
1 failed, 7 passed in 0.11s

### SUITE -- the two briefed files on the live bytes:
FAILED test_bin_help_smoke.py::test_help_smoke[suite_guards.py]
1 failed, 80 passed, 6 skipped in 5.41s
```

`8 passed` → `8 skipped` for the *same command*, and the skip names the strip.
That is the claim: the seam is now loud. The mechanism is untouched — `cli.py`
has **0 production lines** of diff in this round — so the green on live bytes is
the same green; what changed is that a green can no longer be produced by a run
that was not testing what it claimed to.

`test_help_smoke[suite_guards.py]` is the briefed red on this base, recorded the
same way on the DH.578 verdict node; not mine, its file never moved.

## The fix

`extensions/agi/tests/test_round_own_path_set_fails_closed.py`, +40 / −9:

1. **The seam is closed.** `_CLI_PY_AT_IMPORT` captures the var at collection;
   a module-scoped autouse fixture skips — with a reason that names
   `extensions/agi/conftest.py:54 _strip_agi_env`, and the copy's *name* only, no
   path value in a skip line — when it was set at import and is gone at test
   time. Skip, not assert: the honest state when a run cannot know what it is
   testing is to refuse to answer.
2. **Item 4, the re-spelled path segment.** `_spawn` hand-wrote
   `root / "sessions"`. It now goes through `locations.sessions_dir(root)` —
   the per-worktree resolver, never `shared_sessions_dir`, because iteration
   output is the worktree-local fork. Bound semantics unchanged: the pins still
   discriminate (1 failed / 7 passed on the mutated copy, 8 passed live).

## Node-text items (1, 2, 3, 6)

| item | what I did |
|------|------------|
| 1 | The paragraph after `THOUGHT:END` on three nodes, and the one in the body of the fourth, is **gone**. Each node's THOUGHT is rewritten, one per node, about that node. `experiment:a00-8f39d964-fc2306` had no THOUGHT block at all — it now has one. |
| 2 | No two of the four THOUGHTs share a sentence. `grep -c "DH.578 parent review"` on all four now returns **0**. The measurement trap is kept only where it bit me: the `[]`-from-a-mis-shaped-call trap is on the node whose own suite state is a mis-shaped call; the strip trap is on the nodes the pins live on. |
| 3 | `experiment:a00-1389258c-50f93f` frontmatter said `proved`; its own body said one conjunct proved, one falsified. **The body wins** — it recorded the falsifier, and the frontmatter is what a reader and the gate read, so the field is the one that has to be honest. It now reads `inconclusive_lean_disproved:80`. The later round that corrected the falsified half is a *supersession*, not a proof, and the number says so. |
| 6 | Route **(a), re-run and paste**. `.gitignore` ignores `.agi/sessions/*`, so the DH.578 probe pointer was a pointer no merged reader can follow. I re-ran the probes and pasted the output into the verdict node's own body (new `## DH.604` section) and here. No pointer into an ignored tree survives on any node I touched. |

## Deviations, named not absorbed

- **No git was run**, per the round contract for a kid. The brief's PARENT line
  said "COMMIT every kid edit and every node edit on the loop branch before you
  exit"; the round contract says a kid runs no git and `cli.py done` is the only
  versioning step. The contract wins; the commit is the loop's. The one git read
  permitted — `git diff --numstat` for the line count — was run and is below.
- **No file outside FILE SCOPE was touched.** The one thing this round wanted
  and could not have is `extensions/agi/conftest.py` itself: it deletes every
  `AGI_*` key session-wide, which is correct policy and is what made the seam
  possible. Naming it for the director's findings row: the strip is the ROOT
  cause; the fix here is a symptom-level refusal. A `conftest`-level guarantee
  (a session fixture that FAILS a test which reads a stripped var) would close
  the class, not this instance.

## Line count

```
$ git diff --numstat -- extensions/agi/tests/test_round_own_path_set_fails_closed.py
40      9      extensions/agi/tests/test_round_own_path_set_fails_closed.py
```

40 added / 9 deleted, net +31 — at the 40-line test ceiling on the gross
reading and well under on the net. `extensions/agi/bin/cli.py`: **0 production
lines**. Node files are not production paths.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.604. The interesting half of this round is not the fix, it is the shape of the fix.

A documented dead branch is not neutral. The DH.578 kid wrote six lines explaining that the env var this file uses to name a copy of cli.py is stripped by the suite conftest, kept the branch, and called that a documentation win. It is the opposite: the branch still reads as a working seam, the next kid sets the var, gets a green, and concludes the mutation was wrong. A note that describes a trap without refusing to enter it teaches the trap. So the work was to make the file answer, not to make the file explain.

THE MOVE THAT MADE IT POSSIBLE, and it is one line of reading the harness, not thirty of cleverness: the strip is a SESSION-scoped fixture, so it runs after collection. Everything before that point still sees the variable. That turns "the var was silently taken from me" from an undetectable condition into a comparison between two reads of the same name, and the whole fix follows from it — capture at import, compare at test time, refuse when they disagree. A skip, not an assert: an assert would need a claim about the right answer, and the right answer here is that the run does not know what it is testing. Refusing to answer is the honest state.

THE MEASUREMENT THAT PROVES IT rather than the one that flatters it: a green from inside the tests tree is worth nothing on its own, because it is exactly what a run that loaded the live cli.py also produces. So the under-test tree had to be made WRONG on purpose — a full bin copy with the DH.552 leg re-widened — and then the same copy was run from two places. Inside: 8 passed. Outside: 1 failed. After: 8 skipped, with the strip named in the reason, and outside still 1 failed, live still 8 passed. The identity of those two runs is the whole result; a single green could not have told me anything.

THE SAME FILE, SAME ROUND, A SECOND INSTANCE OF THE SHAPE: the sessions path segment was hand-spelled in the fixture. That is the identical mistake in a different costume — a second copy of a fact one module owns, which drifts silently, and which answers empty for the wrong reason when the root is wrong. Two defects in one 200-line file, both of the form "this expression means something other than what it looks like, and nothing says so". That is the real shape of this chain's residue, and it is worth a reader more than either fix.

WHAT I DELIBERATELY DID NOT DO: I did not touch the conftest that causes it. The strip is correct policy and the director owns it; a session-level guarantee that FAILS a test which reads a stripped var would close the class instead of this instance, and that is a bigger change than a kid round should make unasked. Named on my node for the findings row instead of absorbed.

STILL WEAK IN WHAT I LANDED: the fix is per-file. Any other test in this repo that names an AGI_* var to redirect a load has the identical trap, and mine will not catch it. The skip is also strictly a refusal — a run that sets the var from outside and copies the file out still has to be done by hand, and a reader who skips the file's advice gets no test at all, which is a better failure than a lie but is not coverage.
<!-- THOUGHT:END -->

## Agent Notes
AGI_CLI_PY seam closed: same mutated cli.py read 8 passed from inside extensions/agi/tests and 1 failed from outside; after the fix the inside run is 8 SKIPPED naming the conftest strip, outside still 1 failed, live 8 passed; sessions join routed through locations.sessions_dir; four THOUGHTs rewritten per-node, 1389258c frontmatter verdict made to agree with its own body

DH.604 PARENT REVIEW (a00-c1408ac0) — ACCEPTED, no demotion. Probes are mine, run by me, on the tip bytes; the kid's own suite is its claim, not my evidence.

(1) WHAT THE INSTRUCTION SAID, quoted: "fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number)", plus the residue the round itself measured: "the AGI_CLI_PY seam the round DISCOVERED and then kept in code ... a documented dead branch is a trap the next round re-steps in" and "a dead evidence citation ... the four node paragraphs' 'probes pasted in the DH.578 session dir' is a pointer no merged reader can follow."

(2) WHAT THE MACHINE ACTUALLY DOES — I read `git diff 6ce74be6d..f2f24d6e2` (the changed bytes, not this node's summary) and then measured, on a MUTANT full copy of extensions/agi/bin with the DH.552 leg re-widened (`v = r.get("dispatch_node_id") or r.get("node_id")`):
  - GATE probe (the exact state the gate must refuse): from INSIDE extensions/agi/tests with AGI_CLI_PY set to that mutant -> `ssssssss / 8 skipped in 0.59s`, and `-rs` prints the reason naming `extensions/agi/conftest.py:54 _strip_agi_env` and the copy's NAME only. The pre-fix behaviour of that same command is the kid's pasted "8 passed" — so the run that used to measure the LIVE tree and read green now measures nothing and says why.
  - WIRE probe (does the honest route still reach the changed bytes?): the SAME mutant, test file copied OUT of extensions/agi/tests, `PYTHONPATH=<copy>:extensions/agi/src` -> `1 failed, 7 passed`, the failure being `test_only_dispatch_node_id_widens_the_set_never_the_node_id_line`. The seam was closed without closing the door behind it.
  - CONTROL: live bytes, no var set -> `8 passed in 0.11s`. The ordinary green is unchanged; cli.py carries 0 production lines of diff.
  - NODE items, measured not read: `grep -c 'DH.578 parent review'` = 0 on all four nodes; zero bytes after `THOUGHT:END` on 06eab0c0/8f39d964/ee2d4cb1; 1389258c frontmatter now `inconclusive_lean_disproved:80` in agreement with its own body's recorded falsifier; `grep -c 'iter-DH.578'` = 0 on all four nodes. Pairwise sentence-overlap between the four rewritten THOUGHTs is 1, and that one is the `THOUGHT:BEGIN` boilerplate itself — item 2 (four nodes, one paragraph stapled four times) is genuinely closed, not re-stapled with new words.
  - TMM.268 check for the residue below: sha256 of all six node files EQUALS the last write-log sha256 for each (06eab0c0 879d98f3, 1389258c e8403833, 8f39d964 ac9fccc0, ee2d4cb1 0c61cccd, 29a5edeb 0984379f, 619731a3 b87ed780).

(3) THE NEAR MISS, and why the probe had to be the mutant: a green from inside the tests tree is worth nothing on its own, because a run that loaded the live cli.py produces the same green. Closing the seam by ASSERTING `AGI_CLI_PY` is readable would have satisfied every word of the brief (the trap is named, the var is checked) and lost the mechanism — the assert fires only after the strip, so it would fire on a correct live run too. Capturing at import and comparing at test time is the only version that distinguishes "you named a copy and I lost it" from "you named nothing". The same shape reappears in item 4: routing the join through `locations.sessions_dir` while leaving the literal somewhere else would fix one line and leave the second copy to drift.

(4) IF I DEVIATED FROM A STANDING RULE: two. (a) The corrective's PARENT line says "COMMIT every kid edit AND every node edit on the loop branch before you exit"; this seat's round contract is "Do not commit. Do not push. Do not run git at all", and the property of THIS case is that the kid's `done` scope carried its own node and the test file but NOT the four foreign nodes it was ordered to fix — the property that matters is the TMM.268 sha match above, which makes the uncommitted residue landable by whoever owns commits without guessing. (b) A kid that leaves its own node uncommitted gets a re-brief from me; this kid's own node IS committed (f2f24d6e2) and it is the FOREIGN nodes that are uncommitted, which is the scope rule working as designed, not a kid defect.

RESIDUE, named not absorbed: the five edited node files (four experiment nodes + verdict:a00-29a5edeb-7b795d) are uncommitted in the shared worktree; the kid's branch tip is f2f24d6e2 on season2/loops/hypothesis-a-rounds-own-path-set-a00-c1408ac0. A second residue the kid named and did not absorb: the fix is per-FILE, so any other test in this repo that redirects a load through an AGI_* var keeps the identical trap; the class-level closure is a conftest session guarantee that FAILS a test reading a stripped var, and extensions/agi/conftest.py:54 is outside FILE SCOPE — director's findings row.
