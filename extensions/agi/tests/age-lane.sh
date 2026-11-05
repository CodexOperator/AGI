# age-lane.sh DIR: sourced by the out-line tests (goal:g7.16.1.11.46.15). When `age` is not on the PATH, fetch the PINNED archive package
# (age=1.1.1-1ubuntu0.24.04.3, council 20:23:34Z 10-25) with `apt-get download`, check its sha256 against the archive's own Packages entry,
# unpack it into DIR with `dpkg-deb -x` (no root) and put DIR/usr/bin on THIS test's PATH only. A host that already has the pinned age uses it.
# AGE_PIN=<ver> names another pin; a failed download or a sha that differs returns 1 (the caller says so and exits).
age_lane(){ command -v age >/dev/null 2>&1&&return 0;_p=${AGE_PIN:-1.1.1-1ubuntu0.24.04.3};mkdir -p "$1"||return 1
 (cd "$1"&&apt-get download age=$_p >/dev/null 2>&1)||return 1;_d=$(ls "$1"/age_*.deb 2>/dev/null|head -1);[ -f "$_d" ]||return 1
 _w=$(apt-cache show age=$_p 2>/dev/null|awk '/^SHA256:/{print $2;exit}');[ -n "$_w" ]&&[ "$(sha256sum "$_d"|cut -d' ' -f1)" = "$_w" ]||return 1
 dpkg-deb -x "$_d" "$1/x"||return 1;PATH=$1/x/usr/bin:$PATH;export PATH;}
