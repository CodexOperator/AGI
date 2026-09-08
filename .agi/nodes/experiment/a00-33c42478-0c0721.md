---
id: experiment:a00-33c42478-0c0721
mint_id: d0945722a1f94e38bf812cf385c34371
type: experiment
parents:
  - hypothesis:l3-deep-search-workflow-harness-agnostic
next_edges: []
confidence: 0.85
edited_by: a00-4785dbf3
evidence_runs:
  - experiment:a00-33c42478-0c0721
loop: hypothesis:l3-deep-search-workflow-harness-agnostic@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: be0f743cc9b8a239
season: 2
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
