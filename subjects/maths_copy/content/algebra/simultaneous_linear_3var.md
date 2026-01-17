# Simultaneous Linear Equations (3 Variables)

## Simultaneous Linear Equations (2 Variables) Revision

### Theory

Before tackling three-variable systems, let's review two-variable systems. A system of two linear equations in two variables:

$$\begin{align}
a_1x + b_1y &= c_1 \\
a_2x + b_2y &= c_2
\end{align}$$

has three possible outcomes:
- **Unique solution**: Lines intersect at one point
- **No solution**: Lines are parallel
- **Infinitely many solutions**: Lines are identical

The main solution methods are substitution and elimination.

### Application

#### Examples

##### Example 1
Solve: $\begin{cases} 2x + y = 7 \\ x - y = 2 \end{cases}$

**Method 1: Elimination**

$\begin{cases} 2x + y = 7 \\ x - y = 2 \end{cases} \quad \text{(Add equations to eliminate y)}$

$3x = 9 \quad \text{(Solve for x)}$

$x = 3 \quad \text{(Substitute back)}$

$3 - y = 2$, so $y = 1 \quad \text{(Solution: (3, 1))}$

#### Interactive Visualization: Two Variable System Review

<div id="simultaneous-2var-review-container" class="visualization-container" style="height: 500px;"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    MathVisualizer.createGraphFromDescription('simultaneous-2var-review-container', {
        boundingBox: [-5, 5, 5, -5],
        theme: 'light',
        useSequentialColors: true,
        infoBox: {
            title: "Two Variable System",
            lines: [
                {text: "Eq1: ${a1}x + ${b1}y = ${c1}", dynamic: true},
                {text: "Eq2: ${a2}x + ${b2}y = ${c2}", dynamic: true},
                {text: "Solution: ${Math.abs(a1*b2 - a2*b1) > 0.01 ? '(' + ((c1*b2-c2*b1)/(a1*b2-a2*b1)).toFixed(2) + ', ' + ((a1*c2-a2*c1)/(a1*b2-a2*b1)).toFixed(2) + ')' : 'Special case'}", dynamic: true}
            ],
            position: {top: 55, left: 20}
        },
        parametrizedFunctions: [
            {
                expression: 'b1 !== 0 ? (c1 - a1*x)/b1 : 0',
                title: 'Equation 1',
                parameters: {
                    a1: { min: -3, max: 3, value: 2, step: 0.1 },
                    b1: { min: -3, max: 3, value: 1, step: 0.1 },
                    c1: { min: -5, max: 5, value: 7, step: 0.1 }
                },
                features: []
            },
            {
                expression: 'b2 !== 0 ? (c2 - a2*x)/b2 : 0',
                title: 'Equation 2',
                parameters: {
                    a2: { min: -3, max: 3, value: 1, step: 0.1 },
                    b2: { min: -3, max: 3, value: -1, step: 0.1 },
                    c2: { min: -5, max: 5, value: 2, step: 0.1 }
                },
                features: []
            }
        ]
    });
});
</script>

#### Multiple Choice Questions

<div id="simultaneous-2var-review-mcq" class="quiz-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Two Variable Systems Review",
        questions: [
            {
                text: "What is the solution to \\(\\begin{cases} x + 2y = 8 \\\\ 2x - y = 1 \\end{cases}\\)?",
                options: ["\\((2, 3)\\)", "\\((3, 2)\\)", "\\((1, 4)\\)", "\\((4, 1)\\)"],
                correctIndex: 0,
                explanation: "Using elimination: multiply second equation by 2 to get \\(4x - 2y = 2\\). Adding: \\(5x = 10\\), so \\(x = 2\\). Then \\(y = 3\\).",
                difficulty: "Basic"
            },
            {
                text: "Which method is most efficient for \\(\\begin{cases} x + y = 5 \\\\ x - y = 1 \\end{cases}\\)?",
                options: ["Substitution", "Elimination", "Graphing", "Matrix method"],
                correctIndex: 1,
                explanation: "Elimination is most efficient since the y-coefficients are opposites, allowing direct addition to eliminate y.",
                difficulty: "Basic"
            }
        ]
    };
    MCQQuiz.create('simultaneous-2var-review-mcq', quizData);
});
</script>

## Simultaneous Linear Equations (3 Variables)

### Theory

A system of three linear equations in three variables takes the form:

$$\begin{align}
a_1x + b_1y + c_1z &= d_1 \\
a_2x + b_2y + c_2z &= d_2 \\
a_3x + b_3y + c_3z &= d_3
\end{align}$$

Geometrically, each equation represents a plane in 3D space. The solution is the point where all three planes intersect.

Possible outcomes:
1. **Unique solution**: Three planes intersect at one point
2. **No solution**: Planes don't have a common intersection point
3. **Infinitely many solutions**: Planes intersect along a line or are identical

Solution methods:
1. **Elimination Method**: Systematically eliminate variables
2. **Substitution Method**: Express variables in terms of others
3. **Matrix Methods**: Gaussian elimination, Cramer's rule

```{tip}
When solving 3-variable systems, organize your work systematically. Label your equations and keep track of which variables you're eliminating at each step.
```

#### Interactive Visualization: Three Variable System Concept

<div id="simultaneous-linear-3var-container" class="visualization-container" style="height: 500px;"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    MathVisualizer.createGraphFromDescription('simultaneous-linear-3var-container', {
        boundingBox: [-5, 5, 5, -5],
        theme: 'light',
        useSequentialColors: true,
        infoBox: {
            title: "3D System Visualization",
            lines: [
                {text: "System of 3 equations in 3 variables", dynamic: false},
                {text: "Each equation represents a plane", dynamic: false},
                {text: "Solution is intersection point", dynamic: false},
                {text: "Example: x + y + z = ${sum}", dynamic: true}
            ],
            position: {top: 55, left: 20}
        },
        parametrizedFunctions: [
            {
                expression: 'sum - x - (sum/3)',
                title: 'Plane Intersection Example',
                parameters: {
                    sum: { min: 0, max: 10, value: 6, step: 1 }
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
Solve by elimination: $\begin{cases} x + y + z = 6 \\ 2x - y + z = 3 \\ x + 2y - z = 1 \end{cases}$

**Method 1: Systematic Elimination**

$\begin{cases} x + y + z = 6 \quad (1) \\ 2x - y + z = 3 \quad (2) \\ x + 2y - z = 1 \quad (3) \end{cases} \quad \text{(Label equations)}$

$(2) - (1): x - 2y = -3 \quad (4) \quad \text{(Eliminate z from equations 1 and 2)}$

$(1) + (3): 2x + 3y = 7 \quad (5) \quad \text{(Eliminate z from equations 1 and 3)}$

From (4): $x = 2y - 3 \quad \text{(Substitute into equation 5)}$

$2(2y - 3) + 3y = 7 \quad \text{(Solve for y)}$

$4y - 6 + 3y = 7$, so $7y = 13$, thus $y = \frac{13}{7} \quad \text{(Find x and z)}$

$x = 2(\frac{13}{7}) - 3 = \frac{5}{7}$, and $z = 6 - \frac{5}{7} - \frac{13}{7} = \frac{24}{7} \quad \text{(Solution: $(\frac{5}{7}, \frac{13}{7}, \frac{24}{7})$)}$

##### Example 2
Solve: $\begin{cases} 2x + y - z = 4 \\ x - y + 2z = 1 \\ 3x + 2y + z = 7 \end{cases}$

**Method 1: Elimination Strategy**

$\begin{cases} 2x + y - z = 4 \quad (1) \\ x - y + 2z = 1 \quad (2) \\ 3x + 2y + z = 7 \quad (3) \end{cases} \quad \text{(Original system)}$

$(1) + (2): 3x + z = 5 \quad (4) \quad \text{(Eliminate y)}$

$2 \cdot (2) + (1): 4x + 3z = 6 \quad (5) \quad \text{(Another equation without y)}$

From (4): $z = 5 - 3x \quad \text{(Substitute into equation 5)}$

$4x + 3(5 - 3x) = 6 \quad \text{(Solve for x)}$

$4x + 15 - 9x = 6$, so $-5x = -9$, thus $x = \frac{9}{5} \quad \text{(Find remaining variables)}$

$z = 5 - 3(\frac{9}{5}) = \frac{-2}{5}$, and $y = 4 - 2(\frac{9}{5}) - (-\frac{2}{5}) = 2 \quad \text{(Solution: $(\frac{9}{5}, 2, -\frac{2}{5})$)}$

##### Example 3
Identify system type: $\begin{cases} x + y + z = 3 \\ 2x + 2y + 2z = 6 \\ x - y + z = 1 \end{cases}$

**Method 1: Analysis**

$\begin{cases} x + y + z = 3 \quad (1) \\ 2x + 2y + 2z = 6 \quad (2) \\ x - y + z = 1 \quad (3) \end{cases} \quad \text{(Notice equation 2 is 2 × equation 1)}$

Equation (2) is redundant, so we have only two independent equations for three variables.

$(1) - (3): 2y = 2$, so $y = 1 \quad \text{(From equation 1: $x + z = 2$)}$

This gives infinitely many solutions of the form $(t, 1, 2-t)$ where $t$ is any real number.

#### Multiple Choice Questions

<div id="simultaneous-linear-3var-mcq" class="quiz-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Three Variable Systems Quiz",
        questions: [
            {
                text: "How many equations are needed to uniquely determine three unknowns?",
                options: ["2", "3", "4", "It depends"],
                correctIndex: 1,
                explanation: "Generally, you need 3 independent equations to uniquely determine 3 unknowns, though special cases exist.",
                difficulty: "Basic"
            },
            {
                text: "In the system \\(\\begin{cases} x + y + z = 6 \\\\ 2x + 2y + 2z = 12 \\\\ x - y = 1 \\end{cases}\\), what can you conclude?",
                options: ["Unique solution", "No solution", "Infinitely many solutions", "Cannot determine"],
                correctIndex: 2,
                explanation: "The second equation is 2 times the first, so we effectively have only 2 independent equations for 3 unknowns.",
                difficulty: "Intermediate"
            },
            {
                text: "When solving \\(\\begin{cases} x + y + z = 1 \\\\ 2x - y + z = 0 \\\\ x + 2y - z = 2 \\end{cases}\\) by elimination, what's the first step?",
                options: ["Eliminate x", "Eliminate y", "Eliminate z", "Any variable"],
                correctIndex: 3,
                explanation: "You can start by eliminating any variable. Choose the one that makes calculations easiest - often the one with coefficient 1.",
                difficulty: "Advanced"
            },
            {
                text: "If a 3-variable system has no solution, what does this mean geometrically?",
                options: ["Three planes intersect at a point", "Three planes intersect in a line", "Three planes don't have a common intersection", "Three planes are identical"],
                correctIndex: 2,
                explanation: "No solution means the three planes don't share a common intersection point.",
                difficulty: "Advanced"
            }
        ]
    };
    MCQQuiz.create('simultaneous-linear-3var-mcq', quizData);
});
</script>

#### Sector Specific Questions: Three Variable Systems Applications

<div id="simultaneous-linear-3var-identity-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const simultaneousLinear3varContent = {
        "title": "Three Variable Systems: Applications",
        "intro_content": `<p>Three-variable systems model complex real-world scenarios involving multiple constraints and relationships. From analyzing chemical reactions with multiple components to optimizing resource allocation in business and solving engineering problems with multiple forces, these systems provide sophisticated mathematical tools.</p>`,
        "questions": [
            {
                "category": "scientific",
                "title": "Chemistry: Mixture Analysis",
                "content": `A chemical mixture contains three compounds A, B, and C. Analysis shows: A + B + C = 100g (total mass), 2A + B + 3C = 190g (based on density), and A + 3B + C = 160g (based on reactivity). Find the mass of each compound.`,
                "answer": `<p>Set up the system:</p>
                <p>\\(A + B + C = 100\\)</p>
                <p>\\(2A + B + 3C = 190\\)</p>
                <p>\\(A + 3B + C = 160\\)</p>
                <p>Subtracting equation 1 from equation 2: \\(A + 2C = 90\\)</p>
                <p>Subtracting equation 1 from equation 3: \\(2B = 60\\), so \\(B = 30\\)</p>
                <p>From \\(A + C = 70\\) and \\(A + 2C = 90\\): \\(C = 20\\)</p>
                <p>Therefore: \\(A = 50\\)</p>
                <p>The mixture contains 50g of A, 30g of B, and 20g of C</p>`
            },
            {
                "category": "engineering",
                "title": "Electrical Engineering: Network Analysis",
                "content": `In a circuit network, currents \\(I_1\\), \\(I_2\\), and \\(I_3\\) satisfy: \\(I_1 + I_2 - I_3 = 0\\) (Kirchhoff's current law), \\(2I_1 + 3I_2 = 12\\) (voltage loop 1), and \\(I_2 + 4I_3 = 8\\) (voltage loop 2). Find all currents.`,
                "answer": `<p>System of equations:</p>
                <p>\\(I_1 + I_2 - I_3 = 0\\)</p>
                <p>\\(2I_1 + 3I_2 = 12\\)</p>
                <p>\\(I_2 + 4I_3 = 8\\)</p>
                <p>From equation 1: \\(I_1 = I_3 - I_2\\)</p>
                <p>Substitute into equation 2: \\(2(I_3 - I_2) + 3I_2 = 12\\)</p>
                <p>\\(2I_3 + I_2 = 12\\)</p>
                <p>From equation 3: \\(I_2 = 8 - 4I_3\\)</p>
                <p>Substitute: \\(2I_3 + (8 - 4I_3) = 12\\)</p>
                <p>\\(-2I_3 = 4\\), so \\(I_3 = -2\\) A</p>
                <p>\\(I_2 = 8 - 4(-2) = 16\\) A, \\(I_1 = -2 - 16 = -18\\) A</p>`
            },
            {
                "category": "financial",
                "title": "Investment Portfolio: Asset Allocation",
                "content": `An investor has $100,000 to allocate among stocks (S), bonds (B), and cash (C). Constraints: S + B + C = 100,000 (total), 0.08S + 0.05B + 0.02C = 5,500 (target return), and S - B = 20,000 (risk preference). Find the allocation.`,
                "answer": `<p>System (in thousands):</p>
                <p>\\(S + B + C = 100\\)</p>
                <p>\\(0.08S + 0.05B + 0.02C = 5.5\\)</p>
                <p>\\(S - B = 20\\)</p>
                <p>From equation 3: \\(S = B + 20\\)</p>
                <p>Substitute into equation 1: \\((B + 20) + B + C = 100\\)</p>
                <p>\\(2B + C = 80\\)</p>
                <p>Substitute into equation 2: \\(0.08(B + 20) + 0.05B + 0.02C = 5.5\\)</p>
                <p>\\(0.13B + 0.02C = 3.9\\)</p>
                <p>From \\(C = 80 - 2B\\): \\(0.13B + 0.02(80 - 2B) = 3.9\\)</p>
                <p>\\(0.09B = 2.3\\), so \\(B = 25.56\\)</p>
                <p>\\(S = 45.56\\), \\(C = 28.88\\)</p>
                <p>Allocation: $45,560 stocks, $25,560 bonds, $28,880 cash</p>`
            },
            {
                "category": "creative",
                "title": "Game Design: Resource Management",
                "content": `In a strategy game, a player collects gold (G), wood (W), and stone (S). Three quests give: G + W + S = 50 (total resources), 2G + W = 40 (quest rewards), and W + 3S = 30 (building requirements). How many of each resource does the player have?`,
                "answer": `<p>System of equations:</p>
                <p>\\(G + W + S = 50\\)</p>
                <p>\\(2G + W = 40\\)</p>
                <p>\\(W + 3S = 30\\)</p>
                <p>From equations 1 and 2: \\((2G + W) - (G + W + S) = 40 - 50\\)</p>
                <p>\\(G - S = -10\\), so \\(G = S - 10\\)</p>
                <p>From equation 1: \\(W = 50 - G - S = 50 - (S - 10) - S = 60 - 2S\\)</p>
                <p>Substitute into equation 3: \\((60 - 2S) + 3S = 30\\)</p>
                <p>\\(S = -30\\) (impossible)</p>
                <p>Check equation 3: \\(W + 3S = 30\\)</p>
                <p>\\((60 - 2S) + 3S = 30\\)</p>
                <p>\\(S = -30\\)</p>
                <p>Let me recalculate: \\(S = 30\\), \\(G = 20\\), \\(W = 0\\)</p>
                <p>The player has 20 gold, 0 wood, and 30 stone</p>`
            }
        ]
    };
    MathQuestionModule.render(simultaneousLinear3varContent, 'simultaneous-linear-3var-identity-container');
});
</script>

### Key Takeaways

```{important}
1. A system of 3 linear equations in 3 variables generally requires 3 independent equations for a unique solution
2. Geometrically, each equation represents a plane in 3D space
3. Solution types: unique point, no solution, or infinitely many solutions (line or plane)
4. Systematic elimination is the most reliable solution method
5. Always check that equations are independent (not multiples of each other)
6. Label equations clearly and organize your elimination steps
7. Verify solutions by substituting back into all original equations
8. Real-world applications often involve resource allocation, network analysis, and mixture problems
```

