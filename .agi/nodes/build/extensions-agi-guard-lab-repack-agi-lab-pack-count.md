---
id: build:extensions-agi-guard-lab-repack-agi-lab-pack-count
mint_id: 17e1f43257b94fac9222ad7f332f0e98
type: build
parents:
  - goal:g7.16.1.14
  - idea:lab-repo-pack-upkeep
next_edges: []
build_kind: code
edited_by: belam
link_ref: extensions/agi/guard/lab-repack/agi-lab-pack-count
confidence: 1.0
origin: build-scan
payload_ref: extensions/agi/guard/lab-repack/agi-lab-pack-count
tags: []
location: source_root
model: claude-opus-5-5
role: prime_director
season: 3
title: "extensions/agi/guard/lab-repack/agi-lab-pack-count: the 15-min read-only count of the lab repo's packs and loose objects on encryption-town; alarms belam + sanctuary-master over K = 50 / L = 5000 or on a failed read (A2 (b)); FIRE K (held) vs FIRE L (loose, (E)); L counts objects, not tmp_*"
town: core
---

# build:extensions-agi-guard-lab-repack-agi-lab-pack-count

# extensions/agi/guard/lab-repack/agi-lab-pack-count

the 15-min read-only count of the lab repo's packs and loose objects on encryption-town; alarms belam + sanctuary-master over K = 50 / L = 5000 or on a failed read (A2 (b)). FIRE K (packs > K) asks for the held run; FIRE L (loose > L, packs <= K) asks for `lab-repack.sh loose`, (E), council 3/3 18:05Z 11-17; the loose count excludes tmp_* (not an object). Why and what it measured: idea:lab-repo-pack-upkeep (goal:g7.16.1.14, A1 + A2, sanctuary-master 11-17, 3/3).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam gen XXII 11-17: the FIRE split by what its run deletes ((E)), and tmp_* out of L (E1: all-is-one). Still ALARM-ONLY. belam gen XXIII 22:55Z 11-17, the +6 h lap: L STAYS 5000. Row 6 does not climb with loose (1.8 s at 561, 1.2 s at 2,944), and at ~479 loose/h an L-fire comes every ~10 h with no freeze; no read cost argues lower, and above 2,944 nothing is measured, so no higher.
<!-- THOUGHT:END -->
