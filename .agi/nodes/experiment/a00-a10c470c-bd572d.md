---
id: experiment:a00-a10c470c-bd572d
mint_id: 08dbbe17ccaa4cc28a054cbc295758b3
type: experiment
parents:
  - hypothesis:l4-a-frontmatter-container-entry-escapes-the-yaml-line-break-code-points-nel-ls-ps-explicitly
next_edges: []
confidence: 0.9
edited_by: a00-31e60eca
evidence_runs:
  - experiment:a00-a10c470c-bd572d
loop: hypothesis:l4-a-frontmatter-container-entry-escapes-the-yaml-line-break-code-points-nel-ls-ps-explicitly@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 8e21214dbbfca4eb
season: 2
title: A00 a10c470c bd572d
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a10c470c-bd572d

## Experiment

Closure of hypothesis:l4-a-frontmatter-container-entry-escapes-the-yaml-line-break-code-points-nel-ls-ps-explicitly — a g15 CLAIM, so build-then-prove, not measure-and-report.

**Pre-fix measurement (the defect is real):**

`extensions/agi/bin/node_writer.py:338` rendered a list-of-dict frontmatter entry as `json.dumps(i, ensure_ascii=False)`. json.dumps emits U+0085 (NEL), U+2028 (LS) and U+2029 (PS) LITERALLY (JSON does not require escaping them). Feeding each through `render_frontmatter` -> `yaml.safe_load` (frontmatter.py:55/67, PyYAML, YAML 1.1) gave:

```
0x85  round-trip same? False | got= ' '      <- U+0085 folded to a SPACE (lossy)
0x2028 round-trip same? True
0x2029 round-trip same? True
0x2014 round-trip same? True                 <- em-dash control fine
```

Only NEL is measurably lossy in this PyYAML — YAML 1.1 treats it as a line break and folds it to a space. LS/PS happen to round-trip here, but they are equally line-break code points in YAML 1.1; escaping all three is the spec-correct, library-version-proof claim.

**Implemented (the claim):** added `_escape_yaml_linebreaks()` + a three-entry `_YAML_LINEBREAK_ESCAPES` table (`\u0085`, `\u2028`, `\u2029`) in node_writer.py, wired into the json.dumps site at :338. Every other non-ASCII code point stays literal.

**Post-fix round trip (same harness):**

```
0x85   -> 'k:\n  - {"name": "\\u0085"}'   round-trip TRUE
0x2028 -> '..."\\u2028"}'                    round-trip TRUE
0x2029 -> '..."\\u2029"}'                    round-trip TRUE
0x2014 -> '..."—"}'  em-dash stays literal, not re-escaped
0x41   -> '..."A"}'   ASCII untouched
```

**Tests:** added one parametrized round trip over the three code points (asserts the parsed value is unchanged AND the literal code point never survives into the rendered frontmatter) plus a falsifier parametrized over em-dash/ASCII (asserts they render literally). SL7.43 tests untouched.

```
python3 -m pytest extensions/agi/tests/test_node_writer.py -q
80 passed in 1.11s   (75 prior + 5 new)
```

## Evidence

- PRE-FIX: `json.dumps({'name': chr(0x85)}, ensure_ascii=False)` -> `'{"name": "\x85"}'` (literal NEL), and `yaml.safe_load` read it as a space.
- PRE-FIX: `render_frontmatter({'k':[{'name':chr(0x85)}]})` -> `'k:\n  - {"name": "\x85"}'`, round-trip parsed to `' '` — the loss.
- POST-FIX: same input -> `'k:\n  - {"name": "\\u0085"}'`, parsed back to chr(0x85) byte-identical.
- POST-FIX falsifiers: em-dash `—` and `A` both remain literal in the rendered text (`present in text`), single line, round-trip identical.
- `python3 -m pytest extensions/agi/tests/test_node_writer.py -q` → `80 passed` (exit 0); tier-gate showed only a phantom-record skip note, no failures.

## Agent Notes
Built g15 claim: node_writer._render_value now escapes YAML-1.1 line-break cps U+0085/U+2028/U+2029 in the json.dumps(ensure_ascii=False) site; NEL was measurably lossy (folded to space), now round-trips byte-identical; em-dash/ASCII stay literal; 5 new tests, 80 pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEWED BY PARENT a00-31e60eca (SL7.51): accepted, no change to the body.

(1) WHAT THE BRIEF SAID: the target hypothesis is a FIX-ONLY goal:g13.1 node whose claim is that node_writer.py:338 renders a list-of-dict frontmatter entry via json.dumps(i, ensure_ascii=False), which emits U+0085/U+2028/U+2029 literally, and that a string carrying one of them is "split across two YAML lines on the next read"; the demanded fix is a post-process replace table at the json.dumps site plus a three-code-point round-trip test.

(2) WHAT THE MACHINE ACTUALLY DOES, built and run here: the kid added _YAML_LINEBREAK_ESCAPES + _escape_yaml_linebreaks() and wired it into the dumps site (now node_writer.py:361). I re-ran the check myself, not the kid harness: for each cp, render_frontmatter({"rows":[{"name":"a"+chr(cp)+"b"}]}) -> full text -> frontmatter.read_frontmatter. Result: 0x85 roundtrip True literal_in_render False; 0x2028 True/False; 0x2029 True/False; em-dash stays literal and round-trips; render(parse(render(x))) == render(x) (fixpoint, so no escape churn on repeated writes). pytest extensions/agi/tests/test_node_writer.py -> 80 passed. The kid 5 new tests include the falsifier parametrization (em-dash, ASCII stay literal).

(3) THE NEAR MISS the kid avoided and the one the claim over-states: a fragment that escapes the VALUE instead of the json.dumps OUTPUT double-escapes (\\u0085 -> YAML reads a literal backslash) and would have failed the fixpoint check above; the kid escaped the output. Conversely the claim enumerates three code points "split across two YAML lines" — on THIS box (PyYAML 6.0.3, YAML 1.1) only NEL is measurably lossy (folded to a space); LS/PS already round-tripped byte-identical pre-fix, measured before the fix and reported honestly in the body. Escaping all three is still the spec-correct and library-version-proof choice, and the em-dash control confirms no over-escaping, so the claim stands as an implemented behaviour; only its "one of them" phrasing reads as broader than the measurement supports, and the body does not repeat that over-claim.

(4) DEVIATION: none. Scope held to _render_value JSON site + test_node_writer.py; the adjacent literal-NEL path through _scalar() is a real but separate defect and was correctly left outside this node.
<!-- THOUGHT:END -->
