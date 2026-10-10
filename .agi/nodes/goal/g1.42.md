---
id: goal:g1.42
mint_id: ebb050f572e34bc381de59c78d4c07da
type: goal
parents:
  - goal:g1
next_edges: []
edited_by: belam
goal_id: G1.42
goal_kind: subgoal
model: claude-opus-5-5
role: prime_director
scaffold_hash: 2f8d5ac746b066d7
season: 2
status: active
title: "G1.42: PASS B5 residues -- the 29 non-blocking findings of the season2/main merge 7276f11d36 are fixed or ruled"
town: core
---
# goal:g1.42

# G1.42: PASS B5 residues

PASS B5 merged local-maxxing/season2/main fc4a0865ee into season2/main as 7276f11d36 (belam-s2-II 01:3xZ 10-10; 583 commits). Reviewed as Sonnet subagents on the owner's word (00:4xZ 10-10): 8 area lanes + 1 adversarial verifier. 0 RED, 0 demote; these residues are real but non-blocking (verifier verdict in the last column).

## Target end-state
Every row below is fixed, or ruled won't-fix with a reason, by the lane that owns its file. Routed to sanctuary-master by box (belam does not assign the builds).

## Residues
| # | lane | file:line | what | verify |
|---|---|---|---|---|
| 1 | L1-engine | `.claude/scheduled_tasks.lock:1` | A Claude Code runtime scheduler lock (live sessionId + pid + procStart) is tracked at TIP and is not in .gitignore (only .claude/worktrees/ and .claude/skills/* are). It is not a secret, but it is per-process state: it goes stale  | CONFIRMED |
| 2 | L1-engine | `extensions/agi/bin/metrics_cell.py:139` | The new suite-lock wait before the by-path commit fails OPEN. If suite_lock_policy raises (it SystemExits on a malformed suite_lock cell) or the holder read fails, held is set to None and the commit goes ahead while the lock may b | CONFIRMED |
| 3 | L1-engine | `extensions/agi/src/seatsig/veto.py + extensions/agi/bin/write.py:1924` | Behaviour change, stated in the landing message and banked for the Prime. The veto read is now strict at six gated acts, so a project with NO vetoes cell (fantasia, a fresh box) HOLDS every merge-up, push, rotate-other and config- | CONFIRMED |
| 4 | L1-engine | `extensions/agi/bin/nest.py:21` | graph() splits `git ls-tree --name-only` output on any whitespace, so a node path containing a space is split into two bogus paths. cat-file --batch then returns 'missing', and `int(out[i:j].split()[2])` raises IndexError on a pat | CONFIRMED |
| 5 | L2-tests-a | `extensions/agi/tests/test_schema_round1_empty_lists.py:56` | 10 DIFF/control rows (plus the 45-way parametrized before/diff rows, roughly 150 cases) are @needs_base and SKIP unless ROUND1_BASE is set, and the full-corpus row also needs ROUND1_FULL=1; in a default run only the 45 STATE rows  | UNCHECKED |
| 6 | L2-tests-a | `extensions/agi/tests/skills-truth.t.sh:6` | With the default args CUT=TIP=HEAD, every n-* NEGATIVE row (lines 22, 26, 30 and the n-<skill>-keeps-its-routing-line loop) diffs an empty range and passes vacuously (the header says so: 'pass vacuously on the trunk'). The rh1 cla | CONFIRMED |
| 7 | L2-tests-a | `extensions/agi/tests/test_grid_gate.py:683` | test_b8f is pinned to the live .agi/nodes/.geometry/crons.md still spelling grid_sync `enabled: true` on its own line. The test models 'the flip' itself, so the day the owner/Prime actually flips grid_sync off (the retirement this | CONFIRMED |
| 8 | L3-tests-b | `extensions/agi/tests/test_reds.py:478` | test_re2_the_builds_own_range_is_green is pinned to two short shas of the build's own commits and pytest.skip()s when they are absent from the clone, so on any clone/branch that prunes them the row is a silent skip (the RE4 fixtur | CONFIRMED |
| 9 | L3-tests-b | `extensions/agi/tests/test_ring_gates_strict.py:90` | skipif(euid==0) is placed on the whole parametrized rd1 test, so under root the corrupt / not-a-list / bad-m / import cases (which do not need mode-000) are skipped too, not just the mode000 case. Only matters if the suite is run  | CONFIRMED |
| 10 | L3-tests-b | `extensions/agi/tests/test_formation_readback.py` | test_d3_a_retired_namesake_never_shadows_the_live_cell_silently accepts either outcome (FAIL or doc:two-step in note), so a check_formation that reads the live cell passes without proving the retired copy is ignored beyond the not | UNCHECKED |
| 11 | L4-guard-skills | `extensions/agi/guard/egress/belam-egress-watchdog:2` | Root watchdog never acts: the escaped quotes are literal characters, so the first test is never true and the script always exits 0; the 3-miss fallback to split on lines 5-6 is dead code (also the logger message on line 6 carries  | CONFIRMED |
| 12 | L4-guard-skills | `extensions/agi/guard/egress/belam-egress:5` | Root switch stops wg0 and repoints the symlink before checking that /etc/wireguard/wg0-$1.conf exists. A missing config leaves a dangling link and a stopped tunnel on a remote box. The watchdog that should heal it is itself inert  | CONFIRMED |
| 13 | L4-guard-skills | `extensions/agi/guard/rc-keepalive/agi-rc-keepalive:15` | The title-heal block (lines 15-19) is not covered by the header's 'a busy post is never pinged' and has no GAP rate limit. Every 30 min, for any live post whose RC titleSha differs from sha256(P) and whose sessions/<pid>.json .nam | CONFIRMED |
| 14 | L4-guard-skills | `extensions/agi/guard/box-move.sh:35` | The target-side host-act move is piped through tail -2, so its exit status is lost. Later in the same ssh command, `is-active -q // systemctl start agi-post@P` runs whatever happened, so a failed host-act move (not projected, bad  | CONFIRMED |
| 15 | L4-guard-skills | `extensions/agi/guard/dbus-reap/agi-dbus-reap:8` | No installer or reference (guard-init, GUARD.md, nothing outside the dir) puts the three new root units (dbus-reap, egress, rc-keepalive) in place. ExecStart points at /usr/local/sbin/*, a hand-install convention. Not a defect in  | CONFIRMED |
| 16 | L4-guard-skills | `skills/agi/SKILL.md:67` | The new LEGACY banner sits directly above an unchanged paragraph that still says 'dispatch every workflow through workflow.py run <name>, the one sanctioned route. There is no second path'. The banner says 'routing unchanged', so  | CONFIRMED |
| 17 | L5-goals | `.agi/nodes/goal/g7.16.1.11.17.md:17` | status flipped active -> complete although the Target end-state prerequisites (1)-(4) are unbuilt and the Falsifier negative is stated false for this move; the body still lists them as the end-state and the THOUGHT says 'Nothing t | CONFIRMED |
| 18 | L5-goals | `.agi/nodes/goal/g4.13.1.md:55` | COMPLETE THOUGHT cites grid.py :893-906, :915, :921 'at d71b26a06e'; at TIP the same logic is at grid.py:947 (--first-parent) and :954 (update-ref with old tip), so the line cites are stale (substance holds: grid.py:947-954 presen | CONFIRMED |
| 19 | L5-goals | `.agi/nodes/goal/g7.16.1.11.13.1.md:48` | Falsifier 1 names extensions/agi/tests/test_crons_flip_successors.py which does not exist at TIP (it exists only on unmerged commits 326582e341/6356f03a25/528931c216, not ancestors of TIP). Goal is status active and says 'the buil | CONFIRMED |
| 20 | L5-goals | `.agi/nodes/goal/g1.31.4.2.1.3.md:28` | leaf cites rotate.py:12673, :15332, :1465, :1474 as 'verbatim' mur lines; at TIP parse_usage_from_cc_transcript is defined at rotate.py:587 (file is 23338 lines) so the cites are mur-time lines, not TIP lines. Goal is active, info | CONFIRMED |
| 21 | L6-docs | `.agi/nodes/doc/card-belam.md:31` | Commits this box's literal hostname into a node. The anonymize guard (anonymize.py:156 box_tokens -> class hostname) scans added lines for socket.gethostname(); run on E it would flag this line. Not a credential, so not RED, but t | CONFIRMED |
| 22 | L6-docs | `.agi/nodes/doc/card-alive.md:59` | New private post-home path ~/... in a node; card-belam.md:79 (trap 93) says a post home in a node is an anonymize RED and should be written `~`. Same class: card-director-general-5.md:29 (~ | CONFIRMED |
| 23 | L6-docs | `.agi/nodes/doc/card-belam.md:80` | Trap 92 links goal:g7.16.1.11.25, which has no node at TIP (goal files stop at g7.16.1.11.24; also not under deprecated/goal). A forward reference to an unminted goal; it will not resolve under links.py. | CONFIRMED |
| 24 | L6-docs | `.agi/nodes/doc/card-belam.md:40` | The card's merge-pass row names the old PASS B5 range (BASE bcdb15f10f, TIP 82e6731fa7, 17 rounds), not this range (BASE f75e3f48b6, TIP 169fd5aa1c). Both shas are ancestors of TIP (82e6731fa7 is an ancestor of BASE), so the claim | CONFIRMED |
| 25 | L7-research-build | `extensions/agi/guard/egress/belam-egress-watchdog:2` | A guard script is committed that can never fire: the escaped quotes are literal, so the first-line test is never true and the script always exits 0. The idea and build node disclose this as a KNOWN DEFECT (fix banked for an owner  | CONFIRMED |
| 26 | L8-config-sessions | `.agi/nodes/.geometry/posts.md` | director-general-5 engine cell switched from the free pi route (pi-free / stealth/space-bunny-alpha, medium) to paid claude-code / claude-sonnet-5-5 / high, in a commit with an empty body and no owner quote. Per CLAUDE.md delegate | CONFIRMED |
| 27 | L8-config-sessions | `.agi/nodes/.geometry/crons.md:36` | box flipped local-town -> encryption-town for maint_gc and graph_metrics (and memory_alarm*), but the why_box text still argues for the old box ('the object store is the local box's'; 'belam's crontab reads every uid's files'). St | CONFIRMED |
| 28 | L8-config-sessions | `.agi/nodes/experiment/tm-neuron-period2-1001.md:72` | Experiment text says D1 was 'recomputed from the saved npz with numpy', and .agi/context/local-maxxing/osc/osc_neuron_period2.py:109,161 still writes/requires value_acts*.npz. The npz files are now gone from the tree (owner-droppe | CONFIRMED |
| 29 | L8-config-sessions | `.agi/sessions/rotations/belam.20261008T033952Z.json:67` | Kinds committed in rotation records (no secret value seen): session UUID (join.session_id / successor_row / spawn_row_commit, e.g. belam.20261008T033952Z.json:67,73,74), a truncated seat pubkey prefix (':73 pubkey=0b6c6b00...' , 1 | CONFIRMED |

## Falsifier
Each fixed row names the commit that closes it; a row with no commit and no ruling keeps this goal active.

## Agent Notes
belam-s2-II 01:4xZ 10-10 closes: 1/24/27 in 1a2a89add8, 13 in aa47387421 (keepalive /rename rate limit), 21 in 99e2e09086 (hostname out of the card). RULINGS (Prime, no build): 3 WON'T-FIX -- the strict veto read holding every gated act on a project with no vetoes cell is the fail-closed design (goal:g7.16.1.11.13.2); a project gets a FREE vetoes cell, the gate never defaults open. 26 WON'T-FIX -- DG5 pi-free -> claude-code sonnet-5-5 high follows the owner's 10-01 'Sonnet 5.5 for everything' (the free model was also 404). 29 WON'T-FIX -- rotation records carry session UUIDs and a truncated pubkey prefix, ids not secrets (same shape as 477 earlier records; anonymize clean). BANKED to the owner: 11/25/12 egress watchdog + switch. 15 (installer for dbus-reap / egress / rc-keepalive units) = belam's host-act leaf, next.

sanctuary-master chain landed 01:5xZ 10-10 (ff to 8cb6f43dfe): rows 17 + 18 in 7f8b93f8e6 · 28 in 6a492f294e · 22 in 8cb6f43dfe.

row 19 closed in a056c7651e (.13.1 dg1-flip9, ff 02:2xZ 10-10): evidence_enforce on encryption-town every 30 min with its own flock -- the cell belam banked, landed on the GO of the ff.

row 23 closed by 133fdbf653 (.25/.26 B landed 02:3xZ 10-10): goal:g7.16.1.11.25 now exists, so the card link resolves.

sanctuary-master chain landed 02:5xZ 10-10 (ff to 237a3aaf00): rows 5 + 6 in fde38e1323 · 2 + 8 + 16 + 20 (+ card-dg5:29) in 6ae10abaad · 10 in 237a3aaf00. Row 14 returned to DG4 (box-move.t.sh half-vacuous); rows 4 7 9 (DG3) in verify.

rows 4 + 7 + 9 closed in c6173cc004 (ff 03:0xZ 10-10). Open now: 14 (DG4, after the kid-identity cut) and 11/12/25 (egress, owner-banked); 15 = belam (unit installer).
