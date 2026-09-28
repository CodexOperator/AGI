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

## §0 STATE (00:3xZ 09-28 · seat woke 22:31Z 09-27 · per-chain history = git log of this node)
```
MERGE-UP  [merge-up] to TM 00:3xZ 09-28 (belam [decision] 00:0xZ, owner: WHOLE post branch, in-progress included) -- tip d4446340f,
          mb 26d914498, 188 files, 365 passed 1 RED declared (boxkit probe vs the 429 tasks-max chain -> EG.1), 28 nodes labelled ## OPEN
SERIES    RESET: rounds EG.N (EG.1-5 used, next EG.6) · murs merge_up "eg" -> mur-eg, mur-eg-2 ... (T/mkmur.py 6th arg = "eg"); DH.N queued
          before the reset keep their labels (orders already generated) -- the counter only moves forward
TOOLS     T=<scratchpad 96494ce7-...>: MURK=<key> [EXTRA=f,g] gen2.py N murq<Q>.json tip label -> orders<N>.md (N may be EG.n: sed the
          header to CORRECTIVE EG.n) · place2.sh / placef.sh N (DH.N or EG.N label) · drainqgf.sh N:K (K=F fresh via h<N>.txt) · mkmur.py + runmur.sh
          D=<scratchpad 4cf27ed6-...>: verd.py Q · harvest-all.sh N (removes a RAM de-base + its symlink after copying sessions to flash)
GATE      TMM.306: load1 < 16 AND io PSI avg60 < 50 on two reads 5 min apart, one placement per pass · arm 10 · key cap x live < balance
PLACEMENT de-base-N ON DISK (the /dev/shm variant broke parent done -> DH.648 swept, reverted 00:0xZ); 651's RAM checkout is symlinked
PRUNE     unit prune-debase (TMM.309 GO: idle io, io<50, 1/30 s, lossless, skips symlinks; log in the flash harvest dir) 41 removed so far
LIVE      no parent · murq128 = mur-eg (DH.651, harvested d21100a87, the suite_guards red inherited) · murq125 126 127 ENDED -> EG.2 EG.5 EG.3 (126: kid item-4 edit landed 867b44a8b)
QUEUE     qg2 EG.1 680 653 · qg3 654 · qg4 655 656 · qg5 657 · qg6 658 · qg7 659 · qg8 660-664 · qg9 665 · qg10 666 · qg11 668 · qg12 669 ·
          qg13 675 670-674 (g1.27) · qg14 678 · qg15 679 · qg16 EG.2 EG.3 · qg17 EG.5 (chained units, T/drainqg<N>.log)
BELAM     00:0xZ order: (1) merge-up DONE (2) counters DONE (3) RAM: report the tmpfs claim PROVED when the kid-worktrees chain clears
          (680 -> then mint the 17-consumer routing round) -- belam then does guard.env + guard-init (4) NEXT, dependency order:
          g4.18.1.2 = EG.4 hypothesis:a-draft-mints-one-checked-row-per-call MINTED f1d6f12a1,
          QUEUE it (EG.4:F, h-file) only after DH.660 clears, cut from that g4.18.1.1 tip -> g7.32.6 send pipeline core -> g7.31.3.3 rotate core (EG rounds, briefs on nodes)
DECISION  out to TM: DH.577 cron policy (send-hub chain HELD) · wake-facts touches config:rotations (belam's) · logs: symlink until EG.2 lands
```

## §1 PLAN
```
next   (1) per ENDED mur: D/verd.py Q -> clean = git merge --no-ff the chain tip · residue -> gen2 (EG.N) -> a qg unit
       (2) harvest each ended parent AT ONCE (the sweep reaps a 0-commit worktree after 30 min) (3) belam (3)+(4) above
```

## 🔴 WHERE IT STOPS
Merge-up out to TM (red declared, EG.1 fixes it); counters reset (mur-eg live); every ended mur triaged; murq128 (DH.651) running.
```
FIRST   D/verd.py 128 (mur-eg, DH.651) -> clean: merge the chain tip · residue: EG.6 ; watch T/drainqg2.log (EG.1 heads it)
        ; spawn_budget.py status ; systemctl --user list-units 'agi-director-engine-*' ; send.py read director-engine (TM gates the merge-up)
THEN    EG.4 (g4.18.1.2) queues only after DH.660 clears (cut from its tip) ; brief g7.32.6 send pipeline core, then g7.31.3.3 (belam item 4)
```

## §4 TRAPS
Skills: agi-dispatch §5 · agi-corrective · agi-workflow · agi-node-write §5 · agi-memory-guard · agi-master-gate (TMM.304). Card-only: pi-free murs ~7 min/stage, verify can die (review stands) ·
harvests under load flake 1 test: re-run before a corrective · `pgrep -f place2` matches your own shell: list /proc cmdlines instead ·
`git merge -F -` does not read stdin · worktrees VANISH (617 618 597 parents/kids): harvest from the branch, update-ref to fast-forward ·
done-time commits skip foreign nodes: check the KID worktree too (618) · parents end WITHOUT a harvest dm: reconcile · stale index.lock
(no holder) refuses kid commits · murall/harvest greps match 'failed' in slugs · only / fills: /tmp basetemps. · a PARENT-DEMOTED round's uncommitted config
stays for its corrective: never land it at harvest (mur-44 DH.650 V4: "hand-landed gate").

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
treats a finished 0-commit branch as landed and removes its worktree with uncommitted work (DH.648); cli.py:149-160 sibling lookup finds records only under <main>/.agi/worktrees.

## BANKED
- [rule] to ride the next [merge-up]: (a) skills/agi-merge-pass: every pasted measurement names its base commit + a re-runnable command
  (mur-37 DH.626, 4x in probe-gate) (b) skills/agi/SKILL.md:528 has no home for the structural-count rule (mur-38 DH.597).
- TMM.268 (b) durable fix = a g7.33.17 row -- TM's. · config:brief `extras.parent` -- prime/owner. · claude-code kids on local-town -- owner's.
- findings rows 22 13 17 unowned: TM to rank · residue-severity floor (node-text pointers -> demote) -- rule-changing, TM to judge.
- [rule] (c) template_max, mur-43 DH.638: the four-part review scaffold (orders said / machine does / near miss / deviation) is restated per node
  (a00-05c36cc7:152-158, a00-6273b184:163-166) -> ONE config:rotations review-brief template line, THOUGHT cites it (belam's cell).

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Whole rewrite at 00:3xZ 09-28 after belam [decision] 00:0xZ (owner): the merge-up went out with its one red declared and fixed by EG.1, the DH counter reset to EG, and the /dev/shm dispatch checkout was reverted because it broke parent done (DH.648 swept). Card trimmed to 100 lines: the resolved trunk-merge traps dropped.
<!-- THOUGHT:END -->
