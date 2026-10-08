---
id: experiment:a00-f2f8465a-b4eb8e
mint_id: e643ea04a513449d9e55938adb40633d
type: experiment
parents:
  - hypothesis:l4-a-parent-with-nothing-left-to-do-does-not-exit
next_edges: []
confidence: 0.8
edited_by: a00-10b3c5f8
evidence_runs:
  - experiment:a00-f2f8465a-b4eb8e
loop: hypothesis:l4-a-parent-with-nothing-left-to-do-does-not-exit@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 1391fed990721351
season: 2
title: A00 f2f8465a b4eb8e
verdict: inconclusive_lean_proved:80
---
# experiment:a00-f2f8465a-b4eb8e

## Experiment

Diagnosed `hypothesis:l4-a-parent-with-nothing-left-to-do-does-not-exit` READ-ONLY
against the two preserved idle-parent artefacts (L4.65 `a00-400db3c3`, pre-`_sibling_session_lookup`;
L4.70 `a00-faa1edba`, post-). No code changed; the preserved worktrees were only read.

**Q3 (where does it stop) — the parent never reaches `cli.py done` at all.**
For BOTH rounds the dispatcher-side parent record (seat-sanctuary-director worktree)
still reads `status: running` with `finished_at` absent, and its mtime equals its
creation time (L4.70 parent record mtime = 07:28 = spawn; parents' rounds were
committed manually by the operator). Since `cmd_done` writes `rec["status"]="done"`
and `finished_at` into the record BEFORE `_auto_commit_worktree` (cli.py: `ap.write_text`
precedes the commit), a `done` that had STARTED would have touched the record's mtime
and left `finished_at`. Neither happened in either round → `done` was never invoked:
not reached-then-failed-inside, not a failed auto-commit.

**Q1 (what was it doing):** it was not progressing. The parents' own `output.log`s are
the 100-byte launch warning (`Model "~z-ai/glm-flash-latest" not found for provider
"openrouter". Using custom model id.`) and nothing more — no tool-call trace, no `done`
summary (the KIDS' logs carry their `cli.py done` output, so the log does capture agent
stdout). No record write, no commit, no exit across the ~20-45 min idle tail. Consistent
with an idle / self-termination-failing parent, not an active-but-erroring one.

**Q2 (did `done` fail, and how):** NO — and this is the decisive negative. I ran the
exact record-resolution `cmd_done` would perform, from each parent's own worktree:
`_resolve_session_record(_session_root(), _agent_path(...))` resolves for both
a00-400db3c3@L4.65 and a00-faa1edba@L4.70 to the seat-dispatcher record, `exists=True`.
At head, a parent's own `done` record IS reachable and `done` would NOT refuse on record
lookup. L4.70 ran AFTER `_sibling_session_lookup` landed and still idled identically to
L4.65 → the session-record/three-tree lookup fix is NOT the cause (same behavior both
times, not different) and is exonerated. The completion-commit path is proven working:
both rounds' kids called `cli.py done` successfully (`status=done`), and the parents'
own records resolve.

**Diagnosis.** The parents demonstrably never reached `done` even though (a) from the
parent's own tree `cli.py status <iter>` printed every kid as `done` (run for both
L4.65 and L4.70), and (b) the parent's own done-record resolves. The poll loop had all
the information needed to terminate and did not. The defect is therefore NOT in the
session-record / commit-signal code (the seam the last three merge-ups worked) — it is
that the PARENT AGENT does not self-terminate its loop. Root-cause class: parent-loop
judgement / weak-model termination, the completion signal being a commit the parent is
forbidden to make and a `done` it never issues. No code fix is in reach; I did not
guess at a repair. The evidence does not support blaming `_sibling_session_lookup`,
`provisioning.py`, `session-complete`, or any edit to an existing test.

## Evidence

Command/output (verbatim, read-only):
- `python3 extensions/agi/bin/cli.py status L4.65` (from worktree a00-400db3c3) →
  `iter L4.65: 2 agents / a00-23a3db9f: status=done verdict=proved pid=1581505 /
  a00-293e8c51: status=done verdict=proved pid=3395636` (exit 0).
- `... status L4.70` (from a00-faa1edba) → `iter L4.70: 1 agents /
  a00-6d441b55: status=done verdict=proved pid=3977541` (exit 0).
- Parent own-record resolution (read-only, via `_resolve_session_record`):
  a00-400db3c3@L4.65 local absent → resolved to
  `seat-sanctuary-director/.agi/sessions/iter-L4.65/a00-400db3c3/agent.json` exists=True;
  a00-faa1edba@L4.70 → `.../iter-L4.70/a00-faa1edba/agent.json` exists=True.
- Parent records: both `status: "running"`, no `finished_at`, mtime = creation
  (L4.70 frozen at 07:28 spawn; parent killed ~08:11). Kids' records live in the
  PARENT worktree — L4.65 both `done proved` (finished_at 1789030106 / 1789032150);
  L4.70 `a00-6d441b55 status=done verdict=proved confidence=0.9 finished_at=1789041061`.
- Parents' `output.log` (dispatcher copies): 100-byte model-warning only.
- Kids' `cli.py done` succeeded (their output.logs echo "`cli.py done` succeeded:
  `agent a00-23a3db9f status=done verdict=proved`").
- Operator's own note (merge70.txt, the round's landing): "Parent a00-faa1edba never
  committed — it sat idle 45 minutes with the work staged, so I killed it, swept twice
  by PID, reviewed the bytes and landed the round on its own branch." — the same
  manual-landing for L4.65.

Caveat: the parents' internal LLM loop transcript is not preserved (only the 100-byte
launch warning), so "it kept polling and never decided done" vs "wedged retrying the
model" is inferred from the frozen record + absent commit + idle trace, not directly
observed. Both readings are "parent does not terminate its own loop"; the exact
internal reason is not pinned.

## Agent Notes
phenomenon real: parent with nothing left to do doesn't exit and never commits (2 preserved rounds).
Root cause: parent never reaches `cli.py done` at all — dispatcher record frozen at running, no
commit, kids already terminal and visible via `cli.py status`. Decisive negative: parent's own
done-record resolves at head (verified both rounds), and L4.70 ran post-`_sibling_session_lookup`
yet idled identically → the session-record lookup fix is exonerated, not the cause. Completion-commit
path works (kids' done succeeded). Defect is parent-agent loop self-termination (LLM judgement),
not the code the last three merge-ups worked.

## Agent Notes
Diagnosed the idle-parent shape read-only: parents never reach cli.py done at all (dispatcher record frozen running, no commit, mtime=creation; kids terminal + visible via cli.py status). Decisive negative: parent own-record resolves at head (both rounds) and L4.70 ran post-sibling-lookup yet idled identically -> session-record fix exonerated. Defect is parent-agent loop self-termination, not the completion-commit code.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-10b3c5f8, L4.75) — accepted as written, verdict held at inconclusive_lean_proved:80. Why this version: the kid answered all three of the hypothesis questions in order with verbatim, checkable artefacts — Q1 from the 100-byte parent output.logs plus frozen dispatcher records (status running, no finished_at, mtime=creation), Q2 as a decisive negative (parent own-record resolves at head for BOTH rounds, and L4.70 ran post-_sibling_session_lookup yet idled identically, so the record-lookup fix is exonerated rather than merely untested), Q3 by timing (cmd_done writes status/finished_at before _auto_commit_worktree, so a done that had started would have left traces; none exist). The kid correctly declined a code fix — the defect it names (parent-loop self-termination, an LLM-judgement failure, not a defect in the seam the merge-ups worked) has no repair within the round constraints, and the hypothesis explicitly made diagnose-without-fix a success. Two things keep it lean rather than proved: the parents internal LLM transcript is not preserved, so idle-polling vs wedged-retry is inferred, not observed; and the conclusion rests on two instances of the shape (n=2). I checked the gates directly: parents link resolves, verdict is in the finite taxonomy, evidence_runs cites this experiment itself (legal — an experiment IS its run). One cosmetic defect: the node carries TWO "## Agent Notes" headings (the kids own note plus the --notes injection); harmless to readers but a writer-side dedupe would be nicer.
<!-- THOUGHT:END -->
