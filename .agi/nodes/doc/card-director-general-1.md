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

## §0 State (10-07 ~16:25Z, ROTATING at the line 474185/1000000; gen 10 wakes next)
| | |
|---|---|
| post | director-general-1: a director, claude-code, a v5 unit (engine.v 4) · parent SM · trunk local-maxxing/season2/main · my t = posts/director-general-1 |
| rotate | the meter hook prints the line: write this card, `git commit` it, then `touch ~/.fresh;kill $PPID` |
| mail | `python3 extensions/agi/bin/send.py --from director-general-1 send POST "$(cat FILE)"` ONLY, run FROM /var/lib/agi/director-general-1/t; bodies in a FILE (a shell string with $( expands: DG2 and DG3 both garbled one). Read: `... read director-general-1`, then ALSO grep the inbox FILE /data/work/agi/.agi/sessions/inbox/director-general-1.md (`read` can show empty). To belam tags decision, merge-up, rotation, red, rule, owner; ONE [rule] line back |
| roles | DG1 = goals + nodes + merge-ups + JUDGING every return by RUNNING it at the sha (then a mutant or sibling probe); DG2 = falsifiers (test-only, ONE file + sha, written FIRST, RED on the trunk); DG3 = builds; SM gates + lands (Sonnet mur, FULL suite); alive = council lead (designs); belam (rotating, next belam wakes) = Prime |
| scratch | worktrees: `git -C /data/work/agi worktree add --detach SCRATCHPAD/x SHA`, remove after; a branch: `git -C /data/work/agi branch N BASE` then `worktree add PATH N` |

## §1 Plan
```
OWNER 10-07 14:4xZ (via belam): old Python kept this season (provisioning.py, metrics.py, success_metrics.py, verification.py, commands.py run verify), shell rewrites = season 3, metrics back on,
messaging needs a council pass; goal g7.16.1.11.17 (belam on v5) RESTATED. COUNCIL (alive) PLACED it 14:54Z; I WROTE the goals (landed): .17 restated (horizon), .19 verify, .20 messaging, g3.8 metrics, g4.13.1 grid CAS.
ENGINE QUEUE = NEXT SEASON, not built: pq (DG2 lanes c6176d986 stay unbuilt), revoke(+LC_ALL=C), flowrot, round B mail, sealer box side. THIS season only: agi-signers retires = the ring-install step (belam GO).
LANDED (local trunk, pushed): CKPT.3 70530c33c, OUT.7 666098f19, OUT.8 3fb54c655 (PATH-aware skip; ceilings 828), goals through 8bc80981d2.
WITH SM, one gate at a time (sent 16:1xZ): (1) g4.13.1 corrective #2 dg3-gridcas f8e756801b (DG2 lanes 6831d75f7, 52); (2) g7.16.1.11.19 verify as a v5 uid dg3-verify5 23a6591f72 (DG2 520c9c722, 25).
JUST ARRIVED, NOT RUN BY ME: g3.8 dg3-gmetrics 989d77684a (one commit on trunk b828e57bf4: metrics.py, success_metrics.py, crons.md + graph-metrics.t.sh == DG2 d9510cbed, 25 lanes; DG3 reports 25/0, 15 mutants RED, the real line 634 B in 65.6 s).
IN FLIGHT: g7.16.1.11.20 messaging: DG2 writes lanes (brief sent 16:1xZ; he must find agi-run box-n poll + cccc.ts on et-grok-pilot, ask alive). Goal ACTIVE on dg1-goals-1007d 83d745b9a6 (node-only, +.19 bounds note, NOT yet sent: bundle in the next [merge-up]).
A12 stays ROLLED BACK (belam's install GO); preconditions: bin/agi-out in every v5 t, host sh = dash check, EnvironmentFile root-owned.
```

## 🔴 Where it stops + the exact next command
FIRST: `cd /var/lib/agi/director-general-1/t && python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1` (copy what you need, then grep the inbox FILE after the last ts you saw: 16:20:34Z DG3 g3.8 correction). THEN, in order:
1. RUN g3.8 989d77684a (not run by me): scratch worktree at the sha; `git diff --stat b828e57bf4 989d77684a` = metrics.py, success_metrics.py, crons.md, graph-metrics.t.sh; `sh extensions/agi/tests/graph-metrics.t.sh` 25/0 (trunk 17 RED); `python3 extensions/agi/bin/metrics.py /tmp/emptydir` rc 2 + 0 METRIC lines; `success_metrics.py --line <root>` ONE line (~65 s); the crons.md cmd = `L=$(python3 {repo_root}/extensions/agi/bin/success_metrics.py --line {root}) && python3 {repo_root}/extensions/agi/bin/write.py town:local-maxxing "set graph_metrics $L" --actor belam`; mutants of the new code; then ONE [merge-up] to SM with my numbers. The job goes live only when belam's grid_sync applies crons (box local-town).
2. SM [landed]/[return] on corrective #2 + verify: a [return] = NEW commits by DG3 on their branches, DG2 lanes first, I run, forward.
3. DG2's .20 lanes sha: run RED on the trunk (shell, v5 uid), then DG3 builds, then me, then SM. alive's wake-after-read lane is in the goal falsifier.
4. Bundle dg1-goals-1007d into the next SM [merge-up]. Then: agi-signers retire = belam's ring-install GO (not mine to build). Never invent goals.



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
