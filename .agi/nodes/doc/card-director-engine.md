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

## §0 STATE (07:3xZ 09-28 · seated by the captive capture 07:13Z · per-chain history = git log of this node)
```
MERGE-UP  last LANDED: EG.1 chain 57debf3a2 (TMM.318). EG.64 chain MERGED on the post 19564b6c0 (mur-eg-19 ACCEPT; 467 passed) -> [merge-up] to TM 09:2xZ, awaiting TM gate
SERIES    next EG.95 · murs mur-eg-N (last read mur-eg-23 = murq189 + mur-eg-22 = murq186) · next murq194
TOOLS     T=<scratchpad 96494ce7-...>: gen2.py N murq<Q>.json tip label (MURK=, NOEX=1, EXTRA=; triage by hand) · place2.sh (pi-free parent) ·
          placecc.sh (CC TEXT KID; overlays the POST config+ladder so kids resolve opus-5-5) · placef.sh N HYP (fresh) · mkmur.py + runmur.sh ·
          hcc.sh N (CC kid: waits for its PID, not its lease, then flock-harvests) · D=<scratchpad 4cf27ed6-...>: verd.py Q · harvest-all.sh N
          (TMM.322 pytest env; ends with a heal.py sweep, ONE per 15 min) · S=<scratchpad d74d6d20-...>/watch2.sh MURS="murq191 murq193" (run_in_background)
GATE      TMM.306 load1 < 16 AND io avg60 < 50, two reads 5 min apart · CC kids: <= max_live 4, MemAvailable >= (live+2) x 2G · belam: a memory
          ALARM -> hold new placements
OWNER     05:2xZ via belam 05:38Z: CC kids + parents = claude-opus-5-5 (merged 11476d1f6) · 06:2xZ via belam 06:21Z: (a) sweep at EVERY harvest,
          never --force (skill row = EG.57 -> EG.69) (b) per-ROLE worktree roots + reaper eviction WITH the RAM round, not EG.53 (c) object store left
          · 06:4xZ via belam 06:27Z: progress -> board 'note' -- REFUSED for posts (goal:g12) -> TMM.323: progress in §2 until EG.59 lands
TMM.322   (3) every pytest: TMPDIR + --basetemp /dev/shm, env -u TMUX -u TMUX_PANE -u AGI_POST -u AGI_SEAT · (1) = EG.60 · (2) answered
MURS murq193 = EG.48 (45d9be0d7; 116 passed + suite_guards BASE red; STRAY file named = committed at root) · murq192 = EG.60 (bfc310107; verdict UNSET; CEILING BREACH 2 kids + test 63 net vs 30) · murq190 = DH.674 (DISPROVED: skills first_turn omits agi-corrective; tests 6 passed) · murq191 = DH.661 (node only; kid branch superseded) · murq189 = EG.44 (850091463; 107 passed + suite_guards BASE red + ws_raw_client load flake) · murq188 READ -> EG.86 · murq187 = DH.673 (first round, a5478e026; 95 passed provisioning) · murq186 READ -> EG.83-85 · murq183 = EG.41 (ecaab9920; 427 + 55 passed; send.py +15 -1; parent dm 07:40Z: item 5 OPEN = 3 stale send.py pointers at a00-c3bf7379:42,45 + a00-5e3cfa03:135 -> add to the murq183 triage) · murq184 = EG.59 (first round, 309fdb267; 147 passed; CEILING BREACH 2 kids + prod 33 net + test 171 -> residue) · murq185 = EG.37 (7030a6261; 166 passed + test_write unknown-location red = BASE lineage, red at f812751ad too)
          · READ: murq172 -> EG.70 EG.71 (text) + EG.72 (pi) · murq177 EG.19 DEMOTE (4/5 items uncommitted in a00-3c15c94c) -> EG.73 (text + 1 skill row) · murq179 EG.69 awr (3 row residues) -> EG.74 · murq180 DH.672 awr (--cap zero_usd test pin) -> EG.75 pi · murq181 EG.36 awr (verify died; 4 node + rlimit/config_max test) -> EG.76 pi · murq183 EG.41 awr (verify died; 3 node-text) -> EG.77 (placecc10) · murq184 EG.59 awr (ceiling breach + 3 missing tests + dedup) -> EG.78 pi (net <= 0 prod/test) · murq182 EG.58 awr (review died; 4 test/text) -> EG.79 pi OWN LANE HARVESTED -> murq188 · murq185 EG.37 awr (test anchoring + _node_fm 2nd source) -> EG.80 pi · murq187 DH.673 awr (vacuous sys.path guard test) -> EG.81 pi · murq189 EG.44 DEMOTE (all node text; 2 deletions to restore) -> EG.82 (placecc11) · murq186 EG.70 awr + EG.73 DEMOTE + EG.74 awr (all text) -> EG.83 84 85 (placecc12) · murq188 EG.79 awr (text: stale lines, self-refuting comment) -> EG.86 (placecc13) · murq190 DH.674 awr (tripwire test, circular cap, 221 vs 120) -> EG.87 pi · murq178: EG.64 ACCEPT -> MERGED 19564b6c0 + [merge-up] delivered 09:2xZ; EG.61 62 63 65 66 67 awr (text) -> EG.88-93 (placecc14) · murq192 EG.60 DEMOTE (test logic) -> EG.94 pi
KIDS      placecc6 OOMD-KILLED 07:48Z mid-dispatch of EG.70 (orders cd5bd057c, cut left overlay-dirty, no spawn) -> recovery unit placecc9 PLACED 07:58Z (EG.70 a00-775fe9d4 · EG.71 a00-475427c2): EG.70
          dispatch-only from de-base-EG.70 + restore, then EG.71 via placecc.sh (auto-harvest hcc) · EG.73 HARVESTED af9cb933c + EG.70 HARVESTED 49b7b899d -> murq186 · EG.71 EG.77 LIVE · EG.74 HARVESTED fc894e586 (72 passed; mur with EG.73) a00-dbc0e8a5
          ENDED 07:56Z, hcc harvesting · EG.51 V3/M2 ladder ultracode pair = DEMOTED: owned by EG.56 -> EG.67
PI LANE   EG.58 = EG.9 chain REDO HARVESTED -> murq182 (own lane, FIRST; EG.50 parent-demoted, 0 commits, NOT landed; pointer cli.py:3066 / copy2 :3207 :3211 verified)
          -> EG.59 (board note verb grant) HARVESTED -> murq184 -> EG.60 HARVESTED -> murq192 (test-root leak) · chain qgEG(36 37 41 44 48 done) 42 -> 48 (EG.33) 49 (EG.31) 53 (EG.18) 54 (EG.34
          DEMOTE) 68 (DH.671) 72 (EG.52 + test_write.py pin) 75 (DH.672 test pin) 76 (EG.36) 78 (EG.59) 80 (EG.37) 81 (DH.673) 87 (DH.674) 94 (EG.60) · qgRS serial lane (EG.19 done -> 661 HARVESTED -> EG.20) · drainqg13..18: 672 673 674 HARVESTED · 678 · 679 · EG.2 EG.3 · EG.5 · EG.6
PASS 12   belam 06:50Z goal:g1.28 (on the TRUNK: merge local-maxxing/season2/main first), BEHIND the fix queue: 5 engine hypotheses (create/API
          set-verbs gate · suite fence stdlib spawn leaves · done commit never sweeps the gate source · seat-wrap DEMOTE · heal seat path cell WITH
          per-role roots) + hypothesis:pass12-0928-residue-batch (153 items) -> opus text kids <= 4
TMPFS     belam TMM.319: KID worktrees ONLY in RAM, PARENT on disk · GO = EG.9 chain MERGED + 24 h no memory crit
HELD      demoted/out-of-scope uncommitted bytes: EG.7 (a00-0194accb) · EG.30 · EG.24 · EG.50 (a00-44cd2258) · DH.671 cell (a00-6f49a5f0) -- never land · EG.19 (a00-3c15c94c, 4 nodes)
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
- 07:1x-07:4xZ: 5 murs judged (murq172 = 2 awr + 1 demote · 177 demote · 179 awr · 180 awr · 181 awr), 0 clean · 7 correctives (EG.70 71 73 74 text · EG.72 75 76 pi) · 7 harvested (EG.69 DH.672 EG.36 EG.58 EG.41 EG.59 EG.37) · 1 hand salvage (EG.36)

## 🔴 WHERE IT STOPS
07:3xZ: murq172 + murq177 triaged -> EG.70 EG.71 (placecc6) + EG.73 (placecc7) + EG.74 (placecc8) + EG.72 EG.75 EG.76 (qgEG72 75 76, last in chain); murq178 182-185 running; watch2 armed
```
FIRST   on a watch2 EVENT: a mur ended -> D/verd.py Q -> triage (skill agi-corrective §3): pure text -> gen2 EG.73.. + a placecc<N>.sh unit; mixed ->
        a qgEG<N> unit chained after the last qg; a clean round -> git merge --no-ff its tip -> [merge-up] to TM (batch + mur key + verdicts + findings)
        · a parent/kid ended unharvested -> D/harvest-all.sh N (CC kid: hcc.sh already queued by placecc6) · re-arm MURS with whatever is still active
THEN    EG.70 EG.71 EG.73 EG.74 harvest -> ONE text mur over all (mkmur per round, merge the two json rounds[] by hand) · pi lane as §0 PI LANE (gate-held)
        · PASS 12 (goal:g1.28, merge the trunk first) behind all of it
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
treats a finished 0-commit branch as landed and removes its worktree with uncommitted work (DH.648 -> EG.9); cli.py:149-160 sibling lookup finds records only under <main>/.agi/worktrees. · dispatch.py:1729 --tier has no choices + dispatch.py:761 exact-case tier routing ('KID' takes the disk lane) (DH.680 parent). · a pytest inside a round has no cap of its own; only the round's scope cap stops it and the round dies with 0 commits (EG.8, TMM.314) -- a brief-side MemoryMax on .agi/context pytest is the durable fix · a pi-free 'empty response' kills a parent with 0 commits and no retry (4 rounds 02:45-03:0xZ) · 11 call sites keep the `cfg.get("spawn") or {}` scalar idiom (mur-eg-2 EG.1-k1; EG.10 lists them). · probes mutate PRODUCTION bytes in place for ~2 s and restore from a scratch copy (mur-eg-15 EG.33-k1 M4) -- a parallel reader sees the mutant · rotate.py:11555 explicit wait_secs=float('inf') keeps _reap_chain non-terminating (pre-existing, unreachable from config; mur-eg-15 EG.33-k1 V3) · harvest.sh LANDs only write-log-sha-matched node edits: DH.675's 2 in-scope edits read NOLAND (sha drift) -> salvaged by hand (377f6e201). · a CC kid dispatched from a de-base cut at an old loop tip resolves model AND allowlist from THAT tip's config + ladder (EG.47 got sonnet-5 after belam's opus-5-5 cells landed; refusal 'not in allowed_models') -- placecc overlays the post's two files uncommitted; durable = dispatch reads model cells from the live/post root, not the cut. · parents leave in-scope edits UNCOMMITTED (DH.675 nodes, EG.34 + DH.670 config.json: 3 of 5 parents this gen) -> hand salvage; a done-time commit that NOLANDs on sha drift -- same class as row 13 (mur-eg-17 EG.35 V5) · two done commits with one identical subject naming neither path (EG.35 MIS-1) · dispatch.py:1292-1294 _effective_carry_forward: --orders + --prompt-file at kid tier silently drops the brief (EG.35 MIS-2) · a corrective's CEILING line + the node's ## CEILING = two ceiling cells (EG.35 MIS-3; same as "CEILING has no home cell") · EG.35 parent ran 2 kids vs HARD CAP 1 (ceiling breach, row 17). · a claude-code kid's spawn-budget lease ends BEFORE its process exits (EG.55 a00-c2167bce, EG.57 a00-1e3fe297): the watcher fires early and a harvest lands mid-work -- check /proc/<pid> before harvesting a CC kid · a corrective's order carried a mur's unverified pointer and the kid pasted it (EG.50 item 2: 'copytree at cli.py:2779' = a docstring) -- orders now carry a director-verified pointer + the paste command. · heal.py:1635 sweep grace reads the worktree DIR mtime: an old but just-edited unleased tree is removable (mur-eg-18 EG.57 M3) · test_help_smoke[suite_guards.py] red on the base lineage (0824b7b5b; EG.19, EG.33) · a full heal.py sweep = ~59 MiB/5 s over 329 trees: harvest-time sweeps throttled to 1 per 15 min (io red 06:56Z). · TMM.324: agi-reaper io per pass (~93 MiB / 10 s random reads, disk at 95% util; prior pass 41 min CPU) -- what it scans + how often; a g7.33 hypothesis only past a named bound; rides the RAM-round reaper eviction (owner 06:2xZ). · heal.py:1678-1682 `sweep --dry-run` logs '(dry-run)' then `removed += 1`: the stdout summary reports removed=N for a census that removed nothing (mur-eg-19 EG.69-k1 M1). · TEXT-FIX CHURN: 3 text murs (mur-eg-17 19 22) = 0 clean; each text corrective mints new pin/numstat/citation residues of the class it fixes (EG.70 own numstat omits itself; EG.73 shipped a WRONG pin c9d703f46 from MY OWN order -- the cell landed in e84bf0272; a director order pointer must be verified by command before it is written). · heal.py:1525-1526 `if not wt_base.is_dir(): return (0,0,0)` = a silent no-op sweep with no log line (mur-eg-22 EG.74-k1).
## BANKED
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
Card written at 07:2xZ after the captive-capture seat: murq172 triaged (EG.47-k1 + EG.51-k1 text -> EG.70 EG.71 CC kids; EG.52-k1 demote needs a committed test_write.py pin -> EG.72 pi-free, chained after qgEG68); EG.51 ladder ultracode pair demoted to EG.56 -> EG.67 (lineage conflict, not the round); EG.69 harvest red was a load flake (re-run 72 passed).
<!-- THOUGHT:END -->
