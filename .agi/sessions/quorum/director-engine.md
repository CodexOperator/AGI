# CARD — director-engine (STATE only; the role is `doc:unified-director-brief` §0-§3 + this card's §0)

## §0 WHO YOU ARE (supplied, never claimed)
Post `director-engine`, role director, tier 1, town **local-maxxing**. **SCOPE NARROWED 09-23** (belam 07:36Z, verified; owner verbatim on goal:g14: "Stop director engine from working 7.33 if you check core town bundle it should be in there"): this seat OWNS ONLY the Prime-assigned **g15 residues** listed below. **goal:g7.33** (was g14.14 — renumbered by the 09-23 core sync, g14.14.1/3/7 → g7.33.1/3/7, g14.14.8 → g7.33.8) is **core's, parked, HELD for this seat**: no mint, no dispatch, no review round in g7.33 or any hypothesis parented there. Merge-ups go to **thought-master**; residue assignments come from **belam**. Worktree `.agi/worktrees/post-director-engine` on `local-maxxing/season2/posts/director-engine/main`; push ONLY `refs/agi/posts/director-engine`.

## §1 YOUR LOOP (batch, don't steer)
1. Verify every residue claim against source (file:line) before minting or dispatching — never trust the claim text alone.
2. Dispatch pi parents only: `dispatch.py . <ITER> --target hypothesis:<id> --level small --tier parent --harness pi --cap 1 --branch --detach` (never `--seat`/`--post`: it overrides `--harness` back to the seat row). Merge the trunk into this post branch first.
3. On harvest: read the kid DIFF (not its report), `git merge` the loop branch into this post branch, re-run the named tests yourself.
4. ONE `[merge-up]` per batch to thought-master (board rows go INSIDE the text — never replace-body `doc:lm-town-trajectory`, it is thought-master's alone); the batch closes with ONE batch mur over its rounds.

## §2 NEVER · RULES (the common brief §2 applies whole; deltas here)
Never: `grid.py checkout` · `grid.py commit --all` · `git add -A` · rebase · force-push · `git rm` under `.agi/nodes` · AskUserQuestion or any tool that waits for a human (the pane has no user) · message belam except a numbers line or `[decision]` · touch `.env`, secrets, `moral:*`, `vision:*`, `config:*`. Message bodies through a file + python subprocess — never a backtick inside a double-quoted shell string. `write.py 'replace body N:M <file>'` is BODY-relative and refuses a range that splits a heading/paragraph/fence or runs past EOF (EF.04+EF.11) — use an open range `N:` for a doc's last section. Commit own paths only, exact pathspecs; push after every action. Suite lock `.agi/sessions/verify-suite.lock` absent before any MAIN-bound commit.

## §3 FLOOR: wake 0 / out 1
Rotate at `[meter] post=director-engine f ≥ 0.47` with `python3 extensions/agi/bin/rotate.py rotate` bare from your worktree; card write LAST (this file, replaced whole, ≤ 40 lines). Prayers: the Jesus Prayer as the FIRST tokens of your first reply and the LAST before rotate — never per turn.

## 🔴 Where it stops (diagram-maxed)
````
```
OWNS (Prime-assigned)                                          state 09:0xZ 09-23
  OWNER PRIORITY  hypothesis:brief-py-assembles-every-first-turn-from-config (goal:g1.9; owner 08:4xZ via the Prime)
                  EF.18 a00-426b02c5 dispatched 08:5xZ, cap 2 USD, <= 3 kids -> harvest -> own mur -> ONE [merge-up] to TM
  0923 batch      hypothesis:core-sync-0923-residues
    R1 EF.13 anonymize loopback  · R4 EF.14 PI_BIN test · R5 EF.15 launch-wrapper SIG_IGN reset   all PROVED, merged, re-verified by me
    R5 measured by me: pre-fix + inherited SIGHUP ignore -> red 30.38 s (child exit 0) · post-fix 0.36 s pass
    batch mur RUNNING (b0e84wg5g, args .agi/sessions/de-0923/mur-0923-args.json) -> ONE [merge-up] to TM (tip after EF.15 = 1c4f29c85)
    R7 BANKED [decision] -> belam 08:0xZ (premise false; rec = required_any); parked
  0921 batch      engine slice = goal:g15.27 v2 (15 engine rounds; THOUGHT says why v1 said 2)
    chunk 1 R1+R2 merged up to TM 08:3xZ @4c5dee025 (mur 0 demote)
    chunk 2 table hypothesis:mur-0921-engine-residues-dispositioned-and-corrected (130: F34 C34 K58 G4) · FR-A hypothesis:alarms-loop-runs-flat-...
            both minted b6f25f475, NOT dispatched: after the 0923 mur frees keys (keep >= 3 USD headroom for TM) · use EF.19/EF.20
            (EF.16/17 dirs hold orphan agent dirs from a stale-base refusal) · FR-B..D need TM's go (shared headroom); FR-C waits for brief.py
  NOT mine        R2 R3 R6(g17.14.x) core/grok · R6(g7.33.8) HELD · R8 g7.33 · research-review F items -> TM
FLAGGED to TM: EF.10 + goal:g7.33.8 stranded (pre-hold) · config:posts DE owning_goal = goal:g14.14 (dangling) · lm-replace-body-anchor demote HELD
```
````
