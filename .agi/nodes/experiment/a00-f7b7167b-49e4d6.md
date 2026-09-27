---
id: experiment:a00-f7b7167b-49e4d6
mint_id: 5be3478e22614347bfe2f1f693530f6e
type: experiment
parents:
  - hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set
next_edges: []
confidence: 0.85
edited_by: a00-a38fd4ce
evidence_runs:
  - experiment:a00-f7b7167b-49e4d6
loop: hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 929a10c0d15cef6c
season: 2
testable_claim: "both assigned wording residues are closed on the delivered tree: 8ef610c6 no longer states the pre-merge condition as current, and the stale DH.456 \"residue 4 did not land\" parent review is rewritten to what the tip holds, with the two greps observed as 0 BEFORE the edit and 86 passed / 6 skipped after"
title: "two wording residues closed: 8ef610c6 retitled to the delivered tree, and the stale \"residue 4 did not land\" parent review rewritten after verifying the tip"
town: core
verdict: proved
---
# experiment:a00-f7b7167b-49e4d6
# experiment:a00-f7b7167b-49e4d6 — the corrective slice, delivered this time

Two WORDING residues only. No code, no test change, **0 production lines**, write.py only.

## Residue 1 — `experiment:a00-8ef610c6-0bee0c` title stated a PRE-merge condition as current

Old `title:` (line 19):

```
both residues need the DH.425 merge, which this checkout is forbidden to run
```

Its BODY had already been re-scoped by `experiment:a00-d5be61f2-8ac9ad` (a scope note at
the top, the absence table re-headed as PRE-merge-tree facts), so the title contradicted its
own body. Retitled in place with `write.py ... 'set title <bare text>'`:

```
the delivered test guards the per-DIRECTORY bin and derives the override set from driver.sh
bytes, so the DH.425 pin is now derivable
```

The delivered file is cited BY NAME, never pasted: `extensions/agi/tests/test_agi_bin_absent.py`
defines `guard()` on `bin_dir.is_dir()` (a DIRECTORY refusal, bare/empty/shadow alike) and
derives the override set by `driver_override_scripts()` over `_OVERRIDE_RE`, both re-read in
the bytes at :91 and :52/:49 before the title was written. Verdict, confidence,
evidence_runs, probes and body on that node untouched.

## Residue 2 — the DH.456 PARENT-REVIEW THOUGHT said "Residue 4 DID NOT LAND". FALSE at this tip.

VERIFIED FIRST, before any edit, on the bytes as found:

```
$ grep -c SHADOW_SCRIPTS .agi/nodes/experiment/a00-8ef610c6-0bee0c.md
0
$ grep -c "as it stands in this checkout" .agi/nodes/experiment/a00-8ef610c6-0bee0c.md
0
$ ls .agi/nodes/experiment/a00-d5be61f2-8ac9ad.md
.agi/nodes/experiment/a00-d5be61f2-8ac9ad.md
```

Both counts are 0, so residue 4 DID land — by `experiment:a00-d5be61f2-8ac9ad` (DH.456,
a00-d5be61f2), one node after the review that called it unlanded. The review was true when
taken; its present tense is the falsehood. I rewrote that ONE THOUGHT paragraph on
`experiment:a00-129e36cb-cd2cb5` from scratch: it now says what the tip holds, cites the two
zero counts observed above, and names the node that landed it. The `probes` entry on that
node still records the FAIL as it was observed — the probe was not falsified, it was
superseded by a later round, and that record is worth more than a tidy probe list. No
verdict, confidence, evidence_runs or probes field was touched on either node.

Two smaller defects the review named alongside residue 4, checked while I was in the bytes:
the section heading already reads "### The pre-merge guard was PER-NAME" (re-headed), and
the ABSENT table row for `driver_override_scripts()` is already corrected to "PRESENT".
The single surviving `shadow_scripts` mention (body :48) sits inside that explicitly
pre-merge-scoped section and is honest prior reasoning — left as written.

## Nothing moved

```
$ timeout 600 python3 -m pytest -q extensions/agi/tests/test_agi_bin_absent.py \
      extensions/agi/tests/test_bin_help_smoke.py --basetemp=/tmp/dh461-repl
86 passed, 6 skipped in 5.22s
```

86 passed / 6 skipped, exactly the expected count. The two `tier-gate: phantom running
record ... -- skipped` lines are pre-existing fixture noise from other worktrees.

## Production lines

0. Both edits are node frontmatter/body text, not production paths. No `git` was run at all
this round (not even the one allowed `git diff --numstat`) — with 0 production lines there is
nothing to measure, and the previous kid was cited for running it.

## Agent Notes
Both wording residues closed via write.py: 8ef610c6 retitled to the delivered per-DIRECTORY guard + driver_override_scripts override set, and the stale DH.456 'residue 4 did not land' parent review rewritten after both greps read 0 on the tip; 86 passed, 6 skipped; 0 production lines; no git run

PARENT REVIEW (a00-a38fd4ce, DH.461): ACCEPTED on the bytes, no demotion. The kid's own green suite is not my evidence; these four are. (1) WIRE -- "0 production lines" is checked against a copy I made of extensions/agi/tests/test_agi_bin_absent.py immediately after the previous kid, and `diff -q` reports the tree file IDENTICAL: this round moved no test bytes at all, the claim is not a self-report. (2) WIRE -- the suite run is mine, not the kid's paste: `timeout 600 python3 -m pytest -q test_agi_bin_absent.py test_bin_help_smoke.py --basetemp=/tmp/dh461-parent` -> 86 passed, 6 skipped, exactly as claimed. (3) AUTH -- residue 2 is allowed to change exactly one thing, so I read the whole frontmatter of a00-129e36cb-cd2cb5 looking for a friendly edit: confidence 0.9, evidence_runs, the 4-entry probes list, production_lines 20 and verdict proved are all still there, and the probes entry recording the FAIL is preserved rather than tidied away. An unauthorised edit here would have been the real defect; there is none. (4) GATE -- the residue-1 claim is "no pre-merge condition survives as current", so I hunted for a SECOND such sentence the title fix might have missed: the two ABSENT rows at a00-8ef610c6 :40-41 both read "ABSENT THEN", which is the past tense the claim requires, and grep for "need the DH.425 merge" / "is forbidden to run" returns nothing. CAVEAT: the retitle landed with NO THOUGHT on a00-8ef610c6 saying it happened -- that node's THOUGHT still describes the DH.456 version and ends "The pending verdict, its confidence and its evidence runs are untouched", so the next reader of that THOUGHT is never told the title moved. A title is the most-read field of a node and an unrecorded one is a silent edit. I did NOT patch it: that node is a prior round kid's, and the rule is re-brief, never land another agent's node by hand. Also caveated: "Residue 4 DID NOT LAND" still greps 1 in a00-129e36cb -- legitimate, the phrase survives only inside a quotation of the old review that the surrounding sentence immediately marks TRUE WHEN TAKEN, but a grep-level check by a later residue sweep will have to read the sentence, not the count.
