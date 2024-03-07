---
title: Demystifying Quantum Computing
layout: post
---

(lecture-1)=
# Lecture 1: Demystifying Quantum Computing



```{warning} These lecture notes are a work in progress and are not a replacement for watching the lecture video, it's intended to be a supplementary reading after watching the lecture 
```

```{admonition} Learning outcomes
:class: tip

This is an introductory module, which sets the stage for the remaining course by discussing some very elementary question into computing, and delves into quantum computing. As we go through the sections below, we will -

- Gain knowledge to evaluate the capabilities, limitations and potential areas for applying quantum computing.

- Demonstrate an understanding of the value chain and value proposition of quantum computing alongside classical high-performance computing.

- Demonstrate ability to identify key high-level tipping points to reach practical quantum computing.
```

```{image} ../prep/images/quant.png
:align: center
```


## The Era of High-Performance Computing

### Generations of Computing

The current form of Classical Computation started in the first half of the 20th century, where vacuum tubes used voltages differences and were used to control the electron flows and implement logical operations for early digital computations. This led to innovations towards electronics where semiconductor-based transistors had the ability to have smaller form factor, more reliable, faster and energy-efficient electronic devices.

The third generation came about when semiconductor-based devices could be packaged into dense electronic circuits, in which a large number of tiny transistors could be integrated into discrete electronic components for specific functionalities.

With the fourth revolution, very-large-scale integration capabilities and micro and nano-fabrication technologies allowed the revolution where a wide range of powerful, application specific, parallel, field-based or energy-efficient microprocessors have been created. These microprocessors have led to the development of smart devices that are deployed out in the field as sensors, in our mobile devices, work stations or more aggregated compute systems such as HPC clusters or public cloud systems.

There are two common elements in each of these first four generations of computing:
```{card}
1. The unit of representing and processing data has been in terms of binary states (on/off, or 0/1 or `true/false`).
```
```{card}
2. The advancements have been in shrinking the form factor through fabrication and packaging within the world of classical mechanics, i.e. controlling a stream of sub-atomic particles to represent the binary states (to oversimplify – a flow of electrons represents zero, or the opposite a one).
```


One among the latest emerging revolutions in computing is quantum computing about which we will learn more in this lecture and the rest of the course.

At a high-level the leap and main difference in quantum computing is:

```{card}
1. By controlling the properties of atomic or sub-atomic particles at a much finer level of granularity and precision, quantum computing works as a different paradigm of computation.
```
```{card}
2. And in this new paradigm, data is no longer represented in binary states (i.e. either zero or one), but as a probability-based combination of different possible states (for example, as a zero and one at the same time with certain probabilities). This brings in a huge change in the way data is represented as well as processed in quantum computing compared to classical computing – but more on this later in this session and rest of the course – particularly, the one on bits to qubits.
```

#### Scales of Computing

From another perspective, we can see the trends in how capabilities of computing systems have also evolved. The currently familiar form of digital computers were initially targeted at personal computing (of course if we acknowledge and park the mainframe computations for the moment).​

These desktop-based computers originated with limited single-core processor capabilities, and then evolved into multi-core processors on which computations in an application are parallelized at the logic/algorithmic level as well as at the instruction level to exploit parallel execution on several hardware or virtual cores on processors. ​Depending on the systems, current multi-core systems have 4, 8 or even dozens of cores on a single processor these days.​ This led to the parallelization of many applications delivering performance through shorter time-to-solution or in the form of high-throughput computing.​
​
A complementary approach to parallelization using multiple cores evolved into the innovation of many-core processors (such as Graphics Processing Units, or FPGAs) which are typically used as accelerators for the more traditional CPU-based processors.​

Together, CPU-based computing coupled with GPU or FPGA or recently Tensor Processing Units and Vector Processing Units, such accelerators have created a generation of heterogeneous parallel processing systems and applications. Some types of computations and data are better suited for processing on CPUs, while other types are better on certain accelerator devices.​

Now, the field of high-performance computing has leveraged this ability to build heterogeneous parallel processing systems and applications that are optimised for computation performed on large-scale systems such as supercomputers, public cloud systems, as well as on small-form factor devices such as smart sensors or mobile platforms or even satellites. It is important to note that high-performance computing, typically referred to as HPC, is the ability to seamlessly execute different parts of a complex application efficiently (for faster time-to-solution, energy efficiency, or high-throughput) on different types of computing devices which may be connected together. And these HPC systems may be supercomputers, HPC clusters or your powerful workstation, or smart devices.​

Currently, most of the focus in HPC is not just about building more powerful or efficient systems, but also to optimise the algorithms and their software implementations to solve more complex problems with increased accuracy, speed and scale. This is where quantum computing is positioned to serve as another type of accelerator in high-performance computing, where certain parts of a computation or application could benefit from being solved on quantum processors, while the rest of the application is better to be run on classical processors. With this, we are at the cusp of quantum computers being coupled or integrated to form hybrid high-performance quantum computers. So, as the quantum computing technology evolves, we are likely to see more seamless hybrid classical HPC quantum systems, and heterogeneous applications where there are both classical as well as quantum algorithms and software solutions.​

### What can HPC do?

Now, before going further to quantum computing or its applications, we take a moment to acknowledge where classical high-performance computing currently plays a role across different domains and problems.​

The digital transformation of many sectors, businesses and solutions has moved to a data-centric scenario where the huge variety and volume of heterogeneous datasets from different sources​ -

```{card}
- be observed data from satellites, devices, vehicles​
- human-related data such as transaction, personal data, activities​
- or data from simulation of different systems and scenarios​
```

All of these types of input data are analysed to infer intelligent, actionable, decisions, policies and strategies – both for commercial services or by public agencies​.

The analysis is typically performed by a variety of techniques – numerical or statistical modelling that use rules of the underlying principles (whether in natural or man-made systems), more recently AI-based modelling that are build to capture the ​characteristics of data.​

These types of models are used to analyse the data, simulate further scenarios – the models generate more data and also allow for end results, outputs that are used for decision-making, designing products, solutions and services.​

The role of high-performance computing has increasingly allowed for building and running such modelling and analytics – with a focus on doing more complex modelling and analytics that used to be out of reach of less powerful computing systems​.

So, HPC allows for doing increasingly more data-informed complex modelling and analytics.​

Another factor that HPC enables is increasing the accuracy and precision of these modelling, simulation and analysis exercises – instead of approximating the complexity and simplifying the computations due to limitations in time or computing resources.​

Thus, HPC has enabled a wide variety of sectors and businesses to do more complex modelling, simulation and analysis with improved accuracy, precision and time-to-solution.​

#### Where does Quantum Computing fit?

Now that we have touched on the role and applications of high-performance computing, and pointed out where many of our sectors and organisations are most likely already using it to build and power digital solutions,​

we now move on to addressed where quantum computing fits in this context, and why we look towards this emerging computing paradigm.​

​The primary reasons why computational technology developers and its end-users are looking at the next generation of methodologies and platforms is that currently there are a number of challenges and limitations that classical high-performance computing is hitting​

```{card}
- a number of complex computational, simulation and modelling problems remain intractable – and, an feasible time-to-solution is achieved by reducing the complexity through approximations of the problems/systems that are solved (through methods such as heuristics), or reducing the precision of the solution to be completed to an acceptable threshold that produces a good-enough solution. This is a compromise between high-accuracy or high-precision, versus a reasonable time-to-solution or what problem size can be actually represented and solved in a classical high-performance computer.​
```
```{card}
- Typically, these are faced in all of the sectors, algorithms and application areas that we walked through earlier.​
```
```{card}
- even on supercomputers, for time-bound applications such as weather forecast, or real-time applications – the available time to compute a solution is limited, or the ability of decompose a problem into smaller parts for parallel processing is also being limited due to the nature of the problem.​
```
```{card}
- this is one of the primary reasons where developers are looking at alternate computing techniques to supplement the existing classical high-performance computing as accelerators for specific parts of the problem.​
```

There are also fundamental reasons that are closer to the hardware-level that has limited the ability to build more and more powerful classical HPC systems​

```{card}
- the power wall is a problem that limits the ability of pack more transistors into processors with limited power consumption, heat dissipation, or also about building larger supercomputing systems that are energy efficient and do not require a township’s worth of energy consumption - therefore the power requirements of more and more powerful HPC systems and processors is a limiting factor​
```

```{card}
- the memory wall on the other hand is the increasing disparity between processors and memory/data storage devices - the computational modelling and analysis methods are increasingly moving driven by more and more data that are stored and have to be efficiently processed; exploring large data or parameter spaces are typical in areas such as computational physics, chemistry, optimisation and data analysis problems; therefore, how data is represented and computations are performed on the data is becoming another key bottleneck​.
```

```{card}
- finally, the ability to build more powerful and dense processors has been a long-standing problem in the semiconductor industry – scaling the fabrication of classical processors into smaller and smaller form factors are limited by challenges in engineering as well as fundamental physics​.
```

This is where the underlying principles for making quantum computing feasible, by leveraging its fundamental computational power, and engineering quantum computing devices emerged.​

#### How does Quantum Computing work??

One of the key methods my which individual processors have been classically made more powerful has been through reducing their scale and size.​Chipmakers have incrementally gone down in the sizes of transistors that are used to build processors from 10 nanometers to 7 nanometers to now 5 and 3 nanometers.​

​In simplistic terms, a transistor is a device to control the flow of electrons, and using that ability to represent binary states (simplistically, a flow in a certain direction may represent zero, while in the opposite may represent one). ​Typically within a transistor, the source and drain are two ends, while a gate is used to control the flow of electrons between the source and drain.​

​As transistor sizes are reduced to pack more of them into processors, the physical sizes of the transistors, particularly, the dimensions of source, drain, gate also reduce in size.​

They have been reducing so much in size that it becomes increasingly difficult at an engineering level to control the flow of electrons accurately, and also the physics principles based on which electrons behave also move from classical mechanics to quantum mechanics.​

This is a challenge and has limited the ability to build smaller transistors and more densely packed classical processors.​

However, quantum mechanics and quantum effects that happen in a device at such small scales have been the opportunity to represent and process data in a different paradigm – quantum computing technologies.​

Rather than controlling a flow of electrons, and using that to represent zero or one as binary states of data – quantum computing works at such as small scale where the states of data are represented using individual particles - electrons or ions or specific charged atoms – and these individual particles are then controlled and manipulated to implement processing of their states and data​

Therefore, fundamentally, representation and processing of data works at a much smaller scale in quantum computing devices compared to classical computing devices.​

Often, these quantum effects are presented in many articles as quantum tunnelling, entanglement, superposition, etc.. Further details on these quantum effects are discussed in the {ref}`lecture-3`.​

Now, to implement a quantum processor, different particles are being explored to present the state of data and the methods used to control the particles also vary – this is what we observe from different technology developers pursuing superconducting, trapped ion, neutral atom, silicon dots, diamond-based or topological qubit technologies.​

Which approach is the most efficient, accurate and promising one? That is yet to be determined. Presently, all of these are being pursued by different players with an aim to improve the accuracy of these systems, their reliability because at such a small scale, quantum systems are easily affected by noise from their environment, the ability to control the individual particles is so fragile that the quantum states do not last too long – thus, they become erroneous or incorrect very soon, and hence you can do only very short computations.​

Thus, most of the efforts are currently to pursue these different approaches for realising and manufacturing quantum processors, and explore which ones can become mature and reliable enough like current classical processors.​

```{card}
- Classical computing works by controlling flow of electrons (bits, binary states)​
- Quantum computing works by controlling (sub-)atomic particles at an individual level​
- This is the source of quantum computing’s power that is based on quantum mechanics​
- Can bring precision, accuracy, scale of problem, time to solution, etc.​
- That a representation of data (as qubit) can be at more than one value (state) at the same time with certain probabilities​
```

This is where quantum computing, specifying data and operations/computing for quantum computers and quantum programming is radically different from classical computing​

### Where is Quantum Computing Positioned

Looking ahead, given that we are in the second revolution of quantum technologies and at the early stages of developing the quantum computing technologies, where should we position it alongside the existing classical computing technologies?​

Well, as we have already mentioned quantum computing is an emerging methodology and technology that is aimed as an accelerator in high-performance computing platforms and systems.​

Currently, it is understood to be suitable for very specific types of computations which it can do much better than their classical HPC counterpart implementations.​

These types of specific computations include tasks such as modelling and simulating complex systems that are analogous to quantum mechanics systems (such as physics systems, molecular structures, certain mathematical problems), and typically quantum computing can potentially make such complex simulations and computations which are currently in-tractable at the desired level of accuracy, achievable using the quantum computing approach.​

Having said that, while a number of interesting algorithmics approaches are being developed and their applications to practically relevant use-cases identified, there is a lot more to be further explored both in terms of algorithms and the types of use-cases that are suited for quantum computing.​

We will look at a few examples in a moment. Before that however, for any of us that are at the first step with the question, “where do I start to see if quantum computing is going to be relevant or beneficial for me”, typically​

```{card}
- when modelling and simulating systems with complex characteristics, parameter spaces, correlations​
```
```{card}
- when the computations and calculations require approximations to make the solution tractable, for instance exploring a huge parameter space for the best solution,
```
```{card} ​
- when we use lower precision to perform computations and representation of data on classical HPC compared to the problem’s natural precision;​
```
```{card}
- when the time to compute a solution requires optimised by orders of magnitude,​
```

These are typically candidates where quantum computing could help and deliver a potential improvement compared to classical computing methods.​

Therefore, when looking for candidate computations or use-cases, look for specific parts that need more accuracy in exploring large parameter spaces, probabilistic systems when complex correlations, representing systems or problems with higher precision.​

### The Quantum Computing Ecosystem

Here is an initial sketch of the ecosystem.

```{mermaid}
%%{init: {'theme':'base', 'fontSize': '11', 'securityLevel': "loose"}}%%
mindmap
    root["Quantum Computing Ecosystem"]
        prv(("Providers"))
            [IBM Quantum]
            [Rigetti Computing]
            [D-wave Systems]
            [IonQ]
            [Microsoft]
        dev("Developers")
            [Researchers]
            [Industries]
        use(("Users"))
            [Researchers]
                [Chemistry]
                [Bioinformatics]
                [Material Science]
            [Industry]
                [Pharmacy]
                [Finance]
        inv("Investors")
            [Government]
            [Industry]
```

### Appendix

> Future updates and Scratchpad

### References
