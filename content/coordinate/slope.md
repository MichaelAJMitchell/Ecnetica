# Slope

<iframe 
    src="https://drive.google.com/file/d/1vdGEXKXShfyGUPCW-bBhQtMC1W2FJZCj/preview" 
    width="100%" 
    height="480" 
    frameborder="0" 
    allowfullscreen>
</iframe>

## Slope of a Line

### Theory

The slope of a line is a measure of its steepness and direction. It represents the rate of change of the y-coordinate with respect to the x-coordinate.

Given two points $(x_1, y_1)$ and $(x_2, y_2)$ on a line, the slope $m$ is calculated as:

$$m = \frac{y_2 - y_1}{x_2 - x_1}$$

where $x_2 \neq x_1$.

**Key Properties:**
- **Positive slope**: Line rises from left to right
- **Negative slope**: Line falls from left to right
- **Zero slope**: Horizontal line
- **Undefined slope**: Vertical line (when $x_2 = x_1$)

The slope can also be interpreted as:
- **Rise over run**: The vertical change divided by the horizontal change
- **Gradient**: Another term commonly used for slope
- **Rate of change**: In real-world applications

#### Interactive Visualization: Slope Explorer

<div id="slope-explorer" class="visualization-container" style="height: 500px;"></div>
<script>
document.addEventListener('DOMContentLoaded', function() {
    MathVisualizer.createGraphFromDescription('slope-explorer', {
        boundingBox: [-10, 10, 10, -10],
        parametrizedFunctions: [{
            expression: 'm*x + b',
            title: 'Line: y = mx + b',
            parameters: {
                m: { min: -5, max: 5, value: 1, step: 0.1 },
                b: { min: -5, max: 5, value: 0, step: 0.5 }
            },
            features: ['intercepts']
        }],
        infoBox: {
            title: "Slope Properties",
            lines: [
                {text: "Slope (m) = ${m}", dynamic: true},
                {text: "Y-intercept (b) = ${b}", dynamic: true},
                {text: "Angle with x-axis = ${Math.atan(m) * 180 / Math.PI}°", dynamic: true}
            ]
        }
    });
});
</script>

### Application

#### Examples

**Example 1: Finding the slope between two points**

Find the slope of the line passing through the points $A(2, 3)$ and $B(6, 11)$.

**Solution:**
Using the slope formula:
$$m = \frac{y_2 - y_1}{x_2 - x_1} = \frac{11 - 3}{6 - 2} = \frac{8}{4} = 2$$

Therefore, the slope is 2, meaning the line rises 2 units for every 1 unit it moves to the right.

**Example 2: Determining the type of line**

Classify the following lines based on their slopes:
- Line through $(1, 5)$ and $(4, 5)$
- Line through $(3, 2)$ and $(3, 8)$
- Line through $(0, 4)$ and $(2, 0)$

**Solution:**
1. For $(1, 5)$ and $(4, 5)$: $m = \frac{5 - 5}{4 - 1} = \frac{0}{3} = 0$ → Horizontal line
2. For $(3, 2)$ and $(3, 8)$: $m = \frac{8 - 2}{3 - 3} = \frac{6}{0}$ → Undefined (Vertical line)
3. For $(0, 4)$ and $(2, 0)$: $m = \frac{0 - 4}{2 - 0} = \frac{-4}{2} = -2$ → Negative slope

**Example 3: Real-world application**

A road rises 15 meters over a horizontal distance of 200 meters. Find the slope and express it as a percentage gradient.

**Solution:**
- Slope = $\frac{\text{rise}}{\text{run}} = \frac{15}{200} = 0.075$
- Percentage gradient = $0.075 \times 100\% = 7.5\%$

This means the road has a 7.5% gradient.

#### Multiple Choice Questions

<div id="slope-mcq" class="quiz-container"></div>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Slope Concepts Quiz",
        questions: [
            {
                text: "What is the slope of the line passing through the points \\((2, 5)\\) and \\((6, 13)\\)?",
                options: ["\\(2\\)", "\\(3\\)", "\\(4\\)", "\\(\\frac{1}{2}\\)"],
                correctIndex: 0,
                explanation: "Using the slope formula: \\(m = \\frac{13 - 5}{6 - 2} = \\frac{8}{4} = 2\\)",
                difficulty: "Basic"
            },
            {
                text: "Which type of line has an undefined slope?",
                options: ["Horizontal line", "Vertical line", "Line with positive slope", "Line with negative slope"],
                correctIndex: 1,
                explanation: "A vertical line has an undefined slope because the denominator in the slope formula becomes zero (\\(x_2 - x_1 = 0\\)).",
                difficulty: "Basic"
            },
            {
                text: "If a line has slope \\(-\\frac{3}{4}\\), what is the slope of a line perpendicular to it?",
                options: ["\\(\\frac{3}{4}\\)", "\\(-\\frac{4}{3}\\)", "\\(\\frac{4}{3}\\)", "\\(-\\frac{3}{4}\\)"],
                correctIndex: 2,
                explanation: "For perpendicular lines, the product of their slopes is -1. If \\(m_1 = -\\frac{3}{4}\\), then \\(m_2 = \\frac{4}{3}\\) because \\((-\\frac{3}{4}) \\times \\frac{4}{3} = -1\\).",
                difficulty: "Intermediate"
            },
            {
                text: "A ladder leans against a wall such that its base is 4m from the wall and its top reaches 3m up the wall. What is the slope of the ladder?",
                options: ["\\(\\frac{3}{4}\\)", "\\(-\\frac{3}{4}\\)", "\\(\\frac{4}{3}\\)", "\\(-\\frac{4}{3}\\)"],
                correctIndex: 1,
                explanation: "If we place the base of the wall at the origin, the base of the ladder is at (4, 0) and the top is at (0, 3). The slope is \\(\\frac{3 - 0}{0 - 4} = -\\frac{3}{4}\\).",
                difficulty: "Intermediate"
            }
        ]
    };
    MCQQuiz.create('slope-mcq', quizData);
});
</script>

#### Sector Specific Questions: Slope Applications

<div id="slope-identity-container"></div>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const content = {
        "title": "Slope: Real-World Applications",
        "intro_content": `<p>The concept of slope appears in numerous real-world contexts across different fields. Let's explore how professionals use slope in their work.</p>`,
        "questions": [
            {
                "category": "engineering",
                "title": "Civil Engineering: Road Design",
                "content": `A civil engineer is designing a highway ramp that must rise 8 meters over a horizontal distance of 160 meters to meet safety standards. The maximum allowable gradient for the ramp is 6%. 
                
                Does the proposed design meet the safety requirements? If not, what is the minimum horizontal distance needed?`,
                "answer": `Let's calculate the slope of the proposed design:
                
                Slope = \\(\\frac{\\text{rise}}{\\text{run}} = \\frac{8}{160} = 0.05 = 5\\%\\)
                
                Since 5% < 6%, the design meets safety requirements.
                
                For the minimum horizontal distance at 6% gradient:
                \\(0.06 = \\frac{8}{d}\\)
                \\(d = \\frac{8}{0.06} = 133.33\\) meters
                
                Therefore, the minimum horizontal distance needed is 133.33 meters.`
            },
            {
                "category": "scientific",
                "title": "Physics: Inclined Plane",
                "content": `A physicist is studying an object sliding down an inclined plane. The plane is 5 meters long and rises 2 meters above the horizontal. 
                
                (a) Calculate the slope of the incline.
                (b) Find the angle of inclination.
                (c) If friction is negligible, what is the acceleration of the object down the plane? (Use g = 9.8 m/s²)`,
                "answer": `(a) To find the slope, we need the horizontal distance:
                Using Pythagoras: horizontal = \\(\\sqrt{5^2 - 2^2} = \\sqrt{21} ≈ 4.58\\) m
                
                Slope = \\(\\frac{2}{4.58} ≈ 0.437\\)
                
                (b) Angle of inclination:
                \\(\\sin θ = \\frac{2}{5} = 0.4\\)
                \\(θ = \\sin^{-1}(0.4) ≈ 23.6°\\)
                
                (c) Acceleration down the plane:
                \\(a = g \\sin θ = 9.8 × 0.4 = 3.92\\) m/s²`
            },
            {
                "category": "financial",
                "title": "Economics: Supply and Demand",
                "content": `An economist is analyzing the demand curve for a product. When the price is €20, the quantity demanded is 1000 units. When the price increases to €30, the quantity demanded drops to 600 units.
                
                (a) Calculate the slope of the demand curve.
                (b) Interpret what this slope means in economic terms.
                (c) If the trend continues linearly, at what price will the demand reach zero?`,
                "answer": `(a) Slope of demand curve:
                \\(m = \\frac{\\Delta Q}{\\Delta P} = \\frac{600 - 1000}{30 - 20} = \\frac{-400}{10} = -40\\)
                
                (b) Economic interpretation:
                The slope of -40 means that for every €1 increase in price, the quantity demanded decreases by 40 units. This represents the price elasticity of demand in linear form.
                
                (c) To find when demand reaches zero:
                Using point-slope form: \\(Q - 1000 = -40(P - 20)\\)
                When Q = 0: \\(0 - 1000 = -40(P - 20)\\)
                \\(-1000 = -40P + 800\\)
                \\(40P = 1800\\)
                \\(P = €45\\)
                
                The demand will reach zero at a price of €45.`
            },
            {
                "category": "creative",
                "title": "Architecture: Roof Design",
                "content": `An architect is designing a modern house with a slanted roof. The roof must span a horizontal distance of 12 meters and rise 3 meters to ensure proper water drainage. Building codes require a minimum slope of 1:5 (rise:run) for this type of roofing material.
                
                (a) Calculate the slope of the proposed roof design.
                (b) Does it meet building code requirements?
                (c) What is the angle of the roof with respect to the horizontal?`,
                "answer": `(a) Slope of the proposed roof:
                \\(m = \\frac{\\text{rise}}{\\text{run}} = \\frac{3}{12} = \\frac{1}{4} = 0.25\\)
                
                (b) Building code requirement: 1:5 = 0.2
                Since 0.25 > 0.2, the design exceeds the minimum requirement and meets building codes.
                
                (c) Angle with horizontal:
                \\(\\tan θ = \\frac{3}{12} = 0.25\\)
                \\(θ = \\tan^{-1}(0.25) ≈ 14.0°\\)
                
                The roof makes an angle of approximately 14° with the horizontal.`
            }
        ]
    };
    MathQuestionModule.render(content, 'slope-identity-container');
});
</script>

### Key Takeaways

```{important}
**Essential Slope Concepts:**

1. **Slope Formula**: $m = \frac{y_2 - y_1}{x_2 - x_1}$ for points $(x_1, y_1)$ and $(x_2, y_2)$

2. **Types of Slopes**:
   - Positive: Line rises left to right
   - Negative: Line falls left to right
   - Zero: Horizontal line
   - Undefined: Vertical line

3. **Perpendicular Lines**: Product of slopes = -1

4. **Parallel Lines**: Same slope

5. **Real-World Applications**: Gradients, rates of change, engineering design
```