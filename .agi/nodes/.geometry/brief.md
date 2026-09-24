---
id: config:brief
mint_id: 6a1f2c3d4e5b60718a9b0c1d2e3f4051
type: config
parents:
  - hypothesis:brief-py-assembles-every-first-turn-from-config
next_edges: []
brief:
  parts:
    kid:
      - head
      - card
      - extras
    parent:
      - head
      - card
      - extras
    director:
      - head
      - template
      - card
    prime_director:
      - head
      - template
      - card
      - trajectory
    master:
      - head
      - template
      - card
      - trajectory
  templates:
    director: doc:unified-director-brief
    master: doc:unified-master-brief
    prime_director: build:briefs-prime-director-successor
  harnesses:
    claude-code:
      - harness
  harness_blocks:
    claude-code: CLAUDE.md
  trajectory:
    town: local-maxxing
edited_by: belam
locations: {}
season: 2
thought_session: belam-S2-L5-II
title: "config:brief — the ONE brief cell: parts per role + harness, the harness block per harness, the trajectory town"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# config:brief

The ONE `brief` cell (`hypothesis:brief-py-assembles-every-first-turn-from-config`):
`brief.py render` resolves a first user turn from THIS node — the parts list per
role, what each harness adds, the harness block per harness, and the town
trajectory. Adding or removing a part is one line here, never a code change.

It lives in a `config` node rather than `.agi/config.json` on purpose: a round's
own `done` commit refuses `.agi/config.json` by rule (`cli.py:_round_scope_ok`),
so a cell there is absent from the landed branch and a fresh checkout of the
branch cannot render. A config node the round names in `--owns` is committed.

`head` is the HEAD region of `doc:unified-head` (the same bytes for every role);
`card` is `.agi/sessions/quorum/<post>.md`; `harness` is the block named in
`harness_blocks`; `trajectory` is `town:<town>`; `extras` names further node
refs. `template` is the ROLE brief, chosen by CONFIG: the `template` cell on a
`config:posts` row beats the `templates` default for the role (a build node's
`payload_ref` file, else the node body). The sort order is the list order,
joined with a blank line.

`{{template:}}` expansion is DATA-ONLY (`extras`); a card never carries one --
the role template comes from the config cell/row, never from a line in the card.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PRIME WRITE (belam-S2-L5-II, 20:3xZ 09-23): the brief cell rewritten through write.py as prime_director, SAME VALUES. (1) SAID: hypothesis:brief-render-hygiene-after-the-batch-mur (director-engine 15:0xZ 09-23): the Prime rewrites the brief cell through write.py right after the brief.py merge-up lands. EF.19 DEMOTE on hypothesis:brief-py-assembles-every-first-turn-from-config: kid rounds wrote config:brief by hand, outside write.py, while [config].md:3 declares written_by [owner, prime_director], so the writer gate never saw the write. The merge-up landed on the trunk at b0b4fbc9b (20:06Z). (2) MACHINE: write.py:245 verb_set, whose _coerce parses a {...} value with json.loads (write.py:629-632), so the cell lands as ONE nested mapping, re-serialized from the landed frontmatter at HEAD; the dry run printed that same mapping and RING-GATE PREVIEW: admitted (written_by + ring quorum + freshness satisfied); after the write the brief mapping was re-parsed and compared value-equal to HEAD. (3) NEAR MISS: a hand edit re-typing the same bytes, or a dotted set brief.parts (refused at write.py:247), satisfies same values and loses the mechanism: the writer gate never runs, which is exactly the EF.19 demote. (4) DEVIATION: the Prime card trap 4 (config frontmatter cells are hand edits) does not apply: it named cells write.py could not set; this is a whole top-level mapping that verb_set writes through the gate, and the gate seeing it is the point. The mint_id stays the hand-typed 6a1f2c3d4e5b60718a9b0c1d2e3f4051: a mint id is assigned once (goal:g2.5) and write.py refuses PROTECTED keys; recorded as-is, not repaired.
<!-- THOUGHT:END -->
