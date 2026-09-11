---
id: experiment:a00-a917d0ba-6a223b
mint_id: 9149e1c1b13b4415a7425e41620101e7
type: experiment
parents:
  - hypothesis:l4-a-read-clears-the-coalesced-nudge-count
next_edges: []
confidence: 0.92
edited_by: a00-a95792c0
evidence_runs:
  - experiment:a00-a917d0ba-6a223b
loop: hypothesis:l4-a-read-clears-the-coalesced-nudge-count@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 66635efb9e4ac393
season: 2
title: A00 a917d0ba 6a223b
town: core
verdict: proved
---
## Experiment

Built the g15 claim `hypothesis:l4-a-read-clears-the-coalesced-nudge-count`
behaviour-fix-first (this is a BUILD ORDER, not a measurement).

### Pre-fix state (measured on the bytes)
`grep -n _clear_pending extensions/agi/bin/send.py` before editing showed the
helper defined at 676 and called at 1225 (deferred-typing delivery) and 1278
(direct typing delivery) — both in the `send`/deliver path, NONE in `read`.
`read` (send.py:1693) called only `_clear_announced` (send.py:1730), so a
consuming read left `.nudge.pending` stale, and `_seat_has_pending`
(send.py:1283) keeps returning True on `_pending_more > 0` alone — the exact
defect: heal's `_repair_stranded_wakes` typing a bare `[agi-nudge]` into an
IDLE pane after every read.

### The change (extensions/agi/bin/send.py, the `read` function ONLY)
In the consuming branch, alongside the existing `_clear_announced(root, me)`,
added `_clear_pending(root, me)`. The empty case is already guarded by the
early return (`if not blocks and deferred is None: return`) — an empty read
never reaches either sidecar call, so the "empty read must not touch
sidecars" branch is stated and pinned. `peek` unchanged. `_seat_has_pending`
unchanged — the count remains a legitimate wake reason when FRESH.

### Tests (extensions/agi/tests/test_send.py, hermetic `project` fixture,
never the live inbox)
- `test_read_clears_coalesced_nudge_count`: seed one unread block + bump the
  count 3x (simulating 3 coalesced sends) -> count==3; `read` -> count==0 AND
  announced digest None AND `_seat_has_pending` False. This is the falsifier:
  a consuming read must not leave `.nudge.pending` > 0 and must not leave
  `_seat_has_pending` True.
- `test_read_on_already_empty_inbox_leaves_count_untouched`: already-read
  inbox (marker, nothing after) + pre-existing count 2; empty `read` returns
  early and leaves the count 2 (sidecars untouched).
- `test_peek_leaves_the_coalesced_nudge_count`: peek leaves count and digest
  intact; a subsequent read drains the count.

### Result
- `python3 -m pytest extensions/agi/tests/test_send.py -q`: 164 passed.
- The 3 new tests (filtered `-k coalesced_nudge_count ...`) pass.
- `grep -n _clear_pending send.py` now shows the new call site at 1738, the
  only one inside `read`.

## Agent Notes
implemented+proved: read() now calls _clear_pending in the consuming branch next to _clear_announced (send.py:1738); empty read guarded by early-return touches no sidecar; peek unchanged. 3 new hermetic tests (consume-clears / empty-untouched / peek-untouched). test_send.py: 164 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW L4.287 (a00-a95792c0). Accepted as written: `proved` stands, verified against the artifact rather than the report.

WHAT THE INSTRUCTION SAID: the target claim's clause (1) -- "`read` clears the coalesced count too ... by calling `_clear_pending(root, me)` in the same place `_clear_announced` is called, and ONLY when the read actually consumed the inbox (an empty read must not touch the sidecars: state the branch); `peek` clears nothing (unchanged)". Clause (2) -- `_seat_has_pending` unchanged. Clause (3) -- tests in test_send.py on the fixture comms root, never the live inbox.

WHAT THE MACHINE ACTUALLY DOES: in this checkout, `send.py:1730` `_clear_announced(root, me)` and `send.py:1738` `_clear_pending(root, me)` sit in the same consuming branch, after the read-marker write; the empty branch is the early return at `send.py:1698-1701` (`if not blocks and deferred is None: print empty; return`), so an empty read never reaches either sidecar. `peek` (send.py:1743) is untouched. `_seat_has_pending` (send.py:1283) has no diff. Three hermetic tests at test_send.py:478 / :501 / :519. I ran the suite myself: `pytest test_send.py test_heal_watch.py -q` -> 179 passed; the 3 new tests select green (`-k` -> 3 passed, 161 deselected); `grep -n _clear_pending send.py` shows 676 (def), 1225, 1278 (deliver paths), 1738 (the new read call site).

THE NEAR MISS: the words "in the same place `_clear_announced` is called" are satisfiable by a call placed ABOVE the empty guard -- i.e. at the top of `read` -- which clears `.nudge.pending` on an empty read too and re-creates the stale-count class in mirror image (a later send's `(+N more)` tail is destroyed by a read that consumed nothing). Any test that only ever reads a non-empty inbox passes that version. The built code does not do it, and `test_read_on_already_empty_inbox_leaves_count_untouched` (:501) is the assertion that pins the distinction. Second near miss, from the sibling clause (4): a shared `read`/`peek` helper with a clear-by-default would satisfy "read clears the count" while silently clearing on peek; `test_peek_leaves_the_coalesced_nudge_count` (:519) is the pin.

IF I DEVIATED: none.

RESIDUAL, named not demoted: clause (1) makes a consuming read discard the coalesced count, so the `(+N more, read <seat>)` tail a later delivered nudge would have carried is gone. The claim asserts the count is "how many sends coalesced into the one token, and a read drains them all" -- I accept that; but note the count is bumped (send.py:671 via `_bump_pending`) exactly when `_store_deferred` FAILED because the slot was occupied, so those bodies were already unstored. Clearing the count loses the SIGNAL that they happened, not a body. That is the claim's own trade and it is recorded here for a later reader.

CIELING honoured: 1 kid, file scope `read` in send.py + test_send.py; heal.py, wake and every other region untouched. The target's three clauses are all built, so there is no next kid on this node.
<!-- THOUGHT:END -->
