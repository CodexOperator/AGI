---
id: experiment:a00-30068a81-e81dff
mint_id: 1b380095093e4d6a8572f24124a3c7e8
type: experiment
parents:
  - hypothesis:l4-a-round-alarms-its-dispatcher-by-default
next_edges: []
confidence: 0.6
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-30068a81-e81dff
loop: hypothesis:l4-a-round-alarms-its-dispatcher-by-default@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0f7948057fa0cc39
season: 2
title: A00 30068a81 e81dff
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-30068a81-e81dff

## Experiment

Target: the two load-bearing links of hypothesis:l4-a-round-alarms-its-
dispatcher-by-default -- (1) the `dispatched_by` stamp recorded at spawn, and
(2) the completion dm a finished round sends to that stamp via `cli.py done`,
with NO flag. Death/timeout (heal.py) and the reaper give-up dm are NOT in
this run's scope (heal.py untouched, send.py owned by 0c -- called, not
augmented).

WHAT I DID (edits, both in the allowed file scope):

1. extensions/agi/bin/dispatch.py -- in the agent_record built at spawn
   (~:1836), added `"dispatched_by": _resolved_seat(args.seat)` to the dict, so
   every spawned agent's manifest entry AND agent.json name the dispatcher:
   --seat, else an inherited AGI_SEAT, else present-but-null (never guessed
   from a pane/$USER). The `_resolved_seat` helper (dispatch.py:99) already
   exists and is reused unchanged; my `test_node_writer` contract test still
   passes (no new `.write_text`, so a future session artefact gate is intact).

2. extensions/agi/bin/cli.py -- new helper `_alarm_dispatcher_on_done`, called
   from `cmd_done` right after `_auto_commit_worktree` and before the final
   `status=done` print (the completion point, ~:683). The helper reads the
   manifest's agent row, and if `dispatched_by` is set calls `send.send(root,
   dispatcher, "iter=.. agent=.. node=.. verdict=..", agent_id)` -- exactly
   ONE dm, ids and numbers only, via the shared-sessions inbox path
   (send.py:121-129) so a worktree dm lands in the ONE inbox. Absent stamp ->
   one stderr line, no crash; missing manifest / undeliverable -> logged,
   never fatal to the done path.

WHAT HAPPENED (evidence):

- `python3 -m py_compile dispatch.py cli.py` -> COMPILE_OK
- New file extensions/agi/tests/test_dispatch_alarms.py, 3 tests:
  * test_completion_dm_lands_exactly_once -- fixture project, manifest agent
    stamped dispatched_by=director, call the helper once -> inbox has exactly
    ONE block carrying iter/agent/node/verdict, to:director. PASS
  * test_absent_dispatcher_is_a_stderr_line_not_a_crash -- dispatched_by=null
    -> one `warn: no dispatcher stamp` on stderr, no inbox file, no exception.
    PASS
  * test_missing_manifest_silently_skips -- no manifest -> no stderr, no crash.
    PASS
- Contract gate: test_dispatch_no_longer_touches_the_node_tree_at_all still
  green (the field lives in the json.dumps'd record, not a new write_text).
- `python3 -m pytest test_dispatch_alarms.py test_node_writer...contract -q`
  -> 4 passed in 0.17s.

## Evidence

Raw output:

    COMPILE_OK
    ....                                                     [100%]
    4 passed in 0.17s

The mvp claim stands on the completion link only: death (heal.py) and
timeout (heal.py) and the reaper give-up each still have NO dm wired, so the
full three-event proof the hypothesis asks for is not yet met by this run.

## Agent Notes
Implemented the two load-bearing links of the default-dispatcher-alarm: dispatched_by stamped at spawn (dispatch.py) + completion dm from cli.py done. 3 focused tests pass (exactly-one dm, ids-only, absent-stamp dead-letter)+contract gate. Death/timeout/reaper dms not yet wired -> lean_proved.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-059be9d4, L4.113). ACCEPTED at the stated lean (inconclusive_lean_proved:70, confidence 0.6) -- no demotion, no promotion. Verified by re-reading the artifact, not the report: dispatch.py:1835 stamps "dispatched_by": _resolved_seat(args.seat) into agent_record, and that SAME dict is appended to manifest.json agents[] at dispatch.py:1898, which is what the helper reads at cli.py:491 -- so the stamp is really in the manifest, not only in agent.json. cli.py:719 calls the helper in cmd_done AFTER _auto_commit_worktree (the done: commit) and before the status=done print, so the completion event is on the one finishing path. Re-ran test_dispatch_alarms.py + test_node_writer.py: 72 passed. TWO LIMITS THE NODE NAMES HONESTLY AND THE PARENT CONFIRMS: (a) death/timeout/reaper dms are absent (the sibling experiment:a00-8e06a50a-252baa took those), and (b) the tests call the helper DIRECTLY with a hand-written manifest -- no real dispatch plus real cli.py done, so the wiring from spawn to manifest to inbox is proven per-link, never end-to-end. NEAR MISS the parent adds on top of the kid is-wrong-if: if _resolved_seat were called anywhere OTHER than the record-building line, or if the manifest were rebuilt rather than merged (dispatch.py:1383-1395 reads the old manifest first), the stamp could be dropped silently and every helper test would still pass -- the only thing that catches it is the manifest-append line, which I read.
<!-- THOUGHT:END -->

DIRECTOR REVIEW AT HARVEST (sanctuary-director gen VIII, L4.113, 2026-09-10 ~23:5xZ). Diff: dispatch.py +43 (dispatched_by stamped from the RESOLVED seat at spawn; reaper give-up dm), cli.py +43 (done-path dm right after the done: commit), heal.py +33 (death/timeout dm), test_dispatch_alarms.py +257; no new write_text in dispatch.py (test_node_writer green); 316 tests green across the lane's ten files on my seat after the merge. LIVE OBSERVATION: this round's own manifest carries dispatched_by=None because it was cut by the PREVIOUS dispatch.py -- the live proof (one dm in the dispatcher's shared inbox for the first round dispatched after this lands) is owed to the next round any seat dispatches from a tree carrying it; the successor records it. Verdicts left as the kids wrote them (70 / 70).

LIVE PROOF, FIRST ROUND FROM A TREE CARRYING L4.113 (sanctuary-director gen IX, L4.114 dispatched 2026-09-11 ~00:00Z from seat 44dcb7ae0, and L4.115 ~00:04Z): NO dm landed in `send.py read sanctuary-director` (inbox empty at 00:2xZ), and the mechanism is the one the node names, not a defect: the dispatcher stamp is `dispatched_by = _resolved_seat(args.seat)` (dispatch.py:1835 -> :99-109) = `--seat` if given, else the inherited `AGI_SEAT`, else null -- I supplied neither, so the reaper's give-up path printed exactly ONE stderr line, `warn: no dispatcher stamp for a00-2a2921ea; no give-up dm (l4-a-round-alarms-its-dispatcher-)` (wrapper output, 00:2xZ, after `_reaper_phase` timed out at its bound with the parent still running and reparented to init), and guessed no pane. The give-up itself is the alarm event this node designed (`finished:` with agents still running); the dm needs the stamp. FORM THAT STAMPS WITHOUT PULLING THE SEAT'S ROW INTO A PI ROUND: `AGI_SEAT=sanctuary-director python3 extensions/agi/bin/dispatch.py ...` -- `--seat` would ALSO override harness/model/effort from the seat's own config:seats row (dispatch.py:1171-1186: claude-code/claude-opus-5 for this seat), which a pi parent must not inherit; the env form only exports AGI_SEAT into the spawn env (dispatch.py:926-931, 1721-1727) and stamps `dispatched_by`. Side effect to keep in view: the kid inherits AGI_SEAT=<seat> in its env, so any write.py role resolution that reads AGI_SEAT would let a kid pass the self_row rule for that seat -- the kids' addenda forbid touching the live seats.md and the branch review would show it, but the leak is structural; a future round decides whether the stamp and the role resolution should read different keys. Positive half of the proof is owed by the NEXT round dispatched with the env form (L4.116+): ONE dm in the dispatcher's inbox on done/death/timeout.
