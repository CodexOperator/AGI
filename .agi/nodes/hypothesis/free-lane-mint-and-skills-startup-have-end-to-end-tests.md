---
id: hypothesis:free-lane-mint-and-skills-startup-have-end-to-end-tests
mint_id: be696b18df884036a528a038429c6274
type: hypothesis
parents:
  - goal:g1.27
next_edges: []
edited_by: a00-f38a455b
scaffold_hash: fc5927f37ae403ef
season: 2
status: measured
testable_claim: "Two committed tmp_path tests: (a) dispatch.main() with a drained balance and a zero_usd harness mints a key capped at zero_usd_key_limit while a paid harness is refused by the account floor; (b) the live templates skills first_turn cmd exits 0 under its byte_cap, names EVERY skills/agi-* dir on the trunk (NO exemption - a named omission is RED, fix site config:rotations rotations.md 83 and 123), and every build node it names RESOLVES in the graph via node_writer.find_node_file."
title: "The free-lane mint on a drained account and the skills first_turn entry have end-to-end tests (assigned: director-engine)"
town: core
---
# hypothesis:free-lane-mint-and-skills-startup-have-end-to-end-tests

# hypothesis:free-lane-mint-and-skills-startup-have-end-to-end-tests

PASS 11 engine-delta-1 defect 4 + missed 5 (the 5 zero-usd tests cover can_fund and the mint payload only, never dispatch.main) and engine-delta-2 missed 3 + UNVERIFIED (ten flow skills + the skills entry landed with zero test coverage; nothing runs a first_turn cmd).

## Agent Notes
Assigned to **director-engine**. Parent: goal:g1.27 (PASS 11).

## BRIEF DH.674 (director-engine, from belam [decision] 23:0xZ: goal:g1.27 PASS 11) -- queued AFTER DH.671-673 so it tests their bytes
Dispatch line  config-max: the tests read zero_usd_key_limit and the first_turn byte_cap from their cells, never a literal · template-max: none · code: tests only
FALSIFIERS (a) dispatch.main() on a drained balance + zero-usd harness does not mint at zero_usd_key_limit, or a paid harness is not refused · (b) the live templates' skills first_turn cmd exits non-zero, exceeds its byte_cap, or omits a skills/agi-* dir present on the tree
TESTS      two new files: extensions/agi/tests/test_free_lane_dispatch_main.py · extensions/agi/tests/test_skills_first_turn_entry.py -- tmp_path graphs, a faked provider (no network, no real mint), never a live pane or seat -- + test_dispatch.py test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE)
FILE SCOPE the two new test files · the kid's own node (a production defect the tests expose = NAME it on your node, never fix it here)
CEILING    HARD CAP: 1 kid · 0 production lines · <= 120 test lines (two files) · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
ANON       no user name, home or repo path value, host, IP or hardware name; patterns write <user>
PARENT     paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit AND every node/config edit on the loop branch before you exit


## OPEN at the 2026-09-28 merge-up (director-engine; belam [decision] 00:0xZ: in-progress included)
STATUS    MEASURED, bytes landed, suite GREEN on the EG.150 cut (f9fbf587a). DH.674 (experiment:a00-77faeb4c-e043fa, merged at a71c05502) built the two tmp_path suites; EG.87 (experiment:a00-59be3549-a3443e) de-circularised them (fixture cap DIFFERS from DEFAULT_ZERO_USD_KEY_LIMIT_USD, so a literal at the mint site is RED); EG.124 (experiment:a00-e5b926db-80ea64) replaced the OMITTED_DEFECT exemption with the STRICT shape -- the skills entry must name every skills/agi-* dir and every build node it names must RESOLVE, with no exemption left in the suite; EG.150 (experiment:a00-f38a455b-d5028f) split the free-lane assert onto the TRUNK's real gate split (the two DOLLAR floors absent AND the provisioning-ABSENT runtime-key gate PRESENT, mutation-pasted) and added the converse leg (a dead runtime key refuses a zero_usd lane and mints nothing). The suite is green today because the live cell names agi-corrective (ee82066ec) -- there is no tolerance mechanism left for a reader to rely on.
ROUNDS    this post's rounds on this node: DH.674 (merged), EG.87 (corrective, 1 kid), EG.124 (corrective, 1 kid), EG.150 (corrective, 1 kid). Bytes live on the loop branch, never the post branch, until its mur clears.


## CORRECTIVE DH.EG.87 -- closes mur-eg-23 DH.674 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-free-lane-mint-and-sk-a00-43384a01 tip a71c05502 (branch de-base-EG.87; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. Tripwire: the coverage assert equals the one-element OMITTED_DEFECT, so the commit that adds the missing clause turns the suite red unless it also edits the test (test_skills_first_turn_entry.py:74)
2. Dead-clause blind spot: the `;`-chained cmd rc is the last clause's and named-minus-present is never asserted, so a clause naming a removed skills/agi-* dir passes silently (test_skills_first_turn_entry.py:58)
3. Ceiling overage: 221 test lines against the brief's HARD CAP of 120 (test_free_lane_dispatch_main.py:1)
4. Parent hypothesis node still says 'IN PROGRESS, not landed ... DH.674 QUEUED (not yet dispatched)' with status open while its disproved kid is merged (free-lane-mint-and-skills-startup-have-end-to-end-tests.md:1)
5. The round's central conjunct (a) config-max claim is CIRCULAR and therefore unfalsifiable as written: the fixture writes provisioning.zero_usd_key_limit_usd = 0.01 (extensions/agi/tests/test_free_lane_dispatch_main.py:34), the test reads `cap` from that same cell (:114-115) and asserts mints[0]["limit"] == cap (:120) -- but DEFAULT_ZERO_USD_KEY_LIMIT_USD is 0.01 (extensions/agi/bin/provisioning.py:109), so replacing the cell read at the dispatch/mint site with the literal 0.01 passes BOTH tests. The only cell-variation test (:135-143) exercises the READER provisioning.zero_usd_key_limit(root), never the dispatch path that builds the mint payload. Nothing in the round proves the minted limit comes from the cell rather than a literal, which is exactly what the brief demanded ('config-max: the tests read zero_usd_key_limit and the first_turn byte_cap from their cells, never a literal', parent node:26); the node's mutant check removed the SKIP clause (dispatch.py:2350), not the cell read. One-line fix: a fixture cap that differs from the default (e.g. 0.07) makes a literal red. Residue.
6. test_the_cap_and_the_floor_come_from_cells_not_literals names and docstrings the FLOOR but its body varies only zero_usd_key_limit_usd and asserts only the cap (extensions/agi/tests/test_free_lane_dispatch_main.py:135-143). The two paid floors the sibling test actually depends on -- min_mint_remaining_usd and min_account_remaining_usd (:35-36) -- are never varied and never asserted. A test whose name claims a property its bytes do not exercise. Residue.
7. The paid-lane refusal is asserted only as rc == 1 (extensions/agi/tests/test_free_lane_dispatch_main.py:129) while check_account_floor is stubbed to return the specific reason 'account floor 0.005 below 1.6' (:90-91) that no assertion ever inspects. Any refusal that still runs the two floors satisfies the test, so 'refused BECAUSE the account is drained' is not pinned. Residue.
8. _dispatch mutates the global sys.argv without monkeypatch and never restores it (extensions/agi/tests/test_free_lane_dispatch_main.py:103), so every later test in the same session inherits an argv naming a tmp_path pytest has already torn down. House pattern (extensions/agi/tests/test_ring_cli_seam.py:146 does the same), so residue rather than a new defect -- but the new file is the cleaner place to fix it with monkeypatch.setattr(sys, 'argv', ...).
9. The live omission (config:rotations skills entry lacks skills/agi-corrective) is NOT yours to fix -- the director banks it for the cell's owner. Pin it so the FIX turns a test GREEN, never red: e.g. an xfail(strict=True) naming the omission, or an assertion on the set difference, so adding the clause needs no test edit.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees (belam [red] 06:56Z: two such searches held io PSI at 84)
TESTS     test_free_lane_dispatch_main.py test_skills_first_turn_entry.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_free_lane_dispatch_main.py · extensions/agi/tests/test_skills_first_turn_entry.py · .agi/nodes/experiment/a00-77faeb4c-e043fa.md · .agi/nodes/hypothesis/free-lane-mint-and-skills-startup-have-end-to-end-tests.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · 0 production lines net over a71c05502 · test lines net <= 0 over a71c05502 (the round is already +221 vs its 120 cap: every fix is paid for by cutting duplicated setup) · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat a71c05502 <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE DH.EG.124 -- closes mur-eg-33 EG.87-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-free-lane-mint-and-sk-a00-befd213e tip 37a5a2f85 (branch de-base-EG.124; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. OUTSIDE, INFORMATION ONLY: the live skills first_turn entry (config:rotations, .agi/nodes/.geometry/rotations.md) omits agi-corrective; that cell is belam's/thought-master's and the director has banked it for them -- NEVER edit rotations.md. Keep OMITTED_DEFECT; item 4 makes it self-expiring.
2. 2. Hypothesis testable_claim (b) still asserts 'names every skills/agi-* dir on the trunk' while the shipped test exempts one dir
3. 4. The rc check cannot see a dead mid-chain clause (rc comes from the last clause; the regex only matches skills DIRS) - false negative on a renamed/removed build node
4. 5. OMITTED_DEFECT has no staleness assertion (test_skills_first_turn_entry.py:23) - a manual TODO, so a later re-deletion of the clause is invisible
5. RECORDED CEILING BREACH (TMM.315), NO ACTION: 221 test lines vs the prior brief's cap 120 stays a recorded residue -- never delete test lines to meet it.
6. experiment:81 names `.agi/context/config.json` as the file holding the live skills first_turn clause. That file DOES NOT EXIST (`ls .agi/context/config.json` -> No such file or directory). The real cell is `.agi/nodes/.geometry/rotations.md` (frontmatter id `config:rotations`), lines 83 and 123. Only the address on the same line rescues a fixer; a fixer who follows the named path lands nowhere, and the residue the round hands the merge-up (item 1's fix site) is mis-pointed. Mechanism, not wording: `ls` plus rotations.md:2 `id: config:rotations`.
7. The mutation proof is only half re-runnable and the first reviewer treated it as settled. experiment:55 claims 'On the tip bytes that same mutation is GREEN (3 passed)' - confirming it requires editing provisioning.py, which a reviewer may not do. UNVERIFIED-BY-RUN, mechanism-confirmed instead: the cut fixture wrote `"zero_usd_key_limit_usd": 0.01` (a71c05502:test_free_lane_dispatch_main.py:34) and the mint site reads `if zero_usd: limit_usd = zero_usd_key_limit(root)` (provisioning.py:874), so a literal 0.01 at that site is indistinguishable from the cell. Probe I would run and did NOT: copy the tip tree, replace line 874 with `limit_usd = DEFAULT_ZERO_USD_KEY_LIMIT_USD # MUTANT`, run the two files, `cmp` the restore.
KIDBRIEF  (mur-eg-31 EG.97 parent finding: the corrective reached the parent only, so the kid wrote code over a 0 cap) -- PARENT: dispatch your kid with --orders pointing at a file holding THIS WHOLE SECTION, and paste its FILE SCOPE + CEILING into the kid prompt; verify the kid's context carries the word CORRECTIVE before it starts.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees (belam [red] 06:56Z: two such searches held io PSI at 84)
TESTS     test_free_lane_dispatch_main.py test_skills_first_turn_entry.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_free_lane_dispatch_main.py · extensions/agi/tests/test_skills_first_turn_entry.py · .agi/nodes/experiment/a00-59be3549-a3443e.md · .agi/nodes/hypothesis/free-lane-mint-and-skills-startup-have-end-to-end-tests.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 37a5a2f85 · <= 40 test lines net over 37a5a2f85 · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat 37a5a2f85 <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE DH.EG.150 -- closes mur-eg-54 EG.124-k1 accept_with_residue (no verify)
BASE      CUT FROM de-cut-EG.150 tip f9fbf587a = the director-engine post (trunk-synced, TMM.344) merged INTO the EG.124 chain tip d8f6236a6 (merge-resolution round, TMM.329; branch de-base-EG.150). No further merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. The merge turns a round test RED -- measured by the director on the cut f9fbf587a: `pytest -q extensions/agi/tests/test_skills_first_turn_entry.py extensions/agi/tests/test_free_lane_dispatch_main.py` = 1 failed, 6 passed; FAILED test_free_lane_mints_at_the_zero_usd_cell_cap_on_a_drained_account (`assert not ['runtime_key']`). The skills guard is GREEN on this cut (the live cell names agi-corrective since ee82066ec). Make the free-lane test agree with the trunk's mint path, naming on your node which side (the trunk's zero-USD mint or the round's fixture) is the source of truth and why; never weaken the assert.
2. Hypothesis body still asserts the DELETED tolerance mechanism -- .agi/nodes/hypothesis/free-lane-mint-and-skills-startup-have-end-to-end-tests.md:36 -- Frontmatter testable_claim (:12) was rewritten to the strict shape, but the body's STATUS line still says the entry 'TOLERATES the one live omission so adding the clause needs no test edit' and the THOUGHT (:40) still argues 'the correct shape tolerates a NAMED omission' — the exact mechanism item 4 deleted. A reader of the hypothesis node is told the suite is green today; it is red. The body is director-owned and was not in the round's file scope, so the harvest should have caught it. The ROUNDS list on the same line also omits EG.124.
3. Standing test-line ceiling unreconciled (241 vs the node's own 120 cap) -- extensions/agi/tests/test_skills_first_turn_entry.py:91 -- The BRIEF on the same node (line 30) sets 'HARD CAP ... <= 120 test lines (two files)'. Measured at the tip: 91 + 150 = 241 (the kid's arithmetic 221 -> 241 is correct; the cut file is 71). The round's own delta is +20 net (30/10 numstat), inside its 40 cap, and no line was deleted to buy it — disclosed as recorded residue, never reconciled against the standing cap. The kid carried the proof that the 20 lines buy a real blind-spot cover, so this is a bookkeeping residue, not a defect in the bytes.
DEMOTED   by the director at triage, not orders: items 1 (the by-design skills red: closed on the trunk by ee82066ec, green on this cut; TMM.344) · 4 (the director landed an accepted round's uncommitted in-scope kid edit by the recorded rule)
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees (belam [red] 06:56Z: two such searches held io PSI at 84)
TESTS     test_skills_first_turn_entry.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_free_lane_dispatch_main.py · extensions/agi/tests/test_skills_first_turn_entry.py · .agi/nodes/experiment/a00-59be3549-a3443e.md · .agi/nodes/experiment/a00-e5b926db-80ea64.md · .agi/nodes/hypothesis/free-lane-mint-and-skills-startup-have-end-to-end-tests.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over f9fbf587a · <= 40 test lines net over f9fbf587a · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat f9fbf587a <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE DH.EG.169 -- closes mur-eg-x1305298-83f469 EG.150-k1 accept_with_residue (TEXT-FIX KID, skill agi-corrective 3a)
BASE      CUT FROM season2/loops/hypothesis-free-lane-mint-and-sk-a00-af643b89 tip 2b866de03 (branch de-base-EG.169). No merge. Never rebase.
TRIAGE    verify wins: review R1-R4 refuted by the verify stage (dropped) · every kept item is PURE TEXT (node prose or a docstring): no behaviour, test logic or config changes
DEMOTED   by the director at triage: verify V5 (the converse leg fakes available()=True) = a NOTE, severity note, no false claim in the bytes
Pointers below were re-read by the director at 2b866de03 (git show 2b866de03:<path> | sed -n A,Bp).
1. STALE SENTENCE -- .agi/nodes/experiment/a00-e5b926db-80ea64.md, the "Corrective EG.124:" paragraph (tip line 172) says "suite RED on the live agi-corrective omission by design"; the CORRECTION section above it ("the expected red is GONE") refutes that. Fixed = the sentence says the red was expected then and is gone now (cite the CORRECTION heading), via write.py.
2. STALE SENTENCE -- same node, the "CAVEAT I accept from the kid:" line (tip line 178) says the tree "now carries ONE expected red"; the same CORRECTION refutes it. Fixed = marked as history superseded by the CORRECTION, via write.py.
3. FALSE LINE -- .agi/nodes/experiment/a00-f38a455b-d5028f.md, the bullet starting "The hypothesis node body no longer records the OMITTED_DEFECT history ANYWHERE (probe D)" (tip line 190): the hypothesis node carries OMITTED_DEFECT 4 times. Fixed = the bullet states the truth, settled by PASTING the output of: git grep -c OMITTED_DEFECT <your tip> -- .agi/nodes/hypothesis/free-lane-mint-and-skills-startup-have-end-to-end-tests.md
4. STALE HEADER COMMENT -- extensions/agi/tests/test_skills_first_turn_entry.py, the "# NO OMITTED_DEFECT EXEMPTION." comment block (tip lines 19-25) says "the suite is RED on purpose until the clause is added at the fix site". The clause is added; the file passes. Fixed = the comment says the fix site now names agi-corrective and the test guards against its removal; settled by PASTING the pytest summary line of that file.
5. UNDERSTATED DOCSTRING -- extensions/agi/tests/test_free_lane_dispatch_main.py module docstring, the sentence "No network: credit_balance and the create call are the only fakes." (tip lines 5-6). The harness also fakes adapters.load, subprocess.Popen/run, the grace sleep, provisioning.available, the key reader, the mutation guard and the key checks. Fixed = the sentence says it is a dispatch-path proof with every I/O boundary faked (name them by function, no line numbers).
TEXT RULES NUMSTAT SELF-REFERENCE: never paste a numstat that includes the commit it is pasted in -- measure <cut>..<tip before the paste commit>, labelled so · ANCHOR RULE: a cite names a function / heading / cell key / quoted sentence, a line number only where the claim IS the line · every number on your node is a PASTED command output
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees
TESTS     test_skills_first_turn_entry.py test_free_lane_dispatch_main.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_skills_first_turn_entry.py (comment only) · extensions/agi/tests/test_free_lane_dispatch_main.py (docstring only) · .agi/nodes/experiment/a00-e5b926db-80ea64.md · .agi/nodes/experiment/a00-f38a455b-d5028f.md · the kid's own node (all nodes via write.py)
CEILING   HARD CAP: 1 kid · 0 production lines · <= 16 test-file lines changed, comments/docstrings only · 0 USD -- a code byte or a line over = the round is cut · paste `git diff --numstat 2b866de03 <tip before the paste commit>` on your node
KID       COMMIT every edit (files AND nodes) on your branch before you exit (cli.py done)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective EG.169: mur-eg-x1305298-83f469 EG.150-k1 residues batched into one corrective (orders above, generated from the verdict files).

EG.150: a red round test is a claim about which side is stale, and the owner-dated comment in the BYTES settles it -- the trunk says a ZERO-USD lane skips the two DOLLAR floors and keeps every other gate, so the fixture was the stale paraphrase and the test is the thing to fix. Fixing it by asserting the real split (floors absent AND the runtime-key gate PRESENT, plus the converse leg: a dead runtime key still refuses) TIGHTENS rather than weakens: the old single "no gates ran" assert would have gone GREEN on a mutant that de-indents the gate away. An exemption is a promise a later reader cannot check; the strict suite that is green because the cell was fixed is the same green with the receipt attached.
<!-- THOUGHT:END -->
