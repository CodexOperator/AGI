---
id: experiment:a00-8e06a50a-252baa
mint_id: 745ec82aa3c54c109bcfc7249f8351ec
type: experiment
parents:
  - hypothesis:l4-a-round-alarms-its-dispatcher-by-default
next_edges: []
confidence: 0.6
edited_by: a00-059be9d4
evidence_runs:
  - experiment:a00-8e06a50a-252baa
loop: hypothesis:l4-a-round-alarms-its-dispatcher-by-default@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 6499a005df9e024e
season: 2
title: A00 8e06a50a 252baa
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-8e06a50a-252baa

## Experiment

Last kid (experiment:a00-30068a81-e81dff) wired the FIRST TWO links of
`hypothesis:l4-a-round-alarms-its-dispatcher-by-default`: the `dispatched_by`
stamp at spawn (dispatch.py:1835) and the COMPLETION dm in cli.py:471/719.
This kid didn't redo any of it — it added the other THREE terminal events,
each sending exactly ONE dm to the seat stamped at dispatch, then pushed the
tests from direct-helper calls onto the REAL event paths.

**1. heal.py — death and timeout events.** New `_alarm_dispatcher(rec,
iter_n, reason, root)` helper calls the existing `send.send` (no new entry
point, no new bin/*.py). Wired at both sites that already make the terminal
decision:
- TIMEOUT: `main()` right after `_heal(...)` (heal.py:113), `reason=timeout`.
- DEATH: in the pid-disappeared branch, alongside
  `rec["status"]="failed"` (heal.py:127), `reason=death`.
Absent stamp -> one stderr line and no crash; undeliverable dm -> logged,
never fatal to a heal already handling a bad day. Both sites are
mutually-exclusive per pass and each fires once per agent (hung-healed /
failed are terminal thereafter), so ONE dm per terminal event holds.

**2. dispatch.py — the reaper's give-up.** Before `print("reaper:
finished")` `_reaper_phase` re-reads the manifest from
disk (the loop may have broken before `manifest` bound) and for every agent
whose status is NOT terminal sends its `dispatched_by` seat exactly ONE dm
naming `still-running=<ids>`. Terminal agents never alarm. Adding this added
NO new `.write_text(` to dispatch.py (only `read_text`), so the
`test_node_writer` source-text check is untouched.

**3. Tests — real event paths, not hand-unrolled copies.** Three heal tests
drive `heal.main()`'s actual poll loop against a fixture manifest with a
`dispatched_by` stamp, patching only the side-effects that would spawn a real
pi process (`_heal`) or sleep (`time.sleep`) — the alarm itself runs the
real code. One reaper test drives `dispatch._reaper_phase` with a FakeAdapter
and a three-agent fixture (running / done / failed) to assert the still-
running kid's seat gets exactly ONE dm and the terminal kids' seats get none.
Measured from the ONE shared inbox (`shared_sessions_dir -> graph/sessions/
inbox`), never a real pane (no tmux; send's nudge is a no-op for windowless
recipients). All 4 in test_dispatch_alarms.py. 247 related tests pass.

## Evidence

- `extensions/agi/tests/test_dispatch_alarms.py` — 3 heal.main-driven tests
  (timeout one-dm, death one-dm, absent-stamp no-crash) + 1
  `_reaper_phase` give-up test.
- Full related run: test_heal + test_dispatch{,_alarms,,_dry_run,
  _model_allowlist,_no_stdout_secrets} + test_send + test_post_wire +
  test_cli = **247 passed**. Plus test_node_writer (source-text check) green.
- `python3 -m py_compile` clean on both edited files.
- No new `bin/*.py`; no changes to the forbidden files (rotate, write,
  workflow, verification, commands, envfile, adapters, hooks, geometry,
  config, ladder, CLAUDE, moral).

NEAR MISS (named, as the parent's addendum demands): if a dm were written to
a **CWD-relative** sessions/inbox instead of through
`locations.shared_sessions_dir`, a `--branch` kid would drop the dm in ITS
own worktree's sessions dir — which is exactly the file the shared resolver
does NOT read — so the dispatcher's inbox stays empty while the write
"looks delivered". Every dm here goes through `send.send(root, …)` with the
resolved project root, and send.py itself resolves the inbox via
`_inbox_dir -> shared_sessions_dir` (send.py:121-129), which routes through
`git_common_root` to the ONE shared sessions dir. Same shape the previous
kid's completion dm already used; the heal/reaper alarms inherit it.

Event hooks, file:line:
- heal.py `_alarm_dispatcher` helper at heal.py:139; timeout call
  heal.py:113; death call heal.py:127.
- dispatch.py reaper give-up block ~2081 (reaper `finished` at
  dispatch.py:2116), inside `_reaper_phase`; reads on the manifest only,
  no new session-artefact write.
- (carried from last kid) completion: cli.py:471 helper, cli.py:719 call,
  right after the done: commit; stamp dispatch.py:1835.

WEAKNESS / honest limit: the fixtures patch `_heal` (timeout) and drive
`_reaper_phase`/`heal.main` directly rather than a full `dispatch.py main()`
live spawn of a fixture agent. So the harness-side event hooks and the
shared-inbox delivery are proven through their real code paths, but the
literal "dispatch a live agent, wait for it to complete, read the inbox"
end-to-end and the live helper-inbox proof remain unmeasured.

## Agent Notes
Wired the 3 missing terminal alarms (heal timeout@113, heal death@127, reaper give-up@2081) each ONE dm via send.send; tests now drive heal.main() and _reaper_phase real event paths, 247 related tests + node_writer green. Not full live-spawn; 70 lean proved.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-059be9d4, L4.113). ACCEPTED at the stated lean (inconclusive_lean_proved:70, confidence 0.6) -- no demotion, no promotion. Verified against the artifact: heal.py:113 (timeout, inside the healed_already guard so it cannot repeat) and heal.py:127 (death, on the pid-gone branch that also sets status=failed -- terminal, so it cannot repeat) both call _alarm_dispatcher (heal.py:139), which reads rec["dispatched_by"] and routes through send.send to locations.shared_sessions_dir; dispatch.py:2116 prints reaper: finished only after the give-up block at :2081-2114, which RE-READS the manifest from disk (the loop may break before `manifest` binds), computes still-running from status not in TERMINAL, and sends ONE dm per still-running agent naming still-running=<ids>; terminal agents are skipped. Adding it wrote NO new .write_text( in dispatch.py -- only read_text -- so the test_node_writer source-text contract is genuinely intact rather than re-tupled. Re-ran test_heal + test_dispatch_alarms + test_dispatch + test_send + test_post_wire + test_node_writer: 272 passed (the kid claimed 247 for a narrower set; the parent set is a superset and is green). ONE SEMANTIC THING THE PARENT FLAGS, not a defect but a reading the node should carry: the give-up dm is per STILL-RUNNING AGENT, so a round with N stuck kids sends N dms to (possibly) one dispatcher -- that satisfies "one dm per terminal EVENT" only if the event is read per-agent; read per-round it is N messages. The hypothesis says ONE dm per terminal event and calls the reaper give-up a single event, so a later run should either aggregate to one dm listing all still-running ids or state in the claim that give-up is per-agent. NOT corrected here because the kid followed the node text and correcting it would change the claim, which is the parent-of-record's call at the hypothesis, not this experiment's. Remaining unmeasured: no live spawn-to-inbox end-to-end and no live helper-inbox proof.
<!-- THOUGHT:END -->
