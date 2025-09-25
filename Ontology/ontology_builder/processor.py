"""
File Processor - Handles MD and CSV file formats

This module converts MD and CSV files into text for LLM processing.
"""

import os
import pandas as pd
import re

class FileProcessor:
    """Handles MD and CSV file processing."""
    
    def __init__(self):
        self.supported_formats = ['.md', '.csv']
    
    def process_file(self, file_path: str) -> tuple[str, str]:
        """Extract content and return file type."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not self.is_supported(file_path):
            raise ValueError(f"Unsupported file format: {self.get_file_extension(file_path)}")
        
        extension = self.get_file_extension(file_path)
        
        if extension == '.csv':
            return self.process_csv(file_path), 'csv'
        elif extension == '.md':
            return self.process_md(file_path), 'md'
    
    def is_supported(self, file_path: str) -> bool:
        return self.get_file_extension(file_path) in self.supported_formats
    
    def get_file_extension(self, file_path: str) -> str:
        return os.path.splitext(file_path)[1].lower()
    
    def process_csv(self, file_path: str) -> str:
        """Return CSV data as structured text for row-based chunking."""
        df = pd.read_csv(file_path)
        return df.to_json(orient='records')
    
    def process_md(self, file_path: str) -> str:
        """Return markdown content for chapter-based chunking."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read() 