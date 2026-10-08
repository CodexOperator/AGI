---
id: experiment:a00-fd0b0598-b493d7
mint_id: f5e7c249936940c2becb2193ce2103f9
type: experiment
parents:
  - hypothesis:l3-write-partial-diffs-as-writes
next_edges: []
confidence: 0.7
edited_by: a00-c3ec5478
evidence_runs:
  - experiment:a00-fd0b0598-b493d7
loop: hypothesis:l3-write-partial-diffs-as-writes@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3eb1b246425552a0
season: 2
thought_session: L3.43
title: "\"patch verb lands a one-line diff through write.py, fail-closed\""
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-fd0b0598-b493d7

## Experiment

Built the `patch` verb for `write.py` (**hypothesis:l3-write-partial-diffs-as-writes**) and proved, red-first, that a one-line change to a payload now lands through the one sanctioned hand as a one-line diff instead of a whole-file re-emission. The diff vocabulary is the grid's own (`git diff` / `grid.py diff` delta), so no second patch format was invented, exactly as the owner's "piggyback off the diff system" asked.

**What was added to `extensions/agi/bin/write.py`:**

1. A `patch <path|->` verb — reads a unified diff from a file or stdin (`patch -`, copying the `payload -` precedent because a diff can contain the `&&` that splits the script form).
2. `apply_unified_diff(original, diff)` — a fail-closed in-memory applier. Every context line and every removal is checked against the payload's current bytes; the first mismatch (or a malformed hunk header, or bytes outside any hunk) raises `EditError` and returns nothing. **No partial application, ever** — a half-applied payload patch is this loop's single most expensive failure shape.
3. The patched bytes funnel through the *same* `node_writer.replace_payload` path as a whole-file `payload` verb, so `edited_by`, `thought_session` and the grid version all happen identically. write.py's own no-file-write invariant is untouched — the diff is applied in memory and handed over as `data=`. Exec-bit preservation comes free from `replace_payload`'s existing `os.chmod(dest, mode)`.
4. A ranged-read is implicit in the same resolver (`_read_payload_bytes`), returning only the payload's current bytes for the diff to apply against.

**Proven, red-first and green, against a scratch `build:scratchmod` node + payload in a throwaway project** (real CLI, real `write.py create → payload → patch`), with obs under Evidence:

- one-line change (beta `return 2` → `return 20`) via a 7-line unified diff — output byte-identical to the reference file.
- fail-closed: a mismatched hunk refused loudly (`ERR: removal mismatch at original line 5...`) and the payload checksum was byte-identical afterwards.
- malformed hunk header refused.
- exec bit (`0o755`) preserved across a successful patch.
- provenance stamped on the node (`edited_by: kid`, `thought_session: s1`).

**First attempt failed** (the red): `test_patch_*` were written against hand-rolled hunter strings missing the leading-space context prefix that real unified diffs carry, so `apply_unified_diff` correctly refused them — the dichotomy that proved the fail-closed claim.

## Evidence

Full engine suite: `python3 -m pytest extensions/agi/tests/ -q` → **2107 passed, 1 skipped** (was 2105 before the two new `test_write.py` patch tests). `test_edit_py_contains_no_file_write` still green, confirming the verb layer stayed a front end.

```text
$ write.py build:scratchmod "patch - && thought one-line change" < one.patch
updated: build:scratchmod
payload: /tmp/patchtest/lib/mod.py replaced
$ grep -A1 "def beta" lib/mod.py
    return 20
$ diff lib/mod.py modseed.txt && echo IDENTICAL
IDENTICAL
```

```text
$ write.py build:scratchmod "patch - && thought should refuse" < bad.patch
ERR: removal mismatch at original line 5: diff expects '    return ZZZ-NOT-HERE', file has '    return 20'
$ md5sum -c checksum-before.txt
lib/mod.py: OK
```

Exec preservation: `-rwxrwxr-x` before and after the successful patch.

Caveat / residual: the throwaway project had no grid commits to show the version delta itself (grid `diff`/`versions` need `grid.py init` + a branch that will accept a commit); the grid-versioning claim rests on `patch` routing through the identical `replace_payload` path the whole-file verbs use, which this repo's own 5-minute cron grid-commits.

## Agent Notes
patch verb lands a one-line diff through write.py fail-closed; one-line beta change matched reference byte-for-byte, mismatched hunk refused with file checksum-identical, exec bit preserved, provenance stamped. Full suite 2107 passed. Ranged-read surfaced only implicitly (the diff resolver), not as a named read verb, so write-by-diff proved, read-by-range left for a later round.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-c3ec5478, L3.43): verified the artifact against the code, not the report — patch verb and apply_unified_diff are present in write.py as claimed, the two test_patch_* tests exist and pass (test_write.py: 44 passed), and the fail-closed claim matches the applier design (every context/removal checked before any mutation; EditError on first mismatch). Accepted the kid verdict inconclusive_lean_proved:70 as honest: the write-by-diff half has real evidence, the read-by-range half of the parent hypothesis is explicitly NOT covered by this run, so full proved would overclaim — this lean is exactly the right shape.
<!-- THOUGHT:END -->

Parent review accepted this node at inconclusive_lean_proved:70. Evidence verified directly: patch verb + fail-closed applier present in write.py, 2 new tests green, suite green. Residual per kid: grid-version-delta shown only by path identity (no grid commits in throwaway project), and ranged read not delivered as a named verb — both left for a later round.
