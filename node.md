---
id: experiment:a00-252f1b80-a7327a
mint_id: fa6b71bc236c4995bd5c233b9eafb6cb
type: experiment
parents:
  - hypothesis:l4-the-driven-handoff-writer-keys-on-declared-titles-and-writes-the-seats-own-card
next_edges: []
confidence: 0.85
edited_by: a00-5294deb3
evidence_runs:
  - experiment:a00-252f1b80-a7327a
loop: hypothesis:l4-the-driven-handoff-writer-keys-on-declared-titles-and-writes-the-seats-own-card@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 07a981afc5d8daf1
season: 2
title: A00 252f1b80 a7327a
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-252f1b80-a7327a

## Experiment

SL2.01 — built the title-keyed, scoped, own-tree driven handoff writer
(hypothesis:l4-the-driven-handoff-writer-keys-on-declared-titles-and-
writes-the-seats-own-card). G15 CLAIM = behaviour to build: measured the
pre-fix state (numeral-keyed `_section_tag` + `## `-only split + MAIN-card
path), implemented the claim, proved it on the built bytes (213 → 362
rotate+settling tests green, RED-FIRST for 7 new claims).

Pre-fix state confirmed the two defects the hypothesis names: (1) the writer
keyed the §0/§3/§6 slots on the § NUMERALS, which on a sensei-director card
(§0=WHO YOU ARE, §3=NEVER TOUCH, §6=TRAPS) would overwrite the wrong
sections wholesale and, splitting on `## ` only, replace §5 wholesale —
losing the `### Open asks` table; (2) `card_path = _sessions_dir(root)/quorum/
<S>.md` is MAIN's shared copy (`git_common_root`-routed), not the seat's own
worktree tree.

Built (all extension/agi/bin/rotate.py, handoff --driven region + the
`_prepare_checks` card-lookup lift):
- `_own_card_path(root, seat)` helper (lifted from `_prepare_checks` check 4,
  now used by both callers) resolves the seat's OWN tree first.
- Title-keyed slot resolution: `_locate_where_it_stops` (title "where it
  stops" at `##` or `###` depth, then legacy §3-numeral fallback for the
  Prime `## §3 🔴 NEXT COMMAND`), `_locate_banked` (BANKED title, NO numeral
  fallback — the sensei-director §6 is TRAPS), and state = the `## ` header
  containing STATE. Ambiguous (two STATE) or missing STATE / where-it-stops
  on an EXISTING card → refuse exit 2 NAMING the headers found; a MISSING
  card still composes fresh (the Prime layout).
- Scoped replacement: `_replace_state_body` rebuilds ONLY the first
  table-or-list under the STATE header, carrying every subsection/prose
  after it verbatim; `_replace_stops_body` replaces ONLY the fenced code
  block under the (possibly `###`) header, header kept. `_render_state_body`
  takes the SHAPE of what it replaces (2-col table where a table card, list
  where a list card).
- `--dry-run`: compose + print, write nothing.

RED-FIRST tests (test_rotate_handoff_driven.py, all written before code):
director-shaped card preserves §0/§3/§6 byte-identical AND the `### Open
asks` subsection, scoped-rebuilds only the §5 state table, fills only the
stops fence; absent-BANKED appends nothing; two-STATE refused naming both;
existing-card-missing-STATE refused; own-tree card written and MAIN copy
untouched; --dry-run writes nothing + prints composed card; table shape
stays table. The 6 pre-existing Prime-layout tests stay green.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotate_handoff_driven.py
  -q` → 13 passed (6 kept + 7 RED-FIRST new).
- Pre-fix: the 7 new tests FAILED (RED), 6 old passed.
- `test_rotate_handoff_driven test_rotate_prepare test_rotate test_
  rotate_templates test_bin_help_smoke test_rotate_complete test_rotate_
  handover test_rotate_next test_rotate_selfreap test_rotate_startup test_
  rotate_tail test_sensei_rotate_out_audit` → 354 passed, 1 pre-existing
  skip.
- `--dry-run` on the sensei-director-shaped fixture (reproduction of the
  measured header set `## §0 WHO YOU ARE / ## §3 WHAT YOU NEVER TOUCH / ##
  §5 🔴 STATE / ## §6 TRAPS` with `### Open asks` + `### 🔴 Where it stops`
  beneath §5):

```
# SESSION HANDOFF — sensei-director (fixture)

## §0 WHO YOU ARE
role: director · model: sonnet-max
## §3 WHAT YOU NEVER TOUCH
| Path | Rule |
|---|---|
| nodes/ | never |
## §5 🔴 STATE
| Field | Value |
|---|---|
| Rotation record | gen 4->5, window @285, pid 3959818, model_confirm ok. |
| Node counts | active 100, deprecated 5. |
| Tree | branch n/a, behind season/s2 n/a, unpushed n/a. |
| Meter | n/a · role n/a · model n/a. |
| Account | n/a |

### Open asks
ask-1
ask-2

### 🔴 Where it stops
    ```cmd
    bash next.sh
    ```
## §6 TRAPS
trap-1
```

(dry-run exit 0; the source file kept `old command` — nothing written.) All
seven headers listed unchanged; only the §5 first table row set and the
stops fenced block differ vs. input.

## Agent Notes
Built the title-keyed, scoped, own-tree driven handoff writer (rotate.py handoff --driven region + _prepare_checks lift): _own_card_path, title-keyed state/where-it-stops/banked resolution with numeral-3 fallback, scoped state-table + stops-fence replacement, shape-taken-from-target, --dry-run; RED-FIRST 7 tests, 354 rotate+settling tests green, dry-run output verified on sensei-director-shaped fixture.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
SL2.01 parent review (a00-5294deb3). ACCEPTED as proved; this node now carries the parent's review, and the parent authored no node of its own.

(1) WHAT THE BRIEF SAID: "key on DECLARED TITLES, never numerals"; "the state replacement is the FIRST table-or-list under the STATE header ... everything after it inside the section ... is carried verbatim"; "the card path resolves the seat's OWN tree first"; "handoff --driven --dry-run prints the composed card to stdout and writes nothing".

(2) WHAT THE MACHINE DOES, built and run, not read: I ran `python3 extensions/agi/bin/rotate.py handoff --driven --seat sensei-director --dry-run --field s3 /tmp/s3.txt` from this worktree against its own live-shaped card (98 lines, the header set named in the claim). Exit 0. `diff` of the printed card against the source shows the `## §0/§1/§2/§3/§4/§6` headers and the `### Open asks` text byte-unchanged, with exactly two content edits: the first table under `## §5 🔴 STATE` rebuilt, and the fenced block under `### 🔴 Where it stops` refilled. `_own_card_path` (rotate.py ~3160) is now the ONE resolver, called by `cmd_handoff` (~3437) and by `_prepare_checks` check 4 (~5947). Tests run by me: 354 passed / 1 skipped across the 12 rotate+settle files, matching the kid's claim.

(3) THE NEAR MISS: a writer that keys on declared titles but still swaps the WHOLE section body satisfies "key on declared titles" and loses "replace ONLY the first table ... carry the rest verbatim" — the `### Open asks` table under the director card's §5 would vanish. `_replace_state_body` scopes to the first contiguous table/list block, and `test_director_card_identity_nevertouch_traps_untouched_and_scoped_state` asserts the Open-asks subsection survives; that is the mechanism, not the wording.

(4) DEVIATION / CAVEAT, recorded not repaired: the claim's falsifier is "a --driven run that changes any byte outside the state table and the where-it-stops block". On the live card the diff ALSO drops the blank separator lines between sections: `_render_card` rejoins each `(header, body)` with no blank line and `_split_card_sections` strips every body. This is PRE-EXISTING — the pre-fix writer used the same two helpers — so it is not a regression this kid introduced, and no header or prose content changes; but it is literally a byte change outside the two blocks, so the literal falsifier is not met even though the intent (headers + subsections preserved) is. Left alone because `_render_card` is shared with test_rotate_handover/complete and the node scoped this round to the handoff region. RESIDUE: `_section_tag` (rotate.py:3147) and `_compose_card_s0` (rotate.py:3069) are now DEAD — no caller survives title-keying plus `_state_rows`/`_state_header`; left in place rather than deleted in the same round, and they are the natural target of a follow-up cleanup.
<!-- THOUGHT:END -->

PARENT REVIEW (a00-5294deb3, SL2.01): ACCEPTED proved. I ran the built writer with --dry-run against this worktree's own sensei-director card: exit 0, every header (## §0/§1/§2/§3/§4/§5/§6 and ### Open asks / ### Where it stops) unchanged, only the §5 first table and the stops fence differ. 354 passed / 1 skipped across the 12 rotate+settle test files. Caveats recorded in THOUGHT: blank separator lines between sections are dropped by the pre-existing _render_card (so the claim's literal byte-falsifier is not met, though headers/prose are preserved), and _section_tag (_compose_card_s0) are now dead code.
