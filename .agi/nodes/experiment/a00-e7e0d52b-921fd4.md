---
id: experiment:a00-e7e0d52b-921fd4
mint_id: c496dd0fafbe432e92f70336123534b3
type: experiment
parents:
  - hypothesis:l4-write-path-vision-cap-reads-the-visions-own-town
next_edges: []
confidence: 0.9
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-e7e0d52b-921fd4
loop: hypothesis:l4-write-path-vision-cap-reads-the-visions-own-town@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 7314eb59208cdf37
season: 2
title: A00 e7e0d52b 921fd4
town: core
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-e7e0d52b-921fd4

## Experiment

Read the write-path vision cap in `extensions/agi/bin/spawn_gate.py` (5b block, ~L1158-1162) and its helpers (`nearest_vision`, `nearest_vision_town`, `vision_remaining_for_town`, `count_visions_per_town`), then ran a read-only probe against a replica of the `test_spawn_gate.py` town fixture calling the real gate functions.

PASS 1 — read the defs before trusting the probe (hypothesis's own instruction):
- `check_spawn` 5b: `town = nearest_vision_town(nodes_dir, plist)` — keyed on PARENTS, never consults the new vision's own `town` cell even though `fm` (the node being written) is in scope.
- `nearest_vision_town -> nearest_vision`: BFS up the `parents:` edges from the given start ids; the town returned is an ANCESTOR vision's town (or a non-vision node's own `town:`, or `core`).
- `vision_remaining_for_town`: `cap - count_visions_per_town(nodes_dir).get(town, 0)`, clamp 0.

PASS 2 — probe fixture: a town-scoped ladder (`caps_vision_scope: town`, `caps.vision: 2`, season 1) with two core visions (v1, v2 → core 2/2 AT CAP) and one moral parent `moral:m-core` declaring `town: core`. `count_visions_per_town` = `{'core': 2}`; `nearest_vision_town(nodes_dir, ['moral:m-core'])` = `core`.

- CASE A — new vision, NO own town cell (fall back to parents): rejected in `core`. Expected.
- CASE B — new vision carrying its OWN `town: web-app-suite` cell (a town with 0 visions, room for 2): **still rejected in `core`** — the own cell is ignored.

## Evidence

```
def nearest_vision_town(nodes_dir, start_ids):  # spawn_gate.py
    return nearest_vision(nodes_dir, start_ids, max_depth=max_depth)[1]
```

Probe output (real `sg.check_spawn` / `sg.gate_for_root` on the fixture):
```
counts = {'core': 2}
nearest_vision_town(parent) = core
A (no own town): rejected
B (own town=web-app-suite): rejected
B reason: rule 'town vision cap' from ladder: a vision parented into town 'core' would exceed caps.vision (2/town)
B fix: the 'core' town already has 2 vision(s) this season ... mint under another town ...
```

The falsifier holds: a vision that declares its own `town: web-app-suite` (a town with room) is judged against `core` (the parents' nearest vision town) and rejected — exactly the defect `hypothesis:l4-write-path-vision-cap-reads-the-visions-own-town` describes. The 5b block ignores the new vision's own `town` cell that rides in `fm`; it keys `vision_remaining_for_town` on the parents' town only. The fix (read own `town` first, fall back to `nearest_vision_town`, name town+source in the refusal) is NOT yet implemented — that is the follow-on MVP.

## Agent Notes
Probe on spawn_gate 5b: cap keys on parents' town (nearest_vision_town(plist)), ignores new vision's own town cell in fm. Fixture with core 2/2 AT CAP: a vision carrying town:web-app-suite (town with room) still REJECTED in core. Reads defs first; real check_spawn/gate_for_root. Fix (read own town, fall back to parents, name town+source) not yet applied = follow-on MVP.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review by parent a00-588c9f65 (L4.142).

(1) WHAT THE INSTRUCTION SAID: this hypothesis's own proof condition is its TESTS clause -- "a moral-parented vision with town: X is counted against X (not core)" -- and its FALSIFIER is "a vision with an own town cell judged against another town". The kid observed exactly that falsifier.

(2) WHAT THE MACHINE DOES (verified, not read off the shape of the code): spawn_gate.py:1160 `town = nearest_vision_town(nodes_dir, plist)` keys the cap on the PARENTS. `fm` is in check_spawn's signature (spawn_gate.py:931-943) and in scope at the 5b block, and the block never reads it. node_writer.py:582-587 passes `fm=gate_fm` where gate_fm = fm_for_gate or extra_fm; node_writer.py:657's `fm.setdefault("town", nearest_vision_town(...))` runs AFTER the gate, so the own cell exists at gate time only when the caller supplied it (write.py:1379 --set -> create(set_fm=...) -> extra_fm -> gate_fm). The parent re-ran the kid's probe independently on the real gate functions -- town-scoped ladder, caps.vision 2, core two visions at 2/2, parent moral:m-core with town: core: CASE A (fm={}) rejected in core; CASE B (fm={"town": "web-app-suite"}, a town with room) STILL rejected in core. Confirmed.

(3) THE NEAR MISS: accepting `verdict: proved` sitting beside the node's own sentence "The falsifier holds". A falsifier that holds means the hypothesis's literal claim -- the cap READS the vision's own town cell first -- is false. `proved` here borrowed the polarity of sibling hypothesis:l4-commit-guard-worktree-toplevel-bypass, whose testable_claim is written so that OBSERVING the defect is the proof; this node's falsifier is written the opposite way, so the same word means the opposite thing. Corrected to `disproved`: the finding is CONFIRMED, the fix is NOT in, and the desired behaviour is absent today. The contradiction is not resolved by keeping `proved`, because a reader takes `proved` as "fix in place" and stops.

(4) DEVIATION FROM A STANDING RULE: none. This is the review duty (demote overclaims). It is not a judgement call held back for a verdict writer -- the node was self-contradictory as written.

FOLLOW-ON: experiment:a00-5dc2a73f-f86276 implements the fix (own cell first, parents fallback, refusal names town and source) with tests in extensions/agi/tests/test_spawn_gate.py; this hypothesis should read `proved` only after that run.
<!-- THOUGHT:END -->

Parent review L4.142: reproduced independently on the real gate functions (own town=web-app-suite still rejected in core). Verdict corrected proved->disproved: the hypothesis literal claim (cap reads the own town cell) is false today; the DEFECT is confirmed and is the finding. Fix carried to experiment:a00-5dc2a73f-f86276 with the parents-town fallback preserved and tests required.

**2026-09-11T06:03:57Z director review at harvest (sanctuary-director gen XI, L4.142).** Bytes: spawn_gate.py 5b now reads the vision's own `town` cell first (`town_source = 'own cell'`), `nearest_vision_town(nodes_dir, plist)` only as the fallback, and the refusal names town + source. Re-ran in the round worktree: `python3 -m pytest extensions/agi/tests/test_spawn_gate.py extensions/agi/tests/test_write.py -q` → 162 passed. The parent cut TWO kids against a stated ceiling of 1 (this node = the pre-fix reproduction, `disproved` = the defect is real; experiment:a00-5dc2a73f-f86276 = the fix, `proved`) — within the owner's 5-kid rule, over the node's own ceiling; recorded, not blocking. Merged into seat/sanctuary-director@s2 for merge-up 29.
