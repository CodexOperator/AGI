---
id: experiment:a00-6941179b-4673c7
mint_id: abd13a823a634635bc0ddc23681c949d
type: experiment
parents:
  - hypothesis:box-memory-guard-probe-reads-back-the-table-read-only
next_edges: []
confidence: 0.85
edited_by: a00-f0f1a8b1
evidence_runs:
  - experiment:a00-6941179b-4673c7
loop: hypothesis:box-memory-guard-probe-reads-back-the-table-read-only@s2
model: stealth/space-bunny-alpha
probes:
  - "red: restoring mem_cap._read_cached_probe(cfg) makes both spy tests fail, spy names os.mkdir + os.chmod on the runtime dir; reverted byte-identical (refuted)"
  - "gate: no flag -> reserve UNKNOWN rc=3; 0.0 held -> info; MemTotal held -> DRIFT rc=1 naming reserve (derived) (refuted)"
  - "auth: planted stale-boot-id 0 and a symlinked cache dir both read None/UNKNOWN, never False (refuted)"
  - "lits: AST walk of probe.py finds every /-bearing .conf/.py literal inside FILES/UNITS (refuted)"
  - "live: probe.py --held-outside-user-mib 6656 -> EXIT=1, mem_cap row True read from the existing cache file, no dir created (refuted)"
production_lines: 52
profile: balanced
role: kid
scaffold_hash: e68bd84a2c1b600d
season: 2
title: The mem-cap row reads the cache FILE, a negative reserve is drift, and the dest literals live in one table
town: core
verdict: proved
---
# experiment:a00-6941179b-4673c7

Corrective slice of DH.439: the parent measured, on the SHIPPED bytes, that the
"read-only" probe WRITES.  All four residues are closed in
`extensions/agi/boxkit/probe.py` + `extensions/agi/tests/test_boxkit_probe.py`.

## The four closes

| # | close | how | falsified by |
|---|-------|-----|--------------|
| 1 | the probe never writes on ANY path | `probe.cached_usable(cfg)` reads the cache FILE only: same cells (`values.memcap.probe_cache_dir_name` / `probe_cache_file`, else `AGI_MEMCAP_CACHE`), same `$XDG_RUNTIME_DIR`-then-tempdir base, same trust test (`mem_cap._trusted_cache_file` = regular file, our uid) and the same boot-id check.  `mem_cap._read_cached_probe` is NOT called: it mkdirs 0700 + chmods before reading.  No mkdir, no chmod, no write, no spawn; nothing trustworthy -> `None` -> row `UNKNOWN` | `test_the_real_cached_probe_path_creates_nothing_and_reports_unknown` + `..._reads_a_planted_verdict_and_writes_nothing`, both under a recording spy on `open(w|a|x|+)` / `Path.write_text|write_bytes` / `os.mkdir` / `os.chmod`, on the REAL unmonkeypatched path |
| 2 | the LIVE cfg drives that read | `rows()` passes the same `cfg_all` it already parses into `run_usable(cfg_all)` -> `cached_usable(cfg)`; the cells choose the dir and file names | `..._reads_a_planted_verdict_...` rewrites the two cells to `capdir`/`verdict` and the row follows them |
| 3 | a NEGATIVE derived reserve is DRIFT | `res < 0` -> `DRIFT` (reaches the exit code); a healthy margin stays `info`; a MISSING input stays `UNKNOWN` with exit 3.  Row renamed `reserve (derived)` because "informational" is now false | `test_a_negative_reserve_is_drift_and_reaches_the_exit_code`: `--held-outside-user-mib MemTotal` -> rc=1 and `DRIFT: reserve (derived)` |
| 4 | ONE table of dest literals | `OOMD_DROPIN` folded into `FILES`; a comment above `FILES` names the manifest row each `dest_rel` will read when g7.33.18.1's manifest lands | `test_the_only_dest_literals_left_live_in_one_table` (AST-walks probe.py: any `*.conf`/`*.py` literal carrying a `/` must be a `FILES`/`UNITS` entry) |

## Negative probes I ran myself (read-first, then red)

1. Restore the old call -- `mem_cap._read_cached_probe(cfg)` instead of
   `cached_usable(cfg)` in `run_usable` -- and re-run the two spy tests:
   `2 failed, 1 passed`, with the spy naming the write:
   `[('os.mkdir', .../rt/capdir), ('os.chmod', .../rt/capdir)]`, and the
   empty-runtime-dir test fails because the probe CREATED `agi-memcap/`.
   Reverted byte-for-byte (`probe.py.bak` in my session dir) -> `3 passed`.
2. `test_a_cache_file_from_another_boot_is_unknown_not_false`: a planted
   `stale-boot-id 0` reads `None` (UNKNOWN), and a symlinked cache dir reads
   `None` -- a stale or redirected verdict is never a `False` that would send
   the caller down a path the box never took.
3. Whole table on an over-committed fixture: 0.0 held -> `info`; `MemTotal`
   held -> `DRIFT` + rc=1; no flag -> `UNKNOWN` + rc=3.

## Tests

    timeout 600 python3 -m pytest extensions/agi/tests/test_boxkit_probe.py \
      extensions/agi/tests/test_launch_memory_cap.py \
      extensions/agi/tests/test_mem_cap_tasks_max.py -q --basetemp=/tmp/...   -> 43 passed

(`--basetemp` under /tmp; NO `prlimit --nproc` -- the DH.439 measurement stands,
it makes 7 unrelated tests fail with EAGAIN on this box.)

## The one live read-only run (this box, once, anonymised)

    python3 extensions/agi/boxkit/probe.py --held-outside-user-mib 6656   -> EXIT=1

`reserve (derived) 1911 info info`; `mem_cap.systemd_run_usable True True ok`
-- read from the EXISTING cache file, with no directory created by this run
(`/run/user/<uid>/agi-memcap` already existed).  The three real drifts the
parents named are unchanged: `OOMPolicy streamer-stub-watch`, the absent
`agi.slice drop-in`, and `spawn.tasks_max 150 declared vs 96 resolved`
(`values.memcap.tasks_max` is still absent from the live config).
Full capture: `.agi/sessions/iter-DH.450/a00-6941179b/live-run.txt`;
`anonymize.py check` -> `ok, no box-derived physical token in 2407 bytes`.

## Ceiling

`git diff --numstat -- extensions/agi/boxkit/probe.py` -> **52 added / 12
removed** production lines (ceiling 40, 2x = 80): under the re-brief trigger,
no re-brief needed.  The 52 are the read-only cache reader (docstring
included), the negative-reserve judgement and the table comment; two of the
four residues were one-line deletions.

## Carried forward, not closed here

- The same `_private_dir` mkdir+chmod still lives in `mem_cap`'s OWN write
  path, which is correct there; the fix was to stop a read-only CALLER from
  reaching it.  A future read-only caller must use `probe.cached_usable` (or a
  sibling reader in mem_cap) -- the name is the contract.
- `values.memcap.tasks_max` and `values.boxkit.held_outside_user_mib` are
  still requested cells, still not added (.agi/config.json is off limits).

## Agent Notes
All four DH.450 residues closed: mem_cap row now reads the cache FILE (no mkdir/chmod/spawn, UNKNOWN otherwise, live cfg cells drive it), negative derived reserve is DRIFT with rc=1, all dest literals in one FILES table; 43 tests pass, red-first by restoring the old call.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW DH.450 (a00-f0f1a8b1) -- I read the BYTES the kid moved (probe.py rows/run_usable/cached_usable/FILES plus the five new tests in test_boxkit_probe.py), not its result file, and I ran 20 negative probes of my own, built independently of the kid test file (probes450.py in my session dir: throwaway install_root, fake systemctl, no real box, no claude). ACCEPTED as proved. ALL FOUR RESIDUES CLOSED.

(1) WHAT THE ORDERS SAID: "the probe must be read-only on EVERY path: read the cache file directly (no write, no spawn) or report UNKNOWN"; "pass the LIVE cfg (values.memcap.probe_cache_dir_name / probe_cache_file) instead of None"; "a NEGATIVE derived reserve is DRIFT and affects the exit code; UNKNOWN stays UNKNOWN"; "name every remaining literal in ONE module-level table with a comment naming the manifest row it will read".

(2) WHAT THE MACHINE ACTUALLY DOES, cited to bytes and to artifacts I BUILT AND RAN. My own baseline, before the spawn, on the DH.439 bytes: with XDG_RUNTIME_DIR pointed at an empty tmpdir, mem_cap._read_cached_probe(None) left a NEW 0o700 dir agi-memcap/ behind -- the write is mem_cap._private_dir -> mkdir + chmod, reached through _probe_cache_path. The hole was real and the DH.439 suite could not see it, because that suite monkeypatched the very function. After the kid, probe.cached_usable(cfg) re-implements ONLY the read half: mem_cap._cache_names(cfg) for the cells, $XDG_RUNTIME_DIR-then-tempfile.gettempdir() for the base, mem_cap._trusted_cache_file for the regular-file/our-uid test, mem_cap._boot_id() for the boot check, and nothing else; there is no mkdir, no chmod, no mkstemp, no write on that path. PROBE A/gate: an empty runtime dir stays empty with the write spy silent, and a planted "<boot-id> 1" file reads True with zero writes. PROBE B/wire: rewriting the two values.memcap cells to capdir/verdict makes the read follow them (True), and the negative control with default names misses that same file (None) -- the cells, not a literal, drive it. PROBE F/wire, through rows() rather than the helper: a verdict in the cells-named file makes the mem_cap row print ok, and a stale-boot verdict makes it UNKNOWN, never False. PROBE C/gate: --held-outside-user-mib == MemTotal -> the reserve row prints DRIFT and rc == 1 naming it; held == 0 -> the row stays informational; no flag at all -> UNKNOWN, named, non-zero exit. PROBE D/auth: six mutation verbs (set-property, restart, stop, edit, daemon-reload, --user restart) all raise ValueError naming the verb BEFORE subprocess is reached -- I replaced probe.subprocess.run with a raiser and nothing was spawned, while a read verb still goes through the same door. PROBE E/gate: over a full run install_root and the graph root are byte-identical before and after (sha256 over both trees), the verbs that reached systemctl are exactly {show, is-active}, and a spy on open(w|a|x|+) / Path.write_* / os.mkdir / os.chmod recorded ZERO writes. Residue 4: OOMD_DROPIN is gone as a module constant, its dest_rel strings live inside FILES, and a comment above FILES names the manifest swap.

(3) THE NEAR MISS, three of them, all rejected by a probe rather than by reading. (a) Calling mem_cap._read_cached_probe(cfg) with the live cfg instead of None -- a one-word change that satisfies "pass the live cfg" and loses read-only, because the write lives in _private_dir, not in the cache read. (b) Resolving the path through mem_cap._probe_cache_path(cfg): it is the engine's own resolver and looks like reuse, and it mkdirs and chmods on every call. (c) Keeping a negative reserve as "info" with a comment, which is the DH.437/DH.439 shape: it satisfies "the reserve row exists" and loses the exit code, and a substring or AST check for the word DRIFT in the source would have passed that variant.

(4) DEVIATION FROM A STANDING RULE: none. The prlimit recipe from my own orders was NOT used (DH.439 measured it failing 7 unrelated tests with EAGAIN); timeout 600 with --basetemp under /tmp, as the orders said.

MY OWN PROBES THAT FAILED FIRST FOR MY OWN REASON, recorded because a probe that fails for its own sake is not evidence: four of the first run FAILED on MY harness, not on the kid -- I had replaced probe.run with my own raiser, which deleted the very guard under test (D); I counted "--user" as a verb (E2); my own shim log opens in "a" mode and showed up in the write spy (E3); and I hashed one fixture before a run and a different fixture after (E1). The read-only row also legitimately DRIFTS on my throwaway graph (no crons node), so C3 asserts the reserve row's own state and a non-zero exit rather than rc == 3 exactly.

CAVEATS, not refutations: (1) cached_usable duplicates mem_cap's cache-path arithmetic (_cache_names, the runtime base, the trust test, the boot id) instead of sharing it, because the engine resolver WRITES; the duplication is a live drift risk if mem_cap changes its cache layout, and a shared pure resolver inside mem_cap would be the honest fix -- one line, outside this round's file scope. (2) AGI_MEMCAP_SYSTEMD_RUN still forces the row, so a forced value is a claim nobody re-verified: correct for an operator override, invisible in the read-only guarantee. (3) the reserve still depends on a flag with no config cell (DH.439 caveat, carried).
<!-- THOUGHT:END -->

PARENT REVIEW (a00-f0f1a8b1, DH.450): accepted, proved, 20 of my own negative probes recorded in this node's THOUGHT (A/gate read-only on the real cache path, B+F/wire the values.memcap cells thread through rows(), C/gate negative reserve DRIFTS rc=1, D/auth six mutation verbs refused by name with zero spawns, E/gate install_root+graph root byte-identical and only {show,is-active} reached systemctl). All four DH.450 residues closed. No demotions, no failures, one kid.
