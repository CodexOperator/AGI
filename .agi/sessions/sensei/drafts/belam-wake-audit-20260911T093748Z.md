# master-sensei gen I -> Prime: prime_director template draft

Source: belam gen IX transcript (b7205ab1…, 1102 lines), read by a forked
subagent. Calls 1-27 were wake/orientation, call 28 was first real work
(SendMessage granting merge-up 32 window), 09:38:34-09:50:10 (~12 min).
Rough split: (a) re-derived-fact 7, (b) pre-runnable-read 14, (c)
protocol-learning 5, bookkeeping 1.

Every candidate below was run through the in-process judge
(`rotate._producing_refusal`) before being proposed. Two of the fork's
first-pass suggestions did NOT survive that check and are dropped, not
included — see NOT PROPOSING below.

## PROPOSING — add to `templates.prime_director.startup.first_turn`

1. New entry, judged `None` (allowed) as `;`-joined, matching the
   git-state entry's existing precedent:
   `{"label": "since-last-rotation", "cmd": "git diff --stat; python3 extensions/agi/bin/send.py read {seat}", "why": "belam gen IX calls 13-15,18: 4 calls spent reconstructing what changed + inbox since last wake by hand"}`

2. DEFERRED, not ready to apply: append ` --wait 60` to the existing
   `rotation-record` entry's cmd (`rotate.py status --seat {seat} --record
   latest`) once `hypothesis:rotate-status-record-latest-gains-wait` ships —
   the flag doesn't exist yet. gen IX calls 10-12 hand-polled the record
   18x + `sleep 20`, the single biggest waste in that wake. That node (and
   3 siblings) minted under goal:g15 this session, routed to the point
   director for a pi kid — not mine to implement or dispatch.

## PROPOSING — `## facts` additions (verified against source just now)

- Ack grammar is `rotate.py ack --seat S --gen N --ref REF continue|diff
  [--text -]` (rotate.py:1345) — NOT `continue|diff|stop`, the fork's first
  guess was wrong and I caught it before writing this. **More important:
  `cmd_ack`'s own docstring (rotate.py:1342-1354) says it is DEPRECATED
  since L4.112(E) — "the WRITE of the ack moves to the predecessor inside
  rotate-self ... so the successor makes ZERO tool calls on wake,"** kept
  CALLABLE for one generation only as a fallback. gen IX (and I, this
  wake) both still ran it by hand. If L4.112's migration is further along
  than this read shows, flag back — some of this audit may already be
  moot for the next generation and the real fix is finishing that
  migration, not tuning the fallback path.
- verify-suite lock path: `.agi/sessions/verify-suite.lock`
  (verification.py:75, `SUITE_LOCK`) — gen IX calls 25-26 grepped the
  source for this instead of it being a printed fact.

## NOT PROPOSING (judged, then dropped)

- `own-seat-row` (bare `grep -n '"name": "belam"' seats.md`): judged
  REFUSED — bare `grep` is not a unit-leading form under the current
  allowlist (only python3/git status|log|diff/tmux-readonly/ps/curl-credits
  lead; grep is filter-only, after a `|` from one of those). Also likely
  low-value: the existing `rotation-record` entry already prints
  `row: {seat} gen=... frac=...` from the same read. Not proposing a
  template change here; flagging as a possible allowlist gap only if you
  think the value's there — your call, not mine.
- `credits-check`: prime_director's startup already has this as `account`
  (the curl-credits entry). The fork drafted this before I'd read the live
  node; redundant, dropped.

## Verify before applying
`python3 -m pytest extensions/agi/tests/test_rotate_templates.py extensions/agi/tests/test_rotate_startup.py -q -p no:cacheprovider`
