#!/usr/bin/env python3
"""
Convert graph-data.json to CSV format.
Creates separate CSV files for concepts and relationships.
"""

import json
import csv
import sys
from pathlib import Path


def convert_concepts_to_csv(json_data, output_file):
    """Convert concepts array to CSV."""
    concepts = json_data.get("concepts", [])
    
    if not concepts:
        print("No concepts found in JSON file.")
        return
    
    # Get all unique field names from all concepts
    fieldnames = set()
    for concept in concepts:
        fieldnames.update(concept.keys())
    
    # Sort fieldnames for consistent column order
    fieldnames = sorted(fieldnames)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for concept in concepts:
            # Ensure all fields are present (fill missing with empty string)
            row = {field: concept.get(field, '') for field in fieldnames}
            writer.writerow(row)
    
    print(f"Converted {len(concepts)} concepts to {output_file}")


def convert_relationships_to_csv(json_data, output_file):
    """Convert relationships array to CSV."""
    relationships = json_data.get("relationships", [])
    
    if not relationships:
        print("No relationships found in JSON file.")
        return
    
    # Get all unique field names from all relationships
    fieldnames = set()
    for relationship in relationships:
        fieldnames.update(relationship.keys())
    
    # Sort fieldnames for consistent column order
    fieldnames = sorted(fieldnames)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for relationship in relationships:
            # Ensure all fields are present (fill missing with empty string)
            row = {field: relationship.get(field, '') for field in fieldnames}
            writer.writerow(row)
    
    print(f"Converted {len(relationships)} relationships to {output_file}")


def main():
    # Default input and output files
    input_file = Path("graph-data.json")
    concepts_output = Path("graph-data-concepts.csv")
    relationships_output = Path("graph-data-relationships.csv")
    
    # Allow command-line arguments
    if len(sys.argv) > 1:
        input_file = Path(sys.argv[1])
    if len(sys.argv) > 2:
        concepts_output = Path(sys.argv[2])
    if len(sys.argv) > 3:
        relationships_output = Path(sys.argv[3])
    
    # Check if input file exists
    if not input_file.exists():
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    
    # Read JSON file
    print(f"Reading {input_file}...")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {input_file}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading {input_file}: {e}")
        sys.exit(1)
    
    # Convert concepts
    convert_concepts_to_csv(json_data, concepts_output)
    
    # Convert relationships
    convert_relationships_to_csv(json_data, relationships_output)
    
    print("\nConversion complete!")


if __name__ == "__main__":
    main()


