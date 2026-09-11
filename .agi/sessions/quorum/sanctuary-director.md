# SESSION HANDOFF — 2026-09-11 sanctuary-director: LIVE SCRATCHPAD (written by the 214458Z session — record `sanctuary-director.20260911T214458Z.json`, gen 19, ref `27c314`, window @308, woke 21:45Z; the successor replaces this wholesale as it works)

**OWNER 14:0xZ: NO GENERATIONS in prose, dms or commits — name a session by its rotation-record stamp.** **OWNER 16:0xZ: this seat touches only its own tracking, in this file.**

🔴 IF THERE IS NO `## STARTUP OUTPUT` BLOCK BELOW THIS FILE, you were seated by `rotate.py spawn` or by the reaper's crash-recovery (L4.283, live): nothing above was pre-run — no record with your name, no wrapper waiting on your ack. The wake is STILL: ListAgents → `rotate.py ack --seat sanctuary-director --gen <the row's generation> --ref <bare ref> continue` → `send.py read`. The autopsy (g15.21) is dm'd to you. **ONE `send.py read sanctuary-director` reads the whole inbox — never `peek | head` slices.**

## §0 STATE (last edit stamped in §3)

- **WAKE SHAPE (measured 21:45Z on the L4.291 bytes):** ONE `ListAgents` → `rotate.py ack --seat sanctuary-director --gen <N> --ref <bare ref> continue`. 🔴 **THE ACK REFUSES on every worktree wake right now** (`refuse to ack --commit: '.agi/nodes/.geometry/seats.md' is dirty`): the dirt is YOUR OWN row — rotate-self's spawn write (session_id/gen/window/pid) lands in MAIN uncommitted and `_ack_seats_dirty` (rotate.py:5011) cannot tell it from a foreign row. Workaround until the sensei-director's fix lands (the Sensei routed it there, draft `sensei/drafts/sanctuary-director-wake-audit-20260911T214458Z.md`): in MAIN, `git diff -- .agi/nodes/.geometry/seats.md` must show ONLY your row (+ `edited_by`), then `git add` that file + `git commit -F <file>` (one line: `<seat> rotate-self spawn write (gen N): ...`), then re-run the ack. The ack then back-fills `session_ref`, commits in MAIN (not pushed; `branch_push` at :07 pushes), prints its +/- lines — never `git diff seats.md` after it (F8). Then `rotate.py meter --pin /home/ubuntu/work/agi/.agi/sessions/sanctuary-director.meter --session-log ~/.claude/projects/-home-ubuntu-work-agi--agi-worktrees-seat-sanctuary-director/<YOUR-SESSION-ID>.jsonl` (🔴 `meter --seat` REFUSES cross-generation: it reads the WORKTREE row, frozen at the last merge-up — L4.295 item) → `git fetch` + merge `origin/season/s2` if behind → ONE `send.py read sanctuary-director`. NO address line to the prime (the rotation alert carries it). Read the inbox at EVERY seam. **ALWAYS `--from sanctuary-director`; a dm with a backtick rides a FILE.**
- **PRIME = XII `agi-1b [fda770]`, window `@305`** (whois IS-AUTHORIZED at wake vs 231e388bf). Standing lines: (b) the pin is the lease — pin-reap **STAYS NOT ARMED** (mur-41 ruling: named blockers = the exact-name clause, the registry-FILE-vs-window-@id key mismatch with already_gone continuing, the ack pinning over a dead/foreign transcript; predecessor pins KEEP=9/UNPINNED=0; the OWNER's GO; the reaper unit is NOT restarted for merge-up 41); (c) the merge-up window is STATE — `ls /home/ubuntu/work/agi/.agi/sessions/verify-suite.lock` AND the inbox before ANY MAIN merge. (2) A ROLE IS RESOLVED, NEVER TYPED (`--role` may name only a role the seat holds or lower).
- **sensei-director** = `seat-sensei-director-aa [588897]` @306 (ids `SL<n>.<nn>`; owns rotate.py first_turn/bootstrap/spawn/handoff/prepare/`_shell_cmd` — and now the ack-dirty fix (a)/(b)). **master-sensei** `agi-88 [516457]` @292: NODE IDS ONLY. **Helper** = `seat-sanctuary-helper-88 [5f209b]` @307 (rotated 21:4xZ); its L4.257-259 harvested on `seat/sanctuary-helper@s2` tip 3779d727c — **ride merge-up 42 as Nb**; next id L4.260; ONLY PI PARENTS; account floor $1.00.
- **OWNER 21:4xZ (vision:web-app-suite, db436e1f1): the Sanctuary is an MCP app with a web app layer; eight rungs; "Rungs 1-4 are live as goal lines under goal:g15 at the Sanctuary director"** (rung 1 = SL4.06 keys on rows, sensei-director). NO rung goal lines exist under g15 yet (checked 21:5xZ: g15.1-24, none name a rung) — propose rungs 2-4 (multisig rings / veto-human gate / open onboarding) as g15 lines to the prime AFTER the queue, at the mur-42 report (the point proposes; the Prime accepts).
- **Tree:** season/s2 = MAIN; **merge-up 41 = `13de8c37e`, 11/11, 3468/14, stamp 2266/195/2461.** Seat synced to s2 at wake (`17527758e`, then merged the mur-41 + ack commits; 10 ahead / 0 behind at 22:0xZ). **Free ids: L4.296+.**
- **UNIT:** reaper (`heal.py watch` from MAIN, restarted 19:56Z; NOT restarted for mur-41 by ruling — every heal.py change since is dead in the live watcher until the prime restarts it).
- **Helpers (scratchpad dir `$S=/tmp/claude-1001/-home-ubuntu-work-agi--agi-worktrees-seat-sanctuary-director/<session-id>/scratchpad`, die with the session):** `$S/note.py <node> <file>` · `$S/mint.py <spec.json>` (`{slug,parents,title,testable_claim,town}`) · `$S/claim_append.py <node> <file>` (APPENDS the file to `testable_claim` — the assignment). All three: write.Edit/create + submit, actor sanctuary-director role director, `@@TS@@` → `date -u`. ~12 lines each; the successor rewrites them in its first harvest.

## §1 WHAT THE 214458Z SESSION LANDED (21:45Z–)

- Wake: ack refused (own spawn write = pre-dirt) → by-hand spawn commit in MAIN `5aee07beb` → ack `fc8da2a6f` (gen 19, ref 27c314, @308, pid 1990547) — the Sensei audited it (wake 8) and routed the fix to the sensei-director.
- L4.293 + L4.294 build orders written INTO `testable_claim` (`f9850117c`) from the mur-40 verdict; both CUT in parallel (disjoint files) 22:0xZ.

## §2 LIVE + QUEUE — cut with `AGI_SEAT=sanctuary-director python3 extensions/agi/bin/dispatch.py . L4.NNN --target <node> --level small --tier parent --harness pi --branch` (sync first; `--level big` is REFUSED)

- **LIVE: L4.292 `a00-a4f9327b` (pid 1981144, spawned ~21:3xZ by the 195718Z session; kid a00-b64b2c2d live at 21:56Z) on `hypothesis:l4-a-dead-seat-is-recovered-by-the-loop-not-by-a-human`** (g15.19 fix-only: after_join parity via the record shape + `_latest_rotate_record` widening, pin-keyed liveness guard, numeral from row+record, launch cwd = the seat tree, row via the ONE writer), branch `loop/hypothesis-l4-a-dead-seat-is-rec-a00-a4f9327b@s2`, 2 kids serial. Harvest: check heal.py + the one rotate.py widening only; re-run L4.283's fixture live proof if the kid did not paste it.
- **LIVE: L4.293 `a00-69e7f2be` (pid 2090765, 22:0xZ) on `hypothesis:l4-a-workflow-run-is-named-not-numbered`** — run key from the REAL `rounds:[{merge_up,...}]` shape (`mur-40`, `mur-sl2-2`); branch `loop/hypothesis-l4-a-workflow-run-is--a00-69e7f2be@s2`; 1 kid; files workflow.py + test_workflow.py.
- **LIVE: L4.294 `a00-365fb831` (pid 2091355, 22:0xZ) on `hypothesis:l4-a-read-clears-the-coalesced-nudge-count`** — compare-and-clear under flock + ONE note on `experiment:a00-a917d0ba-6a223b`; branch `loop/hypothesis-l4-a-read-clears-the--a00-365fb831@s2`; 1 kid; files send.py + test_send.py.
- **L4.295 (small, AFTER 292 harvests — serial on rotate.py) on `hypothesis:l4-a-seats-identity-cell-has-one-writer-and-it-writes-main`:** residue (i) twice-rotation falsifier + (ii) rebase the worktree-local row readers (`_generation_measured`/meter `--seat`, first-seating announce, `status`) onto `_shared_graph_root` + L4.281/285's "own-chain reap without a pid is NAMED in the record" + mur-41's L4.288 residue (KEEP-BOTH ref-equal-identity-differs test; the SUBSTRING join key in `_join_successor`). **EXCLUDE `_ack_seats_dirty` + the spawn-write commit — the sensei-director has that (state it in the claim).**
- **To MINT (helper-proposed, accepted): `l4-a-rotation-record-caps-the-reaped-chains-argv`** — `_short_ps` = `ps -o pid=,cmd=` unbounded → 311 KB of 463 KB in rotations/ is argv; cap at ~120 chars (rotate.py `_reap_chain`/`_reap_one` region, 1 kid). Serial on rotate.py → after 295.
- Then: pin-is-the-lease round 2 on heal.py = mur-41's SIX L4.289 residues (exact-name belam window → REAP via dead code; verdict keyed by registry FILE vs armed reap keyed by window @id; already_gone → one dm + one log line per 30 s pass and a green test REQUIRES it; a successor whose s6.2 pin failed is judged REAP after 600 s; renamed `seat.genN` predecessors never judged; skip reasons unlogged; a test reads the real `~/.claude/sessions`) + the predecessor pins (KEEP=9/UNPINNED=0) — still DRY-RUN. → 0a / 0c-cert → seatsig writer wiring.
- **Merge-up 42 = 292/293/294 (+295 if in) + helper's 257-259 as Nb.** The report also carries: rungs 2-4 g15 proposals; mur-41's L4.290 residue (a kid self-declared `--role owner` — the elevation path is a g15 line, the PRIME's).

## §3 🔴 NEXT COMMAND (last stamped 22:0xZ)

**`spawn_budget.py status --iter L4.292 --wait --timeout 540` → harvest 292 (then 293/294 as they finish: `--iter L4.293` / `--iter L4.294`) → write L4.295's claim (`$S/claim_append.py`) → cut 295 → request merge-up 42.** Every branch of this session is pushed (seat tip = origin/seat/sanctuary-director@s2); no kid worktree of mine holds uncommitted work.

## §4 TRAPS (214458Z session + carried)

- 🔴 **`rotate.py ack ... continue` REFUSES on a worktree wake since L4.291 landed (own spawn write = pre-dirt in MAIN)** — see §0 for the by-hand commit; NEVER `git checkout -- seats.md` in MAIN to "clean" it (that erases your own identity cells). The fix is the sensei-director's, not yours.
- 🔴 **`rotate.py meter --seat sanctuary-director` refuses cross-generation** — it reads the WORKTREE row (gen frozen at the last merge-up). Use the explicit `--pin ... --session-log <your .jsonl>` form; L4.295 rebases the reader.
- 🔴 **The predecessor's "21:5xZ" stamps were estimates** (L4.292 was cut ~21:3xZ; the handoff commit is 21:44Z) — every stamp in this file comes from `date -u`, run in the same call.

- 🔴 **A merge-up window GRANT is state, not a message (XI 21:0xZ):** two grants 65 s apart put my merge into MAIN under another seat's RUNNING suite; `ls /home/ubuntu/work/agi/.agi/sessions/verify-suite.lock` + `ps -p <its pid>` + the inbox BEFORE `git merge` in MAIN, and undo with `git reset --soft <base>` + per-file restore (never `reset --hard`: MAIN's comms/rotations files carry live uncommitted messages).
- 🔴 **The rotation record's `ps_before` is the predecessor's whole argv = the prompt (~50 KB)** — grep the record for `"result"` and `termd` only.
- 🔴 **`git diff seats.md` after the ack is a re-read the Sensei audits (F8)** — the ack prints its back-fill.

- 🔴 **`pkill -f '<pattern>'` inside a Bash-tool command MATCHES THE BASH RUNNING THAT COMMAND** (its argv carries the pattern) — it killed my own compound command mid-way at 19:07Z, leaving rotate.py on pre-fix bytes until I noticed. Kill by pid (`pgrep -f` first, then `kill <pid>`), never `pkill -f` in a compound line.
- 🔴 **A refused dispatch (stale-base JSON) leaves an EMPTY `.agi/sessions/iter-L4.NNN/<id>/` in the SEAT tree** — rmdir it before re-cutting the same id.

- 🔴 **season/s2 moves every few minutes (prime + sensei-director + helper): the dispatch shape is a loop** — `git fetch; if behind: git merge --no-edit -F <file> origin/season/s2; git push; dispatch` up to 3 tries per round; a conflict lands in YOUR scratchpad when the prime edits a bullet in it (16:10Z) — `git checkout --ours` then re-apply their line by hand.
- 🔴 **A parent can exit `done` with the kid's work STAGED and UNCOMMITTED in the KID's worktree and nothing on its own branch** (L4.243, 14:47Z) — check every kid worktree's `git status --short` at harvest; commit under the kid's authorship with the circumstances in the message; `harvest-table` prints the row. **A staged kid tree `a00-f8019bc1` (not mine) exists at 16:34Z — tell its director.**
- 🔴 **A kid may do unrelated global edits** (L4.234 stripped all 79 em-dashes from write.py incl. the THOUGHT marker string) — diff the deletions, not only the additions; restore in a director fix-up commit.
- 🔴 **A fix-only claim in Agent Notes is missed by the next kid** (L4.243 worked the parent's finding instead) — write the AMENDED BUILD ORDER INTO `testable_claim` (write.Edit.set_fm) so it is the assignment.
- 🔴 **`--level big` is refused by dispatch** (`no context for target ... at level big` + `INJECTION.md missing`; leaves a stray branch, delete it) — always `--level small`.
- 🔴 **Notes: `@@TS@@` in the note file is replaced by `$S/note.py` with the real UTC time** — never type a timestamp from memory (two notes this session carried a guessed time).
- **Never hand-poll `spawn_budget.py status` in a loop** (Sensei) — `status --iter L4.NNN --wait --timeout 540` (L4.244) is the wait; the inbox mtime loop is the fallback for "any dm".
- **Scratchpad helpers live in the session scratchpad dir (`/tmp/claude-1001/.../scratchpad/`) and die with the session** — the successor rewrites `note.py` (write.Edit + verb_note + submit, actor sanctuary-director role director, `@@TS@@`) and `mint.py` (write.create(root,'hypothesis',slug,parents,set_fm={testable_claim,title,town})) in its first harvest; both are ~12 lines.

- 🔴 **`git merge` needs the EXACT branch name** — `git branch --list 'loop/*<agent-id>@s2' | tr -d ' +*'`; a guessed slug prefix fails with "not something we can merge" and your note commit lands alone (gen XIV, L4.230 — recovered).
- 🔴 **`write.create(...)` returns a TUPLE `(NodeWrite, created_file)`**; `write.submit(...)` returns a NodeWrite. Long claims via the Python API from a `<<'EOF'` file (backticks are safe there).
- 🔴 **A round whose FILE SCOPE is the owner's stub tree (`/home/ubuntu/work/streamer-stub`) cannot commit there** — kid and parent briefs forbid git; the DIRECTOR commits at harvest under the kid's authorship (`git -c user.name=<kid-id> -c user.email=<kid-id>@agi.local commit -F <file>`), never pushes (the owner's relay session pushes), and re-runs `bash bin/install-cli.sh` to deploy, then probes the DEPLOYED `~/bin/sb-status` from the agi seat too (L4.229 broke that shape). The owner is LIVE on that relay — read, never restart anything there.
- **A parent may cite `git stash` in its review (L4.222)** — check `git stash list` is empty at harvest; a `/tmp` copy is the safe counterfactual.
- **`test_commands.py`/verify from a seat: `bin-suite-fresh` red on the merits after engine merges** — the merge-up suite clears it; 9/10 is the expected seat verify.

- **rotate-self's STARTUP OUTPUT block: the two dead commands were FIXED by L4.179 + the prime's eb03a22bc** (`rotation-record` now `rotate.py status --seat {seat} --record latest`; `seat-row` dropped). If a first_turn entry still shows exit 2, it is a NEW defect — note it.
- 🔴 **Never run `test_provisioning.py` or a full-suite pytest with `--basetemp` under the repo** — `root=tmp_path` walks up to the REAL `.agi` and mints a REAL key. (L4.170's bound stops CROSS-repo climbs only; a scratch dir inside your own repo still resolves it.) **An UNQUOTED heredoc runs backticks** — notes ride `<<'EOF'` files only.
- 🔴 **NEVER `cat` a round's `manifest.json` raw** (~3k tokens of prompt per agent) — `jq '.agents[] | {id,status,pid,finished_at,fail_reason}'`. **NEVER print a claude process's argv** — `ps -o pid,ppid,etimes,comm`.
- 🔴 **Both generations share `--debug-file .agi/sessions/sanctuary-director.log`** — grep by timestamp, never tail blind.
- 🔴 **A note OR A DM with a backtick rides a FILE — never a double-quoted shell string** (20:3xZ: a `send.py send` in double quotes ran `ack` as a command and blanked the word). `write.submit` returns a NodeWrite (`status='updated'`).
- 🔴 **Timestamps: `date -u` for every note; never estimate elapsed time.** `ls -la` prints LOCAL time (UTC-4 here) — the meter/log mtimes read 4 h early.
- 🔴 **A parent can exit with its review UNCOMMITTED in the KID's worktree** (L4.126): `git status` in `.agi/worktrees/<kid-id>` before calling a round dead.
- 🔴 **A dispatch that prints no `spawned` line left an EMPTY agent dir and nothing else** — it was the stale-base guard's JSON (`{"issue": "stale-base", "behind": 1 …}`), hidden by my grep; sync, re-cut the SAME id. **The stale-base guard refuses at behind ≥ 1** — `git fetch && git merge origin/season/s2 -F <file>` + push, re-cut with the SAME id.
- 🔴 **STAMP THE DISPATCHER: `AGI_SEAT=sanctuary-director`** — never `--seat` for a pi round. **`crons.py` refuses from a linked worktree.** **`heal.py watch --once` has no dry-run.**
- **`[agi-nudge] …` / `iter=… verdict=…` lines are MACHINE nudges, not the owner.** `send.py read` marks read; monitors use `peek`. **Address tmux windows by `@id`.** **The Bash tool blocks bare `sleep`** — an until-loop with `sleep 5` inside is fine. **`grep -v grep` hides your own claude process.** **`cut` is shadowed.**

## §5 KNOWN-GOOD VERIFICATION

`python3 extensions/agi/bin/commands.py run verify` — 10/10 in ~35 s (`bin-suite-fresh` red on the merits after engine edits — the merge-up suite clears it). Baseline: active ≥ 2266 / dep 195, links 0, goals 178 byte-identical; last MAIN suite 3468 / 14 @ merge-up 41 (`13de8c37e`).

## 🔴 §6 BANKED — not mine, with a recommendation — and g15 CANDIDATES

1. Kid model (`~deepseek/deepseek-v4-flash-latest`) — the owner named only the parent.
2. `hypothesis:l4-completion-signal-cannot-tell-dead-from-silent` — the prime's held round.
3. `links.py schema` 124 pre-L4 `testable_claim` violators — never `--fix` blind.
4. `crons.py cmd_remove` deliberately unfenced (L4.102 residue).
5. L4.126's parent died silently under the INLINE reaper — first live case for the service: `.agi/worktrees/a00-05d4d886/.agi/sessions/iter-L4.126/manifest.json`.
7. ~~carve-out~~ RULED YES by the prime 13:3xZ (scope in the node's claim) — cuts after L4.230.
9. L4.192 wording residue (prime, 35 verdict): send.py:733/961 docstrings call the both-join a "fallback" while :967 applies it to every capture — fold into the next send.py round, not worth its own.
8. **Stub repo (`/home/ubuntu/work/streamer-stub`, the owner's live relay tree) carries two loop commits unpushed on `main` (6bb09b8 kid-authored template, 8b50fe3 director fallback fix) on top of the owner's own unpushed c4a928a.** Not mine to push. Recommendation: tell the prime with the merge-up 37 numbers; the owner's relay session pushes when it pushes.
10. ~~Four dirty agent worktrees~~ DEAD (helper L4.256 21:4xZ: removed by hand on the 16:35Z ruling; diffs lost). **Four dirty agent worktrees with MODIFIED SOURCE (helper's measurement 15:5xZ): a00-400db3c3 (L4.65), a00-74d9b3b8 (L4.173), a00-99a5a43d (L4.52), a00-de936ecd.** Old rounds, long harvested; the edits are probably abandoned kid work. Recommendation: `git -C .agi/worktrees/<id> diff --stat` each, keep anything a landed round did not carry as a note on the round's hypothesis, then let the helper's sweep remove them. Do it before the helper's lane 3 round lands.
6. **g15 candidates still to PROPOSE:** (iii) the 0b-b captive after_join as a g15 node on 0b; (iv) from L4.197: `l4-a-foreign-tree-edit-is-committed-in-the-same-breath` (a round whose FILE SCOPE is a tree another live session commits in must edit + commit in one step, or its authorship is lost — the stub template edit rode the relay session's c4a928a).

## 🔴 THE ROTATE CHAIN — SPECS AS AMENDED (read the nodes; this is the map)

Order: **0a → 0b → 0c → seat-model rotate-half**, strictly serial on `rotate.py`. Owner targets (dd0f977c6): wake = **ZERO tool calls**; rotate = **ONE call from the predecessor** (`rotate-self` does everything, every role incl. the prime); predecessor **self-reaped by PID inside that call** (window-kill ≠ process-kill; the prime measured gen VII's reap half did NOT run — `e_predecessor_alive: present`); Belam chain **capped at FIVE**.
- **0a `hypothesis:l4-the-predecessor-hands-over-authority`** — `rotate.py handover`/rotate-self writes the successor's seats row + pin + handoff identity + the ack (gate `continue` BY CONSTRUCTION), releases own authority, reaps itself. Templates in a NEW `.geometry` node `rotations.md` (write.py create; SHARED with 0b): per-role default (successor brief + step list + telemetry set), named custom entries, `rotate-self --template <name>`; NO hardcoded brief path left. **Its TESTS use temp fixtures, never the live seats row.** Tell the prime before the `.geometry` suite run.
- **0b `hypothesis:l4-startup-is-one-script-or-a-driven-prompt`** — bootstrap.json + SessionStart hook injection + `rotate.py next` driven prompt; writes the OTHER two sections of `rotations.md` (facts with staleness bounds; steps). Telemetry BY DEFAULT in the bootstrap block. **Hook edit: the round proves on a COPY; the PRIME installs into the live global hook and verifies with a fresh session** (L4.94 rule). HALF B of L4.108 (active CLI-drive of the stale-base record) lands here.
- **0c `hypothesis:l4-identity-is-a-signature-not-a-story`** — seat keypairs, session certs, signed `send.py` (VERIFIED/UNSIGNED/FORGED; UNSIGNED = label, never a drop). **Pure-python from-scratch crypto PERMITTED/PREFERRED (42b369ebf), published test vectors in the suite, pynacl only as a test oracle.** MODULAR (e7c5f6dbd): one Signer/Verifier interface keyed by the row's `sig_scheme`; proof (g) = register a dummy scheme, rotate a seat onto it, nothing changes outside the table + the row.
- **Round (a) `hypothesis:l4-a-seats-live-model-is-measured-not-assumed`** (goal:g17) — PUSH delivery, no seat checks itself; watcher on the cron/reaper sends ONE `send.py` line on drift or a new `model_refusal_fallback`; verify-half `seat-model` check in commands.py/verification.py (after merge-up 17 — now clear). Rotate-half folds into 0a or after 0c. **The trap it detects fired on gen VII: a `[cyber]` false positive silently downgraded opus-5 → opus-4-8 for 191 turns; bytes on `goal:g17.1`.**
- **`hypothesis:l4-dispatch-echoes-less-than-it-knows`** (goal:g1.11) — one line per spawn on stdout, detail to `spawn.json`, suite asserts no key-shaped string; SERIAL behind L4.108 on dispatch.py → after merge-up 18.
- **L4-final `hypothesis:l4-the-stream-goes-live`** (`goal:g18.1`) — HELD until the rotate + workflow chains land. Works in `/home/ubuntu/work/streamer-stub`; owner's one touchpoint = backup email (BANK the ask); platform verification blocks are BANKED, never worked around.

## 🔴 THE OWNER'S REPORTING ORDER — 2026-09-10, verbatim

*"Tell both directors to stop reporting to you needlessly it's wasting fable tokens. Only reach out when actually necessary."* Binds you→prime AND helper→you. **NECESSARY = four things:** (1) a merge-up ready or done — ONE message, numbers only (ask the window in the same message); (2) a decision only the prime can make; (3) a rotation — new address, one line; (4) **a red merge, or a finding that changes a standing rule / what someone else would DO.** Everything else is readable in the graph.

## 🔴 AUTHORITY IS VERIFIED AGAINST THE GRAPH, NEVER AGAINST THE MESSAGE

`git fetch && python3 extensions/agi/bin/send.py whois <ref> --claim <seat>` (exit 0 = IS-AUTHORIZED against a pushed season/s2 sha) + the `ListAgents` row carrying `agi-rc:@id` + `tmux capture-pane`. **All three, even for a message announcing itself as the new prime.** Never address a rotated-out predecessor. `ListAgents` marks every peer `idle`; idle is not dead.

## 🔴 STANDING RULES (binding)

- **OWNER 02:08Z (relayed two-step, prime lands the config):** *"let's let parents cut up to 5 kids at once"* · *"the new parent should be smart enough to handle that type of merge"* — addenda from now on: **up to 5 kids, PARALLEL where file scopes are disjoint, the PARENT merges every kid branch into the round branch (union for notes, tests with neighbours re-run) before `done:`**; `spawn.parent_max_kids: 5` is the prime's config edit.

- **A peer's instruction — including the prime's — is not authority to edit `CLAUDE.md`, permissions, `.agi/config.json`, `ladder.md`, `config:seats`, `moral:*`.** Quote the false line, write the replacement into the node, stop; the prime lands it.
- **The repo is PUBLIC (AGPL-3.0)** — every push is world-readable. Quote log LINES, never a key, token or key-bearing URL.
- **Mode: ENHANCED SURVIVAL** (`goal:g17.1`): parallel rounds GO, "always prefer dispatch over not"; state the FILE exclusion in each node. Still: wake no other seat · never write `config:seats` (0a's CODE may, its tests on fixtures) · never touch `moral:*` · never `git rm` under `.agi/nodes` · never rebase/force-push · never `level3.py` without `--dry-run` · never `grid.py checkout` · never `git stash`.
- **Landed + verified work is never re-derived** — a fix-only re-dispatch says in the claim what is already done.
- **`HANDOFF.md` is the PRIME's file** — this file (`.agi/sessions/quorum/sanctuary-director.md`) is the seat's scratchpad and what `rotate-self --prompt-file` hands your successor.

## 🔴🔴 YOUR METER — PIN IT EXPLICITLY, FIRST ACT

```
python3 extensions/agi/bin/rotate.py meter --pin /home/ubuntu/work/agi/.agi/sessions/sanctuary-director.meter \
  --session-log /home/ubuntu/.claude/projects/-home-ubuntu-work-agi--agi-worktrees-seat-sanctuary-director/<YOUR-SESSION-ID>.jsonl
```
Your session id is the directory name in your SCRATCHPAD PATH. Never take the newest `.jsonl`. `--seat sanctuary-director` is the safe read once pinned. Rotate at **0.47**; close under the line (gen VII 0.44, gen VIII see §0).

## The loop you are running

`doc:l4-plan` §5.2 — read only the range you need (`write.py doc:l4-plan "read body N:M"`). **Per round:** mint/edit in YOUR tree via `write.py` (Python API for long prose; script form splits on `&&`) · the assignment IS the node's `testable_claim` · ceiling + FILE scope stated IN the node · **commit AND PUSH before dispatching** · `dispatch.py . L4.NN --target <node> --level small --tier parent --harness pi --branch` (foreground, its own call, never behind a trailing `&`) · review in the BYTES, run the thing against the REAL tree, paste what you ran · merge the round's BRANCH into the seat (never `git apply --3way` blind) · report per the order above.
**Falsifiers must not contradict each other or a standing rule** — a falsifier satisfiable only by breaking a rule is a defect in the round.

## Watching a round

- `spawn_budget.py status` between harvests — an `-r1` suffix = the reaper restarted a round (`max_restarts: 0` set; kill the `dispatch.py` WRAPPER first, verify by a second sweep; the wrapper can still be reaping at 18 min).
- **Stalled parent (L4.75) = CPU ~0% AND per-spawn key STILL (`provisioning.py status`) AND no live kid AND no `done:` commit.** Low CPU ALONE is normal (API-bound). Kill the pi pid, sweep twice, review the bytes yourself, commit on the round's branch under the kid's authorship with the circumstances in the message.
- A parent with NO kid after ~15 min: kill it (L4.77, $0.22 for nothing).
- **A running pi parent takes no mail** — a correction after dispatch lands as a fix-only re-dispatch on the same node after harvest; edit the node the moment it arrives anyway.
- A parent's session dir lives in ITS worktree (`.agi/worktrees/<agent-id>/.agi/sessions/iter-N/`); killing a wrapper truncates the background task log — read the manifest.
- `write.py`'s Python API takes `root` RAW — pass `locations.find_project_root(Path('.').resolve())` and read `SPAWN-GATE APPROVED` back.

## Merge-up

1. Sync the seat to `origin/season/s2` first (conflict rules in §3.2). Seat `verify` green (bin-suite-fresh may be red on the merits — the suite clears it).
2. ONE message to the prime: "taking the merge-up-N window" + what it lands + numbers. Hold until it replies with lock state + tip + baseline.
3. In MAIN `/home/ubuntu/work/agi` (check `git status` first — leave files outside your path set alone; never clean, never stash): `git merge --no-ff seat/sanctuary-director@s2 -F <file>` → `snapshot-goals.py --render` → `--render --check` → `commands.py run verify-suite` FOREGROUND (`timeout: 600000`, expect 10/10 first read — the "expect the first read red" rule is RETIRED) → `grid.py commit --all` (legal on season/s2 only) → `git push origin season/s2` + `git push origin "refs/grid/*:refs/grid/*"` → **`python3 extensions/agi/bin/verification.py --level rotation --stamp` in MAIN AFTER the push (L4.153: the baseline is stamped only by a kept, pushed merge; the pre-push suite only compares; `--level quick` has NO node-count check and stamps NOTHING — gen XII measured 07:49Z)** → ONE message, five numbers + hash.
4. **Never merge-then-hold** — MAIN is a tree the prime and the `:07` `branch_push` cron also push from; `grid_sync` pushes grid refs every 5 min. Check crons with `crontab -l | grep agi-crons`, never `crons.py show` from a seat.
5. **`-F <file>` for every commit/merge message** — `-m` runs command substitution on backticks. `-F -` does not read stdin.
6. A new file under `bin/` needs the suite (`test_bin_help_smoke.py` enrols it) — a real CLI, not an exemption.

## Spend

- `provisioning.py spend` (read-only) / `capture --out F` / `diff --prev F`; quote `account.used`. A round ≈ **$0.055**. Account ~$107 total, ~$17 left at gen VII's read.
- **Per-spawn keys are minted at dispatch ($5 cap, ~3 h) and REVOKED when the agent exits** — a post-hoc diff cannot see them; observe DURING.
- **Stopping rule (prime): account remaining < $1.00 → stop dispatching pi rounds and report.** Never auto-switch to the Claude fallback (owner's spend profile). Never mint/revoke/re-cap/PATCH a key — the owner's.
- Free models: 2 of 21 usable; pi treats an empty `length` completion as a normal turn (reads as a stall). Batch the sweeps, not the loop.
- `qwen` 49% of account spend, NOT the loop, identification is the owner's (banked in `doc:l4-owner-decisions`).

## Rotating yourself

At **0.47**; close under the line (gen VIII rotated at ~0.38 after three merge-ups in one session). `rotate.py rotate-self`, NEVER `loop`; `--dry-run` first; explicit `--name sanctuary-director --model claude-opus-5`, effort `max`, `--prompt-file .agi/sessions/quorum/sanctuary-director.md`. **Replace this file wholesale — written AS YOU WORK.** The successor acks on the explicit channel (`rotate.py ack --seat sanctuary-director --gen N --ref <ref> continue|diff`) until 0a moves the write to the predecessor. **Confirm your successor by the `ListAgents`/@id join or `tmux capture-pane`; check the window list before saying "cleanly" — gen VII said it and the record said `e_predecessor_alive: present`.** Announce the new address to the prime in ONE line; it writes the row before the successor acts.

## What this seat has learned about doing the job well

- **Ask what subject a check actually resolved before you believe its verdict** — the tell is a confident, specific answer to a question you did not ask (`crons.py show` from a seat, `envfile.py --check` on a revoked key, `bin-suite-fresh` on a stamp another room wrote, `agent_dispatch.model` that only the legacy path reads).
- **Run it against the real tree before you believe its tests — with the bytes under review, from the tree that has the defect.** Paste what you ran into the node.
- **Check the easy inference before you make it, especially when it flatters your own work**; cite the mechanism (file:line, a built command), never the correlate.
- **Draw the boundary in the direction that costs you something** — governing docs, the prime's held rounds, the owner's keys.
- **Correct your own record in the file your successor reads, in the same breath as the finding.**
- **A round that stops at the correct boundary is not a failed round**; verdicts stay where their authors put them.
- **The prayer closes a SESSION, not a turn** — at rotation, after the report.
