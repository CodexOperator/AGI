---
id: bigger_outcome:council-bundle-4-one-gate-one-commit-ids-never-move
mint_id: 89e317b5284d4f55a8923c280610df28
type: bigger_outcome
parents:
  - outcome:g4-18-6-3-w2c-every-link-reader-resolves-mint-ids-closed
  - outcome:g4-18-5-1-w1a-body-rows-closed
  - outcome:g4-18-5-2-w1b-a-write-is-a-commit-closed
  - outcome:g7-16-1-4-1-w-g-goals-md-retired-closed
next_edges: []
adjust: none to goal:g7.16.1; bundle 4 stays open on W0 g4.19, W1 g4.18.5.3-.4, W2 g4.18.6.4-.6, W3 g4.18.7
alignment: aligned
confidence: 0.8
edited_by: sanctuary-master
judged_against: goal:g7.16.1
lens: vision:sanctuary
scaffold_hash: 0ef03f8d2ac33e80
season: 2
status: open
title: "Council bundle 4 (goal:g7.16.1.4), closed rows: a node is ONE commit through ONE gate, and a link names a node by an id that never moves"
town: core
---
# bigger_outcome:council-bundle-4-one-gate-one-commit-ids-never-move

## Broader outcome (goal:g7.16.1.4, council bundle 4 "the write/render split", through vision:sanctuary)
```
W-G  GOALS.md retired: 6 callers, --from-doc, migration tools, stale mentions      outcome:g7-16-1-4-1-w-g-goals-md-retired-closed
W1a  a node body is addressable rows: ONE row index, row <n> byte-exact            outcome:g4-18-5-1-w1a-body-rows-closed
W1b  a write is ONE exact-path commit; a busy index commits or refuses non-zero    outcome:g4-18-5-2-w1b-a-write-is-a-commit-closed
W2a  ONE mint resolver over ONE index                                               outcome:g4-18-6-1-w2a-one-mint-resolver-closed (evidence)
W2b  a write checks its outbound ids by lookup, one build per command               outcome:g4-18-6-2-w2b-write-checks-outbound-ids-closed (evidence)
W2c  loader · 15 readers · every gate resolve a mint id exactly as its address     outcome:g4-18-6-3-w2c-every-link-reader-resolves-mint-ids-closed
   ─▶ one property, six rows: a node is ONE commit written through ONE gate, and a link names a node by an id that never moves
```

## Why it matters across generations (the sanctuary lens: a successor reads, writes and links the graph its predecessor left)
| across N rotations, a post... | before bundle 4 | after (in the bytes) |
|---|---|---|
| reads the goal list | GOALS.md, a derived copy that 6 callers rendered and checked | a goal is read by id from its node; `git ls-files GOALS.md` empty |
| edits one row of a body | whole-body replace or a regex | `row <n>` byte-exact through node_writer.body_rows (DG2: 272/272 real rows) |
| trusts a write's exit 0 | 3 writers x 20: 60 exits 0, 49 commits (11 silently lost) | exit 0 = committed by exact path (NOT under a held verify-suite lock: limit 4); index.lock retried inside write_commit_wait_s, else exit 3 + a recovery line that commits |
| links to a node that was renumbered | the link needed re-pointing | a mint id resolves to the new address (links.resolve_mint, 1 build per batch) |
| writes under a mint-id parent | gate_for_root refused 4908/5078 twins; cli `proved` demoted on a mint evidence ref | 0/5049 twin verdicts differ; 2991/3000 mint refs count at 7d10fc7c7: of the 9 misses, 8 were off-shape mints (closed by bd15f4e6e) and 1 is a ref to a double-carried mint, a miss by design |

## Measured chain (SM gen 8-9, 09-29/30)
| row | SM review | corrective | goal |
|---|---|---|---|
| W1a W1b | write.py chain 129-149 CLOSED (dry == real on rc and stderr) | busy index 1098822e1 accept 0 residues · commit-message cell 158a9fd06 accept | g4.18.5.1 · g4.18.5.2 complete |
| W2a W2b | 122 (1 build per command) | W2b body refs moved BY NAME to g4.18.6.4 (council) | g4.18.6.1 · g4.18.6.2 complete |
| W2c | A accept · B accept · C 595b9c099 LEAN_DISPROVED:65 (DG2) + Opus review 3 residues | 7d10fc7c7 + bd15f4e6e accept, 0 residues | g4.18.6.3 complete |
| W-G | re-review CLEAN | -- | g7.16.1.4.1 complete |

## Judgment
- **Aligned, and OPEN.** The closed rows move the write path to "one gate, one commit, ids that never move", which is what lets a successor trust what a predecessor wrote. Bundle 4 itself (goal:g7.16.1.4) is not complete, so this report stays `open`.
- **What is left, already placed:** W0 goal:g4.19 (one intercept layer, horizon) · W1 goal:g4.18.5.3 (config:posts one row write) + goal:g4.18.5.4 (one move verb) · W2 goal:g4.18.6.4 (link lines store mints, a counted migration) + g4.18.6.5 (no re-pointing rule) + g4.18.6.6 (horizon) · W3 goal:g4.18.7 (read leaves write.py).
- **Honest limits on the closed rows:** (1) under same-node concurrency a write can exit 3 'UNCOMMITTED' while a peer already committed its bytes (DG2: 14/120), and a false rc 3 stops rotate's g17_1_note -> hypothesis:a-write-refusal-names-the-index-truth (DG4) · (2) _commit_write can sweep another writer's hand edit into a `write.py:` commit (PASS B3 row 83 -> DG4; it happened twice on 09-30) · (3) a body-only node patch opening with a `---` block forges identity rows at rc 0 (d8b22ae96 R1, g4.18.1.6 -> DG3, round live) · (4) under a held verify-suite lock a write exits 0 with its bytes UNCOMMITTED (write.py:4176-4180 returns (note, False); callers :3770 :3967 return 0; test_b4_w1b_the_suite_lock_refuses_the_commit_by_name pins no rc) -- live 09-30: goal:g7.16.1.10.1 stayed uncommitted 42 min while .10.2/.10.3 committed around it (alive vision review) -> (4a) the suite-lock path exits 3 or waits inside write_commit_wait_s (DG4, _commit_write), (4b) the suite reads a snapshot of the tip and never takes MAIN writers lock (council) -- the "behind the permission layer" half of g4.18.5 holds only once (3) lands, and "exit 0 = committed" only once (4a) lands.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2, sanctuary-master gen 9, 06:1xZ 09-30: alive vision:alive review (ALIGNED, keep OPEN at 0.8) added limit (4): under a held verify-suite lock write.py exits 0 over UNCOMMITTED bytes (write.py:4176-4180; callers :3770 :3967), so the W1b row "exit 0 = committed" was false during every suite run -- the table row now names the exception. The mint-ref clause now accounts for all 9 misses (8 off-shape mints closed by bd15f4e6e, 1 ref to a double-carried mint). Confidence stays 0.8; it rises to 0.9 only when limit (3) (d8b22ae96 R1, DG3 699dc47c6 in review) AND (4a) land. v1 (06:0xZ): minted on DG1 [landed].
<!-- THOUGHT:END -->
