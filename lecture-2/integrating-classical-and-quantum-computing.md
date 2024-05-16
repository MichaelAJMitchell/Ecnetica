---
title: Integrating Classical and Quantum Computing
layout: post
---

(lecture-2)=
# Lecture 2: Integrating Classical and Quantum Computing


```{warning} These lecture notes are a work in progress and are not a replacement for watching the lecture video, it's intended to be a supplementary reading after watching the lecture 
```

```{admonition} Learning outcomes
:class: tip
1. Understand the reasons and opportunities for integrating classical high-performance computing & quantum computing systems.
2. Demonstrate a high-level technical understanding of hybrid high-performance computing & quantum computing systems.
3. Acquire knowledge of ongoing efforts towards integrating classical high-performance & quantum computing systems.
```



## Why imtegrate classical & Quantum Computing

### Classical High-Performance Computing

In the simplest of cases, applications to process data or perform modelling or analysis, are typically represented as a computer program which is executed on a Central Processing Unit (CPU). For simple cases, the CPU can be imagined to have one worker that executes the program instructions in a serial fashion to produce the desired output.
As the complexity of applications and their logics increased, opportunities arose to do what is called parallel computing – this involves executing multiple parts of a program simultaneously on multiple workers within Processing Units. For example, the program or parts of the instructions (known as kernels) within the program, may have to be executed to process different input data sets which are independent of each other – so, these could be done in parallel. This is typically referred to as data parallelism.
Another example is where for the same input data, different kernels within a program may be executed independent of each other and hence in parallel. This is referred to as task parallelism.
As the complexity of applications and their logics increased, computational scientists and HPC specialists built software libraries that take advantage of data parallelism and task parallelism within their applications, so that their programmes could be executed in parallel in more powerful CPUs that have multiple workers within them – these workers are often referred to as cores – due to which the CPUs are referred to as multi-core CPUs which can execute parallel programmes. Typically, multi-core CPUs have anywhere between 2 to 40 or 60 cores, depending upon whether you have them in your laptop or in a powerful server on high-performance computing systems. Now-a-days even processors on edge devices such as smart sensors and satellites have multi-core processors.
In this context, as the complexity of applications and their logics continued to grow, and the opportunities for data and task parallelism within them were identified more and more, special-purpose processors which are very good at certain types of parallel execution were created.
Examples of these are graphics processor units (GPUs) and Field Programmable Gate Arrays (FPGAs) which have 100s or 1000s of cores in a single processor. Since these are special-purpose, they are often referred to as Accelerators.
Consequently, while the general purpose CPUs are responsible for executing an application programme, they offload some of the kernels in an application to these special-purpose accelerators and get partial results back from them to complete the rest of the program’s execution. Of course there are exceptions where, for instance, FPGAs are deployed as standalone devices on control systems in factories, robots, etc.. But, in the context of systems modelling, analytics, AI, simulation, these special-purpose processors such as GPUs and FPGAs are often used by the CPU for specific kernels within an application’s program.

Another point to note is that, initially the software tools and libraries required to program such different types of processors also remained different. Over a number of years, programmers, software developers and HPC experts have had to integrate different software tools and libraries for a single program that is composed of multiple heterogeneous kernels. Often, this was done in collaboration with end users from academia and industry that own the applications in order to better understand the use-cases and ensure that these tools fit the requirements and uses within the community.
Over time, interoperability and unification of these software tools and libraries was achieved – as a result of which now-a-days many programming libraries have the ability to target different processor types under the hood, thereby reducing the difficulty of end-users, application developers and computational scientists.

### Co-existence of Classical & Quantum Computing

Now, given the history and trajectory of how such special-purpose accelerators such as GPUs and FPGAs were developed and have been integrated into the general-purpose CPUs ecosystem (both at hardware and software levels), it is essential for us to take a moment and observe where quantum computing systems and quantum processing units QPUs are currently placed, and how they will and should function alongside these classical processors.

In our earlier lecture on “Demystifying quantum computing”, we had introduced that quantum computing is an emerging methodology and technology, and is understood to be suitable for very specific types of computations.
Therefore, similar to GPUs and FPGAs, quantum computers and QPUs will be used as accelerators and be driven by a general purpose CPU-based computer whether on a desktop or within HPC systems.

In this context, there are two aspects to observe with regards to the co-existence of classical and quantum computing systems and applications.

Firstly, while classical computing systems are already interfaced with quantum computers, this has been done more for the purpose of providing access, development and demonstration.
How classical and quantum computing systems interface to exchange data, transfer application kernels between each other, and how the existing classical software tools and libraries can support the seamless programming of quantum computers has a lot more gaps and opportunities for innovation and development.
This is analogous to how time and efforts were spent through collaboration between the scientific, enterprise and HPC communities to integrate CPUs, GPUs and FPGAs at hardware and software levels.

The second aspect to observe is that, while all of the classical computing systems and processors represent and process data in the same way – as bits using high-level abstract programming libraries, quantum computing systems and QPUs represent and process data in a completely different way – as qubits and currently use low-level gates which is equivalent to how computers were programmed around the mid 20th century. This is covered in more details in our lecture on “From Bits to Qubits”. 
Therefore, on one hand how classical and quantum computing systems exchange data and application kernels for processing is non-trivial – there has to significant translation performed.
On the other hand, current methods and levels of representation of data and programs for quantum computing are at a very low-level. As mentioned earlier, quantum computers are programmed with data as qubits (while classical computers have higher-level abstractions such as objects, files, etc.) and quantum operations are defined using a combination of gates (which is similar to programming early computers using gates and flip-flops around the mid 20th century). Having acknowledged the currently primitive level of programming quantum computers, this will only continue to improve wherein high-level powerful abstractions for data and software libraries are being developed at the same time as the quantum computing hardware is improved. 

Again, in the earlier lecture on “Demystifying quantum computing” we highlighted that while the reliability and scale of quantum computing is currently limited, 
there are ongoing efforts by enterprises and research groups to improve these noisy-intermediate scale quantum systems to build reliable error-corrected larger-scale quantum computing systems, 
quantum algorithms are bring explored for different example use-cases, 
the computing community driven by the HPC experts and organisations, is driving the understanding and efforts required to enrich the software ecosystem and programmability of quantum computing systems. 

And, the importance of doing this as a part of existing HPC software methods and tools through extensions is under discussion and being acknowledged by the scientific and enterprise communities, so that quantum computers can be seamlessly used within and by existing classical high-performance computing systems and its users. We will discuss this in a bit more detail later during this lecture.

### Quantum Computation Workflow
Before going forward with some specific examples of potential hybrid high-performance quantum computing applications, let us look deeper into the quantum computing part of an application workflow.

Presently, all data is generated and stored in classical format – that is in binary as bits. This is represented by the first letter in this map where C represents generation of classical data.
This classical data is then processed by classical computing systems in classical formats. This is represented by the second letter in the map where C represents classical nature of the processing/computing system.
Thus, the top left category CC is the scenario where classical data is generated and stored is processed by classical computing systems.

Towards the end of this lecture, we will highlight quantum sensing and metrology to collect or measure quantum data. So, that is one source of quantum data generation and the two bottom categories are scenarios where 
QC is the scenario where quantum data may be used for classical computing systems, an example is where classical applications such as machine learning models could be useful to study the internal state of a quantum system and associated quantum data.
And, QQ is where quantum data is processed by quantum computers. This quantum data may come from measuring a quantum system through quantum sensing and metrology technologies, or quantum data within a quantum computer to simulate a quantum system such as a physics or molecular models.

Now, the highlighted category CQ is the scenario where quantum computing systems process classical data. The data can be constituted of any kind of observations from classical systems such as text, images, time series, structured or unstructured data. In this scenario, is necessary to translate the classical data and represent it as quantum data within a quantum computer for it to be processed. This is illustrated in the workflow on the right.

<<CLICK>>
The classical input data is prepared into quantum data through a step commonly referred to as quantum encoding or state preparation. The result is quantum states in which a set of qubits are used to represent the data as a superposition – do not worry about the terminologies and complexities now – if you continue with future lectures, these are introduced more understandably. For now, it is essential to just acknowledge that classical input data has to be encoded into quantum states, which can then be processed by a quantum program which is defined using a series of quantum operations. These quantum operations process the initial quantum state into a resultant quantum state. At the end of the processing, in order to get the quantum results out of the quantum computer, a series of steps have to be performed. The first of these steps is to perform measurements to read what are called observables of the quantum computing system.

Let’s pause here for a moment. In the lecture on “Demystifying quantum computing”, we discussed that there are several technology options available to engineer and develop a quantum computer – using superconductors, photons, neutral atoms, ions, etc. – each with its own pros and cons. Depending on the technology used to implement a quantum processor, the observables of the quantum system that will be measured may be different. For a photon-based quantum computer, the observables can be phase, polarisation and wavelength. Irrespective of this, the observables are measured to describe the state of a quantum system.

Coming back to this workflow, the measurements are performed to read the observables of the quantum computing system’s state at the end of a quantum program’s execution, these observables describe the properties of final state of the quantum system, and these observables are post-processed to translate the output of quantum workflow into classical data.

In summary, explicit complex steps are required to encode classical input data into an initial quantum state, on which a quantum program through quantum operations can be applied, and the final quantum state of the quantum computing system is measured to read observables that describe the system’s properties, and the observed properties have to be post-processed to reconstruct the results of the quantum computation as classical output data.

There are two points to note here:
- First, all steps indicated as green rectangles and their results as green circles are in the quantum paradigm or system, while the blue and red steps and their results are in the classical paradigm or system.
- Second, quantum encoding can be a very expensive step depend on what data we want to encode and quantum processing we want to do. For instance, the cost of encoding the properties of a molecule may be less expensive.

But large datasets like those used to train machine learning or deep learning models will be very expensive to encode, and hence any quantum advantage due to quantum processing may be negated by the cost of quantum encoding. This is a key dictator of what types of data and problems have an advantage for using quantum computing.
Also, at present due to the low-level of programming abstraction that we discussed earlier, it is quite complex to define a quantum program using quantum operators. A combination of skills spanning quantum mechanics, quantum information processing, advanced algebra, software development and domain expertise are required together. This is where advancement of software tools and libraries as well as skills development is important for programming quantum computers.

Finally, reading out the results from a quantum computer is also an area of active development to improve accuracy of the measurements and one of the places where error correction can be applied.

More details on these will be discussed in other QPCC lectures

### Quantum computing as an accelerator

Now, having looked a bit more into the detail of what a quantum computing workflow generally involves, let us fit this into the larger picture that we had discussed earlier.

For classical computing using CPUs, GPUs and FPGAs, the classical application program natively takes classical data as input and produces classical data as output.
When using quantum computing systems and QPUs as accelerators alongside the classical computing systems and processors, the result is that the entire quantum workflow that we discussed earlier needs to be implemented in order to offload an application kernel and its data from the classical computer that has to be accelerated by the quantum computer.

Consequently, this is the primary reason that necessitates integration of classical high-performance and quantum computing systems at different levels of the stack, from physical location, communication network, processing , data storage, several payers of software and programming tools, algorithms and applications. This full-stack integration is essential for efficiently and effectively using quantum computing as an accelerator, is non-trivial, and is discussed in a bit more detail later in this lecture.

In the meantime, let us have a look at some application examples from a few select sectors to understand why integrated hybrid high-performance quantum computing could be beneficial and impactful.


### Where does Quantum Computing fit?

### How does the quantum computing ecosystem look

### What does QPCC offer you

### Appendix

> ### Future updates and Scratchpad

### References

