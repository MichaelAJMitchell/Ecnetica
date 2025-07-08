# Polynomial Division

Polynomial division is a fundamental algebraic technique used to divide one polynomial by another. It's similar to long division with numbers but applied to algebraic expressions.

## Methods of Polynomial Division

### 1. Long Division Method

The long division method for polynomials follows these steps:
1. Arrange both polynomials in descending order of powers
2. Divide the first term of the dividend by the first term of the divisor
3. Multiply the divisor by this quotient term
4. Subtract the result from the dividend
5. Repeat until the degree of the remainder is less than the degree of the divisor

### 2. Synthetic Division

Synthetic division is a shortcut method that works when dividing by a linear polynomial of the form $(x - a)$.

## Detailed Example: Long Division

Let's divide $2x^3 + 3x^2 - 5x + 7$ by $x + 2$.

**Step 1:** Set up the division
```
                    
x + 2 | 2x³ + 3x² - 5x + 7
```

**Step 2:** Divide the first terms: $\frac{2x^3}{x} = 2x^2$
```
                2x²
        ________________
x + 2 | 2x³ + 3x² - 5x + 7
        2x³ + 4x²
        __________
             -x²
```

**Step 3:** Bring down the next term and repeat: $\frac{-x^2}{x} = -x$
```
                2x² - x
        ________________
x + 2 | 2x³ + 3x² - 5x + 7
        2x³ + 4x²
        __________
             -x² - 5x
             -x² - 2x
             ________
                 -3x
```

**Step 4:** Continue: $\frac{-3x}{x} = -3$
```
                2x² - x - 3
        ____________________
x + 2 | 2x³ + 3x² - 5x + 7
        2x³ + 4x²
        __________
             -x² - 5x
             -x² - 2x
             ________
                 -3x + 7
                 -3x - 6
                 _______
                     13
```

**Result:** 
$$\frac{2x^3 + 3x^2 - 5x + 7}{x + 2} = 2x^2 - x - 3 + \frac{13}{x + 2}$$

## The Division Algorithm

For polynomials $f(x)$ (dividend) and $g(x)$ (divisor) where $g(x) \neq 0$:

$$f(x) = g(x) \cdot q(x) + r(x)$$

Where:
- $q(x)$ is the quotient
- $r(x)$ is the remainder
- degree of $r(x) <$ degree of $g(x)$

## Practice Problems

1. Divide $x^3 - 2x^2 + 5x - 6$ by $x - 1$
2. Divide $3x^4 + 2x^3 - x + 4$ by $x^2 + 1$
3. Use synthetic division to divide $x^3 + 4x^2 - 3x - 12$ by $x + 3$

## Applications

Polynomial division is essential for:
- Finding factors of polynomials
- Simplifying rational expressions
- Solving polynomial equations
- Partial fraction decomposition
- Determining asymptotes of rational functions

## Connection to Other Topics

- **Factor Theorem**: If $f(a) = 0$, then $(x - a)$ is a factor of $f(x)$
- **Remainder Theorem**: When $f(x)$ is divided by $(x - a)$, the remainder is $f(a)$
- **Rational Functions**: Understanding polynomial division helps analyze rational function behavior