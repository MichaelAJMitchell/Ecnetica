# Claude Code: Pedagogical MCQ Generation

Generate educationally valuable multiple choice questions that test understanding, not just computation.

## MCQ Structure
```json
{
    "id": "mcq_topic_type_001",
    "text": "Question with LaTeX: \\(equation\\)",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correctIndex": [0-3],
    "option_explanations": [
        "Detailed explanation for each option",
        "Include step-by-step solutions",
        "Explain why answers are right or wrong", 
        "Focus on teaching concepts"
    ],
    "solution_breakdown": [
        {
            "description": "Brief description of this step",
            "equation": "\\(mathematical result\\)",
            "reasoning": "Why we perform this step"
        }
    ],
    "main_topic_index": "uuid-from-knowledge-graph",
    "chapter": "algebra",
    "subtopic_weights": {
        "main_topic_uuid": 0.8,
        "related_topic_uuid": 0.2
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

**CRITICAL**: 
- Use `correctIndex` (with capital I) - the JavaScript system will not recognize `correctindex` (lowercase)
- **NEW FEATURE**: The MCQ system now supports solution breakdown visualization! When `solution_breakdown` is provided, a step-by-step walkthrough will appear after answering questions.

## Question Types (Mix These)
- **Procedural**: "Solve for x..." "Simplify..." "Calculate..."
- **Conceptual**: "Why do we...?" "What does this tell us?" "Which statement is true?"
- **Strategic**: "Which method is best?" "What should be the first step?"
- **Error Analysis**: "A student got X. What error did they make?"

## Essential Requirements

### **Complete Solution Breakdowns**
**For correct answers:**
```
"Correct! Step-by-step solution:
Step 1: [Action and reasoning]
Step 2: [Next step with why]
Step 3: [Final calculation]
Check: [Verify the answer]"
```

**For incorrect answers:**
```
"Incorrect. The answer is [correct value].
If you chose [wrong answer], you likely [what went wrong].
Correct approach: [brief walkthrough]"
```

### **Good Distractors**
Make wrong answers represent realistic mistakes:
- Sign errors (forgetting negatives)
- Method confusion (wrong formula)
- Incomplete work (stopping too early)
- Common calculation mistakes

Avoid random numbers or impossible answers.

### **Educational Focus**
- Test WHY and WHEN, not just HOW
- Connect to underlying mathematical concepts
- Help students learn from wrong answers
- Use clear, precise language

## Example Quality MCQ
```json
{
    "id": "mcq_linear_procedural_001",
    "text": "Solve for x: \\(3x - 7 = 14\\)",
    "options": ["\\(x = 7\\)", "\\(x = 21\\)", "\\(x = \\frac{7}{3}\\)", "\\(x = -7\\)"],
    "correctIndex": 0,
    "option_explanations": [
        "Correct! Step 1: Add 7 to both sides: 3x = 21. Step 2: Divide by 3: x = 7. Check: 3(7) - 7 = 14 ✓",
        "Incorrect. The answer is x = 7. If you got 21, you forgot to divide by 3 after getting 3x = 21.",
        "Incorrect. The answer is x = 7. If you got 7/3, you may have divided 7 by 3 instead of 21 by 3.",
        "Incorrect. The answer is x = 7. A negative answer suggests a sign error in your calculations."
    ],
    "main_topic_index": "e7a4f6d2-3b85-4f54-a64b-7a4e7f6d2b86",
    "chapter": "algebra",
    "subtopic_weights": {
        "e7a4f6d2-3b85-4f54-a64b-7a4e7f6d2b86": 1.0
    },
    "difficulty_breakdown": {
        "conceptual_understanding": 0.3,
        "procedural_fluency": 0.7,
        "problem_solving": 0.2,
        "mathematical_communication": 0.2,
        "memory": 0.4,
        "spatial_reasoning": 0.0
    }
}
```

## Key Principles
1. **Every question should teach something valuable**
2. **Explanations should help students understand concepts**
3. **Wrong answers should represent realistic student thinking**
4. **Focus on mathematical reasoning, not just computation**
5. **Make mathematics accessible and logical**

## Generation Process
1. **Choose a learning objective** - what should students understand?
2. **Design the question** to test that understanding
3. **Calculate the correct answer** carefully
4. **Create meaningful distractors** based on likely errors
5. **Write teaching explanations** for all options
6. **Verify** mathematical accuracy

Generate MCQs that help students develop mathematical understanding and reasoning skills.

## Validation Checklist

Before finalizing your MCQ, verify:

1. **Field Names**: Use `correctIndex` (capital I), not `correctindex`
2. **Array Alignment**: Ensure `correctIndex` value matches the right position in `options` array
3. **Explanation Match**: Verify `option_explanations[correctIndex]` starts with "Correct!"
4. **Answer Logic**: Double-check that the marked correct answer is actually mathematically correct
5. **Index Range**: Confirm `correctIndex` is 0, 1, 2, or 3 (not 1, 2, 3, 4)

**Example Verification**:
- If `correctIndex: 2`, then `options[2]` should be correct
- If `correctIndex: 2`, then `option_explanations[2]` should start with "Correct!"

**Note**: The MCQ system now supports clean line-by-line solution breakdown visualization. When `solution_breakdown` is provided, users will see each step clearly separated on its own line with proper spacing, equation, and reasoning. This provides a clean, readable walkthrough of the solution process.