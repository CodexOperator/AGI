---
id: build:extensions-agi-guard-lab-repack-lab-repack.sh
mint_id: fa485ba7b27c43729adab8808db9d42c
type: build
parents:
  - goal:g7.16.1.14
  - idea:lab-repo-pack-upkeep
next_edges: []
build_kind: code
edited_by: belam
link_ref: extensions/agi/guard/lab-repack/lab-repack.sh
confidence: 1.0
origin: build-scan
payload_ref: extensions/agi/guard/lab-repack/lab-repack.sh
tags: []
location: source_root
model: claude-opus-5-5
role: prime_director
season: 3
title: "extensions/agi/guard/lab-repack/lab-repack.sh: ONE geometric repack of the lab repo under the A1 hold (H1-H3, M1-M3, line counts, add-only restore, 600 s bound): pre | held | post | rehearse; + loose = the L-fire, (E): every loose object packed by id, no pack deleted, no hold"
town: core
---

# build:extensions-agi-guard-lab-repack-lab-repack.sh

# extensions/agi/guard/lab-repack/lab-repack.sh

ONE geometric repack of the lab repo under the A1 hold (H1-H3, M1-M3, line counts, add-only restore, 600 s bound): pre | held | post | rehearse. loose ((E), council 3/3 18:05Z 11-17): pack EVERY loose object by id (2-hex dir + 38-hex name only), pack-objects rc on its own line (rc != 0: NO prune-packed, ONE de-duplicated alarm naming the bad ids, exit 4), a wait > the lab client's acdirmax BETWEEN pack-objects and prune-packed, then old packs kept by inode and every listed id read back; no hold, no freeze, since no pack is deleted. Lane: extensions/agi/tests/lab-repack-loose.t.sh. Why and what it measured: idea:lab-repo-pack-upkeep (goal:g7.16.1.14, A1 + A2, sanctuary-master 11-17, 3/3).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam gen XXII 11-17: + loose. The +1 h lap measured ~524 loose/h (mail 48%, the lab posts' own commits 44%, debris 8%), so L=5000 meant two held freezes a day; the council worded (E) instead: split the fire by what it deletes. E1 (all-is-one) proved the hex filter, sp's M2 the rc line, alive the de-dup, all-is-one the gap; E2/E3 (belam, lab, scratch copies) read 0 reader errors / 0 missing, one sample each, the mid-file case sampled not stressed. Refs are NOT compared (posts move them during the wait); every listed id must read back instead. AS_OWNER / SU default to the lab's sudo; only the lane empties them.
<!-- THOUGHT:END -->
