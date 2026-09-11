---
id: hypothesis:l4-the-stream-fragment-argv-resolves-to-executables
mint_id: 398bfb7e64e84d7ea4bb74bf8ccfdfd8
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-stream-goes-live
next_edges: []
edited_by: a00-ede39964
scaffold_hash: 40e4733cab5f1dd4
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ (doc:l4-owner-decisions): bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 27 review by name (wf_6699487e-b72), goal:g15 newest note at 549b8f682, the prime's priority order. Line numbers on 549b8f682. g15-4: extensions/agi/briefs/commands.stream.fragment.md:33 (and the brb/back/panic entries) declare `argv: [<stub>, sb-status]` / `[<stub>, brb]` / `[<stub>, back]` / `[<stub>, panic]` where `<stub>` resolves to the streamer-stub DIRECTORY (/home/ubuntu/work/streamer-stub) — argv[0] is a directory, the HELD stream command group cannot run (reproduced by the review). CLAIM: the fragment is rewritten to real executables — `sb-status` → `~/bin/sb-status` (exists, 131 bytes, exec), `brb`/`back` → `<stub>/bin/hold.sh brb` / `<stub>/bin/hold.sh back`, `panic` → `<stub>/bin/panic.sh` (all exist under /home/ubuntu/work/streamer-stub/bin/) — and the group STAYS HELD and owner_only exactly as declared (L4.124 landed `<stub>` + owner_only in commands.py; the fragment is the only thing that changes). TESTS: the fragment's every argv[0] resolves (after `<stub>` substitution) to an existing executable FILE — asserted against the real paths, the test must NOT monkeypatch the exec away; a `commands.py` dry-run of the group prints the resolved argv and refuses to run it without owner authority. FALSIFIER: an argv[0] that is a directory or absent. NEVER execute panic/hold/live for real. CEILING: 1 kid. FILE SCOPE: extensions/agi/briefs/commands.stream.fragment.md + the test that reads it (extensions/agi/tests/test_commands*.py). EXCLUDED: commands.py logic (landed), the streamer-stub repo, .agi/nodes/.geometry/commands.md."
title: The stream command fragment's argv[0] resolves to an executable, not the stub directory — the HELD group can run
town: streaming-suite
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-stream-fragment-argv-resolves-to-executables

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ (doc:l4-owner-decisions): bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 27 review by name (wf_6699487e-b72), goal:g15 newest note at 549b8f682, the prime's priority order. Line numbers on 549b8f682. g15-4: extensions/agi/briefs/commands.stream.fragment.md:33 (and the brb/back/panic entries) declare `argv: [<stub>, sb-status]` / `[<stub>, brb]` / `[<stub>, back]` / `[<stub>, panic]` where `<stub>` resolves to the streamer-stub DIRECTORY (/home/ubuntu/work/streamer-stub) — argv[0] is a directory, the HELD stream command group cannot run (reproduced by the review). CLAIM: the fragment is rewritten to real executables — `sb-status` → `~/bin/sb-status` (exists, 131 bytes, exec), `brb`/`back` → `<stub>/bin/hold.sh brb` / `<stub>/bin/hold.sh back`, `panic` → `<stub>/bin/panic.sh` (all exist under /home/ubuntu/work/streamer-stub/bin/) — and the group STAYS HELD and owner_only exactly as declared (L4.124 landed `<stub>` + owner_only in commands.py; the fragment is the only thing that changes). TESTS: the fragment's every argv[0] resolves (after `<stub>` substitution) to an existing executable FILE — asserted against the real paths, the test must NOT monkeypatch the exec away; a `commands.py` dry-run of the group prints the resolved argv and refuses to run it without owner authority. FALSIFIER: an argv[0] that is a directory or absent. NEVER execute panic/hold/live for real. CEILING: 1 kid. FILE SCOPE: extensions/agi/briefs/commands.stream.fragment.md + the test that reads it (extensions/agi/tests/test_commands*.py). EXCLUDED: commands.py logic (landed), the streamer-stub repo, .agi/nodes/.geometry/commands.md.

REVIEW L4.143 (parent a00-ede39964): this claim names the rewrite "brb/back -> <stub>/bin/hold.sh brb / <stub>/bin/hold.sh back". THAT SPELLING IS FALSE and must not be re-used. /home/ubuntu/work/streamer-stub/bin/hold.sh:21-25 dispatches on argv[0] basename via case "${0##*/}" in brb), so with argv[0]=hold.sh the literal word brb becomes MODE and falls to hold.sh:81 usage/exit 2 -- it never pauses. The landed fix uses the explicit flags hold.sh --status / --pause / --off, plus <stub>/bin/panic.sh (no flag = hard cut); test_stream_fragment_argv_resolves_to_executable_files (extensions/agi/tests/test_commands.py) reads the REAL fragment and asserts isfile+X_OK AND the flag that reaches each mode, and was mutation-checked against the broken spelling. Outcome of this node: experiment:a00-f2b9aefb-f82039, verdict demoted by review to inconclusive_lean_proved:85 because the claim letter was corrected in flight.
