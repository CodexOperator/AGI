# CARD — director-thought

## SELF-FACTS (gen1 wake-audit, master-sensei 2026-09-16T07:21Z) — handed, not fetched
- Ack grammar is F6, verbatim: `rotate.py ack --post <post> --ref <bare ref> continue|diff [--text -]`. Never grep rotate.py source for it.
- Card path is always `.agi/sessions/quorum/<post>.md` (F26). Never `find`/search for it.
- On any wake, read your own inbox FIRST (call 1) — a nudge names the reason you're awake.
- Never read another seat's rotation record — not your concern; wait for their message instead.
- Check `git rev-parse --verify MERGE_HEAD` before ANY other git command in the shared primary checkout.
- `send.py send --to <seat> "text"` resolves/creates the dm file itself — never guess or `ls`-hunt the filename first.
- **🔴 PRIME RULING, goal:g17.1, gen 22 — MANDATORY in the shared MAIN checkout (not an isolated worktree):** commit ONLY with `git commit -o -m "..." -- <exact paths>`; NEVER run `season.py merge-up` against shared MAIN (use a scratch `git worktree add --detach`, merge+test there, then one fast merge on MAIN); a red merge-up gate runs `git merge --abort` and proves it with `test ! -e .git/MERGE_HEAD`.
- **🔴 REF-PUSH RULE, superseding everything below about two refs (Prime, 2026-09-18 ~02:19Z, measured 16 heads vs 13, relayed by thought-master 02:20Z) — READ THIS BEFORE ANY PUSH:**
  - **NEVER push a post or loop branch to a `refs/heads/*` name on origin.** Your post branch pushes **only** to its mirror: `git push origin local-maxxing/season1/posts/director-thought/main:refs/agi/posts/director-thought`. That is the ONE push command for your own card/node commits — not two anymore, not the old `...:local-maxxing/season1/posts/director-thought/main` refspec, which recreates a head the Prime just deleted.
  - **A finished round branch (`season2/loops/<slug>-<agent>`) is archived, never left or pushed as a head:** `git push origin <round-branch>:refs/agi/archive/<round-branch>`, done by the reviewing director once mur is complete, named in the `[merge-up]` line. Most round branches this session were never even pushed to origin at all (local-only, sibling worktree) — check with `git ls-remote origin refs/heads/<branch>` before assuming an archive step is needed.
  - The two-refs description that used to be here (ordinary branch + mirror, push both) is RETIRED by this rule — do not follow it.
- **`dispatch.py`'s `iter_n`** is validated by `locations.iteration_id`: `<LABEL>.<digits>` (letters-then-digits label, digits only after the dot) or a bare int — `C2R2` refused, `C2.2` normalises to `C2.02`.
- **`write.py create <type> <slug> --set k=v` (repeatable)** is the mint path for a hand-authored node — each `--set` is its own shell-quoted argv token; a long prose value is safe if it never contains a literal apostrophe. `--set` cannot touch THOUGHT; that needs `write.py <id> 'thought <text>'` (or `'set status retired && thought <text>'`, verbs joined by `&&` in one script). `mint_id`/`scaffold_hash` are PROTECTED, never settable.
- **`grid.py commit --all` refuses (exit 2) on a non-master branch** — a node minted/edited from a post worktree gets a normal git commit only.
- **`workflow.py run <name> --args "$(cat file.json)"` is the ONE sanctioned way to run a registered workflow** (never the Claude Code Workflow tool). Launch with the Bash tool's `run_in_background: true` — a stage's `timeout_s` (1800s for merge-up-review) can exceed the Bash tool's own max wait. Poll `.agi/sessions/workflows/<name>.jsonl` or wait for the background-task notification. **Uncertain whether a backgrounded workflow survives a rotation** (new session = new process tree) — if `mur-c2-2`'s task is gone next wake, check `workflow.py status` before assuming the review needs a full re-launch.
- **🔴 STANDING, owner 01:5xZ 09-18 (banked `doc:l5-owner-decisions`): every director runs `merge-up-review` on its OWN landed rounds before reporting up.** One `--args` slice per round: `{key, hypothesis, experiments, files, focus, merge_up, old_tip = merge-base with season2/main, new_tip}`. Fix any real demote in-loop BEFORE delivery, then ONE `[merge-up]` DM to thought-master with tips/merge-base/file-count/run-key/verdicts + the archive-ref name (see REF-PUSH RULE). Thought-master's job shrank to: gate + land on `local-maxxing/season1/main` + one numbers line to the Prime per daily batch.
- **🔴 STANDING, owner via thought-master 02:1xZ 09-18: RESEARCH vs ROUNDS is now a hard split.** RESEARCH (reading docs/papers/troves, ranking candidates) = thought-master's `trove-survey` workflow, never a director-dispatched parent+kids round. ROUNDS (your parents+kids) = APPLYING an already-returned research ranking — measured experiments, code, tooling. **Do not mint or dispatch a docs-hunt/trove-survey-shaped round again** — if a research question comes up, it goes to thought-master to run as trove-survey, and their ranked output becomes your next round.
- **🔴 UNREAD, banked for next wake — thought-master 02:1xZ 09-18: "read both once now and at every wake":** `doc:unified-director-brief` (season2/main, §4 "thought" is this seat) and `doc:lm-director-brief-customizations` (NOT yet on season2/main — thought-master's own town branch `local-maxxing/season1/main`; read with `git show origin/local-maxxing/season1/main:.agi/nodes/doc/lm-director-brief-customizations.md`). **Not read yet this generation** — meter crossed the rotation line before I got to it. Read both FIRST on next wake, before any dispatch.

## 0 STATE (2026-09-18T02:2xZ, gen5 director-thought session, ROTATING — meter crossed 0.47)
Rotating because the meter hook fired at 86%+ of the line while several things were still moving. Read this whole section before doing anything.

- **TM.27** (fetch_parallel.py fix, athena r4): still running, parent `a00-88f9ae5f` + kid `a00-56343823` both alive at last check. Off-box, no A1 footprint. Nothing to do but poll.
- **Q4KV.2** (q4-KV Kid B): still running, parent `a00-c37444ca` + kid `a00-8263e536` both alive. A1-heavy — do not dispatch bitnet.cpp or any other A1-heavy round beside it.
- **C2.2** (metronome toy): FINISHED, verdict disproved:0.8 (conj 1 quantisation + conj 2 energy-tracks-alignment held; conj 3 re-lock failed — flat costlier floor after the flip). Branch `season2/loops/hypothesis-c2-kuramoto-metronome-a00-9c053b3f` tip `2ebebea2d711beeb59cbfa92409ec22403afc181` (**local only, never pushed to origin** — check before assuming an archive step is needed, see REF-PUSH RULE). Kid `experiment:a00-762dba58-d6d914`.
  - **`merge-up-review` launched, run key `mur-c2-2`, background Bash task `b9kb821vg`.** Last checked: review stage still in progress (`[~] review:C2.2`), verify stage not started. **NOT delivered to thought-master — do not send a `[merge-up]` line until this is read and acted on.**
  - **Thought-master gave the reviewer TWO specific probes, verbatim, feed these in whenever the result is read (do not let a generic review skip them):** (a) the measured 3.5e-18 residual is suspiciously perfect — check the kid's read-sites are not fed a tone's phase directly (a trivial copy would quantise exactly, which would be a bug reading as a positive result); (b) the disproof may be an ARTIFACT of flip semantics — the flip is a sign inversion (a π phase shift), and the kid's energy formula `E = mean(1 - cos(phi - psi))` is sign-sensitive (distinguishes a 0-phase lock from a π-phase lock), so a population that re-locks into a stable ANTI-PHASE state would read as "never re-locked" even though it IS locked, just phase-shifted. **If (b) holds: the disproved verdict on C2.2 STANDS AS RECORDED regardless** (thought-master was explicit about this) — it just motivates a natural follow-up round C2.03 (flip as phase jump vs sign inversion; energy signed vs mod-π; same $0 A1-light shape; new hypothesis node under the same chain) rather than a retroactive change to this node.
- **TM.28 (jev/TypeSafe docs hunt): CANCELLED BY THE OWNER mid-session, already handled.** Parent `a00-1333d3b5` + 2 live kids (`a00-2132d69a`, `a00-bb925977`) killed by pid (none had completed — no evidence, no harvest). `hypothesis:lm-jev-docs-hunt` marked `status: retired` with a THOUGHT explaining why, committed (`46f7e5259`), pushed. **New standing split from this cancellation is in SELF-FACTS — read it, it changes what a director is allowed to dispatch.** Nothing further owed on TM.28 itself.
- **bitnet.cpp: still queued, next A1-heavy slot AFTER Q4KV.2 — but reconsider whether it now falls under the new RESEARCH-vs-ROUNDS split before dispatching it.** It was scouted from a research trove (TM.22's synthesis.md rank 2) as a MEASUREMENT (run the binary, measure tok/s) rather than a docs-reading task, which reads more like an "apply a measurement" round than a "hunt docs" round — but given TM.28 was cancelled for crossing this exact line, **do not dispatch bitnet.cpp without either checking with thought-master first or being genuinely confident it is a ROUND (execute + measure) and not RESEARCH (read and rank).**
- Balance not re-checked recently (~$42.9 minus TM.27 $1, C2.2 $1, TM.28 $2 mostly unspent-and-killed, Q4KV.2 $0.50) — recheck before any further dispatch.
- Two new docs to read at every wake — see SELF-FACTS, not done yet this generation.

## 1 PLAN (for gen6, cold)
1. Read `doc:unified-director-brief` + `doc:lm-director-brief-customizations` FIRST (SELF-FACTS has the exact paths) — thought-master asked for this at every wake and it was skipped this generation for time.
2. Read the thought-master DM thread for anything past this card's timestamp.
3. Resolve `mur-c2-2`: read the result (background-task notification, or `.agi/sessions/workflows/merge-up-review.jsonl`, or `workflow.py status`), applying thought-master's two probes above if the reviewer did not already. Fix a real demote in-loop or demote the claim; then ONE `[merge-up]` line to thought-master (tip, merge-base `50b9d2ffcc2fd1a5d3cd1611942f3bd731e522a9`, 3 files, run key, verdict) — and archive the branch per the REF-PUSH RULE (it is local-only right now, so this is a fresh push, not a re-push).
4. Poll TM.27 / Q4KV.2; run the SAME mur pattern on whichever lands next, before reporting either.
5. Do not mint or dispatch anything RESEARCH-shaped (reading/ranking docs or papers) — that is thought-master's `trove-survey` now. Only apply already-ranked results as rounds.
6. No merges — still thought-master's, only the review step is yours.
7. Report shape: `[merge-up]`, `[status]`, `[red]`, `[ack]`, `[owner]` tags to thought-master; `--from director-thought`; no apostrophes in DM or node text.

## 2 TRAPS
- **New this session:** an owner order can directly CANCEL a thought-master order mid-flight ("Cancel the round do the workflow instead") — when it does, stop the live processes by pid immediately (`kill <pid...>`, confirmed via `spawn_budget.py status` before and after), then mark the node, then report. Speed matters more than ceremony here — a live agent is spending real money on cancelled work every second.
- **New this session:** the ref-push convention CHANGED mid-session (Prime measured head clutter and cut it) — a rule you followed correctly three times earlier in this same session (push both refs/heads AND the mirror) became wrong by the fourth. Always read a `[TM]`/`[owner]` message fully before repeating a pattern you have used already this session; do not assume session-start facts are still current at session-end.
- A long registered workflow (`workflow.py run <name>`) needs `run_in_background: true` — its stage timeout can exceed the Bash tool's max wait.
- A hypothesis node's own prose can be internally impossible even when carefully drawn from a source doc (K=8 vs "10-200 of the K tones" this session) — a kid catching and reasonably reinterpreting it is a good outcome to confirm, not a defect.
- `git fetch origin <branch>` on a round's branch can 128 if it was never pushed to origin — it can still be fully present locally (sibling worktree, same repo). Use the local branch name, not `FETCH_HEAD`.
- `dispatch.py`'s `iter_n` must match `<LABEL>.<digits>` or a bare int.
- `grid.py commit --all` refuses on a non-master branch.
- The owner can speak directly into this pane mid-turn, outside `send.py` entirely — treat it as the highest-authority channel, act immediately, relay through normal channels.
- A dispatched round's `--branch` is cut from the SPAWNER's own checked-out branch, which can predate other unmerged rounds on the SAME target node.
- "overdue" on a live agent (pid alive) is expected past the 20-minute manifest timeout — never cut a replacement.
- `dispatch.py` returns almost immediately regardless of `--detach` — a fast return is a SPAWN signal, never completion.
- **`--cap` refuses two ways:** pool-headroom-exceeded (report up) vs workspace-mismatch-403 (report the line). Balance check: `K=$(grep -m1 '^OPENROUTER_PROVISIONING_KEY=' /home/ubuntu/work/agi/.env | cut -d= -f2-) && curl -s -m 20 https://openrouter.ai/api/v1/credits -H "Authorization: Bearer $K"`.
- `write.py`'s `thought` verb REPLACES the whole THOUGHT block, does not append.
- When a round touches zero engine `.py` files, `links.py links` (0 broken) is the merge gate, not a full pytest run.
- **Proving a redaction worked is itself a leak risk** — describe what you checked, never restate the value.
- **🔴 A bare `send.py read director-thought` does NOT show DM threads** — needs `send.py read director-thought --dm <seat> --from director-thought`.
- `--orders` takes a FILE PATH (or `-` for stdin), never an inline string.
- A key existing in MAIN `.env` does NOT mean a dispatched kid's environment has it — TM.25's open finding; check `hypothesis:l4-a-named-env-key-reaches-a-spawned-kid-through-a-config-forward-env-list-read-from-the-main-env-at-spawn-never-a-literal-never-the-dispatcher-environ.md` next wake, may already be the fix.
- `origin/season2/main` moves continuously from other posts/crons — re-sync immediately before every dispatch or push.

## 3 VERIFICATION
- C2.2: verdict disproved, probes in the kid node confirm mechanism not artifact; thought-master's two follow-up probes not yet independently checked (§0).
- TM.28: killed cleanly, confirmed via `spawn_budget.py status` before/after (7 live -> 4 live), node retirement committed and pushed via the mirror ref.
- TM.27 / Q4KV.2: dispatched earlier, confirmed live at every subsequent check; not yet reported done.
- Everything else this session (TM.27/C2.2/Q4KV.2/TM.28 dispatch mechanics, the two node mints, the PARALLELISM RULE, the base-branch handling for TM.27): see prior card versions / git log — not reproduced here.

## 4 WHAT LANDED THIS SESSION (gen5, final)
- TM.27, C2.2, Q4KV.2, TM.28 all dispatched; C2.2 finished (disproved, real result); TM.28 cancelled by the owner mid-flight and cleanly torn down (killed, retired, reported).
- Minted two hypothesis nodes (`c2-kuramoto-metronome-rhythm-bank`, `lm-jev-docs-hunt`) under the towns "TM mints" exception, both documented; one of the two was then retired by owner order the same session.
- Launched the FIRST `merge-up-review` under the new director-runs-mur policy (pending read).
- Learned and recorded three new standing rules this session: PARALLELISM RULE (resource classes), director-runs-mur, RESEARCH-vs-ROUNDS split, plus the ref-push rule change.
- Relayed one direct owner message; corrected one of my own mid-session mistakes (merge ownership).
- Never got to the two new director-brief docs — banked for gen6, first thing.

## 5 🔴 WHERE IT STOPS — exact next action (rotate-out, meter over the line)
```
python3 extensions/agi/bin/rotate.py rotate
```
If it refuses: read the exact refusal line, fix only what it names, rewrite this slot fresh, retry once. A second refusal for an unrelated reason: dm thought-master the exact line, do not guess at flags.

If rotation succeeds and gen6 reads this cold: **read the two brief docs first (SELF-FACTS)**, then the thought-master DM thread, then resolve `mur-c2-2` per §0/§1 above before touching anything else. TM.27 and Q4KV.2 are both still running and need nothing but polling. Do not dispatch a research-shaped round. Do not push to any `refs/heads/*` — mirror ref only.

## 6 BANKED
Nothing owner-only pending beyond what is already reported. Two director-brief docs unread (time, not a decision) — first action next wake, not a question for anyone. Whether bitnet.cpp counts as ROUND or RESEARCH under the new split is a genuine judgment call for gen6 to make carefully or ask thought-master, not something to guess under time pressure the way this generation nearly did with TM.28.
