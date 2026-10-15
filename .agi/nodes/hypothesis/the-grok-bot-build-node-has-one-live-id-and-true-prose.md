---
id: hypothesis:the-grok-bot-build-node-has-one-live-id-and-true-prose
mint_id: db894f5688324c71af3173dc62ca56dc
type: hypothesis
parents:
  - goal:g15.28.3
next_edges: []
assigned: director-engine (leaf goal:g15.28.3, the EF.53 mur residues)
ceiling: "1 kid, graph data only, pi parent (scope, never spend: owner 09-23 14:xZ)"
confidence: 0.7
edited_by: director-engine
scaffold_hash: c302cb4fe66d91ec
season: 2
testable_claim: "After the round the graph has zero duplicate node ids and one payload claim per file: the a00 duplicate of build:bin-adapters-grok-bot-adapter (mint 07acc9ce, .agi/nodes/build/a00-fcfbc2f9-bin-adapters-grok-bot-adapter.md) takes a free id of its own, stops claiming extensions/agi/bin/adapters/grok_bot_adapter.py (payload_ref and link_ref unset; its grid history keeps every prior version) and is retired with status deprecated and a move to .agi/nodes/deprecated/build/ (mint_id unchanged, never git rm, never a supersedes pair), so the loader's duplicate_ids is empty and stitch.py --verify's duplicate_payload_ref drops 1 -> 0 with orphan_files and missing_payload not growing; the canonical (mint 93a56c11) has its stale prose corrected in place through write.py (the pinned SHA-256/line count, the harnesses.grok-bot out-of-scope line vs .agi/config.json:107, the no-reader-flags-duplicates absolute vs loader.py:222-227, dashboard.py:279 and stitch.py:436-444); the a00 node's stale spawn_check_reason and experiment:a00-11ad274b-e6e0c1's proved-over-partial are recorded in their THOUGHTs, never by changing a verdict; links.py links 0 broken, snapshot-goals.py --render --check rc 0, active plus deprecated node count unchanged."
title: "The grok-bot build node has one live id and true prose -- EF.53's dedupe executed, the stale prose corrected (leaf goal:g15.28.3; assigned: director-engine)"
town: core
---
# hypothesis:the-grok-bot-build-node-has-one-live-id-and-true-prose

# hypothesis:the-grok-bot-build-node-has-one-live-id-and-true-prose

**Assigned: director-engine** (leaf goal:g15.28.3; the EF.53 mur residues on my own rounds' grok-bot nodes) · build loop · one `[merge-up]` to thought-master.

## Measured (director-engine, 20:5xZ 09-23, post tip 102658116c)
```
loader        extensions/agi/src/graph_core/loader.py:205-229 load_directory(.agi/nodes): 4144 loaded, duplicate_ids = 1 ->
              build:bin-adapters-grok-bot-adapter KEPT build/a00-fcfbc2f9-bin-adapters-grok-bot-adapter.md (mint 07acc9ce, parent
              mvp:grok-bot-adapter-minimum) · HIDDEN build/bin-adapters-grok-bot-adapter.md (mint 93a56c11, parent mvp:unified-spawn-path,
              the DT.24 canonical carrying the R14#3 THOUGHT)
stitch        stitch.py --project . --verify: [3] duplicate_payload_ref 1 = grok_bot_adapter.py <- both nodes; a retired node is read
              like a live one and still claims its payload_ref (stitch.py:274-279); only a supersedes chain (:374-404) clears it
stale prose   canonical :34 SHA-256 66b7891f.../162 lines -- the live file is 07f2ef7f.../168 (EF.65's +2 moved it again) · :39-41 "not yet
              reachable through config ... Belam's cell ... out of scope" -- .agi/config.json:107 carries harnesses.grok-bot · its THOUGHT's
              "no committed reader flags two live files sharing one id" -- loader.py:222-227 warns + sets graph.duplicate_ids,
              dashboard.py:279 find_duplicate_ids, stitch.py:436-444 duplicate_payload_ref
a00 node      spawn_check_reason "parent id(s) resolve to no node: ['mvp:grok-bot-adapter-minimum']" -- that mvp resolves live
experiment    experiment:a00-11ad274b-e6e0c1 :28 verdict proved beside :15 probes[0] "partial/refused by address"
mur           R-EF53 verify: 4 defects refuted: false + 1 missed; the fix is EF.53's own proposal (the canonical's THOUGHT)
```

## CLAIM
After the round the graph has zero duplicate node ids and one payload claim per file: the a00 duplicate (mint 07acc9ce) takes a free id of its own, stops claiming `extensions/agi/bin/adapters/grok_bot_adapter.py` (payload_ref / link_ref unset -- its grid history keeps every prior version; the canonical still claims the file, so nothing goes orphan) and is retired with `status: deprecated` and a move to `.agi/nodes/deprecated/build/` -- mint_id unchanged, never `git rm`, never a `supersedes:` pair -- so every reader resolves `build:bin-adapters-grok-bot-adapter` to the canonical (mint 93a56c11). The canonical's stale prose is corrected in place through write.py (the pinned hash/line count, the config-row line, the reader-gap absolute); the a00 node's stale spawn_check_reason and the experiment's proved-over-partial are recorded in their THOUGHTs, never by changing a verdict.

## Dispatch line
config-max: none -- graph data only / template-max: none / code: none -- write.py verbs and the sanctioned retire move

## FALSIFIERS
- the loader still reports a duplicate id (or prints its WARN line) after the round
- stitch.py --verify: duplicate_payload_ref not 0, or orphan_files / missing_payload grows by any file
- a node file deleted, a mint_id changed, or active + deprecated node count differs from before
- any reader (stitch.py, level3.py, node_writer.py, zoom.py, links.py) failing to resolve `build:bin-adapters-grok-bot-adapter` or the retired node's new id
- the canonical still asserting a payload hash that does not match its payload
- a verdict / confidence / lean field changed on the experiment

## TESTS
measured, not new code: loader duplicate_ids before/after · stitch.py --project . --verify before/after · links.py links -> 0 broken · snapshot-goals.py --render --check rc 0 · node counts before/after · test_grok_bot_adapter.py green

## FILE SCOPE
.agi/nodes/build/a00-fcfbc2f9-bin-adapters-grok-bot-adapter.md (-> .agi/nodes/deprecated/build/) · .agi/nodes/build/bin-adapters-grok-bot-adapter.md · .agi/nodes/experiment/a00-11ad274b-e6e0c1.md -- every one named in `cli.py done --owns`; nothing under extensions/

## CEILING
1 kid · graph data only · pi parent · scope, never spend (owner 09-23 14:xZ)
