# CARD — director-thought

## SELF-FACTS (gen1 wake-audit, master-sensei 2026-09-16T07:21Z) — handed, not fetched
- Ack grammar is F6, verbatim: `rotate.py ack --post <post> --ref <bare ref> continue|diff [--text -]`. Never grep rotate.py source for it.
- Card path is always `.agi/sessions/quorum/<post>.md` (F26). Never `find`/search for it.
- On any wake, read your own inbox FIRST (call 1) — a nudge names the reason you're awake.
- Never read another seat's rotation record (e.g. your master's) — not your concern; wait for their message instead.

## 0 STATE (2026-09-16, ~08:3xZ)
- Re-stood on claude-sonnet-5/max per owner 06:3xZ resume order; tree-wide 09-14 PAUSE/FULL IDLE lifted same morning. Three TM orders processed so far, all concurrent under the owner's 5-parent/10-kid ruling.
- **TM.02** (`hypothesis:c2-digital-kuramoto-flip-mode`, ORDER 3) — CLOSED. Parent `a00-08515464` proved; all 3 kids (A/B/C) proved, 4 negative probes/kid all hold, independent cross-check matched to 3 decimals. My own `season.py merge-up` was refused twice for environmental reasons, never a code problem (attempt 1: `verify-suite.lock` held by an unrelated live pytest run; attempt 2: raced by another seat's concurrent git op in this same shared primary checkout — top-level seats aren't worktree-isolated from each other the way kids/parents are). C2 landed anyway, swept into belam's own SM.23b/24b/24c bundle merge (tip `1c7072101`); attempt 3 correctly found "zero commits ahead -- nothing to merge". Verified post-hoc: C2 files present on `season2/main`, `links.py links` = 3093 resolved/0 broken, `grid.py commit --all` = already current (0 new versions). Reported: one line to thought-master, `[complete]`-tagged dm to belam. Nothing further owed on this round.
- **TM.03** (`hypothesis:gpu-local-town-openai-endpoint`, ORDER 4) — running. Parent `a00-ab5b20f7` (pid 2843538) went OVERDUE at ~20 min but is confirmed still alive — expected (GPU docker pull + multi-GB GGUF download plausibly exceeds the manifest timeout), not terminal. High-sensitivity round (SSH, systemd tunnel, one additive config key) but every guardrail is baked into the node itself; nothing for this seat to add beyond auditing the result once it lands.
- **TM.04** (`hypothesis:ws-raw-zero-injection-adapter`, ORDER 5) — running. Parent `a00-2f819956` (pid 2996851). Kids write real engine code this round (`ws_raw.py`, `ws_raw_client.py`, `test_ws_raw.py`) — fine, "directors never hand-write engine code" binds me, not dispatched kids. The round only runs `test_ws_raw.py` internally; my own merge-up gate still runs the FULL suite regardless (more warranted, not less, since real code lands).
- TM reviewed + demoted prior D1 work (`hypothesis:lm-round0-box-calibration-and-two-kill-tests` -> inconclusive_lean_disproved:60; `experiment:a00-51318335-e170a9` -> lean_disproved:60). Informational only.

## 1 PLAN
- next: no dedicated poll. Wait for a nudge — TM.03/TM.04 completion or overdue notices, or a further TM order (a 4th+ concurrent round is explicitly allowed under the 5-parent ruling).
- when TM.03 or TM.04 lands: same audit shape each time — diff vs merge-base (never a moved tip), confirm no self-authored parent node, confirm the kids' own claims + the parent's negative probes actually hold from the bytes, confirm file scope, THEN `season.py merge-up`. Expect the lock/race hiccups seen on TM.02 to recur under this much concurrency — retry rather than escalate unless the cause is genuinely new.
- report shape per round: one line to thought-master always; belam gets a `[complete]`-tagged dm only, per the lap-report rule (never untagged, never any other tag for routine completion).
- still true: dispatching whatever TM mints is in-scope any time; minting a hypothesis node myself, or hand-writing engine code, never is (owner 04e5070c9).

## 2 TRAPS
- `links.py schema` is a dry report (156 pre-existing missing-field nodes, unrelated to my rounds) — not a clean-suite signal.
- `season.py merge-up`'s default `--suite` is exactly `python3 -m pytest extensions/agi/tests/ -q` (DEFAULT_SUITE in season.py) — never compose a custom suite string. It stages (`--no-ff --no-commit`) THEN gates THEN commits, so a red suite (or a race that clears the stage) aborts clean either way — always re-check `git log --ancestry-path <branch-tip>..HEAD` before assuming a refused merge-up means the work is unlanded; something else may have already carried it in.
- `dispatch.py` returns almost immediately regardless of `--detach` whenever `agent_dispatch.inline_reaper=false` (true here) — a fast return is a SPAWN signal, never a completion signal. Completion arrives as an inbox dm from the parent's own agent id.
- top-level seats (director/master/prime) all share ONE primary checkout, not isolated worktrees like kids/parents get — a merge-up here can legitimately race another seat's concurrent git operation. Diagnose (branch/worktree intact? did the content land anyway?) before treating a refusal as a real problem.

## 3 VERIFICATION
- C2 on main: `git log --oneline --ancestry-path 27f9c7883..season2/main | tail -5` (expect it inside the SM.23b/24b/24c bundle)
- D1 (prior round, demoted by TM): `git show --stat --oneline 04994c52f`
