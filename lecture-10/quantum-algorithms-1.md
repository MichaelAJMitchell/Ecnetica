---
title: Quantum Algorithms - I
layout: post
---

(lecture-10)=
# Lecture 10: Quantum Algorithms - I

```{warning} These lecture notes are a work in progress and are not a replacement for watching the lecture video, it's intended to be a supplementary reading after watching the lecture 
```

```{admonition} Learning Outcomes
:class: tip
In this lecture we will be taking a look at the landscape of quantum algorithms, and talk about two of the layers of the quantum stack shown in the right, namely the applications and quantum algorithms. The learning outcomes of this lecture will be the following : 
- Introduction to quantum algorithms and their applications.
- Grasping potential advantage of quantum algorithms.
- Understanding the requirements for the practical application of quantum algorithms.
```


```{image} ../prep/images/quant.png
:align: center
```

## Introduction

## Quantum stack

In the table below one can see some of the problems that can be solved with quantum algorithms (left) and also the type of the quantum algorithms suitable for solving them (right). 

|**Quantum Applications** | **Quantum Algorithms**|
|:---:|:---:|
|![left](./images/applications.png)|![right](./images/algorithms.png)|

## Why do we need quantum computers?

Let's start with a quick recap of why we need quantum computers:

- One example of an application of QC is the Benzene molecule, which is a quantum system that is studied frequently in the oil gas and fuel industry. The Benzene molecule can be fully simulated with a 84 qubit quantum computer. This is something impossible to simulate even with the current best high-performance classical computers.

- Appart from simulation of quantum systems like the Benzene, it turns out that QC has even broader applications in areas like optimisation, machine learning and cryptography.

```{image} ./images/benzene.png
:align: center
```

- Qubits are informationally dense, meaning that we can encode 1 GB of information in just 33 qubits. A quantum computer with 272 qubits can represent more states than atoms are in the universe!
- The examples we have just presented assume noise-free qubits. In practice qubits have errors, which means that more qubits are needed in order to make computations.


## What is an algorithm? 

- An algorithm is a set of instructions that takes in some input and produces some output.
- A classic algorithm is based on the moving around of 0s and 1s, what we call classical hardware.
- One example of an algorithm is the google maps route optimisation algorithm, which finds the fastest route from point A to point B

```{image} ./images/maps.png
:align: center
```

### What is a quantum algorithm? 

- The definition of quantum algorithm is the same as the classical except for the fact that it is implemented using a quantum computing paradigm.

- Operating on quantum hardware allows the algorithm to take advantage of quantum mechanical properties such as superposition, entanglement or interference.

- For gate-based models for quantum computation, the input of the algorithm is encoded in an array of qubits, which are acted upon by a quantum circuit.

```{image} ./images/circuit.png
:align: center
```

- The result of applying a quantum algorithm is a probability distribution over the possible different outcomes, which are arrays of 0s and 1s representing the final state of each qubit.

```{image} ./images/outcome.jpg
:align: center
```

### Computational complexity

- Time and memory space are the two fundamental variables we are concerned with when comparing classical and quantum algorithms.

- These two metrics are encapsulated in the subject of computational complexity.

```{image} ./images/complexity.jpg
:align: center
```

- The image above represents an example of time/memory complexity with respect to some value N, that could be for example the number of variables of a given optimisation problem.

- In the graph we can see how the different lines scale in a different way with the N value. We would say in this case that the algorithm represented by the blue line is the most efficient. 

- The O shown in the graph legend is known as big O notation. It represents the limit behaviour of a function. As an example, this would mean that in the graph the orange line would be at most a multiple of N.

### Grover's algorithm


- Grover's algorithm was one of the earliest quantum algorihtms. It allows us to find elements in an unstructured database. What is more, Grover's algorithm is capable of doing this with a quadratic speedup over its classical counterpart, as we can see in the image below, with N being the number of elements in the database.

```{image} ./images/grover_1.jpg
:align: center
```

- The quantum algorithm works as follows:
    1. First we take a superposition of all the indexes of the elements in the database.
    2. An _oracle_ that can recognise the targeted element is applied to the superposition of elements
    3. Then the so-called _Grover operator_ is applied. This operator amplifies the probability of measuring the desired state. We can apply this operator several times in order to maximise our probability of success.
    4. In particular, by repeating this operator $\sqrt{N}$ times, we will end up with a high probability of finding our targeted element.

### Shor's algorithm 

- Shor's algorithm is one the most important quantum algorithms, as it allows to break RSA-encryption, as it is capable of performing integer factorisation.

- Factorising large numbers is computationally very expensive. Shor's algorithm is exponentially faster that any classical counterpart

- The algorithm works by using a trial and error process.
    ```{image} ./images/shor.jpg
    :align: center
    ```
    
    1. A random initial guess integer between 1 and the number we want to factorise in input.
    2. This input is sent into the quantum circuit, whose diagram (without entering into details) is shown in blue in the image above.
    3. We measure and if the result is not correct we repeat all the process again.


### Solving problems with early algorithms

- Most of the early quantum algorithms are based on the following techniques:
    1. Quantum amplitude estimation (Grover's algorithm).
    2. Quantum walks.
    3. Quantum phase estimation (Shor's algorithm).
    
```{drawio-image} ./images/early_algorithms.drawio
    :align: center
    :width: 100%
```

### Drawbacks of early quantum algorithms

- The early quantum algorithms that we have just seen are not really used in practice.

- This is due to the presence of decoherence and errors in the qubits of actual devices. As the number of qubits increase, the errors increase in our quantum algorithm. As an example, as we consider larger and larger lists, the number of qubits needed for Grover search algorithm would increase, increasing as well the errors of the circuit.

- Thus a distinction is made between what is called _logical qubits_, which are ideal noise-free qubits and the _physical qubits_, which are the real qubits with noise.

- In order to mitigate this errors, we can use error mitigation techniques that imply adding more physical qubits. This way, in order to have the equivalent to 100 logical qubits, we would need 1,000,000 physical qubits with errors.

- Another solution to face the errors is to modify the algorithms and try to make them shallower and using less qubits.

## NISQ era and algorithms

- NISQ stands for Noisy Intermediate Scale Quantum. This describes the current state of quantum hardware, with approximately 100 qubits, subject to noise.

- To work with this circuit, shallow quantum algorithms with low number of qubits are needed. In most of the cases, this algorithms are embbeded to a classical algorithm, resulting on _hybrid classical-quantum algorithms_.

- The most common type of NISQ algorithms are the variational quantum circuits (VQCs), which are quantum circuits that contain classical parameters that need to be classically optimised.
```{image} ./images/nisq_algorithm.jpg
:align: center
```

### Variational quantum algorithms

- One can think as VQC's as trainable quantum circuits. Different problems will require different gates and parameter structure.

- In order to train the variational parameters, we will measure the output of the circuit, sent it to a cost function (which is problem-dependant) and perform an optimisation step (like stochastic gradient descent) to update the parameters. We can repeat this process until we get a set of parameters that make the circuit output the desired solution.
```{image} ./images/vqc.jpg
:align: center
```

- We can use VQCs to solve simulation, optimisation and machine learning problems.

- Even though VQCs by themselves doesn't allow us to solve large problems, its integration in classical pipelines may be of interest in the near future.

### Map of NISQ algorithms

In the diagram below we can see some of the applications of NISQ algorithms. We will cover the different areas of application (simulation, optimisation and machine learning) in the following sections.
```{image} ./images/nisq_applications.jpg
:align: center
```

### Quantum algorithms and applications

In the diagram below we can see another diagram showing the problems solved by NISQ algorithms and the sectors in which these algorithms are useful. As examples, the maximum-cut proble is frequent in the tech sector, like in the study of networks. On the other hand fluid dynamics is present in aerospace engineer, or the travelling salesman problem in logistics. 

```{image} ./images/nisq_applications_2.jpg
:align: center
```


### Simulation 

- Simulation of quantum systems aims to predict the behaviour of a complex physical system such as a molecule. It remains extremely difficult for a classical computer to simulate this kind of systems.
```{image} ./images/simulation_1.jpg
:align: center
```

- These complex systems are generally composed of interacting quantum objects, which can be simulated on quantum computers by directly mapping these objects onto qubits.

- To run a quantum computing simulation algorithm, we have to encode the problem we are solving in a mathematical function called Hamiltonian, which can be thought as the energy model for the system. After encoding the Hamiltonian in the qubits of our circuit, we can apply one of our simulation algorithms to reach the desired solution.
```{image} ./images/simulation_2.jpg
:align: center
```

### Advantage of NISQ simulation algorithms

- Quantum systems like molecules are easy to simulate with other quantum systems (qubits are quantum systems!), as they maintain the same properties and follow the same physical laws.

- As quantum systems are very complex, they are impossible to simulate classically due to memory constraints when the system size exceeds $N=50$.

- This however doesn't mean that any problem computation done with more than 50 qubits can't be solved classically using alternative methods.


### Simulation map 

```{image} ./images/simulation_map.jpg
:align: center
```

- Above is shown the mapping between quantum simulation algorithms and some of their applications in specific industries.

- Algorithms are shown in red, applications in green, and more abstract problems in blue.

- Algorithms can solve a set of particular problems, shown in blue, which can be used for a particular application on an industry.

- As we see, the generic simulation algorithms are the Variational Quantum Eigensolver (VQE) and the Quantum Approximate Optimsation Algorithm (QAOA). The objective of both algorithms is to measure the energies of some Hamiltonian.

### The variational quantum eigensolver

- Looking back at the Benzene molecule we saw at the beginning of the lecture, let's see how we can use the VQE to find its minimum energy state in a process called eigensolving.

- We can encode the Benzene molecule in a Hamiltonian in which we can the apply the VQE to.

- Each of our qubits will represent one component of the system. We can apply evolution operators to these qubits, which will contain variational quantum parameters, that will be optimised until we find the desired minimum energy.
```{image} ./images/vqe.jpg
:align: center
```

### PFAS molecule destruction

- An important use-case of the VQE is the study of PFAS (per-and polyfluoroalkyl) molecule destruction. These molecules are used as heat, water and oil resistant coatings in many areas.

- These molecules are present in many materials, and have the inconvenient that are toxic to human bodies and they can easily contaminate water. Thus, there is an interest in chemical degradation and destruction of these molecules. In order to break these molecules we need to be able to simulate their energies, something that can be done with the VQE.

### Optimisation

- Optimisation is a branch of mathematics and computer science that deals with finding the best solution (maximum or minimum) of some problem, by performing iterations of a given algorithm.

- One may want to minimise quantities like energy use or manufacturing time, or maximise profit for example.

- It turns out that the VQCs we have seen before are promising candidates to solve optimisation problems.

- An optimisation problem can be encoded on a VQC. The quantity we want to maximise/minimise would therefore be a function of the output when measuring the VQC. We can update the variational parameters of the VQC (using a classical optimiser) in successive iterations until the desired solution for our optimisation problem is attained.
```{image} ./images/optimisation.jpg
:align: center
```

### Optimisation map

```{image} ./images/optimisation_map.jpg
:align: center
```

- Above is shown the mapping between quantum optimisation algorithms and some of their applications in different industries.

- When comparing this map with the one we presented before for simulation, we seen than the Grover adaptative search algorithm has been added now. This algorithm is a NISQ variation of Grover's algorithm, where Grover search is iteratively applied and classically optimised to find good solutions.

- As we see, the applications and sectors are different when we compare them to the simulation map.

### Max-cut problem

- A graph is a structure made up of various nodes that have weighted connections (edges) between them. They can be used to model different problems and scenarios. For example social media users can be modelled using a graph, where its edges represent the influence between different users.

- The Max-cut problem aims to do a binary partition of the nodes of the graph so that the sum of the weights of the connections between the two sets is maximised. In the image below we can see how the graph's nodes were divided in two sets: one conatining nodes 0,3 and the other containing nodes 1,2.
```{image} ./images/max_cut.jpg
:align: center
```

- The Max-cut problem can be easily mapped to what is called an Ising Hamiltonian, which can be easily encoded and optimised on quantum computers.

- The Max-cut problem has applications in many areas including clustering, or graph and electrical design. It is often used as benchmnarking for evaluating optimisation techniques.

### Travelling-salesman problem

- The travelling-salesman problem is another famous optimisation problem. Given a list of cities represented with nodes on a graph, and its distances represented by the weighted edges, the objective of this problem is to find the shortest possible route, so that each city is visited just once, and the starting and ending point of the route is the same.

- Similarly to Max-cut, this problem can be easily mapped to an Ising hamiltonian and optimised in a quantum computer. In the image below we can see the graph representing the problem (left) and the shortest optimal route (right).
```{image} ./images/travelling_salesman.jpg
:align: center
```

- This problem has different applications in many areas, being finance and marketing among the most notable ones.

### Optimisation using annealing

- Until now we have mainly focused on VQCs, a type of quantum algorithm that is meant to be implemented on a gate-based quantum computer. However, there exist other types of quantum computer architectures that are good when it comes to solve optimisation problems.

- One of these architectures is what is called quantum annealing. This type of quantum computers are only capable of solving problems that can be encoded as Ising Hamiltonians.

- While this is a limitation, it is compensated by the fact that annealers have more than 5,000 qubits available, meaning that the size of the problems that can be solved is much larger when compared to gate based computers.
```{image} ./images/annealing.jpg
:align: center
```

- One of the most promising quantum annealing applications is portfolio optimisation.</li>


## Machine learning

- The primary goal of machine learning is to develop models that can generalize well to new, unseen data, allowing them to make accurate predictions or decisions in various situations.

- A simple example of a machine learning task is image classification. In the image below we can see bees and ants. One machine learning model (which is well trained), would be capable of distinguishing between the bees and ants in the image.
```{image} ./images/machine_learning.png
:align: center
```

### Advantage of NISQ machine learning algorithms

- We can find different computational bottlenecks in a classical machine learning workflow. One example of this is matrix-vector multiplication, a seemingly simple operation which consumes a lot of computation power when the matrices are very large.
```{image} ./images/matrix.jpg
:align: center
```

- Other examples of computationally expensive tasks appearing in machine learning tasks are Fourier transforms, diagonalising matrices or solving linear systems of equations.

- With quantum algorithms it is thought that we can get an speed-up in some of these tasks.


### Machine learning map 

```{image} ./images/machine_learning_map.jpg
:align: center
```

- Above is shown the mapping between quantum machine learning algorithms and some of their applications in different industries.

- When compared to the previous maps we have shown, it can be seen that VQCs are still important here, and also the quantum embedding kernels, which are based on classical kernel methods but implemented on a quantum computer.

- Among the applications we find neural networks (we can use VQCs as one neural network layer) or quantum generative adversarial methods (quantum GANs), that can be used to generate data that resembles the original data used for training. These are especially important in fraud detection in finance industry.

### Classical neural networks 

```{image} ./images/neural_network.jpg
:align: center
```

- A classical neural network is composed of multiple layers of transformations, governed by certain weights and parameters, which are represented in nodes in the image.

- A vector is input to the networks and is transformed multiple times until we get the output vector.

- The parameters of the network are trained to minimise a cost function that will depend on the quantity that we are measuring.

### Quantum neural network

- A quantum neural network is a neural network where one of more of the layers is a VQC.

- As we seen in the previous section, each layer of the network is governed by a set of parameters. When a layer is a VQC, these parameters will be the variational parameters appearing in the quantum circuit, that will be optimised during the training phase.

- What the benefits are of having a VQC as layer is still an open question in quantum machine learning.
```{image} ./images/quantum_neural_network.jpg
:align: center
```

### Quantum tranfer learning 

- Quantum transfer learning is a technique that falls within the field of quantum neural networks.

- This technique involves using a pre-trained classical neural network, and substituting one of the layers of the networks by a VQC, as we can see in the image.

- The VQC variational parameters are trained using the output of the pre-trained classical neural network to get the desired result.
```{image} ./images/quantum_transfer_learning.jpg
:align: center
```

### Quantum machine learning example 

- Let's return to the image processing task on bees and ants that we saw before to see an example of application of quantum machine learning.

- As we see in the diagram, we input an image encoded in 512 pixeles to a pre-trained neural network on image classification.

- After that a layer is applied to reduce dimensionality, and its output is sent to a VQC with 4 parameters. Then, another layer is applied to get a 2-dimensional vector with out predictions
```{image} ./images/quantum_machine_learning_example.jpg
:align: center
```

### Anomaly detection with qGANs

- As we have seen before, GANs have seen great success in anomaly detection.

- A GAN consists of two neural networks, a generator and a discriminator. The generator aims to to create a dataset which is indistinguishable from the training data provided, and the discriminator aims to succesfully distinguish between these two datasets.

- After training these two networks, the discriminator will be capable of detecting anomalies on unseen data.

- The classical GANs have shown limitations in training phase and sampling procedure. That is why in qGANs the classical generator is replaced with a VQC to try to overcome this limitations.
```{image} ./images/qGANs.jpg
:align: center
```

## Wrap-up
Learning outcomes achieved:
- Introduction to early quantum algorithms
    - Searching
    - Cryptography
- Grasping potential advantage of quantum algorithms
- Introduction to NISQ algorithms and their applications in different areas
    - Simulation
    - Optimisation
    - Machine learning
