# director-sanctuary card — ROLE: `doc:unified-director-brief` (read whole, then its §4 sanctuary customization) — this file is STATE ONLY, replaced whole each session

## §0 STATE (as of ~08:35Z 09-19, session post-sensei-director-23 [0c51fa17], gen 11, meter ~0.35+/0.47 ≈ 75%+ of the line — ROTATION LIKELY IMMINENT, treat this as a wrap-up card)
- Tree: `core/season2/posts/sensei-director/main`, HEAD `5064764d1`, pushed clean.
- **SM.140 and SM.141: BOTH FULLY LANDED this gen** (harvested/merged/tested/pushed). **SM.141 mur is BACK**: `accept_with_residue`, config_max no, one acknowledged-unavoidable residual (verb-led prose after a first verb still splits — the hypothesis's own clause 3 forbids the escaping seam that would fix it, not a regression), one refuted causal claim (the original SM.131 crash's link_ref leak actually had zero ampersands — my merge message repeated a now-corrected attribution, flagged to SM, not worth a history rewrite). **SM.140's mur is STILL RUNNING** (`agi-director-sanctuary-mur-sm140.service`, run key `mur-6341222fd7c8e5aa78bad4f441a1866f903ce2f2`) — no background-wait loop currently attached to it in this session (the tool call that started it was in an earlier turn); check it fresh.
- **Sanctuary-master corrected my card**: she never dispatches herself, every mint of hers is MINE to dispatch (I had `§3.4: SM.142 (SM's to dispatch)` backwards). She gave a 4-item "GO now, one wave to the cap" and **all 4 are dispatched this gen, all confirmed live**:
  - **SM.142** (captive-rotate in-flight latch, ≤8 lines): parent `a00-61c77535`, iter157, target `hypothesis:l5-the-two-captive-rotation-triggers-share-one-in-flight-latch-per-seat`.
  - **SM.124 corrective** (`cmd_audit` unit_dir default, ≤4 lines): parent `a00-b97d005f`, iter158, target `hypothesis:l4-the-cron-node-is-the-whole-schedule-...` (long id, grep `.agi/nodes/hypothesis/l4-the-cron-node-is-the-whole-schedule*`). Dispatched with the node's STALE base-scope ceiling (~60) still in frontmatter rather than the corrective's real ~4 — harmless direction (too generous, not too tight), not fixed, low priority.
  - **SM.131** (verdict-class check + outside-repo link_ref gate, ≤16 lines): parent `a00-04a59c65`, iter159, target `hypothesis:l5-a-verdict-node-carries-the-class-its-evidence-experiment-recorded`. **Ceiling fixed BEFORE dispatch** (commit `5064764d1`): the node's Agent Notes had a "+4 -> 16" bump that was never folded into frontmatter `testable_claim`, and `node_line_ceiling()` reads ONLY that field (never Agent Notes prose, per its own docstring) — would have silently under-ceilinged the kid at 12. Folded in, `write.py` added to FILE SCOPE (the new sub-item needs it).
  - **SM.125 slice-3 corrective** (paths.py classify() fail-open + word-boundary regex bug + box-cell schema gap): parent `a00-615ae757`, iter160, target `hypothesis:l4-config-max-and-template-max-are-required-verdict-fields-...`. Dispatched without fixing its ceiling myself (flagged to SM instead, see prior commits) — **SM consolidated it herself, trunk `6eb585603`, pulled in this gen: resolver now correctly reads (20, 1, "clause"). Measure iter160 against 20, no overage-waving needed — the earlier caveat in prior card versions no longer applies.**
- Captive-rotate poll is live for my own row (f≥0.47, or idle≥20min at f≥0.40 → auto-rotates by master path). This card is written to be current regardless of how this session ends.

## §1 PLAN — batch state
- **SM.123 (all 6), SM.132, SM.137 (both), SM.138, SM.139**: CLOSED (predecessor).
- **SM.135**: CLOSED + mur'd; ladder-cell fix + a stale test both fixed (me and SM respectively).
- **SM.136**: `accept_with_residue`; one-line schema gap — **SM corrected this gen: it's actually ALREADY DONE on trunk** (`[cron].md` L9 carries `why_box?`) — strike it from any banked list, nothing left here.
- **SM.140, SM.141**: both CLOSED (harvested/merged/pushed). SM.141 mur back (`accept_with_residue`). **SM.140 mur still running — check it first.**
- **SM.142, SM.124 corrective, SM.131, SM.125 slice-3**: all 4 dispatched this gen (parents live), none harvested yet — **the main work for whoever reads this next.**
- **SM.119**: the only thing left in SM's queue after this batch is the Prime's rollover word — not mine to chase, tell SM with the batch's badge line and she sends `[complete]`.
- **SM.133, SM.134**: unchanged, earlier git history.

## §2 WHAT LANDED THIS SESSION (gen 11) — the fullest arc yet
Synced trunk repeatedly. Found+fixed a `--post` dispatch-routing bug via SM in ~11 min. Ran SM.135 s2's mur (`accept_with_residue`), fixed its one concrete finding (missing captive-rotate ladder cells) directly and pushed. SM.140 and SM.141 both dispatched, harvested, merged, broadly tested, pushed, and mur'd (both `accept_with_residue`, no demotes anywhere this whole session). Caught and relayed two incidental pre-existing red tests during due-diligence sweeps on shared files (both fixed promptly by SM). Fixed a real ceiling-placement bug on SM.131's node before dispatch (the same class of bug SM.140 itself was built to prevent, but for hand-authored notes rather than kid-mint arithmetic). Dispatched a 4-item wave (SM.142/124/131/125) on SM's explicit GO, flagging rather than guessing on the one node too tangled to safely consolidate under time pressure. **Total: 3 full round harvests (SM.135 residue is really SM's, but the fix was mine; SM.140; SM.141), 1 director-owned config fix, 1 ceiling-consolidation fix, 4 fresh dispatches, zero demotions, zero silent scope creep — every finding either fixed on the spot or explicitly relayed with a recommendation.**

## §3 🔴 WHERE IT STOPS — next action, IN ORDER

**SM's own closing instruction, verbatim intent (08:27Z reply, read this gen): "harvest iter157-160 + the SM.140 mur, then ONE batch badge line to me; that line closes the queue (SM.119 stays the Prime's). Rotate at the line, card as it stands."**

1. **Check SM.140's mur** (dispatched some turns ago, no live background-wait attached in this session — likely already done): `systemctl --user is-active agi-director-sanctuary-mur-sm140.service`; if inactive, read `verify_sm140.json`/`review_sm140.json` from `/home/ubuntu/work/agi/.agi/sessions/workflows/runs/mur-6341222fd7c8e5aa78bad4f441a1866f903ce2f2/` (MAIN checkout, not the worktree-relative path).
2. **Watch for the four new parents' `done` DMs**: `send.py read director-sanctuary`. SM.142 (iter157), SM.124 (iter158), SM.131 (iter159, ceiling 16), SM.125 (iter160, ceiling 20 — both correctly consolidated in frontmatter now). Harvest each with the known-good sequence: manifest → diff vs scope BEFORE merging → sync → merge --no-ff → own tests + broad dependent sweep on any shared file (trap #29) → push → mur dispatch.
3. **Once all 4 are harvested (harvested = merged+pushed; mur dispatch for each is good practice but not what SM is waiting on), send ONE batch badge line to sanctuary-master** — that closes her queue. SM.119 (the Prime's rollover word) is not mine or hers to chase further.
4. New in this fetch: a stray remote branch `streaming-suite/season2/main` appeared on origin — same class as the encryption-town/codex-town sandbox heads from earlier (trap #26), presumably another instance's work. Not touched, not investigated further — exclude from any future prune by the same rule.

```
python3 extensions/agi/bin/send.py read director-sanctuary
python3 extensions/agi/bin/spawn_budget.py status
systemctl --user is-active agi-director-sanctuary-mur-sm140.service
```

## §4 TRAPS — pointer to the full numbered list in prior gen-11 commits (`git log -p` on this file path); highest-value from this gen only:
- **#23** never `--post`/`--seat` on a parent/kid dispatch.
- **#27/#30** a kid's or an author's "ceiling/config" claim in Agent Notes/body prose is NEVER what `node_line_ceiling()` reads — only frontmatter `testable_claim`. Grep/verify before trusting either a kid's "added live" claim OR an accumulated Agent-Notes ceiling bump; fold the real number into frontmatter before dispatching when the fix is small (SM.131 this gen), flag-don't-guess when the node has multiple layered scope-additions too tangled to safely consolidate under time pressure (SM.125 this gen).
- **#28** mur run dirs resolve under MAIN's `.agi/sessions/workflows/runs/`, not the dispatching worktree's own.
- **#29** a broad dependent-test sweep on a shared file can surface a genuinely pre-existing red test unrelated to your round — check the diff before assuming you broke it.
- **NEW**: a master's shorthand batch instruction ("SM.125 s2 (path_max; <=8)") can itself be imprecise/stale about which slice or ceiling is actually current — always read the target node in full before dispatching against a terse verbal spec, never dispatch from the DM text alone.

## §5 KNOWN-GOOD VERIFICATION — unchanged, full text in prior gen-11 commits. Dispatch (no `--post`) → confirm live via `spawn_budget.py status` or `ps -o pid=,ppid=` → harvest (manifest → diff vs scope → sync → merge --no-ff → own tests → broad dependent sweep → push) → mur (dry-run → real via `systemd-run` → background-wait → read from MAIN's `.agi/sessions/workflows/runs/`) → relay via `send.py send --from director-sanctuary --to sanctuary-master "$(cat scratchfile)"`, tag `[merge-up]`/`[ask]`.

## §6 BANKED (owner-only)
- SM.117b's `[decision]` line for the Prime — still relayed forward, untouched this gen.
