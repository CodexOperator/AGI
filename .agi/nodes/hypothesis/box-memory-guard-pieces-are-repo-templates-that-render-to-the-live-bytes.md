---
id: hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes
mint_id: 8d3f4fbac3104be29da7e895a6c95a34
type: hypothesis
parents:
  - goal:g7.33.18.1
next_edges: []
edited_by: director-engine
scaffold_hash: d1bd18074c8a2550
season: 2
testable_claim: "every piece of goal:g7.33.18's table is a template + manifest entry under paths.boxkit.templates_dir that renders to the live local-town bytes, with no literal host/path and anonymize clean (assigned: director-engine)"
title: Box memory guard pieces are repo templates that render to the live bytes
town: core
---
# hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes

## Measured
- goal:g7.33.18 (TMM.265, OWNER 20:4xZ): the box-level memory-watch pieces live only on local-town, hand-installed; encryption-town must install the same stack sized to its RAM from ONE kit in the repo. The node's table lists every piece and its measured value on local-town (15932 MiB RAM, 4095 MiB swap).
- Config cells committed by the director at 3b42eb930: paths.boxkit.{templates_dir, install_root, sbin_dir, systemd_system_dir, systemd_conf_dir, user_systemd_dir, watchdog_conf}.

## CLAIM
Every piece in goal:g7.33.18's table (user@ / oomd / user.slice / user-UID.slice / system.slice drop-ins, agi.slice, agi-memguard.py + agi-memguard.service, the 10-agi-survival no-cascade drop-ins, watchdog.conf + sanctuary-health) is a template under paths.boxkit.templates_dir with manifest.json per the KIT CONTRACT; rendering each with local-town's measured values reproduces the live file byte-for-byte; no template carries a literal host, address, hardware name or path; anonymize check is clean.

## Dispatch line
config-max: every path is a paths.boxkit cell, every sized knob a values.boxkit cell (the director commits them) / template-max: the pieces themselves ARE templates / code: manifest.json + a tiny render helper (placeholder substitution, refuses an unfilled placeholder by name).

## FALSIFIERS
- a rendered template differs from the live file it was copied from (the test fixture holds the live bytes with host tokens already replaced);
- anonymize.py check flags a template;
- a template contains an unlisted placeholder, or a manifest placeholder the template never uses.

## TESTS
extensions/agi/tests/test_boxkit_templates.py: render every piece against a committed fixture of local-town's measured values and diff against a committed ANONYMIZED copy of the live bytes; manifest schema row; unfilled-placeholder refusal row. + test_anonymize*.py neighbourhood.

## FILE SCOPE
extensions/agi/boxkit/** (templates, manifest.json, render helper) · extensions/agi/tests/test_boxkit_templates.py · extensions/agi/tests/fixtures/boxkit/**. Never .agi/config.json.

## CEILING
<= 3 kids · <= 12 production lines per conjunct where code is new logic (template bytes do not count) · pi-free tier-0 · 0 USD.

## THE KIT CONTRACT (shared by g7.33.18.1/.2/.3 -- fixed by the director; a change is a [rule] line to the director, never a local edit)
- Templates live under the cell `paths.boxkit.templates_dir` (repo-relative), one file per live piece, `{{UPPER_SNAKE}}` placeholders for every SIZED value and every host-specific token.
- `<templates_dir>/manifest.json` = {"pieces": [{"name", "template" (relative to templates_dir), "dest_cell" (a key of paths.boxkit: sbin_dir | systemd_system_dir | systemd_conf_dir | user_systemd_dir | watchdog_conf), "dest_rel" (under that dir; "" when dest_cell names a file), "mode" (octal string), "sudo" (bool), "placeholders" [names], "reload" ("system" | "user" | "none")}]}.
- Every destination = install_root (cell paths.boxkit.install_root, "/" live, a tmp dir in every test) joined with the dest_cell value (`{home}` expanded) and dest_rel. NO literal path anywhere in code.
- SIZING (goal:g7.33.18): (g7.33.18 v2, 9b03554ac) user@ MemoryMax = MemTotal - held_outside_user - the box's MEASURED system reserve (an INPUT per box: local-town ~1.9 GiB, encryption-town 942 MiB -- never a fixed 2 GiB; the installer takes it as a flag/cell, the probe derives it from the installed MemoryMax) · MemoryHigh = 0.9 x MemoryMax · MemorySwapMax = 0.5 x swap · agi.slice MemoryHigh / MemoryMax = 0.63 / 0.70 x user@ MemoryMax (reproduces 4639/5155 MiB on local-town) -- the numeric knobs are cells under values.boxkit.* the director commits; name any you need in THOUGHT.
- FENCES (every round, every kid): NEVER run an install for real on this box -- no sudo, no systemctl start/stop/enable/daemon-reload, no write under /etc, /usr, ~/.config/systemd, no crontab write. Reading live files and `systemctl show` read-only is allowed. Every test uses a tmp install_root and a stubbed systemctl. Copied bytes pass `python3 extensions/agi/bin/anonymize.py check`: a host name, address, hardware name or key id becomes a placeholder. Every pytest `timeout 600 prlimit --nproc=300`, named files, --basetemp under /tmp; no test spawns pytest; kids never launch real claude.
- The director commits .agi/config.json cells; a round NEVER does (cli.py refuses it) -- write the cells you need in THOUGHT with their values.

## CORRECTIVE DH.530 -- closes mur-director-engine-17 DH.504-k1..k4 (verify: accept_with_residue x3 + unstructured, the same residues in every slice)
BASE      CUT FROM season2/loops/hypothesis-box-memory-guard-piec-a00-e20a597b tip 80113e993 (worktree a00-e20a597b). No merge. Never rebase. NEVER DH.432 itself.
0 production lines: the test file and nodes only. The round SHRINKS the test file.
1. Row 14 (test_boxkit_templates.py:940-969) is vacuous: anonymize.scan is a literal `v in text` over the denylist VALUES (bin/anonymize.py:72-74) and the fixture denylist is FAKE_BOX, so no kit byte can ever red it -> keep ONE row that is able to go red on a KIT byte: copy a template into tmp, plant one FAKE_BOX value in it, assert scan names it; the unplanted kit stays clean. Delete the rest of the 89-line row. Correct the file header (:51-57) and a00-0acacf93's text that credit it with guarding 'every template byte'.
2. _uncovered's general branch (test:761-763) never reads p['dest_cell'] -> read it; one row: a same-relative piece in the WRONG cell does not cover.
3. test:940 `ANONYMIZE = _load_bin("anonymize")` at IMPORT does sys.path.insert + sys.modules[name] = mod (test:113-120) -> load inside a fixture that restores both; prove it by running test_anonymize_guard.py in the SAME pytest session after this file (a00-0acacf93 reported 7 failures that way).
4. The '/a/b' case (test:876-881) is green under the old AND new rule -> replace it with a case the old `len(p.parts) >= 3` rule gets wrong.
5. Nodes (write.py): a00-cfbbb97e-297f01 prints P5 and the cells[0] fragility as open (a00-f0bbeb3a closed both at rows 11d/11e) -> mark closed; a00-f0bbeb3a cites '_uncovered line 739' (a docstring line; the branch is :761) -> correct; a00-0acacf93-aa4632 :67 prints the checkout root's absolute path value -> write `<repo>` instead (ANON).
ANON      no user name, home or repo path value, host or IP; patterns write <user>; paths write <repo>
TESTS     test_boxkit_templates.py test_anonymize_guard.py (the SAME session, that order) test_bin_help_smoke.py once (timeout 600, --basetemp under /tmp)
FILE SCOPE extensions/agi/tests/test_boxkit_templates.py · experiment:a00-0acacf93-aa4632 · a00-cfbbb97e-297f01 · a00-f0bbeb3a-46e50b (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · 0 production lines · test file net <= 0 vs the base (row 14's 89 lines pay for items 2-4) · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit

## CORRECTIVE DH.580 -- closes mur-director-engine-26 DH.530-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-box-memory-guard-piec-a00-d3d5ead8 tip b32e952ea (branch de-base-580; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 2. UNIT_DIRS hard-codes the tails of two committed boxkit cells (test_boxkit_templates.py:702) — a cell rename inverts _cell_fits_dir silently
2. Lost falsifier, prose-only now: the collapse deleted the only row that pinned the row-4 / anonymize DISJOINTNESS. At base, test_row_14_sees_what_row_4_cannot_and_is_not_a_restatement_of_it (80113e993:973) asserted, per class, scan(planted)==[cls] AND _leaks(planted)==[], plus the checkout root the other way round. After the diff the only scan caller is test_one_planted_kit_copy_goes_red_and_the_kits_own_bytes_stay_clean (test:975-992) and _leaks is called only from rows 4 and 12 — no row asserts that a hostname/ip/mac/board/secret token passes the bespoke denylist CLEAN, yet the file header (test:49-51) and the node table (a00-0acacf93:60-67) still state the disjointness as fact. A future merge of the two denylists is again a silent no-op, which was the deleted row's stated purpose. Residue, not demote: the order asked for one row and the property is measured true.
3. Item 3's sys.path half is inert inside pytest, so the node's claim is wider than the bytes: extensions/agi/tests/conftest.py:408-409 already inserts bin/ on sys.path and :411 imports locations before any test module loads, so under a session the fixture's sys.path restore (test:949-954) is a no-op and only the sys.modules['anonymize'] unbind can matter. The corrected body (a00-0acacf93:83-85) and the parent's P1 gate ('sys.path unchanged / anonymize in sys.modules: False') were measured in a BARE interpreter, not in a pytest session where conftest has already done both. The fix is still a strict improvement; the contamination it names is real by construction (base: BIN_DIR on sys.path True, anonymize bound True).
4. New residue introduced by this diff: _leak_roots_by_depth (test:856-859) keeps the REJECTED `len(p.parts) >= 3` rule alive in the file and row 12 pins its wrong answer verbatim (test:873 `assert _leaks("cd /a and ls\n", old) == []`). Legitimate as a comparison oracle and red-first is real (on Path('/a') the old rule yields [], the new yields ['/a']), but it means a later correct fix of that helper would red a passing row for the right reason at the wrong place. Named, not blocking.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_boxkit_templates.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_boxkit_templates.py · .agi/nodes/experiment/a00-0acacf93-aa4632.md · .agi/nodes/experiment/a00-c8edb94f-25553f.md · .agi/nodes/experiment/a00-cfbbb97e-297f01.md · .agi/nodes/experiment/a00-f0bbeb3a-46e50b.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over b32e952ea · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.580: mur-director-engine-26 DH.530-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
