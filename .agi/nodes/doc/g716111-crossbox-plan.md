---
id: doc:g716111-crossbox-plan
mint_id: 8c761257cd7d46f58899180b861e0fad
type: doc
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: director-general-3
scaffold_hash: 3076a04e9ae70fa1
season: 2
tags:
  - doc
  - cross-box
  - g7.16.1.11
title: "g7.16.1.11 night item 6: DG5 cross-box on encryption-town -- PLAN ONLY, blocked on the owner's cutover authorization (scrub note); 14 root acts with undo, GitHub-first comms, X1 AGI_BOX bug"
town: core
---
# doc:g716111-crossbox-plan

Night item 6 of goal:g7.16.1.11 (owner 06:5xZ ruling (b)). PLAN ONLY, BLOCKED on the owner: on 2026-09-30 the owner scrubbed the agi checkout from encryption-town and left a note that a fresh clone may be made only when the owner explicitly authorizes cutover. Unit names spelled agi-post@${P2}.service. Off-graph copy /tmp/agi-crossbox/plan.md.

Prepared 2026-10-01 by an Opus 5.5 subagent of director-general-3. Read-only on every box: nothing was written on encryption-town.
Inputs: goal:g7.16.1.11 rulings (b) and the 07:0xZ lines, config:engine v4c, doc:g716111-stage25-rootplan (R1-R17, T1-T10),
doc:radically-simple-engine §T. Probe scripts: /tmp/agi-crossbox/agi-crossbox-probe*.sh (each sanitizes its output on the far side).
Names used: E = encryption-town · L = local-town (this box) · M_E = /data/work/agi on E (the clone; it does not exist yet) ·
P2 = the new post on E (proposed name `dg5-enc`; belam's cell) · A2 = agi-P2 · Hm2 = /var/lib/agi/P2.

### 0 · Route and probe results (E, 2026-10-01; numbers only)
Route: `ssh -F <home>/work/.sanctuary/ssh/config -o BatchMode=yes -o ConnectTimeout=10 encryption-town` (= `commands.py run mesh-encryption-town`).
The existing mesh key is used. Host key pinned. rc 0.
| probe | result |
|---|---|
| OS / systemd | Linux x86_64 · systemd 255 (L is also x86_64) |
| lands as | <user>, uid 1000 (not root); groups: <user> adm cdrom sudo dip video plugdev lxd render |
| `sudo -n true` | **rc 0**: passwordless sudo exists (nothing else was run with sudo) |
| tools present | git 2.43 · node v20.20.2 · npm 10.8 · claude 2.1.283 · python3 3.12 · jq 1.7 · strace 6.8 · script (util-linux 2.39.3) · ssh-keygen · systemd-sysusers · pkaction · doppler 3.76 · gh 2.101 · tmux · wg |
| tools ABSENT | **pi** (L has pi 0.67.68; its package needs node >= 20.6, so E's node v20.20.2 is enough) |
| memory | 7854M total · 6919M avail · swap 4095M (3918M free) · PSI mem some avg10 0.00 · PSI io 0.00 · load 0.01 on 4 threads |
| disk | / 59G (45G free, 21%) · /data 352G ext4 (328G free, 2%), its own filesystem · /data/work is 775 <user> |
| agi footprint | group agi: absent · /var/lib/agi: absent · /opt/agi: absent · system agi-post@ units: 0 · no system agi.slice file · user units: agi.slice static, agi-engine.slice + agi-work.slice masked (guard-init ran here) · crontab: 0 lines · linger yes · polkit rules.d exists |
| agi-* users | **1 already exists**: `agi-lane` (home 750, own group). NOT one of ours (see trap X3) |
| repo clone | **NONE.** <home>/work holds `AGI-REMOVED-REFUSE-NOTE.md` + `AGI-DISABLED-REMOTE.stub` (owner heavy scrub 2026-09-30 08:10Z): "AGI local checkout REMOVED ... DO NOT re-enable prior agi-* systemd units or crontab grid/push jobs from backups without owner review. **Fresh scrubbed clone only when owner explicitly authorizes cutover.**" |
| GitHub | gh authenticated (rc 0), git credential helper for GitHub = gh, protocol https · viewer permission on origin's repo: ADMIN · **the repo is PUBLIC** · `ls-remote` over https works · GitHub over ssh: refused (no key; <home>/.ssh holds only authorized_keys + known_hosts) |
| TPM | absent (same honest limit O.3 as L) · sshd TrustedUserCAKeys lines: 0 |

### 1 · Shape: how DG5 seeds / spawns on E
```
 L (local-town)                               GitHub origin (PUBLIC)                         E (encryption-town)
 MAIN @ local-maxxing/season2/main  --push-->  local-maxxing/season2/main  --fetch(timeout)-->  M_E @ same branch (seed §T)
 config:posts row P2 {box: E, engine.v 4}                                                       agi-project AGI_BOX=encryption-town
 master gates posts/P2 onto trunk  <--fetch--  posts/P2  <--push (<user>, gh https)--          unit agi-post@${P2} (A2, agi.slice)
                                                                                              commits SIGNED by A2's own key
```
- **ONE graph change does the spawning**: a config:posts row with `box: "encryption-town"` and an `engine` object. agi-project already
  filters `select(.box==$b and .engine.v==4)` with `$b = ${AGI_BOX:-local-town}`, so the SAME config:engine bytes project the row on E and
  ignore it on L. No engine byte changes for the projection.
- **Recommended: a SECOND row (P2), not a move.** The owner wants DG5 to stay up on pi on L for the shell-viz test; "spawn more on encryption
  town" is proven by P2 without taking DG5 down. A MOVE later = DG5 row's `box` cell L -> E: L's agi-project stops projecting it
  (T1 locally, agi-flush merges), E projects it; the unit's ExecStartPre mints a NEW key on E (private keys never travel) = a key_history
  rotation on the row, verified by the old key's signature. Do the move only after X-PROOF passes for P2.
- P2's row: a copy of DG5's row minus session cells (`session_id`, `session_name`, `window`, `pid`, `pubkey`, `key_history`), `name: P2`,
  `box: "encryption-town"`, `recover: false`, `pid: 0`, and the SAME engine object DG3 lands for DG5 in Phase C (harness pi-free, 0 USD,
  trunk local-maxxing/season2/main). Written by belam (config:posts = Prime) through write.py, `--dry-run` first (skill agi-post).
- **AGI_BOX**: the engine reads it only in agi-project (default local-town). On E it MUST be passed explicitly (`AGI_BOX=encryption-town`)
  every time agi-project runs, or E projects L's rows (trap X1).
- **The clone** (blocked on the owner, B1): `git clone --filter=blob:none --branch local-maxxing/season2/main <origin https url> /data/work/agi`
  as <user> on /data (328G free, ext4; L's MAIN is tmpfs, E's need not be). Path = §T's `AGI_ROOT` default. Fresh clone of today's
  history only; the DISABLED stub's old-history remotes are never reattached.

### 2 · Cross-comms: GitHub first
| leg | who | how | signed |
|---|---|---|---|
| L -> GitHub | L's `branch_push` (hourly :07) or the post's push after its iteration | trunk `local-maxxing/season2/main` | today's trunk tips are UNSIGNED (`%G?` = N on the last 8); see B4 |
| GitHub -> E | <user> on E (by hand tonight; a user timer only after owner review, B1) | `timeout 60 git -C M_E fetch origin local-maxxing/season2/main` + merge; later the §T seed (fsck + verify-commit vs the anchor) | §T verifies the tip vs ONE anchor line |
| E post -> E clone | A2's unit | agi-turn: one commit per turn on posts/P2, signed with A2's ssh key (gitconfig piece); its pubkey lands in `.agi/keys/P2` on the branch | yes (A2) |
| E -> GitHub | <user> only (holds gh; A2 never gets a GitHub credential) | `git -C M_E push origin posts/P2` after a privacy check of the range | carries A2's signatures |
| GitHub -> L | the master (skill agi-master-gate) | fetch posts/P2, `git log --format=%G? ` must be G for every commit vs allowed_signers incl. P2's key, land onto trunk | verified |
| mail | send.py dm/room transcripts under `.agi/comms` are TRACKED and ride the branches; `.agi/sessions/inbox/*` is gitignored | after each E fetch: `send.py read --box-local` (the mail_poll reader; VERIFY it appends to `$O/.agi/sessions/inbox/P2.md`, the file agi-run/cccc.ts watch) | dm lines are signed by send.py |
Mesh/direct LATER: E already has `wg`; once the DC issues certificates (§6), a post on one box reaches a peer by ssh certificate over
WireGuard instead of a GitHub round-trip.

### 3 · Pre-flight on E (no root; every line must print the expected value, else STOP)
- E0.1 route: `ssh ... encryption-town true; echo $?` -> 0
- E0.2 clean: `getent passwd | grep '^agi-' | cut -d: -f1` -> exactly `agi-lane` · `getent group agi | wc -l` -> 0 · `ls -d /var/lib/agi /opt/agi 2>/dev/null | wc -l` -> 0 · `ls /run/systemd/system | grep -c '^agi'` -> 0
- E0.3 memory/disk (skill agi-memory-guard): MemAvailable >= 4 GiB · PSI mem some avg10 < 10 · /var and /opt avail >= 1024M · /data avail >= 5G
- E0.4 the guard values current: `bash M_E/extensions/agi/guard/guard-init.sh --dry-run --user "$(id -un)" ...` (rootplan P0.5 form) -> 0 value lines
- E0.5 the row projects ONLY P2 on E and NOTHING new on L: on E `cd M_E && AGI_BOX=encryption-town sh -c "$(sh .../sect agi-project HEAD)" -s /tmp/x HEAD; ls /tmp/x/multi-user.target.wants` -> `agi-post@${P2}.service agi-project.path`; on L the same with AGI_BOX unset -> unchanged from before the row
- E0.6 BF_E = /tmp/agi-xbox/before (700): `getfacl`/`stat` of M_E/.git{,/objects,/refs,/refs/heads,/logs,/worktrees} and M_E/.agi/sessions{,/inbox,/rotations}; `git -C M_E worktree list | wc -l`

### 4 · Non-root acts
- **N1 [OWNER-GATED, B1] the clone** (§1). UNDO: `rm -rf /data/work/agi` on E after N7's push. PROOF: `git -C M_E rev-parse --abbrev-ref HEAD` -> `local-maxxing/season2/main`; `git -C M_E rev-parse HEAD` = L's `git rev-parse origin/local-maxxing/season2/main`.
- **N2 [PRIV] the privacy pre-commit guard in M_E** for <user>'s own commits: copy L's guard + `scrub-denylist.json` over the mesh as a pipe (`G` never echoed, never in a node), install as `M_E/.git/hooks/pre-commit` (700). UNDO: remove both files. PROOF: a commit of a file holding `hostname` output is refused (rc 1), the token never printed (rootplan G4 form). REQUIRED before any push from E: the repo is PUBLIC.
- **N3 the row** (belam, on L): write.py config:posts creates row P2 (§1), `--dry-run` first. UNDO: the reverse sub (row retired, never deleted: `status`/`recover` cells per agi-post). PROOF: E0.5.
- **N4 push trunk L -> GitHub** (branch_push at :07, or the post's push). PROOF: `git ls-remote origin local-maxxing/season2/main` = L's tip.
- **N5 fetch on E** (by hand): `timeout 60 git -C M_E fetch -q origin local-maxxing/season2/main && git -C M_E merge --ff-only FETCH_HEAD`. PROOF: E's HEAD = the pushed tip. When §T lands: the seed replaces N5 (B4).
- **N6 deliver mail on E**: `python3 M_E/extensions/agi/bin/send.py read --box-local` with `AGI_BOX=encryption-town` (VERIFY first on a scratch copy that it appends to P2's inbox file). PROOF: `stat -c%s M_E/.agi/sessions/inbox/P2.md` grows by >= 1 line.
- **N7 push E -> GitHub**: as <user>, the privacy guard run over `origin/posts/P2..posts/P2` first, then `git -C M_E push -q origin posts/P2`. PROOF: `git ls-remote origin refs/heads/posts/P2` = E's `git rev-parse posts/P2`.
- **N8 land on L** (the master): `git fetch origin posts/P2`; every commit `%G?` = G; land per skill agi-master-gate. PROOF: P2's reply dm line is on L's trunk.

### 5 · Root acts on E: command · UNDO · PROOF (rootplan R1-R15 as they would run there; every root command over `ssh ... encryption-town 'sudo ...'`)
Runner: DG3 (on the owner's word for B1, B2). No act prints a key, token, hostname, IP, username or home path. P = P2 everywhere.
- **XR1 [SHARED]** `sudo install -d -m 755 /opt/agi /opt/agi/bin /var/lib/agi` · UNDO XT9 · PROOF `stat -c '%a %U' /opt/agi/bin /var/lib/agi` -> `755 root` x2
- **XR2 [SHARED] pi for A2** (E has no pi): stream L's reviewed tree, never npm on E: on L `tar -C <L pi package dir> -c . | ssh ... encryption-town 'sudo sh -c "install -d /opt/agi/pi && tar -C /opt/agi/pi -x && chmod -R a+rX /opt/agi/pi && ln -s ../pi/dist/cli.js /opt/agi/bin/pi"'` (207 MiB) · UNDO XT9 · PROOF `sudo -u nobody /opt/agi/bin/pi --version` -> `0.67.68`, and `find /opt/agi/pi -type f | sort | xargs sha256sum | sha256sum` equal on both boxes
- **XR3 claude for A2: SKIP** for a pi-free row (E's claude 2.1.283 exists; only needed if P2 is ever claude-code, then + the owner's login, rootplan R8a)
- **XR4 [SHARED] project the body from M_E at HEAD with AGI_BOX** · PRE: `cd M_E && sh .../sect agi-project HEAD | cmp - <L's reviewed bytes>` silent, else STOP · `cd /data/work/agi && sudo env AGI_BOX=encryption-town sh -c 'echo HEAD:.agi/nodes/.geometry/engine.md|git cat-file --batch --follow-symlinks|sed -n "/^### agi-project /,/^### /{/^~~~/,/^~~~/{//!p}}"|sh -s /run/systemd/system HEAD'` · UNDO XT2 · PROOF wants = `agi-post@${P2}.service agi-project.path` exactly; `grep -o 'O=[^ ]*' .../agi-post@${P2}.service.d/h.conf` -> `O=/data/work/agi`; `grep -c 'H=pi --provider openrouter'` -> 1
- **XR4b [SHARED] never arm the re-projector on E**: `sudo rm /run/systemd/system/multi-user.target.wants/agi-project.path` (also: its agi-project.service carries no AGI_BOX, trap X1) · UNDO re-link · PROOF wants lists only `agi-post@${P2}.service`
- **XR5 [SHARED] user + group**: `sudo systemd-sysusers /run/systemd/system/agi-users.conf` · UNDO XT8 · PROOF `id -nG agi-P2` -> `agi-P2 agi`; home cell `/var/lib/agi/P2`
- **XR6 home**: `sudo install -d -m 755 -o agi-P2 -g agi-P2 Hm2 Hm2/.claude Hm2/.config Hm2/.config/agi Hm2/hooks` · UNDO XT7 · PROOF `stat -c '%U %a' Hm2` -> `agi-P2 755`
- **XR7 [KEY] the env file: ONE per-spawn zero-USD OpenRouter key**, minted on L (the provisioning key never leaves L) and piped straight into root's file on E, never on disk on L, never printed: `python3 -c '<rootplan R7 mint, agent_id="agi-P2", zero_usd=True, ttl_minutes=480>' | ssh ... encryption-town 'sudo sh -c "umask 077; cat > /var/lib/agi/P2.env"'`; rc 3 = no provisioning key: STOP · UNDO `sudo shred -u /var/lib/agi/P2.env` (key dies at TTL) · PROOF `grep -c '^OPENROUTER_API_KEY='` -> 1, `600 root`, `grep -c '^ANTHROPIC'` -> 0; `provisioning.py status | grep -c agi-P2` -> 1 (on L). Later (§6): minted on E from Doppler instead (B3).
- **XR8 claude credential: SKIP** (pi-free row)
- **XR9 [PRIV] the post's privacy guard**: as rootplan R9, the source = N2's copy in M_E · UNDO XT7 · PROOF G4 form as A2 -> `rc=1`
- **XR10 [MAIN_E] minimal write for A2 on M_E** (ACLs, exactly rootplan R10 with M = /data/work/agi on E; no seat-key line: P2 has no old-engine seat key) · UNDO the `setfacl -x` forms, diff vs BF_E empty · PROOF `sudo -u agi-P2 test -w .git/refs/heads && test ! -w .git/config && test ! -w .git/hooks && echo scoped`
- **XR11 [SHARED] polkit**: `sect agi.rules HEAD | sudo tee /etc/polkit-1/rules.d/50-agi.rules` · UNDO XT4 · PROOF `sudo cmp` vs the piece: silent
- **XR12 [SHARED] SYSTEM agi.slice from E's own user agi.slice** (guard-init wrote it from config:guard's E lines): rootplan R12 command run as <user> on E · UNDO XT2 · PROOF Memory*/ManagedOOM lines equal. VERIFY the E values leave >= 2G for <user> on 7.8G (unit MemoryHigh=4G)
- **XR13 [SHARED]** `sudo systemctl daemon-reload` · UNDO XT3 · PROOF `systemctl cat agi-post@${P2} | grep -c '^# /run/systemd/system'` -> 2
- **GATE N4 (HARD)** as rootplan: Slice = agi.slice, finite MemoryMax/High, ManagedOOM kill, `systemd-analyze verify` silent; E0.3 holds
- **XR14 START** `sudo systemctl start agi-post@${P2}` · UNDO XT1 · PROOF active; ControlGroup `/agi.slice/agi-post@${P2}.service`; `oomctl dump | grep -c /agi.slice` >= 1; worktree branch `posts/P2`; fifo `i` 600, `o` 600; journal `dubious ownership` 0
- **XR15 owner view**: `sudo setfacl -m u:<user>:r Hm2/o` · UNDO `setfacl -x` · PROOF `tail -c 300 Hm2/o | wc -c` -> 300 as <user>
Count: **14 sudo acts** (XR1 XR2 XR4 XR4b XR5 XR6 XR7 XR9 XR10 XR11 XR12 XR13 XR14 XR15) + 2 skipped (XR3, XR8) + 8 non-root (N1-N8).

### 6 · X-PROOF: cross-box seeding + cross-comms, end to end
1. N3 + XR4 proofs: the row alone made P2 exist on E (wants, user, unit) while L projects nothing new.
2. P2's first turn commits `.agi/keys/P2` + its rotation record, signed (`%G?` = G in M_E).
3. DG3 on L: `send.py dm P2 "[ping] xbox-1"` -> N4 -> N5 -> N6: P2's inbox grows, P2 takes a turn (`grep -c 'mail: send.py read P2' Hm2/o` >= 1).
4. P2 replies by send.py -> agi-turn commit -> N7 -> N8: the reply line is on L's trunk, every P2 commit G.
5. Timing row: wall time from step 3's send to step 4's landing (GitHub-first latency, the baseline mesh/direct must beat).

### 7 · Rollback
- ONE graph edit on L first: the reverse sub drops P2's engine cell (or its `box` cell back to L): E's next projection drops it.
- On E, in order: **XT1** `sudo systemctl stop agi-post@${P2}` (agi-flush commits + merges) -> N7 one last push (the work survives on GitHub) ->
  **XT2** remove the projected files by exact name (rootplan T2 list, never a glob over agi*) -> **XT3** daemon-reload + reset-failed ->
  **XT4** rm the polkit rule -> **XT5** M_E: `worktree remove --force Hm2/t`, XR10 undo, chown A2's files back to <user> ->
  **XT6 [KEY]** shred P2.env (+ the guard copies) -> **XT7** `rm -rf Hm2` -> **XT8** `userdel agi-P2; groupdel agi-P2; groupdel agi`
  (NEVER touch `agi-lane`) -> **XT9** `rm -rf /var/lib/agi /opt/agi` -> N1's undo only on the owner's word (back to the scrub state; the
  REFUSE note stays). PROOF after: E0.2 prints its expected values again.
- Never: deleting `posts/P2` on GitHub (retire, never delete), a force push, re-attaching the stub's old-history remotes, any crontab line.

### 8 · What the DOMAIN CONTROLLER adds later (council designs; NOT built here)
- E holds PUBLIC identities only: the allowed_signers set (today TOFU: a post's key arrives on the same branch it signs) becomes E's
  published, quorum-signed list; private keys stay in posts' homes and capsules.
- SSH CA: E's sshd and every box gain `TrustedUserCAKeys` (0 today); the CA key lives in a CAPSULE (signing = a quorum pop, never viewable).
- Owner 07:0xZ (design input only): a login makes a fresh key pair in memory (agent, never a file); E signs a certificate valid for
  minutes; the private key is never written and rotates every login; neither E nor the user can write it. Matrix form (belam): one matrix
  row per certificate template (who · principals · box/interface · validity · force-command · source) IS the cert policy; key =
  KDF(per-login randomness, info = row hash); cert key-id = row hash. Honest limit: no TPM on E either (probed): root on a box can read a
  live session's memory; the win is minutes-long keys and no cross-box minting.
- Then mesh/direct: posts reach peers by certificate over WireGuard (`wg` present on E), GitHub stays the durable channel; per-spawn
  OpenRouter keys minted on E from Doppler (the owner's full Doppler login there), not piped from L; revocation by KRL.

### 9 · Traps
- **X1** agi-project defaults `AGI_BOX` to local-town and the printf'd agi-project.service passes no AGI_BOX: run on E without it and E
  projects L's v4 rows (a second DG5 on another box). Fix in config:engine (Environment=AGI_BOX in agi-project.service) before XR4b is undone.
- **X2** the repo is PUBLIC: every E commit is published at N7; the privacy guard (N2/XR9) is a precondition, not a nicety.
- **X3** `agi-lane` exists on E: observe.sh's `/^agi-/` will report `user agi-lane` that project.sh never projects, so tick.sh writes a
  drift commit every tick. Scope observe.sh to group agi before tick.sh runs on E; never userdel it.
- **X4** trunk tips are unsigned: §T's verify-commit refuses them (rc 1, stays ro). Until the anchor signs the trunk, N5 (plain ff fetch) is the sync.
- **X5** the remote branch `encryption-town/season2/main` (2026-09-19, not an ancestor of today's HEAD) predates the scrub: never base on it, never delete it.
- **X6** `After=agi-ram-main.service` in the unit: absent on E, harmless (ordering only).
