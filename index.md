---
layout: home
---

# Ecnetica Project Overview

The Ecnetica project exists to induce a paradigm shift in Irish education by tearing down the barriers that have turned advanced mathematical understanding into a privilege rather than a right. Through cutting-edge animations, expert instruction, and freely accessible content, we’re dismantling the pay-to- win culture of private tuition while simultaneously raising the standard of mathematics education across the nation.

Our mission transcends exam preparation – we aim to ignite a deep, intuitive understanding of math- ematics that will empower the next generation of Irish problem solvers. We’re building a future where understanding of Higher Level mathematics is democratized, where every student can develop the quantitative reasoning skills needed to tackle tomorrow’s challenges, and where Ireland’s tradition of academic excellence is accessible to all. This is mathematics education reimagined: comprehensive, inspired, and absolutely free

## How it Works

## The Knowledge Graph

Our knowledge graph connects Leaving Certificate topics in a way that reflects the true structure of the curriculum, not as a linear path, but as a web of interrelated concepts. The knowledge graph is an interconnected structure of thousands of topics, organising the curriculum and facilitating our procedurally generated content delivery. The nodes represent individual concepts, and the connections represent relationships between concepts.

To accurately model a student’s understanding, we break concepts down to their smallest meaningful parts. Currently, the graph contains over 3,000 microconcepts. The fine grained structure allows us to deliver hyper-specific remedial content, and to introduce exactly the concepts the student is most prepared for. The strength of the knowledge graph is in its scale and accuracy.

Our graph ties in with our knowledge tracing systems to update student learning as they complete content. We track progress at each node, with connections enabling us to update implicitly covered topics. Precise mapping of student knowledge gives us the ability to address and target knowledge gaps, for a completely personalised experience. We can then focus on introducing new concepts, advancing the student’s knowledge frontier.

## Multiple Choice Questions

The best way to solidify knowledge during the learning process is through practice. Our multiple choice question (MCQ) format encourages active learning, helping students learn by doing rather than just reading. MCQs are organised by topic, interfacing directly with the knowledge graph.

Some questions are inherently more complex than others, and we account for this by defining a difficulty parameter. The difficulty of an MCQ is determined by a number of properties including, problem solving, memory requirement, notational difficulty, algebraic nuance, and topic interconnectivity. To deepen learning, every MCQs includes an explanation, giving students an insight into where they may have gone wrong when answering a question. This reinforces student learning and understanding.

Selecting the right questions for a student gives them a more personalised experience, as though they have their own tutor. We frame question selection as a constrained set cover optimization problem factoring in, low mastery topics, post-requisite importance, and indirect topic reviews. Additionally, our selection system is difficulty and student-ability aware. In our system we aim to use the minimum number of questions to cover the maximum amount of material, prioritisng an efficient learning process.

## Knowledge Tracing and Spaced Repetition

Tracking student progress is essential in determing what a student knows and how fast they'll learn. We achieve this using an altered bayesian knowledge tracing (BKT) algorithm. This algorithm uses Bayes’ “hypothesis testing” to find the probability a student knows a given topic given their MCQ performance. This probability is then taken as the student’s “mastery” or “ability” in a topic.

Once a student is confident in a subject, we want it to stay in their long term memory. Revising at the right times brings down an already heavy workload associated with the leaving certificate programme, so we've focused on maximum recall with minimum revisions. We used an altered version of the free spaced repetition scheduler (FSRS) to achieve this, notifying students when a revision is due at optimal intervals.

We aim to give students a personalised experience on our website. Not everybody learns the same way, or at the same pace. Before we apply any of our algorithms we use a diagnostic process to determine where a student is. Personalised Clustering splits students into categories of initial parameters, including initial knowledge in topics and learning speed. Rather than fitting our model to each specific student, we aim to put them in a larger box of ability. This allows us to cover many different types of students, and ensure accuracy in our assumptions about them.

## Procedural Generation

The leaving certificate curriculum is large and evolving, so similarly our implementation is designed to be scalable and adaptable. We've split the curriculum into 18 separate mathematics topics requiring individual content creation. Using a master blueprint, a carefully constructed prompt document, we dynamically generate all 18 sections.

Our system includes a range of interactive features including graphs, plots, and multiple choice questions. Through the use of smart mapping, we auto-select the most appropriate interactive components for each topic. In total, we’ve developed over 215 topic files to complete the Irish leaving certificate for higher level mathematics. All of our content follows a universal structure, which ensures a consistent pedagogical flow across the website. We organise the topic material and interactive components in the most effective way for student understanding, starting with the theory, then application, visualisation, and finally MCQs.

The benefits of procedural generation are far reaching. Our system is efficient, we are capable of generating complete sections in minutes vs. the hours it would otherwise take. In addition, we are able to ensure the student experience is uniform across the entire curriculum. Most notably, our approach is inherently very scalable, a single update improves all of the content generation on the website.

```{mermaid}
%%{init: {'theme':'base', 'fontSize': '11', 'securityLevel': "loose"}}%%
mindmap
  root((Ecnetica))
    lec1("**2. Algebra 2**")
    ::icon(fa fa-book)
        (Quadraitcs)
        (Factorisation)
        (Polynomials)
```

<!--
## List of Lectures

- [Topic 2 - Algebra 2](algebra_2/algebra_2.ipynb)

  - [Lecture 2
    ](algebra_2/Discriminant.ipynb)
-->
---

## Contact

For Ecnetica or TPSA C.L.G. related queries, contact us at following -

| Name                                  |                               Email                               |
| ------------------------------------- | :----------------------------------------------------------------: |
| TPSA Information                      |               [problemsolving@tpsa.ie](mailto:problemsolving@tpsa.ie)               |
| Michael Mitchell (Director & CEO)     |        [emil.michael@tpsa.ie](mailto:michael@tpsa.ie)        |
| Casey Farren-Colloty (Director & COO) | [casey@tpsa.ie](mailto:casey@tpsa.ie) |
