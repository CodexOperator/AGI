---
id: doc:card-all-is-one
mint_id: f3ab702d3c454a6aab2d41c2e88533d2
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: all-is-one
scaffold_hash: 15b137cded6cbf1b
season: 2
title: Card all is one
town: core
---
# doc:card-all-is-one — all-is-one's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (02:5xZ 09-30 — council working; meter 0.34, rotate at 0.47)
| | |
|---|---|
| post | all-is-one |
| stage | council — embody vision:all-is-one ONLY ("everyone uses a unified set of tools ... same UI/UX by any role"); TOP-DOWN, generations, never the nitty gritty (doc:council-loop "The council's lens") |
| loop (doc:council-loop) | DG1 finalizes ONE outcome per goal · SM writes bigger_outcomes · council REVIEWS them -> new goals / bundles / nested goals, or none -> season OVERVIEW nodes |
| place | local-town · MAIN /data/work/agi (on the RAM disk since 01:41Z, same path) on local-maxxing/season2/main · claude-code Opus 5.5 high · CC session agi-8f / 242e8c (heal crash-resumed 02:0xZ) |
| messaging (owner, until bundles land) | "use internal messaging only for everything and full guarantee until bundles land": SendMessage by session name ONLY; NO send.py, NO rooms |
| peers (02:5xZ) | Prime belam = agi-c2 · alive = agi-b3 (convener) · self-perpetuating = agi-53 — names change: ListAgents + tmux @id -> post |
| skills | agi-node-write · agi-goal · agi-send · agi-rotate · agi-post |

## §1 Plan
```
done   bundles 1-3 converged + reviewed; bigger_outcome 1-3 ACCEPTED (v2 08fc9e701 names the home-path false green, residue 128)
done   placements: bundle 4 write/render split · g7.16.1.6 (tip = truth, per-file snapshot refusal) · .7 (7a/7b) · g7.32.6 re-shaped (Prime (a))
done   owner-task 1 (rewrite goals from OWNER lines): mine g7.32.6 586b72bdd + g4.18.5 5b40c0f49; alive .6 .5; s-p .7 .8; .9 -> .7.3 (alive)
done   owner-task 2 (retire S goals, OWNER 01:2xZ): mine s7 s35 s18 s32 -> report sent to alive (agi-b3):
         s7 RETIRED + leaf g4.18.6.6 (goal seeds derived, never stored twice) · s35 RENUMBERED -> g4.18.8 · s18 RETIRED (nothing open) · s32 RETIRED + leaf g2.4.1 (cache + vector storage)
         deviation: retired IN PLACE (skill agi-goal; 39 retired goals in goal/; no deprecated/goal/ dir)
done   lens to s-p: g4.18.5.4 keep under g4.18.5; widen to `retire` + `renumber` verbs for ANY node type (tonight's renumbers were git mv + hand identity edits)
done   03:0xZ all 12 S goals closed (alive adopted retire-in-place for all); residue placed: s32 hyps a00-12e9183c + a00-ec5ee032 re-homed -> g2.4.1 (9a0651a7c 234c4f73c); a00-c4b84f52 + s18 4 hyps -> DG2 (agi-7f, window @7) for closing verdicts
next   council checks PLACEMENT of belam's g7.16.1.5 leaves (owner priority: worktree + RAM cleanup) when they land · place horizon leaves g4.18.6.6 + g2.4.1 · review each SM bigger_outcome
never  OVERVIEW until .6, .7 and bundle 4 close (all 3 agreed)
```
Lens questions for every bundle: two paths for one act? · a role-only verb or flag? · a copy of a rule (one source)? · an overbuilt branch?

## 🔴 Where it stops
02:5xZ 09-30 idle after S-goal report; next = g7.16.1.5 leaf placement when belam lands them
```
on wake: ListAgents (names change) · read any SendMessage · git log --since='1 hour ago' --format='%h %an %s' -- '.agi/nodes/goal/g7.16.1.5*' .agi/nodes/bigger_outcome
placement check = read each new leaf by id (write.py goal:<id> 'read body 1:60') -> one lens line to alive + belam (SendMessage)
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| write.py auto-commits, BUT refuses under verify-suite.lock / a busy index.lock | it prints "commit refused": `git add -- <new file>` then `git commit -- <path>` |
| renumber a goal (no verb; `id` is protected) | write.py edits FIRST (H1, title, thought), THEN `git mv` + the 3 identity lines (id, parents, goal_id) as ONE commit, THEN re-point refs via write.py — a write on a half-renamed node commits the new file beside the staged old one (2 files, 1 mint_id) |
| `set title` in a write.py script | the value = the rest of the unit, NO quotes (quotes become part of the value) |
| ack after a crash | non-prime: `rotate.py ack --post all-is-one --session 5d1031fa --ref <ref> continue` (--gen refused); own row dirty from heal's clear -> commit that clear by path first |
| `grep -r` / `find` over .agi/ | io-stalls the box: `git grep PATTERN <sha> -- <paths>` |
| tests | `git archive <tip> extensions .agi/context/schemas` under /tmp, `--basetemp` /tmp; ONE file at a time while a PASS runs |
| write.py `sub` with `\n` | a literal `\n` in single quotes: build the arg with python3 -c print(...) |
| .agi/sessions/quorum/all-is-one.md | a STALE tracked regular file (09-18 brief), not this card — not mine to re-point |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken (02:5xZ: 5263 resolved, 0 broken)

## §6 BANKED
(none)
