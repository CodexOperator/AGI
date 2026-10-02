#!/bin/sh
# aa1m-install.sh STEP T (ROOT, ONE step per belam GO; reads only the PINNED trunk sha T, so a post-writable ref or replace object changes nothing)
# STEP = pieces | signers | units. REPO=<the box repo> is required. REPO must equal the cell box.repo at T. Scratch dry run: OPT= ETC= SYSD= (dirs) NOSYSTEMCTL=1 (no systemctl) AGI_STORES= BOXREPO=<the scratch repo, replaces the cell check>
set -e;S=$1;T=$2;R=${REPO:?REPO=<the box repo>};O=${OPT:-/opt/agi/bin};E=${ETC:-/etc/agi};D=${SYSD:-/etc/systemd/system};St=${AGI_STORES:-/var/lib/agi}
case $T in ""|*[!0-9a-f]*)exit 1;;esac;[ ${#T} = 40 ]||exit 1
export GIT_NO_REPLACE_OBJECTS=1 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory GIT_CONFIG_VALUE_0=$R
cell(){ git -C $R show $T:.agi/config.json|jq -r ".box.$1//\"\"";}
[ "$R" = "${BOXREPO:-$(cell repo)}" ]||{ echo "REPO is not the cell box.repo">&2;exit 1;}
piece(){ git -C $R ls-tree --full-tree --name-only $T .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$T:|"|git -C $R cat-file --batch --follow-symlinks|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
rows(){ git -C $R show $T:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -r --arg b $(cell alias) 'select(.box==$b and .engine.v==4)|.name';}
sd(){ [ -n "$NOSYSTEMCTL" ]||systemctl "$@";}
put(){ piece "$1">$2.new&&[ -s $2.new ]&&chmod $3 $2.new&&mv $2.new $2&&sha256sum $2;}
case $S in
pieces)install -d -m 755 $O $E;for n in box box-carry agi-signers sect;do put $n $O/$n 755;done
 { echo AGI_BOX=$(cell alias);echo AGI_HUB=$(cell hub);echo AGI_REPO=$(cell repo);echo AGI_TRUNK=$T;echo GIT_CONFIG_VALUE_0=$(cell repo);}>$E/carry.env.new&&chmod 644 $E/carry.env.new&&mv $E/carry.env.new $E/carry.env;cat $E/carry.env;;
signers)for p in $(rows);do sh $O/agi-signers $p;done;wc -l $St/allowed_signers;;
units)install -d -m 755 $D;for n in agi-carry@.path agi-carry@.service agi-carry-fetch.timer agi-carry-fetch.service;do put $n $D/$n 644;done;sd daemon-reload
 for p in $(rows);do sd enable --now agi-carry@$p.path;done;[ -n "$(. $E/carry.env;echo $AGI_HUB)" ]&&sd enable --now agi-carry-fetch.timer||echo "hub empty: fetch timer not enabled";;
*)exit 1;;esac
