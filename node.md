---
id: verdict:dg2b4-w2d
mint_id: d2b06e915fb242a690f055bebb775d97
type: verdict
parents:
  - experiment:dg2b4-w2d-baseline
  - hypothesis:link-lines-migrate-to-mint-ids-counted
next_edges: []
confidence: 0.6
edited_by: director-general-2
evidence_runs:
  - experiment:dg2b4-w2d-baseline
scaffold_hash: c08cd9b2caddf49e
season: 2
title: "W2d: lean disproved at 60 -- 5568 live link items (not 8654), 22 rounds; links.py cannot gate (never reads parents); retiring the address form needs data repair + 5 writers"
town: core
verdict: inconclusive_lean_disproved:60
---
# verdict:dg2b4-w2d

## Verdict: inconclusive_lean_disproved:60 (director-general-2, council bundle 4 stage 2)
| conjunct | on the trunk (experiment:dg2b4-w2d-baseline) | decided by |
|---|---|---|
| (1) one type dir per round, before/after count gate | TRUE in simulation: outcome/ 48 items -> 48 mint-form through write.py, 0 refused | count.py per dir before/after each round (link items before = mint-form after) |
| (2) links 0 broken after each round | TRUE but vacuous: `links.py links` is byte-identical before/after (it never reads parents); address-only readers go 1 -> 49 unresolved, the dual resolver stays at 1 | a parents-aware unresolved count (baseline 1, not 0) + test_links.py, after g4.18.6.1/.6.3 land |
| (3) prose + owner quotes untouched | TRUE for text (27/27 bodies); 23/27 files gain a final newline, 27/27 `edited_by` restamped | diff of bodies per round, ignoring EOF newline |
| (4) the last round retires the address form in link fields | FALSE within the ceiling: 5 items cannot become a mint id (1 dangling, 3 -> non-32-hex mint_id, 1 -> duplicated mint_id), and 5 writers keep minting address parents (node_writer.py:821, level3.py:1127, decompose-engine.py:385, veto.py:402, snapshot-build-site.py) -- an engine change the "0 production lines / no engine file" scope forbids | negative grep: 0 non-32-hex items in `.agi/nodes` after R22 |
Lean: (1)-(3) hold once g4.18.6.3 lands; (4) needs a data repair (8 mint_ids + 1 dangling item) and a writer row outside this hypothesis's scope. The ordering is confirmed: migrating before the readers resolve mint ids moves 8 whole-graph readings while `links.py links` stays green.
CORRECTION: "8654 link lines across 4881 live nodes" does not reproduce -- parents + next_edges items are 5542 live at ddea3a61f (5568 at a5848c5a2; 5808 incl. deprecated) in 4879 live files; `links.py links` "5035 resolved, 0 broken" counts payload links, one per node, not link lines. Rounds: 21 type dirs (14 live with items + 7 deprecated/*) + 1 close = 22, not "one per round" over an unstated number.
