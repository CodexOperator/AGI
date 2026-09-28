---
id: experiment:a00-a46d3b83-8fc296
mint_id: c4f50cb92c1b459dbb76059b157e5fe9
type: experiment
parents:
  - hypothesis:send-read-prints-every-unread-block-and-every-dm-send-nudges
next_edges: []
confidence: 0.85
edited_by: a00-16f0ec5d
evidence_runs:
  - experiment:a00-a46d3b83-8fc296
  - experiment:a00-db001065-4d153e
loop: hypothesis:send-read-prints-every-unread-block-and-every-dm-send-nudges@s2
model: stealth/space-bunny-alpha
probes:
  - "PARENT (a00-16f0ec5d) GATE conjunct 1: TWO consecutive partial reads (printer walks block 0 only), then a full read -> after every rewrite the file ends in exactly ONE trailing newline and body-B/body-C still sit BEHIND the read marker; PASS. The kid test only ever does ONE partial read. Probe script: sessions/iter-DH.524/a00-16f0ec5d/parent_probes.py, tmp roots, no live pane."
  - "PARENT (a00-16f0ec5d) AUTH conjunct 2: a dm send to a seat with NO seats row at all (a target the claim never authorises) -> send_dm does not raise, nothing is typed, pending=1 is registered for that unknown seat; status prints marker=none pending=1 in_mode=no-target. The pending mark is NOT restricted to seats the graph knows: an unlisted recipient accrues a sidecar. Recorded, not fatal: the send itself was accepted, so the count matches an accepted block."
  - "PARENT (a00-16f0ec5d) WIRE conjunct 2: the real CLI main([... send --to thought-master TEXT]) reaches the changed send_dm bytes live -> rc=0, the body is in the dm file, and status shows pending=1 BEFORE any read; the same no-pane fixture through an INBOX send still shows pending=0. That asymmetry is the open residue: the inbox path carries the same hole and was explicitly outside this slice. PASS on the claimed conjunct."
  - "PARENT (a00-16f0ec5d) VERDICT: ACCEPTED. Deliverables checked against the BYTES (diff 5cf6b511e..worktree), not the node text: all three named deliverables present -- the marker write at send.py:3922-3933, the send_dm pending mark at send.py:4026-4042, and the db001065 frontmatter now reads inconclusive_lean_disproved:55 / 0.55 via write.py. Ceiling holds: 9 production code lines, 52 test lines, 1 kid, 0 USD. Title is the own words of the kid. One claim beyond the bytes: production_lines 21/2 from git diff --numstat counts COMMENT lines; the code lines are 9."
production_lines: 21
profile: balanced
role: kid
scaffold_hash: 680463a42bc4ff0d
season: 2
title: "DH.524 corrective: read-marker newline kept, dm send registers pending, db001065 demoted"
town: core
verdict: proved
---
# DH.524 corrective slice (kid a00-a46d3b83) — 3 jobs, all landed

Scope: the read-marker rewrite, the dm-file send's pending mark, the
`a00-db001065-4d153e` frontmatter/body contradiction. Base bytes as handed.

## 1 · read marker no longer de-newlines the file (send.py:3925)

Pre-fix write:

```python
inbox.write_text(content[:cut].rstrip("\n") + "\n" + READ_MARKER
                 + content[cut:].lstrip("\n"))
```

`content[cut:].lstrip("\n")` is the UNREAD TAIL, and nothing puts a newline
back: with `cut < len(content)` the rewritten file no longer ends in the
single trailing newline the writer gave it, so the next `send` append fuses
onto the last body line. Post-fix:

```python
tail = content[cut:].lstrip("\n")
if tail and not tail.endswith("\n"):
    tail += "\n"
inbox.write_text(content[:cut].rstrip("\n") + "\n" + READ_MARKER + tail)
```

`tail` non-empty is the ONLY new case (a fully-consumed read keeps the old
bytes exactly), so the marker index space and the one-index-space `cut` are
untouched.

## 2 · TMM.283 — a dm-FILE send registers pending (send.py send_dm)

A `--to` dm whose nudge never resolved (no pane target) left NO mark: the
block sat in the dm file while `send.py status` read `pending=0` until someone
read. The mark belongs to the SENDER, so it is made there:

```python
before = _pending_more(root, other)
ok = _nudge_window(root, other, ...)
if not ok and not _row_is_quiet(root, other) \
        and not _read_deferred(root, other) \
        and _pending_more(root, other) == before:
    _bump_pending(root, other)
```

The three guards are each a measurement, not a guess:
- `not ok` — a typed nudge IS the delivery; no pending owed.
- `not _row_is_quiet` — a quiet row types nothing by choice (it still writes
  the file); counting it would invent a pending it never owed.
- `not _read_deferred` — a busy pane stores the deferred body instead of
  counting it, so bumping too would double-count one dm. Found by a RED:
  without this guard `test_dm_deferred_under_busy_retries_inline` grew
  `(+1 more, ...)` on a dm that was already deferred.
- the count comparison — a window coalesce bumps the counter itself.

## 3 · experiment:a00-db001065-4d153e — frontmatter aligned with its body

`set verdict inconclusive_lean_disproved:55` + `set confidence 0.55` via
`write.py` only (the body's own PARENT DEMOTION on probe P3; the frontmatter
still read `proved` / `0.9`).

## Evidence — RED first, then GREEN

| test | pre-fix bytes | post-fix |
| --- | --- | --- |
| `test_partial_read_keeps_the_unread_tail_and_the_trailing_newline` | FAIL (`after` ends with no newline) | pass |
| `test_dm_send_registers_pending_when_no_pane_ever_nudged` | FAIL (`pending=0`) | pass |

RED shown by reverting each hunk in the checkout (scratch copy under this
session dir), not by argument.

Neighbourhood, post-fix:
`test_send.py test_seatsig.py test_sensei.py test_heal.py
test_bin_help_smoke.py test_write_self_row.py` → **468 passed, 6 skipped**;
`test_send_nudge_classes.py test_send_quiet.py test_send_rewind.py
test_send_undelivered.py` → **36 passed**.

Production lines (`git diff --numstat`, read-only): `send.py` **21 / 2**.
Test lines added: 55.
Raw output, screenshots, logs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-16f0ec5d, DH.524) — ACCEPTED, one open residue. (1) WHAT THE ORDERS SAID, quoted: "send.py:3925 -- when cut < len(content) the marker write ... drops the file trailing newline -> keep it byte-exact; one test: a partial read leaves unread blocks behind the marker AND the file still ends in exactly one newline", "TMM.283 ... dm-FILE sends ... never registered pending -- the SENDER skipped the pending mark ... one test: a --to dm-file send registers pending for its recipient", "experiment:a00-db001065-4d153e frontmatter says verdict proved / confidence 0.9 while its body PARENT DEMOTION demotes it -> set both fields to what the demotion says (write.py only)", "FILE SCOPE extensions/agi/bin/send.py (the read-marker write + the dm-file sends pending mark only)", "CEILING net <= 12 production lines / <= 60 test lines / HARD CAP 1 kid". (2) WHAT THE MACHINE ACTUALLY DOES, cited to the BYTES I diffed (5cf6b511e..worktree), not to the node text: send.py:3925-3933 adds tail = content[cut:].lstrip("\n"); if tail and not tail.endswith("\n"): tail += "\n" -- 3 code lines, the newline returns only when the unread tail is non-empty, so a fully consumed read keeps its exact old bytes. send.py:4029-4042 adds root/before plus a four-condition guard around _bump_pending -- 6 code lines. 9 code lines total against a cap of 12; test_send.py gains 52 lines against 60. The third deliverable is a 2-line frontmatter change on db001065 (proved/0.9 -> inconclusive_lean_disproved:55/0.55) made through write.py, edited_by a00-a46d3b83. My own probes, built and run: P1 gate -- two consecutive partial reads then a full read, every rewrite ends in exactly one trailing newline with body-B and body-C still behind the marker: PASS (the kid test does only ONE partial read, so the second rewrite and the full-read path are new coverage from me, and both hold). P2 auth -- a dm send to a seat with no seats row: no raise, nothing typed, pending=1 registered for a seat the graph does not know. P3 wire -- the real CLI main([... send --to thought-master TEXT]) reaches the changed send_dm bytes live: rc=0, body in the dm file, status pending=1 before any read. (3) THE NEAR MISS -- and it is the one the fix just created, not the one it removed. The claimed invariant is that a dm send registers pending LIKE an inbox send. P3 measures both halves in one fixture: the dm path now reports pending=1 and the INBOX path in the same no-pane fixture still reports pending=0, which I reproduced standalone. A fix that patches only the dm branch satisfies every fixture the kid wrote -- each of them sends a dm and never an inbox send to the same unreachable recipient -- and loses the invariant the target actually claims, because the hole was never dm-specific. The same near miss made the byte-exactness claim nearly false: a fix that unconditionally appends "\n" to the tail would pass the kid test and would ADD a newline to a file whose final line carries a bare CR, which is exactly the byte the newline="" read at :3894 exists to preserve. The kid guarded it with "tail and", which is right. (4) DEVIATION: none from the standing rules -- I ran no git, authored no node of my own, and the accepted verdict is the kid own claim, not mine. RESIDUE, recorded not ridden: (a) the inbox send to a no-pane seat still registers no pending, one line of scope wider than this slice was allowed to reach; (b) _bump_pending accrues a sidecar for a seat the graph never listed; (c) the node reports production_lines 21/2 from --numstat, which counts the comment lines this fix spends as much prose on as code. None of the three is a falsification of the claim -- each survives the probes -- so the node is accepted and (a) is the next round target.
<!-- THOUGHT:END -->

## Agent Notes
read-marker rewrite keeps exactly one trailing newline on a partial read; a --to dm send with no resolvable pane now registers pending (guards: quiet row, already-deferred body, count-unchanged); db001065 frontmatter demoted to its body's inconclusive_lean_disproved:55/0.55. RED-first both fixes; 468+36 neighbourhood green.

PARENT ACCEPT (a00-16f0ec5d, DH.524): 1 kid (a00-a46d3b83), 1 owned, 0 demoted, 0 failed. All three named deliverables are in the diff and every one of my three probes passes the claimed conjunct. The open residue is the INBOX half of TMM.283: an inbox send to a seat with no resolvable pane still leaves pending=0, measured in the same fixture where the dm send now leaves pending=1. That is the next round, not a demotion here.
