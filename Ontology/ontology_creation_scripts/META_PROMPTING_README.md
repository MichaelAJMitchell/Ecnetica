# Meta-Prompting System for Knowledge Graph Extraction

## Overview

The Meta-Prompting System is an advanced AI-powered approach that continuously improves the quality of knowledge graph extraction by:

1. **Quality Assessment**: Automatically evaluating the quality of extracted concepts and relationships
2. **Prompt Refinement**: Using AI to improve extraction prompts based on quality feedback
3. **Adaptive Management**: Automatically selecting the best-performing prompts
4. **Performance Tracking**: Monitoring and analyzing system performance over time

## System Components

### 1. Quality Assessor (`quality_assessor.py`)

**Purpose**: Evaluates the quality of extracted concepts and relationships using AI

**Features**:
- Scores extraction quality on 5 dimensions (1-10 scale)
- Provides specific feedback and improvement suggestions
- Handles malformed AI responses gracefully
- Stores quality metrics for analysis

**Quality Dimensions**:
- **Concept Granularity**: Are concepts specific enough?
- **Concept Completeness**: Are important concepts missing?
- **Relationship Accuracy**: Are prerequisite relationships logical?
- **Relationship Completeness**: Are key relationships missing?
- **Overall Quality**: How well does the extraction represent the content?

### 2. Prompt Refiner (`prompt_refiner.py`)

**Purpose**: Uses quality feedback to automatically improve extraction prompts

**Features**:
- Analyzes quality assessment results
- Generates improved prompts using AI
- Maintains refinement history
- Tracks performance improvements

**Refinement Process**:
1. Analyze quality feedback
2. Identify common issues
3. Generate prompt improvements
4. Test and validate changes

### 3. Adaptive Prompt Manager (`adaptive_prompt_manager.py`)

**Purpose**: Manages prompt versions and automatically selects the best performing ones

**Features**:
- Tracks prompt performance over time
- Automatically triggers refinement when needed
- Maintains prompt version history
- Provides performance analytics

**Refinement Triggers**:
- Low recent performance (< 6.0/10)
- Significant performance decline
- Extended periods without improvement

### 4. Meta-Prompting Dashboard (`meta_prompting_dashboard.py`)

**Purpose**: Interactive interface for monitoring and analyzing system performance

**Features**:
- Real-time performance metrics
- Quality trend analysis
- Prompt refinement history
- Improvement suggestions
- Performance report export

## Usage

### Basic Usage

```bash
# Process files with quality assessment
python main.py --file ../ontology_source_materials/textbook.md

# Process entire folder with quality tracking
python main.py --input-folder ../ontology_source_materials/

# Launch interactive dashboard
python main.py --dashboard

# Generate quality report
python main.py --quality-report

# Save quality metrics
python main.py --file ../ontology_source_materials/textbook.md --save-quality-metrics quality_data.json

# Save prompt performance data
python main.py --file ../ontology_source_materials/textbook.md --save-prompt-performance prompt_data.json
```

### Dashboard Usage

```bash
python meta_prompting_dashboard.py
```

The dashboard provides:
- **Overall Summary**: System performance overview
- **Quality Trends**: Performance changes over time
- **Prompt Refinement History**: Track of prompt improvements
- **Improvement Suggestions**: AI-generated recommendations
- **Performance Reports**: Exportable analysis data

### Testing the System

```bash
# Run comprehensive tests
python test_meta_prompting.py

# Test individual components
python -c "from quality_assessor import QualityAssessor; print('Quality Assessor imported successfully')"
python -c "from prompt_refiner import PromptRefiner; print('Prompt Refiner imported successfully')"
python -c "from adaptive_prompt_manager import AdaptivePromptManager; print('Adaptive Prompt Manager imported successfully')"
```

## How It Works

### 1. Extraction Process with Quality Assessment

```
Document → Text Extraction → AI Processing → Quality Assessment → Feedback Loop
    ↓              ↓              ↓              ↓              ↓
  Chunking    Multi-Stage    Concepts &      AI Scoring    Prompt
  Strategy    Extraction    Relationships   (1-10 scale)   Refinement
```

### 2. Quality Assessment Flow

1. **Extract Content**: Process document chunks
2. **AI Assessment**: Evaluate extraction quality
3. **Score Calculation**: Generate 5-dimensional scores
4. **Feedback Generation**: Provide improvement suggestions
5. **Performance Recording**: Store metrics for analysis

### 3. Prompt Refinement Flow

1. **Monitor Performance**: Track quality scores over time
2. **Identify Issues**: Detect performance problems
3. **Generate Improvements**: Use AI to refine prompts
4. **Test Changes**: Validate improvements
5. **Deploy Updates**: Automatically update prompt versions

### 4. Adaptive Management Flow

1. **Performance Tracking**: Monitor all extractions
2. **Trend Analysis**: Identify performance patterns
3. **Automatic Refinement**: Trigger improvements when needed
4. **Version Management**: Maintain prompt history
5. **Optimization**: Continuously improve system performance

## Configuration

### Environment Variables

```bash
OPENAI_API_KEY=your_api_key_here
```

### Quality Thresholds

The system automatically refines prompts when:
- Recent performance drops below 6.0/10
- Performance declines by more than 1.0 point
- No improvements for extended periods

### Data Storage

Quality metrics and prompt performance data are stored in:
- `quality_metrics.json`: Quality assessment results
- `prompt_registry.json`: Prompt versions and performance

## Benefits

### 1. Continuous Improvement
- Prompts automatically improve over time
- Quality consistently increases
- Reduced manual prompt engineering

### 2. Quality Assurance
- Real-time quality monitoring
- Automatic issue detection
- Consistent extraction standards

### 3. Performance Optimization
- Best prompts automatically selected
- Performance trends tracked
- Optimization opportunities identified

### 4. Transparency
- Full audit trail of changes
- Performance history maintained
- Improvement suggestions documented

## Monitoring and Analysis

### Key Metrics to Watch

1. **Quality Scores**: Track improvement over time
2. **Refinement Frequency**: How often prompts are updated
3. **Performance Trends**: Identify patterns and issues
4. **Improvement Suggestions**: Common areas for enhancement

### Dashboard Features

- **Real-time Monitoring**: Live performance updates
- **Trend Analysis**: Historical performance patterns
- **Issue Detection**: Automatic problem identification
- **Recommendation Engine**: AI-powered improvement suggestions

## Troubleshooting

### Common Issues

1. **Quality Assessment Failures**
   - Check OpenAI API key
   - Verify API rate limits
   - Review error logs

2. **Prompt Refinement Issues**
   - Ensure quality data exists
   - Check prompt format compatibility
   - Verify AI model availability

3. **Performance Tracking Problems**
   - Check file permissions
   - Verify data format
   - Review system resources

### Debug Mode

Enable detailed logging by setting:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Future Enhancements

### Planned Features

1. **Cross-Document Validation**: Compare concepts across multiple sources
2. **Advanced Analytics**: Machine learning-based performance prediction
3. **Custom Quality Metrics**: User-defined assessment criteria
4. **Integration APIs**: Connect with external quality systems

### Research Areas

1. **Prompt Optimization**: Advanced prompt engineering techniques
2. **Quality Prediction**: ML models for quality estimation
3. **Automated Testing**: Self-validating extraction systems
4. **Performance Benchmarking**: Industry-standard quality metrics

## Support

For issues or questions:
1. Check the test suite: `python test_meta_prompting.py`
2. Review error logs and quality metrics
3. Use the dashboard for system analysis
4. Examine prompt refinement history

## Conclusion

The Meta-Prompting System represents a significant advancement in knowledge graph extraction, providing:

- **Automated Quality Control**: Continuous monitoring and improvement
- **Intelligent Optimization**: AI-powered prompt refinement
- **Performance Transparency**: Full visibility into system behavior
- **Scalable Architecture**: Designed for production use

This system transforms static extraction processes into dynamic, learning systems that continuously improve extraction quality through intelligent feedback loops and automated optimization. 