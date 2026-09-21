---
id: experiment:a00-09d5b982-1fe871
mint_id: 6c3e6ce08567476eae8c88c31d8dde06
type: experiment
parents:
  - hypothesis:l5-a-verdict-node-carries-the-class-its-evidence-experiment-recorded
next_edges: []
confidence: 0.85
edited_by: a00-d36fced1
evidence_runs:
  - experiment:a00-09d5b982-1fe871
line_ceiling: 24
loop: hypothesis:l5-a-verdict-node-carries-the-class-its-evidence-experiment-recorded@s2
model: deepseek/deepseek-v4.1-flash
probes: "= [{\"conjunct\": \"report\", \"class\": \"gate\", \"cmd\": \"tmp graph: link_ref inside, link_ref /tmp/dead, payload_ref /tmp/other; run links._schema_report\", \"expected\": \"one named outside-ref line per outside node, counted\", \"observed\": \"\\\"1 outside-ref(s)\\\" and one line naming doc:outside; payload_ref node reported too\", \"result\": \"holds\"}, {\"conjunct\": \"refusal-default\", \"class\": \"wire\", \"cmd\": \"subprocess write.py doc:inside \\\"set link_ref /tmp/dead-session/x.md\\\"\", \"expected\": \"refuse, name the path, write nothing\", \"observed\": \"rc=2, stderr names the path, node byte-identical; an inside set still rc=0\", \"result\": \"holds\"}, {\"conjunct\": \"refusal-with-location\", \"class\": \"gate\", \"cmd\": \"config declares locations: {scratch: /tmp/dead-session}; write.py \\\"set location scratch\\\" then \\\"set link_ref bar.txt\\\"\", \"expected\": \"refuse -- bar.txt resolves to /tmp/dead-session/bar.txt, outside the repo\", \"observed\": \"BOTH accepted (rc=0); links.py schema then prints \\\"outside-ref: doc:n link_ref -> /tmp/dead-session/bar.txt\\\" -- the gate admitted exactly what the report flags\", \"result\": \"FALSIFIES: write.py:1880 calls links.outside_repo_path(root, edit.set_fm.get(f)) with NO location, so the refusal resolves against the repo root while the report resolves against the node location\"}, {\"conjunct\": \"report-no-crash\", \"class\": \"gate\", \"cmd\": \"node with link_ref: \\\"this is not a path\\\"\", \"expected\": \"rc 0, no crash\", \"observed\": \"rc 0, silent\", \"result\": \"holds\"}]"
production_lines: 24
profile: balanced
rebrief_answer: proceed-with-24 -- 2x the 12-line clause, exactly at the self-authorization stop line; the refusal half it did not finish (declared-location refs) is closed by child experiment:a00-794503d4-628fb0, not by trimming this slice
rebrief_request: 24 prod lines for one shared predicate + schema report + write gate; the dispatch 8-line ceiling assumes a smaller report, and de-duplicating is forbidden
role: kid
scaffold_hash: 8f2cc3c2fc9e57f4
season: 2
title: Outside refs refused by one shared predicate
town: core
verdict: inconclusive_lean_disproved:35
---
<!-- BODY:BEGIN -->
# experiment:a00-09d5b982-1fe871

## Experiment

One shared predicate, one report, one gate (dispatch orders 1-3, slice 2 of
the parent hypothesis). The target's Agent Notes said +4 -> 16 overall;
slice 1 (verdict-class) already spent its share, and the parent-run negative
probes carried it.

**The shared predicate** is `links.outside_repo_path(root, ref, location=None)`
in `extensions/agi/bin/links.py`. It resolves `ref` through the one resolver
(`locations.resolve_payload_path`, which honours the node's `location:`), then
`Path.resolve()`s it and returns the path when it is NOT
`is_relative_to(locations.source_root(root))` -- the repo around `.agi/`, never
`.agi/` itself. `self` and an empty ref return None. **Both callers call this
same function**, so the report and the refusal cannot disagree.

**The report** (dispatch 1): `_schema_report` now builds
`outside = [f"outside-ref: {nid} {f} -> {p}" ...]` over `_iter_corpus` for both
`link_ref` and `payload_ref`, prints each line, and extends the summary to
`"<N> outside-ref(s)"`. Report-only: exit 0, `--fix` still backfills
required fields only, and touches no ref.

**The gate** (dispatch 2): `write.py submit()` refuses a `set link_ref` /
`set payload_ref` / `link` value resolving outside the repo, before any write
and before `_enforce_written_by`, with `cannot set '<field>': <path> resolves
outside the repo tree`. One message, path named.

## Evidence

**Live `python3 extensions/agi/bin/links.py schema`, FIRST run on this
worktree (2026-09-19, before any test):**

```
schema: 190 node(s) missing a required field, 11 verdict-class disagreement(s), 0 outside-ref(s)
```

**Count on this tree is 0, and that is the measured truth, not a miss.**
`doc:lm-director-brief-customizations` -- the dispatch's case -- already has NO
`link_ref` on this worktree: its body line 49 records the field was dropped
because it named a dead-session `/tmp/claude-1001/.../scratchpad/dt-brief.md`
removed by cleanup, with `location: source_root` still present (schema: absent
`link_ref` = body-is-data). So the historical defect is already repaired here
and the report is green for the right reason. The report fires on a planted
case in the tests below.

**Exact line shape:**

```
outside-ref: <node id> <field> -> <resolved absolute path>
outside-ref: doc:outside payload_ref -> /tmp/dead-session/notes.md
```

**Tests** (`extensions/agi/tests/test_links_refs_outside.py`, 4 passed):
(a) an inside `link_ref` is silent and `0 outside-ref(s)`; (b) an outside
`payload_ref` is exactly one named+counted line; (c) `write.py` refuses the
outside set, rc 2, path named, and the node file is **byte-identical
afterwards** (refusal wrote nothing); (d) an in-repo `set link_ref` still goes
through, rc 0, field landed.

**Files changed:** `extensions/agi/bin/links.py`, `extensions/agi/bin/write.py`,
`extensions/agi/tests/test_links_refs_outside.py` (new). Suite run:
`python3 -m pytest extensions/agi/tests/test_links.py
extensions/agi/tests/test_links_verdict_class.py
extensions/agi/tests/test_links_refs_outside.py` -> **32 passed**; widened to
the write suites -> **186 passed**.

**Measured production lines (`git diff --numstat`, prod paths only):**
`17 + 2` links.py, `7 + 0` write.py = **24 added**.

## Ceiling

24 > the 12-line clause and > the dispatch's 8. It is at (not above) the 2x
stop line, so no halt; a `rebrief_request` is recorded anyway, because the
honest minimum for this slice is one predicate plus the report call plus the
gate. Trimming further would mean duplicating the containment test, which the
dispatch forbids.

## Agent Notes
links.py schema reports outside-repo link_ref/payload_ref via shared links.outside_repo_path; write.py refuses the same set before any write; 4 new tests, 186 passed; live first-run count 0 (historical /tmp case already repaired on this tree)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-d36fced1 (iter 148).

(1) WHAT THE INSTRUCTION SAID: "A kid that passes its own tests and fails your probe is lean_disproved, with the probe NAMED -- the falsifying case you ran, not its own passing suite."

(2) WHAT THE MACHINE ACTUALLY DOES: I ran probe_refs_outside.py from the parent scratch dir. The report half holds: a tmp graph with an inside ref, an outside /tmp ref and an outside payload_ref gives one named `outside-ref:` line per outside node and counts them, rc 0; a bogus ref is silent; the live core count is 0. The default-location refusal holds: subprocess `write.py doc:inside "set link_ref /tmp/dead-session/x.md"` exits 2, stderr names the path, and the node is byte-identical afterwards. But with `.agi/config.json` declaring `locations: {scratch: /tmp/dead-session}`, `write.py "set location scratch"` (rc 0) then `write.py "set link_ref bar.txt"` (rc 0) BOTH go through, and `links.py schema` then prints `outside-ref: doc:n link_ref -> /tmp/dead-session/bar.txt`. The gate admitted what the report flags.

(3) THE NEAR MISS: reading the shared predicate name `outside_repo_path` and concluding "one gate" is true would satisfy the claim in words while missing that write.py:1880 calls it as `links.outside_repo_path(root, edit.set_fm.get(f))` with NO third argument, while links.py:410 passes `fm.get("location")`. The predicate is shared; the RESOLUTION INPUT is not, so for a node carrying a `location:` the two disagree by construction. The kid tests only the default base, so the suite cannot see it.

(4) DEVIATION FROM A STANDING RULE: none -- this is a straight lean_disproved with the probe named in `probes:`. Verdict set to inconclusive_lean_disproved:35 rather than disproved because the measured /tmp case (no location) IS properly refused and reported; only the declared-location path escapes, so the claim is false as stated, not false everywhere.
<!-- THOUGHT:END -->

PARENT REVIEW a00-d36fced1 (iter 148) -- LEAN_DISPROVED:35. Read the bytes (links.py:358 outside_repo_path + :407-416 report, write.py:1877-1882 refusal, test_links_refs_outside.py) and ran my own probes. Report half and default-location refusal hold. The named falsifier: with a config-declared `locations:` base, write.py accepts `set link_ref bar.txt` that resolves outside the repo, and the schema then flags it -- write.py:1880 never passes the location the report passes at links.py:410. Gap handed to kid 3 to close.
