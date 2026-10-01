---
id: hypothesis:g1-inbox-read-cursor-never-passes-an-unprinted-line
mint_id: 8ccafe9990e745deb66e60a9aa2e46a7
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: director-general-1
scaffold_hash: 3aa7c9323afc4e40
season: 2
testable_claim: A message appended to a post inbox after its last read is reported by the next send.py read; no path advances the read-up-to-here cursor past an unprinted line; the advancer of both 10-01 cases is named with file:line
title: "G1 comms red: the inbox read cursor never passes a line the reading call did not print -- name the advancer, then fix it"
town: core
---
# hypothesis:g1-inbox-read-cursor-never-passes-an-unprinted-line

## Measured
- 16:46Z 10-01 (DG5, SM verified): `.agi/sessions/inbox/director-general-5.md` -- SM's `[board]` 16:37Z is line 111, the `# read up to here` cursor is line 112 = EOF; `send.py read director-general-5` printed `empty`; DG5 saw the line only by reading the pair dm file. Same for SM's 15:43Z `[decision]`.
- 16:2xZ 10-01 (belam, independent): `inbox/director-general-3.md` cursor at line 954 sat PAST belam's 16:09:39Z `[red]` (the G8 order); DG3 never saw it; the owner caught it.
- 17:1xZ 10-01 (SM, measured; DG1 re-read the bytes): `inbox/director-general-5.md` cursor at line 120 sits past SM's 17:0xZ `[decision]` (C2 re-mur) at line 119; DG5's 17:05Z reply answers other items and never mentions it -- the second case on DG5's inbox in 30 min.
- 3 cases / 2 posts (DG5 twice): an action order can vanish silently -- a comms red (belam 17:0xZ), not a residue.
- The advancer is UNNAMED. Candidates to rule in or out by measurement: the first-turn inbox injection (rotate/brief runs `read`), a wake/nudge path (`send.py wake`, heal `_repair_stranded_wakes`), the v5 mail poll (engine-wrap types `send.py read $AGI_SEAT`), a compaction / resume re-running a read, a second session sharing the seat name.

## CLAIM
A message appended to a post's inbox after that post's last read is reported by the next `send.py read <post>`: no path advances the `# read up to here` cursor past a line that the reading call did not print. The advancer of both measured cases is named in this node, with the file:line.

## Dispatch line
config-max: none expected (no new cell unless the fix needs a tunable) / template-max: none expected (the director brief's interim "action orders need a one-line ack back" rule is retired by this round's landing, not before) / code: the cursor write in send.py's read path (and any other writer of the marker) -- the cursor moves only over lines the same call printed.

## FALSIFIERS
1. Append line L to a fixture inbox after a read; the next `read` does not print L -> the claim is false.
2. Any code path other than the printing read writes `# read up to here` (git grep the marker across extensions/agi/bin) and is not named here -> false.
3. Reproduce the measured shape (two readers / a wake between append and read) in a test: the cursor ends past an unprinted line -> false.

## TESTS
- A committed test in extensions/agi/tests/ (send neighbourhood: test_send.py and siblings) that drives append -> (the named advancer) -> read on a tmp comms root and asserts L is printed; red on today's trunk, green after.
- The send neighbourhood stays green.

## FILE SCOPE
extensions/agi/bin/send.py (+ the ONE other file that holds the advancer, once named) · extensions/agi/tests/test_send*.py · this node. Never a live inbox, never MAIN's comms.

## CEILING
1 pi parent · kids <= 2 · 10-12 production lines per conjunct · pi-free (0 USD) · measure with a two-operand numstat <cut>..<tip before the paste commit>.

## CORRECTIVE DH.DG1.01 -- closes mur-dg1 dg101-mailpoll / dg101-race / dg101-rotalert (demote, one defect read by 3 slices, verify CONFIRMED)
BASE      CUT FROM season2/loops/hypothesis-g1-inbox-read-cursor--a00-d311e8c8 tip d2420e17c (worktree .agi/worktrees/de-base-dg101-1). No merge. Never rebase.
1. send.py:5986-5988 -- the POSITIONAL `read <seat> --peek` honours peek_: it prints and does NOT write `# read up to here` (read(mark=not peek_)), and read_dms does not commit either; so rotation_alert's pre-flight (rotation_alert.py:1381/1405, argv `read <seat> --peek`) retires nothing and the marking read (:1437) prints the body. Settle with: git grep -n 'peek_' extensions/agi/bin/send.py (paste).
2. rotation_alert.py:1438 -- the `if not marked` guard is blind: the real CLI prints the truthy literal 'inbox for <seat>: empty' (send.py:5991), never ''. Test for THAT verdict (not for an empty string) and return False with the NOT-delivered line; the empty-case test must feed the real literal, not '' (test_rotation_alert.py:1905).
3. A CLI-SEAM test, RED on d2420e17c then GREEN: drive rotation_alert's _auto_post through a REAL send.py read (send.main / subprocess on a tmp comms root, one block appended, _run_send_read NOT stubbed) and assert the body is printed and the next read of the inbox is empty only AFTER the marking read. Also assert main(['read', seat, '--peek']) leaves the inbox bytes unchanged. Paste the red run and the green run.
4. send.py:5942 -- `read --dm` / `read --room` with --peek: refuse (parser error naming the `peek` verb) so the flag never promises what it does not do; one test.
5. test_send.py:8469 -- make the race test's retired-invariant assertion UNCONDITIONAL (assert the unprinted body is never in the retired set; drop the duplicate params 'read' vs 'partial').
6. send.py:8-33 Usage block -- one line for `read <me> --peek`.
Landing note (not for the kid): the LIVE crontab mail_poll line still lacks --peek until crons re-renders; the director names it in the merge-up.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
FILE SCOPE extensions/agi/bin/send.py · extensions/agi/hooks/rotation_alert.py · extensions/agi/tests/test_send.py · extensions/agi/tests/test_rotation_alert.py · this node's kid node. Never a live inbox, never MAIN's comms.
CEILING   HARD CAP: 1 parent, 0 kids · 24 production lines · 70 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit
DISPATCH  (run from .agi/worktrees/de-base-dg101-1 by whoever holds the key; orders file = this section: write.py <node> 'read body 30:43' > <file>): python3 extensions/agi/bin/dispatch.py . DG1.01 --target hypothesis:g1-inbox-read-cursor-never-passes-an-unprinted-line --level small --tier parent --role parent --ladder-tier 0 --harness pi-free --branch --detach --orders <file> --from director-general-1 --allow-stale-base "corrective cut from the loop tip d2420e17c, never merged"

## CORRECTIVE DH.DG1.03 -- closes mur-dg1-2 dg101-c1 (accept_with_residue) + belam's config-max decision (18:3xZ, via SM)
BASE      CUT FROM season2/loops/hypothesis-g1-inbox-read-cursor--a00-3eeb965e tip e052b1a1b (worktree .agi/worktrees/de-base-dg101-2). No merge. Never rebase.
1. CONFIG-MAX (belam, verbatim intent): mail_poll's FULL command (incl. --peek, the rotate.py migrate --receive half) moves into a `cmd:` cell on the mail_poll row of .agi/nodes/.geometry/crons.md (the node cron:crons; edit it ONLY through write.py, skill agi-node-write); crons.py:~946 renders FROM that cell through the existing _substitute (placeholders {root} {repo_root} {logs_dir} {box}); the f-string literal goes. A mail_poll row WITHOUT a cmd: cell renders exactly as today, so no other row shifts. Falsifiers (paste each output): (a) `python3 extensions/agi/bin/crons.py show` prints the mail_poll line WITH --peek, FROM the cell; (b) a test pins the rendered mail_poll line == the line the f-string rendered at e052b1a1b for the same root/repo_root/box (same bytes), and a row without cmd: still renders it; (c) the live crontab picks it up after ONE crons.py apply -- DO NOT run apply (the director/grid_sync does); state the command only.
2. test_send.py:~8468-8480 -- the race test's comment claims an UNCONDITIONAL invariant while the loop still opens with if body in retired. The `if` is the right invariant (a body AHEAD of the cursor is read by the NEXT call and owes nothing to this one) -- keep it, make the comment TRUE, and kill the vacuous pass: assert "one" and "two" (both present at the scan) ARE in `retired` and in `shown`, so the loop cannot pass with nothing behind the marker.
3. test_send.py:8443 -- RESTORE the `partial` param: it is NOT a duplicate of `read` (the nested read's blocks are printed but never recorded in `shown` -- the case the first-round demote was about). Re-run it green.
Not corrective (director): the node's red/green paste + verdict (director prose commit on the final tip); the re-typed empty literal in rotation_alert (_empty_verdict) is demoted -- the hook must not import send.py's CLI module; the alias/PROJECT_ROOT claims were refuted by the verify stage.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
FILE SCOPE extensions/agi/bin/crons.py · .agi/nodes/.geometry/crons.md (via write.py) · extensions/agi/tests/test_send.py · the crons test file that already covers the mail_poll render (git grep -l mail_poll extensions/agi/tests) · this node's kid node. Never a live crontab, never crons.py apply.
CEILING   HARD CAP: 1 parent, 0 kids · 20 production lines · 60 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit
DISPATCH  (from .agi/worktrees/de-base-dg101-2 by whoever holds the key; orders = this section, 'read body 45:57' to a file -- check the range first): python3 extensions/agi/bin/dispatch.py . DG1.03 --target hypothesis:g1-inbox-read-cursor-never-passes-an-unprinted-line --level small --tier parent --role parent --ladder-tier 0 --harness pi-free --branch --detach --orders <file> --from director-general-1 --allow-stale-base "corrective cut from the loop tip e052b1a1b, never merged"

## CORRECTIVE DH.DG1.04 -- closes mur-dg1-4 dg101-c2 (accept_with_residue)
BASE      CUT FROM de-land-dg101-3 tip 284cb32d5 (worktree .agi/worktrees/de-base-dg101-3). No merge. Never rebase.
1. test_crons.py (near :1749) -- PIN THE LIVE CELL: one test that loads the REAL cron:crons node of the checkout (crons.load_crons_node on this worktree's .agi) and asserts the mail_poll cmd cell exists and contains `read --box-local --peek`, and that the line render_managed_lines renders from it contains --peek too (stub resolve_branch as the existing tests do). Red when --peek is removed from the cell: paste the red run (edit a COPY of the node in tmp_path, never the live one) and the green run.
2. test_send.py ~8443-8450 + ~8474 -- ONLY the comment: the `partial` case is the pre-existing d2420e17c shape restored verbatim (the nested read prints through the REAL printer, so its blocks are deliberately not in `shown`; the outer seam still sees the measured read); say that in one comment line, and say in one line why 'three' is checked conditionally (a body AHEAD of the cursor is read by the next call). No logic change.
Demoted by the director, not corrective: the crons.md THOUGHT/body staleness (verify REFUTED: doc lag that predates the range).
SAFETY    NEVER run find or grep -r outside your own worktree; never walk .agi/worktrees or /mnt/agi-ram; `git grep -- <paths>` only. Commit every edit on the branch BEFORE you report (cli.py done), and check `git status -s` after.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
FILE SCOPE extensions/agi/tests/test_crons.py · extensions/agi/tests/test_send.py (comments only) · this node's kid node. Never a live crontab, never crons.py apply, never edit the live crons.md.
CEILING   HARD CAP: 1 parent, 0 kids · 0 production lines · 35 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit
DISPATCH  (from .agi/worktrees/de-base-dg101-3 by whoever holds the key; orders = this section, write.py <node> 'read body 57:67' to a file): python3 extensions/agi/bin/dispatch.py . DG1.04 --target hypothesis:g1-inbox-read-cursor-never-passes-an-unprinted-line --level small --tier parent --role parent --ladder-tier 0 --harness pi-free --branch --detach --orders <file> --from director-general-1 --allow-stale-base "corrective cut from the landed tip 284cb32d5, never merged"

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.DG1.04: mur-dg1-4 dg101-c2: pin the live mail_poll cell in test_crons (red/green); partial-case + three-conditional explained in comments; crons.md staleness refuted by verify
<!-- THOUGHT:END -->
