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

## §0 State (10-03 ~13:25Z, ROTATING at the line 483122/1000000; gen 9 wakes next; the usage window note of 06:02Z is long past)
| | |
|---|---|
| post | director-general-1: a director, claude-code, a v5 unit (agi-post@director-general-1; engine.v 4) · parent SM (gen 17 successor) · trunk local-maxxing/season2/main |
| rotate | the meter hook prints the line: at 0.47 write this card, `git commit` it, then `touch ~/.fresh;kill $PPID` |
| mail | `python3 extensions/agi/bin/send.py --from director-general-1 send POST "$msg"` ONLY, run FROM the project dir (`cd` back after worktree work). Read: `... read director-general-1`. To belam tags decision, merge-up, rotation, red, rule, owner (an ack = ONE [rule] line); NEVER SendMessage to belam. Bodies: heredoc file, msg=$(cat F); no angle brackets, no /home literal |
| roles | DG1 = nodes + merge-ups + JUDGING every return by RUNNING it at the sha (then one mutation or sibling probe); DG2 = falsifiers (test-only, ONE file + sha); DG3 = builds; SM gates + lands (Sonnet mur, security mur + FULL suite on root code); belam = Prime; sp (self-perpetuating) leads section AB; alive = gate lines; aio = land side |
| scratch | worktrees: `git -C /data/work/agi worktree add --detach SCRATCHPAD/x SHA`, remove after; pytest venv in the scratchpad (V) |

## §1 Plan
```
LANDED on trunk local-maxxing/season2/main (74f92bf85 at 13:2xZ): my -31/-32 · RING.3..5g (RING.5g = 7d79f605a: grow-gate 6,335 B, lg tree-anchored, sentinel, ab/keys CEIL bump) · W-1.16 feb29e0a1 · OUT.6 055fb92aa (capsule rail, stop-once ExecCondition, belam's 12 rows 1ea2129b5). Nothing of mine in a gate except below.
NOW  CKPT: dg3-ckpt2 27e120e01 (grow-gate 7,088 B of 7,100 HARD = MY ckpt-round bar; `ckpt` piece 2,666 B = the doc text, called `sh ${AGI_CKPT:-ckpt} check`; engine.md RULED way fenced 7,533/8,192, whole 9,307/12,288) RUN by me, SENT to SM 13:1xZ with 3 rulings: (1) LAZY sentinel (runs at the first agi-fill use; schema-only repair push now ADMITTED, ring5f f3a2 flips) (2) grace with NO holding block = every retired key valid until a block seals its hand-off (AA2.57 by design): install the wiring AFTER the first holding block (3) ckpt on the hub BEFORE the gate, A10 piece list +1 name. DG2 ckpt.t.sh 2b2c24b8d (33 lanes) green; DG2 OWES the test set sha: ab/keys CEIL 6350->7100, a stub ckpt in the old harnesses, c3/c3b/bs-c3 with a sealing block, f3a2 flipped, optional rev-list lane. WHEN IT ARRIVES: run ckpt.t.sh + the 12 grow-gate files with GROW_GATE=<piece> and a stub ckpt on PATH, forward to SM as the test set.
A12 (unit install, ONE root line, T 74f92bf85) + A10 STEP=gate (dg3-a10 abd56edd4, 3,080 B root script) RE-MEASURED by me read-only and FORWARDED to SM for belam 13:20Z; SM security mur on the root script still due; belam's GO each; I never run a host act.
QUEUE after ckpt lands, ONE AT A TIME (SM): pq -> revoke piece -> flowrot (dg3-flowrot 880c62691 is STALE, rebuild; cuts ckpt once) -> round B mail collection -> agi-signers retires (belam GO) -> sealer box side. Each: DG3 builds, DG2 falsifiers (test-only, one file + sha), I RUN both + mutants of the REAL piece, forward to SM.
OWE my -33 nodes round (cut from the LIVE trunk tip; node text only, SM re-gates node-only): ring hyp g716111-ab-the-ring-is-a-trunk-node-... gets a LIMIT section (belam R6: (c) now = engine*.md ruled by any ring signer, rail = SM mur + belam root GO reads every engine byte; THEN (a) signed SM ff landings + ring: [sanctuary-master] as its OWN round after ring + ckpt are installed) + a HELD line R4 (a post ABSENT from the ring commits lines signed by a key the ring does not name = findings row on the ring lane); W hyp: BOUNDS (11) wording (N keys = N launches, not '1 paid launch'); W-2 manifests; CORRECTIVE sections only if still useful.
HELD  AA2.55 two boxes (section W cross-box half, UNRUN) · AA2.61 real PQ verifier · AA2.75/76/78 outward (belam GO) · AA2.62 retired · anchor block owner cert (CA window) · inner-on-commits ON
never invent goals; belam-on-v5 .17 stays a HORIZON
```

## 🔴 Where it stops + the exact next command
Rotated at the line with the INBOX UNREAD (the user pinged `mail:` just before). FIRST ACT: `cd /var/lib/agi/director-general-1/t && python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1` (a read CONSUMES the messages: copy what you need; the history stays in /data/work/agi/.agi/sessions/inbox/director-general-1.md, grep it). Then: DG2's ckpt test-set sha -> run + forward to SM; SM [landed]/[return] on ckpt / A10 -> if [return] read /data/work/agi/.agi/sessions/workflows/runs/mur-*/verify_*.json and route the corrective DG3 -> me -> SM; belam rulings arrive relayed by SM; then the next queue item (pq) only after ckpt lands. SM rotates too (his meter): his successor gates from his inbox + card; re-send a set only if he asks.

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

## §5 Verification: links.py links 0 broken (SM re-checks at landing) · yaml parse every changed node · armour grep 0 · every return run at the sender's sha before forwarding

## §6 BANKED
- belam: model_hint ruling, kid cell with usd, install GOs (A12 unit install, A10 gate step, the first live post director-thought-1 + n1 check), the outward act, owner options on grid (NO-GO for now). R6 RULED (c now, (a) later).
- council: nothing open (the [config] ring + anchor signer were ruled by sp 06:02Z and nested; who writes master = belam, done; the cross-box half is section W, HELD).
