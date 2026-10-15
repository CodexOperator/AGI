---
id: experiment:a00-6b82217f-dbef27
mint_id: 8e2de109cf5240c78e26982e717ac4f0
type: experiment
parents:
  - hypothesis:l4-a-container-entry-in-frontmatter-round-trips-its-utf8-unchanged-through-every-write-verb
next_edges: []
confidence: 0.9
edited_by: sensei-director
evidence_runs:
  - experiment:a00-6b82217f-dbef27
loop: hypothesis:l4-a-container-entry-in-frontmatter-round-trips-its-utf8-unchanged-through-every-write-verb@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 93543d2412625eb6
season: 2
title: a list-of-dict frontmatter entry round-trips its non-ASCII byte-identical through every write verb (json.dumps ensure_ascii=False); a pre-escaped entry normalizes once
town: core
verdict: proved
---
# experiment:a00-6b82217f-dbef27

## Experiment

Built the g13.1 FIX claim (a one-keyword fix, one test): a list-of-dict
frontmatter entry carrying non-ASCII round-trips byte-identical through every
write.py verb, because the writer was escaping it.

**Measured pre-fix.** Reproduced in-process on the seat. `json.dumps(i)` at
`node_writer.py:338` uses the default `ensure_ascii=True`, so a first_turn-style
entry with a literal em-dash renders escaped:

    first_turn:
      - {"cmd": "print", "arg": "a\u2014b"}

`yaml.safe_load` of that line still yields the dict with the literal `—` (the
reader half understands both spellings), so the damage was write-side only: an
unrelated one-line edit re-rendered the whole frontmatter and silently rewrote
the unrelated entry's bytes.

**Applied the fix.** One keyword argument, exactly the ceiling the node set:
`node_writer.py:338` `json.dumps(i)` → `json.dumps(i, ensure_ascii=False)`. No
serializer redesign, no other call touched. The single-EOF rule at 876-877 was
left alone (explicitly out of scope).

**Added two tests** in `extensions/agi/tests/test_node_writer.py`, both
round-tripping through `nw.update_node` — the ONE routine every write verb
routes through (hypothesis cited this), so this equals a `write.py <id> note x`
round trip:
  - literal entry survives a write byte-identical (no `\u2014` appears);
  - a pre-escaped `\u2014` entry normalizes ONCE to the literal characters.

**Proved non-vacuous + on the built bytes.** Reverted the one line, ran the two
new tests → both FAILED exactly on the claim (equal/`a—b` assertions). Restored
the fix → both PASS. Full file runs green: test_node_writer.py 75 passed,
test_write.py (the verb layer) 99 passed.

## Evidence

Pre-fix render of a literal-em-dash container entry:
`'...first_turn:\n  - {"cmd": "print", "arg": "a\\u2014b"}'` — `\u2014` present
(needlessly escaped).

Pre-fix run against the new tests:
```
2 failed, 73 deselected   # both: escaped-entry / literal-entry assertions
```
Post-fix run against the new tests:
```
9 passed (utf8 + preescaped + existing serializer tests)
```
Full files:
```
test_node_writer.py ... 75 passed in 1.30s
test_write.py ......... 99 passed in 0.70s
```
config:rotations.md left untouched (out of scope — its four mixed entries
normalize on the next engine write of that node, per the hypothesis).

## Agent Notes
Added ensure_ascii=False at node_writer.py:338 json.dumps; two non-vacuous round-trip tests (literal survives, pre-escaped normalizes once). Confirmed both FAIL pre-fix, PASS post-fix; full files green (75 + 99).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-583d0c24, SL7.43) — ACCEPTED, verdict proved.

(1) WHAT THE INSTRUCTION SAID: "a list entry that is a container is rendered at node_writer.py:338 as json.dumps(i) with the default ensure_ascii=True, so every non-ASCII character inside a JSON-in-YAML entry is escaped on any write, related to the edit or not", with FILE SCOPE "node_writer.py — _render_value, that one json.dumps call only" and CEILING "one keyword argument, one test".

(2) WHAT THE MACHINE ACTUALLY DOES, measured on this base: node_writer.py:338 was EXACTLY json.dumps(i) (read pre-review at line 338); the staged diff changes only that call to json.dumps(i, ensure_ascii=False) — one call site, no other hunk. write.py:36 states "Every verb ends in node_writer.update_node", so the kid test routing through nw.update_node exercises the verb layer, not a proxy. Reproduced the escape directly: json.dumps({'cmd':'print','arg':'a—b'}) -> a\u2014b; with ensure_ascii=False -> a—b. RAN extensions/agi/tests/test_node_writer.py: 75 passed. The two new tests are non-vacuous: the literal test asserts the escape string "\\u2014" is absent from the file, which json.dumps(i) with the default cannot satisfy.

(3) NEAR MISS (counterfactual that satisfies the words and loses the mechanism): a kid could have made the em-dash survive by patching the READER (frontmatter.read_frontmatter) or by adding a post-render unescape pass keyed on the escape sequence, leaving the write path still escaping every non-ASCII container entry on every unrelated edit. The claim is a WRITE-SITE property — the entry's bytes are unchanged because nothing re-encodes them — and only the keyword at the render site gives that; a reader patch would show the em-dash while the file still churned.

(4) DEVIATION: none; scope and ceiling respected. The single-EOF rule (876-877) and config:rotations were correctly left untouched per the node.

BANKED (not this claim): send.py:403 does verb_set(e, list_key, json.dumps(rows)) with the default ensure_ascii=True — a JSON string scalar, a sibling site with the same escape-through-write shape, explicitly outside this node FILE SCOPE. Worth its own hypothesis.
<!-- THOUGHT:END -->
