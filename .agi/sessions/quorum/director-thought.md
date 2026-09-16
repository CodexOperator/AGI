# CARD — director-thought

## SELF-FACTS (gen1 wake-audit, master-sensei 2026-09-16T07:21Z) — handed, not fetched
- Ack grammar is F6, verbatim: `rotate.py ack --post <post> --ref <bare ref> continue|diff [--text -]`. Never grep rotate.py source for it.
- Card path is always `.agi/sessions/quorum/<post>.md` (F26). Never `find`/search for it.
- On any wake, read your own inbox FIRST (call 1) — a nudge names the reason you're awake.
- Never read another seat's rotation record (e.g. your master's) — not your concern; wait for their message instead.
- Check `git rev-parse --verify MERGE_HEAD` before ANY other git command in the shared primary checkout.
- `send.py send --to <seat> "text"` resolves/creates the dm file itself — never guess or `ls`-hunt the filename first; `config:posts` (`.agi/nodes/.geometry/posts.md`) is the authority on whether a seat name is real.
- **🔴 PRIME RULING, goal:g17.1, gen 22, 2026-09-16 ~11:0x-11:2xZ — MANDATORY for every post in the shared MAIN checkout (`/home/ubuntu/work/agi`, not an isolated worktree), effective now:**
  1. **Commit ONLY with `git commit -o -m "..." -- <exact paths>`** (`-m` BEFORE `--`), never a bare `git commit`/`git commit -a`. It REFUSES during a merge ("cannot do a partial commit during a merge") — **that refusal is the alarm, never a reason to drop `-o`.** (Root cause of the TM.06 round-1 bypass: master-sensei's own bare card-commit silently completed a merge it never started, because it had no `-o` to refuse with.)
  2. **🔴 `season.py merge-up` is NEVER run against the shared MAIN checkout, full stop** (thought-master's direct 11:19Z order, after two of my calls collided with other seats' granted windows and had to be aborted by hand). It holds `MERGE_HEAD` + runs the suite IN the shared checkout for minutes at a time. Replacement procedure, proven clean on TM.08 and TM.09 this session: `git worktree add --detach <scratch-path> <current season2/main sha>` (a genuinely separate directory — can't reuse the branch name since it's checked out in the primary checkout), `git merge --no-ff <branch>` there, run tests there, and ONLY once green go back to the shared checkout for ONE fast `git merge --no-ff <branch>` (auto-commits immediately if no conflicts — no separate commit step, no suite runs there). `git rev-parse --verify MERGE_HEAD` must exit 128 (absent) before AND after every touch of MAIN. If in doubt, touch nothing and ask thought-master.
  3. A merge-up gate that goes red must run `git merge --abort` **and prove it** with `test ! -e .git/MERGE_HEAD` before reporting anything.

## 0 STATE (2026-09-16, ~12:3xZ, gen1 director-thought session — meter near/at the rotation line, may hand off any moment)
Ten TM orders processed under thought-master (TM.02 through TM.11). **Nine CLOSED, one live (TM.11).**

- **Rotation record:** gen n/a, window @391, pid 27026, model_confirm ok.
- **Node counts:** active 3002, deprecated 200.
- **Tree:** branch season2/main, behind season2/main 0, unpushed 0.
- **Meter:** 0.500884 · role director · model claude-sonnet-5.
- **Account:** total=$182.00 used=$173.25 remaining=$8.75
## 1 PLAN
- next: **wait for TM.11's completion dm** (`a00-912fc962`). Once it lands and is audited/merged: dispatch a small TM.12 for the still-open ip_decimal-encoding leak + spend.md citation fix (§0's TM.09 bullet has the exact detail) — nothing else is queued behind that.
- audit shape, unchanged: diff vs merge-base (never a moved tip), no self-authored parent node, kid claims + parent's own negative probes hold from bytes read directly, file scope against the node's FILE SCOPE field, IP-grep the whole diff (+ any named gitignored files directly, they never show in a tracked diff). THEN merge using the throwaway-worktree procedure in SELF-FACTS #2. After any merge, confirm both `git rev-parse --verify MERGE_HEAD` (must exit 128) and `git merge-base --is-ancestor <tip-or-merge-commit> HEAD` (must be true) before reporting anything landed.
- if the suite is ever genuinely red on HEAD (confirmed by an independent run, not just a gate's own report): do NOT hand-write the fix. Revert (`git revert --no-commit <sha>`, verify the specific failing test green with the revert staged, `git commit -o -m "..." -- <the reverted paths>`, re-run), then report full file:line causal evidence to thought-master (tag `[red]`) and belam (tag `[red]`, shorter).
- report shape per landed round: one line to thought-master always; belam gets a separate `[complete]`-tagged dm too. A regression/revert gets `[red]` to both instead.
- loadavg / ORDER 6: condition already met — still blocked purely on TM's fresh account read.
- still true throughout: dispatching whatever TM mints, or a follow-up round against a node TM already minted (including a small residue round I scope myself, like TM.10), is in-scope any time; minting a brand-new hypothesis node myself, or hand-writing engine code, never is (owner 04e5070c9). A `write.py thought` correction on an existing node (like striking a stale clause) IS in-scope when the owning seat (thought-master) explicitly asks for it that way.

## 2 TRAPS
- **A parent that dies outright (`status=failed`, pid gone — not "overdue") can still have left real, complete, uncommitted work in its own worktree.** Check `git status` in `.agi/worktrees/<parent-id>/` before assuming a dead parent means a wasted round; `cli.py status <iter>` run from INSIDE that worktree can show a different, more complete picture than from the primary checkout (a `--branch`-isolated parent's kids register to the worktree's own nested `.agi/sessions/`). Read the kid's node directly, verify evidence against raw artifact files, harvest it yourself with a `write.py thought` explaining the circumstance.
- **Next time a parent dies before `done` and I salvage its kid's work, write the parent-tier `probes:` line myself** (a numbered-conjunct list, like a normal parent review would) — TM.07's salvage skipped this since there was no parent left to write it, and thought-master flagged the gap as residue. A `write.py` edit can add this after the fact if it's ever missed again.
- ALWAYS grep a round's whole diff for IP-shaped strings before merging when the node's ceiling bans IPs. When a ceiling extends the ban to local/gitignored files, a tracked-diff grep alone is NOT sufficient — check the named files directly on disk; they're invisible to `git diff` by construction.
- **A node's own CLAIM/TESTS body prose can go stale** after a round fails (frontmatter amended, body prose still describing the old approach — TM.06 round 2) or after a hypothesis's actual round-2 shape diverges from what TESTS originally narrated (this GPU node). Read ALL of a node before dispatching a follow-up round; if frontmatter/THOUGHT and body prose disagree, the more recent, specific source wins — say so explicitly in `--orders`. To fix a stale clause permanently, a fresh `write.py thought` (not a hand edit to CLAIM/TESTS) is the sanctioned way, per thought-master directly.
- `links.py schema` is a dry report (pre-existing missing-field nodes) — not a clean-suite signal.
- `dispatch.py` returns almost immediately regardless of `--detach` — a fast return is a SPAWN signal, never completion.
- write.py's `thought` verb REPLACES the whole `<!-- THOUGHT:BEGIN -->` block, it does not append — if the existing THOUGHT holds content still worth keeping (e.g. original minting rationale), compose the new text to carry it forward rather than just writing the delta in isolation.
- A full `python3 -m pytest extensions/agi/tests/ -q` run on this box normally takes ~8-9 min (500s+); it can time out even at 590s when load spikes (this session hit loadavg 6-8 once every seat started using throwaway worktrees at once). When a full run isn't practical, the directly-relevant test files run alone (confirmed against the actual merge result, not just a branch tip) is adequate evidence — say so plainly rather than skipping verification silently.
- Leaving the primary checkout to work inside a worktree (`cd .agi/worktrees/<id>/`) and back is fine — the environment tracks cwd, not a special ritual; a plain `cd /home/ubuntu/work/agi` returns cleanly.

## 3 VERIFICATION
- TM.02 on main: `git log --oneline --ancestry-path 27f9c7883..season2/main | tail -5`
- TM.03 on main: `git log --oneline --ancestry-path ad8df57cc..season2/main | tail -5`
- TM.04 on main: `git log --oneline --ancestry-path 173e5c560..season2/main | tail -5`
- TM.05 on main: merge commit `b3d11375b`
- TM.06 round 1 regression + revert: revert commit `0edbb3128`; reverted kid nodes recoverable via `grid.py payload experiment:a00-0d0ebadb-568acc --version 1` (and `a00-587bb508-8e68ff`).
- TM.06 round 2 / TM.08 on main: merge commit `dfef305bc`.
- TM.07 on main: merge commit `62bab19c7`; salvage commit `d50628e8e`.
- TM.09 on main: merge commit `71bfe2f94`.
- GPU hypothesis node's stale-clause correction: commit `f1bf4f393`.
- TM.10 on main: merge commit `aaeddd2b0`.
- TM.11 (once landed): `git merge-base --is-ancestor <branch-tip> HEAD && echo landed`.

## 4 (closed — kept empty on purpose; next 🔴, if any, goes here)

## 5 🔴 WHERE THIS STOPS — exact next command
```
TM.11 (a00-912fc962) reported done -- harvest accepted=1 demoted=0 failed=0, kid experiment:a00-c1b9dfec-62a1aa, branch season2/loops/hypothesis-l4-needs-credential-i-a00-912fc962, tip 400f8eda66630cf5920cefb0b91f6f54a83500db -- NOT YET AUDITED OR MERGED (session rotated before starting). This round DOES change real code (the credential-none pop consolidated into all three adapters' child_env, per thought-master's TM.06-round-3 spec in card SS0) -- do not skip the full suite in the throwaway worktree the way TM.09/TM.10 could. First commands for whoever picks this up: read the kid node in full, diff vs merge-base (git merge-base season2/main season2/loops/hypothesis-l4-needs-credential-i-a00-912fc962), confirm file scope = the three adapters' child_env + dispatch.py's two consolidated pop sites + tests + this node + one kid node, IP-grep the diff, then the throwaway-worktree merge+test procedure from card SELF-FACTS (season.py merge-up is BANNED in the shared checkout), verify MERGE_HEAD absent + ancestry true independently, report to thought-master (full account) and belam ([complete]). After TM.11 lands: dispatch TM.12 for the still-open ip_decimal-encoding leak in 2 named gitignored files + spend.md citation-by-blob-sha fix (thought-master's ~12:11Z dm has the exact ask) -- thought-master said no new GPU round until TM.11 lands, which it now has. ORDER 6 stays held on thought-master's own fresh account word specifically (not just any fresh read -- a driven-handoff account read already exists in SS0 at $8.76 remaining, but TM wanted to be the one to say go).
```
No other action is pending beyond TM.11 (live) and the queued-behind-it TM.12 (ip_decimal residue). This is a genuine wait-for-nudge state, not a blocked one.
## 6 BANKED
Nothing owner-only pending. Every open item above is thought-master/belam-directed and already actioned or fully specified for the next step — no ambiguity needs the owner.
