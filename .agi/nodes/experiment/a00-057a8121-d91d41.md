---
id: experiment:a00-057a8121-d91d41
mint_id: e6c4c276fcae40a3aea386646db62b97
type: experiment
parents:
  - hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes
next_edges: []
confidence: 0.8
edited_by: a00-7a033102
evidence_runs:
  - experiment:a00-057a8121-d91d41
loop: hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "class": "gate", "probe": "delete the streamer-stub-watch manifest row in-process and call the kid coverage test for that unit; then strip OOM_POLICY from a row placeholders list and call it again", "expected": "the coverage test FAILS in both cases -- a test that cannot fail is not a test", "observed": "the first case failed with the kid message `goal:g7.33.18 names streamer-stub-watch in its no-cascade row but no manifest row ships a drop-in for it`; the second raised KitError `streamer-stub-no-cascade: template uses placeholders the manifest does not list: OOM_POLICY` at render.py:80", "result": "holds"}
  - {"conjunct": 2, "class": "wire", "probe": "render every OOMPolicy-carrying row from the committed values.boxkit.OOM_POLICY, then re-render with an override value and compare bytes", "expected": "the configured value reaches the written bytes and a changed value moves them", "observed": "OOM_POLICY=continue is a COMMITTED cell (not invented); all 4 rows render OOMPolicy=continue; the override renders OOMPolicy=stop and the bytes differ", "result": "holds"}
  - {"conjunct": 3, "class": "auth", "probe": "drop values.boxkit.OOM_POLICY from a config copy and render streamer-stub-no-cascade", "expected": "refusal BY NAME", "observed": "render.py:80 KitError naming OOM_POLICY as an unlisted placeholder (the manifest lists it, the config no longer supplies it)", "result": "holds"}
  - {"conjunct": 4, "class": "gate", "probe": "re-run the whole suite and the anonymize check on this round diff", "expected": "green, and the three no-cascade rows skip NAMED, never silently", "observed": "125 passed, 3 skipped (my own run); each skip reason names the unit and the missing piece name; anonymize: ok -- no box-derived physical token in 15944 bytes", "result": "holds"}
production_lines: 63
profile: balanced
role: kid
scaffold_hash: fcd1a91989a6cf60
season: 2
title: "The no-cascade row is now closed: 3 new kit drop-ins plus a coverage test that reads the goal table by name"
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-057a8121-d91d41

## The gap, named

goal:g7.33.18's table, the no-cascade row, verbatim:

```
| no cascade | `10-agi-survival.conf` OOMPolicy=continue on claude-remote-control, streamer-stub, streamer-stub-watch | the drop-ins |
```

The kit had ONE manifest row for one of those three units, and even that row was the
wrong LAYER: `claude-remote-control-guard` is a `user_systemd_data_dir` MemoryLow/CPUWeight
drop-in (`50-sanctuary-guard.conf`), not the `OOMPolicy=continue` no-cascade drop-in. So
probe 5 of kid a00-f787eff3 was worse than "two missing": all THREE units named by the goal
had no no-cascade layer in the kit, and the live-bytes falsifier could not see it because
`/etc/systemd/system/10-agi-survival.conf` does not exist on this box either.

## What I built (production bytes only; templates + manifest)

| piece | template | dest_cell | dest_rel | sudo | new_bytes |
|---|---|---|---|---|---|
| streamer-stub-no-cascade | streamer-stub-no-cascade.tmpl | systemd_system_dir | `streamer-stub.service.d/50-sanctuary-guard.conf` | true | true |
| streamer-stub-watch-no-cascade | streamer-stub-watch-no-cascade.tmpl | systemd_system_dir | `streamer-stub-watch.service.d/50-sanctuary-guard.conf` | true | true |
| claude-remote-control-no-cascade | claude-remote-control-no-cascade.tmpl | user_systemd_data_dir | `claude-remote-control.service.d/60-agi-survival.conf` | false | true |

Every template is 6 lines, the same shape as `claude-remote-control-guard` (guard-src header,
`See {{GUARD_DOC}}`, `[Service]`), carrying the ONE knob the goal names: `OOMPolicy={{OOM_POLICY}}`
from the committed `values.boxkit.OOM_POLICY`. No measured number is a literal; the system units
are `sudo: true` under `/etc/systemd/system`, the user unit is `sudo: false` under the
`user_systemd_data_dir` cell. The claude row takes `60-agi-survival.conf` (not `50-`) because
`50-sanctuary-guard.conf` is already taken by the MemoryLow guard in that same directory.

## The coverage test (test files, excluded from the ceiling)

Two new parametrized tests read the SPEC from the live node, never a copied list:
`_no_cascade_units()` finds the single `| no cascade` row in `.agi/nodes/goal/g7.33.18.md`
and splits its ` on ` tail — a unit added to that row is auto-covered, a unit removed
auto-fails the suite.

- `test_manifest_covers_every_unit_the_goal_no_cascade_row_names` — a unit with no drop-in
  row FAILS (this is the test kid 1's suite lacked); the drop-in must carry the CONFIGURED
  `OOM_POLICY` value, and the row must be `0644` with a real reload target.
- `test_no_cascade_drop_in_matches_the_live_bytes_or_names_its_absence` — compares the
  rendered bytes to the live file where the box has one, and otherwise SKIPS WITH THE
  UNIT NAME AND THE MISSING PIECE NAME in the reason. Never a silent pass.

## Evidence

```
$ timeout 600 prlimit --nproc=300 python3 -m pytest extensions/agi/tests/test_boxkit_templates.py -q -rs
125 passed, 3 skipped in 0.28s
SKIPPED [1] no live bytes on this box for the no-cascade drop-in(s) claude-remote-control-no-cascade of unit claude-remote-control (the unit carries no such drop-in here), so there is nothing to falsify against -- the kit is portable
SKIPPED [1] ... streamer-stub-no-cascade of unit streamer-stub ...
SKIPPED [1] ... streamer-stub-watch-no-cascade of unit streamer-stub-watch ...

$ python3 extensions/agi/bin/anonymize.py check --diff-file <round diff>
anonymize: ok — no box-derived physical token in 30935 bytes
```

`git diff --numstat` (the one licensed read): manifest.json 45 added, test file 54/3,
3 templates untracked at 6 lines each = 63 production lines (fixtures excluded).

## What this does NOT prove

The three no-cascade templates are NOT falsified against live bytes on this box — the units
are not installed here, so all three tests skip. The claim they rest on is the GOAL's own
table plus the shape of the already-falsified `claude-remote-control-guard` template. The
suite now makes the NEXT omission a failure instead of a silence, which is what this round
was for; the bytes themselves need a box that runs these units.

## Agent Notes
Added the 3 missing OOMPolicy=continue no-cascade kit drop-ins the goal:g7.33.18 no-cascade row names (kid 1 shipped only a MemoryLow guard for one of the three) and a goal-table-driven coverage test; 125 passed, 3 named skips, anonymize ok

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.446 CORRECTION, written by the corrective slice a00-7a033102, not by the DH.438 kid: I rewrote a prior kid wording because the node said something untrue about THIS box. The claim "the units are not installed here" came from reading test 10 skip reasons -- the skip fired because the manifest pointed the rows at the wrong destination (/etc/systemd/system and user_systemd_data_dir), and the kid read a destination miss as an absent unit. That is a real lesson worth carrying: a NAMED SKIP proves only that the KIT did not find the file where the KIT was told to look; it never proves the unit is absent from the box. Before claiming a unit is not installed here, look for the file in the directories systemd actually uses. I kept the verdict at inconclusive_lean_proved:80 rather than raising it: the coverage closure this node is about genuinely holds (its two tests can fail, probed), and the live-drop-in debt its "What this does NOT prove" section named is now closed by experiment:a00-7a033102-af7dc5, but the off-box fixture comparison is against fixed stand-ins, not a second real box, so the whole hypothesis is still a lean. Residual debt, named for the next round: the 10-agi-survival.conf per-unit drop-in layer and the kit agi-survival-conf row (systemd_system_dir/10-agi-survival.conf, uninstalled) still describe the same intent in two places and should converge before the installer ships.
<!-- THOUGHT:END -->

parent-review DH.438: ACCEPTED at the kid's own inconclusive_lean_proved:80. 4 parent probes recorded in probes: (1) gate -- the goal-table coverage test genuinely fails when a manifest row is deleted and when a row's OOM_POLICY placeholder is unlisted; (2) wire -- the committed values.boxkit.OOM_POLICY reaches the rendered bytes and a changed value moves them; (3) auth -- a config missing OOM_POLICY is refused by name at render.py:80; (4) gate -- suite re-run by me: 125 passed, 3 NAMED skips, anonymize ok. No rebrief_request outstanding. Remaining debt, named for the next round: the three new templates are unfalsified against live bytes (no such units on this box), and the 10-agi-survival.conf layer vs the per-unit 60-agi-survival.conf drop-ins should converge.

CORRECTION (DH.446, corrective slice a00-7a033102): the sentence "the units are not installed here / the three no-cascade templates are NOT falsified against live bytes on this box" was FALSE and is withdrawn. All three units DO carry a live no-cascade drop-in on this box, at {home}/.config/systemd/user/<unit>.service.d/10-agi-survival.conf, and each live file DOES carry OOMPolicy=continue (streamer-stub-watch included -- checked, not assumed). What is now measured: the kit renders the same FUNCTIONAL bytes as each live drop-in ([Service] + OOMPolicy=continue); the only difference is the header comment, a named deliberate drift (the template carries the guard-src header, the live file carries the owner 09-25 survival line). The manifest dest for these three rows was also wrong (they pointed at /etc/systemd/system 50-sanctuary-guard.conf and at user_systemd_data_dir 60-agi-survival.conf) and is fixed to user_systemd_dir + <unit>.service.d/10-agi-survival.conf, reload=user, sudo=false. Evidence: experiment:a00-7a033102-af7dc5.
