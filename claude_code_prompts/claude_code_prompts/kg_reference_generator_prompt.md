# Claude Code Prompt: Generate Knowledge Graph Reference Documentation

You are tasked with creating comprehensive Knowledge Graph Reference documentation for the **Ecnetica** mathematics learning system. Transform raw knowledge graph data into structured reference documents that support both content generation and adaptive MCQ creation.

## Input Data Format

You will receive knowledge graph data in this format:
```
Chapter: [Chapter Name]
Section: [Section Name] (e.g., "Quadratic Functions", "Statistics", "Trigonometry")

Node Data:
Index | Topic | Chapter | Dependencies (index, weight)
------|-------|---------|-----------------------------
0     | [topic_name] | [chapter] | [(dest_index, weight), (dest_index, weight)]
1     | [topic_name] | [chapter] | [(dest_index, weight)]
...
```

## Required Output Structure

Generate a complete `.md` file following this EXACT structure:

```markdown
# [Section Name] Knowledge Graph Reference

This document provides the essential knowledge graph structure for content generation and MCQ creation for the [Section Name] section of the Ecnetica mathematics curriculum.

## Current Implementation: [Section Name] Knowledge Graph

### Node Structure
```
[Recreate the input table exactly as provided]
```

## Key Relationship Patterns

### Foundation → Application Flow
```
[Analyze dependencies to create ASCII flow diagram showing learning progression]
```

### Weight Interpretation
- **0.9-1.0**: Essential prerequisite (must know before attempting)
- **0.7-0.8**: Strong relationship (significant overlap)
- **0.5-0.6**: Moderate relationship (helpful but not essential)
- **0.3-0.4**: Weak relationship (minor connection)

## Cross-Section Dependencies

### [Current Section] → [Related Sections]
[Identify and list logical connections to other mathematics sections]

## Topic Classification

### Learning Levels
[Analyze nodes and classify into 3-4 progressive levels based on dependency complexity]

### Question Difficulty Mapping
- **Basic (0.2-0.4)**: [List foundation topics], direct application
- **Intermediate (0.4-0.7)**: [List core topics], problem-solving required
- **Advanced (0.7-0.9)**: [List advanced topics], conceptual understanding

## MCQ Topic Coverage Guidelines

### Efficient Question Design
Questions should aim to cover multiple related topics:

```
High-value combinations:
[Identify 3-4 pedagogically sound topic combinations based on dependency analysis]
```

### Prerequisites Calculation
For any topic, prerequisites include:
1. **Direct dependencies** (listed in node structure)
2. **Indirect dependencies** (dependencies of dependencies)
3. **Weighted by relationship strength** and path length

## System Integration Notes

### For Content Generation
- Structure theory sections to build from prerequisites to applications
- Ensure examples progress through dependency levels
- Connect topics naturally using relationship weights

### For MCQ Generation  
- Questions on topic X can assume mastery of all prerequisites
- Subtopic weights should reflect natural topic combinations
- Overall difficulty should match the topic's position in dependency graph

### For Adaptive Algorithms
- Use dependency weights for mastery propagation
- Higher out-degree topics (many dependencies) have higher importance
- Path lengths in graph determine learning sequence optimization

## Future Expansion Framework

As the knowledge graph grows to include all 18 sections:
- **Maintain consistent indexing** (add new topics at end)
- **Cross-reference section dependencies** ([current section] supports [dependent sections], etc.)
- **Weight recalibration** as new connections are discovered
- **Chapter clustering** for review optimization

This reference supports the comprehensive [Section Name] curriculum in the Ecnetica adaptive learning system.
```

## Analysis Guidelines

### **INTERNAL ANALYSIS INSTRUCTIONS (DO NOT INCLUDE IN OUTPUT):**

### 1. Dependency Flow Analysis
- **Identify starting points**: Nodes with no incoming dependencies (foundation topics)
- **Trace learning paths**: Follow dependency chains to create logical progression
- **Create ASCII flow**: Use arrows (→) and levels to show progression
- **Example format**: `Foundation Topic (X) → Core Method (Y) → Advanced Application (Z)`

### 2. Learning Level Classification
- **Foundation**: Nodes with 0-2 incoming dependencies, basic concepts
- **Core**: Nodes with 3-5 incoming dependencies, main methods
- **Advanced**: Nodes with 6+ incoming dependencies, complex applications
- **Adjust based on context**: Some topics may be advanced despite fewer dependencies

### 3. Cross-Section Connection Identification
Look for natural connections to other mathematics areas:
- **Algebra** → Functions, Coordinate Geometry, Calculus
- **Functions** → Calculus, Coordinate Geometry
- **Geometry** → Trigonometry, Coordinate Geometry
- **Statistics** → Probability, Data Analysis
- **Trigonometry** → Calculus, Physics applications

### 4. High-Value Topic Combinations
Identify groups of 2-4 related topics that:
- **Share strong dependencies** (weights 0.7+)
- **Form logical question sequences** (can be tested together)
- **Represent different skill levels** (basic → intermediate → advanced)
- **Support efficient learning** (cover multiple concepts per question)

### 5. Difficulty Classification Strategy
- **Basic**: Foundation topics, direct application, low dependency count
- **Intermediate**: Core methods, some problem-solving, moderate dependencies  
- **Advanced**: Complex concepts, high conceptual understanding, many dependencies

## Formatting Requirements

### ASCII Flow Diagrams
Use simple text-based diagrams:
```
Topic A (index) → Topic B (index) → Topic C (index)
                               ↓
                          Topic D (index) → Topic E (index)
```

### Topic References
- Always include topic index numbers for clarity
- Use exact topic names from the input data
- Maintain consistent formatting throughout

### Weight-Based Analysis
- Prioritize relationships with weights 0.6 and above for flow diagrams
- Use weights to determine strength of connections in combinations
- Consider cumulative weights for prerequisite chains

## Quality Standards

### Comprehensive Analysis
- **Complete coverage**: Address all major topics in the input data
- **Logical progression**: Learning flows should make pedagogical sense
- **Practical utility**: Guidance should support actual content and MCQ generation
- **Cross-section awareness**: Connect to broader mathematics curriculum

### Accurate Classification
- **Learning levels**: Should reflect actual cognitive complexity
- **Difficulty mapping**: Should align with typical student progression
- **Topic combinations**: Should be pedagogically sound and efficient

### Clear Integration Guidance
- **Content generation**: Provide actionable advice for structuring educational content
- **MCQ creation**: Offer specific guidance for question design and topic coverage
- **Adaptive algorithms**: Support intelligent question selection and mastery tracking

### Professional Documentation
- **Consistent formatting**: Follow the established template exactly
- **Clear language**: Accessible to both technical and educational teams
- **Structured organization**: Easy to navigate and reference
- **Future-focused**: Consider scalability and expansion

Generate knowledge graph reference documentation that serves as the authoritative guide for educational content creation and adaptive assessment design for the specified mathematics section.