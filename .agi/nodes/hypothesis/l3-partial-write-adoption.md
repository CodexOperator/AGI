---
id: hypothesis:l3-partial-write-adoption
mint_id: 9062498898d748db91e1340b839d51c4
type: hypothesis
parents:
  - goal:g13.1
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 9bd55933eaff1181
season: 2
testable_claim: After the change, write.py read prints only the requested line range to stdout and leaves the node byte-identical on disk - no edited_by restamp, no body mutation, no grid version - asserted red-first by a test that fails against todays code; brief.py hands the engine-working tiers the patch, body_patch and read verbs with the stdin rule; SKILL.md no longer declares partial writes an open gap; and at least one REAL engine change lands on a build-noded file through write.py patch with edited_by and thought_session stamped and a new grid version cut, shown by command and output rather than by unit test alone.
title: "the partial-write verbs landed and nobody uses them: read silently falls through to the write path and restamps edited_by, no test covers it, brief.py never names the verbs and SKILL.md still calls the gap open"
---
<!-- BODY:BEGIN -->
# hypothesis:l3-partial-write-adoption

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
PARENT SD.14 BRIEF -- SANCTUARY-DIRECTOR GEN V, 2026-09-09, item 54 ADOPTION. READ THIS FIRST; it is your whole task. You ITERATE: spawn a kid, review its node, then judge continue / adjust / done. HARD CEILING 3 kids. Only "done" exits.

THE MECHANISM ALREADY LANDED. DO NOT REBUILD IT. write.py carries three partial verbs today: patch (unified diff onto a payload, fail-closed, routes through replace_payload), body_patch (unified diff onto a node BODY), and read (line-ranged read, verb_read at write.py L290 with _parse_range at L316). Read write.py before designing anything. What is open is ADOPTION, and I measured why.

MEASURED BY ME JUST NOW, so you do not spend a kid re-deriving it. Reproduce each before you change it.

MEASUREMENT 1 -- ADOPTION IS ZERO. Since the patch verb merged (commit a52a08952, L3.43 harvest), 48 engine files changed across 29 commits on season/s2. Recorded uses of patch or body_patch in the whole graph: TWO, and both are the experiment nodes that BUILT the verbs (a00-fd0b0598-b493d7, a00-260a392b-040782). Zero real engine edits have gone through a partial verb. Every one of those 48 files was edited directly, so edited_by, thought_session, the spawn gate and write_guard were skipped on all of them.

MEASUREMENT 2 -- THE READ VERB IS BROKEN, AND IT WRITES. This is the headline finding and it is why nobody adopted it. I ran, against the live tree:
  python3 extensions/agi/bin/write.py build:bin-write 'read payload 290:300'
  python3 extensions/agi/bin/write.py hypothesis:l3-write-partial-diffs-as-writes 'read body 1:6'
Neither printed a single line of content. Both printed "updated: <node-id>". Both MODIFIED THE NODE ON DISK: git diff showed edited_by overwritten to "ubuntu" on both (destroying "season.py" and "sanctuary-director"), and the trailing newline stripped off the hypothesis node body. I reverted both with git checkout; the tree is clean and you start from clean. A READ THAT DESTROYS AUTHORSHIP IS WORSE THAN NO READ VERB AT ALL, and an agent that tried it once would never touch it again.

ROOT CAUSE, ALREADY NAMED, so spend your kid on the fix and not the hunt: verb_read sets edit.read_target and edit.read_range (write.py L311-312) and the emptiness check at L148 counts them, but main() has NO terminal branch that renders the range and returns before submit(). The docstring at L302-305 promises "handled as a terminal verb in main before submit is reached" -- that code was never written. So a read falls straight through the write path: prints nothing, stamps edited_by from _default_actor(), rewrites the file, and would cut a grid version.

MEASUREMENT 3 -- NO TEST COVERS IT. grep of extensions/agi/tests for "read payload", "read body", "read_target", "verb_read" returns NOTHING. The suite is 2241 passed 1 skipped and green WITH this defect live. That is the gap that let it ship.

MEASUREMENT 4 -- THE TEMPLATE NEVER TELLS A KID THE VERBS EXIST. grep -c for body_patch or "write.py patch" in extensions/agi/bin/brief.py returns 0. Every tier is handed set, thought and note only (brief.py L1130-1132 and L1383-1384). A kid cannot adopt a verb it has never been shown.

MEASUREMENT 5 -- THE DOCS STILL DECLARE THE GAP OPEN. skills/agi/SKILL.md lines 281-283 read: "Known gap: payload writes are whole-file only. There is no anchored or partial edit, so a one-line change to a large module still means emitting the whole file". That is now FALSE and it actively instructs agents not to try.

WHAT TO BUILD, in this order.
1. FIX THE READ VERB, RED-FIRST. Write the failing test before the fix: assert that a ranged read prints the requested lines to stdout AND leaves the node file BYTE-IDENTICAL on disk -- no edited_by restamp, no body mutation, no trailing-newline loss, no grid version. Then make it pass with a terminal branch in main() that renders and returns before submit(). Cover payload and body, both bound forms (10:20, 10:, :20), and a refused bad range. A read must never look like an edit.
2. MEASURE THE READ, because the node's own build item 1 demands it and a partial-read feature with no measurement is a claim, not a result. Report bytes and approximate tokens for a ranged read of a real large module against reading it whole. write.py itself is 1005 lines and has a build node (build:bin-write); extensions/agi/bin/level3.py and rotate.py are larger. Put the numbers in your node.
3. TEACH THE TEMPLATE. Add patch, body_patch and read to brief.py where the write.py verb syntax is already documented, for the tiers that do engine work. State the stdin rule plainly: diff bytes arrive by path or by "-", NEVER inline, because a diff contains the doubled-ampersand that the script form splits on. Keep it short -- brief.py is injected into every agent and context is the scarce currency.
4. CORRECT SKILL.md lines 281-283. Replace the stale known-gap paragraph with what actually exists: the three verbs, the stdin rule, and the fail-closed guarantee. Do not inflate it into a tutorial.
5. PROVE ADOPTION LIVE. This is the deliverable that makes the round count, and it is the fix's proof condition, not a restatement of the defect. Land at least ONE of your own real engine changes onto a file that HAS a build node by running write.py patch with a unified diff on stdin -- write.py itself (build:bin-write) is the natural target since you are editing it anyway. Then show the provenance it stamped: the node's edited_by and thought_session after the write, and grid.py versions for that node showing a new version. Paste the exact command and its output. A unit test that the verb applies a diff is necessary and NOT sufficient; the claim is that a real change landed this way.

MUST NOT REGRESS, check each explicitly. The namespace guard in dispatch.py (adapters.assert_model_in_provider_namespace) is a money-safety guard the owner asked for by name -- it must survive untouched. So must kid_ceiling threading, the --prompt-file carry-forward channel, and the fail-closed behaviour of patch and body_patch: a hunk that does not apply must still refuse the WHOLE write and change nothing. Full suite before you report: python3 -m pytest extensions/agi/tests/ -q, and it must be at least 2241 passed 1 skipped plus your new tests. Then links.py links (0 broken), snapshot-goals.py --render --check (byte-identical), grid_coverage_check.py (exit 0), write_guard.py check (silent).

YOUR GUARDRAILS. HARD CEILING 3 kids for your loop. Check the OpenRouter KEY, not the account, before every kid (python3 extensions/agi/bin/provisioning.py status) and stop cleanly at the $1.00 provisioning.min_key_remaining_usd floor -- never lower it. Do not leave a kid or a nested agent running past your own exit: a parent that iterates now spends to its ceiling. Inspect any branch with MERGE-BASE diffs only: git diff $(git merge-base season/s2 BRANCH)..BRANCH answers "what did this branch change"; git diff season/s2..HEAD does NOT and has already falsely shown owner verbatim as deleted. Carry each kid's result into the next kid's brief with dispatch.py --prompt-file. Do NOT push, do NOT merge, do NOT touch season/s2 -- commit locally on your own branch; the director merges. A branch that ends at zero commits ahead has produced nothing as far as every automated reader is concerned.

DO NOT: run level3.py without --dry-run, git rm any node, touch moral:*, write config:seats, run workflow.py run, or launch any seat.

Write your result into THIS node via write.py note labeled "PARTIAL-WRITE ADOPTION" -- the red-first test name, the ranged-read byte and token numbers, the exact write.py patch command that landed a real engine change with its provenance and grid version, the brief.py and SKILL.md diffs in one line each, the suite counts, and the OpenRouter account delta. Note text must not contain a doubled-ampersand sequence: the script parser splits on it and your note will silently not land. If the live adoption proof does not pass, say so plainly and report how far it got -- a truthful partial beats a claimed pass.
