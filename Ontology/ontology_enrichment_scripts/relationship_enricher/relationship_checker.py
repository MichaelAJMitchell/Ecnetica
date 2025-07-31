#!/usr/bin/env python3
"""
Mathematics Knowledge Graph Relationship Checker

This script analyzes relationships to detect prerequisite loops (circular dependencies)
that could cause issues in the knowledge graph structure.
"""

import pandas as pd
import networkx as nx
from collections import defaultdict, deque
import os
from datetime import datetime
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

def find_cycles(graph):
    """Find all cycles in the directed graph."""
    try:
        # Find all simple cycles
        cycles = list(nx.simple_cycles(graph))
        return cycles
    except nx.NetworkXNoCycle:
        return []

def find_cycles_dfs(graph):
    """Find cycles using DFS approach for more detailed analysis."""
    cycles = []
    visited = set()
    rec_stack = set()
    
    def dfs(node, path):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        
        for neighbor in graph.successors(node):
            if neighbor not in visited:
                if dfs(neighbor, path):
                    return True
            elif neighbor in rec_stack:
                # Found a cycle
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                cycles.append(cycle)
                return True
        
        rec_stack.remove(node)
        path.pop()
        return False
    
    for node in graph.nodes():
        if node not in visited:
            dfs(node, [])
    
    return cycles

def analyze_cycles(cycles, concepts, relationships):
    """Analyze cycles and provide detailed information."""
    cycle_details = []
    
    for i, cycle in enumerate(cycles):
        cycle_info = {
            'cycle_id': i + 1,
            'cycle_length': len(cycle),
            'cycle_nodes': cycle,
            'cycle_concepts': [],
            'cycle_relationships': [],
            'cycle_explanations': []
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
                cycle_info['cycle_explanations'].append(rel_row['explanation'])
        
        cycle_details.append(cycle_info)
    
    return cycle_details

def find_long_paths(graph, max_length=10):
    """Find long prerequisite chains that might indicate potential issues."""
    long_paths = []
    
    # Find all pairs of nodes
    nodes = list(graph.nodes())
    
    for i, start in enumerate(nodes):
        for end in nodes[i+1:]:
            try:
                # Find shortest path from start to end
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

def generate_reports(cycle_details, long_paths, concepts, relationships):
    """Generate detailed reports about loops and issues."""
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Summary report
    summary_file = f"{OUTPUT_DIR}/summary_report_{timestamp}.txt"
    with open(summary_file, 'w') as f:
        f.write("MATHEMATICS KNOWLEDGE GRAPH - PREREQUISITE LOOP ANALYSIS\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Concepts: {len(concepts)}\n")
        f.write(f"Total Relationships: {len(relationships)}\n")
        f.write(f"Cycles Found: {len(cycle_details)}\n")
        f.write(f"Long Paths (>10): {len(long_paths)}\n\n")
        
        if cycle_details:
            f.write("CRITICAL ISSUES FOUND:\n")
            f.write("-" * 30 + "\n")
            f.write(f"⚠️  Found {len(cycle_details)} prerequisite cycles!\n")
            f.write("These create circular dependencies that break the learning sequence.\n\n")
        else:
            f.write("✅ NO CYCLES FOUND - Graph structure is valid!\n\n")
    
    # Detailed cycles report
    if cycle_details:
        cycles_file = f"{OUTPUT_DIR}/cycles_detailed_{timestamp}.txt"
        with open(cycles_file, 'w') as f:
            f.write("DETAILED CYCLE ANALYSIS\n")
            f.write("=" * 30 + "\n\n")
            
            for cycle_info in cycle_details:
                f.write(f"CYCLE {cycle_info['cycle_id']} (Length: {cycle_info['cycle_length']})\n")
                f.write("-" * 40 + "\n")
                
                # Show cycle as a chain
                cycle_chain = " → ".join(cycle_info['cycle_concepts'])
                f.write(f"Cycle: {cycle_chain} → {cycle_info['cycle_concepts'][0]}\n\n")
                
                f.write("Relationships in this cycle:\n")
                for rel in cycle_info['cycle_relationships']:
                    f.write(f"  • {rel['prerequisite']} → {rel['dependent']}\n")
                    f.write(f"    Reason: {rel['explanation']}\n\n")
                
                f.write("RECOMMENDATION: Review these relationships and remove at least one to break the cycle.\n")
                f.write("\n" + "=" * 50 + "\n\n")
    
    # Long paths report
    if long_paths:
        paths_file = f"{OUTPUT_DIR}/long_paths_{timestamp}.txt"
        with open(paths_file, 'w') as f:
            f.write("LONG PREREQUISITE CHAINS (>10 steps)\n")
            f.write("=" * 40 + "\n\n")
            f.write("These long chains might indicate missing intermediate concepts:\n\n")
            
            for path_info in long_paths:
                start_concept = concepts[concepts['id'] == path_info['start']].iloc[0]['name']
                end_concept = concepts[concepts['id'] == path_info['end']].iloc[0]['name']
                
                f.write(f"Chain: {start_concept} → ... → {end_concept}\n")
                f.write(f"Length: {path_info['path_length']} steps\n")
                f.write(f"Path: {' → '.join([concepts[concepts['id'] == node_id].iloc[0]['name'] for node_id in path_info['path']])}\n\n")
    
    # CSV export of cycles
    if cycle_details:
        cycles_csv = f"{OUTPUT_DIR}/cycles_export_{timestamp}.csv"
        cycle_data = []
        for cycle_info in cycle_details:
            for rel in cycle_info['cycle_relationships']:
                cycle_data.append({
                    'cycle_id': cycle_info['cycle_id'],
                    'cycle_length': cycle_info['cycle_length'],
                    'prerequisite': rel['prerequisite'],
                    'dependent': rel['dependent'],
                    'explanation': rel['explanation']
                })
        
        cycle_df = pd.DataFrame(cycle_data)
        cycle_df.to_csv(cycles_csv, index=False)
    
    return summary_file, cycles_file if cycle_details else None

def main():
    """Main function to run the relationship checker."""
    print("Mathematics Knowledge Graph Relationship Checker")
    print("=" * 50)
    
    # Load data
    concepts, relationships = load_data()
    if concepts is None:
        return
    
    # Build graph
    print("\nBuilding prerequisite graph...")
    graph = build_graph(relationships)
    
    # Find cycles
    print("\nSearching for prerequisite cycles...")
    cycles = find_cycles(graph)
    
    if cycles:
        print(f"⚠️  Found {len(cycles)} cycles!")
    else:
        print("✅ No cycles found - graph structure is valid!")
    
    # Analyze cycles
    cycle_details = analyze_cycles(cycles, concepts, relationships)
    
    # Find long paths
    print("\nAnalyzing prerequisite chain lengths...")
    long_paths = find_long_paths(graph, max_length=10)
    
    if long_paths:
        print(f"Found {len(long_paths)} long prerequisite chains (>10 steps)")
    
    # Generate reports
    print("\nGenerating reports...")
    summary_file, cycles_file = generate_reports(cycle_details, long_paths, concepts, relationships)
    
    print(f"\nReports saved to {OUTPUT_DIR}/")
    print(f"Summary: {os.path.basename(summary_file)}")
    if cycles_file:
        print(f"Cycles: {os.path.basename(cycles_file)}")
    
    # Print summary to console
    print(f"\nSUMMARY:")
    print(f"  • Total concepts: {len(concepts)}")
    print(f"  • Total relationships: {len(relationships)}")
    print(f"  • Cycles found: {len(cycles)}")
    print(f"  • Long chains (>10): {len(long_paths)}")
    
    if cycles:
        print(f"\n⚠️  CRITICAL: Found {len(cycles)} prerequisite cycles!")
        print("   These create circular dependencies that break learning sequences.")
        print("   Review the detailed reports and remove problematic relationships.")
    else:
        print(f"\n✅ SUCCESS: No cycles found! Your knowledge graph structure is valid.")

if __name__ == "__main__":
    main() 