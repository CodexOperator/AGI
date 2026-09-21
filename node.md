---
id: experiment:a00-470c9871-3d57d3
mint_id: 4c5393f0f37443e89a2e2248e04192c0
type: experiment
parents:
  - hypothesis:l4-the-predecessor-answers-the-ack-and-rotate-out-is-one-signed-call
next_edges: []
confidence: 0.7
edited_by: a00-a316ccc9
evidence_runs:
  - experiment:a00-470c9871-3d57d3
loop: hypothesis:l4-the-predecessor-answers-the-ack-and-rotate-out-is-one-signed-call@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 223e8852db06cd88
season: 2
title: "rotate-self --stops: built the one-call rotate-out (stops write, one pathspec commit, push, rotation line)"
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-470c9871-3d57d3

## Experiment

BUILT the goal:g15.25 line (3) rotate-out half in extensions/agi/bin/rotate.py
(the claim is behaviour to build, not a hypothesis to measure). The rotate-out
is now ONE call when `--stops` is given.

What landed:
- **argparse** (rotate-self): `--stops '<text>'`, `--stops-file F` (mutually
  the same source; `--stops -` reads stdin). `--ask-diff` became `nargs='?'`,
  `const=True` — bare `--ask-diff` still hands `True` (byte-compatible with
  the existing ack leg), and `--ask-diff '<gap>'` ALSO writes
  `diff requested: <gap>` into the stops section.
- **`_write_stops_section(card_path, seat, text, diff_gap)`** — writes the
  where-it-stops slot on the seat's OWN card (`_own_card_path`), REUSING the
  driven-writer machinery `_locate_where_it_stops` / `_split_card_sections` /
  `_render_card`. When absent it CREATES `### 🔴 Where it stops` at the card's
  end; when present it REPLACES only that subheader + block up to the next
  heading, carrying everything else verbatim (a `###`-inside-a-`##` rewrite no
  longer wipes the section above it). Ambiguous slot -> refuse, never guess.
- **`_commit_stops_row(root, seat, card, msg)`** — the ONE rotate-out commit:
  card blob + the seat's OWN seats.md row (`_seats_ownrow_content`) into a
  throwaway index seeded from HEAD, commiting NOTHING else. NEVER `git add -A`
  (mirrors `_commit_spawn_row`).
- **`_stops_push(root)`** — pushes the branch; a refused push returns a NAMING
  block -> cmd exits 3, nothing rotated. Never a force-push.
- **cmd_rotate_self pre-spawn region** (between the registry gate and the
  key gate, per FILE SCOPE): when `--stops` is given, write the section, commit
  card + own row, push, print the rotation line — the out-count is ONE call.
  `--dry-run` prints the stops write + the commit message + BOTH push lines and
  touches nothing. Empty stops text refuses (exit 2). Without `--stops` the
  flow is byte-identical to today.
- **captive-4 carve-out** (`_prepare_checks`): the seat-row path (posts.md/
  seats.md) is now excluded from the "last WORK commit" measurement, mirroring
  the card exclusion — otherwise the stops commit (which may touch the seat
  row) would re-age the card and self-block the flow it exists to satisfy.

## Evidence

Tests (extensions/agi/tests/test_rotate.py, test_rotate_prepare.py):
- `test_stops_block_refuses_empty` — `--stops '  '` -> exit 2, empty refused.
- `test_write_stops_section_created_and_replaced` — slot CREATED at card end
  when absent; REPLACED (up to next heading) when present; `diff requested:
  <gap>` rides both; surrounding section carried verbatim.
- `test_commit_stops_row_commits_card_and_own_row_nothing_else` — the rotate-out
  commit stages card + the seat's OWN seats row only; a FOREIGN seats row edit
  and a stray untracked file never ride it (no `-A`).
- `test_rotate_self_stops_one_call_writes_card_commits_rotates` — on a real
  git-backed fixture with an upstreamed seat branch and a fake tmux: ONE
  `rotate-self --stops 'fix the merge on seat-3'` returns rc 0; the card carries
  `### 🔴 Where it stops` + the text; `git log -1 --name-only` on the seat branch
  = card only (nothing outside card+seats); the committed card contains the
  text; the rotation line prints.

Suite run (files changed/covering):
```
python3 -m pytest test_rotate.py test_rotate_prepare.py \
  test_rotate_handoff_driven.py test_rotate_handover.py \
  test_bin_help_smoke.py -q   -> 330 passed, 3 skipped
python3 -m pytest test_sensei_rotate_out_audit.py \
  test_rotate_handoff_driven.py test_rotate_tail.py -q -> 59 passed
```
The no-flag path is byte-identical: all pre-existing rotate/prepare/handoff/
handover/help tests still pass (the only edit to pre-existing behaviour is the
captive-4 seat-row exclusion, whose own test was updated to assert it).

## Agent Notes

Verdict: inconclusive_lean_proved:70. The core falsifier (one call rotates,
card gets the stops text, commit scoped to card+seats, rotation line printed,
push-refusal blocks) is proven on a fixture with a real git repo. Not every
sub-claim is individually proven here: the KEYED-seat signing of the rotate-out
commit, the exact live second push line (captive-3 merge push before spawn),
and the belt-and-suspenders own-seats-row commit on a genuinely-dirty seat row
at rotate-out. push_further: prove the signed-keyed-commit sub-claim on the keyed
fake seat and the dry-run "second push line" wording against the live merge path.

## Agent Notes
Built rotate-self --stops: one-call rotate-out (card stops write + one pathspec commit card+own seats row + push + rotation line); dry-run prints stops write/commit/both-push-lines, push-refusal blocks exit 3, empty stops refused; captive-4 excludes the seat-row path so the stops commit doesn't self-block. 330+59 suite tests pass.

Parent review SL7.12: accepted inconclusive_lean_proved:70. The one-call rotate-out (--stops write, one pathspec commit of card plus own seats row, push, rotation line) is built and the core falsifier is proven by test_rotate_self_stops_one_call_writes_card_commits_rotates. Parent measured one sub-claim as a real gap rather than merely unproven: the live flow ran ONE push while dry-run printed push line 2, so the captive-3 merge commit sat unpushed at spawn. That gap is closed by the later experiment:a00-c9e0b67f-bcfbf5, which now cites this node as evidence.
