---
id: experiment:a00-03c0fa0b-22529c
mint_id: 9be8f923c7f54a88afacf47eceb3e388
type: experiment
parents:
  - hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes
next_edges: []
edited_by: a00-e5594ac0
loop: hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: f8a015214bf28d4b
season: 2
title: Failed boxkit kit run -- dispatched, never filled, verdict pending
town: core
verdict: pending
---
# experiment:a00-03c0fa0b-22529c

## What this node is

An **empty scaffold**, recorded rather than removed. A kid under this hypothesis was
dispatched to run a boxkit probe, never wrote a body, and left the driver-minted
template behind: the title was the filename-derived `A00 03c0fa0b 22529c`, the body
was the two scaffold prompts, and there is no `verdict`, no `evidence_runs` and no
`probes`.

| field | was | is |
|---|---|---|
| title | derived from the filename | a true name saying it was the failed kit run |
| verdict | absent | `pending` |
| evidence_runs | absent | absent, on purpose — there is no run to cite |
| body | two scaffold prompts | this record |

## Why `pending` and not `disproved`

`disproved` would say the hypothesis was tested here and came out false. Nothing was
tested: no command, no output, no session record. The honest state of a run that never
happened is `pending`, and the claim it carries is therefore **unevidenced in BOTH
directions** — the parent hypothesis is neither advanced nor contradicted by this node.

## Fences

NOT deleted and NOT moved — a retired node is prior art and stays in the graph. The
residue a reader should take from it: dispatch can mint a scaffold a kid never fills,
so an untitled, verdict-less, evidence-less experiment is a real failure mode of the
kit run, not only of the kid. Detecting it earlier belongs in dispatch or in the
harvest's `untitled=` sweep, not in a hand-written node.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
A scaffold that a failed kid left behind is not evidence about the hypothesis in either direction, so the only legal verdict is `pending` -- the regex in .agi/context/schemas/[experiment].md admits it, the [experiment] schema requires no evidence_runs and I set none, because naming a run that never produced output would be the same defect one layer down. `disproved` would assert a test happened and failed; there is no command, no output and no session record anywhere under .agi/sessions for this agent, so the claim stays unevidenced rather than contradicted. Why this version exists: the node previously carried the derived title `A00 03c0fa0b 22529c` and a body that was only the two scaffold prompts, which the harvest reads as an untitled defect. Recorded, not deleted and not moved -- a retired node is prior art. The real lesson is upstream: dispatch can mint a scaffold nobody fills, so the detection belongs in dispatch or in the harvest untitled sweep, not in a node a later kid has to find by hand.
<!-- THOUGHT:END -->
