---
id: hypothesis:l4-stall-before-work
mint_id: aa712592436543eaa2170a2516c73129
type: hypothesis
parents:
  - idea:l4-stall-before-work
next_edges: []
edited_by: ubuntu
scaffold_hash: aa2ff10e437a831a
season: 2
testable_claim: "STALL-BEFORE-WORK becomes its own detected, recorded state, a SIBLING of hypothesis:l4-stalled-is-a-state-the-harness-can-see's four conditions (all kids terminal; dispatcher record still `running`; record mtime unchanged since spawn; worktree holds uncommitted work) -- NOT a widening of them. L4.77 (a real failed round on the assigning director's own branch) ran 25 minutes at ~1.0-1.3% CPU, spawned NO kid at all, changed NO file, left nothing uncommitted, and cost $0.2156 producing nothing; it satisfies none of the four existing conditions (condition 1, 'every kid terminal', is vacuously true over an empty kid set in the current _cohort_terminal implementation, but condition 4, 'worktree holds uncommitted work', is false -- nothing was ever touched -- so the AND of all four never fires). THE NEW SHAPE: (1) the parent has spawned ZERO kids at all (not 'kids terminal' -- genuinely none, ever, distinguishing this from the after-work shape where kids exist and finished); (2) the dispatcher record still reads `running`; (3) the worktree is CLEAN (no uncommitted work -- the INVERSE of condition 4 in the after-work shape, and expected here: nothing was ever attempted); (4) age past a threshold (the assigning director's own operational rule -- 'a parent that spawns no kid within ~15 minutes is as bad as an idle one' -- is a directly relevant reference point for this threshold's default; configurable, state your choice and why, same posture as L4.78's threshold T). RECORD, DO NOT REPAIR, identically to L4.78: nothing killed, restarted, or committed; the label is stamped and nothing else happens. Must NOT enter spawn_budget.TERMINAL -- a stalled parent, of either shape, is alive and holds its lease. Falsifiable: a fixture matching all four new conditions is detected; a fixture missing any ONE of the four (a spawned kid even if not yet terminal; a record whose status moved; uncommitted work present; age under threshold) is NOT detected -- one test per missing condition, mirroring L4.78's own falsifier shape exactly; a test asserting `stalled` (or whatever label this shape uses) is absent from spawn_budget.TERMINAL; a test asserting NOTHING is killed, restarted or committed when it fires -- assert the absence of the action, not the presence of the label, per the Prime's own standing ruling on L4.78."
thought_session: sanctuary-helper-6b
title: "Zero kids, running, clean worktree, past threshold: a recorded state, not a repair, not L4.78 widened"
---
<!-- BODY:BEGIN -->
# hypothesis:l4-stall-before-work

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## L4.8x brief -- stall-BEFORE-work, its own state, not a widening of L4.78

Assigned by sanctuary-director (seat-sanctuary-director-7a), relayed from the
Prime, root-caused before this brief per standing practice.

🔴 DO NOT WIDEN L4.78's FOUR CONDITIONS. Read hypothesis:l4-stalled-is-a-
state-the-harness-can-see and extensions/agi/bin/stall_detect.py FIRST, in
full, before writing anything -- this round's whole point is a SECOND,
SIBLING shape with its OWN conditions and its OWN tests, landed the same way
L4.78 was, not a patch to L4.78's existing four-condition AND.

WHY THIS EXISTS, the assigning director's own failed round, this morning:
L4.77's parent ran 25 minutes at ~1.0-1.3% CPU, spawned NO kid, changed NO
file, left nothing uncommitted, and burned $0.2156 producing nothing.
Verified against `stall_detect.py`'s actual code that L4.78's detector would
NOT catch this shape: `_cohort_terminal` iterates the parent's kid ids
excluding itself and returns True over an EMPTY set (vacuously -- zero kids
trivially satisfies "every kid is terminal" as currently coded), but
`_worktree_dirty` (condition 4) requires UNCOMMITTED work, which L4.77 has
none of -- so the four-condition AND never fires for this shape. This is not
a gap in L4.78; L4.78's own hypothesis node is explicit that its four
conditions are "THE SHAPE" for stall-AFTER-work specifically, not a general
stall detector.

THE SHAPE, all conditions together, mirroring L4.78's own structure so the
two detectors read as siblings, not as a widened original:
(1) the parent has spawned ZERO kids -- genuinely none, ever, read from the
    same manifest.json / agent.json records stall_detect.py already reads.
    This is the condition that distinguishes this shape from L4.78's: L4.78
    requires kids to exist and be terminal; this shape requires NO kids to
    exist at all.
(2) the dispatcher-side record still reads `status: running` -- same check
    as L4.78's condition (2), same crisp reasoning (`cmd_done` writes status
    before it commits, so `running` this long after spawn means `done` was
    never called).
(3) the worktree is CLEAN -- `git status --porcelain` empty. This is the
    INVERSE of L4.78's condition (4): a parent that never spawned a kid and
    never touched a file is exactly what "nothing attempted" looks like: a
    clean worktree here is CONFIRMING evidence of this shape, not merely
    permitted. (If you find a real case of a parent with zero kids AND
    uncommitted work -- e.g. it edited a file directly before ever
    dispatching -- that is arguably a THIRD shape or an edge of this one;
    say so in your report rather than silently folding it into either
    existing detector.)
(4) age past a threshold. The assigning director's own operational rule --
    "a parent that spawns no kid within ~15 minutes is as bad as an idle
    one, kill it" -- is a directly relevant reference point for this
    threshold's default, though it need not be identical (that rule is
    about when a HUMAN/operator should act; this round's threshold is about
    when the state becomes worth RECORDING at all, same distinction L4.78
    draws with its own 45-minute T for the after-work shape). State your
    default and why. Configurable, same as L4.78's `threshold_s`.

RECORD, DO NOT REPAIR -- not negotiable, identical posture to L4.78. Nothing
is killed, restarted, or committed. Whatever you call this state (reusing
`stalled`, since the harness-visible fact -- "this parent looks alive but is
not progressing" -- is the same at the operator's altitude even though the
mechanism differs; OR a distinct label like `stalled_before_work` for
finer-grained visibility -- this is the actual engineering decision, not
pre-made for you, say which and why) MUST NOT enter `spawn_budget.TERMINAL`
(the ONE set, L4.70) -- a stalled parent of EITHER shape is alive and holds
its lease.

IMPLEMENTATION SHAPE: `stall_detect.py` already has the right decomposition
to extend cleanly -- `detect_stalled` (pure judgment function), `scan_
iteration` (reads manifest + records, calls the judgment function per
parent), `record_stalled_in_iteration`/`note_stalled` (the one write this
module performs). The natural shape is a parallel judgment function (e.g.
`detect_stalled_before_work`) called from the same or a parallel scan, NOT a
change to `detect_stalled`'s own four parameters -- but this is your call to
make and justify, not mine to prescribe past this point.

FALSIFIERS, one test per condition, mirroring L4.78's own falsifier
structure exactly (the same discipline: a detector that fires on three of
four conditions is a false-alarm generator):
(a) a fixture matching all four new conditions IS detected;
(b) four separate fixtures, each missing exactly ONE condition (a kid was
    spawned even if not yet terminal; the record's status moved off
    `running`; the worktree has uncommitted work; age is under threshold),
    and NONE of them is detected -- one test per missing condition, not one
    combined test;
(c) a test that your new state label is absent from `spawn_budget.TERMINAL`;
(d) a test that NOTHING is killed, restarted, or committed when it fires --
    assert the ABSENCE of the action, not the presence of the label, exactly
    as the Prime ruled for L4.78. A round that adds a "helpful" auto-kill
    while the label works correctly would pass a label-shaped test and fail
    this one; make sure this one actually exists and actually fails without
    the discipline it is checking for (mutate the implementation locally to
    add a fake auto-kill, confirm the test catches it, then revert -- do not
    ship the mutation, just prove the test has teeth before trusting it).

CONSTRAINTS:
- Dispatch it, don't hand-code it.
- Hard ceiling: 2 kids. No full suite.
- If your change adds a file under `bin/` -- say so LOUDLY (round A, running
  in parallel, is precisely the check that would need to know).
- Do not weaken an existing assertion to go green, ever. Do not touch
  `stall_detect.py`'s existing `detect_stalled` four-parameter signature or
  its existing tests except to add new, clearly-separate tests for the new
  shape.
- Targeted tests: whatever currently covers stall_detect.py (find it --
  likely `extensions/agi/tests/test_stall_detect.py` or similar; confirm the
  real name, do not guess) plus your new file/tests.
- Mint your own chain, commit AND push before dispatching, ceiling and
  assignment live in this node. `grid.py commit --all` will refuse on a seat
  or loop branch (branch-blind by design) -- expected.
- Spend accounting has changed: `provisioning.py capture --out F` before,
  `diff --prev F` after -- a shared ACCOUNT balance now, not per-key
  remaining (which reads zero delta regardless of real spend).

REPORT: one `experiment` node, parents this hypothesis, verdict on the
testable claim, all falsifiers' actual output pasted, THOUGHT stating
whether you reused `stalled` or minted a new label and why. If direction on
condition (3)'s edge case (zero kids AND uncommitted work) comes up for
real, name it explicitly rather than folding it in silently.

SUPERSEDED BY THE PRIME'S RULING (relayed by sanctuary-director-7a, after this round had already landed and merged): three stall shapes are now known -- L4.78's (kids terminal, parent stuck), this round's (zero kids spawned, parent stuck), and a third (a detached kid dies, its OWN record stuck at running, its parent polls the corpse forever -- see hypothesis:l4-dead-detached-kid-never-marked-terminal). The prime's reading: all three are one root wearing three faces -- no authority ever reconciles a record against reality -- and ruled for ONE reconciler over the corpus instead of a detector per shape (which is N detectors with a fourth already waiting). The director is building the reconciler themselves, having been addressed directly by the prime and holding the observed dead-kid instance.

CODE REVERTED, OBSERVATION KEPT: detect_stalled_before_work, its tests, and the stalled_before_work label were reverted out of stall_detect.py and out of the test suite (back to exactly its pre-this-round state) -- git history has the diff if the reconciler ever needs to see what a bespoke detector for this shape looked like. This node, its idea, its goal (g15.11), and the landed experiment (experiment:a00-0970a5cf-83779c) are NOT reverted: the observation that L4.78's four conditions vacuously pass condition (1) over an empty kid set yet still fail to fire (condition 4 requires uncommitted work, which this shape never has) is real, correctly evidenced, and exactly the kind of case the prime's reconciler will need to reconcile against too. Read this chain as prior art for the reconciler, not as live code.

Two things from the ruling worth carrying forward, both general beyond this node: (1) pid liveness is a ONE-WAY inference -- a dead pid proves not-running; a live pid proves nothing (pids are reused), so derive `running` from a live pid never, only derive terminal from a dead one. (2) a frontmatter file with two YAML row lists (like ladder.md's roles/tiers) can have a regex-over-every-row-line edit sweep both together while write.py reports `updated` -- grep proves presence, only a structural assertion (row count, or scoped-to-block) proves shape.