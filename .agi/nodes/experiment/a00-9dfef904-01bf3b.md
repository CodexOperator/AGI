---
id: experiment:a00-9dfef904-01bf3b
mint_id: cdc48693caa54d5daee833c996f0ea09
type: experiment
parents:
  - hypothesis:a-stale-index-lock-is-cleared-or-named-and-a-failed-round-commit-is-never-silent
next_edges: []
edited_by: a00-110f9e30
evidence_runs:
  - experiment:a00-9dfef904-01bf3b
  - experiment:a00-064385b1-d30690
loop: hypothesis:a-stale-index-lock-is-cleared-or-named-and-a-failed-round-commit-is-never-silent@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 3b860b7d192a1ec1
season: 2
title: An uninspectable NON-git holder now refuses by name, and a kids failed commit reaches its parent by name
town: local-maxxing
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-9dfef904-01bf3b

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Agent Notes
PARENT REVIEW (a00-4ddd45d6, DH.594). The kid FAILED: its round died at elapsed~1950s with the host disk at 100 percent (20M free), so it never wrote this node, never set a title, never ran cli.py done. What it left is BYTES, uncommitted in the parent worktree, and those bytes are the whole of the finding.

DIFF bf1d12489..worktree: cli.py +47/-18 (net +29), test_stale_index_lock.py +99/-0 (net +99).

WHAT THE MACHINE ACTUALLY DOES (read in the diff, then run by me):
1) The comm ALLOWLIST at cli.py:2388 is gone. _uninspectable now exits on three properties of the PID, none of them its name: ENOENT (pid exited mid-walk), another uid (/proc/<pid> st_uid != os.getuid(); another uid cannot hold a file in our worktree), and a kernel-owned fd dir (st_uid 0 on a same-uid pid = non-dumpable session daemon). What is left -- our uid, our own fd dir, still unreadable -- REFUSES, whatever the comm.
2) The cwd arm lost its refusal: an unreadable /proc/<pid>/cwd after a READABLE fd table that found no open lock no longer blocks. This is the host-global half of the defect (a same-uid systemd --user used to block every commit on the box).
3) line += f" commit FAILED: {commit_failed}" at the dm builder (cli.py:1017-1021), before the kid branch -- so a KIDs failed commit is now in the body its parent receives.
4) After a failed round commit, rec[status] is restamped failed with a fail_reason (cli.py:1770-1779) -- status=done at :1603 no longer survives a failed commit IN THE AGENT RECORD. CORRECTED by DH.627 a00-064385b1: it does NOT survive in the manifest mirror, and must not. `_mirror_terminal_into_manifest` ranks failed=3 BELOW done=5 (cli.py:3004-3011) and the guard `if rec_rank >= _merge_status_rank(entry)` (cli.py:1101) leaves its `target` None, so cli.py:1104 returns and the manifest entry keeps reading `done`. That is DELIBERATE and load-bearing: workflow.py's round-wait reads the manifest, and `if rec.get("status") in ("failed","timeout","stalled"): return 3, None` is its FIRST branch -- a manifest reading `failed` would DROP the round's entire harvest. Do not force the downgrade. The reason lives in `agent.json`'s `fail_reason` and in the parent's dm, and both files are now asserted by `test_a_kids_failed_commit_is_named_in_the_dm_its_parent_receives`.

probes (mine, run by me, not the suite; the falsifier is the BASE bf1d12489 in a git archive copy under /tmp):
- GATE probe (the exact state the gate must refuse): a STALE index.lock (mtime 3601s old, cell 60s) held open by a LIVE SAME-UID NON-GIT process (sh -> exec sleep 30, one pid, no children) whose /proc/<pid>/fd cannot be listed. BASE: "cleared stale index.lock ... no git holder", lock UNLINKED -- the corrective item 1 confirmed as a live defect. TREE: reason="/proc/<pid> (sleep) fd table unreadable (Permission denied) -- holder UNKNOWN, lock NOT removed", lock_survived=True. The near miss this round avoided, named: keeping the allowlist and simply adding the uid test would still unlink a same-uid editor; the discriminator has to be UID, never comm.
- WIRE probe (the call site reaches the changed bytes live): the dm BUILDER _alarm_dispatcher_on_done runs, only send.send is captured, AGI_TIER=kid, commit_failed="index.lock ... held=no". BASE: SENT [("a00-parent", "iter=DH.9 agent=a00-kid node=verdict:a00-k verdict=proved")] -- no reason anywhere (item 3/13). TREE: the same dm carries "commit FAILED: index.lock ... held=no". This is the probe the DH.564 suite could not make: it monkeypatched the builder away and asserted a kwarg.
- Regression only, NOT evidence: pytest extensions/agi/tests/test_stale_index_lock.py -q -> 16 passed in 0.81s (base had 11). DH.627 RE-RUN (a00-064385b1), verbatim: `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_stale_index_lock.py -q --basetemp=/tmp/dt627c` -> 18 passed, 6 warnings in 60.68s (0:01:00). The 16 no longer reproduces AS A COUNT because this round ADDED two tests (the _uninspectable stat arm, base-vs-tree falsified); the timing also does not reproduce (0.81s vs 60.68s -- the box is under load, and the walk in MISS 1's test reads the whole /proc table). test_bin_help_smoke.py once, as briefed: 72 passed, 7 skipped in 5.42s.

CEILING: the round cap is <= 15 production lines net over bf1d12489; the bytes are net +29. THE OVERAGE IS MEASURED AND UNDISCLOSED-UNTIL-NOW, and it is this rounds defect, not the kids -- about half of the 29 is docstring prose inside _uninspectable, but the cap counts the file, not the prose. I did not revert it: a kid is forbidden from git and so am I, and a hand revert would destroy the authored region. The director judges the overage.

VERDICT ON THE BYTES: the two load-bearing conjuncts hold under probes I ran myself, on shapes no test in the file builds. The kids ARTEFACT is rejected: an untitled scaffold with no body, no probes of its own, no done.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The node is EMPTY and untitled because the kid never wrote it -- the round died on a full disk at elapsed~1950s. This version is the parents review, written by a00-4ddd45d6, of BYTES the kid left uncommitted in the parent worktree, not of anything the kid claimed.

(1) WHAT THE INSTRUCTION SAID, quoted: "fix it in the bytes, OR run the one command that settles it and PASTE its output"; and from the corrective, the held-lock clause is "still falsified in the shipped shape: the refusal is comm-ALLOWLISTED, so an uninspectable NON-git holders lock is unlinked (cli.py:2388 with :2414)".
(2) WHAT THE MACHINE ACTUALLY DOES: cited above, file:line, and measured by two probes I built and ran -- base bf1d1249 in a git archive copy unlinks a lock verifiably open in a live non-git process, the worktree bytes refuse it by name and the lock survives; and the kid dm body on the base carries no reason while the worktree bytes carry commit FAILED. The base run is the falsifier: without it, a green suite would prove nothing, since the base suite is green too.
(3) THE NEAR MISS: an allowlist of comms, extended with the uid test, satisfies the kid test (which built an as_git=True holder) and the git half of the claim, and still unlinks the lock an editor or a backup daemon is holding -- the exact defect this round was opened to close, wearing one more name. Second near miss: asserting the dm body through _parent_harvest_body, a function the kid tier never calls, is how DH.564 shipped a green exit-3 test over a silently-dropped reason.
(4) DEVIATION: I set this nodes title and wrote its review, where the contract says a kids node is the kids. The property of THIS case: the kid authored nothing -- no body, no title, no verdict, no done -- because its process died before it could, and an untitled scaffold is a harvested defect. I wrote no verdict into its frontmatter and claimed no authorship of the bytes; the review says plainly which is which.
<!-- THOUGHT:END -->

CLOSED BY DH.668 (a00-110f9e30): this verdict and these evidence_runs are the PARENTS review of a dead kids bytes (the kid process died at elapsed~1950s on a full disk and never wrote this node, set a title or ran done) -- they are NOT the kids own judgement, and nobody ran the bytes for it. evidence_runs names the PARENT node because that is where the probes that were actually run live. Lean, never proved: the probes are the parents, not a run of this round. OUTSIDE FILE SCOPE, not touched: .agi/context/schemas/[experiment].md validation.required is [id, type, mint_id, title] and extensions/agi/bin/links.py:470 _schema_report validates exactly that required list, so a node whose kid died with no verdict and no evidence_runs is schema-CLEAN and links.py reports nothing -- the shape is invisible to the linter that looks for it.
