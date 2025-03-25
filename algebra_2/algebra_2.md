---
title: Algebra 2
layout: post
---

(algebra_2)=
# Algebra 2

## Linear Equations Revision

In order to make the jump cleanly to quadratic equations, it’s worth giving some
time to go over linear equations briefly.
Linear equations are a class of polynomial[^1] equations that either come in
or can be rearranged to have the **standard form**:  

\begin {gather}
x + b = 0 
\end {gather}

[^1]:_Extra Learning_: Properly, polynomials are equations of the form $a_n x^n + a_{n-1} x^{n-1} + \dots + a_1 x + a_0$, where
        the $a$’s are constants and the $n$-based numbering is used to nicely match a constant to its $x$
        term. What this really means is that if you take a bunch of x’s, put them to various powers,
        multiply them each by a different number, and then add them together, then what you get
        at the end is called a polynomial. Any definition that complicates this more is an effort by
        mathematicians to make the definition more general (more general = more widely applicable
        = more useful), but we don’t need to go any more general than this for now.



where $a$ and $b$ can be any constant numbers, and $x$ is the variable, or what we’re
solving for[^2]. Once in this form, it takes only a little manipulation to solve:
\begin{align} 
ax &= -b \\ x &= -b/a 
\end{align}

[^2]: Don’t get hung up on the actual letter itself, you could technically use any letter you like.

We subtracted $b$ from both sides, then divided by $a$ to get $x$ on its own on
one side. Linear equations are called that because, when graphed, they are a
straight line. They may also be called “first order equations” or“equations of
degree 1”, both because the highest power on $x$ is 1, since $x$ in the equation
could also be written as $x^1$. Let’s do one quick example and then move on.



### Example 1.

\begin {gather*} 3x+9=3 \end {gather*}  

To get this into the standard form of Eq. 1, and then solve, we do some manipulation:

\begin{align}
3x+9 = 3 \quad & \text{Not in standard form}\\
3x +9  -3 &= 3 - 3 \\
3x + 6 = 0 \quad& \text{Now in standard form}\\
x = - 6/3& = -2
\end{align} 

You may have spotted that we took the long way round here - we didn’t really
have to bring it to standard form first - and you would be correct. For a linear
equation, we could have simply went;

\begin{align}
3x+9&=3\\
3x = & 3 - 9\\
3x = & -6\\
x = - 6/3& = -2
\end{align} 

if all we were interested in was what x was in this particular case. However,
for more advanced problems like quadratic equations, moving to the quadratic
equation standard-form is almost always the first step to solving them. This
will be clearer later.



## Quadratic Equations and their Form
Quadratic equations, much like linear equations, are a special class of polynomial equations that have the following standard form:

$ax^2 + bx + c = 0$

where $a$, $b$, $c$ are numbers and $x$ is again, the variable. Like linear equations, they might need to be moved around to get to this form. You'll notice that there's two $x$ terms - an $x^2$ and an $x$. It's the presence of the $x^2$ that makes this equation quadratic - the **highest** power of the $x$ is 2.

The main reason we want quadratic equations in this standard form is that this is the starting point for solving them (the secondary reason is that this form contains some useful graphical information). Also, if you can convince another equation to shift into quadratic form without breaking any mathematical rules, you can also apply quadratic techniques to solve equations you otherwise couldn't.

### Example 1
Is the following a quadratic equation?

$2x(x+3) = -x$

All we need to do here is multiply out the brackets and bring everything to one side:

\begin{gather*}2x(x+3) = -x\\
2x(x) + 2x(3) = -x\\
2x^2 + 6x = -x\\
2x^2 + 7x = 0\end{gather*} 

and we have a quadratic where $a=2$, $b=7$ and $c=0$.

### Example 2
Is the following a quadratic equation?

$x^4 + x^2 + 1 = 0$

Since the highest power on $x$ isn't $2$, it's $4$, technically, this isn't a quadratic. But we can choose a new variable, say, $t$, and say that:

$t = x^2$

If we then substitute it in, noting that $x^4=(x^2)(x^2)$:

\begin{gather*}x^4 + x^2 + 1 = 0\\
(x^2)(x^2) + x^2 + 1 = 0\\
(t)(t) + (t) + 1 = 0\\
t^2 + t + 1 = 0\end{gather*} 

and suddenly, we get a quadratic form that we can solve, where $a=1$, $b=1$ and $c=1$. Once we find an answer for $t$, then we work backwards from $t=x^2$ to find $x$. This is a common trick they pull in the Leaving Cert that's worth getting comfortable with.

### Example 3
$\tan^2(x) + \tan(x) + 2 = 0$

This is quite similar to the last question. We choose (maybe after some trial and error) to let $t = \tan(x)$, and then substitute in:

\begin{gather*}\tan^2(x) + \tan(x) + 2 = 0\\
\tan(x)\tan(x) + \tan(x) + 2 = 0\\
(t)(t) + t + 2 = 0\\
t^2 + t + 2 = 0\end{gather*} 

and now we have a quadratic again, where $a=1$, $b=1$ and $c=2$.

### Example 4
\begin{gather}
\tan(x) + x^2 + 5 = 0
\end{gather}

The highest power on the $x$ is $2$, but this is not actually a quadratic equation. We can't just let $t = \tan(x)$ again, because we'll end up with:

\begin{gather}
\tan(x) + x^2 = 0
t + x^2 = 0
\end{gather}

Which doesn't get us very far, since now we have 2 unknowns and not enough information to find either. Try all you want, but there's no real way to get this into a quadratic form since $\tan(x)$ is a trigonometric function - not a constant multiplying $x$, which is what we require of our polynomial coefficients.

### Example 5
\begin{gather}
x^2\sin(\frac{\pi}{3}) + x = 0
\end{gather}

In this case, despite $\sin$ showing up, this is a quadratic, since (and you can type this into your calculator to check) $\sin(\frac{\pi}{3})$ is just a number (0.866, a constant). In this case, it meets the requirements for a quadratic expression - here we have $a=\sin(\frac{\pi}{3})$, $b=1$ and $c=0$.

## Factorising by Inspection

Factorising by inspection is the most straightforward way of solving quadratic equations. Factorisation is the process of splitting a number or an algebraic expression into a product of terms, doing it "by inspection" is basically us hoping that we can spot those terms that form the right product. The downside to this method is that not all quadratic equations have nice enough $a$, $b$, $c$ to be able to have a simple factorisation we can spot - if you see a fraction or a surd you're almost always better off using other methods.

The way to do this is to break the equation apart into two brackets, which multiply together to give $0$ (since in the standard from, the equations ends with "$=0$"). We know that anything multiplied by $0$ is $0$, so if the two brackets get multiplied together, we can conclude that one of the brackets must be $0$.

\begin{gather}
(x+...)(x+...)=0
\end{gather}

Most learn how to do this type of factorising for Junior Cert and everyone has their own methods - you should stick to what you're most comfortable with. The thing all methods have in common is that you can guess at the ingredients by looking at the finished product and then do a little trial-and-error to get it right.

### Example
Take for example:

\begin{gather}
x^2 + 2x - 8=0
\end{gather}

We can see that there's an $x^2$, so we need to make sure there's an $x$ in each bracket to multiply with each other. Similarly, we'll need two numbers that will multiply with each other to give us the $-8$ at the end. So, we've restricted the possible bracket combinations significantly by noticing these two things.

The pairs of numbers that multiply to give $8$ are $1$ and $8$, and $2$ and $4$ (we can take care of the minus part of the $8$ by putting a minus in front of either number in a pair).

We can either:
1. Try to put both of these into the bracket pairs we're building and check if they give us the right method, or 
2. Notice that we can build the $2$ part of the $2x$ middle term by using one pair specifically: $4-2=2$

This points to using them to build our brackets:

\begin{gather}
(x+4)(x-2) = 0
x(x-2)+4(x-2) = 0
x^2 -2x +4x -8 = 0
x^2 +2x -8 = 0
\end{gather}

which is what we want. 

## Solving the Factored Equation

If we go on to solve this, having factorised:

\begin{gather}
(x+4)(x-2) = 0
\end{gather}

Either:
* $x + 4 = 0$
    * Therefore $x = -4$
* Or $x - 2 = 0$
    * Therefore $x = +2$

We can verify these solutions:

* For $x=-4$: $(-4)^2 + 2(-4)-8=16-8-8=0$
* For $x=2$: $(2)^2 + 2(2) - 8 = 4+4-8=0$

Either one of these solutions make the value of the quadratic expression $x^2 + 2x -8$ go to $0$, which is what we want since the equation ends with $=0$. $x=2$ and $x=-4$ are known as the **roots** of $x^2 +2x-8$.


Sometimes, the $a$ coefficient multiplying the $x^2$ term will not just be $1$. This is a little trickier, because it means we have a wider amount of combinations of brackets to consider. 

While your Junior Cert teacher will likely have given a technique to deal with these $a\ne 1$ quadratic equations, but if not don't worry; you can skip right to the solution without factorisation by inspection via the "quadratic formula", see Section on Quadratic Formula.

## Graphical Solutions

If you look at what we've been solving for so far, we've been searching for values of $x$ that can make a quadratic expression become $0$ - there are at most two $x$ values that can bring this about for a given quadratic expression. However, we can start putting any values of $x$ into:

\begin{gather}
ax^2 + bx + c = ?
\end{gather}

and just keep track of what comes out. This idea of feeding an "input" and getting an "output" is precisely what we come across when dealing with functions - which is why you'll see that question mark replaced with $f(x)$.


If we write down every value of $x$ we put in, and then we write down every value we get out, and then mark those pairs of input/output on an $x$-$y$ graph, we'll get out a nice shape called a "parabola". If we do this, the convention is to call the "?" in the equation above $y$ to reflect the idea that the output is on the y-axis of the graph. This parabola shape on a graph is a key feature of quadratic equations. 


But all that work we did finding the $x$ values at $y=0$ previously wasn't for nothing. If you plot any parabola, you'll find that the places where it crosses the $x$-axis are exactly the solutions we found earlier. This is because at every single spot along an $x$-axis, $y=0$. So if $y=0$, and we solve the equation, what we're really doing is solving the equation in standard form.

Key points about x-intercepts:
* They can be used as a method to solve any quadratic equation
* They are the points where the curve "intercepts" the x-axis
* They represent the solutions to the quadratic equation


If it just so happens that the parabola only touches the $x$-axis at a single point - that is it touches the $x$-axis as it turns - then the two solutions to the equation are both the same number. This point as it turns is sometimes called the "vertex" or the "turning point".


You may notice that it is entirely possible to have a parabola in such a way that it never touches the $x$-axis. Without spoiling too much of a future chapter, these equations have solutions that are "not real", i.e., you need complex numbers to understand account for their solutions, which you will see later in the course.

## Completing the Square


Besides standard form, there are a few other forms that you can move quadratic equations into. One was the factorised form. Another, which we'll do here, is the completed square form. It looks like:

\begin{gather}
f(x + d)^2 + e
\end{gather}

where $f$, $d$ and $e$ are constants. This form is useful for giving us information about the shape and location of the parabola when graphed. Completing the square is also the method used to derive the "minus b" formula - a derivation which is on the syllabus but has never been asked!

*Sidenote*: for the Leaving Cert exam, however, you do need to know how to *do* the method of completing the square, as there will be questions where you'll be asked to solve equations specifically by completing the square.

The general method relies on guessing $d$ to give us the right $a$ and $b$ terms from the standard form, then adding or subtracting constants until we match our standard form constant $c$. This is best shown through examples:

### Example 1

Take for example the following:

\begin{gather}
x^2 + 3x - 4
\end{gather}

We want to get this to completed square form, meaning we will have a $(x + d)^2$ when we finish. We want to choose $d$ so that we can get out the $+3x$ term. Maybe the most straightforward way to see what $d$ should be is to multiply out:

\begin{align*}
5(x+d)^2 &= 5x^2 + 10dx + 5d^2 \\
\implies 10dx &= 2x \\
\implies d &= \frac{2}{10}
\end{align*} 

All we need to do is check that we have the $x^2$ term we want before we move on - and sure enough:

\begin{gather}
(x+\frac{3}{2})^2 = x^2 + 3x + \frac{9}{4}
\end{gather}

This means that we let $f = 1$. We've established what $d$ must be, and because the $e$ is going to be just a constant, we don't need to worry about it affecting the $bx$ term - $d$ is the only thing that controls $b$. Now, using $d=\frac{3}{2}$, let's pay attention to the extra constant term spat out during squaring:

\begin{align*}
(x+d)^2 &= \left(x + \frac{3}{2}\right)^2 \\
&= x^2 + 3x + \frac{9}{4}
\end{align*} 

Now comes the tinkering. We're aiming for a $c=-4$, but what we have right now is a $\frac{9}{4}$. We also have the free choice of $e$. So we want to add (or subtract) numbers to get that $\frac{9}{4}$ to $-4$:

\begin{align*}
\left(x + \frac{3}{2}\right)^2 &= x^2 + 3x + \frac{9}{4} \\
\implies x^2 + 3x + \frac{9}{4} - \frac{25}{4} &= x^2 + 3x - 4
\end{align*} 

For the victory lap:

\begin{align*}
\left(x+\frac{3}{2}\right)^2 - \frac{25}{4} &= x^2 + 3x + \frac{9}{4} - \frac{25}{4} \\
                                    &= x^2 + 3x - \frac{16}{4} \\
                                    &= x^2 + 3x - 4
\end{align*} 

In other words, our completed square form and the standard form are equivalent!

### Example 2
Let's put the following in completed square form:
$5x^2 + 2x + 10$

Let's start by finding $d$:
\begin{gather}
(x+d)^2\\
x^2 + 2dx + d^2
\end{gather} 

But wait! We haven't gotten out a $5x^2$, only an $x^2$. This means we need to tinker a little extra until we can decide what $d$ is. Let's multiply across by $5$ then choose $d$:



Because we multiplied by $5$ to get the right $x^2$, that means that $f=5$. Then we substitute in for $d$ and $f$, multiply out, and decide what constants we need to add and subtract to get to the $c$ we want (thereby choosing $e$):

\begin{align*}
5\left(x+\frac{2}{10}\right)^2 &= 5x^2 + 2x + \frac{2}{10} \\
\implies 5x^2 + 2x + \frac{2}{10} + \frac{98}{10} &= 5x^2 + 2x + 10
\end{align*} 

where the $\frac{98}{10}$ is what we had to add on to get the $10$ we wanted at the end - so it is our $e$. Our completed square form is then:

\begin{gather}
5\left(x^2 + \frac{2}{10}\right)+ \frac{98}{10}
\end{gather}


## Deriving the Quadratic Formula

I mentioned previously that the completed square form can be used to derive the "minus b" formula that you've almost certainly already met at Junior Cert level. This derivation is on the syllabus but has never before been asked. We will go through it quickly before we discuss using it.

The quadratic formula we're aiming to derive is:

\begin{gather}
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
\end{gather}

And we are starting from standard form:

\begin{gather}
ax^2 + bx + c = 0
\end{gather}

The first thing we want to do is to divide by $a$ to neaten things up slightly:

\begin{gather}
x^2 + \frac{bx}{a} + \frac{c}{a} = 0
\end{gather}

We now want to put it into completed square form, so we choose $d$ of the completed square form to be $\frac{b}{2a}$, but we get an extra term at the end:

\begin{gather}
\left(x+\frac{b}{2a}\right)^2 = x^2 + \frac{b}{2a}x + \frac{b}{2a}x + \frac{b^2}{4a^2}\\
\end{gather}

Therefore we put in a $-\frac{b^2}{4a^2}$ to deal with it:

\begin{gather}
\left(x+\frac{b}{2a}\right)^2 -\frac{b^2}{4a^2} = x^2 + \frac{b}{a}x + \frac{b^2}{4a^2} - \frac{b^2}{4a^2} = x^2 + \frac{b}{a}x\\
\end{gather}

Comparing this with our target equation, we're almost there, we just need to add a $c/a$ term:

\begin{gather}
\left(x+\frac{b}{2a}\right)^2 - \frac{b^2}{4a^2} + \frac{c}{a} = x^2 + \frac{b}{a} + \frac{c}{a} = 0
\end{gather}

And now we do some algebra to get the $x$ on its own:

\begin{align*}
\left(x+\frac{b}{2a}\right)^2 &= \frac{b^2}{4a^2} - \frac{c}{a} \\
x+\frac{b}{2a} &= \pm\sqrt{\frac{b^2}{4a^2} - \frac{c}{a}}
\end{align*} 

And then continue to move things around to get things in a nicer form:

\begin{align*}
2ax + b &= \pm 2a \sqrt{\frac{b^2}{4a^2} - \frac{c}{a}} \\
&= \pm \sqrt{4a^2} \sqrt{\frac{b^2}{4a^2} - \frac{c}{a}} \\
&= \pm \sqrt{\frac{4a^2b^2}{4a^2} - \frac{4a^2c}{a}} \\
&= \pm \sqrt{b^2 - 4ac}
\end{align*} 

This should be beginning to look familiar now. We move the last few pieces over and end up with our quadratic formula:

\begin{align*}
2ax + b &= \pm \sqrt{b^2 - 4ac} \\
2ax &= -b \pm \sqrt{b^2 - 4ac} \\
x &= \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
\end{align*} 

The formula we just derived is **very** useful, because it allows us to jump directly to solutions for $x$ for a quadratic in $ax^2 + bx +c$ form without fiddling about with algebra. On occasion it's faster to factorise by inspection rather than go through the formula, especially if the factorisation is very obvious, but it's important to remember the quadratic formula every time there are roots to find.


## Discriminant

You may have noticed somewhere that not all our methods give answers for all quadratic equations - but you will have seen in the video series that not all parabolas hit the x-axis. When this happens, our minus-b quadratic formula ends up trying to find the square root of a negative number. Take for example this very simple problem:

\begin{gather}
x^2 + 1 = 0 \implies x = \sqrt{-1}
\end{gather}

We don't know how to take the square root of a negative number (yet!) and if we graph this, we'll notice that the parabola doesn't even touch the $x$-axis, let alone cross it twice - so do they even have solutions?

In fact, yes they do have solutions, even if not on the x-axis; the way to solve these is to extend our number line (in these cases, the real number line) to account for the square root of a negative number. This larger set of numbers is called the set of complex numbers. This will be covered in another part of your course - there's a lot of interesting things to be done in the complex number line. 

For now, what we need to know is how to tell the difference between a problem that we can solve in the real numbers and a problem that we need the complex numbers for - or, alternatively, the difference between a parabola that touches the $x$-axis or doesn't.

We do this by looking at the "discriminant", which is the part of the quadratic/minus b formula under the square root - the part that gives us problems when it's negative. In other words, the discriminant (which we will denote with $\Delta$) is:

\begin{gather}
\Delta = b^2 - 4ac
\end{gather}

By checking if $\Delta$ is positive, negative, or equal to zero, we can decide certain things about the quadratic equation:

* When $\Delta > 0$:
    * We have two real solutions to the quadratic equation
    * The parabola crosses the $x$-axis at these two values of $x$
    * There are two different $x$ values, that, when put into $f(x)$, will give us 0
    * We can use the minus b formula or plot it

* When $\Delta < 0$:
    * We have two complex solutions to the equation
    * Plotted on a graph, this means the parabola doesn't touch the $x$-axis at all
    * There are no (real) values of $x$ that, when put into $f(x)$ will give us 0
    * The best way to solve these is using the minus b formula once you learn how to handle complex numbers

* When $\Delta = 0$:
    * We have two solutions which happen to be the same
    * The parabola touches the $x$-axis only once, at the vertex
    * There is only one value of $x$ that will give us 0 when put into $f(x)$
    * This value will occur twice in a factorisation of $f(x)$


## Higher Order Polynomials

The same way that "quadratic" refers to a polynomial of degree 2, we can have polynomials of degree 3 ("cubic"), or 4 ("quartic"). When graphed, they no longer have a parabola shape, but instead have extra turns - the higher order the polynomial is, the more turns it will have. Similar rules to quadratic functions dictate how higher order polynomials look when graphed. We will briefly consider these, as they are handy for visualising functions.

1. If the degree of a function is odd, then the "arms" (the parts of the function before and after the twists and turns where the function is constantly increasing/decreasing) will go in opposite directions. If the degree is even, the arms will go in the same direction.

2. If the leading coefficient (the constant term multiplied by the highest power of $x$) is positive, then the arm on the right hand side will go up. Otherwise, it will go down. To figure out what the left hand side arm is doing, check if the degree is odd or even.

3. The $y$-intercept, as learned in linear equations, holds here too: the constant term at the end that doesn't have any $x$ multiplied by it is the $y$-intercept, and this is the point that the graph cuts the $y$-axis.

4. Substituting $-x$ for $x$ mirrors the graph about the $y$-axis. Multiplying the whole equation by $-1$ (so changing $y$ to $-y$) flips the graph about the $x$-axis.

5. Roots that appear only once are the line crossing the $x$-axis. Roots that appear twice are the line touching the $x$-axis as it turns. Roots that appear three times are the line passing through the $x$-axis but which briefly flatten as it does so (to test this: graph $y = x^3$, which has the root $x=0$ three times, to see this shape in action).

6. If you multiply a polynomial by a constant, it makes the amplitude larger by that amount i.e., it stretches the graph vertically by that amount.

7. Local minima/maxima* are the lowest/highest points on a graph in their immediate area. We want these to be "local" as the arms of polynomials can stretch on to infinity whilst constantly increasing/decreasing, so overall, the minimum/maximum would be at $\pm\infty$.

*The singular form is local minimum/maximum

## Cubic Expressions
For cubic expressions in the form:

\begin{gather}
ax^3 + bx^2 + cx + d
\end{gather}

Note: what the $a$, $b$, and $c$ are multiplied by has changed from the quadratic form, with $a$ now multiplying a cubic term.

If we take the discriminant ($\Delta = b^2 - 4ac$), we can check certain things about its roots:

* When $\Delta > 0$:
    * Three real roots
    * The line crosses the $x$-axis 3 times

* When $\Delta = 0$:
    * Three real roots but two are the same
    * The line crosses the $x$-axis once then just barely touches it as it turns

* When $\Delta < 0$:
    * One real root and two complex roots
    * The line crosses the $x$-axis once but twists and turns without approaching it again