<iframe 
    src="https://drive.google.com/file/d/1KQdEOxFP1FnUw8zJnDHHblAgbaGw_UCd/preview" 
    width="100%" 
    height="480" 
    frameborder="0" 
    allowfullscreen>
</iframe>

## Linear Equations Revision

### Theory
Before diving into quadratic equations, it's worth taking a moment to review linear equations.

Linear equations are a class of polynomial equations that can be rearranged into the **standard form**:

$$ax + b = 0$$

where $a$ and $b$ are any constant numbers (with $a \neq 0$), and $x$ is the variable we're solving for. Once in this form, solving for $x$ requires just a couple of steps:

$$ax + b = 0$$
$$ax = -b$$
$$x = -\frac{b}{a}$$

We first isolate the $x$ term by subtracting $b$ from both sides, then divide by $a$ to get $x$ on its own.

Linear equations get their name because they create straight lines when graphed. They're also called "first-order equations" or "equations of degree 1" because the highest power of $x$ is 1 (since $x$ could also be written as $x^1$).

```{tip}
When solving linear equations, always keep track of your operations and apply them to both sides of the equation consistently. This habit will serve you well for more complex equations later.
```

#### Interactive Visualization: Linear Equations

<div id="linear-equation-container" class="visualization-container" style="height: 500px;"></div>
<script>
document.addEventListener('DOMContentLoaded', function() {
    MathVisualizer.createGraphFromDescription('linear-equation-container', {
        boundingBox: [-5, 5, 5, -5],
        theme: 'light',
        useSequentialColors: true,
        infoBox: {
            title: "Linear Equation",
            lines: [
                {text: "y = ax + b", dynamic: false},
                {text: "a (slope): ${a}", dynamic: true},
                {text: "b (y-intercept): ${b}", dynamic: true},
                {text: "x-intercept: ${a !== 0 ? (-b/a).toFixed(2) : 'Undefined'}", dynamic: true}
            ],
            position: {top: 55, left: 20}
        },
        parametrizedFunctions: [
            {
                expression: 'a*x + b',
                title: 'Linear Function Explorer',
                parameters: {
                    a: { min: -3, max: 3, value: 1, step: 0.1 },
                    b: { min: -5, max: 5, value: 0, step: 0.1 }
                },
                features: [] // Adding an empty features array
            }
        ]
    });
});
</script>

### Application

#### Examples

##### Example 1
Let's solve: $3x + 9 = 3$

**Method 1: Converting to standard form first**

$$3x + 9 = 3 \quad \text{(Not in standard form yet)}$$

$$3x + 9 - 3 = 3 - 3 \quad \text{(Subtracting 3 from both sides)}$$

$$3x + 6 = 0 \quad \text{(Now in standard form)}$$

$$x = -\frac{6}{3} = -2 \quad \text{(Dividing by 3)}$$

**Method 2: Direct approach**

$$3x + 9 = 3 \quad \text{(Original equation)}$$

$$3x = 3 - 9 \quad \text{(Moving constant to the right)}$$

$$3x = -6 \quad \text{(Simplifying)}$$

$$x = -\frac{6}{3} = -2 \quad \text{(Dividing by 3)}$$

```{note}
You might notice we took the long way in Method 1 - we didn't really have to bring it to standard form first - and you'd be right! For a simple linear equation, we could just directly solve as in Method 2 if all we care about is finding the value of $x$.

However, for more advanced problems like quadratic equations, converting to standard form is almost always the first step to solving them. This habit will come in handy later.
```

#### Multiple Choice Questions

<div id="linear-equation-mcq" class="quiz-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Linear Equations Quiz",
        questions: [
            {
                text: "What is the standard form of a linear equation?",
                options: [
                    "\\(ax^2 + bx + c = 0\\)",
                    "\\(ax + b = 0\\)",
                    "\\(\\frac{a}{x} + b = 0\\)",
                    "\\(a^x + b = 0\\)"
                ],
                correctIndex: 1,
                explanation: "The standard form of a linear equation is \\(ax + b = 0\\), where \\(a \\neq 0\\) and \\(b\\) are constants, and \\(x\\) is the variable.",
                difficulty: "Basic"
            },
            {
                text: "What is the solution to the linear equation \\(2x - 6 = 0\\)?",
                options: [
                    "\\(x = -3\\)",
                    "\\(x = 3\\)",
                    "\\(x = -4\\)",
                    "\\(x = 4\\)"
                ],
                correctIndex: 1,
                explanation: "To solve \\(2x - 6 = 0\\), we isolate the variable: \\(2x = 6\\), then \\(x = 3\\).",
                difficulty: "Basic"
            },
            {
                text: "Which of the following is NOT a linear equation?",
                options: [
                    "\\(3x + 2 = 7\\)",
                    "\\(x - 5 = 2x + 1\\)",
                    "\\(2x^2 + x = 3\\)",
                    "\\(4x = 12\\)"
                ],
                correctIndex: 2,
                explanation: "The equation \\(2x^2 + x = 3\\) contains an \\(x^2\\) term, making it a quadratic equation, not a linear equation.",
                difficulty: "Intermediate"
            }
        ]
    };
    
    MCQQuiz.create('linear-equation-mcq', quizData);
});
</script>

#### Identity Questions: Linear Equations Applications

<div id="linear-identity-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const linearContent = {
        "title": "Linear Equations: Real-World Applications",
        "intro_content": `
            <p>Linear equations are powerful tools for modeling many real-world situations. They describe relationships where one quantity changes at a constant rate relative to another.</p>
            <p>The general form of a linear equation is \\(ax + b = 0\\), or alternatively \\(y = mx + c\\) when used as a function, where \\(m\\) represents the rate of change (slope) and \\(c\\) represents the initial value or \\(y\\)-intercept.</p>
        `,
        "questions": [
            {
                "category": "scientific",
                "title": "Physics: Distance and Time",
                "content": `
                    <p>A car travels along a straight road at a constant speed of 60 km/h. After 2 hours, it is 150 km from its starting point.</p>
                    <p>a) Write a linear equation describing the car's distance from the starting point as a function of time.</p>
                    <p>b) How far from the starting point was the car when it began its journey?</p>
                    <p>c) How long will it take for the car to be 270 km from the starting point?</p>
                `,
                "answer": `
                    <p>a) If we let \\(d\\) represent the distance in kilometers and \\(t\\) represent the time in hours, then:</p>
                    <p>\\(d = 60t + d_0\\)</p>
                    <p>where \\(d_0\\) is the initial distance.</p>
                    <p>We know that when \\(t = 2\\), \\(d = 150\\):</p>
                    <p>\\(150 = 60 \\times 2 + d_0\\)</p>
                    <p>\\(150 = 120 + d_0\\)</p>
                    <p>\\(d_0 = 30\\)</p>
                    <p>Therefore, our linear equation is: \\(d = 60t + 30\\)</p>
                    
                    <p>b) The car was 30 km from the starting point when it began the journey (\\(t = 0\\)).</p>
                    
                    <p>c) To find when the car will be 270 km from the starting point:</p>
                    <p>\\(270 = 60t + 30\\)</p>
                    <p>\\(240 = 60t\\)</p>
                    <p>\\(t = 4\\) hours</p>
                `
            },
            {
                "category": "engineering",
                "title": "Civil Engineering: Material Expansion",
                "content": `
                    <p>A steel bridge expands linearly with temperature. Engineers have measured that the bridge is 150.00 meters long at 0°C and 150.08 meters long at 40°C.</p>
                    <p>a) Find the linear equation relating the bridge's length \\(L\\) to the temperature \\(T\\).</p>
                    <p>b) What will be the bridge's length at 25°C?</p>
                    <p>c) If the maximum safe length of the bridge is 150.12 meters, what is the maximum temperature the bridge can safely withstand?</p>
                `,
                "answer": `
                    <p>a) We can model the length \\(L\\) of the bridge (in meters) as a function of temperature \\(T\\) (in °C) using a linear equation:</p>
                    <p>\\(L = mT + b\\)</p>
                    <p>where \\(m\\) is the rate of expansion and \\(b\\) is the initial length.</p>
                    <p>Using the given data points:</p>
                    <p>When \\(T = 0\\)°C, \\(L = 150.00\\) m, so \\(b = 150.00\\)</p>
                    <p>When \\(T = 40\\)°C, \\(L = 150.08\\) m</p>
                    <p>Substituting to find \\(m\\):</p>
                    <p>\\(150.08 = m \\times 40 + 150.00\\)</p>
                    <p>\\(0.08 = 40m\\)</p>
                    <p>\\(m = 0.002\\) m/°C</p>
                    <p>Therefore, the linear equation is: \\(L = 0.002T + 150.00\\)</p>
                    
                    <p>b) At \\(T = 25\\)°C:</p>
                    <p>\\(L = 0.002 \\times 25 + 150.00 = 150.05\\) meters</p>
                    
                    <p>c) For the maximum safe length of 150.12 meters:</p>
                    <p>\\(150.12 = 0.002T + 150.00\\)</p>
                    <p>\\(0.12 = 0.002T\\)</p>
                    <p>\\(T = 60\\)°C</p>
                    <p>The maximum safe temperature is 60°C.</p>
                `
            },
            {
                "category": "financial",
                "title": "Business: Cost Analysis",
                "content": `
                    <p>A manufacturing company has fixed costs of €5,000 per month and variable costs of €25 per unit produced.</p>
                    <p>a) Write a linear equation for the total monthly cost \\(C\\) as a function of the number of units \\(x\\) produced.</p>
                    <p>b) If the company sells each unit for €40, write an equation for the revenue \\(R\\) and profit \\(P\\).</p>
                    <p>c) How many units must the company produce and sell to break even?</p>
                `,
                "answer": `
                    <p>a) The total cost \\(C\\) is the sum of fixed costs and variable costs:</p>
                    <p>\\(C = 5,000 + 25x\\)</p>
                    <p>where \\(x\\) is the number of units produced.</p>
                    
                    <p>b) The revenue \\(R\\) from selling \\(x\\) units at €40 each is:</p>
                    <p>\\(R = 40x\\)</p>
                    <p>The profit \\(P\\) is revenue minus costs:</p>
                    <p>\\(P = R - C = 40x - (5,000 + 25x) = 40x - 5,000 - 25x = 15x - 5,000\\)</p>
                    
                    <p>c) At the break-even point, profit is zero:</p>
                    <p>\\(P = 0\\)</p>
                    <p>\\(15x - 5,000 = 0\\)</p>
                    <p>\\(15x = 5,000\\)</p>
                    <p>\\(x = 333.33\\)</p>
                    <p>Since you can't produce a fraction of a unit, the company must produce and sell 334 units to break even.</p>
                `
            },
            {
                "category": "creative",
                "title": "Music: Pitch and Frequency",
                "content": `
                    <p>In music theory, the relationship between the position on a guitar string (where you press down) and the pitch produced follows a linear relationship when expressed in appropriate units.</p>
                    <p>A guitarist notes that pressing down at the 12th fret (exactly halfway along the string) produces a note exactly one octave higher than the open string. On the low E string, the open string frequency is 82.41 Hz, and at the 12th fret, it's 164.82 Hz.</p>
                    <p>a) If we denote the fret number as \\(n\\) and the frequency as \\(f\\), find a linear relationship between \\(n\\) and \\(\\log_2(f/82.41)\\).</p>
                    <p>b) Use this relationship to predict the frequency at the 7th fret.</p>
                    <p>c) If another guitarist's E string is slightly out of tune at 80 Hz, what would be the frequency at the 12th fret?</p>
                `,
                "answer": `
                    <p>a) We know that the relationship between frequency and pitch is logarithmic (specifically, with base 2 for octaves). Let's define \\(y = \\log_2(f/82.41)\\).</p>
                    <p>For the open string (\\(n = 0\\)):</p>
                    <p>\\(y = \\log_2(82.41/82.41) = \\log_2(1) = 0\\)</p>
                    <p>For the 12th fret (\\(n = 12\\)):</p>
                    <p>\\(y = \\log_2(164.82/82.41) = \\log_2(2) = 1\\)</p>
                    <p>This gives us two points: (0,0) and (12,1). Using the point-slope form:</p>
                    <p>\\(y = \\frac{1}{12}n\\) or \\(\\log_2(f/82.41) = \\frac{n}{12}\\)</p>
                    
                    <p>b) For the 7th fret (\\(n = 7\\)):</p>
                    <p>\\(\\log_2(f/82.41) = \\frac{7}{12}\\)</p>
                    <p>\\(f/82.41 = 2^{7/12}\\)</p>
                    <p>\\(f = 82.41 \\times 2^{7/12} \\approx 82.41 \\times 1.4983 \\approx 123.47\\) Hz</p>
                    
                    <p>c) If the open string is at 80 Hz:</p>
                    <p>At the 12th fret, the frequency would be doubled: \\(80 \\times 2 = 160\\) Hz</p>
                    <p>This illustrates an important point about the guitar: regardless of the starting frequency, the 12th fret always produces exactly twice the frequency (one octave higher).</p>
                `
            }
        ]
    };
    
    MathQuestionModule.render(linearContent, 'linear-identity-container');
});
</script>

### Key Takeaways

```{important}
1. A linear equation can be written in the standard form $ax + b = 0$ where $a \neq 0$
2. To solve, isolate the variable: $x = -\frac{b}{a}$
3. When graphed, a linear equation forms a straight line
4. The slope of the line equals $-\frac{a}{b}$ in standard form, or $m$ in slope-intercept form $y = mx + c$
5. Linear equations model situations with constant rates of change
```

```{seealso}
For more advanced linear equation concepts, look into:
- Systems of linear equations
- Linear inequalities
- Linear functions and their transformations
- Applications in linear programming
```

## Quadratic Equations and their Form

### Theory

Quadratic equations are the next step up from linear equations in the polynomial family. They have the following **standard form**:

$$ax^2 + bx + c = 0$$

where $a$, $b$, and $c$ are constants (with $a \neq 0$), and $x$ is our variable. What makes an equation quadratic is the presence of that $x^2$ term — the **highest** power of $x$ must be 2.

Getting quadratic equations into this standard form serves two main purposes:
1. It's the starting point for solving them using standard techniques
2. The coefficients $a$, $b$, and $c$ reveal important information about the graph of the equation

If you can transform another type of equation into quadratic form without violating any mathematical rules, you can use quadratic techniques to solve problems that might otherwise seem challenging.

```{warning}
A common mistake is to confuse equations that contain $x^2$ with quadratic equations. Remember, a true quadratic equation must be able to be written in the form $ax^2 + bx + c = 0$. Equations like $x^2 + \frac{1}{x} = 3$ are not quadratic despite having an $x^2$ term!
```

#### Interactive Visualization: Quadratic Function Explorer

<div id="quadratic-form-container" class="visualization-container" style="height: 500px;"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    MathVisualizer.createGraphFromDescription('quadratic-form-container', {
        boundingBox: [-5, 5, 5, -5],
        theme: 'light',
        useSequentialColors: true,
        
        infoBox: {
            title: "Quadratic Function",
            lines: [
                {text: "y = ax² + bx + c", dynamic: false},
                {text: "a: ${a}", dynamic: true},
                {text: "b: ${b}", dynamic: true},
                {text: "c: ${c}", dynamic: true},
                {text: "Vertex: (${-b/(2*a)}, ${c-b*b/(4*a)})", dynamic: true}
            ],
            position: {top: 55, left: 20}
        },
        
        parametrizedFunctions: [
            {
                expression: 'a*x^2 + b*x + c',
                title: 'Quadratic Function Explorer',
                parameters: {
                    a: { min: -2, max: 2, value: 1, step: 0.1 },
                    b: { min: -5, max: 5, value: 0, step: 0.1 },
                    c: { min: -5, max: 5, value: 0, step: 0.1 }
                },
                features: ['zeros', 'extrema']
            }
        ]
    });
});
</script>

### Application
#### Examples: Identifying and Working with Quadratic Equations

##### Example 1: Expanding brackets

Is this a quadratic equation?

$$2x(x+3) = -x$$

To find out, we'll expand the brackets and bring everything to one side:

$$2x(x+3) = -x$$
$$2x^2 + 6x = -x$$
$$2x^2 + 7x = 0$$

Yes! This is a quadratic equation where $a=2$, $b=7$, and $c=0$.

##### Example 2: Substitution method

Is this a quadratic equation?

$$x^4 + x^2 + 1 = 0$$

At first glance, no—the highest power is 4, not 2. However, we can use a clever substitution. Let's define $t = x^2$ and see what happens:

$$x^4 + x^2 + 1 = 0$$
$$(x^2)^2 + x^2 + 1 = 0$$
$$t^2 + t + 1 = 0$$

We've transformed it into a quadratic equation in terms of $t$, where $a=1$, $b=1$, and $c=1$. After solving for $t$, we can find $x$ using $t = x^2$. This substitution trick appears frequently in exams and is worth mastering.

```{tip}
When faced with a polynomial equation where the powers of the variable increase by multiples of 2 (like $x^4$, $x^2$, $x^0$), try substituting $t = x^2$ to convert it to a quadratic equation.
```

##### Example 3: Trigonometric substitution

$$\tan^2(x) + \tan(x) + 2 = 0$$

This follows the same logic as Example 2. We can let $t = \tan(x)$ and substitute:

$$\tan^2(x) + \tan(x) + 2 = 0$$
$$t^2 + t + 2 = 0$$

Now we have a quadratic in $t$ with $a=1$, $b=1$, and $c=2$.

##### Example 4: Not all equations with $x^2$ are quadratic

$$\tan(x) + x^2 + 5 = 0$$

Despite having an $x^2$ term, this is not a quadratic equation. If we try to substitute $t = \tan(x)$:

$$t + x^2 + 5 = 0$$

We end up with two different variables ($t$ and $x$), and no way to convert between them. The presence of the trigonometric function $\tan(x)$ alongside the polynomial term $x^2$ prevents this from being converted to quadratic form.

##### Example 5: Functions with constants

$$x^2\sin\left(\frac{\pi}{3}\right) + x = 0$$

Although it involves a trigonometric term, this **is** a quadratic equation because $\sin\left(\frac{\pi}{3}\right)$ evaluates to a constant (approximately 0.866). The equation has the form:

$$ax^2 + bx + c = 0$$

where $a = \sin\left(\frac{\pi}{3}\right)$, $b = 1$, and $c = 0$.

#### Multiple Choice Questions

<div id="quadratic-form-mcq" class="quiz-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Quadratic Equations Form Quiz",
        questions: [
            {
                text: "Which of the following is a quadratic equation?",
                options: [
                    "\\(x^3 - 2x + 1 = 0\\)",
                    "\\(2x^2 + 3x - 5 = 0\\)",
                    "\\(\\frac{1}{x} + \\frac{1}{x^2} = 3\\)",
                    "\\(\\sqrt{x} + 2 = 0\\)"
                ],
                correctIndex: 1,
                explanation: "A quadratic equation has the form \\(ax^2 + bx + c = 0\\) where \\(a \\neq 0\\). The equation \\(2x^2 + 3x - 5 = 0\\) fits this form with \\(a = 2\\), \\(b = 3\\), and \\(c = -5\\).",
                difficulty: "Basic"
            },
            {
                text: "Which substitution would turn \\(x^4 - 5x^2 + 6 = 0\\) into a quadratic equation?",
                options: [
                    "Let \\(u = x\\)",
                    "Let \\(u = x^4\\)",
                    "Let \\(u = x^2\\)",
                    "This equation cannot be converted to a quadratic form"
                ],
                correctIndex: 2,
                explanation: "By substituting \\(u = x^2\\), the equation becomes \\(u^2 - 5u + 6 = 0\\), which is a quadratic equation in \\(u\\).",
                difficulty: "Intermediate"
            },
            {
                text: "Which of the following is NOT in standard quadratic form?",
                options: [
                    "\\(2x^2 - 3x + 1 = 0\\)",
                    "\\(x(x + 3) = 2\\)",
                    "\\(x^2 = 4x - 4\\)",
                    "\\(\\frac{x^2}{4} + \\frac{x}{2} = 2\\)"
                ],
                correctIndex: 1,
                explanation: "The equation \\(x(x + 3) = 2\\) is not in standard form \\(ax^2 + bx + c = 0\\). To convert it, we would expand: \\(x^2 + 3x = 2\\) and then rearrange: \\(x^2 + 3x - 2 = 0\\).",
                difficulty: "Intermediate"
            },
            {
                text: "If \\(\\sin(\\pi/4) = \\frac{\\sqrt{2}}{2}\\), which of the following is a quadratic equation?",
                options: [
                    "\\(x^2\\sin(x) + x + 1 = 0\\)",
                    "\\(x^2\\sin(\\pi/4) + x + 1 = 0\\)",
                    "\\(\\sin(x^2) + x + 1 = 0\\)",
                    "\\(\\sin(\\pi/4)^2 + x + 1 = 0\\)"
                ],
                correctIndex: 1,
                explanation: "Since \\(\\sin(\\pi/4) = \\frac{\\sqrt{2}}{2}\\) is a constant, the equation \\(x^2\\sin(\\pi/4) + x + 1 = 0\\) can be written as \\(\\frac{\\sqrt{2}}{2}x^2 + x + 1 = 0\\), which is a quadratic equation.",
                difficulty: "Advanced"
            }
        ]
    };
    
    MCQQuiz.create('quadratic-form-mcq', quizData);
});
</script>

#### Identity Questions: Quadratic Equations Applications

<div id="quadratic-form-identity-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quadraticFormContent = {
        "title": "Quadratic Equations: Form and Applications",
        "intro_content": `
            <p>Quadratic equations, expressed in the standard form \\(ax^2 + bx + c = 0\\) where \\(a \\neq 0\\), appear across numerous fields and applications. Understanding how to identify, transform, and work with these equations is fundamental to solving many real-world problems.</p>
            <p>The structure of quadratic equations allows us to model situations where quantities change at varying rates, rather than the constant rate seen in linear relationships.</p>
        `,
        "questions": [
            {
                "category": "scientific",
                "title": "Physics: Projectile Motion",
                "content": `
                    <p>A physicist is studying projectile motion. When an object is thrown upward with an initial velocity \\(v_0\\) from a height \\(h_0\\), its height \\(h\\) at time \\(t\\) is given by:</p>
                    <p>\\(h = h_0 + v_0t - \\frac{1}{2}gt^2\\)</p>
                    <p>where \\(g\\) is the acceleration due to gravity (approximately 9.8 m/s²).</p>
                    <p>a) Explain why this is a quadratic equation in terms of \\(t\\).</p>
                    <p>b) If a ball is thrown upward at 15 m/s from a height of 2 meters, write the equation for its height.</p>
                    <p>c) To find when the ball hits the ground, what would you set \\(h\\) equal to, and what form would the resulting equation take?</p>
                `,
                "answer": `
                    <p>a) The equation \\(h = h_0 + v_0t - \\frac{1}{2}gt^2\\) is quadratic in terms of \\(t\\) because it contains a \\(t^2\\) term (specifically \\(-\\frac{1}{2}gt^2\\)), and the highest power of \\(t\\) is 2. We can identify the coefficients as:</p>
                    <p>\\(a = -\\frac{1}{2}g\\) (coefficient of \\(t^2\\))</p>
                    <p>\\(b = v_0\\) (coefficient of \\(t\\))</p>
                    <p>\\(c = h_0\\) (constant term)</p>
                    
                    <p>b) Given \\(v_0 = 15\\) m/s, \\(h_0 = 2\\) meters, and \\(g = 9.8\\) m/s², the equation becomes:</p>
                    <p>\\(h = 2 + 15t - \\frac{1}{2} \\times 9.8 \\times t^2\\)</p>
                    <p>\\(h = 2 + 15t - 4.9t^2\\)</p>
                    
                    <p>c) When the ball hits the ground, its height is zero: \\(h = 0\\)</p>
                    <p>This gives us:</p>
                    <p>\\(0 = 2 + 15t - 4.9t^2\\)</p>
                    <p>Rearranging to standard form:</p>
                    <p>\\(4.9t^2 - 15t - 2 = 0\\)</p>
                    <p>This is a quadratic equation in standard form \\(at^2 + bt + c = 0\\) with \\(a = 4.9\\), \\(b = -15\\), and \\(c = -2\\).</p>
                `
            },
            {
                "category": "engineering",
                "title": "Electrical Engineering: Circuit Design",
                "content": `
                    <p>An electrical engineer is designing a resonant circuit with a capacitor and inductor. The resonant frequency \\(f\\) of the circuit is given by:</p>
                    <p>\\(f = \\frac{1}{2\\pi\\sqrt{LC}}\\)</p>
                    <p>where \\(L\\) is the inductance in henries and \\(C\\) is the capacitance in farads.</p>
                    <p>a) If the engineer needs a circuit with a resonant frequency of 1 MHz (10⁶ Hz) and has a fixed capacitance of 10 nF (10⁻⁸ F), how would you set up an equation to find the required inductance?</p>
                    <p>b) Show that this equation can be transformed into a quadratic equation.</p>
                    <p>c) What additional techniques would you use to solve for the inductance?</p>
                `,
                "answer": `
                    <p>a) We start with the resonant frequency formula:</p>
                    <p>\\(f = \\frac{1}{2\\pi\\sqrt{LC}}\\)</p>
                    <p>Given \\(f = 10^6\\) Hz and \\(C = 10^{-8}\\) F, we substitute these values:</p>
                    <p>\\(10^6 = \\frac{1}{2\\pi\\sqrt{L \\times 10^{-8}}}\\)</p>
                    
                    <p>b) To transform this into a quadratic equation, we rearrange to isolate \\(L\\):</p>
                    <p>\\(10^6 = \\frac{1}{2\\pi\\sqrt{L \\times 10^{-8}}}\\)</p>
                    <p>\\(2\\pi \\times 10^6 \\times \\sqrt{L \\times 10^{-8}} = 1\\)</p>
                    <p>\\(\\sqrt{L \\times 10^{-8}} = \\frac{1}{2\\pi \\times 10^6}\\)</p>
                    <p>Squaring both sides:</p>
                    <p>\\(L \\times 10^{-8} = \\frac{1}{(2\\pi \\times 10^6)^2}\\)</p>
                    <p>\\(L = \\frac{1}{10^{-8} \\times (2\\pi \\times 10^6)^2}\\)</p>
                    
                    <p>Alternatively, if we were looking for values of \\(L\\) and \\(C\\) that satisfy a specific frequency and had a constraint like \\(L + C = k\\) (where \\(k\\) is a constant), we could substitute \\(C = k - L\\) into the frequency equation and expand to get a quadratic in \\(L\\).</p>
                    
                    <p>c) In this specific problem, since we're solving directly for \\(L\\) with known values of \\(f\\) and \\(C\\), we can calculate:</p>
                    <p>\\(L = \\frac{1}{(2\\pi f)^2 C} = \\frac{1}{(2\\pi \\times 10^6)^2 \\times 10^{-8}} \\approx 2.53 \\times 10^{-6}\\) H or about 2.53 μH</p>
                    
                    <p>If the equation were truly quadratic, we would use standard quadratic solving techniques, including factoring or the quadratic formula, then verify our solutions in the original context to ensure they're physically meaningful (e.g., positive values for inductance).</p>
                `
            },
            {
                "category": "financial",
                "title": "Economics: Market Equilibrium",
                "content": `
                    <p>An economist modeling a market has determined the following:</p>
                    <p>Supply function: \\(S(p) = 2p^2 + 3p\\) (quantity supplied at price \\(p\\))</p>
                    <p>Demand function: \\(D(p) = 100 - p^2\\) (quantity demanded at price \\(p\\))</p>
                    <p>a) Set up an equation to find the market equilibrium price (where supply equals demand).</p>
                    <p>b) Transform this equation into standard quadratic form.</p>
                    <p>c) If the demand function changes to \\(D(p) = 120 - 2p^2\\), how would the equilibrium equation change, and what form would it take?</p>
                `,
                "answer": `
                    <p>a) At market equilibrium, supply equals demand:</p>
                    <p>\\(S(p) = D(p)\\)</p>
                    <p>\\(2p^2 + 3p = 100 - p^2\\)</p>
                    
                    <p>b) Transforming into standard form:</p>
                    <p>\\(2p^2 + 3p = 100 - p^2\\)</p>
                    <p>\\(3p^2 + 3p - 100 = 0\\)</p>
                    <p>Dividing by 3 to simplify:</p>
                    <p>\\(p^2 + p - 33.33 = 0\\)</p>
                    <p>This is in standard form \\(ap^2 + bp + c = 0\\) where \\(a = 1\\), \\(b = 1\\), and \\(c = -33.33\\).</p>
                    
                    <p>c) With the new demand function \\(D(p) = 120 - 2p^2\\), the equilibrium equation becomes:</p>
                    <p>\\(S(p) = D(p)\\)</p>
                    <p>\\(2p^2 + 3p = 120 - 2p^2\\)</p>
                    <p>\\(4p^2 + 3p - 120 = 0\\)</p>
                    <p>This is still a quadratic equation in standard form with \\(a = 4\\), \\(b = 3\\), and \\(c = -120\\).</p>
                    
                    <p>The coefficient of \\(p^2\\) has increased from 3 to 4, and the constant term has changed from -100 to -120. This will result in different equilibrium prices compared to the original scenario.</p>
                `
            },
            {
                "category": "creative",
                "title": "Architecture: Arch Design",
                "content": `
                    <p>An architect is designing an arched doorway whose shape follows a parabola. The doorway is 3 meters wide at the base and 4 meters high at the center.</p>
                    <p>a) Setting up a coordinate system with the origin at the center of the base of the arch, write a quadratic equation that describes the shape of the arch.</p>
                    <p>b) If the architect wants to ensure there's at least 2 meters of height at 1 meter from the center, does the current design satisfy this requirement?</p>
                    <p>c) How would you modify the equation if the architect wants to make the arch 5 meters high while keeping the same width?</p>
                `,
                "answer": `
                    <p>a) We'll establish a coordinate system with the origin (0,0) at the center of the base, the x-axis running horizontally, and the y-axis running vertically up through the center of the arch.</p>
                    
                    <p>A general form of a parabola with vertex at (0,0) is \\(y = ax^2\\). Since the arch opens downward, we have \\(y = -ax^2 + b\\) where \\(b\\) is the height at the center.</p>
                    
                    <p>We know two points on the parabola:</p>
                    <p>(0,4): At the center (\\(x = 0\\)), the height is 4 meters</p>
                    <p>(1.5,0): At the edges (\\(x = \\pm1.5\\)), the height is 0 (the base)</p>
                    
                    <p>From the first point (0,4):</p>
                    <p>\\(4 = -a(0)^2 + b = b\\)</p>
                    <p>So \\(b = 4\\)</p>
                    
                    <p>From the second point (1.5,0):</p>
                    <p>\\(0 = -a(1.5)^2 + 4\\)</p>
                    <p>\\(a(1.5)^2 = 4\\)</p>
                    <p>\\(a = \\frac{4}{2.25} = \\frac{16}{9}\\)</p>
                    
                    <p>Therefore, the equation of the arch is:</p>
                    <p>\\(y = -\\frac{16}{9}x^2 + 4\\)</p>
                    
                    <p>b) To check if there's at least 2 meters of height at 1 meter from the center, we evaluate the function at \\(x = 1\\):</p>
                    <p>\\(y = -\\frac{16}{9}(1)^2 + 4 = -\\frac{16}{9} + 4 = 4 - \\frac{16}{9} = \\frac{36 - 16}{9} = \\frac{20}{9} \\approx 2.22\\) meters</p>
                    <p>Since 2.22 > 2, the current design does satisfy the requirement.</p>
                    
                    <p>c) To modify the equation for a 5-meter height while keeping the same width, we adjust the coefficient \\(b\\) to 5 and recalculate \\(a\\):</p>
                    <p>Using the point (1.5,0):</p>
                    <p>\\(0 = -a(1.5)^2 + 5\\)</p>
                    <p>\\(a(1.5)^2 = 5\\)</p>
                    <p>\\(a = \\frac{5}{2.25} = \\frac{20}{9}\\)</p>
                    
                    <p>The new equation would be:</p>
                    <p>\\(y = -\\frac{20}{9}x^2 + 5\\)</p>
                    <p>This parabola has the same width at the base (3 meters) but reaches a height of 5 meters at the center.</p>
                `
            }
        ]
    };
    
    MathQuestionModule.render(quadraticFormContent, 'quadratic-form-identity-container');
});
</script>

### Key Takeaways

```{important}
1. A quadratic equation has the form $ax^2 + bx + c = 0$ where $a \neq 0$
2. Equations can often be rewritten or transformed into quadratic form
3. Using substitution, we can convert some higher-degree equations into quadratics
4. Not all equations containing $x^2$ are quadratics, especially if they contain other non-polynomial functions of $x$
5. A trigonometric expression that doesn't contain $x$ as a variable acts as a constant in the equation
```

## Factorizing Quadratic Equations by Inspection

### Theory

Factorizing by inspection is the most intuitive approach to solving quadratic equations. At its core, factorization means breaking down an expression into simpler parts that multiply together to give the original expression.

When we have a quadratic equation in standard form:

$ax^2 + bx + c = 0$

Factorizing means rewriting it as:

$(px + q)(rx + s) = 0$

Where $p$, $q$, $r$, and $s$ are constants we need to find. The beauty of this approach is that once factorized, the solutions become immediately apparent thanks to the **zero product property**: if a product equals zero, at least one of the factors must be zero.

```{tip}
Factorizing by inspection works best when:
- The coefficients are "nice" integers (no messy fractions or surds)
- You have strong pattern recognition skills
- You need a quick solution without using formulas

If you see fractions, decimals, or square roots in your coefficients, you're probably better off using the quadratic formula directly.
```

### The Factorizing Process

Let's break down the approach:

1. Ensure your equation is in standard form with zero on the right side
2. Look for two numbers that:
   - Multiply to give $ac$ (the product of the first and last coefficients)
   - Add up to give $b$ (the middle coefficient)
3. Use these numbers to split the middle term and create your factors

#### Interactive Visualization: Factorization Explorer

<div id="factorization-container" class="visualization-container" style="height: 500px;"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const factorizationGraph = MathVisualizer.createGraphFromDescription('factorization-container', {
        boundingBox: [-10, 10, 10, -10],
        theme: 'light',
        useSequentialColors: true,
        
        infoBox: {
            title: "Factorization Explorer",
            lines: [
                {text: "y = (x+p)(x+q)", dynamic: false},
                {text: "p: ${p}", dynamic: true},
                {text: "q: ${q}", dynamic: true},
                {text: "Expanded: y = x² + ${p+q}x + ${p*q}", dynamic: true},
                {text: "Roots: x = ${-p} and x = ${-q}", dynamic: true}
            ],
            position: {top: 55, left: 20}
        },
        
        parametrizedFunctions: [
            {
                expression: '(x+p)*(x+q)',
                title: 'Factorization Explorer',
                parameters: {
                    p: { min: -5, max: 5, value: 2, step: 0.1 },
                    q: { min: -5, max: 5, value: -3, step: 0.1 }
                },
                features: ['zeros']
            }
        ]
    });
    
    // Fix: Ensure quadraticParams exists on the board object
    factorizationGraph.board.quadraticParams = factorizationGraph.parameterValues;
    
    // Create the point elements after the quadraticParams are set
    factorizationGraph.board.create('point', [
        function() { return -this.board.quadraticParams.p; }, 0
    ], { 
        name: 'Root 1',
        size: 4,
        fillColor: '#e74c3c',
        strokeColor: '#ffffff'
    });
    
    factorizationGraph.board.create('point', [
        function() { return -this.board.quadraticParams.q; }, 0
    ], { 
        name: 'Root 2',
        size: 4,
        fillColor: '#3498db',
        strokeColor: '#ffffff'
    });
});
</script>

### Application

#### Example: Step by Step

Let's work through:

$x^2 + 2x - 8 = 0$

**Step 1:** We need to find two numbers that multiply to give $-8$ (which is $a \times c = 1 \times -8$) and add up to give $+2$ (our $b$ value).

**Step 2:** Let's list possible number pairs that multiply to give $-8$:
- $1 \times -8 = -8$ (sum: $1 + (-8) = -7$)
- $2 \times -4 = -8$ (sum: $2 + (-4) = -2$)
- $-1 \times 8 = -8$ (sum: $-1 + 8 = 7$)
- $-2 \times 4 = -8$ (sum: $-2 + 4 = 2$) ← This works!

**Step 3:** Now we've found our pair: $-2$ and $4$. Let's use them to split the middle term:
$x^2 + 2x - 8 = x^2 - 2x + 4x - 8$

**Step 4:** Group the terms in pairs and factor each pair:
$x^2 - 2x + 4x - 8 = x(x - 2) + 4(x - 2)$

**Step 5:** Factor out the common term $(x - 2)$:
$x(x - 2) + 4(x - 2) = (x + 4)(x - 2)$

So our factorized equation is:
$(x + 4)(x - 2) = 0$

#### Finding the Solutions

Now that we have factorized the equation, the solutions are straightforward:

If $(x + 4)(x - 2) = 0$, then either:
- $x + 4 = 0$, which gives $x = -4$
- $x - 2 = 0$, which gives $x = 2$

We can verify these solutions:
- For $x = -4$: $(-4)^2 + 2(-4) - 8 = 16 - 8 - 8 = 0$ ✓
- For $x = 2$: $(2)^2 + 2(2) - 8 = 4 + 4 - 8 = 0$ ✓

$x = 2$ and $x = -4$ are the **roots** of the quadratic equation.

```{warning}
When the leading coefficient isn't 1 (i.e., $a \neq 1$), factorizing by inspection becomes more challenging because we have more combinations to consider.

Two approaches for these cases:
1. First multiply everything by $a$ to make the coefficient of $x^2$ equal to $a^2$, then find factors where the outer terms multiply to give $a^2 \times c$
2. Use the quadratic formula directly (which we'll cover in a later section)
```

#### Multiple Choice Questions

<div id="factorization-mcq" class="quiz-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Factorizing Quadratics Quiz",
        questions: [
            {
                text: "The factorized form of \\(x^2 - 7x + 12 = 0\\) is:",
                options: [
                    "\\((x - 3)(x - 4) = 0\\)",
                    "\\((x - 4)(x - 3) = 0\\)",
                    "\\((x - 6)(x - 2) = 0\\)",
                    "\\((x - 12)(x + 1) = 0\\)"
                ],
                correctIndex: 1,
                explanation: "We need to find two numbers that multiply to give 12 and add to give -7. The numbers are -3 and -4, since (-3)(-4) = 12 and (-3) + (-4) = -7. Therefore, the factorized form is \\((x - 4)(x - 3) = 0\\).",
                difficulty: "Basic"
            },
            {
                text: "To factorize \\(2x^2 - 5x - 3 = 0\\), you need to find two numbers that:",
                options: [
                    "Multiply to give -3 and add to give -5",
                    "Multiply to give -6 and add to give -5",
                    "Multiply to give 6 and add to give 5",
                    "Multiply to give 6 and add to give -5"
                ],
                correctIndex: 1,
                explanation: "Since the coefficient of \\(x^2\\) is 2, we need to find two numbers that multiply to give \\(2 \\times (-3) = -6\\) and add to give -5. These numbers are -6 and 1, since (-6)(1) = -6 and (-6) + 1 = -5.",
                difficulty: "Intermediate"
            },
            {
                text: "The solutions to the equation \\(x^2 + 6x + 8 = 0\\) are:",
                options: [
                    "\\(x = -4\\) and \\(x = -2\\)",
                    "\\(x = 4\\) and \\(x = 2\\)",
                    "\\(x = -4\\) and \\(x = 2\\)",
                    "\\(x = 4\\) and \\(x = -2\\)"
                ],
                correctIndex: 0,
                explanation: "Factorizing \\(x^2 + 6x + 8 = 0\\), we get \\((x + 4)(x + 2) = 0\\). Setting each factor equal to zero: \\(x + 4 = 0\\) gives \\(x = -4\\) and \\(x + 2 = 0\\) gives \\(x = -2\\).",
                difficulty: "Basic"
            },
            {
                text: "Which of the following quadratic expressions cannot be factorized using integers?",
                options: [
                    "\\(x^2 + 5x + 6\\)",
                    "\\(x^2 - 3x - 10\\)",
                    "\\(x^2 + x + 1\\)",
                    "\\(x^2 - 9\\)"
                ],
                correctIndex: 2,
                explanation: "For \\(x^2 + x + 1\\), we need two numbers that multiply to give 1 and add to give 1. The only numbers that multiply to give 1 are 1 and 1, which add to give 2, not 1. Alternatively, we can use the discriminant: \\(b^2 - 4ac = 1^2 - 4(1)(1) = 1 - 4 = -3\\). Since the discriminant is negative, this quadratic cannot be factorized using real numbers.",
                difficulty: "Advanced"
            }
        ]
    };
    
    MCQQuiz.create('factorization-mcq', quizData);
});
</script>

#### Identity Questions: Factorization Applications

<div id="factorization-identity-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const factorizationContent = {
        "title": "Factorizing Quadratic Equations: Applications",
        "intro_content": `
            <p>Factorizing quadratic equations allows us to find their roots efficiently and provides insight into the behavior of quadratic functions. This technique is essential across various fields where we need to determine when a quadratic expression equals zero or to simplify complex expressions.</p>
            <p>Understanding factorization helps us connect the algebraic form of a quadratic with its graphical representation and real-world meaning.</p>
        `,
        "questions": [
            {
                "category": "scientific",
                "title": "Physics: Projectile Range",
                "content": `
                    <p>In physics, when a projectile is launched at angle \\(θ\\) with initial velocity \\(v_0\\) from ground level, its horizontal range \\(R\\) is given by:</p>
                    <p>\\(R = \\frac{v_0^2 \\sin(2θ)}{g}\\)</p>
                    <p>where \\(g\\) is the acceleration due to gravity (9.8 m/s²).</p>
                    <p>A student wants to know at what angles a projectile launched at 20 m/s will reach a target 30 meters away.</p>
                    <p>a) Set up an equation to find the angles.</p>
                    <p>b) Show how this can be converted to a quadratic equation by using an appropriate substitution.</p>
                    <p>c) Solve the equation to find the possible launch angles.</p>
                `,
                "answer": `
                    <p>a) Starting with the range equation:</p>
                    <p>\\(R = \\frac{v_0^2 \\sin(2θ)}{g}\\)</p>
                    <p>We substitute the given values: \\(R = 30\\) m, \\(v_0 = 20\\) m/s, and \\(g = 9.8\\) m/s²:</p>
                    <p>\\(30 = \\frac{20^2 \\sin(2θ)}{9.8}\\)</p>
                    <p>\\(30 = \\frac{400 \\sin(2θ)}{9.8}\\)</p>
                    <p>\\(30 \\times 9.8 = 400 \\sin(2θ)\\)</p>
                    <p>\\(294 = 400 \\sin(2θ)\\)</p>
                    <p>\\(\\sin(2θ) = \\frac{294}{400} = 0.735\\)</p>
                    
                    <p>b) To convert this to a quadratic equation, we can use the substitution \\(u = \\tan(θ)\\). With this substitution, we can express \\(\\sin(2θ)\\) as:</p>
                    <p>\\(\\sin(2θ) = \\frac{2\\tan(θ)}{1+\\tan^2(θ)} = \\frac{2u}{1+u^2}\\)</p>
                    <p>Substituting this into our equation:</p>
                    <p>\\(0.735 = \\frac{2u}{1+u^2}\\)</p>
                    <p>\\(0.735(1+u^2) = 2u\\)</p>
                    <p>\\(0.735 + 0.735u^2 = 2u\\)</p>
                    <p>\\(0.735u^2 - 2u + 0.735 = 0\\)</p>
                    <p>This is a quadratic equation in \\(u\\) (where \\(u = \\tan(θ)\\)).</p>
                    
                    <p>c) Solving the quadratic equation:</p>
                    <p>\\(0.735u^2 - 2u + 0.735 = 0\\)</p>
                    <p>We can factor this by finding two numbers that multiply to give \\(0.735 \\times 0.735 = 0.54\\) and add to give \\(-2\\).</p>
                    <p>Let's use the quadratic formula instead:</p>
                    <p>\\(u = \\frac{2 \\pm \\sqrt{4 - 4 \\times 0.735 \\times 0.735}}{2 \\times 0.735}\\)</p>
                    <p>\\(u = \\frac{2 \\pm \\sqrt{4 - 2.16}}{1.47}\\)</p>
                    <p>\\(u = \\frac{2 \\pm \\sqrt{1.84}}{1.47}\\)</p>
                    <p>\\(u = \\frac{2 \\pm 1.356}{1.47}\\)</p>
                    <p>\\(u_1 = \\frac{2 + 1.356}{1.47} \\approx 2.283\\)</p>
                    <p>\\(u_2 = \\frac{2 - 1.356}{1.47} \\approx 0.438\\)</p>
                    
                    <p>Since \\(u = \\tan(θ)\\), we have:</p>
                    <p>\\(θ_1 = \\tan^{-1}(2.283) \\approx 66.4°\\)</p>
                    <p>\\(θ_2 = \\tan^{-1}(0.438) \\approx 23.6°\\)</p>
                    
                    <p>Therefore, the projectile will reach the target when launched at either approximately 23.6° or 66.4°.</p>
                    <p>This demonstrates how one obtains two solutions when solving projectile problems - a low angle and a high angle - both reaching the same distance.</p>
                `
            },
            {
                "category": "engineering",
                "title": "Civil Engineering: Bridge Design",
                "content": `
                    <p>A civil engineer is designing a suspension cable for a bridge. The cable will hang between two towers of equal height, forming a parabolic shape. The equation of the cable's shape in a suitable coordinate system is:</p>
                    <p>\\(y = ax^2 + bx + c\\)</p>
                    <p>where \\(y\\) is the height at position \\(x\\).</p>
                    <p>The cable needs to satisfy these conditions:</p>
                    <ul>
                        <li>The towers are located at \\(x = -100\\) m and \\(x = 100\\) m</li>
                        <li>The towers are 40 meters high (so \\(y = 40\\) at \\(x = -100\\) and \\(x = 100\\))</li>
                        <li>The lowest point of the cable should be at \\(y = 15\\) meters</li>
                    </ul>
                    <p>a) Write a system of equations to determine the coefficients \\(a\\), \\(b\\), and \\(c\\).</p>
                    <p>b) Use factorization to help solve for these coefficients.</p>
                    <p>c) Where exactly is the lowest point of the cable, and how would you verify this?</p>
                `,
                "answer": `
                    <p>a) We can set up a system of equations using the given conditions:</p>
                    <p>Condition 1: At \\(x = -100\\), \\(y = 40\\)</p>
                    <p>Condition a: At \\(x = -100\\), \\(y = 40\\)</p>
                    <p>\\(40 = a(-100)^2 + b(-100) + c\\)</p>
                    <p>\\(40 = 10000a - 100b + c\\)</p>
                    
                    <p>Condition b: At \\(x = 100\\), \\(y = 40\\)</p>
                    <p>\\(40 = a(100)^2 + b(100) + c\\)</p>
                    <p>\\(40 = 10000a + 100b + c\\)</p>
                    
                    <p>Condition 3: The lowest point of a parabola occurs at \\(x = -\\frac{b}{2a}\\)</p>
                    <p>Since the parabola opens upward (for stability, \\(a > 0\\)), the minimum height is:</p>
                    <p>\\(y_{min} = a\\left(-\\frac{b}{2a}\\right)^2 + b\\left(-\\frac{b}{2a}\\right) + c\\)</p>
                    <p>\\(y_{min} = a\\frac{b^2}{4a^2} - b\\frac{b}{2a} + c\\)</p>
                    <p>\\(y_{min} = \\frac{b^2}{4a} - \\frac{b^2}{2a} + c\\)</p>
                    <p>\\(y_{min} = -\\frac{b^2}{4a} + c\\)</p>
                    <p>Since \\(y_{min} = 15\\), we have:</p>
                    <p>\\(15 = -\\frac{b^2}{4a} + c\\)</p>
                    <p>\\(c = 15 + \\frac{b^2}{4a}\\)</p>
                    
                    <p>b) From the first two conditions, we can observe symmetry around \\(x = 0\\).</p>
                    <p>Subtracting the first equation from the second:</p>
                    <p>\\(0 = 10000a + 100b + c - (10000a - 100b + c)\\)</p>
                    <p>\\(0 = 200b\\)</p>
                    <p>\\(b = 0\\)</p>
                    
                    <p>This makes sense due to the symmetry of the problem - the cable should be symmetric around \\(x = 0\\).</p>
                    
                    <p>Since \\(b = 0\\), from the third condition:</p>
                    <p>\\(c = 15\\) (since \\(\\frac{b^2}{4a} = 0\\))</p>
                    
                    <p>Using this in the first condition:</p>
                    <p>\\(40 = 10000a + 15\\)</p>
                    <p>\\(25 = 10000a\\)</p>
                    <p>\\(a = \\frac{25}{10000} = \\frac{1}{400} = 0.0025\\)</p>
                    
                    <p>Therefore, the equation of the cable is:</p>
                    <p>\\(y = 0.0025x^2 + 15\\)</p>
                    
                    <p>c) The lowest point of the cable occurs at \\(x = -\\frac{b}{2a}\\). Since \\(b = 0\\), this gives \\(x = 0\\).</p>
                    <p>At \\(x = 0\\), \\(y = 0.0025(0)^2 + 15 = 15\\) meters, confirming our earlier determination.</p>
                    
                    <p>To verify this is indeed the minimum, we can check that the second derivative is positive:</p>
                    <p>\\(\\frac{d^2y}{dx^2} = 2a = 2(0.0025) = 0.005 > 0\\)</p>
                    <p>Since the second derivative is positive, the parabola opens upward, confirming that \\(x = 0\\) is indeed the location of the minimum point.</p>
                `
            },
            {
                "category": "financial",
                "title": "Business: Revenue Optimization",
                "content": `
                    <p>A company produces and sells customized software packages. Market research suggests that the relationship between the price \\(p\\) (in dollars) and the quantity \\(q\\) sold follows this demand equation:</p>
                    <p>\\(q = 1200 - 2p\\)</p>
                    <p>The total revenue \\(R\\) is given by \\(R = p \\times q\\).</p>
                    <p>a) Express the revenue \\(R\\) as a function of price \\(p\\) only.</p>
                    <p>b) Find the price that maximizes revenue using factorization.</p>
                    <p>c) If the company's cost function is \\(C = 50000 + 100q\\), find the price that maximizes profit, and explain how factorization helps in solving this problem.</p>
                `,
                "answer": `
                    <p>a) Revenue is price times quantity: \\(R = p \\times q\\)</p>
                    <p>Substituting the demand equation \\(q = 1200 - 2p\\):</p>
                    <p>\\(R = p \\times (1200 - 2p)\\)</p>
                    <p>\\(R = 1200p - 2p^2\\)</p>
                    <p>This is our revenue function in terms of price only.</p>
                    
                    <p>b) To find the price that maximizes revenue, we need to find where the derivative of the revenue function equals zero:</p>
                    <p>\\(\\frac{dR}{dp} = 1200 - 4p\\)</p>
                    <p>Setting this equal to zero:</p>
                    <p>\\(1200 - 4p = 0\\)</p>
                    <p>\\(4p = 1200\\)</p>
                    <p>\\(p = 300\\)</p>
                    
                    <p>To verify this is a maximum (not a minimum), we check that the second derivative is negative:</p>
                    <p>\\(\\frac{d^2R}{dp^2} = -4 < 0\\)</p>
                    <p>Since the second derivative is negative, \\(p = 300\\) gives a maximum revenue.</p>
                    
                    <p>c) Profit equals revenue minus cost: \\(P = R - C\\)</p>
                    <p>\\(P = 1200p - 2p^2 - (50000 + 100q)\\)</p>
                    <p>Substituting \\(q = 1200 - 2p\\):</p>
                    <p>\\(P = 1200p - 2p^2 - (50000 + 100(1200 - 2p))\\)</p>
                    <p>\\(P = 1200p - 2p^2 - 50000 - 120000 + 200p\\)</p>
                    <p>\\(P = 1400p - 2p^2 - 170000\\)</p>
                    
                    <p>To maximize profit, we take the derivative and set it to zero:</p>
                    <p>\\(\\frac{dP}{dp} = 1400 - 4p\\)</p>
                    <p>\\(1400 - 4p = 0\\)</p>
                    <p>\\(4p = 1400\\)</p>
                    <p>\\(p = 350\\)</p>
                    
                    <p>To verify this is a maximum, we check that the second derivative is negative:</p>
                    <p>\\(\\frac{d^2P}{dp^2} = -4 < 0\\)</p>
                    
                    <p>Factorization helps in solving this problem because:</p>
                    <p>1. It allows us to rewrite the revenue function in a form that makes it easier to differentiate</p>
                    <p>2. After differentiating, we get a linear equation that can be solved directly</p>
                    <p>3. The factorized form of the profit function gives insights into how revenue and cost interact</p>
                    
                    <p>Additionally, if we were to explore where the profit is zero, we would need to solve \\(1400p - 2p^2 - 170000 = 0\\), which can be approached through factorization after dividing by 2: \\(p^2 - 700p + 85000 = 0\\). The roots of this quadratic would give us the break-even prices.</p>
                `
            },
            {
                "category": "creative",
                "title": "Photography: Framing and Focus",
                "content": `
                    <p>A photographer is working with a camera lens that has a specific property: the area that appears in focus (depth of field) can be modeled by a quadratic equation.</p>
                    <p>For a particular lens setting, the range of distances (in meters) that will be in acceptable focus is given by:</p>
                    <p>\\(d^2 - 10d + 21 = 0\\)</p>
                    <p>where \\(d\\) represents the distance from the camera.</p>
                    <p>a) Find the range of distances that will be in acceptable focus by factorizing the equation.</p>
                    <p>b) If the photographer wants to ensure that everything between 2.5 meters and 6 meters is in focus, will the current lens setting work?</p>
                    <p>c) The photographer adjusts the lens to obtain a new depth of field equation: \\(d^2 - 9d + 20 = 0\\). Does this better match the desired focus range?</p>
                `,
                "answer": `
                    <p>a) To find the range of distances in focus, we need to factorize and solve the equation:</p>
                    <p>\\(d^2 - 10d + 21 = 0\\)</p>
                    <p>We need to find two numbers that multiply to give 21 and add to give -10.</p>
                    <p>The factors of 21 are: 1, 3, 7, and 21.</p>
                    <p>Testing the pairs:</p>
                    <p>-3 and -7: (-3)(-7) = 21 and (-3) + (-7) = -10</p>
                    <p>So the equation factors as:</p>
                    <p>\\((d - 3)(d - 7) = 0\\)</p>
                    <p>Setting each factor equal to zero:</p>
                    <p>\\(d - 3 = 0 \\implies d = 3\\)</p>
                    <p>\\(d - 7 = 0 \\implies d = 7\\)</p>
                    <p>Therefore, the range of distances in acceptable focus is from 3 meters to 7 meters from the camera.</p>
                    
                    <p>b) The photographer wants everything between 2.5 meters and 6 meters to be in focus.</p>
                    <p>The current setting gives a focus range of 3 to 7 meters.</p>
                    <p>This partially overlaps with the desired range but does not fully cover it:</p>
                    <p>- Objects at 2.5 meters will not be in focus (too close)</p>
                    <p>- Objects between 3 and 6 meters will be in focus (good)</p>
                    <p>- Objects between 6 and 7 meters will be in focus, but this extends beyond what's needed</p>
                    <p>Therefore, the current lens setting does not work optimally for the photographer's needs.</p>
                    
                    <p>c) For the new depth of field equation:</p>
                    <p>\\(d^2 - 9d + 20 = 0\\)</p>
                    <p>Factorizing:</p>
                    <p>We need two numbers that multiply to give 20 and add to give -9.</p>
                    <p>Testing the factor pairs of 20: (1, 20), (2, 10), (4, 5)</p>
                    <p>-4 and -5: (-4)(-5) = 20 and (-4) + (-5) = -9</p>
                    <p>So the equation factors as:</p>
                    <p>\\((d - 4)(d - 5) = 0\\)</p>
                    <p>The new focus range is from 4 meters to 5 meters.</p>
                    
                    <p>This new setting:</p>
                    <p>- Does not include objects at 2.5 meters (still too close)</p>
                    <p>- Includes only a subset (4 to 5 meters) of the desired range (2.5 to 6 meters)</p>
                    <p>- Provides a narrower depth of field than the previous setting</p>
                    
                    <p>This new setting is actually worse for the photographer's desired focus range. The ideal setting would produce a depth of field equation with roots at approximately 2.5 and 6 meters, such as \\(d^2 - 8.5d + 15 = 0\\), which would factor as \\((d - 2.5)(d - 6) = 0\\).</p>
                `
            }
        ]
    };
    
    MathQuestionModule.render(factorizationContent, 'factorization-identity-container');
});
</script>

### Key Takeaways

```{important}
1. Factorizing a quadratic means writing it in the form $(px + q)(rx + s) = 0$
2. The zero product property lets us set each factor equal to zero to find solutions
3. To factorize $ax^2 + bx + c$, find two numbers that multiply to give $ac$ and add to give $b$
4. Factorization works best with "nice" integer coefficients
5. The solutions of a quadratic equation are also called the "roots" or "zeros" of the corresponding function
```

## Graphical Solutions to Quadratic Equations

### Theory
#### Understanding the Parabola

When we solve quadratic equations in the form $ax^2 + bx + c = 0$, we're searching for values of $x$ that make the expression equal to zero. But what happens if we evaluate this expression for many different values of $x$?

If we plot these inputs and outputs on a coordinate plane, with $x$ on the horizontal axis and the result on the vertical axis, we get a distinctive U-shaped curve called a **parabola**. This graphical representation lets us visualize quadratic equations in a powerful way:

$y = ax^2 + bx + c$

Where $y$ represents the output value for any given input $x$.

```{tip}
You can think of the solutions to $ax^2 + bx + c = 0$ as the points where the parabola $y = ax^2 + bx + c$ crosses the x-axis (where $y = 0$). This visual interpretation makes many quadratic equation properties immediately apparent!
```

#### Key Insights from Graphing Quadratics

The graph of a quadratic equation reveals several important features:

1. **X-intercepts**: The points where the parabola crosses the x-axis are precisely the solutions to the quadratic equation. At these points, $y = 0$, which means they satisfy our original equation $ax^2 + bx + c = 0$.

2. **Vertex** (turning point): The lowest point of the parabola (if $a > 0$) or highest point (if $a < 0$) indicates where the function changes direction. If this point lies exactly on the x-axis, it means the equation has a repeated root.

3. **Number of solutions**: A parabola can:
   - Cross the x-axis twice (two distinct real solutions)
   - Touch the x-axis once (one repeated real solution)
   - Never cross the x-axis (two complex solutions)

#### Completing the Square

Another useful way to express quadratic expressions is in "completed square form":

$a(x + p)^2 + q$

Where $a$, $p$, and $q$ are constants. This form provides immediate insight into the graph's shape and position:
- $a$ determines whether the parabola opens upward ($a > 0$) or downward ($a < 0$)
- $p$ tells us the horizontal shift of the vertex (it's at $x = -p$)
- $q$ gives us the y-coordinate of the vertex

Converting from standard form to completed square form is a technique called "completing the square," which is also the foundation for deriving the quadratic formula.

```{warning}
When completing the square, always remember to:
1. Factor out the leading coefficient $a$ first (if it's not 1)
2. Only complete the square for the terms inside the parentheses
3. Balance any operations by applying them to both sides of the equation
```

#### The Process of Completing the Square

To convert $ax^2 + bx + c$ to $a(x + p)^2 + q$:

1. Factor out the coefficient $a$ from the first two terms
2. Complete the square for the expression inside the parentheses
3. Add and subtract the necessary constant to maintain equality

#### Interactive Visualization: Completing the Square

<div id="completing-square-container" class="visualization-container" style="height: 500px;"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    MathVisualizer.createGraphFromDescription('completing-square-container', {
        boundingBox: [-10, 10, 10, -10],
        theme: 'light',
        useSequentialColors: true,
        
        infoBox: {
            title: "Completing the Square",
            lines: [
                {text: "Standard form: y = ax² + bx + c", dynamic: false},
                {text: "a: ${a}", dynamic: true},
                {text: "b: ${b}", dynamic: true},
                {text: "c: ${c}", dynamic: true},
                {text: "Completed square form:", dynamic: false},
                {text: "y = ${a}(x + ${b/(2*a)})² + ${c - b*b/(4*a)}", dynamic: true},
                {text: "Vertex: (${-b/(2*a)}, ${c - b*b/(4*a)})", dynamic: true}
            ],
            position: {top: 55, left: 20}
        },
        
        parametrizedFunctions: [
            {
                expression: 'a*x^2 + b*x + c',
                title: 'Completing the Square Explorer',
                parameters: {
                    a: { min: -2, max: 2, value: 1, step: 0.1 },
                    b: { min: -5, max: 5, value: 2, step: 0.1 },
                    c: { min: -5, max: 5, value: -3, step: 0.1 }
                },
                features: ['zeros', 'extrema']
            }
        ]
    });
});
</script>

### Application
#### Examples: Graphical Solutions and Completing the Square

##### Example 1: When $a = 1$

Let's convert $x^2 + 3x - 4$ to completed square form:

**Step 1**: Since $a = 1$, we can proceed directly to completing the square.

**Step 2**: To complete the square for $x^2 + 3x$, we:
- Take half the coefficient of $x$: $\frac{3}{2}$
- Square it: $\left(\frac{3}{2}\right)^2 = \frac{9}{4}$
- Add and subtract this value to maintain equality:

$x^2 + 3x - 4 = x^2 + 3x + \frac{9}{4} - \frac{9}{4} - 4$

**Step 3**: Recognize the perfect square and simplify:

$x^2 + 3x - 4 = \left(x + \frac{3}{2}\right)^2 - \frac{9}{4} - 4 = \left(x + \frac{3}{2}\right)^2 - \frac{25}{4}$

So the completed square form is: $\left(x + \frac{3}{2}\right)^2 - \frac{25}{4}$

From this form, we can immediately identify:
- The vertex is at $\left(-\frac{3}{2}, -\frac{25}{4}\right)$ or $(-1.5, -6.25)$
- Since the vertex's y-coordinate is negative and $a > 0$, the parabola must cross the x-axis at two points

##### Example 2: When $a \neq 1$

Let's convert $5x^2 + 2x + 10$ to completed square form:

**Step 1**: Factor out the coefficient of $x^2$:

$5x^2 + 2x + 10 = 5\left(x^2 + \frac{2}{5}x\right) + 10$

**Step 2**: Complete the square inside the parentheses:
- Take half the coefficient of $x$: $\frac{1}{5}$
- Square it: $\left(\frac{1}{5}\right)^2 = \frac{1}{25}$
- Add and subtract the necessary value inside the parentheses:

$5\left(x^2 + \frac{2}{5}x + \frac{1}{25} - \frac{1}{25}\right) + 10$

**Step 3**: Rearrange and simplify:

$5\left(x^2 + \frac{2}{5}x + \frac{1}{25}\right) - 5 \cdot \frac{1}{25} + 10$
$5\left(x + \frac{1}{5}\right)^2 - \frac{5}{25} + 10$
$5\left(x + \frac{1}{5}\right)^2 - \frac{1}{5} + 10$
$5\left(x + \frac{1}{5}\right)^2 + \frac{49}{5}$

So the completed square form is: $5\left(x + \frac{1}{5}\right)^2 + \frac{49}{5}$

From this form, we can identify:
- The vertex is at $\left(-\frac{1}{5}, \frac{49}{5}\right)$ or $(-0.2, 9.8)$
- Since the vertex's y-coordinate is positive and $a > 0$, the parabola never crosses the x-axis, meaning the equation $5x^2 + 2x + 10 = 0$ has no real solutions

```{seealso}
The completed square form isn't just useful for finding the vertex of a parabola. It also:
- Makes it easier to sketch the graph of a quadratic function
- Provides a pathway to the quadratic formula
- Helps solve problems involving optimization
- Simplifies integrating certain expressions in calculus
```

#### Multiple Choice Questions

<div id="graphical-mcq" class="quiz-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Graphical Solutions & Completing the Square Quiz",
        questions: [
            {
                text: "The vertex of the parabola \\(y = 2x^2 - 8x + 3\\) is at the point:",
                options: [
                    "\\((2, -5)\\)",
                    "\\((-2, 11)\\)",
                    "\\((2, -5)\\)",
                    "\\((4, -13)\\)"
                ],
                correctIndex: 0,
                explanation: "To find the vertex, we can complete the square: \\(y = 2x^2 - 8x + 3 = 2(x^2 - 4x) + 3 = 2(x^2 - 4x + 4 - 4) + 3 = 2(x - 2)^2 - 8 + 3 = 2(x - 2)^2 - 5\\). From the completed square form, we can see that the vertex is at \\((2, -5)\\).",
                difficulty: "Intermediate"
            },
            {
                text: "A quadratic function crosses the x-axis at \\(x = -1\\) and \\(x = 3\\). If the y-intercept is 6, what is the function's equation?",
                options: [
                    "\\(y = 2x^2 - 4x - 6\\)",
                    "\\(y = 2x^2 + 4x - 6\\)",
                    "\\(y = -2x^2 + 4x + 6\\)",
                    "\\(y = 2x^2 - 4x + 6\\)"
                ],
                correctIndex: 3,
                explanation: "If the function crosses the x-axis at \\(x = -1\\) and \\(x = 3\\), then its factored form is \\(y = a(x + 1)(x - 3)\\) for some value of \\(a\\). Expanding: \\(y = a(x^2 - 2x - 3)\\). When \\(x = 0\\) (y-intercept), we have \\(y = a(-3) = 6\\), so \\(a = -2\\). Therefore, \\(y = -2(x^2 - 2x - 3) = -2x^2 + 4x + 6\\).",
                difficulty: "Advanced"
            },
            {
                text: "The completed square form of \\(f(x) = x^2 + 6x + 5\\) is:",
                options: [
                    "\\(f(x) = (x + 3)^2 - 4\\)",
                    "\\(f(x) = (x + 3)^2 - 9 + 5\\)",
                    "\\(f(x) = (x + 3)^2 - 4\\)",
                    "\\(f(x) = (x - 3)^2 - 4\\)"
                ],
                correctIndex: 2,
                explanation: "To complete the square for \\(x^2 + 6x + 5\\), we take half the coefficient of \\(x\\), which is 3, and square it, giving 9. Then: \\(x^2 + 6x + 5 = x^2 + 6x + 9 - 9 + 5 = (x + 3)^2 - 9 + 5 = (x + 3)^2 - 4\\).",
                difficulty: "Intermediate"
            },
            {
                text: "For the function \\(f(x) = -2x^2 + 4x - 3\\), which statement is true?",
                options: [
                    "The parabola opens upward and has two x-intercepts",
                    "The parabola opens downward and has no x-intercepts",
                    "The parabola opens downward and has one x-intercept",
                    "The parabola opens downward and has two x-intercepts"
                ],
                correctIndex: 1,
                explanation: "Since the coefficient of \\(x^2\\) is negative (-2), the parabola opens downward. To determine the number of x-intercepts, we check the discriminant: \\(b^2 - 4ac = 4^2 - 4(-2)(-3) = 16 - 24 = -8\\). Since the discriminant is negative, the function has no real roots and thus no x-intercepts.",
                difficulty: "Intermediate"
            }
        ]
    };
    
    MCQQuiz.create('graphical-mcq', quizData);
});
</script>

#### Identity Questions: Graphical Solutions Applications

<div id="graphical-identity-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const graphicalContent = {
        "title": "Graphical Solutions & Completing the Square: Applications",
        "intro_content": `
            <p>Graphical approaches to quadratic equations provide powerful insight into their behavior and solutions. The parabola's shape, position, and intersection points with the axes reveal crucial information about the quadratic function.</p>
            <p>Completing the square transforms a quadratic from standard form \\(ax^2 + bx + c\\) to the form \\(a(x - h)^2 + k\\), revealing its vertex at \\((h, k)\\) and making it easier to analyze its properties.</p>
        `,
        "questions": [
            {
                "category": "scientific",
                "title": "Physics: Projectile Motion Analysis",
                "content": `
                    <p>A physics student is studying projectile motion. When a ball is thrown upward with an initial velocity of 15 m/s from a height of 1.2 meters above the ground, its height \\(h\\) (in meters) after \\(t\\) seconds is given by:</p>
                    <p>\\(h = 1.2 + 15t - 4.9t^2\\)</p>
                    <p>a) By completing the square, find the maximum height reached by the ball and the time at which it occurs.</p>
                    <p>b) Find the times when the ball is at a height of 10 meters, and explain the significance of both solutions.</p>
                    <p>c) When does the ball hit the ground (\\(h = 0\\))? Explain how the graph helps understand the physical situation.</p>
                `,
                "answer": `
                    <p>a) First, let's rewrite the equation in the form suitable for completing the square:</p>
                    <p>\\(h = -4.9t^2 + 15t + 1.2\\)</p>
                    <p>Factoring out the coefficient of \\(t^2\\):</p>
                    <p>\\(h = -4.9(t^2 - \\frac{15}{-4.9}t) + 1.2\\)</p>
                    <p>\\(h = -4.9(t^2 - 3.06t) + 1.2\\)</p>
                    
                    <p>To complete the square, we take half the coefficient of \\(t\\) and square it: \\((-3.06/2)^2 = 2.33\\)</p>
                    <p>\\(h = -4.9(t^2 - 3.06t + 2.33 - 2.33) + 1.2\\)</p>
                    <p>\\(h = -4.9(t^2 - 3.06t + 2.33) + 4.9 \\times 2.33 + 1.2\\)</p>
                    <p>\\(h = -4.9(t - 1.53)^2 + 11.42 + 1.2\\)</p>
                    <p>\\(h = -4.9(t - 1.53)^2 + 12.62\\)</p>
                    
                    <p>From this completed square form, we can determine:</p>
                    <p>- The maximum height is 12.62 meters</p>
                    <p>- It occurs at \\(t = 1.53\\) seconds</p>
                    
                    <p>b) To find when the ball is at a height of 10 meters, we set \\(h = 10\\) and solve:</p>
                    <p>\\(10 = 1.2 + 15t - 4.9t^2\\)</p>
                    <p>\\(0 = -4.9t^2 + 15t - 8.8\\)</p>
                    <p>Using the quadratic formula:</p>
                    <p>\\(t = \\frac{-15 \\pm \\sqrt{15^2 - 4(-4.9)(-8.8)}}{2(-4.9)}\\)</p>
                    <p>\\(t = \\frac{-15 \\pm \\sqrt{225 - 172.48}}{-9.8}\\)</p>
                    <p>\\(t = \\frac{-15 \\pm \\sqrt{52.52}}{-9.8} \\approx \\frac{-15 \\pm 7.25}{-9.8}\\)</p>
                    <p>\\(t_1 \\approx \\frac{-15 + 7.25}{-9.8} \\approx 0.79\\) seconds</p>
                    <p>\\(t_2 \\approx \\frac{-15 - 7.25}{-9.8} \\approx 2.27\\) seconds</p>
                    
                    <p>These two solutions have physical significance:</p>
                    <p>- \\(t = 0.79\\) seconds: The ball reaches a height of 10 meters on its way up</p>
                    <p>- \\(t = 2.27\\) seconds: The ball passes through 10 meters again on its way down</p>
                    
                    <p>c) To find when the ball hits the ground, we set \\(h = 0\\) and solve:</p>
                    <p>\\(0 = 1.2 + 15t - 4.9t^2\\)</p>
                    <p>\\(4.9t^2 - 15t - 1.2 = 0\\)</p>
                    
                    <p>Using the quadratic formula:</p>
                    <p>\\(t = \\frac{15 \\pm \\sqrt{15^2 - 4(4.9)(-1.2)}}{2(4.9)}\\)</p>
                    <p>\\(t = \\frac{15 \\pm \\sqrt{225 + 23.52}}{9.8}\\)</p>
                    <p>\\(t = \\frac{15 \\pm \\sqrt{248.52}}{9.8}\\)</p>
                    <p>\\(t = \\frac{15 \\pm 15.76}{9.8}\\)</p>
                    <p>\\(t_1 \\approx \\frac{15 - 15.76}{9.8} \\approx -0.08\\) seconds</p>
                    <p>\\(t_2 \\approx \\frac{15 + 15.76}{9.8} \\approx 3.14\\) seconds</p>
                    
                    <p>Since time cannot be negative in this physical scenario (we start measuring from when the ball is thrown), we discard the negative solution. Therefore, the ball hits the ground approximately 3.14 seconds after being thrown.</p>
                    
                    <p>The graphical interpretation helps understand this situation. The parabola represents the ball's height over time:</p>
                    <p>- The y-intercept (1.2) represents the initial height</p>
                    <p>- The vertex (1.53, 12.62) represents the maximum height</p>
                    <p>- The positive x-intercept (3.14) represents when the ball hits the ground</p>
                    <p>- The negative x-intercept (-0.08) is not physically meaningful in this context</p>
                    <p>- The parabola opens downward due to gravity's negative acceleration</p>
                `
            },
            {
                "category": "engineering",
                "title": "Electrical Engineering: Resonant Circuit Design",
                "content": `
                    <p>An electrical engineer is designing a resonant RLC circuit. The impedance \\(Z\\) of the circuit can be expressed as a function of frequency \\(f\\) as follows:</p>
                    <p>\\(Z(f) = R + j(2\\pi fL - \\frac{1}{2\\pi fC})\\)</p>
                    <p>where \\(R = 50\\) ohms is the resistance, \\(L = 5\\) mH is the inductance, \\(C = 1\\) μF is the capacitance, and \\(j\\) is the imaginary unit.</p>
                    <p>The magnitude of the impedance is given by:</p>
                    <p>\\(|Z(f)| = \\sqrt{R^2 + (2\\pi fL - \\frac{1}{2\\pi fC})^2}\\)</p>
                    <p>a) Use completing the square to express the term \\((2\\pi fL - \\frac{1}{2\\pi fC})^2\\) in a form that reveals when it equals zero, and explain the significance of this frequency.</p>
                    <p>b) Show that \\(|Z(f)|\\) has a minimum value of \\(R\\), and determine at what frequency this occurs.</p>
                    <p>c) If the circuit is modified so that \\(C = 2\\) μF, how does this affect the frequency at which \\(|Z(f)|\\) is minimized?</p>
                `,
                "answer": `
                    <p>a) Let's focus on the term \\((2\\pi fL - \\frac{1}{2\\pi fC})^2\\)</p>
                    
                    <p>First, note that this is already in the form of a perfect square of a difference, so we don't need to complete the square in the traditional sense. However, we want to find when this term equals zero:</p>
                    <p>\\(2\\pi fL - \\frac{1}{2\\pi fC} = 0\\)</p>
                    <p>\\(2\\pi fL = \\frac{1}{2\\pi fC}\\)</p>
                    <p>\\(4\\pi^2 f^2LC = 1\\)</p>
                    <p>\\(f^2 = \\frac{1}{4\\pi^2 LC}\\)</p>
                    <p>\\(f = \\frac{1}{2\\pi\\sqrt{LC}}\\)</p>
                    
                    <p>For the given values \\(L = 5\\) mH = \\(5 \\times 10^{-3}\\) H and \\(C = 1\\) μF = \\(10^{-6}\\) F:</p>
                    <p>\\(f = \\frac{1}{2\\pi\\sqrt{5 \\times 10^{-3} \\times 10^{-6}}} = \\frac{1}{2\\pi\\sqrt{5 \\times 10^{-9}}} = \\frac{1}{2\\pi \\times 7.07 \\times 10^{-5}} \\approx 71.2\\) Hz</p>
                    
                    <p>This frequency is the <strong>resonant frequency</strong> of the circuit. At this frequency, the inductive reactance \\(X_L = 2\\pi fL\\) and the capacitive reactance \\(X_C = \\frac{1}{2\\pi fC}\\) exactly cancel each other out, leaving only the resistance \\(R\\) to determine the impedance.</p>
                    
                    <p>b) The magnitude of the impedance is:</p>
                    <p>\\(|Z(f)| = \\sqrt{R^2 + (2\\pi fL - \\frac{1}{2\\pi fC})^2}\\)</p>
                    
                    <p>Since the square root of a sum of squares is always greater than or equal to any individual term, \\(|Z(f)| \\geq R\\).</p>
                    
                    <p>The minimum value of \\(|Z(f)| = R\\) occurs when \\((2\\pi fL - \\frac{1}{2\\pi fC})^2 = 0\\), which happens at the resonant frequency we calculated in part (a): \\(f = \\frac{1}{2\\pi\\sqrt{LC}} \\approx 71.2\\) Hz.</p>
                    
                    <p>At resonance, the impedance is purely resistive: \\(Z = R = 50\\) ohms. This is significant in circuit design because:</p>
                    <p>- Voltage and current are in phase (no reactive component)</p>
                    <p>- Power transfer is maximized</p>
                    <p>- The circuit can be used for frequency selection (as in radio tuning)</p>
                    
                    <p>c) If the capacitance is changed to \\(C = 2\\) μF = \\(2 \\times 10^{-6}\\) F, the new resonant frequency becomes:</p>
                    <p>\\(f_{new} = \\frac{1}{2\\pi\\sqrt{5 \\times 10^{-3} \\times 2 \\times 10^{-6}}} = \\frac{1}{2\\pi\\sqrt{10 \\times 10^{-9}}} = \\frac{1}{2\\pi \\times 10^{-4}} \\approx 50.3\\) Hz</p>
                    
                    <p>Therefore, doubling the capacitance reduces the resonant frequency by a factor of \\(\\frac{1}{\\sqrt{2}} \\approx 0.707\\). This illustrates an important principle in circuit design: the resonant frequency is inversely proportional to the square root of either the inductance or capacitance. This relationship allows engineers to tune circuits to specific frequencies by adjusting component values.</p>
                `
            },
            {
                "category": "financial",
                "title": "Economics: Profit Optimization",
                "content": `
                    <p>An economic analyst is studying the profits of a manufacturing company. Based on market research, the company's profit function \\(P(x)\\) (in thousands of dollars) for producing and selling \\(x\\) thousand units is modeled by:</p>
                    <p>\\(P(x) = -2x^2 + 120x - 1600\\)</p>
                    <p>a) Use completing the square to find the production level that maximizes profit and the maximum profit amount.</p>
                    <p>b) Determine the break-even points (where profit is zero) and explain their economic significance using graphical interpretation.</p>
                    <p>c) If the company faces a new constraint that it cannot produce more than 25 thousand units due to capacity limitations, what is the new profit-maximizing strategy?</p>
                `,
                "answer": `
                    <p>a) To find the production level that maximizes profit, we complete the square on the profit function:</p>
                    <p>\\(P(x) = -2x^2 + 120x - 1600\\)</p>
                    
                    <p>Step 1: Factor out the coefficient of \\(x^2\\)</p>
                    <p>\\(P(x) = -2(x^2 - 60x) - 1600\\)</p>
                    
                    <p>Step 2: Complete the square inside the parentheses</p>
                    <p>Half of the coefficient of \\(x\\) is \\(-60/2 = -30\\), and its square is \\((-30)^2 = 900\\)</p>
                    <p>\\(P(x) = -2(x^2 - 60x + 900 - 900) - 1600\\)</p>
                    <p>\\(P(x) = -2(x^2 - 60x + 900) + 2 \\times 900 - 1600\\)</p>
                    <p>\\(P(x) = -2(x - 30)^2 + 1800 - 1600\\)</p>
                    <p>\\(P(x) = -2(x - 30)^2 + 200\\)</p>
                    
                    <p>From this form, we can see that the function has a maximum when \\(x = 30\\) (when the squared term equals zero), and the maximum profit is \\(P(30) = 200\\) thousand dollars, or \\$200,000.</p>
                    
                    <p>b) To find the break-even points, we set \\(P(x) = 0\\) and solve:</p>
                    <p>\\(-2x^2 + 120x - 1600 = 0\\)</p>
                    <p>\\(x^2 - 60x + 800 = 0\\)</p>
                    
                    <p>Using the quadratic formula:</p>
                    <p>\\(x = \\frac{60 \\pm \\sqrt{60^2 - 4 \\times 1 \\times 800}}{2 \\times 1}\\)</p>
                    <p>\\(x = \\frac{60 \\pm \\sqrt{3600 - 3200}}{2}\\)</p>
                    <p>\\(x = \\frac{60 \\pm \\sqrt{400}}{2}\\)</p>
                    <p>\\(x = \\frac{60 \\pm 20}{2}\\)</p>
                    <p>\\(x_1 = \\frac{60 - 20}{2} = 20\\)</p>
                    <p>\\(x_2 = \\frac{60 + 20}{2} = 40\\)</p>
                    
                    <p>The company breaks even (zero profit) when it produces either 20 thousand units or 40 thousand units.</p>
                    
                    <p>Economic interpretation using the graph:</p>
                    <p>- The profit function is a parabola opening downward, with vertex at (30, 200)</p>
                    <p>- Below 20 thousand units, the profit is negative (the company operates at a loss)</p>
                    <p>- Between 20 and 40 thousand units, the profit is positive</p>
                    <p>- Beyond 40 thousand units, the profit becomes negative again (diminishing returns, increased costs of scaling)</p>
                    <p>- The optimal production level (30 thousand units) lies exactly midway between the break-even points</p>
                    
                    <p>c) If the company cannot produce more than 25 thousand units due to capacity limitations, the profit-maximizing strategy changes.</p>
                    
                    <p>Since the unconstrained maximum occurs at \\(x = 30\\) (beyond the new capacity limit), and the profit function is a downward-facing parabola, the new maximum profit will occur at the upper bound of the feasible region, which is \\(x = 25\\) thousand units.</p>
                    
                    <p>The profit at this production level is:</p>
                    <p>\\(P(25) = -2(25)^2 + 120(25) - 1600\\)</p>
                    <p>\\(P(25) = -2(625) + 3000 - 1600\\)</p>
                    <p>\\(P(25) = -1250 + 3000 - 1600\\)</p>
                    <p>\\(P(25) = 150\\) thousand dollars, or \\$150,000</p>
                    
                    <p>This represents a reduction of \\$50,000 in profit due to the capacity constraint, highlighting the opportunity cost of the limitation. The company might consider investing in expanding capacity if the cost of doing so is less than the present value of the additional profit that could be earned.</p>
                `
            },
            {
                "category": "creative",
                "title": "Architecture and Design: Arch Proportions",
                "content": `
                    <p>An architect is designing a parabolic arch for the entrance of a building. The shape of the arch can be described by the quadratic function:</p>
                    <p>\\(y = -0.4x^2 + bx + c\\)</p>
                    <p>where \\(y\\) is the height and \\(x\\) is the horizontal distance from the center, both measured in meters. The arch needs to have the following properties:</p>
                    <ul>
                        <li>The arch should be 10 meters wide at the base (5 meters on either side of the center)</li>
                        <li>The arch should be 8 meters high at its peak</li>
                        <li>The arch should be symmetrical about its center line</li>
                    </ul>
                    <p>a) Use the symmetry condition and the given constraints to determine the values of \\(b\\) and \\(c\\).</p>
                    <p>b) Rewrite the equation using the completed square form, and interpret what this tells you about the arch's dimensions.</p>
                    <p>c) If the architect wants the arch to have a height of exactly 6 meters at a distance of 2 meters from the center, does the current design meet this requirement? If not, what adjustment would be needed?</p>
                `,
                "answer": `
                    <p>a) Let's establish a coordinate system where the origin (0,0) is at the center of the base of the arch, the x-axis runs horizontally, and the y-axis runs vertically up through the center of the arch.</p>
                    
                    <p>For the arch to be symmetrical about the center line (the y-axis), the function must be even, which means that \\(f(-x) = f(x)\\) for all values of \\(x\\). In a quadratic function \\(y = -0.4x^2 + bx + c\\), this is only possible if the coefficient of \\(x\\) (the \\(b\\) term) is zero.</p>
                    <p>Therefore, \\(b = 0\\) and our function simplifies to:</p>
                    <p>\\(y = -0.4x^2 + c\\)</p>
                    
                    <p>Now, we need to determine \\(c\\) using the given constraints:</p>
                    <p>The arch is 10 meters wide at the base, meaning it extends from \\(x = -5\\) to \\(x = 5\\), and at these points, \\(y = 0\\).</p>
                    <p>Using the point \\((5, 0)\\):</p>
                    <p>\\(0 = -0.4(5)^2 + c\\)</p>
                    <p>\\(0 = -0.4 \\times 25 + c\\)</p>
                    <p>\\(0 = -10 + c\\)</p>
                    <p>\\(c = 10\\)</p>
                    
                    <p>Let's verify with the second point \\((-5, 0)\\):</p>
                    <p>\\(0 = -0.4(-5)^2 + 10\\)</p>
                    <p>\\(0 = -0.4 \\times 25 + 10\\)</p>
                    <p>\\(0 = -10 + 10\\)</p>
                    <p>\\(0 = 0\\) ✓</p>
                    
                    <p>Now let's check if the height at the peak is 8 meters as required. The peak occurs at \\(x = 0\\) (the center):</p>
                    <p>\\(y(0) = -0.4(0)^2 + 10 = 10\\) meters</p>
                    
                    <p>This gives us a height of 10 meters, not 8 meters as required. We need to adjust our parameters.</p>
                    
                    <p>Let's reconsider with the constraint that the height at the center is 8 meters:</p>
                    <p>\\(y(0) = -0.4(0)^2 + c = 8\\)</p>
                    <p>\\(c = 8\\)</p>
                    
                    <p>Now let's determine where the arch meets the ground (y = 0):</p>
                    <p>\\(0 = -0.4x^2 + 8\\)</p>
                    <p>\\(-8 = -0.4x^2\\)</p>
                    <p>\\(8 = 0.4x^2\\)</p>
                    <p>\\(20 = x^2\\)</p>
                    <p>\\(x = \\pm\\sqrt{20} \\approx \\pm 4.47\\) meters</p>
                    
                    <p>This would make the width of the arch approximately 8.94 meters, not the 10 meters specified. Let's readjust our approach.</p>
                    
                    <p>Let's keep the 10-meter width requirement and adjust the coefficient of \\(x^2\\):</p>
                    <p>At \\(x = 5\\), \\(y = 0\\):</p>
                    <p>\\(0 = a(5)^2 + c\\)</p>
                    <p>\\(c = -25a\\)</p>
                    
                    <p>At \\(x = 0\\), \\(y = 8\\) (the peak height):</p>
                    <p>\\(8 = a(0)^2 + c\\)</p>
                    <p>\\(8 = c\\)</p>
                    <p>\\(8 = -25a\\)</p>
                    <p>\\(a = -\\frac{8}{25} = -0.32\\)</p>
                    
                    <p>Therefore, the equation of the arch is:</p>
                    <p>\\(y = -0.32x^2 + 8\\)</p>
                    
                    <p>b) The equation \\(y = -0.32x^2 + 8\\) is already in a form similar to completed square form since there is no \\(x\\) term. We can rewrite it as:</p>
                    <p>\\(y = -0.32(x - 0)^2 + 8\\)</p>
                    
                    <p>This tells us that:</p>
                    <p>- The axis of symmetry of the parabola is at \\(x = 0\\)</p>
                    <p>- The vertex of the parabola is at (0, 8)</p>
                    <p>- The parabola opens downward (because the coefficient of \\(x^2\\) is negative)</p>
                    <p>- The maximum height of the arch is 8 meters, occurring at the center</p>
                    <p>- The width of the arch at any height \\(h\\) can be determined by solving: \\(h = -0.32x^2 + 8\\) for \\(x\\)</p>
                    
                    <p>c) To check if the current design has a height of 6 meters at 2 meters from the center, we evaluate:</p>
                    <p>\\(y(2) = -0.32(2)^2 + 8\\)</p>
                    <p>\\(y(2) = -0.32 \\times 4 + 8\\)</p>
                    <p>\\(y(2) = -1.28 + 8\\)</p>
                    <p>\\(y(2) = 6.72\\) meters</p>
                    
                    <p>The current design does not meet the requirement exactly. At 2 meters from the center, the height is 6.72 meters, not 6 meters as required.</p>
                    
                    <p>To adjust the design to meet this additional constraint, we would need to solve a system of equations with three conditions:</p>
                    <p>1. \\(y(0) = 8\\) (height at center is 8 meters)</p>
                    <p>2. \\(y(5) = 0\\) (width at base is 10 meters)</p>
                    <p>3. \\(y(2) = 6\\) (height at 2 meters from center is 6 meters)</p>
                    
                    <p>This would require a more general form of the quadratic function, possibly \\(y = ax^2 + bx + c\\), which would not preserve symmetry. Therefore, the architect would need to decide which constraints are most important and potentially compromise on some of them.</p>
                    
                    <p>Alternatively, the architect could consider using a different mathematical curve that can satisfy all three constraints, such as a higher-degree polynomial or a piecewise function.</p>
                `
            }
        ]
    };
    
    MathQuestionModule.render(graphicalContent, 'graphical-identity-container');
});
</script>

### Key Takeaways

```{important}
1. The graph of a quadratic equation is a parabola
2. The zeros or roots of the quadratic equation are the x-intercepts of the parabola
3. The vertex of the parabola represents the minimum (if $a > 0$) or maximum (if $a < 0$) value
4. The completed square form $a(x + p)^2 + q$ directly reveals the vertex at $(-p, q)$ 
5. A parabola can have two distinct real roots, one repeated real root, or no real roots, depending on whether it crosses, touches, or misses the x-axis
```

## Deriving the Quadratic Formula

### Theory

The quadratic formula gives us a direct way to solve any quadratic equation. While it may seem like a formula to memorize, understanding its derivation builds deeper insight into quadratic equations.

We're aiming to derive the formula:

$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$

Starting from the standard form:

$$ax^2 + bx + c = 0$$

The first step is to divide by $a$ to neaten things up:

$$x^2 + \frac{b}{a}x + \frac{c}{a} = 0$$

Next, we put it into completed square form by adding and subtracting the same term:

$$x^2 + \frac{b}{a}x + \frac{b^2}{4a^2} - \frac{b^2}{4a^2} + \frac{c}{a} = 0$$

This gives us:

$$\left(x + \frac{b}{2a}\right)^2 = \frac{b^2}{4a^2} - \frac{c}{a}$$

Simplifying the right side:

$$\left(x + \frac{b}{2a}\right)^2 = \frac{b^2 - 4ac}{4a^2}$$

Taking the square root of both sides:

$$x + \frac{b}{2a} = \pm\frac{\sqrt{b^2 - 4ac}}{2a}$$

Solving for $x$:

$$x = -\frac{b}{2a} \pm\frac{\sqrt{b^2 - 4ac}}{2a} = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$

And there we have the quadratic formula!

```{tip}
When using the quadratic formula:
1. Always check that your equation is in standard form $ax^2 + bx + c = 0$
2. Identify the values of $a$, $b$, and $c$ correctly
3. Be careful with negative signs, especially in $b$
4. Always verify your solutions by substituting back into the original equation
```

#### Interactive Visualization: Quadratic Formula

<div id="quadratic-formula-container" class="visualization-container" style="height: 500px;"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    MathVisualizer.createGraphFromDescription('quadratic-formula-container', {
        boundingBox: [-5, 5, 5, -5],
        theme: 'light',
        useSequentialColors: true,
        
        infoBox: {
            title: "Quadratic Formula",
            lines: [
                {text: "Equation: ax² + bx + c = 0", dynamic: false},
                {text: "a: ${a}", dynamic: true},
                {text: "b: ${b}", dynamic: true},
                {text: "c: ${c}", dynamic: true},
                {text: "Discriminant: ${b*b - 4*a*c}", dynamic: true},
                {text: "Roots: ${(-b+Math.sqrt(b*b-4*a*c))/(2*a)} and ${(-b-Math.sqrt(b*b-4*a*c))/(2*a)}", dynamic: true}
            ],
            position: {top: 55, left: 20}
        },
        
        parametrizedFunctions: [
            {
                expression: 'a*x^2 + b*x + c',
                title: 'Quadratic Formula Explorer',
                parameters: {
                    a: { min: -2, max: 2, value: 1, step: 0.1 },
                    b: { min: -5, max: 5, value: -2, step: 0.1 },
                    c: { min: -5, max: 5, value: -3, step: 0.1 }
                },
                features: ['zeros', 'extrema']
            }
        ]
    });
});
</script>

### Application
#### Examples: Using the Quadratic Formula

##### Example 1: A Basic Application

Solve $2x^2 + 5x - 3 = 0$

We identify $a = 2$, $b = 5$, and $c = -3$. Using the quadratic formula:

$$x = \frac{-5 \pm \sqrt{5^2 - 4(2)(-3)}}{2(2)}$$

$$x = \frac{-5 \pm \sqrt{25 + 24}}{4}$$

$$x = \frac{-5 \pm \sqrt{49}}{4}$$

$$x = \frac{-5 \pm 7}{4}$$

$$x = \frac{-5 + 7}{4} = \frac{2}{4} = \frac{1}{2} \quad \text{or} \quad x = \frac{-5 - 7}{4} = \frac{-12}{4} = -3$$

So the solutions are $x = \frac{1}{2}$ and $x = -3$.

Verification:
- $2(\frac{1}{2})^2 + 5(\frac{1}{2}) - 3 = 2(\frac{1}{4}) + \frac{5}{2} - 3 = \frac{1}{2} + \frac{5}{2} - 3 = 0$ ✓
- $2(-3)^2 + 5(-3) - 3 = 2(9) - 15 - 3 = 18 - 15 - 3 = 0$ ✓

##### Example 2: When the Discriminant is Zero

Solve $4x^2 - 12x + 9 = 0$

We identify $a = 4$, $b = -12$, and $c = 9$. Using the quadratic formula:

$$x = \frac{12 \pm \sqrt{(-12)^2 - 4(4)(9)}}{2(4)}$$

$$x = \frac{12 \pm \sqrt{144 - 144}}{8}$$

$$x = \frac{12 \pm 0}{8} = \frac{12}{8} = \frac{3}{2}$$

There is only one solution: $x = \frac{3}{2}$, which is a repeated root.

This means the parabola touches the x-axis at exactly one point, $x = \frac{3}{2}$.

##### Example 3: When the Discriminant is Negative

Solve $x^2 + x + 1 = 0$

We identify $a = 1$, $b = 1$, and $c = 1$. Using the quadratic formula:

$$x = \frac{-1 \pm \sqrt{1^2 - 4(1)(1)}}{2(1)}$$

$$x = \frac{-1 \pm \sqrt{1 - 4}}{2}$$

$$x = \frac{-1 \pm \sqrt{-3}}{2}$$

Since $\sqrt{-3}$ is not a real number, this equation has no real solutions. The solutions are:

$$x = \frac{-1 + i\sqrt{3}}{2} \quad \text{or} \quad x = \frac{-1 - i\sqrt{3}}{2}$$

These are complex numbers, and the graph of $y = x^2 + x + 1$ never crosses the x-axis.

```{warning}
When the discriminant $b^2 - 4ac$ is negative, the quadratic equation has no real solutions. In such cases, the solutions are complex numbers and the graph of the corresponding quadratic function does not intersect the x-axis.
```

#### Multiple Choice Questions

<div id="quadratic-formula-mcq" class="quiz-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Quadratic Formula Quiz",
        questions: [
            {
                text: "Using the quadratic formula, the solutions to \\(2x^2 - 5x - 3 = 0\\) are:",
                options: [
                    "\\(x = \\frac{5 \\pm \\sqrt{25 + 24}}{4}\\)",
                    "\\(x = \\frac{5 \\pm \\sqrt{49}}{4}\\)",
                    "\\(x = \\frac{5 \\pm \\sqrt{25 + 24}}{2}\\)",
                    "\\(x = \\frac{5 \\pm 7}{4}\\)"
                ],
                correctIndex: 3,
                explanation: "Using the quadratic formula with \\(a = 2\\), \\(b = -5\\), and \\(c = -3\\): \\(x = \\frac{-(-5) \\pm \\sqrt{(-5)^2 - 4(2)(-3)}}{2(2)} = \\frac{5 \\pm \\sqrt{25 + 24}}{4} = \\frac{5 \\pm \\sqrt{49}}{4} = \\frac{5 \\pm 7}{4}\\).",
                difficulty: "Intermediate"
            },
            {
                text: "The quadratic equation \\(3x^2 + 6x + 4 = 0\\) has:",
                options: [
                    "Two distinct real roots",
                    "One repeated real root",
                    "No real roots (two complex conjugate roots)",
                    "Exactly one real root and one complex root"
                ],
                correctIndex: 2,
                explanation: "To determine the nature of the roots, we compute the discriminant: \\(b^2 - 4ac = 6^2 - 4(3)(4) = 36 - 48 = -12\\). Since the discriminant is negative, the equation has no real roots, but rather two complex conjugate roots.",
                difficulty: "Basic"
            },
            {
                text: "For which value of \\(k\\) will the equation \\(x^2 + kx + 16 = 0\\) have exactly one solution?",
                options: [
                    "\\(k = 8\\)",
                    "\\(k = -8\\)",
                    "\\(k = 16\\)",
                    "\\(k = -16\\)"
                ],
                correctIndex: 0,
                explanation: "For the equation to have exactly one solution, the discriminant must equal zero: \\(b^2 - 4ac = 0\\). With \\(a = 1\\), \\(b = k\\), and \\(c = 16\\): \\(k^2 - 4(1)(16) = 0\\) \\(\\Rightarrow k^2 - 64 = 0\\) \\(\\Rightarrow k^2 = 64\\) \\(\\Rightarrow k = \\pm 8\\). Since both values would give a repeated root, we need to check each. With \\(k = 8\\), the equation becomes \\(x^2 + 8x + 16 = 0\\), which can be factored as \\((x + 4)^2 = 0\\), giving the repeated root \\(x = -4\\). With \\(k = -8\\), the equation becomes \\(x^2 - 8x + 16 = 0\\), which can be factored as \\((x - 4)^2 = 0\\), giving the repeated root \\(x = 4\\). Both values of \\(k\\) would work, but only \\(k = 8\\) is listed among the options.",
                difficulty: "Advanced"
            },
            {
                text: "If one root of the quadratic equation \\(x^2 + px + q = 0\\) is 3, and the sum of the roots is -5, what is the value of \\(p\\)?",
                options: [
                    "\\(p = 2\\)",
                    "\\(p = 5\\)",
                    "\\(p = -2\\)",
                    "\\(p = -5\\)"
                ],
                correctIndex: 1,
                explanation: "If one root is 3, and the sum of the roots is -5, then the other root must be -5 - 3 = -8. For a quadratic equation in the form \\(ax^2 + bx + c = 0\\), the sum of the roots is \\(-\\frac{b}{a}\\) and the product of the roots is \\(\\frac{c}{a}\\). In our case, with \\(a = 1\\), the sum of the roots is \\(-p\\). Therefore, \\(-p = -5\\) \\(\\Rightarrow p = 5\\).",
                difficulty: "Intermediate"
            }
        ]
    };
    
    MCQQuiz.create('quadratic-formula-mcq', quizData);
});
</script>

#### Identity Questions: Quadratic Formula Applications

<div id="quadratic-formula-identity-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quadraticFormulaContent = {
        "title": "Quadratic Formula: Applications",
        "intro_content": `
            <p>The quadratic formula \\(x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}\\) provides a direct method for finding the solutions to any quadratic equation in the form \\(ax^2 + bx + c = 0\\). This powerful formula has applications across numerous fields of study and real-world scenarios.</p>
            <p>Understanding when and how to apply the quadratic formula allows us to solve problems that might be difficult or impossible to approach using factorization alone.</p>
        `,
        "questions": [
            {
                "category": "scientific",
                "title": "Astronomy: Orbital Mechanics",
                "content": `
                    <p>An astrophysicist is studying the trajectory of a comet passing through our solar system. The comet's distance \\(d\\) (in astronomical units, AU) from the Sun at time \\(t\\) (in Earth years since perihelion passage) can be approximated by:</p>
                    <p>\\(d = 0.8t^2 - 0.4t + 0.6\\)</p>
                    <p>a) At what times will the comet be exactly 1 AU from the Sun (the same as Earth's average distance)?</p>
                    <p>b) What is the minimum distance of the comet from the Sun, and when does it occur?</p>
                    <p>c) If instruments can only effectively observe the comet when it's between 0.5 AU and 1.5 AU from the Sun, during what time intervals will observation be possible?</p>
                `,
                "answer": `
                    <p>a) To find when the comet is exactly 1 AU from the Sun, we set \\(d = 1\\) and solve:</p>
                    <p>\\(1 = 0.8t^2 - 0.4t + 0.6\\)</p>
                    <p>\\(0 = 0.8t^2 - 0.4t + 0.6 - 1\\)</p>
                    <p>\\(0 = 0.8t^2 - 0.4t - 0.4\\)</p>
                    
                    <p>Using the quadratic formula with \\(a = 0.8\\), \\(b = -0.4\\), and \\(c = -0.4\\):</p>
                    <p>\\(t = \\frac{0.4 \\pm \\sqrt{(-0.4)^2 - 4(0.8)(-0.4)}}{2(0.8)}\\)</p>
                    <p>\\(t = \\frac{0.4 \\pm \\sqrt{0.16 + 1.28}}{1.6}\\)</p>
                    <p>\\(t = \\frac{0.4 \\pm \\sqrt{1.44}}{1.6}\\)</p>
                    <p>\\(t = \\frac{0.4 \\pm 1.2}{1.6}\\)</p>
                    <p>\\(t_1 = \\frac{0.4 - 1.2}{1.6} = \\frac{-0.8}{1.6} = -0.5\\) years</p>
                    <p>\\(t_2 = \\frac{0.4 + 1.2}{1.6} = \\frac{1.6}{1.6} = 1\\) year</p>
                    
                    <p>Therefore, the comet will be exactly 1 AU from the Sun at \\(t = -0.5\\) years (0.5 years before perihelion) and \\(t = 1\\) year (1 year after perihelion).</p>
                    
                    <p>b) To find the minimum distance, we need to find the vertex of the parabola. For a quadratic function \\(f(t) = at^2 + bt + c\\), the t-coordinate of the vertex is \\(t = -\\frac{b}{2a}\\).</p>
                    <p>\\(t_{min} = -\\frac{-0.4}{2(0.8)} = \\frac{0.4}{1.6} = 0.25\\) years</p>
                    
                    <p>The minimum distance occurs at \\(t = 0.25\\) years and equals:</p>
                    <p>\\(d_{min} = 0.8(0.25)^2 - 0.4(0.25) + 0.6\\)</p>
                    <p>\\(d_{min} = 0.8(0.0625) - 0.1 + 0.6\\)</p>
                    <p>\\(d_{min} = 0.05 - 0.1 + 0.6 = 0.55\\) AU</p>
                    
                    <p>Therefore, the minimum distance of the comet from the Sun is 0.55 AU, occurring 0.25 years after perihelion passage.</p>
                    
                    <p>c) To find when the comet is between 0.5 AU and 1.5 AU, we need to solve two inequalities:</p>
                    
                    <p>For \\(d \\geq 0.5\\):</p>
                    <p>\\(0.8t^2 - 0.4t + 0.6 \\geq 0.5\\)</p>
                    <p>\\(0.8t^2 - 0.4t + 0.1 \\geq 0\\)</p>
                    
                    <p>The discriminant is \\(b^2 - 4ac = (-0.4)^2 - 4(0.8)(0.1) = 0.16 - 0.32 = -0.16 < 0\\)</p>
                    <p>Since the discriminant is negative and the leading coefficient is positive, the parabola never crosses below 0.5 AU. Therefore, the distance is always greater than or equal to 0.5 AU.</p>
                    
                    <p>For \\(d \\leq 1.5\\):</p>
                    <p>\\(0.8t^2 - 0.4t + 0.6 \\leq 1.5\\)</p>
                    <p>\\(0.8t^2 - 0.4t - 0.9 \\leq 0\\)</p>
                    
                    <p>Using the quadratic formula with \\(a = 0.8\\), \\(b = -0.4\\), and \\(c = -0.9\\):</p>
                    <p>\\(t = \\frac{0.4 \\pm \\sqrt{0.16 + 2.88}}{1.6} = \\frac{0.4 \\pm \\sqrt{3.04}}{1.6} = \\frac{0.4 \\pm 1.74}{1.6}\\)</p>
                    <p>\\(t_1 = \\frac{0.4 - 1.74}{1.6} \\approx -0.84\\) years</p>
                    <p>\\(t_2 = \\frac{0.4 + 1.74}{1.6} \\approx 1.34\\) years</p>
                    
                    <p>Therefore, the comet can be effectively observed when \\(-0.84 \\leq t \\leq 1.34\\), or from approximately 0.84 years before perihelion to 1.34 years after perihelion.</p>
                `
            },
            {
                "category": "engineering",
                "title": "Mechanical Engineering: Motion Analysis",
                "content": `
                    <p>A mechanical engineer is designing a pneumatic system where a piston moves according to the equation:</p>
                    <p>\\(x(t) = 2t^2 - 18t + 40\\)</p>
                    <p>where \\(x\\) is the position in centimeters from a reference point and \\(t\\) is the time in seconds.</p>
                    <p>a) At what times does the piston pass through the reference point (\\(x = 0\\))?</p>
                    <p>b) The piston is contained within a cylinder that has a length of 50 cm. If the reference point is at the end of the cylinder, will the piston ever hit the other end of the cylinder? If so, when?</p>
                    <p>c) What is the minimum position of the piston, and at what time does it reach this position?</p>
                `,
                "answer": `
                    <p>a) To find when the piston passes through the reference point, we set \\(x(t) = 0\\) and solve:</p>
                    <p>\\(0 = 2t^2 - 18t + 40\\)</p>
                    
                    <p>Using the quadratic formula with \\(a = 2\\), \\(b = -18\\), and \\(c = 40\\):</p>
                    <p>\\(t = \\frac{18 \\pm \\sqrt{(-18)^2 - 4(2)(40)}}{2(2)}\\)</p>
                    <p>\\(t = \\frac{18 \\pm \\sqrt{324 - 320}}{4}\\)</p>
                    <p>\\(t = \\frac{18 \\pm \\sqrt{4}}{4}\\)</p>
                    <p>\\(t = \\frac{18 \\pm 2}{4}\\)</p>
                    <p>\\(t_1 = \\frac{18 - 2}{4} = \\frac{16}{4} = 4\\) seconds</p>
                    <p>\\(t_2 = \\frac{18 + 2}{4} = \\frac{20}{4} = 5\\) seconds</p>
                    
                    <p>Therefore, the piston passes through the reference point (\\(x = 0\\)) at \\(t = 4\\) seconds and \\(t = 5\\) seconds.</p>
                    
                    <p>b) To determine if the piston will hit the other end of the cylinder, we need to find when \\(x(t) = 50\\):</p>
                    <p>\\(50 = 2t^2 - 18t + 40\\)</p>
                    <p>\\(0 = 2t^2 - 18t + 40 - 50\\)</p>
                    <p>\\(0 = 2t^2 - 18t - 10\\)</p>
                    
                    <p>Using the quadratic formula with \\(a = 2\\), \\(b = -18\\), and \\(c = -10\\):</p>
                    <p>\\(t = \\frac{18 \\pm \\sqrt{(-18)^2 - 4(2)(-10)}}{2(2)}\\)</p>
                    <p>\\(t = \\frac{18 \\pm \\sqrt{324 + 80}}{4}\\)</p>
                    <p>\\(t = \\frac{18 \\pm \\sqrt{404}}{4}\\)</p>
                    <p>\\(t = \\frac{18 \\pm 20.1}{4}\\)</p>
                    <p>\\(t_1 \\approx \\frac{18 - 20.1}{4} \\approx -0.53\\) seconds</p>
                    <p>\\(t_2 \\approx \\frac{18 + 20.1}{4} \\approx 9.53\\) seconds</p>
                    
                    <p>Since \\(t_1\\) is negative and we assume the motion starts at \\(t = 0\\), we only consider the solution \\(t_2 \\approx 9.53\\) seconds. Therefore, the piston will hit the other end of the cylinder at approximately 9.53 seconds after the start of motion.</p>
                    
                    <p>c) To find the minimum position, we find the vertex of the parabola. For a quadratic function \\(x(t) = at^2 + bt + c\\), the t-coordinate of the vertex is \\(t = -\\frac{b}{2a}\\).</p>
                    <p>\\(t_{min} = -\\frac{-18}{2(2)} = \\frac{18}{4} = 4.5\\) seconds</p>
                    
                    <p>The minimum position occurs at \\(t = 4.5\\) seconds and equals:</p>
                    <p>\\(x_{min} = 2(4.5)^2 - 18(4.5) + 40\\)</p>
                    <p>\\(x_{min} = 2(20.25) - 81 + 40\\)</p>
                    <p>\\(x_{min} = 40.5 - 81 + 40 = -0.5\\) cm</p>
                    
                    <p>Therefore, the minimum position of the piston is -0.5 cm (which means it extends 0.5 cm beyond the reference point in the negative direction), occurring at 4.5 seconds after the start of motion.</p>
                `
            },
            {
                "category": "financial",
                "title": "Business: Revenue Forecasting",
                "content": `
                    <p>A marketing analyst at a retail company has modeled the quarterly revenue \\(R\\) (in millions of dollars) as a function of advertising spending \\(x\\) (in hundreds of thousands of dollars):</p>
                    <p>\\(R(x) = -0.2x^2 + 3x + 10\\)</p>
                    <p>a) Using the quadratic formula, determine the advertising budgets that would result in a quarterly revenue of \\$15 million.</p>
                    <p>b) What is the maximum possible revenue according to this model, and what advertising budget achieves it?</p>
                    <p>c) The company has set a target revenue of \\$20 million for the next quarter. Is this achievable according to the model? Explain your answer using the quadratic formula.</p>
                `,
                "answer": `
                    <p>a) To find the advertising budgets that would result in a revenue of \\$15 million, we set \\(R(x) = 15\\) and solve:</p>
                    <p>\\(15 = -0.2x^2 + 3x + 10\\)</p>
                    <p>\\(0 = -0.2x^2 + 3x + 10 - 15\\)</p>
                    <p>\\(0 = -0.2x^2 + 3x - 5\\)</p>
                    
                    <p>Using the quadratic formula with \\(a = -0.2\\), \\(b = 3\\), and \\(c = -5\\):</p>
                    <p>\\(x = \\frac{-3 \\pm \\sqrt{3^2 - 4(-0.2)(-5)}}{2(-0.2)}\\)</p>
                    <p>\\(x = \\frac{-3 \\pm \\sqrt{9 - 4}}{-0.4}\\)</p>
                    <p>\\(x = \\frac{-3 \\pm \\sqrt{5}}{-0.4}\\)</p>
                    <p>\\(x_1 \\approx \\frac{-3 - 2.24}{-0.4} \\approx \\frac{5.24}{0.4} \\approx 13.1\\)</p>
                    <p>\\(x_2 \\approx \\frac{-3 + 2.24}{-0.4} \\approx \\frac{-0.76}{-0.4} \\approx 1.9\\)</p>
                    
                    <p>Therefore, the company can achieve a quarterly revenue of \\$15 million with advertising budgets of either approximately \\$190,000 (\\(x = 1.9\\)) or approximately \\$1,310,000 (\\(x = 13.1\\)).</p>
                    
                    <p>b) To find the maximum possible revenue, we find the vertex of the parabola. For a quadratic function \\(R(x) = ax^2 + bx + c\\), the x-coordinate of the vertex is \\(x = -\\frac{b}{2a}\\).</p>
                    <p>\\(x_{max} = -\\frac{3}{2(-0.2)} = \\frac{3}{0.4} = 7.5\\)</p>
                    
                    <p>The maximum revenue occurs at \\(x = 7.5\\) and equals:</p>
                    <p>\\(R_{max} = -0.2(7.5)^2 + 3(7.5) + 10\\)</p>
                    <p>\\(R_{max} = -0.2(56.25) + 22.5 + 10\\)</p>
                    <p>\\(R_{max} = -11.25 + 22.5 + 10 = 21.25\\) million dollars</p>
                    
                    <p>Therefore, the maximum possible revenue according to this model is \\$21.25 million, achieved with an advertising budget of \\$750,000 (\\(x = 7.5\\)).</p>
                    
                    <p>c) The target revenue of \\$20 million can be achieved if there exists a real solution to the equation:</p>
                    <p>\\(20 = -0.2x^2 + 3x + 10\\)</p>
                    <p>\\(0 = -0.2x^2 + 3x + 10 - 20\\)</p>
                    <p>\\(0 = -0.2x^2 + 3x - 10\\)</p>
                    
                    <p>Using the quadratic formula with \\(a = -0.2\\), \\(b = 3\\), and \\(c = -10\\):</p>
                    <p>\\(x = \\frac{-3 \\pm \\sqrt{3^2 - 4(-0.2)(-10)}}{2(-0.2)}\\)</p>
                    <p>\\(x = \\frac{-3 \\pm \\sqrt{9 - 8}}{-0.4}\\)</p>
                    <p>\\(x = \\frac{-3 \\pm \\sqrt{1}}{-0.4}\\)</p>
                    <p>\\(x = \\frac{-3 \\pm 1}{-0.4}\\)</p>
                    <p>\\(x_1 = \\frac{-3 - 1}{-0.4} = \\frac{4}{0.4} = 10\\)</p>
                    <p>\\(x_2 = \\frac{-3 + 1}{-0.4} = \\frac{-2}{-0.4} = 5\\)</p>
                    
                    <p>Yes, the target revenue of \\$20 million is achievable according to the model. The company can achieve this by setting the advertising budget to either \\$500,000 (\\(x = 5\\)) or \\$1,000,000 (\\(x = 10\\)).</p>
                    
                    <p>From a business perspective, the company would likely choose the lower advertising budget (\\$500,000) to achieve the target revenue, as it would result in higher net profit. However, other factors such as market penetration goals or long-term brand building might influence the decision.</p>
                `
            },
            {
                "category": "creative",
                "title": "Photography: Depth of Field Calculation",
                "content": `
                    <p>A photographer is working with a camera that uses the following quadratic equation to model the range of distance (in meters) that will appear in acceptable focus:</p>
                    <p>\\(d^2 - 12d + 20 = 0\\)</p>
                    <p>where \\(d\\) represents the distance from the camera.</p>
                    <p>a) Use the quadratic formula to find the near and far limits of the depth of field.</p>
                    <p>b) The photographer needs to photograph a scene that extends from 2 meters to 8 meters from the camera. Will the current lens setting capture the entire scene in focus? Explain your answer.</p>
                    <p>c) If the photographer adjusts the aperture to obtain a new depth of field equation: \\(d^2 - 14d + 24 = 0\\), how does this change the range of focus, and would it be better for the scene described in part (b)?</p>
                `,
                "answer": `
                    <p>a) To find the near and far limits of the depth of field, we solve the equation \\(d^2 - 12d + 20 = 0\\) using the quadratic formula:</p>
                    <p>\\(d = \\frac{12 \\pm \\sqrt{12^2 - 4 \\times 1 \\times 20}}{2 \\times 1}\\)</p>
                    <p>\\(d = \\frac{12 \\pm \\sqrt{144 - 80}}{2}\\)</p>
                    <p>\\(d = \\frac{12 \\pm \\sqrt{64}}{2}\\)</p>
                    <p>\\(d = \\frac{12 \\pm 8}{2}\\)</p>
                    <p>\\(d_{near} = \\frac{12 - 8}{2} = 2\\) meters</p>
                    <p>\\(d_{far} = \\frac{12 + 8}{2} = 10\\) meters</p>
                    
                    <p>Therefore, the depth of field extends from 2 meters to 10 meters from the camera.</p>
                    
                    <p>b) The scene extends from 2 meters to 8 meters from the camera, and our calculated depth of field extends from 2 meters to 10 meters. Since \\(2 \\leq 2\\) and \\(8 \\leq 10\\), the current lens setting will capture the entire scene in focus.</p>
                    
                    <p>The near limit of the depth of field coincides exactly with the nearest part of the scene (2 meters), which means objects at precisely 2 meters will be just barely in acceptable focus. The photographer might want to adjust the settings slightly to ensure a safety margin, especially if any subjects might move slightly closer than 2 meters.</p>
                    
                    <p>c) For the new depth of field equation \\(d^2 - 14d + 24 = 0\\), we again use the quadratic formula:</p>
                    <p>\\(d = \\frac{14 \\pm \\sqrt{14^2 - 4 \\times 1 \\times 24}}{2 \\times 1}\\)</p>
                    <p>\\(d = \\frac{14 \\pm \\sqrt{196 - 96}}{2}\\)</p>
                    <p>\\(d = \\frac{14 \\pm \\sqrt{100}}{2}\\)</p>
                    <p>\\(d = \\frac{14 \\pm 10}{2}\\)</p>
                    <p>\\(d_{near} = \\frac{14 - 10}{2} = 2\\) meters</p>
                    <p>\\(d_{far} = \\frac{14 + 10}{2} = 12\\) meters</p>
                    
                    <p>The new depth of field extends from 2 meters to 12 meters from the camera.</p>
                    
                    <p>Comparing the two settings:</p>
                    <p>- Original setting: Depth of field from 2 to 10 meters</p>
                    <p>- New setting: Depth of field from 2 to 12 meters</p>
                    
                    <p>The new setting provides a greater depth of field, extending the far limit from 10 meters to 12 meters while maintaining the same near limit of 2 meters. For the scene that extends from 2 to 8 meters, both settings would capture the entire scene in focus.</p>
                    
                    <p>However, the new setting might be slightly better as it provides more "buffer" on the far end, which could be useful if any elements of the scene are positioned slightly beyond 8 meters. Additionally, if the photographer wants to include more of the background in focus for compositional reasons, the extended far limit would be beneficial.</p>
                    
                    <p>In photography terms, the new setting likely represents a smaller aperture (higher f-number), which increases depth of field but may require longer exposure times or higher ISO settings to maintain proper exposure.</p>
                `
            }
        ]
    };
    
    MathQuestionModule.render(quadraticFormulaContent, 'quadratic-formula-identity-container');
});
</script>

### Key Takeaways

```{important}
1. The quadratic formula $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$ gives us a direct way to find solutions for any quadratic equation
2. It works for all quadratic equations, even those that cannot be easily factorized
3. The formula is derived by completing the square on the general form $ax^2 + bx + c = 0$
4. The expression under the square root ($b^2 - 4ac$) is called the discriminant and determines the nature of the solutions
5. When using the formula, always pay attention to signs and ensure your equation is in standard form
```

## The Discriminant: Understanding the Nature of Quadratic Solutions

### Theory
#### What is the Discriminant?

For any quadratic equation in standard form $ax^2 + bx + c = 0$, the discriminant (denoted by $\Delta$) is defined as:

$$\Delta = b^2 - 4ac$$

This expression appears under the square root in the quadratic formula:

$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a} = \frac{-b \pm \sqrt{\Delta}}{2a}$$

```{tip}
The discriminant acts as a "solution predictor" - you can determine the number and type of solutions by evaluating this single expression, without actually solving the equation!
```

#### The Three Scenarios

The value of the discriminant determines both the number and type of solutions:

##### Case 1: Positive Discriminant ($\Delta > 0$)
- **Algebraically**: The equation has two distinct real solutions
- **Graphically**: The parabola crosses the x-axis at two different points
- **Example**: For $x^2 - 5x + 6 = 0$:
  - $\Delta = (-5)^2 - 4(1)(6) = 25 - 24 = 1 > 0$
  - Solutions are $x = 2$ and $x = 3$ (two distinct real roots)
  - The parabola crosses the x-axis at $x = 2$ and $x = 3$

##### Case 2: Zero Discriminant ($\Delta = 0$)
- **Algebraically**: The equation has exactly one repeated real solution
- **Graphically**: The parabola touches the x-axis exactly once at its vertex
- **Example**: For $x^2 - 6x + 9 = 0$:
  - $\Delta = (-6)^2 - 4(1)(9) = 36 - 36 = 0$
  - The only solution is $x = 3$ (repeated twice)
  - The parabola's vertex is at $(3,0)$, just touching the x-axis

##### Case 3: Negative Discriminant ($\Delta < 0$)
- **Algebraically**: The equation has two complex solutions (not real numbers)
- **Graphically**: The parabola never intersects the x-axis
- **Example**: For $x^2 + 1 = 0$:
  - $\Delta = 0^2 - 4(1)(1) = -4 < 0$
  - Solutions are $x = \pm i$ (complex numbers)
  - The parabola sits entirely above the x-axis with vertex at $(0,1)$

#### The Discriminant and Factorization

The discriminant also tells us about factorization possibilities:

- When $\Delta > 0$: The quadratic can be factored into two different linear factors with real coefficients
- When $\Delta = 0$: The quadratic can be factored as a perfect square: $(x - r)^2$
- When $\Delta < 0$: The quadratic cannot be factored with real coefficients

```{warning}
Be careful with your signs when computing the discriminant. A common mistake is to forget the negative sign when $a$ or $c$ is negative.
```

#### Interactive Visualization: The Discriminant

<div id="discriminant-container" class="visualization-container" style="height: 500px;"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    MathVisualizer.createGraphFromDescription('discriminant-container', {
        boundingBox: [-5, 5, 5, -5],
        theme: 'light',
        useSequentialColors: true,
        
        infoBox: {
            title: "The Discriminant",
            lines: [
                {text: "Equation: ax² + bx + c = 0", dynamic: false},
                {text: "a: ${a}", dynamic: true},
                {text: "b: ${b}", dynamic: true},
                {text: "c: ${c}", dynamic: true},
                {text: "Discriminant: ${b*b - 4*a*c}", dynamic: true},
                {text: "Nature of roots:", dynamic: false},
                {text: "${b*b - 4*a*c > 0 ? 'Two distinct real roots' : (b*b - 4*a*c == 0 ? 'One repeated real root' : 'Two complex roots')}", dynamic: true}
            ],
            position: {top: 55, left: 20}
        },
        
        parametrizedFunctions: [
            {
                expression: 'a*x^2 + b*x + c',
                title: 'Discriminant Explorer',
                parameters: {
                    a: { min: -2, max: 2, value: 1, step: 0.1 },
                    b: { min: -5, max: 5, value: 0, step: 0.1 },
                    c: { min: -5, max: 5, value: 1, step: 0.1 }
                },
                features: ['zeros']
            }
        ]
    });
});
</script>

### Application
#### Examples: Using the Discriminant

##### Example 1: Analyzing an Equation

For the equation $2x^2 - 5x + 3 = 0$, calculate the discriminant and determine the nature of its solutions.

We identify $a = 2$, $b = -5$, and $c = 3$.

$$\Delta = b^2 - 4ac = (-5)^2 - 4(2)(3) = 25 - 24 = 1$$

Since $\Delta > 0$, the equation has two distinct real solutions. We could find these using the quadratic formula:

$$x = \frac{5 \pm \sqrt{1}}{2(2)} = \frac{5 \pm 1}{4}$$

So $x = \frac{6}{4} = \frac{3}{2}$ or $x = \frac{4}{4} = 1$.

##### Example 2: Finding a Condition for a Single Root

For what value of $k$ will the equation $x^2 + kx + 4 = 0$ have exactly one real solution?

For the equation to have exactly one real solution, its discriminant must equal zero.

$$\Delta = k^2 - 4(1)(4) = 0$$
$$k^2 - 16 = 0$$
$$k^2 = 16$$
$$k = \pm 4$$

So $k = 4$ or $k = -4$ will give the equation exactly one real solution.

##### Example 3: No Real Solutions

Is it possible for the equation $2x^2 + kx + 3 = 0$ to have no real solutions? If so, for what range of values of $k$?

For the equation to have no real solutions, its discriminant must be negative.

$$\Delta = k^2 - 4(2)(3) < 0$$
$$k^2 - 24 < 0$$
$$k^2 < 24$$
$$-\sqrt{24} < k < \sqrt{24}$$
$$-4.9 < k < 4.9$$

So the equation will have no real solutions when $k$ is between approximately $-4.9$ and $4.9$.

#### Multiple Choice Questions

<div id="discriminant-mcq" class="quiz-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Discriminant Quiz",
        questions: [
            {
                text: "For the quadratic equation \\(3x^2 - 5x + 1 = 0\\), the discriminant is:",
                options: [
                    "\\(\\Delta = 25\\)",
                    "\\(\\Delta = 13\\)",
                    "\\(\\Delta = 37\\)",
                    "\\(\\Delta = 17\\)"
                ],
                correctIndex: 1,
                explanation: "The discriminant is calculated using the formula \\(\\Delta = b^2 - 4ac\\). For the equation \\(3x^2 - 5x + 1 = 0\\), we have \\(a = 3\\), \\(b = -5\\), and \\(c = 1\\). Therefore, \\(\\Delta = (-5)^2 - 4(3)(1) = 25 - 12 = 13\\).",
                difficulty: "Basic"
            },
            {
                text: "Which of the following quadratic equations has exactly one real solution?",
                options: [
                    "\\(2x^2 - 4x + 3 = 0\\)",
                    "\\(x^2 - 6x + 9 = 0\\)",
                    "\\(3x^2 + 2x - 1 = 0\\)",
                    "\\(4x^2 + 3x + 5 = 0\\)"
                ],
                correctIndex: 1,
                explanation: "A quadratic equation has exactly one real solution when its discriminant equals zero. Let's calculate the discriminant for each option:<br><br>\\(2x^2 - 4x + 3 = 0\\): \\(\\Delta = (-4)^2 - 4(2)(3) = 16 - 24 = -8 < 0\\) → No real solutions<br><br>\\(x^2 - 6x + 9 = 0\\): \\(\\Delta = (-6)^2 - 4(1)(9) = 36 - 36 = 0\\) → Exactly one real solution<br><br>\\(3x^2 + 2x - 1 = 0\\): \\(\\Delta = 2^2 - 4(3)(-1) = 4 + 12 = 16 > 0\\) → Two distinct real solutions<br><br>\\(4x^2 + 3x + 5 = 0\\): \\(\\Delta = 3^2 - 4(4)(5) = 9 - 80 = -71 < 0\\) → No real solutions",
                difficulty: "Intermediate"
            },
            {
                text: "What is the relationship between the discriminant and the factorization of a quadratic expression?",
                options: [
                    "A positive discriminant means the quadratic can be factored as a perfect square",
                    "A negative discriminant means the quadratic can always be factored with real coefficients",
                    "A zero discriminant means the quadratic can be factored as a perfect square",
                    "The discriminant has no relationship to factorization"
                ],
                correctIndex: 2,
                explanation: "When the discriminant is zero, the quadratic expression factors as a perfect square: \\(ax^2 + bx + c = a(x - r)^2\\) where \\(r\\) is the repeated root. When the discriminant is positive, the quadratic can be factored into two different linear factors with real coefficients: \\(ax^2 + bx + c = a(x - r_1)(x - r_2)\\). When the discriminant is negative, the quadratic cannot be factored with real coefficients (complex factors would be required).",
                difficulty: "Intermediate"
            },
            {
                text: "For what value of \\(k\\) will the equation \\(x^2 + kx + 25 = 0\\) have two complex roots?",
                options: [
                    "\\(k = 10\\)",
                    "\\(k = -10\\)",
                    "\\(|k| < 10\\)",
                    "\\(|k| > 10\\)"
                ],
                correctIndex: 2,
                explanation: "For the equation to have two complex roots, the discriminant must be negative: \\(\\Delta = k^2 - 4(1)(25) < 0\\). Simplifying: \\(k^2 - 100 < 0\\), which gives us \\(k^2 < 100\\), or \\(|k| < 10\\). This means the equation will have two complex roots for any value of \\(k\\) between -10 and 10, excluding -10 and 10 themselves.",
                difficulty: "Advanced"
            }
        ]
    };
    
    MCQQuiz.create('discriminant-mcq', quizData);
});
</script>

#### Identity Questions: Discriminant Applications

<div id="discriminant-identity-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const discriminantContent = {
        "title": "The Discriminant: Applications and Analysis",
        "intro_content": `
            <p>The discriminant \\(\\Delta = b^2 - 4ac\\) of a quadratic equation \\(ax^2 + bx + c = 0\\) provides immediate insight into the nature of its solutions. This powerful mathematical tool can predict whether an equation has two distinct real solutions, one repeated real solution, or two complex solutions, without actually solving the equation.</p>
            <p>Beyond just counting solutions, the discriminant connects algebra to geometry and has far-reaching applications across multiple disciplines.</p>
        `,
        "questions": [
            {
                "category": "scientific",
                "title": "Physics: Kinematic Analysis",
                "content": `
                    <p>A physicist is analyzing the trajectory of a projectile launched from a height of 45 meters with an initial velocity of 20 m/s at an angle of 30° above the horizontal. The height \\(h\\) of the projectile above the ground at time \\(t\\) is given by:</p>
                    <p>\\(h = 45 + 20\\sin(30°)t - 4.9t^2\\)</p>
                    <p>Simplifying: \\(h = 45 + 10t - 4.9t^2\\)</p>
                    <p>a) Form a quadratic equation to determine when the projectile hits the ground (\\(h = 0\\)).</p>
                    <p>b) Calculate the discriminant of this equation and explain what it tells you about the projectile's motion.</p>
                    <p>c) If the launch angle is increased, how would this affect the discriminant and what would this mean physically?</p>
                `,
                "answer": `
                    <p>a) To find when the projectile hits the ground, we set \\(h = 0\\) and solve:</p>
                    <p>\\(0 = 45 + 10t - 4.9t^2\\)</p>
                    <p>\\(4.9t^2 - 10t - 45 = 0\\)</p>
                    <p>This is our quadratic equation in standard form with \\(a = 4.9\\), \\(b = -10\\), and \\(c = -45\\).</p>
                    
                    <p>b) The discriminant is \\(\\Delta = b^2 - 4ac\\):</p>
                    <p>\\(\\Delta = (-10)^2 - 4 \\times 4.9 \\times (-45)\\)</p>
                    <p>\\(\\Delta = 100 + 882\\)</p>
                    <p>\\(\\Delta = 982\\)</p>
                    
                    <p>Since the discriminant is positive, the quadratic equation has two distinct real solutions. This tells us that:</p>
                    <p>1. The projectile crosses the ground level at two different times</p>
                    <p>2. The first solution represents when the projectile is launched (if we were to extend the trajectory backwards in time, which is not physically relevant for this problem)</p>
                    <p>3. The second solution represents when the projectile actually hits the ground after following its parabolic path</p>
                    
                    <p>We can verify this by finding the solutions:</p>
                    <p>\\(t = \\frac{10 \\pm \\sqrt{982}}{2 \\times 4.9} \\approx \\frac{10 \\pm 31.34}{9.8}\\)</p>
                    <p>\\(t_1 \\approx \\frac{10 - 31.34}{9.8} \\approx -2.18\\) seconds (not physically relevant)</p>
                    <p>\\(t_2 \\approx \\frac{10 + 31.34}{9.8} \\approx 4.22\\) seconds (when the projectile hits the ground)</p>
                    
                    <p>c) If the launch angle is increased:</p>
                    <p>- The initial vertical velocity component (\\(20\\sin(\\theta)\\)) would increase</p>
                    <p>- In our equation \\(h = 45 + 20\\sin(\\theta)t - 4.9t^2\\), the coefficient of \\(t\\) would increase</p>
                    <p>- For the quadratic \\(4.9t^2 - 20\\sin(\\theta)t - 45 = 0\\), the absolute value of \\(b\\) would increase</p>
                    <p>- This would make the discriminant \\(\\Delta = (20\\sin(\\theta))^2 - 4 \\times 4.9 \\times (-45)\\) larger</p>
                    
                    <p>Physically, this means:</p>
                    <p>- The projectile would stay in the air longer before hitting the ground</p>
                    <p>- The difference between the two solutions would increase, indicating a longer flight time</p>
                    <p>- The projectile would reach a greater height and travel farther horizontally</p>
                    
                    <p>If the angle were increased enough (approaching 90°), the projectile would rise almost straight up and fall back down along nearly the same path, spending the maximum possible time in the air for the given initial velocity.</p>
                `
            },
            {
                "category": "engineering",
                "title": "Civil Engineering: Arch Design",
                "content": `
                    <p>A civil engineer is designing a parabolic arch for a bridge. The arch is modeled by the equation:</p>
                    <p>\\(y = -0.05x^2 + 0.5x + 10\\)</p>
                    <p>where \\(y\\) is the height in meters and \\(x\\) is the horizontal distance in meters from the left support.</p>
                    <p>a) Formulate a quadratic equation to determine where the arch height equals 8 meters.</p>
                    <p>b) Calculate the discriminant of this equation and interpret what it means for the arch design.</p>
                    <p>c) The engineer needs to ensure the arch is at least 5 meters high throughout the middle 20-meter section of the bridge. Determine if this constraint is met by analyzing an appropriate discriminant.</p>
                `,
                "answer": `
                    <p>a) To find where the arch height equals 8 meters, we set \\(y = 8\\) and solve:</p>
                    <p>\\(8 = -0.05x^2 + 0.5x + 10\\)</p>
                    <p>\\(0 = -0.05x^2 + 0.5x + 10 - 8\\)</p>
                    <p>\\(0 = -0.05x^2 + 0.5x + 2\\)</p>
                    <p>This is our quadratic equation in standard form with \\(a = -0.05\\), \\(b = 0.5\\), and \\(c = 2\\).</p>
                    
                    <p>b) The discriminant is \\(\\Delta = b^2 - 4ac\\):</p>
                    <p>\\(\\Delta = 0.5^2 - 4 \\times (-0.05) \\times 2\\)</p>
                    <p>\\(\\Delta = 0.25 + 0.4\\)</p>
                    <p>\\(\\Delta = 0.65\\)</p>
                    
                    <p>Since the discriminant is positive, the equation has two distinct real solutions. This means the arch crosses the 8-meter height at two different horizontal positions. This makes sense geometrically, as a parabolic arch would reach the same height at two symmetric points on either side of its peak.</p>
                    
                    <p>We can find these points:</p>
                    <p>\\(x = \\frac{-0.5 \\pm \\sqrt{0.65}}{2 \\times (-0.05)} \\approx \\frac{-0.5 \\pm 0.806}{-0.1}\\)</p>
                    <p>\\(x_1 \\approx \\frac{-0.5 - 0.806}{-0.1} \\approx 13.06\\) meters</p>
                    <p>\\(x_2 \\approx \\frac{-0.5 + 0.806}{-0.1} \\approx -3.06\\) meters</p>
                    
                    <p>Since a bridge would have positive x-coordinates, the solution \\(x_1 \\approx 13.06\\) meters is physically relevant, but \\(x_2\\) is not. This suggests the equation might need to be adjusted with a different coordinate system or the arch is asymmetric.</p>
                    
                    <p>Alternatively, if we interpret negative x-values as valid (measuring from some central point with leftward being negative), then the arch crosses the 8-meter height at approximately -3.06 meters and 13.06 meters from the reference point.</p>
                    
                    <p>c) To analyze if the arch is at least 5 meters high throughout the middle 20-meter section, we need to identify this section first. Let's assume the bridge has a symmetric design with the midpoint at \\(x = 0\\), so the middle 20-meter section extends from \\(x = -10\\) to \\(x = 10\\).</p>
                    
                    <p>We need to check whether the height drops below 5 meters anywhere in this section. We set \\(y = 5\\) and solve:</p>
                    <p>\\(5 = -0.05x^2 + 0.5x + 10\\)</p>
                    <p>\\(0 = -0.05x^2 + 0.5x + 10 - 5\\)</p>
                    <p>\\(0 = -0.05x^2 + 0.5x + 5\\)</p>
                    
                    <p>The discriminant is:</p>
                    <p>\\(\\Delta = 0.5^2 - 4 \\times (-0.05) \\times 5\\)</p>
                    <p>\\(\\Delta = 0.25 + 1\\)</p>
                    <p>\\(\\Delta = 1.25\\)</p>
                    
                    <p>Since the discriminant is positive, there are two points where the arch equals 5 meters. Calculating these points:</p>
                    <p>\\(x = \\frac{-0.5 \\pm \\sqrt{1.25}}{2 \\times (-0.05)} \\approx \\frac{-0.5 \\pm 1.118}{-0.1}\\)</p>
                    <p>\\(x_1 \\approx \\frac{-0.5 - 1.118}{-0.1} \\approx 16.18\\) meters</p>
                    <p>\\(x_2 \\approx \\frac{-0.5 + 1.118}{-0.1} \\approx -6.18\\) meters</p>
                    
                    <p>This means the arch equals 5 meters at \\(x \\approx -6.18\\) and \\(x \\approx 16.18\\). Since both of these points lie outside the middle section (\\(-10 \\leq x \\leq 10\\)), and the arch is parabolic (opening downward), the height must be greater than 5 meters throughout the entire middle section.</p>
                    
                    <p>Therefore, the constraint that the arch be at least 5 meters high throughout the middle 20-meter section is met.</p>
                `
            },
            {
                "category": "financial",
                "title": "Economics: Market Equilibrium Analysis",
                "content": `
                    <p>An economist is analyzing a market where the demand function \\(D(p)\\) and supply function \\(S(p)\\) (both in thousands of units) are related to price \\(p\\) (in dollars) as follows:</p>
                    <p>\\(D(p) = 100 - 2p^2\\)</p>
                    <p>\\(S(p) = p^2 - 6p + 13\\)</p>
                    <p>a) Develop a quadratic equation for finding the market equilibrium price (where supply equals demand).</p>
                    <p>b) Calculate the discriminant of this equation and explain what it reveals about the number of possible equilibrium points in this market.</p>
                    <p>c) The economist proposes a new supply function \\(S'(p) = p^2 - 6p + 25\\). How would this change the market equilibrium situation? Use the discriminant to explain your answer.</p>
                `,
                "answer": `
                    <p>a) At market equilibrium, supply equals demand:</p>
                    <p>\\(S(p) = D(p)\\)</p>
                    <p>\\(p^2 - 6p + 13 = 100 - 2p^2\\)</p>
                    <p>\\(p^2 - 6p + 13 + 2p^2 = 100\\)</p>
                    <p>\\(3p^2 - 6p + 13 - 100 = 0\\)</p>
                    <p>\\(3p^2 - 6p - 87 = 0\\)</p>
                    
                    <p>This is our quadratic equation in standard form with \\(a = 3\\), \\(b = -6\\), and \\(c = -87\\).</p>
                    
                    <p>b) The discriminant is \\(\\Delta = b^2 - 4ac\\):</p>
                    <p>\\(\\Delta = (-6)^2 - 4 \\times 3 \\times (-87)\\)</p>
                    <p>\\(\\Delta = 36 + 1044\\)</p>
                    <p>\\(\\Delta = 1080\\)</p>
                    
                    <p>Since the discriminant is positive, the equation has two distinct real solutions. This means there are two different prices at which market equilibrium can occur.</p>
                    
                    <p>Let's calculate these equilibrium prices:</p>
                    <p>\\(p = \\frac{6 \\pm \\sqrt{1080}}{2 \\times 3} = \\frac{6 \\pm 32.86}{6}\\)</p>
                    <p>\\(p_1 \\approx \\frac{6 - 32.86}{6} \\approx -4.48\\)</p>
                    <p>\\(p_2 \\approx \\frac{6 + 32.86}{6} \\approx 6.48\\)</p>
                    
                    <p>Since prices can't be negative in this economic context, only \\(p_2 \\approx \\$6.48\\) is a valid equilibrium price. At this price, supply and demand are both approximately 55.97 thousand units.</p>
                    
                    <p>This illustrates an important point: even when the discriminant indicates two mathematical solutions, only one may be economically meaningful.</p>
                    
                    <p>c) With the new supply function \\(S'(p) = p^2 - 6p + 25\\), we get a new equilibrium equation:</p>
                    <p>\\(S'(p) = D(p)\\)</p>
                    <p>\\(p^2 - 6p + 25 = 100 - 2p^2\\)</p>
                    <p>\\(p^2 - 6p + 25 + 2p^2 = 100\\)</p>
                    <p>\\(3p^2 - 6p + 25 - 100 = 0\\)</p>
                    <p>\\(3p^2 - 6p - 75 = 0\\)</p>
                    
                    <p>The new discriminant is:</p>
                    <p>\\(\\Delta' = (-6)^2 - 4 \\times 3 \\times (-75)\\)</p>
                    <p>\\(\\Delta' = 36 + 900\\)</p>
                    <p>\\(\\Delta' = 936\\)</p>
                    
                    <p>The discriminant is still positive, indicating two distinct real solutions:</p>
                    <p>\\(p = \\frac{6 \\pm \\sqrt{936}}{2 \\times 3} = \\frac{6 \\pm 30.59}{6}\\)</p>
                    <p>\\(p_1 \\approx \\frac{6 - 30.59}{6} \\approx -4.1\\)</p>
                    <p>\\(p_2 \\approx \\frac{6 + 30.59}{6} \\approx 6.1\\)</p>
                    
                    <p>The valid equilibrium price is now approximately \\$6.10, slightly lower than before. This makes economic sense because the new supply function has a higher constant term, meaning that at every price, more units are supplied. With greater supply at all price levels, we would expect equilibrium to occur at a lower price.</p>
                    
                    <p>At this new equilibrium price, supply and demand are both approximately 54.6 thousand units, slightly less than the previous equilibrium quantity. This indicates that the market has shifted to a new equilibrium with a lower price and slightly lower quantity.</p>
                `
            },
            {
                "category": "creative",
                "title": "Music Theory: Harmonics and Frequency",
                "content": `
                    <p>A music theorist is studying the relationship between frequency ratios and perceived harmonics. For two notes to be in perfect harmony, their frequencies must be in specific ratios. When a note of frequency \\(f\\) is played, the frequencies that create pleasing harmonies with it can often be described by quadratic relationships.</p>
                    <p>For a reference note with frequency 440 Hz (A4), the frequencies \\(x\\) that form specific harmonic intervals satisfy the equation:</p>
                    <p>\\(3x^2 - 2640x + 580800 = 0\\)</p>
                    <p>a) Calculate the discriminant of this equation and interpret what it tells you about the possible harmonies.</p>
                    <p>b) Find the frequencies that satisfy this equation and identify what musical intervals they create with the reference note.</p>
                    <p>c) If we modify the equation to \\(3x^2 - 2640x + 580800 + k = 0\\), determine the range of values for \\(k\\) that would result in no real solutions. What would this mean musically?</p>
                `,
                "answer": `
                    <p>a) The discriminant of \\(3x^2 - 2640x + 580800 = 0\\) is:</p>
                    <p>\\(\\Delta = (-2640)^2 - 4 \\times 3 \\times 580800\\)</p>
                    <p>\\(\\Delta = 6969600 - 6969600\\)</p>
                    <p>\\(\\Delta = 0\\)</p>
                    
                    <p>Since the discriminant is exactly zero, the equation has exactly one repeated real solution. This suggests that there is precisely one frequency that forms this particular harmonic relationship with the reference note.</p>
                    
                    <p>In music theory, when the discriminant is zero, it often represents a special or "perfect" interval, such as an octave or perfect fifth, which have simple frequency ratios (2:1 and 3:2 respectively).</p>
                    
                    <p>b) With a discriminant of zero, we have one repeated solution:</p>
                    <p>\\(x = \\frac{2640 \\pm 0}{2 \\times 3} = \\frac{2640}{6} = 440\\) Hz</p>
                    
                    <p>Interestingly, the frequency that satisfies the equation is 440 Hz, which is the same as our reference note A4. This suggests that the equation is modeling the relationship of a note with itself, which is called a unison (1:1 ratio).</p>
                    
                    <p>We can verify this by checking:</p>
                    <p>\\(3(440)^2 - 2640(440) + 580800\\)</p>
                    <p>\\(= 3 \\times 193600 - 2640 \\times 440 + 580800\\)</p>
                    <p>\\(= 580800 - 1161600 + 580800\\)</p>
                    <p>\\(= 0\\)</p>
                    
                    <p>This confirms that 440 Hz is indeed the solution. The equation represents the unison interval, where a note is in harmony with itself.</p>
                    
                    <p>c) For the modified equation \\(3x^2 - 2640x + 580800 + k = 0\\) to have no real solutions, its discriminant must be negative:</p>
                    <p>\\(\\Delta = (-2640)^2 - 4 \\times 3 \\times (580800 + k) < 0\\)</p>
                    <p>\\(\\Delta = 6969600 - 6969600 - 12k < 0\\)</p>
                    <p>\\(\\Delta = -12k < 0\\)</p>
                    <p>\\(k > 0\\)</p>
                    
                    <p>Therefore, any positive value of \\(k\\) would result in no real solutions.</p>
                    
                    <p>Musically, this means that if we modify the harmonic relationship slightly (by adding a small positive value to the equation), there would be no frequency that forms this exact harmonic relationship with the reference note. This reflects the concept of "tempering" in music, where perfect mathematical ratios are slightly adjusted to accommodate practical considerations in instrument tuning.</p>
                    
                    <p>In modern music, especially with equal temperament tuning (used in pianos and most Western instruments), pure mathematical harmonies are often slightly modified to allow playing in different keys. The lack of real solutions when \\(k > 0\\) mathematically represents the compromise between theoretical perfection and practical musical flexibility.</p>
                `
            }
        ]
    };
    
    MathQuestionModule.render(discriminantContent, 'discriminant-identity-container');
});
</script>

### Key Takeaways

```{important}
1. The discriminant $\Delta = b^2 - 4ac$ determines the nature of solutions to a quadratic equation
2. When $\Delta > 0$, the equation has two distinct real solutions
3. When $\Delta = 0$, the equation has one repeated real solution
4. When $\Delta < 0$, the equation has two complex solutions but no real solutions
5. The discriminant can be used to analyze problems without solving the full equation
```

## Summary

In this module, we explored quadratic equations and their various solution methods:

```{important}
1. **Standard Form**: $ax^2 + bx + c = 0$ where $a \neq 0$
2. **Factorization**: $(px + q)(rx + s) = 0$, best for quadratics with "nice" integer coefficients
3. **Graphical Methods**: Understanding parabolas and using the completed square form $a(x + p)^2 + q$
4. **Quadratic Formula**: $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$ works for any quadratic equation
5. **Discriminant**: $\Delta = b^2 - 4ac$ determines the number and type of solutions
```

Each method has its strengths:
- Factorization is quick when the roots are rational numbers
- Completing the square reveals the vertex and graph properties
- The quadratic formula works universally, even for complex solutions
- The discriminant lets you analyze the nature of solutions without solving

Mastering these techniques gives you powerful tools to solve a wide range of mathematical and real-world problems across various disciplines.