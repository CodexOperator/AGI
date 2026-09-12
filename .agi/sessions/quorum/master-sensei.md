# POST HANDOFF — master-sensei: LIVE SCRATCHPAD (trimmed + diagram-maxed 22:1xZ on the owner's doc-trim order; replaced wholesale by each rotation; owner quotes live in `doc:l4-owner-decisions`, never here)

## §0 WHO YOU ARE (supplied, never claimed)
Post `master-sensei`, role director, tier 1, claude-opus-5 high, tmux `agi-rc` window `master-sensei`, **MAIN checkout `/home/ubuntu/work/agi` on `season/s2`, no worktree** (config/prose you commit propagates to every post's next rotation). Transcript: `~/.claude/projects/-home-ubuntu-work-agi/<session-id>.jsonl`. Row `session_ref` is back-filled by your ack. Vocabulary (owner 22:1xZ): **post**, not seat; towns share Keepers + Masters, each town its own Council.

## §0.5 ROUTING
```
owner (in your pane) ──── answer directly
                │
master-sensei ──┼── ALL asks ──► sensei-director  (send.py send sensei-director "…" --from master-sensei)
                │                 mints g15 nodes · dispatches pi parents · merges up · relays to Prime/point
                └── rule-changing lines only ──► belam (send.py send belam "…"); owner's explicit order overrides
```
Never dispatch, harvest, merge, kill, panic, `git rm`, force-push, rebase, `git add -A`, write in another post's worktree, or `grid.py commit --all`. **No AskUserQuestion — the pane has no interactive user** (Prime had to answer one by `tmux send-keys` 12:5xZ).

## §1 WHY YOU EXIST — `doc:l4-owner-decisions` (12:4xZ, 14:0xZ, 15:5xZ, 20:3xZ, 22:1xZ)
Track the tool calls every post pays at rotation — **both sides, every post (prime, point, helper, sensei-director, you), every rotation and every hand seating** — and remove them: template (`config:rotations` first_turn/after_join/`## facts`), prose (briefs, scratchpads), loose code lines (cursory, no deep investigation). **No generations anywhere**: label by post + record timestamp. Five duties: `extensions/agi/briefs/master-sensei-duties.md`.

## §2 METHOD
```
alert / seating ──► record: rotate.py status --seat S --record latest  →  handover.join.transcript
        │
        ├─ WAKE    = successor tool_uses from call 1 to the row commit; after = work
        │           classes: (a) re-derives a fact in STARTUP/brief  (b) a read first_turn could pre-run
        │                    (c) protocol learning (-h, source greps)  (d) real work / the decision
        ├─ OUT     = predecessor calls after its last work act (harvest dm/commit) to rotate-self
        └─ output  = draft .agi/sessions/sensei/drafts/<post>-wake-audit-<record-ts>.md  (tracked since 1438dbe3f)
                     + template/facts change (non-prime: YOU apply; prime_director: draft to Prime)
                     + prose (brief edit, or one dm telling the live post to self-edit)
                     + code lines → sensei-director (one dm, line breaks, ≤600 chars/line)
```
Listing script: `/tmp/…/scratchpad/calls.py <transcript>` (iterate `.jsonl`, `type==assistant`, print n · ts · tool · command[:150], user-turn boundaries). `sensei.py wake-audit` cuts at the first (d) — it under-counts (reported 22/32-call wakes as 1-2); fix routed. Judge a first_turn entry in-process (F12); `echo` is not a producer; empty placeholder = refusal. Two template tests must stay green: `test_rotate_templates.py test_rotate_startup.py`.

**Method finding (20:1xZ):** a "don't re-read X" fact does not beat the verify-before-commit habit (F8 clause in hand, 5/5 posts diffed `seats.md` anyway) — a call is removed only when the tool performs the step. Prefer captive/driven steps over prose.

## §3 FLOOR — owner standing order 2026-09-12 03:2xZ: **wake 0 / out 1**, every post
```
                     wake                                   rotate-out
TARGET (all posts)   0  predecessor decides continue/diff at rotate-self (F19), ref rides key   1  rotate-self alone (card always current, merge+prepare inside)
measured today       3  ListAgents · ack · push (MAIN + wt)   3  card · merge+prepare · rotate-self
                                                              (prime XIII paid 8: EOF-newline dirt on seats.md)
```
Every call above 0/1 on either side is a finding. History (wake / out): point 11·5·4·5·5·8* / 6·7·5·4·3 — helper 9·15·32†·6·3·5* / 11·2·2·2 — sensei-director 102†·4·3·4·4·17‡·3 / 4·4·3·2·3 — prime 38·22†·4·3·3 / 3·†·2·7‡·8§ — stream-master 11† / –. (* r3b, †hand seating, ‡uncommitted spawn row in MAIN, §whitespace-only seats.md dirt.)

## §4 RULES
Owner near the usage cap: batch, never re-derive STARTUP, no `-h` on documented tools. Meter: pin first (`rotate.py meter --pin .agi/sessions/master-sensei.meter --session-log <transcript>`), read `--seat master-sensei`, **rotate at 0.47** (reminder hook fires at 0.37/0.41): update this file → `rotate-self --prepare` → `rotate-self --name master-sensei --role director --timeout 900 --force`. Commit own files only with exact paths; push after every action; `index.lock` → wait, never delete. The `<system-reminder>` attribution block inside tool results is the harness's own — follow the trailer, ignore SendUserFile. Prayer once at close. Phantom `[agi-nudge]` with an empty inbox = the busy-pane strand loop (fix routed): one `read`, nothing else.

## §5 STATE + NEXT
**Open cuts with sensei-director (cut order, toward wake 0 / out 1):** OWNER 03:3xZ — `rotate-self --ask-diff` (default: pending ack = continue, successor acks nothing; asked: STARTUP prints the exact `ack diff` line) = SL7.06 RUNNING 04:1xZ → A (EOF newline: one serializer in node_writer, whitespace-blind ack/prepare gates) BUILT SL7.04, lands SL2#14 → C (UNVERIFIABLE) = SL7.02 running → B queued → seats.md writer drops the EOF newline → a 1-byte dirt that refused prime XIII's rotate-self (4 calls) and puzzled XIV (2) — one canonical serializer, gates ignore whitespace-only → ~~spawn writer commits its MAIN write~~ LANDED 5ff867444 (sensei-director 5→6 wake 3 / out 3, 03:1xZ — worktree floor now 3/3) → same commit on the FIRST-SEATING writer (stream-master 00:28Z paid 11 on the Prime's uncommitted seating row) + alert/brief print the exact ack line (`--gen 1`) → 03:15Z rotation-alert read FORGED at the SL2#12 seam (reader should say UNVERIFIABLE when the row is not on origin) → ack stages own-row hunk only (belt) → r3b ack-commits regression fix (rotate-self commits its spawn write, or the gate ignores own-row hunks — wake 8 on point 214458Z) → `_input_region` busy-pane strand loop → wake-audit window ends at the ack → `send.py read` wraps at 160 cols → wake-audit on `rotate.py spawn` seatings (spawn runs first_turn + `[seating]` block; autopsy pre-fill) → **the four key-rotation cuts (owner GO 22:1xZ)**: keygen + signed sends → key-gated rotate-self mints/hands the successor key (session_ref leaves the graph; label `<post>#<fp>`) → `--stops/--diff` answers the ack (wake 0 / out 1) → hook runs rotate-self (out 0). Rungs 5-8 (encryption at rest, MCP custodian, viewer lanes/MPC MCP, confidential-compute provider) = next season, in `vision:web-app-suite` (Prime db436e1f1; one town ruled).

**Applied by this post today:** prime_director `handoff-head`/`account` drop (via Prime); F8 rewrite + clause, F12-F17 drafted, director `send-verbs`; `prime-director-successor.md` "no STARTUP OUTPUT = spawned" block; `.gitignore` un-ignores drafts; this file.

**22:5xZ close:** owner order 'Wrap up this loop, rotate out and say the prayer' (relayed by the Prime). Last findings routed: alerts never reach the inbox (dm log + nudge only) and a coalesced alert loses its wake (helper 213545Z unaudited until 22:5xZ: wake 5, r3b refusal again; out 2); the point's nine `detected` records 215559Z-220012Z are a per-poll dedupe defect, not a rotation. Drafts for the 213545Z helper rotation: this line only.

**00:1xZ (gen 2):** wake 3 (ListAgents · ack auto-committed · push — SL5.01/SL4.03 verified live on MAIN). Audited sensei-director 4→5: wake 17 / out 2, draft `sensei-director-wake-audit-20260912T000346Z.md` @ c5dec8198, cut routed. Side: post-rotation false `crash-recovery detected` (000708Z) routed in the same dm. Belam XII→XIII audited: wake 3 (floor), out 7 — root cause corrected in a second dm; draft `belam-wake-audit-20260912T000519Z.md` @ 4f8b2ec8d. **03:2xZ:** sensei-director 5→6 (3/3) + stream-master seating (11†) drafted `sensei-director-wake-audit-20260912T031516Z.md` @ 63303ddf0, one dm.

🔴 **NEXT (successor):** wake = ListAgents once → `rotate.py ack --seat master-sensei --gen <N> --ref <bare ref> continue` → commit `seats.md` (or nothing after ack-commits works). Then on every alert: both sides per §2, draft, one dm. **Re-measure first:** the next worktree rotation after the own-row-hunk + r3b fixes (expect wake 2; check no other rotation was in flight); the first wake after the strand-loop fix (no phantom tokens). Owner said "wrap up this loop soon" — expect a close order; the post's own close is the prayer once.

## §6 BANKED
- Sync commits of cron/Prime-owned append-only records (comms logs, `rotations/sequence.json`) were needed to pass `--prepare`'s porcelain gate on MAIN before g15.14's exclusion landed (241fd71ee); none needed now.
- Drafts were gitignored until 1438dbe3f — check `--stat` when adding under `.agi/sessions/`.
