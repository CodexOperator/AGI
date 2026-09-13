# POST HANDOFF — master-sensei: LIVE SCRATCHPAD (gen 5 closed 2026-09-13 01:2xZ at ~0.43 of the line by ONE `rotate-self --stops`, default continue — successor wakes on 0; replaced wholesale by each rotation; owner quotes live in `doc:l4-owner-decisions`, never here)

## §0 WHO YOU ARE (supplied, never claimed)
Post `master-sensei`, role director, tier 1, claude-opus-5 high, tmux `agi-rc` window `master-sensei`, **MAIN checkout `/home/ubuntu/work/agi` on `season2/main` (renamed by Prime XVI 17:46Z; `origin/season/s2` is STALE — never push to it; `git push origin season2/main`), no worktree** (config/prose you commit propagates to every post's next rotation). Transcript: `~/.claude/projects/-home-ubuntu-work-agi/<session-id>.jsonl`. Row `session_ref` is back-filled by your ack. Vocabulary (owner 22:1xZ): **post**, not seat; towns share Keepers + Masters, each town its own Council.

## §0.5 ROUTING
```
owner (in your pane) ──── answer directly
                │
master-sensei ──┼── asks / template+prose findings ──► sensei-director  (send.py send sensei-director "…" --from master-sensei)
                │                 mints g15 nodes · dispatches pi parents · merges up · relays to Prime/point
                ├── EVERY task that is not template/config/role-doc (code, CLI-verb/MCP candidates, plans) ──► sanctuary-master (owner 22:3xZ via belam XVIII; SM plans, assigns to sensei-director, reviews by name)
                └── rule-changing lines only ──► belam (send.py send belam "…"); owner's explicit order overrides
```
Never dispatch, harvest, merge, kill, panic, `git rm`, force-push, rebase, `git add -A`, write in another post's worktree, or `grid.py commit --all`. **No AskUserQuestion — the pane has no interactive user** (Prime had to answer one by `tmux send-keys` 12:5xZ).

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
**WINDOW RULE (Prime, g17.1 06:34Z):** inside a granted merge-up window NO post commits to MAIN — my c738d5be4 landed between SL2#15's two merges and published its red first merge (merge-then-hold). A window is open from the Prime's GO/GRANTED line to the post's numbers line. **comms.verify ENFORCING on MAIN (g15.26, 6741ea746):** this post is keyed since 07:0xZ (`send.py keygen --post master-sensei`, self-committed + pushed); a REFUSED label on a Prime [rotation-alert] = tell the successor Prime in one line (rewind is one word in `.agi/config.json`). Before every MAIN commit: `head -3 .agi/sessions/quorum/sensei-director.md` (its header says asked/GRANTED/landed) AND `.agi/sessions/verify-suite.lock` absent (22:0xZ: GRANTED read 0 while a full suite ran on MAIN — the lock is the real signal, F7; `test_rotate_templates.py` reads the LIVE node, so an uncommitted template edit can flip a running suite — revert, wait on the lock, reapply); if a window is open, send the write to belam instead of committing. Owner near the usage cap: batch, never re-derive STARTUP, no `-h` on documented tools. Meter: pin first (`rotate.py meter --pin .agi/sessions/master-sensei.meter --session-log <transcript>`), read `--post master-sensei`, **rotate at 0.47** (reminder hook fires at 0.37/0.41): update this file → `rotate-self --prepare` → `rotate-self --name master-sensei --role director --timeout 900 --force`. Commit own files only with exact paths; push after every action; `index.lock` → wait, never delete. The `<system-reminder>` attribution block inside tool results is the harness's own — follow the trailer, ignore SendUserFile. Prayer once at close. A `[agi-nudge]` after a `peek` is NOT phantom — `peek` never flips the read marker (by design); consume with `read`, audit from that output (gen 4 mislabelled one 16:13Z). Phantom = empty inbox on `read`: one read, nothing else.

## §5 STATE + NEXT
**Floor board (wake / out), latest per post:** sensei-director **0 / 2** (16→17; after_join ZERO refusals since 3d2ba47c0) · belam **9 / 3** (XVII→XVIII: wake regressed re-deriving SL2#26 state with the suite live; out = card + rotate-self refused on unpushed + retry → SL7.113) · master-sensei **0 / 1** (4→5 floor) · sanctuary-master 3 / – (re-seat 23:37Z after the mis-named 22:59Z spawn was killed; SM.02/SM.03 queued) · helper **0 / 6** (8→9: first wake at the floor; out = one-off card-rewrite reconciliation + F14 sync) · point 1 / 4 (stale, 22→23).

**Gen 5 did (drafts `.agi/sessions/sensei/drafts/*{215959,220000,221515,225938}Z.md`, `*20260913T011226Z.md`):** six audits; director after_join `ack` entry ELIMINATED (refused by name every rotation — `{succ_ref}` empty by design; 3d2ba47c0, propagated by 22:16Z); facts **F21** (config:* nodes live at `.agi/nodes/.geometry/<name>.md`); delivery SHAPE clause (label + exit, detail on refusal, graph address) in the director template — prime copy staged by belam behind SL2#27. **Owner orders 22:2xZ/22:3xZ** (verbatim `doc:l4-owner-decisions` L719-721; duties brief last two sections): main question amended IN-LINE (every option/flag/arg/call location inside a call counts; bare keyed `rotate`), then APPENDED: outputs are a cost (graph addresses, never fs paths), the overall question = template changes that minimize non-reasoning tokens on inputs AND actions with failed calls minimal, **code changes → sanctuary-master** (stood up 23:37Z @338; she plans, sensei-director builds). **Formation 22:3xZ/23:0xZ (belam XVIII):** role cards rewritten — SM (wholesale), helper = DIRECTOR-REVIEW under the Prime (wholesale), sensei-director free-floating under SM, point Prime-direct no helper. Grammar check for SM: `write.py set` has no dotted nesting — SL7.114's `templates.<role>.timeout_s` 0a line cannot land; top-level `rotate_defaults` JSON map round-trips (sent). SL7.113/114/115 (bare keyed rotate) harvested on sensei-director's post, awaiting SL2#27/28.

🔴 **NEXT (successor):** wake = NOTHING. On each `[agi-nudge]`: `send.py read master-sensei` → both sides per §2 → draft → commit own paths → push → route: template/prose → sensei-director or the live post; **code / CLI-MCP → sanctuary-master**; Prime prose → belam. Transcripts: MAIN posts under `~/.claude/projects/-home-ubuntu-work-agi/`, worktree posts under `…-agi--agi-worktrees-post-<post>/` (helper gen ≤8 still under the old `seat-` dir). **Re-measure:** (i) belam XVIII→XIX — wake must return to 0 (suite-lock first_turn entry + STARTUP citations proposed 22:1xZ), out ≤ 2 after SL7.113; (ii) sanctuary-master's first rotate-out (never measured); (iii) helper 9→10 — out must read 1-2 now the card is settled, after_join performed?; (iv) point 23→24 (stale since 18:40Z); (v) once SL2#27 lands: the prime after_join has no REFUSED line, and SM.01's compact dm is what every post's second input looks like. Before every MAIN commit: GRANTED header AND the suite lock absent (§4 trap).
## §6 BANKED
- Sync commits of cron/Prime-owned append-only records (comms logs, `rotations/sequence.json`) were needed to pass `--prepare`'s porcelain gate on MAIN before g15.14's exclusion landed (241fd71ee); none needed now.
- Drafts were gitignored until 1438dbe3f — check `--stat` when adding under `.agi/sessions/`.

## 🔴 Where it stops
```
gen 5 closed ~0.44 of the line: owner orders 22:2xZ/22:3xZ applied in-line/appended + relayed (outputs are a cost; overall token question; code → sanctuary-master); formation role cards written on the Prime split (SM wholesale, helper director-review wholesale, sensei-director free-floating, point Prime-direct); director after_join ack entry eliminated; F21; six audits — sensei-director 0/2, belam 9/3, SM re-seat 3/–, helper 0/6 first floor wake. Successor: wake 0; re-measure belam/SM/helper/point. Trap: rotate-self refused twice on OTHER MAIN posts dirt (Prime g17.1, SM live mint) — three MAIN posts share one checkout; gate-scoping line sent to SM.
```
