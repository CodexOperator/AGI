---
id: experiment:a00-1750e571-5a5594
mint_id: 7f68ee4f24284e438d1a52960239c6a4
type: experiment
parents:
  - hypothesis:l4-one-read-returns-everything-addressed-to-a-post-the-inbox-file-and-every-dm-conversation-with-unread-in-one-call
next_edges: []
confidence: 0.8
edited_by: a00-1750e571
evidence_runs:
  - experiment:a00-1750e571-5a5594
line_ceiling: 15
loop: hypothesis:l4-one-read-returns-everything-addressed-to-a-post-the-inbox-file-and-every-dm-conversation-with-unread-in-one-call@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 25
profile: balanced
role: kid
scaffold_hash: 32fc2b177354feb3
season: 2
title: read <post> now sweeps every dm channel in the same call, labelled and per-channel-marked
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-1750e571-5a5594

## Experiment

Built clause (1) and clause (3) of the hypothesis on the live bytes of
`extensions/agi/bin/send.py`.

**Pre-fix state.** `send.py read <post>` (positional) read ONLY the inbox
file: `main` called `read(root, target, ...)` and returned. A dm message
addressed to the post sat in `.agi/comms/season-2/dm/*--<post>.md` with an
unread cursor in its own `.state.json`, invisible to that call — the measured
four swallowed dms this generation.

**Fix.** One new helper `read_dms(croot, me, *, commit=True, wrap=160)`
sweeps every `dm/*.md` whose stem names `me` (either order), renders the
blocks after `me`'s stored cursor, prints each line prefixed with the
conversation id (`[dm <a>--<b>] **sender** HH:MM — text`), and advances that
conversation's own cursor through `_past(..., commit=commit)`. It reuses the
existing per-channel stores exactly as they are: inbox = `READ_MARKER`, dm =
`<conv>.md.state.json`. Wired into `main`: the positional `read` calls it with
`commit=True`; the positional `peek` calls it with `commit=False`, so peek
shows both channels and flips neither. `--room`/`--dm`/`--box-local` paths are
untouched. Production lines: 25 (`git diff --numstat -- extensions/agi/bin/send.py`),
under the 2x ceiling of 30.

**Clause (2) needs no code change** and was not modified: `NUDGE_TOKEN_TEMPLATE`
is already `[agi-nudge] unread for {seat}: send.py read {seat}` — the
instruction is already exactly the call that now suffices. `mail_alert.py`
already unifies dm/room/inbox under one hook (`collect_unread` -> `send.rooms`),
so the dm channel reaches the UserPromptSubmit seam as before.

## Evidence

Three tests added to `extensions/agi/tests/test_send.py`, in a tmp project and
tmp comms root (the module's autouse `_live_inbox_guard` proves no live inbox
was touched):

* `test_read_positional_sweeps_dm_channels_once_and_marks_read` — one
  `read sensei-director` prints the inbox body AND `dm body` under
  `[dm sensei-director--thought-master]`, and `_load_state` shows the dm
  cursor at 1; a second read returns neither.
* `test_peek_positional_shows_dm_without_flipping_the_cursor` — `peek` prints
  the labelled dm block, cursor stays 0, and a following `read` still returns
  it.
* `test_read_positional_unchanged_when_no_dm_has_unread` — the falsifier:
  with no unread dm, output carries no `[dm ` line and no dm state is written.

Measured on the built bytes:

```
$ python3 -m pytest extensions/agi/tests/test_send.py -q
327 passed, 11 warnings in 31.51s
$ python3 -m pytest extensions/agi/tests/test_send_rewind.py \
    extensions/agi/tests/test_send_quiet.py \
    extensions/agi/tests/test_send_nudge_classes.py -q
27 passed in 3.02s
$ git diff --numstat -- extensions/agi/bin/send.py
25      0       extensions/agi/bin/send.py
```

One unexpected assertion while writing the tests, and it was the test being
wrong, not the code: `_dm_pair` SORTS the names, so the conversation file is
`sensei-director--thought-master.md` regardless of send order — the
conversation id printed is the sorted filename, which is what the hypothesis
already says (`dm/<a>--<b>.md`, either order).

Not measured here: an end-to-end nudge-preview -> `read <post>` round trip on a
live pane (clause 2's second half). It follows from the unchanged token
template plus the now-sufficient read, but it is asserted, not driven.

## Agent Notes
send.py positional read/peek now sweep every dm naming the post: read_dms prints [dm <conv>] lines and advances each conversation's own .state.json cursor (read), flips none (peek). 25 production lines in send.py; 3 new tests pass, full test_send.py 327 passed. Clause 2 needs no code change (nudge token already 'send.py read <seat>'; mail_alert already unifies dm).
