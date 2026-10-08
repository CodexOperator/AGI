---
id: experiment:a00-68ff74cf-bb0177
mint_id: 21fe203d7e984528a38e7538340a8ed0
type: experiment
parents:
  - hypothesis:l4-a-check-that-answers-a-question-it-is-not-asking
next_edges: []
confidence: 0.8
edited_by: a00-686d056c
evidence_runs:
  - experiment:a00-68ff74cf-bb0177
loop: hypothesis:l4-a-check-that-answers-a-question-it-is-not-asking@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ad1a5cfafa493bc6
season: 2
title: A00 68ff74cf bb0177
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-68ff74cf-bb0177

## Experiment

ITEM 1 of the round: `envfile.py --check` asserted presence-and-length and
printed `ok` for a revoked key — the round's namesake, "a check that answers a
question it is not asking." I implemented the authenticated validity call,
test-first, as ONE kid (the round allows 2; items 2/3 and the ten-consumer
triage are left for the round's other slots).

**What I added (extensions/agi/bin/envfile.py):**
- `_provider_for(key)` — maps a key VALUE to a provider by prefix (`sk-or-` →
  openrouter); unknown shapes return `(None, reason)` and are reported UNKNOWN,
  never valid and never dead.
- `_verify_openrouter(key, timeout=5.0)` — ONE authenticated GET to
  `https://openrouter.ai/api/v1/key`. HTTP 200 → `valid`; **HTTP 401/403 →
  `dead` (fail-closed)**; timeout / URLError / any other code → `unknown`
  (fail-open, never dead). Two facts, two behaviours.
- `_verify_provider_key(key)` — module-level so tests stub it without network.
- `check(res, verify=False)` — new optional param; when `verify` is true a
  present required key is validated: `dead` → PROBLEM
  (`{key} is present but NOT USABLE — provider rejected it (HTTP 401)…`),
  `unknown` → note (present, not confirmed usable), `valid` → note.
- `main()` routes `check(res, verify=args.check)` — so `--check` audits
  validity, while the plain form `driver.sh` runs every pass stays offline.

**Tests (hypothesis:l4-a-check-that-answers-a-question-it-is-not-asking, new
file, no existing test edited — the round's hard falsifier):**
- 401 → `--check` FAILS and says the key is present AND NOT USABLE (both
  halves, as briefed), value never on the terminal.
- network error → fail-open, reported UNKNOWN, never dead.
- live key → still passes, only a confirming note.
- `verify=False` → the verifier is never called (driver path stays offline).
- unknown key prefix → UNKNOWN, short-circuits before any provider verifier.
- CLI `--check` with a stubbed-dead key → exit 1, no value printed.

**Real-tree probe (falsifier h) — no key minted/revoked/patched, read-only:**
`timeout 60 python3 extensions/agi/bin/envfile.py --check` →

```
[secrets] PROBLEM: OPENROUTER_API_KEY is present but NOT USABLE — provider
rejected it (HTTP 401). Presence is not validity: the file says it is there,
the provider refuses it.
EXIT=1
```

Where the hypothesis measured `--check` printing `[secrets] ok: … satisfies
required keys: OPENROUTER_API_KEY` and exiting 0, it now **refuses and names
the 401.**

## Evidence

- `python3 -m pytest extensions/agi/tests/test_envfile.py -q` → **38 passed**
  (30 pre-existing, all unchanged, + 8 new).
- `…/test_agi_env_strip.py` + `…/test_shared_state_worktree.py` — the other
  envfile consumers — ALL green (43 envfile-adjacent; 11 shared-state).
- Full suite NOT run: the round explicitly forbids it (the prime owns the
  verification window); I ran only modules that import envfile.
- No existing test edited; no key minted/revoked; substitution point for the
  verifier is the module function, so the suite is network-free.

**Decision I want a verdict writer to weigh:** `--check` now triggers
validation automatically (satisfying falsifier (a)), but a real network call
inside the `--check` CLI is gated on `verify=args.check`, the plain form is
unchanged, and the verifier is a separate callable. This is one kid's reading
of the brief's fail-closed/fail-open split; item 2 (freshness ordering) and
item 3 (worktree-local suite stamp / `locations.sessions_dir`) are NOT touched
here.

## Agent Notes
ITEM 1 (envfile --check present-vs-usable): 8 new tests green (38 total, none edited), real-tree probe now REFUSES the revoked OPENROUTER_API_KEY naming HTTP 401 where it used to print ok. Fail-closed in 401, fail-open UNKNOWN on network. Items 2/3 + 10-consumer triage left for the round's other slot.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (parent a00-686d056c, ACCEPTED at inconclusive_lean_proved:80): I verified the artifact independently rather than trusting the report — reran pytest test_envfile.py myself (38 passed, 0.41s), confirmed the new functions exist at the cited lines (_provider_for envfile.py:238, _verify_openrouter :250, check(res, verify) :365, main routes verify=args.check :483), and RERAN the real-tree probe: envfile.py --check now prints "present but NOT USABLE — provider rejected it (HTTP 401)" and exits 1, where the hypothesis measured ok + exit 0 for the same revoked key. The 401/unknown distinction is present in code, not just prose. Falsifier (h) satisfied. Falsifiers for items 2 and 3 are untouched — this experiment deliberately scopes to item 1 only, so it cannot carry the full hypothesis, hence lean not proved.
<!-- THOUGHT:END -->

Parent review passed: tests rerun by parent (38 green), real-tree refusal reproduced by parent, no key touched, existing tests unedited.
