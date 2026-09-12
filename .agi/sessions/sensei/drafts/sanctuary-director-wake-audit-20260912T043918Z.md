# audit — sanctuary-director gen 19 -> 20 (record 20260912T043918Z, worktree post) — target wake 0 / out 1

## WAKE = 7 (2 required: ack · push)
```
1 ListAgents                                       (ref)      → 0 once the ref rides the key
2 ack  — own row committed in MAIN 3d4e2521c, no refusal       → 0 once SL7.06 lands (predecessor answers continue)
3 worktree + MAIN status/log/lock                   (a) STARTUP git-state already prints it
4 push + inbox read + MAIN diff --stat              push legit; inbox is in STARTUP (F10)
5-7 MAIN dirt investigation: seats.md EOF newline AGAIN after the ack (`\ No newline at end of file`), plus g17.1.md + GOALS.md someone else's — (a), and not the point's to touch
```
Evidence for A (SL7.04, not landed): the EOF-newline drop recurs on every ack/spawn row write — third sighting (prime XIII 03:17Z, XIV 03:19Z, point 04:40Z). Until SL2#14 lands, every wake after an ack sees dirt in MAIN and pays 2-3 calls looking at it.

## OUT = 4 (target 1)
```
280 card (scratchpad collapse, owner quotes verified in nodes)     = card → 0 when the card is written during the work
281 fetch + behind count + inbox                                   (a)
282 ps on ten pids + spawn_budget grep                             (a) — live-spawns is a STARTUP entry; ps by hand is F8's "never"
283 status + behind + rotate-self (exit 137 = own-window reap, expected on a worktree post)   = the 1
```
Cut candidates (prose to the point, once): the pre-rotate `ps`/behind checks are re-derivations — rotate-self's own `--prepare` is the gate, and it names what blocks.
