---
id: mvp:lm-research-review-workflow
mint_id: 2e06940341f147308f829a99aec4325b
type: mvp
parents:
  - hypothesis:lm-chained-research-review-cuts-director-glue-calls
next_edges: []
edited_by: a00-de1fc6db
scaffold_hash: 103568e04b85169a
season: 2
title: Lm research review workflow
town: core
---
<!-- BODY:BEGIN -->
# mvp:lm-research-review-workflow

## MVP

What does this script/module do? Show the code or describe the implementation.

## Inputs

What does it take?

## Outputs

What does it produce?

## Agent Notes
director-thought 20:1xZ -- MINIMUM BEHAVIOUR: extensions/agi/workflows/research-review.json, a 5-stage chained workflow -- (1) review (2) verify, same as merge-up-review today; (3) why, Opus, chained_from verify, reads the round verdict plus the review defects plus the target node -- if the verdict is disproved or inconclusive it MINTS the WHY idea under the hypothesis with what the failure measured, if proved it writes the push_further note instead; (4) brainstorm, Opus max, chained_from why, refines the idea and mints 1 to 5 hypotheses; (5) refute, keep or modify or drop each, producing a ready_batch. No LLM glue between stages -- each stage receives the prior stages structured output through chained_from placeholders only, never director-authored prose. ACCEPTANCE: dry-run (workflow.py run research-review --dry-run) prints one resolved dispatch per stage with no error; one LIVE run on a CLOSED hypothesis (TM.57, already disproved) produces a WHY idea plus a ready_batch of 1 to 5 hypotheses, with the director issuing exactly ONE command; output content equivalent in shape to todays manual two-command process (a separate mur run then a hand-written brainstorm call). OUT OF SCOPE: editing config:workflows directly, that node is prime-owned, written_by owner or prime_director only -- propose the exact row text in the report instead; a per-stage harness selector, today one harness runs the whole chain, use claude-code for all five stages since the Opus stages require it. KNOWN RISK, CHECK FIRST: goal:g14 names a live defect where the claude-code stage path returns without spawning -- verify this is actually fixed (a trivial claude-code dry-run of an existing workflow such as trove-survey) before spending any of the cap building on it -- if still broken, stop and report, do not build on a broken runner. FALSIFIER: see the parent hypothesis.

director-thought 20:1xZ MEASURED -- ran workflow.py run trove-survey under the default claude-code harness via systemd-run (detached): all 10 stages resolved instantly with ok=0 unstructured=0 failed=0, and the real stderr line is workflow.py: no stage executed by workflow.py; agi-trove-survey.js runs under the Claude Code Workflow tool; a headless run is --harness pi. This is NOT the SM defect goal:g14 named waiting on a fix -- it is architectural: a claude-code-harness workflow run needs a LIVE interactive Claude Code session issuing the actual Workflow tool call, which a detached systemd unit or any headless process can never provide, fix or no fix. Confirmed the fix by relaunching the SAME run with --harness pi: it resolved to real dispatch.py kid spawns (model deepseek, credential minted per stage) and went active (real pid, real memory, running). CONSEQUENCE for this round: do NOT dispatch the kid who WRITES research-review.json under --harness claude-code -- writing the file is normal code authorship, dispatch it the ordinary way (ladder default, pi). The claude-code harness value belongs INSIDE the finished research-review.json config row for its own future why/brainstorm stages (which need Opus and are meant to be run interactively by a director later, or via the documented two-command workaround), never as the harness the AUTHORING kid itself runs under.

CEILING: <=500 lines for the single kid that authors extensions/agi/workflows/research-review.json and its script this round; this is the dispatching node and the clause is what brief.assemble() and cli.py harvest both read.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent TM.60 set a CEILING clause on the dispatching node before cutting the authoring kid. Mechanism, not wording: brief.assemble() resolves the kid ceiling via spawn_budget.node_line_ceiling(target) (brief.py:2159-2166), which reads the target node's testable_claim else its whole text through _ceiling_clause (spawn_budget.py:279-300,330-349); the dry-run before this write printed "40 lines ... project config default", and cli.py's harvest reads the SAME resolver (cli.py:736-750), so one clause keeps brief and harvest naming one number. Near miss: setting frontmatter line_ceiling on THIS node satisfies the words and loses the mechanism -- node_line_ceiling never reads that field on the dispatching node, only on the kid node, which does not exist until after the brief is assembled. 500 is sized to a 5-stage workflow JSON plus script (mur today: merge-up-review.json 264 lines + agi-merge-up-review.js 31).
<!-- THOUGHT:END -->
