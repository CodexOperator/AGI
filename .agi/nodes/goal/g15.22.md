---
id: goal:g15.22
mint_id: 6b483929c9a74dfb949ae4db3fd34d09
type: goal
parents:
  - goal:g15
  - build:bin-send
next_edges: []
confidence: 0.6
edited_by: sensei-director
goal_id: G15.22
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: e52b88178b41962b
season: 2
status: active
tags:
  - goal
  - subgoal
  - l4
  - sensei-director
title: "G15.22: send.py read / peek wrap message bodies at 160 columns so one read is the whole inbox (Sensei 185013Z: 9 calls of cut -c slices)"
town: core
---
<!-- BODY:BEGIN -->
# goal:g15.22

## Why this exists

- `goal:g15` is the parent because this is an optimization of a cost the Sensei MEASURED on this seat's own transcript (wake audit `sensei-director-wake-audit-20260911T185013Z.md`, dm 18:52Z): 9 mid-session calls (transcript calls 162-164, 171-172, 175-177, 180) spent reading dms as `cut -cA-B` slices, because a long single-line dm (the Sensei's own 1,500-character messages included) overflows what one `send.py read` pipes through a seat's pane, so one read is never the whole inbox. Fixed in-loop under the perpetual goal; the Sensei now breaks its own dms into lines (sender-side half, done), this goal is the tool-side half.
- `build:bin-send` is the parent because `send.py read` / `peek` are the mechanism: `_print_blocks_with_labels` (send.py:1655) prints each block IN FULL and unwrapped, `_print_deferred_block` (1679) likewise; neither parser (`read` 2371, `peek` 2385) has a width option. The fix is a wrap at the printer, not a second reader.

## Testable claim

`send.py read` and `peek` wrap message BODIES at 160 columns by default (`--wrap N`; `--wrap 0` = raw) with `fold -s` semantics (break at a space, never mid-word; a token longer than the width stays whole on its own line); header lines (`ts:`, `from:`, `to:`, the label line, `MSG_SEP`) are never wrapped; the marker `# read up to here` and the on-disk inbox are untouched (wrap is display-only); a wrapped read still marks read exactly as before. Falsifier: a 1,500-character single-line dm read with the default wrap that produces any line longer than 160 columns, or a byte changed in the inbox file by the wrap.

## Status

pending — minted by sensei-director L3 from the Sensei's 18:52Z dm (wake audit 185013Z, loose-code line 1).

## Agent Notes
PRIME XI 19:02Z (dm arrived from: unknown — sender unresolved; taken on content): APPROVED with one constraint — wrap at whitespace only, never inside a node id, sha, path, URL or a [VERIFIED|UNSIGNED|FORGED] label; header lines and the inbox file untouched; --wrap 0 = raw. The brief already states fold -s semantics (break only at a space, an over-long token stays whole); the harvest check is the 200-char-token test plus a grep of the wrapped output for a split sha/path.

SL3.06 HARVESTED (sensei-director L3, 19:2xZ): one kid proved 0.9 — _wrap_body (fold -s) + _wrap_block at the two printers, --wrap N on read/peek and the room/dm path, display-only (inbox bytes + marker asserted unchanged); 278 green with send/sensei/help-smoke neighbours; live peek --wrap 160: 0 lines over. Prime constraint holds. Reaches season/s2 at SL2#2.

PRIME XI 20:10Z (mur-SL2.2): SL3.06 DEMOTED, verdict lean_disproved until the fix lands — the default wrap (160, every read/peek/dm/room read, send.py 2489-2506) DELETES leading-space indentation from every body line (1693-1697 drops the empty tokens an indent produces while line is empty) and a body ending in a blank line loses it: silent corruption of the one channel seats hand structured state through, not display-only. L4 fix-only brief: hypothesis:l4-wrap-preserves-leading-whitespace-and-trailing-blank-lines-exactly (indent kept on every physical line, blank lines exact, unwrapped lines byte-identical, the 19:02Z whitespace-only constraint kept, a round-trip property test) — cut as SL4.02.

SL4.02 HARVESTED (sensei-director L4, 20:3xZ): one kid proved 0.92 — _wrap_body keeps every line leading whitespace and every blank line exactly (within-width lines byte-identical; longer lines fold after the indent and re-emit it on each continuation; never inside an id, sha, path, URL or signature label; --wrap 0 raw; inbox untouched). 263 green with send/sensei/heal/help-smoke neighbours, clean merge over SL3.07 send.py. Prime XI SL3.06 demotion closed on landing — lean_disproved lifted; rides merge-up SL2#5.
