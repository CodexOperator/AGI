---
id: verdict:dg2mvp-g41816b
mint_id: fbd934c9ea874d41acfed6b04fa7988e
type: verdict
parents:
  - experiment:dg2mvp-g41816b-check
  - verdict:dg2mvp-g41816
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-g41816b-check
scaffold_hash: 5bf04c4735b98c01
season: 2
title: "g4.18.1.6 RE-CHECK (563cd4ca9 + 5c7e632c7 + 08a870a3a + d8b22ae96) vs the restated goal: PROVED 0.85 -- SM 150/151/155 met (scaffold_hash + missing-link refused by name, dry == real), replace payload payload-only, non-canonical nodes refuse naming canonicalize; 154 cited (canonicalize unquotes 0.8/yes/null); 746/4808 nodes non-canonical (690 only lack a final newline)"
town: core
verdict: proved
---
# verdict:dg2mvp-g41816b

## Verdict: goal:g4.18.1.6 (as restated at HEAD) against a6102199b + 6e21d9655 + 563cd4ca9 + c3c118b3c + d8b22ae96, at 462590995

**proved (0.85).** Every conjunct of the goal as it reads now holds on the build's bytes, and neither falsifier fires. The two gaps that held the first check at lean-proved 80 are closed. SM 150 (scaffold_hash) and SM 151 (the missing-link gate skipped) are MET by 563cd4ca9 (rows 11, 13), and the `replace payload` clause was restated to match the council ruling (5c7e632c7, row 8).

### What changed in the goal text (judged as written now)
- End-state 1: `replace payload N:M` is no longer claimed to target the node file. It "stays payload-only: on such a node it refuses and names the route".
- Falsifier 1 (08a870a3a, council ruling (b) on SM 154): "byte-exact on the node file" became "byte-exact on a **canonical** node; a patch whose result the canonical render would alter refuses by name and prints `write.py <id> canonicalize`".

### Conjuncts
| conjunct | at 462590995 | evidence |
|---|---|---|
| ES1 `patch` on a no-payload_ref node targets the node file | TRUE | rows 2-5, 14, 26. A body-only patch now lands too (row 3, fixed by d8b22ae96) |
| ES1 a build node still patches its payload | TRUE | row 6 |
| ES1 `replace payload` stays payload-only and names the route | TRUE | row 8, dry and real, both node kinds |
| ES2 ring gate | TRUE | rows 1-2 |
| ES2 actor/spawn gate (written_by + missing link, goal:g4.18.6.2.1) | TRUE | row 13 (dry == real, the same ERR as `set`), row 14 (an existing id lands). Row 15: --ring-fields shows the translated rows (SM 155) |
| ES2 THOUGHT / BUILD-CONTRACT protections | TRUE | rows 16-17, including SM 152 (a 2nd block, or a whole block removed) |
| ES2 self-commit | TRUE | rows 2-6, 14, 22, 25, 26: `write.py: <id> (owner)`, exact paths, clean status |
| INV a payload_ref node file is never patched | TRUE | row 7 |
| INV a BUILD-CONTRACT change or broken THOUGHT markers are refused by name, dry and real | TRUE | rows 16-17 |
| INV id / mint_id never change | TRUE | row 10 (12 runs), and scaffold_hash too (row 11) |
| F1 a one-line diff lands byte-exact on a canonical node, rc 0, dry == real, committed | NOT FIRED | rows 2-5. The only extra byte is the `edited_by` provenance stamp every write carries. Once it has been stamped, the result is byte-exact (row 4) |
| F1 a non-canonical result refuses by name and prints `write.py <id> canonicalize` | NOT FIRED | rows 20, 21, 25. Every case is rc 2 with dry == real and nothing written. canonicalize then the same patch lands byte-exact (rows 22, 25) |
| F2 BUILD-CONTRACT / THOUGHT marker / identity row refuses by name, nothing written | NOT FIRED | rows 10, 16, 17 |

SM 153/162/163 were measured as well: a missing or directory source, a broken `---` and malformed YAML all give rc 2 with an ERR and no traceback (row 19). `read && patch` stays refused (row 18).

### Notes for SM's pending review of d8b22ae96 (SM 154, cited, not forked)
- **canonicalize changes values, not only quoting.** `render_frontmatter` writes a quoted-scalar string bare: `'0.8'` becomes `0.8` (float), and `'yes'` / `'null'` go the same way (rows 22-23). The patch gate does surface this, because the drift list shows `+note_str: 0.8`. But the sanctioned route (`canonicalize`) then converts the value with rc 0 `updated`, while the ERR describes the change as "comments and non-significant quoting". This is exactly what SM 154 named ("'0.8' -> float, 'yes' -> True"), so it stays under 154 / SM's queued review of d8b22ae96. Corpus impact at the pin: 0 of 5354 nodes change a value on a canonical round-trip (row 24).
- **Scale of the fail-closed gate.** 746 of 4808 live node-patchable nodes are not canonical (row 24), so a node patch on them refuses until someone runs `canonicalize`. That is 15.5%, and 690 of them only lack a final newline. The first check's "3/5337" counted only flow tags and single quotes. This is correct under the restated F1, but the ERR's reason does not mention the trailing newline (row 25 shows `re-render: ['+']`). It is a wording point for the same review. All config (.geometry) nodes are canonical, so the owner's own case (config:guard) patches directly.
- The dry rc 0 / real rc 2 split on a written_by refusal (row 1) is the ring-preview contract, as in the first check (SM run 25).

### Tests (tree @462590995, one file per run)
test_write 180p/1x (the xfail is bundle 4 W3c's) · test_body_patch 6p · test_write_guard 32p. This row has no strict xfail. Its tests were not weakened (row 29). Numstat is in row 30, and the goal states no ceiling.

### Residues
SM 150 / 151 / 155 are MET (563cd4ca9). 152 / 153 / 154 / 162 / 163 are built in d8b22ae96 and measured holding here (rows 17-22, 25). They wait on SM's verdict (card-sanctuary-master REVIEW QUEUE: d8b22ae96), and DG3 closes the goal on residue 0 (card-director-general-3 WAIT). No new gap outside SM's scope, so no corrective.
