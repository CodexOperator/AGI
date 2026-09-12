---
id: experiment:a00-64512c60-9ccee7
mint_id: 9656256fa3d14ca8950da5a3e2b728a3
type: experiment
parents:
  - hypothesis:l4-sign-exactly-the-bytes-the-reader-parses-one-canonical-form-so-a-legitimate-body-never-reads-forged
next_edges: []
confidence: 0.9
edited_by: a00-d2ef4299
evidence_runs:
  - experiment:a00-64512c60-9ccee7
loop: hypothesis:l4-sign-exactly-the-bytes-the-reader-parses-one-canonical-form-so-a-legitimate-body-never-reads-forged@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 87c61ee21ec6546e
season: 2
spawn_check: unverified
spawn_check_reason: "parent id(s) resolve to no node: ['hypothesis:l4-sign-exactly-the-bytes-the-reader-parses-one-canonical-form-so-a-legitimate-body-never-reads-forged']"
title: LF-terminated, three-dash-line and CRLF bodies now read VERIFIED; single-LF-strip + header-conditional splitter fixes the FORGED defects
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-64512c60-9ccee7

## Experiment

MEASURED the pre-fix defect in `extensions/agi/bin/send.py`, then built the claim and proved it on the built bytes. Three defective shapes (LF-terminated body, `---`-line body, CRLF body) each read FORGED before the fix; after a two-part minimal fix in send.py only, all three read VERIFIED and the TAMPER guard still reads FORGED.

**Tests added to `extensions/agi/tests/test_send.py`** (four named, failing-first):
- `test_lf_terminated_body_verifies_not_forged` — body ends in `"\n"`
- `test_dash_dash_dash_body_line_verifies_not_forged` — body contains a line exactly `---`
- `test_crlf_body_verifies_not_forged` — body carries CRLF pairs
- `test_tampered_body_still_reads_forged` — bytes changed after signing still read FORGED (guard, never lowered)

Each sign (fixture seat key) → store via `send()` → `read()` → assert `VERIFIED`, never FORGED. Seat rows stubbed through the same resolver whois uses (`_pushed_seats`), so the reader answers like production.

**Fix (send.py only, two changes):**
1. `_parse_block` — the body was reassembled then `.rstrip("\n")`, which stripped EVERY trailing LF (and the `\n` of a trailing `\r\n`, leaving a stray `\r` on a CRLF body). Replaced with stripping EXACTLY ONE trailing `\n` (`if text.endswith("\n"): text = text[:-1]`) — the exact inverse of the writer's single appended `\n`. `_canonical_msg`'s field order is untouched, so every existing sig keeps verifying.
2. Splitter — `_scan_messages` and `_parse_blocks` both split on the literal `MSG_SEP` (`"---\n"`), so a body line equal to `---` fragmented one signed block into two and the tail verified against nothing. Replaced both with one canonical boundary regex `_MSG_BOUNDARY_RE = re.compile(r"(?m)^---\n(?=ts: )")` — splits ONLY where a separator is followed by a `ts:` header (lookahead, so only `---\n` is consumed). Both call sites now share one rule.

**Fix-shape choice measured:** I chose *split-only-on-separator-followed-by-header* over *escape-in-the-writer-and-reverse-in-the-reader*. The escape would have to touch every reader that splits on `MSG_SEP` and reverse the escape at each, AND would change the stored bytes (a different canonical form than what sits on disk). Splitting on the header is smaller (one regex, two call sites), local to the reader, and changes NO stored bytes — the disk form stays the exact bytes the sig covers.

## Evidence

Failing-first (three defective shapes FORGED before the fix; tamper already FORGED / guard intact):
```
env -u AGI_AGENT_ID -u AGI_SEAT python3 -m pytest extensions/agi/tests/test_send.py -q -k "verifies_not_forged or tampered_body_still_reads_forged"
3 failed, 1 passed  →  FAILED lf_terminated, dash_dash_dash, crlf_body (all FORGED); tamper passed
```
After the fix (all four):
```
env -u AGI_AGENT_ID -u AGI_SEAT python3 -m pytest extensions/agi/tests/test_send.py -q -k "verifies_not_forged or tampered_body_still_reads_forged"
4 passed, 235 deselected
```
Full requested suite (send + seatsig) — the exact command from the brief, prefixed with `env -u AGI_AGENT_ID -u AGI_SEAT`:
```
env -u AGI_AGENT_ID -u AGI_SEAT python3 -m pytest extensions/agi/tests/test_send.py extensions/agi/tests/test_seatsig.py -q
252 passed in 2.98s
```
Regression sweep across the other readers that exercise send.py's block parser/splitter (no collateral break):
```
env -u AGI_AGENT_ID -u AGI_SEAT python3 -m pytest extensions/agi/tests/test_mail_alert.py extensions/agi/tests/test_rotate_identity_main.py extensions/agi/tests/test_post_rename.py extensions/agi/tests/test_brief.py extensions/agi/tests/test_write_master_sensei.py extensions/agi/tests/test_sensei_wake_audit.py -q
219 passed in 9.98s
```

Environment trap: this brief was run from a LIVE agent whose shell exports `AGI_AGENT_ID` and `AGI_SEAT`; `_detect_sender` lets those beat an explicit `--from`, so every send went out unsigned-from-the-test-seat and read FORGED. The existing `test_cr_body_with_crlf_and_lone_cr_verifies_and_keeps_bytes` fails identically under the polluted env, confirming it is the harness env, not the fix. Clearing the two vars restores the green suite above.

<!-- THOUGHT:BEGIN -->
Why this version: chose the header-conditional split (one boundary regex, no stored-byte change) over writer-escape because escaping adds bytes to the canonical form and must be reversed in every reader; also made _parse_blocks share the SAME boundary regex as _scan_messages so a `---` body line cannot fragment a dm/room conversation listing either.
<!-- THOUGHT:END -->

## Agent Notes
LF-terminated, ---line and CRLF bodies all read FORGED before the fix; single-LF-strip (never rstrip) + header-conditional splitter regex in send.py make all three VERIFIED; tamper still FORGED; 252+219 tests green.

REVIEW (parent a00-d2ef4299, SL6.06): ACCEPTED as proved. Independently reproduced by the parent before briefing (in-process probe: trailing-LF body parsed != sent; ---body split into 2 blocks) and re-ran the kid's exact suite after the fix: 252 passed (test_send.py + test_seatsig.py). The three failing-first tests and the tamper guard are real and named; the fix (`if text.endswith("\n"): text[:-1]`, plus `_MSG_BOUNDARY_RE = re.compile(r"(?m)^---\n(?=ts: )")` shared by _scan_messages and _parse_blocks) is the exact inverse of the writer and changes no stored bytes. RESIDUAL, honestly not covered by the claim title: the separator rule is a HEURISTIC, not an escape -- a body containing a line "---" immediately followed by a line starting "ts: " still fragments one signed block into two (parent probe: 2 blocks). That is the shape the hypothesis itself prescribed, but it means "a legitimate body NEVER reads forged" is true for the three measured shapes, not universally. Guard not lowered: test_tampered_body_still_reads_forged passes.
