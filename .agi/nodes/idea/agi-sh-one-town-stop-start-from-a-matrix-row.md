---
id: idea:agi-sh-one-town-stop-start-from-a-matrix-row
mint_id: a21dd728dfd14561ac574489903f4ead
type: idea
parents:
  - goal:g7.16.1.11.44.8
next_edges: []
edited_by: director-general-2
model: claude-sonnet-5-5
role: director
scaffold_hash: 9a369b38367982ff
scale: small
season: 3
title: The town stops and starts with ONE agi.sh whose step order is a matrix row
town: core
---
# idea:agi-sh-one-town-stop-start-from-a-matrix-row

# The town stops and starts with ONE agi.sh whose step order is a matrix row

FRAME (council 3/3, 10-15 19:36Z): the owner's 10-15 ask is the target (agi-stop packs the town and brings it down; a fresh machine starts from the pack); the 10-14 bullets are HOW. agi.sh READS its step order from the `### matrix` row `town<TAB>start<TAB>posts crons units blast<TAB>agi.sh`: START runs the names left to right, STOP right to left, each name one function with an up arm and a down arm. So "the matrix carries crons and town start / stop as rows" is true by construction.

S1 (goal:g7.16.1.11.44.8): status + stop, the down arms only, on stubs. The stop is `blast` (`box town down <sha>`, belam only) -> `units` (town.state first, then every active agi-* unit outside the keep-list) -> `crons` (crons.py remove for every uid holding the marked block) -> `posts` (the posts' own units, agi-boot disabled). The ack is by the down commit's sha, never mail. S2 (start) and S3 (--pack / --from, the ring, the acceptance box move) come after.
