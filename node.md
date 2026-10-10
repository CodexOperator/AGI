---
id: goal:g7.16.1.11.13
mint_id: 0d5e0a34405d4ec0aab3c608edee9433
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.11.13
goal_kind: subgoal
origin: goal
scaffold_hash: c6b17011fb0f9e1d
season: 2
seeds:
  - goal:g7.16.1.11
status: active
tags:
  - council
  - design
  - g7.16.1.11
  - aa3
  - land
  - trunk
title: "G7.16.1.11.13: AA3 land -- a land is mail one parent edge up; root ff-lands a post's range on the trunk after edge + ring-signer + grow-gate + agi-gate checks; the trunk has ONE writer"
town: core
---
# goal:g7.16.1.11.13

## Why this exists
goal:g7.16.1.11: the council's AA3 section (doc:rse-aa3-land on posts/all-is-one, measured on a scratch repo borrowing MAIN's objects, now 17 lanes (AA3.14), 0 shared refs written) answers the owner's 'things could only go where they must go' for the merge path: today the master's hand-gated merge-up (skill agi-master-gate's landing) and the hub's pre-receive are the only gates. It found three byte defects that make today's gates read nothing (AA3.4) and, after belam's ruling 1efd017e6 (members <- council), a fail-closed rule for council authority (AA3.8: a name in the council row's `members` cell, absent = nobody; belam wrote the cell, faabf9b7a). The author's follow-up: the three byte fixes come BEFORE agi-land, or its checks read nothing. Two later additions (all-is-one 00:4xZ 10-02): AA3.11, the `lands` mask (AA2 defines a `lands` cell on a row, AA3 enforces it in ONE line of agi-land: the council row `lands: ["sanctuary-master"]` means a council member cannot land alive; +294 B), and AA3.10, versioning (belam [decision] 00:25Z, owner 00:3x-00:4xZ): the hourly snapshot is root's carrier pushing the trunk, the trunk's history IS the grid, grid_sync retires with refs/grid/* kept as the archive, and the crontab applier gets its own cadence.

## OWNER 2026-10-01 23:0xZ + 23:2xZ, verbatim (via the council bundle)
"We just need to allow each post to have a will box which they already do, an inbox and a holding box or an outbox or something."
"This is why protocol needs to be a mathematical matrix rotation or projection. So things could only go where they must go."
"Remember the graph can hold as much as you want just the engine itself needs to be tiny. It can lead on the graph via templates we have so much recursion and linking built in."
Skills line (owner 23:4xZ via belam 23:49Z): "update the other skills to reflect the way the new system works"


## Target end-state
- agi-land (<= 1,829 B, the AA3.14 text as committed in doc:rse-aa3-land AA3.2; root-side, in config:engine-root, 0 B in the zygote) ff-lands <post>'s <sha> on the trunk iff ALL hold at the RECEIVING tip $o: EDGE sender = parent(post) on the parent cells, and a parent with a `members` cell is an INERT group that passes the land to ITS parent (SM and thought-master-new under keep are landed by belam; a group member lands neither itself nor a peer; a post whose parent is owner lands itself) AND MASK the immediate parent's `lands` cell (absent = all children, [] = none: council lands [] since the level round 3a33c71b9), SIGNERS every commit in $o..$sha verifies on root's ring as the sender or a post under <post>, GROWTH grow-gate over $o..$sha, BODY agi-gate $sha, FF $o is an ancestor and the move is compare-and-swap (in MAIN the last step is `git merge --ff-only`).
- The request travels as AA1 mail to root: refs/box/<sender>/root, body `land <post> <sha>`; no master role, no human gate step.
- FOUR byte fixes land FIRST (AA3.4 + fix 4, all-is-one 00:5xZ): (1) [SUPERSEDED by A3: council ruling (alive 22:1xZ, relayed by SM 22:4xZ): SKIP item 1 only, A3's agi-signers ring writes <post>@agi and agi-land strips @agi itself; item 3 (the @agi strip in GROW-GATE's signer sed) BUILDS, grow-gate stays after A3] (2) grow-gate `rev-list $n --not ${AGI_NOT:---all}` (+12 B); (3) grow-gate signer sed strips `@agi` (+7 B); (4) grow-gate is blind to merges (`diff-tree -r` prints nothing for a merge, so a signed merge adding a node in neither parent lands unchecked; lane 4m): `diff-tree -r -c` + treat `AA` as an add (+14 B; grow-gate +33 B in all).
- The trunk reflog shows ONLY root as the trunk writer after the switch.
- VERSIONING (AA3.10): root's carrier pushes the trunk (+ refs/box/*) hourly (branch_push retires: no snapshot commit, every change already IS a commit); the trunk's history is the grid (`git log -- <node path>` replaces refs/grid/node/<mint>); grid_sync is disabled and refs/grid/* are NOT moved or deleted (they are the archive); the crontab applier gets its own cadence (`crons_apply: every_mins 5`, 0 engine bytes), then becomes a projection of cron:crons at the trunk tip with no polling.

## Invariants
- A land is ff-only and compare-and-swap: a not-ff is refused (the child merges the trunk and re-requests), never merged by root.
- Root runs no suite on the land path (small and synchronous); the parent's judgment (suites on tmpfs, reds attributed) happens BEFORE it mails `land`.
- A forged commit (a key outside the subtree) moves nothing; SM cannot land alive; DG1 cannot land itself.
- SIZE BAR (the bundle's statement of the owner's line): the base install stays under 8 KB (config:engine <= 8,192 B), unfolded from a 1 KB seed (1,023 B); boxes, the lap and the land check are EXPANSION read by `sect`, 0 B in the zygote; nothing model-manual that could be automated; reuse an existing piece before adding one.

## Falsifier
1. All 17 lanes of doc:rse-aa3-land AA3.3 + AA3.11 + AA3.14 (3c-3k) + 4m reproduce on a scratch clone against the real ring + real trunk cells (never MAIN): the harness is AA3.9 of doc:rse-aa3-land (17 lanes, committed as extensions/agi/tests/aa3-lanes.t.sh; self-contained, alternates, 0 shared refs written; extract + run: `sed -n '/^## AA3.9/,$p' .agi/nodes/doc/rse-aa3-land.md | sed -n '/^```sh/,/^```$/{//!p}' > /tmp/lanes.sh; sh /tmp/lanes.sh`) and prints 17 lines `ok`. TODAY (trunk 3a33c71b9, with `AGI_LAND=<AA3.14 block>`): 15 ok + `FAIL 4m` + `FAIL 4v`, exit 2; WITHOUT it exit 17 (agi-land is not an engine node yet: DG3's build); with the byte fixes (`GROW_GATE=<fixed grow-gate>`) 17/17 expected; 4m + 4v are the byte-fix witnesses, so the blocking order is a test that fails now and passes when they land.
3. Versioning (AA3.10 V1-V4, see the hypotheses): `git for-each-ref refs/grid | wc -l` is constant for 1 h while posts work; the origin trunk tip is never older than 65 min; a hand edit of the crontab is undone within 5 min; `git log --format=%h -1 -- <node>` on the trunk names the land that carried the node's last per-turn commit.
2. Negative: after the switch `git reflog <trunk>` shows no writer other than root, and `git grep -n 'refs/heads/trunk' -- <post-writable scripts>` returns zero hits.

## Out of scope
goal:g7.16.1.11.11 (the box root reads) · goal:g7.16.1.11.12 (the ring) · goal:g7.16.1.11.14 (skill deltas) · the agi-land build until the three byte fixes land.

## refs/grid writers, pushers and fetchers (DG1 v4 = v3 + SM's WL-1..3, PINNED at the trunk 2e92b6447a, code identical at 83cca19a79: `git diff 2e92b6447a 83cca19a79 -- extensions src .agi/nodes/.geometry` is empty; belam 16:4xZ: "stop hand-tabling: the exact command + its verbatim output at one sha; GATED reads only yes / no / exempt-by-name + path:line")
RULE the commands close: a ref can be named in the grid namespace only through the builders (REF_NS / FETCH_SPEC / PUSH_SPEC / push_spec_for / fetch_spec_for / ref_ns_for, all in grid.py) or the literal `refs/grid`. C6 shows the literal outside grid.py is in COMMENTS, docstrings and print text only (rotate.py:9654 reaches it through push_spec_for); C2 and C3 list the users of the SPEC builders (cli.py:4691 is a `ref_ns_for` READ and is not a spec user; level3.py:330-332 and stitch.py:194-196 are `_grid_spec` importlib spec objects, false positives of the C2 pattern). So a writer, pusher or fetcher of the grid namespace is either in grid.py or in C2 / C3 / C4. FETCHERS are closed by C7 at the pin (a plain `git fetch` runs the configured forced refspec; an explicit-ref fetch does not touch refs/grid; the spellings that would slip are the stated limit (1) below, and NONE slips at the pin) and CALLERS of the gated verbs by C8 (a new subprocess caller spelled `with_name("grid.py")` or a new rendered `{grid_py}` / `{script}` line shows up there; a caller that spells the path another way, e.g. `str(BIN / "grid.py")` as viewport.py:939 does for a read verb today, is NOT found by C8). Every other `update-ref` (C1) and every other push (C5) names a different ref.
The commands run from the repo root at the pinned sha. NOT scanned by any test today: `grid_writers()` (test_grid_gate.py:737-751; test_b8b :754, test_b9 :774) parses rotate.py ALONE; nothing scans grid.py, cli.py, heal.py, scripts or the engine pieces (a repo-wide scanner row is ordered from DG2: it pins the per-file counts of C1, C5 and the lines of C2-C4, so a new site fails until classified here). The ordered scanner rows WILL compare (path, text) with line numbers STRIPPED (no scanner row is in the tree yet): the line numbers in the blocks below are informational at the pinned sha. LIMITS, stated: (1) the quoted-list spellings: C5 and C7 also match the UNQUOTED `git push` / `push -q` / `git fetch ` forms, but their list-form alternatives are double-quoted only (`"push"`, `"fetch"`), so a single-quoted `'push'` / `'fetch'` list element slips; (2) C8 finds only `with_name("grid.py")` and the rendered `{grid_py}` / `{script}` forms followed by `commit` / `push-changed` / `sync` (see the RULE line): a rendered `{grid_py} migrate-refs|migrate-mint-refs|migrate-trunk` line slips, and none is rendered today; a widening to `['"]` and to `BIN / "grid.py"` is a future row, not part of this pin; (3) the cut-tail: the C1-C4, C6, C7 and C8 commands end in `| cut -c1-120` (C5 is a per-file count, unaffected), so the pinned text of a matching line is its first 120 columns only; a change past column 120 of an otherwise matching line is neither pinned nor seen.
C1 every ref writer
```
$ git grep -nE 'update-ref|commit-tree|mktree|hash-object -w' -- extensions src .agi/nodes/.geometry ':!extensions/agi/tests' ':!*.js' ':!*.json' ':!extensions/**/*.md' | cut -c1-120
.agi/nodes/.geometry/engine-post.md:25:w=${AGI_WT:-$RUNTIME_DIRECTORY/wt};x=$(git rev-parse -q --verify refs/heads/posts
.agi/nodes/.geometry/engine-post.md:61:[ $n = $(git rev-parse $t^{tree}) ]&&exit;c=$(echo "$P: $*"|git commit-tree -S -p
.agi/nodes/.geometry/engine-post.md:74: t=$(git rev-parse $b)&&git read-tree $t&&git --work-tree=$d add --ignore-removal
.agi/nodes/.geometry/engine-post.md:78: c=$(echo "$P: $(sed q $d.p)"|git commit-tree -S -p $t $q $n 2>&1)||{ echo "[comm
.agi/nodes/.geometry/engine-post.md:79: git update-ref $r $c "$o"||{ echo "[raced] $m">&2;k=4;continue;}
.agi/nodes/.geometry/engine-post.md:109:t=$(git rev-parse $b)&&T=$(git rev-parse ${AGI_TRUNK:-trunk})&&! git merge-base 
.agi/nodes/.geometry/engine-post.md:208:  c=$(printf '%s\n' "$b"|GIT_AUTHOR_EMAIL=$P@agi GIT_COMMITTER_EMAIL=$P@agi git 
.agi/nodes/.geometry/engine-post.md:213:  [ $1 = n ]&&echo "$f"&&continue;echo "[$f] $(git log -1 --format=%B $c)";git u
.agi/nodes/.geometry/engine-root.md:115: { echo $n;[ -z "$o" ]||echo ^$o;}|as $1 git -C $2 pack-objects --revs --stdout|
.agi/nodes/.geometry/engine-root.md:202:git update-ref $T $n $o
.agi/nodes/.geometry/engine-wrap.md:65:V=1;fl $M;V=;fl $M;(export GIT_DIR=$PWD/.git GIT_WORK_TREE=$D GIT_INDEX_FILE=$(mk
extensions/agi/bin/grid.py:16:  - Commits are made with plumbing (hash-object -> mktree -> commit-tree ->
extensions/agi/bin/grid.py:17:    update-ref), never a checkout, so the working tree is untouchable by
extensions/agi/bin/grid.py:92:# `payload_ref`, so a flat entry name is unambiguous and keeps `mktree` to the
extensions/agi/bin/grid.py:360:# `ref_tip`, `rev-list` and `commit-tree` take no pathspec and were correct
extensions/agi/bin/grid.py:849:    return git(root, "mktree", input_text=lines)
extensions/agi/bin/grid.py:899:#: refs whose update-ref failed for a reason other than a CAS miss (goal:g4.13.1 N1):
extensions/agi/bin/grid.py:943:                built = git_try(root, "mktree", input_text=lines.lstrip("\n"))
extensions/agi/bin/grid.py:958:    commit = git(root, "commit-tree", tree, *parent, "-m", message)
extensions/agi/bin/grid.py:960:    res = git_try(root, "update-ref", ref, commit, tip or "")
extensions/agi/bin/grid.py:969:            print(f"ERROR: update-ref {ref} failed (not a CAS miss): {why}", file=sys.std
extensions/agi/bin/grid.py:1633:      1. `git update-ref <new_ref> <old_tip>` -- point the NEW ref at the
extensions/agi/bin/grid.py:1642:      2. `git update-ref -d <old_ref> <old_tip>` -- a **compare-and-swap
extensions/agi/bin/grid.py:1656:        if git_try(root, "update-ref", new_ref, old_tip, "").returncode != 0:  # CAS (go
extensions/agi/bin/grid.py:1658:        git(root, "update-ref", "-d", old_ref, old_tip)
extensions/agi/bin/grid.py:1849:    UNCHANGED for the safety-critical mutation -- `update-ref <new> <old_tip>`
extensions/agi/bin/grid.py:1851:    then a compare-and-swap `update-ref -d <old> <old_tip>` -- so it inherits
extensions/agi/bin/heal.py:1546:            # unborn tree reached _sweep_archive, and `update-ref <ref> 0000..0` on an
extensions/agi/bin/heal.py:1701:            _, rc = _git(["update-ref", ref, head], main_checkout)
extensions/agi/bin/heal.py:1703:                return "update-ref failed"
extensions/agi/bin/heal.py:1728:            cm = run("commit-tree", tree.stdout.strip(), *(["-p", head] if head else [])
extensions/agi/bin/heal.py:1737:        _, rc = _git(["update-ref", ref + "-dirty", cm.stdout.strip()], main_checkout)
extensions/agi/bin/heal.py:1739:            return "dirty update-ref failed"
extensions/agi/bin/rotate.py:11072:            sha = _g("commit-tree", tree, "-p", head, "-m",
extensions/agi/bin/rotate.py:11076:                last = "commit-tree failed"; continue
```
C2 every user of the grid push-spec builders
```
$ git grep -nE 'PUSH_SPEC|push_spec_for|grid_spec' -- extensions src .agi/nodes/.geometry ':!extensions/agi/tests' ':!*.js' ':!*.json' ':!extensions/**/*.md' | cut -c1-120
extensions/agi/bin/crons.py:83:import grid  # noqa: E402 -- grid.push_spec_for: ONE spelling of the ref namespace
extensions/agi/bin/grid.py:107:PUSH_SPEC = f"{REF_NS}/*:{REF_NS}/*"
extensions/agi/bin/grid.py:171:def push_spec_for(root: Path) -> str:
extensions/agi/bin/grid.py:254:    line (`commit --all && git push -q origin PUSH_SPEC`, installed only by
extensions/agi/bin/grid.py:281:    """`REF_NS` fetch refspec for graph root `root` (see `push_spec_for`)."""
extensions/agi/bin/grid.py:289:    `REF_NS`, `FETCH_SPEC` and `PUSH_SPEC` are the values every other function
extensions/agi/bin/grid.py:295:    global REF_NS, FETCH_SPEC, PUSH_SPEC
extensions/agi/bin/grid.py:298:    PUSH_SPEC = push_spec_for(root)
extensions/agi/bin/grid.py:1907:    out = git(root, "push", "origin", PUSH_SPEC)
extensions/agi/bin/grid.py:1949:            f"git push -q origin '{PUSH_SPEC}' >> {log} 2>&1")
extensions/agi/bin/level3.py:330:_grid_spec = importlib.util.spec_from_file_location("grid_for_level3", _GRID_PATH)
extensions/agi/bin/level3.py:331:grid = importlib.util.module_from_spec(_grid_spec)
extensions/agi/bin/level3.py:332:_grid_spec.loader.exec_module(grid)
extensions/agi/bin/rotate.py:9651:        # graph root, so `push_spec_for(main)` would read no config and return
extensions/agi/bin/rotate.py:9654:        grid_spec = grid.push_spec_for(_shared_graph_root(root))
extensions/agi/bin/rotate.py:9661:        p2 = _git_proc(main, "push", "origin", grid_spec)
extensions/agi/bin/rotate.py:9666:                    f"push: push origin {grid_spec} refused: "
extensions/agi/bin/rotate.py:9669:                f"push origin {_CLOSEOUT_MERGE_TARGET} + {grid_spec} from MAIN")
extensions/agi/bin/stitch.py:194:_grid_spec = importlib.util.spec_from_file_location("grid_for_stitch", _GRID_PATH)
extensions/agi/bin/stitch.py:195:grid = importlib.util.module_from_spec(_grid_spec)
extensions/agi/bin/stitch.py:196:_grid_spec.loader.exec_module(grid)
```
C3 every user of the grid fetch-spec builders
```
$ git grep -nE 'FETCH_SPEC|fetch_spec_for|remote.origin.fetch' -- extensions src .agi/nodes/.geometry ':!extensions/agi/tests' ':!*.js' ':!*.json' ':!extensions/**/*.md' | cut -c1-120
extensions/agi/bin/crons.py:426:    `git config --add remote.origin.fetch '+refs/agi/*:refs/agi/*'`)."""
extensions/agi/bin/grid.py:106:FETCH_SPEC = f"+{REF_NS}/*:{REF_NS}/*"
extensions/agi/bin/grid.py:280:def fetch_spec_for(root: Path) -> str:
extensions/agi/bin/grid.py:289:    `REF_NS`, `FETCH_SPEC` and `PUSH_SPEC` are the values every other function
extensions/agi/bin/grid.py:295:    global REF_NS, FETCH_SPEC, PUSH_SPEC
extensions/agi/bin/grid.py:297:    FETCH_SPEC = fetch_spec_for(root)
extensions/agi/bin/grid.py:878:        specs = git(root, "config", "--get-all", "remote.origin.fetch",
extensions/agi/bin/grid.py:880:        if FETCH_SPEC not in specs:
extensions/agi/bin/grid.py:881:            git(root, "config", "--add", "remote.origin.fetch", FETCH_SPEC)
extensions/agi/bin/grid.py:882:            print(f"grid: added fetch refspec {FETCH_SPEC} to origin")
```
C4 wildcard-push probe (its three hits are comment / docstring / prose text -- the third is crons.md's THOUGHT line, whose words push ... commit --all match the pattern: no `--all` / `--mirror` / `refs/*` push exists)
```
$ git grep -nE 'push[^|]*(--all|--mirror|refs/\*)' -- extensions src .agi/nodes/.geometry ':!extensions/agi/tests' ':!*.js' ':!*.json' ':!extensions/**/*.md' | cut -c1-120
.agi/nodes/.geometry/crons.md:94:goal:g7.16.1.11.13.1 (DG1 order 17:22Z, rows test_crons_flip_successors.py c3a114bd3a b
extensions/agi/bin/rotate.py:18601:    single call so a future push site (ack/prepare/cron/keygen --all-live)
extensions/agi/bin/send.py:878:    """g15.26 claim (b) -- the push-like line the NO-WRITE --all-live path
```
C5 every push site, per file (count)
```
$ git grep -c -E '"push"|git push|push -q|[ (]push (-q )?origin' -- extensions src .agi/nodes/.geometry ':!extensions/agi/tests' ':!*.js' ':!*.json' ':!extensions/**/*.md'
.agi/nodes/.geometry/engine-post.md:1
.agi/nodes/.geometry/engine-root.md:2
extensions/agi/bin/adapters/claude_code_adapter.py:1
extensions/agi/bin/branches.py:1
extensions/agi/bin/cli.py:37
extensions/agi/bin/crons.py:3
extensions/agi/bin/grid.py:5
extensions/agi/bin/metrics.py:1
extensions/agi/bin/rotate.py:44
extensions/agi/bin/season.py:1
extensions/agi/bin/sensei.py:1
extensions/agi/guard/box-move.sh:2
extensions/agi/hooks/agent-git/pre-push:1
```
C6 the literal outside grid.py
```
$ git grep -nE 'refs/grid' -- extensions src .agi/nodes/.geometry ':!extensions/agi/tests' ':!*.js' ':!*.json' ':!extensions/**/*.md' ':!extensions/agi/bin/grid.py' | cut -c1-120
.agi/nodes/.geometry/crons.md:162:(every 5 minutes, snapshot + push refs/grid/*) and `branch_push` (hourly).
.agi/nodes/.geometry/formations/council-loop.md:26:| director-general-3 | MVPs + build nodes + tests; a build node may t
extensions/agi/bin/cli.py:4682:    """Byte source of truth for the refs/grid namespace: refname + object name
extensions/agi/bin/cli.py:5886:            # mur-52 residue 2b: the refs/grid IDENTICAL|CHANGED summary
extensions/agi/bin/cli.py:5893:            print("refs/grid: IDENTICAL before/after --apply "
extensions/agi/bin/cli.py:6370:        print(f"refs/grid: {same} before/after --apply (expected IDENTICAL)")
extensions/agi/bin/level3.py:327:# payloads out of `refs/grid/node/<mint-id>`, and grid.py is the one definition
extensions/agi/bin/level3.py:822:        # `refs/grid/node/*`. Measured 2026-08-25: editing README.md and
extensions/agi/bin/level3.py:1137:    # doc's history is invisible to `refs/grid/node/*` — see the comment in
extensions/agi/bin/rotate.py:9128:    "push",          # push origin season2/main and refs/grid
extensions/agi/bin/rotate.py:9434:    push that omits refs/grid) REFUSES BY NAME.
extensions/agi/bin/rotate.py:9624:        # push origin season2/main THEN origin refs/grid/*:refs/grid/*, both
extensions/agi/bin/rotate.py:9626:        # omits refs/grid is the falsifier. First non-zero rc refuses by
extensions/agi/bin/rotate.py:9628:        # the seat tree and never carried refs/grid.)
extensions/agi/bin/stitch.py:190:# `refs/grid/node/<mint-id>`, and grid.py is the one definition of how those
extensions/agi/bin/stitch.py:669:    tree" to "read it out of `refs/grid/node/<mint-id>`". Nothing falls back to
extensions/agi/bin/stitch.py:965:                          "own grid ref (refs/grid/node/<mint-id>) instead of "
extensions/agi/guard/sanctuary-watch:159:- Never pass --allow-branch to grid.py; never push refs/grid/* wholesale.
extensions/agi/src/graph_core/identity.py:138:# are case-sensitive (refs/grid/node/<id>), but case-insensitive filesyste
extensions/agi/src/graph_core/identity.py:379:# | Keys | `refs/grid/node/<mint-id>` | addressing, zoom, prefixes |
```
C7 every fetch consumer
```
$ git grep -nE '"fetch"|fetch -q|git fetch( |")|git -C [^ ]+ fetch' -- extensions src .agi/nodes/.geometry ':!extensions/agi/tests' ':!*.js' ':!*.json' ':!extensions/**/*.md' | cut -c1-120
.agi/nodes/.geometry/crons.md:32:    cmd: git -C {repo_root} fetch -q origin && python3 {engine_root}/extensions/agi/bin
.agi/nodes/.geometry/engine-post.md:214:carry)h=$2;shift 2;x=;for p;do git push -q $h "$m/$p/*:$m/$p/*";x="$x ^$m/$p/*";
.agi/nodes/.geometry/engine-root.md:96:F(){ git -C $n -c protocol.version=2 fetch -q --upload-pack="$u" file://$G "$@";}
.agi/nodes/.geometry/engine-root.md:119: git -C $C -c transfer.fsckObjects=1 fetch -q $H "$m/*:$m/*"
extensions/agi/bin/cli.py:4239:    _post_rename_print("fetch", "git fetch", apply)
extensions/agi/bin/cli.py:4240:    if apply and not step_done("fetch"):
extensions/agi/bin/cli.py:4241:        r = subprocess.run(["git", "fetch"], cwd=repo, capture_output=True, text=True)
extensions/agi/bin/cli.py:4243:            print(f"  note: git fetch rc={r.returncode} (no remote or offline); "
extensions/agi/bin/cli.py:4245:        mark("fetch")
extensions/agi/bin/crons.py:953:            f"git -C {repo_root} fetch -q origin && "
extensions/agi/bin/crons.py:964:            text = text.replace("fetch -q origin", "fetch -q origin '+refs/heads/*:refs/
extensions/agi/bin/dispatch.py:579:                ["git", "-C", str(root), "fetch", "origin", fetch_ref],
extensions/agi/bin/rotate.py:10999:            fetch = subprocess.run(["git", "-C", str(top), "fetch", "origin",
extensions/agi/bin/rotate.py:11009:            last = f"could not launch git fetch for {branch}: {exc}"
extensions/agi/bin/rotate.py:13206:#: rotation template uses it, so it falls through to `producer git fetch not
extensions/agi/bin/rotate.py:14387:    rotate-self values build never performs a real git fetch inside the
extensions/agi/bin/rotate.py:17007:        _fp = _git_proc(root, "fetch", "origin", _sb)
extensions/agi/bin/rotate.py:17016:    behind_clear = (f"git fetch origin {_sb} && git merge --no-edit "
extensions/agi/bin/rotate.py:17301:    return (f"git fetch origin {b} && git merge --no-edit origin/{b}")
extensions/agi/bin/send.py:550:        # a git fetch under tests). The explicit ``role`` argument stays
extensions/agi/bin/send.py:905:            ["git", "-C", str(top), "fetch", "origin", branch],
extensions/agi/bin/send.py:4935:            fetch = _run_git(root, ["fetch", "origin", name])
```
C8 every caller of the gated verbs (commit / push-changed / sync)
```
$ git grep -nE 'with_name\("grid.py"\)|\{grid_py\} (commit|push-changed|sync)|\{script\} (commit|push-changed|sync)' -- extensions src .agi/nodes/.geometry ':!extensions/agi/tests' ':!*.js' ':!*.json' ':!extensions/**/*.md' | cut -c1-120
extensions/agi/bin/crons.py:902:            f"python3 {grid_py} commit --all --prefix 'cron: ' >> {log} 2>&1; "
extensions/agi/bin/crons.py:903:            f"python3 {grid_py} push-changed >> {log} 2>&1; "
extensions/agi/bin/grid.py:1948:            f"python3 {script} commit --all --prefix 'cron: ' >> {log} 2>&1 && "
extensions/agi/bin/rotate.py:9617:        binp = Path(__file__).with_name("grid.py")
extensions/agi/bin/rotate.py:12564:                              str(Path(__file__).with_name("grid.py")),
```
TABLE (every CODE site of C1-C5, C7 and C8 is in a row; NOT in a row, by design: C1's comment / docstring hits (grid.py:16, :17, :92, :354, :893, :1627, :1636, :1833, :1835; heal.py:1546); gates are those live on this trunk TODAY)
G-E2 = `grid_retired()` (grid.py:240; guards grid.py:1150 and :269): EXISTS, reads False on live MAIN (crons.md grid_sync enabled: true), so GATED TODAY = no for everything it covers; it is the only gate that can stop W1/W2. grid.py:1171 (namespace refusal) and :1201 (branch refusal) fire only when ref_ns_for(root) == DEFAULT_REF_NS; .agi/config.json:239 sets grid.storage_trunk = refs/grid/local-maxxing, so both are open here.
| # | path:line | acts | carries refs/grid | gated today | covered once the flip lands |
|---|---|---|---|---|---|
| W1 | grid.py:952 commit-tree, :954 update-ref (commit_file :898; mktree :843, :937; sole caller cmd_commit :1117) | writes | yes | no | grid.py:1150 |
| W2 | grid.py:275 `git push -q origin *batch` (cmd_push_changed :267) | pushes | yes | no | grid.py:269 |
| W3 | grid.py:1907 `push origin PUSH_SPEC` (cmd_sync :1897) | pushes | yes | exempt-by-name grid.py:250-256 (row test_grid_gate.py:491) | exempt |
| W4 | rotate.py:9661 `push origin grid_spec` (_push :9623, grid_spec :9654) | pushes | yes | exempt-by-name grid.py:250-253 (row test_grid_gate.py:473) | exempt |
| W5 | rotate.py:9617-9619 (_grid_commit runs `grid.py commit --all`; C8) | via W1 | yes | no | grid.py:1150 |
| W6 | rotate.py:12564-12565 (_button_down runs `grid.py commit --all`; C8) | via W1 | yes | no | grid.py:1150 |
| W7 | crons.py:902-903 (rendered `commit --all` ; `push-changed`; C8) | via W1, W2 | yes | no | grid.py:1150, :269 |
| W8 | grid.py:1650 update-ref, :1652 update-ref -d (migrate helpers; cmd_migrate_refs :1656, cmd_migrate_mint_refs :1717, cmd_migrate_trunk :1822) | writes (renames existing tips) | yes | no | dry-run unless --write (grid.py:1656, :1717, :1822) |
| W9 | grid.py:881 `git config --add remote.origin.fetch FETCH_SPEC` (cmd_init :874) | config | no ref written | n/a | n/a |
| W10 | grid.py:1948-1949 snap line (commit half :1948 = C8, push half :1949) `git push -q origin PUSH_SPEC` (cron_lines :1927, cmd_cron :1967); its commit half is W1 | pushes | yes | exempt-by-name grid.py:253-254 (row test_grid_gate.py:522) | exempt |
| W11 | cli.py:4241 (`git fetch`), crons.py:953 (the built-in mail_poll line, 5 min) and the LIVE cell .agi/nodes/.geometry/crons.md:32 (mail_poll `fetch -q origin`, which crons.py prefers over :953): plain fetches under the configured FETCH_SPEC `+refs/grid/*:refs/grid/*` ('+' forced, grid.py:106) | fetches into local grid refs | yes | exempt-by-name (this row; brings in tips that already exist remotely); AFTER goal:g7.16.1.11.13.1 (F2) with grid_sync off the RENDERED mail_poll line is rewritten at render time by crons.py (`text.replace("fetch -q origin", "fetch -q origin '+refs/heads/*:refs/remotes/origin/*'", 1)`, a C7 TEXT site, not a new git call) so it fetches heads only and writes no refs/grid | exempt |
| T1 | C7 text only, no fetch run: cli.py:4239-4240, :4243, :4245 (the rename verb's step label and notes around W11's :4241), rotate.py:11009, :13206, :14387, :17016, :17301 (strings, comments and a printed `git fetch origin <b> && git merge` that a human runs), send.py:550 (a comment; all of these ARE lines of the C7 block); NOT matched by C7's pattern, found by a wider read of the word `fetch` and listed so no one hunts them again: grid.py:20, metrics.py:367, send.py:5798 (docstring / help text) | none | n/a | n/a | n/a |
| F1 | dispatch.py:579, rotate.py:10999, :17007, send.py:905, :4935 (`fetch origin <ref>`: an explicit ref); engine-root.md:96, :119 (fetch from file:// G / refs/box) | fetches a named ref | no | n/a | n/a |
| N1 | engine-post.md:61 (agi-at: commit-tree + `update-ref $b` = refs/heads/posts/$P by CAS), :74 (agi-turn's kept save: `commit-tree` + `update-ref $a $e "$o"` = refs/archive/$P/<dir> by CAS, a whole unclean tree), :78-:79 (agi-turn: commit-tree + `update-ref $r $c "$o"`, $r = posts/$P or refs/archive/$P/<mint> on a moved tip), :109 (agi-flush: the CAS merge of the trunk onto posts/$P, commit-tree + update-ref), :208, :213 (refs/held/$P/$f); :25 is the words `git update-ref -d it` inside agi-brief's printed [kept] line, no write | writes | no (refs/heads/posts/*, refs/archive/*, refs/held/*; never refs/grid) | n/a | n/a |
| N2 | engine-root.md:115 (refs/box via put), :202 (`update-ref $T`, the trunk branch after grow-gate) | writes | no | n/a | n/a |
| N3 | engine-wrap.md:65 (`update-ref $R`, R=refs/spawn/$M/$s, engine-wrap.md:54) | writes | no | n/a | n/a |
| N4 | heal.py:1701, :1728, :1737 (SWEEP_ARCHIVE_NS + name, refs/archive/worktrees/...) | writes | no | n/a | n/a |
| N5 | rotate.py:11065 commit-tree (an index tree; pushed at :11072 as a branch) | writes | no | n/a | n/a |
| P1 | cli.py (37 matching lines of C5: `git push origin <branch>` / `--delete <ref>` / `<old>:<new>`, branch rename and delete verbs) | pushes | no | n/a | n/a |
| P2 | rotate.py (44 matching lines of C5, minus W4: branch pushes, `HEAD:<mirror>` refs/agi/*, `:refs/heads/*` deletes, :9655 the merge target) | pushes | no | n/a | n/a |
| P3 | season.py:1158 `<sha>:refs/heads/<head>`; branches.py:425 `<sha>:<refs/agi/..>` | pushes | no | n/a | n/a |
| P4 | crons.py:430 `refs/heads/<town>/*:refs/agi/<town>/*` (_mirror_push_line :425-433) | pushes | no | stops WITH the flip: rendered only inside the grid_sync enabled block (crons.py:871, :908-917; mirror_towns true; refs/heads/local-maxxing/ = 6 refs live) | stops |
| P5 | crons.py:925, :933 (rendered `push -q origin {branch}` / `{engine_branch}`); grid.py:1950 (the legacy cron line `push -q origin {branch}`) | pushes | no | n/a | n/a |
| P6 | engine-root.md:118, :124 (`push -q $H $r:$r`, refs/box/*); engine-post.md:214 (the `box` piece's `carry)` arm, was :192 before AA1.V v5: `push -q $h $m/$p/*` AND its FETCH half `fetch -q $h "$m/*:$m/*"`, m=refs/box, so refs/box/* only, never refs/grid) | pushes, fetches | no | n/a | n/a |
| P7 | claude_code_adapter.py:110 (a disallowed-verb tuple), metrics.py:1138 (help text), sensei.py:2375 (a variable `push_at`; :2373 is the comment above it), hooks/agent-git/pre-push (a refusing hook) | no push | no | n/a | n/a |
| P8 | extensions/agi/guard/box-move.sh:31 (`git push -q origin HEAD:local-maxxing/season2/main`, the trunk branch) and :33 (`git push -q ssh://$TO/data/work/agi <sha>:refs/heads/carry/trunk refs/heads/posts/$P:refs/heads/posts/$P`, branches to the target box): host move tooling, branch refs only, never refs/grid | pushes | no | n/a | n/a |
FLIP NOTES (what stops or changes when cron:crons grid_sync.enabled turns false; belam's gate list): (1) `commit --all` and `push-changed` become no-ops (grid.py:1150, :269); (2) evidence_gate.enforce_on_disk (grid.py:1264) is skipped, no other caller runs it automatically (goal:g7.16.1.11.13.1 moves it to the `evidence_enforce` job); (3) the town MIRROR push P4 (crons.py:430) is no longer rendered: refs/agi/local-maxxing/* stops updating; (4) W3, W4, W10, W11 stay (exempt, named); W8 (the migrate verbs) is NOT exempt: its gated column is `no` and it is dry-run unless `--write` (grid.py:1656, :1717, :1822) -- its code gap is fix row F1 of goal:g7.16.1.11.13.1. The census is DROPPED (belam 18:2xZ (c)); the flip waits ONLY on goal:g7.16.1.11.13.1 (evidence_enforce + town_mirror).

## Agent Notes
Assigned to **director-general-1**.
