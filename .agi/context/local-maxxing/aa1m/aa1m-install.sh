#!/bin/sh
# aa1m-install.sh STEP T (ROOT, ONE step per belam GO): run it as `f=$(mktemp) && git -C $REPO show T:<this path> >$f && sha256sum $f && REPO=$REPO sh $f STEP T` (a failed show cannot run an empty script), so the bytes are the ones AT T; reads only the pinned 40-hex trunk sha T
# STEP = pieces | signers | units. REPO must equal the cell box.repo at T. Cells are validated (charset, no leading '-') and written UNQUOTED (charset-gated), never sourced. Scratch dry run (refused when uid 0): AGI_DRY_OPT AGI_DRY_ETC AGI_DRY_SYSD AGI_DRY_BOXREPO AGI_DRY_NOSYSTEMCTL AGI_STORES
set -e;S=$1;T=$2;R=${REPO:?REPO=<the box repo>};O=${AGI_DRY_OPT:-/opt/agi/bin};E=${AGI_DRY_ETC:-/etc/agi};D=${AGI_DRY_SYSD:-/etc/systemd/system};St=${AGI_STORES:-/var/lib/agi}
[ "$(id -u)" = 0 ]&&[ -n "$AGI_DRY_OPT$AGI_DRY_ETC$AGI_DRY_SYSD$AGI_DRY_BOXREPO$AGI_DRY_NOSYSTEMCTL$AGI_STORES" ]&&{ echo "dry-run overrides are refused as root">&2;exit 1;}
case $T in ""|*[!0-9a-f]*)exit 1;;esac;[ ${#T} = 40 ]||exit 1
export GIT_NO_REPLACE_OBJECTS=1 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory GIT_CONFIG_VALUE_0=$R
cell(){ git -C $R show $T:.agi/config.json|jq -r ".box.$1//\"\"";}
BA=$(cell alias);BH=$(cell hub);BR=$(cell repo)
for v in "$BA" "$BH" "$BR";do case $v in *[!A-Za-z0-9._/:@-]*|-*)echo "a box cell holds a character outside [A-Za-z0-9._/:@-] or starts with -: refused">&2;exit 1;;esac;done
[ "$R" = "${AGI_DRY_BOXREPO:-$BR}" ]||{ echo "REPO is not the cell box.repo">&2;exit 1;}
piece(){ git -C $R ls-tree --full-tree --name-only $T .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$T:|"|git -C $R cat-file --batch --follow-symlinks|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
rows(){ git -C $R show $T:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -r --arg b "$BA" 'select(.box==$b and .engine.v==4)|.name';}
sd(){ [ -n "$AGI_DRY_NOSYSTEMCTL" ]||systemctl "$@";}
put(){ piece "$1">$2.new&&[ -s $2.new ]&&chmod $3 $2.new&&mv $2.new $2&&sha256sum $2;}
case $S in
pieces)install -d -m 755 $O $E;for n in box box-carry agi-signers sect;do put $n $O/$n 755;done
 printf 'AGI_BOX=%s\nAGI_HUB=%s\nAGI_REPO=%s\nAGI_TRUNK=%s\nGIT_CONFIG_VALUE_0=%s\n' "$BA" "$BH" "$BR" $T "$BR">$E/carry.env.new;chmod 644 $E/carry.env.new;mv $E/carry.env.new $E/carry.env;cat $E/carry.env;;
signers)for p in $(rows);do sh $O/agi-signers $p;done;wc -l $St/allowed_signers;;
units)install -d -m 755 $D;for n in agi-carry@.path agi-carry@.service agi-carry-fetch.timer agi-carry-fetch.service;do put $n $D/$n 644;done;sd daemon-reload
 for p in $(rows);do sd enable --now agi-carry@$p.path;done
 sd enable --now agi-carry-fetch.timer;;
*)exit 1;;esac
