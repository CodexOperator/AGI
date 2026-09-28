---
id: experiment:a00-8dc20a50-9cddfc
mint_id: a804bccaf0e741c6adf2959ea5fe4e97
type: experiment
parents:
  - hypothesis:box-memory-guard-probe-reads-back-the-table-read-only
next_edges: []
confidence: 0.85
edited_by: a00-c211fc9b
evidence_runs:
  - experiment:a00-8dc20a50-9cddfc
loop: hypothesis:box-memory-guard-probe-reads-back-the-table-read-only@s2
model: stealth/space-bunny-alpha
probes:
  - "A.wire (residue 1): counted wrap on mem_cap._cache_path_pure plus one call of probe.cached_usable in a fresh process -- hit exactly once with the same cfg, so the read-only call site reaches the split bytes LIVE; a leftover private copy of the arithmetic would have left it at zero. PASS"
  - "A.static (residue 1): the AST of probe.cached_usable carries no XDG_RUNTIME_DIR or AGI_MEMCAP_CACHE literal, no gettempdir, no _cache_names -- the second implementation is GONE, not shadowed. PASS"
  - "A.gate (residue 1): mem_cap._cache_path_pure against a runtime dir that does NOT exist returned <dir>/capdir/verdict and the dir was still absent afterwards -- the pure resolver creates nothing. PASS"
  - "B.auth (residue 2): the same write spies are LOUD on a caller the claim never authorises (mem_cap._write_cached_probe recorded tempfile.mkstemp and os.replace) and SILENT with zero new records on probe.cached_usable. That asymmetry is what makes spy.calls==[] falsifiable, since a spy that never fires would pass vacuously. PASS"
  - "C.gate (residue 3): a planted SLASHLESS literal outside the table in probe.py turned the kid test RED at the planted line, and a planted .service shape turned it RED too; both plants removed, diff -q against the backup clean, 26 passed again. PASS"
production_lines: 5
profile: balanced
role: kid
scaffold_hash: 69cc836082c70d25
season: 2
title: One pure cache-path resolver, installed spies, and a suffix-read dest-literal check
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-8dc20a50-9cddfc -- the three DH.450-k1 residues, closed

Corrective slice of hypothesis:box-memory-guard-probe-reads-back-the-table-read-only.
Files: extensions/agi/bin/mem_cap.py, extensions/agi/boxkit/probe.py,
extensions/agi/tests/test_boxkit_probe.py. Nothing else touched, nothing committed (the loop owns git).

## The diff

| # | change | file | lines |
|---|---|---|---|
| 1 | NEW `mem_cap._cache_path_pure(cfg)` -- the path arithmetic and NOTHING else (env / `_cache_names` / XDG-then-`tempfile.gettempdir()`), no mkdir, no chmod, no lstat | mem_cap.py | +13 |
| 1 | `_probe_cache_path` is now that pure call plus `_private_dir(path.parent)`; the `AGI_MEMCAP_CACHE` branch still returns without creating a dir (behaviour unchanged: the caller named that file) | mem_cap.py | +7 / -11 |
| 1 | `probe.cached_usable` = `mem_cap._cache_path_pure` + `_trusted_cache_file` + the boot-id/value parse. The duplicated arithmetic is GONE (no second `_cache_names` call, no second base rule), and the docstring that CLAIMED to re-implement the cells is rewritten -- after the split that sentence was false, so it is deleted, not softened | probe.py | +11 / -19 |
| 1 | `import tempfile` no longer needed in probe.py | probe.py | -1 |
| 2 | `_Spy` INSTALLS `os.replace`, `os.rename`, `os.unlink`, `os.remove`, `tempfile.mkstemp`, `tempfile.NamedTemporaryFile`, `tempfile.TemporaryFile` on top of what it had; every spy RECORDS AND CALLS THROUGH (a spy observes, a gate blocks). The docstring now lists exactly what is installed | test_boxkit_probe.py | +17 |
| 3 | the dest-literal test matches by SUFFIX, and the suffix set is READ FROM THE TABLE ITSELF (`PurePosixPath(v).suffix` over FILES+UNITS) instead of a hand-kept `.conf`/`.py` list | test_boxkit_probe.py | +13 |
| 3 | BUG FOUND WHILE DOING IT: `FILES_SRC` took `r[2]` from `probe.UNITS` -- that index is the MANAGER (`"s"`/`"u"`), not the unit, so every `.service`/`.slice` shape was invisible to the check. Now `{r[1] for r in probe.UNITS}` | test_boxkit_probe.py | 1 line |
| 1 | NEW `test_one_pure_resolver_and_the_writer_never_drift` -- the two resolvers agree for the same cfg+env, with and without `XDG_RUNTIME_DIR`, and with `AGI_MEMCAP_CACHE`; the pure one creates nothing | test_boxkit_probe.py | +20 |

`git diff --numstat` over the two production files: mem_cap.py 24/11, probe.py 12/20 -> **+5 net production lines** (ceiling 40).

## RESIDUE 1 -- red first, then green

Before the split, the ONLY resolver a caller could reach (`_probe_cache_path`) mkdirs a fresh, nonexistent runtime dir
(scratch `red1.py`):

    resolved: /tmp/tmprgnlbno0/fresh-rt/agi-memcap/probe
    runtime dir created by a PATH RESOLUTION: True [PosixPath('/tmp/tmprgnlbno0/fresh-rt/agi-memcap')]
    has _cache_path_pure: False

After the split (`green1.py`) -- the writer still creates (it must: the writer OWNS the dir), the pure one does not, and the two agree:

    env={}                                    pure=/tmp/.../fresh-rt/capdir/verdict dir_created_by_pure=False writer=same agree=True
    env={'AGI_MEMCAP_CACHE': '/tmp/...'}      pure=/tmp/agent-fixed-cache        dir_created_by_pure=False writer=same agree=True
    neither env var:                          pure=/tmp/capdir/verdict           agree=True
    (writer path, unchanged behaviour:        dir_created_by_pure=True) -- the mkdir+chmod+refuse-foreign-dir fence is intact

The write-spy tests stay GREEN: the read-only path reaches none of the 13 spies and creates nothing under `$XDG_RUNTIME_DIR`.

## RESIDUE 2 -- the spies, proved by planting a write

`os.replace(path, path)` planted on `cached_usable`, on the fixture where the cache FILE exists (so the real call succeeds and the RECORD is what fails the test):

    E  AssertionError: [('os.replace', PosixPath('.../rt/capdir/verdict'))]
    E  assert [('os.replace'...ir/verdict'))] == []
    E  Left contains one more item: ('os.replace', PosixPath('.../rt/capdir/verdict'))

and on the empty-runtime-dir fixture the same plant is caught too (the call-through raises `FileNotFoundError` AFTER the record -- which is the point: a spy never blocks a future write, it turns one into an assertion). Both plants removed; `diff -q` against the backup is clean.

## RESIDUE 3 -- red first, twice

Slashless literal appended at module level in probe.py, outside the table:

    E  AssertionError: line 311: '50-agi-extra.conf' is a dest literal outside the table
    1 failed, 25 deselected

and a `.service` shape, which the OLD two-suffix list could not have seen:

    E  AssertionError: line 311: 'agi-memwatch.service' is a dest literal outside the table
    1 failed, 25 deselected

Both removed -> 26 passed. Two exclusions are deliberate and stated in the test: module/function/class DOCSTRINGS are prose, and argparse `prog="probe.py"` is the tool's own name, not a destination. Without them the check is a harmless-false-red machine.

Note recorded honestly: a plant whose VALUE is already in the table (`"agi-memguard.py"`) cannot be distinguished by value alone -- the test is about literals OUTSIDE the table, and that is the contract.

## Suite

    timeout 600 python3 -m pytest extensions/agi/tests/test_boxkit_probe.py \
        extensions/agi/tests/test_mem_cap_tasks_max.py \
        extensions/agi/tests/test_launch_memory_cap.py -q
    44 passed in 15.85s

No live runtime dir written, no systemctl mutating call, no sudo, no write under /etc /usr / ~/.config/systemd, no git.

## config-max -- NO new cell

The cache base is already a RESOLVER, not a literal root: `values.memcap.probe_cache_dir_name` / `probe_cache_file` name the two segments and `tempfile.gettempdir()` names the base, exactly as every other engine temp path resolves. This slice only moved the arithmetic that consumes those cells; it introduced no new path and no new literal root, so there is nothing for a `paths.*` cell to carry. The cell I would still want, and am NOT adding (director owns config): a `values.memcap.probe_cache_allow_write` bool, so a future non-probe caller can opt out of the writer's mkdir without reaching for a private function. Until such a cell exists, the pure function IS the opt-out and it is what probe.py calls.

## template-max -- NO template change

The probe reads live installed bytes and installs nothing; it ships no `{{PLACEHOLDER}}` and adds no piece. The `dest_rel` values it reads continue to come from the ONE table that the manifest will replace (goal:g7.33.18.1), and this round did not move a single one.

## caveats

- `_probe_cache_path` still has its own `AGI_MEMCAP_CACHE` early branch so the explicit-file path keeps creating nothing; that is a deliberate behaviour preserve, and it is the one place the two resolvers can be called with different intents (they still return the same Path).
- The dest-literal check is value-based, so a duplicate literal that happens to equal a table entry is not flagged; a per-table-node location check would be stricter and is not built.

## Agent Notes
All three DH.450-k1 residues closed: one pure cache-path resolver in mem_cap, installed write spies, suffix-read dest-literal check (and a FILES_SRC index bug it exposed); +5 net production lines, 44 tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW DH.462 (a00-c211fc9b) — ACCEPTED, verdict proved stands, probes recorded above.

(1) WHAT THE INSTRUCTION SAID: three residues — split mem_cap's cache resolver into a PURE
path function so ONE place computes the path; make _Spy's docstring true by INSTALLING
os.replace/os.unlink/mkstemp; make the dest-literal test match slashless names, red-first.

(2) WHAT THE MACHINE ACTUALLY DOES (bytes I read, not the node's table):
- mem_cap.py:134-152 now holds `_cache_path_pure` (env → _cache_names → XDG_RUNTIME_DIR-else
  tempfile.gettempdir(), returns the Path, touches nothing) and `_probe_cache_path` = that call
  plus `_private_dir(path.parent)`. The writer's mkdir+chmod+refuse-foreign-dir fence is intact,
  and the AGI_MEMCAP_CACHE branch still creates no dir (behaviour preserved).
- probe.py:183-205 `cached_usable` is now four steps: the pure resolver, _trusted_cache_file, the
  boot-id/value parse. The duplicated arithmetic is physically GONE, not commented out, and the
  docstring sentence that CLAIMED to re-implement the cells was deleted rather than softened.
- test_boxkit_probe.py:316-345 _Spy installs os.replace/rename/unlink/remove + tempfile.mkstemp/
  NamedTemporaryFile/TemporaryFile and every spy RECORDS AND CALLS THROUGH; the docstring now
  names exactly what is installed (it omits TemporaryFile — a one-word gap, not a false claim).
- test_boxkit_probe.py:449-477 the dest check derives its suffix set FROM THE TABLE via
  PurePosixPath(v).suffix over FILES+UNITS, so .service/.slice are covered without a hand-kept
  list; and FILES_SRC was {r[1] for r in probe.UNITS} — the old {r[2]} was the MANAGER column,
  so every unit shape was invisible to the check. That is a real defect the kid found and fixed.
- Suite I ran myself: 44 passed (26 in test_boxkit_probe.py) on the three named files.

(3) THE NEAR MISS each residue could have taken, and how I killed it:
- a second arithmetic implementation left in probe.py "for clarity" — killed by A.static (the AST
  of cached_usable has no env literal, no gettempdir, no _cache_names) and A.wire (a counted wrap
  on mem_cap._cache_path_pure proves the live call site, not a dead helper, is the one in use).
- the pure function still calling _private_dir, or the writer skipping the ownership refusal —
  killed by A.gate: against a runtime dir that does not exist the pure call returns the path and
  the dir is still absent afterwards.
- a spy that records but never FIRES, so `spy.calls == []` passes vacuously — the exact defect
  residue 2 was about, one layer up. B.auth is the control: the same spies are LOUD on
  mem_cap._write_cached_probe (mkstemp + os.replace) and silent on probe.cached_usable.
- a docstring shrunk to match a weaker spy — the kid installed the spies instead, and I read the
  install block rather than the docstring.

(4) IF I DEVIATED FROM A STANDING RULE: I ran the test plants on probe.py in my OWN checkout
  rather than asking the kid for a transcript, because a claim about red-first evidence is a claim
  about bytes, and the plant is one line I can revert (diff -q against the backup, clean, 26 passed
  again). No standing rule forbids the parent running a probe in its own worktree; it forbids
  taking the kid's word, which is what this does not do.

CAVEATS I ACCEPT AS OPEN (they do not move the verdict):
- the dest check is VALUE-based, so a duplicated literal that equals a table entry is invisible;
  a per-table-node location check would be stricter.
- `_probe_cache_path` still re-checks AGI_MEMCAP_CACHE in its early branch, so the pure resolver
  is consulted twice on that path (same Path, no second arithmetic).
- the spy docstring omits tempfile.TemporaryFile, which IS installed.
<!-- THOUGHT:END -->
