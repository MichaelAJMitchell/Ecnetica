---
title: Landscape of Quantum SDK's and Tools
layout: post
mathjax: true
mermaid: true
---

(lecture-6)=
# Lecture 6: Landscape of Quantum SDK's and Tools

```{warning} These lecture notes are a work in progress and are not a replacement for watching the lecture video, it's intended to be a supplementary reading after watching the lecture 
```

```{admonition} Learning Outcome
:class: tip
In this lecture, we discuss the Software and Tools for Quantum Programming. We will begin by mapping out the components of the quantum stack that we wish to investigate. In particular we will discuss the high level and low level quantum computing software components in the quantum computing software layer. This is followed by a discussion on how we can build a quantum programming stack by bringing components from the software and hardware layers as needed.​ Through the lecture, we will - 

- Develop insight into the key components of the Quantum computing Software layer.
- and gain awareness of the different ways of using the Quantum Programming Stacks.​
```

```{image} ../prep/images/quant.png
:align: center
```

## Introduction
Software Development Kit (SDK) is a very common acronym used to collectively represent softwares one requires to write program that either are in specific language, or suited for specific domain of tasks, such as web development, system programming, or app development for a given operating system. Our domain of interest is Quantum programming, where we wish to write programs that implement quantum algorithms.

Just like the SDKs (which you know now :-D) we will run through some of the *software* terminologies along with the introduction and discussion of the programming tools for running quantum algorithms.


## Softwares and Tools for Quantum Programming

Some of the most common terms in softwares and programming in general are the following
- [Programming Language](https://en.wikipedia.org/wiki/Programming_language) is a system of notation for writing computer program, and is usually described in terms of its syntax (grammer) and semantics (meaning). Unlike human languages, here you need to be precise, as computers don't take kindly on incorrect codes :-D .
- [High and low level](https://en.wikipedia.org/wiki/High-_and_low-level) is often used to categorise or classify programming languages and libraries, and is based on scale of systemic operation. High-level describes more abstract, macro level, and generic usage, while low-level describes more specific, individualistic component of a systemic operation focusing on details of rudimentary micro function. In programming language, high-level languages focus on architectural capabilities to enable wide range of usage, while low-level languages focus on doing specific tasks efficiently.
- [Software library](https://en.wikipedia.org/wiki/Library_(computing)) is a collection of computer programs packaged in specific format to be used by user to aid writing their own programs. Some libraries are generic enough to be used in wide usecases, such as **libstdc++** (which provide numerous functions to aid writing a c++ code) and other are specific to special usage, such as **LAPACK** (Linear Algebra package for a range of matrix and vector operations). They are also classified as high and low level.
- [Software layer](https://en.wikipedia.org/wiki/Abstraction_layer) is a terms that originates from different layer of abstraction in writing a program that does a particular task for me.
- [Software Stack](https://en.wikipedia.org/wiki/Solution_stack) is basically a set of software subsystems or components needed to create a complete platform to build and run a certain type of program. For example, to write a simple python code and execute it, you need (i) a python interpreter, (ii) a convenient text editor to write python code, (iii) a file manager to save and organize file, and (iv) a terminal to sometime configure, install or manage python interpreter. So the collection of these four will be required to develop python software. Such collection is often referred to as **full-stack**.

Then we'll introduce the notion of the quantum programming stack, which overlaps the lower two layers of the Quantum Stack. This encapsulates the idea that these two layers are tightly connected and in order to build a functioning quantum programming stack, one must carefully select the compatible components from the two constituting layers. Alternatively a number of big vendors provide pre-integrated quantum programming stacks as a service, deployed in a cloud environment, some components of which could also be used locally. Another approach are the so called Quantum Orchestrators which are very similar to the QPSaaS, but they are generally provided by smaller, independent quantum software companies. The Quantum Orchestrators are generally bespoke and more flexible and could be deployed either on-prem or in the cloud. ​

```{mermaid}
:center:

 graph LR;
    linkStyle default fill-opacity:0.0,stroke-width:0px,stroke-opacity:0.0
    subgraph qp [Quantum Programming Stack]
    subgraph soft [Quantum Software]
    1(High level) --- 2(Low level)
    end
    subgraph hard [Quantum Hardware]
    3(Circuit Based) --- 4(Anolog)   
    end
end
```

## High-Level Quantum Software

### Quantum programming languages

### Generic quantum languages & libraries

```python
# Qiskit
qc = QuantumCircuit(2) # this constructs a quantum circuit object named qc.
# quantum circuit object has methods, that can add different gates to the circuit.

qc.h(0) # Applies the Hadamard gate to the first qubit.
qc.cx(0, 1) # Applies the CNOT gate between the first two qubits.
qc.draw() # Print the drawing of the circuit.
```


### Specialised quantum languages & libraries

## Low-Level Quantum Software

```openqasm
OPENQASM 2.0;
include "qelib1.inc";

qreg q[2];
creg c[2];

h q[0];
cx [0], q[1];
measure q[0] -> c[0];
measure q[1] -> c[1];
```

## Quantum Programming Stacks as a Service

## Quantum Workflows & Orchestrators

## Custom Quantum Software Stacks

