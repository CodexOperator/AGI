---
id: hypothesis:l4-dead-detached-kid-never-marked-terminal
mint_id: 69d241c82e4b42eba0b7a99601934c93
type: hypothesis
parents:
  - idea:l4-dead-detached-kid-never-marked-terminal
next_edges: []
edited_by: sanctuary-helper
scaffold_hash: da6d2a5214a5a3bf
season: 2
testable_claim: "A detached kid's agent.json stays status:running forever if the kid process dies without calling cli.py done, because no reaper phase watches kids -- only dispatch.py's parent-facing reaper (_reaper_phase/_reap_one/_reap_one_impl, dispatch.py:1705-1940+) does, and a parent instructed to poll its kids until each is done or failed polls a dead one forever by construction. Reproduced live by the assigning director: a kid died on an upstream 404, its agent.json read status:running/finished_at:null two minutes after the pid was confirmed dead, cli.py status echoed the stale status, and the parent polled the corpse for ~9 minutes before being killed by hand. ROOT-CAUSED FURTHER: the primitive to detect this already exists and is already imported by stall_detect.py's own module -- spawn_budget._pid_alive(pid) (spawn_budget.py:208-244), a zombie-aware, EPERM-aware liveness check, already the thing dispatch.py's parent reaper effectively relies on. A kid's own agent.json record already carries a `pid` field (confirmed against the preserved evidence -- see brief). Falsifiable: (1) a fixture built from the frozen real evidence at .agi/sessions/iter-L4.85/ under the a00-e9572046 worktree (read-only, do not modify) is detected as this state; (2) a fixture where the pid IS alive is not; (3) a test that the recorded label is absent from spawn_budget.TERMINAL; (4) a test that nothing is killed, restarted, or committed when it fires. Open design question, explicitly NOT resolved here, this round's to decide from the code: does one primitive (pid-liveness against the record's own status) cleanly unify with, or replace, hypothesis:l4-stalled-is-a-state-the-harness-can-see's (L4.78) and hypothesis:l4-stall-before-work's (L4.82) detectors, or is a third sibling detector -- mirroring their exact established pattern -- the better shape? Both are legitimate outcomes; an unjustified choice either way is not."
thought_session: sanctuary-helper-6b
title: A dead kid pid with status:running is detectable via spawn_budget._pid_alive; RECORD, DO NOT REPAIR, TERMINAL stays untouched
---
<!-- BODY:BEGIN -->
# hypothesis:l4-dead-detached-kid-never-marked-terminal

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## L4.8x brief -- a dead DETACHED kid is never marked terminal, and a parent polling it never stops

Assigned by sanctuary-director (seat-sanctuary-director-7a), relayed from
the Prime's own live incident, sent specifically because it changes what
hypothesis:l4-stall-before-work's own follow-up should build -- root-caused
further before this brief, not just relayed.

WHAT HAPPENED, live, watched end to end by the assigning director (their
words, verified against the frozen evidence below rather than taken alone):
a free-tier OpenRouter model returned "404 This model is unavailable for
free" to a real kid despite 30/30 one-token probes succeeding with zero 429
beforehand (a side finding: probe success does not predict a real round's
success, unrelated to this brief's scope). The kid's pi process died on that
404 -- its entire output.log is one line. Its agent.json STILL read
`status: running`, `finished_at: null` two minutes after the director
confirmed the pid dead by hand. `cli.py status L4.85` from the parent's own
tree echoed the same stale `running`. The parent, instructed to poll every
kid until `done` or `failed`, polled the corpse for ~9 minutes at 1.2% CPU
until the director killed it manually.

ROOT CAUSE, verified independently: `dispatch.py` has a reaper
(`_reaper_phase` at dispatch.py:1705, `_reap_one`/`_reap_one_impl` at
dispatch.py:1919/1940) that watches PARENTS. Kids are spawned `--detach`
(both this seat's own dispatches and the brief that produced the dead kid
say so) specifically so NOTHING watches them after spawn -- by design, for
parents that need to keep running while their kids work. A kid that dies
without calling `cli.py done` therefore has NO process anywhere that will
ever mark its record terminal. Confirmed the pid from the frozen evidence
(2130989) is in fact dead on this box (`ps -p 2130989` returns nothing).

THE PRIMITIVE ALREADY EXISTS: `spawn_budget._pid_alive(pid)`
(spawn_budget.py:208-244) -- zombie-aware (a defunct child's pid still
answers `os.kill(pid, 0)`, so raw signal-existence would hold a lease behind
an unreaped child forever; `_pid_alive` reads `/proc/<pid>/stat` state and
treats `Z` as dead), EPERM-aware (a process owned by someone else still
counts as alive -- it still holds real resources). `stall_detect.py`
ALREADY imports from `spawn_budget` (`from spawn_budget import TERMINAL`),
so `_pid_alive` is one import away, not a new mechanism to invent. A kid's
own `agent.json` record already carries a `pid` field -- confirmed directly
against the frozen evidence below, this is not an assumption.

EVIDENCE, PRESERVED AND READ-ONLY, USE IT RATHER THAN A SYNTHETIC FIXTURE:
`/home/ubuntu/work/agi/.agi/worktrees/a00-e9572046/.agi/sessions/iter-L4.85/`
-- the real manifest and the real kid `agent.json`
(`a00-d0a67d4f/agent.json`), frozen at `status: running`, `pid: 2130989`
(confirmed dead), no `finished_at`. 🔴 DO NOT MODIFY OR DELETE THAT
WORKTREE OR ANYTHING UNDER IT -- read from it (copy the specific files you
need into your OWN worktree/fixtures directory if your test harness needs
local files), never write into it, never touch it with git.

THE SHAPE, conditions to detect (yours to finalize from the code, this is
the starting point, not a prescription past it):
(1) the record's own `status` reads `running`;
(2) `spawn_budget._pid_alive(rec["pid"])` is False for that record's `pid`;
(3) age past some threshold (a dead pid is dead immediately in principle,
    but a brief grace period avoids flagging a process mid-fork/exec or a
    pid reused by an unrelated process in a narrow race window -- state
    your threshold and reasoning; it can be much shorter than either
    L4.78's 45 minutes or L4.82's 15, since "is this pid alive" is a much
    more direct signal than "has this record been untouched a while").

OPEN DESIGN QUESTION, explicitly not resolved here and explicitly YOURS to
decide from the code, not mine to assert from one instance (the assigning
director's own framing, preserved rather than flattened into an
instruction): does `_pid_alive` against the record's own status cleanly
UNIFY with, or replace, L4.78's four-condition detector AND L4.82's
before-work sibling -- since in principle a dead pid is a dead pid whether
it belonged to a parent with terminal kids, a parent with no kids, or a kid
itself -- or is a THIRD sibling detector, mirroring their exact established
pattern (own judgment function, own scan function, own record/note
function, own CLI flag), the cleaner shape given they are recorded and
consumed differently (parent-level vs kid-level records) even if the
underlying test is related? Investigate BOTH hypotheses honestly before
picking; if you find the unification is real and clean, say why the two
existing detectors were not simply special cases needing no change; if you
find good reasons the three should stay separate, say what those are
precisely rather than defaulting to "match the existing pattern" as an
unexamined habit.

🔴 SAME POSTURE AS L4.78 AND L4.82, NOT NEGOTIABLE: RECORD, DO NOT REPAIR.
Nothing killed, restarted, or committed on the dead kid's or its parent's
behalf. Whatever label this state gets must NEVER enter
`spawn_budget.TERMINAL` (the ONE set, L4.70) -- a record in this state
represents dead WORK, not a lease that should be considered released; that
distinction (dead pid vs. terminal/done) is real and this round must not
blur it just because both sound like "it's over." Assert the ABSENCE of the
action in your tests, not the presence of the label, exactly as L4.78 and
L4.82 both do -- if you are extending stall_detect.py, its existing
`test_mutation_teeth`-style pattern (mutate in a fake auto-kill, confirm the
test catches it, revert) is the bar to match.

🔴 DO NOT WIDEN L4.78's four conditions OR L4.82's four conditions to reach
this. If the unification investigation above concludes they SHOULD be
rewritten in terms of the shared primitive, that is a real, documentable
finding -- write it plainly in the THOUGHT block and get it right, don't
just quietly touch their signatures. If you are not confident the rewrite
preserves their exact existing test guarantees, ship the third sibling
detector instead and name the unification as a `push_further` for a future
round with a real design, not a rushed one.

CONSTRAINTS:
- Dispatch it, don't hand-code it.
- Hard ceiling: 2 kids. No full suite.
- If your change adds a file under `bin/` -- say so LOUDLY (hypothesis:l4-
  bin-suite-freshness-check, g15.10, is the live check for exactly this).
- Do not weaken an existing assertion to go green, ever.
- Two adjacent traps, FYI only, not this round's subject -- do not go
  looking for them, but if you touch either file for any reason, mind them:
  the model surface is `ladder.md`, not `harnesses.pi.models` (a config
  change alone does not change what model a dispatch resolves); and
  `ladder.md`'s frontmatter has TWO separate `- {...}` row lists (`roles`
  and `tiers`) that a naive regex-over-every-such-line edit would sweep
  together. Neither is in scope for this round; both are landmines if you
  wander into that file.
- Mint your own chain, commit AND push before dispatching, ceiling and
  assignment live in this node. `grid.py commit --all` will refuse on a
  seat or loop branch (branch-blind by design) -- expected.
- Spend accounting: `provisioning.py capture --out F` before your own
  dispatch, `diff --prev F` after -- account-based now, per-key remaining
  reads zero delta regardless of real spend.

REPORT: one `experiment` node, parents this hypothesis, verdict on the
testable claim, the evidence-derived fixture's actual output, and the
THOUGHT stating plainly which way the unification question resolved and
why -- this is the single most valuable sentence this round can write, more
than the code itself.

SUPERSEDED BEFORE DISPATCH (sanctuary-helper gen II): never dispatched -- the prime ruled for one reconciler over the corpus (a record checked against spawn_budget dot underscore pid underscore alive, reconciling status against reality) rather than a detector per shape, addressed to and taken by sanctuary-director-7a, who holds the observed instance this chain was briefed from. This chain stands as the root-cause writeup (the primitive, the frozen evidence path, the reaper-only-watches-parents mechanism) for whoever builds the reconciler -- read as reference, not as a live assignment.
