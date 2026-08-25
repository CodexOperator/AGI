---
confidence: 1.0
goal_id: S16
goal_kind: short-term
id: "goal:s16"
mint_id: f52e9f204e264a91b64f9e7e7aecef15
origin: goals-doc
seeds: []
status: complete
tags:
  - goal
  - root
  - short-term
title: "S16: The evidence gate demoted `verdict:` and left the `status` shadow behind"
type: goal
---

Done 2026-08-25. The H4 gate rewrote exactly one field. A demoted node
therefore read:

```
status: proved
verdict: "inconclusive_lean_proved:50"
evidence_runs: 0
demoted_from: proved
```

**The contradiction was not inert.** `bin/benchmark.py:85` builds the LLM
judge's prompt with `Status: {fm['status']}` and `Verdict: {fm['verdict']}` as
two adjacent lines, so the judge deciding CONTINUE / CLOSE / BRANCH was being
handed the overclaim the gate had just removed.

**`status:` is a legacy shadow of `verdict:`, and that is settled on three
independent grounds** — worth stating, because `status` is *also* a real,
engine-read field on other node types and the distinction is what makes the
fix safe:

1. **No schema declares it for a chain node.** `context/schemas/` declares
   `status` only in `[task].md` (`pending|in_progress|done`, required) and
   `[idea].md` (`open|extended|abandoned`). There is no `[verdict].md` at all,
   and that is a gap rather than a design — `task:t-031`
   (schema-registry/R8, still `pending`) is the unbuilt task that ships one.
   Its spec names the field `state`, not `status`.
2. **No engine writer writes it.** `cli.py done` sets `rec["status"]` on the
   *agent record* under `sessions/`; it never puts `status` in node
   frontmatter. Every occurrence in `nodes/` was hand-written by a kid
   alongside `verdict:`.
3. **No engine reader interprets it as a verdict.** `status` is read as goal
   lifecycle (`metrics.py` `SCORING_GOAL_STATUSES`, `dashboard.py`) and as
   task/idea lifecycle. Nothing reads it as a verdict claim.

**The domains are disjoint, which is the whole safety argument.** No
lifecycle vocabulary anywhere in this corpus contains `proved` or
`disproved`. So a rule that rewrites `status` **only when it reads one of
those two words** cannot reach a task's, idea's or goal's lifecycle, and
needs no per-type branching to prove it.

**Engine fix (in `agi`).** `evidence_gate.SHADOW_VERDICT_FIELDS` names the
shadow; `stamp()` rewrites every shadow field that reads a decisive verdict to
the demoted value, so both writer paths (`post_wire.py`, which calls `stamp`,
and `cli.py`'s raw-line `_append_verdict_to_node`, which cannot and enforces
it inline) now hold one invariant: **after a demotion, no frontmatter field of
the node reads `proved` or `disproved`.**

**Metric fix.** `unevidenced_decisive_verdicts` reads `verdict:` and only
`verdict:` — deliberately unchanged, because its definition has to stay
comparable across runs. It was reporting 1 while 58 nodes advertised a
decisive verdict elsewhere. The blind spot is now its own counter,
`shadow_decisive_verdicts` (plus `shadow_decisive_no_verdict` for the worse
subset), sharing `evidence_gate.shadow_verdict_fields` with the gate for the
same reason `build_corpus` is shared: the alarm and the rule must not drift.

**Sweep of 57 nodes, demote-only.** Node count held at 764.

| class | n | action |
|---|---|---|
| decisive `status` + already-demoted `verdict` | 42 | `status` := the honest verdict |
| decisive `status`, **no `verdict:` field at all** | 10 | claim migrated into `verdict:`; evidence resolved, so it stands |
| same, evidence resolves to 0 | 5 | migrated **and** demoted, `demoted_from` stamped |
| same, `evidence_runs` is a taxonomy violation | 1 | **rejected — nothing written**, see below |

**The middle two rows are the finding, not the bookkeeping.** 16 nodes
expressed their verdict *only* in `status:`, so `evidence_stats` — which
starts by reading `fm.get("verdict")` and skipping the node if it is absent —
could not see them at all. They were in no numerator and no denominator.
Five of them were unevidenced decisive verdicts that
`unevidenced_decisive_verdicts: 0` had never once counted.

> **[truncated: 1658 of 5406 characters dropped at a block boundary to fit the 4000-character cap. `GOALS.md` section `S16` is the complete text; raise `goal_body_cap` in the project config to keep more.]**
