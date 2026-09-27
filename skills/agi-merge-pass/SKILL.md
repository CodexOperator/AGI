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
```
(A) read: dm files *belam* + the inbox FILE (ts > belam.lastcheck) + one send.py read belam → answer only what needs the Prime
(B) N = rev-list BASE..TIP (TIP = local-maxxing/season2/main); landed = experiment files changed
    a. N==0 or landed==0 → nothing      b. pending, no notice → ONE [owner] 5 h notice dm to thought-master + a one-shot
    c. notice pending, now < run_at → nothing      d. now ≥ run_at, never fired (pass_started_at null) → run the PASS now
(C) owner reply ≤ 5 lines; ONE line when nothing changed
```

## 2 · PASS (steps as numbered in section 2)
```
0 stamp pass_started_at FIRST
1 fetch · origin/season2/main must be an ancestor of TIP, else sync it into the trunk (below) · PIN TIP as a sha · credits (< 4 USD → engine-delta + 5 sampled rounds)
2 build rounds: one per hypothesis with ≥1 experiment changed in BASE...TIP (files ≤ 12) + engine-delta-N over unlisted
  extensions/ skills/ src/ .agi/config.json .agi/nodes/.geometry paths (≤ 12 each; rotate test files dropped)
3 launch chunks (≤ 2 rounds each) in the background, CAP chunks live; ONE Monitor (monitor.sh)
4 verdicts ONLY from runs/<key>/{review,verify}_<label>.json → RED | demote | accept(_with_residue)
5 clear → prime-root: pull --ff-only · merge --no-ff TIP (merge-tree preview) · commands.py run verify · push season2/main ·
  ff local-maxxing/main to TIP · grid.py commit --all (background)
6 residues → ONE batch hypothesis under goal:g1 + one hypothesis per real code defect (assigned: director-engine) → ONE [decision] dm to DE
7 state file (last_merged_town_sha = TIP …, pass fields → null) · ONE numbers-only note on the town:local-maxxing board · commit by path
8 ONLY NOW one [merge-up] report dm to thought-master      9 owner report ≤ 6 lines
```
RED = secrets (scan ADDED lines, counts only, never print) · a node deletion (resolve `D` by mint_id first: a move into
`deprecated/` is not one, trap 15) · a broken link · a protocol regression → no merge, one [red] dm. demote = node-text overclaim → merges as a residue.

## 3 · Tooling (/tmp/belam-passN/, rebuilt from the previous pass)
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
| suite lock `.agi/sessions/verify-suite.lock` | "free" = absent in MAIN and every post worktree (F7); no MAIN commit while it exists |
| MAIN is shared with thought-master | commit by exact path; never switch branches, never touch others' uncommitted edits |
