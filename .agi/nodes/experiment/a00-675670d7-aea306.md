---
id: experiment:a00-675670d7-aea306
mint_id: a13c1abace754296a73e749cd7085c7f
type: experiment
parents:
  - hypothesis:l4-quick-migrate-one-verb-moves-a-post-to-another-box-as-a-fresh-rotation-from-the-card-or-a-transcript-fork-over-the-git-messaging-layer
next_edges: []
confidence: 0.6
edited_by: a00-2a62c783
evidence_runs:
  - experiment:a00-675670d7-aea306
line_ceiling: 120
loop: hypothesis:l4-quick-migrate-one-verb-moves-a-post-to-another-box-as-a-fresh-rotation-from-the-card-or-a-transcript-fork-over-the-git-messaging-layer@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "a --dry-run prints every step by alias and touches nothing", "class": "gate", "cmd": "rotate.py migrate --post p --to boxB --dry-run (AGI_BOX=boxA)", "expected": "rc 0; steps 1..6 by alias; nothing created", "observed": "rc 0; step 1:..step 6:; 'dry-run: nothing touched'; tmp/comms absent", "result": "held"}
  - {"conjunct": "a migrate to the box the post is already on is refused BY NAME", "class": "wire", "cmd": "rotate.py migrate --post p --to boxA --dry-run", "expected": "rc 1; REFUSED, nothing touched", "observed": "rc 1; REFUSED: a migrate to the box the post is already on (boxA) (nothing touched)", "result": "held"}
  - {"conjunct": "an unknown mode is refused BY NAME before any write", "class": "wire", "cmd": "rotate.cmd_migrate(mode=teleport)", "expected": "rc 1; names the mode", "observed": "rc 1; REFUSED: unknown mode 'teleport' (one of rotate|fork); nothing touched", "result": "held"}
  - {"conjunct": "the record round-trips every field and admits only kind=migrate", "class": "gate", "cmd": "format_record -> parse_record; parse a kind:dm record", "expected": "parsed == rec; non-migrate kind and non-record return None", "observed": "parsed == rec; kind:dm -> None; no-frontmatter -> None", "result": "held"}
  - {"conjunct": "the record is signed with the post key and a tampered byte does not verify", "class": "auth", "cmd": "send._mint_seat_key(p) -> format_record(sign_root) -> verify_record(pub_hex)", "expected": "sig present; verify True; one changed byte False; unsigned False", "observed": "sig: ed25519:...; verify True; rotate->fork False; unsigned False", "result": "held"}
  - {"conjunct": "--apply writes ONE record, named by aliases only, under <comms>/migrate", "class": "gate", "cmd": "rotate.py migrate --post p --to boxB (comms_root stubbed to tmp)", "expected": "exactly 1 *.md; fields correct; prints 'signed with the p key'", "observed": "1 file; mode=rotate source_box=boxA target_box=boxB; sig present; line printed", "result": "held"}
  - {"conjunct": "(5) one REAL dry run against local-town", "class": "wire", "cmd": "rotate.py migrate --post <post> --to local-town --dry-run", "expected": "prints the plan with no live write", "observed": "NOT RUN: no second box or its clone exists on this host (only config provider 'local-town')", "result": "not run"}
production_lines: 212
profile: balanced
role: kid
scaffold_hash: 7e78d39ee043bfdc
season: 2
title: "SM.123 quick-migrate source slice: the ONE signed cross-box migrate record kind + the migrate verb plan/refusals; commit/push/receive named not built"
town: core
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-675670d7-aea306

## Experiment

SM.123 QUICK-MIGRATE, SOURCE-SIDE SLICE. The parent hypothesis is a whole
cross-box moving day (card gate, carryover commit, ref push, mail_poll
receive, seated line). This round builds the ONE thing every later slice
must agree on -- the `migrate` record kind -- plus the `rotate.py migrate`
verb's plan and its refusals. The git steps (carryover commit, ref push)
and the target-side receive are named steps 2/3/5 and are NOT built here:
a kid never runs the landing's git, and the target acts on its own tick.

Built bytes:

- `extensions/agi/bin/migrate_channel.py` (118 lines) -- ONE record kind:
  `record()`, `record_name()` (aliases only, sanitized), `format_record()`
  (YAML frontmatter + optional `sig:`), `parse_record()`, `verify_record()`.
  The signed envelope is `send._canonical_msg(ts, post, target_box, <nine
  fields>)`, so the signer's format and the reader's parse cannot drift.
- `extensions/agi/bin/rotate.py` `migrate` subcommand + `cmd_migrate()`
  (94 lines) -- plan by alias, refusals by name, `--dry-run` touches
  nothing, otherwise ONE signed record under `<comms>/migrate/`.

Files touched (production): `rotate.py`, `migrate_channel.py`. Test:
`extensions/agi/tests/test_migrate_channel.py` (8 tests, all pass).

## Evidence

Commands and observed output (fixture root, `AGI_BOX=boxA`):

```
$ python3 extensions/agi/bin/rotate.py migrate --post p --to boxB --dry-run
migrate p: boxA -> boxB (mode rotate)
  step 1: card: refuse a stale where-it-stops slot by name (rotate's own gate)
  step 2: carryover commit: the post worktree's diffs as ONE commit on its branch
  step 3: push: refs/agi/posts/p (the post branch rides git)
  step 4: record: ONE migrate record, signed with the post key
  step 5: target receive: the mail_poll tick seats the successor from the ref
  step 6: seated line: ONE answer back on the same channel
  dry-run: nothing touched
$ python3 extensions/agi/bin/rotate.py migrate --post p --to boxA --dry-run
REFUSED: a migrate to the box the post is already on (boxA) (nothing touched)
$ python3 -m pytest extensions/agi/tests/test_migrate_channel.py -q
8 passed
$ python3 -m pytest extensions/agi/tests/test_rotate_verb.py \
    extensions/agi/tests/test_rotate_verb_resolvers.py \
    extensions/agi/tests/test_send.py -q
356 passed
```

The apply path (comms root stubbed to tmp) wrote exactly one file,
`2026-09-18T22-07-55.223813-00-00-p--boxB.md`, under `<comms>/migrate/`,
with all nine fields, `sig: ed25519:...`, and printed `signed with the p key`.

Not run, never faked: hypothesis item (5), the real dry run against
`local-town`. There is no second box or clone of it on this host -- `local-town`
appears only as an unrelated `provider` value in `.agi/config.json`. It stays
for the round that has the clone.

## Boundary (what this does NOT prove)

The record kind and the plan are proved on the built bytes. The parent claim's
items (1)-(4) are NOT: no carryover commit, no ref push, no mail_poll receive
hook, no fork transcript copy, no seated line. Steps 2/3/5 are printed plans,
not executed behaviour. `--mode fork` accepts `--session-id` but nothing copies
a transcript yet; `migrations.md`'s `migrate_fork_below` cell does not exist yet.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This round forks the parent hypothesis into a buildable first slice. Rationale: the record kind is the one artifact every later slice (carryover commit, ref push, mail_poll receive, seated line) must agree on, so it ships first with its parser and signature. The git steps are deliberately absent -- a kid may not run the landing git, and the target acts on its own tick. production_lines=212 is over the 120 ceiling but under 2x; the module is the irreducible record/formatter/verifier, and no line is a stub that pretends to be behaviour.
<!-- THOUGHT:END -->

## Agent Notes
SM.123 source-side slice built: migrate_channel.py = the ONE signed cross-box migrate record kind (format/parse/verify against send._canonical_msg), plus rotate.py migrate with the six-step plan by alias, same-box and unknown-mode refusals by name, --dry-run touching nothing and --apply writing ONE signed record under <comms>/migrate/. 8 new tests + 356 existing rotate/send tests pass. Carryover commit, ref push, mail_poll receive, fork transcript copy and the seated line are named plan steps, not built; the real local-town dry run (item 5) is NOT RUN (no second box/clone on this host), never faked.

PARENT REVIEW (a00-2a62c783, iter 151): accepted as the narrowed claim it states (record kind + plan/refusals; verdict left inconclusive_lean_proved:60). Parent probe, recorded here because it does not ride: cmd_migrate (rotate.py:20447-20520) prints "card: refuse a stale where-it-stops slot by name (rotate own gate)" as step 1 but NEVER calls _locate_where_it_stops or any card gate -- not on --dry-run, not on the write path. So hypothesis conjunct 1 card clause (refuses a stale where-it-stops slot by name, exactly like rotate) is NOT met by these bytes; the step is a printed plan line, nothing more. The kid never claimed otherwise (its title says commit/push/receive named not built), so this is a named hypothesis gap, not a demotion.
