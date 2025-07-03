# Claude Code Prompt: Generate Adaptive MCQs for Ecnetica

You are tasked with generating intelligent, adaptive Multiple Choice Questions for the **Ecnetica** mathematics learning system. These MCQs integrate with a sophisticated knowledge graph and adaptive learning algorithm that optimizes student learning paths.

## Knowledge Graph Context

### Topic Dependencies (Quadratic Functions Example)
```
Topic: "using quadratic formula" (index: 15)
Dependencies: 
- "factorization by inspection for a=1" (weight: 0.6)
- "quadratic formula derivation" (weight: 0.8) 
- "form of quadratic equations" (weight: 0.8)

Leads to:
- "discriminant" (weight: 0.7)
- "nature of roots" (weight: 0.8)
```

### Dependency Principles
- **Prerequisites**: Topics student must know before attempting this question
- **Subtopics**: Related topics covered within the question (excluding direct prerequisites)
- **Weights**: Strength of relationship (0.0-1.0, where 1.0 = essential dependency)

## MCQ Structure Requirements

### Core MCQ Format
```python
{
    "text": "[Question with LaTeX: \\(equation\\)]",
    "options": ["\\(option1\\)", "\\(option2\\)", "\\(option3\\)", "\\(option4\\)"],
    "correctIndex": [0-3],
    "option_explanations": [
        "Correct! [Explanation emphasizing theory]",
        "Incorrect. [Common mistake explanation + correct method]",
        "Incorrect. [Why this is wrong + correct approach]", 
        "Incorrect. [Error identification + correct solution]"
    ],
    "main_topic_index": [number],
    "chapter": "[chapter_name]",
    "subtopic_weights": {
        "[main_topic_index]": 0.6,
        "[related_topic_index]": 0.2,
        "[another_topic_index]": 0.2
    },
    "difficulty_breakdown": {
        "conceptual": [0.0-1.0],
        "procedural": [0.0-1.0], 
        "problem_solving": [0.0-1.0],
        "communication": [0.0-1.0],
        "memory": [0.0-1.0],
        "spatial": [0.0-1.0]
    },
    "id": "[auto-generated]"
}
```

## Six-Dimensional Difficulty Framework

### 1. Conceptual Understanding (0.0-1.0)
- **0.0-0.3**: Basic recall, definitions
- **0.4-0.7**: Understanding relationships, applying concepts
- **0.8-1.0**: Deep understanding, explaining why concepts work

### 2. Procedural Fluency (0.0-1.0)
- **0.0-0.3**: Simple arithmetic, basic substitution
- **0.4-0.7**: Multi-step calculations, algebraic manipulation
- **0.8-1.0**: Complex calculations, advanced algebraic techniques

### 3. Problem Solving (0.0-1.0)
- **0.0-0.3**: Direct application of known methods
- **0.4-0.7**: Strategy selection, multi-step reasoning
- **0.8-1.0**: Unfamiliar problems, creative problem-solving

### 4. Mathematical Communication (0.0-1.0)
- **0.0-0.3**: Plain language, familiar terminology
- **0.4-0.7**: Some mathematical notation and terminology
- **0.8-1.0**: Formal mathematical language, complex notation

### 5. Memory (0.0-1.0)
- **0.0-0.3**: Information provided or easily recalled
- **0.4-0.7**: Standard formulas and procedures
- **0.8-1.0**: Complex formulas, advanced theorems

### 6. Spatial Reasoning (0.0-1.0)
- **0.0-0.3**: No visual/spatial component
- **0.4-0.7**: Basic graphical interpretation
- **0.8-1.0**: Complex visualization, 3D reasoning

## Question Design Principles

### Topic Coverage Strategy
1. **Main Topic** (highest weight): The primary concept being assessed
2. **Subtopics** (weighted): Additional concepts naturally included
3. **Prerequisites** (calculated): Foundation topics assumed known

### Example Topic Weightings
```javascript
// Quadratic Formula question covering discriminant
subtopic_weights: {
    15: 0.6,  // "using quadratic formula" (main topic)
    17: 0.3,  // "discriminant" 
    16: 0.1   // "nature of roots"
}
// Note: Prerequisites (factorization, etc.) calculated automatically
```

### Difficulty Targeting
- **Questions should span difficulty levels**: Basic (0.2-0.4), Intermediate (0.4-0.7), Advanced (0.7-0.9)
- **Overall difficulty** = average of six dimensions
- **Difficulty matching**: Questions should slightly challenge student's current mastery level

## Adaptive Learning Integration

### Question Selection Context
Questions are selected by algorithms that consider:
- **Student mastery levels** for each topic
- **Topic dependencies** and prerequisites
- **Coverage optimization** (maximum learning per question)
- **Spaced repetition** scheduling

### Question Quality for Algorithms
- **Clear topic boundaries**: Main topic should be unambiguous
- **Balanced coverage**: Subtopic weights should sum to 1.0
- **Mistake targeting**: Incorrect options should represent common errors
- **Scaffold potential**: Questions should support learning progression

## Common Mistake Categories

### For Incorrect Options
1. **Calculation Errors**: Sign mistakes, arithmetic errors
2. **Conceptual Confusion**: Mixing up similar concepts
3. **Method Errors**: Using wrong formula or approach
4. **Notation Mistakes**: Misinterpreting mathematical symbols

### Option Distribution Strategy
- **Correct answer**: Evenly distributed across positions (A, B, C, D)
- **Plausible distractors**: Based on actual student errors
- **Graduated difficulty**: Some obviously wrong, others subtle mistakes

## MCQ Generation Examples

### Basic Level Example (Overall difficulty: 0.3)
```javascript
{
    "text": "What is the standard form of a quadratic equation?",
    "difficulty_breakdown": {
        "conceptual": 0.3, "procedural": 0.0, "problem_solving": 0.1,
        "communication": 0.4, "memory": 0.6, "spatial": 0.0
    }
    // Tests basic recall with some mathematical communication
}
```

### Advanced Level Example (Overall difficulty: 0.8)
```javascript
{
    "text": "Given that the quadratic equation \\(kx^2 + (k-3)x + 1 = 0\\) has equal roots, find the value(s) of \\(k\\).",
    "difficulty_breakdown": {
        "conceptual": 0.8, "procedural": 0.7, "problem_solving": 0.9,
        "communication": 0.7, "memory": 0.6, "spatial": 0.0
    }
    // Requires deep understanding of discriminant and solving complex equations
}
```

## Quality Standards

### Mathematical Accuracy
- **Precise LaTeX**: All mathematical notation properly formatted
- **Verified solutions**: Correct answers mathematically confirmed
- **Consistent notation**: Standard mathematical conventions throughout

### Educational Effectiveness
- **Clear progression**: From basic to advanced understanding
- **Meaningful assessment**: Questions test genuine understanding
- **Learning support**: Explanations that teach, not just correct

### System Integration
- **Unique identification**: Each MCQ has proper ID for tracking
- **Dependency accuracy**: Topic relationships correctly specified
- **Algorithm compatibility**: Structure supports adaptive selection

## Technical Requirements

- **LaTeX formatting**: Use \\( \\) for inline math, \\[ \\] for display math
- **JSON structure**: Proper formatting for system integration
- **Weight validation**: Subtopic weights must sum to 1.0
- **Difficulty consistency**: All six dimensions must be specified

## Generation Workflow

1. **Identify main topic** and its knowledge graph position
2. **Determine subtopics** naturally covered in question
3. **Set appropriate difficulty** for target student level
4. **Design question stem** testing core understanding
5. **Create option set** with strategic distractors
6. **Write explanations** that support learning
7. **Validate weights** and technical requirements

Generate MCQs that seamlessly integrate with the adaptive learning system while providing meaningful, progressive mathematical assessment for Leaving Certificate students.