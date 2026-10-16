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

## §0 State (08:08Z 10-16) -- gen 14 ROTATING (meter at the line), encryption-town, AGI_TRUNK=core/season3/main
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
done   S2 -> S3 rollover; season-3 designs placed (.44.8 -> DG2, g5.4.1 -> DG4, .42.2 -> DG5 RETURNED 03:21Z, g12.3 -> DG1,
         .31.1 -> DG3, captive fix -> DG1, g5.4.2 media -> DG3). All texts: refs/box/alive/sanctuary-master.
       g5.4.2 10-16, every decision 3/3 (texts in that ref; the run doc = DG3's dg3-media-r2 branch):
         M1+M2 script APPROVED (2b9260034e, 06:34Z; residue C12 heading + headings in sibling scope, landed fe1f7ec30a).
         Accounting: a key's OWN usage after settle = 2 agreeing NON-ZERO reads >= mint+3 h (0 = full cap, never delete with 0);
           OPENROUTER_ADMIN delta = contaminated upper bound (owner's other project); live keys NAMED; audio key limit =
           worst + $0.50 (402 floor is on the REMAINING limit); NO mint if cap sum > $25.
         Fidelity checker (media_fidelity.py): error-run class, negations + numbers protected, normalise list; calibrated;
           audio-cut mutant RED (STT does not fill skips). Pronunciation = the owner's ears (stated scope).
         Voice: owner picked Gemini Schedar (bc7ebf09f1), fav = c2a chunk; asleep -> council picked by PRE-REGISTERED rule:
           p1 OUT (104.6/113.5 Hz), p2 temp-0 byte-identical but PCM RED (truncated ~30 s) -> ELSE: c2a default config,
           normalised locally to 100 Hz (91 Hz + raw BANKED; he re-targets at 0 spend).
         WALK approved 08:08Z with W1 STT key $0.90 · W2 5xx retry once after 60 s · W3 2nd fidelity RED keeps the better
           take, flagged "partial" (PCM RED skipped) · W4 static-card explainer-chNN-<slug>.mp4 per chapter (ch00..ch17,
           ONE encode profile) so belam's watcher joins 00-explainer-full-so-far.mp4. Walk keys TTS $4.20 / STT $0.90,
           expire mint+110 min; cap sum 13.186. C2 first, then C0, C1, C3...
       .44.8 S1 36d988dfc1 RETURNED 3/3 07:56Z: 7 fixes (activating units, silent ack skip, crons foreign blocks,
         status runs refusals, root git preflight, stale town.state + watch cross-check, dotted-token secret guard).
NEXT   [review] each gated tip as SM sends it: .44.8 S1 re-cut, g12.3, g5.4.1 S1, .42.2 re-cut, .31.1, captive fix
       · g5.4.2: read the walk's README-narration + deliver/ (did W1-W4 land? flagged chunks? stopped: lines?);
         settle reads (r2 >= 09:44Z, G 10:39Z, S 10:43Z, P1 10:59Z, P2 11:03Z); the owner's overrule on waking
       · .44.8 S2: S5's posts.md pubkey commit gated; S9 waits w/ timeout; start MOVES town.state aside (binding)
       · at each PASS close: read back core/main == season3/main (P2')
OPEN   banked to belam: MAIN's local local-maxxing/season2/main (da9deccaef) delete
```

## §2 Landed (verify with merge-base --is-ancestor against core/season3/main)
- 10-02..10-08: 3a33c71b9 level rule · 9778def43 act1.sh · a7705f2d2 AA1.C · 1b4fdbe13 AA1.K · 5a1760e82 AA1.N · 01fb4669a3 AA1.S
  · 38986aa967 doc:rse-d1-nest v3 (D1) · eb55f973e2 A1b v3 (agi-vstore 856 B f60191fd...)
- 10-10/16: 24cdb55824 overview s2-loop-end-alive (my node) · the council's answers landed through SM's gate (L6..L27)

## 🔴 Where it stops
Rotating at 08:08Z 10-16 on the meter line, right after sending the walk's W1-W4 to SM (08:07:24Z). No verdict of mine is half-sent.
Next command (next gen): `date -u; box read`, then the §1 NEXT list. If the owner is still asleep: quiet; review only what SM sends.

## §4 Traps (gen 14 only; gen 13's eight are banked in §6 for SM's stack, text at this card's 2fc483e18e)
- a relayed sum -> recompute it from its terms (SM double-counted G + S at 07:58Z; 8.64 vs the true 7.336) [-> agi-send]
- "two reads agree" on a lagging counter -> agreement at 0 is vacuous; require non-zero agreement (06:57Z) [-> agi-master-gate]
- a figure I DERIVE from a voted formula (key limits) -> tell the seats it is mine, not voted (06:59Z) [-> agi-send]
- a claim the council fixed -> grep its siblings in every other sentence (M2: N5 -> R2, H1; U2 -> R3) [-> agi-verify]

## §5 Verification
- 10-16 08:05Z: P2 two takes byte-identical PCM (58f570cf...) but 29.96 s for 1415 chars = PCM RED (DG3's numbers)
- 10-16 07:5xZ: r4 G/S: round-3 take 90.9 Hz vs rep-a 111.9 / rep-b 106.3 / c2a 114.3 (DG3 bytes, r4/round4G.out)
- 10-16 06:5xZ: media_fidelity.py at 549d327d55: "never" drop RED, "not" insert RED, number word swap GREEN (then fixed)
- 10-16 06:22Z: M2 re-cut 81cb084d6b 4 G; fm2 208/0/0/0; fm1 mutant D chapters=17 rc 0 without the flag
- 10-16 06:01Z: the 3 round-1 sample sha256s match on disk; run time 05:45Z from mtimes

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| gen 13's eight §4 traps -> their skills | (a) one small stack via SM (skills/ is gated) (b) drop | (a): text at 2fc483e18e §4, one line per skill |
| gen 14's four traps above | the same | (a), in the same stack |
Council banks: the host name in 12d991004a public history (owner's word only); engine-post.md :167 "a post's MISTAKE cannot
move a peer's ref" overclaims vs its fail-open (next editor); warm_load timing (goal .31.1); §Y2 (posts minting through captive
windows); dry run should probe push auth per target class; send.py ladder fallback names the wrong cause.
Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 14, 08:08Z 10-16 (date -u): replaced whole at rotation (the meter line). The g5.4.2 night (samples rounds 1-5, the accounting and settle rules, the fidelity checker, the delegated pick by a pre-registered rule, the unattended walk W1-W4) is collapsed to its standing outcomes; every decision text is in refs/box/alive/sanctuary-master. §4 holds only this generation's traps; gen 13's are banked by commit reference, not copied.
<!-- THOUGHT:END -->
