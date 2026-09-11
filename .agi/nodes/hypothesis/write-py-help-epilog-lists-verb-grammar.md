---
id: hypothesis:write-py-help-epilog-lists-verb-grammar
mint_id: be336e08e158423f92437b2c27b4f6e7
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 2da7424eba0117c0
season: 2
testable_claim: "OWNER 2026-09-11 12:4xZ order, master-sensei gen I proposal 6 -- queued behind 1-5, minted after the Prime's reply confirmed engagement with the first batch (applied at 361020232). Grounded in config:rotations `## facts` F4 (sanctuary-director gen XIV calls 22-23: 2 calls spent learning the note verb's grammar from source) and this seat's own template first_turn entry `write-verbs` (`write.py -h | sed -n 1,40p`, present in both director and prime_director templates) which reads the CLI epilog for exactly this purpose. CLAIM: `write.py -h`'s epilog documents `create`'s flags (--parent/--payload/--set/etc.) but never enumerates the 12 verbs a plain `node_id script` edit actually accepts (write.py:406-419: set/unset/link/thought/note/payload/payload_text/patch/body_patch/read/replace/adopt) or their arity (write.py:430-432: e.g. `replace` takes 3 args, `note` takes 1 that absorbs the rest of the chunk as prose) -- confirmed by running `write.py -h` this session: the printed epilog has no verb list at all. A seat wired to read this epilog as its `write-verbs` first_turn fact (both live templates do this today) gets zero grammar from it and still has to grep the source, exactly F4's waste. Add an epilog section (argparse `epilog=` string, appended to the existing help text) listing each verb name, its arity, and a one-line example (`note <text>`, `read A:B`, `replace A:B <file>`, `set k=v`, ...), generated from or kept hand-in-sync with the `VERBS`/`ARITY` dicts so the two cannot silently diverge -- kid's call which, recorded as a deviation if it picks the derived form. FALSIFIER: any of the 12 verbs, or its arity, missing or wrong in the new epilog text when checked against `ARITY`/`VERBS`. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/write.py (argparse epilog / help text only, no verb-logic changes) + its tests."
thought_session: 914d302a-b33f-4c5f-b78d-a8b7320df6c5
title: write.py -h epilog lists every verb's name, arity, and a one-line example
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:write-py-help-epilog-lists-verb-grammar

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
DIRECTOR HARVEST (sanctuary-director gen XIV, L4.230, 2026-09-11 13:49Z). Kept both kids' proved (0.9 / 0.85) and the parent's accept. Ran myself on the round bytes (a00-3a8b9077): `write.py -h` now ends with a `verbs (each accepts a node_id first; join several with &&):` epilog listing every verb with its arity, derived at help-build time from VERBS/ARITY with a fail-closed drift guard (a verb added without an example raises SystemExit at `-h`, which the `bin-help-smoke` test would catch); the single write.py hunk sits inside `main()` (help build only), so no verb logic moved. 147 passed / 1 skipped with neighbours (test_write/test_bin_help_smoke). The `write-verbs` first_turn entry (`write.py -h | sed -n 1,40p`) now needs its range to reach the epilog -- the verbs block starts after the options, past line 40 on this box; a template edit for master-sensei (it may write that once the carve-out lands), noted for it here. write.py lane free: the CARVE-OUT cuts next.
