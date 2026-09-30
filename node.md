---
id: doc:card-director-general-3
mint_id: 960e181d30924fb3ba1a63ca4a6698f4
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: belam
scaffold_hash: 67b067422d7509fe
season: 2
title: Card director general 3
town: core
---
# doc:card-director-general-3

# doc:card-director-general-3 — director-general-3's card (council loop, goal:g7.16.1): the ONE scratch

## §0 State (04:4xZ 09-30) — IDLE on the council STOP 04:00Z (fired 04:43Z) — seat agi-91 [87eb1e] (gen 7) · predecessor window director-general-3.prev = agi-8f [e68acb] (reap = the service's, never by hand)
| | |
|---|---|
| post | director-general-3 · stage 3 of 3 — MVPs + build nodes + tests · graph-builder with DG4 + DG5 |
| protocol | doc:council-loop · goal:g7.16.1 · MAIN /data/work/agi on local-maxxing/season2/main |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-post |
| sessions (03:0xZ) | Prime agi-79 · COUNCIL = Prime to directors (owner 02:5xZ): every [decision]/[red] ruling -> alive agi-b3 · all-is-one agi-8f [242e8c] · self-perpetuating agi-53 · DG1 agi-2a · DG2 agi-7f · DG4 agi-80 · DG5 agi-5b · SM agi-ed [d57b6e] · alive agi-b3 · all-is-one agi-8f [242e8c] · self-perpetuating agi-53 · stream-master agi-8c -- names shift on every rotation: trust ListAgents + the sender's from-name |
| split | DG3 write.py + node_writer.py (CLAIMED) · bundle-4 W2c-W3 rest · g7.16.1.6 MACHINERY commit_node + the ~15-min snapshot cell · DG4 non-rotate writers + grid crons + leftovers · DG5 rotate.py WHOLLY |
| owner priority | worktree cleanup: DG4 goal:g7.16.1.5.3 · DG5 .5.4 (not mine) |

## §1 Plan
```
done   gen 7: SM 138-149 all landed + ACCEPTED (bundle-4 write.py chain 129-149 CLOSED by SM) -- 8964a7c62 b514b6d47 51c664397
       eb91a95aa 4538ed382 b1f0e415f 033d75454 f0768720f · DG2 pins c55d8b9d3 · grid fork 6ec1f046c (ACCEPT, closes g4.18.6.3.2)
       W2c C goal:g4.18.6.3.3 595b9c099 (its review DIED on the Claude limit: SM re-runs on pi-free after the STOP)
       OWNER ORDER goal:g4.18.1.6: a6102199b · council ruling 6e21d9655 (ACCEPT) · 150/151/155 563cd4ca9 (MET; 162 163 found)
       · end-state restated 5c7e632c7 · HOTFIX c3c118b3c (DG4's 1098822e1 swept my WIP canonicalize; write.py refused every call)
       · council (b) on 154 + 152 153 162 163 = d8b22ae96
WAIT   SM verdict on d8b22ae96 (154/152/153/162/163) · W2c C pi-free re-review · then close g4.18.1.6 MYSELF (council: status
       complete + THOUGHT citing a6102199b 6e21d9655 563cd4ca9 d8b22ae96 + the SM run key) when residue = 0
       g4.18.1.6 falsifier 1 -> the council's (b) wording: "lands byte-exact on a canonical node; a patch whose result the
       canonical render would alter refuses by name" (write.py goal:g4.18.1.6 sub, with the THOUGHT)
NEXT   1 SM board item: goal:g4.18.5.2.2 -- the commit-a-write teaching as ONE config cell (commit-message template) + the skill
         lines (agi-goal, agi-node-write teach the self-committing write). LANE: write.py _commit_write / index.lock = DG4's
         (g4.18.5.2.1): no edit there without agreeing with DG4 (agi-80) first
       3 census leaf goal:g7.16.1.1.6.1 (config:census + verification.check_census; test_census 14 strict xfail) then .6.2
       4 DG1's goal:g6.41.1.1: hypothesis:a-session-resumed-outside-heal-gets-one-after-join-wake (ff358c109) -- boot-resume
         record + wake lines to config:rotations; NOT heal's worktree sweep (DG4)
       g7.16.1.6 machinery once the council places it + DG1 mints the leaf (commit_node signature in room directors)
       snapshot-goals integrity pair: strict xfail test_w2cb_snapshot_goals_integrity waits on BANKED 86
HELD   hypothesis:a-write-commit-survives-a-busy-index (DG2): commit_node replaces it; build only if .6 stalls (<= 12 prod lines)
ASK    hypothesis:node-type-schemas-name-a-thought-reader-that-exists (text-only, 16 schemas): DG4 first
NOTES  (DG2, no fork) test_w2ca's source check greps "mint" and misses address_resolver calls · metrics._load_graph builds
       the index twice when parents AND next_edges are mint ids (family B) · (SM run 21) brief.py:2520 level3.py:267
       links.py:391 keep their own THOUGHT closers (DG2's one-definition fork) · run-17: brief._parents_of builds a resolver per
       hop; address_resolver lets GrepError propagate on a colon-less ref; post_wire:541 a dict entry would TypeError
NEVER  hypothesis:a-write-refuses-a-missing-outbound-id-by-lookup · hypothesis:every-link-reader-resolves-mint-ids (superseded)
```

## §2 Landed
gen 7: 8964a7c62 b514b6d47 51c664397 eb91a95aa c55d8b9d3 4538ed382 b1f0e415f 033d75454 1f28e5b50 5310fc212 a6102199b
6e21d9655 f0768720f 6ec1f046c 595b9c099 563cd4ca9 5c7e632c7 c3c118b3c d8b22ae96 (cards 9d958497f)
gen 6: 99a3ce3b6 96f1c6fae 647501f0c dd141136d eeccfbaa1 f8332a053 6082bf802 4a96d8bd0 27c454526 4be11df59 22193d6ba 4a420102e
d3f1d80c0 e77d0515a 7e1bed5b8 9c069f7dc 854aceb35 688d86d6f 3b61f9f73 9a39d55fa 09a8397e4 74f03f003

## 🔴 Where it stops
IDLE on the council STOP (04:00Z, fired 04:43Z): step finished, nothing live, nothing of mine uncommitted.
Owner 03:2xZ: Claude usage OUT -- no Opus subagents; agentic subtasks on pi (workflow.py --harness pi-free) or Sonnet 5.5 at most.
Lanes (owner 03:0xZ): coordination -> SM agi-ed · rulings / mid-work questions -> the council (alive agi-b3 lead).
On resume: read SM's verdict on d8b22ae96 FIRST, then WAIT list, then NEXT 1. First command:
```
python3 extensions/agi/bin/write.py doc:card-director-general-3 'read body 1:55'
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; `git diff` each file for FOREIGN hunks first (heal.py + conftest.py carry another post's WIP 01:xZ); never switch branches, stash or reset |
| stale .git/index.lock (oomd kills, 09-30 02:4x-02:5x; cause fixed by the Prime) | clear ONLY when mtime unchanged 3-5 s AND fuser empty AND ZERO git procs (a commit running hooks holds the lock CLOSED); never chain a commit after a test run without reading it |
| shared write.py in MAIN | another post may hold UNCOMMITTED hunks: take the diff in the SAME command as the commit; if foreign hunks exist, build HEAD+mine in /tmp, test it in an isolated copy, swap-commit-restore (563cd4ca9) |
| SHA reporting | read the SHA off `git commit`'s own output line, never `git log -1` (raced all-is-one once) |
| suite lock races | /tmp/dg3_pt.sh <file> [-k ..] retries until pytest gets its own window; ONE file per run (PASS B3 on the box) |
| red-on-HEAD proof | copy the fixed file to /tmp, `git show HEAD:<f> > <f>`, run the one test, copy back, `cmp` -- never stash |
| write.py in MAIN | commits ITSELF by exact path, but a held suite lock leaves the write UNCOMMITTED with rc 0: check git status after every write.py call |
| write.py script | ONE script argument, verbs joined by ' && ' |
| row <top>.<key> | src = the row's YAML VALUE; --remove removes (empty refuses); YAML keys keep their colon |
| grid.py commit --all | never off season2/main -- the grid cron versions MAIN; do not run it by hand |
| test counts in commit messages | quote the FULL-file run, never a -k subset (SM N4) |
| messaging | until the bundles land (owner 01:4xZ): SendMessage to a session name ONLY -- no send.py, no rooms; context in goal nodes |
| /tmp after a reboot | /tmp/dg3_pt.sh (lock-retry pytest wrapper) is gone: recreate it (loop until verify-suite.lock is absent, --basetemp /tmp/dg3pt); it takes a BARE test file name (it prefixes extensions/agi/tests/) |
| build parent shapes | [mvp] · [build, goal] · [goal, mvp] · [goal, idea] |
| replace body on a heading/paragraph line | refused: widen to whole section or the blank line above |
| claims | write.py + node_writer.py stay CLAIMED by DG3 in room directors; [claim]/[release] any other shared file |
| create --set | type / parents refuse by name since eeccfbaa1: pass them as the create's type / --parent |
| write --dry-run | = submit(dry_run=True) since 22193d6ba: a new submit refusal needs NO mirror in main; update_node's own REJECTED is still invisible to a dry run |
| tests that fake subprocess.run | links.frontmatter_rows' git grep reads BYTES: a fake must answer it in bytes (4a96d8bd0) |
| a new link reader | `r = links.address_resolver(root); r(x) or x` -- an address never greps; resolve per CALL, never inside a per-file cache |

## §5 Verification (02:5xZ gen 7): write 172p/1x · node_writer 112p/3x · viewport 56p/7x · test_commands_manifest[rotate.py] RED ON HEAD (DG5's, flagged) · (02:0xZ): viewport 53p/8x · metrics 60p · zoom 41p · dashboard 23p · dispatch 139p · write/ring family 14 files green · write 164p/1x · node_writer 112p/3x · write_answers_file 42p · write_guard 32p · write_sub 17p · links 42p/2x · spawn_gate 81p · rotation_record 4p · post_wire 5p · season 56p · help smoke 70p/8s · live: 5279/5279 index rows == yaml, grep 0.47 s

## §6 BANKED
- 86 (SM wf_8ce06028-a81): report_integrity + warn_premature_complete (goal:s26) have NO caller since cmd_render left; links.py does not check parents.
  Options: (a) re-wire both into verification level quick as a `goals-integrity` command (recommended) · (b) retire both and re-point the W2c-B xfail row.
- 94 ([red] with belam from SM): 4 engine subprocess callers of the write.py CLI auto-commit (rotate.py closeout · season.py:274 · sensei.py:2465 ·
  failures.py:361) -- DISSOLVES under g7.16.1.6 (a write is a grid-ref commit, no branch): recommend closing it there, not with an env opt-out.
- R1 slice (owner / council): a dedicated uncapped posts slice, then flip `spawn.post_scope.live` after PASS B3 with the owner present.
- goal:g4.18.4 Falsifier 2 scans all history: scope it to commits after 2c412e5bb, then complete it.

## Findings for the next bundle: see the previous card version (grid) -- unchanged

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
