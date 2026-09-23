---
id: experiment:a00-34b27af0-profile-live-binding-absent
mint_id: c821420c517f4ef795c0b71901e28fbf
type: experiment
parents:
  - hypothesis:a00-34b27af0-c74d7a
next_edges: []
edited_by: a00-34b27af0
evidence_runs: experiment:a00-34b27af0-profile-live-binding-absent
line_ceiling: 40
loop: goal:g7.31.5.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 4064571dfe61db06
season: 2
title: Forward projection is proved only against fixtures; no live node carries profile_ref and no Grok Bot profile artifact exists
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-34b27af0-profile-live-binding-absent

## Question

Is the **forward projection** mechanism (`write.py` -> `profile_sync.py` ->
artifact) bound to any **live** graph node, and does a real **Grok Bot
profile/settings** artifact exist to bind to? `goal:g7.31.5.1`'s falsifier
needs both halves exercised on a live node, not a fixture.

## What was run

All commands run read-only from the repo root
(`/data/work/agi/.agi/worktrees/a00-0f77c803`). Raw output below, not a
summary.

### SWEEP 1 — live nodes carrying `profile_ref`

```
$ grep -rl '^profile_ref:' .agi/nodes/
(no output)
$ echo $?
1
$ grep -rl '^profile_ref:' .agi/nodes/ | wc -l
0
```

**0 files.** No node in the live graph carries a `profile_ref:` frontmatter
key, so no standing/instruction/routine/todo node is linked to any artifact.

### SWEEP 1b — control: the string `profile_ref` IS present as prose

To prove Sweep 1 is not a broken grep, the bare string appears in **17** node
files (16 before this experiment existed) — all of them discussion of the
feature, none a live binding:

```
$ grep -rl 'profile_ref' .agi/nodes/ | sort
.agi/nodes/experiment/a00-00c1e876-refusal-path-probes.md
.agi/nodes/experiment/a00-1b9a8e7e-profile-sync.md
.agi/nodes/experiment/a00-34b27af0-profile-live-binding-absent.md
.agi/nodes/experiment/a00-8fe9b3e7-profile-residues-audit.md
.agi/nodes/experiment/a00-fcd60995-reverse-bridge-absent.md
.agi/nodes/experiment/malformed-sibling-clean-noop-a00-61667d02.md
.agi/nodes/experiment/whole-graph-drift-sweep-pre-rotation-guard.md
.agi/nodes/goal/g7.31.5.2.md
.agi/nodes/goal/g7.31.5.3.md
.agi/nodes/hypothesis/a00-00c1e876-eff35f.md
.agi/nodes/hypothesis/a00-1b9a8e7e-9f618e.md
.agi/nodes/hypothesis/a00-5ffe6174-59e3aa.md
.agi/nodes/hypothesis/a00-61667d02-859c87.md
.agi/nodes/hypothesis/a00-8fe9b3e7-f0f08d.md
.agi/nodes/hypothesis/a00-ce81c047-f9185d.md
.agi/nodes/hypothesis/a00-d98256f8-5665e1.md
.agi/nodes/hypothesis/a00-fcd60995-474fcc.md
```

### SWEEP 2 — the adapter-landing goal is not landed

```
$ grep -E '^(status|title):' .agi/nodes/goal/g7.30.md
status: horizon
title: "G7.30: Land grok-bot adapter + post template on core/season2/main"
```

`goal:g7.30` is `status: horizon` — not landed.

### SWEEP 3 — the adapter names no profile/settings artifact

```
$ grep -rniE 'profile|settings' extensions/agi/bin/adapters/grok_bot_adapter.py
(no output)
$ echo $?
1
```

The only file path the adapter ever writes is a **session record**, not a
Grok Bot profile/settings surface:

```
$ grep -niE 'write_text|\.json|\.md' extensions/agi/bin/adapters/grok_bot_adapter.py
156:        (sess_dir / "agent.json").write_text(json.dumps(agent_record, indent=2))
```

### SWEEP 3b — `harnesses.grok-bot` config has no artifact cell

```
$ python3 -c "import json;d=json.load(open('.agi/config.json'));print(json.dumps(d.get('harnesses',{}).get('grok-bot'),indent=2))"
{
  "adapter": "grok_bot",
  "allowed_extra": [
    "grok-4",
    "grok-4-fast"
  ],
  "bin": "/home/ubuntu/.npm-global/bin/grok-bot",
  "models": {
    "kid": "grok-4-fast",
    "parent": "grok-4"
  }
}
```

No `profile`, `settings`, `env`, or artifact path cell. A repo-wide grep for a
Grok-specific profile/settings path returns nothing:

```
$ grep -rniE 'grok.*(profile|settings)|(profile|settings).*grok' \
    --include='*.py' --include='*.json' --include='*.md' extensions/ .agi/context/ .agi/config.json
(no output)
```

### SWEEP 4 — none of the standing/instruction node types exist live

```
$ for t in standing instruction routine todo; do echo "$t: $(ls .agi/nodes/$t 2>/dev/null | wc -l)"; done
standing: 0
instruction: 0
routine: 0
todo: 0
```

`.agi/nodes/` contains only: bigger_outcome, build, deprecated, doc,
experiment, goal, hypothesis, idea, moral, mvp, outcome, overview, town,
verdict, vision. There is no live `standing/` or `instruction/` type
directory, so the falsifier's *subject* type does not yet exist either.

### SWEEP 5 — the projector exists and is real

```
$ ls -la extensions/agi/bin/profile_sync.py
-rw-rw-r-- 1 belam belam 7131 Sep 23 14:32 extensions/agi/bin/profile_sync.py
```

## Observed

| sweep | command | result |
|---|---|---|
| 1 | `grep -rl '^profile_ref:' .agi/nodes/` | 0 files, exit 1 |
| 1b | `grep -rl 'profile_ref' .agi/nodes/` | 17 files, all prose mentions |
| 2 | `grep ^status `.agi/nodes/goal/g7.30.md` | `status: horizon` |
| 3 | grep adapter for profile/settings | no match (exit 1); only `agent.json` session record |
| 3b | harness config cell | no artifact path; repo-wide Grok-profile grep empty |
| 4 | live standing/instruction/routine/todo types | 0 each |
| 5 | `profile_sync.py` | present, 7131 bytes |

## Evidence / conclusion

**Two independent absences, one blocker.** (a) No live node carries
`profile_ref` — the link half of the falsifier sentence has never existed on
the live graph. (b) No real Grok Bot profile/settings artifact or settings
path exists anywhere in the adapter, the `harnesses.grok-bot` config cell, or
the repo — the target half has never existed either. Both are downstream of
`goal:g7.30`, which is `status: horizon`.

The forward projection itself is proved, but only against fixtures
(`experiment:a00-1b9a8e7e-profile-sync`; refusal path
`hypothesis:a00-00c1e876-eff35f`). **Live binding: ABSENT, blocked on
`goal:g7.30`.**

### Falsifier for when `goal:g7.30` lands

When a live node carries a real `profile_ref` to a Grok Bot profile/settings
artifact, editing that node via `write.py` must change the artifact bytes to
match. This experiment's Sweep 1 flips from `0` to `>=1` at that moment and
the claim is retested.
