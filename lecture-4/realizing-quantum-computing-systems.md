---
title: Realizing Quantum Computing Systems
layout: post
mathjax: true
mermaid: true
---

### Learning Outcomes

<table style="width:100%">
<tr>
<td width="60%">
Discuss the types of Quantum Computing Hardware and the Physical components that they are made up of as well as the guiding principle behind their operation. 

<ul>
  <li> This leads us into a discussion into the various engineering challenges in building Quantum Computing systems and what techniques and mechaisms need to be used to tackle said challenges </li>
  <li> We also breifly look into the Roadmaps of Quantum Hardware Companies to identify critical milestones in the path towards Universal Quantum Computing. </li>
</ul>
</td>
<td width="40%"> <img width="900" src="/prep/images/stack-4.png"> </td>
</tr>
</table>


- Why do we need Quantum Computing?
- Qubits
- Quantum Gates
- Quantum Circuits
- Building Quantum Computers
    - Gate based Models
    - Quantum Analog Simulation
        - Universal Analog Simulation
        - Quantum Annealing

- Challenges in building Quantum Computers
    - Noise
    - Scalability
- Tackling the challenges
    - Improved Temperature Control
    - Quantum Errir Correction and Mitigation
    - QRAM
- Quantum Computing Roadmap

- Appendix
- References
{:toc}

### Why do we need Quantum Computing?
First let us answer the question of Why we need quantum computers, There are broadly two reasons why Quantum Computing promises to be useful to us in the future of computing. 

- The first reason is that there exist a class of problems which are very difficult to solve on Classical Computers but can be efficiently calculated on a Quantum Computer. These include certain Optimization problems, Chemical Simulations and some search problems, Quantum computers can theoretically solve these problems in exponentially fewer computational steps in comparison to their classical counterpart. 
- Secondly,Classical computers and processors are getting smaller as observed by the Moore’s law, which was introduced in the previous module, the Quantum effects within the Hardware start becoming more apparent the Quantum Interactions between the individual bits start affecting the information stored in the system and therefore it is important to understand Quantum Phenomenon to build better Classical Processors in the future. 

### Qubits

#### A new paradigm for computation
 Qubits are the fundamental unit of information in Quantum Computing systems they play a role similar to that of bits in Classical Computing. However, there are some key differences between the properties of Bits and Qubits. Bits always correspond to distinct energy values or levels whereas Qubits do not possess a definite energy value until they are measured before which they exist in a superposition of states, this superposition allows us to process multiple states in a single round of computation which is one of the key sources of speedup in Quantum Computing systems. Let us look at some other Quantum Properties which make Quantum systems different from their Classical counterparts

 #### Quantum Properties

- Superposition : It is the ability for a Quantum Particle to exist in a state which has probability of being measured in either of the basis states which are labelled as 0 or 1.In the previous module we showed light polarized in the + state is measured as 0 or 1 with equal probability, this state is an equal superposition of both the basis states.

- Entanglement : A8 feature of Quantum particles which allows us to interact them in a way such that the measurement on one particle influences the state of the other particle, Classically, this would be equivalent to there being 2 coins such that when you flip one coin as heads the other automatically also goes to the state heads. Entanglement is leveraged specifically for Quantum Communication and Crytography.

- Tunneling : Particles are able to cross over a potential barrier even when it would seem to not posses enough energy to do so, this would classically correspond to rolling a ball up a hill with not enough energy to cross the peak but there being a finite probability of finding the ball on the other side of the hill. We use this  phenomenon in certain `Quantum Computing systems especially Quantum Annealing which we will discuss in a section ahead


### Classical vs Quantum Logic 

Similar to how Classical Gates are used to build Classical Computing operations we have a set of Quantum Gate operations which take a qubit or a set of qubits as input and returns a modified version of the state as output. In the previous lecture we discussed the existence of Universal Gate set which means that there always exists is a set of gates that can be used to construct any logical operation that we require, the Pauli operations along with the CNOT gate is one example of such a gate set.


All Quantum gates are required to be reversible in nature which means that there always exists an operation which can reverse the action of a previous gate or a set of gates. This, is however not true for the Quantum Measurement operation which was introduced in the provious module, this operation measures a Quantum state and returns a Classical measurement value as it’s outcome while also collapsing the qubit to the corresponding Quantum state, thisoperation is not reversible and the state that existed before the measurement cannot be recovered. There are several properties of Qubit that you could measure. All Quantum gates are required to be reversible in nature which means that there always exists an operation which can reverse the action of a previous gate or a set of gates.






### Appendix


> Future updates and Scratchpad
{: .block-tip}

## References

