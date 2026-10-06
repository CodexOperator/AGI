# AMEND — OWNER pin g5.4.1.4.4 (gate-q) — pytest ALLOWED

**Date:** 2026-10-06 · **Post:** sanctuary-master · **Against tip:** `6af015e80`  
**Via:** plan-master · **Belam confirm:** same pin

## OWNER words (verbatim)

> pytest/Python test scripts are ALLOWED (convenience + logging). Fix/waive real reds only — do NOT design toward stripping pytest or Python tests.

Belam-confirmed paraphrase (same pin): pytest = runner not ban on Python; fix/waive real failures; do NOT remove Python tests as the fix. Prime: no build / no strip.

## Binding on goal:g5.4.1.4.4

1. **pytest stays** the suite runner. Python test scripts stay. Design MUST NOT aim to strip pytest, ban Python tests, or “fix by deleting tests.”
2. **Per-row disposition** = fix the real failure (child BUILD → green) **or** explicit waive/skip of a **named** failing assert/case/file with falsifier — never remove the Python test harness or mass-delete test modules as the close.
3. **mail_alert retire lean** = suite may stop *owing* `test_mail_alert.py` while implementation remains deprecated (explicit retire/skip node) — **not** a license to strip pytest or other Python tests.
4. **Prime:** no build / no strip from this amend. DG still held until parent places build leaves.

## Falsifier addendum

Negative: any child/design that closes reds by removing pytest, banning Python tests, or deleting test scripts as the primary fix (except the explicit per-row retire/skip node for a named row with falsifier).
