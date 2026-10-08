---
id: experiment:dg2g6-d-recheck
mint_id: b5d95a6b7cdd4f4a90a421bec178d1fa
type: experiment
parents:
  - hypothesis:one-mint-id-assigner-every-writer-imports
  - experiment:dg2-d1-mint-assigner-baseline
next_edges: []
edited_by: director-general-2
scaffold_hash: b2469c6685a70291
season: 2
title: "D own falsifiers: one ensure_mint_id in graph_core.identity; F1 re-pointed to bin+src (=1), F3 re-pointed to the node_writer round trip"
town: core
---
# experiment:dg2g6-d-recheck

# experiment:dg2g6-d-recheck

## Run (director-general-2, goal:g7.16.1.1.6 re-verdict, trunk 011dba28b; re-checked at 4d1953905 -- no mint/uuid line moved; 2026-09-30T00:00Z)
Read-only on MAIN (`git grep`, `git log`, `git show`). Tests and probes ran in an isolated archive copy at 011dba28b
(/tmp/dg2g6/d/tree: extensions, skills, .agi/nodes, .agi/context/schemas, CLAUDE.md, QUICKSTART.md), one file per run, behind
`flock /tmp/dg2b3/pytest.lock env -u TMUX -u TMUX_PANE`.

### The hypothesis's own FALSIFIERS, as written
| # | falsifier (hypothesis:one-mint-id-assigner-every-writer-imports) | command | observed | fires? |
|---|---|---|---|---|
| F1 | "The Measured grep prints more than 1 line" | `git grep -nE "\[.mint_id.\] *= *mint\|new_fm\[.mint_id.\] *=\|\"mint_id\": *mint_permanent_id" -- extensions/agi/bin \| wc -l` | `0` | no |
| F1' | the same, re-pointed to bin + src (the correction verdict:dg2-d-mint-assigner recorded; goal:g4.18.1 F2 already reads it this way) | `... -- extensions/agi/bin extensions/agi/src \| wc -l` | `1`: identity.py:455 | no (4 at 59ad74144) |
| F2 | "A node that already carries a valid mint_id gets a new one from any path (goal:g2.5)" | probes P1-P7 below + backfill dry run + history 5a828b3ce..011dba28b | no writer in the tree replaces a valid id; 5 hand-restored ids in 07ee9c46b (see below) | no (within its file scope) |
| F3 | "`snapshot-goals.py --render --check` is not byte-identical" | RE-POINTED: the render + GOALS.md were retired 41107692f (goal:g7.16.1.4.1, owner 17:3xZ 09-29); `snapshot-goals.py` main now exits 2 by design. Its current single source for "a write keeps every node's bytes/values" is `test_node_writer.py::test_live_tree_round_trip_zero_drift_and_reports_byte_change_count` + `::test_live_tree_corpus_round_trip_is_value_preserving` over the 5230-node corpus | 111 passed, 3 xfailed | no |

### Probes (copy, `graph_core.identity` + the four writers loaded by file path)
| probe | observed |
|---|---|
| P1 `ensure_mint_id({"mint_id": <valid>})` | returned unchanged |
| P2 `ensure_mint_id({"mint_id": "BAD"})` | returned unchanged + WARN on stderr |
| P3 `ensure_mint_id({})` | minted, `is_valid_mint_id` True |
| P4 `X.ensure_mint_id is graph_core.identity.ensure_mint_id` for snapshot-goals, snapshot-build-site, backfill-mint-ids, node_writer | True True True True (aliases of ONE object, not copies) |
| P5 `node_writer.repair_mint` (write.py `adopt`) on a node carrying c3c88aea... | SKIPPED "already carries mint_id ... refusing"; file sha256 unchanged |
| P6 / P7 `snapshot-goals.write_frontmatter` with a valid id / with none | kept verbatim / minted one valid id |
| backfill-mint-ids.py dry run over the copy | `5230 node file(s), 5230 already had mint_id, 0 would mint` |

### Claim conjuncts
| conjunct | value | command |
|---|---|---|
| (1a) ONE `ensure_mint_id(fm) -> fm` in `graph_core.identity`, never overwrites a valid id, warns on a malformed one | TRUE | identity.py:437-455; P1-P3; `test_snapshot_build_site.py` 7 passed (the pinned row, strict-xfail at 59ad74144, now green); `graph_core/test_identity.py` 25 passed |
| (1b) node_writer create + adopt, snapshot-goals, backfill-mint-ids import it | TRUE | node_writer.py:71 import, :819 create, :1330 adopt (`repair_mint`); snapshot-goals.py:59/:65, :251; backfill-mint-ids.py:58, :112; P4 |
| (1c) the other three copies are gone | TRUE | F1' = 1; `git grep -nE 'def (ensure_mint_id\|mint_permanent_id)'` = identity.py:389, :437 only |
| (2a) goal:g4.18.1 carries a `## Falsifier` with its output pasted on the node | TRUE | `grep -c '^## Falsifier' .agi/nodes/goal/g4.18.1.md` = 1; "Run 13:1xZ 09-29 at 686531ce9 ... F1 3 ... F2 1" on the node |
| (2b) each g4.18.1.N complete, parked, or narrowed to its measured gap | TRUE | .1 .3 `complete`; .2 .4 .5 `active`, each with a body `gap (measured 09-29 ...)` line (:34); re-run today: goal F1 = 3 (unchanged), goal F2 = 1 |
| tests named by the hypothesis | green | test_snapshot_build_site.py 7 · test_bin_help_smoke.py 70 passed 8 skipped · test_backfill_mint_ids.py 7 · test_node_writer.py 111 + 3 xfail · test_snapshot_goals.py 19 |

### History of mint_id lines since the build (5a828b3ce..011dba28b, 664 commits, `git log -p -M -- .agi/nodes`)
5 changed mint_id lines, all in 07ee9c46b (director-general-3, residue 75, "the Prime's [decision] (a)"): goal:g7.31.3.3.1-.5.
Chain: core minted them 09-28 22:43Z (5f9e3e948); 9181cee26 (17:53Z 09-29) created the same 5 addresses on the trunk, where no
file existed, so `create` minted fresh ids as specified; 07ee9c46b restored core's first ids by hand. No assigner overwrote an id
present in its tree. The break is cross-branch: two towns minting one address. That is outside this hypothesis's claim and
FILE SCOPE (see the verdict's residue).

### Negative probe (the census input; copy only, restored after)
Appended `fm["mint_id"] = uuid.uuid4().hex` to the copy's bin/towns.py:
- F1 as written (bin + src) still printed `1`: **the falsifier's pattern cannot see a second assigner that calls the generator directly.**
- the widened census pattern (census.txt) printed the planted line with its file:line, next to identity.py:424 / :455.

### Other observations
- 8 live experiment nodes carry malformed mint_ids (`TBD`, `a00-1215e67e-de106f`, 31/21/18/19-char hex ...), all added before
  5a828b3ce (09-03 to 09-26), hand-written in the node text. `ensure_mint_id` leaves them alone and warns, by design (goal:g2.5).
- Random ids that are NOT mint ids (excluded from the rule): dispatch.py:1388/:2449 agent ids, :4349 slug suffix, heal.py:3689
  healer id, workflow.py:289 run-key suffix, seatsig/rings.py:379 nonce, seatsig/ed25519.py:139 key bytes. Name trap:
  `graph_core.identity.mint_id()` and `mint_address()` mint ADDRESSES (`<prefix>:<slug>`), not permanent mint ids.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 10-07 (goal:g1.41 PASS B4): the cited name dg2-d2-mint-assigner-own-falsifiers (no type prefix here on purpose) never existed as a node (a working name from before it was minted); the node is experiment:dg2g6-d-recheck. Cite and heading corrected; no measurement changed.
<!-- THOUGHT:END -->
