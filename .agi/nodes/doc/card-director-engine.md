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

## §0 STATE (03:2xZ 09-28 · seat woke 00:45Z · per-chain history = git log of this node)
```
MERGE-UP  EG.1 chain [merge-up] to TM 02:25Z -- TIP 95c425f8c, MB dc93a2660, 21 files +1149/-69, 0 deletions, 123 passed; 1 DECLARED residue carried
          (mem_cap.py:89-90 docstring -> Item 7 round) · TM has not answered yet (owner 02:2xZ: a TM send may have failed; owner checking)
SERIES    EG.N (next EG.29) · murs merge_up "eg" -> mur-eg-N (next mur-eg-10) · DH.N queued before the reset keep their labels
TOOLS     T=<scratchpad 96494ce7-...>: MURK=<key> [EXTRA=f] gen2.py N murq<Q>.json tip label (run FROM the worktree; sed header DH.EG.n -> EG.n)
          · place2.sh N (splice fixed 01:1xZ) · placef.sh N (fresh) · redispatch2.sh N (dead round, EG labels ok, gated) · mkmur.py + runmur.sh
          · qgEG<N>.sh = gate -> place2 (chain via `while is-active qgEG<prev>`) · D=<scratchpad 4cf27ed6-...>: verd.py Q · harvest-all.sh N...
GATE      TMM.306: load1 < 16 AND io avg60 < 50, two reads 5 min apart, one placement per pass · arm 10
LIVE      no parent at 03:2xZ · no mur running · everything below is QUEUED in chained units (systemctl --user list-units 'agi-director-engine-*')
FRONT     EG.27 (qgEG27) = EG.9 heal-sweep chain: EG.23's kid DIED on its last write -> director SALVAGE 344d79ad2 (UNREVIEWED) -> EG.27 cut from it,
          FIRST ACT verify + close heal.py:1683 rc-discard fail-open. TMM.313: tmpfs GO waits on this chain MERGED + 24 h no memory crit
RE-DISP   provider-dead 02:45-03:15Z (pi-free empty response, 0 commits): qgR660 (DH.660) -> qgR2 (EG.18 EG.19 661) -> qgR3 (EG.20) · [red] to TM 03:1xZ
QG-EG     EG.21 (EG.13 chain, memory-cap HARD RULE) -> EG.22 (DH.657) -> EG.24 (DH.655 clean-kid; BOUNDARY vs EG.9) -> EG.25 (DH.659 parent-demote)
          -> EG.26 (EG.16/DH.653) -> EG.28 (DH.656, mur-eg-9 verify: cli.py guard unpinned, cache key fail-open)
QG-DH     drainqg8.. chain (T/drainqg<N>.log): 662-664 · 665 · 666 · 668 · 669 · 675 670-674 · 678 · 679 · EG.2 EG.3 · EG.5 (facts chain, TMM.313 (2):
          goes up as ONE [merge-up], lands with belam's F13 trim + cell) · EG.6
HELD      EG.11 (folded into EG.14's item 4) · EG.7's 5 corpus edits stay UNCOMMITTED in a00-0194accb (parent-demoted, never land)
NEXT      EG.1 lands -> Item 7 config-max round (AGI_TASKS_MAX cell + the carried docstring), behind the EG.9 chain · EG.4 after DH.660 clears ->
          g7.32.6 send core -> g7.31.3.3 rotate core (belam item 4) · kid-worktrees chain clean -> tmpfs claim to belam + the 17-consumer round
DECISION  out to TM: DH.577 cron policy (send-hub chain HELD) · wake-facts touches config:rotations (belam's) · logs: symlink until EG.2 lands
```

## §1 PLAN
```
loop   per ENDED parent: harvest AT ONCE (D/harvest-all.sh N; a 0-commit tip = provider-dead -> redispatch2.sh) -> mkmur/runmur
       per ENDED mur: D/verd.py Q -> clean = git merge --no-ff the chain tip -> [merge-up] · residue -> gen2 EG.N -> qgEG<N> chained last
       ceiling breaches = RECORDED residues (TMM.315), never a prose-only corrective · uncommitted in-scope bytes of an ACCEPTED round: land them;
       of a DEMOTED round: never; of a DEAD kid: salvage-commit on the kid branch, UNREVIEWED, and re-run from it
```

## 🔴 WHERE IT STOPS
Queue drained into chained gated units; EG.27 (EG.9 chain, from the salvage) at the front; EG.1 merge-up 95c425f8c waits on TM.
```
FIRST   send.py read director-engine ; spawn_budget.py status (every ended parent -> harvest AT ONCE) ; systemctl --user list-units 'agi-director-engine-qg*'
THEN    EG.27 ended -> harvest -> mur (range a935bf010..tip covers the salvage) ; TM answers the EG.1 merge-up -> Item 7 round ; murs -> verd.py
```

## §4 TRAPS
Skills: agi-dispatch §5 · agi-corrective · agi-workflow · agi-node-write §5 · agi-memory-guard · agi-master-gate (TMM.304). Card-only: pi-free murs ~7 min/stage, verify can die (review stands) ·
WATCH NEW PARENTS TOO: a wait keyed on the parents live at its start misses rounds placed and dead in between (EG.18 EG.19 661) · harvests under load flake 1 test: re-run before a corrective · `pgrep -f place2` matches your own shell: list /proc cmdlines instead ·
`git merge -F -` does not read stdin · TWO chains edit heal.py _sweep_finished_worktrees: EG.9 chain (EG.23) + clean-kid chain (EG.24) -- merge EG.9 first, then test the second merge's heal tests before its [merge-up] · place2 splice fixed 01:1xZ (body ending mid-paragraph / THOUGHT glued to it was refused) · worktrees VANISH (617 618 597 parents/kids): harvest from the branch, update-ref to fast-forward ·
done-time commits skip foreign nodes: check the KID worktree too (618) · parents end WITHOUT a harvest dm: reconcile · stale index.lock
(no holder) refuses kid commits · NEVER stop a qg unit mid-placement (it kills the dispatch: 680); a killed unit stays failed -> reset-failed before reusing its name · murall/harvest greps match 'failed' in slugs · only / fills: /tmp basetemps. · a PARENT-DEMOTED round's uncommitted config
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
treats a finished 0-commit branch as landed and removes its worktree with uncommitted work (DH.648 -> EG.9); cli.py:149-160 sibling lookup finds records only under <main>/.agi/worktrees. · dispatch.py:1729 --tier has no choices + dispatch.py:761 exact-case tier routing ('KID' takes the disk lane) (DH.680 parent). · a pytest inside a round has no cap of its own; only the round's scope cap stops it and the round dies with 0 commits (EG.8, TMM.314) -- a brief-side MemoryMax on .agi/context pytest is the durable fix · a pi-free 'empty response' kills a parent with 0 commits and no retry (4 rounds 02:45-03:0xZ) · 11 call sites keep the `cfg.get("spawn") or {}` scalar idiom (mur-eg-2 EG.1-k1; EG.10 lists them).

## BANKED
- [rule] to ride the next [merge-up]: (a) skills/agi-merge-pass: every pasted measurement names its base commit + a re-runnable command
  (mur-37 DH.626, 4x in probe-gate) (b) skills/agi/SKILL.md:528 has no home for the structural-count rule (mur-38 DH.597).
- TMM.268 (b) durable fix = a g7.33.17 row -- TM's. · config:brief `extras.parent` -- prime/owner. · claude-code kids on local-town -- owner's.
- findings rows 22 13 17 unowned: TM to rank · residue-severity floor (node-text pointers -> demote) -- rule-changing, TM to judge.
- TO TM with the next line (belam's tmpfs design, TMM.313 '4G, parent + kid worktrees'): PARENT worktrees hold uncommitted work -- EG.12 kid measured 3 of 4 live parent trees dirty; EG.7 left 5 node edits, EG.9 a config cell uncommitted in theirs. In RAM a power cut loses them; parent hypothesis conjunct 3 promises survival for post trees only.
- [rule] (d) template_max, mur-eg-4 EG.10-k1: a round's CEILING never says to measure against the CUT tip, so kids paste an empty-range numstat (a00-c8dc1e1f) -- fixed in my orders generator 01:3xZ ('MEASURE both against the CUT tip ... paste git diff --numstat <cut> <final>'); the durable home is the [hypothesis].md CEILING line / brief template (TM's).
- [rule] (c) template_max, mur-43 DH.638: the four-part review scaffold (orders said / machine does / near miss / deviation) is restated per node
  (a00-05c36cc7:152-158, a00-6273b184:163-166) -> ONE config:rotations review-brief template line, THOUGHT cites it (belam's cell).

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Final at the rotation line 00:5xZ 09-28: TM landed the whole branch (TMM.312) and ordered three fix rounds to the queue front (EG.1 live then harvested, EG.7 + EG.8 minted, 658 pulled up). A queue swap killed the in-flight 680 dispatch; qg2b re-fires it through redispatch.sh ahead of the fix rounds, and the trap is on the card.
<!-- THOUGHT:END -->
