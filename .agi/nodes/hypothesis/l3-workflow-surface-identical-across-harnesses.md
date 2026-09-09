---
id: hypothesis:l3-workflow-surface-identical-across-harnesses
mint_id: a45f04511a2f4c2180322c65257c97ee
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-XI
scaffold_hash: d67900f67ff176e8
season: 2
testable_claim: After the change, one workflow run through workflow.py presents the same surface on both harnesses - the same stage tree, the same per-stage progress, the same final summary - so a reader cannot tell from the presentation which harness executed it, proven by running one workflow both ways and diffing the rendered views.
thought_session: belam-S1-L3-XI
title: "A workflow presents a different surface depending on the harness it runs on: the Claude Code path renders the native interactive workflow view and the pi path prints flat log lines, so the same workflow is two different experiences"
---
<!-- BODY:BEGIN -->
# hypothesis:l3-workflow-surface-identical-across-harnesses

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD, NOT A PROBE. YOUR ARTEFACT IS A DIFF. An empty `git diff --stat` at the end means you are NOT done.

THE OWNER ASKED FOR THIS DIRECTLY, 2026-09-08, verbatim as received (voice transcription; a homophone is noted in brackets where the intent is unambiguous from context): "I'm fine deep search being Claude and review I just want it to work the other way as well. When using The sonic [Sonnet] subscription model or the Opus subscription model, I wanted to show up the same way all the workflows show up and call code interactively. And then if I use the black [pi] harness, I still wanted to show up and look the same as the workflow does in Claude code if at all possible."

WHAT IS BEING ASKED. `workflow.py run <name>` is the unified route (owner, 2026-09-08: "always dispatched from the unified route. As always everything unified"). It is unified in EXECUTION and not in PRESENTATION. Run a workflow on `--harness claude-code` and the native Claude Code workflow surface renders it: a live stage tree, per-stage progress, agents appearing and completing, an interactive view. Run the identical workflow on `--harness pi` and `workflow.py` writes flat text lines to a file. Same manifest, same stages, same intent, two different experiences - and the pi one is the one nobody can watch.

The owner's phrase "if at all possible" is an honest hedge and you should treat it as one: the pi path cannot literally become the Claude Code UI. What it CAN be is the same INFORMATION in the same SHAPE, rendered from one description of the run rather than two. That is the target.

WHAT TO BUILD.
1. ONE run model, two renderers. The runner should emit a structured stream of run events - stage started, agent spawned, stage finished, stage failed, run summarized - and BOTH harness paths should feed that same stream. Nothing should be able to appear in one view and not the other, because there is only one source. This is the same "one render, two readers" shape `viewport.py --verify` already proves for the graph (`goal:g9.7`); read that first and follow it rather than inventing a second pattern. If `viewport.py`'s emitter can be reused rather than duplicated, reuse it and say so.
2. A pi-harness renderer that draws the stage tree as it runs, not a transcript after the fact. Live enough to watch. It does not need color or animation; it needs to show which stages exist, which are running, which are done, and what each returned.
3. The final summary must be byte-identical in content across harnesses - same stages, same counts, same outcomes - even where the live rendering differs.

MODEL POLICY IS SETTLED AND IS NOT YOURS. The owner's model choices (review: weak OpenRouter or Sonnet; deep-search: Opus at high effort) are config values set by the director, and the per-harness model RESOLUTION is `hypothesis:l3-workflow-model-crosses-harness-namespace`. Do not touch model resolution here. Do not touch `.agi/config.json` workflow rows.

PROVE IT. Run ONE workflow both ways - `--harness claude-code` and `--harness pi` - and put both rendered views in your node side by side. The gate is that a reader cannot tell from the SUMMARY which harness ran it, and can follow the live view on the pi side without reading a log file. `--dry-run` is not sufficient evidence here: this brief is about what a run LOOKS like, and a dry run looks like nothing. If the runtime OpenRouter key is still at its cap when you run, say so plainly and demonstrate on the harness you can actually reach rather than faking the other.

DO NOT touch `dispatch.py`, `brief.py`, `rotate.py`, `cli.py` or `zoom.py`. Do not write `.agi/nodes/.geometry/seats.md`. Do not kill any `belam-*` tmux window. Do not change what any manifest MEANS - stages and prompts are settled and other work depends on them.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted from the owner's own words within minutes of them arriving, and deliberately separated from the cost brief it came in the same breath as. The owner asked for two things at once - make both harnesses work, and make both look the same - and they are different builds with different risks: one is a namespace error with a dollar figure, the other is a presentation architecture. Folding them together would have let the cheap urgent half hide the expensive structural half. The one-stream-two-renderers shape is not invented here; it is g9.7's proven pattern pointed at a second subject.
<!-- THOUGHT:END -->

YOU HOLD A BRANCH — READ THIS BEFORE ANYTHING ELSE (Belam XI, L3.43, 2026-09-08). You were dispatched with `--branch`, so you are in your own git worktree on your own `loop/...@s2` branch. **COMMIT YOUR KID'S WORK TO THAT BRANCH BEFORE YOU EXIT.** From inside your worktree:

    git add -A
    git commit -m "L3.43 <your agent id>: <what landed>"

MEASURED TWICE NOW, INCLUDING THE ROUND IMMEDIATELY BEFORE THIS ONE: every `--branch` parent so far has exited with its branch at ZERO commits ahead, `season.py merge-up` then merged an empty branch and REPORTED GREEN, and a human had to harvest the work by hand from inside the worktree. A round that ends with your branch empty has produced nothing as far as every automated reader is concerned. You are the live proof that this can work — see `hypothesis:l3-parent-brief-forbids-the-only-commit`.

Do NOT push. Do NOT merge. Do NOT touch `season/s2`. The director merges. Commit locally on your own branch, that is all.

Run on pi/OpenRouter. Your kid: `python3 extensions/agi/bin/dispatch.py . L3.43 --target <this node> --level small --tier kid --harness pi`. Do NOT run `workflow.py run` for any reason this round.
