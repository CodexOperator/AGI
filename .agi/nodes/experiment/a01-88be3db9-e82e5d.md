---
id: experiment:a01-88be3db9-e82e5d
mint_id: b1bedea83802489baf3d5926ecd402b9
type: experiment
parents:
  - hypothesis:a00-abd94427-d2294b
next_edges: []
confidence: 0.85
scaffold_hash: 0ff59902f8ba82c1
title: Falsifier grep single-pass doc sweep
verdict: inconclusive_lean_proved:85
---
# experiment:a01-88be3db9-e82e5d

## Experiment

Tested hypothesis:a00-abd94427-d2294b: can a falsifier grep (retired names: render-context.py, payloads/, grid.py checkout as live command, context/kits) drive a single-pass doc sweep to zero across QUICKSTART.md, CLAUDE.md, skills/agi/SKILL.md, and HANDOFF.md §5?

**Protocol:**
1. Run grep -n -E '(render-context\.py|payloads/|grid\.py checkout|context/kits)' on all four target files
2. Classify each hit: inside a "retired marker" sentence (explicit retired label, "gone", "retired", "Before goal:g11" framing, or under a "Retired" heading) = pass; outside = fail
3. Tally unique targets and assess tractability of a single-pass sweep

**Results — raw hits: 14 occurrences across 3 of 4 files (HANDOFF.md: 0)**

| File | Line | Term | Status | Marker? |
|---|---|---|---|---|
| QUICKSTART.md | 29 | render-context.py | STALE | no — describes pre-L1 driver.sh path check |
| QUICKSTART.md | 108 | render-context.py | STALE | no — ASCII pipeline diagram shows retired step |
| CLAUDE.md | 12 | payloads/, grid.py checkout | PASS | "It is gone" marks retired |
| CLAUDE.md | 60 | context/kits | PASS | "(retired 2026-09-03, L1.09)" explicit |
| CLAUDE.md | 207-208 | grid.py checkout, payloads/ | PASS | "Before goal:g11" historical framing |
| CLAUDE.md | 228-229 | payloads/, grid.py checkout | PASS | Under "Retired" heading |
| CLAUDE.md | 271 | render-context.py | BORDERLINE | Live warning ("NEVER create"); no retired marker |
| CLAUDE.md | 285 | context/kits | BORDERLINE | Cross-ref to other-project hazard; no retired marker |
| SKILL.md | 56 | grid.py checkout | PASS | "gone — never run it" marks retired |
| SKILL.md | 304-305 | payloads/, grid.py checkout | PASS | Under "Retired" heading |
| SKILL.md | 448 | render-context.py | BORDERLINE | Safety rail warning; no retired marker |

**Key findings:**

1. **Unique stale targets: 2** (both in QUICKSTART.md — render-context.py references that describe pre-L1 state without retired marker). Well under hypothesis's 20-target upper bound.

2. **Falsifier produces 3 false positives** — CLAUDE.md:271, CLAUDE.md:285, SKILL.md:448 reference retired names as part of semantically important live warnings ("don't recreate this dangerous file"). These are current content, not stale drift. The goal's falsifier as written ("any hit outside a sentence that marks it retired") does not say how to score prohibition sentences or live cross-project warnings, so the gate is under-specified, not just the docs.

3. **Single-pass sweep is feasible — 2 fixes, not 5** — the 2 stale QUICKSTART.md refs get updated/replaced (pipeline diagram L108; quoted driver.sh check L29, whose line number is also stale — the real check sits near driver.sh:240 and only as a legacy fallback behind inject.py). The 3 borderline warnings keep their text; they need the *falsifier's spec* to add an exclusion for live warning sentences, not a "(retired)" marker in the docs. CLAUDE.md:285 in particular must NOT be marked retired — it warns that the hazard is live for other projects, and tagging it retired would assert the opposite of what it says.

4. **No stale reference is semantically important enough to keep as-is** — the 2 QUICKSTART hits describe pre-L1 state in prose that should be updated to current; the 3 borderline hits are live warnings that stay exactly as written.

**Conclusion:** Hypothesis is directionally confirmed. The drift is shallow (tractable set of retired names, not structural rewriting needed). The falsifier correctly catches real stale content (QUICKSTART.md) but also flags live warnings by design — the sweep must add retired markers to the latter. A single-pass sweep is practical and would take ~5 minutes.

## Evidence

Falsifier command: `grep -n -E '(render-context\.py|payloads/|grid\.py checkout|context/kits)' QUICKSTART.md CLAUDE.md skills/agi/SKILL.md HANDOFF.md`

Full output:
```
CLAUDE.md:12:payloads/
CLAUDE.md:207:grid.py checkout
CLAUDE.md:208:payloads/
CLAUDE.md:228:payloads/
CLAUDE.md:229:grid.py checkout
CLAUDE.md:271:render-context.py
CLAUDE.md:285:context/kits
CLAUDE.md:60:context/kits
QUICKSTART.md:108:render-context.py
QUICKSTART.md:29:render-context.py
skills/agi/SKILL.md:304:payloads/
skills/agi/SKILL.md:305:grid.py checkout
skills/agi/SKILL.md:448:render-context.py
skills/agi/SKILL.md:56:grid.py checkout
```

**Sibling run:** experiment:a00-e1482929-779b16 ran the same census independently. Raw hit counts agree exactly (14 hits, same lines). It classifies the 3 live-warning hits as retired markers — a more generous read than this node's; the under-specification is recorded in both nodes.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-92d87f34): grep output verified line-for-line against an independent run — 14 hits, all match, HANDOFF.md clean. Verdict kept at inconclusive_lean_proved:85 (consistent with confidence 0.85). Body corrected: the "add retired markers to 3 warnings" prescription was wrong for CLAUDE.md:285 (a live cross-project hazard — marking it retired would assert its opposite) and partly wrong for the other two (prohibition sentences are the warning's value, not stale text). The sweep is 2 doc fixes plus a spec amendment to the falsifier, not 5 doc edits. Sibling cross-reference added.
<!-- THOUGHT:END -->


## Agent Notes
Falsifier grep on 4 target files: 14 raw hits, 2 genuinely stale (QUICKSTART.md), 3 borderline live warnings the falsifier spec must exclude, 6 properly marked. Shallow drift confirmed — single-pass sweep tractable under 5 targets. Falsifier produces false positives on live warnings referencing retired names.
