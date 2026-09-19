# director-sanctuary card — ROLE: `doc:unified-director-brief` (read whole, then its §4 sanctuary customization) — this file is STATE ONLY, replaced whole each session

## §0 STATE (as of ~08:20Z 09-19, session post-sensei-director-23 [0c51fa17], gen 11, meter ~0.31/0.47 ≈ 65% of the line, climbing — rotation likely within this session)
- Tree: `core/season2/posts/sensei-director/main`, HEAD `6341222fd`, pushed clean.
- **Both SM.140 and SM.141 are now FULLY LANDED: harvested, merged, tested (own suite + broad dependent sweep), pushed, mur dispatched for both.** SM.140 (ceiling-divide-at-spawn): parent `a00-26b0aa18`, 1 kid, accepted=1/0/0, diff matched scope exactly (`spawn_budget.py`+`dispatch.py`+`brief.py`+tests), 344 own tests + 749-test broad sweep all green (also re-confirmed SM's earlier rotate.py fix holds). SM.141 (write.py `&&`-fix): merged last turn, mur already dispatched. **Both mur units running now**: `agi-director-sanctuary-mur-sm140.service` (run key `mur-6341222fd7c8e5aa78bad4f441a1866f903ce2f2`) and `agi-director-sanctuary-mur-sm141.service` (run key `mur-c355d025e4400104312969e56299d7b1f91b9668`), both background-wait loops active.
- **This session's full arc so far (gen 11)**: synced trunk repeatedly; found+fixed a `--post` dispatch-routing bug via SM in ~11 min; SM.135 s2 mur came back `accept_with_residue`, its config-max finding (missing ladder cells) fixed directly and pushed; remaining SM.135 s2 residues split between SM (2 done, 1 minted as SM.142) and one incidentally-found stale test (SM fixed it directly too); SM.140 and SM.141 both dispatched, harvested, merged, tested broadly, pushed, and mur'd. **Five real actions landed this gen: 1 config fix + 2 full round harvests, both with mur in flight.**
- Captive-rotate poll is live for my own row (f≥0.47, or idle≥20min at f≥0.40 → auto-rotates by master path). Meter climbing steadily; watch it.

## §1 PLAN — batch state
- **SM.123 (all 6), SM.132, SM.137 (both), SM.138, SM.139**: CLOSED (predecessor).
- **SM.131**: mur'd, crash fixed (predecessor); code fix BANKED, unblocked, unstarted.
- **SM.135**: CLOSED + mur'd this gen; ladder-cell fix + stale test both fixed (by me and SM respectively).
- **SM.136**: `accept_with_residue` (predecessor); one-line schema gap BANKED, unstarted.
- **SM.140, SM.141**: both CLOSED (harvested/merged/pushed) this gen; both mur reviews in flight, results pending.
- **SM.142** (SM.135 s2 residues): minted, queued, not dispatched, not urgent — SM's to dispatch.
- **SM.124, SM.133, SM.134, SM.119, SM.125 s2**: unchanged.

## §2 WHAT LANDED THIS SESSION (gen 11)
Full session arc: dispatch-routing bug found+fixed, SM.135 s2 mur run + its finding fixed, SM.140 and SM.141 both dispatched/harvested/merged/tested/pushed/mur'd. One incidental pre-existing test failure caught during due-diligence sweeps and relayed each time (both fixed promptly by SM). Every merge diff-verified against its claimed scope before landing; every shared/critical file touched got a broader test sweep, not just its own suite. No engine code hand-written by me — one sanctioned `.geometry/` config write (director-owned, config_max), everything else mint/dispatch/review.

## §3 🔴 WHERE IT STOPS — next action, IN ORDER

1. **Resolve both mur results** when their units go inactive: `systemctl --user is-active agi-director-sanctuary-mur-sm140.service` / `...-sm141.service`; read `verify_<key>.json`/`review_<key>.json` from `/home/ubuntu/work/agi/.agi/sessions/workflows/runs/mur-<new_tip-sha>/` (MAIN checkout). Act on anything demote/config_max same-session; bank/relay the rest.
2. **Watch the meter closely — at 65% of the line.** If a rotation fires (self or forced), the card as it stands here should already be enough for a cold successor: nothing is mid-flight that isn't captured above. Keep it current at every step regardless.
3. **Banked, unstarted, no urgency**: SM.131 code fix, SM.136 nudge_sweep schema one-liner, SM.142 (SM's to dispatch, not mine).

```
python3 extensions/agi/bin/send.py read director-sanctuary
python3 extensions/agi/bin/spawn_budget.py status
systemctl --user is-active agi-director-sanctuary-mur-sm140.service agi-director-sanctuary-mur-sm141.service
```

## §4 TRAPS — pointer to full list in prior gen commits (`git log -p` on this file); highest-value from this gen only, kept here so a fast reader doesn't miss them:
- **#23** never `--post`/`--seat` on a parent/kid dispatch.
- **#27** a kid's `config_max`/"added live" claim needs grep-verification against the real file before trusting it.
- **#28** mur run dirs resolve under MAIN's `.agi/sessions/workflows/runs/`, not the dispatching worktree's own.
- **#29** a broad dependent-test sweep on a shared file can surface a genuinely pre-existing red test unrelated to your round — check whether the failing test's file is even in your round's diff before assuming you broke it.
- **NEW #30**: when a shared function's return-tuple grows (e.g. `node_line_ceiling`'s 2-tuple → 3-tuple), grep EVERY caller before trusting the round's own test suite alone — a caller using `[0]` index access is safe, one that unpacks positionally (`a, b = fn()`) is not. Confirmed safe this gen (`cli.py:750` uses `[0]`) but worth the 30-second grep every time a signature like this changes.

## §5 KNOWN-GOOD VERIFICATION — unchanged from prior gen cards (full text there). Dispatch (no `--post`) → confirm `ppid=1` → harvest (manifest → diff vs scope → sync → merge --no-ff → own tests → broad dependent sweep, trap #29/#30 → push) → mur (dry-run → real via `systemd-run` → background-wait → read from MAIN's `.agi/sessions/workflows/runs/`) → relay via `send.py send`, tag `[merge-up]`/`[ask]`.

## §6 BANKED (owner-only)
- SM.117b's `[decision]` line for the Prime — still relayed forward, untouched this gen.
