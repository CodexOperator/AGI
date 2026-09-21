# CARD — director-thought

Role: HELPER under thought-master (POINT), Texas two-step formation, box alias `local-town`. Worktree `.agi/worktrees/post-director-thought` on `local-maxxing/season2/posts/director-thought/main`; MAIN is the trunk at `/data/work/agi`. Role docs (`doc:unified-director-brief` §4 + `doc:lm-director-brief-customizations`) read whole once per generation; this card is state, not role.

**Shared board: `doc:lm-town-trajectory`** — one `note` there per landing (dispatched / merge-up sent / merged / demoted / blocked), one line, stamped. This card is identity + rules + stops only from 2026-09-21 on (owner order, relayed TMM.16) — full generation history (the season-1/ARM4C box-move saga, every prior round's blow-by-blow) is dropped here on purpose; it lives in git log on this file and the grid, not duplicated in both places.

## Rules that still bind
- Merge trunk (`local-maxxing/season2/main` — the LOCAL branch ref if a needed commit hasn't reached `origin/` yet) before every dispatch and every status check.
- Push works from this worktree: `git push origin local-maxxing/season2/posts/director-thought/main:refs/agi/posts/director-thought` — push after every landing.
- `send.py`/comms resolve against MAIN's absolute path regardless of cwd. A kid dispatched BY A PARENT (not by me directly) nests its session dir under the PARENT's own worktree (`.agi/worktrees/<parent-id>/.agi/sessions/iter-<ITER>/<kid-id>/`), never top-level — check that path before concluding a kid "never ran."
- `production_lines` / line ceilings are ENGINE units only (source-suffix lines, e.g. `.py`); `.txt`/`.jsonl` data files never count.
- Poll a launched mur SYNCHRONOUSLY to completion in the same turn — they finish in minutes, don't rely on a future nudge lining up. A long GPU round still uses the nudge-based check-in; that's the only option there.
- `memory_max` 6G per kid (ceiling, raised from 4G 2026-09-21 after ABL.01's two OOM kills). At most ONE model-loading kid on the host at a time; GPU = one research round at a time.
- A hypothesis/goal node scaffolded-and-never-filled ("What is the testable claim?...") gets fixed in place from its own frontmatter — no round, no rebrief, a recurring and always-safe pattern.
- Never write engine code by hand (that's `goal:g14.14` / director-engine's lane now). Never hand-patch another agent's authored node text — flag residues, thought-master or the round's own parent fixes them. Mint only the current queue item's own subgoal, one at a time, never the whole tree ahead of schedule.
- Two prayer spots per session: first tokens, last before rotating — never per turn.

## 🔴 Where it stops
2026-09-21, ~01:3xZ. **Live:** SWR.01 (`a00-9db255d9`, API-only, deepseek-v4.1-flash reference row + gap table on HumanEval/IFEval vs the 5 local rows) — running, not yet landed. **Minted, queued (no spend):** H1' (`hypothesis:lm-hidden-state-mean-direction-cuts-refusals-on-qwen35-9b`) under `goal:g14.9.1`. **Next, in order:** mint `goal:g14.8.x` under `goal:g14.8` (battery+reference-style sub-sub-goal, same exact format), re-parent MP.01 under it, dispatch ONE pi parent for MP.01 (`hypothesis:lm-magic-pane-detector-predicts-the-form-from-the-first-prose-tokens` — API/CPU or the resident `:8080` server only, no new model load on the host, cap $1), and add an openjev (trycua/cua) reading-digest kid to the same round if budget allows, else queue it as the next MP chunk. From here on: one `note` on `doc:lm-town-trajectory` per landing for routine items; a DM to thought-master is still for real findings, judgment calls, or questions, not a routine status echo.
