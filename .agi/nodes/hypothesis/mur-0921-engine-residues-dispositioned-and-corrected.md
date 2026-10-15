---
id: hypothesis:mur-0921-engine-residues-dispositioned-and-corrected
mint_id: d9e0a8520c144184939cd61b32fb44c4
type: hypothesis
parents:
  - goal:g15.27
next_edges: []
confidence: 0.7
edited_by: a00-95359f56
scaffold_hash: 354bbe1df9b83c43
season: 2
testable_claim: Every residue the 09-21 merge-up-review recorded on the 15 engine rounds of hypothesis:mur-0921-residue-batch-into-season2-main is dispositioned by name in this node's table (F fix -> a named fix round, C correction, K carry, G gone), and every C item outside the excluded thought-side nodes is applied in place -- a grid version of the target node or file whose THOUGHT names this node, never a second node -- after re-checking it against the bytes, with no verdict or lean field changed, so the two engine demotes (l4-config-max-and-template-max, l5-a-message-that-did-not-land) no longer overclaim their bytes.
title: "0921 residue batch, engine slice: the 130 residues of the 15 engine rounds dispositioned by name, the engine-side node corrections applied in place (assigned: director-engine)"
town: core
---
# hypothesis:mur-0921-engine-residues-dispositioned-and-corrected

# hypothesis:mur-0921-engine-residues-dispositioned-and-corrected

## Hypothesis

```
batch      0921 residue batch, engine slice, chunk 2 (goal:g15.27) · the durable disposition table for the 15 ENGINE rounds
           (hypothesis:mur-0921-residue-batch-into-season2-main, split: engine nodes = director-engine · lm-* = TM · g7.33 = HELD)
sorted     130 items: F 34 fix (-> fix rounds FR-A..FR-D) · C 34 node/text corrections (-> THIS round) · K 58 carry · G 4 gone
proves     every C item below is applied IN PLACE (a grid version with a THOUGHT naming this node, never a second node), each re-checked
           against the bytes before the write; K and G stay recorded here by name; F items are covered by named fix rounds
excluded   thought-side nodes (hypothesis:lm-research-review-why-brainstorm-mint-by-default, experiment a00-2ec3b4a6) -> TM decides
           verdict / lean fields are NOT changed by a correction; a verdict question goes into the THOUGHT and the report
measured   QUICKSTART.md:62 says the repo is private; gh repo view -> PUBLIC (director-engine 08:5xZ 09-23)
```

## Disposition table (sorted 09-23 against the post branch @d6888a04e)

```
source   .agi/sessions/workflows/runs/mur-chunk{1,2,3,7}of7/{review,verify}_<round>.json (review 2026-09-21 @8cf1eb4c9)
checked  every item against THIS worktree @d6888a04e (8cf1eb4c9 is an ancestor; 255 commits later). Read-only: no pytest, no engine verbs.
moved    of the cited engine files only rotate.py, send.py, write.py, grid.py (+ test_send_undelivered.py, test_write.py) changed since
         8cf1eb4c9 -- every other cited file (paths.py boxes.py crons.py cli.py brief.py dispatch.py heal.py links.py mem_cap.py
         spawn_budget.py branches.py migrate_channel.py hooks/rotation_alert.py workflows/*.json|js and their tests) is byte-identical
key      F fix round (file:line now + testable claim) · C node/text correction · K carry (reason) · G gone (file:line showing it)
         "-> fold #n" = same fix round as item n. node paths are under .agi/nodes/.
```

```
l4-config-max  node=hypothesis/l4-config-max-and-template-max-are-required-verdict-fields-of-every-merge-up-review-and-a-named-line-of-every-dispatch-order.md  final=demote
  1 C  node:11 cl.(5) "path_max is the THIRD check in the same verdict fields and dispatch-order line ... landed in slices 1-2" (+ title :13
       "config_max + template_max + path_max are REQUIRED fields") vs bytes: extensions/agi/workflows/merge-up-review.json has 0 path_max (both
       required lists = config_max/template_max); doc/unified-director-brief.md:61 order line = config-max/template-max/code only
       (alt F: land path_max {answer,where} in both stage schemas + prompts + brief line, the owner's 22:1xZ order)
  2 C  same cl.(5) "+ the migration of the measured baseline -- landed in slices 1-2" vs bytes: not migrated -- merge-up-review.json:15,:166
       (and 8 more workflows/*.json) still name a /home/<user>/work/agi root that does not exist on this box; no test runs the audit as a gate
  3 F  extensions/agi/bin/paths.py:23-36 findings() returns [] when a box cell is unset; only main() :44-48 refuses (cl.(6a) says classify()
       fails closed)  -> claim: paths.findings(root) with any box cell unset refuses by name (raises) instead of returning a clean []
  4 F  extensions/agi/bin/boxes.py:21-23 _BOX_CELLS/_PLACEHOLDERS re-declare .agi/context/schemas/[box].md (placeholder->cell map exists only
       as comments [box].md:6-9); config_max=yes in BOTH stages  -> claim: box_cell_names and resolve_placeholders read cell names and
       placeholder keys from [box].md fields; with both literals deleted test_paths_audit.py stays green
  5 K  paths.py:28 endswith("config.json") over-broad but latent: .agi/config.json is the only tracked *config.json today (git ls-files)
  6 K  test_paths_audit.py:6-7 docstring "nothing here reads the live tree" vs :132/:142 live reads -- docstring only (rider for #4)
  7 K  a00-df88db0f 80-vs-40 overrun with no rebrief: disclosed later in a00-93e8501b THOUGHT; historical
  8 F  test_paths_audit.py:29-35 _graph() writes no [box].md, so 6 tests pass only via the boxes.py:40 fallback  -> fold #4
  9 K  boxes.resolve_placeholders (boxes.py:54) has no production caller (only test_paths_audit.py:65): a seam awaiting the #2 migration
 10 K  paths.py:9 HOME_RE matches bare `expanduser`: by design -- the owner's path_max scope (node:26) names expanduser as home-relative
 11 K  cl.(4) mur wall/load UNVERIFIED: no measurement exists; unverified, not false
 12 F  NEW (found checking #2): paths.py:42 default --root = <repo>/.agi and :13-14 runs `git ls-files` with cwd there, so a no-dir audit lists
       only the graph (4804 tracked files, 0 under extensions/) and never sees the bin/*.py baseline it was built to track
       -> claim: `paths.py audit` with no dir lists every tracked repo file (ls-files from the repo top), so a /home/<user> literal in
       extensions/agi/bin/*.py is reported
```

```
l4-quick-migrate  node=hypothesis/l4-quick-migrate-one-verb-moves-a-post-to-another-box-as-a-fresh-rotation-from-the-card-or-a-transcript-fork-over-the-git-messaging-layer.md  final=accept_with_residue
  1 K  cl.(1) source-side card gate / carryover commit / push unbuilt: cmd_migrate docstring rotate.py:20616-20621 names them as later slices;
       the hypothesis carries no verdict (open scope, not an overclaim)
  2 C  node:11 cl.(2) "the source reads it on its next tick" vs bytes: nothing reads a `stage: seated` record (writers only:
       migrate_channel.py:45 seat_record, rotate.py:20923-20927); the slice-3 order (node:26) to name it deferred in a Boundary section was
       never done -- the node has no Boundary section
  3 K  cl.(4) carryover-commit test absent: follows #1 (feature unbuilt)
  4 K  cl.(5) real dry run: needs a second box; recorded 'not run', never faked
  5 F  extensions/agi/bin/rotate.py:20892 _migrate_seat (git worktree add + spawn) runs BEFORE the grant is resolved (:20912); the no-grant
       `continue` (:20919-20922) comes after a spawn and a session-cell write (:20909); test_migrate_channel.py:175-205 pins that spawn
       -> claim: with no actor_rows grant covering box/worktree, cmd_migrate_receive spawns nothing, writes no row cell and leaves the
       request record byte-identical (grant resolved before _migrate_seat)
  6 K  DEF2 refuted by verify as wording (the cell list is not exhaustive; both writes go through the one writer)
  7 K  DEF3 ceiling numbers are the claim's global 120: disclosed in the hypothesis SLICE-5 note
  8 K  DEF4 a00-ca0a163b kept lean_proved:85: the fail-open is recorded on the hypothesis; the class is already inconclusive
  9 F  MISSED2 partial row write: session cells (window/pid/session_id) land at rotate.py:20909 before the grant check  -> fold #5
 10 F  MISSED3 an inadmissible grant makes _write_identity_cells raise write.EditError (write.submit, rotate.py:9441) outside the only try
       (`except OSError`, :20893), aborting the whole receive tick  -> fold #5 (skip that record by name; the tick lives)
 11 F  MISSED4 rotate.py:20747 remote path "$HOME/.claude/projects/..." handed to scp: OpenSSH here is 9.6, whose default SFTP-mode scp does
       not shell-expand $HOME, so the fork transcript copy (check=False) can fail silently (inferred from scp semantics; unmeasured -- no
       second box)  -> fold #5 (a relative or ~/ remote path; a test asserts the argv carries no literal $HOME)
 12 F  MISSED5 rotate.py:20661 and :20762 spell "refs/agi/posts/{post}" beside the one resolver branches.mirror_ref (branches.py:365);
       the claim itself says "never a second spelling"  -> fold #5
```

```
l4-the-cron-node  node=hypothesis/l4-the-cron-node-is-the-whole-schedule-any-job-is-one-entry-one-variable-silences-the-box-audit-names-the-undeclared-and-apply-is-the-box-init.md  final=accept_with_residue
  1 K  DEF1 refuted (wording, disclosed): bare apply never touches units (crons.py:752-753) but the grid_sync self-reapply bakes --unit-dir
       (crons.py:536, :551); recorded in a00-074cd13d probes / a00-5d3a3267 THOUGHT
  2 K  DEF2 refuted (wording, disclosed): audit globs user-scope unit files (crons.py:1085-1090); system-scope limit in a00-074cd13d THOUGHT
  3 K  DEF3 cmd_audit docstring crons.py:1063-1065 ("any `agi-*` systemd unit", "no test touches the real user manager") stale vs the
       real-manager default :1085-1086 and ordinary-name flag :1101 -- doc-only; rider for #8
  4 K  DEF4+MISSED3 unit-dir literal twice (crons.py:536, :1086): drift risk only; rider for #8 (one module constant)
  5 K  DEF5 dead guard crons.py:1087 `if unit_dir is not None:` -- cosmetic; rider for #8
  6 K  DEF6 a00-074cd13d evidence_runs also cites demoted a00-0e932af3: noisy, gate satisfied, its own probes carry the proof
  7 C  MISSED1 .agi/context/schemas/[cron].md:74-75 built-ins "(`grid_sync`, `branch_push`, `publish_engine`, `engine_push`, `mail_poll`)" vs
       crons.py:93-94 KNOWN_JOBS, which adds `nudge_sweep`
  8 F  MISSED2 extensions/agi/bin/crons.py:1081 audits why_box only `if name in KNOWN_JOBS`, while [cron].md:10 says a gated job MUST say why
       (audited) and :83 lets any entry carry box  -> claim: `crons.py audit` names a generic cmd job gated on box with no why_box exactly
       as it names a built-in
  9 K  MISSED4 Path.home() with HOME unset falls back to the passwd entry (raises only without one): not reproducible on a normal box
 10 K  MISSED5 the parent re-probe read the real unit dir: read-only evidence path; the committed tests stay hermetic
```

```
l5-a-message-that-did-not-land  node=hypothesis/l5-a-message-that-did-not-land-tells-its-sender-so-at-once.md  final=demote
  (its demote-severity code defect is GONE -- EF.12; the demote now rests only on node text #2/#3)
  1 G  DEF1 extensions/agi/bin/send.py:2804 `send_dm(comms_root(root), "wake-repair", ...)` (merged 831b6e0ad,
       hypothesis:send-undelivered-notice-lands-in-the-comms-root)
  2 C  DEF2 node:11 cl.(2) "prints one plain line `[undelivered-yet] <to> ...` instead of the coalesce jargon" vs bytes: both lines print --
       `nudge: coalesced (<reason>)` (send.py:2491) is KEPT by design and pinned by test_send_undelivered.py:88-100; the R1 node
       send-undelivered-notice-lands-in-the-comms-root.md:12/:27 already says "KEPT, not gone" -- this node still says "instead of"
  3 C  DEF3 node:11 cl.(4) "T minutes later (ladder cell, default 10)" + FILE SCOPE ".agi/nodes/.geometry/ladder.md (T cell)" vs bytes:
       T = .agi/config.json comms.undelivered_after_minutes via _comms_config (send.py:2782; default _COMMS_DEFAULTS send.py:323);
       ladder.md carries no comms cell
  4 K  DEF4+MISSED2 refuted on bytes: wake() returns False ("quiet-skip") for a quiet row (send.py:2689-2692) before _nudge_window, so
       wake_all_local's [delivered-late] branch (send.py:2830-2831) is unreachable for it; a stored record goes to _notify_undelivered
       (residual: its one dm says "pane busy" for a quiet seat -- wording)
  5 K  DEF5 ladder.md comms cell removed via write.py unset: a cell, not a node file; the mur-prescribed fix
  6 G  MISSED1 fixture split: test_send_undelivered.py:42-51 `croot` = comms_root(project); seats under project/.agi (:54-62); the notice
       is asserted on croot/dm at :148 and :186-187
  7 K  MISSED3 experiment/a00-27a7e0b8-67c514.md:46/:48 cite cli.py:2117/:2069 vs defs cli.py:2121/:2070: <=4-line drift, names right
```

```
l5-a-parent-waits  node=hypothesis/l5-a-parent-waits-for-its-kid-in-the-foreground-and-a-turn-end-with-a-live-kid-is-named-not-a-death.md  final=accept_with_residue
  1 F  DEF1 extensions/agi/bin/cli.py:2356 heartbeat prints only id=status; cmd_wait docstring :2339 and the claim promise elapsed
       -> claim: every `cli.py wait` heartbeat line carries each agent's elapsed seconds (a test on a flipping manifest asserts it)
  2 K  DEF2 refuted as wording: brief.py:1897-1898 carries the NEVER rule's operative content
  3 K  DEF3 aggregate ~103 vs declared 26: ceilings resolve per kid (cli.py:737-751, >2x only); each kid disclosed its 1.96x
  4 C  DEF4 experiment/a00-c2bcfc6a-03c123.md:49 "no regression of the honest death label", :53 "Tests added (all pass)", :91 "Built conjunct 3
       ... 223 passed" read as a clean build vs :25 verdict inconclusive_lean_disproved:60, whose cause (a pid-null kid counted live) is only
       in probes :16 and THOUGHT :87
  5 F  DEF5 cli.py:2357 `if states and all(...)`: zero matching kid rows (an iter with no kid rows, or an --agent not in the manifest) sleeps
       to the deadline and returns 2 with an empty "still running:" (:2360) -- and brief.py:1898 orders "when wait returns 2, call it again",
       so that parent loops forever  -> claim: wait over zero matching rows returns at once (0 for an iter with no kids, non-zero naming an
       --agent absent from the manifest), never 2
  6 K  DEF6 test_brief.py pinned brief test moved to `cli.py wait`: the claim replaces that instruction; disclosed in the THOUGHT
  7 K  MISSED1 dispatch.py:3440 reaper log line reworded ("agent X failed (pid N died (detected by reaper))"): human-facing wording only
  8 F  MISSED2 dispatch.py:3429-3430 and heal.py:486 overwrite death.evidence with "turn-end" after _death_class set it to the stream-error
       line (dispatch.py:155, class at :186), so a record can read class=infra-stream-error, evidence=turn-end and lose the error line
       -> claim: a turn-end-with-live-kid reap keeps _death_class's evidence and records the turn-end in its own key
  9 F  MISSED3 manifest-level falsifier untested: test_heal_watch.py:2417-2440 asserts the record's death.evidence but only the manifest's
       fail_reason (heal.py:495 copies death)  -> fold #8
 10 K  MISSED4 "SM.133's count is a manifest query from now on": rationale (the field now exists to query), not a promised verb
```

```
l5-a-verdict-node  node=hypothesis/l5-a-verdict-node-carries-the-class-its-evidence-experiment-recorded.md  final=accept_with_residue
  1 C  DEF1 experiment/a00-794503d4-628fb0.md:15 probes truncated mid-JSON (575 chars, ends `write.py doc:n \"set location scratch`): the
       second (refusal-atomic) probe is lost -- restore it from the body Evidence prose
  2 C  DEF2 a00-794503d4:15, experiment/a00-09d5b982-1fe871.md:15, experiment/a00-f0f7f404-aceba1.md:15 store probes as a quoted "= [...]"
       scalar (cli._parse_probes -> None) vs [experiment].md:18 `probes: {type: list}`
  3 C  DEF3 a00-794503d4:21 title "...agrees with the links.py report in every reachable state" + :23 inconclusive_lean_proved:70 vs its own
       :90 "-- FALSE" (the location-only-edit bypass, still live: #4)
  4 F  DEF4 extensions/agi/bin/write.py:1912-1922 resolves only refs present in edit.set_fm, so a location-only edit that moves an existing
       relative link_ref outside the repo is admitted while links.py:407-410 reports it; comment :1907-1911 "agree in every reachable state"
       is false  -> claim: write.py judges the EFFECTIVE frontmatter (on-disk refs + set_fm - unset_fm) and refuses every edit links.py
       schema would report as outside-ref, before any write
  5 F  DEF5+MISSED2a write.py:1912-1918 never reads edit.unset_fm: unsetting location while setting an inside relative ref resolves against
       the stale on-disk location and over-refuses  -> fold #4
  6 K  DEF6+MISSED2b conjunct-5 probes are string-labelled (a00-09d5b982:15): bites only a decisive tier-parent verdict on the hypothesis;
       none recorded
  7 K  MISSED1 round total 60 vs claim 16: ceilings resolve per kid; per-kid rebriefs (proceed-with-24) recorded
```

```
l5-an-across-k-kids  node=hypothesis/l5-an-across-k-kids-ceiling-is-divided-onto-each-kid-node-by-the-spawn-never-by-parent-arithmetic.md  final=accept_with_residue
  1 C  DEF1 experiment/a00-dab18263-f2f8c4.md has no probes: field; Probes A/B/C live only as THOUGHT prose (:109-127) vs [experiment].md:18
       and the parent brief's order to record them as probes:
  2 F  DEF2 the named red-first test "hand-set 10 survives" (node:11) was never committed; only the harvest-side
       test_kid_reports_to_parent.py:588 covers node-field-first  -> fold #5 (that test, driven through brief + kid write, reds today)
  3 K  DEF3 24 vs 12 sits on the strict >2x boundary (cli.py gate is `>`), disclosed
  4 F  DEF4 node:11 "brief.assemble (line_ceiling explicit) ... read the slice" vs bytes: brief.py:2169-2174 reads the TARGET's clause
       (source 'clause'), never the kid node  -> fold #5 (makes the sentence true)
  5 F  DEF5 extensions/agi/bin/brief.py:1400-1402 orders the kid to `set line_ceiling N` while the brief's own number comes from the clause
       (:2172) and harvest reads the kid node first (cli.py:743): it BIT -- a kid rewrote its parent's hand-set slice 2 back to 8
       (experiment/a00-10c6b7b5-3b78b9.md:185-188)  -> claim: the kid brief names the kid node's own line_ceiling when set (else the clause
       slice) and never orders the kid to write line_ceiling, so a parent's hand-set 10 survives the kid's whole round
  6 K  MISSED1 whether the parent's proved done passed the tier-parent probe gate: its agent record is not on this box; unverifiable from
       committed bytes
```

```
l5-moral-one  node=hypothesis/l5-moral-one-loads-in-full-into-every-master-and-director-head-each-rotation.md  final=accept_with_residue
  1 K  DEF1 refuted: 19 vs 10 is per-round arithmetic the engine never computes; each kid is <= its own line_ceiling 10 (cli.py:737-751)
  2 C  DEF2 node:11 cl.(2) "renders the FULL body of moral:faith (moral 1) byte-for-byte" vs bytes: brief.py:590-594 prepends
       _read_faith_moral = the MORAL region only (ESSENCE/QUESTION/IN PRACTICE/VIOLATED WHEN, the node's own Agent Notes b03c3c680);
       cl.(1) "only the prayers section" is the pre-change measurement and stays
  3 K  DEF3 no committed rotate-self dry-render test: that path renders brief.py head (_prepend_head -> _build_head), which the 7 l5-moral
       tests cover; no defect found
  4 K  DEF4 brief.py:598 preamble "Prayers, sourced from moral:faith at run time" now incomplete for the director head -- pre-existing wording
  5 F  MISSED1 extensions/agi/bin/brief.py:144 _LIAISON_HEAD_TIER = "director" -> :2135 _finish(segs, _LIAISON_HEAD_TIER) -> :591
       `if tier == "director"`: an assembled liaison brief carries the moral region; test_brief.py:1420 never asserts ESSENCE absent.
       Latent (no liaison row in posts.md)  -> claim: brief.assemble(tier="liaison") carries no `## ESSENCE` while head --tier director does
```

```
l5-rotate-accepts  node=hypothesis/l5-rotate-accepts-the-pending-successor-key-the-signer-already-prefers.md  final=VERIFY-EMPTY
  note: the verify is NOT empty -- verify_l5-rotate-...json holds a complete return under `unstructured` (the model echoed the schema
        beside its data; rejected on "'round' is a required property"): D1 real (captive half refuted), D2 real, D3 refuted, 4 missed,
        final accept_with_residue. Used here as the substitute verify; every item re-checked against the bytes below.
  1 F  DEF1 extensions/agi/bin/rotate.py:4459 cmd_merge_up --post target lookup and :18309 rotate-self --prepare registry gate read root's copy
       (_find_seat(root, ...)) while _caller_post and cmd_rotate use _seat_read_root (:17739, :20964); the captive-rotate half is refuted
       (crons.md:41 `--root {root}` + crons.py:941 require_common_root pin alarms to MAIN)  -> claim: merge-up --post and rotate-self
       --prepare run from a worktree whose seats copy lacks a row MAIN has resolve MAIN's row (no "no seat" refusal); from MAIN unchanged
  2 C  DEF2 experiment/a00-2e6aafdb-b5acf1.md:16-19 probes (conjunct 2/2/3/4) and THOUGHT :96 restate the pre-re-scope pending-key claim (node
       last committed a41b65791, before re-scope 3626f0eb3) vs the current conjuncts (2) read tree (3) key_history never authorizes
       (4) .key.pending stays out -- relabel, or mark the probes pre-re-scope
  3 K  DEF3 refuted: test_rotate.py:489 and :603 drive a real cmd_rotate_self over a git+bare-origin fixture with a deferred .key.pending
  4 K  DEF4 a00-3630fb0b production_lines 1 (net) vs 2 added: cosmetic, ceiling 8 unaffected
  5 K  DEF5 harvest commit message "0 demoted": git history; the node's verdict is authoritative
  6 F  MISSED1 cmd_rotate's target lookup (rotate.py:20964) has no committed shared-vs-worktree test (test_rotate_verb.py uses one root;
       test_rotate_caller_post.py never calls cmd_rotate)  -> fold #1
  7 F  MISSED2 _caller_post's env path (AGI_POST) from a worktree root with a stale row is untested (only root==MAIN,
       test_rotate_caller_post.py:126-135)  -> fold #1
  8 K  MISSED3 retired-file artifact: asserted 0600 retired-<fp> by the direct test test_rotate.py:409; the live tests assert pending consumed
  9 K  MISSED4 ~40 other _find_seat(root)/_load_seats(root) call sites (cmd_spawn, cmd_status, _prepare_checks, _fd_seat_worktree ...):
       the wider read-tree sweep, not re-checked per site; #1 takes the two the verify named on a post's own-worktree path
 10 K  conj(1) "refusal MEASURED on two generations": historical, not re-derivable from bytes
 11 K  conj(2) non-MAIN shared root via origin: an explicit deferral in the claim itself
  note: still no verdict node for this hypothesis (none under verdict/): the batch mur's call, not a defect
```

```
l5-the-meter  node=hypothesis/l5-the-meter-captures-the-final-card-and-forces-the-rotation-itself.md  final=accept_with_residue
  1 C  DEF1 node:11 "alarms runs as a detached user unit per master (systemd-run --user, --working-directory)" and "alarms --once dms a held
       seat idle >= M min at 0.85 x line" vs bytes: the declared service (.geometry/crons.md:39-41) runs `rotate.py alarms --holder ...
       --root {root}` (no systemd-run; no --detach/_run_alarms_unit left in rotate.py, grep 0); cmd_alarms (rotate.py:7206) calls
       _master_rotate and sends no dm (verify called it wording, but node:39 says "amended above" and these fragments remain)
  2 C  DEF2+MISSED3 experiment/a00-3a04e059-da77bd.md:16 production_lines 81 and :34 "Ladder cells added live" vs kid commit a63959d87
       (rotation_alert.py 78/3 only; the cells landed later, ceaa79618); :23 stays proved on a deliverable its diff lacks
  3 C  DEF3 experiment/a00-81fb6a5d-63f6f9.md:19 production_lines 77 sums crons.md 11 + ladder.md 4 absent from kid commit 8ca78e04c
       (rotate.py 62/6 only)
  4 C  DEF4+MISSED2 a00-3a04e059:15 and experiment/a00-931b52d8-2c24f6.md:15 store probes as a quoted scalar vs [experiment].md:18 list
  5 G  DEF5 test_rotate.py:2787 test_alarms_once_master_rotates_the_due_seat_then_stops (rewritten by 0eb6d7603) asserts the master-path spawn
  6 K  DEF6 live poller vs declared unit: operational, not inspectable read-only; node:39 records the unit re-created on the merged bytes
  7 F  DEF7 extensions/agi/hooks/rotation_alert.py:875 `float(ladder.get("captive_rotate_ratio", 0.85))` and :877 `ratio = 0.85`: a ladder
       with only captive_rotate_masters arms trigger (a) at a code literal (config_max=yes both stages; trigger (b) reads default None,
       rotate.py:7231)  -> claim: with no parseable captive_rotate_ratio cell trigger (a) never fires and names the missing cell
  8 C  DEF8+MISSED1 experiment/a00-d7588719-d59894.md:24 title "Detached alarms unit is wired: --detach launches the meter", :26 proved vs
       bytes: _run_alarms_unit/--detach deleted in 20e848493 (grep 0 in rotate.py) -- mark superseded
  9 C  DEF9 a00-81fb6a5d:24 title "Alarms dms an idle held seat below the line and runs as a detached user unit" vs built: no dm, no detached
       unit (its lean_disproved:55 is honest)
 10 C  DEF10 node:11 "trigger (b) the heal-watch poll" vs bytes: trigger (b) is rotate.py cmd_alarms (:7206); heal.py untouched
 11 F  DEF11 extensions/agi/bin/rotate.py:7263-7265 `while True: time.sleep(args.interval); return cmd_alarms(args, root)` recurses once per
       interval; the declared 24/7 service (crons.md:41, no --once; default 300 s, rotate.py:21319) hits RecursionError after ~1000
       intervals (~83 h), surviving only by Restart=on-failure  -> claim: the non---once alarms loop is iterative -- N >
       sys.getrecursionlimit() stubbed intervals run at constant stack depth
 12 K  template_max=yes (review): order text in code at rotation_alert.py:293 IMPERATIVE, :295 AUTO_CAPTURED, :1478 -- policy residue with
       no behavioural defect; bank for one template_max pass into config:rotations templates (same as engine-delta #2)
 13 K  conj(4) MEASURED trigger (gen 6 idle at f=0.444): historical; the run dir is gone
 14 K  MISSED4 test_rotate_alarms_idle.py:143-158 reads the committed crons.md node: read-only, part of the claim; no unit/crontab touched
```

```
l5-tracked-files  node=hypothesis/l5-tracked-files-name-origin-by-its-current-url.md  final=accept_with_residue
  1 C  (low) conj C1-C4 node:11 "(1) The old literal origin URL appears in 6 tracked files (README.md, TODO.md, package.json, 2 nodes, 1 rotation
       record)" + CEILING 6 vs bytes at cb21bf01d: the live addresses were QUICKSTART.md, TODO.md, context/refs/legacy-prestate.md,
       package.json (4 files / 7 lines; README.md:49 is agi-tree) -- the correction lives only in the experiment (:58, :127)
  2 C  DEF1+MISSED1 experiment/a00-39a8276d-9dfd67.md:18 probe and :127 THOUGHT "12 residual lines" vs the post-change 7 non-self the node's
       own title :25 and body state; 12 is the pre-change count
  3 K  DEF2 refuted: the origin URL is per-clone git config, valid where the kid ran; the committed rewrite reproduces
  4 K  DEF3+MISSED2 the later residual datasets/trajectories/ABC.02/a00-b2deb33c/trajectory.jsonl:28 (added by 4a9d9dca0) is a pasted
       `git remote -v` line, not an address
  5 C  DEF4 QUICKSTART.md:62 "`CodexOperator/AGI` is **private**" vs the graph: public (doc/l4-owner-decisions.md:529 "REPO IS PUBLIC";
       goal/g19.md:112 recreated "public") -- confirm the live visibility before editing
  6 K  DEF5 test_bin_help_smoke.py spawns `--help` subprocesses: pre-existing; no tmux/systemd/crontab
```

```
l5-why-parents-die  node=experiment/a00-dd617306-ee4cd1.md (hypothesis/l5-why-parents-die-before-the-review-step-measured-before-any-fix.md)  final=accept_with_residue
  1 C  DEF1 a00-dd617306:99 "Measured 16/16 sanctuary-seat parent deaths (18/18 tree-wide)" vs the corrected verdict line :93 "16 of 18 tree-wide"
  2 K  DEF2 refuted: title :25 "16 of 16" is the sanctuary-seat count that :67 separates from rows 17-18
  3 C  DEF3 :73 "`dispatch.py` never calls `systemd-run` ... There is no parent unit to name" vs dispatch.py:2668 mem_cap.wrap_argv ->
       mem_cap.py:67-75 wraps the spawn in `systemd-run --user --scope` whenever systemd_run_usable() (rows 7-16 carry memory_max 4G, :75)
  4 C  MISSED1 :38 "18 parent-dead/kid-survived rounds tree-wide" vs its own probe :16 "17 rows" and review :105 "recomputed 17" -- unreconciled
  5 C  MISSED2 :71 "`death.evidence` is `null` on all 18" vs row 18 (:65) "no `death` key"
  6 C  MISSED3 :99 "no parent unit exists" vs :73, which marks that channel UNKNOWN
```

```
l5-write-py-splits  node=hypothesis/l5-write-py-splits-a-script-only-at-an-ampersand-pair-that-begins-a-verb.md  final=accept_with_residue
  1 F  DEF1 extensions/agi/bin/write.py:527 _VERB_SEP (split at :620) splits before any known verb, so `note quote && set status x` executes
       the set -- the claim's own cl.(2a) falsifier, pinned as expected by test_write.py:2039; same accident class as the a00-794503d4
       probes truncation  -> claim: a free-text argument carries a literal `&& <verb> ...` through one escape the parser honours and never
       executes it (test_write.py:2039 inverted)
  2 K  DEF2 refuted as wording: the `|$` / `|&&` alternatives are documented deviations (a00-b0575ad8, a00-10c6b7b5)
  3 F  DEF3 write.py:527 doubled separator: `note a&&&&note b` -> [note 'a&&', note b] vs the pre-fix [note a, note b]; no `&&&&` test
       (grep 0 in test_write.py)  -> fold #1 (consecutive separators parse as the pre-fix loop did)
  4 C  DEF4 node:12 title "the measured way experiment:a00-794503d4's link_ref filled with leaked prose and crashed links.py links" vs bytes:
       the leaked link_ref at 2c1c54732 (1281 bytes) holds zero `&&`; the experiments carry the correction, the hypothesis never did
  5 K  DEF5 write.py:518-520 comment ("ONLY when ... ending at whitespace or end-of-string") vs the :524-526 alternatives: comment; rider #1
  6 K  DEF6 line_ceiling 8 vs slice 2: disclosed at a00-10c6b7b5-3b78b9.md:185-188; its cause is l5-an-across-k-kids #5
  7 C  MISSED1 node:20 body is still the scaffold placeholder "What is the testable claim? What would prove it? What would disprove it?"
  8 F  MISSED2 test_write.py:2039 pins the falsifier as expected behaviour  -> fold #1 (the escape rewrites it)
  9 C  MISSED3 experiment/a00-b0575ad8-e27a4c.md:155 "closes the last clause-(2) hole" vs cl.(2a) still false (test_write.py:2039)
```

```
lm-research-review-mint  node=hypothesis/lm-research-review-why-brainstorm-mint-by-default.md (thought-side node, director-thought gen12)  final=accept_with_residue
  1 F  DEF1 extensions/agi/workflows/research-review.json:192 sets why_node none on the propose-only path and :252 reads why_node `none` as
       "verdict proved" (refines push_further); brainstorm renders no {proposed_idea_title}/{proposed_idea_body}
       -> claim: a bare (propose-only) run on a disproved target hands brainstorm the proposed WHY idea (branch keyed on {branch}, not why_node)
  2 C  DEF2 experiment/a00-2ec3b4a6-b531ae.md:23 inconclusive_lean_proved:70 vs its own probe :15 and THOUGHT :112 (the mint:false clause
       FAILS the named falsifier) -> lean_disproved (superseded by a00-0546e377)
  3 C  DEF3 node:14 tests "asserting no write.py create appears in the rendered prompt" vs the landed test_research_review_mint_gate.py:67-68
       (asserts the propose-only markers; the bare prompt keeps `write.py create` by design)
  4 C  DEF4 node:13 proposal fields "that are ALWAYS filled" vs bytes: empty on a proved verdict (:192), proposed_hypotheses empty on
       push_further (:252) -- always present, not always filled
  5 F  DEF5+MISSED2 extensions/agi/workflows/agi-research-review.js:22 `(args && args.mint) ? "true" : ""` mints on any truthy value (the
       string "false", 1) while the python render and the stated rule (:192/:252) read them as off  -> fold #1
  6 K  conj: a LIVE bare / mint:true run was never dispatched -- outside the round's declared dry-run scope, stated in both experiments
  7 F  MISSED1 research-review.json:320 refute reads only {hypotheses}; the propose-only brainstorm returns hypotheses [] (:252), so a bare --
       i.e. DEFAULT -- run's proposals never reach refute or the ready_batch  -> fold #1
```

```
engine-delta  node=(none; the goal it reviewed, g14.14, is now goal/g7.33.md)  final=accept_with_residue
  1 F  DEF1 extensions/agi/hooks/rotation_alert.py:1414-1418 writes capture-<seat>.json once (`if not fp.exists()`) and nothing unlinks it
       (grep: :793 read, :1414 write only); _maybe_force_capture (:788-799) gates on time since that first stamp, so every later session of
       the seat skips the card_capture_minutes grace  -> claim: a new session's first over-line prompt starts its own grace (stamp keyed
       per session, or cleared when the rotation lands); no force-capture before card_capture_minutes of THAT session
  2 K  DEF2 rotation_alert.py:293/:295 IMPERATIVE/AUTO_CAPTURED order text in code (template_max=yes both stages): policy residue, no
       behavioural defect; bank with l5-the-meter #12
  3 F  DEF3 cli.py:2357 empty kid set waits to the deadline and returns 2 = l5-a-parent-waits #5 (same fix)
  4 G  DEF4a branch-blind grid guard lifted for a configured trunk: extensions/agi/bin/grid.py:935
       `if not session and not allow_branch and ref_ns_for(root) == DEFAULT_REF_NS` (EF.09)
  5 K  DEF4b send.py --body-file/stdin still absent (grep 0): scope carried by goal:g7.33, not a regression
  6 K  DEF4c dispatch.py `where <kid-id>` still absent: scope under goal:g7.33
  7 K  DEF4d write.py `replace body --at '<heading>'` still absent: scope under goal:g7.33 (the guard half landed, now fence-aware + clamped:
       write.py:2171 _guard_headings, :2255 past-EOF refusal)
  8 F  MISSED1 the captive triggers share no in-flight latch: _captive_rotate (rotation_alert.py:865-895) calls _force_capture and
       _master_rotate (rotate.py:7268) spawns on every tick; no _rotation_in_flight seam exists (grep 0). Already minted as
       hypothesis:l5-the-two-captive-rotation-triggers-share-one-in-flight-latch-per-seat (SM.142): unbuilt, no experiment
       -> claim per SM.142 (both triggers hold a seat whose rotation is in flight younger than the role timeout)
```

```
SUMMARY
counts   130 items: F 34 · C 34 · K 58 · G 4   (F rows include "-> fold" sub-items; distinct fix rounds below)
G        send.py:2804 · test_send_undelivered.py:42-51 · test_rotate.py:2787 · grid.py:935

F ROUNDS (priority order)
FR-A hypothesis:captive-rotation-loop-is-flat-session-scoped-and-latched      LIVE: ladder.md:15-17 captive cells set; alarms declared 24/7
     rotate.py:7263-7265 recursion · rotation_alert.py:1414-1418/:793-799 seat-keyed stamp · rotation_alert.py:865-895 + rotate.py:7268
     no in-flight latch (= SM.142, already minted: run it here or as-is) · rotation_alert.py:875/:877 0.85 literal
     claim: the declared alarms service loops at constant stack depth, a seat's force-capture grace restarts each session, neither captive
     trigger spawns for a seat whose rotation is already in flight, and trigger (a) stays off without a parseable captive_rotate_ratio cell.
FR-C hypothesis:round-pipeline-keeps-the-kid-ceiling-bounds-wait-and-hands-proposals-to-refute   (the ceiling overwrite has already bitten)
     brief.py:1400-1402 + :2169-2174 kid ceiling · cli.py:2357/:2360 empty wait (+ :2356 elapsed) · dispatch.py:3429-3430 + heal.py:486/:495
     evidence · brief.py:144/:2135/:591 liaison moral (latent) · research-review.json:192/:252/:320 + agi-research-review.js:22
     claim: a kid brief names its own node's line_ceiling and never orders it rewritten (a parent's hand-set 10 survives the round); wait
     returns at once on zero matching kids and prints elapsed; a turn-end reap keeps the stream-error evidence in record and manifest; a
     liaison brief carries no moral region; and a bare research-review run's proposals reach brainstorm and refute (mint = literal true).
FR-B hypothesis:rotate-verbs-read-main-rows-and-migrate-seats-only-when-granted
     rotate.py:4459 + :18309 read root's copy (+ tests for :20964 and _caller_post env) · rotate.py:20892 seat before grant :20912 ·
     EditError rotate.py:9441 past `except OSError` :20893 · rotate.py:20661/:20762 second ref spelling · rotate.py:20747 $HOME under scp
     claim: merge-up --post and rotate-self --prepare resolve rows via _seat_read_root like rotate, and cmd_migrate_receive resolves the
     grant before _migrate_seat -- an ungranted or inadmissible record spawns nothing, writes no cell and is skipped by name while the tick
     lives -- with the ref from branches.mirror_ref and a fork transcript path scp's SFTP mode resolves.
FR-D hypothesis:write-gates-and-audits-cover-what-they-declare
     write.py:1912-1922 outside-ref gate · write.py:527/:620 `&&` escape + `&&&&` (test_write.py:2039) · paths.py:13-14/:42 graph-only scope ·
     paths.py:23-36 fail-open findings() · boxes.py:21-23 + test_paths_audit.py:29-35 second declaration · crons.py:1081 why_box
     claim: write.py refuses exactly what links.py schema reports as outside-ref (effective frontmatter) and lets prose carry an escaped
     `&& <verb>`; paths.py audit covers every tracked repo file, fails closed inside findings() and reads names/placeholders from [box].md
     alone; crons.py audit names every box-gated job lacking why_box.
     (riders when touched: crons.py:1063-1065 docstring, :536/:1086 literal, :1087 guard; write.py:518-520 comment; test_paths_audit.py:6-7)

C LIST (node -> correction; one write.py pass per node, grid commit after)
 hyp l4-config-max…:11/:13      cl.(5) path_max "THIRD check … landed" + baseline "migrated" -> not delivered (0 path_max; unmigrated)
 hyp l4-quick-migrate…:11       cl.(2) "the source reads it on its next tick" -> no reader; add the ordered Boundary line (deferred)
 schema [cron].md:74-75         built-ins list += nudge_sweep
 hyp l5-a-message…:11           "instead of the coalesce jargon" -> both lines print; "ladder cell"/"ladder.md (T cell)" -> config.json comms
 exp a00-c2bcfc6a :49/:53/:91   body/Agent Notes name the pid-null hole behind lean_disproved:60
 exp a00-794503d4 :15/:21/:23   restore the truncated probe; narrow "every reachable state"; lean_disproved
 exp a00-794503d4/a00-09d5b982/a00-f0f7f404/a00-3a04e059/a00-931b52d8 :15   probes scalar -> YAML list
 exp a00-dab18263               add probes: from THOUGHT Probes A/B/C (:109-127)
 hyp l5-moral-one…:11           cl.(2) "FULL body of moral:faith" -> the MORAL region
 exp a00-2e6aafdb :16-19/:96    probes + THOUGHT are pre-re-scope; relabel
 hyp l5-the-meter…:11           drop "(systemd-run --user, --working-directory)", "alarms --once dms", "heal-watch poll"
 exp a00-3a04e059 :16/:23/:34   production_lines 81 -> 78; "Ladder cells added live" false; proved rests on a missing deliverable
 exp a00-81fb6a5d :19/:24       production_lines 77 -> 62; title (no dm, no detached unit)
 exp a00-d7588719 :24/:26       superseded (--detach/_run_alarms_unit deleted in 20e848493)
 exp a00-39a8276d :18/:127      "12 residual lines" -> 7
 hyp l5-tracked-files…:11 (low) premise file set (README.md, 2 nodes, 6 files) -> the 4 files / 7 lines actually rewritten
 QUICKSTART.md:62               "is **private**" -> public (confirm live visibility first)
 exp a00-dd617306 :38/:71/:73/:99   18/18 -> 16 of 18; 17 vs 18; row 18 has no death key; dispatch DOES wrap in systemd-run; channel UNKNOWN
 hyp l5-write-py-splits…:12/:20 drop the link_ref causal attribution; author the body (scaffold placeholder)
 exp a00-b0575ad8 :155          "closes the last clause-(2) hole" -> (2a) still open
 hyp lm-research-review…:13/:14 "ALWAYS filled" -> always present; tests field -> the propose-only marker assertions  (thought-side node)
 exp a00-2ec3b4a6 :23           lean_proved:70 -> lean_disproved (its mint:false falsifier failed)  (thought-side node)
```

## Agent Notes
assigned: director-engine (0921 residue batch, engine slice, goal:g15.27); table sorted by a read-only helper for director-engine and spot-checked against the bytes before minting.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
EF.23 (parent a00-95359f56) executed this node's C list. Twenty non-excluded C items applied IN PLACE across 20 nodes: seven hypothesis nodes plus two files (.agi/context/schemas/[cron].md and QUICKSTART.md) by kid a00-11797ce4, whose process died on a provider error before it could call done (its node experiment:a00-11797ce4-ddb8cb carries no verdict; the parent read its edits as bytes); and eleven experiment nodes by kid a00-baa8e365 (experiment:a00-baa8e365-a4a8cb, inconclusive_lean_proved:75). Two thought-side C items skipped by the dispatch order (hypothesis:lm-research-review-why-brainstorm-mint-by-default, experiment:a00-2ec3b4a6-b531ae) and named as skipped. No verdict, lean or confidence field was changed anywhere: a parent probe compared the verdict/confidence/lean/demoted_from/evidence_gate lines of all 20 corrected nodes against their pre-round values and found zero deltas. Every corrected node's THOUGHT names hypothesis:mur-0921-engine-residues-dispositioned-and-corrected. Probe-shape corrections landed as real YAML lists (a00-794503d4 2 entries with the truncated refusal-atomic probe restored, a00-09d5b982 4, a00-f0f7f404 4, a00-3a04e059 1, a00-931b52d8 1, a00-dab18263 3). Two verdict questions were surfaced and left for their authors, not resolved: experiment:a00-794503d4 should read inconclusive_lean_disproved (its own THOUGHT says the every-reachable-state claim is FALSE), and experiment:a00-dd617306's tree-wide count reconciles to 16 of 18 with 17 the committed-probe figure. The two engine demotes this table targeted now agree with their bytes: extensions/agi/workflows/merge-up-review.json carries zero path_max, and send.py:2491 still prints the coalesce line the l5-a-message claim now says is KEPT. Parent-run negative probes are recorded on the parent round a00-95359f56 (inconclusive_lean_proved:80). One defect seen and NOT fixed by the parent: the round-done commit's scope rule left all 20 corrected node files uncommitted in this worktree (foreign paths by basename), so the loop must carry them.
<!-- THOUGHT:END -->
