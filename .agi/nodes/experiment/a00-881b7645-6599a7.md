---
id: experiment:a00-881b7645-6599a7
mint_id: 3526cf53348846f784279b886f91cac0
type: experiment
parents:
  - hypothesis:l3w0-rotate-roles
next_edges: []
confidence: 0.8
edited_by: ubuntu
evidence_runs:
  - experiment:a00-881b7645-6599a7
loop: hypothesis:l3w0-rotate-roles@s2
model: ~z-ai/glm-flash-latest
profile: balanced
role: parent
scaffold_hash: f255d002abbce12a
season: 2
title: A00 881b7645-6599a7
verdict: proved
---
# experiment:a00-881b7645-6599a7

## Experiment

Took the OPEN follow-up in hypothesis:l3w0-rotate-rules' STATUS (owner rule
2026-09-07): rotate.py had shipped the integer `belam-N` successor name; the
owner rotated by hand with `--name belam-S1-L3-II` while the following
derivation was still open. Implemented and verified the replace scheme.

**What changed.** `rotate.py` `_derive_successor_name` now derives the
successor as `<base>-<ROM>` instead of `<prefix>-<N>`:

- The line of the tree's prime: bare prime `belam-S1-L3` is line value 1
  (its successor is `belam-S1-L3-II`); `-II` is line 2 (successor `-III`);
  `-III` -> `-IV`. The base is the current window's name stripped of any
  trailing `-<ROM>`.
- Nothing matching `--prefix` (or no windows) yields `<prefix>-II`.
- `--name` still overrides; non-matching windows ignored.
- New helpers: `_roman_value`/`_is_roman` (canonical, rejects `IIII`-style
  garbage), `_int_to_roman`, `_split_roman_suffix`.

Files edited: `extensions/agi/bin/rotate.py` (module docstring, `_derive`,
Roman helpers), `extensions/agi/briefs/prime-director-successor.md` (the
rotate line no longer says `--name belam-<N+1>`), `extensions/agi/tests/test_rotate.py`
(updated existing derive/name tests to the Roman scheme; added `-III`, bare
prefix, non-matching, cross-prefix cases).

**Verification.** In a hermetic env (AGI_* unset): `test_rotate.py` full —
**first red, 3 failed** (the untouched integer expectations), then **14
passed** after the Roman edit. Full suite: **1785 passed, 1 skipped** with 4
failures in `test_claude_code_adapter.py`/`test_dispatch.py` (`brief_tier`
routing) that also fail (as order/state leaks) when run with these same
lines on the current branch — reproducible in the full run, green when the
two files run alone (72 passed) and green per-test; none touch `rotate.py`,
so they are pre-existing and not from this change.

**Live-run witness** (real command shape, `--dry-run`, no tmux):
```
extensions/agi/bin/rotate.py spawn --window-path /tmp/w.txt --prompt-file
  extensions/agi/briefs/prime-director-successor.md --dry-run
```
Windows named `belam-S1-L3` and `belam-S1-L3-II`. Actual stdout
(first ~ chars):
```
claude --remote-control belam-S1-L3-III --permission-mode bypassPermissions
--debug-file .agi/sessions/belam-S1-L3-III.log --model claude-fable-5-1
--effort max --settings'{"ultracode": true}' '─── CONSTITUTION HEAD ───
...
```
successor name is *Roman* (`belam-S1-L3-III`, not `belam-3`), and the rest of
the assembled command (model / effort / settings / head-first prompt) is
unchanged from the already-proved claim.

## Evidence

Commands run (in `.git/work/agi`) with output:

1. Unit derivation spot-check:
   ```
   python3 -c "import rotate; ..."
   empty            -> belam-II
   [belam-S1-L3]    -> belam-S1-L3-II
   [+belam-II]      -> belam-S1-L3-III
   [+belam-III]     -> belam-S1-L3-IV
   [belam]          -> belam-II
   [agi-master-7]   -> belam-II
   [ccc-III]        -> ccc-IV
   ```

2. `env -u AGI_LOOP -u AGI_MODEL -u AGI_ROLE -u AGI_PROFILE -u AGI_SEASON
python3 -m pytest extensions/agi/tests/test_rotate.py -q`
   -> `14 passed`

3. Dry spawn (real argv) as in «What changed» — remote-control name, model,
   effort, settings and head-first prompt all correct; the derived name is
   Roman.

4. Full engine suite:
   `env -u AGI_LOOP ... python3 -m pytest extensions/agi/tests/ -q`
   -> `1785 passed, 1 skipped` with 4 tracked pre-existing order failures
   (brief_tier in test_claude_code_adapter/test_dispatch) that vanish when
   the two files are run alone (`72 passed`) and are untouched by this work.

## Caveats / dependencies

- This is code+unit+integration-level evidence; no live tmux window was
  spawned (per the addendum the prime runs live proofs; this agent is
  dry-run-only). The derived `-III` name is witnessed in the printout of the
  command, not in a real window.
- The 4 full-suite failures are order-dependent `brief_tier` tests that pass
  in isolation; I did not chase them. They are not this hypothesis's code,
  but they block a clean 0-failure suite on which to hang confidence.
- Owner rule's wording "Belam II, Belam III" is satisfied by the window name
  carrying `-II`/`-III` via the template's `{name}` line; the successor
  filename line names the prime by its window, fine for a mantle.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-2c839188, L3.12): accepted as proved. Independently re-verified in the current tree: (1) test_rotate.py 14 passed; (2) derivation spot-check via the real helpers — empty->belam-II, belam-S1-L3->belam-S1-L3-II, belam-S1-L3-II->belam-S1-L3-III, belam-3->belam-3-II, non-belam windows ignored — matching the owner rule of 2026-09-07 (bare prime = line 1, so first follower is -II); (3) dry spawn with a two-line window file derives belam-S1-L3-III with --model claude-fable-5-1 --effort max --settings {"ultracode": true} and a head-first prompt; (4) FULL suite in this pass is 1789 passed, 1 skipped, ZERO failures — the kid's 4 pre-existing brief_tier order leaks no longer reproduce, which strengthens rather than weakens the claim. evidence_runs correctly self-lists (the experiment IS the run); parents resolve. Caveats accepted as honest: live tmux continue-witness stays the prime's per addendum; the Roman scheme is not yet exercised by a real rotation (the current prime belam-S1-L3-II was rotated by hand). Cosmetic: two typos in the body (l3w0-rotate-rules, Romom) — noted, not demoting. No demotion.
<!-- THOUGHT:END -->

## Agent Notes
Implemented+verified Roman-numeral successor derivation (OPEN follow-up): _derive_successor_name now yields <base>-<ROM> (belam-S1-L3 -> -II -> -III), tests red-first then 14 passed; dry spawn emits belam-S1-L3-III with fable-5-1/max/ultracode head-first. 4 full-suite brief_tier failures are pre-existing order leaks.

Parent review L3.12 (a00-2c839188): accepted proved. Re-ran test_rotate.py (14 passed), derivation spot-check (bare->II, -II->-III, belam-3->belam-3-II, non-belam ignored), dry spawn derives belam-S1-L3-III with fable-5-1/max/ultracode head-first; full suite 1789 passed / 1 skipped, zero failures (kid's 4 pre-existing brief_tier leaks do not reproduce). Caveats honest (live tmux witness = prime's). No demotion.
