# CARD — director-thought

## SELF-FACTS (gen1 wake-audit, master-sensei 2026-09-16T07:21Z) — handed, not fetched
- Ack grammar is F6, verbatim: `rotate.py ack --post <post> --ref <bare ref> continue|diff [--text -]`. Never grep rotate.py source for it.
- Card path is always `.agi/sessions/quorum/<post>.md` (F26). Never `find`/search for it.
- On any wake, read your own inbox FIRST (call 1) — a nudge names the reason you're awake.
- Never read another seat's rotation record (e.g. your master's) — not your concern; wait for their message instead.

## 0 STATE (2026-09-16, ~08:2xZ)
- Re-stood on claude-sonnet-5/max per owner 06:3xZ resume order; tree-wide 09-14 PAUSE/FULL IDLE lifted same morning (belam broadcast).
- TM ORDER 3 (`hypothesis:c2-digital-kuramoto-flip-mode`, chain 2) dispatched as **TM.02**: parent `a00-08515464` done, verdict=proved. All 3 kids (A/B/C) proved, all 4 negative probes per kid HOLD, independent cross-check matches to 3 decimals (Kid A K_c=115.96 == Kid B all-flip K_c=115.962). File scope clean, no self-authored parent node, real `spawn.json` for all 3 kids (TM.01 trap checked, avoided). Branch `season2/loops/hypothesis-c2-digital-kuramoto-f-a00-08515464` tip `27f9c7883`.
- TM.02 merge-up attempt 1: REFUSED (suite red) — but the cause is `verify-suite.lock` contention, NOT a broken suite: `test_zoom.py`'s traceback is `RuntimeError: suite window refused — pid 2907182 is a LIVE runner holding .agi/sessions/verify-suite.lock; one suite at a time` (confirmed pid 2907182 alive, a `test_workflow.py` targeted run, not mine). All 4871 "errors" on a bare pytest run were this ONE cause repeated per test (session-scoped autouse fixture), not 4871 real failures. `season.py merge-up` did exactly what it should: staged, ran the suite, saw red, `git merge --abort`ed cleanly — branch `season2/loops/hypothesis-c2-digital-kuramoto-f-a00-08515464` is untouched, season2/main is untouched, MERGE_HEAD confirmed absent after. Not a rule-changing finding, not a real red merge — routine contention. Retry once `cat .agi/sessions/verify-suite.lock` is empty/absent, no need to tell TM or belam over this.
- TM ORDER 4 (`hypothesis:gpu-local-town-openai-endpoint`) arrived, explicitly concurrent with C2 per owner ruling (<=5 pi parents live, 10 kids each). Dispatched as **TM.03**: parent `a00-ab5b20f7` (pid 2843538, branch `season2/loops/hypothesis-gpu-local-town-openai-a00-ab5b20f7`) spawned, running. Higher-sensitivity round (SSH to local-town, systemd tunnel, one additive `.agi/config.json` key) but every guardrail is already baked into the node (loopback-only, no IP ever printed, `<keeper-dir>` contents never read, no ufw, static non-secret key, defined rollback) — nothing for this seat to add beyond dispatching what TM already minted.
- TM reviewed + demoted prior D1 work: `hypothesis:lm-round0-box-calibration-and-two-kill-tests` -> inconclusive_lean_disproved:60; `experiment:a00-51318335-e170a9` -> lean_disproved:60. Informational, no action needed here.

## 1 PLAN
- next: check `.agi/sessions/verify-suite.lock` next time something wakes this seat anyway (no dedicated poll loop just for this); retry `season.py merge-up` for C2 once it's free/absent.
- TM.02 merge-up green -> validate links/schema, confirm the push landed, one line to thought-master, a `[complete]`-tagged dm to belam per the lap-report rule (never untagged).
- TM.02 merge-up red AGAIN with a DIFFERENT cause (not lock contention) -> that's the real "red merge" case: dm thought-master the exact suite failure verbatim, never attempt a manual fix myself (directors never hand-write engine code, owner 04e5070c9).
- TM.03 parent lands -> same audit shape as C2: diff vs merge-base, confirm no self-authored node, confirm the 3 kid claims + parent's own probes, confirm file scope (no sanctuary contents, no IP strings, exactly one additive config key), then merge-up.
- a further order may land while these two are in flight (owner ruling allows up to 5 concurrent parents) — dispatching what TM mints is in-scope any time; minting a node myself, or hand-writing engine code, never is.

## 2 TRAPS
- `links.py schema` is a dry report, not a clean-suite signal.
- `season.py merge-up`'s default `--suite` is exactly `python3 -m pytest extensions/agi/tests/ -q` (DEFAULT_SUITE in season.py) — no need to compose a custom suite string, and it already stages-then-gates-then-commits so a red suite aborts clean.
- `dispatch.py` returns almost immediately regardless of `--detach` whenever `agent_dispatch.inline_reaper=false` (true here) — a fast return is a SPAWN signal, never a completion signal. Completion arrives as an inbox dm from the parent's own agent id.

## 3 VERIFICATION
- C2 round bytes (pre-merge, on the loop branch): `git show --stat --oneline 27f9c7883`
- D1 (prior round, now demoted by TM): `git show --stat --oneline 04994c52f`
