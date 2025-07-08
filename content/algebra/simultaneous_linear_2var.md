# Simultaneous Linear Equations (2 Variables)

## Linear Equations Revision

### Theory

Before solving systems of linear equations, let's review single linear equations. A linear equation in one variable has the form:

$$ax + b = 0$$

where $a \neq 0$. The solution is $x = -\frac{b}{a}$.

For two variables, a linear equation takes the form:

$$ax + by = c$$

This represents a straight line in the coordinate plane. A single linear equation in two variables has infinitely many solutions - all the points on the line.

### Application

#### Examples

##### Example 1
Find three solutions to: $2x + 3y = 12$

**Solution:**

$2x + 3y = 12 \quad \text{(Choose values for x and solve for y)}$

When $x = 0$: $3y = 12$, so $y = 4 \quad \text{(Solution: (0, 4))}$

When $x = 3$: $6 + 3y = 12$, so $y = 2 \quad \text{(Solution: (3, 2))}$

When $x = 6$: $12 + 3y = 12$, so $y = 0 \quad \text{(Solution: (6, 0))}$

#### Interactive Visualization: Linear Equations in Two Variables

<div id="linear-2var-revision-container" class="visualization-container" style="height: 500px;"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    MathVisualizer.createGraphFromDescription('linear-2var-revision-container', {
        boundingBox: [-5, 5, 5, -5],
        theme: 'light',
        useSequentialColors: true,
        infoBox: {
            title: "Linear Equation in Two Variables",
            lines: [
                {text: "ax + by = c", dynamic: false},
                {text: "a: ${a}, b: ${b}, c: ${c}", dynamic: true},
                {text: "x-intercept: ${b !== 0 ? (c/a).toFixed(2) : 'N/A'}", dynamic: true},
                {text: "y-intercept: ${b !== 0 ? (c/b).toFixed(2) : 'N/A'}", dynamic: true}
            ],
            position: {top: 55, left: 20}
        },
        parametrizedFunctions: [
            {
                expression: 'b !== 0 ? (c - a*x)/b : 0',
                title: 'Linear Equation',
                parameters: {
                    a: { min: -3, max: 3, value: 2, step: 0.1 },
                    b: { min: -3, max: 3, value: 1, step: 0.1 },
                    c: { min: -5, max: 5, value: 3, step: 0.1 }
                },
                features: ['zeros']
            }
        ]
    });
});
</script>

#### Multiple Choice Questions

<div id="linear-2var-revision-mcq" class="quiz-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Linear Equations (2 Variables) Review",
        questions: [
            {
                text: "How many solutions does \\(3x + 2y = 6\\) have?",
                options: ["0", "1", "2", "Infinitely many"],
                correctIndex: 3,
                explanation: "A single linear equation in two variables represents a line, which contains infinitely many points (solutions).",
                difficulty: "Basic"
            },
            {
                text: "What is the y-intercept of \\(4x - 2y = 8\\)?",
                options: ["\\((0, -4)\\)", "\\((0, 4)\\)", "\\((2, 0)\\)", "\\((-2, 0)\\)"],
                correctIndex: 0,
                explanation: "Set \\(x = 0\\): \\(-2y = 8\\), so \\(y = -4\\). The y-intercept is \\((0, -4)\\).",
                difficulty: "Basic"
            }
        ]
    };
    MCQQuiz.create('linear-2var-revision-mcq', quizData);
});
</script>

## Simultaneous Linear Equations (2 Variables)

### Theory

A system of simultaneous linear equations consists of two or more linear equations that must be satisfied at the same time. For two equations in two variables:

$$\begin{align}
a_1x + b_1y &= c_1 \\
a_2x + b_2y &= c_2
\end{align}$$

The solution is the point $(x, y)$ where both lines intersect. There are three possible outcomes:

1. **Unique Solution**: Lines intersect at exactly one point
2. **No Solution**: Lines are parallel (inconsistent system)
3. **Infinitely Many Solutions**: Lines are identical (dependent system)

The main methods for solving simultaneous linear equations are:

1. **Graphical Method**: Plot both lines and find their intersection
2. **Substitution Method**: Solve one equation for a variable and substitute
3. **Elimination Method**: Add or subtract equations to eliminate a variable
4. **Matrix Method**: Use matrices and row operations

```{tip}
Always check your solution by substituting the values back into both original equations. This verifies correctness and catches arithmetic errors.
```

#### Interactive Visualization: Simultaneous Linear Equations

<div id="simultaneous-linear-2var-container" class="visualization-container" style="height: 500px;"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    MathVisualizer.createGraphFromDescription('simultaneous-linear-2var-container', {
        boundingBox: [-5, 5, 5, -5],
        theme: 'light',
        useSequentialColors: true,
        infoBox: {
            title: "Simultaneous Linear Equations",
            lines: [
                {text: "Eq1: ${a1}x + ${b1}y = ${c1}", dynamic: true},
                {text: "Eq2: ${a2}x + ${b2}y = ${c2}", dynamic: true},
                {text: "Intersection: ${Math.abs(a1*b2 - a2*b1) > 0.01 ? '(' + ((c1*b2-c2*b1)/(a1*b2-a2*b1)).toFixed(2) + ', ' + ((a1*c2-a2*c1)/(a1*b2-a2*b1)).toFixed(2) + ')' : 'Parallel/Same'}", dynamic: true}
            ],
            position: {top: 55, left: 20}
        },
        parametrizedFunctions: [
            {
                expression: 'b1 !== 0 ? (c1 - a1*x)/b1 : 0',
                title: 'Equation 1',
                parameters: {
                    a1: { min: -3, max: 3, value: 1, step: 0.1 },
                    b1: { min: -3, max: 3, value: 1, step: 0.1 },
                    c1: { min: -5, max: 5, value: 2, step: 0.1 }
                },
                features: []
            },
            {
                expression: 'b2 !== 0 ? (c2 - a2*x)/b2 : 0',
                title: 'Equation 2',
                parameters: {
                    a2: { min: -3, max: 3, value: 2, step: 0.1 },
                    b2: { min: -3, max: 3, value: -1, step: 0.1 },
                    c2: { min: -5, max: 5, value: 1, step: 0.1 }
                },
                features: []
            }
        ]
    });
});
</script>

### Application

#### Examples

##### Example 1
Solve by substitution: $\begin{cases} x + 2y = 7 \\ 3x - y = 4 \end{cases}$

**Method 1: Substitution**

$x + 2y = 7 \quad \text{(Solve for x in terms of y)}$

$x = 7 - 2y \quad \text{(Substitute into second equation)}$

$3(7 - 2y) - y = 4 \quad \text{(Expand and simplify)}$

$21 - 6y - y = 4 \quad \text{(Combine like terms)}$

$21 - 7y = 4 \quad \text{(Solve for y)}$

$-7y = -17$, so $y = \frac{17}{7} \quad \text{(Find x)}$

$x = 7 - 2(\frac{17}{7}) = 7 - \frac{34}{7} = \frac{15}{7} \quad \text{(Solution: $(\frac{15}{7}, \frac{17}{7})$)}$

##### Example 2
Solve by elimination: $\begin{cases} 2x + 3y = 11 \\ 5x - 2y = 4 \end{cases}$

**Method 1: Elimination**

$\begin{cases} 2x + 3y = 11 \\ 5x - 2y = 4 \end{cases} \quad \text{(Multiply first by 2, second by 3)}$

$\begin{cases} 4x + 6y = 22 \\ 15x - 6y = 12 \end{cases} \quad \text{(Add equations to eliminate y)}$

$19x = 34 \quad \text{(Solve for x)}$

$x = \frac{34}{19} = \frac{34}{19} \quad \text{(Substitute back)}$

$2(\frac{34}{19}) + 3y = 11 \quad \text{(Solve for y)}$

$\frac{68}{19} + 3y = 11$, so $3y = \frac{209 - 68}{19} = \frac{141}{19}$

$y = \frac{47}{19} \quad \text{(Solution: $(\frac{34}{19}, \frac{47}{19})$)}$

##### Example 3
Identify the nature of the system: $\begin{cases} 2x + 4y = 6 \\ x + 2y = 3 \end{cases}$

**Method 1: Analysis**

$2x + 4y = 6 \quad \text{(Divide by 2)}$

$x + 2y = 3 \quad \text{(Compare with second equation)}$

$x + 2y = 3 \quad \text{(Both equations are identical)}$

Therefore, the system has infinitely many solutions. All points on the line $x + 2y = 3$ are solutions.

#### Multiple Choice Questions

<div id="simultaneous-linear-2var-mcq" class="quiz-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Simultaneous Linear Equations Quiz",
        questions: [
            {
                text: "What is the solution to \\(\\begin{cases} x + y = 5 \\\\ x - y = 1 \\end{cases}\\)?",
                options: ["\\((3, 2)\\)", "\\((2, 3)\\)", "\\((4, 1)\\)", "\\((1, 4)\\)"],
                correctIndex: 0,
                explanation: "Adding the equations: \\(2x = 6\\), so \\(x = 3\\). Substituting: \\(3 + y = 5\\), so \\(y = 2\\).",
                difficulty: "Basic"
            },
            {
                text: "For what value of \\(k\\) does \\(\\begin{cases} 2x + 3y = 6 \\\\ 4x + 6y = k \\end{cases}\\) have infinitely many solutions?",
                options: ["\\(k = 6\\)", "\\(k = 12\\)", "\\(k = 18\\)", "\\(k = 24\\)"],
                correctIndex: 1,
                explanation: "For infinitely many solutions, the second equation must be a multiple of the first. Since \\(4x + 6y = 2(2x + 3y)\\), we need \\(k = 2 \\times 6 = 12\\).",
                difficulty: "Intermediate"
            },
            {
                text: "Which system has no solution?",
                options: ["\\(\\begin{cases} x + y = 2 \\\\ x - y = 0 \\end{cases}\\)", "\\(\\begin{cases} 2x + y = 3 \\\\ 4x + 2y = 6 \\end{cases}\\)", "\\(\\begin{cases} x + 2y = 4 \\\\ 2x + 4y = 9 \\end{cases}\\)", "\\(\\begin{cases} 3x - y = 1 \\\\ x + y = 3 \\end{cases}\\)"],
                correctIndex: 2,
                explanation: "In option C, the second equation is not consistent with twice the first equation: \\(2(x + 2y) = 2x + 4y = 8 \\neq 9\\).",
                difficulty: "Advanced"
            },
            {
                text: "Using elimination, what should you multiply the first equation by to eliminate \\(x\\) in \\(\\begin{cases} 3x + 2y = 7 \\\\ 5x - 4y = 1 \\end{cases}\\)?",
                options: ["\\(5\\)", "\\(-5\\)", "\\(\\frac{5}{3}\\)", "\\(-\\frac{5}{3}\\)"],
                correctIndex: 3,
                explanation: "To eliminate \\(x\\), we want the coefficients to be opposites. Multiply first equation by \\(-\\frac{5}{3}\\) to get \\(-5x\\), which will cancel with \\(5x\\) in the second equation.",
                difficulty: "Advanced"
            }
        ]
    };
    MCQQuiz.create('simultaneous-linear-2var-mcq', quizData);
});
</script>

#### Sector Specific Questions: Simultaneous Linear Equations Applications

<div id="simultaneous-linear-2var-identity-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const simultaneousLinear2varContent = {
        "title": "Simultaneous Linear Equations: Applications",
        "intro_content": `<p>Simultaneous linear equations model situations where multiple constraints must be satisfied simultaneously. From balancing chemical equations to optimizing resource allocation and analyzing economic equilibrium, these systems provide powerful tools for solving complex real-world problems.</p>`,
        "questions": [
            {
                "category": "scientific",
                "title": "Chemistry: Solution Mixing",
                "content": `A chemist needs to create 500ml of a 15% acid solution by mixing a 10% solution with a 25% solution. Let \\(x\\) be ml of 10% solution and \\(y\\) be ml of 25% solution. Set up and solve the system.`,
                "answer": `<p>Set up the system of equations:</p>
                <p>Volume constraint: \\(x + y = 500\\)</p>
                <p>Concentration constraint: \\(0.10x + 0.25y = 0.15(500) = 75\\)</p>
                <p>From first equation: \\(x = 500 - y\\)</p>
                <p>Substitute: \\(0.10(500 - y) + 0.25y = 75\\)</p>
                <p>\\(50 - 0.10y + 0.25y = 75\\)</p>
                <p>\\(0.15y = 25\\), so \\(y = \\frac{25}{0.15} = 166.67\\) ml</p>
                <p>\\(x = 500 - 166.67 = 333.33\\) ml</p>
                <p>Mix 333.33ml of 10% solution with 166.67ml of 25% solution</p>`
            },
            {
                "category": "engineering",
                "title": "Electrical Engineering: Circuit Analysis",
                "content": `In a circuit with two loops, Kirchhoff's laws give: \\(2I_1 + 3I_2 = 12\\) and \\(I_1 - I_2 = 2\\), where \\(I_1\\) and \\(I_2\\) are currents in amperes. Find both currents.`,
                "answer": `<p>System: \\(\\begin{cases} 2I_1 + 3I_2 = 12 \\\\ I_1 - I_2 = 2 \\end{cases}\\)</p>
                <p>From second equation: \\(I_1 = I_2 + 2\\)</p>
                <p>Substitute into first: \\(2(I_2 + 2) + 3I_2 = 12\\)</p>
                <p>\\(2I_2 + 4 + 3I_2 = 12\\)</p>
                <p>\\(5I_2 = 8\\), so \\(I_2 = 1.6\\) A</p>
                <p>\\(I_1 = 1.6 + 2 = 3.6\\) A</p>
                <p>The currents are \\(I_1 = 3.6\\) A and \\(I_2 = 1.6\\) A</p>`
            },
            {
                "category": "financial",
                "title": "Business: Production Planning",
                "content": `A company produces chairs and tables. Each chair requires 2 hours of labor and 3 units of material. Each table requires 4 hours of labor and 2 units of material. With 40 hours of labor and 36 units of material available, how many chairs (\\(x\\)) and tables (\\(y\\)) can be produced to use all resources?`,
                "answer": `<p>System of equations:</p>
                <p>Labor constraint: \\(2x + 4y = 40\\)</p>
                <p>Material constraint: \\(3x + 2y = 36\\)</p>
                <p>From first equation: \\(x + 2y = 20\\), so \\(x = 20 - 2y\\)</p>
                <p>Substitute: \\(3(20 - 2y) + 2y = 36\\)</p>
                <p>\\(60 - 6y + 2y = 36\\)</p>
                <p>\\(-4y = -24\\), so \\(y = 6\\)</p>
                <p>\\(x = 20 - 2(6) = 8\\)</p>
                <p>Produce 8 chairs and 6 tables</p>`
            },
            {
                "category": "creative",
                "title": "Game Design: Resource Balance",
                "content": `In a strategy game, a player has gold coins (\\(g\\)) and gems (\\(m\\)). Buying a sword costs 3 gold and 2 gems, while a shield costs 1 gold and 4 gems. If the player spends all 25 gold and 30 gems on swords and shields, how many of each did they buy?`,
                "answer": `<p>Let \\(s\\) = number of swords, \\(h\\) = number of shields</p>
                <p>Gold constraint: \\(3s + h = 25\\)</p>
                <p>Gem constraint: \\(2s + 4h = 30\\)</p>
                <p>From first equation: \\(h = 25 - 3s\\)</p>
                <p>Substitute: \\(2s + 4(25 - 3s) = 30\\)</p>
                <p>\\(2s + 100 - 12s = 30\\)</p>
                <p>\\(-10s = -70\\), so \\(s = 7\\)</p>
                <p>\\(h = 25 - 3(7) = 4\\)</p>
                <p>The player bought 7 swords and 4 shields</p>`
            }
        ]
    };
    MathQuestionModule.render(simultaneousLinear2varContent, 'simultaneous-linear-2var-identity-container');
});
</script>

### Key Takeaways

```{important}
1. A system of two linear equations in two variables can have one solution, no solution, or infinitely many solutions
2. Graphically, the solution is where the two lines intersect
3. Substitution method: solve one equation for a variable and substitute into the other
4. Elimination method: add or subtract equations to eliminate a variable
5. For unique solution: lines intersect at one point (different slopes)
6. For no solution: lines are parallel (same slope, different y-intercepts)
7. For infinitely many solutions: lines are identical (same slope and y-intercept)
8. Always verify solutions by substituting back into both original equations
```

