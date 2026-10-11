S=$1;K=$S/k;G=.agi/nodes/.geometry;rm -rf $S/r;git init -q $S/r;cd $S/r;git config user.name t;git config user.email t@t;git config gpg.format ssh;mkdir -p $G .agi/context/schemas .agi/nodes/doc
printf -- '---\n---\n  - {"name": "belam", "parent": "owner"}\n  - {"name": "council", "parent": "belam"}\n  - {"name": "keep", "parent": "belam"}\n  - {"name": "alive", "parent": "council"}\n  - {"name": "sanctuary-master", "parent": "keep"}\n  - {"name": "director-general-1", "parent": "sanctuary-master"}\n  - {"name": "director-general-9", "parent": "sanctuary-master"}\n'>$G/posts.md
printf 'owner cert-authority %s\nbelam %s\nalive %s\nsanctuary-master %s\ndirector-general-1 %s\n' "$(cut -d' ' -f1,2 $K/ca.pub)" "$(cut -d' ' -f1,2 $K/belam1.pub)" "$(cut -d' ' -f1,2 $K/alive1.pub)" "$(cut -d' ' -f1,2 $K/sm1.pub)" "$(cut -d' ' -f1,2 $K/dg1.pub)">$G/ring
printf -- '---\nid: doc:x\nring: [sanctuary-master]\n---\nbody\n'>.agi/nodes/doc/x.md;echo s>.agi/context/schemas/s.md;git add -A;git -c user.signingKey=$K/belam1.pub commit -q -S -m genesis;git branch -f trunk HEAD;git checkout -q --detach trunk
cm(){ k=$1;m=$2;shift 2;sh -c "$*";git add -A;git -c user.signingKey=$K/$k commit -q -S -m "$m" --allow-empty; }
pk(){ cut -d' ' -f1,2 $K/$1.pub; }
case_(){ n=$1; want=$2; o=$(sh $S/ring-gate trunk HEAD 2>&1); rc=$?; v=$([ $rc = 0 ] && echo ADMIT || echo REFUSE); [ $v = $want ] && r=PASS || r=FAIL; printf '%-4s %-6s %-64s %s\n' $r $v "$n" "$(echo $o|sed 's/[0-9a-f]\{40\}/<c>/'|cut -c1-90)"; [ $rc = 0 ] && [ "$3" != keep-out ] && git branch -f trunk HEAD; git checkout -q --detach trunk; }
cm alive1.pub a "echo a>>.agi/nodes/doc/y.md"; case_ "C1 alive gen1 plain node edit" ADMIT
cm alive1.pub h "sed -i 's|^alive .*|alive $(pk alive2)|' $G/ring"; case_ "C2 alive gen1 hands off to gen2 (its own line)" ADMIT
cm alive1.pub b "echo b>>.agi/nodes/doc/y.md"; case_ "C3 alive gen1 after the handoff" REFUSE
D=$(date -d '-1 day' -R); echo c>>.agi/nodes/doc/y.md; git add -A; GIT_COMMITTER_DATE="$D" GIT_AUTHOR_DATE="$D" git -c user.signingKey=$K/alive1.pub commit -q -S -m bd; case_ "C3b alive gen1, the commit BACKDATED a day" REFUSE
cm alive2.pub d "echo d>>.agi/nodes/doc/y.md"; case_ "C4 alive gen2 plain edit" ADMIT
B=$(git rev-parse trunk~2); git checkout -q --detach $B; cm alive1.pub e "echo e>.agi/nodes/doc/z.md"; SIDE=$(git rev-parse HEAD); git checkout -q --detach trunk; git -c user.signingKey=$K/sm1.pub merge -q --no-ff --no-edit -S $SIDE; case_ "C5 SM merges an OLD-BASE side commit by retired gen1" REFUSE
cm dg1.pub f "sed -i 's|^alive .*|alive $(pk dg1)|' $G/ring"; case_ "C6 DG1 rewrites alive's line (not above it)" REFUSE
cm belam1.pub g "sed -i 's|^alive .*|alive $(pk alive1)|' $G/ring"; case_ "C7 belam re-vouches alive's line (ancestor)" ADMIT keep-out
cm sm1.pub i "echo 'director-general-9 $(pk alive1)' >> $G/ring"; case_ "C8 SM stands up DG9's line (its parent)" ADMIT keep-out
cm alive2.pub j "echo 'director-general-9 $(pk alive1)' >> $G/ring"; case_ "C9 alive stands up DG9 (not above it)" REFUSE
cm dg1.pub k "echo f>>.agi/nodes/doc/x.md"; case_ "C10 DG1 edits a node ringed [sanctuary-master]" REFUSE
cm sm1.pub l "echo g>>.agi/nodes/doc/x.md"; case_ "C11 SM edits it (ring member)" ADMIT keep-out
cm belam1.pub m "echo h>>.agi/nodes/doc/x.md"; case_ "C12 belam edits it (above the member)" ADMIT keep-out
cm alive2.pub n "echo i>>.agi/nodes/doc/x.md"; case_ "C13 alive edits it (outside the subtree)" REFUSE
cm belam1.pub o "echo t>>.agi/context/schemas/s.md"; case_ "C14 belam's PLAIN key changes a schema (rules = owner)" REFUSE
cm belam1-cert.pub p "echo u>>.agi/context/schemas/s.md"; case_ "C15 belam's key + an owner window cert changes it" ADMIT keep-out
cm belam1.pub q "echo v>>.agi/context/schemas/s.md"; export AGI_RULES=belam; case_ "C16 option B (rules ring = belam): belam plain" ADMIT keep-out; unset AGI_RULES
cm belam1-cert.pub r "echo w>>.agi/nodes/doc/x.md"; case_ "C17 owner (cert) edits a node ringed [SM]: the tree's root" ADMIT keep-out
cm belam1.pub s "sed -i 's|^belam .*|belam $(pk belam2)|' $G/ring"; case_ "C18a belam gen1 hands off to gen2" ADMIT
cm belam1-cert.pub t "echo x>>.agi/context/schemas/s.md"; case_ "C18 an owner cert on RETIRED belam gen1 (cert still in date)" REFUSE
cm belam2-cert.pub u "echo y>>.agi/context/schemas/s.md"; case_ "C19 an owner cert on CURRENT belam gen2" ADMIT keep-out
cm sm1.pub v "sed -i 's|^owner .*|owner cert-authority $(pk sm1)|' $G/ring"; case_ "C20 SM replaces the owner line (moves the anchor)" REFUSE
cm belam2.pub w "sed -i 's|^owner .*|owner cert-authority $(pk sm1)|' $G/ring"; case_ "C21 belam replaces the owner line (only owner is above owner)" REFUSE
