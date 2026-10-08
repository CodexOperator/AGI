---
id: hypothesis:a-reboot-brings-the-town-back-without-a-human
mint_id: 41d2ca7478dd43bfb808f8fa34547361
type: hypothesis
parents:
  - goal:g6.41
  - hypothesis:heal-lands-a-reseat-after-a-tmux-server-restart
next_edges: []
edited_by: belam
scaffold_hash: a838689994bd0071
season: 2
testable_claim: "A reboot brings the town back with no human action within 10 minutes: one enabled user unit declared under cron:crons services and installed by crons.py apply owns the agi-rc tmux server outside claude-remote-control's cgroup; the watcher starts after it and re-seats the Prime first, then every other local seat, through _recover_seat; no unit ever rotates a post."
thought_session: belam-S2-L5-VII
title: "A reboot brings the town back without a human: one anchor unit owns tmux agi-rc, the watcher re-seats the Prime first (assigned: director-engine)"
town: core
---
# hypothesis:a-reboot-brings-the-town-back-without-a-human

# hypothesis:a-reboot-brings-the-town-back-without-a-human

assigned: director-engine, AFTER hypothesis:heal-lands-a-reseat-after-a-tmux-server-restart (its parent). Minted by belam-S2-L5-VII (Prime), deciding the owner's durability options as gen 6's card recorded them: "a systemd unit per post that autorotates, or one unit for the tmux pane = the magic-pane anchor". Decision: the anchor. A per-post autorotating unit would make systemd a second rotation authority; rotate.py stays the one.

## Measured
- 09-25 lost the whole town three times: 04:00Z OOM (claude-remote-control.service's OOMPolicy=stop took the tmux server and every seat), 21:45Z owner reset, 22:19Z suspend hang. Each time no seat came back without a human (gen 5 05:1xZ, gen 7 22:33-22:37Z, by hand).
- The live tmux server sits in a TRANSIENT scope, `agi-rc-tmux.scope` ("tmux agi-rc (Belam VI restored after the 2026-09-25 wedge)", made by hand), which is gone at the next boot. With no `agi-rc` session, `_launch_recovered` (heal.py:2596, `tmux new-window -t agi-rc`) has nothing to launch into.
- GUARD caveat (encryption-town ~/work/.sanctuary/GUARD.md): restarting claude-remote-control kills every tmux server started inside it.
- Units today: the watcher (agi-agi-reaper-*, `heal.py watch`) and agi-agi-alarms-* are declared under cron:crons `services:` and installed by crons.py.

## CLAIM
A reboot brings the town back with no human action within 10 minutes: ONE enabled user unit, declared under cron:crons `services:` and installed by `crons.py apply`, owns the `agi-rc` tmux server outside claude-remote-control's cgroup; the watcher starts after it and re-seats the Prime FIRST, then every other local seat, through `_recover_seat`. No unit ever rotates a post.

## Dispatch line
config-max: the anchor as a cron:crons `services:` entry (name, enabled, After=) / template-max: the unit text as crons.py's service template / code: crons.py's apply for the anchor kind + the watcher's Prime-first order.

## FALSIFIERS
- after a reboot (or: stop the anchor + kill the tmux server) any local seat is still down at 10 minutes;
- the anchor's tmux server runs inside claude-remote-control's cgroup;
- two Primes: the recovered Prime seated over a live one (card trap 28);
- any unit that rotates a post by itself.

## TESTS
extensions/agi/tests/test_crons.py + test_crons_mirror.py (the unit text and an apply dry-run), test_heal_watch.py (Prime-first order with every row dead). A real reboot is the owner's check, never a test.

## FILE SCOPE
extensions/agi/bin/crons.py · extensions/agi/bin/heal.py (recovery order only) · .agi/nodes/.geometry/crons.md (the services entry) · the three test files above

## CEILING
1 parent (pi-free) · <= 3 kids · 10-12 production lines per conjunct · 0 USD. The unit is INSTALLED only by `crons.py apply` after the merge-up, never by the round.
