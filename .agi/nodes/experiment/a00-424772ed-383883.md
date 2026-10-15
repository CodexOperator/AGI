---
id: experiment:a00-424772ed-383883
mint_id: 9e10b625fb7b4b77b63bb94f2fb26836
type: experiment
parents:
  - hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go
next_edges: []
confidence: 0.9
edited_by: a00-3f96a9a0
evidence_runs:
  - experiment:a00-424772ed-383883
line_ceiling: 12
loop: hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 3c19a3af6de50866
season: 2
title: "Four node-wording residues closed: duplicate H1, conjunct inflation, and a bullet that contradicted its own correction"
town: core
verdict: inconclusive_lean_proved:85
---
# experiment:a00-424772ed-383883

Node-wording slice, 0 production lines, four residues closed by `write.py` under
my own `--actor`.

## The four residues, and what each one was

1. Conjunct inflation. `cli._CLAIM_ITEM_RE` is `re.compile(r"\(\s*(\d+)\s*\)")`
   and `_claim_conjunct_numbers` unions the `testable_claim` field with EVERY
   match in the BODY (cli.py:1169-1184), so a review that cites its own four
   orders as `(1)`..`(4)` manufactures a fourth conjunct. Measured on the base
   before any edit: `[1, 2, 3, 4]`. Fixed by rewording the DH.459 / DH.465
   review prose to `ORDER 1`..`ORDER 4` and `gate order 3a` / `wire order 2`
   shapes. The field's own three conjuncts were not touched.
2. The body CLAIM section lettered its parts `(a)`/`(b)` while the field
   numbers `(1)`/`(2)`/`(3)`. Rewritten as CONJUNCT 1 / 2 / 3, one per field
   conjunct, same text, no parenthesised digit.
3. `experiment:a00-416266d2-e77f31`, "What this does NOT settle", carried a
   bullet asserting the None arm was "deleted, not commented-in-place" -- flatly
   contradicting its own CORRECTION section and its own title. The DH.449
   director ruling REVERSED that deletion: the `gdir is None` arm is restored
   with its one-line log and docstring clause. The bullet is rewritten to say so
   and to name what genuinely remains open (a docstring assertion with no
   type-check behind it).
4. `experiment:a00-02784673-21e2f6` emitted its H1 twice, on body lines 2 and 3
   (immediately after the `BODY:BEGIN` marker). One left.

## Proof I ran

    $ python3 -c "import sys; sys.path.insert(0,'extensions/agi/bin'); import cli; \
        from pathlib import Path; print(cli._claim_conjunct_numbers(Path('.agi/nodes/hypothesis/heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go.md')))"
    [1, 2, 3]

Before this slice the same line printed `[1, 2, 3, 4]`. The third conjunct
appears only in the frontmatter field, which is where the claim lives.

    $ cd extensions/agi/tests && python3 -m pytest test_heal.py -q --basetemp /tmp/dh477-a00-424772ed
    23 passed in 0.31s

Hygiene, not evidence: this slice changes prose, so the only mechanical proofs
are the conjunct print and the fact that nothing moved.

    $ git diff --numstat -- extensions/agi/bin/heal.py extensions/agi/tests/test_heal_worktree_refusal.py
    (no output)

0 production lines against a 12-line ceiling. No test file, no `cli.py`, no
`heal.py` touched.

## The commit trap, and the deliverable

A round's commit scope is the set of node ids DISPATCH named. My dispatch target
is the hypothesis, so the hypothesis edit would commit and the TWO EXPERIMENT
edits would sit `M` forever -- the exact trap DH.436 and DH.459 both recorded.
`cli._round_committable` returns True for `experiment:a00-416266d2-e77f31` and
`experiment:a00-02784673-21e2f6`, so both are passed on `done` via `--owns`
alongside `--node-id`, widening the scope legally rather than by hand.

## What this does NOT settle

- The `cli.py` union itself is untouched, by orders and by scope. Any future
  review that writes a parenthesised digit in a hypothesis body will inflate the
  conjunct set again. This slice makes the CURRENT node correct; it does not make
  the machine stop counting prose. That is a g15 for the director.
- The evidence here is a single probe plus a hygiene suite run. A claim about
  prose has no red-first shape; the falsifier is the conjunct print going back to
  four, which anyone can re-run in one line.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.477 PARENT REVIEW (a00-3f96a9a0) -- reviewing experiment:a00-424772ed-383883 from the BYTES, not from the result file. The four residues landed; one mechanism claim in the reasoning record does not survive my probe.

(1) WHAT THE INSTRUCTION SAID, quoted from my own orders to this kid: "Any byte outside FILE SCOPE = the parent cuts you, do not accept"; "A deliverable the diff does not carry is a demotion, not a note"; and the deliverable I added because two earlier rounds lost these bytes -- "pass --owns experiment:a00-416266d2-e77f31 experiment:a00-02784673-21e2f6 ... the two experiment nodes stay M and the residue stands".

(2) WHAT THE MACHINE ACTUALLY DOES, all six measurements mine, on the changed bytes:
- wire/probe 1: cli._claim_conjunct_numbers on the live hypothesis node prints [1, 2, 3]. I ran the identical line on the base before the kid and it printed [1, 2, 3, 4], so the manufactured fourth conjunct is gone, and the mechanism is the one the residue named: cli.py:1169-1184 unions the testable_claim field with EVERY _CLAIM_ITEM_RE match in the body.
- gate/probe 2: grep -c of the exact H1 string in a00-02784673 returns 1, sitting on body line 25 immediately after the BODY:BEGIN marker. The duplicate is gone.
- gate/probe 3: sweeping every _CLAIM_ITEM_RE hit by line across the three in-scope nodes, the ONLY hits left in the hypothesis are frontmatter line 11, the field itself. No review prose carries a parenthesised digit any more, so nothing re-inflates the set without a new writer.
- auth/probe 4: a00-416266d2 bullet b now reads SUPERSEDED BY THE CORRECTION BELOW, not deleted, and names what genuinely stays open, so the body agrees with its own DH.449 CORRECTION. I read heal.py:3087-3090 myself: the gdir-is-None arm with its one-line _watch_log and its docstring clause IS present, so the prose this round wrote about code it never touched is true.
- gate/probe 5: diff -rq of the whole .agi tree against the base lists exactly four changed node files and ZERO source or test files; extensions differs only in __pycache__ and one .pytest_cache, i.e. run artifacts of the one suite run the orders asked for. FILE SCOPE held.
- wire/probe 6, the one that mattered most: git status --porcelain -- .agi/nodes is EMPTY, and show --numstat on b23b13c12 carries a00-02784673 (1/2), a00-416266d2 (10/4), the kid node (95/0) and the hypothesis (11/5), with no .py in the commit. So --owns genuinely widened the round commit scope and the byte-loss that DH.436 and DH.459 each recorded is CLOSED at 0 production lines. That is the real finding of this round, and it was a one-flag miss nobody had tried.

(3) THE NEAR MISS I REFUTE, named: this node THOUGHT asserts the hypothesis body LAST LINE is unterminated, that every whole-body body_patch against the node therefore refused with a removal mismatch at the last body line, and that _standard_unified_diff emits the no-newline marker "for the added side only". All three halves fail against the mechanism.
- read_bytes().endswith(b"\n") is True on the base AND on the current file. There is no unterminated last line here to mismatch, so the stated cause was never present in the bytes this round edited.
- write.py:2615-2621 says in its own docstring that the marker follows EVERY content line with no trailing newline, on both sides, and I ran it in memory on an unterminated string: the rendered diff carried the marker twice, once per side, and apply_unified_diff round-tripped the unterminated last line with no error at all. The opposite of a refusal.
So whatever the four refusals really were, this is not their mechanism. The node SECOND near miss IS correct and is the lesson worth keeping: a diff built from the WHOLE FILE and handed to a body verb is offset by the height of the frontmatter, so the hunk must be built from the body alone. A node that publishes a confident false mechanism is worse than one that publishes none -- the next seat reads it, concludes this hypothesis is unpatchable by body_patch, and loses the run diagnosing the real blocker. That is why the verdict below is demoted from proved: the four residues are proved on the bytes, the reasoning record that explains them is not.

(4) IF I DEVIATED FROM A STANDING RULE: none bypassed. I ran READ-ONLY git (log, status, show --numstat) because whether the commit carried the bytes was the deliverable under review; no mutating git, no commit, no push, and not one byte of the kid authored region landed by hand -- the verdict demotion and this review went through write.py under my own --actor.
<!-- THOUGHT:END -->

## Agent Notes
Four node-wording residues via write.py, 0 production lines: cli._claim_conjunct_numbers on the hypothesis went [1,2,3,4] -> [1,2,3]; body CLAIM now names the field's three conjuncts; a00-416266d2's deleted-arm bullet rewritten to agree with its own DH.449 CORRECTION (the arm was RESTORED); duplicate H1 in a00-02784673 removed. Probe printed [1, 2, 3]; test_heal.py 23 passed. --owns widens the commit scope to both experiment nodes so the bytes commit.

PARENT REVIEW DH.477 (a00-3f96a9a0): 1 kid, residues ACCEPTED, verdict demoted proved -> inconclusive_lean_proved:85 on one refuted mechanism claim. probes, all mine on the bytes: wire -- cli._claim_conjunct_numbers on the hypothesis = [1, 2, 3] (base was [1, 2, 3, 4]); wire -- git status --porcelain -- .agi/nodes is EMPTY and b23b13c12 carries all three corrected nodes (1/2, 10/4, 11/5) plus the kid node, no .py, so the --owns commit-scope fix WORKS and the DH.436/DH.459 byte-loss trap is closed; gate -- the exact H1 appears once in a00-02784673; gate -- the only remaining _CLAIM_ITEM_RE hits in the hypothesis body are on the field line 11 itself; auth -- a00-416266d2 bullet (b) agrees with its own CORRECTION and heal.py:3087-3090 does carry the restored gdir-is-None arm; gate -- diff -rq over the whole .agi tree shows four node files and no source or test file. DEMOTED, named probe: the THOUGHT claims an unterminated last body line and a one-sided no-newline marker caused four body_patch refusals; read_bytes() ends with a newline on base and now, and _standard_unified_diff emits the marker on BOTH sides (write.py:2615-2621) and apply_unified_diff round-trips an unterminated line cleanly, so the stated cause is not the cause. RESIDUE, named not patched, for the director: the hypothesis body still carries an absolute worktree path in a pre-existing DH.465 line (anonymization), and the cli.py union that makes conjunct counts a function of prose is untouched -- a g15, as the kid also recorded.
