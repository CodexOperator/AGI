---
id: doc:g716111-land-package
mint_id: ea0f68d4e03c46e88ee40f5ffbad110f
type: doc
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: director-general-3
scaffold_hash: a58e6a1fd6199410
season: 2
tags:
  - doc
  - engine
  - land
  - g7.16.1.11
title: "g7.16.1.11 rounds 5-7 LAND-READY package: as-built + split sets (itest 17/0 each, cmp 44/44 + 45/45), read sets per post kind (split post 20,374 B under the cap), LAND.md for belam"
town: core
---
# doc:g716111-land-package

The LAND-READY package for rounds 5-7 (goal:g7.16.1.11; belam CAP RULING 08:2xZ: bootstrap <= 8,192 B, 20,480 B = ONE post's read set). Assembled by a Sonnet 5.5 subagent of director-general-3; nothing landed in MAIN; both sets rehearsed in a scratch worktree (itest 17 PASS 0 FAIL each; cmp as-built 44/44, split 45/45). Bodies off-graph in /tmp/agi-land/ (asbuilt/ and split-pkg/; land.sh); sources: doc:g716111-round5-build, doc:g716111-round6-build (built from §T.1 @3772d6ff7), doc:g716111-round7-build + two scope adds (post identity line in agi-post@, pane trim cell pane_max_mb).

READ SETS (strace-measured): AS-BUILT every post reads all four engine*.md = 33,444 B (+12,964 over); pi-free / claude-code post needs engine+post+wrap = 28,286 (+7,806); hub engine+wrap+grow = 25,138 (+4,658). SPLIT (agi-fill -> engine-grow; agi-post@.service -> new engine-root; the unit loop reads engine.md engine-[pw]*.md: +38 B in the unit piece): post at start 20,374 (-106 under), hub 19,128, root at boot 10,167; a post's first node write reads agi-fill (31,598 transient). Bootstrap under 8,192 in both.

HOLES: the box privacy guard REFUSES a staged x at example.invalid, so the engine identity line ships as %i@agi (the live DG5 drop-in, not committed, uses @example.invalid) -- belam's call on the domain · R5/R7 named config:engine as a parent of the expansion nodes: the [config] spawn gate refuses it -> they land with --parent goal:g7.16.1.11 only · write.py create adds its own H1 (landed nodes larger than the build files) · ORDER: expansion nodes first, config:engine last · the seed needs the real 82 B anchor line (not invented; shipped open) · banked, not in land.sh: the hub pre-receive wiring, the seed's root install, the T7 wake row.

## MANIFEST.tsv
~~~~~text
set	node / file	repo path (target)	how	input file	input bytes	sha256[:16]	bytes on disk after landing
asbuilt	config:engine	.agi/nodes/.geometry/engine.md	write.py config:engine replace body 1:273	asbuilt/engine.body.md	7792	46ddb60a1a07f450	7987
asbuilt	config:engine-post	.agi/nodes/.geometry/engine-post.md	write.py create config engine-post --parent goal:g7.16.1.11	asbuilt/engine-post.create-body.md	8084	07e314003ee56ea3	8306
asbuilt	config:engine-wrap	.agi/nodes/.geometry/engine-wrap.md	write.py create config engine-wrap --parent goal:g7.16.1.11	asbuilt/engine-wrap.create-body.md	11771	8713520e7a6413b9	11993
asbuilt	config:engine-grow	.agi/nodes/.geometry/engine-grow.md	write.py create config engine-grow --parent goal:g7.16.1.11	asbuilt/engine-grow.create-body.md	4936	8ccdc792f6b283f3	5158
asbuilt	[goal].md	.agi/context/schemas/[goal].md	cp + git commit by path	asbuilt/[goal].md	13125	c55709eafc04b70e	13125
asbuilt	[hypothesis].md	.agi/context/schemas/[hypothesis].md	cp + git commit by path	asbuilt/[hypothesis].md	5787	0c437139d2f9f9de	5787
asbuilt	growth.tsv	.agi/nodes/.geometry/growth.tsv	cp + git commit by path	asbuilt/growth.tsv	7111	f58a48615cb83f09	7111
asbuilt	growth-aliases.tsv	.agi/nodes/.geometry/growth-aliases.tsv	cp + git commit by path	asbuilt/growth-aliases.tsv	30	41b0b5d095f129ab	30
asbuilt	agi-seed (T.1 seed, anchor slot open)	ROOT-installed, not a repo path (e.g. /opt/agi/bin/agi-seed)	root act after the anchor line is chosen	asbuilt/agi-seed.template	985	6438211d769c288a	1023 with the 82 B anchor
asbuilt	### matrix (T.1 piece 100 B; section 128 B)	inside .agi/nodes/.geometry/engine.md	part of the engine body	asbuilt/matrix.piece	100	3a0f57dc88ee3c3e	-
split-pkg	config:engine	.agi/nodes/.geometry/engine.md	write.py config:engine replace body 1:273	split-pkg/engine.body.md	7709	459b8b0bd9cc9e70	7904
split-pkg	config:engine-post	.agi/nodes/.geometry/engine-post.md	write.py create config engine-post --parent goal:g7.16.1.11	split-pkg/engine-post.create-body.md	6581	0796a52d7d2e2588	6803
split-pkg	config:engine-wrap	.agi/nodes/.geometry/engine-wrap.md	write.py create config engine-wrap --parent goal:g7.16.1.11	split-pkg/engine-wrap.create-body.md	5445	a33749c48dd49a35	5667
split-pkg	config:engine-grow	.agi/nodes/.geometry/engine-grow.md	write.py create config engine-grow --parent goal:g7.16.1.11	split-pkg/engine-grow.create-body.md	11002	aa3fb65fbe8f42f4	11224
split-pkg	config:engine-root	.agi/nodes/.geometry/engine-root.md	write.py create config engine-root --parent goal:g7.16.1.11	split-pkg/engine-root.create-body.md	2041	d7c762842e5f4834	2263
split-pkg	[goal].md	.agi/context/schemas/[goal].md	cp + git commit by path	split-pkg/[goal].md	13125	c55709eafc04b70e	13125
split-pkg	[hypothesis].md	.agi/context/schemas/[hypothesis].md	cp + git commit by path	split-pkg/[hypothesis].md	5787	0c437139d2f9f9de	5787
split-pkg	growth.tsv	.agi/nodes/.geometry/growth.tsv	cp + git commit by path	split-pkg/growth.tsv	7111	f58a48615cb83f09	7111
split-pkg	growth-aliases.tsv	.agi/nodes/.geometry/growth-aliases.tsv	cp + git commit by path	split-pkg/growth-aliases.tsv	30	41b0b5d095f129ab	30
split-pkg	agi-seed (T.1 seed, anchor slot open)	ROOT-installed, not a repo path (e.g. /opt/agi/bin/agi-seed)	root act after the anchor line is chosen	split-pkg/agi-seed.template	985	6438211d769c288a	1023 with the 82 B anchor
split-pkg	### matrix (T.1 piece 100 B; section 128 B)	inside .agi/nodes/.geometry/engine.md	part of the engine body	split-pkg/matrix.piece	100	3a0f57dc88ee3c3e	-
reference	R7 whole node as built (pre scope-add; NOT landed)	-	cmp source	asbuilt/r7-whole-nodes/engine.md	7903	73a80da4a721fab6	-
reference	R7 whole node as built (pre scope-add; NOT landed)	-	cmp source	asbuilt/r7-whole-nodes/engine-post.md	8079	4bc40cc3220c110a	-
reference	R7 whole node as built (pre scope-add; NOT landed)	-	cmp source	asbuilt/r7-whole-nodes/engine-wrap.md	11682	7ed3ba87999a9f17	-
reference	R7 whole node as built (pre scope-add; NOT landed)	-	cmp source	asbuilt/r7-whole-nodes/engine-grow.md	5105	63a2a4ea9c218ec4	-
~~~~~

## READSETS.tsv
~~~~~text
variant	post kind	nodes read (landed bytes, whole files)	total B	vs 20,480
AS BUILT	every kind (the loop globs engine*.md; strace-measured)	engine 7,987 + post 8,306 + wrap 11,993 + grow 5,158	33,444	+12,964 OVER
AS BUILT	pi-free post (DG5), needs only	engine + post + wrap	28,286	+7,806 OVER
AS BUILT	claude-code post, needs only	engine + post + wrap (cccc.ts + agi-kid + agi-infer = 2,962 B of pieces ride along)	28,286	+7,806 OVER
AS BUILT	hub / Prime as pre-receive (grow-gate)	engine + wrap (agi-fill) + grow	25,138	+4,658 OVER
SPLIT	pi-free post (DG5) at start	engine 7,904 + post 6,803 + wrap 5,667	20,374	-106 UNDER
SPLIT	claude-code post at start	same three nodes	20,374	-106 UNDER
SPLIT	hub pre-receive	engine 7,904 + grow 11,224 (grow-check/gate/project + agi-fill)	19,128	-1,352 UNDER
SPLIT	root at boot (agi-project)	engine 7,904 + root 2,263	10,167	-10,313 UNDER
SPLIT	a post at its first node write (agi-fill on demand)	20,374 + grow 11,224	31,598	+11,118 OVER (transient)
~~~~~

## LAND.md

Two packages, same pipeline: **/tmp/agi-land/asbuilt** (R5+R6+R7 exactly as built; every post kind's start read is OVER 20,480 B, see READSETS.tsv)
and **/tmp/agi-land/split-pkg** (whole-piece moves + ONE loop edit; every kind UNDER the cap). Pick one, then run:

    cd /data/work/agi && git branch --show-current          # confirm the branch BEFORE anything
    bash /tmp/agi-land/land.sh /tmp/agi-land/asbuilt  /data/work/agi      # or split-pkg
    # STOP_AFTER=n stops after step n; any FAIL line exits non-zero: stop and read it

`land.sh` IS the command list below (DG3 rehearsed it end to end in a scratch worktree, never MAIN: final/rehearsal-asbuilt.txt, final/rehearsal-split.txt).
Edit order matters: **expansion nodes first, config:engine last** (v4c's readers read engine.md only, so the extra files are inert until step 4).

| # | step (exact command) | proof printed right after |
|---|---|---|
| 0 | preflight: `git show HEAD:.agi/nodes/.geometry/engine.md \| sha256sum` must start `fb6d18ba066414bc` (v4c); no `engine-*.md`, no `growth*` | PASS x2; `links.py links` = 5616 resolved / 0 broken and `links.py schema` saved as the "before" |
| 1 | `cp asbuilt/[goal].md asbuilt/[hypothesis].md .agi/context/schemas/` ; `git add -- <both>` ; `git commit -m "schemas: tags item_regex lookahead-free (g7.16.1.11 R7 Y3)" -- <both>` | `git diff --numstat` = 2 added / 2 removed lines (one line per schema); `links.py schema` output byte-identical before/after |
| 2 | `cp asbuilt/growth.tsv asbuilt/growth-aliases.tsv .agi/nodes/.geometry/` ; `git add -- <both>` ; `git commit -m "growth.tsv + growth-aliases.tsv" -- <both>` | 7,111 B / 30 B; `grow-project .agi/context/schemas growth-aliases.tsv \| cmp - growth.tsv` rc 0 |
| 3 | per node: `python3 extensions/agi/bin/write.py create config engine-post --parent goal:g7.16.1.11 --body-file asbuilt/engine-post.create-body.md --actor belam --role prime_director` ; same for `engine-wrap`, `engine-grow` (split-pkg: + `engine-root`) | `awk 'c>=2' node \| tail -n +3 \| cmp - <create-body>` rc 0 for each; bytes on disk (8,306 / 11,993 / 5,158; split 6,803 / 5,667 / 11,224 / 2,263) |
| 4 | THE SWITCH: `L=$(awk 'c>=2{n++} /^---$/{c++} END{print n}' .agi/nodes/.geometry/engine.md)` (273) ; `write.py config:engine "replace body 1:$L asbuilt/engine.body.md" --actor belam --role prime_director` | node body `cmp` the package body rc 0; engine.md 7,987 B (split 7,904) <= 8,192 |
| 5 | extract `sect` + `agi-gate` from the new engine.md, then: every name in the pieces map through `sect NAME HEAD` (30 names, bytes == the map); `sh agi-gate HEAD`; duplicate-name count; `sect matrix HEAD \| cmp - asbuilt/matrix.piece` | all PASS, `agi-gate` rc 0 |
| 6 | `links.py links` | 5619 resolved / 0 broken (+3 nodes; split +4 = 5620) |
| 7 | (MAIN, not rehearsed: heavy / writes shared refs) `python3 extensions/agi/bin/commands.py run verify` ; `python3 extensions/agi/bin/grid.py commit --all` | verify green, node count up by 3 (split 4); grid versions the new nodes |

Steps 0-6 are land.sh; 7 is yours. Total: 7 scripted steps + 1 manual = **8**; plus 3 banked (below).

#### Holes found while assembling (all closed in the package unless marked BANKED)
1. **Parents:** R5/R7 engine-post/-wrap/-grow list `config:engine` as a parent; `[config].md` allows only goal/hypothesis -> spawn gate REJECTS it. Landed with `--parent goal:g7.16.1.11` only (the frontmatter in r7-whole-nodes/ is NOT what lands).
2. **Double H1:** `create` adds `# config:<id>`; the R7 bodies start with their own `# config:<id> — ...` -> create-bodies drop the leading `# config:<id> — ` (landed node = frontmatter + a 22 B H1 + the description line). Read sets are counted on the LANDED bytes (MANIFEST last column): all four nodes 33,444 B (32,928 B before the two scope adds; 32,769 B in the R7 doc).
3. **Order:** engine.md first would leave v4c's DG5 template looping over a bootstrap with no pieces until re-projection. Expansions first, switch last. DG5's unit re-projects from the ref change (agi-project.path); a restart inside that window uses the old loop: stop it first or accept one 30 s RestartSec cycle (root act, yours).
4. **Read sets (the ruling's metric):** the extraction loop globs `engine*.md`, so EVERY kind reads all four nodes = 33,444 B; the ruling's "bootstrap + the expansions that post reads" needs a per-kind loop. See READSETS.tsv.
5. **settings.json** now wires `agi-captive` as PreToolUse for every post (claude natively, pi through cccc.ts): a window-less post pays one jq per tool call; it exits 0 when `~/.fill` is absent.

6. **PRIVACY GUARD vs the identity line (new, blocking if ignored):** the box's pre-commit privacy guard REFUSES any staged content containing `x at example.invalid` (tested: `%i at example.invalid` refused; `%i@agi`, `%i@localhost` accepted). Landing the ruling's literal line would fail step 3/`create` for engine-post (as-built) or engine-root (split). The package therefore carries `GIT_AUTHOR_EMAIL=%i@agi GIT_COMMITTER_EMAIL=%i@agi` (the shape the unit's gitconfig already has: `agi@agi`). DG3's live `ident.conf` drop-in (example.invalid) stays valid and wins until removed; after re-projection the template itself carries the identity. Your call if you want example.invalid: it cannot go through a commit.

#### SCOPE ADD (belam 08:5xZ) — what changed, in bytes
| item | piece | before -> after | how it is carried |
|---|---|---|---|
| (1) post identity (parity 42) | agi-post@.service | 1,266 -> 1,371 B (+104 the line `Environment=GIT_AUTHOR_NAME=%i GIT_COMMITTER_NAME=%i GIT_AUTHOR_EMAIL=%i@agi GIT_COMMITTER_EMAIL=%i@agi`, +1 the `a` below) | env beats the repo-local user.* (itest: a commit under the unit's env shows `director-general-5`, author AND committer; the same repo without it commits as the repo-local identity) |
| (2) pane trim | agi-run | 357 -> 501 B (+144: one background loop line) | cell `pane_max_mb` = `AGI_PANE_MAX_MB` (the engine object projects it with ZERO new agi-project code; default 64; every 300 s, past the cap keep the LAST HALF of `~/o`) |
| (2) pane trim | agi-post@.service | `script -qfO` -> `script -qfaO` (the `a` is what makes the trim safe) | measured: WITHOUT -a the writer keeps its offset, a trim leaves 47 KB of NUL holes in 345 KB; WITH -a 0 NULs, bounded (itest + pane_test.sh: 9 MB of pane output at cap 1 MiB -> ~0.5 MiB kept) |
Side effect to know: with `-a` `~/o` survives a restart (it was truncated by `script` at each start); the trim loop bounds it. At 18 MB/h the default 64 MB cap trims about every 3.5 h and keeps ~1.8 h of scrollback.
Read-set impact: as built +516 B on the all-nodes read (32,928 -> 33,444), post-kind needs 27,770 -> 28,286; SPLIT post start 20,256 -> 20,374 (+118, after trimming the zygote's THOUGHT by 85 B so it still fits: 106 B headroom).

#### BANKED (not run, not mine to run)
- **hub wiring of grow-gate** (needs the hub path and `AGI_ALLOWED` = the allowed_signers file; I do not know the hub): `sect grow-gate HEAD > hooks/pre-receive`, plus `grow-check`, `agi-fill` on the hub's PATH (extract: `sect NAME HEAD`), `AGI_TRUNK=refs/heads/<trunk>`. Proof to run there: push a node with a wrong `key:` -> `refused: locked`. A push that changes ONLY a schema or growth.tsv lands unguarded (R7 hole 4).
- **the seed (§T.1 round 6)**: `asbuilt/agi-seed.template` == §T.1's seed block byte for byte (985 B; text with `@ANCHOR@` hashes to the doc's cd97baf8f62b6460). The anchor is ONE allowed_signers line, 82 B (`* ssh-ed25519 <68 b64>`) = the owner's or the master's PUBLIC key: DG3 does not have it and invented none. To finish: `K='* ssh-ed25519 <the 68 chars>'; python3 -c "import sys;t=open('asbuilt/agi-seed.template').read();open('/tmp/agi-seed','w').write(t.replace('<the anchor: ONE allowed_signers line, 82 B>',sys.argv[1]))" "$K"; wc -c /tmp/agi-seed` -> **1,023** (T8: <= 1,024), then root: `install -m755 /tmp/agi-seed /opt/agi/bin/agi-seed` (+ `git config --global --add safe.directory <repo>` as root, AGI_ROOT=<repo>). Needs the trunk tip SIGNED by that anchor (S7) or every sync is rc 1.
- **T7** (a Prime wake line for `refs/conflicts/*`): one `first_turn` row under prime_director in config:rotations, `git -C {repo} for-each-ref refs/conflicts/` (round-6 doc), after the seed is live.

#### RULINGS (belam 09:39Z) -> the package as it lands
| call | ruling | in the bytes |
|---|---|---|
| 1 set | SPLIT (a post reads 20,374 B at start) | land.sh runs split-pkg (unchanged) |
| 2 identity | %i AT agi.invalid IF the privacy guard admits it, else %i@agi | guard REFUSED %i AT agi.invalid (scratch detached commit, 09:4xZ, rc 1 "staged diff carries email") -> engine-root keeps %i@agi; DG5's live ident.conf drop-in aligns to %i@agi at its next restart (the R7 renew) |
| 3 parents | engine-post / engine-wrap / engine-root -> goal:g7.16.1.11.5 · engine-grow -> goal:g7.16.1.11.8 | land.sh step 3: one `case` line picks the parent (pre-patch copy land.sh.pre-parents; bash -n OK); the [config] spawn gate lists goal parents |
| 4 order | expansions first, config:engine LAST | unchanged (step 3 then step 4) |
| 5 seed anchor | not tonight; the §T.1 matrix + seed land with @ANCHOR@ pending | unchanged (no root install in land.sh) |
Also run by DG3 on belam's approval: MAIN gpg.ssh.allowedSignersFile -> .git/allowed_signers (1 line, posts/director-general-5); proof %G? = G, the post's 2 commits G, the 2 trunk commits N; undo `git config --unset gpg.ssh.allowedSignersFile` + rm the file.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam 09:39Z rulings applied: SPLIT · identity %i@agi (the guard refused %i AT agi.invalid) · parents .11.5 (post/wrap/root) and .11.8 (grow) in land.sh step 3 · config:engine last · seed anchor pending
<!-- THOUGHT:END -->
