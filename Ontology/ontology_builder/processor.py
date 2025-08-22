"""
File Processor - Handles different file formats (MD, PDF, CSV)

This module is responsible for converting various document formats into plain text
that can be processed by the LLM. It handles the technical aspects of reading
different file types and extracting their textual content while preserving structure.
"""

import os
import pandas as pd
import PyPDF2
import fitz  # PyMuPDF
import re

class FileProcessor:
    """
    Handles the conversion of different file formats to extractable text.
    
    This class provides a unified interface for processing various document formats,
    abstracting away the complexity of different file types. It ensures that
    regardless of input format, the system always works with clean, structured text.
    """
    
    def __init__(self):
        """
        Initialize the file processor with supported file formats.
        
        Supported formats:
        - .md: Markdown files (text-based with formatting)
        - .pdf: PDF documents (binary format requiring special parsing)
        - .csv: Comma-separated values (tabular data converted to text)
        """
        self.supported_formats = ['.md', '.pdf', '.csv']
    
    def process_file(self, file_path: str) -> str:
        """
        Extract text content from a supported file format.
        
        This method automatically detects the file type and applies the appropriate
        extraction method. It handles encoding issues and provides fallback options
        for problematic files.
        
        Args:
            file_path: Path to the file to be processed
            
        Returns:
            str: Extracted text content ready for chunking and LLM processing
            
        Raises:
            Exception: If file format is not supported or processing fails
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not self.is_supported(file_path):
            raise ValueError(f"Unsupported file format: {self.get_file_extension(file_path)}")
        
        extension = self.get_file_extension(file_path)
        
        processors = {
            '.csv': self.process_csv,
            '.pdf': self.process_pdf,
            '.md': self.process_md
        }
        
        return processors[extension](file_path)
    
    def is_supported(self, file_path: str) -> bool:
        """
        Check if a file format is supported by the processor.
        
        This method examines the file extension to determine if the file
        can be processed. It's used to filter files in directories and
        provide helpful error messages for unsupported formats.
        
        Args:
            file_path: Path to the file to check
            
        Returns:
            bool: True if the file format is supported, False otherwise
        """
        return self.get_file_extension(file_path) in self.supported_formats
    
    def get_file_extension(self, file_path: str) -> str:
        """Get the file extension from a file path."""
        return os.path.splitext(file_path)[1].lower()
    
    def process_csv(self, file_path: str) -> str:
        """Extract text content from CSV files."""
        try:
            df = pd.read_csv(file_path)
            text_content = []
            
            # Add column headers
            text_content.append("Columns: " + ", ".join(df.columns.tolist()))
            text_content.append("\n")
            
            # Add data rows
            for index, row in df.iterrows():
                row_text = f"Row {index + 1}: " + " | ".join([f"{col}: {val}" for col, val in row.items()])
                text_content.append(row_text)
            
            return "\n".join(text_content)
        except Exception as e:
            raise Exception(f"Error processing CSV file {file_path}: {str(e)}")
    
    def process_pdf(self, file_path: str) -> str:
        """Extract text content from PDF files using PyMuPDF with PyPDF2 fallback."""
        try:
            # Try PyMuPDF first (better text extraction)
            doc = fitz.open(file_path)
            text_content = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                if text.strip():
                    text_content.append(f"Page {page_num + 1}:\n{text}")
            
            doc.close()
            return "\n\n".join(text_content)
        except Exception as e:
            # Fallback to PyPDF2 if PyMuPDF fails
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text_content = []
                    
                    for page_num, page in enumerate(pdf_reader.pages):
                        text = page.extract_text()
                        if text.strip():
                            text_content.append(f"Page {page_num + 1}:\n{text}")
                    
                    return "\n\n".join(text_content)
            except Exception as e2:
                raise Exception(f"Error processing PDF file {file_path}: {str(e)} and fallback failed: {str(e2)}")
    
    def process_md(self, file_path: str) -> str:
        """Extract text content from Markdown files with basic formatting removal."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Basic markdown cleaning - remove formatting while preserving text
            # Remove headers (lines starting with #)
            content = re.sub(r'^#{1,6}\s+', '', content, flags=re.MULTILINE)
            
            # Remove bold/italic formatting
            content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)
            content = re.sub(r'\*(.*?)\*', r'\1', content)
            
            # Remove code formatting
            content = re.sub(r'`([^`]*)`', r'\1', content)
            content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
            
            # Remove links and images
            content = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', content)
            content = re.sub(r'!\[([^\]]*)\]\([^)]*\)', r'\1', content)
            
            # Remove list markers
            content = re.sub(r'^[\s]*[-*+]\s+', '', content, flags=re.MULTILINE)
            content = re.sub(r'^[\s]*\d+\.\s+', '', content, flags=re.MULTILINE)
            
            # Clean up whitespace
            content = re.sub(r'\n\s*\n', '\n\n', content)
            content = content.strip()
            
            return content
        except Exception as e:
            raise Exception(f"Error processing Markdown file {file_path}: {str(e)}") 