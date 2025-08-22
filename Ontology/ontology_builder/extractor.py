"""
Concept Extractor - Handles LLM-based concept and relationship extraction

This is the main orchestrator class that coordinates the entire extraction process.
It manages the workflow: file processing → text chunking → LLM extraction → data management.
This class acts as the central hub connecting all other components.
"""

import os
from processor import FileProcessor
from data_manager import DataManager
from llm_client import LLMClient
from chunker import TextChunker
from config import CONCEPT_EXTRACTION_PROMPT, RELATIONSHIP_EXTRACTION_PROMPT, VERIFICATION_PROMPT

class ConceptExtractor:
    """
    Main extraction engine that coordinates all components of the ontology building process.
    
    This class orchestrates:
    1. File processing (converting various formats to text)
    2. Text chunking (breaking large documents into manageable pieces)
    3. LLM extraction (using AI to identify concepts and relationships)
    4. Data management (storing and organizing extracted information)
    """
    
    def __init__(self):
        """
        Initialize all required components for the extraction pipeline.
        
        Components:
        - file_processor: Handles different file formats (PDF, MD, CSV)
        - data_manager: Manages extracted data and JSON output
        - llm_client: Interfaces with LLM APIs for concept extraction
        - chunker: Breaks large texts into manageable chunks with context
        """
        self.file_processor = FileProcessor()
        self.data_manager = DataManager()
        self.llm_client = LLMClient()
        self.chunker = TextChunker()
    
    def process_file(self, file_path: str, output_file: str):
        """
        Process a single file to extract mathematical concepts and relationships.
        
        Workflow:
        1. Extract text from the file
        2. Split text into context-aware chunks
        3. Use LLM to extract concepts from each chunk
        4. Use LLM to extract relationships between concepts
        5. Verify extraction quality with LLM
        6. Save results to JSON output file
        
        Args:
            file_path: Path to the input file (PDF, MD, or CSV)
            output_file: Path where the JSON output should be saved
        """
        print(f"Processing file: {file_path}")
        
        # Extract text from file
        try:
            text_content = self.file_processor.process_file(file_path)
            print(f"Extracted {len(text_content)} characters of text")
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
            return
        
        # Create context-aware chunks
        chunks = self.chunker.create_chunks(text_content)
        print(f"Split into {len(chunks)} chunks for processing")
        
        # Get existing data for context
        existing_concepts = self.data_manager.get_concepts()
        existing_relationships = self.data_manager.get_relationships()
        
        # Process each chunk
        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i+1}/{len(chunks)}")
            
            # Step 1: Extract concepts
            new_concepts = self._extract_concepts(
                chunk, existing_concepts, existing_relationships, file_path, i, len(chunks)
            )
            
            # Step 2: Extract relationships
            new_relationships = self._extract_relationships(
                chunk, new_concepts, existing_concepts, existing_relationships, file_path, i, len(chunks)
            )
            
            # Step 3: Verify extraction quality
            verification_result = self._verify_extraction(
                chunk, new_concepts, new_relationships, file_path, i, len(chunks)
            )
            
            # Add verified concepts and relationships
            if verification_result['concepts_valid']:
                self.data_manager.add_concepts(new_concepts)
                existing_concepts = self.data_manager.get_concepts()  # Update for next iteration
            
            if verification_result['relationships_valid']:
                self.data_manager.add_relationships(new_relationships)
                existing_relationships = self.data_manager.get_relationships()  # Update for next iteration
        
        # Save final results
        self.data_manager.save_to_json(output_file)
        print(f"Processing complete. Results saved to {output_file}")
    
    def process_directory(self, directory_path: str, output_file: str):
        """
        Process all supported files in a directory to build a comprehensive ontology.
        
        This method iterates through all files in the specified directory,
        processing each supported file and accumulating all extracted concepts
        and relationships into a single knowledge graph.
        
        Args:
            directory_path: Path to directory containing files to process
            output_file: Path where the combined JSON output should be saved
        """
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        supported_files = []
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                if self.file_processor.is_supported(file_path):
                    supported_files.append(file_path)
        
        print(f"Found {len(supported_files)} supported files to process")
        
        for file_path in supported_files:
            try:
                self.process_file(file_path, output_file)
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
                continue
    
    def _extract_concepts(self, chunk: str, existing_concepts: list, existing_relationships: list, 
                         source: str, chunk_index: int, total_chunks: int) -> list:
        """
        Extract mathematical concepts from a text chunk.
        
        Args:
            chunk: Text content to analyze
            existing_concepts: Previously extracted concepts for context
            existing_relationships: Previously extracted relationships for context
            source: Source file name
            chunk_index: Current chunk position
            total_chunks: Total number of chunks
            
        Returns:
            list: New concepts extracted from the chunk
        """
        # Build context for concept extraction
        context = {
            'existing_concepts': existing_concepts,           # Key - for deduplication
            'existing_relationships': existing_relationships, # Key - for context
            'source_file': source,                           # Key - for tracking
            'chunk_position': f"{chunk_index + 1} of {total_chunks}"  # Key - for awareness
        }
        
        return self.llm_client.extract_concepts(chunk, context, CONCEPT_EXTRACTION_PROMPT)
    
    def _extract_relationships(self, chunk: str, new_concepts: list, existing_concepts: list, 
                             existing_relationships: list, source: str, chunk_index: int, 
                             total_chunks: int) -> list:
        """
        Extract relationships between mathematical concepts.
        
        Args:
            chunk: Text content to analyze
            new_concepts: Concepts just extracted from this chunk
            existing_concepts: All previously extracted concepts
            existing_relationships: Previously extracted relationships
            source: Source file name
            chunk_index: Current chunk position
            total_chunks: Total number of chunks
            
        Returns:
            list: New relationships extracted from the chunk
        """
        # Build context for relationship extraction
        context = {
            'new_concepts': new_concepts,                    # Key - for relationship building
            'existing_concepts': existing_concepts,          # Key - for context
            'existing_relationships': existing_relationships, # Key - for patterns
            'source_file': source,                           # Key - for tracking
            'chunk_position': f"{chunk_index + 1} of {total_chunks}", # Key - for awareness
            'concept_hierarchy_hints': self._get_concept_hierarchy_hints(existing_concepts),  # Key - for guidance
            'prerequisite_patterns': self._get_prerequisite_patterns(existing_relationships)   # Key - for patterns
        }
        
        return self.llm_client.extract_relationships(chunk, new_concepts, context, RELATIONSHIP_EXTRACTION_PROMPT)
    
    def _verify_extraction(self, chunk: str, new_concepts: list, new_relationships: list,
                          source: str, chunk_index: int, total_chunks: int) -> dict:
        """
        Verify the quality of extracted concepts and relationships.
        
        Args:
            chunk: Original text content
            new_concepts: Concepts to verify
            new_relationships: Relationships to verify
            source: Source file name
            chunk_index: Current chunk position
            total_chunks: Total number of chunks
            
        Returns:
            dict: Verification results with validity flags
        """
        context = {
            'new_concepts': new_concepts,                    # Key - for verification
            'new_relationships': new_relationships,           # Key - for verification
            'source_file': source,                           # Key - for tracking
            'chunk_position': f"{chunk_index + 1} of {total_chunks}"  # Key - for awareness
        }
        
        return self.llm_client.verify_extraction(context, VERIFICATION_PROMPT)
    
    def _get_concept_hierarchy_hints(self, concepts: list) -> dict:
        """Extract hierarchy hints from existing concepts."""
        hierarchy = {}
        for concept in concepts:
            strand = concept.get('strand', 'Unknown')
            broader = concept.get('broader_concept', 'Unknown')
            if strand not in hierarchy:
                hierarchy[strand] = []
            hierarchy[strand].append({
                'name': concept['name'],
                'broader_concept': broader
            })
        return hierarchy
    
    def _get_prerequisite_patterns(self, relationships: list) -> list:
        """Extract common prerequisite patterns from existing relationships."""
        patterns = []
        for rel in relationships:
            patterns.append({
                'prerequisite': rel.get('prerequisite_name', ''),
                'dependent': rel.get('dependent_name', ''),
                'type': rel.get('relationship_type', 'prerequisite')
            })
        return patterns 