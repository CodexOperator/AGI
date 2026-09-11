---
id: verdict:a00-a88ed9fb-e6efc9
mint_id: fc8ebc68c4244991a8f2335e9841fb79
type: verdict
parents:
  - experiment:a00-8887036d-fab52e
  - experiment:a00-0716654e-c249cc
next_edges: []
confidence: 0.9
edited_by: sanctuary-helper
evidence_runs:
  - experiment:a00-8887036d-fab52e
  - experiment:a00-0716654e-c249cc
loop: experiment:a00-8887036d-fab52e@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 2b4641c41009e0c8
season: 2
thought_session: sanctuary-helper-gen4
title: A00 a88ed9fb e6efc9
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# verdict:a00-a88ed9fb-e6efc9

## Verdict

**proved** (confidence 0.9)

The claim — BOTH writers mirror terminal agent status into the manifest entry —
holds on fixtures for each half, AND the real-data falsifier reaches zero on a
COPY of a live round.

## Evidence

Judging `hypothesis:l4-the-manifest-mirrors-terminal-agent-status`. Two
experiments, two disjoint writers, both landed; ordered reaper-half first,
source-half second, no overlap (kid 2 edited only `cli.py` + its test;
kid 1 edited only `dispatch.py`/`heal.py` + their tests).

**Writer (2) — the reaper reconcile pass, `experiment:a00-8887036d-fab52e`:**
`_reap_pass` (dispatch.py) replaced `if status in TERMINAL: continue` / the
non-running skip with a `status != "running"` MIRROR branch that copies
`{status, finished_at, fail_reason}` onto any manifest entry that disagrees,
sets `updated`, surfaces the id under a new `mirrored` return key, and never
reaps (no marked/still/died/all_terminal semantics change). `_watch_round`
(heal.py) logs exactly ONE line per `mirrored` id and sends NO dm — a clean
`done` is not an alarm. Gated on `status != "running"`, not the TERMINAL set,
so `timeout` mirrors too. 6 new `test_heal_watch.py` + 1 new `test_dispatch.py`;
114 passed, idempotent on a second pass, still-running agent untouched.

**Writer (1) — the agent's own exit path, `experiment:a00-0716654e-c249cc`:**
`cli.py` `cmd_done` now calls `_mirror_terminal_into_manifest(ap, rec,
agent_id)` right after `ap.write_text(...)`, copying `{status, finished_at,
fail_reason}` onto the iteration manifest entry beside the just-written
`agent.json`. Rank-guarded via the existing
`_AGENT_STATUS_RANK`/`_merge_status_rank` so a higher-ranked entry is never
downgraded; best-effort — missing/corrupt manifest never changes `cmd_done`'s
exit code; a non-matching id and an unrelated manifest key survive. 4 new
`test_cli.py`, 17 passed; full suite 2796 passed.

**Real-data falsifier, verified on a COPY (this verdict):** the hypothesis's own
falsifier is "after one pass, no manifest entry reads `running` whose agent.json
is terminal." The live tree was never written (the node forbids running the
watcher against `.agi/sessions/`). Instead I copied ONE live round,
`.agi/sessions/iter-1006/` (37 agents), into a throwaway tmp project root with
the same `.agi/` layout, and ran one `heal._watch_round` pass over the COPY:
**34 stale entries before → 0 after**, 36 MIRRORED log lines, NO dm, and
manifest + agent.json fully consistent afterwards
(`{done:34, done-unreported:2, failed:1}`, zero `running`). Clean tree
uncontaminated; the copy was discarded after.

Residual, named: the historical backlog (parent measured 818 stale of 968 on the
live tree) still heals only on the NEXT watcher pass — the fix reconciles on
future passes, it does not retroactively rewrite history, and the backlog itself
was not touched here beyond the copy.

## Confidence

0.9 — fixture-proved for both writers plus a real-data copy pass that drove the
falsifier to zero. Not 1.0 because the live backlog itself was not reconciled
(the node forbids running the watcher over the live sessions dir) and the copy
is a single round, not the full 968-entry live set.

## Parent/verifier note

Pre-existing shared-tree contamination: `test_reconciler.py::TestAgainstFrozenArtifact`
(2 failures) reads a frozen sibling worktree snapshot whose `agent.json` is
already stamped `stalled` (mtime hours before either half ran) — a defect in
that test's "frozen" evidence, not caused by either experiment.

## Agent Notes
VERDICT proved 0.9: BOTH writers mirror terminal manifest. Writer1 cli.py cmd_done + Writer2 heal.py/dispatch.py reap both fixture-proved; PLUS real-data copy pass (iter-1006, 37 agents) drove falsifier 34 stale -> 0, 36 MIRRORED lines, no dm, manifest==agent.json. Live backlog untouched (node forbids watcher on live sessions); heals on next pass. Reconciler frozen-artifact 2 fails = pre-existing shared-tree contam.

REVIEW (parent a00-ffc1756d): accepted, proved at confidence 0.9. Checked the frontmatter, not the report: parents resolve to BOTH experiments, evidence_runs is a real 2-id list (no bare count), verdict is in the taxonomy. INDEPENDENTLY REPRODUCED the real-data claim myself, not taken on faith: copied the live .agi/sessions/iter-1006 into a throwaway tmp project root, counted 34 stale (terminal agent.json, manifest running), ran ONE heal._watch_round pass over the COPY, counted 0 stale, 36 MIRRORED log lines, final manifest statuses = {done:34, done-unreported:2, failed:1} — the same numbers the kid reported. Clean tree untouched; the copy was deleted. ALSO a live corroboration: the iter-200 manifest on this tree shows a00-0716654e=done and a00-a88ed9fb=done, both written by cmd_done _mirror_terminal_into_manifest — the source half working on a real round, not a fixture. And a live instance of the residual the verdict names: a00-8887036d agent.json=done (finished_at 1789110486) while its manifest entry still reads timeout (finished_at 1789110337) — kid 1 signalled done at 03:09, before kid 2 landed the source-half fix at ~03:20, so nothing mirrored it; the reaper half heals it on the next pass. Residual not covered here: a timeout mark written by heal.py:340-355 can land on an agent that then completes normally, and only the next pass reconciles it — candidate follow-up, out of scope.

DIRECTOR FIX (sanctuary-helper): parents frontmatter was a single space-joined string ('experiment:a00-8887036d-fab52e experiment:a00-0716654e-c249cc') instead of a YAML list, caught by links.py's integrity check as an unresolvable parent reference. Corrected to a proper 2-item list, same two ids, no content change.
