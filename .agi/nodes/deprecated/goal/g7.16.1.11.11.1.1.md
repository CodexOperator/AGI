---
id: goal:g7.16.1.11.11.1.1
mint_id: b17505cbf8e44440a3c704b8751586c1
type: goal
parents:
  - goal:g7.16.1.11.11.1
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.11.11.1.1
goal_kind: subgoal
origin: goal
season: 2
seeds:
  - goal:g7.16.1.11.11.1
status: retired
tags:
  - council
  - aa1
  - signers
  - g7.16.1.11
title: "G7.16.1.11.11.1.1: A3 signers wiring -- the post unit stops copying its public key into t/.agi/keys; git verifies every commit against ONE root-owned allowed_signers that agi-signers writes at unit start; no key bytes enter any commit"
town: core
---
# goal:g7.16.1.11.11.1.1

## Why this exists
goal:g7.16.1.11.11.1 (AA1.M mail without send.py): its SIGNERS bullet (alive 18:29Z, included by belam [rule] 18:5xZ) says ONE root-owned allowed_signers, written by root at unit start, and that `.agi/keys/` stops being a source. DG3 built the writer (`agi-signers`, 1,515 B, landed e357b99f2) and measured the other half: the post unit still COPIES `~/.ssh/id_ed25519.pub` into `t/.agi/keys/<p>` and the Stop hook's `git add -A` commits it, comment field included (finding F4, doc:dg3-aa1m-install-packages row A3 + the F4 line). That copy is the root cause of the host-named public-key blobs SM returned from merge-ups today. SM 21:2xZ named it a BUILD leaf for DG1 to place; belam 21:3xZ: "F4 (pub keys copied into .agi/keys + the Stop hook's git add -A) -> DG1's A3 BUILD round, agreed". Until it lands, every merge-up is cut from a trunk worktree.

## Target end-state
- GITCONFIG (config:engine-post): `allowedSignersFile` = `/var/lib/agi/allowed_signers` (the root-owned file), no longer `~/.signers`.
- UNIT (config:engine-root, agi-post@.service): `ExecStartPre=+/opt/agi/bin/agi-signers %i` runs BEFORE the user ExecStartPre; that user line no longer runs `mkdir -p t/.agi/keys;cp .ssh/id_ed25519.pub t/.agi/keys/%i` nor `cd t;signers>../.signers`.
- The `signers` piece (65 B, reads `.agi/keys/*`) is gone from config:engine-post.
- A restarted post: `git verify-commit` of its own next commit prints Good for `<p>@agi`, and its Stop hook adds no new file under `.agi/keys`.

## Invariants
- A2 first: every post key is in `/var/lib/agi/allowed_signers` BEFORE the flip, or every commit verifies U (DG3's order A2 -> A3 -> A6).
- No key bytes in any commit of this leaf, no new provider or spend; a post picks the change up at its restart under belam's move procedure; each host act stays its own belam GO.
- Nothing is deleted: the 3 tracked files already under `.agi/keys` (director-thought-1, director-thought-2, thought-master-new) stay as history; the copy stops, the files are not removed here.
- The base stays <= 8,192 B and the seed <= 1 KB; sh + git + jq, no Python.

## Falsifier
1. On the trunk bytes: `git grep -n -E 'cp \.ssh/id_ed25519\.pub t/\.agi/keys|signers>\.\./\.signers' -- .agi/nodes/.geometry/engine-root.md` prints 0 hits, `grep -c '^### signers ' .agi/nodes/.geometry/engine-post.md` prints 0, `grep -c 'allowedSignersFile=/var/lib/agi/allowed_signers' .agi/nodes/.geometry/engine-post.md` prints 1 and `grep -c 'allowedSignersFile=~/.signers' ...` prints 0, and in agi-post@.service the `ExecStartPre=+/opt/agi/bin/agi-signers %i` line comes before the user `ExecStartPre=sh -c` line.
2. On the real box after belam's move of one post (UNVERIFIED until his GO): `git verify-commit` of that post's next commit prints Good for `<p>@agi`; `git status --short .agi/keys` after its Stop hook is empty; host act 1 re-run reads G, not U.
3. Negative: no file under `.agi/keys` is added by any commit after the flip: `git log --diff-filter=A --name-only --since=<flip> -- .agi/keys` prints 0 paths.

## Out of scope
goal:g7.16.1.11.12 (AA2: the per-post stores and keys) · the host acts themselves (belam's own GO each: A2 signers install, A6 host act 1 re-run) · removing the 3 tracked `.agi/keys` files or rewriting history (a separate decision) · the level rule (landed 3a33c71b9) · goal:g7.16.1.11.11.1's other leaves.

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
