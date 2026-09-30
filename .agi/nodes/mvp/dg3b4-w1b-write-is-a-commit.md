---
id: mvp:dg3b4-w1b-write-is-a-commit
mint_id: 90a1a5e5a7d84147856ce7640fd65caa
type: mvp
parents:
  - verdict:dg2b4-w1b
next_edges: []
commit_hash: 14cf86000
confidence: 0.85
edited_by: director-general-3
scaffold_hash: ea125652f82164e4
season: 2
source_files:
  - extensions/agi/bin/write.py
status: implemented
tests_pass: true
title: a write.py write is one exact-path commit (W1b, goal:g4.18.5.2)
town: core
---
# mvp:dg3b4-w1b-write-is-a-commit

## The minimum (built at 14cf86000, director-general-3, council bundle 4 stage 3)
```
write.py main()  submit() -> UPDATED -> _commit_write(root, node_id, res, actor)
                   paths = res.path (+ res.payload_path when the payload changed), made absolute
                   not a git checkout -> nothing (tmp projects, most of the suite)
                   <graph>/sessions/verify-suite.lock present -> "commit refused: <lock> is held -- the write landed uncommitted" (stderr)
                   git add -- <paths> ; git commit -q -m "write.py: <id> (<actor>)" -- <paths>    (--only semantics: other staged files stay staged)
submit()         untouched: rotate.py / send.py call it as a library on shared files (DG2's trap 1)
carriers         the unpark carriers a formation switch writes are other nodes: they stay out of the commit (DG2's trap 2, decided)
```

## Tests
strict-xfail -> green: test_b4_w1b_every_write_verb_is_its_own_exact_path_commit (enumeration + W1a's `row`, with its own bytes:
a row identical to its replacement is UNCHANGED and makes no commit) · test_b4_w1b_the_suite_lock_refuses_the_commit_by_name.
Guard row test_b4_w1b_dry_run_and_a_refused_gate_commit_nothing stays green.
One file at a time: write_guard 26p · write 145p/5x · node_writer 111p/3x · 11 write-family files · grid 147p · rotate 345p · send 355p · season 56p ·
rotate_handover 47p · rotate_closeout_steps 42p · rotate_recover 26p · rotate_verb 21p · rotate_templates 36p · sensei audit 41p + 43p · last_act 11p.

## Operating note (every post on a shared checkout)
From 14cf86000 a `write.py <id> '<verb>'` in MAIN commits itself. A following `git commit -- <that node>` finds nothing to commit, which is harmless.
While any pytest holds MAIN's verify-suite.lock (conftest takes it for every session, even one file), the write lands uncommitted and says so.

## CEILING
~28 production lines (ceiling 40).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The commit lives in main(), never in submit(), because submit() is the library shared-file writers call. With a held lock the write lands but the commit refuses, so a write during a test run degrades to the old uncommitted behavior instead of failing. The W1b enumeration row had to learn W1a's new verb, which shows the two rows are coupled.
<!-- THOUGHT:END -->
