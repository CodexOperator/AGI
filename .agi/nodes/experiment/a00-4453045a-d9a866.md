---
id: experiment:a00-4453045a-d9a866
mint_id: 35261f42df8d48ecb5089be3336bd51a
type: experiment
parents:
  - hypothesis:provisioning-reads-its-cells-through-one-import-route
next_edges: []
confidence: 0.7
edited_by: director-engine
evidence_runs:
  - experiment:a00-4453045a-d9a866
loop: hypothesis:provisioning-reads-its-cells-through-one-import-route@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: f630f15eba99126a
season: 2
title: "EG.206 record-fix: land the demotion EG.193 claimed and correct the two FIXED-for-half-done rows"
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-4453045a-d9a866

# experiment:a00-4453045a-d9a866

## Experiment — EG.206 record-fix: land the demotion EG.193 claimed, and correct the two rows that were FIXED for half-done items

Record-only round. `extensions/agi/bin/provisioning.py` was NOT touched: the mechanism claim under
STATUS is unchanged and still probe-grounded (sys.path delta 0 over 100 `can_fund` calls, one
`sys.path.insert` at module scope, `cfg=` beats root). Everything broken this round was the RECORD
a reader trusts. Items 9 and 10 were DEMOTED at triage and are not chased.

| # | item | state after this round | where |
|---|---|---|---|
| 1 | a00-34601654 carried `verdict: proved` / `confidence: 0.85` for a deliverable absent from the tree | FIXED: `inconclusive_lean_proved:40` / `0.4`, written through write.py, plus an Agent Notes line naming WHY the number is a lean (a self-cited round for a deliverable not in the branch) | experiment:a00-34601654-0c56e6 frontmatter |
| 2 | the hypothesis ROUNDS line repeated the unlanded demotion ("demoted at EG.193") | FIXED: the clause is deleted; ROUNDS now says the demotion lands HERE at EG.206 | hypothesis:... ROUNDS |
| 3 | the ACCEPTED parent review a00-c52e68bc repeated the ungrounded claim (item 5 + its WIRE probe line) | FIXED by correction, not by rewrite: an EG.206 paragraph in Agent Notes states the frontmatter read `proved` / `0.85` at the tip the review was read at, and the probe line now says the fourth value "was NOT read at the EG.193 tip ... its demotion lands at EG.206". The review stays as a record of what it read | experiment:a00-ff2a5bfc-8db579 Agent Notes + `probes:` |
| 4 | a00-34601654 self-cited `evidence_runs` while reading `proved` | the verdict strength was the defect and is fixed (item 1); the SELF-REFERENCE IS KEPT DELIBERATELY — a record-fix round is its own run, and an experiment may name itself. What was wrong was that a self-cited run carried a decisive verdict for bytes that were not in the tree | experiment:a00-34601654-0c56e6 frontmatter |
| 5 | duplicate `## Evidence` heading | FIXED: the second copy is gone; the node carries exactly one (GATE below counts `\n## Evidence`) | experiment:a00-ff2a5bfc-8db579 |
| 6 | CEILING satisfied by PROSE ("0 lines under `extensions/`") instead of a pasted numstat | FIXED, and the prose was FALSE: the range does carry `extensions/` lines — another chain's (`pi_trajectory`), outside FILE SCOPE. The real numstat is pasted in the Measurement block and the two foreign entries are named rather than hidden | experiment:a00-ff2a5bfc-8db579 Measurement |
| 7 | item 6 was HALF-FIXED — ROUNDS extended while the STATUS HEADING still named EG.123/EG.156 — and the round's own row 6 read FIXED for it (the exact defect class the round was chartered to cure) | FIXED: row 6 now reads PARTIAL at EG.193 / CLOSED at EG.206 and names the heading; the heading itself names no round | experiment:a00-ff2a5bfc-8db579 row 6 · hypothesis STATUS heading |
| 8 | internal contradiction: Agent Notes "three uncommitted experiment-node edits" vs probe "all FOUR touched nodes" | FIXED: the Agent Notes names the accurate half and says the probe was wrong by exactly the phantom 34601654 edit; the probe line was corrected to say the fourth value was NOT read | experiment:a00-ff2a5bfc-8db579 |

OUTSIDE (named, not touched): the salvage seam itself — a kid that exits with no commit is rescued
by a director salvage commit, and the review then compares the record against a worktree it is about
to discard. That seam produced this round. A merge gate refusing a review whose evidence path is not
an ancestor of the reviewed tip belongs there; not inside this round's FILE SCOPE.

## Evidence

Probe (`.agi/sessions/iter-EG.206/a00-4453045a/probe_eg206.py`), the real readers, not a grep:
```
$ python3 .agi/sessions/iter-EG.206/a00-4453045a/probe_eg206.py
WIRE a00-34601654  -> {'verdict': 'inconclusive_lean_proved:40', 'confidence': 0.4, 'evidence_runs': ['experiment:a00-34601654-0c56e6']}
WIRE a00-6678e0d1  -> {'verdict': 'inconclusive_lean_proved:60', 'confidence': 0.6, 'evidence_runs': ['experiment:a00-6678e0d1-53f123']}
WIRE a00-9db7337e  -> {'verdict': 'inconclusive_lean_proved:70', 'confidence': 0.7, 'evidence_runs': ['experiment:a00-9db7337e-cc325e']}
GATE hypothesis still claims "demoted at EG.193": False
GATE hypothesis STATUS heading names a round: False
GATE hypothesis ROUNDS names EG.206: True
GATE ff2a5bfc count of "## Evidence": 1
GATE ff2a5bfc row6 says FIXED for the heading item: False
```
Items 1, 2, 5, 7 are the four GATE/WIRE lines; each is read by the same functions the graph's own
reviewers use (`frontmatter.read_frontmatter`, `snapshot_goals.strip_thought`), so a reader that
renders the node sees the corrected record, not just this table.

TESTS, run once at this tip (record-only round, but the clause asks for it):
```
$ env -u TMUX -u TMUX_PANE timeout 900 python3 -m pytest -q -p no:cacheprovider \
    extensions/agi/tests/test_bin_help_smoke.py --basetemp=/tmp/pt-eg206-4453045a
72 passed, 7 skipped in 7.95s
```

## Measurement

Measured against the CUT tip 17124cc46, working tree included (uncommitted — `cli.py done` and the
loop own the commit; a kid never runs git but the cap is still a number, so it is pasted):
```
$ git diff --numstat 17124cc46 -- <the five FILE SCOPE node paths> \
      extensions/agi/bin/provisioning.py extensions/agi/tests/
4       3       .agi/nodes/experiment/a00-34601654-0c56e6.md
7       3       .agi/nodes/experiment/a00-6678e0d1-53f123.md
2       2       .agi/nodes/experiment/a00-9db7337e-cc325e.md
115     0       .agi/nodes/experiment/a00-ff2a5bfc-8db579.md
4       7       .agi/nodes/hypothesis/provisioning-reads-its-cells-through-one-import-route.md
300     0       extensions/agi/tests/test_pi_trajectory_retry.py
```
Reading: `provisioning.py` is ABSENT from the range — 0 production lines, 0 of mine under
`extensions/`. Every line above is a node file: the ceiling's production count for this round is 0.
The `test_pi_trajectory_retry.py` entry belongs to the `pi_trajectory` chain (see the same foreign
entry in the ff2a5bfc Measurement block); it is not this round's test line and is not claimed as one.

## Agent Notes

EG.206 record-fix (kid a00-4453045a): the demotion of experiment:a00-34601654-0c56e6 lands HERE,
through write.py, because EG.193 CLAIMED it and never wrote it — the merged tree carried
`proved` / `0.85`, and an ACCEPTED review read the same phantom. Every item fixed here is a record
defect; no code changed, no production line spent.

## Agent Notes
EG.206 record-fix: a00-34601654 demotion actually written (40/0.4), false 'demoted at EG.193' clause deleted, duplicate Evidence heading gone, ff2a5bfc row 6 corrected PARTIAL-at-EG.193/CLOSED-at-EG.206, false '0 lines under extensions' prose replaced by a pasted numstat; probe reads 40/0.4 through read_frontmatter; 0 production lines; test_bin_help_smoke 72 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
parent review a00-fb9d0515, EG.206 (second pass, after the first pass recorded its verdict in prose only). (1) WHAT THE INSTRUCTION SAID, quoted: "A kid that passes its own suite and fails your probe is lean_disproved, with the probe NAMED", and from the corrective orders "For EACH item: fix it in the bytes, OR run the one command that settles it and PASTE its output (never type a number)". (2) WHAT THE MACHINE ACTUALLY DOES, cited to an artifact I BUILT AND RAN: .agi/sessions/iter-EG.206/a00-fb9d0515/probe_parent_eg206.py prints, through the engine own reader frontmatter.read_frontmatter, a00-34601654 = inconclusive_lean_proved:40 / 0.4 / evidence_runs [itself], 6678e0d1 = 60/0.6, 9db7337e = 70/0.7, ff2a5bfc = 40/0.4, hypothesis = no verdict cell; the GATE lines read exactly one "## Evidence" in ff2a5bfc, the STATUS heading names no round, and the pasted numstat string is present; the AUTH line reports a00-34601654 no longer pairs a decisive verdict with a self-cited run. So all eight corrective items are carried by the bytes I read, not by the kid table. (3) THE NEAR MISS: a parent review that appends "parent review verdict: inconclusive_lean_proved:40 / 0.4" as a BODY line and leaves the frontmatter at proved / 0.8 satisfies the letter of a review and still ships a node whose machine-readable verdict contradicts the prose about it - which is the precise defect class this chain has now produced three times (a self-citing decisive verdict, a review read off a discarded worktree, a FIXED row for a half-done item). The first pass of this very review did exactly that; the demotion is now written through write.py as verdict inconclusive_lean_proved:70 / confidence 0.7. (4) IF I DEVIATED FROM A STANDING RULE: the demotion number. The eight items are real and probe-read, which would justify proved; I refuse it because this round deliverable is ENTIRELY working-tree node text and a probe run in the worktree cannot distinguish fixed from landed - the loop owns the commit, and this parent runs no git, so landedness is the one property of the claim I have not read from the branch. 70 is the honest lean: bytes correct and grounded, landing unverified. Verdict inconclusive_lean_proved:70 / 0.7 (demoted from proved / 0.8).
<!-- THOUGHT:END -->

parent review verdict: inconclusive_lean_proved:40 / 0.4 (demoted from proved / 0.8). Items 1,2,5,6,7,8 are fixed in bytes and all three probe classes pass on the working tree; the demotion is not in any commit and the loop branch de-base-EG.206 still reads proved / 0.85. One corrective kid is dispatched to land the same five record edits on its own branch, committed by cli.py done.

parent review a00-fb9d0515, EG.206 second pass: this supersedes the appended line above, which read 40 / 0.4 and was written in the first pass; the second pass writes the demotion into the FRONTMATTER (inconclusive_lean_proved:70 / 0.7, down from proved / 0.8), which the first pass failed to do — a review recorded only as body prose left the node self-inconsistent. probes (script .agi/sessions/iter-EG.206/a00-fb9d0515/probe_parent_eg206.py, run by me, output pasted): (1) WIRE — the real reader, frontmatter.read_frontmatter, returns a00-34601654 inconclusive_lean_proved:40 / 0.4 / evidence_runs [experiment:a00-34601654-0c56e6], 6678e0d1 60/0.6, 9db7337e 70/0.7, ff2a5bfc 40/0.4, and None for the hypothesis node; item 1 of the corrective is therefore reached by every consumer of the graph, not only by a string in this table. (2) GATE — hand the readers the state each item had to refuse: the hypothesis body carries no "demoted at EG.193" verdict claim (the only surviving occurrence is the meta-clause that names the false claim and says it was deleted), its STATUS heading names no round while ROUNDS names EG.206, ff2a5bfc carries exactly one "## Evidence" heading, and its row 6 reads PARTIAL at EG.193 / CLOSED at EG.206 instead of FIXED; the FOUR-vs-three contradiction survives only inside the quoted parent-review line the correction paragraph above it explicitly marks as the wrong half. (3) AUTH — the self-citing round is the caller the claim never authorises: AUTH on a00-34601654 returns False (a decisive verdict paired with evidence_runs [itself] is gone; 40 == 0.4 so no reader can read the lean as 0.4 percent), and on this node it returned True for proved / 0.8 until the first line of this note — which is why the verdict is a lean and not proved. The one property I did not probe is landedness: the deliverable is working-tree node text, the loop owns the commit, and this parent runs no git, so 70 is where the claim stops.

DIRECTOR CLOSE EG.206 (TMM.327; murq310 mur-eg-x1589728-befe3a accept_with_residue, prose-only): (1) CUT -- the Measurement block above measured against 17124cc46 (EG.193's cut); this round's cut is b8f87205e: git diff --numstat b8f87205e a61eeb3ca = 4/3 a00-34601654 · 110/0 a00-4453045a · 22/12 a00-ff2a5bfc · 3/4 the hypothesis node -- node files only, 0 production, 0 test, so the ceiling reading holds over the right cut. (2) GATE -- the round asserted the hygiene gate without running it; run at a61eeb3ca: test_thought_hygiene.py 1 failed, 4 passed (test_the_real_corpus_has_no_node_with_two_thought_blocks: 8 offenders, one of them a00-ff2a5bfc -- a marker pasted in its Evidence repr); after this close's elision 7, none of them this chain's; the town trunk carries 14, so the red is pre-existing. (3) the repeated H1 and the second Agent Notes heading on this node are the goal:g7.33.19 row 24 writer habit; no sanctioned write.py verb removes a heading, so they stay recorded, not hand-edited.
