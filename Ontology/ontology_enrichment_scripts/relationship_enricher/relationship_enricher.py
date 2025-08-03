#!/usr/bin/env python3
"""
Mathematics Knowledge Graph Relationship Enricher - Node by Node Approach

This script analyzes each concept against all other concepts to find prerequisite relationships
using OpenAI's GPT-4.1-mini model with its large context window.
"""

import pandas as pd
import openai
import uuid
import time
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OpenAI_API_KEY not found in .env file.")

client = openai.OpenAI(api_key=api_key)

# File paths - Updated to use Ontology directory
ONTOLOGY_DIR = "../../"  # Path to Ontology directory from relationship_enricher folder
ARCHIVE_DIR = os.path.join(ONTOLOGY_DIR, "ontology_archive")

# Input files from Ontology directory
CONCEPTS_FILE = os.path.join(ONTOLOGY_DIR, "concepts.csv")
RELATIONSHIPS_FILE = os.path.join(ONTOLOGY_DIR, "relationships.csv")

# Output file to Ontology directory
OUTPUT_FILE = os.path.join(ONTOLOGY_DIR, "relationships.csv")

def archive_existing_files():
    """Archive existing knowledge graph files before processing."""
    try:
        from archive_manager import archive_existing_files as archive_files, ensure_archive_directory
        
        # Ensure archive directory exists
        ensure_archive_directory(ARCHIVE_DIR)
        
        # Archive existing files
        archive_files(ONTOLOGY_DIR, ARCHIVE_DIR)
        
    except ImportError:
        print("Warning: archive_manager not found, skipping archiving")
    except Exception as e:
        print(f"Warning: Error during archiving: {e}")

def load_data():
    """Load concepts and existing relationships."""
    # Check if the expected files exist, if not try alternative names
    concepts_file = CONCEPTS_FILE
    relationships_file = RELATIONSHIPS_FILE
    
    if not os.path.exists(concepts_file):
        # Try to find concept files with different names
        import glob
        concept_files = glob.glob(os.path.join(ONTOLOGY_DIR, "*concepts*.csv"))
        if concept_files:
            concepts_file = concept_files[0]
            print(f"Using concept file: {os.path.basename(concepts_file)}")
        else:
            raise FileNotFoundError(f"No concept files found in {ONTOLOGY_DIR}")
    
    if not os.path.exists(relationships_file):
        # Try to find relationship files with different names
        import glob
        relationship_files = glob.glob(os.path.join(ONTOLOGY_DIR, "*relationships*.csv"))
        if relationship_files:
            relationships_file = relationship_files[0]
            print(f"Using relationship file: {os.path.basename(relationships_file)}")
        else:
            raise FileNotFoundError(f"No relationship files found in {ONTOLOGY_DIR}")
    
    concepts = pd.read_csv(concepts_file)
    relationships = pd.read_csv(relationships_file)
    
    # Track existing pairs to avoid duplicates
    existing_pairs = set(zip(relationships['prerequisite_id'], relationships['dependent_id']))
    
    return concepts, relationships, existing_pairs

def create_node_analysis_prompt(target_concept, all_concepts, existing_examples):
    """Create a prompt to analyze one concept against all others."""
    
    prompt = f"""You are a mathematics education expert analyzing prerequisite relationships for the concept: "{target_concept['name']}"

A prerequisite relationship exists when understanding concept A significantly helps in learning concept B. Consider:
1. Does concept A provide fundamental skills or knowledge that B builds upon?
2. Would learning B be much more difficult without first understanding A?
3. Are there mathematical operations, definitions, or principles from A that B directly uses?

Here are examples of existing prerequisite relationships:
"""
    
    for _, rel in existing_examples.iterrows():
        prompt += f"'{rel['prerequisite_name']}' → '{rel['dependent_name']}': {rel['explanation']}\n\n"
    
    prompt += f"\nNow analyze the target concept against all other concepts:\n\n"
    prompt += f"TARGET CONCEPT: {target_concept['name']}\n"
    prompt += f"Description: {target_concept['explanation']}\n"
    prompt += f"Strand: {target_concept['strand']}\n\n"
    
    prompt += "OTHER CONCEPTS TO COMPARE AGAINST:\n"
    for _, concept in all_concepts.iterrows():
        if concept['id'] != target_concept['id']:
            prompt += f"- {concept['name']}: {concept['explanation']} (Strand: {concept['strand']})\n"
    
    prompt += f"""
For each concept pair, determine if there's a prerequisite relationship. Consider both directions:
1. Is the target concept a prerequisite for the other concept?
2. Is the other concept a prerequisite for the target concept?

Respond with exactly this format:

PREREQUISITE RELATIONSHIPS FOUND:

1. "Target Concept" → "Other Concept": [Brief explanation of why this is a prerequisite relationship]
2. "Other Concept" → "Target Concept": [Brief explanation of why this is a prerequisite relationship]
3. [Continue for all relationships found...]

If no prerequisite relationships exist, respond with: "No prerequisite relationships found."

Only include relationships where there is a clear, significant prerequisite dependency."""
    
    return prompt

def parse_node_response(response, target_concept, all_concepts, existing_pairs):
    """Parse the AI response to extract new relationships."""
    new_relationships = []
    
    if "No prerequisite relationships found" in response:
        return new_relationships
    
    try:
        # Extract relationships from the response
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if '→' in line and line[0].isdigit():
                # Parse relationship line
                parts = line.split('→')
                if len(parts) == 2:
                    prereq_name = parts[0].split('"')[1] if '"' in parts[0] else parts[0].split(':')[1].strip()
                    dep_name = parts[1].split('"')[1] if '"' in parts[1] else parts[1].split(':')[0].strip()
                    explanation = parts[1].split(':')[1].strip() if ':' in parts[1] else ""
                    
                    # Find concept IDs
                    prereq_concept = all_concepts[all_concepts['name'] == prereq_name]
                    dep_concept = all_concepts[all_concepts['name'] == dep_name]
                    
                    if not prereq_concept.empty and not dep_concept.empty:
                        prereq_id = prereq_concept.iloc[0]['id']
                        dep_id = dep_concept.iloc[0]['id']
                        
                        # Check if this relationship doesn't already exist
                        if (prereq_id, dep_id) not in existing_pairs:
                            new_rel = {
                                'id': str(uuid.uuid4()),
                                'prerequisite_id': prereq_id,
                                'dependent_id': dep_id,
                                'prerequisite_name': prereq_name,
                                'dependent_name': dep_name,
                                'explanation': explanation,
                                'source': f'AI_node_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
                            }
                            new_relationships.append(new_rel)
                            existing_pairs.add((prereq_id, dep_id))
    
    except Exception as e:
        print(f"Error parsing response: {e}")
    
    return new_relationships

def analyze_concept_node(target_concept, all_concepts, existing_pairs, existing_examples):
    """Analyze one concept against all others."""
    try:
        prompt = create_node_analysis_prompt(target_concept, all_concepts, existing_examples)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a mathematics education expert specializing in prerequisite relationships between mathematical concepts."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=8000
        )
        
        response_text = response.choices[0].message.content
        new_relationships = parse_node_response(response_text, target_concept, all_concepts, existing_pairs)
        
        return new_relationships
        
    except Exception as e:
        print(f"Error analyzing concept {target_concept['name']}: {e}")
        return []

def save_relationships(new_relationships, output_file, existing_relationships):
    """Save new relationships to output file."""
    if new_relationships:
        new_df = pd.DataFrame(new_relationships)
        if os.path.exists(output_file):
            out_df = pd.read_csv(output_file)
            out_df = pd.concat([out_df, new_df], ignore_index=True)
        else:
            out_df = pd.concat([existing_relationships, new_df], ignore_index=True)
        out_df.to_csv(output_file, index=False)
        print(f"Saved {len(new_relationships)} new relationships to {output_file}")

def main():
    """Main function to run the node-by-node analysis."""
    print("Starting Relationship Enricher...")
    print("=" * 60)
    
    # Archive existing files before processing
    print("Archiving existing knowledge graph files...")
    archive_existing_files()
    
    print("Loading data...")
    concepts, relationships, existing_pairs = load_data()
    
    # Ensure Ontology directory exists for output
    os.makedirs(ONTOLOGY_DIR, exist_ok=True)
    
    # Get examples for context
    existing_examples = relationships.head(5)
    
    total_new_relationships = 0
    total_concepts = len(concepts)
    
    print(f"Starting node-by-node analysis of {total_concepts} concepts...")
    print(f"Found {len(existing_pairs)} existing relationships")
    
    for idx, concept in concepts.iterrows():
        print(f"\nAnalyzing concept {idx+1}/{total_concepts}: {concept['name']}")
        
        # Analyze this concept against all others
        new_relationships = analyze_concept_node(concept, concepts, existing_pairs, existing_examples)
        
        if new_relationships:
            print(f"Found {len(new_relationships)} new relationships")
            save_relationships(new_relationships, OUTPUT_FILE, relationships)
            total_new_relationships += len(new_relationships)
        else:
            print("No new relationships found")
        
        # Small delay to respect rate limits
        time.sleep(1)
    
    print(f"\nAnalysis complete!")
    print(f"Total new relationships found: {total_new_relationships}")
    print(f"Output saved to: {OUTPUT_FILE}")
    print(f"Files archived to: {ARCHIVE_DIR}")

if __name__ == "__main__":
    main() 