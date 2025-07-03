# Claude Code Prompt: Create Ecnetica Mathematics Content

You are tasked with creating content for the **Ecnetica** Jupyter Book - a comprehensive Leaving Certificate Higher Level Mathematics resource for Irish students. Create complete `.md` files following the exact structure, format, and pedagogical approach shown in the reference template.

## Required Structure (in this exact order):

1. **Title**: `# [Topic Name]`

2. **Video Section** (OMIT by default):
```markdown
<!-- OMIT video section unless user specifically requests it -->
```

3. **Prerequisite Review Section** (if applicable):
```markdown
## [Previous Topic] Revision

### Theory
[Brief review with LaTeX equations using $$display$$ and $inline$]

### Application
#### Examples
[1-2 worked examples]

#### Interactive Visualization: [Name]
[Complete interactive visualization implementation]

#### Multiple Choice Questions
[MCQ section with explanations]
```

4. **Main Content Section**:
```markdown
## [Main Topic Name]

### Theory

[Core concepts with LaTeX covering all essential elements for comprehensive application work]

**INTERNAL GUIDELINE (DO NOT INCLUDE IN OUTPUT)**: The theory section must provide comprehensive coverage that enables diverse application examples across all four sectors (scientific, engineering, financial, creative). Include: foundational definitions with clear mathematical notation, key formulas and relationships with step-by-step derivations where appropriate, properties and characteristics that students need for problem-solving, multiple solution methods when applicable (algebraic, graphical, numerical), common variations and special cases that appear in real-world applications, and connections to prerequisite concepts and preview of advanced applications.

**WRITING STYLE GUIDELINE (DO NOT INCLUDE IN OUTPUT)**: Write with the voice of an engaging, supportive teacher. Use conversational language that connects with students. Include phrases like "Let's explore...", "Notice how...", "This is important because...", "Here's a helpful way to think about it...", "Before we dive into...", "It's worth taking a moment to..." Make concepts feel accessible and interesting rather than dry or intimidating. Explain the 'why' behind mathematical concepts, not just the 'what'. Use analogies and real-world connections when appropriate.

**KNOWLEDGE GRAPH AWARENESS (DO NOT INCLUDE IN OUTPUT)**: Consider topic dependencies when structuring content. Build from prerequisite concepts (mentioned naturally) to main topic to applications. For example: factorization → quadratic formula → discriminant → nature of roots. Ensure theory coverage supports both simpler and more complex question types that may cover multiple related topics.

#### Interactive Visualization: [Name]
[Complete interactive visualization implementation]

### Application

#### Examples

**CRITICAL**: Follow this EXACT formatting pattern for examples:

**WRITING STYLE FOR EXAMPLES (DO NOT INCLUDE IN OUTPUT)**: Write examples with encouraging, step-by-step teacher guidance. Use phrases like "Let's solve this step by step", "Here's how we approach this", "Notice what happens when...", "This might look tricky at first, but...", "The key insight here is...". Make each step feel logical and achievable.

##### Example 1: [Descriptive Title]
[Problem statement with engaging introduction - e.g., "Let's work through this problem step by step:" or "Here's a typical question you might encounter:"]

**Method 1: [Method Description]**

$[equation] \quad \text{([explanation with teaching voice])}$

$[next step] \quad \text{([why we do this step])}$

$[final step] \quad \text{([what this tells us])}$

**Method 2: [Alternative Method]** (if applicable)

$[equation] \quad \text{([comparison to Method 1])}$

$[next step] \quad \text{([advantage of this approach])}$

##### Example 2: [Descriptive Title]
[Problem statement with connection to previous example]

[Same formatting pattern with display equations and engaging descriptions]

##### Example 3: [Descriptive Title]
[Problem statement that builds complexity]

[Same formatting pattern with display equations and supportive explanations]

#### Multiple Choice Questions
[MCQ section - use simple format for basic assessment]

#### Sector Specific Questions: [Topic] Applications
[4 categories: scientific, engineering, financial, creative]

### Key Takeaways
```{important}
[Numbered list of key points]
```
```

## Interactive Visualization Placeholder

### For All Sections:
```html
<div id="[unique-id]-container" class="visualization-container" style="height: 500px; display: flex; align-items: center; justify-content: center; background-color: #f8f9fa; border: 2px dashed #dee2e6; border-radius: 8px;">
    <div style="text-align: center; color: #6c757d; font-size: 18px; font-weight: 500;">
        Interactive Graph
        <div style="font-size: 14px; margin-top: 8px; font-weight: normal;">
            [Topic-specific visualization will be implemented here]
        </div>
    </div>
</div>
```

## Standard Components

### Multiple Choice Questions (Basic Format):
```html
<div id="[topic]-mcq" class="quiz-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "[Topic] Practice Questions",
        questions: [
            {
                text: "[Question with LaTeX: \\(equation\\)]",
                options: ["\\(option1\\)", "\\(option2\\)", "\\(option3\\)", "\\(option4\\)"],
                correctIndex: 0,
                explanation: "[Detailed explanation with LaTeX]",
                difficulty: "Basic"
            }
        ]
    };
    MCQQuiz.create('[topic]-mcq', quizData);
});
</script>
```

### Sector Applications:
```html
<div id="[topic]-identity-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const [topic]Content = {
        "title": "[Topic]: Applications",
        "intro_content": `<p>[Introduction with \\(LaTeX\\)]</p>`,
        "questions": [
            {
                "category": "scientific",
                "title": "[Field]: [Application]",
                "content": `[Problem with LaTeX]`,
                "answer": `[Detailed solution]`
            },
            {
                "category": "engineering",
                "title": "[Field]: [Application]", 
                "content": `[Problem with LaTeX]`,
                "answer": `[Detailed solution]`
            },
            {
                "category": "financial",
                "title": "[Field]: [Application]",
                "content": `[Problem with LaTeX]`,
                "answer": `[Detailed solution]`
            },
            {
                "category": "creative",
                "title": "[Field]: [Application]",
                "content": `[Problem with LaTeX]`,
                "answer": `[Detailed solution]`
            }
        ]
    };
    MathQuestionModule.render([topic]Content, '[topic]-identity-container');
});
</script>
```

## Formatting Requirements

**Critical Formatting Rules:**
- **Consistent headings:** Use proper heading hierarchy (### for main concepts, **bold** for subsections)
- **Uniform spacing:** Single line break between concepts, double line break before new major sections
- **Mathematical notation:** All formulas must use consistent LaTeX formatting
- **Text flow:** Avoid awkward line breaks or spacing within sentences
- **Font consistency:** Use standard markdown formatting throughout
- **Bullet points:** Each bullet point must be on its own separate line with proper line breaks
- **Formula presentation:** Display important formulas on separate lines with proper LaTeX
- **NO INLINE BULLET POINTS:** Never combine multiple bullet points on the same line separated by bullets (•)

## Technical Requirements

- **LaTeX:** Use $$display$$ and $inline$ notation
- **Unique IDs:** Base on topic name (e.g., 'quadratic-functions-container')
- **No placeholders:** All code must be complete and functional
- **Exact formatting:** Follow the example spacing and structure precisely
- **MyST callouts:** Use ```{important}, ```{tip}, ```{warning}, ```{note}
- **File naming:** lowercase with underscores (e.g., quadratic_functions.md)

## Quality Standards

- **Engaging Teaching Voice:** Write with personality and warmth like a supportive teacher
- **Complete step-by-step solutions:** Show all working steps with encouraging explanations
- **Proper mathematical notation:** Throughout with clear reasoning for each step
- **Functional interactive visualizations:** With appropriate placeholders
- **Real-world sector applications:** That connect meaningfully to student experiences
- **Leaving Cert curriculum alignment:** While maintaining accessibility and engagement
- **Consistent educational progression:** That builds confidence and understanding
- **Conversational tone:** Use "Let's explore...", "Notice how...", "Here's why..." style language
- **Student-centered explanations:** Focus on helping students understand the 'why' not just the 'how'

Select the appropriate visualization template based on the mathematical content being covered. Always omit video sections unless specifically requested.