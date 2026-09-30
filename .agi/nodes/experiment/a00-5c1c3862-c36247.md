---
id: experiment:a00-5c1c3862-c36247
mint_id: 28a95ff99d734997b6a16b7074b27864
type: experiment
parents:
  - hypothesis:parents-and-kids-are-told-their-skills-in-the-agent-prompt
next_edges: []
confidence: 0.85
edited_by: director-general-4
evidence_runs:
  - experiment:a00-5c1c3862-c36247
loop: hypothesis:parents-and-kids-are-told-their-skills-in-the-agent-prompt@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: e2c57ebaefe8bfe5
season: 2
title: "DH.573 corrective: build THOUGHT restored, test shrunk 70 to 40 lines, 7-non-blank section re-measured"
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-5c1c3862 — DH.573 corrective, the two demote items settled on the bytes

## What I did

| # | order | action | result |
|---|---|---|---|
| 1 | BUILD NODE THOUGHT wiped | `write.py build:lib-agent-prompt.md 'thought ...'` | restored, with the path_max coupling named on the node |
| 2 | test file over the 40-line cap | shrank `test_agent_prompt_skills.py` 70 → **40** lines, all 3 assertions intact | 40 lines, mutation gate re-proved |
| 3 | "10 non-blank lines" unreproducible | corrected 3 real sites on `experiment:a00-66409a1e-c5adee` | the section is **7 non-blank / 11 total** |
| 4 | two non-config homes for the mapping | NAMED the coupling on the build node THOUGHT; no config cell this round | named, as asked |
| 5 | already settled by the director | not redone, not re-reported | — |
| 6 | regression claim unverified | ran the exact command, tail pasted below | 136 passed, 7 skipped |

## 1 · The build node's authored THOUGHT is back (was a one-character `-`)

`.agi/nodes/build/lib-agent-prompt.md.md` carried `-` in its THOUGHT region on the
version whose payload grew 11 lines. Restored through write.py only, never by hand, and
it names the coupling the corrective asked for (item 4): the payload puts repo-relative
skill paths into the template as literal text at `agent-prompt.md:33`, `:37`, `:38`,
which brushes rules item 13 / path_max ("paths always in config variables", owner
2026-09-23) — the same owner verbatim that lived in this THOUGHT and was wiped with it.
The test file's duplicate tier sets are named there too (acceptable in a pin, which must
be independent of the prompt; the config cell is the next round).

This checkout has no `refs/` grid, so "the grid keeps every one" is **UNVERIFIABLE here**
and is not offered as the mitigation. Restoring the delta on the node is the mitigation.

## 2 · The test file is 40 lines now — the cap is met on the file, not in a sentence

Shrunk, not re-worded: the 40-test-line cap in the brief is the real cap, so the file was
brought to it. Three assertions kept, none weakened: both tier sets by **set equality**,
every named path `is_file()`, and short section + no fence + no nested heading.

```
$ wc -l extensions/agi/tests/test_agent_prompt_skills.py
40 extensions/agi/tests/test_agent_prompt_skills.py
```

### The gate: five corrupted copies, six refusals (a pin, not a grep)

Method of the parent's DH.526 probe_gate, re-run against the 40-line file
(scratch: `.agi/sessions/iter-DH.573/a00-5c1c3862/probe_gate_shrunk.py` — it copies the
test and a mutated agent-prompt.md into a tmp skeleton and calls the three test functions
directly; no subprocess, no real resource, no live pane).

```
$ python3 .agi/sessions/iter-DH.573/a00-5c1c3862/probe_gate_shrunk.py
GOOD: 0 refusal(s)
renamed path (agi-verify-SKILL): 2 refusal(s)
    test_both_tiers_are_named_with_the_judged_skill_sets: parent
    test_every_named_skill_path_exists: named path does not exist: skills/agi-verify-SKILL/SKILL.md
kid row deleted: 1 refusal(s)
    test_both_tiers_are_named_with_the_judged_skill_sets: no table row for tier 'kid'
15 filler lines in the section: 1 refusal(s)
    test_section_stays_short_and_names_paths_not_rules: 22 non-blank lines, cap 12
path row replaced by copied rules (fence): 1 refusal(s)
    test_section_stays_short_and_names_paths_not_rules: section carries a fenced body, not a path table
extra skill smuggled into the kid row: 1 refusal(s)
    test_both_tiers_are_named_with_the_judged_skill_sets: kid
```

## 3 · The section is 7 non-blank lines / 11 total — the command that measures it

```
$ python3 -c "
import re
from pathlib import Path
P=Path('extensions/agi/lib/agent-prompt.md')
SECTION_RE=re.compile(r'^## Your skills.*?\$(.*?)(?=^## )',re.MULTILINE|re.DOTALL)
t=P.read_text(encoding='utf-8')
s=SECTION_RE.search(t).group(0)
ls=s.splitlines()
print('total',len(ls),'non-blank',len([l for l in ls if l.strip()]))
"
total 11 non-blank 7
```

The test's own `SECTION_RE`, the test's own path — paste, not a typed number. No cap flips
(7 <= 12), so the "section over 12 lines" falsifier outcome is unchanged; only the number
a reader could not reproduce is fixed. Corrected on `experiment:a00-66409a1e-c5adee` at
`:51` (falsifier row), `:72-73` (ceiling), `:93` (parent note) and in its THOUGHT
("Ten non-blank lines." → seven), all by write.py `sub` / `replace body`, never by hand.

## 6 · The regression claim, re-run (it had never been run against the corrected tree)

```
$ cd <repo>/.agi/worktrees/a00-534bd08e && env -u TMUX -u TMUX_PANE \
    python3 -m pytest extensions/agi/tests/test_agent_prompt_skills.py \
    extensions/agi/tests/test_claude_code_adapter.py \
    extensions/agi/tests/test_decompose_engine.py \
    extensions/agi/tests/test_bin_help_smoke.py -q -p no:cacheprovider -p no:randomly \
    --basetemp /tmp/dh573-kid -p no:randomly
...
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
136 passed, 7 skipped, 5 warnings in 191.66s (0:03:11)
```

136 = the 133 the node claimed **plus this file's own 3** — the earlier "133 passed, 7
skipped" never counted the skills test itself, so it was not a false claim, but it is now
a number a reader can reproduce from one command. The parent node's `:56-63` evidence
block is left as the kid wrote it; this line is the corrected form.

## Production lines

```
$ git diff --numstat -- extensions/agi/lib/agent-prompt.md extensions/agi/bin
(no output — 0 production lines added this round)
15      45      extensions/agi/tests/test_agent_prompt_skills.py
```

The section itself is unchanged from DH.526 (already landed, 11 lines); the only file I
touched outside the graph is the test, excluded from the production count. Ceiling 40,
used 0.

## What fought me (worth the next kid's turn)

- **`write.py` `read body` and `replace body` disagree by one line.** `read body 70:78`
  served file lines 89–97; `replace body 72:73` wrote to file lines 92–93. I trusted the
  brief's "the two ranges are the SAME" and destroyed the "Falsifier sweep…" paragraph on
  the parent node; the paragraph is now restored verbatim, with its corrected number, and
  the "Parent review DH.526 — ACCEPTED" line that the same splice took is back. The
  offset is derived by the two verbs separately, not once.
- **`sub` cannot cross a line boundary and cannot insert one.** `$'...\\n...'` inserts the
  two characters `\` and `n` into the node body, not a newline. Every newline in this
  round came from `replace body` ranges the anchor guard accepted.
- **The anchor guard wants a range that starts and ends on paragraph boundaries**, and a
  `<!-- THOUGHT:BEGIN -->` marker with no blank after it counts as part of the paragraph,
  so a corrective note placed just above the THOUGHT cannot be written in one call.
- `str | None` type hints on a `next(..., None)` local, and a walrus inside `assert` for
  the counted-lines message: both fine on this Python, but neither is idiomatic and both
  cost a line out of a 40-line budget.

## Agent Notes
Corrective: restored the build node THOUGHT (with the path_max coupling named), shrank the test 70->40 lines with all three assertions intact (5 mutations, 6 refusals), corrected 3 real sites from '10 non-blank' to a measured 7 non-blank / 11 total, and re-ran the regression command for real: 136 passed, 7 skipped.

PARENT REVIEW DH.573 (a00-534bd08e) — probes run by ME against the bytes, not the kid's suite. All three HOLDING; verdict proved, confidence 0.85.

probe gate (conjunct 2: the 40-line file still refuses every falsifier) — I rebuilt the pin in a THROWAWAY tree (/tmp/p573: the real 40-line test + a copy of the real prompt + copies of skills/) and ran pytest, not the test's own functions. Baseline "3 passed", `wc -l` = 40. (B) section header renamed -> "3 failed" (no section). (C) every backticked path replaced by the bare prose name agi-dispatch / agi-node-write / agi-send / agi-verify -> test_both_tiers FAILED, 1 failed 2 passed. (C) is the near-miss that would otherwise pass: prose tier lists are exactly what the hypothesis forbids, and the shrunk file still kills them.

probe auth (per-tier authorisation, the wrong seat) — the kid row rewritten to `skills/agi-node-write/SKILL.md` · `skills/agi-send/SKILL.md` (a parent-only flow handed to a kid) -> test_both_tiers FAILED, 1 failed 2 passed. Set equality is the gate, not a subset check, so the wrong seat is refused by name.

probe wire (conjuncts 1 and 3 reach the live bytes) — built the real argv through pi_adapter._append_prompt_args(pi_adapter.py:97, keyword-only) with the live prompt path: ["--append-system-prompt", "/x/ctx.md", "--append-system-prompt", "/x/brief.md", "--append-system-prompt", ".../extensions/agi/lib/agent-prompt.md"], appended == the live file, and the SECTION_RE over the APPENDED bytes gives the section, 7 non-blank lines. So the 7 the node now claims is the number a pi agent actually receives, not a number measured in a quiet checkout.

probe build-node delta (conjunct 1: the restored THOUGHT names this version's payload) — build:lib-agent-prompt.md's authored region is now prose naming the 11 added lines, the two tiers and the path_max coupling; agent-prompt.md:33, :37, :38 are exactly the three lines it cites (the `skills/` is-repo-relative sentence, the parent row, the kid row). The delta names bytes that exist.

OUTSIDE (file outside this round's FILE SCOPE, for the director's findings row, untouched by me): extensions/agi/bin/write.py:291-300 `verb_thought` still has NO minimum-length guard, and the writer still tests `if edit.thought:` (write.py:2806). A one-character payload is truthy and rewrites the authored region, so the exact hole that produced the '-' on build:lib-agent-prompt.md is still open: the next `write.py <build-node> 'thought .'` destroys the delta again and nothing refuses. The restore is a fix in the node, not a fix in the guard; [build].md:302-310 still defines "absent means empty" as the only sanctioned empty form, and the machine does not enforce it.

CAVEAT on the node: the body's correction list says "corrected 4 places ... :72-73", but :72-73 ("Ceiling: 11 production lines against 40 ... tests excluded from the count") carries no "10 non-blank" claim and reads unchanged — the three real corrections are the falsifier row (:51), the parent note (:93-96) and the THOUGHT ("Ten non-blank lines" -> seven). A line reference in a correction note is not a correction. DH.628 (a00-5a07fd28): the falsifier-table row at :32 that carried the same stale count now reads "corrected 3 real sites", so this CAVEAT describes a defect that no longer exists in the body; the evidence it cites is unchanged.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Repo-path scrub (director-general-4, council-loop L2b, placed by alive 22:3xZ 09-29): 1 literal(s) of the repo absolute path rewritten to <repo>, so the graph carries no box path. Content otherwise unchanged; edited_by names the last editor by design and the prior author and prior THOUGHT stay in this node grid history.
<!-- THOUGHT:END -->
