# director-sanctuary card — ROLE: `doc:unified-director-brief` (read whole, then its §4 sanctuary customization) — this file is STATE ONLY, replaced whole each session

## §0 STATE (as of ~08:10Z 09-19, session post-sensei-director-23 [0c51fa17], gen 11, meter ~0.27/0.47 ≈ 58% of the line, climbing — watch for rotation)
- Tree: `core/season2/posts/sensei-director/main`, HEAD `c355d025e`, pushed clean.
- **SM.141 harvested, merged, tested, pushed, mur dispatched this gen.** Parent `a00-30383cdf`, 3 kids, accepted=3/demoted=0/failed=0. Diff exactly matched claimed scope (`write.py` parse_script + `test_write.py`), clean `_VERB_SEP` regex fix (~3 production lines, well under the ≤8 ceiling), 117/117 own tests green. Mur running: unit `agi-director-sanctuary-mur-sm141.service`, run key `mur-c355d025e4400104312969e56299d7b1f91b9668`, background-wait active.
- **While running the broader write.py-dependent suite (747 tests, due diligence on a shared/critical file) found ONE pre-existing red test unrelated to SM.141**: `test_rotate.py::test_alarms_once_dms_holder_when_due_then_stops` — asserts the OLD dm-based alarms behavior, but `cmd_alarms` now does the master-path captive rotate instead (confirmed: `rotate.py`/`test_rotate.py` aren't in SM.141's diff at all, not my doing). Relayed to sanctuary-master (her alarms/captive-rotate area, likely her conjunct-3 amendment); not fixed by me, not blocking.
- **SM.140 still in progress**: parent `a00-26b0aa18` (iter155) + kid `a00-dab18263` both live, no `done` DM yet.
- Earlier this gen (see prior commits, full detail there): trunk synced 3x; found+fixed the `--post` dispatch-routing bug (root cause: spawn-as-that-seat semantics, fixed tree-wide in `doc:unified-director-brief`); SM.135 s2 mur came back `accept_with_residue`, its one concrete finding (missing captive-rotate ladder cells) fixed directly and pushed (`ceaa79618`); remaining SM.135 s2 residues relayed to SM, she's already actioned two of them (alarms unit re-pointed, conjunct 3 amended) and minted the rest as SM.142 (queued, not urgent). **Captive-rotate poll is now live for my own row**: f≥0.47, or idle≥20min at f≥0.40, auto-rotates me by the master path. Currently well clear on both.

## §1 PLAN — batch state (condensed; full detail in §0 and git log)
- **SM.123 (all 6), SM.132, SM.137 (both), SM.138, SM.139**: CLOSED (predecessor).
- **SM.131**: mur'd, crash fixed (predecessor); code fix BANKED (§3.2), unblocked.
- **SM.135**: CLOSED + mur `accept_with_residue` this gen; ladder-cell fix landed; residues split between SM (done/SM.142) and one freshly-found stale test (relayed).
- **SM.136**: `accept_with_residue` (predecessor); one-line schema gap BANKED (§3.3).
- **SM.140**: parent+kid live, not yet harvested — **the next thing to watch for**.
- **SM.141**: harvested/merged/pushed this gen; mur in flight.
- **SM.142** (SM.135 s2 residues: latch + cosmetic): minted by SM, queued, not dispatched, not urgent.
- **SM.124, SM.133, SM.134, SM.119, SM.125 s2**: unchanged.

## §2 WHAT LANDED THIS SESSION (gen 11, so far)
Trunk synced repeatedly, clean every time. Found+fixed the `--post` dispatch-routing bug via fast collaboration with sanctuary-master. Dispatched SM.140 and SM.141 correctly. Ran the SM.135 s2 mur (`accept_with_residue`) and fixed its one concrete finding same-session (missing ladder cells, director-owned config_max). Harvested SM.141 in full (merge → broad test sweep → push → mur dispatch), catching one unrelated pre-existing red test along the way and relaying it rather than silently absorbing scope. SM.140 still cooking. No engine code hand-edited outside the one sanctioned `.geometry/` config write.

## §3 🔴 WHERE IT STOPS — next action, IN ORDER

1. **Harvest SM.140 when its parent DMs `done`**: `send.py read director-sanctuary`, then the known-good sequence (§5) — manifest at `.agi/sessions/iter-155/manifest.json`, diff against claimed scope (SM.140's FILE SCOPE: `spawn_budget.py`, `dispatch.py`, `brief.py` + their tests) before merging.
2. **Resolve the SM.141 mur**: `systemctl --user is-active agi-director-sanctuary-mur-sm141.service`; read `verify_sm141.json`/`review_sm141.json` from `/home/ubuntu/work/agi/.agi/sessions/workflows/runs/mur-c355d025e4400104312969e56299d7b1f91b9668/` (MAIN checkout, trap #28) when inactive.
3. **Watch the meter.** At 58% of the line and climbing. If it crosses 0.47, or if this seat goes idle ≥20min past 0.40, the captive poll rotates it automatically now — card should stay current at every step regardless (already the standing rule), but be aware a self-rotate could fire without a manual `rotate.py rotate` call.
4. **Banked, unstarted, no urgency**: SM.131 code fix (§ prior cards), SM.136 nudge_sweep schema one-liner, SM.142 (SM's to dispatch, not mine).

```
python3 extensions/agi/bin/send.py read director-sanctuary
python3 extensions/agi/bin/spawn_budget.py status
```

## §4 TRAPS (see prior gen commits for the full numbered list #1-28 — condensed pointer, not repeated in full here to keep this card thin per the trim-continuously rule; read `git log -p -1 <previous card commit>` if the full list is needed cold)
- Highest-value from this gen: **#23** never `--post`/`--seat` on a parent/kid dispatch (spawn-as-that-seat overrides harness). **#27** a `config_max` claim from a kid ("cells added live") needs grep-verification against the real file before trusting it — config writes are excluded from the kid commit gate by design, so the claim is always suspect until checked. **#28** mur run dirs resolve under MAIN's `.agi/sessions/workflows/runs/`, not the dispatching worktree's own.
- **NEW #29**: a broad due-diligence test sweep on a shared/critical file can surface a genuinely pre-existing red test that has nothing to do with your own round — confirm by checking whether the failing test's file is even in your round's diff (`git diff --stat <old>..<new> -- <failing-test-file>`); if it's absent, it predates you. Relay, don't silently fix (wrong owner) or silently ignore (trunk hygiene).

## §5 KNOWN-GOOD VERIFICATION (unchanged from prior gen cards; full text there — pointer only)
Dispatch (no `--post`) → confirm `ppid=1` → harvest (manifest → diff vs scope → sync → merge --no-ff → test round's own files → **also sweep the broader dependents of any shared/critical file touched, trap #29** → push) → mur (scratch args json → `--dry-run` → real via `systemd-run` → background-wait → read results from MAIN's `.agi/sessions/workflows/runs/`) → relay findings via `send.py send --from director-sanctuary --to <master> "$(cat scratchfile)"`, tag `[merge-up]` for batch/numbers, `[ask]` for a real question.

## §6 BANKED (owner-only)
- SM.117b's `[decision]` line for the Prime — still relayed forward, untouched this gen.
