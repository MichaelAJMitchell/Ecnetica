# Angle Between Lines

<iframe 
    src="https://drive.google.com/file/d/1_angle_between_lines_LC/preview" 
    width="100%" 
    height="480" 
    frameborder="0" 
    allowfullscreen>
</iframe>

## Slope of a Line Revision

### Theory
Before finding angles between lines, let's review the concept of slope:
- Slope $m = \frac{y_2 - y_1}{x_2 - x_1}$ for a line through $(x_1, y_1)$ and $(x_2, y_2)$
- For line $ax + by + c = 0$, slope $m = -\frac{a}{b}$
- Parallel lines have equal slopes
- Perpendicular lines have slopes whose product is $-1$

### Application
For the line through $A(2, 3)$ and $B(5, 9)$:
- Slope $m = \frac{9 - 3}{5 - 2} = \frac{6}{3} = 2$

## Angle Between Two Lines

### Theory

The angle between two lines can be found using their slopes or direction vectors.

#### Using Slopes
For two lines with slopes $m_1$ and $m_2$, the acute angle $\theta$ between them is:
$$\tan \theta = \left|\frac{m_1 - m_2}{1 + m_1m_2}\right|$$

#### Special Cases
1. **Parallel Lines**: If $m_1 = m_2$, then $\theta = 0°$
2. **Perpendicular Lines**: If $m_1m_2 = -1$, then $\theta = 90°$
3. **Vertical Line**: Use direction vectors instead

#### Using Direction Vectors
For lines with direction vectors $\vec{v_1} = (a_1, b_1)$ and $\vec{v_2} = (a_2, b_2)$:
$$\cos \theta = \frac{|\vec{v_1} \cdot \vec{v_2}|}{|\vec{v_1}||\vec{v_2}|} = \frac{|a_1a_2 + b_1b_2|}{\sqrt{a_1^2 + b_1^2}\sqrt{a_2^2 + b_2^2}}$$

#### Interactive Visualization: Angle Between Lines Explorer

<div id="angle-lines-explorer" class="visualization-container" style="height: 500px;"></div>
<script>
document.addEventListener('DOMContentLoaded', function() {
    MathVisualizer.createGraphFromDescription('angle-lines-explorer', {
        boundingBox: [-8, 8, 8, -8],
        elements: [
            {type: 'point', coords: [0, 0], fixed: true, name: 'O', visible: false},
            {type: 'line', equation: function(params) {
                return 'y = ' + params.m1 + '*x + ' + params.b1;
            }, style: {strokeColor: 'blue', strokeWidth: 2}, name: 'L1'},
            {type: 'line', equation: function(params) {
                return 'y = ' + params.m2 + '*x + ' + params.b2;
            }, style: {strokeColor: 'red', strokeWidth: 2}, name: 'L2'},
            {type: 'angle', vertex: 'O', points: function(params) {
                // Calculate intersection point and angle display
                const m1 = params.m1, b1 = params.b1;
                const m2 = params.m2, b2 = params.b2;
                const xi = (b2 - b1) / (m1 - m2);
                const yi = m1 * xi + b1;
                return {center: [xi, yi], radius: 1.5, from: Math.atan(m1), to: Math.atan(m2)};
            }}
        ],
        parameters: {
            m1: {min: -3, max: 3, value: 1, step: 0.1, label: "Slope of Line 1"},
            b1: {min: -5, max: 5, value: 0, step: 0.5, label: "y-intercept of Line 1"},
            m2: {min: -3, max: 3, value: -0.5, step: 0.1, label: "Slope of Line 2"},
            b2: {min: -5, max: 5, value: 2, step: 0.5, label: "y-intercept of Line 2"}
        },
        infoBox: {
            title: "Angle Between Lines",
            lines: [
                {text: function(params) {
                    const angle = Math.abs(Math.atan((params.m1 - params.m2)/(1 + params.m1*params.m2)));
                    return "Angle θ = " + (angle * 180 / Math.PI).toFixed(1) + "°";
                }, dynamic: true},
                {text: "Formula: tan θ = |m₁ - m₂|/|1 + m₁m₂|", dynamic: false}
            ]
        }
    });
});
</script>

### Application

#### Examples

**Example 1: Angle Between Lines with Given Slopes**
Find the angle between lines with slopes $m_1 = 2$ and $m_2 = -\frac{1}{3}$.

**Solution:**
Using the formula:
$$\tan \theta = \left|\frac{2 - (-\frac{1}{3})}{1 + 2(-\frac{1}{3})}\right|$$
$$= \left|\frac{2 + \frac{1}{3}}{1 - \frac{2}{3}}\right|$$
$$= \left|\frac{\frac{7}{3}}{\frac{1}{3}}\right| = 7$$

Therefore, $\theta = \arctan(7) \approx 81.87°$

**Example 2: Angle Between Lines in General Form**
Find the angle between $2x + 3y - 5 = 0$ and $3x - 2y + 7 = 0$.

**Solution:**
First, find the slopes:
- Line 1: $m_1 = -\frac{2}{3}$
- Line 2: $m_2 = \frac{3}{2}$

Using the formula:
$$\tan \theta = \left|\frac{-\frac{2}{3} - \frac{3}{2}}{1 + (-\frac{2}{3})(\frac{3}{2})}\right|$$
$$= \left|\frac{-\frac{4}{6} - \frac{9}{6}}{1 - 1}\right|$$

Since the denominator is 0, the lines are perpendicular, so $\theta = 90°$.

**Example 3: Using Direction Vectors**
Find the angle between lines with direction vectors $\vec{v_1} = (3, 4)$ and $\vec{v_2} = (5, -12)$.

**Solution:**
$$\cos \theta = \frac{|3(5) + 4(-12)|}{\sqrt{3^2 + 4^2}\sqrt{5^2 + (-12)^2}}$$
$$= \frac{|15 - 48|}{\sqrt{9 + 16}\sqrt{25 + 144}}$$
$$= \frac{33}{5 \times 13} = \frac{33}{65}$$

Therefore, $\theta = \arccos\left(\frac{33}{65}\right) \approx 59.49°$

#### Multiple Choice Questions

<div id="angle-lines-mcq" class="quiz-container"></div>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Angle Between Lines Quiz",
        questions: [
            {
                text: "Find the angle between lines with slopes \\(m_1 = 1\\) and \\(m_2 = -1\\).",
                options: ["\\(45°\\)", "\\(90°\\)", "\\(60°\\)", "\\(30°\\)"],
                correctIndex: 1,
                explanation: "Since \\(m_1 \\times m_2 = 1 \\times (-1) = -1\\), the lines are perpendicular. Therefore, the angle is \\(90°\\).",
                difficulty: "Basic"
            },
            {
                text: "The angle between lines \\(y = 3x + 2\\) and \\(y = \\frac{1}{2}x - 1\\) is:",
                options: ["\\(\\arctan(\\frac{5}{7})\\)", "\\(\\arctan(\\frac{7}{5})\\)", "\\(\\arctan(\\frac{5}{2})\\)", "\\(\\arctan(\\frac{2}{5})\\)"],
                correctIndex: 0,
                explanation: "Using \\(\\tan \\theta = \\left|\\frac{3 - \\frac{1}{2}}{1 + 3 \\times \\frac{1}{2}}\\right| = \\left|\\frac{\\frac{5}{2}}{\\frac{5}{2}}\\right| = \\frac{5}{7}\\)",
                difficulty: "Intermediate"
            },
            {
                text: "Two lines make angles of \\(30°\\) and \\(75°\\) with the positive x-axis. Find the angle between them.",
                options: ["\\(45°\\)", "\\(105°\\)", "\\(35°\\)", "\\(55°\\)"],
                correctIndex: 0,
                explanation: "The angle between the lines is \\(|75° - 30°| = 45°\\).",
                difficulty: "Intermediate"
            },
            {
                text: "Find the angle between \\(x + \\sqrt{3}y = 1\\) and \\(\\sqrt{3}x - y = 5\\).",
                options: ["\\(30°\\)", "\\(45°\\)", "\\(60°\\)", "\\(90°\\)"],
                correctIndex: 2,
                explanation: "Slopes are \\(m_1 = -\\frac{1}{\\sqrt{3}}\\) and \\(m_2 = \\sqrt{3}\\). Using the formula: \\(\\tan \\theta = \\left|\\frac{-\\frac{1}{\\sqrt{3}} - \\sqrt{3}}{1 + (-\\frac{1}{\\sqrt{3}})(\\sqrt{3})}\\right| = \\sqrt{3}\\), so \\(\\theta = 60°\\).",
                difficulty: "Advanced"
            }
        ]
    };
    MCQQuiz.create('angle-lines-mcq', quizData);
});
</script>

#### Sector Specific Questions: Angle Between Lines Applications

<div id="angle-lines-identity-container"></div>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const content = {
        "title": "Angles Between Lines: Real-World Applications",
        "intro_content": `<p>Understanding angles between lines is crucial in various fields, from engineering design to navigation systems. This concept helps in analyzing intersections, optimizing structures, and solving spatial problems.</p>`,
        "questions": [
            {
                "category": "engineering",
                "title": "Road Intersection Design",
                "content": `Two roads meet at an intersection. Road A follows the line \\(3x - 4y + 12 = 0\\) and Road B follows \\(5x + 12y - 60 = 0\\). For safety regulations, the angle between roads must be at least \\(60°\\). Does this intersection meet the safety requirement?`,
                "answer": `First, find the slopes of both roads:
Road A: \\(3x - 4y + 12 = 0\\) → \\(m_1 = \\frac{3}{4}\\)
Road B: \\(5x + 12y - 60 = 0\\) → \\(m_2 = -\\frac{5}{12}\\)

Using the angle formula:
\\(\\tan \\theta = \\left|\\frac{m_1 - m_2}{1 + m_1m_2}\\right| = \\left|\\frac{\\frac{3}{4} - (-\\frac{5}{12})}{1 + \\frac{3}{4} \\times (-\\frac{5}{12})}\\right|\\)

\\(= \\left|\\frac{\\frac{9}{12} + \\frac{5}{12}}{1 - \\frac{15}{48}}\\right| = \\left|\\frac{\\frac{14}{12}}{\\frac{33}{48}}\\right| = \\frac{14}{12} \\times \\frac{48}{33} = \\frac{56}{33}\\)

\\(\\theta = \\arctan\\left(\\frac{56}{33}\\right) \\approx 59.4°\\)

The intersection angle is approximately \\(59.4°\\), which is just below the \\(60°\\) requirement. The intersection does NOT meet the safety requirement.`
            },
            {
                "category": "scientific",
                "title": "Crystal Structure Analysis",
                "content": `In a crystal lattice, two atomic bonds are represented by vectors \\(\\vec{v_1} = (3, 4, 0)\\) and \\(\\vec{v_2} = (4, -3, 0)\\) in the xy-plane. Find the bond angle between these atomic connections.`,
                "answer": `Using the dot product formula for angle between vectors:
\\(\\cos \\theta = \\frac{\\vec{v_1} \\cdot \\vec{v_2}}{|\\vec{v_1}||\\vec{v_2}|}\\)

Calculate the dot product:
\\(\\vec{v_1} \\cdot \\vec{v_2} = 3(4) + 4(-3) + 0(0) = 12 - 12 = 0\\)

Since the dot product is 0, the vectors are perpendicular.
Therefore, the bond angle is \\(\\theta = 90°\\).

This perpendicular arrangement is common in crystal structures and contributes to their stability.`
            },
            {
                "category": "financial",
                "title": "Market Trend Analysis",
                "content": `A financial analyst models two market trends: Stock A's price follows \\(P_A = 2t + 50\\) and Stock B's price follows \\(P_B = -0.5t + 80\\), where \\(t\\) is time in days and \\(P\\) is price in euros. Find the angle between these trend lines to assess their divergence.`,
                "answer": `The trend lines have slopes:
- Stock A: \\(m_1 = 2\\) (rising trend)
- Stock B: \\(m_2 = -0.5\\) (falling trend)

Calculate the angle between trends:
\\(\\tan \\theta = \\left|\\frac{m_1 - m_2}{1 + m_1m_2}\\right| = \\left|\\frac{2 - (-0.5)}{1 + 2(-0.5)}\\right|\\)

\\(= \\left|\\frac{2.5}{1 - 1}\\right| = \\left|\\frac{2.5}{0}\\right|\\)

Since the denominator is 0, we check: \\(m_1 \\times m_2 = 2 \\times (-0.5) = -1\\)

The trends are perpendicular (\\(\\theta = 90°\\)), indicating maximum divergence. This suggests the stocks are moving in completely opposite directions, which could be useful for portfolio diversification.`
            },
            {
                "category": "creative",
                "title": "Architectural Roof Design",
                "content": `An architect designs a modern building with two sloped roof sections. Section A has slope \\(\\frac{3}{4}\\) and Section B has slope \\(-\\frac{1}{2}\\). Find the angle between these roof sections at their ridge line. If the angle exceeds \\(120°\\), special waterproofing is required.`,
                "answer": `Given slopes: \\(m_1 = \\frac{3}{4}\\) and \\(m_2 = -\\frac{1}{2}\\)

Calculate the angle:
\\(\\tan \\theta = \\left|\\frac{m_1 - m_2}{1 + m_1m_2}\\right| = \\left|\\frac{\\frac{3}{4} - (-\\frac{1}{2})}{1 + \\frac{3}{4} \\times (-\\frac{1}{2})}\\right|\\)

\\(= \\left|\\frac{\\frac{3}{4} + \\frac{2}{4}}{1 - \\frac{3}{8}}\\right| = \\left|\\frac{\\frac{5}{4}}{\\frac{5}{8}}\\right| = \\frac{5}{4} \\times \\frac{8}{5} = 2\\)

\\(\\theta = \\arctan(2) \\approx 63.43°\\)

The angle between roof sections is approximately \\(63.43°\\), which is less than \\(120°\\). Therefore, special waterproofing is not required.`
            }
        ]
    };
    MathQuestionModule.render(content, 'angle-lines-identity-container');
});
</script>

### Key Takeaways

```{important}
**Angle Between Lines - Essential Concepts**

1. **Slope Formula**: For lines with slopes $m_1$ and $m_2$:
   $$\tan \theta = \left|\frac{m_1 - m_2}{1 + m_1m_2}\right|$$

2. **Special Cases**:
   - Parallel lines: $m_1 = m_2$ → $\theta = 0°$
   - Perpendicular lines: $m_1m_2 = -1$ → $\theta = 90°$

3. **Vector Method**: For direction vectors $\vec{v_1}$ and $\vec{v_2}$:
   $$\cos \theta = \frac{|\vec{v_1} \cdot \vec{v_2}|}{|\vec{v_1}||\vec{v_2}|}$$

4. **Applications**: Used in road design, crystallography, financial analysis, and architecture

5. **Remember**: Always take the acute angle (0° to 90°) unless otherwise specified
```

