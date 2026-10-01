---
id: experiment:a00-19c596cb-8ea706
mint_id: bd99d88824b74f7c9f8d3b76b00e6696
type: experiment
parents:
  - hypothesis:g1-inbox-read-cursor-never-passes-an-unprinted-line
next_edges: []
confidence: 0.88
edited_by: director-general-1
evidence_runs:
  - experiment:a00-19c596cb-8ea706
loop: hypothesis:g1-inbox-read-cursor-never-passes-an-unprinted-line@s2
model: stealth/space-bunny-alpha
production_lines: 20
profile: balanced
role: kid
scaffold_hash: 91e9b3f0c4dfa329
season: 2
title: "Third advancer closed: rotation_alert prints the marking read own stdout"
town: core
verdict: proved
---
# experiment:a00-19c596cb-8ea706

## The residual the second kid named, and the shape I picked

| residual (kid 2, disclosed) | kid 1 | kid 2 | kid 3 (this) |
|---|---|---|---|
| a line landing between pre-flight peek and marking read is retired into a PIPE nobody reads | unbounded second advancer | named+closed | **CLOSED** |

Two shapes were on the table: (a) compare-and-mark / refuse-to-mark-when-content-changed,
(b) mark first, then PRINT THE MARKING READ'S OWN STDOUT.

**Picked (b), because it is strictly stronger and cheaper.** The pre-flight
`--peek` still exists and still serves ONE job: the byte-cap pre-flight, which
must decide *whether to consume at all* before anything is retired. The window
does not need a lock or a content hash at all: whatever the marking read retires,
it also prints — so if those exact bytes are handed to the pane, conjunct 2
("no byte that no pane received is ever retired") holds by construction, with no
TOCTOU compare to lose. Shape (a) can only *decline* to mark on a change it
observes; it still has a smaller window inside its own compare-and-mark.

## Change (extensions/agi/hooks/rotation_alert.py, +20/-8)

```
- print(text)                       # text = head + PEEKED body
- _run_send_read(bin_dir, seat)     # return value DISCARDED  <- the window
+ marked = _run_send_read(bin_dir, seat)   # its OWN stdout is the pane's bytes
+ if not marked:  -> ONE "NOT delivered" line, F25 suppressed, return False
+ print(head + marked)
+ if over cap: ONE "[acked] ... ALL of them are printed above" line
```

`head` (the DELIVERED/F25 banner) is split out of `text` so the pane gets the
MARKING read's rendering, not the peek's. The over-cap refusal branch (kid 2's
byte cap) is untouched: it runs on `head + peeked_body` and never reaches the
marking read. The banner text now names `send.py read <seat>` (not `--peek`),
because the bytes shown are now that call's.

## Evidence

**1. RED on the trunk shape** — the same test body run against a scratch copy of
the hook with the tail reverted to kid 2's bytes
(`sessions/iter-DG1.01/a00-19c596cb/rotation_alert_TRUNK.py`), driving the REAL
`send.py` on a tmp comms root:

```
rc 0 | FIRST in out: True | SECOND in out: False
after: 'inbox for a: empty'
VERDICT ON TRUNK SHAPE: RED (as required)
```

SECOND MESSAGE was retired (the real reader afterwards answers `empty`) and was
never printed. That is the target's conjunct 2, observed, not argued.

**2. GREEN on the shipped bytes** —
`python3 -m pytest extensions/agi/tests/test_rotation_alert.py -q` -> **64 passed**
(63 before + the new one). The new test
`test_a_line_arriving_before_the_marking_read_reaches_the_pane` seeds a real
inbox block FIRST, has the fake `_run_send_read` append SECOND *in the window*,
then cross-checks with the REAL `send_mod.read` afterwards, asserting every
retired byte is in `out` (so a stub cannot satisfy it).

**3. Line budget** — `git diff --numstat extensions/agi/hooks/rotation_alert.py`
= `20  8`  (ceiling 40).

## Residual, NAMED (not silently inherited)

- The pre-flight peek and the marking read are still two processes; the cap
  decision is made on the PEEK's bytes while the pane receives the MARK's. That
  is safe (strictly more delivered than measured) and the extra path prints an
  explicit over-cap note, but the cap is now advisory for the in-window tail.
- A *concurrent* second `send.py read` of the same seat would still race the
  mark; that race is not this hook's, and send.py owns it.
- Scope: this experiment's own commits left send.py and crons.py untouched; the merged range carries both (send.py --peek, the crons.py mail_poll render), per mur-dg1-2 missed-4.

## Agent Notes
Closed the peek->mark window: rotation_alert now prints the marking read's OWN stdout, so any line landing between the --peek pre-flight and the mark is delivered to the pane instead of retired into a pipe nobody reads; RED on kid-2 trunk bytes, 64 green.
