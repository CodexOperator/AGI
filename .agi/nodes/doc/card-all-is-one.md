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

## §0 State (15:4xZ 09-29 — STOPPED at the owner's 16:00Z line)
| | |
|---|---|
| post | all-is-one |
| stage | council — you embody vision:all-is-one ONLY (read it whole first); every review speaks from that vision alone, never alive or self-perpetuating |
| protocol | doc:council-loop (read it first) · goal:g7.16.1 (the owner's words) |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high · CC session agi-96 this run |
| peers (this run) | alive agi-8b (convener) · self-perpetuating agi-20 · DG1 agi-f8 · DG2 agi-63 · DG3 agi-8f · SM agi-4f — session names change per run: ListAgents first |
| skills | agi-node-write · agi-send · agi-workflow · agi-rotate · agi-post |

## §1 Plan
```
done   bundle 1 = goal:g7.16.1.1: drafted, converged (B E {C D} A), SM clean at 80c1c245d, council mur 2 chunks + 3 lens reviews
done   bundle 2 = goal:g7.16.1.2 (794a0782e): converged, SM clean at 9c54fb3c4 (re-mur wf_42a582dc-d1f accept, residues 32-56 closed)
next   FIRST ACT next run: council review of bundle 2, range 794a0782e..9c54fb3c4 (430 files) — alive runs the batched mur by row, I send ONE all-is-one lens review
then   bundle 3 = grok core/season2/main simplify (order of work item 2); season-2 close only when nothing is left to simplify
```
Lens questions for every bundle: two paths for one act? · a role-only verb or flag? · a copy of a rule (one source)? · an overbuilt branch?

## §2 Landed (this run)
- bundle-1 draft reply: keep A-E; A narrowed (template = the existing kind, switch = one write.py set); D = count mint assigners; retire → park g7.32.5
- conceded B first + park over retire (s-p); schema fix: park = status horizon (`held` is illegal, [goal].md:33)
- bundle-1 lens review: BETTER — 9 copies → 2 single sources (THOUGHT regex 5→1, mint assigner 4→1); change: switch only listed wakes · marker literal x2 · check_formation's own rglob
- park-as-TAG (existing `tags`, `parked:g<N>`) over a new field — alive + s-p adopted; migration gate recounted (16 real parks, minus 2 live-code)
- chunk-1 residues: rotation records fixed at the WRITER, no anonymize exemption; conceded the 109-JSON scrub to one `~` shape; s-p added one transcript resolver

## 🔴 Where it stops
15:4xZ 09-29 idle at the owner's stop; bundle 2 is SM-clean and awaits the council review
```
next run: ListAgents · send.py --from all-is-one read all-is-one · git diff --stat 794a0782e 9c54fb3c4 · wait for alive's mur chunks, then SendMessage alive ONE lens review (keep / change / next-bundle, bytes cited)
```
Pre-read at the tip 9c54fb3c4 (15:3xZ, for that review):
| row | reading |
|---|---|
| M | HOLDS: THOUGHT_BEGIN/END live only in node_writer.py:985/987 (0 literals in snapshot-goals / write) |
| T | HOLDS (alive): one home .geometry/formations/, 3 templates each mapped to a goal, 1/3/4 retired; one `templates:` registry in config:formations |
| R1 | HOLDS (alive): one resolve_transcript, rotate.py:445 |
| CLASSES pointer | RESIDUE: skills/agi-master-gate/SKILL.md:66 still hand-lists "hostname / ip / mac / board / secret" — missing `home`, and still a copy |
| F | NOT landed: no formation line in config:rotations first_turn (Prime-written, owed) |

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN <sha> -- <paths>` |
| `send.py read all-is-one` without `--from` | exits 2 (whoami = unknown): always `send.py --from all-is-one ...` |
| town:local-maxxing board | ring-gated (owner/prime only): the measure line goes to room council-loop as [measure] |
| tests | run touched files from a `git archive <tip> extensions` copy under /tmp, `--basetemp` under /tmp; check `.agi/sessions/verify-suite.lock` first |
| .agi/sessions/quorum/all-is-one.md | a STALE tracked regular file (09-18), not a link to this node — do not read it as the card; not mine to re-point |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken · `snapshot-goals.py --render --check`

## §6 BANKED
(none)
