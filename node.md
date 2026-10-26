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
thought_session: belam-s3-VI
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED · ATOMS)"
town: core
---
# doc:card-belam — the Prime's card (encryption-town = this box, v5): the ONE scratch

Owner 09-23: the card is the handoff scratch and a doc node; `HANDOFF.md` + `.agi/sessions/quorum/belam.md` are symlinks to it. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; §0-§6 ≤ 100 lines; §7 ATOMS is bounded by time, not length (doc:brainstorm-unify §39). Skills: agi-rotate · agi-send · agi-merge-pass · agi-verify · agi-post · agi-town · agi-memory-guard · agi-node-write · agi-goal · agi-master-gate.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam-s3-VI 01:0xZ 10-26 (wake 00:52Z): ~/.gitconfig credential lines re-added (the skill's trap, again); L139 landed (DG2 atomize lane fix).
belam-s3-V rotation card, 00:5xZ 10-26 (meter at the line): L124-L138 landed this generation; agi-cred went LIVE (S1 S2 Row 1+1' K', L132r, the read under env -i after two council HOLDs); verify-land moved into the repo and is INSTALLED (L136, /opt/agi/bin/verify-land, every land now ends OK rc 0 or HOLD rc 1); age installed after SEAL (L134); census fix L138 meets the legacy-retire hold. gen IV traps 124/126/128 moved to agi-send + agi-merge-pass, 125/127 dropped.
belam-s3-V 13:5xZ 10-24: the Fable fork handed back §40: doc:brainstorm-unify §40+§8f appended, goal .46 waves + count 74, §1 brief 1b / W2 / W3 / W4 lines, §7 throw 10.
<!-- THOUGHT:END -->

## §0 State (00:5xZ 10-26, at belam-s3-V's rotation; pin = 946888334f)
| | |
|---|---|
| trunk | core/season3/main = MAIN's checkout = posts/belam = origin; the :28 board job auto-lands my town:local-maxxing commits (it can move the trunk between my verify and my CAS: then ask SM to re-cut) |
| pin | /etc/agi/carry.env AGI_TRUNK = 946888334f (00:0xZ 10-26, L136; 7acb2c1bdd at 21:3xZ (L132r); 60faead1a5 at 19:5xZ (L127); 3138d08b8e at 19:1xZ, before that 6a4c10bf00, before that d751329195 (owner GO 20:0xZ 10-24 "get dr to have the boot pin true"; `agi.sh host` at that pin 20:10Z, rc 0, host: met; backup + rollback /var/backups/agi-act-20261024T201036Z). Dry run first: the pin's projection differed from /run ONLY by the agi-post@director-review wants link; every root piece and post unit byte-equal. Boot set = 11 posts, director-review included |
| me | uid agi-belam SIGNS and PUSHES; after a reboot ~/.gitconfig loses the credential lines (re-add '' + the belam gh helper); I mail SM only; keepalive timer RE-ENABLED 23:14Z 10-23 (the owner saw RC sessions archived after the idle stretch; its first run renamed 6 posts' RC titles back to the post name and pinged all-is-one 15 min from token expiry); CHECK cron still off; box-wake still types `mail: box read` |
| accounts | owner 17:2xZ 10-24: the 10 other posts here (alive, all-is-one, self-perpetuating, sanctuary-master, director-goals-1, director-science-1, director-general-1/2/3; director-review started by hand 18:3xZ, boot=true from the 20:10Z pin move) are logged into the owner's ALTERNATE Max account (17:24-18:4xZ, /login typed into each idle post's fifo, the owner pasted each code; /remote-control <post> re-titled); their RC sessions show in THAT account's app. belam stays on the main account. A re-login = the same fifo route, idle posts only, one at a time. The box's environment encryption-town = the belam LOGIN user's `claude remote-control` user unit: logged out since the 10-23 reboot, re-logged 20:48Z on the MAIN account; agi-rc-keepalive now gives that user one headless haiku turn within 300 s of expiry (owner 20:5xZ "Let's extend the keep alive"; log lines `rc-user belam:`) |
| fork | the Fable fork (tmux belam-fable, scope agi-belam-fable-2, RC belam-fable) is DONE; V0 is LIVE, so my restart resumes ~/.session's id, never the fork |
| intake | §7: 74 rows (62 brainstorm src:doc + 8.1 + 9.1 + a1/a2 = the owner's 07:2xZ write.py/renderer ruling + 10.1-10.8 = §40, handed back by the fork 13:5xZ 10-24); placed 12 (10.2 10.4 10.8 -> .46.13/.46.14, council 14:0xZ) |
| landing my commits | `AGI_POST=belam ~/bin/agi-at <paths>` (signs onto posts/belam) -> `sudo -n -u belam git -C /data/work/agi merge --ff-only -q refs/heads/posts/belam` -> push to core/season3/main + posts/belam; commit my card ONLY right after landing an SM cut, and mail SM the new tip |
| landing SM's L<n> | `verify-land L<n> LAND BASE GATETIP` (installed, /opt/agi/bin; must end `verify-land: OK`, rc 0), links on its own tree, CAS posts/belam, ff MAIN, push both, `git checkout -q --detach` |

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
MINE in W1: the P1 mint step (`p1_ab.py kid-key ARM LEAF --kid-uid N --keydir D --ledger L`, then `kid-done`) ONLY at DG3's explicit request AND after DG3's R1-R4 tip is on the trunk with every P0 item written down; STOP after the g7.31.3.1 smoke for ONE [result]; an unexpected guard = HALT + [red] to SM, never a retry (council, L89 03:38Z). Council 7f0640e29b: ≤ 15 keys (5 frozen leaves x 3 arms; 2 openrouter arms = 10), each $0.50 cap + a non-null expires_at, both read back; one 0600 file per key in a belam-owned 0700 dir, ACL file u:<kid uid>:r + dir u:<kid uid>:x; never in a repo/ref/mail/argv/env; disabled + read back + file removed at arm end. C1 root install DONE 02:31Z 10-24 on L87 e801e96a92: /opt/agi/bin/agi-cred (2832 B) + agi-cred.service + .timer (5 min), first run success, check 'posts 10 pids 190 read 190 gone 0 key-hits 0'; /etc/credstore empty (credits_live false). Rollback: `systemctl disable --now agi-cred.timer; rm /opt/agi/bin/agi-cred /etc/systemd/system/agi-cred.{service,timer}; daemon-reload`.
Each minted leaf closes its §7 rows (state -> leaf:<goal id> | idea:<id> | decision:<line> | out:<reason>); board: intake/placed/red for belam.

## §2 Landed (this generation, 10-25 19:1xZ .. 10-26 00:4xZ; L70-L123 = git history and the grid)
L124 3138d08b8e (b1 idea + .46.6-.8 Row 1) · L125 09ae297ed2 (DG1 V8a 1) · L126 96ae91aa6f (DG2 cite) · L127 60faead1a5 (mine: agi-cred.service HOME=/root) · L128 acfadaeaef (DG2 horizons + cite heading) · L129 699a8e2630 (DG1 V8a 2a) · L130 9b24838409 (DG1 census v2 doc) · L131 ac375ee636 (DG2 V-1..V-3) · L132r 7acb2c1bdd (mine: agi-cred S1 env -i, S2, Row 1+1', K') · L133 7e8bb822d3 (DG2 close .46.24 .46.26) · L134 c510be7ca5 (DG3 SEAL) · L135 ed0b5743df (DG2 M10 row a + meter fix) · L136 946888334f (mine: VL C1-C6, verify-land into the repo) · L137 a0059fed5a (DG1 V8a 2b re-cut 4; first land under the installed verify-land) · L138 c697a5b9bc (DG3 census re-cut) · L139 b3b71f9ac0 (DG2 agi-atomize lane fix, belam-s3-VI).
HOST ACTS: pin moved 6a4c10bf00 -> 3138d08b8e -> 60faead1a5 -> 7acb2c1bdd -> 946888334f (each `agi.sh host` rc 0, host: met, backups /var/backups/agi-act-*). agi-cred + unit from the pin: claude-sp written 0600 (19:5xZ 10-25), unchanged since; key-hits 0. age 1.1.1-1ubuntu0.24.04.3 (apt, after L134). /opt/agi/bin/verify-land (L136 pin blob 184fea25), ~/tools/verify-land.sh -> .retired. agi-mem reinstalled after L126/L128/L131/L135 (cite 1 new / 0 violations).
## 🔴 Where it stops
belam-s3-VI seated: nothing in flight; land SM's next cuts with the installed verify-land.
01:0xZ 10-26. trunk = MAIN = posts/belam = origin after this card; pin 946888334f; no tip of mine at SM's gate.
OPEN, in order: (1) SM's queue: DG1 2c report mode (GATE259), DG1 3a re-cut (removes g17_1_note: my no-veto 00:3xZ; goal:g17.1 = goal:g7.16 since da2edb3f9e), DG3 legacy-retire follow-on (L138 met the council hold; it carries two binding rows), director-goals-1 memguard leaf .40.1.2 (alive 00:49:43Z: ALERT on the 2nd consecutive no-harness tick of a live tracer, no InvocationID read; the pending set clears when the harness is found or the cgroup empties, that cleared case RECORDED non-red as a stop window; I answered 00:5xZ: the g7.33.18 HOLD covers that leaf's WORK, not the file -> cut). Land each: `verify-land L<n> LAND BASE GATETIP` (installed; must end `verify-land: OK`, rc read BARE), links on the land tree, CAS posts/belam, ff MAIN, push both; every [landed] quotes the `self: = the pin's blob (...)` line, no RED. (2) After .40.1.2 lands: the live memguard install = MY re-stage host act at a quiet hour (council). (3) R-land owner batch in §6 waits the owner's word. (4) The age agi-out + new agi-mem reach each post at its next start (pin 946888334f); first start seen clean (self-perpetuating 00:44Z, no out-refused). (5) W2 leaves .46.15-.46.26 continue; credits: ONE shared workspace, an org-scoped key MUST send anthropic-workspace-id.
NEXT COMMAND: `AGI_POST=belam AGI_BOX=encryption-town timeout 120 box read | fold -s -w 220` (from ~/t). Body on STDIN for box send; anonymize first.

## §4 Traps (this gen 129-132; gen IV 124/126/128 moved to agi-send + agi-merge-pass at this rotation, 125/127 dropped)
| # | trap | rule |
|---|---|---|
| 129 | my L127 [landed] said "derive check RED rc 0": the rc was `tail`'s, read through a pipe (council R-rc) | an rc is read BARE (`cmd >/dev/null; echo rc=$?`), never through a pipe or wrapper |
| 130 | agi-cred S1 passed SM's gate on a GREP of the scoped line; the unit's env pair, then GIT_CONFIG_PARAMETERS / GIT_DIR / GIT_OBJECT_DIRECTORY / GIT_NAMESPACE still reached the root read (alive HOLD x2) | a "scoped / refused / cancels" claim gets a hostile-input lane (every inherited source at once) + one mutant per guard, never a grep |
| 131 | VL C1-C5 were returned at GATE255: grid-writers C7 pins every `git fetch` site and verify-land.sh:9 was a new one | any tip that adds a git call runs test_grid_writers.py on a scratch merge with the live trunk BEFORE it is sent |
| 132 | my [note] called memguard ALERT 6adea244 a restart-window transient; it was TRUE: the stop side of self-perpetuating's v5 rotation (harness gone at `kill $PPID`, 33 s before the restart; alive + aio measured) | before calling an alert a transient, read the post's rotation record (its [rotation-alert] commit, ~/.fresh) and the guard's existing skips |

## §5 Verification
10-26 L137/L138: the INSTALLED verify-land, bare rc 0, `self: = the pin's blob (184fea259339)`, no RED; links 5960 resolved 0 broken on each land tree. verify-land.t.sh 17/17 (C5), agi-cred.t.sh 65/0, grid-writers 27/0 on a scratch merge before sending VL C6.
10-25 L132r host act: agi-cred start rc 0, key-hits 0, claude-sp sha + mtime unchanged; root doppler dir names only: /root/.doppler 700 + .doppler.yaml 600 (10-09), 0 key/token bytes.

## §6 BANKED (owner-only; no council needed)
| item | recommendation |
|---|---|
| CLOSED 18:3xZ 10-25 (owner picks 18:25:37Z + chunk c:670f16229a2a): Doppler token for root = agi/dev rw service token in /etc/credstore/doppler-token (0600) | goal:g7.16.1.11.46.6 THOUGHT |
| CLOSED 18:3xZ 10-25 to C2's true size: the three lanes share the owner's workspace "agi" wrkspc_01F6D36dQiczWRCAEvea8FHC; per-lane spend/TPM caps NOT set: C2 reads 'passed with ONE shared workspace' until the owner says that is the intent | goal:g7.16.1.11.46.7 THOUGHT |
| Doppler token for root is agi/dev READ-WRITE (your pick of the '(Recommended)' option, 18:25:37Z); agi-cred only READS CLAUDE_CONSOLE_SP_KEY, and an rw token in root's credstore can rewrite every agi/dev secret (council Row 3, aio, alive [decision] 18:56:18Z 10-25) | RECOMMEND: mint a read-only service token scoped to agi/dev in the Doppler dashboard and swap /etc/credstore/doppler-token, one root act on your GO; agi-cred needs no change |
| R-LAND OWNER BATCH (council 3/3 alive 23:12:35Z 10-25; table doc:r-land-report-table 4868e494bd on DG1's post branch, goal:g7.16.1.11.46.23): two grants in .agi/context/schemas/[config].md (RULES, r=owner). Row 3: add `engine` to sanctuary-master's actor_rows fields (S23 rollover set it on 14 rows). Row 4: {actor: sanctuary-master, list_key: posts, ops: [create], retire_copy: true}: a `<X>-retired` create is admitted only if <X> is retired in the SAME commit, the process cells take FIXED values {name, session_label = new name, boot null, box off, worktree "", session_name "", window "", pid 0, recover false}, and every other cell (pubkey, key_history, sig/enc scheme, session_id, role, tier...) equals <X>'s at the parent; DG1 cuts the small r-land tip only on your yes (mutants: lone -retired; pubkey/key_history differ; box != off or recover true or pid != 0; <X> still live -> refused; the real 7c1ef3664f AND b737cef238 replayed -> ADMITTED; clause (c) settled alive 23:14:35Z). One-offs get NO grant: such a cell change lands as SM's/belam's own commit with a `row-for:` line | RECOMMEND accept both (the two repeating flows; the council's shape, measured on the real moves) |
| g7.33.18 HOLD (owner 21:1xZ 09-26 via the Prime: "encryption-town config, sanctuary-master activation and stream-master are ALL on hold -- no stream until messaging (goal:g7.32.6) is done") | sanctuary-master is active since and the guard runs live here; I ruled 00:5xZ 10-26 it holds the kit ROLLOUT + stream, not the template file. RECOMMEND: say whether the hold still stands (or lift it except the stream) |
| prime-director's org role | developer, unless the Admin cost reports (C4) need admin; then root only ever holds it |
| OpenRouter for P1: RESOLVED 06:1xZ 10-24. The owner topped up the OPENROUTER_ADMIN account ($33.44 left); .env's OPENROUTER_PROVISIONING_KEY now = Doppler agi/dev OPENROUTER_ADMIN (read on the box through ~belam/.config/sanctuary/doppler/agi-dev.rw), the old line kept in .env.before-or-admin-20261024 | the retry of the one kid-key waits on the council's go |
| the prereq_notice cron row (goal .46.12, L94, user agi-sanctuary-master) is DARK until a `crons.py apply --sudo` | the owner's GO; then the notices run each trunk move (SM seeded refs/notices/prereq/seen at L94) |
| link the Console org that carries the $200/mo credits (§13, §36) | link now (the credits expire monthly); the credits arm of P1 needs it |
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
| 2.19 | "Belam to Fable permanently; bother the owner only at thirds/rollover" | src:doc | target:decision:§21 #11 (rows = thirds + rollover) — Fable-permanent is a posts.md row edit, owner's call | lap124501 |
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
| 8.1 | "seat_status.py retire" | src:af6b174d9c507c5f812992fdd993b12b62b45da6 | leaf:goal:g7.16.1.11.46.16 (W2 L122) | lap124501 |
| 9.1 | "if a director has claimed a given goal leaf or hypothesis leaf or whatever or a bundle of them, let them get notice automatically via mail system that hey your bundle pre-req's have cleared and it's just a simple little unified system that is all wired into the data already available via the town board/trajectory and the post cards" | src:goal:g7.16.1.11.46.12#OWNER | leaf:goal:g7.16.1.11.46.12 (L78, director-goals-1) | lap124501 |

**added 10-24 (owner 07:2xZ) — not a brainstorm throw: unregistered in the trajectory on purpose (council R4, 10-25)**
| # | atom (owner ask, short) | source | state | lap |
|---|---|---|---|---|
| a1 | "Retire write py for sure we don’t need it at all and need to retire that whole build node as the capsule wrapper now tags everything for us using standard read routes" | src:goal:g7.16.1.11.46#OWNER | leaf:goal:g7.16.1.11.46.23 (W2 L122) | lap124501 |
| a2 | "We need to redo the renderer if needed to be a git based graph system that uses the minimal shell code matrix integrated design" | src:goal:g7.16.1.11.46#OWNER | leaf:goal:g7.16.1.11.46.18 (W2 L122) | lap124501 |

**added 10-25 (owner 18:4xZ) — not a brainstorm throw: unregistered in the trajectory on purpose**
| # | atom (owner ask, short) | source | state | lap |
|---|---|---|---|---|
| b1 | "we're trying to see how to best compose using the claude console with the openrouter models to create a system optimized for high-speed failure analysis and healing" | src:owner 18:4xZ 10-25 (chat) | idea:g7161146-b1-console-openrouter-failure-healing (council R1 18:45Z; the W3 brief cites it) | lap124510 |

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
