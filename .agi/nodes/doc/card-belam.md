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
thought_session: belam-s3-VII
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED · ATOMS)"
town: core
---
# doc:card-belam — the Prime's card (encryption-town = this box, v5): the ONE scratch

Owner 09-23: the card is the handoff scratch and a doc node; `HANDOFF.md` + `.agi/sessions/quorum/belam.md` are symlinks to it. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; §0-§6 ≤ 100 lines; §7 ATOMS is bounded by time, not length (doc:brainstorm-unify §39). Skills: agi-rotate · agi-send · agi-merge-pass · agi-verify · agi-post · agi-town · agi-memory-guard · agi-node-write · agi-goal · agi-master-gate.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam-s3-IX live card, 12:5xZ 10-27. Gen VIII died at 22:10Z 10-26 of a FULL / (ENOSPC on transcript + /tmp task writes) right after its rotation card; the unit stayed hollow (strace parent of agi-run's loops kept MainPID alive, Restart never fired) until the Fable fork t-e4 restarted it on the owner's word at 12:43Z 10-27. So the OWNER's 00:00Z models2 order (o1) landed 12h51m LATE: L186 = W eacb63ba5a at 12:51:40Z + the narrow re-pin (h.conf == row 13/13). The memory held (card + SM's queue); the lander did not. Now landing the queue in SM's order: L187, L188 (the strand fix), the 16, the RULES tail.
<!-- THOUGHT:END -->

## §0 State (12:5xZ 10-27, belam-s3-IX; pin = eacb63ba5a)
| | |
|---|---|
| trunk | core/season3/main = MAIN = posts/belam = origin = eacb63ba5a (L186 W) at 12:51:40Z, then each queued L as landed (§2); the board's :23/:28 jobs MOVE posts/belam: land outside :20-:30 |
| pin | /etc/agi/carry.env AGI_TRUNK = eacb63ba5a11a63cc8edd5b7d2d59ce57982bb68 (NARROW re-pin 12:51:46Z 10-27; backup /var/backups/agi-act-20261027T125146Z/rollback.sh); /opt/agi/bin/verify-land = a HAND install, guard/verify-land.sh blob 931233448d59 |
| land script | /data/work/.scratch-agi-belam/land.sh N L GATETIP = the land step below, fail-closed per stage, links on the reused scratch tree $S/wtl; prints `LANDED ...` or `STOP N: <why>` |
| stall watch | /data/work/.scratch-agi-belam/stall/watch.sh (background, dies with this session): 11 active agi-post units, 0 claude > 60 s -> measure file + restart; log stall/watch.log |
| land step | `verify-land wrap L<n> LAND BASE GATETIP` -> `^land: ` (plain <L> / wrap <W>) -> `verify-land L<n> <that> BASE GATETIP` (rc 0 OK) -> links.py links on a scratch worktree under /data/work/.scratch-agi-belam -> box read (stop on mail) -> `git update-ref refs/heads/posts/belam <sha> BASE` -> `sudo -n -u belam git -C /data/work/agi merge --ff-only -q refs/heads/posts/belam` -> `git push -q origin <sha>:refs/heads/posts/belam <sha>:refs/heads/core/season3/main`; a HOLD lands only on the council's explicit word (L154, L177/L178) |
| re-pin | `sudo -n env PIN=<40-hex wrap sha> sh extensions/agi/bin/agi.sh host` (from ~/t at that sha); read-back: a 2nd run prints `host: met`; every /run/systemd/system/agi-post@<p>.service.d/h.conf `--model/--effort` == its row at the pin (13 on this box; director-thought-2 + stream-master are local-town: unread here); agi-project.path is inactive BY DESIGN, the act starts agi-project.service itself |
| me | uid agi-belam SIGNS and PUSHES; ~/.gitconfig loses the gh credential lines at each restart (skill agi-rotate); CHECK cron off |
| meter | compute by hand: newest usage in ~/.claude/projects/*/<session>.jsonl (input + cache_read + cache_creation) / 1e6; 0.41 = no new multi-ref act; 0.47 = rotate (L176's agi-meter is live only from a post's next start) |
| disk/mem | / 83% (9.8G free) at 12:45Z 10-27; a THIRD fill at 22:10Z 10-26 killed gen VIII (ENOSPC, writer unnamed); a full / kills agi-track and the harness: keep scratch on /data; slab refills ~1.5G/h: drop_caches at each memory-alarm warn |

## §1 Plan — goal:g7.16.1.11.46, the brainstorm in waves (one council brief per wave; the gate line passes before the next brief)
```
W0  me alone           doc node · §7 atoms · V0 · §6 banks                                               DONE 10-23
W1  council brief 1    M1-M4 (§37-§39 atoms tooling) · C1-C3 (§36 agi-cred, workspace cells, the header) · P1 (§30/§34.3 pi 1.x A/B)
                       · U1 (§7 scope report mode) · V10 (§35 AGI_[retired] -> AGI_POST: SM's mechanical leaf, not a council design)
    council brief 1b   §40 M6 chunk tap + store (mem: full / faces: cells) · M7 chunk->atom edge, agi-atom where, reply-names-its-ids red (W1's gate line unchanged)
    gate               M1-M4 + C1-C3 falsifiers pass; P1's four numbers on the board
W2  council brief 2    V1 refs/id/P · V2 cred piece (ONE post) · U3 MANIFEST scope/reach/at/pull/atoms · G1 compose/split (§25, §34.5)
                       · the age seal (§23, §34.6) · U6 move falls out · §40: V4 pulled forward (claude-code adapter only) · M9 summary tree · M10 owner quotes cite chunk ids
    gate               one rename end to end with 0 edits; one node's history only on its refs/grid/<mint>
W3  council brief 3    V3 root verbs + held lines · U2 certs enforced · U4 routes · spider families red/unify/tune · walk = idle
                       · two lanes (§34.4) · tests to region spiders (§31) · V8 grow-check + §G, python ports (§34.6) · §40 M8 reconcile walk as a unify-spider flow
    gate               a planted red found and fixed with no director turn; a held root action printed from the closed set
W4  council brief 4    U5 · U7 one plugin dir · U8 harness cells · §12 alphabet + agi-walk · V6 IOMap rows · V4's pi adapter (after P1) · V9 season-0 · C4 · C5
season 4 (out)         PQ signatures · numeric control surface · hardware alphabet · WIF per-kid tokens · income/streaming
```
Labels: §22 is the leaf table; "V3'" = new leaf G1 compose/split; "V7 (python out)" in §34.7/§36.4 = §22's V8.
Each minted leaf closes its §7 rows (state -> leaf:<goal id> | idea:<id> | decision:<line> | out:<reason>); board: intake/placed/red for belam.

## §2 Landed (gen IX, 10-27 12:43Z ..; gen VIII L164-L185 + L70-L163 = git history and the grid)
L186 W eacb63ba5a 12:51:40Z (the OWNER's models2, 12h51m late; wrap over SM 7742ad21e0). · L187 4a3a5a57c4 12:55:16Z (DG3 silent-rc-0, plain) · L188 W 5443847c58 12:58:51Z (DG2 agi-run strand = t-e4's gap (a); self-installs at each post's next start). · L189..L196 17cc9039e7 13:04:10Z (8 plain census lanes, one CAS ff). L197 HELD (home: /var/backups = system user backup's passwd home; false positive) -> asked the council 13:05Z: (a) land over it (my rec) or (b) re-cut; L198..L204 pre-read OK on their chain parents.
HOST ACTS: NARROW re-pin 12:51:46Z (pin eacb63ba5a; host: met; h.conf == row 13/13) · gh credential lines restored at wake (push dry-run OK).
## 🔴 Where it stops
belam-s3-IX is landing SM's queue in order: L186-L196 DONE; L197 waits on the council's word over its home HOLD (13:05Z ask; on (a): `land-chain.sh 197 204` needs a wrap-free path past the HOLD = land by hand per the council's word, then L198..L204 as one ff); then -> L205 f1-nspawn (RULES) -> L206 DG1 3b (RULES) -> L207 DG3 1d03fbb794 (RULES) -> L208 DG3 v5uid (plain) -> L209 SM own56 (RULES, LAST). SM re-cuts each on my new head after my [landed]; a land never runs inside :20-:30 (the board moves posts/belam: say 'trunk moved' and SM re-cuts).
Per L: `/data/work/.scratch-agi-belam/land.sh L<n> <held 40-hex> <gate tip>` -> `LANDED` line -> [landed] to SM (message file <<'EOF', `AGI_POST=belam box send sanctuary-master < file`). The 16 land as ONE CAS ff to L204 after verify-land on each.
THEN: (1) commit this card in a gap (never while a [merge-up] is pending: trap 136). (2) Two reds from t-e4 (the Fable fork, 12:4xZ) for owners: (a) a tracer with no harness must END the unit (agi-run's loops must not be children of the exec'd strace, or memguard's 'no harness under its tracer' ALERT restarts) = DG2, check L188 covers it; (b) a disk floor on / (ENOSPC killed the harness) = the memory-guard owner, no cell today. (3) The OWNER's two open asks (§6): the HOST ORDER batch of 40 and the per-post /data scratch dir. (4) L176 STARTS LEDGER + GATE297's g2/g3 owed reads (gen VII/VIII cards). (5) Stall watch stays until L188 is live at every post's next start.
NEXT COMMAND: `AGI_POST=belam AGI_BOX=encryption-town timeout 120 box read > /data/work/.scratch-agi-belam/mail.txt 2>&1; fold -s -w 220 /data/work/.scratch-agi-belam/mail.txt` (from ~/t; output via a /data file survives a full /).

## §4 Traps
- gen IX 12:4xZ: the restart again dropped ~/.gitconfig's gh credential lines (skill agi-rotate covers it; push failed 'could not read Username' until re-added).
- gen IX: a verify-land WRAP keeps L's tree: an L cut on an older trunk would revert the board commits in between -> every held L must have first parent == live posts/belam before the wrap (verify-land's parents line checks it).
- gen VII/VIII traps 136-143: moved into skills by L200 (traps-viii) in the queue; until it lands, `git show 54efadffea`.

## §5 Verification
L186: verify-land wrap -> `land: wrap eacb63ba5a over 7742ad21e0`; verify-land OK (parents 7e0c542ecd + 1b7425f328; R3 wrap tree = land tree; signers G belam / G sanctuary-master; D 0; anon-diff 0; anon-msg 0; r-land report 15 set, 0 would-refuse); links 5963 resolved / 0 broken on the W tree; MAIN = posts/belam = origin both refs = W (ls-remote). Re-pin: agi.sh host rc 0; 2nd run `host: met`; h.conf --model/--effort == posts.md row for 13/13 units on this box.

## §6 BANKED (owner-only; no council needed)
| item | recommendation |
|---|---|
| CLOSED 18:3xZ 10-25 (owner picks 18:25:37Z + chunk c:670f16229a2a): Doppler token for root = agi/dev rw service token in /etc/credstore/doppler-token (0600) | goal:g7.16.1.11.46.6 THOUGHT |
| CLOSED 18:3xZ 10-25 to C2's true size: the three lanes share the owner's workspace "agi" wrkspc_01F6D36dQiczWRCAEvea8FHC; per-lane spend/TPM caps NOT set: C2 reads 'passed with ONE shared workspace' until the owner says that is the intent | goal:g7.16.1.11.46.7 THOUGHT |
| Doppler tokens: owner 05:0xZ + 05:3xZ 10-26: "I wanted to leave it read and write for you but read only for everyone else." · "I have a read only token in the access project but can share it here as well." belam keeps its rw token. OPEN: root's /etc/credstore/doppler-token (read by the root agi-cred timer) is rw today | ASKED: never paste a token in chat (the box-local chunk store keeps chat unredacted, M6); put the read-only token in Doppler where my rw token reads it (e.g. agi/dev DOPPLER_RO_TOKEN), scoped to read agi/dev; then I swap root's credstore (one root act, agi-cred unchanged) |
| CLOSED owner 05:0xZ 10-26 (chat, to belam): R-LAND OWNER BATCH rows 3 + 4, verbatim "Accept both" | DG1 cuts the small r-land tip (relayed to SM 05:1xZ) |
| CLOSED owner 05:0xZ 10-26 (chat, to belam): WHO LANDS RULES = (1), verbatim "Yeah you can land but ideally over time rules become integrated into the matrix math": belam SIGNS the RULES land; the council shapes how my step makes/signs the land commit; 1141aef73b = a past one-off, no rewrite | relayed to SM 05:1xZ; atom c1 (rules into the matrix math) |
| CLOSED owner 05:0xZ 10-26 (chat, to belam): g7.33.18 HOLD LIFTED EXCEPT THE STREAM, verbatim "Lift it except for stream": the one-box memory-guard kit + encryption-town config are unheld; sanctuary-master activation was already live; stream-master + any stream stay held until messaging (goal:g7.32.6) | SM records it on goal:g7.33.18 (relayed 05:1xZ) |
| CLOSED owner 05:0xZ 10-26 (chat, to belam): ATOM 8.1 seat_status.py RETIRE, verbatim "Sure maybe we can retire Crons py as well soon if possible": move [R] (+[M]) to hierarchy.load_seats, drop [L]/[C] from both heads, retire the CLI row (DG3, .46.16) | relayed to SM 05:1xZ; atom c2 (crons.py retire: a reader census first) |
| / RED 15:37Z (95%): the 3 council seats' review fixtures in /tmp were ~2.4G of ~4G (alive [finding] 15:42:25Z; freed own files, / ~91%); DG2's census names the rest. BANK (alive + council): a per-post scratch dir on /data owned by each post uid (/data is belam:belam today, a post uid cannot write it) | YES, recommended: belam's host act, one `install -d -o agi-<p> -g agi-<p> -m 700 /data/scratch/<p>` per live post + TMPDIR in the unit; on your word |
| HOST ORDER BATCH (asked 19:1xZ 10-26): 40 grid mints whose origin version (09-19..09-29, before the 10-08 re-mint) is in NEITHER live's grid history NOR the trunk's history: 24 goal, 10 hypothesis, 4 doc, 2 build (39 node.md + 1 payload); live keeps its own tip; each diff in .agi/sessions/unify/20261026T184714Z-151412-0.batch (on disk only) | council's suggested batch rule: tree = LIVE for all 40, origin's diff kept in the stamped record (no content lost); unblocks `rejected 0` -> grid.py init |
| prime-director's org role | developer, unless the Admin cost reports (C4) need admin; then root only ever holds it |
| OpenRouter for P1: RESOLVED 06:1xZ 10-24. The owner topped up the OPENROUTER_ADMIN account ($33.44 left); .env's OPENROUTER_PROVISIONING_KEY now = Doppler agi/dev OPENROUTER_ADMIN (read on the box through ~belam/.config/sanctuary/doppler/agi-dev.rw), the old line kept in .env.before-or-admin-20261024 | the retry of the one kid-key waits on the council's go |
| CLOSED owner 05:3xZ 10-26 "Yes you can run crons py apply": prereq_notice enabled (8aa05a31dd) + `crons.py apply --root /data/work/agi --sudo` AS uid belam 05:38Z rc 0: agi-sanctuary-master 3 -> 4 lines (+prereq_notice */3); belam 11 + agi-belam 5 unchanged | notices live; SM's crontab sha f019.. -> fa0a5fb3d35f176d (F3 baseline) |
| CLOSED owner 05:3xZ 10-26: the credits org key = CLAUDE_CONSOLE_SP_KEY, verbatim "Yes it is a service provider key so it should be able to mint other keys. It is an org wide key that can do special stuff across orga and needs an org or workspace or whatever passed in. I think I meant workspace." (live via agi-cred since 10-25; every call sends anthropic-workspace-id; it can mint per-kid keys for P1) | relayed to SM; P1's credits arm can use it |
| R2: agi.sh rows() starts boot=false posts (TM, DT-1) on a first start | (b1) filter boot=false + recover=false in rows() — decide before F2 |
| R3: each agi-post@ start leaves settings.json 755; flags_ok wants 600 | R3a the unit chmods it 600; NO `agi.sh start` on the live town until ruled |
| §21 decisions still open: #1 identity = refs/id/P chain · #2 cred as a secret piece, one post first · #3 signatures only at the boundary set · #4 chain height over wall time · #5 mem: cell in OptChat's shape · #6 symbolic control surface · #8 root never loaned as a shell · #10 IOMap on the hypothesis, g2.2 active · #11 season-3 pick as a route exercise (your rows = thirds + rollover) | each as the doc recommends; council reviews #1-#4 in W2, #8 in W3. Ruled already: #7 in part (you made prime-director/prime-key in Doppler; the org link stays above) · #9 (§34.1 three spider families) · #12 (§39 atoms in the card) |
| V10b (the word sweep, later wave): the owner's §35 "No seat reference anywhere" vs SM's reading 10-23 (the whole-word grep hits 2152 files / 21165 lines; ~5937 are quote or owner-verbatim lines; ~30 node ids carry the word) | exclude owner-verbatim lines and closed records (complete/disproved/supported/retired), as deprecated/ is excluded; the owner's words are never rewritten (SM's recommendation, mine too; the council's [decision] follows). V10a (AGI_[retired] -> AGI_POST) goes ahead in W1 |
| §40 chunk store (brief 1b, M6): every owner utterance verbatim on refs/mem/<post>/- — pushed to the GitHub origin or box-local only? | box-local (excluded from every push refspec) until you rule; atoms + cited slices travel as today |
| M6 (.46.13, DG2 gap 4): a SECRET token typed into the chat is not redacted (a post uid cannot read the secrets source) — it sits as plaintext in the 0700 box-local store in my home, never travels | accept for now (0700, no remote, box-local), OR have a root-run redactor pass over the store; never paste a secret into the chat meanwhile |
| atom 2.19: Belam on Fable permanently | a posts.md row edit (model cell), your call |
| atom 4.1: "anti-fragile" read as self-perpetuating (no council post carries the name) | confirm, or name a fourth council post |
| .44.8 F2 + .44.7 live half: the next real fresh box | one event; both leaves close on it |
| /data/f1-nspawn-image (noble.tar) | remove once you confirm you read F1 |
| 657 refs/archive/worktrees/* in MAIN; refs/grid on E vs L differ | G1 compose/split (W2) settles the grid; keep until then |

## §7 ATOMS — the owner's 10-22/23 brainstorm (doc:brainstorm-unify), 62 rows; state = target into the doc until placed

**owner 10-26 20:27:57Z (chat, to belam) — timed model order**
| # | atom (owner ask, short) | source | state | lap |
|---|---|---|---|---|
| o1 | "ok at 8pm EDT or whatever (in about 3.5 hours) switch everyone other than yourself to opus 5.5 medium, and make the council be opus 5.5 extra. Leave yourself on opus 5.5 high. I'm testing how well the system will remember things like that." | src:chat 10-26 20:27:57Z (time confirmed 20:29:11Z) | CLOSED decision:L186 W eacb63ba5a 12:51:40Z 10-27 + re-pin (h.conf == row 13/13): LATE 12h51m (gen VIII died of a full / at 22:10Z; unit hollow until 12:43Z) | lap0 |

**throw 1 (10-22) — graph-interface design**
| # | atom (owner ask, short) | source | state | lap |
|---|---|---|---|---|
| 1.1 | "button down the graph-interface design" | src:doc | target:§0–§2 | lap124501 |
| 1.2 | "simplify / unify" | src:doc | leaf:goal:g7.16.1.11.46.21 (W2 L122) | lap124501 |
| 1.3 | "compare with matrix-skills" | src:doc | target:§1 (take O/check + api module; leave its engine) | lap124501 |
| 1.4 | "MCP auto-start" | src:doc | target:§6 (wake abstraction; start = visitor) · decision:§21-Part I #2 | lap124501 |
| 1.5 | "MCP push" | src:doc | target:§6/§26 (no push dependence; wake tool + fifo) | lap124501 |
| 1.6 | "filesystem-like MCP by post identity" | src:doc | target:§6 (resources = scope closure; visitor default) — thin, one line | lap124501 |
| 1.7 | "cross-compat CC / codex / grok / pi" | src:doc | target:§8, §26, §28 | lap124501 |
| 1.8 | "engine updates reach seeds without re-project" | src:doc | target:§4 (root fixpoint on the trunk ref) | lap124501 |
| 1.9 | "mathematical guardrails: scope/graph packs, parent/kid inheritance" | src:doc | leaf:goal:g7.16.1.11.46.21 (W2 L122) | lap124501 |
| 1.10 | "move tooling with fewer pieces" | src:doc | leaf:goal:g7.16.1.11.46.22 (W2 L122) | lap124501 |
| 1.11 | "matrix math for a Go port" | src:doc | target:§7 "Go: not now" (one algebra module, port only on latency) | lap124501 |
| 1.12 | "compare openrig / herdr / t3" | src:doc | target:§8 | lap124501 |

**throw 2 (10-23) — identity, memory, hashes, matrices, credits, root, season, income, projects, spiders, IOMap**
| # | atom (owner ask, short) | source | state | lap |
|---|---|---|---|---|
| 2.1 | "restore the Prime's session" | src:doc | leaf:goal:g7.16.1.11.46.1 (V0) · was: done (restore.sh; V0 leaf) | lap124501 |
| 2.2 | "credentials ride in a capsule / reuse the username slot" | src:doc | leaf:goal:g7.16.1.11.46.20 (W2 L122) | lap124501 |
| 2.3 | "identity = composable key over signed pieces, re-hashed on swap, continuity = the history" | src:doc | leaf:goal:g7.16.1.11.46.19 (W2 L122) | lap124501 |
| 2.4 | "optmem: Prime always; council/keep per season; directors per goal; parents/kids in optchat" | src:doc | target:§11 (`mem:` cell) · decision:§21 #5 · §37 (the ledger) | lap124501 |
| 2.5 | "fully hash-based ids, minimize public/private keys" | src:doc | target:§10 (boundary set B) · decision:§21 #3 | lap124501 |
| 2.6 | "daisy-chained hashes as the post's sense of time" | src:doc | target:§10 (time = chain/block height) · decision:§21 #4 — covered under other words | lap124501 |
| 2.7 | "each node a location in a matrix space; traversal = matrix op" | src:doc | target:§12 (words in, algebra in the engine) · §32 (graph distance is the coordinate) | lap124501 |
| 2.8 | "actions as vectors; mail as a vector" | src:doc | target:§12 (alphabet Σ, M_a) | lap124501 |
| 2.9 | "workflows ARE spawns ARE subagents ARE posts" | src:doc | leaf:goal:g7.16.1.11.46.21 (W2 L122) | lap124501 |
| 2.10 | "soft constraints: no hard cornering / teleportation" | src:doc | target:§12 (word length k, transition matrix T, phase bound Θ) | lap124501 |
| 2.11 | "a jev experience for all models" | src:doc | target:§12 (one line) — thin; g1.25 jev grammar is the owner of it | lap124501 |
| 2.12 | "can LLMs tolerate matrix-encoded control" | src:doc | target:§12 (no: never numbers in a prompt) · decision:§21 #6 | lap124501 |
| 2.13 | "use the $200/mo Console credits; batching" | src:doc | leaf:goal:g7.16.1.11.46.8 (C3) (L74) · was: §13, §36 · decision:§21 #7 · leaves C1–C5 | lap124501 |
| 2.14 | "batch-spawn parents/kids" | src:doc | target:§13, §29 (only `pull: none` steps batch) | lap124501 |
| 2.15 | "headless pi, cheap on memory" | src:doc | leaf:goal:g7.16.1.11.46.9 (P1) (L74) · was: §30 (P1) | lap124501 |
| 2.16 | "Fable sparingly for council reviews" | src:doc | target:§13/§30 (a `plan`/review step model) — thin | lap124501 |
| 2.17 | "loan root to SM (graph moves) and council (unanimous)" | src:doc | target:§14 · decision:§21 #8 | lap124501 |
| 2.18 | "report why a root action was withheld" | src:doc | target:§14 (closed set of held lines) | lap124501 |
| 2.19 | "Belam to Fable permanently; bother the owner only at thirds/rollover" | src:doc | target:decision:§21 #11 (rows = thirds + rollover) — Fable-permanent is a posts.md row edit, owner's call | lap124501 | chunks: c:24a0f5a4719c |
| 2.20 | "let the season close independently, picking from this brainstorm + horizon goals" | src:doc | target:§15 · decision:§21 #11 | lap124501 |
| 2.21 | "self-improve" | src:doc | target:folded:§34.1 tune + §19 IOMap loop (was dropped; caught by §37's grep) | lap124501 |
| 2.22 | "live-stream its own progress; interactive games for income" | src:doc | target:deferred:season 4 (§20 dependencies) | lap124501 |
| 2.23 | "stream-master with optchat/optmem always on" | src:doc | target:§11 (`mem: always` row) + §20 | lap124501 |
| 2.24 | "animated avatars via mystudio.fun; grant; hold tokens for credits" | src:doc | target:§20 (mystudios.fun = reseller, no avatar product; treasury = owner) | lap124501 |
| 2.25 | "a second subscription for split logins" | src:doc | leaf:goal:g7.16.1.11.46.20 (W2 L122) | lap124501 |
| 2.26 | "import other projects; let others use the system; season 0→1 as init" | src:doc | target:§16 (season-0 capsule) — one section, thin on "others use it" | lap124501 |
| 2.27 | "replace grow.py / links.py with shell or chain checks; auto-written links" | src:doc | leaf:goal:g7.16.1.11.46.15 (W2 L122) | lap124501 |
| 2.28 | "self-summarizable graph via optmem/optchat per chain" | src:doc | target:§11 (store = node tree; brief = recall) | lap124501 |
| 2.29 | "spiders crawl / test / fix / launch ideas; no more gating or waiting" | src:doc | target:§18, §31, §32, §34 · decision:§21 #9 | lap124501 |
| 2.30 | "IOMap goal: shapes before build; primitive transport; lower-level / inverse abstractions later" | src:doc | target:§19 · decision:§21 #10 · deferred:season 4 (inverse/assembly) | lap124501 |
| 2.31 | "some parts can wait till season 4 (lower-level matrix)" | src:doc | target:§15 (season-4 list) | lap124501 |

**throw 3 (10-23) — the ten reading questions**
| # | atom (owner ask, short) | source | state | lap |
|---|---|---|---|---|
| 3.1 | "retire the python; only keygen/hashing left?" | src:doc | leaf:goal:g7.16.1.11.46.15 (W2 L122) | lap124501 |
| 3.2 | "one spawn/dispatch path; pull setting" | src:doc | leaf:goal:g7.16.1.11.46.21 (W2 L122) | lap124501 |
| 3.3 | "grid monolith, node = branch, post = slice; spiders under council; red-team" | src:doc | leaf:goal:g7.16.1.11.46.18 (W2 L122) | lap124501 |
| 3.4 | "MCP single surface; pane; mixed harnesses; fifo fallback" | src:doc | target:§26 | lap124501 |
| 3.5 | "mint id per post and kid; inherit director's slot; different login" | src:doc | leaf:goal:g7.16.1.11.46.19 (W2 L122) | lap124501 |
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
| 4.3 | "census: count tips; old versions as deprecated?" | src:doc | leaf:goal:g7.16.1.11.46.16 (W2 L122) | lap124501 |
| 4.4 | "port the rest of the python safely" | src:doc | leaf:goal:g7.16.1.11.46.15 (W2 L122) | lap124501 |
| 5.1 | "posts, never seats; stand guard, never idle" | src:doc | target:§35 (V10 + the walk as idle state) | lap124501 |
| 6.1 | "service-account key in Doppler; workload identity later?; needed for batching?" | src:doc | leaf:goal:g7.16.1.11.46.6 (C1) (L74) · was: §36 (cannot mint keys; WIF = season 4; not needed for batching) | lap124501 |
| 6.2 | "automatic vs manual prompt caching" | src:doc | target:§36.3 | lap124501 |
| 7.1 | "optmem for the Prime; trajectory = momentum, optmem = state" | src:doc | leaf:goal:g7.16.1.11.46.2 (M1) (L74) · was: §37 (this ledger is M5) | lap124501 |

**added 10-23 (council V10a decision, alive 21:06Z) — not a brainstorm throw: unregistered in the trajectory on purpose (council R4, 10-25)**
| # | atom (owner ask, short) | source | state | lap |
|---|---|---|---|---|
| 8.1 | "seat_status.py retire" | src:af6b174d9c507c5f812992fdd993b12b62b45da6 | leaf:goal:g7.16.1.11.46.16 (W2 L122) · census DG3 02:3xZ 10-26 -> owner question §6 | lap124501 | chunks: c:0b2518f4f58f c:79cf930cf587 c:c747715b5f42 c:8de9f5733c32 c:24a0f5a4719c |
| 9.1 | "if a director has claimed a given goal leaf or hypothesis leaf or whatever or a bundle of them, let them get notice automatically via mail system that hey your bundle pre-req's have cleared and it's just a simple little unified system that is all wired into the data already available via the town board/trajectory and the post cards" | src:goal:g7.16.1.11.46.12#OWNER | leaf:goal:g7.16.1.11.46.12 (L78, director-goals-1) | lap124501 | chunks: c:24a0f5a4719c |

**added 10-24 (owner 07:2xZ) — not a brainstorm throw: unregistered in the trajectory on purpose (council R4, 10-25)**
| # | atom (owner ask, short) | source | state | lap |
|---|---|---|---|---|
| a1 | "Retire write py for sure we don’t need it at all and need to retire that whole build node as the capsule wrapper now tags everything for us using standard read routes" | src:goal:g7.16.1.11.46#OWNER | leaf:goal:g7.16.1.11.46.23 (W2 L122) | lap124501 |
| a2 | "We need to redo the renderer if needed to be a git based graph system that uses the minimal shell code matrix integrated design" | src:goal:g7.16.1.11.46#OWNER | leaf:goal:g7.16.1.11.46.18 (W2 L122) | lap124501 |

**added 10-25 (owner 18:4xZ) — not a brainstorm throw: unregistered in the trajectory on purpose**
| # | atom (owner ask, short) | source | state | lap |
|---|---|---|---|---|
| b1 | "we're trying to see how to best compose using the claude console with the openrouter models to create a system optimized for high-speed failure analysis and healing" | src:owner 18:4xZ 10-25 (chat) | idea:g7161146-b1-console-openrouter-failure-healing (council R1 18:45Z; the W3 brief cites it) | lap124510 |

**added 10-26 (owner 05:0xZ, chat) — not a brainstorm throw**
| # | atom (owner ask, short) | source | state | lap |
|---|---|---|---|---|
| c1 | "ideally over time rules become integrated into the matrix math" | src:owner 05:0xZ 10-26 (chat) | target:§12 (alphabet / M_a) + W4 §12 line; relayed to SM 05:1xZ | lap124510 |
| c2 | "maybe we can retire Crons py as well soon if possible" | src:owner 05:0xZ 10-26 (chat) | relayed to SM 05:1xZ: a reader census (the seat_status shape) before any leaf | lap124510 |

**throw 10 (10-24) — §40 the owner-facing post: full memory beside the atoms (the fork's throw 8, renumbered on intake)**
| # | atom (owner ask, short) | source | state | lap |
|---|---|---|---|---|
| 10.1 | "the owner-facing post gets a full optmem/chat memory beside the atoms (via pi-optchat or UniiChat if needed)" | src:doc | leaf:goal:g7.16.1.11.46.24 (W2 L122) (the adapter half; the store half = .46.13) | lap124503 |
| 10.2 | "every chunk is marked to an atom; several chunks map to one atom (the owner asking, the agent acknowledging)" | src:doc | leaf:goal:g7.16.1.11.46.14 | lap124503 |
| 10.3 | "the post relays any atoms missing vs its memories to the Prime, periodically" | src:doc | target:§40 M8 walk check 1 + one batched atoms: relay per lap (W3) | lap124503 |
| 10.4 | "the post can say: you asked X at this day/time; recorded here, being worked on / not transferred yet, marked for the spiders" | src:doc | leaf:goal:g7.16.1.11.46.14 | lap124503 |
| 10.5 | "a spider carries out these routine cross-updates" | src:doc | target:§40 M8 unify-spider pass, four checks (W3) | lap124503 |
| 10.6 | "classifiers via openrouter or our own; otherwise cheap haiku/sonnet" | src:doc | target:§40 tiers: tier 1 Haiku/Sonnet now (M7 atomizer cell), P1 = the openrouter arm; tiers 2-3 season 4 | lap124503 |
| 10.7 | "UniiChat only if it lets me use my own keys" | src:doc | target:§40 import-only; any third-party harness gets a workspace-scoped key (C2/C3) | lap124503 |
| 10.8 | "mark it full memory enabled so non-owner-facing posts can have it; the Prime always" | src:doc | leaf:goal:g7.16.1.11.46.13 | lap124503 |
