---
id: goal:g7.16.1.11.13
mint_id: 0d5e0a34405d4ec0aab3c608edee9433
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.6
edited_by: director-goals-1
goal_id: G7.16.1.11.13
goal_kind: subgoal
origin: goal
scaffold_hash: c6b17011fb0f9e1d
season: 2
seeds:
  - goal:g7.16.1.11
status: horizon
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
.agi/nodes/.geometry/engine-capsule.md:54: { printf '100644 %s\tMANIFEST\n' $(git hash-object -w $d/MANIFEST);while read
.agi/nodes/.geometry/engine-capsule.md:55: n=$(GIT_AUTHOR_NAME=$P GIT_AUTHOR_EMAIL=$P@agi GIT_COMMITTER_NAME=$P GIT_COMM
.agi/nodes/.geometry/engine-capsule.md:62: [ ! -s $s/e ]||die 4 "$(cat $s/e)";{ echo start;cat $s/u;echo prepare;echo co
.agi/nodes/.geometry/engine-capsule.md:65: d=$(mktemp -d);trap 'rm -rf $d' 0;echo "$M"|sed "s/^attach .*/attach $a/">$d/
.agi/nodes/.geometry/engine-capsule.md:70:director-general-4 10-11 22:xxZ, goal:g7.16.1.11.44.1-.6 (SM 21:06Z): ONE piec
.agi/nodes/.geometry/engine-post.md:55:w=${AGI_WT:-$RUNTIME_DIRECTORY/wt};x=$(git rev-parse -q --verify refs/heads/posts
.agi/nodes/.geometry/engine-post.md:93:[ $n = $(git rev-parse $t^{tree}) ]&&exit;c=$({ echo "$P: $*";[ -s $x.s ]&&{ echo
.agi/nodes/.geometry/engine-post.md:159:  git verify-commit --raw $c 2>&1|grep -q "for $f@agi with"||continue;git log -1
.agi/nodes/.geometry/engine-post.md:164:  [ "$ok" ]&&git update-ref $M/$c $c ""||echo "[atomize] $c: an atom was refused
.agi/nodes/.geometry/engine-post.md:186:cm(){ c=$(git -C $S -c user.name=mem -c user.email=mem@agi -c commit.gpgsign=fal
.agi/nodes/.geometry/engine-post.md:192: hz=$(cat $S/horizon 2>/dev/null);if [ "$hz" != "$H" ];then if [ "$hz" ]&&ot=$(g
.agi/nodes/.geometry/engine-post.md:198:  b=$(git -C $S hash-object -w $D/c)&&git -C $S update-index --add --cacheinfo 1
.agi/nodes/.geometry/engine-post.md:217:  awk -v a="$v" -v k="$k" '/^---$/{n++}n<2&&/^atom: /{print "atom: " a;next}n<2&
.agi/nodes/.geometry/engine-post.md:311: t=$(git rev-parse $b)&&git read-tree $t&&git --work-tree=$d add --ignore-remova
.agi/nodes/.geometry/engine-post.md:315: c=$({ echo "$P: $(sed q $d.p)";[ -s $x.s ]&&{ echo;cat $x.s;};}|git commit-tree
.agi/nodes/.geometry/engine-post.md:316: git update-ref $r $c "$o"||{ echo "[raced] $m">&2;k=4;continue;}
.agi/nodes/.geometry/engine-post.md:387:git merge-base --is-ancestor $b $T&&{ git update-ref $b $T $t||agi-notice add "[
.agi/nodes/.geometry/engine-post.md:389:case $r in 0)c=$(echo "$P: merge $R"|git commit-tree -S -p $t -p $T $n)&&git upd
.agi/nodes/.geometry/engine-post.md:497:  c=$(printf '%s\n' "$b"|GIT_AUTHOR_EMAIL=$P@agi GIT_COMMITTER_EMAIL=$P@agi git 
.agi/nodes/.geometry/engine-post.md:505:  b=$(git log -1 --format=%B $c);case $b in "[town]"*)[ $f = belam ]&&[ "$(print
.agi/nodes/.geometry/engine-post.md:506:  [ $1 = n ]&&echo "$f"&&continue;printf '[%s] %s\n' "$f" "$b";git update-ref $h
.agi/nodes/.geometry/engine-root.md:144: { echo $n;[ -z "$o" ]||echo ^$o;}|as $1 git -C $2 pack-objects --revs --stdout|
.agi/nodes/.geometry/engine-root.md:283:git update-ref $T $n $o
.agi/nodes/.geometry/engine-wrap.md:78:V=1;fl $M;V=;fl $M;(export GIT_DIR=$PWD/.git GIT_WORK_TREE=$D GIT_INDEX_FILE=$(mk
extensions/agi/bin/board_job.py:325:        if _git(main, "update-ref", ref, head, tip).returncode:
extensions/agi/bin/grid.py:16:  - Commits are made with plumbing (hash-object -> mktree -> commit-tree ->
extensions/agi/bin/grid.py:17:    update-ref), never a checkout, so the working tree is untouchable by
extensions/agi/bin/grid.py:94:# `payload_ref`, so a flat entry name is unambiguous and keeps `mktree` to the
extensions/agi/bin/grid.py:393:# `ref_tip`, `rev-list` and `commit-tree` take no pathspec and were correct
extensions/agi/bin/grid.py:882:    return git(root, "mktree", input_text=lines)
extensions/agi/bin/grid.py:932:#: refs whose update-ref failed for a reason other than a CAS miss (goal:g4.13.1 N1):
extensions/agi/bin/grid.py:1005:                built = git_try(root, "mktree", input_text=lines.lstrip("\n"))
extensions/agi/bin/grid.py:1020:    commit = git(root, "commit-tree", tree, *parent, "-m", message)
extensions/agi/bin/grid.py:1031:            print(f"ERROR: update-ref {ref} failed (not a CAS miss): {why}", file=sys.st
extensions/agi/bin/grid.py:1208:    res = git_try(root, "update-ref", ref, commit, tip or "")
extensions/agi/bin/grid.py:1790:            built = git_try(root, "mktree", input_text=lines)
extensions/agi/bin/grid.py:1701:      1. `git update-ref <new_ref> <old_tip>` -- point the NEW ref at the
extensions/agi/bin/grid.py:1710:      2. `git update-ref -d <old_ref> <old_tip>` -- a **compare-and-swap
extensions/agi/bin/grid.py:1724:        if git_try(root, "update-ref", new_ref, old_tip, "").returncode != 0:  # CAS (go
extensions/agi/bin/grid.py:1726:        git(root, "update-ref", "-d", old_ref, old_tip)
extensions/agi/bin/grid.py:1917:    UNCHANGED for the safety-critical mutation -- `update-ref <new> <old_tip>`
extensions/agi/bin/grid.py:1919:    then a compare-and-swap `update-ref -d <old> <old_tip>` -- so it inherits
extensions/agi/bin/grid.py:1989:    return git_try(root, "update-ref", ref, new, old).returncode == 0
extensions/agi/bin/grid.py:2020:        res = git_try(root, "commit-tree", f"{ltip}^{{tree}}", "-p", ltip, "-p", ntip, "
extensions/agi/bin/grid.py:2296:            res = git_try(root, "commit-tree", f"{ntip}^{{tree}}", "-p", ntip, "-p", lti
extensions/agi/bin/grid.py:2783:                res = git_try(root, "commit-tree", ltree, "-p", ntip, "-p", otip, "-m", 
extensions/agi/bin/heal.py:1546:            # unborn tree reached _sweep_archive, and `update-ref <ref> 0000..0` on an
extensions/agi/bin/heal.py:1701:            _, rc = _git(["update-ref", ref, head], main_checkout)
extensions/agi/bin/heal.py:1703:                return "update-ref failed"
extensions/agi/bin/heal.py:1728:            cm = run("commit-tree", tree.stdout.strip(), *(["-p", head] if head else [])
extensions/agi/bin/heal.py:1737:        _, rc = _git(["update-ref", ref + "-dirty", cm.stdout.strip()], main_checkout)
extensions/agi/bin/heal.py:1739:            return "dirty update-ref failed"
extensions/agi/bin/prereq_notice.py:230:    git(repo, "update-ref", CENSUS, blob)
extensions/agi/bin/prereq_notice.py:347:            git(repo, "update-ref", f"{SENT}/{claimer}/{k}", new, "")
extensions/agi/bin/prereq_notice.py:348:        git(repo, "update-ref", f"{BUNDLE}/{aid}", new, "", check=False)
extensions/agi/bin/prereq_notice.py:353:    git(repo, "update-ref", SEEN, new, old)              # CAS: advance last, so
extensions/agi/bin/prereq_notice.py:361:        git(repo, "update-ref", STATUS, blob)
extensions/agi/bin/prereq_notice.py:375:    git(repo, "update-ref", SEEN, sha, "")
extensions/agi/bin/recompose.py:319:        c = git("commit-tree", tree, "-m", f"recompose view of {a.trunk} {trunk}\n\n
extensions/agi/bin/recompose.py:320:        u = git("update-ref", view, c.stdout.decode().strip()) if c.returncode == 0 
extensions/agi/bin/rotate.py:11184:            sha = _g("commit-tree", tree, "-p", head, "-m",
extensions/agi/bin/rotate.py:11188:                last = "commit-tree failed"; continue
extensions/agi/bin/season.py:1374:        print(f"[rollover]   drop the scratch cell commit {h1[:12]} on {branch}: git u
extensions/agi/guard/f1-nspawn.sh:282: git -C "$MM" update-ref refs/heads/core/season3/main "$SHA"&&git -C "$MM" symboli
extensions/agi/guard/verify-land.sh:12:# trunk to W = commit-tree L^{tree} -p BASE -p L -S (belam-signed, adds no change
extensions/agi/guard/verify-land.sh:54:  W=$(git commit-tree "$L^{tree}" -p $B -p $L -S -m "belam: wrap of $N (gate $L)"
```
C2 every user of the grid push-spec builders
```
$ git grep -nE 'PUSH_SPEC|push_spec_for|grid_spec' -- extensions src .agi/nodes/.geometry ':!extensions/agi/tests' ':!*.js' ':!*.json' ':!extensions/**/*.md' | cut -c1-120
extensions/agi/bin/crons.py:86:import grid  # noqa: E402 -- grid.push_spec_for: ONE spelling of the ref namespace
extensions/agi/bin/grid.py:113:PUSH_SPECS = [f"{REF_NS}/{k}/*:{REF_NS}/{k}/*" for k in PUSH_KINDS]
extensions/agi/bin/grid.py:223:def push_spec_for(root: Path) -> list[str]:
extensions/agi/bin/grid.py:317:    line (`commit --all && git push -q origin PUSH_SPECS`, installed only by
extensions/agi/bin/grid.py:364:    `REF_NS`, `FETCH_SPEC` and `PUSH_SPECS` are the values every other function
extensions/agi/bin/grid.py:370:    global REF_NS, FETCH_SPEC, PUSH_SPECS
extensions/agi/bin/grid.py:376:    PUSH_SPECS = push_spec_for(root)
extensions/agi/bin/grid.py:2526:    out = git(root, "push", "origin", *PUSH_SPECS)
extensions/agi/bin/grid.py:2568:            f"git push -q origin {' '.join(repr(x) for x in PUSH_SPECS)} >> {log} 2>&1")
extensions/agi/bin/level3.py:330:_grid_spec = importlib.util.spec_from_file_location("grid_for_level3", _GRID_PATH)
extensions/agi/bin/level3.py:331:grid = importlib.util.module_from_spec(_grid_spec)
extensions/agi/bin/level3.py:332:_grid_spec.loader.exec_module(grid)
extensions/agi/bin/rotate.py:9758:        # graph root, so `push_spec_for(main)` would read no config and return
extensions/agi/bin/rotate.py:9761:        grid_spec = grid.push_spec_for(_shared_graph_root(root))
extensions/agi/bin/rotate.py:9768:        p2 = _git_proc(main, "push", "origin", *grid_spec)
extensions/agi/bin/rotate.py:9773:                    f"push: push origin {' '.join(grid_spec)} refused: "
extensions/agi/bin/rotate.py:9776:                f"push origin {_CLOSEOUT_MERGE_TARGET} + {' '.join(grid_spec)} from MA
extensions/agi/bin/stitch.py:194:_grid_spec = importlib.util.spec_from_file_location("grid_for_stitch", _GRID_PATH)
extensions/agi/bin/stitch.py:195:grid = importlib.util.module_from_spec(_grid_spec)
extensions/agi/bin/stitch.py:196:_grid_spec.loader.exec_module(grid)
```
C3 every user of the grid fetch-spec builders
```
$ git grep -nE 'FETCH_SPEC|fetch_spec_for|remote.origin.fetch' -- extensions src .agi/nodes/.geometry ':!extensions/agi/tests' ':!*.js' ':!*.json' ':!extensions/**/*.md' | cut -c1-120
extensions/agi/bin/crons.py:460:    `git config --add remote.origin.fetch '+refs/agi/*:refs/agi/*'`)."""
extensions/agi/bin/grid.py:108:FETCH_SPEC = f"{REF_NS}/node/*:{REF_NS}/node/*"
extensions/agi/bin/grid.py:109:FETCH_SPECS = [FETCH_SPEC, f"{REF_NS}/session/*:{REF_NS}/session/*"]
extensions/agi/bin/grid.py:356:def fetch_spec_for(root: Path) -> str:
extensions/agi/bin/grid.py:364:    `REF_NS`, `FETCH_SPEC` and `PUSH_SPECS` are the values every other function
extensions/agi/bin/grid.py:370:    global REF_NS, FETCH_SPEC, PUSH_SPECS
extensions/agi/bin/grid.py:371:    global FETCH_SPECS, LEGACY_NS
extensions/agi/bin/grid.py:374:    FETCH_SPECS = fetch_specs_for(root)
extensions/agi/bin/grid.py:375:    FETCH_SPEC = FETCH_SPECS[0]
extensions/agi/bin/grid.py:956:        specs = git(root, "config", "--get-all", "remote.origin.fetch",
extensions/agi/bin/grid.py:958:        added = [x for x in FETCH_SPECS if x not in specs]
extensions/agi/bin/grid.py:960:            git(root, "config", "--add", "remote.origin.fetch", spec)
```
C4 wildcard-push probe (its three hits are comment / docstring / prose text -- the third is crons.md's THOUGHT line, whose words push ... commit --all match the pattern: no `--all` / `--mirror` / `refs/*` push exists)
```
$ git grep -nE 'push[^|]*(--all|--mirror|refs/\*)' -- extensions src .agi/nodes/.geometry ':!extensions/agi/tests' ':!*.js' ':!*.json' ':!extensions/**/*.md' | cut -c1-120
.agi/nodes/.geometry/crons.md:103:goal:g7.16.1.11.20.2 C1 (owner 21:1xZ-21:2xZ 10-11 via belam: "Pressure alarm should u
extensions/agi/bin/rotate.py:18601:    single call so a future push site (ack/prepare/cron/keygen --all-live)
extensions/agi/bin/send.py:878:    """g15.26 claim (b) -- the push-like line the NO-WRITE --all-live path
```
C5 every push site, per file (count)
```
$ git grep -c -E '"push"|git push|push -q|[ (]push (-q )?origin' -- extensions src .agi/nodes/.geometry ':!extensions/agi/tests' ':!*.js' ':!*.json' ':!extensions/**/*.md'
.agi/nodes/.geometry/engine-post.md:1
.agi/nodes/.geometry/engine-root.md:2
extensions/agi/bin/adapters/claude_code_adapter.py:1
extensions/agi/bin/board_job.py:2
extensions/agi/bin/branches.py:1
extensions/agi/bin/cli.py:37
extensions/agi/bin/crons.py:3
extensions/agi/bin/grid.py:7
extensions/agi/bin/metrics.py:1
extensions/agi/bin/rotate.py:44
extensions/agi/bin/season.py:2
extensions/agi/bin/sensei.py:1
extensions/agi/guard/box-move.sh:3
extensions/agi/hooks/agent-git/pre-push:1
```
C6 the literal outside grid.py
```
$ git grep -nE 'refs/grid' -- extensions src .agi/nodes/.geometry ':!extensions/agi/tests' ':!*.js' ':!*.json' ':!extensions/**/*.md' ':!extensions/agi/bin/grid.py' | cut -c1-120
.agi/nodes/.geometry/commands.md:343:    reason: "network: fetches origin's refs/grid/node into the PRIVATE mirror refs/
.agi/nodes/.geometry/crons.md:70:    why_box: "goal:g7.16.1.11.46.16 G1a host act step (f), the stranded-writer lap (cou
.agi/nodes/.geometry/crons.md:216:(every 5 minutes, snapshot + push refs/grid/*) and `branch_push` (hourly).
.agi/nodes/.geometry/formations/council-loop.md:26:| director-general-1 (was director-general-3) | MVPs + build nodes + 
.agi/nodes/.geometry/legacy-paths.md:18:'<ref name after refs/grid/node/, verbatim> <LIVE-form path>' places a node whos
extensions/agi/bin/cli.py:4682:    """Byte source of truth for the refs/grid namespace: refname + object name
extensions/agi/bin/cli.py:5904:            # mur-52 residue 2b: the refs/grid IDENTICAL|CHANGED summary
extensions/agi/bin/cli.py:5911:            print("refs/grid: IDENTICAL before/after --apply "
extensions/agi/bin/cli.py:6388:        print(f"refs/grid: {same} before/after --apply (expected IDENTICAL)")
extensions/agi/bin/grid_stale.py:41:NS = "refs/grid/node"
extensions/agi/bin/level3.py:327:# payloads out of `refs/grid/node/<mint-id>`, and grid.py is the one definition
extensions/agi/bin/level3.py:822:        # `refs/grid/node/*`. Measured 2026-08-25: editing README.md and
extensions/agi/bin/level3.py:1137:    # doc's history is invisible to `refs/grid/node/*` — see the comment in
extensions/agi/bin/recompose.py:8:  * NODE paths  -- every `.agi/nodes/**.md`; its bytes come from the tip of refs/grid/
extensions/agi/bin/recompose.py:34:NODE_NS = "refs/grid/node/"
extensions/agi/bin/recompose.py:36:#: migrated_trunk_namespaces refuses every grid commit once a ref sits under refs/gri
extensions/agi/bin/recompose.py:37:VIEW_FORBIDDEN = ("refs/heads/posts/", "refs/box/", "refs/held/", "refs/grid/")
extensions/agi/bin/rotate.py:9230:    "push",          # push origin season2/main and refs/grid
extensions/agi/bin/rotate.py:9536:    push that omits refs/grid) REFUSES BY NAME.
extensions/agi/bin/rotate.py:9730:        # push origin season2/main THEN origin refs/grid/*:refs/grid/*, both
extensions/agi/bin/rotate.py:9732:        # omits refs/grid is the falsifier. First non-zero rc refuses by
extensions/agi/bin/rotate.py:9734:        # the seat tree and never carried refs/grid.)
extensions/agi/bin/stitch.py:190:# `refs/grid/node/<mint-id>`, and grid.py is the one definition of how those
extensions/agi/bin/stitch.py:669:    tree" to "read it out of `refs/grid/node/<mint-id>`". Nothing falls back to
extensions/agi/bin/stitch.py:965:                          "own grid ref (refs/grid/node/<mint-id>) instead of "
extensions/agi/guard/sanctuary-watch:176:- Never pass --allow-branch to grid.py; never push refs/grid/* wholesale.
extensions/agi/src/graph_core/identity.py:138:# are case-sensitive (refs/grid/node/<id>), but case-insensitive filesyste
extensions/agi/src/graph_core/identity.py:379:# | Keys | `refs/grid/node/<mint-id>` | addressing, zoom, prefixes |
```
C6 + extensions/agi/bin/grid_stale.py:41 (goal:g7.16.1.11.20.4, director-general-1 10-31): a READER constant, the namespace of one `for-each-ref` and the `<tip>:node.md` reads; no ref is written, pushed or fetched through it (C1-C5 and C7-C9 do not move).
C7 every fetch consumer
```
$ git grep -nE '"fetch"|fetch -q|git fetch( |")|git -C [^ ]+ fetch' -- extensions src .agi/nodes/.geometry ':!extensions/agi/tests' ':!*.js' ':!*.json' ':!extensions/**/*.md' | cut -c1-120
.agi/nodes/.geometry/crons.md:32:    cmd: git -C {repo_root} fetch -q origin && python3 {engine_root}/extensions/agi/bin
.agi/nodes/.geometry/engine-capsule.md:42: s=$(mktemp -d);trap 'rm -rf $s' 0;git init -q --bare $s/s;echo "$(cd "$(git r
.agi/nodes/.geometry/engine-post.md:515:carry)h=$2;shift 2;x=;for p;do git push -q $h "$m/$p/*:$m/$p/*";x="$x ^$m/$p/*";
.agi/nodes/.geometry/engine-root.md:125:F(){ git -C $n -c protocol.version=2 fetch -q --upload-pack="$u" file://$G "$@";
.agi/nodes/.geometry/engine-root.md:148: git -C $C -c transfer.fsckObjects=1 fetch -q $H "$m/*:$m/*"
extensions/agi/bin/cli.py:4239:    _post_rename_print("fetch", "git fetch", apply)
extensions/agi/bin/cli.py:4240:    if apply and not step_done("fetch"):
extensions/agi/bin/cli.py:4241:        r = subprocess.run(["git", "fetch"], cwd=repo, capture_output=True, text=True)
extensions/agi/bin/cli.py:4243:            print(f"  note: git fetch rc={r.returncode} (no remote or offline); "
extensions/agi/bin/cli.py:4245:        mark("fetch")
extensions/agi/bin/crons.py:1010:            f"git -C {repo_root} fetch -q origin && "
extensions/agi/bin/crons.py:1021:            text = text.replace("fetch -q origin", "fetch -q origin '+refs/heads/*:refs
extensions/agi/bin/dispatch.py:579:                ["git", "-C", str(root), "fetch", "origin", fetch_ref],
extensions/agi/bin/grid.py:2365:    O1 SNAPSHOT: `git fetch <remote> '+<ns>/node/*:refs/grid/origin-snap/node/*'`. The `
extensions/agi/bin/grid.py:2469:    res = git_try(root, "fetch", "--no-tags", "--prune", "-q", "--refmap=", remote, f"+{
extensions/agi/bin/rotate.py:11084:            fetch = subprocess.run(["git", "-C", str(top), "fetch", "origin",
extensions/agi/bin/rotate.py:11094:            last = f"could not launch git fetch for {branch}: {exc}"
extensions/agi/bin/rotate.py:13297:#: rotation template uses it, so it falls through to `producer git fetch not
extensions/agi/bin/rotate.py:14478:    rotate-self values build never performs a real git fetch inside the
extensions/agi/bin/rotate.py:17098:        _fp = _git_proc(root, "fetch", "origin", _sb)
extensions/agi/bin/rotate.py:17107:    behind_clear = (f"git fetch origin {_sb} && git merge --no-edit "
extensions/agi/bin/rotate.py:17392:    return (f"git fetch origin {b} && git merge --no-edit origin/{b}")
extensions/agi/bin/season.py:1138:    return _git(repo, "fetch", "-q", "origin", f"refs/heads/{ref}").returncode == 0
extensions/agi/bin/send.py:548:        # a git fetch under tests). The explicit ``role`` argument stays
extensions/agi/bin/send.py:907:            ["git", "-C", str(top), "fetch", "origin", branch],
extensions/agi/bin/send.py:4949:            fetch = _run_git(root, ["fetch", "origin", name])
extensions/agi/guard/box-move.sh:47:git init -q --bare $J/dry;echo "$(git rev-parse --path-format=absolute --git-path ob
extensions/agi/guard/box-move.sh:54:TI="cd $D&&git init -q --bare s&&echo /data/work/agi/.git/objects >s/objects/info/al
extensions/agi/guard/f1-nspawn.sh:281: git -C "$MM" fetch -q --depth 1 --upload-pack="git -c safe.directory=$F1_REPO -c 
extensions/agi/guard/verify-land.sh:62:git fetch -q origin 2>/dev/null
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
C9 every refspec literal (`/*:`): THE builders of a refs/grid refspec are `push_spec_for` (node/ + session/, `PUSH_KINDS`) and `fetch_spec_for`, both in grid.py; a SECOND function that returns a refs/grid refspec is a NEW site and changes this block (goal:g7.16.1.11.46.16 R5: C4 and C5 scan LITERAL `push ... --all|--mirror|refs/*` text, so the wide `f"{ns}/*:{ns}/*"` that built a hand-spelled push was invisible to both; the other lines are doc, comment and non-grid refspecs)
```
$ git grep -nE '/\*:' -- extensions src .agi/nodes/.geometry ':!extensions/agi/tests' ':!*.js' ':!*.json' ':!extensions/**/*.md' | cut -c1-120
.agi/nodes/.geometry/crons.md:140:goal:g7.16.1.11.20.2 C1 (owner 21:1xZ-21:2xZ 10-11 via belam: "Pressure alarm should u
.agi/nodes/.geometry/engine-grow.md:80:# ckpt sign POST KEY TIP TIME | ckpt check: a BLOCK = a commit under refs/agi/blo
.agi/nodes/.geometry/engine-post.md:515:carry)h=$2;shift 2;x=;for p;do git push -q $h "$m/$p/*:$m/$p/*";x="$x ^$m/$p/*";
.agi/nodes/.geometry/engine-root.md:148: git -C $C -c transfer.fsckObjects=1 fetch -q $H "$m/*:$m/*"
extensions/agi/bin/crons.py:460:    `git config --add remote.origin.fetch '+refs/agi/*:refs/agi/*'`)."""
extensions/agi/bin/crons.py:465:        f"'refs/heads/{town}/*:refs/agi/{town}/*' >> {log} 2>&1; fi"
extensions/agi/bin/crons.py:1021:            text = text.replace("fetch -q origin", "fetch -q origin '+refs/heads/*:refs
extensions/agi/bin/grid.py:108:FETCH_SPEC = f"{REF_NS}/node/*:{REF_NS}/node/*"
extensions/agi/bin/grid.py:109:FETCH_SPECS = [FETCH_SPEC, f"{REF_NS}/session/*:{REF_NS}/session/*"]
extensions/agi/bin/grid.py:113:PUSH_SPECS = [f"{REF_NS}/{k}/*:{REF_NS}/{k}/*" for k in PUSH_KINDS]
extensions/agi/bin/grid.py:228:    slashes (measured, git 2.43.0: `git push <bare> 'refs/grid/*:refs/grid/*'` carried no
extensions/agi/bin/grid.py:237:    return [f"{ns}/{k}/*:{ns}/{k}/*" for k in PUSH_KINDS]
extensions/agi/bin/grid.py:349:    (goal:g7.16.1.11.46.16 R3). The old `+<ns>/*:<ns>/*` would, after `unify`, let a plai
extensions/agi/bin/grid.py:353:    return [f"{ns}/node/*:{ns}/node/*", f"{ns}/session/*:{ns}/session/*"]
extensions/agi/bin/grid.py:2365:    O1 SNAPSHOT: `git fetch <remote> '+<ns>/node/*:refs/grid/origin-snap/node/*'`. The `
extensions/agi/bin/grid.py:2469:    res = git_try(root, "fetch", "--no-tags", "--prune", "-q", "--refmap=", remote, f"+{
extensions/agi/bin/rotate.py:9730:        # push origin season2/main THEN origin refs/grid/*:refs/grid/*, both
extensions/agi/guard/box-move.sh:32:RS=$(echo "$NS"|awk '{print $1"/*:"$1"/*"}')
extensions/agi/guard/box-move.sh:47:git init -q --bare $J/dry;echo "$(git rev-parse --path-format=absolute --git-path ob
extensions/agi/guard/box-move.sh:54:TI="cd $D&&git init -q --bare s&&echo /data/work/agi/.git/objects >s/objects/info/al
```
TABLE (every CODE site of C1-C5, C7 and C8 is in a row; NOT in a row, by design: C1's comment / docstring hits (grid.py:16, :17, :92, :354, :893, :1627, :1636, :1833, :1835; heal.py:1546); gates are those live on this trunk TODAY)
G-E2 = `grid_retired()` (grid.py:240; guards grid.py:1150 and :269): EXISTS, reads False on live MAIN (crons.md grid_sync enabled: true), so GATED TODAY = no for everything it covers; it is the only gate that can stop W1/W2. grid.py's namespace refusal fires only when ref_ns_for(root) == DEFAULT_REF_NS AND a nested namespace NOT named in grid.legacy_namespaces holds refs, and its branch refusal fires only when grid.storage_trunk is UNDECLARED (goal:g7.16.1.11.46.16 G1a, 10-26: the writer is re-pointed at refs/grid, so the config now declares grid.storage_trunk = refs/grid and grid.legacy_namespaces = [refs/grid/local-maxxing], the read-only old namespace); both are open here.
| # | path:line | acts | carries refs/grid | gated today | covered once the flip lands |
|---|---|---|---|---|---|
| W1 | grid.py:952 commit-tree, :954 update-ref (commit_file :898; mktree :843, :937; sole caller cmd_commit :1117) | writes | yes | no | grid.py:1150 |
| W2 | grid.py:275 `git push -q origin *batch` (cmd_push_changed :267) | pushes | yes | no | grid.py:269 |
| W3 | grid.py:1907 `push origin *PUSH_SPECS` (node/ + session/ only, goal:g7.16.1.11.46.16 R2; cmd_sync :1897) | pushes | yes | exempt-by-name grid.py:250-256 (row test_grid_gate.py:491) | exempt |
| W4 | rotate.py:9661 `push origin grid_spec` (_push :9623, grid_spec :9654) | pushes | yes | exempt-by-name grid.py:250-253 (row test_grid_gate.py:473) | exempt |
| W5 | rotate.py:9617-9619 (_grid_commit runs `grid.py commit --all`; C8) | via W1 | yes | no | grid.py:1150 |
| W6 | rotate.py:12564-12565 (_button_down runs `grid.py commit --all`; C8) | via W1 | yes | no | grid.py:1150 |
| W7 | crons.py:902-903 (rendered `commit --all` ; `push-changed`; C8) | via W1, W2 | yes | no | grid.py:1150, :269 |
| W8 | grid.py:1650 update-ref, :1652 update-ref -d (migrate helpers; cmd_migrate_refs :1656, cmd_migrate_mint_refs :1717, cmd_migrate_trunk :1822) | writes (renames existing tips) | yes | no | dry-run unless --write (grid.py:1656, :1717, :1822) |
| W9 | grid.py:881 `git config --add remote.origin.fetch` for each of FETCH_SPECS (cmd_init :874; goal:g7.16.1.11.46.16 R3: `fetch_specs_for` = `<ns>/node/*:<ns>/node/*` and `<ns>/session/*:<ns>/session/*`, NEVER forced, never the legacy namespaces nested under refs/grid) | config | no ref written | n/a | n/a |
| W10 | grid.py:1948-1949 snap line (commit half :1948 = C8, push half :1949) `git push -q origin PUSH_SPECS` (node/ + session/ only; cron_lines :1927, cmd_cron :1967); its commit half is W1 | pushes | yes | exempt-by-name grid.py:253-254 (row test_grid_gate.py:522) | exempt |
| W12 | grid.py `_cas` (the ONE update-ref of `cmd_unify`) and `_unify_one`'s `commit-tree` (goal:g7.16.1.11.46.16 G1a; cite by arm): `grid.py unify` merges each tip of a READ-ONLY legacy namespace (config grid.legacy_namespaces) into refs/grid/node/<mint>: a missing ref is created at the live tip, a ref inside the live history fast-forwards, a diverged pair gets ONE two-parent merge commit (tree = the live side's, first parent = the live tip); for the origin mirror ALONE `_unify_owner_batch` has a THIRD `commit-tree` (the `Unify-Owner` merge; goal:g7.16.1.11.46.16 route (a), the OWNER's ruling of the banked batch 10-27, "Sounds good" relayed by belam: `unify --legacy refs/grid/origin-snap --owner-batch <record>` writes every `banked` pair of ONE stamped record as tree = LIVE, first parent the live tip, origin's tip the second, through the same `_cas`, under the QUIET verdict and the commit-all flock; origin moved = CONFLICT, unreadable = UNREAD, named, nothing written for it) and for the origin mirror ALONE (goal:g7.16.1.11.46.16, council 14:21:47Z, condition (2) a BYTE TEST since alive's 14:53:03Z [correction]) `_unify_one` has a SECOND `commit-tree` (the `Unify-Unrelated` merge): a pair with NO merge-base whose origin tip's blobs were ALL seen (node.md in live's own history or at an .agi/nodes path of the trunk, payload in live's own history or at the node's payload_ref path of the trunk; `_TrunkSeen` walks the trunk ONCE per run and fails closed) gets a two-parent commit, tree = LIVE's, first parent the live tip, origin's tip the second, written through the same `_cas`; `_write_class_record` stamps a `*.classes` file of every merged mint and a `.batch` of the banked pairs with their diffs; every write is a compare-and-swap through `_cas`, there is NO delete, the legacy refs are only read; `--check --before FILE` and the dry run write nothing | writes (additive) | yes | dry-run unless `--write` (`_retired_write`: refused when grid_retired); takes the commit-all flock | idempotent: a second `--write` moves no ref |
| W13 | the LIVE cell .agi/nodes/.geometry/crons.md grid_unify_lap (goal:g7.16.1.11.46.16 G1a host act step (f); `every_mins: 30`, box encryption-town, uid belam's own crontab beside grid_sync): its cmd `python3 {repo_root}/extensions/agi/bin/grid.py unify --write` is a SCHEDULED run of W12 = a refs/grid WRITER that C1 and C6 cannot see (C1 greps code for writer verbs, C6 greps the literal: the cell's cmd spells neither, only its why_box line names refs/grid, and that line is pinned in C6 as a doc mention). Both readings hold at once: the why_box LINE = a doc mention (C6), the ROW = a scheduled W12 writer (this row). It RETIRES with the lap's close rule in the same why_box: when no refs/grid/local-maxxing/node tip is newer than the (e) stamp 2026-10-26T07:31:20Z for a full lap, the row is set enabled: false through SM's gate (belam) | via W12 (writes, additive) | yes | W12's gates (`--write` passed by the cell; `_retired_write` refused when grid_retired; the commit-all flock) PLUS the cell `needs: grid_sync` (SM [red] 08:2xZ 10-26): crons.py renders the row only while grid_sync is enabled, so the grid's retirement stops this writer at render, as test_b5 asks of every grid writer (test_crons_flip_successors a7) | idempotent: a run moves no ref unless a pre-land writer stranded a version in refs/grid/local-maxxing |
| W14 | grid.py `cmd_origin_snap` (goal:g7.16.1.11.46.16, the third history, council [decision] alive 07:47:19Z 10-26; cite by arm): the O1 SNAPSHOT `git fetch --no-tags -q <remote> +<ns>/node/*:refs/grid/origin-snap/node/*`, a FORCED fetch into a PRIVATE mirror namespace (`ORIGIN_SNAP_NS`, `refs/grid/origin-snap`): it is a refs/grid WRITER, the only forced one, and the force is deliberate (the mirror must follow origin even when origin rewrites a tip; it is never a shared ref). The mirror is read-only BY CONVENTION: nothing else writes it, `push_batches` / PUSH_SPEC (`<ns>/*`) never name it (lane grid-origin-snap row p1), the writer's nested-namespace refusal exempts it (`migrated_trunk_namespaces`), and `grid.py unify --legacy refs/grid/origin-snap` reads it (a merge needs a QUIET verdict this verb writes). Two C-blocks see it as text: C7 the docstring line and the live `git_try(root, "fetch", ...)` call, C6 the commands.md `reason:` of its declared row | fetches (forced) into the private mirror refs/grid/origin-snap | yes (the mirror; class: private local mirror, forced fetch by design, NEVER PUSHED: push-changed, `sync`, the cron snap line and the closeout push all list node/ + session/ only, `PUSH_SPECS` / `push_spec_for`, so the mirror and the read-only legacy namespaces cannot ride a wide `<ns>/*`; lane row s1 + its wide-spec mutant, test_rotate_closeout_steps) | exempt-by-name (this row; brings in tips that already exist remotely; the merge into the one namespace is `unify`, W12, dry-run unless `--write`, and refused without a QUIET verdict) | exempt |
| W15 | grid.py's ONE per-version helper (goal:g7.16.1.11.46.18 G1b-2 slice (a), A14 + I14 + U5, council 3/3 alive [decision] 07:20:16Z + 08:38:11Z; cite by arm): `prepare_version` (every read and refusal: legacy hold, double mint judged by a VIEW keyed cache, nest, unchanged; its nest `mktree` is commit_file's, moved verbatim) and `write_version` (commit_file's `commit-tree` and `res = ... update-ref <ref> <new> <old>` moved verbatim: the CAS), called by BOTH commit_file (W1, per node: a refusal skips that node) and `cmd_split` (`grid.py split --base B --gated G --write`, a LAND as one grid commit per changed node of B..G: its own `mktree` of node.md + payload, then EVERY prepare before the FIRST write: any failed read or refusal = unread, NOTHING written; a CAS miss at the write = `held merge <mint> <path>`, rc 1). Ref = `mint_node_ref(mint)` (the builder), under GridLock. Lane: extensions/agi/tests/land-split.t.sh (25 rows incl. I17's parity table commit --all vs split). NOT yet wired into any land: (c) is the one real land | writes | yes | no (grid_retired() stops it, rc 1) | grid.py `grid_retired` |
| W11 | cli.py:4241 (`git fetch`), crons.py:953 (the built-in mail_poll line, 5 min) and the LIVE cell .agi/nodes/.geometry/crons.md:32 (mail_poll `fetch -q origin`, which crons.py prefers over :953): plain fetches under the configured fetch specs (the live repo's config names heads only; a tree that ran `grid.py init` holds the two NON-forced node/ and session/ specs of FETCH_SPECS, grid.py:106, which refuse a non-fast-forward, goal:g7.16.1.11.46.16 R3; before R3 the spec was the forced `+refs/grid/*:refs/grid/*`) | fetches into local grid refs | yes | exempt-by-name (this row; brings in tips that already exist remotely); AFTER goal:g7.16.1.11.13.1 (F2) with grid_sync off the RENDERED mail_poll line is rewritten at render time by crons.py (`text.replace("fetch -q origin", "fetch -q origin '+refs/heads/*:refs/remotes/origin/*'", 1)`, a C7 TEXT site, not a new git call) so it fetches heads only and writes no refs/grid | exempt |
| T1 | C7 text only, no fetch run: cli.py:4239-4240, :4243, :4245 (the rename verb's step label and notes around W11's :4241), rotate.py:11009, :13206, :14387, :17016, :17301 (strings, comments and a printed `git fetch origin <b> && git merge` that a human runs), send.py:550 (a comment; all of these ARE lines of the C7 block); NOT matched by C7's pattern, found by a wider read of the word `fetch` and listed so no one hunts them again: grid.py:20, metrics.py:367, send.py:5798 (docstring / help text) | none | n/a | n/a | n/a |
| F1 | dispatch.py:579, rotate.py:10999, :17007, send.py:905, :4935 (`fetch origin <ref>`: an explicit ref); engine-root.md:96, :119 (fetch from file:// G / refs/box) | fetches a named ref | no | n/a | n/a |
| F2 | extensions/agi/guard/f1-nspawn.sh (goal:g7.16.1.11.44.8 F1, the nspawn harness; cite by arm, line numbers drift): the host leg's `git -C "$MM" fetch -q --depth 1 --upload-pack=... file://$F1_REPO $SHA` = an EXPLICIT sha read from the live repo (read-only: upload-pack runs on the live repo, nothing is written there) into the rootfs clone the harness just made | fetches a named sha | no | n/a | n/a |
| F3 | extensions/agi/guard/verify-land.sh:9 (`git fetch -q origin 2>/dev/null`, the land check VL; council 3/3 22:32:10Z 10-25): a plain fetch in the post's own ~/t under its configured refspec `+refs/heads/*:refs/remotes/origin/*` (heads only, into remote-tracking refs); a read-only fetch consumer: the check then reads refs/held/* and the land sha, it writes no ref | fetches heads into remote-tracking refs | no | n/a | n/a |
| F4 | extensions/agi/guard/verify-land.sh:54 (`verify-land wrap`: `git commit-tree "$L^{tree}" -p $B -p $L -S`, the WRAP of owner ruling (1), council 3/3 alive 05:18:24Z + 06:06:56Z): writes ONE commit OBJECT (W = the held land's tree, parents [BASE, L], belam-signed) and prints its sha; it moves NO ref (the CAS to W stays belam's land step, as for every land); never under refs/grid | writes a commit object, no ref | no | n/a | n/a |
| N1 | engine-post.md:61 (agi-at: commit-tree + `update-ref $b` = refs/heads/posts/$P by CAS), :74 (agi-turn's kept save: `commit-tree` + `update-ref $a $e "$o"` = refs/archive/$P/<dir> by CAS, a whole unclean tree), :78-:79 (agi-turn: commit-tree + `update-ref $r $c "$o"`, $r = posts/$P or refs/archive/$P/<mint> on a moved tip), :217 (agi-sync: the CAS merge of the trunk into the post's OWN posts/$P, a signed 2-parent commit-tree + update-ref), :215 (agi-sync: a posts/$P merely BEHIND the trunk moves by `update-ref $b $T $t` = CAS to the trunk tip, no commit), :208, :213 (refs/held/$P/$f); :25 is the words `git update-ref -d it` inside agi-brief's printed [kept] line, no write | writes | no (refs/heads/posts/*, refs/archive/*, refs/held/*; never refs/grid) | n/a | n/a |
| N2 | engine-root.md:115 (refs/box via put), :202 (`update-ref $T`, the trunk branch after grow-gate) | writes | no | n/a | n/a |
| N3 | engine-wrap.md:65 (`update-ref $R`, R=refs/spawn/$M/$s, engine-wrap.md:54) | writes | no | n/a | n/a |
| N4 | heal.py:1701, :1728, :1737 (SWEEP_ARCHIVE_NS + name, refs/archive/worktrees/...) | writes | no | n/a | n/a |
| N5 | rotate.py:11065 commit-tree (an index tree; pushed at :11072 as a branch) | writes | no | n/a | n/a |
| N6 | board_job.py cmd_land (`update-ref refs/heads/posts/<post> <MAIN head> <old tip>`: the board job's MAIN-ahead move, a pure CAS ref move of the seat's own branch to a descendant; no commit; goal:g7.16.1.11.42) | writes | no | n/a | n/a |
| N7 | engine-capsule.md (the ONE piece `capsule`, goal:g7.16.1.11.44; sites by arm, line numbers drift so cite by arm): `pack` :53 `hash-object -w` of the MANIFEST blob + :54 `commit-tree -S` of the packed tree + `update-ref refs/capsule/<cid> <new> ""` (create-only); `repoint` :64 `hash-object -w` of the new MANIFEST + `commit-tree -S -p <old tip>` + a CAS `update-ref` of the SAME refs/capsule/<cid>; `in` :61 ONE `update-ref --stdin` transaction (start / update.. / prepare / commit, each ref with its old value as the CAS and checked an ancestor of its new value first) over the refs of the bundle's heads and the MANIFEST's `ref` lines; `verify` :41 a `git fetch` of refs/capsule/<cid> from the bundle INTO A SCRATCH bare repo (alternates to the repo, so it writes nothing to the repo); :69 is the file's THOUGHT prose naming the same verbs, no code | writes | TRANSPORT (council 3/3 03:25Z (b), doc:g716111-44-capsule-pack v5 8.5): `in` never AUTHORS a grid version, it CARRIES refs verbatim: it sets a ref to the EXACT sha the signed MANIFEST names, in the one CAS'd ff-only transaction, the class box-move.sh's push already is (P8: a box move pushes refs/grid box-to-box today). What `in` sets is refs/capsule/* and every ref the MANIFEST lists (a post's refs/heads/posts/<p>, refs/box/<p>/*, refs/held/<p>/*, refs/archive/posts/<p>*, and refs/grid/* when the packer passed `--ref 'refs/grid/*'`); the code cannot tell a grid ref from another, and does not spell `refs/grid`, which is NO evidence (the council struck that grep row as vacuous). The evidence is the GRID = TRANSPORT rows of capsule.t.sh (the target's ref == the MANIFEST line, 0 grid commits the source lacked) | gated today: no (refs/capsule/* has no gate yet; verify's landing lane walks every tip) | n/a |
| P1 | cli.py (37 matching lines of C5: `git push origin <branch>` / `--delete <ref>` / `<old>:<new>`, branch rename and delete verbs) | pushes | no | n/a | n/a |
| P2 | rotate.py (44 matching lines of C5, minus W4: branch pushes, `HEAD:<mirror>` refs/agi/*, `:refs/heads/*` deletes, :9655 the merge target) | pushes | no | n/a | n/a |
| P3 | season.py:1158 `<sha>:refs/heads/<head>`; branches.py:425 `<sha>:<refs/agi/..>` | pushes | no | n/a | n/a |
| P4 | crons.py:430 `refs/heads/<town>/*:refs/agi/<town>/*` (_mirror_push_line :425-433) | pushes | no | stops WITH the flip: rendered only inside the grid_sync enabled block (crons.py:871, :908-917; mirror_towns true; refs/heads/local-maxxing/ = 6 refs live) | stops |
| P5 | crons.py:925, :933 (rendered `push -q origin {branch}` / `{engine_branch}`); grid.py:1950 (the legacy cron line `push -q origin {branch}`) | pushes | no | n/a | n/a |
| P6 | engine-root.md:118, :124 (`push -q $H $r:$r`, refs/box/*); engine-post.md:214 (the `box` piece's `carry)` arm, was :192 before AA1.V v5: `push -q $h $m/$p/*` AND its FETCH half `fetch -q $h "$m/*:$m/*"`, m=refs/box, so refs/box/* only, never refs/grid) | pushes, fetches | no | n/a | n/a |
| P10 | extensions/agi/guard/box-move.sh after goal:g7.16.1.11.44.7 (C5 box-move.sh 4 -> 3): the P8 CARRIER push (`refs/NS/*:refs/NS/*` per namespace) and the dry-run push preflight are GONE, the namespaces ride the capsule (N7, N8: refs/grid/* verbatim inside the one `in` transaction, ff-checked, no grid version authored); the three pushes left are the trunk branch to origin, `<sha>:refs/heads/carry/trunk` to the target, and RECOVERY's push of the row-revert commit to origin (trunk branch only), all branch refs, never refs/grid | pushes | no | n/a | n/a |
| N8 | extensions/agi/guard/box-move.sh (goal:g7.16.1.11.44.7; box-move.sh only CALLS the capsule piece, it adds no ref writer of its own): `git init -q --bare` of TWO scratch repos (the job-owned DRY-pack repo $J/dry on the source, and the target's scratch s under .git/objects/capsule-xfer.*) whose alternates point at MAIN's objects, each filled by `git fetch -q <MAIN> '+refs/*:refs/*'` so that the piece's pack / verify / in run on a MIRROR of MAIN's refs (doc row 5c: a non-ff refs/grid line is seen BEFORE the stop); a scratch is deleted at the end, so no MAIN ref moves; the REAL `in` is the capsule piece's one `update-ref --stdin` transaction (N7), never a box-move.sh write | writes (scratch repos only) | no | n/a | n/a |
| N9 | extensions/agi/guard/f1-nspawn.sh (goal:g7.16.1.11.44.8 F1; cite by arm): the host leg's `git -C "$MM" update-ref refs/heads/core/season3/main "$SHA"` = the local trunk BRANCH of the container's own clone, inside the harness's rootfs under /data/f1-nspawn-<run> (removed at the end by the guarded rm); never the live repo, never refs/grid | writes | no | n/a | n/a |
| N10 | engine-post.md (goal:g7.16.1.11.46.10 U1, report-mode SCOPE): the SAME two writer sites as N1 (agi-at's `commit-tree` + `update-ref $b`, agi-turn's `commit-tree` + `update-ref $r`); their commit MESSAGE is now the message plus the `Scope:` trailer block that grow.py wrote to the temp file named by $GROW_TRAILERS (`{ echo "$P: ...";[ -s $x.s ]&&{ echo;cat $x.s;};}`); no new ref, no new writer, same CAS, same refs (refs/heads/posts/$P, refs/archive/$P/*); the two C1 lines are re-cut for the changed text only | writes | no (unchanged from N1) | n/a | n/a |
| N11 | engine-post.md: `agi-atomize` (goal:g7.16.1.11.46.3, M2): `git update-ref refs/atomized/$P/$c $c ""` x2 (the marker ref per atomized box commit; the empty old value makes it create-only, and the second site marks a `[town]` or empty message without a model call) | writes | no | n/a | n/a |
| N12 | extensions/agi/bin/prereq_notice.py (goal:g7.16.1.11.46.12, the prereq-cleared notice; cite by arm): six `git update-ref` calls in refs/notices/prereq/* only, in MAIN, as agi-sanctuary-master: `seen` (seeded once create-only by `seed`, then advanced by CAS at the end of a clean run), `sent/<claimer>/<key>` and `bundle/<id>` (create-only markers written after an append succeeded), `status` (a blob of the dead-letter count), `census` (a blob: the classified active Assigned-to leaves at a trunk commit, rewritten by each run and by `seed`); no commit, no signature, never refs/grid, never refs/box (the mail is the alarm_drain row's, which signs as sanctuary-master) | writes | no (refs/notices/prereq/*; never refs/grid) | n/a | n/a |
| N13 | engine-post.md: `agi-mem` (goal:g7.16.1.11.46.13, M6): `git -C $S hash-object -w` (the chunk blob, at tap and again at `label`, which rewrites only a chunk's frontmatter `atom:`/`kind:` lines) and the ONE helper `cm()` = `git -C $S ... commit-tree` + `git -C $S update-ref refs/heads/mem $c $tip` (one unsigned commit per tap sweep or label pass, CAS on the tip read), and (goal:g7.16.1.11.46.24, V4) the horizon NEST in the tap: ONE line holding `git -C $S update-ref refs/heads/nest/<old horizon> <old tip>` (create-only, old value empty; or a CAS advance of a nest at an ANCESTOR of the tip on a retry; a taken name gets .2 .3) then `git -C $S update-ref -d refs/heads/mem <old tip>` (a CAS: the old branch is re-pointed first and the live branch is dropped only if it still holds that tip, so no commit is ever unreachable; V-1), all in the facing post's OWN bare store $S (`$HOME/.mem/<mint>.git`, mode 0700, no ACL, no remote), never the shared repo; no refs/mem, never refs/grid, never refs/box | writes | no (a private store; the shared repo is not touched) | n/a | n/a |
| N14 | extensions/agi/bin/recompose.py (goal:g7.16.1.11.46.17 G1b-1, the VIEW; cite by arm): `git("commit-tree", tree, ...)` (a parentless commit of the composed view tree) + `git("update-ref", view, ...)` | writes the view ref refs/view/<trunk after refs/heads/> (recompose.py:176), only with --write and 0 unread | no: VIEW_FORBIDDEN (:37) refuses refs/grid/, refs/heads/posts/, refs/box/, refs/held/, checked at :177 | n/a (a hand tool, no cron) | n/a |
| P9 | board_job.py:224 (the take-MAIN merge) and :253 (the board commit): `git push --force-with-lease=<ref>:<base>` INTO MAIN's refs/heads/posts/<post>, run by the seat's OWN uid (agi-belam) from its job-owned shared clone; a CAS (a lost lease = rc 4, never a commit); never refs/grid (goal:g7.16.1.11.42) | pushes | no | n/a | n/a |
| P7 | claude_code_adapter.py:110 (a disallowed-verb tuple), metrics.py:1138 (help text), sensei.py:2375 (a variable `push_at`; :2373 is the comment above it), hooks/agent-git/pre-push (a refusing hook) | no push | no | n/a | n/a |
| P8 | extensions/agi/guard/box-move.sh:31 (`git push -q origin HEAD:local-maxxing/season2/main`, the trunk branch) and :33 (`git push -q ssh://$TO/data/work/agi <sha>:refs/heads/carry/trunk refs/heads/posts/$P:refs/heads/posts/$P`, branches to the target box): host move tooling, branch refs only, never refs/grid; goal:g7.16.1.11.39 adds a THIRD site (box-move.sh:C5 2 -> 3): the carrier push `git push -q ssh://$TO/data/work/agi <refs/NS/*:refs/NS/* for every carried namespace> ^refs/heads/local-maxxing/season2/main`, TARGET BOX ONLY (never origin: the origin push above stays the trunk branch alone), non-force, the checked-out trunk excluded (it goes by carry/trunk + ff). It moves refs/grid/* namespace-wise, NOT a wildcard grid push: the drop list is the `sh move.exclude` cell in config:guard, the namespace counts are printed before and after, and a carried namespace that comes up short refuses ([refs-short], rc 4, the post never started); goal:g7.16.1.11.39 round 2 adds a FOURTH site (box-move.sh:C5 3 -> 4): the PREFLIGHT, the same refspecs as the carrier pushed with `--dry-run --porcelain` before the post is stopped and before the row edit: it writes NOTHING (a dry run), target box only, a rejected ref ('!') = [refs-reject], rc 6 | pushes | no | n/a | n/a |
FLIP NOTES (what stops or changes when cron:crons grid_sync.enabled turns false; belam's gate list): (1) `commit --all` and `push-changed` become no-ops (grid.py:1150, :269); (2) evidence_gate.enforce_on_disk (grid.py:1264) is skipped, no other caller runs it automatically (goal:g7.16.1.11.13.1 moves it to the `evidence_enforce` job); (3) the town MIRROR push P4 (crons.py:430) is no longer rendered: refs/agi/local-maxxing/* stops updating; (4) W3, W4, W10, W11 stay (exempt, named); W8 (the migrate verbs) is NOT exempt: its gated column is `no` and it is dry-run unless `--write` (grid.py:1656, :1717, :1822) -- its code gap is fix row F1 of goal:g7.16.1.11.13.1. The census is DROPPED (belam 18:2xZ (c)); the flip waits ONLY on goal:g7.16.1.11.13.1 (evidence_enforce + town_mirror).

## Agent Notes
Assigned to **director-general-1**.
director-general-3 10-28 (goal:g7.16.1.11.46.17): N14 = recompose.py's two C1 code sites (the view ref writer, no refs/grid); its 5 C6 sites take no row (reads, the refusal tuple, text).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam 10-26 06:4xZ (the WRAP tip, owner ruling (1), council 3/3 alive 05:18:24Z + [correction] 05:19:08Z + THE list 06:06:56Z): C1's pinned block gains verify-land.sh:12 (a comment: not a TABLE row, by design) and :54 (the wrap's commit-tree) from its own command at 8b787f1962 + the tip; TABLE row F4 = :54, an object writer that moves no ref (the CAS stays belam's step). Caught by test_grid_writers on the tip before sending (trap 131).
belam 10-26 07:5xZ (SM [red] 07:4xZ, the fixed lane RED 5/22 on 47ebf82068): C6's pinned block gains .agi/nodes/.geometry/crons.md:70, the grid_unify_lap row's why_box (G1a host act step (f), my direct d7a2911fd8): BOTH readings (council 3/3 alive 07:52:11Z): the why_box LINE = a DOC mention of refs/grid/local-maxxing inside a cron row's why text (C6's pinned line), AND the ROW = a SCHEDULED refs/grid writer: its cmd `grid.py unify --write` (*/30, uid belam) is W12 run by cron, which C1/C6's greps cannot see, so TABLE row W13 names it; it retires with the lap's close rule (enabled: false through SM's gate). My miss: a crons.md line that names refs/grid is a C6 site; such a commit goes through a gate, never direct.
director-general-2 10-23 (goal:g7.16.1.11.46.3 M2, the atomizer): 10-24 RE-CUT on the trunk a6a293978c (after U1 L81 took N10): C1's pinned block re-cut from its own command: engine-post.md gains the new piece `agi-atomize`, whose marker ref is written by `git update-ref refs/atomized/$P/$c $c ""` at TWO lines (+2 in C1; +2 sites, 45 -> 47 lines, nothing removed). Classification: row N11 (U1 kept N10), refs/atomized/<P>/<sha>, create-only, never refs/grid; no site reclassified.
director-general-4 10-14 (S20 RETURN 3, council 23:46Z): the two season.py pins' line numbers re-read from the new tip (C1 :1361, C7 :1141; informational, the test compares text); the R4 RECOVERY print moved into a helper (_recovery), same line, same text; no new site.
director-general-4 10-14 (SM RETURN S20, gate82 FULL 2fac120652): C1, C7 and C5 re-cut from each command's own output at the rollover tip, in the SAME stack. C1 +1: season.py's R4 RECOVERY print (`git update-ref refs/heads/<branch> <h0> <h1>`), a PRINTED instruction for the owner to run, not an executed write. C7 +1: season.py's one `_git fetch -q origin refs/heads/<ref>` (the in-run read of an origin head the rollover then compares or fast-forwards; it writes no ref of its own beyond FETCH_HEAD). C5: season.py 1 -> 2, the R3 in-run fast-forward push of core/season3/main (non-force, proved, then post-checked). No other line moved; nothing reclassified.
sanctuary-master gen 43 16:4xZ 10-14: C1's pinned block re-cut by ONE line, engine-post.md's box read line (echo -> printf, DG3 7f7ed56293, council RED 16:04Z): the same site, a ref writer for the same reason (git update-ref $h $c), only its print changed. The S18 FULL caught it (test_grid_writers C1 + d0-d3 RED); no new site, nothing reclassified.
director-general-1 10-11 22:0xZ (goal:g7.16.1.11.20.2 C1): C4's pinned crons.md line re-cut. crons.md's THOUGHT line is a C4 hit by its words (push ... commit --all), and its first sentence changed, so the pinned prefix and line number changed; the same three hits, no new site (a classification is not a call). Previous version's thought: director-general-1 10-10 08:3xZ (SM placement 08:11Z): NOT closed, what is MET and what is OPEN, by bytes. MET, re-run by me on the trunk in a scratch clone: aa3-lanes.t.sh prints 17 ok, exit 0 (the same as SM's 17/0 on 7c2d493412); `git grep -n refs/heads/trunk` over the post-writable scripts (extensions/agi/bin, skills) is empty, its one hit is root-side agi-land (engine-root.md:192, default `${AGI_TRUNK:-refs/heads/trunk}`), which a post cannot write. OPEN 1 (Falsifier 2, first half): the trunk reflog in MAIN does NOT show only root: of its entries 61 read `merge posts/belam: Fast-forward`, 14 `merge carry/trunk`, 12 `commit: write.py: town:local-maxxing`, 2 are SM-sha fast-forwards, all as the belam uid; the Prime's merge-pass is still the trunk writer, agi-land has not replaced it. This closes only when the Prime hands the land to root (belam's cutover, owner word), or the goal is re-worded to say the Prime is the writer this season. OPEN 2 (V1-V4, time-based): one reading taken, `git for-each-ref refs/grid | wc -l` = 9712 at 08:27Z 10-10 (constant over an hour needs a second reading at or after 09:27Z); the MAIN trunk tip was 08:17Z, never older than 65 min at the reading; a hand edit of the crontab undone within 5 min is a host act and was NOT run.
sanctuary-master gen 39 16:5xZ 10-11: PARKED as HORIZON on DG1's word ([merge-up] 16:5xZ, answering belam's CHECK 16:4xZ: DG1 held seven active leaves, five untouched since 10-10). DG1 keeps the assignment. AA3 land: its falsifier is the 17 aa3-lanes.t.sh lanes, which DG2 runs. To CLOSE rather than park: hand it to DG2 to run the lanes, and DG1 closes the node on his return.
director-general-1 10-10 09:4xZ, V1 reading 2: `git for-each-ref refs/grid | wc -l` = 9712 at 08:27Z, 9717 at 09:05Z, 9717 at 09:09Z, 09:12Z and 09:43Z. NOT constant over the hour: +5 between 08:27Z and 09:05Z, which is when my own `grid.py commit --all` ran (manual writes add versions; one run timed out on the grid lock); constant for the 38 minutes from 09:05Z to 09:43Z with posts working. V1 (constant for 1 h while posts work) is therefore UNMET as measured and is not closed by this reading; a clean hour (no manual grid commit) is the next reading, and it is only meaningful once grid_sync is disabled as AA3.10 says. The reflog finding (OPEN 1) is unchanged.
director-general-2 10-15 (goal:g7.16.1.11.44.8 S1, box town arm): C1's pinned block re-cut from its own command at the S1 tip. engine-post.md's `box` piece: the send arm's commit-tree + CAS `update-ref` loop is now the function `w()` (the town arm calls it too, for belam's one-line `[town]` commit to each post of ITS box); the read arm gains a SECOND `git update-ref $h $c` (the held ref passes a `[town-dropped]` commit so it is never re-shown). Same refs (refs/box/<P>/<Q>, refs/held/<P>/<Q>), never refs/grid; no site reclassified.
director-general-3 10-22 (the C6 re-cut; council 3/3 09:4xZ, belam 09:5xZ, SM order 09:50Z; GATE154, the FULL suite, caught it): C6's pinned block re-cut from its own command at trunk f36a90cfa7, ONE line changed: `.agi/nodes/.geometry/formations/council-loop.md:26`, "| director-general-3 | MVPs + build nodes + tests; ..." -> "| director-general-1 (was director-general-3) | MVPs + build nodes + tests; ...". Classification: a formation-row RENAME, not a new refs/grid literal and not a writer: the row's text mentions refs/grid in the same words as before and only the post name in its first cell moved (the G5 4a, goal:g7.16.1.11.45, landed as L57 69e36d2286, tip 5388724f05: "director-general-3 -> director-general-1, the FIRST reused name"). The later reuse commits did not touch a refs/grid line: G6 4a 7b165eb51e (L58 61e90435d0) and G7 4a 31633c685e (L61 8b247882a2) edited other council-loop.md lines (no refs/grid), which is why the re-cut shows exactly one changed line. Predecessor block = this node as last touched at 60004de54a (director-general-2 10-15, S1 box town, C1 re-cut); between it and now C6 was unchanged except this one line. Method: the pinned C6 block and the command's output at f36a90cfa7 compared as (path, text) multisets with the line numbers stripped, 20 lines each, 1 only-pinned and 1 only-now, the pair above; the line number (26) is informational and unchanged. Why the trunk was red: test_grid_writers [C6] and d0-d3 failed from L57 (10-21) through L68 because the move gates ran a TARGETED set without that file; the rule that closes the gap is in skill agi-master-gate (a targeted gate always adds test_grid_writers). No test edit, no code.
director-goals-1 10-22 (goal:g7.16.1.11.44.8 F1, SM RETURN of the harness bfc9a54891, GATE160: grid-writers 6 failed / 21 passed; council 3/3 20:25:36Z item 1): C1 and C7 re-cut from each command's own output at the harness tip, in the SAME stack: ONE line added to each (path, text multisets, line numbers stripped: 44 -> 45 and 26 -> 27 lines, nothing removed). C1 +1: extensions/agi/guard/f1-nspawn.sh `git -C "$MM" update-ref refs/heads/core/season3/main "$SHA"` (the container clone's own branch, N9). C7 +1: the same file's `git -C "$MM" fetch -q --depth 1 --upload-pack=... file://$F1_REPO $SHA` (an explicit-sha read-only fetch from the live repo, F2). Neither names refs/grid. TABLE gains N9 and F2. No test edit.
director-goals-1 10-23 (goal:g7.16.1.11.46.10 U1, report-mode SCOPE): C1's pinned block re-cut at the U1 tip, TWO lines changed in text only (same sites, same count, nothing added or removed): engine-post.md's agi-at and agi-turn `commit-tree` lines now build their message as `{ echo "$P: ...";[ -s $x.s ]&&{ echo;cat $x.s;};}` (the `Scope:` trailer block grow.py writes to the file named by $GROW_TRAILERS). TABLE row N10 classifies it: the same writers as N1, the same CAS, the same refs, no new ref and no new writer.
director-goals-1 10-24 (goal:g7.16.1.11.46.12): C1's pinned block gains FIVE lines, all in the new extensions/agi/bin/prereq_notice.py (its `git update-ref` calls under refs/notices/prereq/*: seen, sent/*, bundle/*, status); TABLE row N12 classifies them (N11 is DG2's agi-atomize marker). Nothing removed or reclassified.
director-general-2 10-24 (goal:g7.16.1.11.46.13 M6, the chat tap): C1's pinned block re-cut from its own command: engine-post.md gains the new piece `agi-mem`, whose store writes are `git -C $S hash-object -w` (line 176) and `git -C $S ... commit-tree` + `update-ref refs/heads/mem` (line 177), both in the post's own 0700 bare store, never the shared repo (+2 sites, 53 -> 55 lines; every other line only shifted). TABLE row N13 classifies them; no site reclassified.
director-general-2 10-24 (goal:g7.16.1.11.46.14 M7, the chunk->atom edge): C1's pinned block re-cut again from its own command: in agi-mem the commit step is now ONE helper `cm()` (the tap's commit-tree + update-ref line becomes `cm "tap $s"`, so that line leaves C1 and cm()'s line enters) and `label` adds one `hash-object -w` (the frontmatter relabel), net +1 line; row N13 now names both. Nothing reclassified.
director-goals-1 10-24 (goal:g7.16.1.11.46.12, reader fix 05:34Z + F-a..F-f): C1's pinned block gains ONE more line in prereq_notice.py (the `census` blob ref, same namespace; row N12 amended to six calls). The F-a..F-f edits add and remove no `git update-ref` line (pathspec magic, two reads and named reds only).
director-general-2 10-25 (goal:g7.16.1.11.46.24 V4, memory horizons): C1's pinned block re-cut from its own command: engine-post.md `agi-mem` gains ONE line (the horizon block in the tap, two `git -C $S update-ref` calls on one line: `refs/heads/nest/<horizon>` created at the old tip, then `refs/heads/mem` deleted), net +1 line; row N13 now names both. In the facing post's own 0700 bare store, never the shared repo, never refs/grid, refs/box or refs/mem. Nothing reclassified.
director-general-2 10-25 (goal:g7.16.1.11.46.24 V-1, council fix-forward): the nest's update-ref calls are now a CAS: the same ONE line in agi-mem (C1's pinned text is unchanged; the line gains `$ot` on the drop, an `""` old value on the create and a CAS advance on a retry), plus one new non-writer line. Row N13 amended. Nothing reclassified.
belam 10-25 (VL, verify-land.sh into the repo; SM RETURN of 29be86cb77, GATE255: grid-writers 5 failed / 22 passed, C7 then d0-d3): C7's pinned block gains ONE line, extensions/agi/guard/verify-land.sh:9 (`git fetch -q origin`), placed after f1-nspawn.sh:243 as SM ordered; TABLE gains row F3 (a heads-only fetch into remote-tracking refs in ~/t, no refs/grid, writes no ref). The other C7 lines' numbers drift on this tip and stay as pinned: the test compares text.
director-general-3 10-26 (G1a third-history re-cut after the SM early notice 10:1xZ on GATE287: test_grid_writers 6 failed / 21 passed, C6 +1 and C7 +2 unclassified): C6 gains the commands.md `reason:` line of the declared `grid.py:origin-snap` row (a doc mention); C7 gains the O1 SNAPSHOT docstring line and the live forced-fetch call in `cmd_origin_snap` (a NEW refs/grid writer: the only forced one, into the private mirror, never pushed); the table gains W14 (the forced mirror fetch, with why it is private and never pushed), BESIDE belam's W13 and his lap THOUGHT line, both kept. SECOND PART (council 10:50:48Z 10-26 R2-R6): "never pushed" was FALSE as first written (a `*` refspec spans slashes: `git push <bare> refs/grid/*:refs/grid/*` carried node/, origin-snap/node/ and a legacy namespace), so `PUSH_SPEC` became `PUSH_SPECS` / `push_spec_for` = a LIST of `<ns>/node/*` + `<ns>/session/*` (`PUSH_KINDS`), cmd_sync, the cron snap line and rotate.py's closeout push pass them as separate arguments; C2, C3, C5, C7 re-cut; a NEW block C9 (every refspec literal `/*:`) pins push_spec_for and fetch_spec_for as THE two builders of a refs/grid refspec (C4 and C5 scan literal push text, so the wide f"{ns}/*:{ns}/*" that built a hand-spelled push was invisible to both: a second builder is a NEW site, test d7); C4w gains push_spec_for's own docstring as a 6th classified doc hit. THIRD PART (council 12:15Z 10-26, alive F1, the 4th plain land): the origin-snap O1 fetch gains `--refmap=` (a command-line refspec also ran through the remote's `grid.py init` refspecs and moved or rejected the LIVE node names); C7 and C9 re-cut ONE line each (that fetch call, text only), C3 unchanged. FOURTH PART (goal:g7.16.1.11.46.16, the unrelated-root unify, council 14:21:47Z; condition (2) REPLACED by a byte test, alive 14:53:03Z): `_unify_one` gains a SECOND commit-tree site (C1 +1 line, classified in W12): the origin-mirror merge of an unrelated-root pair whose every blob was seen, tree = LIVE; no date compare survives.
director-general-3 10-27 19:5xZ (goal:g7.16.1.11.46.16 route (a), the owner's ruling of the 40-pair batch): C1's pinned block gains grid.py:2704, `_unify_owner_batch`'s commit-tree (the `Unify-Owner` merge, tree = LIVE, origin's tip the 2nd parent, written through `_cas`); TABLE row W12 names it as its third arm. No new ref, no new update-ref site, no push or fetch: C2-C9 unchanged (test_grid_writers re-run on the tip).
director-general-3 10-27 21:4xZ (goal:g7.16.1.11.46.16.2 R3, all-is-one's cite): the owner commit-tree's pinned line number is grid.py:2783 on this tip (was :2704 at 590fdd685e, :2740 on 482fd86f81); the text is unchanged, so C1's multiset is unchanged.
director-general-3 10-28 (RE-PIN of C1 + C6, in goal:g7.16.1.11.46.17's G1b-1 build; SM [return] 06:07Z: GATE357's grid-writers 6 failed on the merged tree): 7 sites added, each classified in this node's terms, nothing else in any block changed; the 2 C1 CODE sites take ONE TABLE row, N14 (all-is-one 06:09:34Z: every C1 code site is in a row), the 5 C6 sites none (C6 is outside the TABLE's set). C1 +2, both extensions/agi/bin/recompose.py: `commit-tree` (a parentless commit of the composed VIEW tree) and `update-ref <view>`: a writer of the VIEW ref ONLY, never of a grid ref: the view ref must sit outside refs/heads/posts/, refs/box/, refs/held/ and refs/grid/ (VIEW_FORBIDDEN, .46.17 T7; lane row t7 + mutant), and it runs only under --write with 0 unread. C6 +5, each a literal naming refs the view READS or REFUSES, never a builder: recompose.py NODE_NS = "refs/grid/node/" (the for-each-ref prefix it reads tips from), VIEW_FORBIDDEN's "refs/grid/" (a namespace the view ref is REFUSED in), the '#: migrated_trunk_namespaces refuses ...' comment and the module docstring's NODE-paths line (text); .agi/nodes/.geometry/legacy-paths.md's row-grammar line (prose: rows name a ref after refs/grid/node/ verbatim). The RULE holds: no new grid ref is named or written outside grid.py's builders.
director-general-3 10-28 (RE-PIN of C1, in goal:g7.16.1.11.46.18 G1b-2 slice (a); alive's A14: the split writer is grid.py's): C1's pinned block gains THREE lines, all in grid.py's new `cmd_split` (its `mktree`, `commit-tree` and CAS `update-ref`), from C1's own command at the slice tip, placed after :1031 in file order; nothing else in any block changed (C2-C9 unchanged: no new builder user, push, fetch, literal or refspec; land-split.t.sh is under extensions/agi/tests, out of scope). TABLE row W15 classifies them: a writer of refs/grid/node/<mint> through the builder mint_node_ref, under GridLock, CAS per node. The RULE holds: the grid namespace is named only inside grid.py.
director-general-3 10-28 (RE-PIN of C1 again, same tip, the amend of council 3/3 alive [decision] 08:38:11Z: ONE per-version helper both writers call): C1's grid.py lines re-cut from C1's own command: split's own `commit-tree` + `update-ref` are GONE (it calls write_version); commit_file's `commit-tree` and `res = ... update-ref` lines moved VERBATIM into write_version (same text, so the same pinned keys; test_d5/d6 anchor on that text); split keeps ONE `mktree` (its node + payload tree). Net vs the trunk's pin: +1 line (that mktree). W15 rewritten for the helper.
<!-- THOUGHT:END -->
