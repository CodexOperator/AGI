---
id: experiment:a00-f7270e83-61eada
mint_id: 928c028dba6f4e91b4218dbb8b71f33e
type: experiment
parents:
  - hypothesis:send-read-prints-every-unread-block-and-every-dm-send-nudges
next_edges: []
confidence: 0.9
edited_by: director-engine
evidence_runs:
  - experiment:a00-f7270e83-61eada
  - experiment:a00-cf800c23-1459e5
loop: hypothesis:send-read-prints-every-unread-block-and-every-dm-send-nudges@s2
model: claude-opus-5-5
production_lines: 0
profile: balanced
role: kid
scaffold_hash: ed8db90b44ed8fb9
season: 2
title: "EG.77 corrective: send.py pointers re-measured at ecaab9920, cf800c23 verdict aligned to its review"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f7270e83-61eada

CORRECTIVE DH.EG.77 (kid a00-f7270e83, cut tip ecaab9920). Three node-text items,
0 production / 0 test lines. Every number below was measured with `grep -n` on this
worktree's `extensions/agi/bin/send.py`, which is byte-identical to ecaab9920 (the
numstat further down lists no send.py row).

## Experiment

| # | item | node : body lines | before | after (tip ecaab9920) | state |
|---|---|---|---|---|---|
| 1 | +14 docstring re-staled the pointers | a00-c3bf7379 : 12-24 | read 3994 · _nudge 2659 / 2600 · _print_deferred_block 3897-3913 (print 3907-3913) · _notify_undelivered 2906-2943 | 4008 · 2673 / 2614 · 3911-3927 (print 3921-3927) · 2920-2957, one call 2976; tip named beside each | FIXED |
| 2 | sibling `def read(` pointer | a00-5e3cfa03 : 113 | "3956 at this tip", UNVERIFIED | "3956 at 38fa6e926, 3970 at tip ecaab9920" + grep line pasted | FIXED |
| 3 | one node, two verdicts | a00-cf800c23 frontmatter | verdict proved · confidence 0.85 | inconclusive_lean_proved:55 · 0.55, same as its PARENT REVIEW | FIXED |

Beyond the brief: table rows 2659/2600, which the EG.41 note had certified CORRECT at
38fa6e926, sit below the docstring too, so they had also moved +14. Both were corrected.
The EG.41 notes (a00-c3bf7379 body ~154, a00-5e3cfa03 note above the fix) are left
as they are. They are the record of the 38fa6e926 numbering and each names that tip.
Each edited node has a THOUGHT that gives the reason.

## Evidence

grep -n on extensions/agi/bin/send.py (tip ecaab9920):
```
1890:def _clear_deferred(root: Path, seat: str) -> None:
2614:            _clear_deferred(root, to)
2673:    _clear_deferred(root, to)
2920:def _notify_undelivered(root: Path, seat: str, rec: dict) -> None:
2957:            _nudge_deferred_path(root, seat).write_text(json.dumps(rec))
2960:def wake_all_local(root: Path, tmux_session: str | None = None) -> bool:
2976:            _notify_undelivered(root, name, rec)
3911:def _print_deferred_block(root: Path, me: str, deferred: dict,
3922:    print(f"deferred dm from {sender} ({_deferred_stamp(root, me, defe...
3927:    print(body, end="")
3970:def read(root: Path, me: str, sender: str | None,
4008:        _print_deferred_block(root, me, deferred, wrap=wrap)
```
cf800c23 frontmatter after `write.py 'set verdict inconclusive_lean_proved:55 && set confidence 0.55'`:
```
8:confidence: 0.55
40:verdict: inconclusive_lean_proved:55
```
`git diff --numstat ecaab9920` (this worktree, before this node was written):
```
3	3	.agi/nodes/experiment/a00-5e3cfa03-650288.md
8	8	.agi/nodes/experiment/a00-c3bf7379-8e12ed.md
4	4	.agi/nodes/experiment/a00-cf800c23-1459e5.md
```
The rows are node files only. production 0, test 0, USD 0, and this is the only kid.
`test_bin_help_smoke.py` (env -u TMUX -u TMUX_PANE, --basetemp /tmp/pt-a00-f7270e83): `72 passed, 6 skipped in 8.03s`.

OUTSIDE: none. All three fixes were inside FILE SCOPE, and a00-143f92b1 needed no edit.
Git runs: `git diff --numstat` only. The brief's `git show <tip>:send.py` was swapped
for a grep of the worktree copy, which has the same bytes, because the kid contract allows
only the numstat read.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Director close (TMM.327) of mur-eg-27 EG.77-k1, node prose only, measured by grep on send.py at 96980237f (the range touches no code, so ecaab9920 reads the same). The before-value of read goes 3995 -> 3994 (38fa6e926:3994 is the _print_deferred_block call), so the row's +14 now holds. The pasted grep line for the deferred-dm print goes 3921 -> 3922 (3921 is the sender line). Siblings changed in the same commit: a00-c3bf7379's clear-itself row now cites _clear_deferred with the unlink at 1920 (the quoted 'if p.exists()' text exists at no tip), and its Honest limits carries both tips' nudge numbers. a00-5e3cfa03's caller pointer now reads 2429.
<!-- THOUGHT:END -->

## Agent Notes
EG.77 corrective: 3/3 items fixed in node text at tip ecaab9920 (c3bf7379 pointers +14 incl 2 extra table rows, 5e3cfa03 def read 3970, cf800c23 verdict -> lean_proved:55); 0 prod/test lines
