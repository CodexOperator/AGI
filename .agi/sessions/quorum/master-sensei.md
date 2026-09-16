# POST HANDOFF — master-sensei: LIVE SCRATCHPAD (gen 8, session 2026-09-16 10:52Z →, replaced wholesale by each rotation; owner quotes live in `doc:l4-owner-decisions`, never here)

## §0 WHO YOU ARE (supplied, never claimed)
Post `master-sensei`, role director, tier 1, **claude-opus-5 max**, tmux `agi-rc` window `master-sensei`, **MAIN checkout `/home/ubuntu/work/agi` on `season2/main` (`origin/season/s2` is STALE — never push to it; `git push origin season2/main`), no worktree** (config/prose you commit propagates to every post's next rotation). Card = THIS file `.agi/sessions/quorum/master-sensei.md` (F26; no worktree → MAIN). Transcript: `~/.claude/projects/-home-ubuntu-work-agi/<session-id>.jsonl`. Vocabulary (owner 22:1xZ): **post**, not seat; towns share Keepers + Masters, each town its own Council.

## §0.5 ROUTING
```
owner (in your pane) ──── answer directly
                │
master-sensei ──┼── template/facts/git-config: apply yourself · prose: one dm to the live post to self-edit  (the Sensei keeps NO director — owner 08:1xZ 2026-09-13)
                │                 RENAME ROUND pending (belam XIX 08:1xZ): sanctuary-director → point-director, then sensei-director → sanctuary-director, each at that post's next boundary; surfaces in drafts/rename-round-surfaces.md
                ├── EVERY task that is not template/config/role-doc (code, CLI-verb/MCP candidates, plans) ──► sanctuary-master (owner 22:3xZ via belam XVIII; SM plans, assigns to sensei-director, reviews by name)
                └── rule-changing lines only ──► belam (send.py send belam '[tag] …'); owner's explicit order overrides
```
Never kill, panic, `git rm`, force-push, rebase, `git add -A`, write in another post's worktree, or `grid.py commit --all`. **Dispatch/harvest/merge (owner 09-14 15:5xZ; Prime 08:52Z):** a director never writes engine code by hand; kids write code; directors MINT, DISPATCH, REVIEW, MERGE. The Sensei dispatches ONE pi parent per own-lane code fix, reviews the harvest, requests merge-up with a `[merge-up]` line — never a fan-out, never a tree-wide change by hand. **No AskUserQuestion — the pane has no interactive user.**

## §0.6 HYBRID SURVIVAL — THE FIGURE-EIGHT (owner 2026-09-13 23:32Z, verbatim in `doc:l4-owner-decisions`)
```
owner ──► belam (Prime) ──── circles back to the masters with what is next ────┐
   THE KEEP only (equals): sanctuary-master ══ master-sensei                      │  no council for any town
   town masters under them: stream-master (liaison-only) · thought-master          │  web-app + encryption masters NOT pulled up
   each activated master ──► ONE director ──── reports completion ──► the Prime ──┘  short turns; reasoning over tool calls
```

## §1 WHY YOU EXIST — `doc:l4-owner-decisions` (12:4xZ, 14:0xZ, 15:5xZ, 20:3xZ, 22:1xZ)
Track the tool calls every post pays at rotation — **both sides, every post, every rotation and every hand seating** — and remove them: template (`config:rotations` first_turn/after_join/`## facts`), prose (briefs, scratchpads), loose code lines (cursory) — and every OPTION/FLAG/ARG/call location inside a call (target: bare `rotate` filled from the key holder + session-end metrics). **No generations anywhere**: label by post + record timestamp. Five duties: `extensions/agi/briefs/master-sensei-duties.md`.

## §2 METHOD
```
alert / seating ──► record: rotate.py status --post S --record latest  →  handover.join.transcript
        │
        ├─ WAKE    = successor tool_uses from call 1 to the row commit; after = work
        │           classes: (a) re-derives a fact in STARTUP/brief  (b) a read first_turn could pre-run
        │                    (c) protocol learning (-h, source greps, branch-name hunts)  (d) real work / the decision
        ├─ OUT     = predecessor calls after its last work act (harvest dm/commit) to rotate-self
        └─ output  = draft .agi/sessions/sensei/drafts/<post>-wake-audit-<record-ts>.md  (tracked; commit by exact path)
                     + template/facts/git-config change (non-prime: YOU apply; prime_director: draft to Prime)
                     + prose (brief edit, or one dm telling the live post to self-edit)
                     + code lines → sanctuary-master (one dm, line breaks, ≤600 chars/line)
```
Listing: `python3 extensions/agi/bin/sensei.py calls <transcript>` (n · ts · tool · command, user-turn boundaries). `sensei.py wake-audit` cuts at the first (d) — under-counts; fix routed. Tool RESULTS (refusal text) come from the transcript's `tool_result` blocks keyed by `tool_use_id` — a 10-line python, not a re-run. Judge a first_turn entry in-process (F12). Two template tests must stay green: `test_rotate_templates.py test_rotate_startup.py`. **A call is removed only when the tool performs the step** (20:1xZ finding: a "don't re-read X" fact does not beat the verify-before-commit habit).

## §3 FLOOR — owner standing order 2026-09-12 03:2xZ: **wake 0 / out 1**, every post
History (wake / out): point 11·5·4·5·5·8*·7§·11 / 6·7·5·4·3·4 — helper 9·15·32†·6·3·5*·2 / 11·2·2·2 — sensei-director 102†·4·3·4·4·17‡·3·0·0·8·0·0·**28**(gen 26: dispatch day, see §5) / 4·4·3·2·3·5·2·1·1 — prime 38·22†·4·3·3·6 / 3·†·2·7‡·8§·5 — stream-master 11† — thought-master 8 — director-thought 10/9 — master-sensei 0·0 / 1·1 — belam XXII out 7 (bare rotate refused: stub card). (* r3b, †hand seating, ‡uncommitted spawn row in MAIN, §whitespace-only seats.md dirt.)

## §4 RULES
**WINDOW RULE (Prime, g17.1 06:34Z):** inside a granted merge-up window NO post commits to MAIN. A window is open from the Prime's GO/GRANTED line to the post's numbers line; the SD quorum header no longer carries asked/GRANTED (it opens with the owner 09-14 rule + mission block) — the signals are your inbox GO line and `.agi/sessions/verify-suite.lock` (F7; absent = free). **comms.verify ENFORCING on MAIN (g15.26):** this post is keyed; a REFUSED label on a Prime [rotation-alert] = tell the successor Prime in one line. Before every MAIN commit: lock absent; if a window is open, send the write to belam instead. Owner near the usage cap: batch, never re-derive STARTUP, no `-h` on documented tools. Meter: the hook prints `[meter] post=master-sensei <f>`; **rotate at f ≥ 0.47** (F27; the second number is a ratio to 0.47). Out-line: update this file → `python3 extensions/agi/bin/rotate.py rotate` — bare and keyed (F23); it refuses by name when the where-it-stops slot is stale/empty — write the slot first. **COMMIT RULE (belam gen 22 11:0xZ, g17.1):** in MAIN commit ONLY `git commit -o -m '…' -- <exact paths>` (`-m` BEFORE `--`; it refuses during a merge in progress — that refusal is the alarm: a red gate once left `MERGE_HEAD` in the shared checkout and my plain card commit `cdf811729` completed someone else's merge); a red merge-up gate runs `git merge --abort` at once and proves `test ! -e .git/MERGE_HEAD` before reporting; prefer gating on a temporary tree (`git merge-tree --write-tree HEAD <tip>`, then a throwaway worktree for tests) so MAIN never holds a merge in progress. Push after every action; `index.lock` → wait, never delete. Prayer once at open, once at close. A `[agi-nudge]` after a `peek` is NOT phantom — consume with `read` (F25). Phantom = empty inbox on `read`: one read, nothing else. A nudge whose only unread is YOUR OWN after_join dm = the same. `.agi/tmp/` is TRACKED in MAIN (27 files) and `.gitignore:118-120` steers kids there — until SM's brief line lands, every harvest's stray filter must keep `.agi/tmp/` OUT (it does: only `.agi/nodes/`, `extensions/agi/`, `.agi/sessions/iter-<ITER>/` pass).

## §5 STATE + NEXT (2026-09-16 14:0xZ — gen 8 closing near the line; successor wakes on 0)
**Today, one line each (all on MAIN, pushed):** SL7.128 `cdc1d9364` (fixture from the producer) · SL7.129 `ba888a20e` (both producers, read back; SL7.124 chain CLOSED) · SL7.130 `db6357605` (**audit verbs record-keyed** — `b_generation` is prime-only since `e85a1a797`) · SL7.131 `cc42a58fd` (selector refuses ambiguous stamps by name; `latest` ≡ no-flag) · suite windows: run 1 red 4997/1 (SIGTERM test, ruled a timing bug), run 2 **stamped `a51f8deee`** 11/11 · `merge-up-review` re-authored `timeout_s` 1800/stage `b31eaef3c` (SM's line, `workflow.py author`) · upstreams set on all 3 post worktree branches · 5 code lines routed to SM, all minted (scratch-dir brief clause, stops-slot card path, stale-base `sync`, post-branch `-u`, reap-proof placeholder) · audits drafted: SD gen 26 wake 28 / gen 27 wake **0**, TM, Prime XXII→XXIII (stub-card `--stops` pair), SM; card (4) closed on TM + SM rows.

**IN FLIGHT:**
- **SL7.132** (SIGTERM stale-record test waits on `armed`/`cleaned`, never wall clock): parent `a00-99de32ca` DIED on a 520 before harvest → I completed the review (TM.07 precedent), kept the kid's `inconclusive_lean_proved:75` (fix built, 30/30 + 40/40 ×3; pre-fix reproduction never fired in 55 loops), done-committed on the loop branch **tip `598bb875f`**, gate `7a0216c41` 40 passed, **`[merge-up]` sent 13:5xZ — awaiting GO.** Land: ff-only sync, merge-tree, ONE `--no-ff 598bb875f`, push, proof (blobs == merge-tree, ancestor, no MERGE_HEAD), numbers line.
- **SL7.133** (audit verbs write their result into the rotation record under `audit:`; print `green`/`FINDING` by the ladder floors; dm to the Prime stays a Sensei act): parent `a00-747119ec` pid 2345247 dispatched 14:0xZ, worktree `.agi/worktrees/a00-747119ec/`. Harvest: strays → loop branch; tests = the four `test_sensei*.py`; proof = a record's bytes outside `audit` unchanged before/after, re-run idempotent.

**Rules that changed today (owner via belam, verbatim in `doc:l4-owner-decisions`):** 13:5xZ **ROTATION PINGS** — alerts matrix `{audit:[master-sensei],edges:{}}`: a rotation announces to the Sensei ONLY; nobody sends `[rotation]` one-liners any more; the Sensei dms the Prime ONLY on a finding (floor breach with a structural cause, or failed key verification); a green audit stays in the rotation record (= SL7.133). 13:3xZ **ACCOUNT** — floor 5.0 → 1.6 (`8e29dd8d2`), run the OpenRouter account to $0, successor account proven, dispatch stays ON, 520 is transient — check the KEY, not the account; the old "remaining − 5.00 ≥ 3.00" line is VOID. 11:0xZ + g17.1 **COMMIT RULES** (§4).

🔴 **NEXT (successor):** wake = NOTHING. **(1)** Land SL7.132 on GO (above). **(2)** Harvest SL7.133 when the parent dms; then the first record-written audit is the proof. **(3) Template line, mine:** `config:rotations` body :123 — the Prime row's after_join `sensei-wake` entry (`send.py send master-sensei 'rotation-alert: belam gen {gen} is live…'`) is now a DUPLICATE of the matrix announce, arrives UNSIGNED (from: unknown), and says "gen {gen}" against the no-generations order → drop the entry (`write.py config:rotations 'read body 118:128'` first; `replace body N:M`; `test_rotate_templates.py test_rotate_startup.py` green; never under a suite lock). **(4)** facts-2 template half once SM's `l4-the-facts-guard-…` code half lands (`test_rotate_templates.py:400` → `startswith("facts")`); region 7189/7200 → no new fact before it. **(5)** Audit every rotation with the verbs (`sensei.py --root . rotate-out-audit|wake-audit --post <p>`; `--record <stamp>` for an earlier one; `--gen` deprecated): green → record (after SL7.133) / draft; finding → one dm to the Prime; code lines → SM. Hygiene notes for the lane's next node: sensei.py `:829` return annotation (2-tuple for a 3-tuple), `_select_wake_record` docstring `:813-816`. **(6)** Measure (4): helper + council-local-maxxing rows unobserved; Prime row carries `ultracode` until SM's renderer fix. **(8) SM line 14:00Z, mine when SM.45/46 reach MAIN:** the parent brief's answer-protocol segment (`brief.py` `_parent`, on the sensei-director post branch now) must also say: when a parent answers a kid's `rebrief_request` in-node it dms its director the answer line (kid id, N/C, proceed-with-N | cut) BEFORE the kid resumes (SM.46's kid ran to 6× with the parent self-authorising in-node). Prose in a code file → ONE tiny own-line node + one kid, never a hand edit. **(7)** Hand-seating class (TM + SM chains today): a hand re-seat leaves no record naming the joined transcript — mint on the third case.

## §6 BANKED
- Drafts under `.agi/sessions/sensei/drafts/` are tracked; commit by exact path (`git add` a NEW file first, then `commit -o`).
- **Facts edits, the safe way:** capture `write.py config:rotations 'read body 37:64'` to scratch; build the new region; splice into a COPY; `tests.test_rotate_templates._region_refusal(copy)` must be `None`; ≤ 7200 B; exactly 28 lines; pinned by ID — F1 F3 F8 F9 F13 F14 F15 F16 F17 F18 F27; apply with `write.py config:rotations 'replace body 37:64 <file>'`; run the two template tests; NEVER with the suite lock up.
- Shell: single-quote `send.py send` lines; `sensei.py --root <dir> <verb>` (global option BEFORE the verb); `git commit -o -m '…' -- <paths>` (`-m` before `--`).
- Landing shape: strays dropped on the loop branch; a parent's post-`done` edits or a dead parent's kid work = one loop-branch commit; one true merge; temp-tree gate MANDATORY (g17.1 `8d2f9d12e`).
- `.agi/tmp/` is TRACKED (27 files) and `.gitignore:118-120` steers kids there until SM's brief clause lands — the stray filter keeps it out.
- Phantom dead-pid record under `iter-L3.39/rescued-kid-logs/…/a00-3881afe7` (pid 1459751): L3 artefact, note only (belam).
- Dirty nodes in MAIN's tree that are not mine are other posts' in-flight writes — never bundled.

## 🔴 Where it stops
```
2026-09-16 14:0xZ: gen 8 at ~0.36 of the window. Four rounds landed (SL7.128-131), suite stamped a51f8deee, SL7.132 awaiting GO (tip 598bb875f, director-reviewed after the parent died on a 520), SL7.133 in flight (parent a00-747119ec). Successor: wake 0; land SL7.132 on GO; harvest SL7.133; drop the Prime row's sensei-wake after_join entry (NEXT 3).
```
