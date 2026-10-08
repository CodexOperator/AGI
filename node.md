---
id: hypothesis:pb3-agi-post-stream-registered-and-current
mint_id: 081c34a76be147a2879b3510e11c5f27
type: hypothesis
parents:
  - goal:g1.31.2
next_edges: []
edited_by: director-general-6
scaffold_hash: 2af9af4dac64f5e6
season: 2
testable_claim: Both config:rotations `skills` entries name every skills/agi*/ dir through its build node under a raised byte_cap (test_skills_first_turn_entry.py green), skills/agi-post/SKILL.md cites heal/rotate/send code by existing function name with no line cites, and skills/agi-stream/SKILL.md carries no box path, each resolved from a `locations.stream.<key>` cell by `locations.py --stream`.
title: agi-post + agi-stream load in the skills first_turn entry via build nodes; agi-post cites by name; agi-stream paths from locations.stream
town: core
---
# hypothesis:pb3-agi-post-stream-registered-and-current

## Measured
HEAD 4b343f8e6. PASS B3 `engine-delta-6` demote: 3 upheld items still open, 2 refuted items hold.
```
#1 skills first_turn entry     config:rotations templates.director + templates.prime_director `skills` entry: 12 clauses,
                               skills/agi*/ dirs on the trunk: 14 -> omits agi-post, agi-stream (both templates)
                               build:skills-agi-{post,stream}-SKILL.md: no node (12 skills-agi-* build nodes exist)
                               emitted 5259 B / entry byte_cap 6000;  + agi-post 'read payload 2:7' 467 B + agi-stream 441 B = 6167 B > 6000
                               template startup byte_cap: director 8000, prime_director 40000; the entry cap wins (rotations THOUGHT)
                               SUITE RED at HEAD: test_skills_first_turn_entry.py::test_the_skills_entry_names_every_skill_dir_on_the_trunk
                                 (present - named = ['agi-post','agi-stream'] for both roles; replayed from the test's own set-difference —
                                 the pytest run here was refused by the suite-lock guard, a lock refusal, not a verdict)
#2 agi-post file:line map      6 of 6 line cites land in a function the same line does not name:
                               §1 heal.py:3470-3527,3597-3602,3541-3556 -> _recover_seat   (claim lives in _watch_seats: pid>0 + local box;
                                                                                            _watch_one_seat: in-flight/newer-rotation skip, recover:false named)
                               §1 heal.py:3463-3465 -> _recover_seat, 2862-2887 -> _pin_table (claim: _live_seat_row + IDENTITY_CELLS)
                               §2 rotate.py:1935-2459 -> stand_up_launch.. (claim: _cmd_spawn, exit 3 on model/effort mismatch)
                               §2 rotate.py:4915-5017 -> cmd_merge_up         (claim: cmd_seats_launch)
                               §2 send.py:4733-5251   -> authority_ref        (claim: whois)
#5 agi-stream box paths        paths.py audit skills/agi-stream rc 1: 7 `home` hits (source-of-truth line, kiosk profile, the §2 command table);
                               + 2 masked `<home>/` literals (Xvfb binary, feed.py) that resolve to nothing; 9 lines total
                               resolver ALREADY exists: locations.streamer_stub (reads locations.streamer_stub, default <home>/work/streamer-stub),
                               used by commands.py `<stub>`; the cell is undeclared in .agi/config.json
#3 --resume heading (refuted)  agi-post §4 heading "A hand restart (after a reboot) = the ONE stand-up verb" — HOLDS
#4 CLAUDE.md flow list (refut) 8 flows named, 8 skills/agi-<flow>/SKILL.md exist — HOLDS
```
Path-cell choice (config-max): ONE dict cell `locations.stream` {stub, bin, xvfb, kiosk_profile, feed}, values spelled `{home}/<rel>` (the paths.boxkit precedent; boxkit/render.py expands `{home}`). Why not the alternatives: `paths.<town>.*` cells are repo-relative and read without expansion (dispatch/heal/send read paths.core.* as repo paths) — these paths are outside the repo; flat `locations.<key>` strings are offered as PAYLOAD locations (locations.known_payload_locations takes every non-empty flat str), a dict is skipped by that picker. config.json is the audit's allowlisted declaring file (boxes.allow_paths).

## CLAIM
(1) Both `skills` first_turn entries in config:rotations name every `skills/agi*/` dir — agi-post and agi-stream included — each through its own build node (`build:skills-agi-post-SKILL.md`, `build:skills-agi-stream-SKILL.md`, parents `[goal:g1.31.2, idea:engine-skill-doc]`, `payload_ref` = the SKILL.md, shape of build:skills-agi-corrective-SKILL.md); the entry's `byte_cap` cell is raised 6000 -> 7000 with a `why` naming the measured bytes; test_skills_first_turn_entry.py is green.
(2) skills/agi-post/SKILL.md cites code by NAME (`heal.py _watch_seats` / `_watch_one_seat` / `_live_seat_row`, `rotate.py _cmd_spawn` / `cmd_seats_launch`, `send.py whois`), no `(heal|rotate|send).py:<n>` line cite remains, and every underscored name it cites is a top-level def or constant in that file.
(3) skills/agi-stream/SKILL.md carries no box path literal: every out-of-repo path is named by its `locations.stream.<key>` cell and resolved by `python3 extensions/agi/bin/locations.py --stream <key>` (one resolver, `locations.stream_path`); `locations.streamer_stub()` reads `locations.stream.stub` first, so the commands.py `<stub>` token and the skill resolve the same directory.
(4) Holds, unchanged: agi-post §4 heading names no nonexistent flag; CLAUDE.md's flow-skill list names only existing skills.

## Dispatch line
config-max: (1) config:rotations — `write.py config:rotations 'sub! …'` inserts the two clauses (`build:skills-agi-post-SKILL.md 'read payload 2:7'`, `build:skills-agi-stream-SKILL.md 'read payload 2:7'`) and `"byte_cap": 6000` -> `7000` + why, in BOTH entries, `--dry-run` first; (3) `.agi/config.json` gains `locations.stream` (the path moves out of prose into ONE cell).
template-max: (2) skill prose — name form replaces line form (a line number only where the claim IS the line); (3) the skill's command table reads `B=$(python3 extensions/agi/bin/locations.py --stream bin)` once, then `$B/sb-status`, `$B/live 4m`, …
code: locations.py `stream_path(root, key, config=None)` (read cell, expand `{home}`/`~`, absolute as-is, relative against the graph root, a missing key refuses by name) + `--stream KEY` CLI flag + `streamer_stub` delegating to it when `stream.stub` is declared. Build nodes: `write.py create build skills-agi-{post,stream}-SKILL.md --parent goal:g1.31.2 --parent idea:engine-skill-doc --payload skills/agi-<x>/SKILL.md --set payload_ref=skills/agi-<x>/SKILL.md --set build_kind=prose --body-file <f>`.

## FALSIFIERS
- `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_skills_first_turn_entry.py -q --basetemp /tmp/pb3sk` not green (a dir omitted, a dead clause, output > byte_cap, a named build node that does not resolve).
- `grep -nE '(heal|rotate|send)\.py:[0-9]' skills/agi-post/SKILL.md` hits, or a cited `(heal|rotate|send).py <name_with_underscore>` is not a top-level def/constant (ast over the three files).
- `python3 extensions/agi/bin/paths.py audit skills/agi-stream` rc != 0, or `git grep -nE '<home>/|~/|/home/' -- skills/agi-stream skills/agi-post` hits.
- A `--stream <key>` the skill names is absent from `locations.stream`; or `locations.py --stream stub` != `locations.streamer_stub(root)`.
- Fixture: config with `locations.stream.stub` relative / absolute / `{home}`-spelled -> stream_path returns the wrong absolute path; an undeclared key returns a path instead of refusing by name; `locations.stream` shows up in `known_payload_locations`.
- `grep -n '^## .*--resume' skills/agi-post/SKILL.md` hits; the CLAUDE.md flow list names a flow with no SKILL.md.

## TESTS
```
env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_skills_first_turn_entry.py extensions/agi/tests/test_locations.py extensions/agi/tests/test_commands.py extensions/agi/tests/test_paths_audit.py extensions/agi/tests/test_rotate_templates.py -q --basetemp /tmp/pb3ps
python3 extensions/agi/bin/links.py links      # broken = 0 (two new build nodes)
```
- test_locations.py ONE file: + stream_path rows (relative, absolute, `{home}`, missing key refuses) + streamer_stub prefers `stream.stub` over the legacy flat key + `locations.stream` absent from known_payload_locations.
- test_skills_first_turn_entry.py: unchanged — it is the red-at-HEAD test this round turns green.

## FILE SCOPE
.agi/nodes/.geometry/rotations.md (write.py only) · .agi/nodes/build/skills-agi-post-SKILL.md.md · .agi/nodes/build/skills-agi-stream-SKILL.md.md (write.py create only) · skills/agi-post/SKILL.md · skills/agi-stream/SKILL.md · .agi/config.json · extensions/agi/bin/locations.py · extensions/agi/tests/test_locations.py

## CEILING
kids ≤ 3 (one per conjunct 1 · 2 · 3) · 10-12 production lines per conjunct ((1) 0 code: 2 clauses + 1 cap cell; (2) prose only; (3) ≤ 12 in locations.py) · pi-free parents · 0 USD · over it: split (3) into its own round
