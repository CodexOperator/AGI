---
id: exp:grid-payload-roundtrip
mint_id: ddf2c1ef390a460c9f2f331d0d91d2bc
type: experiment
parents:
  - hyp:payload-in-node
confidence: 0.8
edited_by: season.py
evidence_runs: 1
season: 1
subgraph: false
tags:
  - g6.3
  - grid
  - stitch
thought_session: season
title: "Grid-ref payload round-trip: bytes pass everywhere, mode/symlink pass only if commit_file() is rewritten, not reused"
---
**What was run:** A throwaway sandbox repo (`git init`,
`sessions/iter-9007/kid-c/sandbox/`, never touched `refs/grid/*` in the real
`agi-tree`), seeded with 3 real engine files copied verbatim —
`extensions/agi/bin/grid.py` (664, non-exec), `extensions/agi/lib/find-root.sh`
(775, exec bit set), `extensions/agi/lib/agent-prompt.md` (non-ASCII: em
dashes, arrows, prose) — plus one synthetic symlink,
`extensions/agi/lib/find-root-link.sh -> find-root.sh` (mode 120000), because
`find /home/ubuntu/work/agi -type l` returns zero results — the engine has no
real symlinks to sample, so this case tests the mechanism, not a production
node, exactly as scoped.

For each file, two variants of grid.py's plumbing were run, committing the
*payload path itself* into its own ref (`refs/grid/naive/<name>` /
`refs/grid/modeaware/<name>`) via `hash-object -w` → `mktree` → `commit-tree`
→ `update-ref`, mirroring `commit_file()` at
`extensions/agi/bin/grid.py:148-166`:

- **naive** — a literal transcription of `commit_file()` with `node.md`
  replaced by the real path and nothing else touched: `git hash-object -w
  str(path.resolve())`, tree line hardcoded to `"100644 blob {blob}\t{name}\n"`.
  This is what you get if `payload_ref` resolution is pointed at
  `commit_file()` as it exists today.
- **mode-aware** — same 4 plumbing primitives, but mode read via
  `os.lstat()` (100644 / 100755 / 120000) and, for symlinks, the blob content
  is the `readlink()` target text (`git hash-object -w --stdin`) instead of
  the dereferenced file — i.e. what `git add` does internally, hand-built
  from the same primitives grid.py already calls.

Each file got 3 version bumps (v1 original → v2 append a marker line
containing non-ASCII `éà中文` (symlink: retarget) → v3 same again), 3 commits
per ref per variant. Reconstruction: `naive` = `git cat-file -p
ref:name` written as a plain 0644 file (no mode info available to apply);
`mode-aware` = `git ls-tree ref -- name` for the real mode, then
`cat-file`, materializing a real symlink for 120000 and `chmod`ing 0755 for
100755. Compared by sha256 against an "old-way" baseline built by applying
the identical edits to a plain copy, never touching git. Script:
`sessions/iter-9007/kid-c/sandbox/run_experiment.py`.

**What happened:**

| file | tag | orig mode | v1→v2→v3 shas distinct | naive: bytes | naive: mode | naive: symlink | mode-aware: bytes | mode-aware: mode | mode-aware: symlink |
|---|---|---|---|---|---|---|---|---|---|
| bin/grid.py | regular | 100644 | yes (3 distinct sha256) | match | match (644=644, trivial) | n/a | match | match | n/a |
| lib/find-root.sh | exec-bit | 100755 | yes | match | **FAIL (100644)** | n/a | match | match | n/a |
| lib/agent-prompt.md | non-ascii | 100644 | yes | match | match | n/a | match | match | n/a |
| lib/find-root-link.sh | symlink (synthetic) | 120000 | yes | **FAIL — wrong content, not just wrong mode** | **FAIL (100644)** | **FAIL (materialized as regular file)** | match | match | match |

Raw v1/v2/v3 blob shas and the full sha256 table are in the script's stdout,
reproduced faithfully by re-running
`python3 sessions/iter-9007/kid-c/sandbox/run_experiment.py`. Sample: the
naive-path reconstruction of `find-root-link.sh` at the v3 tip has sha256
`1ee3aa9f...`, the old-way baseline has `dbe4c5a1...` — not a metadata
mismatch, the *bytes* differ, because `Path.resolve()` in `commit_file()`
silently follows the symlink to whatever it pointed at *at that moment* and
hashes that file's content instead of the link text. It didn't error or
warn; it committed the wrong object.

**Against the pre-registered falsifier:** 3 real files (>= 2 required),
3 version bumps each (v1→v2→v3, matching the bar exactly), all with
distinct per-version sha256 (real edits, not no-ops). Byte-identical
reconstruction passes for all 4 files under the mode-aware variant, and for
3 of 4 (all but the symlink) under the naive variant. The two required
"something a plain copy handles for free" cases were both tested by name:

- **Exec bit** — disproved under naive (silently downgraded 100755 → 100644
  on reconstruction); passed under mode-aware.
- **Symlinks** — disproved hardest under naive (not just mode: the
  reconstructed file's *content* was wrong, and it materialized as a
  regular file, not a symlink); passed under mode-aware, including 3 correct
  version bumps of the link target.

Neither variant ever fell back to reading the engine-repo disk path to fix
a wrong reconstruction — naive just produced wrong output, mode-aware never
needed to. So read at the letter of the disproof clause ("anything
`mktree`/`cat-file` can't carry that a plain copy can") — git's tree format
demonstrably *can* carry 100755 and 120000 correctly; the mode-aware run
proves that with real bytes, not an argument. The literal disproof condition
does not trigger.

**What this means for hyp:payload-in-node:** Passes, with a caveat the
hypothesis's own confidence note already flagged and this run makes
concrete. The mechanism (git plumbing: `hash-object`/`mktree`/`commit-tree`/
`update-ref`, the same four calls `commit_file()` already uses) is fully
capable of lossless round-trips — bytes, exec bit, and symlink-ness — across
real version history. But `commit_file()` as it exists today
(`extensions/agi/bin/grid.py:148-166`) is not that implementation: its
`Path.resolve()` dereferences symlinks *before* hashing (silently
substituting the wrong object, not merely dropping metadata) and its tree
line hardcodes `100644` unconditionally. Pointing `payload_ref` resolution
at `commit_file()` unmodified would reproduce the naive column above,
disproving the hypothesis on both counts the falsifier called out by name.
The hypothesis's text that this needs "no new command" is true at the
CLI-surface level (`grid commit` stays `grid commit`) but undersells the
work underneath it: `commit_file()` and any grid-reading `stitch.py --out`
both need to become mode/symlink-aware (~15-20 line change, not zero) before
this is the "no new command" story the hypothesis is telling. That's real,
unwritten, and small — not a wall, but not free either.