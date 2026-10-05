---
id: config:engine-root
mint_id: c9ebcb4c2c7c4fcbac4b232eb47d76f4
type: config
parents:
  - goal:g7.16.1.11.5
next_edges: []
edited_by: belam
scaffold_hash: 649a07578115c7e3
season: 2
town: core
---

# config:engine-root

EXPANSION of config:engine: the unit template (root's agi-project reads it through sect; a post's extraction loop and the hub's gate do not)
Read only through `sect <name> [REV]`.

## files — depth 2, each whole; extract: sect <name> [REV]
### agi-post@.service (1977 B)
~~~ini
[Unit]
After=agi-ram-main.service
[Service]
User=agi-%i
StateDirectory=agi/%i
WorkingDirectory=/var/lib/agi/%i
EnvironmentFile=-/var/lib/agi/%i.env
Environment=PATH=/var/lib/agi/%i/bin:/opt/agi/bin:/usr/local/bin:/usr/bin:/bin SHELL=/bin/sh DISABLE_AUTOUPDATER=1 AGI_SEAT=%i
Environment=GIT_AUTHOR_NAME=%i GIT_COMMITTER_NAME=%i GIT_AUTHOR_EMAIL=%i@agi GIT_COMMITTER_EMAIL=%i@agi
Environment=PI_CODING_AGENT_DIR=/opt/agi/pi-agent PI_CODING_AGENT_SESSION_DIR=/var/lib/agi/%i/.pi/sessions
RuntimeDirectory=agi-%i
RuntimeDirectoryPreserve=restart
ExecCondition=sh -c '[ ! -e .ssh/out-refused ]||[ .fresh -nt .ssh/out-refused ]||exit 2'
ExecStartPre=awk -F"[= ]" "/some/{exit $$3>40}" /proc/pressure/memory
ExecStartPre=sh -c 'mkdir -p .ssh;[ -d t ]||[ -e .fresh ]||touch .fresh;[ .fresh -nt .ssh/id_ed25519 -a ! -f t/.agi/nodes/.geometry/ring ]&&rm -f .ssh/id_ed25519*;[ -f .ssh/id_ed25519 ]||ssh-keygen -qN "" -ted25519 -f.ssh/id_ed25519'
ExecStartPre=+/usr/bin/env -i PATH=/usr/sbin:/usr/bin:/bin /opt/agi/bin/agi-signers %i
ExecStartPre=sh -c 'mkdir -p .ssh bin .claude hooks;git config --global safe.directory "*";[ -d t ]||{ git -C $O branch posts/%i $AGI_TRUNK;git -C $O worktree add -fq $PWD/t posts/%i;};for e in $O/.agi/nodes/.geometry/engine.md $O/.agi/nodes/.geometry/engine-[pw]*.md;do for x in $(grep -o "^### [^ ]*" $e|cut -c5-);do sed -n "/^### $x /,/^##/{/^~~~/,/^~~~/{//!p}}" $e>bin/$x;done;done;chmod +x bin/*;mv bin/gitconfig .gitconfig;mv bin/settings.json .claude;mkfifo -m620 %t/agi-%i/i;chgrp agi %t/agi-%i/i;[ -e o ]||install -m600 /dev/null o'
ExecStartPre=sh -c 'ls bin/agi-out>/dev/null 2>&1&&exec agi-out;echo agi-out skipped, stale t>&2'
ExecStartPre=+/usr/bin/env -i PATH=/usr/sbin:/usr/bin:/bin /opt/agi/bin/agi-signers %i
ExecStart=sh -c 'exec 3<>%t/agi-%i/i;exec script -qfaO$HOME/o -c agi-run <&3'
StandardOutput=null
ExecStopPost=sh -c agi-flush
SuccessExitStatus=1 SIGTERM
Restart=always
RestartSec=30
Slice=agi.slice
MemoryHigh=4G
[Install]
WantedBy=multi-user.target
~~~


### agi-boot.service (447 B)
~~~ini
[Unit]
After=agi-ram-main.service
Requires=agi-ram-main.service
[Service]
Type=oneshot
RemainAfterExit=yes
TimeoutStartSec=infinity
WorkingDirectory=/data/work/agi
Environment=GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory GIT_CONFIG_VALUE_0=*
ExecStart=sh -c 'echo HEAD:.agi/nodes/.geometry/engine-root.md|git cat-file --batch --follow-symlinks|sed -n "/^### agi-boot /,/^##/{/^~~~/,/^~~~/{//!p}}"|sh -s'
[Install]
WantedBy=multi-user.target
~~~

### agi-boot (1933 B)
~~~sh
#!/bin/sh
R=${AGI_RAM:-/mnt/agi-ram} t=${AGI_TRUNK:-HEAD} o=${AGI_BOOT_OUT:-/run/systemd/system};w=$o/multi-user.target.wants
e=0;f(){ "$@"||{ echo "agi-boot: failed: $*">&2;e=1;};};f setfacl -m g:agi:x $R;f setfacl -m g:agi:--- ${AGI_RAM_STATE:-$R/state};I=$PWD/.agi/sessions/inbox;f mkdir -p $I;f setfacl -m g:agi:rwx $I;f setfacl -d -m g:agi:rwx $I
c(){ git show $t:.agi/config.json|jq -r ".values.local_maxxing.$1";};L=$(c de_live_parents.ceiling_if.loadavg1_lt) P=$(c de_live_parents.ceiling_if.io_psi_some_avg60_lt) N=$(c agi_boot.poll_s) M=$(c agi_boot.wait_max_s) S=$(c agi_boot.space_s)
echo $t:.agi/nodes/.geometry/engine.md|git cat-file --batch --follow-symlinks|sed -n '/^### agi-project /,/^### /{/^~~~/,/^~~~/{//!p}}'|sh -s $o $t||exit 3
f systemctl daemon-reload;s(){ git ls-tree --full-tree --name-only $t .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$t:|"|git cat-file --batch --follow-symlinks|sed -n "/^### $1 /,/^##/{/^~~~/,/^~~~/{//!p}}";};s xai-proxy>/opt/agi/bin/xai-proxy;chmod 755 /opt/agi/bin/xai-proxy;s xai-proxy.service>/etc/systemd/system/xai-proxy.service;systemctl enable --now xai-proxy.service
ok(){ l=;read l _<${AGI_LOADAVG:-/proc/loadavg};i=$(sed -n 's/^some .*avg60=\([0-9.]*\).*/\1/p' ${AGI_PSI_IO:-/proc/pressure/io});[ -n "$l" ]&&[ -n "$i" ]&&awk -v l=$l -v i=$i -v L=$L -v P=$P 'BEGIN{exit !(l<L&&i<P)}';}
rows=$(git show $t:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -r 'select(.boot==true)|.name');[ -n "$rows" ]||{ echo "agi-boot: no boot rows read from $t">&2;e=1;};for p in $rows;do [ -L $w/agi-post@$p.service ]||{ echo "agi-boot: $p not projected (engine v4 row absent), skipped">&2;continue;};[ $n ]&&f sleep $S;s=$(date +%s)
until ok;do [ $(($(date +%s)-s)) -ge $M ]&&{ echo "agi-boot: gate not open after ${M}s, skipping $p">&2;e=1;continue 2;};sleep $N;done
systemctl start agi-post@$p</dev/null||{ echo "agi-boot: start failed $p">&2;e=1;};n=1;done
exit $e
~~~

### box-carry (3246 B)
~~~sh
#!/bin/sh
# box-carry P (ROOT, agi-carry@P.service, woken by P's own refs/box/P): P's refs/box/P/<Q> -> the store of each recipient on this box (pipe, ff-only, strict), or -> the hub when Q's box is elsewhere; re-scanned (max 5x) as long as P's tips keep moving; still moving after the last pass = exit 75 (the unit restarts it)
# box-carry --fetch (the timer): FIRST carry each local post, then push what a failed push left in C, then the hub's refs/box/*/Q -> Q's store, for a Q here and a sender elsewhere
# trust: root reads the matrix at a PINNED 40-hex trunk sha (a post can write AGI_REPO's refs, never a sha's bytes; replace refs ignored) and runs git only in its OWN repos (C, AGI_REPO); a post's store is read and written AS that post; a ref name is data (validated, an argument, never script text); every edge is the box script's own a() at that sha, both for local, hub-bound and hub-sourced refs
export GIT_NO_REPLACE_OBJECTS=1
S=${AGI_STORES:-/var/lib/agi};R=${AGI_RUN:-runuser};B=${AGI_BOX:?};H=$AGI_HUB;C=${AGI_CARRY:-$S/carry.git};m=refs/box;AGI_TRUNK=${AGI_TRUNK:?}
case $AGI_TRUNK in *[!0-9a-f]*)exit 1;;esac;[ ${#AGI_TRUNK} = 40 ]||exit 1;export AGI_TRUNK
cd ${AGI_REPO:?}||exit 1;eval "$(sect box $AGI_TRUNK|sed -n '/^a(){/p')";type a>/dev/null||exit 1
W=$(git show $AGI_TRUNK:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -r '"\(.name) \(.box//"")"');[ -n "$W" ]||exit 1
bx(){ echo "$W"|awk -v n=$1 '$1==n{print $2}';}
ok(){ case $1 in ""|-*|*[!A-Za-z0-9._-]*)return 1;;esac;}
as(){ u=$1;shift;case $u in -)"$@";;*)case $R in runuser)runuser -u agi-$u -- "$@";;none)"$@";;*)return 1;;esac;;esac;}
put(){ n=$(as $1 git -C $2 rev-parse "$5")||return;o=$(as $3 git -C $4 rev-parse -q --verify "$5");[ "$o" = "$n" ]&&return
 { echo $n;[ -z "$o" ]||echo ^$o;}|as $1 git -C $2 pack-objects --revs --stdout|as $3 sh -c 'git -C $0 unpack-objects -q --strict&&{ [ -z "$2" ]||git -C $0 merge-base --is-ancestor $2 $1||exit 3;git -C $0 update-ref $3 $1 "$2";}' $4 $n "$o" "$5"||{ echo "[carry-failed] $5 -> $4">&2;return 1;};}
[ -d $C ]||git init -q --bare $C
if [ "$1" = --fetch ];then for p in $(echo "$W"|awk -v b=$B '$2==b{print $1}');do ok $p&&[ -d $S/$p/g.git ]&&timeout 10 sh $0 $p;done;[ -n "$H" ]||exit 0
 for r in $(git -C $C for-each-ref --format='%(refname)' $m);do f=${r#$m/};f=${f%/*};q=${r##*/};ok $f&&ok $q&&[ "$(bx $f)" = $B ]&&[ "$(bx $q)" != $B ]&&a $f $q&&git -C $C push -q $H $r:$r;done
 git -C $C -c transfer.fsckObjects=1 fetch -q $H "$m/*:$m/*"
 for r in $(git -C $C for-each-ref --format='%(refname)' $m);do f=${r#$m/};f=${f%/*};q=${r##*/};ok $f&&ok $q&&[ "$(bx $q)" = $B ]&&[ "$(bx $f)" != $B ]&&a $f $q&&put - $C $q $S/$q/g.git $r;done
else P=$1;ok $P&&[ -n "$(bx $P)" ]||exit 1;k=;i=0
 while [ $i -lt 5 ];do s=$(as $P git -C $S/$P/g.git for-each-ref --format='%(objectname) %(refname)' $m/$P/);[ "$s" = "$k" ]&&break;k=$s;i=$((i+1))
  for r in $(echo "$s"|cut -d' ' -f2);do q=${r##*/};[ $r = $m/$P/$q ]&&ok $q&&a $P $q||continue
   if [ "$(bx $q)" = $B ];then put $P $S/$P/g.git $q $S/$q/g.git $r;elif [ -n "$H" ];then put $P $S/$P/g.git - $C $r&&git -C $C push -q $H $r:$r;fi;done;done;[ "$(as $P git -C $S/$P/g.git for-each-ref --format='%(objectname) %(refname)' $m/$P/)" = "$k" ]||exit 75;fi;:
~~~

### agi-signers (1727 B)
~~~sh
#!/bin/sh
PATH=/usr/sbin:/usr/bin:/bin;export PATH
# agi-signers POST (ROOT, ExecStartPre=+ of the post unit): the ONE allowed_signers, root-owned, append-only: every generation of every post key; a changed key stamps the old line valid-before and the new one valid-after=NOW, so an old commit still verifies at its own date
# the key file is the POST's: read AS the post (a symlink cannot reach a root-only file), ONE line, strictly `ssh-ed25519 <base64>`, else refused (a post can add no other line, no other principal, no option)
# BOUND: the ring is append-only: revoking a key takes effect only at the post's next start (a stale .pub whose private key is gone leaves the ring one start behind: fail closed); git checks a signature at the COMMIT's own date, which its signer writes: a rotated-out key still verifies a commit it dates inside its own window; rotation does not stop that key backdating, only dating after valid-before
p=$1;S=${AGI_STORES:-/var/lib/agi};F=${AGI_SIGNERS:-$S/allowed_signers};t=$(date -u +%Y%m%d%H%M%SZ);case $p in ""|*[!a-z0-9-]*)exit 1;;esac
case ${AGI_RUN:-runuser} in runuser)k=$(runuser -u agi-$p -- head -c 400 $S/$p/.ssh/id_ed25519.pub);;none)k=$(head -c 400 $S/$p/.ssh/id_ed25519.pub);;*)exit 1;;esac
[ "$(echo "$k"|wc -l)" = 1 ]&&echo "$k"|grep -qE '^ssh-ed25519 AAAAC3NzaC1lZDI1NTE5[A-Za-z0-9+/]{48}( .*)?$'||{ echo "agi-signers: $p key file refused">&2;exit 1;};k=$(echo "$k"|cut -d' ' -f1,2)
touch $F;chmod 644 $F;exec 9>>$F.lock;flock 9;grep -q "^$p@agi namespaces=\"git\",valid-after=\"[0-9Z]*\" $k\$" $F&&exit 0
sed -i "/^$p@agi /{/valid-before/!s/valid-after=\"\([0-9Z]*\)\"/valid-after=\"\1\",valid-before=\"$t\"/}" $F;echo "$p@agi namespaces=\"git\",valid-after=\"$t\" $k">>$F
~~~

### agi-carry@.path (149 B)
~~~ini
[Unit]
Description=box mail wake for %i
StartLimitIntervalSec=0
[Path]
PathChanged=/var/lib/agi/%i/g.git/refs/box/%i
[Install]
WantedBy=paths.target
~~~

### agi-carry@.service (287 B)
~~~ini
[Unit]
StartLimitIntervalSec=0
[Service]
Type=oneshot
TimeoutStartSec=120
Restart=on-failure
RestartSec=5
EnvironmentFile=/etc/agi/carry.env
Environment=GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory PATH=/opt/agi/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=/opt/agi/bin/box-carry %i
~~~

### agi-carry-fetch.timer (88 B)
~~~ini
[Timer]
OnBootSec=60
OnUnitActiveSec=60
AccuracySec=1s
[Install]
WantedBy=timers.target
~~~

### agi-carry-fetch.service (229 B)
~~~ini
[Service]
Type=oneshot
TimeoutStartSec=120
EnvironmentFile=/etc/agi/carry.env
Environment=GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory PATH=/opt/agi/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=/opt/agi/bin/box-carry --fetch
~~~

### agi-land (1855 B)
~~~sh
#!/bin/sh
# agi-land <sender> <post> <sha>: root ff-lands <post>'s <sha> on the trunk, ONE parent edge up: sender = parent(post); a parent with a members cell is an inert group: the land passes to ITS parent; a parent-owner post lands itself; a `lands` cell on the parent narrows which children it takes (absent = all, [] = none).
# each commit in $o..$n signed (root's ring) by the sender or a post under <post> on the parent cells · grow-gate on $o..$n · agi-gate · CAS ff
T=${AGI_TRUNK:-refs/heads/trunk};A=${AGI_RING:?};o=$(git rev-parse -q --verify $T)||exit 1;n=$(git rev-parse -q --verify "$3^{commit}")||exit 1
git merge-base --is-ancestor $o $n||{ echo "refused: not ff";exit 1;};t=$(mktemp -d);trap 'rm -rf $t' EXIT
git show $o:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -r '"\(.name) \(.parent//"")",(select(.members)|"I \(.name)"),(.name as $n|.lands|select(.)|"\($n)>",(.[]|"\($n)>\(.)"))'>$t/p
u(){ x=$1;i=0;while [ "$x" ]&&[ $((i+=1)) -le 32 ];do [ $x = $2 ]&&return;x=$(awk -v n=$x '$1==n{print $2}' $t/p);done;return 1;}
q(){ awk -v n=$1 '$1==n{print $2}' $t/p;};Q=$(q $2);P=$Q;grep -qx "I $Q" $t/p&&P=$(q $Q)
{ [ "$P" != owner ]&&[ "$1" = "$P" ];}||{ [ $1 = $2 ]&&[ "$P" = owner ];}||{ echo "refused: $1 is not the parent of $2";exit 1;}
grep -q "^$Q>" $t/p&&! grep -qx "$Q>$2" $t/p&&{ m=$(sed -n "s/^$Q>\(.\)/\1/p" $t/p|tr '\n' ' ');echo "refused: $Q lands only ${m:-nothing}";exit 1;}
for c in $(git rev-list $o..$n);do s=$(git -c gpg.ssh.allowedSignersFile=$A verify-commit --raw $c 2>&1|sed -n 's/.*signature for \([^@]*\)@agi with.*/\1/p')
[ "$s" ]&&{ [ $s = $1 ]||u $s $2;}||{ echo "refused: $c signed by ${s:-nobody}: not $1, not under $2";exit 1;};done
echo "$o $n $T"|AGI_ALLOWED=$A AGI_TRUNK=$o AGI_NOT=$o grow-gate||exit 1;agi-gate $n||{ echo "refused: engine would not regrow";exit 1;}
git update-ref $T $n $o
~~~

### xai-proxy (2006 B)
~~~py
#!/usr/bin/env python3
"""127.0.0.1 xAI bearer proxy: read auth.json on every request. No token in logs."""
import http.client
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

AUTH = os.environ.get("XAI_AUTH", "/opt/agi/pi-agent/auth.json")
UP = os.environ.get("XAI_UP", "api.x.ai")
PORT = int(os.environ.get("XAI_PROXY_PORT", "18790"))


class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        return

    def do_GET(self):
        self._go()

    def do_POST(self):
        self._go()

    def do_PUT(self):
        self._go()

    def do_PATCH(self):
        self._go()

    def do_DELETE(self):
        self._go()

    def _go(self):
        n = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(n) if n else b""
        try:
            key = json.load(open(AUTH)).get("xai", {}).get("key") or ""
        except (OSError, json.JSONDecodeError, TypeError):
            key = ""
        hdrs = {k: v for k, v in self.headers.items()
                if k.lower() not in ("host", "authorization")}
        hdrs["Authorization"] = "Bearer " + key
        conn = http.client.HTTPSConnection(UP, timeout=600)
        try:
            conn.request(self.command, self.path, body=body or None, headers=hdrs)
            r = conn.getresponse()
            self.send_response(r.status)
            for k, v in r.getheaders():
                if k.lower() not in ("transfer-encoding", "connection"):
                    self.send_header(k, v)
            self.send_header("Connection", "close")
            self.close_connection = True
            self.end_headers()
            while True:
                chunk = r.read1(65536)
                if not chunk:
                    break
                self.wfile.write(chunk)
                self.wfile.flush()
        finally:
            conn.close()


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
~~~

### xai-proxy.service (170 B)
~~~ini
[Unit]
After=network-online.target
[Service]
ExecStart=/usr/bin/python3 /opt/agi/bin/xai-proxy
Restart=always
RestartSec=5
User=root
[Install]
WantedBy=multi-user.target
~~~


<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
owner 2026-10-05 via liaison: xai-proxy hang patched live (Connection: close). Land patched proxy + r.read1 into engine-root so projection owns it. agi-boot installs the binary and unit. Heading bytes = fence. Do not bounce posts.
<!-- THOUGHT:END -->
