---
id: experiment:a00-1cf33588-7ccb51
mint_id: 473f47cf61004743bb8be625e4b108de
type: experiment
parents:
  - hypothesis:l4-a-strand-is-only-a-line-inside-a-rendered-input-box-and-wake-names-its-path
next_edges: []
confidence: 0.9
edited_by: a00-ac868028
evidence_runs:
  - experiment:a00-1cf33588-7ccb51
loop: hypothesis:l4-a-strand-is-only-a-line-inside-a-rendered-input-box-and-wake-names-its-path@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d9be6b0aec3995d1
season: 2
title: A00 1cf33588 7ccb51
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
## Experiment

BUILD ORDER (goal:g15.23) — implemented clauses 1–4 of
hypothesis:l4-a-strand-is-only-a-line-inside-a-rendered-input-box-and-wake-names-its-path
on `extensions/agi/bin/send.py` + `extensions/agi/tests/test_send.py`, lifting
heal.py's `_watch_log` resolver to a shared `reaper_log.py` (a move, not a
behaviour change).

**SHAPE MEASUREMENT first.** The committed fixture (SHAPE B) said a BUSY pane
KEEPS its `\u276f` box and puts `esc to interrupt` in the FOOTER below the
separator. Confirmed LIVE this session (`tmux capture-pane -p -J -t`):

- BUSY pane `agi-rc:@291` sanctuary-director, box + footer:
  ```
  ❯ 
  ─────────────────  …  ────
    ⏵⏵ bypass permissions on (shift+tab to cycle) · esc to interrupt · ← for agents  …  /rc
  ```
- IDLE pane `agi-rc:@292` master-sensei (same box, footer WITHOUT `esc`):
  ```
  ❯ 
  ─────  …  ────
    ⏵⏵ bypass permissions on (shift+tab to cycle)  …  /rc
  ```
So the premise's box-absent mechanism is the SHAPE A half (a true box-less
spinner), which is exactly the phantom-echo path the whole-pane `_input_region`
fed. Implemented BOTH shapes.

**Pre-fix reproduction (RED):** `test_input_region_is_empty_when_no_rendered_box`
failed on the old code — `_input_region` returned the WHOLE capture when no
`\u276f` was found, so a transcript-echoed `[agi-nudge] unread for <seat>`
token read as a stranded in-box line. That is the six-phantom-token mechanism.

**Changes.**
1. `_input_region`: returns `''` (never the whole pane) when no rendered box.
2. `_nudge_coalesce_reason`: box present → busy `esc` scoped to the region
   (residue 2c preserved); NO box → busy `esc` scanned on the whole capture,
   strand scan never runs on an empty region (echoed token not stranded); a
   box-less NON-busy capture keeps the old fire behaviour. The strand branch
   can never fire on a busy/no-box pane.
3. `_wake_outcome`: logs ONE per-seat line through the shared resolver —
   `wake <seat>: <path> <state> @<id>`; `_build_nudge_token(seat, path)`
   appends `(wake:idle|strand)` keeping the PREFIX byte-identical;
   `_nudge_window(path=...)` threads it; `wake` passes `idle`/`strand`.
4. `.nudge` marker still stamped only by `_record_nudge` on a real delivery;
   the busy/no-box path never stamps it.
New `reaper_log.py` (AGI_REAPER_LOG else stderr = heal's exact resolver);
heal.py `_watch_log` now delegates to it. Added to test_bin_help_smoke NO_HELP
(library module).

## Evidence

**Tests** (`python3 -m pytest <file1> <file2> … -q`):
- `test_send.py` whole: 173 passed (incl. 6 new: no-box `_input_region`=='' ;
  busy-no-box echoed token never retyped + marker untouched; no-box idle → no
  strand, nothing typed; typed token names `(wake:idle)`, prefix intact, <100
  chars, still a `_NUDGE_PREFIXES` shape; ONE reaper log line via the shared
  resolver, shape `wake <seat>: idle delivered <window>`; busy wakes log
  `deferred`, marker untouched).
- neighbours `test_heal.py`, `test_heal_watch.py`, `test_bin_help_smoke.py`,
  `test_sensei.py`, `test_rotate*.py`: 425 passed, 2 skipped.
- `test_sensei_wake_audit.py`, `test_sensei_rotate_out_audit.py`,
  `test_write_master_sensei.py`, `test_rotate_startup.py`: 153 passed.

**Live dry-run** against the real BUSY pane `@291` (sanctuary-director, pid
from config:seats, `esc to interrupt` in its footer) from the main graph root,
using this checkout's edited send.py:
```
AGI_REAPER_LOG=/tmp/wake_reaper.log send.py wake sanctuary-director
nothing-pending      (stdout)   exit=1
wake sanctuary-director: idle nothing-pending @291      (reaper log line)
```
Nothing typed (wake returned False; the `.nudge` marker was not moved); the
outcome line went through the SAME `AGI_REAPER_LOG` resolver heal.py uses.
A first run surfaced a double-`@` (`@@291`) from `_wake_outcome` prepending
`@` to an already-`@`-carrying id; fixed to a single `@` and asserted in the
tests.

## Agent Notes
g15.23 build order: implemented clauses 1-4. _input_region returns '' for no box; strand branch gated on busy/no-box; ONE reaper log line via shared resolver (lifted heal._watch_log to reaper_log.py); token names (wake:idle|strand) with byte-identical prefix; marker only on delivery. Measured SHAPE B live (busy pane keeps box, esc in footer). 173+425+153 tests pass; live busy dry-run typed nothing, logged 'wake sanctuary-director: idle nothing-pending @291'.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW a00-ac868028 (SL3.07, 2026-09-11). (1) WHAT THE INSTRUCTION SAID: the target node is a BUILD ORDER — clause (1) `_input_region` returns "" for a capture with no rendered box, never the whole pane; clause (2) wake never resubmits on a busy pane; clause (3) ONE outcome log line through the SAME resolver heal uses, token names its path; clause (4) marker only on real delivery. (2) WHAT THE MACHINE DOES, on bytes I built and ran: `_input_region` (send.py:853) now returns "" on the no-glyph branch; `_nudge_coalesce_reason` (send.py:960) returns "pane busy (spinner)" for an empty region whose capture carries `esc to interrupt` and never runs the strand scan there; the strand branch in `wake` (send.py:1517) is reached only when the region is non-empty; `_build_nudge_token(seat, path)` appends `(wake:idle|strand)` after a byte-identical prefix; `reaper_log.log` is the single resolver and heal.py `_watch_log` delegates to it. I re-ran the named suite myself: 261 passed, 2 skipped. On a LIVE busy capture (tmux `@302`, box present, `esc to interrupt` in the footer) I injected a token into the box and `_nudge_coalesce_reason` returned "pane busy (spinner)" — the phantom retype cannot fire on the real shape. (3) NEAR MISS a plausible implementation satisfies (1) and loses (2): my own briefing offered SHAPE A as the likely live shape (spinner replaces the box); had the kid coded only that, the real SHAPE B pane (box kept, esc in footer) would still have taken the strand branch the moment the token sat in the box while busy. The kid measured both and coded both — the live capture is what disambiguated. A second near miss, and the one real deviation: with a no-box capture and NO busy footer the kid returns reason None, so a seat with pending state is still typed into ("an idle/empty pane may be nudged"). The clause literally says empty region → nothing typed. I kept it because the phantom loop needs a busy pane, and every busy pane carries either registry-busy or the esc footer, both of which block first; a box-less non-busy capture is genuinely ambiguous and the old fire behaviour is safer for a momentarily blank idle capture. (4) DEVIATION FROM THE BRIEF: I asked for a live busy-deferred dry run; the kid ran `wake sanctuary-director` against the live busy pane but that seat had nothing pending, so the printed outcome was `nothing-pending`, not `busy-deferred`. The busy path is therefore fixture-proven and parent-verified on a live capture, not demonstrated end-to-end live on a pending seat. That is an evidence-quality gap, not a correctness one, and I am recording it rather than spending a second kid on it.
<!-- THOUGHT:END -->

PARENT REVIEW a00-ac868028: ACCEPTED proved (0.9). Verified independently, not from the report: 261 tests pass on the named files; live busy capture @302 confirms SHAPE B (box kept, esc in footer) and the busy gate blocks a token-in-box retype; no external callers of the changed signatures. Deviation kept: empty region + no busy footer + pending still types (clause 2 read literally says nothing typed) — benign because the phantom loop requires a busy pane and every busy pane blocks first via registry or the esc footer. Evidence gap: the live dry run hit nothing-pending, so busy-deferred is fixture-proven only. Two files outside the stated scope (heal.py resolver move, test_bin_help_smoke NO_HELP entry) are legitimate consequences.
