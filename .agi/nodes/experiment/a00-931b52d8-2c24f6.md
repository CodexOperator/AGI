---
id: experiment:a00-931b52d8-2c24f6
mint_id: 72a40d26b26b438abccd529e79c5db5c
type: experiment
parents:
  - hypothesis:l5-the-meter-captures-the-final-card-and-forces-the-rotation-itself
next_edges: []
confidence: 0.85
edited_by: a00-c6d54e05
evidence_runs:
  - experiment:a00-931b52d8-2c24f6
line_ceiling: 44
loop: hypothesis:l5-the-meter-captures-the-final-card-and-forces-the-rotation-itself@s2
model: deepseek/deepseek-v4.1-flash
probes: "\"kid-C1 idle@ratio: argv=[rotate,--post,kid-1] env AGI_POST=advisor dms=0 OK. kid-C2 below-ratio: hold no child no dm OK. kid-C3 over-line: rotate no dm OK. kid-C4 cell 0.5 lane 0.20 f=0.21: 1 spawn OK. kid-C5 cell ABSENT f=0.9*line idle 60m: HOLD OK. kid-C6 no literal 0.85 in cmd_alarms OK. kid-C7 unkeyed holder: refusal by name, nothing spawned, no dm OK. PARENT-PB1 wire: idle 60m f=0.42 line 0.40 ratio 0.85 -> _spawn_master_rotate exactly once, argv [rotate,--post,kid-1], env AGI_POST=advisor, 0 dm: HELD. PARENT-PB2 gate: unkeyed holder -> no spawn, no dm, refusal by name: HELD. PARENT-PB3 gate: captive_rotate_ratio ABSENT -> 0.9*line idle 60m stays held: HELD. PARENT-PB4 auth: role parent / prime_director / master-named-with-cell-false at f>=line -> 0 spawn 0 dm: HELD. PARENT-PB4d auth: master-named WITH captive_rotate_masters true -> 1 spawn, 0 dm: HELD. PARENT-PB5 adversarial: over-line NON-director gets no dm and no rotate -- the dm lane was removed for every role, so a held non-director is now silent: CAVEAT, not a claim falsifier (owner scoped the rotate to directors and said the alarms path becomes this).\""
production_lines: 54
profile: balanced
role: kid
scaffold_hash: 4cd1be5f45ed7b20
season: 2
title: "trigger (b): the alarms meter rotates an idle held seat by the master path at captive_rotate_ratio x the line, no dm"
town: core
verdict: proved
---
# experiment:a00-931b52d8-2c24f6

## Experiment

BUILT CAPTIVE AUTO-ROTATE TRIGGER (b) (owner ruling 05:1xZ, slice 2,
`hypothesis:l5-the-meter-captures-the-final-card-and-forces-the-rotation-itself`),
red-first. The timed meter poller `rotate.py cmd_alarms --holder H` no longer
nudges an idle director: when the lane fires it ROTATES the held seat directly
by the MASTER PATH — `rotate.py rotate --post <seat>`, detached, with
`AGI_POST=<holder>` so `_caller_post` resolves the holder's key — and sends NO
dm.

Changed in `extensions/agi/bin/rotate.py` (`cmd_alarms` + two new helpers):
- the idle lane's `low_line = 0.85 * threshold` literal is GONE. The ratio is
  `load_ladder_field(root, "captive_rotate_ratio", None)`; **absent = the idle
  lane is OFF by name**, exactly like trigger (a). `captive_rotate_masters`
  (default false) gates *master*-named seats.
- lane = `f >= director_rotate_at` (over-line, unchanged) OR
  (`idle >= alarms_idle_minutes` AND `f >= ratio * line`). Below both: `hold
  <seat> <fraction>`, unchanged.
- firing calls the new `_master_rotate(root, holder, seat, row, masters)`:
  DIRECTOR role only, never the Prime (`_is_prime_role`), a `*master*`-named
  seat only when the ladder cell is on; then it pre-checks the HOLDER's own
  signing key with the existing `_caller_hold_key` so the refusal is printed BY
  NAME *before* any spawn (otherwise cmd_alarms would print success and the
  detached child would refuse silently).
- the ONE detached child seam is `_spawn_master_rotate(argv, env, cwd)`
  (`subprocess.Popen`, `start_new_session=True`, stdio DEVNULL, cwd=root);
  tests monkeypatch that, never `subprocess.run`, and no pytest reaches a real
  `rotate.py rotate`.

Ladder cells were ALREADY present (written by kid trigger-(a),
`experiment:a00-3a04e059-da77bd`); I did NOT touch `ladder.md`.
`rotation_alert.py` and `heal.py` untouched — the trigger fits the existing
alarms lane, so no heal.py edit was needed.

Production lines: `git diff --numstat -- extensions/agi/bin/rotate.py` = 54
added / 21 removed (added-lines convention, matching the predecessor's 81 for
78+/3-). Ceiling 44 (dispatch), 16 (kid brief); 54 is under the 2x stop of 88,
so no `rebrief_request` is owed, but it is 1.23x the dispatch ceiling — the
overage is the docstring rewrite plus the refusal pre-check and the seam.

## Evidence

RED FIRST: `python3 -m pytest extensions/agi/tests/test_rotate_alarms_captive.py -q`
-> 8 errors (`AttributeError: module ... has no attribute '_spawn_master_rotate'`)
before the build. GREEN after: 8 passed.

SUITE (files I changed / that cover the changed file):
`python3 -m pytest extensions/agi/tests/test_rotate_alarms_captive.py
extensions/agi/tests/test_rotate_alarms_idle.py
extensions/agi/tests/test_dispatch_alarms.py
extensions/agi/tests/test_rotation_alert_captive.py
extensions/agi/tests/test_ladder_node.py
extensions/agi/tests/test_heal_ack_rotation.py -q`
-> **45 passed**, 0 failed. (`test_rotate_alarms_idle.py` was amended: its old
`test_alarms_idle_below_line_dms_held_seat` asserted the DM the ruling
replaces; it now asserts the master-path rotate and its `fake_ladder` declares
`captive_rotate_ratio: 0.85`.)

INDEPENDENT PROBES against the built bytes
(`.agi/sessions/iter-154/a00-931b52d8/probes_b.py`, output `probes_b.out`), one
per conjunct, seam hand-patched so nothing real spawns:
- C1 idle 60m f=0.42 (line 0.40, ratio 0.85 -> lane 0.34): argv
  `['rotate','--post','kid-1']`, env `AGI_POST='advisor'`, cwd=root, **0 dms**.
- C2 f=0.10: hold kid-1 0.1000, 0 children, 0 dms.
- C3 f=0.50 (>= line): rotate directly, 0 dms.
- C4 ladder cell 0.5 -> lane at 0.20, f=0.21 rotates.
- C5 cell ABSENT -> f=0.36 (0.9*line) idle 60m HELD.
- C6 no literal `0.85` remains in the `cmd_alarms` region; the cell is read.
- C7 REAL `_caller_hold_key` on an unkeyed holder: `cmd_alarms` returns 0 and
  prints `captive rotate refused: holder 'advisor': post 'advisor' is unkeyed:
  python3 .../send.py keygen --post advisor first` — nothing spawned, no dm,
  no silent fallback.
- LIVE ladder read in this tree: `director_rotate_at 0.47`,
  `alarms_idle_minutes 20`, `captive_rotate_ratio 0.85`,
  `captive_rotate_masters False`.

## The heal-watch / "timer is live" question (requirement 4)

The timer IS live — but it is NOT the crons.md-declared unit, and it does not
run these bytes:
- declared (`.agi/nodes/.geometry/crons.md`): service
  `agi-alarms-sanctuary-master`, enabled, exec_start
  `/usr/bin/python3 {repo_root}/extensions/agi/bin/rotate.py alarms --holder
  sanctuary-master --root {root}`, working_directory `{repo_root}`. `crons.py`
  would render it as `agi-agi-alarms-sanctuary-master-<hash>.service`.
- actually running: a TRANSIENT hand-made unit
  `agi-sanctuary-master-alarms.service` (active, running, MainPID 2672828,
  since 01:03:06 EDT), `WorkingDirectory=/home/ubuntu/work/agi/.agi/worktrees/alarms-trunk`,
  ExecStart `/usr/bin/python3 extensions/agi/bin/rotate.py alarms --holder
  sanctuary-master --interval 120` (relative path, no `--root`, no `--once`).
  `~/.config/systemd/user/` holds no alarms unit file (only the reaper,
  `agi-agi-reaper-2f118e6f.service`).
- the live unit's checkout `worktrees/alarms-trunk` (HEAD 21155f1b4) has
  `grep -c "_master_rotate|captive_rotate_ratio" rotate.py` = **0**: production
  alarms today does NOT carry trigger (b). Consequence stated plainly: this
  round builds and proves the behaviour, but the live poller executes another
  worktree until that tree carries the merged change (and the transient unit
  is replaced by, or re-pointed at, the declared service). NOT fixed here —
  `crons.md` service rows and the live crontab/unit surface are outside this
  kid's file scope; the finding is the deliverable.

Raw output, screenshots, logs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-c6d54e05). (1) INSTRUCTION: the parent brief says "read each kid DIFF, never its result file ... run one negative probe per claim conjunct yourself ... a kid that passes its own suite but fails your probe is lean_disproved with the probe named". (2) MACHINE: I read `git show 12b3bdb4a -- extensions/agi/bin/rotate.py` (54+/21-: cmd_alarms idle lane rewired to the ladder cell, the dm+`import send` removed, `_master_rotate` with the `_caller_hold_key` pre-check and `_is_prime_role`/master-name scope, and the ONE `_spawn_master_rotate` Popen seam) and ran six probes from /home/ubuntu/work/agi/.agi/worktrees/post-sensei-director/.agi/sessions/iter-154/a00-c6d54e05/probes_b_parent.py against the built bytes: PB1 wire, PB2 gate (unkeyed holder), PB3 gate (cell absent = idle lane off), PB4 auth (parent/prime/master-default), PB4d auth (master+cell true) all HELD. I also confirmed the holder key is genuinely resolvable on this box: `_caller_hold_key(root, "sanctuary-master", row, "env")` returns the seat (the key file exists in the shared sessions dir), so the refusal pre-check is not a blanket block. (3) NEAR MISS: PB1/PB4d first read FALSIFIED with n_spawn=0 and looked like a real dead lane; the cause was MY probe fixture omitting the `director_context_tokens` ladder cell, so `_seat_fraction` read None and cmd_alarms skipped the row before any gate. The built lane was correct; the probe harness was wrong. Named because a weaker probe would have demoted a correct kid. (4) DEVIATION: none from the standing rules. I ACCEPT the kid proved, on the bytes, with two caveats: (a) PRODUCTION REACHABILITY -- the kid disclosed that the live alarms unit is a transient hand-made `agi-sanctuary-master-alarms.service` running worktrees/alarms-trunk (0 trigger-b bytes), NOT the declared crons.md service; so the mechanism is built and proved in this tree but the running poller does not execute it. That is a deployment step outside the kid file scope, recorded as push_further, not a code defect. (b) The over-line lane lost its dm for EVERY role, so a held NON-director seat (parent/council) is now silent (PB5); the owner scoped the captive rotate to directors and said the alarms path becomes the rotate, so this is intended scope, but it is a behaviour loss for non-director held seats and is named.
<!-- THOUGHT:END -->

## Agent Notes
Trigger (b) built red-first: cmd_alarms rotates an idle held director by the master path (rotate.py rotate --post <seat>, AGI_POST=<holder>) at captive_rotate_ratio x the line from the ladder (absent=idle lane off), no dm; over-line lane also rotates directly; unkeyable holder refuses by name before any spawn. 8 new tests (3 error-red before build) + 45 passed across the 6 covering files; 7 independent probes. CAVEAT: the live alarms timer is a transient hand-unit agi-sanctuary-master-alarms.service running worktrees/alarms-trunk (0 trigger-b bytes), NOT the crons.md-declared agi-alarms-sanctuary-master — production does not yet execute this change. 54 production lines vs 44 ceiling (under 2x stop).

PARENT (a00-c6d54e05) ACCEPTED, verdict proved on the bytes: 6/6 claim-conjunct probes held (PB1 wire, PB2/PB3 gate, PB4/PB4d auth). Two caveats recorded, not demotions: (a) the LIVE alarms poller runs worktrees/alarms-trunk with 0 trigger-b bytes, so production does not yet execute this change -- a deployment step, push_further; (b) the over-line dm lane was removed for every role, so a held non-director is now silent (PB5) -- intended director scope, named.
