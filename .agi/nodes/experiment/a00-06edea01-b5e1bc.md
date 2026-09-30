---
id: experiment:a00-06edea01-b5e1bc
mint_id: 4d6e1cbba8694e6182ca1d13419ab4ae
type: experiment
parents:
  - hypothesis:g133-one-resolve-old-sha-reads-pre-rewrite-ids-through-a-cell-named-map
next_edges: []
confidence: 0.8
edited_by: a00-06edea01
evidence_runs:
  - experiment:a00-06edea01-b5e1bc
loop: hypothesis:g133-one-resolve-old-sha-reads-pre-rewrite-ids-through-a-cell-named-map@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 332e2ad1a02a26d2
season: 2
title: An unreadable map is a silent miss and the WARN judges every file source
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-06edea01-b5e1bc

# g133 residue round: an unreadable map is a MISS, and the WARN reads every source

## MECHANISM, NOT WORDING

(1) WHAT THE INSTRUCTION SAID (verify, quoted): "An UNREADABLE map is not a
silent None: links.py `_map_rows` calls `p.stat()` / `read_text()` UNGUARDED
(links.py:630-638) ... GUARD BOTH — OSError/UnicodeError -> None, NOTHING
PRINTED." / "The WARN judges text the writer never reads: ... OMITS the payload;
`payload_from` / `replace_from` are read in SUBMIT, AFTER the WARN. Judge the
ADDED text of EVERY file source — payload_from, replace_from, body_patch_from,
patch_from — on create AND on edit, one WARN row per file source." / "`_MAP_CACHE`
is proved by NOTHING ... two calls read the file ONCE; a changed mtime re-reads."
/ "trim ... so this round's NET production delta (links.py + write.py together)
is <= 0 lines."

(2) WHAT THE MACHINE DOES (file:line, on the built bytes):
- links.py `_map_rows`: `p.stat()` sits in `try: key = (str(p), p.stat().st_mtime_ns)`
  / `except (OSError, ValueError): return []`; the read sits in its own
  `try: _MAP_CACHE[key] = [...]` / `except (OSError, ValueError): pass`, and the
  return is `_MAP_CACHE.get(key, [])`. An unreadable map therefore yields NO ROWS
  and caches NOTHING (the next call retries), and `resolve_old_sha` returns None.
- write.py: `_added_text` is replaced by `_added_sources(edit) -> list`, ONE
  `(kind, text)` row per SOURCE: body, thought, replace_text, payload_bytes, set
  values, the `+` lines of body_patch/patch diffs (read from the diff FILE when
  submit has not yet read it), and `payload file` (`_source_text(edit.payload_from)`).
  `_warn_home_path` iterates those rows and prints one WARN per offending kind.
  The create branch now passes `payload_from=_pay`, the same `args.payload or
  answers.get("payload")` value `create()` receives. `replace_from` is judged
  through `replace_text`, which `main()` fills via `_resolve_replace_text` BEFORE
  the WARN (write.py ~4216 vs 4252). Labels name the KIND, never the path.

(3) THE NEAR MISS: keeping the single combined `text = _added_text(edit)` and
adding `Path(edit.payload_from).read_text()` to the `parts` list. It satisfies
"judges the payload" and still loses: a write whose BODY is clean but whose
PAYLOAD FILE is home-rooted prints exactly one WARN identical to a body-carrying
one, so the operator cannot tell which source to fix, and "one WARN row per file
source" is unprovable. Second near miss: wrapping `read_text` in `try/except`
INSIDE the `if key not in _MAP_CACHE` block only — that guards the read but not
`p.stat()`, which is the call that raises first on a vanished file.

(4) DEVIATIONS: none from the standing rules. The WARN now names a KIND
("this write's payload file") instead of a path — required by the ANON rule,
since the source path is exactly the value that must never print. No map row, no
pre-rewrite id, no host path is in any test or line: `HOME` is JOINED at runtime
from two literals and the old ids are `"a"*40`.

## WHAT RAN

    python3 -m pytest extensions/agi/tests/test_resolve_old_sha.py \
      extensions/agi/tests/test_links.py extensions/agi/tests/test_write.py \
      extensions/agi/tests/test_anonymize_guard.py extensions/agi/tests/test_bin_help_smoke.py \
      -q --basetemp /tmp/dh346
    379 passed, 8 skipped, 2 xfailed, 160 warnings in 23.09s

    $ git diff --numstat -- extensions/agi/bin/links.py extensions/agi/bin/write.py \
        extensions/agi/tests/test_resolve_old_sha.py
    14	7	extensions/agi/bin/links.py
    64	71	extensions/agi/bin/write.py
    45	0	extensions/agi/tests/test_resolve_old_sha.py

Production net (links.py + write.py): (14+64) - (7+71) = 78 - 78 = 0. The four
residues are paid for INSIDE the trim: restating docstrings/comments in
`_resolve_api_root`, `create()`, the create body-file block, and two refuse-first
comment blocks were condensed; no mechanism line was removed.

## THE THREE NEW TEST ROWS (the claim, not the evidence)

- F8 `an_unreadable_map_is_a_silent_none` — a map path that EXISTS but whose
  `read_text` raises OSError: `resolve_old_sha` is None, stdout and stderr both
  empty. Falsifier for residue 1; the old bytes RAISE here.
- F9 `map_cache_reads_once_per_mtime` — two resolutions read the map once;
  `os.utime(..., ns=(0,0))` makes the third read again. Residue 3 made provable.
- F10 `every_file_source_is_judged` — create with `--payload <file carrying a home
  path>` prints exactly one WARN and still writes the node; `replace body 4:6
  <file>` on an existing node prints exactly one WARN. Residue 2; the old create
  branch printed ZERO.

Committing is the parent's: five files are edited in this worktree and uncommitted
by design (the loop owns every commit).

## Agent Notes
g133 residues closed: unreadable map -> silent None (links.py _map_rows guarded), WARN judges payload_from/replace_from on create AND edit one row per source (write.py _added_sources), _MAP_CACHE covered by F9; production net 0 lines (78/78), tests +45.
