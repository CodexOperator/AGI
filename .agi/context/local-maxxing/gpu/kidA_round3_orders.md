# ROUND 3 — `hypothesis:l4-needs-credential-is-provider-gated`

You are the ONE kid for round 3. You IMPLEMENT the fix and prove it. This is a
g15 build-order, not a measurement: reproduce-and-report is a failed round.

## WHAT THE LAST KID PRODUCED (round 2, node `experiment:a00-9d2ad822-0861fe`)

Round 2 landed the allowlist predicate and two ad-hoc pops:

- `.agi/config.json` — `harnesses.pi-local.credential = "none"` (only that row).
- `extensions/agi/bin/adapters/pi_adapter.py:316` — `needs_credential()` is now
  `return harness.get("credential") != "none"` (allowlist, default mint).
- `dispatch.py:1191-ish` — banner gate: `if issuing and adapters.needs_credential(dispatch_harness):`
- `dispatch.py:2373` — live spawn env pop: `if not adapters.needs_credential(...): spawn_env.pop(provisioning.RUNTIME_KEY_VAR, None)`
- `dispatch.py:1219` — dry-run mirror pop (same line).
- `test_adapters.py` — two predicate tests.

Round 2 verdict was **inconclusive_lean_proved:80**, NOT proved, on four named
residues (review `mur-dfef305bc` / thought-master 2026-09-16 12:0xZ):

- **R1 (the central one):** the pop covers only the MAIN spawn path. The RESTART
  seam `pi_adapter.restart` (builds `child_env(base=dict(os.environ))` around
  `pi_adapter.py:292`) has no pop, and `dispatch.py:3280` passes
  `harness=rec.get("harness_spec") or {}` — and **`harness_spec` is never
  written into the agent record** (`agent_record = {...}` at `dispatch.py:2544`
  has no such key), so restart always gets `{}`. `pi.needs_credential({})`
  returns **True** (`{}.get("credential") != "none"`), so a RESTARTED pi-local
  kid still inherits `OPENROUTER_API_KEY`. Same shape at
  `claude_code_adapter.py:855`, `copilot_cli_adapter.py:362`, `workflow.py`'s
  `_pi_env` (line ~1165), and `heal.py:2952` (uses `_scrubbed_env()` directly).
- **R2:** no regression test guards the two `dispatch.py` pop lines — deleting
  either leaves the suite green.
- **R3:** the real-kid env conjunct was proved on a controlled build of the
  dispatch functions, not on a spawned `--harness pi-local` child.
- **W1:** round 2's kid-node probe command checked `minting-per-spawn` (hyphens)
  but the real banner text is `minting per spawn` (spaces), so that probe
  likely passed vacuously.

## YOUR ORDERS (verbatim from thought-master, round 3)

1. **Move the credential-none pop INTO `child_env` of all three adapters**
   (`pi_adapter.py`, `claude_code_adapter.py`, `copilot_cli_adapter.py`) so
   every spawn path — main, restart, workflow, heal — shares ONE mechanism
   instead of two ad-hoc pops in `dispatch.py`. Read each adapter's `child_env`
   first; **the goal is one shared code path, not three separate copies of the
   same pop.**
   - Note `claude_code_adapter.needs_credential()` and
     `copilot_cli_adapter.needs_credential()` currently return `False`
     unconditionally, so the rule is a no-op drop for them today but must be
     shared so it stays true when their rows change.
   - For the RESTART path to actually reach the rule, the harness row must
     ARRIVE at `child_env` on restart. `harness_spec` is never recorded today
     (`dispatch.py:2544` + `:3280`). Make the config row reach restart — record
     `harness_spec` on the agent record so `rec.get("harness_spec")` resolves,
     or resolve the row at restart. Whatever you choose, the shared
     `child_env` rule must fire on restart.
   - Consolidate the two `dispatch.py` pop call sites (`~1219`, `~2373`) to go
     through the shared mechanism (call `child_env`, which now applies the
     rule) rather than re-implementing the pop.

2. **Tests:** the banner gate, the env pop, AND the restart env — with `Popen`
   monkeypatched so nothing spawns a real process, **no `_reap_*` involved**.
   Add tests that FAIL if either dispatch pop is removed (regression guard for
   R2). Add a restart test that asserts a `credential: "none"` row yields an
   env with no `OPENROUTER_API_KEY` while an unmarked row keeps it.

3. **ONE real `--harness pi-local` kid spawn**, with the env-keys log (NAMES
   ONLY, never values) as the proof that restart and main paths both come up
   clean. If a real spawn is impossible inside your session, say so explicitly
   and mark only that conjunct unproven — do NOT silently substitute a
   controlled build for a real spawn.

4. **Fix round 2's probe command (W1).** The real banner string is
   `minting per spawn` (SPACES). Re-verify the probe yourself against that
   exact string and record the corrected `probes:` in your experiment node.

## WHAT TO WRITE

- The engine edits.
- ONE new experiment node: `experiment:<your-agent-id>` (dispatch scaffolds
  it), `parents: [hypothesis:l4-needs-credential-is-provider-gated]`, with:
  - `probes:` a YAML list of `{conjunct, class, cmd, expected, observed, result}`
    — run by YOU, against the real banner string.
  - evidence (`evidence_runs`) pointing at the spawn/log.
  - a verdict: `proved` only if items 1-4 all land on disk; otherwise
    `inconclusive_lean_proved:N` naming exactly which item is short.
- Do NOT edit the hypothesis node's body. You may leave it alone entirely;
  the parent owns its verdict.

## FILE SCOPE (do not exceed)

`extensions/agi/bin/adapters/pi_adapter.py`,
`extensions/agi/bin/adapters/claude_code_adapter.py`,
`extensions/agi/bin/adapters/copilot_cli_adapter.py`,
`extensions/agi/bin/adapters/__init__.py` (only if that is where the shared
helper lives), `extensions/agi/bin/dispatch.py` (the pop call sites + the
harness_spec record line), the test files covering the three adapters + the
restart path, ONE kid experiment node. Nothing else.

## CEILING + SECRECY

$0.50 OpenRouter for the round's own tokens. Never print or commit an
`OPENROUTER_API_KEY` value; key NAMES only in any log. No network, no
Doppler/.env writes.
