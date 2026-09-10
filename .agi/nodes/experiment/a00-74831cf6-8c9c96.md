---
id: experiment:a00-74831cf6-8c9c96
mint_id: d56eab989d3b44b0beca882dc43f868b
type: experiment
parents:
  - hypothesis:l4-workflow-types-and-default-harness-are-a-geometry-node
next_edges: []
confidence: 0.7
edited_by: a00-778cb024
evidence_runs:
  - experiment:a00-74831cf6-8c9c96
loop: hypothesis:l4-workflow-types-and-default-harness-are-a-geometry-node@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: fa3c1f37bd2cdb96
season: 2
title: "Shadowing-gap experiment: config-row and manifest provider eclipse the node per-workflow/per-type override levels"
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-74831cf6-8c9c96

Experimental follow-up on hypothesis:l4-workflow-types-and-default-harness-are-
a-geometry-node (parent experiment:a00-2b046d3e-35273a, accepted
inconclusive_lean_proved:85). THE GAP it must test (named in that THOUGHT and
in the shipped body): `_resolve_default_harness` resolves the config row
`provider` and a manifest `provider` FIRST (levels "config row", "manifest"),
so a workflow that carries either one SHADOWS the node's own per-workflow
`workflows.<key>.harness` AND its per-type `types[type].harness` — those two
graph-committed override levels become unreachable. Three of the six live
workflows (review, drafting, deep-search) carry a config.json provider row.

## What I did

Added one test to extensions/agi/tests/test_workflow.py,
`test_config_row_shadows_node_perworkflow_and_type`, that proves the shadowing
with DELIBERATELY DISTINCTIVE values so the assertion can only pass because a
row eclipses the node — not because two values happen to agree:

- workflow X has a config row `provider: claude-code`, a manifest `type: tX`
  whose type harness is `type-seek`, and a node per-workflow harness
  `deep-seek`. Resolved: `claude-code` / level `config row`. Neither
  `deep-seek` / `per-workflow` nor `type-seek` / `type:tX` ever appears —
  both node levels are DEAD behind the row.
- workflow Y has NO config row but a manifest `provider: claude-code-py`.
  Resolved: `claude-code-py` / level `manifest` — the manifest provider also
  shadows both node levels (and the node is never even loaded).

Then I measured the LIVE six on the real .agi/config.json with a temp node
where every workflow+type got a distinctive override (`_resolve_default_harness`
with the node path redirected to the temp file):

    workflow              config_row.provider  resolved     level
    review                pi                   pi           config row
    drafting              claude-code          claude-code  config row
    deep-search           pi                   pi           config row
    l3w-route-probe       (none)               P-route      per-workflow
    l4-plan-research      (none)               P-plan       per-workflow
    prime-open-questions  (none)               P-inv        per-workflow

## What happened (results)

The shadowing is REAL, MEASURED, and confined to the three workflows that
carry a config row. For review/drafting/deep-search the config row is the
single source of truth: committing a per-workflow `harness` or a per-type
`harness` for them is a silent no-op. The other three (l3w-route-probe,
l4-plan-research, prime-open-questions) resolve through the node's own
per-workflow level. `python3 -m pytest extensions/agi/tests/test_workflow.py -q`
-> 38 passed (37 prior + this one). The engine's kid-tier guard refuses a bare
`tests/` directory run by design (advisory window), so scoped to test_workflow.py.

## Judgment (child of the parent's deviation, not a re-litigation)

This is NOT a code bug: `_resolve_default_harness` faithfully implements the
order the shipped body documents ("the config row `provider` and a manifest
`provider` are the same per-workflow level and resolve first — kept so existing
config rows keep working unchanged"). Runtime config beating a committed
`.geometry` default is exactly the config-maxxed contract
(hypothesis:l3w4-workflows-config-maxxed): `config.json workflows.<name>` is
the live knob, flip-with-no-edit. The claim's PROVED-BY only promises the
prime-default flip for a workflow with NO override, so the shadowing does not
violate the hypothesis. What the graph should remember: for 3 of 6 live
workflows the node's per-workflow and per-type override levels are unreachable
— a prime who commits `workflows.review.harness=claude-code` following the
"edit-and-commit IS the change" doctrine would watch nothing change, because
review's config row `provider: pi` still wins. Low severity today (the live
config rows agree with the type defaults anyway), but it is a latent trap for
whoever treats the node row as a real override. No engine change made here —
reordering the levels would break the documented "config rows keep working
unchanged" promise and is the prime's call.

## Evidence

Full shadowing fixture (workflow.py test) and the six-workflow live-column
measurement above. Tools: `python3 -m pytest ... -k "config_row_shadows" -v`
(PASSED); a one-off python call into `_resolve_default_harness` with the node
path monkeypatch-redirected to a /tmp node.

## Agent Notes
Measured the shadowing gap the parent flagged: a config.json provider row
(and a manifest provider) resolves BEFORE the node's per-workflow and per-type
harnesses, so those graph-committed override levels are unreachable for the 3
affected live workflows (review, drafting, deep-search). Matches the shipped
body's documented order and the config-maxxed contract — not a code bug, but a
real latent trap (node override commit is a silent no-op for half the
registry). Added the proving test; 38 passed. No engine change; ordering is the
prime's call.

## Agent Notes
Measured the shadowing gap: config-row/manifest provider resolve before the node's per-workflow and per-type harnesses, so those committed override levels are unreachable for the 3 config-row live workflows (review, drafting, deep-search) — matches shipped documented order + config-maxxed, not a code bug, but a latent trap; added proving test (38 passed), no engine change, ordering is the prime's call.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-778cb024 L4.111 — ACCEPTED at the kid's own lean (70), evidence linked, no overclaim. VERIFIED BY READING THE ARTIFACT, not the report: test_config_row_shadows_node_perworkflow_and_type is real and uses distinctive values (config row claude-code vs node per-workflow deep-seek vs type type-seek) so it can only pass because a provider row eclipses both node levels; pytest test_workflow.py = 38 passed. Its live-column table (review/drafting/deep-search resolve at "config row"; l3w-route-probe/l4-plan-research/prime-open-questions resolve "per-workflow") is a correct consequence of the code order I read in _resolve_default_harness (cfg_row provider, manifest provider, node workflows.<key>.harness, node types[type].harness, default_harness, raise). WHY THIS VERSION DIFFERS FROM THE ONE BEFORE IT: the first experiment (experiment:a00-2b046d3e-35273a) shipped the resolution order and DOCUMENTED the shadowing in extensions/agi/briefs/workflows.geometry.md; this experiment turns that documented sentence into a measured, regression-locked fact, so a future reorder of the levels cannot silently un-shadow them. MECHANISM NEAR MISS: a test that used the live config values would pass whether or not the node level were reachable, since the live rows agree with the type defaults; the distinctive-value fixture is what makes the dead level observable. NEAR MISS 2: reading the kid's report ("shadowing is real") without running the test would have accepted the claim on the report rather than on an artifact — I ran the 38 and read the assertion text instead.
<!-- THOUGHT:END -->
