---
id: goal:s25
mint_id: c205acee53484885b8e5ae817e8f6fa8
type: goal
parents:
  - goal:g15
confidence: 0.8
edited_by: season.py
goal_id: S25
goal_kind: short-term
heading_level: 2
origin: goals-doc
season: 1
seeds: []
status: complete
tags:
  - goal
  - root
  - short-term
thought_session: season
title: "S25: `build_corpus` resolves whatever directory it is handed"
---
**`goal:s10`'s second fix, which that goal said to do "regardless of (1)" and
which never landed.** Split out on 2026-09-02 when S10 retired: its title
asserts a file count that is now zero, so it can no longer carry a live defect
honestly.

`evidence_gate.build_corpus(nodes_dir)` takes a directory and `rglob`s it for
`*.md`, returning every `id:` it finds. Called on `nodes/` it is correct.
Called on a project root it returns whatever else is lying there — measured at
the time as **657 ids vs 29,582**, the pre-purge gamed corpus resurrected. A
verdict citing a deleted node as `evidence_runs` would resolve against it and
pass the gate, silently undoing `goal:g3.1`'s fix.

**The engine is not affected today, and that was checked rather than assumed:**
all three real callers pass `root / "nodes"`. But *"the correct argument is
passed at all three current call sites"* is a property of today's callers, not
of the function, and the incorrect call takes one line to write. The fuel is
gone; the mechanism is not.

**A gate that cannot verify must fail closed** — the function already argues
exactly this for a `None` corpus and should hold itself to it for a wrong
directory. Either refuse a non-`nodes/` root, or resolve `nodes/` itself from
the project root rather than trusting the caller.

## Falsifier

Call `build_corpus` on a project root containing stray `.md` files with `id:`
frontmatter outside `nodes/`. It refuses, or returns only the `nodes/` ids —
never the union. Then confirm the three live callers still pass.