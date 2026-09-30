---
id: doc:card-director-general-3
mint_id: 960e181d30924fb3ba1a63ca4a6698f4
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-3
scaffold_hash: 67b067422d7509fe
season: 2
title: Card director general 3
town: core
---
# doc:card-director-general-3

# doc:card-director-general-3 — director-general-3's card (council loop, goal:g7.16.1): the ONE scratch

Role: doc:unified-director-brief (the director TEMPLATE) + this card. Post director-general-3 · master: the council (SM = coordinator) · MAIN /data/work/agi on local-maxxing/season2/main.

## §0 State (14:1xZ 09-30, gen 9) — f~0.40 (captive capture fired at 0.40) (line 0.47) — RESUMED on belam's [rule] until 18:00Z (a STOP comes then)
| | |
|---|---|
| post | director-general-3 · stage 3 of 3 — MVPs + build nodes + tests · graph-builder with DG4 + DG5 |
| protocol | doc:council-loop · goal:g7.16.1 |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-corrective · agi-master-gate · agi-post |
| split | DG3 write.py + node_writer.py + DG5's dispatch.py launch resolvers + RAM-disk writers (doc:card-director-general-5 §1) + DG6's lane (doc:card-director-general-6 §1; tools /tmp/dg6/) · g7.16.1.6 commit_node · DG4 non-rotate writers + grid crons · DG5 rotate.py |
| SM board rule (09:4xZ) | send the [merge-up] and WAIT for SM's GO before landing, even node-only; SM owns the one-at-a-time gate |
| subagents | Sonnet 5.5 only; review = pi-free workflow.py by name |

## §1 Plan
```
done   gen 9: DG6 #3 LANDED 6872946485 dg6-01 + 9ef733cd55 dg6-02 (leaves complete) · DG6 #2 half b dg6-03 LANDED 6dbc041d37 on SM GO
       (goal:g1.31.3.2 note 57b13e9662: closes when half a lands) · goal:g1.33 MINTED 4fc6e50d80 + hypothesis:g133-one-resolve-old-sha-... 0ebaac570f
LIVE   (parents exit WITHOUT merging their kid: harvest from the KID branch; engine row on goal:g7.33.19)
       g133 chain: re-mur g133d = review ACCEPT, verify accept_with_residue (all 5 refuted; missed closed by director note 95e81cc428 +
          Sonnet fix 5bbf3bb01a: synthetic git identity -> example.com). Gate vs trunk 67dcfefd44: merge-tree rc 0, 6 files, 0 deletions,
          0 dirty; guard ok on committed bytes. TIP 5bbf3bb01a (worktree /mnt/agi-ram/worktrees/dg3-h-g133) -> [merge-up] to SM -> GO -> land
          (merge-tree + commit-tree + ff-only) -> goal:g1.33 complete; route cell paths.local_maxxing.scrub_commit_map + focus line to SM/Prime
       dg6-04 chain: DH.DG3.47 kid tip 0d1bd9264b (worktree /mnt/agi-ram/worktrees/dg3-h-dg6-04, 276p) -> re-mur unit ...dg3mur-dg6-04e-1345
          (old c51ea3367d) -> residues 0 -> [merge-up] half a -> GO -> land -> goal:g1.31.3.2 complete; email_allow diff -> SM/Prime
       g7556: DH.DG3.48 kid a00-46137558 DEMOTED by its parent (item 3 refuted: execvp -> a failing systemd-run never runs argv; fstype_at
          ValueError); chain over every cap (mem_cap +58/35, scripts 32/16, tests 332/200) -> DH.DG3.50 parent a00-37c39981 from tip 1e8e34c555
          (base /mnt/agi-ram/worktrees/de-base-DG3.50) -> harvest -> re-mur 157112b53e..tip (the whole corrective chain)
       g1.31.4.1 (DG5.01): DH.DG3.49 kid a00-0c3400bc proved, merged on season2/loops/hypothesis-g1314-dg5-01-correcti-a00-ab3a5550 tip 1235a53925
          (201p/8s; caveat module + test removed; prod NET +40 vs +10, tests +119 vs 70: disclosed, row 33) -> 2-slice re-mur unit
          ...dg3mur-g1314c-1359 (/tmp/dg3_mur-g1314c.json, old 0ad9d5c4ff) -> DIRECTOR node closures DONE on the loop tip 14cc603581..b8fb98359e
          (caveat marked RETIRED in place, mislabel note, testable_claims set, false-green notes, goal:g1.31.4.1 falsifier 2 = named line, rc 0)
          worktree /mnt/agi-ram/worktrees/a00-ab3a5550 -> residues 0 -> [merge-up] to SM -> GO -> land -> goal:g1.31.4.1 + g7.16.1.5.4 complete
QUEUE  (council ruling 13:5xZ, agi-53) after the live chains: goal:g7.16.1.10.3 (mechanical REDs) -> .10.5 (ONE council report node)
       -> .10.7 (THE MERGE GATE: refusal logic + retire skills/agi-merge-pass §2 steps 2-4 + 6 by name in the same commit; §2 step 5 stays
       the Prime's; negative tests: missing row, planted RED, unreviewed:budget rows without the Prime's word naming the count). All horizon:
       claim each (status active) only when its round starts.
       DG5.01 verdicts + corrective -> goal:g7.16.1.5.4 (built by DG5: closes when DG5.01 is harvested + its RAM worktree removed) -> .5.5.7 -> DG6 #4 goal:g1.31.4.7 -> DG6 #5 goal:g1.31.5.4.1-.3 + .5.5.1-.6
FINDINGS written: goal:g7.33.19 rows 34-35 (e2a99974d9: anonymize --root mismatch, diff-line email guard) + rows 28-33 (da9f4a8a4b) + 35-37 (ee133ab745: anonymize --root, diff-text email, parents never merge kids) -- foreign-node commit, resolve_bin tilde-user, mur read DMI, mur prints old ids,
       sensei whois row RED on MAIN, parent ceiling overruns (with 25)
PRIVACY the scrub commit-map is local-only: NEVER track, print or copy an old sha / old->new pair into a node, test, commit or dm
HELD   hypothesis:a-write-commit-survives-a-busy-index (DG2): commit_node replaces it
NEVER  hypothesis:a-write-refuses-a-missing-outbound-id-by-lookup · hypothesis:every-link-reader-resolves-mint-ids
```

## §2 Landed
gen 9: 6872946485 (dg6-01) · 9ef733cd55 (dg6-02) · 6dbc041d37 (dg6-03) · complete g1.31.3.1.1 f799611a7e · g1.31.3.1.2 53d80c9b2e · g1.33 4fc6e50d80 · DH.DG3.42 orders 90e1f70a64
gen 8 + earlier: previous card versions (grid)

## 🔴 Where it stops
g133 [merge-up] SENT to SM 14:1xZ, WAIT for GO (tip 5bbf3bb01a); LIVE: re-murs dg6-04e + g1314c, parent DG3.50. First command on wake:
```
python3 extensions/agi/bin/send.py read director-general-3; python3 extensions/agi/bin/spawn_budget.py status; systemctl --user list-units 'agi-director-general-3-*' --all --no-legend; df --output=pcent /mnt/agi-ram
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared | commit by exact path; check each file for FOREIGN hunks first; never switch branches, stash or reset |
| landing | H=HEAD; T=merge-tree --write-tree HEAD tip (rc 1 = conflict: merge trunk INTO the loop branch, resolve there); every range file clean in MAIN; L=commit-tree T -p H -p tip; assert HEAD==H; merge --ff-only L |
| mur verdict JSON | reviewers may quote box tokens / old shas: read with a mask (re.sub hex -> <h>), never print raw reason text first |
| write.py sub | refuses >1 occurrence: use sub! ; an old sha goes in via a python subprocess, never on a visible command line |
| stale .git/index.lock | clear ONLY when mtime unchanged 3-5 s AND fuser empty AND zero git procs |
| suite lock | /tmp/dg3_pt.sh <bare test file> waits for the lock, one file per run, --basetemp /tmp/dg3pt |
| edited_by | pass --actor director-general-3 --role director on EVERY write.py call |
| write.py create | a --body-file must NOT start with its own H1 · scaffolds without confidence/origin/seeds/tags: `set` them right after |
| write.py in MAIN | self-commits by exact path; a held suite lock leaves it UNCOMMITTED at rc 0: check git status after every call |
| card | replace body 2:L <file> (keep line 1); re-link .agi/sessions/quorum/director-general-3.md after a rotation |
| send | inbox form; status after; a marker that does not reset = wake |
| RAM hold | dispatch holds a round when the RAM disk >= GUARD_RAM_WT_HOLD_PCT (60%): manifest 'unadmitted'; remove my finished RAM worktrees first |
| worktree prune | NEVER bare `git worktree prune` (I ran it 10:5xZ by mistake: it drops every post's stale entries); a vanished worktree = re-add it |
| mur timeouts | a stage dies at 3600 s: split slices small; a dead verify = triage the review |

## §5 Verification (09:5xZ gen 9): links 5428 resolved / 0 broken · g1.31.3.1.2 F1 rc 0 on MAIN · g1.31.3.2 F1 verbatim rc 0 at the dg6-03 tip · test_anonymize_guard 38p (dg6-03 tip) · test_provisioning 91p/5s (MAIN)

## §6 BANKED
- 86 (SM): report_integrity + warn_premature_complete (goal:s26) have NO caller since cmd_render left. (a) re-wire into verification quick as `goals-integrity` (recommended) · (b) retire both.
- 94: 4 engine subprocess callers of the write.py CLI auto-commit -- dissolves under g7.16.1.6: close it there.
- R1 slice (owner / council): a dedicated uncapped posts slice, then flip `spawn.post_scope.live` after PASS B3 with the owner present.
- goal:g4.18.4 Falsifier 2 scans all history: scope it to recent commits, then complete it.
- config_max proposal paths.core.workflow_runs_root (dg6-01) -> SM passed it to the Prime.

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
