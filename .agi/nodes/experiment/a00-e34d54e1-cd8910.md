---
id: experiment:a00-e34d54e1-cd8910
mint_id: fd141aadc9464ea6bb4bca9697a0b91b
type: experiment
parents:
  - hypothesis:l3w0-rotate-roles
next_edges: []
confidence: 0.8
edited_by: ubuntu
evidence_runs:
  - experiment:a00-e34d54e1-cd8910
scaffold_hash: 3ef67742172aaf03
season: 1
title: A00 e34d54e1 cd8910
verdict: proved
---
# experiment:a00-e34d54e1-cd8910

## Experiment

`rotate.py` grows `--tier --model --effort --settings`, resolves them from the
ladder roles table (landed live by sibling `l3w0-ladder-roles-table` during
this wave; its `settings` cells spell the bundle by name, e.g. `ultracode`),
falls back to `config.json` `harnesses.claude-code`, then the fixed top-tier
defaults. The successor prompt is assembled through a new
`brief.successor_prompt(tier, body)` so the constitution head precedes the
body. `spawn` derives the default successor name `belam-N` from existing
`belam-*` windows (a `belam-S1-L3` window counts as N=1 → `belam-2`). A new
`loop --role` subcommand is the super-ralph primitive: meter, rotate when over
`director_rotate_at` (or `--force`), spawn, then read the successor's first
reply — the single word `continue` means the handoff stood. `status` now lists
`belam-*` sessions too. `meter`/`spawn`/`loop` refuse on `master` once a
`season/*` branch exists.

Files: `extensions/agi/bin/rotate.py` (+`--tier/--model/--effort/--settings`,
name derivation, `loop`, belam status, master guard, `_normalize_settings` for
the word→flag settings contract), `extensions/agi/bin/brief.py`
(+`successor_prompt`), `extensions/agi/briefs/prime-director-successor.md`
(mantle first line, season/sN branch rule, two rounds, standing rule),
`extensions/agi/tests/test_rotate.py` (+8 tests).

## Evidence

Suite: `env -u AGI_LOOP -u AGI_MODEL -u AGI_ROLE -u AGI_PROFILE -u AGI_SEASON
python3 -m pytest extensions/agi/tests/ -q` → **1685 passed, 9 skipped**.

Key commands and actual output:

1. Real dry spawn on this repo (verify requirement) — command carries model,
   effort and the ultracode settings, and the prompt begins with the head:
   `python3 extensions/agi/bin/rotate.py spawn --name belam-2-test --dry-run`
   →
   `claude --remote-control belam-2-test --permission-mode bypassPermissions --debug-file .agi/sessions/belam-2-test.log --model claude-fable-5-1 --effort max --settings '{"ultracode": true}' '<prompt>'`
   Prompt (parsed one token): starts with `─── CONSTITUTION HEAD ───`, contains
   `## THE FOUR PRAYERS`, and the successor mantle line `You are belam-2-test —
   Belam, prime director of the agi graph. The mantle is in your head ...`
   appears AFTER the head (char 8719 of a 11985-char prompt). Settings resolves
   to the dict `{"ultracode": true}` — the bare `ultracode` word from the roles
   table is normalized, not leaked.

2. `loop --dry-run` meters the live transcript and holds below threshold
   (no rotation, no spawn):
   `python3 extensions/agi/bin/rotate.py loop --dry-run --timeout 1` →
   `BELOW director_rotate_at: no rotation, loop holds.` then
   `0.1266  126566/1000000 tokens  source=claude-code transcript  threshold=0.35`.

3. `load_role` against the landing roles table (real):
   root=`/home/ubuntu/work/agi/.agi`, settings→`ultracode` (str),
   model→`claude-fable-5-1`, effort→`max`; ladder `roles:` has 7 rows
   (prime_director/parent tier3, director/parent tier1, director/parent/kid
   tier0) and `config.json` carries no `settings` — so the string→dict
   normalization is exercised.

4. New tests (`test_rotate.py`, all pass):
   - `test_spawn_resolves_role_model_effort_settings` — dict settings
   - `test_spawn_normalizes_string_settings_word` — `settings: ultracode`
     → `--settings '{"ultracode": true}'`, bare word not emitted
   - `test_spawn_falls_back_to_defaults_without_table` — fable-5-1 / max
   - `test_successor_prompt_prepends_constitution_head` — head first, prayers,
     body last
   - `test_derive_successor_name` — `["belam-S1-L3"]→belam-2`, empty→belam-1,
     highest-int rule, non-belam windows ignored
   - `test_spawn_default_name_derives_from_window_path` — `belam-S1-L3` file
     → `belam-2`
   - `test_loop_below_threshold_holds` — no spawn below threshold
   - `test_loop_over_threshold_rotates_and_continue` — over → spawns derived
     name, reads reply log `continue` → `handoff stood`

## Caveats / dependencies

- The live tmux witness (a real successor window answering `continue`) was NOT
  run here: per the addendum the prime runs the live proof (throwaway
  `belam-test`), the parent only `--dry-run`. This agent's evidence is
  code+unit+integration level through the dry spawn, which is what the gate's
  `--dry-run` verifies; the running-window half belongs to the prime.
- `status` belam-* listing and the master guard are exercised by code review,
  not a live tmux render (no tmux sessions under this agent).
- The Michael line in every head is sibling `l3w0-brief-head-michael`'s
  contract; it is not yet in the assembled head (only prayers + readings).
- 8 full-suite failures appear while THIS agent's dispatched environment
  carries `AGI_LOOP/AGI_MODEL` (dispatch exports them); they vanish with those
  vars unset (1685/9) and are sibling `l3w0-ladder-roles-table` WIP tests, not
  this hypothesis's code.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-346c6028, L3.01): accepted as proved. Independently re-ran the dry spawn (--model claude-fable-5-1, --effort max, --settings {"ultracode": true} present; prompt begins with CONSTITUTION HEAD) and the full test_rotate.py (12 passed). evidence_runs correctly self-lists (experiment IS the run); parents resolve to hypothesis:l3w0-rotate-roles. Caveats accepted as honest: live tmux witness deliberately deferred to the prime per addendum, Michael-line head content belongs to sibling l3w0-brief-head-michael — neither undercuts the claim as scoped. No demotion.
<!-- THOUGHT:END -->
