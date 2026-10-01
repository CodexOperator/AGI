---
id: doc:g716111-uvwx-build
mint_id: 418e9b728505487e8e4fc08a0a201a1c
type: doc
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: director-general-3
scaffold_hash: a7efcb959b904fae
season: 2
tags:
  - doc
  - domain-controller
  - g7.16.1.11
title: "g7.16.1.11 §U-§X phase A (dry): agent-held stand-in cert + test CA on scratch sshd 127.0.0.1, 56/56, 10 holes in the doc pieces (patched beside), 12 real-box acts listed (none run)"
town: core
---
# doc:g716111-uvwx-build

The council's domain-controller design §U-§X (doc:radically-simple-engine; belam 07:19Z release, owner scope confirmed 07:4xZ: SSH certificates, the test CA, the stand-in cert, the sshd Match drop-in on the owner's OWN box for its OWN posts; cert tests on a SCRATCH sshd bound to 127.0.0.1; any real-sshd change = sshd -t + a systemd-run --on-active auto-revert cancelled only after a fresh login; the owner's login path never touched). PHASE A, dry only: the doc pieces were extracted byte-exact by an Opus subagent (stopped mid-task by a safety classifier; not re-dispatched until the owner confirmed the scope), the remainder built and tested by a Sonnet 5.5 subagent of director-general-3: 56/56 checks, scratch sshds on 127.0.0.1 only, the CA and stand-in held in agents only, every scratch key shredded; the real sshd, /etc, units and keys untouched. Doc pieces (byte-exact, in the council doc): agi-sign 722 · agi-login 337 · xb 1,025 · pre-receive 673 (the 681 claim = a tested copy with a real path) · dc-project 288 · dc-principals 302 · the 4 Match lines 156.

## Holes in the doc pieces (doc bytes kept; patched copies below)
| # | piece | hole | patched |
|---|---|---|---|
| 1 | agi-login | §X/§V call it with a PRINCIPAL, it passes it to agi-sign as a RID -> exit 3 | looks up rid or principal |
| 2 | agi-login | ./agi-sign not found from another cwd (rc 127) | $(dirname $0) |
| 3 | agi-login | mktemp -p $XDG_RUNTIME_DIR errors when unset (service users) | falls back to /dev/shm |
| 4 | pre-receive | the literal <U: allowed> placeholder refuses EVERY push | reads git config agi.allowed (740 B) |
| 5 | pre-receive | the skew check bounds only the past: a commit dated up to the cert's end passes | bounded both ways |
| 6 | xb | git 2.43 needs user.signingkey; the agent lists the plain key before the cert, so a first-key default signs WITHOUT the cert | signs with the cert line |
| 7 | the 4 Match lines | omit AuthorizedKeysFile none + RevokedKeys (which §V's box line says are there): a plain key still logs in for the Match user and a REVOKED serial still logs in | 50-agi.conf.patched adds both |
| 8 | RevokedKeys | a missing KRL file refuses every cert login for that Match user | the empty KRL must exist before reload |
| 9 | row opts | environment=AGI_POST is ignored (no PermitUserEnvironment) | a forced-command wrapper agi-git <post> |
| 10 | AuthorizedPrincipalsCommand | sshd refuses a script not owned by root (scratch-only workaround; the real /etc/agi path is fine) | none needed live |

## Tests (all PASS; full sanitized output below)
(a) the agent-held stand-in cert (key-id = its rid, principal owner-standin, valid to 14:00Z, force-command capsule-login, no extensions) runs ONLY the forced stub; a pty and a remote forward refused · (b) another CA's cert refused rc 255 · (c) an expired cert refused · (d) a row without restrict: agi-sign exits 3; a cert signed outside agi-sign refused · (e) a plain key for the same user logs in as before; with the doc's agi-* Match the owner path is untouched · extras: another box's rid, a hostile key-id, a deleted row, an edited row cell, a KRL serial -- all refused · agi-login (patched): two logins = two fresh keys, 0 key files · xb send/recv over a scratch hub (cert login, git-shell, patched pre-receive) and over a file remote (GitHub stand-in); forgery to the hub refused; to a hook-less remote recv prints [refused]; a backdated commit refused by the skew check; a cert-less signature refused.

## PLAN (real-box acts, NOT run)

Status: NOTHING below has been run. Phase A touched only /tmp/agi-uvwx/ (scratch sshd on 127.0.0.1, own user, no sudo, no /etc).
Owner scope (via belam 07:4xZ): SSH certificates, the CA, the stand-in cert and the sshd Match drop-in, on the owner's OWN box for its OWN posts.
Conditions: any change to the REAL sshd = `sshd -t` first + a timed auto-revert cancelled only after a fresh login works; the owner's existing login path is never touched.
Placeholders: `<box>` = the box name written in the matrix `box` cell · `<agi-user>` = an existing `agi-*` account (§X: `agi-capsule`) · `<owner-user>` = the owner's own login.
Install the PATCHED pieces (`agi-login.patched`, `pre-receive.patched`, `xb.patched`, `50-agi.conf.patched`); the verbatim ones fail (test.txt: L0, XB-V, XB0, X11g, KRLA, a6).
Every act is run by a root-capable human/post the owner names; none is run by Phase A. Acts 1-12 are the whole real-box change set.

| # | Act (command) | UNDO | PROOF |
|---|---|---|---|
| 1 | **Baseline, read-only.** `sshd -T -C user=<owner-user>,host=x,addr=127.0.0.1 > /root/sshd-T.owner.before` · same for `user=<agi-user>` · `sshd -T \| grep -E '^(include\|authorizedkeysfile\|trustedusercakeys\|revokedkeys\|authorizedprincipalscommand)'` · `systemctl is-active ssh ssh.socket` · `ls /etc/ssh/sshd_config.d/` | none (read-only) | the 3 files exist; `Include` is the FIRST directive of /etc/ssh/sshd_config (the Match block must come before any global AuthorizedKeysFile: first value wins; test.txt section 5) |
| 2 | **Install the pieces, root-owned.** `install -d -m 755 -o root -g root /etc/agi /etc/agi/dc /etc/agi/bin` · `install -m 755 -o root -g root dc-principals /etc/agi/dc-principals` · `install -m 755 -o root -g root dc-project agi-sign /etc/agi/bin/` · `install -m 755 -o root -g root agi-login.patched /etc/agi/bin/agi-login` (it finds agi-sign beside itself) | `rm -rf /etc/agi` (only ever our files) | `stat -c '%U:%G %a %n' /etc/agi /etc/agi/dc /etc/agi/dc-principals` = `root:root 755/755/755`; sshd refuses a script not root-owned or any parent group/other-writable (test a7: `Unsafe AuthorizedPrincipalsCommand`) |
| 3 | **The CA public key (the TEST CA only) + an EMPTY KRL.** `install -m 644 -o root -g root test-ca.pub /etc/agi/dc/ca.pub` · `ssh-keygen -k -f /etc/agi/dc/krl && chmod 644 /etc/agi/dc/krl` | `rm /etc/agi/dc/ca.pub /etc/agi/dc/krl` | `ssh-keygen -lf /etc/agi/dc/ca.pub` = the fingerprint `ssh-add -l` shows in the CA agent. The KRL file MUST exist before act 9: a missing RevokedKeys file fails CLOSED, every cert login refused (test KRL0) |
| 4 | **Project this box's rows.** `/etc/agi/bin/dc-project <box> < matrix.tsv > /etc/agi/dc/rows.new && chmod 644 /etc/agi/dc/rows.new && mv /etc/agi/dc/rows.new /etc/agi/dc/rows` (matrix = the §U node's fenced TSV, user cells = the real agi accounts; owner-standin row `valid` = `-5m:20261001140000Z`, written once with `date -u` read) | `rm /etc/agi/dc/rows` (no row = no cert login) | `dc-project <box> < matrix.tsv \| cmp - /etc/agi/dc/rows` rc 0 (U9a) · `sudo -u nobody /etc/agi/dc-principals <agi-user> <standin-rid>` prints `restrict,command="capsule-login" owner-standin` (the `AuthorizedPrincipalsCommandUser nobody` can read it) · a row with empty opts prints nothing (U-P2) |
| 5 | **Offline parse of the candidate, no system effect.** Copy /etc/ssh/sshd_config + its drop-ins to `/tmp/pre/`, point its `Include` at `/tmp/pre/d/*.conf`, add `50-agi.conf.patched` there; `sshd -t -f /tmp/pre/sshd_config` · `sshd -T -f /tmp/pre/sshd_config -C user=<owner-user>,host=x,addr=127.0.0.1 > /tmp/pre/owner.after` · same for `<agi-user>` | `rm -rf /tmp/pre` | `-t` rc 0 · `diff /root/sshd-T.owner.before /tmp/pre/owner.after` EMPTY (the owner's path is untouched) · the `<agi-user>` dump shows `trustedusercakeys /etc/agi/dc/ca.pub`, `authorizedkeysfile none`, `revokedkeys /etc/agi/dc/krl`, `authorizedprincipalscommanduser nobody` (test.txt REAL-doc / REAL-patched) |
| 6 | **Install the drop-in** (the only change to /etc/ssh). `install -m 644 -o root -g root 50-agi.conf.patched /etc/ssh/sshd_config.d/50-agi.conf` | `rm -f /etc/ssh/sshd_config.d/50-agi.conf` | `cmp 50-agi.conf.patched /etc/ssh/sshd_config.d/50-agi.conf` rc 0; /etc/ssh/sshd_config itself unchanged (`sha256sum` before = after) |
| 7 | **`sshd -t` on the live files, before anything reloads.** `sshd -t && echo OK` | on non-zero: `rm -f /etc/ssh/sshd_config.d/50-agi.conf` at once, STOP, do not reload | rc 0, no output |
| 8 | **Arm the auto-revert BEFORE the reload.** `systemd-run --unit=agi-ssh-revert --on-active=10min /bin/sh -c 'rm -f /etc/ssh/sshd_config.d/50-agi.conf; sshd -t && systemctl reload ssh'` | `systemctl stop agi-ssh-revert.timer` (only in act 11) | `systemctl list-timers agi-ssh-revert.timer` shows NEXT within 10 min; it runs under systemd, so it fires even if every ssh session is gone |
| 9 | **Reload, never restart.** `systemctl reload ssh` (SIGHUP; the listener and every open session stay) | the revert timer (act 8) or the lockout recovery below | `systemctl is-active ssh` = active; the session you ran it from is still alive; `journalctl -u ssh -n 5` shows `Received SIGHUP; restarting` and no error |
| 10 | **Fresh login test from a SECOND session** (keep the first open). (a) the owner's own path: a NEW connection `ssh -o BatchMode=yes -o IdentitiesOnly=yes <owner-user>@<box> true` rc 0. (b) negative: a cert signed by another CA and an expired cert for `<agi-user>` are refused. (c) positive, only if `<agi-user>` already exists: `eval $(ssh-agent -s); KEY_LIFE=300 CA_SOCK=<armed CA agent> /etc/agi/bin/agi-login owner-standin; ssh <agi-user>@<box> ask-0001` runs ONLY the forced command | any failure of (a): do nothing, the act-8 timer reverts in ≤ 10 min, or run the recovery below | (a) rc 0 · (b) rc 255 + log `Certificate invalid: expired` / `Failed publickey` (test b, c) · (c) the forced command ran with `ask-0001` only in SSH_ORIGINAL_COMMAND (test a1, a2) · `diff /root/sshd-T.owner.before <(sshd -T -C user=<owner-user>,host=x,addr=127.0.0.1)` EMPTY on the live daemon |
| 11 | **Cancel the revert, only now.** `systemctl stop agi-ssh-revert.timer agi-ssh-revert.service` | re-arm act 8 and remove the drop-in by hand | `systemctl list-timers \| grep -c agi-ssh-revert` = 0 · /etc/ssh/sshd_config.d/50-agi.conf still present |
| 12 | **Record + CHECK.** `dc-project <box> < matrix.tsv \| cmp - /etc/agi/dc/rows` · commit the matrix, the patched pieces and this act log to the graph (`write.py`, then `grid.py commit --all`) | `git revert` the graph commit (never delete) | cmp rc 0 · `links.py links` broken 0 |

**Lockout recovery (the order to try).** The Match block names only `agi-*`, so the owner's login cannot be locked out by its rules; the risks are a bad config (act 7 catches it; a failed reload keeps the OLD config running) and a missing KRL file (act 3).
1. Do nothing: the act-8 timer removes the drop-in and reloads within 10 minutes, with no ssh needed.
2. From the still-open first session: `rm -f /etc/ssh/sshd_config.d/50-agi.conf && sshd -t && systemctl reload ssh`.
3. From the console / out-of-band: the same one line. Never `systemctl restart ssh`; never edit /etc/ssh/sshd_config or any existing login line; never `sshd -T` as proof of an `agi-*` login, only a real second session.

**BLOCKED, encryption-town acts (owner cutover; Phase A does not list them as doable):**
| # | Act | Blocked on |
|---|---|---|
| E1 | `agi-capsule` account + `i` writable by it (§X.2, ExecStartPre `+`, ~60 B) + the REAL capsule-login (§O.5, 692 B) in place of the stub | the owner: a root act on encryption-town |
| E2 | the real CA's first armed window (`ssh-add -t` from the capsule seed) | the owner's real phone (mutual quorum, O.8); tonight only the throwaway test CA arms |
| E3 | the owner-standin row in the §U matrix NODE (graph commit), `valid` ending 14:00Z, projected on encryption-town; `dc-project enc \| cmp` rc 0 on BOTH boxes (U10) | E1 + the owner's go |
| E4 | SI1-SI7 re-read on the real units, DG5's login on encryption-town and nowhere else (U10, SI8 at 14:00Z+1 min) | E1, E3 |
| E5 | §W hub: a bare repo + `pre-receive.patched` under the git-shell row of dg5/belam on encryption-town; W12-W15 live over GitHub and the hub | E1, E3, a second real account (W15) |
| E6 | at the owner's wake: delete the owner-standin row, `dc-project enc \| cmp`, record the rid that died (SI5, SI9) | the owner's real phone key |
| E7 | cutover of the per-seat signing keys and the ExecStartPre post key (parity rows 17-18) onto agi-login | after E4; the owner's call |

**What Phase A proved for these acts:** /tmp/agi-uvwx/test.txt (56 PASS, 0 FAIL, real outputs, user/host/home redacted) · pieces + patched copies beside them · configs `conf/rendered/` · matrix `matrix.tsv` + `rows.enc`.


## Patched pieces (byte-exact)
### agi-login.patched (663 B, sha256 cd13292ff2cb5058)
~~~~~
#!/bin/sh
# agi-login RID|PRINCIPAL: a fresh key pair per login, in RAM (tmpfs) for < 1 s, then held ONLY by the session agent; the private key is never written to disk
# patched: the arg is looked up in the rows (rid or principal) so §X's `agi-login owner-standin` works; agi-sign is found beside this file; tmpfs falls back to /dev/shm
d=${DC:-/etc/agi/dc};i=$(awk -F'\t' -v p="$1" '$1==p||$4==p{print $1;exit}' $d/rows);[ "$i" ]||exit 3
t=$(mktemp -d -p ${XDG_RUNTIME_DIR:-/dev/shm});ssh-keygen -q -t ed25519 -N "" -f $t/k&&$(dirname $0)/agi-sign $i<$t/k.pub>$t/k-cert.pub&&ssh-add -q -t ${KEY_LIFE:-300} $t/k;r=$?;shred -u $t/k 2>/dev/null;rm -rf $t;exit $r
~~~~~
### pre-receive.patched (740 B, sha256 fea9a03d7f6db77f)
~~~~~
#!/bin/sh
# pre-receive on a box we own: the row's opts set AGI_POST; a login writes only refs/agi/<itself>/*, every new commit signed by itself
# and dated within S s of now (the login proved the cert valid NOW, so the signature date cannot be backdated past it)
S=${AGI_SKEW:-120};T=$(date +%s);A=$(git config agi.allowed)
while read o n r;do case $r in refs/agi/$AGI_POST/*);;*)echo "refused: $r for ${AGI_POST:-none}";exit 1;;esac
 for c in $(git rev-list $n --not --all);do git -c gpg.ssh.allowedSignersFile=$A verify-commit --raw $c 2>&1|grep -q "for $AGI_POST with"&&[ $((T-$(git log -1 --format=%ct $c))) -lt $S ]&&[ $(($(git log -1 --format=%ct $c)-T)) -lt $S ]||{ echo "refused: $c not signed by $AGI_POST now";exit 1;};done;done
~~~~~
### xb.patched (1091 B, sha256 2f39c6bd8d2e75d8)
~~~~~
#!/bin/sh
# xb send REMOTE TO MSG | xb recv REMOTE -- a message = ONE signed commit on refs/agi/<from>/<to>; any remote, the same verbs.
# recv keeps a commit only if fsck passes AND its signer's cert principal IS <from> (the CA line in agi.allowed); else [refused].
P=${AGI_POST:?};V="git -c gpg.ssh.allowedSignersFile=$(git config agi.allowed) verify-commit --raw"
case $1 in
send)r=refs/agi/$P/$3;p=$(git rev-parse -q --verify $r)&&p="-p $p";t=$(git hash-object -w -t tree /dev/null)
 c=$(echo "$4"|git -c gpg.format=ssh -c user.signingkey="key::$(ssh-add -L|sed -n '/cert-v01/{p;q;}')" commit-tree -S $p $t)&&git update-ref $r $c&&git push -q $2 $r;;
recv)git -c transfer.fsckObjects=1 fetch -q $2 "+refs/agi/*/$P:refs/xb/*/$P"||exit 1
 git for-each-ref --format='%(refname)' refs/xb|while read r;do f=${r#refs/xb/};f=${f%/*};s=refs/xbseen/$f/$P
  for c in $(git rev-list --reverse $r --not $(git rev-parse -q --verify $s));do
   if $V $c 2>&1|grep -q "for $f with";then echo "[$f] $(git log -1 --format=%s $c)";git update-ref $s $c;else echo "[refused] $f $c";break;fi;done;done;;
esac
~~~~~
### 50-agi.conf.patched (212 B, sha256 c71939dd5d4691d7)
~~~~~
Match User agi-*
  TrustedUserCAKeys /etc/agi/dc/ca.pub
  AuthorizedPrincipalsCommand /etc/agi/dc-principals %u %i
  AuthorizedPrincipalsCommandUser nobody
  AuthorizedKeysFile none
  RevokedKeys /etc/agi/dc/krl
~~~~~

## Test output (sanitized)
~~~~~text
scratch run 2026-10-01T07:51:46Z   ssh: OpenSSH_9.6p1 Ubuntu-3ubuntu13.19, OpenSSL 3.0.13 30 Jan 2024   git: git version 2.43.0

######## 1 THE TEST CA (throwaway ed25519): the private half goes into a CA AGENT and the file is shredded; a second CA = 'another CA'
CA public: 256 SHA256:CRAnlCX/D8f5f7U1GnRXuk4aAwvIrOUM7hhtmb7hPVM test-ca (ED25519)
CA private key file after loading: none ; the CA agent lists: 256 SHA256:CRAnlCX/D8f5f7U1GnRXuk4aAwvIrOUM7hhtmb7hPVM test-ca (ED25519)
other CA (file, shredded at the end): 256 SHA256:EmHcCJS8l3Cd3xt+KtMb5UkmOVN7K/Z9bf2kGFpgJ9Q other-ca (ED25519)

######## 2 THE §U DIRECTORY MATRIX + dc-project / dc-principals
$ dc-project enc < matrix > $DC/rows
[rc=0]
--- rows for box 'enc' (rid = 16 hex of sha256 over the row line = the cert key-id)
5bf564ba77f61a36 | enc | <user> | owner-standin | -5m:20261001140000Z | restrict,command="capsule-login"
c9b9950e023d8258 | enc | <user> | dg5 | -5m:+10m | restrict,command="agi-git dg5"
9d0b6143f8bdbb5a | enc | <user> | prime | -5m:+10m | restrict,command="agi-git prime"
1ddf1cf25999a604 | enc | <user> | ptyman | -5m:+10m | restrict,pty
c4882ee7a3f3b984 | enc | <user> | envprobe | -5m:+10m | restrict,command="capsule-login",environment="AGI_POST=probe"
e88736bcb47470d8 | enc | <user> | old-standin | 20260101:20260102 | restrict,command="capsule-login"
4d18661230513ac8 | enc | <user> | bare | -5m:+10m | 
f90d75e336040dd8 | * | <user> | wild | -5m:+10m | restrict
RESULT U-P1 PASS -- dc-project enc projects the 7 enc rows + the '*' row = 8, never a box2 row (8 rows)
$ dc-project box2 < matrix | wc -l
box2 rows: 2
$ dc-project enc < matrix | cmp - $DC/rows   (U9 CHECK, clean)
[rc=0]
RESULT U9a PASS -- CHECK clean: rc 0
CHECK after one hand-added row: rc=1
RESULT U9b PASS -- CHECK dirty after a hand-added row: rc 1
rid owner-standin=5bf564ba77f61a36 dg5=c9b9950e023d8258 prime=9d0b6143f8bdbb5a ptyman=1ddf1cf25999a604 old-standin=e88736bcb47470d8 bare=4d18661230513ac8
--- dc-principals <user> <rid>  (what sshd's AuthorizedPrincipalsCommand would get)
dc-principals <user> [owner-standin]  -> [restrict,command="capsule-login" owner-standin]
dc-principals <user> [dg5]  -> [restrict,command="agi-git dg5" dg5]
dc-principals <user> [ptyman]  -> [restrict,pty ptyman]
dc-principals <user> [bare]  -> []
dc-principals <user> bogus-rid -> []   wrong user -> []
RESULT U-P2 PASS -- dc-principals: standin row -> restrict,command + principal; bare row (empty opts) -> nothing (fail closed)

######## 3 agi-sign round-trips (verbatim piece; CA only in the CA agent)
$ agi-sign <rid owner-standin> < k.pub   (then ssh-keygen -L)
[rc=0]
        Type: ssh-ed25519-cert-v01@openssh.com user certificate
        Public key: ED25519-CERT SHA256:tx8CmU8F77P90dNCEauSM6PgyRQucqq4XovnTn2A/ls
        Signing CA: ED25519 SHA256:CRAnlCX/D8f5f7U1GnRXuk4aAwvIrOUM7hhtmb7hPVM (using ssh-ed25519)
        Key ID: "5bf564ba77f61a36"
        Serial: 1790841106640010246
        Valid: from 2026-10-01T07:46:46 to 2026-10-01T14:00:00
        Principals: 
                owner-standin
        Critical Options: 
                force-command capsule-login
        Extensions: (none)
RESULT SIGN1 PASS -- agi-sign: key-id = rid, principal owner-standin, valid ends 2026-10-01T14:00:00, critical option force-command capsule-login, extensions none
ptyman row (restrict,pty):  Critical Options: (none) Extensions: permit-pty 
RESULT SIGN2 PASS -- restrict,pty row -> permit-pty only
agi-sign on the bare (empty opts) row: rc=3
RESULT SIGN3 PASS -- empty opts -> signer exit 3
agi-sign on an unknown rid: rc=3
RESULT SIGN4 PASS -- unknown rid -> exit 3
agi-sign with the CA agent EMPTY (window closed): rc=255
RESULT SIGN5 PASS -- window closed -> no cert (rc != 0)
(CA window re-armed with a fresh test CA: 256 SHA256:3M4uxXTvrcXbt8nNzj0mNzTz4JAlhRTrQsN3rWsSWZk test-ca (ED25519))

######## 4 §X THE STAND-IN: key generated to tmpfs, ssh-add into a PRIVATE agent, file shredded+deleted at once
tmpfs dir: tmpfs (0700: 700)
agi-sign rc=0
ssh-add rc=0
files left in the tmpfs dir: 0 ; key file on disk anywhere under scratch: 0
--- the stand-in agent holds:
    256 SHA256:QXQ0NeqOq8h2ksuHOVVsNPTdZR5T/CNUZlNtEwy8fWU owner-standin (ED25519)
    256 SHA256:QXQ0NeqOq8h2ksuHOVVsNPTdZR5T/CNUZlNtEwy8fWU owner-standin (ED25519-CERT)
--- ssh-keygen -L on the stand-in cert (read back from the agent):
            Type: ssh-ed25519-cert-v01@openssh.com user certificate
            Public key: ED25519-CERT SHA256:QXQ0NeqOq8h2ksuHOVVsNPTdZR5T/CNUZlNtEwy8fWU
            Signing CA: ED25519 SHA256:3M4uxXTvrcXbt8nNzj0mNzTz4JAlhRTrQsN3rWsSWZk (using ssh-ed25519)
            Key ID: "5bf564ba77f61a36"
            Serial: 1790841106969119651
            Valid: from 2026-10-01T07:46:46 to 2026-10-01T14:00:00
            Principals: 
                    owner-standin
            Critical Options: 
                    force-command capsule-login
            Extensions: (none)
RESULT X-KEY PASS -- stand-in key lives ONLY in the agent: 0 files left on tmpfs/scratch; agent has key + cert
stand-in agent lifetime: ssh-add -t 3600 (the agent drops it after 1 h; the CERT itself stays valid until 2026-10-01T14:00:00)

######## 5 THE SCRATCH sshd'S: 127.0.0.1 only, own user, throwaway host key, UsePAM no, StrictModes no
--- config A: port 40225; drop-in:
    Match User <user>
      TrustedUserCAKeys /tmp/agi-uvwx/scratch/dc/ca.pub
      AuthorizedPrincipalsCommand /usr/bin/env DC=/tmp/agi-uvwx/scratch/dc /bin/sh /tmp/agi-uvwx/scratch/bin/dc-principals %u %i
      AuthorizedPrincipalsCommandUser <user>
    sshd -t rc=0
--- config B: port 47103; drop-in:
    Match User <user>
      TrustedUserCAKeys /tmp/agi-uvwx/scratch/dc/ca.pub
      AuthorizedPrincipalsCommand /usr/bin/env DC=/tmp/agi-uvwx/scratch/dc /bin/sh /tmp/agi-uvwx/scratch/bin/dc-principals %u %i
      AuthorizedPrincipalsCommandUser <user>
      AuthorizedKeysFile none
      RevokedKeys /tmp/agi-uvwx/scratch/dc/krl
    sshd -t rc=0
--- config V: port 49251; drop-in:
    Match User agi-*
      TrustedUserCAKeys /tmp/agi-uvwx/scratch/dc/ca.pub
      AuthorizedPrincipalsCommand /usr/bin/env DC=/tmp/agi-uvwx/scratch/dc /bin/sh /tmp/agi-uvwx/scratch/bin/dc-principals %u %i
      AuthorizedPrincipalsCommandUser <user>
    sshd -t rc=0
--- config D: port 39155; drop-in:
    # D: the doc's lines with the command given DIRECTLY (not via /usr/bin/env): shows sshd's safe-path rule on a non-root-owned script
    Match User <user>
      TrustedUserCAKeys /tmp/agi-uvwx/scratch/dc/ca.pub
      AuthorizedPrincipalsCommand /tmp/agi-uvwx/scratch/bin/dc-principals %u %i
      AuthorizedPrincipalsCommandUser <user>
    sshd -t rc=0
--- Match scoping + the owner's existing path, read by sshd -T (no login):
config A as user [<user>]: port 40225;passwordauthentication no;trustedusercakeys <S>/dc/ca.pub;authorizedkeysfile <S>/authorized_keys;
config V as user [<user>]: port 49251;passwordauthentication no;trustedusercakeys none;authorizedkeysfile <S>/authorized_keys;
config V as user [agi-capsule]: port 49251;passwordauthentication no;trustedusercakeys <S>/dc/ca.pub;authorizedkeysfile <S>/authorized_keys;
config V as user [somebody]: port 49251;passwordauthentication no;trustedusercakeys none;authorizedkeysfile <S>/authorized_keys;
--- the REAL drop-in text, parsed read-only by sshd -t / -T against a scratch main config (no /etc file is read for the check):
real drop-in [doc]: sshd -t rc=0 ; as agi-capsule: trustedusercakeys /etc/agi/dc/ca.pub;revokedkeys none;authorizedprincipalscommand /etc/agi/dc-principals %u %i;authorizedprincipalscommanduser nobody;authorizedkeysfile /tmp/agi-uvwx/scratch/authorized_keys; ; as the owner's user: trustedusercakeys none;revokedkeys none;authorizedprincipalscommand none;authorizedkeysfile <S>/authorized_keys;
RESULT REAL-doc PASS -- sshd -t accepts the doc drop-in text (paths /etc/agi/..), an Include'd Match, rc 0
real drop-in [patched]: sshd -t rc=0 ; as agi-capsule: trustedusercakeys /etc/agi/dc/ca.pub;revokedkeys /etc/agi/dc/krl;authorizedprincipalscommand /etc/agi/dc-principals %u %i;authorizedprincipalscommanduser nobody;authorizedkeysfile none; ; as the owner's user: trustedusercakeys none;revokedkeys none;authorizedprincipalscommand none;authorizedkeysfile <S>/authorized_keys;
RESULT REAL-patched PASS -- sshd -t accepts the patched drop-in text (paths /etc/agi/..), an Include'd Match, rc 0
(config B adds AuthorizedKeysFile none + RevokedKeys) as user [<user>]: revokedkeys <S>/dc/krl;authorizedkeysfile none;
RESULT M-SCOPE PASS -- an Include'd Match does not leak: Port/globals after the Include still parse (sshd -t rc 0 for A B V)
sshd A listening 127.0.0.1:40225 (pid file ok)
sshd B listening 127.0.0.1:47103 (pid file ok)
sshd V listening 127.0.0.1:49251 (pid file ok)
sshd D listening 127.0.0.1:39155 (pid file ok)
Server listening on 127.0.0.1 port 40225.

######## 6 (a) the agent-held stand-in logs in and runs ONLY the forced capsule-login stub  [config A]
$ ssh -p A <stand-in via private agent> ask-0042   (the dummy code on stdin)
STUB capsule-login argc=0 args=[] orig=[ask-0042] tty=none stdin_bytes=15 post=unset
[rc=0]
RESULT a1 PASS -- stand-in cert logs in; the FORCED command ran with the ask-id only in SSH_ORIGINAL_COMMAND, code on stdin
    sshd log: Failed publickey for <user> from 127.0.0.1 port 60928 ssh2: ED25519 SHA256:QXQ0NeqOq8h2ksuHOVVsNPTdZR5T/CNUZlNtEwy8fWU
    sshd log: Accepted publickey for <user> from 127.0.0.1 port 60928 ssh2: ED25519-CERT SHA256:QXQ0NeqOq8h2ksuHOVVsNPTdZR5T/CNUZlNtEwy8fWU ID 5bf564ba77f61a36 (serial 1790841106969119651) CA ED25519 SHA256:3M4uxXTvrcXbt8nNzj0mNzTz4JAlhRTrQsN3rWsSWZk
asking for another command ('id; ...'): STUB capsule-login argc=0 args=[] orig=[id; echo pwned] tty=none stdin_bytes=2 post=unset
RESULT a2 PASS -- U1b: asking for another command -> the forced command ran instead (orig kept in SSH_ORIGINAL_COMMAND)
asking for a shell (no command, -T): STUB capsule-login argc=0 args=[] orig=[] tty=none stdin_bytes=2 post=unset
RESULT a3 PASS -- no command asked -> still only the stub (orig empty)
asking for a pty + a command: PTY allocation request failed on channel 0  
RESULT a4 PASS -- restrict: a pty is refused (ssh -tt: 'PTY allocation request failed'; no tty reached the stub)
asking for a remote forward: Error: remote port forwarding failed for listen port 0  
RESULT a5 PASS -- restrict: remote forward refused (ssh reports the forward failed)
row opts carry environment="AGI_POST=probe" (no PermitUserEnvironment in the 4 lines): STUB capsule-login argc=0 args=[] orig=[ask-4] tty=none stdin_bytes=2 post=unset
RESULT a6 PASS -- environment= in a row's opts is NOT applied by the 4 Match lines (post=unset): a row cannot set AGI_POST without PermitUserEnvironment
-- config D: the same login, but AuthorizedPrincipalsCommand is the script path itself (owned by the scratch user, not root):
rc=255 <user>@127.0.0.1: Permission denied (publickey).
    sshd log: Failed publickey for <user> from 127.0.0.1 port 33146 ssh2: ED25519 SHA256:QXQ0NeqOq8h2ksuHOVVsNPTdZR5T/CNUZlNtEwy8fWU
    sshd log: Unsafe AuthorizedPrincipalsCommand "/tmp/agi-uvwx/scratch/bin/dc-principals": bad ownership or modes for file /tmp/agi-uvwx/scratch/bin/dc-principals
    sshd log: Certificate does not contain an authorized principal
    sshd log: Failed publickey for <user> from 127.0.0.1 port 33146 ssh2: ED25519-CERT SHA256:QXQ0NeqOq8h2ksuHOVVsNPTdZR5T/CNUZlNtEwy8fWU ID 5bf564ba77f61a36 (serial 1790841106969119651) CA ED25519 SHA256:3M4uxXTvrcXbt8nNzj0mNzTz4JAlhRTrQsN3rWsSWZk
    sshd log: Connection closed by authenticating user <user> 127.0.0.1 port 33146 [preauth]
RESULT a7 PASS -- sshd refuses a non-root-owned AuthorizedPrincipalsCommand path (so the real script must be root-owned: /etc/agi/dc-principals)

######## 7 (b) a cert signed by ANOTHER throwaway CA, key-id = the LIVE stand-in rid, right principal  [config A]
            Signing CA: ED25519 SHA256:EmHcCJS8l3Cd3xt+KtMb5UkmOVN7K/Z9bf2kGFpgJ9Q (using ssh-ed25519)
            Key ID: "5bf564ba77f61a36"
    --
            Principals: 
<user>@127.0.0.1: Permission denied (publickey).
[rc=255]
    sshd log: Failed publickey for <user> from 127.0.0.1 port 60938 ssh2: ED25519 SHA256:QXQ0NeqOq8h2ksuHOVVsNPTdZR5T/CNUZlNtEwy8fWU
    sshd log: Accepted publickey for <user> from 127.0.0.1 port 60938 ssh2: ED25519-CERT SHA256:QXQ0NeqOq8h2ksuHOVVsNPTdZR5T/CNUZlNtEwy8fWU ID 5bf564ba77f61a36 (serial 1790841106969119651) CA ED25519 SHA256:3M4uxXTvrcXbt8nNzj0mNzTz4JAlhRTrQsN3rWsSWZk
    sshd log: Failed publickey for <user> from 127.0.0.1 port 60950 ssh2: ED25519 SHA256:QXQ0NeqOq8h2ksuHOVVsNPTdZR5T/CNUZlNtEwy8fWU
    sshd log: Accepted publickey for <user> from 127.0.0.1 port 60950 ssh2: ED25519-CERT SHA256:QXQ0NeqOq8h2ksuHOVVsNPTdZR5T/CNUZlNtEwy8fWU ID 5bf564ba77f61a36 (serial 1790841106969119651) CA ED25519 SHA256:3M4uxXTvrcXbt8nNzj0mNzTz4JAlhRTrQsN3rWsSWZk
    sshd log: Failed publickey for <user> from 127.0.0.1 port 57814 ssh2: ED25519 SHA256:QXQ0NeqOq8h2ksuHOVVsNPTdZR5T/CNUZlNtEwy8fWU
    sshd log: Accepted publickey for <user> from 127.0.0.1 port 57814 ssh2: ED25519-CERT SHA256:QXQ0NeqOq8h2ksuHOVVsNPTdZR5T/CNUZlNtEwy8fWU ID 5bf564ba77f61a36 (serial 1790841106969119651) CA ED25519 SHA256:3M4uxXTvrcXbt8nNzj0mNzTz4JAlhRTrQsN3rWsSWZk
RESULT b PASS -- other-CA cert refused (rc 255, no stub output)

######## 8 (c) an EXPIRED cert (row old-standin valid 20260101:20260102, signed through agi-sign into its own agent)  [config A]
agi-login (patched) old-standin rc=0
            Key ID: "e88736bcb47470d8"
            Valid: from 2026-01-01T00:00:00 to 2026-01-02T00:00:00
<user>@127.0.0.1: Permission denied (publickey).
[rc=255]
    sshd log: Failed publickey for <user> from 127.0.0.1 port 57848 ssh2: ED25519 SHA256:ITWlgI//idM/5ntetwyJ82F+iKJ7wioU5TwHa9o3F7k
    sshd log: Certificate invalid: expired
    sshd log: Failed publickey for <user> from 127.0.0.1 port 57848 ssh2: ED25519-CERT SHA256:ITWlgI//idM/5ntetwyJ82F+iKJ7wioU5TwHa9o3F7k ID e88736bcb47470d8 (serial 1790841110153115733) CA ED25519 SHA256:3M4uxXTvrcXbt8nNzj0mNzTz4JAlhRTrQsN3rWsSWZk
    sshd log: Connection closed by authenticating user <user> 127.0.0.1 port 57848 [preauth]
RESULT c PASS -- expired cert refused (rc 255); sshd log says expired

######## 9 (d) a matrix row WITHOUT restrict (U9c: empty opts), cert signed OUTSIDE agi-sign (permissive, no -O clear)  [config A]
    permissive cert:  Principals: bare Critical Options: (none) Extensions: permit-X11-forwarding permit-agent-forwarding permit-port-forwarding permit-pty permit-user-rc 
<user>@127.0.0.1: Permission denied (publickey).
[rc=255]
RESULT d PASS -- no-restrict row refused (rc 255): dc-principals prints nothing for it, sshd never gets a principal
    sshd log: Failed publickey for <user> from 127.0.0.1 port 57854 ssh2: ED25519 SHA256:ItsFMyEPNfPfVFUWd6uZYwqSJmxWfB0WW9f4uv+uF/w
    sshd log: Certificate does not contain an authorized principal
    sshd log: Failed publickey for <user> from 127.0.0.1 port 57854 ssh2: ED25519-CERT SHA256:ItsFMyEPNfPfVFUWd6uZYwqSJmxWfB0WW9f4uv+uF/w ID 4d18661230513ac8 (serial 7) CA ED25519 SHA256:3M4uxXTvrcXbt8nNzj0mNzTz4JAlhRTrQsN3rWsSWZk
    sshd log: Connection closed by authenticating user <user> 127.0.0.1 port 57854 [preauth]
U2 key-id = a row of box2: rc=255 <user>@127.0.0.1: Permission denied (publickey).
RESULT U2 PASS -- key-id = another box's row refused (rc 255)
U8 hostile key-id: rc=255 ; files created by it: 0
RESULT U8 PASS -- key-id with ; spaces $(...) refused, nothing executed

######## 10 (e) a PLAIN key in the scratch authorized_keys for the SAME user: the existing path untouched
-- config A (the doc's 4 Match lines only, Match applies to this user):
PLAIN-OK-42 [rc=0]
RESULT e1 PASS -- plain key logs in as before on A (no forced command, free shell command ran)
-- config V (the doc's Match User agi-* pattern VERBATIM; this user is not an agi-* user = the owner's real login):
PLAIN-OK-V [rc=0]
RESULT e2 PASS -- plain key logs in on V: the Match block does not touch a non-agi user
stand-in cert against V (user not matched by agi-*): rc=255 <user>@127.0.0.1: Permission denied (publickey).
RESULT e3 PASS -- the same stand-in cert is NOT honoured for a non-agi user (rc 255): certificates only open the agi users
-- config B (A + AuthorizedKeysFile none + RevokedKeys, the §V box line the 4 lines omit): plain key for the matched user:
<user>@127.0.0.1: Permission denied (publickey).
 [rc=255]
RESULT e4 PASS -- B: plain key refused for the Match user (AuthorizedKeysFile none) - U6
B: the stand-in still logs in: rc=0 STUB capsule-login argc=0 args=[] orig=[ask-3] tty=none stdin_bytes=2 post=unset
RESULT e5 PASS -- B: cert path unaffected by the two extra lines

######## 11 extras: U3 row edited / SI5 row deleted -> the old cert refused; KRL by serial (config B)
SI5 stand-in row deleted: rc=255
RESULT SI5 PASS -- row deleted -> stand-in refused at its next login (rc 255)
U3 one cell of the row edited (valid 14:00 -> 13:00): new rid 269c03e28b0c60eb (was 5bf564ba77f61a36)
old cert vs the edited row: rc=255
RESULT U3 PASS -- old cert refused after one cell edit (rid changed)
row restored: rc=0
RESULT U3r PASS -- row restored -> the same cert logs in again
stand-in cert serial 1790841106969119651; revoke it in the KRL
B with the serial in the KRL: rc=255
RESULT KRL PASS -- serial revoked in the KRL -> refused on B (RevokedKeys, which the 4 lines lack)
A (4 lines, no RevokedKeys) same cert: rc=0
RESULT KRLA PASS -- A has no RevokedKeys: the revoked serial still logs in (the hole the patched drop-in B closes)
B with RevokedKeys naming a file that does NOT exist (krl deleted): rc=255 <user>@127.0.0.1: Permission denied (publickey).
    sshd log: Error checking authentication key ED25519 SHA256:QXQ0NeqOq8h2ksuHOVVsNPTdZR5T/CNUZlNtEwy8fWU in revoked keys file /tmp/agi-uvwx/scratch/dc/krl: No such file or directory
    sshd log: Failed publickey for <user> from 127.0.0.1 port 53112 ssh2: ED25519 SHA256:QXQ0NeqOq8h2ksuHOVVsNPTdZR5T/CNUZlNtEwy8fWU
    sshd log: Error checking authentication key ED25519-CERT SHA256:QXQ0NeqOq8h2ksuHOVVsNPTdZR5T/CNUZlNtEwy8fWU in revoked keys file /tmp/agi-uvwx/scratch/dc/krl: No such file or directory
    sshd log: Failed publickey for <user> from 127.0.0.1 port 53112 ssh2: ED25519-CERT SHA256:QXQ0NeqOq8h2ksuHOVVsNPTdZR5T/CNUZlNtEwy8fWU ID 5bf564ba77f61a36 (serial 1790841106969119651) CA ED25519 SHA256:3M4uxXTvrcXbt8nNzj0mNzTz4JAlhRTrQsN3rWsSWZk
    sshd log: Connection closed by authenticating user <user> 127.0.0.1 port 53112 [preauth]
RESULT KRL0 PASS -- a MISSING RevokedKeys file fails CLOSED: every cert login of the Match user is refused -> the (empty) KRL must exist before the reload

######## 12 agi-login: the verbatim piece vs the patched one; rotation; no key files
verbatim (as §X/§V call it: a PRINCIPAL), from its own dir:
verbatim agi-login owner-standin: rc=3 ; keys in agent: 0
RESULT L0 PASS -- verbatim agi-login with a PRINCIPAL -> FAILS (the arg goes to agi-sign as a RID: exit 3)
verbatim agi-login <rid> from its own dir: rc=0 ; keys in agent: 2
RESULT L0b PASS -- verbatim works given a RID, run from its own dir
/tmp/agi-uvwx/scratch/bin/agi-login-v: 3: ./agi-sign: not found
verbatim from another cwd (./agi-sign): rc=127
verbatim with XDG_RUNTIME_DIR unset: mktemp: option requires an argument -- 'p'
patched agi-login dg5 #1 rc=0
patched agi-login dg5 #2 rc=0
agent after two logins (fingerprints):
    SHA256:vhykxY0uq4U+c9844ukSAZo0NsPpFAd0xoTtAnxS7yA (ED25519)
    SHA256:vhykxY0uq4U+c9844ukSAZo0NsPpFAd0xoTtAnxS7yA (ED25519-CERT)
    SHA256:zO5EW4hlpaBiJySSekt9KtY9PfFZsfsrmY+qTGzaXNE (ED25519)
    SHA256:zO5EW4hlpaBiJySSekt9KtY9PfFZsfsrmY+qTGzaXNE (ED25519-CERT)
RESULT L1 PASS -- patched: two logins -> 4 identities (2 fresh keys + 2 certs); 2 DIFFERENT fingerprints (a cert shows its key fingerprint)
files left on tmpfs after the logins: 0 ; key files in scratch: 0
RESULT L2 PASS -- no key file left on tmpfs
unknown principal: rc=3
RESULT L3 PASS -- patched: unknown principal/rid -> rc 3, nothing added
patched with XDG_RUNTIME_DIR unset: rc=0 (falls back to /dev/shm); agent now holds 6 identities
RESULT L4 PASS -- patched: XDG_RUNTIME_DIR unset -> /dev/shm fallback works

######## 13 xb + pre-receive (W): signed commits; hub = a bare repo behind the SCRATCH sshd (rows dg5/prime -> agi-git wrapper sets AGI_POST); 'GitHub' = a bare file remote, no hook
--- 13-0 the VERBATIM xb with git 2.43 (no user.signingkey in the repo):
fatal: either user.signingkey or gpg.ssh.defaultKeyCommand needs to be configured [rc=128]
RESULT XB-V PASS -- verbatim xb send fails on git 2.43: 'either user.signingkey or gpg.ssh.defaultKeyCommand needs to be configured'
--- 13a the VERBATIM pre-receive as the hub hook (xb.patched signs; the hook is the piece as extracted) (it carries the literal '<U: allowed>'):
remote: hooks/pre-receive: 6: cannot open U:: No such file        
remote: refused: 0eb7b0fca91a88701dd9437e926b73d90eb0da43 not signed by dg5 now        
To ssh://dc/tmp/agi-uvwx/scratch/hub.git
 ! [remote rejected] refs/agi/dg5/prime -> refs/agi/dg5/prime (pre-receive hook declined)
error: failed to push some refs to 'ssh://dc/tmp/agi-uvwx/scratch/hub.git' [rc=1]
RESULT XB0 PASS -- verbatim pre-receive refuses EVERY push (the '<U: allowed>' placeholder is a shell syntax error / bad redirect)
--- 13b the PATCHED pre-receive (agi.allowed read from the hub's git config):
xb send hub prime 'hello over the mesh' (as dg5): rc=0 
RESULT XB1 PASS -- xb send over the scratch-sshd hub (cert login dg5 -> agi-git -> pre-receive.patched): lands in refs/agi/dg5/prime
the signature as the hub reads it:
    Good "git" signature for dg5 with ED25519-CERT key SHA256:62As5BFWpYdr5qZWGeh+f2NQ+oqiHwOvSo/qCErKVIo
xb recv hub (as prime): [dg5] hello over the mesh [rc=0]
RESULT XB2 PASS -- xb recv prints: [dg5] hello over the mesh
recv again: []
RESULT XB2b PASS -- a second recv delivers nothing
--- GitHub stand-in (a file remote, no hook), the same verbs:
send rc=0 
recv: [dg5] hello over github
RESULT XB3 PASS -- same verbs over a file remote: [dg5] hello over github
--- a cert-less agent (plain key only):
xb.patched send with no cert in the agent: rc=1 error: Couldn't load public key /tmp/.git_signing_key_tmpTYJirg: No such file or directory?
RESULT XB4a PASS -- xb.patched cannot sign without a cert in the agent (fails closed at the sender)
forging a commit signed by the plain key alone (outside xb) and pushing it to the GitHub stand-in:
forge push rc=0
recv: [refused] dg5 0771b6850e49839af1d5e6b8736151f4af057b61
RESULT XB4 PASS -- a plain-key (cert-less) signature is refused by recv: [refused] dg5 <sha>, not delivered
--- X6a forgery to the hub: dg5's cert login pushes into refs/agi/prime/* (xb run with AGI_POST=prime so it signs and targets that namespace):
remote: refused: refs/agi/prime/hq for dg5        
To ssh://dc/tmp/agi-uvwx/scratch/hub.git
 ! [remote rejected] refs/agi/prime/hq -> refs/agi/prime/hq (pre-receive hook declined)
error: failed to push some refs to 'ssh://dc/tmp/agi-uvwx/scratch/hub.git'
RESULT X6a PASS -- hub pre-receive refuses refs/agi/prime/* from the dg5 login
--- X6b the same forgery to the hook-less GitHub stand-in: the push lands, recv decides:
push rc=0
recv as prime: [refused] dg5 0771b6850e49839af1d5e6b8736151f4af057b61
[refused] prime 2b6e7f6d3491bb78a6e1b278d7859d6196a85568
RESULT X6b PASS -- forgery lands on gh, but recv prints [refused] prime <sha> and delivers nothing
--- X11b backdated 30 min through the hub:
remote: refused: 528da0d7095b044545a4d9e76fab80dd7751a7f8 not signed by dg5 now        
To ssh://dc/tmp/agi-uvwx/scratch/hub.git
 ! [remote rejected] refs/agi/dg5/prime -> refs/agi/dg5/prime (pre-receive hook declined)
RESULT X11b PASS -- backdated commit refused by the skew check
--- 5 min in the FUTURE (inside the cert window, beyond S=120) through the hub, hook = the verbatim piece with ONLY the placeholder fixed:
rc=0 
RESULT X11g PASS -- verbatim skew test lets a FUTURE-dated commit through (it only bounds the past)
--- the same with the patched hook:
remote: refused: e0bfef6804bd54ad1ad885635476acecbdfc4455 not signed by dg5 now        
To ssh://dc/tmp/agi-uvwx/scratch/hub.git
 ! [remote rejected] refs/agi/dg5/prime -> refs/agi/dg5/prime (pre-receive hook declined)
RESULT X11f PASS -- future-dated commit refused (the verbatim skew test only bounds the PAST)
a now-dated send after the refusals: rc=0
RESULT X11c PASS -- a now-dated send still lands
--- which identity does the verbatim xb sign with? the agent holds key + cert, listing order (ssh-add -L):
    1: ssh-ed25519
    2: ssh-ed25519-cert-v01@openssh.com

######## 14 sshd log: what the scratch sshd saw (ids are rids; ED25519-CERT = a cert login)
      7 Accepted publickey for <user> from 127.0.0.1 ssh2: ED25519-CERT SHA256:QXQ0NeqOq8h2ksuHOVVsNPTdZR5T/CNUZlNtEwy8fWU ID 5bf564ba77f61a36 (serial 1790841106969119651) CA ED25519 SHA256:3M4uxXTvrcXbt8nNzj0mNzTz4JAlhRTrQsN3rWsSWZk
      7 Accepted publickey for <user> from 127.0.0.1 ssh2: ED25519-CERT SHA256:62As5BFWpYdr5qZWGeh+f2NQ+oqiHwOvSo/qCErKVIo ID c9b9950e023d8258 (serial 1790841114149882044) CA ED25519 SHA256:3M4uxXTvrcXbt8nNzj0mNzTz4JAlhRTrQsN3rWsSWZk
      2 Accepted publickey for <user> from 127.0.0.1 ssh2: ED25519-CERT SHA256:hEz6k4VwFEIxmJk0wMGsWWLP5iFo6ozNGpXCNnX+oDQ ID 9d0b6143f8bdbb5a (serial 1790841114200768548) CA ED25519 SHA256:3M4uxXTvrcXbt8nNzj0mNzTz4JAlhRTrQsN3rWsSWZk
      1 Accepted publickey for <user> from 127.0.0.1 ssh2: ED25519 SHA256:OjnI3Okv+Sjc5r+XuR6xVXmjBvMEYlb61cux0seXy3U
      1 Accepted publickey for <user> from 127.0.0.1 ssh2: ED25519-CERT SHA256:kLUcyZfmfHE0Bw4W25hCzKtikPK8qnnFdTMNMigX31E ID c4882ee7a3f3b984 (serial 1790841109523040501) CA ED25519 SHA256:3M4uxXTvrcXbt8nNzj0mNzTz4JAlhRTrQsN3rWsSWZk

######## SUMMARY
pass=56 fail=0

######## CLEANUP: stop the scratch sshd's + agents, shred every key file, delete the scratch dir
sshd pids stopped: 4 ; agents stopped: 9 ; still alive: 0
scratch dir: deleted ; tmpfs run dir: deleted ; CA private key files: 0 (ca shredded after ssh-add, ca2 shredded with the rest)
listeners left on the scratch ports: 0
~~~~~
