#!/usr/bin/env python3
"""memguard-proof2 -- goal:g7.16.1.11.40.1 Falsifier 1, read-only. usage: memguard-proof2.py GUARD_SCRIPT [PROC_ROOT=/proc]
Classifies every process of every agi-post@* cgroup with the GUARD'S OWN tree functions (post_rows, guarded: read out of the
rendered script, never a copy) and compares with /proc/PID/oom_score_adj and the nice in /proc/PID/stat: a spine or harness pid must
hold the protect value and a nice at or below the protect nice, every other pid must hold neither (a child inherits both). Exit 0 only when 0 pids are on the wrong side; 2 when the script cannot be read as a guard.
The guard sets a new spine/harness pid, and resets a child that inherited the protect value, on its NEXT tick, so a pid younger
than two ticks + 1 s is skipped and counted: the window is DERIVED from the script (2 x its time.sleep + 1), never a literal."""
import sys, re, os, collections

def main(script, proc='/proc'):
    src = open(script).read()
    sleeps = re.findall(r"time[.]sleep[(]([0-9.]+)[)]", src)
    cg = re.search(r"POST_CG = re.compile[(]r'(.*?)', re.M[)]", src)
    pv = re.search(r"setadj[(]pid, (-?[0-9]+)[)]", src)             # the FIRST numeric setadj in the source = the protect branch (the reset takes a variable, the pi worker's comes after it)
    pn = re.search(r"os[.]setpriority[(]os[.]PRIO_PROCESS, pid, (-?[0-9]+)[)]", src)      # likewise the first numeric setpriority = the protect nice
    if len(sleeps) != 1 or not cg or not pv or not pn or 'def post_rows' not in src or 'return out, bool(h)' not in src:
        print('NOT A GUARD: cannot read its tick, post cgroup, protect value or tree functions'); return 2
    min_age = 2 * float(sleeps[0]) + 1; prot = int(pv.group(1)); pnice = int(pn.group(1))
    ns = {'collections': collections, 'POST_CG': re.compile(cg.group(1), re.M)}
    exec(src[src.index('def post_rows'):src.index('return out, bool(h)') + len('return out, bool(h)')].replace('/proc', proc), ns)
    snap = []
    for d in os.listdir(proc):
        if d.isdigit():
            try: snap.append((int(d), open(f'{proc}/{d}/comm').read().strip(), open(f'{proc}/{d}/cmdline').read().replace(chr(0), ' '), 0))
            except Exception: pass
    up = float(open(f'{proc}/uptime').read().split()[0]); hz = os.sysconf('SC_CLK_TCK')
    def stat(p):
        s = open(f'{proc}/{p}/stat').read(); return s[s.rindex(')') + 2:].split()
    def age(p): return up - int(stat(p)[19]) / hz
    bad = n = young = 0; units = ns['post_rows'](snap)
    for unit, rows in sorted(units.items()):
        g, found = ns['guarded'](rows)
        if not found: print('NO HARNESS', unit); bad += 1
        for p in rows:
            try: a = int(open(f'{proc}/{p}/oom_score_adj').read()); nice = int(stat(p)[16]); old = age(p) >= min_age
            except Exception: continue
            if not old: young += 1; continue
            n += 1
            right = (a == prot and nice <= pnice) if p in g else (a != prot and nice != pnice)
            if not right: bad += 1; print('WRONG', unit.split('/')[-1], p, 'adj', a, 'nice', nice, 'should be protected' if p in g else 'should NOT be protected')
    print(f'{n} pids over {len(units)} units, {young} younger than {min_age:.0f} s skipped, {bad} on the wrong side')
    return 1 if bad else 0

if __name__ == '__main__':
    if len(sys.argv) not in (2, 3): print(__doc__.splitlines()[0]); sys.exit(2)
    sys.exit(main(*sys.argv[1:]))
