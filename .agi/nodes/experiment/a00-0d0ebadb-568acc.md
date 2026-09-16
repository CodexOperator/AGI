---
id: experiment:a00-0d0ebadb-568acc
mint_id: 727cdf6f86f540e18d8ce9cb652a1c08
type: experiment
parents:
  - hypothesis:l4-needs-credential-is-provider-gated
next_edges: []
confidence: 0.85
edited_by: a00-d38b9adf
evidence_runs:
  - experiment:a00-0d0ebadb-568acc
loop: hypothesis:l4-needs-credential-is-provider-gated@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 2bb89f3a68881389
season: 2
title: "needs_credential is provider-gated: pi-local mints no OpenRouter key (built + proved)"
town: local-maxxing
verdict: inconclusive_lean_proved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-0d0ebadb-568acc

## Claim tested
`hypothesis:l4-needs-credential-is-provider-gated` — gate `needs_credential` on
the resolved provider, so a `--harness pi-local` spawn (provider `local-town`,
cost 0) mints no OpenRouter key, while `--harness pi` (provider `openrouter`)
still mints exactly as before.

## Step 0 — the defect, measured before the fix
The pre-fix dry-run printed the minting line for a local harness:

```
$ python3 extensions/agi/bin/dispatch.py . TM.06 --dry-run --harness pi-local --tier kid
credentials: minting per spawn, limit=$1.5 ttl=180min workspace=72750376-...
[dry-run] slot=0 harness=pi-local tier=kid ... command: .../pi --provider local-town --model Qwen3.5-9B-Q4_K_M ...
```

`adapters/pi_adapter.py:316 needs_credential` returned `True` unconditionally,
and `dispatch.py:1911` printed the announcement behind `if issuing:` alone —
provisioning availability, with no harness predicate. So the line said a key
would be issued for a harness whose endpoint never sees one.

## Step 1 — the fix (two provider-gated sites, one predicate)

**`extensions/agi/bin/adapters/pi_adapter.py` — `needs_credential` (the claim's
one-liner, now 5 lines of predicate + docstring):**

```python
provider = harness.get("provider")
if provider is None or provider == "":
    return True
return provider == "openrouter"
```

Absent/None/empty stays `True` on purpose: the legacy `agent_dispatch`
synthesis carries no `provider` key and IS OpenRouter by default, and
`test_provisioning.py::test_pi_harness_needs_a_credential` calls
`needs_credential({"adapter": "pi"})` and must stay green.

**`extensions/agi/bin/dispatch.py:1911` — DEVIATION FROM STATED FILE SCOPE.**
The claim's falsifier is *"the dry run still prints 'minting per spawn' for
pi-local"*, and that print is the only observable a `--dry-run` can produce
(no key is ever minted in a dry run). The announcement was gated on `issuing`
alone — the same ungated site the claim names. It is now gated on the SAME
predicate the mint itself is:

```python
if issuing and adapters.needs_credential(dispatch_harness):
```

One line changed; no other dispatch behaviour touched. Recorded here because
the hypothesis's `file_scope` names only `pi_adapter.py`: without this line the
falsifier could not be cleared by any amount of correct work in `pi_adapter.py`.

**`extensions/agi/tests/test_adapters.py` — one test,**
`test_pi_needs_credential_only_when_the_provider_is_openrouter`, covering the
absent/None/empty case, `openrouter` -> True, and `local-town` -> False.

## Step 2 — proof on the built bytes

`--harness pi-local --tier kid`, POST-fix:

```
=== POST-FIX dry-run: --harness pi-local --tier kid (falsifier: NO minting line) ===
...
[dry-run] slot=0 harness=pi-local tier=kid ... command: /home/ubuntu/.npm-global/bin/pi --provider local-town --model Qwen3.5-9B-Q4_K_M ...
  env: AGI_TIER=kid ... AGI_MODEL=Qwen3.5-9B-Q4_K_M ... (no OPENROUTER_API_KEY key name emitted)
dry-run: nothing spawned, nothing written, no budget slot taken
```

No `credentials: minting per spawn` line in the pi-local section.

`--harness pi --tier kid`, POST-fix — the openrouter path is unchanged:

```
=== POST-FIX dry-run: --harness pi --tier kid (openrouter, must still mint) ===
credentials: minting per spawn, limit=$1.5 ttl=180min workspace=72750376-2d45-452e-8273-197fdaabae95
```

Both sections are in `.agi/context/local-maxxing/gpu/kidA_round2_dryrun.log`
(the two runs side by side, one file, as the brief asked).

## Step 3 — key-name evidence (names only, never values)
`.agi/context/local-maxxing/gpu/kidA_round2_env_keys.log`, evaluated against the
LIVE `.agi/config.json` rows (not a copied list):

| harness | adapter | provider | needs_credential | `spawn_env[OPENROUTER_API_KEY]` |
|---|---|---|---|---|
| `pi-local` | `pi` | `local-town` | `False` | ABSENT (no key minted) |
| `pi` | `pi` | `openrouter` | `True` | SET (minted) |

`provisioning.RUNTIME_KEY_VAR` is the name dispatch injects on a mint, read from
live code. **No REAL pi-local spawn was performed** — the round's budget is $1
and a real spawn costs a paid model call. The names above are what `dispatch.py`
would export; the dry-run `env:` lines list only static vars, because dispatch
never prints the secret.

`.agi/context/local-maxxing/gpu/kidA_round2_provisioning_delta.txt`: a
`provisioning.py status` snapshot before and after the two dry-runs. `keys_visible`
(8) and `engine_minted` (7) are identical; the only diff is the `used=` float
on already-outstanding keys, which the OpenRouter API moves on its own. No key
was minted or revoked by either dry-run.

## Step 4 — tests, each file alone

```
$ python3 -m pytest extensions/agi/tests/test_adapters.py -q
34 passed in 0.16s

$ python3 -m pytest extensions/agi/tests/test_provisioning.py -q
75 passed, 5 skipped in 0.53s

$ python3 -m pytest extensions/agi/tests/test_dispatch.py -q
121 passed, 2 warnings in 7.24s
```

`test_dispatch.py` is included although the claim names only the first two:
`dispatch.py` was edited, and `test_dispatch.py:712`
`test_the_mint_call_is_guarded_by_needs_credential` is the assertion that
watches that gate.

## Evidence

- `.agi/context/local-maxxing/gpu/kidA_round2_dryrun.log` — both harnesses,
  post-fix; pi-local minting line absent, pi minting line present.
- `.agi/context/local-maxxing/gpu/kidA_round2_env_keys.log` — key NAMES only,
  live config rows, per-harness predicate result, plus the explicit note that
  no real spawn was run.
- `.agi/context/local-maxxing/gpu/kidA_round2_provisioning_delta.txt` — status
  before/after, byte-diff showing no key minted.
- Test runs above, each file run alone.

## What this does not prove

The second half of the hypothesis's falsifier — *"a REAL pi-local kid's env
carries no OPENROUTER key"* — is proved only at the predicate level
(`dispatch.py:2427` evaluates `needs_credential(dispatch_harness)` before
`provisioning.mint`, and the same harness dict reaches both the print and the
mint). A real pi-local spawn with a `env | grep OPENROUTER` readback would close
it and was not run under the $1 ceiling.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, TM.06: I did not take the kid's proved at face value. Read the bytes: needs_credential returns True for absent/None/empty or openrouter, False otherwise; dispatch.py:1911 announcement now gated on the same predicate. Ran my own probes: the gate predicate directly, both dry-runs, and -- the one the kid could not run -- a REAL pi-local spawn. That last probe falsified the claim's env conjunct: the child env carries OPENROUTER_API_KEY, inherited from the parent, not minted. The kid was candid that it substituted dry-run names for a real spawn; that gap is exactly where the claim broke. I demoted proved->inconclusive_lean_proved:65 rather than the mechanical lean_disproved because the built behaviour is correct and the failing conjunct is a non-discriminating test (env presence is true with and without the fix); the probe is named so it cannot ride.
<!-- THOUGHT:END -->

## Agent Notes
needs_credential now provider-gated (pi_adapter.py) AND the dispatch.py:1911 minting announcement gated on the same predicate; dry-run pi-local prints no minting line, pi still does; test_adapters/test_provisioning/test_dispatch pass each alone

PARENT REVIEW (TM.06 a00-d38b9adf): fix built and holds -- needs_credential is provider-gated in pi_adapter.py, and the dispatch.py:1911 minting announcement is gated on the same predicate (a necessary deviation beyond the stated file_scope; without it the dry-run falsifier could not clear). Gate probe: needs_credential({"provider":"local-town"})==False, absent/openrouter==True. Wire probe: dry-run pi-local prints no minting line, dry-run pi does. Auth probe: openrouter path mints unchanged. BUT conjunct 2 is FALSIFIED by a real spawn: a pi-local kid (a00-587bb508) DOES carry OPENROUTER_API_KEY in /proc/<pid>/environ -- inherited from the parent (hash == parent lease key_hash), not minted; its own lease has no key_hash and engine_minted stayed 5. So env presence is non-discriminating and the clause is false before and after the fix. Verdict set lean_proved not lean_disproved because the built behaviour is correct and the failed clause is a broken test, not broken code; probe named here so it cannot ride.
