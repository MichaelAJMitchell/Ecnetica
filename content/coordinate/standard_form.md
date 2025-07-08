# Standard Form of a Line

<iframe 
    src="https://drive.google.com/file/d/1_standard_form_line_LC/preview" 
    width="100%" 
    height="480" 
    frameborder="0" 
    allowfullscreen>
</iframe>

## Linear Equations Revision

### Theory
Before exploring standard form, let's review linear equations:
- Slope-intercept form: $y = mx + b$ where $m$ is slope and $b$ is y-intercept
- Point-slope form: $y - y_1 = m(x - x_1)$ for line through $(x_1, y_1)$ with slope $m$
- Every linear equation represents a straight line

### Application
The line $y = 2x + 3$ has:
- Slope: $m = 2$
- Y-intercept: $(0, 3)$

## Standard Form of a Line

### Theory

The standard form of a linear equation is:
$$Ax + By + C = 0$$

where $A$, $B$, and $C$ are constants, and conventionally:
- $A$ and $B$ are not both zero
- $A$ is non-negative (if $A = 0$, then $B > 0$)
- $A$, $B$, and $C$ have no common factor (reduced form)

#### Converting Between Forms

**From Slope-Intercept to Standard:**
$y = mx + b$ becomes $mx - y + b = 0$

**From Standard to Slope-Intercept:**
$Ax + By + C = 0$ becomes $y = -\frac{A}{B}x - \frac{C}{B}$ (if $B \neq 0$)

#### Key Properties
1. **Slope**: $m = -\frac{A}{B}$ (when $B \neq 0$)
2. **X-intercept**: $\left(-\frac{C}{A}, 0\right)$ (when $A \neq 0$)
3. **Y-intercept**: $\left(0, -\frac{C}{B}\right)$ (when $B \neq 0$)
4. **Special Cases**:
   - Vertical line: $x = k$ → $x - k = 0$ (B = 0)
   - Horizontal line: $y = k$ → $y - k = 0$ (A = 0)

#### Interactive Visualization: Standard Form Explorer

<div id="standard-form-explorer" class="visualization-container" style="height: 500px;"></div>
<script>
document.addEventListener('DOMContentLoaded', function() {
    MathVisualizer.createGraphFromDescription('standard-form-explorer', {
        boundingBox: [-10, 10, 10, -10],
        elements: [
            {type: 'line', equation: function(params) {
                return params.A + '*x + ' + params.B + '*y + ' + params.C + ' = 0';
            }, style: {strokeColor: 'blue', strokeWidth: 2}},
            {type: 'point', coords: function(params) {
                if (params.A !== 0) return [-params.C/params.A, 0];
                return [0, 0];
            }, visible: function(params) { return params.A !== 0; },
            name: 'X-int', color: 'red', label: 'X-intercept'},
            {type: 'point', coords: function(params) {
                if (params.B !== 0) return [0, -params.C/params.B];
                return [0, 0];
            }, visible: function(params) { return params.B !== 0; },
            name: 'Y-int', color: 'green', label: 'Y-intercept'}
        ],
        parameters: {
            A: {min: -5, max: 5, value: 2, step: 1, label: "Coefficient A"},
            B: {min: -5, max: 5, value: 3, step: 1, label: "Coefficient B"},
            C: {min: -10, max: 10, value: -6, step: 1, label: "Constant C"}
        },
        infoBox: {
            title: "Standard Form Properties",
            lines: [
                {text: "Equation: ${A}x + ${B}y + ${C} = 0", dynamic: true},
                {text: function(params) {
                    if (params.B === 0) return "Vertical line";
                    if (params.A === 0) return "Horizontal line";
                    return "Slope: " + (-params.A/params.B).toFixed(2);
                }, dynamic: true}
            ]
        }
    });
});
</script>

### Application

#### Examples

**Example 1: Converting to Standard Form**
Convert $y = \frac{3}{4}x - 2$ to standard form with integer coefficients.

**Solution:**
Starting with $y = \frac{3}{4}x - 2$:
- Multiply by 4: $4y = 3x - 8$
- Rearrange: $3x - 4y - 8 = 0$

This is in standard form with $A = 3$, $B = -4$, $C = -8$.

**Example 2: Finding Line Through Two Points**
Find the standard form equation of the line through $(2, 5)$ and $(6, -3)$.

**Solution:**
First find the slope:
$m = \frac{-3 - 5}{6 - 2} = \frac{-8}{4} = -2$

Using point-slope form with $(2, 5)$:
$y - 5 = -2(x - 2)$
$y - 5 = -2x + 4$
$2x + y - 9 = 0$

Therefore: $2x + y - 9 = 0$

**Example 3: Finding Perpendicular Line**
Find the standard form equation of the line perpendicular to $3x - 2y + 7 = 0$ passing through $(4, 1)$.

**Solution:**
Original line has slope $m_1 = -\frac{3}{-2} = \frac{3}{2}$

Perpendicular slope: $m_2 = -\frac{1}{m_1} = -\frac{2}{3}$

Using point-slope form:
$y - 1 = -\frac{2}{3}(x - 4)$
$3(y - 1) = -2(x - 4)$
$3y - 3 = -2x + 8$
$2x + 3y - 11 = 0$

#### Multiple Choice Questions

<div id="standard-form-mcq" class="quiz-container"></div>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Standard Form Quiz",
        questions: [
            {
                text: "Convert \\(y = -\\frac{1}{2}x + 3\\) to standard form with integer coefficients.",
                options: ["\\(x + 2y - 6 = 0\\)", "\\(x - 2y + 6 = 0\\)", "\\(2x + y - 3 = 0\\)", "\\(-x + 2y - 6 = 0\\)"],
                correctIndex: 0,
                explanation: "Multiply by 2: \\(2y = -x + 6\\). Rearrange: \\(x + 2y - 6 = 0\\).",
                difficulty: "Basic"
            },
            {
                text: "Find the x-intercept of \\(4x - 3y + 12 = 0\\).",
                options: ["\\((-3, 0)\\)", "\\((3, 0)\\)", "\\((-4, 0)\\)", "\\((4, 0)\\)"],
                correctIndex: 0,
                explanation: "At x-intercept, \\(y = 0\\): \\(4x + 12 = 0\\), so \\(x = -3\\). Point: \\((-3, 0)\\).",
                difficulty: "Basic"
            },
            {
                text: "Which line is parallel to \\(2x + 5y - 10 = 0\\)?",
                options: ["\\(2x + 5y + 3 = 0\\)", "\\(5x + 2y - 10 = 0\\)", "\\(2x - 5y + 7 = 0\\)", "\\(4x + 10y - 5 = 0\\)"],
                correctIndex: 0,
                explanation: "Parallel lines have the same slope. Both \\(2x + 5y - 10 = 0\\) and \\(2x + 5y + 3 = 0\\) have slope \\(-\\frac{2}{5}\\).",
                difficulty: "Intermediate"
            },
            {
                text: "The line \\(Ax + 3y - 6 = 0\\) passes through \\((2, 4)\\). Find \\(A\\).",
                options: ["\\(A = -3\\)", "\\(A = 3\\)", "\\(A = -6\\)", "\\(A = 6\\)"],
                correctIndex: 0,
                explanation: "Substitute \\((2, 4)\\): \\(A(2) + 3(4) - 6 = 0\\). So \\(2A + 12 - 6 = 0\\), giving \\(A = -3\\).",
                difficulty: "Intermediate"
            }
        ]
    };
    MCQQuiz.create('standard-form-mcq', quizData);
});
</script>

#### Sector Specific Questions: Standard Form Applications

<div id="standard-form-identity-container"></div>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const content = {
        "title": "Standard Form: Real-World Applications",
        "intro_content": `<p>The standard form of a line is particularly useful in optimization problems, computer graphics, and analytical geometry. Its symmetric treatment of x and y makes it ideal for many applications.</p>`,
        "questions": [
            {
                "category": "engineering",
                "title": "Structural Load Analysis",
                "content": `A beam's neutral axis under load follows the line \\(3x + 4y - 24 = 0\\) (units in meters). Find where this axis intersects the support boundaries at \\(x = 0\\) (left support) and \\(y = 0\\) (bottom support). What is the length of the beam section between these points?`,
                "answer": `For intersection with left support (\\(x = 0\\)):
\\(3(0) + 4y - 24 = 0\\)
\\(4y = 24\\)
\\(y = 6\\)
Left support intersection: \\((0, 6)\\)

For intersection with bottom support (\\(y = 0\\)):
\\(3x + 4(0) - 24 = 0\\)
\\(3x = 24\\)
\\(x = 8\\)
Bottom support intersection: \\((8, 0)\\)

Length between points:
\\(d = \\sqrt{(8-0)^2 + (0-6)^2} = \\sqrt{64 + 36} = \\sqrt{100} = 10\\) meters

The beam section is 10 meters long between the support points.`
            },
            {
                "category": "scientific",
                "title": "Chemical Reaction Boundary",
                "content": `In a chemical reaction chamber, the boundary between two reagent zones follows \\(5x + 12y - 60 = 0\\) (x and y in cm). A sensor at position \\((4, 3.5)\\) needs to determine which zone it's in. Is the sensor in the positive or negative half-plane relative to this boundary?`,
                "answer": `To determine which side of the line the sensor is on, substitute \\((4, 3.5)\\) into the equation:
\\(5(4) + 12(3.5) - 60\\)
\\(= 20 + 42 - 60\\)
\\(= 2\\)

Since the result is positive (\\(2 > 0\\)), the sensor is in the positive half-plane.

To verify the reagent zones:
- Points where \\(5x + 12y - 60 > 0\\) are in the positive zone
- Points where \\(5x + 12y - 60 < 0\\) are in the negative zone
- The line \\(5x + 12y - 60 = 0\\) is the exact boundary

The sensor at \\((4, 3.5)\\) is in the positive reagent zone.`
            },
            {
                "category": "financial",
                "title": "Break-Even Analysis",
                "content": `A company's break-even line is represented by \\(150x + 200y - 30000 = 0\\), where \\(x\\) is units of Product A and \\(y\\) is units of Product B. Find the break-even points when: (a) only Product A is sold, (b) only Product B is sold, and (c) equal units of both products are sold.`,
                "answer": `(a) Only Product A (\\(y = 0\\)):
\\(150x + 200(0) - 30000 = 0\\)
\\(150x = 30000\\)
\\(x = 200\\) units

(b) Only Product B (\\(x = 0\\)):
\\(150(0) + 200y - 30000 = 0\\)
\\(200y = 30000\\)
\\(y = 150\\) units

(c) Equal units (\\(x = y\\)):
\\(150x + 200x - 30000 = 0\\)
\\(350x = 30000\\)
\\(x = y = \\frac{30000}{350} \\approx 85.7\\) units each

Break-even points:
- 200 units of Product A only
- 150 units of Product B only
- 86 units each when selling equal quantities`
            },
            {
                "category": "creative",
                "title": "Perspective Drawing Guide",
                "content": `An artist uses the line \\(2x - 3y + 18 = 0\\) as a perspective guide in a drawing (units in cm from bottom-left corner). Find where this guide line intersects the canvas edges at \\(x = 0\\) (left edge) and \\(x = 30\\) (right edge). What angle does this line make with the horizontal?`,
                "answer": `Left edge intersection (\\(x = 0\\)):
\\(2(0) - 3y + 18 = 0\\)
\\(-3y = -18\\)
\\(y = 6\\) cm
Point: \\((0, 6)\\)

Right edge intersection (\\(x = 30\\)):
\\(2(30) - 3y + 18 = 0\\)
\\(60 - 3y + 18 = 0\\)
\\(-3y = -78\\)
\\(y = 26\\) cm
Point: \\((30, 26)\\)

Slope: \\(m = \\frac{26 - 6}{30 - 0} = \\frac{20}{30} = \\frac{2}{3}\\)

Angle with horizontal:
\\(\\theta = \\arctan\\left(\\frac{2}{3}\\right) \\approx 33.7°\\)

The perspective guide runs from \\((0, 6)\\) to \\((30, 26)\\) at approximately 33.7° to the horizontal.`
            }
        ]
    };
    MathQuestionModule.render(content, 'standard-form-identity-container');
});
</script>

### Key Takeaways

```{important}
**Standard Form of a Line - Essential Concepts**

1. **General Equation**: $Ax + By + C = 0$
   - $A$ and $B$ not both zero
   - Conventionally, $A \geq 0$ (or $B > 0$ if $A = 0$)

2. **Key Formulas**:
   - Slope: $m = -\frac{A}{B}$ (when $B \neq 0$)
   - X-intercept: $\left(-\frac{C}{A}, 0\right)$ (when $A \neq 0$)
   - Y-intercept: $\left(0, -\frac{C}{B}\right)$ (when $B \neq 0$)

3. **Advantages**:
   - Handles vertical lines naturally
   - Symmetric in x and y
   - Integer coefficients possible
   - Useful for half-plane problems

4. **Applications**: Optimization, computer graphics, boundary analysis, linear programming

5. **Remember**: To convert from slope-intercept form, clear fractions and rearrange terms
```

