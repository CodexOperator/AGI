#!/bin/sh
# reader-census.t.sh: goal:g7.16.1.11.46.18 G1b-2 slice (b), falsifier 2 (rows 11 + 12, council 3/3 alive [decision] 10:07:47Z, option (3)): every reader that
# NAMES the trunk is classed (reader_census.py repo), and the installed readers are listed by home + path + sha256 (reader_census.py homes). sh + git + python3
# on SCRATCH repos (git archive of the committed tree) and a scratch homes root; nothing outside $T is written. Every mutant (m-*) must read RED.
T=$(mktemp -d);trap 'chmod -R u+rwx $T 2>/dev/null;rm -rf $T' 0;f=0;nrows=0;G=/usr/bin/git;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};REV=${REV:-HEAD}
ok(){ nrows=$((nrows+1));if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
printf '[user]\n\tname=t\n\temail=t@t\n[commit]\n\tgpgsign=false\n[safe]\n\tdirectory=*\n[gc]\n\tauto=0\n' >$T/gitconfig;export GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null PYTHONDONTWRITEBYTECODE=1
mut(){ python3 - "$1" "$2" "$3" <<'PY'
import sys
s=open(sys.argv[1]).read();a,b=sys.argv[2],sys.argv[3]
assert s.count(a)==1,("mutant anchor",a)
open(sys.argv[1],"w").write(s.replace(a,b))
PY
}
CB=extensions/agi/bin/reader_census.py;TB=extensions/agi/bin/reader_census.tsv
# the base: the COMMITTED tree of $REV in a scratch repo (git archive: an uncommitted file of the real tree is never read)
mkdir -p $T/base;$G -C $R0 archive $REV|tar -x -C $T/base;$G -C $T/base init -q;$G -C $T/base add -A;$G -C $T/base commit -qm base
# D1 (aio 10:5xZ, belam's disk finding 10:53Z): ONE extract per run; a row is a --shared clone of it (its checkout only), and the previous row's dir is
# removed before the next is built, so a run holds the base + one row, never one tree per row
cp_(){ [ -n "$P" ]&&[ "$P" != $T/base ]&&rm -rf $P;rm -rf $T/$1;$G clone -q --shared $T/base $T/$1;P=$T/$1;}
cen(){ (cd $P&&python3 $CB repo "$@");}
# plant <path> <line> [table row]: commit a file (and a table row) on the scratch tree; then apply mutants "$@" to the census and run it
plant(){ mkdir -p $(dirname $P/$1);printf '%s\n' "$2" >$P/$1;[ -n "$3" ]&&printf '%b\n' "$3" >>$P/$TB;$G -C $P add -A;$G -C $P commit -qm plant;}
# --- g0: the real committed tree: every hit classed, the floor printed
cp_ g0;cen >$T/g0.out 2>&1;g0=$?
ok "g0-the-real-tree-every-hit-classed rc $g0: $(grep 'files scanned' $T/g0.out|cut -c1-150)" '[ $g0 = 0 ]&&grep -q "every hit classed" $T/g0.out&&grep -qE "census: [1-9][0-9]* files scanned, [1-9][0-9]* with a hit" $T/g0.out'
# --- U1 = I16: a planted reader with no row -> unclassed BY PATH; mutant: a narrowed literal pattern misses it
u1(){ cp_ $1;shift;while [ $# -ge 2 ];do mut $P/$CB "$1" "$2";shift 2;done;plant extensions/agi/bin/planted_reader.py 'TRUNK = "refs/heads/posts/belam"';cen >$T/$OUT.out 2>&1;}
OUT=u1;u1 u1;u1=$?
ok "u1-a-planted-reader-with-no-row-is-red-by-path rc $u1: $(grep unclassed $T/u1.out|cut -c1-110)" '[ $u1 = 1 ]&&grep -q "unclassed extensions/agi/bin/planted_reader.py:1:" $T/u1.out'
OUT=u1m;u1 u1m 'LITERAL = r"posts/belam|refs/heads/posts/|season3/main|season/s3"' 'LITERAL = r"season3/main|season/s3"'
ok "m-a-narrowed-pattern-misses-the-planted-reader-reads-RED the literal pattern without posts/: no unclassed line for it (want one, so its absence = caught)" '! grep -q "planted_reader" $T/u1m.out'
# --- C1: a reader that BUILDS the alias ("season%d/main" % n) is a hit; mutant: the composed pattern dropped
c1(){ cp_ $1;shift;while [ $# -ge 2 ];do mut $P/$CB "$1" "$2";shift 2;done;plant extensions/agi/bin/composed_reader.py 'ref = "season%d/main" % n';cen >$T/$OUT.out 2>&1;}
OUT=c1;c1 c1;c1=$?
ok "c1-a-composed-trunk-name-is-a-hit rc $c1: $(grep unclassed $T/c1.out|cut -c1-110)" '[ $c1 = 1 ]&&grep -q "unclassed extensions/agi/bin/composed_reader.py:1:" $T/c1.out'
OUT=c1m;c1 c1m '    g = git("grep", "-n", "-I", "-E", f"{LITERAL}|{COMPOSED}", sha, "--", *SCOPE)' '    g = git("grep", "-n", "-I", "-E", f"{LITERAL}", sha, "--", *SCOPE)'
ok "m-the-literal-pattern-alone-reads-RED without the composed pattern the built name is no hit (want unclassed, so its absence = caught)" '! grep -q "composed_reader" $T/c1m.out'
# --- B2: 'fixture' holds only in a test file that builds its repo on mktemp / tmp_path; mutant: the check cut
b2(){ cp_ $1;shift;while [ $# -ge 2 ];do mut $P/$CB "$1" "$2";shift 2;done;plant extensions/agi/guard/live_reader.sh 'git rev-parse refs/heads/posts/belam' 'hit\textensions/agi/guard/live_reader.sh\tfixture\t*\tplanted';cen >$T/$OUT.out 2>&1;}
OUT=b2;b2 b2;b2=$?
ok "b2-a-live-reader-classed-fixture-is-red-by-path rc $b2: $(grep bad-fixture $T/b2.out|cut -c1-110)" '[ $b2 = 1 ]&&grep -q "bad-fixture extensions/agi/guard/live_reader.sh" $T/b2.out'
OUT=b2m;b2 b2m '        if not path.startswith("extensions/agi/tests/") or not re.search(rb"mktemp|tmp_path", body):' '        if False:'
ok "m-the-fixture-rule-cut-reads-RED the live reader passes as a fixture: rc 0 (want bad-fixture, so its absence = caught)" '! grep -q bad-fixture $T/b2m.out&&grep -q "every hit classed" $T/b2m.out'
# --- W1 (aio): a 'family' hit may name no trunk; mutant: the guard cut
w1(){ cp_ $1;shift;while [ $# -ge 2 ];do mut $P/$CB "$1" "$2";shift 2;done;plant extensions/agi/bin/family_reader.py 'ref = f"season{n}/main"' 'hit\textensions/agi/bin/family_reader.py\tfamily\t*\tplanted';cen >$T/$OUT.out 2>&1;}
OUT=w1;w1 w1;w1=$?
ok "w1-a-trunk-reader-classed-family-is-red-by-path rc $w1: $(grep bad-family $T/w1.out|cut -c1-110)" '[ $w1 = 1 ]&&grep -q "bad-family extensions/agi/bin/family_reader.py:1" $T/w1.out'
OUT=w1m;w1 w1m '        if row[1] == "family" and (re.search(LITERAL, text) or re.search(TRUNK_COMPOSED, text)):' '        if False:'
ok "m-the-family-guard-cut-reads-RED the trunk reader passes as another family (want bad-family, so its absence = caught)" '! grep -q bad-family $T/w1m.out&&grep -q "every hit classed" $T/w1m.out'
cp_ w1f;plant extensions/agi/bin/family_ok.py 'ref = f"season{n}/posts/{name}"' 'hit\textensions/agi/bin/family_ok.py\tfamily\t*\tplanted';cen >$T/w1f.out 2>&1;w1f=$?
ok "w1f-a-real-other-family-passes season{n}/posts/{name} classed family: rc $w1f, no bad-family" '[ $w1f = 0 ]&&! grep -q bad-family $T/w1f.out'
# --- the floor: a commit whose table sits OUTSIDE the scope and holds no file under extensions / skills / .geometry reads 'unread' rc 1, never
# 'every hit classed'; mutant: the floor cut
fl(){ cp_ $1;shift;while [ $# -ge 2 ];do mut $P/$CB "$1" "$2";shift 2;done;e=$($G -C $P commit-tree $(printf '100644 blob %s\ttbl.tsv\n' $(printf '# empty\n'|$G -C $P hash-object -w --stdin)|$G -C $P mktree) -m no-scope)
 (cd $P&&python3 $CB repo --rev $e --table tbl.tsv) >$T/$OUT.out 2>&1;}
OUT=fl;fl fl;fl=$?
ok "fl-zero-files-scanned-is-unread a commit with no extensions/skills/.geometry: rc $fl, $(sed -n 2p $T/fl.out|cut -c1-110)" '[ $fl = 1 ]&&grep -q "census: unread (0 files scanned" $T/fl.out&&! grep -q "every hit classed" $T/fl.out'
OUT=flm;fl flm '    if not scanned:
        print(f"census: unread' '    if False:
        print(f"census: unread'
ok "m-the-floor-cut-reads-RED with the floor cut the empty commit reads 'every hit classed' (want unread, so the pass = caught)" '! grep -q "unread" $T/flm.out&&grep -q "every hit classed" $T/flm.out'
# --- a stale row (classes no hit) is red; an UNCOMMITTED reader is never read (the census reads a commit)
cp_ st;printf 'hit\textensions/agi/bin/nothing_here.py\tprose\t*\tstale\n' >>$P/$TB;$G -C $P add -A;$G -C $P commit -qm stale;cen >$T/st.out 2>&1;st=$?
ok "st-a-row-that-classes-no-hit-is-stale rc $st: $(grep stale $T/st.out|cut -c1-110)" '[ $st = 1 ]&&grep -q "stale $TB:[0-9]* extensions/agi/bin/nothing_here.py" $T/st.out'
cp_ uc;printf 'TRUNK = "refs/heads/posts/belam"\n' >$P/extensions/agi/bin/uncommitted_reader.py;cen >$T/uc.out 2>&1;uc=$?
ok "uc-an-uncommitted-reader-is-not-read rc $uc (the census reads the commit, never the working tree): no line names uncommitted_reader" '[ $uc = 0 ]&&! grep -q uncommitted_reader $T/uc.out'
# --- A15 + B1: the homes come from a LISTING (count printed); a home not listable = unread unless its table row says not in the boot set; a piece whose
# bytes cannot be read = unread <home> <path>; mutant: a hard-coded home list missing one home -> its pieces absent with rc 0
mkh(){ H=$T/homes.$1;rm -rf $H;for h in ha hb hc;do mkdir -p $H/$h/bin;printf 'b=refs/heads/posts/$P\n' >$H/$h/bin/agi-at;printf 'echo hi\n' >$H/$h/bin/other;done
 mkdir -p $H/retired $H/hidden;chmod 000 $H/retired;printf 'MAIN hook refs/heads/posts/belam\n' >$H/mainhook
 grep -v '^extra' $P/$TB >$P/$TB.n;mv $P/$TB.n $P/$TB;[ -n "$EX" ]&&printf '%b\n' "$EX" >>$P/$TB;$G -C $P add -A;$G -C $P commit -qm homes-table;}
hm(){ (cd $P&&python3 $CB homes --root $H --main-hooks $H/mainhook) >$T/$OUT.out 2>&1;}
EX=;cp_ h0;mkh h0;OUT=h0;hm;h0=$?
ok "h0-every-listed-home-and-MAIN rc $h0: $(grep 'homes:' $T/h0.out|tr '\n' '|'|cut -c1-160)" '[ $h0 = 0 ]&&grep -q "homes: 3 homes with bin/" $T/h0.out&&[ $(grep -c " $H/h[abc]/bin/agi-at [0-9a-f]\{64\} posts/<P>" $T/h0.out) = 3 ]&&grep -q "MAIN $H/mainhook" $T/h0.out&&grep -q "retired: not in the boot set" $T/h0.out&&! grep -q "/other " $T/h0.out'
cp_ h1;mkh h1;chmod 000 $H/hidden;OUT=h1;hm;h1=$?;chmod 755 $H/hidden
ok "h1-a-home-not-listable-is-unread rc $h1: $(grep 'unread hidden' $T/h1.out|cut -c1-80)" '[ $h1 = 1 ]&&grep -q "unread hidden (the home cannot be listed)" $T/h1.out'
cp_ h2;mkh h2;chmod 000 $H/hb/bin/agi-at;OUT=h2;hm;h2=$?;chmod 644 $H/hb/bin/agi-at
ok "h2-a-piece-that-cannot-be-read-is-unread rc $h2, never a pass or a skip: $(grep 'unread hb' $T/h2.out|cut -c1-90)" '[ $h2 = 1 ]&&grep -q "unread hb $H/hb/bin/agi-at" $T/h2.out'
cp_ h3;mkh h3;mut $P/$CB '        entries = sorted(os.listdir(root))' '        entries = ["ha", "hb", "retired"]';OUT=h3;hm
ok "m-a-hard-coded-home-list-reads-RED the list misses hc: its agi-at is absent and nothing is unread (want hc listed, so its absence = caught)" '! grep -q "$H/hc/bin/agi-at" $T/h3.out&&grep -q "homes: 2 homes" $T/h3.out'
cp_ h4;mkh h4;chmod 000 $H/hb/bin/agi-at;mut $P/$CB '        if names is None or digest is None:
            bad.append(f"unread {h} {p} (its bytes cannot be read)")
            continue' '        if names is None or digest is None:
            continue';OUT=h4;hm;h4=$?;chmod 644 $H/hb/bin/agi-at
ok "m-an-unread-piece-skipped-reads-RED the failed read is skipped: rc $h4, no unread line (want unread, so its absence = caught)" '[ $h4 = 0 ]&&! grep -q "^  unread" $T/h4.out'
# U-b1 (sp 10:29:01Z): the listing finds 0 homes (a wrong or empty root) = 'unread homes' rc 1, never a clean 0; mutant: that check cut -> a clean 0
ub(){ cp_ $1;shift;while [ $# -ge 2 ];do mut $P/$CB "$1" "$2";shift 2;done;mkdir -p $T/emptyroot.$OUT;grep -v '^extra\|^home' $P/$TB >$P/$TB.n;mv $P/$TB.n $P/$TB;$G -C $P add -A;$G -C $P commit -qm no-extras;printf 'refs/heads/posts/belam\n' >$T/emptyroot.$OUT.hook;(cd $P&&python3 $CB homes --root $T/emptyroot.$OUT --main-hooks $T/emptyroot.$OUT.hook) >$T/$OUT.out 2>&1;}
OUT=ub1;ub ub1;ub1=$?
ok "ub1-zero-homes-is-unread an empty homes root: rc $ub1, $(grep 'unread homes' $T/ub1.out|head -1|cut -c1-80)" '[ $ub1 = 1 ]&&grep -q "unread homes (0 homes with bin/" $T/ub1.out'
OUT=ub1m;ub ub1m '    if not homes:                                        # U-b1' '    if False:                                        # U-b1' '    if not hashed:
        bad.append' '    if False:
        bad.append';ub1m=$?
ok "m-an-empty-listing-reads-clean-reads-RED both read-nothing checks cut: the empty root reads rc $ub1m with no unread line (want unread, so the clean 0 = caught)" '[ $ub1m = 0 ]&&! grep -q "^  unread" $T/ub1m.out'
# an extra glob (SM's gate scripts) under a directory this uid cannot list = unread, naming that its owner reads the row
cp_ h5;H=$T/homes.h5;EX="extra\t$H/locked/*.sh\tposts\tplanted";mkh h5;mkdir -p $H/locked;printf 'refs/heads/posts/belam\n' >$H/locked/g.sh;chmod 000 $H/locked;OUT=h5;hm;h5=$?;chmod 755 $H/locked;EX=
ok "h5-an-extra-under-an-unlistable-dir-is-unread rc $h5: $(grep 'unread extra' $T/h5.out|cut -c1-110)" '[ $h5 = 1 ]&&grep -q "unread extra $H/locked/\*.sh ($H/locked cannot be listed by this uid" $T/h5.out'
# A-N2 (alive 11:05:52Z): MAIN's own reference-transaction is read by DEFAULT (the git common dir of the repo the census runs in); unreadable = 'unread MAIN';
# mutant: the default dropped -> MAIN absent with no unread line
an2(){ cp_ $1;shift;while [ $# -ge 2 ];do mut $P/$CB "$1" "$2";shift 2;done;EX=;mkh $OUT;[ "$NOHOOK" ]||printf 'case $r in refs/heads/posts/belam);;esac\n' >$P/.git/hooks/reference-transaction
 (cd $P&&python3 $CB homes --root $H) >$T/$OUT.out 2>&1;}
OUT=an2;NOHOOK=;an2 an2;an2=$?
ok "an2-MAINs-hook-is-read-by-default rc $an2: $(grep ' MAIN ' $T/an2.out|cut -c1-110)" '[ $an2 = 0 ]&&grep -q "MAIN $P/.git/hooks/reference-transaction [0-9a-f]\{64\} posts/<P>" $T/an2.out'
OUT=an2b;NOHOOK=1;an2 an2b;an2b=$?;NOHOOK=
ok "an2b-an-unreadable-MAIN-hook-is-unread rc $an2b: $(grep 'unread MAIN' $T/an2b.out|cut -c1-110)" '[ $an2b = 1 ]&&grep -q "unread MAIN $P/.git/hooks/reference-transaction" $T/an2b.out'
OUT=an2m;an2 an2m '    if main_hooks is None:                               # A-N2' '    if False:                               # A-N2' '    if not os.path.isfile(main_hooks) or not os.access(main_hooks, os.R_OK):' '    if not main_hooks:
        pass
    elif not os.path.isfile(main_hooks) or not os.access(main_hooks, os.R_OK):'
ok "m-MAIN-not-read-by-default-reads-RED the default dropped: no MAIN line and no unread MAIN (want MAIN listed, so its absence = caught)" '! grep -q "^  MAIN " $T/an2m.out&&! grep -q "unread MAIN" $T/an2m.out&&grep -q "+ MAIN (none) +" $T/an2m.out'
# A-N3 (alive): the not-in-the-boot-set escape is guarded: a row whose entry is listable reads stale; a row may not name a seat of config:posts; mutant: the seat check cut
an3(){ cp_ $1;shift;while [ $# -ge 2 ];do mut $P/$CB "$1" "$2";shift 2;done;mkh $OUT;mkdir -p $H/alive;chmod 000 $H/alive;hm;}
EX="home\talive\tnot-in-the-boot-set\tplanted";OUT=an3;an3 an3;an3=$?;chmod 755 $H/alive
ok "an3-a-seat-cannot-be-excused rc $an3: $(grep bad-home $T/an3.out|cut -c1-110)" '[ $an3 = 1 ]&&grep -q "bad-home $TB:[0-9]* alive (a seat of config:posts" $T/an3.out'
OUT=an3m;an3 an3m '        if h in seats:' '        if False:' '            if e in skip and e not in seats:' '            if e in skip:';chmod 755 $H/alive;EX=
ok "m-the-seat-check-cut-reads-RED the seat alive passes as not in the boot set (want bad-home, so its absence = caught)" '! grep -q bad-home $T/an3m.out&&grep -q "alive: not in the boot set" $T/an3m.out'
EX="home\tha\tnot-in-the-boot-set\tplanted";OUT=an3s;cp_ an3s;mkh an3s;hm;an3s=$?;EX=
ok "an3s-a-row-for-a-listable-home-is-stale rc $an3s: $(grep 'stale.*home ha' $T/an3s.out|cut -c1-100)" '[ $an3s = 1 ]&&grep -q "stale $TB:[0-9]* home ha (the entry is absent or listable" $T/an3s.out'
# A-N3b (alive): 0 seats parsed from config:posts = 'unread config:posts' rc 1; mutant: the regex key changed (and the check cut) -> a seat row excused, rc 0
OUT=an3b;an3 an3b '"name": "([^"]+)"' '"nom": "([^"]+)"';an3b=$?;chmod 755 $H/alive
ok "an3b-zero-seats-parsed-is-unread rc $an3b: $(grep 'unread config:posts' $T/an3b.out|cut -c1-100)" '[ $an3b = 1 ]&&grep -q "unread config:posts (0 seats parsed" $T/an3b.out'
EX="home\talive\tnot-in-the-boot-set\tplanted";OUT=an3bm;an3 an3bm '"name": "([^"]+)"' '"nom": "([^"]+)"' '    if not seats:  ' '    if False:  ';an3bm=$?;chmod 755 $H/alive;EX=
ok "m-the-seat-parse-broken-reads-RED with the key changed and the 0-seat check cut the seat alive passes as not in the boot set (want unread config:posts, so its absence = caught)" '! grep -q "unread config:posts" $T/an3bm.out&&grep -q "alive: not in the boot set" $T/an3bm.out'
# A-N4 (alive): no catch-all prose row on a code file outside tests/: a live read planted in board_job.py is unclassed by path; a '*' prose row there is refused;
# mutant: that guard cut, with the '*' row -> the planted read passes as prose
OUT=an4;cp_ an4;printf '_x = "git rev-parse refs/heads/posts/belam"\n' >>$P/extensions/agi/bin/board_job.py;$G -C $P add -A;$G -C $P commit -qm an4;cen >$T/an4.out 2>&1;an4=$?
ok "an4-a-live-read-added-to-a-code-file-is-unclassed rc $an4: $(grep 'unclassed extensions/agi/bin/board_job.py' $T/an4.out|cut -c1-100)" '[ $an4 = 1 ]&&grep -q "unclassed extensions/agi/bin/board_job.py:[0-9]*: _x = " $T/an4.out'
an4b(){ cp_ $1;shift;while [ $# -ge 2 ];do mut $P/$CB "$1" "$2";shift 2;done;printf '_x = "git rev-parse refs/heads/posts/belam"\n' >>$P/extensions/agi/bin/board_job.py
 printf 'hit\textensions/agi/bin/board_job.py\tprose\t*\tplanted catch-all\n' >>$P/$TB;$G -C $P add -A;$G -C $P commit -qm an4b;cen >$T/$OUT.out 2>&1;}
OUT=an4b;an4b an4b;an4b=$?
ok "an4b-a-catch-all-prose-row-on-code-is-refused rc $an4b: $(grep bad-prose-row $T/an4b.out|cut -c1-100)" '[ $an4b = 1 ]&&grep -q "bad-prose-row $TB:[0-9]* extensions/agi/bin/board_job.py" $T/an4b.out'
OUT=an4m;an4b an4m '            if x[1] == "prose" and x[2] == "*" and not x[0].startswith("extensions/agi/tests/") and not x[0].endswith(".md")' '            if False'
ok "m-the-catch-all-guard-cut-reads-RED the planted live read passes as prose (want bad-prose-row, so 'every hit classed' = caught)" '! grep -q bad-prose-row $T/an4m.out&&grep -q "every hit classed" $T/an4m.out'
# U-b3 + U-b3b + A-N5 (sp 11:08:39Z, aio 11:1xZ, alive [correction] 11:11:21Z): a name DERIVED through branches.py is a MODULE hit in a non-test file; a planted
# derive_names(..)['town_season_main'] read, a NEW branches.py builder called from send.py, and the aliased-import row as '*' each read RED; mutant: MODULE cut
ub3(){ cp_ $1;shift;while [ $# -ge 2 ];do mut $P/$CB "$1" "$2";shift 2;done;printf '_t = branches.derive_names("core", 3)["town_season_main"]\n' >>$P/extensions/agi/bin/board_job.py;$G -C $P add -A;$G -C $P commit -qm ub3;cen >$T/$OUT.out 2>&1;}
OUT=ub3;ub3 ub3;ub3=$?
ok "ub3-a-derived-trunk-read-is-unclassed rc $ub3: $(grep 'unclassed module extensions/agi/bin/board_job.py' $T/ub3.out|cut -c1-110)" '[ $ub3 = 1 ]&&grep -q "unclassed module extensions/agi/bin/board_job.py:[0-9]*: _t = branches.derive_names" $T/ub3.out'
OUT=ub3m;ub3 ub3m 'MODULE, sha, "--", *SCOPE)' '"^NEVER-MATCHES$", sha, "--", *SCOPE)'
ok "m-the-MODULE-grep-cut-reads-RED the planted derived read is never named (its module rows read stale; want unclassed module board_job.py, so its absence = caught)" '! grep -q "board_job.py:[0-9]*: _t = " $T/ub3m.out&&grep -q "census: [0-9]* files scanned" $T/ub3m.out'
OUT=ub3b;cp_ ub3b;printf '\n\ndef trunk_k(town, k):\n    return f"{town}/season{k}/main"\n' >>$P/extensions/agi/bin/branches.py;printf '_K = branches.trunk_k("core", 3)\n' >>$P/extensions/agi/bin/send.py;$G -C $P add -A;$G -C $P commit -qm ub3b;cen >$T/ub3b.out 2>&1;ub3b=$?
ok "ub3b-a-NEW-branches-builder-called-from-send-is-unclassed rc $ub3b: $(grep 'unclassed module extensions/agi/bin/send.py' $T/ub3b.out|cut -c1-110)" '[ $ub3b = 1 ]&&grep -q "unclassed module extensions/agi/bin/send.py:[0-9]*: _K = branches.trunk_k" $T/ub3b.out'
OUT=an5;cp_ an5;python3 -c "import sys;p=sys.argv[1];s=open(p).read();a='alias\timport derive_names as\t';assert s.count(a)==1;open(p,'w').write(s.replace(a,'alias\t*\t'))" $P/$TB;$G -C $P add -A;$G -C $P commit -qm an5;cen >$T/an5.out 2>&1;an5=$?
ok "an5-the-aliased-import-row-as-star-reads-RED rc $an5: $(grep 'unclassed module extensions/agi/bin/towns.py' $T/an5.out|cut -c1-110)" '[ $an5 = 1 ]&&grep -q "unclassed module extensions/agi/bin/towns.py:[0-9]*: from branches import derive_names as _derive" $T/an5.out'
OUT=ub3t;cp_ ub3t;printf '_t = branches.derive_names("core", 3)["town_season_main"]\n' >$P/extensions/agi/tests/test_planted_module.py;$G -C $P add -A;$G -C $P commit -qm ub3t;cen >$T/ub3t.out 2>&1;ub3t=$?
ok "ub3t-a-test-file-call-is-not-a-module-hit rc $ub3t (MODULE reads non-test files only): no line names test_planted_module" '[ $ub3t = 0 ]&&! grep -q test_planted_module $T/ub3t.out'
# I-M1 (all-is-one 12:1xZ): a module hit's class is CHECKED against FN_CLASS: a live branches.season_main( call under a 'prose' row = bad-module-class; a NEW public
# def of branches.py that FN_CLASS does not name = unmapped, even with a row for its call; mutants: each check cut -> 'every hit classed'
im1(){ cp_ $1;shift;while [ $# -ge 2 ];do mut $P/$CB "$1" "$2";shift 2;done;printf 't = branches.season_main(3)\n' >>$P/extensions/agi/bin/board_job.py;printf 'hit\textensions/agi/bin/board_job.py\tprose\tbranches.season_main(\tplanted\n' >>$P/$TB;$G -C $P add -A;$G -C $P commit -qm im1;cen >$T/$OUT.out 2>&1;}
OUT=im1;im1 im1;im1=$?
ok "im1-a-live-call-under-a-prose-row-is-bad-module-class rc $im1: $(grep bad-module-class $T/im1.out|cut -c1-110)" '[ $im1 = 1 ]&&grep -q "bad-module-class extensions/agi/bin/board_job.py:[0-9]* (row $TB:[0-9]* says prose, branches.py returns alias)" $T/im1.out'
OUT=im1m;im1 im1m '            if want and row[1] not in want' '            if False'
ok "m-the-module-class-check-cut-reads-RED the live call passes as prose (want bad-module-class, so 'every hit classed' = caught)" '! grep -q bad-module-class $T/im1m.out&&grep -q "every hit classed" $T/im1m.out'
im2(){ cp_ $1;shift;while [ $# -ge 2 ];do mut $P/$CB "$1" "$2";shift 2;done;printf '\n\ndef trunk_k(town, k):\n    return town + "/main"\n' >>$P/extensions/agi/bin/branches.py;printf '_K = branches.trunk_k("core", 3)\n' >>$P/extensions/agi/bin/send.py;printf 'hit\textensions/agi/bin/send.py\tgrammar\tbranches.trunk_k(\tplanted\n' >>$P/$TB;$G -C $P add -A;$G -C $P commit -qm im2;cen >$T/$OUT.out 2>&1;}
OUT=im2;im2 im2;im2=$?
ok "im2-a-new-branches-def-with-a-row-is-unmapped rc $im2: $(grep 'unmapped branches' $T/im2.out|cut -c1-110)" '[ $im2 = 1 ]&&grep -q "unmapped branches.trunk_k (a public def" $T/im2.out'
OUT=im2m;im2 im2m '    bad += [f"unmapped branches.{fn}' '    bad += [] and [f"unmapped branches.{fn}'
ok "m-the-unmapped-check-cut-reads-RED the new builder passes by its row (want unmapped, so 'every hit classed' = caught)" '! grep -q "unmapped branches" $T/im2m.out&&grep -q "every hit classed" $T/im2m.out'
# A-N6 = I-M1r (alive [view] 12:19:49Z, sp [word] 12:19:43Z): a call the line BUILDS into a remote name owes 'remote'; the strip form keeps FN_CLASS.
# a6: heal.py:1238's row re-classed alias -> bad-module-class; mutants (sp): the prefix rule cut -> cli.py:669; 'origin/ anywhere' -> send.py's strip-form line
OUT=a6;cp_ a6;python3 -c "import sys;p=sys.argv[1];s=open(p).read();a='heal.py\tremote\t';assert s.count(a)==1;open(p,'w').write(s.replace(a,'heal.py\talias\t'))" $P/$TB;$G -C $P add -A;$G -C $P commit -qm a6;cen >$T/a6.out 2>&1;a6=$?
ok "a6-a-built-remote-name-classed-alias-is-bad-module-class rc $a6: $(grep 'bad-module-class extensions/agi/bin/heal.py' $T/a6.out|cut -c1-110)" '[ $a6 = 1 ]&&grep -q "bad-module-class extensions/agi/bin/heal.py:[0-9]* (row $TB:[0-9]* says alias, branches.py returns remote)" $T/a6.out'
a6m(){ cp_ $1;shift;while [ $# -ge 2 ];do mut $P/$CB "$1" "$2";shift 2;done;cen >$T/$OUT.out 2>&1;}
OUT=a6m1;a6m a6m1 '"remote" if re.search(' '"remote" if False and re.search('
ok "m-the-remote-prefix-rule-cut-reads-RED cli.py's built origin/ line owes alias, its remote row is bad-module-class (want every hit classed, so this red = caught)" 'grep -q "bad-module-class extensions/agi/bin/cli.py:[0-9]* (row $TB:[0-9]* says remote, branches.py returns alias)" $T/a6m1.out'
OUT=a6m2;a6m a6m2 ', before) else FN_CLASS[fn])' ', before) or "origin/" in text else FN_CLASS[fn])'
ok "m-origin-anywhere-reads-RED the strip form in send.py owes remote, its alias row is bad-module-class (want alias kept, so this red = caught)" 'grep -q "bad-module-class extensions/agi/bin/send.py:[0-9]* (row $TB:[0-9]* says alias, branches.py returns remote)" $T/a6m2.out'
# CRUMBS (alive [decision] 13:53:50Z: A1 A2, sp [approve] 13:50:41Z: U1 U2), each a plant + its mutant
# pl <file line> <row match> <row class>: append a line to board_job.py and a row for it, then apply mutants "$@"; run the census
pl(){ cp_ $OUT;printf '%s\n' "$1" >>$P/extensions/agi/bin/board_job.py;printf 'hit\textensions/agi/bin/board_job.py\t%s\t%s\tplanted\n' "$3" "$2" >>$P/$TB;shift 3;while [ $# -ge 2 ];do mut $P/$CB "$1" "$2";shift 2;done;$G -C $P add -A;$G -C $P commit -qm pl;cen >$T/$OUT.out 2>&1;}
# A1: a docstring opener is a prose start
D1='"""docs: branches.season_main(3) is the season main"""'
OUT=a1;pl "$D1" 'docs: branches.season_main(' prose;a1=$?
ok "a1-a-docstring-line-under-a-prose-row-is-classed rc $a1: no bad-module-class for board_job.py" '[ $a1 = 0 ]&&! grep -q "bad-module-class extensions/agi/bin/board_job.py" $T/a1.out&&grep -q "every hit classed" $T/a1.out'
OUT=a1m;pl "$D1" 'docs: branches.season_main(' prose '") or stripped[:3] in (' '") or False and stripped[:3] in ('
ok "m-the-docstring-opener-cut-reads-RED the docstring line owes alias (want classed, so bad-module-class = caught)" 'grep -q "bad-module-class extensions/agi/bin/board_job.py:[0-9]* (row $TB:[0-9]* says prose, branches.py returns alias)" $T/a1m.out'
# A2: the single-quoted and the refs/remotes/origin/ builds owe remote
S2="_r = 'origin/' + branches.season_main(3)";R2="_q = \"refs/remotes/origin/\" + branches.season_main(3)"
OUT=a2;pl "$S2" "'origin/' + branches.season_main(" remote;a2=$?
ok "a2-a-single-quoted-origin-build-owes-remote rc $a2: the remote row holds" '[ $a2 = 0 ]&&grep -q "every hit classed" $T/a2.out'
OUT=a2r;pl "$R2" '"refs/remotes/origin/" + branches.season_main(' remote;a2r=$?
ok "a2r-a-refs-remotes-origin-build-owes-remote rc $a2r: the remote row holds" '[ $a2r = 0 ]&&grep -q "every hit classed" $T/a2r.out'
OUT=a2m;pl "$S2" "'origin/' + branches.season_main(" remote 'REMOTE_BUILD, before)' 'REMOTE_BUILD.split("|")[0].replace("(?:refs/remotes/)?", ""), before)'
ok "m-the-remote-widening-cut-reads-RED the single-quoted build owes alias again, its remote row is bad-module-class (want remote, so this red = caught)" 'grep -q "bad-module-class extensions/agi/bin/board_job.py:[0-9]* (row $TB:[0-9]* says remote, branches.py returns alias)" $T/a2m.out'
# U1: 'from <pkg> import branches' owes grammar
OUT=u1g;pl 'from agi import branches' 'from agi import branches' remote;u1g=$?
ok "u1g-a-package-import-under-a-remote-row-is-bad-module-class rc $u1g: $(grep 'bad-module-class extensions/agi/bin/board_job.py' $T/u1g.out|cut -c1-100)" '[ $u1g = 1 ]&&grep -q "bad-module-class extensions/agi/bin/board_job.py:[0-9]* (row $TB:[0-9]* says remote, branches.py returns grammar)" $T/u1g.out'
OUT=u1gm;pl 'from agi import branches' 'from agi import branches' remote '    elif re.match(r"\s*from\s+\S+\s+import\s+(.*,\s*)?branches\b", text):' '    elif False:'
ok "m-that-form-returns-empty-reads-RED the package import passes as remote (sp p2: want bad-module-class, so 'every hit classed' = caught)" '! grep -q bad-module-class $T/u1gm.out&&grep -q "every hit classed" $T/u1gm.out'
# U2: branches.py gone at the rev with module hits to class = unread branches.py, rc 1
u2(){ cp_ $1;shift;while [ $# -ge 2 ];do mut $P/$CB "$1" "$2";shift 2;done;$G -C $P rm -q extensions/agi/bin/branches.py;$G -C $P commit -qm u2;cen >$T/$OUT.out 2>&1;}
OUT=u2;u2 u2;u2=$?
ok "u2-branches-py-gone-is-unread rc $u2: $(grep 'unread branches.py' $T/u2.out|cut -c1-100)" '[ $u2 = 1 ]&&grep -q "unread branches.py (0 public defs at [0-9a-f]*, [1-9][0-9]* module hit(s) to class)" $T/u2.out'
OUT=u2m;u2 u2m '    if module and not defs:' '    if False:'
ok "m-the-unread-branches-check-cut-reads-RED no unread line names branches.py (want unread, so its absence = caught)" '! grep -q "unread branches.py" $T/u2m.out&&grep -q "census: [0-9]* files scanned" $T/u2m.out'
echo "reader-census: $nrows rows";echo "reader-census: $f FAIL";[ $f = 0 ]
