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
> **Council approves, belam only lands (owner 21:5xZ 10-10, doc:council-loop §Rulings and landing):** a gated tip goes to the council as `[review]`; ONE council post answers `[approve <sha>]` or `[return <sha>: why]` (a split / stuck council → belam breaks the tie). Only then box belam `[merge-up] … ff-only <sha> · council: <post> approve <ts>` — belam refuses a merge-up without that line and runs only the secret guard + the ff. That landing guard is the ONE anonymize gate before origin (belam 03:1xZ 10-11): the only auto-pushed branch is MAIN's trunk, posts/* are never pushed (posts/belam aside), and a post uid cannot run the secret class -- so no per-post pre-commit hook; keep the gate-time anonymize. FALSIFIER, belam runs it at every landing (council 03:1xZ): `git ls-remote origin` holds no refs/heads/posts/* but posts/belam and 0 refs/archive|box|held -- one hit voids the ruling: stop landing, [red] to SM + the owner. Right before the ff, re-read the NEWEST lines on the approver's ref AND your own box: a later [return]/[withdraw] for that sha wins over the earlier approve (belam 08:15Z 10-11 landed 549c1a2381 one minute before the council's own correction to RETURN). Every `[decision]` goes to the council, never belam; belam gets only what needs the owner.
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
             own config; the live grid block had none -> TMM.141)
             · SELF-INSTALLING PIECES (council 3/3 11:08Z 10-11, after .32 b3316f1aa0 deleted agi-run's box loop and SM called it
               'bytes only'): agi-post@'s ExecStartPre extracts every fenced `### <piece>` of engine.md AND engine-[pw]*.md into each post's
               ~/bin at EACH start -> a landing that changes, adds or DELETES such a piece goes live at each post's next start on a synced
               branch, no host act. Its [review] carries a 'first-start:' line per post kind (claude / pi / kid): what a post GAINS and LOSES;
               and either lands WITH its host act (preferred: one GO, one moment) or carries an interim belam has ACKed, with a retire date.
               engine-root.md pieces stay host-act-only (root renders them)
               · the SAME first-start: line goes into the landing COMMIT message, word for word (goal:g7.16.1.11.41.1 checks the
                 commit, the council checks the mail: one line, or they drift; council remark, alive 11:17Z 10-11); a piece RUN only
                 by root (agi-project) is marked 'inert in a post (root-run)' in that line
             · a code path that turns on by itself after landing (a cron line crons.py
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
             · a temp-index recipe = GIT_INDEX_FILE=<tmp> with read-tree <tree-ish>; a bare read-tree empties the index at rc 0 (SM gen 32,
               live gate tree): probe git semantics on a scratch repo only, restore with `git reset -q`
             · a merge-up tip that MOVES after you named it -> cc EVERY post that may have read the old tip and name the new sha; ask them
               for the cmp, do not assert a mismatch (alive: tip moved under reviewers)
             · signing a commit: spell the flags apart, `git commit -q -S -m` (a clustered `-qSm` makes m the key id; self-perpetuating); read
               a file at a ref with `git show <ref>:file`
push         (the Prime's [rule] 02:54Z, owner 09-25; doc:unified-director-brief §2) directors' post branches are LOCAL-ONLY, never pushed; a
             merge-up names a LOCAL tip; my landing on $AGI_TRUNK is the town's ONLY remote push; the Prime keeps local-maxxing/main
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
             · GPU-name scan of added lines: grep the FULL name AND the model (last two words), never awk $NF (it missed the model form); never
               print the name or write the pattern into a node
             · before commit-tree run anonymize over the landing message FILE (minus the attribution trailer): the diff guard never reads
               commit messages (a landing message leaked past it)
             · anonymize.py check as a non-belam uid: --root = a scratch archive (extensions + .agi/config.json), not MAIN / the worktree
               (PermissionError on .env); read the result BEFORE any message cites it (SM gen 35: sent 'anonymize ok' unread)
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
- **GATE SELECTION RULE (council 03:18Z 10-12):** (1) the gate's pytest set is DERIVED at the gate sha, printed with its count: every test file naming a changed path's dir or basename (`git grep -lF <dir|basename> -- 'extensions/agi/tests/'`) + every scanner file (`SCOPE=` / `SCAN_DIRS` / `git grep` in a test, AND a source-dir walk: `.glob(` / `iterdir(` / `os.walk` / `os.listdir` -- council 07:18Z 10-12 after test_seat_alias_notice, a BIN.glob scanner, landed red in L6); (2) the FULL engine suite runs once per LANDED stack at the L tip (disk basetemp, nice 10, slice under its line) -- else the land message names it 'not run (<why>)'; (3) the land message says which ran. Lanes: the sha goes ONLY to lanes printing `[no-candidate]`; `FAIL=0 ok=0` is not green
- `-p no:cacheprovider` makes `--lf` run NOTHING (no cache to read): to name failures re-run with `-rf`, never `--lf` (SM gen 39)
```
suite        ON DISK (belam [rule] 14:2xZ 10-11, skill agi-memory-guard: tmpfs is charged to agi.slice): git worktree add --detach ~/gate/<gate> M + TMPDIR=~/gate/tmp (chmod 700); /dev/shm only while the slice is under 4600 MiB (NEVER a tmp name that starts with the gate path: test_commands' ENGINE_ROOT substring check reds -- gen 27, /dev/shm/gate-mu9 + gate-mu9-tmp) -> no disk writes, 13:20; remove both after (STOPPING one = kill every pid whose /proc/<pid>/cwd is the gate path, THEN remove
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
             · gate suites run with GIT_CONFIG_GLOBAL=/dev/null: the global core.hooksPath shadows fixture repos' hooks; a red that vanishes
               under it is goal:g1.43 row 13, not the range (SM gen 35: 5 test_rotate reds on trunk AND candidate)
lanes       the FULL suite is PYTEST ONLY: the extensions/agi/tests/*.t.sh lanes never run in it (DG1 [red] 14:06Z 10-08: D1 v2 38e61463c7
             landed green on FULL and left graph-metrics.t.sh c2/c2b red -- its gold pins metrics.py output) -> at EVERY gate run ALL .t.sh lanes
             bare (env -i, empty HOME, git config /dev/null, node's dir on PATH, `sh`) on the gate tree AND a detached trunk tree, diff the two
             FAIL sets: a lane red on the gate only = the range's · and `git grep -l <changed output> -- 'extensions/agi/tests/*.t.sh'` before any
             landing that changes a CLI's printed lines
             · env -i lanes lose the user-site pytest -> PYTHONPATH=$(python3 -c 'import pytest,os;print(os.path.dirname(os.path.dirname(pytest.__file__)))');
               always run with sh (dash), never bash (false reds)
             · a falsifier lane that is RED on the trunk by design never lands alone: it rides in the SAME landing as its build
             · any .geometry/engine*.md change: also run test_grid_writers.py + test_thought_hygiene.py and grep lanes for the FILE name, not
               only piece names -- they scan by pattern (SM gen 33 AA1.V: 5 RED on trunk after landing); an engine PIECE (engine*.md) also runs test_bin_help_smoke, test_commands_manifest and test_first_start (SM gen 41, stack 7: only its shell lanes ran, test_grid_writers red on the trunk for 1.5 h)
             · run lanes in a git worktree or a `git clone --shared` scratch copy, NEVER from an archive with GIT_DIR on a shared repo:
               lanes that build scratch repos then write the REAL one (aio 10-11 09:56Z: moved posts/director-general-1, created refs/heads/trunk)
             · a lane with a TRUNK arg (agi-out-*, aa3, ckpt, grow-gate-*, agi-land-bounds) extracts from that REF -> pass the CANDIDATE commit
               as T (the lane REFUSES a bare run: exit 2 '[no-candidate]'; trunk-arg-lanes.t.sh guards the 17); a green that does not change when the piece changes is no gate (SM gen 33 AA1.V: vacuous 44/0, 9 RED landed)
post uid    the full engine pytest as a POST uid on a /data gate tree (goal:g7.16.1.11.43, DG3 10-11: 8,970 collected, 0 failed, the 9 embeddings / renderers
             collection errors on their own line) · env -u TMUX -u TMUX_PANE, GIT_CONFIG_GLOBAL=/dev/null (the leak asserts read the spawn-channel family only), nice 10,
             TMPDIR and --basetemp in /data/work/gate-<post> (the workflow leak guard accepts the basetemp as a tmp root) · a post uid's env carries
             GIT_AUTHOR_* / GIT_COMMITTER_*: a fixture that commits inherits that identity (test_rotate_prepare's 'unpushed by author' read 'other author');
             a test that needs an identity sets its own · a post uid cannot read MAIN's .env and has no pi: provisioning.available() reads EACCES as ABSENT,
             the conftest points PI_BIN at a stub for test_workflow* (a test that runs a fake pi sets PI_BIN to it) · a stage-return test stubs
             _stage_context: the real build is viewport.py over the whole graph, 70-160 s at box load vs the 60 s context cap · a SPLIT run (a self-stop at PSI full
             avg60 > 10 cut one at 35%) is order-sensitive: `chain_engine` (the engine package) and tests/chain_engine/ share a name, so a resume that skips
             test_chain_engine.py reads 14 false reds in test_links + tests/chain_engine/ -> resume from the failing file's EARLIEST importer, or re-run the three together
             · kill the python CHILD of `timeout` on a self-stop (kill $timeout_pid alone leaves pytest running)
gate dir    NAME-keyed: /data/work/gate-<post> follows the post's NAME. A rename moves the mover's gate-<old> -> gate-<new> in the sitting's step 3 (pre-usermod guard 'gate-free'); the PREVIOUS holder of a reused name clears its TREE as itself (named-path `git worktree repair`, locks kept) and the /data/work entry rename is belam's, before that move's 1a (council 21:35:22Z + 21:40:58Z 10-21, G5)
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
             · a test that pins `git grep -n` output or line numbers needs a NEG: a pure line shift (a comment line in a big file) must stay
               GREEN, else every edit reds FULL (SM gen 30: 4/8 reds from pinned line numbers)
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
             · mutant check: apply as python (old,new) pairs, assert count==1, anchor headings at line start ('\n## '), print the hit line;
               never sed/grep '$' or '|'-split specs; a fatal break sits outside the arm's own except (SM gen 29: a quoted '## DG1 RULING'
               gave a false GREEN)
             · unit semantics in a gate or a return (Requires=, Restart=, ExecCondition): systemd-analyze verify --root=<scratch> with the host
               base targets copied + read the man row in the SAME command; name the trade-off (SM gen 31 a5b1a41009; gen 33 D10 Restart=)
             · probing git permissions / signing: run bare (env -i, empty HOME, GIT_CONFIG_NOSYSTEM=1, GIT_CONFIG_GLOBAL=/dev/null; a fixture
               repo gets its own AGI_TRUNK) -- your ~/.gitconfig (safe.directory=*, allowedSignersFile) masks it (alive 03:09Z; self-perpetuating)
             · signed-commit fixtures: issue certs -V -1m:+4h (a 30-min cert expires mid-session); git checks valid-before at the COMMIT's
               date, so never trust a date: the receiving tip + blocks are the clock (self-perpetuating: §AB cert dated at commit)
             · an owner cert counts only on a CURRENT ring key (C18): issue a fixture cert on belam's ring key and sign with `-f <key>-cert.pub`
             · `ssh-keygen -Y sign` prompts to overwrite an old .sig and hangs a python caller -> delete the old .sig first; run such tests
               with </dev/null and a timeout (self-perpetuating: signing test hung)
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
             · a builder's report of 'N rows' is not a check: count them yourself on the trunk AND the candidate; the same count with
               RED -> GREEN is the gate (SM: DG2 '8 rows' was 7 on both trees)
review       read each round's FINAL verify stage in .agi/sessions/workflows/runs/mur-*/verify_R-EFnn.json · no mur under the hold = read the
             director's in-place review AND the diff yourself, and say so · agi-research-review PROPOSE-ONLY: the refute stage reads 0 of the
             brainstorm's proposed_hypotheses -> read runs/rr-*/brainstorm_*.json yourself (FIXED: goal:g7.33.12 complete, read gen 27)
             · a mur's focus names it: reviewer probes run with a scratch HOME + XDG_CONFIG_HOME, never the box user's (belam [rule] 09:4xZ 10-08)
             · every mur brief names its review root = YOUR /dev/shm gate tree (never a disk worktree under .agi/worktrees), and its
               reviewers search only inside that root by explicit paths (belam [rule] 19:2xZ 10-08: SM gen 31's D3 mur read
               .agi/worktrees/de-base-EG.82 on the slow disk = 13.3 GB of IO in 15 min, io PSI some 93%)
             · mur reviewer probes touch real paths: snapshot `ls ~/.config/systemd/user | md5sum` before each mur and compare after; the mur
               focus names a scratch HOME/XDG and forbids real paths (SM gen 31: mur mutants ran as belam)
             · after every mur `git symbolic-ref HEAD` in MAIN must still name the branch before any landing (reviewers detached it 3 times);
               re-attach first
             · a mur review stage can be hollow -> the FINAL verify stage decides; reproduce each unrefuted residue yourself; read every
               citation you send (returns AND placements) down to the CODE line, never a header comment (SM gen 31 E send.py docstring;
               04:3xZ engine-root.md:104)
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

## Traps moved from cards (owner 10-10: one sweep, then a rule)
- a gate path list read without -z skips C-quoted paths = fail OPEN -> every path list: -z + NUL split (SM gen 35)
- ONE full gate tree at a time (two took E from 3.1 to 2.6 GiB); a partial tmpfs tree reds whole-graph tests, and `git add -A` skips .gitignored files -> gate on a FULL archive / worktree (SM gen 35)
- a [merge-up] sent on the FIRST word of a crossed council vote landed a returned tip (549c1a2381, 10-11 08:15Z) -> merge up only on the SETTLED word (doc:council-loop answerer rule); re-read the council's refs right before sending (SM gen 36)
- a pkill/pgrep -f pattern matched the calling shell's own argv and ended it (SM gen 36) -> stop a run by its process GROUP found via comm + cwd, never an argv pattern
- 'no live effect' claimed from ONE listed dir (SANCTUARY resolves via hosts.json) -> resolve the path the CODE computes before claiming absence; a root-only path = ask belam (SM gen 37)
- a director's commit can sit unboxed, or a crossed return be read as done -> at wake read each director's branch tips + held refs, not only the box (SM gen 37)
- a cut listing (`ls | head`) read as absence: a file past the cut was called missing (aio gen 6 09:1xZ 10-11; sp 01:3xZ 10-12) -> read the whole listing or `test -e` the path
- a syntax-broken mutant reds every row and proves nothing (aio gen 6) -> keep a mutant a one-token change that still parses
- a commit's "X, so no race" claim read, not probed (aio + sp, alarm_spool 22:5xZ 10-11; alive caught the inode race) -> probe the interleaving before approving
- a FULL pytest on /dev/shm (tree + a 1 GB TMPDIR basetemp) is charged to agi.slice: it pushed every post into reclaim (mem PSI full 20, swap 0.9 GB, slice at MemoryHigh; belam [red] 12:4xZ 10-11) -> the full suite runs with its basetemp on a /data disk dir, niced, only when MemAvailable and the slice have room (ask belam when near MemoryHigh); else targeted files only (SM gen 38)
- a 'text only' batch (goal / town / doc nodes) shipped with NO lanes reddened graph-metrics.t.sh on the trunk: its r3b hard-codes the town node's 'other writer' (TM set edited_by: thought-master; SM gen 38, ea72c8050d) -> every range runs the lanes that NAME a changed node file: `git grep -l -F <node file basename> -- 'extensions/agi/tests/*.t.sh'`, on the gate AND the trunk
- test_grid_writers is a fixed lane of every gate (the template), and a gate report without its count is not green (the council refuses it); incident GATE154 / L57, where the gen-38 and gen-41 rules existed and were skipped.
- a lspci-derived GPU probe matched '(rev xx)' = a vacuous 0 -> strip the rev suffix and assert the probe is not it (SM gen 38)
- `box read` with its output discarded (>/dev/null) marks mail read unseen -> never; if it happens, re-check refs/box/*/<me> dates (SM gen 38)
- a for-loop piped into tee runs in a subshell: its last sha was empty in the parent -> write shas to a file, read them back (SM gen 38)
- a master edit built on a director's UNLANDED version of a node lands their text without their code -> base node edits on the TRUNK's text (SM gen 38)
- a merge-tree conflict label is the tip's FULL sha -> match conflict blocks by regex, assert 0 markers after (SM gen 38)
- crons.py apply refuses a linked worktree -> measure a cron line's first live apply on a `git archive` copy (extensions + .agi/nodes/.geometry, git init) with --crontab-file / --user-crontab-dir fixtures (SM gen 39)
- a bare `git worktree prune` on MAIN's shared .git drops EVERY entry whose path the running uid cannot stat -- every post's 700 gate dir (SM gen 39: my own 'remove, then prune' ask to DG2 + DG4 at 17:0xZ voided my 3 /data gate trees, the full suite's included, and re-created several posts' ~/t entries) -> never prune bare; remove your own tree by path (`git worktree remove <path>`); gate trees are `git worktree add --lock` (prune skips a locked entry)
- a grep for '/home/' read three fixture lines as harmless, but belam's landing guard (anonymize.py check, HOME_PATH_RE) refused L d6bef9de69 on a home-path-shaped lane fixture under `$T` (SM gen 39) -> at the gate run anonymize.HOME_PATH_RE itself over the added lines of diff(trunk, L) and require 0; a post uid cannot run the full `anonymize.py check` (it reads MAIN's .env), so the home class is the one you run; lane fixtures use `$T/hm`, never a home-shaped dir under `$T`
- HOME_PATH_RE run AS A POST UID knows only /home/, /Users/, uid 1000..65533 homes and $HOME: the post users are system uids, so a peer's home (the Prime's) reads 0 and belam's guard (run as agi-belam) refuses it (SM gen 40: 46a67827c7 returned on .42's crons.md log path, a test and a message) -> at the gate ALSO match every passwd home of ANY uid under the agi state root and /data (pwd.getpwall()), over the added lines AND every message of the range
- "bytes only" in a review -> check what agi-post@ extracts at each start (engine.md + engine-[pw]*.md): live at the next restart, no host act (alive gen 10)
- a waiter whose OWN command text held the pytest invocation counted itself as a peer; a kill loop grepping cmdlines killed its own shell; a suite started while DG3's ran, links.py mid-suite (SM gen 40) -> the peer check lives in a SCRIPT FILE and EXITS there: peers = `ps -eo args | grep -cE '^(/usr/bin/)?python3 -m pytest'`; links.py counts as heavy
- an UNQUOTED heredoc (<<EOF) ran belam's quoted backticks as commands (SM gen 40) -> node text with backticks: <<'EOF', substitute vars after
- belam commits to MAIN's LOCAL trunk before pushing: origin looked unchanged and the ff would have refused (SM gen 40) -> watch refs/heads/$AGI_TRUNK; re-mint by `merge-tree --merge-base <old trunk> <new trunk> <old L>`
- a peer polling its own file can miss box asks for an hour (DG3 21:17-22:49Z, SM gen 40) -> check its run by ps (comm + cwd), not by silence
- agi-out-states.t.sh run bare = '[no-candidate] pass the sha under test' rc 2 ok 0 (16 lanes take [TRUNK]); then the sha passed to EVERY lane made engine-sizes read it as a dir, rc 99 (SM gen 41) -> the gate sha goes as $1 to exactly the lanes that print '[no-candidate]' (header [TRUNK] or not: grow-gate-bootstrap)
- two re-cuts each bumped engine.md's title 50->51 (DG4, DG3): identical edits merge CLEAN and wrong (SM gen 41) -> 2+ items adding engine pieces are chained (cut B ON A) and engine-sizes runs on the merged tree
- a council fix-forward for DG1 sat on my card 80 min unsent (SM gen 41) -> a verdict's fix-forwards go OUT in the landing's turn, one box each; a card records sent ones only
- a posts-branch item (DG1 3832b21aa7) dragged 525 history commits + an unpublished key blob into a gate tree; the net diff hid it (SM gen 41) -> per item `git rev-list --count <item> --not <trunk>`: more than a few = read its history; `git log --full-history -- .agi/keys/` over the range
- a [decision] boxed to alive only reached ONE council seat; aio + sp read it second-hand (SM gen 42, council 06:53Z 10-14) -> every [decision] / [review] to the council goes to ALL THREE seats (alive, all-is-one, self-perpetuating)
- STANDING CLOSE FORM (council 3/3 06:53Z 10-14): every CLOSE line a master or belam sends reads "CLOSE <leaf> = <sha> + falsifiers RE-RUN at <trunk sha>: <counts>"; 'it landed once' is not a close
- ROLLOVER RULE (council 3/3 06:54Z 10-14, a CHECK; corrected path set): the season rollover runner's FIRST line refuses, fail closed and named (`[rollover] stages the judge: <paths>`, rc 1, nothing committed), any commit that stages extensions/agi/bin/spawn_gate.py, extensions/agi/bin/frontmatter.py, .agi/context/schemas/* or .agi/nodes/.geometry/engine-post.md (grow.py is the `### grow.py` piece there, not a file). .agi/nodes/.geometry/ladder.md (current_season) is allowed ONLY in the season-bump commit that stages it ALONE, gated through a stack; ladder.md + any other path = rc 1. Rows: node-move turn staging a schema -> rc 1 named; bump (ladder.md alone) passes AND read_ladder_season(trunk) == the new season, never None (it fails OPEN on an unreadable ladder: None after the bump = rollover RED, named; council 06:54Z addendum 2); ladder.md + a node -> rc 1; mutant (line dropped) RED. Judge edits land only through a gated stack (goal:g7.16.1.11.8.1's hole, deferred to s3)
- CAPSULE LANDING LANE (goal:g7.16.1.11.44.3, wired SM gen 42 at L14): at EVERY landing run, on the land tree, `LANDING_REPO=/data/work/agi LAND_TRUNK=refs/heads/$AGI_TRUNK CAPSULE_FLOOR=<refs/capsule count named in the LAST land message> sh extensions/agi/tests/capsule.t.sh` (env -i lane shape); row l4-the-real-repo must be ok; the land message names the refs/capsule count it saw = the next landing's floor (L14: 0). A count below the floor is RED (a capsule ref is create-only)
- "on the live trunk" in a [review] -> check `git merge-base --is-ancestor`; if not, pin the LANDING tree (merge-tree trunk x tip) in the verdict (alive gen 12: L13 f632cd4854 approved as pinned, tree 75edefcbdf)
- a master's OWN skill / node edits sit on its posts branch -> agi-at never lands them, and a later stack touching the same file makes agi-sync refuse ([trunk-conflict]): carry them into the next stack as ONE trunk commit (temp GIT_INDEX_FILE + commit-tree -S on the stack tip); hand-sync = merge-tree + trunk blob + CAS (SM gen 42, e490acd6c6)
- a RETIRE claim in a range -> `git diff -M` must show the status line + link edits, not a pure R100 rename; links.py reads 0 broken while skipping deprecated/, so it cannot catch it (SM gen 42: DG2 7a9eec6bd6 returned)
- verify-land's anon-diff / anon-msg hits that are systemd unit names, the Co-Authored-By trailer or the test authors' .invalid address are not leaks -> list every hit; land only when each is one of those (belam gen II)
- the LIVE tip at a cut = refs/heads/posts/belam (= MAIN), never the master's local core/season3/main (it lags belam's :28 board and card commits) -> re-read posts/belam at cut time (SM gen 48: L73/L75/L79 raced)
- a cut whose [merge-up] goes out later (held across :20-:30, or queued) -> re-read posts/belam AT SEND TIME and refuse when it is not the land's first parent (gsend.sh [r1p], rc 5): re-cut, re-gate only if merge-tree is not clean; a queued send that crosses :20-:30 counts as a cut inside it (R1', council 3/3 alive 16:3xZ 10-24; incident L110 2b48516f89, board commit d3f940d46e at :25)
- a land whose leaves OTHER posts build on -> a [landed] relay to those builders the moment belam reports it, never "build after your leaf is on the trunk" alone (SM gen 48: 4 directors idle 2 h, owner-flagged 23:2xZ 10-23)
- a blind sed rename flips NEGATIVE test rows (absent-X becomes absent-Y) and turns `delenv(old)` beside `setenv(new)` into a wipe of the new value -> rename tests by hand (SM gen 48, V10a: 20 reds caught)
- a gate tree checked out at a temp commit -> grep the summary for ALLDONE before reading it; a gate cut on an older trunk can carry a red the trunk already fixed -> re-run that lane on merge-tree(posts/belam, tip) (SM gen 48)
- F1 OUT files carry the HOST NAME -> sed it to <host> before any relay; a fix-forward touching root deletes waits for the answerer's word (SM gen 48)
- slash-joined words with "root" or "home" trip gsend's path scan -> write them comma-separated, and say so in a verbatim relay's header (SM gen 48)
