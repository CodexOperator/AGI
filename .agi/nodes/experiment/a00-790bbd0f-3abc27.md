---
id: experiment:a00-790bbd0f-3abc27
mint_id: cfc2d58e29c24ba997754e19ade598c7
type: experiment
parents:
  - hypothesis:l4-startup-is-one-script-or-a-driven-prompt
next_edges: []
confidence: 0.8
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-790bbd0f-3abc27
loop: hypothesis:l4-startup-is-one-script-or-a-driven-prompt@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 7154a9a26456ee83
season: 2
title: "startup first_turn: allowlisted pre-spawn telemetry composed into the successor first turn"
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-790bbd0f-3abc27

## Experiment

Implemented the first_turn half of the `startup` hypothesis in
`extensions/agi/bin/rotate.py`: a template-driven `startup.first_turn` runner
that rotate-self executes BEFORE spawn, with the successor's telemetry
composed into a `## STARTUP OUTPUT` block appended to its first input turn
(after head + brief). The CONFIG half (`.geometry/rotations.md` templates)
was already landed by the Prime; this round wrote the code that consumes it.

Scope delivered (one tight slice, per the owner's acceptance test):
1. Loader — reads `templates.<role>.startup` from `config:rotations` via the
   existing `_load_templates` path (frontmatter).
2. Placeholder resolver over exactly the 11 keys `{seat} {succ_ref}
   {succ_name} {succ_transcript} {pin_ref} {gen} {prime_ref} {worktree}
   {repo} {tmux_session} {pred_pids}`; an unknown `{key}` is REFUSED by name
   (`ValueError`), never silently left in.
3. Allowlist — `_producing_refusal` judges each `;`-/`|`-PRODUCING segment
   against the executable allowlist (engine `python3 <...>.py`, read-only
   `git status/log/diff`, read-only `tmux list-*/display-message`, `ps`,
   `curl` to the openrouter credits endpoint); stdio filters after `|`
   (head/sed/grep/...) are allowed. An off-allowlist verb is REFUSED and its
   LABEL named — never run.
4. Per-command timeout (`first_turn_timeout_s`, default 60), one command at
   a time, before spawn.
5. Per-command byte cap (`byte_cap`, default 4000) — output truncated and
   marked.
6. `## STARTUP OUTPUT (rotate-self ran these for you; you ran nothing)`
   block composed from the per-command results (label/status/output each),
   appended to the successor prompt via `spawn_window extra=` (head + brief
   + block).
7. Wired into `cmd_rotate_self` as step (2.5) — between the own-window rename
   and the spawn — building values from the seat row + seats registry
   (prime_ref from the prime_director row), and the dry-run prints the
   resolved first_turn list with every placeholder filled and runs nothing.

## Evidence

Test-first — `extensions/agi/tests/test_rotate_startup.py` (8 tests, all
pass) on a hermetic fixture (no graph, no real spawn, no tmux):
(a) `## STARTUP OUTPUT` composition, (b) per-command timeout caught+named,
(c) byte-cap truncation + "output truncated to N bytes",
(d) allowlist refusal names the label (`rm -rf /` → `[danger] REFUSED`),
(e) unknown placeholder refused by name (`{bogus}`), (f) dry-run runs
nothing (probe marker file absent on dry-run, present on live).

Full suite green on the changed tree: `pytest extensions/agi/tests/
-k "test_"` → **2718 passed, 1 skipped** (rotate files: 138 passed).

Real-tree acceptance (requirement 7), `rotate.py rotate-self --name
sanctuary-director --dry-run` from this checkout, ran NOTHING and printed the
resolved first_turn list with every placeholder filled:
```
(2.5) startup first_turn (resolved, NOTHING run):
    [rotation-record] dry-run: ... rotate.py whois --seat sanctuary-director --record latest
    [seat-row] dry-run: ... send.py whois  --claim sanctuary-director
    [prime-authority] dry-run: ... send.py whois 7cff1a --claim belam
    [git-state] dry-run: git -C <repo> status -sb | head -5; git -C <repo> status -sb | head -3
    [inbox] dry-run: ... send.py read sanctuary-director
    [live-spawns] dry-run: ... spawn_budget.py status; ... provisioning.py status
    [write-verbs] dry-run: ... write.py -h | sed -n 1,40p
(4) read back successor reply — pending ack channel -> ...
```
`prime_ref` resolves 7cff1a from the prime_director seats row. `succ_ref` is
empty pre-spawn (`{succ_ref}` for `seat-row` resolves to the seam value,
which is empty in a dry-run) — the successor ref is only decidable post-join,
an honest open item for the live path.

## Agent Notes
startup first_turn runner in rotate.py: placeholder resolver (11 keys, unknown refused), allowlist (_producing_refusal, off-verb label refused), per-command timeout+bytecap, ## STARTUP OUTPUT compose, wired pre-spawn in cmd_rotate_self(2.5), dry-run prints resolved list. 8 fixture tests + real-tree dry-run verified; full suite 2718 passed.

PARENT VERIFIED (a00-2f2d0784, L4.125): re-ran test_rotate_startup.py (8 passed) and the real-tree rotate-self --dry-run (7 commands resolved, nothing executed). Verdict kept inconclusive_lean_proved:80 — PROVED-BY (2) demonstrated on fixtures, not yet on a live rotation.

DIRECTOR REVIEW AT HARVEST (sanctuary-director gen X, L4.125 = 0b, 04:59Z). Branch loop/hypothesis-l4-startup-is-one-scr-a00-2f2d0784@s2, done d5cc78cad, 10 files (rotate.py +738, hooks/cc-session-start.next.sh +291 = the COPY, test_rotate_next/startup/tail, test_session_start_bootstrap), FOUR kids: a00-790bbd0f :80 first_turn composition; a00-0f40a201 lean bootstrap facts + staleness (config facts write blocked for a kid -- correct, the prime writes .geometry); a00-51d8da5f :75 bootstrap-block reader + the .next hook copy; a00-30f8c08e :80 rotate.py next driven walk. LANDED, verified on the real tree from the round worktree: rotate-self --dry-run --name sanctuary-director prints (2.5) startup first_turn: 7 commands resolved (rotation-record, seat-row, prime-authority -> whois 7cff1a --claim belam, git-state, inbox, live-spawns, write-verbs), composes the ## STARTUP OUTPUT block into the successor prompt and runs NOTHING (no gen11 window); tests 473/1 in the round tree, 365/1 on the merged seat (rotate*, session_start*, send, heal*, bin_help_smoke). NOT LANDED -- the owner 03:0xZ refinement (verbatim on doc:l4-owner-decisions, ruled into this round): (i) after_join PERFORMED BY THE SERVICE on startup.after_join_delay_s as ONE flow (join, pin claim on the derived transcript, ack continue, model_confirm after the ack, reap proof) delivered as the successor SECOND input, CAPTIVE where a decision remains -- in the bytes after_join exists only inside the DRIVEN walk (rotate.py next :3951-3967); grep for delay/captive in rotate.py = 0; heal.py untouched; (ii) join-only placeholders ({succ_ref}) resolve EMPTY in first_turn -- the [seat-row] command ran as send.py whois  --claim sanctuary-director (kid 4 saw it and left it) -- a first_turn entry with a join-only placeholder must be refused/deferred by label, never run with an empty arg; (iii) the successor briefs (quorum/*.md, prime-director-successor.md) still carry every first-do-X line. Verdicts stand as the kids wrote them; the ROUND claim is PARTIAL: 0b-b fix-only owes (i)-(iii), serial on rotate.py behind the seventh 0a. Bootstrap count for the next rotation on these bytes: first_turn output arrives in turn one (7 commands the successor no longer runs); the pin + ack stay manual until (i) lands.
