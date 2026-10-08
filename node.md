---
id: experiment:a00-2dd38e5b-df0d42
mint_id: cbaecd5d5b584e21a2083429f2e4c220
type: experiment
parents:
  - hypothesis:l4-delete-old-presence-pass-containment-fail-is-a-named-regression
next_edges: []
confidence: 0.9
edited_by: a00-b2e311a2
evidence_runs:
  - experiment:a00-2dd38e5b-df0d42
loop: hypothesis:l4-delete-old-presence-pass-containment-fail-is-a-named-regression@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d183501812d8c6e4
season: 2
title: A00 2dd38e5b df0d42
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-2dd38e5b-df0d42

## Experiment

Test-only round. Wrote the NAMED regression the parent hypothesis asks for:
the **PRESENCE-PASS + CONTAINMENT-FAIL** shape (mur-52's original gap),
where the direct-delete job's derived v3 successor genuinely EXISTS on origin
(so the presence gate ADMITS the job) yet the old branch tip is NOT an
ancestor of that successor.

Fixture `_presence_pass_repo(tmp_path, contained)` in
`extensions/agi/tests/test_branch_reshuffle_v3.py`: a bare-origin repo with a
declared v3 town set where `core/season2/main` (the post's derived successor)
is pushed to origin, and a season-first POST `season2/posts/sanctuary-director`
is a `new is None` direct-delete job. `contained=False` puts a stray commit on
the post tip that `core/season2/main` does not contain; `contained=True`
leaves the post tip an ancestor.

Two committed tests:

* `test_delete_old_refuses_a_post_whose_content_is_not_contained` — the
  diverged variant: `--delete-old --kinds posts` exits non-zero, REFUSES by
  name with `content is NOT contained`, deletes nothing. Its **separation
  assertion** (`"v3 successor is absent" not in stderr`) proves the refusal
  came from containment, NOT from the already-covered absent-successor path —
  the successor IS present.
* `test_delete_old_admits_a_contained_post_whose_successor_is_present` — the
  inverse control: SAME presence-PASS fixture, containment-PASS, deletes
  normally. Guards against an over-broad regression.

No production code in `cli.py`/`branches.py` was changed: the existing
containment gate already refuses this shape correctly. This is the finding the
hypothesis anticipated — a test-only round.

## Evidence

Non-mutating separation proof (dry-run preview, same fixture, both variants —
successor present in BOTH, so presence passes in both):

```
==== diverged rc 0
    [DRY ] REFUSE branch delete (remote, content not contained): \
        season2/posts/sanctuary-director -> not an ancestor of core/season2/main
    NOTE: --delete-old would REFUSE 1 branch(es) whose content is NOT \
        contained in any successor or the season trunk main: \
        season2/posts/sanctuary-director
==== contained rc 0
    [DRY ] branch delete (remote): git push origin --delete \
        season2/posts/sanctuary-director
```

The refusal names `core/season2/main` — the PRESENT successor — as the target
whose content does not contain the old tip. Presence did not refuse; containment
did.

Falsifier (why the test is not vacuous): with the containment refusal removed,
the diverged post would be admitted to `git push origin --delete`, `got` would
be empty and rc would be 0 — the first assertion (`returncode != 0`) and the
survival assertion would both fail.

Suite run (test files named, never the bare directory):

```
python3 -m pytest extensions/agi/tests/test_branch_reshuffle.py \
    extensions/agi/tests/test_branch_reshuffle_v3.py -q
84 passed in 120.69s

python3 -m pytest extensions/agi/tests/test_branch_reshuffle_v3.py -v \
    -k "content_is_not_contained or contained_post_whose_successor"
3 passed, 48 deselected
```

(The `-k` selection matched three: the pre-existing loop containment falsifier
plus the two new post tests.)

FILE SCOPE honoured: only `extensions/agi/tests/test_branch_reshuffle_v3.py`
was edited.

## Agent Notes
Test-only round: added _presence_pass_repo fixture + two named tests in test_branch_reshuffle_v3.py proving PRESENCE-PASS+CONTAINMENT-FAIL is refused by name (separation asserted: presence msg absent) and the contained inverse is admitted. No production change needed; existing gate already correct. test_branch_reshuffle.py + _v3.py: 84 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (L4.365, a00-b2e311a2). What the instruction said: "a committed test names the presence-PASS + containment-FAIL shape ... A sibling assertion in the SAME test (or an adjacent one) proves the inverse control case still WORKS". What the machine does, from the staged bytes of extensions/agi/tests/test_branch_reshuffle_v3.py (+104 lines, test-only; git diff --cached shows one hunk): new fixture _presence_pass_repo(tmp_path, contained) pushes the post job s derived v3 successor core/season2/main to origin BEFORE the job branch, so the presence gate at cli.py:4346-4353 returns present and the job never enters v3_gate_refused; containment then runs at cli.py:4387-4396 and refuses with the named message at cli.py:4427. Two tests: test_delete_old_refuses_a_post_whose_content_is_not_contained and test_delete_old_admits_a_contained_post_whose_successor_is_present. Near miss: a fixture that merely renames the existing _containment_repo loop would satisfy the words and lose the mechanism -- loops never reach the presence gate (cli.py:4349 skips any job whose kind is not post/town_main), so presence would be inert rather than PASSING. The kid avoided exactly that by choosing a post direct-delete job, and the separation assertion ("v3 successor is absent" not in stderr) is what pins it. PARENT PROBES, run by me, not by the kid, on my own throwaway fixture (/tmp/probe_presence_pass_containment_fail.py): (1) gate, conjunct 1 -- hand --delete-old the presence-PASS+containment-FAIL state: rc 1, stderr "content is NOT contained in any successor or the season trunk main ... season2/posts/p1", and ls-remote still shows refs/heads/season2/posts/p1 on origin; PASS. (2) gate, conjunct 2 -- the same fixture with a contained tip: rc 0 and the branch IS deleted; PASS. (3) adversarial mutation -- copy the kid s test file, DELETE the successor push so presence fails, rerun: the kid s separation assertion fires on the presence message, so the assertion is load-bearing and not vacuous; the test is not passing by inertia. (4) wire -- --dry-run on the diverged fixture prints "[DRY ] REFUSE branch delete (remote, content not contained): season2/posts/p1 -> not an ancestor of core/season2/main", naming the PRESENT successor, so the live call site reaches the changed bytes and the containment target really is the presence-gate target.
<!-- THOUGHT:END -->
