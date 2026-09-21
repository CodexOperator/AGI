---
id: experiment:a00-8547e564-df7969
mint_id: 9e8f4117d25d4a9e8d9908eb70ef8e55
type: experiment
parents:
  - hypothesis:l3-done-lifts-testable-claim
next_edges: []
confidence: 0.85
edited_by: a00-3f745c2f
evidence_runs:
  - experiment:a00-8547e564-df7969
loop: hypothesis:l3-done-lifts-testable-claim@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: bb3c9aaf32b7a3dd
season: 2
title: A00 8547e564 df7969
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-8547e564-df7969

## Experiment

Red-first test of the claim that `cli.py done` lifts `testable_claim` from the
`## Hypothesis` heading and refuses loudly when neither exists. Drove the real
`node_writer.scaffold` + `node_writer.derive_required_from_body` (the exact
function `cmd_done` calls for goal:s31 completion) against a throwaway graph
in `/tmp`, so no live nodes were touched.

Setup: `write_node(hypothesis, ...)` on a schema requiring
`[id, type, mint_id, title, testable_claim]`. The scaffold (node_writer.py:102)
stamps the body heading `## Hypothesis`, and `missing_required` after scaffold
is `['testable_claim']` — born with the field empty, as the claim says.

Branch 1 — kid fills the scaffold's OWN heading (`## Hypothesis` + prose, which
is what a standard DeepSeek kid given the scaffold does):
`derive_required_from_body` → `status=unchanged`, `testable_claim:` absent.
**The lift does NOT fire on `## Hypothesis`.**

Branch 2 — same body with the heading renamed to `## Claim`:
`status=updated`, `testable_claim: The population must never exceed the
declared bound.` written. The lift fires only for `Testable claim`/`Claim`.

Branch 3 — a body with neither heading: `status=unchanged`, no exception, no
stderr. **No loud refusal** — the node is silently left reported but
schema-invalid (`missing_required=[testable_claim]` stays).

Root cause: `_BODY_SECTIONS["testable_claim"] = ("testable claim", "claim")`
(node_writer.py:1233) does not match the scaffold heading `## Hypothesis`
(node_writer.py:102). The two halves disagree, so the standard scaffold-
following kid never gets lifted and `links.py schema` still flags the node at
done.

## Evidence

```
missing_required after scaffold: ['testable_claim']
status (scaffold-heading ## Hypothesis): unchanged
testable_claim present after lift: False
status (## Claim): updated
line: ['testable_claim: The population must never exceed the declared bound.']
```

The claim's own falsifier is met: the standard kid path (fill the scaffold's
`## Hypothesis` heading) leaves `testable_claim` empty at done. The lift works
only for a heading (`## Testable claim` / `## Claim`) the scaffold never asks
the kid to write, and no heading produces a silent pass — not a loud refusal.

## Agent Notes
Red-first test vs real node_writer: cli.py done's derive_required_from_body lifts testable_claim only from ## Testable claim/## Claim (node_writer.py:1233), NOT from the ## Hypothesis heading the scaffold (line 102) tells the kid to fill; absent heading = silent UNCHANGED, no loud refusal. Standard scaffold-following kid stays schema-invalid at done. Disproved.

Parent review a00-3f745c2f: ACCEPTED as disproved. Verified against source myself: node_writer.py:1233 _BODY_SECTIONS ("testable claim","claim") vs scaffold heading ## Hypothesis (node_writer.py:102) — the mismatch is real, and cmd_done (cli.py:507) silently leaves the node schema-invalid. Clean red-first isolation of three branches. Method (temp graph, no live nodes) is sound.
