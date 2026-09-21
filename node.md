---
id: experiment:a00-da23eefb-64a6f1
mint_id: 05fc7494abdc44aaa8a55b23ef46dc6e
type: experiment
parents:
  - hypothesis:l3-done-lifts-testable-claim
next_edges: []
confidence: 0.9
evidence_runs:
  - experiment:a00-da23eefb-64a6f1
loop: hypothesis:l3-done-lifts-testable-claim@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 8ebde8e18349fa2b
season: 2
title: A00 da23eefb 64a6f1
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-da23eefb-64a6f1

## Experiment

Probe the claim that `cli.py done` on a hypothesis node lifts the
testable claim out of the kid body, so a finished hypothesis is
schema-valid at done. Reduced it to a red-first, end-to-end run.

**What I did.** Built a temp project (`.agi/`, a `[hypothesis].md`
schema requiring `testable_claim`), scaffolded a hypothesis with
`node_writer.write_node` — born missing `testable_claim`, exactly the
s31 failure the parent hypothesis names. Simulated the kid's ONE legal
channel: replaced the scaffold placeholder paragraph under the
scaffold's own `## Hypothesis` heading with a real claim, touching only
the body. Wrote the `sessions/iter-001/*/agent.json` record, patched
`_find_root`/`_session_root`, and drove the real `cli.cmd_done`
(`--node-id hypothesis:...`, `--no-evidence-gate`).

**What happened.**

```
scaffold: written missing: ['testable_claim']
agent a00-probe status=done verdict=inconclusive_lean_proved:60
cmd_done rc: 0
testable_claim lifted: False
missing_required after done: ['testable_claim']
```

`cmd_done` returned 0 and wrote the verdict, but `testable_claim` was
NEVER lifted. `derive_required_from_body` is called from `cmd_done`
(cli.py ~L507) but returned nothing, because `_BODY_SECTIONS` in
node_writer.py only recognizes headings `"testable claim"` and
`"claim"` — not the `## Hypothesis` heading the scaffold actually hands
the kid.

I then mapped every heading to confirm it is the heading, not the lift
path, that fails:

```
'## Hypothesis'      -> status=unchanged missing=['testable_claim']
'### Testable claim' -> status=updated   lifted
'### Claim'          -> status=updated   lifted
'## Claim:'          -> status=updated   lifted
'### The claim'      -> status=unchanged missing=['testable_claim']
```

## Evidence

- **Red-first run**: `cmd_done` on a hypothesis corrected only by a real
  body under `## Hypothesis` → `testable_claim` still empty after done.
- **Exact code path exercised**: cli.py `cmd_done` → `node_writer.derive_required_from_body`
  → `_section_text` → `_BODY_SECTIONS["testable_claim"] = ("testable claim", "claim")`.
- **Heading map** (above) shows `## Hypothesis` and `### The claim` are
  NOT keys; only literal `testable claim` / `claim` fire the lift.
- **Repo suite stays green**: `test_node_writer.py test_cli.py` 80 passed
  (mechanism is intended and separately tested, on the non-brief heading).

## Verdict reasoning

Hypothesis `l3-done-lifts-testable-claim` states: if `done` lifts the
claim from the `## Hypothesis` heading, then a standard kid's hypothesis
is schema-valid at done. The enabling condition is **false in the
current tree**: the lift fires only under headings the scaffold never
uses, and it returns `UNCHANGED` silently (no loud refusal) when no
section matches. So the predicted outcome — schema-valid at done for a
standard DeepSeek kid — does NOT hold; the node still ships
`missing_required=['testable_claim']`. The claim's own falsifier is
triggered ("the standard kid path still leaves the field empty").

One nuance: the hypothesis hedges on "or a Claim: line the kid brief
now tells it to write". The current scaffold body is the ground truth
of the brief, and it instructs `## Hypothesis`, not a `Claim:` line, so
today the hedge does not rescue the claim. The fix is one line — add
`"hypothesis"` to `_BODY_SECTIONS["testable_claim"]` (and possibly
"the claim") — but deciding/applying it belongs to the parent chain,
not this probe; the probe's job was to falsify the claim, and it did.

## Agent Notes
Probe: done lifts testable_claim only under 'Testable claim'/'Claim' headings, NOT the scaffold's '## Hypothesis' heading; standard kid still ships schema-invalid. Disproved.
