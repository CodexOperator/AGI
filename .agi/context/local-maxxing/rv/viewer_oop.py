"""goal:g5.48 -- the viewers, as their OWN process (fork + exec by harness_oop.py).

Protocol: one JSON object per line on stdin, {"trial": t, "commitment": c, "leak": salt_hex | null};
one JSON object per line on stdout, {"desc": [tags], "channel": name | null}.  argv carries only
PUBLIC values (kind, public seed, n, the public secret_sha256, the run dir); the env is scrubbed.

Kinds:
  null      the F1 null viewer (round 2's NullViewer, policy 0, keyed on the public seed);
  salt      the F2 planted-salt mutant (round 2's SaltMutantViewer; only the salt it is HANDED);
  attacker  A*: tries every same-uid channel to the parent's secret or targets, in this order,
            and describes the true target from the first that works, else answers like a null
            viewer (its own public stream):
              frame    the caller-frame chain (a local `target` / `targets`, a `secret/<hex>` key)
              gc       a gc heap walk (any tracked container holding a `secret/<hex>` key)
              environ  /proc/PPID/environ          cmdline  /proc/PPID/cmdline
              fd       every regular file /proc/PPID/fd/* resolves to
              mem      /proc/PPID/mem over the rw regions of /proc/PPID/maps
              files    every file under the run dir and the rv dir
              self     its own env and argv
            A candidate secret is accepted only if its sha256 equals the PUBLIC secret_sha256.
The attacker class is importable, so harness_oop.py also runs it IN process (mutant M1).
"""
import gc
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as h  # noqa: E402  (round 2's closed harness: imported, never edited)

KEY_RE = re.compile(rb"secret/([0-9a-f]{64})")
HEX_RE = re.compile(rb"(?<![0-9a-f])([0-9a-f]{64})(?![0-9a-f])")
CHANNELS = ("frame", "gc", "environ", "cmdline", "fd", "mem", "files", "self")


class Attacker:
    def __init__(self, seed, n, secret_sha256, dirs, ppid=None):
        self.seed, self.n, self.want, self.dirs = seed, n, secret_sha256, dirs
        self.ppid = ppid if ppid is not None else os.getppid()
        self.pool = h.make_pool(seed)
        self.targets, self.channel = None, None
        self.dead = set()          # channels that refused once (EPERM / EACCES): not retried
        self.tried = {c: 0 for c in CHANNELS}

    # -- candidate checks -------------------------------------------------------------------
    def _accept(self, hexes):
        for x in hexes:
            x = x.decode() if isinstance(x, bytes) else x
            try:
                if hashlib.sha256(bytes.fromhex(x)).hexdigest() == self.want:
                    return bytes.fromhex(x)
            except ValueError:
                pass
        return None

    def _scan(self, blob, any_hex=False):
        found = self._accept(m.group(1) for m in KEY_RE.finditer(blob))
        if found is None and any_hex:
            found = self._accept(m.group(1) for m in HEX_RE.finditer(blob))
        return found

    def _from_secret(self, secret, channel):
        self.targets = h.draw_targets(h.secret_key(secret), self.pool, self.n)
        self.channel = channel
        return True

    # -- channels ----------------------------------------------------------------------------
    def _frame(self, trial):
        f = sys._getframe(1)
        while f is not None:
            loc = f.f_locals
            if isinstance(loc.get("target"), int) and loc.get("trial") == trial:
                return ("target", loc["target"])
            for v in loc.values():
                if isinstance(v, str) and v.startswith("secret/"):
                    s = self._accept([v[len("secret/"):len("secret/") + 64]])
                    if s:
                        return ("secret", s)
            f = f.f_back
        return None

    def _gc(self):
        for o in gc.get_objects():
            vals = o.values() if isinstance(o, dict) else (o if isinstance(o, (list, tuple)) else ())
            for v in vals:
                if isinstance(v, (bytes, str)) and len(v) >= 71:
                    b = v.encode() if isinstance(v, str) else v
                    if b"secret/" in b:
                        s = self._scan(b)
                        if s:
                            return s
        return None

    def _read(self, path, limit=1 << 26):
        with open(path, "rb") as f:
            return f.read(limit)

    def _proc(self, name):
        return self._scan(self._read(f"/proc/{self.ppid}/{name}"), any_hex=True)

    def _fd(self):
        d = f"/proc/{self.ppid}/fd"
        for e in os.listdir(d):
            t = os.path.realpath(os.path.join(d, e))
            if os.path.isfile(t):
                s = self._scan(self._read(t), any_hex=True)
                if s:
                    return s
        return None

    def _mem(self):
        with open(f"/proc/{self.ppid}/maps") as m:
            regions = [ln.split() for ln in m]
        with open(f"/proc/{self.ppid}/mem", "rb", buffering=0) as mem:
            for r in regions:
                if "r" not in r[1] or (len(r) > 5 and r[5].startswith("[v")):
                    continue
                a, b = (int(x, 16) for x in r[0].split("-"))
                if b - a > 1 << 28:
                    continue
                try:
                    mem.seek(a)
                    s = self._scan(mem.read(b - a))
                except (OSError, ValueError, OverflowError):
                    continue
                if s:
                    return s
        return None

    def _files(self):
        for d in self.dirs:
            for root, _, files in os.walk(d):
                for fn in files:
                    try:
                        s = self._scan(self._read(os.path.join(root, fn)), any_hex=True)
                    except OSError:
                        continue
                    if s:
                        return s
        return None

    def _self(self):
        blob = "\0".join(sys.argv + [f"{k}={v}" for k, v in os.environ.items()]).encode()
        return self._scan(blob, any_hex=True)

    def _try(self, trial):
        for c in CHANNELS:
            if c in self.dead:
                continue
            self.tried[c] += 1
            try:
                if c == "frame":
                    r = self._frame(trial)
                    if r and r[0] == "target":
                        return ("target", r[1], c)
                    if r:
                        self._from_secret(r[1], c)
                        return None
                    continue
                s = {"gc": self._gc, "environ": lambda: self._proc("environ"),
                     "cmdline": lambda: self._proc("cmdline"), "fd": self._fd,
                     "mem": self._mem, "files": self._files, "self": self._self}[c]()
            except (PermissionError, ProcessLookupError, FileNotFoundError):
                self.dead.add(c)
                continue
            except OSError:
                self.dead.add(c)
                continue
            if s:
                self._from_secret(s, c)
                return None
            if c in ("environ", "cmdline", "fd", "files", "self"):
                self.dead.add(c)       # static content: one look is enough
        return None

    def describe(self, trial, commitment, leak=None):
        if self.targets is None:
            r = self._try(trial)
            if r:
                return set(self.pool[r[1]]), r[2]
        if self.targets is not None:
            return set(self.pool[self.targets[trial]]), self.channel
        return set(h.Dice(self.seed, f"viewer/attacker/{trial}").sample(h.VOCAB, h.TAGS_PER_TARGET)), None


def main(argv):
    kind, seed, n = argv[1], argv[2], int(argv[3])
    if kind == "null":
        v, ch = h.NullViewer(seed, 0), None
    elif kind == "salt":
        v, ch = h.SaltMutantViewer(h.make_pool(seed)), None
    elif kind == "attacker":
        v = Attacker(seed, n, argv[4], argv[5:])
    else:
        raise SystemExit(f"unknown kind {kind}")
    for line in sys.stdin:
        q = json.loads(line)
        leak = bytes.fromhex(q["leak"]) if q.get("leak") else None
        out = v.describe(q["trial"], q["commitment"], leak=leak)
        desc, ch = out if isinstance(out, tuple) else (out, None)
        print(json.dumps({"desc": sorted(desc), "channel": ch}), flush=True)
    if kind == "attacker":
        print(json.dumps({"tried": v.tried, "dead": sorted(v.dead)}), file=sys.stderr, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
