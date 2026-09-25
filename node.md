---
id: hypothesis:a-parent-swarm-splits-its-goal-before-it-mints-a-hypothesis
mint_id: c084a33890bd4743a6dc846b61279511
type: hypothesis
parents:
  - goal:g7.16
next_edges: []
edited_by: belam
scaffold_hash: 7bfefea90e30ad6c
season: 2
testable_claim: A mini-swarm of 3 parents on one target, which talks first, splits the target into 3 sub-subgoals and mints them, then runs hypothesis -> kids exactly as today from its own sub-subgoal, lands >= 2x the accepted experiments per wall-clock hour of one parent per round on the same branch, with no drop in merge-up verdict quality, no build-loop sibling touching the same file, and <= 3 swarms live town-wide inside the spawn budget (30) and memory (MemAvailable >= 1.5 GiB).
thought_session: belam-S2-L5-VII
title: "A parent swarm of 3 talks first, splits its goal into sub-subgoals, then runs hypothesis -> kids as now; <= 3 swarms town-wide, both branches (assigned: director-engine + director-thought)"
town: core
---
# hypothesis:a-parent-swarm-splits-its-goal-before-it-mints-a-hypothesis

# hypothesis:a-parent-swarm-splits-its-goal-before-it-mints-a-hypothesis

assigned: director-engine (build arm) + director-thought via thought-master (research arm). Minted by belam-S2-L5-VII (Prime) from the owner's words below; supersedes, FOR THIS TRIAL ONLY, doc:unified-director-brief's "DISPATCH ONE parent per round -- parent/kid pairs ONLY" (owner 09-24 03:39Z, 17:02Z, 20:1xZ).

## OWNER (verbatim, 09-25 22:5xZ, to the Prime)
> Can we dial up the concurrency and also investigate if parallel hypotheses make sense in a build loop? Maybe have the parent brief mention communicating with one another in a small swarm of 3-5 to subsplit the assigned goal even further and then also dial up concurrency a bit as well to 3 or so mini-swarms running at once. Basically the only difference from standard parent brief is that we ask the parents to talk to one another first and figure out the goal split into further subgoals and mint said subgoals and then  hypothesis and onwards and spawn kids on those the way it works now. Just start at a sub-subgoal instead of a hypothesis but everything else the same. Does that make sense? Could try in both branches see how it does. I think parents already talk together well

## Measured
- Today a round is ONE parent (doc:unified-director-brief:58). The spawn budget is 30 live (.agi/config.json:140); 2 were live at 22:5xZ.
- Parents already talk: OSC.10 (director-thought, 09-23) put 2 parents on one hypothesis in room `swarm-osc10` ("post your interpretation before your first kid"), .agi/comms/season-2/room/swarm-osc10.md.
- No code is needed for a trial: `dispatch.py --orders <file>` rides the file VERBATIM as the parent brief's LAST section (`## DISPATCH ORDERS (from <post>, <ts>)`) and records it on the manifest.
- Cost per process, measured 22:5xZ: a pi parent tree ~134 MiB, a pi kid ~133 MiB; one research experiment process (parent a00-bcea484d's worktree) 3.2 GiB; a claude seat 330-415 MiB; the box has 15 GiB and MemAvailable fell to 6.6 GB with the stream up.
- pi-free returned 'Provider returned an empty response' on 2 of 9 PASS 6 reviews, so the free tier may throttle at higher concurrency.

## CLAIM
A mini-swarm of 3 parents on one target, which TALKS FIRST, splits the target into 3 sub-subgoals and mints them, then runs hypothesis -> kids exactly as today from its own sub-subgoal, lands >= 2x the accepted experiments per wall-clock hour of one parent per round on the same branch. Merge-up verdict quality does not drop, build-loop siblings never touch the same file, and <= 3 swarms live town-wide stay inside the spawn budget (30) and memory (MemAvailable >= 1.5 GiB throughout).

## Dispatch line
config-max: swarm_size (3) + max_swarms (3) become config cells ONLY after the verdict / template-max: the ORDERS below become ONE section of the parent template ONLY after the verdict (the trial rides `--orders`) / code: none for the trial.

## ORDERS (the --orders file, identical in both arms; the director fills <room> <target> <i>)
```
## SWARM (hypothesis:a-parent-swarm-splits-its-goal-before-it-mints-a-hypothesis) -- you are parent <i> of 3 on <target>, room <room>
1. TALK FIRST in <room> (send.py send <room> '<text>'; send.py read <room>), before any mint or kid: LAP 0 = your reading of <target>, <= 5 lines.
2. SPLIT: parent 1 proposes 3 sub-subgoals of <target>, one per parent, with DISJOINT file scopes (build) or DISJOINT compute (research: at most ONE model-running kid per swarm at a time); the others accept or amend once; parent 1 posts the final split. At most 2 laps; after 2 laps parent 1's split stands.
3. MINT only your own sub-subgoal: write.py create goal <slug> --parent <target>, its THOUGHT naming the split and who took which.
4. Then EXACTLY as your brief says, starting from your sub-subgoal instead of <target>: hypothesis -> kids -> experiments -> report. <= 2 kids live per parent.
5. One line to <room> at each landing (kid done, verdict) and before you exit.
```

## BUILD the --orders file (owner 22:5xZ, verbatim: “Make sure the patent brief contains the goal and hypothesis node schemas as guides.”)
The --orders file = the ORDERS block above (filled) + BOTH schema files appended VERBATIM at dispatch time (read live, never a copy that can go stale), each under a `### GUIDE: the <type> node schema (<path>, verbatim)` line inside a four-backtick fence: `.agi/context/schemas/[goal].md`, then `.agi/context/schemas/[hypothesis].md`. Verified 23:1xZ by building the real spawn: `dispatch.py . 999 --target goal:g7.16 --level small --tier parent --role parent --ladder-tier 0 --orders <file> --dry-run` reports `orders: 391 lines` (389 file lines + the heading), both schemas whole, frontmatter included. Config route (answering the owner 23:0xZ, “Do we have a config or template based way to append docs to briefs”): config:brief `extras: {role: [refs]}` exists (brief.py:2473) but a DISPATCHED parent never sees it (the extras part returns the dynamic dispatch brief first, brief.py:2467-2471) and a ref must be a node (`_node_text`), not a schema file -- director-engine closes both, then `extras.parent` = the two schema paths is one config edit for every parent.

## FALSIFIERS
- throughput < 1.5x the branch's single-parent baseline after 2 swarms per arm;
- a build-loop collision: two siblings' branches touch the same file (merge-tree conflict at the merge-up);
- the talk-first split takes > 2 laps or > 20 min median, so talk eats the gain;
- memguard SIGSTOP, an OOM kill, or MemAvailable < 1.5 GiB while swarms run;
- pi-free empty responses at >= 9 live parents > 2x the single-parent rate.

## TESTS
No committed test: a process trial. Measured from `.agi/sessions/iter-*/` manifests (wall clock, kids, experiments), the rooms, the merge-up verdicts, `spawn_budget.py status`, the memguard log. Baseline = each branch's last 5 single-parent rounds.

## FILE SCOPE
Trial: the directors' orders files (box-local) + the goal / hypothesis / experiment nodes the swarms mint. Promotion after the verdict (director-engine): the parent template section + the two config cells.

## CEILING
3 parents per swarm (the low end of the owner's 3-5) · <= 3 swarms live town-wide: director-engine 1, director-thought 1, the 3rd to whichever arm lands a clean split first while MemAvailable >= 3 GiB with the stream up · <= 2 kids live per parent (worst case 9 + 18 = 27 <= 30) · pi-free, 0 USD · 2 swarms per arm, then judge.
