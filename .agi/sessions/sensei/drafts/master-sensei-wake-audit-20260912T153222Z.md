# wake audit — master-sensei, record 20260912T153222Z (3→4, rotate-self --stops)

## successor (this post, transcript 21497613, from call 1)
- **wake = 1**, wasted: `rotate.py meter --pin …` — the pin was ALREADY written at spawn (F8; `.meter` mtime 15:33:13Z). Cause = prose: the predecessor card said "meter pin is your one setup call". Card fixed 848fa20fd. Also in that call: copied the listing script from a scratchpad (routed → `sensei.py calls`, harvested as SL7.68) and re-read an inbox STARTUP had already printed empty.
- owner in pane 15:4xZ–15:5xZ (verbatim in doc:l4-owner-decisions): stale `--seat` args (template fixed → `--post`, 5 sites, 848fa20fd); per-spawn setup is rotation's job for every role; the context meter prints automatically before the turn; via template — `meter` telemetry key added to both role templates (4bad592ec, fb9e86652), resolver routed.

## predecessor (gen 3 tail)
- out = 1 + card during work (2bd8b2549 card, f07aa6a54 rotate-out). At target.

## after_join — first ever performed for this post (16:09:44Z, `performed_by: service`, `delay_s: 0`)
Measured on the delivered dm and the record's `results`:
1. **37 min late** — spawned 15:33Z, performed 16:09Z; `after_join_delay_s: 20`. A second input that lands mid-session is context spam. Suppress past a bound (e.g. 5 min) or perform in rotate-self's post-spawn tail when no watcher runs.
2. `pin` exit 0: `0.1112 111213/1000000 threshold=0.47` — correct, this IS the wake meter print; only the timing was wrong.
3. `ack` exit 2: `--gen 0 --ref ''` — `{gen}` and `{succ_ref}` unresolved at perform time; the dm's captive line also hardcodes `--seat` and `--gen 0`.
4. `reap-proof` exit 0 with 8000 bytes: `{pred_pids}` resolved empty → `grep -E ''` matches every process. Must refuse on an empty pid list (P6), never dump.
5. every entry's output carries the `config:seats is deprecated` note (SL7.67 deletes it).
Before 16:09Z: 86/91 records lacked the `after_join` key, 5 held `{}` — never performed anywhere. Whatever went live at ~16:09Z (SL7.54 fix / heal watch) is the performer; it performed both master-sensei and sensei-director records within one minute.

## floor board
master-sensei wake 1 / out 1 (3→4).
