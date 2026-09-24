---
id: experiment:a00-0812237b-2177d5
mint_id: 0f777698e22e420fbfb35cbe4bba06e9
type: experiment
parents:
  - hypothesis:migrate-transcript-dest-test-asserts-an-independent-root
next_edges: []
confidence: 0.9
edited_by: a00-c043cd15
evidence_runs:
  - experiment:a00-0812237b-2177d5
loop: hypothesis:migrate-transcript-dest-test-asserts-an-independent-root@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "inject a DECOY mutant via a pytest -p plugin: rotate.transcript_from_registry_dict returns rotate.CC_PROJECTS_DIR/'decoy'/<slug>/<sess>.jsonl; run env -u TMUX -u TMUX_PANE PYTHONPATH=extensions:scratch python3 -m pytest extensions/agi/tests/test_migrate_channel.py -q -p decoy_plugin -k test_migrate_transcript_dest_is_the_path_resume_reads", "expected": "the pinned exact-equality oracle refuses the decoy (RED at line 414); the pre-fix startswith(rotate.CC_PROJECTS_DIR) oracle on the SAME dest evaluates True, exposing it as tautological", "observed": "decoy plugin: 1 failed at test_migrate_channel.py:414 (dest .../projects/decoy/... != fixture/...); standalone: old_oracle=True, new_oracle=False on the identical decoy dest", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "inject a WRONG-ROOT mutant via pytest -p plugin: rotate.transcript_from_registry_dict returns /tmp/wrong-root-mutant-probe/<slug>/<sess>.jsonl (ignores CC_PROJECTS_DIR); run the same single-test -k selector", "expected": "test_migrate_transcript_dest_is_the_path_resume_reads FAILS by name at the pinned assertion", "observed": "1 failed, 34 deselected in 0.11s -- AssertionError at extensions/agi/tests/test_migrate_channel.py:414, dest=/tmp/wrong-root-mutant-probe/-home-x--agi-worktrees-p/sess-1.jsonl", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "patch rotate.CC_PROJECTS_DIR to a fresh tmp fixture in a clean process and call rotate._migrate_transcript_dest(Path('/home/x/.agi/worktrees/p'),'sess-1'); then env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_migrate_channel.py -q; then git show bd1c58f59f --stat", "expected": "the patched module global threads live to the produced dest (dest lands under the fixture), the named file is green, and the commit carries test_migrate_channel.py plus the experiment node only (test-only, 0 production lines)", "observed": "real fn dest under patched global=True; 35 passed, 2 warnings; stat = 2 files changed (test_migrate_channel.py +12/-3, experiment node) and no rotate.py / production path", "result": "held"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: d8e44ffbc125ec62
season: 2
title: Migrate dest test pins an independent root; mutant caught red
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-0812237b-2177d5

## What was done

Test-only fix to the tautological oracle in
`test_migrate_transcript_dest_is_the_path_resume_reads`
(`extensions/agi/tests/test_migrate_channel.py`, formerly L400-408).

| before (defect) | after (independent oracle) |
|---|---|
| `assert str(dest).startswith(str(rotate.CC_PROJECTS_DIR))` | `assert dest == fixture / "-home-x--agi-worktrees-p" / "sess-1.jsonl"` |
| compares dest against the live global the code derives from (rotate.py:95) | `monkeypatch.setattr(rotate, "CC_PROJECTS_DIR", fixture)`, `fixture = tmp_path/".claude"/"projects"` (separately built) |
| signature `(tmp_path)` | signature `(tmp_path, monkeypatch)` |

The existing `dest.name`, `dest.parent.name`, `.migrate-transcript.jsonl`
assertions were kept unchanged. No production file was changed.

## Evidence

**Green on the tip (test-only):**
```
env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_migrate_channel.py -q
35 passed, 2 warnings in 0.81s
```

**Falsifier — mutant in `transcript_from_registry_dict` (rotate.py:6747):**
```
-  transc = str(CC_PROJECTS_DIR / slug / f"{sess}.jsonl")
+  transc = str(Path("/tmp/wrong-root-literal") / slug / f"{sess}.jsonl")
```
Mutant file md5 `c9c1b90664e15d0b1da9b013e62a3186` (pristine `efce5c66751f45037dee087904ddd829`).
Observed failure (RED), exactly the new assertion:
```
env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_migrate_channel.py -q \
  -k test_migrate_transcript_dest_is_the_path_resume_reads
E  AssertionError: assert PosixPath('/tmp/wrong-root-literal/-home-x--agi-worktrees-p/sess-1.jsonl')
E       == PosixPath('/tmp/pytest-of-belam/.../.claude/projects') / '-home-x--agi-worktrees-p' / 'sess-1.jsonl'
1 failed, 34 deselected
```
`rotate.py` was then restored byte-exactly to md5 `efce5c66751f45037dee087904ddd829`;
`git status --porcelain extensions/agi/bin/rotate.py` is empty. The mutant was
never committed; it existed only for the falsifier run.

**Production lines changed:** `git diff --numstat -- extensions/agi/bin/rotate.py`
returned nothing — 0 production lines (test file only: 9 insertions, 3 deletions).

## Note on the tier gate

`pytest extensions/agi/tests/test_migrate_channel.py::test_...` (node-id
selector) is refused by the kid tier gate as a "bare full-suite directory run";
the same single test runs fine via `-k test_...`. This cost a turn.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-c043cd15, EF.82) of experiment:a00-0812237b-2177d5.

(1) INSTRUCTION: "A kid's tests are its CLAIM, not your evidence ... One negative probe per claim conjunct, run by YOU, recorded as `probes:` in the kid's node." I judged the DIFF (git show bd1c58f59f), not the result file.

(2) MACHINE: the committed diff carries exactly the claimed bytes -- test_migrate_transcript_dest_is_the_path_resume_reads (extensions/agi/tests/test_migrate_channel.py:400-414) drops `assert str(dest).startswith(str(rotate.CC_PROJECTS_DIR))`, gains `monkeypatch` + `fixture = tmp_path/".claude"/"projects"` + `monkeypatch.setattr(rotate,"CC_PROJECTS_DIR",fixture)`, and pins `assert dest == fixture / "-home-x--agi-worktrees-p" / "sess-1.jsonl"`. The commit stat is 2 files (test file + experiment node), 0 production paths; rotate.py md5 on the tip is efce5c66, the kid's stated pristine value. I did NOT trust the report: I re-ran the falsifier myself, twice, with mutants the kid did not use, injected through a pytest -p plugin so no shared source file was touched. Both went RED at exactly the pinned assertion (line 414). The decoy probe is the stronger one -- a mutant deriving under CC_PROJECTS_DIR/'decoy' computes old_oracle=True but new_oracle=False, which is the tautology the leaf exists to kill.

(3) NEAR MISS: a fix that keeps `startswith(str(rotate.CC_PROJECTS_DIR))` after redirecting the global satisfies the words "pinned to a separately built tmp path" and still certifies nothing -- the assertion would remain the code's own root compared to itself. The equality against `fixture / <slug> / <name>` is what makes the oracle independent; a redirect alone is the plausible-but-lost implementation.

(4) ACCEPT: verdict proved stands; probes recorded. Caveat carried to the node: the mutant lives only in this parent's probe run and is not a committed regression test, so a future re-introduction of a wrong root is caught by CI only via the exact-path assertion, not by an independent fixture harness.
<!-- THOUGHT:END -->

## Agent Notes
test_migrate_transcript_dest_is_the_path_resume_reads now monkeypatches rotate.CC_PROJECTS_DIR to a tmp fixture and asserts dest == fixture/-home-x--agi-worktrees-p/sess-1.jsonl; mutant wrong-root at rotate.py:6747 observed RED, rotate.py restored byte-exact (efce5c66); full file green 35 passed; 0 production lines

Parent review EF.82: ACCEPTED proved. Diff inspected (test-only, 0 production lines; rotate.py efce5c66 pristine). Three parent-run negative probes held, not the kid suite: (P1 gate) decoy mutant under CC_PROJECTS_DIR -> new exact-equality oracle RED at L414 while the old startswith oracle =True, tautology exposed; (P2 gate) wrong-root mutant -> RED at L414; (P3 wire) patched CC_PROJECTS_DIR threads to _migrate_transcript_dest, file green 35 passed. Caveat: the mutant is a probe, not a committed regression.
