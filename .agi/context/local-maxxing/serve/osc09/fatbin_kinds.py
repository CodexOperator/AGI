"""OSC.09 harvest (director-thought): count the entries of every fatbin in a raw .nv_fatbin section
(objcopy -O binary --only-section=.nv_fatbin LIB OUT) by (kind, sm arch).
kind 1 = PTX (JIT-compiled by the driver at first use), kind 2 = ELF cubin (SASS, runs as shipped)."""
import struct, sys, collections
data = open(sys.argv[1], "rb").read()  # the raw .nv_fatbin section (objcopy -O binary --only-section=.nv_fatbin)
cnt = collections.Counter(); off = 0; containers = 0
while off + 16 <= len(data):
    magic, ver, hsz, fsz = struct.unpack_from("<IHHQ", data, off)
    if magic != 0xBA55ED50:
        off += 8; continue
    containers += 1; e = off + hsz; end = off + hsz + fsz
    while e + 32 <= end:
        kind, _, ehsz, psz = struct.unpack_from("<HHIQ", data, e)
        arch = struct.unpack_from("<I", data, e + 28)[0]
        cnt[({1: "PTX", 2: "SASS"}.get(kind, "kind%d" % kind), "sm_%d" % arch)] += 1
        e += ehsz + psz
    off = end
print("fatbin containers:", containers)
for (k, a), n in sorted(cnt.items()): print("  %-4s %-6s entries=%d" % (k, a, n))
