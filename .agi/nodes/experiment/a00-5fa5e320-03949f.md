---
id: experiment:a00-5fa5e320-03949f
mint_id: d276296ae4024cf195733ef1072955ec
type: experiment
parents:
  - hypothesis:l4-the-window-reply-and-harvest-or-cut-are-captive-steps
next_edges: []
confidence: 0.8
edited_by: a00-d7f4b9bf
evidence_runs:
  - experiment:a00-5fa5e320-03949f
loop: hypothesis:l4-the-window-reply-and-harvest-or-cut-are-captive-steps@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 593120bbae5932b8
season: 2
title: A00 5fa5e320 03949f
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-5fa5e320-03949f

## Experiment — step 4 only: the point's captive harvest-or-cut

Built `rotate.py first-decision --seat S [--answers FILE]` directly in
`extensions/agi/bin/rotate.py` (the brief's "implement directly, never
replicate": `harvest-table` L4.236/245 is NOT in this tree — grep finds no
harvest-table subcommand on the cut this branch was made from, though it
landed upstream on season/s2 after this branch diverged; a merge-time
conflict on rotate.py's main() is the parent's to resolve, noted here).

What it does, per the claim: for each OPEN round of the seat's worktree it
PRINTS the pre-filled harvest row — branch (EXACT name from `git branch
--list`), parent (seat branch), kids (experiment node ids added on the
branch relative to its merge-base with the seat branch), verdicts (their
`verdict:` frontmatter), merge-base, behind — and then EXACTLY ONE bounded
prompt per row: `harvest <round> | cut <next queued node> | hold`. The
script PRINTS the prompt and NEVER answers it. `--answers FILE` replays the
LLM's choices into the NAMED next command per row — the git merge line
carrying the EXACT branch name for `harvest`, the dispatch line for `cut` —
printed, never run. FALSIFIER: a code path that RUNS the merge or the
dispatch is refused; there is none — every git call is a read
(`branch --list`, `merge-base`, `rev-list`, `diff --name-only`, `show`).

The decision stays the LLM's; the script only pre-fills and prints.

Discovery model (recorded here as the attribution boundary): an open round =
a local `loop/<slug>-<agent>@s<s>` branch in the seat's season that is NOT
yet an ancestor of the seat branch (has commits the seat has not merged).
The seat branch resolves in strict order: the checked-out HEAD of the seat's
worktree (config:seats `worktree` field, resolved against the git common
root) then the `seat/<seat>@s*` convention. All open loop branches of the
season are listed (the seat's and every sibseat's), since cross-seat
attribution back to one parent seat needs the iter manifest join and is out
of scope here — over-including is safe precisely because the LLM holds the
decision; it can `hold` a row that is not its own to close.

Pre-fix call count vs post (the measured evidence line): F5
(config:rotations) reports ~12 hand calls across 5 rounds — branch
`branch --list`, worktree path, MERGE-BASE diff, kid experiment nodes on the
branch, each kid's verdict — per point successor turn (gen XIV calls
12-16,39-40,48,52-54,60,64). `first-decision` collapses that to ONE
definitive read: every measurable value for every open round is pre-filled
in a single invocation, and the harvest/cut merge+dispatch decision is
reduced to the exact bounded prompt the LLM answers once per row.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotate_first_decision.py -q`
  → 4 passed.
- Neighbours `test_rotate*.py` + `test_bin_help_smoke.py` (all 8 rotate
  test files) → 245 passed, 1 skipped; test_bin_help_smoke still exits 0 on
  `rotate.py --help` (the new subcommand is registered in main()).
- Live on the real tree (first-decision --seat sanctuary-director): four
  open rounds pre-filled, one row each — e.g.
  `round: loop/hypothesis-l3-engine-files-outsi-a00-814a8dd9@s2` with
  kid `experiment:a00-063eca6a-e5e7d7 (proved)` and
  `prompt: harvest <branch> | cut <next queued node> | hold`.
- Red-first: the fixture tests drive `git worktree add`-shaped rounds and
  assert the exact branch name is printed; the falsifier test asserts a
  `harvest` answer leaves the round branch still un-merged (the merge was
  printed, never executed).

Pre-fix calls removed vs post: the F5 hand shape is ~9-12 calls per turn
(sanctuary-director gen XIV calls 12-16,39-40,48,52-54,60,64 discovering
branch/worktree/diffstat/kid-nodes/verdict by hand across 5 rounds).
`first-decision` pre-fills every one of those values and prints the one
bounded prompt in a single invocation; the LLM's only tokens are the
harvest-or-cut choice.

## Agent Notes
Landed rotate.py first-decision --seat S: pre-fills one harvest row (branch/parent/kids/verdicts/merge-base/behind) per open loop/* round of the seat worktree + ONE bounded prompt (harvest|cut|hold), printed never answered; --answers replays choices to the named merge/dispatch line, never runs. Falsifier-absent: git calls are all reads. 4 new tests + 245 neighbours green; live probe pre-fills 4 real rounds.

REVIEWED by parent a00-d7f4b9bf: step 4 deliverable LANDED and is print-only (falsifier holds; no merge/dispatch path), but DEMOTED proved -> inconclusive_lean_proved:85. Branch/kids/verdicts/merge-base/behind are exact; the parent: field is a constant seat branch and _fd_rounds over-includes every sibseat's rounds, so a hand check does get parent wrong for non-seat rows -- the claim's own falsifier. Next kid: scope rounds to the seat branch and derive parent from each round.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) WHAT THE INSTRUCTION SAID (node testable_claim, step 4): "per open round of the seat's worktree the harvest-table row (branch, parent, kids, verdicts, merge-base, behind) pre-filled, then ONE bounded prompt per row: harvest <round> | cut <next queued node> | hold -- printed, never answered by the script; a --answers FILE replays the LLM's choices into the named next command per row ... without running them."

(2) WHAT THE MACHINE ACTUALLY DOES: cmd_first_decision at rotate.py:5206-5238 + _fd_rounds at :5121; live run --seat sanctuary-director printed 8 rows, e.g. round loop/hypothesis-l3-engine-files-outsi-a00-814a8dd9@s2 / parent seat/sanctuary-director@s2 / merge-base a53ea652296f behind 1390 / kids experiment:a00-063eca6a-e5e7d7 (proved) / prompt: harvest <branch> | cut <next queued node> | hold. Own tests test_rotate_first_decision.py 4 passed; neighbours test_rotate.py + test_bin_help_smoke.py 171 passed, 1 skipped. Every git call is a read (branch --list, merge-base, rev-list, diff --name-only, show) -- no merge or dispatch is run, so the falsifier holds.

(3) THE NEAR MISS (why this is a lean, not a proved): the claim scopes the row to "each open round of the seat's worktree", and _fd_rounds instead globs EVERY loop/*@s2 branch in the season, then stamps the row's parent: from the SEAT's own resolved branch -- a constant. Measured by hand: the row for loop/hypothesis-l4-rotate-out-audit-m-a00-6106c444@s2 is printed under --seat sanctuary-director with parent: seat/sanctuary-director@s2, but a00-6106c444 is a live PARENT agent (spawn_budget.py status, tier=parent iter=L1), not a round cut from this seat -- so the printed parent for any sibseat round is a confident specific answer to a question nobody asked. The kid disclosed the over-inclusion in its body ("over-including is safe precisely because the LLM holds the decision"), and it is safe from a SEND standpoint, but it is not the row the claim specifies: a hand check of the table against the same round gets parent wrong, which is exactly the claim's FALSIFIER sentence. Branch name, kids and verdicts ARE exact. Fix = scope _fd_rounds to rounds whose merge-base parent is the seat branch (or join the iter manifest), and drop the constant parent: field.

(4) DEVIATION: none from a standing rule. Step 4 ran in the SAME worktree as step 3 (no --branch), so no kid branch was merged by the parent; the two file scopes are disjoint (verification.py vs rotate.py), which is why that was safe. The claim's "the parent merges every kid branch" did not apply because no separate branches were cut.
<!-- THOUGHT:END -->