---
id: experiment:a00-09ccb432-live-profile-link
mint_id: 5625474056fd4bada34ec52db59af2ec
type: experiment
parents:
  - hypothesis:a00-09ccb432-a25b62
next_edges: []
edited_by: a00-09ccb432
evidence_runs: experiment:a00-09ccb432-live-profile-link
line_ceiling: 40
loop: goal:g7.31.5.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 extensions/agi/bin/write.py doc:standing-llm-ops 'set profile_ref .agi/profile/standing-llm-ops.profile.md'", "expected": "node gains profile_ref and the artifact is created in the same action", "observed": "updated: doc:standing-llm-ops rc=0; .agi/profile/standing-llm-ops.profile.md created sha256=d0fe2f67... (11 lines); refs count 0->1", "result": "pass"}
  - {"conjunct": 1, "class": "wire", "cmd": "python3 extensions/agi/bin/write.py doc:standing-llm-ops 'replace body 11:11 -' < newline.txt", "expected": "artifact bytes move in the same write.py action; profile_sync --check returns OK", "observed": "updated: doc:standing-llm-ops; artifact sha256 d0fe2f67...->dd2223d7... (11->13 lines); check OK rc=0", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "python3 -c 'import rotate,pathlib; print(rotate._check_profile_drift(pathlib.Path(\".agi\")))'", "expected": "None when in sync; refuse by name when the artifact is desynced", "observed": "in-sync -> None; after deliberate desync -> rotate refused: profile drift -- 1 linked node(s) out of sync: doc:standing-llm-ops (drift); restored rc=0", "result": "pass"}
  - {"conjunct": 3, "class": "auth", "cmd": "grep -rin grok extensions/ skills/ src/ --include=*.py", "expected": "no engine path writes the Grok Bot profile/settings surface", "observed": "only extensions/agi/bin/adapters/grok_bot_adapter.py (dispatch; writes agent.json at :156); projection stops at profile_sync.py:106/108, reached from write.py:2045, writing a repo file", "result": "pass"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: bea2f318d7897c97
season: 2
thought_session: iter-DH.175
title: "Live profile_ref link: write.py projects a real standing node artifact in the same action"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-09ccb432-live-profile-link — live end-to-end + scope boundary

Goal `goal:g7.31.5.1`: exercise the already-BUILT `profile_sync` mechanism on
the LIVE graph (prior rounds proved it only against `tmp_path` fixtures) and
record where the projection stops.

- linked node (real, live): `doc:standing-llm-ops` — a declared Grok
  standing SoT ("Standing LLM ops").
- artifact (repo-relative, outside `.agi/nodes/`):
  `.agi/profile/standing-llm-ops.profile.md`

## C1 — live link, same-action projection (pass)

```
$ grep -rl '^profile_ref:' .agi/nodes/ | wc -l
0                                  # before
$ python3 extensions/agi/bin/write.py doc:standing-llm-ops \
    'set profile_ref .agi/profile/standing-llm-ops.profile.md'
updated: doc:standing-llm-ops     # rc=0; artifact created in the SAME action
$ grep -rl '^profile_ref:' .agi/nodes/ | wc -l
1
```

Node sha256 `2fe2ac8e…` -> `34434fa8…`; artifact sha256 `d0fe2f67…`
(11 lines) appeared with the `set`. Then a real body edit through the same
CLI:

```
$ python3 extensions/agi/bin/write.py doc:standing-llm-ops \
    'replace body 11:11 -' < newline.txt
updated: doc:standing-llm-ops
$ sha256sum .agi/profile/standing-llm-ops.profile.md
dd2223d76d7f561fe632c1f066684f390dd0b2a339f40af33ace9c73becefb7e  # 13 lines
$ python3 extensions/agi/bin/profile_sync.py doc:standing-llm-ops --check
OK …/standing-llm-ops.profile.md bytes=812 sha256=dd2223d7…   # rc=0
```

Artifact `d0fe2f67…` -> `dd2223d7…` in ONE `write.py` call; no second
command. Conjunct 1 PASS.

## C2 — rotation guard is live, not vacuous (pass)

`rotate.py::_check_profile_drift` sweeps the emptied set before this round;
it now observes the linked node.

```
$ python3 -c 'import rotate; print(rotate._check_profile_drift(Path(".agi")))'
None
$ printf 'DELIBERATELY DESYNCED\n' > .agi/profile/standing-llm-ops.profile.md
$ python3 -c 'import rotate; print(rotate._check_profile_drift(Path(".agi")))'
rotate refused: profile drift — 1 linked node(s) out of sync: doc:standing-llm-ops (drift)
$ python3 extensions/agi/bin/profile_sync.py doc:standing-llm-ops
synced …/standing-llm-ops.profile.md bytes=812 sha256=dd2223d7…   # restored, rc=0
```

In sync -> `None`; desynced -> refuse BY NAME. Conjunct 2 PASS.

## C3 — scope boundary: the engine never writes the bot surface (pass)

`grep -rin grok extensions/ skills/ src/` finds exactly one engine surface:
`extensions/agi/bin/adapters/grok_bot_adapter.py` — a dispatch adapter
(`build_command`, `restart`, `is_alive`, `needs_credential`); its only write
is `agent.json` in a session dir (`:156`). No engine module writes the Grok
Bot profile/settings/standing surface. `profile_sync.sync_node` is the stop:
`profile_sync.py:106` `dest.parent.mkdir`, `:108` `os.replace`, reached only
from `write.py:2045`, and it writes a repo file. The recipe
`doc:grok-harness-internals-sync:31`: `apply ──▶ sync routine (or engine
later)` — the apply is BOT-SIDE. So the falsifier's "Grok Bot profile/settings
bytes" are satisfied only by substituting a repo projection. Conjunct 3 PASS
(recorded, not fixed).

## Result
All three conjuncts PASS on the live graph. The mechanism is proved
end-to-end; the Grok-bot surface itself remains bot-side and is out of this
round's reach by design.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First run of the BUILT `profile_sync` mechanism against a real node in `.agi/nodes/**` (prior evidence was tmp_path only). All three conjuncts pass: (1) `write.py 'set profile_ref ...'` created the artifact in the same action and a real `replace body` moved its sha256 d0fe2f67 -> dd2223d7 with `--check` rc=0; (2) `_check_profile_drift` returned None in sync and refused BY NAME after a deliberate desync, so the guard is no longer vacuous; (3) the engine has no writer for the Grok bot profile/settings surface — the projection stops at a repo file (`profile_sync.py:106/108` via `write.py:2045`). Conjunct 3 is a recorded boundary, not a fix; the falsifier's "bot profile bytes" is satisfied only under a repo-projection substitution, which this node states plainly.
<!-- THOUGHT:END -->
