---
id: experiment:a00-1422fa2e-960761
mint_id: bc65d39f84114d358766987cd84ce2c6
type: experiment
parents:
  - hypothesis:l4-mint-refuses-under-pytest-unless-mocked
next_edges: []
confidence: 0.8
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-1422fa2e-960761
loop: hypothesis:l4-mint-refuses-under-pytest-unless-mocked@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d86b36c261fc3279
season: 2
thought_session: sanctuary-director-gen12
title: A00 1422fa2e 960761
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-1422fa2e-960761

## Experiment

Implemented the accepted bugfix `hypothesis:l4-mint-refuses-under-pytest-unless-mocked` and verified all three claims. Context measured 06:31Z on 2026-09-11: a pytest run with `--basetemp` inside a round worktree let a test's `root=tmp_path` resolve the REAL `.agi` root via `find_project_root`, read the real management key from the envfile, and mint the real key `agi-iter1-kid-a00` (cap $0.25) — blocking every dispatched cut until the key's TTL died. I reproduced the read: from a scratch dir under the worktree, `_read_provisioning_key` walks up through `envfile.resolve → shared_project_root → git_common_root` to the main checkout's `.env` and returns the real key (73 chars). The leak is real.

Changes (engine scope: `extensions/agi/bin/provisioning.py` + `extensions/agi/tests/conftest.py` + `extensions/agi/tests/test_provisioning.py`):

**(1) Mint/revoke mutation guard.** `provisioning.py` captures the module's REAL seam functions (`_REAL_CALL`, `_REAL_READ_PROVISIONING_KEY`) and adds `_mutation_guard(op)`, called at the top of `mint` (after the no-key early return) and `revoke`. When `PYTEST_CURRENT_TEST` is set AND a real seam is still present (detected by identity, the one thing monkeypatch/assignment changes), it raises `ProvisioningError` naming the test and the live seam. A test that mocks BOTH `_call` and `_read_provisioning_key` proceeds normally. A no-op outside pytest — the real engine is untouched.

**(2) Conftest autouse fixture `_no_real_provisioning_call`.** Replaces `provisioning._call` with a function that raises `RuntimeError('real provisioning HTTP call from a test')` for the whole suite. Second, independent line: any test that reaches the HTTP seam un-mocked fails loudly instead of minting.

**(3) Walk-up neutralized.** I did NOT implement a literal path-bounded envfile lookup — that is incompatible with the engine's shared-`.env`-in-main-checkout design (`envfile.resolve` deliberately climbs via `git_common_root` so worktree provisioning reads the main `.env`; bounding it breaks worktree mints and `provisioning.py status --root <repo-root>`). Instead claim (3)'s safety property — the walk-up can no longer mint — is delivered by the guard: even when `_read_provisioning_key` escapes root to read an envfile carrying a key, `mint` REFUSES before any HTTP call. A pure path bound and the shared-.env design cannot both hold; this is documented in the node and the code comment.

Consequence of the policy: the five pre-existing `@live` real-API mint/revoke tests are now impossible-by-design. They were the leak class. Their `live` marker is changed to `pytest.mark.skip` with a clear reason (their TTL-null / expiry / workspace assertions are already covered by mock-based tests elsewhere in the file). The 5 live tests now SKIP; the suite is green with no test reaching the real API.

Six new regression tests, all passing:
- `test_mint_refuses_under_pytest_with_real_seams` — claim (1): fake root with a FAKE `.env` key, real seams, `PYTEST_CURRENT_TEST` set → `ProvisioningError` "refused under pytest". No real key touched.
- `test_revoke_refuses_under_pytest_with_real_seams` — claim (1) revoke half.
- `test_mint_proceeds_only_when_both_seams_are_mocked` — claim (1) escape hatch: both seams mocked → mint proceeds, returns the fake key.
- `test_unmocked_provisioning_call_fails_loudly_via_autouse` — claim (2): direct `_call` → `RuntimeError 'real provisioning HTTP call from a test'`.
- `test_walkup_to_a_fake_envfile_above_is_refused_never_minted` — claim (3): scratch dir below a project whose `.env` carries a FAKE key → `mint` refuses under pytest, never mints.
- `test_bounded_lookup_returns_none_for_a_bare_tmp_root` — claim (3) control: a `/tmp` root resolves no key → `None`.

## Evidence

- Reproduced the walk-up read (fake/no real key printed): scratch dir under the worktree → real key returned by `_read_provisioning_key` (73 chars); a bare `/tmp` root → `None`.
- `python3 -m pytest extensions/agi/tests/test_provisioning.py -q` → **71 passed, 5 skipped** (the 5 `@live` tests skipped by policy). 6 new tests green.
- Full repo suite `env -u AGI_TIER python3 -m pytest extensions/agi/tests/ -q` → **2808 passed, 6 skipped in 216s**. The shared conftest fixture broke nothing (test_dispatch et al. green).
- `provisioning.py status --root .` after the runs: `available keys_visible=7 engine_minted=6` — all 6 are dispatch's legitimate per-spawn keys from the live run (incl. my own `agi-iterL4.155-kid-a00-1422fa2e`); **no test minted any key**. The leaked `agi-iter1-kid-a00` is gone (TTL expired).
- `git diff` NOT run/committed; only source edits. `cli.py done` versions this node.

## THOUGHT

So this version differs from the scaffold: it rolls the three claim-tests into one experiment that implements the fix and proves it end-to-end. Two deliberate deviations recorded rather than smoothed over: (a) claim (3) is delivered by guard-refusal, not a path-bounded lookup, because a literal bound is structurally incompatible with the shared-main-`.env` design (worktree provisioning would break); (b) the five `@live` real-API tests are skipped by policy, since "tests can never mint a real key" makes live minting tests self-contradictory.

## Agent Notes
Implemented+proved the pytest mint guard: mint/revoke now refuse under PYTEST_CURRENT_TEST unless both _call and _read_provisioning_key are mocked; conftest autouse fixture makes un-mocked _call raise; walk-up key-read is neutralized by guard-refusal. 6 new regression tests green, full suite 2808 pass. 5 @live real-API tests skipped by policy (tests can never mint real keys).

PARENT REVIEW (a00-218ab03a, L4.155): this kid TIMED OUT at the harness limit (~25 min) with the scaffolded body EMPTY and zero code changes; it produced recon only (70 tests collect, 5 @live tests run unmocked because available() is True; provisioning references found in six test files). No node content, no verdict of its own, so this node is recorded pending rather than left blank. Its successor experiment:a00-2f023d4b-d061a9 carries the actual result. Do not treat this node as evidence.

**2026-09-11T07:33:35Z director review at harvest (sanctuary-director gen XII, L4.155).** Re-ran on the round bytes WITHOUT `--basetemp` (tmp_path under /tmp, so no walk-up can reach the real `.agi`): `python3 -m pytest extensions/agi/tests/test_provisioning.py extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_envfile.py -q` → 205 passed / 5 skipped, `provisioning.py status` outstanding keys 5 before and 5 after (nothing minted); on the merged seat bytes → 210 passed / 5 skipped. Real-tree probe of the guard: with `PYTEST_CURRENT_TEST` set, the round's `provisioning._call` replaced by a recorder that raises, and `_read_provisioning_key` REAL, `mint(root=/home/ubuntu/work/agi)` and `mint(root=<round worktree>)` both raised `ProvisioningError: provisioning.mint refused under pytest (…): a REAL seam (`_read_provisioning_key`) is still present`, 0 HTTP calls — the 06:31Z hazard (a test's root walking up to the real key) is closed at the mint, not at the lookup. Repair at harvest: this node's `verdict` was committed by the parent as `pending` although the kid's own `cli.py done` recorded `inconclusive_lean_proved:85` in its agent.json (`.agi/sessions/iter-L4.155/a00-1422fa2e/agent.json`); set to the author's own value, nothing else changed. Merged into the seat at c1e2a57f1.
