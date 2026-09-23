---
id: experiment:grok-session-ingest-pipe-plus-batch-scan
mint_id: 764f5ee55d194b3dada59673bcfb0a92
type: experiment
parents:
  - hypothesis:a00-ed92438f-92acc9
next_edges: []
confidence: 0.9
edited_by: a00-366de186
evidence_runs: experiment:grok-session-ingest-pipe-plus-batch-scan
line_ceiling: 140
loop: goal:g7.32.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 129
profile: balanced
rebrief_answer: proceed with ceiling 140
rebrief_request: "ingest_grok_session.py is 129 production lines against the 40-line default; prior single-artifact art was 75 and batch mode cannot fit 40. git diff --numstat reads 0 because the file is untracked. No work remains: pipe + batch + 9 tests green. A ceiling of 140 lines for bin/ ingest scripts would fit."
role: kid
scaffold_hash: 4b7dae1d26d150a1
season: 2
thought_session: ses-DH179
title: "Grok session ingest pipe lands on this tip: single artifact + batch --scan, idempotent by source_session, 9 tests green"
town: core
verdict: proved
---
# experiment:grok-session-ingest-pipe-plus-batch-scan

## Experiment

Authored `extensions/agi/bin/ingest_grok_session.py` ON THIS TIP (the prior
proven bytes lived only on side branch `8bc75e1e5`) and added the increment the
brief asks for: **batch discovery**. One artifact by path, or `--scan DIR`
which ingests every `*.jsonl` in stable sorted order, prints one node id (or
one `refused:` line) per artifact, continues past a per-artifact refusal, and
exits non-zero iff ZERO artifacts ingested. Re-running a scan prints the same
ids and mints nothing new (idempotent by `source_session`).

Files: `extensions/agi/bin/ingest_grok_session.py`,
`extensions/agi/tests/test_ingest_grok_session.py`,
`extensions/agi/tests/fixtures/grok-session-{sample,batch-b,malformed,empty}.jsonl`.

All five falsifier steps were run at the CLI against a throwaway graph root
(`.agi/sessions/iter-DH.179/a00-ed92438f/tmpgraph{,2}`), never the live graph.

## Evidence — the five falsifiers, real stdout

```
$ python3 extensions/agi/bin/ingest_grok_session.py <tmp>/sessions/a.jsonl --root <tmpgraph> --actor kid-a00 --thought-session ses-DH179
hypothesis:grok-2026-09-22-abc123
rc=0

=== files under nodes after step1 ===
<tmpgraph>/.agi/nodes/goal/g7.32.1.md
<tmpgraph>/.agi/nodes/hypothesis/grok-2026-09-22-abc123.md

=== STEP 2: re-run same ===
$ python3 extensions/agi/bin/ingest_grok_session.py <tmp>/sessions/a.jsonl --root <tmpgraph> --actor kid-a00 --thought-session ses-DH179
hypothesis:grok-2026-09-22-abc123
rc=0

=== files after step2 (still one new, mint unchanged) ===
<tmpgraph>/.agi/nodes/goal/g7.32.1.md
<tmpgraph>/.agi/nodes/hypothesis/grok-2026-09-22-abc123.md

=== STEP 3: malformed ===
$ python3 extensions/agi/bin/ingest_grok_session.py <tmp>/sessions/c.jsonl --root <tmpgraph> --actor kid-a00 --thought-session ses-DH179
refused: unparseable JSON: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
rc=2

=== STEP 4: empty ===
$ python3 extensions/agi/bin/ingest_grok_session.py extensions/agi/tests/fixtures/grok-session-empty.jsonl --root <tmpgraph> --actor kid-a00 --thought-session ses-DH179
refused: empty session artifact
rc=2

=== STEP 5: missing provenance (no --actor/--thought-session, no env) ===
$ env -u AGI_ACTOR -u AGI_AGENT_ID -u AGI_THOUGHT_SESSION python3 extensions/agi/bin/ingest_grok_session.py <tmp>/sessions/a.jsonl --root <tmpgraph2>
refused: no actor
rc=2

=== files after step5 (nothing new) ===
<tmpgraph2>/.agi/nodes/goal/g7.32.1.md

=== BATCH: first --scan (a.jsonl good, b.jsonl good, c.jsonl malformed) ===
$ python3 extensions/agi/bin/ingest_grok_session.py --scan <tmp>/sessions --root <tmpgraph2> --actor kid-a00 --thought-session ses-DH179
hypothesis:grok-2026-09-22-abc123
hypothesis:grok-2026-09-22-batch222
refused: c.jsonl: unparseable JSON: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
rc=0

=== files after first scan (two new, one refusal did not abort) ===
<tmpgraph2>/.agi/nodes/goal/g7.32.1.md
<tmpgraph2>/.agi/nodes/hypothesis/grok-2026-09-22-abc123.md
<tmpgraph2>/.agi/nodes/hypothesis/grok-2026-09-22-batch222.md

=== BATCH: second --scan (same ids, mints nothing) ===
$ python3 extensions/agi/bin/ingest_grok_session.py --scan <tmp>/sessions --root <tmpgraph2> --actor kid-a00 --thought-session ses-DH179
hypothesis:grok-2026-09-22-abc123
hypothesis:grok-2026-09-22-batch222
refused: c.jsonl: unparseable JSON: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
rc=0

=== files after second scan (unchanged) ===
<tmpgraph2>/.agi/nodes/goal/g7.32.1.md
<tmpgraph2>/.agi/nodes/hypothesis/grok-2026-09-22-abc123.md
<tmpgraph2>/.agi/nodes/hypothesis/grok-2026-09-22-batch222.md
```

The minted node carries both provenance fields and the idempotency key:

```
edited_by: kid-a00
ingest_source: grok-session
source_session: grok-2026-09-22-batch222
thought_session: ses-DH179
testable_claim: Grok session grok-2026-09-22-batch222 lands as graph residue.
```

## Evidence — pytest

```
$ python3 -m pytest extensions/agi/tests/test_ingest_grok_session.py -q
.........                                                                [100%]
9 passed, 5 warnings in 8.83s
```

The 9: mint-with-provenance, reingest-same-id, malformed-refused,
empty-refused, env-provenance, missing-provenance-refused, batch-sorted +
idempotent + refusal-does-not-abort, batch-all-refused exits 2, bad-scan-dir
refused.

## Ceiling checkpoint

`production_lines: 129` against the 40-line config default (`git diff
--numstat` over the production path reads **0** because the file is untracked —
the instrument is blind to a brand-new file, which is exactly what an ingest
pipe is). Prior art `ingest_grok_session.py@8bc75e1e5` was 75 lines for the
single-artifact mode alone; the batch mode this round adds cannot fit 40.
`rebrief_request` names what is needed; no work remains — the pipe and its
falsifiers are complete and green.

## Verdict

proved — the claim is behaviour built on this tip, and all five falsifiers plus
the batch scan hold on the built bytes.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First landing of the ingest pipe on this tip (prior bytes survived only on side branch 8bc75e1e5), plus the batch-discovery increment the brief asks for. Deviation: experiment parented to hypothesis:a00-ed92438f-92acc9, not goal:g7.32.1, because the experiment schema forbids a goal parent -- the chain hyp->exp underneath the goal is the same residue. Overage disclosed via rebrief_request, not blocked on, because the falsifiers are complete.
<!-- THOUGHT:END -->
