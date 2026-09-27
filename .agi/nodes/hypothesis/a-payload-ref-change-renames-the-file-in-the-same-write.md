---
id: hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write
mint_id: 0b764207c4494a45a5d167b539c75524
type: hypothesis
parents:
  - goal:g4.18.1.4
next_edges: []
confidence: 0.8
edited_by: director-engine
scaffold_hash: 8b25e9228029f4e9
season: 2
tags:
  - engine
  - write
  - node_writer
  - g4.18.1
testable_claim: "(1) a same-directory payload_ref change renames the file and the row in one write, mint_id unchanged (2) a cross-directory or cross-location change is refused unless explicitly confirmed (3) the row always resolves to an existing file and an existing destination is never overwritten (assigned: director-engine)"
title: "a payload_ref change renames the file in the same write; a directory move needs an explicit confirm (goal:g4.18.1.4; assigned: director-engine)"
town: core
---
# hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write

## Measured
- A build node names its file by `payload_ref` + `location` (a base NAME, locations.payload_base, locations.py:445). A write that sets `location` in the same edit wins over disk (write.py ~2218-2221), but NOTHING moves the file: `grep -nE 'git mv|shutil.move|rename\('` over write.py + node_writer.py = 0 hits (`os.replace` only for atomic temp writes, node_writer.py:1127, :1203). So `set payload_ref=<new>` rewrites the row and leaves the file at the old name: the row dangles until a hand `git mv`.

## CLAIM
(1) a node write that changes `payload_ref` to a new NAME in the same directory renames the file and updates the row in ONE write (mint_id unchanged, the grid history of the node continuous) (2) a change that moves the file to another DIRECTORY or another `location` is REFUSED, naming both paths, unless the write carries an explicit confirm (one named flag/verb arg); with it, the move happens (3) after any such write the row resolves to an existing file, the old path no longer exists, and an existing file at the destination is refused (never overwritten).

## Dispatch line
config-max: none (bases are already config names). template-max: none. code: the rename path in the writer, because no mover exists.

## FALSIFIERS
- a same-dir rename on a temp build node leaves the old file or a dangling row, or changes mint_id.
- a cross-directory change without the confirm moves any byte.
- a rename onto an existing file overwrites it.

## TESTS
extensions/agi/tests/test_payload_rename.py (new; temp graph under tmp_path only). Neighbourhood: test_write*.py test_node_writer*.py test_links*.py. Every pytest under `timeout 600`, --basetemp under /tmp.

## FILE SCOPE
extensions/agi/bin/node_writer.py (a mover beside replace_payload) · extensions/agi/bin/write.py (ONLY the update path that calls it, ~2215-2250 -- never main()/create/answers: goal:g4.18.1.1 is under review there) · extensions/agi/tests/test_payload_rename.py.

## CEILING
1-2 kids · <= 45 production lines · pi-free tier-0 · 0 USD. No test spawns pytest; kids never launch real claude.

## CORRECTIVE DH.579 -- closes mur-director-engine-26 DH.497-k1 demote + DH.497-k2 demote
BASE      CUT FROM season2/loops/hypothesis-a-payload-ref-change--a00-263a936b tip 4190de691 (branch de-base-579; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. Consent gate bypassed when the old payload file is absent (node_writer.py:565)
2. 2. Unguarded move after the row write (write.py:2271)
3. 5. Uncovered row-only repoints (write.py:2252)
4. MISSED[1] -- CONTRADICTORY SIBLING VERDICTS, and the tree carries the demoted bytes. Commit 4190de69 adds BOTH experiment nodes under one hypothesis: a00-a022ddab-5727e8.md `verdict: proved` AND a00-6cb920d2-f30271.md `verdict: inconclusive_lean_disproved:60`, whose probes P5 records conjunct 2 BROKEN and whose body carries 'PARENT REVIEW (a00-263a936b, DH.497): verdict DEMOTED proved -> inconclusive_lean_disproved:60'. The code in this branch is the SECOND (demoted) version -- plan_move at node_writer.py:549-574, which is the bytes that broke the gate. So the merge lands (a) code the graph has already demoted and (b) a node still asserting `verdict: proved` for a claim its own sibling measures as broken. A merge-pass should reconcile the sibling verdicts onto the claim before this branch lands, not carry both.
5. MISSED[2] -- the dry-run preview does NOT simulate the new refusal, so preview and land now disagree. main() returns on `--dry-run` at write.py:3358 (`return _preview_dry_run_gate(root, edit, args)`) and only calls submit() at write.py:3386, so the consent refusal raised at write.py:2261-2267 is never reached in a dry run: `set payload_ref sub/moved.py` (no --confirm-move) previews clean and exits 0, then the real write raises EditError. The house pattern is the opposite and is stated in the file itself -- `sub` is resolved for the preview at write.py:3187-3191, `replace` at write.py:3300, and create's schema gate is run PRE-dry-run on purpose (comment at write.py:3107-3113: 'a dry run simulates the mint, so it refuses what the real mint would refuse'). UNVERIFIED by execution (no committed test); the probe I WOULD run: `write.py build:<tmp-node> 'set payload_ref sub/moved.py' --dry-run` and compare its exit code and text with the same command without --dry-run.
6. MISSED[3] -- the node's own residue ledger mis-describes two of the three paths it names, so the next kid's fix will be aimed at the wrong lines. a00-a022ddab-5727e8.md Caveats: '`set payload_ref` is not the only way a row's path can change: `sub`/`body_patch`/`unset` reach `set_fm` too ... the mover is not wrong there, but it was not separately tested.' `sub` DOES route into set_fm (write.py:2418, called at write.py:2073) and IS therefore covered by the mover and the gate; `body_patch` never reaches set_fm at all (it writes edit.sub_body / body_patch_diff, write.py:2136-2143). Only `unset payload_ref` is genuinely uncovered (verb_unset write.py:288-293 vs the set_fm-only test at write.py:2254).
7. MISSED[4] -- an undeclared `location` NAME escapes as a traceback, not a refusal. plan_move resolves the NEW location through the shared resolver (node_writer.py:564 `_loc.resolve_payload_path(Path(root), new_ref, new_location)`), and locations.payload_base raises `KeyError` for an unknown name (locations.py:487-490, 'An unknown name is an error, never a fallback'). submit catches only `node_writer.MoveRefused` (write.py:2266) and main catches only `(EditError, FileNotFoundError)` (write.py:3390), so `set location vendor` in a project whose config.json declares no `vendor` tracebacks where the same write used to land a row. UNVERIFIED by execution; the probe I WOULD run: `write.py build:<node> 'set location vendor'` on a temp graph whose config.json has no `locations.vendor`, and assert exit 2 + an `ERR:` line rather than a traceback.
8. 1. Absent source short-circuits the cross-directory/cross-location consent gate — node_writer.py:565
9. 2. A committed test asserts the negation of conjunct 3 — test_payload_rename.py:150
10. 3. Claim narrowed in prose only — hypothesis node:17
11. 4. The P5 fix has no machine-tracked next step — hypothesis node:7
12. 6. Parent experiment unretracted — a00-a022ddab-5727e8.md:40
13. 7. Comment contradicts the mechanism — write.py:159
14. 8. Untested set-payload_ref + patch interaction — write.py:2169
15. link_ref / payload_ref resolution order is INVERTED between the two readers, and the mover makes it a broken link on the DEFAULT shape of a minted build node. create --payload records link_ref and never payload_ref (write.py:2950). The mover sources its old ref from write.py:2783 (`fm.get("payload_ref") or fm.get(links.LINK_FIELD)` — payload_ref FIRST), while links.py:126-142 resolves `link_ref` FIRST and falls back to payload_ref second. So `write.py build:x "set payload_ref lib/new.py"` on a --payload-minted node moves the file link_ref named and leaves link_ref dangling at the old path — the exact field `links.py links` reads, whose broken count must be 0 per CLAUDE.md's command table and per goal:g4.18.1.4.md:40. No committed test covers it: the fixture node at test_payload_rename.py:44-47 carries payload_ref only, never link_ref, so all 8 green tests sit in the one shape where the inversion cannot show. The probe I WOULD run (not run): a tmp_path graph with a node frontmattered `link_ref: lib/mod.py` only, submit `set payload_ref lib/new.py`, then assert links.links reports 0 broken — it will report 1.
16. template_max breach, unreported by the first reviewer. The new consent flag has no template line and no rendered source of truth. skills/agi-node-write/SKILL.md:12 declares `python3 extensions/agi/bin/write.py -h` the source of truth for the verb grammar, and write.py:2992 records that a `write-verbs` fact machine-reads that epilog for the grammar (hypothesis:write-py-help-epilog-lists-verb-grammar). The epilog is built from VERB_EXAMPLES (write.py:602-620, `"set": "set key value"` at :603) and VERBS/ARITY (:555-576) — none of which the diff touched, and none of which mention `--confirm-move` (grep over the file hits only :160, :274, :277-279, :2265). The single cell that does spell the flag, write.py:160, spells it as a suffix (defect 7). So the flag that admits a cross-tree byte move is undiscoverable from the declared source of truth and misdescribed in the one place it is written down.
17. The `set location` + payload-verb path was never analysed, and it composes with the new mover into a third case. write.py:2236-2237 rebinds `location` AFTER the patch bytes are read at :2177-2186, so `set location vendor && patch -` computes the new bytes from the OLD base and then writes them into the NEW base at :2283. The rebind is pre-existing (unchanged context in the diff hunk) so it is not this round's defect, but after this diff it also MOVES the file across, so a confirmed cross-location move + patch in one submit has three interacting paths and no probe among P1-P7.
18. The suite is UNVERIFIED by me, not green: 4190de691 is on season2/loops/hypothesis-a-payload-ref-change--a00-263a936b and is NOT an ancestor of this worktree's HEAD (55e6b1adc), and extensions/agi/tests/test_payload_rename.py does not exist at HEAD. The kid's '8 passed' and the parent's '146 + 81 passed neighbourhood' are claims I could not reproduce here. What I would run, on a read-only checkout of 4190de6: env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_payload_rename.py -q -p no:cacheprovider, plus test_write.py and test_write_guard.py for the neighbourhood.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_payload_rename.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/node_writer.py · extensions/agi/bin/write.py · extensions/agi/tests/test_payload_rename.py · .agi/nodes/experiment/a00-6cb920d2-f30271.md · .agi/nodes/experiment/a00-a022ddab-5727e8.md (write.py) · the kid's own node
CEILING   HARD CAP: 2 kids (k1 = the code items, k2 = the node-text items) · <= 15 production lines net over 4190de691 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.603 -- closes mur-director-engine-31 DH.579-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-a-payload-ref-change--a00-174d4044 tip 1876dfc83 (branch de-base-603; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. A second repoint of a link_ref row leaves link_ref dangling (write.py:2292)
2. 4. `set payload_ref` + a `payload` verb in one write loses the caller's bytes (write.py:2332)
3. 5. The narrowed conjunct 3 never reached testable_claim (hypothesis node:17)
4. 7. Stale line citations in the hypothesis prose (test_payload_rename.py:140 is :159; write.py:2950 is :3019)
5. 9. The epilog --confirm-move line has no committed test (write.py:3096)
6. Dry-run/land parity is fixed for the MOVE gate but not for the outside-repo gate the same diff touched: links.outside_repo_path has exactly ONE call site in write.py (write.py:2119, inside submit()), and main's dry-run branch returns at write.py:3436 via _preview_dry_run_gate without ever calling submit. So `write.py <node> set location <outside-base> --dry-run` prints a preview and exits 0 while the same command without --dry-run exits 2 with 'resolves outside the repo tree' (the land half is committed at test_write.py:2203-2206). The diff even adds the KeyError->EditError catch to that very gate (write.py:2121-2125) and still does not simulate it, while the new test's own name states the invariant: 'the dry run preview refuses what the land refuses' (test_payload_rename.py:251). PROBE I WOULD RUN (NOT run): write.main(['doc:n','set location scratch','--dry-run','--root',graph]) vs the same call without --dry-run on a tmp_path graph, asserting equal rc. Statically confirmed from the single call site plus the return at :3436.
7. The rollback restores the ref but not the `location` the same write may have set: the rebinding at write.py:2263-2264 lands in set_fm and is persisted by update_node at write.py:2306, while the rollback at write.py:2319-2322 restores only payload_ref/link_ref to _old_ref. So `set location <base>` + `set payload_ref --confirm-move ...` whose move raises OSError leaves the row with the NEW location and the OLD ref -- which then resolves through the new base and names nothing: precisely the dangling row the rollback was written to prevent. PROBE I WOULD RUN (NOT run): monkeypatch node_writer.move_payload to raise OSError on a two-base fixture, submit both sets, assert locations.resolve_payload_path(root, row_ref, row_location).is_file().
8. Checked and REFUTED on my own reading, recorded so a later reader does not re-open it: the plan_move reorder does NOT newly over-refuse. The tip order is src==dest -> None; cross-dir and not confirm -> raise; not src.is_file() -> None; dest.exists() -> raise (node_writer.py in 1876dfc83), so an absent source still returns nothing-to-move BEFORE the destination-exists check even with --confirm-move. The only intended behaviour change is the P5 consent fix, which is pinned at test_payload_rename.py:208-222.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_payload_rename.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/node_writer.py · extensions/agi/bin/write.py · extensions/agi/tests/test_payload_rename.py · .agi/nodes/experiment/a00-3d52306e-031125.md · .agi/nodes/experiment/a00-a022ddab-5727e8.md · .agi/nodes/experiment/a00-cee48ba1-ad56c2.md · .agi/nodes/hypothesis/a-payload-ref-change-renames-the-file-in-the-same-write.md (write.py) · the kid's own node
CEILING   HARD CAP: 2 kids (k1 = the write.py data-loss paths + tests, k2 = node text + testable_claim) · <= 15 production lines net over 1876dfc83 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.619 -- closes mur-director-engine-35 DH.603-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-a-payload-ref-change--a00-241566a5 tip 1d01c0b5b (branch de-base-619; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. P-A half-fix: effective-pair re-aim guarded on _plan.src (write.py:2365)
2. The test for that fix cannot fail for it (test_payload_rename.py:287)
3. link_ref clobbered on every repoint (write.py:2313)
4. Citation drift on the mirror line (hypothesis node cites write.py:2310-2311, bytes are :2312-2313)
5. Three MORE drifted citations in the sibling experiment's fix table, same class as defect 4 and not reported: a00-6761ec8a:81 cites `write.py:2311` for the mirror (actual :2312-2313) and `write.py:2864` for `_link_ref` (`def _link_ref` is at write.py:2860; :2864 is a docstring line); a00-6761ec8a:82 cites `write.py:2325` + `2363` for the effective pair (actual: `_after` assigned at :2323-2324, guard and aim at :2365-2366). The round's own citation discipline is its deliverable (a00-06ed089b:81, 'Every line the node cites is the line that holds'), so these belong in the findings row with defect 4.
6. The chain never names the WORSE consequence of the widened mirror: at write.py:2316-2320 `plan_move` is then handed `_old_ref`, which for a link-only row is the `link <ref>` target (write.py:2892 falls back to `link_ref`), so a `set payload_ref X` on such a row RENAMES the file the node's body link named, not merely overwriting the field. The read-ORDER falsifier (hypothesis:39) describes the field disagreement and stops there; the file move is unreported and untested.
7. The frontmatter `testable_claim` (hypothesis:17) was deliberately moved into the field by this round — the claim a reader meets FIRST — and it still contains NO conjunct for the payload verb in the same write, which is the round's own top OPEN residual (hypothesis:40). A reader who reads only the field cannot see that the title's second half ('renames the file in the same write') is PARTIALLY closed; the kid fixed the field-vs-test drift and left the field-vs-residual drift in place.
8. Unread-reader check, reported clean rather than as a defect: no test in the diff touches a real tmux pane, systemd unit, crontab or process — `_cli` (test_payload_rename.py:322-332) drops TMUX/TMUX_PANE from the child env and execs only `write.py` against a graph under `tmp_path`, with `--root` given explicitly; every other case is a `tmp_path` fixture. No node file is deleted or demoted in the diff (numstat shows 0 deletions under `.agi/nodes`). The round did not loosen the gate it passes through: the outside-ref gate got STRICTER and its new test asserts rc 2 on BOTH the preview and the land (test_payload_rename.py:345).
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_payload_rename.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/write.py · extensions/agi/tests/test_payload_rename.py · .agi/nodes/experiment/a00-06ed089b-7c4e55.md · .agi/nodes/experiment/a00-6761ec8a-99af24.md · .agi/nodes/hypothesis/a-payload-ref-change-renames-the-file-in-the-same-write.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 1d01c0b5b · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.643 -- closes mur-director-engine-38 DH.619-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-a-payload-ref-change--a00-280a80d2 tip aee3afa2c (branch de-base-643; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 3. `unset payload_ref` never reaches the mover (write.py:2300 keys on set_fm; verb_unset writes unset_fm at write.py:288-293)
2. 4. the two readers of payload_ref/link_ref still disagree on order (write.py:2904 vs links.py:124-141)
3. 5. conjunct 3's 'never overwritten' is absolute in the claim, narrower in the bytes (node_writer.py:571)
4. M1 - the round's NEW test pins a silent overwrite that escapes the mover's documented guarantee: with the source absent, plan_move returns at node_writer.py:571-572 and never reaches the dest-exists refusal at :573-575 (docstring 'An existing destination is NEVER overwritten, confirmed or not', :592-594); the widened re-aim (write.py:2377) then lets replace_payload write over that existing file, asserted as intended at test_payload_rename.py:307-312. The node names only the BOTH-absent case; the dest-exists-absent-source case is unnamed, and the node's fix-table bullet still says the dest refusal is CLOSED in the PLAN. Claim-narrowing or a one-line refusal is owed before any later round treats conjunct 3 as absolute.
5. M2 - rollback asymmetry the round did not address: write.py:2340-2362 rolls the ROW back (ref AND location) when move_payload raises OSError, but the new failure mode - row landed at :2335, replace_payload raises FileNotFoundError at :2383 - has no rollback, and the new test asserts the dangling row as the EXPECTED outcome (test_payload_rename.py:325 `assert _row_ref(n2) == 'lib/renamed.py'` after the raise). The chain now holds two half-done-write shapes and rolls back only one. The node says 'the row already repointed' but never says the rollback idiom is not applied here.
6. M3 - an explicit `set payload_ref` on a BOTH-fields row still silently repoints the body link: the narrowed mirror at write.py:2317-2320 fires whenever the write names payload_ref and the row has any link_ref, writing set_fm['payload_ref'] over link_ref, so `link_ref: docs/notes.py` + `set payload_ref lib/renamed.py` destroys the body-link target. Identical hazard class to the P-B case the round fixed, one step away, and not named in the node (which presents the mirror narrowing as the end of that finding). Verified by reading the two lines plus the pre-fix evidence in the reverted-bytes run: base bytes turn `link_ref: docs/notes.py` into `link_ref: lib/mod.py` on a location-only write (that test failing is the round's proof P-B was real).
7. M4 - API contract, minor: submit() declares 'Everything that can refuse, refuses BEFORE anything is written' (write.py:2205-2208) and converts MoveRefused/KeyError to EditError (:2330-2333), yet the newly-tested shape escapes submit() as a raw FileNotFoundError AFTER the row was written (node_writer.py:643-646). The CLI is fine - main catches (EditError, FileNotFoundError) at write.py:3514 and returns rc 2 - but the new test now pins FileNotFoundError as the contract for an API caller that catches EditError only. Not new (pre-fix raised the same type), but newly blessed.
8. M5 - coverage note, minor: test_a_location_only_write_does_not_clobber_the_body_link (test_payload_rename.py:333-339) asserts only the row's fields; it never asserts where the bytes went, so it would pass if the location move copied instead of moved or left the original behind. Cheap to tighten, no defect asserted.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_payload_rename.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/node_writer.py · extensions/agi/bin/write.py · extensions/agi/tests/test_payload_rename.py · .agi/nodes/experiment/a00-0b87822c-8fcef5.md · .agi/nodes/experiment/a00-cee48ba1-ad56c2.md · .agi/nodes/hypothesis/a-payload-ref-change-renames-the-file-in-the-same-write.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over aee3afa2c · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.643: mur-director-engine-38 DH.619-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
