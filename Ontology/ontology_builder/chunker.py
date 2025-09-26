"""
Text Chunker - Chapter-based MD and row-based CSV chunking
"""

import json
import re

class TextChunker:
    """Chunks MD files by chapters and CSV files by rows."""
    
    def __init__(self, chapters_per_chunk: int = 3, rows_per_chunk: int = 10):
        """
        Initialize chunker with configurable parameters.
        
        Args:
            chapters_per_chunk: Number of chapters to process together (MD files)
            rows_per_chunk: Number of CSV rows to process together (CSV files)
        """
        self.chapters_per_chunk = chapters_per_chunk
        self.rows_per_chunk = rows_per_chunk
    
    def create_chunks(self, content: str, file_type: str) -> list:
        """Create chunks based on file type."""
        if file_type == 'md':
            return self._chunk_markdown_by_chapters(content)
        elif file_type == 'csv':
            return self._chunk_csv_by_rows(content)
        else:
            return [content]
    
    def _chunk_markdown_by_chapters(self, content: str) -> list:
        """Chunk markdown by main chapters only (level 1 headers)."""
        headers = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if re.match(r'^#\s+', line):  # Only level 1 headers
                headers.append((i, line.strip()))
        
        if not headers:
            return [content]
        
        chunks = []
        for i in range(0, len(headers), self.chapters_per_chunk):
            start_line = headers[i][0]
            end_line = headers[i + self.chapters_per_chunk][0] if i + self.chapters_per_chunk < len(headers) else len(lines)
            
            chunk_lines = lines[start_line:end_line]
            chunks.append('\n'.join(chunk_lines))
        
        return chunks
    
    def _chunk_csv_by_rows(self, content: str) -> list:
        """Chunk CSV data by multiple rows."""
        try:
            data = json.loads(content)
            chunks = []
            
            for i in range(0, len(data), self.rows_per_chunk):
                chunk_rows = data[i:i + self.rows_per_chunk]
                
                chunk_lines = []
                for row in chunk_rows:
                    for key, value in row.items():
                        chunk_lines.append(f"{key}: {value}")
                    chunk_lines.append("---")  # Separator between rows
                
                chunks.append('\n'.join(chunk_lines))
            
            return chunks
        except json.JSONDecodeError:
            return [content]