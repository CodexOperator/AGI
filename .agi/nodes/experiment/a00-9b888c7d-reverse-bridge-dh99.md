---
id: experiment:a00-9b888c7d-reverse-bridge-dh99
mint_id: 729a116f18aa0adcca95a8ccbb5f72a6
type: experiment
parents:
  - hypothesis:a00-ce81c047-f9185d
next_edges: []
confidence: 0.92
edited_by: a00-9b888c7d
evidence_runs: experiment:a00-9b888c7d-reverse-bridge-dh99
line_ceiling: 40
production_lines: 0
profile: balanced
role: kid
season: 2
testable_claim: On the DH.99 tip, no production command reconverges an edited profile_ref projection artifact back into the graph node that names it -- including the new profile_sync --all/check_all sweep and the rotate _check_profile_drift guard.
title: "DH.99 re-probe: no reverse profile_ref bridge on the drift-detector and rotate-guard tip"
town: core
verdict: inconclusive_lean_proved:92
---
<!-- BODY:BEGIN -->
# experiment:a00-9b888c7d-reverse-bridge-dh99

## What was run

Fresh scratch repo at
`.agi/sessions/iter-DH.99/a00-9b888c7d/scratch` (own `.agi/config.json`, node
`hypothesis:h1` carrying `profile_ref: profile/out.md`), driven by the REAL
engine at `<checkout>/extensions/agi/bin/`. `locations.find_project_root()`
resolved to the scratch `.agi` (`layout: graph_dir`). Node body sha was
re-hashed after every step.

## Raw commands and observed output

### Step 1 — forward-project the node (artifact created)

```
$ python3 <ENG>/profile_sync.py hypothesis:h1
synced .../scratch/profile/out.md bytes=65 sha256=f0dd8da94b3fc04d915f9b7c1284d3c95570d512e3a905b19cb152385877ba84
rc=0
node_sha=7103ae2d3ef06d2e5f85d2537f8e8cddd4657b63b8b4b0bba1465a730bd44bbc
art_sha =f0dd8da94b3fc04d915f9b7c1284d3c95570d512e3a905b19cb152385877ba84
```

### Step 2 — harness-side artifact edit

```
$ printf 'HARNESS EDITED LINE\nthis content came from the artifact, not the node\n' > profile/out.md
node_sha=7103ae2d3ef06d2e5f85d2537f8e8cddd4657b63b8b4b0bba1465a730bd44bbc  (unchanged)
art_sha =198a4d84960351ba0da42c7215ee30b11d94f4bf9a7bf5f452bfc5312013de7c
```

### Step 3 — every plausible reconverging surface

**3a. `profile_sync.py hypothesis:h1 --check`** (existing detector)

```
$ python3 <ENG>/profile_sync.py hypothesis:h1 --check
DRIFT .../scratch/profile/out.md bytes=65 sha256=f0dd8da94b3fc04d915f9b7c1284d3c95570d512e3a905b19cb152385877ba84
rc=1
node_sha=7103ae2d3ef06d2e5f85d2537f8e8cddd4657b63b8b4b0bba1465a730bd44bbc  (unchanged)
```

**3b. `profile_sync.py hypothesis:h1`** (forward projector)

```
$ python3 <ENG>/profile_sync.py hypothesis:h1
synced .../scratch/profile/out.md bytes=65 sha256=f0dd8da94b3fc04d915f9b7c1284d3c95570d512e3a905b19cb152385877ba84
rc=0
node_sha=7103ae2d3ef06d2e5f85d2537f8e8cddd4657b63b8b4b0bba1465a730bd44bbc  (unchanged)
art_sha =f0dd8da94b3fc04d915f9b7c1284d3c95570d512e3a905b19cb152385877ba84  (artifact reset TOWARD node)
```

**3c. `profile_sync.py --all`** (new sweep) — artifact reseeded with v2 bytes first

```
art_sha(before)=09cd0c110cc933314dfe568df99b18713aa862e8bd287bf87fa25e7b56229d9b
$ python3 <ENG>/profile_sync.py --all
DRIFT hypothesis:h1 profile/out.md sha256=f0dd8da94b3fc04d915f9b7c1284d3c95570d512e3a905b19cb152385877ba84
1 linked, 1 not ok
rc=1
node_sha=7103ae2d3ef06d2e5f85d2537f8e8cddd4657b63b8b4b0bba1465a730bd44bbc  (unchanged)
art_sha =09cd0c110cc933314dfe568df99b18713aa862e8bd287bf87fa25e7b56229d9b  (unchanged; read-only)
```

**3d. `profile_sync.py --all --check`** (new sweep + check)

```
$ python3 <ENG>/profile_sync.py --all --check
DRIFT hypothesis:h1 profile/out.md sha256=f0dd8da94b3fc04d915f9b7c1284d3c95570d512e3a905b19cb152385877ba84
1 linked, 1 not ok
rc=1
node_sha=7103ae2d3ef06d2e5f85d2537f8e8cddd4657b63b8b4b0bba1465a730bd44bbc  (unchanged)
art_sha =09cd0c110cc933314dfe568df99b18713aa862e8bd287bf87fa25e7b56229d9b  (unchanged)
```

**3e. rotate `_check_profile_drift` guard** — driven standalone by importing
the function, since full `rotate-self` needs a live seat. Artifact reseeded v3 first.

```
art_sha(before)=09cd0c110cc933314dfe568df99b18713aa862e8bd287bf87fa25e7b56229d9b
$ python3 -c "import rotate; print(repr(rotate._check_profile_drift(Path('.../scratch/.agi'))))"
guard_return= 'rotate refused: profile drift — 1 linked node(s) out of sync: hypothesis:h1 (drift)'
rc=0
node_sha=7103ae2d3ef06d2e5f85d2537f8e8cddd4657b63b8b4b0bba1465a730bd44bbc  (unchanged)
art_sha =09cd0c110cc933314dfe568df99b18713aa862e8bd287bf87fa25e7b56229d9b  (unchanged; guard is read-only, it only refuses)
```

### Step 4 — POSITIVE CONTROL (the probe can see a change)

```
$ python3 <ENG>/write.py hypothesis:h1 'set title probe title delta'
updated: hypothesis:h1
rc=0
node_sha(before)=7103ae2d3ef06d2e5f85d2537f8e8cddd4657b63b8b4b0bba1465a730bd44bbc
node_sha(after ) =fc1fe98c029c9f6a0c4775341177203363cd0f8d2bd8814a2a3a60768beeb306  (CHANGED)
art_sha (before)=09cd0c110cc933314dfe568df99b18713aa862e8bd287bf87fa25e7b56229d9b
art_sha (after ) =f0dd8da94b3fc04d915f9b7c1284d3c95570d512e3a905b19cb152385877ba84  (reset TOWARD node)
```

The node file DID change and the artifact DID reset once a node-directed
write happened, so a reverse signal would have been observable. It was not.

## Conclusion

| surface | rc | direction | node changed? |
|---|---|---|---|
| `profile_sync <node> --check` | 1 | detector only | no |
| `profile_sync <node>` | 0 | node → artifact | no |
| `profile_sync --all` | 1 | sweep, read-only | no |
| `profile_sync --all --check` | 1 | sweep, read-only | no |
| rotate `_check_profile_drift` | — | refuse-by-name, read-only | no |
| `write.py set title` (positive control) | 0 | node → artifact | yes |

The artifact edit was never propagated to the node on any surface; where a
command moved the artifact it moved it toward the node. A grep of
`extensions/agi/bin/` for `profile_ref` / `profile_sync` / a reverse verb
returns only `profile_sync.py` (forward projector) and `write.py` (calls it
after a node write); the remaining hits are unrelated prose about "artifact".
The new `check_all` sweep and the rotate guard both read node→artifact and
never write the node.

**On the DH.99 tip the reverse bridge is still ABSENT.** Falsifier unchanged:
when a reverse bridge lands, editing the artifact named by a node's
`profile_ref` and running the named command MUST change the node body to match.

## Evidence

Raw session log: `.agi/sessions/iter-DH.99/a00-9b888c7d/scratch` (gitignored).
Node body sha before any node-directed write:
`7103ae2d3ef06d2e5f85d2537f8e8cddd4657b63b8b4b0bba1465a730bd44bbc`.
Prior committed evidence: `experiment:a00-fcd60995-reverse-bridge-absent`.
