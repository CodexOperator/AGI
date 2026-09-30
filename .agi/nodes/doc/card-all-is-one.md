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

## §0 State (05:3xZ 09-30 — council RESUMED to 11:00Z; meter 0.41+: small steps only, rotate at 0.47)
| | |
|---|---|
| post | all-is-one |
| stage | council — embody vision:all-is-one ONLY ("everyone uses a unified set of tools ... same UI/UX by any role"); TOP-DOWN, generations, never the nitty gritty (doc:council-loop "The council's lens") |
| role (owner 02:5xZ 09-30) | "directors should reach out to council for rulings who discuss it among themselves using the lenses to keep you free. Remember the council IS prime to everyone else." alive convenes: ONE lens line to alive; alive sends ONE ruling; silence = agree |
| run (owner 04:5xZ) | "Continue hammering at it as fast as you can until 7am" = 11:00Z · subagents + reviews on Sonnet 5.5 (Opus allowed ~05:0x-06:0xZ: "I need to max sub use before reset in an hour" + "No make it opus as well") · workflow.py stays pi-free |
| place | local-town · MAIN /data/work/agi (RAM disk, same path) on local-maxxing/season2/main · claude-code Opus 5.5 high · CC session agi-8f / 242e8c |
| messaging (owner, until bundles land) | SendMessage by session name ONLY; NO send.py, NO rooms |
| peers (05:3xZ) | Prime belam agi-79 · alive gen 4 agi-e3 · self-perpetuating agi-53 · SM (rotating; successor TBD) · DG1 agi-2a · DG2 agi-7f · DG3 agi-91 · DG4 agi-80 · DG5 agi-5b · DG6 agi-bb |
| skills | agi-node-write · agi-goal · agi-send · agi-rotate · agi-post |

## §1 Plan
```
done   season so far: bundles 1-3 reviewed · goals rewritten from OWNER lines (mine g7.32.6, g4.18.5) · 12 S goals closed (mine s7 s35->g4.18.8 s18 s32; leaves g4.18.6.6, g2.4.1)
done   rulings: DG5 keys (C) own-box remint, box = AGI_BOX, rule = key_template row · DG3 replace payload NOT extended · DG1 body refs -> g4.18.6.4 · DG3 residue 154 fail closed
done   g7.16.1.5 placement check -> belam (via alive): A .5.5.3 restates .5.5 · B two session-dir movers (.5.2 timer vs .5.3.2 heal) -> one mover
done   s-p g7.16.1.10 (merge-up reviews off the Prime): review identity = git patch-id + touched-file base blobs, tip sha recorded not keyed
done   goal:g1.31 (PASS B3 residues): SM agreed DG6 first assignment; 47 upheld triaged INTO g1.31 Target LANES (19b56ec70): DG3 3 · DG5 8 · DG6 19 · NODE 17; DG3 + DG5 told
done   05:4xZ DG6 SEATED as agi-bb, already on g1.31 (owed brief moot) · LANES fixed 3a76b6eb4 (#22 #25 CLOSED, DG6 17, NODE 19) · DG3 took #12 #24 #37 · ruling to DG6 g1.31.4.2.2: meter fallback + unmeasured tag AGREED (fallback = the same ladder cell; ONE open finding per unmeasured model)
was-owed DG6 brief: "first assignment goal:g1.31 -- read its LANES block by id; 47 upheld first, then the 147 missed rows; Sonnet 5.5 subagents"
done   05:5xZ bundle-4 lens to alive: (4a) write.py rc 0 on an uncommitted write under the suite lock -> exit 3, leaf under g4.18.5, a STOPGAP deleted at the .6 cutover · (4b) suite reads a tip snapshot -> NEST under g7.16.1.6, so the verify-suite lock RETIRES · one config block for the lock policy meanwhile\nopen   horizon leaves g4.18.6.6 + g2.4.1 wait for their lines · no OVERVIEW until .6, .7 and bundle 4 close
```
Lens questions for every ask: two paths for one act? · a role-only verb or flag? · a copy of a rule (one source)? · an overbuilt branch?

## 🔴 Where it stops
05:3xZ 09-30 g1.31 triaged into lanes; DG6 brief owed at its seating; council rulings continue
```
on wake: ListAgents (names change; DG6 seated? -> SendMessage it the owed brief above) · answer any director ask with ONE lens line to alive (agi-e3)
check: git log --since='1 hour ago' --format='%h %an %s' -- .agi/nodes/goal/g1.31.md '.agi/nodes/goal/g7.16.1.5*' .agi/nodes/bigger_outcome
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| write.py auto-commit refused (verify-suite.lock / busy index.lock) | `git add -- <new>`; `git commit -- <paths>` in a retry loop; NEVER remove a lock |
| a verdict NODE minted ≠ the hypothesis closed | the hypothesis's own `verdict` field must be set too (alive fixed 5 at 172902cd7) |
| `git grep -h ... | grep -v <path>` | -h drops paths: the filter does nothing (my s18 error) |
| `replace body N:N` on a `## ` heading line | refused (splits heading from text): insert at the blank line ENDING the previous section |
| renumber a goal (no verb; `id` protected) | write.py edits FIRST, THEN `git mv` + id/parents/goal_id as ONE commit, THEN re-point refs |
| `set title` in a write.py script | value = rest of the unit, NO quotes |
| ack after a crash | non-prime: `rotate.py ack --post all-is-one --session <sid8> --ref <ref> continue` |
| `grep -r` / `find` over .agi/ | io-stalls the box: `git grep PATTERN <sha> -- <paths>` |
| SendMessage short names COLLIDE (05:5xZ: agi-e3 = alive [761106] + DG2 [78fffb]; agi-8c = DG1 + stream-master; agi-c8 = DG4 + DG5) | address as "name [ref]" from ListAgents |
| .agi/sessions/quorum/all-is-one.md | a STALE tracked regular file (09-18 brief), not this card |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken (03:0xZ: 5270 resolved, 0 broken)

## §6 BANKED
(none)
