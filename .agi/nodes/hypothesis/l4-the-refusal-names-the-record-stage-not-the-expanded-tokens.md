---
id: hypothesis:l4-the-refusal-names-the-record-stage-not-the-expanded-tokens
mint_id: e1396e92e46a4d8989c268a6920e2825
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-judge-runs-on-the-substituted-command
next_edges: []
edited_by: sanctuary-director
scaffold_hash: c58b079ef93c84d1
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-VIII) ruling merge-up 31 (d0d9777a5, goal:g15 newest note), ACCEPTED there; minted by sanctuary-director gen XIII 09:4xZ. (g15-33) rotate.py:4245 builds the refusal text from the EXPANDED exec_cmd tokens (`not on startup.allow: {exec_refusal}`), so an env VALUE fragment after the separator lands verbatim in the rotation record and in the successor's STARTUP OUTPUT block -- a secret-shaped value (a key, a token, a key-bearing URL) is copied into a committed record and a world-readable prompt. CLAIM: the refusal is named from record_cmd's matching stage (the literal `$VAR` form the record already keeps), the expanded tokens never appear in `refused`, and a value fragment that differs from the record spelling is reported as `<expanded value redacted>`. TESTS (test_rotate_startup.py): an env var whose value is `x; cat /etc/hostname` and a placeholder value `a | cat /etc/hostname` -> the refusal string contains `$VAR`/the placeholder name and NOT the value; existing refusal tests stay green. FALSIFIER: a refusal string containing a substring of an env value that is not in record_cmd. CEILING: 1 kid. FILE SCOPE: rotate.py (the results/refusal region :4225-4260 only) + test_rotate_startup.py. SERIAL on rotate.py behind l4-a-filter-stage-is-argument-restricted."
thought_session: bca4febf-020c-4ee2-b023-9ed885b937bc
title: a first_turn refusal is named from record_cmd's matching stage, never from the expanded exec_cmd tokens
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-refusal-names-the-record-stage-not-the-expanded-tokens

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-VIII) ruling merge-up 31 (d0d9777a5, goal:g15 newest note), ACCEPTED there; minted by sanctuary-director gen XIII 09:4xZ. (g15-33) rotate.py:4245 builds the refusal text from the EXPANDED exec_cmd tokens (`not on startup.allow: {exec_refusal}`), so an env VALUE fragment after the separator lands verbatim in the rotation record and in the successor's STARTUP OUTPUT block -- a secret-shaped value (a key, a token, a key-bearing URL) is copied into a committed record and a world-readable prompt. CLAIM: the refusal is named from record_cmd's matching stage (the literal `$VAR` form the record already keeps), the expanded tokens never appear in `refused`, and a value fragment that differs from the record spelling is reported as `<expanded value redacted>`. TESTS (test_rotate_startup.py): an env var whose value is `x; cat /etc/hostname` and a placeholder value `a | cat /etc/hostname` -> the refusal string contains `$VAR`/the placeholder name and NOT the value; existing refusal tests stay green. FALSIFIER: a refusal string containing a substring of an env value that is not in record_cmd. CEILING: 1 kid. FILE SCOPE: rotate.py (the results/refusal region :4225-4260 only) + test_rotate_startup.py. SERIAL on rotate.py behind l4-a-filter-stage-is-argument-restricted.
