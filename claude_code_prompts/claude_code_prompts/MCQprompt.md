# Claude Code Prompt: Generate Educational MCQs

Generate Multiple Choice Questions for mathematics learning that test understanding, not just computation.

## MCQ Structure
```json
{
    "text": "Question with LaTeX: \\(equation\\)",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correctIndex": [0-3],
    "option_explanations": [
        "Detailed explanation for each option",
        "Include step-by-step solutions for correct answers",
        "Explain specific mistakes for incorrect answers", 
        "Connect to underlying concepts"
    ],
    "solution_breakdown": [
        {
            "description": "Brief description of this step",
            "equation": "\\(mathematical result\\)",
            "reasoning": "Why we perform this step"
        }
    ],
    "main_topic_index": "uuid_from_knowledge_graph",
    "chapter": "Chapter_Name",
    "subtopic_weights": {
        "main_topic": 0.6-0.8,
        "related_topic": 0.2-0.4
    },
    "difficulty_breakdown": {
        "conceptual_understanding": 0.0-1.0,
        "procedural_fluency": 0.0-1.0,
        "problem_solving": 0.0-1.0,
        "mathematical_communication": 0.0-1.0,
        "memory": 0.0-1.0,
        "spatial_reasoning": 0.0-1.0
    }
}
```

## Question Types (Required Distribution)
- **40% Conceptual**: "Why does...?" "What does X tell us about...?" "Which statement is always true?"
- **30% Procedural**: "Solve..." "Simplify..." "Calculate..."
- **20% Strategic**: "Which method is most efficient?" "What should be the first step?"
- **10% Error Analysis**: "A student got X. What error did they make?" "What's wrong with this solution?"

## Correct Answer Distribution
**CRITICAL**: Distribute correct answers evenly across positions:
- 25% of questions: correctIndex = 0 (Option A correct)
- 25% of questions: correctIndex = 1 (Option B correct)  
- 25% of questions: correctIndex = 2 (Option C correct)
- 25% of questions: correctIndex = 3 (Option D correct)

**For single MCQ generation**: Randomly select correctIndex from [0, 1, 2, 3]
**Never** make correctIndex = 0 for consecutive questions.

**IMPORTANT**: Use `correctIndex` (capital I) - the JavaScript system requires this exact field name.

**SYSTEM UPDATE**: The MCQ system now supports solution breakdown visualization! When `solution_breakdown` is provided in the MCQ data, users will see a step-by-step walkthrough showing exactly how to solve the problem after answering.

## Essential Distractor Guidelines
Create wrong answers that represent:
1. **Sign errors**: Forgetting negatives, not flipping inequality signs
2. **Method confusion**: Using wrong formulas or procedures
3. **Conceptual mistakes**: Confusing related concepts (coefficient vs variable)
4. **Incomplete solutions**: Stopping too early, missing steps

Avoid: Random numbers, obvious impossibilities, pure arithmetic errors.

## CRITICAL: Complete Solution Breakdowns Required

**EVERY MCQ must include 4 detailed option_explanations:**

### For the Correct Answer:
```
"Correct! Step-by-step solution:
Step 1: [First operation with reasoning]
Step 2: [Second operation with reasoning]
Step 3: [Final step]
Check: [Substitute back to verify]
Key concept: [Why this method works]"
```

### For Each Incorrect Answer:
```
"Incorrect. The answer is [correct value].
If you got [this wrong answer], you likely [specific mistake].
Correct method: [brief walkthrough]
To avoid this error: [key tip]"
```

**Example for equation 5x - 20 = 0:**
- Correct (x = 4): "Correct! Step 1: Add 20 to both sides: 5x = 20. Step 2: Divide by 5: x = 4. Check: 5(4) - 20 = 0 ✓"
- Wrong (x = -4): "Incorrect. The answer is x = 4. If you got x = -4, you likely made a sign error. Remember: adding 20 to both sides gives 5x = 20, so x = 4."

**MANDATORY**: All 4 explanations must be educational and specific to that option.

## Key Misconceptions to Target

**Variables**: Thinking coefficient of 1 means x = 1
**Equations**: Moving terms without changing signs
**Inequalities**: Not flipping signs with negative operations
**Factoring**: Canceling terms instead of factors
**Quadratics**: Forgetting ± in square root method
**Fractions**: Cross-canceling inappropriately

## Difficulty Framework
Rate each dimension 0.0-1.0:
- **Conceptual**: How much deep understanding is required
- **Procedural**: Complexity of calculations needed
- **Problem Solving**: How much strategy/reasoning required
- **Communication**: Level of mathematical language
- **Memory**: How much must be recalled
- **Spatial**: Visual/graphical reasoning needed

## Quality Requirements
- Questions test WHY and WHEN, not just HOW
- Every explanation teaches something valuable
- Distractors represent realistic student thinking
- Language is clear and unambiguous
- Difficulty matches knowledge graph progression
- Each question naturally connects to prerequisite concepts

## Generation Focus
1. **Start with the learning objective** - what should students understand?
2. **Design the question** to test that understanding
3. **Create distractors** based on common mistakes
4. **Write explanations** that teach and correct misconceptions
5. **Verify** mathematical accuracy and pedagogical value

## Debugging Instructions for Single MCQ Generation

**Step 1: Generate ONE MCQ and verify JSON structure**
```json
{
    "text": "Question text",
    "options": ["A", "B", "C", "D"],
    "correctIndex": 2,  // THIS MUST BE 0, 1, 2, OR 3
    "option_explanations": [
        "Explanation for option A (index 0)",
        "Explanation for option B (index 1)", 
        "Explanation for option C (index 2) - THE CORRECT ONE",
        "Explanation for option D (index 3)"
    ]
}
```

**Step 2: Manually verify correctIndex matches the right option**
- If correctIndex is 0, option A should be correct
- If correctIndex is 1, option B should be correct
- etc.

**Step 3: Check that option_explanations[correctIndex] starts with "Correct!"**

**CURRENT SYSTEM CAPABILITIES**: The MCQ system now supports clean line-by-line solution breakdown visualization through the enhanced `MCQQuiz.create()` functionality. When `solution_breakdown` metadata is provided, users will see each step clearly separated on its own line with proper spacing, equation, and reasoning. This provides a clean, readable walkthrough of the solution process.

Generate MCQs that make students think deeply about mathematical concepts, not just apply procedures mechanically.