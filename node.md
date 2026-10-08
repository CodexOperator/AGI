---
id: hypothesis:pb3-anonymize-email-class-and-forward-scrub
mint_id: d6a06521e5ee4e48af1faf6a99451cdf
type: hypothesis
parents:
  - goal:g1.31.5.1.2
next_edges: []
edited_by: director-general-6
scaffold_hash: cc9e65f07e1ccfe8
season: 2
testable_claim: scan() refuses any email address not fully matched by a regex in the config cell anonymize.email_allow, by class `email` and never printing the value (synthetic fixtures assembled at run time); the 4 named experiment nodes are scrubbed forward through write.py `sub!` (<email>, <user>@<host>) with no history rewrite; SCRUB_SCOPES gains skills and the 4 home-path lines in skills/agi/SKILL.md + QUICKSTART.md become <home>/, so committed bytes carry 0 non-allowed addresses and 0 home paths across .agi/nodes, skills and QUICKSTART.md.
title: anonymize.py refuses an email address by class (allow list in cell anonymize.email_allow); 4 experiment nodes scrubbed forward; skills/ joins the scope
town: core
---
# hypothesis:pb3-anonymize-email-class-and-forward-scrub

## Measured
- goal:g1.31.5.1.2 (PASS B3 missed rows n112 red + n88 residue; verify files `.agi/sessions/workflows/runs/mur-pb3chunk7of20/verify_a-second-director-ran-this-graph-uninvited.json`, `.../mur-pb3chunk3of20/verify_engine-delta-6.json`). HEAD 0de3a32a0, counts only, no address printed.
- `extensions/agi/bin/anonymize.py`: `CLASSES` = hostname · ip · mac · board · secret · home. `scan()` = token substring test + ONE generic class (`HOME_PATH_RE`, no token source). No email class: `check --text '<synthetic address>'` rc 0.
- 4 tracked experiment nodes carry an owner address: `a00-75e7c869-24b9f0` (2 hits) · `a01-4a4d8f92-b02a7a` (2 owner hits + 2 user-at-host tokens) · `a01-9bc63860-d97453` (2) · `a00-9f8f7f3e-99d092` (1) = 7 owner hits (1 distinct address) + 2 user-at-host. Files with any email-shaped string tracked in the repo: 62; under `.agi/nodes` + `skills` + `QUICKSTART.md`, after dropping the allowed shapes (`example.com/org/net/invalid` · `email.com` · `@openssh.com` key types · `user@<uid>.service` · `UID.service`), the residue is exactly the 7 owner hits, the 2 user-at-host hits (same 4 files) and 2 `github.com` hits (a `git@` remote in prose, allow by shape).
- `test_anonymize_guard.py` `SCRUB_SCOPES` = rotations · quorum · datasets · `.agi/nodes`; `git grep -P HOME_PATH_RE` finds 4 lines in 2 files outside it: `skills/agi/SKILL.md` (3) + `QUICKSTART.md` (1). `skills/agi-stream/SKILL.md` (the file the n88 row cites) is clean at HEAD; the class of leak remains.
- `write.py`: `sub! <old> => <new>` = every occurrence, count printed; `sub` = one literal occurrence. The `<old>` IS the address, so the operator's shell must build it, never a file or a note.
- The pre-commit hook of a `--branch` kid refuses another author's node (`cli._round_scope_ok`), so a kid cannot commit the 4 scrubs; the round's parent/director does, through write.py (which commits by itself), exactly like `.agi/config.json`.

## CLAIM
(1) `anonymize` refuses an email address by the generic class `email` inside `scan()` (no token source, so it stays out of `CLASSES`; the boxkit "every class reached" row is untouched), judged on added lines only, printing the class and never the value. An address passes iff it full-matches a regex of the config cell `anonymize.email_allow` (list of regexes, each matched against the WHOLE address): the cell carries the reserved example domains, `@openssh.com` key-type names, `user@<uid>.service` units and the the `git` user at github.com remote; the code carries NO domain and no default allow, so a graph without the cell refuses every address.
(2) The 4 named experiment nodes are scrubbed FORWARD, through write.py only: `sub!` per file, the owner address replaced by `<email>` and the 2 user-at-host tokens by `<user>@<host>`; each version's THOUGHT records the scrub. No history rewrite (owner's call, banked: CLAUDE.md "Delegated authority" 6).
(3) `SCRUB_SCOPES` gains `skills`; the 4 home-path lines in `skills/agi/SKILL.md` + `QUICKSTART.md` become `<home>/` (`QUICKSTART.md` is one file, checked by its own pathspec row), so `HOME_PATH_RE` and the email class both have 0 non-allowed hits over `.agi/nodes` + `skills` + `QUICKSTART.md` at the round's tip.
```
.agi/config.json  anonymize.email_allow = [re, re, ...]   (director commits; same cell reader as home_roots / hardware)
scan(text, tokens, root=None) ──► + _email_hits(text, root) ──► "email" in hits ──► REFUSED: ... email ...   (value never printed)
   EMAIL_RE.finditer(text) ─ m.group(0) ─ any(re.fullmatch(a, m) for a in allow) ? pass : hit
test rows (SYNTHETIC, assembled at run time)          write.py <4 nodes> 'sub! <addr> => <email>' | mask
```

## Dispatch line
config-max: the allowed non-personal shapes move to the cell `anonymize.email_allow` in `.agi/config.json`; a round cannot commit `.agi/config.json`, so the kid returns the 1-cell diff and the DIRECTOR commits it by exact path BEFORE the code lands (else the live hook refuses example.com in any engine edit). template-max: none. code: `EMAIL_RE` + `_email_hits(text, root)` + one line in `scan()` + `root` threaded from `cmd_check`; SEQUENCING (director): cut this round from the loop tip of hypothesis:pb3-anonymize-refuses-a-hardware-model-fragment (goal:g1.31.3.2, live round DG6.04) once it merges; that round adds `hardware` + `user` to the same `anonymize.py`, the same test file and the same `anonymize` cell. This round touches DIFFERENT functions (a new `_email_hits`, one `scan()` line, `cmd_check`'s scan call), adds its OWN cell key beside theirs, and REUSES their one cell reader (find it by name at that tip; never a third reader). If it has not merged, hold, do not fork the reader.

## FALSIFIERS
- F1 (HEAD -> fix; rc 0 at HEAD, measured): `python3 extensions/agi/bin/anonymize.py check --root . --text "reach fixture.person$(printf '\x40')fixture-corp.test"`; rc != 1, or stderr lacks `email`, or any output carries the local part / domain = false. (The leaf's own falsifier uses `example.invalid`; the cell allows it because 4 tracked lines already use it, so the leaf permits the swap.)
- F2 (allowed shapes pass): the same call for a synthetic `<name>@openssh.com`, a `user@<uid>.service` unit, a synthetic `<name>` at `example.com` and at `example.invalid` (each assembled with `printf '\x40'`) rc != 0 = false.
- F3 (config-max): with a tmp config whose `anonymize.email_allow` is `[]` or absent, the `openssh.com` shape IS refused; with the cell naming it, it passes. The regex list is read from the cell, never from a code constant. A domain literal in anonymize.py's code (`git grep -nE 'example|openssh' extensions/agi/bin/anonymize.py` returns a hit outside a comment) = false.
- F4 (forward scrub): `git grep -qE '<EMAIL_RE>' -- <the 4 nodes>` finds a hit at the tip = false; a `<email>` count per file differs from that file's HEAD hit count (2 · 2 · 2 · 1 owner hits) = false; `git log --format=%H -- <a node>` shows a rewritten (not appended) history, or `git filter-*`/force-push ran = false.
- F5 (mask): the round's log, dm, commit message or THOUGHT carries an address, a user or a host string = false (`git grep -cE '<EMAIL_RE>'` on the round's diff prints only counts).
- F6 (scope): `python3 - <<< "import sys,subprocess; sys.path.insert(0,'extensions/agi/bin'); import anonymize as a; sys.exit(int(subprocess.run(['git','grep','-qP',a.HOME_PATH_RE.pattern,'--','skills','QUICKSTART.md']).returncode==0))"` rc 1 = false; `SCRUB_SCOPES` lacks `skills` = false.
- F7: any existing row red (`test_anonymize_guard.py`, the boxkit `CLASSES` coverage row, `test_verification.py -k anonymize`) = false; the hardware round's rows red after the rebase onto its tip = false.

## TESTS
- `extensions/agi/tests/test_anonymize_guard.py` ONE file, <= 4 rows, every string SYNTHETIC and assembled at run time (`"fixture.person" + "@" + "fixture-corp.test"`; a test file holding an address literal would be refused by the very hook it tests): (a) a synthetic address refused by class `email`, stderr never carries it (capsys) · (b) allowed shapes pass under a tmp cell, refused under an empty cell (config-max) · (c) a diff whose ONLY email is on a removed line passes (added-lines rule) · (d) `test_no_committed_email_or_home_path_in_the_scrub_scopes`: reuses `SCRUB_SCOPES` (+ `skills`) and `QUICKSTART.md`, counts non-allowed EMAIL_RE matches and HOME_PATH_RE files over COMMITTED bytes (`git grep -o`, counts only) == 0; the existing four-scope row's `SCRUB_SCOPES` edit is the `skills` add. Test names never name an address, user or host.
- neighbourhood: `test_verification.py -k anonymize` · `test_boxkit_templates.py` (its `FAKE_BOX` must not gain an `email` entry: `email` is not in `CLASSES`) · the hardware round's rows.
```
python3 -m pytest extensions/agi/tests/test_anonymize_guard.py -q -k 'email or scrub_scopes or home' --basetemp /tmp/pb3e
python3 -m pytest extensions/agi/tests/test_verification.py extensions/agi/tests/test_boxkit_templates.py -q -k 'anonymize or box' --basetemp /tmp/pb3en
```
- then F1-F3 by hand; F4 after the scrub commits (write.py, director/parent seat, `--actor <post>`; the run's output piped to `| sed 's/.*/[masked]/'` or `>/dev/null`, the address held in a shell variable built by `grep -ohE "$R" <file> | sort -u` and never echoed). If write.py refuses a foreign experiment node for the actor, BANK it (card §6) with the refusal class; never hand-edit.

## FILE SCOPE
Kid (worktree): extensions/agi/bin/anonymize.py · extensions/agi/tests/test_anonymize_guard.py · skills/agi/SKILL.md · QUICKSTART.md
Director (exact paths, after merge): .agi/config.json (cell `anonymize.email_allow` ONLY) · .agi/nodes/experiment/a00-75e7c869-24b9f0.md · a01-4a4d8f92-b02a7a.md · a01-9bc63860-d97453.md · a00-9f8f7f3e-99d092.md (write.py `sub!` + `thought` only)

## CEILING
kids <= 1 (the scrub is a director write.py step, not a kid's) · anonymize.py <= 12 production lines per conjunct (email class + cell read via the shared reader <= 12) · tests <= 40 lines · skills/QUICKSTART edits = 4 lines · config <= 6 lines · pi-free parents · 0 USD · over it: split the committed-bytes row (d) out. Never print an address, user or host in a dm, commit message, test name, pattern or probe output; probes print classes and counts only.

## Agent Notes
DG6 06:1xZ: the forward node scrub is DONE by the director through write.py (4 experiment nodes, 9 hits -> <email>; commits 05ae9fa37 5585ea79f 6646cf424 e3ff2c6a5; tree-wide count of non-allowed email-shaped strings in tracked nodes, skills, QUICKSTART, CLAUDE.md = 0). The round keeps the anonymize.py email class + test + skills/ scrub scope, cut from the pb3-anonymize-refuses-a-hardware-model-fragment loop tip once that merges.
