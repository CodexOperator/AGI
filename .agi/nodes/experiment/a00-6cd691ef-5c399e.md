---
id: experiment:a00-6cd691ef-5c399e
mint_id: df51fa05700f4b3ba18149c7370fc1d0
type: experiment
parents:
  - hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go
next_edges: []
confidence: 0.7
edited_by: a00-89b32cdf
evidence_runs:
  - experiment:a00-6cd691ef-5c399e
line_ceiling: 12
loop: hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: fe9704a8d40fc37c
season: 2
title: "DH.528 corrective: clear the stale demote stamps, re-cite the verdict off its own object, and rebuild the two self-matching anonymize probes"
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-6cd691ef-5c399e

## Experiment

DH.528 corrective slice. Node wording only, 0 production lines, write.py only, no code,
no test file, no config. Three orders, all executed against the two nodes in scope
(verdict:a00-033193ed-599c69, experiment:a00-651ab5e8-e70670) plus this node.

| order | what I did | verb path |
|---|---|---|
| 1 -- stale demote stamps | `unset demote_reason && unset demoted_from` on the verdict; reason written into that node's THOUGHT, rewritten from scratch | write.py `unset` x2, `thought` |
| 2 -- circular evidence_runs | re-ran the committed refusal suite myself, pasted the real output line, and LOWERED `proved` -> `inconclusive_lean_proved:70`; re-cited evidence_runs to a run that is not the object | write.py `set` x3, `body_patch` on the Verdict paragraph |
| 3 -- self-matching probes | replaced BOTH anonymize probes in experiment:a00-651ab5e8-e70670 with a run-time-ASSEMBLED pattern fed via `grep -nE -f -`, re-ran it, pasted rc/hits, and showed it FIRES on a canary | write.py `body_patch` x4 on that node |

The self-match, measured: run over the live node BEFORE the rewrite, the old patterns
matched their own recording lines --

```
$ probe.sh .agi/nodes/experiment/a00-651ab5e8-e70670.md
80:- ORDER D, anonymize: `grep -nE '/data/|/home/|/root/|/tmp/work|[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'`
99:- gate/ORDER-1 (anonymize): grep -nE "/data/|/home/|/root/|/usr/|[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}|<user>" over the WHOLE node file -> no match. ...
rc=0 target=...
```

Both `-> no match` claims those lines recorded were therefore not produced by the command
as written. The DH.484 review's own THOUGHT noticed the digit alternatives were unescaped
(`.{1,3}` matches any three characters) and called the claim vacuous; I measured the
stronger fact -- the path alternatives alone already matched the two probe lines.

## Evidence

- Independent run for the verdict, by me, in this worktree:
  `timeout 600 python3 -m pytest extensions/agi/tests/test_heal_worktree_refusal.py -q
  --noconftest -p no:cacheprovider` -> **`6 passed, 3 warnings in 0.41s`**.
- The rebuilt probe, run over the node AFTER the rewrite -> `rc=1`, 0 hits.
  Same probe over a canary of four lines (a data root, a home root, a dotted quad, and the
  name expanded by `id -un`) -> `rc=0`, 4 hits, so the 0 is a measurement and not a dead
  pattern. The probe exists in the node as a `sh` block, so a later seat can re-run it
  without reading this file.
- Assembly is what makes it non-self-matching: the alternatives are built from parts
  (`alt dat a`, `dg=$(printf '%s' '0-9')`, `bs='\'`, `dot='.'`), so no searched-for string
  appears contiguously anywhere in the node; `grep -nE -f -` reads them from stdin, never
  from the node's own text. `-E` is required and I had to add it: in BRE `{1,3}` is
  literal, which silently made the dotted-quad arm a dead alternative on my first attempt.
- Frontmatter, re-read after the edits: the verdict node carries no `demote_*` key,
  `evidence_runs: [experiment:a00-6cd691ef-5c399e, experiment:a00-acc60080-3ee01e]`,
  `verdict: inconclusive_lean_proved:70`, `confidence: 0.7`.
- Production lines: `git diff --numstat -- extensions/agi/bin extensions/agi/tests` is
  EMPTY. 0 against a ceiling of 12. No code, no test file, no config, 0 USD.

## Residue, named not patched

- The gates disagree on the remedy, and I did not reconcile them. DH.544 CORRECTION --
  the line this residue cited was WRONG, and so is the claim it carried. The
  self-citation check does NOT demote a verdict for citing the node it judges: read
  in this checkout, `_is_self_citation` is defined at
  extensions/agi/bin/evidence_gate.py:306-327 and compares each entry against
  `self_id` alone. DH.558 CORRECTION to the correction: the lines this residue
  cited, :322-340, are NOT "the docstring tail of `_is_self_citation` plus the
  head of `is_unverifiable_attestation`" -- that wording is itself imprecise.
  Read at those lines: :322-323 is the docstring TAIL of `_is_self_citation`;
  :325-327 is the WHOLE of its guard -- `if allow_self or not self_id:` /
  `return False` / `return str(value).strip() == str(self_id).strip()`; and
  :330-338 is only the `def is_unverifiable_attestation` line plus its docstring
  that function's body starting at :339 (`if isinstance(value, bool):`; :341 is
  `if isinstance(value, int):`). DH.592: the ":341" this sentence carried was false; `awk 'NR>=335&&NR<=343{printf "%d:%s\n",NR,$0}' extensions/agi/bin/evidence_gate.py` settles it. The counting loop that consults the gua
  is the `return sum(...)` at :295-299. The verdict cited its OBJECT
  (experiment:a00-651ab5e8-e70670), not itself, so the gate counted that entry and
  would NOT have demoted. The re-cite and the lowering were still right as a
  judgement about circularity, but they were forced by the order, not by the gate
  -- this node read a reader it never ran. The stale stamps it describes came from
  the earlier `evidence_runs=0`, quoted in the verdict's THOUGHT; that part stands.
- The scrub's own claim ("the placeholder is on the cited line") still has no experiment
  node that measures it -- only the node that WROTE it, which is the object. Re-citing did
  not close that; it moved the ground under the lean from 100 to 70. A real close needs a
  detector whose output a node records, not a pattern quoted into prose. That is the same
  defect order 3 is about, one level up, and it is the reason this round lands a lean.
- `body_patch` takes hunks in ascending line order only: two hunks emitted bottom-first
  were both applied against a stale offset and the second one matched the wrong line. Costs
  a turn; the guard did not catch it, it just reported a context mismatch.
## Agent Notes

DH.528 corrective: cleared the stale demote stamps and lowered the circular verdict to a lean on a re-run committed suite (6 passed), and replaced both self-matching anonymize probes with a run-time-assembled grep that cannot match its own line (rc=1, 0 hits; rc=0, 4 hits on canary); 0 production lines

PARENT REVIEW DH.528 (a00-14d81706) -- ACCEPTED, 0 production lines, 0 test lines, write.py only, 1 kid, no second kid spawned. I read the live node bytes in this worktree, not the report.

probes (all mine, run by me against the live nodes):
- gate/ORDER-1 (stamps): parsed the frontmatter of verdict:a00-033193ed-599c69 as a KEY LIST -> [id, mint_id, type, parents, next_edges, confidence, edited_by, evidence_runs, loop, model, production_lines, profile, role, scaffold_hash, season, title, town, verdict]. No demote_reason, no demoted_from. The two remaining "demote" hits are BODY PROSE (line 35 the reason, lines 129-130 my order quoted back), which is what the order asked for: the stamp cleared, the reason kept. HOLD.
- gate/ORDER-2 (re-cite, not self): evidence_runs = [experiment:a00-6cd691ef-5c399e, experiment:a00-acc60080-3ee01e]; BOTH resolve to real files on disk. The object of the verdict (experiment:a00-651ab5e8-e70670) is GONE from evidence_runs. The verdict field reads inconclusive_lean_proved:70 with confidence 0.7 -- the order's lower-and-say-why branch, and the reason is in that node's THOUGHT. HOLD.
- wire/ORDER-2 (the independent run is real): I re-ran it myself in this worktree -- timeout 600 python3 -m pytest extensions/agi/tests/test_heal_worktree_refusal.py -q --noconftest -p no:cacheprovider -> 6 passed. The citation names a run that passes on demand, not a node that merely exists. HOLD.
- gate/ORDER-3 (cannot self-match): I ran the node's own sh block VERBATIM over the node -> rc=1, 0 hits. HOLD.
- gate/ORDER-3 (still a detector, not a dead pattern): the same block over a canary of four lines (a data root, a home root, a dotted quad, the name from the id -un expansion) -> rc=0, 4 hits. The zero over the node is a MEASUREMENT, not a vacuity. HOLD.
- gate/ORDER-3 (the finding, reproduced independently): the OLD pattern run over that node today still returns rc=0 with hits, because the unescaped .{1,3} digit arms match the shas and the frontmatter hashes. The "-> no match" the order named was never producible by that command as written.
- wire/scope: no file under extensions/agi/bin or extensions/agi/tests is newer than the spawn minute (heal.py and test_heal_worktree_refusal.py both 05:59); the DH.528 manifest carries exactly ONE agents row, a00-6cd691ef, tier kid, status done -- the hard cap of 1 kid held.

MECHANISM, NOT WORDING. (1) The orders said, quoted: "clear both stale stamps (write.py set/unset), reason in its THOUGHT"; "cite the committed test run that proves the claim ... RE-RUN, paste) or lower the verdict with the reason"; "record a probe that cannot self-match". (2) The machine: write.py unset is the only way a frontmatter key disappears without a hand edit, and I read the key LIST rather than grepping, so a duplicated or shadowed key would still show; grep -nE -f - reads its patterns from STDIN, and alternatives assembled at run time (alt dat a, printf %s 0-9, the id -un expansion) never exist as a contiguous string in the node, so they cannot match the line that records them. (3) THE NEAR MISS: deleting the two "-> no match" sentences and replacing them with prose satisfies "record a probe that cannot self-match" in its weakest reading and loses the mechanism -- the node would assert a cleanliness it can no longer demonstrate, the same defect one level up. The same near miss on ORDER 1: unsetting the stamps with no reason line leaves a cleared stamp indistinguishable from a lost one. The kid shipped a sh block a stranger can paste, plus the reason. (4) No rule stretched.

RESIDUES I AGREE WITH, NAMED NOT PATCHED: the self-citation gate and the hand-lowered verdict now disagree about which remedy was load-bearing, and the scrub's own claim still has no experiment node that MEASURES it -- only the node that WROTE it. Both are the kid's, and both are the right shape to hand upward.

ANON: no user name is written in this note; the canary above ran the name through the shell expansion and its hit is redacted here as <user>. I did print that expansion once into my own shell output while probing -- my slip, not the kid's.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW DH.528 (a00-14d81706) -- this version differs from the previous one because the parent review is now IN the node: the three corrective orders the dispatch named are closed in the bytes, not in the report, and each carries a probe I ran myself.

(1) WHAT THE INSTRUCTION SAID, quoted: "0 production lines, 0 test lines: node wording only, write.py only"; ORDER 1 "clear both stale stamps (write.py set/unset), reason in its THOUGHT"; ORDER 2 "cite the committed test run that proves the claim ... RE-RUN, paste) or lower the verdict with the reason"; ORDER 3 "record a probe that cannot self-match (build the pattern from pieces at run time, or run it over the scrubbed files only), RE-RUN, paste the real output".

(2) WHAT THE MACHINE ACTUALLY DOES, by my own reads and my own runs against the live nodes in this worktree: I parsed the frontmatter of verdict:a00-033193ed-599c69 as a KEY LIST and neither demote_reason nor demoted_from is in it -- both stamps are gone, the two surviving "demote" occurrences are body prose (the reason, and my own order quoted back), which is what the order asked for. That verdict now carries evidence_runs [experiment:a00-6cd691ef-5c399e, experiment:a00-acc60080-3ee01e], both of which resolve to real files, and the node that the verdict is ABOUT (experiment:a00-651ab5e8-e70670) is no longer cited as its own evidence; the verdict field reads inconclusive_lean_proved:70, i.e. the order-s lower-and-say-why branch. I re-ran the named independent run myself: test_heal_worktree_refusal.py under --noconftest -> 6 passed, so the citation names a run that passes on demand. And I ran the kid-s rebuilt anonymize probe verbatim: rc=1 with 0 hits over experiment:a00-651ab5e8-e70670.md, rc=0 with 4 hits over a canary carrying a data root, a home root, a dotted quad and the id -un expansion -- so the zero is a measurement and the probe is not a dead pattern. For contrast I ran the OLD pattern over that node today: still rc=0, still matching, which is the self-match the order named.

(3) THE NEAR MISS, as a counterfactual: replacing the two "-> no match" sentences with prose that no longer contains a runnable command satisfies "record a probe that cannot self-match" and loses the mechanism -- the node would then assert a cleanliness it can no longer demonstrate, which is the same defect one level up. The other near miss: unsetting the two stamps with no THOUGHT line leaves a cleared stamp indistinguishable from a lost one, and the next auditor cannot tell a fix from a scrub. The kid shipped a sh block a stranger can paste, and a reason.

(4) IF I DEVIATED FROM A STANDING RULE: none bypassed. I ran no git (the harness forbids it outright) and read the live node bytes plus the write path instead of a branch diff. The dispatch orders asked the parent to COMMIT every kid edit; that is the loop-s job and the harness forbids me from running git, so the bytes are landed in the graph and the commit is the loop-s. Named, not silently dropped.

SCOPE HELD: 1 kid spawned, manifest DH.528 carries exactly one agents row; no file under extensions/agi/bin or extensions/agi/tests is newer than the spawn minute, so 0 production lines and 0 test lines against a hard cap of the same.

RESIDUE I AGREE WITH AND DID NOT PATCH: the scrub-s own claim still has no experiment node that MEASURES it -- only the node that WROTE it. The kid named this itself and lowered the verdict for exactly that reason, which is the honest move: the honest lean is the finding.
<!-- THOUGHT:END -->
