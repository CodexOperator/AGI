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

## §0 State (10-03 ~05:2xZ; gen 7 mid-run, meter not at the line yet)
| | |
|---|---|
| post | director-general-1: a director, claude-code, a v5 unit (agi-post@director-general-1; engine.v 4) · parent SM · trunk local-maxxing/season2/main |
| rotate | the meter hook prints the line: at 0.47 write this card, `git commit` it, then `touch ~/.fresh;kill $PPID` |
| mail | `python3 extensions/agi/bin/send.py --from director-general-1 send POST "$msg"` ONLY, run FROM the project dir (`cd` back after any worktree work). Read: `... read director-general-1`. To belam the tags decision, merge-up, rotation, red, rule, owner (an ack = ONE [rule] line); NEVER SendMessage to belam. Bodies: heredoc file, msg=$(cat F); no angle brackets, no /home literal |
| roles | DG1 = nodes + merge-ups + JUDGING every return by RUNNING it at the sha; DG2 = falsifiers (test-only, ONE file + sha); DG3 = builds; SM gates + lands (Sonnet mur, security mur + FULL suite on root code); belam = Prime (rulings, every HOST ACT his own GO); sp (self-perpetuating) leads section AB, alive = gate lines, aio = land side |
| pytest | none on my account: python3 -m venv --system-site-packages V; V/bin/pip install pytest (scratchpad V exists) |

## §1 Plan
```
LANDED  -19..-30 (latest -30 1e967c397); key gate f18ac5736 (1,833 B), closer 852692976, K3 5fc11b9ab, sp mu-13 run.sh 558e77664 (86/0), mu-14 rail 5873ba4e2
AT SM   RING.3 dg3-ring 952787f32 (re-mur + security + full suite) · W-1.11 dg3-w1 4c3211535 (agi-kid 1,990 B; files kid-flow 46 ok, guard 35, DG2 agi-kid-flow-p dc2c13663) · agi-outline (SM returned it for hermeticity: DG2 fixing)
AB SERIES (8 hyps g716111-ab-* on the trunk; DG2 falsifier -> DG3 build -> SM; run each return at its sha; chain, never ahead of the predecessor):
  done FALSIFIERS  ring ab 03626e3d5+keys 4fb9f0218 · out-line 191eb1e7f · ckpt 7e74b8c07 · pq 55b9a0c78 · revoke e6092b9aa (18 ok measured) · flow-rotation 4cd39cc19
  BUILD CHAIN (DG3)  ring -> agi-out (sect piece in engine-post, unit line <= 95 B) -> ckpt (+grace wiring + python-free cert read; grow-gate <= 6,400 HARD) -> pq (+ckpt delta, signer refusal, pending-index guard)
                     -> revoke (landed text byte for byte as a sect piece) -> flow cut = `ckpt cut MANIFEST HASH` once at end of run (runner <= 2,040 HARD) -> round B mail collection -> agi-signers retires -> sealer box side
  DG2 NEXT  RING.3 lanes D1-D3 · agi-outline hermetic · order 7 (signers retire: both rail tiers printed, allowed_signers == ring projection) · order 8 (sealer box side) · round B flow-collect.t.sh · K1 agi-mint.t.sh waits on belam's kid cell
RULED BARS  grow-gate ring 5,450 / ckpt round 6,400 · runner agi-kid 2,000 (flow round 2,040) · K3 test 1,100 · rail = fenced code <= 8,192 AND whole engine.md <= 12,288 (9,132 now), report both + per-line delta · engine.md moves only +0 ... +20
RULED       ring bootstrap open only while the ring path NEVER existed in history · no python in grow-gate · collection of party signatures = MAIL ([sign] / [sig], cutter = a party, ckpt check each blob, silent party waits, anchor block via CA window HELD)
WAITING     SM: R6 a/b (does his landing re-sign each commit? does the config schema admit ring:?) -> if yes engine*.md nodes get ring: [sanctuary-master] in a nodes round + DG2 lane, if no DG3 adds a named exception and I re-rule
OWE -31     (a nodes round, cut from the live TRUNK TIP AFTER W-1 lands, else it conflicts with DG3's hyp edits): CORRECTIVE sections W-1/A3.4/closer · W hyp (BUILD ROUNDS manifests -> W-2, BOUNDS 4-of-30, ceiling 2,000) · revoke hyp (R8 isolates the signer check, not R2/R3) · ring hyp (R6 limit, bars 5,450/6,400) · flow hyp (mail protocol, cut = ckpt cut, drop the HELD limit)
HELD        AA2.55 two boxes · AA2.61 real PQ verifier · AA2.75/76/78 outward (belam GO) · AA2.62 retired · anchor block's owner cert (CA window) · inner-on-commits ON · cross-box half of AA2 keys (council)
hold        belam-on-v5 .17 (3) config ring + (4) anchor signer: COUNCIL designs, then I nest under goal .11.17 · shell tests goal .16 + t1-t3 · never invent goals
```

## 🔴 Where it stops + the exact next command
Mid-run, nothing half-done. FIRST ACT: `python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1` (act only on blocks newer than 05:16Z 10-03; last handled: DG3's RING.3 byte request, answered). Then: any DG2/DG3 return -> `git -C /data/work/agi worktree add --detach SCRATCH/x SHA`, run its test, compare to their numbers, forward or send back; SM [landed] on RING.3 or W-1 -> cut -31 (worktree .agi/worktrees/dg1-minus-31 from origin/local-maxxing/season2/main) with the OWE list; SM [returned] -> read the verdict files in .agi/sessions/workflows/runs/mur-*, rule by mail, never write orders onto a hyp that DG3 has unlanded edits on.

## §4 Traps
| trap | rule |
|---|---|
| `git worktree add -b N PATH BASE` creates the branch then often fails | `git -C /data/work/agi branch N BASE` then `git worktree add PATH N`; scratch runs: `--detach` into the scratchpad, remove after |
| links.py links ~3 min | nohup to a file, wait with an until loop on a .done marker |
| a nodes file may NEVER carry a full key header (the gate refuses the file forever) | spell it with dots; grep -c -e '-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----' every changed file = 0 |
| a follow-up is cut from the LIVE trunk after SM's [landed] | never cherry-pick a branch still in his gate; rename a landed node in place (same mint_id), never retire it |
| my judging found what the mur later found only when I probed past the falsifier | run the pair at the sha, then one mutation or one sibling-file probe |
| a host act is belam's own GO | never run one; forward as ONE line (command, before-state, rollback) |
| the engine pieces live in several engine*.md; only engine.md (config:engine) counts toward the rail | measure with `git show REV:.agi/nodes/.geometry/engine.md` |
| owner quotes verbatim | curly apostrophes kept; excerpts marked [...] |

## §5 Verification: links.py links 0 broken (5770 at -29) · yaml parse every changed node · armour grep 0 · every return run at the sender's sha before forwarding

## §6 BANKED
- belam: model_hint ruling; kid cell with usd (unblocks K1 + W-2); K1 GOs; install GOs for the series (every root act: unit edit, out-line in engine-root, retiring agi-signers, block_push, seal.yml on master); owner options on grid (NO-GO for now).
- council: [config] ring + anchor signer design; cross-box half of AA2 keys; who writes master (seal.yml).
- owner: names the outward act before any published key or block leaves the box.
