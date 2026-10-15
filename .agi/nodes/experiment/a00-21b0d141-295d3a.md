---
id: experiment:a00-21b0d141-295d3a
mint_id: 33d0b892c4034e6588e4177582cb9c8a
type: experiment
parents:
  - hypothesis:lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot
next_edges: []
confidence: 0.99
edited_by: a00-bade0c21
evidence_runs:
  - experiment:a00-21b0d141-295d3a
loop: hypothesis:lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot@s2
model: stealth/space-bunny-alpha
production_lines: 39
profile: balanced
role: kid
scaffold_hash: b997878832c6cc90
season: 2
title: Re-runnable null-usage trim check finds early-stop replacement
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-21b0d141-295d3a

## Experiment

Added a standalone ESM check that imports the committed context extension, registers its real context handler with a fake `pi`, and invokes it with a null usage, a 26,600-character system prompt, one assistant marker, and two 100,000-character tool results. The check writes its stdout to the configured brain-swap output directory and exits non-zero if any assertion fails.

## Assertions and actual results

| assertion | actual result |
|---|---|
| (a) message count | PASS: `3 === 3` |
| (b) role order | PASS: `["assistant","toolResult","toolResult"]` |
| (c) assistant text | PASS: `"ASSISTANT_MARKER_TEXT"` |
| (d) both tool bodies replaced by the extension placeholder | FAIL: first body is `"[older tool result elided]"`; second remains a 100,000-character body beginning with 40 `y` characters |
| (e) JSON-plus-system estimate below 43,616 | PASS: `31706.75 < 43616` |

The check exits `1`; its stdout is committed at `paths.local_maxxing.brain_swap_out_dir/a00-21b0d141-context-trim-fallback.stdout.txt`. Node's only stderr noise was the repository's package-type warning. `anonymize.py check --text` passed for both the script and stdout. Production size is 39 script lines (45 including evidence output), below the 70-line ceiling.

## Verdict

**Disproved as specified.** The extension stops replacing tool bodies as soon as the estimate is below the limit, so the first replacement is sufficient for this input and the second tool result is intentionally left intact. The weaker invariant (roles/count/assistant retention and the size bound) passes, but the requested both-tool-body replacement does not.

## Largest safe step

Change the extension only if the intended contract is “replace every eligible tool-result body,” then rerun this exact check; otherwise preserve the current bounded-trim behavior and narrow the hypothesis to replacement until under the limit.

## Evidence

- `paths.local_maxxing.brain_swap_out_dir/a00-21b0d141-context-trim-fallback-check.js` — standalone re-runnable check.
- `paths.local_maxxing.brain_swap_out_dir/a00-21b0d141-context-trim-fallback.stdout.txt` — five assertion lines plus exit code.

## Agent Notes
Standalone real-handler check passes length, roles, assistant retention, and 31706.75-token bound, but fails the required both-tool-body replacement because trim stops after the first replacement.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The instruction said to assert that both 100000-character toolResult bodies become the imported extension placeholder, and the machine run of datasets/brain-swap/2026-09-24/a00-21b0d141-context-trim-fallback-check.js returned PASS for length, roles, assistant text, and estimate 31706.75 < 43616, but FAIL for the second body: it remained length 100000. The near miss is treating an early-stop trim as a failure; here the real handler deliberately stops after the first replacement once under the limit, so the test disproves the stronger both-bodies assertion, not the narrower under-slot loop claim. I reran the script and both anonymize checks; the only struggle was the documented anonymize syntax requiring a text argument rather than stdin.
<!-- THOUGHT:END -->

Parent review: accepted the kid as a valid negative probe against the explicit both-tool-body assertion. Evidence is the rerunnable script, exact stdout, exit 1, and anonymize checks; verdict disproved is appropriate for that assertion. It does not refute the parent hypothesis because stopping once under the limit is the claimed mechanism.
