#!/usr/bin/env python3
"""SD.06 experiment a00-e6925346-673328: measure the diagram-forms question with data.
Renders the SAME state-card+role-map+loop content three ways (prose, box-drawn,
indented-arrow) and counts o200k tokens for each. Settles "box glyphs cost tokens"
for the context-minimal hypothesis instead of taste.
Method: tiktoken o200k_base, identical to prior kids' baseline.
"""
import tiktoken

enc = tiktoken.get_encoding("o200k_base")

# Same underlying facts, three surfaces. Facts: 4 roles, build boundary,
# 6-kid loop with 2 exit branches, one tree each, merge to self-perpetuating,
# key floor $1.00, meter 0.41/0.46.

PROSE = """Four quorum seats share one worktree each on the season branch:
owner, planning, architecture, and delivery. Every seat speaks over the
shared dispatch channel, and only the two openrouter parent seats may build
source. The sanctuary master merges work upward into the self-perpetuating
branch. Work proceeds in a loop: dispatch a kid, review its node, choose
continue, adjust, or done. Continue spawns the next slice, adjust restates
what was wrong, and done exits the loop. The loop is capped at six kids.
Before every dispatch the openrouter key balance is checked and the run stops
at a one dollar floor, never lower. The rotation meter is at 0.41 of a 0.46
cap."""

BOX = """+-- quorum -- season/s2 -------- meter 0.41 / cap 0.46 --+
| ROLE     tree        build        channel            |
| owner    one         no           shared dispatch    |
| planning one         no           shared dispatch    |
| arch     one         no           shared dispatch    |
| delivery one         BUILD yes    shared dispatch    |
+-------------------------------------------------------+
            owner / planning / arch / delivery
              |          |        |         |
              +-- 1 tree each, merge -> self-perpetuating
                     |
                     v
           dispatch kid -> review node -> choose:
              continue -> next slice
              adjust   -> restate what was wrong
              done     -> exit
           cap: max 6 kids . check KEY before each . stop at $1.00 floor"""

INDENT = """quorum / season/s2 ... meter 0.41 / cap 0.46

roles (4, all one tree each, no build except delivery)
  owner
  planning
  architecture
  delivery      <- ONLY one that builds source

merge
  every role tree -> self-perpetuating

loop
  dispatch kid
  -> review its node
  -> choose
     -> continue  spawns next slice
     -> adjust    restates what was wrong
     -> done      exits
  ceiling: max 6 kids
  guard:   check OPENROUTER KEY before each dispatch
           stop at $1.00 floor, never lower"""

for name, text in [("PROSE", PROSE), ("BOX", BOX), ("INDENT", INDENT)]:
    n = len(enc.encode(text))
    print(f"{name:8s} {n:5d} tok  ({len(text):5d} B)")

# The node's own worked BLOCK 1 (box form), as shipped, for direct comparison:
BLOCK1 = """  +- BELAM . prime . season/s2 --------------- meter 0.41 / cap 0.46 -+
  | MODE  survival: 1 active seat, all others idle (~0 tok/h)         |
  | TREE  season/s2   pushed, 0 unpushed   3 dirty = unreviewed draft |
  | GATE  my rotation BLOCKED on l3w4-context-load-minimal            |
  | SPEND openrouter key $9.26 / $15   floor $1.00 NEVER lower        |
  +-------------------------------------------------------------------+
  NEXT   wait SD.03 -> commit rotate.py -> dispatch ctx-trim -> SD.05
  READ   S6.71 state . S6.75 trim . S6.78 roles       <- these three only"""
n = len(enc.encode(BLOCK1))
print(f"BLOCK1    {n:5d} tok  ({len(BLOCK1):5d} B)  [node's shipped box state card]")