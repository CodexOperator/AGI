---
id: hypothesis:the-choice-surface-derives-proposable-from-declared-side-effects
mint_id: 144e23c2a5034a9b96d1cc9913708ba5
type: hypothesis
parents:
  - goal:g1.25.5
next_edges: []
assigned: "director-engine (leaf goal:g1.25.5, round C1: proposable derived from side effects)"
ceiling: 1 kid, 10-12 production lines per conjunct, pi parent (scope, never spend)
confidence: 0.7
edited_by: director-engine
scaffold_hash: 4bb3c9c7a3d4c279
season: 2
testable_claim: After the fix, commands.py names one never-proposable side-effect set (spawn, spend, destructive, plus new box-write and long-running) that _entry forces off the surface and that propose refuses by name on a supplied arg declaring it, command:commands declares crons.py:apply/remove and anonymize.py:install-hook box-write, dashboard.py watch arg long-running and envfile.py set arg box-write, season.py:judge is proposable false with a reason, and the operator-verb gate derives its set from each entry side_effects and reason instead of the three-key list, proved by committed tests red on the pre-fix bytes, with test_commands_manifest.py, test_commands.py and test_graphweb.py green.
title: "The choice surface derives proposable from declared side effects -- no box writer, endless watch or judgment stamp is offered, and the operator gate reads the set, not three keys (goal:g1.25.5 round C1; assigned: director-engine)"
town: local-maxxing
---
# hypothesis:the-choice-surface-derives-proposable-from-declared-side-effects

# hypothesis:the-choice-surface-derives-proposable-from-declared-side-effects

**Assigned: director-engine** (leaf goal:g1.25.5, round C1; the owner's cli-maxxing, goal:g1.25) · build loop · one `[merge-up]` to thought-master.

## Measured (bytes verified by a read-only triage pass for director-engine 22:4xZ 09-23 on the post tip d5696ac1de (every file:line read))
```
gate      test_commands_manifest.py:848-855 pins the literal ("crons.py:apply", "crons.py:remove", "mesh-gw") (:853) -- R-EF45 M2,
          untouched since EF.45; :619-624 restates commands.py:225's literal ("spend","spawn","destructive") and cannot fail
derive    commands.py:201-202 SIDE_EFFECTS has no value for a write to box state outside the graph or a run that never exits;
          _entry (:215-227) forces proposable false only for spawn/spend/destructive (:225-226) -- every other value keeps its flag
writers   crons.py:apply :1165 / crons.py:remove :1194 / anonymize.py:install-hook :2717 say graph-write and leave the surface only
          by a declared flag (:1166 / :1195 / :2718); grid.py:cron escaped the key list (R-EF45 D1) until 211a92165 (:1257 destructive)
watch     dashboard.py: (commands.md:2837-2850) read, proposable true, declares `watch` (:2845); dashboard.py:699-701 --watch,
          :727-737 `while True` + sleep, only Ctrl-C exits; propose("dashboard.py:", {watch: 5}) -> [..., --watch, 5] (R-EF54 M1)
set       envfile.py: (commands.md:1211-1225) graph-write, proposable true, declares `set` (:1222); envfile.py:363-419 prompts on a
          TTY and rewrites the env file; propose("envfile.py:", {set: K}) -> [..., --set, K] -- same class, not in the goal's list
judge     season.py:judge (commands.md:2161-2181) graph-write, proposable TRUE (:2180-2181): stamps judged_against/lens/alignment via
          write.py, --quorum may shell send.py audience prime; its 4 graph-write siblings are proposable false, operator-only
          (:2205, :2220, :2234, :2253)
limits    146 of 220 entries proposable, 45 of them graph-write (the write.py seam; live tests propose write.py:set at :541, :565,
          :627) -- "graph-write => off the surface" is not derivable, so judge leaves by a reason; reason <=> not proposable holds
          over all 220 today (0 exceptions either way)
schema    [command].md:10 names side_effects as a key; no field meaning lists its values or a per-arg side_effects
```

## CLAIM
After the round, whether a proposer is offered an entry is derived from its declared side effects. `commands.py` names ONE never-proposable set beside `SIDE_EFFECTS` (`NEVER_PROPOSABLE`): spawn, spend, destructive, plus two new values -- `box-write` (writes box state outside the graph: the crontab, systemd units, a git hook, the env file) and `long-running` (never exits on its own). `_entry` forces an entry whose side effect is in the set off the surface; `propose` refuses BY NAME a supplied arg whose own declared `side_effects` is in it. command:commands declares by that vocabulary: crons.py:apply, crons.py:remove and anonymize.py:install-hook `box-write` (grid.py:cron keeps `destructive`), dashboard.py's `watch` arg `long-running`, envfile.py's `set` arg `box-write`; season.py:judge is `proposable: false` with a reason, like its four season.py siblings (director's call: a judgment stamp -- with `--quorum`, an audience with the Prime -- is the reviewer's act; side_effects cannot tell it from write.py:set, so it leaves by a reason, not a derivation). The operator-verb gate names no key: every entry whose side effect is in the set is off the surface with a reason, reason <=> not proposable over every entry, and every never-proposable arg is optional and refused by name. Red on the pre-fix bytes: a synthetic entry declared `box-write` + `proposable: true` comes out proposable, and `propose` returns an argv for dashboard.py `watch`, envfile.py `set` and season.py:judge. `[command].md` names both values and the per-arg field; `propose` still imports and executes nothing.

## Dispatch line
config-max: which entries and args a proposer is never offered is read off the node's side_effects cells (entry and per-arg) and reason cells / template-max: none / code: `_entry` already derives off-surface for spawn/spend/destructive (commands.py:225-226) -- the set gains two values and `propose` one per-arg refusal; the set stays a code constant beside SIDE_EFFECTS, a floor a node edit cannot lower

## FALSIFIERS
- an entry whose side_effects is in the never-proposable set that is proposable or carries no reason; an entry with a reason that is proposable; one off the surface without a reason
- the gate (or the spend/spawn/destructive test at :619-624) naming a key or copying the set instead of reading `commands.NEVER_PROPOSABLE`
- `propose` returning an argv carrying `--watch` for dashboard.py: or `--set` for envfile.py:, or any argv for season.py:judge; a never-proposable arg that is required, or refused without its name
- a new committed test green on the pre-fix bytes
- an existing assertion relaxed: `_full_supply` may omit only an arg whose declared side effect is in the set, and only beside an assertion that supplying it refuses by name
- `[command].md` not naming box-write, long-running and the per-arg side_effects; `propose` importing or running a CLI
- any of the named test files red; a change outside FILE SCOPE

## TESTS
test_commands_manifest.py (the derived gate, the propose falsifiers, full supply, drift, coverage) · test_commands.py · test_graphweb.py (POST /propose) -- those files only, under `env -u TMUX -u TMUX_PANE`

## FILE SCOPE
extensions/agi/bin/commands.py · .agi/nodes/.geometry/commands.md (command:commands -- pass `--owns command:commands` to `cli.py done`) · .agi/context/schemas/[command].md · extensions/agi/tests/test_commands_manifest.py

HAZARD: HIGH blast radius: never run a verb this round re-declares -- crons.py apply/remove write the real crontab and systemd units (grid_sync re-applies every 5 min), anonymize.py install-hook writes a git hook, envfile.py --set rewrites the env file, dashboard.py --watch never exits, season.py judge stamps a live report node -- prove through manifest()/propose() and tmp_path fixtures only
HAZARD: commands.md and test_commands_manifest.py are shared with g1.25.5 rounds B, C2 and D -- never in parallel with them

## CEILING
1 kid · 10-12 production lines per conjunct · pi parent · scope, never spend (owner 09-23 14:xZ)
