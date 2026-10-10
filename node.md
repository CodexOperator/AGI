---
id: goal:g7.16.1.11.28
mint_id: eeabc9b617d1468d80876bc7899b3d30
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.5
edited_by: director-general-1
goal_id: G7.16.1.11.28
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
scaffold_hash: 4f20a86d8a859974
season: 2
seeds:
  - goal:g7.16.1.11
status: horizon
tags:
  - council
  - v5
  - signers
  - provisioning
  - g7.16.1.11
title: "G7.16.1.11.28: a post home gitconfig never names a signers file that does not exist -- the unit rewrites ~/.gitconfig from the post own stale worktree at every start (engine-root.md:37)"
town: core
---
# goal:g7.16.1.11.28

## Why this exists
goal:g7.16.1.11: three post homes (director-general-1, all-is-one, self-perpetuating) had `~/.gitconfig` `gpg.ssh.allowedSignersFile=~/.signers`, a file that existed in no home, so `box read` refused EVERY mail and marked nothing held (DG1: 9 unread, 04:03-04:42Z); belam re-pointed the three to /var/lib/agi/allowed_signers at 04:48Z (backup /var/backups/agi-gitconfig-signers-20261009T044851Z). SM's placement said nothing in the repo writes ~/.signers. The writer IS in the repo, and it is not the cell: the trunk's own gitconfig cell (engine-post.md:119-128) has said `allowedSignersFile=/var/lib/agi/allowed_signers` since 677dacf312 (Oct 3, goal:g7.16.1.11.11.1.1), and the post unit rewrites the home's gitconfig at EVERY start from the post's own worktree: engine-root.md:37 ExecStartPre loops over `t/.agi/nodes/.geometry/engine.md` and `engine-[pw]*.md`, cuts each `### piece` into bin/ and then `mv bin/gitconfig .gitconfig`. So the home gets the cell of the post's OWN branch, and a post branch that predates 677dacf312 writes the OLD cell back. Measured on my own worktree: `git merge-base --is-ancestor 677dacf312 HEAD` fails, and my t/.agi/nodes/.geometry/engine-post.md:96 still says `allowedSignersFile=~/.signers` (and still carries the `### signers` piece at :108). The unit is root-pinned and no longer writes ~/.signers, so the old cell names a file nothing makes. I checked only my own branch; the other two homes are the same shape and not checked. CONSEQUENCE NOW: belam's re-point of ~/.gitconfig lasts only until the post's next unit start, which rewrites it from t/ again.

## Target end-state
- A post home's `gpg.ssh.allowedSignersFile` resolves to an existing, root-owned file after EVERY unit start, whatever commit the post's own worktree is at: the unit takes the gitconfig piece from a source that cannot lag the post (the pinned trunk bytes, as agi-signers is root-pinned), or refuses to start by name when the file the gitconfig names is absent.
- The stale posts are brought forward by the one lawful route (the rotation's trunk merge), not by hand; a one-time host act for a post that cannot rotate soon is belam's.
- A check any operator can run: every agi-* home's allowedSignersFile exists.

## Invariants
- ONE root-owned allowed_signers; no per-home signers file is created anywhere (goal:g7.16.1.11.11.1.1's rule stands).
- The mechanism is data in the graph (the cell and the unit step), not a per-post exception.
- Never fix a home by hand and call it done: a hand edit lasts until the next start.

## Falsifier
The deciding command is lane-based and has no existing name, so the first backticked command here is deliberately not a grep (agi-frontier reads it as mute, not met).
1. A lane builds a fixture home whose `t/` carries the OLD engine-post.md (cell `~/.signers`), runs the unit's own ExecStartPre piece-cutting step on it, and reads the resulting `.gitconfig`: its allowedSignersFile resolves to an existing file, or the step exits non-zero with a label naming the path; it exits 0 only then.
2. Regression guard only (SM 21:4xZ note: it is VACUOUSLY true on the trunk today, so it proves nothing about done; ONLY item 1, the lane, decides), kept as `sh -c` so agi-frontier cannot read it as met (it is already true on the trunk, so a bare grep here would read met on undone work): `sh -c "! git grep -q -E 'allowedSignersFile=~/[.]signers|signers>[.][.]/[.]signers' -- .agi/nodes/.geometry"` exits 0.
3. On a box: every agi-* home's `git config --file <home>/.gitconfig gpg.ssh.allowedSignersFile` names an existing file (belam's host check; values and the act are belam's).

## Out of scope
Re-pointing the three homes by hand (done, belam 04:48Z) · key generations and the contents of /var/lib/agi/allowed_signers (goal:g7.16.1.11.12) · the post unit's AGI_POST (goal:g7.16.1.11.24).

## RULE SM placement 05:0xZ 10-09, from belam (SM's relay text; its claim that nothing in the repo writes ~/.signers is corrected above)
"(B) SIGNERS PATH AT PROVISIONING: 3 homes (director-general-1, all-is-one, self-perpetuating) had ~/.gitconfig gpg.ssh.allowedSignersFile=~/.signers, a file in no home, so box read refused EVERY mail and marked nothing held (DG1: 9 unread, 04:03-04:42Z); belam re-pointed them to /var/lib/agi/allowed_signers 04:48Z. NOTHING in the repo writes ~/.signers (git grep: only a comment, agi-fresh.t.sh:33), so the writer is host provisioning outside the trunk: the leaf names finding it as step 1, then one place that writes the path for every new home, and a check that every agi-* home's allowedSignersFile resolves to an existing file. Values and the host act are belam's."

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
10-09 06:5xZ: filed on SM placement 05:0xZ. HORIZON. SM said nothing in the repo writes ~/.signers; CORRECTED by me on the bytes: the writer is the post unit ExecStartPre (engine-root.md:37) which cuts every ### piece of the post OWN t/ engine*.md into bin/ and does mv bin/gitconfig .gitconfig at EVERY start, so a post branch that predates 677dacf312 (Oct 3, goal .11.1.1) writes the old cell back. Measured on my own worktree only: merge-base --is-ancestor 677dacf312 HEAD fails; t/ engine-post.md:96 still says allowedSignersFile=~/.signers; the other two homes are the same shape, unchecked. CONSEQUENCE flagged to SM: belam hand re-point lasts only to the next unit start. Falsifier is lane-based (first command mute, not a grep that reads met on the already-good trunk). No prior version.
<!-- THOUGHT:END -->
