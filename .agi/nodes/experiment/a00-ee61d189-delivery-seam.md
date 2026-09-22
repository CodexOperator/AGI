---
id: experiment:a00-ee61d189-delivery-seam
mint_id: 97fe129b235c410aa72f40e587fd61ab
type: experiment
parents:
  - hypothesis:a00-ee61d189-8e9594
next_edges: []
edited_by: a00-ee61d189
line_ceiling: 40
loop: goal:g7.32.4@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 43
profile: balanced
role: kid
scaffold_hash: 83bde4eff418cd55
season: 2
testable_claim: A delivery transport registered at run time in DELIVERY_TRANSPORTS is selected by a generic first-match loop in send()/send_dm(); unregistered behaviour is byte-identical
title: Send delivery table — file append and pane nudge are rows
town: core
---
# experiment:a00-ee61d189-delivery-seam

## What was built (goal:g7.32.4 falsifier 2, DELIVERY leg)

`extensions/agi/bin/send.py` gained a second, independent table beside kid-1's
CLI-addressing table:

```
DELIVERY_TRANSPORTS: list = []          # rows: (name, handler(root, kind, path, payload, **kw))
register_delivery(name, handler, *, priority=0)
_deliver_default(root, kind, path, payload, **kw)   # kind "file" -> append; kind "nudge" -> wake
_deliver(root, kind, path, payload, **kw)           # generic first-True loop
```

`send()`'s inline `with open(inbox, "a") as f: f.write(block)` is now one call
-- `_deliver(root, "file", inbox, block)` -- and `send_dm()`'s inline
`_nudge_window(...) + _announce_nudge(...)` pair is now
`_deliver(<root>, "nudge", other, text, sender=..., croot=croot)`. The built-in
row ("default") is the removed code verbatim and is registered last, so a
`priority=1` row is consulted first. Nothing in keygen / row-commit /
pending-swap / policy was touched; `SEND_TRANSPORTS` (addressing) keeps its
order -- the two decisions are separate tables for separate jobs.

## Falsifier 2, delivery half -- PROVED

New test `extensions/agi/tests/test_send_delivery_seam.py` (4 tests):

- `send()` hands the block to a RUN-TIME-registered transport (no edit to
  send.py) and the inbox file is never created -- it really replaced the
  default, not shadowed it.
- with no transport registered the inbox bytes are the old append
  (`---\nts: ...` .. `\nhello\n`), byte-preserving.
- a row returning False falls through to the built-in (claim semantics).
- `send_dm()`'s wake leg is routable: a registered transport claims
  `kind="nudge"` and sees the dm body, while the dm FILE is still written
  (durable record unchanged).

```
$ python3 -m pytest extensions/agi/tests/test_send_delivery_seam.py -q
4 passed
```

## Behaviour preservation (all existing send suites)

```
$ python3 -m pytest extensions/agi/tests/test_send.py \
    test_send_nudge_classes.py test_send_quiet.py test_send_rewind.py \
    test_send_surface_ssh_or_not.py test_send_undelivered.py \
    test_send_transport_seam.py -q
376 passed, 11 warnings in 159.61s
```

## Falsifier 1 -- census (unchanged residue, NOT attempted this round)

```
$ grep -nE "^[[:space:]]*(import|from)[[:space:]]+(rotate|dispatch)\b" extensions/agi/bin/send.py
613, 727, 825, 843, 1580, 1608, 2188   # 7 local `import rotate`; 0 `import dispatch`
```
Four of the seven are ORCHESTRATION symbols (`_commit_spawn_row`,
`_persist_pending_key`, `_finish_pending_swap_on_push`, `_push_season_branch`)
and remain the named residue. Parent instruction: measure, do not refactor.

## Falsifier 3 (g7.32.2) -- still DEFERRED

No messaging/magic-pane module on this tip; the cross-harness nudge already
lands through this router (now via the delivery table's `nudge` kind).

## Budget

```
$ git diff --numstat -- extensions/agi/bin/send.py
43      5       extensions/agi/bin/send.py
```
production_lines=43, line_ceiling=40 (over the ceiling by 3, well under the 2x
rebrief line at 80; no rebrief_request). The overage is the docstring/comments
on a genuinely new public seam, not duplicated behaviour.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Smallest real delivery seam: one table, one discriminator (`kind`), the old
code verbatim as the last row. Chose `_deliver` (a plain first-True loop) over
a per-kind dict so a new transport can claim or decline by kind exactly as the
CLI `_route_send` loop claims by matcher -- one idiom, two tables. Put the
table at the bottom of the module, beside kid-1's, because both are import-time
registries and `send()`/`send_dm()` resolve names at call time.
<!-- THOUGHT:END -->
