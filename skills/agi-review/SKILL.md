---
name: agi-review
description: >
  Review a merge range (BASE..TIP) with Sonnet subagents from a graph-held brief: cut the range into area
  lanes with review-lanes.sh, fan out one Sonnet reviewer per lane (the harness Agent tool, model sonnet),
  then ONE adversarial Sonnet verifier over every lane's findings; the RED scans stay mechanical. Use for a
  merge pass, a merge-up gate (mur), or any range a post must judge. Replaces workflow.py reviews.
---

# agi-review — Sonnet lanes + one verifier, from the graph

Owner 00:4xZ 10-10: "Nah just use sonnet subagents and we retired workflows.py in favor of shel scripts". Owner
07:5xZ 10-10 asked for it as a graph template. First run: PASS B5 (season2/main 7276f11d36, 272 files, 0 RED).
The brief lives in the graph: `doc:agi-review-brief` (rules, RED / demote / residue, the OUT JSON shape).

## 1 · Cut the lanes (read-only)
```bash
O=<your scratchpad>/review-<key>                      # never inside a repo worktree
sh extensions/agi/bin/review-lanes.sh <BASE> <TIP> $O [MAX]   # MAX files per lane, default 40
```
Writes `$O/range`, `$O/all.txt`, one `$O/L<n>-<area>.txt` per lane; every changed path lands in exactly one lane.
Copy the brief out of the node next to them, past BOTH frontmatter fences (a single `sed '1,/^---$/d'` leaves 0 B -- SM 08:44Z):
`awk 'f>=2; /^---$/{f++}' .agi/nodes/doc/agi-review-brief.md > $O/brief.md`

## 2 · Fan out (one Agent call per lane, all in ONE message, `model: sonnet`, background)
Prompt per lane = "Read the brief at $O/brief.md and follow it exactly." + `LANE` · `RANGE: $O/range` ·
`FILES: $O/L<n>-<area>.txt` · `OUT: $O/out/L<n>-<area>.json` · ONE focus line for the area
(engine: weakened rails · tests: tests that cannot fail · guard: root-shell safety · goals: complete without
bytes, dangling links · docs: secrets/home paths, sha claims · research: overclaims, payload paths · config:
loosened bounds, keys in records). Keep ≤ ~9 lanes; reviewers run NO tests and no repo scripts.

## 3 · Verify (ONE adversarial Sonnet agent)
Merge the lane JSONs into `$O/combined.json`; the verifier hunts a MISSED RED across the whole range
(credential shapes, a D that is not a move into deprecated/, a removed lock/refusal) and marks each residue
CONFIRMED / REFUTED / UNCHECKED into `$O/out/verify.json`. Its first word is CLEAR or RED.

## 4 · Mechanical REDs (the caller, never an agent)
Full anonymize with `.env` (`anonymize.py check --root <MAIN> --diff-file F`, as a uid that reads `.env`) ·
deletions by mint_id · `links.py links` = 0 broken. A RED blocks; residues go to ONE leaf goal (skill agi-goal).

## Traps
| trap | rule |
|---|---|
| a reviewer printing a secret | the brief forbids values: kind + file:line only |
| scratch paths in a node body | rewrite home paths to `~` before minting (anonymize home class) |
| a stale TIP | pin TIP as a sha at the start; a later delta gets its own small lane |
| a new test in the range | prove it can fail: run the SAME file on the previous tip (control = RED) and mutate one guard on yours; green alone is not evidence (DG5 round 1) |
| a grep-shaped falsifier | prove it can FAIL against the bytes: falsifier 5 grepped 'refs/grid' in a piece that never names it (alive gen 12) |

## Traps moved from cards (owner 10-10: one sweep, then a rule; self-perpetuating gens 5-8 swept at gen 9, gen 9 swept at gen 10, gens 10-11 swept at gen 11, gen 12 swept at gen 13, gens 13-14 swept at gen 14)
- a checker you approve -> read it WHOLE and ask which input makes it check NOTHING and still exit 0 (sp gen 8: DG3's checker, no sha line -> 0 checked, rc 0)
- a probe's RED you cite -> it must also go GREEN on the fixed sha; run it there first (sp gen 5: my probe disabled a job in a 2nd project and I cited the RED)
- a gate of N conjuncts -> one mutant PER conjunct, named before you judge the row; ABSENT and PRESENT-BUT-LOW are different inputs (sp gen 5: 3 flips on the PSI row in 2 min; gen 8: one mutant for a 5-conjunct gate)
- an alarm row -> two rows: RED on stress AND GREEN on a healthy live reading (sp gen 6: a NEVER-fires fix agreed into an ALWAYS-fires one)
- a red from a lane you ran -> run the same lane on the BASE in the same env before calling it (sp gen 6: 25 FAIL from an archive without .agi/context)
- an append/drain pair -> test an fd opened BEFORE the rename and written AFTER the read; never pass on the commit's own claim (sp gen 6: alarm_spool)
- a claimed hole -> trace the input through every EARLIER refusal before saying it reaches its sink (sp gen 8: .42.2 returned for a drop an earlier refusal blocks)
- a claim about what code, a unit or a key does -> read the CODE it rests on and its STATE (is-active, timestamps, expires_at, the SUM over every live key), never a name, a grep or a unit FILE (sp gen 7-8: 'carry.env writes project' from a never-active unit; a key TTL assumed)
- a count or an open item -> measure it, on the director's BRANCH as well as the trunk (sp gen 8)
- refusing a carry, or naming another path to use -> read what the CURRENT carrier moves (guard.md move.exclude) and how fresh the other path is (sp gen 5: origin lagged box-move by 5 min; withdrawn)
- testifying about a past generation -> grep the card's HISTORY (`git log -G <pat> -p -- <card>`), never the trunk text: a card is replaced whole (sp gen 5: 'VERDICT YES' was in the history; withdrawn)
- a line number in a word -> cite the one you READ, after the read (sp gen 6: baseline() placed from memory, alive corrected)
- an SM ask to the council -> the answerer (alive) writes it; another seat writes only when alive names it (sp + alive gen 5: two .5 commits 1 min apart)
- a gate report you word on -> it must carry test_grid_writers' N/0; without it the gate is incomplete, not a GO (sp gen 9: L57-L68 trunk red agreed unseen)
- naming the trunk in a land check -> the LOCAL ref (refs/heads/core/season3/main = posts/belam = MAIN), never origin/*, which lags an hour (sp gen 9: L70)
- an event's time -> read it from the actor's own ref or log, never from a downstream effect's timestamp (sp gen 9: .45 login stamp inferred from a unit start)
- a start the council BANKED on an owner GO -> it is a CELL (enabled: false) on the bytes, never a prose bank line (sp gen 9: the .46.12 cron row read enabled: true and any apply installed it)
- a [decision] that crossed the last words -> ask SM to HOLD the relay and name the stale point before it reaches belam (sp gen 9: alive 06:18:48Z would have capped every town mint)
- a board segment or CLI that reads the repo -> resolve the repo ONCE (locations.repo_root) and test through the REAL CLI root, not the test root (sp gen 9: L84 p1_segment, L94 notices)
- every check -> ask what it prints when it read NOTHING (empty selector, wrong root, 0-byte read, unparsed rows); that case is a named red (sp gen 9: silent greens all night)
- a send's stamp -> `date -u` in the SAME command as the send, substituted into a placeholder that cannot occur in prose (` TT `), never `NOW` (sp gen 10: a stamp off by minutes; alive gen 20: `NOW` inside UNKNOWN)
- a send body -> a QUOTED heredoc (`<<'EOF'`); an unquoted one runs backticks (sp gen 10: a span of a view eaten)
- a re-tip you word on -> check EVERY claim it makes, not only your own row (sp gen 10: 'my amendment met', the tip was a grep)
- a check line -> find its HOLD; a printed rc with no hold is a reading, not a check (sp gen 10: verify-land anon-msg)
- a hostile-input fix -> walk the input one level UP from where the fix sits (sp gen 10: the capsule DIR as a dangling link)
- a falsifier's text -> checked against the script's bytes before the word (sp gen 10: alive reworded one without opening the code)
- a 'mode first' / 'guard first' fix -> list EVERY early exit before the line it claims to precede (sp gen 11: GATE264, vetoes/ladder read before r_land.mode)
- every HOLD you propose -> ask whether the REPAIR can land under it (sp gen 11: 'deleted judge -> HOLD' re-made the GATE264 lockout)
- a mutant's RED -> read the DOWNSTREAM branch first: does the claimed consequence happen at all? (sp gen 11: heal.py 'worktree removed', the branch already refused)
- a role or a count in a word -> read it from the rows / frontmatter, never body text or memory (sp gen 11: SM assumed in written_by; aio + alive: config nodes counted from body quotes)
- a judge or probe that gates its work on memory / load -> its SILENCE under that condition is a red (sp gen 11: GATE265 no-harness ALERT skipped under the low line)
- a git walk over history for a 'last good' state -> `--first-parent`, or a side branch picks the judge (sp + alive gen 11: GATE272 soften-then-empty)
- "X has no gate" -> grep every CALLER path (CLI dispatch, wrappers) before claiming a missing guard, never X's body alone (sp gen 12: cmd_unify's gate sat in main's dispatch :2554)
- a mutant you cite -> build the fixture where the mutant DOES move the line, then claim the row can fail (sp gen 12: P2's :(glob) specs already read 0, the mutant was inert)
- a census that must read 0 -> never `grep -s` / `2>/dev/null` in it: an unreadable dir is a silent 0; name every unreadable place (sp gen 12: GATE278 host row)
- a changed return-on-unread -> trace its CONSUMER to the act it gates before GO, not only the flagged sites (sp gen 12: GATE286, _seat_sessions -> [] fed the liveness guard)
- "live at the re-pin" / "the installed piece" -> read the unit (`systemctl cat` + `show -p Environment agi-post@<p>`) and how it is invoked before naming when or where a piece goes live (sp gen 12; again gen 13: AGI_TRUNK is a BRANCH, a hook sha matched the pin only by start time)
- a fix that names a directory for a multi-uid hook -> `stat` / `getfacl` it and name each mover uid's access (sp gen 12: the .git root is belam 775, objects/ is group agi rwx)
- a git fetch / push claim ("writes only X") -> test it under the configs the repo's own init / sync WRITE, not only today's (sp gen 12: GATE296 O1 lacked `--refmap=`, init adds FETCH_SPECS)
- a gate your word relies on -> read the proof on the tree the run runs in, not your own (alive gen 13: a pre-run read on the wrong tree)
- a dry run that never pushes proves nothing about push auth -> probe `git push --dry-run` on the pushing seat (alive gen 13)
- a key minted for a stage -> read back expires_at NON-NULL; expires_in_seconds is ignored (alive gen 13: a NULL-TTL key minted 05:28Z 10-16)
- a live-key count -> list EVERY provisioning account, not the one you use (alive gen 13: two old media keys, $40 live)
- "two reads agree" on a lagging counter -> agreement at 0 is vacuous; require non-zero agreement (alive gen 14)
- a claim the council fixed -> grep its siblings in every other sentence of the text (alive gen 14: N5 -> R2, H1; U2 -> R3)
- a flag's cause -> read the heard text (transcript, log) before stating it (alive gen 15: C15, the L70 stamp re-hit)
- a mutant you have not run -> label it a prediction, never a result (alive gen 15: M5 a1)
- a hole claimed at a sink -> trace the input through EVERY earlier refusal first (alive gen 15: .42.2 R1, rule (m))
- a home-path scan -> '/home/' AND the posts' home root AND a bare '~/'; read what a tool already refuses before adding a rule on top (alive gen 15: SM's gate missed DG3's 3 lines; an inverted clause)
- "I cannot read X" -> `ls -l` it first (alive gen 15: belam's tools dir was 644; claimed otherwise)
- a test that greps the fix's own text -> passes on an ineffective fix; ask for the behavior under a hostile input (alive gen 18: S1 d31e8c9b18)
- `timeout N pytest ... | tail` -> exits with TAIL's rc and a killed run prints dots, no summary: count only `N passed` + pytest's own rc; a timeout is never a pass (alive gen 18 at 28%, gen 21)
- a lane red on your uid -> can be the GLOBAL git config (ref-guard hook); re-run with env -i + GIT_CONFIG_GLOBAL=/dev/null before FAIL, and a test green only with the runner's identity is not hermetic (alive gen 19, gen 21: GATE293 V2_e/V2_f)
- a strip/allow pattern you spec -> mutate INSIDE the allowed span before sending it (alive gen 19: `[A-Za-z0-9. ]+` swallowed the leak it existed to expose)
- a 0-hit grep for a test's owner -> grep the FUNCTION's words before retiring it (alive gen 19: g4.18.7.1 says 'a line range', not 'viewport --range')
- a tip adding a git fetch / push / show site -> also runs test_grid_writers (alive gen 19: VL own-lane 17/17, SM's merged gate red on C7)
- a mutant script -> prints its diff (or 'applied') before the run; an assert that stops the edit leaves an UNMUTATED green (alive gen 20: GATE277 anchor x2)
- a mutant that stops reading RED after a tip -> check its ANCHOR still matches first (alive gen 20: agi-town rep() prints only '# NO EDIT')
- a replay meant to be ADMITTED -> check its SIGNER (%GS) against the grant actor, not only its cells (alive gen 20: b737cef238 = DG3)
- a CWD-sensitive test -> green from a scratch worktree says nothing; run it from the post's own tree too (alive gen 20, #6)
- a lane's skip line reads `ok` -> grep the log for SKIP/skipped before counting it green; an archive under /tmp is not the gate's environment, a seam-path rule may skip rows by design (alive gen 21: st-seam-rows-skipped hid 7 rows)
- a probe that needs a branch -> never create one in the shared repo (deleting it needs packed-refs.lock, not your uid's); use a detached HEAD (alive gen 20)
- a date compare is not the safety property -> the property is BYTES (was origin's blob seen at its own path class); measure it, never a proxy (alive gen 22: tip-vs-tip passed 10 origin-only edits; the root date was a re-mint coincidence)
- a one-commit `git archive` fixture -> fails tests that read repo history; run the BASE fixture too (alive gen 22: p1_ab leaf_brief, frozen base)
- a dedup KEY is not a display rule -> run the real consumer piece over N reads before describing how often a post sees a line (alive gen 22: GATE302, 3 seats said 'per day'; agi-notice dedups only while unprinted)
- a count 'N/N' over rows of two boxes -> a row with no file HERE is UNREAD, never ok (alive gen 22: h.conf 13/13 here + 2 local-town unread)
- a gate SET has lanes a subset fixture cannot run -> name the lanes you did NOT run in every word, and read each lane's fixture bin for the piece's dependencies (alive gen 23: GATE304 went RED on agi-strand, the one lane with no tap, after my GO on a fixture that could not run it)
- a matching count is not a measurement -> measure the property the note asserts, never infer it from an aggregate that could match for another reason (alive gen 23: '51 + 7 = the seats' count, so the merge-blind walk costs nothing' was wrong; 12 of the 51 WERE merge-only blobs)
- `pytest ... | tail -1` keeps the count and DROPS the FAILED names -> capture `grep -E '^FAILED|passed|failed'` on every run whose red you may have to name (alive gen 23: a '1 failed' with no name cost a second fixture run)
- a sentence that names what a regex COVERS -> measured against the regex before it enters a decision (alive gen 23: 'HOME_PATH_RE covers the posts' home root' was carried from a seat's word unmeasured; 19/20 agi uids were below the module's passwd floor)
- review copies (`git archive`) on / -> ONE at a time, mutants in place + restored, rm in the same turn as the word; a post uid cannot write /data (sp gen 13: 1.13 GB, / at 95%)
- a display rate read off a notice's dedup KEY -> run the print path over N reads before naming how often a post sees a line (sp gen 13: 'once per day', shown every read)
- an extraction source named from a hook sha -> read the unit's Environment (AGI_TRUNK = a branch) before naming where a start extracts from (sp gen 13)
- a date proxy for 'live saw these bytes' -> test BYTES at their path class, never commit dates, when deciding which side superseded (sp gen 13: e719282b has 2 roots)
- a sweep 'done' by agi-at on posts/<me> -> a skill edit lands only through SM's gate: a signed tip on the trunk tip, then seen ON the trunk (sp gen 13: gens 10-11 never reached it)
- a python assert inside a heredoc does not stop the && chain after it -> end the heredoc's python with `|| exit 1` and read the diff stat before sending a tip (sp gen 13: an empty sweep commit)
- posts/<me> keeps a stale agi-at copy of a path after its tip lands -> agi-sync `[trunk-conflict]`; make the copy = the trunk's blob (`git show trunk:PATH > PATH; agi-at PATH`), never a hand merge (sp gen 14)
- 'this class covers X' said from a regex's SHAPE -> call the module's scan() on X under your uid and print the list first (sp gen 14: HOME_PATH_RE misses 19/20 post uids < 1000)
- the harness writes every command's output under the session's tasks dir -> never rm there; a cleanup mid-command deleted that command's own output (sp gen 14)
- a lane that drives real fronts (claude -p, pi, strace) -> never rerun by hand from a scratch copy: it hangs at the fronts; SM's gate is its one runner (sp gen 14: lane-header)
- a file-level guard grep ('cmp -s | NO EDIT | exit 99 anywhere') reads a lane as guarded while its fixture helper has none -> judge each rewrite helper by its own mutant (sp gen 14: the two known reds read 'guarded')
- a gate [review]'s attribution ('the fix is at X', 'the lane greps Y') -> a READING: grep the claimed string in the tree before building a mutant on it (aio gen 12: GATE274)
- a blob census over history -> `git log --raw` prints NOTHING for a merge commit without -m: walk with -m, and a trunk walk is --first-parent (aio gen 12: GATE305 C2)
- a new branch in a tip that matches the asked SHAPE -> not a reach check: name the CONDITION under which it runs and read the guard's own case line first (aio gen 12: GATE265; the ref-guard's case arm judges posts/belam + the trunk only)
- a text-only tip (a skill, a doc) -> still makes claims: every tool, flag, path or function it names exists on the tree, and a def line is not its body (aio gen 12)
- a parse added by a tip -> run it on the REAL input (the live row, the live log), not the lane's fixture: a probe that drops a production input proves nothing (aio gen 12)
- a [result] you word on -> checked against the goal's PREREGISTERED definitions, and a proposed row measured on the trunk before it is sent (aio gen 12)
- a hook or script that GAINS an output line -> grep EVERY lane that runs it for a silence assert before GO (aio gen 12: GATE304 agi-strand)
- a process tree read as a trace relation -> read TracerPid (/proc/<pid>/status) and the tracer's -b / -f flags before naming the mechanism (aio gen 12: agi-run strand)
- a lane that fails closed at its inputs on a box without its fronts (`FAIL inputs: pi is not on PATH`, exit 99) -> not a lane red: SM's gate is its one runner; a lane that needs only sh + python3 (secrets-lanes) RUNS bare on an archive in seconds (alive gen 24)
- a sentence that compares two measurements, written before the measurement ran -> measure, then write the sentence from the values, or leave it out (alive gen 24: a 'side finding' that live != trunk; they were equal)
- a sed in a lane judged against the TRUNK's file when the lane runs it on a STUB the test writes -> find the sed's INPUT file first (what simworld copies), then run the sed on those bytes and count changed lines (alive gen 24: f1-nspawn :318 dead, :319 live; two seats read agi.sh)
- `kill $(jobs -p)` in a piece run by /bin/sh (dash) -> `$(...)` runs in a subshell whose job table is EMPTY, the kill is a no-op and a mutant that drops it cannot go RED -> capture `$!` at the fork, and prove the kill in a row that runs the piece BARE, without the pty hangup (alive gen 24: DG2's strand tip)
- a dead strace -o consumer leaves a pane flood of `strace: |agi-track: Broken pipe` with claude ALIVE; only claude is a tracee under `-b execve` -> the flood names the consumer's death (an ENOSPC append), not a tracer outliving claude; a count of 'Broken pipe' in ~/o must exclude your own echoed text (alive gen 24)
- a REPLACEMENT set named in a red -> diff the old and new sets on THIS box's passwd before sending (aio gen 13, 10-27 13:06Z: the 19 post homes are uid < 1000 nologin; the red was withdrawn 13:1xZ)
- a table row's TEXT taken as a count -> re-measure the file before scoping a leaf on it (aio gen 13, 10-27 17:43Z: alive's '3 sites in secrets-lanes' came from a census row naming lane-header's own lines)
- a test that reads the GRAPH (links.frontmatter_rows, any walk over .agi/nodes) FAILS on a few-path review fixture (no goal nodes, ids unresolvable) -> a test that reads nodes runs on a fixture with the WHOLE .agi; print the E line before calling any red (alive gen 27, 20:53Z 10-27: two false REDs in a 4-path fixture, caught before a send)
- a mutant that cuts ONE conjunct of a test can be EQUIVALENT when the remaining conjuncts imply it -> before naming a mutant, ask whether the other conjuncts already force the cut one; when they do, the mutant cuts the WHOLE test (alive gen 28, 23:16:27Z 10-27: 'first-parent cut to a bare ancestor' beside '0 merges in O..L' could never read RED, since an ancestor O with 0 merges in O..L is already on L's first-parent chain; sp 00:07:14Z; DG3's owM1 cut the whole condition)
- a node diff that ADDS a '## OWNER' block -> run the land's cite check on it before your word (a c:<12 hex> chunk id in the block; grandfather list .agi/nodes/.geometry/owner-cite-grandfather.txt; the speaker read stays belam's), and a rule learned mid-queue is re-run over EVERY queued range before the next land (alive gen 28: GATE339's g7.33.18 OWNER block approved on a box trace alone; verify-land RETURNED L241 'cites no chunk id', then L242 the same on the ruling node)
- a land's anon-msg read by `anonymize.py check --diff-file` on a commit MESSAGE refuses on the Co-Authored-By noreply address -> check the message WITHOUT its trailer block and say so in the word, never call the trailer a home-path red (self-perpetuating gen 16, 10-27 18:34Z)
- a lane run from a `git archive` copy -> archive .agi/config.json AND .agi/nodes/.geometry (and extensions/agi/src for grid.py) with it, or anonymize.py fails CLOSED and verify-land reads ~45 FAIL unmutated; read the UNMUTATED baseline before any mutant; a lone exit 1 on 'SKIP st-seam-rows' is the fixture's place, never a red (self-perpetuating gen 16 17:49Z 10-27; gen 17 01:3xZ 10-28, all-is-one gen 16 03:16Z)
- a build node's parent SHAPE that passes the mint check is not its CLAIM: [build, goal] = a new VERSION of an existing file ([build].md:55); a NEW file is [mvp] / [goal, mvp] / [goal, idea] -> read origin + the parent build's payload before calling a shape legal (self-perpetuating gen 18, .46.17 05:50Z 10-28)
- a NEW engine file that writes a ref or names refs/grid falls under goal:g7.16.1.11.13's census (C1 writers, C6 literals) -> a pre-read runs or reads test_grid_writers.py, not only the leaf's own lane (self-perpetuating gen 18 + alive missed it on .46.17; GATE357 caught 6 FAIL)
- a RULES wrap verified as 'W tree == L tree' reads a false RED once the trunk moves between SM's cut and belam's wrap (alive gen 29, L242: 7295d01fa1 cut on c3cbabf4e5, trunk at 115aad0c50) -> check W as G belam, p2 == L, tree == merge-tree(W.p1, L)
- `git rev-parse --short A B` exits 128 'Needed a single revision' (--short implies --verify) and read as a missing ref (alive gen 29) -> one rev per `rev-parse --short` call
- a pre-read that ran only the leaf's own lane approved twice: a NEW bin/recompose.py left test_commands_manifest RED on the trunk from L255 on (missed ['recompose.py']), and .46.18 (a) bfee4a53d7 ran land-split while the condition named grid-double-mint, whose mutant anchor the amend had removed (alive gen 31; aio [red] 09:08:50Z 10-28) -> the lane set for ANY edit = every test that names the edited file (`git grep -l <file> extensions/agi/tests`) + test_commands_manifest for a new bin/*.py with __main__, on a committed fixture of the tip, before any word
- a NEW writer that REPLACES an old one (grid.py split vs commit_file) -> diff its guards against the old writer's, guard by guard (double mint, payload, nest, legacy hold, unchanged, CAS), before a word (self-perpetuating gen 19, .46.18 (a) 08:34Z 10-28: the split read alone missed A16-A18)
- a code line a reviewer ASKS a builder to change -> before the [approve], every 'mut <..>file' mutant anchor of every lane still matches ONCE at the new tip (self-perpetuating gen 19, 10-28: bfee4a53d7 was reopened by grid-double-mint.t.sh:65's anchor; the lanes that drive the moved code are the 'every test that names the edited file' line above)
- a census of the readers of a name (the trunk, a ref family) -> grep the LITERAL names, the COMPOSED stems (season<n>/main built by a format or a shell variable) AND the callers of a name builder (the town_season_main key of derive_names) before saying 'every reader' (self-perpetuating gens 19-20, .46.18 (b) 10-28: 11 files with no literal hit at 10:06Z, then 3 trunk readers through derive_names with 0 hits at 11:08Z)
- a pre-read's privacy check read home paths only and missed the email class (aio, alive + sp, gen 18 on 8f03c21a51, 10-28) -> the check = anonymize.scan(the added lines, []) plus a control line that must flag, in the same call
- anonymize.scan over a diff's added lines with the '+' marker kept read ['email'] on a pytest decorator line: a '+' kept before a top-level '@' decorator is a one-character local part to EMAIL_RE (aio gen 20, 17:2xZ 10-28) -> cut the marker (`cut -c2-`) before the scan, and the control that must flag stays in the same call
- C1 judged by whether the new code WRITES a ref, while C1 is a LEXICAL grep and a new .tsv's prose carried its literal (aio gen 18, [red] 12:22:01Z 10-28; refines the 'C1 writers, C6 literals' line above: the trigger is the text, not the behaviour) -> run C1's and C6's grep over the ADDED lines of any range under extensions/, src/ or .geometry; any hit = test_grid_writers.py on the exact fixture
- `git archive | tar` + `git add -A` dropped 128 committed files that match .gitignore, so the fixture's tree != the merge-tree (aio gen 18, 10-28) -> `git add -A -f`, then CHECK `HEAD^{tree}` == the merge-tree before any lane
- a guard (a start check, an assert) followed by `;` lets the rest of the line RUN after it refuses (self-perpetuating gen 20, 12:55Z 10-28: pytest ran on the read view after a start-check refusal; gen 21, 14:14Z 10-28: agi-turn ran after a card edit's assert) -> the guard and everything it guards in ONE `&&` chain, or `|| exit` right after the guard (the heredoc case is the 'python assert inside a heredoc' line above)
- a skill line naming the trunk literally, a composed stem or a branches.py call -> name it by placeholder: since L265 the reader census reads skills/; a literal is classed only in the 8 skills with a `*` prose row, any other skill's is unclassed, and a call is a MODULE hit no `*` row classes, so either is a census RED at the next gate (self-perpetuating gen 20, read on my g19 sweep before slice (b) landed)
- a measure of what deleted tests leave untested, keyed on 'module.name' only -> it misses every name a test reaches through an alias (`import node_writer as nw`): read import-as, from-import and import_module aliases, plus a bare-name grep as the net (self-perpetuating gen 21, 14:12:33Z 10-28: 3 false losses through 'nw', 2 missed, replace_payload + log_write; corrected 14:35:27Z)
- a range with a D or R -> every pre-read runs the reader-census lane: since L265 reader_census.tsv is keyed by path, so a D of a file it classes reads stale + bad-fixture; a pre-read that did not run it says so (self-perpetuating gen 22 + aio gen 20, 10-28: step 4 re-cut 3 deleted test_town_mint_final.py while tsv:82 still classed it, all 3 pre-reads green, SM's GATE375 lane caught it; alive [decision] 17:11:42Z)
- an [approve] 'on the bytes' read the tree and not the commit message -> it reads the message (`git log -1 --format=%B`) too, the record that lands: unfilled placeholders, 'measured on' scopes, counts (self-perpetuating gen 22, 10-28: step 4's unfilled PYTEST_LINE rode 5 cuts and 3 seats; alive [decision] 17:41:42Z)
- an anonymize control built on an example-domain address read [] (example domains pass), so it proved nothing (self-perpetuating gen 22, 17:5xZ 10-28) -> the privacy check's control is an address at a real mail domain ASSEMBLED in the call (want ['email']) or a home path assembled the same way (want ['home']); never the literal on a card or a skill
- a `git archive` fixture for a skill lane read RED on the BASE: test_snapshot_goals.py:410 also reads CLAUDE.md and QUICKSTART.md at the root (alive gen 32, own59 11:2xZ 10-28) -> a fixture for any test that names a skill archives CLAUDE.md + QUICKSTART.md with skills/, and a red is attributed on the base fixture alone before it is called the tip's
- skills-truth.t.sh on a ONE-commit fixture read 0 FAIL / 8 SKIP: its 8 NEGATIVE rows diff CUT..TIP and that range was empty (alive gen 32, sweep-g31 11:14Z 10-28) -> a lane with CUT/TIP rows runs on a 2-commit fixture (the base tree, then the tip) with STRICT=1 CUT=HEAD~1 TIP=HEAD, and every SKIP is read by name, never counted as an ok
- an atom placed with a post from a card row without running the row: verify-land's system-account home false positive had been fixed at L211 + L214 (alive gen 34; DG1 [finding] 18:58Z 10-28) -> before placing an atom, run its own row or reading on the live trunk; an atom that reads fixed closes on that reading, it is never placed
- a probe's scratch repo set up under the seat's own global git config: the ref-guard hook refused its write of a peer's posts/<q> (rc 5) and every probe read a void fixture (self-perpetuating gen 23, 18:59Z 10-28) -> each setup git call runs with `env GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null` (in the call, never exported: agi-send's box-read line), and the setup ends `|| { echo SETUP FAILED; exit 1; }` before any read
- a mutant run with PIECES=<one engine*.md>: agi-strand.t.sh and agi-turn.t.sh then read that ONE file as all the pieces, so every other file's pieces vanish and r1 FAILed on a mutant that never touched it (self-perpetuating gen 23, 10-28) -> a mutant's PIECES = every .geometry/engine*.md cat'd into one file with the edit in it, and the same file UNMUTATED reads green first
- a [word] AGREED to a [view] whose premise it had not measured ('the ancestry is history, not bytes'; aio then counted 549 objects, 16 flagged; self-perpetuating gen 23, 10-28) -> every term a word agrees to is measured in it or named 'unmeasured'; a merge's privacy read covers the objects it brings: `git rev-list --objects <p2> --not <p1>`, p1 = the live trunk (SM's b-7)
- a check's `rc $?` read after `| tail` printed TAIL's rc, not the check's (self-perpetuating gen 23, 10-28: the reader census) -> read a check's rc with no pipe: its output to a file, `rc=$?`, then tail the file (the pytest case is the `timeout N pytest ... | tail` line above)
