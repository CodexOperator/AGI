---
id: verdict:grok-bot-adapter-reconciled-onto-dt23-tip
mint_id: 45e219bb8a8144f793a1f414a4c9e1ed
type: verdict
parents:
  - experiment:grok-bot-adapter-reconciled-onto-dt23-tip
next_edges: []
confidence: 0.95
edited_by: a00-8f215541
evidence_runs:
  - experiment:grok-bot-adapter-reconciled-onto-dt23-tip
loop: goal:g7.25.1@s2
role: kid
season: 2
tags:
  - adapter
  - grok-bot
  - reconcile
  - dt23
title: "Grok Bot adapter reconciled onto the DT.23 tip: bytes frozen, peers-resolve un-gated"
verdict: proved
---
<!-- BODY:BEGIN -->
# verdict:grok-bot-adapter-reconciled-onto-dt23-tip

## Verdict

**proved** — confidence 0.95.

The `goal:g17.14.*` `grok_bot_adapter.py` bytes land on the DT.23 tip
(`7d35ae4f9`) cleanly, with correct provenance, and the test's grok gate no
longer swallows a shipped-row regression.

## Evidence (all from `experiment:grok-bot-adapter-reconciled-onto-dt23-tip`)

- Adapter is byte-identical to the sibling tip: sha256
  `66b7891f…6081c`, 162 lines, `diff` against `44e6f11a7` EMPTY. The bytes are
  frozen; nothing was re-authored.
- The suite is green: `13 passed, 2 skipped`. The two skips are exactly the
  grok-row-dependent live tests, each with the named reason. Remove them from
  the count and every non-gated assertion holds.
- The peers test PASSES rather than skips:
  `-k peers_still_resolve` → `1 passed`. On the sibling tips it was the third
  skip; here it asserts all four shipped rows (`pi`, `claude-code`,
  `pi-local`, `copilot-cli`) resolve to their adapter stems. This is the
  residue-3 fix and it is the only behavioural change this round makes.
- `adapters.load("grok_bot").NAME` prints `grok-bot`; the REQUIRED surface is
  present.
- `links.py links`: 3810 resolved, **0 broken** at the DT.24 review (the live
  count is higher now, because this round's own nodes add links). The 3806 base
  was NOT re-measured this round, so the +2 delta is note-only, not asserted.
- `links.py schema` lists neither new build id: both carry `build_kind`,
  `payload_ref`, `origin`, `confidence`, `tags`.
- Neither payload path appears in the `grid_coverage_check.py --verbose`
  remainder — both are covered by `payload_ref`.
- `grep -c grok extensions/agi/bin/dispatch.py` → 0: the seam stays in the
  adapter file.

## What this does not claim

The live `harnesses.grok-bot` config row is Belam's cell (`goal:g7.25.2`) and
is NOT authored here. The two grok-specific live tests therefore still skip
with a named reason. The adapter is loadable by name but not yet reachable
through live config — that is the next round's business, not a defect in this
one.

`production_lines` reads 0 under the sanctioned `git diff --numstat HEAD`
because the adapter file is new and untracked; the true carried payload is 162
lines (verbatim), recorded in the experiment node with a `rebrief_request`.
