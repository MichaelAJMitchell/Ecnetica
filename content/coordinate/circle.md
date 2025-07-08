# Circle

<iframe 
    src="https://drive.google.com/file/d/1_circle_coordinate_geometry_LC/preview" 
    width="100%" 
    height="480" 
    frameborder="0" 
    allowfullscreen>
</iframe>

## Distance Formula Revision

### Theory
The equation of a circle relies on the distance formula:
- Distance from point $(x, y)$ to center $(h, k)$ is: $d = \sqrt{(x - h)^2 + (y - k)^2}$
- A circle is the set of all points at a fixed distance (radius) from a center
- This fundamental concept leads to the circle equation

### Application
All points at distance 5 from center $(2, 3)$ satisfy:
$\sqrt{(x - 2)^2 + (y - 3)^2} = 5$

## Equation of a Circle

### Theory

A circle can be represented in different forms:

#### Standard Form
A circle with center $(h, k)$ and radius $r$ has equation:
$$(x - h)^2 + (y - k)^2 = r^2$$

#### General Form
Expanding the standard form gives:
$$x^2 + y^2 + 2gx + 2fy + c = 0$$

where:
- Center: $(-g, -f)$
- Radius: $r = \sqrt{g^2 + f^2 - c}$ (exists only if $g^2 + f^2 - c > 0$)

#### Special Cases
1. **Circle centered at origin**: $x^2 + y^2 = r^2$
2. **Unit circle**: $x^2 + y^2 = 1$ (center at origin, radius 1)
3. **Point circle**: When $r = 0$ (degenerate case)

#### Interactive Visualization: Circle Equation Explorer

<div id="circle-equation-explorer" class="visualization-container" style="height: 500px;"></div>
<script>
document.addEventListener('DOMContentLoaded', function() {
    MathVisualizer.createGraphFromDescription('circle-equation-explorer', {
        boundingBox: [-10, 10, 10, -10],
        elements: [
            {type: 'point', coords: function(params) {
                return [params.h, params.k];
            }, name: 'C', color: 'red', label: 'Center'},
            {type: 'circle', center: function(params) {
                return [params.h, params.k];
            }, radius: function(params) {
                return params.r;
            }, style: {strokeColor: 'blue', strokeWidth: 2}},
            {type: 'point', coords: function(params) {
                return [params.h + params.r, params.k];
            }, name: 'R', color: 'green', label: 'Radius'},
            {type: 'line', points: ['C', 'R'], style: {strokeColor: 'green', strokeWidth: 1, dash: 2}}
        ],
        parameters: {
            h: {min: -5, max: 5, value: 0, step: 0.5, label: "Center x-coordinate (h)"},
            k: {min: -5, max: 5, value: 0, step: 0.5, label: "Center y-coordinate (k)"},
            r: {min: 0.5, max: 6, value: 3, step: 0.5, label: "Radius (r)"}
        },
        infoBox: {
            title: "Circle Equation",
            lines: [
                {text: "(x - h)² + (y - k)² = r²", dynamic: false},
                {text: "(x - ${h})² + (y - ${k})² = ${r}²", dynamic: true}
            ]
        }
    });
});
</script>

### Application

#### Examples

**Example 1: Finding Center and Radius**
Find the center and radius of the circle $x^2 + y^2 - 6x + 8y - 11 = 0$.

**Solution:**
Rearrange and complete the square:
$(x^2 - 6x) + (y^2 + 8y) = 11$
$(x^2 - 6x + 9) + (y^2 + 8y + 16) = 11 + 9 + 16$
$(x - 3)^2 + (y + 4)^2 = 36$

Therefore:
- Center: $(3, -4)$
- Radius: $r = \sqrt{36} = 6$

**Example 2: Writing Circle Equation**
Write the equation of a circle with center $(2, -3)$ passing through point $(5, 1)$.

**Solution:**
First, find the radius using the distance formula:
$r = \sqrt{(5 - 2)^2 + (1 - (-3))^2} = \sqrt{9 + 16} = \sqrt{25} = 5$

The equation is:
$(x - 2)^2 + (y + 3)^2 = 25$

Expanding to general form:
$x^2 + y^2 - 4x + 6y - 12 = 0$

**Example 3: Circle Through Three Points**
Find the equation of the circle passing through $(1, 1)$, $(2, 4)$, and $(5, 3)$.

**Solution:**
Let the general equation be $x^2 + y^2 + 2gx + 2fy + c = 0$.

Substituting the three points:
- $(1, 1)$: $1 + 1 + 2g + 2f + c = 0$ → $2g + 2f + c = -2$
- $(2, 4)$: $4 + 16 + 4g + 8f + c = 0$ → $4g + 8f + c = -20$
- $(5, 3)$: $25 + 9 + 10g + 6f + c = 0$ → $10g + 6f + c = -34$

Solving this system:
$g = -3$, $f = -2$, $c = 12$

Therefore: $x^2 + y^2 - 6x - 4y + 12 = 0$

#### Multiple Choice Questions

<div id="circle-mcq" class="quiz-container"></div>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Circle Equations Quiz",
        questions: [
            {
                text: "Find the center of the circle \\(x^2 + y^2 + 4x - 6y + 9 = 0\\).",
                options: ["\\((-2, 3)\\)", "\\((2, -3)\\)", "\\((-4, 6)\\)", "\\((4, -6)\\)"],
                correctIndex: 0,
                explanation: "From the general form, center is \\((-g, -f)\\). Here \\(2g = 4\\), so \\(g = 2\\), and \\(2f = -6\\), so \\(f = -3\\). Center: \\((-2, 3)\\).",
                difficulty: "Basic"
            },
            {
                text: "What is the radius of the circle \\((x - 3)^2 + (y + 2)^2 = 49\\)?",
                options: ["\\(49\\)", "\\(7\\)", "\\(14\\)", "\\(\\sqrt{49}\\)"],
                correctIndex: 1,
                explanation: "From standard form, \\(r^2 = 49\\), so \\(r = 7\\).",
                difficulty: "Basic"
            },
            {
                text: "A circle has center \\((1, -2)\\) and passes through \\((4, 2)\\). Find its equation.",
                options: ["\\((x-1)^2 + (y+2)^2 = 25\\)", "\\((x-1)^2 + (y+2)^2 = 5\\)", "\\((x+1)^2 + (y-2)^2 = 25\\)", "\\((x-1)^2 + (y-2)^2 = 25\\)"],
                correctIndex: 0,
                explanation: "Radius = \\(\\sqrt{(4-1)^2 + (2-(-2))^2} = \\sqrt{9+16} = 5\\). Equation: \\((x-1)^2 + (y+2)^2 = 25\\).",
                difficulty: "Intermediate"
            },
            {
                text: "For what value of \\(k\\) does \\(x^2 + y^2 + 6x - 4y + k = 0\\) represent a circle of radius 5?",
                options: ["\\(k = -12\\)", "\\(k = 12\\)", "\\(k = -8\\)", "\\(k = 8\\)"],
                correctIndex: 0,
                explanation: "Using \\(r = \\sqrt{g^2 + f^2 - c}\\) with \\(g = 3\\), \\(f = -2\\), \\(r = 5\\): \\(25 = 9 + 4 - k\\), so \\(k = -12\\).",
                difficulty: "Advanced"
            }
        ]
    };
    MCQQuiz.create('circle-mcq', quizData);
});
</script>

#### Sector Specific Questions: Circle Applications

<div id="circle-identity-container"></div>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const content = {
        "title": "Circles in Coordinate Geometry: Real-World Applications",
        "intro_content": `<p>Circles appear everywhere in the real world, from satellite orbits to roundabouts. Understanding their equations helps solve problems in engineering, science, and design.</p>`,
        "questions": [
            {
                "category": "engineering",
                "title": "Radar Coverage Area",
                "content": `A radar station is located at coordinates \\((15, 20)\\) km from a reference point. The radar has an effective range of 50 km. Write the equation representing the boundary of the radar coverage area and determine if a target at \\((55, 65)\\) km is within range.`,
                "answer": `The radar coverage boundary is a circle with center \\((15, 20)\\) and radius 50 km.

Equation: \\((x - 15)^2 + (y - 20)^2 = 2500\\)

To check if \\((55, 65)\\) is within range, calculate the distance:
\\(d = \\sqrt{(55 - 15)^2 + (65 - 20)^2}\\)
\\(= \\sqrt{40^2 + 45^2}\\)
\\(= \\sqrt{1600 + 2025}\\)
\\(= \\sqrt{3625} \\approx 60.2\\) km

Since 60.2 km > 50 km, the target is NOT within radar range.`
            },
            {
                "category": "scientific",
                "title": "Particle Accelerator Design",
                "content": `In a circular particle accelerator, particles follow a path described by \\(x^2 + y^2 - 40x - 30y + 400 = 0\\) (units in meters). Find the center and radius of the accelerator ring. What is the circumference of the particle path?`,
                "answer": `Complete the square to find standard form:
\\((x^2 - 40x) + (y^2 - 30y) = -400\\)
\\((x^2 - 40x + 400) + (y^2 - 30y + 225) = -400 + 400 + 225\\)
\\((x - 20)^2 + (y - 15)^2 = 225\\)

Center: \\((20, 15)\\) meters
Radius: \\(r = \\sqrt{225} = 15\\) meters

Circumference of particle path:
\\(C = 2\\pi r = 2\\pi(15) = 30\\pi \\approx 94.25\\) meters`
            },
            {
                "category": "financial",
                "title": "Market Coverage Analysis",
                "content": `A delivery service operates from a warehouse at coordinates \\((8, 12)\\) on a city grid (units in km). They guarantee delivery within a 25 km radius. The delivery fee is €5 base plus €0.50 per km. Find the equation of their service boundary and calculate the delivery fee to a customer at \\((28, 24)\\).`,
                "answer": `Service boundary equation:
\\((x - 8)^2 + (y - 12)^2 = 625\\)

Distance to customer at \\((28, 24)\\):
\\(d = \\sqrt{(28 - 8)^2 + (24 - 12)^2}\\)
\\(= \\sqrt{20^2 + 12^2}\\)
\\(= \\sqrt{400 + 144}\\)
\\(= \\sqrt{544} \\approx 23.32\\) km

Since 23.32 km < 25 km, delivery is available.

Delivery fee = €5 + €0.50 × 23.32 = €5 + €11.66 = €16.66`
            },
            {
                "category": "creative",
                "title": "Stage Lighting Design",
                "content": `A circular spotlight on a theater stage creates a lit area described by \\((x - 4)^2 + (y - 3)^2 = 9\\) (units in meters from stage left corner). The light intensity decreases linearly from 100% at center to 0% at the edge. Find the light intensity at position \\((6, 5)\\) on the stage.`,
                "answer": `From the equation:
- Center: \\((4, 3)\\)
- Radius: \\(r = 3\\) meters

Distance from \\((6, 5)\\) to center:
\\(d = \\sqrt{(6 - 4)^2 + (5 - 3)^2} = \\sqrt{4 + 4} = \\sqrt{8} = 2\\sqrt{2} \\approx 2.83\\) meters

Since intensity decreases linearly from center (100%) to edge (0%):
Intensity = \\(100\\% \\times \\left(1 - \\frac{d}{r}\\right)\\)
\\(= 100\\% \\times \\left(1 - \\frac{2\\sqrt{2}}{3}\\right)\\)
\\(= 100\\% \\times \\left(1 - \\frac{2.83}{3}\\right)\\)
\\(= 100\\% \\times 0.057 = 5.7\\%\\)

The light intensity at position \\((6, 5)\\) is approximately 5.7%.`
            }
        ]
    };
    MathQuestionModule.render(content, 'circle-identity-container');
});
</script>

### Key Takeaways

```{important}
**Circle Equations - Essential Concepts**

1. **Standard Form**: $(x - h)^2 + (y - k)^2 = r^2$
   - Center: $(h, k)$
   - Radius: $r$

2. **General Form**: $x^2 + y^2 + 2gx + 2fy + c = 0$
   - Center: $(-g, -f)$
   - Radius: $r = \sqrt{g^2 + f^2 - c}$ (if $g^2 + f^2 - c > 0$)

3. **Key Techniques**:
   - Complete the square to convert between forms
   - Use distance formula to find radius
   - Three non-collinear points determine a unique circle

4. **Applications**: Radar coverage, particle physics, delivery zones, lighting design

5. **Remember**: A circle exists only when $g^2 + f^2 - c > 0$ in general form
```

