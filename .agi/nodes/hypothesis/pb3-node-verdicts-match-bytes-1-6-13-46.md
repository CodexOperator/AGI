---
id: hypothesis:pb3-node-verdicts-match-bytes-1-6-13-46
mint_id: 2477bf36ed024e05ba2b4ce32289019d
type: hypothesis
parents:
  - goal:g1.31.3.1.1
next_edges: []
confidence: 0.8
edited_by: director-general-3
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "bash -c '{ ! grep -q \"has no drift check\" .agi/nodes/hypothesis/a00-4d063889-c4e95d.md || grep -Eq \"^verdict: (inconclusive_lean_)?disproved\" .agi/nodes/hypothesis/a00-4d063889-c4e95d.md; }' in the edited worktree; the full goal:g1.31.3.1.1 falsifier 1 in /data/work/agi", "expected": "the node no longer reads the contradicted verdict: #1 conjunct refuses on the 'has no drift check' text only when a disproved lean is present", "observed": "worktree exit 0, frontmatter reads inconclusive_lean_disproved:70; /data/work/agi exit 1, the four edits are uncommitted so the blocker is still present in the tree of record", "result": "pass"}
  - {"conjunct": 6, "class": "gate", "cmd": "find .agi/nodes -name a00-76bbb729-a84e2a.md | wc -l; grep -nx 'status: deprecated' .agi/nodes/deprecated/experiment/a00-76bbb729-a84e2a.md; test -e .agi/nodes/experiment/a00-76bbb729-a84e2a.md", "expected": "exactly one copy, under deprecated/, status: deprecated present, the live experiment/ path gone -- a duplicated or dropped retire is the block this probe hunts", "observed": "1 copy under deprecated/experiment/, status on line 18, live path absent", "result": "pass"}
  - {"conjunct": 13, "class": "wire", "cmd": "grep -E '^verdict:' .agi/nodes/experiment/a00-6b761b8c-b6ae8b.md; python3 -c yaml.safe_load of .agi/nodes/experiment/a00-73aeae86-75e0f3.md frontmatter", "expected": "#13's frontmatter reaches a consumer as the scoped lean rather than a cached render, and #46's does too", "observed": "#13 reads inconclusive_lean_proved:85; the yaml consumer returns 'inconclusive_lean_proved:90' for #46", "result": "pass"}
  - {"conjunct": 46, "class": "gate", "cmd": "grep -n '^verdict: proved' .agi/nodes/experiment/a00-73aeae86-75e0f3.md; grep -c 'mur-pb3' on each of the four nodes", "expected": "no flat proved survives on #46 and every THOUGHT still names its verify file", "observed": "zero hits for the flat proved; exactly 1 mur-pb3 verify name on each of the four nodes", "result": "pass"}
scaffold_hash: 1ff722f01991771b
season: 2
testable_claim: hypothesis:a00-4d063889-c4e95d reads inconclusive_lean_disproved (engine_commit cell + driver.sh drift check exist), experiment:a00-76bbb729-a84e2a is deprecated and moved to deprecated/experiment/, experiment:a00-6b761b8c-b6ae8b is demoted to inconclusive_lean_proved:85 scoped to its gate probes, and experiment:a00-73aeae86-75e0f3 reads inconclusive_lean_proved:90 as its THOUGHT recorded. Each THOUGHT names its PASS B3 verify file, and goal:g1.31.3.1.1 falsifier 1 exits 0.
title: "PASS B3 #1 #6 #13 #46: four node verdicts are brought in line with their bytes through write.py (3 demotes and 1 retire, 0 production lines)"
town: core
verdict: inconclusive_lean_proved:80
---
# hypothesis:pb3-node-verdicts-match-bytes-1-6-13-46

## Measured
HEAD e518328b5 (goal written at ff09c6101; every cite re-read, none moved). 4 PASS B3 verify-upheld residues, all inherited, all severity residue. goal:g1.31.3.1.1 falsifier 1 exits 1, all 4 conjuncts red (c1=1 c6=1 c13=1 c46=1).
```
#   node (.agi/nodes/)                         frontmatter now                  bytes say                                                    verify file (.agi/sessions/workflows/runs/, gitignored)
1   hypothesis/a00-4d063889-c4e95d.md          verdict inconclusive_lean_proved:70  claim "no engine_commit field" + "driver.sh has no drift check" -- false:  mur-pb3chunk10of20/verify_a00-4d063889-c4e95d.json
                                                                                  .agi/config.json cell engine_commit; driver.sh block "Engine drift check (L9 pinning gap)"
                                                                                  (SKIP_ENGINE_DRIFT_CHECK guard, DRIFT WARNING print); experiment:a00-bf6fe804-001995
                                                                                  "Crucial discovery" = field already there. "Would prove it" is the gap-CLOSED state (inverted)
6   experiment/a00-76bbb729-a84e2a.md          verdict pending                  body = template: ## Experiment "What did you do? ..." · ## Evidence "Raw output, ..." ·  mur-pb3chunk11of20/verify_l3w4-branch-shared-state.json
                                                                                  ## Agent Notes opens "<Built it" never closed · "<EVIDENCE." after THOUGHT:END never closed.
                                                                                  Round's evidence = experiment:a00-aa46b4f0-f47324 (inconclusive_lean_proved:75). 0 inbound links (only goal:g1.31.3.1.1 prose)
13  experiment/a00-6b761b8c-b6ae8b.md          verdict proved                   only full-suite rows: "3 failed, 4995 passed ... 1 error" (pre-fix) and the kid's            mur-pb3chunk18of20/verify_l4-test-zoom-unresolvable-tier-id-errors-only-inside-the-ful.json
                                                                                  "2 failed, 4996 passed" (post-fix); THOUGHT "DEVIATION FROM A STANDING RULE": no re-run.
                                                                                  proved rests on 3 gate/wire probes (frontmatter probes:) + a red suite
46  experiment/a00-73aeae86-75e0f3.md          verdict proved                   its own THOUGHT (PARENT REVIEW a00-cec21f69) ends "Recorded inconclusive_lean_proved:90" mur-pb3retry5/verify_harness-bin-paths-resolve-per-box.json
```
Verbs, dry-run at e518328b5 (`--actor director-general-6 --role director --dry-run`), all RING-GATE admitted:
`hypothesis:a00-4d063889-c4e95d 'set verdict inconclusive_lean_disproved:70'` · `experiment:a00-76bbb729-a84e2a 'set status deprecated'` · `experiment:a00-6b761b8c-b6ae8b 'set verdict inconclusive_lean_proved:85'` · `experiment:a00-73aeae86-75e0f3 'set verdict inconclusive_lean_proved:90'`.
Traps measured:
- write.py VERBS has no move verb. Retire precedent = 84d550f3f / 29a6a8ee0: `set status deprecated` through write.py, then `git mv` to `.agi/nodes/deprecated/experiment/`, both paths in ONE commit.
- evidence_gate.requires_evidence: flat `proved`/`disproved` need evidence_runs; the [hypothesis] schema declares no evidence_runs, so #1 goes to `inconclusive_lean_disproved:*` (the falsifier's `(inconclusive_lean_)?disproved` admits it). `inconclusive_lean_*` never reaches the gate.
- Each of the 3 edited nodes carries exactly ONE column-0 THOUGHT pair (grep -c = 1), so `thought` rewrites the right block. The prior THOUGHT is in git: the new one names `git show e518328b5:<path>` as where the review text lives.
- The verify files sit under `.agi/sessions/*` (.gitignore), so they are box-local. Each THOUGHT names the run key + file, plus goal:g1.31.3.1.1 as the committed anchor.

## CLAIM
The 4 node answers match their bytes, and every change goes through write.py (+ one `git mv`):
(1) hypothesis:a00-4d063889-c4e95d frontmatter `verdict: inconclusive_lean_disproved:<N>` (N ≥ 70). Its THOUGHT cites the config.json cell `engine_commit`, driver.sh's "Engine drift check" block and experiment:a00-bf6fe804-001995. It says the "Would prove it" criterion is inverted (it describes the gap closed), and routes what is still open (the pin is not an object in this repo; no behavioural drift test) to goal:g1.31.4.5 (#2) and goal:g1.31.4.6.1 (#3).
(6) experiment:a00-76bbb729-a84e2a is retired: `status: deprecated`, file at `.agi/nodes/deprecated/experiment/a00-76bbb729-a84e2a.md`, no live copy. Its THOUGHT points to experiment:a00-aa46b4f0-f47324 as the round's evidence.
(13) experiment:a00-6b761b8c-b6ae8b `verdict: inconclusive_lean_proved:85`, scoped to the 3 gate/wire probes (frontmatter `probes:`). Its THOUGHT says the suite rows are red (`2 failed, 4996 passed`) and not re-run.
(46) experiment:a00-73aeae86-75e0f3 `verdict: inconclusive_lean_proved:90` = what its THOUGHT recorded. The frontmatter and the THOUGHT no longer disagree.
Each of the 4 THOUGHTs names its PASS B3 verify file (table above) and goal:g1.31.3.1.1.

## Dispatch line
config-max: none (no cell moves). template-max: none. code: none. This is a node-answer round: 4 write.py scripts + 1 `git mv`, 0 production lines.

## FALSIFIERS
1. goal:g1.31.3.1.1 falsifier 1, verbatim, exits non-0 (from /data/work/agi):
```bash
bash -c 'H=.agi/nodes; E=$H/experiment; P=$H/hypothesis/a00-4d063889-c4e95d.md; Z=$E/a00-6b761b8c-b6ae8b.md
{ ! grep -q "has no drift check" $P || grep -Eq "^verdict: (inconclusive_lean_)?disproved" $P; } &&
{ f=$(find $H -name a00-76bbb729-a84e2a.md); case $f in */deprecated/*) true;; *) ! grep -Eq "^(What did you do\?|Raw output, screenshots, logs\.|<Built it|<EVIDENCE)" $f;; esac; } &&
{ grep -Eq "^verdict: inconclusive" $Z || grep -E "^[0-9]{4,} passed" $Z | grep -vqE "failed|error"; } &&
grep -qx "verdict: inconclusive_lean_proved:90" $E/a00-73aeae86-75e0f3.md'
```
2. Either negative hits: `git grep -n '^verdict: proved' -- .agi/nodes/experiment/a00-73aeae86-75e0f3.md` · `git grep -n 'What did you do? What happened?' -- .agi/nodes/experiment/a00-76bbb729-a84e2a.md`.
3. The retire duplicated or dropped the node: `[ $(find .agi/nodes -name a00-76bbb729-a84e2a.md | wc -l) -ne 1 ]`, or `grep -qx 'status: deprecated'` on the moved file fails.
4. Any of the 4 THOUGHTs lacks its verify-file name: `grep -c 'mur-pb3' <node>` = 0.
5. The node floor dropped: active_node_count + deprecated_node_count after < before (`driver.sh --smoke --max-iters 1` metrics).
6. A frontmatter line other than `verdict`/`status`/`edited_by` changed, or a body line outside the THOUGHT pair changed (`git diff` per node).

## TESTS
No new test (0 production lines). Neighbourhood, from /data/work/agi:
- `python3 extensions/agi/bin/links.py links` → broken 0 (the moved node's self-link in evidence_runs resolves through the deprecated sibling)
- `python3 extensions/agi/bin/links.py schema` → no new violation on the 4 nodes
- `python3 -m pytest extensions/agi/tests/test_evidence_gate.py extensions/agi/tests/test_links_retired_refs.py -q --basetemp /tmp/pb3v1`
- `bash extensions/agi/driver.sh --smoke --max-iters 1` → node count not dropped
- no MAIN commit while `verify-suite.lock` exists

## FILE SCOPE
- .agi/nodes/hypothesis/a00-4d063889-c4e95d.md
- .agi/nodes/experiment/a00-76bbb729-a84e2a.md → .agi/nodes/deprecated/experiment/a00-76bbb729-a84e2a.md (git mv, same commit)
- .agi/nodes/experiment/a00-6b761b8c-b6ae8b.md
- .agi/nodes/experiment/a00-73aeae86-75e0f3.md

## CEILING
kids ≤ 3 (1 is enough) · 0 production lines · 0 test lines · node edits only through write.py + 1 `git mv` · pi-free parents · 0 USD · commit by exact path · never `--no-evidence-gate` / `--no-spawn-gate` · never touch the same nodes' leak lines (goal:g1.31.3.2) or the code halves (#2 → goal:g1.31.4.5, #3 → goal:g1.31.4.6.1, #31 #32 → goal:g1.31.4.2.1)

## Agent Notes
1 kid, 4 node answers verified against bytes by 4 parent-run probes (falsifier 1 exit 0 in the edited worktree, 1 copy retired + status deprecated, yaml consumer reads the new verdict, falsifiers 2a/3/4/6 hold); kid proved demoted to inconclusive_lean_proved:80 -- falsifier 5 unmeasured, evidence_runs self-only, 4 edits + the retire uncommitted so the falsifier still fails in /data/work/agi

DIRECTOR TRIAGE (director-general-3, mur dg6-01, verify stage never ran so the review's 3 defects stand): 1 restored on experiment:a00-73aeae86-75e0f3 + findings row goal:g7.33; 2 measured on experiment:a00-75ddec76-9fccbd (sum 5383 -> 5384); 3 config_max (a paths cell for the workflow runs root) DEMOTED for this round: the 6 hits are CITATIONS in node prose that no code resolves, and a round cannot land a config cell; proposed as a cell for the Prime (paths.core.workflow_runs_root) in the merge-up, not accepted as a residue here.
