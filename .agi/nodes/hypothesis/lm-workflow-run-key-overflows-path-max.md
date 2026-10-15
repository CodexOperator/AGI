---
id: hypothesis:lm-workflow-run-key-overflows-path-max
mint_id: 07a2331a0c82463096dd5723f8fbe623
type: hypothesis
parents:
  - idea:engine-tests
next_edges: []
ceiling: 0 USD; local pytest only; engine-file edit under extensions/agi/bin/, not a dispatched round
edited_by: director-thought
falsifier: a run_key over 300 bytes still throws on mkdir after the fix, OR two distinct long run_keys sharing a 190-byte prefix collide on the same truncated directory (digest collision), OR the descriptive run_key returned by _mint_run_key changes (regression in citing/tracking).
scaffold_hash: 9eb08d78df96eac4
season: 2
testable_claim: "extensions/agi/bin/workflow.py _persist_stage_value(root, run_key, label, value) uses run_key directly as a directory name under sessions/workflows/runs/. A run_key over 255 bytes UTF-8 (measured: brainstorm idea id plus full why sentence plus max_hypotheses, slugged) causes os.mkdir to raise OSError File name too long, caught by a bare except Exception, so label.json is never written and the stage falls back to the 200-char in-process preview. Claim: bounding only the path COMPONENT (truncate plus sha256 digest suffix) at the mkdir call site fixes persistence without changing the descriptive run_key used for reporting/citing elsewhere."
tests: pytest extensions/agi/tests/test_workflow.py -k run_key_path_component or persist_stage_value; plus the full extensions/agi/tests/test_workflow.py suite for no regression
title: "workflow.py run_key overflows the filesystem path_max: a long why/args blob in a brainstorm call mkdirs a directory name past 255 bytes, mkdir throws File name too long, the broad except swallows it, and the stage structured return is silently lost"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:lm-workflow-run-key-overflows-path-max

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
"Found live, gen 7: the gen-6 jev brainstorm run (idea:lm-why-jev-echoes-leaked-verdicts causes 2-4) logged both its brainstorm and refute stages as recorded unstructured despite committing 5 well-formed hypothesis nodes (453445d60), verified against the actual node diffs. Root-caused to this mechanism by reading _mint_run_key/_run_arg_tokens/_persist_stage_value directly. sanctuary-master confirmed by DM this is a known bug class (SM.125 path_max, alongside config_max/template_max) and asked it be routed as a normal TM node with tests plus mur verdict, delivered to thought-master by merge-up, never pushed to core/season2/main directly -- which is what this node is."
<!-- THOUGHT:END -->
