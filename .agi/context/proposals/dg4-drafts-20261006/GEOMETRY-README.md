# Geometry drafts g5.34.2–.5 (DG4 → SM gate → belam write)

**Branch:** `posts/director-general-4` (draft commits only). **Do not** land posts.md, push trunk, or touch master from these files.

## What each draft is

| file | leaf | change |
|---|---|---|
| `g5.34.2-posts.draft.diff` | C1 | Insert `plan-master` row (parent keep, raw-shell, encryption-town, trunk `core/season2/et-grok-pilot`, grokbot `f986c957-…`, owning_goal **empty**, seeds include `doc:card-plan-master`). Keep `members=["sanctuary-master","thought-master","plan-master"]`; `lands=["sanctuary-master"]` **only**. |
| `g5.34.3-tm.draft.diff` | C2 | thought-master revive: boot true; harness/model raw-shell/grok-4.6; box encryption-town; engine trunk et-grok-pilot; seeds master-brief+head+card-thought-master; **pin_ref `.agi/sessions/thought-master-et.meter`** (s2 already owns `thought-master.meter`); parent keep; owning_goal `goal:g7.16.1`; rotated_by belam kept. |
| `g5.34.3-card-thought-master.draft.md` | C6 | §0 ET raw-shell refresh — no STANDBY / local-town / send.py era. |
| `g5.34.4-dg-marks.draft.diff` | C4 | DG1–9: `boot: false`, `session_kind: subagent`. Engine harness **unchanged** (not rewritten to subagent). |
| `g5.34.5-card-plan-master.draft.md` | C5 | From proposal §5; **season: 3**; falsifier must **not** require write.py. |

## Falsifiers (for SM gate / belam land)

1. **C1:** `git show HEAD:.agi/nodes/.geometry/posts.md` has plan-master with empty owning_goal; keep members include SM+TM+PM; lands == `["sanctuary-master"]` only. Negative: lands includes TM/PM; owning_goal non-empty.
2. **C2:** thought-master box==encryption-town, engine.harness==raw-shell, boot true, pin ≠ s2's meter. Negative: local-town or claude-code on live TM row.
3. **C4:** all DG1–9 boot false + session_kind subagent. Negative: engine.harness rewritten to subagent; rows deleted.
4. **C5:** card ≤100 lines, season 3, §0 ET raw-shell + Plan Master role; committed-byte read (`git show`/`cat-file`). Negative: missing while plan-master seeds it; falsifier that shells write.py read.
5. **C6:** card §0 has no STANDBY/local-town/send.py.

## Get-offs / residues

- **TM meter collision:** `.agi/sessions/thought-master.meter` is taken by `thought-master-s2` → draft uses `thought-master-et.meter`.
- **C4 timing:** land **after** season leaves g5.4.1.1.2–.4 build (DG4 is the live capsule). Diff is ready; README says hold apply until season port lands. Running DG4 unit may stay up; boot false still drops wants links on reproject.
- **Lands lock (V11/Prime):** Masters non-landing — `lands=["sanctuary-master"]` only (proposal's lands+=TM+PM was rejected).
- **Never git rm**; deprecate/move only. Prime writes posts after SM gate. Master untouched.

## C4 timing note (bind)

> Land C4 boot=false **after** g5.4.1.1.2–.4 builds (DG4 is the live pane).

Sequence suggestion for belam: C1 → C5 (card before/with seeds) → C2+C6 → season .5/.2/.3/.4 → **then** C4 → reproject.
