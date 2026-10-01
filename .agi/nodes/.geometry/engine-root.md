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
### agi-post@.service (1409 B)
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
RuntimeDirectory=agi-%i
RuntimeDirectoryPreserve=restart
ExecStartPre=awk -F"[= ]" "/some/{exit $$3>40}" /proc/pressure/memory
ExecStartPre=sh -c 'mkdir -p .ssh bin .claude hooks;git config --global safe.directory "*";[ -f .ssh/id_ed25519 ]||ssh-keygen -qN "" -ted25519 -f.ssh/id_ed25519;[ -d t ]||{ git -C $O branch posts/%i $AGI_TRUNK;git -C $O worktree add -fq $PWD/t posts/%i;touch .fresh;};for e in t/.agi/nodes/.geometry/engine.md t/.agi/nodes/.geometry/engine-[pw]*.md;do for x in $(grep -o "^### [^ ]*" $e|cut -c5-);do sed -n "/^### $x /,/^##/{/^~~~/,/^~~~/{//!p}}" $e>bin/$x;done;done;chmod +x bin/*;mv bin/gitconfig .gitconfig;mv bin/settings.json .claude;mkdir -p t/.agi/keys;cp .ssh/id_ed25519.pub t/.agi/keys/%i;mkfifo -m600 %t/agi-%i/i;[ -e o ]||install -m600 /dev/null o;cd t;signers>../.signers'
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


### agi-boot.service (491 B)
~~~ini
[Unit]
After=agi-ram-main.service
Requires=agi-ram-main.service
[Service]
Type=oneshot
RemainAfterExit=yes
TimeoutStartSec=infinity
WorkingDirectory=/data/work/agi
Environment=AGI_TRUNK=local-maxxing/season2/main GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory GIT_CONFIG_VALUE_0=*
ExecStart=sh -c 'echo $$AGI_TRUNK:.agi/nodes/.geometry/engine-root.md|git cat-file --batch --follow-symlinks|sed -n "/^### agi-boot /,/^##/{/^~~~/,/^~~~/{//!p}}"|sh -s'
[Install]
WantedBy=multi-user.target
~~~

### agi-boot (1179 B)
~~~sh
#!/bin/sh
R=${AGI_RAM:-/mnt/agi-ram} t=${AGI_TRUNK:-HEAD} o=${AGI_BOOT_OUT:-/run/systemd/system};w=$o/multi-user.target.wants
setfacl -m g:agi:x $R;setfacl -m g:agi:--- ${AGI_RAM_STATE:-$R/state}
c(){ git show $t:.agi/config.json|jq -r ".values.local_maxxing.$1";};L=$(c de_live_parents.ceiling_if.loadavg1_lt) P=$(c de_live_parents.ceiling_if.io_psi_some_avg60_lt) N=$(c agi_boot.poll_s) M=$(c agi_boot.wait_max_s)
echo $t:.agi/nodes/.geometry/engine.md|git cat-file --batch --follow-symlinks|sed -n '/^### agi-project /,/^### /{/^~~~/,/^~~~/{//!p}}'|sh -s $o $t||exit 3
systemctl daemon-reload
ok(){ read l _<${AGI_LOADAVG:-/proc/loadavg};i=$(sed -n 's/^some .*avg60=\([0-9.]*\).*/\1/p' ${AGI_PSI_IO:-/proc/pressure/io});[ -n "$i" ]&&awk -v l=$l -v i=$i -v L=$L -v P=$P 'BEGIN{exit !(l<L&&i<P)}';}
git show $t:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -r 'select(.boot==true)|.name'|while read p;do [ -L $w/agi-post@$p.service ]||continue;s=$(date +%s)
until ok;do [ $(($(date +%s)-s)) -ge $M ]&&{ echo "agi-boot: gate not open after ${M}s, skipping $p">&2;continue 2;};sleep $N;done
systemctl start agi-post@$p</dev/null||echo "agi-boot: start failed $p">&2;done
~~~

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
SPLIT (DG3 read sets): agi-post@.service moved here whole from engine-post; its ONE loop edit: for e in engine.md engine-[pw]*.md (was engine*.md), so a post reads engine + engine-post + engine-wrap only.
G9 (hypothesis:g716111-g9-boot-install-brings-the-boot-set-up): agi-boot.service + agi-boot, root once at boot: ACL pair, local-trunk projection (the agi-project section reused as is), daemon-reload, then one start at a time of the rows with boot:true behind the config load/io gate. Gate numbers = de_live_parents.ceiling_if; poll/bound = agi_boot cells.
<!-- THOUGHT:END -->
