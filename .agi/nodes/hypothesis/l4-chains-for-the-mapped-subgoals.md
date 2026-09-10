---
id: hypothesis:l4-chains-for-the-mapped-subgoals
mint_id: 8f262215f12b438db9442478ba32483c
type: hypothesis
parents:
  - goal:g5
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 5c2d6cdcf4beb5ab
season: 2
status: pending
tags:
  - l4
  - chain
  - g5
testable_claim: "Under each of the TEN sub-goals listed in this node's body, an `idea` and a `hypothesis` exist, minted with write.py. Each hypothesis's `testable_claim` states, in checkable form, WHAT CHANGES, in WHICH file or node, and HOW IT IS PROVED -- it is the assignment its named L4 round will be dispatched at, so it must read as an instruction a later agent can execute without opening the plan. Every `parents` edge resolves (`links.py links` reports broken_links: 0). NO build node is minted -- goal:s29's shapes belong to the rounds that build, not to this one. No node is deleted and no goal id is renumbered. HARD CEILING: 3 kids. A kid writes NODES ONLY; the point director reviews claim quality and demotes or rejects, never deletes."
thought_session: sanctuary-director-genVI-L4
title: Ten L4 sub-goals have no idea/hypothesis chain, so the rounds that will act on them have nothing to be dispatched at
---
<!-- BODY:BEGIN -->
**BUILD, NOT A PROBE. YOUR ARTEFACT IS NODES ON DISK.** Mint them with `write.py`; a report describing what should be minted is a FAILED round.

Round L4.20 put every owner brief point into the graph as a sub-goal. Ten of those sub-goals will be acted on by a later L4 round, and a round is dispatched AT a hypothesis whose `testable_claim` IS its assignment (trap 0ak). Those ten have no chain yet, so there is nothing to dispatch at. **Mint `idea` -> `hypothesis` under each.**

## The ten. Everything you need is here; do NOT open `doc:l4-plan` (19.7k words).

| sub-goal | brief point | the round that will act on it | what its hypothesis must make checkable |
|---|---|---|---|
| `goal:g5.3` | B1 every top-level `gN` is perpetual | **L4.07** | twelve `gN` flip to `goal_kind: perpetual`; `goal:g11` does NOT; node count unchanged; `snapshot-goals.py --render --check` round-trips. Note `perpetual` is carried STRUCTURALLY by GOALS.md's `## Perpetual` section, so the flip MOVES twelve goals in the rendered document |
| `goal:g17.3` | B3 she owns seats, models, how many active | **L4.13** | who may write `config:seats` and the model/count fields, and what refuses when anyone else does |
| `goal:g17.5` | B5 the duty matrix | **L4.03, L4.04, L4.08** | `brief.py` renders the card and it REPLACES the tier's prose job description, identical under `full` and `survival`, per-role tokens go DOWN; `hierarchy.py --check` refuses more than the matrix allows and WARNS (never refuses) on fewer |
| `goal:g17.6` | B6 each role's ONE question | **L4.08** | all twelve existing seats carry a valid card whose question is present and singular; `hierarchy --check` clean; NO new seat added |
| `goal:g17.7` | B7 the `seat` node type | **L4.13** | `[seat].md` declares the type; twelve EXISTING rows mint as `seat` nodes under `parents: [goal:g17]`, cells verbatim; `config:seats` still resolves and still serves `send.py`; `active_node_count` grows by exactly 12; `seat` added to `CANONICAL_NODE_TYPES` |
| `goal:g17.8` | B8 messaging restrictions | **L4.14** | `send.py` resolves targets through the seat nodes and refuses one outside the sender's `tells`, while the inbox-only prime and the closed `quorum` room refuse exactly what they refuse today |
| `goal:g17.9` | B9 channels A/B, no director->Prime edge | **L4.21** | `send.py` gains `audience keep` and `audience council`; any director->prime message is refused; existing refusals stand |
| `goal:g17.10` | B10 one voice per chamber, the DM room | **L4.21** | an inter-chamber DM room accepts exactly ONE response per chamber act; Council->Keep propagation happens |
| `goal:g17.12` | B12 the Masters own their workflows | **L4.22, L4.27** | each `* Master` dispatches its own workflows through the one router; and the five unstaffed seats get tracks/tells/question/writes as **SPEC ONLY** -- not one is created, launched or given a row |
| `goal:g5.4` | B21 season review and rollover | **L4.18, L4.19** | one `bigger_outcome` per perpetual goal and one `overview` per lens vision; `rollover` keeps refusing while any season-current overview is unjudged; the verdict is recorded via `season.py judge` and `explain` stamps NOTHING |

## Rules — these are the graph's, not mine

1. **`idea` then `hypothesis`, in that order**, the hypothesis parented on the idea. Check each type's `allowed_parents` in `.agi/context/schemas/[idea].md` and `[hypothesis].md` BEFORE minting; the spawn gate refuses a wrong shape and that refusal is the gate working.
2. 🔴 **NO BUILD NODES.** `goal:s29`'s shapes belong to the rounds that build. A build node here is an over-build and will be rejected.
3. **The `testable_claim` is the assignment**, in checkable form: what changes, in which file or node, how it is proved. Write it so a later agent can execute it without opening the plan. Vague claims are demoted on review.
4. **No node is deleted, ever** — deprecate and move. No goal id is renumbered.
5. **Verify the BYTES with grep after every write** — never the `updated:` line (trap 0ah).
6. `links.py links` must report **broken_links: 0** when you are done.
7. 🔴 **Do NOT run the full pytest suite** — the prime may be running it. Nothing here touches `.geometry`, so it is not needed.
8. **HARD CEILING: 3 kids.** Ten chains is comfortably one kid's work; spend a second only if the first leaves rows unminted.

**DONE means:** twenty nodes exist (ten `idea`, ten `hypothesis`), each hypothesis parented on its idea and reaching its sub-goal, `links.py links` reporting 0 broken. Report what you minted per sub-goal. If you cannot reach it, name the exact row that failed and stop — a truthful partial beats a green report.

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?