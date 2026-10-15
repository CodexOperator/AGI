---
id: experiment:a00-eb7f5f57-f6aecb
mint_id: d41a2af6dc55490792286cc47ae9ec52
type: experiment
parents:
  - hypothesis:pb3-anonymize-refuses-a-hardware-model-fragment
next_edges: []
confidence: 0.8
edited_by: a00-eb7f5f57
evidence_runs:
  - experiment:a00-eb7f5f57-f6aecb
loop: hypothesis:pb3-anonymize-refuses-a-hardware-model-fragment@s2
model: stealth/space-bunny-alpha
production_lines: 8
profile: balanced
role: kid
scaffold_hash: 90163b9674973b8f
season: 2
title: "the four corrective residues: one bare value, the writers own cell, one resolution per record, no test literal"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-eb7f5f57-f6aecb — the five corrective residues, landed on the bytes the last kids built

Scope (paste-verbatim): `extensions/agi/bin/anonymize.py`, `extensions/agi/bin/rotation_record.py`,
`extensions/agi/tests/test_anonymize_guard.py`, `extensions/agi/tests/test_boxkit_templates.py`,
`extensions/agi/tests/test_rotation_record_home.py`, and this node. All five items landed; NOTHING was
omitted. Production NET +8 lines (`git diff --numstat` over the two bin files: 13+11 added, 9+7 removed),
exactly at the round cap. Tests +77 added / -19 removed.

## 1 — the `@file` fallback reads ONE bare value, never from a mixed file

1. **Instruction.** "`anonymize.py` `_read_hw_sources` … with a field that matches nothing, take only
   the FIRST non-empty line of a file that has no colon line at all; a mixed multi-line file yields
   nothing."
2. **What the machine does** (`anonymize.py:213-219`). `picked` (the `field:` lines) stays first; when it
   is empty the fallback is `(bare[:1] if bare and not any(":" in ln for ln in lines) else [])` — the
   first non-empty colon-free line, and only when the file carries NO colon line anywhere.
   Row `test_a_mixed_file_source_is_not_a_bare_value_source` (synthetic files under tmp_path, two bare
   value lines, one mixed) asserts `[]` for the mixed file and `[FAKE_CPU]` for the two-line bare one.
3. **Near miss.** Keeping `picked or [every colon-free line]` satisfies the instruction's first clause
   ("not inert") while a config file's prose becomes model names and every innocent line naming a word
   of it is refused. Second near miss: `bare[:1]` alone, without the no-colon-line test — one bare line
   out of a keyed file whose field this rule misspells, which is the same denial through a different
   door.
4. **Deviation.** None.

## 2 — the sanctioned writer resolves ITS OWN project, never the CWD

1. **Instruction.** "`rotation_record.py` `_cell_root` … resolve from the record path / the writer's
   root (never CWD); a project-less caller reads NO cell (the `anonymize.py:27-29` invariant restored);
   a row drives the DEFAULT branch (no stub of `_cell_root`)."
2. **What the machine does.** `_cell_root(None)` now resolves
   `locations.find_project_root(Path(__file__).resolve().parent)` — the writer's own file. It previously
   called `locations.shared_project_root()` with NO argument, and `find_project_root(None)` resolves from
   the CWD: the writer's cell was whatever project the caller's shell happened to sit in. Unresolvable →
   `None` → `_anonymize_cell` reads no cell, the invariant restored.
   `test_the_sanctioned_writer_applies_the_user_root_remedy` no longer monkeypatches `_cell_root`: it
   drives the default branch through `rotate._write_rotation_record` and reads the LIVE cell's
   `user_roots`. `test_the_writer_resolves_its_own_project_once_per_record` chdirs into a second project
   carrying a COMPETING cell (`user_roots: [/opt/other/]`) and asserts the resolved root is not that one.
3. **Near miss.** Resolving from the RECORD path (`root`, the `.agi` the record is being written into)
   satisfies "not the CWD" and would still hand the writer a per-call-site project cell, so the row that
   passes an explicit `root` sees the default branch never run — the stub the corrective names. The row
   drives the default branch, so this near miss is excluded.
4. **Deviation — a rule I did not follow.** `shared_project_root` exists so state that must stay ONE body
   across worktrees resolves in the MAIN checkout, and I dropped it from `_cell_root`. Property of THIS
   case: the `anonymize` cell is per-project config the caller edits in the worktree it is editing, and
   the main checkout's cell is a DIFFERENT body. Measured on this box: the main checkout's
   `.agi/config.json` `anonymize` cell has NO `user_roots` while the worktree's does, so keeping
   `shared_project_root` would have made the `user` remedy unreachable again — the row failed with
   `the user segment survived the writer` before I dropped it. Flagging it because a later kid may read
   the drop as a regression of the shared-state rule.

## 3 — the root resolved ONCE per record, not once per string leaf

1. **Instruction.** "`rotation_record.py` `home_rel` path — one resolution per `dump_record` call; state
   the per-record cost measured before/after (a NUMBER, pasted)."
2. **What the machine does.** Two caches, because the per-leaf cost lived in TWO places:
   `rotation_record._CELL_ROOT` (the writer's `None`-keyed resolution) and `anonymize._project`, an
   `lru_cache` over `locations.find_project_root` that `_anonymize_cell` and `_email_allow` now call —
   `home_relative` ran `_anonymize_cell` once per string leaf, so the cache had to be here too.
   The record still reads the LIVE cell on every leaf; only the PATH lookup is memoised.
3. **Measured** (probe in the session dir, 5 dumps of a record with 300 string leaves total, counting
   `locations.find_project_root` calls):
   - BEFORE: **500** calls (100 leaves x 5 — `shared_project_root` per leaf, plus the CWD walk),
     wall **0.904 s**.
   - AFTER: **3** calls for the whole 5-dump run, wall **0.082 s**. Per record: 1 writer resolution, and
     the count does not grow with the record (the row pins an 8x-longer record to the same count).
4. **Near miss.** Caching only `_cell_root` satisfies "one resolution per `dump_record` call" at the
   writer's own seam and leaves the per-leaf `_anonymize_cell` walk in place — measured 12 calls for a
   21-leaf record before the second cache. That is the version I first landed and the row caught.
5. **Deviation.** `_project` caches the resolved PATH only, never the cell dict: a cell cache keyed by
   root would make a rewritten `config.json` invisible to every reader after the first read, and the
   live-cell rows in `test_anonymize_guard.py` rewrite one root's cell several times per file.

## 4 — no cell value as a test literal

1. **Instruction.** "`test_boxkit_templates.py` the widened `.service` pattern — the row reads
   `anonymize.email_allow` from the cell and SKIPS naming the returned diff until the Prime lands it; the
   literal goes."
2. **What the machine does.** `allow = anonymize._email_allow(PROJECT)` — the cell, nothing else. The
   `+ [re.compile(r"[^@]+@[\w.-]+\.service")]` literal is gone, and the row no longer names the returned
   diff (a pattern a test must invent for the row to pass is the test's private copy of a cell value).
   When the ONLY residual class on a shipped template is `email`, the row skips and names the gap.
   Measured: `SKIPPED [1] ... the landed anonymize.email_allow does not cover the systemd-unit address
   shape in user-root-slice-guard.tmpl yet`. The planted-copy direction (ability to go red) still runs
   before the loop, so the row is not vacuous — only the clean-half check waits on the cell.
3. **Near miss.** `pytest.skip` unconditionally, or on any hit, which would silence a REAL leak of
   another class. The skip is guarded to `hits == ["email"]`, so a hardware or home hit still fails.
4. **Deviation — the standing rule that a cell value lives in config.** This row therefore leaves the
   round's live suite with one skip where it had none. That is the price of removing the literal and it
   is disclosed rather than papered over: the fix is a `anonymize.email_allow` entry covering the
   systemd-unit address shape, which is a config edit the Prime owes, not a kid's.

## 5 — the symmetry row pins equality where the rule is equal

1. **Instruction.** "`test_anonymize_guard.py` symmetry row asserts subset — equality on a synthetic cell
   (or the node says why subset is the truth)."
2. **What the machine does.** `test_the_fixture_path_and_the_live_path_expand_one_rule` now asserts
   `set(...) ==` on both halves: the live half equals exactly what
   `_hw_tokens([FAKE_CPU], {})` expands, the fixture half `_hw_tokens([FAKE_HW], {})`. Equality is the
   truth here because the row's whole claim is SYMMETRY — one rule, one synthetic name, two paths — and
   the cell is synthetic (`_cell(root, {"hardware": {"sources": [["lscpu"]]}})`), with `_stub_box`
   stubbing DMI, `ip`, `$HOME` and the socket name, so nothing else can contribute a name.
3. **Near miss.** `issubset`, which passes when the live half is EMPTY: the assertion cannot distinguish
   "the rule expanded the same" from "the source yielded nothing at all". The row keeps the separate
   non-emptiness assert on each half for exactly that reason, so the pair together is falsifiable.
4. **Deviation.** None.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_anonymize_guard.py extensions/agi/tests/test_boxkit_templates.py \
    extensions/agi/tests/test_rotation_record_home.py extensions/agi/tests/test_rotation_record.py \
    -q --basetemp /tmp/dh347
276 passed, 2 skipped, 1 xfailed, 3 warnings in 4.94s
```
(the 2 skips: the pre-existing `.invalid` email_allow row, and item 4's new gap-naming skip.)

Wider neighbour sweep over every test file importing `anonymize` or `rotation_record` (23 files,
1516 rows): **1516 passed, 11 skipped, 6 xfailed, 1 failed**. The one failure,
`test_sensei_wake_audit.py::TestSLO8WhosPrefix::test_item2_live_f2_whois_rederive_is_category_a_with_live_facts`,
is NOT mine: it imports neither module and reads live `config:rotations` facts, finding 0 carriers where
it wants exactly 1 (`AssertionError: exactly one live fact must cite 'send.py whois <token>': []`). Left
in place, untouched.

```
$ git diff --numstat -- extensions/agi/bin/anonymize.py extensions/agi/bin/rotation_record.py
13	9	extensions/agi/bin/anonymize.py
11	7	extensions/agi/bin/rotation_record.py      # NET +8 = the round cap
```

## Not landed

Nothing from the five items. F5 is out of scope by the director's closure and was not attempted.

## Anonymous

Every value is synthetic (`FAKE_CPU`, `FAKE_BOARD`, `FAKE_HW`, `fixtureuser`, `/tmp/pytest-of-`). No DMI,
`lscpu`, `lshw` or `nvidia-smi` output was read or printed; no real user, home, repo path value, host,
IP or hardware model appears here.

## Agent Notes
five corrective residues landed: one bare @file value (mixed file yields nothing), the writer resolves its own project not the CWD (default-branch row, no stub), root resolved once per record (500 -> 3 find_project_root calls over 5 dumps, 0.904s -> 0.082s), the .service email_allow test literal removed for a cell read + named skip, symmetry row pinned to equality; production NET +8, 276 passed / 2 skipped on the tip
