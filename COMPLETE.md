# COMPLETE.md — post-loop completion reports

**One section per completed loop, newest first.** `HANDOFF.md` is the live scratchpad of a session; this is the closing record of a loop — what it did and did not close. **Replaced whole at each loop close, appended only when the owner asks** (owner 2026-09-05, reaffirmed 2026-09-11). Every prior report is `grid.py payload build:COMPLETE.md --version N` — L3 (2026-09-06 → 09-09), L2 and L1 live there. Shape and rules: `goal:g1.13`; contents: `mvp:complete-md-the-post-loop-completion-report`; why a director writes it today: `goal:g14`. **Every per-goal claim is grounded in a commit, a node diff or a parent report; a claim that cannot be grounded says so; a decision banked to the owner is a failure of the harness, not the model.**

## Loop L4 — 2026-09-09 → 2026-09-17 — enhanced survival, the figure-eight, the suite-leak saga, the closeout (prime director `belam-S1-L4-VII` … `XXVII`)

Owner GO 2026-09-09 on `doc:l4-plan`; closed by the sequence in `goal:g18.1` (owner 14:1xZ 09-16). Owner verbatim for every ruling: `doc:l4-owner-decisions`. The seat protocol and every measured rule: `goal:g17.1` (its notes are the loop's memory).

## 1. What ran

- **Formation, in order:** enhanced survival (Prime + point + helper + Sanctuary director) → the Keep (`sanctuary-master` ══ `master-sensei`) + town masters with ONE director each, the hybrid figure-eight (owner 09-13 23:32Z) → FULL PAUSE (owner question 09-17 00:5xZ, ruled YES) → sequential mode (owner 01:0xZ) → parallel closeout (owner 04:0xZ, "break rules to close out quicker").
- **Posts:** Prime `belam` gens VII → XXVII (rotate-self, wake 0 / out 1 from SL7.06); point `sanctuary-director` (L4.* and SD.01–SD.13); `sensei-director` (SL1.01–SL7.140); `sanctuary-helper`; `sanctuary-master` gens 1 → 7 (SM.01–SM.100); `master-sensei` (rotation watch + audits; template/config/role-doc only from 09-17 00:4xZ); `thought-master` + `director-thought` (TM.01–TM.25; idle from 09-17 01:0xZ by owner order).
- **Rounds:** L4.01–L4.290 · SL1.01–SL7.140 · SD.01–SD.13 · SM.01–SM.100 · TM.01–TM.25 — every round a pi parent with kids in a round worktree (`season2/loops/<hyp>-<agent>`), reviewed BY NAME through `workflow.py run merge-up-review` on pi (owner 09-16 19:1xZ), merged one GO-by-SHA at a time with a merge-tree gate on HEAD.
- **Harness:** Claude Code remote-control posts (Opus 5 max; the point on Sonnet 5); pi parents + kids on OpenRouter `~deepseek/deepseek-v4-flash-latest` from 09-16 19:4xZ (Sonnet/gpt earlier).
- **Spend:** the original OpenRouter account (topped up 09-11, workspace monthly/weekly caps hit 09-12 = items 109/110, revived by the owner 09-17) and the Doppler `<admin-secret>` account (switched 09-16 21:26Z; $25 → $16.5 at close; ≈ $0.75/h through the closeout, ≈ $1.6/h under full parallel rounds). Floor cell 1.6; both accounts in rotation (owner 09-17 06:4xZ).

## 2. Scoreboard

- **Nodes:** 1828 active at the loop floor → **3198 active / 202 deprecated / 3400 total STAMPED at `66ef15961`** (SM gen 7, 09-17 11:5xZ); never a drop across 60+ merge-ups. Closeout deltas after that stamp: SD.13 `f9f0a332b` (+3 nodes) then the 15 retirements `7b911d6d6` → **3186 active / 217 deprecated / 3403 total, steady** (links 0, goals byte-identical; the next granted window stamps 3403).
- **Suite:** **5386 passed / 0 failed / 16 skipped, 12/12 checks green at `66ef15961`** — the first fully green MAIN suite of the stream came at `676db3111` (5355/0/16, 09-17 07:20Z) once the leak's root cause was closed.
- **Links:** 0 broken (18 retired payloads unresolved, not damage). **Goals:** 180, byte-identical round trip at every verify.
- **Metrics:** `outcome_coverage` 0.068 primary (dilution as hypothesis/experiment nodes enter the denominator, not regression); `evidence_fraction` 0.621 and rising.
- **Landings this closeout gen (27) alone:** SM.77+73+76 (+75 revert) `eb3cc9095` · H2 = SM.79+74 `c84d99efb` · SM.80 suite-green `68d1d4070` · SD.12/R6 `5f9c2bb35` · SM.81+82+83 `90dc3fb50` · D re-cut `e3646ced5` · SM.86 `676db3111` · SL7.139 `fe8703725` · SM.84 `d56b84b90` · SM.87 `9f669459d` · SM.88 `7a87bcc61` · SL7.140 `f0131b9e6` · SM.90 `903718e22` · SM.91 `5df2301a1` · the bundle SM.92+94+95+98+96 `6a6467829` · SM.93 `83c0e7f7d` · SM.100 `66ef15961`.

## 3. Per active goal

- **`goal:g17.1` (the seat protocol):** the formation and every measured rule — ~50 notes this loop; the FULL PAUSE, sequential and parallel-closeout rulings; the rules earned (test the MERGE RESULT never the loop tip; a stamp refuses on a mid-run node commit; a suite window is void the moment a second pytest exists; findings during a closeout are minted always and rounded only into a free slot). Grounded: the note commits `f7f2fbf8e` … `b35cfb283`.
- **`goal:g15` (the Sanctuary, perpetual):** ~100 SM rounds + SL7.*; the leak saga closed — node H (`eb3cc9095`, demoted :60, tests-only), H2 (`c84d99efb`: the suite refuses an in-repo basetemp, the runner mkdtemps under /tmp, every live-root resolver refuses), SM.80 suite-green, SM.82 no detached second suite, SM.88 the cron evidence gate defers under a held suite lock, SM.92 one lease-delete helper, SM.93 a generation cell on every row, SM.94 prepare performs its own clears, SM.98 read-only lock probe, SM.100 tier-gate guard. Root cause measured by SM's falsifier: `dee5b3221` placed the pytest basetemp inside the live `.agi/sessions`, so `git_common_root` resolved every test root to the live checkout. Grounded: the landings above.
- **`goal:g18.1` (the L4 close):** executed as written — queue drained, self-review on the morals, this report, push, prayer.
- **`goal:g11` (one repo):** stood the whole loop; `grid.py commit --all` on `season2/main` only.
- **`goal:g14` / `goal:g1.13`:** this report, written by the Prime once at close.
- **`goal:g13`:** links 0 at every merge-up.
- **`hypothesis:l4-the-stream-goes-live`:** HELD — deferred to the next stream by the owner (09-11 01:4xZ).

## 4. Goals closed

- The L4 plan rounds L4.02–L4.27 (`doc:l4-plan` §5) landed through the point by 09-13; the ad-hoc L4.28+ through L4.290 by 09-16 (`git log --oneline --merges season2/main`).
- No goal is marked `complete` that the record cannot ground; `g15` and `g17.1` are perpetual by design and stay open.

## 5. Completion-failure categories

- **`banked-to-owner`:** (1) three pushed commits carrying private/CGNAT tokens — STAY, rewrite owner-only; (4) `.env OPENROUTER_API_KEY` owner-deleted, a fresh runtime key never named; (8) TypeSafe plugin install; (9) TM.24 egress route on `<keeper-dir>` iron; (11) the thought-town relocation to the GPU box — GO given post-closeout, not yet cut; the orphan loop branch `season2/loops/hypothesis-l4-post-branches-are--a00-ea1066f0` left for the owner branch-cleanup pass (its pending kid node deprecated `9acd28d87`).
- **`hazard-carry-over`:** SM plans (4) encryption town + key seats and (5) town numbering (owner-deferred to the next stream); master-sensei's F23 fact fix (an unchanged where-it-stops slot IS refused as stale) pending its lock-free moment; the successor brief still lacks the line "never run an after_join ack whose `--gen` ≠ row gen + 1" (a fixture after_join was typed into the Prime's pane 09-17 00:57Z); the point's pane froze after 10:0xZ 09-17 in a self-declared pause, answering nudges without reading (SD.13 landed by SM in its place; a typed lift line broke it 11:5xZ); `test_wrapper_tty_hangup_forwards_to_the_child` red under full-suite load stays open (SD.13 kid A demoted :35, next-cut recipe on the node).
- **`late-minting`:** node I (message bodies are files, never argv) — SM.78 struck by the owner 03:0xZ as not a good enough fix morally; the hypothesis stays unrounded. Three code lines from the point's rotation audit minted at the boundary, unrounded.
- **`verification-blindness`:** the suite wrote the live roots from `dee5b3221` (09-13) until 09-17 — fixture rows and acks reached `season2/main` (four `belam ack: gen 3` commits 00:50Z 09-17, three more reverted `d098c42de`), a leaked heal-test rewrote the Prime's row twice and a restore erased thought-master's legitimate dirty row; two suite runs ran concurrently in MAIN because `verification.py --suite` spawned a detached second pytest ~10 min in. Every one is closed by H2/SM.80/SM.82/SM.88; the cost was a day of rotate refusals and a 0.5-day closeout pause.
- **`ceiling-found-by-dying`:** SM.97 died pre-code (superseded by SM.100); SM.85 demoted :40 before landing (the built spawn command exited 2 — shape-only tests missed it).
- **`attribution-void`:** the fixture commits above carry the Prime's name with fixture content; netted at HEAD, not rewritten.
- **`saturation`:** none claimed.

## 6. Findings that are not failures

- Parallel rounds were never the trash source; the in-repo basetemp was. Once closed, five live rounds on 4 cores ran at load 2.8 with reviews inside their 1800 s cap.
- The figure-eight held under load: one director per master, masters briefing and reviewing by name, the Prime accepting from the report plus the bytes — twelve SM landings in one SM generation.
- Narrowing master-sensei to template/config/role-doc (owner 00:4xZ) relieved the audit lane the same hour; its two wake-audit rows now run in the Prime's first turn (`dc3e28758`).
- `quiet` posts (SM.81) + a silent alerts list turn a post's wake into its own schedule; the alerts cell had been stored in a flow-string spelling reached only through a yaml fallback (`0f86eabde`).
- A no-op re-cut honestly reported (SM.90) is a result, and a kid falsifying its sibling's fixture (SM.87) is the method working.
- Account succession works as a two-step (`.env` key + `spawn.credential.workspace_id`); both accounts are in Doppler.

## 7. Minted or changed in response

- **g15 hypotheses landed:** H, H2, D re-cut, E, F, G re-cut, SM.81 quiet posts, SM.82 no detached spawn, SM.83 spawn-row ref-race retry, SM.86 launch-site guard, SM.88 cron gate defers, SM.90 (no-op), SM.91 rc-5 regression test, SM.92 delete-lease, SM.93 generation cell (supersedes the generation-less clause of g15.25), SM.94 prepare performs clears, SM.95 stops wording, SM.98 read-only lock probe, SM.96 the 3-red slice, SM.100 tier-gate guard; SL7.139 harvest demotes a claimed-but-absent deliverable; SL7.140 the deliverable check diffs against the round base; SD.12 `TownAbsentError`; SD.13 (`f9f0a332b`): kid A's bounded wrapper wait DEMOTED :35 by SM's probe (CPython `wait(timeout)` already polls to the deadline; the tty-hangup red under full-suite load stays OPEN on its node) + the 37-row experiment-less survey (`hypothesis:a00-e1933e6a-176c0e`, :85).
- **Retired at close (deprecated, moved, never deleted):** 13 experiment-less g15 hypotheses closed by landed bytes or superseded, plus 2 folded into their siblings — executed by sanctuary-master from the Prime's list (`7b911d6d6`, 11:5xZ 09-17); 22 stay active.
- **Config:** `config:rotations` alerts as a map with thought-master + director-thought silent; two prime first_turn rows (landed-since-stamp, owner-decisions-tail); `config:posts` settings quiet on the thought town; the Prime successor brief's floor text (5.00 → the 1.6 cell + succession).
- **Owner verbatim banked this gen:** nine entries in `doc:l4-owner-decisions` (00:4xZ master-sensei remit · 00:5xZ full pause · 01:0xZ sequential · 03:0xZ SM.78 struck · 03:0xZ relocation idea + assessment · 03:1xZ GO + quiet · 04:0xZ parallel closeout · 06:3xZ–06:4xZ two accounts).
- **Next stream heads (named, unrounded):** the thought-town relocation rounds (box cell, pull cron, ssh/<overlay-if> nudge, after_join off-box); node I re-thought; SM plans (4)+(5); the three rotation-audit code lines; F23 fact fix.
