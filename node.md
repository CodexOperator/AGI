---
id: hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell
mint_id: 0c4b7c466b1b4226ab2d601cb17d23e2
type: hypothesis
parents:
  - hypothesis:a00-1ff9316d-177aae
next_edges: []
edited_by: director-engine
scaffold_hash: 2b76fd5380d914b6
season: 2
testable_claim: "mem_cap.resolve_tasks_max reads spawn.tasks_max (150 on the live config, TMM.263 (2)) and values.memcap.tasks_max is read nowhere; absent or bad cell falls back to the fail-closed 96; AGI_TASKS_MAX still overrides (assigned: director-engine)"
title: Per spawn tasks max reads the spawn tasks max cell
town: core
---
# hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell

## Measured
- TMM.263 (2), OWNER 19:5xZ via the Prime 20:13Z: the per-spawn scope's TasksMax is the cell `spawn.tasks_max` = 150, beside `spawn.memory_max` (2G). Committed by the director at 684a83a3a (.agi/config.json spawn.tasks_max: 150).
- PRE-FIX STATE, measured before this hypothesis's kid (DH.495 re-dates this row from the bytes: the reader itself is now correct): extensions/agi/bin/mem_cap.py `resolve_tasks_max` read `values.memcap.tasks_max` (absent on the live config) -> the shipped default 96 applied, not the owner's 150. The reader now reads `spawn.tasks_max`; DH.488 touched NO production line and did not re-measure this row.

## CLAIM
`resolve_tasks_max(cfg)` reads `spawn.tasks_max` (one cell, the one `resolve_memory_cap` sits beside), so on the live config every per-spawn scope carries TasksMax=150; `values.memcap.tasks_max` is read nowhere; an absent/non-numeric/<1 cell still falls back to the fail-closed default 96; AGI_TASKS_MAX still overrides for tests.

## Dispatch line
config-max: the value is the cell spawn.tasks_max (already committed; READ it, never write config.json) / template-max: none / code: the reader's key path + its docstring/comment.

## FALSIFIERS
- `grep -rn "memcap.*tasks_max\|\"memcap\").*tasks_max" extensions/agi/bin` hits a reader;
- `resolve_tasks_max(json.load(open('.agi/config.json')))` != 150;
- a cfg with spawn.tasks_max absent returns anything but 96.

## TESTS
extensions/agi/tests/test_mem_cap_tasks_max.py (rows on spawn.tasks_max + a live-config row = 150) + neighbourhood test_launch_memory_cap.py test_heal_mem_cap.py test_dispatch.py. Every pytest under `timeout 600`, --basetemp under /tmp. No test in this family launches a real systemd scope (DH.453 removed the DH.421 spawn rows).

## FILE SCOPE
extensions/agi/bin/mem_cap.py · extensions/agi/tests/test_mem_cap_tasks_max.py. Never .agi/config.json.

## CEILING
1 kid · <= 12 production lines · pi-free tier-0 · 0 USD. No test spawns pytest; kids never launch real claude.

## ROUND EG.1 -- the post-branch RED between two merged chains (director-engine, first round of the EG series: belam [decision] 00:0xZ 09-28 reset the DH counter)
Measured   post branch bf2430484: test_boxkit_probe.py::test_spawn_rows_target_the_config_and_the_resolvers_not_a_literal FAILS (1 failed, 365 passed over the 23 touched test files): assert (150, 150, 'ok') == (150, 96, 'DRIFT'). The fixture drives the drift through values.memcap.tasks_max (test:85, :550) while this node's chain (merged 1ee2340c3) made mem_cap.resolve_tasks_max read spawn.tasks_max (mem_cap.py:73-82) -- two merged chains disagree on which cell the resolver reads.
CLAIM      the boxkit probe's spawn.tasks_max row and its test agree with the ONE cell this node names (spawn.tasks_max via mem_cap.resolve_tasks_max): a resolver/cell disagreement is still reported as DRIFT, driven through a path production can take (e.g. the resolver's env override), and no test or probe reads values.memcap.tasks_max as the tasks bound.
Dispatch line  config-max: spawn.tasks_max is the one cell (no new cell) · template-max: none · code: the probe row / test fixture follow the resolver; never bring back a second cell
FALSIFIERS the named test still fails · any probe/test path still sets or reads values.memcap.tasks_max as the bound · the DRIFT case is removed rather than re-driven
TESTS      test_boxkit_probe.py test_mem_cap*.py (if present) + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE)
FILE SCOPE extensions/agi/tests/test_boxkit_probe.py · extensions/agi/boxkit/probe.py (the spawn.tasks_max row only) · the kid's own node
CEILING    HARD CAP: 1 kid · <= 8 production lines net · <= 30 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT     paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit

## CORRECTIVE EG.10 -- closes mur-eg-2 EG.1-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-per-spawn-tasks-max-r-a00-5ad98eb5 tip 4d2c43ea5 (branch de-base-EG.10; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 2. The round's own HARD CAP was exceeded with no recorded widening — hypothesis:...:40: CEILING EG.1 caps 1 kid and <=30 test lines; the range carries 3 experiment nodes and +49/-3 test lines (production net +6 of 8, in budget), with no node recording the Prime widening the cap.
2. OUTSIDE by director decision (a findings row, not this round): the eleven other `cfg.get("spawn") or {}` + `.get(...)`-on-a-scalar call sites (dispatch.py:1122, spawn_budget.py, ... as the reviewer lists them) -- LIST each file:line on your node in one table for the g7.33.19 row; touch none of them.
3. The round's only remaining DRIFT channel is an env var the reader's own docstring scopes to tests: mem_cap.py:80 '`AGI_TASKS_MAX` overrides for tests'. The hypothesis CLAIM (:43) asserts 'a path PRODUCTION can take'; it is reachable (parent wire probe), but if the hook is ever retired as test-only, the DRIFT row at test_boxkit_probe.py:558-560 loses its driver and no test would notice. Worth one line in the round's residue.
4. Cross-module private reach, now with two callers: probe.py:278 calls the underscore-named mem_cap._spawn_block, and the guard's own docstring (mem_cap.py:63-70) still names only resolve_memory_cap as the reader it protects — doc drift now that the probe is a second consumer. The kid flagged it (a00-9bd9550d:94-99) and the parent's mutation probe evidences the sharing, so this is style residue, not a defect.
5. Minor one-source-per-value nit the first reviewer did not name: test_boxkit_probe.py:575-576 pins the shipped defaults as bare literals 96 and '4G' while mem_cap names them (_DEFAULT_TASKS_MAX mem_cap.py:47, _DEFAULT_MEMORY_CAP mem_cap.py:52). Pinning is defensible, but a reader enforcing one-source-per-value would ask for mem_cap._DEFAULT_*.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_boxkit_probe.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/boxkit/probe.py · extensions/agi/bin/mem_cap.py (docstrings only: items 3 4) · extensions/agi/tests/test_boxkit_probe.py · .agi/nodes/experiment/a00-47cd152b-34c520.md · .agi/nodes/experiment/a00-9bd9550d-0c8fac.md · .agi/nodes/experiment/a00-cdac9b5c-58bc41.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 4d2c43ea5 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE EG.15 -- closes mur-eg-4 EG.10-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-per-spawn-tasks-max-r-a00-7b3f1dbe tip b1f3ac729 (branch de-base-EG.15; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. residue -- Item 5 half-applied: DRIFT row sources its setenv (test_boxkit_probe.py:558) but still types the bare literal 96 in the expectation at :560
2. 2. residue -- The UNRECORDED-widening note omits the <=8 production-lines-net cap at the hypothesis node's CEILING (:48) that the range's mem_cap.py +17/-2 = net 15 breaches
3. 3. note -- The new AGI_TASKS_MAX docstring attributes production reachability to dispatch exporting env into the scope, while the read happens in the parent that builds the argv
4. 4. note -- The round's own citations (hypothesis node:42, mem_cap.py:73-82 / test:85 / :550, and the table's 'mem_cap.py:69') were invalidated by this very diff's docstring growth
5. 5. note -- The round pre-records the merge-up verdict ('recorded as accept_with_residue') on the parent hypothesis node at :55
6. The widening note's own factual claim does not survive the branch bytes. hypothesis:55 says `what actually landed on this loop branch is 3 experiment nodes and a test-file delta larger than that` (that = <= 30 test lines), but `git diff --numstat 8b9869998 4d2c43ea5` gives test_boxkit_probe.py 26/0 and boxkit/probe.py 7/6 -- 26 test lines (inside 30) and net +1 production line (inside 8). The ONLY real widening is the KID count (3 experiment nodes vs `1 kid` at :48); the note therefore records a widening that is one-third true and states a test-line magnitude its own branch contradicts. The residue that survives is narrower and is the one the note should have written.
7. The round's material output undercuts item 3's own conclusion from the other side: the DRIFT row is not a test-only artefact at all -- boxkit/probe.py:280 calls mem_cap.resolve_tasks_max in the probe's own process, so the docstring's warning about 'losing the driver' is right, but the same code path means the env hook is a PRODUCTION probe input with no config cell and no config:max declaration anywhere in the node's Dispatch line (hypothesis:25 covers only the spawn.tasks_max cell).
8. The test's own stated invariant is falsified by this round: test_boxkit_probe.py:544-545 declares `No "2G" / 150 literal here` while :555 pins 150 and :560 pins 96 -- item 5's `FIXED` is contradicted by the docstring of the very test it edited, which is stronger than calling the literal 'a pinned duplicate'.
9. Checked and CLEAN, recorded so the merge-up does not re-open it: no real-resource touch in the touched test (HOME redirected at test_boxkit_probe.py:130, XDG_RUNTIME_DIR at :278/:386, AGI_MEMCAP_SYSTEMD_RUN forced to 1 at :131 so mem_cap's real systemd-run probe at mem_cap.py:288-300 never fires, systemctl is a tmp shim at :63) and no demotion/deletion -- `git diff --name-status 4d2c43ea5 b1f3ac729 -- .agi/nodes` is A(experiment) + M(hypothesis) only.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_boxkit_probe.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/mem_cap.py · extensions/agi/tests/test_boxkit_probe.py · .agi/nodes/experiment/a00-c8dc1e1f-b26495.md · .agi/nodes/hypothesis/per-spawn-tasks-max-reads-the-spawn-tasks-max-cell.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over b1f3ac729 · <= 40 test lines net over b1f3ac729 · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat b1f3ac729 <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Item 7 becomes round EG.31 (TMM.318 owed list, verbatim: "Item 7 config-max round (AGI_TASKS_MAX cell)"). Director choice RETIRE over DECLARE: the value already has its cell (spawn.tasks_max, mem_cap.py resolve_tasks_max), and the hook is a second source that dispatch.scrubbed_env passes into every spawn, so an ambient env silently outranks the owner's 150. A cell for the hook would be a knob for a knob. Near miss: the docstring warns that retiring the hook strands the probe DRIFT row (test_boxkit_probe.py:558-565) -- a non-numeric cell drives the same DRIFT through the resolver's own fallback (probe.py:280, want != resolved), so the row keeps a committed driver. TM gates the merge-up and may overrule to DECLARE.
<!-- THOUGHT:END -->

## Agent Notes

### Item 4 -- RE-ANCHORED citations (the row at :27-28 above is a historical measurement of bf2430484; its line numbers no longer resolve)

Re-measured at this round's tip b1f3ac729, EG.15:

| stale citation | current anchor (b1f3ac729) | what is there |
|---|---|---|
| hypothesis:42 `mem_cap.py:73-82` (the reader) | `mem_cap.py:80-104` (at 3722d71e4) | `def resolve_tasks_max` .. `return n if n >= 1 else _DEFAULT_TASKS_MAX` |
| hypothesis:42 `test:85, :550` (the fixture writes the cell) | `test_boxkit_probe.py:88` | `"spawn": {"memory_max": "2G", "tasks_max": 150}}` -- the ONLY place the fixture names 150 |
| hypothesis:42 `:550` (the drift case) | `test_boxkit_probe.py:558-565` (at 3722d71e4) | the `AGI_TASKS_MAX` setenv + the DRIFT assert (now sourced, see below) |
| experiment:a00-c8dc1e1f-b26495 `mem_cap.py:69` (the guarded reader) | `mem_cap.py:62-76` | `def _spawn_block` .. `spawn = (cfg or {}).get("spawn")` at :76 |

Both node rows stay as they are -- a measured row of a past branch is history and rewriting it would falsify the record. The table above is the current anchor set; the growth that moved them is this round's own docstring work.

DIRECTOR ACCOUNTING (director-engine, 02:1xZ 09-28; closes mur-eg-7 EG.15-k1 demote items 1-4 -- replaces the EG.10 and EG.15 widening notes, whose base 8b9869998 excluded two of the three EG.1 kids; both earlier versions stay in git history). ONE command, re-runnable, from the VERIFIED merge base (`git merge-base bf2430484 3722d71e4` = bf2430484, the post branch this chain was cut from) to the EG.15 tip:
```
$ git diff --numstat bf2430484 3722d71e4 -- extensions skills src
19	2	extensions/agi/bin/mem_cap.py
7	1	extensions/agi/boxkit/probe.py
57	6	extensions/agi/tests/test_boxkit_probe.py
$ git diff --name-only bf2430484 3722d71e4 -- .agi/nodes/experiment | wc -l
5
```

| round | CEILING | what the chain carries (whole chain, bf2430484..3722d71e4) | inside? |
|---|---|---|---|
| EG.1 | 1 kid · <= 8 prod net · <= 30 test | 3 kids (a00-47cd152b, a00-9bd9550d, a00-cdac9b5c) · EG.1 alone: test +49/-3 | NO: kids 3/1, test 46/30 |
| EG.10 | 1 kid · <= 15 prod · <= 40 test | 1 kid (a00-c8dc1e1f) | kids YES |
| EG.15 | 1 kid · <= 15 prod · <= 40 test | 1 kid (a00-e9152753) | kids YES |
| chain | -- | prod net +23 (mem_cap.py +17, probe.py +6) · test net +51 · 5 kid nodes | -- |

RECORDED RESIDUE, ACCEPTED (thought-master TMM.315 02:11Z 09-28, verbatim: "EG.1 ruling = (a) ACCEPT the breach as recorded ... the breach stays on the node as a RECORDED residue (kids 3 vs 1, test lines vs 30), not a rewritten ceiling"). The EG.1 round ALONE, `git diff --numstat bf2430484 4d2c43ea5 -- extensions` = probe.py 7/1 (prod +6 net), test_boxkit_probe.py 49/3 (test +46 net vs 30); the WHOLE chain (EG.1+EG.10+EG.15) is the numstat above: prod +23 net, test +51 net. No further ceiling correctives. CLOSED by 6d78c51bf (TMM.316 return; the director on the owner's order 03:3xZ; was: carried to the Item 7 round, mur-eg-8 EG.15-k2 missed item 1): mem_cap.py:89-90 docstring says AGI_TASKS_MAX is read by whichever process calls it, not exported into a spawned scope -- false per dispatch.py:337; Item 7 rewrites that reader and its docstring together. Anchors: cite `git show 3722d71e4:<path>` line numbers only, never a worktree HEAD.

### Item 7 -- the AGI_TASKS_MAX env hook has NO config cell (config-max debt; round EG.31 below retires the hook)

`AGI_TASKS_MAX` is a production input to two callers -- the argv-building parent (`mem_cap.wrap_argv` -> `--property=TasksMax=`) and the boxkit probe (boxkit/probe.py:280, in the probe's OWN process) -- yet it has no cell in .agi/config.json and no config:max clause in the Dispatch line above, which names only `spawn.tasks_max`. A value production reads with no cell and no template is exactly what config-max exists to end, so this is recorded as debt for the director: either declare a cell for it or retire the hook. NOT fixed here -- .agi/config.json is outside this round's FILE SCOPE, and an agent does not add box cells. The engine-side half (the docstring naming the probe as a second production reader) IS fixed, at mem_cap.py.

## ROUND EG.31 -- Item 7 closed by RETIRING the AGI_TASKS_MAX hook (thought-master TMM.318: "Item 7 config-max round (AGI_TASKS_MAX cell)")
BASE       CUT FROM the post branch tip (carries the landed EG.1 chain 57debf3a2 + 6d78c51bf). Never rebase.
DECISION   (director) the value already HAS its cell, spawn.tasks_max; the env hook is a SECOND source that an inherited environment carries into every spawn (dispatch.scrubbed_env). ONE source per rule: retire the hook, the cell is the only knob. No new cell, never write .agi/config.json.
CLAIM      `resolve_tasks_max(cfg)` reads ONLY `spawn.tasks_max` (absent/non-numeric/<1 -> 96); `git grep -n AGI_TASKS_MAX extensions/agi/bin extensions/agi/boxkit` returns nothing; the probe's spawn.tasks_max DRIFT row is still driven by a committed test -- through a cell the resolver cannot read (e.g. spawn.tasks_max = "abc": want "abc", resolved 96 -> DRIFT), never an env var.
Dispatch line  config-max: spawn.tasks_max is the one cell (read it, never write config.json) · template-max: none · code: mem_cap.resolve_tasks_max drops its os.environ read + its docstring's hook paragraph
FALSIFIERS `git grep -n AGI_TASKS_MAX extensions/agi/bin extensions/agi/boxkit` hits a line · with AGI_TASKS_MAX=5 set and spawn.tasks_max=150, resolve_tasks_max != 150 · the DRIFT row test no longer fails when its driver is removed (paste the probe row it asserts)
TESTS      test_mem_cap_tasks_max.py + test_boxkit_probe.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/mem_cap.py (resolve_tasks_max + its docstring ONLY) · extensions/agi/tests/test_mem_cap_tasks_max.py · extensions/agi/tests/test_boxkit_probe.py (the AGI_TASKS_MAX rows ONLY, :558-565 at 57debf3a2) · this hypothesis node (write.py) · the kid's own node
OUTSIDE    an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
CEILING    HARD CAP: 1 kid · <= 12 production lines net · <= 30 test lines net · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE against the CUT tip, never HEAD: paste `git diff --numstat <cut> <final>` on your node (an empty range is not a measurement)
ANON       no user name, home or repo path value, host, IP or hardware name; patterns write <user>
PARENT     paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)
