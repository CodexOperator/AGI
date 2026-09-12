---
id: hypothesis:l4-stitch-and-level3-project-resolve-the-graph-root-or-refuse-by-name-and-verify-prints-its-count
mint_id: b8a9e38eb9b449b384db85a02a2b91fb
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-prepare-check-2-reads-the-index-blob-and-the-writers-marker-guard-is-the-readers-regex
next_edges: []
edited_by: sensei-director
scaffold_hash: e15309537021e5c4
season: 2
testable_claim: "goal:g15 FIX-ONLY node, mur-SL2.16 (Prime XV 08:06Z, by name) line (4) — SL7.17 evidence gap. Cite lines at 2451606d0; re-measure on your base. MEASURED: SL7.17's kid (experiment:a00-483c2fe4-5b0b23) cited `stitch.py --project . --verify: clean, rc 0` as evidence for clause (d) (the dropped frontmatter pre-check is byte-identical) — but `stitch.py --project <p>` resolves `<p>/nodes/build` LITERALLY (stitch.py 935; level3.py 120 the same), so from the repo root `--project .` looks for `./nodes/build`, finds ZERO nodes, and reports clean: the evidence measured nothing. The graph lives at `<root>/.agi/nodes/` (G11 layout; `bin/locations.py` is the one resolver). CLAIM: (a) `--project` in stitch.py and level3.py resolves the GRAPH ROOT through `locations` (nearest enclosing `.agi/` from the given path, or the path itself when it IS a graph root holding `nodes/`), never a literal `<p>/nodes`; a path that resolves to no graph root is REFUSED by name (`ERR: no graph root at or above <p> (no .agi/ and no nodes/)`, exit 2) — never a silent zero-node clean; (b) `--verify` prints the node count it verified (`verified N build node(s)`) so a zero reads as zero; (c) the SL7.17 clause (d) evidence is RE-RUN on the real graph (from the repo root, `stitch.py --project . --verify` → verified 300 build nodes, clean) and recorded in the new kid node with the count; (d) tests: `--project <tmp repo root with .agi/nodes/build/…>` resolves and counts; `--project <tmp dir with neither>` refuses by name, exit 2; the count line asserted. FALSIFIERS: `--project .` from the repo root still reads zero nodes; a rootless path exits 0; the re-run evidence is missing or reports zero; any existing stitch/level3 test changes assertion beyond the rootless-path one. TESTS: test_stitch.py test_level3*.py test_frontmatter.py test_snapshot_goals*.py test_bin_help_smoke.py with neighbours. RULES: merge, never rebase; `stitch.py --from-grid`/`--out` unchanged; the render --check round trip byte-identical. FILE SCOPE: stitch.py + level3.py `--project` resolution and the verify count print, tests; the new kid node carries the re-run. EXCLUDED: rotate.py, write.py, send.py, the frontmatter module. CEILING: 1 parent, up to 2 kids, small."
thought_session: sensei-director-genIX-L9
title: stitch.py/level3.py --project resolve the graph root (never a literal <p>/nodes) or refuse a rootless path by name; --verify prints the node count; SL7.17's clause (d) evidence re-run on the real graph
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-stitch-and-level3-project-resolve-the-graph-root-or-refuse-by-name-and-verify-prints-its-count

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
