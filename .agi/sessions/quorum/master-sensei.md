# POST HANDOFF — master-sensei: LIVE SCRATCHPAD (gen 3 closed 15:3xZ at 0.41 of the line by ONE `rotate-self --stops`, default continue — successor wakes on 0; replaced wholesale by each rotation; owner quotes live in `doc:l4-owner-decisions`, never here)

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
**Floor board (wake / out), latest per post:** sensei-director **0 / 2** (16→17: out = card edit + rotate-self, after_join ZERO refusals post-3d2ba47c0; 13→14 was 0 / 1 floor) · belam **9 / 3** (XVII→XVIII: wake REGRESSED 0→9 re-deriving SL2#26 state with the suite live in MAIN; out 4→3 = card + rotate-self refused on unpushed + push/retry; XVI→XVII was 0 / 4) · point 1 / 4 (22→23: inbox read forced by the after_join nudge; card, GO-wait polls, stops file, hand merge at close) · master-sensei **0 / 1** (4→5: floor both sides; 3→4 was 1 / 1) · sanctuary-master **3 / –** (re-seat 23:37Z after the 22:59Z spawn came up mis-named `belam-S1-L4-XIX` and was killed — spawn without --name uses the belam numeral scheme for every post; the re-seat hunted the dm log for intake the dead session had already consumed; 1 / – on the killed seating) · helper STAYS as director-review under the Prime (owner 23:0xZ; card rewritten, last 5 / 2 — next rotation should read 0 / 1).

**Gen 4 did (drafts `.agi/sessions/sensei/drafts/*20260912T{153222,160914,175150,175359,182422,183732}Z.md`):** owner in pane 15:4xZ–16:4xZ, four orders, all verbatim in `doc:l4-owner-decisions`: (1) stale `--seat` → `--post` in both templates (848fa20fd); (2) per-spawn setup belongs to rotation for every role — meter pin IS spawn-written (F8), card fixed; (3) the context meter prints automatically before each turn — hook half LIVE (`[meter] post=… line=…` every prompt since ~16:40Z), template half = `meter` telemetry key in both role templates (4bad592ec, fb9e86652; resolver routed); (4) close-out bundled under one rotate command, captive/fill-in form → relayed to belam; sanctuary round SL7.84 `l4-rotate-self-closeout-is-one-call…` in flight. **after_join went live 16:09Z** (never performed before: 86/91 records lacked it); measured defects routed and mostly fixed the same day: ack `--gen 0` (SL7.87), reap-proof empty-pids dump → refusal by name, 37-min-late / pre-join performs → `performed_by: tail` at 20 s post-join, 4× re-fire per rotation, old 12:09Z performer still emitting at 18:37Z (restart asked), second input as nudge → typed body (SL7.93 queued). Stale spawn-ack refuses the next rotate-out (belam paid 2; `sanctuary-helper.ack.json` + `stream-master.ack.json` queued to hit it) — routed. Prayer two-spot order: sensei-director 12 had 7 openers after the order then 0; gens 13/14 clean (1 opener, 0 mid); closer missing on every post so far; point 22 had 0/2.

**Late gen 4 (19:0xZ–22:1xZ):** owner's NEW MAIN QUESTION per finished session — every call gets one verdict in strict order **eliminated > automated > consolidated**, template first, harness code only to make the next such change a template edit (verbatim `doc:l4-owner-decisions`; duties brief last section; relayed to belam, owner meets him there). Parent-role pass from demoted L4.327 (draft `parent-role-pass-L4.327-20260912T2157Z.md`): parent a00-6b41b0ad got a 75 KB sibling dump + the KID contract, brief has 0 words on bytes/probe/refute — four lines routed; **deeper pass banked**: read each kid's report vs its diff for the exact sentence each layer believed. sensei-director 15→16: 0/2, after_join fully green (`performed_by: watch`, once, no dumps).

🔴 **NEXT (successor):** apply the three-verdict pass to WHOLE sessions from now on (not only the two tails). wake = NOTHING (pin spawn-written; meter prints per prompt; inbox in STARTUP). On each `[agi-nudge]`: `send.py read master-sensei` (never `peek` — it does not flip the marker) → both sides per §2 → draft → commit that path → push (`origin season2/main`; `origin/season/s2` is STALE) → one dm sensei-director (code) / belam (Prime prose only) / the live post (its prose). Wait for a successor's calls with ONE background `until` on the record's `handover.join.transcript`. Listing tool: `python3 extensions/agi/bin/sensei.py calls <transcript>` (SL7.68, live) — no scratchpad copy. **Re-measure:** (i) belam XVII→XVIII — out must drop from 4 (stale-ack fix landed? window cleanup during work?); (ii) sensei-director 15→16 — out 1 again, closing prayer present?, pin gen intact (SL7.91); (iii) point 23→24 — out 1 after the prose dm, wake 0 once SL7.93 types the second input; (iv) helper — stale since 21:35Z yesterday, audit its next rotation whole; (v) every record: after_join performed ONCE, `performed_by: tail`, no old-performer dump. Before every MAIN commit: `head -3 .agi/sessions/quorum/sensei-director.md` for GRANTED.
## §6 BANKED
- Sync commits of cron/Prime-owned append-only records (comms logs, `rotations/sequence.json`) were needed to pass `--prepare`'s porcelain gate on MAIN before g15.14's exclusion landed (241fd71ee); none needed now.
- Drafts were gitignored until 1438dbe3f — check `--stat` when adding under `.agi/sessions/`.

## 🔴 Where it stops
```
gen 4 closed at 0.46 of the line: four owner orders applied/relayed (--seat→--post, spawn-time setup, meter print via hook+template, closeout bundle → Prime), after_join went live and was measured green by 18:49Z, six audits (sensei-director 0/1 floor twice, belam wake 0 first time), owner heuristic eliminate>automate>consolidate in the duties brief, parent-role pass from L4.327 routed. Successor: wake 0; three-verdict pass over whole sessions; re-measure belam/sensei-director/point/helper.
```
