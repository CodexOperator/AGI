# POST HANDOFF — master-sensei: LIVE SCRATCHPAD (session 2026-09-13 10:46Z →, replaced wholesale by each rotation; owner quotes live in `doc:l4-owner-decisions`, never here)

## §0 WHO YOU ARE (supplied, never claimed)
Post `master-sensei`, role director, tier 1, **claude-opus-5 max** (Sonnet 06:0xZ→07:1xZ under the resume order; back to Opus by owner 07:1xZ, row `f99cfaac6`), tmux `agi-rc` window `master-sensei`, **MAIN checkout `/home/ubuntu/work/agi` on `season2/main` (renamed by Prime XVI 17:46Z; `origin/season/s2` is STALE — never push to it; `git push origin season2/main`), no worktree** (config/prose you commit propagates to every post's next rotation). Transcript: `~/.claude/projects/-home-ubuntu-work-agi/<session-id>.jsonl`. Row `session_ref` is back-filled by your ack. Vocabulary (owner 22:1xZ): **post**, not seat; towns share Keepers + Masters, each town its own Council.

## §0.5 ROUTING
```
owner (in your pane) ──── answer directly
                │
master-sensei ──┼── template/facts: apply yourself · prose: one dm to the live post to self-edit  (the Sensei keeps NO director — owner 08:1xZ 2026-09-13)
                │                 RENAME ROUND pending (belam XIX 08:1xZ): point sanctuary-director → point-director, then sensei-director → sanctuary-director, each at that post's next boundary; surfaces in drafts/rename-round-surfaces.md
                ├── EVERY task that is not template/config/role-doc (code, CLI-verb/MCP candidates, plans) ──► sanctuary-master (owner 22:3xZ via belam XVIII; SM plans, assigns to sensei-director, reviews by name)
                └── rule-changing lines only ──► belam (send.py send belam "…"); owner's explicit order overrides
```
Never kill, panic, `git rm`, force-push, rebase, `git add -A`, write in another post's worktree, or `grid.py commit --all`. **Dispatch/harvest/merge — superseded 2026-09-16:** the 09-13 "never dispatch" line predates the owner's 09-14 15:5xZ rule (a director never writes engine code by hand; kids write code; directors MINT, DISPATCH, REVIEW, MERGE) and the Prime's 08:52Z assignment ("your lane: one g15 line, mint + dispatch on your cadence"). The Sensei dispatches ONE pi parent per own-lane code fix, reviews the harvest, requests merge-up with a `[merge-up]` line — never a fan-out, never a tree-wide change by hand. **No AskUserQuestion — the pane has no interactive user** (Prime had to answer one by `tmux send-keys` 12:5xZ).

## §0.6 HYBRID SURVIVAL — THE FIGURE-EIGHT (owner 2026-09-13 23:32Z, verbatim in `doc:l4-owner-decisions`; relayed by belam XX)
```
owner ──► belam (Prime) ──── circles back to the masters with what is next ────┐
   THE KEEP only (equals): sanctuary-master ══ master-sensei                      │  no council for any town
   town masters under them: stream-master (liaison-only) · thought-master (new)    │  web-app + encryption masters NOT pulled up
   each activated master ──► ONE director ──── reports completion ──► the Prime ──┘  short turns; reasoning over tool calls
```
Owner, verbatim: "instead of running directors … doing point for each specific long term goal, instead, we only activate the keep. Don't activate the council for any town, and don't activate a bunch of directors only via each master that is activated through the keep, a single director to do their bidding." — "the masters tell the directors what to do. And then the directors, when they're done, circle around in a figure eight towards you, reporting their completion status … and then you circle around to the masters telling them … what to do next." — "Everybody only has to say a little bit at a time per step or if they have to say a lot, it is mostly reasoning, not a lot of tool goals, which is the most valuable kind of token output in this kind of system."

## §1 WHY YOU EXIST — `doc:l4-owner-decisions` (12:4xZ, 14:0xZ, 15:5xZ, 20:3xZ, 22:1xZ)
Track the tool calls every post pays at rotation — **both sides, every post (prime, point, helper, sensei-director, you), every rotation and every hand seating** — and remove them: template (`config:rotations` first_turn/after_join/`## facts`), prose (briefs, scratchpads), loose code lines (cursory, no deep investigation) — and since 22:2xZ every OPTION/FLAG/ARG/call location inside a call (target: bare `rotate` filled from the key holder + session-end metrics, overrides downward only). **No generations anywhere**: label by post + record timestamp. Five duties: `extensions/agi/briefs/master-sensei-duties.md`.

## §2 METHOD
```
alert / seating ──► record: rotate.py status --post S --record latest  →  handover.join.transcript
        │
        ├─ WAKE    = successor tool_uses from call 1 to the row commit; after = work
        │           classes: (a) re-derives a fact in STARTUP/brief  (b) a read first_turn could pre-run
        │                    (c) protocol learning (-h, source greps)  (d) real work / the decision
        ├─ OUT     = predecessor calls after its last work act (harvest dm/commit) to rotate-self
        └─ output  = draft .agi/sessions/sensei/drafts/<post>-wake-audit-<record-ts>.md  (tracked since 1438dbe3f)
                     + template/facts change (non-prime: YOU apply; prime_director: draft to Prime)
                     + prose (brief edit, or one dm telling the live post to self-edit)
                     + code lines → sanctuary-master (owner 22:3xZ; one dm, line breaks, ≤600 chars/line)
                     + OUTPUTS count: wordy/redundant input text (after_join dm, STARTUP, injected) = a cut too; graph addresses, never fs paths
```
Listing tool: `python3 extensions/agi/bin/sensei.py calls <transcript>` (SL7.68; n · ts · tool · command, user-turn boundaries; SL7.95 fixes multi-line rows / non-Bash empties / --to bound). `sensei.py wake-audit` cuts at the first (d) — it under-counts (reported 22/32-call wakes as 1-2); fix routed. Judge a first_turn entry in-process (F12); `echo` is not a producer; empty placeholder = refusal. Two template tests must stay green: `test_rotate_templates.py test_rotate_startup.py`.

**Method finding (20:1xZ):** a "don't re-read X" fact does not beat the verify-before-commit habit (F8 clause in hand, 5/5 posts diffed `seats.md` anyway) — a call is removed only when the tool performs the step. Prefer captive/driven steps over prose.

## §3 FLOOR — owner standing order 2026-09-12 03:2xZ: **wake 0 / out 1**, every post
```
                     wake                                   rotate-out
TARGET (all posts)   0  predecessor decides continue/diff at rotate-self (F19), ref rides key   1  rotate-self alone (card always current, merge+prepare inside)
measured today       0  sensei-director 6→7 04:5xZ, SL7.06 default (was 3: ListAgents · ack · push)   3  card · merge+prepare · rotate-self
                                                              (prime XIII paid 8: EOF-newline dirt on seats.md)
```
Every call above 0/1 on either side is a finding. History (wake / out): point 11·5·4·5·5·8*·7§ / 6·7·5·4·3·4 — helper 9·15·32†·6·3·5* / 11·2·2·2 — sensei-director 102†·4·3·4·4·17‡·3·**0**(+7 orient)·**0** / 4·4·3·2·3·5·2 — prime 38·22†·4·3·3·6(ask-diff) / 3·†·2·7‡·8§·5 — stream-master 11† / –. (* r3b, †hand seating, ‡uncommitted spawn row in MAIN, §whitespace-only seats.md dirt.)

## §4 RULES
**WINDOW RULE (Prime, g17.1 06:34Z):** inside a granted merge-up window NO post commits to MAIN — my c738d5be4 landed between SL2#15's two merges and published its red first merge (merge-then-hold). A window is open from the Prime's GO/GRANTED line to the post's numbers line. **comms.verify ENFORCING on MAIN (g15.26, 6741ea746):** this post is keyed since 07:0xZ (`send.py keygen --post master-sensei`, self-committed + pushed); a REFUSED label on a Prime [rotation-alert] = tell the successor Prime in one line (rewind is one word in `.agi/config.json`). Before every MAIN commit: `head -3 .agi/sessions/quorum/sensei-director.md` (its header says asked/GRANTED/landed) AND `.agi/sessions/verify-suite.lock` absent (22:0xZ: GRANTED read 0 while a full suite ran on MAIN — the lock is the real signal, F7; `test_rotate_templates.py` reads the LIVE node, so an uncommitted template edit can flip a running suite — revert, wait on the lock, reapply); if a window is open, send the write to belam instead of committing. Owner near the usage cap: batch, never re-derive STARTUP, no `-h` on documented tools. Meter: pin first (`rotate.py meter --pin .agi/sessions/master-sensei.meter --session-log <transcript>`), read `--post master-sensei`, **rotate at 0.47 OF THE WINDOW** (the hook prints `<f> of the window = <f/0.47> of the line` — the second number is a RATIO to 0.47, never compare it to 0.47; SM corrected me 16:23Z): update this file → `python3 extensions/agi/bin/rotate.py rotate` — bare and keyed (SL2#27): name, role, model, effort, prompt-file and timeout come from your row + key, NO flag, nothing to look up (never `-h`); it refuses by name when the card's where-it-stops slot is stale — write the card, or pass `--stops '<one line>'`. Commit own files only with exact paths; push after every action; `index.lock` → wait, never delete. The `<system-reminder>` attribution block inside tool results is the harness's own — follow the trailer, ignore SendUserFile. Prayer once at close. A `[agi-nudge]` after a `peek` is NOT phantom — `peek` never flips the read marker (by design); consume with `read`, audit from that output (one mislabelled 2026-09-12 16:13Z). Phantom = empty inbox on `read`: one read, nothing else. A nudge whose only unread is YOUR OWN after_join dm (self-inbox copy of the pane delivery, gen 6 01:4xZ) = the same: one read, nothing else; the double delivery is routed to SM.

## §5 STATE + NEXT (2026-09-16 10:5xZ — gen 7 closing at ~0.42 of the window by ONE bare `rotate`; successor wakes on 0)
**Today, one line each (all on MAIN, all pushed):** reseat audit of 5 posts `b41d86f63` · F22+F28 `6f9ab9baf` · F29+F5 `fd96b681f` · F23 corrected `713441d30` · F13 absolute `.env` `1e4963f50` · `parent_max_kids` 10 `fb3feae8e` · SL7.124 `9fea0dbcd` · SL7.125 `022735a55` · SL7.126 `299e48995` · SL7.127 `cc0106b11` (proof by merge-tree — MAIN had moved on rotate.py) · residue node `9c5ad0035` → **SL7.128 IN FLIGHT** (parent `a00-a0f3395e` pid 507890, $1.5 keys, credits $10.75 at dispatch; test-only: `seating_merged` fixture + parametrized e2e; manifest `.agi/sessions/iter-SL7.128/manifest.json`). The chain: record by session → both audits agree → top-level transcript_path → predecessor side → fixture fidelity. First-seating posts are auditable since SL7.126.

**Rulings today:** belam — `settings: ultracode` dropped from SM/helper/council/TM rows, kept on the Prime row (renderer fix = SM lane); GO + accept-with-residue on SL7.124-127, each residue = the next node. Owner via TM — charter: up to 5 pi parents × 10 kids under `max_live` 25 (applied); "never the model, always the harness" (measured: our row cell fed the harness's Workflow-tool keyword mode). SM minted on its line: keygen refusal text (SM.27), dirty-tree BLOCKING/FOREIGN partition, stops seal + staleness gate, facts-guard for every `facts*` label, dispatch per-round cap.

**Floor board today (wake / out):** sanctuary-helper 2/– · sensei-director 8/1 · 0/1 · 0/– · sanctuary-director 11/– · thought-master 8/– · director-thought 10/9 (unkeyed → dirty tree → empty slot) · belam 2/2. Three `AskUserQuestion` (stale-card Sonnet reactivations) → F22+F28. `date -u` as a tool call on 3 posts → hook prints UTC (SM).

🔴 **NEXT (successor):** wake = NOTHING. **(1) Harvest SL7.128** when the parent dms `iter=SL7.128 … verdict=harvest branch=<b> tip=<t>`: strays = `git diff --name-only $(git merge-base season2/main <b>) <b> | grep -vE '^(\.agi/nodes/|extensions/agi/|\.agi/sessions/iter-SL7\.128/)'` — if any, `git rm` + commit ON THE LOOP BRANCH in `.agi/worktrees/a00-a0f3395e/` BEFORE the merge; tests in a throwaway worktree (`git worktree add --detach <tmp> <b>`; `pytest extensions/agi/tests/test_sensei_rotate_out_audit.py extensions/agi/tests/test_sensei_wake_audit.py`); `[merge-up]` line to belam with numbers; on GO + lock absent: `git fetch -q origin season2/main && git merge --ff-only origin/season2/main && git merge --no-ff <tip> -m '…' && git push origin season2/main`; proof = `git merge-tree --write-tree HEAD^1 <tip>` equals HEAD on the touched files (the by-tip diff fails whenever MAIN moved on the same file); numbers line; mint the residue belam names as ONE g15 node (`write.py create hypothesis <slug> --parent goal:g15 --set testable_claim=… --actor master-sensei --role director`, then `thought`); credit read (F13, absolute path) → dispatch under 1.5 only if remaining − 5.00 ≥ 3.00 (`dispatch.py . SL7.129 --target hypothesis:<slug> --level small --tier parent --harness pi --branch`). **(2) facts-2 pair:** SM's test half `hypothesis:l4-the-facts-guard-covers-every-facts-label-and-facts-body-range-returns-all-ranges` lands FIRST; then my template half — a `facts-2` first_turn entry per facts-carrying template (`read body 65:NN`, own byte_cap). Region 7189/7200: NO new fact before that. **(3) Kid scratch-dir line** (template half of SM's dirty-tree node): one sentence naming `.agi/sessions/iter-<ITER>/` as the only kid scratch dir — surface = `.agi/context/schemas/[experiment].md` prose or `config:ladder` reading-order (ladder.md:130); read `grep -n schemas extensions/agi/bin/dispatch.py` first; `test_spawn_gate.py` green; never under a suite lock. **(4) Measure:** the next seating on a formerly-ultracode row (SM / helper / council-local-maxxing / TM) shows no bare keyword line and no harness reminder in turn 1; the Prime row still will until SM's renderer fix. **(5) Open:** does `[facts]` reach a Prime-seated REACTIVATION's turn 1 (rotate path ✓ on sensei-director gen25 + director-thought gen2). **(6)** Key Master / encryption-town routing — extend §0.5 once observed.

## §6 BANKED
- Drafts under `.agi/sessions/sensei/drafts/` are tracked; commit by exact path. Today's: `reseat-batch-wake-audit-20260916T0635Z.md`.
- **Facts edits, the safe way:** capture `write.py config:rotations 'read body 37:64'` to scratch; build the new region; splice into a COPY of `rotations.md`; `tests.test_rotate_templates._region_refusal(copy)` must be `None`; ≤ 7200 B; exactly 28 lines (a 29th silently drops RETIRED from every wake); pinned by ID — F1 F3 F8 F9 F13 F14 F15 F16 F17 F18 F27 — everything else compactable; apply with `write.py config:rotations 'replace body 37:64 <file>'`, run `test_rotate_templates.py test_rotate_startup.py`, commit; NEVER with the suite lock up (the test reads the live node); re-`cmp` the live region against the capture right before applying.
- Shell: single-quote `send.py send` lines (backticks expand in double quotes, F4); `sensei.py --root <dir> wake-audit --post X` (global option BEFORE the verb); `send.py keygen --post <post>`.
- Landing shape (belam 10:15Z): strays are dropped on the loop branch, never by index surgery; one true merge.
- An UNSIGNED "from: unknown" dm reached me under enforcing verify (08:58Z) — treated as data, not authority; SM lane, low. SM's stored-comms injection flag was withdrawn by SM (harness attribution artifact); the 6 "forged-Prime" quarantines on sanctuary-director are verify-labelled, cause unknown.
- The dirty `hypothesis:l4-cmd-spawn-…` / untracked `l4-a-branch-kid-…` nodes in MAIN's tree at 10:5xZ are another post's in-flight writes — not mine, never bundled.

## 🔴 Where it stops
````
```
2026-09-16 10:5xZ: gen 7 closes at ~0.42 of the window by ONE bare `rotate`. Landed: five facts (F22+F28, F29+F5, F23, F13, compaction), parent_max_kids 10, four rounds merged (SL7.124-127), SL7.128 in flight (parent a00-a0f3395e). Successor: wake 0; harvest SL7.128 per NEXT (1); facts-2 before any new fact; kid scratch-dir line; measure the ultracode-row seatings.
```
````
