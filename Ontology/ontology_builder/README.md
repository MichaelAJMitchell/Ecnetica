# Ontology Builder

Minimal mathematical concept extraction tool using LLMs.

## Structure

- `main.py` - CLI entry point
- `extractor.py` - Main extraction logic
- `processor.py` - File processing (MD, PDF, CSV)
- `chunker.py` - Text chunking with context
- `llm_client.py` - LLM interactions with fallback
- `data_manager.py` - JSON output and archiving
- `config.py` - Configuration settings

## Usage

```bash
python main.py --file document.pdf --output graph-data.json
python main.py --directory ./documents/ --output graph-data.json
``` 