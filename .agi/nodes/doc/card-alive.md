---
id: doc:card-alive
mint_id: 873c4980ef2340dfa4af5b298318f54c
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: alive
scaffold_hash: 0394875185875b1d
season: 2
title: Card alive
town: core
---
# doc:card-alive — alive's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (23:5xZ 09-29)
| | |
|---|---|
| post | alive gen 2 · session agi-13 (6c4fe6) · window @3 · rotating at meter ~0.42 (the next step starts hours out) |
| stage | council RESUMED 23:4xZ (owner via belam XVIII: "Restart council including DG5 stand up. Then let them tackle the bundle and see how best to streamline it further.") · I embody vision:alive ONLY: the system reporting its own true state |
| lens | doc:council-loop "The council's lens" (owner 23:3xZ): top-down, big picture over 1000s of generations, never the nitty gritty (directors') · "## The loop" (owner 23:5xZ, fbff64dc1, SUPERSEDES): DG1 finalizes ONE OUTCOME per goal · SM writes the BIGGER_OUTCOMEs · the COUNCIL reviews bigger outcomes -> new goals / bundles / nested goals at any level -> none remain: write the season OVERVIEW nodes, hand them to belam · full steam to ~04:00Z 09-30 |
| peers | self-perpetuating agi-ff · all-is-one agi-86 · DG1 agi-77 · DG2 agi-40 · DG3 agi-c5 @10 · DG4 agi-47 @12 · DG5 agi-c8 @14 · SM agi-b8 (rotated gen 7 at 23:4xZ: check ListAgents) · Prime belam-S2-L5-XVIII agi-9c @11 · room `directors` = DG1-DG5 split their own work |
| skills | agi-goal · agi-node-write · agi-send · agi-workflow · agi-rotate · agi-post |

## §1 Plan
```
done   bundle 3 CLOSED 1f39ffb1c · outcome:g7-16-1-3-bundle-3-closed (the FIRST goal-chain outcome) · goal:g7.16.1.3 complete
done   placed goal:g7.16.1.6 = WRITE line after bundle 4 (one truth = ref tip, one branch writer, moved-set, per-file refusing
       snapshot with one OPEN finding per file) + goal:g7.16.1.7 = SPAWN line NOW (7a DG5: one stand-up verb, heal keys, one pi
       template · 7b after .6 + W2: link rows, walk, swap; guards; cold-start falsifier) -- 3 lenses converged, 9032a157f
done   the Prime's (a) ruling c67f80708: [outcome].md allows `goal` as parent; judged_against = that goal or omitted
now    outcomes are DG1's now (new loop; .3's council outcome exists: DG1 adopts it, never a second); row F .9 MOVED UNBUILT to g7.16.1.7; bundle 4 building (DG3 W1 first: nested row verb)
next   on SM's BIGGER_OUTCOME handoff: review it through vision:alive -> new goals / bundles / nested goals, or none left -> OVERVIEW nodes to belam
```
Council mur route: args like /tmp/alive/cmur/b3-chunk{1,2}.json (one round per row pair, COMMON focus + a SIMPLIFY pass,
old_tip = bundle base, new_tip = SM's clean tip; a distinct merge_up per chunk = a distinct run key) ->
`PI_BIN=$HOME/.npm-global/bin/pi python3 extensions/agi/bin/workflow.py run agi-merge-up-review --harness pi-free --args ...`
(skill agi-workflow: NEVER the Claude Workflow tool) -> read .agi/sessions/workflows/runs/<run-key>/verify_<label>.json
(verdicts + "missed"), never stdout. ~12 min per stage on the free model; run both chunks in PARALLEL.

## §2 Landed (this generation, 17:34Z-23:5xZ)
- bundle 3 placement + close: 1559f7ae5 · aaf9f3286 · eef097d03 · outcome + complete 23:5xZ · bundle 4 minted + base + inputs
- goal:g4.18.7 6804f5c00 · g4.18.6 mint rule d2d57a4bf · .6/.7 placements 9032a157f · DG4 L2 rulings 0670c8612 841857ddb
- my own corrections, named in the room: guessed stamps 32d6053b3 · teacher count a5848c5a2 · "no live path" (the hook) ·
  "write.py commits every write" (not under the suite lock) · "preserve edited_by" withdrawn (edited_by = last editor)

## 🔴 Where it stops
alive gen 2 rotates at 0.42: bundle 4 is building; the council waits on SM's clean handoff
```
on SM's BIGGER_OUTCOME for a bundle: read it + its outcomes (render path) -> vision:alive lens: does the system now report its own true state? -> new goal / bundle / nested goal (agi-goal) or none -> OVERVIEW -> SendMessage agi-ff + agi-86
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset; filter a dirty posts.md to YOUR hunk (git apply --cached) |
| write.py commits each write itself, EXCEPT while .agi/sessions/verify-suite.lock is held | it prints "commit refused" and the write lands uncommitted: wait for the lock, THEN commit by exact path; never commit MAIN under the lock |
| my timestamps were guessed TWICE | `date -u` before writing ANY time; git log --date=format-local for a past one |
| `send.py read` shows only new blocks; a [red] sat in the inbox FILE alone | after any wake, tail the inbox file too |
| `send.py status belam` marker stuck after an inbox send | SendMessage the Prime directly as well |
| `sub` has no newline: `\n` lands LITERALLY | build a multi-line change in python and `replace body` the WHOLE paragraph or section |
| `thought` rewrites the THOUGHT whole | read the old one first; carry owner verbatim forward word for word |
| a relay says "the owner said X" | verify on the bytes (a node section, a signed inbox block) before spending; a STOP needs no proof |
| the captive capture chain tried rotate-self at 0.4035 and FAILED rc=1 (23:4xZ) | rotate yourself (agi-rotate §2); read the ladder's capture_chain_log if it repeats |
| grep -r / find over .agi/ or the repo root stalls the box | `git grep PATTERN -- <paths>` |
| .agi/sessions/quorum/alive.md | a SYMLINK to this node (re-link at wake if rotate flattens it: agi-rotate §3) |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken (5169 at 23:5xZ) · GOALS.md is RETIRED: read goals by id

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| row R live cutover (restart drops every post) | the Prime gen 17: dummy proof GO; live step = owner's word after PASS B3 (doc:card-belam §6) | step 1 at the cutover commit: `env AGI_LIVE_SYSTEMD=1 python3 -m pytest extensions/agi/tests/test_rotate.py -k test_r1_cutover_dummy_one_kill_is_one_post -q`; no pass line = (a) restart, never (c); form = GROUPED Delegate=yes scopes (R1 v3 b2d946498) |

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Whole rewrite at rotation (23:5xZ 09-29, meter ~0.42): the owner's 23:5xZ loop (doc:council-loop "## The loop") changed the council's job from writing goal-chain outcomes to reviewing SM's BIGGER_OUTCOMEs and, at the end, writing the season OVERVIEW nodes; this version hands that job over whole, with the placements and the one council outcome already minted, the mur route as actually run, and the traps paid for this generation (including my own four corrections).
<!-- THOUGHT:END -->
