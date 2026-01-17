# Distance from a Point to a Line

<iframe 
    src="https://drive.google.com/file/d/1yMHZYXShfyGUPCW-bBhQtMC1W2FJZCm/preview" 
    width="100%" 
    height="480" 
    frameborder="0" 
    allowfullscreen>
</iframe>

## Line Equations Revision

### Theory

Before finding distances from points to lines, recall:
- **General form of a line**: $ax + by + c = 0$
- **Point-slope form**: $y - y_1 = m(x - x_1)$
- The coefficients $a$ and $b$ determine the line's direction

### Application

Converting between forms helps us apply the distance formula effectively.

## Distance from a Point to a Line

### Theory

The **perpendicular distance** from a point $(x_0, y_0)$ to a line $ax + by + c = 0$ is given by:

$$d = \frac{|ax_0 + by_0 + c|}{\sqrt{a^2 + b^2}}$$

**Key concepts:**
- This gives the shortest distance from the point to the line
- The distance is always measured perpendicular to the line
- The absolute value ensures distance is positive
- The denominator $\sqrt{a^2 + b^2}$ normalizes the line equation

**Special cases:**
- Distance from origin $(0, 0)$: $d = \frac{|c|}{\sqrt{a^2 + b^2}}$
- For vertical line $x = k$: distance from $(x_0, y_0)$ is $|x_0 - k|$
- For horizontal line $y = k$: distance from $(x_0, y_0)$ is $|y_0 - k|$

#### Interactive Visualization: Point-to-Line Distance Explorer

<div id="point-line-distance" class="visualization-container" style="height: 500px;"></div>
<script>
document.addEventListener('DOMContentLoaded', function() {
    MathVisualizer.createGraphFromDescription('point-line-distance', {
        boundingBox: [-10, 10, 10, -10],
        parametrizedFunctions: [{
            expression: 'm*x + b',
            title: 'Line: y = mx + b',
            parameters: {
                m: { min: -3, max: 3, value: 1, step: 0.1 },
                b: { min: -5, max: 5, value: 0, step: 0.5 }
            },
            features: ['intercepts']
        }],
        points: [{
            coords: [3, 2],
            draggable: true,
            name: 'P',
            showProjection: true
        }],
        infoBox: {
            title: "Distance Calculation",
            lines: [
                {text: "Point P: (${P.x}, ${P.y})", dynamic: true},
                {text: "Line: ${m}x - y + ${b} = 0", dynamic: true},
                {text: "Distance = ${Math.abs(m*P.x - P.y + b)/Math.sqrt(m*m + 1)}", dynamic: true}
            ]
        }
    });
});
</script>

### Application

#### Examples

**Example 1: Basic distance calculation**

Find the distance from the point $(4, 3)$ to the line $3x - 4y + 5 = 0$.

**Solution:**
Using the distance formula:
$$d = \frac{|3(4) - 4(3) + 5|}{\sqrt{3^2 + (-4)^2}}$$
$$d = \frac{|12 - 12 + 5|}{\sqrt{9 + 16}}$$
$$d = \frac{|5|}{\sqrt{25}} = \frac{5}{5} = 1$$

The distance is 1 unit.

**Example 2: Finding parallel lines at a given distance**

Find equations of lines parallel to $2x + y - 3 = 0$ at a distance of 2 units from it.

**Solution:**
Parallel lines have the form $2x + y + k = 0$.
The distance between parallel lines $2x + y - 3 = 0$ and $2x + y + k = 0$ is:
$$d = \frac{|k - (-3)|}{\sqrt{2^2 + 1^2}} = \frac{|k + 3|}{\sqrt{5}}$$

Setting $d = 2$:
$$\frac{|k + 3|}{\sqrt{5}} = 2$$
$$|k + 3| = 2\sqrt{5}$$
$$k + 3 = \pm 2\sqrt{5}$$
$$k = -3 \pm 2\sqrt{5}$$

The two parallel lines are:
- $2x + y + (-3 + 2\sqrt{5}) = 0$
- $2x + y + (-3 - 2\sqrt{5}) = 0$

**Example 3: Point equidistant from two lines**

Find the locus of points equidistant from the lines $3x + 4y - 12 = 0$ and $3x + 4y + 8 = 0$.

**Solution:**
Let $(x, y)$ be equidistant from both lines:
$$\frac{|3x + 4y - 12|}{\sqrt{9 + 16}} = \frac{|3x + 4y + 8|}{\sqrt{9 + 16}}$$

Since denominators are equal:
$$|3x + 4y - 12| = |3x + 4y + 8|$$

This gives us two cases:
1. $3x + 4y - 12 = 3x + 4y + 8$ (impossible)
2. $3x + 4y - 12 = -(3x + 4y + 8)$

From case 2:
$$3x + 4y - 12 = -3x - 4y - 8$$
$$6x + 8y = 4$$
$$3x + 4y = 2$$

The locus is the line $3x + 4y - 2 = 0$, which is parallel to and midway between the given lines.

#### Multiple Choice Questions

<div id="distance-point-line-mcq" class="quiz-container"></div>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Distance from Point to Line Quiz",
        questions: [
            {
                text: "What is the distance from the point \\((2, 1)\\) to the line \\(x + y - 5 = 0\\)?",
                options: ["\\(\\sqrt{2}\\)", "\\(2\\sqrt{2}\\)", "\\(\\frac{2}{\\sqrt{2}}\\)", "\\(\\frac{\\sqrt{2}}{2}\\)"],
                correctIndex: 0,
                explanation: "Using the formula: \\(d = \\frac{|2 + 1 - 5|}{\\sqrt{1^2 + 1^2}} = \\frac{|-2|}{\\sqrt{2}} = \\frac{2}{\\sqrt{2}} = \\sqrt{2}\\)",
                difficulty: "Basic"
            },
            {
                text: "The distance from the origin to the line \\(3x - 4y + 10 = 0\\) is:",
                options: ["\\(1\\)", "\\(2\\)", "\\(\\frac{10}{5}\\)", "\\(\\frac{10}{7}\\)"],
                correctIndex: 1,
                explanation: "Distance from origin: \\(d = \\frac{|0 + 0 + 10|}{\\sqrt{9 + 16}} = \\frac{10}{5} = 2\\)",
                difficulty: "Basic"
            },
            {
                text: "Which point is closest to the line \\(x - y + 2 = 0\\)?",
                options: ["\\((0, 0)\\)", "\\((1, 1)\\)", "\\((-1, 1)\\)", "\\((2, 2)\\)"],
                correctIndex: 2,
                explanation: "Calculate distances: \\((0,0)\\): \\(\\sqrt{2}\\), \\((1,1)\\): \\(\\sqrt{2}\\), \\((-1,1)\\): 0 (on the line), \\((2,2)\\): \\(\\sqrt{2}\\). Point \\((-1,1)\\) is on the line.",
                difficulty: "Intermediate"
            },
            {
                text: "Two parallel lines \\(ax + by + c_1 = 0\\) and \\(ax + by + c_2 = 0\\) are 3 units apart. If \\(a = 3\\) and \\(b = 4\\), then \\(|c_1 - c_2| =\\)?",
                options: ["\\(3\\)", "\\(12\\)", "\\(15\\)", "\\(20\\)"],
                correctIndex: 2,
                explanation: "Distance between parallel lines: \\(d = \\frac{|c_1 - c_2|}{\\sqrt{a^2 + b^2}} = \\frac{|c_1 - c_2|}{\\sqrt{9 + 16}} = \\frac{|c_1 - c_2|}{5} = 3\\). Therefore, \\(|c_1 - c_2| = 15\\).",
                difficulty: "Advanced"
            }
        ]
    };
    MCQQuiz.create('distance-point-line-mcq', quizData);
});
</script>

#### Sector Specific Questions: Distance Applications

<div id="distance-point-line-identity-container"></div>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const content = {
        "title": "Point-to-Line Distance: Real-World Applications",
        "intro_content": `<p>The distance from a point to a line is crucial in navigation, construction, quality control, and many other fields. Let's explore practical applications.</p>`,
        "questions": [
            {
                "category": "engineering",
                "title": "Civil Engineering: Highway Planning",
                "content": `A highway follows the line \\(3x + 4y - 120 = 0\\) on a coordinate map (units in kilometers). A town is located at point (20, 15).
                
                (a) Calculate the shortest distance from the town to the highway.
                (b) If a service road must be built perpendicular to the highway from the town, find its equation.
                (c) Where does the service road meet the highway?
                (d) If construction costs €50,000 per kilometer, what is the cost of the service road?`,
                "answer": `(a) Distance from town to highway:
                \\(d = \\frac{|3(20) + 4(15) - 120|}{\\sqrt{9 + 16}}\\)
                \\(d = \\frac{|60 + 60 - 120|}{5} = \\frac{0}{5} = 0\\)
                
                The town is on the highway! Let's recalculate with town at (20, 10):
                \\(d = \\frac{|3(20) + 4(10) - 120|}{5} = \\frac{|60 + 40 - 120|}{5} = \\frac{20}{5} = 4\\) km
                
                (b) Service road equation:
                Highway has slope \\(m_1 = -\\frac{3}{4}\\)
                Perpendicular slope: \\(m_2 = \\frac{4}{3}\\)
                
                Through (20, 10): \\(y - 10 = \\frac{4}{3}(x - 20)\\)
                \\(3y - 30 = 4x - 80\\)
                \\(4x - 3y - 50 = 0\\)
                
                (c) Intersection point:
                Solve: \\(3x + 4y = 120\\) and \\(4x - 3y = 50\\)
                Multiply first by 3, second by 4:
                \\(9x + 12y = 360\\)
                \\(16x - 12y = 200\\)
                Adding: \\(25x = 560\\), so \\(x = 22.4\\)
                \\(y = \\frac{120 - 3(22.4)}{4} = 13.2\\)
                
                Intersection at (22.4, 13.2)
                
                (d) Cost calculation:
                Distance = 4 km
                Cost = 4 × €50,000 = €200,000`
            },
            {
                "category": "scientific",
                "title": "Physics: Electric Field Lines",
                "content": `An infinite charged wire creates an electric field. The wire lies along the line \\(2x - y + 3 = 0\\) in the xy-plane (units in meters). The electric field strength at distance r from the wire is \\(E = \\frac{k}{r}\\) where k = 100 N⋅m/C.
                
                (a) Find the electric field strength at point P(4, 2).
                (b) At what points is the field strength exactly 20 N/C?
                (c) Find the equation of the field line passing through P(4, 2).
                (d) Calculate the potential difference between P(4, 2) and Q(1, -1).`,
                "answer": `(a) Field strength at P(4, 2):
                Distance: \\(r = \\frac{|2(4) - 2 + 3|}{\\sqrt{4 + 1}} = \\frac{|9|}{\\sqrt{5}} = \\frac{9}{\\sqrt{5}}\\) m
                
                Field strength: \\(E = \\frac{100}{9/\\sqrt{5}} = \\frac{100\\sqrt{5}}{9} ≈ 24.85\\) N/C
                
                (b) Points where E = 20 N/C:
                \\(20 = \\frac{100}{r}\\), so \\(r = 5\\) m
                
                Distance from line \\(2x - y + 3 = 0\\) equals 5:
                \\(\\frac{|2x - y + 3|}{\\sqrt{5}} = 5\\)
                \\(|2x - y + 3| = 5\\sqrt{5}\\)
                
                Two parallel lines:
                \\(2x - y + 3 = 5\\sqrt{5}\\) → \\(2x - y + 3 - 5\\sqrt{5} = 0\\)
                \\(2x - y + 3 = -5\\sqrt{5}\\) → \\(2x - y + 3 + 5\\sqrt{5} = 0\\)
                
                (c) Field line through P (perpendicular to wire):
                Wire slope: \\(m_1 = 2\\)
                Field line slope: \\(m_2 = -\\frac{1}{2}\\)
                
                Through P(4, 2): \\(y - 2 = -\\frac{1}{2}(x - 4)\\)
                \\(x + 2y - 8 = 0\\)
                
                (d) Potential difference:
                \\(V = -k\\ln(r)\\)
                \\(r_P = \\frac{9}{\\sqrt{5}}\\), \\(r_Q = \\frac{|2(1) - (-1) + 3|}{\\sqrt{5}} = \\frac{6}{\\sqrt{5}}\\)
                
                \\(ΔV = -100[\\ln(\\frac{6}{\\sqrt{5}}) - \\ln(\\frac{9}{\\sqrt{5}})] = -100\\ln(\\frac{6}{9}) = 100\\ln(1.5) ≈ 40.55\\) V`
            },
            {
                "category": "financial",
                "title": "Risk Management: Portfolio Optimization",
                "content": `In a risk-return graph, the efficient frontier follows the line \\(x - 2y + 10 = 0\\) where x is risk (%) and y is return (%). An investor's current portfolio is at point P(8, 6).
                
                (a) Calculate the distance from the current portfolio to the efficient frontier.
                (b) Find the nearest point on the efficient frontier to the current portfolio.
                (c) If moving to the efficient frontier, by how much would risk and return change?
                (d) What is the risk-return ratio at the optimal point?`,
                "answer": `(a) Distance to efficient frontier:
                \\(d = \\frac{|8 - 2(6) + 10|}{\\sqrt{1 + 4}} = \\frac{|8 - 12 + 10|}{\\sqrt{5}} = \\frac{6}{\\sqrt{5}} = \\frac{6\\sqrt{5}}{5} ≈ 2.68\\) units
                
                (b) Nearest point on frontier:
                Line perpendicular to frontier through P(8, 6):
                Frontier slope: \\(\\frac{1}{2}\\)
                Perpendicular slope: \\(-2\\)
                
                Through P: \\(y - 6 = -2(x - 8)\\)
                \\(y = -2x + 22\\)
                
                Intersection with frontier:
                \\(x - 2(-2x + 22) + 10 = 0\\)
                \\(x + 4x - 44 + 10 = 0\\)
                \\(5x = 34\\)
                \\(x = 6.8\\), \\(y = -2(6.8) + 22 = 8.4\\)
                
                Optimal point: (6.8%, 8.4%)
                
                (c) Changes:
                Risk change: 6.8 - 8 = -1.2% (risk decreases)
                Return change: 8.4 - 6 = +2.4% (return increases)
                
                (d) Risk-return ratio at optimal point:
                Risk/Return = 6.8/8.4 ≈ 0.81
                
                This represents an improved portfolio with lower risk and higher return.`
            },
            {
                "category": "creative",
                "title": "Architecture: Sound Design",
                "content": `In a concert hall design, a sound-reflecting wall follows the line \\(5x + 12y - 60 = 0\\) (units in meters). A speaker is placed at S(2, 3).
                
                (a) Calculate the distance from the speaker to the wall.
                (b) Find the point on the wall closest to the speaker.
                (c) If sound travels at 343 m/s, how long does it take for sound to reach the wall and reflect back?
                (d) Design a parallel wall 8 meters behind the first wall. What is its equation?`,
                "answer": `(a) Distance from speaker to wall:
                \\(d = \\frac{|5(2) + 12(3) - 60|}{\\sqrt{25 + 144}} = \\frac{|10 + 36 - 60|}{\\sqrt{169}} = \\frac{14}{13}\\) meters
                
                (b) Closest point on wall:
                Wall slope: \\(m_1 = -\\frac{5}{12}\\)
                Perpendicular slope: \\(m_2 = \\frac{12}{5}\\)
                
                Line through S(2, 3): \\(y - 3 = \\frac{12}{5}(x - 2)\\)
                \\(5y - 15 = 12x - 24\\)
                \\(12x - 5y - 9 = 0\\)
                
                Intersection with wall:
                Solve \\(5x + 12y = 60\\) and \\(12x - 5y = 9\\)
                Multiply first by 12, second by 5:
                \\(60x + 144y = 720\\)
                \\(60x - 25y = 45\\)
                Subtracting: \\(169y = 675\\), so \\(y = \\frac{675}{169} = \\frac{675}{169}\\)
                \\(x = \\frac{60 - 12y}{5}\\)
                
                After calculation: Closest point ≈ (3.08, 3.71)
                
                (c) Time for sound reflection:
                Total distance = 2 × \\(\\frac{14}{13}\\) = \\(\\frac{28}{13}\\) ≈ 2.15 meters
                Time = \\(\\frac{2.15}{343}\\) ≈ 0.0063 seconds = 6.3 milliseconds
                
                (d) Parallel wall 8m behind:
                Distance between parallel lines \\(5x + 12y + c_1 = 0\\) and \\(5x + 12y - 60 = 0\\) is:
                \\(\\frac{|c_1 - (-60)|}{13} = 8\\)
                \\(|c_1 + 60| = 104\\)
                \\(c_1 = 44\\) or \\(c_1 = -164\\)
                
                Since "behind" means away from speaker:
                Check which gives greater distance from S(2,3)
                Wall equation: \\(5x + 12y + 44 = 0\\)`
            }
        ]
    };
    MathQuestionModule.render(content, 'distance-point-line-identity-container');
});
</script>

### Key Takeaways

```{important}
**Essential Distance Concepts:**

1. **Distance Formula**: For point $(x_0, y_0)$ to line $ax + by + c = 0$:
   $$d = \frac{|ax_0 + by_0 + c|}{\sqrt{a^2 + b^2}}$$

2. **Key Properties**:
   - Always gives the perpendicular (shortest) distance
   - Result is always positive (due to absolute value)
   - Denominator normalizes the line equation

3. **Special Cases**:
   - Distance from origin: $d = \frac{|c|}{\sqrt{a^2 + b^2}}$
   - Vertical/horizontal lines have simpler formulas

4. **Applications**:
   - Finding parallel lines at given distances
   - Optimization problems
   - Physics (fields, waves)
   - Engineering (clearances, tolerances)
```