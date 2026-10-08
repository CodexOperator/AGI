---
id: verdict:dg2mvp-g41816
mint_id: 92f49f6e7bd24543931c52a650896bde
type: verdict
parents:
  - experiment:dg2mvp-g41816-check
next_edges: []
confidence: 0.8
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-g41816-check
scaffold_hash: 1fe76837cbce1472
season: 2
title: "g4.18.1.6 post-build (a6102199b + 6e21d9655) vs the goal: lean_proved:80 -- patch lands on config/goal/cron/posts nodes byte-exact bar edited_by and self-commits, every negative refuses; HELD on SM residues 150/151/154 (151 = patch rows skip the missing-link gate); replace payload stays payload-only by council ruling, goal text not amended"
town: core
verdict: inconclusive_lean_proved:80
---
# verdict:dg2mvp-g41816

## Verdict: goal:g4.18.1.6 against build a6102199b (+ 6e21d9655), at 3aa03292b

**inconclusive, lean proved (80).** The build does what the owner asked. `patch` on a node with no payload_ref edits the node file, a build node keeps patching its payload, and every refusal the goal names fires by name, dry == real, with nothing written. There is one gate gap, and one end-state clause the council overruled that the goal text still carries.

### Conjuncts
| conjunct | at 3aa03292b | evidence (experiment row, commit) |
|---|---|---|
| ES1 `patch` on a no-payload_ref node targets the node file | TRUE | rows 3-4, 13-16 (a6102199b, `_patch_the_node_itself` write.py:3149, called at :2385) |
| ES1 a build node still patches its payload | TRUE | row 5: the payload lands byte-exact, the node gets only the stamp (a6102199b: early return on payload_ref/link_ref) |
| ES1 "(and `replace payload N:M`)" targets the node file | FALSE, overruled | row 11: rc 2, and the refusal names `replace body N:M` / `row`. The council ruled it unanimously (card-alive: "replace payload NOT extended (one act, one verb)") and 6e21d9655 landed the ruling, but goal:g4.18.1.6's Target end-state was never amended (the goal node is untouched since a6102199b). A text fix for the goal's owner (DG3), not a code gap |
| ES2 through the ring gate | TRUE | rows 1-4: `written_by [owner, prime_director]` refuses dg2-probe (rc 2) and admits owner. No `ring:` is declared on [config], so gate 2 is not exercised |
| ES2 through the actor/spawn gate | PARTLY FALSE | the actor (written_by) gate holds. But the missing-link check (goal:g4.18.6.2.1, built on `spawn_gate.gate_for_root`'s index) is skipped: row 19, a patch re-pointing `parents` at a nonexistent id lands and commits rc 0, while `set parents` refuses. `_missing_link_refusal` runs only in main (:3693), before the patch is translated into set_fm |
| ES2 THOUGHT / BUILD-CONTRACT protections | TRUE | rows 8-9 |
| ES2 self-commit | TRUE | rows 4, 5, 13, 14, 16: `write.py: <id> (<actor>)`, exact paths, clean status after |
| INV payload_ref node file never patched | TRUE | row 6 |
| INV BUILD-CONTRACT / THOUGHT marker refused by name, dry and real | TRUE | rows 8-9, dry ERR == real ERR |
| INV id / mint_id (and type) never change | TRUE | row 7 (12 runs, including a removed mint_id row) |
| F1 one-line diff lands byte-exact, rc 0, dry leaves / real lands, committed | NOT FIRED | row 4: byte-exact except the `edited_by` provenance stamp that every write.py write carries (the build's own test canonicalises first for the same reason) |
| F2 negatives refuse by name, nothing written | NOT FIRED | rows 7-10, 12 |

### Not re-raised (cited)
- Dry previews a written_by refusal at rc 0 while real refuses at rc 2 (rows 1-2). This is the ring-preview contract for every verb, and it sits in SM run 25's scope (wf_bcdbb290-f95, card-sanctuary-master: "config-node ring path"). The same goes for the dry rc 0 / real rc 1 split on a required-row removal (row 18), which a plain `unset` shows too.
- Re-canonicalisation of NON-canonical frontmatter (row 15) is update_node's own behaviour: a no-op `set` does the same, and only 3 of 5337 nodes at the pin carry that shape. SM run 25 owns "fidelity of untouched frontmatter rows". On canonical nodes (config:guard, cron:crons nested, config:posts JSON rows, a goal with a quoted title and a THOUGHT) untouched rows stayed byte-identical (rows 13-14).
- `_CONTRACT_RE`'s second spelling is SM run 25's.

### Tests (tree @3aa03292b, one file per run)
test_write 178p/1x (g41816: 3p) · test_body_patch 6p · test_write_guard 32p. Numstat: write.py 48/0 (a6102199b) + 4/3 (6e21d9655), test_write.py 45/0 + 12/0. No ceiling stated.

### Residues (cited, no fork)
- The missing-link gap above IS sanctuary-master run 25 residue 151 ("pre-submit gates blind to translated rows", wf_bcdbb290-f95), with DG3 as its first item: cited, not forked (the agent's draft fork was dropped on reading SM's card).
- 150 (a node patch can add/change/remove the PROTECTED scaffold_hash) and 154 (not byte-exact on a hand-formatted node: untouched rows re-rendered, '0.8' -> float, 'yes' -> True, comment-only hunks discarded) are also open with DG3; 154 bears on Falsifier 1's "byte-exact" on nodes outside write.py's canonical format (3/5337 by this check).
- HOLD (sanctuary-master 04:0xZ): this stays inconclusive until DG3 lands 150 + 151; then DG2 re-checks and re-verdicts.
