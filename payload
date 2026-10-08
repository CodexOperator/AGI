#!/usr/bin/env python3
"""
Analyze session context files to test the premise of hypothesis:a01-c422b874-397418:
"Derivation chats have a front-loaded signal structure."

Measures whether the first 25% of chat lines carry disproportionally more
structural signal (IDs, edges, decisions, claims) than the tail 75%.

Proxy metric: "signal density" = number of structural tokens per line.
If head-25% has significantly higher signal density than tail-75%, the
front-loaded premise is supported.
"""
import os
import re
import json
import math
from collections import defaultdict

SESSIONS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sessions")
NODES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "nodes")

def count_signal_tokens(line):
    """Count structural signal tokens in a line.
    
    Structural signals = node IDs, edge references, type declarations,
    verdicts, goal references, tool_use markers.
    """
    count = 0
    # Node IDs (hex-ish patterns like a00-xxxx or goal:g10.1)
    count += len(re.findall(r'\b[a-z][0-9a-f]{7,8}(?:-[a-z0-9]+)*\b', line))
    # Edge markers
    count += len(re.findall(r'(?:→|->|parent:|child:|edge:|next_edges)', line))
    # Type declarations
    count += len(re.findall(r'\b(type|verdict|confidence|evidence_runs|status):', line))
    # Goal references
    count += len(re.findall(r'\bgoal:g\d+', line))
    # Hypothesis references
    count += len(re.findall(r'\bhypothesis:[a-z0-9-]+', line))
    # Tool calls
    count += len(re.findall(r'\b(tool_call|run_experiment|log_experiment|read|edit|write):', line))
    # Decision markers
    count += len(re.findall(r'\b(DONE|VERDICT|PROVED|DISPROVED|ACCEPT|REJECT)\b', line))
    return count

def is_structural_line(line):
    """Check if a line carries structural information vs boilerplate/cruft."""
    stripped = line.strip()
    if not stripped:
        return False
    # Boilerplate patterns (low-signal)
    boilerplate = [
        'Do not commit', 'Do not run', 'Do not force', 'do not wander',
        'Then signal completion', 'When done', 'If stuck', 'This line is here',
        'Guidelines:', 'Available tools:', 'In addition to the tools above',
        'You have access to', 'Current date:', 'Current working directory',
        'DEFAULT MODE:', 'pi documentation', 'Global default', 'Respond terse',
        'Active every response', 'Rules:', 'Drop articles',
    ]
    for bp in boilerplate:
        if bp in stripped:
            return False
    return True

def analyze_context_files():
    """Analyze all session context files for signal distribution."""
    results = []
    signal_by_quarter = defaultdict(list)
    
    for root, dirs, files in os.walk(SESSIONS_DIR):
        for f in files:
            if f == 'context.md':
                path = os.path.join(root, f)
                with open(path) as fh:
                    lines = fh.readlines()
                
                n = len(lines)
                if n < 10:
                    continue  # skip trivial files
                
                # Divide into quarters
                q1_end = max(1, int(n * 0.25))
                q2_end = max(q1_end + 1, int(n * 0.50))
                q3_end = max(q2_end + 1, int(n * 0.75))
                
                quarters = {
                    'head_25': lines[:q1_end],
                    'mid_25': lines[q1_end:q2_end],
                    'mid2_25': lines[q2_end:q3_end],
                    'tail_25': lines[q3_end:],
                }
                
                # Count signal per quarter
                signals = {}
                structural_lines = {}
                for qname, qlines in quarters.items():
                    total_signal = sum(count_signal_tokens(l) for l in qlines)
                    total_structural = sum(1 for l in qlines if is_structural_line(l))
                    signal_density = total_signal / len(qlines) if qlines else 0
                    struct_density = total_structural / len(qlines) if qlines else 0
                    signals[qname] = {
                        'signal_tokens': total_signal,
                        'structural_lines': total_structural,
                        'signal_density': round(signal_density, 3),
                        'struct_density': round(struct_density, 3),
                    }
                
                record = {
                    'file': path,
                    'total_lines': n,
                    'head_pct': signals['head_25']['signal_density'],
                    'mid1_pct': signals['mid_25']['signal_density'],
                    'mid2_pct': signals['mid2_25']['signal_density'],
                    'tail_pct': signals['tail_25']['signal_density'],
                    'head_signal_ratio': signals['head_25']['signal_tokens'] / max(1, sum(s['signal_tokens'] for s in signals.values())),
                    'head_struct_density': signals['head_25']['struct_density'],
                    'tail_struct_density': signals['tail_25']['struct_density'],
                }
                results.append(record)
    
    return results

def analyze_node_bodies():
    """Analyze node files for length/complexity distribution."""
    results = []
    body_lengths = defaultdict(list)
    
    for node_type in ['hypothesis', 'experiment', 'build', 'goal', 'mvp']:
        type_dir = os.path.join(NODES_DIR, node_type)
        if not os.path.isdir(type_dir):
            continue
        for f in os.listdir(type_dir):
            if not f.endswith('.md'):
                continue
            path = os.path.join(type_dir, f)
            with open(path) as fh:
                content = fh.read()
            
            # Split frontmatter from body
            parts = content.split('---\n', 2)
            if len(parts) < 3:
                continue
            frontmatter = parts[1]
            body = parts[2]
            
            body_lines = body.strip().split('\n')
            fm_lines = frontmatter.strip().split('\n')
            
            # Count structural tokens in frontmatter vs body
            fm_signal = sum(count_signal_tokens(l) for l in fm_lines)
            body_signal = sum(count_signal_tokens(l) for l in body_lines)
            
            # Measure frontmatter density vs body density
            body_lengths[node_type].append({
                'file': path,
                'fm_lines': len(fm_lines),
                'body_lines': len(body_lines),
                'fm_signal': fm_signal,
                'body_signal': body_signal,
                'fm_density': round(fm_signal / max(1, len(fm_lines)), 3),
                'body_density': round(body_signal / max(1, len(body_lines)), 3),
                'head_25_lines': max(1, int(len(body_lines) * 0.25)),
                'body_head_signal': sum(count_signal_tokens(l) for l in body_lines[:max(1, int(len(body_lines) * 0.25))]),
            })
    
    return body_lengths

def main():
    print("=" * 80)
    print("CHAT STRUCTURE ANALYSIS — Testing hypothesis:a01-c422b874-397418")
    print("Premise: Derivation chats have front-loaded signal structure")
    print("=" * 80)
    
    # 1. Analyze session context files
    print("\n--- 1. Session Context File Analysis ---")
    results = analyze_context_files()
    print(f"Analyzed {len(results)} session context files")
    
    if results:
        # Aggregate
        head_densities = [r['head_pct'] for r in results]
        mid1_densities = [r['mid1_pct'] for r in results]
        mid2_densities = [r['mid2_pct'] for r in results]
        tail_densities = [r['tail_pct'] for r in results]
        
        print(f"\nSignal density (signal tokens per line) by quarter:")
        print(f"  Head 25%:  mean={sum(head_densities)/len(head_densities):.3f}, median={sorted(head_densities)[len(head_densities)//2]:.3f}")
        print(f"  Mid 25%:   mean={sum(mid1_densities)/len(mid1_densities):.3f}")
        print(f"  Mid2 25%:  mean={sum(mid2_densities)/len(mid2_densities):.3f}")
        print(f"  Tail 25%:  mean={sum(tail_densities)/len(tail_densities):.3f}, median={sorted(tail_densities)[len(tail_densities)//2]:.3f}")
        
        # Head vs tail signal ratio
        head_signals = [r['head_signal_ratio'] for r in results]
        avg_head_ratio = sum(head_signals) / len(head_signals)
        print(f"\n  Head's share of total signal: {avg_head_ratio*100:.1f}% (random would be 25%)")
        
        # Count files where head has HIGHER density than tail
        higher_count = sum(1 for r in results if r['head_pct'] > r['tail_pct'])
        lower_count = sum(1 for r in results if r['head_pct'] < r['tail_pct'])
        equal_count = sum(1 for r in results if r['head_pct'] == r['tail_pct'])
        print(f"\n  Files where head > tail density: {higher_count}")
        print(f"  Files where head < tail density: {lower_count}")
        print(f"  Files where head == tail density: {equal_count}")
        
        # Structural line density
        head_struct = [r['head_struct_density'] for r in results]
        tail_struct = [r['tail_struct_density'] for r in results]
        print(f"\n  Structural line density (non-boilerplate / total):")
        print(f"    Head 25%: mean={sum(head_struct)/len(head_struct):.3f}")
        print(f"    Tail 25%: mean={sum(tail_struct)/len(tail_struct):.3f}")
        
        # Length distribution
        lengths = [r['total_lines'] for r in results]
        print(f"\n  File length distribution: min={min(lengths)}, max={max(lengths)}, median={sorted(lengths)[len(lengths)//2]}")
        
        # Binned by length
        short = [r for r in results if r['total_lines'] <= 80]
        medium = [r for r in results if 80 < r['total_lines'] <= 150]
        long = [r for r in results if r['total_lines'] > 150]
        
        print(f"\n  Length bins:")
        for label, bin_ in [("short (<=80)", short), ("medium (80-150)", medium), ("long (>150)", long)]:
            if bin_:
                avg_head = sum(r['head_pct'] for r in bin_) / len(bin_)
                avg_tail = sum(r['tail_pct'] for r in bin_) / len(bin_)
                print(f"    {label}: n={len(bin_)}, head_density={avg_head:.3f}, tail_density={avg_tail:.3f}, head>tail={sum(1 for r in bin_ if r['head_pct'] > r['tail_pct'])}/{len(bin_)}")
    else:
        print("  No context files found or all too short.")
    
    # 2. Analyze node body structure
    print("\n\n--- 2. Node Body Structure Analysis ---")
    body_data = analyze_node_bodies()
    
    for node_type, records in sorted(body_data.items()):
        if not records:
            continue
        n = len(records)
        avg_fm_lines = sum(r['fm_lines'] for r in records) / n
        avg_body_lines = sum(r['body_lines'] for r in records) / n
        avg_fm_density = sum(r['fm_density'] for r in records) / n
        avg_body_density = sum(r['body_density'] for r in records) / n
        avg_head_signal = sum(r['body_head_signal'] for r in records) / n
        
        print(f"\n  {node_type} nodes (n={n}):")
        print(f"    Avg frontmatter lines: {avg_fm_lines:.1f} (density: {avg_fm_density:.3f})")
        print(f"    Avg body lines: {avg_body_lines:.1f} (density: {avg_body_density:.3f})")
        print(f"    Frontmatter carries {avg_fm_density/max(0.001, avg_body_density):.1f}x more signal per line than body")
        print(f"    Avg signal in body head-25%: {avg_head_signal:.1f} tokens")
    
    # 3. Summary
    print("\n\n--- 3. Summary ---")
    print(f"Total session context files analyzed: {len(results)}")
    if results:
        head_densities = [r['head_pct'] for r in results]
        tail_densities = [r['tail_pct'] for r in results]
        
        if sum(head_densities) > sum(tail_densities):
            print("FINDING: Context files have front-loaded signal structure — head quarter")
            print(f"  carries more structural signal per line than tail quarter.")
            print(f"  This SUPPORTS the premise of hypothesis:a01-c422b874-397418 that")
            print(f"  derivation chats have front-loaded signal distribution.")
        elif sum(head_densities) < sum(tail_densities):
            print("FINDING: Context files have BACK-loaded signal structure — tail quarter")
            print(f"  carries more structural signal per line than head quarter.")
            print(f"  This WEAKENS the premise of hypothesis:a01-c422b874-397418.")
        else:
            print("FINDING: Signal is evenly distributed across context files.")
            print(f"  This is INCONCLUSIVE for the premise of hypothesis:a01-c422b874-397418.")
    
    print(f"\nTotal node types analyzed: {len(body_data)}")
    for node_type, records in sorted(body_data.items()):
        if records:
            total = len(records)
            avg_body = sum(r['body_lines'] for r in records) / total
            print(f"  {node_type}: {total} nodes, avg body length = {avg_body:.0f} lines")

if __name__ == '__main__':
    main()