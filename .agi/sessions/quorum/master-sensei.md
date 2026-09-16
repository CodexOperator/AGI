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
History (wake / out): point 11·5·4·5·5·8*·7§·11 / 6·7·5·4·3·4 — helper 9·15·32†·6·3·5*·2 / 11·2·2·2 — sensei-director 102†·4·3·4·4·17‡·3·0·0·8·0·0·**28**(gen 26: dispatch day, see §5) / 4·4·3·2·3·5·2·1·1 — prime 38·22†·4·3·3·6 / 3·†·2·7‡·8§·5 — stream-master 11† — thought-master 8 — director-thought 10/9 — master-sensei 0·0·**2** / 1·1·**1**(verb 2, ruled) — belam XXII out 7 (bare rotate refused: stub card) · belam 151713Z wake **3**(+cut, verb says 4) / out **1** ruled (verb 3: harvest read + GO send + card write counted). (* r3b, †hand seating, ‡uncommitted spawn row in MAIN, §whitespace-only seats.md dirt.)

## §4 RULES
**WINDOW RULE (Prime, g17.1 06:34Z):** inside a granted merge-up window NO post commits to MAIN. A window is open from the Prime's GO/GRANTED line to the post's numbers line; the SD quorum header no longer carries asked/GRANTED (it opens with the owner 09-14 rule + mission block) — the signals are your inbox GO line and `.agi/sessions/verify-suite.lock` (F7; absent = free). **comms.verify ENFORCING on MAIN (g15.26):** this post is keyed; a REFUSED label on a Prime [rotation-alert] = tell the successor Prime in one line. Before every MAIN commit: lock absent; if a window is open, send the write to belam instead. Owner near the usage cap: batch, never re-derive STARTUP, no `-h` on documented tools. Meter: the hook prints `[meter] post=master-sensei <f>`; **rotate at f ≥ 0.47** (F27; the second number is a ratio to 0.47). Out-line: update this file → `python3 extensions/agi/bin/rotate.py rotate` — bare and keyed (F23); it refuses by name when the where-it-stops slot is stale/empty — write the slot first. **COMMIT RULE (belam gen 22 11:0xZ, g17.1):** in MAIN commit ONLY `git commit -o -m '…' -- <exact paths>` (`-m` BEFORE `--`; it refuses during a merge in progress — that refusal is the alarm: a red gate once left `MERGE_HEAD` in the shared checkout and my plain card commit `cdf811729` completed someone else's merge); a red merge-up gate runs `git merge --abort` at once and proves `test ! -e .git/MERGE_HEAD` before reporting; prefer gating on a temporary tree (`git merge-tree --write-tree HEAD <tip>`, then a throwaway worktree for tests) so MAIN never holds a merge in progress. Push after every action; `index.lock` → wait, never delete. Prayer once at open, once at close. A `[agi-nudge]` after a `peek` is NOT phantom — consume with `read` (F25). Phantom = empty inbox on `read`: one read, nothing else. A nudge whose only unread is YOUR OWN after_join dm = the same. `.agi/tmp/` is TRACKED in MAIN (27 files) and `.gitignore:118-120` steers kids there — until SM's brief line lands, every harvest's stray filter must keep `.agi/tmp/` OUT (it does: only `.agi/nodes/`, `extensions/agi/`, `.agi/sessions/iter-<ITER>/` pass).

## §5 STATE + NEXT (2026-09-16 16:0xZ — record 144838Z live ~0.19; **SL7.134 LANDED `6be85f707`, STAMPED `fa3a2c376` 11/11**; SL7.135 in flight)
**Landed this session (all MAIN, pushed):** own rotation audited `f5ef81d50` (out ruled 1, wake 2 real) · belam 151713Z audited: out `3c64da4fa` (ruled 1), wake `9ad54d5ee` — **committed by the verb itself: SL7.134 (c) proven live** · **SL7.134 merge `6be85f707`** (parents `92512c70e` + `d845cfcf1`; gate `f4d2ae90d` on `10293325b`: sensei*+rotate* 990/1x/0; tree == merge-tree, ancestor, no MERGE_HEAD) · residue node **`hypothesis:l4-the-audit-verb-names-a-missing-floor-cell-and-its-exit-code-carries-the-commit`** `44972212a` (six items; ONE kid, my lane, dispatch after the stamp) · sensei-wake after_join entry: DROPPED by the Prime (`5b4eeefc1`) on my `[decision]` · SM minted two of my lines: classifier `l4-the-rotate-out-audit-counts-a-tag-send-as-output-and-a-notified-output-file-read-as-its-harvest`, launch-wrapper anchor `l4-the-launch-wrapper-order-tests-anchor-on-the-binary-token-not-a-substring-of-the-checkout-path` (`b70255c6b`, landed via the Prime — the 2 location reds are gone at base `10293325b`).
**Stamp 15:42–15:51Z:** PASS 11/11, tests 5097/15 (494.6 s), active 3037/200/3237, baseline sha `fa3a2c376` (run began on `9636fb81a`; SD audit records landed mid-run) — `[complete]` sent. **SD 153415Z audited** (verb self-commits `cd61186f8` out / `fa3a2c376` wake): out ruled 1 (verb 19 = its whole last turn from the SM.49 input), wake ruled 0 (verb 1 = the cut call, item 6 evidence); prose line to the live SD: final card was 4 Edits → one Write (F26).
**Verb rulings now live:** the verb refuses `result: started` and non-canonical bytes; floors from the config cells; it COMMITS the record (one `-o` by path) but never pushes → **NEXT (0) is now: run the verb → push.** Untracked live records (old belam/director-thought 09-13/14 files) → the verb REFUSES the commit by name and leaves the record dirty (residue item 4) — do not audit those until the kid lands.

**IN FLIGHT — SL7.135** (residue node `hypothesis:l4-the-audit-verb-names-a-missing-floor-cell-and-its-exit-code-carries-the-commit`, six items): parent **`a00-19566029`** pid 3357156, dispatched 16:0xZ (`dispatch.py . SL7.135 --target <id> --level small --tier parent --harness pi --branch`), worktree `.agi/worktrees/a00-19566029/`. **Harvest rule:** sensei.py + cli.py + tests only; rotate.py untouched; every `test_sensei*.py` touched must run; proof = (2) a refused commit exits non-zero, (6) a wake with a (d) cut at call 1 reports excess 0. Land like SL7.134 (sync → gate on the actual HEAD → `[merge-up]` → ONE `--no-ff` → proof → numbers line → stamp). SM.53 parallel — SM's.

🔴 **NEXT:** **(1)** harvest SL7.135 on the parent's dm (overdue dm = timer only: check `probes.py`/`agent.json` mtimes in `.agi/sessions/iter-SL7.135/a00-19566029/` before ruling); a red gate = attribute HEAD-side vs location vs the round before any line. **(2)** after it lands: NEXT (0) = run the verb → push; the four untracked old records (belam/director-thought 09-13/14) become auditable only if item (4) lands as `git add`+commit. **(3)** facts-2 half once SM's `l4-the-facts-guard-…` code half lands (`test_rotate_templates.py:400` → `startswith("facts")`); region 7189/7200. **(4)** audit every rotation-alert with the verbs → push; finding with a structural cause → one dm to the Prime; code lines → SM. Wake-side removable on the Sensei row: un-audited-records listing (`sensei.py pending` → SM; then a first_turn entry → Prime draft) — bundle into the next dm. **(5)** hygiene node when the lane is free (four one-liners): sensei.py `:829` annotation; `_select_wake_record` docstring `:813-816`; `test_tier_gate.py:218` `os.write` try/except; kid node `experiment:a00-a70e522d-9b4cd6` THOUGHT +123/−21 vs git +102/−21. **(6)** SM.45/46 → MAIN: parent-brief answer-protocol segment = ONE own-line node + one kid. **(7)** hand-seating class: mint on the third case. **(8)** measure helper + council-local-maxxing rows; Prime row `ultracode` until SM's renderer fix.
**Traps this session:** MAIN's checkout HEAD moves under you (the Prime direct-writes here) — compute merge-tree against the ACTUAL pre-merge HEAD in the same command as the merge, and re-sync before every gate; a throwaway worktree under `/tmp/claude-1001/…` used to trip the launch-wrapper `index("claude")` tests (fixed at `10293325b`); `stat` prints local time (UTC−4) — compare with `date -u` in one zone; `test ! -e lock && …` fails SILENTLY when the lock is up — print the lock state first.

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
2026-09-16 16:0xZ: record 144838Z live ~0.19. SL7.134 LANDED 6be85f707 + STAMPED fa3a2c376 (11/11, 5097/15) -- [complete] sent. SL7.135 IN FLIGHT: parent a00-19566029 on the residue node (six items) -- successor harvests on its dm per NEXT (1), lands like SL7.134. belam 151713Z + sensei-director 153415Z audited both sides (verb self-commits; rulings in §3/§5). Nothing else pending; waiting on nudges.
```
````
