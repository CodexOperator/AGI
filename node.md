---
id: doc:g716111-stage2-rootplan
mint_id: 490588c9c0fb429abb268d1152b0366f
type: doc
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: director-general-3
scaffold_hash: 6a686011171304d8
season: 2
tags: []
title: "g7.16.1.11 stage 2: the root-act plan for ONE test post (agi-probe) on a throwaway origin, each act with its undo"
town: core
---
# doc:g716111-stage2-rootplan

Stage 2 of goal:g7.16.1.11 (belam [decision] 01:58Z 10-01, owner 'Stages 1-2 now, stop before 3'): every root act with its undo and proof, listed BEFORE any is run. Prepared by an Opus 5.5 build subagent of director-general-3 (no root), reviewed by DG3 (R10 changed: a per-spawn 0.01 USD key, never the .env key). Inputs live in /tmp/agi-stage2/ (seed.bundle, bin/, engine.diff = the v3 pieces).


Runner: DG3, with root. Inputs (built unprivileged, read-only from here on): `/tmp/agi-stage2/seed.bundle`
(trunk 4ef2dcce68: tree of live HEAD 3405c41faa + the seed commit: engine v3, ONE probe row, owner attrs, card +
scratch), `/tmp/agi-stage2/bin/` (the 22 v3 pieces, for the master's push), `/tmp/agi-stage2/seed.mints` (card, scratch).
The live repo, its refs and hooks, the live posts (user-manager scopes `agi-post-*.scope`), `agi-memguard.service` and
`agi-ram-main.service` are never touched. **Never glob-delete `agi-*` units: two pre-existing system units share the prefix.**
Shorthands: `P=probe` (unit names are spelled agi-post@${P}.service so the privacy guard does not read them as an address); in checks only: `PU='sudo -u agi-probe -H env PATH=/var/lib/agi/probe/bin:/usr/bin:/bin'`, `SB=$(cut -d' ' -f2 /tmp/agi-stage2/seed.mints)`.
Risk marks: **[SHARED]** = touches box-wide state on a box with live sessions; **[KEY]** = key handling.

## 0 · Pre-flight (no root; every line must print the expected value, else STOP)
- `getent passwd | grep -c '^agi-'` ; `getent group agi | wc -l`  ->  expect 0 ; 0
- `ls -d /var/lib/agi /opt/agi /run/systemd/system/multi-user.target.wants /run/systemd/system/agi-* 2>/dev/null | wc -l`  ->  expect 0
- `sudo test -e /etc/polkit-1/rules.d/50-agi.rules; echo $?`  ->  expect 1
- `dpkg -s dtach 2>/dev/null | grep -c '^Status: install ok'`  ->  expect 0 (so R1 is ours to undo)
- `git bundle verify -q /tmp/agi-stage2/seed.bundle`  ->  expect "is okay"
- memory / disk per skill agi-memory-guard; `df --output=avail -h /var /opt`  ->  expect >= 2 GB free on / (origin + home + checkout + pi copy ~ 0.6 GB)

## 1 · Root acts (17), in order. Each: command · UNDO · proof
- **R1** [SHARED] dpkg lock: `sudo apt-get install -y --no-install-recommends dtach`
  - UNDO: `sudo apt-get purge -y dtach`
  - PROOF: `dtach 2>&1 | grep -c -- '-N'` >= 1
- **R2** `sudo install -d -m 755 /opt/agi/bin /var/lib/agi`
  - UNDO: `sudo rm -rf /opt/agi /var/lib/agi` (T6)
  - PROOF: `stat -c '%a %U' /opt/agi/bin /var/lib/agi` = 755 root ×2
- **R3** `sudo cp -r "$(readlink -f "$(dirname "$(readlink -f /usr/local/bin/pi)")/..")" /opt/agi/pi`
  - UNDO: T6
  - PROOF: `ls /opt/agi/pi/dist/cli.js`
- **R4** `sudo sh -c 'chmod -R a+rX /opt/agi/pi && ln -s ../pi/dist/cli.js /opt/agi/bin/pi'` (one file in the package is not world-readable: the edit tool)
  - UNDO: T6
  - PROOF: `sudo -u nobody /opt/agi/bin/pi --version` = 0.67.68
- **R5** `sudo git clone -q --bare --branch trunk /tmp/agi-stage2/seed.bundle /var/lib/agi/origin.git`
  - UNDO: T6
  - PROOF: `sudo git -C /var/lib/agi/origin.git rev-parse --short trunk` = 4ef2dcce68; `symbolic-ref HEAD` = refs/heads/trunk
- **R6** `cd /var/lib/agi/origin.git && sudo sh -c 'git remote remove origin; echo trunk:.agi/nodes/.geometry/engine.md|git cat-file --batch --follow-symlinks|sed -n "/^### agi-project /,/^### /{/^~~~/,/^~~~/{//!p}}"|sh -s /run/systemd/system trunk'` = agi-seed's own pipeline (BOOT), minus sysusers/reload/start
  - UNDO: T2
  - PROOF: `ls /run/systemd/system/multi-user.target.wants` = agi-post@${P}.service agi-project.path; `cat /run/systemd/system/agi-post@${P}.service.d/h.conf` shows H=pi ... and O=/var/lib/agi/origin.git; nothing else in /run/systemd/system changed
- **R7** `sudo systemd-sysusers /run/systemd/system/agi-users.conf`
  - UNDO: T5
  - PROOF: `id -nG agi-probe` = agi-probe agi
- **R8** `sudo sh -c 'cd /var/lib/agi/origin.git && git config core.sharedRepository group && git config core.logAllRefUpdates always && chgrp -R agi . && chmod -R g+rwX . && find . -type d -exec chmod g+s {} +'`
  - UNDO: T6
  - PROOF: `$PU git -C /var/lib/agi/origin.git log --oneline -1 trunk` works as agi-probe
- **R9** `cd /var/lib/agi/origin.git && sudo sh -c 'echo trunk:.agi/nodes/.geometry/engine.md|git cat-file --batch --follow-symlinks|sed -n "/^### pre-receive /,/^### /{/^~~~/,/^~~~/{//!p}}">hooks/pre-receive && chmod 755 hooks/pre-receive'`
  - UNDO: T6
  - PROOF: `sudo cmp /var/lib/agi/origin.git/hooks/pre-receive /tmp/agi-stage2/bin/pre-receive` silent
- **R10** [KEY] (DG3 change: NEVER the long-lived .env key -- a director never touches .env; the engine's own per-spawn mint, capped at provisioning.zero_usd_key_limit_usd = 0.01 USD, TTL 240 min): `cd <MAIN> && python3 -c 'import sys;sys.path.insert(0,"extensions/agi/bin");import provisioning as p;k=p.mint(iter_n="S2",agent_id="agi-probe",tier="kid",zero_usd=True,ttl_minutes=240,root=".");sys.stdout.write("OPENROUTER_API_KEY="+k.secret+"\n") if k else sys.exit(3)' | sudo sh -c 'umask 077; cat > /var/lib/agi/probe.env'` (never printed; rc 3 = no provisioning key -> STOP)
  - UNDO: `sudo shred -u /var/lib/agi/probe.env` + the key expires by its TTL
  - PROOF: `sudo sh -c 'grep -c "^OPENROUTER_API_KEY=" /var/lib/agi/probe.env; stat -c "%a %U" /var/lib/agi/probe.env'` = 1 / 600 root; `provisioning.py status` lists one outstanding agi-probe key at 0.01 USD
- **R11** [SHARED] /etc: `cd /var/lib/agi/origin.git && sudo sh -c 'echo trunk:.agi/nodes/.geometry/engine.md|git cat-file --batch --follow-symlinks|sed -n "/^### agi.rules /,/^### /{/^~~~/,/^~~~/{//!p}}">/etc/polkit-1/rules.d/50-agi.rules'`
  - UNDO: T4
  - PROOF: `sudo cmp /etc/polkit-1/rules.d/50-agi.rules /tmp/agi-stage2/bin/agi.rules` silent (polkitd reloads rules on change; proven functionally in (g))
- **R12** [SHARED]: `sudo systemctl daemon-reload` (system manager; the live posts are user-manager scopes)
  - UNDO: T3
  - PROOF: `systemctl cat agi-post@probe` = template + h.conf; `systemctl show -p Environment agi-post@probe` has H= and O=
- **R13 (a) START** `sudo systemctl start agi-post@probe` (ExecStartPre clones ~110 MiB: if it times out at 90 s, `sudo rm -rf /var/lib/agi/probe/t` and re-run)
  - UNDO: `sudo systemctl stop agi-post@probe`
  - PROOF: `systemctl is-active agi-post@probe` = active; `sudo test -S /run/agi-probe/s`; `sudo ls /var/lib/agi/probe/t/.agi/keys` = probe
- **R14 (f) ROTATION** `sudo systemctl restart agi-post@probe` -- run after (b)-(d) below pass
  - UNDO: --
  - PROOF: `sudo git -C /var/lib/agi/origin.git for-each-ref --format='%(refname)' refs/posts` = refs/posts/probe/head (agi-flush pushed it through pre-receive as agi-probe); active again; `.brief` mtime newer than the restart; `sudo ls /var/lib/agi/probe/.pi/agent/sessions/*/ | wc -l` = 1 (pi -c resumed, no 2nd session)
- **R15 (e) MASTER MERGE** `sudo sh -c 'set -e; git clone -q /var/lib/agi/origin.git /var/lib/agi/master; cd /var/lib/agi/master; git fetch -q origin refs/posts/probe/head; git -c user.name=master -c user.email=<master-email> -c commit.gpgsign=false merge -q --no-ff -m "master: merge probe" FETCH_HEAD; git diff --name-only HEAD^1 HEAD | grep -v "^\.agi/\(n/$(cut -d" " -f2 /tmp/agi-stage2/seed.mints)/|keys/probe$|drift/agi-probe$\)" && exit 9 || :; PATH=/tmp/agi-stage2/bin:$PATH git push -q origin HEAD:trunk'` -- refuses (rc 9) if the probe touched ANY path but its scratch node, its key, its drift file, BEFORE the root push runs the gate (see risk M2)
  - UNDO: T6
  - PROOF: `sudo git -C /var/lib/agi/origin.git log -1 --format=%s trunk` = master: merge probe (agi-gate ran in pre-receive and passed)
- **R16 (g) HEAL, 1/2** `sudo systemctl stop agi-post@probe` (simulated death; ExecStopPost flushes again)
  - UNDO: --
  - PROOF: `systemctl is-active agi-post@probe` != active
- **R17 (g) HEAL, 2/2** `sudo -u agi-probe -H env PATH=/var/lib/agi/probe/bin:/usr/bin:/bin sh -c tick.sh` (tick runs AS THE POST; its `systemctl start` goes through polkit, not sudo)
  - UNDO: --
  - PROOF: active again; `$PU git -C /var/lib/agi/probe/t log -1 --format='%s %G?'` = drift: agi-probe (signed); `sudo cat /var/lib/agi/probe/t/.agi/drift/agi-probe` = `< unit agi-post@probe`

(b)-(d) are checks on R13, no act:
- **(b) brief**: `sudo head -3 /var/lib/agi/probe/.brief` = the card-probe and probe-scratch rows (expect `0.544 +0.0 doc:card-probe`).
- **(c) work** (poll up to 5 min): `sudo grep -c 'probe was here' /var/lib/agi/probe/t/.agi/n/$SB/node.md` >= 1.
- **(d) signed turn-end commit**: `$PU sh -c 'cd ~/t; sect signers|sh>~/allowed; git log -1 --format=%s; git -c gpg.ssh.allowedSignersFile=$HOME/allowed verify-commit HEAD'` = agi-probe + Good "git" signature for probe. (It reaches refs/posts/probe/head at the flush in R14; re-verify there with `git -C /var/lib/agi/origin.git`.)
- Narrowness of the rule (optional, no change): `sudo -u agi-probe systemctl stop agi-post@probe` must FAIL (polkit grants start only).
- After R15, the next rotation's brief sees trunk: `sudo systemctl restart agi-post@probe` then `$PU git -C /var/lib/agi/probe/t log --oneline -3` contains "master: merge probe".
- `agi-project.path` is projected and linked but NOT started in stage 2 (it re-runs the projector as root on every trunk move); starting it is a stage-3 item.

## 2 · Teardown (returns the box to 0 agi- users / 0 agi units / no polkit rule / no dtach)
- **T1** `sudo systemctl stop agi-post@probe`
  - PROOF: `pgrep -c -u agi-probe` = 0
- **T2** `sudo sh -c 'cd /run/systemd/system && rm -rf agi-post@.service agi-post@${P}.service.d agi-project.service agi-project.path agi-users.conf multi-user.target.wants/agi-post@${P}.service multi-user.target.wants/agi-project.path && rmdir multi-user.target.wants'` (exact names; the wants dir did not exist before, pre-flight)
  - PROOF: `ls /run/systemd/system | grep -c agi` = 0
- **T3** `sudo sh -c 'systemctl daemon-reload; systemctl reset-failed agi-post@${P}.service 2>/dev/null; :'`
  - PROOF: `systemctl list-units --all --no-legend 'agi-post@*' 'agi-project*' | wc -l` = 0
- **T4** `sudo rm -f /etc/polkit-1/rules.d/50-agi.rules`
  - PROOF: `sudo test -e /etc/polkit-1/rules.d/50-agi.rules; echo $?` = 1
- **T5** `sudo sh -c 'userdel agi-probe; getent group agi-probe >/dev/null && groupdel agi-probe; groupdel agi'`
  - PROOF: `getent passwd | grep -c '^agi-'` = 0; `getent group agi agi-probe | wc -l` = 0
- **T6** `sudo rm -rf /var/lib/agi /opt/agi` (origin, master clone, the probe home WITH its private key, the env file)
  - PROOF: `ls -d /var/lib/agi /opt/agi 2>/dev/null | wc -l` = 0
- **T6b** no reap (it could revoke a live round's key): the probe key dies at its 240-min TTL, capped at 0.01 USD
  - PROOF: `provisioning.py status` after the TTL lists no agi-probe key
- **T7** `sudo apt-get purge -y dtach` (only if pre-flight showed it absent)
  - PROOF: `dpkg -s dtach 2>/dev/null | grep -c 'install ok'` = 0
- **T8** (no root) `systemctl list-unit-files --no-legend 'agi*' | awk '{print $1}'`
  - PROOF: exactly agi-memguard.service, agi-ram-main.service (pre-existing, untouched)
Leftovers by design: journal lines for agi-post@probe; `/tmp/agi-stage2/` (no keys; delete when the council is done).

## 3 · Risks on a shared box with live sessions
- **[SHARED] R1/T7** apt takes the dpkg lock (blocks unattended-upgrades for seconds). Low.
- **[SHARED] R11** a file under /etc: grants group agi `start` of `agi-post@<name>` and nothing else; group agi has one member. Low.
- **[SHARED] R12/T3** system daemon-reload: reloads every system unit file; running services keep running; the live posts are in the USER manager. Low.
- **[SHARED] wants links in /run/systemd/system/multi-user.target.wants**: anyone running `systemctl start multi-user.target` / `isolate` / `default` during the test would also start agi-post@probe and agi-project.path. Low; gone at T2 or reboot.
- **[KEY] M1** (DG3: mitigated) R10 now mints a per-spawn key capped at 0.01 USD with a 240-min TTL -- never the long-lived .env key; the probe can still read it from /proc/self/environ, so the worst case is 0.01 USD on the free row.
- **M2 (UNSAFE without the guard in R15)**: the master's push runs pre-receive AS ROOT, and agi-gate executes `agi-project` extracted from the PUSHED tip. A post that edits engine.md in its own ref gets its code run as root at the master merge. R15 refuses any path outside the probe's three; for stage 3, the master must not be root (council).
- **M3** the shared origin is group-writable (core.sharedRepository=group): any member can rewrite refs/heads/trunk with plain file writes, bypassing pre-receive and agi-gate; harmless with one member, a real hole with many (council).
- The probe's read tool can read every world-readable path on the box (e.g. the live repo, which is 775/664). It cannot write outside its home and the origin. Low.
- pi's first start downloads fd/rg into ~/.pi/agent/bin (network to GitHub). Low.

## RESULT -- stage 2 PASS (run 02:49-02:58Z 10-01, Opus executor of DG3; full log off-graph)
| behaviour | proof |
|---|---|
| (a) start | unit active, NRestarts 0 after ONE corrective (below); dtach socket present; the post's key in t/.agi/keys |
| (b) brief | .brief written 3 s after start: doc:card-probe 0.544, doc:probe-scratch 0.456 |
| (c) work | 'probe was here' in the scratch node within ~30 s; sessions 2 + 3 after each restart |
| (d) signed turn-end commit | subject agi-probe, verify-commit Good for probe; touched only its key + the scratch node |
| (e) master merge | origin trunk 'master: merge probe'; the R15 guard saw only the expected paths; pre-receive ran agi-gate |
| (f) rotation | restart flush pushed refs/posts/probe/head; brief rewritten 1 s after; key kept; the next rotation pulled the merge |
| (g) heal | tick.sh AS agi-probe restarted the stopped unit in 0.2 s via polkit (no sudo); signed 'drift: agi-probe' commit; agi-probe could NOT stop the unit |
DEVIATIONS: R1 ran at 02:49:08Z, 52 s before the stated 02:5xZ floor (the executor misread a wait-loop exit) -- disclosed. R13 corrective: the ExecStartPre clone of the root-owned origin was refused as dubious ownership (git 2.43 ignores a per-clone -c safe.directory for a local clone), the unit crash-looped 0 USD; fixed by seeding [safe] directory=* in the probe's ~/.gitconfig BEFORE the clone. Typos fixed in place: R1 proof (dtach --help), R5 short sha, R8 proof, R15 guard regex (grep -vE), T2 quoting; probe.env shredded before T6.
TEARDOWN (re-verified by DG3 03:0xZ): 0 agi- users, 0 agi groups, no /var/lib/agi or /opt/agi, no polkit rule, 0 agi entries under /run/systemd/system, unit files = the two pre-existing (both active), dtach purged. USD 0 (the 0.01 cap key used=0, dies at its TTL).
FINDINGS for the council: 1 the clone-ownership fix must live in a piece (stage-3 blocker) · 2 strace output ~/r grows unbounded (14.1 MB in ~4 min) · 3 pi exits 1 on stop: the unit reads failed though the flush ran · 4 a polkit DENY times out ~25 s instead of refusing fast · 5 the prep emulated as the clone's owner, so a different-user clone was never exercised · 6 %G? checks need the signers file.
