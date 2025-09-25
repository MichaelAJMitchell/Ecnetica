"""
Text Chunker - Chapter-based MD and row-based CSV chunking
"""

import json
import re

class TextChunker:
    """Chunks MD files by chapters and CSV files by rows."""
    
    def create_chunks(self, content: str, file_type: str, chapters_per_chunk: int = 1) -> list:
        """Create chunks based on file type."""
        if file_type == 'md':
            return self._chunk_markdown_by_chapters(content, chapters_per_chunk)
        elif file_type == 'csv':
            return self._chunk_csv_by_rows(content)
        else:
            return [content]
    
    def _chunk_markdown_by_chapters(self, content: str, chapters_per_chunk: int) -> list:
        """Chunk markdown by chapters/sections."""
        # Find all headers (# ## ###)
        headers = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if re.match(r'^#{1,3}\s+', line):
                headers.append((i, line.strip()))
        
        if not headers:
            return [content]
        
        chunks = []
        for i in range(0, len(headers), chapters_per_chunk):
            start_line = headers[i][0]
            end_line = headers[i + chapters_per_chunk][0] if i + chapters_per_chunk < len(headers) else len(lines)
            
            chunk_lines = lines[start_line:end_line]
            chunks.append('\n'.join(chunk_lines))
        
        return chunks
    
    def _chunk_csv_by_rows(self, content: str) -> list:
        """Chunk CSV data by individual rows."""
        try:
            data = json.loads(content)
            chunks = []
            
            for row in data:
                # Format as key: value pairs
                chunk_lines = []
                for key, value in row.items():
                    chunk_lines.append(f"{key}: {value}")
                chunks.append('\n'.join(chunk_lines))
            
            return chunks
        except json.JSONDecodeError:
            return [content] 