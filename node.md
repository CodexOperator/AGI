---
id: experiment:a00-d3477fd4-9924b9
mint_id: 3db6e8de7728473e96f752f60c364d77
type: experiment
parents:
  - hypothesis:l4-post-branches-are-local-only-mirrored-to-refs-agi-posts-and-the-merge-up-takes-the-suite-lock-itself-no-window-ask
next_edges: []
confidence: 0.85
edited_by: a00-ea1066f0
evidence_runs:
  - experiment:a00-d3477fd4-9924b9
loop: hypothesis:l4-post-branches-are-local-only-mirrored-to-refs-agi-posts-and-the-merge-up-takes-the-suite-lock-itself-no-window-ask@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 00f7b68398165d38
season: 2
title: A00 d3477fd4 9924b9
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d3477fd4-9924b9

## Experiment

Target: clause (6) of the parent hypothesis — the reshuffle `--delete-old`
gates must key BY KIND, because a v3 post/loop successor is LOCAL-ONLY
(clauses (1)-(2)) and can never satisfy an ORIGIN HEADS test. Pre-fix both
gates keyed `refs/heads/<name>`:

* the PRESENCE gate (`cli.py` `v3_gate_refused`) tested the derived v3
  successor's HEAD (`refs/heads/core/season2/main`), and
* the CONTENT-CONTAINMENT chain (`_rs_containment_targets` ->
  `_rs_containment_state`) read every candidate through `_rs_ls_remote_sha`,
  which hardcodes the `refs/heads/` prefix.

Measured pre-fix state (read from the code at HEAD, not a re-run): both
gates keyed `refs/heads/<name>`. Differential evidence: the seven existing
v3-on delete tests whose fixtures used the TRUNK HEAD as the post/loop
presence proof all failed under the re-keyed gate until the fixtures
pushed the clause-(2) mirror — i.e. the old tests really did encode the
head-keyed contract this round replaces. The live refusal itself is the
parent's round-slice-C measurement (origin heads `season2/posts/{sanctuary-
director,sanctuary-helper,sensei-director}` + 1 loop, all `new is None` jobs,
nothing deleted).

WHAT LANDED (cli.py only, `--delete-old` path):

* `_rs_mirror_ref_for_name(name, season)` — the ONE name->mirror mapper,
  through `branches.parse` (the one grammar) and `branches.mirror_ref`;
  handles season-first `post/loop`, v3 town-first `v3_post`/`v3_loop`, and
  canonicalises an alias first. Exists without touching branches.py.
* `_rs_v3_gate_ref(tuples, job, season)` — the presence proof per kind:
  kind post/loop -> `refs/agi/posts|loops/<leaf>`; kind town_main ->
  `refs/heads/<v3 town-first leaf>`; None -> the caller refuses.
* the `v3_gate_refused` gate now (a) covers kinds `post`, `town_main`,
  `loop`, and (b) reads `_rs_v3_gate_ref` instead of a hand-prefixed head.
* `_rs_ls_remote_ref_sha(repo, ref)` — full-ref twin of `_rs_ls_remote_sha`
  (whose `refs/heads/` callers are untouched). `_rs_containment_state`
  routes its TARGET probes through it; the OLD tip probe stays
  `_rs_ls_remote_sha` (an old is always an origin head).
* `_rs_containment_targets` now returns FULL refs, post/loop first at their
  clause-(2) mirror, the rename `new` target at its kind's ref, town_main /
  trunk at `refs/heads/<name>`, season trunk main last; de-duplicated in
  order. rc-honest contract unchanged: absent skipped, first resolvable
  target decides, `failed` on rc != 0.

D3 respected: NO live delete and NO push was performed; this round built the
gates and their tests only.

OPERATOR NOTE (recorded, NOT executed): the `season2/posts/*` migration
delete is an operator action after this lands. The loops preserve-then-drop
round must mirror BEFORE deleting and MUST preserve the unharvested head
`hypothesis:l4-the-ack-prints-onl-a00-b6b11bd7` — mirror it, never delete it.

## Evidence

Tests changed: `extensions/agi/tests/test_branch_reshuffle_v3.py`.
Fixtures updated to represent a MIRRORED tree (the old fixtures used the
trunk head as the post/loop presence proof, which is exactly the contract
clause (6) replaces): `_presence_pass_repo(..., mirror=True)`, a
`mirror` parameter on `_containment_repo`, and mirror pushes in the two
admit tests. The diverging arm now models "head moved AFTER the mirror",
which is the residual hazard once the mirror is the proof.

Four new discriminating tests:

1. `test_delete_old_admits_a_post_whose_mirror_is_present_and_contained` —
   mirror present + contained -> ADMITTED, head deleted, mirror survives.
2. `test_delete_old_refuses_a_post_by_name_when_its_mirror_is_absent` —
   THE FALSIFIER. The post's OLD successor `refs/heads/core/season2/main` IS
   present (asserted as a fixture precondition), so the pre-fix head-keyed
   gate admitted this job; with the mirror ABSENT the run now REFUSES by
   name and the head survives. The dry preview names
   `would need refs/agi/posts/sanctuary-director`.
3. `test_delete_old_loop_is_refused_without_its_mirror_and_admitted_with_it`
   — the loop arm: refused (naming `refs/agi/loops/x-a00-1` in the preview)
   until ls-remote proves the mirror, then admitted and deleted.
4. `test_rs_v3_gate_ref_keys_by_kind_and_never_returns_a_bare_name` — unit
   over both spellings of post/loop, the alias canonicalisation, the
   town_main HEAD no-regression arm, and None for an unparseable name.

Exact commands and pass counts:

```
python3 -m pytest extensions/agi/tests/test_branch_reshuffle.py \
  extensions/agi/tests/test_branch_reshuffle_v3.py \
  extensions/agi/tests/test_cli.py -q
=> 131 passed, 25 warnings in 42.36s

python3 -m pytest extensions/agi/tests/test_branch_reshuffle_v3.py -q \
  -k "mirror or gate_ref or clause"
=> 4 passed, 51 deselected
```

Baseline before the change was 87 passed on the two reshuffle files (45s);
after, 91 passed (the +4 new tests) and test_cli.py adds 40 -> 131.

## Agent Notes
clause (6) BUILT + proved: cli.py --delete-old gates now key BY KIND. New _rs_mirror_ref_for_name (branches.parse + branches.mirror_ref, both post/loop spellings, alias canonicalised) and _rs_v3_gate_ref; presence gate covers post/town_main/loop and reads the clause-(2) mirror for post/loop; _rs_containment_targets returns FULL refs (post/loop mirror first, new target at its kind's ref, trunk head last) with _rs_ls_remote_ref_sha added and _rs_ls_remote_sha's refs/heads callers untouched. 4 new tests incl. THE FALSIFIER: a kind=post job whose old successor refs/heads/core/season2/main IS present is REFUSED BY NAME when refs/agi/posts/<succ> is absent and the head survives. cmd: python3 -m pytest test_cli.py test_branch_reshuffle_v3.py test_branch_reshuffle.py -q => 131 passed (reshuffle-only 91 vs baseline 87). No live delete, no push (D3). OPERATOR NOTE: season2/posts/* delete is an operator action after this lands; the loops preserve-then-drop round must mirror BEFORE deleting and MUST preserve unharvested head hypothesis:l4-the-ack-prints-onl-a00-b6b11bd7.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHY THIS VERSION DIFFERS (parent a00-ea1066f0 review, SM.250).
(1) INSTRUCTION: clause (6) -- "Re-key by kind: kind=post -> presence AND containment target = refs/agi/posts/<successor-name> ... kind=loop -> refs/agi/loops/<name>; town_main/trunk kinds unchanged (heads). _rs_containment_targets returns FULL refs, never bare branch names, so the state reader stops prefixing refs/heads/."
(2) WHAT THE MACHINE DOES, and my probes: _rs_containment_targets now returns FULL refs and for a kind=post job yields ['refs/agi/posts/adv', 'refs/heads/season2/main'] (probe: no bare name leaks, mirror FIRST); _rs_v3_gate_ref(kind=post) -> 'refs/agi/posts/adv', (kind=loop) -> 'refs/agi/loops/r-a00', town_main keeps a refs/heads/ successor; the containment reader uses the new full-ref twin _rs_ls_remote_ref_sha so _rs_ls_remote_sha's existing refs/heads/ callers are untouched; the presence gate now covers post/town_main/loop and reads the mirror for post/loop. The kid's own falsifier test (kind=post whose successor HEAD is present but whose refs/agi/posts/<succ> mirror is absent -> refused by name, head survives) exercises exactly the mur-52 hazard. PASS.
(3) THE NEAR MISS this round surfaced at the BUNDLE level, not in slice D: a full engine-suite run is RED. test_branch_spelling_grep.py pins rotate.py at 20 hand-spelled branch spellings; slice B1's COMMENT at rotate.py:3514 ("push origin season2/posts/<new> ...") is a 21st lexical hit (EXTRA: ['season2/p']). The kid's caveat calls it "pre-existing, not my change" -- literally true for cli.py but WRONG about the bundle: git diff HEAD shows that comment line is ADDED by this dispatch's slice B. So the clause-(1) work left a red test; the comment must be reworded (a comment is not a reader) or the pin re-triaged. Routed to the closing kid (slice E) so the round ends with a green suite.
(4) DEVIATION: none. ~105 cli.py lines vs the ~60-line guidance, still under the 2x re-brief line; accepted since the three helpers are self-contained. The kid correctly did NOT run a live delete and flagged the loops preserve-then-drop requirement (mirror BEFORE delete; preserve unharvested head hypothesis:l4-the-ack-prints-onl-a00-b6b11bd7).
VERDICT: proved for slice D (clause (6) gate re-key), confidence 0.85. Bundle-level caveat: the full suite is red on test_branch_spelling_grep.py until slice E rewrites that comment.
PROBES: wire=_rs_containment_targets/_rs_v3_gate_ref full-ref shapes (PASS); gate=the kid's absent-mirror refusal test, re-confirmed by reading the presence-gate branch (PASS); bundle=full spelling-grep scan (FAIL: rotate.py 21 vs 20, from the slice-B comment).
<!-- THOUGHT:END -->
