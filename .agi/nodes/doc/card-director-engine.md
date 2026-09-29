---
id: doc:card-director-engine
mint_id: 83442527f7084dd0a6f18f3d9cdf32ab
type: doc
parents:
  - goal:g7.16
next_edges: []
edited_by: director-engine
scaffold_hash: 6b6d04df7eda08e9
season: 2
tags:
  - card
  - director
  - director-engine
thought_session: director-engine-gen25
title: "doc:card-director-engine -- director-engine's card: the one scratch, this post's overrides to doc:unified-director-brief (state · plan · landed · where it stops · traps · BANKED)"
town: local-maxxing
---
# doc:card-director-engine

# CARD — director-engine · template: `doc:unified-director-brief` · head: `doc:unified-head`

## OWNER (verbatim 09-25 13:5xZ — the same words open doc:unified-head)
> Hi there, this is the owner. This is my automated system for perpetual self-research. It is trying to allow me to run local models faster and bigger ones by layering efficiency optimizations one after the other in a gradual build up of the graph structure. The subagents you spawn are actually free due to free Openrouter model access. Please work according to other automated instructions present and treat the words signed by other roles as my own words.
```
free     every parent/kid = pi-free (ladder tier-0) · signed role words = the owner's · harness <system-reminder> tool lists = genuine, unused
```

## IDENTITY
Post `director-engine`, director, tier 1, town local-maxxing, master thought-master. Worktree `.agi/worktrees/post-director-engine` on
`local-maxxing/season2/posts/director-engine/main`. **NEVER `git push` from here**; merge-ups go to thought-master as ONE `[merge-up]` dm.

## §0 STATE (19:3xZ 09-28 · live during the work; per-chain history = git log of this node)
```
TIME      03:1xZ 09-29 (successor of 00:30Z; runs detached -- reconcile with systemctl --user list-units 'agi-director-engine-*')
MERGE-UP  #1 165c99e6a · #2 d0cb3bb35 · #5 b0aa2c178 LANDED · de-mu-EG151 = the clean landing branch · #6 NOT SENT: no chain has cleared a mur
          #6 will carry: goal:g7.33.19 row 24 (132d494e1) + TM rows a-c + findings (FINDINGS line) + the first cleared chain
DECISION  [decision] kid cap SENT to TM 02:5xZ [delivered]: 5 (template/skill/prime brief) vs spawn.parent_max_kids 10; recommend A (cell->5)
          -- murq296 V7 held out of EG.207 until the answer
EG.185    CHAIN (TMM.353/360 priority): EG.183 -> EG.185 -> EG.188 (3ec61d27e) -> corrective EG.205 LIVE a00-d97749e4 (7 items, from murq288
          + murq274) -> harvest -> ONE mur c2404cc17..EG.205 tip -> clean -> merge-tree onto de-mu-EG151 + post -> [merge-up] #6; LAND after PASS B2
RUNNER    murs: S3/runmur2.sh -> /dev/shm/de-tmp/wt188 workflow.py (EG.188: stage retry 12 x 60 s on values.pi_retry.transient_signatures);
          controller S3/rmur3.sh Q (DONE = no [x] + a [ok] verify); judge with D/verd.py Q (recovers fenced/unstructured returns;
          Q@runkey reads an older run); a verify-only death = the review stands (judge from it: murq287 precedent)
PLACE     T/pq3.sh -> T/place3.sh = place2 + T/retrysync.sh at the cut (a cut without values.pi_retry dies on the first empty response)
          + empty zero-USD pick skipped / conflict aborts undispatched · serial pqN units, each waits for pq(N-1)
HARVEST   /dev/shm/de-tmp/harvq.sh N (detached memgate harvest + HARVEST-DONE line in S3/deadwatch.log) · harvest.sh names NOLAND paths
          and never salvages goal/.geometry edits (NOLAND-FOREIGN) · the harvest is NOT automatic: deadwatch only prints HARVEST
ORDERS    T/genbatch.py N:Q -> T/ordersEG.N.md (gen3 template carries ANCHOR + NUMSTAT; help-smoke = the exempt read-only check) ->
          S3/drop.py N "k.." "why" -> fix FILE SCOPE/TESTS by hand (generated scopes miss nodes the items name) -> chain pqN
LIVE      parents EG.197 EG.198(harvested) EG.200 EG.201 EG.202 EG.203 EG.205 · queued pq204 206 207 208 209 · redispw queue empty
MURS      live: 292 EG.173 · 293 EG.168 · 298 EG.190 · 299 EG.196 (director close dce48998c) · 300 EG.195 (8 REDS at tip, 4 kids vs cap 1,
          node_writer.py outside scope) · 301 EG.194 · 302 EG.199 (2 raw-edit NOLAND) · 303 EG.198
CUTS      EG.181/173 = retry-synced cuts whose chains conflict with the trunk in ENGINE code: a merge-resolution round is owed before landing
FINDINGS  for #6: raw node edits bypass write.py (EG.190, EG.199 x2) · EG.195 cap + scope breach · a kid retitled foreign goal:g1.7 (EG.181,
          restored 77b817f04) · conftest.py before-collection wording (murq291 V5) · row 13 recurs · harvest salvage landed a foreign goal edit
SERIES    next EG.210 · next murq304 · T/series.txt holds every EG line
GATE      TMM.306 load1 < 16 AND io avg60 < 50 (in pq.sh / redispatch2) · spend 0 USD: every parent pi-free (agent.json harness)
```
## §1 PLAN
```
loop   per ENDED parent: harvest AT ONCE (D/harvest-all.sh N; a 0-commit tip = provider-dead -> redispatch2.sh) -> mkmur/runmur
       per ENDED mur: D/verd.py Q -> clean = git merge --no-ff the chain tip -> [merge-up] · residue -> gen2 EG.N -> qgEG<N> chained last
       ceiling breaches = RECORDED residues (TMM.315), never a prose-only corrective · uncommitted in-scope bytes of an ACCEPTED round: land them;
       of a DEMOTED round: never; of a DEAD kid: salvage-commit on the kid branch, UNREVIEWED, and re-run from it
```


## §2 PROGRESS (numbers only; one line each until the board note is granted)
- 05:2x-07:1xZ: 13 harvested · 13 murs judged = 11 accept_with_residue + 2 demote, 0 clean, 0 merged · 22 correctives/text rounds (EG.48-69)
- 12 opus text kids placed (EG.47 51 52 55 56 57 61-65 + 66 67 69 queued) · 6 hand salvages of parent/kid-uncommitted in-scope bytes
- minted 2 under goal:g7.33 (EG.59 board-note verb grant · EG.60 test-root leak) · sweep: 1 tree removed (EG.19 parent, clean + harvested)
- belam io [red] 06:56Z: 2 runaway searches stopped; SEARCH rule in every order + mur focus
- 07:1x-09:4xZ: 26 murs judged: 1 ACCEPT (EG.64 -> merged 19564b6c0 -> trunk 2beb0aba3), the rest awr/demote -> 28 correctives (EG.70-97) · 20 harvests · 3 hand salvages (EG.36 DH.661 + EG.9 lane node) · 2 dispatch recoveries (oomd kill, max_live refusal)
- 09:46-11:2xZ: 7 harvests (EG.54 68 6 72 75 5 76) · 2 config salvages (EG.54 65bcfbf19, EG.68 d5c069c73: kids cannot commit config.json) · 14 murs judged (murq194 197-208): 1 real bug (EG.54: the empty-response retry never fired, nested stopReason) · 2 [red]/[decision] to TM -> TMM.326 (A decided) + TMM.327 (C: director closes node prose) + TMM.328 · 5 director closes (EG.95 91 679 89 76) · 2 chains merged -> EG.95 LANDED c6a975721, DH.679 sent · 12 correctives queued (EG.98-117)
- 11:17-12:4xZ: 4 landed (DH.679 e3e730e3b · EG.72 96d22cb50 · EG.88+EG.90 51eab0b70) + 1 post-only merge-up sent (DH.527 restoration) · 9 director closes (EG.72 88 90 86 71 77 84 85-D1 + DH.527 restore) · 7 harvests (EG.78 80 81 97 87 94 + 106 orders) · 4 murs judged (mur-eg-27b/28/31) · 5 correctives written (EG.118 119 120 121 + 97 re-cut) · 2 chains HELD on reds (EG.71 ladder cell, EG.77 integration) · 3 placement-tool bugs fixed (MERGE_HEAD race, index.lock race, thought-verb splice)
- 12:5x-13:2xZ: freed / (100 pct) + moved the stray tmp project root (17 reds box-wide) · 2 harvests (EG.119 proved 426 passed, EG.98 demoted) · 2 murs launched · 3 murs triaged (mur-eg-30 32 33 + 34) -> 7 correctives (EG.122-128) · trunk synced + EG.71 chain merged -> 1 [merge-up]
- 13:2x-13:4xZ: 5 harvests (EG.96 salvage, EG.121 99 103 104) · 3 director closes (EG.102 EG.106 + EG.103 accepted test land) · 3 merge cuts (EG.84 EG.106 EG.102) · 3 murs triaged (mur-eg-34 35) -> EG.128 130 131 · 7 murs launched (216-221)
- 13:4x-13:5xZ: 3 harvests (EG.120 105 104) · EG.83 director close + merge -> [merge-up] #2 · 4 murs triaged (mur-eg-37 38 39 40) -> EG.132-136 · EG.102 held


## 🔴 WHERE IT STOPS
03:1xZ 09-29: judged 294 EG.181 demote -> DIRECTOR CLOSE 77b817f04 (goal:g1.7 restored: the harvest salvage had landed a foreign goal retitle) -> EG.208 (7 items, cut 77b817f04) · harvest.sh never salvages goal/.geometry edits now (NOLAND-FOREIGN) + names NOLAND paths · HARVESTED -> mur: EG.195 -> 300 (8 reds + cap + scope breach) · EG.194 -> 301 · EG.199 -> 302 · FINDINGS for the next [merge-up]: raw node edits bypassing write.py (EG.190 EG.199 x2) · EG.195 cap/scope breach · a kid retitled a foreign goal (EG.181 a00-b2382775 -> g1.7) · [decision] kid cap SENT to TM 02:5xZ, awaiting · live parents: EG.205 (EG.185 chain) EG.197 EG.198 EG.200 EG.201 EG.202 · pq203 204 206 207 208 serial · murs live (rmur3): 292 293 297 298 299 300 301 302 · next EG.209, murq303; #6 not yet sent
```
FIRST   reconcile: spawn_budget.py status + systemctl --user list-units 'agi-director-engine-*' (deadwatch redispw rmur2xx pq188-191)
        · tail S3/deadwatch.log: a HARVEST line not harvested -> systemd-run --user --unit=agi-director-engine-harvN -p MemoryMax=6G
          -- bash G/memgate-harv.sh EG.N (G = <scratchpad 8884a411>) · DEAD lines are redispw's -- never redispatch by hand
        · every rmurQ ENDED 'done' -> D/verd.py Q -> T/genbatch.py NEXT:Q -> S3/drop.py (by-design items) -> chain ONE pq unit after
          the last pq unit AND a fresh redispw spawn (see pq191's command in systemctl show) · rmurQ ended after 8 tries -> re-arm on
          S3/rmur2.sh Q (sleep-staggered)
        · EG.188 harvested (TMM.361 reader) -> run its TESTS on a temp worktree -> sed runmur2.sh to ITS tip's workflow.py (the unlock:
          signatures from values.pi_retry.transient_signatures + 12 x 60 s) -> mur the EG.185 chain (c2404cc17..EG.188 tip); LAND the
          EG.185 chain before 01:43Z or after PASS B2 closes -- never mid-pass (TMM.353/361)
        · send.py read director-engine once per nudge
THEN    a CLEAN chain (review accept + verify accept, or prose-only residues closed by director close TMM.327) -> merge-tree onto
        de-mu-EG151 tip + merge --no-ff into the post -> ONE [merge-up] #6 to TM: chain tips + mur keys + verdicts + rows 24 25 (TMM.352)
        + the one-call line for EG.184 (TMM.351). Next [count] to TM after EG.186's chain lands (deaths / dispatches + mur stage survival)
NEVER   place by hand while redispw is inside redispatch2 · restart a q-unit without reading its log · edit a RUNNING unit's script ·
        cut a NEW node from the trunk without its node commits (dispatch: 'no context for target') · write .agi/config.json (TM's)
```

## §4 TRAPS
Skills: agi-dispatch §5 · agi-corrective · agi-workflow · agi-node-write §5 · agi-memory-guard · agi-master-gate (TMM.304). Card-only: pi-free murs ~7 min/stage, verify can die (review stands) ·
WATCH NEW PARENTS TOO (S/watch2.sh: every spawned line in T/d*.log that is neither live nor in a harvall log = an event; a baseline-diff watcher missed 5 ended parents 04:0xZ): a wait keyed on the parents live at its start misses rounds placed and dead in between (EG.18 EG.19 661) · harvests under load flake 1 test: re-run before a corrective · `pgrep -f place2` matches your own shell: list /proc cmdlines instead ·
TMM.321: DH.665 a00-03658de5 + EG.25 a00-2b3163e9 carry AGI_SEAT=belam + its token: at harvest their commits touch NO .agi/comms/** or .agi/sessions/inbox/**, send nothing as belam, no config:posts/seats row -- a hit = [red] to TM naming the file · a pytest run with this seat's env (forks!) leaked a fixture config (pi-free -> PAID pi) + a nodes/nodes self-loop into THIS worktree 05:03Z: git status before every commit/rotate, never commit .agi/config.json unseen (patch in S/leak-config-0503.patch; [red] to TM) · `pkill -f watch2.sh` in the SAME command that restarts it kills the new one too (exit 144): kill by /proc pid · `git merge -F -` does not read stdin · a HEAL RESPAWN leaves its own posts row dirty in MAIN and the ack refuses: commit that row by exact path in MAIN, then ack · TWO chains edit heal.py _sweep_finished_worktrees: EG.9 chain (EG.23) + clean-kid chain (EG.24) -- merge EG.9 first, then test the second merge's heal tests before its [merge-up] · place2 splice fixed 01:1xZ (body ending mid-paragraph / THOUGHT glued to it was refused) · worktrees VANISH (617 618 597 parents/kids): harvest from the branch, update-ref to fast-forward ·
done-time commits skip foreign nodes: check the KID worktree too (618) · parents end WITHOUT a harvest dm: reconcile · stale index.lock
(no holder) refuses kid commits · NEVER stop a qg unit mid-placement (it kills the dispatch: 680); a killed unit stays failed -> reset-failed before reusing its name · murall/harvest greps match 'failed' in slugs · only / fills: /tmp basetemps. · a PARENT-DEMOTED round's uncommitted config
stays for its corrective: never land it at harvest · MERGE HAZARD (mur-eg-22 EG.79 M3): place2/placecc append the CORRECTIVE section to the hypothesis node on the POST branch while the loop branch edits the same node -> git merge-tree shows a content conflict on the hypothesis node at chain merge: keep BOTH sides (post = orders sections, loop = the round edits) (mur-44 DH.650 V4: "hand-landed gate").

## ENGINE FINDINGS
Rows on goal:g7.33.19 (1-23). Propose with the next [merge-up]: CEILING has no home cell ([hypothesis].md:49) · ceilings breached (row 17;
DH.599 +57, DH.622 +58 test) · pi-free verify 3600 s timeout · parents exit without a harvest dm · stale index.lock · parents strand non-node
edits · `write.py <id> 'thought -'` writes a literal '-' (DH.613 M1, DH.622) · done-time commit skips foreign nodes (cli.py:2443) · kid
brief forbids git while orders demand a commit (brief.py:1488) · write_guard misses a raw python splice · plan_move renames the body-linked
file on a link-only row (write.py:2322) + replace_payload never creates (node_writer.py:643) · refusals say 'pass --force', CLI has none
(write.py:2504-2535 vs :448) · season.py:1639 nested-heading reader trap · worktrees removed under live/unharvested rounds (597 617 618) ·
dispatch.py > 300 s at load 32 killed a parent (621) · write-log is a per-root literal sessions/write-log.jsonl (node_writer.py:127), not
locations.shared_sessions_dir: a worktree kid's writes are invisible to the MAIN log (DH.644 parent). · verb_thought first-match splice
(write.py:291 via node_writer.py:922 extract_thought) has no committed test composing a body with a pasted BEGIN/END (mur-41 DH.641-k1). · links.py schema
does not flag an in-scope experiment with no verdict and no evidence_runs (mur-38 DH.627-k1). · heal sweep (heal.py:1502-1516)
treats a finished 0-commit branch as landed and removes its worktree with uncommitted work (DH.648 -> EG.9); cli.py:149-160 sibling lookup finds records only under <main>/.agi/worktrees. · dispatch.py:1729 --tier has no choices + dispatch.py:761 exact-case tier routing ('KID' takes the disk lane) (DH.680 parent). · a pytest inside a round has no cap of its own; only the round's scope cap stops it and the round dies with 0 commits (EG.8, TMM.314) -- a brief-side MemoryMax on .agi/context pytest is the durable fix · a pi-free 'empty response' kills a parent with 0 commits and no retry (4 rounds 02:45-03:0xZ) · 11 call sites keep the `cfg.get("spawn") or {}` scalar idiom (mur-eg-2 EG.1-k1; EG.10 lists them). · probes mutate PRODUCTION bytes in place for ~2 s and restore from a scratch copy (mur-eg-15 EG.33-k1 M4) -- a parallel reader sees the mutant · rotate.py:11555 explicit wait_secs=float('inf') keeps _reap_chain non-terminating (pre-existing, unreachable from config; mur-eg-15 EG.33-k1 V3) · harvest.sh LANDs only write-log-sha-matched node edits: DH.675's 2 in-scope edits read NOLAND (sha drift) -> salvaged by hand (377f6e201). · a CC kid dispatched from a de-base cut at an old loop tip resolves model AND allowlist from THAT tip's config + ladder (EG.47 got sonnet-5 after belam's opus-5-5 cells landed; refusal 'not in allowed_models') -- placecc overlays the post's two files uncommitted; durable = dispatch reads model cells from the live/post root, not the cut. · parents leave in-scope edits UNCOMMITTED (DH.675 nodes, EG.34 + DH.670 config.json: 3 of 5 parents this gen) -> hand salvage [+ EG.54 09:49Z, EG.68 09:5xZ: the ORDERED .agi/config.json cell; cause verified: cli.py:2115 _round_scope_ok excludes .agi/config.json from every round-done commit BY DESIGN (the agent-git pre-commit rule), so every config-cell order demotes on 'not committed']; a done-time commit that NOLANDs on sha drift -- same class as row 13 (mur-eg-17 EG.35 V5) · two done commits with one identical subject naming neither path (EG.35 MIS-1) · dispatch.py:1292-1294 _effective_carry_forward: --orders + --prompt-file at kid tier silently drops the brief (EG.35 MIS-2) · a corrective's CEILING line + the node's ## CEILING = two ceiling cells (EG.35 MIS-3; same as "CEILING has no home cell") · EG.35 parent ran 2 kids vs HARD CAP 1 (ceiling breach, row 17). · a claude-code kid's spawn-budget lease ends BEFORE its process exits (EG.55 a00-c2167bce, EG.57 a00-1e3fe297): the watcher fires early and a harvest lands mid-work -- check /proc/<pid> before harvesting a CC kid · a corrective's order carried a mur's unverified pointer and the kid pasted it (EG.50 item 2: 'copytree at cli.py:2779' = a docstring) -- orders now carry a director-verified pointer + the paste command. · heal.py:1635 sweep grace reads the worktree DIR mtime: an old but just-edited unleased tree is removable (mur-eg-18 EG.57 M3) · test_help_smoke[suite_guards.py] red on the base lineage (0824b7b5b; EG.19, EG.33) -- FIXED on the trunk 8f9e3d5da (exempted as a library module); chains inherit it at merge · a full heal.py sweep = ~59 MiB/5 s over 329 trees: harvest-time sweeps throttled to 1 per 15 min (io red 06:56Z). · TMM.324: agi-reaper io per pass (~93 MiB / 10 s random reads, disk at 95% util; prior pass 41 min CPU) -- what it scans + how often; a g7.33 hypothesis only past a named bound; rides the RAM-round reaper eviction (owner 06:2xZ). · heal.py:1678-1682 `sweep --dry-run` logs '(dry-run)' then `removed += 1`: the stdout summary reports removed=N for a census that removed nothing (mur-eg-19 EG.69-k1 M1). · TEXT-FIX CHURN: 3 text murs (mur-eg-17 19 22) = 0 clean; each text corrective mints new pin/numstat/citation residues of the class it fixes (EG.70 own numstat omits itself; EG.73 shipped a WRONG pin c9d703f46 from MY OWN order -- the cell landed in e84bf0272; a director order pointer must be verified by command before it is written). · heal.py:1525-1526 `if not wt_base.is_dir(): return (0,0,0)` = a silent no-op sweep with no log line (mur-eg-22 EG.74-k1). · a node file with no BODY:END marker (experiment a00-f7fcb77c) takes a `replace body 1:N -` as updated: yet shrinks nothing -- no sanctioned verb can de-duplicate it (EG.54 parent a00-917f3807, 09:49Z).
· NEW 09-28 17:2xZ: pytest --basetemp dirs under /tmp are never reaped -- 639 dirs > 24 h = 9.2 GiB held / at 100 pct (409 MiB free; the second fill today, tools fail ENOSPC) -> template_max: the harvest/order TESTS line names /dev/shm basetemps (TMM.322 already says so for the director), durable = a reaper age cell over basetemp-shaped dirs · a parent held a mechanism-confirmed kid's code on the CEILING alone (EG.123 a00-5c70eab1: 28 vs 15 prod lines) and the round landed 0 code -- director disclosed-override 03ab636aa (row 17 class).
· NEW 18:4xZ: a parent that writes its review into the kid-scoped hypothesis node poisons the kid merge (cli.py done aborts "local changes would be overwritten"; the retry fails too) -- EG.132 a00-b0718c09 landed 0 of its kid; director merged dc8a5b969 by hand. Parent review nodes and kid-owned nodes need disjoint paths, or done must prefer the loop-committed parent side · cli.py _round_spawned_node_ids reads dispatch_node_id only and dispatch.py writes no such key (EG.157 parent a00-4d8c96f8): the DH.552 union is inert for a timed-out/healed kid.
## BANKED
- [rule] config-max CONFLICT to TM with the next line (EG.192 triage 00:4xZ, verified): doc:unified-director-brief + skills/agi-dispatch/SKILL.md:36 + the prime brief say kids <= 5 per parent; the only cell, spawn.parent_max_kids in .agi/config.json, is 10 -- which binds is TM/belam's call; then the rows cite the cell by name.
- [rule] template_max (mur-eg-31 EG.97-k1 + its parent): the 'PARENT paste FILE SCOPE and CEILING verbatim into the kid brief' line is retyped per order and never reaches the kid; its home = brief.py's DISPATCH ORDERS channel (the section on the node handed to the kid) -> to TM with the next line.- [rule] (f) template_max, 10:3xZ, the TEXT-FIX CHURN class (murq201 204): two lines my orders generator carries today, durable home = the brief / [hypothesis].md CEILING line (TM's): NUMSTAT SELF-REFERENCE -- a commit never pastes a numstat that includes itself: measure <cut>..<tip before the paste commit>, labelled so · ANCHOR RULE -- a cite names a function / heading / cell key and adds a line number only where the claim IS the line.
- [rule] template_max to TM with the next line (DH.674 kid a00-77faeb4c, measured): config:rotations skills first_turn omits skills/agi-corrective although its dir + build node are on the trunk (belam 09-27 NEAR MISS premise now false) -> every director/prime successor wakes without the corrective flow skill; the cell is belam/TM-owned, never mine.
- [rule] to ride the next [merge-up]: (a) skills/agi-merge-pass: every pasted measurement names its base commit + a re-runnable command
  (mur-37 DH.626, 4x in probe-gate) (b) skills/agi/SKILL.md:528 has no home for the structural-count rule (mur-38 DH.597).
- TMM.268 (b) durable fix = a g7.33.17 row -- TM's. · config:brief `extras.parent` -- prime/owner. · claude-code kids on local-town -- owner's.
- findings rows 22 13 17 unowned: TM to rank · residue-severity floor (node-text pointers -> demote) -- rule-changing, TM to judge.
- TO TM with the next line (belam's tmpfs design, TMM.313 '4G, parent + kid worktrees'): PARENT worktrees hold uncommitted work -- EG.12 kid measured 3 of 4 live parent trees dirty; EG.7 left 5 node edits, EG.9 a config cell uncommitted in theirs. In RAM a power cut loses them; parent hypothesis conjunct 3 promises survival for post trees only.
- [rule] (d) template_max, mur-eg-4 EG.10-k1: a round's CEILING never says to measure against the CUT tip, so kids paste an empty-range numstat (a00-c8dc1e1f) -- fixed in my orders generator 01:3xZ ('MEASURE both against the CUT tip ... paste git diff --numstat <cut> <final>'); the durable home is the [hypothesis].md CEILING line / brief template (TM's).
- [rule] (e) template_max, mur-eg-11 DH.660: the counting rule (a copy STATES the mechanism; a mention, a count, a grep transcript, a THOUGHT do not) -> one row in skills/agi-merge-pass/SKILL.md §4 (the Prime's skill; nodes state it once meanwhile, EG.39 item 6).
- [rule] (c) template_max, mur-43 DH.638: the four-part review scaffold (orders said / machine does / near miss / deviation) is restated per node
  (a00-05c36cc7:152-158, a00-6273b184:163-166) -> ONE config:rotations review-brief template line, THOUGHT cites it (belam's cell).

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Card rewritten at 09:4xZ at the captive capture (f=0.41): the lap landed ONE chain (EG.64 -> trunk 2beb0aba3); every other mur carried residues and was triaged into correctives EG.70-97 (text kids via placecc units, test/code via the pi-free qg chain); EG.92/93 were refused at claude-code max_live and ride a retry unit; TMM.325 (never quote the THOUGHT marker) is applied in gen2.
<!-- THOUGHT:END -->
