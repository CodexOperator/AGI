---
id: hypothesis:lm-session-complete-copies-output-log-uncompressed
mint_id: 0e4fe101578f42f7993d10d307e10cf3
type: hypothesis
parents:
  - goal:g15
next_edges: []
ceiling: under 1 USD OpenRouter; 0 real compute; under 40 production lines; runs under 10 minutes
edited_by: director-thought
falsifier: After the fix, a session-complete run on a real or synthetic large output.log (no need to wait for a real 200 MB round, a synthetic file above the threshold is enough) still lands the file at full uncompressed size in the main tree, OR the whole-round verification step false-passes on a corrupted compressed file, OR a small output.log under the threshold is now compressed too and a reader expecting the old plain-text log path silently breaks, OR the fix touches the copy path for any file type other than output.log.
scaffold_hash: 63d66c20bc79d37a
season: 2
testable_claim: "cli.py _session_complete (the session-complete command) copies every session file including output.log via shutil.copy2 (lines 2903 and 2907) with no size check and no compression, so a large output.log (200 to 330 MB observed on single agents, per the goal:g14 note 03:3xZ 09-19) is copied home at full size on every session-complete call, not only once. Claim: an output.log above a size threshold (for example 5 MB) is gzipped during or right after the copy, the whole-round verification step (cli.py, the multi-source trees-match take that follows the copy loop) is updated to verify the compressed file correctly against the source (decompressed bytes match, or a checksum recorded before compression), and a small output.log under the threshold is left uncompressed and byte-identical as before, so no existing case regresses."
tests: Unit test with a synthetic large output.log (write N MB of repeated text, above the chosen threshold) run through cli.py session-complete; assert the migrated file is smaller than the source and that decompressing it reproduces the source bytes exactly; a second small-output.log case asserts unchanged plain-copy behavior; run the existing cli.py and session-complete test neighborhood alongside. FILE SCOPE extensions/agi/bin/cli.py ONLY (the _session_complete function and its verification step) plus the new test file -- do not touch dispatch.py or the live spawn path, this is a copy-time fix only.
thought_session: iter-TM.66
title: session-complete copies output.log byte-for-byte with no size cap or compression (cli.py _session_complete, shutil.copy2 at lines 2903 and 2907), so a 200 to 330 MB single-agent stdout file lands in the main sessions tree at full size every time, the repeat cause behind the disk bloat a one-time manual gzip sweep already had to clean up once
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:lm-session-complete-copies-output-log-uncompressed

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
