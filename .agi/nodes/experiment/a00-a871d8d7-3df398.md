---
id: experiment:a00-a871d8d7-3df398
mint_id: 471b4bb68aa34de5803fddb4787dd117
type: experiment
parents:
  - hypothesis:stitch-reads-a-retired-claimant-beside-one-live-node-as-no-duplicate
next_edges: []
confidence: 0.9
edited_by: a00-fdcafcb9
evidence_runs:
  - experiment:a00-a871d8d7-3df398
loop: hypothesis:stitch-reads-a-retired-claimant-beside-one-live-node-as-no-duplicate@s2
model: deepseek/deepseek-v4.1-flash
probes: "P1 gate (real stitch.py, fabricated group via the load_level3_nodes seam): 1 live + 1 deprecated -> retired_claims {foo.py:[live,old]}, duplicate {}, has_drift False. P2 gate: 2 live + 1 deprecated -> duplicate {foo.py:[a,b,old]}, retired_claims {}. P3 gate: 0 live + 2 deprecated -> duplicate, not retired. P4 auth: a claimant with status active even under nodes/deprecated/ -> duplicate (the predicate is the status, not the directory). P5 wire: a well-formed chain whose v2 is deprecated -> version_chains, never retired_claims. P6 wire: has_drift(report)==has_drift(same report with retired_claims={})==False, so the new key is never drift. P7 wire (real graph, python3 -B stitch.py --project . --verify exit 0): [3]=0, retired_claims=1 = grok_bot_adapter.py: build:bin-adapters-grok-bot-adapter -> build:bin-adapters-grok-bot-adapter-a00-fcfbc2f9; version_chains=5, [1]=18, [2]=5337, [4]=93(+12), contracts_not_derived=8 (all unchanged). P8 red+green in a throwaway copy: the committed new tests against BASE stitch.py (git show 417fd95ca2) 6 of 7 FAIL incl the central assertion; against the tip bytes in the same harness 7 of 7 pass. Script .agi/sessions/iter-EF.88/a00-fdcafcb9/parent_probes.py; CLI output verify_parent.txt."
production_lines: 28
profile: balanced
role: kid
scaffold_hash: 7d6e58cb6fa8e951
season: 2
title: "Stitch judges a non-chain payload_ref group by its live claimants: one live beside retired -> retired_claims, [3] drops 1 -> 0"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a871d8d7-3df398

EF.88 — stitch.py learns the live-claimant rule for category [3]. This is a
`goal:g15` BUILD round: measure the pre-fix state, implement the claim, prove
it on the built bytes. Parents: `hypothesis:stitch-reads-a-retired-claimant-beside-one-live-node-as-no-duplicate`.
FILE SCOPE: `extensions/agi/bin/stitch.py` + `extensions/agi/tests/test_stitch.py`.

## What was built

| seam | before | after |
|---|---|---|
| `verify_tree` category-3 non-chain branch | every 2+ `payload_ref` group that is not a well-formed chain -> `duplicate_payload_ref`; `status` never read | `_is_retired` (same predicate as `links.py:234` / `metrics.py:310-312`); exactly ONE live claimant beside retired ones -> new `retired_claims`; 2+ or 0 live stay `duplicate_payload_ref` |
| return dict | — | `"retired_claims"` added |
| `print_verify_report` [3] block | — | prints `retired_claims (informational, not drift): N` + each `ref: live -> retired` |
| docstring category-3 | chain exemption only | names the retired-claims exemption |

`has_drift`, `_group_by_payload_ref`, `_is_well_formed_chain`,
`load_level3_nodes` and `materialize` are untouched — `retired_claims` is
informational exactly like `version_chains`.

## Red on the pre-fix bytes

`.agi/sessions/iter-EF.88/a00-a871d8d7/red_probe.py` loads the NEW stitch.py
with `_is_retired` neutered to `lambda n: False` (the pre-fix branch has no
status read) and builds a temp project with one live + one deprecated claimant:

```
PRE-FIX  duplicate_payload_ref: {'extensions/agi/bin/foo.py': ['build:bin-foo', 'build:bin-foo-old']}
PRE-FIX  retired_claims: {}
POST-FIX duplicate_payload_ref: {}
POST-FIX retired_claims: {'extensions/agi/bin/foo.py': ['build:bin-foo', 'build:bin-foo-old']}
POST-FIX has_drift: False
```

The committed test `test_verify_one_live_plus_retired_claimant_is_not_duplicate`
asserts `duplicate_payload_ref == {}`; that assertion is red pre-fix and green
post-fix.

## Before/after on the real graph (same worktree, same base)

`.agi/sessions/iter-EF.88/a00-a871d8d7/prepost_probe.py` (pre = neutered):

| category | pre-fix | post-fix |
|---|---|---|
| [1] missing_payload | 18 | 18 |
| [2] orphan_files | 5337 | 5337 |
| [3] duplicate_payload_ref | 1 = `grok_bot_adapter.py` | **0** |
| version_chains | 5 | 5 |
| retired_claims | `{}` | 1 = `grok_bot_adapter.py: build:bin-adapters-grok-bot-adapter -> build:bin-adapters-grok-bot-adapter-a00-fcfbc2f9` |
| [4] stale_contracts (+unreadable) | 93 (+12) | 93 (+12) |
| contracts_not_derived | 8 | 8 |

CLI run (`python3 -B extensions/agi/bin/stitch.py --project .agi --verify`,
~95 s, read-only): `[3] duplicate_payload_ref: 0`, `retired_claims: 1`,
`version_chains: 5`, `[1] 18`, `[4] 93 (+12)` — full output in
`.agi/sessions/iter-EF.88/a00-a871d8d7/verify_post.txt`.

## Tests

`env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_stitch.py extensions/agi/tests/test_level3.py extensions/agi/tests/test_links.py -q`
-> 68 + 78 passed. New guards: two live + one retired and zero live + two
retired stay duplicates; a node moved to `deprecated/` WITHOUT
`status: deprecated` stays a duplicate (the predicate is the status, not the
directory); a well-formed chain with a retired head stays `version_chains`;
`materialize` still writes the live claimant (untouched first-writer-wins);
the CLI report prints the retired claim.

## Production lines

`git diff --numstat -- extensions/agi/bin/stitch.py` -> 29 added / 1 removed
(28 net), ceiling 40. Test file excluded by the measurement rule.

## Agent Notes
stitch.py verify_tree category-3 now judges a non-chain payload_ref group by live claimants: one live + retired -> retired_claims, [3] duplicate_payload_ref 1->0 (grok_bot_adapter.py retired claim), every other verify number unchanged; new test RED on pre-fix bytes; test_stitch/test_level3/test_links 68+78 green; 28 production lines

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
"(1) INSTRUCTION: the parent task reads the kid DIFF, runs one negative probe per claim conjunct itself, and records them as probes:; a kid that passes its own suite but fails the parent probe is lean_disproved. (2) MACHINE: the moved bytes are git diff 417fd95ca2..cfb43205f6: +_is_retired (stitch.py:418) + the non-chain branch at :450-468 + the return-dict key at :569 + the print block at :866-869 + the docstring at :53-61; _group_by_payload_ref, _is_well_formed_chain, has_drift and materialize are byte-identical, and there is exactly one print_verify_report call site (:999). I ran the probes myself: P1-P6 through the load_level3_nodes seam returned the expected branch for every live/retired count and for the active-in-deprecated-directory case; the live CLI wire run (python3 -B stitch.py --project . --verify, exit 0) printed [3]=0, retired_claims=1 for grok_bot_adapter.py and left [1]=18, [2]=5337, version_chains=5, [4]=93(+12) unchanged; the committed new tests are 6-of-7 RED against the base stitch.py by git show in a throwaway copy and 7-of-7 green against the tip in the same harness. (3) NEAR MISS: a fix that put the live/retired split inside _group_by_payload_ref (or at load) would satisfy the prose of the claim and lose the mechanism -- that dict is shared with materialize (:737), so it would drop version_chains 5 -> 0 and flip the 5 chain heads on the publish path; this kid kept the split strictly AFTER _is_well_formed_chain inside verify_tree, which is what P5 checks. (4) DEVIATION: none from the brief."
<!-- THOUGHT:END -->

"PARENT REVIEW (a00-fdcafcb9): accepted proved. The diff 417fd95ca2..cfb43205f6 carries every deliverable the node names -- stitch.py 29+/1- (28 net), 7 new tests in test_stitch.py, and the experiment node itself with a kid-authored title. All 8 parent probes held: the rule fires only at exactly one live claimant; 2+ live, 0 live, and an active claimant sitting in deprecated/ all stay duplicate_payload_ref; a well-formed chain with a retired head stays version_chains; has_drift never sees the new key; the live CLI wire run on the post tip gives [3] 1->0 with grok_bot_adapter.py as the retired claim and every other verify number unchanged; the committed tests are red on the base bytes and green on the tip in my own throwaway harness. caveat: 28 net production lines vs the [hypothesis] schema 10-12-per-conjunct guidance, though inside the brief default 40 ceiling."
