#!/usr/bin/env python3
"""GGUF zero-ablation surgery for full-attention KV groups of the served Qwen3.5-9B.

Parses the GGUF header itself (tensor offsets + general.alignment), asserts
blk.<L>.attn_output.weight is Q4_K with shape (4096, 4096), saves the original
tensor bytes, and zeroes Q4_K super-blocks 4g..4g+3 of every row for one or more
KV groups g of a layer L -- the 4 query heads of group g. Zeroing a block
(d = dmin = 0, scale bytes 0) dequantizes to exactly 0, so the group's
write-back into the residual stream is removed with no requantization.

    python3 kv_group_surgery.py info
    python3 kv_group_surgery.py save  <L>          # original tensor -> scratch
    python3 kv_group_surgery.py patch <L> <g,g,..> # zero those groups (idempotent)
    python3 kv_group_surgery.py restore <L>        # original bytes back + sha check
    python3 kv_group_surgery.py tensor-sha <L>

The model file is a scratch COPY (paths.get("osc02_scratch_dir")); the served
model path is never opened for writing. Out-of-repo roots are resolved through
paths.py and proposed as box cells, never config keys.
"""
import hashlib, os, struct, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import paths

MODEL = paths.get("osc02_9b_gguf")
SCRATCH = paths.get("osc02_scratch_dir")
Q4_K, BLOCK, BSIZE = 12, 256, 144  # ggml_type Q4_K: 256 elems / 144 bytes
NSUP = 16                          # super-blocks per row == query heads


class GGUF:
    def __init__(self, path):
        self.path = path
        with open(path, "rb") as f:
            if f.read(4) != b"GGUF":
                raise ValueError("not a GGUF file")
            self.version = struct.unpack("<I", f.read(4))[0]
            n_tensors, n_kv = struct.unpack("<QQ", f.read(8 + 8))
            self.kv = {}
            for _ in range(n_kv):
                k = self._str(f)
                self.kv[k] = self._val(f)
            self.tensors = {}
            for _ in range(n_tensors):
                name = self._str(f)
                nd = struct.unpack("<I", f.read(4))[0]
                dims = struct.unpack("<%dQ" % nd, f.read(8 * nd)) if nd else ()
                ttype, off = struct.unpack("<IQ", f.read(12))
                self.tensors[name] = (dims, ttype, off)
            align = self.kv.get("general.alignment", 32)
            pos = f.tell()
            self.data = pos + (-pos % align)

    def _str(self, f):
        return f.read(struct.unpack("<Q", f.read(8))[0]).decode("utf-8")

    def _val(self, f):
        t = struct.unpack("<I", f.read(4))[0]
        if t == 8:
            return self._str(f)
        if t == 9:
            at = struct.unpack("<I", f.read(4))[0]
            n = struct.unpack("<Q", f.read(8))[0]
            return [self._str(f) if at == 8 else self._scalar(f, at) for _ in range(n)]
        return self._scalar(f, t)

    @staticmethod
    def _scalar(f, t):
        fmt = {0: "<B", 1: "<b", 2: "<H", 3: "<h", 4: "<I", 5: "<i",
               6: "<f", 7: "<?" , 10: "<Q", 11: "<q", 12: "<d"}[t]
        return struct.unpack(fmt, f.read(struct.calcsize(fmt)))[0]


def layer_tensors(g):
    out = {}
    for name, (dims, ttype, off) in g.tensors.items():
        if name.endswith(".attn_output.weight"):
            out[int(name.split(".")[1])] = (dims, ttype, off)
    return out


def geom(g, L):
    dims, ttype, off = layer_tensors(g)[L]
    assert ttype == Q4_K, "blk.%d.attn_output.weight type %d != Q4_K" % (L, ttype)
    assert dims == (4096, 4096), "shape %r != (4096, 4096)" % (dims,)
    ne0, ne1 = dims
    assert ne0 // BLOCK == NSUP
    return g.data + off, ne0 // BLOCK * BSIZE, ne1


def tsize(L):
    _, stride, rows = geom(GGUF(MODEL), L)
    return stride * rows


def tensor_sha(L):
    base, stride, rows = geom(GGUF(MODEL), L)
    h = hashlib.sha256()
    with open(MODEL, "rb") as f:
        f.seek(base)
        left = stride * rows
        while left:
            b = f.read(min(1 << 20, left))
            h.update(b)
            left -= len(b)
    return h.hexdigest()


def save(L):
    base, stride, rows = geom(GGUF(MODEL), L)
    dst = os.path.join(SCRATCH, "orig_L%d.q4k" % L)
    with open(MODEL, "rb") as f, open(dst, "wb") as o:
        f.seek(base)
        left = stride * rows
        while left:
            b = f.read(min(1 << 20, left))
            o.write(b)
            left -= len(b)
    with open(dst + ".sha256", "w") as o:
        o.write(tensor_sha(L) + "\n")
    return dst


def patch(L, groups):
    base, stride, rows = geom(GGUF(MODEL), L)
    zeros = b"\0" * (4 * BSIZE)
    with open(MODEL, "r+b") as f:
        for r in range(rows):
            for g in groups:
                f.seek(base + r * stride + 4 * g * BSIZE)
                f.write(zeros)
        f.flush()
        os.fsync(f.fileno())


def restore(L):
    src = os.path.join(SCRATCH, "orig_L%d.q4k" % L)
    before = open(src + ".sha256").read().strip()
    base, stride, rows = geom(GGUF(MODEL), L)
    with open(MODEL, "r+b") as f, open(src, "rb") as o:
        f.seek(base)
        left = stride * rows
        while left:
            b = o.read(min(1 << 20, left))
            f.write(b)
            left -= len(b)
        f.flush()
        os.fsync(f.fileno())
    after = tensor_sha(L)
    assert before == after, "restore sha mismatch %s != %s" % (before, after)
    return after


def main(argv):
    cmd = argv[1]
    g = GGUF(MODEL)
    if cmd == "info":
        lt = layer_tensors(g)
        print("version", g.version, "align", g.kv.get("general.alignment", 32),
              "data", g.data, "scratch", SCRATCH)
        for L in sorted(lt):
            base, stride, rows = geom(g, L)
            print("L=%d dims=%r type=%d off=%d base=%d stride=%d rows=%d bytes=%d"
                  % (L, lt[L][0], lt[L][1], lt[L][2], base, stride, rows, stride * rows))
    elif cmd == "save":
        print(save(int(argv[2])))
    elif cmd == "patch":
        gs = [int(x) for x in argv[3].split(",")]
        patch(int(argv[2]), gs)
        print("patched L=%s groups=%s tensor_sha=%s" % (argv[2], gs, tensor_sha(int(argv[2]))))
    elif cmd == "restore":
        print("restored L=%s tensor_sha=%s" % (argv[2], restore(int(argv[2]))))
    elif cmd == "tensor-sha":
        print(tensor_sha(int(argv[2])))
    else:
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv) or 0)
