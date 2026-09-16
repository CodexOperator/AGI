# POST HANDOFF — master-sensei: LIVE SCRATCHPAD (record 20260916T144838Z, session 2026-09-16 14:48Z →, replaced wholesale by each rotation; owner quotes live in `doc:l4-owner-decisions`, never here)

## §0 WHO YOU ARE (supplied, never claimed)
Post `master-sensei`, role director, tier 1, **claude-opus-5 max**, tmux `agi-rc` window `master-sensei`, **MAIN checkout `/home/ubuntu/work/agi` on `season2/main` (`origin/season/s2` is STALE — never push to it; `git push origin season2/main`), no worktree** (config/prose you commit propagates to every post's next rotation). Card = THIS file `.agi/sessions/quorum/master-sensei.md` (F26; no worktree → MAIN). Transcript: `~/.claude/projects/-home-ubuntu-work-agi/<session-id>.jsonl`. Vocabulary (owner 22:1xZ): **post**, not seat; towns share Keepers + Masters, each town its own Council.

## §0.5 ROUTING
```
owner (in your pane) ──── answer directly
                │
master-sensei ──┼── facts (`## facts` of config:rotations) + git-config: apply yourself · template ROWS (first_turn/after_join, ANY post): draft to belam — write guard, PRIME RULING 09-11, measured 14:5xZ · prose: one dm to the live post to self-edit  (the Sensei keeps NO director — owner 08:1xZ 2026-09-13)
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
                     + facts/git-config change: YOU apply; a template ROW entry (any post): draft to the Prime (guard; no write.py verb reaches a nested frontmatter entry, a hand edit bypasses the guard = not allowed)
                     + prose (brief edit, or one dm telling the live post to self-edit)
                     + code lines → sanctuary-master (one dm, line breaks, ≤600 chars/line)
```
Listing: `python3 extensions/agi/bin/sensei.py calls <transcript>` (n · ts · tool · command, user-turn boundaries). `sensei.py wake-audit` cuts at the first (d) — under-counts; fix routed. Tool RESULTS (refusal text) come from the transcript's `tool_result` blocks keyed by `tool_use_id` — a 10-line python, not a re-run. Judge a first_turn entry in-process (F12). Two template tests must stay green: `test_rotate_templates.py test_rotate_startup.py`. **A call is removed only when the tool performs the step** (20:1xZ finding: a "don't re-read X" fact does not beat the verify-before-commit habit).

## §3 FLOOR — owner standing order 2026-09-12 03:2xZ: **wake 0 / out 1**, every post
History (wake / out): point 11·5·4·5·5·8*·7§·11 / 6·7·5·4·3·4 — helper 9·15·32†·6·3·5*·2 / 11·2·2·2 — sensei-director 102†·4·3·4·4·17‡·3·0·0·8·0·0·**28**(gen 26: dispatch day, see §5) / 4·4·3·2·3·5·2·1·1 — prime 38·22†·4·3·3·6 / 3·†·2·7‡·8§·5 — stream-master 11† — thought-master 8 — director-thought 10/9 — master-sensei 0·0 / 1·1 — belam XXII out 7 (bare rotate refused: stub card). (* r3b, †hand seating, ‡uncommitted spawn row in MAIN, §whitespace-only seats.md dirt.)

## §4 RULES
**WINDOW RULE (Prime, g17.1 06:34Z):** inside a granted merge-up window NO post commits to MAIN. A window is open from the Prime's GO/GRANTED line to the post's numbers line; the SD quorum header no longer carries asked/GRANTED (it opens with the owner 09-14 rule + mission block) — the signals are your inbox GO line and `.agi/sessions/verify-suite.lock` (F7; absent = free). **comms.verify ENFORCING on MAIN (g15.26):** this post is keyed; a REFUSED label on a Prime [rotation-alert] = tell the successor Prime in one line. Before every MAIN commit: lock absent; if a window is open, send the write to belam instead. Owner near the usage cap: batch, never re-derive STARTUP, no `-h` on documented tools. Meter: the hook prints `[meter] post=master-sensei <f>`; **rotate at f ≥ 0.47** (F27; the second number is a ratio to 0.47). Out-line: update this file → `python3 extensions/agi/bin/rotate.py rotate` — bare and keyed (F23); it refuses by name when the where-it-stops slot is stale/empty — write the slot first. **COMMIT RULE (belam gen 22 11:0xZ, g17.1):** in MAIN commit ONLY `git commit -o -m '…' -- <exact paths>` (`-m` BEFORE `--`; it refuses during a merge in progress — that refusal is the alarm: a red gate once left `MERGE_HEAD` in the shared checkout and my plain card commit `cdf811729` completed someone else's merge); a red merge-up gate runs `git merge --abort` at once and proves `test ! -e .git/MERGE_HEAD` before reporting; prefer gating on a temporary tree (`git merge-tree --write-tree HEAD <tip>`, then a throwaway worktree for tests) so MAIN never holds a merge in progress. Push after every action; `index.lock` → wait, never delete. Prayer once at open, once at close. A `[agi-nudge]` after a `peek` is NOT phantom — consume with `read` (F25). Phantom = empty inbox on `read`: one read, nothing else. A nudge whose only unread is YOUR OWN after_join dm = the same. `.agi/tmp/` is TRACKED in MAIN (27 files) and `.gitignore:118-120` steers kids there — until SM's brief line lands, every harvest's stray filter must keep `.agi/tmp/` OUT (it does: only `.agi/nodes/`, `extensions/agi/`, `.agi/sessions/iter-<ITER>/` pass).

## §5 STATE + NEXT (2026-09-16 15:0xZ — record 144838Z live; wake 2 (mine, real) / out 1 (predecessor, ruled))
**Landed this session:** audit `master-sensei --record 20260916T144838Z` both sides → `f5ef81d50`. Out: verb FINDING excess 2, RULED true out 1 — the `[complete]` send is the window-close work act and the `cat` of the suite output was its harvest (input 1625 = task-notification carried only the output-file path). Wake: excess 2, real — record listing + `git log -3` before the verb. Two dms 14:5xZ: **belam `[decision]`** drop the Prime row's `sensei-wake` after_join entry (FILE line 123 of `.agi/nodes/.geometry/rotations.md` — frontmatter, NOT body; guard: master-sensei writes ONLY `## facts` → not mine; my hand drop REVERTED, nothing committed); **SM** one classifier line (`send.py send '[tag]…'` = work act that starts the out window; a read of the notification's `<output-file>` = harvest).
**Gen-8 landings, one line:** SL7.128-133 on MAIN, tree stamped `aa839b221` 11/11, merge-up-review timeout_s 1800, upstreams on 3 post branches, 5 code lines minted by SM (incl. reap-proof placeholder).

**IN FLIGHT — SL7.134** (`hypothesis:l4-a-started-record-keeps-its-audit-and-the-verb-commits-what-it-wrote`, `2abee4dfd`): parent `a00-ba912100` pid 2614589, kid `a00-a467a5c2`, worktree `.agi/worktrees/a00-ba912100/`. Items: (a) STARTED record keeps its audit (rotate.py preserve list + verb refuses on `result: started`), (b) floors from `config:rotations` cells, (c) `finish_audit` commits the record, (d) one window shape, (e) non-canonical record refusal, (f) tests. **Harvest rule:** rotate.py may change ONLY the preserve list; tests = every `test_sensei*.py` + `test_rotate*.py` touched; proof = a fixture STARTED record audited then rewritten to success keeps `audit`. **Land:** ff-only sync, temp-tree gate (`git merge-tree --write-tree HEAD <tip>` + throwaway worktree tests), `[merge-up]` ask, ONE `--no-ff <tip>` on GO, push, proof (blobs == merge-tree, ancestor, no MERGE_HEAD), numbers line. SM.48 (card-age captive) runs parallel — SM's.

🔴 **NEXT:** **(0)** every audit run → `git commit -o -m 'audit: <post> --record <stamp> <side> <line>' -- .agi/sessions/rotations/<record>` + push (until SL7.134 (c)). **(1)** harvest SL7.134 on the parent's dm. **(2)** belam's answer on the `sensei-wake` drop: the Prime deletes it — never me, even on a GO (guard). **(3)** facts-2 half once SM's `l4-the-facts-guard-…` code half lands (`test_rotate_templates.py:400` → `startswith("facts")`); region 7189/7200 → no new fact before it. **(4)** audit every rotation-alert with the verbs (`sensei.py --root . rotate-out-audit|wake-audit --post <p> [--record <stamp>]`): green → record; finding with a structural cause → one dm to the Prime; code lines → SM. Wake-side removable on the Sensei row: the un-audited-records listing (a `sensei.py pending` verb → SM; then a first_turn entry → Prime draft) — bundle into the next dm to each, never a fresh one. **(5)** hygiene node when the lane is free (four one-liners): sensei.py `:829` annotation; `_select_wake_record` docstring `:813-816`; `test_tier_gate.py:218` wrap `os.write` in try/except so the re-raise at `:219-220` stays unconditional; kid node `experiment:a00-a70e522d-9b4cd6` THOUGHT +123/-21 vs git +102/-21. **(6)** SM.45/46 → MAIN: parent-brief answer-protocol segment (rebrief answer dm'd to the director BEFORE the kid resumes) = ONE own-line node + one kid. **(7)** hand-seating class (TM + SM chains): mint on the third case. **(8)** measure helper + council-local-maxxing rows (unobserved); Prime row carries `ultracode` until SM's renderer fix.
**Notes:** after_join `[reap-proof]` printed exit 1 on stale pids `520777…` — grep no-match = chain gone; placeholder stale (SM's line already). The matrix announce for the Sensei's OWN rotation never reached my inbox (empty at STARTUP, no nudge) — measure on the next Sensei rotation before calling it a gap.

## §6 BANKED
- Drafts under `.agi/sessions/sensei/drafts/` are tracked; commit by exact path (`git add` a NEW file first, then `commit -o`).
- **Facts edits, the safe way:** capture `write.py config:rotations 'read body 37:64'` to scratch; build the new region; splice into a COPY; `tests.test_rotate_templates._region_refusal(copy)` must be `None`; ≤ 7200 B; exactly 28 lines; pinned by ID — F1 F3 F8 F9 F13 F14 F15 F16 F17 F18 F27; apply with `write.py config:rotations 'replace body 37:64 <file>'`; run the two template tests; NEVER with the suite lock up.
- Shell: single-quote `send.py send` lines; `sensei.py --root <dir> <verb>` (global option BEFORE the verb); `git commit -o -m '…' -- <paths>` (`-m` before `--`).
- Landing shape: strays dropped on the loop branch; a parent's post-`done` edits or a dead parent's kid work = one loop-branch commit; one true merge; temp-tree gate MANDATORY (g17.1 `8d2f9d12e`).
- `.agi/tmp/` is TRACKED (27 files) and `.gitignore:118-120` steers kids there until SM's brief clause lands — the stray filter keeps it out.
- Phantom dead-pid record under `iter-L3.39/rescued-kid-logs/…/a00-3881afe7` (pid 1459751): L3 artefact, note only (belam).
- Dirty nodes in MAIN's tree that are not mine are other posts' in-flight writes — never bundled.

## 🔴 Where it stops
````
```
2026-09-16 15:0xZ: record 144838Z live at ~0.08 of the window. Own rotation audited both sides (f5ef81d50): out ruled 1 (classifier line -> SM), wake 2 real. sensei-wake drop routed to belam [decision] (Prime-row template = the Prime's write; guard). SL7.134 in flight (parent a00-ba912100) -- harvest on its dm per NEXT (1). Nothing else pending; waiting on nudges.
```
````
