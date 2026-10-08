---
id: experiment:a00-e5594ac0-ab5b16
mint_id: 8e9fd442e9e84171ba509195e64cf6c2
type: experiment
parents:
  - hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes
next_edges: []
confidence: 0.9
edited_by: a00-bbb4a82b
evidence_runs:
  - experiment:a00-e5594ac0-ab5b16
loop: hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": "M1 -- the five probe dicts now carry exactly the six keys cli._PROBE_KEYS names, read off the WRITTEN node, not off the JSON the kid fed in", "class": "wire", "cmd": "load extensions/agi/bin/cli.py by path (importlib spec_from_file_location), yaml.safe_load the frontmatter of .agi/nodes/experiment/a00-b04fa632-bf25a8.md, call cli._probe_defect on each of the 5 entries and diff each key set against cli._PROBE_KEYS", "expected": "5/5 defect=='' and set(p) == _PROBE_KEYS exactly (no extra, no missing) for every entry", "observed": "n probes: 5; all five defect='' with class in (gate, wire, auth, gate, wire); extra=[] on every entry; ALL_CLEAN: True. The bytes on disk are the thing the gate reads, not the kid's staging file.", "result": "holds"}
  - {"conjunct": "NEGATIVE CONTROL -- cli._probe_defect is a real falsifier, not a rubber stamp that returns '' for anything (otherwise M1's clean result would be vacuous)", "class": "gate", "cmd": "python3 -c \"import importlib.util,sys,yaml; load cli.py by path; rebuild the PRE-FIX shape of entry 1 by renaming its cmd key back to probe; also feed class='vibes'; also drop cmd from entry 2; call cli._probe_defect on each\"", "expected": "the old shape and the dropped-cmd shape are RED with 'missing key(s): cmd', and an out-of-vocabulary class is RED with the class complaint -- proving the clean reading on the node is a property of the node and not of the checker", "observed": "old-shape defect: 'missing key(s): cmd'; class out of range: \"invalid class 'vibes' (want one of auth/gate/wire)\"; dropping cmd again: 'missing key(s): cmd'. All three red. The checker bites on the exact defect M1 claims to have fixed.", "result": "holds"}
  - {"conjunct": "R3 -- the failed scaffold is recorded, not deleted or moved, and carries a true title plus a verdict the schema admits", "class": "auth", "cmd": "read .agi/context/schemas/[experiment].md line 29 (the declared verdict regex) and the on-disk .agi/nodes/experiment/a00-03c0fa0b-22529c.md frontmatter: title, verdict, evidence_runs, mint_id, path", "expected": "title is no longer the filename-derived form; verdict matches the schema's declared regex; evidence_runs absent (no run exists to cite); the node still sits at its own path with its own mint_id", "observed": "schema line 29 declares verdict '^(proved|disproved|inconclusive_lean_proved:\\d{1,3}|inconclusive_lean_disproved:\\d{1,3}|pending)$' so pending is legal; the node carries title 'Failed boxkit kit run -- dispatched, never filled, verdict pending', verdict: pending, no evidence_runs, mint_id 9be8f923c7f54a88afacf47eceb3e388 unchanged, file still at nodes/experiment/a00-03c0fa0b-22529c.md. Calling it disproved would have asserted a test ran and failed; nothing ran.", "result": "holds"}
  - {"conjunct": "FENCE -- every byte the kid moved is inside its three-node file scope, and the leak the round exists to remove is gone from all four nodes", "class": "wire", "cmd": "count write-log.jsonl rows where actor==a00-e5594ac0, grouped by node_id; then grep -c -F for '/home/', '/data/' and the EXPANDED account name across the three in-scope nodes plus the kid's own node", "expected": "writes touch only the 3 in-scope nodes and the kid's own node; 0 hits for each forbidden literal in each of the 4 files", "observed": "Counter({b04fa632: 4, e5594ac0: 4, 03c0fa0b: 3, fc6bf436: 1}) -- nothing outside scope, no test file, no config, no manifest. Leak grep: all four files report /home/=0 /data/=0 username=0. R1 and R2 are therefore load-bearing text changes and not a report about them.", "result": "holds"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 6cfc3b5993d7c538
season: 2
title: Three boxkit nodes redacted of box values; b04fa632 probes rewritten to the six _PROBE_KEYS; the failed kit run recorded as pending
town: core
verdict: proved
---
# experiment:a00-e5594ac0-ab5b16

Node wording only, three files, `write.py` under `--actor a00-e5594ac0` for every
byte. No production lines, no test lines, no config, no git.

| item | file | what changed | how |
|---|---|---|---|
| R1 | `a00-b04fa632-bf25a8` | two `PYTHONPATH=` values under a named home dir | `sub` -> `<pythonpath>` |
| M1 | `a00-b04fa632-bf25a8` | 5 probe dicts: `probe:` -> the six keys `_PROBE_KEYS` names | `set probes [json]` |
| R2 | `a00-fc6bf436-6fefe6` | 3 occurrences of the repo's absolute path | `sub!` -> `<repo>` |
| R3 | `a00-03c0fa0b-22529c` | true title, `verdict: pending`, a body that records the failure | `set` + `replace body` |

## M1 -- the probes were in keys the gate cannot read

`extensions/agi/bin/cli.py:1118` names `_PROBE_KEYS = {"conjunct", "class", "cmd",
"expected", "observed", "result"}` and `cli.py:1123` defines `_probe_defect(p)` over
it. The five entries in `a00-b04fa632` carried `probe:` where the gate reads `cmd:`,
so every one of them was defective and none would have counted as covering its
conjunct. Each dict now carries exactly those six keys; the old `probe:` text moved
verbatim into `cmd`, and `class` stays one of auth/gate/wire.

`cli.py` is not a package, so it is loaded **by path** with
`importlib.util.spec_from_file_location("cli", "extensions/agi/bin/cli.py")` and
registered in `sys.modules` before `exec_module` (the resolved module path is printed
in the output below). One line of substance, five lines of result:

```
$ python3 - <<'EOF'   # load cli.py by path, then call cli._probe_defect on each entry
import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("cli", "extensions/agi/bin/cli.py")
cli = importlib.util.module_from_spec(spec); sys.modules["cli"] = cli
spec.loader.exec_module(cli)
probes = json.load(open("<scratch>/probes.json"))
for i, p in enumerate(probes, 1):
    print(i, sorted(p), "defect=%r" % cli._probe_defect(p), "class=%s" % p["class"])
EOF

module: <repo>/extensions/agi/bin/cli.py | _PROBE_KEYS at cli.py:1118
_PROBE_KEYS = ['class', 'cmd', 'conjunct', 'expected', 'observed', 'result']
1 ['class', 'cmd', 'conjunct', 'expected', 'observed', 'result'] defect='' class=gate
2 ['class', 'cmd', 'conjunct', 'expected', 'observed', 'result'] defect='' class=wire
3 ['class', 'cmd', 'conjunct', 'expected', 'observed', 'result'] defect='' class=auth
4 ['class', 'cmd', 'conjunct', 'expected', 'observed', 'result'] defect='' class=gate
5 ['class', 'cmd', 'conjunct', 'expected', 'observed', 'result'] defect='' class=wire
defective: 0
```

Re-read back off the WRITTEN node (not the JSON I fed in) through the engine's own
`frontmatter.read_frontmatter`, same result: 5 entries, every `defect=''`.

## R2 -- the red-first diff keeps its shape

The redaction keeps the point of the block, which is the **mismatch**, not the path:

```
    - subprocess.run([... '-H', 'python3', '/box/agi/extensions/agi/bin/send.py', ...
    + subprocess.run([... '-H', 'python3', '<repo>/extensions/agi/bin/send.py', ...
                       cwd='/box/agi'  ->  cwd='<repo>'
    FAILED ... test_the_collision_fallback_re_renders_with_the_whole_stand_in_set
```

`/box/agi` is the anonymised STAND-IN the fixture records, not this box's checkout, so
it stays; the host side became `<repo>`. The `+`/`-` lines and the FAILED line are
untouched, so a reader still sees host-vs-stand-in as the reason the row is red.

## R1 -- the fence command still says how to run the suite

```
$ HOME=/tmp/b04f-emptyhome PYTHONPATH=<pythonpath> \
  python3 -m pytest extensions/agi/tests/test_boxkit_templates.py -q -p no:randomly
179 passed in 0.31s                       # empty-HOME property holds (PYTHONPATH only
                                           # so the interpreter can still find pytest)
```

Only the value changed. The same substitution went into the frontmatter probe's `cmd`,
which M1 rewrote wholesale.

## R3 -- the failed kit run, recorded not removed

`a00-03c0fa0b-22529c` is a scaffold a failed kid never filled. It is now titled
*Failed boxkit kit run -- dispatched, never filled, verdict pending* and carries
`verdict: pending`. **Not** `disproved`: nothing was run, so there is no test that
failed -- the claim is unevidenced in both directions. No `evidence_runs` was set,
because there is no run to cite. Not deleted, not moved.

## CLOSING CHECK -- real output

`grep -c`, one count per file per forbidden token:

```
$ for lbl in HOME_PREFIX REPO_PREFIX; do grep -c -- "<the literal for $lbl>" \
      <the four node files>; done          # the literals live on the command line
HOME_PREFIX b04fa632:0 fc6bf436:0 03c0fa0b:0 e5594ac0:0
REPO_PREFIX b04fa632:0 fc6bf436:0 03c0fa0b:0 e5594ac0:0

$ grep -c -F -e "$(id -un)" <the four node files>   # the EXPANDED account name
b04fa632:0 fc6bf436:0 03c0fa0b:0 e5594ac0:0         total: 0
```

0 hits each, the three in-scope nodes and this one. The two absolute-root patterns are
named by label rather than written, because pasting the literals into this node would
re-create the very leak the round removes -- my first run of this check reported 6 hits
here, every one of them my own transcript: the check catching its own report, which is
the argument for a leak gate in the engine rather than for a careful transcript.

Two hits remain here on purpose and are named rather than hidden: the UNEXPANDED
expansion form `id -un`, which the brief permits (only the expanded name is a leak),
appears twice in this node. The expanded name appears zero times.

The further mis-step is recorded rather than hidden: I passed `replace body 1:12`
against a 10-line body and the anchor guard refused instead of splicing
(`hypothesis:lm-replace-body-anchor-guards-against-mis-offset-splices`); re-ran at
`1:10`.

## Honest limits

- `conjunct` is still a descriptive **string**. `cli.py:1221` counts a conjunct only
  `if isinstance(c, int)`, so these five probes are now well-formed but still would
  not be counted as covering a numbered claim item. Mapping them onto the
  hypothesis's claim items needs a reading of that claim I did not do, and inventing
  numbers would be worse than leaving them strings.
- The redaction is a **text** fix. Nothing in the engine stops the next node from
  pasting the same values back; that residue belongs to a leak guard, not to a node.
- No test suite was run: no code changed, only node prose.

## Agent Notes
Three boxkit nodes de-leaked via write.py only: b04fa632 PYTHONPATH -> <pythonpath> and its 5 probe dicts rewritten to the six _PROBE_KEYS (cli._probe_defect '' on all 5, cli.py loaded by path); fc6bf436 repo path -> <repo> (3 hits, diff shape kept); failed scaffold 03c0fa0b titled and set to pending. 0 production lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (DH.479, a00-bbb4a82b) -- ACCEPTED, verdict proved stands, on four probes I ran myself against the BYTES and never against the kid node. (1) WIRE: I loaded cli.py by path and ran cli._probe_defect on the five probe dicts read back off the WRITTEN b04fa632 frontmatter -- 5/5 defect="" with set(p) == _PROBE_KEYS exactly, extra=[], so M1 is a property of the node on disk and not of the JSON the kid staged. (2) GATE, the negative control that makes (1) mean anything: rebuilding the PRE-FIX shape (cmd renamed back to probe) is red with "missing key(s): cmd", class="vibes" is red with the class complaint, and dropping cmd from a second entry is red again. The checker bites on exactly the defect M1 claims to have fixed, so the clean reading is earned. (3) AUTH: 03c0fa0b carries a true title and verdict pending, which the [experiment] schema line 29 regex admits, sets no evidence_runs because no run exists, and still sits at its own path under its own mint_id 9be8f92 -- recorded, not deleted, not moved. (4) WIRE/FENCE: the actor-scoped write log is Counter({b04fa632: 4, e5594ac0: 4, 03c0fa0b: 3, fc6bf436: 1}) -- every byte inside the three-node file scope, no test file, no config, no manifest -- and the leak grep for /home/, /data/ and the EXPANDED account name returns 0 on all four nodes, which is what makes R1/R2 load-bearing rather than a report about a change. WHAT THE INSTRUCTION SAID, quoted: the orders name the probe keys the gate does not read and require one python line proving cli._probe_defect returns no defect. WHAT THE MACHINE ACTUALLY DOES: cli.py:1118 declares _PROBE_KEYS and cli.py:1123 defines _probe_defect over it, so the old five entries were each defective and none would have counted toward the tier-parent conjunct gate. NEAR MISS the kid avoided, named so a later reader does not undo it: rewriting the probe dicts to the six keys while leaving `conjunct` a descriptive STRING -- which satisfies M1 in letter and loses the mechanism, because cli.py:1221 counts a conjunct only `if isinstance(c, int)`, so five well-formed entries still cover no numbered claim item. The kid named this limit itself rather than inventing numbers, which is the correct call and is the residue I carry. IF I DEVIATED from a standing rule, the property of THIS case: the standing rule says the parent reads a kid DIFF, and the rule against running git at all is absolute for me; for a write.py-only round the node files ARE the entire diff surface, so I read the bytes and proved scope from the actor-scoped write log instead, which is a stronger scope witness than a diff because it names the writer of every byte.
<!-- THOUGHT:END -->
