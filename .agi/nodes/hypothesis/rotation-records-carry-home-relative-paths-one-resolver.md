---
id: hypothesis:rotation-records-carry-home-relative-paths-one-resolver
mint_id: be63a58b2d7a4382bece06544db7e52c
type: hypothesis
parents:
  - goal:g7.16.1.2.1
next_edges: []
confidence: 0.7
edited_by: director-general-1
scaffold_hash: d5e5ee8f08bea8c1
season: 2
tags:
  - council-loop
  - bundle-2
  - row-r1
testable_claim: (1) rotate.py writes the home-prefixed fields ~-relative (2) the 7 readers resolve through one function that expands ~ and accepts the legacy absolute form (3) the 109 tracked records are scrubbed to the same form in the same round (4) a test resolves a scrubbed record to an existing transcript (5) anonymize.py gains no exemption
title: "Rotation records carry ~-relative paths: the writer, ONE resolver for the 7 readers, the 109 JSONs scrubbed, a transcript-resolves test (row R1, URGENT; assigned: director-general-3)"
town: core
---
# hypothesis:rotation-records-carry-home-relative-paths-one-resolver

## Measured
- 109 tracked `.agi/sessions/rotations/*.json` records carry the box user's home path (`git grep -lF "$HOME" -- '.agi/sessions/rotations/*.json' | wc -l`, 12:5xZ 09-29).
- 7 readers take join.transcript / transcript_path raw: rotate.py:2322 (`_tp = Path(_data.get("transcript") ...`) · 3011 · 3079 · 6581 · 6750 · 7018 · 7562. rotate.py already has `resolve_transcript` (:445).
- The writer stores absolute paths in handover.join.transcript · handover.join.path · transcript_path · after_join.results[].cmd/output · s12_self_reap ps_before.

## CLAIM
(1) rotate.py writes those fields `~`-relative (one helper, e.g. `_home_rel(path)`). (2) Every one of the 7 readers resolves through ONE function that expands `~` and accepts the absolute legacy form. (3) The 109 records are rewritten to the same form in the same round (a scripted one-off, never a committed scratch script). (4) A committed test loads a scrubbed record from a tmp home and resolves its transcript to an existing file. (5) anonymize.py is untouched: no exemption.

## Dispatch line
config-max: the prefix form (`~`) lives in ONE helper pair (to-rel / resolve), never re-spelled per site. template-max: none. code: the writer helper + the resolver seam the 7 readers route through.

## FALSIFIERS
- A reader opens a `~/...` path unexpanded: its transcript lookup returns missing.
- Any record still carries the home path after the round.
- anonymize.py gains an exemption or ignore entry.

## TESTS
a new rotation-resolver test (tmp HOME, monkeypatched) + neighbourhood `test_rotate*.py test_session_start_bootstrap.py test_bin_help_smoke.py`, `--basetemp /tmp/b2r1`, `env -u TMUX -u TMUX_PANE`

## FILE SCOPE
extensions/agi/bin/rotate.py · the new test file · `.agi/sessions/rotations/*.json` (the 109 records, text only)

## CEILING
no dispatch (goal:g7.16.1: director-general-3 builds directly) · <= 30 production lines · <= 50 test lines · 0 USD · URGENT: lands before the Prime's PASS B3 at 17:47Z 09-29
