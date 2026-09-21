---
id: experiment:a00-33c42478-0c0721
mint_id: d0945722a1f94e38bf812cf385c34371
type: experiment
parents:
  - hypothesis:l3-deep-search-workflow-harness-agnostic
next_edges: []
confidence: 0.85
edited_by: belam-S1-L3-X
evidence_runs:
  - experiment:a00-33c42478-0c0721
loop: hypothesis:l3-deep-search-workflow-harness-agnostic@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: be0f743cc9b8a239
season: 2
thought_session: belam-S1-L3-X
title: A00 33c42478 0c0721
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-33c42478-0c0721

## Experiment

Built and proved the harness-agnostic deep-search workflow registration, additive-only
(touched no rotate/cli/dispatch/zoom). Three artefacts, matching the `review`/`drafting` idiom:

1. `extensions/agi/workflows/deep-search.json` — the stage manifest both harnesses read:
   - `read` — repeat over `lenses` (one reader per lens), renders `{question}`, `{facts}`,
     `{slug}`, `{instruction}`, `{scratch}`; each writes `{scratch}/read-{slug}.json`.
   - `refute` — repeat over `lenses` (one adversarial refuter per lens, DEFAULT TO REFUTED,
     cap `{refute_n}`); writes survivors to `{scratch}/refute-{slug}.json`.
   - `synthesize` — single ranker over `{scratch}/refute-*.json`; merges duplicates, ranks
     survivors, returns `{ranked:[{mechanism,evidence,confidence,fix,red_first_test}],top_mechanism}`.
   Diversity of readers + default-to-refuted refuters preserved as manifest defaults, both
   overridable via `--args`.
2. `extensions/agi/workflows/agi-deep-search.js` — the Claude Code script, matching stage for
   stage; reads every knob (question, facts, lenses, refute_n, scratch, model, effort) from args.
3. `.agi/config.json` → `workflows.deep-search` = `{model: sonnet, effort: high, provider: pi}`.

**No investigation-specific text in either file.** `grep -i -E "worktree|isolation|branch|checkout"`
on both artefacts returns nothing. The question, facts, lens list and refuter count all arrive
through `--args`.

### Proof (a) — dry-run, pi harness
```
$ python3 extensions/agi/bin/workflow.py run deep-search --dry-run --harness pi --args '{"question":"...sublinear in N?","facts":"Measured: per-epoch time grows ~log(N)...","lenses":[{"slug":"scheduler",...},{"slug":"gc",...}],"refute_n":2}'
[dispatch] read:scheduler :: role=reader model=sonnet effort=high
[dispatch] read:gc       :: role=reader model=sonnet effort=high
[dispatch] refute:scheduler :: role=critic model=sonnet effort=high
[dispatch] refute:gc :: role=critic model=sonnet effort=high
[dispatch] synthesize :: role=reviewer model=sonnet effort=high
[summary] workflow=deep-search harness=pi stages=5 ...   (exit 0)
```

### Proof (b) — dry-run, claude-code harness
Same command with `--harness claude-code` → same 5 resolved dispatch lines, exit 0 (the runner
resolves for claude-code and points at `script=agi-deep-search.js`; it never spawns from here).

### Proof (c) — ONE real end-to-end run through the pi harness
Ran headlessly through the harness-agnostic runner (each stage a `pi -p --provider openrouter
--model sonnet` process), question supplied ENTIRELY through `--args` — a real, small, unknown
question about this repo: *"Which function in extensions/agi/bin/write.py is the single entry
that routes a named node operation like `set verdict proved`?"* with two lenses (`entry`, `verbs`),
`refute_n:2`, `scratch:/tmp/agi-deep-search-demo`.

Result: all 5 stages schema-valid; both readers found 5 findings; the two independent refuters
admitted 1 survivor each (killing 9 and 4) and BOTH converged on the same surviving mechanism;
synthesize returned a ranked list whose top mechanism was:
```
{"ranked":[{"confidence":1.0,"evidence":"write.py:297-305 — docstring explicitly states ..."},
 "top_mechanism":"apply_verb(edit, name, args) is the single routing entry ..."}
```
and the runner printed `[summary] workflow=deep-search harness=pi stages=5 all schema-valid`
(exit 0, ~7 min wall).

### Verification the answer was TRUE (workflow found something real)
`sed -n '297,306p' extensions/agi/bin/write.py` shows `def apply_verb(edit, name, args) -> Edit`
with docstring *"Run one named verb. The single entry both callers reach."* and `grep -n apply_verb`
shows exactly one call site (line 617). Both survivors, produced independently and having each
survived adversarial refutation, named the correct function. The converge-and-refute shape works.

## Evidence

- Both dry-runs (a) and (b) above, real commands + real output, exit 0.
- Real end-to-end run (c) above: full per-stage `[dispatch]` / `[ok]` lines and the final
  `[summary] ... stages=5 all schema-valid`.
- Scratch artifacts preserved at `/tmp/agi-deep-search-demo/`:
  `read-entry.json`, `read-verbs.json`, `refute-entry.json` (1 survivor, writes `why_survives`),
  `refute-verbs.json` (1 survivor). Both survivors cite `write.py:297` (apply_verb) with
  confidence 1.0 and independent evidence; each explains why competing candidates
  (main, parse_script, VERBS dict) fail adversarial pressure.
- `grep -i -E "worktree|isolation|branch|checkout" extensions/agi/workflows/deep-search.json
  extensions/agi/workflows/agi-deep-search.js` → no matches (no example hardcoded).
- Repo suite: `python3 -m pytest extensions/agi/tests/ -q` → **2083 passed, 1 skipped**, exit 0.

## Agent Notes
Built and proved deep-search workflow: manifest+js+config row, no investigation-specific text, both dry-runs resolve, one real end-to-end pi run returned a schema-valid ranked list whose top answer (apply_verb write.py:297) verified true in source; 2083 pytest pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-4785dbf3, L3.40): accepted as proved after independent re-verification, not just read-back. Reproduced here: (1) both dry-runs re-run by the parent — 5 resolved dispatch lines each under --harness pi and --harness claude-code, exit 0; (2) grep -i "worktree|isolation|branch|checkout" over deep-search.json and agi-deep-search.js returns nothing — the no-hardcoding property holds; (3) workflows.deep-search config row present; (4) apply_verb at write.py:297-306 confirmed as the single routing entry, so the live run top mechanism was true. Verdict kept at proved because the claims are command-backed, not prose. Weakness recorded in caveat: the live-run evidence lives in /tmp/agi-deep-search-demo scratch, which is ephemeral; the durable evidence is the dry-runs plus this parent re-verification.
<!-- THOUGHT:END -->

REVIEW ACCEPTED — proved stands. Parent re-ran both dry-runs (pi + claude-code, 5 dispatch lines each), confirmed no hardcoded investigation text in either workflow file, config row present, and verified apply_verb/write.py:297 in source. Only weakness: live-run scratch in /tmp is ephemeral. caveat: live-run evidence ephemeral (scratch in /tmp); durable proof is parent-reproduced dry-runs. struggles: kid node initially not resolvable from the main checkout (kid writes into its worktree graph); write.py needed to be run from the worktree root.

PRIME REVIEW NOTE, belam-S1-L3-X, 2026-09-08 — from the first REAL use of this workflow through the unified route, not from reading it.

The owner asked to fix a live grid defect "using workflows, see if it works for us". So the very first customer of `deep-search` was a genuine unknown: the `refs/grid/*` fetch refspec had vanished from `remote.origin.fetch` on this checkout. The workflow was invoked exactly as the owner's rule requires — `workflow.py run deep-search --harness pi --args @file` — with five lenses and refute_n 2. The verdict on the artefact stands: `--dry-run` resolved 11 stages (5 readers, one per lens, 5 refuters, 1 synthesizer) with exit 0 on BOTH harnesses, the `--args` contract held, and nothing investigation-specific is baked into either file. Accepted as `proved` is correct.

TWO LIMITATIONS THAT ONLY APPEAR WHEN YOU RUN IT, and neither is a defect in the kid's work — they are properties of the unified route that nobody had measured because nobody had used it for real.

1. **THE STAGES RUN SERIALLY.** Under `--harness pi` the runner had exactly ONE `pi` child alive at a time (`ps --ppid` on the runner, checked twice several minutes apart). The Claude-Code-native path fans out concurrently; this one does not. For this shape that is the difference between one reader's latency and five readers' latency in series, and deep-search is DEFINED by fanning out over lenses — the whole point of the read stage is that five blind readers look at once. A five-lens investigation that would take one reader's wall-clock takes five. Nothing is wrong with the output; the cost is entirely in time, which is the one budget a director cannot buy more of. Worth a brief: the read stage's agents are independent by construction and should be spawned together, with only the refute stage depending on its own reader and only synthesize depending on all.

2. **WORKFLOW-SPAWNED AGENTS ARE INVISIBLE TO `spawn_budget.py status`.** While this run was live with a `pi` child working, `spawn_budget.py status` showed only the unrelated `--branch` parent and its kid. The workflow path spawns pi directly rather than taking a budget lease. That matters more than it sounds: the round protocol's stop condition, written into HANDOFF.md and used by every prime, is a background loop waiting for `spawn_budget.py status` to reach **0 live**. A prime running a workflow would be told the box is idle while eleven agents were working, and would open the next round on top of them, or rotate believing nothing was in flight. The tree-wide bound in `goal:g4.8` is also not being enforced for these spawns. Either the workflow runner takes leases like every other spawner, or `status` learns to see it — but "0 live" must stop meaning "idle" only sometimes.

THIRD, COSMETIC BUT WORTH ONE LINE: the dry-run prints its stage labels with the placeholder unexpanded — `read:{slug}` five times, `refute:{slug}` five times — so a reader cannot tell the five lenses apart in the dispatch listing. The fan-out itself is correct; only the label is. Fix it where the label is rendered, not by removing the placeholder.
