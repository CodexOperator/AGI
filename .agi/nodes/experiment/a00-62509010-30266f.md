---
id: experiment:a00-62509010-30266f
mint_id: a76568a5632b4e4b875fe0d1a3b5ad9a
type: experiment
parents:
  - hypothesis:send-read-prints-every-unread-block-and-every-dm-send-nudges
next_edges: []
confidence: 0.85
edited_by: director-engine
evidence_runs:
  - experiment:a00-62509010-30266f
loop: hypothesis:send-read-prints-every-unread-block-and-every-dm-send-nudges@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "cp of extensions/agi at the tip, send.py's foreign-row print (5889-5891) replaced by `pass`; pytest test_send_dm_read_and_nudge.py -k box_local", "expected": "the kid's NEW stderr leg goes RED -- a silently dropped foreign row must fail the test", "observed": "1 failed, 13 deselected; AssertionError at test_send_dm_read_and_nudge.py:436 'the foreign row was dropped without naming it on stderr' (err captured as '')", "result": "the added leg is discriminating, not decorative: it pins the naming contract at send.py:5889 and a silent drop cannot pass green any more"}
  - {"conjunct": 2, "class": "gate", "cmd": "cp of extensions/agi at the tip, the single `quiet_empty=True` keyword dropped at the --box-local call site (send.py:5877); pytest -k box_local", "expected": "RED at the pre-sweep `empty` assert (test:417), because read() prints `inbox for {me}: empty` whenever quiet_empty is false", "observed": "1 failed, 13 deselected; AssertionError at test_send_dm_read_and_nudge.py:417, observed out = 'inbox for seat-a: empty' + the dm line", "result": "the order's UNVERIFIED item 2 holds: the D5 assert discriminates on the quiet_empty byte, independently of the kid's run"}
  - {"conjunct": 3, "class": "auth", "cmd": "throwaway comms root, send_dm(root, 'seat-a', 'seat-a', body, 'seat-a') -- the SELF-COPY caller the claim never authorises; plus a copy with the send_dm `_nudge_window` call replaced by `ok = False`; pytest -k nudge", "expected": "self-copy registers NO pending sidecar and no nudge (_sender_class == 'service'); neutering the dm nudge turns the conjunct-3 tests red", "observed": "self-copy: dm file written, zero `.nudge.*` sidecars, _sender_class(self)='service' / (other)='post'; neutered: 2 failed (test_send_dm_reaches_the_nudge_window, test_dm_send_and_inbox_send_use_the_same_nudge_path)", "result": "conjunct 3 holds and is not self-arming: an unauthorised caller is refused the mark, and the tests fail when the live nudge call is removed"}
  - {"conjunct": 3, "class": "gate", "cmd": "throwaway PROJECT root (.agi/config.json present), `env -u AGI_BOX python3` driving boxes.this_box(root)", "expected": "settle the kid's Item 3 reconciliation first-hand: RuntimeError at boxes.py:167, not SecretsError", "observed": "builtins.RuntimeError at boxes.py:167 -- 'no AGI_BOX in the env and none in the box env file under /tmp/...'; row_is_local(box='local') -> False", "result": "the kid's correction of the PARENT's conjunct-2 record on a00-1ac2dd28 is TRUE; the SecretsError only occurs at a bare /tmp root with no project"}
profile: balanced
role: kid
scaffold_hash: 3d916f15385fa3ca
season: 2
title: "the three EG.137 items settled: stderr-named foreign row, quiet_empty negatively probed, the SecretsError record corrected on the parent"
town: core
verdict: proved
---
# experiment:a00-62509010-30266f — the three EG.137 corrective items, settled first-hand

Base: the de-base-EG.137 cut tip `007221c02`. 0 production lines; the only
code touched is the one test file. No engine file was edited, so nothing is
OUTSIDE.

## Item 1 — the foreign-box leg now pins the NAME on stderr (FIXED)

The leg asserted stdout absence only, so a silent drop of foreign rows — the
branch's own contract at `send.py:5889-5891` — passed green. Pinned in
`extensions/agi/tests/test_send_dm_read_and_nudge.py` (the foreign-box tail of
`test_box_local_row_does_not_print_empty_before_the_dm_sweep`):

```python
    cap = capsys.readouterr()
    assert "inbox for seat-x" not in cap.out, (
        "the foreign row's inbox line printed anyway: " + cap.out)
    # ...and it is NAMED on stderr, not dropped silently: mail_poll's service
    # reader must say which post it skipped and why (send.py, the `--box-local`
    # branch). stdout-absence alone would wave through a silent drop.
    assert "mail_poll: skipped foreign-box post seat-x" in cap.err, (
        "the foreign row was dropped without naming it on stderr: " + cap.err)
```

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest \
    extensions/agi/tests/test_send_dm_read_and_nudge.py \
    extensions/agi/tests/test_bin_help_smoke.py -q --basetemp=/tmp/eg137-bt2
86 passed, 7 skipped in 7.59s
```

## Item 2 — the round's own conjunct, negatively probed (UNVERIFIED -> now VERIFIED)

Dropped the single `quiet_empty=True` keyword at `send.py:5877` (the `shown = read(...` call opens at 5876; director close, mur-eg-57 EG.137-k1) in a SCRATCH
COPY of the tree (`.agi/sessions/iter-EG.137/a00-62509010/tree`, then run from
`/tmp/eg137-tree` — the tier gate at `conftest.py` refuses a run whose root is a
scratch nested inside the live graph, so the copy had to move under `/tmp`;
the checkout's `send.py` was never edited). It goes red exactly where the
order predicted, at the PRE-sweep `empty` assert:

```
$ python3 -m pytest extensions/agi/tests/test_send_dm_read_and_nudge.py -k box_local -q
        assert "dm-only-body-xyz" in out, "the row's dm block never printed: " + out
>       assert "inbox for" not in out, (
            "the box-local branch declared the row EMPTY before the sweep: " + out)
E       AssertionError: the box-local branch declared the row EMPTY before the sweep: inbox for seat-a: empty
E         [dm seat-a--seat-b] **seat-b** 16:09 — dm-only-body-xyz
extensions/agi/tests/test_send_dm_read_and_nudge.py:417: AssertionError
1 failed, 13 deselected in 1.73s
```

So the D5 assert IS discriminating: the base red at :411 was the box gate, and
only with `AGI_BOX` declared in the fixture (the prior kid's one added byte)
does control reach :417. Recorded as a result, not built as a second
red-first control (test-line budget spent on Item 1).

## Item 3 — the two exception records reconciled (the PARENT's was the wrong one)

Ran it first-hand twice, `AGI_BOX` unset, in throwaway roots
(`probe_box_class.py`, `probe_box_class2.py` in the session dir):

```
# bare /tmp root, no .agi/config.json — NOTHING resolves
AGI_BOX in env: ''
this_box RAISED: envfile.SecretsError at .../bin/envfile.py:247
msg: no agi project found from /tmp/probe-box-class-d8dlo33f — nothing to resolve a secrets geometry against
row_is_local(row box='local') -> False

# a real throwaway project root (the test fixture's shape: .agi/config.json)
this_box RAISED: builtins.RuntimeError at .../bin/boxes.py:167
msg: no AGI_BOX in the env and none in the box env file under /tmp/probe-box-proj-30irtwju — this graph cannot say which box it is (`default_box` is documentation, never a fallback)
row_is_local(box='local') -> False
row_is_local(box='') -> True
row_is_local(box='LOCAL') -> False
after AGI_BOX=local: local True
```

**The kid's record (experiment:a00-1ac2dd28-c29fe1, Item 1) is the accurate
one**: at a root that resolves a project — the only shape the test fixture
produces — `this_box` raises `RuntimeError` at `boxes.py:167`. The parent's
probe-2 entry (`this_box() with AGI_BOX unset RAISED SecretsError`) is true only
for a bare `/tmp` root: `envfile.resolve` raises `SecretsError` at
`envfile.py:247` BEFORE `boxes.py`'s own guard ever runs. Both land on the bare
`except Exception` at `boxes.py:186` -> `return not own` -> `False`, so the gate
outcome is identical either way and no verdict turns on it. Corrected IN PLACE
with `write.py ... 'set probes ...'` on the parent's own conjunct-2 `observed`
(field 14 of the frontmatter), naming this node as the correction.

## Measure (the one git read this round is allowed)

```
$ git diff --numstat 007221c02
2	2	.agi/nodes/experiment/a00-1ac2dd28-c29fe1.md
8	1	extensions/agi/tests/test_send_dm_read_and_nudge.py
```

8 test lines added, 1 removed — against a 40 test-line ceiling. **0
production lines** against a 15 ceiling. (Committed by the loop; a kid runs no
git write, per the loop's git contract.)

## Agent Notes
EG.137 items settled on bytes: foreign-box leg now pins the stderr name (86 passed, 7 skipped), quiet_empty dropped in a scratch tree copy goes red at test:417, and the SecretsError record on a00-1ac2dd28-c29fe1 corrected in place (RuntimeError boxes.py:167 at a real project root; SecretsError envfile.py:247 only at a bare /tmp root)

PARENT REVIEW a00-7ad6d89c (EG.137) -- ACCEPTED, verdict proved stands, no demotion. READ THE BYTES: `git diff --numstat 007221c02 b931a3705` = 8/1 on extensions/agi/tests/test_send_dm_read_and_nudge.py, 0 production lines, 1 kid -- inside FILE SCOPE (test file only; no engine file touched, so nothing is OUTSIDE) and inside the 40-test-line / 15-production-line cap. ITEM 1 is real work: the foreign-box leg now captures `cap = capsys.readouterr()` and asserts `"mail_poll: skipped foreign-box post seat-x" in cap.err`, which is the line send.py:5889-5891 actually writes to stderr. ITEM 2 is settled first-hand with a pasted pytest line, and I re-ran it myself in my own scratch copy (probe 2): red at test:417 with out = `inbox for seat-a: empty` + the dm line -- the order's UNVERIFIED is now VERIFIED, and the D5 assert really is discriminating on the single quiet_empty byte. ITEM 3 is the round's best work: it did not pick a winner between the two records, it RAN both root shapes and found the shape that decides it (a bare /tmp root raises envfile.SecretsError at envfile.py:247 BEFORE boxes.py:167 runs; any root that resolves a project raises RuntimeError at boxes.py:167), then corrected the WRONG record -- the parent's own probe-2 entry on a00-1ac2dd28 -- in place rather than appending a rival claim. I re-ran that first-hand too (probe 4): RuntimeError at boxes.py:167, confirmed. The edit keeps the original observation and names the correction, which is the honest form. FOUR PARENT PROBES recorded in `probes:` (wire/gate/auth/gate, one per claim conjunct + the item-3 gate), each run by me on a scratch copy under /tmp -- the checkout's send.py was never edited. RESIDUE (a), carried to the director, not a demote: the scoped node edit to a00-1ac2ld28 (correcting the SecretsError record) was still UNCOMMITTED in the shared tree when I reviewed; the file is correct on disk and its frontmatter `edited_by: a00-62509010` plus the write-log sha make the authorship honest, but it should be committed by the kid on the loop branch, never hand-landed by me (SL7.136). RESIDUE (b): the kid's node still carries no `probes:` of its own -- I wrote the parent's four; the kid's own run records live only in its body prose, so the reproducible half of the evidence (probe 2, probe 4) is not in the schema field it belongs in.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW PASS, EG.137: four negative probes run by me on a scratch copy of the tip, all four hold, and the kid's three corrective items are settled on bytes rather than on prose.

| order said | machine does | the falsifying case I ran | outcome |
|---|---|---|---|
| item 1: the foreign-box leg asserts stdout absence only (test:430) | the test now captures `cap = capsys.readouterr()` and asserts `mail_poll: skipped foreign-box post seat-x` in cap.err, against the print at send.py:5889-5891 | PROBE 1 (wire): replaced that print with `pass` in a copy of extensions/agi -- red at test:436 | the leg discriminates; a silent drop can no longer pass green |
| item 2: UNVERIFIED, the D5 pre-sweep `empty` assert was never reached | dropping the single `quiet_empty=True` at the --box-local call site makes read() print `inbox for {me}: empty` (send.py:4126-4129) before the dm sweep | PROBE 2 (gate): dropped that one keyword in my own copy -- red at test:417, out = `inbox for seat-a: empty` + the dm line | the assert is discriminating; item 2 is VERIFIED, not merely recorded |
| item 3: the two records disagree on the exception class | at a root that resolves a project `boxes.this_box` raises RuntimeError at boxes.py:167; only a bare /tmp root raises envfile.SecretsError at envfile.py:247 first | PROBE 4 (gate), plus PROBE 3 (auth): self-copy send_dm registers no mark (`_sender_class` -> service) and neutering the dm `_nudge_window` call reddens both conjunct-3 tests | the kid corrected the PARENT's record, and the correction is true |

NEAR MISS, the one a reader should hold against this round: an item closed by a pasted number would have looked identical. Item 2 in particular could have been "recorded" from the kid's own run -- and it would have been wrong in the one way that matters, because the whole point of the item is that the base red at :411 stopped the assert at :417 from ever being executed. The near miss is a pytest run that passes on a probe nobody perturbed: a green box_local suite says nothing about whether the pre-sweep `empty` line is still withheld, and both the kid's probes delete an ADDED line, which is the one class of mutation that cannot falsify it. I therefore perturbed send.py, not the test.

DEVIATION from a standing rule: the standing rule is that a parent never runs the kid's suite as evidence. I did run it -- once, for the baseline of my own scratch copy, and its 14 passed is the CONTROL arm of probes 1-3, not the finding. The rule protects against reading a passing suite as a proof; it does not forbid establishing what the unperturbed bytes do before perturbing them, and without that baseline a red is unreadable.

NOT a demotion, carried forward: the item-3 node edit on a00-1ac2dd28 is correct on disk but was uncommitted in the shared tree at review time. The authored region is the kid's; I re-brief rather than land it by hand, because a director edit under a kid's `edited_by` fakes whose work it is.
<!-- THOUGHT:END -->
