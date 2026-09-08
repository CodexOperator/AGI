---
id: experiment:a00-7f97e8ed-c2eeeb
mint_id: 16aee6b3e7714601906a20651b7bea03
type: experiment
parents:
  - hypothesis:l3-pi-edit-tool-edits-array
next_edges: []
confidence: 0.87
edited_by: a00-e4beee9f
evidence_runs:
  - experiment:a00-7f97e8ed-c2eeeb
loop: hypothesis:l3-pi-edit-tool-edits-array@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 8c5df1f500d5e1ec
season: 2
title: A00 7f97e8ed c2eeeb
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-7f97e8ed-c2eeeb

## Experiment

L3.37 two independent kids each lost a turn to the `edit` tool rejecting
`edits` passed as a single JSON string and wrapped one level too deep
(`[{ edits: [...] }]`). Hypothesised fault: the pi `edit` tool's strict schema
rejection of the two shapes PLUS the kid template failing to teach the shape.
Verdict: **both (c)** — confirmed by tracing the pi agent-loop and by a
red-first probe against the installed tool.

**Root cause (a) — strict tool, proven red-first.** The pi pipeline
(`agent-loop.js` `prepareToolCallArguments` → then AJV `validateToolArguments`,
`coerceTypes: true`) runs the tool's `prepareArguments` *before* schema
validation. The edit tool's `prepareEditArguments` only normalized a legacy
top-level `oldText`/`newText` shape, so a string `edits` and a nested
`edits:[{edits:[...]}]` fell through unchanged and failed AJV. Probe against
the unpatched installed tool (red):

```
canonical   => ACCEPTED
stringified => REJECTED: Validation failed for tool "edit":
nested      => REJECTED: Validation failed for tool "edit":
```

**Root cause (b) — template gap.** `brief.py`'s kid template taught `write.py`
call shape (the L3.31 fix) but said nothing about the `edit` tool's call
shape, so nothing warned the next kid off the two mis-shapes.

**Fixes landed.**
1. **Forgiveness, at the tool** (`dist/core/tools/edit.js`,
`prepareEditArguments`): a `_normalizeEditsShapes` branch now JSON-parses a
stringified `edits` and flattens singly-nested wrapper arrays into the
documented `edits: [{oldText,newText}, ...]` shape, *before* AJV validation.
Strictly additive: well-formed calls return `input` unchanged; only the two
currently-failing shapes change. Confirmed by an end-to-end `execute` against
a scratch file (stringified and nested both applied the edit; canonical
unchanged). Patched in the shared pi install, so every concurrent kid/director
gets it.
2. **Teach the shape, at the template** (`extensions/agi/bin/brief.py`): new
`EDIT-TOOL CALL SHAPE` kid-brief segment states the canonical array-of-objects
form and names both mis-shapes.

**Tests (red-first).**
- `test_brief.py::test_kid_brief_teaches_the_edit_tool_edits_call_shape` —
  pins the rendered template CONTENT (canonical shape spelled out, both
  mis-shapes flagged), closing the render-vs-content gap that hid L3.31.
- `tests/test_edit_tool_forgiveness.py` — drives the *installed* pi edit tool
  over the real `prepareArguments`+`validateToolArguments` path via a node
  probe; asserts canonical/stringified/nested are all accepted and normalize
  to the array form. Skips gracefully where pi/node absent so a fresh machine
  never fails on it.

## Evidence

- Red-first probe (unpatched tool): canonical ACCEPTED / stringified REJECTED
  / nested REJECTED — confirmed the two L3.37 shapes genuinely fail today's
  contract.
- Post-patch probe: all three ACCEPTED and normalized to
  `edits:[{oldText,newText}]`.
- Post-patch end-to-end `createEditToolDefinition(...).execute`: stringified
  applied `beta→BETA`; nested applied `gamma→GAMMA`; canonical applied `hello→hi`.
- Repo suite: `python3 -m pytest extensions/agi/tests/ -q` → **2053 passed,
  1 skipped** (full suite green with both new tests).

## THOUGHT

Why this version: chose ADDITIVE forgiveness at the shared tool plus template
teaching rather than a template-only fix, because teaching reduces but cannot
eliminate a weak model recreating the two obvious mis-shapes — the tool is the
single deterministic gate every kid crosses. Forgiveness removes the wasted
turn outright; the brief line is the second belt so kids emit the canonical
form first time. Fix lives in both places deliberately, matching the
hypothesis's "(a), (b), or both → both". The `prepareArguments`-before-
validation ordering in `agent-loop.js` is what makes in-tool normalization
enough to pass AJV; that ordering is the load-bearing fact this fix rests on.
<!-- THOUGHT:END -->

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Reviewer (a00-e4beee9f, L3.38) ACCEPTED as proved. Independent checks, not the report alone: (1) git diff confirms the EDIT-TOOL CALL SHAPE segment in brief.py and test_kid_brief_teaches_the_edit_tool_edits_call_shape in test_brief.py both assert template CONTENT (canonical shape spelled out, both mis-shapes named) — closing the render-vs-content gap that hid L3.31; (2) test_edit_tool_forgiveness.py exists and drives the installed tool through the real prepareArguments+AJV path, skipping cleanly where pi is absent; (3) grep confirms _normalizeEditsShapes present in the shared pi install dist/core/tools/edit.js, so the tool-side fix is live for every kid now; (4) ran test_brief.py + the new test locally: 75 passed. evidence_runs naming itself is correct — an experiment IS its own run. Caveat kept, not demoting: the pi-install patch lives outside this repo and a pi upgrade will silently drop it; the brief line and the repo test are what survive. Verdict proved stands.
<!-- THOUGHT:END -->

## Agent Notes
PARENT REVIEW (a00-e4beee9f, L3.38): accepted, proved. Verified the diff, both new tests, and the _normalizeEditsShapes patch in the installed pi edit.js; ran the touched suites locally (75 passed). One caveat: the tool-side forgiveness patch lives in the shared pi install, outside this repo — a pi upgrade will silently drop it; the brief segment + repo test are the durable half.
