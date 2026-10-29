#!/bin/sh
# review-lanes.sh BASE TIP OUT [MAX] -- cut a merge range into area lanes for Sonnet subagent reviewers
# (skill agi-review; owner 00:4xZ 10-10: "just use sonnet subagents and we retired workflows.py in favor of
# shell scripts"). Writes OUT/range ("BASE TIP", full shas), OUT/all.txt (status<TAB>path) and one
# OUT/L<n>-<area>.txt per lane; an area with more than MAX files (default 40) splits into -a, -b, ...
# Every changed path lands in exactly one lane. Read-only on the repo; prints one line per lane.
set -eu
[ $# -ge 3 ] || { echo "usage: review-lanes.sh BASE TIP OUT [MAX]" >&2; exit 2; }
R=$(git rev-parse --show-toplevel)
B=$(git -C "$R" rev-parse --verify "$1^{commit}"); T=$(git -C "$R" rev-parse --verify "$2^{commit}")
O=$3; M=${4:-40}; mkdir -p "$O"; rm -f "$O"/L*.txt
echo "$B $T" > "$O/range"
git -C "$R" diff --name-status --no-renames "$B" "$T" | awk -F'\t' '{print $1"\t"$NF}' > "$O/all.txt"
# area = the first rule that matches; order matters (most specific first)
awk -F'\t' '
  { p=$2; a="other"
    if (p ~ /^extensions\/agi\/tests\//) a="tests"
    else if (p ~ /^extensions\/agi\/guard\// || p ~ /^skills\//) a="guard-skills"
    else if (p ~ /^extensions\// || p ~ /^src\// || p ~ /^\.claude\// || p ~ /^\.gitignore$/ || p ~ /^\.env\.example$/) a="engine"
    else if (p ~ /^\.agi\/nodes\/(goal|town|vision)\//) a="goals"
    else if (p ~ /^\.agi\/nodes\/doc\//) a="docs"
    else if (p ~ /^\.agi\/nodes\/(build|hypothesis|experiment|verdict|outcome|idea|mvp)\//) a="research-build"
    else if (p ~ /^\.agi\/nodes\/deprecated\//) a="deprecated"
    else if (p ~ /^\.agi\// || p ~ /^datasets\//) a="config-sessions"
    print a "\t" $0 }' "$O/all.txt" | sort -s -k1,1 > "$O/.tagged"
n=0
for a in $(cut -f1 "$O/.tagged" | uniq); do
  grep "^$a	" "$O/.tagged" | cut -f2- > "$O/.area"
  c=$(wc -l < "$O/.area"); k=$(( (c + M - 1) / M ))
  if [ "$k" -le 1 ]; then n=$((n+1)); cp "$O/.area" "$O/L$n-$a.txt"; echo "L$n-$a $c"
  else i=0; for s in a b c d e f g h i j k l m n o p; do [ $i -lt $k ] || break
    n=$((n+1)); awk -v k="$k" -v i="$i" 'NR % k == i' "$O/.area" > "$O/L$n-$a-$s.txt"
    echo "L$n-$a-$s $(wc -l < "$O/L$n-$a-$s.txt")"; i=$((i+1)); done; fi
done
rm -f "$O/.tagged" "$O/.area"
t=$(cat "$O"/L*.txt | wc -l); a=$(wc -l < "$O/all.txt")
[ "$t" = "$a" ] || { echo "review-lanes: lanes hold $t of $a paths" >&2; exit 1; }
echo "range ${B%"${B#?????????}"}..${T%"${T#?????????}"}: $a paths in $n lanes"
