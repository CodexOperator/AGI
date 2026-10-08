---
id: hypothesis:pin-reap-never-names-a-live-session-and-a-reap-leaves-no-stale-app-session
mint_id: c401494dac94496c855d0e9bf769240a
type: hypothesis
parents:
  - goal:g6.49
next_edges: []
confidence: 0.7
edited_by: director-engine
scaffold_hash: 732908fe58c8f18a
season: 2
testable_claim: After any reap, rotation or reboot the app lists only live sessions and heal.py pin-reap never judges REAP for a live pid that is its seat current registry session (a stale pin yields STALE-PIN); the late-s12 wait is bounded by a reaper.* config cell; the reap path TERMs with a config grace before any KILL and ends a dead pid app session where the CLI allows, else records that as MEASURED (lean).
title: pin-reap never names a live session, the late-s12 wait is bounded, and a reap leaves no stale app session
town: core
---
# hypothesis:pin-reap-never-names-a-live-session-and-a-reap-leaves-no-stale-app-session

# hypothesis:pin-reap-never-names-a-live-session-and-a-reap-leaves-no-stale-app-session

## Measured
- OWNER 01:0xZ 09-26 (Prime pane), verbatim: "I'm still seeing stale sessions in my app. The directors and master both have old sessions still in app and the prime has app sessions that look live past the 5 most recent ones. Looks like maybe something broke in the heal or reaper script during the fix. Or the rotate isn't working as well". Relayed to director-engine as a [decision] by belam (inbox director-engine.md:1970-1975, card 2c).
- (a) local registry CLEAN at 01:0xZ (7 live, 0 dead-pid entries, belam's measurement) -> the stale entries are the APP's. `rotate.py:11439` `_reap_chain` sends SIGTERM (`:11474`) then SIGKILLs a survivor after 5 s; a KILL'd `claude --remote-control` never disconnects, and no engine path ends/archives an app session (heal.py:2213 only *skips* owner remote-control files). UNMEASURED: whether a clean TERM disconnects the app session -- the round measures it first.
- (b) `heal.py:2256` `_judge_leases`: the verdict is `KEEP` only when the session id is in the meter-pin table (`:2308`); a live seat whose pin is STALE falls through every other branch to `REAP` (`:2319`). Reaper log (agi-reaper log line 564406): `pin-reap REAP: seat=stream-master ... window=@5` every pass -- SM's pin is gen 2, its seat gen 4 (the crash-recovery after_join pin never landed). Not killed ONLY because `.agi/config.json` `reaper` has no `pin_reap: armed` (`heal.py:2341` fail-closed dry-run): one config cell from killing the live stream seat.
- (c) `heal.py:855-861`: `_late_reap_for_skipped` returning `waiting` logs "late s12 reap waiting for belam: successor registry for @<id> still absent" with NO age bound -- a pre-reboot window it waits on forever.
- (d) the belam cap of 5 (`rotate.py:11560`, `:20038`) counts live tmux windows, not the app's session list.

## CLAIM
After any reap, rotation or reboot the app lists only live sessions, and pin-reap never names a seat's live session: (1) `_judge_leases` never returns REAP for a session whose pid is alive and is the seat's CURRENT registry session (row session_id / window match), whatever its pin says -- a stale pin yields a new non-arming verdict (`STALE-PIN`) plus one watch-log line; (2) the late-s12 wait is bounded (a declared config cell, not a literal) and past it the record is closed as `abandoned` with one log line; (3) the reap path ends a remote-control session cleanly (TERM with a grace long enough for the CLI to disconnect, measured) BEFORE any KILL, and where the CLI/API offers a way to end an app session of a dead pid, a sweep uses it -- if it offers none, the node records that as MEASURED and the claim's app half is a lean, never a fabricated pass.

## Dispatch line
config-max: the late-reap age bound and the TERM grace are cells under `.agi/config.json` `reaper.*` (never a literal) / template-max: none / code: the STALE-PIN branch in `_judge_leases`, the bounded wait in the late-reap loop, the clean-disconnect step in the reap path.

## FALSIFIERS
- a fixture seat with a live pid + stale pin still judged REAP -> claim (1) false
- after a TERM of a fixture remote-control process the app session is measured still live and no CLI path ends it -> the app half is disproved; say so (lean), do not paper it
- any test that touches a REAL pane, pid, unit, crontab or `~/.claude/sessions` -> the round is demoted (fixtures + seams only: `pid_alive`, `reaper`, `registry_dir`, `window_path`)

## TESTS
`extensions/agi/tests/test_heal*pin*` and `test_heal*late*` neighbourhoods (read them first); new: live-pid + stale-pin -> STALE-PIN never REAP; late wait past the bound -> abandoned once, not re-logged; reap order TERM -> grace -> KILL from the config cell.

## FILE SCOPE
`extensions/agi/bin/heal.py`, `extensions/agi/bin/rotate.py` (`_reap_chain` grace only), `.agi/config.json` (`reaper.*` cells only), `extensions/agi/tests/test_heal*.py` + one new test file. Nothing else. NEVER set `reaper.pin_reap: armed`.

## CEILING
ONE pi-free parent (tier 0), <= 3 kids, 10-12 production lines per conjunct, cap $1.
