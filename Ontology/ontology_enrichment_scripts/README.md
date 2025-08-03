# Ontology Enrichment Scripts

This directory contains scripts for enriching the mathematical knowledge graph with additional relationships and insights.

## Relationship Enricher

The `relationship_enricher` script analyzes each concept against all other concepts to find prerequisite relationships using OpenAI's GPT models.

### Updated File Management

The relationship enricher has been updated to use a centralized file management system:

#### Input Files
- **Source**: Files are now read from the `Ontology/` directory instead of the local `Input/` folder
- **Files**: The script automatically detects and uses:
  - Concept files (containing 'concepts' in the filename)
  - Relationship files (containing 'relationships' in the filename)

#### Output Files
- **Destination**: Output files are now written to the `Ontology/` directory instead of the local `Output/` folder
- **File**: `relationships.csv` - Updated relationships with new prerequisite connections

#### Automatic Archiving
Before creating new output files, the script automatically archives any existing knowledge graph CSV files to a timestamped folder in `Ontology/ontology_archive/`. This ensures no data is lost when processing new relationships.

### Usage

```bash
cd relationship_enricher
python3 relationship_enricher.py
```

### Requirements

- Python 3.8+
- OpenAI API key (set in `.env` file)
- Required packages: `pandas`, `openai`, `python-dotenv`

## Utility Scripts

The relationship_enricher directory also contains utility scripts for analyzing and validating the knowledge graph:

### Relationship Checker (`relationship_checker.py`)
- **Purpose**: Detects prerequisite loops (circular dependencies) in the knowledge graph
- **Input**: Uses local `checker_input/` directory
- **Output**: Generates reports in `checker_output/` directory
- **Usage**: Copy files to `checker_input/` and run the script

### Efficient Loop Checker (`efficient_loop_checker.py`)
- **Purpose**: Memory-efficient cycle detection for large knowledge graphs
- **Input**: Uses local `checker_input/` directory  
- **Output**: Generates reports in `checker_output/` directory
- **Usage**: Copy files to `checker_input/` and run the script

*Note: These utility scripts use local directories for input/output as they are designed for independent analysis tasks.*

### File Structure

```
ontology_enrichment_scripts/
├── archive_manager.py              # Archive management utilities
├── relationship_enricher/
│   ├── relationship_enricher.py    # Main enrichment script (updated)
│   ├── relationship_checker.py     # Loop detection utility
│   ├── efficient_loop_checker.py   # Memory-efficient loop detection
│   ├── checker_input/              # Input for utility scripts
│   ├── checker_output/             # Output for utility scripts
│   ├── Input/                      # (Legacy - no longer used)
│   └── Output/                     # (Legacy - no longer used)
└── README.md                       # This file
```

### Changes Made

1. **Updated file paths** to use `Ontology/` directory for input and output
2. **Added automatic archiving** of existing files before processing
3. **Enhanced file detection** to automatically find concept and relationship files
4. **Improved error handling** for missing files
5. **Added progress reporting** for archiving operations

### Archive Structure

When the script runs, it creates timestamped archive folders:
```
Ontology/ontology_archive/
└── enrichment_archive_YYYYMMDD_HHMMSS/
    ├── concepts_*.csv
    └── relationships_*.csv
```

This ensures that previous versions of the knowledge graph are preserved and can be recovered if needed. 