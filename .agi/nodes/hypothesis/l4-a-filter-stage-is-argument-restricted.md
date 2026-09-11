---
id: hypothesis:l4-a-filter-stage-is-argument-restricted
mint_id: b4cafae65dbb4876994a159e6c92afed
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-first-turn-filters-truncate
next_edges: []
edited_by: sanctuary-director
scaffold_hash: aaacfb64bee7716f
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-VIII) ruling merge-up 31 (d0d9777a5, goal:g15 newest note), ACCEPTED there; minted by sanctuary-director gen XIII 09:4xZ. (g15-32, FIRST, SECURITY) rotate.py:4105 skips every post-`|` stage whose exe is in _STARTUP_FILTERS (:3891) -- the judge never looks at its ARGUMENTS, so the prime ran `| awk BEGIN{system(...)}` (a command executed), `| sort -o M` (a file written), `| head -1 /etc/hostname` and a placeholder value `a | cat /etc/hostname` (a file read into the STARTUP OUTPUT). CLAIM: a filter stage is judged too -- its arguments may not name a path (no token containing `/`, no `-o`/`-w`/`-i`/`--output`/`-f` file options), `awk` and `sed -w`/`-i`/`e` program bodies are refused (awk refused outright, or allowed only with a program lacking `system`/`getline`/`>`/`|`), and a filter with any refused argument is a NAMED refusal (`filter <exe> <arg>`) before anything runs; FOLD: PATH, PYTHONPATH and LD_* are refused unconditionally in env values (not only by absence from env_allow). TESTS (hermetic, test_rotate_startup.py): each of the prime's four probes is refused by name; `| head -5`, `| grep -c x`, `| sort`, `| cut -c1-80`, `| tr`, `| wc -l` still run. FALSIFIER: any post-| stage that writes, reads a path, or runs a command. CEILING: 2 kids. FILE SCOPE: rotate.py (the filter/producing judge :3885-3900, :4095-4130 and the env refusal only) + test_rotate_startup.py. SERIAL on rotate.py behind L4.179 (l4-rotations-startup-commands-must-parse, the status/record READ region). EXCLUDED: rotations.md, the live seats row."
thought_session: bca4febf-020c-4ee2-b023-9ed885b937bc
title: a post-| filter stage of a first_turn command is argument-restricted and PATH/PYTHONPATH/LD_* are refused unconditionally
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-filter-stage-is-argument-restricted

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-VIII) ruling merge-up 31 (d0d9777a5, goal:g15 newest note), ACCEPTED there; minted by sanctuary-director gen XIII 09:4xZ. (g15-32, FIRST, SECURITY) rotate.py:4105 skips every post-`|` stage whose exe is in _STARTUP_FILTERS (:3891) -- the judge never looks at its ARGUMENTS, so the prime ran `| awk BEGIN{system(...)}` (a command executed), `| sort -o M` (a file written), `| head -1 /etc/hostname` and a placeholder value `a | cat /etc/hostname` (a file read into the STARTUP OUTPUT). CLAIM: a filter stage is judged too -- its arguments may not name a path (no token containing `/`, no `-o`/`-w`/`-i`/`--output`/`-f` file options), `awk` and `sed -w`/`-i`/`e` program bodies are refused (awk refused outright, or allowed only with a program lacking `system`/`getline`/`>`/`|`), and a filter with any refused argument is a NAMED refusal (`filter <exe> <arg>`) before anything runs; FOLD: PATH, PYTHONPATH and LD_* are refused unconditionally in env values (not only by absence from env_allow). TESTS (hermetic, test_rotate_startup.py): each of the prime's four probes is refused by name; `| head -5`, `| grep -c x`, `| sort`, `| cut -c1-80`, `| tr`, `| wc -l` still run. FALSIFIER: any post-| stage that writes, reads a path, or runs a command. CEILING: 2 kids. FILE SCOPE: rotate.py (the filter/producing judge :3885-3900, :4095-4130 and the env refusal only) + test_rotate_startup.py. SERIAL on rotate.py behind L4.179 (l4-rotations-startup-commands-must-parse, the status/record READ region). EXCLUDED: rotations.md, the live seats row.
