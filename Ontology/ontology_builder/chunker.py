"""
Text Chunker - Modular text chunking with context awareness

This module handles the critical task of breaking large documents into manageable
pieces for LLM processing. It implements context-aware chunking that preserves
the relationships between concepts that might span multiple chunks.
"""

class TextChunker:
    """
    Breaks large text documents into manageable chunks while preserving context.
    
    LLMs have token limits, so large documents must be split into smaller pieces.
    This class ensures that chunks are created intelligently to maintain context
    and prevent important mathematical concepts from being split across boundaries.
    """
    
    def __init__(self, chunk_size: int = 1000000, overlap_size: int = 200000):
        """
        Initialize the chunker with configurable chunk and overlap sizes.
        
        Args:
            chunk_size: Maximum characters per chunk (default: 1M characters)
            overlap_size: Number of characters to overlap between chunks (default: 200K)
            
        The overlap ensures that concepts at chunk boundaries aren't lost and
        provides context for the LLM to understand relationships between chunks.
        """
        self.chunk_size = chunk_size
        self.overlap_size = overlap_size
    
    def create_chunks(self, text: str) -> list:
        """
        Create simple text chunks with overlap and sentence boundary awareness.
        
        This method splits text into chunks while ensuring that:
        1. No chunk exceeds the maximum size limit
        2. Adjacent chunks have sufficient overlap for context
        3. Chunks are created at natural break points when possible
        
        Args:
            text: The full text document to be chunked
            
        Returns:
            list: List of text strings, each representing a chunk
        """
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # Try to break at sentence boundary if possible
            if end < len(text):
                end = self._find_sentence_boundary(text, start, end)
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - self.overlap_size
            if start >= len(text):
                break
        
        return chunks
    
    def _find_sentence_boundary(self, text: str, start: int, ideal_end: int) -> int:
        """
        Find the best sentence boundary near the ideal chunk end.
        
        This method looks for sentence endings (., !, ?) within a reasonable
        distance of the ideal chunk end to avoid cutting concepts mid-sentence.
        
        Args:
            text: The full text content
            start: Start position of current chunk
            ideal_end: Ideal end position for current chunk
            
        Returns:
            int: The best position to end the chunk (at sentence boundary if found)
        """
        # Look within 200 characters of ideal end
        search_start = max(ideal_end - 200, start)
        search_end = min(ideal_end + 200, len(text))
        
        # Find last sentence ending
        for char in ['.', '!', '?']:
            pos = text.rfind(char, search_start, search_end)
            if pos > start + self.chunk_size // 2:  # Don't break too early
                return pos + 1
        
        return ideal_end 