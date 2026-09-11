---
id: hypothesis:l4-the-pin-is-the-lease
mint_id: 5c91fdf708314f068411f13d0dba9dd0
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L4-VII
scaffold_hash: 8dcb1e49b2cb9117
season: 2
testable_claim: "OWNER 2026-09-11 03:0xZ (verbatim in doc:l4-owner-decisions): \"The pin becomes the thing that keeps a process alive, and any that loses it loses the process except belam, which could have special 5 'predecessor' pins assigned to predecessors to keep logic uniform.\" CLAIM: THE PIN IS THE LEASE. (1) A seat session stays alive iff a pin names it: the pin file (.agi/sessions/<seat>.meter, pin_ref in the row) resolves to a transcript -> session_id -> pid (the L4.114 identity: ~/.claude/sessions/<pid>.json); the persistent watcher (heal.py watch, the same unit as L4.116b) reads every pin on each pass and REAPS any Claude Code seat session on the box whose identity no pin names (by @id + PID, deepest-first, SIGTERM then SIGKILL after the wait, one dm to the seat's rotator, one log line, idempotent) — a successor's pin claim is what ends its predecessor, no reap step in rotate-self remains. (2) UNIFORM FOR BELAM: the belam row carries predecessor_pins: 5; a prime rotation shifts the chain — the new prime takes belam.meter, the predecessor takes belam.pred-1.meter, pred-1 -> pred-2 ... pred-5 falls off and is reaped by the SAME rule; no Belam-cap code path, no special reap. (3) A pin is claimed only by the session it names (meter --pin verifies the transcript's session_id against the caller's identity) and is never deleted, only re-pointed; a stale pin (transcript gone) is SKIPPED with reason, never treated as a live lease. (4) The kill switch and a per-seat `protected: true` cell (owner-only) exempt a session from reaping; the owner's own remote-control sessions never appear in the pin table and are never touched — the watcher acts ONLY on sessions whose window name matches a seat or a Belam name in config:seats. (5) FIXTURES ONLY: a fake pin table + fake process table prove keep/reap/shift/skip; the live install is the Prime's step at merge-up (the unit), with a dry-run that lists exactly which pids would be reaped BEFORE anything is armed. FALSIFIERS: a live seat without a pin that survives a pass; a pinned session that is reaped; a Belam predecessor reaped while it holds a pred pin; an owner session touched; a reap without a dm. SERIAL: behind L4.123 (the service must first mark deaths correctly) and behind hypothesis:l4-a-spawn-arms-its-own-watch (same watcher). SCOPE: heal.py (watch loop), rotate.py (pin shift on prime rotation; the reap step retired), spawn_budget/config (predecessor_pins, protected), tests beside them."
thought_session: belam-S1-L4-VII
title: The pin is the lease — a seat lives while a pin names it; the watcher reaps the unpinned; Belam keeps five predecessor pins so the rule stays uniform
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-pin-is-the-lease

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
