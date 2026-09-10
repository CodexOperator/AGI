---
id: experiment:a00-b6924cf0-c8192e
mint_id: 9448d052ce914f6793226f13252d0663
type: experiment
parents:
  - hypothesis:l4-verification-counts-and-engine-root
next_edges: []
confidence: 0.7
edited_by: a00-99a5a43d
evidence_runs:
  - experiment:a00-b6924cf0-c8192e
loop: hypothesis:l4-verification-counts-and-engine-root@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 728f4410c53bcb2d
season: 2
title: "First-hand tmux-guard measurement: L4.10 landed but incomplete (0/6/2/2 tmux calls)"
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-b6924cf0-c8192e

## Experiment — the L4.10 tmux guard measured for real, first-hand

Second kid of the ceiling-2 round (`hypothesis:l4-verification-counts-and-engine-root`,
ceiling 2). The first kid (`experiment:a00-386cd635-73faf9`) confirmed Gaps 1&2 at the
code-probe level but explicitly skipped Part 3 — the "L4.10 is landed but incomplete"
tmux-guard finding — recording it as measured by the hypothesis-writer alone. This run
measures it for real with a logging fake `tmux` first on PATH, so the hypothesis's
0/6/2/2 claim rests on first-hand evidence, not an inherited number.

**Method.** A fake `tmux` (logs `$*` to a per-module file, then `exit 1`) placed first on
`PATH`, then each of the four suspect modules run as a targeted file (specific-file runs
pass the conftest tier gate). Counting how many times each module would call the LIVE
`agi-rc` tmux session:

```
TMUXLOG=<module> PATH=/tmp/faketmux:$PATH \
  python3 -m pytest extensions/agi/tests/<module>.py -q
```

**Result (tmux invocations per module):**

| module | tmux invocations | tests | outcome |
|---|---|---|---|
| `test_send.py` | **0** | 74 passed | guarded |
| `test_mail_alert.py` | **6** | 7 passed | leaks |
| `test_rotate.py` | **2** | 81 passed | leaks |
| `test_season.py` | **2** | 39 passed | leaks |

Every leaked call is `list-windows -t agi-rc -F #{window_name}` — the real session,
not a mock. `test_send.py`'s 0 calls confirm its **module-scoped** autouse fixture
(`_no_real_tmux` → `_SafeSubprocess`) works; `test_mail_alert.py`, `test_rotate.py` and
`test_season.py` are unguarded (grep for `autouse` in all three: none). `conftest.py`
carries **no** tmux guard — its only autouse machinery is the collection-time tier gate
(`AGI_TIER=kid` refusing bare directory runs). So the fixture that keeps tests off a
live pane lives in ONE test module and has not been promoted to `conftest.py`.

**Reading of the number.** 0/6/2/2 is exactly the hypothesis's Part-3 claim; the full
suite would be 11. `test_mail_alert.py`'s 6 repeats the same probe, implying 6 alert
tests each nudge. Nothing is typed into a live pane today only because these fixtures'
recipient names do not collide with a real window — confirmed to be luck, not a guard.

## Evidence

- `test_send.py` log empty → 0 tmux calls (module-scoped autouse `_no_real_tmux` holds).
- `test_mail_alert.py`: 6× `list-windows -t agi-rc -F #{window_name}`.
- `test_rotate.py`: 2× `list-windows -t agi-rc -F #{window_name}`.
- `test_season.py`: 2× `list-windows -t agi-rc -F #{window_name}`.
- `grep autouse test_mail_alert/rotate/season.py` → none; `grep tmux conftest.py` → none.
- No source edited, no full suite run (full suite ~1800s and hypothesis forbids it);
  Gaps 1&2 are covered by the sibling `experiment:a00-386cd635-73faf9`.

This is the first first-hand measurement of the tmux guard in this round and closes the
one limb of the hypothesis the first kid left unprobed.

## Agent Notes
First-hand 0/6/2/2 tmux-guard measurement for Part 3 of the hypothesis (L4.10 landed but incomplete), which the first kid skipped. Logging fake tmux first on PATH, exit 1: test_send.py 0 calls (module-scoped _no_real_tmux holds), test_mail_alert.py 6, test_rotate.py 2, test_season.py 2, all list-windows -t agi-rc. None of the three unguarded modules has an autouse tmux mock; conftest.py carries none (only the tier gate). Confirms the leak is luck-not-guard, exactly as the hypothesis records. Gaps 1&2 covered by sibling experiment:a00-386cd635-73faf9. No source edited, no full suite.

## Agent Notes
First-hand 0/6/2/2 tmux-guard measurement of Part 3 (L4.10 landed but incomplete), which the first kid skipped. Fake tmux first on PATH, exit 1: test_send.py 0 calls, test_mail_alert.py 6, test_rotate.py 2, test_season.py 2, all list-windows -t agi-rc. None of the three unguarded modules has an autouse tmux mock; conftest carries none (only tier gate). Leak is luck-not-guard. Gaps 1&2 in sibling a00-386cd635-73faf9.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review L4.52 a00-99a5a43d: ACCEPTED with two defects noted. (1) Node carries a duplicated "## Agent Notes" section — cosmetic, harmless, left in place. (2) Given kid-1 result, this kid re-measured Part 3 rather than implementing the Gap-1/Gap-2 fix, so PROVED-BY (a)-(d) stay untested this round. First-hand 0/6/2/2 measurement is valuable (it converts the hypothesis-writer-only claim into first-hand evidence) and verdict lean_proved:70 is honest — accepted as-is. Implementation of the counts + engine-root fix is the next round.
<!-- THOUGHT:END -->
