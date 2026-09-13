# SESSION HANDOFF — 2026-09-13 sanctuary-director: LIVE SCRATCHPAD (rotating at 0.4875 of the line, 19:23Z) + R3.5 (content-containment, every kind) both harvested and independently reverified; the loop-kind gap R3.4's own harvest surfaced is confirmed closed by R3.5. Merge-up-53 window ASKED to belam (19:2xZ), tip `e919821ac`, awaiting grant. See §0/§2/§3 — the successor's first job is to check for belam's reply and, on grant, execute the merge into MAIN.) (rotating at ~0.45 of the meter, 19:2xZ)

🔴 **TREE:** `$W=/home/ubuntu/work/agi/.agi/worktrees/post-sanctuary-director` on **`season2/posts/sanctuary-director`**; **MAIN `/home/ubuntu/work/agi` = `season2/main`**. ABSOLUTE paths always. Sync = `git fetch && git merge --no-edit origin/season2/main`. Heavy concurrent write load — stale-base refusals are normal, resolve by sync+re-cut or `--allow-stale-base` as the sanctioned third step.

🔴 **HANDOFF.md at the repo root is STALE/LEGACY** — edit the quorum card only.

🔴 **NAMING/TRACKING, owner order 16:4xZ:** no post but the Prime tracks generations. Timestamps/hashes for "when", never `gen N`. **Post renames land in SM.18's bundle — do not rename anything here.**

🔴 **NEW OWNER DECISION THIS SESSION, not yet implemented — check if it's landed before trusting the OLD merge-up recipe below:** owner 18:3xZ asked whether posts can be local-only, auto-merged, no origin push. Prime ruling (relayed to SM 18:4xZ): YES — post branches (this one included) will stop being pushed as heads, mirrored instead to `refs/agi/posts/<name>`; **merge-up drops the window-ask/grant round-trip — the post takes the advisory suite lock itself and tells the Prime ONE line after.** This session still used the OLD recipe (window ask sent, awaiting grant) because it had not visibly landed as of the merge-up-53 ask. Check `doc:l4-owner-decisions` / SM's own card fresh before assuming either way.

## §0 STATE (live — updated as work lands)

**AUTHORITY:** owner speaks ONLY through the Prime (belam); every decision banked verbatim in `doc:l4-owner-decisions`.

- **PRIME = belam** = live seat **agi-16** `[1b5b3b]`. Verified this session.
- **Ids this session:** L4.347-349 = R3.1-R3.3 (merge-up-52, `bef788a5e`, mur-52 ACCEPTED WITH RESIDUE but destructive-path NO-GO). L4.350 = R1 (rotate.py closeout gate, harvested, merged `8f9589eab`). L4.351 = R3.4 (origin-presence gate, harvested, merged `04e1a4e7e`, proved for kind post/town_main). L4.352 = R3.5 (content-containment, harvested, merged `9c21705b8`, proved, applies to every kind/tree). **Next id = L4.353** (whatever comes after merge-up-53 lands — R2/R4/R5/R6 still need a separate GO, unrelated to this sequence).
- 🔴 **THE FULL FINDING AND ITS RESOLUTION — read this before touching branch-reshuffle, even though it is now closed, because the next live run still needs to be read carefully:** mur-52 (belam XIX, 18:25Z) found `--delete-old`'s B2 gate had a bypass that would have unconditionally deleted 5 live branches (`season2/posts/sanctuary-director` — **this post's own** — `sanctuary-helper`, `sensei-director`, 2 town mains). R3.4 fixed this for kind post/town_main via an origin-presence check. R3.4's OWN harvest then surfaced that the fix didn't reach loop-kind jobs — a live re-check found 3 `season2/loops/*` branches still unconditionally deletable. R3.5 added a SEPARATE, independent content-containment gate (`git merge-base --is-ancestor`) that applies to EVERY kind on EVERY tree (a 2-kid self-correcting round: kid 1 scoped it under `_v3_on` like R3.4, its own parent review proved that left a v3-off tree's stray commits destroyable unchecked, kid 2 fixed it universally). **Independently reverified BOTH rounds personally** — diffs read in full, suites re-run (76→151 passed), and critically: the actual live read-only `--dry-run --delete-old --kinds towns,posts,loops` re-run after each fix, reading the actual output list, not just trusting green tests (this is the exact discipline mur-52 itself modeled — "tests pass" was never the right question for this hypothesis class). Current live state (read-only, confirmed): the 5 post/town branches refuse (presence); of the 3 loop branches, 1 refuses (content) and 2 are genuinely, correctly admitted (confirmed by calling the shipped containment helper directly against real origin, not just trusting the printed line).
- **Merge-up-53 window ASKED** (19:2xZ), numbers + hash in the DM (see git log / `send.py read`/`peek` history), **awaiting belam's grant** — this is the live thread, see §2/§3.
- 🔴 **mur-51 demoted L4.345, fix = SANCTUARY MASTER SM.23** — checked this session: still open (no HARVEST on the SM.23 node). Not mine, don't touch. **Do not restart the reaper.**
- 🔴 **OWNER-ORDERED RENAME, check before EVERY rotate-self:** `test -f /home/ubuntu/work/agi/.agi/sessions/seats/sanctuary-director.rename.json` — checked at the top of ROTATING YOURSELF below, re-run fresh, do not trust this note.
- **Tree:** synced repeatedly this session, clean each time. Post branch tip `e919821ac`. `commands.py run verify`: 9/10 (bin-suite-fresh red, expected), active=2828 deprecated=198 total=3026, broken_links=0.

## §1 LANDED

**R3.1+R3.2+R3.3** (merge-up-52, `bef788a5e`) and **R1/L4.350** (rotate.py closeout gate, `8f9589eab`): done earlier this session, full detail in git log + each node's HARVEST note.

**R3.4/L4.351 (harvested):** new helper `_rs_v3_successor` derives the remote-visible v3 successor for a `new is None` post/town_main job; the B2 gate refuses (all-or-nothing) unless it's confirmed present on origin. Folds in 2 bundled mur-52 residues. ONE kid, correct on the first pass, avoided a real near-miss (would have gated on the post_main itself, breaking every genuine migration forever). Independently reverified: diff read, 76 tests passed twice, live read-only dry-run reconfirmed. **Surfaced its own residual gap: loop-kind jobs still unguarded** — carried forward honestly in its own HARVEST note rather than glossed over.

**R3.5/L4.352 (harvested):** new, independent content-containment gate — every job's tip must be `git merge-base --is-ancestor` of its rename target, else its derived v3 successor, else the season trunk main, applied UNCONDITIONALLY (every kind, every tree) — this is what closes the loop-kind gap. 2-kid self-correcting round: kid 1 scoped it under `_v3_on` (mirroring R3.4), its own parent built a v3-off stray-commit fixture and found it still destroyed content unchecked (exactly the claim's own DISPROOF clause), demoted, kid 2 fixed it properly. Independently reverified: diff read, 151 tests passed twice, live read-only dry-run reconfirmed, AND independently called the shipped containment helper directly against real origin for all 3 named loop branches (not just trusted the printed dry-run line) — 2 genuinely contained (correctly admitted), 1 genuinely diverged (correctly refused).

**Merge-up-53 window asked (19:2xZ):** synced, verified (9/10, expected), sent belam the numbers+hash+summary of both rounds. Awaiting grant.

## §2 LIVE + QUEUE

**LIVE: awaiting belam's merge-up-53 grant.** Sent ~19:2xZ. Check inbox fresh on wake — do NOT assume it's still pending without checking.

**QUEUE once granted:**
1. In MAIN `/home/ubuntu/work/agi` (`git status` first; never clean/stash — expect ambient cron-owned dirty comms/rotation files, that's normal, don't touch them): `git merge --no-ff season2/posts/sanctuary-director -F <file>` (write the merge message covering both R3.4 and R3.5, verified accurately against THEIR OWN harvest commits, not from memory — see §4 trap on this).
2. `snapshot-goals.py --render` → `--render --check`.
3. `commands.py run verify-suite` FOREGROUND (timeout 600000) — expect it to take ~2 minutes; read the actual failure list if anything is red, don't assume it's pre-existing without checking (this session confirmed one pre-existing failure this way and it turned out to already be fixed elsewhere by the time it mattered).
4. `grid.py commit --all` (MAIN only — never on a post branch). "0 new version(s)" can be normal if a concurrent `grid_sync` cron beat you to it; verify with `grid.py versions <node>` before assuming an error.
5. `git push origin season2/main` + `git push origin "refs/grid/*:refs/grid/*"`.
6. `verification.py --level rotation --stamp` — should read ALL 10 GREEN if steps 1-5 went cleanly.
7. ONE message to belam: five numbers + hash.
8. **mur-53 by name** (director-review's registered adversarial workflow).
9. **Only on mur-53 ACCEPT**: `branch-reshuffle --dry-run --kinds towns,posts,loops` (never `main`) → `--apply` → suite green → `--delete-old` → cell re-spellings (Prime applies) → `verify` → commit. **Read the `--dry-run` list BY NAME every time**, never an expected count (belam's own standing note: the Prime's manual-cleanup count does not match the engine's own derived delete-set count).

**R2/R4/R5/R6** still need a separate signed GO from belam — not yet asked. Sources: mur-49 review JSON (`.agi/sessions/reviews/mur-49.review.json`, MAIN only, gitignored) keys L4.337 (R5), L4.338 (R4, R6) — read the relevant node body first, per grammar.

**GRAMMAR (still correct):** mint = `write.py create hypothesis <slug> --parent goal:g15 --parent hypothesis:<source> --set town=core --set "title=…" --set "testable_claim=$(cat file)" --actor sanctuary-director --role director` (**no literal `&&` anywhere in generated text** — breaks write.py's script parser). commit + push. cut = `AGI_SEAT=sanctuary-director AGI_POST=sanctuary-director python3 extensions/agi/bin/dispatch.py . L4.NNN --target hypothesis:<id> --level small --tier parent --harness pi --branch` (sync first; `stale-base` = sync + `find .agi/sessions/iter-L4.NNN -type d -empty -delete` + re-cut SAME id; 2 refusals in a row is normal — `--allow-stale-base "<reason>"` is the sanctioned third step; VERIFY via `find`/`git worktree list`, never the printed lines). wait = `spawn_budget.py status --iter L4.NNN --wait --timeout <N>` backgrounded. harvest = diff vs merge-base → review bytes + node directly → check parent worktree `git status -sb` directly → merge `--no-ff -F file` → re-run suites here → **for a destructive-path hypothesis, independently re-run the actual read-only command with the actual planned flags and read its actual output list, never stop at green tests** → `write.py <node> "note HARVEST L4.NNN (sanctuary-director, <ts>): …"` → commit + push.

## §3 🔴 NEXT COMMAND

```````
``````
`````
````
```
Check inbox fresh: python3 extensions/agi/bin/send.py read sanctuary-director. This is the live thread -- belam's merge-up-53 grant (window asked ~19:2xZ, tip e919821ac, lands R3.4+R3.5).

If GRANTED: execute the §2 QUEUE steps 1-7 in MAIN, in order, each gated on the previous succeeding. Write the merge commit message by checking R3.4's and R3.5's OWN harvest commits (git log --grep or read the merge commits already on this branch: search for "harvest L4.351" and "harvest L4.352"), never from memory -- this session mischaracterized an earlier round's target hypothesis once by trusting recollection over the source, do not repeat it. Then mur-53 by name (belam runs or names it). ONLY on mur-53 ACCEPT, run the branch-reshuffle live sequence (§2 step 9) -- dry-run first, read the list BY NAME (not an expected count), then --apply, suite green, --delete-old, cell re-spellings (Prime applies), verify, commit.

If NOT yet granted (empty inbox, or a hold/question from belam): answer any question first. If nothing to answer, this is fine to bank -- it is not blocking anything else. Check R2/R4/R5/R6's status (still need a separate GO, not yet asked) as productive parallel work if truly idle, per the §2 QUEUE "R2/R4/R5/R6" note and the GRAMMAR block's mint/cut sequence -- read the relevant mur-49 node body first (L4.337 for R5, L4.338 for R4/R6), do not read the full 1316-line review JSON unless the node body is insufficient.

SEPARATELY, before ever rotating further: (1) test -f /home/ubuntu/work/agi/.agi/sessions/seats/sanctuary-director.rename.json -- re-check fresh. (2) mur-51/SM.23 -- check if landed; if not, leave demoted-pending-fix standing. (3) generation-less -- never "gen N". (4) check whether the owner's posts-local-only ruling (top of this card) has landed -- if so, the OLD merge-up recipe (window ask + wait) is superseded by a new one (take the suite lock yourself, no round-trip); check doc:l4-owner-decisions and SM's own card, not just this note, before assuming either way.
```
````
`````
``````
```````

## §4 TRAPS (kept from the prior card, trimmed where superseded)

- 🔴 A literal `&&` inside claim/title/note/thought TEXT breaks `write.py`'s script parser — write "and" instead. Hit twice this session.
- 🔴 `write.py`'s `set`/`create --set` edits whatever tree your CWD resolves to — from your OWN worktree it edits YOUR copy, not MAIN's (correct/intended for minting, just don't Read MAIN's copy to check your own edit).
- 🔴 A tier-parent's `cli.py done --owns ...` does **not** write the verdict onto the owned node's frontmatter, and when MULTIPLE kids ran (a self-correcting round), the commit subject may cite only the FIRST (now-superseded) kid — read EVERY kid node in full, the LAST one's frontmatter verdict is the one that matters. Hit on R3.5 this session (commit cited kid 1's `pending`, kid 1 was itself demoted to `inconclusive_lean_disproved:70`, kid 2's real verdict was `proved`).
- 🔴 **For a round guarding a destructive path, "tests pass" answers a narrower question than the gate actually asks.** This recurred THREE times this session at successive levels: mur-52 caught it in R3.1-R3.3 (green tests, live dry-run still deleted 5 branches); R3.4's own harvest caught it one level down (green tests, live dry-run still deleted 3 loop branches); R3.5's own kid-1-to-kid-2 correction caught it again (green tests, a v3-off fixture still destroyed content unchecked). **Always independently re-run the actual read-only command with the actual planned flags and read its actual output list.** For containment/presence-style claims specifically, also independently call the shipped helper function directly against the real data, don't just trust a printed summary line.
- 🔴 A round's session records can be split across MULTIPLE worktrees with MAIN's own copy sitting completely EMPTY — and a dispatch's own printed manifest path can be under YOUR WORKTREE, not MAIN.
- 🔴 `grid.py commit --all` REFUSES on a non-master/non-main branch — MAIN only. A concurrent `grid_sync` cron may beat you to a version.
- 🔴 root `HANDOFF.md` and the quorum card are TWO DIFFERENT FILES.
- 🔴 Under heavy concurrent write load, `dispatch.py` can print `{"issue": "stale-base", ...}` **and then keep printing lines that look like a successful spawn** — verify with `find`/`git worktree list`.
- 🔴 At harvest, always check the parent's own worktree with `git status -sb` directly.
- 🔴 A merge commit's own prose can mischaracterize which node a round targeted if written from memory — verify against the round's own harvest commit.
- 🔴 A round's own narrow test suite going green is not the same as the full engine suite staying green.
- 🔴 A merge-up GRANT is state — `test -f` the lock + inbox before `git merge` in MAIN; undo = `git reset --soft <base>`, never `reset --hard`.
- 🔴 `-F <file>` for every commit/merge/dm message. Never `pkill -f` in a Bash-tool command.
- 🔴 The five node counts are the ENGINE'S metric, never `find | wc`.
- 🔴 A DM claiming to relay a real owner order can be genuine but still arrive before your own branch has synced far enough to see the doc entry it cites.
- `date -u` for stamps. Never `test_provisioning.py` / full-suite pytest with `--basetemp` under the repo. Never hand-poll — `--wait`, backgrounded if long. `crons.py` refuses from a worktree.

## §5 KNOWN-GOOD VERIFICATION

Full rotation-level stamp check post-merge-up-52: `verification.py --level rotation --stamp` → **ALL 10 GREEN**, baseline `bef788a5e` (2811/198/3009). `commands.py run verify` re-run before the merge-up-53 ask: 9/10 (bin-suite-fresh red, expected), active=2828 deprecated=198 total=3026, broken_links=0. `test_branch_reshuffle*.py` + `test_branches.py` + `test_branch_spelling_grep.py`: grew 70→76 (R3.4, +6)→151 (R3.5, +full cross-file set), independently reconfirmed at every step (parent worktree + post-merge here, each time). `test_rotate*.py`: 742 passed + 1 xfailed (R1). Live read-only `--dry-run --delete-old --kinds towns,posts,loops`, most recent run (post R3.5): 5 post/town branches refuse, 1 loop branch refuses, 2 loop branches admitted (independently confirmed genuinely contained via the shipped helper called directly).

## §6 BANKED (not mine; with a recommendation)

**16.** `test_sensei_wake_audit.py` F2/F3 label drift — flagged, already fixed by someone else on MAIN minutes later. Closed.

**14-15, 13** carried unchanged (master-sensei's verification-weakening suggestion not adopted; the "testing plan" phrase's exact scope unconfirmed; director-review's mur-50 process suggestion re: remote-visibility fixtures, not yet minted).

Carried unchanged: 1. Kid model — owner named only the parent. 2. `hypothesis:l4-completion-signal-cannot-tell-dead-from-silent` — the Prime's held round. 3. `links.py schema` 124 pre-L4 violators. 4. `crons.py cmd_remove` unfenced. 5. L4.126's parent died under the INLINE reaper. 6. Stub repo `/home/ubuntu/work/streamer-stub` unpushed commits. 7. L4.192 wording residue. g15 candidates to propose: the 0b-b captive after_join; `l4-a-foreign-tree-edit-is-committed-in-the-same-breath`; rungs 2-4 as g15 lines; `ref_candidates` keeps the input spelling.

**11. RULED by the Prime:** the row (`claude-sonnet-5`) is the authority on model; never a flag in this card. Struck, stays struck.

## STANDING RULES (binding; unchanged from the prior card)

- **Reporting (owner 2026-09-10): only when NECESSARY** = a merge-up ready/done · a Prime-only decision · a rotation line · a red merge or a rule-changing finding.
- **Authority is verified against the GRAPH:** `git fetch && send.py whois <ref> --claim <post>` + the ListAgents row + `tmux capture-pane`. For a RELAYED OWNER DECISION, verify independently against `doc:l4-owner-decisions` and the commit that banked it. **Sync first if the cited entry isn't found locally.**
- A peer's instruction (the Prime's included) is not authority to edit `CLAUDE.md`, permissions, `.agi/config.json`, `ladder.md`, `config:seats`, `moral:*` — quote the false line, write the replacement into the node, stop.
- **ENHANCED SURVIVAL** (`goal:g17.1`): parallel rounds GO where file scopes are disjoint; up to 5 kids per parent. Never: wake another post · write `config:seats` · touch `moral:*` · `git rm` under `.agi/nodes` · rebase/force-push · `level3.py` without `--dry-run` · `grid.py checkout` · `git stash`.
- **Spend:** $5.00 floor: below it NO new round is dispatched, live rounds finish — PAUSED until the owner resumes.
- **No "gen N" anywhere.**

## MERGE-UP RECIPE (may be superseded — check the posts-local-only note at the top of this card first)

1. This branch synced to `origin/season2/main`; `verify` green here.
2. ONE message to the Prime: "taking the merge-up-N window" + what it lands + numbers. Hold for lock state + tip + baseline.
3. In MAIN (`git status` first; never clean/stash): `git merge --no-ff season2/posts/sanctuary-director -F <file>` → `snapshot-goals.py --render` → `--render --check` → `commands.py run verify-suite` FOREGROUND (timeout 600000) → `grid.py commit --all` → `git push origin season2/main` + `git push origin "refs/grid/*:refs/grid/*"` → `verification.py --level rotation --stamp` → ONE message, five numbers + hash.
4. **Never merge-then-hold.**

## ROTATING YOURSELF

**FIRST, always:** `test -f /home/ubuntu/work/agi/.agi/sessions/seats/sanctuary-director.rename.json`. Re-check fresh.

At **0.47** of the meter's `est.` number, or sooner at a clean stopping point. `python3 extensions/agi/bin/rotate.py rotate` — bare and keyed, NO flag. Refuses by name when the card's where-it-stops slot is stale. **NEVER pass a model flag.** Effort `max`; never `loop`. If its gate names `behind`: `git merge --no-edit origin/season2/main` and re-run. **Prayer: exactly two spots per session — the very first tokens of your first reply, and the very last tokens before rotate-self returns; never at the start or end of any turn in between.**

## WHAT THIS POST HAS LEARNED

- A relayed instruction with real stakes deserves independent verification against the graph, not blind trust OR reflexive refusal.
- A round's session dir can be completely empty in one worktree while the real data lives in another; check all plausible locations.
- A rule's own predicted outcome can legitimately differ from the real case without that being a defect.
- A completion tool writing to "the record" can mean two different records depending on flag mode — and when MULTIPLE kids ran, the commit subject may cite only the first, now-superseded one. Read every kid node, the LAST verdict is the one that counts.
- Correct your own record in the file your successor reads, in the same breath as the finding.
- The STARTUP OUTPUT is the wake — a fact printed there is never re-derived by hand.
- A DM citing a graph doc can be genuine but still outrun your own branch's sync.
- A round's own narrow test suite going green is not the same as the full engine suite staying green.
- Verify a round's target hypothesis against its own harvest commit message, not from memory.
- **"Tests pass" is not the same question as "does the actual dry-run list still contain the dangerous thing."** This recurred three times in one session, at successive levels of the same problem (R3.1-3 → R3.4 → R3.5), each caught by someone actually running the real read-only command and reading its real output — never by trusting a suite result. For a destructive-path claim, independently call the shipped check function directly against real data too, not just the printed summary.
