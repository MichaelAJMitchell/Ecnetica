# Claude Code Prompt: Replicating Jupyter Book Mathematics Content Structure

You are tasked with creating new mathematical content for a Jupyter Book that follows the exact structure, format, and pedagogical approach of an existing Leaving Certificate Higher Level Mathematics resource. This is a comprehensive educational resource being built for Irish students.

## Project Context
- **Project Name**: Ecnetica - Free Leaving Cert Mathematics Resource
- **Format**: Jupyter Book with MyST markdown
- **Target Audience**: Leaving Certificate Higher Level Mathematics students
- **Existing Structure**: Comprehensive coverage from Number Systems through Statistics and Probability

## Content Structure Requirements

### File Organization
- All content files go in `content/[topic]/[specific_topic].md`
- Follow the hierarchical structure defined in `_toc.yml`
- Use descriptive, lowercase filenames with underscores (e.g., `quadratic_equations.md`)

### Standard Content Template

Each mathematics topic file must include these sections in order:

```markdown
# [Topic Title]

<iframe 
    src="[GOOGLE_DRIVE_PREVIEW_URL]" 
    width="100%" 
    height="480" 
    frameborder="0" 
    allowfullscreen>
</iframe>

## [Previous Concept] Revision (if applicable)

### Theory
[Brief review of prerequisite concepts]

### Application
[Examples of prerequisite applications]

## [Main Topic Name]

### Theory
[Core mathematical concepts, definitions, formulas]

#### Interactive Visualization: [Descriptive Name]
[Include interactive math visualizations using the established pattern]

### Application
#### Examples
[Worked examples with step-by-step solutions]

#### Multiple Choice Questions
[MCQ quiz section with explanations]

#### Sector Specific Questions: [Topic] Applications
[Real-world applications across different fields]

### Key Takeaways
[Important summary points in a callout box]
```

## Technical Implementation Patterns

### Mathematical Notation
- Use LaTeX notation with double dollar signs for display math: `$$equation$$`
- Use single dollar signs for inline math: `$x^2$`
- For functions in interactive components, use JavaScript-compatible notation

### Interactive Components

#### Math Visualizations
```html
<div id="[unique-container-id]" class="visualization-container" style="height: 500px;"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    MathVisualizer.createGraphFromDescription('[container-id]', {
        boundingBox: [-5, 5, 5, -5],
        theme: 'light',
        useSequentialColors: true,
        
        infoBox: {
            title: "[Function Description]",
            lines: [
                {text: "[Formula]", dynamic: false},
                {text: "[Parameter]: ${parameter}", dynamic: true},
                // Add more parameter displays
            ],
            position: {top: 55, left: 20}
        },
        
        parametrizedFunctions: [
            {
                expression: '[mathematical_expression]',
                title: '[Function Explorer Title]',
                parameters: {
                    [param]: { min: [min], max: [max], value: [default], step: [step] }
                },
                features: ['zeros', 'extrema'] // As appropriate
            }
        ]
    });
});
</script>
```

#### Multiple Choice Questions
```html
<div id="[topic]-mcq" class="quiz-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "[Quiz Title]",
        questions: [
            {
                text: "[Question with LaTeX: \\(equation\\)]",
                options: [
                    "\\(option1\\)",
                    "\\(option2\\)",
                    "\\(option3\\)",
                    "\\(option4\\)"
                ],
                correctIndex: [0-3],
                explanation: "[Detailed explanation with LaTeX]",
                difficulty: "[Basic/Intermediate/Advanced]"
            }
        ]
    };
    
    MCQQuiz.create('[topic]-mcq', quizData);
});
</script>
```

#### Sector-Specific Applications
```html
<div id="[topic]-identity-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const [topic]Content = {
        "title": "[Topic]: [Subtitle]",
        "intro_content": `
            <p>[Introduction paragraph with LaTeX: \\(equations\\)]</p>
        `,
        "questions": [
            {
                "category": "[scientific/engineering/financial/creative]",
                "title": "[Field]: [Specific Application]",
                "content": `[Problem statement with LaTeX]`,
                "answer": `[Detailed solution with LaTeX]`
            }
        ]
    };
    
    MathQuestionModule.render([topic]Content, '[topic]-identity-container');
});
</script>
```

### MyST Markdown Features

#### Callout Boxes
```markdown
```{tip}
Helpful tips and tricks for students
```

```{warning}
Common mistakes and important cautions
```

```{important}
Key concepts that must be understood
```

```{seealso}
References to related topics and further reading
```

```{note}
Additional information and clarifications
```
```

## Pedagogical Approach

### Content Progression
1. **Gentle Introduction**: Start with familiar concepts
2. **Build Complexity**: Gradually introduce new ideas
3. **Multiple Representations**: Show algebraic, graphical, and real-world connections
4. **Practice Opportunities**: Include varied question types
5. **Real-World Relevance**: Connect to practical applications

### Writing Style
- **Clear and Accessible**: Use student-friendly language
- **Step-by-Step**: Break complex procedures into manageable steps
- **Encouraging**: Build confidence through achievable examples
- **Comprehensive**: Cover all aspects students need for Leaving Cert

### Example Quality Standards
- Work through solutions completely
- Show intermediate steps clearly
- Verify answers when possible
- Explain the reasoning behind each step
- Connect to broader mathematical concepts

## Sector-Specific Applications Structure

Include applications from these four categories:
1. **Scientific**: Physics, Chemistry, Biology, Environmental Science
2. **Engineering**: Civil, Mechanical, Electrical, Computer Engineering
3. **Financial**: Economics, Business, Banking, Investment
4. **Creative**: Art, Music, Photography, Architecture, Design

Each application should:
- Present a realistic scenario
- Use authentic data and context
- Require genuine mathematical problem-solving
- Include comprehensive worked solutions
- Connect mathematics to career paths

## Interactive Components Standards

### Math Visualizations
- Use appropriate coordinate systems and scales
- Include clear parameter controls
- Display key information dynamically
- Highlight important features (zeros, extrema, etc.)
- Use consistent color schemes

### Quizzes
- Include 3-4 questions per section
- Vary difficulty levels (Basic/Intermediate/Advanced)
- Provide detailed explanations for all answers
- Use proper LaTeX formatting
- Test understanding, not just memorization

## File Naming and Organization

### Content Files
- Use descriptive, lowercase names with underscores
- Example: `quadratic_formula.md`, `trigonometric_identities.md`
- Place in appropriate subdirectories: `content/algebra/quadratic_formula.md`

### Asset References
- Reference interactive components by unique IDs
- Use consistent naming patterns
- Ensure all container IDs are unique across the entire book

## Quality Checklist

Before completing any content file, verify:

- [ ] All LaTeX renders correctly
- [ ] Interactive components have unique IDs
- [ ] MCQ explanations are thorough
- [ ] Sector applications are realistic and well-solved
- [ ] Callout boxes are used appropriately
- [ ] Mathematical notation is consistent
- [ ] Examples build in logical progression
- [ ] Key takeaways summarize essential points
- [ ] Content aligns with Leaving Cert curriculum
- [ ] File is properly placed in directory structure

## Example Output Request

When asked to create new content, produce a complete `.md` file that:
1. Follows this exact structure and format
2. Includes all required interactive components
3. Provides comprehensive mathematical coverage
4. Uses the established pedagogical approach
5. Maintains consistency with existing content quality

Always create content that would seamlessly integrate with the existing Jupyter Book and provide the same high-quality educational experience for Leaving Certificate students.