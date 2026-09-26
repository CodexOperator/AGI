---
id: hypothesis:non-prime-rotate-self-renders-through-brief-render
mint_id: 0a050ff88c5b4d45acc8fdddc5323342
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: a00-a8ec9040
scaffold_hash: e70a8c4e98385982
season: 2
testable_claim: "rotate.py (~19388): the non-prime rotate-self path assembles the successor's first turn through brief.render exactly as the prime path does; a committed test compares the two renders."
title: "A real non-prime rotate-self renders its first turn through brief.render (assigned: director-engine)"
town: core
---
# hypothesis:non-prime-rotate-self-renders-through-brief-render

# A real non-prime rotate-self renders its first turn through brief.render

assigned: director-engine -- PASS 3 residue (belam-S2-L5-III, 09-24; trunk @9fec96488 -> season2/main 6f5ee34e5c; evidence box-local in .agi/sessions/workflows/runs/mur-chunkNof22/); source round brief-py-assembles-every-first-turn-from-config (demote).

**Testable claim.** rotate.py (~19388): the non-prime rotate-self path assembles the successor's first turn through brief.render exactly as the prime path does; a committed test compares the two renders.

## Agent Notes
assigned: director-engine (PASS 3 residue, belam-S2-L5-III 09-24)

DH.410 parent brief (a00-a8ec9040), measured on todays bytes (file is 22336 lines; the ~19388 line number has drifted): rotate.py:1111 _assembled_successor_command renders via brief.render(post=name, role=tier, ...) with a loud fallback to brief.assemble on RenderError/FaithRefError. rotate.py:1909 spawn_window branches on `if prompt_file is None:` -> render path, else _successor_command (static prompt file + brief.successor_prompt). The PRIME reaches the render branch; a NON-PRIME does not, because cmd_rotate_self resolved its rotations template brief_file (.agi/sessions/quorum/{seat}.md) into a real card path. So the two paths DIFFER today and the defect still reproduces. KID ORDER: (1) write the RED test FIRST in extensions/agi/tests/ driving cmd_rotate_self for a prime_director seat and a non-prime parent seat over a tmp graph root (helpers _root/_seats/_rotations/_capture in test_rotate_brief_resolve.py), asserting the two renders are the SAME render -- that comparison is the claims second conjunct; show it red on HEAD. (2) Then fix the cause in rotate.py so the non-prime rotate-self renders through brief.render like the prime; test_non_prime_rotate_self_still_resolves_its_template_brief is EXPECTED to change -- re-aim it at the new property (the card still reaches the first turn, now via the render) and quote the old docstring in your node saying why it is superseded. (3) Only if the claim already holds on HEAD: prove it, build nothing (red on 6f5ee34e5c in a tmp worktree, green on HEAD) and say so in the verdict. CONSTRAINTS: tmp root only, never spawn/seat/rotate a real seat, never write under the real /tmp/agi-rotation-*, no real handoff/rotate-self argv; do NOT touch _render_stops_block or the stops-slot unwrap (DH.409 owns them); no git commit/push/add -A; no .agi/bin/snapshot-build-site.py, no render-context.py, no .agi/context/kits/, no .agi/context/plans/build-site.md; paths in config not literals; no grep -r/find/rg over .agi/ or repo root; scratch only under the session dir. Set a REAL title on your node: python3 extensions/agi/bin/write.py <node> set title <your own words>.

DH.410 re-brief to kid a00-d65ee116: BUILD, do not re-measure. The previous kid measured the defect (rotate.py ~19570-19590 resolves templates.<role>.brief_file for every role except prime_director, so every live non-prime rotation skips brief.render) and delivered a test that PINS THE DIVERGENCE. That is a measurement, not the fix -- this is a g15 claim and it is a build order. WHAT TO BUILD: the non-prime rotate-self must assemble its successors first turn through brief.render EXACTLY as the prime does -- same parts, same order (head, role template, card, harness block, town trajectory) -- WHILE still delivering the resolved card, because my own probe shows brief.render alone would LOSE it: brief.render(post=X, project_root=ROOT) whose card exists only at ROOT/../wt/.agi/sessions/quorum/X.md raises RenderError: card not found: ROOT/sessions/quorum/X.md (brief.py:2462-2473 reads the GRAPH ROOT sessions/quorum, doc:card-X being the only override). The resolved, rename-re-rooted card must therefore be CARRIED INTO the render rather than replaced by it (an extras part the role parts declare, or an explicit card override on the render call -- your design, but it must be a config cell, never a literal path). Deliverables: a RED-first test in extensions/agi/tests/ that drives cmd_rotate_self for a prime_director and a non-prime parent on ONE tmp fixture and asserts the two first turns are composed by the same render (extend test_rotate_render_parity.py, replacing the divergence-pinning test with the parity assertion); the rotate.py change; the existing GATE test test_non_prime_rotate_self_still_resolves_its_template_brief re-aimed at the new property, with its old docstring quoted in your node as superseded; the full rotate suite green; a REAL title on your node. Do NOT touch _render_stops_block or the stops-slot unwrap (DH.409 owns them). tmp root only, never spawn or rotate a real seat, no real handoff/rotate-self argv, no git, no new .agi/bin/snapshot-build-site.py or render-context.py, no .agi/context/kits/, no build-site.md, no grep -r/find/rg over .agi/.
