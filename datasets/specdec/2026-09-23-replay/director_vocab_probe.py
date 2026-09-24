#!/usr/bin/env python3
"""Director framing probe for hypothesis:lm-agent-transcript-replay-prices-ngram-speculation.

Do two GGUF files carry the SAME tokenizer (model, pre, tokens, merges, token types, special ids)?
If they do, the live brain's read-only /tokenize yields the served 9B's token ids and can stand in
for the stopped router's. Reads only the GGUF header through mmap; prints counts and sha256
digests, never token text.

Usage: director_vocab_probe.py <a.gguf> <b.gguf>
"""
import hashlib
import json
import mmap
import os
import struct
import sys

SCALAR = {0: "<B", 1: "<b", 2: "<H", 3: "<h", 4: "<I", 5: "<i", 6: "<f", 7: "<?",
          10: "<Q", 11: "<q", 12: "<d"}
WANT = ("tokenizer.ggml.model", "tokenizer.ggml.pre", "tokenizer.ggml.tokens",
        "tokenizer.ggml.merges", "tokenizer.ggml.token_type", "tokenizer.ggml.bos_token_id",
        "tokenizer.ggml.eos_token_id", "tokenizer.ggml.padding_token_id",
        "tokenizer.ggml.add_bos_token")


def read_header(path):
    with open(path, "rb") as fh:
        mm = mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ)
    off = 4
    if mm[:4] != b"GGUF":
        raise SystemExit("%s: not a GGUF file" % os.path.basename(path))

    def take(fmt):
        nonlocal off
        val = struct.unpack_from(fmt, mm, off)[0]
        off += struct.calcsize(fmt)
        return val

    def string():
        nonlocal off
        n = take("<Q")
        val = mm[off:off + n]
        off += n
        return val

    def value(kind):
        if kind in SCALAR:
            return take(SCALAR[kind])
        if kind == 8:
            return string()
        if kind == 9:
            elem, n = take("<I"), take("<Q")
            return [value(elem) for _ in range(n)]
        raise SystemExit("unknown GGUF value type %d" % kind)

    out = {"version": take("<I")}
    take("<Q")  # tensor count
    for _ in range(take("<Q")):
        key = string().decode()
        val = value(take("<I"))
        if key in WANT:
            out[key] = val
    return out


def as_bytes(items):
    return [x if isinstance(x, bytes) else str(x).encode() for x in items]


def digest(val):
    if isinstance(val, list):
        return {"n": len(val), "sha256": hashlib.sha256(b"\0".join(as_bytes(val))).hexdigest()[:16]}
    return val.decode(errors="replace") if isinstance(val, bytes) else val


def common_prefix(a, b):
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n


def main(a_path, b_path):
    a, b = read_header(a_path), read_header(b_path)
    rows = {}
    for key in WANT:
        va, vb = a.get(key), b.get(key)
        row = {"a": digest(va) if va is not None else None,
               "b": digest(vb) if vb is not None else None, "equal": va == vb}
        if isinstance(va, list) and isinstance(vb, list) and va != vb:
            row["common_prefix"] = common_prefix(va, vb)
        rows[key] = row
    report = {"a": os.path.basename(a_path), "b": os.path.basename(b_path),
              "tokenizer_identical": all(r["equal"] for r in rows.values()), "keys": rows}
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2])
