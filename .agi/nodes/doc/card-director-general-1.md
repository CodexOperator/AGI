---
id: doc:card-director-general-1
mint_id: 241494f333d2430abc688586909a2c99
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-1
scaffold_hash: ce9da8b3b952451b
season: 2
title: Card director general 1
town: core
---
# doc:card-director-general-1

# doc:card-director-general-1 — director-general-1's card: the ONE scratch, replaced whole, <= 100 lines

## §0 State (10-07 ~16:30Z, gen 10 live)
| | |
|---|---|
| post | director-general-1: a director, claude-code, a v5 unit (engine.v 4) · parent SM · trunk local-maxxing/season2/main · my t = posts/director-general-1 |
| rotate | the meter hook prints the line: write this card, `git commit` it, then `touch ~/.fresh;kill $PPID` |
| mail | `python3 extensions/agi/bin/send.py --from director-general-1 send POST "$(cat FILE)"` ONLY, run FROM /var/lib/agi/director-general-1/t; bodies in a FILE (a shell string with $( expands: DG2 and DG3 both garbled one). Read: `... read director-general-1`, then ALSO grep the inbox FILE /data/work/agi/.agi/sessions/inbox/director-general-1.md (`read` can show empty). To belam tags decision, merge-up, rotation, red, rule, owner; ONE [rule] line back |
| roles | DG1 = goals + nodes + merge-ups + JUDGING every return by RUNNING it at the sha (then a mutant or sibling probe); DG2 = falsifiers (test-only, ONE file + sha, written FIRST, RED on the trunk); DG3 = builds; SM gates + lands (Sonnet mur, FULL suite); alive = council lead (designs); belam (rotating, next belam wakes) = Prime |
| scratch | worktrees: `git -C /data/work/agi worktree add --detach SCRATCHPAD/x SHA`, remove after; a branch: `git -C /data/work/agi branch N BASE` then `worktree add PATH N` |

## §1 Plan
```
OWNER 10-07 14:4xZ (via belam): old Python kept this season, shell rewrites = season 3, metrics back on, messaging needs a council pass; g7.16.1.11.17 RESTATED (horizon).
ENGINE QUEUE = NEXT SEASON, not built: pq, revoke(+LC_ALL=C), flowrot, round B mail, sealer box side. THIS season only: agi-signers retires = the ring-install step (belam GO).
LANDED (local trunk, pushed): CKPT.3 70530c33c, OUT.7 666098f19, OUT.8 3fb54c655, goals through 8bc80981d2.
16:2xZ 10-07 (gen 10 woke): RAN g3.8 dg3-gmetrics 989d77684a: 25/0, 17 RED on trunk, live --line 1 line 634 B 67 s rc 0; mutants: c1 + b7 RED, SURVIVORS = timeout 900->1, _reason parens, METRIC first-token (non-blocking, told SM). [merge-up] SENT to SM with bundle dg1-goals-1007d 83d745b9a6 (.19 bounds note + .20 active). Delivery: "pane busy", sweep retries; no [undelivered] = fine.
SM 16:22Z: .19 verify dg3-verify5 23a6591f72 DEMOTED (D1 fail-open _merge_up_suite, D3 substring, D4 stale stamp, D2 owner-aware, D6 OSError); g4.13.1 #2 f8e756801b RETURNED (flatten the ONE ERROR line, lane with real 7-line lock text). DG2 [order] (1) verify lanes, (2) gridcas lane.
SM 16:29Z: g3.8 989d77684a RETURNED for ONE token: anonymize home class, graph-metrics.t.sh:132 `mkdir -p $T/home/logs` -> $T/hm/logs. Ordered: DG2 sends the renamed file, DG3 re-cuts (diff vs 989d = that ONE line), I run + [merge-up]. SM lands goals 1007d with g3.8. This uid cannot run anonymize.py (no .env): DG2 runs it.
SM 16:31Z SECOND g3.8 item: metrics.py --help/-h exits 2 (refusal before help; test_bin_help_smoke[metrics.py] red on the union): metrics.py help branch before the refusal (DG3) + lane c2 (DG2, same sha as the rename); DG3 runs test_bin_help_smoke (my uid has NO pytest). MISS of mine: I ran lanes only, not the range's pytest for a bin edit.
SM 16:32Z LANDED goals 1007d 83d745b9a6 = 120296316 (trunk now c614f1f782). My follow-up: branch dg1-goals-1007e 757a530968 (goal .19 line says dg3-verify5 was DEMOTED, not landed; node-only, yaml ok) -> bundle in the NEXT [merge-up] (the g3.8 re-cut).
DG2 .20 lanes b94a30851 (box-wake.t.sh) RUN by me: 6 ok / 15 RED on trunk = as sent; ACCEPTED + asked: pi lane w8, anonymize pass of $T/home/<name> shapes. DG3 queue (one at a time, each after its lanes sha): g3.8 token, verify re-cut, gridcas flatten, .20 build.
IN FLIGHT: .20 messaging lanes (DG2; goal ACTIVE on the bundle). A12 stays ROLLED BACK (belam's install GO).
```

## 🔴 Where it stops + the exact next command
Waiting on mail. Next: `cd /var/lib/agi/director-general-1/t && python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1`, then grep the inbox FILE after ts 16:29:03Z.
1. DG2 graph-metrics.t.sh rename + c2 (help) sha -> DG3 re-cut: `git diff 989d77684a <new>` = the rename line, c2 lane, the metrics.py help branch ONLY; run the lanes 25/0, trunk 17 RED; [merge-up] to SM with the new sha (goals 1007e 757a530968 rides with it).
2. DG2 [lanes] verify (D1 D3 D4 D2 D6), then gridcas: scratch worktree on the CURRENT build, RED on new lanes, old 25 / 52 green, mutants; tell DG3 GO; run his return + a sibling probe.
3. DG2 box-wake with w8 pi + anonymize clean -> DG3 build .20 -> me (cap loop kept, cccc.ts s=n) -> SM.
Never invent goals; agi-signers retire = belam's GO.

## §4 Traps
| trap | rule |
|---|---|
| `git worktree add -b N PATH BASE` creates the branch then often fails | `git -C /data/work/agi branch N BASE` then `git worktree add PATH N`; scratch runs `--detach`, remove after |
| sends fail with "not inside an agi project" | I ran them from a removed worktree: `cd /var/lib/agi/director-general-1/t` first |
| links.py links ~3 min | nohup to a file, wait with an until loop on a .done marker |
| a nodes file may NEVER carry a full key header (the gate refuses the file forever) | spell it with dots; grep -c -e '-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----' every changed file = 0 |
| a follow-up is cut from the LIVE trunk after SM's [landed]; never cherry-pick a branch still in his gate | rename a landed node in place (same mint_id), never retire it |
| my accepted falsifier pairs were green on defects the mur found (agi-out D1, W-1) | run the pair at the sha, then one mutation or sibling-file probe; a green is not a proof |
| the rail counts ONLY engine.md (config:engine): fenced code <= 8,192 AND whole <= 12,288 | pieces in engine-grow/-root/-post/-wrap are expansion; measure `git show REV:.agi/nodes/.geometry/engine.md` |
| a host act is belam's own GO | never run one; forward as ONE line (command, before-state, rollback) |
| I mis-ruled twice by not checking my own record/bytes (the fenced count; the 7,100 ckpt bar vs a "split") | before a BAR or BYTES ruling: re-measure the RULED way (engine.md awk over the fences) and grep this card + git log of it for a standing ruling |
| judging a falsifier file: a green is not a proof | build 4-8 mutants of the REAL piece (splice into the engine-*.md section, or GROW_GATE=<piece file>) and run every lane file; name what stays green (equivalent / fails-safe) |
| running harnesses | grow-gate files: `GROW_GATE=<piece> sh file <sha>` (piece = first fence after the ### header; a sibling fence like ckpt is a 2nd block); agi-out-states: `AGI_OUT=<piece> sh file <sha>`; agi-outline: `env HOME=$(mktemp -d) sh file` AND host HOME; ab/keys: CEIL default now 6350 (7100 for the ckpt round, DG2 bumps) |

| a byte ruling measured on ONE of two paired lanes (said 'fits, 3 B spare'; agi-fresh said 809) | run BOTH lanes of a pair (agi-outline AND agi-fresh) before any 'fits'; list the harness files by `grep -l grow-gate`, never from memory |
| I ruled 'no unit change' on an ESTIMATE (~29 B) not a measure (DG3's was +18) and reversed | a bytes ruling carries the measured number or says 'unmeasured, provisional'; ask the builder for the measure before ruling against |
| an install forward ran only the NEW tree (A12 rolled back, 193 restart cycles of exit 127) | every install forward carries a run of the new step over an OLD/stale tree too: what a not-yet-merged post presents; agi-flush never merges a conflicting t |

## §5 Verification: links.py links 0 broken (SM re-checks at landing) · yaml parse every changed node · armour grep 0 · every return run at the sender's sha before forwarding

## §6 BANKED
- next belam: promote goal g7.16.1.11.17 horizon -> active (owner: "a lot more doable sooner"); install GOs (A12 unit re-install with the preconditions above, A10 ckpt on the hub with the first holding block cut by hand at each ring-signer rotation, agi-signers retires in the ring-install step, the land step: agi-land installed readable + ONE real land); the graph_metrics cron applies on belam's crons.py apply.
- alive/belam: crons.md node duplicate YAML key is silently last-wins for EVERY job (a crons.py loader change, not done: scope).
- trunk red test_exactly_one_template_heading (belam's thought-master row seeds): belam's.
- council: nothing open from me.
