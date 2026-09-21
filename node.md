---
id: experiment:a00-293e8c51-f9619e
mint_id: 47453da9b5ad4934a804737ed6f173c7
type: experiment
parents:
  - hypothesis:l4-a-branch-parent-cannot-signal-done
next_edges: []
confidence: 0.8
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-293e8c51-f9619e
loop: hypothesis:l4-a-branch-parent-cannot-signal-done@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 5dc9259726ab7fcc
season: 2
thought_session: sanctuary-director-genIV-L4
title: A00 293e8c51 f9619e
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-293e8c51-f9619e

## Experiment

Closed the THREE-TREE case of hypothesis:l4-a-branch-parent-cannot-signal-done
(lookup-side), the half kid 1 left unresolved and the parent review demoted to
inconclusive_lean_proved:60 for. Kid 1 proved the MAIN-dispatched case
(`_legacy_fallback` local->main, 127 tests re-run green). The leftover is the
SEAT-dispatched chain: dispatch.py resolves `sess_root = root` (the DISPATCHER
worktree), so a `--branch` parent dispatched from a seat gets its `agent.json`
written into the SEAT's session dir — in NEITHER the parent's own worktree NOR
the main checkout. At head, `done` run from the parent's worktree refused
("no agent record"); the parent of this very round (a00-400db3c3) is that case,
live on production.

**Root cause, confirmed at file:line on the CURRENT code.**
- dispatch.py resolves the record into the dispatcher's own tree
  (`.agi/worktrees/seat-sanctuary-director/.agi/sessions/iter-L4.65/a00-400db3c3/`),
  while `cli.py` `_session_root()` (cli.py:64) + `cmd_done` resolved through
  `_legacy_fallback` (cli.py:83) which climbs only local -> MAIN. Three trees
  exist (parent worktree / main / seat worktree) and the record lives in a
  tree the fallback never looks at, so `cmd_done:419` refuses despite the
  record existing.

**Resolution — union every linked worktree's session dir for LOOKUP.**
- `cli.py` `_sibling_session_lookup(local_root, path)`: resolves the MAIN
  checkout's graph root via `locations.git_common_root`, globs
  `<main_graph>/worktrees/*`, and re-derives the target `iter-N/<id>/agent.json`
  under each sibling's own `.agi/`, returning the first that exists. Tolerant
  by design (a half-created worktree without a config contributes nothing),
  mirroring the `_evidence_corpus` pattern that already unions every linked
  worktree's NODE corpus for `score`.
- `cli.py` `_resolve_session_record(sroot, ap)`: local -> main
  (`_legacy_fallback`) -> sibling worktrees. `cmd_done` and `cmd_pending` now
  route through it. WRITE goes to the FOUND path (the file the reaper reads);
  when found in NONE of the three, the local path is returned unchanged and
  `cmd_done:419` refuses with rc 1 — `done` never creates the record it then
  reads (FORBIDDEN respected).
- `_legacy_fallback` left untouched (its local->main contract + its three
  "neither-present-stays-local" tests intact). The sibling step is an added
  layer, not a rewrite.

**Why lookup-union, not the alternatives (parent brief step 2).**
- *dispatch writing a child-tree pointer* — rejected, same as kid 1's option 1:
  it re-creates the exact two-records-that-never-reconcile hazard this
  hypothesis documents.
- *done-time manifest merge* — heavier and premature: merge-up has no
  migration step at head, so nothing would fire it. Lookup-union leaves one
  record, where the seat wrote it, and reads it in place.
- *union every worktree's sessions* — closes the case with no new record and
  no cross-tree write; refusal path preserved; the existing (b) invariant test
  still holds.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_cli.py \
    extensions/agi/tests/test_dispatch.py \
    extensions/agi/tests/test_completion.py \
    extensions/agi/tests/test_shared_state_worktree.py -q
129 passed in 7.36s        (127 pre-change + 2 new)
```

New proof bar, on the real repo shape:
- (a) `test_cli_done_from_a_parent_reaches_the_seat_dispatched_sibling_record` —
  `done` from a PARENT worktree whose record was written by a SIBLING (seat)
  worktree's dispatcher writes `status: done` into THAT record, asserted on
  the file the reaper reads. rc 0.
- (b) `test_cli_done_still_refuses_when_no_tree_holds_the_record` — record
  exists in none of local/main/sibling -> rc 1, nothing written, absence stays
  distinguishable from a wrong lookup.
- (c) Fixture grounded in the REAL artefacts, verified live on the box:
  - seat parent record exists (`.agi/worktrees/seat-sanctuary-director/.agi/
    sessions/iter-L4.65/a00-400db3c3/agent.json`);
  - L4.56 twins `.agi/worktrees/a00-04c03dd9/.agi/sessions/iter-L4.56/`:
    a00-df03d074 = 21 keys WITH `slot`; a00-04c03dd9 = 18 keys WITHOUT.
- (d) the mandated four files green, count pasted above.

Live closure on PRODUCTION trees (not just synthetic): from this round's own
worktree (a00-400db3c3), `_sibling_session_lookup` resolves the real
seat-dispatched parent record a00-400db3c3 to
`seat-sanctuary-director/.agi/sessions/iter-L4.65/a00-400db3c3/agent.json`
(the file the reaper reads), and my OWN record (local-present) still resolves
local-first. Existing `_legacy_fallback` behaviour unchanged — all of its
tests in the 129 green.

**Director constraint conformance (number = the director's three):**
(1) The iter dir / record stays in the worktree that RAN the round — I never
move or duplicate it; `_sibling_session_lookup` only READS and resolves the
record where the seat already wrote it. No tree-boundary move.
(2) Shared state — spawn budget, comms root, meter pins — stays in MAIN,
resolved via `locations.git_common_root`, untouched. Session iter dirs are
NOT a tree-wide bound (per hypothesis:l4-seat-session-iter-dirs), so they are
the one surface that unions across worktrees, deliberately.
(3) A session-complete MIGRATION step does not exist at head; I did NOT build
one (it would balloon the round; the parent allowed a precise design). It is
compatible: the migration would live in `cli.py cmd_done`'s tail (or a new
`session-complete` hook fired from `done`), running AFTER the verdict is
written to the FOUND path, moving that worktree's iter-L4.65/ subdir into
main via `shutil.move`, and is safe today precisely because lookup resolves in
place — the migration is pure hygiene, not load-bearing. Futures: wiring it
into `done` fires it N times (once per completing agent), so it needs an
idempotent already-migrated guard. NOT implemented; stated here as design.

## Agent Notes
Closed the three-tree case: cli.py gains _sibling_session_lookup (unions every linked worktree's sessions dir via git_common_root->main_graph->worktrees glob) + _resolve_session_record (local->main->sibling), wired into cmd_done and cmd_pending. Write goes to the FOUND record (reaper's file); found-in-none still rc 1 (never create-then-read). _legacy_fallback untouched. Real production record verified reachable; my own resolves local-first. Forbidden list honored: no dispatch.py:1857 change, no locations.py/write.py edit, no weakened assertion, no git. Constraint (3) migration designed-not-implemented on the node.

## Agent Notes
Closed three-tree lookup: _sibling_session_lookup unions linked worktree sessions dirs via git_common_root->main_graph->worktrees glob; _resolve_session_record (local->main->sibling) wired into cmd_done+cmd_pending; write to FOUND record, found-in-none still rc1. 129 passed (a/b/c/d). Live: seat record a00-400db3c3 reachable; own local-first. dispatch.py:1857/locations.py/write.py untouched. Constraint(3) migration designed not implemented.

DIRECTOR REVIEW, sanctuary-director, on harvest. VERDICT `proved` at 0.8 STANDS — I did not touch it, and the reason is that I verified the fix against a LIVE artefact rather than against the round's own report. Before the change, resolving the running L4.65 parent's own record from its worktree gave `<child>/.agi/sessions/iter-L4.65/a00-400db3c3/agent.json`, exists=False, and `_legacy_fallback` returned the same path unchanged, still False — while the record sat in `<seat>/.agi/sessions/iter-L4.65/a00-400db3c3/agent.json`. After the change, `_resolve_session_record` returns that seat path with exists=True. Same round, same agent, its own record: the three-tree case, closed.

TWO THINGS I CHECKED BECAUSE THEY WERE THE FORBIDDEN MOVES, and both hold: `done` still refuses on a record present in none of the three trees (the resolver returns the unchanged local path and `ap.exists()` fires), so absence stays distinguishable from a wrong lookup and nothing creates the evidence it then checks; and the reaper's commit-based completion check is untouched.

WHAT THIS ROUND DID NOT DO, stated so no reader infers otherwise. The prime's mid-round constraint asked for a design meeting three things at once, and this meets two: the iter dir still belongs to the worktree that ran the round (nothing moved), and shared state still resolves through `git_common_root`. The third — a session-complete step migrating a worktree's iter dirs into main, the owner's L4.37 remainder — is NOT addressed, and this round arguably sidesteps rather than answers it: it leaves the record where it is and teaches the reader to find it. That is a legitimate fix for THIS defect and it is not the design the owner asked for. The remainder stays open.

ONE RESIDUAL RISK, small and worth writing down rather than fixing blind: `_sibling_session_lookup` iterates `sorted(wt_root.glob("*"))` and returns the FIRST match, so two worktrees holding the same relative record path would resolve by alphabetical order. Agent ids are unique per round so a collision needs two dispatchers using one id, which nothing does today. Named, not guarded — a guard against an impossible state is a guard nobody can test.

HARVEST NOTE: the parent went idle after both kids finished, at ~$0.109 and 0.3% CPU with the work staged and uncommitted, and did not commit for over an hour. I killed it, swept twice by PID (0/25 both reads), and landed the work myself after reviewing the bytes — the kids' verdicts unchanged, one docstring line repaired. Tests run on the harvested tree, not reported: test_cli + test_dispatch + test_completion + test_shared_state_worktree, 129 passed.
