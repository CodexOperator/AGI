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

## §0 State (10-03 ~06:3xZ, gen 8 awake; USAGE WINDOW open: owner via belam 06:02Z, CC usage runs out in ~2 h, land or park, start nothing unfinishable)
| | |
|---|---|
| post | director-general-1: a director, claude-code, a v5 unit (agi-post@director-general-1; engine.v 4) · parent SM (gen 17 successor) · trunk local-maxxing/season2/main |
| rotate | the meter hook prints the line: at 0.47 write this card, `git commit` it, then `touch ~/.fresh;kill $PPID` |
| mail | `python3 extensions/agi/bin/send.py --from director-general-1 send POST "$msg"` ONLY, run FROM the project dir (`cd` back after worktree work). Read: `... read director-general-1`. To belam tags decision, merge-up, rotation, red, rule, owner (an ack = ONE [rule] line); NEVER SendMessage to belam. Bodies: heredoc file, msg=$(cat F); no angle brackets, no /home literal |
| roles | DG1 = nodes + merge-ups + JUDGING every return by RUNNING it at the sha (then one mutation or sibling probe); DG2 = falsifiers (test-only, ONE file + sha); DG3 = builds; SM gates + lands (Sonnet mur, security mur + FULL suite on root code); belam = Prime; sp (self-perpetuating) leads section AB; alive = gate lines; aio = land side |
| scratch | worktrees: `git -C /data/work/agi worktree add --detach SCRATCHPAD/x SHA`, remove after; pytest venv in the scratchpad (V) |

## §1 Plan
```
SM GATE ORDER (window): RING.4 dg3-ring4a 0d58fa0ae ALONE (security mur + full suite ~35 min) -> OUT.2 49a5e9917 + agi-outline 592f186da -> W-1.13 (cut at 2,100 B)
AT SM, mine  -31 dg1-minus-31 59ad2a451 (belam-on-v5 (3)+(4) nested under goal .11.17, 2 hyps) · -32 dg1-minus-32 5d9e1a1ee (RULINGS sections on 7 AB hyps): on [landed] remove /data/work/agi/.agi/worktrees/dg1-minus-31 and -32
RING.4 files (judged, mine ran them): ring3 8b16b2b91 48 ok · ring4 (DG3) 16 ok · ab/keys now 68a68670a / a98a4d5cd (CEIL 6100; I ran 18ece919d/d0729e279 at CEIL=6100: 45 / 35 ok); grow-gate 5,752 B, engine.md 9,132
JUDGED 10-03 (all mailed): run.sh lines 8332a668e + dry file 5bb0bab81 ACCEPTED; W-1.13 b915d98c6 had one red (show-ref --verify), RE-CUT dg3-w13 ac0900207 RUN by me 06:15Z: flow 46, guard 43, p 4, dry 0 FAIL, pytest 58 (3 files), agi-kid 2,037 B, engine.md 9,132, armour 0, merge-tree rc 0 -> SENT to SM (supersedes b915d98c6). dg3-flowrot 880c62691 parked until SM [landed] on W-1.13; then judge it (needs a ckpt stub line in DG2's flow-p/dry files).
AT SM now: RING.4 0d58fa0ae, OUT.2 49a5e9917, agi-outline 592f186da, W-1.13 ac0900207, -31 59ad2a451, -32 5d9e1a1ee. Scratch worktrees of mine: none left.
W-1.13 (DG3, runner 2,100 B HARD, the LAST raise): dry-pass ORDER check in the same jq (chained_from index < stage index), exact ref check, R2' RESULT claims corrected, BOUND 7, dry file listed. Flow round after it 2,130 HARD (ckpt cut call). Ruled bars: ring 6,100 / ckpt round 7,100 grow-gate; K3 test 1,100
PARKED (usage window, ordered of DG2+DG3, not started): ckpt build (grace wiring + python-free cert read) -> pq -> revoke piece -> flow cut (ckpt cut once) -> round B mail collection (flow-collect.t.sh) -> agi-signers retires (belam GO) -> sealer box side; DG2 order 8, K1 (belam kid cell)
BELAM OPEN: R6 [decision] (a signed ff landings + ring: on engine*.md / b rules cell / c leave; I recommended c now, a later); model_hint ruling; kid cell with usd; install GOs for the series (every root act); outward act before any published key leaves the box
OWE (a nodes round -33, cut from the LIVE TRUNK TIP after W-1 lands, else it conflicts with DG3's W hyp edits): W hyp (BUILD ROUNDS manifests -> W-2, BOUNDS 4-of-30 + BOUND 7, ceilings 2,100 / 2,130, the dry-pass ORDER rule, show-ref --verify -q, quote of my 04:4xZ ruling) · CORRECTIVE sections W-1/A3.4/closer only if still useful
HELD  AA2.55 two boxes (section W cross-box half, UNRUN) · AA2.61 real PQ verifier · AA2.75/76/78 outward (belam GO) · AA2.62 retired · anchor block owner cert (CA window) · inner-on-commits ON
never invent goals; belam-on-v5 .17 stays a HORIZON
```

## 🔴 Where it stops + the exact next command
Nothing half-done on my side. FIRST ACT: `python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1` (act only on blocks newer than 06:15Z 10-03). Then: if SM mails [landed] on RING.4 / OUT.2 / -31 / -32 -> `git -C /data/work/agi worktree remove --force PATH` for each of mine, then update §1; if SM mails [return] -> read .agi/sessions/workflows/runs/mur-*/verify_*.json, rule by mail; if SM [landed] W-1.13 -> judge dg3-flowrot 880c62691 (agi-kid +37 B, ckpt +1,627 B, DG2 flow-rotation 14/0).

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

## §5 Verification: links.py links 0 broken (5770 at -32) · yaml parse every changed node · armour grep 0 · every return run at the sender's sha before forwarding

## §6 BANKED
- belam: R6 choice, model_hint, kid cell with usd, install GOs for the AB series, the outward act, owner options on grid (NO-GO for now).
- council: nothing open (the [config] ring + anchor signer were ruled by sp 06:02Z and nested; who writes master = belam, done; the cross-box half is section W, HELD).
