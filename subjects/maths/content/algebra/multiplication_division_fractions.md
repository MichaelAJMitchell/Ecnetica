# Multiplication and Division of Algebraic Fractions

## Introduction

### Theory

Multiplying and dividing algebraic fractions is actually simpler than addition and subtraction—you don't need common denominators! These operations follow straightforward rules that mirror those for numerical fractions, with the added benefit that you can often simplify before multiplying.

## Multiplication of Algebraic Fractions

### Theory

#### The Basic Rule

To multiply fractions, multiply the numerators together and multiply the denominators together:

$$\frac{a}{b} \times \frac{c}{d} = \frac{a \times c}{b \times d} = \frac{ac}{bd}$$

#### The Smart Approach: Cancel First, Multiply Later

The key to efficient multiplication is to **cancel common factors before multiplying**. This keeps numbers smaller and reduces the need for simplification later.

```{tip}
Always look for opportunities to cancel before multiplying. This is not just a time-saver—it also reduces the chance of arithmetic errors with large expressions.
```

### Application

#### Example 1: Basic Multiplication

Multiply: $\frac{x}{3} \times \frac{6}{x^2}$

**Method 1** (multiply first, then simplify):

$$\frac{x}{3} \times \frac{6}{x^2} = \frac{6x}{3x^2} = \frac{2}{x}$$

**Method 2** (cancel first—more efficient):

$$\frac{x}{3} \times \frac{6}{x^2} = \frac{\cancel{x}}{3} \times \frac{6}{x^{\cancel{2}}} = \frac{1}{3} \times \frac{6}{x} = \frac{6}{3x} = \frac{2}{x}$$

Both methods work, but canceling first is cleaner!

#### Example 2: Factoring Before Multiplying

Multiply: $\frac{x^2-4}{x+3} \times \frac{x+3}{x-2}$

**Step 1**: Factor where possible:

$$\frac{(x+2)(x-2)}{x+3} \times \frac{x+3}{x-2}$$

**Step 2**: Cancel common factors:
- $(x+3)$ appears in numerator and denominator
- $(x-2)$ appears in numerator and denominator

$$\frac{(x+2)\cancel{(x-2)}}{\cancel{x+3}} \times \frac{\cancel{x+3}}{\cancel{x-2}} = x+2$$

**Domain**: $x \neq -3, x \neq 2$ (from the original fractions)

```{note}
Even though the final answer is simply $x+2$, the domain restrictions from the original fractions still apply. This is crucial for exam success!
```

#### Example 3: Multiple Fractions

Multiply: $\frac{x^2-1}{x} \times \frac{2x}{x+1} \times \frac{3}{x-1}$

**Step 1**: Factor all expressions:

$$\frac{(x+1)(x-1)}{x} \times \frac{2x}{x+1} \times \frac{3}{x-1}$$

**Step 2**: Write as one fraction:

$$\frac{(x+1)(x-1) \times 2x \times 3}{x \times (x+1) \times (x-1)}$$

**Step 3**: Cancel common factors:

$$\frac{\cancel{(x+1)}\cancel{(x-1)} \times 2\cancel{x} \times 3}{\cancel{x} \times \cancel{(x+1)} \times \cancel{(x-1)}} = 2 \times 3 = 6$$

## Division of Algebraic Fractions

### Theory

#### The Basic Rule

To divide by a fraction, multiply by its reciprocal:

$$\frac{a}{b} \div \frac{c}{d} = \frac{a}{b} \times \frac{d}{c} = \frac{ad}{bc}$$

**Remember**: "Dividing by a fraction = multiplying by its flip"

```{warning}
A common error is to flip the wrong fraction. Always flip the fraction you're dividing BY (the second one), not the fraction you're dividing.
```

### Application

#### Example 4: Simple Division

Divide: $\frac{x^2}{4} \div \frac{x}{2}$

**Step 1**: Rewrite as multiplication by the reciprocal:

$$\frac{x^2}{4} \div \frac{x}{2} = \frac{x^2}{4} \times \frac{2}{x}$$

**Step 2**: Cancel and multiply:

$$= \frac{x^{\cancel{2}}}{4} \times \frac{2}{\cancel{x}} = \frac{x}{4} \times \frac{2}{1} = \frac{2x}{4} = \frac{x}{2}$$

#### Example 5: Division with Factoring

Divide: $\frac{x^2-9}{x^2+x} \div \frac{x-3}{x}$

**Step 1**: Factor and flip:

$$\frac{(x+3)(x-3)}{x(x+1)} \div \frac{x-3}{x} = \frac{(x+3)(x-3)}{x(x+1)} \times \frac{x}{x-3}$$

**Step 2**: Cancel common factors:

$$= \frac{(x+3)\cancel{(x-3)}}{\cancel{x}(x+1)} \times \frac{\cancel{x}}{\cancel{x-3}} = \frac{x+3}{x+1}$$

**Domain**: $x \neq 0, x \neq -1, x \neq 3$

#### Example 6: Complex Division

Simplify: $\frac{\frac{x^2-4}{x}}{\frac{x+2}{x^2}}$

This is a division of two fractions. We can rewrite it as:

$$\frac{x^2-4}{x} \div \frac{x+2}{x^2}$$

**Step 1**: Factor and flip:

$$\frac{(x+2)(x-2)}{x} \times \frac{x^2}{x+2}$$

**Step 2**: Cancel:

$$= \frac{\cancel{(x+2)}(x-2)}{\cancel{x}} \times \frac{x^{\cancel{2}}}{\cancel{x+2}} = (x-2) \times x = x(x-2) = x^2-2x$$

## Mixed Operations

### Theory

When combining multiplication and division, work from left to right, converting each division to multiplication by the reciprocal.

### Application

#### Example 7: Mixed Operations

Simplify: $\frac{x}{x-1} \times \frac{x^2-1}{x^2} \div \frac{x+1}{x}$

**Step 1**: Convert division to multiplication:

$$\frac{x}{x-1} \times \frac{x^2-1}{x^2} \times \frac{x}{x+1}$$

**Step 2**: Factor:

$$\frac{x}{x-1} \times \frac{(x+1)(x-1)}{x^2} \times \frac{x}{x+1}$$

**Step 3**: Combine into one fraction:

$$\frac{x \times (x+1)(x-1) \times x}{(x-1) \times x^2 \times (x+1)}$$

**Step 4**: Cancel:

$$\frac{\cancel{x} \times \cancel{(x+1)}\cancel{(x-1)} \times x}{\cancel{(x-1)} \times x^{\cancel{2}} \times \cancel{(x+1)}} = \frac{x}{x} = 1$$

**Domain**: $x \neq 0, x \neq 1, x \neq -1$

## Special Techniques and Patterns

### Technique 1: Recognizing Conjugates

When you see expressions like $(a+b)$ and $(a-b)$, their product is $a^2-b^2$.

**Example**: $\frac{x+\sqrt{3}}{x-\sqrt{3}} \times \frac{x-\sqrt{3}}{x+\sqrt{3}} = \frac{(x+\sqrt{3})(x-\sqrt{3})}{(x-\sqrt{3})(x+\sqrt{3})} = 1$

### Technique 2: Powers of Fractions

Remember that $\left(\frac{a}{b}\right)^n = \frac{a^n}{b^n}$

**Example**: $\left(\frac{x-1}{x+1}\right)^2 = \frac{(x-1)^2}{(x+1)^2}$

### Technique 3: Negative Exponents

Recall that $x^{-n} = \frac{1}{x^n}$, so:

$$\frac{x^{-2}}{y^{-3}} = \frac{1/x^2}{1/y^3} = \frac{1}{x^2} \times \frac{y^3}{1} = \frac{y^3}{x^2}$$

## Common Mistakes to Avoid

### Mistake 1: Canceling Addition/Subtraction

❌ **Wrong**: $\frac{x+2}{x} = 2$

✓ **Correct**: $\frac{x+2}{x} = \frac{x}{x} + \frac{2}{x} = 1 + \frac{2}{x}$

Only factors can be canceled, not terms!

### Mistake 2: Forgetting to Flip When Dividing

❌ **Wrong**: $\frac{a}{b} \div \frac{c}{d} = \frac{ac}{bd}$

✓ **Correct**: $\frac{a}{b} \div \frac{c}{d} = \frac{a}{b} \times \frac{d}{c} = \frac{ad}{bc}$

### Mistake 3: Domain Restrictions

Even if factors cancel, the original restrictions remain.

If you simplify $\frac{x^2-1}{x-1}$ to $x+1$, you must still note that $x \neq 1$.

## Problem-Solving Strategy

1. **Factor everything first** - This reveals cancelation opportunities
2. **Convert division to multiplication** - Flip the divisor
3. **Cancel before multiplying** - This keeps expressions manageable
4. **State domain restrictions** - Include all values that make any denominator zero
5. **Check your answer** - Substitute a simple value to verify

```{tip}
When checking your work, choose a simple test value (like $x = 2$ or $x = 0$) that doesn't violate any domain restrictions. Evaluate both the original expression and your answer—they should give the same result.
```

## Applications

Multiplication and division of algebraic fractions appear in:
- **Rate problems**: Distance/time, work rates, flow rates
- **Physics formulas**: Resistance in parallel circuits, lens equations
- **Economics**: Compound interest, depreciation formulas
- **Calculus**: Derivative and integration techniques

## Summary

For multiplication:
- Multiply numerators and denominators
- Factor and cancel first for efficiency
- Watch for domain restrictions

For division:
- Flip the second fraction and multiply
- Remember: "keep, change, flip"
- Apply the same factoring and canceling techniques

These operations are generally easier than addition/subtraction because you don't need common denominators—just factor, cancel, and multiply!