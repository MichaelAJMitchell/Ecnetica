# Ecnetica Knowledge Graph Reference

This document provides the essential knowledge graph structure for content generation and MCQ creation. It will expand to cover all 18 mathematics sections as the system scales.

## Current Implementation: Quadratic Functions Knowledge Graph

### Node Structure
```
Index | Topic | Chapter | Dependencies (index, weight)
------|-------|---------|-----------------------------
0     | solving linear equations | algebra | [(6,0.5), (14,0.8), (15,0.6)]
1     | linear equations in standard form | algebra | [(0,0.3), (2,0.4)]
2     | form of quadratic equations | algebra | [(5,0.9), (6,0.7), (9,0.6), (10,0.8), (12,0.6), (14,0.7), (15,0.8), (17,0.6)]
3     | expanding brackets | algebra | [(0,0.7), (9,0.8), (14,0.2)]
4     | substitution | algebra | [(5,0.9), (11,0.3), (12,0.3), (13,0.4), (15,0.9), (17,0.8)]
5     | using substitution to make equations in quadratic equations | algebra | [(9,0.5), (11,0.6), (12,0.7), (13,0.5)]
6     | factorisation by inspection for a=1 | algebra | [(7,0.8), (12,0.9)]
7     | factorisation by inspection for a≠1 | algebra | [(12,0.9)]
8     | basic coordinate geometry | geometry | [(10,0.8), (11,0.6), (13,0.7)]
9     | writing quadratics in completed square form | algebra | [(11,0.9), (13,0.8)]
10    | graph of quadratics | algebra | [(11,0.7), (12,0.5), (13,0.6)]
11    | vertex of parabola | algebra | []
12    | x-intercept/roots of quadratic equations | algebra | [(15,0.4), (16,0.6), (17,0.5)]
13    | interpreting completed square form | algebra | []
14    | quadratic formula derivation | algebra | [(15,0.9)]
15    | using quadratic formula | algebra | [(16,0.8), (17,0.7)]
16    | nature of roots | algebra | []
17    | discriminant | algebra | [(16,0.7)]
```

## Key Relationship Patterns

### Foundation → Application Flow
```
Linear Equations (0) → Quadratic Forms (2) → Factorization (6,7) → Quadratic Formula (15)
                                        ↓
                    Completing Square (9) → Vertex Form (11) → Interpretation (13)
                                        ↓
                    Discriminant (17) → Nature of Roots (16)
```

### Weight Interpretation
- **0.9-1.0**: Essential prerequisite (must know before attempting)
- **0.7-0.8**: Strong relationship (significant overlap)
- **0.5-0.6**: Moderate relationship (helpful but not essential)
- **0.3-0.4**: Weak relationship (minor connection)

## Cross-Section Dependencies (Future Expansion)

### Algebra → Functions
- Quadratic equations → Quadratic functions
- Factorization → Function zeros
- Completing square → Function transformations

### Functions → Calculus  
- Function behavior → Limits
- Quadratic functions → Basic differentiation
- Function transformations → Derivative rules

### Algebra → Coordinate Geometry
- Linear equations → Line equations
- Quadratic equations → Parabola equations
- Solving systems → Intersection points

### Geometry → Trigonometry
- Coordinate geometry → Unit circle
- Right triangles → Trigonometric ratios
- Circle equations → Trigonometric functions

## Topic Classification

### Learning Levels
1. **Foundation** (0-4): Basic algebra and equation solving
2. **Core** (5-10): Quadratic forms and graphical representation  
3. **Advanced** (11-17): Analysis and interpretation of quadratic behavior

### Question Difficulty Mapping
- **Basic (0.2-0.4)**: Foundation topics, direct application
- **Intermediate (0.4-0.7)**: Core topics, problem-solving required
- **Advanced (0.7-0.9)**: Advanced topics, conceptual understanding

## MCQ Topic Coverage Guidelines

### Efficient Question Design
Questions should aim to cover multiple related topics:

```
High-value combinations:
- Quadratic formula (15) + Discriminant (17) + Nature of roots (16)
- Factorization (6,7) + Roots (12) + Quadratic formula (15)  
- Completing square (9) + Vertex form (11) + Interpretation (13)
- Coordinate geometry (8) + Quadratic graphs (10) + Vertex (11)
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
- **Cross-reference section dependencies** (algebra supports calculus, etc.)
- **Weight recalibration** as new connections are discovered
- **Chapter clustering** for review optimization

This reference will be updated as the knowledge graph expands to cover the complete Leaving Certificate curriculum.