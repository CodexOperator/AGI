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
```
python3 extensions/agi/bin/write.py create config formations --parent goal:g7.16 --set active=doc:council-loop --set 'templates={"doc:council-loop": "g7.16.1", "doc:l4-formation-2-texas-two-step": "g7.16.2", "doc:formation-local-town": "", "doc:l4-formation-1-prime-only": "", "doc:l4-formation-3-hybrid-gradual-expansion": "", "doc:l4-formation-4-full-activation": ""}'
```
Until then the check reads SKIP on the live graph.

## Falsifier
1. `pytest extensions/agi/tests/test_formation_readback.py` exits 0: no cell SKIP · '' / two / unregistered FAIL · one PASS whose wake list holds the THOUGHT mark and not the body mention or `g7.16.20`.
2. Negative: once the cell exists, `verification.check_formation` prints exactly one `active` line and 14 `wake` lines when doc:l4-formation-2-texas-two-step is active (row E's 14 park marks).
