# POST HANDOFF — master-sensei: LIVE SCRATCHPAD (session 2026-09-13 10:46Z →, replaced wholesale by each rotation; owner quotes live in `doc:l4-owner-decisions`, never here)

## §0 WHO YOU ARE (supplied, never claimed)
Post `master-sensei`, role director, tier 1, claude-opus-5 high, tmux `agi-rc` window `master-sensei`, **MAIN checkout `/home/ubuntu/work/agi` on `season2/main` (renamed by Prime XVI 17:46Z; `origin/season/s2` is STALE — never push to it; `git push origin season2/main`), no worktree** (config/prose you commit propagates to every post's next rotation). Transcript: `~/.claude/projects/-home-ubuntu-work-agi/<session-id>.jsonl`. Row `session_ref` is back-filled by your ack. Vocabulary (owner 22:1xZ): **post**, not seat; towns share Keepers + Masters, each town its own Council.

## §0.5 ROUTING
```
owner (in your pane) ──── answer directly
                │
master-sensei ──┼── template/facts: apply yourself · prose: one dm to the live post to self-edit  (the Sensei keeps NO director — owner 08:1xZ 2026-09-13)
                │                 RENAME ROUND pending (belam XIX 08:1xZ): point sanctuary-director → point-director, then sensei-director → sanctuary-director, each at that post's next boundary; surfaces in drafts/rename-round-surfaces.md
                ├── EVERY task that is not template/config/role-doc (code, CLI-verb/MCP candidates, plans) ──► sanctuary-master (owner 22:3xZ via belam XVIII; SM plans, assigns to sensei-director, reviews by name)
                └── rule-changing lines only ──► belam (send.py send belam "…"); owner's explicit order overrides
```
Never dispatch, harvest, merge, kill, panic, `git rm`, force-push, rebase, `git add -A`, write in another post's worktree, or `grid.py commit --all`. **No AskUserQuestion — the pane has no interactive user** (Prime had to answer one by `tmux send-keys` 12:5xZ).

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

## §5 STATE + NEXT (2026-09-14 01:5xZ — PAUSED by owner order)
**⏸ OWNER ORDER 01:38Z (via the Prime, relayed by SM 01:47Z): once live rounds land, ALL masters + directors PAUSE except thought-master + his director — no mints, no dispatch, no audits, no template applies; answer only the owner or the Prime.** On a `[rotation-alert]` during the pause: one `send.py read`, record nothing, no draft, no dm. On a line from the owner or the Prime: act. Resume audits only when the Prime lifts the pause.

**Floor board (wake / out, latest per post; all bare keyed `rotate` now):** director-point (sanctuary-director) 5 / 6 (01:04Z; timing right 3× in a row after three EARLY rotations 16:20-17:09Z caused by the facts byte-cap bug, root-caused + fixed 728698e23) · director-sanctuary (sensei-director) 4 / 7 (01:34Z; wake = ListAgents + whole owner-decisions doc Read) · director-review (sanctuary-helper) 0 / 10 (00:49Z; first bare rotate) · sanctuary-master 0 / 2 (00:45Z first rotation; card switched to bare rotate 3800ad354) · stream-master – / 11 (19:13Z; rotate refused "unkeyed" with a WRONG grammar in the refusal, 3 keygen tries → SM) · belam XIX→XX 0 / 2 (rotate-self still 4 flags incl. --force) · thought-master first seating 00:55Z wake 1 = the owner's order exactly.

**This session landed:** F24 (write.py grammar) F25 (never peek before read) F26 (card path; HANDOFF.md is the engine's) F27 (meter: only f vs 0.47); **facts region compacted 15 KB → 7.2 KB, newest-first, range 37:64** — the 8000-byte cap had cut every director wake's facts at F13 for ~20 h (root cause of the three early rotations); **guard test** `test_live_facts_region_fits_under_every_template_byte_cap_with_headroom` (Prime rule: over-cap = delivery failure); test_sensei_wake_audit fixed (label derived, not pinned); gen-less pass 1 (b7ea2ed71); branch `season2/sensei/genless-templates` @8bb2fff6d (sensei-wake drop, rename lines, brief rename) — NOT picked at SL2#31: waits SM.24b then the next window (SM 01:47Z); AUTHORITY line in 5 cards + brief; FIGURE-EIGHT §0.6 in 6 cards + prime brief (via write.py); **thought-master card drafted** (SM §1.5 charter landed 45553a0b1; owner first-action order bb891e3c6; seated 00:55Z). Routed to SM: SM.20 (harvest stamps the card), SM.22 (dispatch refuses above the line; spawn_budget --wait), SM.14 (hook wording — landed as "of 0.470 window"), refusal string rotate.py:15462 + key-at-seating, TRUNCATED last line for capped entries, remote-control label still `-g31`.

🔴 **NEXT (successor):** wake = NOTHING. PAUSED (above) until the Prime lifts it. After the lift: (i) apply the genless branch when SM names the window (b then d; d after SM.18 apply); (ii) template line: AUTHORITY → "read the doc tail by range (`write.py doc:l4-owner-decisions 'read body N:M'`), never the whole node" (director-sanctuary paid a 767-line Read); (iii) re-measure director-point wake (5 orient) + peek regression; (iv) verify SM's next out is bare `rotate`. Before every MAIN commit: suite lock absent.
## §6 BANKED
- Drafts under `.agi/sessions/sensei/drafts/` are tracked; commit by exact path.
- Own slip this session: backticks inside a double-quoted `send.py send "…"` get shell-expanded — single-quote the line (F4).

## 🔴 Where it stops
```
2026-09-14 01:5xZ: PAUSED by owner order 01:38Z (all masters + directors except thought-master + director); 14 audits this session, facts byte-cap root cause fixed, thought-master card live and seated. Successor: read-only on alerts until the Prime lifts the pause; then genless branch + AUTHORITY tail-by-range line.
```
