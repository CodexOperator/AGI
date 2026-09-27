---
id: experiment:a00-0b87822c-8fcef5
mint_id: e9ec94544c7a4965969e51cd69d2c457
type: experiment
parents:
  - hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write
next_edges: []
confidence: 0.85
edited_by: a00-280a80d2
evidence_runs:
  - experiment:a00-0b87822c-8fcef5
loop: hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 4, "class": "gate", "cmd": "probe_dh619.py probe_a -- a payload verb in the same write, the declared source ABSENT from this checkout", "expected": "the caller bytes land at the NEW name the row now carries, and the row resolves to it", "observed": "PRE-FIX: FileNotFoundError naming lib/mod.py, row=lib/renamed.py, no file at either name. POST-FIX: with a file at the new name the bytes land there and the row resolves to it; with no file at either name the refusal names lib/renamed.py, the path the row carries", "result": "fixed"}
  - {"conjunct": 4, "class": "gate", "cmd": "probe_dh619.py probe_b -- a write naming ONLY location, on a row carrying BOTH payload_ref and link_ref", "expected": "link_ref untouched: a write that never names the ref must not write the ref field", "observed": "PRE-FIX: link_ref docs/notes.md -> lib/mod.py, the body link silently repointed while its file stayed on disk. POST-FIX: link_ref stays docs/notes.md", "result": "fixed"}
  - {"conjunct": 3, "class": "wire", "cmd": "probe_dh619.py probe_c -- set payload_ref X on a row whose link_ref names a file it never claimed as payload", "expected": "the row is repointed; the LINKED file is not moved, because the row never claimed those bytes", "observed": "link_ref a/spec.md -> a/renamed.md, a/spec.md GONE, a/renamed.md created with its bytes; the same write across directories IS refused by the consent gate naming both paths", "result": "named-not-fixed (a create-path marker is needed; outside FILE SCOPE)"}
production_lines: 12
profile: balanced
role: kid
scaffold_hash: 8c9392a8c0099fd1
season: 2
title: "the effective-pair re-aim and the mirror narrowed: two payload_ref defects fixed, one named"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-0b87822c-8fcef5 — DH.619 corrective on the `payload_ref` mover

Two production defects in the DH.603 tree, both measured then fixed in the bytes;
every citation in the brief re-measured; the top OPEN residual closed. The
third item (the file-move consequence) is NAMED with a probe, not fixed, because
a correct fix needs the `create` path, which is outside FILE SCOPE.

## 0 · the citations in the brief, re-measured before acting

| brief says | bytes at the tip said (pre-my-edit) | verdict |
|---|---|---|
| the both-fields write is at write.py:2312-2313 | `:2312` `if _link_ref(...)`, `:2313` the mirror | **ON** |
| `def _link_ref` is at :2860, `:2864` is a docstring line | `:2860` def, `:2864` inside the docstring | **ON** |
| `_after` at :2323-2324, guard+aim at :2365-2366 | `:2323-2324` assign, `:2365-2366` guard+aim | **ON** |
| `plan_move` hands over `_old_ref` for a link-ONLY row; `_payload_ref` falls back to `link_ref` at :2892 | `:2892` `ref = fm.get("payload_ref") or fm.get(links.LINK_FIELD)` | **ON** |
| `plan_move` returns `_MovePlan(None, dest)` at node_writer.py:565-566 and :571-572, refusal at :567-570 | read: the refusal precedes the non-file short-circuit | **ON** |
| the move fires at write.py:2333, guarded on `_plan.src is not None`, rollback at :2339-2355 | `:2333` the guard, `:2339-2355` the rollback | **ON** |
| the outside-ref gate test is at test_payload_rename.py:345 | it was at `:345`, now `:385` (my tests sit above it) | **ON, moved by me** |

No citation in the brief was off. Two MORE drifted citations of the same class
were found in the sibling's fix table and corrected there (`write.py:1509` for
`def _preview_dry_run_gate`, actual `:1493`; `write.py:2346` for `_rb`, actual
`:2345`) -- reported in the findings row, not silently fixed.

## 1 · P-A' — the half-written `payload` verb (item 1) — FIXED

Probe on the tree as I received it (`.agi/sessions/iter-DH.619/a00-0b87822c/probe_dh619.py`):

```
P-A' RAISED FileNotFoundError: payload /tmp/tmpygc4ztgc/lib/mod.py does not exist
     — `payload` replaces bytes, it never creates.
    row payload_ref = 'lib/renamed.py'
    lib/renamed.py exists = False
```

The row is repointed, the caller's bytes are nowhere, and the error names a path
the row no longer carries. The guard `_plan.src is not None` (write.py:2365
pre-fix) is False exactly in the shape it was written for.

**Fix (write.py:2377):** the guard is `_after is not None` ALONE. The effective
pair is the right destination whether or not there were bytes here to move.
After the fix the same probe names the row's own path:

```
P-A' RAISED FileNotFoundError: payload /tmp/tmpwkhad683/lib/renamed.py does not exist
    row payload_ref = 'lib/renamed.py'
```

**Residual, named not fixed:** with no file at EITHER name the write still
refuses, because `payload` replaces bytes and never creates
(node_writer.py:643-646, outside FILE SCOPE), and the row is already repointed.
The row follows claim conjunct 3; the payload verb cannot create the file the row
now names. One line in `node_writer.replace_payload` would settle it and would
also weaken a documented invariant, so it is left to a kid with that scope.

## 2 · the test that could not fail for its own fix (item 2) — FIXED

`_graph` (test_payload_rename.py:29-42) always CREATES `lib/mod.py`, so
`_plan.src` was never None and the half-fixed guard always passed: the existing
`test_a_payload_verb_in_the_rename_write_lands_on_the_new_name` (`:287`) could
not fail for the defect it was written for.

`test_a_payload_verb_lands_on_the_new_name_when_the_old_file_is_absent`
(test_payload_rename.py:301) is the absent-source shape and asserts BOTH halves
— the caller's bytes land at the NEW name, and the row resolves to it — plus
the no-file-at-either-name refusal, which must name the path the ROW carries.
Fails on the pre-fix bytes, passes on the fixed ones (proved by reverting the
two conditions and re-running, output below).

## 3 · P-B — the mirror wrote the ref's field on every repoint (item 3) — FIXED

`set_fm[links.LINK_FIELD] = str(set_fm.get("payload_ref", _old_ref))` fired on
every write naming `payload_ref` **or** `location`. On a row carrying BOTH
fields a write naming only `location` wrote the `_old_ref` DEFAULT back over
`link_ref`, and `_old_ref` is the `payload_ref` value first (write.py:2904):

```
P-B status=updated payload_ref='lib/mod.py' link_ref='lib/mod.py' (was 'docs/notes.md')
     docs/notes.md exists=True
```

A plain `set location --confirm-move vendor` silently repointed a body link from
`docs/notes.md` to `lib/mod.py` — the file it used to name is still there,
untouched, and the link now resolves to different bytes. The "harmless because
the default equals the current value" defence holds only for a link-ONLY row.

**Fix (write.py:2317):** the mirror fires only when the write itself names the
ref — `if "payload_ref" in set_fm and _link_ref(...)`, writing `set_fm["payload_ref"]`.
After: `link_ref='docs/notes.md' (was 'docs/notes.md')`. Held by
`test_a_location_only_write_does_not_clobber_the_body_link` (:327), which fails
on the pre-fix bytes.

## 4 · item 6 — the WORSE consequence, NAMED with a probe, not fixed

`plan_move` is handed `_old_ref`, and `_payload_ref` falls back to `link_ref`
(write.py:2904), so on a row that names its file in `link_ref` ALONE,
`set payload_ref X` renames the file the node's BODY LINK named. Measured:

```
P-C status=updated link_ref='a/renamed.md' payload_ref='a/renamed.md'
     a/spec.md exists=False  a/renamed.md exists=True
```

A hand-minted row carrying `link_ref: a/spec.md` and no `payload_ref` lost that
file to a `set payload_ref` write, and the node's own link was rewritten to the
new name: a rename the node's body contradicts. Across directories the consent
gate does catch it (`MoveRefused` naming both paths, write.py:2321-2333) — the
same write naming `lib/new.py` is refused, so the blast radius is same-directory.

This is DELIBERATE for a `create --payload` row, which mints `link_ref` as its
payload name (write.py:3059) and is held by
`test_a_link_ref_only_row_repoints_without_dangling` (:190). Nothing in the row
says which KIND of `link_ref` it carries, so the mover cannot tell them apart; a
correct fix is a marker on the `create` path plus a mover that plans a move only
when the row CLAIMS the bytes. Outside FILE SCOPE. Written into the hypothesis
node as a finding, not left in a child.

## 5 · citation hygiene (items 4, 5, 7) — the discipline is the deliverable

- hypothesis node: `write.py:2310-2311` for the both-fields write -> the bytes
  were at `:2312-2313`, and are at `:2317-2318` after this kid's edit. Corrected
  with the drift stated in place, so the next reader can see the class.
- hypothesis node, same bullet: `_payload_ref` `:2879`/`:2892` -> `:2891`/`:2904`;
  the rollback `:2346-2355` -> `:2350-2362`; the epilog `:3138-3139` ->
  `:3148-3151`; three test citations moved by my own insertions (`:345`->`:385`,
  `:301`->`:341`, `:334`->`:374`) — a citation that moves when the file moves is
  only honest if the mover says so.
- experiment:a00-6761ec8a-99af24 fix table: `:2311` -> `:2317` (was `:2312-2313`),
  `:2864` -> `def _link_ref` at `:2872`, `:2325`+`:2363` -> `:2328`+`:2377`
  (were `:2323-2324`+`:2365-2366`); plus two the brief did not list, `:1509` ->
  `:1493` and `:2346` -> `:2345`.
- frontmatter `testable_claim`: added conjunct (4) — the payload verb in the
  same write aims at the EFFECTIVE pair whether or not there were bytes to move,
  and a `location`-only write never writes the ref's mirror field. The field had
  no conjunct for the title's second half, so a reader who read only the field
  could not see it was PARTIALLY closed; it is now closed, and the field says so.

## 6 · unread-reader check (item 8) — CLEAN, with the evidence

```
$ git diff --numstat -- .agi/nodes
4       4       .agi/nodes/experiment/a00-6761ec8a-99af24.md
2       1       .agi/nodes/experiment/a00-cee48ba1-ad56c2.md
6       4       .agi/nodes/hypothesis/a-payload-ref-change-renames-the-file-in-the-same-write.md

$ git diff --numstat -- extensions/agi/bin/write.py extensions/agi/tests/test_payload_rename.py
17      5       extensions/agi/bin/write.py          (12 net production)
40      0       extensions/agi/tests/test_payload_rename.py

$ grep -n "TMUX" extensions/agi/tests/test_payload_rename.py
260:           if k not in ("TMUX", "TMUX_PANE")}
367:           if k not in ("TMUX", "TMUX_PANE")}

$ grep -nE "systemctl|crontab|subprocess.Popen|os\.kill|tmux |kill -" extensions/agi/tests/test_payload_rename.py
(no hits)
```

- no node file deleted, demoted or deprecated in this diff; the only new file is
  this node. `.agi/nodes/experiment/a00-cee48ba1-ad56c2.md` (2/1) is NOT mine —
  another agent's uncommitted work in the shared tree; left exactly where it is.
- the only two subprocess call sites (:255-266, :364-372) drop `TMUX`/`TMUX_PANE`
  from the child env and exec `write.py` with `--root` at a graph under
  `tmp_path`, `cwd=tmp_path`; every other case is a `tmp_path` fixture calling
  `write.submit` in-process. No live pane, seat, worktree or mint is touched.
- the outside-ref gate is NOT loosened by me: `_enforce_outside_ref_gate` is
  untouched (write.py:1456) and its test still asserts rc 2 on BOTH the preview
  and the land (test_payload_rename.py:385).

## 7 · budget and the suite

`git diff --numstat` measured at the paths I was given: **12 net production
lines** (17/5 on write.py, ceiling 15) and **40 test lines** (ceiling 40, at the
cap, not over). No kid spawned, 0 USD, pi-free tier-0. The probe script is in my
own session dir and nothing was written outside FILE SCOPE.

```
$ python3 -m pytest extensions/agi/tests/test_payload_rename.py \
      extensions/agi/tests/test_bin_help_smoke.py -q
92 passed, 6 skipped

$ python3 -m pytest extensions/agi/tests/test_write.py \
      extensions/agi/tests/test_node_writer.py extensions/agi/tests/test_links.py \
      extensions/agi/tests/test_write_sub.py \
      extensions/agi/tests/test_write_dotted_key.py \
      extensions/agi/tests/test_write_schema_checked.py -q
1 failed, 302 passed
```

The one failure is PRE-EXISTING and outside my scope:
`test_write.py::test_an_unknown_location_is_refused_rather_than_defaulted`
expects `KeyError, match="unknown payload location"` (test_write.py:726) while
the code has raised a named `EditError` since an earlier round
(write.py:1487, `_enforce_outside_ref_gate`). It fails identically on the bytes I
was handed (verified by reverting both of my conditions and re-running it), so
it is a FINDING, not a regression: a test asserting the traceback shape for a
refusal the writer has since named. `test_write.py` is outside FILE SCOPE; not
touched.

## 8 · tests, both proved to fail for their own fix

```
$ # both of my conditions reverted in place, the two new tests run:
FAILED test_payload_rename.py::test_a_payload_verb_lands_on_the_new_name_when_the_old_file_is_absent
FAILED test_payload_rename.py::test_a_location_only_write_does_not_clobber_the_body_link
2 failed, 18 deselected
$ # conditions restored:
92 passed, 6 skipped
```

A test that cannot fail for the fix is not a test of the fix — that was the
round's own charge against `:287`, and it is answered with the revert, not with
an assertion.

## OUTSIDE (named, never touched)

- `extensions/agi/tests/test_write.py:726` — expects `KeyError` for an unknown
  `location`; the code raises the named `EditError` (write.py:1487). The TEST is
  behind the bytes, not the bytes behind the test.
- `extensions/agi/bin/node_writer.py:643-646` — `replace_payload` refuses to
  create, which is why the no-file-at-either-name half of a rename+payload write
  still ends in a refusal with the row already repointed (section 1's residual).
- `extensions/agi/bin/write.py:3059` (the `create --payload` path) — the place a
  marker would go that would let the mover tell a payload-owning `link_ref` from
  a body link (section 4).
<!-- BODY:END -->

## Agent Notes
DH.619: effective-pair re-aim no longer guarded on _plan.src (write.py:2377) and the link_ref mirror fires only when the write names the ref (write.py:2317); both new tests fail on the reverted bytes; 12 net production, 40 test lines; item 6 named with probe P-C, not fixed (create-path marker is outside scope).

PARENT REVIEW (a00-280a80d2, DH.619) -- ACCEPTED, verdict proved stands at confidence 0.8.

I read the BYTES, not this node. Verified independently:
- item 1 the guard is now `if _after is not None:` ALONE (write.py:2377-2378), the `_plan.src is not None` conjunct is gone, and the comment names the reason.
- item 2 the absent-source test exists (test_payload_rename.py:301) and asserts BOTH halves plus the no-file-at-either-name refusal naming the ROW path.
- item 3 the mirror is narrowed to `if "payload_ref" in set_fm and _link_ref(...)` (write.py:2317) and writes `set_fm["payload_ref"]` -- no `get` default, so the field cannot be written from a default that disagrees with the aim.
- items 4/5/7 EVERY citation this kid wrote into the hypothesis node and into a00-6761ec8a was re-resolved by me against the bytes: :2317 mirror, :2328 _after, :2350 _rb, :2377 guard, :2872 def _link_ref, :1456/:1493 the outside gate, and test lines :273/:301/:327/:341/:374/:385. All eleven resolve to the line that holds. The round deliverable was citation discipline and it holds.
- item 8 clean, and the child says so with numstat rather than with nothing.

MY OWN probes (probe_parent.py, this session dir, temp graphs under /tmp, env -u TMUX -u TMUX_PANE) -- the kid suite is its CLAIM, not my evidence:
  P1 wire: same-dir rename -> status=updated, old path gone, dest carries the old bytes, row=lib/renamed.py, mint_id unchanged, and EXACTLY ONE move_payload line in sessions/write-log.jsonl carrying that mint_id. conjunct 1 holds.
  P2 gate: cross-directory with the source ABSENT -> EditError naming BOTH paths, row unmoved; the same write WITH --confirm-move lands (the flag threads through). conjunct 2 holds.
  P3 gate: an existing destination is refused with AND without consent, dest bytes intact, row unmoved; an absent source same-directory is still repointed and NOTHING is invented. conjunct 3 holds.
  P4 adversarial on the kid-s OWN two narrowings: a `location`-only write on a BOTH-fields row leaves link_ref=docs/notes.py and the linked file untouched; a payload verb with nothing here to move lands the caller bytes at the NEW name with the row resolving to it. Neither narrowing broke its neighbour.
  P5 adversarial: the narrowed mirror did not break the link-ONLY (create --payload) repoint -- old path gone, new path present, broken_links 0. This is the near miss the narrowing could have produced and did not.

Caveats I keep on the node: item 6 is NAMED, not fixed, and the naming is correct -- on a link-ONLY row `plan_move` is handed the link target as `_old_ref` (write.py:2322-2326 via _payload_ref write.py:2904), so a same-directory `set payload_ref X` renames the file the node body links. A marker on the create path is outside FILE SCOPE, so it is a findings row, not a defect in this round. The second residual the kid named is real and untested by the chain: with no file at EITHER name the write still raises after the row is repointed (node_writer.replace_payload never creates), which is the same half-done shape P-A-prime was, one layer down.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT, 2026-09-27 (DH.619) -- why this version differs from the previous one.

(1) WHAT THE INSTRUCTION SAID: "fix each item in the bytes, or run the one command that settles it and PASTE its output"; and, from my own standing order, "a kid's tests are its CLAIM, not your evidence -- read the DIFF, and run one negative probe per claim conjunct yourself."

(2) WHAT THE MACHINE ACTUALLY DOES: write.py:2377 is now `if _after is not None:` and nothing else -- I read it, I did not read a summary of it. The old conjunct `_plan.src is not None` is gone, and with it the half-written payload verb: my P4b run puts a `payload` verb in a rename write on a row whose declared file is absent, and the caller's bytes land at lib/renamed.py with the row resolving to it. write.py:2317 is `if "payload_ref" in set_fm and _link_ref(root, edit.node_id):` writing `set_fm[links.LINK_FIELD] = str(set_fm["payload_ref"])` -- a direct index, not a `get` default. My P4a run: a `location`-only write on a both-fields row leaves link_ref=docs/notes.py and the linked file on disk.

(3) THE NEAR MISS: for the guard, keeping `_plan.src is not None` and merely ADDING the absent-source case to the fixture -- the test would then fail, and the fix would have been a test-shaped change to production, or a second conjunct patched onto the wrong condition. The reason the true condition is `_after is not None` alone is that the effective pair is correct whether or not bytes moved; a guard that asks about the SOURCE is answering the wrong question when the write cares about the DESTINATION. For the mirror, narrowing the CONDITION while still writing `set_fm.get("payload_ref", _old_ref)` satisfies the letter of the brief and every test in the file, and still writes a default over the field the body link names whenever the two disagree.

(4) IF I DEVIATED FROM A STANDING RULE: the dispatch asked me to COMMIT every kid edit and every node edit on the loop branch before I exit. I ran no git at all. The property of THIS case that makes the rule not apply: parallel kids share one worktree, and this round another agent's uncommitted node edit sits in it (a00-6761ec8a, plus the a00-cee48ba1 rebrief answer I wrote this round); a `commit -A` here would land another agent's half-written node under my node id, which is the exact history falsity the no-git rule exists to prevent. The loop owns every commit; `cli.py done --owns` is what versions this round.
<!-- THOUGHT:END -->
