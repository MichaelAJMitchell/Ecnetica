"""
File Processor - Handles different file formats (MD, PDF, CSV)

This module is responsible for converting various document formats into plain text
that can be processed by the LLM. It handles the technical aspects of reading
different file types and extracting their textual content while preserving structure.
"""

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
        pass
    
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
        pass 