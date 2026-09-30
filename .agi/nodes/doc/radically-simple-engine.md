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

## §1 Per-post Unix users -- a post is a wrap (separation · auto-rotate · auto-track · auto-heal keys)
**What am I ACTUALLY trying to get the machine to do here?** Keep ONE post alive across any number of sessions: know everything it did, let it touch only what it may, and hand each new session the last one's state, with no command from anyone. The owner's shape (22:0xZ): "The post is like a wrap or shell around whatever session slots into it. It auto-rotates, no command needed, it auto-tracks actions, it auto heals keys ... Aim for kilobytes of code not megabytes."

**Separation: the one primitive everything else rests on**
| option | what | root, once | who-did-what comes from | verdict |
|---|---|---|---|---|
| A · per-post Unix users via **systemd-sysusers** | ONE declarative file `/etc/sysusers.d/agi.conf` (`u agi-<post> -` + `m agi-<post> town-<town>` / `role-<role>`), GENERATED from the post rows (the rows are the source), applied by `systemd-sysusers` (idempotent, off-the-shelf, no useradd scripting); `agi-post@.service` runs `User=agi-%i` | yes (applying the file) | the kernel: a STABLE uid owns node files, mode bits, audit by uid; the signing key has a stable home | RECOMMENDED (all-is-one's lens, 22:0xZ): lighter AND stable, zero custom user code |
| B · a systemd unit per post with `DynamicUser=` | systemd allocates the uid per unit start (hashed from the name, re-picked on collision) and expects it to own files only under StateDirectory; ProtectSystem=strict comes with it | yes (the unit template) | the same kernel facts, but only while the unit runs | the spike's COMPARISON ARM: our permission unit is a node file in a SHARED repo, so its owner must be a stable uid (falsifier (e)) |
| C · same uid, one user unit (cgroup) per post | `systemd-run --user --unit=post-<post>` | no | env (GIT_AUTHOR, AGI_ACTOR) + git hooks only | REJECTED: permissions stay in Python, which is exactly the one-user problem |
Either way the unit IS the post: `agi-post@<post>.service` (User=agi-%i under A, DynamicUser under B). Falsifier (e), in §8: a node minted by the post survives a reboot still owned by the same uid.

**The wrap, written out whole (the owner's stretch bar 22:1xZ: "so low that it feels like it doesn't even exist"). These ARE the files; `wc -c` counts them.**
```
# /etc/systemd/system/agi-post@.service (447 B) -- ONE template for every post; the instance name IS the post
[Service]
User=agi-%i
Group=agi
WorkingDirectory=/srv/agi
Environment=GIT_AUTHOR_NAME=%i GIT_COMMITTER_NAME=%i
RuntimeDirectory=agi-%i
ExecStartPre=-/bin/sh -c 'test -e ~/.ssh/id_ed25519||ssh-keygen -qt ed25519 -N "" -f ~/.ssh/id_ed25519'
ExecStart=/usr/bin/dtach -N /run/agi-%i/s claude
ExecStopPost=/bin/sh -c 'git ls-files -m|xargs -r find -user agi-%i|xargs -r git commit -qm "%i: exit" --'
Restart=always
[Install]
WantedBy=multi-user.target
# agi-inbox@.path (42 B) + agi-inbox@.service (99 B) -- delivery = a file lands in the post's inbox dir
[Path]
PathChanged=/srv/agi/.agi/inbox/%i
[Service]
User=agi-%i
ExecStart=/bin/sh -c 'echo "new mail: .agi/inbox/%i"|dtach -p /run/agi-%i/s'
# the meter hook, in the ONE settings file every post's harness links to (295 B) -- AUTO-ROTATE
{"hooks":{"UserPromptSubmit":[{"hooks":[{"type":"command","command":"jq -r .transcript_path|xargs tail -1|jq -e '.message.usage|.input_tokens+.cache_read_input_tokens+.cache_creation_input_tokens>470000'>/dev/null&&echo 'At the line: write your card, git commit it, then run: kill $PPID'"}]}]}}
# /etc/gitconfig (79 B) -- every commit SSH-signed by the post's own key
[gpg]
format=ssh
[commit]
gpgsign=true
[user]
signingkey=~/.ssh/id_ed25519.pub
# /etc/audit/rules.d/agi.rules (55 B) -- AUTO-TRACK every open, graph or not, recorded with the post's uid
-a always,exit -F arch=b64 -S openat -F gid=agi -k agi
# /etc/sysusers.d/agi.conf (26 B) -- generated from the post rows; ONE line per post
g agi -
u agi-alive -:agi
```
| act | how, in the files above |
|---|---|
| auto-rotate | the meter hook tells the session at the line to write its card, commit it and exit; `Restart=always` starts a FRESH session, which loads the card through the harness's own instruction file (a symlink into the graph) |
| auto-heal | `Restart=always` (a crash is the same path as a rotation) · `ExecStartPre` regenerates a missing key (the public key reaches the row on its next commit) |
| auto-track | graph writes: every commit is authored AND SSH-signed as the post · every other read/write: one audit rule records each open with the post's uid (`ausearch -ui <uid> -k agi`) |
| write | the post's own `git commit` of a node (the tree-free, CAS form: §2, §4); `ExecStopPost` salvages any file the post still owns uncommitted at exit |
| message | write a file into `.agi/inbox/<post>/`; the `.path` unit pushes one line into the live session through `dtach -p` |
| human view | `dtach -a /run/agi-<post>/s` attaches to any post's live session |
| memory | a per-post drop-in (`MemoryHigh=`) only where a post needs one: tens of bytes |

**The count: the whole wrap = 1,043 bytes of our code; one post = 18 bytes (its sysusers line) plus one enable symlink.** "A post in tens": MET. "The wrap in hundreds": missed by 44 bytes (the meter hook's jq line is the fattest, 295 B). The megabytes live in what is already written and tested: the kernel, systemd, git, auditd, jq and dtach (two small packages, `auditd` + `dtach`, installed on the owner's go).
**Where the bar cannot be met, and why:** the graph checker (schemas + links, §2) and the MCP wrapper (§5) are the only pieces that still need kilobytes; both can drop to configuration if an off-the-shelf JSON-schema validator reads the schemas as data and an off-the-shelf shell/filesystem MCP server runs as each post user. Root setup is required ONCE (the unit files, the sysusers file, the audit rule, two packages): the owner's go, per the goal's invariant.

**What the post row keeps:** name · role · town · template · harness · model · effort · owning_goal · memory · the public key. The kernel or the unit now holds the rest, which retires: pid · window · session_id / name / ref / label · key_history · fp · rotated_by_sig · generation.

alive's lens (vision:alive, the system reports its own TRUE state): every true-state defect the council caught on 09-30 is a one-user artifact. rc 0 over uncommitted bytes · `edited_by: belam` on other posts' writes · colliding session names · an inbox reporting "empty" over unread mail · a rotation committing a flattened card. Each is Python re-deriving a fact that the kernel, git or systemd simply KNOWS once a post is a unit with its own uid. The wrap reports true state because it stops re-deriving it. It is antifragile the same way: a dead session is just the loop's next turn.

Rows: rotate.py + heal.py + rotation_alert.py (1,465 KB) REPLACE-BY agi-post@.service + the meter hook (~740 B) · seatsig + send.py signing/whois (~160 KB) SCRAP -> ssh keys + git signing + the uid · spawn_budget.py (52 KB) REPLACE-BY the unit's TasksMax · envfile.py (26 KB) REPLACE-BY a 0600 env file in the post user's home · hierarchy.py KEEP (reads the rows).

## §2 Write = a shell script over a git commit
**What am I ACTUALLY trying to get the machine to do here?** Record ONE new version of ONE node, by ONE post, so that everyone sees it, nobody else could have made it, and exit 0 means it landed.

```
the post's harness edits the file  ─▶ the KERNEL checks it (mode bits, §1): EACCES = refused, no Python
        │
agi-write <node-path> [-m why]      ~30 lines of sh, the ONE write path for every role (human, Claude, pi, kid, MCP §5)
                                    budget: agi-write + agi-read <= 2 KB together
  1 schema-check <node-path>        the one check that stays code (spawn_gate + evidence_gate rules, read from .agi/context/schemas); exit 2 BY NAME
  2 anonymize check <node-path>     the token refusal, unchanged
  3 GIT_INDEX_FILE=$(mktemp)        a PRIVATE index: no shared index.lock, no suite lock
    git read-tree $old && git update-index --add -- <node-path>
  4 new=$(git commit-tree -S $(git write-tree) -p $old -m "<why>")   signed by the uid's SSH key (§1)
  5 git update-ref refs/heads/<branch> $new $old                        compare-and-swap; the loser re-reads and retries N s, else exit 3 BY NAME
exit 0  ⇔  the signed commit is on the branch  (by construction, not by policy)
```
Decided:
- **Attribution is the signature.** `--actor`, `--role`, `--session`, `edited_by`, `thought_session`, the role ceiling and the ring signatures (`--ring-sig/-fresh/-fields`) retire: the uid signs, and `allowed_signers` (derived from the post rows) verifies.
- **The verb grammar retires.** `set · sub · row · replace · read · note · payload · patch` are 16 verbs re-implementing what every harness already has (its own Edit tool, `sed`, `cat`). The file is edited by whatever the post already uses; `agi-write` only lands it. `--dry-run` = `git diff`.
- **The commit message IS the THOUGHT.** "body is state, thought is delta" is exactly file vs commit message. The THOUGHT block stays in files until §3's render shows `git log -1 --format=%B -- <node>` beside the node, then it retires. One source.
- **The protected fields stay protected** (`id`, `mint_id`, `type`): schema-check compares them to `$old` and refuses a change.
- **commit-tree runs no hooks**, so steps 1-2 run INSIDE the script and never in a hook alone. A post that forges a commit by hand is caught by the landing audit: every commit on the ref is signed by a uid that owns (or shares the group of) every path it touches (§8 b).
- **Trap, named:** the shared checkout's own index lags a private-index commit (its `git status` shows the file as a reversal). `agi-write` refreshes that ONE path in the shared index afterwards (`git update-index -- <path>`, a millisecond lock, retried). Nobody ever `git commit`s through the shared index again: `agi-write` is the only path. Spike (a) proves it.
- **agi-read <mint-id|path>** = resolve the path, then `cat` (the read half of the owner's "system read/write pair that adds up to git").
- **Mint id -> path**: `git grep -l "^mint_id: <id>" -- .agi/nodes` (or one derived index file). The address may change; the mint id never does.

Rows: write.py 231 KB + node_writer.py 83 KB + write_guard.py 15 KB REPLACE-BY `agi-write` + `schema-check` · spawn_gate.py + evidence_gate.py 101 KB KEEP their rules, as `schema-check` · the ring layer (src/seatsig/rings.py, inside §1's seatsig row) SCRAP.

## §3 Render = the git graph or an off-shelf package
**What am I ACTUALLY trying to get the machine to do here?** Show any reader, human or model, the graph's shape and one node's story, from the SAME files, by ONE path.

```
edges     = frontmatter `parents:`       (already the graph; no store beyond the files)
versions  = git log --follow -- <node>   (one write = one commit, §2: the grid is git's own history)
picture   = one short emitter -> graphviz DOT / JSON  (off-shelf: graphviz; graphweb's 3D view reads the same JSON)
the node  = cat <file> + git log -1 --format=%B (its THOUGHT, §2)
the kid   = viewport.py --emit llm       (THE one render script: one stream, two readers, g2.19 / g4.18.7)
```
Decided:
- **viewport.py stays as the ONE render script.** Everything else that renders is either a reader of its stream or retires: zoom / brief / briefing assembly becomes the files each user's harness already loads (§1 settings symlinks); `write.py 'read body N:M'` retires with write.py; `grid.py log|diff|versions|payload` = `git log|diff|show`.
- **BUILD-CONTRACT regeneration is render, not write.** A regenerated block inside an authored file is a second writer; render derives it on read and never commits it back.
- **refs/grid/\* freezes, never deleted.** New versions stop landing there; the existing refs stay as the archive of the pre-simple era (Nothing is deleted).
- A second read path is the defect this section exists to prevent: every reader reads files through viewport or plain git.

Rows: grid.py 95 KB REPLACE-BY git log/show (refs frozen) · stitch.py 51 KB REPLACE-BY `git archive <sha>` (it assembled a tree from grid versions) · viewport.py 53 KB KEEP, the one render · graphweb.py 56 KB + dashboard.py 31 KB KEEP, optional human views over the same JSON · zoom.py + brief.py + briefing.py 207 KB REPLACE-BY, mostly: harness-loaded files.

## §4 No standing worktrees
**What am I ACTUALLY trying to get the machine to do here?** Two things only: (1) change a node, and (2) run some code (a test, a kid's build) against a chosen mix of commits. Neither needs a checkout that outlives the act. And from the generations lens: what the next session of a post inherits must be exactly what the last one COMMITTED. Nothing else.

**Measured 22:0xZ 09-30 (MAIN, this box)**
| fact | number |
|---|---|
| registered worktrees | 718 (713 under .agi/worktrees; 716 real, 1 stale) |
| size of one | ~135 MB, 11,715 tracked files -> ~96 GB of the 233 GB used on /data |
| created in the last day / older than 3 days | 49 / 2 (most are thought-town iteration bases: de-base-* 311, de-h* 370) |
| per-generation state that is NOT a commit | 7,971 files under .agi/sessions (inbox 2,329 · workflows 2,295 · seats 2,053 · rotations 481) |
| engine lines coupled to trees | "worktree" in rotate.py 257 · cli.py 179 · heal.py 140 · dispatch.py 102 · locations.py 41 · spawn_budget.py 38 |
| write a node with NO tree (private GIT_INDEX_FILE -> hash-object -> update-index -> write-tree -> commit-tree) | 64 ms |
| a registration-free tree (a dir + a private index: `git --work-tree=D read-tree -u --reset <sha>`), fresh | 1.05 s, 148 MB, `git worktree list` unchanged |
| the same dir recycled to another sha | 0.69 s |
| a MIXED tree: `git merge-tree --write-tree A B` (4 ms) then read-tree into the dir | 0.15 s (HEAD x core/season2/main: clean) |

**The generations lens (vision:self-perpetuating).** A generation leaves exactly ONE thing behind: commits on its refs. Every other thing it leaves (a tree, a pid, a pane, a rotation record, a seat file, an inbox marker) is state the NEXT generation must reconcile. A reconciler is code, and each new kind of leftover grows it: rotate.py 23,229 lines · heal.py 4,291 · 69 of 322 test files. Project that across a thousand rotations and the reconcilers are the engine. Commits-only makes generation 1,000 cost the same as generation 1, and `git gc` is the only janitor.

**Decided**
```
act                    tree?          how                                                       lives
write / edit a node    NONE           §2 agi-write: private GIT_INDEX_FILE + commit-tree +      0 bytes on disk
                                      update-ref <ref> <new> <old>   (CAS; a lost race fails loud)
run code / tests       ephemeral      a SLOT = dir + private .index; fill = read-tree -u --reset   the act
kid builds code        ephemeral      same slot; commit = add -A on the slot's index -> write-tree   the kid's unit
                                      -> commit-tree -p <base> -> update-ref CAS; no `git worktree`
mix code across nodes  ephemeral      T = merge-tree --write-tree A B (fold for >2); fill a slot with T  the test run
                                      exit 1 = the mix does not compose = a finding, never a hand-merge
```
- **Slots are recycled, not minted.** They live in the post unit's `CacheDirectory=` (§1 option B): slot-0..N, N = the row's kid cap + 1. Recycling a slot is one `read-tree -u --reset <sha>` plus `git clean`-equivalent over the slot's index (0.69 s). Disk is bounded by posts x slots x ~140 MB (12 posts x 3 = ~5 GB, versus ~96 GB today). A fresh slot is the same command into an empty dir.
- **No `git worktree` at all.** A slot registers nothing in .git/worktrees, so there is no prune, no stale lock and no "branch already checked out" refusal, and a dead slot is just a directory.
- **Tests mix and match.** A test names its commits; the runner folds them through merge-tree and fills a slot with the result. It holds up: it is how git itself previews merges. Conflicts come out as data (the exit code plus the conflicted paths), never as a dirty tree someone must clean.
- **Refs, under per-post uids (the one open question this section hands to the spike).** Spike (a) proves that commits land in ONE shared repo; it does not prove who may MOVE a ref, and in one shared .git any group writer can move any ref (loose refs and packed-refs are group-writable files). Spike (h) tests that. If (h) fails, the zero-daemon fallback is tried before gitolite: each post owns a bare `graph.git` in its StateDirectory, whose `objects/info/alternates` points at the shared object store (zero copy). A post moves only its own refs, which the kernel enforces because they are its files. A master PULLS a merge-up with `git fetch` from the director's repo, and nobody pushes into another post's refs. This is git's own distributed model, with no hook and no daemon.

**When a session dies mid-card (alive's question), or mid-anything:**
```
card write  = ONE agi-write = blob -> tree -> commit -> update-ref CAS
  died before update-ref  -> the previous card stands (at most one step stale: cards are written DURING the work)
  died after              -> the new card stands
  there is NO third state: no working file to flatten or leave dirty (trap 10 and "a flattened card committed" vanish)
kid / test slot at death -> the unit's ExecStopPost: dirty slot? commit it to refs/salvage/<post>/<mint> (never onto a branch), then recycle
successor at wake        -> reads: the card node @ its ref + `git for-each-ref refs/salvage/<post>` -- nothing else
```
So post-wrap's "agi-write the card if still dirty" step (§1) is not needed: a card is never dirty. The successor has nothing to reconcile, because its predecessor could only have left commits.

**Migration (retire, never delete).** The 716 standing trees retire in three passes, and the destructive step waits for the owner's go: (1) list every tree with its branch, its dirty count and whether it is merged (read-only); (2) commit each dirty tree to `refs/salvage/...` (additive); (3) `git worktree remove` only for trees that are clean AND merged. That pass frees ~96 GB and is irreversible, so it is BANKED for the owner.

Rows (§4):
| piece | verdict | retires |
|---|---|---|
| rotate.py tree + closeout + fd + flatten/re-link paths (worktree x257) | REPLACE-BY agi-write (no tree) + salvage ExecStopPost | inside the §1 rotate.py row |
| heal.py orphan / worktree reconcile (x140) | SCRAP: nothing is left to reconcile | inside the §1 heal.py row |
| dispatch.py `--branch` worktree creation, stale-base refusal, merge-base plumbing | REPLACE-BY a slot fill + a CAS on the post's own ref | ~1.5k of 4,542 (estimate; spike measures it) |
| cli.py kid worktree / done / auto-commit (x179) | REPLACE-BY slot commit + ExecStopPost salvage | ~2k of 6,655 (estimate) |
| locations.py worktree-path mapping (x41) | REPLACE-BY slot = CacheDirectory; KEEP the nearest-`.agi/` resolver | ~300 of 1,218 |
| .agi/sessions/{rotations, seats, inbox markers, workflows run dirs} (7,971 files) | RETIRE (move, never delete) -> journald + git log + refs/salvage | files, not lines |
| the 716 standing trees under .agi/worktrees | RETIRE by the 3 passes above; pass 3 is the owner's go | ~96 GB |
| new: agi-slot.sh (fill · recycle · mix · salvage) | NEW | ~2 KB |

## §5 An MCP wrapper over the engine as it works now
**What am I ACTUALLY trying to get the machine to do here?** Give every role the SAME verbs the SAME way (a Claude post, a pi kid, a human), so the machinery underneath can be swapped without any caller noticing.

```
harness (as user agi-<post>) ──stdio──▶ agi-mcp  (spawned BY the harness, so it runs AS the uid: no token, no auth layer)
                                          │ tools (stable names)          today's body               simple body (after §1-§4)
                                          ├ read_node(id|path)            write.py read / viewport     cat + mint->path
                                          ├ write_node(path, why)         write.py                     agi-write (§2)
                                          ├ children / graph(id)          links.py / viewport          viewport --emit
                                          ├ send(to, text) · inbox()      send.py                      a file in the inbox dir (§6)
                                          ├ dispatch(node) · status()     dispatch.py / spawn_budget   unchanged / systemctl list-units
                                          └ log(node)                     grid.py log                  git log --follow
```
Decided:
- **Build it NOW over today's CLIs** (the owner: "wrapping the whole thing in an MCP now as it works partially"): each tool is a subprocess of the existing command, a few lines each. It is the stable seam: every §1-§4 retirement swaps one tool BODY, and the tool NAMES never change.
- **Off-shelf first:** the reference MCP filesystem and git servers already cover read / write-file / log / diff. agi-mcp adds only what they lack: schema_check, send/inbox, dispatch, status, graph.
- **pi and scripts call the same commands the tools wrap** (the scripts ARE the API; MCP is its protocol face). Nothing is reachable through MCP that is not also one plain command, and vice versa.
- **Not in the MCP:** rotate / spawn / key machinery (HELD, owner 21:3xZ); the magic pane (g5.24.3) later becomes the live face over the same tool names.

Rows: new `agi-mcp` (budget <= 8 KB, one file) ADD · adapters/ (claude_code 39 KB + __init__ 22 KB + copilot_cli 17 KB) KEEP until the MCP covers their verbs, then trim.

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
| .agi/worktrees (716 standing trees) + per-generation .agi/sessions state (7,971 files) | ~96 GB · files | RETIRE | recycled slots in each post unit's CacheDirectory · journald + git log + refs/salvage; removing the trees waits for the owner's go | §4 |
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
new code     post wrap ~11-13 KB (§1, incl. the rows -> sysusers agi.conf generator) · agi-write + agi-read <= 2 KB (§2) · schema-check <= 10 KB (§2) · agi-mcp <= 8 KB (§5) · agi-slot.sh ~2 KB (§4)  ≈ 33-35 KB
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
| g | auto-rotate and auto-heal with NO command, and a death loses nothing (self-perpetuating) | write the meter flag · kill the harness mid-card (after the card's commit-tree, before its update-ref) · remove a's key | a fresh session slots into the wrap each time, with the card @ a's ref as its first input · the card is the previous version OR the new one, never partial and never dirty on disk · the key is re-minted and its row updated by one `agi-write` | a human or a second script has to act · a half-written or dirty card |
| h | a post's refs are its own | b: `git update-ref <a's ref> <any sha>` in the shared repo | refused (EACCES) | the ref moves -> the §4 fallback (per-post bare repo + alternates, merge-ups pulled), then gitolite |
| i | no standing trees, and a killed kid loses nothing | a runs 100 test runs over mixed commits (merge-tree -> slot), then a kid is killed mid-edit | `git worktree list` count unchanged · slot disk <= (kid cap + 1) x 150 MB · the kid's dirty bytes are on `refs/salvage/agi-spike-a/<mint>` and its slot is recycled | a registered worktree appears · disk grows per run · the dirty bytes are lost |
Fallback named in advance: if (a) or (b) fails on one shared repo, each post pushes from its own tree to one bare repo whose per-path push rules are off-shelf (gitolite), and the kernel gate moves to the push.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
self-perpetuating, 22:1xZ 09-30: filled §4 (no standing worktrees) through the generations lens -- a generation leaves ONLY commits; measured 716 standing trees ~96 GB, 7,971 per-generation session files, a tree-free node write 64 ms, a registration-free slot 1.05 s fresh / 0.69 s recycled / 0.15 s mixed via merge-tree. Amended §8 (g) with the mid-card death, added (h) ref ownership and (i) slots + salvage; §7 gained the trees/sessions RETIRE row and agi-slot.sh in new code. Tree removal is irreversible and waits for the owner's go.
<!-- THOUGHT:END -->
