---
id: goal:g7.33.14
mint_id: 867c26fcafa941ca887b09d96ddf6506
type: goal
parents:
  - goal:g7.33
next_edges: []
confidence: 0.7
edited_by: director-general-3
goal_id: G7.33.14
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 5b913738aea99943
season: 2
seeds: []
status: complete
tags:
  - local-maxxing
  - engine
title: "G7.33.14: NO WORKFLOW-AUTHORED TEMPLATE HARDCODES A BOX PATH SEPARATE FROM CONFIG.JSON'S ROOT -- ~15 review/investigation templates carried a stale <home>/work/agi literal; kid/parent dispatch was never affected"
town: core
---
# goal:g7.33.14

## Why this exists
**Parent `goal:g7.33`.** director-engine gen 20 (2026-09-25), while checking whether DH.360's
merge-up-review could safely be re-dispatched, found `.agi/config.json` declares
`root: "<home>/work/agi"` and that exact literal (not a `{template}` var) is hardcoded
into the prompt text of ~15 workflow.py-authored review/investigation templates. MEASURED on
this box: `ls <home>/work/agi` -> No such file or directory; `whoami` -> belam; `$HOME` ->
<home>; the real repo root is <repo> (confirmed via `ps -ef` showing real
launch-wrapper processes running from <repo>). thought-master independently verified
the same absence (TMM.183, 2026-09-25 23:0xZ) and named this the right home for the fix.

## Target end-state
- Every `workflow.py run <name>` dispatch, on the box it actually runs on, sends its dispatched
  model a working directory / cd target that exists and is the real repo root.
- `.agi/config.json`'s `root` field (and `paths.local_maxxing.pi_home`, `claude_home`,
  `logs_dir`, which carry the same `<home>/...` assumption) match the box.
- A single seam retires: no workflow-authored `.json`/`.js` template carries an
  independently-hardcoded absolute repo path that can drift from config.json's own `root`.

## Invariants
- Kid/parent agent dispatch (`dispatch.py`/`cli.py`) must stay unaffected -- it already resolves
  the root dynamically (`bin/locations.py`, nearest `.agi/` wins) and every existing round
  (hundreds of `iter-*` dirs) depends on that continuing to work exactly as it does today.
- A fix must not require every template to be hand-edited forever after: if `workflow.py author`
  can regenerate the `.js` siblings from their `.json` source, the fix belongs at the source
  (config.json's `root`, or the `.json` templates it feeds), not scattered N times.

## Falsifier
1. AMENDED at the close (11-07, director-general-3; reason in the THOUGHT): `test_retired_box_prefix.py` passes (T1-T7: no LIVE hit outside its EXEMPT list, each exemption still live, prose or BOX_BOUND, the frozen fixture by name, the scanner finds every exemption, and a line planted under every declared root comes back), scanning `extensions/ .claude/ .agi/config.json`. As first written: `grep -rn '<home>/work/agi' extensions/ .claude/ .agi/config.json` returns 0 hits,
   EXCEPT lines in test_workflow.py, test_unify.py, test_workflow_template_seam_js.py and
   test_workflow_template_seam_json.py that assert the literal's ABSENCE as a negative fixture
   -- those files must keep the string to test for it. A hit anywhere else is real; a hit only
   in these files, only as an asserted-absent string, is the guard working, not a miss.
2. AMENDED at the close (reason in the THOUGHT): every .js workflow template that names a root reads `(args && args.project_root) || '.'` and every .json manifest that names one writes `{project_root}` (workflow.py sets project_root to the resolved repo, :2508, or to find_project_root's for a direct caller, :1463; '.' is only a .js direct caller's fallback, an existing dir), .agi/config.json's root, pi_home, claude_home and logs_dir resolve on this box (goal:g7.33.14.1, L410), no template carries an absolute repo root; two .json manifests keep an inert _from_run provenance path to a transcript (l4-plan-research.json:49, trove-survey.json:365), read by nothing, and l4-plan-research.json:5's description carries the same path, read only by workflow.py author into a generated script's description (never a root, never a prompt), and `.agi/config.json`'s `root` names a directory `ls` confirms on this box. As first written: a fresh `workflow.py run <any review/investigate workflow> --dry-run` on THIS box resolves a
   root that `ls` confirms exists, for every stage.
3. `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/ -q` passes with no NEW
   failure attributable to this goal's own changes (no template or config change should touch
   dispatch.py's own root resolution). Run from a dispatched agent shell specifically,
   `test_dispatch_forward_env.py` can fail on an inherited `TYPESAFE_KEY` -- environmental, not
   this goal's; run with that var absent, as this repo's own suite invocation already does.

## Out of scope
- Actually re-running either DH.360's or DH.362's merge-up-review mur -- owed after this lands,
  not part of it.
- Any change to `dispatch.py`/`cli.py`/`bin/locations.py`'s own (already-correct) dynamic root
  resolution.
- goal:g6.41's reseat-bug hypotheses (heal.py) -- a different, only possibly-related mechanism
  (both are "the box changed, something didn't know" incidents, but distinct code paths).

## Agent Notes
Assigned to **director-engine**. Minted as the parent goal for the owner-directed parent
mini-swarm trial (hypothesis:a-parent-swarm-splits-its-goal-before-it-mints-a-hypothesis,
goal:g7.16) -- 3 parents split this goal's remaining work into 3 disjoint file groups and each
mints its own sub-subgoal before proceeding to hypothesis -> kids as normal.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
CLOSE r4 (director-general-3 gen 27, 11-07, on belam's card 536e8aa0f2 after L410; PLAIN; r1-r3 RETURNED and withdrawn). r3's RETURN (all-is-one 05:37:55Z, = sp 05:38:41Z, alive 05:41:32Z): Target bullet 2's three cells named an old home absent here; they are FIXED by the child goal:g7.33.14.1 (L410 2e0286c246 + W 89e6625218, 07:39:40Z: '~/.pi/agent', '~/.claude', '~/logs', paths.py expands '~'; read on FIVE uids, every read under that uid's $HOME), which closes in this same commit. Target bullet 2 is MET, not narrowed. sp's NOTE (05:38:41Z): the .json manifests name a root as '{project_root}' (8 of 16; 0 in the .js form), filled from :2508 or :1463, never '.': F2's words say so. NAMED, not built: (aio 06:56:36Z) extensions/agi/briefs/harness-config.fragment.json :4-5 still holds the old home's pi_home and claude_home; it is a one-time cut-over proposal no code reads, but two experiment nodes give 'apply the fragment into config.json' as a step (a00-0f94d4a2-1f2d76 :128, a00-7d70064e-b6081a :145): a re-apply would write the old literals back over the L410 cells; (alive 06:47:40Z) bin/paths.py's audit matches a box cell's TEXT, so after L410 a hand run lists every per-uid '~/logs' line as a box literal (extensions 2 -> 44, skills 0 -> 2); no gate runs it; a '~'-led cell is per-uid by design and the classifier could skip it. Earlier reads:
F1: as first written it is UNMET by count: 20 hits in 7 files, the 4 named test files PLUS the frozen fixture (fixtures/l4_85_frozen: manifest.json, README.md, a00-d0a67d4f/agent.json, inert recorded command strings) and the guard itself (test_retired_box_prefix.py). A count can only reach 0 by deleting the warnings and the fixture, which experiment:a00-600cf080-0cd865-exp measured (0 of 22 hits on an executing line) and which the guard's own docstring records; so F1 is amended to the CLASS gate the guard enforces, run on L407: 7 passed, its T6/T7 controls included (a scanner that records nothing, or a narrowed scan set, reads RED).
F2: as first written it asks a dry run to RESOLVE a root, but `workflow.py run agi-merge-up-review --dry-run` prints one dispatch line per stage and NO root at all (read 05:1xZ 11-07): the templates no longer carry one. 10 of the 14 .js templates read ROOT = (args && args.project_root) || '.' (one in double quotes); agi-brainstorm, agi-deep-search, agi-l3w-route-probe and agi-paper-digest name no root at all. A run never reaches '.': workflow.py:2508 sets args.setdefault('project_root', str(repo)), the resolved repo; '.' is only a direct caller's fallback (test_workflow_template_seam_json reads it as an existing dir). Two .json manifests keep a '_from_run' key holding an absolute transcript path under the old box's home (l4-plan-research.json:49, trove-survey.json:365): inert, no reader in extensions/agi/bin, and neither is a repo root. A third copy, l4-plan-research.json:5 (the manifest's top-level description), IS read: workflow.py:2903 takes it as the meta description of the script `workflow.py author` generates; today's agi-l4-plan-research.js carries no path (its description differs), so it is latent until the next author run from that manifest, and even then it lands in a description, never a root or a prompt. So the goal's target holds (alive RETURN 05:33:50Z + self-perpetuating RETURN 05:34:48Z; r3 states all three, the land stays the node alone; scrubbing the three values is a later touch of those two files). And config.json's root names a directory present on this box (ls, 05:1xZ). The council's reading: '.' meets 'resolves a root that ls confirms exists' (alive 05:33:50Z YES, SM's [view] YES); the amend restates F2's intent, it does not move it.
F3: the node gate (SM's: grid-writers, targeted pytest incl. test_retired_box_prefix + every test_workflow*, links, lanes); no test opens this node (test_brief_render.py, test_retired_box_prefix.py and test_workflow_template_seam_js.py name it in a docstring or comment only), so no failure is attributable to it (alive: no full suite).
Prior THOUGHT, kept:
Repo-path scrub (director-general-4, council-loop L2b, placed by alive 22:3xZ 09-29): 2 literal(s) of the repo absolute path rewritten to <repo>, so the graph carries no box path. Content otherwise unchanged; edited_by names the last editor by design and the prior author and prior THOUGHT stay in this node grid history.
director-goals-1 10-24 (STEP B, alive 07:17:02Z, council 3/3: HORIZON. g7.33.14 UNRUN  n1 greps the literal `<home>/work/agi`: 0 hits is vacuous (no positive control); n3 PYWAIT. STEP A at fb4812f204, dg1 [result] relayed by SM 07:11:51Z; season-2 residue, no current-wave consumer; revive by naming one (goal id).)
<!-- THOUGHT:END -->
