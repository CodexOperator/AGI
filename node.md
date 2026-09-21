---
id: hypothesis:l4-code-head-is-persisted-on-the-after-join-record-and-the-heal-watch-guards-execv-and-re-execs-only-on-a-changed-head-with-a-clean-tree
mint_id: 58b579bd1c9c46e6943318eab7724f6a
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: 07cd4b1f96f30d2f
season: 2
testable_claim: "goal:g15.25 FIX-ONLY (mur-SL2.25 residue line (b), Prime XVII 20:5xZ — heal watch residues of SL7.89). MEASURED by the Prime on ffcfa4e2f, re-locate on post tip 1d07f3521 (heal.py:941-942 comment; :986 os.execv; rotate.py run_after_join_for_seat's `result['code_head'] = _code_head(root)`): code_head is stamped on the RESULT dict that nobody persists — the record on disk carries no code_head; heal's 'after_join performed' log line (:475) lacks it; the os.execv at :986 raises OSError uncaught (a missing interpreter / EACCES ends the watch loop); a FILE-ONLY identity change with UNCHANGED HEAD (an uncommitted edit) still execs. CLAIM: (1) code_head is written INTO the record's after_join block (through the same pathspec commit that writes results) and printed on heal's performed line ('performed … code_head=<sha>'); (2) os.execv is guarded: OSError is caught, logged by name with errno, and the loop continues on the running bytes (one line, no retry storm — next re-exec attempt only after the next clean-tree code change); (3) the re-exec condition is 'HEAD changed AND tree clean' — a file-only change with unchanged HEAD never execs (state the rule in the docstring); (4) the heal watch's existing tests stay green untouched. FALSIFIERS: code_head absent from the persisted record; an uncaught OSError; an exec on unchanged HEAD. TESTS (append to test_heal_watch.py + test_after_join_service.py, <= 5): (a) record on disk carries code_head after a perform; (b) performed line names it; (c) execv raising OSError -> logged, loop continues (fake execv); (d) unchanged HEAD + dirty file -> no exec; (e) changed HEAD + clean -> exec (existing, keep). FILE SCOPE: heal.py — the watch loop's exec guard + performed line; rotate.py — where the after_join result is persisted (the record write in run_after_join, code_head field only); the two test files. EXCLUDED: the after_join gate/claim (SL7.104), delivery/dm blocks, closeout, cmd_ack. CEILING: <= 40 lines + <= 5 tests; heal + after_join nbhds green."
thought_session: sensei-director-genXVII-L17
title: "heal watch residues (b): code_head is written into the persisted after_join block and printed on the performed line; os.execv OSError is caught and logged and the loop continues; a re-exec needs a CHANGED HEAD and a clean tree — a file-only change never execs"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-code-head-is-persisted-on-the-after-join-record-and-the-heal-watch-guards-execv-and-re-execs-only-on-a-changed-head-with-a-clean-tree

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
