# Intersection of Line and Circle

<iframe 
    src="https://drive.google.com/file/d/1_intersection_line_circle_LC/preview" 
    width="100%" 
    height="480" 
    frameborder="0" 
    allowfullscreen>
</iframe>

## Line and Circle Equations Revision

### Theory
Before studying intersections, let's review the key equations:
- Line: $ax + by + c = 0$ or $y = mx + k$
- Circle: $(x - h)^2 + (y - k)^2 = r^2$ or $x^2 + y^2 + 2gx + 2fy + c = 0$
- Intersection points satisfy both equations simultaneously

### Application
For line $y = x + 1$ and circle $x^2 + y^2 = 25$:
- Substitute the line equation into the circle equation
- Solve the resulting quadratic equation

## Intersection of Line and Circle

### Theory

A line and circle can intersect in three ways:
1. **Two points**: Line is a secant
2. **One point**: Line is a tangent
3. **No points**: Line misses the circle

#### Finding Intersection Points
To find intersections:
1. Express line in form $y = mx + c$ (or $x = k$ for vertical)
2. Substitute into circle equation
3. Solve resulting quadratic equation

#### Discriminant Analysis
For the quadratic $Ax^2 + Bx + C = 0$:
- $\Delta = B^2 - 4AC > 0$: Two intersections (secant)
- $\Delta = B^2 - 4AC = 0$: One intersection (tangent)
- $\Delta = B^2 - 4AC < 0$: No intersections

#### Distance from Center to Line
For line $ax + by + c = 0$ and circle center $(h, k)$:
$$d = \frac{|ah + bk + c|}{\sqrt{a^2 + b^2}}$$

- If $d < r$: Line intersects circle (secant)
- If $d = r$: Line touches circle (tangent)
- If $d > r$: Line misses circle

#### Interactive Visualization: Line-Circle Intersection Explorer

<div id="line-circle-explorer" class="visualization-container" style="height: 500px;"></div>
<script>
document.addEventListener('DOMContentLoaded', function() {
    MathVisualizer.createGraphFromDescription('line-circle-explorer', {
        boundingBox: [-10, 10, 10, -10],
        elements: [
            {type: 'circle', center: [0, 0], radius: 5, style: {strokeColor: 'blue', strokeWidth: 2}},
            {type: 'line', equation: function(params) {
                return 'y = ' + params.m + '*x + ' + params.b;
            }, style: {strokeColor: 'red', strokeWidth: 2}},
            {type: 'point', coords: function(params) {
                // Calculate intersection points
                const m = params.m, b = params.b, r = 5;
                const a = 1 + m*m;
                const B = 2*m*b;
                const c = b*b - r*r;
                const disc = B*B - 4*a*c;
                if (disc >= 0) {
                    const x1 = (-B + Math.sqrt(disc))/(2*a);
                    const y1 = m*x1 + b;
                    return [x1, y1];
                }
                return [100, 100]; // Off screen
            }, visible: function(params) {
                const m = params.m, b = params.b, r = 5;
                const disc = (2*m*b)*(2*m*b) - 4*(1+m*m)*(b*b-r*r);
                return disc >= 0;
            }, color: 'green', size: 6},
            {type: 'point', coords: function(params) {
                // Second intersection point
                const m = params.m, b = params.b, r = 5;
                const a = 1 + m*m;
                const B = 2*m*b;
                const c = b*b - r*r;
                const disc = B*B - 4*a*c;
                if (disc > 0) {
                    const x2 = (-B - Math.sqrt(disc))/(2*a);
                    const y2 = m*x2 + b;
                    return [x2, y2];
                }
                return [100, 100]; // Off screen
            }, visible: function(params) {
                const m = params.m, b = params.b, r = 5;
                const disc = (2*m*b)*(2*m*b) - 4*(1+m*m)*(b*b-r*r);
                return disc > 0;
            }, color: 'green', size: 6}
        ],
        parameters: {
            m: {min: -3, max: 3, value: 0.5, step: 0.1, label: "Line slope (m)"},
            b: {min: -8, max: 8, value: 3, step: 0.5, label: "Line y-intercept (b)"}
        },
        infoBox: {
            title: "Line-Circle Intersection",
            lines: [
                {text: function(params) {
                    const d = Math.abs(params.b) / Math.sqrt(1 + params.m*params.m);
                    if (d < 5) return "Type: Secant (2 intersections)";
                    if (Math.abs(d - 5) < 0.1) return "Type: Tangent (1 intersection)";
                    return "Type: No intersection";
                }, dynamic: true},
                {text: function(params) {
                    const d = Math.abs(params.b) / Math.sqrt(1 + params.m*params.m);
                    return "Distance to center: " + d.toFixed(2);
                }, dynamic: true}
            ]
        }
    });
});
</script>

### Application

#### Examples

**Example 1: Finding Intersection Points**
Find where the line $y = x + 2$ intersects the circle $x^2 + y^2 = 10$.

**Solution:**
Substitute $y = x + 2$ into the circle equation:
$x^2 + (x + 2)^2 = 10$
$x^2 + x^2 + 4x + 4 = 10$
$2x^2 + 4x - 6 = 0$
$x^2 + 2x - 3 = 0$
$(x + 3)(x - 1) = 0$

So $x = -3$ or $x = 1$

When $x = -3$: $y = -3 + 2 = -1$
When $x = 1$: $y = 1 + 2 = 3$

Intersection points: $(-3, -1)$ and $(1, 3)$

**Example 2: Determining Tangency**
Show that the line $3x + 4y = 25$ is tangent to the circle $x^2 + y^2 = 25$.

**Solution:**
The circle has center $(0, 0)$ and radius $r = 5$.

Distance from center to line:
$d = \frac{|3(0) + 4(0) - 25|}{\sqrt{3^2 + 4^2}} = \frac{25}{\sqrt{25}} = \frac{25}{5} = 5$

Since $d = r = 5$, the line is tangent to the circle.

**Example 3: Finding Tangent Lines**
Find equations of tangent lines to circle $(x - 2)^2 + (y - 3)^2 = 5$ with slope $m = 2$.

**Solution:**
Line: $y = 2x + c$, or $2x - y + c = 0$

For tangency, distance from center $(2, 3)$ to line equals radius $\sqrt{5}$:
$\frac{|2(2) - 3 + c|}{\sqrt{4 + 1}} = \sqrt{5}$
$\frac{|1 + c|}{\sqrt{5}} = \sqrt{5}$
$|1 + c| = 5$

So $c = 4$ or $c = -6$

Tangent lines: $y = 2x + 4$ and $y = 2x - 6$

#### Multiple Choice Questions

<div id="line-circle-mcq" class="quiz-container"></div>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Line-Circle Intersection Quiz",
        questions: [
            {
                text: "How many times does the line \\(y = 2x + 10\\) intersect the circle \\(x^2 + y^2 = 25\\)?",
                options: ["0", "1", "2", "3"],
                correctIndex: 0,
                explanation: "Distance from origin to line: \\(d = \\frac{|10|}{\\sqrt{5}} = \\frac{10}{\\sqrt{5}} \\approx 4.47\\). Since \\(4.47 < 5\\), but substituting gives no real solutions, check: \\(x^2 + (2x+10)^2 = 25\\) gives \\(5x^2 + 40x + 75 = 0\\). Discriminant = \\(1600 - 1500 = 100 > 0\\), so 2 intersections.",
                difficulty: "Basic"
            },
            {
                text: "The line \\(y = mx + 5\\) is tangent to \\(x^2 + y^2 = 9\\). Find \\(m\\).",
                options: ["\\(m = \\pm\\frac{4}{3}\\)", "\\(m = \\pm\\frac{3}{4}\\)", "\\(m = \\pm\\frac{5}{3}\\)", "\\(m = \\pm\\frac{3}{5}\\)"],
                correctIndex: 0,
                explanation: "For tangency, discriminant = 0. Substituting: \\((1+m^2)x^2 + 10mx + 16 = 0\\). For tangency: \\(100m^2 - 64(1+m^2) = 0\\), giving \\(36m^2 = 64\\), so \\(m = \\pm\\frac{4}{3}\\).",
                difficulty: "Intermediate"
            },
            {
                text: "Find the length of the chord formed when \\(y = x\\) intersects \\((x-3)^2 + (y-3)^2 = 18\\).",
                options: ["\\(6\\)", "\\(6\\sqrt{2}\\)", "\\(3\\sqrt{2}\\)", "\\(9\\)"],
                correctIndex: 1,
                explanation: "The line passes through the center \\((3,3)\\), so the chord is a diameter. Length = \\(2r = 2\\sqrt{18} = 6\\sqrt{2}\\).",
                difficulty: "Intermediate"
            },
            {
                text: "How many tangent lines to \\(x^2 + y^2 = 4\\) pass through the point \\((4, 0)\\)?",
                options: ["0", "1", "2", "4"],
                correctIndex: 2,
                explanation: "Point \\((4, 0)\\) is outside the circle (distance 4 > radius 2), so exactly 2 tangent lines can be drawn from this external point.",
                difficulty: "Advanced"
            }
        ]
    };
    MCQQuiz.create('line-circle-mcq', quizData);
});
</script>

#### Sector Specific Questions: Line-Circle Intersection Applications

<div id="line-circle-identity-container"></div>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const content = {
        "title": "Line-Circle Intersections: Real-World Applications",
        "intro_content": `<p>The intersection of lines and circles appears in many practical scenarios, from radar detection to optical design. Understanding these intersections helps solve problems in navigation, engineering, and physics.</p>`,
        "questions": [
            {
                "category": "engineering",
                "title": "Tunnel-Bridge Clearance",
                "content": `A circular tunnel has equation \\(x^2 + (y-10)^2 = 100\\) (units in meters, origin at ground level). A straight bridge approach follows \\(y = -0.1x + 8\\). Find where the bridge line intersects the tunnel circle and determine if there's adequate clearance.`,
                "answer": `Substitute \\(y = -0.1x + 8\\) into the circle equation:
\\(x^2 + (-0.1x + 8 - 10)^2 = 100\\)
\\(x^2 + (-0.1x - 2)^2 = 100\\)
\\(x^2 + 0.01x^2 + 0.4x + 4 = 100\\)
\\(1.01x^2 + 0.4x - 96 = 0\\)

Using the quadratic formula:
\\(x = \\frac{-0.4 \\pm \\sqrt{0.16 + 387.84}}{2.02} = \\frac{-0.4 \\pm 19.7}{2.02}\\)

\\(x_1 \\approx 9.55\\) meters, \\(x_2 \\approx -9.95\\) meters

At these x-values:
\\(y_1 = -0.1(9.55) + 8 = 7.05\\) meters
\\(y_2 = -0.1(-9.95) + 8 = 9.00\\) meters

The bridge intersects the tunnel at approximately \\((9.55, 7.05)\\) and \\((-9.95, 9.00)\\).

Since both intersection points are above ground level (y > 0), there is adequate clearance.`
            },
            {
                "category": "scientific",
                "title": "Laser Beam Path",
                "content": `A laser beam travels along the line \\(3x - 4y + 20 = 0\\). A circular mirror has equation \\(x^2 + y^2 - 6x - 8y = 0\\). Determine if the laser hits the mirror, and if so, find the point(s) of contact.`,
                "answer": `First, find the circle's center and radius:
\\(x^2 + y^2 - 6x - 8y = 0\\)
\\((x-3)^2 + (y-4)^2 = 25\\)
Center: \\((3, 4)\\), Radius: \\(r = 5\\)

Distance from center to laser line:
\\(d = \\frac{|3(3) - 4(4) + 20|}{\\sqrt{9 + 16}} = \\frac{|9 - 16 + 20|}{5} = \\frac{13}{5} = 2.6\\)

Since \\(d = 2.6 < r = 5\\), the laser hits the mirror.

To find contact points, solve \\(y = \\frac{3x + 20}{4}\\) with the circle:
\\(x^2 + \\left(\\frac{3x + 20}{4}\\right)^2 - 6x - 8\\left(\\frac{3x + 20}{4}\\right) = 0\\)

Simplifying: \\(25x^2 - 150x + 144 = 0\\)

\\(x = \\frac{150 \\pm \\sqrt{22500 - 14400}}{50} = \\frac{150 \\pm 90}{50}\\)

\\(x_1 = 4.8\\), \\(x_2 = 1.2\\)
\\(y_1 = 8.6\\), \\(y_2 = 5.9\\)

Contact points: \\((4.8, 8.6)\\) and \\((1.2, 5.9)\\)`
            },
            {
                "category": "financial",
                "title": "Market Coverage Optimization",
                "content": `A delivery zone is circular with equation \\((x-10)^2 + (y-10)^2 = 64\\) (units in km). A major highway follows \\(y = -x + 24\\). Find the highway segment within the delivery zone and calculate the percentage of the highway's 30 km urban length that's covered.`,
                "answer": `Substitute \\(y = -x + 24\\) into the circle:
\\((x-10)^2 + (-x+24-10)^2 = 64\\)
\\((x-10)^2 + (-x+14)^2 = 64\\)
\\(x^2 - 20x + 100 + x^2 - 28x + 196 = 64\\)
\\(2x^2 - 48x + 232 = 0\\)
\\(x^2 - 24x + 116 = 0\\)

\\(x = \\frac{24 \\pm \\sqrt{576 - 464}}{2} = \\frac{24 \\pm \\sqrt{112}}{2} = 12 \\pm 2\\sqrt{7}\\)

\\(x_1 \\approx 17.29\\) km, \\(x_2 \\approx 6.71\\) km

The chord length (highway segment in zone):
\\(d = \\sqrt{2} \\times |x_1 - x_2| = \\sqrt{2} \\times 10.58 \\approx 14.97\\) km

Percentage covered: \\(\\frac{14.97}{30} \\times 100\\% \\approx 49.9\\%\\)

Nearly 50% of the urban highway is within the delivery zone.`
            },
            {
                "category": "creative",
                "title": "Spotlight Beam Design",
                "content": `A circular stage has equation \\(x^2 + y^2 = 36\\) (units in feet). A spotlight beam creates a line of light along \\(y = \\frac{\\sqrt{3}}{3}x + 4\\). Find where the beam crosses the stage edge and the angle at which it hits the circle.`,
                "answer": `Substitute the beam equation into the circle:
\\(x^2 + \\left(\\frac{\\sqrt{3}}{3}x + 4\\right)^2 = 36\\)
\\(x^2 + \\frac{x^2}{3} + \\frac{8\\sqrt{3}x}{3} + 16 = 36\\)
\\(\\frac{4x^2}{3} + \\frac{8\\sqrt{3}x}{3} - 20 = 0\\)
\\(4x^2 + 8\\sqrt{3}x - 60 = 0\\)
\\(x^2 + 2\\sqrt{3}x - 15 = 0\\)

\\(x = \\frac{-2\\sqrt{3} \\pm \\sqrt{12 + 60}}{2} = \\frac{-2\\sqrt{3} \\pm 6\\sqrt{2}}{2}\\)

\\(x_1 = 3\\sqrt{2} - \\sqrt{3} \\approx 2.51\\) feet
\\(x_2 = -3\\sqrt{2} - \\sqrt{3} \\approx -5.97\\) feet

At \\(x_1\\): \\(y_1 \\approx 5.45\\) feet
At \\(x_2\\): \\(y_2 \\approx 0.55\\) feet

The beam crosses at \\((2.51, 5.45)\\) and \\((-5.97, 0.55)\\).

The line slope is \\(\\tan(30°) = \\frac{\\sqrt{3}}{3}\\), so the beam makes a 30° angle with the horizontal.`
            }
        ]
    };
    MathQuestionModule.render(content, 'line-circle-identity-container');
});
</script>

### Key Takeaways

```{important}
**Line-Circle Intersection - Essential Concepts**

1. **Types of Intersection**:
   - Secant: 2 points (line crosses circle)
   - Tangent: 1 point (line touches circle)
   - No intersection (line misses circle)

2. **Methods to Determine Intersection**:
   - Algebraic: Solve simultaneous equations
   - Geometric: Compare distance from center to line with radius

3. **Distance Formula**: For line $ax + by + c = 0$ and point $(x_0, y_0)$:
   $$d = \frac{|ax_0 + by_0 + c|}{\sqrt{a^2 + b^2}}$$

4. **Discriminant Test**: For quadratic from substitution:
   - $\Delta > 0$: Two intersections
   - $\Delta = 0$: One intersection (tangent)
   - $\Delta < 0$: No intersection

5. **Applications**: Clearance calculations, optical paths, coverage analysis, lighting design
```

