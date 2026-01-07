"""
Text Chunker - Chapter-based MD, row-based CSV, and strand-based PDF chunking
"""

import json
import re

class TextChunker:
    """Chunks MD files by chapters, CSV files by rows, and PDF files by strands."""
    
    def __init__(self, chapters_per_chunk: int = 3, rows_per_chunk: int = 10, strands: list = None):
        """
        Initialize chunker with configurable parameters.
        
        Args:
            chapters_per_chunk: Number of chapters to process together (MD files)
            rows_per_chunk: Number of CSV rows to process together (CSV files)
            strands: List of strand titles for PDF chunking (e.g., ["Organic Chemistry", "Chemical Bonding"])
        """
        self.chapters_per_chunk = chapters_per_chunk
        self.rows_per_chunk = rows_per_chunk
        self.strands = strands or []
    
    def create_chunks(self, content: str, file_type: str) -> list:
        """Create chunks based on file type."""
        if file_type == 'md':
            return self._chunk_markdown_by_chapters(content)
        elif file_type == 'csv':
            return self._chunk_csv_by_rows(content)
        elif file_type == 'pdf':
            return self._chunk_pdf_by_strands(content)
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
    
    def _chunk_pdf_by_strands(self, content: str) -> list:
        """
        Chunk PDF content by strand titles.
        
        Splits the PDF at each strand title, but only if the title is NOT 
        followed by "(continued)" - this ensures we split at the start of 
        each strand, not on continuation pages.
        
        Falls back to page-based chunking if no strands are configured or found.
        """
        if not self.strands:
            # No strands configured, fall back to page-based chunking
            return self._chunk_pdf_by_pages(content)
        
        # Build regex pattern that matches strand titles NOT followed by "(continued)"
        # Using negative lookahead: (?!\s*\(continued\))
        # The pattern is case-insensitive and allows for whitespace variations
        escaped_strands = [re.escape(strand) for strand in self.strands]
        pattern = r'(?=(' + '|'.join(escaped_strands) + r')(?!\s*\(continued\)))'
        
        # Split content at strand boundaries (using lookahead to keep the delimiter)
        chunks = re.split(pattern, content, flags=re.IGNORECASE)
        
        # re.split with capturing groups creates alternating content/match elements
        # We need to recombine: each strand title should start its chunk
        if len(chunks) <= 1:
            # No strand matches found, fall back to page-based chunking
            return self._chunk_pdf_by_pages(content)
        
        # Recombine chunks: merge strand title with following content
        result_chunks = []
        i = 0
        
        # First element might be content before any strand (preamble)
        if chunks[0] and not any(strand.lower() in chunks[0].lower() for strand in self.strands):
            preamble = chunks[0].strip()
            if preamble:
                result_chunks.append(preamble)
            i = 1
        
        # Process remaining chunks (alternating: strand_title, content, strand_title, content...)
        while i < len(chunks):
            current_chunk = chunks[i].strip() if chunks[i] else ""
            
            # Skip empty chunks
            if not current_chunk:
                i += 1
                continue
                
            # Check if this is a strand title
            is_strand = any(strand.lower() == current_chunk.lower() for strand in self.strands)
            
            if is_strand and i + 1 < len(chunks):
                # Combine strand title with its content
                combined = current_chunk + chunks[i + 1]
                if combined.strip():
                    result_chunks.append(combined.strip())
                i += 2
            else:
                if current_chunk:
                    result_chunks.append(current_chunk)
                i += 1
        
        # If we ended up with no chunks, fall back to page-based
        if not result_chunks:
            return self._chunk_pdf_by_pages(content)
        
        return result_chunks
    
    def _chunk_pdf_by_pages(self, content: str, pages_per_chunk: int = 3) -> list:
        """
        Fallback: Chunk PDF content by page breaks.
        
        Uses the --- PAGE BREAK --- markers inserted by the PDF processor.
        """
        pages = content.split("\n\n--- PAGE BREAK ---\n\n")
        
        if len(pages) <= 1:
            return [content] if content.strip() else []
        
        chunks = []
        for i in range(0, len(pages), pages_per_chunk):
            chunk = "\n\n".join(pages[i:i + pages_per_chunk])
            if chunk.strip():
                chunks.append(chunk)
        
        return chunks if chunks else [content]