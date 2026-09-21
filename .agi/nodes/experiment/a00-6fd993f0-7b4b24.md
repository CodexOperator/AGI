---
id: experiment:a00-6fd993f0-7b4b24
mint_id: 848b9e4688d944d2b4c99c735db8f6b2
type: experiment
parents:
  - hypothesis:lm-create-body-file-lands-real-prose-not-the-placeholder-scaffold
next_edges: []
confidence: 0.9
edited_by: a00-8f754fdf
evidence_runs:
  - experiment:a00-6fd993f0-7b4b24
line_ceiling: 200
loop: hypothesis:lm-create-body-file-lands-real-prose-not-the-placeholder-scaffold@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "real CLI subprocess against a temp project: `write.py create hypothesis wp --parent goal:g1 --body-file real.md --root <tmp>`", "expected": "rc 0; node body is `\\n# hypothesis:wp\\n\\n` + the file bytes; BODY_PROMPTS placeholder absent", "observed": "rc 0; body == heading + file bytes byte-for-byte; 'What is the testable claim?' not in body", "result": "HOLD - the flag threads argparse -> main -> create(body=) -> write_node(body=) live"}
  - {"conjunct": 2, "class": "gate", "cmd": "two temp-project runs: (i) create with no --body-file, compared byte-for-byte against node_writer.BODY_BEGIN + heading + BODY_PROMPTS['hypothesis']; (ii) create --body-file on a MISSING path", "expected": "(i) exact scaffold bytes unchanged; (ii) exit 2 naming --body-file, no node file created", "observed": "(i) equal=True; (ii) rc=2, `ERR: --body-file <path>: [Errno 2] ...`, node absent", "result": "HOLD - absent flag is a no-op regression-free; a bad path fails closed before any node"}
  - {"conjunct": 3, "class": "gate", "cmd": "node_writer._is_untouched_scaffold(full text of a --body-file node, BODY:BEGIN + heading + placeholder); plus empty --body-file and re-create-with-different-file runs", "expected": "real body -> False; empty file -> empty body with NO placeholder fallback; re-create must not clobber existing prose", "observed": "False; empty body='\\n# hypothesis:we\\n' no placeholder; first prose preserved, 'SECOND' absent", "result": "HOLD - a real body is never mistaken for an untouched scaffold and never clobbered"}
production_lines: 22
profile: balanced
role: kid
scaffold_hash: 76fa4d1f84861706
season: 2
title: write.py create --body-file lands real prose (built and proven); node_writer untouched
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-6fd993f0-7b4b24

## Experiment

**This is a g15 build order, not a measurement.** The claim was replicated in
its pre-fix state and then IMPLEMENTED on the built bytes.

### Pre-fix state (reproduced)

`node_writer.write_node` already accepts a `body` kwarg (node_writer.py ~L617)
that, when non-None, is used AS-IS instead of the per-type `BODY_PROMPTS`
placeholder (L725: `scaffold_body += BODY_PROMPTS.get(ntype, "") if body is None
else body`). `write.py create()` had no `body` parameter and no `--body-file`
flag, so every `create` landed the placeholder. Verified by reading the two
source sites and by `write.py create -h` (no such flag).

### What was built

`extensions/agi/bin/write.py` only (`node_writer.py` deliberately untouched):

- new `--body-file PATH` argparse flag in the `create` block, `metavar="PATH"`,
  mirroring `--payload`;
- `create()` gains keyword-only `body: str | None = None`, forwarded to
  `node_writer.write_node(..., body=body)`;
- `main()`'s create branch reads the file as UTF-8. The verb layer owns IO, so
  the read lives in `main()` and the refusal can name the path; `-"` is treated
  as a literal path (it simply does not exist, so it refuses by name);
- FAIL-CLOSED: a `--body-file` that does not exist or is unreadable prints
  `ERR: --body-file <path>: <reason>` to stderr, returns 2, and writes NO node;
- `--body-file` absent passes `body=None` unchanged, so today's `BODY_PROMPTS`
  scaffold path is byte-identical. No refactor of `scaffold_body`.

### What the bytes show

- **Real prose lands, verbatim after `write_node`'s canonical heading.**
  `create --body-file prose.md` produced a body equal to
  `"\n# <node-id>\n\n" + <file bytes>` with the `BODY_PROMPTS` placeholder
  ABSENT. `node_writer` prepends the `# <id>` heading to ANY supplied body, so
  the heading is the writer's, not the file's — the file's prose below it is
  byte-identical.
- **No flag = unchanged.** A no-flag create produced exactly
  `BODY_BEGIN + "\n# <id>\n\n" + BODY_PROMPTS["hypothesis"]` (trailing newline
  normalised to one by `_serialize_node`).
- **Falsifier (c) clear.** `_is_untouched_scaffold` on a real `--body-file` body
  against the placeholder scaffold returns **False**.
- **Fail-closed proven against a missing path AND an unreadable (chmod 000)
  path**: exit 2, no node file created in either case.

## Evidence

Engine test suite, changed file only:

```
$ python3 -m pytest extensions/agi/tests/test_write.py -q
130 passed, 84 warnings in 0.96s
```

The three new fixtures (no fourth added):

- `test_create_body_file_lands_real_prose_not_the_placeholder` — CLI path,
  multi-line prose, body == heading + file bytes, placeholder absent.
- `test_create_without_body_file_still_scaffolds_the_placeholder` — byte
  comparison against the exact `body is None` scaffold bytes (regression).
- `test_is_untouched_scaffold_rejects_a_real_body_file_body` — falsifier (c).

Manual fail-closed run against a temp project (`failclosed2.sh`):

```
--- good body-file ---
created: hypothesis:goodbody -> .../goodbody.md   rc=0
# hypothesis:goodbody

  Real prose line A.

  Line B.
--- unreadable body-file ---
ERR: --body-file /tmp/.../noperm.md: [Errno 13] Permission denied   rc=2
(no noperm.md written)
```

Production lines: `git diff --numstat -- extensions/agi/bin/write.py` =
`24  2` (22 net), ceiling 200.

## Caveat (recorded, out of scope)

A `--body-file` node carries NO `<!-- BODY:BEGIN -->` marker: `node_writer` only
prepends it when `body is None`. `cli.py done`'s frontmatter-repair path needs
that anchor only when the `---` block is unclosed/mangled — a body-file node
whose frontmatter is clean (the normal case) is unaffected. But a body-file node
whose closing `---` is later mangled has no anchor to separate frontmatter from
body, and `done` will refuse the repair by name. Fixing it means touching
`node_writer.py` (explicitly out of scope for this round).

## Agent Notes
Built write.py create --body-file (argparse flag -> keyword-only body -> node_writer.write_node body=), fail-closed on missing/unreadable with exit 2 and no node; --body-file absent byte-identical to the BODY_PROMPTS scaffold. 3 fixtures, 130 passed in test_write.py. 22 production lines. Caveat: body-file nodes carry no BODY:BEGIN repair anchor.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review EF.05 (a00-8f754fdf). (1) The instruction said: one negative probe per claim conjunct, run BY THE PARENT, recorded as `probes:`; a kid that passes its own tests but fails a probe is lean_disproved with the probe named. (2) What the machine does, cited to artifact I built and ran: the kid commit 3ba616f61 adds `--body-file` (write.py:2590), reads UTF-8 in main() (write.py:2674-2681, fail-closed exit 2), and threads `body=body` through `create()` (write.py:2474, 2518) into `node_writer.write_node`'s existing `body` kwarg. My own probes (3 fixtures, /scratch/probe_body_file.py) invoked the REAL CLI as a subprocess against a temp project: prose landed byte-for-byte after the canonical `# <id>` heading; no-flag output equalled BODY:BEGIN+heading+BODY_PROMPTS byte-for-byte; a missing path gave rc=2 and wrote no node; an empty --body-file landed empty with NO placeholder fallback; `_is_untouched_scaffold(real_body, placeholder)` returned False; a re-create with different prose did not clobber. All HOLD. (3) The near miss this diff avoids: a plausible implementation reads the file inside `create()` and lets an unreadable path raise a traceback, or falls back to the placeholder when the read yields empty — that satisfies the words and loses the mechanism. This one refuses by name before minting and lands empty verbatim. (4) Deviation: none from a standing rule. Caveat carried from the kid and accepted: a --body-file node carries no `<!-- BODY:BEGIN -->` marker (write_node adds it only when body is None), so `done`'s frontmatter-repair path has no anchor for such a node if its `---` is later mangled; out of this round's file scope (write.py only) and recorded rather than fixed. VERDICT: kid's `proved` accepted; probes recorded.
<!-- THOUGHT:END -->
