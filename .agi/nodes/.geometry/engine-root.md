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


<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
SPLIT (DG3 read sets): agi-post@.service moved here whole from engine-post; its ONE loop edit: for e in engine.md engine-[pw]*.md (was engine*.md), so a post reads engine + engine-post + engine-wrap only.
<!-- THOUGHT:END -->
