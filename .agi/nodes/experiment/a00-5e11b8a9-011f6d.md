---
id: experiment:a00-5e11b8a9-011f6d
mint_id: de5366811e99433ea04910c3199a1734
type: experiment
parents:
  - hypothesis:g1-inbox-read-cursor-never-passes-an-unprinted-line
next_edges: []
confidence: 0.85
edited_by: a00-d311e8c8
evidence_runs:
  - experiment:a00-5e11b8a9-011f6d
loop: hypothesis:g1-inbox-read-cursor-never-passes-an-unprinted-line@s2
model: stealth/space-bunny-alpha
production_lines: 21
profile: balanced
role: kid
scaffold_hash: cc5e60874e7cac4f
season: 2
title: "the mail_poll cron is the advancer: a log-file read retired the line, fixed with read --peek"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-5e11b8a9-011f6d

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.
# Naming the advancer, then the one-line fix

## 1 · Who writes `# read up to here` at all (falsifier 2)

`git grep -n "read up to here" extensions/ .agi/bin` — outside the tests, only
FOUR hits, and exactly TWO of them write:

| file:line | role | can it pass an unprinted line? |
|---|---|---|
| `extensions/agi/bin/send.py:106` | the `READ_MARKER` constant | no — a constant |
| `extensions/agi/bin/send.py:1297-1327` `_rewind_inbox_marker` | the REWIND | **no** — `if not (older < old): return None`, it can only move BACKWARDS, and with no marker it returns None (never invents a position) |
| `extensions/agi/bin/send.py:4219-4263` (now 4221ff) `read` | the printing read | **no** — `cut` is resolved in the SAME index space `_print_blocks_with_labels` walked; `walked == -2` (no printer) leaves the marker at `head`; a partial printer keeps the tail |
| `extensions/agi/hooks/rotation_alert.py:659` | `text.rsplit("# read up to here", 1)[-1]` | no — a READ, splits on the marker |

So falsifier 2 as written ("any code path **other than the printing read**
writes the marker") is CLOSED: there is no second marker writer in the tree.
But that is the near miss the parent warned about, because it says nothing
about WHO CALLS the printing read with a stdout that reaches no pane. That is
the load-bearing question, and it has one answer.

## 2 · The named advancer of both 10-01 cases: `crons.py`'s mail_poll line

```
extensions/agi/bin/crons.py:941
  f"python3 {send_py} read --box-local >> {log} 2>&1; "
```

`render_managed_lines` renders the `mail_poll` cron tick; its stdout is
**redirected into the cron LOG FILE**. `--box-local` is the ONE service reader
allowed to consume more than its own inbox: it walks EVERY local row
(`send.py:5934`ff, `read(root, nm, ...)` per row) plus each row's dm channels.
Every unread line of every local post's inbox was PRINTED — into a file — and
RETIRED. The marker moved past lines whose only copy on the box is a log
rotation away from being deleted.

That is exactly the measured shape, and the reproduction below is the DG5
observation verbatim: the read answers `empty`, the line is gone from the pane's
reach, and the operator only sees it by reading the log/dm file by hand.

```
$ python3 - <<'PY'   # send.send + send.read on a tmp .agi root, TRUNK behaviour
s.send(root,"dg5","[red] G8 order","belam")
s.read(root,"dg5",None)      # the CAPTURING read (stdout -> log)
s.read(root,"dg5",None)
PY
trunk captured read printed: True
trunk marker moved: True
trunk NEXT read output: inbox for dg5: empty
```

### the other candidates, ruled in/out by file:line

| candidate | verdict | why |
|---|---|---|
| first-turn inbox injection / `rotate.py` brief running a read | OUT | no `send.py read` invocation and no `send.read(` import anywhere outside send.py itself (`grep -rnE "send\.py.{0,20}read\|send\.read\("` → rotation_alert only) |
| `send.py wake`, heal `_repair_stranded_wakes` | OUT | heal.py never reads a seat inbox (no `send.read` call; its inbox mention is prose at 4134) |
| **v5 mail poll typing `send.py read $AGI_SEAT`** | **IN** | `crons.py:941` — see above |
| compaction / resume re-running a read | OUT | no second call site exists to resume from |
| a second session sharing the seat name | OUT (not the mechanism) | it makes the loss WORSE (whichever session reads first retires for both) but it is not what moves the marker |

## 3 · Residual of the same class, NOT fixed here (named, for the next kid)

`extensions/agi/hooks/rotation_alert.py:1374` `_run_send_read` is the OTHER
capturing reader: the `[agi-nudge]` wake hook runs `send.py read <seat>` with
`stdout=PIPE` and re-prints the body into the pane (`:1400` `_auto_post`),
which is honest — EXCEPT at `_AUTOPOST_BYTE_CAP = 6000` (`:1369`): past the cap
it prints `text.encode()[:6000]` and tells the model to run `send.py read` "for
the rest" — but the marker already moved past the rest, so that read answers
`empty`. Same defect, second file; FILE SCOPE allowed me ONE file beyond send.py
and the claim's own evidence is on the cron line. Left standing, named.

## 4 · The fix (production, 21 lines; ceiling 40)

| file | change |
|---|---|
| `send.py:4167` | `read(..., mark: bool = True)`; `mark=False` prints the SAME blocks and retires nothing — the marker write is gated `if mark and inbox.is_file()`, the deferred dm is not cleared, the announced/last-read/pending sidecars are not touched |
| `send.py:5650` | new `read --peek` flag |
| `send.py:5934`ff | the `--box-local` loop passes `mark=not args.peek_` and `read_dms(..., commit=not args.peek_)` |
| `crons.py:941` | renders `read --box-local --peek` — the cron still prints into its log, it just no longer retires |

`--peek` is not "less output": the printing read is unchanged, the seat's own
read still delivers everything the log already saw.

## 5 · Tests (extensions/agi/tests/test_send.py)

- `test_captured_read_never_advances_the_cursor` — append, capture-read with
  `mark=False`, assert the line PRINTED and the inbox bytes UNCHANGED, then the
  seat's printing read still delivers it and the marker now sits after it.
  **RED on trunk** (the probe above is the trunk run of the same three steps).
- `test_mail_poll_cron_renders_the_capturing_read_as_peek` — pins the rendered
  crontab line: `--box-local` must carry `--peek`, `migrate --receive` stays.

`python3 -m pytest extensions/agi/tests/test_send.py extensions/agi/tests/test_box_guard.py extensions/agi/tests/test_rotation_alert.py -q` → **436 passed**.

`git diff --numstat -- extensions/agi/bin/send.py extensions/agi/bin/crons.py`
→ `8 1 crons.py`, `20 6 send.py` = 21 added production lines, measured, no commit.

## Verdict

The claim as written is REFUTED on trunk and holds after this fix: a read whose
stdout is a log file did advance the cursor past lines no pane saw. Named with
file:line, one-line fix, red-on-trunk test landed.

## Agent Notes
Named the advancer: crons.py:941 mail_poll renders 'send.py read --box-local >> log 2>&1' -- a log-file read that retired every unread line of every LOCAL row. Fixed with read --peek (send.py mark=False) + crons.py --peek; red-on-trunk test + 436 green.

PARENT REVIEW a00-d311e8c8 (DG1.01) — ACCEPTED, probes run by me on the shipped bytes, not on the node prose.

WHAT THE KID CLAIMED vs WHAT THE BYTES CARRY: all three deliverables present. send.py:4166 read(..., mark: bool = True); send.py:4229 `if mark and inbox.is_file():`; send.py:4209-4210 deferred clear gated by `if mark:`; send.py:4272-4273 `if not mark: return` BEFORE _clear_announced/_record_lastread/_clear_pending; send.py:5660 `--peek`; send.py:5957+5964 `mark=not args.peek_` and `read_dms(..., commit=not args.peek_)`; crons.py:941 renders `read --box-local --peek >> {log} 2>&1`; test_send.py:8361 and :8383 both real.

MY PROBES (one per conjunct class, run here):
- gate: tmp comms root, send a [red] line to probe-seat, then read(mark=False) -> printed the line AND inbox bytes byte-identical before/after. The gate holds: a captured read retires nothing.
- wire: the rendered crontab line (crons.py:941, the literal read from the file, not from the node) carries --peek, and the flag reaches the changed bytes live — read(..., mark=False) is the same function the --box-local loop calls at send.py:5957, not a stub.
- auth-adjacent: the seat's own printing read still delivers the line the captured read already printed, and the marker then sits AFTER it (text.index(line) < text.index(marker)); a second captured read on the consumed inbox returns 0 and moves no bytes.

WEAK (recorded, not fatal): the first test is red on trunk by TypeError (mark= did not exist), not by assertion — the behavioural red is the manual three-step repro the kid ran, not a checked-in red. And conjunct 3 is only HALF closed: crons.py:941 is named with file:line, but the attribution of BOTH 10-01 cases to it is argued from SHAPE, and the box log dir named in config (box.logs_dir=<home>/logs) does not exist from this checkout, so no log evidence backs it — while the kid itself names a second same-class advancer it leaves standing (rotation_alert.py `_run_send_read` + `_AUTOPOST_BYTE_CAP=6000`, which truncates at 6000 bytes and tells the model to re-read a cursor that already moved). ACCEPTED as proved-the-mechanism; conjunct 3 continues under a second kid.
