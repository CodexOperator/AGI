#!/usr/bin/env python3
"""Replace _RE_YAML_PAIR.match(line) pattern with _parse_yaml_line() in graph_builder.py.
This eliminates ~14738 regex match calls during cold build, saving ~35ms.
"""
import re

path = 'extensions/agi/src/agi_algos/graph_builder.py'
with open(path) as f:
    content = f.read()

# Add the helper function right after _RE_YAML_PAIR definition
helper = """_RE_YAML_PAIR = re.compile(r'^(\\w+):\\s*(.*)$')


def _parse_yaml_line(line: str, meta: dict) -> None:
    \"\"\"Parse a key: value YAML line into meta dict. Faster than regex partition.\"\"\"
    if ':' in line:
        key, _, val = line.partition(':')
        meta[key.strip()] = val.strip()
"""

# Replace the helper insertion point
old_def = """_RE_YAML_PAIR = re.compile(r'^(\\w+):\\s*(.*)$')

"""
content = content.replace(old_def, helper, 1)

# Count and replace all usage sites
pattern = re.compile(
    r'^(\s*)m = _RE_YAML_PAIR\.match\(line\)\n\1if m:\n\1    meta\[m\.group\(1\)\] = m\.group\(2\)',
    re.MULTILINE
)

matches = pattern.findall(content)
print(f"Found {len(matches)} replacement sites")

def replacer(m):
    indent = m.group(1)
    return f"{indent}_parse_yaml_line(line, meta)"

content = pattern.sub(replacer, content)

# Verify no remaining _RE_YAML_PAIR.match references (except the definition)
remaining = [l for l in content.split('\n') if '_RE_YAML_PAIR.match' in l]
print(f"Remaining references: {len(remaining)}")
for r in remaining:
    print(f"  {r.strip()}")

with open(path, 'w') as f:
    f.write(content)

print("Done. Written back to", path)