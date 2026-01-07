# Quadratic Equations

## Linear Equations Revision

### Theory

Before we dive into the fascinating world of quadratic equations, let's take a moment to revisit linear equations. Think of this as building a bridge between what you already know and the new concepts we're about to explore.

**Linear Equation Structure**: A linear equation has the form:

$$ax + b = 0$$

where $a \neq 0$. The solution is always $x = -\frac{b}{a}$.

**Key Properties of Linear Equations**:
- **First-degree**: The highest power of $x$ is 1
- **One solution**: Every linear equation has exactly one solution (unless it's a contradiction or identity)
- **Straight line graph**: When graphed, linear equations form straight lines
- **Constant rate of change**: The relationship between variables is constant

**Why This Matters**: Linear equations represent situations where change happens at a constant rate. But what happens when change isn't constant? When acceleration or deceleration occurs? That's where quadratic equations come in.

### Application

#### Examples

##### Example 1: Simple Linear Equation
Let's solve this as a warm-up: $3x - 12 = 0$

**Method 1: Isolation**

$3x - 12 = 0 \quad \text{(Original equation)}$

$3x = 12 \quad \text{(Add 12 to both sides)}$

$x = 4 \quad \text{(Divide by 3)}$

**Verification**: $3(4) - 12 = 12 - 12 = 0$ ✓

##### Example 2: Comparing Linear and Quadratic Behavior
Notice the difference: Linear equation $y = 2x + 1$ vs. Quadratic equation $y = x^2 + 1$

**Linear**: As $x$ increases by 1, $y$ always increases by 2 (constant change)
**Quadratic**: As $x$ increases by 1, the change in $y$ varies (accelerating change)

#### Interactive Visualization: Linear vs Quadratic Comparison

<div id="linear-vs-quadratic-container" class="visualization-container" style="height: 500px; display: flex; align-items: center; justify-content: center; background-color: #f8f9fa; border: 2px dashed #dee2e6; border-radius: 8px;">
    <div style="text-align: center; color: #6c757d; font-size: 18px; font-weight: 500;">
        Interactive Graph
        <div style="font-size: 14px; margin-top: 8px; font-weight: normal;">
            Linear vs quadratic behavior comparison will be implemented here
        </div>
    </div>
</div>

#### Multiple Choice Questions

<div id="linear-revision-mcq" class="quiz-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Linear Equations Review",
        questions: [
            {
                text: "How many solutions does the equation \\(2x + 6 = 0\\) have?",
                options: ["0", "1", "2", "Infinitely many"],
                correctIndex: 1,
                explanation: "A linear equation \\(ax + b = 0\\) with \\(a \\neq 0\\) always has exactly one solution: \\(x = -\\frac{b}{a} = -\\frac{6}{2} = -3\\)",
                difficulty: "Basic"
            },
            {
                text: "What is the degree of the equation \\(5x - 15 = 0\\)?",
                options: ["0", "1", "2", "5"],
                correctIndex: 1,
                explanation: "The degree is the highest power of \\(x\\). In \\(5x - 15 = 0\\), \\(x\\) has power 1, so it's a first-degree equation.",
                difficulty: "Basic"
            }
        ]
    };
    MCQQuiz.create('linear-revision-mcq', quizData);
});
</script>

## Quadratic Equations

### Theory

Now let's explore quadratic equations - one of the most beautiful and useful topics in algebra. Here's why quadratic equations are so important: they describe acceleration, parabolic motion, optimization problems, and countless real-world phenomena where change isn't constant.

**Fundamental Definition**: A quadratic equation is a polynomial equation of degree 2, written in standard form as:

$$ax^2 + bx + c = 0$$

where $a$, $b$, and $c$ are real constants with $a \neq 0$.

**Why "Quadratic"?**: The term comes from the Latin word "quadratum," meaning square, because the defining feature is the $x^2$ term.

**Key Characteristics and Properties**:

**Degree and Solutions**: Quadratic equations are second-degree equations, and they can have:
- **Two distinct real solutions** (most common case)
- **One repeated real solution** (when the parabola just touches the x-axis)
- **Two complex conjugate solutions** (when the parabola doesn't cross the x-axis)

**Graphical Representation**: The graph of a quadratic function $y = ax^2 + bx + c$ is always a parabola:
- If $a > 0$: parabola opens upward (U-shaped)
- If $a < 0$: parabola opens downward (∩-shaped)

**The Discriminant**: The expression $\Delta = b^2 - 4ac$ determines the nature of solutions:
- If $\Delta > 0$: two distinct real solutions
- If $\Delta = 0$: one repeated real solution  
- If $\Delta < 0$: two complex conjugate solutions

**Solution Methods - A Complete Toolkit**:

**1. Factoring Method**: When the quadratic can be written as a product of linear factors
- Most elegant when it works
- Relies on recognizing patterns or systematic trial
- Uses the zero product property: if $(p)(q) = 0$, then $p = 0$ or $q = 0$

**2. Completing the Square**: A systematic method that always works
- Transforms the equation into perfect square form
- Reveals the vertex of the parabola
- Foundation for deriving the quadratic formula

**3. Quadratic Formula**: The universal solution method
$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$
- Works for any quadratic equation
- Provides both solutions simultaneously
- Shows the role of the discriminant clearly

**4. Graphical Method**: Finding x-intercepts of the parabola
- Useful for understanding the geometric meaning
- Helps visualize the relationship between solutions and graph

**Special Quadratic Forms and Patterns**:

**Perfect Square Trinomials**: $x^2 \pm 2ax + a^2 = (x \pm a)^2$

**Difference of Squares**: $x^2 - a^2 = (x + a)(x - a)$

**Standard Factoring Pattern**: $x^2 + (p + q)x + pq = (x + p)(x + q)$

**Vertex Form**: $y = a(x - h)^2 + k$ where $(h, k)$ is the vertex

**Real-World Applications**: Quadratic equations model numerous phenomena:
- **Physics**: Projectile motion, falling objects, pendulum motion
- **Engineering**: Bridge design, optimization problems, signal processing
- **Economics**: Profit maximization, cost-revenue analysis
- **Geometry**: Area problems, optimization of shapes

#### Interactive Visualization: Quadratic Function Explorer

<div id="quadratic-equation-container" class="visualization-container" style="height: 500px; display: flex; align-items: center; justify-content: center; background-color: #f8f9fa; border: 2px dashed #dee2e6; border-radius: 8px;">
    <div style="text-align: center; color: #6c757d; font-size: 18px; font-weight: 500;">
        Interactive Graph
        <div style="font-size: 14px; margin-top: 8px; font-weight: normal;">
            Quadratic function behavior and solution visualization will be implemented here
        </div>
    </div>
</div>

### Application

#### Examples

##### Example 1: Solving by Factoring
Let's solve this step by step: $x^2 - 5x + 6 = 0$

**Method 1: Factoring Approach**

$x^2 - 5x + 6 = 0 \quad \text{(We need two numbers that multiply to 6 and add to -5)}$

$(x - 2)(x - 3) = 0 \quad \text{(Since -2 × -3 = 6 and -2 + (-3) = -5)}$

$x - 2 = 0 \text{ or } x - 3 = 0 \quad \text{(Zero product property)}$

$x = 2 \text{ or } x = 3 \quad \text{(Solutions)}$

**Verification**: $2^2 - 5(2) + 6 = 4 - 10 + 6 = 0$ ✓ and $3^2 - 5(3) + 6 = 9 - 15 + 6 = 0$ ✓

##### Example 2: Completing the Square
Here's a systematic approach to: $x^2 + 6x + 5 = 0$

**Method 1: Completing the Square**

$x^2 + 6x + 5 = 0 \quad \text{(Original equation)}$

$x^2 + 6x = -5 \quad \text{(Move constant to right side)}$

$x^2 + 6x + 9 = -5 + 9 \quad \text{(Add $(6/2)^2 = 9$ to complete the square)}$

$(x + 3)^2 = 4 \quad \text{(Factor the perfect square trinomial)}$

$x + 3 = \pm 2 \quad \text{(Take square root of both sides)}$

$x = -3 + 2 = -1 \text{ or } x = -3 - 2 = -5 \quad \text{(Two solutions)}$

**Method 2: Quadratic Formula Verification**

$x = \frac{-6 \pm \sqrt{36 - 20}}{2} = \frac{-6 \pm \sqrt{16}}{2} = \frac{-6 \pm 4}{2} \quad \text{(Apply formula with a=1, b=6, c=5)}$

$x = \frac{-2}{2} = -1 \text{ or } x = \frac{-10}{2} = -5 \quad \text{(Same solutions - good!)}$

##### Example 3: Using Multiple Methods
Let's solve: $2x^2 - 7x + 3 = 0$

**Method 1: Factoring (AC Method)**

$2x^2 - 7x + 3 = 0 \quad \text{(Find factors of ac = 6 that add to b = -7)}$

$2x^2 - 6x - x + 3 = 0 \quad \text{(Split middle term: -7x = -6x - x)}$

$2x(x - 3) - 1(x - 3) = 0 \quad \text{(Factor by grouping)}$

$(2x - 1)(x - 3) = 0 \quad \text{(Factor out common binomial)}$

$x = \frac{1}{2} \text{ or } x = 3 \quad \text{(Solve each factor)}$

**Method 2: Quadratic Formula**

$x = \frac{-(-7) \pm \sqrt{(-7)^2 - 4(2)(3)}}{2(2)} \quad \text{(Substitute a=2, b=-7, c=3)}$

$x = \frac{7 \pm \sqrt{49 - 24}}{4} = \frac{7 \pm \sqrt{25}}{4} = \frac{7 \pm 5}{4} \quad \text{(Simplify under the radical)}$

$x = \frac{12}{4} = 3 \text{ or } x = \frac{2}{4} = \frac{1}{2} \quad \text{(Same solutions - perfect consistency!)}$

#### Multiple Choice Questions

<div id="quadratic-equations-mcq" class="quiz-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Quadratic Equations Practice",
        questions: [
            {
                text: "Which of the following is a quadratic equation?",
                options: ["\\(3x + 2 = 0\\)", "\\(x^2 + 5x = 7\\)", "\\(x^3 - 1 = 0\\)", "\\(\\frac{1}{x} + 2 = 0\\)"],
                correctIndex: 1,
                explanation: "\\(x^2 + 5x = 7\\) can be rewritten as \\(x^2 + 5x - 7 = 0\\), which has degree 2, making it quadratic.",
                difficulty: "Basic"
            },
            {
                text: "Solve: \\(x^2 - 9 = 0\\)",
                options: ["\\(x = 3\\)", "\\(x = -3\\)", "\\(x = \\pm 3\\)", "\\(x = 9\\)"],
                correctIndex: 2,
                explanation: "\\(x^2 - 9 = 0\\) can be factored as \\((x-3)(x+3) = 0\\), giving \\(x = 3\\) or \\(x = -3\\), so \\(x = \\pm 3\\)",
                difficulty: "Basic"
            },
            {
                text: "For \\(x^2 - 4x + 4 = 0\\), how many distinct real solutions exist?",
                options: ["0", "1", "2", "3"],
                correctIndex: 1,
                explanation: "This factors as \\((x-2)^2 = 0\\), giving a repeated root at \\(x = 2\\). There is only 1 distinct solution. The discriminant is \\(16 - 16 = 0\\), confirming one repeated solution.",
                difficulty: "Intermediate"
            },
            {
                text: "If \\(x^2 + px + 12 = 0\\) has solutions \\(x = 3\\) and \\(x = 4\\), find \\(p\\).",
                options: ["\\(p = -7\\)", "\\(p = 7\\)", "\\(p = -12\\)", "\\(p = 12\\)"],
                correctIndex: 0,
                explanation: "By Vieta's formulas, the sum of roots equals \\(-p\\). Since \\(3 + 4 = 7\\), we have \\(-p = 7\\), so \\(p = -7\\). We can verify: the product of roots is \\(3 \\times 4 = 12\\), which matches the constant term.",
                difficulty: "Advanced"
            }
        ]
    };
    MCQQuiz.create('quadratic-equations-mcq', quizData);
});
</script>

#### Sector Specific Questions: Quadratic Equations Applications

<div id="quadratic-equations-identity-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quadraticEquationsContent = {
        "title": "Quadratic Equations: Applications",
        "intro_content": `<p>Quadratic equations are fundamental in modeling acceleration, optimization, and parabolic relationships across all fields. From calculating projectile trajectories in physics to maximizing profits in business, quadratic equations provide essential tools for understanding and solving problems involving non-linear change and optimization.</p>`,
        "questions": [
            {
                "category": "scientific",
                "title": "Physics: Projectile Motion",
                "content": `A ball is thrown upward with initial velocity 20 m/s from a height of 5 meters. The height \\(h\\) at time \\(t\\) is given by \\(h = -5t^2 + 20t + 5\\). When does the ball hit the ground, and what is the maximum height reached?`,
                "answer": `<p><strong>Part 1: When does the ball hit the ground?</strong></p>
                <p>The ball hits the ground when \\(h = 0\\):</p>
                <p>\\(-5t^2 + 20t + 5 = 0\\)</p>
                <p>Divide by -5: \\(t^2 - 4t - 1 = 0\\)</p>
                <p>Using the quadratic formula:</p>
                <p>\\(t = \\frac{4 \\pm \\sqrt{16 + 4}}{2} = \\frac{4 \\pm \\sqrt{20}}{2} = \\frac{4 \\pm 2\\sqrt{5}}{2} = 2 \\pm \\sqrt{5}\\)</p>
                <p>Since \\(t > 0\\), we take \\(t = 2 + \\sqrt{5} ≈ 4.24\\) seconds</p>
                <p><strong>Part 2: Maximum height</strong></p>
                <p>Maximum occurs at \\(t = \\frac{-b}{2a} = \\frac{-20}{2(-5)} = 2\\) seconds</p>
                <p>\\(h_{max} = -5(4) + 20(2) + 5 = -20 + 40 + 5 = 25\\) meters</p>`
            },
            {
                "category": "engineering",
                "title": "Civil Engineering: Bridge Design",
                "content": `A parabolic arch bridge has the equation \\(y = -0.05x^2 + 2x\\) where \\(y\\) is height and \\(x\\) is horizontal distance (both in meters). Find the span and maximum height of the bridge.`,
                "answer": `<p><strong>Part 1: Find the span (where arch meets ground)</strong></p>
                <p>The span is found where \\(y = 0\\):</p>
                <p>\\(-0.05x^2 + 2x = 0\\)</p>
                <p>\\(x(-0.05x + 2) = 0\\)</p>
                <p>\\(x = 0\\) or \\(-0.05x + 2 = 0\\)</p>
                <p>From the second equation: \\(x = \\frac{2}{0.05} = 40\\)</p>
                <p>The span is 40 meters (from \\(x = 0\\) to \\(x = 40\\))</p>
                <p><strong>Part 2: Maximum height</strong></p>
                <p>Maximum occurs at \\(x = \\frac{-b}{2a} = \\frac{-2}{2(-0.05)} = 20\\) meters</p>
                <p>\\(y_{max} = -0.05(400) + 2(20) = -20 + 40 = 20\\) meters</p>`
            },
            {
                "category": "financial",
                "title": "Business: Profit Maximization",
                "content": `A company's profit \\(P\\) (in thousands of dollars) is modeled by \\(P = -2x^2 + 80x - 750\\) where \\(x\\) is the number of units produced (in hundreds). Find the break-even points and maximum profit.`,
                "answer": `<p><strong>Part 1: Break-even points (where P = 0)</strong></p>
                <p>\\(-2x^2 + 80x - 750 = 0\\)</p>
                <p>Divide by -2: \\(x^2 - 40x + 375 = 0\\)</p>
                <p>Using the quadratic formula:</p>
                <p>\\(x = \\frac{40 \\pm \\sqrt{1600 - 1500}}{2} = \\frac{40 \\pm \\sqrt{100}}{2} = \\frac{40 \\pm 10}{2}\\)</p>
                <p>\\(x = 25\\) or \\(x = 15\\)</p>
                <p>Break-even points: 1500 units and 2500 units</p>
                <p><strong>Part 2: Maximum profit</strong></p>
                <p>Maximum occurs at \\(x = \\frac{-b}{2a} = \\frac{-80}{2(-2)} = 20\\) (hundreds of units)</p>
                <p>\\(P_{max} = -2(400) + 80(20) - 750 = -800 + 1600 - 750 = 50\\)</p>
                <p>Maximum profit is $50,000 at 2000 units</p>`
            },
            {
                "category": "creative",
                "title": "Game Design: Trajectory Planning",
                "content": `In a game, a character jumps following the path \\(y = -\\frac{1}{16}x^2 + x\\) where distances are in game units. What is the maximum height reached and the total horizontal distance traveled?`,
                "answer": `<p><strong>Part 1: Maximum height</strong></p>
                <p>The maximum occurs at the vertex. For \\(y = ax^2 + bx + c\\):</p>
                <p>\\(x = \\frac{-b}{2a} = \\frac{-1}{2(-\\frac{1}{16})} = \\frac{-1}{-\\frac{1}{8}} = 8\\)</p>
                <p>Maximum height: \\(y = -\\frac{1}{16}(64) + 8 = -4 + 8 = 4\\) game units</p>
                <p><strong>Part 2: Horizontal distance (where character lands)</strong></p>
                <p>Character lands when \\(y = 0\\):</p>
                <p>\\(-\\frac{1}{16}x^2 + x = 0\\)</p>
                <p>\\(x(-\\frac{1}{16}x + 1) = 0\\)</p>
                <p>\\(x = 0\\) (start) or \\(x = 16\\) (landing)</p>
                <p>Total horizontal distance: 16 game units</p>`
            }
        ]
    };
    MathQuestionModule.render(quadraticEquationsContent, 'quadratic-equations-identity-container');
});
</script>

### Key Takeaways

```{important}
1. A quadratic equation has the form $ax^2 + bx + c = 0$ where $a \neq 0$
2. Quadratic equations can have 0, 1, or 2 real solutions depending on the discriminant $\Delta = b^2 - 4ac$
3. Four main solving methods: factoring, completing the square, quadratic formula, and graphing
4. The quadratic formula $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$ works for any quadratic equation
5. The graph of a quadratic function is always a parabola
6. Vertex occurs at $x = \frac{-b}{2a}$, which is often the key to optimization problems
7. Quadratic equations model projectile motion, area optimization, and profit maximization
8. Always check solutions by substitution, and consider which solutions make sense in context
```