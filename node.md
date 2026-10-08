---
id: experiment:a00-298f04df-fe3499
mint_id: dbd003267d9e465fbef0a2413b7faf42
type: experiment
parents:
  - hypothesis:a-stale-index-lock-is-cleared-or-named-and-a-failed-round-commit-is-never-silent
next_edges: []
confidence: 0.85
edited_by: a00-298f04df
evidence_runs:
  - experiment:a00-298f04df-fe3499
  - experiment:a00-110f9e30-debcf3
loop: hypothesis:a-stale-index-lock-is-cleared-or-named-and-a-failed-round-commit-is-never-silent@s2
model: claude-opus-5-5
production_lines: 0
profile: balanced
role: kid
scaffold_hash: c51853693ec6a81e
season: 2
title: "EG.64 corrective: range ceiling pasted, round pointer moved to THOUGHT, stale hypothesis cites named"
town: local-maxxing
verdict: inconclusive_lean_proved:85
---
# experiment:a00-298f04df-fe3499

## Experiment

EG.64 corrective, closing mur-eg-14 (EG.45-k1 accept_with_residue). TEXT-ONLY round: every edit is
write.py on `experiment:a00-110f9e30-debcf3`; production 0, test 0, no code opened for writing.

| item | where | shape | what landed |
|---|---|---|---|
| 1 | a00-110f9e30-debcf3 Ceiling | range numstat never pasted | the 42/39 block labelled as the DH.668 round; the range against CUT tip `dedca8545` pasted beneath it (production 0, test 0) |
| 2 | a00-110f9e30-debcf3 body (was :78) | round pointer in the body | `corrected in EG.45 per mur-eg-13` removed via write.py `sub`; the delta it carried is now the node's THOUGHT (write.py `thought`) |
| 3 | hypothesis push_further | stale cites, OUTSIDE file scope | named below, never touched |

## Evidence

Cites re-read in the bytes (`sed -n 2400,2456p extensions/agi/bin/cli.py` at the cut tip):

```
2405        if os.stat(base).st_uid != os.getuid():
2407        if os.getuid() and os.stat(f"{base}/fd").st_uid == 0:
2408            return ""
2452            except OSError:
2453                continue
```

Final ceiling, measured against the CUT tip (working tree, after every edit on the target node; this node
is untracked until `cli.py done` commits it, so it is not in the range):

```
git diff --numstat dedca8545
15	3	.agi/nodes/experiment/a00-110f9e30-debcf3.md
```

Production **0**, test **0**, node text only.

Tests, once: `env -u TMUX -u TMUX_PANE -u AGI_POST -u AGI_SEAT python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q --basetemp=<shm>` (TMPDIR under /dev/shm)
-> `72 passed, 7 skipped in 5.47s`.

## OUTSIDE FINDING (director's findings row, file not touched)

- `.agi/nodes/hypothesis/a-stale-index-lock-is-cleared-or-named-and-a-failed-round-commit-is-never-silent.md:9`
  (push_further): it cites `cli.py:2406` for the non-dumpable uid-0 fd-dir exit, which is **cli.py:2407-2408**,
  and `cli.py:2455` for `except OSError: continue`, which is **cli.py:2452-2453** -- the same stale-cite
  class as mur-eg-13's item 1, and the hypothesis is outside this round's FILE SCOPE.

## Struggle

`write.py 'replace body 54:54 -'` refuses a single line inside a paragraph (anchor guard); `sub old => new`
did the one-phrase fix without `--force`.
Raw output, screenshots, logs.

## Agent Notes
EG.64 text-only corrective: range numstat vs dedca8545 pasted (prod 0, test 0), EG.45 round pointer moved from body to THOUGHT, stale push_further cites cli.py:2406->2407-2408 and :2455->2452-2453 named as OUTSIDE finding
