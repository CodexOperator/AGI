---
name: agi-master-gate
description: >
  A master's gate for a director's merge-up onto its town trunk: the merge-tree / commit-tree
  landing that never stages a merge, what the range carries (config:posts cells, evidence
  demotions, kid-committed nodes), the suite on tmpfs and how to attribute a
  red, the .agi/context runs the engine suite cannot see, and reading verdicts, reviews and
  residues from the bytes. Use whenever a master gates, lands or returns a merge-up.
---

# agi-master-gate — land by SHA, prove every byte

Learned on the local-maxxing trunk (thought-master card, moved verbatim 2026-09-27 on the owner's order to offload
card traps into skills). Each entry names its incident; the rule is the line after the arrow.
Never commit a gated tree onto a moved HEAD: assert `HEAD^{tree}` == the gated base tree, else re-derive T2.

## Land a merge-up — gate, merge, push
```
merge-ups    the WHOLE history rides: list the tip's merges yourself (git log --merges HEAD..tip; one merge base = base..tip agrees) · merge by the
             NAMED tip · LAND WITHOUT A STAGED MERGE: gate M = commit-tree(merge-tree(HEAD, tip)) in a detached /tmp worktree; at landing
             T2 = merge-tree(live HEAD, tip) -- if HEAD moved, diff(gated tree, T2) = exactly the newcomer files, byte-identical to HEAD on
             them; L = commit-tree T2 -p HEAD -p tip; git merge --ff-only L; push · before the ff: the range's files must not be dirty in MAIN
             (comm -12 of the two name lists) · the range = diff(merge-base, tip), never diff(HEAD, tip) · a red suite = return the tip ·
             a pipe to tail masks a failed push's exit code (4905c6d0bf: 'failed to push' = a concurrent pusher sent the same branch; fetch + compare tips) · merge-tree --write-tree prints the tree id EVEN ON CONFLICT: read its exit status (1 = conflict) + --name-only's list, never
             line 1 alone (07:5xZ: config:posts conflict markers reached the gate; test_node_writer's live corpus caught them) · a
             rotation-cells-only conflict in config:posts = take HEAD's file verbatim once the tip's posts.md delta is proven on HEAD
             · a merge-up whose code reads a NEW config cell: check the LIVE config holds it, not the tests (every push_batches test wrote its
             own config; the live grid block had none -> TMM.141) · a code path that turns on by itself after landing (a cron line crons.py
             apply rewrites) = gate what its FIRST live run does, measured on MAIN's real data -- then watch that first run and read the remote
             · locations.shared_project_root(<any worktree>) = MAIN's .agi: a gate-worktree run reads MAIN's config -> to measure a config
             change before landing, patch locations.load_config in-process with the gated config.json
             · a PARTIAL research round may land when its node says pending by its own preregistered rule; the landing message says what is missing
             · GOALS.md and its render --check gate retired 2026-09-29 (goal:g7.16.1.4.1): no landing renders or checks it
             · commit-tree <gated tree> -p HEAD is ONLY safe when HEAD^{tree} == the gated base tree: ASSERT it and ABORT on a mismatch
               (13:31Z 09-27: the watch committed DE's gen-30 rotation between gate + land; my `[ ] && echo` printed nothing and I landed anyway
               -> reverted 3 rotation files, pushed; restored d0c1eba0b) -- else re-derive T2 = merge-tree(live HEAD, gated commit)
             · a fresh seat's first merge-tree can predate the watch's after_join record commit (~2 min after seating): re-run merge-tree on the
               live HEAD right before minting M (gen 21: the first tree differed by that record file only) · or the watch lands FIRST (gen 26:
               09:16:06Z for a 09:14:20Z seat): M's first parent = the live HEAD at landing -> the gated tree IS the landing tree
             · a re-sent tip gated BEFORE a trunk landing can CONFLICT after it (gen 26: DE e362e7947 vs DT's 6f4fb27e0, 2 osc seeds tests,
               adjacent lines, rc 1) -> both halves independent = land the UNION: temp index (read-tree the conflicted tree + update-index
               --cacheinfo the union blobs + write-tree); diff it vs HEAD (= the tip's lines only) and vs the tip (= the trunk's only); prove
               each half by its OWN test; name it in the landing message + both dms
             · after a landing the tip's history is criss-cross: git merge-base picks the trunk commit it merged, so base..tip re-lists landed
               files -> what the tip still owes = git diff --stat HEAD $(git merge-tree --write-tree HEAD tip)
             · a VALIDATION gate (write.py set / create, any refusal every post's calls pass through) = judge it over EVERY live node with the
               gated predicate + real --dry-runs of the routine writes (the briefs' own lines: brief.py, cli.py) -- a green suite cannot see it:
               the tests carry their own fixture schemas (TMM.171: 111 live (type, field) pairs would have been refused)
push         (the Prime's [rule] 02:54Z, owner 09-25; doc:unified-director-brief §2) directors' post branches are LOCAL-ONLY, never pushed; a
             merge-up names a LOCAL tip; my landing on local-maxxing/season2/main is the town's ONLY remote push; the Prime keeps local-maxxing/main
             + season2/main by SHA from it · a push's output names the remote URL: print only the ref-update line · a new seat's key row lands
             on origin/season2/main (f82730feaf, gen 21): merge it ancestry-only (tree identical) so the rotation + dispatch guards read current
mirror       rotate-self's prepare check 1 (rotate.py:16159) BLOCKS until origin's refs/agi/posts/<post> = the post branch HEAD; its
             clear = git push origin HEAD:refs/agi/posts/<post> (non-force) -- the engine's owner-ordered mirror for LOCAL-ONLY branches
             (branches.py:58-62, goal:g15.25), NOT the branch the 09-25 rule keeps off origin · precedent: DE gen 18 12:28Z, DT gen 28
             02:58Z · sanctioned for DE in TMM.193 (00:2xZ 09-26), the Prime told and may overrule
posts        a director tip can REVERT prime/owner-only config:posts cells through a 'keep own row' conflict resolution (DT gen 32's
             f751e71ced undid the Prime's 73cbe21cda model/effort on its own row) -> at EVERY gate diff config:posts rows HEAD vs the
             merged tree; when the tip's only posts delta is such cells, land HEAD's posts.md verbatim (a temp index: read-tree T2 +
             update-index --cacheinfo HEAD's blob + write-tree) and name it (e5bf88d1c7)
kid commits  DH.386 (DE, lands with e362e7947): `cli.py done` auto-commits the round's NAMED nodes -- a kid-supplied --parent resolves ANY id
             (config:posts, config:rotations, doc:unified-head, town:local-maxxing, goal:g5 measured) until DH.390 lands -> at every gate
             list changed .geometry / doc:unified-* / town:* / goal:* files and read each
anonymize    anonymize.py guards the classes named in anonymize.CLASSES (loopback exempt); the home class is anonymize.HOME_PATH_RE (ANY box, bare or with a path) -- read them there, never a list here; it takes NO file args: git diff <merge-base> <tip> > F; anonymize.py check --root <gate> --diff-file F · the model name needs its own grep: grep the added lines ('^+') for the box's GPU model name yourself (anonymize.py does not cover it; never write the pattern into a node)
             · the net diff hides HISTORY: a file ADDED then removed inside the range rides to origin with the merge (SM gen 14, 21:2xZ
               10-01: DG1 e0a261b7b untracked .agi/keys/director-general-1, but 7b37db90f had added it with a host-named comment) ->
               git log --diff-filter=A --name-only <merge-base>..<tip> lists every path ever added; read each one the net diff no longer
               shows (a key file = return the tip; the director re-cuts ONE commit from the live trunk, never a rebase)
               · scan every VERSION of a key file in the range, not only adds (a modified one can carry the host too) -- UNLESS the
                 identical blob is already reachable from origin (a push sends only objects the remote lacks: no new bytes leave);
                 name it in the landing message (gen 14: TM-new d60422468 = the blob 81d0e8729 already published, banked)
evidence     the grid cron's evidence gate (evidence_gate.enforce_on_disk) DEMOTES a proved / disproved verdict without a resolvable
             evidence_runs (a JSON list of existing type:slug ids) IN MAIN'S WORKING TREE, uncommitted, 'caught at grid commit' -> gate
             every landing's range with it: my ae2276a95c carried a00-325d4c56-bedcc8 = disproved with no evidence_runs (22:4xZ)
             · the reverse: a director's grid.py commit --all in ITS worktree runs the gate on a STALE copy and its tip carries a false
               demotion (DE 5957e5fb0f, 09-26) -- merge-tree merges it CLEANLY beside the trunk's evidence_runs -> diff every experiment
               node HEAD vs the merged tree; keep HEAD's blob (temp index) and name it · dry-run: evidence_gate.enforce_on_disk(<repo>/.agi, dry_run=True) -- the GRAPH root: <repo> alone reads <repo>/nodes = nothing = a VACUOUS 0 (gen 24's first three dry-runs; the 4th, on .agi, caught OSC.43's hypothesis: disproved with no evidence_runs)
bodies       a node landed for ONE fix still carries the loop's OTHER known errors in its body: I landed a00-325d4c56-bedcc8's
             evidence_runs fix (8732c4dc8e) after checking only the evidence -- its body still printed bits([w]) = w + 1 and a wrong 4-class
             formula -> PASS 7 DEMOTE (00:06Z 09-26) -> before landing ANY node on a loop, grep its body for that loop's corrected errors
             (here 'w + 1' / 'w+1') and check every printed formula by RUNNING the source (fixed.bits: [5,5,5,5]@32 = 6.0, [4]@64 = 4.125)
             · a director's REJECTION lands in the ledger rows but not the kid's TITLE / Files-touched table (a00-00e0f92a, gen 25: title
             'the claim row count corrected' after DT rejected it) -> read every new node's title + tables against its own ledger rows
```

## Suites and reds — run, attribute, never guess
```
suite        ON TMPFS (09-26): git worktree add --detach /dev/shm/<gate> M + TMPDIR=/dev/shm/<tmp> (chmod 700) (NEVER a tmp name that starts with the gate path: test_commands' ENGINE_ROOT substring check reds -- gen 27, /dev/shm/gate-mu9 + gate-mu9-tmp) -> no disk writes, 13:20; remove both after (STOPPING one = kill every pid whose /proc/<pid>/cwd is the gate path, THEN remove
             it: a test spawns pytest in its OWN session -- gen 26's orphan 2318135 reddened DT's test_suite_no_detached_spawn) · suite        env -u TMUX -u TMUX_PANE, setsid nohup in a ( subshell & ) + a pid waiter (run_in_background) · create the worktree in ITS OWN
             call · 14:25-15:28 at load 2-6 (6413 passed 00:5xZ 09-25; 14:36 at load 3-8, 6433 passed 11:59Z) · foreground sleep is blocked: wait
             with a background loop · a bare 'cd' in a Bash call can stick as the session's cwd -- use absolute paths or cd back to /data/work/agi (gen 24 did it again with a `cd .agi/worktrees && ...`: the session cwd moved; pass absolute paths instead) · grep here is UGREP: a long alternation regex fails ('exceeds complexity limits') -> extract with python re
             · the ENGINE suite's cwd = INSIDE the gate tree (tests resolve the project root from the pytest cwd): a neutral cwd (/dev/shm/tmp-*)
               = 33 failed + 3 errors, every one 'no .agi project root' / 'record root must resolve' (20:06Z 09-26); the neutral cwd is for
               the osc / context runs only -> ( cd /dev/shm/<gate> && env ... setsid nohup python3 -m pytest -q -p no:cacheprovider -rf extensions/agi/tests/ )
             · pgrep -f pytest matches the claude + rotate-wrapper processes (their argv carries the startup prompt): find a live suite by
               comm + cwd (python3 in a worktree), never by the pattern count
             · a 2nd pytest in a worktree whose full suite runs = ERROR at setup (conftest _suite_lock_guard names the live pid), not a result:
               reproduce red in a separate pre-fix worktree, read green from the suite (+N passed = the new cases)
lanes       the FULL suite is PYTEST ONLY: the extensions/agi/tests/*.t.sh lanes never run in it (DG1 [red] 14:06Z 10-08: D1 v2 38e61463c7
             landed green on FULL and left graph-metrics.t.sh c2/c2b red -- its gold pins metrics.py output) -> at EVERY gate run ALL .t.sh lanes
             bare (env -i, empty HOME, git config /dev/null, node's dir on PATH, `sh`) on the gate tree AND a detached trunk tree, diff the two
             FAIL sets: a lane red on the gate only = the range's · and `git grep -l <changed output> -- 'extensions/agi/tests/*.t.sh'` before any
             landing that changes a CLI's printed lines
detached    my setsid-nohup suite fails 3 tests that pass alone 5/5: test_dashboard::test_watch_exits_cleanly_on_sigint + 2x
             test_suite_no_detached_spawn -- the LAUNCH, not the range (3 gates 09-26, 6455 passed each; a director's in-pane run = 6458/0)
             · gen 26 (a125bad37's gate, the tree with DH.381's conftest guard): 6642 passed / 0 failed -- NONE of the 3 appeared: re-attribute
               before calling a red 'environment' again
             · WHY (DE 09:08Z): test_suite_no_detached_spawn scans the BOX for any detached pytest -- it finds the gate suite itself, and a
               director's suite fails the same way while MY gate suite runs; it passes alone only when no detached suite is up
             · an ORDER-DEPENDENT red passes alone: two modules named paths (extensions/agi/bin/paths.py + .agi/context/local-maxxing/paths.py)
               -> an earlier test caches one in sys.modules and a later bare `import paths` gets it (DH.385's test, gen 25); a director's
               targeted run cannot see it -- only the full suite; attribute by the traceback, not by 'passes alone'
             · test_crons_log_cap_long_lived_writer::test_f1_rename_mode... = a load flake (the test_f1c race at another site; gen 27: 1 red
               in the full suite, 5/5 alone) until DE freezes its writer (TMM.241)
reds         attribute each: which range touches the test / its code (git diff --quiet <base> <tip> -- <file>) · re-run it ALONE (a load
             flake passes alone) · run it on MAIN + another range too: red there = the trunk's · test_thought_hygiene counts node_writer.thought_blocks per node (BOTH markers at column 0; the column-0 BEGIN count must equal it): an indented or inline quoted marker never trips it
context      a green main suite + verification's context suite (system python, NO torch) cannot see a .agi/context regression that only a TORCH
             python hits (MU8's guard: 16 errors) -> at every gate touching .agi/context/conftest.py or a context test's imports, run DT's seeds
             tests with the osc pythonpath from a neutral cwd in the gate tree -- never the whole context dir under torch during a model hold
context+     the ENGINE suite never runs .agi/context: a merge-up that RE-EMITS datasets can red an older round's context test that pins the
             artifact's shape (gen 28, TMM.254: 8 uniform rows vs 4 pinned; a join shape) -> at EVERY merge-up with datasets / context /
             conftest changes run the RANGE'S OWN context tests (git diff --name-only <merge-base> <tip> -- '.agi/context/*test*.py') plus any
             older test that reads a re-emitted dataset, ONE FILE AT A TIME under the osc pythonpath from a neutral cwd, each under `timeout`
             + the memory guard, with no model round running -- NEVER the whole .agi/context dir (SM gen 12, 16:0xZ 10-01: it forked 273+
             python3 that never exited, 9.4 GB anon, mem PSI full avg10 33, the Prime SIGTERMed 295 processes; a pytest `timeout` kills only
             the parent, its children live on -- stop = every pid whose cwd is the neutral dir)
             · two gates PIPELINE: gate the 2nd on a PROVISIONAL landing of the 1st (commit-tree, no ff); the 1st fails -> land the 2nd ALONE:
               its extensions/ identical = the engine suite carries; re-run only the range's own context tests (gen 28: DE mu 13 landed alone in ~6 min)
             · the trunk's autouse model guard stubs only modules imported BEFORE a test: an in-body import passes alone and is refused in file
               order once an earlier file imports the real one (DH.413 closed it: import hook + allow_model_load)
fixtures     an experiment's own _test.py: PYTHONPATH=/data/ml/.venv/lib/python3.12/site-packages:/data/ml/scratch/osc03/pylib python3 -m pytest
             <test> (= paths.local_maxxing.osc_test_pythonpath; numpy lives in the osc03 pylib -- the venv's own python has no numpy) · a model
             swap between arms = check the model dir each bench row loaded ('hf'), not the label · the config cell holds {ml_venv_dir}
             placeholders: a python read of it is NOT a path (gen 25's first run: numpy missing) · a deliberate break runs in a SECOND
             detached tmpfs worktree of M (158 MiB): paths.get_local resolves inside that tree (brain_swap_out_dir = <wt>/datasets/...),
             so a mutated log / node / script never touches the gate tree its suite reads; restore with git checkout, status clean
fixtures+    a fixture test's xfails can leave its LOAD-BEARING assertion dead (OSC.43: PASS 8 found the ordering assert dead in all 3 cases after I re-derived only the numbers) -> run it and show the assert executes (pytest -rx; a deliberate break must turn it red) · a verdict resting on a PASS-demoted round's log is weaker than its number
```

## Verdicts and reviews — read the bytes, not the report
```
verdicts     read the CONTROL arms before any verdict: a result FLAT across bit budgets while the controls hold = an allocator or harness bug
             (OSC.23 -> TMM.139) · an arm's NAME is not its budget: read each arm's class widths / bits (fixed.arm mode 'uniform' = sizes [n] =
             every pair at w[0], the TOP width; arm(ones, ...) = index order, argsort of equal energies = identity = the fastest rotary pairs
             widest) -- a control must match the budget; random = the structure-blind control · a harness's recorded actual_bits can be the
             tag, not the arm's truth · results rows: results.json 'bench' = a jsonl path OR inline 'rows' [{prompt, arm, tag|arm suffix, agree,
             kl}] -> mean over prompts per arm x width
             · a claim's NAMED control must be matched to what the arm ALLOCATES in the script: index_order = src ones = positional grouping,
               NOT 'uniform' -- I landed batch 21 'proved' on that miss, PASS 6 demoted it (TMM.167); read the claim's control word against the arm code
             · a round's correction can live only in Agent Notes / THOUGHT while the BODY keeps the kid's false claim (OSC.31: 'w + 1'):
               the body is state -> return it for the rewrite before landing (a PASS demotes it as an overclaim)
             · a TAG is not a budget: compute bits() of the widths yourself (weighted mean width + 16 bits of scale per class over the pairs) -- the '7.75' known cell was [13,13,10,10] = 11.75 (TMM.150/151's premise, corrected in TMM.154)
review       read each round's FINAL verify stage in .agi/sessions/workflows/runs/mur-*/verify_R-EFnn.json · no mur under the hold = read the
             director's in-place review AND the diff yourself, and say so · agi-research-review PROPOSE-ONLY: the refute stage reads 0 of the
             brainstorm's proposed_hypotheses -> read runs/rr-*/brainstorm_*.json yourself (FIXED: goal:g7.33.12 complete, read gen 27)
             · a mur's focus names it: reviewer probes run with a scratch HOME + XDG_CONFIG_HOME, never the box user's (belam [rule] 09:4xZ 10-08)
residues     before routing a residue to ANOTHER director, read the newest dm of the director whose round produced it (gen 25: DT's 2/3 at
             08:01Z had already fixed the model_slot flock item I routed to DE at 08:0xZ -> TMM.215 took it back)
             · accept_with_residue ≠ land (unified-director-brief:32) · NEVER waive a mur residue -- the owner's 09-19 rule gives each its own
             corrective round (my TMM.108 slip, corrected in TMM.110) · a director may land on the trunk itself (DT gen 19, 06:0xZ): compare
             HEAD with the director's claimed trunk sha before gating; the docs forbid it (unified-director-brief:64/73) · a director's
             rescue story can contradict my own stop record (OSC.15, 17:1xZ: 'OOM' vs TMM.123) -> check the kid's iter-<ID>/manifest.json
             (harness, started_at, finished_at, death) in the director's worktree against the node BEFORE gating
             · before any return of a prose brief: ONE whole-node contradiction sweep, all residues in one list (belam [rule] 08:4xZ 10-08)
PASS         the Prime's PASS launcher WAITS while any suite lock is live (belam 1d3aba877, 13:48Z) -- a /dev/shm gate worktree's suite holds one
             too -> never start a gate suite in a PASS start window; stop a returned tip's suite at once
             · a PASS's mur runs import MAIN's LIVE workflow.py (3 runners, cwd MAIN, 16:0xZ): a workflow.py landing mid-PASS changes every chunk
               launched after it -> land mid-PASS only when the mur shape (no extends, no round stage) runs unchanged (gen 27, merge-ups 9 + 10)
```
