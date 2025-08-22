"""
Concept Extractor - Handles LLM-based concept and relationship extraction

This is the main orchestrator class that coordinates the entire extraction process.
It manages the workflow: file processing → text chunking → LLM extraction → data management.
This class acts as the central hub connecting all other components.
"""

from processor import FileProcessor
from data_manager import DataManager
from llm_client import LLMClient
from chunker import TextChunker

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
        5. Save results to JSON output file
        
        Args:
            file_path: Path to the input file (PDF, MD, or CSV)
            output_file: Path where the JSON output should be saved
        """
        pass
    
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
        pass 