---
id: doc:radically-simple-engine
mint_id: ad68a997a9274ca6a13490561478b768
type: doc
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: all-is-one
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
**What am I ACTUALLY trying to get the machine to do here?** Know, per piece, whether the machine still needs it once the kernel, git and systemd do their own jobs, and what it costs in bytes. Nothing is deleted: a SCRAP or REPLACE-BY file is retired and moved (`status: deprecated`), after its replacement passes the spike.

Measured at HEAD 09-30 22:xZ (alive + all-is-one): engine ~5.13 MB · 137 files · 718 git worktrees.
| piece | KB | verdict | by what | from § |
|---|---|---|---|---|
| rotate.py | 1,175 | REPLACE-BY | the post wrap (agi-post@.service + post-wrap.sh): auto-rotate on the meter flag, no command | §1 §4 |
| send.py (+ magic_pane router on core) | 310 | REPLACE-BY | message = a file in the recipient's inbox dir, committed; unread derived; one route | §6 |
| write.py + node_writer.py + write_guard.py | 329 | REPLACE-BY | `agi-write` + `agi-read` (<= 2 KB sh) | §2 |
| heal.py | 206 | REPLACE-BY | `Restart=always` on the post unit | §1 §4 |
| grid.py | 95 | REPLACE-BY | `git log --follow` / `git show`; refs/grid frozen as archive | §3 |
| rotation_alert.py (hook) | 84 | REPLACE-BY | a ~20-line meter hook that writes the rotate flag | §1 §4 |
| src/seatsig/ | 82 | SCRAP | git SSH-signed commits + `allowed_signers` + the kernel | §1 §2 |
| spawn_budget.py | 52 | REPLACE-BY | the user slice's TasksMax + `systemctl list-units 'agi-*'` | §1 |
| stitch.py | 51 | REPLACE-BY | `git archive <sha>` | §3 |
| branches.py | 28 | REPLACE-BY | per-node trees on the fly | §4 |
| envfile.py | 26 | REPLACE-BY | a 0600 env file in the post's own home | §1 |
| suite_guards.py + the suite lock | 18 | SCRAP | tests read a snapshot of the tip | §4 |
| zoom.py + brief.py + briefing.py | 207 | REPLACE-BY, mostly | the files each user's harness already loads (settings symlinks, card, template) | §1 §3 |
| guard-init.sh + mem_cap.py | 70 | REPLACE-BY, mostly | per-user slice MemoryMax; keep only the box-survival layers | §1 |
| spawn_gate.py + evidence_gate.py | 101 | KEEP the rules | as `schema-check` (budget <= 10 KB, reading .agi/context/schemas), then retire the rest | §2 |
| viewport.py | 53 | KEEP | THE one render | §3 |
| graphweb.py + dashboard.py | 87 | KEEP | optional human views over the same files | §3 |
| links.py · hierarchy.py · locations.py | 127 | KEEP, trim | pure reads of rows and files | - |
| provisioning.py | 77 | KEEP | provider keys are budget, not identity; they land in the user's env file | §1 |
| dispatch.py · workflow.py · cli.py | 714 | KEEP core, trim | the kid spawn and review runs stay; seat/session/worktree/index-lock parts go | §4 |
| crons.py · anonymize.py | 92 | KEEP | the crontab from the graph · the token refusal inside `agi-write` | §2 |
| adapters/ | 78 | KEEP until `agi-mcp` covers their verbs | §5 | §5 |
| sensei · season · metrics · level3 · snapshot-* · handoff · decompose-engine | - | OUT OF SCOPE | research and loop tools; not judged here | - |

```
retired      ~2.41 MB certain (rotate … write_guard) + ~0.33 MB "mostly" (brief/zoom, guard, stitch)  ≈ 2.7 MB of 5.13 MB
new code     post wrap ~11-13 KB (§1, incl. the rows -> sysusers agi.conf generator) · agi-write + agi-read <= 2 KB (§2) · schema-check <= 10 KB (§2) · agi-mcp <= 8 KB (§5)  ≈ 31-33 KB
tests        their suites retire with them (test_rotate* ~10.5k lines · test_send ~8.1k · test_after_join_service ~3.1k ...); each new piece ships with the spike as its test
```
The rough share that exists ONLY because every post is one Unix user: seatsig ~100% · rotate ~25-35% · heal ~25% · send ~20-25% · spawn_budget ~20% · write ~15% (a Sonnet survey, low confidence).

## §8 Spike falsifiers
**What am I ACTUALLY trying to get the machine to do here?** Prove, on a throwaway repo under /tmp, that the kernel, git and systemd carry what the Python carried, BEFORE anything is retired. The spike runs only after the owner's go on this doc; until then `getent passwd | grep -c '^agi-'` = 0.

Setup: two spike posts `agi-spike-a`, `agi-spike-b` (declared the same way §1 declares posts) · one repo `core.sharedRepository=group`, umask 002 · `agi-write` + `agi-read` from §2 · one `agi-post@.service` from §1.
| # | claim | run | PASS | FAIL (= the doc changes, not the spike) |
|---|---|---|---|---|
| a | two users commit signed into ONE shared repo | a and b each `agi-write` 100 edits to their own nodes, concurrently | 200 commits on the branch · `git log --show-signature` verifies all 200 against `allowed_signers` · `git fsck` clean · zero lost writes (CAS losers retried) · the shared checkout's `git status` clean | any EACCES under `.git/objects` or `refs/` · a lost write · a stale shared index |
| b | the kernel refuses a cross-post node write | b: `echo x >> <a's node>`; b: forge a private-index commit touching a's node | the append fails EACCES · the landing audit (signer owns every path it touches) flags the forged commit | the write lands, or the forge passes the audit |
| c | Claude Code + pi run AS each user; messaging = graph files | start both harnesses as a and as b with their settings symlinked from the graph; a writes a message file into b's inbox | each harness starts and reads its own settings · b's hook reports "1 unread" within one poll · no send.py in the path | a harness refuses to run as the user · the message needs a daemon |
| d | one memory slice per user | a stress process in a's unit past its MemoryMax | killed inside a's slice; b's session untouched | b's process is hit, or the box is |
| e | every read/write path is tracked onto the post, graph or not (owner 22:0xZ) | a reads and writes files inside and outside `.agi/nodes` | each path appears in a's track (audit keyed on a's uid, flushed by the wrap) and none in b's | a path is missing, or attributed to the wrong post |
| f | ownership is stable | a mints a node; restart the unit; reboot the box | the node is still owned by a's SAME uid and a can still edit it | the uid changed (the DynamicUser arm fails here; the sysusers arm is expected to pass) |
| g | auto-rotate and auto-heal with NO command (self-perpetuating amends) | write the meter flag; kill the harness; remove a's key | a fresh session slots into the wrap each time with the card as its first input; the key is re-minted and its row updated by one `agi-write` | a human or a second script has to act |
Fallback named in advance: if (a) or (b) fails on one shared repo, each post pushes from its own tree to one bare repo whose per-path push rules are off-shelf (gitolite), and the kernel gate moves to the push.
