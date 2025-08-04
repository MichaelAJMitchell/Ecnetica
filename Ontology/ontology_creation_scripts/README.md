# Mathematical Concept Scraper

A comprehensive tool for extracting mathematical concepts and prerequisite relationships from educational documents to build a knowledge graph. The tool processes various document formats and uses OpenAI's GPT models to identify granular mathematical concepts and their dependencies.

## Features

- **Multi-format Support**: Processes PDF, CSV, TXT, TEX, and DOCX files
- **High Granularity**: Extracts very specific mathematical concepts (e.g., "single digit addition" instead of just "addition")
- **Prerequisite Detection**: Identifies relationships between concepts (what must be learned before what)
- **Deduplication**: Avoids duplicate concepts and relationships across documents
- **Continuous Learning**: Uses existing concepts and relationships as context for new extractions
- **Robust Error Handling**: Retry logic with exponential backoff for API failures
- **Model Fallbacks**: Automatically falls back to alternative GPT models if the primary model fails
- **Progress Tracking**: Real-time progress updates and statistics

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd new_curriculum_scraper
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

### Command Line Interface

The tool provides a flexible command-line interface for processing documents:

#### Process a single file:
```bash
python main.py --file path/to/document.pdf
```

#### Process all supported files in a directory:
```bash
python main.py --directory path/to/documents/
```

#### Process multiple specific files:
```bash
python main.py --files math1.pdf math2.txt curriculum.csv textbook.md
```

#### Show current knowledge graph statistics:
```bash
python main.py --stats
```

### Python API

You can also use the scraper programmatically:

```python
from concept_scraper import ConceptScraper

# Initialize the scraper
scraper = ConceptScraper()

# Process a single file
result = scraper.process_single_file("curriculum.pdf")

# Process a directory
results = scraper.process_directory("./documents/")

# Get statistics
stats = scraper.get_statistics()
scraper.print_statistics()
```

## Output Format

The tool generates two CSV files in the `Ontology/` directory:

### Concepts (`concepts.csv`)
| Column | Description |
|--------|-------------|
| `id` | Unique identifier for the concept |
| `name` | Name of the mathematical concept |
| `explanation` | Brief explanation of what the concept is |
| `broader_concept` | Broader category the concept falls under |
| `strand` | Mathematical strand/topic (e.g., Algebra, Number, Geometry) |
| `source` | Source document where the concept was found |

### Relationships (`relationships.csv`)
| Column | Description |
|--------|-------------|
| `id` | Unique identifier for the relationship |
| `prerequisite_id` | ID of the prerequisite concept |
| `dependent_id` | ID of the dependent concept |
| `prerequisite_name` | Name of the prerequisite concept |
| `dependent_name` | Name of the dependent concept |
| `explanation` | Explanation of why this prerequisite relationship exists |
| `source` | Source document where the relationship was found |

### Automatic Archiving

Before creating new output files, the tool automatically archives any existing knowledge graph CSV files (containing 'concepts' or 'relationships' in their names) to a timestamped folder in `Ontology/ontology_archive/`. This ensures no data is lost when processing new documents.

## Configuration

The tool's behavior can be customized by modifying `config.py`:

- **OpenAI Models**: Change default and fallback models
- **Retry Settings**: Adjust retry attempts, delays, and backoff factors
- **Chunking**: Modify text chunk size and overlap for processing
- **Prompts**: Customize the prompts used for concept and relationship extraction
- **Output Directory**: Change where output files are saved (default: Ontology directory)
- **Archive Directory**: Configure where archived files are stored

## Supported File Formats

- **PDF**: Extracts text using PyMuPDF with PyPDF2 fallback
- **CSV**: Converts structured data to readable text format
- **TXT**: Plain text files with UTF-8 encoding support
- **TEX**: LaTeX files with command removal
- **DOCX**: Microsoft Word documents
- **MD**: Markdown files with formatting removal

## Error Handling

The tool includes comprehensive error handling:

- **API Failures**: Automatic retry with exponential backoff
- **Model Fallbacks**: Switches to alternative GPT models if primary fails
- **File Processing**: Graceful handling of corrupted or unsupported files
- **Rate Limiting**: Built-in delays and retry logic for API rate limits

## Example Output

### Concept Extraction
```
Processing file: math_curriculum.pdf
Extracted 15420 characters of text
Split into 8 chunks for processing

Processing chunks: 100%|██████████| 8/8 [00:45<00:00]

Added 12 new concepts from chunk 1
  - Single digit addition
  - Multi-digit addition with carrying
  - Place value understanding
  - Number line addition
  ...

Added 8 new relationships from chunk 1
  - Place value understanding → Multi-digit addition with carrying
  - Single digit addition → Multi-digit addition with carrying
  ...
```

### Statistics
```
============================================================
KNOWLEDGE GRAPH STATISTICS
============================================================
Total Concepts: 156
Total Relationships: 89
Unique Sources: 12

Concept Distribution by Strand:
  Number: 67
  Algebra: 34
  Geometry: 28
  Measurement: 18
  Statistics: 9
============================================================
```

## Advanced Usage

### Custom Prompts

You can modify the extraction prompts in `config.py` to better suit your specific use case:

```python
CONCEPT_EXTRACTION_PROMPT = """
Your custom prompt here...
{context_part}
{text_chunk}
"""
```

### Batch Processing

For large document collections, you can process files in batches:

```python
import os
from concept_scraper import ConceptScraper

scraper = ConceptScraper()

# Get all PDF files in a directory
pdf_files = [f for f in os.listdir("./documents/") if f.endswith('.pdf')]

# Process in batches
batch_size = 10
for i in range(0, len(pdf_files), batch_size):
    batch = pdf_files[i:i+batch_size]
    results = scraper.process_files(batch)
    print(f"Processed batch {i//batch_size + 1}")
```

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your OpenAI API key is set in the `.env` file
2. **Rate Limiting**: The tool automatically handles rate limits, but you may need to increase delays for high-volume processing
3. **File Encoding**: For TXT files with encoding issues, the tool tries UTF-8 first, then falls back to latin-1
4. **Large Files**: Very large documents are automatically chunked for processing

### Performance Tips

- Use smaller chunk sizes for more detailed extraction
- Process files in smaller batches to avoid overwhelming the API
- Monitor your OpenAI API usage and costs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions, please open an issue on the GitHub repository. 