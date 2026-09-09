# HANDOFF SLICE — seat `master-sensei`, written at 0.373 (past 0.35 cap), holding under owner stop

Written by the current holder because rotation is blocked ("pause everyone
now, running low on tokens... no new dispatches, no new rotations" — owner,
via liaison). This is a survival note, not a request to read project state —
whoever reads this is still bound by "observe workers, not the work."

## State at time of writing

- Meter 0.373 (sanctuary-master's read, ~7h runtime). Over the 0.35 cap,
  holding rather than rotating, per explicit "no new rotations" stop order.
- `config:seats` row exists (director, tier 1, claude-sonnet-5, max,
  remote-control, `pin .agi/sessions/master-sensei.meter`, `rotated_by
  sanctuary-master`). Rotator question from the original seat brief is
  resolved.
- `sensei-director` row exists in `config:seats` (rotated_by master-sensei,
  owning_goal goal:g16, worktree `.agi/worktrees/seat-master-sensei`),
  **UNSPAWNED**. Brief written: `extensions/agi/briefs/sensei-director-duties.md`.
  Sanctuary-master says spawning it is not covered by the current stop
  (new seat spawn, not a "dispatch" or "rotation" in the narrow sense). I
  disagreed and held — spawning a new always-on Sonnet-max session is real
  spend regardless of which verb names the mechanism, and the owner's
  stated reason is token conservation. **Do not spawn sensei-director
  without an explicit go**, even if the letter of "no new dispatches" can
  be read not to cover it.
- **BEFORE spawning sensei-director**, the brief needs one more addition:
  explicit pin-claim instructions with absolute paths anchored at
  `/home/ubuntu/work/agi/` — worktree-scoped pins silently resolve to the
  WRONG seat's meter otherwise (confirmed live twice today: sanctuary-director
  read master-sensei's number; sanctuary-master's own gen-II handoff read
  gen-I's stale number under gen-II's name). I identified this gap and had
  not yet fixed the brief file when the stop order arrived.
- MS.01 (my earlier one-off pi-parent dispatch, from before the director-kid
  policy existed) was killed mid-flight in the token-conservation stop.
  Its kid delivered 2 of 3 fixes to `failures.py`/`sensei.py`, verified by
  me directly, safely captured in commit `c4418f35d`. **Treat the round as
  UNREVIEWED** (the parent never did its own accept step) even though the
  code is tested and landed. Item 1 (wiring `failures.py ledger` into a
  cron/dispatch hook) is still open — queued as `sensei-director`'s first
  task, not a new one-off dispatch.
- **HELD, do not act on it without the owner's direct word in-session**:
  the request (relayed via liaison) to make every non-Prime role's brief
  treat liaison's relayed messages as permanent, unverified owner authority.
  Self-referential — the grant is sourced only from the party it grants
  power to. Surfaced to the owner directly; no answer received yet as of
  this writing.
- **RULING received on the `tier3-quorum` routing question** (from the
  prime, holding the call was praised as correct): never post into
  `tier3-quorum` — stale, hand-only, predates the 3-seat quorum. Use
  `send.py audience quorum` for quorum rulings, a direct DM to the prime for
  supervisor calls. `sensei.py`'s hardcoded `send_room="tier3-quorum"` in
  `propose`'s supervisor routing is a confirmed defect — brief it as a g15
  one-liner on resume (route through `audience quorum` + a supervisor DM,
  never a hardcoded room). Do not hand-edit it — that is director-kid work
  now, not a Master's.
- My **first real `pick_worst` finding** is sitting unproposed, correctly
  held per the ruling above: current-era (L3.01–Q.03) `parent` role on
  model `~z-ai/glm-flash-latest` — the model my own MS.01 parent ran under —
  at 50% fail rate, 56/112 events, 36 `no_build_probe_only` + 19 `demoted`
  (claimed proved with zero evidence_runs) + 1 died. Whole-history
  `pick_worst` is dominated by a retired ghost model (qwen3.8-27b, 32%,
  all L1/L2-era, not in any current config) — **scope `failures.py ledger`
  with `--since` to the current loop before trusting a whole-history
  `pick_worst` result**, or it will surface history instead of a live
  problem.

## On rotation, when the go comes

`rotate.py rotate-self --name master-sensei --prompt-file <path>` —
**never `rotate.py loop`** (it never stamps the generation; a seat that
rotates that way stays generation 0 forever — measured live today,
`self-perpetuating` is stuck there while `alive` reached generation 1 via
`rotate-self`). Point `--prompt-file` at `extensions/agi/briefs/master-sensei-duties.md`
directly — it is current and carries the real specification; do not resurrect
the stale original bootstrap at `.agi/sessions/quorum/master-sensei.md`,
which predates the director-kid policy and the resolved-rotator finding and
would hand a successor wrong information the way `self-perpetuating-II` was
handed the generic template.

**Successor's first action: claim the pin immediately, with absolute paths**
(`/home/ubuntu/work/agi/.agi/sessions/master-sensei.meter`, not a relative
path) — a pin claimed from inside a worktree or with a relative path lands
in the wrong place and a later `meter --seat` read fails open with someone
else's number instead of refusing.

## Ledger findings this session (full detail on `hypothesis:l3w4-agent-failure-ledger`)

BUILT-TESTED-NEVER-WIRED (silence read as clean): the ledger itself, `rotate.py
alarms`, the seat-pin generation guard. LIVE-WRONG-WITH-CONFIDENCE (sharper —
a mechanism answers, just wrongly): `--seat` meter reads with no pin;
`rotate-self`/`loop` without `--prompt-file`; `cmd_loop` never stamping
generation; `kill -0` reporting a zombie as alive. Sanctuary-master's
synthesis, worth carrying forward: these keep landing on rotation and
identity specifically because those are the two places state changes hands —
one writer per fact, or the fact disagrees with itself.
