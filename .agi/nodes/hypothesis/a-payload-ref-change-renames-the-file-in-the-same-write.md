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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.579: mur-director-engine-26 DH.497-k1 + DH.497-k2 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
