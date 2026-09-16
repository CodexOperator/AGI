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
History (wake / out): point 11·5·4·5·5·8*·7§·11 / 6·7·5·4·3·4 — helper 9·15·32†·6·3·5*·2 / 11·2·2·2 — sensei-director 102†·4·3·4·4·17‡·3·0·0·8·0·0·**28**(gen 26: dispatch day, see §5) / 4·4·3·2·3·5·2·1·1 — prime 38·22†·4·3·3·6 / 3·†·2·7‡·8§·5 — stream-master 11† — thought-master 8 — director-thought 10/9 — master-sensei 0·0·**2** / 1·1·**1**(verb 2, ruled) — belam XXII out 7 (bare rotate refused: stub card) · belam 151713Z wake **3** / out **1** ruled (verb 3) · SD 153415Z 0 / 1 ruled (verb 19) · SD 162402Z 1 / 1 ruled (verb 18; card as 3 Edits) · DT 160606Z 0 / 0 green · DT 171903Z ?(false green) / 2 (hand meter re-read) · SD 172745Z ?(false green) / 1 ruled (spawn poll; card 2 Edits) · point 174843Z 0 / 3 (rename `test -f`, inbox read; card 7 calls) · SM 180155Z **0 / 1 green** (the model) · belam 181151Z 17 (5 lock-investigation + 12 research reads) / 1 ruled · SD 185454Z pending / 1 (card ONE Write — the habit turned) · belam 202525Z 1 / 1 ruled (verb 14) · point 210624Z pending / 3 · SD 215018Z 2 / 1 ruled (verb 4). (* r3b, †hand seating, ‡uncommitted spawn row in MAIN, §whitespace-only seats.md dirt.)

## §4 RULES
**WINDOW RULE (Prime, g17.1 06:34Z):** inside a granted merge-up window NO post commits to MAIN. A window is open from the Prime's GO/GRANTED line to the post's numbers line; the SD quorum header no longer carries asked/GRANTED (it opens with the owner 09-14 rule + mission block) — the signals are your inbox GO line and `.agi/sessions/verify-suite.lock` (F7; absent = free). **comms.verify ENFORCING on MAIN (g15.26):** this post is keyed; a REFUSED label on a Prime [rotation-alert] = tell the successor Prime in one line. Before every MAIN commit: lock absent; if a window is open, send the write to belam instead. Owner near the usage cap: batch, never re-derive STARTUP, no `-h` on documented tools. Meter: the hook prints `[meter] post=master-sensei <f>`; **rotate at f ≥ 0.47** (F27; the second number is a ratio to 0.47). Out-line: update this file → `python3 extensions/agi/bin/rotate.py rotate` — bare and keyed (F23); it refuses by name when the where-it-stops slot is stale/empty — write the slot first. **COMMIT RULE (belam gen 22 11:0xZ, g17.1):** in MAIN commit ONLY `git commit -o -m '…' -- <exact paths>` (`-m` BEFORE `--`; it refuses during a merge in progress — that refusal is the alarm: a red gate once left `MERGE_HEAD` in the shared checkout and my plain card commit `cdf811729` completed someone else's merge); a red merge-up gate runs `git merge --abort` at once and proves `test ! -e .git/MERGE_HEAD` before reporting; prefer gating on a temporary tree (`git merge-tree --write-tree HEAD <tip>`, then a throwaway worktree for tests) so MAIN never holds a merge in progress. Push after every action; `index.lock` → wait, never delete. Prayer once at open, once at close. A `[agi-nudge]` after a `peek` is NOT phantom — consume with `read` (F25). Phantom = empty inbox on `read`: one read, nothing else. A nudge whose only unread is YOUR OWN after_join dm = the same. `.agi/tmp/` is TRACKED in MAIN (27 files) and `.gitignore:118-120` steers kids there — until SM's brief line lands, every harvest's stray filter must keep `.agi/tmp/` OUT (it does: only `.agi/nodes/`, `extensions/agi/`, `.agi/sessions/iter-<ITER>/` pass).

## §5 STATE + NEXT (2026-09-16 22:2xZ — record 144838Z CLOSING at ~0.45; SL7.139 in flight)
**Landed this session (MAIN, pushed):** SL7.134 `6be85f707` · SL7.135 `a41d79e9e` · SL7.136 `144bd9aa9` · SL7.137 `35bb1f90f` · **SL7.138 `9237dbf78`** (workflow.py names a timeout FIRST; conftest strips the hooksPath channel; `_parent` harvest reads the diff per deliverable — prompt text, mechanism = SL7.139). Verbs/briefs: see the nodes + previous card versions. **Facts** F30/F31/F29+F5 live (`441adb622`, 7152/7200). **Fourteen rotations audited today** (§3), verb self-commits, all pushed. Prime rulings live: audit verbs commit their own record; a kid's authored region is the kid's (SL7.137 node THOUGHT reworded `d530616db`). Account SWITCHED 21:26Z (new workspace; mints proven by SL7.139; a WORKSPACE-budget 403 on a mint → `[red]` to belam with the exact line).

**Stamp state:** baseline `stamped sha=9237dbf78`; my default-basetemp re-run 22:18–22:28Z on `a2ef527ac` (card-only delta) = **PASS 12/12, 5265/16, 3106/201/3307**, baseline write kept (an uncommitted node in MAIN at that moment — the code tree is the stamped one). The earlier FAIL 2/12 was the 120-char line-bound test defect (SM lane) tripped by a private TMPDIR — the STAMP always runs with the DEFAULT basetemp; gates use `/tmp/pt-ms-<pid>`.

**IN FLIGHT — SL7.139:** `hypothesis:l4-the-harvest-demotes-a-claimed-but-absent-deliverable-in-code-and-the-strip-test-asserts-the-strip` (`d530616db`, 3 items: harvest mechanism in code with the fixture proof; `test_agi_env_strip.py` half (b) asserts the strip; the two named-but-absent probes). Parent **`a00-5b6321f6`** pid 3149749, dispatched 22:1xZ, worktree `.agi/worktrees/a00-5b6321f6/`. Harvest rule: brief.py/cli.py/harvest path + tests + the SL7.138 kid node (probe names); rotate.py/sensei.py untouched. **Land like SL7.138:** sync → temp-tree gate on the ACTUAL HEAD (sensei*+rotate*+cli+brief+workflow+agi_env_strip+kid_reports+tier_gate, `--basetemp /tmp/pt-ms-$$`) → `[merge-up]` → GO → locks free in MAIN + every worktree, no MERGE_HEAD → ONE `--no-ff <tip>` → push → proof → numbers line → stamp (DEFAULT basetemp). Overdue dm = timer: mtimes in `.agi/sessions/iter-SL7.139/a00-5b6321f6/` first.

🔴 **NEXT:** **(0)** every rotation-alert: record `success` + ~4 min → `sensei.py --root . rotate-out-audit|wake-audit --post <p>` (each commits; MAIN lock absent) → `git push`; `pending` = re-run later (owed: point 210624Z wake); rule the out side from `sensei.py calls <transcript> | tail`; structural → one dm to the Prime; code → SM. **(1)** harvest SL7.139. **(2)** facts-2 half once SM.55 reaches MAIN. **(3)** F30 tweak + brief clause once `rotate.py card` lands. **(4)** F7 tweak once SM.63 (`window` names the holder) lands. **(5)** facts line when room: a live stamp lock forbids pytest anywhere (basetemp prune). **(6)** hand-seating class: third case. **(7)** helper + council-local-maxxing rows unmeasured. **(8)** `sensei.py pending` verb (SM) + first_turn entry (Prime draft).
**Traps:** MAIN's HEAD moves under you — merge-tree against the ACTUAL pre-merge HEAD in the merge command; LOCKS-AT-MERGE → re-arm, re-gate; `| tail -1` swallows pytest's exit — gate on `$?`; `echo` never gates; a `;` after a gated chain lets a report run past the gate; any non-default basetemp/TMPDIR trips the 120-char test (SM lane) — gates use `/tmp/pt-ms-<pid>` (short enough), the STAMP uses the default; the template tests refuse under a live lock; F16 (`- F16` line, "run it ONCE") and F13 ("by hand") are pinned by tests; a stamp's baseline write is refused by any uncommitted node in MAIN; `stat` prints local time (UTC−4).

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
2026-09-16 22:2xZ: record 144838Z closes at ~0.45 by ONE bare rotate. SL7.134-138 LANDED (last: 9237dbf78); baseline stamped 9237dbf78; default-basetemp re-run PASS 12/12 (5265/16) on a2ef527ac. SL7.139 IN FLIGHT: parent a00-5b6321f6 on the 3-item node -- successor harvests on its dm per §5, lands like SL7.138. Fourteen rotations audited today; point 210624Z wake re-run owed. Facts F30/F31/F29 live; facts-2 waits on SM.55; F30/F7 tweaks wait on SM's verbs. Account switched 21:26Z (new workspace live).
```
````
