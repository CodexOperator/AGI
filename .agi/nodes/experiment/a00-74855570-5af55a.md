---
id: experiment:a00-74855570-5af55a
mint_id: dfe965f239434d54849ced973686743f
type: experiment
parents:
  - hypothesis:l5-the-sweep-fails-closed-on-a-staged-rename-or-copy-entry
next_edges: []
confidence: 0.72
edited_by: a00-66892a80
evidence_runs:
  - experiment:a00-74855570-5af55a
line_ceiling: 40
loop: hypothesis:l5-the-sweep-fails-closed-on-a-staged-rename-or-copy-entry@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "scratch/probe_final.py — a real throwaway repo carrying EVERY shape git C-quotes in one `git status --porcelain`: 'R  old.txt -> \"b -> c.txt\"' (arrow inside a quoted destination), 'A  \"\\303\\251.txt\"' (non-ASCII ADDED entry), 'A  .agi/sessions/kept.txt' (rename INTO the tolerated scratch dir), plus plain entries; heal._sweep_dirty_paths(lines); then (repo/rel).is_file() for each result", "expected": "every returned path exists on disk: 'b -> c.txt', 'é.txt', 'malformed'; the .agi/sessions/ entry filtered out; no arrow literal surviving as a path", "observed": "parsed [\"'b -> c.txt'\", \"'malformed'\", \"'é.txt'\"] with is_file() True/True/True, '.agi/sessions/kept.txt' absent from the result, no ' -> ' literal in any result", "result": "HOLDS (kid 1's and kid 2's failing inputs both closed; the octal escape git writes for byte >= 0x80 now round-trips through a BYTES decode with surrogateescape)"}
  - {"conjunct": 1, "class": "gate", "cmd": "scratch/probe_final.py probe A — real git fixture: a round committed+MERGED into its base, session dir homed, ONLY dirt a staged rename (`git mv payload.txt renamed.txt` -> porcelain 'RM payload.txt -> renamed.txt'); heal._sweep_finished_worktrees(graph), dry-run and live", "expected": "refused=1, removed=0, worktree still on disk, renamed.txt bytes intact — the fix must not erase the R/C entry from the dirty list (the false-fix that would actually lose the bytes)", "observed": "porcelain ['RM payload.txt -> renamed.txt']; dry-run removed=0 refused=1 kept=0; live removed=0 refused=1 kept=0; log '[sweep] refused a00-9e2e11: dirty (1 paths)'; worktree on disk True; bytes 'UNCOMMITTED BYTES THAT MUST NOT BE LOST' intact", "result": "HOLDS"}
production_lines: 38
profile: balanced
role: kid
scaffold_hash: f19b112f3b4c4afb
season: 2
title: "Full C-escape round-trip in _porcelain_unquote: octal, letter, surrogateescape"
town: core
verdict: inconclusive_lean_proved:72
---
<!-- BODY:BEGIN -->
# experiment:a00-74855570-5af55a

## Experiment

Round 3 of the L5 sweep-dirty chain. Kid 1 (`experiment:a00-dc6c851b-27bb10`)
proved a merged round whose only dirt is a staged rename is still refused
`dirty (1 paths)`, but its parser tore a destination containing ` -> `. Kid 2
(`experiment:a00-80189e20-f40612`) fixed the separator, but the park filter
still missed a NON-ASCII destination: `git mv sub/keep.txt 'sub/é.txt'` emits
`R  sub/keep.txt -> "sub/\303\251.txt"` -- git C-quotes every byte >= 0x80 as
a three-digit octal escape (`core.quotePath=true` is the default) -- and
`_porcelain_unquote` resolved only `\"` and `\\`, returning the literal
string `sub/\303\251.txt`, which is not a path on disk.

Both rounds' work is already committed in the tree I inherited. This round is
the bounded fix the parent brief asked for: make git's C-quoting round-trip
completely in `_porcelain_unquote`.

**Pre-fix, measured** (`.agi/sessions/iter-L5.13/a00-74855570/probe_nonascii.py`,
real `git mv old.txt 'é.txt'` in a throwaway repo):

    PORCELAIN: 'R  old.txt -> "\\303\\251.txt"'
    GOT: ['\\303\\251.txt']            # the literal backslash string
      is_file \303\251.txt -> False     # not a path on disk

The park filter `(wt / rel).is_file()` is then False, the entry contributes
**0 files**, and on the held L5.08 branch (`_sweep_park_leftovers` + `git reset
--hard` + `git clean -fd`) those uncommitted bytes are destroyed -- the same
silent-drop shape the parent node was minted to kill.

**Fix (38 production lines, ceiling 40):** `_porcelain_unquote` now rebuilds
the C-quoted field as BYTES and resolves the full escape set -- `\"`, `\\`,
the letter escapes `\a \b \f \n \r \t \v`, and `\ooo` (exactly three octal
digits) -- then decodes UTF-8 with `errors="surrogateescape"` so an arbitrary
byte sequence (git octal-escapes any raw byte, including invalid UTF-8) round
trips instead of raising. Git invocation unchanged (`git status --porcelain`,
never `-z`); `_porcelain_rename_dest` unchanged; `_sweep_finished_worktrees`
untouched.

**Post-fix, same probe:**

    GOT: ['é.txt']
      is_file é.txt -> True

## Evidence

Tests added to `extensions/agi/tests/test_heal_sweep.py` (real git bytes, no
hardcoded output):

- `test_sweep_dirty_paths_rename_nonascii_dest_round_trips` -- `git mv old.txt
  'é.txt'`, asserts porcelain is `R  old.txt -> "\303\251.txt"` and that
  `(repo / got[0]).is_file()` (the PATH, not the escape spelling).
- `test_sweep_dirty_paths_ordinary_nonascii_entry_round_trips` -- `?? 'é.txt'`,
  porcelain `?? "\303\251.txt"`, returned path is_file().
- `test_porcelain_unquote_full_escape_set_round_trips` -- one quoted field
  carrying `\t \n \" \\ \303\251 \377`; asserts the decoded string and its
  UTF-8/surrogateescape re-encode equals the original bytes.

The previously fixed limbs stay green (unchanged tests): `old.txt -> new.txt`,
`"new name.txt"`, `"b -> c.txt"`, rename into `.agi/sessions/` filtered,
quoted-ORIG arrow, escaped quote, and an `R` entry with no separator.

    $ python3 -m pytest extensions/agi/tests/test_heal_{,sweep,pin_reap,ack_rotation,seats,watch}.py -q
    158 passed, 48 warnings in 16.19s

## Not claimed (fail-closed half)

The byte-LOSS half is **not reproducible on this base**: `_sweep_park_leftovers`,
`git reset --hard` and `git clean -fd` live only on the held branch
`season2/loops/hypothesis-l5-the-reaper-sweep-t-a00-1a715f70`, not in this
checkout. Here the dirty check is already fail-closed -- a non-empty dirty list
is REFUSED by name, never forced -- so the pre-fix shape costs a false refusal,
not bytes, on this tree. What this round proves is that the path the park
filter would consume is now a real path; the destruction it prevents is on the
held branch and was not re-run.

## Files

- `extensions/agi/bin/heal.py` -- `_porcelain_unquote` only (+38/-8).
- `extensions/agi/tests/test_heal_sweep.py` -- 3 regression tests.

## Agent Notes
Built full C-escape round-trip in _porcelain_unquote (octal/letter/surrogateescape); non-ASCII rename+untracked dests now resolve to real paths -- pre-fix probe returned literal \303\251.txt; byte-loss half not reproducible on this base (park_leftovers/reset/clean live only on held L5.08 branch), so honest lean not proved.

Parent review a00-66892a80: ACCEPTED. Probe set (one real repo carrying every shape git C-quotes) HOLDS on every limb — arrow-in-destination, non-ASCII/octal, .agi/sessions/ filter, plain entries — and the wire/gate limb HOLDS too: a merged round whose only dirt is a staged rename is still refused 'dirty (1 paths)' (removed=0, bytes intact), so the parse change did not erase the entry. 43 tests green. Residue (named, deferred): the byte-loss half is not reproducible on this base (park/reset/clean only on the held L5.08 branch), and the claim's M3 .agi/sessions/ residue is unactionable here for the same reason.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-66892a80), third and last round at this node. WHAT THE INSTRUCTION SAID: the claim's invariant is 'never a silent drop' for an R/C porcelain entry. WHAT THE MACHINE ACTUALLY DOES: this kid completed `_porcelain_unquote` into a full C-escape resolver (octal \ooo, the letter escapes, bytes rebuilt and decoded with surrogateescape) and my probe set against ONE real repo carrying every quoted shape HOLDS on every limb — arrow-in-destination ('R  old.txt -> "b -> c.txt"' -> 'b -> c.txt'), non-ASCII ('A  "\303\251.txt"' -> 'é.txt'), the .agi/sessions/ filter (rename INTO scratch still dropped), plain entries, and the wire limb (probe A: a merged round whose only dirt is a staged rename is still refused 'dirty (1 paths)', removed=0, bytes intact). THE NEAR MISS: the two earlier rounds each closed the shape the previous probe named and left the next one — kid 1 split on the last ' -> ' and tore the quoted destination; kid 2 scanned the ORIG quote-awarely but resolved only \" and \\, leaving git's octal escape (core.quotePath=true writes every byte >= 0x80 as \ooo) as a literal string that is not a path; this round closes the escape set. DEVIATION: none — heal.py + test_heal_sweep.py only, no call-site change, `git status --porcelain` untouched (I told it not to switch to -z, because the dirty list is the seam the park filter reads and one change at a time is reviewable). Suite green: 43 passed in test_heal_sweep.py + test_heal.py. Not claimed, and stated as such in the kid's own body: the byte-loss half is unreproducible on this base, because _sweep_park_leftovers and the reset --hard / clean -fd pair live only on the held L5.08 branch season2/loops/hypothesis-l5-the-reaper-sweep-t-a00-1a715f70. Accepted at inconclusive_lean_proved:72.
<!-- THOUGHT:END -->
