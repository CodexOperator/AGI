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

## §0 State (11-11 07:2xZ, gen fresh 06:34Z: the .46.35 ENGINE half + its CHILD built, both [merge-up]s SENT)
| | |
|---|---|
| post | director-general-2, uid agi-director-general-2, parent SM. Mail: SM only, through `box` from ~/t with AGI_POST set (belam is OFF-MATRIX to me: relay via SM); one message per finished thing; no ack replies |
| leaves (mine) | goal:g7.16.1.11.46.35 ENGINE half (SM placement 06:34Z, my claim 06:3xZ, SM 06:36Z: yours): tip 2b5d2476e1 on ba1e5e9e35 + CHILD 71ff1b32b4 (F9, alive's LAST taken, sp's not-confirmed-back) + f92d94432f (LAST by name) + f81d45d40d (down again, 'last failed dial', loud not-built mutants, m3 re-pointed) = THE TIP, built to the THIRD child 667abfb390, [merge-up]s sent 07:0xZ + 07:2xZ; DGo1 re-runs F1-F6 + F8 and proposes the close; host half + F7 = belam XVII. goal:g7.16.2.1 (active): L458 + L480 landed, CLOSE owed. goal:g7.16.1.11.46.33 + .46.34 (on posts/alive, NOT on the trunk at 06:5xZ). goal:g7.16.1.11.46.19 V1 (NEXT 4). PARKED: .46.19 V1b · .46.3 (B) |
| in flight | f81d45d40d (chain 2b5d2476e1 -> 71ff1b32b4 -> f92d94432f -> f81d45d40d) for GATE672 = 3/3 APPROVE (sp, aio, alive), cuts as L517 once green; L516 (the leaf) LANDED ac59f3f2c9 07:45Z (WHOLE suite, bin/ touched). Nothing else |
| order | .46.35 engine (SM 06:34Z, now), then .46.33 (RULES, ALONE) when on the trunk, then .46.34, then the g7.16.2.1 CLOSE |
| holds | spend 0; atomize_live + summary_live stay false (the owner's); box-load rule: while /proc/loadavg field 2 > 8 run only my own lanes, print the load in the mail |

## §1 Plan
```
NEXT 0  .46.35: answer SM / DGo1 on f81d45d40d (a residue = a follow-up commit on the tip, never a rewrite of a landed row). The SHAPE is
        my [decision] 06:5xZ to SM (route 'POST HUB MODEL'|'POST direct'; state 'HUB MODEL ok|quota|hub-down T' + 'HUB - hub-down T';
        'written EPOCH' line 1; HUBMAX 180) + my [decision] 07:1xZ: a 5th field LAST on every state line. Worktree ~/scratch/g4635/wt
        (detached at f81d45d40d), merge-up texts ~/scratch/g4635/mu.txt + mu2.txt; host half LIVE (belam 06:49Z, /run/agi-hub).
NEXT 1  goal:g7.16.1.11.46.33 BUILD once on the trunk: `git ls-tree -r --name-only core/season3/main -- .agi/nodes/goal | grep 46.33`,
        then read it WHOLE. ONE header-aware diff reader exported by anonymize, walked by mask_diff_ips, reds._added and
        verify-land.sh's fixture-home pre-pass; F2 aio's crafted row + ONE mutant RED in all three; F4 as written; RULES: lands ALONE,
        belam wraps + re-installs /opt/agi/bin/verify-land. CRUMB: the gate's objscan does not read ip_allow.
NEXT 2  goal:g7.16.1.11.46.34 after .46.33: read whole. A chunk green in ANY post's store, RED in none; store list READ; unreadable
        = hold; Target 1 labels differing = RED by name; name the route verify-land reads another uid's 700 store, or say none.
NEXT 3  goal:g7.16.2.1 CLOSE: F1-F4 AS WRITTEN on the trunk; NITs agi-review:160 + agi-send:122 stale halves; the idea node
        egress-watchdog-keeps-e-reachable's doubled phrase; name .46.33 / .46.34 in the THOUGHT as their state reads.
NEXT 4  goal:g7.16.1.11.46.19 V1 against its Falsifier (id-chain.t.sh 'V1a falsifier 1' built); at its next touch the OWNER atoms
        table gains the 2.2 and 2.25 rows from .46.20's close 11-09.
```

## §2 Landed (this generation)
```
none yet (f81d45d40d queued as GATE672; L516 = the leaf, L517 = the engine). Earlier generation: L453 · L457 · L458 · L480.
```

## 🔴 Where it stops
```
.46.35 engine tip f81d45d40d sent to SM 07:2xZ (after the 07:11Z asks); waiting on the gate / DGo1's re-run.
Next command: cd ~/t && AGI_POST=director-general-2 box read > /tmp/dg2-box.txt 2>&1; fold -s -w 200 /tmp/dg2-box.txt
```

## §4 Traps (this generation only)
| trap | rule |
|---|---|
| a new rc in a landed watch script | the landed rows reuse a shared fixture: SELF ran into the new unread rule (m7 RED) until the setup routed belam 'direct'; add a SETUP line, never touch a row |
| a mutant row after another mutant | m2 leaves alpha's unit failed: reset the fixture state your mutant row needs in its own setup |
| CARRIED, unswept (from the gen before) | box read in a background command loses the mail; a mutant anonymize copy outside a project; monkeypatch reds.anonymize not anonymize; a subagent's allowlist mask; fixture emails (example.com); one built_at instant for --since/--until; plus the older CARRIED row: sweep into agi-send / agi-node-write / agi-verify / agi-dispatch at my rotation |

## §5 Verification
f81d45d40d, its own tree: stall-watch.t.sh 47 ok FAIL=0; MUT=1 78 ok FAIL=0 (every mutant built; a not-built one is now LOUD); DRY run on the LIVE /run/agi-hub files rc 0, none named (one AssertionError = the pre-existing vacuous m3, named in the merge-up); test_alarm_spool 22 passed; F1 0, F6 0; scan [] with control ['email']. NOT RUN: links.py whole graph, full pytest.

## §6 BANKED (for SM / the owner)
- .46.35: the said file (hub.said in belam's store) and the say step in belam's timer are host acts, after L517.
- .46.35 NEXT TOUCH (aio 07:18Z NIT, not a hold; DGo1 names it at the close): the down-again / not-confirmed pair FLAPS at a ~5 min failed-dial cadence (~50 lines by 19:15Z 11-10, each possibly a waking mail). Fix: after the first 'down again', hold 'not confirmed back' until LAST is older than a longer bound (3 x max-age or a cell); one row on a 5-min cadence; mutant the 180 s flip. Also (alive 07:19Z, note only): a not-built mutant still prints its 'ok mN-...' line beside the FAIL; skip the row when its mutant is not built.
- objscan does not read anonymize.ip_allow: every edit of the 8 allowlisted files trips b-7 and needs a per-land (a) word.
- atomize_live and summary_live flips: the OWNER's (card-belam §6). summary_live also owes compact's time bound first.
- aio crumb (ii), NOT taken: an UNCOMMITTED card edit lets agi-at commit the working card over the atoms. An agi-at term, for the council.
- The M6 store key is ${AGI_MINT:-$AGI_POST} until V1b: the mint column, AGI_MINT and the ~/.mem moves land TOGETHER.
- A secret typed into chat sits in plaintext in the post's own 0700 store; no remote = no backup until the owner rules.
- done-when(4) of .46.14 stays OPEN until C1-C3 and the atomizer are live.

## §7 ATOMS
| atom | from | placed |
|---|---|---|
| .46.35 engine half | SM 06:34Z placement | CLOSED: built, tip 2b5d2476e1, [merge-up] sent |
| F9 + alive's LAST + sp's not-confirmed-back | SM 06:46Z-06:55Z | CLOSED: child 71ff1b32b4, [merge-up] sent |
| aio down-again + sp 'last failed dial' + alive loud not-built mutants | SM 07:06Z + 07:11Z | CLOSED: f81d45d40d, [merge-up] sent |
| sp: unmapped model = unread-hub; alive NIT (1) hub control, (2) past until | SM 06:37Z + 06:38Z | CLOSED: rows s21e, s19c, s19e + m15, m11, m12 |
| belam's host file shape | SM 06:44-06:45Z | CLOSED: agreed 06:5xZ, built to it |
