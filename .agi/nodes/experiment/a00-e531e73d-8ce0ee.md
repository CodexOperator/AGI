---
id: experiment:a00-e531e73d-8ce0ee
mint_id: c2ec82f8d178491d840a2cb3f5f56ec3
type: experiment
parents:
  - hypothesis:dm-reader-resolves-aliases-once-per-read
next_edges: []
confidence: 0.85
edited_by: a00-b96edb9d
evidence_runs:
  - experiment:a00-e531e73d-8ce0ee
loop: hypothesis:dm-reader-resolves-aliases-once-per-read@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "probe_ef64.py <fixed send.py> over an 8-dm-file/16-token fixture", "expected": "read_dms loads posts.md 1; rooms loads 1", "observed": "read_loads=1, rooms_loads=1 (pre-fix: 10/10)", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "same fixture, each of two aliases of me appears in 2 files", "expected": "one notice per alias per call: old-name=1, alt-old=1, total=2", "observed": "old-name=1, alt-old=1, total=2 (pre-fix: 2/2/5)", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "same fixture, token other-old maps to a different post", "expected": "zero deprecated-alias notices for other-old", "observed": "other-old_notices=0 (pre-fix: 1)", "result": "pass"}
  - {"conjunct": 4, "class": "wire", "cmd": "read_dms and rooms driven on the fixture; selection compared to pre-fix copy", "expected": "selection set identical to pre-fix; call site routes through the passed-in table", "observed": "both select {old-name two, alt-old two, new-name one}; identical to pre-fix", "result": "pass"}
production_lines: 60
profile: balanced
role: kid
scaffold_hash: ad2f3ee3abaf2e3a
season: 2
title: DM reader loads the alias table once per read/rooms sweep (EF.64)
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e531e73d-8ce0ee

## Experiment

IMPLEMENTED the fix (a build order, not a measurement).

### Pre-fix defect (tip f36cc2420, bytes verified)
`_alias_canon` re-loaded `nodes/.geometry/posts.md` on EVERY call, and
`_dm_names_reader` called it once per `--` token per dm file. Sweep fixture:
5 dm files, 11 tokens.

### Fix in `extensions/agi/bin/send.py`
| before | after |
|---|---|
| `_alias_canon(root,name)` loads + prints per call | `_alias_table(root)` loads ONCE, prints nothing |
| `_dm_names_reader(root,stem,me)` per token | `_dm_names_reader(stem,me,aliases,noticed)` — table passed in |
| read_dms/rooms call it per file | build `aliases` + `noticed` once per call |

Notice rule: at most once per alias per call, and ONLY for a token that
canonicalises to `me`; an alias of a DIFFERENT post prints nothing.

### Pre-fix red (test run BEFORE the fix)
```
$ python3 -m pytest extensions/agi/tests/test_send.py -q -k resolves_the_alias_table_once
FAILED test_read_resolves_the_alias_table_once_per_call  AssertionError: {'n': 6}
FAILED test_rooms_resolves_the_alias_table_once_per_call AssertionError: {'n': 6}
2 failed, 336 deselected
```

### Post-fix green
```
4 passed   (2 new + EF.44 former_name read/rooms)
338 passed test_send.py (full file)
2 passed   test_rename_post.py -k alias (_alias_canon contract unchanged)
```

## Evidence

- `read_dms`: posts.md loads 6 -> 1 per call.
- `rooms`: posts.md loads 6 -> 1 per call.
- notice `old-name -> new-name`: once (was 2, one per matching file).
- notice `other-old -> other-new`: 0 (was 1, wrongly printed for a post that is not the reader).
- selection set unchanged: `rooms` rows == {old-name--sender-a, old-name--sender-b, new-name--sender-e}.
- production_lines measured: 60 (`git diff --numstat send.py`: 42 ins / 18 del) — over the 40 ceiling, under 2x, no re-brief.
<!-- BODY:END -->

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-b96edb9d, EF.64). (1) THE INSTRUCTION SAID: the node testable_claim demands that _dm_names_reader "resolves the alias table once per read/rooms call instead of once per `--` token per dm file, so posts.md is loaded once per call and the `deprecated alias used` notice prints at most once per alias per call and never for a token that does not match the reader". (2) THE MACHINE ACTUALLY DOES: on the post-fix bytes, send.py:3067 _alias_table resolves+loads posts.md once and NEVER prints; send.py:3088 _dm_names_reader(stem, me, aliases, noticed) does a dict lookup and prints only when str(canon)==me and the alias is not already in the per-call noticed set; read_dms (send.py:3890) and rooms (send.py:4120) each build aliases once before their glob loop. I RAN probe_ef64.py over a LARGER fixture than the kid used (8 dm files, 16 tokens, two distinct aliases of me): post-fix read_loads=1, rooms_loads=1, old-name notice=1, alt-old notice=1, other-old notice=0, total=2, selection set identical to the pre-fix copy; the pre-fix copy from git HEAD gave 10/10 loads, 2/2 notices and 1 WRONG other-old notice. (3) THE NEAR MISS: caching the table but still routing tokens through _alias_canon would make posts.md load once (conjunct 1 satisfied) and still print "deprecated alias used" for a token whose canonical is a DIFFERENT post -- conjunct 3 lost under an implementation that reads as a pure cache. A process-global branches-style _warned flag would make the notice "at most once" while still emitting it ONCE for a non-matching token. Both are refused here because the notice is gated on the match and deduped in a per-call set, not per-process. (4) DEVIATION: none from a standing rule. One behaviour note, not a defect: read_dms now resolves the table unconditionally (send.py:3890) even when the dm dir is absent, where the pre-fix path loaded nothing for an empty root; the claim is about once per CALL, so this is inside contract and costs one read. I checked every deliverable the kid named against the diff: send.py and test_send.py are both carried, no deliverable is claimed-but-absent. VERDICT: proved.
<!-- THOUGHT:END -->

## Agent Notes
Built _alias_table (loads posts.md once, no print) + _dm_names_reader(stem,me,aliases,noticed); read_dms/rooms build the table once per call. Pre-fix red: 6 posts.md loads, notice printed for non-matching alias; post-fix 1 load, notice once per matching alias, zero for a different post. test_send.py 338 passed, test_rename_post alias 2 passed.
