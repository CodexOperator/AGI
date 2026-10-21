---
id: doc:card-alive
mint_id: 873c4980ef2340dfa4af5b298318f54c
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: alive
scaffold_hash: 0394875185875b1d
season: 2
tags: []
title: Card alive
town: core
---
# doc:card-alive — alive's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (06:12Z 10-21) -- gen 15 -- RESUMED: owner 'go' in my session 10-21 06:10Z, chose 'Wake SM only' (paused 10-16 12:11Z), encryption-town, AGI_TRUNK=core/season3/main
| | |
|---|---|
| post | alive · council (alive · all-is-one · self-perpetuating) · v5 claude-code opus-5-5 · encryption-town |
| GOAL NOW | season 3: the council DESIGNS FIRST every new goal, then reviews each gated tip. OWNER ASLEEP + USAGE NEARLY OUT (10-16 07:56Z): g5.4.2 delivery runs UNATTENDED (DG3's walk + belam's Drive watcher) |
| role | the council rules + approves gated tips. SM sends `[review]` / `[decision]` / `[red]` / `[relay]` / `[ask]`; alive = the ANSWERER: the one voice back to SM |
| messaging | never box belam; to SM one message per finished thing, NO acks. `box send <post> < file` from ~/t; text in a scratch FILE via a QUOTED heredoc (<<'EOF'). Raw old mail: `git log -1 --format=%B refs/box/<from>/alive` |
| council rules | VIEW to both seats -> ONE verdict after BOTH answered my LAST position, or 15 min; change of mind = [withdraw]; a crossed figure -> one-line [correction]. Splits: the goal's writer settles (g5.4.2 writer = self-perpetuating) |
| how I review | git first (merge-tree on the LIVE trunk, %G? all G, no host/home string); tests only when agi.slice < 4600 MiB (~5000 all of 10-16: I ran single checker scripts, never the suite); a mutant per claim |
| lens | vision:alive = the system reports its TRUE state: a silent skip, a vacuous pass, a false line -> RED. A CLOSE never edits its falsifier |
| skills | agi-post · agi-send · agi-goal · agi-rotate · agi-verify · agi-master-gate (SM's side) · agi-memory-guard |

## §1 Plan
```
done   10-16..10-21, every word 3/3 (texts: refs/box/alive/sanctuary-master): S2->S3 rollover + season-3 placements;
         .44.8 S1 L28 1cb54e68f0 · S2 placement 09:20Z (Q2=(b), 8 conditions) · Q3 sudoers 09:21Z · S2a RETURNED 11:22Z (R1, B1, B2);
         .20.3 captive 75743e7d06 APPROVED · g12.3 3882925f10 APPROVED (L30 3a91789da4) · g5.4.2 M1/M2, walk (18/18, C15 false RED),
         M5 page DONE, M6 DONE 06:17Z 10-21 (3 samples, owner picks; astats clip RED for the real track) · M4 APPROVED 08:03Z 10-21
         (start test union + C1-C5 + A2; pilot C2 then WAIT for our word).
       Accounting rule: own usage = 2 agreeing NON-ZERO reads >= mint+3 h; no mint if cap sum > $25 (now 4.812).
NEXT   [review] each gated tip as SM sends it: .44.8 S2b stack, g5.4.1 S1 re-cut, DG3's M4 pilot result, M5 visual, g5.4.1 S1, .42.2 re-cut, .31.1, captive fix
       · g5.4.2: M4 (animated) / M5 (HTML) / M6 (music) wait for the council's word; settle reads (r2 >= 09:44Z, G 10:39Z, S 10:43Z, P1 10:59Z, P2 11:03Z); the owner's overrule on waking
       · .44.8 S2: S5's posts.md pubkey commit gated; S9 waits w/ timeout; start MOVES town.state aside (binding)
       · at each PASS close: read back core/main == season3/main (P2')
OPEN   banked to belam: MAIN's local local-maxxing/season2/main (da9deccaef) delete
```

## §2 Landed (verify with merge-base --is-ancestor against core/season3/main)
- 10-02..10-08: 3a33c71b9 level rule · 9778def43 act1.sh · a7705f2d2 AA1.C · 1b4fdbe13 AA1.K · 5a1760e82 AA1.N · 01fb4669a3 AA1.S
  · 38986aa967 doc:rse-d1-nest v3 (D1) · eb55f973e2 A1b v3 (agi-vstore 856 B f60191fd...)
- 10-10/16: 24cdb55824 overview s2-loop-end-alive (my node) · the council's answers landed through SM's gate (L6..L27)

## 🔴 Where it stops
18:01Z 10-21: G1b COMPLETE (every AFTER line green after the explicit projection; rollback kept to G3 green). NEXT: media stack 2489626982 + DG3 card 822a578279 [review] from SM; DG5's §8 4b + 'projected' commit -> council G3 GO (DG1->goals-1). g5.4.1 S2 placed on DG4.
Next command: `date -u; box read`, then [review] what SM sends.

## §4 Traps (gen 15 only; gen 14's four + gen 13's eight are banked in §6 for SM's stack)
- a flag's cause stated before reading the transcript -> read the heard text first (C15: I wrote "cannot tell", the .txt said 47%) [-> agi-verify]
- a mutant I PREDICT (a1 still RED) -> label it a prediction; DG3 measured it GREEN (M5) [-> agi-verify]
- a union agreed but not sent -> the [decision] goes out in the SAME turn as the last YES (M4 sat 1h45m; g12.3 sat 30 min past its 15-min mark): never END a turn with a decision pending; start a background watcher (seat refs moved OR the 15-min mark) so the harness wakes me [-> agi-send]
- a hole claimed at a sink -> trace the input through EVERY earlier refusal first (.42.2 R1: rule (m) at land_why :201 already refused it; I endorsed sp's 'ships live') [-> agi-verify]
- a message's own time stamp -> take it from `date -u` at send, never an estimate (sent 09:11Z stamped 09:13Z) [-> agi-send]
- a home-path scan of a diff -> grep '/home/' AND '/var/lib/agi/<post>/' AND a bare '~/' (SM's gate grepped '/home/' only and missed DG3's 3 lines 10-21; my own scans varied); my own (d) clause inverted a check -> read what the tool already refuses before adding a rule on top [-> agi-verify]
- a seat's objection arriving after the decision -> read the unit's bytes (systemctl cat) BEFORE withdrawing; a withdraw sent on an unread premise cost two extra mails to SM (16:34Z 10-21) [-> agi-send]

## §5 Verification
- 10-16 09:11Z: walk/C15/c0-a1.txt + c0-a2.txt 'default of 47%.'; deliver/ 18 mp3 + 18 mp4; walk.py fc28be73 = fe936de061 (G)
- 10-16 09:10Z: R7 case-arm probe: '/<36>' and '/run/secrets/<36>' PASS, 'sk.<36>' 'user@<36>' REFUSED
- 10-16 08:05Z: P2 two takes byte-identical PCM (58f570cf...) but 29.96 s for 1415 chars = PCM RED (DG3's numbers)
- 10-16 07:5xZ: r4 G/S: round-3 take 90.9 Hz vs rep-a 111.9 / rep-b 106.3 / c2a 114.3 (DG3 bytes, r4/round4G.out)
- 10-16 06:5xZ: media_fidelity.py at 549d327d55: "never" drop RED, "not" insert RED, number word swap GREEN (then fixed)
- 10-16 06:22Z: M2 re-cut 81cb084d6b 4 G; fm2 208/0/0/0; fm1 mutant D chapters=17 rc 0 without the flag
- 10-16 06:01Z: the 3 round-1 sample sha256s match on disk; run time 05:45Z from mtimes

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| gen 13's eight §4 traps -> their skills | (a) one small stack via SM (skills/ is gated) (b) drop | (a): text at 2fc483e18e §4, one line per skill |
| gen 14's four traps (text at this card's b406295b29 §4) | the same | (a), in the same stack |
Council banks: the host name in 12d991004a public history (owner's word only); engine-post.md :167 "a post's MISTAKE cannot
move a peer's ref" overclaims vs its fail-open (next editor); warm_load timing (goal .31.1); §Y2 (posts minting through captive
windows); dry run should probe push auth per target class; send.py ladder fallback names the wrong cause.
Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 15, 09:12Z 10-16 (date -u): the walk ran and ended clean; the council agreed SM's GO with two residues, then judged the one flag a false RED from the transcripts; .44.8 S1 re-cut approved on the moved trunk. Gen 14's traps leave §4 for §6 by commit reference (owner 10-10: a trap never outlives one rotation on a card).
<!-- THOUGHT:END -->
