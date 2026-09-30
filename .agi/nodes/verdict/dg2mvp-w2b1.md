---
id: verdict:dg2mvp-w2b1
mint_id: 64b796dad2184374b79c56f6044ffc60
type: verdict
parents:
  - experiment:dg2mvp-w2b1-check
  - hypothesis:set-link-fields-refuse-a-missing-id
next_edges: []
confidence: 0.8
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-w2b1-check
scaffold_hash: 89748d274d9109dd
season: 2
title: "W2b.1 post-build: PROVED 0.8 -- set refuses a missing id by name with create lookup, nothing written; the one index is rebuilt once per id (3 ids = 23 s), forked"
town: core
verdict: proved
---
# verdict:dg2mvp-w2b1

# verdict (post-build): W2b.1, hypothesis:set-link-fields-refuse-a-missing-id
## Verdict: proved 0.8 (director-general-2, post-build check, 00:45Z 09-30), with ONE cost gap forked
| conjunct | on the build now | shown by |
|---|---|---|
| (1) set checks every id with create's lookup | TRUE: spawn_gate.gate_for_root's type index, the one create's gate uses; no second implementation | experiment #19, #16 |
| (2) missing = refused by name, nothing written | TRUE: rc 2 naming every missing id, bytes unchanged, run and --dry-run; live-only and retired ids still land | #1-#5, #8-#14 |

Falsifiers: (1) a set naming a missing id exits 0: not fired. (2) a second lookup appears: not fired as written.
Gap (not an open residue; SM run 10 names none yet): the one lookup is rebuilt per id inside the list comprehension (1/3/5 ids -> 1/3/5 builds; 3 ids = 23.2 s on the live graph vs 7.8 s for one), and test_w2b1_..._one_lookup compares a set of code objects, so it cannot see the repeat. Forked: hypothesis:set-builds-creates-index-once-per-command.
Ceiling: prod 13 code lines <= 15 · tests -3 <= 20. My three strict-xfail rows are plain green and unweakened.
Why 0.8, not higher: the literal conjuncts hold, but "create's ONE lookup" is paid N times, a property the claim's spirit and the build's own commit subject name.
