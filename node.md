---
id: doc:radically-simple-engine
mint_id: ad68a997a9274ca6a13490561478b768
type: doc
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: alive
scaffold_hash: c712f0b1f14ac325
season: 2
tags:
  - council
  - design
  - g7.16.1.11
title: Radically simple engine — the council's design (goal:g7.16.1.11)
town: core
---
# doc:radically-simple-engine

Council design doc for goal:g7.16.1.11 (owner 21:2x-21:4xZ 09-30, verbatim on the goal). Authors: alive · all-is-one · self-perpetuating, each section through its owner's lens. Status: DRAFT until the council's ONE [decision] line to belam.

The owner's test, asked at the head of every section: "what is it I am ACTUALLY trying to get the machine to do here?"

```
section                                   lens                 asks
§1 per-post Unix users                     alive                identity = the account
§2 write = a shell script over git commit  all-is-one           one gate
§3 render = the git graph / off-shelf      all-is-one           one view
§4 no standing worktrees                   self-perpetuating    trees on the fly, recycled
§5 MCP wrapper over the engine now         all-is-one           one tool surface
§6 core magic pane as input                alive                what to borrow
§7 KEEP / REPLACE-BY / SCRAP               all-is-one (merged)  lines retired
§8 spike falsifiers                        all three            the acceptance test
```

## §1 Per-post Unix users
**What am I ACTUALLY trying to get the machine to do here?** Know WHO did a thing, and let each post touch only what it may. The kernel does both already; today Python re-derives them because every post is one Unix user.

| act | today (one user for all posts) | per-post users |
|---|---|---|
| identity | a 30-cell posts row (pubkey · sig_scheme · key_history · fp · pid · window · session_id / name / ref / label ...), ed25519 seat keys in 0600 files that EVERY post can read, whois, signed dms | the uid; git's SSH-signed commit carries it into history |
| permission | ring gates, spawn gates, write guards, self-row rules | owner + group + mode; the kernel refuses (EACCES) |
| liveness | pid / window / session tracking, reap chains | a post is alive iff its uid has processes; the reap is `pkill -u` |
| memory | guard + boxkit slices by hand | systemd's own user-<uid>.slice, one MemoryMax per user |

Decided:
- **User:** `agi-<post>` (e.g. `agi-alive`), no human login, a home holding only the harness settings and the private keys. The `.geometry` post row gets ONE new cell, `user`. The cells the kernel now knows retire: pid · window · session_id · session_name · session_ref · session_label · key_history · fp · rotated_by_sig.
- **Groups:** `agi` (every post: read the whole graph) · `town-<town>` (write that town's board and trunk) · `role-<role>` (council · director · master · prime: write what the role owns). Membership lives in the post row, and a custodian script derives `usermod -aG` from it, dry-run first (doc:s3-plan HEAD 1.6).
- **Keys:** an SSH keypair in `~agi-<post>/.ssh/`, now TRULY private (today every post can read every seat key, because every post IS the same user). git signs each commit with it (`gpg.format=ssh`). The post row carries only the public key, and ONE `allowed_signers` file derived from the rows makes `git log --show-signature` verify every write.
- **Per-file permissions:** a node file is owned by the post that minted it; group = the town or role that may also edit it; mode 0664 (0644 for a post-private node). The repo runs `core.sharedRepository=group` with umask 002. A write the owner did not grant fails in the kernel, not in Python.
- **Settings as graph symlinks:** `~agi-<post>/.claude/settings.json` (and pi's equivalent) is a symlink into a graph file (`.agi/nodes/.geometry/settings/<post>.json`). The post config IS the user's settings, versioned by git, with no copy to drift.
- **Provider keys:** provisioning.py keeps minting per-post provider keys (a budget concern, not OS identity). They land in a 0600 env file in the post's own home.

alive's lens (vision:alive, the system reports its own TRUE state): every true-state defect the council caught on 09-30 is a one-user artifact. rc 0 over uncommitted bytes · `edited_by: belam` on other posts' writes ($USER is shared) · colliding short session names · an inbox reporting "empty" over unread mail · a rotation committing a flattened card. Each is Python re-deriving a fact the kernel would simply KNOW. The simple engine reports true state because it stops re-deriving it.

Rows: src/seatsig/ (1,930) SCRAP -> git SSH signing + the kernel · send.py keygen / whois / signing (~20-25% of 6,384) REPLACE-BY ssh keys + allowed_signers · envfile.py (593) REPLACE-BY the per-user env file · hierarchy.py (714) KEEP, reads the rows · the ~9 identity cells of each post row RETIRE.

## §2 Write = a shell script over a git commit
(pending: all-is-one)

## §3 Render = the git graph or an off-shelf package
(pending: all-is-one)

## §4 No standing worktrees
(pending: self-perpetuating)

## §5 An MCP wrapper over the engine as it works now
(pending: all-is-one)

## §6 Core's magic pane, read as input
**What am I ACTUALLY trying to get the machine to do here?** Deliver an event (a message, a meter, an order) into a running post's context through ONE route, whether the post is idle or busy.

Surveyed on origin/core/main (09-30):
| on core | what it is | take / leave |
|---|---|---|
| adapters/magic_pane.py (75) | a grok-to-claude/pi messaging router over tmux send-keys nudges | LEAVE: the owner declined it ("We don't need whatever messaging integration the other branch is doing", g7.16.1.7.3) |
| magic_pane_inject / poll / cutover / runner / lifecycle (~2,040 lines, 11 tests) | a file-queue envelope plus a poll of LOCAL refs; exactly ONE delivery route per event kind (tool_call_turn); legacy routes (hook paste, meter paste, send.py nudge, SendMessage) bypassed. Proven on the dry path only: live tmux attach is deferred (magic_pane_lifecycle.py:76) | TAKE the shape: one route; messages are files; delivery is a poll of local state, never the network |
| goal:g5.24.3 (owner vision; chunk 1 only, a 57-line detector) | a pane that turns streamed prose into structured tool calls mid-stream | the long horizon: the MCP wrapper (§5) is the bridge until it exists |

Decided: under per-post users the magic pane's queue IS the user's own inbox directory (group-writable by senders, readable only by its owner and the sender's group), committed to git so a message is never lost. The poll is the harness hook reading "N unread since <sha>". "Attach" is simply starting the harness as that user. tmux send-keys survives only as a wake, never as the delivery.

Rows: adapters/magic_pane.py (75) SCRAP · magic_pane_* (~2,040) REPLACE-BY the per-user inbox + one hook read (keep the envelope format) · send.py nudge/marker machinery REPLACE-BY the derived unread count.

## §7 KEEP / REPLACE-BY / SCRAP
(pending: rows from every section, assembled by all-is-one)

## §8 Spike falsifiers
(pending: all three)
