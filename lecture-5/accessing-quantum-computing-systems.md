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

In lecture 3, we learnt about some building blocks of quantum operations similar to classical one, known normally as gates. We learnt the quantum versions of `gates` similar to classical one. One can buid a `quantum program` using a combination of these quantum gates. Building a useful combination that can provide solution to a given problem requires a combination of art and craft, which is essentially programming. Here in the similar spirit, we go through a discussion on classical programming, to set the stage for learning quantum programming. 

## What are Classical Programs

A classical program is a set of instructions for a classical computer to execute. ​Classical programs are not written in a way that takes advantage of quantum hardware, but rather with classical hardware in mind.​

Consider the following simple example -

```{code-cell}
import numpy as np              # import numpy library
import matplotlib.pyplot as plt # import the plotting library

x = np.random.random(30000)     # generate the random numbers
plt.hist(x, bins=100)           # plot the histogram
plt.xlabel("x")                 # set the x-label  |
plt.ylabel("Histogram of x")    # set the y-label  | The 'plot' thickens :-) 
plt.show()                      # display the plot |
```

The small piece of code above is a `program` written in Python programming language and uses the popular scientific library `Numpy`. The first line imports the module[^lib]/library, and the second line imports the famous plotting library `matplotlib`.
We then call the numpy function for 30000 samples of random numbers through `x = np.random.random(30000)`, that are uniformly distributed. Next four lines set the instructions to plot the distribution of these numbers. And we can see the result plotted below the input code block.
Although the underlying programs in the plotting library matplotlib and the random number genenerator from numpy are far from simple, for our purpose within the above code-block, they serve a simple purpose, of writing a two step process -

1. Generate a set of random numbers, and
2. Plot their distribution.

The two libraries that we used, contain the heavy load of complex algorithms to do a high-level task. Both of these libraries are written for our usual classical computer, and execute classical algorithm on a classical computer. 


## What are Quantum Programs

So what is a quantum program?​ Typically, a quantum program -

- is a set of instructions for a quantum computer to execute​, and
- generally takes advantage of one or more of the following:
    - quantum mechanical concepts
    - quantum gates
    - quantum simulation/dynamics

Here we see a similar random number generator to the previous classical version, however there are some differences. Although we attain essentially the same result, a set of random numbers between zero and sixteen, the programs are executed in a different manner and use different techniques to achieve this result.

The quantum program uses the quantum mechanical properties of superposition and measurement to attain random numbers so long as it is executed on quantum hardware, while the classical one uses pseudo-random methods of number generation algorithms. The quantum program can also be executed on a classical software simulator and this case would inherit the pseudo-random nature of the classical machine. ​​

Below we show how a quantum program can be represented by a quantum circuit. It is written in python and uses the popular Qiskit library.

```{code-cell}
import qiskit                   # import qiskit library
import matplotlib.pyplot as plt # plotting library
size = 4                        # number of qubits to use

qc = qiskit.QuantumCircuit(size, size) # Build the quantum circuit
for i in range(size):                  # Loop for adding Hadamard gate
    qc.h(i)
for i in range(size):                  # Loop for adding measurement
    qc.measure(i, i)
qc.draw(output='mpl', scale=1.8)       # Marmalade is served :-)
```

In the above code, we import the `qiskit` library along with matplotlib, and construct a quantum circuit with 4 qubits and 4 classical bits, through `qc = qiskit.QuantumCircuit(size, size)` . Next we add **Hadamard gates** at each qubits through a for loop.
Next we add measurement instruction for each qubit $i$ and to store the output in corresponding $i$th classical bit. The last line draws the circuit.

Now this build circuit can be executed on a quantum device, or a classical backend simulator, which pretends to be a quantum device. We run it through following -

```{code-cell}
from qiskit_aer import Aer                       # import the Aer simulation backend
from qiskit.visualization import plot_histogram  # import plotting function

sim = Aer.get_backend('aer_simulator')           # define a simulator object from Aer
job = sim.run(qc, shots=10000)                   # run circuit via simulated experiment
result = job.result()                            # extract result from job
counts = result.get_counts()                     # get the measured values on state
plot_histogram(counts, figsize=(12,8))           # dinner is ready :-) 
```
The `Aer` module is part of qiskit software ecosystem, and provides us with a few backend software simulators for quantum computing. The line `sim = Aer.get_backend('aer_simulator')` defines a simulator object based on Aer's 'aer_simulator backend'.
This object can now run a job of executing a quantum program. It's done via `job = sim.run(qc, shots=10000)` where `sim.run` is the function that runs the circuit `qc` with 10000 'shots'. The result and the execution details are saved in `job` variable.
Next we extract the results through `job.result()` function, and subsequently get the measuring counts, which we plot.

```{Note}
The counts are essentially random, and because of the structure of the circuit, they are supposed to by uniformly random.

Any idea why they are supposed to be uniformly random?
```

## Executing quantum programs on quantum hardware

Below are some comparative comments on the pros and cons of real quantum hardware.


```{mermaid}
mindmap
    root(Quantum programming)
        Advantages
            Access the full potential of QC
                Superposition
                Entanglement
        Disadvantages
            Current Hardware constraints
                Noise
                Low number of Qubits
                Low circuit depths
            Remote access only
            Availability
```

The previous slide begs the question, if we can simulate quantum programs on classical machine then what is the point in using quantum hardware. Lets take a look at some advantages and disadvantages of using quantum hardware.​
​​
```{admonition} Noise
:class: tip
Physical qubits experience noise and decoherence, resulting in computational errors. This problem also amplifies as we attempt to use more qubits and so ​this limits the number of qubits you can use​, and the circuit depth of the program you are implementing​.
```


## QC hardware vs software simulators

​
	

||Quantum Computing ​Hardware​| Quantum Computing Software ​Simulators​|
|:---|:---|:---|
|Comparison ​to Reality ​| Actual Qubits​|Software objects mimicking qubits​|
|                      |Quantum entanglement and superposition​| Classical backends, heavy on resources​|
|                      |                                      |Simulated quantum behavior​|
|Noise​                 | Inherently exists, need to employ error mitigation/correction​|Controllable​|
|                      |                                                 |Helps understand & improve Real QC​|
|Cost​                  | Very expensive​| Mostly free & open source​|
|                      | Require heavy maintenance​| Easily setup on laptop/desktops/servers​|
|Access and Control​    | Very limited public access​|Widely accessible, easy to install​ |
|                      | Little control on runtime​ | Debug, analyze, develop easily​|
|                      | You can’t really debug on QC| |​
| Scalability​          | Limited qubits​      | Due to classical backends, actual computation cost grows exponentially ​|
|                      | Future research will open new possibilities| |​



[^lib]: In Python, library containing organized sets of functions and utilities are called modules.
