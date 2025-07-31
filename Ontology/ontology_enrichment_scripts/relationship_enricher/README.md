# Mathematics Knowledge Graph Relationship Enricher

This tool analyzes existing mathematical concepts and relationships to find missing prerequisite relationships using OpenAI models.

## Features

- **AI-Powered Analysis**: Uses OpenAI models to identify missing prerequisite relationships
- **Duplicate Prevention**: Ensures no duplicate relationships are created
- **Continuous Progress Saving**: Saves progress after each batch to prevent data loss
- **Configurable Parameters**: Adjustable batch sizes, delays, and analysis limits
- **Comprehensive Logging**: Detailed logs for monitoring progress and debugging

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set OpenAI API Key**:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   Or set it as an environment variable in your system.

3. **Prepare Data**:
   - Ensure your concepts CSV is in `Input/concepts_06_07_better.csv`
   - Ensure your relationships CSV is in `Input/relationships_06_06_better.csv`

## Usage

### Basic Usage

Run the script with default settings:
```bash
python relationship_enricher.py
```

### Configuration

The script is configured with conservative defaults:
- **Batch Size**: 3 pairs per API call (to start small)
- **Max Pairs**: 50 pairs total (for initial testing)
- **Delay**: 2 seconds between batches
- **Model**: gpt-4o-mini

### Output

- **Enriched Relationships**: Saved to `Output/enriched_relationships.csv`
- **Logs**: Saved to `relationship_enricher.log`
- **Progress**: Continuously updated throughout execution

## File Structure

```
.
├── Input/
│   ├── concepts_06_07_better.csv      # Input concepts
│   └── relationships_06_06_better.csv # Existing relationships
├── Output/
│   └── enriched_relationships.csv     # Output with new relationships
├── relationship_enricher.py           # Main script
├── requirements.txt                   # Dependencies
├── README.md                         # This file
└── relationship_enricher.log         # Execution logs
```

## Customization

You can modify the script to:

1. **Change Model**: Update the `MODEL` variable in `main()`
2. **Adjust Batch Size**: Modify `batch_size` parameter
3. **Set Analysis Limits**: Change `max_pairs` parameter
4. **Control Rate Limiting**: Adjust `delay_between_batches`

## Safety Features

- **Duplicate Prevention**: Tracks existing relationships to avoid duplicates
- **Error Handling**: Graceful handling of API errors and parsing issues
- **Progress Recovery**: Can resume from where it left off if interrupted
- **Confidence Filtering**: Only accepts relationships with HIGH or MEDIUM confidence

## Monitoring

The script provides real-time feedback:
- Progress updates for each batch
- Statistics on API calls and new relationships found
- Error logging for debugging
- Final summary statistics

## Cost Management

To manage OpenAI API costs:
- Start with small `max_pairs` values for testing
- Use conservative `delay_between_batches` to avoid rate limits
- Monitor the `api_calls_made` statistic
- The script uses `gpt-4o-mini` which is cost-effective

## Troubleshooting

1. **API Key Issues**: Ensure `OPENAI_API_KEY` is set correctly
2. **File Not Found**: Check that input files exist in the correct locations
3. **Parsing Errors**: Check logs for AI response parsing issues
4. **Rate Limits**: Increase `delay_between_batches` if you hit rate limits

## Example Output

The enriched relationships CSV will contain:
- All original relationships
- New AI-identified relationships
- Source attribution for new relationships
- Confidence levels for new relationships 