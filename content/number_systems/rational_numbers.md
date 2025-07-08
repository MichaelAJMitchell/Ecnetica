# Rational Numbers

## Integers Revision

### Theory

Before we dive into rational numbers, let's take a moment to review integers and why we need to expand our number system even further. Here's why this matters: while integers gave us the ability to subtract any two whole numbers, they still can't handle all division problems.

When we divide integers, we often get results that aren't integers themselves:

$$8 \div 2 = 4 \quad \text{(This works perfectly in integers)}$$

$$7 \div 2 = ? \quad \text{(This doesn't give us a whole number)}$$

This limitation is exactly what led mathematicians to develop rational numbers - a brilliant solution that allows us to express any division result precisely!

**Key Integer Properties We'll Build Upon:**

• **Closure under multiplication:** $a \times b \in \mathbb{Z}$ for all integers $a, b$
• **Distributive property:** $a(b + c) = ab + ac$
• **Commutative property:** $a + b = b + a$ and $a \times b = b \times a$
• **Associative property:** $(a + b) + c = a + (b + c)$ and $(a \times b) \times c = a \times (b \times c)$

Notice how these properties will help us understand fraction operations later!

### Application

#### Examples

##### Example 1: When Integer Division Works Perfectly

Let's explore cases where division stays within integers:

$$(-24) \div 6 = -4 \quad \text{(Negative divided by positive gives negative)}$$

$$36 \div (-9) = -4 \quad \text{(Positive divided by negative gives negative)}$$

$$(-45) \div (-5) = 9 \quad \text{(Negative divided by negative gives positive)}$$

These examples show that integers are sometimes sufficient for division, but what about when they're not?

##### Example 2: The Need for Rational Numbers

Here's a typical problem that shows why we need fractions:

$$13 \div 4 = 3 \text{ remainder } 1 \quad \text{(Integer division with remainder)}$$

But this doesn't tell us the complete story! The exact answer is:

$$13 \div 4 = \frac{13}{4} = 3\frac{1}{4} = 3.25 \quad \text{(Rational number representation)}$$

#### Interactive Visualization: From Integers to Fractions

<div id="integer-to-fraction-container" class="visualization-container" style="height: 500px; display: flex; align-items: center; justify-content: center; background-color: #f8f9fa; border: 2px dashed #dee2e6; border-radius: 8px;">
    <div style="text-align: center; color: #6c757d; font-size: 18px; font-weight: 500;">
        Interactive Graph
        <div style="font-size: 14px; margin-top: 8px; font-weight: normal;">
            Integer division and fraction visualization will be implemented here
        </div>
    </div>
</div>

#### Multiple Choice Questions

<div id="integer-revision-mcq" class="quiz-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Integer Division Practice Questions",
        questions: [
            {
                text: "When dividing 23 by 5, what is the remainder?",
                options: ["\\(2\\)", "\\(3\\)", "\\(4\\)", "\\(1\\)"],
                correctIndex: 1,
                explanation: "\\(23 \\div 5 = 4\\) remainder \\(3\\), since \\(5 \\times 4 = 20\\) and \\(23 - 20 = 3\\).",
                difficulty: "Basic"
            },
            {
                text: "Which property explains why \\(5 \\times (3 + 7) = 5 \\times 3 + 5 \\times 7\\)?",
                options: ["Commutative", "Associative", "Distributive", "Identity"],
                correctIndex: 2,
                explanation: "The distributive property states that multiplication distributes over addition: \\(a(b + c) = ab + ac\\).",
                difficulty: "Basic"
            }
        ]
    };
    MCQQuiz.create('integer-revision-mcq', quizData);
});
</script>

## Rational Numbers

### Theory

Let's explore the ingenious solution to our division problem: rational numbers! A **rational number** is any number that can be expressed as a fraction of two integers, where the denominator isn't zero.

**The Set of Rational Numbers:**

$$\mathbb{Q} = \left\{\frac{a}{b} : a, b \in \mathbb{Z}, b \neq 0\right\}$$

Here's why this definition is so powerful: it allows us to represent any division result exactly, not just as an approximation!

**Understanding Fraction Terminology:**

**Parts of a Fraction:**
• **Numerator** (top): The dividend - what's being divided
• **Denominator** (bottom): The divisor - what we're dividing by
• **Fraction bar**: Represents the division operation

**Types of Fractions:**

**Proper Fractions:** When the numerator is smaller than the denominator

$$\frac{3}{5}, \quad \frac{2}{7}, \quad \frac{11}{15} \quad \text{(All less than 1)}$$

**Improper Fractions:** When the numerator is greater than or equal to the denominator

$$\frac{7}{3}, \quad \frac{9}{4}, \quad \frac{15}{15} \quad \text{(Greater than or equal to 1)}$$

**Mixed Numbers:** A whole number combined with a proper fraction

$$2\frac{1}{3} = \frac{7}{3}, \quad 5\frac{3}{4} = \frac{23}{4}$$

**Equivalent Fractions - The Key to Understanding Rational Numbers:**

Here's a crucial insight: many different fractions represent the same rational number!

$$\frac{a}{b} = \frac{a \times k}{b \times k} \quad \text{for any non-zero integer } k$$

For example:
$$\frac{1}{2} = \frac{2}{4} = \frac{3}{6} = \frac{4}{8} = \frac{50}{100}$$

This is why we often simplify fractions to their lowest terms by dividing both numerator and denominator by their greatest common divisor (GCD).

**Fundamental Properties of Rational Numbers:**

**Density Property:** Between any two rational numbers, there's always another rational number

$$\text{Between } \frac{1}{3} \text{ and } \frac{1}{2}, \text{ we have } \frac{5}{12} \text{ (and infinitely many others!)}$$

**Closure Properties:** Rational numbers are closed under all four basic operations (except division by zero)

• Addition: $\frac{a}{b} + \frac{c}{d} = \frac{ad + bc}{bd}$
• Subtraction: $\frac{a}{b} - \frac{c}{d} = \frac{ad - bc}{bd}$
• Multiplication: $\frac{a}{b} \times \frac{c}{d} = \frac{ac}{bd}$
• Division: $\frac{a}{b} \div \frac{c}{d} = \frac{a}{b} \times \frac{d}{c} = \frac{ad}{bc}$ (when $c \neq 0$)

**Relationship to Other Number Systems:**

Notice how rational numbers include all our previous number systems:
• Every natural number $n$ is rational: $n = \frac{n}{1}$
• Every integer $m$ is rational: $m = \frac{m}{1}$
• This means: $\mathbb{N} \subset \mathbb{Z} \subset \mathbb{Q}$

**Decimal Representations:**

It's worth taking a moment to appreciate that every rational number has a decimal representation that either:
• **Terminates:** $\frac{3}{4} = 0.75$
• **Repeats:** $\frac{1}{3} = 0.333...$ or $\frac{2}{7} = 0.285714285714...$

This property distinguishes rational numbers from irrational numbers!

#### Interactive Visualization: Rational Numbers on the Number Line

<div id="rational-number-line-container" class="visualization-container" style="height: 500px; display: flex; align-items: center; justify-content: center; background-color: #f8f9fa; border: 2px dashed #dee2e6; border-radius: 8px;">
    <div style="text-align: center; color: #6c757d; font-size: 18px; font-weight: 500;">
        Interactive Graph
        <div style="font-size: 14px; margin-top: 8px; font-weight: normal;">
            Rational number placement and equivalence visualization will be implemented here
        </div>
    </div>
</div>

### Application

#### Examples

##### Example 1: Simplifying Fractions

Let's work through simplifying $\frac{48}{72}$. This might look complex at first, but we'll break it down systematically.

**Method 1: Finding the GCD**

Here's how we approach this using prime factorization:

$$48 = 2^4 \times 3 = 16 \times 3 \quad \text{(Factor 48)}$$

$$72 = 2^3 \times 3^2 = 8 \times 9 \quad \text{(Factor 72)}$$

$$\text{GCD}(48, 72) = 2^3 \times 3 = 24 \quad \text{(Take lowest powers of common factors)}$$

$$\frac{48}{72} = \frac{48 \div 24}{72 \div 24} = \frac{2}{3} \quad \text{(Divide by GCD)}$$

**Method 2: Step-by-Step Simplification**

Notice what happens when we divide by common factors one at a time:

$$\frac{48}{72} = \frac{48 \div 2}{72 \div 2} = \frac{24}{36} \quad \text{(Both even, divide by 2)}$$

$$\frac{24}{36} = \frac{24 \div 2}{36 \div 2} = \frac{12}{18} \quad \text{(Still even, divide by 2 again)}$$

$$\frac{12}{18} = \frac{12 \div 6}{18 \div 6} = \frac{2}{3} \quad \text{(Divide by 6)}$$

##### Example 2: Adding Fractions with Different Denominators

Let's add $\frac{3}{8} + \frac{5}{12}$. The key insight here is finding a common denominator.

**Finding the Least Common Denominator (LCD):**

$$8 = 2^3, \quad 12 = 2^2 \times 3 \quad \text{(Prime factorization)}$$

$$\text{LCD} = 2^3 \times 3 = 24 \quad \text{(Take highest powers)}$$

**Converting to Common Denominator:**

$$\frac{3}{8} = \frac{3 \times 3}{8 \times 3} = \frac{9}{24} \quad \text{(Multiply by } \frac{3}{3} = 1\text{)}$$

$$\frac{5}{12} = \frac{5 \times 2}{12 \times 2} = \frac{10}{24} \quad \text{(Multiply by } \frac{2}{2} = 1\text{)}$$

**Adding the Fractions:**

$$\frac{9}{24} + \frac{10}{24} = \frac{19}{24} \quad \text{(Add numerators, keep denominator)}$$

##### Example 3: Converting Mixed Numbers

A recipe calls for $3\frac{2}{5}$ cups of flour. Convert this to an improper fraction.

Here's a helpful way to think about this conversion:

$$3\frac{2}{5} = 3 + \frac{2}{5} \quad \text{(Separate whole and fractional parts)}$$

$$= \frac{3 \times 5}{5} + \frac{2}{5} \quad \text{(Express 3 as fifths)}$$

$$= \frac{15}{5} + \frac{2}{5} = \frac{17}{5} \quad \text{(Combine the fractions)}$$

**Quick Method:** $(3 \times 5) + 2 = 17$, so $3\frac{2}{5} = \frac{17}{5}$

#### Multiple Choice Questions

<div id="rational-numbers-mcq" class="quiz-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Rational Numbers Practice Questions",
        questions: [
            {
                text: "Which of the following is a rational number?",
                options: ["\\(\\pi\\)", "\\(\\sqrt{2}\\)", "\\(\\frac{22}{7}\\)", "\\(e\\)"],
                correctIndex: 2,
                explanation: "\\(\\frac{22}{7}\\) is rational because it's expressed as a fraction of integers. \\(\\pi\\), \\(\\sqrt{2}\\), and \\(e\\) are all irrational numbers.",
                difficulty: "Basic"
            },
            {
                text: "Simplify \\(\\frac{84}{126}\\) to lowest terms:",
                options: ["\\(\\frac{2}{3}\\)", "\\(\\frac{4}{6}\\)", "\\(\\frac{14}{21}\\)", "\\(\\frac{42}{63}\\)"],
                correctIndex: 0,
                explanation: "GCD(84, 126) = 42. So \\(\\frac{84}{126} = \\frac{84 \\div 42}{126 \\div 42} = \\frac{2}{3}\\).",
                difficulty: "Intermediate"
            },
            {
                text: "What is \\(\\frac{2}{3} \\times \\frac{5}{8}\\)?",
                options: ["\\(\\frac{10}{24}\\)", "\\(\\frac{5}{12}\\)", "\\(\\frac{10}{11}\\)", "\\(\\frac{7}{11}\\)"],
                correctIndex: 1,
                explanation: "\\(\\frac{2}{3} \\times \\frac{5}{8} = \\frac{2 \\times 5}{3 \\times 8} = \\frac{10}{24} = \\frac{5}{12}\\) after simplification.",
                difficulty: "Basic"
            }
        ]
    };
    MCQQuiz.create('rational-numbers-mcq', quizData);
});
</script>

#### Sector Specific Questions: Rational Numbers Applications

<div id="rational-numbers-identity-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const rationalNumbersContent = {
        "title": "Rational Numbers: Applications",
        "intro_content": `<p>Rational numbers are everywhere in our world! From precise measurements in science to financial calculations, from musical rhythms to engineering designs, fractions and ratios help us express exact relationships. Let's explore how these fundamental numbers apply across different fields.</p>`,
        "questions": [
            {
                "category": "scientific",
                "title": "Biology: Population Genetics",
                "content": `<p>In genetics, allele frequencies are expressed as rational numbers representing the proportion of specific genes in a population.</p>
                <p>a) In a population of 600 plants, 150 have red flowers (RR), 300 have pink flowers (Rr), and 150 have white flowers (rr). What fraction of all alleles in the population are R alleles?</p>
                <p>b) If the frequency of the dominant allele A is \\(\\frac{3}{5}\\), what is the frequency of the recessive allele a?</p>
                <p>c) In a Hardy-Weinberg population, if \\(\\frac{1}{4}\\) of individuals show the recessive phenotype, what fraction of the population is heterozygous?</p>`,
                "answer": `<p>a) Calculating R allele frequency:</p>
                <p>Total plants: 600</p>
                <p>Total alleles: 600 × 2 = 1200 (each plant has 2 alleles)</p>
                <p>R alleles: RR plants contribute 150 × 2 = 300 R alleles</p>
                <p>Rr plants contribute 300 × 1 = 300 R alleles</p>
                <p>Total R alleles: 300 + 300 = 600</p>
                <p>Frequency of R: \\(\\frac{600}{1200} = \\frac{1}{2}\\)</p>
                
                <p>b) Recessive allele frequency:</p>
                <p>Allele frequencies must sum to 1</p>
                <p>If frequency of A = \\(\\frac{3}{5}\\)</p>
                <p>Then frequency of a = \\(1 - \\frac{3}{5} = \\frac{5}{5} - \\frac{3}{5} = \\frac{2}{5}\\)</p>
                
                <p>c) Hardy-Weinberg calculation:</p>
                <p>If \\(\\frac{1}{4}\\) show recessive phenotype (aa), then q² = \\(\\frac{1}{4}\\)</p>
                <p>So q = \\(\\frac{1}{2}\\) (frequency of a allele)</p>
                <p>And p = \\(1 - \\frac{1}{2} = \\frac{1}{2}\\) (frequency of A allele)</p>
                <p>Heterozygous frequency = 2pq = 2 × \\(\\frac{1}{2}\\) × \\(\\frac{1}{2}\\) = \\(\\frac{1}{2}\\)</p>`
            },
            {
                "category": "engineering",
                "title": "Civil Engineering: Slope and Grade",
                "content": `<p>Engineers use rational numbers to express slopes, grades, and ratios in construction and design.</p>
                <p>a) A road rises 3 meters over a horizontal distance of 40 meters. Express the grade as a simplified fraction and as a percentage.</p>
                <p>b) A wheelchair ramp must have a maximum slope of 1:12. If the ramp needs to reach a height of 75 cm, what is the minimum horizontal length required?</p>
                <p>c) A drainage pipe needs a minimum slope of \\(\\frac{1}{8}\\) inch per foot. Over a 24-foot run, what is the total drop in inches?</p>`,
                "answer": `<p>a) Road grade calculation:</p>
                <p>Grade = \\(\\frac{\\text{Rise}}{\\text{Run}} = \\frac{3}{40}\\)</p>
                <p>This fraction is already in simplest form</p>
                <p>As a percentage: \\(\\frac{3}{40} \\times 100\\% = \\frac{300}{40}\\% = 7.5\\%\\)</p>
                
                <p>b) Wheelchair ramp calculation:</p>
                <p>Maximum slope: 1:12 means \\(\\frac{\\text{Rise}}{\\text{Run}} = \\frac{1}{12}\\)</p>
                <p>Height needed: 75 cm</p>
                <p>\\(\\frac{75}{\\text{Run}} = \\frac{1}{12}\\)</p>
                <p>Run = 75 × 12 = 900 cm = 9 meters</p>
                <p>Minimum horizontal length: 9 meters</p>
                
                <p>c) Drainage pipe drop:</p>
                <p>Slope: \\(\\frac{1}{8}\\) inch per foot</p>
                <p>Total length: 24 feet</p>
                <p>Total drop: 24 × \\(\\frac{1}{8}\\) = \\(\\frac{24}{8}\\) = 3 inches</p>`
            },
            {
                "category": "financial",
                "title": "Banking: Interest Rate Calculations",
                "content": `<p>Financial institutions use rational numbers for precise interest calculations and payment schedules.</p>
                <p>a) A savings account offers \\(\\frac{7}{4}\\)% annual interest. Express this as a decimal and calculate the interest on €2,400 for one year.</p>
                <p>b) A loan payment is split as follows: \\(\\frac{3}{8}\\) goes to principal, \\(\\frac{5}{12}\\) to interest, and the rest to insurance. What fraction goes to insurance?</p>
                <p>c) If monthly payments are €840 and \\(\\frac{2}{5}\\) goes to principal, how much principal is paid over 6 months?</p>`,
                "answer": `<p>a) Interest calculation:</p>
                <p>Interest rate: \\(\\frac{7}{4}\\% = 1.75\\%\\) = 0.0175 as decimal</p>
                <p>Interest on €2,400: €2,400 × 0.0175 = €42</p>
                <p>Alternatively: €2,400 × \\(\\frac{7}{400}\\) = \\(\\frac{16,800}{400}\\) = €42</p>
                
                <p>b) Insurance fraction calculation:</p>
                <p>Principal: \\(\\frac{3}{8}\\), Interest: \\(\\frac{5}{12}\\)</p>
                <p>Find common denominator: LCD(8, 12) = 24</p>
                <p>Principal: \\(\\frac{3}{8} = \\frac{9}{24}\\)</p>
                <p>Interest: \\(\\frac{5}{12} = \\frac{10}{24}\\)</p>
                <p>Total for principal and interest: \\(\\frac{9}{24} + \\frac{10}{24} = \\frac{19}{24}\\)</p>
                <p>Insurance: \\(1 - \\frac{19}{24} = \\frac{5}{24}\\)</p>
                
                <p>c) Principal over 6 months:</p>
                <p>Monthly principal: €840 × \\(\\frac{2}{5}\\) = \\(\\frac{1,680}{5}\\) = €336</p>
                <p>Over 6 months: €336 × 6 = €2,016</p>`
            },
            {
                "category": "creative",
                "title": "Photography: Aspect Ratios and Exposure",
                "content": `<p>Photographers use rational numbers for aspect ratios, shutter speeds, and aperture settings.</p>
                <p>a) A photo has an aspect ratio of 3:2. If the width is 4,500 pixels, what is the height?</p>
                <p>b) The exposure triangle shows shutter speed doubling: \\(\\frac{1}{125}\\)s, \\(\\frac{1}{250}\\)s, \\(\\frac{1}{500}\\)s. If you change from \\(\\frac{1}{250}\\)s to \\(\\frac{1}{60}\\)s, by what factor does the exposure time increase?</p>
                <p>c) An f-stop sequence includes f/2.8, f/4, f/5.6. Each step halves the light. If f/2.8 lets in 16 units of light, how much light does f/8 let in?</p>`,
                "answer": `<p>a) Height calculation from aspect ratio:</p>
                <p>Aspect ratio 3:2 means \\(\\frac{\\text{Width}}{\\text{Height}} = \\frac{3}{2}\\)</p>
                <p>Width = 4,500 pixels</p>
                <p>\\(\\frac{4,500}{\\text{Height}} = \\frac{3}{2}\\)</p>
                <p>Height = 4,500 × \\(\\frac{2}{3}\\) = \\(\\frac{9,000}{3}\\) = 3,000 pixels</p>
                
                <p>b) Exposure time change:</p>
                <p>From \\(\\frac{1}{250}\\)s to \\(\\frac{1}{60}\\)s</p>
                <p>Factor = \\(\\frac{1/60}{1/250} = \\frac{1}{60} \\times \\frac{250}{1} = \\frac{250}{60} = \\frac{25}{6}\\)</p>
                <p>The exposure time increases by a factor of \\(\\frac{25}{6}\\) ≈ 4.17</p>
                
                <p>c) Light through f/8:</p>
                <p>f/2.8 → f/4 → f/5.6 → f/8 (3 stops)</p>
                <p>Each stop halves the light</p>
                <p>Light at f/8 = 16 × \\(\\frac{1}{2}\\) × \\(\\frac{1}{2}\\) × \\(\\frac{1}{2}\\)</p>
                <p>= 16 × \\(\\frac{1}{8}\\) = 2 units of light</p>`
            }
        ]
    };
    MathQuestionModule.render(rationalNumbersContent, 'rational-numbers-identity-container');
});
</script>

### Key Takeaways

```{important}
1. **Rational numbers** ($\mathbb{Q}$) are numbers that can be expressed as $\frac{a}{b}$ where $a, b \in \mathbb{Z}$ and $b \neq 0$
2. **Every integer is rational**: Any integer $n$ can be written as $\frac{n}{1}$
3. **Equivalent fractions** represent the same value: $\frac{2}{3} = \frac{4}{6} = \frac{6}{9}$
4. **Simplification** means dividing numerator and denominator by their GCD
5. **Operations require common denominators** for addition and subtraction
6. **Multiplication is straightforward**: Multiply numerators and denominators separately
7. **Division means multiply by the reciprocal**: $\frac{a}{b} \div \frac{c}{d} = \frac{a}{b} \times \frac{d}{c}$
8. **Rational numbers are dense**: Between any two rationals, there's always another rational
```