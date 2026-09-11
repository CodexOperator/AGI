---
id: experiment:a00-90c8724a-f1f27d
mint_id: d59c3d022c7f47a6a2ad0f10811d44de
type: experiment
parents:
  - hypothesis:l4-a-workflow-run-is-named-not-numbered
next_edges: []
confidence: 0.85
edited_by: a00-47db504f
evidence_runs:
  - experiment:a00-90c8724a-f1f27d
loop: hypothesis:l4-a-workflow-run-is-named-not-numbered@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3d2542c7a670a77b
season: 2
title: A00 90c8724a f1f27d
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-90c8724a-f1f27d

## Experiment

Built the claim (hypothesis:l4-a-workflow-run-is-named-not-numbered) in the two
in-scope files, extensions/agi/bin/workflow.py and
extensions/agi/tests/test_workflow.py, then proved it on the built bytes.

### Part 1 — descriptive per-run keynote minting (was NOT implemented)

Added to workflow.py (helpers after `_config_key_for`):
- `_slugify_token` — `SL1#2` -> `sl1-2`, `39` -> `39` (lowercase, non-alnum
  runs to one `-`, collapsed).
- `_run_key_abbrev` — multi-word key to its initials (`merge-up-review` ->
  `mur`); a single-word key (`author`/`validate`/`review`) keeps its whole name.
- `_run_arg_tokens` — scalar/list-of-scalar arg values, deterministically
  ordered; nested dicts (e.g. `targets:[{window:...}]`) contribute nothing.
- `_existing_run_keys` — reads the run_key values already tracked for this
  workflow key (best-effort).
- `_mint_run_key` — abbrev joined to slugged args, de-collided (`-2`, `-3`).

Wired into `run_workflow` (~L1056): mints `run_key = _mint_run_key(root, key,
args)` and prints `[run-key] <key>` FIRST, before any stage output. `_track_run`
gained a `run_key` param and records it in the row **beside** `workflow`
(harness stays in `harness` field). Added a `status` subcommand
(`status_workflow`) that RESOLVES by run_key (or its owning workflow key) from
`.agi/sessions/workflows/*.jsonl`; `list` stays the registry enumeration (the
claim allowed list *or* status to resolve by key).

### Part 2 — author round-trip dropping type/description (confirmed & fixed)

`author_workflow` built a FRESH manifest with no `type` and a hardcoded
description (measured by prime). Now it reads the existing `<key>.json` if
present, carries forward every non-derived top-level field (so `type`
survives), and APPENDS `(<note>)` to the existing description instead of
replacing it when the note is not already present.

### New tests (test_workflow.py)
- `test_mint_run_key_three_shapes` — `mur-39`, `mur-sl1-2`, `author` keeps its
  name.
- `test_mint_run_key_collision_appends_suffix` — `mur-39-3` after two tracked
  rows claim `mur-39`/`mur-39-2`.
- `test_run_prints_run_key_first_and_tracks_it` — a real (mocked-pi) run
  prints `[run-key] review-sl1-2` as the FIRST line and records `run_key` in
  the tracked row.
- `test_status_resolves_by_run_key` — `status_workflow(tmp, "mur-39")` finds
  the row; a key naming no run exits 1.
- `test_author_round_trip_keeps_type_and_appends_note` — re-authoring a
  fixture manifest with `type` + a description carrying `--note X` keeps
  `type` and yields `base description (X)`, not a replacement.

## Evidence

Commands run (repo test file only, kid-tier gate satisfied):

```
cd /home/ubuntu/work/agi/.agi/worktrees/a00-47db504f \
  && env -u TMUX -u TMUX_PANE python3 -m pytest \
       extensions/agi/tests/test_workflow.py -q -p no:cacheprovider
............................................
44 passed in 0.57s        (39 prior + 5 new)
```

All 39 pre-existing tests still green with the new code; 5 new tests added and
passing. `workflow.py validate` unchanged at **7 violation(s)** — the author
fix did not worsen the registry (the pre-existing `<TODO>` skeletons in
l3w-route-probe / l4-plan-research remain). Falsifier satisfied: every minted
key is derivable from workflow type + run args (the 3 claim shapes pass), and
a re-author run no longer loses `type`/description.

## Agent Notes

Honest gaps: (1) there is NO `wf_xxxx` harness run id minted anywhere in this
code path — dispatch mints `iter-NNN`/`a00-…` ids, and `.agi/sessions/workflows/`
is a separate tracking body — so the row records `run_key` *beside*
`workflow`+`harness` rather than beside a real harness id; the harness id
notion is aspirational until a harness actually mints one. (2) `status` was
chosen as the key-resolver (claim permits list *or* status). (3) A single-word
workflow like `author` keeps its name only when args contribute no tokens; with
a scalar arg it becomes `author-<arg>` — reasonable, and no claim shape
contradicts it.

## Agent Notes
Built claim: workflow.py now mints descriptive run keys (mur-39, mur-sl1-2, author) printed first, recorded beside workflow, resolved by new status subcommand with -2/-3 collision; author re-authoring carries type forward and appends note. 44 tests pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-47db504f, L4.282). Verdict left at inconclusive_lean_proved:85, not upgraded to proved. (1) THE INSTRUCTION SAID the claim has two conjuncts: a run key minted from type+args (mur-39) printed first and recorded beside the harness run id wf_xxxx; and author re-authoring carrying type + description. (2) WHAT THE MACHINE ACTUALLY DOES, verified by me on the built bytes, not read off the report: _mint_run_key at workflow.py:170-183 returns mur-39, mur-sl1-2, author for the three claim shapes and mur-39-3 after two tracked rows (run directly, all four OK); run_workflow:1056-1057 mints and prints [run-key] BEFORE any stage output; _track_run:764-784 writes run_key into the row beside workflow and harness; status_workflow:475-512 resolves by run_key. author_workflow:1358-1383 reads existing <key>.json, carries every non-derived field (so type survives) and appends rather than replaces the description. env -u TMUX -u TMUX_PANE pytest extensions/agi/tests/test_workflow.py -q => 44 passed (39 prior + 5 new). workflow.py validate still 7 violations, so the author fix did not worsen the registry. (3) THE NEAR MISS: a key minted from the CONFIG key alone (which is what the code did before, _config_key_for as the tracking key) satisfies the words "the run has a key" while losing the mechanism entirely -- every run of a workflow shares one file and one name, which is the defect (no per-run identity). The kid minted a per-RUN key, not a per-workflow one. (4) DEVIATION FROM THE CHILD VERDICT: kept 85 lean rather than proved because ONE CONJUNCT IS UNMET -- the claim said record the harness id wf_xxxx beside the key, and no wf_xxxx id is minted anywhere in this code path (grep: the only wf_ tokens are the wf_dir variable at workflow.py:643-644). The kid recorded run_key beside workflow+harness and said so in its Agent Notes; the gap is the CLAIM being aspirational about a harness id that does not exist, not a fault in the build. Residue for a later round: either mint a real harness id or drop that conjunct from the claim.
<!-- THOUGHT:END -->

Parent-reviewed L4.282: two conjuncts of hypothesis:l4-a-workflow-run-is-named-not-numbered are built in extensions/agi/bin/workflow.py and proven on fixtures (mur-39 / mur-sl1-2 / author, collision -3, [run-key] printed first, status resolves by key, author carries type + appends note); 44 tests pass, validate unchanged at 7. Left at inconclusive_lean_proved:85 because the claim also asks that the harness run id (wf_xxxx) be recorded beside the key, and nothing in this code path mints one -- run_key is recorded beside workflow+harness instead.
