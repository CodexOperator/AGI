---
id: doc:card-director-general-5
mint_id: 2ba5a1adbdcb4ea2aa3aa6d92d309253
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: belam
scaffold_hash: e13627c192e516b7
season: 2
tags:
  - card
  - director
  - director-general-5
thought_session: director-general-5
title: Card director general 5
town: core
---
# doc:card-director-general-5

Role = the director template + the HEAD (`doc:unified-head`) + the council protocol (`doc:council-loop`). This card is the ONE scratch: replaced whole, ≤ 100 lines; rules live in skills, progress on the town board.

## §0 State (09-30 04:4xZ, gen 3, meter ~0.32 of 0.47 · IDLE on the council STOP 04:00Z (fired 04:43Z): finish the step, card whole, idle)
| | |
|---|---|
| post | director-general-5 · MAIN /data/work/agi on local-maxxing/season2/main · CC Opus 5.5 high |
| goal | goal:g7.16.1.5.5 (the RAM disk's own memory budget line, assigned by the Prime) · goal:g7.16.1.5.4 ON, closes at the first live round · 7a goal:g7.16.1.7.1 · 7b after goal:g7.16.1.6 + goal:g4.18.6 |
| lanes (owner 03:0xZ) | coordination, queue order, SHAs -> sanctuary-master agi-ed · rulings and mid-work questions -> the council: alive agi-b3 · all-is-one agi-8f [242e8c] · self-perpetuating agi-53 · never the Prime |
| spend (owner 03:2xZ) | Claude usage OUT: no Opus subagents, forks or Workflow tool; agentic subtasks on pi (workflow.py --harness pi-free) or Sonnet 5.5 at most |
| split of record | rotate.py WHOLLY DG5 · dispatch.py launch resolvers · heal.py key path. DG3 = write.py/node_writer · DG4 = every non-rotate writer + goal:g7.16.1.5.5.3 (handed 03:5xZ) |
| skills | agi-goal · agi-node-write · agi-verify · agi-rotate · agi-post · agi-memory-guard |

## §1 Plan
```
.5.5  .5.5.1 BUILT 786c1c13a (ramdisk.slice + locations.ram_write_argv + dispatch RAM checkout) -- apply guard-init = the Prime (sudo)
           left: route every engine bulk RAM writer through ram_write_argv; one-shot recharge of pages already on agi-engine.slice
      .5.5.2 horizon: GUARD_ENGINE_MAX back from the 3G stopgap to a derived value (after .5.5.1 applied + DG4's cold homing)
      .5.5.3 -> DG4 (config-only: one memory home in config:guard)
.1.4  COMPLETE 4abfee9d3 / c14815594 -- run 27 accept_with_residue, 5 residues UPHELD, order 157 -> 158 -> 160 -> 161 -> 159:
      157 card committed clean (this commit) · 158 remint mints the key BEFORE the row write: a failed row write strands the post
      (defer the swap like _rotate_successor_key) · 160 dry-run remint sends findings · 161 no-witness refusal untested
      · 159 spawn (_first_seating_key) ignores key_template
7a    .1.3.3 aliases retire = season 3 · .1.3 closes on 7b's walk
```

## §2 Landed (gen 3)
- 51ed55ec7 card re-link · 37d8a473d .3.2 ONE pi template (bare pi = free row, pi:paid = paid) · 76f8ca776 complete
- 99250d4f0 command:commands excludes rotate.py stand-up (DG3's red)
- 4abfee9d3 .1.4 every stand-up keys its post from key_template (council ruling C) · c14815594 complete
- ce8a681ed / 6cfb8bdf7 goal:g7.16.1.5.4.1 minted + retired (writer = heal's sweep homing into RAM MAIN, not a sweep trigger)
- 6e171495d goal:g7.16.1.5.5.1/.2/.3 minted · 786c1c13a .5.5.1 ramdisk.slice (live probe: 64 MiB -> engine shmem unchanged, ramdisk.slice +64.0)
- gen 1-2: see git history of this node

## 🔴 Where it stops
```
IDLE on the council STOP 04:00Z. Next loop, in SM's order:
1. residue 158 (rotate.py _remint_missing_key): mint to <seat>.key.pending, write + commit the row, THEN os.replace -- mirror
   _rotate_successor_key / _apply_successor_key_gated; test: a refused row write leaves no new key file and the next pass retries.
2. residue 160: in _remint_missing_key, check dry_run BEFORE any _key_finding. 3. residue 161: a test row for the no-witness refusal.
4. residue 159: route spawn's _first_seating_key through key_template (adopt + own-box remint), or restate the goal -> ask the council.
5. .5.5.1 rest: ram_write_argv for every engine bulk RAM writer (grep GUARD_RAM_DIR / RAM_MAIN writers); a recharge tool
   (cp -a + rename inside ramdisk.slice) for pages already on agi-engine.slice, after DG4's cold homing lands (heal restart pending).
Box readings 03:4xZ: agi-engine.slice shmem 2186 MiB (3G stopgap); RAM disk 1.5G / 7G.
Next command: `python3 extensions/agi/bin/write.py goal:g7.16.1.5.5 'read body 1:60'`
```
## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared with 9 posts | commit by exact path; never commit, reset or stash another post's file |
| verify-suite.lock: my own runner holds it per file | write.py commits refuse while ANY runner holds it: commit by exact path after; a pytest inside it ERRORs at setup -> retry loop |
| systemd user manager sets TMPDIR=/data/tmp | a runner script pins `env -u TMUX -u TMUX_PANE TMPDIR=/tmp` (env's -u BEFORE the assignment) or test_workflow's leak guard trips |
| a python heredoc carrying shell text with EOF | use a distinct delimiter (PYEOF) |
| write.py replace body guards paragraphs | replace from a heading through the block's closing fence |
| node_writer indexes a root once | a test that reads a node it writes later needs its own root |
| systemd slice names: a dash nests | agi-ram.slice would sit inside agi.slice's oomd domain: the RAM slice is ramdisk.slice |
| council invariant | no parent/kid dispatch; nodes via write.py; nothing deleted |

## §5 Verification
`python3 extensions/agi/bin/links.py links` 0 broken · runners: ~/dg5/dg5-nbhd5.sh (60 rotate/heal/send/seatsig/stand_up/session_start files) · ~/dg5/dg5-nbhd6.sh (18 dispatch/cli/heal_watch/boxkit/locations files) via `systemd-run --user --unit=agi-director-general-5-<key> --working-directory=/data/work/agi -p MemoryMax=6G -p MemorySwapMax=0 bash <script>` -> ~/dg5/nbhd.out (DONE line)

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Stood up by belam-S2-L5-XVIII on the owner 23:3xZ order, verbatim: "Restart council including DG5 stand up. Then let them tackle the bundle and see how best to streamline it further." Lane per the owner 23:1xZ: "If needed, spawn director-general-5 as well and have them tackle the rotate/spawn unification/template+config gutting and streamlining."
<!-- THOUGHT:END -->
