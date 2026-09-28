---
id: hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes
mint_id: 8d3f4fbac3104be29da7e895a6c95a34
type: hypothesis
parents:
  - goal:g7.33.18.1
next_edges: []
edited_by: director-engine
scaffold_hash: d1bd18074c8a2550
season: 2
testable_claim: "every piece of goal:g7.33.18's table is a template + manifest entry under paths.boxkit.templates_dir that renders to the live local-town bytes, with no literal host/path and anonymize clean (assigned: director-engine)"
title: Box memory guard pieces are repo templates that render to the live bytes
town: core
---
# hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes

## Measured
- goal:g7.33.18 (TMM.265, OWNER 20:4xZ): the box-level memory-watch pieces live only on local-town, hand-installed; encryption-town must install the same stack sized to its RAM from ONE kit in the repo. The node's table lists every piece and its measured value on local-town (15932 MiB RAM, 4095 MiB swap).
- Config cells committed by the director at 3b42eb930: paths.boxkit.{templates_dir, install_root, sbin_dir, systemd_system_dir, systemd_conf_dir, user_systemd_dir, watchdog_conf}.

## CLAIM
Every piece in goal:g7.33.18's table (user@ / oomd / user.slice / user-UID.slice / system.slice drop-ins, agi.slice, agi-memguard.py + agi-memguard.service, the 10-agi-survival no-cascade drop-ins, watchdog.conf + sanctuary-health) is a template under paths.boxkit.templates_dir with manifest.json per the KIT CONTRACT; rendering each with local-town's measured values reproduces the live file byte-for-byte; no template carries a literal host, address, hardware name or path; anonymize check is clean.

## Dispatch line
config-max: every path is a paths.boxkit cell, every sized knob a values.boxkit cell (the director commits them) / template-max: the pieces themselves ARE templates / code: manifest.json + a tiny render helper (placeholder substitution, refuses an unfilled placeholder by name).

## FALSIFIERS
- a rendered template differs from the live file it was copied from (the test fixture holds the live bytes with host tokens already replaced);
- anonymize.py check flags a template;
- a template contains an unlisted placeholder, or a manifest placeholder the template never uses.

## TESTS
extensions/agi/tests/test_boxkit_templates.py: render every piece against a committed fixture of local-town's measured values and diff against a committed ANONYMIZED copy of the live bytes; manifest schema row; unfilled-placeholder refusal row. + test_anonymize*.py neighbourhood.

## FILE SCOPE
extensions/agi/boxkit/** (templates, manifest.json, render helper) · extensions/agi/tests/test_boxkit_templates.py · extensions/agi/tests/fixtures/boxkit/**. Never .agi/config.json.

## CEILING
<= 3 kids · <= 12 production lines per conjunct where code is new logic (template bytes do not count) · pi-free tier-0 · 0 USD.

## THE KIT CONTRACT (shared by g7.33.18.1/.2/.3 -- fixed by the director; a change is a [rule] line to the director, never a local edit)
- Templates live under the cell `paths.boxkit.templates_dir` (repo-relative), one file per live piece, `{{UPPER_SNAKE}}` placeholders for every SIZED value and every host-specific token.
- `<templates_dir>/manifest.json` = {"pieces": [{"name", "template" (relative to templates_dir), "dest_cell" (a key of paths.boxkit: sbin_dir | systemd_system_dir | systemd_conf_dir | user_systemd_dir | watchdog_conf), "dest_rel" (under that dir; "" when dest_cell names a file), "mode" (octal string), "sudo" (bool), "placeholders" [names], "reload" ("system" | "user" | "none")}]}.
- Every destination = install_root (cell paths.boxkit.install_root, "/" live, a tmp dir in every test) joined with the dest_cell value (`{home}` expanded) and dest_rel. NO literal path anywhere in code.
- SIZING (goal:g7.33.18): (g7.33.18 v2, 9b03554ac) user@ MemoryMax = MemTotal - held_outside_user - the box's MEASURED system reserve (an INPUT per box: local-town ~1.9 GiB, encryption-town 942 MiB -- never a fixed 2 GiB; the installer takes it as a flag/cell, the probe derives it from the installed MemoryMax) · MemoryHigh = 0.9 x MemoryMax · MemorySwapMax = 0.5 x swap · agi.slice MemoryHigh / MemoryMax = 0.63 / 0.70 x user@ MemoryMax (reproduces 4639/5155 MiB on local-town) -- the numeric knobs are cells under values.boxkit.* the director commits; name any you need in THOUGHT.
- FENCES (every round, every kid): NEVER run an install for real on this box -- no sudo, no systemctl start/stop/enable/daemon-reload, no write under /etc, /usr, ~/.config/systemd, no crontab write. Reading live files and `systemctl show` read-only is allowed. Every test uses a tmp install_root and a stubbed systemctl. Copied bytes pass `python3 extensions/agi/bin/anonymize.py check`: a host name, address, hardware name or key id becomes a placeholder. Every pytest `timeout 600 prlimit --nproc=300`, named files, --basetemp under /tmp; no test spawns pytest; kids never launch real claude.
- The director commits .agi/config.json cells; a round NEVER does (cli.py refuses it) -- write the cells you need in THOUGHT with their values.

## CORRECTIVE DH.530 -- closes mur-director-engine-17 DH.504-k1..k4 (verify: accept_with_residue x3 + unstructured, the same residues in every slice)
BASE      CUT FROM season2/loops/hypothesis-box-memory-guard-piec-a00-e20a597b tip 80113e993 (worktree a00-e20a597b). No merge. Never rebase. NEVER DH.432 itself.
0 production lines: the test file and nodes only. The round SHRINKS the test file.
1. Row 14 (test_boxkit_templates.py:940-969) is vacuous: anonymize.scan is a literal `v in text` over the denylist VALUES (bin/anonymize.py:72-74) and the fixture denylist is FAKE_BOX, so no kit byte can ever red it -> keep ONE row that is able to go red on a KIT byte: copy a template into tmp, plant one FAKE_BOX value in it, assert scan names it; the unplanted kit stays clean. Delete the rest of the 89-line row. Correct the file header (:51-57) and a00-0acacf93's text that credit it with guarding 'every template byte'.
2. _uncovered's general branch (test:761-763) never reads p['dest_cell'] -> read it; one row: a same-relative piece in the WRONG cell does not cover.
3. test:940 `ANONYMIZE = _load_bin("anonymize")` at IMPORT does sys.path.insert + sys.modules[name] = mod (test:113-120) -> load inside a fixture that restores both; prove it by running test_anonymize_guard.py in the SAME pytest session after this file (a00-0acacf93 reported 7 failures that way).
4. The '/a/b' case (test:876-881) is green under the old AND new rule -> replace it with a case the old `len(p.parts) >= 3` rule gets wrong.
5. Nodes (write.py): a00-cfbbb97e-297f01 prints P5 and the cells[0] fragility as open (a00-f0bbeb3a closed both at rows 11d/11e) -> mark closed; a00-f0bbeb3a cites '_uncovered line 739' (a docstring line; the branch is :761) -> correct; a00-0acacf93-aa4632 :67 prints the checkout root's absolute path value -> write `<repo>` instead (ANON).
ANON      no user name, home or repo path value, host or IP; patterns write <user>; paths write <repo>
TESTS     test_boxkit_templates.py test_anonymize_guard.py (the SAME session, that order) test_bin_help_smoke.py once (timeout 600, --basetemp under /tmp)
FILE SCOPE extensions/agi/tests/test_boxkit_templates.py · experiment:a00-0acacf93-aa4632 · a00-cfbbb97e-297f01 · a00-f0bbeb3a-46e50b (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · 0 production lines · test file net <= 0 vs the base (row 14's 89 lines pay for items 2-4) · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit

## CORRECTIVE DH.580 -- closes mur-director-engine-26 DH.530-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-box-memory-guard-piec-a00-d3d5ead8 tip b32e952ea (branch de-base-580; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 2. UNIT_DIRS hard-codes the tails of two committed boxkit cells (test_boxkit_templates.py:702) — a cell rename inverts _cell_fits_dir silently
2. Lost falsifier, prose-only now: the collapse deleted the only row that pinned the row-4 / anonymize DISJOINTNESS. At base, test_row_14_sees_what_row_4_cannot_and_is_not_a_restatement_of_it (80113e993:973) asserted, per class, scan(planted)==[cls] AND _leaks(planted)==[], plus the checkout root the other way round. After the diff the only scan caller is test_one_planted_kit_copy_goes_red_and_the_kits_own_bytes_stay_clean (test:975-992) and _leaks is called only from rows 4 and 12 — no row asserts that a hostname/ip/mac/board/secret token passes the bespoke denylist CLEAN, yet the file header (test:49-51) and the node table (a00-0acacf93:60-67) still state the disjointness as fact. A future merge of the two denylists is again a silent no-op, which was the deleted row's stated purpose. Residue, not demote: the order asked for one row and the property is measured true.
3. Item 3's sys.path half is inert inside pytest, so the node's claim is wider than the bytes: extensions/agi/tests/conftest.py:408-409 already inserts bin/ on sys.path and :411 imports locations before any test module loads, so under a session the fixture's sys.path restore (test:949-954) is a no-op and only the sys.modules['anonymize'] unbind can matter. The corrected body (a00-0acacf93:83-85) and the parent's P1 gate ('sys.path unchanged / anonymize in sys.modules: False') were measured in a BARE interpreter, not in a pytest session where conftest has already done both. The fix is still a strict improvement; the contamination it names is real by construction (base: BIN_DIR on sys.path True, anonymize bound True).
4. New residue introduced by this diff: _leak_roots_by_depth (test:856-859) keeps the REJECTED `len(p.parts) >= 3` rule alive in the file and row 12 pins its wrong answer verbatim (test:873 `assert _leaks("cd /a and ls\n", old) == []`). Legitimate as a comparison oracle and red-first is real (on Path('/a') the old rule yields [], the new yields ['/a']), but it means a later correct fix of that helper would red a passing row for the right reason at the wrong place. Named, not blocking.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_boxkit_templates.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_boxkit_templates.py · .agi/nodes/experiment/a00-0acacf93-aa4632.md · .agi/nodes/experiment/a00-c8edb94f-25553f.md · .agi/nodes/experiment/a00-cfbbb97e-297f01.md · .agi/nodes/experiment/a00-f0bbeb3a-46e50b.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over b32e952ea · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.591 -- closes mur-director-engine-30 DH.580-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-box-memory-guard-piec-a00-58431684 tip 88415ed96 (branch de-base-591; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. Direction-2 disjointness assertion is unfalsifiable under the fake denylist (extensions/agi/tests/test_boxkit_templates.py:1032)
2. The new session-state assertion is true by construction of the fixture it runs inside (extensions/agi/tests/test_boxkit_templates.py:1016)
3. The node's OWN red-first for direction 2 is self-referential, not a merge: .agi/nodes/experiment/a00-19870cd0-134fe5.md:85-93 reports 'probe C (the guard's "sees the root" assertion flipped) 5 failed, 1 passed' -- flipping the asserted expression, and the parent's THOUGHT at :165 and :175 states the property as 'the engine stays blind to the checkout root', which is the tautology, not a falsification. My production-branch merge (anonymize.py:49) leaves row 14b green, so the test comment 'RED if merged' (test:1021-1022) is unsupported by the round's own evidence. Same defect class the parent already recorded on this hypothesis at experiment:a00-0acacf93 probes P8/P9 ('a node whose title promises a check that its bytes cannot perform').
4. Hand-kept row index drifted in the same commit: the file header (test:1-61, 'Rows 1-13, one per clause ... 14:') never lists 11g or 14b, while the file's own comments cite them by number (test:704 'row 11g', test:864, test:1021) and the node cites ':866' and ':1024'. One source per rule: the inventory is a second copy of what the file already says, and it was already wrong one commit after being written.
5. Undisclosed widening in the derived rule: UNIT_DIR_CELL (test:705) matches ANY cell value ending /systemd/<component>, so a future *drop-in* dir cell (e.g. etc/systemd/system.conf.d) would be read as a UNIT dir and _cell_fits_dir (test:713-719) would ACCEPT a piece the old literal pair rejected -- a loosening, the opposite of the caveat the node discloses (a00-19870cd0:147-149 names only the missing-coverage direction). Harmless today: I recomputed the committed cells and _unit_dir_tails() == {'systemd/system','systemd/user'}, identical to the removed UNIT_DIRS, so 0 manifest rows change verdict; and row 11g is genuinely falsifiable (reverting _unit_dir_tails to the literal red at test:873, matching the node's red-first claim).
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_boxkit_templates.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_boxkit_templates.py · .agi/nodes/experiment/a00-0acacf93-aa4632.md · .agi/nodes/experiment/a00-19870cd0-134fe5.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 88415ed96 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.615 -- closes mur-director-engine-33 DH.591-k1 accept_with_residue (no verify)
BASE      CUT FROM season2/loops/hypothesis-box-memory-guard-piec-a00-36e29ed9 tip 1247ad570 (branch de-base-615; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. row 14b's kit half is tautological: the planted root is read from the set _leaks itself scans -- extensions/agi/tests/test_boxkit_templates.py:1040 -- `assert _leaks("cd %s\n" % root)` with root = LEAK_ROOTS[0] (test:1036) and _leaks' default roots=LEAK_ROOTS (test:149) is true by construction -- the same 'no state can make this false' class item 1 removed one line above; the node's table claim that 'the row's two halves are both reachable' is false, and the parent review records only the degenerate IndexError case, not the vacuity.
2. director item 4 not fixed: the header still enumerates the row index and the enumeration is wrong -- extensions/agi/tests/test_boxkit_templates.py:4 -- '7b-7d, 11a-11g, 14b' -- no row 11a exists, 6b-6e and 7f are unlisted, and test:44 still cites 'test 10b' which has no sub-row; the range rewrite is the same second copy, one row wrong on arrival, and the node body claims it was deleted.
3. experiment:a00-19870cd0 keeps a body claim this same commit falsifies, under an unchanged verdict=proved -- .agi/nodes/experiment/a00-19870cd0-134fe5.md:168 -- The trailing 'PARENT PROBES (a00-58431684) ... gate/P2 -- the MERGE counterfactual reds (_leaks names the value once LEAK_ROOTS gains it)' and 'All five are in the diff. Accepted 1 / demoted 0 / failed 0' survive in the body while the version's own THOUGHT says the MERGE claim was unsupported and this diff deleted the assert that would have red under it; only the THOUGHT records the refutation, so the node's state and its thought disagree.
4. experiment:a00-2efa683b ships an internally contradicted item table -- .agi/nodes/experiment/a00-2efa683b-cd698b.md:8 -- The table row for item 4 says 'CONFIRMED | second copy deleted: the header no longer enumerates rows', and the appended PARENT REVIEW in the same file says 'Item 4 is NOT fixed and the node misdescribes it'; a reader who takes the table as state gets the wrong answer.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_boxkit_templates.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_boxkit_templates.py · .agi/nodes/experiment/a00-19870cd0-134fe5.md · .agi/nodes/experiment/a00-2efa683b-cd698b.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 1247ad570 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.634 -- closes mur-director-engine-36 DH.615-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-box-memory-guard-piec-a00-0899a246 tip d0c4c43ca (branch de-base-634; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 2. Corrected node's own opening still says all four items closed (contradicts its corrected tally)
2. 3. Body section 2 still names direction 2's token the checkout root and pastes the withdrawn probe C
3. 4. Universal negative 'no state of the merge flips anything the suite asserts' is false
4. ONE-SOURCE, NEW: test:1036 hand-copies the literal '/.sanctuary/' that the same file already hard-codes in _leaks at test:151, while the new comment at test:1029-1030 claims 'KIT_TOKEN is drawn from the kit rule's OTHER tokens (home, /.sanctuary/)'. It is a second copy, not a draw: if the guard root changes at :151 the candidate silently diverges and the row keeps passing on a token the rule no longer denies -- the same copy-vs-rule defect the round exists to remove, reintroduced in the fix.
5. NODE-vs-BYTES, MISSED: .agi/nodes/experiment/a00-2efa683b-cd698b.md:31 (item 3 row) claims 'the comment names the mutation precisely instead of "RED if merged"', but the comment DH.615 rewrote at test:1034-1035 still ends with the literal sentence 'RED if merged: adding the kit's roots to anonymize.box_tokens makes `scan` name a class here (probe C, DH.591)'. The row the round says it corrected still asserts a fix the bytes do not carry.
6. STALE POINTER, MISSED: a00-2efa683b-cd698b.md:122 still ends 'RESIDUE: item 4 (test:4 inventory) open, see the note above' although DH.615 closed item 4 (a00-77817316:47-54, and `grep -n "10b\|SUB-ROWS"` on the d0c4c43ca bytes returns nothing, rc=1). The node this round edited still points a reader at an open residue that is closed.
7. (director measured at harvest: test_boxkit_templates.py + smoke = 269 passed, 6 skipped at d0c4c43ca; re-run at your tip and paste) UNVERIFIED: I did not run the suite at d0c4c43ca (the file does not exist at worktree HEAD d64923cd8, deleted after this range), so '269 passed, 6 skipped' (a00-77817316:77-79) and the parent's '197-test -k subset passes' (:119) remain claims, not evidence. Probe I WOULD run: cd <checkout of d0c4c43ca> && env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_boxkit_templates.py -q -k both_directions -p no:cacheprovider. Static substitute I did run: `grep -c '^def test'` is 32 at both 1247ad570 and d0c4c43ca, so the diff dropped and added no test; row 14b writes nothing, reads only repo templates and the fake_box/anonymize fixtures, and introduces no tmux/systemd/crontab/process call -- no real-resource touch found in the diff.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_boxkit_templates.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_boxkit_templates.py · .agi/nodes/experiment/a00-19870cd0-134fe5.md · .agi/nodes/experiment/a00-2efa683b-cd698b.md · .agi/nodes/experiment/a00-77817316-57d27a.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over d0c4c43ca · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## OPEN at the 2026-09-28 merge-up (director-engine; belam [decision] 00:0xZ: in-progress included)
STATUS    IN PROGRESS, not landed: DH.653 QUEUED (not yet dispatched); round work so far on loop branch season2/loops/hypothesis-box-memory-guard-piec-a00-fee425e8 tip 6702b6ee6.
ROUNDS    this post's rounds on this node: DH.591 DH.615 DH.634 DH.653; the open round's bytes live on its loop branch, never on the post branch, until its mur clears.


## CORRECTIVE DH.653 -- closes mur-director-engine-39 DH.634-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-box-memory-guard-piec-a00-fee425e8 tip 6702b6ee6 (branch de-base-653; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1 -- the red-first rewritten by this round and elevated into a node as the 'TRUE SCOPE' that refutes the old universal negative names a mutation that cannot fire (adding the kit's LEAK_ROOTS to anonymize.box_tokens)
2. 3 -- a pasted grep result is summarised as 'all four hits labelled' when one cited line is not; a00-2efa683b:30 still presents probe C as this round's run-and-pasted mutation
3. 6 -- (note) module-level next() candidate selection crashes with a bare StopIteration instead of refusing by name; named twice by kid and parent, unfixed
4. CONFIG-MAX / mechanism, and the strongest thing in the diff: the new 'ONE SOURCE' is a hardcoded path literal duplicating a committed config cell. .agi/config.json:247 carries paths.<town>.boxkit.guard_dir = '{repo_parent}/.sanctuary/guard', and the same test file asserts at test:529-534 that the guard dir IS that cell and derives GUARD_SRC from it. test:153 re-types '/.sanctuary/' instead of drawing it, so nothing ties the two: if the cell moves, the kit denylist keeps denying a path the kit never uses and row 4 (test:263-266) silently stops protecting the real guard dir, with no red anywhere. The drift the round claims to have closed re-enters through its own fix, and the round's central conjunct (a00-3d4e7707-9962d4.md:143, 'the literal /.sanctuary/ is now unique to test:153') is exactly the claim that misses this.
5. Item 4's closure rests on a grep that cannot see the surviving inventory. a00-2efa683b-cd698b.md:131 and a00-3d4e7707-9962d4.md:77 assert 'the header names the RULE (a row is named only by the comment above its own test, no list of row names exists -- test:4-7)', proven only by `grep -n '10b\|SUB-ROWS'` returning rc=1. But the same file enumerates rows 1-10 at test:10-50 and other rows refer to them by name: test:45 'row 10 compares them', :51/:55/:973 'row 4', :657 'Row 10', :717 'row 11g', :896 'row 12', :954 'row 13'. A second copy of row names exists 4 lines below the rule that says none exists, and it is still incomplete (11, 12, 13, 13b, 14b are referenced but not listed) -- the same stale-inventory class DH.591 raised, closed by a grep too narrow to see it.
6. Blast-radius escalation the round missed on its own declared residue: test:1048's next() runs at import, so the StopIteration is a COLLECTION error for all 197 rows, not a row-level failure. a00-3d4e7707:134-138 scopes it as a shape change to row 14b only; the next round should be told it takes the whole file down.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_boxkit_templates.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_boxkit_templates.py · .agi/nodes/experiment/a00-19870cd0-134fe5.md · .agi/nodes/experiment/a00-2efa683b-cd698b.md · .agi/nodes/experiment/a00-3d4e7707-9962d4.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 6702b6ee6 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE EG.16 -- closes mur-eg-5 DH.653-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-box-memory-guard-piec-a00-ec6eb41c tip 7623d8adc (branch de-base-EG.16; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. Row 15's parse keys on the prose form 'row N' while rows are declared as '# N --' comments, so a new row added without a docstring entry stays green (test_boxkit_templates.py:1098)
2. 4. The one-source refactor narrowed the kit denylist: '/.sanctuary/' -> '.sanctuary/guard', so a /.sanctuary/<other> byte in a template is no longer a leak and no row covers the lost class (test_boxkit_templates.py:165)
3. 5. The header still says 'Rows 1-14' with entry 15 present, and row 15 cannot catch it (test_boxkit_templates.py:4)
4. 6. Ceiling breach (22 vs 15 node lines, +41 vs 40 test lines) with the 177-line new node excluded from the count the parent adjudicated (a00-3981a5ee-3dcaba.md:1)
5. 8. a00-3d4e7707 keeps verdict=proved though its own review records a refutation of its one conjunct, now repaired by this diff (a00-3d4e7707-9962d4.md:5)
6. a00-2efa683b:31 — the table cell that IS item 4 still carries the exact claim this round declared false: 'the header names the RULE (a row is named only by the comment above its own test; no list of row names exists)'. The correction was applied to the RESIDUE paragraph at :128 (edited in this diff) and NOT to the cell that makes the claim, so the same node asserts both 'that is FALSE of the same file' and the false claim itself. Row 15 cannot catch it: its parse reads only extensions/agi/tests/test_boxkit_templates.py, never a node. This is the residue of item 5 in the one place item 5 was about.
7. a00-3d4e7707:88-95 — the DH.653 re-grep block is APPENDED beneath the DH.634 block rather than replacing it (the kid says so at a00-3981a5ee, 'Budget and honesty': 'I appended rather than deleted'), so the node now stands with the refuted sentence 'All four hits are now labelled withdrawals or the parent's own review line' immediately above its own refutation 'hit 30 was NOT a withdrawal'. Deliberate and declared, but it leaves an unretracted false claim in the bytes of a node that carries verdict: proved — the same shape as the miss above, and a candidate for a demotion the next round should make in one edit.
8. a00-2efa683b was repaired by hand after a write.py range replace wrote a duplicated table row and dropped row 2 (declared in a00-3981a5ee, 'Budget and honesty'), and the whole byte set was landed by 7623d8adc, whose own message is 'land DH.653's logged node edits left uncommitted in the parent worktree'. A hand write to graph nodes is the class goal:g4.18's `write_guard.py check` exists to witness, and the loop landed the bytes after the fact. UNVERIFIED whether write_guard would have flagged it — I did not run it; the probe I WOULD run is `python3 extensions/agi/bin/write_guard.py check` against the pre-merge parent, expecting the a00-2efa683b window to be named.
9. No real-resource touch and no test-that-requires-a-defect was found: the diff's added lines read only Path(__file__), re, CELLS and R.expand/R.engine_checkout, and render.py contains zero occurrences of subprocess/systemctl/os.system/tmux (engine_checkout resolves the linked-worktree .git FILE, render.py:34-40). The suite is green as claimed: 198 passed, 6.18s, run as a single committed file from a read-only archive of 7623d8adc with `env -u TMUX -u TMUX_PANE`.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_boxkit_templates.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_boxkit_templates.py · .agi/nodes/experiment/a00-19870cd0-134fe5.md · .agi/nodes/experiment/a00-2efa683b-cd698b.md · .agi/nodes/experiment/a00-3981a5ee-3dcaba.md · .agi/nodes/experiment/a00-3d4e7707-9962d4.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 7623d8adc · <= 40 test lines net over 7623d8adc · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat 7623d8adc <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE EG.26 -- closes mur-eg-9 EG.16-k1 accept_with_residue (no verify)
BASE      CUT FROM season2/loops/hypothesis-box-memory-guard-piec-a00-41ee77ef tip 066ebff9e (branch de-base-EG.26; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. The header's row count is a second, unchecked copy — row 15 does not read it -- extensions/agi/tests/test_boxkit_templates.py:4 -- 'Rows 1-15' is matched by neither `[Rr]ow (\d+)` (test:1108) nor the new `^# (\d+)` parse, so adding row 16 plus its docstring entry leaves the file fully green with the header still saying 15 — verified by probe (199 passed). The round's own item 3 cell ('the header's own count is checkable by the same row') is false of the bytes. Latent today, not a live false green.
2. Demotion did not move the confidence cell -- .agi/nodes/experiment/a00-3d4e7707-9962d4.md:8 -- verdict:30 fell proved -> inconclusive_lean_proved:55 while confidence:8 stayed 0.9, so the node's two frontmatter numbers now disagree; the next reader (or the evidence gate) sees a high-confidence node whose only conjunct its own review refuted.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_boxkit_templates.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_boxkit_templates.py · .agi/nodes/experiment/a00-2efa683b-cd698b.md · .agi/nodes/experiment/a00-3d4e7707-9962d4.md · .agi/nodes/experiment/a00-c339cb91-8933d0.md · .agi/nodes/verdict/a00-17f4d750-05709f.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 066ebff9e · <= 40 test lines net over 066ebff9e · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat 066ebff9e <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective EG.26: mur-eg-9 EG.16-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
