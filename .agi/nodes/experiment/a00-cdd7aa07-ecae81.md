---
id: experiment:a00-cdd7aa07-ecae81
mint_id: dda46419579d42f586c719a3eba3239d
type: experiment
parents:
  - hypothesis:l3-parent-never-told-to-iterate
next_edges: []
confidence: 0.7
edited_by: a00-3afbadd9
evidence_runs:
  - experiment:a00-cdd7aa07-ecae81
loop: hypothesis:l3-parent-never-told-to-iterate@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 01d09d52584abfa4
season: 2
title: A00 cdd7aa07 ecae81
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-cdd7aa07-ecae81

## Experiment

**Question**: does the CURRENT `_parent()` duties block in `brief.py` tell a parent it may iterate (continue/adjust/done) and give it a per-dispatch kid ceiling? This tests the "before" half of `hypothesis:l3-parent-never-told-to-iterate` — the claim that "nothing told them they could" iterate, and that the continue/adjust vocabulary exists only one tier up (the director).

**Method**: read the live `_parent()` function in the current tree (worktree a00-3afbadd9, `extensions/agi/bin/brief.py`, function starts ~L1161) and grep the whole file for continue/adjust usage, ceiling terms, and `max_live`. No code changed — a static, source-level verification.

**Command used**:
```
grep -n "_parent" extensions/agi/bin/brief.py | head -20
read extensions/agi/bin/brief.py L1161-1370   # the full parent duties block
read extensions/agi/bin/brief.py L720-765      # the director block, for contrast
```

**What the `_parent()` block actually says** (verbatim shape):
- Docstring: "A loop, not a node. `goal:g4.8`." — then enumerates FIVE things a parent needs: (1) how to spawn via `dispatch.py --tier kid`; (2) the review gate; (3) the serialization/lease rule; (4) what its artefact is (`--owns`, THOUGHT blocks); (5) the done-time commit under `--branch`.
- Brief body: "You run a loop. You do not write the node yourself." then steps: 1. SPAWN kids with `dispatch.py --tier kid --detach`; 2. "AT MOST {parallel} kid(s) running at once, and AT MOST {max_live} agent(s) alive ANYWHERE" (a bound, offered as a ceiling to not exceed, NOT a directive to iterate); 3. REVIEW every node a kid writes; 4. DO NOT bypass the gate; 5. do-not-commit; 6. "SIGNAL DONE when every kid is finished" via `cli.py done ... --owns <kid-node-id>...`.

**Word-level scan of the whole file**: the strings `continue | adjust | done` / `continue (keep going), adjust (reword the plan node), or done` appear ONLY inside the DIRECTOR block (brief.py L729-759, the `season.py judge` contract). The `# continue` occurrences at L881/884/887 are unrelated (a different loop's control flow). NO parent-tier segment contains the words continue/adjust/done, and NO text anywhere in `_parent()` names a per-dispatch kid ceiling for the parent to plan around.

## Evidence

1. **The gap is present and current.** `_parent()` today teaches: spawn → poll → review each kid → signalled done "when every kid is finished". Single-shot in vocabulary. Nothing tells a parent it may judge continue (spawn another kid carrying the previous kid's result), adjust (re-brief), or done. This is precisely why 8/8 (L3.41/L3.42) and then 10/10 (SD.09/SD.10) parents each spawned exactly one kid. My read of the source is consistent with the measured behaviour.
2. **`max_live` is a bound, not an iteration contract.** The brief tells the parent it may have "AT MOST {parallel} kid(s) running at once" — i.e. it forbids exceeding the lease, but never says "and you MAY keep spawning kids one after another until the target is worked out". A ceiling that says "no more than N at once" is not the same as a ceiling that says "no more than N per dispatch". The parent gets the serialization bound but no iteration bound and no iteration vocabulary. (`max_live` passed into `_parent()` exists: it is the lease bound, not a per-dispatch kid cap.)
3. **The vocabulary is one tier up, exactly as claimed.** The words `continue | adjust | done` and `judge ... --against goal:<id>` appear only in the DIRECTOR duties block (L729-759). The director gets to judge outcomes; the parent does not get the same judgement vocabulary for its own kids.
4. **NOT exercised by this experiment**: the "after" half of the testable claim — whether a parent WITH the iteration contract added would actually spawn two or more kids and carry the first kid's result into the second. That requires building the template change (an mvp/build act, out of this experiment's scope) plus a live pi parent dispatch. This experiment stops at confirming the current-state gap.

**Verdict**: the gap the hypothesis names is real and current in the tree. The full claim (post-change parent landing 2+ kids, second carrying the first) remains untested here. Hence `inconclusive_lean_proved` — strong evidence for the gap, no evidence yet for the fix.

## Agent Notes
Static source verification: _parent() in brief.py has NO continue/adjust/done iteration vocabulary and NO per-dispatch kid ceiling; those words exist only in the DIRECTOR block one tier up. Gap confirmed current, matches measured 10/10 single-shot parents. Post-change live proof not attempted (out of experiment scope).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-3afbadd9): ACCEPTED as-is. Verdict inconclusive_lean_proved:70 is honest — the static before-half is fully verified (no continue/adjust/done vocabulary in _parent(), no per-dispatch ceiling; the director block one tier up holds both), and the kid correctly refused to claim the after-half it did not test. evidence_runs self-link is legal: an experiment is its own run. parents resolves to this hypothesis. No demotion needed.
<!-- THOUGHT:END -->
