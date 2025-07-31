#!/usr/bin/env python3
"""
Efficient Loop Detection for Large Knowledge Graphs

This script uses memory-efficient algorithms to detect cycles in large graphs
without running out of memory or taking excessive time.
"""

import pandas as pd
import networkx as nx
import os
from datetime import datetime
import time
import sys
import glob

# File paths
CHECKER_INPUT_DIR = "checker_input"
OUTPUT_DIR = "checker_output"

def find_input_files():
    """Find concept and relationship files in checker_input folder."""
    concept_files = glob.glob(f"{CHECKER_INPUT_DIR}/*concepts*.csv")
    relationship_files = glob.glob(f"{CHECKER_INPUT_DIR}/*relationships*.csv")
    
    if not concept_files:
        print(f"Error: No files with 'concepts' in the name found in {CHECKER_INPUT_DIR}/")
        print("Please copy your concepts file to the checker_input folder")
        return None, None
    
    if not relationship_files:
        print(f"Error: No files with 'relationships' in the name found in {CHECKER_INPUT_DIR}/")
        print("Please copy your relationships file to the checker_input folder")
        return None, None
    
    # Use the first matching file for each type
    concepts_file = concept_files[0]
    relationships_file = relationship_files[0]
    
    print(f"Found concepts file: {os.path.basename(concepts_file)}")
    print(f"Found relationships file: {os.path.basename(relationships_file)}")
    
    return concepts_file, relationships_file

def load_data():
    """Load concepts and relationships from checker_input folder."""
    try:
        concepts_file, relationships_file = find_input_files()
        if concepts_file is None:
            return None, None
            
        concepts = pd.read_csv(concepts_file)
        relationships = pd.read_csv(relationships_file)
        print(f"Loaded {len(concepts)} concepts and {len(relationships)} relationships")
        return concepts, relationships
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please copy your concepts.csv and relationships.csv files to the checker_input folder")
        return None, None

def build_graph(relationships):
    """Build a directed graph from relationships."""
    G = nx.DiGraph()
    
    # Add edges from relationships
    for _, rel in relationships.iterrows():
        G.add_edge(rel['prerequisite_id'], rel['dependent_id'])
    
    print(f"Built graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    return G

def find_cycles_efficient(graph, max_cycles=100):
    """
    Find cycles using a memory-efficient approach.
    Limits the number of cycles found to prevent memory issues.
    """
    cycles = []
    visited = set()
    
    def dfs_find_cycles(node, path, rec_stack):
        """DFS to find cycles with early termination."""
        if len(cycles) >= max_cycles:
            return
        
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        
        for neighbor in graph.successors(node):
            if neighbor not in visited:
                dfs_find_cycles(neighbor, path, rec_stack)
            elif neighbor in rec_stack:
                # Found a cycle
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                cycles.append(cycle)
                if len(cycles) >= max_cycles:
                    return
        
        rec_stack.remove(node)
        path.pop()
    
    # Start DFS from each unvisited node
    for node in graph.nodes():
        if node not in visited and len(cycles) < max_cycles:
            dfs_find_cycles(node, [], set())
    
    return cycles

def check_acyclic_efficient(graph):
    """
    Check if graph is acyclic using topological sort.
    This is much faster than finding all cycles.
    """
    try:
        # Try to find a topological sort
        topo_order = list(nx.topological_sort(graph))
        return True, topo_order
    except (nx.NetworkXError, nx.NetworkXUnfeasible):
        # Graph has cycles
        return False, None

def find_small_cycles_only(graph, max_cycle_length=5):
    """
    Find only small cycles (up to max_cycle_length) which are more likely to be problematic.
    """
    cycles = []
    visited = set()
    
    def dfs_small_cycles(node, path, rec_stack):
        if len(path) > max_cycle_length:
            return
        
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        
        for neighbor in graph.successors(node):
            if neighbor not in visited:
                dfs_small_cycles(neighbor, path, rec_stack)
            elif neighbor in rec_stack and len(path) <= max_cycle_length:
                # Found a small cycle
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                cycles.append(cycle)
        
        rec_stack.remove(node)
        path.pop()
    
    for node in graph.nodes():
        if node not in visited:
            dfs_small_cycles(node, [], set())
    
    return cycles

def analyze_cycles_limited(cycles, concepts, relationships, max_cycles_to_analyze=50):
    """Analyze cycles with a limit to prevent memory issues."""
    cycle_details = []
    
    for i, cycle in enumerate(cycles[:max_cycles_to_analyze]):
        cycle_info = {
            'cycle_id': i + 1,
            'cycle_length': len(cycle),
            'cycle_nodes': cycle,
            'cycle_concepts': [],
            'cycle_relationships': []
        }
        
        # Get concept names for the cycle
        for node_id in cycle:
            concept = concepts[concepts['id'] == node_id]
            if not concept.empty:
                cycle_info['cycle_concepts'].append(concept.iloc[0]['name'])
        
        # Get relationships in the cycle
        for j in range(len(cycle)):
            prereq_id = cycle[j]
            dep_id = cycle[(j + 1) % len(cycle)]
            
            rel = relationships[
                (relationships['prerequisite_id'] == prereq_id) & 
                (relationships['dependent_id'] == dep_id)
            ]
            
            if not rel.empty:
                rel_row = rel.iloc[0]
                cycle_info['cycle_relationships'].append({
                    'prerequisite': rel_row['prerequisite_name'],
                    'dependent': rel_row['dependent_name'],
                    'explanation': rel_row['explanation']
                })
        
        cycle_details.append(cycle_info)
    
    return cycle_details

def find_long_paths_efficient(graph, max_length=10, max_paths=100):
    """Find long paths more efficiently with limits."""
    long_paths = []
    nodes = list(graph.nodes())
    
    # Sample nodes to check (don't check all pairs)
    sample_size = min(50, len(nodes))
    sample_nodes = nodes[:sample_size]
    
    for i, start in enumerate(sample_nodes):
        if len(long_paths) >= max_paths:
            break
            
        for end in sample_nodes[i+1:]:
            if len(long_paths) >= max_paths:
                break
                
            try:
                path = nx.shortest_path(graph, start, end)
                if len(path) > max_length:
                    long_paths.append({
                        'start': start,
                        'end': end,
                        'path_length': len(path),
                        'path': path
                    })
            except nx.NetworkXNoPath:
                continue
    
    return long_paths

def generate_efficient_report(is_acyclic, cycles, long_paths, concepts, relationships):
    """Generate a simplified report."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Summary report
    summary_file = f"{OUTPUT_DIR}/efficient_summary_{timestamp}.txt"
    with open(summary_file, 'w') as f:
        f.write("EFFICIENT LOOP DETECTION RESULTS\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Concepts: {len(concepts)}\n")
        f.write(f"Total Relationships: {len(relationships)}\n\n")
        
        if is_acyclic:
            f.write("✅ GRAPH IS ACYCLIC - No cycles detected!\n")
            f.write("Your knowledge graph structure is valid.\n\n")
        else:
            f.write("⚠️  CYCLES DETECTED!\n")
            f.write(f"Found {len(cycles)} cycles\n\n")
            
            # Show all cycles with concept names
            f.write("ALL CYCLES FOUND:\n")
            f.write("-" * 20 + "\n")
            for i, cycle in enumerate(cycles):
                cycle_concepts = []
                for node_id in cycle:
                    concept = concepts[concepts['id'] == node_id]
                    if not concept.empty:
                        cycle_concepts.append(concept.iloc[0]['name'])
                
                f.write(f"Cycle {i+1} (Length {len(cycle)}): {' → '.join(cycle_concepts)}\n")
                
                # Show the relationships in this cycle
                f.write("  Relationships in this cycle:\n")
                for j in range(len(cycle)):
                    prereq_id = cycle[j]
                    dep_id = cycle[(j + 1) % len(cycle)]
                    
                    rel = relationships[
                        (relationships['prerequisite_id'] == prereq_id) & 
                        (relationships['dependent_id'] == dep_id)
                    ]
                    
                    if not rel.empty:
                        rel_row = rel.iloc[0]
                        f.write(f"    • {rel_row['prerequisite_name']} → {rel_row['dependent_name']}\n")
                        f.write(f"      Reason: {rel_row['explanation']}\n")
                
                f.write("\n")
        
        if long_paths:
            f.write(f"\nLong paths found: {len(long_paths)} (showing first 10)\n")
            for i, path_info in enumerate(long_paths[:10]):
                start_concept = concepts[concepts['id'] == path_info['start']].iloc[0]['name']
                end_concept = concepts[concepts['id'] == path_info['end']].iloc[0]['name']
                f.write(f"Path {i+1}: {start_concept} → ... → {end_concept} ({path_info['path_length']} steps)\n")
    
    # Also create a CSV export of all cycles for easier analysis
    if cycles:
        cycles_csv = f"{OUTPUT_DIR}/all_cycles_{timestamp}.csv"
        cycle_data = []
        
        for i, cycle in enumerate(cycles):
            for j in range(len(cycle)):
                prereq_id = cycle[j]
                dep_id = cycle[(j + 1) % len(cycle)]
                
                rel = relationships[
                    (relationships['prerequisite_id'] == prereq_id) & 
                    (relationships['dependent_id'] == dep_id)
                ]
                
                if not rel.empty:
                    rel_row = rel.iloc[0]
                    cycle_data.append({
                        'cycle_id': i + 1,
                        'cycle_length': len(cycle),
                        'prerequisite_id': prereq_id,
                        'dependent_id': dep_id,
                        'prerequisite_name': rel_row['prerequisite_name'],
                        'dependent_name': rel_row['dependent_name'],
                        'explanation': rel_row['explanation'],
                        'source': rel_row['source']
                    })
        
        cycle_df = pd.DataFrame(cycle_data)
        cycle_df.to_csv(cycles_csv, index=False)
        print(f"All cycles exported to: {cycles_csv}")
    
    return summary_file

def main():
    """Main function with efficient loop detection."""
    print("Efficient Loop Detection for Large Knowledge Graphs")
    print("=" * 55)
    
    # Load data
    print("Loading data...")
    concepts, relationships = load_data()
    if concepts is None:
        return
    
    # Build graph
    print("Building graph...")
    graph = build_graph(relationships)
    
    # First, check if graph is acyclic (fast check)
    print("Checking if graph is acyclic...")
    start_time = time.time()
    is_acyclic, topo_order = check_acyclic_efficient(graph)
    check_time = time.time() - start_time
    
    print(f"Acyclic check completed in {check_time:.2f} seconds")
    
    if is_acyclic:
        print("✅ Graph is acyclic - no cycles found!")
        cycles = []
    else:
        print("⚠️  Graph has cycles - finding them...")
        
        # Find small cycles only (more likely to be problematic)
        start_time = time.time()
        cycles = find_small_cycles_only(graph, max_cycle_length=5)
        cycle_time = time.time() - start_time
        
        print(f"Found {len(cycles)} small cycles in {cycle_time:.2f} seconds")
        
        if len(cycles) == 0:
            # Try finding larger cycles with limits
            print("No small cycles found - checking for larger cycles...")
            cycles = find_cycles_efficient(graph, max_cycles=100)
            print(f"Found {len(cycles)} cycles total")
    
    # Find long paths (sampled)
    print("Checking for long paths...")
    long_paths = find_long_paths_efficient(graph, max_length=10, max_paths=50)
    print(f"Found {len(long_paths)} long paths")
    
    # Generate report
    print("Generating report...")
    summary_file = generate_efficient_report(is_acyclic, cycles, long_paths, concepts, relationships)
    
    print(f"\nReport saved to: {summary_file}")
    print(f"\nSUMMARY:")
    print(f"  • Graph is acyclic: {is_acyclic}")
    print(f"  • Cycles found: {len(cycles)}")
    print(f"  • Long paths found: {len(long_paths)}")
    
    if not is_acyclic:
        print(f"\n⚠️  CYCLES DETECTED! Review the report for details.")
    else:
        print(f"\n✅ SUCCESS: No cycles found! Your knowledge graph is valid.")

if __name__ == "__main__":
    main() 