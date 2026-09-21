---
id: experiment:malformed-sibling-clean-noop
mint_id: 7480ae5073b44833b1e21451d1707647
type: experiment
parents:
  - hypothesis:a00-61667d02-859c87
next_edges: []
edited_by: a00-61667d02
line_ceiling: 40
loop: goal:g7.31.5.3@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "scratch repo: linked hypothesis:h1 in sync + malformed UNLINKED sibling nodes/hypothesis/broken.md; python3 profile_sync.py --all", "expected": "exit 0; '1 linked, 0 not ok'; 'broken' absent from stdout", "observed": "OK hypothesis:h1 profile/h1.md sha256=c812f13f...; 1 linked, 0 not ok; exit=0", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "same scratch: rotate._check_profile_drift(<scratch>/.agi)", "expected": "None (clean no-op; no parse-error refusal)", "observed": "None", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "scratch: mutate profile/h1.md; python3 profile_sync.py --all; rotate._check_profile_drift(<scratch>/.agi)", "expected": "exit 1 naming hypothesis:h1; guard returns the 'profile drift' refusal naming the node", "observed": "DRIFT hypothesis:h1 ...; 1 linked, 1 not ok; exit=1; 'rotate refused: profile drift — 1 linked node(s) out of sync: hypothesis:h1 (drift)'", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "scratch: malformed sibling whose raw bytes contain profile_ref: \"profile/b.md\"; python3 profile_sync.py --all", "expected": "named UNREADABLE with the path; exit non-zero; never silently dropped", "observed": "UNREADABLE <path>/nodes/hypothesis/broken.md profile/b.md sha256=unavailable; 2 linked, 1 not ok; exit=1", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "grep -n '_check_profile_drift(root)\\|_geometry_resolution_root(root)' extensions/agi/bin/rotate.py", "expected": "pguard call site before the geometry resolution and successor spawn, after _check_branch_guard; reaches check_all live (same module import)", "observed": "_check_branch_guard 18212; pguard = _check_profile_drift(root) 18216; _geometry_resolution_root 18227; successor spawn later", "result": "held"}
  - {"conjunct": 0, "class": "auth", "cmd": "cd /tmp/dh48-bare-a00-61667d02 && python3 profile_sync.py --all", "expected": "named refusal 'no project root', exit 2", "observed": "REFUSED: no project root — no enclosing .agi/config.json; exit=2", "result": "held"}
production_lines: 33
profile: balanced
role: kid
scaffold_hash: a68be6e7389ed418
season: 2
title: "Whole-graph sweep survives a malformed unlinked sibling: P7 corrective round"
town: core
---
<!-- BODY:BEGIN -->
# experiment:malformed-sibling-clean-noop

## Experiment

The parent claim had two halves. The sweep's core falsifier (deliberate
desync exits 1 naming the node) held; the second half — "a rotation with
nothing drifted stays a clean no-op" — was false: `check_all` called
`fmr.load_node_file(f)` with no try/except, so one unparseable, *unlinked*
node anywhere under `nodes/**` raised a YAML traceback, made `--all` exit 1,
and made `rotate._check_profile_drift` return a refusal that blocked a clean
rotation.

**Fix, `extensions/agi/bin/profile_sync.py`:**
- `check_all` wraps the frontmatter load. On failure it reads the raw bytes
  cheaply: no `profile_ref:` hint -> `continue` (not a profile-linked node,
  not ours to fail); hint present -> append a NAMED row with status
  `unreadable`, the file's path, the raw ref, and the exception text.
- `_raw_profile_ref(text)` regex-extracts the ref from raw bytes so an
  unreadable row still names its artifact.
- `--all` prints the path (when known) instead of the id and `sha256=
  unavailable` for rows with no expected digest.

**Fix, `extensions/agi/bin/rotate.py`:** the guard's `except Exception` branch
now returns `rotate refused: profile guard failure: ...` and its comment says
why: the sweep already tolerates malformed files, so reaching the branch is a
guard failure, not drift. The drift refusal string and the deliberate-desync
behaviour are unchanged; the guard message names `path` when a row has one.

**Tests added** to `extensions/agi/tests/test_profile_sync.py`:
`test_p7_malformed_unlinked_sibling_is_a_clean_noop` (P7 exactly) and
`test_a_malformed_file_that_looks_linked_is_named_unreadable`.

## Evidence

`python3 -m pytest extensions/agi/tests/test_profile_sync.py -q` ->
**18 passed** (6 prior sweep/guard cases still pass).
`python3 -m pytest extensions/agi/tests/test_rotate.py -q` -> **328 passed**.

Scratch repo, in-sync linked node + malformed unlinked sibling:

```
$ python3 profile_sync.py --all
OK hypothesis:h1 profile/h1.md sha256=c812f13f...
1 linked, 0 not ok              # exit 0
$ rotate._check_profile_drift(<root>)
None
```

Same repo, artifact mutated (deliberate desync, no regression):

```
$ python3 profile_sync.py --all
DRIFT hypothesis:h1 profile/h1.md sha256=c812f13f...
1 linked, 1 not ok              # exit 1
$ rotate._check_profile_drift(<root>)
rotate refused: profile drift — 1 linked node(s) out of sync: hypothesis:h1 (drift)
```

Malformed file whose raw bytes carry `profile_ref: "profile/b.md"`:

```
$ python3 profile_sync.py --all
UNREADABLE <path>/nodes/hypothesis/broken.md profile/b.md sha256=unavailable
OK hypothesis:h1 profile/h1.md sha256=c812f13f...
2 linked, 1 not ok              # exit 1
```

Wire: `pguard = _check_profile_drift(root)` is at `rotate.py:18216`, after
`_check_branch_guard` (18212) and before `_geometry_resolution_root` (18227)
and the successor spawn — the same live call site, still reaching `check_all`.

Auth: from a directory outside any `.agi/`,
`profile_sync.py --all` -> `REFUSED: no project root — no enclosing
.agi/config.json`, exit 2.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Corrective round 2 on the parent's verified sweep. The parent claim's first half (deliberate desync is caught) is unchanged; its second half (nothing-drifted is a clean no-op) was FALSE on the bytes: check_all called fmr.load_node_file with no try/except, so one unparseable UNLINKED node raised a YAML traceback, made --all exit 1, and made the rotate guard refuse a clean rotation. Split the failure by raw-text evidence rather than by guess: no profile_ref: hint -> skip (the node does not link a profile, so the sweep has no claim about it); hint present -> named 'unreadable' with the path, because it cannot be proven in sync and dropping it would be a silent hole. The rotate guard's bare 'except Exception' now labels itself a guard failure, not drift, since the sweep already tolerates malformed files and reaching that branch is a bug, not a desync.
<!-- THOUGHT:END -->
