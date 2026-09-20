---
id: verdict:a00-3d540aa5-seam-verdict
mint_id: fa3eefe7954b49d1a7d26695d870ee8e
type: verdict
parents:
  - experiment:a00-3d540aa5-seam-exp
next_edges: []
confidence: 0.8
edited_by: a00-f694a5f1
evidence_runs:
  - experiment:a00-3d540aa5-seam-exp
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "grep -Ein grok .agi/nodes/goal/g17.14.2.md", "expected": ">=1 line, the control file contains grok", "observed": "3 lines, exit 0", "result": "detected"}
  - {"conjunct": 2, "class": "auth", "cmd": "python3 -c \"adapters.resolve(cfg, .grok-bot.)\"", "expected": "AdapterError naming grok-bot because the harness is not declared", "observed": "AdapterError: no harness .grok-bot. in config; declared: [.claude-code., .copilot-cli., .pi., .pi-local.]", "result": "refused"}
  - {"conjunct": 3, "class": "wire", "cmd": "python3 -c \"adapters.load(.grok_bot.)\"", "expected": "AdapterError naming the expected adapter path from live module resolution", "observed": "AdapterError: no adapter for harness .grok_bot.: expected .../bin/adapters/grok_bot_adapter.py", "result": "refused"}
  - {"conjunct": "C1 dispatch.py grok-free", "class": "gate", "cmd": "grep -Ein grok extensions/agi/bin/dispatch.py", "expected": "0 lines, exit 1", "observed": "0 lines, exit 1", "result": "gate holds"}
  - {"conjunct": "C1 grep is live (negative control)", "class": "wire", "cmd": "same pattern on .agi/nodes/goal/g17.14.2.md", "expected": ">=1 hit if pattern live", "observed": "3 hits, exit 0", "result": "pattern live, zero is a measurement"}
  - {"conjunct": "C2 shipped adapters grok-free", "class": "gate", "cmd": "grep -Ein grok pi_adapter.py claude_code_adapter.py copilot_cli_adapter.py", "expected": "0 lines, exit 1", "observed": "0 lines, exit 1", "result": "gate holds"}
  - {"conjunct": "C3 absent row refused by name", "class": "auth", "cmd": "adapters.resolve(cfg,'grok-bot') on this branch config", "expected": "AdapterError naming grok-bot", "observed": "AdapterError: no harness 'grok-bot' in config; declared: ['claude-code','copilot-cli','pi','pi-local']", "result": "refused by name"}
  - {"conjunct": "C3 present row threads live (wire)", "class": "wire", "cmd": "same resolve on an in-memory COPY with helper-cfg-land row {adapter:grok_bot,bin:/home/ubuntu/.npm-global/bin/grok-bot}", "expected": "resolve succeeds and returns the row", "observed": "RESOLVED grok-bot {adapter:grok_bot,bin:/home/ubuntu/.npm-global/bin/grok-bot,models:{kid:grok-4-fast,parent:grok-4}}", "result": "wire confirmed"}
  - {"conjunct": "residue5 supersedes referent is live in merge set", "class": "auth", "cmd": "git ls-tree -r --name-only season2/loops/goal-g17.14.2-helper-cfg-land | grep a00-bfd0d94a  + same for goal-g17.14.1-a00-597f6b8f", "expected": "node file present on the branches the MUR merges", "observed": "hypothesis/a00-bfd0d94a-d67716.md present on both; links.py links = 3725 resolved, 0 broken", "result": "referent live in merge set, edge is not a broken link"}
profile: balanced
push_further: "on a branch where harnesses.grok-bot IS present (helper-cfg-land), exercise the well-formedness branch: adapter==grok_bot, bin==DEFAULT_BIN, resolve succeeds"
role: kid
season: 2
title: "grok-bot seam holds merge-invariant on this branch: zero grok in dispatch.py and shipped adapters, config row absent and refused by name"
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# verdict:a00-3d540aa5-seam-verdict

## Verdict

`inconclusive_lean_proved:80`

## Evidence

Judging `hypothesis:a00-3d540aa5-fa98ee` against its single backing run,
`experiment:a00-3d540aa5-seam-exp`, whose transcript is
`.agi/sessions/iter-DT.15/a00-3d540aa5/measure.txt`.

**Conjunct 1 — dispatch.py carries no grok literal.** MEASURED.
`grep -Ein grok extensions/agi/bin/dispatch.py` -> 0 lines, exit 1.

**Conjunct 2 — no shipped adapter carries a grok literal.** MEASURED.
One grep across `pi_adapter.py`, `claude_code_adapter.py`,
`copilot_cli_adapter.py` -> 0 lines, exit 1.

**Conjunct 3 — the config row belongs to the subgoal, not the seam.** MEASURED
on this branch, and this is the residue-3 fix: `harnesses` here declares
`['claude-code','copilot-cli','pi','pi-local']`; `harnesses.grok-bot` is
**absent**, and `adapters.resolve(cfg, "grok-bot")` refuses **by name** with
`AdapterError: no harness 'grok-bot' in config; declared: [...]`. The
hypothesis does not assert the row is present, so nothing here contradicts it.
The disproof condition — a grok literal in dispatch.py or a shipped adapter,
or a malformed present row — is not observed.

**Why not `proved`.** The well-formedness half of conjunct 3
(`adapter == "grok_bot"`, `bin == /home/ubuntu/.npm-global/bin/grok-bot`,
resolve succeeds) is a conditional on a row that is absent on this branch, so
it was not exercised. Every conjunct that can be measured here is, but one
branch of one conjunct is untested, and the honest ceiling is a lean.

**Negative control.** The same grep against `.agi/nodes/goal/g17.14.2.md`
hits 3 lines (exit 0), so the two zeros above are live measurements, not a
dead pattern.

## Supersession

`hypothesis:a00-bfd0d94a-d67716` (the false P7, seam gate asserting a config
row absent from this merge target) is superseded by
`hypothesis:a00-3d540aa5-fa98ee` via a machine-readable `supersedes:` edge in
that node's frontmatter — residue 5 cleared with an in-tree edge, not prose.
The superseded node stays live on
`season2/loops/goal-g17.14.2-helper-cfg-land` (`76d141786`) and
`season2/loops/goal-g17.14.1-a00-597f6b8f`.

## What this means for the MUR

The chain is committed in-tree (`hypothesis` + `experiment` + this `verdict`,
all basenames carrying agent id `a00-3d540aa5`), `evidence_runs` names a node
that resolves on the branch, and no file outside `.agi/nodes/**` changed.
The merge-invariant rewording is what lets the claim hold on
`core/season2/main` without the config row being present.

## Agent Notes
Merge-invariant seam verdict: 0 grok hits in dispatch.py and the three shipped adapters, harnesses.grok-bot absent on this branch and adapters.resolve refuses by name; supersession edge to hypothesis:a00-bfd0d94a-d67716 set in frontmatter. Lean not proved because the row-present well-formedness branch is unexercised.

## Agent Notes
merge-invariant seam chain under goal:g17.14.2: 0 grok hits in dispatch.py and the 3 shipped adapters (exit 1), harnesses.grok-bot absent on this branch and adapters.resolve refuses by name, supersedes edge to hypothesis:a00-bfd0d94a-d67716; lean 80 because the row-present well-formedness branch is unexercised

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-f694a5f1), accepted at some confidence below proved.

(1) THE INSTRUCTION SAID: clear five DT.13 MUR residues — commit the experiment+verdict (residue 1), make evidence_runs resolve in-tree (2), either land the g17.14.2 config row OR reword the claim so it does not assert a row absent from the merge target (3), leave no uncommitted parent edits (4), and supersede the false P7 with a live referent or an in-tree edge rather than prose (5).

(2) WHAT THE MACHINE ACTUALLY DOES: all three node files are carried by commit bf21dc482 on season2/loops/goal-g17.14.2-a00-f694a5f1 (git show --stat: hypothesis a00-3d540aa5-fa98ee.md +65, experiment a00-3d540aa5-seam-exp.md +92, verdict a00-3d540aa5-seam-verdict.md +85), and `git status --porcelain` is empty, so residues 1 and 4 are cleared on the bytes, not on the summary. Residue 2: evidence_runs names experiment:a00-3d540aa5-seam-exp, which resolves in this tree. Residue 3: the hypothesis testable_claim is conditional (grep-dispatch, grep-adapters, and 'if the row is present it must be well-formed') so it names no absent row as a seam condition. Residue 5: frontmatter `supersedes: hypothesis:a00-bfd0d94a-d67716`; I confirmed by git ls-tree that the referent node file exists on season2/loops/goal-g17.14.2-helper-cfg-land and season2/loops/goal-g17.14.1-a00-597f6b8f, and `links.py links` reports 3725 resolved, 0 broken. My own negative probes (now in probes:): grep dispatch.py 0/exit1 with a live control (3 hits on goal:g17.14.2.md), grep the three shipped adapters 0/exit1, resolve('grok-bot') refuses by name with the declared list, and the same resolve on a COPY carrying the helper-cfg-land row returns it (wire), so the resolve path reads the row rather than a constant.

(3) THE NEAR MISS: the plausible implementation that satisfies the words and loses the mechanism is the literal 'land the config row' path. `_round_scope_ok` in extensions/agi/bin/cli.py hard-excludes `.agi/config.json` from the round commit, so a hand-landed row is exactly residue 4's dirty worktree and never reaches the tip; the kid reworded instead, which the dispatch expressly permitted. The second near miss is an in-branch `supersedes:` edge to an absent node presented as fixed: the referent is NOT a live node on this branch, only on the branches the MUR merges; the edge is machine-readable and link-clean, which is why I record this as the node's caveat rather than a disproof.

(4) DEVIATION: none. I take the reword branch the dispatch names, not a by-hand config land.
<!-- THOUGHT:END -->

PARENT ACCEPT (a00-f694a5f1): commit bf21dc482 carries hyp+exp+verdict, tree clean. Residues 1-4 cleared on bytes; residue 5 as a machine-readable supersedes edge whose referent lives on the MUR-merged helper-cfg-land/g17.14.1 branches (links.py 0 broken). Independent probes pass: dispatch.py and the three shipped adapters grok-free (grep exit 1, live control hits), resolve refuses an absent grok-bot by name and returns a present row (wire). Kept the kid's honest lean (inconclusive_lean_proved:80) rather than promoting to proved: the row-present well-formedness branch is unexercised on this branch.
