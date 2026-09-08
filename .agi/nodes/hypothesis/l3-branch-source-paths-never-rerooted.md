---
id: hypothesis:l3-branch-source-paths-never-rerooted
mint_id: 973d6413c509429d9ef91360a2fdf09f
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-X
scaffold_hash: 0ce72d64c3732ee4
season: 2
testable_claim=dispatch.py: re-roots the child GRAPH via child_working_graph but derives PLUGIN_ROOT, CLI_PY, skill_prompt and dispatch_py from Path(__file__) of the running dispatch.py, module constants no --branch code touches, so a --branch kid receives one argv containing a worktree-absolute scaffolded node path beside main-absolute cli.py and agent-prompt.md and edits main. After the change a child_engine_paths helper re-roots those four through locations.source_root — which already exists at locations.py:313 and is called by nothing in dispatch, brief or zoom — branch_root becomes the checkout root rather than the .agi graph dir, and the brief states the agent's own checkout out loud; proven by a red-first test asserting every absolute repo path in a --branch kid's argv shares the worktree prefix, red before and green after
thought_session: belam-S1-L3-X
title: dispatch.py re-roots a child graph and never its engine paths, so one argv carries a worktree node path beside main-absolute source paths and the kid follows the only source anchor it was given
---
<!-- BODY:BEGIN -->
# hypothesis:l3-branch-source-paths-never-rerooted

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD, NOT A PROBE. YOUR ARTEFACT IS A DIFF. The mechanism is PINNED — you are not investigating, you are landing a fix somebody else already specified with file:line.

PROVENANCE. A deep-search run of 50 agents (5 lenses, 44 candidate mechanisms, 2 adversarial refuters each, 5 survivors, 2.2 hours) was dispatched at the owner's prompting to explain why a `--branch` kid writes source into the main checkout. This is its rank-1 answer, and it is grounded in the kid's PRESERVED ARGV and its own reasoning trace, not in reading code and guessing.

THE MECHANISM. `dispatch.py` re-roots the child's GRAPH thoroughly and correctly — `child_working_graph` feeds `child_graph`, the zoom render, the scaffolded node path, `sess_dir`, `AGI_TREE_PROJECT_ROOT` and cwd. It re-roots the child's ENGINE paths not at all. `PLUGIN_ROOT` (dispatch.py:38), `CLI_PY` (:40), `skill_prompt` (:1180) and `dispatch_py` (:1185) are module constants derived from `Path(__file__)` of whichever dispatch.py is running, and NO `--branch` code path touches them. Worse, it is self-perpetuating down the tier chain: the parent's own brief (brief.py:1012) hands it main's absolute `dispatch.py`, so when the parent spawns a kid, `PLUGIN_ROOT` resolves to main for the kid too.

The consequence is one argv holding both trees at once. The kid saw `SCAFFOLDED NODE FILE: <worktree>/.agi/nodes/experiment/a00-f8f26cd8-26c4a3.md` — and obeyed it exactly, which is why every node landed correctly. Beside it, the ONLY absolute source-tree strings in the entire prompt: `python3 /home/ubuntu/work/agi/extensions/agi/bin/cli.py done ...` and `@/home/ubuntu/work/agi/extensions/agi/lib/agent-prompt.md`. Both main. The graph half was pinned by an absolute path it was handed; the source half was anchored only by two main-rooted strings. The kid's own trace says it plainly: *"The cli.py path in my prompt is /home/ubuntu/work/agi/extensions/agi/bin/cli.py (main tree), but the node file is in the worktree... These are in DIFFERENT trees."*

A CORRECTION THIS PROJECT MUST ABSORB, because two directors recorded the wrong half. Belam IX's DM and Belam X's own evidence note both named `zoom.py` alongside `brief.py` as rendering main-absolute source paths. **`zoom.py` is EXONERATED.** The rendered `context.md` — 16654 bytes — contains ZERO absolute paths (`grep -c '/home/ubuntu'` returns 0) and names nodes graph-relative. The leak is argv assembly in `dispatch.py` and `brief.py`. Fix the node text where it says otherwise.

THE AGGRAVATOR, rank 2, which you should fix on the same pass. For a spawn WITHOUT `--branch`, dispatch.py:1083 sets `branch_root = root` and :1293 passes `cwd=str(branch_root)` — but `root` is the `.agi` GRAPH DIR, not the checkout. Measured from pi's cwd-keyed session dir: the kid was born in `<worktree>/.agi`, which contains no `extensions/`. So every relative source instruction its own brief gave it (`python3 -m pytest extensions/agi/tests/ -q` at brief.py:906, `write.py` at :918, `edit(path="extensions/agi/bin/some.py")` at :932) was unresolvable, while every graph reference resolved. That deletes the correct answer without supplying the wrong one — rank 1 supplies the wrong one. Together they are sufficient. This also hands the agent-git commit guard a graph dir that `git rev-parse --show-toplevel` can never match (`AGI_PROJECT_ROOT` at :1236).

THE FIX, four parts, ship them together.
1. Add `child_engine_paths(child_graph) -> dict` beside `child_working_graph` (~dispatch.py:221) computing `src = locations.source_root(child_graph)` and returning re-rooted `source_root`, `cli_py`, `skill_prompt`, `dispatch_py`. **`locations.source_root` already exists at locations.py:313 and is called by NOTHING in dispatch, brief or zoom** — the resolver for exactly this was built and never wired up. Fall back to the `PLUGIN_ROOT` constants per-path when a candidate does not exist, since a non-agi project's source tree has no engine.
2. Call it once `child_graph` is settled, on BOTH branches (dispatch.py:1082-1101), and pass its values at the `build_command` site instead of `cli_py=CLI_PY` (:1179), `skill_prompt=...` (:1180) and `dispatch_py=Path(__file__).resolve()` (:1185). Keep `PLUGIN_ROOT`/`CLI_PY` as fallbacks; do not delete them.
3. Replace `branch_root = root` (:1083) with the checkout root so a non-`--branch` kid is born where its own relative paths resolve.
4. In `brief.py`, give `_kid`/`_parent`/`assemble` a `source_root` keyword and emit ONE segment before the relative-path instructions: **"YOUR CHECKOUT: <abs source root>. Every source path below is relative to it. Do not edit any other checkout, even one whose path appears elsewhere in this prompt."** `brief.py` contains the string "worktree" ZERO times today — no agent is ever told which tree it owns. (1)+(2) remove the wrong answer, (3) restores the right one, (4) states it so a model that guesses cannot guess main.

PROVE IT. Red-first in `test_dispatch.py`, reusing the existing `_git_repo(tmp_path)` fixture and `dispatch.branch_worktree_for_spawn`: assert that EVERY absolute repo path in a `--branch` kid's argv shares the worktree prefix. It must fail against dispatch.py as it stands and pass after. Then one live `--branch` round whose main checkout `git status --porcelain` is EMPTY at parent exit — that is the only proof that actually counts, and this project now takes that snapshot every round.

HONEST LIMIT, carried from the synthesis and not to be overclaimed: none of the four files the kid edited is named in the argv. The kid typed the main prefix itself, having been given main as its only source anchor. So the mechanism fully explains the DIRECTION of both halves and is the only surviving candidate that produces a kind-by-kind split, but the final hop — main anchor to model choosing the main prefix — is inference from the kid's reasoning trace rather than forced by code. Fixing (1)-(4) removes the anchor; verify with the live round rather than declaring victory from the test.
