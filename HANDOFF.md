# SESSION HANDOFF — 2026-09-02b: COMPLETE (10 iterations, 107–116)

Standing bootstrap lives in [QUICKSTART.md](QUICKSTART.md). This file is one
session only and the next director replaces it wholesale.

## §0 State block

| | baseline | now |
|---|---|---|
| active nodes | 893 | **922** |
| deprecated | 7 | 7 |
| **`outcome_coverage` (primary)** | 0.266 | **0.300** |
| `evidence_fraction` | 0.250 | **0.328** |
| `decisive_evidence_fraction` | 0.955 | **0.972** |
| `broken_links` (new) | — | **0** |
| `mvp_count` | 33 | **39** |
| `thought_coverage` | 0.099 | **0.127** |
| unevidenced decisive | 1 | 1 |
| goals active / horizon / complete | 12 / 62 / 34 | **13** / 62 / 34 |
| goals | 110 | **111** |
| tests | 1250 | **1335** |
| unpushed | 0 | **0** |

**Every primary and secondary metric moved up.** The primary *fell* for the
first five iterations (0.266 → 0.256) because hypotheses were minted and mvps
were not; iter-112 closed that honestly and it ended at 0.300.

**Runtime:** pi is configured — `deepseek/deepseek-v4-flash` kids under
`qwen/qwen3.8-27b` parents. **The director acted as parent throughout and no pi
agent was dispatched**: every iteration this session was engine-primitive work,
where a cheap kid would have been the wrong instrument.

### 🔴 Crons are still OFF — push by hand

`.geometry/crons.md` has `crons_live: false`, off since the `goal:g11`
migration freeze. Everything below is pushed, but nothing pushes automatically.

```bash
git -C /home/ubuntu/work/agi push origin master
```

### 🔵 The provisioning key is live

`OPENROUTER_PROVISIONING_KEY` is set (73 chars) and per-spawn credentials are
armed: `spawn.parallel: 5`, `spawn.max_live: 25`, `$0.25` and 60 min per key.
**0 engine-minted keys outstanding.**

```bash
python3 extensions/agi/bin/provisioning.py status
python3 extensions/agi/bin/provisioning.py reap     # dry; --yes to act
```

## §1 The plan, and what it came to

All ten ran. Two were reordered mid-session; the reasons are in §2.

- [x] **Phase 0** — `goal:g13`'s three open questions, answered by the owner.
- [x] **107** — `goal:g4.8` item 3: a concurrency bound that survives a tier.
- [x] **108** — `goal:g1.11`: a minted, capped, expiring key per spawn.
- [x] **109 + 109b** — `goal:g13`'s write half; and a self-correction.
- [x] **110** — `goal:s31`: a scaffold is born valid.
- [x] **111** — `goal:g1.10`: `.geometry/commands.md`.
- [x] **112** — five mvps, from what five verdicts said they had *not* proved.
- [x] **113** — both hand-rolled writers routed through the gate.
- [x] **114** — `goal:g13.1`'s verb layer.
- [x] **115** — `goal:g4.7`'s `restart()`, wired.
- [x] **116** — the modal-shell mvp; this handoff.

## §2 What landed

### `goal:g4.8` — the bound is structural (107)

`spawn.parallel` bounds one invocation's slots and **never bounded
grandchildren**: a parent gets kids by running `dispatch.py` again, which reads
its own copy of the same number. A parent carefully *enforcing* the number does
not help either — `experiment:a00-5f927203-8a66a2` disproved that. **A limit
expressed as a number cannot be global.**

`bin/spawn_budget.py` puts it in shared state: one lease per live agent, taken
under a lock at the spawn site, **reclaimed by liveness** so `kill -9` cannot
shrink the budget permanently.

| cap | admitted | peak live |
|---|---|---|
| 1 / 3 / 5 | 2 / 5 / 10 | **1 / 3 / 5** |
| 999 (control = pre-fix) | 25 | **24** |

Peak *equals* cap every time — on the boundary, not passing by starvation.

### `goal:g1.11` — one minted key per spawn (108)

Three independent limits, **because a cleanup step is not a safety property**:
a credit cap, a TTL, and revocation when the lease is reclaimed. The credential
hangs on `spawn_budget`'s lease, so reclaiming the slot and revoking the key
are **one event**.

Measured live: mint **0.760s** mean, 10 concurrent in **0.919s** wall, 20
revocations in 2.781s, 30/30 ok, 0 leaked. That settled the banked granularity
question — **per spawn**: batching is a cost optimisation, the cost is 0.06% of
the timeout it gates, and per-slot cannot answer *which agent*.

🔴 **Trap, asserted in a live test:** `expires_in_seconds` is accepted with a
`201` and **silently ignored**, producing a key with no TTL from a call that
looked like it worked. Only `expires_at` is honoured.

🔴 **Near miss:** the owner's own long-lived key is named `agi`. `reap_orphans`
matches `agi-` **with the hyphen**. One character separated a cleanup routine
from revoking the key the project runs on.

### `goal:g13` — the write half (109, 113)

**Edit-in-place had no routine.** Every fix and retag in this project's history
was a hand edit — `goal:g13.1`'s "completely stray and untraceable commit".
`node_writer.update_node` is that routine, and it **cannot destroy the authored
`THOUGHT`** (`goal:g2.10` made impossible rather than discouraged).

`bin/write.py` is the link layer: `link_ref` generalises `payload_ref`, `self`
means the body is its own data, a single read of a missing link **raises**, a
bulk scan returns a **typed sentinel** counted in `broken_links`.

iter-113 routed both hand-rolled writers through it, which needed one semantic
fix first: **the gate judges the delta, not the state.** Rejecting on state
would have refused verdicts on the 115 already-invalid nodes — and a gate that
punishes the wrong write teaches callers to pass `validate=False`, which is how
a gate stops existing.

`goal:g7` outranks `goal:g13`: a refused gated write **falls back loudly**
rather than dropping a wire.

```
links: 927 resolved, 0 broken · declared 0 · payload_ref 220 · defaulted 707
```

🔵 **`declared: 0` — the corpus is not migrated.** A node body is still a
payload, not a marker.

### `goal:s31` — scaffolds are born valid (110)

Two correct rules composed into a contradiction: the scaffold owns frontmatter,
the kid is told not to touch it, so a required field the writer didn't supply
**could not be added by anyone doing their job as briefed**.

The goal's three candidate shapes were never alternatives — each handles a
different class of field. **Seed** what the engine derives (`title` from the
slug, never a placeholder), **lift** what only the kid holds out of the body at
completion, **report** what neither can supply. Safe because `scaffold_hash`
hashes the **body** — asserted, not assumed.

🔴 **A census bug I made and caught:** the first count said 203 invalid nodes,
led by `goal: seeds x86`. The check was `not fm.get(k)`, and `seeds: []` is
what a goal with no seeds correctly carries. **Corrected: 115.** It is
`goal:s31`'s own thesis committed by its implementer — a hand-rolled predicate
agreeing with the schema by convention instead of reading it.

### `goal:g1.10` — commands declared, not memorised (111)

`.geometry/commands.md` + `[command]` schema + `bin/commands.py`, rendered into
`INJECTION.md` so **every agent is handed the commands**.

**The claim proved itself on first contact:** `grid-commit` was declared as
`grid.py --all`; the real command is `grid.py commit --all`. That string sat
*correct* in `HANDOFF.md` and `CLAUDE.md` for months. **Prose is read and
believed; a command table is run.**

🔵 The four prose copies are **not** deleted — this made a fifth that happens
to be executable. `mvp:prose-derives-from-the-command-node` is the fix.

### Five mvps, from five verdicts' own limits (112)

`outcome_coverage` fell every iteration for five iterations. The fix was *not*
minting mvps for work already done — `[mvp].md` is explicit that an mvp is
**design pointing forward**, and the corpus said so before anyone decided it
(`source_files` 0/26, `tests_pass` 0/26). So the honest mvps are the gaps each
verdict named in its own "what is NOT proved" section. **primary 0.256 →
0.295**, because five chains closed where they were actually open.

### `goal:g13.1` — the verb layer (114)

Stated as a falsifiable claim about **build order**, with a disproof condition:
a verb that only makes sense with a cursor. Five verbs later, none appeared —
**the negative result is the proof**. `bin/edit.py` has **no file write**
(AST-checked, not grepped). `thought_session` gets its first writer, reserved
since `goal:g2.7` with nothing writing it.

### `goal:g4.7` — restart wired (115)

`adapter.restart()` was defined and never called, which is the honest reason
`verdict:a00-fd5d74ab-a74f6c` sat at 55. Now called, behind a decision table
whose **order is the design**: `completion.is_complete` is checked **before**
any restart, because kids die after their node lands and respawning one would
hand a second agent the same scaffolded node. That ordering came from a field
note, not from reasoning about the code.

**The old verdict keeps its 55.** It describes what iteration 104 measured.

## §3 🔴 Where it stopped, and the exact next command

Everything is committed, grid-versioned, pushed. **1335 tests green, 922 active
nodes, 0 broken links, 0 outstanding minted keys, 0 unpushed commits.**

**The next session's work is already in the graph as six open mvps** — put
there deliberately, so it survives this file being replaced:

| mvp | what it discharges |
|---|---|
| `a-live-loop-on-minted-keys` | **run first** — no pi agent has ever used a minted key |
| `the-bound-under-real-agents` | `goal:g4.8` clauses 1, 3, 4, at cap 25 |
| `the-modal-shell-over-the-verbs` | `goal:g13.1`'s other half |
| `the-corpus-becomes-schema-valid` | the 115, minus 62 that need `goal:g1.9` |
| `prose-derives-from-the-command-node` | delete the four copies for real |
| `route-every-writer-through-update-node` | mostly done in 113; falsifier not run |

**Start with the two live runs, in that order and not together** — both are at
an untested concurrency and share a novel credential path, so running them
together means a failure cannot be attributed to either.

```bash
cd /home/ubuntu/work/agi
python3 extensions/agi/bin/commands.py list          # what the graph declares
python3 extensions/agi/bin/provisioning.py status    # armed, 0 outstanding
python3 extensions/agi/bin/dispatch.py "$PWD" 117 --tier parent --target goal:g13 --level small
```

## §4 Traps hit this session

1. 🔴 **A `grep` proved the wrong thing and I published the claim.** An
   experiment node said *"`grep` confirms `type == goal` does not appear"*. It
   returns 1 — the phrase is in the docstring stating the invariant. The
   invariant held; the evidence did not. Replaced with an `ast` test and
   **corrected in a follow-up commit rather than quietly repaired.**
2. **A background `pytest` reported exit 0 with an empty output file while the
   suite was red.** Re-run in the foreground before trusting a green.
3. **Backticks in `git commit -m` are command substitution.** They ate a word
   from the iter-107 message. Use `-F -` with a heredoc.
4. 🔴 **`sys.modules` reassignment makes "the same import" two objects.**
   `test_completion.py` and `test_evidence_gate.py` load modules by path and
   reassign `sys.modules[name]`, so a test patching its own `node_writer` name
   and a module calling through its own reference diverged. Visible **only in
   full-suite order** — both narrower runs were green. **Patch the object the
   caller actually calls through.**
5. **A leaked monkeypatch.** Assigning on a module instead of via `monkeypatch`
   leaks a stub into every later test.
6. **Clean-fixture tests miss real-node defects.** `edit.py` met the live corpus
   one iteration after being built and had two: a fixed-arity script parser,
   and a note that added a second `## Agent Notes` heading to a node that
   already had one.
7. **A hand-rolled emptiness check is not the schema's.** `not fm.get(k)` calls
   `seeds: []` missing; the registry's rule is `None` or an empty *string*.

## §5 Known-good verification sequence

Declared in the graph now — `commands.py list` prints it, in order:

```bash
python3 extensions/agi/bin/commands.py run smoke        # node count must NOT drop from 922
python3 extensions/agi/bin/commands.py run tests        # 1335 passing
python3 extensions/agi/bin/commands.py run goals-check
python3 extensions/agi/bin/commands.py run viewport-verify
python3 extensions/agi/bin/commands.py run links        # 927 resolved, 0 broken
python3 extensions/agi/bin/commands.py run grid-commit
```

## §6 🔵 BANKED — decisions deliberately not made

1. 🔴 **Backfill the 115 schema-invalid nodes?** `write.py schema --fix` has
   only run dry. Would fill **`title` x86** and **`testable_claim` x5**; would
   leave 62 absent rather than invent them. Reversible, probably right, ~91
   nodes of churn nobody asked for. One command either way.
2. **Should the viewport replace `INJECTION.md`'s renderer?** Carried from last
   session. Would delete 4 of 5 render paths — the real prize — but it changes
   what every kid is handed.
3. **`goals_active` is 13 against a cap of 9.** The open question is *how* it
   should count: `g3`, `g5`, `g7` are arguably permanent residents rather than
   in-flight work.
4. ~~`goal:g1.11`'s batching granularity~~ — **SETTLED**: per spawn.

## §7 Standing hazards

- **Neither live run has happened.** The bound, the credentials and the reaper
  are all proved against sleeping interpreters and fake adapters. A `SIGSTOP`ped
  agent is alive to `os.kill(pid, 0)` and holds its slot indefinitely — correct,
  and still a surprise at cap 25.
- **25 concurrent pi agents is well past the ~4 where rate-limit deaths were
  measured.** The credit cap is what makes trying it a bounded decision.
- **A parent's REPORT is not its artefact.** Check the node file.
- **A fix with no test is an assertion.**
