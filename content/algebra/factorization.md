# Factorization

## Algebraic Expressions Revision

### Theory

Before we dive into the powerful world of factorization, let's take a moment to revisit algebraic expressions. Think of this as laying the groundwork for understanding how mathematical expressions can be broken down into their component parts.

**What is an Algebraic Expression?**: An algebraic expression is a mathematical phrase that combines variables, constants, and operations. For example:

$$3x^2 + 5x - 2$$

**Essential Terminology**:
- **Term**: A single part of an expression, like $3x^2$, $5x$, or $-2$
- **Coefficient**: The numerical part of a term, such as $3$ in $3x^2$
- **Variable**: The letter that represents an unknown value, like $x$
- **Constant**: A term without variables, such as $-2$
- **Like terms**: Terms with identical variable parts, like $3x$ and $7x$

**Combining Like Terms**: We can simplify expressions by adding or subtracting coefficients of like terms:

$$3x + 7x - 2x = (3 + 7 - 2)x = 8x$$

**Why This Matters**: Understanding how to manipulate algebraic expressions is crucial because factorization is essentially the reverse process of expanding expressions. When we factor, we're looking for the "building blocks" that, when multiplied together, give us the original expression.

### Application

#### Examples

##### Example 1: Simplifying Expressions
Let's work through this step by step: $4x^2 + 3x - 2x^2 + 7x - 5$

**Step 1: Identify like terms**

$4x^2 + 3x - 2x^2 + 7x - 5 \quad \text{(Group similar terms together)}$

**Step 2: Combine like terms**

$(4x^2 - 2x^2) + (3x + 7x) - 5 \quad \text{(Combine coefficients of like terms)}$

$2x^2 + 10x - 5 \quad \text{(Simplified form)}$

##### Example 2: Understanding Structure
Consider the expression $x^2 + 5x + 6$. Notice how we can think about its structure:
- This could be the result of multiplying two simpler expressions
- Factorization will help us find what those simpler expressions are
- This connects directly to solving quadratic equations

#### Interactive Visualization: Expression Structure Explorer

<div id="algebraic-expressions-container" class="visualization-container" style="height: 500px; display: flex; align-items: center; justify-content: center; background-color: #f8f9fa; border: 2px dashed #dee2e6; border-radius: 8px;">
    <div style="text-align: center; color: #6c757d; font-size: 18px; font-weight: 500;">
        Interactive Graph
        <div style="font-size: 14px; margin-top: 8px; font-weight: normal;">
            Algebraic expression structure and behavior visualization will be implemented here
        </div>
    </div>
</div>

#### Multiple Choice Questions

<div id="expressions-revision-mcq" class="quiz-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Algebraic Expressions Review",
        questions: [
            {
                text: "Simplify: \\(5x + 3x - 2x\\)",
                options: ["\\(6x\\)", "\\(8x\\)", "\\(10x\\)", "\\(11x\\)"],
                correctIndex: 0,
                explanation: "Combine like terms: \\(5x + 3x - 2x = (5 + 3 - 2)x = 6x\\)",
                difficulty: "Basic"
            },
            {
                text: "What is the coefficient of \\(x^2\\) in \\(3x^2 - 7x + 2\\)?",
                options: ["\\(-7\\)", "\\(2\\)", "\\(3\\)", "\\(1\\)"],
                correctIndex: 2,
                explanation: "The coefficient of \\(x^2\\) is the number multiplying \\(x^2\\), which is \\(3\\).",
                difficulty: "Basic"
            }
        ]
    };
    MCQQuiz.create('expressions-revision-mcq', quizData);
});
</script>

## Factorization

### Theory

Now let's explore one of the most powerful and elegant techniques in algebra - factorization. Here's why factorization is so important: it's like finding the DNA of mathematical expressions, revealing their fundamental structure and enabling us to solve complex problems with surprising efficiency.

**Fundamental Definition**: Factorization is the process of expressing an algebraic expression as a product of its factors. It's the reverse operation of expanding expressions.

**The Big Picture**: Think of factorization as mathematical archaeology - we're uncovering the simpler expressions that were multiplied together to create the complex expression we see.

**Why Factorization Matters**: This technique is essential for:
- **Solving quadratic and higher-degree equations** efficiently
- **Simplifying algebraic fractions** by canceling common factors
- **Finding rational roots** and understanding polynomial behavior
- **Optimization problems** in calculus and real-world applications
- **Cryptography and computer science** applications

**Complete Factorization Toolkit**:

**1. Common Factor Method**: Remove the greatest common factor (GCF) first
- **Strategy**: Look for the largest expression that divides all terms
- **Pattern**: $ab + ac = a(b + c)$
- **Benefits**: Simplifies the expression and often reveals further factoring opportunities

**2. Difference of Two Squares**: Recognize the pattern $a^2 - b^2$
- **Formula**: $a^2 - b^2 = (a + b)(a - b)$
- **Key insight**: This only works for subtraction, not addition
- **Applications**: Simplifying expressions, solving equations, rationalizing denominators

**3. Perfect Square Trinomials**: Identify squared binomial patterns
- **Patterns**: 
  - $a^2 + 2ab + b^2 = (a + b)^2$
  - $a^2 - 2ab + b^2 = (a - b)^2$
- **Recognition**: Middle term is twice the product of the square roots of the first and last terms

**4. Quadratic Trinomials**: Factor expressions of the form $ax^2 + bx + c$
- **When $a = 1$**: Find two numbers that multiply to $c$ and add to $b$
- **When $a \neq 1$**: Use the AC method or trial and error systematically
- **Strategy**: Look for patterns and use educated guessing combined with systematic checking

**5. Grouping Method**: Factor by grouping terms strategically
- **When to use**: Four or more terms that don't fit other patterns
- **Process**: Group terms, factor out common factors from each group, then factor the resulting expression

**6. Sum and Difference of Cubes**: Handle cubic expressions
- **Formulas**: 
  - $a^3 + b^3 = (a + b)(a^2 - ab + b^2)$
  - $a^3 - b^3 = (a - b)(a^2 + ab + b^2)$

**Strategic Approach to Factorization**:

**Step 1**: Always look for a common factor first
**Step 2**: Count the number of terms and identify the pattern
**Step 3**: Apply the appropriate method based on the pattern
**Step 4**: Check if further factorization is possible
**Step 5**: Verify by expanding your factored form

**Recognition Patterns**: Developing pattern recognition is crucial:
- Two terms → Look for difference of squares or sum/difference of cubes
- Three terms → Check for perfect square trinomials or general quadratic patterns
- Four or more terms → Consider grouping

#### Interactive Visualization: Factorization Pattern Explorer

<div id="factorization-container" class="visualization-container" style="height: 500px; display: flex; align-items: center; justify-content: center; background-color: #f8f9fa; border: 2px dashed #dee2e6; border-radius: 8px;">
    <div style="text-align: center; color: #6c757d; font-size: 18px; font-weight: 500;">
        Interactive Graph
        <div style="font-size: 14px; margin-top: 8px; font-weight: normal;">
            Factorization patterns and visual verification will be implemented here
        </div>
    </div>
</div>

### Application

#### Examples

##### Example 1: Common Factor Method
Let's start with the foundation: $6x^3 + 9x^2 - 15x$

**Step 1: Identify the GCF**

$6x^3 + 9x^2 - 15x \quad \text{(Look at coefficients: GCF of 6, 9, 15 is 3)}$

$\text{Variables: GCF of } x^3, x^2, x \text{ is } x \quad \text{(Take lowest power)}$

$\text{Overall GCF} = 3x \quad \text{(Combine numerical and variable GCF)}$

**Step 2: Factor out the GCF**

$3x(2x^2 + 3x - 5) \quad \text{(Divide each term by 3x)}$

**Verification**: $3x(2x^2 + 3x - 5) = 6x^3 + 9x^2 - 15x$ ✓

##### Example 2: Difference of Squares
Here's a beautiful pattern in action: $16x^2 - 25$

**Step 1: Recognize the pattern**

$16x^2 - 25 = (4x)^2 - 5^2 \quad \text{(Identify as difference of two squares)}$

**Step 2: Apply the formula**

$(4x)^2 - 5^2 = (4x + 5)(4x - 5) \quad \text{(Use } a^2 - b^2 = (a+b)(a-b)\text{)}$

**Verification**: $(4x + 5)(4x - 5) = 16x^2 - 20x + 20x - 25 = 16x^2 - 25$ ✓

##### Example 3: Quadratic Trinomial Factoring
Let's tackle a classic: $x^2 + 7x + 12$

**Method 1: Find Two Numbers Approach**

$x^2 + 7x + 12 \quad \text{(Need two numbers that multiply to 12 and add to 7)}$

$\text{Factors of 12: } 1 \times 12, 2 \times 6, 3 \times 4 \quad \text{(List factor pairs)}$

$3 + 4 = 7 \text{ and } 3 \times 4 = 12 \quad \text{(Perfect! These are our numbers)}$

$(x + 3)(x + 4) \quad \text{(Write as product of binomials)}$

**Method 2: Verification by Expansion**

$(x + 3)(x + 4) = x^2 + 4x + 3x + 12 = x^2 + 7x + 12 \quad \text{(Confirms our factorization)}$

**Method 3: Visual Understanding**

Think of this as: "What two expressions, when multiplied, give us $x^2 + 7x + 12$?"

The answer: $(x + 3)$ and $(x + 4)$ are the "building blocks"

#### Multiple Choice Questions

<div id="factorization-mcq" class="quiz-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Factorization Practice",
        questions: [
            {
                text: "Factor: \\(6x + 12\\)",
                options: ["\\(6(x + 2)\\)", "\\(3(2x + 4)\\)", "\\(2(3x + 6)\\)", "All of the above"],
                correctIndex: 3,
                explanation: "All options are correct factorizations. However, \\(6(x + 2)\\) shows the greatest common factor most clearly: GCF(6, 12) = 6.",
                difficulty: "Basic"
            },
            {
                text: "Factor: \\(x^2 - 9\\)",
                options: ["\\((x - 3)^2\\)", "\\((x + 3)(x - 3)\\)", "\\((x - 9)(x + 1)\\)", "Cannot be factored"],
                correctIndex: 1,
                explanation: "This is a difference of squares: \\(x^2 - 9 = x^2 - 3^2 = (x + 3)(x - 3)\\)",
                difficulty: "Basic"
            },
            {
                text: "Factor: \\(x^2 + 8x + 15\\)",
                options: ["\\((x + 3)(x + 5)\\)", "\\((x + 1)(x + 15)\\)", "\\((x + 2)(x + 6)\\)", "\\((x - 3)(x - 5)\\)"],
                correctIndex: 0,
                explanation: "We need two numbers that multiply to 15 and add to 8. These are 3 and 5: \\(3 \\times 5 = 15\\) and \\(3 + 5 = 8\\), so \\((x + 3)(x + 5)\\)",
                difficulty: "Intermediate"
            },
            {
                text: "Which expression is a perfect square trinomial?",
                options: ["\\(x^2 + 6x + 8\\)", "\\(x^2 + 10x + 25\\)", "\\(x^2 + 7x + 12\\)", "\\(x^2 + 5x + 6\\)"],
                correctIndex: 1,
                explanation: "\\(x^2 + 10x + 25 = (x + 5)^2\\) is a perfect square trinomial. Check: \\((x + 5)^2 = x^2 + 2(5x) + 25 = x^2 + 10x + 25\\)",
                difficulty: "Advanced"
            }
        ]
    };
    MCQQuiz.create('factorization-mcq', quizData);
});
</script>

#### Sector Specific Questions: Factorization Applications

<div id="factorization-identity-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const factorizationContent = {
        "title": "Factorization: Applications",
        "intro_content": `<p>Factorization is a fundamental tool across all fields of science, engineering, and mathematics. From solving physics equations by finding when forces equal zero, to optimizing business functions by identifying critical points, factorization reveals the underlying structure that makes complex problems manageable and elegant to solve.</p>`,
        "questions": [
            {
                "category": "scientific",
                "title": "Physics: Projectile Motion Analysis",
                "content": `The height of a projectile is given by \\(h(t) = -16t^2 + 64t\\). Factor this expression to find when the projectile is at ground level and determine the time of maximum height.`,
                "answer": `<p><strong>Step 1: Factor the expression</strong></p>
                <p>\\(h(t) = -16t^2 + 64t\\)</p>
                <p>\\(h(t) = -16t(t - 4)\\) (factor out GCF of -16t)</p>
                <p><strong>Step 2: Find when projectile hits ground (h = 0)</strong></p>
                <p>\\(-16t(t - 4) = 0\\)</p>
                <p>\\(t = 0\\) (launch time) or \\(t = 4\\) (landing time)</p>
                <p><strong>Step 3: Time of maximum height</strong></p>
                <p>Maximum occurs at midpoint: \\(t = \\frac{0 + 4}{2} = 2\\) seconds</p>
                <p>The projectile is launched at t = 0, reaches maximum height at t = 2, and lands at t = 4 seconds</p>`
            },
            {
                "category": "engineering",
                "title": "Structural Engineering: Load Distribution",
                "content": `The bending moment in a beam is expressed as \\(M(x) = 2x^3 - 8x^2 + 6x\\). Factor this expression completely to identify critical points where the moment equals zero.`,
                "answer": `<p><strong>Step 1: Factor out the GCF</strong></p>
                <p>\\(M(x) = 2x^3 - 8x^2 + 6x\\)</p>
                <p>\\(M(x) = 2x(x^2 - 4x + 3)\\) (factor out 2x)</p>
                <p><strong>Step 2: Factor the quadratic</strong></p>
                <p>\\(x^2 - 4x + 3\\) needs two numbers that multiply to 3 and add to -4</p>
                <p>These are -1 and -3: \\((-1) + (-3) = -4\\) and \\((-1) \\times (-3) = 3\\)</p>
                <p>\\(x^2 - 4x + 3 = (x - 1)(x - 3)\\)</p>
                <p><strong>Step 3: Complete factorization</strong></p>
                <p>\\(M(x) = 2x(x - 1)(x - 3)\\)</p>
                <p><strong>Step 4: Find critical points</strong></p>
                <p>\\(M(x) = 0\\) when \\(x = 0, 1, 3\\)</p>
                <p>Critical points occur at x = 0, 1, and 3 units along the beam</p>`
            },
            {
                "category": "financial",
                "title": "Economics: Profit Optimization",
                "content": `A company's profit function is \\(P(x) = -x^2 + 10x - 21\\) where \\(x\\) is production level (in thousands). Factor to find break-even points and analyze profit behavior.`,
                "answer": `<p><strong>Step 1: Factor the profit function</strong></p>
                <p>\\(P(x) = -x^2 + 10x - 21\\)</p>
                <p>\\(P(x) = -(x^2 - 10x + 21)\\) (factor out -1)</p>
                <p><strong>Step 2: Factor the quadratic</strong></p>
                <p>For \\(x^2 - 10x + 21\\), need numbers that multiply to 21 and add to -10</p>
                <p>These are -3 and -7: \\((-3) + (-7) = -10\\) and \\((-3) \\times (-7) = 21\\)</p>
                <p>\\(x^2 - 10x + 21 = (x - 3)(x - 7)\\)</p>
                <p><strong>Step 3: Complete factorization</strong></p>
                <p>\\(P(x) = -(x - 3)(x - 7)\\)</p>
                <p><strong>Step 4: Find break-even points</strong></p>
                <p>\\(P(x) = 0\\) when \\(x = 3\\) or \\(x = 7\\)</p>
                <p>Break-even occurs at 3,000 and 7,000 units. Maximum profit occurs at \\(x = 5\\) (midpoint)</p>`
            },
            {
                "category": "creative",
                "title": "Computer Graphics: Area Optimization",
                "content": `In a graphics program, the area of a shape is given by \\(A(s) = s^2 + 6s + 8\\) where \\(s\\) is a scaling factor. Factor this expression to understand the shape's behavior and find when area equals zero.`,
                "answer": `<p><strong>Step 1: Factor the area function</strong></p>
                <p>\\(A(s) = s^2 + 6s + 8\\)</p>
                <p>Need two numbers that multiply to 8 and add to 6</p>
                <p>These are 2 and 4: \\(2 + 4 = 6\\) and \\(2 \\times 4 = 8\\)</p>
                <p>\\(A(s) = (s + 2)(s + 4)\\)</p>
                <p><strong>Step 2: Find when area equals zero</strong></p>
                <p>\\((s + 2)(s + 4) = 0\\)</p>
                <p>\\(s = -2\\) or \\(s = -4\\)</p>
                <p><strong>Step 3: Interpretation</strong></p>
                <p>Since negative scaling factors don't make physical sense in this context, this factorization helps validate that \\(s > 0\\) for meaningful results</p>
                <p>The factored form \\((s + 2)(s + 4)\\) reveals the mathematical structure and domain restrictions</p>`
            }
        ]
    };
    MathQuestionModule.render(factorizationContent, 'factorization-identity-container');
});
</script>

### Key Takeaways

```{important}
1. Factorization is the reverse process of expanding - finding the "building blocks" of expressions
2. Always look for a greatest common factor (GCF) first before applying other methods
3. Key patterns to master:
   - Common factor: $ab + ac = a(b + c)$
   - Difference of squares: $a^2 - b^2 = (a+b)(a-b)$
   - Perfect square trinomials: $a^2 ± 2ab + b^2 = (a ± b)^2$
   - General quadratic: find two numbers that multiply to $ac$ and add to $b$
4. Factorization enables efficient equation solving using the zero product property
5. The technique reveals critical points in physics, engineering, and business applications
6. Always verify factorizations by expanding back to the original expression
7. Some expressions cannot be factored over the real numbers - this is perfectly normal
8. Pattern recognition improves with practice - the more you factor, the faster you'll recognize forms
```