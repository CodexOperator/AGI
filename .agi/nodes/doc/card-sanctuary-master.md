---
id: doc:card-sanctuary-master
mint_id: 9a4a831c938a4501b30d37248ad319c0
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 3e856c7e9b80c2ab
season: 2
tags: []
title: Card sanctuary master
town: core
---
# doc:card-sanctuary-master

# doc:card-sanctuary-master — sanctuary-master's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; <= 100 lines; written DURING the work so a dead session is resumable.

## §0 State (22:0xZ 10-10, date -u) — gen 35 LIVE · trunk MAIN @ e4983fea7c · no gate trees open · E ~3 GiB · belam = belam-s2-III · NEW ROUTE: council approves, belam only ffs (owner 21:5xZ)
| | |
|---|---|
| post | sanctuary-master: master-gate for local-town + the directors' BOARD COORDINATOR (sequencing, placement, gates = me · every [decision] + every landing OK = the council: alive · all-is-one · self-perpetuating, a split -> belam breaks the tie · belam = owner items only: host acts, spend, season close) |
| lanes | Sonnet 5.5; every MUR = skill agi-review: review-lanes.sh BASE TIP <scratch> -> one Sonnet Agent per lane on doc:agi-review-brief (awk past BOTH fences) + ONE adversarial verifier; mechanical REDs mine |
| holds | g7.16.1.11 HOLD: no NEW round on key / identity / signing / rotate / spawn-row / write-gate unless belam lanes it (quote belam's word to the builder) · a HOST ACT needs belam's GO per act |
| land step | (1) mint signed merge(s) on the LIVE trunk (commit-tree -S, parents trunk + tip, tree == gated) (2) box the 3 council posts `[review <L>]` + gate numbers (3) ONE council post answers `[approve <L>]` / `[return <L>: why]` (4) box belam `[merge-up] ... ff-only <L> · council: <post> approve <ts>`; belam runs the secret guard + ff, nothing else (doc:council-loop §Rulings and landing; skill agi-master-gate §Land) |
| skills | agi-master-gate · agi-memory-guard · agi-rotate · agi-goal · agi-send · agi-review (new, belam 7851c52ce3) |
| peers | box send/read as sanctuary-master ONLY; DG1-DG5, thought-master, council (alive, all-is-one, self-perpetuating; level 2 = mine), belam |

## §1 Plan
```
QUEUE (gen 35), in order:
 (1) .8 LANDED d50c519dde (council alive 00:46Z; 3rd send, 2 returns: -z fail-open, CR+LF twin + new-deprecated parent). Residues = goal:g7.16.1.11.8.1 (mine, record only, HOLD); two-parser residue -> g1.43.1 (DG1 879e32e663)
 (2) LANDED 10-11: .36 tui 80a193ae73 (leaf .36.1 hooks-loaded; belam banked a claude pin, gate = RUN the new binary) · .20 v5 alert c6f2d759a5 (leaf .20.1; DG4 'restarted fresh' 128ae202c8 gating). MEASURE: first director restart -> [rotation-alert] in my box. box-wake.t.sh leaks under load (341 procs, DG4 01:0xZ) -> DG2 fixing. Inbox-retire cut HELD.
 (3) goal:g7.16.1.11.37 retire AGI_SEAT (owner 02:4xZ: 'agi seat shouldn't be used anymore'; belam's drop-in 52-post-env = live half 299337b255) -> DG4: unit AGI_POST+AGI_BOX, pieces, ONE python helper (56 hits / 13 files), lane · .38 strand guard, both directions (council: own leaf NOW) -> DG3 · .39 refs carry (record; [red] to belam: local-town refs/archive?) · rollup on .11 must place ONE parity leaf (15 rows) + fence trend/eviction rule
 (4) goal:g1.43 (mine; low): rows 2-19. Row 6: .34 body :38 still pre-fix. · (5) LOOP END (owner: not optional): outcomes -> MY bigger_outcomes -> council -> overview -> belam. 15 goals closed since 10-01, 0 outcomes: mine 4 written (.11.1+.2, .11.3+.5, g4.6.1, g7.16.1.5.3); DG1 7 + DG5 2 placed 02:5xZ -> then bigger_outcome(s) on g7.16.1.11. OPEN: refs/archive 0 on MAIN (19 at 09-30)
 WAITING: the OWNER via belam on host-act GOs (.4 .7 .11.1 .12 ring install .18 units) + the season-close set; .15 W = council design
```

## §2 Landed (each landing message carries its gate numbers; git log --grep 'sanctuary-master: LAND')
- gens 16-33: git log --grep sanctuary-master · gen 34 10-10 04:47Z-09:3xZ: 6de0f00786 + 9db6ed340c (key-stranding + residue rows) · 0aac338b6d .13.1 .13.2 · e0b749fecc .11.1.1 · acdbed2c8f .21 .3 · 652d565152 .36
  · 957e0cbc7d TM g5.28 (first agi-review run) · bde6fd808e .5 rule + F1 amend · 592cb1e416 .20 (C) mail_alert retired + .5 C2/C3 (610 B left) · 53a26cfe96 .13.3
  · 19327c2eb2 .5 .34 complete · b216f5321f .19 · a65c401470 .13.3 complete -- trajectory check answered (table + season-close proposal) and 5 directors placed 08:4xZ
- gen 35 10-10 09:35Z-: 466576bd1e .13.3 follow-up + a0dc449961 dg1-close15 · 6d272246ec .20 (B) + 3e4e33d91b g1.43 row 13 · f31c1ec58e .36 reopened · d9a3ec8efb .20 corrective · 832a7f0eaf .20 notes (3 unmeasurable causes; alerts.audit -> SM e340ca76a4 by belam) · f0c932f727 .20 residues (B12 returned once: load flake)

## 🔴 Where it stops
```
sanctuary-master gen 35 03:04Z 10-11: 5a6f6ce9a6 approved -> belam ff; .38 reshaped (one write path agi-at, refuse-only doors, box to self) a1fbfc48ce -> DG3; [red] belam: ~/hooks EMPTY on all 14 posts + refs/archive carry; waiting DG1/DG5 outcomes -> .11 rollup
NEXT COMMAND: AGI_POST=sanctuary-master box read; on [approve <L>]: box belam [merge-up] ff-only <L> · council: <post> approve <ts>; gate DG4's .37 tip (lane: AGI_POST only, no AGI_SEAT); watch refs/box/*/sanctuary-master for the first [rotation-alert]
```

## §4 Traps (rules live in skills)
| trap | rule |
|---|---|
| my /dev/shm gate trees + suites are charged to MY scope (gen 31 E 06:01Z: started a FULL at 2.7 GB, under E's 3 GB floor, then freed my own trees) | suite only above the box floor (E 3 GB, else 4 GiB) + PSI low, ASSERTED in the SAME command that starts it (`[ $(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo) -ge 3 ] || exit`); remove finished trees BEFORE; stop = every pid with cwd under the gate path, then worktree remove; NEVER prune · a PLACEMENT fan-out is load too (gen 34 08:2xZ: 5 directors placed at once = 5 whole-graph links/schema scans, E WARN): stagger placements, say 'changed nodes only', ONE whole-graph scan on E at a time (belam) |
| a mur REVIEWER runs mutants as belam | snapshot `ls ~/.config/systemd/user | md5sum` before each mur, compare after; the focus forbids real paths + names a scratch HOME/XDG (skill line 7736650a92) |
| a 2nd pytest in a tree whose FULL suite runs = conftest suite-lock ERROR | lanes / NEG / mur root = a SECOND detached worktree of the gate commit |
| rotate flattens the quorum card | re-link: ln -sfn ../../nodes/doc/card-sanctuary-master.md .agi/sessions/quorum/sanctuary-master.md, commit by exact path |
| MAIN shared | commit by exact path; never switch branches, stash or reset; absolute paths or ( subshell ) |
| a tool's --root that takes <repo>/.agi | given <repo> it can read 0 nodes and print a CLEAN (gen 28 census, links-style): check the node count before trusting a 0 |
| a mutant anchored by str.index on a heading text | the FIRST hit can be a quote of it in prose (gen 29: '## DG1 RULING on B4' quoted in FALSIFIERS -> a false GREEN); anchor at line start ('\n## ...') and print the hit line no. |
| a sed/grep mutant check that greps the mutated line | a trailing comment defeats `...$`: apply mutants with python asserts and print the line |
| belam's board edits between mine | git status + re-read the row before a scripted replace; assert the old text, never blind-replace |
| the privacy guard can REFUSE a card commit silently | git status --porcelain on the card after the commit; write 'home-path' in prose · grid commit is RETIRED (owner 01:3xZ 10-08): never run grid.py commit (belam 22:0xZ) |
| inbox notices can VANISH (goal:g1.40) | a branch named in a later notice but never received = ask its sender |
| `send.py read ... | head` marks ALL read | redirect to a scratch file, then read it whole |
| the old send.py route (owner 04:5xZ: box only) | never send.py send / inbox writes / SendMessage; box send as sanctuary-master only |
| mur reviewers detached MAIN HEAD (3x) | after every mur: git symbolic-ref HEAD before any landing |
| agi-merge-up-review review stage can be HOLLOW · a row I hand a director cited a DOCSTRING (gen 31 E: send.py:937-950 said AGI_AGENT_ID then AGI_SEAT; the code puts AGI_POST first -> g24 returned twice) | the FINAL verify stage decides; reproduce each unrefuted residue yourself before returning; read every citation I send -- returns AND placements -- down to the CODE line, never a header comment (broke it again 04:3xZ: --fetch 'retries a failed push' from engine-root.md:104's comment; the retry is hub-only at :118) |
| a re-cut patched on patch (E2b0 returned 3x on parse classes) | after the 2nd return on one input class, return with a DESIGN direction, not a 4th shape list |
| agi-flush ends EVERY turn with `git checkout -q --detach posts/<post>` once AGI_POST is set (gen 35 02:48Z: ce62fd324d stranded to the reflog, no line) | after every commit in ~/t: `git update-ref refs/heads/posts/sanctuary-master HEAD <old>` (ff); a cherry-pick here cannot clear its state (packed-refs.lock) -> rm the worktree's CHERRY_PICK_HEAD |
| `git merge-tree --write-tree` on CONFLICT prints the tree id + the list | read its rc; ALWAYS check D = 0 |
| a .t.sh run with bash (false reds) · `env -i` drops the user-site pytest | run every .t.sh with sh (dash) · PYTHONPATH=$(python3 -c 'import pytest,os;print(os.path.dirname(os.path.dirname(pytest.__file__)))') |
| a Bash call that hits its 120 s timeout is MOVED to the background and keeps running (gen 31: a grep -rl over .agi/ ran 19:00-21:01Z = belam's io storm; I reported it done) | never a recursive search over .agi/; on a 'moved to the background' notice, stop it at once (TaskStop) unless it is wanted |
| crons.py show / links from a gate worktree read MAIN's graph | first live run of a gate: load the gated module in-process against MAIN's real file |
| card stamps written from memory | read `date -u` in the SAME command that writes the stamp |
| GPU-name grep with awk $NF | grep the FULL name AND the model (last two words); never print the name |
| a landing message carries what the diff guard never sees | anonymize the landing message FILE (minus the attribution trailer) before commit-tree |
| a verdict flip pending -> proved on an experiment (gen 31 nodes r2) | links/schema count it as FIXED; only the evidence dry-run sees the missing evidence_runs (self-cite = the convention) |
| a systemd SEMANTICS claim gated by text rows (gen 31: E act a5b1a41009, drop-in 'Requires=' empty does NOT reset deps -> FAILED on E) | systemd-analyze verify --root=<scratch> after the act, with the host's base *.target/*.slice COPIED in (a bare root masks every dep behind sysinit.target); run the mutant without the fix and see E's error |
| a return that STEERS a systemd setting (gen 33: my D10 'choose a Restart= that cannot respin a skip' -> DG1 took on-failure, which leaves a SIGTERM/HUP/INT/PIPE-killed loop dead: those are CLEAN exits) | before naming a unit setting in a return, read its man row in the SAME command (Restart= table, RestartForceExitStatus=, ExecCondition 1..254 = skip) and name the trade-off, never just the constraint |
| my lane list for an engine-piece change came from `git grep -l` of piece NAMES (gen 33 AA1.V: test_grid_writers.py scans engine-post.md for write sites by PATTERN, not by name -> 5 RED on the trunk after my landing; DG1 caught it) | for any .geometry/engine*.md change also run test_grid_writers.py + test_thought_hygiene.py, and grep the lanes for the FILE name, not only the piece names |
| a lane with a TRUNK argument (`T=${1:-local-maxxing/season2/main}`: 17 lanes -- agi-out-*, aa3, ckpt, grow-gate-*, agi-land-bounds) extracts its pieces from that REF, not the worktree (gen 33: my AA1.V gate ran agi-out-states on the OLD trunk piece = vacuous 44/0; the landing left 9 RED and hid a real signing-key-loss path) | pass the CANDIDATE commit as the trunk argument for every such lane; a green that does not change when the piece changes is no gate |
| a test that pins `git grep -n` output | NEG: a pure line shift (a comment line in a big file) must stay GREEN; a pinned line number = every edit reds FULL (gen 30: 4/8) |
| `pgrep -c -f links.py` / `pgrep -f <test>` count the SHELLS whose argv carries the word (my own included: gen 34 read 5 scans, 1 was real) | count real scans by comm: `for p in $(pgrep -f links.py);do ps -o comm= -p $p;done | grep -c python` |
| a mutant harness that splits specs on `|` (shell code is full of `|`/`||`) wrote garbage = 85 false REDs; a `raise` inserted INSIDE the try it tests is caught by that try's own `except` = an EQUIVALENT mutant (gen 34) | specs as python string pairs + assert count == 1; put a fatal mutant where the arm's own handler cannot catch it; a test file run while another pytest runs in the SAME tree = suite-lock ERRORs, not results |
| the box's GLOBAL git config sets core.hooksPath: it shadows fixture repos' .git/hooks (gen 35: 5 test_rotate reds on trunk AND candidate) | run every gate suite with GIT_CONFIG_GLOBAL=/dev/null; a red that vanishes under it = goal:g1.43 row 13, not the range |
| anonymize.py check --root <MAIN or my worktree> reads MAIN's .env -> PermissionError traceback (gen 35: I sent 'anonymize ok' before reading it) | --root = a scratch archive (extensions + .agi/config.json); read the result BEFORE any message that cites it |
| a gate that filters a git path list (`--name-only` without -z) skips C-QUOTED paths (" \\ TAB NL; quotepath=off only covers non-ASCII) = fail OPEN (gen 35 .8 grow.py) | every path list a gate reads: -z + NUL split; an entry the gate cannot read = refused, never skipped |
| partial tmpfs gate trees (archive of extensions + .geometry) red tests that read the whole graph (gen 35: test_successor_prompt_prepends_constitution_head) | attribute on a SAME-SHAPE trunk tree + a full checkout before calling it the range's |
| a builder's 'N rows' is not a check: DG2's '8 rows' was 7 on both trees | count the rows yourself on the trunk AND the candidate; the same count with RED -> GREEN is the gate |
## §5 Verification: every landing = merge-tree rc 0 on the live HEAD + newcomers byte-identical to HEAD + 0 D + anonymize per commit + evidence dry-run + links/schema + FULL suite with every red attributed
## §6 BANKED
- v5 MOVE 6: SM STAYS on this seat (uid agi-sanctuary-master cannot write MAIN .git/index or the working tree); belam banks a LAND BROKER for the owner. The next move is stream-master, not me.
- origin history holds a host-named ssh pubkey comment in 81d0e8729, 8a9b0ad95, 4b7d20df7 (+ a001a3c61): a scrub = history rewrite = OWNER only (sent to belam) · goal:g1.31.4.2.1.1 copilot hooks PARKED (spend = the Prime's)
- a00-fa4269d4's 40 files pinned off-repo: /data/work/agi-pins/a00-fa4269d4.20261001T0247Z.tar.gz
- .env is 600 belam:belam: NO agi-* director can dispatch -> (A) masters/Prime run directors' murs [today's practice] · (B) group:agi read ACL [owner's call]
- refs/grid in the future carrier's refspec: OWNER call banked on belam's card §6 (rec: push once, then drop)
- agi-gate's nobody needs read on MAIN (deploy fact; DG1 banked it for belam via the host-act node)
