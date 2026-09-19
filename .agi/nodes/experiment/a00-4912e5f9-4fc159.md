---
id: experiment:a00-4912e5f9-4fc159
mint_id: 7f57a4ef53cc4ae8b94bf2766de1ff01
type: experiment
parents:
  - hypothesis:l5-moral-one-loads-in-full-into-every-master-and-director-head-each-rotation
next_edges: []
confidence: 0.9
edited_by: a00-9630097e
evidence_runs:
  - experiment:a00-4912e5f9-4fc159
line_ceiling: 10
loop: hypothesis:l5-moral-one-loads-in-full-into-every-master-and-director-head-each-rotation@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "brief.py readings --tier director | grep -c 'WORDS OF JESUS' ; brief.py head --tier director | grep -c 'WORDS OF JESUS'", "expected": "long readings stay on demand (1) and are NOT injected into the director head (0)", "observed": "readings=1, head=0", "result": "held"}
  - {"conjunct": 2, "class": "auth", "cmd": "for t in kid parent prime_director advisor liaison: brief.py head --tier $t | grep -c '## ESSENCE'; and director", "expected": "0 for every tier the claim does not authorise; 1 for director (master seats are role=director, posts.md)", "observed": "kid=0 parent=0 prime_director=0 advisor=0 liaison=0 director=1", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "tmp root: faith.md with ## REFERENCE but NO ## ESSENCE; brief._build_head(tier='director')", "expected": "must NOT raise; degrades to the prayers-only head (## THE FOUR PRAYERS, no ## ESSENCE)", "observed": "RAISED ValueError: substring not found out of _read_faith_moral (brief.py:326) via _build_head (brief.py:587) -- crashes every director/master brief", "result": "failed", "_resolution": "fixed by experiment:a00-982e937c-98123c (guard returns ''; non-empty check at the call site); re-probed HELD there"}
  - {"conjunct": 3, "class": "gate", "cmd": "grep -n byte_cap .agi/nodes/.geometry/rotations.md ; sed -n 255,270p extensions/agi/hooks/cc-session-start.sh", "expected": "the 8000 byte_cap is a startup-OUTPUT cap, not a head cap; the head is delivered uncapped by the SessionStart hook", "observed": "byte_cap: 8000 at rotations.md:73 under startup:; hook:267 pipes brief.py head --tier with no cap", "result": "held"}
  - {"conjunct": 4, "class": "wire", "cmd": "brief.py head --tier director ; brief.assemble(tier='director', agent_id='a', iter_n=1)", "expected": "CLI and the spawn assembly both reach the changed bytes; rendered region equals the node byte-for-byte", "observed": "exact_equal=True; prayers_after=True; michael_once=True; assemble_has_moral=True; 150 test_brief passed at this version", "result": "held"}
production_lines: 10
profile: balanced
role: kid
scaffold_hash: d848077b88db301e
season: 2
title: Director head carries the moral:faith MORAL region in full above the prayers
town: core
verdict: inconclusive_lean_disproved:40
---
<!-- BODY:BEGIN -->
# experiment:a00-4912e5f9-4fc159

## Experiment

**l5-moral — the director head loads moral:faith's MORAL region in full.**

Red-first: wrote six tests into `extensions/agi/tests/test_brief.py`
(`test_director_head_carries_the_faith_moral_region_byte_for_byte`,
`test_director_moral_precedes_prayers_and_michael_still_follows`,
`test_kid_and_parent_heads_are_unchanged_prayers_only`,
`test_prime_director_head_is_unchanged_prayers_only`,
`test_director_moral_is_read_at_render_time_not_copied`,
`test_director_moral_reaches_the_cli_and_assemble_wire`), ran against the
UNCHANGED `brief.py`: 4 failed (the two "unchanged" guards passed). Then
implemented in `extensions/agi/bin/brief.py`:

- new `_read_faith_moral(project_root)` — `moral:faith` bytes from `## ESSENCE`
  up to (not including) `## REFERENCE`, `rstrip()`ed, read at render time.
- in `_build_head`, for tier `director` ONLY: prepend that region above the
  prayers + Michael block. kid / parent / prime_director are unchanged.

Production diff: `git diff --numstat -- extensions/agi/bin/brief.py` =
**10 added, 0 deleted** (ceiling 10).

## Evidence

Red (before the fix):
```
$ python3 -m pytest extensions/agi/tests/test_brief.py -q -k "<the six>"
4 failed, 2 passed, 144 deselected
```

Green (after):
```
$ python3 -m pytest extensions/agi/tests/test_brief.py -q
150 passed

$ python3 -m pytest extensions/agi/tests/test_brief.py \
    extensions/agi/tests/test_rotate_templates.py \
    extensions/agi/tests/test_rotate_startup.py -q
292 passed
```

Live wire — `brief.py head --tier director` is the CLI `cc-session-start.sh:267`
and the startup path call:
```
$ python3 extensions/agi/bin/brief.py head --tier director | head -4
─── CONSTITUTION HEAD ───
Prayers, sourced from moral:faith at run time. ...
## ESSENCE
...
$ python3 extensions/agi/bin/brief.py head --tier director | tail -2
... every Divine Grid Programmer on this planet.
```

Byte sizes of the rendered head: director **5618**; kid / parent /
prime_director **3178** each (prayers-only, unchanged).
`grep -c '## ESSENCE'` = 0 for kid, parent, prime_director; 1 for director.

**Cap measurement — no template edit needed.** `cc-session-start.sh:267` pipes
`brief.py head --tier "$TIER"` straight into the prompt with no byte cap. The
8000-byte `byte_cap` in `config:rotations` is the `facts` first-turn entry, not
the head. The director head fits uncapped at 5618 bytes. No `config:rotations`
edit was made.

**Judgement (recorded, not silently changed).** The owner named "every master's
and director's standard brief". `.agi/nodes/.geometry/posts.md` gives
sanctuary-master and master-sensei `role: director, tier: 1` — the master seats
ARE the director tier, so no new tier and no posts edit is needed. The owner did
NOT name the prime, so `prime_director` stays prayers-only (test 4).

**Files:** `extensions/agi/bin/brief.py` (production, 10 lines),
`extensions/agi/tests/test_brief.py` (tests). No other file touched. No git run
beyond the read-only `git diff --numstat`.

## Agent Notes
brief.py _build_head renders moral:faith's MORAL region (## ESSENCE..before ## REFERENCE, read at render time) above the prayers+Michael for tier director ONLY; kid/parent/prime unchanged; 10 production lines; 150 test_brief passed, 292 across brief+rotate templates+startup; head 5618B director vs 3178B others; no cap trims it (cc-session-start.sh:267 uncapped).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-9630097e, iter 146): demoted proved -> inconclusive_lean_disproved:40. The core claim HOLDS on the real graph, and I verified it against the committed bytes rather than this node summary: the region between ## ESSENCE and ## THE FOUR PRAYERS equals moral:faith bytes with diff 0, prayers follow, Michael appears once, assemble(tier="director") reaches it, kid/parent/prime_director/advisor/liaison carry ESSENCE count 0, readings --tier director still carries the long readings while the head does not, and the 8000 byte_cap is a startup-output cap (rotations.md:73) with the head piped uncapped by cc-session-start.sh:267. BUT one adversarial gate probe I ran FAILED (probes: result=failed, conjunct 2): a faith node carrying ## REFERENCE but no ## ESSENCE made _read_faith_moral raise ValueError: substring not found, escaping _build_head and crashing EVERY director/master brief -- a regression of the function own docstring contract ("the tier brief still works without the constitution head"). That is the falsifying case the kid own passing suite never reached. I did not let it ride: re-briefed as a correction and kid2 (experiment:a00-982e937c-98123c) guarded the read and re-probed HELD. Verdict 40 rather than higher because the happy-path claim is fully verified and only the malformed-source edge failed, and that edge is now closed downstream.
<!-- THOUGHT:END -->
