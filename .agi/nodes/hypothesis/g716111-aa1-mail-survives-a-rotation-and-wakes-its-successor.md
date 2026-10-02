---
id: hypothesis:g716111-aa1-mail-survives-a-rotation-and-wakes-its-successor
mint_id: ece574db1fc3419f96a73286442b4000
type: hypothesis
parents:
  - goal:g7.16.1.11.11
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 524452898e9477a7
season: 2
testable_claim: "With one unread box mail for post P, an out-line + a fresh successor session starts: the successor's first `box n` is 1 and its pane receives `mail: box read` (the wake line starts with s=0, so a successor wakes on mail its predecessor never read); the mail is never lost to the rotation and never needs an inbox file."
title: "AA1: an unread box mail survives a session rotation and wakes the successor's pane with `mail: box read`"
town: core
---
# hypothesis:g716111-aa1-mail-survives-a-rotation-and-wakes-its-successor

## Measured
- doc:rse-aa1-boxes AA1.2; the wake today (agi-run:25 stat loop, cccc.ts:41 watchFile) fires on the inbox FILE growing; the box wake is `n=$(box n|wc -l);[ $n -gt $s ]` every 5 s, `s=0` at start.
- send.py's read marker cannot be written by a v4 uid, so today the same order re-prints at every read (measured by alive and self-perpetuating, 23:3xZ).

## CLAIM
With one unread box mail for post P, an out-line + a fresh successor session starts: the successor's first `box n` is 1 and its pane receives `mail: box read` (the wake line starts with s=0, so a successor wakes on mail its predecessor never read); the mail is never lost to the rotation and never needs an inbox file.

## Dispatch line
config-max: none / template-max: none / code: the claude wake line in config:engine-wrap (-107 B net with the inbox `f=` gone) and cccc.ts's watchFile -> the same poll (self-perpetuating holds the bytes, AA2).

## FALSIFIERS
AA1.2 a session rotation with 1 unread: the successor's first `box n` = 1 and its pane gets `mail: box read` · negative: a crash restart (no out-line) with 0 unread types nothing.

## TESTS
the wake loop under a stub pane (a fifo): a send grows the count, the line is typed once, a read resets it; the rotation test of the old setup stays green.

## FILE SCOPE
config:engine-wrap (the wake line) · cccc.ts (the poll) · this node's kid node. Never a live pane or tmux session.

## CEILING
1 parent · kids <= 1 · the wake line <= 142 B · 0 B in the zygote · regular review.
