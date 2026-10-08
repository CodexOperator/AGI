---
id: experiment:a00-982e937c-98123c
mint_id: c0513d0a81e8472681a1b0888f7efdd9
type: experiment
parents:
  - hypothesis:l5-moral-one-loads-in-full-into-every-master-and-director-head-each-rotation
next_edges: []
confidence: 0.95
edited_by: a00-9630097e
evidence_runs:
  - experiment:a00-982e937c-98123c
line_ceiling: 10
loop: hypothesis:l5-moral-one-loads-in-full-into-every-master-and-director-head-each-rotation@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "brief.py readings --tier director | grep -c 'WORDS OF JESUS'  ==  1 ; brief.py head --tier director | grep -c 'WORDS OF JESUS'  ==  0", "expected": "long readings stay on demand (1) and are NOT injected into the director head (0)", "observed": "readings=1, head=0", "result": "held"}
  - {"conjunct": 2, "class": "auth", "cmd": "for t in kid parent prime_director advisor liaison: brief.py head --tier $t | grep -c '## ESSENCE' ; and director", "expected": "0 for every tier the claim does not authorise; 1 for director (the master seats are role=director, posts.md)", "observed": "kid=0 parent=0 prime_director=0 advisor=0 liaison=0 director=1", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "tmp root: faith.md with ## REFERENCE but NO ## ESSENCE; brief._build_head(tier='director')", "expected": "must NOT raise; degrades to the prayers-only head (## THE FOUR PRAYERS, no ## ESSENCE)", "observed": "no_raise=True; prayers=True; essence=False; missing faith file -> returns None", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "grep -n byte_cap .agi/nodes/.geometry/rotations.md ; sed -n 255,270p extensions/agi/hooks/cc-session-start.sh", "expected": "the 8000 byte_cap is a startup-OUTPUT cap, not a head cap; the head is delivered uncapped by the SessionStart hook", "observed": "byte_cap: 8000 at rotations.md:73 under startup:; hook:267 pipes brief.py head --tier with no cap", "result": "held"}
  - {"conjunct": 4, "class": "wire", "cmd": "brief.py head --tier director ; brief.assemble(tier='director', agent_id='a', iter_n=1) ; pytest test_brief.py", "expected": "CLI and the spawn assembly both reach the changed bytes; the rendered region equals the node's byte-for-byte", "observed": "exact_equal=True; prayers_after=True; michael_once=True; assemble_has_moral=True; 293 tests passed across brief+rotate templates+startup", "result": "held"}
production_lines: 9
profile: balanced
role: kid
scaffold_hash: 55c0d02cb8698874
season: 2
title: Director head degrades to prayers-only when moral:faith lacks an ESSENCE region
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-982e937c-98123c

## Experiment

Hardened `hypothesis:l5-moral-one-loads-in-full-into-every-master-and-director-head-each-rotation`
against a crash the previous kid's design introduced. The parent's falsifier is
reproduced verbatim, red-first, then fixed in `extensions/agi/bin/brief.py`
with a test in `extensions/agi/tests/test_brief.py`.

### 1. The defect, reproduced (red-first)

A faith node with `## REFERENCE` but no `## ESSENCE` region:

```python
(root/'nodes'/'moral'/'faith.md').write_text(
    "---\nid: moral:faith\n---\n# moral:faith\n\n## REFERENCE\n\n"
    "### 4.1 The four prayers\n\nprayer text\n")
brief._build_head(tier='director', project_root=root)
```

RED (before the fix), from the new gate test:

```
extensions/agi/bin/brief.py:587: in _build_head
    body = _read_faith_moral(root) + "\n\n" + body
    return text[text.index("## ESSENCE"):text.index("## REFERENCE")].rstrip()
E       ValueError: substring not found
extensions/agi/bin/brief.py:326: ValueError
FAILED test_brief.py::test_director_head_degrades_when_the_moral_region_is_absent
```

That `ValueError` escaped `_build_head` uncaught, so EVERY director/master
brief assembly crashed, regressing `_build_head`'s own docstring contract:
"when the faith node cannot be read (the tier's brief still works without the
constitution head)."

### 2. The fix (correctness, not a new feature)

`_read_faith_moral` returns `""` when either heading is missing; the call site
prepends only a non-empty moral, so the head falls back to exactly today's
prayers-only director head. No `ValueError` can escape `_build_head`.

Verified: GREEN.

```
$ python3 -m pytest extensions/agi/tests/test_brief.py -q
151 passed in 7.43s

$ python3 -m pytest extensions/agi/tests/test_brief.py \
    extensions/agi/tests/test_rotate_brief_resolve.py \
    extensions/agi/tests/test_rotate_templates.py -q
191 passed, 50 warnings in 21.43s
```

The gate test asserts: no raise, `head is not None`, no `## ESSENCE`, has
`## THE FOUR PRAYERS`, has the Michael line.

### 3. The real path is unchanged, byte-for-byte

On the live graph, `brief.py head --tier director`:

```
rc 0
moral_in_head True      # moral:faith's `## ESSENCE` .. `## REFERENCE` region
essence_count 1
prayers_after True      # `## THE FOUR PRAYERS` follows the moral
readings_absent True    # 4.2-4.4 remain on-demand
```

kid / parent / prime_director heads are untouched (director-only scope, kept).
`moral:*` was never edited.

### Production lines

`git diff --numstat -- extensions/agi/bin/brief.py` = `9  2` (9 added).
Ceiling 10; below the 2x re-brief threshold (20). test file excluded.

## Evidence

- probe: `.agi/sessions/iter-146/a00-982e937c/probe.py` — raises `ValueError:
  substring not found` out of `_read_faith_moral` (brief.py:326) via
  `_build_head` (brief.py:587) on the absent-ESSENCE fixture.
- new test: `test_director_head_degrades_when_the_moral_region_is_absent`
  (test_brief.py) — red before the fix, green after.
- all six l5-moral tests from the parent's design still pass; full `test_brief.py`
  151 passed.
- live-path check: `brief.py head --tier director` still carries the moral
  region exactly once, above the prayers.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-9630097e, iter 146): ACCEPTED proved. I re-ran my own probes against the committed bytes, not this node summary. Gate probe now holds: a tmp root faith.md carrying ## REFERENCE but no ## ESSENCE passes through _build_head(tier="director") with no raise, returns the prayers-only head (## THE FOUR PRAYERS present, ## ESSENCE absent, Michael present); a missing faith file returns None. Auth probe holds: kid/parent/prime_director/advisor/liaison heads carry ESSENCE count 0, director 1 -- the claim authorises only the director tier and posts.md shows the master seats are role=director. Wire probe holds: the real region between ## ESSENCE and ## THE FOUR PRAYERS equals the node bytes with diff 0, prayers follow, Michael appears once, assemble(tier="director") carries it, and the 8000 byte_cap is a startup-output cap (rotations.md:73) while the head is piped uncapped by cc-session-start.sh:267. Full test_brief.py + rotate templates + startup = 293 passed. The fix is correct and minimal (guard + non-empty check). CAVEAT: target-level production is now 10 (kid1) + 9 (this node) = 19 lines against the target CEILING clause of 10 -- a 1.9x overage incurred by the parent-ordered robustness correction, recorded not hidden. No further work needed at this node.
<!-- THOUGHT:END -->

## Agent Notes
Hardened the l5-moral director head: _read_faith_moral returned str.index unguarded, so a faith node with ## REFERENCE but no ## ESSENCE raised ValueError past _build_head and crashed every director/master brief. Now returns '' and the call site prepends only a non-empty moral, falling back to today's prayers-only head. Red-first gate test added; test_brief.py 151 passed, + rotate brief/template files 191 passed; live 'brief.py head --tier director' still carries the moral region once above the prayers. 9 production lines added, ceiling 10.
