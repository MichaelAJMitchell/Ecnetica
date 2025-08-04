import os
import pandas as pd
import PyPDF2
import fitz  # PyMuPDF
import docx
import re
from typing import List, Dict, Any
from config import SUPPORTED_FORMATS

class FileProcessor:
    """Handles processing of different file formats into readable text."""
    
    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """Get the file extension from a file path."""
        return os.path.splitext(file_path)[1].lower()
    
    @staticmethod
    def is_supported_format(file_path: str) -> bool:
        """Check if the file format is supported."""
        return FileProcessor.get_file_extension(file_path) in SUPPORTED_FORMATS
    
    @staticmethod
    def process_csv(file_path: str) -> str:
        """Extract text content from CSV files."""
        try:
            df = pd.read_csv(file_path)
            # Convert DataFrame to text representation
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
    
    @staticmethod
    def process_pdf(file_path: str) -> str:
        """Extract text content from PDF files using PyMuPDF."""
        try:
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
    
    @staticmethod
    def process_txt(file_path: str) -> str:
        """Extract text content from TXT files."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    return file.read()
            except Exception as e:
                raise Exception(f"Error processing TXT file {file_path}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error processing TXT file {file_path}: {str(e)}")
    
    @staticmethod
    def process_tex(file_path: str) -> str:
        """Extract text content from TEX files, removing LaTeX commands."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Remove LaTeX commands and environments
            # Remove \command{...} patterns
            content = re.sub(r'\\[a-zA-Z]+(\{[^}]*\})*', '', content)
            
            # Remove \begin{...} ... \end{...} blocks
            content = re.sub(r'\\begin\{[^}]*\}.*?\\end\{[^}]*\}', '', content, flags=re.DOTALL)
            
            # Remove remaining LaTeX symbols
            content = re.sub(r'\\[a-zA-Z]+', '', content)
            content = re.sub(r'\{[^}]*\}', '', content)
            
            # Clean up extra whitespace
            content = re.sub(r'\s+', ' ', content)
            content = content.strip()
            
            return content
        except Exception as e:
            raise Exception(f"Error processing TEX file {file_path}: {str(e)}")
    
    @staticmethod
    def process_md(file_path: str) -> str:
        """Extract text content from Markdown files, removing markdown formatting."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Remove markdown formatting while preserving text content
            
            # Remove headers (lines starting with #)
            content = re.sub(r'^#{1,6}\s+', '', content, flags=re.MULTILINE)
            
            # Remove bold formatting (**text** or __text__)
            content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)
            content = re.sub(r'__(.*?)__', r'\1', content)
            
            # Remove italic formatting (*text* or _text_)
            content = re.sub(r'\*(.*?)\*', r'\1', content)
            content = re.sub(r'_(.*?)_', r'\1', content)
            
            # Remove code formatting (`text`)
            content = re.sub(r'`([^`]*)`', r'\1', content)
            
            # Remove code blocks (```...```)
            content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
            
            # Remove inline code blocks (```...```)
            content = re.sub(r'`{3,}.*?`{3,}', '', content, flags=re.DOTALL)
            
            # Remove links ([text](url))
            content = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', content)
            
            # Remove images (![alt](url))
            content = re.sub(r'!\[([^\]]*)\]\([^)]*\)', r'\1', content)
            
            # Remove horizontal rules (---, ***, ___)
            content = re.sub(r'^[-*_]{3,}$', '', content, flags=re.MULTILINE)
            
            # Remove blockquotes (> text)
            content = re.sub(r'^>\s*', '', content, flags=re.MULTILINE)
            
            # Remove list markers (-, *, +, 1., 2., etc.)
            content = re.sub(r'^[\s]*[-*+]\s+', '', content, flags=re.MULTILINE)
            content = re.sub(r'^[\s]*\d+\.\s+', '', content, flags=re.MULTILINE)
            
            # Remove table formatting (| and -)
            content = re.sub(r'^\|.*\|$', '', content, flags=re.MULTILINE)
            content = re.sub(r'^[\s]*[-|]+\s*$', '', content, flags=re.MULTILINE)
            
            # Clean up extra whitespace and empty lines
            content = re.sub(r'\n\s*\n', '\n\n', content)
            content = re.sub(r'^\s+$', '', content, flags=re.MULTILINE)
            content = content.strip()
            
            return content
        except Exception as e:
            raise Exception(f"Error processing Markdown file {file_path}: {str(e)}")
    
    @staticmethod
    def process_docx(file_path: str) -> str:
        """Extract text content from DOCX files."""
        try:
            doc = docx.Document(file_path)
            text_content = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_content.append(paragraph.text)
            
            return "\n".join(text_content)
        except Exception as e:
            raise Exception(f"Error processing DOCX file {file_path}: {str(e)}")
    
    @staticmethod
    def process_file(file_path: str) -> str:
        """Process a file based on its extension and return the extracted text."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not FileProcessor.is_supported_format(file_path):
            raise ValueError(f"Unsupported file format: {FileProcessor.get_file_extension(file_path)}")
        
        extension = FileProcessor.get_file_extension(file_path)
        
        processors = {
            '.csv': FileProcessor.process_csv,
            '.pdf': FileProcessor.process_pdf,
            '.txt': FileProcessor.process_txt,
            '.tex': FileProcessor.process_tex,
            '.docx': FileProcessor.process_docx,
            '.md': FileProcessor.process_md
        }
        
        return processors[extension](file_path)
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 2000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks for processing."""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # If this isn't the last chunk, try to break at a sentence boundary
            if end < len(text):
                # Look for sentence endings within the last 100 characters
                search_start = max(start + chunk_size - 100, start)
                search_end = min(end + 100, len(text))
                
                # Find the last sentence ending in this range
                last_period = text.rfind('.', search_start, search_end)
                last_exclamation = text.rfind('!', search_start, search_end)
                last_question = text.rfind('?', search_start, search_end)
                
                # Use the latest sentence ending
                sentence_end = max(last_period, last_exclamation, last_question)
                
                if sentence_end > start + chunk_size // 2:  # Only use if it's not too early
                    end = sentence_end + 1
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position, accounting for overlap
            start = end - overlap
            if start >= len(text):
                break
        
        return chunks 