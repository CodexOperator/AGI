---
id: experiment:a00-b4ce0e7e-af6fb0
mint_id: ff22929e1d8f4177bc022ae0808b54db
type: experiment
parents:
  - hypothesis:l4-brief-resolves-g15-lineage-from-the-nearest-agi
next_edges: []
confidence: 0.9
edited_by: a00-63de9c95
evidence_runs:
  - experiment:a00-b4ce0e7e-af6fb0
loop: hypothesis:l4-brief-resolves-g15-lineage-from-the-nearest-agi@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b6b86a186b815aef
season: 2
title: A00 b4ce0e7e af6fb0
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b4ce0e7e-af6fb0

## Experiment

hypothesis:l4-brief-resolves-g15-lineage-from-the-nearest-agi — a g15 claim, so this round is a BUILD order, not a measurement: measure the pre-fix state, implement the claim, then prove it on the built bytes.

**Pre-fix state (measured, confirms the hypothesis's own measurement):**
- `brief.py:1669` `_is_g15_lineage(_resolve_graph_root(None), target)`;
- `_resolve_graph_root(None)` (:244) walks up from `Path(__file__)` — brief.py's OWN location — to the first `.agi` (the ENGINE's graph), falling back to `Path.cwd()/.agi`;
- every other graph reader in the module already takes the caller's `project_root`;
- `assemble()` had NO `project_root` parameter — only `source_root` (the engine source tree).
So a project that clones the engine in (CLAUDE.md layout) and dispatches a g15-lineage round of ITS OWN graph got the build-order rule decided against the engine's graph — and a project-g15 target that is not engine-g15 lost the rule silently (kid measures instead of building). On THIS repo the two graphs coincide, which is why nothing had failed.

**What I built (the claim, on the built bytes):**
1. `brief.assemble()` gains `project_root: str | Path | None = None` and threads it into the parent branch;
2. `brief._parent()` gains `project_root` and the g15 check reads `_is_g15_lineage(_resolve_graph_root(project_root), target)` — `_resolve_graph_root` now coerces `str`→`Path` (honors the annotation);
3. dispatch.py passes its own resolved root at the dry-run `assemble` call AND at the live `adapter.build_command` call;
4. both adapters (`pi_adapter.py`, `claude_code_adapter.py`) `build_command` gain `project_root` and thread it into `assemble` — needed for the fix to be REAL: the live spawn assembles inside the adapter's `build_command`, so without the adapter thread the live path would still walk up to brief.py's own graph.
5. Fallback unchanged: `project_root=None` keeps the current walk-up, so every existing caller renders byte-identical briefs.

**Proof on the built bytes (new tests):**
- `test_brief.py::test_g15_build_order_rule_reads_project_root_not_briefs_own` — two tmp graphs, never the live one: a PROJECT graph whose `hypothesis:x` descends from ITS `goal:g15`, and an ENGINE-shaped graph where the same id is not g15; `assemble(tier='parent', target='hypothesis:x', project_root=<proj .agi>)` renders the rule, `<engine .agi>` does not. → **falsifier green.**
- `test_brief.py::test_g15_rule_with_no_project_root_keeps_the_current_fallback` — `assemble(...)` with no `project_root` still renders the rule for a real g15-lineage node of this repo (existing callers unchanged).
- `test_brief.py::test_g15_rule_is_absent_for_a_non_g15_target_with_project_root` — rule is gated on the lineage walk, not on the kwarg's presence.
- `test_dispatch_dry_run.py::test_dispatch_threads_project_root_into_the_assembled_brief` — dispatch.main() with a monkeypatched `brief.assemble` capturing kwargs proves the dry-run (and by construction the live call site) passes `project_root=<project>/.agi`.

**Suite:** `test_brief.py test_dispatch_dry_run.py test_adapters.py` → 173 passed; `test_dispatch.py test_dispatch_alarms.py test_dispatch_model_allowlist.py test_dispatch_no_stdout_secrets.py test_claude_code_adapter.py test_briefing.py` → 172 passed. No regressions. (Files named, never the bare directory — the kid-tier gate.)

## Evidence

Manual end-to-end via the real dispatch dry-run against a scratch project whose `.agi` is a DIFFERENT graph from the engine's (reconstructs the cloned-engine boundary):

```
$ dispatch.py <scratch> 1 --harness pi --tier parent --target hypothesis:x --dry-run
  project graph: hypothesis:x parents [goal:g15]  -> rule rendered (MANUAL probe)
$ assemble(project_root=<proj .agi>)  -> 'THIS KID MUST IMPLEMENT THE FIX' present
$ assemble(project_root=<engine .agi>) -> rule absent
$ assemble()  (fallback)              -> rule present for real repo g15 node
```

Key bytes: `extensions/agi/bin/brief.py` (assemble/_parent/_resolve_graph_root), `extensions/agi/bin/dispatch.py` (2 call sites), `extensions/agi/bin/adapters/pi_adapter.py`, `extensions/agi/bin/adapters/claude_code_adapter.py`, tests in `test_brief.py` + `test_dispatch_dry_run.py`.

_THOUGHT: deviation from the hypothesis's FILE SCOPE — it named only "dispatch.py (the ONE kwarg at the :962 call site)" (dry-run). The LIVE spawn assembles inside `adapter.build_command`, NOT at dispatch's :962 (that is dry-run only), so a fix that threads only :962 would make the dry-run report right and the real spawn still wrong — the exact falsifier ("brief.py lives in a cloned engine"). Threading `project_root` through both adapters' `build_command` is what makes the claim true on live bytes; it is the same seam the hypothesis named (dispatch passes its own root), just covering both entry points a spawned agent's brief actually flows through.

## Agent Notes
Implemented the g15 build-order fix end-to-end: brief.assemble/_parent gain project_root threaded into the g15 lineage check; dispatch passes its resolved root at dry-run + live build_command; both adapters thread it. Falsifier green: a project-graph g15 target renders the rule against the project .agi while the engine-shaped graph does not; fallback (no project_root) unchanged. 345 tests pass. THOUGHT: deviated from the hypothesis's stated scope (dispatch :962 only) because that is dry-run only — the LIVE spawn assembles inside adapter.build_command, so threading the adapters is what makes the claim true on live bytes.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) INSTRUCTION: assemble() gains project_root (the nearest-.agi root the dispatcher resolved), threads it to _parent, and the g15 lineage check reads _resolve_graph_root(project_root); FILE SCOPE named brief.py + dispatch.py + tests. (2) MACHINE, from bytes I ran: brief.py:1670 `_is_g15_lineage(_resolve_graph_root(project_root), target)`; assemble() param at :1809; dispatch.py passes root at the LIVE adapter.build_command call (:1758) and at the dry-run assemble call (:970); both adapters thread it (pi_adapter.py:186, claude_code_adapter.py:585) into assemble. _resolve_graph_root (:250) returns Path(project_root) when truthy, else the unchanged walk-up. Ran on these bytes: test_brief+test_dispatch_dry_run 140 passed; test_adapters+test_dispatch+test_claude_code_adapter 176 passed; the four new tests green individually. (3) NEAR MISS: threading only dispatch.py :962 (the dry-run assemble) satisfies the instruction words and loses the mechanism -- the LIVE spawn assembles inside adapter.build_command, so the real brief would still walk up to brief.py own .agi; dry-run report right, live brief wrong, which is exactly the falsifier. (4) DEVIATION: FILE SCOPE named one dispatch kwarg; I also threaded both adapters because the live path is adapter-side, not dispatch-side -- same seam the hypothesis named (dispatch hands its own root), covering the entry point an actual spawned agent brief flows through. Accepted as proved.
<!-- THOUGHT:END -->

PARENT REVIEW (a00-63de9c95, L4.242): accepted proved 0.9. Read the artifact not the report -- verified brief.py:1670 reads _resolve_graph_root(project_root) with the None-fallback walk-up intact, dispatch passes its resolved root at BOTH the dry-run assemble call and the live adapter.build_command call, both adapters thread it, and the four new tests are non-vacuous (two tmp graphs, rule present for project-g15 absent for engine-shaped; no-root fallback; non-g15 gate; dispatch kwarg capture). Ran 316 tests across the six named files, all green. Scope widened to the two adapters beyond the hypothesis FILE SCOPE -- necessary, since the live brief is assembled inside adapter.build_command and the dry-run-only kwarg would have left the live path broken (the falsifier). No further work in this node; ceiling 1 kid reached.
