---
id: hypothesis:trunk-tests-follow-the-owners-0927-ultracode-drop-and-facts-collapse
mint_id: 1ff23358041b4a3683337daee82903d9
type: hypothesis
parents:
  - goal:g7.33.19
next_edges: []
edited_by: director-engine
scaffold_hash: 2f794e43a47f9fcf
season: 2
testable_claim: "test_ladder_node roles-table and test_sensei_wake_audit whois-fact read the live truth (settings not ultracode; F3 points at skill agi-send, which carries the whois shape once) with their contracts kept; test-only (assigned: director-engine)"
title: Trunk tests follow the owner 09-27 ultracode drop and facts collapse
town: core
---
# hypothesis:trunk-tests-follow-the-owners-0927-ultracode-drop-and-facts-collapse

## Measured
TMM.298 (thought-master 13:31Z 09-27): two TRUNK reds that fail without the zero-USD fix too; reproduced on the post branch 32ff79e53 (2 failed in 0.14 s). Attributed by the director:
(1) test_ladder_node.py:70 `assert prime.get("settings") == "ultracode"` -- 20283d21b (belam-S2-L5-XI, owner 09-27: ultracode dropped from every row) set the tier-3 prime_director row's settings to "" (.agi/nodes/.geometry/ladder.md:37). The test pins a value the owner removed.
(2) test_sensei_wake_audit.py:832 `exactly one live fact must cite send.py whois <token>: []` -- cdcfe5c0b (belam-S2-L5-XIII) collapsed config:rotations facts to pointers; F3 now reads `F25+F3 -> skill agi-send (§1)` and the shape `send.py whois <session_name> --claim <post>` lives at skills/agi-send/SKILL.md:24. No live fact carries the shape any more.

## CLAIM
Both tests read the live truth again with their contract kept: (1) the tier-3 prime_director row still resolves harness/model/effort, and its settings is NOT "ultracode" (owner 09-27); (2) exactly ONE live fact points F3 at skill agi-send, and that skill file carries the `send.py whois <token>` shape exactly once in a command line -- the prose-shadow guard (a fact whose prose says whois never wins) is kept. No production line and no graph node changes.

## Dispatch line
config-max: none / template-max: none / code: none -- test-only (the graph is the source; the tests follow it).

## FALSIFIERS
- either test still fails on the post branch;
- a test is deleted, skipped or xfailed instead of retargeted;
- any file outside FILE SCOPE changes.

## TESTS
test_ladder_node.py test_sensei_wake_audit.py (whole files) + test_sensei.py test_bin_help_smoke.py once. timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE.

## FILE SCOPE
extensions/agi/tests/test_ladder_node.py · extensions/agi/tests/test_sensei_wake_audit.py · the kid's own node

## CEILING
HARD CAP: 1 kid · 0 production lines · <= 30 test lines net · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut

## CORRECTIVE DH.545 -- closes mur-director-engine-23 DH.538-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-trunk-tests-follow-th-a00-b83e7193 tip aa383f9f8 (branch de-base-545; the post-branch zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. ultracode guard is prime-row-only and negative-only (test_ladder_node.py:74)
2. 2. F3 pointer check is line-level, not clause-level; the label assert is self-derived (test_sensei_wake_audit.py:838/844/856/863)
3. 3. whois re-derive asserted on a hand-built facts list; no live end-to-end category-(a) pin remains
4. MISSED (test that requires a defect, demote-adjacent but out of scope here): the prose-shadow guard was INVERTED, not kept. The pre-image asserted `len(carriers) == 1` — exactly one live fact CITES the shape (123e0a487:832). The round replaced it with `assert carriers == []` (aa383f9f8:846, 'no live fact inlines a whois shape'). The hypothesis CLAIM and the experiment node's 'contract kept' table both say the guard was KEPT; it was flipped. Consequence: the state that would restore the end-to-end re-derive (defect 3) now makes this test FAIL — a successor who re-inlines `send.py whois <token>` in a live fact is punished for the right fix. The guard should have been kept as 'at most one / never shadows the pointer', not turned into a ban.
5. MISSED (minor, folds into defect 1): the relax also drops the settings SHAPE. `:74` is a not-equal on a possibly-absent key, so a row whose `settings` key is deleted, set to null, or set to a dict passes. The old `== 'ultracode'` at least forced the key to exist and be a string. A form such as `isinstance(prime.get('settings'), str) and prime['settings'] != 'ultracode'` keeps the removal contract without losing the key's presence.
6. UNVERIFIED (execution of the round's own files): this worktree's HEAD is 86ae807b0 and `git merge-base --is-ancestor aa383f9f8 HEAD` exits non-zero, so aa383f9f8's test bytes are not on disk here and I could not run the round's versions without editing the tree. I verified instead by replicating the exact expressions of aa383f9f8:838-863 against the live bytes in this worktree (which `git diff 123e0a487 HEAD` shows are byte-identical for ladder.md, rotations.md, skills/agi-send/SKILL.md and sensei.py): pointer count 1, carriers [], the skill shape present exactly once on a non-comment line, and the re-derive landing on ('a','F25'). All four conjuncts hold, so the round's tests do go green on live truth. The round's own counts (95 passed, then 184 passed/7 skipped) and its 6 negative probes remain UNCLAIMED by me; the probe I WOULD run, if the branch were checked out, is: restore 123e0a487's test files, apply only the round's diff, run `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_ladder_node.py extensions/agi/tests/test_sensei_wake_audit.py -q -p no:cacheprovider --basetemp=/tmp/rev538` and expect 0 failures — a read of committed files only, no rotate/heal/send/dispatch function is called.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_ladder_node.py test_sensei_wake_audit.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_ladder_node.py · extensions/agi/tests/test_sensei_wake_audit.py · .agi/nodes/experiment/a00-5f39d42c-1941d9.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over aa383f9f8 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.562 -- closes mur-director-engine-25 DH.545-k1 accept_with_residue (no verify)
BASE      CUT FROM season2/loops/hypothesis-trunk-tests-follow-th-a00-000b4375 tip e4f039c8d (branch de-base-562; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. the live end-to-end category-(a) re-derive is not pinned; the guard passes vacuously at (b, None) -- extensions/agi/tests/test_sensei_wake_audit.py:871 -- `assert cat != "a" or label not in pointer_labels` is satisfied by cat=="b", which is what the pointer era always yields (shapes are backtick-only, sensei.py:496-501); order item 3 asked for a live category-(a) pin and the comment at :836-840 claims it was 'measured live, below' without pasting the measurement — the engine fix is named OUTSIDE, which is honest, so this lands as residue for the Prime, not a fake test.
2. the label assert is still self-derived and cannot fail -- extensions/agi/tests/test_sensei_wake_audit.py:849 -- `assert "F3" in pointer_labels` is implied by the :844 predicate `re.search(r"\bF3\b", c)` on the same clause, so order item 2's second half (a non-self-derived label check) is satisfied only in wording; the real work is done by :871.
3. the new table-wide shape assert contradicts the ladder schema, which declares a missing settings field legal -- extensions/agi/tests/test_ladder_node.py:78 -- `.agi/context/schemas/[ladder].md:96` states `settings: ""` (or a missing field) emits nothing, but the new assert makes a key-less roles row RED — two sources disagree about the same rule, and a schema-legal ladder edit would fail trunk; one of the two must change (schema line, or restrict the shape assert to rows the schema requires).
4. the round's own demotion is recorded only in prose: frontmatter says `verdict: pending`, the THOUGHT says inconclusive_lean_proved:80 -- .agi/nodes/experiment/a00-6e9861c0-0d1a45.md:30 -- 7bcbb73a0 set `verdict: proved` / confidence 0.82 and e4f039c8d flipped both to `pending` / 0.5, while the THOUGHT (:93+) and the trailing Agent Notes say 'demoted ... to inconclusive_lean_proved:80' and 'ACCEPTED at lean_proved:80'; the machine field the evidence gate reads never carries the lean, and commit 7bcbb73a0's subject still reads verdict=proved. Not a gate violation (pending is non-decisive) but the demotion is invisible to every machine reader.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_ladder_node.py test_sensei_wake_audit.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_ladder_node.py · extensions/agi/tests/test_sensei_wake_audit.py · .agi/nodes/experiment/a00-5f39d42c-1941d9.md · .agi/nodes/experiment/a00-6e9861c0-0d1a45.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over e4f039c8d · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.582 -- closes mur-director-engine-28 DH.562-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-trunk-tests-follow-th-a00-688cfdb9 tip 08da15284 (branch de-base-582; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. residue 1 — a negative probe mutated the LIVE, out-of-scope skills/agi-send/SKILL.md:24,36 (F3 -> F9x) and the loop's own kid done-commit 2d03f3a0f committed it, so that commit is RED on its own bytes at test_sensei_wake_audit.py:859; 08da15284 restores the blob byte-exact, tip is clean
2. residue 2 — .agi/nodes/experiment/a00-ea11b587-6ad475.md:35-36 ('0 production lines / only test files and two node frontmatters changed') is measured over extensions/ only and so cannot see defect 1
3. MISSED-1 (the P3b half the first reviewer folded into its refuted item 3) — the widened shape guard re-admits a case neither the schema it cites nor any probe covers. test_ladder_node.py:82 is `if r.get("settings") is not None:`, so `settings: null` now passes; but the schema line the round itself cites sanctions only `settings: ""` OR a MISSING field (.agi/context/schemas/[ladder].md:96-97), and the round's probe ledger records only the key-DELETED case (a00-ea11b587-6ad475.md:15; PARENT PROBES :146 'P3 gate, the settings KEY deleted'). The pre-image deliberately refused exactly this value ('a bare not-equal passes vacuously on a deleted / null / dict value'). One RED case of the DH.545 contract was re-admitted with no recorded probe, and the live ladder cannot falsify it either: .agi/nodes/.geometry/ladder.md:37-40 shows all four roles carrying `settings: ""`, so no live row takes the new false branch.
4. MISSED-2 — item 2's headline mechanism is SKIPPED, not enforced, when its independent source is absent, and the node records that as a virtue. test_sensei_wake_audit.py:850-851 `if skill is None: pytest.skip("skills/agi-send/SKILL.md not resolvable from this test")` sits directly above the :859 assert whose entire claimed value is that it 'can disagree with the pointer clause, and so can fail'. a00-ea11b587-6ad475.md:18 logs 'NEG agi-send skill file removed -> test SKIPS (never a vacuous pass on a missing file)'. A skip is a non-failure: in any tree without skills/agi-send/, item 2 evaporates silently. That asymmetry is precisely the class of incident residue 1 is — a doc edit turned into a suite RED — while the neighbouring case (a rename) would have been a silent skip, which is worse and unprobed.
5. MISSED-3 — the round's 'independent source' is a third hand-maintained copy of the F3 label, and it priced that as a win. The F3 fact now lives in config:rotations (.agi/nodes/.geometry/rotations.md:13, '- F25+F3 -> skill agi-send (§1)'), is asserted as a literal at test_sensei_wake_audit.py:846 and again at :859, and is now ALSO required to appear in the hand-edited prose of skills/agi-send/SKILL.md:24,36. Before this round the test bound only to a command shape (:861-863); after it, renumbering F3 in a markdown doc — a documentation edit with no code change — reds the engine suite. The round's own P1 probe did exactly that and the loop harvested it as commit 2d03f3a0f (see verdict 1). A second source that is itself hand-edited prose converts a doc edit into a test failure with no owner-facing guard; that cost is not recorded anywhere in the node.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_ladder_node.py test_sensei_wake_audit.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_ladder_node.py · extensions/agi/tests/test_sensei_wake_audit.py · .agi/context/schemas/[ladder].md · .agi/nodes/experiment/a00-6e9861c0-0d1a45.md · .agi/nodes/experiment/a00-ea11b587-6ad475.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 08da15284 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.582: mur-director-engine-28 DH.562-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
