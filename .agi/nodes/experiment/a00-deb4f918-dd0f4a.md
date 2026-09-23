---
id: experiment:a00-deb4f918-dd0f4a
mint_id: 7e5c785637854aceba24e8e9ff7b22c4
type: experiment
parents:
  - hypothesis:commands-manifest-is-jevs-one-choice-surface
next_edges: []
confidence: 0.6
edited_by: a00-deb4f918
evidence_runs:
  - experiment:a00-deb4f918-dd0f4a
line_ceiling: 40
loop: hypothesis:commands-manifest-is-jevs-one-choice-surface@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 64
profile: balanced
role: kid
scaffold_hash: 24871346dbde70f3
season: 2
title: "commands.py manifest: one typed choice set for the write.py verb surface"
town: local-maxxing
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-deb4f918-dd0f4a

## Experiment

Built the first conjunct of the parent hypothesis: the `manifest` reader plus
its declaration data, scoped to `write.py`'s verb surface (the KID 1 brief).

**What changed**

1. `extensions/agi/bin/commands.py` — a new `manifest` action (choices:
   `list|show|run|json|manifest`). `manifest(root)` reads `command:commands`,
   joins each declared command to its `manifest:` metadata (deriving `cli`/
   `verb` from its own argv when absent), adds every `manifest:`-only entry
   and every `excluded:` verb (`proposable: false` + `reason`), and returns a
dict of `name · cli · verb · argv · args · purpose · side_effects ·
proposable`. `render_manifest` serialises it with `indent=2, sort_keys=True`.
   It touches only `raw_argv`, so `<engine>`/`<node-id>` placeholders survive
   and no absolute path is ever emitted. It runs nothing and writes nothing.
2. `.agi/nodes/.geometry/commands.md` — two new frontmatter maps. `manifest:`
   declares 11 write.py verbs (`create`, `set`, `unset`, `link`, `thought`,
   `note`, `payload`, `payload_text`, `read`, `replace`, `adopt`) with argv,
   args schema, purpose, side_effects and proposable. `excluded:` names the
   two stdin-only verbs (`patch`, `body_patch`) with their reason and
   `proposable: false`. The 25 existing `commands:` entries are untouched
   byte-for-byte; the manifest derives their cli/verb.
3. `extensions/agi/tests/test_commands_manifest.py` — the drift test.

## Evidence

```
$ python3 extensions/agi/bin/commands.py --root . manifest | python3 -c "..."
38 entries
write.py surface: adopt(proposable) body_patch(false, reason) create link
note patch(false) payload payload_text read replace set thought unset

$ <manifest twice> ; cmp /tmp/a.json /tmp/b.json
byte-identical

$ python3 extensions/agi/bin/commands.py --root . list | grep -c write.py
0        # `list`/INJECTION.md unchanged: write.py verbs live in `manifest:`

$ python3 -m pytest extensions/agi/tests/test_commands_manifest.py \
      extensions/agi/tests/test_commands.py -q
38 passed, 7 skipped in 3.86s
```

The drift test INTROSPECTS `write.py.VERBS` (loaded by path, registered in
`sys.modules` before `exec_module` — the `@dataclass` decorator needs it) and
asserts `set(VERBS) | {"create"}` equals the `write.py:` keys in the live
manifest. It additionally asserts: two renders byte-identical; every
`side_effects` in the closed `SIDE_EFFECTS` set; every arg carries
`{name, type, required, choices}`; no argv token starts with `/` and no
resolved home/root string appears; and (with `subprocess.call/Popen/run` and
`Path.write_text/write_bytes` monkeypatched to raise) the manifest neither
spawns nor writes.

## What the round did NOT cover

The parent hypothesis is larger than this conjunct. `propose` (Python, CLI and
the graphweb GET /commands.json + POST /propose endpoints), the declarations
for the other listed CLIs (send.py, dispatch.py, grid.py, links.py, ...), and
`side_effects` metadata for the 24 legacy commands are NOT in this round. The
manifest currently defaults them to `read`; that default is honest for the
inspection commands but wrong for e.g. `grid-commit` — a later kid must author
those overrides.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version. Two deviations recorded. (1) The kid brief asks the manifest to
contain no `<home>`, but the five mesh entries carry
`<home>/work/.sanctuary/ssh/config` and the same brief forbids editing the 25
existing commands; `<home>` is a clone-agnostic placeholder resolved at run
time, not a box value, so it stays and the test pins the literal only for the
write.py surface this round authored. (2) The 40-line production ceiling is
exceeded by the code path: 64 added lines in commands.py. This is not above
the 2x hard stop (80), so the round continued rather than re-briefing; the
extra lines are the eight-field per-entry serializer the brief specified, and
the frontmatter `manifest:`/`excluded:` maps (129 lines) are declaration data,
not production code.
<!-- THOUGHT:END -->
<!-- BODY:END -->

## Agent Notes
manifest action + write.py verb-surface data + drift test land and pass (8/8 new, 38 passed total); propose and the other CLIs remain for a later kid
