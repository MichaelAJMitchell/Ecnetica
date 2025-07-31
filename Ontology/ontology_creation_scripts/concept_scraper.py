import os
import time
from typing import List, Dict, Any
from tqdm import tqdm
from file_processor import FileProcessor
from openai_client import OpenAIClient
from data_manager import DataManager
from config import CHUNK_SIZE, OVERLAP_SIZE

class ConceptScraper:
    """Main class for scraping mathematical concepts and relationships from documents."""
    
    def __init__(self):
        self.file_processor = FileProcessor()
        self.openai_client = OpenAIClient()
        self.data_manager = DataManager()
    
    def process_single_file(self, file_path: str) -> Dict[str, Any]:
        """Process a single file and extract concepts and relationships."""
        print(f"\n{'='*60}")
        print(f"Processing file: {file_path}")
        print(f"{'='*60}")
        
        # Extract text from file
        try:
            text_content = self.file_processor.process_file(file_path)
            print(f"Extracted {len(text_content)} characters of text")
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
            return {
                'file': file_path,
                'success': False,
                'error': str(e),
                'concepts_added': 0,
                'relationships_added': 0
            }
        
        # Chunk the text
        chunks = self.file_processor.chunk_text(text_content, CHUNK_SIZE, OVERLAP_SIZE)
        print(f"Split into {len(chunks)} chunks for processing")
        
        # Get existing data for context
        existing_concepts = self.data_manager.get_concepts_for_context()
        existing_relationships = self.data_manager.get_relationships_for_context()
        
        total_concepts_added = 0
        total_relationships_added = 0
        source = os.path.basename(file_path)
        
        # Process each chunk
        for i, chunk in enumerate(tqdm(chunks, desc="Processing chunks")):
            print(f"\nProcessing chunk {i+1}/{len(chunks)}")
            
            # Extract concepts from chunk
            try:
                new_concepts = self.openai_client.extract_concepts(
                    chunk, existing_concepts, source
                )
                
                if new_concepts:
                    added_concepts, existing_concepts_found = self.data_manager.add_concepts(new_concepts)
                    total_concepts_added += len(added_concepts)
                    
                    if added_concepts:
                        print(f"Added {len(added_concepts)} new concepts from chunk {i+1}")
                        for concept in added_concepts:
                            print(f"  - {concept['name']}")
                    
                    if existing_concepts_found:
                        print(f"Found {len(existing_concepts_found)} existing concepts in chunk {i+1}")
                
                # Update existing concepts list for relationship extraction
                existing_concepts = self.data_manager.get_concepts_for_context()
                
            except Exception as e:
                print(f"Error extracting concepts from chunk {i+1}: {str(e)}")
                continue
            
            # Extract relationships from chunk
            try:
                new_relationships = self.openai_client.extract_relationships(
                    chunk, existing_concepts, existing_relationships, source
                )
                
                if new_relationships:
                    added_relationships, existing_relationships_found = self.data_manager.add_relationships(new_relationships)
                    total_relationships_added += len(added_relationships)
                    
                    if added_relationships:
                        print(f"Added {len(added_relationships)} new relationships from chunk {i+1}")
                        for rel in added_relationships:
                            print(f"  - {rel['prerequisite_name']} → {rel['dependent_name']}")
                    
                    if existing_relationships_found:
                        print(f"Found {len(existing_relationships_found)} existing relationships in chunk {i+1}")
                
                # Update existing relationships list for next iteration
                existing_relationships = self.data_manager.get_relationships_for_context()
                
            except Exception as e:
                print(f"Error extracting relationships from chunk {i+1}: {str(e)}")
                continue
            
            # Small delay to avoid overwhelming the API
            time.sleep(0.5)
        
        # Print summary
        stats = self.data_manager.get_statistics()
        print(f"\n{'='*60}")
        print(f"Processing complete for {file_path}")
        print(f"Concepts added: {total_concepts_added}")
        print(f"Relationships added: {total_relationships_added}")
        print(f"Total concepts in database: {stats['total_concepts']}")
        print(f"Total relationships in database: {stats['total_relationships']}")
        print(f"{'='*60}")
        
        return {
            'file': file_path,
            'success': True,
            'concepts_added': total_concepts_added,
            'relationships_added': total_relationships_added,
            'total_concepts': stats['total_concepts'],
            'total_relationships': stats['total_relationships']
        }
    
    def process_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """Process all supported files in a directory."""
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        results = []
        supported_files = []
        
        # Find all supported files
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                if self.file_processor.is_supported_format(file_path):
                    supported_files.append(file_path)
        
        if not supported_files:
            print(f"No supported files found in {directory_path}")
            return results
        
        print(f"Found {len(supported_files)} supported files to process")
        
        # Process each file
        for file_path in supported_files:
            try:
                result = self.process_single_file(file_path)
                results.append(result)
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
                results.append({
                    'file': file_path,
                    'success': False,
                    'error': str(e),
                    'concepts_added': 0,
                    'relationships_added': 0
                })
        
        return results
    
    def process_files(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """Process a list of specific files."""
        results = []
        
        for file_path in file_paths:
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                results.append({
                    'file': file_path,
                    'success': False,
                    'error': 'File not found',
                    'concepts_added': 0,
                    'relationships_added': 0
                })
                continue
            
            if not self.file_processor.is_supported_format(file_path):
                print(f"Unsupported file format: {file_path}")
                results.append({
                    'file': file_path,
                    'success': False,
                    'error': 'Unsupported file format',
                    'concepts_added': 0,
                    'relationships_added': 0
                })
                continue
            
            try:
                result = self.process_single_file(file_path)
                results.append(result)
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
                results.append({
                    'file': file_path,
                    'success': False,
                    'error': str(e),
                    'concepts_added': 0,
                    'relationships_added': 0
                })
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get current statistics about the knowledge graph."""
        stats = self.data_manager.get_statistics()
        
        # Get concept distribution by strand
        strand_counts = {}
        for concept in self.data_manager.concepts:
            strand = concept.get('strand', 'Unknown')
            strand_counts[strand] = strand_counts.get(strand, 0) + 1
        
        stats['strand_distribution'] = strand_counts
        
        return stats
    
    def print_statistics(self):
        """Print current statistics about the knowledge graph."""
        stats = self.get_statistics()
        
        print(f"\n{'='*60}")
        print("KNOWLEDGE GRAPH STATISTICS")
        print(f"{'='*60}")
        print(f"Total Concepts: {stats['total_concepts']}")
        print(f"Total Relationships: {stats['total_relationships']}")
        print(f"Unique Sources: {stats['unique_sources']}")
        
        if stats['strand_distribution']:
            print(f"\nConcept Distribution by Strand:")
            for strand, count in sorted(stats['strand_distribution'].items(), key=lambda x: x[1], reverse=True):
                print(f"  {strand}: {count}")
        
        print(f"{'='*60}") 