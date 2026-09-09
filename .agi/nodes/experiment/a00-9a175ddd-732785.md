---
id: experiment:a00-9a175ddd-732785
mint_id: bf720d1c7e5a404f93424b19ddf669e4
type: experiment
parents:
  - hypothesis:l3w4-context-load-minimal
next_edges: []
confidence: 0.7
evidence_runs:
  - experiment:a00-9a175ddd-732785
loop: hypothesis:l3w4-context-load-minimal@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 74797c05bd42f3b0
season: 2
title: A00 9a175ddd 732785
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-9a175ddd-732785

## Experiment

Implemented **move ONE** of `hypothesis:l3w4-context-load-minimal` (the parent-review slice step 3): the always-injected constitution head now carries PRAYERS ONLY, and the longer readings move to an explicit on-demand read. Did NOT touch `skills/agi/SKILL.md` or `.agi/context/INJECTION.md` (other rounds own those this iteration) — that static-prefix trim is where the 70% of TOTAL is won; this slice gets the head component.

**Changes (`extensions/agi/bin/brief.py`):**
1. `_build_head()` now emits only `## THE FOUR PRAYERS` (which already contains the project's own prayer, sourced at run time from `moral:faith`) + the Archangel Michael line, plus a short framing paragraph pointing to the on-demand read. The mantle, the decision method, words of Jesus, Tao, carried sayings, soul-mind-body and the five axes are NO LONGER injected.
2. New `readings_head(tier)` — the full pre-trim head body (per `read_order` + mantle for prime_director + decision method for director tiers) — the explicit tie-break read.
3. New CLI verb `brief.py readings --tier <tier>` (with `advisor→parent`, `liaison→director` resolution mirroring `assemble`), so a role invokes the readings deliberately instead of paying them every turn.

**Content preservation (must-not-lose):** every reading fragment is reachable on demand; all quoted prose (mantle, decision method, readings) verified byte-present in `readings_head`, still sourced from `moral:faith` at run time (no new hand-maintained duplicate). Attribution untouched.

**Tests (`test_brief.py`):** updated the 8 tests that pinned readings inside the injected head (they encoded the pre-trim contract move ONE retires) to assert the new prayers-only head + on-demand-read contract: parent, advisor, prime_director-sayings, mantle, decision-method, decision-follows-mantle, head-CLI + readings-CLI, and liaison. `test_rotate.py::test_successor_prompt_prepends_constitution_head` still passes untouched (the framing line `─── CONSTITUTION HEAD ───` is preserved, so the successor rotation shrinks too).

## Evidence

**Before → after, head component (tokens, per role; method: `_build_head` + tiktoken o200k, same as sibling baseline a00-0f527d4c):**

| role | head before | head after | head Δ | full-prompt after* | full-prompt Δ |
|---|---|---|---|---|---|
| kid | 579 | 611 | +6% | 22766 | +0.1% |
| parent | 1972 | 611 | **−69%** | 23296 | −5.5% |
| advisor | 1972 | 611 | **−69%** | 23162 | −5.5% |
| director | 2338 | 611 | **−74%** | 22963 | −7.0% |
| prime_director | 3012 | 611 | **−80%** | 23049 | −9.4% |
| liaison | 2338 | 611 | **−74%** | 22531 | −7.1% |

*Full-prompt after = sibling baseline total − (head before − head after). The head is a small fraction of the prompt, so move ONE alone cuts the TOTAL 5.5–9.4%; the owner's 70% of TOTAL needs the SKILL.md+INJECTION.md static-prefix trim (parallel rounds, 13,180+8,406 tok = 85–89% of every role).

**Head-only cut reached the range** for the two tastiest tiers: prime_director −80%, director −74%. Kid is +6% (+32 tokens absolute) because its head was already prayers-only and now carries the short on-demand pointer — a load-bearing affordance (tells a cold reader the readings exist and how to get them), negligible against its 22.8k total.

**Verification** (all green): the full readings set is byte-present in `readings_head(tier='prime_director')` (WORDS OF JESUS / TAO / CARRIED SAYINGS / SOUL MIND BODY / FIVE AXES / DECISION METHOD / MANTLE). `python3 -m pytest extensions/agi/tests/ -q` → **2202 passed, 1 skipped, 1 failed** (and the failure is environmental, not mine — see below).

**Unexpected file / pre-existing failure:** the repo root has an untracked `.env` (1868 B, Sep 7 20:19, from a prior session) holding real OpenRouter credentials. It makes `test_rotate.py::test_openrouter_key_env_file_found_via_repo_root_not_graph_root` fail — `_openrouter_key` walks up past the test's tmp_path and reads the real repo `.env` instead of the fixture key. I touched neither rotate.py nor .env; this fails identically on baseline. Left exactly as found.

**Slice discipline:** touched ONLY `brief.py` + `test_brief.py` + this node. Moves 3/4/5 and the SKILL.md/INJECTION.md trim are separate slices for other kids this iteration.

## Agent Notes
Implemented move ONE: brief.py constitution head is now PRAYERS ONLY (_build_head = four prayers + project prayer + Michael line); the long readings moved to new readings_head() behind a brief.py readings --tier verb for on-demand tie-break. Head cut per role (tiktoken o200k): parent -69%, director -74%, prime -80%, advisor -69%, liaison -74%; kid +6% (+32 tok, gains the on-demand pointer). Full-prompt impact -5.5%..-9.4% — the 70% of TOTAL needs the SKILL.md+INJECTION.md static-prefix trim (parallel rounds). All reading content byte-preserved on-demand, still sourced from moral:faith. 8 pinned tests updated to the new contract; full suite 2202 passed / 1 skipped / 1 fail (pre-existing env: real repo-root .env shadows a rotate.py fixture).
