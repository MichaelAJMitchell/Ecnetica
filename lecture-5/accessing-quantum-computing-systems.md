---
title: Accessing Quantum Computing Systems
jupytext:
    formats: md:myst
    text_representation:
        extension: .md
        format_name: myst
kernelspec:
    display_name: Python 3
    language: python
    name: python3
mystnb:
    render_markdown_format: myst
---

(lecture-5)=
# Lecture 5: Accessing Quantum Computing Systems

```{warning} These lecture notes are a work in progress and are not a replacement for watching the lecture video, it's intended to be a supplementary reading after watching the lecture 
```


## Introduction
In this lecture we touch upon various ways in which you can access quantum computing systems.

Hello, and welcome to QPCC. In this module we will discuss how to access quantum computing systems. We will begin by going over the different ways in which quantum programs can be executed, namely in a remote or local environment and also on a quantum software simulator or on actual quantum hardware. This prefaces how a user might want to access a quantum system according to their circumstances. We will then discuss how to access quantum systems, in particular by looking at local systems, commercial quantum computing and publicly-funded quantum systems. ​

​

Our learning outcomes for the module are to understand the difference between quantum hardware and software simulators, the accessing of quantum computers and the current landscape of public and commercial quantum computing systems.​


## Executing Quantum Programs

In lecture 3, we learnt about some building blocks of quantum operations similar to classical one, known normally as gates. We learnt the quantum versions of `gates` similar to classical one. One can buid a `quantum program` using a combination of these quantum gates. Building a useful combination that can provide solution to a given problem requires a combination of art and craft, which is essentially programming.

Here in the similar spirit, we go through a discussion on classical programming, to set the stage for learning quantum programming. Consider the following simple example -

### What are Classical Programs

```{code-cell}
import numpy as np
import matplotlib.pyplot as plt

x = np.random.random(30000)
x, y, _ = plt.hist(x, bins=100)
plt.xlabel("x")
plt.ylabel("Histogram of x")
plt.show()
```

A classical program is a set of instructions for a classical computer to execute. ​Classical programs are not written in a way that takes advantage of quantum hardware, but rather with classical hardware in mind.​

Take for example the following program which is written in the programming language Python and uses the popular scientific library Numpy. Here we generate a set of random integers between zero and fifteen inclusive, a random number generator program. And we can see the result plotted in this histogram. We should note that no quantum computing paradigms or hardware are used in the execution of this program. This program is entirely executed using classical paradigms of computation on classical hardware. And this will be the distinguishing factor between a classical and a quantum program.​

### What are Quantum Programs

So what is a quantum program?​

- A quantum program is a set of instructions for a quantum computer to execute​
- A quantum program generally takes advantage of the various benefits a quantum computer maintains in contrast to classical computers, although this is not strictly necessary. ​

Here we see a similar random number generator to the previous classical version, however there are some differences. Although we attain essentially the same result, a set of random numbers between zero and sixteen, the programs are executed in a different manner and use different techniques to achieve this result. The quantum program uses  the quantum mechanical properties of superposition and measurement to attain random numbers so long as it is executed on quantum hardware, while the classical uses pseudo-random methods of number generation. The quantum program can also be executed on a classical software simulator and this case would inherit the pseudo-random nature of the classical machine. ​​

We also see that the quantum program can be represented by a quantum circuit as shown on the left. The quantum program shown here is again written in python and uses the popular Qiskit library.

```python
import qiskit
size = 4
qc = qiskit.QuantumCircuit(size, size)
for i in range(size):
    qc.h(i)
qc.measure_all()
```


### Executing Quantum Programs on Quantum Hardware

- Advantages
    - Access the full potential of QC
        - Superposition
        - Entanglement
- Disadvantages
    - Current Hardware constraints
        - Noise
        - Low number of Qubits
        - Low circuit depths
    - Remote access only
    - Availability

The previous slide begs the question, if we can simulate quantum programs on classical machine then what is the point in using quantum hardware. Lets take a look at some advantages and disadvantages of using quantum hardware.​

​​
```{admonition} Noise
:class: tip
Physical qubits experience noise and decoherence, resulting in computational errors. This problem also amplifies as we attempt to use more qubits and so ​this limits the number of qubits you can use​, and the circuit depth of the program you are implementing​.
```
