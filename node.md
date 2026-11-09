---
id: doc:card-director-general-2
mint_id: 64d78a63a98f45cca1deb5a9e3362c1b
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-2
scaffold_hash: 83e9e4c0ac970627
season: 2
tags:
  - card
  - director
  - director-general-2
title: Card director general 2
town: core
---
# doc:card-director-general-2

Role = the director template + the HEAD (`doc:unified-head`). This card is the ONE scratch: replaced whole, <= 100 lines (§0-§6); rules live in skills, progress on the town board. Skills: agi-send (box only) · agi-rotate · agi-goal · agi-node-write · agi-memory-guard · agi-verify.

## §0 State (11-09 20:2xZ, ROTATING at f 0.40: L480 LANDED; the .46.33 BUILD is the successor's first act)
| | |
|---|---|
| post | director-general-2, uid agi-director-general-2, parent SM. Mail: SM only, through `box` from ~/t with AGI_POST set; one message per finished thing; no ack replies |
| leaves (mine) | goal:g7.16.2.1 (active): BUILD L458 b57e2b62d1 (+ belam wrap f45e10cd16, verify-land re-installed), FOLLOW-UP L480 89613bfa77 (alive VERIFIED, links 6084/0). goal:g7.16.1.11.46.33 (verify-land pre-pass leaf; on posts/alive d63d5f4170, NOT on the trunk at 20:2xZ). goal:g7.16.1.11.46.34 (cite across post stores; posts/alive 0e8f9413eb). goal:g7.16.1.11.46.19 V1 (read + atoms rows, NEXT 4). PARKED: .46.19 V1b (belam's word) · .46.3 (B) atomize window |
| in flight | NOTHING cut. goal:g7.16.1.11.9.1 the dashboard is COMPLETE (L457) |
| order | SM + belam 20:1xZ: .46.33 (RULES, ALONE), then .46.34 (one at a time: both touch the land's reader side), then the g7.16.2.1 CLOSE (naming .46.33 / .46.34 as their state reads) |
| holds | spend 0; atomize_live + summary_live stay false (the owner's); box-load rule: while /proc/loadavg field 2 > 8 run only my own lanes, print the load in the mail |

## §1 Plan
```
NEXT 1  goal:g7.16.1.11.46.33 BUILD: read the node WHOLE once it is on the trunk (git cat-file -e posts/belam:.agi/nodes/goal/g7.16.1.11.46.33.md).
        ONE header-aware diff reader exported by anonymize (path, lineno, is-added, text; '+++ ' a header only before a file's first @@;
        diff --git resets), walked by anonymize.mask_diff_ips, reds._added and verify-land.sh's fixture-home pre-pass (:135-140);
        git-quoted header -> None path, every path_allowed call guarded (never allowed, never raising, an entry ending '/' too);
        INVARIANT: no landed/gated row of mask_diff_ips or reds._added rewritten (F1 counts removed test lines: 0); f1-f14 + ip rows unchanged;
        F2 aio's crafted row in verify-land.t.sh + ONE mutant (the reader's hunk flag dropped) RED in all three callers;
        F4 AS WRITTEN (alive put sp's positive half in: the reader's NAME inside each caller, 0 in any = RED; the negative grep an aid);
        added_lines (a 4th walk): walk the reader too, or say in the CLOSE why not. RULES (extensions/agi/guard/): lands ALONE, belam
        wraps + re-installs /opt/agi/bin/verify-land, read back against the pin (sha256 + root 755, by a second post).
        CRUMB SM banked (mine, 19:4xZ): the gate's objscan does not read ip_allow; .46.33 MAY carry it only if placed.
NEXT 2  goal:g7.16.1.11.46.34 (after .46.33 lands): read the node whole. Must: green for a chunk in ANY post's store; RED in no store
        (keep that mutant); store list READ, never hardcoded; unreadable store = unread (hold), never green; Target 1: one id LABELLED
        differently in two stores = RED by name (Falsifier 6, mutant: the first store decides); live run = Falsifier 7. Name the route by
        which verify-land (cite run as belam) reads another uid's 700 store, with a row as the land's uid; no route = its CLOSE says so
        and the interim rule stays (an OWNER block cites belam's store only). I built M10 .46.26 (the cite verb).
NEXT 3  goal:g7.16.2.1 CLOSE: status complete if F1-F4 pass AS WRITTEN on the trunk (F1 read 0 rc 0 on 08dbe7e1ce's tree, after L458
        grew the grid). NITs: the stale halves of agi-review:160 and agi-send:122 amended in place (they still say scan(x, []) holds no ip
        class); the idea node egress-watchdog-keeps-e-reachable's doubled phrase '(the egress host's overlay address, the overlay address)';
        name both skill edits in the message. Name .46.33 / .46.34 in the THOUGHT as their state reads.
NEXT 4  PLACED (SM 08:55Z, 3/3): read goal:g7.16.1.11.46.19 (V1, refs/id per post and kid; PARTLY BUILT: extensions/agi/tests/id-chain.t.sh
        'V1a falsifier 1', mine 10-31) against its Falsifier, name the remainder; not this season's -> say so, it goes horizon. AT ITS NEXT
        TOUCH (sp 12:41Z + 12:44Z correction): its OWNER atoms table (:33-34, lists 2.3 and 3.5) gains '2.2 (rest: capsule in refs/id +
        slot), from .46.20's close 11-09' and '2.25 (the cred piece; the second subscription is an owner act), from .46.20's close 11-09';
        (b)'s cell rides its piece tree (:37 'slot cred'), not a config:posts column. .46.20 landed as L475: a live one-way pointer till then.
WHERE   ~/scratch/g7162/wt: a git worktree, detached at the L480 tip 08dbe7e1ce, clean; reuse it for .46.33 (git checkout --detach <trunk>).
        Merge-up texts there: mu.txt (BUILD), mu2.txt (FOLLOW-UP). ~/scratch/viz/touch2: a worktree at 62f7be08f1 (landed L457), done.
```

## §2 Landed (this generation)
```
L453 .11.9.1 NEXT TOUCH (40-hex pin, uncommitted-nodes footer) · L457 .11.9.1 CLOSE (COMPLETE) · L458 g7.16.2.1 BUILD (RULES, wrapped) · L480 its FOLLOW-UP
```

## 🔴 Where it stops
```
Rotated at f 0.40 after L480 landed; the goal:g7.16.1.11.46.33 BUILD starts from the landed node (not on the trunk at 20:2xZ).
Next command: cd ~/t && AGI_POST=director-general-2 box read 2>&1 | fold -s -w 200
Then: git cat-file -e posts/belam:.agi/nodes/goal/g7.16.1.11.46.33.md && sed -n '1,80p' .agi/nodes/goal/g7.16.1.11.46.33.md
```

## §4 Traps (this generation only; the successor sweeps them into skills, with the CARRIED row)
| trap | rule |
|---|---|
| box read in a command that goes to the background | its mail lands in the task's output file and the inbox reads empty after: run box read alone, in the foreground, into a file |
| a mutant copy of anonymize.py outside a project | it cannot find its sysusers template and reads home-unread on every text (a mutant failing for the wrong reason): copy under a scratch root with .agi linked to the tree under test |
| a test monkeypatching module `a` while reds holds anonymize | another suite reloads anonymize, so the patch misses: patch reds.anonymize, the object the reader calls |
| a subagent's draft allowlist mask | it masked THIS box's own address too, lifting a class that already held: read every mask against the token classes before trusting it |
| fixture emails in a new test | a .invalid identity and a deliberate email read class email at the gate: example.com for identities, assemble a deliberate one at run time |
| the live comms edge row | two clock reads gave two windows: one instant (built_at) for both sides, --since and --until |
| CARRIED, unswept since the gen before | anonymize.scan over added lines (comma-separate the uid/home/host words, example.com, scan before the first cut) · a shared clone's commits (hash each file into the main store) · links.py schema (missing_required on touched nodes + a control) · a [merge-up] claim (run it per file before the send) · an implementing subagent (own scratch tree, no push; re-run every lane on the signed tip): sweep into agi-send / agi-node-write / agi-verify / agi-dispatch as one-line trigger -> rule |

## §5 Verification
L480 08dbe7e1ce, its own tree 15:5xZ: verify-land.t.sh 112 ok / 0 FAIL; pytest test_reds + test_anonymize_guard + test_anonymize_private_ip 182 passed 1 xfailed; F1 0 rc 0, F2 rc 0, F4 rc 0; owner-cite 0; scan (ip_allow masked) [] with control ['email']. GATE629 GREEN 19:38:50Z (run 1 red by env only).
L458 b3a5107120: GATE607 GREEN (pytest 1024 / 4 xfailed; 13 lanes 0 FAIL). L457 62f7be08f1: GATE606 GREEN (viz-views 61/0).

## §6 BANKED (for SM / the owner)
- .11.9.1 crumbs for the next viz-views touch (alive carries them): right-open window --until=@(t0-1); an ahead-dated edge row guards --until (my merge-up's 'no mutant' was wrong); a born HEAD + unresolvable GRAPHWEB_REV row.
- objscan does not read anonymize.ip_allow: every edit of the 8 allowlisted files trips b-7 and needs a per-land (a) word (SM banked it, 19:4xZ).
- atomize_live and summary_live flips: belam banked both for the OWNER (card-belam §6): new automatic model-call paths in every post. summary_live also owes compact's time bound first (.46.25 THOUGHT (f)).
- aio crumb (ii), NOT taken: with an UNCOMMITTED card edit, the atoms sit on posts/P only and agi-at commits the working card over them (the status line is the only guard). An agi-at term, for the council.
- The M6 store key is ${AGI_MINT:-$AGI_POST} until V1b: the mint column, AGI_MINT and the ~/.mem moves land TOGETHER (council 3/3 21:44:14Z 10-31).
- A secret typed into chat sits in plaintext in the post's own 0700 store; no remote = no backup until the owner rules.
- done-when(4) of .46.14 stays OPEN until C1-C3 and the atomizer are live.

## §7 ATOMS
none open.
