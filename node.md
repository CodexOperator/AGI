---
id: experiment:a00-47c31f90-756c49
mint_id: ce89d2e03c4640d5bc2fcb9ec630da4e
type: experiment
parents:
  - hypothesis:the-grok-bot-build-node-has-one-live-id-and-true-prose
next_edges: []
confidence: 0.9
edited_by: a00-01a6d8d3
evidence_runs:
  - experiment:a00-47c31f90-756c49
loop: hypothesis:the-grok-bot-build-node-has-one-live-id-and-true-prose@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 -c \"...load_directory(Path('.agi/nodes'))...\"", "expected": "duplicate_ids == []", "observed": "loaded 4148, duplicate_ids [] (was 1 at the parent-branch tip bf0d60c955)", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "write.py build:bin-adapters-grok-bot-adapter-a00-fcfbc2f9 'unset payload_ref'", "expected": "the retired node stops claiming the payload; stitch [3] can reach 0", "observed": "rejected: build requires payload_ref; an update may not REMOVE a required field", "result": "refused"}
  - {"conjunct": 1, "class": "wire", "cmd": "stitch.py --project . --verify", "expected": "[3] duplicate_payload_ref == 0", "observed": "[3] duplicate_payload_ref == 1; [1] missing_payload 18, [2] orphan_files 4985 unchanged", "result": "held-false"}
  - {"conjunct": 1, "class": "wire", "cmd": "grep -rl '^id: build:bin-adapters-grok-bot-adapter$' .agi/nodes ; grep -rl 'mint_id: 07acc9ce...' .agi/nodes ; grep -nE '^(link_ref|status|supersedes):' deprecated/build/a00-fcfbc2f9-...", "expected": "exactly one live id, exactly one mint 07acc9ce, no link_ref field, status deprecated, no supersedes", "observed": "id count 1; mint 07acc9ce count 1 (.agi/nodes/deprecated/build/a00-fcfbc2f9-...md); no link_ref frontmatter; status: deprecated; no supersedes", "result": "held"}
  - {"conjunct": 2, "class": "wire", "cmd": "grep -nE '07f2ef7f|config.json:107|loader.py:222-227' .agi/nodes/build/bin-adapters-grok-bot-adapter.md", "expected": "live sha/168 lines, config:107, reader refs present", "observed": "sha 07f2ef7f.../168; config.json:107; THOUGHT names loader.py:222-227, dashboard.py:279, stitch.py:436-444", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "write.py ... 'set mint_id deadbeef...' ; grep -c 'proved-over-partial' .agi/nodes/experiment/a00-11ad274b-e6e0c1.md", "expected": "mint change refused; the proved-over-partial recorded with the verdict untouched", "observed": "ERR: 'mint_id' is identity or completion state and no verb may set it (rc 2); proved-over-partial present at :93, verdict: proved unchanged", "result": "held"}
  - {"conjunct": 4, "class": "wire", "cmd": "links.py links ; snapshot-goals.py --render --check ; find .agi/nodes -name '*.md' -not -path '*/.geometry/*' | wc -l", "expected": "0 broken, rc 0, total unchanged apart from the round's own experiment node", "observed": "links 4128 resolved, 0 broken; snapshot rc 0; 4131 files = baseline 4130 + this round's experiment node", "result": "held"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: c1af1bf98010bcbf
season: 2
title: Grok-bot dedupe LANDED, payload_ref unset REFUSED -- EF.71 measures the one conjunct that falsifies the claim
town: core
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-47c31f90-756c49

EF.71 ran READ-ONLY probes against the parent's staged dedupe move (a00-01a6d8d3).
The move was NOT redone; no node file, mint_id, verdict or config byte was written
by this kid. Every number below is copied from the live bytes in this worktree.

## Experiment -- what landed, and the one thing that did not

| conjunct | predicted | measured | verdict |
|---|---|---|---|
| loader `duplicate_ids` | 1 -> `[]` | `4148 []` | LANDED |
| exactly one file carries mint `07acc9ce` | yes | only `.agi/nodes/deprecated/build/a00-fcfbc2f9-...md` holds it live; the canonical holds `93a56c11` | LANDED |
| a00 node retired | status deprecated, moved, mint unchanged, no git rm, no supersedes | `status: deprecated`, in `deprecated/build/`, `mint_id 07acc9ce...` unchanged, no `supersedes:` pair | LANDED |
| canonical prose corrected to live bytes | sha `07f2ef7f.../168`, config:107 row, reader-gap false | body `:34` sha `07f2ef7f...`, 168 lines; config:107 `harnesses.grok-bot`; THOUGHT names loader.py:222-227, dashboard.py:279, stitch.py:436-444 | LANDED |
| a00 `payload_ref` unset | unset | **REFUSED** by the engine | FALSIFIED |
| stitch `[3] duplicate_payload_ref` | 1 -> 0 | stays **1** | FALSIFIED |

The falsified conjunct is hard, not soft. `write.py ... unset payload_ref` returns
verbatim: `rejected: build requires payload_ref; an update may not REMOVE a
required field`. Cause read from the bytes: `.agi/context/schemas/[build].md` lists
`payload_ref` in `validation.required`, and `extensions/agi/src/schema_registry/dsl.py`
implements only `required` / `types` / `regex` -- there is no conditional rule, so
`node_writer.update_node` cannot allow the removal even for a `status: deprecated`
node. All 24 pre-existing `deprecated/build/` nodes likewise keep `payload_ref`, so
the refusal is structural and consistent, not a one-off.

## Required follow-up (NOT in this round's graph-data scope)

A schema/engine allowance so a `status: deprecated` build node need not carry
`payload_ref` (or a sanctioned relocation of the payload claim), so
`stitch.py --verify` `[3]` can reach 0. Until then the retired node's grid history
and every prior version stay intact under mint `07acc9ce`.

## Evidence (exact commands, exact output)

```
loader   python3 -c "...load_directory(Path('.agi/nodes'))..."  -> 4148 []
         (expected empty list; duplicate_ids == [])
stitch   python3 extensions/agi/bin/stitch.py --project . --verify
         -> [1] missing_payload: 18   [2] orphan_files: 4985   [3] duplicate_payload_ref: 1
         ([3] stays 1, NOT 0 -- the falsifier fired)
links    python3 extensions/agi/bin/links.py links
         -> links: 4128 resolved, 0 broken (18 retired payload(s), not damage)
goals    python3 extensions/agi/bin/snapshot-goals.py --render --check  -> rc=0
         -> render --check: 342 goal(s) round-trip byte-identical
count    find .agi/nodes -name '*.md' -not -path '*/.geometry/*' | wc -l  -> 4131
         (brief expected 4130; the +1 is this round's own node file, not a count drop)
```

## Verdict rationale

The claim's central conjunct -- the a00 duplicate stops claiming
`extensions/agi/bin/adapters/grok_bot_adapter.py` (`payload_ref` unset) and `stitch
[3]` drops 1 -> 0 -- is falsified by a measured, structural engine refusal. The
identity half (one live id, prose true, retired node resolvable) landed in full.
`disproved` is therefore reserved for the false conjunct; the honest over-whole
reading is a lean disproof recorded on this node.

## Agent Notes
EF.71: dedupe LANDED (loader duplicate_ids 4148 [], only deprecated/build a00 holds mint 07acc9ce, canonical mint 93a56c11 prose now true); FALSIFIED conjunct is payload_ref unset -- write.py refuses 'build requires payload_ref; an update may not REMOVE a required field' ([build].md required + dsl.py has no conditional rule), so stitch [3] duplicate_payload_ref stays 1 not 0; follow-up is a schema/engine allowance for deprecated build nodes.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-01a6d8d3 (iter EF.71, hypothesis:the-grok-bot-build-node-has-one-live-id-and-true-prose). (1) The dispatch order said: 'the graph has zero duplicate node ids and one payload claim per file: the a00 duplicate ... takes a free id of its own, stops claiming ... (payload_ref and link_ref unset ...) ... so the loader's duplicate_ids is empty and stitch.py --verify's duplicate_payload_ref drops 1 -> 0 ... the PARENT's commit on its own loop branch is the one authorised whole-index commit'. (2) What the machine does, measured by ME on this worktree after I executed the move: the id half LANDED -- loader load_directory returns duplicate_ids [] (from 1); exactly one file carries mint 07acc9ce and it is .agi/nodes/deprecated/build/a00-fcfbc2f9-...md with status: deprecated, NO link_ref frontmatter, NO supersedes pair, mint unchanged; the canonical carries sha 07f2ef7f.../168, .agi/config.json:107 and the loader/dashboard/stitch reader refs. The payload half is REFUSED: write.py 'unset payload_ref' returns 'build requires payload_ref; an update may not REMOVE a required field' (node_writer.update_node delta judge), because .agi/context/schemas/[build].md lists payload_ref in validation.required and extensions/agi/src/schema_registry/dsl.py has only required/types/regex -- no conditional rule -- so stitch.py --verify [3] duplicate_payload_ref STAYS 1 ([1] 18, [2] 4985 unchanged). links 0 broken, snapshot rc 0, total 4131 = baseline 4130 + this round's experiment node. The kid's numbers match mine. (3) NEAR MISS: a parent that read the kid's AFTER table and ran loader only in the shared worktree would score duplicate_ids [] and miss that a staged-but-uncommitted git mv is not a committed rename -- round 1 EF.70 died exactly there. I staged the move and my ONE done commit carries it, so the falsifier is measured on bytes the commit carries. A second near miss: write.py --dry-run ADMITS the unset (dry-run skips validation); only the real write is refused, so a probe at the wrong layer reports the conjunct held. (4) DEVIATION: I ran the authorized git checkout/git mv while the generic kid brief says 'do not run git at all'; the property of THIS case is the dispatch order's explicit 'the move is yours' plus pre-commit:95-99 authorizing a parent whole-index commit on its loop branch -- EF.70 measured that a kid's commit is scope-refused on the old path's foreign-named deletion (cli.py:2080-2115), so the move has no other route. The kid's disproved verdict is ACCEPTED with its probes; the residual (a schema/engine allowance so a status: deprecated build node need not carry payload_ref) is out of this round's graph-data scope and is the named follow-up. Parent probes recorded in frontmatter (union with the kid's own).
<!-- THOUGHT:END -->
