#!/usr/bin/env python3
"""
Lightweight Knowledge Graph Data Processor

This script creates a minimal JSON format from ontology CSV files and creates a minimal JSON format for 
a lightweight canvas-based knowledge graph visualization.
"""

import pandas as pd
import json
import random
import os

def create_lightweight_graph(max_nodes=None):
    """Create a minimal graph from ontology data"""
    
    print("Reading ontology data...")
    
    # Read CSV files
    concepts_file = 'Ontology/concepts_06_07_better.csv'
    relationships_file = 'Ontology/relationships_enriched_07_07.csv'
    
    if not os.path.exists(concepts_file):
        print(f"Error: {concepts_file} not found")
        return None
        
    if not os.path.exists(relationships_file):
        print(f"Error: {relationships_file} not found")
        return None
    
    concepts = pd.read_csv(concepts_file)
    relationships = pd.read_csv(relationships_file)
    
    print(f"Loaded {len(concepts)} concepts and {len(relationships)} relationships")
    
    # Remove node limit: use all concepts
    sample_concepts = concepts
    print(f"Using all {len(sample_concepts)} concepts (no node limit)")
    
    concept_ids = set(sample_concepts['id'])
    
    # Filter relationships to only include sampled concepts
    sample_relationships = relationships[
        (relationships['prerequisite_id'].isin(concept_ids)) & 
        (relationships['dependent_id'].isin(concept_ids))
    ]
    
    print(f"Filtered to {len(sample_relationships)} relationships")
    
    # Create minimal nodes with simple positioning
    nodes = []
    strand_groups = {}
    
    for i, concept in sample_concepts.iterrows():
        strand = concept['strand'] if pd.notna(concept['strand']) else 'Other'
        
        # Group nodes by strand for better positioning
        if strand not in strand_groups:
            strand_groups[strand] = []
        strand_groups[strand].append(concept['id'])
        
        nodes.append({
            'id': concept['id'],
            'name': concept['name'][:30] + '...' if len(concept['name']) > 30 else concept['name'],
            'strand': strand,
            'full_name': concept['name'],
            'explanation': concept['explanation'] if pd.notna(concept['explanation']) else concept['name']
        })
    
    # Position nodes by strand groups
    canvas_width = 800
    canvas_height = 600
    margin = 50
    
    strands = list(strand_groups.keys())
    nodes_per_row = 3
    rows = (len(strands) + nodes_per_row - 1) // nodes_per_row
    
    for i, strand in enumerate(strands):
        row = i // nodes_per_row
        col = i % nodes_per_row
        
        # Calculate base position for this strand group
        base_x = margin + col * (canvas_width - 2 * margin) // nodes_per_row
        base_y = margin + row * (canvas_height - 2 * margin) // rows
        
        # Position nodes in this strand
        strand_nodes = strand_groups[strand]
        for j, node_id in enumerate(strand_nodes):
            # Find the node and update its position
            for node in nodes:
                if node['id'] == node_id:
                    # Add some randomness within the strand area
                    node['x'] = base_x + random.randint(-50, 50)
                    node['y'] = base_y + random.randint(-30, 30)
                    break
    
    # Create minimal edges
    edges = []
    for _, rel in sample_relationships.iterrows():
        edges.append({
            'from': rel['prerequisite_id'],
            'to': rel['dependent_id']
        })
    
    # Create the final graph data
    graph_data = {
        'nodes': nodes,
        'edges': edges,
        'metadata': {
            'total_nodes': len(nodes),
            'total_edges': len(edges),
            'strands': list(strand_groups.keys()),
            'max_nodes': None
        }
    }
    
    return graph_data

def save_lightweight_graph(graph_data, output_file='_static/lightweight-graph.json'):
    """Save the graph data to JSON file"""
    
    # Ensure _static directory exists
    os.makedirs('_static', exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, indent=2, ensure_ascii=False)
    
    print(f"Lightweight graph data saved to {output_file}")
    print(f"Nodes: {len(graph_data['nodes'])}")
    print(f"Edges: {len(graph_data['edges'])}")
    print(f"Strands: {graph_data['metadata']['strands']}")

def main():
    """Main function to process and save the lightweight graph"""
    
    print("Creating lightweight knowledge graph...")
    
    # Create graph with 100 nodes for good performance
    graph_data = create_lightweight_graph(max_nodes=100)
    
    if graph_data:
        save_lightweight_graph(graph_data)
        print("✓ Lightweight graph created successfully!")
    else:
        print("✗ Failed to create lightweight graph")

if __name__ == "__main__":
    main() 