---
id: experiment:a00-b0953a73-9da341
mint_id: b96e349bd78a48d9861dad361f7e01b9
type: experiment
parents:
  - hypothesis:l4-sb-status-resolves-from-home-not-from-stub-depth
next_edges: []
confidence: 0.9
edited_by: a00-569fe8ad
evidence_runs:
  - experiment:a00-b0953a73-9da341
loop: hypothesis:l4-sb-status-resolves-from-home-not-from-stub-depth@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 9205ffbe6a57c985
season: 2
title: A00 b0953a73 9da341
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b0953a73-9da341

## Experiment

Built the fix for the L4.165 residual (hypothesis:l4-sb-status-resolves-
from-home-not-from-stub-depth): `sb-status`'s argv[0] must not depend on how
deep `locations.streamer_stub` sits under the user's home.

**1. `extensions/agi/bin/commands.py` — `_substitute` only:** added a
`<home>` placeholder expanding to `Path.home()`:
`... .replace("<home>", str(Path.home()))`. `<root>`/`<engine>`/`<stub>`
replacements untouched. No other function, no other file in `bin/` changed.

**2. `extensions/agi/briefs/commands.stream.fragment.md`:** changed
`sb-status` argv[0] from `<stub>/../../bin/sb-status` to
`<home>/bin/sb-status` and rewrote the prose to state that `<home>` is the
user's home directory, expanded by `_substitute` alongside
`<root>`/`<engine>`/`<stub>`, so the wrapper path no longer depends on stub
depth (the old spelling is kept only as explanation). The other three
commands' argv untouched.

**3. `extensions/agi/tests/test_commands.py`:** added
`test_real_fragment_sb_status_resolves_from_home_not_stub_depth` —
materialises the REAL fragment's `commands:` yaml into a temp project with
`locations.streamer_stub` pinned THREE levels deep
(`tmp_path/a/b/stub`), asserts
`commands.get(graph, "sb-status").argv[0] ==
os.path.join(str(Path.home()), "bin", "sb-status")` and that it is an
existing executable file, plus the both-halves wrapper check (wrapper body
invokes the real stub's `hold.sh --status` AND `panic.sh --status`, each
executable). Also extended the manual substitution in
`test_stream_fragment_argv_resolves_to_executable_files` to expand
`<home>` (it reads the REAL fragment, which now carries the token).

**Commands run:**
- `python3 -m pytest extensions/agi/tests/test_commands.py -q` → 34 passed
- Verify green on the fixed fragment.

## Evidence

**Resolved argv[0] for the depth-3 stub (fixed fragment):**
`/home/ubuntu/bin/sb-status` (= `os.path.join(str(Path.home()), "bin",
"sb-status")`) — an existing executable file.

**Mutation, both directions (acceptance):**
1. Reverted the fragment's `sb-status` argv to `<stub>/../../bin/sb-status`;
   ran the file → RED:
   ```
   AssertionError: sb-status: argv[0] should resolve from home to
   /home/ubuntu/bin/sb-status (stub is
   /tmp/pytest-of-ubuntu/pytest-1033/.../a/b/stub, THREE levels deep),
   got /tmp/.../a/b/stub/../../bin/sb-status
   ```
   (the OLD spelling resolves to `/tmp/.../a/bin/sb-status`, a MISSING path —
   the assertion names it, exactly the residual the hypothesis predicted).
   1 failed, 33 passed.
2. Restored `<home>/bin/sb-status` byte-identically → 34 passed.

A test that passes on the fixed fragment and fails on the buggy one is the
proof. The depth-independence claim is PROVED on the built bytes.

## Agent Notes
Added <home> placeholder to commands._substitute; sb-status argv[0] is now <home>/bin/sb-status, stub-depth-independent. Added depth-3 mutation test (red on old <stub>/../../bin/sb-status spelling). 34 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-569fe8ad, L4.178. ACCEPT the artifact, KEEP the verdict proved.

(1) WHAT THE INSTRUCTION SAID — hypothesis:l4-sb-status-resolves-from-home-not-from-stub-depth: CLAIM commands.py `_substitute` gains a `<home>` placeholder and the fragment names `<home>/bin/sb-status`; the resolves test asserts the path for a stub at another depth. FALSIFIER: a configured stub at depth 3 resolving sb-status to a missing path. FILE SCOPE: commands.py (_substitute only) + the fragment + test_commands.py.

(2) WHAT THE MACHINE ACTUALLY DOES — re-read and re-ran, not read from the kid report: commands.py `_substitute` now ends `.replace("<home>", str(Path.home()))` after the untouched `<root>`/`<engine>`/`<stub>` lines; the fragment sb-status argv[0] is `<home>/bin/sb-status` with prose updated; the new `test_real_fragment_sb_status_resolves_from_home_not_stub_depth` pins `locations.streamer_stub` to `tmp_path/a/b/stub` (three levels deep) and asserts argv[0] == `~/bin/sb-status`, a file and executable, plus the both-halves wrapper check. My own mutation, independent of the kid: reverting the fragment argv to `<stub>/../../bin/sb-status` turned exactly that one test RED with `assert .../a/b/stub/../../bin/sb-status == /home/ubuntu/bin/sb-status` (1 failed, 33 passed), and restoring left the file byte-identical (md5 1dda48060d7c83f83b6ee0f9b5316796). `python3 -m pytest extensions/agi/tests/test_commands.py -q` = 34 passed.

(3) THE NEAR MISS — a reader could call this proved on the green suite alone and never check that the new test fails on the OLD spelling; a test that passes in both directions certifies nothing. I made that check myself. Second near miss: `proved` here survives because the claim LETTER is exactly what landed (placeholder added, fragment respelled, depth test added) — unlike L4.165, whose claim asked the fragment to name both argv and could not be satisfied by one flat argv[0]. The two-levels-up residual from L4.165 is now closed rather than re-labelled.

(4) DEVIATION — none. No artifact edit; my mutation was restored and md5-verified. The new test carries `@stub_only` (which implies REAL_ROOT is not None), so it skips rather than fails on a box without the stub — the same external-artifact convention as the sibling real-fragment test, and adequate here because its only off-machine assertion is `~/bin/sb-status`, which the stub install creates.
<!-- THOUGHT:END -->

PARENT REVIEW (a00-569fe8ad, L4.178): ACCEPT, verdict proved kept. Independent mutation: old <stub>/../../bin/sb-status spelling turns the new depth-3 test red; restore is md5-identical; 34 passed. Closes the L4.165 residual (stub-depth dependence).
