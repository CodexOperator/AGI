# FIX-ONLY round — after_join refuses an entry whose used placeholder is EMPTY

Target node: `hypothesis:l4-an-after-join-entry-whose-placeholder-resolves-empty-is-refused-by-name-and-skipped-never-run-on-the-empty-slot`

This is a **FIX-ONLY** node (a g15 build order, not a measurement). **You must IMPLEMENT the fix and test it.** A round that only reproduces the defect and reports `disproved` is not accepted.

## The defect, already measured on the current base

- The template's reap-proof entry is `ps -e -o pid=,ppid=,tty=,args= | grep -E '{pred_pids}'` (`.agi/nodes/.geometry/rotations.md` lines 69 and 111).
- `_run_after_join_command` (currently `extensions/agi/bin/rotate.py:9324`) resolves it with `_resolve_startup_placeholders(cmd, values, refuse_empty=False)` (line ~9340).
- The first_turn path refuses an EMPTY used placeholder by name (`placeholder {key} empty at spawn`, rotate.py ~8786), but after_join does not.
- Consequence: a MAIN post with no predecessor chain (`{pred_pids}` = `''`) runs `grep -E ''`, matches every line, and ~40 KB of the process table lands in the rotation record and in the successor's dm (truncated to `DEFAULT_STARTUP_BYTE_CAP` 4000 — still a wrong output, not a refusal).

## What to build

In `_run_after_join_command` ONLY (excluded from scope: `_resolve_startup_placeholders` itself, its first_turn callers, `run_after_join`'s dry-run branch reshaping, `_compose_after_join_dm`, the templates, tail/liveness, catch-up, sender):

1. An after_join entry that USES a placeholder whose value resolves EMPTY is **refused by name and never executed**. Result shape:
   `{"label": ..., "cmd": ..., "refused": "placeholder {pred_pids} empty: no predecessor chain — skipped by name"}` — no `rc`, no `output`.
   Per-placeholder reason map (at minimum): `pred_pids` → `no predecessor chain`; `succ_ref` → `row session_ref empty`; `gen` → `no generation resolved`. A placeholder with no mapped reason still refuses, naming the placeholder (do not invent a silent pass).
   Refusal text must name BOTH the placeholder and the reason, and end `— skipped by name`.
2. This is **generic to every after_join entry**, not a reap-proof special case — the ack entry with empty `{succ_ref}` refuses the same way.
3. An entry whose placeholder has a usable `fallback:` (per-entry, or the code map `_STARTUP_FALLBACKS`) resolves through the fallback instead of refusing — the same precedence first_turn uses. **Decide and state explicitly** whether you honor fallback here; if you do not, say why in the node.
4. A first seating's named value `none: first seating` is a NON-empty string and still runs (its grep matches nothing, exit 1 — expected, not a refusal).
5. The dm goes through the EXISTING refused branch of `_compose_after_join_dm` and prints `REFUSED` plus that refusal line — do not add a new dm branch.
6. State in the node what the after_join DRY-RUN path does (rotate.py ~9682 also calls resolve with `refuse_empty=False`). If you leave dry-run inconsistent, say so explicitly as a known gap; do not silently ignore it.

## Tests (required — in `extensions/agi/tests/test_after_join_service.py`)

- empty `pred_pids` → entry refused, no `rc`, no `output`, refusal names the placeholder; the dm contains `REFUSED` and the refusal line.
- non-empty `pred_pids` runs (rc present).
- the first-seating value runs and is not a refusal.
- empty `succ_ref` on the ack entry refuses by name.
- (if you honor fallback) an entry with a fallback resolves through it instead of refusing.

Run at minimum:
`python3 -m pytest extensions/agi/tests/test_after_join_service.py -q`
and report the count.

## Verdict honesty

If the tests pass and the fix is implemented, write your node with an honest verdict. `proved` requires real evidence — your experiment node IS the run. If anything is incomplete, use `inconclusive_lean_proved:N`/`pending` rather than overclaiming.

## Report

Report exactly:
```
DONE <node-id>
caveats: <one line — what is weak about the node itself>
struggles: <one line — what fought you>
```
Then run the `cli.py done` command for your own agent id. Do NOT run git.
