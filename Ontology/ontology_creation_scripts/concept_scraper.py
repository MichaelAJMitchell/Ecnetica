import os
import time
from typing import List, Dict, Any
from tqdm import tqdm
from file_processor import FileProcessor
from openai_client import OpenAIClient
from data_manager import DataManager
from quality_assessor import QualityAssessor
from adaptive_prompt_manager import AdaptivePromptManager
from config import CHUNK_SIZE, OVERLAP_SIZE

class ConceptScraper:
    """Main class for scraping mathematical concepts and relationships from documents."""
    
    def __init__(self):
        self.file_processor = FileProcessor()
        self.openai_client = OpenAIClient()
        self.data_manager = DataManager()
        
        # Initialize meta-prompting components
        self.quality_assessor = QualityAssessor()
        self.prompt_manager = AdaptivePromptManager(self.quality_assessor, None)  # Will be set up later
        
        # Track quality metrics for this session
        self.session_quality_metrics = []
    
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
        
        # Create semantic chunks with context awareness
        print("Creating semantic chunks with context awareness...")
        context_aware_chunks = self.file_processor.create_context_aware_chunks(
            text_content, CHUNK_SIZE, OVERLAP_SIZE
        )
        print(f"Split into {len(context_aware_chunks)} semantic chunks for processing")
        
        # Get existing data for context
        existing_concepts = self.data_manager.get_concepts_for_context()
        existing_relationships = self.data_manager.get_relationships_for_context()
        
        total_concepts_added = 0
        total_relationships_added = 0
        source = os.path.basename(file_path)
        
        # Process each chunk with multi-stage extraction and quality assessment
        for i, chunk_info in enumerate(tqdm(context_aware_chunks, desc="Processing chunks")):
            print(f"\nProcessing chunk {i+1}/{len(context_aware_chunks)}")
            print(f"Context: {chunk_info['document_context']}")
            
            chunk_content = chunk_info['chunk_content']
            
            # Extract concepts using multi-stage approach
            try:
                new_concepts = self.openai_client.extract_concepts_multi_stage(
                    chunk_content, existing_concepts, source, chunk_info
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
            
            # Extract relationships using enhanced approach
            try:
                new_relationships = self.openai_client.extract_relationships_enhanced(
                    chunk_content, existing_concepts, existing_relationships, source, chunk_info
                )
                
                if new_relationships:
                    added_relationships, existing_relationships_found = self.data_manager.add_relationships(new_relationships)
                    total_relationships_added += len(added_relationships)
                    
                    if added_relationships:
                        print(f"Added {len(added_relationships)} new relationships from chunk {i+1}")
                        for rel in added_relationships:
                            strength = rel.get('strength', 'unknown')
                            print(f"  - {rel['prerequisite_name']} → {rel['dependent_name']} (strength: {strength})")
                    
                    if existing_relationships_found:
                        print(f"Found {len(existing_relationships_found)} existing relationships in chunk {i+1}")
                
                # Update existing relationships list for next iteration
                existing_relationships = self.data_manager.get_relationships_for_context()
                
            except Exception as e:
                print(f"Error extracting relationships from chunk {i+1}: {str(e)}")
                continue
            
            # Quality Assessment and Meta-Prompting
            self._assess_chunk_quality(
                chunk_content, 
                new_concepts, 
                new_relationships, 
                source, 
                chunk_info,
                i + 1
            )
        
        # Final quality summary for the file
        file_quality_summary = self._generate_file_quality_summary(source)
        
        return {
            'file': file_path,
            'success': True,
            'concepts_added': total_concepts_added,
            'relationships_added': total_relationships_added,
            'quality_summary': file_quality_summary
        }
    
    def _assess_chunk_quality(self, 
                             chunk_content: str, 
                             concepts: List[Dict], 
                             relationships: List[Dict], 
                             source: str, 
                             chunk_info: Dict[str, Any],
                             chunk_number: int):
        """Assess the quality of extraction for a chunk and trigger meta-prompting if needed."""
        
        if not concepts and not relationships:
            print(f"  No concepts or relationships extracted from chunk {chunk_number} - skipping quality assessment")
            return
        
        print(f"  Assessing quality of chunk {chunk_number} extraction...")
        
        # Assess quality using AI
        quality_assessment = self.quality_assessor.assess_extraction_quality(
            concepts, relationships, chunk_content, source
        )
        
        # Store quality metrics
        chunk_quality_record = {
            'chunk_number': chunk_number,
            'source_file': source,
            'chunk_context': chunk_info.get('document_context', ''),
            'quality_assessment': quality_assessment,
            'concepts_count': len(concepts),
            'relationships_count': len(relationships)
        }
        
        self.session_quality_metrics.append(chunk_quality_record)
        
        # Display quality summary
        self._display_quality_summary(quality_assessment, chunk_number)
        
        # Record performance for prompt management
        extraction_metadata = {
            'source_file': source,
            'chunk_number': chunk_number,
            'concepts_count': len(concepts),
            'relationships_count': len(relationships),
            'chunk_context': chunk_info.get('document_context', '')
        }
        
        # Record performance for each prompt type used
        if concepts:
            self.prompt_manager.record_extraction_performance(
                'stage1_broad_concept', quality_assessment, extraction_metadata
            )
            self.prompt_manager.record_extraction_performance(
                'stage2_granular_concept', quality_assessment, extraction_metadata
            )
            self.prompt_manager.record_extraction_performance(
                'stage3_cross_reference', quality_assessment, extraction_metadata
            )
        
        if relationships:
            self.prompt_manager.record_extraction_performance(
                'relationship_extraction', quality_assessment, extraction_metadata
            )
    
    def _display_quality_summary(self, quality_assessment: Dict[str, Any], chunk_number: int):
        """Display a summary of quality assessment results."""
        print(f"    Quality Assessment for Chunk {chunk_number}:")
        
        metrics = ['concept_granularity', 'concept_completeness', 'relationship_accuracy', 
                  'relationship_completeness', 'overall_quality']
        
        for metric in metrics:
            if metric in quality_assessment:
                metric_data = quality_assessment[metric]
                if isinstance(metric_data, dict) and 'score' in metric_data:
                    score = metric_data['score']
                    feedback = metric_data.get('feedback', 'No feedback')
                    
                    # Color code the score
                    if score >= 8:
                        score_display = f"✅ {score}/10"
                    elif score >= 6:
                        score_display = f"⚠️  {score}/10"
                    else:
                        score_display = f"❌ {score}/10"
                    
                    print(f"      {metric.replace('_', ' ').title()}: {score_display}")
                    if len(feedback) < 100:  # Only show short feedback
                        print(f"        Feedback: {feedback}")
        
        # Show improvement suggestions
        if 'improvement_suggestions' in quality_assessment:
            suggestions = quality_assessment['improvement_suggestions']
            if suggestions:
                print(f"      Improvement Suggestions:")
                for suggestion in suggestions[:2]:  # Show first 2 suggestions
                    print(f"        - {suggestion}")
    
    def _generate_file_quality_summary(self, source: str) -> Dict[str, Any]:
        """Generate a quality summary for the entire file."""
        if not self.session_quality_metrics:
            return {"message": "No quality metrics available"}
        
        # Filter metrics for this source file
        file_metrics = [m for m in self.session_quality_metrics if m['source_file'] == source]
        
        if not file_metrics:
            return {"message": f"No quality metrics found for {source}"}
        
        # Calculate summary statistics
        total_chunks = len(file_metrics)
        total_concepts = sum(m['concepts_count'] for m in file_metrics)
        total_relationships = sum(m['relationships_count'] for m in file_metrics)
        
        # Calculate average quality scores
        quality_scores = {}
        metrics = ['concept_granularity', 'concept_completeness', 'relationship_accuracy', 
                  'relationship_completeness', 'overall_quality']
        
        for metric in metrics:
            scores = []
            for record in file_metrics:
                if 'quality_assessment' in record and metric in record['quality_assessment']:
                    metric_data = record['quality_assessment'][metric]
                    if isinstance(metric_data, dict) and 'score' in metric_data:
                        scores.append(metric_data['score'])
            
            if scores:
                quality_scores[metric] = {
                    'average': sum(scores) / len(scores),
                    'min': min(scores),
                    'max': max(scores)
                }
        
        summary = {
            'source_file': source,
            'total_chunks_processed': total_chunks,
            'total_concepts_extracted': total_concepts,
            'total_relationships_extracted': total_relationships,
            'quality_scores': quality_scores,
            'chunks_with_issues': len([m for m in file_metrics 
                                     if m['quality_assessment'].get('overall_quality', {}).get('score', 0) < 6])
        }
        
        return summary
    
    def get_session_quality_summary(self) -> Dict[str, Any]:
        """Get a summary of quality metrics for the entire session."""
        return self.quality_assessor.get_quality_summary()
    
    def save_quality_metrics(self, filepath: str):
        """Save quality metrics from this session."""
        self.quality_assessor.save_quality_metrics(filepath)
    
    def save_prompt_performance(self, filepath: str):
        """Save prompt performance data."""
        self.prompt_manager.save_prompt_registry(filepath)
    
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