# Geometric Sequences

## Arithmetic Sequences Revision

### Theory

Geometric sequences build upon the understanding of arithmetic sequences, where terms change by a constant difference. In contrast, geometric sequences involve constant ratios between consecutive terms, leading to exponential growth or decay patterns.

$$\text{Arithmetic: } a_n = a_1 + (n-1)d$$

$$\text{Common Difference: } d = a_{n+1} - a_n$$

### Application

#### Examples

##### Example 1: Arithmetic vs Geometric Recognition
Compare sequences: A) 2, 5, 8, 11, 14, ... and B) 2, 6, 18, 54, 162, ...

**Method 1: Difference Analysis**

$\text{Sequence A differences: } 3, 3, 3, 3, ... \quad \text{(constant difference)}$

$\text{Sequence B differences: } 4, 12, 36, 108, ... \quad \text{(not constant)}$

$\text{Sequence B ratios: } 3, 3, 3, 3, ... \quad \text{(constant ratio)}$

#### Interactive Visualization: Sequence Comparison

<div id="arithmetic-revision-container" class="visualization-container" style="height: 500px; display: flex; align-items: center; justify-content: center; background-color: #f8f9fa; border: 2px dashed #dee2e6; border-radius: 8px;">
    <div style="text-align: center; color: #6c757d; font-size: 18px; font-weight: 500;">
        Interactive Graph
        <div style="font-size: 14px; margin-top: 8px; font-weight: normal;">
            Arithmetic vs geometric sequence visualization will be implemented here
        </div>
    </div>
</div>

#### Multiple Choice Questions

<div id="arithmetic-revision-mcq" class="quiz-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Arithmetic Sequences Review Questions",
        questions: [
            {
                text: "What is the 10th term of the arithmetic sequence 7, 11, 15, 19, ...?",
                options: ["\\(43\\)", "\\(47\\)", "\\(51\\)", "\\(55\\)"],
                correctIndex: 0,
                explanation: "Common difference d = 4. Using \\(a_n = a_1 + (n-1)d\\): \\(a_{10} = 7 + 9(4) = 43\\)",
                difficulty: "Basic"
            },
            {
                text: "Which statement is true about arithmetic sequences?",
                options: ["Ratios are constant", "Differences are constant", "Terms grow exponentially", "Graph is curved"],
                correctIndex: 1,
                explanation: "Arithmetic sequences have constant differences between consecutive terms, creating linear growth.",
                difficulty: "Basic"
            }
        ]
    };
    MCQQuiz.create('arithmetic-revision-mcq', quizData);
});
</script>

## Geometric Sequences

### Theory

**Content Depth Guidelines**: The theory section must provide comprehensive coverage that enables diverse application examples across all four sectors (scientific, engineering, financial, creative). Include foundational definitions with clear mathematical notation, key formulas and relationships with step-by-step derivations where appropriate, properties and characteristics that students need for problem-solving, multiple solution methods when applicable (algebraic, graphical, numerical), common variations and special cases that appear in real-world applications, and connections to prerequisite concepts and preview of advanced applications.

**Foundational Definitions:** A geometric sequence is a sequence where each term after the first is obtained by multiplying the previous term by a constant called the common ratio. This creates patterns of exponential growth or decay.

**Basic Geometric Sequence Properties:**

**Definition and General Term:** A geometric sequence with first term $a_1$ and common ratio $r$

$$a_n = a_1 \cdot r^{n-1}$$

• Each term: $a_n = a_{n-1} \cdot r$ for $n \geq 2$
• Common ratio: $r = \frac{a_{n+1}}{a_n}$ (constant for all valid n)
• Domain: positive integers for term position
• Exponential relationship between term value and position

**Common Ratio Analysis:**

**Growth Patterns:** Different values of $r$ create distinct behaviors

• $r > 1$: Exponential growth (terms increase)
• $0 < r < 1$: Exponential decay (terms decrease toward zero)
• $r = 1$: Constant sequence (all terms equal)
• $r = 0$: Sequence becomes zero after first term
• $r < 0$: Alternating signs with exponential magnitude change

**Special Cases and Considerations:**

• $r = -1$: Alternating sequence: $a_1, -a_1, a_1, -a_1, ...$
• $|r| > 1$ with $r < 0$: Alternating with increasing magnitude
• $|r| < 1$ with $r < 0$: Alternating with decreasing magnitude
• Fractional ratios: Often represent decay processes

**Recursive Definition:** Alternative formulation using recurrence relations

$$a_1 = \text{initial term}$$
$$a_n = r \cdot a_{n-1} \text{ for } n \geq 2$$

• Requires initial condition and common ratio
• Useful for computational generation
• Clear relationship between consecutive terms
• Foundation for series analysis

**Finding Terms in Geometric Sequences:**

**Direct Formula Method:** Using the general term formula

$$a_n = a_1 \cdot r^{n-1}$$

• Requires: first term $a_1$ and common ratio $r$
• Direct calculation of any term
• No need to calculate intermediate terms
• Efficient for large values of $n$

**Given Two Terms Method:** Finding sequence parameters

If $a_m = A$ and $a_n = B$, then:

$$\frac{a_n}{a_m} = \frac{a_1 \cdot r^{n-1}}{a_1 \cdot r^{m-1}} = r^{n-m}$$

Therefore: $r = \left(\frac{B}{A}\right)^{\frac{1}{n-m}}$

**Finding Missing Terms:** Using geometric mean property

Between any two terms $a_m$ and $a_n$ in a geometric sequence:

$$a_k = \sqrt[n-m]{a_m^{n-k} \cdot a_n^{k-m}}$$

For geometric mean of two terms: $a_k = \sqrt{a_m \cdot a_n}$

**Applications and Modeling:**

**Exponential Growth Models:** Population, compound interest, radioactive decay

• Population growth: $P(t) = P_0 \cdot r^t$
• Compound interest: $A = P(1 + i)^n$
• Radioactive decay: $N(t) = N_0 \cdot (1/2)^{t/t_{1/2}}$
• Biological processes: cell division, bacterial growth

**Discrete Sampling of Continuous Functions:**

• Exponential functions: $f(x) = ab^x$ sampled at integer points
• Relationship to continuous exponential growth
• Connection between discrete sequences and continuous models
• Bridge to differential equations and calculus

```{tip}
To verify a sequence is geometric, check that the ratio between any two consecutive terms is constant. This ratio must be the same throughout the entire sequence for it to be truly geometric.
```

#### Interactive Visualization: Geometric Sequence Explorer

<div id="geometric-sequences-container" class="visualization-container" style="height: 500px; display: flex; align-items: center; justify-content: center; background-color: #f8f9fa; border: 2px dashed #dee2e6; border-radius: 8px;">
    <div style="text-align: center; color: #6c757d; font-size: 18px; font-weight: 500;">
        Interactive Graph
        <div style="font-size: 14px; margin-top: 8px; font-weight: normal;">
            Geometric sequence visualization and parameter exploration will be implemented here
        </div>
    </div>
</div>

### Application

#### Examples

##### Example 1: Finding the General Term
Solve: Find the general term of the geometric sequence 3, 12, 48, 192, ...

**Method 1: Common Ratio Identification**

$r = \frac{a_2}{a_1} = \frac{12}{3} = 4 \quad \text{(calculate common ratio)}$

$\text{Verify: } \frac{48}{12} = 4, \frac{192}{48} = 4 \quad \text{(confirm constant ratio)}$

$a_n = a_1 \cdot r^{n-1} = 3 \cdot 4^{n-1} \quad \text{(general term formula)}$

**Method 2: Pattern Recognition**

$3 = 3 \cdot 4^0, 12 = 3 \cdot 4^1, 48 = 3 \cdot 4^2, 192 = 3 \cdot 4^3 \quad \text{(identify pattern)}$

$a_n = 3 \cdot 4^{n-1} \quad \text{(confirm formula)}$

##### Example 2: Finding Missing Terms
Solve: In a geometric sequence, $a_3 = 20$ and $a_7 = 320$. Find $a_1$, $r$, and $a_5$.

**Method 1: Ratio Method**

$\frac{a_7}{a_3} = \frac{a_1 \cdot r^6}{a_1 \cdot r^2} = r^4 = \frac{320}{20} = 16 \quad \text{(find ratio power)}$

$r^4 = 16 \Rightarrow r = \pm 2 \quad \text{(solve for common ratio)}$

$a_3 = a_1 \cdot r^2 \Rightarrow 20 = a_1 \cdot 4 \Rightarrow a_1 = 5 \quad \text{(assuming } r = 2\text{)}$

$a_5 = a_1 \cdot r^4 = 5 \cdot 16 = 80 \quad \text{(find middle term)}$

##### Example 3: Geometric Sequence in Real Context
Solve: A bacteria culture doubles every hour. Starting with 500 bacteria, how many will there be after 8 hours?

**Method 1: Geometric Modeling**

$a_1 = 500, r = 2, n = 9 \quad \text{(initial conditions, 8 hours = 9th term)}$

$a_9 = 500 \cdot 2^{9-1} = 500 \cdot 2^8 \quad \text{(apply formula)}$

$a_9 = 500 \cdot 256 = 128,000 \quad \text{(calculate final population)}$

**Method 2: Step-by-Step Growth**

$\text{Hour 0: } 500, \text{ Hour 1: } 1000, \text{ Hour 2: } 2000, ... \quad \text{(verify pattern)}$

$\text{General: } P(t) = 500 \cdot 2^t \quad \text{(continuous model)}$

#### Multiple Choice Questions

<div id="geometric-sequences-mcq" class="quiz-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Geometric Sequences Practice Questions",
        questions: [
            {
                text: "What is the 6th term of the geometric sequence 2, 6, 18, 54, ...?",
                options: ["\\(162\\)", "\\(486\\)", "\\(1458\\)", "\\(4374\\)"],
                correctIndex: 1,
                explanation: "Common ratio r = 3. Using \\(a_n = 2 \\cdot 3^{n-1}\\): \\(a_6 = 2 \\cdot 3^5 = 2 \\cdot 243 = 486\\)",
                difficulty: "Basic"
            },
            {
                text: "In a geometric sequence, if \\(a_1 = 4\\) and \\(r = \\frac{1}{2}\\), what is \\(a_5\\)?",
                options: ["\\(\\frac{1}{4}\\)", "\\(\\frac{1}{2}\\)", "\\(1\\)", "\\(2\\)"],
                correctIndex: 0,
                explanation: "\\(a_5 = 4 \\cdot \\left(\\frac{1}{2}\\right)^4 = 4 \\cdot \\frac{1}{16} = \\frac{1}{4}\\)",
                difficulty: "Intermediate"
            },
            {
                text: "Which of the following is NOT a geometric sequence?",
                options: ["\\(1, 4, 16, 64, ...\\)", "\\(5, 15, 45, 135, ...\\)", "\\(2, 4, 8, 12, ...\\)", "\\(3, -6, 12, -24, ...\\)"],
                correctIndex: 2,
                explanation: "The sequence 2, 4, 8, 12, ... has differences 2, 4, 4, which are not constant ratios (2, 2, 1.5).",
                difficulty: "Basic"
            },
            {
                text: "If \\(a_2 = 12\\) and \\(a_5 = 96\\) in a geometric sequence, what is the common ratio?",
                options: ["\\(2\\)", "\\(4\\)", "\\(8\\)", "\\(\\pm 2\\)"],
                correctIndex: 3,
                explanation: "\\(\\frac{a_5}{a_2} = r^3 = \\frac{96}{12} = 8\\), so \\(r = 2\\). However, \\(r = -2\\) also works, giving \\(r = \\pm 2\\).",
                difficulty: "Intermediate"
            }
        ]
    };
    MCQQuiz.create('geometric-sequences-mcq', quizData);
});
</script>

#### Sector Specific Questions: Geometric Sequences Applications

<div id="geometric-sequences-identity-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const geometricSequencesContent = {
        "title": "Geometric Sequences: Applications",
        "intro_content": `<p>Geometric sequences model exponential processes across all sectors, from population growth and radioactive decay in science to compound interest in finance and signal processing in engineering. Understanding these patterns is crucial for prediction, optimization, and system design.</p>`,
        "questions": [
            {
                "category": "scientific",
                "title": "Physics: Radioactive Decay Analysis",
                "content": `A radioactive isotope has a half-life of 3 years, starting with 800 grams. Model this as a geometric sequence and determine how much remains after 15 years. At what point will less than 10 grams remain?`,
                "answer": `<p><strong>Solution:</strong></p>
                <p>Step 1: Establish geometric sequence parameters</p>
                <p>Initial amount: \\(a_1 = 800\\) grams</p>
                <p>After each half-life (3 years): amount halves</p>
                <p>Common ratio: \\(r = \\frac{1}{2} = 0.5\\)</p>
                <p>Step 2: Create sequence for 3-year intervals</p>
                <p>\\(a_n = 800 \\times 0.5^{n-1}\\) where \\(n\\) is the number of 3-year periods</p>
                <p>After 15 years: \\(n = \\frac{15}{3} + 1 = 6\\)</p>
                <p>\\(a_6 = 800 \\times 0.5^5 = 800 \\times \\frac{1}{32} = 25\\) grams</p>
                <p>Step 3: Find when amount drops below 10 grams</p>
                <p>\\(800 \\times 0.5^{n-1} < 10\\)</p>
                <p>\\(0.5^{n-1} < \\frac{10}{800} = 0.0125\\)</p>
                <p>\\(n-1 > \\log_{0.5}(0.0125) ≈ 6.32\\)</p>
                <p>Therefore \\(n ≥ 8\\), which means after \\(7 \\times 3 = 21\\) years</p>`
            },
            {
                "category": "engineering",
                "title": "Signal Processing: Digital Filter Design",
                "content": `A digital low-pass filter reduces signal amplitude by 20% at each stage. If an input signal has amplitude 100V, design a 6-stage filter system. What is the output amplitude? How many stages are needed to reduce the signal below 1V?`,
                "answer": `<p><strong>Solution:</strong></p>
                <p>Step 1: Model as geometric sequence</p>
                <p>Initial amplitude: \\(a_1 = 100\\)V</p>
                <p>Reduction factor: 20% removed means 80% remains</p>
                <p>Common ratio: \\(r = 0.8\\)</p>
                <p>Step 2: Calculate 6-stage output</p>
                <p>\\(a_n = 100 \\times 0.8^{n-1}\\)</p>
                <p>After 6 stages: \\(a_6 = 100 \\times 0.8^5 = 100 \\times 0.32768 = 32.768\\)V</p>
                <p>Step 3: Find stages for amplitude < 1V</p>
                <p>\\(100 \\times 0.8^{n-1} < 1\\)</p>
                <p>\\(0.8^{n-1} < 0.01\\)</p>
                <p>\\((n-1) \\log(0.8) < \\log(0.01)\\)</p>
                <p>\\(n-1 > \\frac{\\log(0.01)}{\\log(0.8)} = \\frac{-2}{-0.0969} ≈ 20.6\\)</p>
                <p>Therefore, 22 stages needed to achieve amplitude below 1V</p>
                <p>Engineering significance: Exponential attenuation requires careful stage planning</p>`
            },
            {
                "category": "financial",
                "title": "Investment: Compound Interest Optimization",
                "content": `An investor puts €5,000 into an account with 8% annual compound interest. Model this as a geometric sequence and find the value after 12 years. How long until the investment doubles? Compare with simple interest.`,
                "answer": `<p><strong>Solution:</strong></p>
                <p>Step 1: Compound interest as geometric sequence</p>
                <p>Initial investment: \\(a_1 = 5000\\) €</p>
                <p>Annual growth factor: \\(r = 1 + 0.08 = 1.08\\)</p>
                <p>General term: \\(a_n = 5000 \\times 1.08^{n-1}\\)</p>
                <p>Step 2: Value after 12 years</p>
                <p>\\(a_{13} = 5000 \\times 1.08^{12} = 5000 \\times 2.518 = 12,590\\) €</p>
                <p>Step 3: Doubling time calculation</p>
                <p>\\(5000 \\times 1.08^{n-1} = 10000\\)</p>
                <p>\\(1.08^{n-1} = 2\\)</p>
                <p>\\(n-1 = \\frac{\\log(2)}{\\log(1.08)} = \\frac{0.693}{0.0770} ≈ 9.0\\)</p>
                <p>Doubling time: 9 years</p>
                <p>Step 4: Simple interest comparison</p>
                <p>Simple interest: \\(A = 5000(1 + 0.08 \\times 12) = 9800\\) €</p>
                <p>Compound advantage: €12,590 - €9,800 = €2,790 extra (28.5% more)</p>`
            },
            {
                "category": "creative",
                "title": "Photography: Light Exposure Sequence",
                "content": `A photographer uses a series of neutral density filters, each reducing light by half. Starting with 1000 lux, apply 5 filters in sequence. What's the final light level? Design a filter sequence to achieve exactly 31.25 lux output.`,
                "answer": `<p><strong>Solution:</strong></p>
                <p>Step 1: Model filter sequence</p>
                <p>Initial light: \\(L_1 = 1000\\) lux</p>
                <p>Each filter reduces light by half: \\(r = 0.5\\)</p>
                <p>After \\(n\\) filters: \\(L_n = 1000 \\times 0.5^{n-1}\\)</p>
                <p>Step 2: Calculate final light after 5 filters</p>
                <p>\\(L_6 = 1000 \\times 0.5^5 = 1000 \\times \\frac{1}{32} = 31.25\\) lux</p>
                <p>Step 3: Design sequence for exactly 31.25 lux</p>
                <p>Target: \\(1000 \\times 0.5^{n-1} = 31.25\\)</p>
                <p>\\(0.5^{n-1} = \\frac{31.25}{1000} = 0.03125 = \\frac{1}{32}\\)</p>
                <p>\\(0.5^{n-1} = 0.5^5\\)</p>
                <p>Therefore: \\(n-1 = 5\\), so \\(n = 6\\)</p>
                <p>Photography application: 5 neutral density filters achieve exactly 31.25 lux</p>
                <p>Practical note: \\(2^5 = 32\\), so this represents a 5-stop reduction</p>`
            }
        ]
    };
    MathQuestionModule.render(geometricSequencesContent, 'geometric-sequences-identity-container');
});
</script>

### Key Takeaways

```{important}
1. **General term formula**: \\(a_n = a_1 \\cdot r^{n-1}\\) where \\(a_1\\) is first term and \\(r\\) is common ratio
2. **Common ratio identification**: \\(r = \\frac{a_{n+1}}{a_n}\\) must be constant for all consecutive terms
3. **Growth vs decay**: \\(r > 1\\) creates exponential growth, \\(0 < r < 1\\) creates exponential decay
4. **Alternating sequences**: Negative common ratio creates alternating positive/negative terms
5. **Missing terms**: Use \\(\\frac{a_n}{a_m} = r^{n-m}\\) to find ratio when two terms are known
6. **Geometric mean**: Between terms \\(a_m\\) and \\(a_n\\), intermediate terms satisfy geometric mean property
7. **Real-world modeling**: Geometric sequences model compound interest, population growth, radioactive decay
8. **Exponential nature**: Connection to exponential functions \\(f(x) = ab^x\\) sampled at integer points
```