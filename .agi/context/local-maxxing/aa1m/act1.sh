d=$1;R=${2:-runuser};A=${3:-alive};B=${4:-all-is-one}
r(){ u=$1;shift;if [ "$R" = runuser ];then runuser -u agi-$u -- env HOME=/var/lib/agi/$u "$@";else env "$@";fi;}
install -d -m 755 $d;for u in $A $B;do if [ "$R" = runuser ];then install -d -o agi-$u -g agi-$u -m 700 $d/$u;else mkdir -p $d/$u;fi;r $u git init -q --bare $d/$u/g.git;done
s=$(r $A sh -c "cd $d/$A/g.git && c=\$(echo hello-m1 | GIT_COMMITTER_EMAIL=$A@agi GIT_AUTHOR_EMAIL=$A@agi git commit-tree -S \$(git hash-object -w -t tree /dev/null)) && git update-ref refs/box/$A/$B \$c && echo \$c")
printf '%s\n' "$s" | r $A git -C $d/$A/g.git pack-objects --revs --stdout | r $B sh -c "git -C $d/$B/g.git unpack-objects -q && git -C $d/$B/g.git update-ref refs/box/$A/$B $s && git -C $d/$B/g.git log -1 --format='CARRIED %s %G?' refs/box/$A/$B"
r $B ls $d/$A >/dev/null 2>&1 && echo "BARRIER OPEN: $B reads $A" || echo "BARRIER HOLDS: $B cannot read $A"
