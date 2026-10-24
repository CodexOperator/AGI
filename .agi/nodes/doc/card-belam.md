---
id: doc:card-belam
mint_id: ced15049ceb843b08e51cc50da416298
type: doc
parents:
  - goal:g7.16
next_edges: []
edited_by: belam
scaffold_hash: 3388df8d4c85caa7
season: 3
tags:
  - card
  - prime
  - belam
thought_session: belam-s3-IV
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED · ATOMS)"
town: core
---
# doc:card-belam — the Prime's card (encryption-town = this box, v5): the ONE scratch

Owner 09-23: the card is the handoff scratch and a doc node; `HANDOFF.md` + `.agi/sessions/quorum/belam.md` are symlinks to it. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; §0-§6 ≤ 100 lines; §7 ATOMS is bounded by time, not length (doc:brainstorm-unify §39). Skills: agi-rotate · agi-send · agi-merge-pass · agi-verify · agi-post · agi-town · agi-memory-guard · agi-node-write · agi-goal · agi-master-gate.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam-s3-IV, 10-23 after the owner's hand-off of the Fable brainstorm: §7 ATOMS is new (§39: the owner's asks live in the card, not a second node), 62 rows from the fork's ledger (its header says 60; the tables hold 62). Wave 0 done by the Prime alone: doc:brainstorm-unify (reference), goal:g7.16.1.11.46 (the umbrella) + .46.1 V0 (complete), the owner-only asks banked in §6. Since the last card: L70-L73 landed, F1 nspawn ran (FAIL, 3 causes, R2/R3 banked), the box rebooted 03:45Z, keepalive + CHECK cron off by the owner's word.
<!-- THOUGHT:END -->

## §0 State (10-23)
| | |
|---|---|
| trunk | core/season3/main = MAIN's checkout = posts/belam = origin; the :28 board job auto-lands my town:local-maxxing commits (it can move the trunk between my verify and my CAS: then ask SM to re-cut) |
| pin | /etc/agi/carry.env AGI_TRUNK = 8b247882a2 (L61); director-review is boot=false there (L70 made it true on the trunk), so it is the 1 of 11 posts down after the 03:45Z reboot. Moving the pin = `agi.sh host` then `sudo systemctl start agi-project.service` (banked, §6) |
| me | uid agi-belam SIGNS and PUSHES; after a reboot ~/.gitconfig loses the credential lines (re-add '' + the belam gh helper); I mail SM only; keepalive timer RE-ENABLED 23:14Z 10-23 (the owner saw RC sessions archived after the idle stretch; its first run renamed 6 posts' RC titles back to the post name and pinged all-is-one 15 min from token expiry); CHECK cron still off; box-wake still types `mail: box read` |
| fork | the Fable fork runs beside me as tmux belam-fable (unit agi-belam-fable-2.scope, RC name belam-fable); it is DONE ("just let prime handle it"); ~/.session pins my session id for V0 |
| intake | atoms 64 · placed 9 · red 0 (§7; 63 = the 62 brainstorm rows + V10a's seat_status.py row) |
| landing my commits | commit in ~/t -> `git update-ref refs/heads/posts/belam NEW OLD` -> `sudo -n -u belam git -C /data/work/agi merge --ff-only -q refs/heads/posts/belam` -> push NEW to core/season3/main + posts/belam; links on its own worktree first; anonymize the diff |
| landing SM's L<n> | `~/tools/verify-land.sh L<n> LAND BASE GATETIP`, links on its own tree, CAS posts/belam, ff MAIN, push both, `git checkout -q --detach` |

## §1 Plan — goal:g7.16.1.11.46, the brainstorm in waves (one council brief per wave; the gate line passes before the next brief)
```
W0  me alone           doc node · §7 atoms · V0 · §6 banks                                               DONE 10-23
W1  council brief 1    M1-M4 (§37-§39 atoms tooling) · C1-C3 (§36 agi-cred, workspace cells, the header) · P1 (§30/§34.3 pi 1.x A/B)
                       · U1 (§7 scope report mode) · V10 (§35 AGI_[retired] -> AGI_POST: SM's mechanical leaf, not a council design)
    gate               M1-M4 + C1-C3 falsifiers pass; P1's four numbers on the board
W2  council brief 2    V1 refs/id/P · V2 cred piece (ONE post) · U3 MANIFEST scope/reach/at/pull/atoms · G1 compose/split (§25, §34.5)
                       · the age seal (§23, §34.6) · U6 move falls out
    gate               one rename end to end with 0 edits; one node's history only on its refs/grid/<mint>
W3  council brief 3    V3 root verbs + held lines · U2 certs enforced · U4 routes · spider families red/unify/tune · walk = idle
                       · two lanes (§34.4) · tests to region spiders (§31) · V8 grow-check + §G, python ports (§34.6)
    gate               a planted red found and fixed with no director turn; a held root action printed from the closed set
W4  council brief 4    U5 · U7 one plugin dir · U8 harness cells · §12 alphabet + agi-walk · V6 IOMap rows · V4 mem: · V9 season-0 · C4 · C5
season 4 (out)         PQ signatures · numeric control surface · hardware alphabet · WIF per-kid tokens · income/streaming
```
Labels: §22 is the leaf table; "V3'" = new leaf G1 compose/split; "V7 (python out)" in §34.7/§36.4 = §22's V8.
MINE in W1: the P1 mint step (`p1_ab.py kid-key ARM LEAF --kid-uid N --keydir D --ledger L`, then `kid-done`) ONLY at DG3's explicit request AND after DG3's R1-R4 tip is on the trunk with every P0 item written down; STOP after the g7.31.3.1 smoke for ONE [result]; an unexpected guard = HALT + [red] to SM, never a retry (council, L89 03:38Z). Council 7f0640e29b: ≤ 15 keys (5 frozen leaves x 3 arms; 2 openrouter arms = 10), each $0.50 cap + a non-null expires_at, both read back; one 0600 file per key in a belam-owned 0700 dir, ACL file u:<kid uid>:r + dir u:<kid uid>:x; never in a repo/ref/mail/argv/env; disabled + read back + file removed at arm end. C1 root install DONE 02:31Z 10-24 on L87 e801e96a92: /opt/agi/bin/agi-cred (2832 B) + agi-cred.service + .timer (5 min), first run success, check 'posts 10 pids 190 read 190 gone 0 key-hits 0'; /etc/credstore empty (credits_live false). Rollback: `systemctl disable --now agi-cred.timer; rm /opt/agi/bin/agi-cred /etc/systemd/system/agi-cred.{service,timer}; daemon-reload`.
Each minted leaf closes its §7 rows (state -> leaf:<goal id> | idea:<id> | decision:<line> | out:<reason>); board: intake/placed/red for belam.

## §2 Landed (10-22 .. 10-23)
L70 43086245a3 (director-review boot=true) · .45 close 73a32e5567 · L71 dfd3d65286 (F1 harness) · L72 4ca7c5d592 (image build) · L73 d17d3785a8 (run-3 fix, re-cut after the board-job race). F1 nspawn run 3 = FAIL, a reading: R2 rows() has no boot filter; R3 settings.json left 755 vs flags_ok 600; F strict isup. Evidence /data/f1-nspawn-*.out (700).
10-23: W0 = doc:brainstorm-unify + goal:g7.16.1.11.46 + .46.1 V0 (agi-run 2260 B, lane session-pin.t.sh 9/9) + this card.

## 🔴 Where it stops
W1 RUNNING: brief 1 2ef3c2f6d6 -> council 3/3 (alive 21:06Z) -> L74 6b6f926c0d landed = leaves .46.2-.46.10 (M1-M4 DG2 · C1-C3 DS1 · P1 DG3 · U1 dg1); V10a (.46.11) is SM's, lands as its own L. NEXT: land each L SM cuts; C1's root install is mine. Gate to W2 = M1-M4 + C1-C3 falsifiers pass + P1's numbers on the board ('passed except <banked>' goes to the owner). K4: rotate.py counts my WHOLE card vs 100 lines, so a driven handoff refuses until M1 lands.
NEXT COMMAND: `AGI_POST=belam AGI_BOX=encryption-town timeout 120 box read` (from ~/t) on mail. Chain anonymize -> box send with &&; the body goes on STDIN.

## §4 Traps (121-123 = gen III: move them to their skills at MY rotation)
| # | trap | rule |
|---|---|---|
| 121 | agi.slice hit MemoryHigh on 2.2 GiB of dentry slab after scratch-worktree harness runs | one harness at a time; slab warn: `sync; echo 2 | sudo tee /proc/sys/vm/drop_caches` |
| 122 | a gate dir under another post's uid (700) reads as 'missing' to my uid | read existence as root before calling anything stale |
| 123 | my card with a literal home path was refused at the push after the :28 board land had ff'd MAIN | anonymize the card DIFF before landing; write ~/ for own paths |
| 124 | `box send M` with the body as an argument sent an EMPTY message | the body goes on stdin: `printf '%s\n' "$M" | ... box send sanctuary-master` |
| 125 | a reboot's `claude -c go` resumed the fork (newest transcript) at my post | V0 (.46.1) fixes it on the trunk; live only after the pin moves |
| 126 | the :28 board commit raced SM's cuts 3x (L73, L75, L79): the CAS refused, a re-cut followed | council d4b23bd05a: SM reads posts/belam at cut time (R1) and its send step refuses :20-:29 (R2). My [raced] names the cut's send minute + the newcomer commits. R3 (my land-side re-merge of board-only newcomers, conditions C1-C3) is BANKED; trigger = one race with R1+R2 in place |

## §5 Verification
10-23 W0: session-pin.t.sh 9/9 (mutant m RED as designed); fresh-alert, claude-upsell, boxwake-unit, post-env, restart-bounds, agi-fresh, agi-strand, box-wake all 0 FAIL; anonymize ok on the doc (115 KB, hostname -> <host>), the goals and this card.

## §6 BANKED (owner-only; no council needed)
| item | recommendation |
|---|---|
| Doppler: a READ-ONLY service token for root (project agi, the config holding CLAUDE_CONSOLE_SP_KEY) into /etc/credstore/doppler-token | needed by C1 agi-cred (W1); root has no Doppler token today |
| Console: lane workspaces agi-batch · agi-kids · agi-council with spend + TPM caps, prime-director added to each; their wrkspc_ ids (not secrets) | needed by C2/C3 (W1); or OPTION B: one workspace-scoped key per lane (no header anywhere) |
| prime-director's org role | developer, unless the Admin cost reports (C4) need admin; then root only ever holds it |
| OpenRouter for P1: RESOLVED 06:1xZ 10-24. The owner topped up the OPENROUTER_ADMIN account ($33.44 left); .env's OPENROUTER_PROVISIONING_KEY now = Doppler agi/dev OPENROUTER_ADMIN (read on the box through ~belam/.config/sanctuary/doppler/agi-dev.rw), the old line kept in .env.before-or-admin-20261024 | the retry of the one kid-key waits on the council's go |
| the prereq_notice cron row (goal .46.12, L94, user agi-sanctuary-master) is DARK until a `crons.py apply --sudo` | the owner's GO; then the notices run each trunk move (SM seeded refs/notices/prereq/seen at L94) |
| link the Console org that carries the $200/mo credits (§13, §36) | link now (the credits expire monthly); the credits arm of P1 needs it |
| boot pin move to the current trunk (brings L70 director-review boot=true + V0 live) | `agi.sh host` + start agi-project.service; director-review may need a re-login (keepalive is off) |
| R2: agi.sh rows() starts boot=false posts (TM, DT-1) on a first start | (b1) filter boot=false + recover=false in rows() — decide before F2 |
| R3: each agi-post@ start leaves settings.json 755; flags_ok wants 600 | R3a the unit chmods it 600; NO `agi.sh start` on the live town until ruled |
| §21 decisions still open: #1 identity = refs/id/P chain · #2 cred as a secret piece, one post first · #3 signatures only at the boundary set · #4 chain height over wall time · #5 mem: cell in OptChat's shape · #6 symbolic control surface · #8 root never loaned as a shell · #10 IOMap on the hypothesis, g2.2 active · #11 season-3 pick as a route exercise (your rows = thirds + rollover) | each as the doc recommends; council reviews #1-#4 in W2, #8 in W3. Ruled already: #7 in part (you made prime-director/prime-key in Doppler; the org link stays above) · #9 (§34.1 three spider families) · #12 (§39 atoms in the card) |
| V10b (the word sweep, later wave): the owner's §35 "No seat reference anywhere" vs SM's reading 10-23 (the whole-word grep hits 2152 files / 21165 lines; ~5937 are quote or owner-verbatim lines; ~30 node ids carry the word) | exclude owner-verbatim lines and closed records (complete/disproved/supported/retired), as deprecated/ is excluded; the owner's words are never rewritten (SM's recommendation, mine too; the council's [decision] follows). V10a (AGI_[retired] -> AGI_POST) goes ahead in W1 |
| atom 2.19: Belam on Fable permanently | a posts.md row edit (model cell), your call |
| atom 4.1: "anti-fragile" read as self-perpetuating (no council post carries the name) | confirm, or name a fourth council post |
| .44.8 F2 + .44.7 live half: the next real fresh box | one event; both leaves close on it |
| /data/f1-nspawn-image (noble.tar) | remove once you confirm you read F1 |
| 657 refs/archive/worktrees/* in MAIN; refs/grid on E vs L differ | G1 compose/split (W2) settles the grid; keep until then |

## §7 ATOMS — the owner's 10-22/23 brainstorm (doc:brainstorm-unify), 62 rows; state = target into the doc until placed

**throw 1 (10-22) — graph-interface design**
| # | atom (owner ask, short) | source | state | lap |
|---|---|---|---|---|
| 1.1 | "button down the graph-interface design" | src:doc | target:§0–§2 | lap124501 |
| 1.2 | "simplify / unify" | src:doc | target:§0 (every rule = a cell), §24 (one spawn path) | lap124501 |
| 1.3 | "compare with matrix-skills" | src:doc | target:§1 (take O/check + api module; leave its engine) | lap124501 |
| 1.4 | "MCP auto-start" | src:doc | target:§6 (wake abstraction; start = visitor) · decision:§21-Part I #2 | lap124501 |
| 1.5 | "MCP push" | src:doc | target:§6/§26 (no push dependence; wake tool + fifo) | lap124501 |
| 1.6 | "filesystem-like MCP by post identity" | src:doc | target:§6 (resources = scope closure; visitor default) — thin, one line | lap124501 |
| 1.7 | "cross-compat CC / codex / grok / pi" | src:doc | target:§8, §26, §28 | lap124501 |
| 1.8 | "engine updates reach seeds without re-project" | src:doc | target:§4 (root fixpoint on the trunk ref) | lap124501 |
| 1.9 | "mathematical guardrails: scope/graph packs, parent/kid inheritance" | src:doc | target:§2 (§Z1/§Z2), §24 (`scope ⊆ director's`) | lap124501 |
| 1.10 | "move tooling with fewer pieces" | src:doc | target:§5 (pack → row → tick → in) | lap124501 |
| 1.11 | "matrix math for a Go port" | src:doc | target:§7 "Go: not now" (one algebra module, port only on latency) | lap124501 |
| 1.12 | "compare openrig / herdr / t3" | src:doc | target:§8 | lap124501 |

**throw 2 (10-23) — identity, memory, hashes, matrices, credits, root, season, income, projects, spiders, IOMap**
| # | atom (owner ask, short) | source | state | lap |
|---|---|---|---|---|
| 2.1 | "restore the Prime's session" | src:doc | leaf:goal:g7.16.1.11.46.1 (V0) · was: done (restore.sh; V0 leaf) | lap124501 |
| 2.2 | "credentials ride in a capsule / reuse the username slot" | src:doc | target:leaf:V1 (cred piece) · decision:§21 #2 | lap124501 |
| 2.3 | "identity = composable key over signed pieces, re-hashed on swap, continuity = the history" | src:doc | target:§9 · decision:§21 #1 | lap124501 |
| 2.4 | "optmem: Prime always; council/keep per season; directors per goal; parents/kids in optchat" | src:doc | target:§11 (`mem:` cell) · decision:§21 #5 · §37 (the ledger) | lap124501 |
| 2.5 | "fully hash-based ids, minimize public/private keys" | src:doc | target:§10 (boundary set B) · decision:§21 #3 | lap124501 |
| 2.6 | "daisy-chained hashes as the post's sense of time" | src:doc | target:§10 (time = chain/block height) · decision:§21 #4 — covered under other words | lap124501 |
| 2.7 | "each node a location in a matrix space; traversal = matrix op" | src:doc | target:§12 (words in, algebra in the engine) · §32 (graph distance is the coordinate) | lap124501 |
| 2.8 | "actions as vectors; mail as a vector" | src:doc | target:§12 (alphabet Σ, M_a) | lap124501 |
| 2.9 | "workflows ARE spawns ARE subagents ARE posts" | src:doc | target:§24, §27, §29 (flow = chain = post node) | lap124501 |
| 2.10 | "soft constraints: no hard cornering / teleportation" | src:doc | target:§12 (word length k, transition matrix T, phase bound Θ) | lap124501 |
| 2.11 | "a jev experience for all models" | src:doc | target:§12 (one line) — thin; g1.25 jev grammar is the owner of it | lap124501 |
| 2.12 | "can LLMs tolerate matrix-encoded control" | src:doc | target:§12 (no: never numbers in a prompt) · decision:§21 #6 | lap124501 |
| 2.13 | "use the $200/mo Console credits; batching" | src:doc | leaf:goal:g7.16.1.11.46.8 (C3) (L74) · was: §13, §36 · decision:§21 #7 · leaves C1–C5 | lap124501 |
| 2.14 | "batch-spawn parents/kids" | src:doc | target:§13, §29 (only `pull: none` steps batch) | lap124501 |
| 2.15 | "headless pi, cheap on memory" | src:doc | leaf:goal:g7.16.1.11.46.9 (P1) (L74) · was: §30 (P1) | lap124501 |
| 2.16 | "Fable sparingly for council reviews" | src:doc | target:§13/§30 (a `plan`/review step model) — thin | lap124501 |
| 2.17 | "loan root to SM (graph moves) and council (unanimous)" | src:doc | target:§14 · decision:§21 #8 | lap124501 |
| 2.18 | "report why a root action was withheld" | src:doc | target:§14 (closed set of held lines) | lap124501 |
| 2.19 | "Belam to Fable permanently; bother the owner only at thirds/rollover" | src:doc | target:decision:§21 #11 (rows = thirds + rollover) — Fable-permanent is a posts.md row edit, owner's call | lap124501 |
| 2.20 | "let the season close independently, picking from this brainstorm + horizon goals" | src:doc | target:§15 · decision:§21 #11 | lap124501 |
| 2.21 | "self-improve" | src:doc | target:folded:§34.1 tune + §19 IOMap loop (was dropped; caught by §37's grep) | lap124501 |
| 2.22 | "live-stream its own progress; interactive games for income" | src:doc | target:deferred:season 4 (§20 dependencies) | lap124501 |
| 2.23 | "stream-master with optchat/optmem always on" | src:doc | target:§11 (`mem: always` row) + §20 | lap124501 |
| 2.24 | "animated avatars via mystudio.fun; grant; hold tokens for credits" | src:doc | target:§20 (mystudios.fun = reseller, no avatar product; treasury = owner) | lap124501 |
| 2.25 | "a second subscription for split logins" | src:doc | target:§27 (`cred: <capsule>` per row, own slot) | lap124501 |
| 2.26 | "import other projects; let others use the system; season 0→1 as init" | src:doc | target:§16 (season-0 capsule) — one section, thin on "others use it" | lap124501 |
| 2.27 | "replace grow.py / links.py with shell or chain checks; auto-written links" | src:doc | target:§17, §23, §34.6 | lap124501 |
| 2.28 | "self-summarizable graph via optmem/optchat per chain" | src:doc | target:§11 (store = node tree; brief = recall) | lap124501 |
| 2.29 | "spiders crawl / test / fix / launch ideas; no more gating or waiting" | src:doc | target:§18, §31, §32, §34 · decision:§21 #9 | lap124501 |
| 2.30 | "IOMap goal: shapes before build; primitive transport; lower-level / inverse abstractions later" | src:doc | target:§19 · decision:§21 #10 · deferred:season 4 (inverse/assembly) | lap124501 |
| 2.31 | "some parts can wait till season 4 (lower-level matrix)" | src:doc | target:§15 (season-4 list) | lap124501 |

**throw 3 (10-23) — the ten reading questions**
| # | atom (owner ask, short) | source | state | lap |
|---|---|---|---|---|
| 3.1 | "retire the python; only keygen/hashing left?" | src:doc | target:§23 (keygen/hashing already shell; 4 pieces to port) | lap124501 |
| 3.2 | "one spawn/dispatch path; pull setting" | src:doc | target:§24 | lap124501 |
| 3.3 | "grid monolith, node = branch, post = slice; spiders under council; red-team" | src:doc | target:§25, §34.1 | lap124501 |
| 3.4 | "MCP single surface; pane; mixed harnesses; fifo fallback" | src:doc | target:§26 | lap124501 |
| 3.5 | "mint id per post and kid; inherit director's slot; different login" | src:doc | target:§27 | lap124501 |
| 3.6 | "full plugin" | src:doc | target:§28 | lap124501 |
| 3.7 | "directors vs parents vs kids; chain-launch; batch" | src:doc | target:§29, §34.2 | lap124501 |
| 3.8 | "pi 1.x now; deepseek flash; GLM; A/B with Claude keys" | src:doc | leaf:goal:g7.16.1.11.46.9 (P1) (L74) · was: §30, §34.3 | lap124501 |
| 3.9 | "tests: spiders in background; build vs repair loops" | src:doc | target:§31, §34.4 | lap124501 |
| 3.10 | "territories / smell walk / pre-determined choices" | src:doc | target:§32 | lap124501 |
| 3.11 | "run autonomously; provide keys" | src:doc | leaf:goal:g7.16.1.11.46.6 (C1) (L74) · was: §33, §36 | lap124501 |

**throws 4–7 (10-23)**
| # | atom (owner ask, short) | source | state | lap |
|---|---|---|---|---|
| 4.1 | "red-team = anti-fragile's; unify = all-is-one's; tune = alive's" | src:doc | target:§34.1 (flag: no council post named anti-fragile) | lap124501 |
| 4.2 | "GLM = the flash one" | src:doc | leaf:goal:g7.16.1.11.46.9 (P1) (L74) · was: §34.3 | lap124501 |
| 4.3 | "census: count tips; old versions as deprecated?" | src:doc | target:§34.5 (tips yes; versions are commits, not deprecated nodes) | lap124501 |
| 4.4 | "port the rest of the python safely" | src:doc | target:§34.6 | lap124501 |
| 5.1 | "posts, never seats; stand guard, never idle" | src:doc | target:§35 (V10 + the walk as idle state) | lap124501 |
| 6.1 | "service-account key in Doppler; workload identity later?; needed for batching?" | src:doc | leaf:goal:g7.16.1.11.46.6 (C1) (L74) · was: §36 (cannot mint keys; WIF = season 4; not needed for batching) | lap124501 |
| 6.2 | "automatic vs manual prompt caching" | src:doc | target:§36.3 | lap124501 |
| 7.1 | "optmem for the Prime; trajectory = momentum, optmem = state" | src:doc | leaf:goal:g7.16.1.11.46.2 (M1) (L74) · was: §37 (this ledger is M5) | lap124501 |

**added 10-23 (council V10a decision, alive 21:06Z)**
| # | atom (owner ask, short) | source | state | lap |
|---|---|---|---|---|
| 8.1 | "seat_status.py retire" | src:af6b174d9c507c5f812992fdd993b12b62b45da6 | target:the §34.5 census-cell leaf (wave 2) | lap124501 |
| 9.1 | "if a director has claimed a given goal leaf or hypothesis leaf or whatever or a bundle of them, let them get notice automatically via mail system that hey your bundle pre-req's have cleared and it's just a simple little unified system that is all wired into the data already available via the town board/trajectory and the post cards" | src:goal:g7.16.1.11.46.12#OWNER | leaf:goal:g7.16.1.11.46.12 (L78, director-goals-1) | lap124501 |
