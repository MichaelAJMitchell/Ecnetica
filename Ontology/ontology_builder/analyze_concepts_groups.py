#!/usr/bin/env python3
"""
Program to analyze nodes in graph-data.json and extract broader concepts and groups information.
Creates a comprehensive table showing the relationship between broader concepts and groups.
"""

import json
import csv
from collections import defaultdict, Counter
import os

def load_graph_data(file_path):
    """Load the graph data from JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
        return None

def analyze_concepts_and_groups(data):
    """Analyze the nodes to extract broader concepts and groups information."""
    if not data or 'nodes' not in data:
        print("Error: No nodes found in the data.")
        return None
    
    nodes = data['nodes']
    
    # Initialize data structures
    concept_group_mapping = defaultdict(set)  # broader_concept -> set of groups
    group_concept_mapping = defaultdict(set)   # group -> set of broader_concepts
    concept_counts = Counter()
    group_counts = Counter()
    node_details = []
    
    # Process each node
    for node in nodes:
        broader_concept = node.get('broader_concept', 'N/A')
        group = node.get('group', 'N/A')
        label = node.get('label', 'N/A')
        node_id = node.get('id', 'N/A')
        
        # Update mappings
        concept_group_mapping[broader_concept].add(group)
        group_concept_mapping[group].add(broader_concept)
        
        # Update counts
        concept_counts[broader_concept] += 1
        group_counts[group] += 1
        
        # Store node details
        node_details.append({
            'id': node_id,
            'label': label,
            'broader_concept': broader_concept,
            'group': group
        })
    
    return {
        'concept_group_mapping': dict(concept_group_mapping),
        'group_concept_mapping': dict(group_concept_mapping),
        'concept_counts': concept_counts,
        'group_counts': group_counts,
        'node_details': node_details,
        'total_nodes': len(nodes)
    }

def create_summary_tables(analysis_data):
    """Create summary tables from the analysis data."""
    
    # Table 1: Broader Concepts Summary
    concepts_summary = []
    for concept, count in analysis_data['concept_counts'].most_common():
        groups = sorted(list(analysis_data['concept_group_mapping'][concept]))
        concepts_summary.append({
            'Broader_Concept': concept,
            'Node_Count': count,
            'Groups': ', '.join(groups),
            'Group_Count': len(groups)
        })
    
    # Table 2: Groups Summary
    groups_summary = []
    for group, count in analysis_data['group_counts'].most_common():
        concepts = sorted(list(analysis_data['group_concept_mapping'][group]))
        groups_summary.append({
            'Group': group,
            'Node_Count': count,
            'Broader_Concepts': ', '.join(concepts),
            'Concept_Count': len(concepts)
        })
    
    # Table 3: Cross-tabulation (Concept-Group Matrix)
    cross_tab = []
    all_concepts = sorted(analysis_data['concept_counts'].keys())
    all_groups = sorted(analysis_data['group_counts'].keys())
    
    for concept in all_concepts:
        row = {'Broader_Concept': concept}
        for group in all_groups:
            # Count nodes that have both this concept and group
            count = sum(1 for node in analysis_data['node_details'] 
                       if node['broader_concept'] == concept and node['group'] == group)
            row[group] = count
        cross_tab.append(row)
    
    return concepts_summary, groups_summary, cross_tab

def save_results(analysis_data, concepts_summary, groups_summary, cross_tab, output_dir):
    """Save all results to files."""
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save detailed node information
    nodes_file = os.path.join(output_dir, 'node_details.csv')
    with open(nodes_file, 'w', newline='', encoding='utf-8') as f:
        if analysis_data['node_details']:
            writer = csv.DictWriter(f, fieldnames=analysis_data['node_details'][0].keys())
            writer.writeheader()
            writer.writerows(analysis_data['node_details'])
    print(f"Node details saved to: {nodes_file}")
    
    # Save concepts summary
    concepts_file = os.path.join(output_dir, 'broader_concepts_summary.csv')
    with open(concepts_file, 'w', newline='', encoding='utf-8') as f:
        if concepts_summary:
            writer = csv.DictWriter(f, fieldnames=concepts_summary[0].keys())
            writer.writeheader()
            writer.writerows(concepts_summary)
    print(f"Broader concepts summary saved to: {concepts_file}")
    
    # Save groups summary
    groups_file = os.path.join(output_dir, 'groups_summary.csv')
    with open(groups_file, 'w', newline='', encoding='utf-8') as f:
        if groups_summary:
            writer = csv.DictWriter(f, fieldnames=groups_summary[0].keys())
            writer.writeheader()
            writer.writerows(groups_summary)
    print(f"Groups summary saved to: {groups_file}")
    
    # Save cross-tabulation
    cross_tab_file = os.path.join(output_dir, 'concept_group_cross_tabulation.csv')
    with open(cross_tab_file, 'w', newline='', encoding='utf-8') as f:
        if cross_tab:
            writer = csv.DictWriter(f, fieldnames=cross_tab[0].keys())
            writer.writeheader()
            writer.writerows(cross_tab)
    print(f"Cross-tabulation saved to: {cross_tab_file}")
    
    # Save comprehensive summary as JSON
    # Convert sets to lists for JSON serialization
    concept_group_mapping_json = {k: list(v) for k, v in analysis_data['concept_group_mapping'].items()}
    group_concept_mapping_json = {k: list(v) for k, v in analysis_data['group_concept_mapping'].items()}
    
    summary_data = {
        'analysis_summary': {
            'total_nodes': analysis_data['total_nodes'],
            'unique_broader_concepts': len(analysis_data['concept_counts']),
            'unique_groups': len(analysis_data['group_counts']),
            'most_common_concept': analysis_data['concept_counts'].most_common(1)[0] if analysis_data['concept_counts'] else None,
            'most_common_group': analysis_data['group_counts'].most_common(1)[0] if analysis_data['group_counts'] else None
        },
        'concept_group_mapping': concept_group_mapping_json,
        'group_concept_mapping': group_concept_mapping_json,
        'concept_counts': dict(analysis_data['concept_counts']),
        'group_counts': dict(analysis_data['group_counts'])
    }
    
    summary_file = os.path.join(output_dir, 'analysis_summary.json')
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
    print(f"Analysis summary saved to: {summary_file}")

def print_summary(analysis_data, concepts_summary, groups_summary):
    """Print a summary of the analysis to console."""
    print("\n" + "="*80)
    print("GRAPH DATA ANALYSIS SUMMARY")
    print("="*80)
    
    print(f"\nTotal Nodes Analyzed: {analysis_data['total_nodes']}")
    print(f"Unique Broader Concepts: {len(analysis_data['concept_counts'])}")
    print(f"Unique Groups: {len(analysis_data['group_counts'])}")
    
    print(f"\nTop 10 Most Common Broader Concepts:")
    print("-" * 50)
    for i, (concept, count) in enumerate(analysis_data['concept_counts'].most_common(10), 1):
        print(f"{i:2d}. {concept:<40} ({count} nodes)")
    
    print(f"\nTop 10 Most Common Groups:")
    print("-" * 50)
    for i, (group, count) in enumerate(analysis_data['group_counts'].most_common(10), 1):
        print(f"{i:2d}. {group:<40} ({count} nodes)")
    
    print(f"\nBroader Concepts with Multiple Groups:")
    print("-" * 50)
    multi_group_concepts = [(concept, groups) for concept, groups in analysis_data['concept_group_mapping'].items() 
                           if len(groups) > 1]
    for concept, groups in sorted(multi_group_concepts, key=lambda x: len(x[1]), reverse=True):
        print(f"{concept:<40} -> {', '.join(sorted(groups))}")

def main():
    """Main function to run the analysis."""
    # File paths
    input_file = '/Users/patrickcurran/Documents/personal_new/Ecnetica/Ontology/ontology_builder/graph-data.json'
    output_dir = '/Users/patrickcurran/Documents/personal_new/Ecnetica/Ontology/ontology_builder'
    
    print("Loading graph data...")
    data = load_graph_data(input_file)
    
    if data is None:
        return
    
    print("Analyzing concepts and groups...")
    analysis_data = analyze_concepts_and_groups(data)
    
    if analysis_data is None:
        return
    
    print("Creating summary tables...")
    concepts_summary, groups_summary, cross_tab = create_summary_tables(analysis_data)
    
    print("Saving results...")
    save_results(analysis_data, concepts_summary, groups_summary, cross_tab, output_dir)
    
    print("Printing summary...")
    print_summary(analysis_data, concepts_summary, groups_summary)
    
    print(f"\nAnalysis complete! Files saved to: {output_dir}")

if __name__ == "__main__":
    main()
