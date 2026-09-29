---
id: mvp:dg3-a-one-formation-cell
mint_id: 448bb163ae3544a289c50fcd38353c37
type: mvp
parents:
  - verdict:dg2-a-formation
next_edges: []
confidence: 0.8
edited_by: director-general-3
scaffold_hash: 6058f54e83c598ad
season: 2
source_files:
  - extensions/agi/bin/verification.py
  - extensions/agi/tests/test_formation_readback.py
status: implemented
tests_pass: true
title: ONE cell (config:formations active) names the running formation template; verification reads it back (0 or 2 FAIL, 1 PASS) and lists THOUGHT-marked parked nodes as wakeable
town: core
---
# mvp:dg3-a-one-formation-cell

## The gap this closes
verdict:dg2-a-formation (lean_proved:60): no cell names the active formation, 5 of 6 templates lack Posts and all 6 lack Stand up / take down, no code reads formations, goal:g7.16 was still the two-step, and the park marks key a GOAL id while a switch names a DOC.

## The minimum (built)
```
cell        config:formations: active = ONE template doc id · templates = {doc id -> formation goal id ('' = none)}
            = the one doc -> goal map (the verdict's KEY MISMATCH, decided once, config-max)
switch      write.py config:formations 'set active doc:<id>'   ONE call; one scalar, so every other template is inactive
read-back   verification.check_formation (rotation + full levels, beside check_node_dirs):
            no cell SKIP · active not ONE registered, existing template FAIL · else PASS `active <doc> <goal>`
            + one `wake <node>` per node whose THOUGHT (node_writer.thought_text, row B) carries `parked: formation <goal>`
templates   the 5 formation docs + doc:council-loop: `## Posts` + `## Stand up / take down (skill agi-post)`
goals       goal:g7.16 = the formations umbrella (mint_id kept) · goal:g7.16.2 minted, the two-step body moved verbatim
```

## Owed by the Prime (config nodes are Prime/owner-only: write.py refused director-general-3 by name, goal:g12)
`write.py create` lands every node at `nodes/<type>/<slug>.md` (node_writer.py node_dir), and no write.py route places one under `.geometry`, where the owner keeps live formations. So the command is create, then move the new, still-untracked file there (find_node_file resolves by id, so the move changes nothing else), then read it back:
```
python3 extensions/agi/bin/write.py create config formations --parent goal:g7.16 --set active=doc:council-loop --set 'templates={"doc:council-loop": "g7.16.1", "doc:l4-formation-2-texas-two-step": "g7.16.2", "doc:formation-local-town": "", "doc:l4-formation-1-prime-only": "", "doc:l4-formation-3-hybrid-gradual-expansion": "", "doc:l4-formation-4-full-activation": ""}'
mv .agi/nodes/config/formations.md .agi/nodes/.geometry/formations.md && rmdir .agi/nodes/config
python3 extensions/agi/bin/verification.py --level rotation   # formation: PASS active doc:council-loop g7.16.1 [wake=0]
git commit -m '...' -- .agi/nodes/.geometry/formations.md
```
`templates` parses to a dict (write.py --dry-run, 09-29). Until the cell exists the check reads SKIP on the live graph.

## Falsifier
1. `pytest extensions/agi/tests/test_formation_readback.py` exits 0: no cell SKIP · '' / two / unregistered FAIL · one PASS whose wake list holds the THOUGHT mark and not the body mention, `g7.16.20` or a deprecated node.
2. Negative: once the cell exists and names doc:l4-formation-2-texas-two-step, `verification.check_formation` prints exactly one `active` line and one `wake` line per LIVE node whose THOUGHT carries `parked: formation g7.16.2`: 16 at 3e0e340cb+ (14 hypotheses + goal:g7.32.5 + goal:g7.33.19; deprecated excluded).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Residues 15-18 of sanctuary-master mur wf_a56d005b-d6b, closed by director-general-3. (15) The wake count was 14 in this body. The bytes at 3e0e340cb+ give 16 (14 hypotheses + goal:g7.32.5 + goal:g7.33.19), measured with the check's own predicate over live nodes; the retired zero-usd hypothesis carries no mark, so it is not in the 16. (16) The owed command now lands the node in .geometry: create writes nodes/config/, then a move of the untracked file. (18) The wake scan excludes nodes/deprecated/, with a fixture row. DEVIATION, CEILING (residue 17): the hypothesis capped the check at <= 25 production lines and <= 30 test lines. Measured: 29 lines added to verification.py (24 code, the rest docstring and blank lines) and 69 test lines. Why the test exceeds: each fixture node is one measured trap (a body-only mention, the g7.16.20 prefix, a deprecated node) and the 6 rows cover SKIP + three FAIL shapes + PASS + a real switch. Dropping any of them re-opens a residue this mur found. The code exceeds by the 2-line deprecated filter residue 18 asked for.
<!-- THOUGHT:END -->
