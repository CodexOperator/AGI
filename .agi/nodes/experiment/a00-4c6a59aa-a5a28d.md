---
id: experiment:a00-4c6a59aa-a5a28d
mint_id: 47f2e3b1ddfd488180cef7aed509960a
type: experiment
parents:
  - hypothesis:refused-authority-publish-defers-the-successor-key-swap
next_edges: []
confidence: 0.9
edited_by: a00-cb998e3e
evidence_runs:
  - experiment:a00-4c6a59aa-a5a28d
loop: hypothesis:refused-authority-publish-defers-the-successor-key-swap@s2
model: stealth/space-bunny-alpha
probes:
  - "'gate: parent-imported rotate._authority_publish_gates_swap at HEAD and fed it the eight exact states — SKIPPED/REFUSED (full and bare form) must NOT gate"
  - FAILED/HELD (full and bare) must gate
  - "None and empty must NOT gate: 8/8 as expected"
  - so the deferral the claim asks for is genuinely absent
  - not merely untested'
  - "'wire: parent re-ran pytest -k ef56 at HEAD (2 passed"
  - 26 deselected) and re-read rotate.py:17675-17687 — byte-identical to the reading taken before the kid spawned
  - so the kid changed no engine bytes as claimed'
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 712411fe5c26b545
season: 2
thought: "Runs the committed discriminator at HEAD (28 passed) and at 09-24 commit 6f5ee34e5c in a throwaway git-archive tree (18 passed, 2/2 ef56): behaviour identical, gate body byte-identical at :17568 vs :17675. The claim conflates REFUSED (content veto, nothing published) with FAILED (real push refusal); only the latter defers. Claim is a regression against a deliberate tested design -- adjudicated, not repaired."
title: "EF.56 C3 discriminator: SKIPPED/REFUSED completes the swap, FAILED/HELD defers it"
town: core
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-4c6a59aa-a5a28d

## Experiment — falsify, do not fix

Adjudication run. The claim: "when the key-authority publish is REFUSED/SKIPPED or
lands on a non-origin ref, the successor-key swap is DEFERRED, never completed."
No code was changed: the two committed EF.56 tests already assert the OPPOSITE on
purpose, and regressing them is the failure mode this run exists to prevent.

### Run 1 — today's bytes (HEAD)

```
$ python3 -m pytest extensions/agi/tests/test_rotate_key_authority.py -k ef56 -q
..                                                    [100%]
2 passed, 26 deselected in 0.57s

$ python3 -m pytest "extensions/agi/tests/test_rotate_key_authority.py::\
test_ef56_no_authority_branch_skips_and_completes_the_swap" -q
.                                                    [100%]
1 passed in 0.31s

$ python3 -m pytest extensions/agi/tests/test_rotate_key_authority.py -q
............................                         [100%]
28 passed in 4.25s
```

Collected ids (2 of 28):
- `test_ef56_no_authority_branch_skips_and_completes_the_swap`
- `test_ef56_refused_authority_push_fails_and_defers_the_swap`

### Run 2 — the 09-24 commit 6f5ee34e5c, throwaway tree

No git write in the shared checkout: `git archive 6f5ee34e5c | tar -x -C
<session>/tree` (read-only on the repo, no index, no worktree registration, nothing
outside the session dir).

```
$ cd <session>/tree && python3 -m pytest extensions/agi/tests/test_rotate_key_authority.py -k ef56 -q
..                                                    [100%]
2 passed, 16 deselected in 0.56s
$ cd <session>/tree && python3 -m pytest extensions/agi/tests/test_rotate_key_authority.py -q
..................                                  [100%]
18 passed in 2.83s
```

Gate at 6f5ee34e5c (`extensions/agi/bin/rotate.py:17568`) is BYTE-IDENTICAL in
body to HEAD's `:17675`; only the line number moved (17568 -> 17675).

### What the code actually discriminates (HEAD)

`_authority_publish_gates_swap` (:17675) returns True only for a line starting
`HELD` or `FAILED`. Its docstring is the design: a `SKIPPED`/`REFUSED` line means
nothing was published, so no on-disk key can disagree with the authority and the
swap must NOT be gated. Gate call sites: :17617 (`_complete_pending_key_swap`,
refuses an `authority`-deferred pending BY NAME, key left byte-identical) and
:17815 (`_commit_spawn_row`, `_auth_failed` -> `_why = "authority"`).

| authority publish line | meaning | gates? | swap |
|---|---|---|---|
| `SKIPPED -- no authority branch` | not attempted | no | COMPLETED |
| `REFUSED -- no <seat> row` | not attempted (content veto on the row) | no | COMPLETED |
| `FAILED -- <reason>` | attempted, push refused | YES | DEFERRED, pending left |
| `HELD -- <reason>` | veto gate held the ref | YES | DEFERRED, pending left |

The hypothesis conflates two different strings. `REFUSED` is a content veto on a
row that would carry no `aa` entry — no publish happened, nothing to defer, and
`tests/.../test_rotate_key_authority.py:~640` asserts the ref stays put. A push
that the remote actually refuses is reported `FAILED`, and that one DOES defer:
`test_ef56_refused_authority_push_fails_and_defers_the_swap` asserts
`seat_key.read_bytes() == before`.

## Evidence

Raw: `<session>/full-file.txt` (HEAD, 28 passed), run-2 numbers above
(6f5ee34e5c, 18 passed / 2 ef56 passed). Behaviour did NOT change between
6f5ee34e5c and HEAD: the discriminator and its two committed tests are the same
at both revisions, so the claim was already false when the node's THOUGHT
(director-engine 09-24) recorded that dispatching it would regress a deliberate
design. Line drift only: 17579 in the claim -> 17617/17675 at HEAD.

Verdict: DISPROVED. "REFUSED/SKIPPED defers the swap" is a REGRESSION against
EF.56 C3. The true invariant, which is narrower and holds: an ATTEMPTED publish
that did not succeed (`FAILED`/`HELD`) defers; a non-attempt (`SKIPPED`/
`REFUSED`) completes the swap. If the claim is ever revived, it must be restated
as the FAILED/HELD half.

## Agent Notes
Ran the committed EF.56 discriminator at HEAD (2/2 ef56, 28/28 file) and at 6f5ee34e5c via a throwaway git-archive tree (2/2 ef56, 18/18 file): identical behaviour, gate body byte-identical. SKIPPED/REFUSED completes the swap by design (EF.56 C3); only FAILED/HELD defers. Claim is a regression, not a defect.

REVIEW (parent a00-cb998e3e, DH.405) — ACCEPTED, verdict disproved stands. Checked the artifacts, not the report: the deliverable named in the node is the two pytest runs, and both reproduce (HEAD 2/2 ef56 re-run by me; 6f5ee34e5c via git-archive into a throwaway tree, which is read-only on the shared checkout — the correct move given the no-git rule). The node carries a real title, not a derived A00 one. No engine bytes moved, which is the point: the near miss for this brief was a kid "fixing" rotate.py to defer on REFUSED/SKIPPED and quietly editing test_ef56_no_authority_branch_skips_and_completes_the_swap to match, producing a green suite over a regressed design. It did not, and its body says why. The narrower true invariant is now written down: ATTEMPTED-and-unsuccessful (FAILED/HELD) defers, non-attempt (SKIPPED/REFUSED) completes.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review of DH.405, from the BYTES not the result file. (1) WHAT THE BRIEF SAID: adjudicate, do not fix — no engine edit, do not touch the EF.56 discriminator test, prove the claim false against today bytes and against 6f5ee34e5c if a tmp checkout is safely possible. (2) WHAT THE MACHINE ACTUALLY DOES: rotate.py:17675 _authority_publish_gates_swap returns True only for HELD/FAILED; I imported the real module at HEAD and drove the eight exact gate states through it (SKIPPED/REFUSED in full and bare form -> False; FAILED/HELD full and bare -> True; None and empty -> False), 8/8 as the docstring promises, and re-read the same 13 lines I read before the kid was spawned — byte-identical, so zero engine bytes moved. The kid also re-ran the suite itself: -k ef56 green at HEAD and at a git-archive tree of 6f5ee34e5c, same two tests, so the claim was false on the 09-24 commit too and only the line numbers drifted. (3) THE NEAR MISS: a kid that edits rotate.py so REFUSED/SKIPPED gates the swap and edits test_ef56_no_authority_branch_skips_and_completes_the_swap to match — a fully green suite over a regressed design, indistinguishable from this run except by reading the diff. It did not take that path, and the node now carries probes plus a review note naming it. (4) DEVIATION: none from the standing rules — no git write, no commit, scratch confined to the session dir; the git-archive read was the sanctioned way to get the 6f5ee34e5c data point without a checkout in the shared tree.
<!-- THOUGHT:END -->
