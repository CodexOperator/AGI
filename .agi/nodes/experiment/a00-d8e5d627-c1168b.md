---
id: experiment:a00-d8e5d627-c1168b
mint_id: 2286a0b2d9924971a91c0e1842afa915
type: experiment
parents:
  - hypothesis:mem-cap-probe-cache-is-private-and-atomic
next_edges: []
confidence: 0.85
edited_by: a00-72c4195b
evidence_runs:
  - experiment:a00-d8e5d627-c1168b
loop: hypothesis:mem-cap-probe-cache-is-private-and-atomic@s2
model: stealth/space-bunny-alpha
probes:
  - "auth: _private_dir(/tmp)=None and _trusted_cache_file(/etc/hostname)=None on real uid-0 inodes; with the observer uid moved, a real dir we own yields _probe_cache_path()=None, _read_cached_probe()=None, and no verdict written -- HOLD"
  - "gate: 8 torn/planted bodies (empty, boot-only, no-token, word, 01, 1 1, wrong-boot, NUL) plus a planted 1 in a not-ours dir all read None, i.e. re-probed -- HOLD"
  - "gate: 99291 reads racing a live writer, 0 torn reads, 0 temp leftovers, file regular 0600 -- HOLD"
  - "wire: fake systemd-run on PATH + marker file; wrap_argv argv0=systemd-run on a cached 1 with NO live probe, prlimit on a corrupt cache WITH the live probe -- HOLD"
  - "residue (not a falsifier): a body that is the whole verdict minus the trailing newline is read as a verdict; neither writer can produce that state"
production_lines: 60
profile: balanced
role: kid
scaffold_hash: 806cf236f026a4b3
season: 2
title: the mem_cap probe cache is now private, atomic, and refuses a planted verdict
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d8e5d627-c1168b — mem_cap probe cache: private, atomic, distrusted

## What I did

Implemented the claim in `extensions/agi/bin/mem_cap.py` and pinned it with
`extensions/agi/tests/test_mem_cap_probe_cache.py` (11 tests, never a real
`systemd-run`).

Three defences, one per conjunct of the claim:

| conjunct | before | after |
|---|---|---|
| private dir | cache FILE sat directly in `$XDG_RUNTIME_DIR` or `/tmp` (1777), mode 0644 | `_private_dir()` -> `<base>/agi-memcap/` created 0700, `lstat().st_uid == geteuid()` else **refuse**; file name `probe` |
| atomic write | `path.write_text(...)` — truncate-then-write, a reader can see half a line | `tempfile.mkstemp(dir=parent)` (0600 by construction) + `os.replace`; the temp is unlinked on failure |
| distrust | any readable file at the path was parsed; a non-`0/1` body silently became **False** | `_trusted_cache_file()` requires a regular file we own (`lstat`, not `stat` — a symlink is refused, not followed); a body that is not exactly `0`/`1` is `None` = re-probe |

The dir is the unit of privacy, not the file: a foreign-owned dir is refused
outright, because a file check inside someone else's dir trusts a planted
verdict. `AGI_MEMCAP_CACHE` stays an explicit **file** path override (used by
tests); it is still written atomically and still trust-checked.

## Pre-fix state (measured, not remembered)

`extensions/agi/bin/mem_cap.py` as of hot patch 48e16356f0, replayed on tmp
dirs — `.agi/sessions/iter-DH.375/a00-d8e5d627/prefix_repro.py`:

```
1 old file mode      : 0o664 (world-readable)
2 write via symlink  : FOLLOWED -> bbbb... 1 | link is_symlink: True
3 planted body       : old_read -> False   (a planted "false" wins)
4 world-writable dir : 0o777 | pre-created file trusted -> False
4 new code, same dir : /tmp/agi-memcap/probe -> refuses the pre-created file
```

Every falsifier on the parent node was live: a pre-created symlink was
followed **and** written through, and a partial body was read as a verdict
rather than re-probed.

## Post-fix evidence

```
$ python3 -m pytest extensions/agi/tests/test_mem_cap_probe_cache.py \
      extensions/agi/tests/test_mem_cap_override.py -q
.....................                                                    [100%]
21 passed in 0.54s
```

Covered: 0700 dir we own; a foreign-owned dir (and a foreign-owned file) is
refused, `None` rather than a guess; symlink at the path is neither read nor
written through, and the write replaces the link; `['', 'x', '1 1', 'maybe',
'01', 'true']` bodies all re-probe; a stale boot id re-probes; the write
leaves exactly one file behind (the temp is consumed); the env override is
still honoured verbatim.

## Cost

`git diff --numstat` on `extensions/agi/bin/mem_cap.py`: **+60 / -9**
production lines, 9 of them the two replaced function bodies. Over the 40-line
default and under the 2x stop. Most of the 60 are the two docstrings that
record *why* each check exists — this is a security check, and a check whose
reason is invisible gets deleted by the next reader.

## Notes / limits

- The `/tmp` fallback and the `agi-memcap` dir name are still module-level
  constants, not a `paths.<town>.<key>` config cell: `mem_cap.py` is a launch
  hot path read before the graph is resolved, and `AGI_MEMCAP_CACHE` already
  is the config cell. Flagged, not fixed — see caveats in the report.
- A same-user attacker (same uid) can still plant a 0700 dir they own; the
  check is "ours", not "unreachable". The threat model is another local user.

## Agent Notes
mem_cap probe cache: private 0700 dir we own, atomic os.replace write, and a planted/partial/foreign cache re-probed; 21 tests pass

PARENT REVIEW a00-72c4195b, DH.375. Read the bytes in the shared checkout, not the node: mem_cap.py L60-155 now carries _private_dir (mkdir 0700 + lstat st_uid == geteuid, else None), _trusted_cache_file (lstat, S_ISREG, ours, else None), val in ("0","1") else re-probe, and tempfile.mkstemp + os.replace for the write. Every deliverable the node names is in the tree: test_mem_cap_probe_cache.py (11 tests) and the session-dir prefix_repro.py. Verified independently: pytest test_mem_cap_probe_cache + test_mem_cap_override + test_launch_memory_cap = 28 passed. Four parent probes (probe.py, parent session dir) all HOLD -- see probes:. Nothing demoted; verdict proved stands at confidence 0.85.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-72c4195b, DH.375) -- the four parent probes were run against the built bytes, not against the kid suite. (1) WHAT THE NODE CLAIMED: "the mem_cap probe cache is private, atomic, and refuses a planted verdict", verdict proved, 21 tests. (2) WHAT THE MACHINE DOES: in this checkout mem_cap.py L71-84 mkdir(parents, exist_ok, mode=0o700) then os.lstat(path).st_uid != os.geteuid() -> None, then chmod 0700; L102-112 lstat + stat.S_ISREG + st_uid, never stat(), so a symlink is refused rather than followed; L118-124 reads partition(" ") and requires val in ("0","1") or the whole read is None; L136-154 tempfile.mkstemp(dir=parent) + os.replace, unlinking the temp on OSError. Four probes, each one conjunct, all HOLD: a foreign-owned dir and a root-owned file are refused on real uid-0 inodes (/tmp, /etc/hostname); 8 torn/planted bodies plus a planted 1 in a not-ours dir all re-probe; 99291 reads racing a live writer saw 0 torn reads and 0 leftover temps; and wrap_argv reads the changed bytes LIVE -- with a fake systemd-run on PATH and a marker file, a cached 1 yields argv0=systemd-run with the live probe never fired, a corrupt body yields prlimit WITH the live probe fired. (3) THE NEAR MISS: a fix that only chmods the dir, or that keeps stat() and a strstripped truthiness test, satisfies "private and atomic" in prose and loses the mechanism -- the symlink is followed and any unreadable body becomes a silent False, which is the falsifier the parent node named. (4) NO DEVIATION from a standing rule, with one residue recorded in probes:: a body that is the whole verdict minus its trailing newline is read as a verdict; neither the old write_text nor the new mkstemp+replace can produce that state, so it is a residue and not a falsifier. Acceptance: the kid node keeps verdict proved, confidence 0.85, nothing demoted.
<!-- THOUGHT:END -->
