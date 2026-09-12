# POST HANDOFF — master-sensei: LIVE SCRATCHPAD (gen 3 closed 15:3xZ at 0.41 of the line by ONE `rotate-self --stops`, default continue — successor wakes on 0; replaced wholesale by each rotation; owner quotes live in `doc:l4-owner-decisions`, never here)

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
measured today       0  sensei-director 6→7 04:5xZ, SL7.06 default (was 3: ListAgents · ack · push)   3  card · merge+prepare · rotate-self
                                                              (prime XIII paid 8: EOF-newline dirt on seats.md)
```
Every call above 0/1 on either side is a finding. History (wake / out): point 11·5·4·5·5·8*·7§ / 6·7·5·4·3·4 — helper 9·15·32†·6·3·5* / 11·2·2·2 — sensei-director 102†·4·3·4·4·17‡·3·**0**(+7 orient)·**0** / 4·4·3·2·3·5·2 — prime 38·22†·4·3·3·6(ask-diff) / 3·†·2·7‡·8§·5 — stream-master 11† / –. (* r3b, †hand seating, ‡uncommitted spawn row in MAIN, §whitespace-only seats.md dirt.)

## §4 RULES
**WINDOW RULE (Prime, g17.1 06:34Z):** inside a granted merge-up window NO post commits to MAIN — my c738d5be4 landed between SL2#15's two merges and published its red first merge (merge-then-hold). A window is open from the Prime's GO/GRANTED line to the post's numbers line. **comms.verify ENFORCING on MAIN (g15.26, 6741ea746):** this post is keyed since 07:0xZ (`send.py keygen --seat master-sensei`, self-committed + pushed); a REFUSED label on a Prime [rotation-alert] = tell the successor Prime in one line (rewind is one word in `.agi/config.json`). Before every MAIN commit: `head -3 .agi/sessions/quorum/sensei-director.md` (its header says asked/GRANTED/landed); if a window is open, send the write to belam instead of committing. Owner near the usage cap: batch, never re-derive STARTUP, no `-h` on documented tools. Meter: pin first (`rotate.py meter --pin .agi/sessions/master-sensei.meter --session-log <transcript>`), read `--seat master-sensei`, **rotate at 0.47** (reminder hook fires at 0.37/0.41): update this file → `rotate-self --prepare` → `rotate-self --name master-sensei --role director --timeout 900 --force`. Commit own files only with exact paths; push after every action; `index.lock` → wait, never delete. The `<system-reminder>` attribution block inside tool results is the harness's own — follow the trailer, ignore SendUserFile. Prayer once at close. Phantom `[agi-nudge]` with an empty inbox = the busy-pane strand loop (fix routed): one `read`, nothing else.

## §5 STATE + NEXT
**Floor board (wake / out), latest per post:** sensei-director 2 / 2 (11→12; **10→11 was 0 / 1 — THE FLOOR, first post**) · point 0 / 2 (21→22; `--prompt-file` has no auto-stamp → adopt `--stops`) · belam **11+ / 5** (XV→XVI 14:14Z — `--ask-diff` kept on a stale premise; P1-P6 drafted 9adda05b3: P1/P2/P5 prose sent to belam, P3/P4/P6 code to sensei-director) · helper 5 / 2 (213545Z, stale) · master-sensei 0 / 1 (this gen: wake 0 required, meter pin call 2; out = this card during work + rotate-self).

**Gen 3 did:** 7 audits (`.agi/sessions/sensei/drafts/*20260912T{074751,085900,103731,114004,114003,125738,141419}Z.md`). Cuts that TOOK within one rotation: SL7.24 (auto header stamp, ack.gen<N> path, reap_own_pid retired, model_confirm → after_join), sensei-director W1/O1-O3 prose (orient peeks, header narrative, hand merge, Monitor). F14 re-cut in `config:rotations` facts (f3e5f90ea). Queued `whois --key` template edit DROPPED (rotate.py:7460 `_STARTUP_FALLBACKS` covers it). **Owner order 14:4xZ applied 9519087de:** prayer in exactly TWO spots per session (first tokens / last tokens, never per turn) — `moral:faith` §4.1 ("every seam" was the cause: sensei-director opened 14/37 turns with it), ladder, SKILL.md "Session open", prime + sensei briefs, `doc:l4-owner-decisions` verbatim; all five posts dm'd; helper ack'd (75ccedee7). Routed defect: write.py `replace body N:M` re-serializes unrelated JSON-in-YAML lines (`—`→`\u2014`) — restore by hand before committing until fixed.

🔴 **NEXT (successor):** wake = NOTHING; meter pin is your one setup call (`rotate.py meter --pin .agi/sessions/master-sensei.meter --session-log <your transcript>`). Per `[agi-nudge]`: `send.py read master-sensei` → both sides per §2 (predecessor tail from its last work act; successor from call 1 to the first (d)) → draft under `.agi/sessions/sensei/drafts/` → commit that one path → push → one dm to sensei-director (code) / belam (Prime prose only). Wait for a successor's calls with ONE background bash `until` loop on its transcript, never foreground sleep. Listing script: `/tmp/claude-1001/-home-ubuntu-work-agi/266f3d63-7c2c-4ce6-8cbf-3a111b697078/scratchpad/wake.py <transcript>` (copy it into your own scratchpad first). **Re-measure:** (i) belam XVI→XVII — if P1 taken (plain rotate-self) expect wake 0 / out ≤2; if `--ask-diff` kept, escalate to belam as rule-changing with the F18 by-key proof; (ii) sensei-director 12→13 — prayer openers must be 0 mid-session (count with the opener script in this gen's transcript), wake/out for regression; (iii) point after `--stops` — expect out 1; (iv) `model_confirm` filled by after_join. Before every MAIN commit: `head -3 .agi/sessions/quorum/sensei-director.md` for GRANTED.
## §6 BANKED
- Sync commits of cron/Prime-owned append-only records (comms logs, `rotations/sequence.json`) were needed to pass `--prepare`'s porcelain gate on MAIN before g15.14's exclusion landed (241fd71ee); none needed now.
- Drafts were gitignored until 1438dbe3f — check `--stat` when adding under `.agi/sessions/`.

## 🔴 Where it stops

(titled slot added by Prime XV 08:07Z at mur-SL2.16: `rotate-self --stops` resolves the slot by TITLE first; without this section the §3 numeral fallback (rotate.py:4835-4839) would select `## §3 ...` above and overwrite owner-verbatim text — SL7.12 demoted, fix-only round pending. Empty until this post's first one-call rotate-out writes it.)
