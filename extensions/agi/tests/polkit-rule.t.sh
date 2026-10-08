#!/bin/sh
# polkit-rule.t.sh: goal:g1.41 B3 + B5 (DG1 22:12Z + 22:14Z addendum; hypothesis:g141-b-engine-grow-and-post-pieces-...): (B3) the polkit rule agi.rules lets a post start only its OWN agi-post@<name>.service (subject agi-<name>), not any agi-post@ unit (today any member of group agi may start ANY agi-post@ unit; the only `systemctl start agi-post@` in the engine is root's agi-boot); (B5) engine-post.md agi-wt drop names the archive ref by the caller's OWN seat, s=${AGI_SEAT:-$AGI_POST} (was ${AGI_POST:-$AGI_SEAT}): a kid whose env inherits AGI_POST=<parent> archives under the KID name and never overwrites the parent's refs/archive/worktrees entry.
# node (the REAL rule text, `sect agi.rules` from the .geometry/engine*.md of ROOT, default the working tree, evaluated in a vm with a FAKE polkit + fake action `a` and subject `s`) + sh + git on a SCRATCH repo for B5, no polkit, no systemd, no root, no network, 0 USD.
# Lanes: j-* the rule on a table of (subject user, unit, verb, action id, group) cases: the own unit = YES; another post's unit, a prefix of it, a user without the agi- prefix, regex-special user names (a dot, a plus, a group, .*, a dollar), a slash / capital / newline / template / non-service unit, a verb that is not start, another action id, a user outside group agi = NOT YES. w-* the real agi-wt piece: a kid env, a post env, one variable alone, none.
# Honest limits: the rule is judged as a function of (a.id, a.lookup(verb|unit), s.user, s.isInGroup) -- the fields polkit gives a rule; the real polkit daemon is not run; the rule reads the user as s.user (the lane's subject carries only user and isInGroup); B5 reads the archive ref name, not the tree contents.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE AGI_TRUNK AGI_SEAT AGI_POST
sect agi.rules >$T/rule.js;sect agi-wt >$T/agiwt;command -v node >/dev/null||{ echo "FAIL needs node";exit 99;};[ -s $T/rule.js ]&&[ -s $T/agiwt ]||{ echo "FAIL extract: agi.rules $(wc -c <$T/rule.js) agi-wt $(wc -c <$T/agiwt)";exit 99;}
# j: the rule table. name|user|unit|verb|action|in-group|want(YES or no); \n in a field is a newline, {at} is an at sign (restored at run time: the anonymize email class reads a literal unit name with an at sign as an address)
cat >$T/cases<<'XX'
own-unit|agi-alpha|agi-post{at}alpha.service|start|manage|1|YES
own-unit-with-hyphen|agi-ab-c|agi-post{at}ab-c.service|start|manage|1|YES
own-unit-with-digits|agi-a1|agi-post{at}a1.service|start|manage|1|YES
another-posts-unit|agi-alpha|agi-post{at}beta.service|start|manage|1|no
a-longer-unit-with-the-name-as-prefix|agi-alpha|agi-post{at}alpha-x.service|start|manage|1|no
a-longer-user-for-the-shorter-unit|agi-alpha-x|agi-post{at}alpha.service|start|manage|1|no
a-user-without-the-agi-prefix|alpha|agi-post{at}alpha.service|start|manage|1|no
a-prefix-lookalike-user|xagi-alpha|agi-post{at}alpha.service|start|manage|1|no
the-bare-agi-user|agi-|agi-post{at}.service|start|manage|1|no
a-dot-in-the-user-matches-any-char|agi-a.c|agi-post{at}abc.service|start|manage|1|no
a-plus-in-the-user|agi-a+|agi-post{at}aa.service|start|manage|1|no
a-group-in-the-user|agi-(a)|agi-post{at}a.service|start|manage|1|no
a-wildcard-user|agi-.*|agi-post{at}anything.service|start|manage|1|no
a-dollar-in-the-user|agi-a$|agi-post{at}a.service|start|manage|1|no
a-slash-in-the-unit|agi-alpha|agi-post{at}alpha/../x.service|start|manage|1|no
a-prefix-before-the-template|agi-alpha|xagi-post{at}alpha.service|start|manage|1|no
a-path-before-the-template|agi-alpha|/run/agi-post{at}alpha.service|start|manage|1|no
a-capital-in-the-unit|agi-alpha|agi-post{at}Alpha.service|start|manage|1|no
a-newline-after-the-unit|agi-alpha|agi-post{at}alpha.service\n|start|manage|1|no
a-newline-inside-the-unit|agi-alpha|agi-post{at}alpha\n.service|start|manage|1|no
a-newline-in-the-user|agi-alpha\n|agi-post{at}alpha.service|start|manage|1|no
the-template-unit|agi-alpha|agi-post{at}.service|start|manage|1|no
a-socket-unit|agi-alpha|agi-post{at}alpha.socket|start|manage|1|no
a-different-template|agi-alpha|agi-run{at}alpha.service|start|manage|1|no
verb-restart|agi-alpha|agi-post{at}alpha.service|restart|manage|1|no
verb-stop|agi-alpha|agi-post{at}alpha.service|stop|manage|1|no
verb-reload|agi-alpha|agi-post{at}alpha.service|reload|manage|1|no
another-action-id|agi-alpha|agi-post{at}alpha.service|start|reload-daemon|1|no
a-user-outside-group-agi|agi-alpha|agi-post{at}alpha.service|start|manage|0|no
no-user-at-all||agi-post{at}alpha.service|start|manage|1|no
XX
node -e '
const vm=require("vm"),fs=require("fs");
const src=fs.readFileSync(process.argv[1],"utf8");let rule=null;const polkit={addRule:f=>{rule=f},Result:{YES:"YES",NO:"NO",AUTH_ADMIN:"AUTH_ADMIN",NOT_HANDLED:null}};
vm.runInNewContext(src,{polkit});if(!rule){console.log("NORULE");process.exit(0)}
for(const l of fs.readFileSync(process.argv[2],"utf8").split("\n")){if(!l)continue;const [n,user,unit,verb,act,grp,want]=l.split("|").map(x=>x.replace(/\\n/g,"\n").replace(/\{at\}/g,"@"));
 const a={id:act==="manage"?"org.freedesktop.systemd1.manage-units":"org.freedesktop.systemd1."+act,lookup:k=>({verb,unit})[k]};
 const s={user,isInGroup:g=>grp==="1"&&g==="agi"};let r;try{r=rule(a,s)}catch(e){r="THROW:"+e.message}
 console.log(n+"|"+(r===polkit.Result.YES?"YES":"no")+"|"+want)}' $T/rule.js $T/cases >$T/jout 2>$T/jerr
nr=$(grep -c NORULE $T/jout)
ok "j-the-rule-loads the agi.rules piece registers ONE rule in the fake polkit: NORULE lines $nr (want 0), result rows $(grep -c '|' $T/jout) (want $(grep -c . $T/cases)), node stderr bytes $(wc -c <$T/jerr|tr -d ' ') (want 0)" '[ $nr = 0 ]&&[ "$(grep -c "|" $T/jout)" = "$(grep -c . $T/cases)" ]&&[ ! -s $T/jerr ]'
while IFS='|' read -r n got want;do [ -n "$n" ]||continue;ok "j-$n the rule says [$got] (want $want)" '[ "$got" = "$want" ]';done <$T/jout
# w: the real agi-wt piece, ONE node tree under $HOME/t, drop on a dirty pulled tree under several envs
chmod +x $T/agiwt;mkdir -p $T/hm;printf '[user]\n\tname=t\n\temail=t@t\n[commit]\n\tgpgsign=false\n[safe]\n\tdirectory=*\n' >$T/gitconfig;export GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null
MINT=0123456789abcdef0123456789abcdef
wt(){ rm -rf $T/hm/t $T/wtdir;mkdir -p $T/hm/t/.agi/nodes/idea $T/wtdir;printf -- '---\nid: idea:n\nmint_id: %s\ntype: idea\n---\nbody\n' $MINT >$T/hm/t/.agi/nodes/idea/n.md;$G init -q $T/hm/t;$G -C $T/hm/t add -A;$G -C $T/hm/t commit -qm base;SEED=$($G -C $T/hm/t rev-parse HEAD)
 $G -C $T/hm/t update-ref refs/archive/worktrees/parentpost@$MINT $SEED
 aw(){ (cd $T&&env -i PATH=/usr/bin:/bin HOME=$T/hm USER=t GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null AGI_WT=$T/wtdir AGI_WT_HOLD=101 "$@" sh $T/agiwt $WCMD idea:n >$T/w.out 2>$T/w.err);wrc=$?;}
 WCMD=pull;aw X=1;d=$(cat $T/w.out);echo "the wt edit" >>$d/.agi/nodes/idea/n.md;echo "the repo moved meanwhile" >>$T/hm/t/.agi/nodes/idea/n.md;WCMD=drop;}   # drop archives the wt copy when the repo's own copy moved since the pull
refs(){ $G -C $T/hm/t for-each-ref --format='%(refname:strip=3)' refs/archive/worktrees|tr '\n' ' ';}
wt;aw AGI_POST=parentpost AGI_SEAT=kidseat;r=$(refs);pp=$($G -C $T/hm/t rev-parse refs/archive/worktrees/parentpost@$MINT)
ok "w-a-kid-archives-under-its-own-seat a kid env (AGI_POST=parentpost inherited, AGI_SEAT=kidseat): rc $wrc (want 4 = moved), refs [${r% }] (want kidseat@$MINT and parentpost@$MINT), the parent's ref untouched: $([ $pp = $SEED ]&&echo yes||echo NO) (want yes)" '[ $wrc = 4 ]&&echo "$r"|grep -q "kidseat@$MINT"&&[ $pp = $SEED ]'
wt;aw AGI_POST=alpha AGI_SEAT=alpha;r=$(refs)
ok "w-a-post-env-archives-under-its-name both variables = alpha: rc $wrc (want 4), refs [${r% }] (want alpha@$MINT)" '[ $wrc = 4 ]&&echo "$r"|grep -q "alpha@$MINT"'
wt;aw AGI_POST=alpha;r=$(refs)
ok "w-only-AGI_POST-still-works AGI_POST=alpha alone: rc $wrc (want 4), refs [${r% }] (want alpha@$MINT)" '[ $wrc = 4 ]&&echo "$r"|grep -q "alpha@$MINT"'
wt;aw AGI_SEAT=kidseat;r=$(refs)
ok "w-only-AGI_SEAT-still-works AGI_SEAT=kidseat alone: rc $wrc (want 4), refs [${r% }] (want kidseat@$MINT)" '[ $wrc = 4 ]&&echo "$r"|grep -q "kidseat@$MINT"'
wt;aw X=1;r=$(refs)
ok "w-no-seat-archives-nothing neither variable: rc $wrc (want 5), a message on stderr: $(grep -c 'agi-wt' $T/w.err) (want >= 1), refs [${r% }] (want only parentpost@$MINT)" '[ $wrc = 5 ]&&[ $(grep -c "agi-wt" $T/w.err) -ge 1 ]&&[ "${r% }" = "parentpost@$MINT" ]'
# t (RB-1): tick.sh starts ONLY its own unit. The real tick.sh piece under a stub `sect` (project.sh lists TWO down units, p1 and p2; observe.sh lists none) and a stub `systemctl` that logs argv, run as USER=agi-p1 in a scratch $HOME/t repo: only the unit of agi-p1 is started; the drift file still lists BOTH (the drift is evidence, not an order). The at sign is built at run time (the anonymize email class).
sect tick.sh >$T/tick.sh;AT=$(printf '\100');U1=agi-post${AT}p1;U2=agi-post${AT}p2
tk(){ args=;for u in "$@";do args="$args agi-post${AT}$u";done;rm -rf $T/tk;mkdir -p $T/tk/bin $T/tk/hm/t;$G init -q $T/tk/hm/t;$G -C $T/tk/hm/t commit -q --allow-empty -m base;: >$T/tk/log
 cat >$T/tk/bin/sect<<XX
#!/bin/sh
case "\$1" in project.sh) printf '%s\\n' 'printf "unit %s\\n" $args';; *) echo true;; esac
XX
 printf '#!/bin/sh\necho "$*" >>%s\n' $T/tk/log >$T/tk/bin/systemctl;chmod +x $T/tk/bin/sect $T/tk/bin/systemctl
 (cd $T/tk/hm&&env -i PATH=$T/tk/bin:/usr/bin:/bin HOME=$T/tk/hm USER=agi-p1 GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null timeout 60 sh $T/tick.sh >$T/tk/out 2>&1);trc=$?
 D1F=$T/tk/hm/t/.agi/drift/agi-p1;nstart=$(grep -c '^start ' $T/tk/log);own=$(grep -c "^start $U1\(\.service\)\?\$" $T/tk/log);other=$(grep -c "$U2" $T/tk/log);dd=$(grep -c '^< unit ' $D1F 2>/dev/null);d1=$(grep -c "$U1" $D1F 2>/dev/null);d2=$(grep -c "$U2" $D1F 2>/dev/null);nall=$(wc -l <$T/tk/log|tr -d ' ');true;}
tk p1 p2
ok "t-the-tick-piece-is-extracted-and-the-stubs-ran the real tick.sh piece: $(wc -c <$T/tick.sh|tr -d ' ') bytes (want > 0), rc $trc (want 0), the drift file lists $dd '< unit' line(s) (want 2)" '[ -s $T/tick.sh ]&&[ $trc = 0 ]&&[ "$dd" = 2 ]'
ok "t-the-tick-starts-only-its-own-unit systemctl start calls: $nstart (want 1), for the own unit agi-post@p1: $own (want 1), mentioning the other post's unit: $other (want 0)" '[ "$nstart" = 1 ]&&[ "$own" = 1 ]&&[ "$other" = 0 ]'
ok "t-the-drift-file-still-lists-both-units the drift file names the own unit $d1 time(s) (want 1) and the other post's $d2 time(s) (want 1)" '[ "$d1" = 1 ]&&[ "$d2" = 1 ]'
# t2 (DG1 12:37Z): the own-unit filter is an EXACT match (p1 must not start p10) and starts nothing when only other posts are down
tk p1 p10 p2
ok "t-a-prefix-of-the-own-unit-is-not-the-own-unit units down: p1 p10 p2, USER=agi-p1: systemctl start calls $nstart (want 1), for exactly agi-post@p1: $own (want 1), total systemctl calls $nall (want 1), the drift file lists $dd unit line(s) (want 3)" '[ "$nstart" = 1 ]&&[ "$own" = 1 ]&&[ "$nall" = 1 ]&&[ "$dd" = 3 ]'
tk p10 p2
ok "t-with-only-other-posts-down-systemctl-is-not-called units down: p10 p2 (the own unit is up), USER=agi-p1: systemctl calls $nall (want 0: an empty list must not reach systemctl with no argument), the drift file still lists $dd unit line(s) (want 2)" '[ "$nall" = 0 ]&&[ "$dd" = 2 ]'
echo "polkit-rule: $f FAIL"
exit $f
