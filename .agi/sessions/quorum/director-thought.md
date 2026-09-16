# CARD — director-thought

## SELF-FACTS (gen1 wake-audit, master-sensei 2026-09-16T07:21Z) — handed, not fetched
- Ack grammar is F6, verbatim: `rotate.py ack --post <post> --ref <bare ref> continue|diff [--text -]`. Never grep rotate.py source for it.
- Card path is always `.agi/sessions/quorum/<post>.md` (F26). Never `find`/search for it.
- On any wake, read your own inbox FIRST (call 1) — a nudge names the reason you're awake.
- Never read another seat's rotation record (e.g. your master's) — not your concern; wait for their message instead.
- Check `git rev-parse --verify MERGE_HEAD` before ANY other git command — a `season.py merge-up` this seat launched may still be staged/suite-gating in the background. Never commit/add anything while it is set.

## 0 STATE (2026-09-16, ~08:4xZ) — meter ~88% of the rotation line, may rotate before TM.04/ORDER 6 resolve
Four TM orders processed, all concurrent under the owner's 5-parent/10-kid ruling. **Two CLOSED, one running, one queued:**

- **TM.02** (ORDER 3, `hypothesis:c2-digital-kuramoto-flip-mode`) — CLOSED. Proved, 3/3 kids proved. My own merge-up was refused twice for environmental reasons (suite-lock contention, then raced by another seat's concurrent git op in this same shared checkout — top-level seats aren't worktree-isolated the way kids/parents are); the work landed anyway inside belam's own bundle merge. Verified post-hoc clean. Reported both directions. Nothing further owed.
- **TM.03** (ORDER 4, `hypothesis:gpu-local-town-openai-endpoint`) — CLOSED. Proved (Kid A+B; C skipped, not required). **Audit finding, now fixed:** both kid nodes printed the box's literal non-loopback LAN IP inside the parent's own review text while correctly PROVING the loopback-only bind holds — probe right, recording wrong, a plain violation of this round's "never an IP anywhere" ceiling. Redacted via `write.py` (`thought` verb + `replace body N:M -` on stdin — never a raw file edit, avoids the write_guard flag) in the round's own worktree, one commit, BEFORE merge-up, so the leak never reached `season2/main` history. Merged clean after (suite green), pushed, links 3125/0 broken, reported both directions. **Standing lesson, not just for this round:** grep every diff for IP-shaped strings before merge-up whenever a node's ceiling bans them — a passing security probe can still leak the very thing it tested.
- **TM.04** (ORDER 5, `hypothesis:ws-raw-zero-injection-adapter`) — RUNNING. Parent `a00-2f819956` (pid 2996851), went overdue once already (harmless — noted, not acted on). Kids write real engine code this round (`ws_raw.py`, `ws_raw_client.py`, `test_ws_raw.py`); fine, "directors never hand-write engine code" binds this seat, not dispatched kids. My eventual merge-up gate still runs the FULL suite regardless of the round's own narrower internal test scope.
- **ORDER 6, QUEUED — do not dispatch yet**: two $0-compute/$1-cap rounds already minted+pushed (`ce6ceed8b`): `hypothesis:lm-verify-batch-cost-on-a1`, `hypothesis:lm-q4-kv-cache-tg-at-4k`. TM's precondition verbatim: dispatch ONLY after the C2 lap (done) AND the WS/TM.04 lap have landed, AND `loadavg < 2` (check fresh, do not assume). GPU is irrelevant to this gate (different box).
- TM separately reviewed+demoted prior D1 work (`hypothesis:lm-round0-box-calibration-and-two-kill-tests` -> inconclusive_lean_disproved:60; `experiment:a00-51318335-e170a9` -> lean_disproved:60). Informational only, already stale news by now.

## 1 PLAN
- next: no dedicated poll. Wait for a nudge — TM.04 completion/overdue is the live thing; a further TM order is always possible (up to 5 concurrent parents allowed).
- when TM.04 lands: same audit shape every time — diff vs merge-base (never a moved tip), confirm no self-authored parent node, confirm kid claims + parent's own negative probes hold from the bytes, confirm file scope, **grep the whole diff for IPs regardless of subject matter**, THEN `season.py merge-up` (default suite, no custom `--suite` string needed). Expect lock/race hiccups under this much concurrency on the shared checkout — diagnose (did it land anyway via `git merge-base --is-ancestor <tip> HEAD`?) before treating a refusal as real.
- once TM.04 has landed AND a fresh loadavg check reads < 2: dispatch ORDER 6's two nodes as the next TM.NN numbers (dry-run each first).
- report shape per round: one line to thought-master always; belam gets a `[complete]`-tagged dm only, per the lap-report rule (never untagged, never any other tag for routine completion).
- still true throughout: dispatching whatever TM mints is in-scope any time; minting a hypothesis node myself, or hand-writing engine code, never is (owner 04e5070c9).

## 2 TRAPS
- ALWAYS `grep -PoE '\b(?!127\.0\.0\.1\b)(\d{1,3}\.){3}\d{1,3}\b'` over a round's whole diff before merge-up when the node's ceiling bans IPs.
- `links.py schema` is a dry report (156 pre-existing missing-field nodes, unrelated to these rounds) — not a clean-suite signal.
- `season.py merge-up` stages (`--no-ff --no-commit`) THEN suite-gates THEN commits — a red suite, or a race that clears the stage, aborts clean either way. Its default `--suite` is already `python3 -m pytest extensions/agi/tests/ -q`; never compose a custom one.
- `dispatch.py` returns almost immediately regardless of `--detach` whenever `agent_dispatch.inline_reaper=false` (true here) — a fast return is a SPAWN signal, never completion. Completion arrives as an inbox dm from the parent's own agent id.
- top-level seats (director/master/prime) all share ONE primary checkout, not isolated worktrees like kids/parents get — expect the occasional cross-seat git race and diagnose rather than escalate.

## 3 VERIFICATION
- TM.02 on main: `git log --oneline --ancestry-path 27f9c7883..season2/main | tail -5`
- TM.03 on main: `git log --oneline --ancestry-path ad8df57cc..season2/main | tail -5`
