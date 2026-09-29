---
id: doc:card-self-perpetuating
mint_id: 05887a05d0054eee9adcf7d0658dfe2b
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: belam
scaffold_hash: c808a090daec9950
season: 2
title: Card self perpetuating
town: core
---
# doc:card-self-perpetuating

# doc:card-self-perpetuating — self-perpetuating's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (11:1xZ 09-29)
| | |
|---|---|
| post | self-perpetuating · CC session agi-20 |
| stage | council — you embody vision:self-perpetuating ONLY (read it whole first); every review speaks from that vision alone, never alive or all-is-one |
| protocol | doc:council-loop (read it first) · goal:g7.16.1 (the owner's words) |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high · seated 10:3xZ 09-29 by belam |
| sessions | alive agi-8b (@4) · all-is-one agi-96 (@5) · DG1 agi-f8 · DG2 agi-63 · DG3 agi-8f · SM agi-4f — SendMessage; room council-loop for the record |
| skills | agi-node-write · agi-send · agi-workflow · agi-rotate · agi-post |

## §1 Plan
```
done   seated · bundle-1 lens reply · council CONVERGED · goal:g7.16.1.1 built DG1->DG3, SM CLEAN at 80c1c245d · my lens review sent 11:3xZ · park shape settled 11:4xZ
next   alive writes the board line + the bundle-2 draft (park tag first, then grok core simplify); answer it through the lens
then   bundle 2 completes -> batched mur in chunks (alive runs the one council mur) + ONE self-perpetuating lens review
```

## §2 Landed
- bundle 1 lens review (d6cfe7749..80c1c245d): KEEP all 5 rows, 0 red · re-ran falsifier on HEAD: 51 touched tests pass · links 4966/0 broken · render --check 0 · home-path nodes 0 · formation PASS
- next-bundle items accepted into the bundle-2 draft: park = tag `parked:g7.16.2` (goal+hypothesis, schema-declared, one migration commit, count gate) → templates' goals (4 of 6 map "": retire 1/3/4 or g7.16.N) → one formation home (.geometry/formations; doc:council-loop sits in doc/) → first_turn formation line
- count gate CORRECTED: 16 real THOUGHT parks (14 hypothesis + 2 goal, via node_writer.thought_text), not 30 (plain grep hits quotes); the 14 hypotheses have no tags key (not required on [hypothesis])
- risk measured: node_writer.py:1018 replace_thought swaps the whole block, so an honest THOUGHT rewrite un-parks a node silently
- chunk 1 (wf_68d07c15-818): verified _reap_chain callers rotate.py:11741,20805 + heal.py:989,2751 (live in every formation, so reap-chain + model-fence are mis-parked) · 109/372 tracked rotation JSONs carry the home path (the anonymize guard refuses the engine's own records)
- row R item 1 gate (12:0xZ): scrub to the `~` form (all-is-one) + every reader of join.transcript / transcript_path through ONE resolver (rotate.py 2322 3011 3079 6581 6750 7018 7562; only 2322 expands `~`) + a test resolving a scrubbed record's transcript

## 🔴 Where it stops
11:5xZ 09-29 chunk-1 lens sent (row R first: C-rotation → un-park reap-chain+model-fence → generic home regex → small E/B round); waiting on chunk 2 (D A, wf_9b8822db-1e5) + the bundle-2 draft
```
python3 extensions/agi/bin/send.py --from self-perpetuating read self-perpetuating
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN -- <paths>` |
| `send.py read self-perpetuating` exits 2 ('not you: unknown') | pass `--from self-perpetuating` before the verb |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken · `snapshot-goals.py --render --check`

## §6 BANKED
(none)
