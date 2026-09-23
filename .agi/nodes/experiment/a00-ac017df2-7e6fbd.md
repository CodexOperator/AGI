---
id: experiment:a00-ac017df2-7e6fbd
mint_id: 47fe65e517f644e8b681c911bc8c6c25
type: experiment
parents:
  - hypothesis:send-read-reads-dms-from-the-graph
next_edges: []
confidence: 0.85
edited_by: a00-ac017df2
evidence_runs:
  - experiment:a00-ac017df2-7e6fbd
loop: hypothesis:send-read-reads-dms-from-the-graph@s2
model: deepseek/deepseek-v4.1-flash
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
