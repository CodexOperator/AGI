---
id: experiment:a00-e1482929-779b16
mint_id: eef31064f9654fb39025d0146b0d7fcf
type: experiment
parents:
  - hypothesis:a00-abd94427-d2294b
next_edges: []
confidence: 0.7
scaffold_hash: 7450616cb93005e3
title: Falsifier pre-sweep hit census — detection half of the S33 falsifier
verdict: inconclusive_lean_proved:70
---
# experiment:a00-e1482929-779b16

## Experiment

Ran falsifier grep across all four target files (pre-sweep census; the sweep itself is a later step) (QUICKSTART.md, CLAUDE.md, skills/agi/SKILL.md, HANDOFF.md) searching for retired names: `render-context.py`, `payloads/`, `grid.py checkout`, `context/kits`. Categorized each hit as either inside a retired-marker sentence (pass) or outside one (fresh hit — falsifier fails).

**Command:**
```bash
grep -n 'render-context\.py' QUICKSTART.md CLAUDE.md skills/agi/SKILL.md HANDOFF.md
# repeat for payloads/, grid.py checkout, context/kits
# then inspect ±2 lines context for retired-marker classification
```

**Raw hit counts per term per file:**

| Term | QUICKSTART.md | CLAUDE.md | skills/agi/SKILL.md | HANDOFF.md |
|---|---|---|---|---|
| `render-context.py` | 2 | 1 | 1 | 0 |
| `payloads/` | 0 | 3 | 1 | 0 |
| `grid.py checkout` | 0 | 2 | 2 | 0 |
| `context/kits` | 0 | 2 | 0 | 0 |

**After retired-marker classification:**

| File | Total hits | In retired marker | Fresh hits |
|---|---|---|---|
| QUICKSTART.md | 2 | 0 | **2** (`render-context.py` L29, L108) |
| CLAUDE.md | 8 | 8 | **0** |
| skills/agi/SKILL.md | 4 | 4 | **0** |
| HANDOFF.md | 0 | 0 | **0** |

**Fresh hit detail:**

1. **QUICKSTART.md L29** — `render-context.py` in code block quoting `driver.sh:99`. Surrounding text describes a "live, unfixed defect" — the print warns about stale script overrides but does NOT mark `render-context.py` as retired. The line-number in the quote (99) is itself stale (actual driver.sh line is ~240).

2. **QUICKSTART.md L108** — `render-context.py` in the "loop, one iteration" pipeline diagram as `render-context.py graph -> context/INJECTION.md`. The actual driver replaced this with `inject.py` on 2026-09-03 (L1.05). The pipeline diagram is stale.

## Evidence

**Falsifier grep raw output:**

```
=== render-context.py ===
QUICKSTART.md:29:  driver.sh:99   [[ -x "$PROJECT_ROOT/bin/render-context.py" ]] && RENDER_PY=...
QUICKSTART.md:108:  render-context.py        graph -> context/INJECTION.md (bounded ASCII map)
CLAUDE.md:271:  `.agi/bin/render-context.py`.** `driver.sh` resolves the project root
skills/agi/SKILL.md:448:- **Never create ... or `bin/render-context.py`** — that's `.agi/bin/*.py`...

=== payloads/ ===
CLAUDE.md:12:carry bytes across that boundary: `payloads/` as a staged checkout, `grid.py
CLAUDE.md:208:under `payloads/`, run the tests against that staged copy, `grid.py commit
CLAUDE.md:228:- **`payloads/`** — the staged checkout. Gone; the payload *is* the source file.
skills/agi/SKILL.md:304:- `payloads/` — the staged checkout. Gone; the payload *is* the source file.

=== grid.py checkout ===
CLAUDE.md:207:**Before `goal:g11`:** an engine change was `grid.py checkout --all`, edit
CLAUDE.md:229:- **`grid.py checkout`** — nothing to check out. **Never run it.**...
skills/agi/SKILL.md:56:**`grid.py checkout` is gone — never run it.**...
skills/agi/SKILL.md:305:- `grid.py checkout` — nothing to check out. **Never run it**...

=== context/kits ===
CLAUDE.md:60:| *(retired 2026-09-03, L1.09)* `.agi/context/kits/`...
CLAUDE.md:285:  keeps a live `context/kits/` + `context/plans/build-site.md` pair: there,
```

**Retired-marker classification rule:**
- CLAUDE.md `payloads/` (L12): "Before goal:g11 — It is gone" → retired ✓
- CLAUDE.md `context/kits` (L60): "*(retired 2026-09-03, L1.09)*" → retired ✓
- CLAUDE.md `payloads/`+`grid.py checkout` (L207-210): "Before goal:g11 — That whole pipeline computed nothing" → retired ✓
- CLAUDE.md `payloads/`+`grid.py checkout` (L228-231): Under retired bullet list → retired ✓
- CLAUDE.md `render-context.py` (L271): Under "NEVER create" safety rail — forbids creation → retired ✓
- CLAUDE.md `context/kits` (L285): "applies to any other project" context — not about this project → retired ✓
- SKILL.md `grid.py checkout` (L56): "is gone — never run it" → retired ✓
- SKILL.md `payloads/`+`grid.py checkout` (L304-305): Under "Retired" heading → retired ✓
- SKILL.md `render-context.py` (L448): Under "Never create" safety rail → retired ✓
- QUICKSTART.md L29: Describes "live, unfixed defect" — hazard warning, not retired marker → **fresh**
- QUICKSTART.md L108: In pipeline diagram with no retirement note → **fresh**

**Key findings:**
- **2 fresh hits total** (both `render-context.py` in QUICKSTART.md), well under 20-target threshold
- **1 unique retired name** with stale references (`render-context.py`)
- **0 stale references** in CLAUDE.md, SKILL.md, or HANDOFF.md
- Both fixes are straightforward: update pipeline diagram (L108) and update code block + line numbers (L29)
- The stale reference at L29 is embedded in a hazard warning about stale scripts; replacing `render-context.py` with `inject.py` in the quoted code block would preserve the warning's value
- No stale reference carries independent semantic importance that would be lost by updating it

**Sibling run:** experiment:a01-88be3db9-e82e5d ran the same census independently. Raw hit counts agree exactly (14 hits, same lines, HANDOFF.md clean). It classifies CLAUDE.md:271, CLAUDE.md:285 and SKILL.md:448 as BORDERLINE live warnings, not retired markers — a stricter read than this node's classification. The falsifier as specified in goal:s33 is under-specified: a "NEVER create" prohibition sentence is not literally a sentence that marks the name retired, and CLAUDE.md:285 is a live warning about other projects where nothing is retired. Agreement on raw counts across two independent runs is the strongest evidence in either node.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-92d87f34): raw census verified against an independent grep — all 14 lines match. Lean demoted 80 -> 70 to match the node's own confidence (0.7) and because this run executes only the detection half of the falsifier: the sweep itself was never run, and this node's classification of the three live-warning hits as "retired" is the generous read; the sibling run calls them borderline. Title was a scaffold placeholder.
<!-- THOUGHT:END -->


## Agent Notes
Ran falsifier grep across QUICKSTART.md CLAUDE.md skills/agi/SKILL.md HANDOFF.md for retired names (render-context.py, payloads/, grid.py checkout, context/kits). Fresh hits: 2 (both render-context.py in QUICKSTART.md L29 pipeline code block, L108 pipeline diagram). All CLAUDE.md/SKILL.md hits properly inside retired-marker sentences. Hit set tractable (<20 targets, 1 unique name). Sweep not executed end-to-end — evidence supports approach but incomplete to claim proved.
