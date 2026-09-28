---
id: hypothesis:pass2-engine-rows-corrected-in-place
mint_id: 4128ecb4bc034d83a328311ff35114d6
type: hypothesis
parents:
  - goal:g15.28.2
next_edges: []
confidence: 0.75
edited_by: director-engine
scaffold_hash: fd5c3b0c6a2dfd4b
season: 2
testable_claim: "Every C row of the PASS 2 table on director-engine's side (the grok-bot nodes: the stub-versus-real-respawn claims, the bin cell claim, the duplicate build id) is applied in place through write.py after re-checking the bytes -- a grid version whose THOUGHT names this node, never a second node, no verdict / lean / confidence field changed -- and the rows on held (goal:g7.33 subtree) and thought-master's nodes are left untouched and listed."
title: "the PASS 2 node corrections on director-engine's rounds applied in place (assigned: director-engine)"
town: core
---
# hypothesis:pass2-engine-rows-corrected-in-place

# hypothesis:pass2-engine-rows-corrected-in-place

## Hypothesis

```
leaf      goal:g15.28.2 -- the C rows on director-engine's side of the PASS 2 batch, applied IN PLACE (a grid version with a THOUGHT, never a
          second node), each re-checked against the bytes; the rows on held (goal:g7.33 subtree) and thought-master's nodes are NOT touched
```

## Disposition table (sorted 09-23 16:3xZ, read-only, against the post branch @feb043a63e)

# PASS 2 (09-23) residues -> dispositions, 21 rounds (director-engine, for hypothesis:pass2-0923-residue-batch)

```
source   /data/work/agi/.agi/sessions/workflows/runs/mur-chunk{1,2,3,4b,4c,4d}of4/{review,verify}_<round>.json (trunk @ebae4adde -> season2/main @4c35ff60f)
checked  every item against THIS worktree @feb043a63e (local-maxxing/season2/posts/director-engine/main), read-only. Where an item is live state,
         also read-only live evidence: git for-each-ref, `git ls-remote` counts, the grid_sync crontab line + its cron log, one
         `derive-commands.py --check --all` (writes nothing). No pytest, no engine verbs.
rows     57 review items (54 residue + 3 demote; the 59 notes are context only) + 55 verify "missed" = 112 rows.
         Per round: D<n> = the review's defects[] index, M<n> = the verify's missed[] index.
late     verify_engine-delta-3a.json landed 16:16Z, after the batch node (accept_with_residue, 2 missed) -- included. verify_engine-delta-3b.json
         is still absent. verify_a00-89094f2f is not empty: its `unstructured` text carries a full verdict (accept_with_residue, D1 upheld, 2 missed).
key      F  fix round: mechanism defect present now (file:line now + testable claim)
         F° mechanism present now but ALREADY its own minted round outside this batch (listed, never a leaf)
         C  node/text correction · K carry (reason) · G gone (file:line that shows it) · -- not an item (the verifier's "none found")
         "-> fold #n" = closed by the same fix/correction as item n.  HELD = hypothesis under goal:g7.33 · TM = thought-master research (lm-*, goal:g5.*)
         node paths are under .agi/nodes/.
```

```
R1  lm-grid-commit-configured-trunk-lifts-branch-blind-refusal · hypothesis/lm-grid-commit-configured-trunk-lifts-branch-blind-refusal.md
    final=accept_with_residue · HELD (goal:g7.33.7)
 1 K  D1 extensions/agi/bin/grid.py:930 "the collision it is refused for cannot occur" (+ the claim's same sentence): verify refuted it as mechanism --
        the guard (grid.py:935) is correct and tested; the absolute is over-broad only for two branches sharing ONE non-default trunk. Wording.
 2 K  M1 dual resolver (note): the guard keys ref_ns_for(root) (grid.py:935), writers key the REF_NS global (set grid.py:160); main() applies it
        before dispatch (grid.py:1823) and grid.py:931-932 now states the coupling. Latent; no production caller skips it.
```

```
R2  lm-grid-storage-trunk-migration-for-local-maxxing · hypothesis/lm-grid-storage-trunk-migration-for-local-maxxing.md
    final=accept_with_residue · HELD (goal:g7.33.7)
 1 F° D1 old namespace refilled + forked: still 3807 refs under refs/grid/node/ (newest 2026-09-21 11:47Z -- not refilled since, never cleaned);
        grid.py:110-130 ref_ns_for still falls back to refs/grid for an unconfigured tree and nothing refuses the write
        -> own round hypothesis:grid-old-namespace-refilled-and-forked (goal:g15, director-engine; excluded from this batch)
 2 F  D2 clause (f) never passed -- and it is LIVE, not merely unrecorded: the grid_sync cron (crontab) pushes 'refs/grid/local-maxxing/*' every
        5 min and origin rejects every ref: "Timed out validating rule, please try again" x2,244,581 lines (+ "Internal Server Error" x61,995),
        661 "failed to push" = about every tick since the 09-21 06:5xZ cutover, 0 accepted; ls-remote: 0 trunk refs on origin vs 4060 local;
        the cron log <logs>/agi-crons-agi-3fbc6951.log is 550 MB and grows ~4k lines per tick.
        claim: the grid_sync push of the configured trunk goes out in batches of <= N refspecs (N a config cell) so a first push of ~4k new refs
        completes and `git ls-remote origin 'refs/grid/local-maxxing/*' | wc -l` equals the local count; a rejected batch logs one summary
        line, not one line per ref.  (cause inferred from the rejection text; if the remote's ruleset itself forbids the refs, bank for the owner)
        + C rider: node:28 "G14.14.7 closed end to end" -> (f) not met
 3 C  D3 node:28 "versions doc:lm-town-trajectory = 1, the seed" vs the claim's (d) >= 3 (:16): mark (d) failed at cutover (live count is 8 now)
 4 K  D4 verify refuted: exp a00-b60c64bd:49 is superseded by its own THOUGHT :136; "one code path" (:47-48) is about the destination, true at
        grid.py:1574 (new_ns = target or ref_ns_for(root))
 5 C  M1 experiment/a00-b60c64bd-a999da.md:35 "No live ref was moved and the live .agi/config.json was not edited" vs its own THOUGHT :136 (the
        probe moved and restored all 3773 live refs)
 6 F° M2 root mechanism = worktrees whose config lacks grid.storage_trunk -> fold #1 (same own round)
 7 C  M3 node:28 ends "PROOF PENDING ... checked at 06:55Z+" and never records the result (trunk newest version 2026-09-23 16:15Z: the cron commits)
 8 K  M4 clause (e) rests on the sibling round's guard change (grid.py:935 = R1): a dependency between two hypotheses, correctly separate
```

```
R3  lm-jev-class-conditional-t-recovers · hypothesis/lm-jev-class-conditional-t-recovers.md · final=accept_with_residue · TM (idea -> goal:g5.24)
 1 K  D1 experiment/a00-2bfe6e45-9d9f08.md:38 bare corpus path (rule 13, extensions/agi/lib/agent-prompt.md:91): no paths.* cell and no reader exist on
        this branch (.agi/config.json has no `paths` key; .agi/context/local-maxxing/paths.py is 2c5b0a26a, not an ancestor) -> the path-cell lane
        (hypothesis:lm-every-experiment-path-is-a-config-variable, goal:g5), not a round
 2 K  D2 probe_cls_t.py gone under .gitignore:100 (.agi/sessions/*): disclosed (:112-113, THOUGHT :131); the committed 9-row bench reproduces the table
 3 K  D3 parent probes likewise gone: disclosed; same class and precedent as #2
 4 K  M1 .agi/context/local-maxxing/bench/20260919T055050Z.jsonl:9 "out" = an absolute /home/<user>/... worktree path: the certified run's own record;
        rewriting evidence to satisfy path_max is worse than the literal
 5 K  M2 the named paths.local_maxxing.* cell does not exist -> same lane as #1
 6 K  M3 the review's ":47,:123,:125" repeat is a slip (the corpus literal is only at :38); nothing to change
```

```
R4  lm-kv-span-shift-reproduces-re-prefill-continuation · hypothesis/lm-kv-span-shift-reproduces-re-prefill-continuation.md
    final=accept_with_residue · TM (goal:g5.30.1)
 1 C  D1 experiment/a00-3879bc40-677758.md:17 probe ":3020 return NEOX" + "every citation is line-exact", again THOUGHT :123/:126 -> 3025 (its table :61
        and commit 7a161ae1c already say 3025); add an in-node correction line
 2 C  D2 experiment/a00-7cb81102-d4f828.md:214 Agent Notes "nothing restarted" unflagged (the :156 heading IS flagged by the :218 correction) ->
        restarted (container Created 05:42:48Z with --cache-reuse 8; the parent review :216 says so)
 3 K  D3 verify refuted: goal:g14.15.1/.2 in body prose (:39/:43/:73/:79); the renumber rule binds frontmatter, re-pointed at :7
 4 C  M1 D1 under-cited (THOUGHT :123/:126, no in-node correction note) -> fold #1
```

```
R5  lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery · hypothesis/lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery.md
    final=accept_with_residue · TM (goal:g5.27.1)
 1 C  D1 datasets/switch-rule/2026-09-21/README.md:133/:135 IFEval "not measured" for B/C2 and :138 "The IFEval side has no local row" -> B 0.778189
        (421/541), C2 0.802218 (434/541) per gap_table.md; exp a00-b52705a2:109 left it for the parent, never done
 2 K  D2 verify refuted: ifeval_gen_arm{B,C2}.py:14 "[REDACTED]" default is the mandatory scrubber's output on a dead default; every documented
        invocation passes base_url
 3 K  D3 datasets/switch-rule/2026-09-21/ifeval_seeded_wrapper.py:2 default IFEVAL_HARNESS = a gitignored session dir: disclosed (exp a00-1864ce6e:89),
        env override exists, a cell cannot restore a gitignored harness -> path-cell lane
 4 K  D4 C2 HumanEval is a single run, per-problem scorer output never landed: disclosed (a00-b52705a2 title); parent re-run reproduced 143/164
 5 C  D5 goal/g5.27.1.md:43 "renumber ... g5.27.1 -> g5.27.1" -> g14.11.1 -> g5.27.1   -> fold R16 #4 (13 goal THOUGHTs, one pass)
 6 K  D6 experiment/a00-e699a4ec-a83259.md:167 "goal:g14.10's own rule": body prose (class refuted in R4/R12/R13/R14/R16)
 7 C  M1 experiment/a00-e699a4ec-a83259.md:41/:53 define b = #ref-only / c = #arm-only; gap_table.md:27/:38 (after TMM.39) read b (#arm-only) | c (#ref-only)
 8 C  M2 duplicate live id build:bin-adapters-grok-bot-adapter -> same correction as R14 #3
 9 C  M3 datasets/switch-rule/2026-09-21/gap_table.md:3 round/node credit omits SWR-RS.01 / experiment:a00-1864ce6e-9139b7 (its seeded table is in the file)
```

```
R6  lm-jev-verdict-ece-floor-is-label-disagreement · hypothesis/lm-jev-verdict-ece-floor-is-label-disagreement.md · final=accept_with_residue · TM (goal:g5.24)
 1 F  D1 datasets/jev-typed-acts/jev_label_disagreement_split.py:8 `W = D + '/../../../..'` (4 levels, the old typesafe/ depth) resolves above the repo
        from datasets/jev-typed-acts/, so the node glob is empty and the graph split collapses to 0 acts
        claim: run from datasets/jev-typed-acts/, the script finds the repo by walking up to the nearest .agi (as q1_label_pairs.py:12-15) and its
        graph split reproduces resolvable_graph_acts 40 and the 10 graph rows of bench 20260919T063222Z
 2 C  M1 experiment/a00-f8aca319-427816.md:66-67 isotonic "<=0.10 on 2/5 seeds (gold 0.067/0.102)" -> 1/5 (0.1022 > 0.10)
 3 C  M2 experiment/a00-f8aca319-427816.md:62 full-corpus 0.3234 sits under "Rows: bench/20260919T063222Z.jsonl" (:36); it lives in 20260919T055335Z.jsonl:2
 4 F  M3 datasets/README.md:12 "locate data relative to themselves and still run" is false for this script -> fold #1 (true once #1 lands)
 5 F  M4 path_max root cause of #1 -> fold #1
```

```
R7  lm-jev-verdict-ece-target-is-under-the-finite-sample-floor · hypothesis/lm-jev-verdict-ece-target-is-under-the-finite-sample-floor.md
    final=accept_with_residue · TM (goal:g5.24)
 1 C  D1 datasets/jev-typed-acts/jev_ece_floor.py:52 emits real_ece at row level only; the pre-registered report clause (hyp :22: real held-out ECE per
        ACT) is unmet and the experiment never says so -> record it NOT_MET on experiment/a00-f61fb527-194c52.md (verdict-neutral: the falsifier
        rides the synthetic medians)
 2 K  D2 verify refuted: random.Random split (script :37) is a recorded numpy-forced deviation (exp :47-54) that reproduces the bench byte-identically
 3 C  D3 experiment/a00-f61fb527-194c52.md:89 and :120 "2-6x its own null median" -> 1.31-7.10x row / 0.77-4.44x act (seed 7 sits inside its null band)
 4 C  D4 hypothesis/lm-jev-verdict-ece-target-is-under-the-finite-sample-floor.md:30 Ceiling ".agi/context/local-maxxing/typesafe/" (gone) -> datasets/jev-typed-acts/
 5 C  M1 experiment/a00-f61fb527-194c52.md:56 Command writes "../bench/20260920T061450Z.jsonl" (= datasets/bench/, absent) -> the committed
        .agi/context/local-maxxing/bench/20260920T061450Z.jsonl
 6 C  M2 experiment/a00-f61fb527-194c52.md:62 experiment/20260918 real ECE 0.1901 -> 0.1902 (bench and a byte-identical re-run)
 7 K  M3 hyp :24 control "(600 rows)" vs 300 held out: reconciled in the hypothesis Agent Notes; pre-registered text stays as written
```

```
R8  lm-jev-verdict-t-is-degenerate · hypothesis/lm-jev-verdict-t-is-degenerate.md · final=accept_with_residue · TM (goal:g5.24)
 1 K  D1 verify refuted: the hypothesis is the pre-registered claim; the experiment (title :24, :106-112) carries the refutation (sibling practice)
 2 K  D2 verify refuted: sweep_t.py gone (.gitignore:100), disclosed by the CORRECTION :128; bench 20260919T055309Z.jsonl (2211 rows) re-derives every table
 3 C  D3 experiment/a00-c522b82d-5f20fe.md:35 ".agi/context/local-maxxing/typesafe/acts_replay_scrub.jsonl" -> datasets/jev-typed-acts/ (siblings were
        re-pointed in 9755735e0, this one not); the bench config row :1 carries the same dead string (keep the recorded row, note it in the node)
 4 C  D4 experiment/a00-c522b82d-5f20fe.md:18 and :120 "ECE range 0.34-0.47" beside "ece_min 0.09-0.15" in one sentence; rows give 0.4965-0.5589 per
        seed / 0.0961-0.5414 seed-mean; the probe script is uncommitted -> strike or mark unverifiable
 5 K  D5 verify refuted: inconclusive_lean_proved:60 is honest (pre-registered falsifier did not trip; the refutations are stated at :106-112)
 6 C  M1 the self-contradiction is the stronger citation -> fold #4
 7 C  M2 bench :1 dead source string -> fold #3
 8 K  M3 curv_over_sigma field name (note): disclosed in THOUGHT :120
 9 K  M4 shared-RNG protocol deviation (note): disclosed in THOUGHT :120; the numbers re-derive
10 --  M5 "no missed real-resource touch" (not an item)
```

```
R9  lm-magic-pane-detector-predicts-the-form-from-the-first-prose-tokens · hypothesis/lm-magic-pane-detector-predicts-the-form-from-the-first-prose-tokens.md
    final=accept_with_residue · TM (goal:g5.24.3)
 1 C  D1 experiment/a00-aecd4776-2f10c5.md:73-76 "the hypothesis's own falsifier HOLDS" and Agent Notes :112 "falsifier holds" vs title :25 and the
        corrected section :92-103 "VOID, not a falsifier-hold" -> strike/flag both
 2 C  D2 experiment/a00-aecd4776-2f10c5.md:70-71 "Confusion matrices ... in datasets/magic-pane/report.md" -> report.md is now the strict census
        (0 matrices); they survive only at b79f77537
 3 K  D3 hypothesis ...prose-tokens.md:52/:57/:60 goal:g14.10.2 in Agent Notes: prose (frontmatter re-pointed to goal:g5.24.3); the same class is
        refuted by 6 sibling verifies and the planned retired-ref reader scans frontmatter/config/instruction surfaces only
 4 C  M1 :112 "thinking mode scores 0/30 at 12.3s" uncaveated (the UNEVIDENCED marker is only at :90) -> fold #1
 5 C  M2 Evidence table + findings :61-90 still present the void 237-set numbers as results -> fold #1
```

```
R10 lm-pi-local-9b-kid-completes-a-minimal-round-within-the-slot · hypothesis/lm-pi-local-9b-kid-completes-a-minimal-round-within-the-slot.md
    final=accept_with_residue · TM (goal:g5.19)
 1 C  D1 hypothesis/lm-pi-local-9b-...-slot.md:15 verdict inconclusive_lean_proved:85 while its only experiment a00-e51d276e-f76d76.md:22 is pending
        (TMM.40) -> pending (the brief's rule: a failed gate is honest pending, never a lean)
 2 C  D2 verdict/a00-b88dc08d-bcf00b.md:20 inconclusive_lean_proved:85 -> pending; `links.py schema` reports exactly this verdict-class pair
 3 K  D3 verify refuted: "45-2,973 tokens/turn" is an unchanged, source-disclosed narrative line; the cache-hit mechanism is backed by the bench
 4 C  M1 the reader is links.py:337-354 (_verdict_class_disagreements) -> fold #2
 5 K  M2 no reader compares a hypothesis verdict to its experiment (metrics.py:505-524 counts the lean): a feature gap; #1 closes the instance
```

```
R11 a00-89094f2f-940a6c · hypothesis/a00-89094f2f-940a6c.md (goal:g7.25.2) · final=accept_with_residue (verify in `unstructured`: schema-violating, complete)
 1 G  D1 .agi/config.json:113 bin is now "~/.npm-global/bin/grok-bot" (076e6698f, EF.29): no /home/<user> literal. (The binary is absent on this
        box -- provisioning, not this item.)
 2 K  M1 extensions/agi/tests/test_grok_bot_adapter.py:248 `assert live_bin != grok.DEFAULT_BIN` would redden on a bare-name cell; the ~/ fix taken
        keeps it green. Latent only.
 3 K  M2 os.fork() at test_grok_bot_adapter.py:50: a self-reaped, test-owned child (note, same as every sibling review)
```

```
R12 a00-8ee9bdff-40419b · hypothesis/a00-8ee9bdff-40419b.md (goal:g7.25.3) · final=DEMOTE (review and verify)
 1 C  D1 (demote) hypothesis/a00-8ee9bdff-40419b.md:19 claim "asserts the locked NotImplementedError stub restart" (+ body :36/:51) vs bytes: restart
        is a real detached respawn (extensions/agi/bin/adapters/grok_bot_adapter.py:105-161, Popen :143), test :40-45 expects TypeError
        -> demote `verdict: proved` (:23) or re-version the claim to the merged artifact
 2 C  D2 (demote) :19 and probes :14 "8 passed", blob 85c5cb43 (+ :32/:49) vs the committed file: 15 tests, blob now e37baef7 (ee2306f24) -> fold #1
 3 C  D3 (demote) experiment/grok-bot-mirror-green-and-loud.md:81 "git hash-object = 85c5cb43..." (+ title :19 "8-passed", :31 blobs, :21 proved) -> fold #1
 4 C  D4 experiment/grok-bot-mirror-green-and-loud.md:83 "on this branch alone the file collection-errors": stale (adapter + row present, suite green)
 5 K  D5 verify refuted: g17.14.x in body prose (:31-33/:69); frontmatter re-pointed (270e93a7e); core's (core-sync-0923-residues R6)
 6 K  M1 os.fork() in the round's test (note)
 7 C  M2 verdict/grok-bot-mirror-proved-loud.md:20 proved, :34 "8 passed in 0.03s", :36 helper blobs, :48: the same stale artifact -> fold #1
 8 K  M3 experiment :30 branch name season2/loops/goal-g17.14.2-helper-cfg-land is a resolvable ref: do NOT re-point it under R6
```

```
R13 a00-da41e117-c79b5e · hypothesis/a00-da41e117-c79b5e.md (goal:g7.25.2) · final=accept_with_residue
 1 C  D1 hypothesis/a00-da41e117-c79b5e.md:27 "DEFAULT_BIN = /home/ubuntu/.npm-global/bin/grok-bot" (+ experiment/grok-bot-bin-matches-adapter.md:18/:42/
        :50/:140, verdict/grok-bot-bin-cell-agrees-with-adapter.md:17/:42) vs grok_bot_adapter.py:30 DEFAULT_BIN = "grok-bot" (bare, PATH) and the
        cell .agi/config.json:113 "~/.npm-global/bin/grok-bot"
 2 K  D2 verify refuted: g17.14.x body prose -- core's (R6)
 3 G  D3 .agi/config.json:113 "~/.npm-global/bin/grok-bot" (076e6698f): no per-box /home literal
 4 C  M1 experiment/grok-bot-bin-matches-adapter.md:101 "verbatim from the file (sed -n '113,124p')" is neither verbatim nor that range (row :107-118,
        different key order) -> fold #1
 5 C  M2 title :16 "config bin must equal the sibling adapter DEFAULT_BIN" is the opposite of the committed gate test_grok_bot_adapter.py:248
        (live_bin != DEFAULT_BIN) -> fold #1 (re-version title/claim: the cell is carried; DEFAULT_BIN is only the bare fallback)
 6 C  M3 verdict/grok-bot-bin-cell-agrees-with-adapter.md:17/:42 repeats the equality -> fold #1
```

```
R14 a00-fcfbc2f9-7d809f · hypothesis/a00-fcfbc2f9-7d809f.md (goal:g7.25.1) · final=accept_with_residue
 1 C  D1 hypothesis/a00-fcfbc2f9-7d809f.md:37 "restart refuses with NotImplementedError" + mvp/a00-fcfbc2f9-grok-bot-adapter-minimum.md:37 "restart
        raises NotImplementedError" vs grok_bot_adapter.py:105-161 real detached respawn (test :40-45, :106-109)
 2 K  D2 verify refuted: g17.14.x body prose -- core's (R6)
 3 C  M1 DUPLICATE LIVE ID: build/a00-fcfbc2f9-bin-adapters-grok-bot-adapter.md (mint 07acc9ce) and build/bin-adapters-grok-bot-adapter.md (mint
        93a56c11, the DT.24 canonical) both declare build:bin-adapters-grok-bot-adapter with the same payload_ref; the loader keeps the a00 file and
        hides the canonical from every reader (links.py still 0 broken) -> give the a00 node its own id and deprecate it (mint kept; never git rm)
 4 C  M2 its spawn_check_reason "parent ... mvp:grok-bot-adapter-minimum resolves to no node" is stale (it resolves) -> fold #3
```

```
R15 lm-jev-isotonic-per-group-fixes-verdict-ece · hypothesis/lm-jev-isotonic-per-group-fixes-verdict-ece.md · final=accept_with_residue · TM (goal:g5.24)
 1 C  D1 hypothesis :11 "the same 50/50 by-act-id split ... as experiment:a00-bdec620b" is false: datasets/jev-typed-acts/jev_isotonic_residual.py:33 builds
        acts from all rows (170, incl. the label-less verdict:a00-4e84f537) -> 85/85, 252 held rows vs 169 / 84-85 / 255 there -> disclose on
        experiment/a00-fb3ab94b-01f359.md (disproved unaffected: the target fails 2/5 by a wide margin)
 2 K  M1 config_max=yes on the bare datasets/ paths in node text (rule 13): no paths.* cell/reader on this branch -> path-cell lane (as R3 #1)
 3 C  M2 datasets/jev-typed-acts/jev_isotonic_residual.py:3-4 docstring "Kept under typesafe/ not sessions/" -> datasets/jev-typed-acts/
 4 K  M3 review-meta (asymmetric ownership answers); no bytes to change
```

```
R16 core-sync-conflicts · goal:g15 (merge 8451055b5; sync node hypothesis/core-sync-0923-residues.md) · final=accept_with_residue
 1 C  D1 goal/g5.30.md:33 town copy orders "mints G14.15.1 ... G14.15.2" beside core's :42 G5.30.1/G5.30.2 -> drop :33   (TM-side node)
 2 C  D2 goal/g5.31.md:46 "ADD G14.16.2 ... after G14.16.1" beside :53 G5.31.2/G5.31.1 -> drop :46   (TM-side node)
 3 K  D3 verify refuted: stale G14.x ids in historical agent-note prose (g7.33:51-63, g5.24, ...); every frontmatter parent resolves
 4 C  M1 13 goal THOUGHTs record a self-renumber "renumber local-maxxing research gX -> gX" (g5.22 g5.23 g5.24 g5.24.3 g5.25 g5.25.1 g5.26 g5.27
        g5.27.1 g5.28 g5.29 g5.30 g5.31) -> the g14.* source id (map: `git show --stat acdb0e4f7`; g14.11.1 via 8451055b5); goal/g7.33.md:48 records
        no g14.14 -> g7.33 at all   (TM-side nodes + g7.33)
 5 C  M2 doc/lm-town-trajectory.md status: deprecated (:11) but not moved to deprecated/doc/; still carries live metric rows (:40-46); its pointer
        :19/:32 names "G7.33.5" (no such goal) where town/local-maxxing.md:49 says goal:g7.34.1/.2   (TM-side node)
```

```
R17 core-sync-renumbers · goal:g15 (the 8 renamed goal nodes) · final=accept_with_residue
 1 C  D1 goal/g7.33.3.md:22 title "(owner ... on goal:g14, relayed via goal:g7.33)": g14 is retired and its owner lines moved to goal:g5 (g14 THOUGHT)
        -> goal:g5 (the reporter's "links.py retired-refs ... -> g20" does not exist)   (g7.33 subtree)
 2 C  D2 goal/g7.33.7.md:25 title "... on goal:g14, supersedes G14.14.6 ..." -> same   (g7.33 subtree)
 3 C  D3 8 renamed goals keep the old id as title prefix AND body heading: g7.33.1:24/:28 g7.33.3:22/:26 g7.33.7:25/:29 g5.30.1:23/:27 g5.30.2:21/:25
        g5.23.2:22/:26 g5.23.3:22/:26 g5.26.2:22/:26; snapshot-goals.py:912-913 strips only a matching prefix, so GOALS.md:12795/:12884/:12887 render
        two ids for one goal ("G7.33.1 -- G14.14.1: ...", "# goal:g14.14.1") -> "G7.33.1:" / "# goal:g7.33.1" etc.
 4 K  M1 in-scope bodies cite deleted ids (g5.23.3:30/:32/:38, g5.26.2:36, g5.30.1:39, g5.30.2:37, g7.33.1:33/:39, g7.33.7:42): prose, as R16 #3
 5 K  M2 the same prose dangle outside the 8 (lm-kv-span-shift, g5.24.3:42, lm-magic-pane:52, a00-bb4db5d2:128/133): prose
 6 C  M3 goal/g7.33.1.md:33/:39 cite "(THOUGHT on goal:g14.14.3)" for the chained-note-calls bug, but that THOUGHT was replaced by the renumber note
        -> cite the grid version of goal:g7.33.3 that still carries it (or restate the bug inline)   (g7.33 subtree)
 7 K  M4 review-meta: the reporter's reader (links.py retired-refs) and its g20 successor were invented; the defects stand on re-derived bytes
```

```
R18 engine-delta-1 · goal:g15 (ed54be7d..ebae4adde; experiments []) · final=accept_with_residue
 1 K  D1 adapter/test docstrings name goal:g17.14.1/.2/.3 (grok_bot_adapter.py:1/:12, test_grok_bot_adapter.py:1/:5/:41/:132): verify refuted as
        wording; routed to hypothesis:links-py-flags-live-references-to-retired-goals (the batch node: not in this batch)
 2 F° D2 harness_template._emit silently drops an unknown slot/when: still extensions/agi/bin/harness_template.py:174 and :186 (`values.get` -> [])
        -> own round hypothesis:harness-template-emit-refuses-an-unknown-slot (excluded from this batch)
 3 K  M1 node bodies mvp/grok-bot-mirror-test-deliverable.md:24/:36/:51/:52 and build/{bin-adapters-grok-bot-adapter,tests-test-grok-bot-adapter}.md:32
        spell goal:g17.14.*: prose (no live frontmatter parent/loop carries g17.14 any more; 22 live bodies do) -- core's g17.14.x (R6)
 4 F  M2 test_bin_help_smoke[harness_template.py] is RED: extensions/agi/bin/harness_template.py has no __main__/--help (exit 0, empty stdout) and is
        not in NO_HELP (extensions/agi/tests/test_bin_help_smoke.py:24-30); it is the only such bin/*.py
        claim: test_bin_help_smoke passes for every bin/*.py -- harness_template.py is skipped by name as a library module (or answers --help)
 5 K  M3 pi_adapter._append_prompt_args (extensions/agi/bin/adapters/pi_adapter.py:97-109) spells --append-system-prompt: the disclosed NAMED LIMIT
        (a template cannot repeat a flag over a dynamic list), not a template_max miss
```

```
R19 engine-delta-2 · hypothesis/harness-arg-builders-are-templates-only.md (goal:g7.27) · final=accept_with_residue
 1 F  D1 Town.location is read (extensions/agi/bin/towns.py:138, _load_one), carried (:157) and printed (:385) but no committed test reads it
        (test_towns.py / test_town_rows_readers.py never touch .location; test_town_schema.py:46 is a superset check)
        claim: a committed test loads a town node carrying `location: <alias>` and asserts Town.location == <alias> ('' when the cell is absent),
        failing if _load_one drops the cell
 2 F  D2 help-smoke registry -> fold R18 #4
 3 K  M1 dead g17.14.x ids in the grok adapter/test docstrings -> routed as R18 #1
 4 K  M2 os.fork() in test_grok_bot_adapter.py:50 (note)
 5 --  M3 "no unread reader / test-requiring-a-defect found" (not an item)
```

```
R20 engine-delta-3a · hypothesis/harness-arg-builders-are-templates-only.md (goal:g7.27) · final=accept_with_residue (review: accept; verify 16:16Z)
 1 F° M1 harness_template._emit unknown slot/when (harness_template.py:174/:186) -> own round hypothesis:harness-template-emit-refuses-an-unknown-slot
 2 F  M2 help-smoke registry -> fold R18 #4
```

```
R21 engine-delta-3b · goal:g15 (experiments []) · final=accept_with_residue (review only -- verify_engine-delta-3b.json still absent)
 1 G  D1 .agi/nodes/.geometry/commands.md:54 no longer names goal:g13 and :145 names goal:g4.18, matching skills/agi/SKILL.md:807/:816 (the Prime's
        fix at merge, 52c6b630e): a re-derive no longer re-injects g13. (`derive-commands.py --check --all` still exits 1, but only by ADDING the
        declared rows the block never carried -- the pre-existing subset in the review's note D3, not this item.)
 2 G  D2 skills/agi/SKILL.md:272 heading is now "(goal:g4.18)" = commands.md:145
```

```
SUMMARY  112 rows = 57 review items (54 residue + 3 demote) + 55 verify "missed" · worktree @feb043a63e · read-only
counts   F 8 · F° 4 · C 51 · K 43 · G 4 · -- 2        (F/C include "-> fold" rows; 4 distinct F fixes, 20 C-list entries)
 mine    R11-R14, R16-R21 = 47 rows: F 4 · F° 2 · C 20 · K 16 · G 4 · -- 1
 HELD    R1-R2 (goal:g7.33.7) = 10 rows: F 1 · F° 2 · C 3 · K 4
 TM      R3-R10, R15 (lm-*, goal:g5.*) = 55 rows: F 3 · C 28 · K 23 · -- 1
G        .agi/config.json:113 "~/.npm-global/bin/grok-bot" (076e6698f; R11 #1, R13 #3) · commands.md:54/:145 = SKILL.md:807/:816/:272 (52c6b630e; R21)
late     verify_engine-delta-3a landed 16:16Z (2 missed, both folded below); verify_engine-delta-3b still absent

CANDIDATE LEAVES
L1 help-smoke-registers-harness-template  [mine, goal:g15 · closes R18 #4, R19 #2, R20 #2]
   files  extensions/agi/tests/test_bin_help_smoke.py:24-30 (NO_HELP) -- or a --help in extensions/agi/bin/harness_template.py
   claim  test_bin_help_smoke passes for every bin/*.py: harness_template.py (no __main__, exit 0 + empty stdout = the suite's one red case today)
          is skipped by name as a library module or answers --help.
L2 town-location-cell-is-pinned  [mine, goal:g7.27 · closes R19 #1]   (L1 + L2 are test-only; one small round can carry both)
   files  extensions/agi/tests/test_towns.py (reads extensions/agi/bin/towns.py:138/:157)
   claim  a committed test loads a town node carrying `location: <alias>` and asserts Town.location == <alias> ('' when absent); it fails if
          _load_one drops the cell.
L3 grid-trunk-push-lands-on-origin  [HELD, goal:g7.33.7 · closes R2 #2]   LIVE: every 5-min grid_sync push since the 09-21 cutover is rejected
          ("Timed out validating rule" x2.24M lines, 661 failed pushes, 0 trunk refs on origin vs 4060 local; the cron log is 550 MB and growing)
   files  extensions/agi/bin/crons.py (grid_sync line) · extensions/agi/bin/grid.py (a batched push; batch size a config cell)
   claim  the trunk push goes out in batches of <= N refspecs so a first push of ~4k new refs completes and ls-remote's trunk count equals the
          local count; a rejected batch logs one summary line, not one per ref.
L4 jev-split-script-finds-the-repo  [TM, goal:g5.24 · closes R6 #1/#4/#5]
   files  datasets/jev-typed-acts/jev_label_disagreement_split.py:8
   claim  run from datasets/jev-typed-acts/, the script walks up to the nearest .agi (as q1_label_pairs.py:12-15) and reproduces
          resolvable_graph_acts 40 + the 10 graph rows of bench 20260919T063222Z (then datasets/README.md:12 "still run" holds).
F°       hypothesis:grid-old-namespace-refilled-and-forked <- R2 #1/#6 (3807 stale refs/grid/node; grid.py:110-130 refuses nothing)
         hypothesis:harness-template-emit-refuses-an-unknown-slot <- R18 #2, R20 #1 (harness_template.py:174/:186)
routed K g17.14.x prose/docstrings -> core-sync-0923-residues R6 (core) + hypothesis:links-py-flags-live-references-to-retired-goals

C LIST (node -> correction)
 mine
 hyp a00-8ee9bdff :14/:19/:23/:32/:36/:49/:51 + exp grok-bot-mirror-green-and-loud :19/:21/:31/:81/:83 + verdict grok-bot-mirror-proved-loud
   :20/:34/:36/:48 -> DEMOTE: "NotImplementedError stub / 8 passed / blob 85c5cb43" vs real respawn (grok_bot_adapter.py:105-161), 15 tests (R12)
 hyp a00-da41e117 :16/:27 + exp grok-bot-bin-matches-adapter :18/:42/:50/:101/:140 + verdict grok-bot-bin-cell-agrees-with-adapter :17/:42
   -> "bin must equal DEFAULT_BIN = /home/ubuntu/..." is false: DEFAULT_BIN is bare grok-bot and the ~/ cell must DIFFER (test :248) (R13)
 hyp a00-fcfbc2f9 :37 + mvp a00-fcfbc2f9-grok-bot-adapter-minimum :37 -> "restart raises NotImplementedError" is a real respawn (R14 #1)
 build/a00-fcfbc2f9-bin-adapters-grok-bot-adapter (07acc9ce) -> duplicate id hides canonical 93a56c11: own id + deprecate (R14 #3-4, R5 #8)
 goal g7.33.3:22 · g7.33.7:25 -> "on goal:g14" (retired) -> goal:g5   [g7.33 subtree] (R17 #1-2)
 goals g7.33.1/.3/.7 g5.30.1/.2 g5.23.2/.3 g5.26.2 -> title prefix + "# goal:" heading to the new id (GOALS.md:12795/:12884/:12887) (R17 #3)
 goal g7.33.1:33/:39 -> "(THOUGHT on goal:g14.14.3)" points at an overwritten THOUGHT: cite its grid version [g7.33 subtree] (R17 #6)
 TM-side nodes named by my rounds
 goal g5.30:33 · g5.31:46 -> drop the town copies ordering G14.15.x / G14.16.x (R16 #1-2)
 13 goal THOUGHTs (g5.22-g5.31, g5.24.3, g5.25.1, g5.27.1) -> "gX -> gX" names the g14.* source id; g7.33:48 add g14.14 -> g7.33 (R16 #4, R5 #5)
 doc lm-town-trajectory -> move to deprecated/doc/; "G7.33.5" (:19/:32) -> g7.34.1/.2; fold live rows :40-46 into town:local-maxxing (R16 #5)
 HELD
 hyp lm-grid-storage-trunk-migration :28 -> (d) versions=1 unmarked, (e) PROOF PENDING never closed, (f) never passed (R2 #2-3/#7)
 exp a00-b60c64bd :35 -> "No live ref was moved" vs its own THOUGHT :136 (R2 #5)
 TM
 exp a00-3879bc40 :17/:123/:126 ":3020"/"line-exact" -> 3025 · exp a00-7cb81102 :214 "nothing restarted" (R4)
 switch-rule README.md:133/:135/:138 IFEval "not measured" -> B .778 / C2 .802 · exp a00-e699a4ec :41/:53 b/c labels · gap_table.md:3 credit (R5)
 exp a00-f8aca319 :66-67 "2/5" -> 1/5 · :62 0.3234 cited to the wrong bench (R6)
 exp a00-f61fb527 :89/:120 "2-6x" · :56 ../bench/ · :62 0.1901 -> 0.1902 · act-level real ECE NOT_MET · hyp ...finite-sample-floor :30 typesafe/ (R7)
 exp a00-c522b82d :35 typesafe/ path · :18/:120 "ECE range 0.34-0.47" (R8)
 exp a00-aecd4776 :61-90/:73-76/:112 "falsifier HOLDS" + void numbers -> VOID · :70-71 matrices pointer (R9)
 hyp lm-pi-local-9b :15 + verdict a00-b88dc08d :20 lean_proved:85 -> pending (R10)
 exp a00-fb3ab94b (hyp :11) split is 170 acts / 252 held, not a00-bdec620b's · jev_isotonic_residual.py:3-4 docstring (R15)
```

## Agent Notes
assigned: director-engine (the Prime's PASS 2 batch, 16:14Z 09-23; KEEP SPLITTING); the table was sorted by a read-only helper and spot-checked before minting.
