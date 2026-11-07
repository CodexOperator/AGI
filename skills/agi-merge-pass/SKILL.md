---
name: agi-merge-pass
description: >
  The Prime's merge routine: the 4-hourly CHECK, the notice, and a PASS that reviews every
  hypothesis/engine round landed on the town trunk since the last merge and merges it into
  season2/main — trunk sync, chunked pi reviews under the memory guard, verdicts, reds,
  residues, the verify-and-push close. Use when the CHECK cron fires, a PASS is due, or a
  post's merge-up has to be judged. Prime only (belam).
---

# agi-merge-pass — CHECK ▸ notice ▸ PASS

Procedure text: `.agi/sessions/prime-merge.crons.md` (box-local, untracked; section 1 = CHECK, section 2 = the
pending PASS). The crons are POINTER prompts — edit the section, never the cron. State:
`.agi/sessions/prime-merge.state.json` (last_merged_town_sha, notice_sent_at, run_at, pass_started_at).

## 1 · CHECK (cron "13 */4 * * *", re-armed at every wake)
> **TRAJECTORY FIRST (owner 07:5xZ 10-10, verbatim: "Yes always. Thats your main check every 4 hours is to see what’s stuck if anything and keep town on trajectory and moving toward season completion").** Every CHECK: (T1) each post's state -- idle/busy, unread box, stuck dialog, last box send; (T2) the season's active leaves (goal:g7.16.1.11.*): landed-but-still-active -> ask the master to close; unowned or idle -> ask the masters (SM engine / TM research) what is queued and to dispatch idle posts; (T3) a post silent > 12 h -> nudge via its master (belam mails masters only). Then (A)-(C) below.
```
(A) read: dm files *belam* + the inbox FILE (ts > belam.lastcheck) + one send.py read belam → answer only what needs the Prime
(B) N = rev-list BASE..TIP (TIP = $AGI_TRUNK); landed = experiment files changed
    a. N==0 or landed==0 → nothing      b. pending, no notice → ONE [owner] 5 h notice dm to thought-master + a one-shot
    c. notice pending, now < run_at → nothing      d. now ≥ run_at, never fired (pass_started_at null) → run the PASS now
(C) owner reply ≤ 5 lines; ONE line when nothing changed
```

## 2 · PASS (steps as numbered in section 2; goal:g7.16.1.10.7)
> **The Prime never runs a chunk review** (goal:g7.16.1.10). Steps 2, 3, 4 and 6 are RETIRED BY NAME below: the council reviews each round and writes `doc:council-report` (council_report.py, goal:g7.16.1.10.5); the mechanical REDs run in `reds.py` (goal:g7.16.1.10.3); the PASS reads ONE word.
```
0 stamp pass_started_at FIRST
1 fetch · origin/season2/main must be an ancestor of TIP, else sync it into the trunk (below) · PIN TIP as a sha
2 RETIRED (was: build rounds)                 -> the council's rounds, one report row each
3 RETIRED (was: launch chunks + Monitor)      -> the council reviews; the Prime launches nothing
4 THE WORD: python3 extensions/agi/bin/merge_gate.py check BASE TIP [--prime-count N]
  prints `merge` or `hold` FIRST, then one reason per line; rc 0 merge · 1 hold · 2 cannot answer (a missing cell or report: a hold, never a merge)
  hold over: a RED (secrets / a node deletion by mint_id / a broken link) · a BASE..TIP commit on a review path with no accepting report row ·
  a row whose verdict is not accept*; `unreviewed:budget` rows merge only with --prime-count = their count (the Prime's word naming it)
5 merge: prime-root: pull --ff-only · merge --no-ff TIP (merge-tree preview) · commands.py run verify · push season2/main ·
  ff local-maxxing/main to TIP · grid.py commit --all (background)
6 RETIRED (was: a Prime-minted PASS leaf)     -> residues are already routed by council_report.py to their owner post's residue leaf
7 state file (last_merged_town_sha = TIP …, pass fields → null) · ONE numbers-only note on the town:local-maxxing board · commit by path
8 ONLY NOW one [merge-up] report dm to thought-master      9 owner report ≤ 6 lines
```
A `hold` or rc 2 is ONE [red]/[hold] line to the owner naming the first reason; nothing is merged over it. Config cell `merge_gate.review_paths` (the paths a commit must be covered on) is the Prime's: absent = rc 2 naming it.
RED = what `reds.py` prints (counts and names, never a secret's bytes) · a protocol regression stays a judgment call -> no merge, one [red] dm. demote = node-text overclaim → merges as a residue.

## 3 · Tooling (/tmp/belam-passN/; everything but the trunk sync belongs to the RETIRED steps 2-4 and is kept only as the old route)
build.py (BASE hard-coded; TIP/OS/PER from env) · launch.sh (CAP from ./cap; holds on user@ headroom < 1500 MiB and on memory_alarm
WARN/ALARM in 15 min) · monitor.sh (exits, launcher death; kills a recursive grep/rg/find over .agi/ or the repo root at io60 ≥ 25 ONLY
when an ancestor's argv carries this pass's tag (`p10chunk`/`p10retry`) — other posts' processes are spared, logged to
spared.log; owner 2026-09-27 01:5xZ: fine-grained reach) · verdicts.py (newest run per round wins; unwraps an unstructured return leniently) ·
retry.sh. Trunk sync: /tmp/belam-trunk-sync/{sync.sh, resolve.py} — merge-tree preview, a posts.md-only conflict resolved as
trunk rows + the directors' model cells (pubkeys must agree), temp index + ff-only, never a conflicted MAIN. A reboot wipes /tmp: rebuild per card trap 26.

## 4 · Traps paid for
| trap | rule |
|---|---|
| PER × CAP ≤ 6 pi (user@1000 high 6628M) | CAP counts CHUNKS; never 6 over 5-round chunks |
| `pgrep -f 'workflow.py run'` matches seat wrappers; foreground sleep blocked | anchor patterns; wait with Monitor / run_in_background |
| verify `verdicts[]` rules on the FIRST reviewer's defects + `missed[]` | a residue table reads verify, never the review list alone |
| `grid.py commit --all` in prime-root can leave an evidence-gate demotion dirty | save the patch, restore the file, then merge |
| every push prints the remote's moved location | `git push … 2>&1 \| grep -v '^remote:'` |
| the trunk push is thought-master's alone (owner 09-25) | belam pushes only season2/main + local-maxxing/main |
| suite lock `.agi/sessions/<values.core.suite_lock.file>` | "free" = absent in MAIN and every post worktree (F7); no MAIN commit while it exists |
| MAIN is shared with thought-master | commit by exact path; never switch branches, never touch others' uncommitted edits |
| the :28 board job lands the Prime's town commits on posts/belam (belam trap 126, gen IV) | it raced SM's cuts 3x (L73, L75, L79): SM re-reads posts/belam at send (R1') and refuses :20-:29 (R2); the Prime's CAS refusal is the guard; R3 (a land-side re-merge of board-only newcomers) stays banked until one race with R1'+R2 in place |
| a commit on belam's ~/t MOVES the local posts/belam to its commit (since goal:g7.16.1.11.46.30 belam's turn end commits its card alone, every other ~/t path a [trunk-post] line) (belam trap 128, gen IV; a gate-only tip sat there unpushed and the next merge-up would have carried it ungated) | a tip for SM's gate: commit, `git update-ref refs/heads/tip/belam/<name> NEW`, then CAS posts/belam back (`update-ref posts/belam OLD NEW`); never push it; for a chain, set posts/belam to the tip only for the instant of each commit |
| my L127 [landed] quoted an rc read through a pipe (belam trap 129, gen V) | an rc is read BARE (`cmd >/dev/null; echo rc=$?`), never through a pipe or wrapper |
| agi-cred S1 passed a gate on a GREP of the scoped line; inherited env still reached the root read (belam trap 130, gen V; alive HOLD x2) | a "scoped / refused / cancels" claim gets a hostile-input lane (every inherited source at once) + one mutant per guard, never a grep |
| VL C1-C5 returned at GATE255: grid-writers pins every git call site (belam trap 131, gen V); again 10-26: the WRAP's commit-tree (C1) and a crons.md why_box naming refs/grid (C6, it RED the trunk, L149) | any tip that adds a git call OR a line naming refs/grid (a .geometry doc line counts) runs test_grid_writers on the live trunk + the edit BEFORE it is sent; a hand commit on a land.rules_paths path goes through SM's gate, never direct |
| L140 landed 8 min after SM's [STOP] sat in the box (belam trap 133, gen VI); two direct commits raced SM's next [merge-up] (trap 134) | `box read` IMMEDIATELY before every CAS and every direct commit, in the SAME command, and stop on any mail: land a waiting [merge-up] first |
| my card commit after SM cut L154 moved posts/belam past its CAS base: L154 needed a re-cut (belam trap 136, gen VII); the :28 board job did the same to L180-L185 at 21:28Z 10-26 (gen VIII) | no commit on posts/belam while a [merge-up] is pending; commit the card right AFTER a land; land outside :20-:30 (the board's :23 / :28 move the tip), and a cut that must wait for a clock time is re-cut after the last :28 before it |
| a land's 'GRID NOT LANDED' is soft, yet the 7th read of it found L364's [red] (belam gen XIV, 11-05) | read recompose's AHEAD/BEHIND paths at every land before calling it harmless |
| land.sh's mail guard stopped 3 of 5 land tries on council notes, ~4 min each (belam gen XIII), and it CONSUMES mail (gen XIV) | read mail.L<n> and re-run; send anything that closes a thread before the run; while a land runs read the sender's ref (`git log -1 --format=%B refs/box/<p>/belam`), never box read |
| a card commit 16 s after a land crossed SM's next cut (L349 on c26b08c137); I CAS'd it back unsaid and the seats traced the rewind from the reflog in two mails (belam gen XIII) | during a chain of lands commit NO card until the last one; if a rewind is needed, send the one-line cause BEFORE it |
| a tool result 'rejected' arrived after the command had run: I told the owner TM never ran, the sudo log said it did (belam gen XII, 07:33Z 11-05) | read the sudo log or the unit state before saying what did not happen; a 'no backup file' check proves nothing when the original never existed |
| 'it did not clear' and 'none stuck' told to the owner from what was unread: the gate had opened 12 min before the retry, aio and TM were unread (belam gen XIV, 11-05) | read it before saying it |
| a RULES land that changes a ~/bin piece reaches posts only at their next START (belam gen X); a new hook needs that start for its settings line too: DG2, DGo1, DRev, DSci1 started 06:06Z 11-04, before L354, so at 22:4xZ 11-06 they had no agi-pray piece and 0 settings hits (belam gen XV) | when the land line leaves it to me, re-extract ONLY the changed pieces (per-section diff of the piece files), as a consistent set (agi-wt + agi-in at L318), into the posts that carry the broken one, sha per post == trunk; a missing hook is read from the unit's start time against the land's before it is called a fault |
