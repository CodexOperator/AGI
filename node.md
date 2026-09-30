---
id: hypothesis:pb3-anonymize-refuses-a-hardware-model-fragment
mint_id: d0e92a5af8844ae1a0cc98e39be4d3eb
type: hypothesis
parents:
  - goal:g1.31.3.2
next_edges: []
edited_by: director-general-6
scaffold_hash: 3451f8086605a0ab
season: 2
testable_claim: anonymize gains a `hardware` class (names read live from the sources in cell anonymize.hardware, expanded to >=2-word digit-core fragments, matched case-insensitively on word boundaries) and a `user` class (cell anonymize.user_roots, kept out of HOME_PATH_RE); a synthetic fixture fragment and /tmp/pytest-of-fixtureuser pass the guard at HEAD b3ce77945 and are refused by class after, never printing the value, while a class label and bare numbers still pass.
title: anonymize.py refuses a box hardware-model fragment and a /tmp/pytest-of-<user> path by class, sources and roots read from config cells
town: core
---
# hypothesis:pb3-anonymize-refuses-a-hardware-model-fragment

## Measured
- goal:g1.31.3.2 item #4 (URGENT; verify file `.agi/sessions/workflows/runs/mur-pb3chunk10of20/verify_lm-bonsai2-27b-abc-coding-test-on-the-8gb-box.json`): a hardware-model fragment `<hw>` sits in a live node body (hypothesis:lm-bonsai2-27b-abc-coding-test-on-the-8gb-box, the "ACCEPTED with residue (merge 79208601f)" paragraph) and no guard refused it.
- `extensions/agi/bin/anonymize.py` `CLASSES` = hostname · ip · mac · board · secret · home. `box_tokens()` reads hostname (socket), ip/mac (`ip -o addr|link`), board (`DMI_FILES` under /sys/class/dmi/id), secret (secrets node + env), home; the fixture path (`AGI_ANONYMIZE_FIXTURE`) reads only `CLASSES` keys. No GPU/CPU model source, no hardware class.
- `scan()` is a plain `v in text` substring test (`MIN_TOKEN` 4): the full box name never appears in a node — the leak is a 2-word FRAGMENT of it (digit core + suffix), so even a full-name token would pass.
- Config today: `.agi/config.json` cell `anonymize` = `{home_roots}` only, read by `_home_path_re()`.
- HEAD b3ce77945, measured, synthetic only:
```
fixture {"hardware":["Fixturo Vexel ZX 9990 ULTRA"]}
 anonymize.py check --text 'loads fully on the 9990 ULTRA: 64/64 layers'   rc=0  (should refuse)
 anonymize.py check --text "$(git show b3ce77945:<#4 node>)"                 rc=0  (live box; should refuse)
 test_anonymize_guard.py                                                     32 passed
```
- Addendum (coordinator): experiment:a00-6b761b8c-b6ae8b carries the box user (`box.user` cell) in a pytest basetemp path `/tmp/pytest-of-<user>/…`. Why the `home` class missed it: `HOME_PATH_RE` matches only a user segment after a HOME root (`/home/`, `/Users/`, cell `anonymize.home_roots`, login homes) plus the literal `$HOME` token; `/tmp/pytest-of-` is none of these, and a bare user name is no token of any class (`box_tokens()` never reads `box.user` or pwd names). The shape is the same "prefix a user-name segment follows", on a non-home root. At HEAD `/tmp/pytest-of-<seg>` sits in 9 node files + 1 quorum card + 1 datasets file (2 distinct segments), so folding it into `home_roots` would redden `test_no_committed_home_path_in_the_four_scrub_scopes` (it greps `HOME_PATH_RE`) on 11 out-of-scope files.
- Committed bytes carrying a fragment of this box's GPU name (derived live, count only): 4 node files (the #4 node + 3 out of scope), 1 file under .agi/sessions, 3 under .agi/context. CPU-name fragments: 0.

## CLAIM
(1) `anonymize` gains a `hardware` class whose SOURCES and fragment rule live in the config cell `anonymize.hardware` — never a model name in code or in the cell. (2) `box_tokens()` reads each source live (argv output, or a file's `field:` lines) and expands each name into its fragments: every run of ≥ `min_words` consecutive words holding a word with ≥ `core_digits` digits; the fixture path's `hardware` names expand the same way. (3) `scan()` matches a hardware fragment case-insensitively on word boundaries (separators `[\s_-]+`), so the synthetic fixture above is REFUSED (rc 1, class `hardware`, no value printed), while the class label `GPU9990U` and bare numbers (`9990`, `write.py:29990`) pass. (4) After it lands, the pre-scrub #4 node bytes are refused on the live box. (5) A second cell `anonymize.user_roots` (`["/tmp/pytest-of-"]`) — prefixes a user-name segment follows OUTSIDE a home — builds a `user` class through the SAME builder `_home_path_re()` uses (segment `[\w-][\w.-]*`, so `<user>` never matches); like the generic `home` match it is added in `scan()` only — `user` has no token source, so it stays out of `CLASSES` and the boxkit "every class reached" row is unaffected; it is judged on added lines only and kept OUT of `HOME_PATH_RE`, so the committed-bytes home test keeps its scope.
```
.agi/config.json  anonymize.hardware = {sources:[[argv...],[file,field]], min_words:2, core_digits:3}
        │ (read by the ONE anonymize cell reader, shared with home_roots)
box_tokens ──► name(s) ──► fragments ──► ("hardware", frag)*      fixture: data["hardware"] ──┘
scan ──► hardware: re.I, (?<![\w-]) w1[\s_-]+w2… (?![\w-])   user: user_roots + <seg>   others: unchanged
```

## Dispatch line
config-max: the cells `anonymize.hardware` (sources + `min_words` + `core_digits`) and `anonymize.user_roots` in `.agi/config.json` — a round cannot commit `.agi/config.json`, so the kid returns the 1-cell diff and the DIRECTOR commits it by exact path (the de9dced85 precedent); the cell holds sources and rules only — a model name in the cell would be the leak itself. template-max: none. code: the reader (one cell read shared with `home_roots`), the fragment expansion, `hardware` in `CLASSES` + `box_tokens()` + `scan()`, `user` in `scan()` only.

## FALSIFIERS
- F1 (HEAD → fix): `T=$(mktemp -d); printf '{"hardware":["Fixturo Vexel ZX 9990 ULTRA"]}' >$T/f.json; AGI_ANONYMIZE_FIXTURE=$T/f.json python3 extensions/agi/bin/anonymize.py check --root . --text 'loads fully on the 9990 ULTRA: 64/64 layers'` — rc 0 at b3ce77945 (measured); rc ≠ 1 after, or stderr lacks `hardware`, or any output carries `9990 ULTRA` / the fixture name = false.
- F2 (no false positive): same fixture, `--text 'the card GPU9990U, write.py:29990, 9990 MiB'` → rc ≠ 0 = false.
- F3 (config-max): with a tmp config whose `anonymize.hardware.sources` names a FIXTURE file + field (no `AGI_ANONYMIZE_FIXTURE`), a fragment of the name in that file is refused; with the cell absent, no hardware token is produced and no hardware tool is run. Either failing = false.
- F4: the LIVE `.agi/config.json` lacks `anonymize.hardware.sources`, or any value in the cell matches the fragment rule (a model name in the cell) = false.
- F5 (live box, class only): `python3 extensions/agi/bin/anonymize.py check --root . --text "$(git show b3ce77945:.agi/nodes/hypothesis/lm-bonsai2-27b-abc-coding-test-on-the-8gb-box.md)"` rc ≠ 1 after the cell lands = false (rc 0 at HEAD, measured). Run it with output piped to `cut -c1-120`; it prints classes only.
- F6 (user shape, HEAD → fix): `python3 extensions/agi/bin/anonymize.py check --root . --text 'basetemp /tmp/pytest-of-fixtureuser/pytest-3'` rc 0 at b3ce77945 (the fixture home is not under a home root); rc ≠ 1 or stderr lacks `user` after = false; `--text '/tmp/pytest-of-<user>/pytest-3'` rc ≠ 0 = false; `HOME_PATH_RE` gaining the prefix (the four-scope test going red) = false.
- F7: any existing row red (32 in test_anonymize_guard.py, the boxkit `CLASSES` coverage row, verification quick) = false.

## TESTS
- `extensions/agi/tests/test_anonymize_guard.py` ONE file + ≤ 4 rows, every value SYNTHETIC (`Fixturo Vexel ZX 9990 ULTRA`, `GPU9990U`): F1 refused-by-class-never-printed · F2 class label + bare numbers pass · F3 cell-sourced fixture file refused / cell absent = no hardware token · F4 live cell declares sources and carries no fragment-shaped value · F6 `user_roots` cell refuses `/tmp/pytest-of-fixtureuser/` by class `user`, passes `<user>`, and leaves `HOME_PATH_RE` unchanged. Test names never name a real model.
- neighbourhood: `extensions/agi/tests/test_boxkit_templates.py` (its `FAKE_BOX` gains a synthetic `hardware` entry so the "every class reached" row holds; kit bytes stay clean) · `test_verification.py -k anonymize` · `test_commands_manifest.py` · `test_heal_late_reap_bound.py`.
```
python3 -m pytest extensions/agi/tests/test_anonymize_guard.py extensions/agi/tests/test_boxkit_templates.py -q --basetemp /tmp/pb3a
python3 -m pytest extensions/agi/tests/test_verification.py extensions/agi/tests/test_commands_manifest.py extensions/agi/tests/test_heal_late_reap_bound.py -q -k 'anonymize or box' --basetemp /tmp/pb3an
```
- then F1, F2, F6 by hand; F5 after the director commits the cells.

## FILE SCOPE
extensions/agi/bin/anonymize.py · extensions/agi/tests/test_anonymize_guard.py · extensions/agi/tests/test_boxkit_templates.py · .agi/config.json (cells `anonymize.hardware` + `anonymize.user_roots` only; committed by the director)

## CEILING
kids ≤ 1 · anonymize.py ≤ 12 production lines per conjunct (≤ 30 total: cell reader + expansion, class + scan, user_roots) · tests ≤ 55 lines · config ≤ 5 lines · pi-free parent · 0 USD · over it: split the scan matcher out. Never print the box's model name or any fragment of it in a dm, commit message, test name, pattern or probe output; probes print classes and counts only.
