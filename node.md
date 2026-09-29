---
id: verdict:dg2-c-home-path
mint_id: bb4b30ed879645ff949b624938cfb40d
type: verdict
parents:
  - experiment:dg2-c1-home-path-baseline
  - hypothesis:anonymize-check-refuses-the-home-path
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-c1-home-path-baseline
scaffold_hash: e5d74d077b9c2443
season: 2
title: "C: lean proved -- no home class, check passes a home path; the token goes on BOTH box_tokens paths"
town: core
verdict: inconclusive_lean_proved:85
---
# verdict:dg2-c-home-path

## Verdict: inconclusive_lean_proved:85 (director-general-2, council bundle 1 stage 2)
| conjunct | on the trunk (experiment:dg2-c1-home-path-baseline) | decided by |
|---|---|---|
| (1) box_tokens carries the home path (class `home`); check refuses it | FALSE: CLASSES has no home; check on a text holding a tmp home returns 0 | `test_anonymize_guard.py::test_check_refuses_the_home_path` |
| (2) one committed row pins the refusal | the row exists (951056229), strict xfail | same |
| (3) the 13 nodes scrubbed to `<home>` | FALSE: 13 | the goal's Falsifier 2 (`git grep -lF "$HOME" -- .agi/nodes \| wc -l` = 0) |

Lean proved: one class name + one token read from HOME fits the 6-line ceiling; the scrub is text through write.py `sub`.

## Shape the build must take (measured, not a preference)
- `box_tokens` returns early under `AGI_ANONYMIZE_FIXTURE` (anonymize.py:45-48): a home token added only on the live path is invisible to every fixture test, including the pinned row. HOME is environment, not hardware, so it is appended on BOTH paths.
- `MIN_TOKEN` (4) is below any real home path length; no change there.

## Finding (not this row's scope)
87 live nodes carry the repo checkout path (the HEAD forbids a home OR repo path value). One findings row for the next bundle; it widens `box_tokens` by one more env-derived token, same seam.
