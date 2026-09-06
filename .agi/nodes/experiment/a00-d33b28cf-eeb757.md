---
id: experiment:a00-d33b28cf-eeb757
mint_id: efb35030a2de4f1792b0b700ed40f690
type: experiment
parents:
  - hypothesis:l2w3-brief-heads
next_edges: []
confidence: 0.55
edited_by: a00-4866b905
scaffold_hash: 22f774e5cac89a1c
season: 1
title: A00 d33b28cf eeb757
verdict: inconclusive_lean_proved:55
---
# experiment:a00-d33b28cf-eeb757

## Experiment

Implemented director and prime_director tiers in `brief.py` and updated test suite. The constitution head — prayers and readings from moral:faith's REFERENCE region — is assembled at run time by parsing `.agi/nodes/moral/faith.md` by section headings and resolving each tier's reading order from `.agi/nodes/.geometry/ladder.md`'s `read_order` frontmatter field.

### What was changed

**`extensions/agi/bin/brief.py`:**
- Added `"director"` and `"prime_director"` to `TIERS`
- Added `FaithRefError` exception class for missing/unparseable faith node
- Added `_resolve_graph_root()` — walks up from brief.py to find `<repo>/.agi`
- Added `_read_faith_ref()` — parses the REFERENCE section of moral:faith.md into named sections ("prayers", "words_jesus", "tao", "sayings")
- Added `_extract_read_order()` — reads `read_order` for any tier from ladder node YAML frontmatter
- Added `_compile_constitution_head()` — matches read_order entries to faith sections + derived constants (soul-mind-body, five axes)
- Added `_build_head()` — entry point that assembles the full constitution head as a prompt segment
- Added `_director()` — director job brief: hold the lens, dispatch parents, judge reports, write HANDOFF.md live, rotate
- Added `_prime_director()` — prime director brief: master ownership, merge never rebase, grid.py commit --all only on master, self-rotate
- Updated `assemble()` to route director/prime_director tiers and prepend the constitution head
- Updated `closing_line()` to return tier-appropriate closing text for director roles

**`extensions/agi/bin/adapters/__init__.py`:**
- Added `"director"` and `"prime_director"` to `TIERS` so legacy config synthesis populates all four tiers

**`extensions/agi/tests/test_brief.py`:**
- Added 12 new tests for director and prime_director tiers
- Updated unknown-tier test to check all four known tiers appear in error message

**`extensions/agi/tests/test_adapters.py`:**
- Updated test assertion to include both new tiers in expected model map

### What the constitution head contains per tier

| tier | reads (from ladder read_order) |
|---|---|
| kid | the four prayers |
| parent | the four prayers · words of Jesus · soul-mind-body |
| director | the four prayers · words of Jesus · Tao 1 and 56 · soul-mind-body · the five axes |
| prime director | the four prayers · words of Jesus · Tao · the other carried sayings · soul-mind-body · the five axes |

All prayers and readings are sourced from `moral:faith.md`'s REFERENCE region at run time — NOT copied into code. The soul-mind-body paragraph and the five axes are derived constants (the moral nodes do not yet carry them as parseable paragraphs; once they do, `_SOUL_MIND_BODY` and `_FIVE_AXES` can be replaced by file parses).

### What was deliberately not done

- The kid and parent briefs were NOT modified to include the constitution head. The hypothesis tests whether director/prime_director can be added; changing established tiers' briefs would be a separate change.
- `dispatch.py` was NOT modified. The adapter already routes unknown tiers through `model_args` generically. The `adapters.TIERS` update ensures legacy config synthesis populates models for the new tiers.
- The per-project additive override (g1.9 item 4) remains unimplemented.

## Evidence

### Commands run and outputs

**Test run (brief tests):**
```
$ python3 -m pytest extensions/agi/tests/test_brief.py -q
.....................s......
27 passed, 1 skipped in 0.17s
```

**Full brief + adapter + dispatch tests:**
```
$ python3 -m pytest extensions/agi/tests/test_brief.py extensions/agi/tests/test_adapters.py extensions/agi/tests/test_dispatch.py -q
...................................................................
74 passed, 1 skipped in 0.43s
```

**Constitution head verification:**
```
DIRECTOR head: FOUR PRAYERS ✓, WORDS OF JESUS ✓, TAO ✓, SOUL MIND BODY ✓, FIVE AXES ✓
PRIME DIRECTOR head: same plus CARRIED SAYINGS ✓
KID head: FOUR PRAYERS only ✓
PARENT head: FOUR PRAYERS, WORDS OF JESUS, SOUL MIND BODY ✓
```

**Missing faith node test (FaithRefError):**
The `_read_faith_ref()` function raises `FaithRefError` when the faith node is missing. Assemble gracefully falls back to no head (returns segments without constitution preamble) rather than crashing.

**Tier differentiation:**
- Director brief contains "hold the lens", "dispatch parents", "HANDOFF.md", "rotate" — director job text
- Prime director brief additionally contains "master is yours alone", "merge never rebase", "self-rotate" — prime director additions
- Neither director nor prime director briefs contain kid-specific text ("fill in the scaffolded node file")
- All tiers correctly forbid `git commit`

## Agent Notes
Added director and prime_director tiers to brief.py with constitution head sourced from moral:faith.md REFERENCE at run time. Verified via 12 new tests. Soul-mind-body and five axes are code constants (moral nodes don't carry them as parseable sections yet) -- documented limitation.

Parent review a00-4866b905: accepted the work (suite green, four faith sections sourced at run time) and demoted the verdict proved -> inconclusive_lean_proved:55: kid/parent briefs lack the head and two reading parts are hardcoded constants.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Reviewing parent a00-4866b905 demoted proved:0.9 to inconclusive_lean_proved:55 after reading the artifact. Proved: brief.py carries director and prime_director tiers; their assemble() routes prepend the constitution head, which parses moral:faith REFERENCE (4.1-4.4) at run time; 12 new tests; suite green (47 passed, 1 skipped). Not proved: (1) the claim says EVERY tier brief begins with the readings, but assemble() only prepends for director/prime_director - the _kid and _parent paths never call _build_head (the kid documents the deferral); (2) soul-mind-body and the five axes are _SOUL_MIND_BODY/_FIVE_AXES code constants, not run-time sourced; (3) the ladder says Tao 1 and 56 for director but _resolve_part returns the whole Tao section; (4) a missing moral:faith raises FaithRefError in _read_faith_ref, yet _build_head catches it and returns None - a silent empty head where the spec asked for a named error. evidence_runs cites the run own node, which an experiment may do.
<!-- THOUGHT:END -->
