---
id: experiment:a00-ac017df2-7e6fbd
mint_id: 47fe65e517f644e8b681c911bc8c6c25
type: experiment
parents:
  - hypothesis:send-read-reads-dms-from-the-graph
next_edges: []
confidence: 0.85
edited_by: a00-c9a444b9
evidence_runs:
  - experiment:a00-ac017df2-7e6fbd
loop: hypothesis:send-read-reads-dms-from-the-graph@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "parent P1: tmp fixture; send_dm post-a<-sender-a first dm; read post-a; send_dm second dm; read post-a", "expected": "the second read lists only the newly appended dm; the per-conversation cursor reaches the appended bytes", "observed": "rc=0, second dm listed, first dm not relisted", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "parent P2: monkeypatch send_mod._row_is_quiet to raise, then read post-a over an unread dm", "expected": "read never consults the row quiet setting and still lists the dm", "observed": "rc=0, dm listed, _row_is_quiet never called", "result": "pass"}
  - {"conjunct": 1, "class": "auth", "cmd": "parent P3: --from someone-else read post-a while an unread dm exists", "expected": "refused by name (exit 2), no dm cursor written, body not leaked", "observed": "rc=2, is-not-you refusal, no state file, private dm absent from stdout", "result": "pass"}
production_lines: 13
profile: balanced
role: kid
scaffold_hash: c5e9853ef61de3b5
season: 2
title: read/rooms resolve dm filenames through the ONE aliases table so a former post name still delivers
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-ac017df2-7e6fbd

## What was built

The parent measured that the positional `read <post>` sweep already ignores row
`settings: quiet` (quiet lives only at the nudge sites). The one real gap left
in "every dm addressed to the post" was **name resolution**: `read_dms`
(`send.py:3852`) and `rooms` (`send.py:4071`) matched the reader against the RAW
filename tokens only (`if me not in path.stem.split("--")`). A dm filed under a
post's FORMER name (`old-name--sender.md`) was silently skipped when the post
read under its canonical name.

| seam | before | after |
|---|---|---|
| `read_dms` reader match | raw token equality | `_dm_names_reader` (token IS me, or canonicalises to me) |
| `rooms` dm reader match | raw token equality | same helper |
| alias source | n/a | `_alias_canon` -> the ONE `aliases:` table in `nodes/.geometry/posts.md` |

`_dm_names_reader` (3 production lines) + graph-root resolution (1+1) + two
call-site swaps = **13 added / 2 removed production lines** (`git diff
--numstat`, test file excluded), under the 40-line ceiling. A non-aliased
filename still matches by exact equality (`_alias_canon` returns `None`).

## Red first (measured on the untouched tree)

```
$ python3 -m pytest extensions/agi/tests/test_send.py -q \
      -k "former_name or quiet_independent"
FAILED test_read_lists_a_dm_filed_under_a_former_name_of_the_post
  AssertionError: inbox for new-name: empty
  assert 'old-name dm body' in 'inbox for new-name: empty\n'
FAILED test_rooms_lists_a_dm_filed_under_a_former_name_of_the_post
  AssertionError: []
  assert ('dm', 'old-name--sender-a', 1) in []
1 passed  (quiet-independence: already green today)
```

## Green after the fix

```
$ python3 -m pytest extensions/agi/tests/test_send.py -q \
      -k "former_name or quiet_independent"
3 passed, 333 deselected
$ python3 -m pytest extensions/agi/tests/test_send.py \
      extensions/agi/tests/test_send_quiet.py \
      extensions/agi/tests/test_bin_help_smoke.py -q
1 failed, 414 passed, 4 skipped
  FAILED test_bin_help_smoke[harness_template.py] -- PRE-EXISTING and
  unrelated: harness_template.py has no `--help` handler (empty stdout, rc=0);
  it never imports send.py. Every send.py / quiet test is green.
```

## Tests added (test_send.py, SM.126 block)

1. `test_read_lists_a_dm_filed_under_a_former_name_of_the_post` - RED first;
   now lists the dm, cursor lands on the CANONICAL key `new-name`, second read
   reprints nothing.
2. `test_rooms_lists_a_dm_filed_under_a_former_name_of_the_post` - same rule
   in the `rooms` listing; a non-participant still sees nothing.
3. `test_read_is_quiet_independent` - identical dm bytes under a
   `settings: quiet` row and a row with no setting produce byte-identical
   `read` output and identical cursors (pins the hypothesis's second conjunct).

## Evidence

- Production diff: `extensions/agi/bin/send.py` +13/-2, scoped to `read_dms`,
  `rooms` and one new helper beside `_alias_canon`.
- RED text and GREEN counts above are the actual pytest output from this
  worktree, not a reconstruction.
- `caveats`: the `read` positional dispatch passes the resolved SENDER as the
  reader; an inbox `read old-name` (where the target is the alias) still
  canonicalises the target only, so a dm named under the canonical name and
  read via the old alias is not covered by this fix - out of the falsifier as
  written, which is canonical-reader -> former-filename.

## Agent Notes
read_dms+rooms now resolve dm/room filename tokens through the ONE aliases table (old->new), so a dm filed under a former post name is delivered; +13/-2 production lines, 3 new tests (2 red-first, 1 quiet-independence), test_send/quiet/seatsig green

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-c9a444b9, EF.44). WHAT THE INSTRUCTION SAID: "A kid's tests are its CLAIM, not your evidence ... read each kid's DIFF ... Run one negative probe per claim conjunct yourself and record them as probes:". WHAT THE MACHINE ACTUALLY DOES: the kid's commit 2db0202da carries +13/-2 production lines in extensions/agi/bin/send.py -- a new `_dm_names_reader` that resolves each `--`-separated filename token through the ONE `aliases:` table via `_alias_canon`, and `read_dms` + `rooms` swapped from `me not in stem.split("--")` to that helper -- plus 3 tests in test_send.py. I read those bytes (git show), ran test_send.py + test_send_quiet.py (343 passed), test_bin_help_smoke.py (1 pre-existing, unrelated failure in harness_template.py, a file the diff never touches), and ran 3 parent probes recorded in `probes:` (wire: new dm after a consuming read; wire: `_row_is_quiet` instrumented to raise is never called on the read path; auth: a foreign reader is refused with no cursor write). All three hold. NEAR MISS: a helper matching `_alias_canon(token) is not None` instead of `== me` would list every renamed post's dms to every reader, and the kid's own suite would still pass -- it only asserts the positive case plus a non-participant; the strict equality and my auth probe are what hold the boundary. What the instruction LOST: the target's central behaviour was already built by SM.126 (073b9378e, 09-18) and the parent's pre-spawn measurement confirmed read already ignores row settings -- so this round is a hardening, not a first build; it pins the previously-untested quiet-independence conjunct and closes the former-name gap in the target's own falsifier (`*--<post>.md` filed under an old name). Still open, outside the written falsifier: read matches FILENAME participants, never the `to:` header, so a dm whose filename omits the post is missed; and `_alias_canon` prints a deprecation notice and reloads posts.md per token per file, an unbounded stderr/perf cost on large dm dirs.
<!-- THOUGHT:END -->

Parent accepted (a00-c9a444b9): diff read byte-for-byte (+13/-2 send.py, 3 tests), 343 send+quiet tests green, 3 parent probes pass (P1 cursor wire, P2 quiet-never-consulted wire, P3 auth refusal); verdict proved stands. Caveat: behaviour was already built by SM.126; this round hardens+pins it and closes the former-name falsifier; read matches filenames, not the to: header.
