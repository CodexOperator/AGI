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
belam post-rotation 21:1xZ 10-25: L124-L130 landed; R-rc corrected (bare rc 1; my 'rc 0' was tail's); agi-cred S1 S2 Row 1+1' K' authored; alive HELD d31e8c9b18 (my s1 was a grep; the unit's env pair still admitted '*') -> re-tip 787713baae, then the council's class fix: the read under env -i = tip cred-rows-envi f62e072220; H1 DONE: the first live start failed closed rc 5 (doppler needs HOME under systemd), fixed by L127 (HOME=/root), re-pinned 60faead1a5, agi-cred wrote claude-sp 0600, key-hits 0: .46.3's live leg is STARTED.
belam-s3-V 13:5xZ 10-24: the Fable fork handed back §40 (owner: "hand off the updates to be incorporated into plan"): doc:brainstorm-unify §40+§8f appended, goal .46 waves + count 74, §1 brief 1b / W2 / W3 / W4 lines, §7 throw 10 (the fork's throw 8 renumbered). L101-L105 landed this generation.
belam-s3-IV rotation card, 07:3xZ 10-24 (meter at the line): W1 of the brainstorm ran end to end overnight (L74-L100, 27 lands); the owner topped up OpenRouter, the provisioning key moved to OPENROUTER_ADMIN, P1's first key is minted and waits for its kid-done; the owner ruled write.py retired. gen III traps 121-123 moved into skills.
belam-s3-IV, 10-23 after the owner's hand-off of the Fable brainstorm: §7 ATOMS is new (§39: the owner's asks live in the card, not a second node), 62 rows from the fork's ledger (its header says 60; the tables hold 62). Wave 0 done by the Prime alone: doc:brainstorm-unify (reference), goal:g7.16.1.11.46 (the umbrella) + .46.1 V0 (complete), the owner-only asks banked in §6. Since the last card: L70-L73 landed, F1 nspawn ran (FAIL, 3 causes, R2/R3 banked), the box rebooted 03:45Z, keepalive + CHECK cron off by the owner's word.
<!-- THOUGHT:END -->

## §0 State (21:1xZ 10-25; pin = 60faead1a5)
| | |
|---|---|
| trunk | core/season3/main = MAIN's checkout = posts/belam = origin; the :28 board job auto-lands my town:local-maxxing commits (it can move the trunk between my verify and my CAS: then ask SM to re-cut) |
| pin | /etc/agi/carry.env AGI_TRUNK = 60faead1a5 (19:5xZ 10-25, L127; 3138d08b8e at 19:1xZ, before that 6a4c10bf00, before that d751329195 (owner GO 20:0xZ 10-24 "get dr to have the boot pin true"; `agi.sh host` at that pin 20:10Z, rc 0, host: met; backup + rollback /var/backups/agi-act-20261024T201036Z). Dry run first: the pin's projection differed from /run ONLY by the agi-post@director-review wants link; every root piece and post unit byte-equal. Boot set = 11 posts, director-review included |
| me | uid agi-belam SIGNS and PUSHES; after a reboot ~/.gitconfig loses the credential lines (re-add '' + the belam gh helper); I mail SM only; keepalive timer RE-ENABLED 23:14Z 10-23 (the owner saw RC sessions archived after the idle stretch; its first run renamed 6 posts' RC titles back to the post name and pinged all-is-one 15 min from token expiry); CHECK cron still off; box-wake still types `mail: box read` |
| accounts | owner 17:2xZ 10-24: the 10 other posts here (alive, all-is-one, self-perpetuating, sanctuary-master, director-goals-1, director-science-1, director-general-1/2/3; director-review started by hand 18:3xZ, boot=true from the 20:10Z pin move) are logged into the owner's ALTERNATE Max account (17:24-18:4xZ, /login typed into each idle post's fifo, the owner pasted each code; /remote-control <post> re-titled); their RC sessions show in THAT account's app. belam stays on the main account. A re-login = the same fifo route, idle posts only, one at a time. The box's environment encryption-town = the belam LOGIN user's `claude remote-control` user unit: logged out since the 10-23 reboot, re-logged 20:48Z on the MAIN account; agi-rc-keepalive now gives that user one headless haiku turn within 300 s of expiry (owner 20:5xZ "Let's extend the keep alive"; log lines `rc-user belam:`) |
| fork | the Fable fork (tmux belam-fable, scope agi-belam-fable-2, RC belam-fable) is DONE; V0 is LIVE, so my restart resumes ~/.session's id, never the fork |
| intake | §7: 74 rows (62 brainstorm src:doc + 8.1 + 9.1 + a1/a2 = the owner's 07:2xZ write.py/renderer ruling + 10.1-10.8 = §40, handed back by the fork 13:5xZ 10-24); placed 12 (10.2 10.4 10.8 -> .46.13/.46.14, council 14:0xZ) |
| landing my commits | `AGI_POST=belam ~/bin/agi-at <paths>` (signs onto posts/belam) -> `sudo -n -u belam git -C /data/work/agi merge --ff-only -q refs/heads/posts/belam` -> push to core/season3/main + posts/belam; commit my card ONLY right after landing an SM cut, and mail SM the new tip |
| landing SM's L<n> | `~/tools/verify-land.sh L<n> LAND BASE GATETIP`, links on its own tree, CAS posts/belam, ff MAIN, push both, `git checkout -q --detach` |

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

## §2 Landed (10-22 .. 10-24)
L101 3de19a2732 07:31Z 10-24 (dg1 C-2 + C-3, goal:g7.16.1.11.13.4: crons.py apply makes 0 sudo calls without --sudo; the sudo path refuses temp/suite projects): D1 (1)(2)(3) PASS, [landed] sent.
L102 866d194ec5 07:42Z (dg1 O2: 61 goals -> horizon, 7 retired, 1 hypothesis retired): links 0 broken, nodes 5961 = 5961 (dep +1), board reader dead/unreachable/unparsed 0, red only lag>60min. L103 fad4c67fb6 07:50Z (DG3 (b): p0 g n/a from a keyless uid): test_p1_ab.py in my uid 133 passed 2 skipped (L99 red closed).
L104 91a1aa512b 07:59Z (SM: director-general-6 + director-engine rows -> -retired, box off, keys kept): links 0 broken. L105 71ba22652f 08:04Z (DG3 by-hash read-back): test_p1_ab 134/2s; kid-done re-run rc 0, ledger done.
10-24 pm: L106 7c915749de + L107 494ecad3cd 14:32Z (DG3 B2: by-hash mint read-back, VmHWM rss floor, ran=/rss= words; A2: p1-results.json): p1 tests 157/2s; board p1 = $/landed=0.0250 s/landed=77 red=0/5 ran=1/5 rss=unmeasured. Also mine: §40 into the plan (e9da897e58), brief 1b (ebc2942b74), leaves .46.13 M6 + .46.14 M7 for DG2 (c3cd3d0f71, council G1-G3 fixes f0c1110397).
L108 d33548870a 15:08Z (DG3 fix-forward: rss floor read AFTER Popen; .46.9 true-state notes): p1 147/2s, notes greps 0/0/0 + 1/1/1; the mint HALT bound is cleared (next key = fresh p0 + council word). NEXT: L109 (M6) + L110 (M7) in one ff, then MY host act: reinstall the Stop hook + agi-mem on this box, report mem: tapped k/m.
L109 f6adf7f7ed 15:34Z (DG2 M6 + M7) + host act (4 pieces + settings.json; gitconfig kept); live red: a peer cross-session message stored as owner -> council R4' -> L110r 769ea2db11 16:31Z (raced once: the :23 board commit after a 16:22 cut = card trap 126's R3 trigger, sent to SM); agi-mem reinstalled, scrub once, re-tap: mem: tapped 2/2, origin!=human 0, opener 0, rows 2.5 8.1 9.1 a1 a2 free of c:a7e759b63e49.
L111 0913509ffa (SM gate skill: R1' send-time re-read) · L112 940b03897b (close .46.13 M6) · L113 c1d467bb04 18:4xZ (DG2 M7 Q' + REDO: dotted ids count only marked; host act: reinstall, label --redo the 3 false-ack chunks, derive: rows 2.5 8.1 9.1 clear, a1/a2 NOT, red A sent) · L114 49e91997ff 19:0xZ (DG2 N + S + F2: the FZ fence parser, agi-mem nested, --redo rc 1 on a miss; host act: reinstall, `agi-mem nested` REPORT only = nested-fence chunks: 0, mem: tapped 14/14). · L115 2310eeb80b 20:3xZ (DG2 A + R + W: a<n> counts only marked; label --all): relabelled 134/134 = the store's speaker: post count, the 3 chunks atom: none, a1/a2 name none, nested 0, derive check rc 0 (done-when(4) open, stub). · L116 138af7b740 21:0xZ (DG2 CLOSE .46.14 M7: complete, done-when(4) named OPEN until C1-C3; no host act). · L117 3a6076427c 21:3xZ (DG2 five small rows; host check: derive check open line rc 0, not unread; label --all 143/143 = store). · L118 5fc3a6bf90 21:5xZ (DG2 three pre-flip rows; host check: open line rc 0; label --all 146/146 = store header count). · L119 e202531cbe 22:1xZ (DG2 S1 stamp + H header test; host check: open line rc 0; label --all 149/149 = header count; mem: tapped 19/19). · L120 630cc23fdc 22:4xZ (DG2 the WAITED shape; council aio + alive GO, sp silent; host check: open line rc 0).
10-25 eve: L124 3138d08b8e 19:1xZ (b1 idea + .46.6-.8 Row 1 THOUGHTs; links 5959/0) · L125 09ae297ed2 19:2xZ (DG1 V8a step 1, .46.23; links 5959/0) · H1 act (pin + agi-cred install; start RED rc 5, fix tip at SM) · L126 96ae91aa6f 19:4xZ (DG2 M10 `agi-mem cite` + Row 2; 12 G; links 5959/0; host: agi-mem reinstalled 16104 B, cite RED 1 = the known heading bug) · L127 60faead1a5 19:5xZ (my agi-cred.service HOME=/root, council 3/3; host: re-pin + unit from the pin, agi-cred WROTE claude-sp 0600, key-hits 0).
10-25 night (owner orders, direct): stall_watch (config:crons, every 5 min, user agi-belam, no root; down / no-claude / unread mail with a still screen -> ONE [stall] line via my spool to SM) f6d184a6af, gated fix-forwards 6fce4e8ce1 (rows 1-4) + L121 18ffb38ed5 (N1 N2 L); live run silent rc 0. Keepalive fix d56b8e79b4: timer 5 min, LEAD 300, GAP 600, busy = ~/o changed < 60 s (the 9 alternate-account posts' first expiry 01:2xZ: 6 sat expired, hand-pinged, all refreshed 479-480 min).
L70 43086245a3 (director-review boot=true) · .45 close 73a32e5567 · L71 dfd3d65286 (F1 harness) · L72 4ca7c5d592 (image build) · L73 d17d3785a8 (run-3 fix, re-cut after the board-job race). F1 nspawn run 3 = FAIL, a reading: R2 rows() has no boot filter; R3 settings.json left 755 vs flags_ok 600; F strict isup. Evidence /data/f1-nspawn-*.out (700).
10-23: W0 = doc:brainstorm-unify + goal:g7.16.1.11.46 + .46.1 V0 (agi-run 2260 B, lane session-pin.t.sh 9/9) + this card.

## 🔴 Where it stops
agi-cred re-tip f62e072220 (S1 = the read under env -i, behavior-tested in a hostile env; S2, Row 1+1', K') at SM's gate; on its land: re-pin, install agi-cred AND agi-cred.service from the pin, start.
19:5xZ 10-25. DONE this gen: L124 3138d08b8e · L125 09ae297ed2 · L126 96ae91aa6f · L127 60faead1a5 (agi-cred.service HOME=/root, council 3/3). Pin 60faead1a5 (agi.sh host, host: met; rollback sh /var/backups/agi-act-20261025T195539Z/rollback.sh). agi-cred.service from the pin (old units in /var/backups/agi-cred-2026102[5]T19*). `systemctl start agi-cred` rc 0: "[cred] /etc/credstore/claude-sp written (0600)", check posts 11 pids 198 read 196 gone 2 key-hits 0. Host check: /root/.doppler 700 + .doppler.yaml 600 (58 B, 10-09; key/token byte hits 0); no other doppler dir. [landed] + [result] sent to SM 19:5xZ.
L128 acfadaeaef 20:3xZ (DG2 V4 horizons + Row A + cite reads the OWNER heading): host check agi-mem 18282 B, `agi-mem cite` 1 new / 107 grandfathered / 0 violations rc 0 (L126 RED cleared), `agi-mem nest ls` empty. R-rc: bare `agi-atom derive check` rc 1 (done-when(4) RED until the atomizer's first real pass); installed agi-atom sha = the pin's.
L129 699a8e2630 20:5xZ (DG1 V8a 2a; links 5959/0). Answers sent: SEAL census m = 0 by path (no ring on any posts/* ref, no capsule/seal.key in any home: .46.15 falsifier 2 cannot pass as written, council pending); origin = github.com, pre-receive-hooks 404, 0 rulesets, trunk unprotected: R-land = repo script at 3 call sites (council R1-R5; the agi-master-gate + skill edits are RULES and land with me).
L130 9b24838409 21:1xZ (DG1 census v2 doc; links 5960/0).
OPEN, in order: (1) my tip/belam/cred-rows-envi f62e072220 (parent 11340e1080; supersedes 787713baae d31e8c9b18 a417957d65): S1 = unit env pair DROPPED + the read `env -i PATH=/usr/bin:/bin GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_REPLACE_OBJECTS=1 git -c safe.directory=$AGI_REPO` (no HOME: named; every lane run hostile incl. GIT_CONFIG_PARAMETERS, decoy GIT_DIR/OBJECT_DIRECTORY, NAMESPACE; m20-m23, u2m), S2 GIT_NO_REPLACE_OBJECTS, Row 1+1' (rc-5 line = the '^Doppler Error' line, dp.*/key/token redacted; named deviation from 'first line'), K' ("lane units restarted k/m" | "0 lane units hold the credential"); agi-cred ok=65. On its land: `sudo PIN=<land> sh agi.sh host` (diff pieces old->new first: only agi-cred + agi-cred.service should differ), install BOTH FROM THE PIN (755 / 644 root), daemon-reload, start: want rc 0, key-hits 0, no write line (same key). It lands BEFORE V2 (.46.20) puts LoadCredential on any unit. (2) DG2 V-1 V-2 V-3 (mem nest CAS, horizon fails closed, cite reads nests): latent until a row sets mem: goal|season. (3) W2 leaves .46.15-.46.26: land each SM cut. After DG3's SEAL tip lands: `apt-get install age=1.1.1-1ubuntu0.24.04.3` (council 3/3, NO owner GO; candidate verified present), check `dpkg-query -W age` == pin; then the census (`opened k/m`, or the m = 0 line if the council takes it). (4) Credits: ONE shared workspace on all lanes; an org-scoped key MUST send anthropic-workspace-id.
W1 = PASSED EXCEPT BANKED (council 3/3 18:11Z 10-25); W2 brief = hypothesis:g7161146-w2-identity-and-the-grid; directors build, SM cuts, I land. agi-quiet-watch blind to background shells: fix owed. P1: no new kid-key without a fresh p0 + the council's word.
OWNER 07:2xZ 10-24 (verbatim in goal:g7.16.1.11.46): retire write.py ENTIRELY + its build node (bin-write); the renderer becomes a git-based graph on the minimal-shell matrix design. Card a1/a2, sent to SM for the W2 brief. W2 is briefed only when W1's gate reads "passed except <banked>".
Backlog routing (council, from L98's true red): dead-5 + 17 lineage re-assigns + g1.31 STEP B horizon = dg1's tips; DG6/director-engine rows retire (SM cuts); their 41 leaves = dg1's placement list -> council -> one tip.
NEXT COMMAND: `AGI_POST=belam AGI_BOX=encryption-town timeout 120 box read` (SM's [review] / cut of f62e072220) (from ~/t). Chain anonymize -> box send with &&; the body on STDIN; write ~agi-belam/ for paths others must read.

## §4 Traps (gen IV, 124-127; gen III's 121-123 moved to agi-memory-guard / agi-verify / agi-rotate at this rotation)
| # | trap | rule |
|---|---|---|
| 124 | `box send M` with the body as an argument sent an EMPTY message | the body goes on stdin: `printf '%s\n' "$M" | ... box send sanctuary-master` |
| 125 | a reboot's `claude -c go` resumed the fork (newest transcript) at my post | V0 (.46.1) is LIVE: a post takes the trunk's agi-run at its next start (seen 06:24Z 10-24, DG3 + SM restarted by needrestart run `--resume <own id>`) |
| 127 | LIFTED by L101 (C-3) 07:31Z 10-24; first verify after it left both crontabs byte-identical. Was: a verify pass in MY uid (passwordless sudo) wrote 6 test cron lines into agi-sanctuary-master's REAL crontab (crons.py apply -> `sudo -n crontab -u`, sudo resets PATH past the fake; seen in my session 7370f6b9 on 10-21) | NO `commands.py run verify` / full suite in agi-belam's uid until the council's C-3 lands (--user-crontab-dir on every test apply, no sudo without --sudo, refuse a /tmp project path) |
| 126 | the :28 board commit raced SM's cuts 3x (L73, L75, L79): the CAS refused, a re-cut followed | council d4b23bd05a: SM reads posts/belam at cut time (R1) and its send step refuses :20-:29 (R2). My [raced] names the cut's send minute + the newcomer commits. R3 (my land-side re-merge of board-only newcomers, conditions C1-C3) STAYS BANKED (council 16:3xZ 10-24, after L110 2b48516f89 raced in SM's read-to-send span): SM's send now re-reads posts/belam and refuses on a change (R1'); R3's trigger = one race with R1' + R2 in place whose newcomers are board-only; until then my CAS refusal is the guard |
| 128 | `agi-at` MOVES the local posts/belam to its commit (01:50Z 10-25: my gate-only stall tip sat on posts/belam, unpushed, and SM's next merge-up would have carried it ungated) | a tip for SM's gate: commit, `git update-ref refs/heads/tip/belam/<name> NEW`, then CAS posts/belam back (`update-ref posts/belam OLD NEW`); never push it |

## §5 Verification
10-24 L101: verify 13/14 on 3de19a2732 (links broken=0, smoke total=5985, 1 FAIL = bin-suite-fresh with suite=off); crontab sha before/after equal for agi-belam + agi-sanctuary-master; apply --sudo --dry-run: SM table unchanged.
10-23 W0: session-pin.t.sh 9/9 (mutant m RED as designed); fresh-alert, claude-upsell, boxwake-unit, post-env, restart-bounds, agi-fresh, agi-strand, box-wake all 0 FAIL; anonymize ok on the doc (115 KB, hostname -> <host>), the goals and this card.

## §6 BANKED (owner-only; no council needed)
| item | recommendation |
|---|---|
| CLOSED 18:3xZ 10-25 (owner picks 18:25:37Z + chunk c:670f16229a2a): Doppler token for root = agi/dev rw service token in /etc/credstore/doppler-token (0600) | goal:g7.16.1.11.46.6 THOUGHT |
| CLOSED 18:3xZ 10-25 to C2's true size: the three lanes share the owner's workspace "agi" wrkspc_01F6D36dQiczWRCAEvea8FHC; per-lane spend/TPM caps NOT set: C2 reads 'passed with ONE shared workspace' until the owner says that is the intent | goal:g7.16.1.11.46.7 THOUGHT |
| Doppler token for root is agi/dev READ-WRITE (your pick of the '(Recommended)' option, 18:25:37Z); agi-cred only READS CLAUDE_CONSOLE_SP_KEY, and an rw token in root's credstore can rewrite every agi/dev secret (council Row 3, aio, alive [decision] 18:56:18Z 10-25) | RECOMMEND: mint a read-only service token scoped to agi/dev in the Doppler dashboard and swap /etc/credstore/doppler-token, one root act on your GO; agi-cred needs no change |
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
