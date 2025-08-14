import os
import pandas as pd
import uuid
from typing import List, Dict, Any, Optional, Tuple
from config import OUTPUT_DIR, CONCEPTS_FILE, RELATIONSHIPS_FILE, ARCHIVE_DIR
from archive_manager import archive_existing_files, ensure_archive_directory

class DataManager:
    """Manages loading, saving, and deduplication of concepts and relationships data."""
    
    def __init__(self):
        self.concepts = []
        self.relationships = []
        self.concept_name_to_id = {}  # For quick lookup
        self.relationship_key_to_id = {}  # For deduplication
        
        # Ensure archive directory exists
        ensure_archive_directory(ARCHIVE_DIR)
        
        # Archive existing files before loading new data
        self._archive_existing_files()
        
        # Create output directory if it doesn't exist
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # Load existing data
        self.load_existing_data()
    
    def _archive_existing_files(self):
        """Archive existing knowledge graph files before processing new data."""
        ontology_dir = OUTPUT_DIR
        archive_dir = ARCHIVE_DIR
        
        if os.path.exists(ontology_dir):
            archive_existing_files(ontology_dir, archive_dir)
    
    def load_existing_data(self):
        """Load existing concepts and relationships from CSV files."""
        # Load concepts
        if os.path.exists(CONCEPTS_FILE):
            try:
                df_concepts = pd.read_csv(CONCEPTS_FILE)
                self.concepts = df_concepts.to_dict('records')
                
                # Build lookup dictionary
                for concept in self.concepts:
                    self.concept_name_to_id[concept['name']] = concept['id']
                
                print(f"Loaded {len(self.concepts)} existing concepts")
            except Exception as e:
                print(f"Error loading concepts file: {str(e)}")
                self.concepts = []
        
        # Load relationships
        if os.path.exists(RELATIONSHIPS_FILE):
            try:
                df_relationships = pd.read_csv(RELATIONSHIPS_FILE)
                self.relationships = df_relationships.to_dict('records')
                
                # Build lookup dictionary for relationships
                for rel in self.relationships:
                    key = f"{rel['prerequisite_name']}->{rel['dependent_name']}"
                    self.relationship_key_to_id[key] = rel['id']
                
                print(f"Loaded {len(self.relationships)} existing relationships")
            except Exception as e:
                print(f"Error loading relationships file: {str(e)}")
                self.relationships = []
    
    def _generate_id(self) -> str:
        """Generate a unique ID for concepts and relationships."""
        return str(uuid.uuid4())
    
    def _normalize_concept_name(self, name: str) -> str:
        """Normalize concept name for comparison."""
        return name.lower().strip()
    
    def _find_concept_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Find a concept by name with flexible matching."""
        normalized_name = self._normalize_concept_name(name)
        
        # First try exact match
        for concept in self.concepts:
            if self._normalize_concept_name(concept['name']) == normalized_name:
                return concept
        
        # If no exact match, try partial matching
        for concept in self.concepts:
            concept_normalized = self._normalize_concept_name(concept['name'])
            if normalized_name in concept_normalized or concept_normalized in normalized_name:
                return concept
        
        return None
    
    def _find_concept_by_semantic_match(self, name: str) -> Optional[Dict[str, Any]]:
        """Find a concept by semantic meaning using OpenAI - single API call for all comparisons."""
        if not self.concepts:
            return None
        
        try:
            from openai_client import OpenAIClient
            client = OpenAIClient()
            
            # Prepare list of existing concepts for comparison
            concept_list = []
            for i, concept in enumerate(self.concepts):
                concept_list.append(f"{i+1}. {concept['name']}: {concept['explanation']}")
            
            concept_text = "\n".join(concept_list)
            
            prompt = f"""You are a mathematical education expert. I have a new concept that might be equivalent to one of the existing concepts below.

NEW CONCEPT: "{name}"

EXISTING CONCEPTS:
{concept_text}

Please identify if the new concept is equivalent to any of the existing concepts. Consider:
- Are they referring to the same mathematical concept?
- Do they represent the same idea or procedure?
- Are they just different ways of expressing the same thing?

If you find an equivalent concept, respond with ONLY the number of the matching concept (e.g., "3").
If no equivalent concept exists, respond with "NONE".

Respond with only the number or "NONE"."""

            messages = [
                {"role": "system", "content": "You are a mathematical education expert."},
                {"role": "user", "content": prompt}
            ]
            
            response = client._make_api_call(
                model=client.models[0],  # Use the first available model
                messages=messages,
                temperature=0.1,
                max_tokens=10
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse the response
            if content.upper() == "NONE":
                return None
            
            try:
                # Try to parse as a number
                match_index = int(content) - 1  # Convert to 0-based index
                if 0 <= match_index < len(self.concepts):
                    matched_concept = self.concepts[match_index]
                    print(f"Found semantic match: '{name}' matches '{matched_concept['name']}'")
                    return matched_concept
                else:
                    print(f"Invalid concept number returned: {content}")
                    return None
            except ValueError:
                print(f"Could not parse response as number: {content}")
                return None
            
        except Exception as e:
            print(f"Error checking concept equivalence: {str(e)}")
            return False
    
    def _is_duplicate_concept(self, concept: Dict[str, Any]) -> Optional[str]:
        """Check if a concept is a duplicate and return existing ID if found."""
        normalized_name = self._normalize_concept_name(concept['name'])
        
        for existing_concept in self.concepts:
            if self._normalize_concept_name(existing_concept['name']) == normalized_name:
                return existing_concept['id']
        
        return None
    
    def _is_duplicate_relationship(self, relationship: Dict[str, Any]) -> Optional[str]:
        """Check if a relationship is a duplicate and return existing ID if found."""
        prereq_name = relationship['prerequisite']
        dep_name = relationship['dependent']
        
        key = f"{prereq_name}->{dep_name}"
        
        if key in self.relationship_key_to_id:
            return self.relationship_key_to_id[key]
        
        return None
    
    def add_concepts(self, new_concepts: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Add new concepts, handling duplicates and returning added and existing concepts."""
        added_concepts = []
        existing_concepts = []
        
        for concept in new_concepts:
            # Ensure concept has all required fields
            if 'source' not in concept:
                concept['source'] = 'unknown'
            if 'grade_level' not in concept:
                concept['grade_level'] = ''
            if 'difficulty' not in concept:
                concept['difficulty'] = ''
            
            # Check for duplicates
            existing_id = self._is_duplicate_concept(concept)
            
            if existing_id:
                # Concept already exists
                existing_concept = next(c for c in self.concepts if c['id'] == existing_id)
                existing_concepts.append(existing_concept)
            else:
                # New concept
                concept['id'] = self._generate_id()
                self.concepts.append(concept)
                self.concept_name_to_id[concept['name']] = concept['id']
                added_concepts.append(concept)
        
        # Save to file after adding new concepts
        if added_concepts:
            self.save_concepts()
        
        return added_concepts, existing_concepts
    
    def add_relationships(self, new_relationships: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Add new relationships, handling duplicates and returning added and existing relationships."""
        added_relationships = []
        existing_relationships = []
        
        for rel in new_relationships:
            # Ensure relationship has all required fields
            if 'source' not in rel:
                rel['source'] = 'unknown'
            if 'strength' not in rel:
                rel['strength'] = 'moderate'
            
            # Check for duplicates
            existing_id = self._is_duplicate_relationship(rel)
            
            if existing_id:
                # Relationship already exists
                existing_rel = next(r for r in self.relationships if r['id'] == existing_id)
                existing_relationships.append(existing_rel)
            else:
                # New relationship
                rel['id'] = self._generate_id()
                
                # Get or create prerequisite concept
                prereq_concept = self._find_concept_by_name(rel['prerequisite'])
                if not prereq_concept:
                    prereq_concept = self._find_concept_by_semantic_match(rel['prerequisite'])
                if not prereq_concept:
                    prereq_concept = self._create_missing_concept(rel['prerequisite'], rel.get('source', 'relationship_creation'))
                
                # Get or create dependent concept
                dep_concept = self._find_concept_by_name(rel['dependent'])
                if not dep_concept:
                    dep_concept = self._find_concept_by_semantic_match(rel['dependent'])
                if not dep_concept:
                    dep_concept = self._create_missing_concept(rel['dependent'], rel.get('source', 'relationship_creation'))
                
                # Create the relationship
                rel['prerequisite_id'] = prereq_concept['id']
                rel['dependent_id'] = dep_concept['id']
                rel['prerequisite_name'] = prereq_concept['name']
                rel['dependent_name'] = dep_concept['name']
                
                self.relationships.append(rel)
                key = f"{rel['prerequisite_name']}->{rel['dependent_name']}"
                self.relationship_key_to_id[key] = rel['id']
                added_relationships.append(rel)
        
        # Save to file after adding new relationships and concepts
        if added_relationships:
            self.save_concepts()  # Save any new concepts that were created
            self.save_relationships()
        
        return added_relationships, existing_relationships
    
    def _create_missing_concept(self, name: str, source: str) -> Dict[str, Any]:
        """Create a missing concept with basic information."""
        concept = {
            'id': self._generate_id(),
            'name': name,
            'explanation': f"Concept referenced in relationship: {name}",
            'broader_concept': 'Unknown',
            'strand': 'Unknown',
            'source': source
        }
        
        self.concepts.append(concept)
        self.concept_name_to_id[concept['name']] = concept['id']
        print(f"Created missing concept: {name}")
        
        # Immediately save to ensure the concept persists
        self.save_concepts()
        
        return concept
    
    def save_concepts(self):
        """Save concepts to CSV file."""
        if self.concepts:
            df = pd.DataFrame(self.concepts)
            # Ensure all concepts have required fields
            for concept in self.concepts:
                if 'source' not in concept:
                    concept['source'] = 'unknown'
                if 'grade_level' not in concept:
                    concept['grade_level'] = ''
                if 'difficulty' not in concept:
                    concept['difficulty'] = ''
            
            # Recreate DataFrame with ensured fields
            df = pd.DataFrame(self.concepts)
            df = df[['id', 'name', 'explanation', 'broader_concept', 'strand', 'source']]
            df.to_csv(CONCEPTS_FILE, index=False)
            print(f"Saved {len(self.concepts)} concepts to {CONCEPTS_FILE}")
    
    def save_relationships(self):
        """Save relationships to CSV file."""
        if self.relationships:
            df = pd.DataFrame(self.relationships)
            # Ensure all relationships have required fields
            for rel in self.relationships:
                if 'source' not in rel:
                    rel['source'] = 'unknown'
                if 'strength' not in rel:
                    rel['strength'] = 'moderate'
            
            # Recreate DataFrame with ensured fields
            df = pd.DataFrame(self.relationships)
            df = df[['id', 'prerequisite_id', 'dependent_id', 'prerequisite_name', 'dependent_name', 'explanation', 'source']]
            df.to_csv(RELATIONSHIPS_FILE, index=False)
            print(f"Saved {len(self.relationships)} relationships to {RELATIONSHIPS_FILE}")
    
    def get_concepts_for_context(self) -> List[Dict[str, Any]]:
        """Get concepts for context in prompts."""
        return self.concepts
    
    def get_relationships_for_context(self) -> List[Dict[str, Any]]:
        """Get relationships for context in prompts."""
        return self.relationships
    
    def get_concept_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a concept by name using flexible matching."""
        return self._find_concept_by_name(name)
    
    def get_statistics(self) -> Dict[str, int]:
        """Get statistics about the current data."""
        # Ensure all concepts have source field for statistics
        sources = set()
        for concept in self.concepts:
            source = concept.get('source', 'unknown')
            sources.add(source)
        
        return {
            'total_concepts': len(self.concepts),
            'total_relationships': len(self.relationships),
            'unique_sources': len(sources)
        } 