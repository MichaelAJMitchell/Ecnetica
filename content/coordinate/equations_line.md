# Equations of a Line

<iframe 
    src="https://drive.google.com/file/d/1wKHZYXShfyGUPCW-bBhQtMC1W2FJZCk/preview" 
    width="100%" 
    height="480" 
    frameborder="0" 
    allowfullscreen>
</iframe>

## Slope Revision

### Theory

Before exploring different forms of line equations, let's review the concept of slope:
- Slope $m = \frac{y_2 - y_1}{x_2 - x_1}$ for two points $(x_1, y_1)$ and $(x_2, y_2)$
- Represents the rate of change of $y$ with respect to $x$
- Determines the direction and steepness of a line

### Application

A line with slope $m = 2$ rises 2 units for every 1 unit it moves horizontally to the right.

## Equations of a Line

### Theory

There are several ways to express the equation of a line, each useful in different situations:

#### 1. Slope-Intercept Form
$$y = mx + c$$

where:
- $m$ is the slope
- $c$ is the y-intercept (where the line crosses the y-axis)

#### 2. Point-Slope Form
$$y - y_1 = m(x - x_1)$$

where:
- $m$ is the slope
- $(x_1, y_1)$ is a known point on the line

#### 3. Two-Point Form
$$\frac{y - y_1}{x - x_1} = \frac{y_2 - y_1}{x_2 - x_1}$$

where $(x_1, y_1)$ and $(x_2, y_2)$ are two known points on the line

#### 4. General Form
$$ax + by + c = 0$$

where $a$, $b$, and $c$ are constants, and at least one of $a$ or $b$ is non-zero

#### 5. Intercept Form
$$\frac{x}{a} + \frac{y}{b} = 1$$

where:
- $a$ is the x-intercept
- $b$ is the y-intercept
- Neither $a$ nor $b$ equals zero

#### Interactive Visualization: Line Equation Explorer

<div id="line-equation-explorer" class="visualization-container" style="height: 500px;"></div>
<script>
document.addEventListener('DOMContentLoaded', function() {
    MathVisualizer.createGraphFromDescription('line-equation-explorer', {
        boundingBox: [-10, 10, 10, -10],
        parametrizedFunctions: [{
            expression: 'm*(x - h) + k',
            title: 'Point-Slope Form: y - k = m(x - h)',
            parameters: {
                m: { min: -5, max: 5, value: 1, step: 0.1 },
                h: { min: -5, max: 5, value: 0, step: 0.5 },
                k: { min: -5, max: 5, value: 0, step: 0.5 }
            },
            features: ['intercepts']
        }],
        infoBox: {
            title: "Line Properties",
            lines: [
                {text: "Slope (m) = ${m}", dynamic: true},
                {text: "Point: (${h}, ${k})", dynamic: true},
                {text: "Y-intercept = ${k - m*h}", dynamic: true},
                {text: "X-intercept = ${h - k/m}", dynamic: true}
            ]
        }
    });
});
</script>

### Application

#### Examples

**Example 1: Converting between forms**

Given a line passing through point $(3, 5)$ with slope $m = 2$, express the equation in:
a) Point-slope form
b) Slope-intercept form
c) General form

**Solution:**

a) Point-slope form: $y - 5 = 2(x - 3)$

b) Slope-intercept form:
   - Expand: $y - 5 = 2x - 6$
   - Simplify: $y = 2x - 1$

c) General form:
   - From $y = 2x - 1$
   - Rearrange: $2x - y - 1 = 0$

**Example 2: Finding equation from two points**

Find the equation of the line passing through $A(2, 3)$ and $B(5, 9)$.

**Solution:**

Step 1: Calculate the slope
$$m = \frac{9 - 3}{5 - 2} = \frac{6}{3} = 2$$

Step 2: Use point-slope form with either point
Using point $A(2, 3)$:
$$y - 3 = 2(x - 2)$$

Step 3: Convert to slope-intercept form
$$y - 3 = 2x - 4$$
$$y = 2x - 1$$

**Example 3: Using intercept form**

A line crosses the x-axis at $(4, 0)$ and the y-axis at $(0, -3)$. Find its equation.

**Solution:**

Using intercept form with $a = 4$ and $b = -3$:
$$\frac{x}{4} + \frac{y}{-3} = 1$$

Simplifying:
$$\frac{x}{4} - \frac{y}{3} = 1$$

Multiplying by 12:
$$3x - 4y = 12$$

#### Multiple Choice Questions

<div id="line-equations-mcq" class="quiz-container"></div>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Line Equations Quiz",
        questions: [
            {
                text: "What is the slope-intercept form of the line passing through \\((0, 4)\\) with slope \\(m = -\\frac{1}{2}\\)?",
                options: ["\\(y = -\\frac{1}{2}x + 4\\)", "\\(y = \\frac{1}{2}x + 4\\)", "\\(y = -\\frac{1}{2}x - 4\\)", "\\(y = 4x - \\frac{1}{2}\\)"],
                correctIndex: 0,
                explanation: "Using \\(y = mx + c\\) with \\(m = -\\frac{1}{2}\\) and \\(c = 4\\) (the y-intercept), we get \\(y = -\\frac{1}{2}x + 4\\).",
                difficulty: "Basic"
            },
            {
                text: "Which equation represents a line parallel to \\(y = 3x - 2\\) passing through \\((1, 5)\\)?",
                options: ["\\(y = 3x + 2\\)", "\\(y = -3x + 8\\)", "\\(y = 3x - 2\\)", "\\(y = \\frac{1}{3}x + \\frac{14}{3}\\)"],
                correctIndex: 0,
                explanation: "Parallel lines have the same slope. Using \\(m = 3\\) and point \\((1, 5)\\): \\(y - 5 = 3(x - 1)\\), which simplifies to \\(y = 3x + 2\\).",
                difficulty: "Intermediate"
            },
            {
                text: "Convert \\(2x - 3y + 6 = 0\\) to slope-intercept form.",
                options: ["\\(y = \\frac{2}{3}x + 2\\)", "\\(y = \\frac{2}{3}x - 2\\)", "\\(y = \\frac{3}{2}x + 3\\)", "\\(y = -\\frac{2}{3}x + 2\\)"],
                correctIndex: 0,
                explanation: "Solving for y: \\(-3y = -2x - 6\\), so \\(y = \\frac{2}{3}x + 2\\).",
                difficulty: "Basic"
            },
            {
                text: "A line has x-intercept 3 and y-intercept -2. What is its equation in general form?",
                options: ["\\(2x - 3y - 6 = 0\\)", "\\(2x + 3y - 6 = 0\\)", "\\(3x - 2y - 6 = 0\\)", "\\(3x + 2y - 6 = 0\\)"],
                correctIndex: 0,
                explanation: "Using intercept form: \\(\\frac{x}{3} + \\frac{y}{-2} = 1\\). Multiplying by 6: \\(2x - 3y = 6\\), or \\(2x - 3y - 6 = 0\\).",
                difficulty: "Intermediate"
            }
        ]
    };
    MCQQuiz.create('line-equations-mcq', quizData);
});
</script>

#### Sector Specific Questions: Line Equations Applications

<div id="line-equations-identity-container"></div>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const content = {
        "title": "Line Equations: Real-World Applications",
        "intro_content": `<p>Line equations are fundamental in modeling relationships between variables across many fields. Let's explore practical applications.</p>`,
        "questions": [
            {
                "category": "scientific",
                "title": "Chemistry: Reaction Rates",
                "content": `A chemist is studying a first-order reaction where the concentration decreases linearly with time. Initial measurements show:
                - At time t = 0 minutes, concentration = 8.0 mol/L
                - At time t = 5 minutes, concentration = 6.5 mol/L
                
                (a) Find the equation relating concentration C to time t.
                (b) When will the concentration reach 2.0 mol/L?
                (c) What is the rate of change of concentration?`,
                "answer": `(a) Finding the equation:
                Points: (0, 8.0) and (5, 6.5)
                
                Slope: \\(m = \\frac{6.5 - 8.0}{5 - 0} = \\frac{-1.5}{5} = -0.3\\) mol/L per minute
                
                Using slope-intercept form with y-intercept 8.0:
                \\(C = -0.3t + 8.0\\)
                
                (b) When C = 2.0:
                \\(2.0 = -0.3t + 8.0\\)
                \\(0.3t = 6.0\\)
                \\(t = 20\\) minutes
                
                (c) Rate of change = slope = -0.3 mol/L per minute
                The concentration decreases by 0.3 mol/L every minute.`
            },
            {
                "category": "financial",
                "title": "Business: Break-Even Analysis",
                "content": `A startup company has fixed costs of €50,000 per month and variable costs of €30 per unit produced. They sell each unit for €80.
                
                (a) Write the equation for total cost C as a function of units produced x.
                (b) Write the equation for revenue R as a function of units sold x.
                (c) Find the break-even point where cost equals revenue.
                (d) Express profit P as a function of x.`,
                "answer": `(a) Total cost equation:
                \\(C = 30x + 50000\\)
                (Fixed costs + variable costs per unit)
                
                (b) Revenue equation:
                \\(R = 80x\\)
                (Price per unit × number of units)
                
                (c) Break-even point (C = R):
                \\(30x + 50000 = 80x\\)
                \\(50000 = 50x\\)
                \\(x = 1000\\) units
                
                At break-even: Revenue = Cost = €80,000
                
                (d) Profit equation:
                \\(P = R - C = 80x - (30x + 50000)\\)
                \\(P = 50x - 50000\\)
                
                This shows the company makes €50 profit per unit after covering fixed costs.`
            },
            {
                "category": "engineering",
                "title": "Electrical Engineering: Ohm's Law",
                "content": `An electrical engineer is testing a resistor by measuring voltage (V) across it at different currents (I):
                - At I = 2.0 A, V = 10.0 V
                - At I = 5.0 A, V = 25.0 V
                
                (a) Find the equation relating voltage to current.
                (b) What is the resistance of the component?
                (c) What voltage would be measured at 8.0 A?
                (d) Graph this relationship and interpret the y-intercept.`,
                "answer": `(a) Finding V-I relationship:
                Points: (2.0, 10.0) and (5.0, 25.0)
                
                Slope: \\(m = \\frac{25.0 - 10.0}{5.0 - 2.0} = \\frac{15.0}{3.0} = 5.0\\) V/A
                
                Using point-slope form:
                \\(V - 10.0 = 5.0(I - 2.0)\\)
                \\(V = 5.0I\\)
                
                (b) Resistance:
                From Ohm's Law (V = IR), the slope represents resistance:
                \\(R = 5.0\\) Ω
                
                (c) Voltage at 8.0 A:
                \\(V = 5.0 × 8.0 = 40.0\\) V
                
                (d) The y-intercept is 0, which makes physical sense: 
                No current means no voltage drop across a pure resistor.`
            },
            {
                "category": "creative",
                "title": "Photography: Depth of Field",
                "content": `A photographer notes that for a particular lens at f/2.8, the depth of field (DOF) relates linearly to subject distance for portrait photography:
                - At 2m distance, DOF = 0.12m
                - At 5m distance, DOF = 0.30m
                
                (a) Find the equation relating DOF to distance d.
                (b) What is the DOF at 3.5m?
                (c) At what distance would the DOF be 0.5m?
                (d) Interpret the practical meaning of the slope.`,
                "answer": `(a) Finding the DOF equation:
                Points: (2, 0.12) and (5, 0.30)
                
                Slope: \\(m = \\frac{0.30 - 0.12}{5 - 2} = \\frac{0.18}{3} = 0.06\\) m/m
                
                Using point-slope form:
                \\(DOF - 0.12 = 0.06(d - 2)\\)
                \\(DOF = 0.06d\\)
                
                (b) DOF at 3.5m:
                \\(DOF = 0.06 × 3.5 = 0.21\\) m
                
                (c) Distance for DOF = 0.5m:
                \\(0.5 = 0.06d\\)
                \\(d = \\frac{0.5}{0.06} = 8.33\\) m
                
                (d) Slope interpretation:
                For every meter increase in subject distance, the depth of field increases by 6cm. This helps photographers plan their shots for desired background blur.`
            }
        ]
    };
    MathQuestionModule.render(content, 'line-equations-identity-container');
});
</script>

### Key Takeaways

```{important}
**Essential Line Equation Forms:**

1. **Slope-Intercept**: $y = mx + c$
   - Best for: graphing, identifying slope and y-intercept

2. **Point-Slope**: $y - y_1 = m(x - x_1)$
   - Best for: known point and slope

3. **Two-Point**: $\frac{y - y_1}{x - x_1} = \frac{y_2 - y_1}{x_2 - x_1}$
   - Best for: two known points

4. **General Form**: $ax + by + c = 0$
   - Best for: computational work, systems of equations

5. **Intercept Form**: $\frac{x}{a} + \frac{y}{b} = 1$
   - Best for: known intercepts

**Key Skills**: Converting between forms, finding equations from given information
```