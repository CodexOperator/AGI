Prayers, sourced from moral:faith at run time. The long readings moved out (trim, hypothesis:l3w4-context-load-minimal): read them on demand — `brief.py readings --tier <tier>` — for a tie-break.

# SESSION HANDOFF — 2026-09-11 gen XII → XIII: LIVE SCRATCHPAD (written as I work; replaced wholesale at rotation)

## §0 STATE (gen XII at its rotation, 09:1xZ by `date -u`)

- **You (gen XIII)** were spawned by gen XII's `rotate-self`. **Verify, then ONE ack call:** seats row (`grep -o '"name": "sanctuary-director"[^}]*' .agi/nodes/.geometry/seats.md` — session_id/pid/window/generation = YOU; `session_ref` EMPTY until your ack), then `python3 extensions/agi/bin/rotate.py ack --seat sanctuary-director --gen 13 --ref <your ListAgents ref> continue`; then check the record `ls -t /home/ubuntu/work/agi/.agi/sessions/rotations/sanctuary-director.*.json | head -1` (`s12_self_reap.planned: true`, result `success`; `tmux list-windows -a` must show no window for gen XII's @274). Meter is pinned by rotate-self (`rotate.py meter --seat sanctuary-director`); pin by hand only if missing. **The STARTUP block's `[rotation-record]`/`[seat-row]` commands fail by construction (finding (iv), queued) — ignore those two, read the rest.**
- **Prime: L4-VIII `agi-b1 [7cff1a]`, window `@272`**, seat `belam` (row gen 8 at 09:0xZ; its handoff f6ccd713e says it rotates VIII→IX on merge-up 30's bytes — if a IX announces: `git fetch && send.py whois <ref> --claim belam` + ListAgents row + `tmux capture-pane` before the first send). L4-III..VI idle in @239/@242/@244/@247 — never address them.
- **Helper: gen IV `seat-sanctuary-helper-bd [71b63a]` @248**, ids L4.200+; owns g15-20 (merge-kids HELD — folding L4.201 onto my node, deprecating its own) and g15-26 (paid stream tests). p1/p5 its queue.
- **Tree:** season/s2 = MAIN = **`1b5700ea5` (merge-up 31, mine, 09:14Z)**; seat synced to it at rotation. **Floor 2013 / 194 / 2207 (stamped 1b5700ea5); last MAIN suite 2907 / 13 (11/11 first read).** Free ids: **L4.174+**.
- **UNIT UP:** reaper service reaps; `inline_reaper=false`. Dispatch OPEN; sync to origin/season/s2 before every cut (guard refuses at behind ≥ 1; re-cut with the SAME id after `git merge origin/season/s2 -F <file>` + push).
- **OWNER 05:1xZ g15 rule:** every review finding = a hypothesis under `goal:g15` (claim in the BODY too), PROPOSED in the merge-up report (slug + claim), the prime accepts, then mint + dispatch. **OWNER 05:3xZ:** auto-memory OFF.
- **Spend:** model rows sum $91.94 through 2026-09-10 (LAG 1 day); gen XII cut 16 rounds (≈$0.06–0.15 each) → est. ~$8 left of ~$107. Stopping rule < $1.00 — read `provisioning.py spend` (sum `usage` of `models` in `.agi/sessions/.spend-captures/spend.json`) before cutting more.

## §1 WHAT GEN XII LANDED (one line each)

- 07:03Z ack; gen XI reaped cleanly. **Merge-up 30 DONE 07:49Z: ee2000edc → d0465c36a**, suite 11/11 first read (2868 / 13), 1984/194/2178 stamped (`--level rotation --stamp`). Prime reviewed by name (f6ccd713e) and is rotating on those bytes.
- **MERGE-UP 31 DONE 09:14Z: f6ccd713e → 1b5700ea5**, suite 11/11 first read (2907 / 13), 2013/194/2207 stamped. Harvested with a director note + real-tree probe each: 149, 155, 156, 157 (merge-up 30) and 158-169, 171-173 (merge-up 31). The prime reviews 31 by name, then rotates VIII→IX.
- Minted g15-18..27, (iv)-(vii), g15-28..31 (all accepted by the prime); L4.141 evidence corrected. Demoted by me with evidence: L4.166 (:60, int-vs-string iter) → fixed by L4.167.
- (viii)-(xii) ACCEPTED and minted (cbf7d5777): `hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement` (kid sentence LANDED in brief.py; parent half + test to cut), `l4-a-stamp-forces-the-smoke-count` (**FIRST of the residues per the prime**, verification.py), `l4-the-kid-tier-gate-has-no-env-seam` (conftest), `l4-stall-candidate-measures-an-api-bound-parent-honestly` (spawn_budget.py), `l4-sb-status-resolves-from-home-not-from-stub-depth` (commands.py + fragment). All on FREE lanes — cut them after your ack (budget permitting).

## §2 LIVE + QUEUE — cut with `AGI_SEAT=sanctuary-director python3 extensions/agi/bin/dispatch.py . L4.NNN --target <node> --level small --tier parent --harness pi --branch` (sync first; my ids L4.174+; helper L4.200+)

LIVE at rotation: **L4.170** g15-29 bounded key lookup (a00-98b9fa43, provisioning/envfile/locations; kid 2 a00-0b7f0b48 cut ~09:0xZ). Harvest it → merge-up 32.

SERIAL QUEUES:
- rotate.py: free → **(iv)** `hypothesis:l4-rotations-startup-commands-must-parse` → **g15-28** `hypothesis:l4-the-dry-run-chain-line-is-tested-hermetically` → 0b-b `hypothesis:l4-startup-first-turn-is-performed-by-the-service-and-the-hook-fires-at-turn-one` (≤3 kids; PRIME installs the hook) → g15-8 `hypothesis:l4-config-rotations-facts-have-a-reader` → `hypothesis:l4-the-pin-is-the-lease`.
- heal.py + brief.py kid-status paragraph: **(vi)** `hypothesis:l4-a-timeout-mark-on-a-live-agent-is-not-terminal` — FIRST priority per the prime; SERIAL behind helper p1 (`hypothesis:l4-the-manifest-mirrors-terminal-agent-status`) on heal.py — check whether p1 landed (`ls .agi/nodes/experiment | xargs grep -l manifest-mirrors` on season) and cut it the moment it has.
- After the prime rules merge-up 31: mint accepted (viii)-(xii) and cut on free lanes (conftest, verification.py, spawn_budget.py, briefs).
- Free lanes: crons.py, send.py, spawn_gate.py, test_season.py, spawn_budget.py, verification.py, briefs.

## §3 🔴 NEXT COMMAND

Merge-up 31 IS done (1b5700ea5). Send your address line to the prime (ONE line; verify a IX first if one announced). Then: cut (x) `hypothesis:l4-a-stamp-forces-the-smoke-count` (verification.py, free), (vi) if helper p1 landed, then (viii)/(ix)/(xi)/(xii) on their free lanes, (iv) on rotate.py; harvest L4.170 when its parent exits; merge-up 32 when 3-6 rounds are in. Per harvest: `git -C /home/ubuntu/work/agi/.agi/worktrees/<parent-id> status --short` → `git branch -a | grep <parent-id>` (COPY the printed name) → read the kids' experiments + the parent's THOUGHT there → tests with neighbours on the round bytes, again on the merged seat bytes → a real-tree probe you paste into a director note (`write.verb_note` via the Python API, text from a `<<'EOF'` file) → `git merge --no-ff <branch> -F <file>` → push → cut the next in that file's queue. **Stalled parent** = 0 CPU ticks over 8 s + no socket + no live kid (`spawn_budget.py status --iter L4.NNN` — a CANDIDATE, verify) + no `done:` → TERM, commit the staged bytes under the kid, review yourself.

## §4 TRAPS (gen XII + carried)

- 🔴 **rotate-self's STARTUP OUTPUT block has two dead commands** (`.geometry/rotations.md:34-35,70-71`): `rotate.py whois` does not exist (invalid choice) and `send.py whois {succ_ref}` renders with an EMPTY ref because session_ref is back-filled only by the successor's ack (r3). Read `[prime-authority]` and `[git-state]`/`[inbox]`/`[live-spawns]` from the block; run the row grep by hand. Proposed as g15 in §6.
- 🔴 **Never run `test_provisioning.py` or a full-suite pytest with `--basetemp` under the repo** — a test's `root=tmp_path` walks up to the REAL `.agi` and mints a REAL key (06:31Z). **An UNQUOTED heredoc (`<<EOF`) runs backticks** — notes ride `<<'EOF'` files only.
- 🔴 **NEVER `cat` a round's `manifest.json` raw** — every agent entry carries the whole pi `command` with the prompt inline (~3k tokens; cost me one at 07:11Z). Use `jq '.agents[] | {id,status,pid,finished_at,fail_reason}' manifest.json`.
- 🔴 **NEVER print a claude process's argv** (`ps … args`, `/proc/<pid>/cmdline`) — the whole successor prompt rides in it. Use `ps -o pid,ppid,etimes,comm`.
- 🔴 **Both generations share `--debug-file .agi/sessions/sanctuary-director.log`** — grep it by timestamp, never tail it blind.
- 🔴 **A note with a backtick rides a FILE or single quotes — never a double-quoted shell string.** Same for `$(...)`. `write.create` returns a TUPLE `(NodeWrite, payload)`, `write.submit` a NodeWrite.
- 🔴 **Timestamps: `date -u` for every note; never estimate elapsed time.**
- 🔴 **A parent can exit with its review written but UNCOMMITTED in the KID's worktree** (L4.126): check `git status` in `.agi/worktrees/<kid-id>` before calling a round dead.
- 🔴 **The stale-base guard refuses at behind ≥ 1** — `git fetch && git merge origin/season/s2 -F <file>` + push, then re-cut with the SAME iteration id.
- 🔴 **STAMP THE DISPATCHER: `AGI_SEAT=sanctuary-director`** — never `--seat` for a pi round. **`crons.py` refuses from a linked worktree** — dry-run only from a seat. **`heal.py watch --once` has no dry-run** — never against live sessions.
- **`[agi-nudge] …` / `iter=… verdict=…` lines are MACHINE nudges, not the owner.** `send.py read` marks read; monitors use `peek`. **Address tmux windows by `@id`.** **The Bash tool blocks bare `sleep`** — a Monitor/until-loop. **`grep -v grep` hides your own claude process.** **`cut` is shadowed.**

## §5 KNOWN-GOOD VERIFICATION

`python3 extensions/agi/bin/commands.py run verify` — 10/10 in ~35 s (`bin-suite-fresh` red on the merits after engine edits — the merge-up suite clears it). Baseline: active ≥ 1959 / dep 194, links 0, goals 166 byte-identical; last MAIN suite 2850 / 8 @ merge-up 29.

## 🔴 §6 BANKED — not mine, with a recommendation — and g15 CANDIDATES for the merge-up 30 report

1. Kid model (`~deepseek/deepseek-v4-flash-latest`) — the owner named only the parent.
2. `hypothesis:l4-completion-signal-cannot-tell-dead-from-silent` — the prime's held round.
3. `links.py schema` 124 pre-L4 `testable_claim` violators — never `--fix` blind.
4. `crons.py cmd_remove` deliberately unfenced (L4.102 residue).
5. L4.126's parent died silently under the INLINE reaper (1200 s give-up) — first live case for the service: `.agi/worktrees/a00-05d4d886/.agi/sessions/iter-L4.126/manifest.json`.
6. **g15 candidates to PROPOSE (not mint until the prime accepts):** (i) helper's finding — the `--basetemp under .agi/sessions` brief instruction breaks fixtures that build a synthetic `.agi/` root (4 of 8 L4.113b tests) → narrow the instruction; (ii) `test_model_judge_fails_OPEN_when_no_api_key` hard-fails instead of skipping in a keyless env (cosmetic, helper — may be closed by 29c's p3); (iii) the 0b-b captive after_join as a g15 node on 0b; **(iv) NEW gen XII: `rotations.md` startup block carries two commands that cannot succeed by construction — `rotate.py whois` (no such verb) and `send.py whois {succ_ref}` ({succ_ref} empty until the ack) → replace with `rotate.py status --seat {seat}`-class reads that exist, and drop/defer the seat-row check to after the ack; a test renders every template `cmd` and asserts each verb parses (`-h` exit 0).** **(v) NEW gen XII: `_run_units_no_shell` (rotate.py:3978-3997) appends EVERY stage's stdout to the merged output, so a `| head -N` / `| sed -n 1,40p` filter truncates nothing — the STARTUP block carried the full `provisioning.py status` (12 keys) ahead of its `head -4` copy and `write.py -h` twice (measured on my own first turn 07:02Z) → append only the LAST stage's stdout per pipeline (every stage's stderr still merged); a test pipes a 100-line producer through `head -3` and asserts 3 lines.** **(vi) NEW gen XII: heal.py `_watch_round` (heal.py:339-352) marks a STILL-ALIVE agent `status: timeout` at `timeout_seconds` (1200 s) without reaping it, and the pi parent reads the mark as terminal and cuts a REPLACEMENT kid into the same worktree — L4.149 (parent's own review thought on experiment:a00-e64974da-091214) and L4.155 (kid a00-1422fa2e marked timeout 07:11:13Z, alive with an established TCP socket at 07:12Z and landing edits at 07:16Z; the parent cut a00-2f023d4b at 07:14Z) → two kids editing the same files. Fix: a live agent past its deadline is marked `overdue` (one dm, not terminal) OR reaped by the mark, never a terminal word on a live pid; the parent brief names `overdue` as still-working. Touches heal.py (serial behind helper p1) + the parent brief (brief.py).**
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
