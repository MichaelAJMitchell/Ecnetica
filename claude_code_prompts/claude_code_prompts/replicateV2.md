# Claude Code Prompt: Create Ecnetica Mathematics Content

You are tasked with creating content for the **Ecnetica** Jupyter Book - a comprehensive Leaving Certificate Higher Level Mathematics resource for Irish students. Create complete `.md` files following the exact structure, format, and pedagogical approach shown in the reference template.

## Section Structure Requirements

**CRITICAL**: For comprehensive topics (like Quadratic Functions, Calculus, Statistics), break content into focused subsections rather than one massive section.

### Multi-Section Topic Breakdown

**INTERNAL STRUCTURE GUIDELINE (DO NOT INCLUDE IN OUTPUT)**: 

When creating content for complex topics, use this progressive structure:

**Individual Section Pattern:**
```markdown
## [Specific Method/Concept Name]

### Theory
[Focused theory for this specific concept]

#### Interactive Visualization: [Specific Name]
[Visualization for this concept]

### Application
#### Examples
[Examples specific to this method]

#### Multiple Choice Questions  
[MCQs testing this specific concept]

#### Sector Specific Questions: [Specific Concept] Applications
[Applications for this particular method]

### Key Takeaways
```{important}
[Key points for this specific concept]
```
```

**Topic Progression Examples:**

For **Quadratic Functions**, create separate sections:
1. ## Quadratic Equations and their Form
2. ## Factorizing Quadratic Equations by Inspection  
3. ## Graphical Solutions to Quadratic Equations
4. ## Deriving the Quadratic Formula
5. ## The Discriminant

For **Calculus**, create separate sections:
1. ## Limits and Continuity
2. ## Differentiation from First Principles
3. ## Differentiation Rules
4. ## Applications of Differentiation

**Section Dependencies**: Each section should build naturally on previous ones, referencing prior concepts where needed.

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

4. **Main Content Section(s)**:

**For Simple Topics** (use single main section):
```markdown
## [Main Topic Name]

### Theory
[Core concepts with LaTeX]

#### Interactive Visualization: [Name]
[Complete interactive visualization implementation]

### Application
[Examples, MCQs, Sector Applications]

### Key Takeaways
```{important}
[Key points]
```
```

**For Complex Topics** (use multiple focused sections):
```markdown
## [First Concept Name]

### Theory
[Focused theory for this specific concept]

#### Interactive Visualization: [Specific Name]  
[Visualization for this concept]

### Application
[Examples, MCQs, Applications specific to this concept]

### Key Takeaways
```{important}
[Key points for this concept]
```

## [Second Concept Name]

### Theory  
[Theory building on previous section]

#### Interactive Visualization: [Specific Name]
[Visualization for this new concept]

### Application
[Examples, MCQs, Applications for this concept]

### Key Takeaways
```{important}
[Key points for this concept]  
```

[Continue pattern for additional concepts...]
```

**DECISION CRITERIA (DO NOT INCLUDE IN OUTPUT)**: 
- **Single Section**: Simple topics with one main concept (e.g., "Linear Equations", "Circle Area")
- **Multiple Sections**: Complex topics with distinct methods or concepts (e.g., "Quadratic Functions", "Integration Techniques", "Statistical Analysis")

### Content Guidelines for Each Section:

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

**MANDATORY EXAMPLE FORMAT (MUST FOLLOW EXACTLY)**:

```markdown
##### Example N: [Descriptive Title]
Let's solve: [equation or problem statement]

**Method 1: [Method Name]**

$[equation] \quad \text{(explanation for this step)}$

$[next equation] \quad \text{(what we did and why)}$

$[final answer] \quad \text{(verification or insight)}$

**Method 2: [Alternative Method Name]** (if applicable)

$[equation] \quad \text{(explanation for this step)}$

$[next equation] \quad \text{(comparison to Method 1 or advantage)}$

$[final answer] \quad \text{(verification or insight)}$
```

**EXAMPLE FORMAT REQUIREMENTS**:
- Always start with "Let's solve:" or "Let's work through:" followed by the problem
- Use **Method 1:**, **Method 2:** etc. for different approaches
- Each mathematical step must use the format: $equation \quad \text{(explanation)}$
- Explanations in text() should be conversational and educational
- Include verification or insight in the final step
- Never use display math $...$, always use inline $...$ with \quad \text{}

**FORBIDDEN FORMATS**:
- ❌ Using **Step 1:**, **Step 2:** instead of **Method 1:**
- ❌ Starting with "Solve" instead of "Let's solve:"
- ❌ Using display math $equation$ without explanatory text
- ❌ Explanations outside the \text{} format
- ❌ Missing method names in headers

#### Multiple Choice Questions
[MCQ section - use simple format for basic assessment]

#### Sector Specific Questions: [Topic] Applications
[4 categories: scientific, engineering, financial, creative]

### Key Takeaways
```{important}
[Numbered list of key points specific to THIS section only]
```

## Pedagogical Elements Requirements

### Callout Boxes (MUST include throughout each section):

**MANDATORY DISTRIBUTION PER SECTION**:
- **```{tip}**: 1-2 per section for helpful strategies, shortcuts, or problem-solving approaches
- **```{warning}**: 1 per section for common mistakes, misconceptions, or pitfalls to avoid  
- **```{note}**: 1 per section for interesting connections, additional insights, or context
- **```{important}**: For crucial formulas, theorems, or concepts students must remember
- **```{seealso}**: For related topics, advanced extensions, or cross-references

**STRATEGIC PLACEMENT**:
- Place ```{tip} boxes after introducing methods or before complex examples
- Use ```{warning} boxes near common error-prone areas
- Include ```{note} or ```{seealso} boxes for enrichment and connections
- ```{important} boxes should highlight key formulas or breakthrough concepts

**EXAMPLE CALLOUT USAGE**:

```markdown
```{tip}
When factorizing quadratics, always check if there's a common factor first. This can simplify your work significantly!
```

```{warning}
Remember that when $a \neq 1$, factorizing becomes more complex. Consider using the quadratic formula for these cases unless the factors are obvious.
```

```{note}
This completing the square method is the foundation for deriving the quadratic formula. Understanding it deeply will help you in calculus when finding maxima and minima!
```

```{seealso}
The discriminant connects to the study of conic sections in coordinate geometry. A parabola's intersection with the x-axis is just one example of curve intersections.
```

```{important}
The quadratic formula $x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$ works for ALL quadratic equations and should be memorized.
```
```

### Key Takeaways Distribution:
- **CRITICAL**: Key Takeaways must appear at the end of EACH major ## section, not just at the file end
- **Content**: 4-6 numbered points specific to that section's content only
- **Format**: Always use ```{important} blocks  
- **Focus**: What students should remember from THIS specific section, not the entire topic

### Sector Applications Distribution:
- **EACH major ## section needs its own complete set of 4 sector applications**
- **No reuse**: Don't repeat applications across sections  
- **Method-specific**: Each application should specifically demonstrate that section's method/concept
- **Example**: Factorization section → problems that are best solved by factoring; Formula section → problems requiring the quadratic formula

### Minimum Pedagogical Element Count Per Section:
- 2-3 Callout boxes (mix of tip, warning, note, seealso)
- 1 Key Takeaways block with 4-6 points  
- 4 Sector applications (scientific, engineering, financial, creative)
- 2-3 Examples with proper formatting
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

- **LaTeX:** Use $display$ and $inline$ notation
- **Unique IDs:** Base on topic name (e.g., 'quadratic-functions-container')
- **No placeholders:** All code must be complete and functional
- **Exact formatting:** Follow the example spacing and structure precisely
- **MyST callouts:** Use ```{important}, ```{tip}, ```{warning}, ```{note}
- **File naming:** lowercase with underscores (e.g., quadratic_functions.md)
- **Section Organization:** For multi-section topics, create comprehensive single files with multiple ## sections rather than separate files for each concept

## Content Generation Strategy

**INTERNAL DECISION FRAMEWORK (DO NOT INCLUDE IN OUTPUT)**:

**When asked to create content for a topic, determine:**

1. **Is this a simple concept?** → Use single main section structure
   - Examples: "Linear Equations", "Circle Properties", "Basic Trigonometry"

2. **Is this a complex topic with multiple methods/concepts?** → Use multiple focused sections
   - Examples: "Quadratic Functions", "Differentiation", "Statistical Analysis"

3. **What are the logical subdivisions?** → Create ## sections for each major concept/method

4. **How do sections connect?** → Each section should reference and build on previous sections

**Progressive Building Pattern:**
- Section 1: Foundation concepts
- Section 2: Building on foundation with new method
- Section 3: Advanced applications of previous methods
- Section 4: Integration and analysis
- etc.

## Quality Standards

- **Rich Pedagogical Elements**: Each section must include 2-3 callout boxes, section-specific Key Takeaways, and complete sector applications
- **Appropriate Section Structure:** Break complex topics into focused, logical subsections rather than cramming everything into one section
- **Progressive Learning:** Each section should build naturally on previous sections with clear connections
- **Strategic Callout Usage**: Use tips for strategies, warnings for common errors, notes for connections, and important boxes for key concepts
- **Section-Specific Consolidation**: Every major section needs its own Key Takeaways (4-6 points) focusing only on that section's content
- **Comprehensive Applications**: Each section requires 4 unique sector applications demonstrating that section's specific methods
- **Engaging Teaching Voice:** Write with personality and warmth like a supportive teacher
- **Complete step-by-step solutions:** Show all working steps with encouraging explanations
- **Proper mathematical notation:** Throughout with clear reasoning for each step
- **Functional interactive visualizations:** With appropriate placeholders
- **Real-world sector applications:** That connect meaningfully to student experiences and demonstrate section-specific methods
- **Leaving Cert curriculum alignment:** While maintaining accessibility and engagement
- **Consistent educational progression:** That builds confidence and understanding
- **Conversational tone:** Use "Let's explore...", "Notice how...", "Here's why..." style language
- **Student-centered explanations:** Focus on helping students understand the 'why' not just the 'how'
- **Logical Topic Flow:** Ensure each ## section represents a distinct concept or method that students can master independently

Select the appropriate visualization template based on the mathematical content being covered. Always omit video sections unless specifically requested.

**FINAL STRUCTURE CHECK (DO NOT INCLUDE IN OUTPUT)**: Before generating content, determine if the topic requires multiple focused sections or can be handled as a single comprehensive section. Complex topics like "Quadratic Functions", "Calculus Applications", or "Statistical Analysis" should be broken into distinct ## sections, each with complete Theory → Interactive Visualization → Application → Key Takeaways structure. Simple topics like "Linear Equations" or "Circle Properties" can use the single main section format.

**PEDAGOGICAL COMPLETENESS CHECK (DO NOT INCLUDE IN OUTPUT)**: Each major ## section must include:
- 2-3 Callout boxes strategically placed (mix of tip, warning, note, seealso, important)
- Section-specific Key Takeaways (4-6 points about only that section's content)
- Complete set of 4 sector applications demonstrating that section's specific method
- 2-3 properly formatted examples using the mandatory format
- At least one interactive visualization placeholder

**CALLOUT BOX PLACEMENT STRATEGY (DO NOT INCLUDE IN OUTPUT)**:
- After introducing a new concept: ```{tip} for strategy or ```{important} for key formula
- Before tricky examples: ```{warning} about common mistakes
- After completing a method: ```{note} for connections or ```{seealso} for related topics
- Never place all callouts together - distribute throughout the section