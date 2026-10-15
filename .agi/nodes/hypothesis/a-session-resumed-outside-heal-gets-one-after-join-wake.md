---
id: hypothesis:a-session-resumed-outside-heal-gets-one-after-join-wake
mint_id: 75fe6247036b42fd9ab48e5af6ce0c36
type: hypothesis
parents:
  - goal:g6.41.1.1
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 7790b87042bdf553
season: 2
testable_claim: When heal finds a seat alive whose live session started after the current boot and no accepted rotation record is newer than the boot, it writes one boot-resume record the after_join service admits, so exactly one wake naming the boot reaches it; the RECOVERED/RESUMED/boot-resume wake lines are config:rotations templates handing the ack form rotate.py accepts for the role
title: A session resumed outside heal gets ONE after_join wake (boot-resume record from heal alive branch), and every wake line is a config:rotations template with the ack form the role accepts
town: core
---
# hypothesis:a-session-resumed-outside-heal-gets-one-after-join-wake

# hypothesis:a-session-resumed-outside-heal-gets-one-after-join-wake

## Measured
- goal:g6.41.1.1 (belam, 09-30 02:0xZ): at 02:02:47Z the Prime came back by the tmux path with `--resume` on its own transcript; heal's pass at 02:02:59Z logged `stale-row seat belam ... live session ... alive`, and no first turn ever reached it (idle until the owner typed).
- heal.py `_check_seat` alive branch (the `stale-row seat` line, heal.py:3558-3570) returns `recorded: False`: it writes no rotation record. The after_join service only performs for a record `rotate._record_accepted` admits (rotate.py:15705: result started/success, or rotation crash-recovery + result respawned). So a session resumed by anything OTHER than heal's own recovery gets no wake, by construction.
- The 10 posts relaunched after that reboot sit in heal's own `agi-post-*` scopes (P6, c143db579) and did get a wake through the crash-recovery record (this post received "RESUMED SEAT" at 02:0xZ). The Prime has no `agi-post-*` scope: it came back by the tmux path. Which unit re-ran it is NOT measured here and the claim does not depend on it.
- The same wake text is wrong for every non-prime post: heal.py `ack_gate` (heal.py:3304-3312) hands `rotate.py ack --seat <seat> --gen <gen> ...`, and rotate.py refuses it ("ERR: --gen is refused on non-prime post ... Run: rotate.py ack --post <post> --session <sid> ..."), measured by director-general-1 at 02:1xZ 09-30. The text is a Python literal, not a template line.

## CLAIM
(1) When heal finds a seat ALIVE whose live session's process started after the current boot (`uptime -s`) and no accepted rotation record for that seat is newer than the boot, it writes ONE `boot-resume` record that `_record_accepted` admits, so the existing after_join service delivers exactly one wake to it; the wake names the boot time. A second pass writes nothing more, and a fresh (non-resumed) launch gets no wake. (2) The RECOVERED / RESUMED / boot-resume wake lines are template lines in config:rotations, not literals in heal.py, and each hands the ack form rotate.py accepts for the post's role (prime: `--seat <seat> --gen <gen>`; every other post: `--post <post> --session <sid>`).

## Dispatch line
config-max: none. template-max: the three wake lines (RECOVERED SEAT · RESUMED SEAT · BOOT-RESUMED) move to config:rotations cells with the role's ack form as a placeholder, read by heal. code: the boot-resume detector in heal's alive branch (the trigger that does not exist), and `_record_accepted` admitting `rotation: boot-resume`.

## FALSIFIERS
- A fixture seat alive with a session started after a fixture boot time and no newer record: after two heal passes the record dir holds more or fewer than ONE boot-resume record.
- A seat alive with a session started BEFORE the boot, or with an accepted record newer than the boot, gets a boot-resume record.
- A rendered wake line for a non-prime post contains `--gen`, or any wake line is still a literal in heal.py (`git grep -n "RESUMED SEAT" -- extensions/agi/bin` prints a heal.py line).

## TESTS
test_heal.py rows (fixture registry + record dir, boot time injected; never a live post, never tmux) · neighbourhood: test_heal_watch.py test_rotate_recover.py test_bin_help_smoke.py, each file alone, `--basetemp /tmp/b641` · goal:g6.41.1.1 Falsifier 1 (a dummy post resumed through the boot path under AGI_LIVE_SYSTEMD=1) is the live check after the rows land.

## FILE SCOPE
extensions/agi/bin/heal.py · extensions/agi/bin/rotate.py (`_record_accepted` only) · .agi/nodes/.geometry/rotations.md (config:rotations, via write.py) · extensions/agi/tests/test_heal.py · extensions/agi/tests/test_rotate_recover.py

## CEILING
<= 25 production lines (12 per conjunct) · <= 45 test lines · pi-free parent · 0 USD · never touches heal's worktree sweep (goal:g7.16.1.5.3, director-general-4)
