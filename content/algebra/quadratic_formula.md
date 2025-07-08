# Quadratic Formula

## Quadratic Formula

### Theory

The quadratic formula is a universal method for solving any quadratic equation of the form $ax^2 + bx + c = 0$ where $a \neq 0$. It provides a direct way to find the solutions without factoring or completing the square.

The quadratic formula is:

$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$

This formula was derived by completing the square on the general quadratic equation. The expression under the square root, $b^2 - 4ac$, is called the **discriminant** and is denoted by $\Delta$ (delta).

The discriminant tells us about the nature of the solutions:
- If $\Delta > 0$: Two distinct real solutions
- If $\Delta = 0$: One repeated real solution (also called a double root)
- If $\Delta < 0$: Two complex conjugate solutions (no real solutions)

```{note}
The quadratic formula always works for any quadratic equation, making it a reliable fallback when other methods are difficult to apply.
```

#### Interactive Visualization: Quadratic Formula Explorer

<div id="quadratic-formula-container" class="visualization-container" style="height: 500px;"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    MathVisualizer.createGraphFromDescription('quadratic-formula-container', {
        boundingBox: [-5, 5, 5, -5],
        theme: 'light',
        useSequentialColors: true,
        infoBox: {
            title: "Quadratic Formula",
            lines: [
                {text: "y = ax² + bx + c", dynamic: false},
                {text: "a: ${a}, b: ${b}, c: ${c}", dynamic: true},
                {text: "Δ = b² - 4ac = ${(b*b - 4*a*c).toFixed(2)}", dynamic: true},
                {text: "x₁ = ${a !== 0 && b*b - 4*a*c >= 0 ? ((-b + Math.sqrt(b*b - 4*a*c))/(2*a)).toFixed(2) : 'N/A'}", dynamic: true},
                {text: "x₂ = ${a !== 0 && b*b - 4*a*c >= 0 ? ((-b - Math.sqrt(b*b - 4*a*c))/(2*a)).toFixed(2) : 'N/A'}", dynamic: true}
            ],
            position: {top: 55, left: 20}
        },
        parametrizedFunctions: [
            {
                expression: 'a*x^2 + b*x + c',
                title: 'Quadratic Function',
                parameters: {
                    a: { min: -3, max: 3, value: 1, step: 0.1 },
                    b: { min: -5, max: 5, value: -2, step: 0.1 },
                    c: { min: -5, max: 5, value: -3, step: 0.1 }
                },
                features: ['zeros', 'extrema']
            }
        ]
    });
});
</script>

### Application

#### Examples

##### Example 1
Solve using the quadratic formula: $x^2 + 5x + 6 = 0$

**Method 1: Quadratic Formula**

$x^2 + 5x + 6 = 0 \quad \text{(Identify: a = 1, b = 5, c = 6)}$

$\Delta = b^2 - 4ac = 25 - 24 = 1 \quad \text{(Calculate discriminant)}$

$x = \frac{-5 \pm \sqrt{1}}{2(1)} = \frac{-5 \pm 1}{2} \quad \text{(Apply formula)}$

$x = \frac{-5 + 1}{2} = -2 \text{ or } x = \frac{-5 - 1}{2} = -3 \quad \text{(Calculate both solutions)}$

##### Example 2
Solve: $2x^2 - 4x - 3 = 0$

**Method 1: Quadratic Formula**

$2x^2 - 4x - 3 = 0 \quad \text{(Identify: a = 2, b = -4, c = -3)}$

$\Delta = (-4)^2 - 4(2)(-3) = 16 + 24 = 40 \quad \text{(Calculate discriminant)}$

$x = \frac{4 \pm \sqrt{40}}{4} = \frac{4 \pm 2\sqrt{10}}{4} \quad \text{(Apply formula and simplify)}$

$x = \frac{2 \pm \sqrt{10}}{2} \quad \text{(Reduce fraction)}$

##### Example 3
Solve: $x^2 - 6x + 9 = 0$

**Method 1: Quadratic Formula**

$x^2 - 6x + 9 = 0 \quad \text{(Identify: a = 1, b = -6, c = 9)}$

$\Delta = (-6)^2 - 4(1)(9) = 36 - 36 = 0 \quad \text{(Discriminant is zero)}$

$x = \frac{6 \pm \sqrt{0}}{2} = \frac{6}{2} = 3 \quad \text{(One repeated solution)}$

**Method 2: Recognition of Perfect Square**

$x^2 - 6x + 9 = (x - 3)^2 = 0 \quad \text{(Recognize perfect square)}$

$x = 3 \quad \text{(Double root)}$

#### Multiple Choice Questions

<div id="quadratic-formula-mcq" class="quiz-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Quadratic Formula Quiz",
        questions: [
            {
                text: "For the equation \\(3x^2 + 2x - 1 = 0\\), what is the discriminant?",
                options: ["\\(\\Delta = -8\\)", "\\(\\Delta = 8\\)", "\\(\\Delta = 16\\)", "\\(\\Delta = -16\\)"],
                correctIndex: 2,
                explanation: "\\(\\Delta = b^2 - 4ac = 2^2 - 4(3)(-1) = 4 + 12 = 16\\)",
                difficulty: "Basic"
            },
            {
                text: "If the discriminant of a quadratic equation is 0, how many real solutions does it have?",
                options: ["0", "1", "2", "Infinitely many"],
                correctIndex: 1,
                explanation: "When \\(\\Delta = 0\\), the quadratic has exactly one real solution (a repeated root).",
                difficulty: "Basic"
            },
            {
                text: "For \\(x^2 + 4x + 5 = 0\\), what type of solutions exist?",
                options: ["Two positive real", "Two negative real", "One real", "Two complex conjugate"],
                correctIndex: 3,
                explanation: "\\(\\Delta = 16 - 20 = -4 < 0\\), so there are two complex conjugate solutions.",
                difficulty: "Intermediate"
            },
            {
                text: "If \\(ax^2 + bx + c = 0\\) has solutions \\(x = 2 \\pm \\sqrt{3}\\), what is \\(\\frac{b}{a}\\)?",
                options: ["\\(-4\\)", "\\(4\\)", "\\(-2\\)", "\\(2\\)"],
                correctIndex: 0,
                explanation: "From the quadratic formula, if \\(x = 2 \\pm \\sqrt{3}\\), then \\(\\frac{-b}{2a} = 2\\), so \\(\\frac{b}{a} = -4\\).",
                difficulty: "Advanced"
            }
        ]
    };
    MCQQuiz.create('quadratic-formula-mcq', quizData);
});
</script>

#### Sector Specific Questions: Quadratic Formula Applications

<div id="quadratic-formula-identity-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quadraticFormulaContent = {
        "title": "Quadratic Formula: Applications",
        "intro_content": `<p>The quadratic formula is essential in fields requiring precise calculations where factoring may be impractical. From calculating trajectories to optimizing designs and analyzing financial models, the quadratic formula provides exact solutions efficiently.</p>`,
        "questions": [
            {
                "category": "scientific",
                "title": "Chemistry: Equilibrium Calculations",
                "content": `In a chemical equilibrium, the concentration \\(x\\) (in mol/L) satisfies \\(2x^2 + 3x - 0.5 = 0\\). Find the positive concentration using the quadratic formula.`,
                "answer": `<p>Using the quadratic formula with \\(a = 2\\), \\(b = 3\\), \\(c = -0.5\\):</p>
                <p>\\(\\Delta = 9 - 4(2)(-0.5) = 9 + 4 = 13\\)</p>
                <p>\\(x = \\frac{-3 \\pm \\sqrt{13}}{4}\\)</p>
                <p>\\(x = \\frac{-3 + \\sqrt{13}}{4} \\approx \\frac{-3 + 3.606}{4} \\approx 0.151\\) mol/L</p>
                <p>(We take the positive solution as concentration must be positive)</p>`
            },
            {
                "category": "engineering",
                "title": "Electrical Engineering: RC Circuit",
                "content": `In an RC circuit, the time constant satisfies \\(0.001t^2 - 0.1t + 2 = 0\\) where \\(t\\) is in milliseconds. Find both time values.`,
                "answer": `<p>Using the quadratic formula with \\(a = 0.001\\), \\(b = -0.1\\), \\(c = 2\\):</p>
                <p>\\(\\Delta = 0.01 - 4(0.001)(2) = 0.01 - 0.008 = 0.002\\)</p>
                <p>\\(t = \\frac{0.1 \\pm \\sqrt{0.002}}{0.002} = \\frac{0.1 \\pm 0.0447}{0.002}\\)</p>
                <p>\\(t_1 = \\frac{0.1447}{0.002} = 72.35\\) ms</p>
                <p>\\(t_2 = \\frac{0.0553}{0.002} = 27.65\\) ms</p>`
            },
            {
                "category": "financial",
                "title": "Finance: Investment Returns",
                "content": `An investment grows according to \\(1000(1+r)^2 = 1210\\) where \\(r\\) is the annual return rate. Find \\(r\\) using the quadratic formula.`,
                "answer": `<p>Expanding: \\(1000(1 + 2r + r^2) = 1210\\)</p>
                <p>\\(1000r^2 + 2000r + 1000 = 1210\\)</p>
                <p>\\(1000r^2 + 2000r - 210 = 0\\)</p>
                <p>\\(r^2 + 2r - 0.21 = 0\\)</p>
                <p>Using quadratic formula: \\(r = \\frac{-2 \\pm \\sqrt{4 + 0.84}}{2} = \\frac{-2 \\pm \\sqrt{4.84}}{2}\\)</p>
                <p>\\(r = \\frac{-2 \\pm 2.2}{2}\\)</p>
                <p>\\(r = 0.1\\) or \\(r = -2.1\\)</p>
                <p>The positive rate is \\(r = 0.1 = 10\\%\\) annual return</p>`
            },
            {
                "category": "creative",
                "title": "Computer Graphics: Bezier Curves",
                "content": `A quadratic Bezier curve intersects the line \\(y = 3\\) when \\(2t^2 - 3t + 1 = 0\\), where \\(t\\) is the parameter. Find both intersection parameters.`,
                "answer": `<p>Using the quadratic formula with \\(a = 2\\), \\(b = -3\\), \\(c = 1\\):</p>
                <p>\\(\\Delta = 9 - 8 = 1\\)</p>
                <p>\\(t = \\frac{3 \\pm 1}{4}\\)</p>
                <p>\\(t_1 = \\frac{4}{4} = 1\\)</p>
                <p>\\(t_2 = \\frac{2}{4} = 0.5\\)</p>
                <p>The curve intersects at parameters \\(t = 0.5\\) and \\(t = 1\\)</p>`
            }
        ]
    };
    MathQuestionModule.render(quadraticFormulaContent, 'quadratic-formula-identity-container');
});
</script>

### Key Takeaways

```{important}
1. The quadratic formula $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$ solves any quadratic equation
2. The discriminant $\Delta = b^2 - 4ac$ determines the nature of solutions
3. When $\Delta > 0$: two distinct real solutions
4. When $\Delta = 0$: one repeated real solution
5. When $\Delta < 0$: two complex conjugate solutions
6. The quadratic formula is derived by completing the square on $ax^2 + bx + c = 0$
7. Always simplify the final answer by reducing fractions and simplifying radicals
8. The quadratic formula works even when factoring is difficult or impossible
```

