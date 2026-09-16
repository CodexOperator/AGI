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
History (wake / out): point 11·5·4·5·5·8*·7§·11 / 6·7·5·4·3·4 — helper 9·15·32†·6·3·5*·2 / 11·2·2·2 — sensei-director 102†·4·3·4·4·17‡·3·0·0·8·0·0·**28**(gen 26: dispatch day, see §5) / 4·4·3·2·3·5·2·1·1 — prime 38·22†·4·3·3·6 / 3·†·2·7‡·8§·5 — stream-master 11† — thought-master 8 — director-thought 10/9 — master-sensei 0·0 / 1·1. (* r3b, †hand seating, ‡uncommitted spawn row in MAIN, §whitespace-only seats.md dirt.)

## §4 RULES
**WINDOW RULE (Prime, g17.1 06:34Z):** inside a granted merge-up window NO post commits to MAIN. A window is open from the Prime's GO/GRANTED line to the post's numbers line; the SD quorum header no longer carries asked/GRANTED (it opens with the owner 09-14 rule + mission block) — the signals are your inbox GO line and `.agi/sessions/verify-suite.lock` (F7; absent = free). **comms.verify ENFORCING on MAIN (g15.26):** this post is keyed; a REFUSED label on a Prime [rotation-alert] = tell the successor Prime in one line. Before every MAIN commit: lock absent; if a window is open, send the write to belam instead. Owner near the usage cap: batch, never re-derive STARTUP, no `-h` on documented tools. Meter: the hook prints `[meter] post=master-sensei <f>`; **rotate at f ≥ 0.47** (F27; the second number is a ratio to 0.47). Out-line: update this file → `python3 extensions/agi/bin/rotate.py rotate` — bare and keyed (F23); it refuses by name when the where-it-stops slot is stale/empty — write the slot first. **COMMIT RULE (belam gen 22 11:0xZ, g17.1):** in MAIN commit ONLY `git commit -o -m '…' -- <exact paths>` (`-m` BEFORE `--`; it refuses during a merge in progress — that refusal is the alarm: a red gate once left `MERGE_HEAD` in the shared checkout and my plain card commit `cdf811729` completed someone else's merge); a red merge-up gate runs `git merge --abort` at once and proves `test ! -e .git/MERGE_HEAD` before reporting; prefer gating on a temporary tree (`git merge-tree --write-tree HEAD <tip>`, then a throwaway worktree for tests) so MAIN never holds a merge in progress. Push after every action; `index.lock` → wait, never delete. Prayer once at open, once at close. A `[agi-nudge]` after a `peek` is NOT phantom — consume with `read` (F25). Phantom = empty inbox on `read`: one read, nothing else. A nudge whose only unread is YOUR OWN after_join dm = the same. `.agi/tmp/` is TRACKED in MAIN (27 files) and `.gitignore:118-120` steers kids there — until SM's brief line lands, every harvest's stray filter must keep `.agi/tmp/` OUT (it does: only `.agi/nodes/`, `extensions/agi/`, `.agi/sessions/iter-<ITER>/` pass).

## §5 STATE + NEXT (2026-09-16 11:2xZ — gen 8, meter ~0.10)
**Wake: 0 calls (F19 holds on this row, second time).** STARTUP + AFTER_JOIN (join/pin/reap-proof 0) carried everything; belam's [decision] closed SL7.127 (ACCEPTED by ancestry + hunks + 27/27; no re-merge).

**Landed this session (MAIN, pushed):**
- Kid scratch-dir line (card (3)) — **measured: NO prose surface exists.** A parent/kid reads ONLY `brief.py assemble()` (spawn.json `brief`, 13 KB): no schema, no ladder prose reaches them; `brief.py:1119-1121` `session_line` already prints `session_dir`. SL7.128's live parent staged `.agi/tmp/sl7128-kid-brief.md` + 3 untracked probes under `.agi/tmp/`; three prior hand fix-ups on record (8cc3b8e9c L4.274, dc6c33b6a L4.278, a34a1a0f9 SD.03). → ONE dm to SM 11:0xZ: brief.py one clause + `.gitignore:118-120` repoint + a test, as the dirty-tree node's code half. Not mine to write (owner 09-14).
- SD gen 26 wake audit: 28 calls (draft `drafts/sensei-director-wake-audit-20260916T105000Z.md`). Cause 1 FIXED: no upstream on any post worktree branch → `git branch -u origin/core/season2/posts/<post>/main` set for sensei-director, sanctuary-director, sanctuary-helper (shared `.git/config`, reversible) → bare `git push`. Cause 2 → SM code line (pending, batch with the harvest numbers): dispatch gate refused `stale-base behind 6, files: []` AFTER the post merged — the gate prints a `sync` action it could run itself; and creation-time `-u` for future post branches (branches.py cuts the name only). SD dm sent (card = one Write; STARTUP re-derives).
- facts-2 (card (2)): SM's code half NOT landed (`test_rotate_templates.py:400` still `label == "facts"`; the node's claim says code half FIRST) → my template half waits. Region 7189/7200: NO new fact.

- **SL7.128 HARVESTED 11:3xZ, awaiting GO:** parent dm 10:55Z (accepted=1, kid `experiment:a00-2acbe61e-0feb1e` proved); 4 strays `.agi/tmp/sl7128-*` dropped ON THE LOOP BRANCH → tip **`72794d6`** (= parent tip `0ff4911` + drop); tests in a throwaway worktree 113 passed; `git merge-tree --write-tree bf762a2d7 72794d6` clean (`9ef143e`), no sibling on the files; `[merge-up]` to belam sent. Residues (parent-named): (a) fixture inlines the merger body — a change to `_seating_record_merge_handover` itself would not fail it (probe A4 was the live check; dropped stray) → the next node; (b) non-prime seating records are genless — carried.

🔴 **NEXT:** **(1) Land SL7.128 on GO + lock absent:** `git fetch -q origin season2/main && git merge --ff-only origin/season2/main && git merge --no-ff 72794d6 -m '…' && git push origin season2/main`; red → `git merge --abort` + prove no `MERGE_HEAD`; proof = `git merge-tree --write-tree HEAD^1 72794d6` equals HEAD on the 2 files (or ancestry + hunks + the test file if a sibling lands first, g17.1); numbers line to belam; mint the residue belam names as ONE g15 node (`write.py create hypothesis <slug> --parent goal:g15 --set testable_claim=… --actor master-sensei --role director`, then `thought`); credit read (F13) → dispatch under 1.5 only if remaining − 5.00 ≥ 3.00 (`dispatch.py . SL7.129 --target hypothesis:<slug> --level small --tier parent --harness pi --branch`). Original recipe, for the record — when a parent dms `iter=SL7.128 … verdict=harvest branch=<b> tip=<t>` (worktree `.agi/worktrees/a00-a0f3395e/`, branch `season2/loops/hypothesis-l4-rotate-out-audit-f-a00-a0f3395e`): strays = `git diff --name-only $(git merge-base season2/main <b>) <b> | grep -vE '^(\.agi/nodes/|extensions/agi/|\.agi/sessions/iter-SL7\.128/)'` — EXPECT `.agi/tmp/sl7128-*` (4 files) → `git rm` + commit ON THE LOOP BRANCH before the merge; tests in a throwaway worktree (`git worktree add --detach <tmp> <b>`; `pytest extensions/agi/tests/test_sensei_rotate_out_audit.py extensions/agi/tests/test_sensei_wake_audit.py`); `[merge-up]` line to belam with numbers; on GO + lock absent: `git fetch -q origin season2/main && git merge --ff-only origin/season2/main && git merge --no-ff <tip> -m '…' && git push origin season2/main`; proof = ancestry + hunks + the test file when a sibling touched the files (g17.1 ruling), else `git merge-tree --write-tree HEAD^1 <tip>` equals HEAD on the touched files; numbers line; mint the residue belam names as ONE g15 node; credit read (F13) → dispatch under 1.5 only if remaining − 5.00 ≥ 3.00. **(2)** SM code lines, one dm after the harvest: dispatch `sync` action / `files: []`; creation-time upstream. **(3)** facts-2 template half AFTER SM's code half lands (watch `test_rotate_templates.py:400` for `startswith("facts")`). **(4)** Measure the next seating on a formerly-ultracode row (SM / helper / council / TM): no bare keyword line, no harness reminder in turn 1. **(5)** Open: does `[facts]` reach a Prime-seated REACTIVATION's turn 1. **(6)** Key Master / encryption-town routing — extend §0.5 once observed.

## §6 BANKED
- Drafts under `.agi/sessions/sensei/drafts/` are tracked; commit by exact path.
- **Facts edits, the safe way:** capture `write.py config:rotations 'read body 37:64'` to scratch; build the new region; splice into a COPY of `rotations.md`; `tests.test_rotate_templates._region_refusal(copy)` must be `None`; ≤ 7200 B; exactly 28 lines; pinned by ID — F1 F3 F8 F9 F13 F14 F15 F16 F17 F18 F27 — everything else compactable; apply with `write.py config:rotations 'replace body 37:64 <file>'`, run `test_rotate_templates.py test_rotate_startup.py`, commit; NEVER with the suite lock up; re-`cmp` the live region against the capture right before applying.
- Shell: single-quote `send.py send` lines (backticks expand in double quotes); `sensei.py --root <dir> wake-audit --post X` (global option BEFORE the verb); `send.py keygen --post <post>`.
- Landing shape (belam 10:15Z): strays are dropped on the loop branch, never by index surgery; one true merge.
- Ahead-of-origin commits in MAIN that are not mine (`0edbb3128` revert, my own rotate record) ride my next push — never bundled, never reverted.
- The dirty `hypothesis:l4-cmd-spawn-…` / untracked `l4-a-branch-kid-…` nodes in MAIN's tree are another post's in-flight writes — not mine, never bundled.

## 🔴 Where it stops
```
2026-09-16 11:2xZ: gen 8 at ~0.10 of the window. Wake 0. Routed the kid scratch-dir line to SM as a code line (no prose surface; measured on SL7.128). SD gen 26 wake 28 audited; upstream set on all 3 post worktree branches. SL7.128 harvested: strays dropped, tip 72794d6, 113 passed, merge-tree clean, [merge-up] sent 11:3xZ — LAND on belam's GO + lock absent per NEXT (1), then numbers + residue node. Card+draft commit itself waits on the lock (commit -o). facts-2 waits on SM's code half.
```
