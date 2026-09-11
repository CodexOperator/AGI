---
id: experiment:a00-cbe6a356-00e291
mint_id: 42e2a03263ba4f4da6d3c469a08d40eb
type: experiment
parents:
  - hypothesis:l4-the-window-reply-and-harvest-or-cut-are-captive-steps
next_edges: []
confidence: 0.85
edited_by: a00-d7f4b9bf
evidence_runs:
  - experiment:a00-cbe6a356-00e291
loop: hypothesis:l4-the-window-reply-and-harvest-or-cut-are-captive-steps@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 978f9350d23c88c4
season: 2
title: "first-decision owner: the manifest join for loop/*@s2"
town: core
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# experiment:a00-cbe6a356-00e291

Parent: hypothesis:l4-the-window-reply-and-harvest-or-cut-are-captive-steps (the parent's
scope, step 4 of goal:g15.14: `first-decision --seat S` must pre-fill one harvest-or-cut row per
OPEN round of the seat's OWN worktree, never mis-credit another district's round).

## What I built — discriminator (b), the manifest join, in `_fd_rounds`

Kid 3 (a00-283598d5) had tried discriminator *(a)* — a round is the seat's iff it
*descends from the seat's current tip* (`git merge-base --is-ancestor <seat> <round>`)
— and measured 0 rows live. The parent's diagnosis: `dispatch.py`'s own docstring
(branch_worktree_for_spawn) says a round is cut from the SPAWNER's branch one layer
up, so a round forked at spawn is a descendant of an OLD seat commit, never of the
seat's current tip; after any seat merge the ancestry OWN-test fails for every round	of the seat ever spawned → 0 rows forever.

Replaced the ancestry OWN-test with the manifest join, evidence not convention:

1. `_fd_seat_worktree(root, main, seat)` — the seat worktree dir, resolved from
   config:seats `worktree` (the live `sanctuary-director` row names
   `.agi/worktrees/seat-sanctuary-director`), falling back to the convention
   `.agi/worktrees/seat-<S>` under `main` — mirrors `_fd_seat_branch`.
2. `_fd_seat_agent_ids(root, main, seat)` — the set of agent ids the seat ITSELF
   dispatched, parsed from `<wt>/.agi/sessions/iter-*/manifest.json` `agents[].id`
   (the seat's dispatch wrote these; READ-BEFORE-WRITE evidence, not a guess).
   Missing/unreadable manifests → empty set → under-count, never mis-attribution.
3. `_fd_agent_from_branch(branch)` — the `a00-<hex>` run before `@s<N>` in
   `loop/<slug>-a00-XXXXXXXX@s2`; '' when unresolvable.
4. `_fd_rounds` now drops a candidate unless `agent in own_ids`. A manifest-verified
   own round prints `parent: <seat_branch>`; an unresolvable/unowned round is never
   shown with a copied constant, and an agent-id that cannot be resolved would
   print `parent: ?` were it ever surfaced.

Call site updated: `rows = _fd_rounds(root, main, seat, seat_branch)`.

## Tests

Rewrote the `test_rotate_first_decision.py` fixture so the seat worktree lives AT the config-resolved
path (`.agi/worktrees/seat-sanctuary-director`) and the seat's iteration manifests are written/read back
as the manifest join does, then extended red-first:

- `test_manifest_join_owns_exactly_the_recorded_round` (NEW, proof bar 6): two rounds cut from the
  SAME seat branch (so ancestry (a) cannot tell them apart), only ONE recorded in the seat's manifest
  → exactly one row, correct parent; the un-recorded one never prints.
- `test_no_matching_manifest_yields_no_rows` (NEW, proof bar 7): an open round not in the seat's
  manifests → `no open rounds for this seat` — under-count, never a mis-credit.
- `test_sibseat_round_scoped_out_never_copying_seat_parent` (updated): the sibseat round is now cut
  with `manifest=False` (its agent lives in ITS OWN seat's manifests) → still exactly one own row, still no copied parent.
- `test_truncated_deferral` (the merge-falsifier) and the prefill tests still pass unchanged.

Result: `test_rotate_first_decision.py` 7 passed; all 248 `test_rotate*.py` neighbors + `test_bin_help_smoke.py` green.

## Falsifier on the REAL tree — reconciled, and why it is not 0-by-defect

`rotate.py first-decision --seat sanctuary-director` (fixed tool vs live root) prints
`first-decision: no open rounds for this seat`. This is the CORRECT live-state answer,
proven not the (a)-defect, by direct measurement of every `loop/*@s2` branch:

| agent | in seat manifest | ancestor of seat branch | ancestor of origin/season/s2 |
|---|---|---|---|
| a00-4218d47a | yes | **yes (closed)** | no |
| a00-8512520d | yes | **yes (closed)** | no |
| a00-25b3c7ba | yes | **yes (closed)** | no |
| a00-6c0bf498 | yes | **yes (closed)** | no |
| a00-d7f4b9bf (parent's own) | **no** | no (open) | yes |
| a00-0ce3c7fb (sensei's) | **no** | no (open) | yes |

The four seat-owned rounds the scope expected to see are already MERGED into the seat branch
(`--no-ff` makes their tips ancestors of the seat) — harvested since the parent's snapshot, which
measured openness vs `origin/season/s2` (origin simply has not caught up). A harvested round needs
no harvest-or-cut decision, so skipping it is correct. The parent's own round and sensei's round are
the genuinely-OPEN ones, and BOTH are excluded here precisely by the manifest join — the negative
half of the falsifier, verified live. The positive half (a manifest-owned OPEN round prints exactly
one row, correct parent) is proven hermetically in `test_manifest_join_owns_exactly_the_recorded_round`.

This 0-row live output is categorically different from (a)'s: (a) could NEVER show a round (its OWN-test
fails for every seat round after any merge); (b) shows a round the moment a manifest-owned round is open
— which, on the live seat today, none is.

## THOUGHT — why this version

The parent prescribed the manifest join; I implemented it without the reserve-out clause of the
ancestry test. Two judgement calls, both recorded: (1) an unowned/unresolvable round is DROPPED
otright, not printed with `parent: ?`, because the falsifier requires the parent's own round and
sensei's round NOT to print at all — the `?` is a documented fallback for a round that is surfaced
but unverifiable, never a licence to show a constant parent. (2) I kept the pre-existing OPEN gate
(`branch` not an ancestor of the seat branch) unchanged — it is the round's actionable state, and
the parent's defect was exclusively in the OWN-test, not the OPEN-test.

## Evidence

Live falsifier command + full output:
```
$ python3 .agi/worktrees/a00-d7f4b9bf/extensions/agi/bin/rotate.py first-decision \
      --seat sanctuary-director --root /home/ubuntu/work/agi/.agi
first-decision: no open rounds for this seat
```

Both foreign open rounds excluded (grep for the two forbidden branches in the full output → absent by
construction since the owned set is built from manifest ids). Hermetic proof of one-row correct-parent
display: `test_rotate_first_decision.py::test_manifest_join_owns_exactly_the_recorded_round` passes.

## Agent Notes
Implemented manifest-join discriminator (b) in first-decision: a round is the seat's iff its a00-<hex> branch agent appears in the seat worktree's own iter manifests agents[].id. Hermetic test proves one-manifest-owned-row/correct-parent; live tree excludes parent's and sensei's open rounds; seat-owned six are harvested (ancestor of seat) hence correctly closed.

REVIEWED by parent a00-d7f4b9bf: kid 4's manifest join is the correct discriminator and is live-consistent. I re-measured independently: the six manifest-owned rounds are all merged into seat/sanctuary-director@s2 (closed, correctly skipped); the two foreign OPEN rounds are correctly excluded. 7 tests pass. Verdict ACCEPTED as inconclusive_lean_proved:90 -- positive half is fixture-only because no seat-owned round is open live today. Kid 3's ancestry fix (a) is superseded: it could never show any round after a seat merge.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) WHAT THE INSTRUCTION SAID (parent brief, kid 4): "A round belongs to seat S iff an agent id parsed from the round branch name ... appears as an id in one of S's own iter manifests ... Drop the constant parent: ... Falsifier, measured on the real tree: first-decision --seat sanctuary-director must print rows for the six seat-owned open rounds above ... and must NOT print loop/hypothesis-l4-the-window-reply-a-a00-d7f4b9bf@s2 (the parent's own round) or loop/hypothesis-l4-rotate-self-drives-a00-0ce3c7fb@s2 (sensei-director's)."

(2) WHAT THE MACHINE ACTUALLY DOES: _fd_seat_worktree at rotate.py:5115, _fd_seat_agent_ids at :5138 (parses <seat-wt>/.agi/sessions/iter-*/manifest.json agents[].id), _fd_agent_from_branch at :5164, and the own_ids filter in _fd_rounds at :5212,5228-5229. Live: "first-decision: no open rounds for this seat". I verified that 0 is honest by checking each round directly: all six manifest-owned rounds (a00-4218d47a, a00-8512520d, a00-25b3c7ba, a00-6c0bf498, a00-221d5b56, a00-0360c2ad) are ANCESTORS of seat/sanctuary-director@s2 (now 9dde5563a) -- merged/closed since the parent's snapshot, which measured openness against origin/season/s2 (origin has not caught up). The two genuinely-OPEN foreign rounds -- mine (a00-d7f4b9bf) and sensei-director's (a00-0ce3c7fb) -- are excluded by the join. test_rotate_first_decision.py 7 passed.

(3) THE NEAR MISS: a join that matched the agent id ANYWHERE in the manifest text (grep) would credit rounds whose id appears incidentally, exactly my own first-pass method; the kid used the structured agents[].id, which is the right side of that line. And an implementation that swapped the ancestry test without KEEPING the pre-existing OPEN gate would print already-merged rounds as harvestable. The live 0 is the conjunction of both, and I separated them by measuring each round's ancestry rather than trusting the 0.

(4) DEVIATION FROM MY BRIEF: scope item 2 said print parent: ? for an unresolvable row; the kid instead DROPS unowned/unresolvable rounds. Justified and recorded by the kid: the brief's own falsifier requires the foreign rounds NOT to print at all, so ? is a documented-but-unreached fallback. I accept it -- dropping is stricter than the brief asked.

Verdict kept at the kid's inconclusive_lean_proved:90: the negative half of the falsifier is live-verified; the positive half (a manifest-owned round that is still open prints exactly one row with the right parent) is proven only hermetically in test_manifest_join_owns_exactly_the_recorded_round, because no manifest-owned round is open on the live tree today.
<!-- THOUGHT:END -->
