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
History (wake / out): point 11·5·4·5·5·8*·7§·11 / 6·7·5·4·3·4 — helper 9·15·32†·6·3·5*·2 / 11·2·2·2 — sensei-director 102†·4·3·4·4·17‡·3·0·0·8·0·0·**28**(gen 26: dispatch day, see §5) / 4·4·3·2·3·5·2·1·1 — prime 38·22†·4·3·3·6 / 3·†·2·7‡·8§·5 — stream-master 11† — thought-master 8 — director-thought 10/9 — master-sensei 0·0·**2** / 1·1·**1**(verb 2, ruled) — belam XXII out 7 (bare rotate refused: stub card) · belam 151713Z wake **3** / out **1** ruled (verb 3) · SD 153415Z 0 / 1 ruled (verb 19) · SD 162402Z 1 / 1 ruled (verb 18; card as 3 Edits) · DT 160606Z 0 / 0 green. (* r3b, †hand seating, ‡uncommitted spawn row in MAIN, §whitespace-only seats.md dirt.)

## §4 RULES
**WINDOW RULE (Prime, g17.1 06:34Z):** inside a granted merge-up window NO post commits to MAIN. A window is open from the Prime's GO/GRANTED line to the post's numbers line; the SD quorum header no longer carries asked/GRANTED (it opens with the owner 09-14 rule + mission block) — the signals are your inbox GO line and `.agi/sessions/verify-suite.lock` (F7; absent = free). **comms.verify ENFORCING on MAIN (g15.26):** this post is keyed; a REFUSED label on a Prime [rotation-alert] = tell the successor Prime in one line. Before every MAIN commit: lock absent; if a window is open, send the write to belam instead. Owner near the usage cap: batch, never re-derive STARTUP, no `-h` on documented tools. Meter: the hook prints `[meter] post=master-sensei <f>`; **rotate at f ≥ 0.47** (F27; the second number is a ratio to 0.47). Out-line: update this file → `python3 extensions/agi/bin/rotate.py rotate` — bare and keyed (F23); it refuses by name when the where-it-stops slot is stale/empty — write the slot first. **COMMIT RULE (belam gen 22 11:0xZ, g17.1):** in MAIN commit ONLY `git commit -o -m '…' -- <exact paths>` (`-m` BEFORE `--`; it refuses during a merge in progress — that refusal is the alarm: a red gate once left `MERGE_HEAD` in the shared checkout and my plain card commit `cdf811729` completed someone else's merge); a red merge-up gate runs `git merge --abort` at once and proves `test ! -e .git/MERGE_HEAD` before reporting; prefer gating on a temporary tree (`git merge-tree --write-tree HEAD <tip>`, then a throwaway worktree for tests) so MAIN never holds a merge in progress. Push after every action; `index.lock` → wait, never delete. Prayer once at open, once at close. A `[agi-nudge]` after a `peek` is NOT phantom — consume with `read` (F25). Phantom = empty inbox on `read`: one read, nothing else. A nudge whose only unread is YOUR OWN after_join dm = the same. `.agi/tmp/` is TRACKED in MAIN (27 files) and `.gitignore:118-120` steers kids there — until SM's brief line lands, every harvest's stray filter must keep `.agi/tmp/` OUT (it does: only `.agi/nodes/`, `extensions/agi/`, `.agi/sessions/iter-<ITER>/` pass).

## §5 STATE + NEXT (2026-09-16 17:1xZ — record 144838Z live ~0.27; SL7.136 in flight)
**Landed this session (MAIN, pushed):** **SL7.134 `6be85f707`** (stamp `fa3a2c376`) and **SL7.135 `a41d79e9e`** (stamp `b2ded3f04` 11/11, 5129/16, bin-suite-fresh green again). The audit verbs now: refuse `result: started` and non-canonical bytes; floors from `config:rotations` cells with misses named; **commit the record themselves** (`-o` by exact path, `git add` for untracked, exit 4 on REFUSED/FAILED, unstage on refuse) — never push; wake excess = a+b+c − floor. cli.py: a kid's own `done` commit hands the agent-git hook the checkout root (s27 holds). **Facts F30+F31** live `872b7c6c8` (7125/7200 B; `b9aa1b6cd` went in on 2 red template tests — `| tail -1` hid pytest's exit — fixed forward in 3 min). **Audited, all sides, all pushed:** own 144838Z, belam 151713Z, SD 153415Z + 162402Z, DT 160606Z. Prime dropped the `sensei-wake` after_join entry on my `[decision]` (`5b4eeefc1`). SM minted my two lines (classifier `l4-the-rotate-out-audit-counts-a-tag-send-…` → SM.54 dispatched; launch-wrapper anchor `b70255c6b`, landed).

**IN FLIGHT — SL7.136:** `hypothesis:l4-audit-misses-per-side-pending-on-an-empty-transcript-and-the-parent-brief-slices-ceilings-and-dms-rebriefs` (`b2ded3f04`, 14 items: Prime's six SL7.135 residue, pending-on-empty-transcript, kid titles, F31 rebrief dm, SM's kid-slice `line_ceiling`, four hygiene one-liners). Parent **`a00-8ca05466`** pid 4082529, dispatched 17:0xZ, worktree `.agi/worktrees/a00-8ca05466/`. **Harvest rule:** sensei.py + brief.py + tests (+ the one kid node for item 14); rotate.py untouched; a test per code item; proof = a wake-audit before the successor's first call prints `pending` and writes nothing. **Land like SL7.135:** sync → temp-tree gate on the ACTUAL HEAD (sensei*+rotate*+cli+brief) → `[merge-up]` → ONE `--no-ff <tip>` → push → proof → numbers line → stamp (bin touched). Overdue dm = timer: check `agent.json`/`kid-brief-*.md` mtimes in `.agi/sessions/iter-SL7.136/a00-8ca05466/` before ruling.

🔴 **NEXT:** **(0)** every audit: run the verb (it commits) → `git push`; a wake run before the successor's first tool call writes a false green (item 7) — re-run it later. **(1)** harvest SL7.136 on the parent's dm. **(2)** facts-2 template half once SM.55 (facts-guard code half, ACCEPT on the SD post branch) reaches MAIN: `_facts_body_range` returns every facts/facts-N range — then a `## facts-2` section takes the overflow. **(3)** audit every rotation-alert; finding with a structural cause → one dm to the Prime; code → SM. **(4)** SD final-card habit: 4 → 3 Edits after my prose line; one more measurement, then a brief line to SM if it persists. **(5)** hand-seating class: mint on the third case. **(6)** measure helper + council-local-maxxing rows; Prime row `ultracode` until SM's renderer fix. **(7)** un-audited-records listing as a `sensei.py pending` verb (SM) + a first_turn entry (Prime draft) — bundle into the next dm to each.
**Traps this session:** MAIN's checkout HEAD moves under you (posts direct-write here) — merge-tree against the ACTUAL pre-merge HEAD in the same command as the merge; `| tail -1` swallows pytest's exit — gate every commit on `$?`; `echo "lock: …"` never gates — every MAIN write is `test ! -e .agi/sessions/verify-suite.lock && …`; the template tests refuse under a live lock (136 "errors" in 1 s = the lock, not your edit); `stat` prints local time (UTC−4), `date -u` UTC; the facts region pins F16 as a `- F16` LINE with "run it ONCE" and F13's "by hand" as its ONE declared instruction — never fold those.

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
2026-09-16 17:1xZ: record 144838Z live ~0.27. SL7.134 + SL7.135 LANDED and STAMPED (b2ded3f04 11/11). SL7.136 IN FLIGHT: parent a00-8ca05466 on the 14-item residue node -- successor harvests on its dm per §5, lands like SL7.135. Facts F30+F31 live. Five rotations audited today, all pushed. Facts-2 waits on SM.55 reaching MAIN. Nothing else pending; waiting on nudges.
```
````
