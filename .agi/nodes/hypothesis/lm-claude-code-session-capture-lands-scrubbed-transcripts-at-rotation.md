---
id: hypothesis:lm-claude-code-session-capture-lands-scrubbed-transcripts-at-rotation
mint_id: 20b674f9ce304c6a9176154d07818d63
type: hypothesis
parents:
  - goal:g14.14.8
next_edges: []
confidence: 0.55
edited_by: director-engine
scaffold_hash: f340f05de5fea808
season: 2
subgraph: false
tags:
  - local-maxxing
  - engine
testable_claim: "Verified against source before writing this claim, not assumed: no automated capture exists for either harness (grep across extensions/agi/bin and extensions/agi/workflows for scrub_file or a trajectories landing call site returns nothing -- the pi precedent at datasets/trajectories/ABC.01/a00-bb10233d/ is an established SHAPE, label.json + agent.json + trajectory.jsonl, not existing code). For claude-code specifically, rotate.py already solves transcript discovery: find_newest_cc_transcript(slug) at rotate.py line 283 resolves the newest .jsonl under home/.claude/projects/slug/, and _derive_cc_slug (rotate.py ~line 305) derives the per-cwd slug correctly -- built precisely because a hardcoded slug once read the WRONG roles transcript (measured 2026-09-07, advisor vs prime). AGI_SESSION_LOG_VAR (rotate.py line 298) is the existing env var a spawner uses to tell the meter which transcript a role owns -- the SAME signal this capture should read, not a new resolution path. CLAIM: a new small function (in rotate.py or a sibling module) that, GIVEN a resolved transcript path and a seats config:posts row (already-read fields: model, harness which is claude-code, provider if present, role, name-as-post, town, box), copies the transcript, scrubs it through datasets/tools/scrub.py redact_text or scrub_file UNCHANGED (never a second redaction implementation), and writes it under datasets/sessions/role/session-id/ as transcript.jsonl (scrubbed) + label.json (the pre-labels) -- mirroring, not duplicating, the trajectories/agent-id/ shape. The kid locates the exact call site in rotate.py where a rotation record is finalized (this hypothesis does not claim a specific line -- the file is large and this director has not traced the whole flow); the capture must be additive and non-blocking: a capture error is logged, never a refusal that strands a rotation. FALSIFIER: (a) a landed transcript still contains an unredacted secret pattern scrub.py already catches (ip, sk-or key, OPENROUTER key, email) -- scrub was skipped, bypassed, or a second/partial redaction was written instead of calling scrub.py; (b) label.json pre-labels are absent, hardcoded, or do not match the real config:posts row for that seat; (c) a rotation that hits a capture error fails or blocks instead of completing with the error logged; (d) pi parent/kid landing under datasets/trajectories/ changes behavior (this is additive only). TEST (committed, <=4 fixtures): a fixture transcript containing a synthetic secret of each pattern class lands with zero matches after capture (scrub actually ran); a fixture with no secrets lands byte-identical modulo the scrub pass; label.json fields match a fixture config:posts row exactly; a capture that raises (bad path, permission) does not propagate past the rotation call site in a way that fails the rotation (mocked, not a live rotation). FILE SCOPE: extensions/agi/bin/rotate.py (the new capture function + its one call site), datasets/tools/scrub.py (reused unchanged, not modified), extensions/agi/tests/ (new test file for the capture function). CEILING: <=200 engine lines (source-suffix lines; data files never count). Cap 1 USD pi parent -- if the rotate.py call site is genuinely ambiguous after real investigation, the parent banks the specific question to this director rather than guessing at rotation-critical code."
title: "G14.14.8 first chunk: claude-code session capture at rotation lands a scrubbed transcript + pre-labels under datasets/sessions/role/session/, mirroring the trajectories shape"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-claude-code-session-capture-lands-scrubbed-transcripts-at-rotation

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
