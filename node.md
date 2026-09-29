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
`write.py create config` is REFUSED at the spawn gate ("no active schema for type 'config'": [config].md is `structural: true`, spawn_gate.py:996-998; belam 12:1xZ). `--dry-run` never reaches the gate, and `--no-spawn-gate` stamps the node unreviewed. So no create route exists. The .geometry config nodes were born as files written directly: config:workflows by the Prime in 555dc2a59 (one 80-line add); config:vetoes and config:key-authority in rounds. The sanctioned route for such a file is write.py's `adopt` verb: "mint a first mint_id for a node written outside node_writer" (node_writer.repair_mint, no spawn gate; the config written_by admits the Prime). Proven end to end on a throwaway project 09-29 (file -> adopt -> check_formation PASS `active doc:council-loop g7.16.1` wake 0):
```
cat > .agi/nodes/.geometry/formations.md <<'EOF'
---
id: config:formations
type: config
parents:
  - goal:g7.16
next_edges: []
active: doc:council-loop
templates:
  doc:council-loop: g7.16.1
  doc:l4-formation-2-texas-two-step: g7.16.2
  doc:formation-local-town: ""
  doc:l4-formation-1-prime-only: ""
  doc:l4-formation-3-hybrid-gradual-expansion: ""
  doc:l4-formation-4-full-activation: ""
---
# config:formations

The run-mode switch (goal:g7.16). `active` = ONE formation template; `templates` = template -> the goal it serves.
Switch: write.py config:formations 'set active doc:<id>'. Read-back: verification.py `formation` check (rotation, full).
EOF
python3 extensions/agi/bin/write.py config:formations adopt
python3 -c "import sys; sys.path.insert(0,'extensions/agi/bin'); import verification; from pathlib import Path; r=verification.check_formation(Path('.agi')); print(r.status, r.note, r.number)"
git add .agi/nodes/.geometry/formations.md && git commit -m 'config:formations: the formation cell (goal:g7.16.1.1.5)' -- .agi/nodes/.geometry/formations.md
python3 extensions/agi/bin/grid.py commit --all   # on season2/main only (director template §2); elsewhere the grid_sync cron versions it
```
Expected read-back: `PASS active doc:council-loop g7.16.1 {'wake': 0}`. Until the cell exists, the check reads SKIP on the live graph.

## Falsifier
1. `pytest extensions/agi/tests/test_formation_readback.py` exits 0: no cell SKIP · '' / two / unregistered FAIL · one PASS whose wake list holds the THOUGHT mark and not the body mention, `g7.16.20` or a deprecated node.
2. Negative: once the cell exists and names doc:l4-formation-2-texas-two-step, `verification.check_formation` prints exactly one `active` line and one `wake` line per LIVE node whose THOUGHT carries `parked: formation g7.16.2`: 16 at 3e0e340cb+ (14 hypotheses + goal:g7.32.5 + goal:g7.33.19; deprecated excluded).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Residue 24+ (belam 11:54Z, run 12:1xZ): the owed create config command was REFUSED at the spawn gate ([config].md is structural, so it has no active schema); my earlier --dry-run proof never reached the gate. That is the near miss: a dry-run proves the verbs parse, never the gate (director template §2 'dry-run != gate'). Corrected: the .geometry config nodes were born as directly written files (config:workflows 555dc2a59 by the Prime), and write.py adopt is the sanctioned first-mint for such a file, with no gate bypass. Proven on a throwaway project: file -> adopt -> check_formation PASS. git add now precedes the commit and grid.py commit --all follows it, on season2/main only per the director template (residue 24, re-mur wf_aa3f01d4-2aa). Earlier residues 15-18 (DG3, 6d00b84fd) stand: wake 16 live, deprecated excluded; CEILING deviation 29 added (24 code) / 69 test lines vs 25 / 30, each fixture a measured trap.
<!-- THOUGHT:END -->
