#!/usr/bin/env python3
"""
Process the ontology CSV files into JSON format for the knowledge graph visualization.
This script reads the concepts and relationships CSV files and converts them to a format
suitable for the vis.js network visualization.
"""

import pandas as pd
import json
import os

def find_file_by_pattern(directory, pattern):
    """Find a file in directory that contains the pattern in its name."""
    if not os.path.exists(directory):
        return None
    
    for filename in os.listdir(directory):
        if pattern.lower() in filename.lower() and filename.endswith('.csv'):
            return os.path.join(directory, filename)
    return None

def process_ontology_data():
    """Process the ontology CSV files and create JSON data for visualization."""
    
    # Find CSV files by pattern
    concepts_file = find_file_by_pattern('Ontology', 'concepts')
    relationships_file = find_file_by_pattern('Ontology', 'relationships')
    
    if not concepts_file:
        print("Error: No concepts CSV file found in Ontology directory")
        return
    
    if not relationships_file:
        print("Error: No relationships CSV file found in Ontology directory")
        return
    
    print(f"Found concepts file: {concepts_file}")
    print(f"Found relationships file: {relationships_file}")
    
    # Load the data
    concepts_df = pd.read_csv(concepts_file)
    relationships_df = pd.read_csv(relationships_file)
    
    print(f"Loaded {len(concepts_df)} concepts and {len(relationships_df)} relationships")
    
    # Create nodes from concepts
    nodes = []
    for _, concept in concepts_df.iterrows():
        # Clean up the strand name
        strand = concept['strand'] if pd.notna(concept['strand']) else 'Unknown'
        
        # Create node object
        node = {
            'id': concept['id'],
            'label': concept['name'],
            'group': strand,
            'title': concept['explanation'] if pd.notna(concept['explanation']) else concept['name']
        }
        nodes.append(node)
    
    # Create edges from relationships
    edges = []
    for _, relationship in relationships_df.iterrows():
        # Create edge object
        edge = {
            'from': relationship['prerequisite_id'],
            'to': relationship['dependent_id'],
            'title': relationship['explanation'] if pd.notna(relationship['explanation']) else 'Prerequisite relationship'
        }
        edges.append(edge)
    
    # Create the complete graph data
    graph_data = {
        'nodes': nodes,
        'edges': edges
    }
    
    # Save to JSON file
    output_file = '_static/graph-data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, indent=2, ensure_ascii=False)
    
    print(f"Graph data saved to {output_file}")
    print(f"Nodes: {len(nodes)}")
    print(f"Edges: {len(edges)}")
    
    # Print some statistics
    strands = set(node['group'] for node in nodes)
    print(f"Strands found: {sorted(strands)}")
    
    return graph_data

def create_simplified_data():
    """Create a simplified version for testing with fewer nodes."""
    
    # Read the CSV files
    concepts_file = find_file_by_pattern('Ontology', 'concepts')
    relationships_file = find_file_by_pattern('Ontology', 'relationships')
    
    if not concepts_file:
        print("Error: No concepts CSV file found in Ontology directory")
        return
    
    if not relationships_file:
        print("Error: No relationships CSV file found in Ontology directory")
        return
    
    # Load the data
    concepts_df = pd.read_csv(concepts_file)
    relationships_df = pd.read_csv(relationships_file)
    
    # Select a subset of concepts (first 50 for performance)
    sample_concepts = concepts_df.head(50)
    
    # Get relationships that involve only the sampled concepts
    concept_ids = set(sample_concepts['id'])
    sample_relationships = relationships_df[
        (relationships_df['prerequisite_id'].isin(concept_ids)) & 
        (relationships_df['dependent_id'].isin(concept_ids))
    ]
    
    # Create nodes
    nodes = []
    for _, concept in sample_concepts.iterrows():
        strand = concept['strand'] if pd.notna(concept['strand']) else 'Unknown'
        node = {
            'id': concept['id'],
            'label': concept['name'][:30] + '...' if len(concept['name']) > 30 else concept['name'],
            'group': strand,
            'title': concept['explanation'] if pd.notna(concept['explanation']) else concept['name']
        }
        nodes.append(node)
    
    # Create edges
    edges = []
    for _, relationship in sample_relationships.iterrows():
        edge = {
            'from': relationship['prerequisite_id'],
            'to': relationship['dependent_id'],
            'title': relationship['explanation'] if pd.notna(relationship['explanation']) else 'Prerequisite relationship'
        }
        edges.append(edge)
    
    # Create the simplified graph data
    graph_data = {
        'nodes': nodes,
        'edges': edges
    }
    
    # Save to JSON file
    output_file = '_static/graph-data-simplified.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, indent=2, ensure_ascii=False)
    
    print(f"Simplified graph data saved to {output_file}")
    print(f"Nodes: {len(nodes)}")
    print(f"Edges: {len(edges)}")
    
    return graph_data

if __name__ == "__main__":
    print("Processing ontology data...")
    
    # Create both full and simplified versions
    print("\nCreating full graph data...")
    process_ontology_data()
    
    print("\nCreating simplified graph data...")
    create_simplified_data()
    
    print("\nDone! You can now use the JSON files in your visualization.") 