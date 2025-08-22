"""
Data Manager - Handles JSON output and archiving

This module manages all extracted data, providing storage, organization, and
output functionality. It handles the conversion to the required JSON format
and implements a modular archiving system to preserve previous results.
"""

import os
import json
import shutil
from datetime import datetime
from typing import List, Dict, Any

class DataManager:
    """
    Manages the storage, organization, and output of extracted concepts and relationships.
    
    This class serves as the data hub, collecting all extracted information and
    converting it to the required JSON format that matches your existing graph-data.json
    structure. It also handles archiving to prevent data loss during updates.
    """
    
    def __init__(self):
        """
        Initialize the data manager with empty data structures.
        
        The data manager maintains two main collections:
        - concepts: All extracted mathematical concepts with detailed metadata
        - relationships: All identified relationships between concepts
        
        These are built up during processing and then converted to the final JSON format.
        """
        self.concepts = []
        self.relationships = []
    
    def add_concepts(self, concepts: list):
        """
        Add new concepts to the internal data structure.
        
        This method processes newly extracted concepts, ensuring they don't duplicate
        existing ones and maintaining consistent data structure. It handles the
        conversion from LLM output format to internal storage format.
        
        Args:
            concepts: List of concept dictionaries from the LLM extraction
            
        Each concept should contain:
            - name: The concept name
            - explanation: Brief description
            - broader_concept: Higher-level category
            - strand: Mathematical strand
            - grade_level: Educational level
            - difficulty: Complexity assessment
        """
        for concept in concepts:
            # Validate concept structure before adding
            if not self._validate_concept_structure(concept):
                print(f"Skipping invalid concept: {concept}")
                continue
                
            if not self._is_duplicate_concept(concept):
                # Generate unique ID
                concept['id'] = self._generate_id()
                self.concepts.append(concept)
    
    def add_relationships(self, relationships: list):
        """
        Add new relationships to the internal data structure.
        
        This method processes newly extracted relationships, ensuring they reference
        valid concepts and don't create duplicate connections. It validates the
        relationship structure and maintains referential integrity.
        
        Args:
            relationships: List of relationship dictionaries from the LLM extraction
            
        Each relationship should contain:
            - prerequisite_name: ID of the prerequisite concept
            - dependent_name: ID of the dependent concept
            - relationship_type: Nature of the relationship
            - strength: Confidence level (0.0 to 1.0)
        """
        for relationship in relationships:
            # Validate relationship structure before adding
            if not self._validate_relationship_structure(relationship):
                print(f"Skipping invalid relationship: {relationship}")
                continue
                
            # Check for duplicates by prerequisite->dependent pair
            if not self._is_duplicate_relationship(relationship):
                # Generate unique ID
                relationship['id'] = self._generate_id()
                self.relationships.append(relationship)
    
    def get_concepts(self) -> list:
        """Get all concepts for context in prompts."""
        return self.concepts
    
    def get_relationships(self) -> list:
        """Get all relationships for context in prompts."""
        return self.relationships
    
    def save_to_json(self, output_file: str):
        """
        Save all extracted data to JSON format matching graph-data.json structure.
        
        This method converts the internal data structures to the exact JSON format
        expected by your graph visualization system. It creates the nodes and edges
        structure with all required fields and metadata.
        
        Args:
            output_file: Path where the JSON file should be saved
            
        The output JSON will have this structure:
            {
                "nodes": [
                    {
                        "id": "uuid",
                        "label": "concept_name",
                        "group": "strand",
                        "title": "explanation",
                        "broader_concept": "category",
                        "grade_level": "level",
                        "difficulty": "complexity"
                    }
                ],
                "edges": [
                    {
                        "from": "prerequisite_id",
                        "to": "dependent_id",
                        "strength": "relationship_strength"
                    }
                ]
            }
        """
        # Archive previous data if it exists
        self.archive_previous_data(output_file)
        
        # Convert concepts to nodes format
        nodes = []
        for concept in self.concepts:
            node = {
                'id': concept['id'],
                'label': concept['name'],
                'group': concept.get('strand', 'Unknown'),
                'title': concept.get('explanation', ''),
                'broader_concept': concept.get('broader_concept', ''),
                'grade_level': concept.get('grade_level', ''),
                'difficulty': concept.get('difficulty', '')
            }
            nodes.append(node)
        
        # Convert relationships to edges format using IDs directly
        edges = []
        for relationship in self.relationships:
            edge = {
                'from': relationship.get('prerequisite_concept_id', ''),  # Direct ID reference
                'to': relationship.get('dependent_concept_id', ''),       # Direct ID reference
                'strength': relationship.get('strength', 0.5)
            }
            edges.append(edge)
        
        # Create final JSON structure
        output_data = {
            'nodes': nodes,
            'edges': edges
        }
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(nodes)} concepts and {len(edges)} relationships to {output_file}")
    
    def archive_previous_data(self, output_file: str):
        """
        Archive previous data before saving new results.
        
        This method creates a timestamped backup of any existing output file
        before overwriting it with new data. This prevents data loss and allows
        for comparison between different extraction runs.
        
        Args:
            output_file: Path to the file that will be archived
            
        The archiving process:
        1. Checks if the output file exists
        2. Creates a timestamped backup folder if needed
        3. Moves the existing file to the archive with a timestamp
        4. Ensures the new extraction can proceed safely
        """
        if os.path.exists(output_file):
            # Create timestamp for archive name
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = os.path.basename(output_file)
            file_base = os.path.splitext(file_name)[0]
            archive_name = f"{file_base}_{timestamp}.json"
            
            # Create archive directory if it doesn't exist
            archive_dir = os.path.join(os.path.dirname(output_file), "archive")
            os.makedirs(archive_dir, exist_ok=True)
            
            # Move file to archive
            archive_path = os.path.join(archive_dir, archive_name)
            shutil.move(output_file, archive_path)
            print(f"Archived previous data to {archive_path}")
    
    def _generate_id(self) -> str:
        """Generate a unique ID for concepts and relationships."""
        import uuid
        return str(uuid.uuid4())
    
    def _is_duplicate_concept(self, concept: dict) -> bool:
        """Check if a concept is a duplicate by name."""
        concept_name = concept.get('name', '').lower().strip()
        for existing in self.concepts:
            if existing.get('name', '').lower().strip() == concept_name:
                return True
        return False
    
    def _is_duplicate_relationship(self, relationship: dict) -> bool:
        prereq = relationship.get('prerequisite_concept_id', '').lower().strip()
        dependent = relationship.get('dependent_concept_id', '').lower().strip()
        for existing in self.relationships:
            existing_prereq = existing.get('prerequisite_concept_id', '').lower().strip()
            existing_dependent = existing.get('dependent_concept_id', '').lower().strip()
            if existing_prereq == prereq and existing_dependent == dependent:
                return True
        return False

    def _validate_concept_structure(self, concept: dict) -> bool:
        """Validate that a concept has the required fields."""
        required_fields = ['name']
        for field in required_fields:
            if not concept.get(field):
                return False
        return True

    def _validate_relationship_structure(self, relationship: dict) -> bool:
        """Validate that a relationship has the required fields."""
        required_fields = ['prerequisite_concept_id', 'dependent_concept_id']
        for field in required_fields:
            if not relationship.get(field):
                return False
        return True 