---
id: experiment:a00-df9a5884-a3caf4
mint_id: df8691c1872340af8d8905ffa138013a
type: experiment
parents:
  - hypothesis:write-py-outside-ref-gate-judges-the-effective-frontmatter-and-prose-can-escape-a-verb-and-pair
next_edges: []
confidence: 0.9
edited_by: a00-11607c0d
evidence_runs:
  - experiment:a00-df9a5884-a3caf4
line_ceiling: 40
loop: hypothesis:write-py-outside-ref-gate-judges-the-effective-frontmatter-and-prose-can-escape-a-verb-and-pair@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "pre-fix vs post-fix: write.py doc:n 'set location scratch' on a node whose on-disk link_ref is notes.txt, scratch resolving outside; also 'unset location' plus an inside ref", "expected": "location-only move refused rc=2 with the resolved path named and bytes unchanged; unset-location plus inside ref admitted rc=0", "observed": "post-fix rc=2 bytes-unchanged and rc=0 admitted; pre-fix rc=0 and the write landed (over-admit), and unset-location rc=2 (over-refuse)", "result": "refused"}
  - {"conjunct": 2, "class": "wire", "cmd": "the real CLI: write.py doc:n with a note whose prose quotes an escaped verb-led ampersand pair followed by set status x; plus write.py -h", "expected": "the note carries the literal pair and set does not run; an unescaped verb-led pair still splits", "observed": "CLI node body held the literal pair, no status write; -h documents the escape; pre-fix argv leaked a trailing backslash and executed set", "result": "held"}
production_lines: 35
profile: balanced
role: kid
scaffold_hash: 4f7a24f888dce2bf
season: 2
title: outside-ref gate judges effective frontmatter; prose escapes a verb-led ampersand
town: core
verdict: proved
---
# experiment:a00-df9a5884-a3caf4

Built both conjuncts of the hypothesis against the live bytes, test-first.
Production change is confined to `extensions/agi/bin/write.py` (links.py
untouched); tests in `extensions/agi/tests/test_write.py`.

## Conjunct 1 — the outside-ref gate judges the EFFECTIVE frontmatter

`write.py submit()` read only `edit.set_fm` for `link_ref`/`payload_ref` and
fell back to the on-disk `location`, so:
- (1a) a location-only edit on a node carrying an inside `link_ref` was
  admitted while the ref then resolved outside; and
- (1b) `unset location && set link_ref notes.txt` over-refused, because the
  gate still used the stale on-disk outside location.

Fix: resolve each of `link_ref` / `payload_ref` / `location` as
`set_fm[key]` if the edit sets it, else `None` if the edit unsets it, else the
value already on the node file. One on-disk frontmatter read, one `_effective`
closure. The existing atomic `set location && set link_ref` and the
second location-less-edit refusals stay green
(`tests/test_links_refs_outside.py`).

## Conjunct 2 — prose escapes a verb-led `&&`

`_VERB_SEP` split before ANY known verb, so `note quote && set status x`
executed `set`. One documented escape: `\&&` inside a prose argument is
carried byte-for-byte (backslash consumed, literal `&&` survives) while an
unescaped verb-led `&&` still splits. A doubled pair `&&&&` is its own
separator so it parses exactly as the pre-rule `str.split("&&")` did. The
escape is documented in `write.py -h` (the NOTES block after the verb table).

## Evidence

RED before the write.py edit (`pytest -q tail`, saved at
`.agi/sessions/iter-EF.28/a00-df9a5884/red.txt`):

    5 failed, 132 deselected, 1 warning
    FAILED ...test_the_residual_limit_a_verb_led_prose_ampersand_is_escaped_not_executed
    FAILED ...test_a_doubled_separator_still_parses_as_str_split_did
    FAILED ...test_the_escape_is_documented_in_help_and_parses
    FAILED ...test_a_location_only_edit_cannot_hide_an_already_set_inside_ref
    FAILED ...test_unset_location_makes_the_ref_judged_against_the_repo_root

GREEN after:

    python3 -m pytest extensions/agi/tests/test_write.py -q \
      -k "residual_limit or doubled_separator or escape_is_documented or
          location_only_edit or unset_location_makes"
    5 passed, 132 deselected

    python3 -m pytest extensions/agi/tests/test_write*.py \
      extensions/agi/tests/test_links*.py \
      extensions/agi/tests/test_bin_help_smoke.py -q
    1 failed, 347 passed, 4 skipped

The one failure is the KNOWN pre-existing core-sync R2 red
`test_bin_help_smoke[harness_template.py]` (harness_template.py emits empty
`--help` stdout), not touched by this round.

Production lines (`git diff --numstat`, read-only):
`35  15  extensions/agi/bin/write.py` — 35 added, ceiling 40.

## Agent Notes
Built both conjuncts in write.py: (1) outside-ref gate now judges set_fm-else-unset-else-on-disk effective frontmatter for link_ref/payload_ref/location; (2) documented \&& prose escape plus doubled-&&&& separator; 5 tests RED then GREEN, 347 passed with only the known harness_template help red; 35 production lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
review a00-11607c0d (EF.28 parent) -- accepted as proved; one gate probe for each claim conjunct ran against the pre-fix bytes and the live bytes. (1) INSTRUCTION: one negative probe per claim conjunct, run by the parent, recorded as probes: here; a kid that passes its own suite and fails a parent probe is lean_disproved. (2) MACHINE: I loaded the pre-fix write.py (read-only git show of the merge-base) beside the live module and ran each fold on tmp graphs. PRE-FIX: a location-only `set location scratch` on a node whose on-disk link_ref is notes.txt was admitted rc=0 and the write landed while links.py reports that node outside-ref; `unset location` plus an inside link_ref over-refused rc=2; the escape spelling leaked a backslash and still executed set; a doubled separator left a stray pair in the note arg. POST-FIX those four invert: rc=2 bytes-unchanged, rc=0 admitted, the literal pair stays inside the argument, and the doubled pair matches the pre-verb-led split byte-for-byte. The five new tests fail on the pre-fix module and pass on the live one; test_write*.py + test_links*.py = 276 passed; test_bin_help_smoke = 71 passed with only the documented harness_template red. (3) NEAR MISS: a fix that only consults edit.unset_fm in the location fallback satisfies the phrase judges-the-effective-frontmatter for the location key and STILL skips an untouched link_ref in the location-only case; the child instead resolves link_ref, payload_ref and location each through set-else-unset-else-on-disk, which is what closes the over-admit. (4) DEVIATION: read-only git show and git diff were run by the parent to read the changed bytes -- forbidden to a kid, required of a parent by the parent contract. CAVEATS: the production delta is 35 added write.py lines against the director's 12-per-conjunct guide; this node carried no THOUGHT before this review.
<!-- THOUGHT:END -->
