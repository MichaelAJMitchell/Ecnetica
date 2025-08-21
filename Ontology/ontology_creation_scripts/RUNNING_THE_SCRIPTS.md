# Running the Ontology Creation Scripts

## The Problem

If you're getting errors like:
```
ModuleNotFoundError: No module named 'tqdm'
```

This means the script is running outside the virtual environment where the dependencies are installed.

## Solutions

### Option 1: Use the Python Wrapper (Recommended)

```bash
# From the ontology_creation_scripts directory
python3 run.py --help
python3 run.py --stats
python3 run.py --file your_file.pdf
```

The `run.py` wrapper automatically:
- ✅ Detects the virtual environment
- ✅ Adds the virtual environment's site-packages to Python path
- ✅ Ensures all dependencies are available
- ✅ Runs the main script with proper environment

### Option 2: Use the Shell Wrapper

```bash
# From the ontology_creation_scripts directory
./run.sh --help
./run.sh --stats
./run.sh --file your_file.pdf
```

The `run.sh` wrapper:
- ✅ Activates the virtual environment
- ✅ Runs the script
- ✅ Deactivates the virtual environment automatically

### Option 3: Manual Virtual Environment Activation

```bash
# From the ontology_creation_scripts directory
source venv/bin/activate
python3 main.py --help
python3 main.py --stats
deactivate
```

## Why This Happens

The scripts require dependencies like:
- `tqdm` (progress bars)
- `openai` (OpenAI API client)
- `pandas` (data manipulation)
- `python-dotenv` (environment variables)

These are installed in the virtual environment (`venv/`) to avoid conflicts with system Python packages.

## Quick Start

1. **Navigate to the scripts directory:**
   ```bash
   cd Ontology/ontology_creation_scripts
   ```

2. **Use the wrapper (recommended):**
   ```bash
   python3 run.py --help
   ```

3. **Or activate virtual environment manually:**
   ```bash
   source venv/bin/activate
   python3 main.py --help
   deactivate
   ```

## Available Commands

- `--help` - Show help and usage examples
- `--stats` - Show current knowledge graph statistics
- `--file FILE` - Process a single file
- `--directory DIRECTORY` - Process all files in a directory
- `--input-folder FOLDER` - Process files in the default input folder
- `--files FILE1 FILE2` - Process multiple specific files

## Examples

```bash
# Show help
python3 run.py --help

# Show current statistics
python3 run.py --stats

# Process a single PDF file
python3 run.py --file curriculum.pdf

# Process all files in a directory
python3 run.py --directory ./documents/

# Process multiple specific files
python3 run.py --files math1.pdf math2.txt curriculum.csv
```

## Troubleshooting

### "Virtual environment not found"
- Make sure you're in the `ontology_creation_scripts` directory
- Run `python3 setup.py` to create the virtual environment
- Install dependencies with `pip install -r requirements.txt`

### "Permission denied" on run.sh
- Make the script executable: `chmod +x run.sh`
- Or use the Python wrapper instead: `python3 run.py`

### Still getting import errors
- Ensure you're using the wrapper scripts (`run.py` or `run.sh`)
- Or manually activate the virtual environment first
- Check that dependencies are installed: `pip list`

## Dependencies

The following packages are required and installed in the virtual environment:
- `openai>=1.0.0` - OpenAI API client
- `pandas>=2.0.0` - Data manipulation
- `tqdm>=4.65.0` - Progress bars
- `python-dotenv>=1.1.0` - Environment variables
- `tenacity>=8.0.0` - Retry logic
- And more...

All dependencies are automatically installed when you run `python3 setup.py`. 