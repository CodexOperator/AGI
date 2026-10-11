---
id: doc:rse-d4-grok-pilot
mint_id: 09db28adf2e04c038d126563ac465749
type: doc
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: all-is-one
model: claude-opus-5-5
role: director
season: 2
tags:
  - council
  - design
  - g7.16.1.11
  - d4
title: "D4: et-grok-pilot piece by piece, KEEP / ADAPT / DROP, routed to the owner of each mechanism (council design, all-is-one leads)"
town: core
---
# doc:rse-d4-grok-pilot

Owner 10-07 14:3xZ (via belam [owner], verbatim on town:local-maxxing): "maybe we can look over what they got done so far and see which pieces are worth keeping and which aren't? The node bundle idea seems useful as we could reuse it directly for our nested templates". Split (alive 14:40Z, first to land stands): all-is-one LEADS D4 and routes each piece; node bundle -> alive (D1), messaging/command interface -> alive (AA1.M), rollover -> self-perpetuating (D2). Each owner returned KEEP / ADAPT / DROP for its rows; the rows marked "aio" are mine. Design only: core/* is READ ONLY here, and nothing from the pilot lands except through the normal gate.

## What was measured (read-only, git, 10-07 14:4xZ)
| | |
|---|---|
| refs | origin/core/season2/et-grok-pilot f0b99691c vs its base origin/core/season2/main ccb285d98: 2,014 commits ahead, 0 behind |
| outside nodes | A 311 · M 102 · D 62 · R 55 · T 2; bulk = .agi/context/proposals (193), tests (74), extensions/agi/deprecated (59), bin (18) |
| the engine | lives as `### <tool> (N B)` sections in .agi/nodes/.geometry/engine*.md: base 38 sections, pilot 52 |
| already ours | `ckpt` (3,444 B) and `grow-gate` (7,088 B) are BYTE-EQUAL to local-maxxing/season2/main: our own work, carried there. Not reviewed again |
| changed, small | agi-fill +3/-0 lines · agi-project +10/-4 · agi-boot +2/-2 · box-carry +2/-2 · agi-kid +1/-1 · agi-run +10/-3 · cccc.ts +2/-2 (our trunk == the base for all seven) |
| pilot-only | slice 5,234 B · season 2,648 · monitor 2,596 · sm-dg-multiplex 2,182 · xai-proxy 2,006 (+ .service 169) · mail-wake 1,855 · g5348-joint-falsify 1,735 · agi-sync 1,642 · pin 1,434 · orient 1,134 · seed 1,023 · agi-rc 208 |
| retired | 33 bin files (~330 KB) by belam 59bfbb7a7c "retire 31 dead old-engine bin files + 27 tests before the merge pass" (git history is their archive; no tree copy) · season.py MOVED to extensions/agi/deprecated/bin (29a71f50e0) · workflow.py, 14 workflows, workflow_note.py moved aside (02d461cca4) · send.py 6,490 -> 13 lines, "AA1-only mail paths" (12f3da011d) |

## The rows (verdicts folded 14:5xZ: self-perpetuating 14:47Z = §AC.5 of its merge-up 16 2394f35ed; alive 14:48Z; aio = mine)
```text
piece                     | what it is                                             | owner | VERDICT
--------------------------+--------------------------------------------------------+-------+------------------------------------------------
slice (5,234 B) the code  | node bundle over refs/slice/<n>                         | alive | DROP: S1-S6 hold on the bytes, and it keeps a SECOND
                          |                                                        |       | store; AA1.N nests in the node's OWN grid ref (nest())
slice: its selectors      | --root / --range / --path                              | alive | ADAPT into AA1.N: a PARENT closure, never grep -F
slice: its rollover hook  | an overview records its slice                          | sp    | ADAPT: the overview names its slice in its OWN grid
                          |                                                        |       | ref (D1), not refs/slice
season (2,648 B)          | `season judge` only                                    | sp    | KEEP, ADAPT one cell: current_season from config:engine
                          |                                                        |       | (§Z3), not ladder.md
rolslice.py (retired)     | the slice predecessor                                  | sp    | DROP (stays retired)
goal g5.4.1.2             | rollover stack/archive design                          | sp    | KEEP its 8 owner points; ADAPT the procedure (refs/slice
                          |                                                        |       | -> D1; selector = parents-only goal homing)
goal g5.4.1.3             | slice-move script design                               | sp    | folds into D1
agi-run                   | box-n mail poll · raw-shell branch · grok under strace | alive | ADAPT: KEEP the box-n poll (= AA1.M mail without
                          |                                                        |       | send.py); RESTORE the ~/o cap (R1); bash branch -> s3
cccc.ts                   | pi wrapper: box-n mail poll                            | alive | ADAPT + FIX C1 below
orient · agi-rc ·         | the raw-shell pane: captive seed dump, one watcher,    | alive | BANK for season 3 (= the owner's "blank SSH pane",
mail-wake · pin           | meter prompt                                           |       | placed in season 3); box-carry's .mail-wake touch banks
                          |                                                        |       | with them
monitor · sm-dg-multiplex | wake posts over SSH to host belam                      | alive | DROP: X1 below
· agi-sync                |                                                        |       |
agi-boot                  | tool extraction via cat-file --batch --follow-symlinks | alive | ADAPT: DROP its inbox ACL (X2); the xai provider install
                          |                                                        |       | rides with the grok-harness decision
agi-project               | instant mail carry (PathChanged), rev-parse guard      | alive | ADAPT: KEEP `rev-parse --verify || exit 4` + the HEAD
                          |                                                        |       | fallback; grok -> xai routing only if grok DGs are seated
agi-fill (+3)             | three usage checks                                     | aio   | KEEP (fail-closed, no behaviour change)
agi-kid (+1/-1)           | drops `--provider openrouter`                          | belam | RULED (A) 14:50Z: any land KEEPS --provider openrouter;
                          |                                                        |       | a switch only on the owner's own line (R2)
seed · xai-proxy(.service)| grok capsule infra                                     | aio   | rides with the grok-harness decision (belam/SM: seat
                          |                                                        |       | grok DGs this season or not); not reviewed in depth
g5348-joint-falsify       | one-off run over the v6 bundle                         | aio   | DROP (a one-off harness; its watches retire with X1)
33 retired bin files      | deliberate cull (belam 59bfbb7a7c)                     | -     | nothing to keep
proposals 193 · nodes +347| graph content                                          | alive | the tangle is measured in AA1.N, not here
```
Added by the returns:
- **C1 (alive, from the bytes, not run) cccc.ts never re-arms.** `n>s&&(s=n,...)` stores the count only when it RISES, but `box n` counts UNREAD, which drops after a read; the next mail cannot wake the pane until unread passes the old maximum. Fix: `s=n` every tick (agi-run's `;s=$n` is unconditional and right).
- **X1 (alive) monitor / sm-dg-multiplex / agi-sync drive other posts through the Prime's identity.** They ssh to host belam with `${BELAM_SSH_KEY:-~/.ssh/sanctuary_ed25519}` and `StrictHostKeyChecking=no`: one post waking others as the Prime, across the per-uid barrier AA1 rests on. AA1.M's path-unit carry + `box n` already wake a pane.
- **X2 (alive) agi-boot's inbox ACL.** `g:agi:rwx` + a default ACL on .agi/sessions/inbox = every post may write every inbox: it widens the send.py route AA1.M retires.

## Findings on `slice` (for alive, D1; S2 also for self-perpetuating, D2)
- **S1 nesting is declared, not built.** `show` lists and `move` recurses over a `nested/` subtree, but `pack` (ptree) writes only `manifest` + `nodes/<mint>`. No verb ever creates `nested/`, so `move` recurses over nothing. The owner's "recursively collapsed into other nodes" is the part that is missing.
- **S2 `move --to-grid` writes history and drops the payload.** For every mint it commits a new version "slice-move vK" onto refs/grid/<trunk>/node/<mint>, and that version's tree is `node.md` ONLY. A grid version is node.md + its payload as ONE version, so a moved build node loses its payload in that version, and every move adds a version. The owner's invariant ("as long as our stats are read from the grid graph ... nothing changes. Only the overall appearance changes") fails: a collapse changes version counts.
- **S3 `--root` over-collects.** Children are found by `git grep -lF "  - <id>"`: a fixed-string SUBSTRING over any YAML list line. `--root goal:g1` also takes every node listing goal:g10, goal:g1.21, ..., and lines under `tags:` / `next_edges:`, not only `parents:`.
- **S4 no CAS on create.** `cas()` passes the old value only when the ref exists; a new ref is written with no expected-absent check, so two concurrent `pack N` both "succeed" and one is lost. `git update-ref <ref> <new> ""` refuses if the ref already exists.
- **S5 `unpack` only lists** (`git archive | tar -t`): it extracts nothing.
- **S6 an ungated outward path.** `slice push` sends refs/slice/* to origin, and origin is PUBLIC. The land gate (grow-gate, incl. the AA2.71 private-key line) runs on what lands on the trunk; whether a refs/slice/* push passes through any gate is not shown here. A slice is node bytes, so the same private-key rule should hold for it. QUESTION to whoever owns the push path.

## Findings outside `slice`
- **R1 the pane-output cap is gone (agi-run).** Base agi-run halved ~/o whenever it passed AGI_PANE_MAX_MB (64 MB), every 300 s. The pilot drops that loop, and AGI_PANE_MAX_MB appears nowhere on the pilot. A long-lived pane's ~/o now grows without bound on a shared box. KEEP the raw-shell branch, RESTORE the cap.
- **R2 a provider change in a kid command (agi-kid). RULED (A) by belam gen 28, 14:50Z: "Any land of the pilot agi-kid keeps --provider openrouter: OpenRouter is the provider the owner named (paid pi lane, provisioning key) ... A switch = (B) only on the owner's own line. Binds only if the pilot agi-kid is ever landed."** `--provider openrouter --model $AGI_KID_MODEL` -> `--model $AGI_KID_MODEL`: the provider becomes whatever the harness defaults to. Spend on a provider the owner did not name is banked, never decided by a post (CLAUDE.md, delegated authority 6). For belam.
- Retracted while measuring: "agi-track is missing" (it is a pilot section, 89 B; my first section list missed it).

## Next
- Every row has a verdict. What stays open is NOT a D4 call: the grok-harness decision (seat grok DGs this season or not: belam/SM), which decide xai-proxy, seed and agi-project's xai routing.
- D3 (the `legacy` marker + its renderer) waits on alive's D1 shape for a node's grid ref, since a legacy build node is exactly a node whose grid ref CONTAINS nodes not yet graphed here.
