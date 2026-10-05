#!/bin/sh
# One writer refreshes the shared SuperGrok OIDC token into pi auth and
# every post grok auth. encryption-town only. Never prints the token.
set -eu
if [ "$(id -u)" -ne 0 ]; then
  exec sudo -n "$0" "$@"
fi
writer=/var/lib/agi/sanctuary-master/.grok/auth.json
pi=/opt/agi/pi-agent/auth.json
[ -f "$writer" ] || exit 2
python3 - "$writer" "$pi" << 'PY'
import datetime, grp, json, os, pwd, shutil, sys, time, urllib.parse, urllib.request, base64
writer, pi_path = sys.argv[1], sys.argv[2]
d = json.load(open(writer))
k = next(iter(d))
rec = d[k]
key = rec.get("key") or ""
exp = 0
parts = key.split(".")
if len(parts) >= 2:
    pad = parts[1] + "=" * ((4 - len(parts[1]) % 4) % 4)
    exp = int(json.loads(base64.urlsafe_b64decode(pad)).get("exp") or 0)
now = time.time()
if exp < now + 7200:
    body = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": rec["refresh_token"],
        "client_id": rec.get("oidc_client_id") or k.split("::", 1)[-1],
    }).encode()
    req = urllib.request.Request("https://auth.x.ai/oauth2/token", data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode())
    rec["key"] = data["access_token"]
    if data.get("refresh_token"):
        rec["refresh_token"] = data["refresh_token"]
    if data.get("expires_in"):
        rec["expires_at"] = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=int(data["expires_in"]))).isoformat().replace("+00:00", "Z")
    d[k] = rec
    tmp = writer + ".tmp"
    with open(tmp, "w") as f:
        json.dump(d, f)
    os.chmod(tmp, 0o600)
    os.replace(tmp, writer)
    os.chmod(writer, 0o600)
    print("refreshed")
else:
    print("fresh")
key = rec["key"]
pi = {"xai": {"type": "api_key", "key": key}}
tmp = pi_path + ".tmp"
with open(tmp, "w") as f:
    json.dump(pi, f)
os.chmod(tmp, 0o640)
os.replace(tmp, pi_path)
try:
    gid = grp.getgrnam("agi").gr_gid
except KeyError:
    gid = 0
os.chown(pi_path, 0, gid)
os.chmod(pi_path, 0o640)
n = 0
for name in sorted(os.listdir("/var/lib/agi")):
    if name == "sanctuary-master":
        continue
    try:
        pw = pwd.getpwnam("agi-" + name)
    except KeyError:
        continue
    home = "/var/lib/agi/" + name
    if not os.path.isdir(home):
        continue
    grok = home + "/.grok"
    os.makedirs(grok, mode=0o700, exist_ok=True)
    dest = grok + "/auth.json"
    shutil.copy(writer, dest)
    os.chown(grok, pw.pw_uid, pw.pw_gid)
    os.chown(dest, pw.pw_uid, pw.pw_gid)
    os.chmod(grok, 0o700)
    os.chmod(dest, 0o600)
    n += 1
print("fanout", n)
PY
