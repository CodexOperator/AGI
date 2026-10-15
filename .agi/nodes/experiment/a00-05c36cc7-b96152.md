---
id: experiment:a00-05c36cc7-b96152
mint_id: 761378ce34dc456295178fdd5c93c830
type: experiment
parents:
  - hypothesis:a-zero-usd-lane-prints-the-cap-it-mints-and-keeps-the-key-and-cap-guards
next_edges: []
confidence: 0.6
edited_by: a00-cb44102b
evidence_runs:
  - experiment:a00-05c36cc7-b96152
loop: hypothesis:a-zero-usd-lane-prints-the-cap-it-mints-and-keeps-the-key-and-cap-guards@s2
model: stealth/space-bunny-alpha
probes:
  - "wire: M-wire-1 — the refused write (tier-3 prime_director settings ultracode -> \"\") applied to a THROWAWAY copy of .agi/nodes in /tmp, read back via spawn_gate.read_ladder_roles + dispatch.resolve_role_spec: live {\"settings\": \"ultracode\"} vs mutated {\"settings\": null}; dispatch.py:2093-2094 copies that cell into dispatch_harness[\"settings\"], a real launch flag; ARTEFACT .agi/sessions/iter-DH.638/a00-05c36cc7/probe_settings_flag.py + .out"
production_lines: 0
profile: balanced
role: kid
scaffold_hash: b9f7aeff0cfc9df8
season: 2
title: "DH.638 corrective: ladder cell refused to a kid, sibling numbers corrected, one real wire probe"
town: core
verdict: inconclusive_lean_proved:60
---
# experiment:a00-05c36cc7-b96152

DH.638 corrective round, kid a00-05c36cc7. Parent brief carried six open items.
I ran each to ground; three are settled in the bytes, three are NAMED because a
kid cannot reach them. No production line was added: net production lines = 0.

## 0. Verdict in one table

| item | state | what I did |
|---|---|---|
| 1 ladder cell | **NAMED** — a kid cannot write `config:ladder` | ran the ordered write.py verb; it refused; pasted |
| 2 production_lines citation | **SETTLED (claim withdrawn)** | re-measured at this base, pasted |
| 3 self-cited test count | **SETTLED (node corrected)** | re-ran the three files, node body corrected via write.py |
| 4 no `probes:` | **SETTLED** | ran M-wire-1, recorded `probes:` on the sibling node |
| 5 stray `the` | **SETTLED** | removed from the working tree (unstaged; the loop commits) |
| 6 deprecated stray node | **NAMED** — out of any round's reach | see below |

## 1. The ladder cell — the writer refuses, so a kid cannot fix it

The brief's ordered fix, run verbatim:

```
$ python3 extensions/agi/bin/write.py config:ladder 'set prime_director settings ultracode -> ""'
ERR: config nodes (config:ladder) may be hand-edited only by admitted roles owner,
     prime_director; resolution for actor '' gave kid, which is not admitted. (goal:g12)
```

The live row, read back from `.agi/nodes/.geometry/ladder.md`:

```
- {"tier": 3, "role": "prime_director", "harness": "claude-code", "model": "claude-fable-5-1", "effort": "max", "settings": "ultracode"}
```

I did NOT hand-edit the file (the brief forbids it) and I did NOT rewrite the
assertion to `== "ultracode"` — see the probe below for why that is the opposite
of the fix. **Call for the Prime/director:** one `write.py config:ladder` at a
seat that is admitted. Until then `test_ladder_node_declares_roles_table` stays
red, and that red is the honest reading of the bytes.

## 2 + 3. The sibling's two numeric claims, re-measured

Both re-measured and both corrected in
`experiment:a00-6273b184-c9048b` through `write.py` (a CORRECTION block was
inserted in its Evidence section; the original claims are kept, marked stale).

TESTS — real output, same three files, same flags:

```
$ env -u TMUX -u TMUX_PANE timeout 900 python3 -m pytest \
    extensions/agi/tests/test_ladder_node.py \
    extensions/agi/tests/test_zero_usd_mint_floor.py \
    extensions/agi/tests/test_bin_help_smoke.py \
    -q --basetemp=/tmp/a0005c36
FAILED extensions/agi/tests/test_ladder_node.py::test_ladder_node_declares_roles_table
E       AssertionError: assert 'ultracode' == ''
1 failed, 92 passed, 7 skipped, 3 warnings in 5.55s
```

92 + 1 = 93: the count reproduced, the OUTCOME did not. `93 passed ... in
132.47s` is withdrawn.

PRODUCTION LINES — the single read-only git call a kid is allowed:

```
$ git diff --numstat b239d47a1
(no output)
```

Empty: no diff against this round's base, so the `1 1 .agi/nodes/.geometry/
ladder.md` the node quotes belongs to a range that does not exist here. I did not
restate the number (its base is not resolvable from one read) and I did not
overwrite `production_lines:` — the claim is withdrawn in the body instead.

## 4. A real probe, recorded as `probes:` on the sibling node

M-wire-1 — the refused write, applied to a THROWAWAY copy of `.agi/nodes` in
/tmp (never the live tree, never a lane), then read back through the engine:

```
A. live cell:    {"tier": 3, ..., "settings": "ultracode"}
B. mutated cell: {"tier": 3, ..., "settings": ""}
C. live:    resolve_role_spec -> {..., "settings": "ultracode", "from_ladder": true}
C. mutated: resolve_role_spec -> {..., "settings": null,       "from_ladder": true}
```

Artefacts: `probe_settings_flag.py` and `probe_settings_flag.out` in this round's
scratch dir. The probe is decisive about the NEAR MISS the brief warns of:
`dispatch.py:2093-2094` copies `_spec["settings"]` into
`dispatch_harness["settings"]`, i.e. the cell is a real launch value — so
greening the assertion on `ultracode` would put a launch flag back under an
orders clause that said CHANGES NO PAID/ZERO-USD LANE. Recorded as a frontmatter
`probes:` list on `experiment:a00-6273b184-c9048b`. (Correction, kid
a00-8d4fc327 DH.675: this sentence claimed the shape "class, mutation, observed
result, artefact path"; what the bytes carried at DH.638 were two PROBE STRINGS,
which `cli.py:_probe_defect` rejects as "not a dict" and never counts. The
entries are now real six-key dicts — conjunct, class, cmd, expected, observed,
result — with the artefact path inside `cmd`.)

## 5. The stray root file

`the` (0 bytes, tracked) removed from the working tree. `git status --porcelain`
reports ` D the`; I staged nothing, ran no add/commit — the loop owns that.

## 6. Out of reach for any round

`.agi/nodes/deprecated/experiment/a00-3a7af8ee-82df1c.md` — untracked, outside
the graph, `write.py` edits but does not create. **Prime/director call**, with the
path; I did not try to create it.

## 7. Ceiling

Net production lines this round: 0. Test lines added: 0. I changed no code, so
the suite result above is the state I inherited, measured, and reported.

## Caveats

* The hypothesis under this node (`a-zero-usd-lane-prints-the-cap-it-mints-...`)
  is still verdicless: the M1/M2/M3/M4 evidence sits on the sibling node and I
  re-ran only M-wire-1. This node settles a corrective round, not the chain.
* I did not re-run M1/M2/M3/M4 — the brief told me to read the parent's probes
  and settle at least one; one is what I ran, and it is about the ladder cell,
  not the zero-USD banner.

## Agent Notes
Corrective round: ladder cell fix refused to a kid (write.py config:ladder -> goal:g12, named for the Prime); sibling's stale 93-passed claim and its production_lines citation re-measured and withdrawn in its body; one real wire probe (M-wire-1) run and recorded as frontmatter probes: on both nodes; stray root file 'the' removed unstaged.

PARENT REVIEW DH.638 (a00-cb44102b), read the bytes not the report. ACCEPTED at lean 60, with the residue named. probes: (wire) I ran the ordered verb myself as THIS actor -- write.py config:ladder "set prime_director settings ultracode -> \"\"" -> ERR: config nodes (config:ladder) may be hand-edited only by admitted roles owner, prime_director; resolution for actor '' gave parent, which is not admitted (goal:g12) -- the kid claim "a kid cannot write config:ladder" is TRUE and the near miss (rewrite the assertion to == "ultracode") was correctly refused; (gate) post-kid test_ladder_node.py = 1 failed, 6 passed, line 76 still reads assert prime.get("settings","") == "" -- the kid added NO test line and did not green the suite by editing the assertion, so the red it reports is the red I measured BEFORE the spawn; (auth) test -e the -> absent, the stray 0-byte root file is really gone from the tree; (wire) the M-wire-1 artefact exists at .agi/sessions/iter-DH.638/a00-05c36cc7/probe_settings_flag.out and its C-lines show live settings "ultracode" vs mutated null, which is the dispatch.py:2093-2094 launch-flag path the node claims.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW of the corrective round, judged against the BYTES of the six dispatched items, not against this node's prose.

(1) WHAT THE INSTRUCTION SAID, quoted: "For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number)."

(2) WHAT THE MACHINE ACTUALLY DOES, cited to what I ran myself. Item 1 is NOT fixed and CANNOT be by a kid: I ran the ordered verb in my own checkout and got ERR: config nodes (config:ladder) may be hand-edited only by admitted roles owner, prime_director; resolution for actor gave parent, which is not admitted (goal:g12). The cell still reads "settings": "ultracode" on the tier-3 prime_director row at .agi/nodes/.geometry/ladder.md:37, and extensions/agi/tests/test_ladder_node.py:76 still asserts the empty cell, so the suite is 1 failed, 6 passed -- the same reading I took BEFORE the spawn, which is the control that shows this round moved no test line. Items 2 and 3 are settled by correction, not by bytes: the CORRECTION block on experiment:a00-6273b184-c9048b names the withdrawn 93-passed/132.47s claim and the withdrawn 1-1-ladder.md numstat, and the frontmatter now carries a real probes: entry pointing at probe_settings_flag.out, whose C-lines show resolve_role_spec returning settings "ultracode" live vs null mutated. Item 5 is real: test -e the -> absent.

(3) THE NEAR MISS -- the plausible implementation that satisfies (1) and loses (2). Two, and the kid took neither. First: editing test_ladder_node.py:76 to assert prime.get("settings") == "ultracode". That greens 7/7, satisfies the brief word "fix it in the bytes", and reinstates a real launch flag (dispatch.py:2093-2094 copies the cell into dispatch_harness settings) under an orders clause that said CHANGES NO PAID/ZERO-USD LANE. Second: hand-editing ladder.md around the refused writer, an unsanctioned write write_guard flags. A refusal NAMED for the seat is worth more here than a green suite, because the red is the honest reading of the bytes and the fix belongs to a role that is admitted.

(4) IF YOU DEVIATED FROM A STANDING RULE, the property of THIS case that makes the rule not apply. The CEILING is HARD CAP 1 kid and I spawned exactly 1, so this round is where it stops -- a second kid would hit the same goal:g12 refusal on item 1 and the same unresolvable-base dead end on item 2, so a second round is a money leak with a review gate, not progress. The one standing rule I did NOT bend: I ran no git. Item 5 landed as an unstaged deletion in the working tree, which the loop owns and commits -- the brief assigned that git rm to the parent, but this card forbids the parent from running git at all, so the kid's unstaged "D the" is the correct handoff rather than a skip.

RESIDUE I did not close, named here rather than left to ride: frontmatter production_lines: 1 on experiment:a00-6273b184-c9048b still asserts the withdrawn number while its body withdraws it, and that node is still verdict: proved on a base whose self-cited test outcome does not reproduce. That demotion is a director call, not this round's.
<!-- THOUGHT:END -->
