---
id: hypothesis:l4-the-card-age-captive-clocks-the-rotating-seat-own-last-act-never-a-repo-wide-commit-and-merge-up-in-flight-means-a-real-merge
mint_id: 3e18c67ff9ee4fb7b76e4f18421c2713
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 19a0fc1f42466888
season: 2
testable_claim: "PRIORITY (owner in-pane 14:0xZ: directors are always rotating; a brand-new director under a brand-new master hit it 4 times running). Measured by director-thought 10:23Z and verified on MAIN 7180ab91e: the card-age captive is a REPO-WIDE clock. rotation_alert.py:615 _work_last_ts = `git log -1 --no-merges --format=%ct -- . :(exclude).agi/comms :(exclude).agi/sessions/rotations :(exclude)<card> :(exclude)<seats>` -- the newest non-merge commit by ANY seat -- and :635 _card_stale_measure calls the card stale when its mtime is older than that; rotate.py:14647 (_prepare_checks check 4, `card older than last commit`) is a second copy of the same clock. Nothing scopes it to the rotating seat, so with N seats committing to ONE shared checkout, every other seat's card write, node note or GOALS.md re-render re-stales the rotating seat's check faster than its write -> commit -> push -> recheck round trip; director-thought looped 4 consecutive times, thought-master paid 6 recovery calls (master-sensei 12:48Z). Gate (b) rotation_alert.py:573 _season_unpushed labels ANY unpushed commit `merge-up in flight` (`rev-list --count origin/<season>..<season>`), which in a shared checkout is the normal state between pushes and is usually another seat's commit. CLAIM: (1) ONE helper (bin, imported by both the hook and rotate) defines the seat's LAST WORK ACT as the newest of the seat's OWN acts, never a repo-wide commit: a per-seat stamp `<sessions>/seats/<seat>.last-act` touched by the engine verbs the seat runs -- write.py (--actor), send.py send (--from), dispatch.py (the dispatching seat), cli.py harvest/merge-up/session-complete (the seat) -- plus the seat's own card commit time; (2) _card_stale_measure and rotate check 4 both compare the card mtime against THAT value; another seat's commit can never stale this seat's card (test: two fixture seats, seat B commits a node, seat A's card check stays fresh); a seat with no stamp yet reads NOT stale (ok-unmeasurable); (3) gate (b) fires only on an actual merge in flight -- MERGE_HEAD present in the seat's own tree, or the suite lock held by the seat's own merge-up pid -- and prints the unpushed count as INFO, never as a captive; (4) the refusal text keeps the one-line exit first (write the card, commit it by path, rotate). FALSIFIERS: any commit not made by the rotating seat changing its card-stale verdict; two implementations of the clock surviving; a rotation refused for an unpushed commit that is not a merge in flight; a seat's own write.py/send.py/dispatch act after its card write NOT staling the card. TESTS (<=6, fixtures only, no live hook/tmux): foreign commit -> fresh; own write.py act after the card -> stale, naming the act; card saved after the act -> fresh; no stamp -> fresh (unmeasurable); MERGE_HEAD -> gate (b) fires; ahead-only -> info line, not a captive; hook and rotate agree byte-for-byte on the same fixture. FILE SCOPE: one new helper in bin (or spawn_budget/rotate), rotation_alert.py (:573, :615, :635), rotate.py check 4 (~:14647), the four verbs' stamp call (one line each), their tests. CEILING: <=60 production lines, <=2 kids (helper+gates, then the verb stamps) -- re-brief SM past 2x."
title: L4 the card age captive clocks the rotating seat own last act never a repo wide commit and merge up in flight means a real merge
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-card-age-captive-clocks-the-rotating-seat-own-last-act-never-a-repo-wide-commit-and-merge-up-in-flight-means-a-real-merge

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
