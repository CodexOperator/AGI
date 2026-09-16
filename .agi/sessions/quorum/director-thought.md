# CARD — director-thought

## SELF-FACTS (gen1 wake-audit, master-sensei 2026-09-16T07:21Z) — handed, not fetched
- Ack grammar is F6, verbatim: `rotate.py ack --post <post> --ref <bare ref> continue|diff [--text -]`. Never grep rotate.py source for it.
- Card path is always `.agi/sessions/quorum/<post>.md` (F26). Never `find`/search for it.
- On any wake, read your own inbox FIRST (call 1) — a nudge names the reason you're awake.
- Never read another seat's rotation record (e.g. your master's) — not your concern; wait for their message instead.
- Check `git rev-parse --verify MERGE_HEAD` before ANY other git command — a `season.py merge-up` this seat launched may still be staged/suite-gating in the background, or may have already been raced clear by another seat (see TRAPS). Never commit/add anything while it is set.

## 0 STATE (2026-09-16, ~08:5xZ) — meter was ~94% of the rotation line at last write; may have rotated
Four TM orders processed under thought-master, all concurrent under the owner's 5-parent/10-kid ruling. **Three CLOSED, one queued:**

- **TM.02** (ORDER 3, `hypothesis:c2-digital-kuramoto-flip-mode`) — CLOSED, proved, 3/3 kids proved. Landed via a cross-seat git race (see TRAPS), verified post-hoc, both reports sent.
- **TM.03** (ORDER 4, `hypothesis:gpu-local-town-openai-endpoint`) — CLOSED, proved (A+B; C not required). Caught and redacted a leaked non-loopback LAN IP in the parent's own review text before merge (the probe was correct — proving loopback-only bind holds — only the recording leaked the address). Merged clean, both reports sent.
- **TM.04** (ORDER 5, `hypothesis:ws-raw-zero-injection-adapter`) — CLOSED, verdict `inconclusive_lean_proved:85` (parent's own honest call, not "proved" — it caught and named a real auth bug in Kid A, which B then fixed). No IPs, no self-authored parent node, file scope respected (one benign naming deviation: Kid C's extra probe scripts to exercise the now-live GPU endpoint from TM.03). Landed via the same cross-seat race pattern as TM.02. Both reports sent.
- **ORDER 6, QUEUED — still not dispatched**: two $0-compute/$1-cap rounds already minted+pushed (`ce6ceed8b`): `hypothesis:lm-verify-batch-cost-on-a1`, `hypothesis:lm-q4-kv-cache-tg-at-4k`. TM's precondition verbatim: dispatch only after the C2 lap (✅ done) AND the WS/TM.04 lap (✅ done as of this write) AND `loadavg < 2`. **Last measured loadavg: 2.64/2.55/3.35 — still ABOVE 2.** This is the ONLY thing blocking ORDER 6. Re-check `cat /proc/loadavg` fresh before dispatching; do not dispatch on a stale reading.
- All three closed rounds ended up landing through OTHER seats' concurrent git activity on this shared checkout rather than this seat's own `season.py merge-up` call completing cleanly (TM.03 was the one exception — that one committed directly). Every time, the content was verified present and correct post-hoc before reporting. This is now an established, understood pattern here, not a red flag each time it recurs.

## 1 PLAN
- next: re-check `cat /proc/loadavg`. The moment it reads < 2, dispatch both ORDER 6 nodes as the next two TM.NN numbers (TM.05, TM.06) — dry-run each first, same pattern as every prior order, no new pattern needed.
- no dedicated poll otherwise. Wait for a nudge — a further TM order is always possible (up to 5 concurrent parents allowed), or eventually a rotation.
- audit shape for any future round, unchanged: diff vs merge-base (never a moved tip), confirm no self-authored parent node, confirm kid claims + the parent's own negative probes hold from the bytes read directly, confirm file scope, **grep the whole diff for IP-shaped strings whenever a ceiling bans them**, THEN `season.py merge-up` (its default suite is already `python3 -m pytest extensions/agi/tests/ -q` — never compose a custom one). If merge-up refuses with "no merge to abort (MERGE_HEAD missing)", check `git merge-base --is-ancestor <branch-tip> HEAD` before retrying — it may have already landed via another seat.
- report shape per round: one line to thought-master always; belam gets a `[complete]`-tagged dm only, per the lap-report rule (never untagged, never any other tag for routine completion).
- still true throughout: dispatching whatever TM mints is in-scope any time; minting a hypothesis node myself, or hand-writing engine code, never is (owner 04e5070c9).

## 2 TRAPS
- ALWAYS `grep -PoE '\b(?!127\.0\.0\.1\b)(\d{1,3}\.){3}\d{1,3}\b'` over a round's whole diff before merge-up when the node's ceiling bans IPs — a passing security probe can still leak the very address it proves is refused (TM.03, twice).
- `links.py schema` is a dry report (156 pre-existing missing-field nodes, unrelated to these rounds) — not a clean-suite signal.
- top-level seats (director/master/prime) all share ONE primary checkout, not isolated worktrees like kids/parents get. A `season.py merge-up` here can be raced by another seat's concurrent git operation mid-suite-run — symptom: `git merge --abort` itself warns "no merge to abort (MERGE_HEAD missing)". Diagnose with `git merge-base --is-ancestor <branch-tip> HEAD` before retrying or escalating — three-for-three this session, the content had already landed safely via someone else's commit.
- `dispatch.py` returns almost immediately regardless of `--detach` whenever `agent_dispatch.inline_reaper=false` (true here) — a fast return is a SPAWN signal, never completion. Completion arrives as an inbox dm from the parent's own agent id, sometimes preceded by one harmless "overdue" nudge (still alive, still working — never cut a replacement for it).
- write.py's `thought` verb only touches the `<!-- THOUGHT:BEGIN -->` block. If the same text also appears in "## Agent Notes" (kids/parents sometimes duplicate it there), that needs its own `replace body N:M -` edit — check both when redacting anything.

## 3 VERIFICATION
- TM.02 on main: `git log --oneline --ancestry-path 27f9c7883..season2/main | tail -5`
- TM.03 on main: `git log --oneline --ancestry-path ad8df57cc..season2/main | tail -5`
- TM.04 on main: `git log --oneline --ancestry-path 173e5c560..season2/main | tail -5`
