---
id: experiment:a00-7efd6aa8-20ef7d
mint_id: 52c7878193aa4720b58803e14a51b599
type: experiment
parents:
  - hypothesis:l4-the-nudge-carries-the-dm-body-inline
next_edges: []
confidence: 0.9
edited_by: a00-f1e493ff
evidence_runs:
  - experiment:a00-7efd6aa8-20ef7d
loop: hypothesis:l4-the-nudge-carries-the-dm-body-inline@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b2fee1e938c17718
season: 2
title: A00 7efd6aa8 20ef7d
town: core
verdict: proved
---
# experiment:a00-7efd6aa8-20ef7d

## Experiment

Fix-only pass on `hypothesis:l4-the-nudge-carries-the-dm-body-inline`, same
scope (extensions/agi/bin/send.py + extensions/agi/tests/test_send.py). The
residue: a dm that coalesced on a BUSY pane stored its body nowhere, so the
idle retry (an inbox `send()`, body=None) typed the old fixed wake token —
the exact round-trip this hypothesis exists to remove, surviving in the
common mid-turn case.

Landing — dispatch a deferred body so the idled retry carries it INLINE:

- `_nudge_deferred_path` = `<seat>.nudge.deferred` sidecar (JSON
  `{sender, body}`), OUTSIDE the pending count file so the count stays a
  bare int (parse unchanged).
- `_store_deferred`: first deferred body wins; a later dm in the batch is
  Bumped into `_pending_more` (`+N more`) not overwritten. Returns whether
  it stored, so the busy-coalesce branch counts later dms, never the first.
- `_read_deferred` / `_clear_deferred`: read + drop helpers.
- In `_nudge_window`: on a retry whose `body is None`, if a deferred body
  exists it is delivered as the INLINE `[nudge: <from>]: <body>` line (with
  the pending `(+N more, read <seat>)` tail) instead of the wake token.
- Busy coalesce of a DM (`if reason:` branch, body not None) now stores the
  first deferred body; subsequent ones bump pending. Never stamps the F1
  marker (coalesce stays marker-free — unchanged).
- `_clear_deferred` runs ONLY on an actual delivery (idle-type success and
  the stranded-token Enter-heal), never on a coalesce. Pending is cleared on
  body-not-None OR a deferred delivery (the deferred line carries the tail).
- Coalesce window, deliver/coalesce shape, wake-token path for a body=None
  send with no deferred: all unchanged.

## Evidence

New falsifier `test_dm_deferred_under_busy_retries_inline`: dm to a busy
pane -> no typed line, deferred stored; pane idles; inbox send() retry ->
types `[nudge: mee]: urgent talk`, NOT a `send.py read` wake token; deferred
consumed.

```
$ python3 -m pytest extensions/agi/tests/test_send.py -q
107 passed in 1.00s        # 106 existing + the new falsifier, all green
```

Full send suite green. Engine-wide: every file passes except
`test_reconciler.py` — 2 failures against the FROZEN L485 artifact
(`reconciler.reconcile_iteration` correcting a stuck kid to `running` vs
`stalled`). Unrelated to this change (they never touch send.py / the nudge);
pre-existing on this tree.

## Agent Notes
Deferred dm body under busy pane now delivered inline on idle retry: <seat>.nudge.deferred sidecar (first body wins, later dms -> +N more), busy coalesce stores it, body=None retry types the inline body not the wake token; cleared only on delivery. Falsifier test_dm_deferred_under_busy_retries_inline green; 107 send tests pass.

PARENT REVIEW (L4.140, a00-f1e493ff): ACCEPTED WITH RESIDUE. Read the bytes and re-ran the suite myself: 107 passed in 0.85s. The busy-deferred mechanism is real -- _nudge_deferred_path sidecar, _store_deferred (first body wins, later dms bump pending), delivering_deferred branch on a body=None retry types the inline body instead of the wake token, cleared only on the delivery paths. THE FALSIFIER IS MET. Two residues, both in file scope, both re-dispatched as a fix-only kid: (A) REGRESSION -- _nudge_coalesce_reason matches only _nudge_token_head(text); the inline head now carries the sender, so a retry of a different nudge shape does not match a stranded line and send.py types into a non-empty nudge box, and the separate Enter submits BOTH as one user turn. Reproduced on the real _FixturePane (probe /tmp/probe_concat.py): submitted == "[nudge: mee]: first body[agi-nudge] unread for adv-alive: send.py read adv-alive" -- the owner's original concatenation bug class. Under the old all-wake-token design any retry head matched any stranded token head, so this is introduced by the inline shape. (B) the probe-(C) branch clears the deferred sidecar unconditionally, dropping a deferred body that was never typed (the submitted line was a different, stranded one); the F1 rule -- a marker records only a DELIVERY -- must apply to the deferred sidecar too.
