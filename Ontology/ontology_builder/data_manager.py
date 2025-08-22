"""
Data Manager - Handles JSON output and archiving

This module manages all extracted data, providing storage, organization, and
output functionality. It handles the conversion to the required JSON format
and implements a modular archiving system to preserve previous results.
"""

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
        pass
    
    def add_relationships(self, relationships: list):
        """
        Add new relationships to the internal data structure.
        
        This method processes newly extracted relationships, ensuring they reference
        valid concepts and don't create duplicate connections. It validates the
        relationship structure and maintains referential integrity.
        
        Args:
            relationships: List of relationship dictionaries from the LLM extraction
            
        Each relationship should contain:
            - prerequisite_id: ID of the prerequisite concept
            - dependent_id: ID of the dependent concept
            - relationship_type: Nature of the relationship
            - strength: Confidence level (0.0 to 1.0)
        """
        pass
    
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
        pass
    
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
        pass 