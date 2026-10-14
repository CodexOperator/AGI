#!/bin/sh
# A0 -- STAGE (inert: reads MAIN, writes only under $STAGE; no sudo, nothing under /usr, /etc, /var). The ONE source of every act below:
# this file and its siblings (memguard-a1.sh, -a1.proof.sh, -a1.undo.sh, -a2.sh, -a2.proof.sh, -a2.undo.sh, -restage.sh, memguard-proof2.py) are the
# bytes AT the GO sha; A0 archives that tree to $STAGE/src and every later act runs from there, never from a copy in a home.
# usage: SHA=<the 40-hex GO sha> [STAGE=$HOME/memguard-A0] [MAIN=/data/work/agi] sh memguard-a0.sh
#   bootstrap: git -C $MAIN show $SHA:extensions/agi/boxkit/memguard-a0.sh > $HOME/memguard-a0.sh   (A0 itself cannot come from the archive it makes)
set -eu
: "${SHA:?set SHA to the 40-hex sha the GO names}"
STAGE="${STAGE:-$HOME/memguard-A0}"; MAIN="${MAIN:-/data/work/agi}"
case "$STAGE" in                                                       # rm -rf runs on STAGE: only a directory of our own making, under HOME
  *..*|"") echo "A0 REFUSED: STAGE is empty or holds '..': $STAGE"; exit 1;;
  "$HOME"/memguard-A0*) [ -n "$HOME" ] && [ "$HOME" != / ] || { echo "A0 REFUSED: HOME is empty or /"; exit 1; };;
  *) echo "A0 REFUSED: STAGE must be under HOME and named memguard-A0*: $STAGE"; exit 1;;
esac
case "$SHA" in *[!0-9a-f]*|"") echo "A0 REFUSED: SHA is not lowercase hex"; exit 1;; esac
[ "${#SHA}" = 40 ] || { echo "A0 REFUSED: SHA must be the full 40 hex"; exit 1; }
git -C "$MAIN" cat-file -e "$SHA^{commit}" || { echo "A0 REFUSED: $SHA is not a commit in $MAIN"; exit 1; }
rm -rf "$STAGE"; mkdir -p "$STAGE/src" "$STAGE/out"
git -C "$MAIN" archive "$SHA" | tar -x -C "$STAGE/src"                 # the bytes AT the sha; MAIN's checkout is never touched
python3 -I - "$STAGE" <<'PY'
import sys, json, hashlib, importlib.util, pwd, os
from pathlib import Path
stage = Path(sys.argv[1]); src = stage / "src"; out = stage / "out"
cfg = json.loads((src / ".agi/config.json").read_text(encoding="utf-8")); cells = cfg["paths"]["boxkit"]
fx = src / cells["fixtures_dir"]
load = lambda n: {k: v for k, v in json.loads((fx / n).read_text(encoding="utf-8")).items() if not k.startswith("_")}
meas = {k: v for k, v in load("measurements.json").items() if k != "box"}; stand = load("standins.json")
spec = importlib.util.spec_from_file_location("boxkit_render", src / "extensions/agi/boxkit/render.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
pieces = {p["name"]: p for p in R.manifest(src / cells["templates_dir"])["pieces"]}
owner = pwd.getpwuid(os.getuid()).pw_name
sums = []
for name, dest in (("memguard-script", "agi-memguard.py"), ("memguard-service", "agi-memguard.service")):
    piece = pieces[name]
    # C1: the template AT this sha, rendered with the STAND-INS (the recipe of tests/test_boxkit_templates._vs), must hash to the manifest's fixture_sha256
    got = R.rendered(piece, R.values(cfg, meas, stand, guard={}), src / cells["templates_dir"])
    h = hashlib.sha256(got.encode("utf-8")).hexdigest()
    onfile = hashlib.sha256((fx / (name + ".fixture")).read_bytes()).hexdigest()
    print(f"C1 {name}: stand-in render {h[:16]}  manifest {piece['fixture_sha256'][:16]}  fixture file {onfile[:16]}")
    if not (h == piece["fixture_sha256"] == onfile):
        print(f"A0 REFUSED (C1): {name} does not hash to its fixture"); sys.exit(1)
    # the real-values stage: the same render with this uid's identity tokens; it may differ from the stand-in render ONLY where the owner name is
    real = R.rendered(piece, R.values(cfg, meas, {**stand, "OWNER_USER": owner, "UID": str(os.getuid())}, guard={}), src / cells["templates_dir"])
    if real.replace(owner, stand["OWNER_USER"]) != got:
        print(f"A0 REFUSED: the real render of {name} differs from the stand-in render by more than the owner name"); sys.exit(1)
    (out / dest).write_text(real, encoding="utf-8")
    (out / dest).chmod(int(piece["mode"], 8))
    sums.append(f"{hashlib.sha256(real.encode('utf-8')).hexdigest()}  {dest}")
(out / "SHA256SUMS").write_text("\n".join(sums) + "\n")
PY
python3 -I -m py_compile "$STAGE/out/agi-memguard.py" && echo "py_compile agi-memguard.py: ok"; rm -rf "$STAGE/out/__pycache__"
cat "$STAGE/out/SHA256SUMS"
echo "$SHA" > "$STAGE/SHA"
echo "A0 OK: staged $STAGE/out (inert: /usr/local/sbin/agi-memguard.py exists? $( [ -e /usr/local/sbin/agi-memguard.py ] && echo YES || echo no))"
