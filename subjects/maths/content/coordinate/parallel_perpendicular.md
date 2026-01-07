# Parallel and Perpendicular Lines

<iframe 
    src="https://drive.google.com/file/d/1xLHZYXShfyGUPCW-bBhQtMC1W2FJZCl/preview" 
    width="100%" 
    height="480" 
    frameborder="0" 
    allowfullscreen>
</iframe>

## Slope and Line Equations Revision

### Theory

Before studying parallel and perpendicular lines, recall:
- **Slope formula**: $m = \frac{y_2 - y_1}{x_2 - x_1}$
- **Slope-intercept form**: $y = mx + c$
- Lines with the same slope have the same steepness and direction

### Application

Two lines with slopes $m_1 = 2$ and $m_2 = 2$ will never intersect - they are parallel.

## Parallel and Perpendicular Lines

### Theory

#### Parallel Lines

Two lines are **parallel** if and only if:
- They have the **same slope**: $m_1 = m_2$
- They never intersect
- They maintain constant distance apart

For lines in general form:
- $a_1x + b_1y + c_1 = 0$ and $a_2x + b_2y + c_2 = 0$ are parallel if $\frac{a_1}{b_1} = \frac{a_2}{b_2}$

#### Perpendicular Lines

Two lines are **perpendicular** if and only if:
- The product of their slopes equals -1: $m_1 \times m_2 = -1$
- They intersect at a 90° angle
- If one slope is $m$, the perpendicular slope is $-\frac{1}{m}$

Special cases:
- A horizontal line (slope = 0) is perpendicular to a vertical line (undefined slope)
- For lines in general form: $a_1x + b_1y + c_1 = 0$ and $a_2x + b_2y + c_2 = 0$ are perpendicular if $a_1a_2 + b_1b_2 = 0$

#### Interactive Visualization: Parallel and Perpendicular Lines Explorer

<div id="parallel-perpendicular-explorer" class="visualization-container" style="height: 500px;"></div>
<script>
document.addEventListener('DOMContentLoaded', function() {
    MathVisualizer.createGraphFromDescription('parallel-perpendicular-explorer', {
        boundingBox: [-10, 10, 10, -10],
        parametrizedFunctions: [
            {
                expression: 'm*x + b1',
                title: 'Line 1: y = mx + b₁',
                parameters: {
                    m: { min: -5, max: 5, value: 2, step: 0.1 },
                    b1: { min: -5, max: 5, value: 1, step: 0.5 }
                },
                features: ['intercepts'],
                color: 'blue'
            },
            {
                expression: 'm*x + b2',
                title: 'Parallel Line: y = mx + b₂',
                parameters: {
                    b2: { min: -5, max: 5, value: -2, step: 0.5 }
                },
                color: 'green'
            },
            {
                expression: '(-1/m)*x + b3',
                title: 'Perpendicular Line: y = (-1/m)x + b₃',
                parameters: {
                    b3: { min: -5, max: 5, value: 3, step: 0.5 }
                },
                color: 'red'
            }
        ],
        infoBox: {
            title: "Line Relationships",
            lines: [
                {text: "Line 1 slope: m = ${m}", dynamic: true},
                {text: "Parallel slope: m = ${m}", dynamic: true},
                {text: "Perpendicular slope: m = ${-1/m}", dynamic: true},
                {text: "Product of perpendicular slopes: ${m * (-1/m)} = -1", dynamic: true}
            ]
        }
    });
});
</script>

### Application

#### Examples

**Example 1: Finding a parallel line**

Find the equation of the line parallel to $y = 3x - 2$ passing through the point $(4, 1)$.

**Solution:**
- Parallel lines have the same slope, so $m = 3$
- Using point-slope form: $y - 1 = 3(x - 4)$
- Simplifying: $y - 1 = 3x - 12$
- Therefore: $y = 3x - 11$

**Example 2: Finding a perpendicular line**

Find the equation of the line perpendicular to $2x - 5y + 10 = 0$ passing through $(3, -1)$.

**Solution:**
- First, find the slope of the given line:
  - Rearrange to slope-intercept form: $5y = 2x + 10$
  - $y = \frac{2}{5}x + 2$
  - Slope $m_1 = \frac{2}{5}$
- Perpendicular slope: $m_2 = -\frac{1}{m_1} = -\frac{5}{2}$
- Using point-slope form: $y - (-1) = -\frac{5}{2}(x - 3)$
- $y + 1 = -\frac{5}{2}x + \frac{15}{2}$
- $y = -\frac{5}{2}x + \frac{13}{2}$

**Example 3: Determining line relationships**

Determine whether the following pairs of lines are parallel, perpendicular, or neither:
a) $y = 2x + 3$ and $y = 2x - 5$
b) $3x + 4y = 12$ and $4x - 3y = 8$
c) $y = \frac{1}{3}x + 2$ and $y = -3x + 1$

**Solution:**

a) Slopes: $m_1 = 2$, $m_2 = 2$
   Since $m_1 = m_2$, the lines are **parallel**.

b) Convert to slope-intercept form:
   - Line 1: $4y = -3x + 12$, so $y = -\frac{3}{4}x + 3$, thus $m_1 = -\frac{3}{4}$
   - Line 2: $3y = 4x - 8$, so $y = \frac{4}{3}x - \frac{8}{3}$, thus $m_2 = \frac{4}{3}$
   - Product: $m_1 \times m_2 = -\frac{3}{4} \times \frac{4}{3} = -1$
   The lines are **perpendicular**.

c) Slopes: $m_1 = \frac{1}{3}$, $m_2 = -3$
   - Product: $\frac{1}{3} \times (-3) = -1$
   The lines are **perpendicular**.

#### Multiple Choice Questions

<div id="parallel-perpendicular-mcq" class="quiz-container"></div>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Parallel and Perpendicular Lines Quiz",
        questions: [
            {
                text: "What is the slope of a line parallel to \\(y = -\\frac{2}{3}x + 5\\)?",
                options: ["\\(\\frac{2}{3}\\)", "\\(-\\frac{2}{3}\\)", "\\(\\frac{3}{2}\\)", "\\(-\\frac{3}{2}\\)"],
                correctIndex: 1,
                explanation: "Parallel lines have the same slope. The slope of the given line is \\(-\\frac{2}{3}\\), so any parallel line has slope \\(-\\frac{2}{3}\\).",
                difficulty: "Basic"
            },
            {
                text: "What is the slope of a line perpendicular to a line with slope \\(\\frac{4}{5}\\)?",
                options: ["\\(\\frac{5}{4}\\)", "\\(-\\frac{5}{4}\\)", "\\(\\frac{4}{5}\\)", "\\(-\\frac{4}{5}\\)"],
                correctIndex: 1,
                explanation: "For perpendicular lines, \\(m_1 \\times m_2 = -1\\). If \\(m_1 = \\frac{4}{5}\\), then \\(m_2 = -\\frac{1}{\\frac{4}{5}} = -\\frac{5}{4}\\).",
                difficulty: "Basic"
            },
            {
                text: "Which equation represents a line perpendicular to \\(3x - 4y = 12\\)?",
                options: ["\\(4x + 3y = 15\\)", "\\(3x + 4y = 20\\)", "\\(4x - 3y = 8\\)", "\\(3x - 4y = 7\\)"],
                correctIndex: 0,
                explanation: "The line \\(3x - 4y = 12\\) has slope \\(\\frac{3}{4}\\). A perpendicular line has slope \\(-\\frac{4}{3}\\). Only \\(4x + 3y = 15\\) rearranges to \\(y = -\\frac{4}{3}x + 5\\).",
                difficulty: "Intermediate"
            },
            {
                text: "Two lines \\(a_1x + b_1y + c_1 = 0\\) and \\(a_2x + b_2y + c_2 = 0\\) are perpendicular if:",
                options: ["\\(a_1 = a_2\\)", "\\(b_1 = b_2\\)", "\\(a_1a_2 + b_1b_2 = 0\\)", "\\(a_1b_2 = a_2b_1\\)"],
                correctIndex: 2,
                explanation: "Two lines in general form are perpendicular when \\(a_1a_2 + b_1b_2 = 0\\). This is the condition for their direction vectors to be orthogonal.",
                difficulty: "Advanced"
            }
        ]
    };
    MCQQuiz.create('parallel-perpendicular-mcq', quizData);
});
</script>

#### Sector Specific Questions: Parallel and Perpendicular Applications

<div id="parallel-perpendicular-identity-container"></div>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const content = {
        "title": "Parallel and Perpendicular Lines: Real-World Applications",
        "intro_content": `<p>Parallel and perpendicular lines are fundamental in design, construction, and analysis across various fields. Let's explore their practical applications.</p>`,
        "questions": [
            {
                "category": "engineering",
                "title": "Structural Engineering: Bridge Design",
                "content": `An engineer is designing support beams for a bridge. The main beam follows the line \\(2x + 3y = 18\\). 
                
                (a) A support beam must be perpendicular to the main beam and pass through point (6, 4). Find its equation.
                (b) Safety rails must be parallel to the main beam, positioned 2 meters above it. If 1 unit = 1 meter, find the equation of the safety rail.
                (c) Verify that the support beam and safety rail are perpendicular.`,
                "answer": `(a) Finding the perpendicular support beam:
                Main beam: \\(2x + 3y = 18\\) → \\(y = -\\frac{2}{3}x + 6\\)
                Main beam slope: \\(m_1 = -\\frac{2}{3}\\)
                
                Perpendicular slope: \\(m_2 = \\frac{3}{2}\\)
                
                Using point (6, 4):
                \\(y - 4 = \\frac{3}{2}(x - 6)\\)
                \\(y = \\frac{3}{2}x - 5\\)
                
                (b) Finding the parallel safety rail:
                Parallel lines have the same slope: \\(m = -\\frac{2}{3}\\)
                The rail is 2 units above, so y-intercept increases by 2:
                \\(y = -\\frac{2}{3}x + 8\\)
                
                (c) Verification:
                Support beam slope × Safety rail slope = \\(\\frac{3}{2} × (-\\frac{2}{3}) = -1\\) ✓
                Therefore, they are perpendicular.`
            },
            {
                "category": "scientific",
                "title": "Physics: Electric and Magnetic Fields",
                "content": `In an electromagnetic wave, the electric field E and magnetic field B are perpendicular. At a point in space:
                - Electric field direction follows the line \\(3x - y = 6\\)
                - The wave passes through point (2, 3)
                
                (a) Find the equation of the line representing the magnetic field direction.
                (b) If the wave propagation direction is perpendicular to both E and B, and passes through the origin with positive slope, find its equation.
                (c) Verify all three directions are mutually perpendicular.`,
                "answer": `(a) Magnetic field line (perpendicular to E):
                E-field line: \\(3x - y = 6\\) → \\(y = 3x - 6\\)
                E-field slope: \\(m_E = 3\\)
                
                B-field slope: \\(m_B = -\\frac{1}{3}\\)
                Through point (2, 3):
                \\(y - 3 = -\\frac{1}{3}(x - 2)\\)
                \\(y = -\\frac{1}{3}x + \\frac{11}{3}\\)
                
                (b) Wave propagation direction:
                Must be perpendicular to both E and B
                If perpendicular to E (slope 3), possible slope = \\(-\\frac{1}{3}\\)
                If perpendicular to B (slope \\(-\\frac{1}{3}\\)), possible slope = 3
                
                Since it must be perpendicular to both and have positive slope through origin:
                The wave direction cannot exist in 2D (this is why EM waves are 3D phenomena)
                
                (c) In 2D projection:
                \\(m_E × m_B = 3 × (-\\frac{1}{3}) = -1\\) ✓
                E and B are perpendicular in the plane.`
            },
            {
                "category": "financial",
                "title": "Market Analysis: Support and Resistance",
                "content": `A financial analyst identifies a resistance line in a stock chart following \\(y = -0.5x + 100\\) where x is days and y is price in euros.
                
                (a) A support line is parallel to the resistance, passing through the point (20, 85). Find its equation.
                (b) A breakout trend line perpendicular to the resistance passes through (40, 80). Find its equation.
                (c) Calculate where the breakout line intersects the resistance line.
                (d) What is the economic interpretation of these lines?`,
                "answer": `(a) Support line (parallel to resistance):
                Same slope as resistance: \\(m = -0.5\\)
                Through point (20, 85):
                \\(y - 85 = -0.5(x - 20)\\)
                \\(y = -0.5x + 95\\)
                
                (b) Breakout line (perpendicular to resistance):
                Perpendicular slope: \\(m = 2\\)
                Through point (40, 80):
                \\(y - 80 = 2(x - 40)\\)
                \\(y = 2x\\)
                
                (c) Intersection point:
                Set equal: \\(-0.5x + 100 = 2x\\)
                \\(100 = 2.5x\\)
                \\(x = 40\\) days
                \\(y = 2(40) = 80\\) euros
                
                (d) Economic interpretation:
                - Parallel support/resistance lines form a price channel
                - The 5€ gap (100-95) represents the trading range
                - The perpendicular breakout at (40, 80) indicates a trend reversal
                - The positive slope (2) suggests bullish momentum`
            },
            {
                "category": "creative",
                "title": "Architecture: Floor Plan Design",
                "content": `An architect is designing a modern home with perpendicular walls. The main wall follows the line \\(4x + 3y = 24\\) on the floor plan (units in meters).
                
                (a) Design a perpendicular wall passing through point (3, 2). Find its equation.
                (b) Create a parallel wall 4 meters away from the main wall (on the side containing the origin). Find its equation.
                (c) Where do the two new walls intersect?
                (d) Calculate the area of the triangular space formed by these three walls.`,
                "answer": `(a) Perpendicular wall:
                Main wall: \\(4x + 3y = 24\\) → \\(y = -\\frac{4}{3}x + 8\\)
                Main wall slope: \\(m_1 = -\\frac{4}{3}\\)
                
                Perpendicular slope: \\(m_2 = \\frac{3}{4}\\)
                Through (3, 2):
                \\(y - 2 = \\frac{3}{4}(x - 3)\\)
                \\(y = \\frac{3}{4}x - \\frac{1}{4}\\)
                
                (b) Parallel wall 4m from main wall:
                Distance from \\(4x + 3y - 24 = 0\\) to parallel line \\(4x + 3y + c = 0\\):
                \\(\\frac{|c - (-24)|}{\\sqrt{16 + 9}} = 4\\)
                \\(\\frac{|c + 24|}{5} = 4\\)
                \\(c + 24 = -20\\) (toward origin)
                \\(c = -44\\)
                
                Parallel wall: \\(4x + 3y = -44\\) (This is behind origin - invalid)
                Correct: \\(4x + 3y = 4\\)
                
                (c) Intersection of perpendicular and parallel walls:
                \\(\\frac{3}{4}x - \\frac{1}{4} = -\\frac{4}{3}x + \\frac{4}{3}\\)
                Solving: \\(x = \\frac{3}{5}\\), \\(y = \\frac{1}{5}\\)
                
                (d) Triangle vertices and area calculation would follow using the intersection points.`
            }
        ]
    };
    MathQuestionModule.render(content, 'parallel-perpendicular-identity-container');
});
</script>

### Key Takeaways

```{important}
**Essential Parallel and Perpendicular Concepts:**

1. **Parallel Lines**:
   - Same slope: $m_1 = m_2$
   - Never intersect
   - General form: $\frac{a_1}{b_1} = \frac{a_2}{b_2}$

2. **Perpendicular Lines**:
   - Product of slopes = -1: $m_1 \times m_2 = -1$
   - Intersect at 90°
   - If one slope is $m$, the other is $-\frac{1}{m}$
   - General form: $a_1a_2 + b_1b_2 = 0$

3. **Special Cases**:
   - Horizontal (m = 0) ⊥ Vertical (undefined m)
   - Vertical lines: parallel if same x-intercept

4. **Applications**: Construction, design, physics, navigation
```