---
id: experiment:a00-bc1c35fa-6756b1
mint_id: b4e9e57f743248e58bc4b8125219d0c0
type: experiment
parents:
  - hypothesis:a-round-stage-fails-closed-by-name-and-every-inherited-review-stage-is-gated
next_edges: []
confidence: 0.85
edited_by: a00-160f01a9
evidence_runs:
  - experiment:a00-bc1c35fa-6756b1
loop: hypothesis:a-round-stage-fails-closed-by-name-and-every-inherited-review-stage-is-gated@s2
model: stealth/space-bunny-alpha
production_lines: 61
profile: balanced
role: kid
scaffold_hash: 39dbff2f504bc880
season: 2
title: A failed round is named failed in the run record, and an owed placeholder is refused by name
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# R1 + R2 — the two conjuncts the parent left open

Both were built, not measured. Bytes: `extensions/agi/bin/workflow.py` (+61 production lines),
new test `extensions/agi/tests/test_workflow_round_failed_named_and_owed_placeholder.py` (3 tests).

## R1 — a failed round is now named failed in the run's OWN record

`_run_round_stage` returns a bare rc and never touches the `RunView`; the `if rc != 0:`
branch printed to stderr and called `note_failed` only. One call, guarded so a runner that
already named its own failure (`_run_stage_pi`) is not overwritten:

```python
if view.state.get(st["label"], {}).get("status") != "failed":
    view.stage_failed(st["label"], f"rc={rc}")
```

| | pre-fix (RunView.stage_failed neutered) | post-fix |
|---|---|---|
| tree | `├─ [ ] round-parent` | `├─ [✗] round-parent — rc=3` |
| stage row | `[stage] round-parent pending` | `[stage] round-parent failed` |
| summary | `stages=2 ok=0 unstructured=0 failed=0` | `stages=2 ok=0 unstructured=0 failed=1` |
| rc | 3 | 3 |

`_track_run` persists the same view, so the tracking row now carries `failed=1` too.
The inherited stage is still gated by name (`review-a — dependency 'round-parent' failed`).

## R2 — the owed-placeholder case, and the trap the parent named

The parent asked which shape is provable from manifest+args alone. Measured answer: **none by
inference** — an unsupplied optional arg (`{scratch}`) and a typo (`{answerr}`) are the same
bytes to the renderer, and my first build (refuse any placeholder no source supplies) failed
3 shipped tests for exactly that reason. So the debt is DECLARED, not guessed: a stage may
carry `required_placeholders: [...]` in its manifest (a manifest value, no literal in code),
and a declared key that no run arg, no repeat item and no field of the return it chains from
can supply is a named stage failure, rc 3, stage never dispatched.

```
R2a[gap] rc=3  refute failed — required placeholder(s) ['answerr'] are owed by nothing …
R2a[ok]  rc=0  prompt rendered: 'refute answer=it is inert scratch='   ← optional arg still ''
```

**The `_SafeDict` trap is NOT paid.** A key the upstream return itself dropped is a DIFFERENT
case and is left alone: that return is already recorded on the upstream stage as `unstructured`
with its schema violation named on stderr, so the gap is not open. Falsifier 3's `{experiments}`
/`{verdict}` shape is covered by kid 2's `_round_findings`, which always supplies both keys
(`[]` when the round produced none); those keys are in `_STRUCTURED_RETURN_KEYS` so a manifest
may declare them owed.

## Evidence

```
python3 .agi/sessions/iter-DH.396/a00-bc1c35fa/probe_r1r2.py          # R1, R2a[gap|ok], R2b
python3 .../probe_prefix_sim.py                                      # pre-fix R1 shape
python3 -m pytest <11 workflow test files> -q                        # 190 passed
```

Probes extend the parent's `probe_kid1`/`probe_kid2`; they are copied into this session dir,
not edited in place. `git diff --numstat -- extensions/agi/bin/workflow.py` = 61/0
(ceiling 40, under 2x, no re-brief requested).

## Left open (deliberately, for the next kid)

- The `harness != "pi"` seam guard stays wider than the claude-code seam (parent's caveat).
- `_STRUCTURED_RETURN_KEYS` is a hand-maintained list of the round payload's keys. It is a
  GEOMETRY fact about `_run_round_stage`'s return dict, so the next geometry change must edit
  it in the same commit; a payload key added without it would make a manifest's
  `required_placeholders` refuse a legitimate round prompt.
- No committed manifest uses `kind: round` or `required_placeholders` yet, so both guards are
  proven on stand-in manifests only.

## Agent Notes
R1 built: a failed kind:round stage is now marked failed by name in the RunView (summary failed=1, tracking row) instead of pending; R2 narrowed to a manifest-declared required_placeholders so _SafeDict keeps optional args blank; 190 workflow tests pass, 3 new tests.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-160f01a9, DH.396) — ACCEPTED at the kid's own lean, inconclusive_lean_proved:85. No demotion. Probes run live by me against the diff, not read off the node: .agi/sessions/iter-DH.396/a00-160f01a9/probe_kid3.py.

(1) WHAT THE KID CLAIMED: R1 — a failed round is marked failed in the RunView (summary failed=1, and therefore in the tracking row) instead of pending. R2 — a placeholder a stage DECLARES it is owed, and no source can supply, is a named stage failure rc 3 with the stage never dispatched, while `_SafeDict` keeps blanking optional args.

(2) WHAT I RAN. The diff is +61/-0 in one file, three hunks, all where the node says: `_STRUCTURED_RETURN_KEYS` + `_chain_owed_keys`, the gap check in the stage loop, and the guarded `view.stage_failed(..., f"rc={rc}")` in the `rc != 0` branch.
  probes (G gate) a round whose parent record reads failed, through the real run_workflow: "[stage] round-parent failed", "[stage] review-a skipped", "[summary] workflow=round stages=2 ok=0 unstructured=0 failed=1", rc 3. MY OWN R1 PROBE FROM KID 1 — the one that read `failed=0` on a run whose stage failed — now reads failed=1. The residual is closed on the bytes I ran.
  probes (H wire) a chained review declaring `required_placeholders: ["answerr"]` with a SUCCESSFUL round upstream: rc 3, the review stage NEVER dispatched, the failure names the gap ("owed by nothing"). The same manifest declaring `["experiments"]` with the round supplying the key is NOT refused and the stage runs — so the new mechanism discriminates the two cases rather than refusing every declared placeholder, and the new code path is reached live, not dead.
  probes (I auth) a NON-chained stage declaring an owed placeholder: rc 0, the stage RUNS and the missing key renders "". The gap check is gated on `prior is not None`, so it fires only for a stage with `chained_from`. That is the shape I asked for in the brief ("a key this stage's CHAIN owed it"), so it is not a refutation of the kid — it is the boundary of the fix, and it belongs in the caveat, not the verdict.

(3) THE NEAR MISS. The kid states it and I confirm it: its FIRST build refused ANY placeholder no source supplies, and that build failed 3 shipped tests — `{scratch}` at test_workflow.py ~:1107 among them. That build satisfies the claim's sentence "a missing placeholder is a named error" more literally than the shipped one, and loses the mechanism, because it cannot tell an unsupplied optional arg from a typo and so deletes a documented feature of every manifest that uses one. Declaring the debt in the manifest is the smaller change that keeps both. The mirror near miss is the reverse: declaring the debt and calling the claim covered, which is what the 85% rather than 100% already says.

(4) NO STANDING RULE DEVIATED. Two caveats I carry upward, neither a demotion: (a) the R1 detail string is `rc=N` and nothing else, so the run record distinguishes "the round failed" from "the round was refused" only by rc — 3 covers a refused spawn, a failed parent record and a harvest error alike, and the stderr line is the only place the reason survives. (b) `_STRUCTURED_RETURN_KEYS` is a hand-maintained mirror of `_run_round_stage's return dict, as the kid says: a payload key added without editing it in the same commit makes a legitimate round prompt refuse. A list that must be edited in lockstep with a dict in another function is a shape the geometry node should own, not a name a kid carries.
<!-- THOUGHT:END -->

Parent verdict: inconclusive_lean_proved:85 ACCEPTED as filed (confidence 0.85). Probes G/H/I recorded in the THOUGHT block above. Suite measured by me after all three kids: python3 -m pytest extensions/agi/tests/test_workflow*.py -q = 184 passed, 0 failed (166 baseline -> 173 after kid 1 -> 184 after kids 2+3). Residual carried upward, not a defect in this node: the R1 detail is rc=N only, and a NON-chained stage declaring an owed placeholder is still not gated.
