# Approach and Implementation Regarding BKT

This document outlines specifically the chosen route to applying BKT. It describes in words how I've applied the research in the last document practically to the prototype, and why I've taken each approach. The prototype itself may undergo some changes, but this file goes over what I hope to achieve.


# 1 Diagnostic Algorithm

The first question to tackle is, how do we measure a student's skill level before any training has taken place?
The most effective method would be likely a combination of some previously discussed choices.

## 1.1 What Have they Covered?

This question can be split into two parts, the first being, what does the student think they've covered? We can answer this simply by having students choose topics they believe they've covered out of a given list. We want to minimise effort on the students part here, so this would require clustering nodes under umbrella chapters.

The next question is, what should they know? If a topic has a large number of post-requisites, it's likely to be a simple or important topic. If a student says they know a topic like this we should be willing to believe them more than we would if they say they're comfortable with an advanced topic. In practice this means we consider 'graph depth' on our knowledge graph.

If a student says they've covered a topic we respond to this by giving them a higher initial $P(L_0)$ (mastery). The amount we raise it by ( $\Delta P(L_0)$ ) will be based on graph depth (number of prerequisites, R). 

To figure out the relationship between graph depth and $\Delta P(L_0)$ we should consider a few things:
We should never ignore the student completely- this means $\Delta P(L_0)$ will approach 0 but never hit it. We also assume this relationship is trending down and has no bumps, since there shouldn't be a jump in $\Delta P(L_0)$  for intermediate topics. These two observations point us to something like an exponential decay, subject to some constant.

$\Delta P(L_0)= Ae^{-\lambda R}$

The **sigmoid** function fits this description inversely which comes naturally from the last statement but might prove to be useful.

$\frac{1}{\Delta P(L_0)}=A\frac{1}{1+e^{-\lambda R}}$

The sigmoid function is interesting because its derivative takes on the shape of a normal distribution. This could prove useful to us in making guesses about student initial knowledge.

Another small note is if a student says they've covered a topic, the  essential prerequisites of that topic should also recieve an update.

## 1.2 Testing

Finally, we should test our guesswork. Ideally, questions should be chosen in order of a topic's number of prerequisites (high to low), that way we cover more topics with less input from the student.
A possible way to go about this could be asking the student questions down different prerequisite lines until they get one right.

Here we could make use of the guess and slip probabilities, $P(G)$ and $P(S)$, which will be predetermined in order to allow for the possibility that a student does indeed deserve a mastery update after getting a question wrong, or vice versa.

## 1.3 Graph Depth

A new parameter we've introduced is the 'graph depth' of a node. This describes the number of edges in the longest path back to the root node. There are multiple approaches to finding this value but one of the most common ways of solving this problem is through simple graph traversal.

**Depth First Search** (DFS) is a method by which we can find all paths from any given node to another in a graph. It has a linear computational complexity based on the number of nodes (N) and edges (E), O(N+E), which is why it's useful for large graphs. The algorithm functions by travelling down all the edges connected to a given "root node", and storing the nodes it passes 'til it reaches the end of each branch.

This simple algorithm allows us to find the graph depth of a given node quickly by checking the number of edges in its path back to the root node. The information gained from this search also allows us to perform mastery updates on related topics after a question is answered on a given subject. Another use for this data is to create "personalised learning paths" that focus on the topics students are likely to find engaging, eg. geometry route for students into architecture.

## 1.5 Personalised Clustering

Although the previous sections will help us determine the initial mastery spread of a new student, we are sort of shooting in the dark as to whether the guesses we're making are particularly accurate or not. We're making an educated guess as to what the student has covered but that doesn't tell us the fine details, for example, how comfortable a student really is with a topic. It's much more efficient to use this information to instead try to categorise students into predetermined models (pre-lit knowledge graphs), such that we can work backwards from student behaviour to find the initial parameters.

One of the ways we can achieve this is personalised clustering. In this approach, we create categories of initial parameters. Then we build rough models based on them. After we have built our models, when we test a given student we don't try to find their specific initial parameters, but instead try and fit them into a pre-defined category. From there, the parameters can be made more specific.

This is a tested method that has been shown to produce favourable results. I think rather than aiming to completely nail the specific values for a student we should instead aim for smaller and smaller intervals, for the longer we have them on the site. We should also allow for a confidence parameter that depends on how long it has been in days since their last log in. We can't necessarily assume the student won't have covered more topics, or studied more in their own time.

# 2 Altered Bayesian Knowledge Tracing 

Here we outline the major ways in which the classical BKT algorithm discussed in the research document will be changed for our purposes.

## 2.1 Question difficulty

In practice, the most reliable method to address question difficulty is by varing guess and slip parameters ($P(G), $P(S)$). The use of this is fairly intuitive, if a question is difficult a student is more likely to make a mistake and less likely to guess the answer, than for an easy question.

Previously, we discussed using $P(T)$ to inform question difficulty but in practice that hasn't been very straightforward. Instead, I think $P(T)$ could be used to inform topic "learning curves". Some topics are perhaps more dense or more inherently conceptually difficult than others, for example statistics is usually challenging for leaving cert students. This affects how much a student can actually learn from getting a question wrong/right, i.e the probability a student changes from not knowing to knowing a topic after an MCQ. For that reason, I believe $P(T)$ is a faithful representation of that concept.

Since $P(T)$ is topic based it can be used to inform $P(L_0)$. P(T) can be used to make a backward inference about mastery,

$P(L_{t+1})= P(L_t| Result) + (1-P(L_t| Result))P(T)$  &nbsp; [1.1]

## 2.2 Multiple skills per question

Here we can just use the weights attached to the MCQ, by normalising the vector, and spreading out the total mastery update onto different topics. Eg, if a question is based on one topic then we just have $P(L_{topic})=1(P(L_t))$, if its based on two with equal weights then, 
$P(L_{topic1})=\frac{1}{\sqrt{2}}(P(L_t)), \ P(L_{topic2})=\frac{1}{\sqrt{2}}(P(L_t))$ 

This might not be exactly the best approach but I think it's a reasonable start. This can be altered once we get a bit more data on its effectiveness. Another point to mention is this might not interface nicely with our "area of effect" approach [2.4.1] for related topic updates. If two topics are in the same question, but are closely related, we may end up over-updating those topics. The main solution here is just to keep skills reasonably distinct, by that I mean, by the time the area of effect actually gets to them it will be a negligible difference. 

## 3 Spaced Repetition

## 3.1 Forgetting Curves

The general model for forgetting we'll be using is the **Ebbinghaus Forgetting Curve** which describes the exponential decay in mastery in our case. The curve is based on the following equation, where R is the retrievability or memory retention, t denotes the time elapsed since learning, and S signifies the strength of the memory.

$R = e^{–t/S}$ &nbsp; [2.1]

Repeated review and building on prior knowledge should flatten the curve, i.e memory strength should grow after revision and decay according to a function of time. 
The implementation of this is straightforward with $\Delta t$ being the time since last answering a question and $C=\frac{1}{S}$. We also introduce the constant of initial retention $R_0$.

$R = R_0e^{– C \Delta t}$

Then the mastery is simply continuously updated such that it decays appropriately, ( in this case t is defined as time directly and **not** as a "tick" like in the case of eq.[2.2])

$P(L_{t+\Delta t}) = P(L_t)R_0e^{– C \Delta t}$

If no revision has taken place we should see an increase in our parameter $C(t)$ according to some function of time.

This is the analytical explanation of memory, and can be applied for a simple decay case. This might be a favourable option if we're more concerned with computation time and consistency than accuracy.

## 3.2 FSRS ###

If we care more for accuracy we should consider some algorithms already employed by learning software, eg. super memo and FSRS. The **Free Spaced Repetition Scheduler** (FSRS) is a spaced repettition algorithm proven to be 20-30% better at predicting when revisions are due than Super Memo 2 (SM-2). 

FSRS is a spaced repetition aglorithm based on three components of memory: DSR (Difficulty, Stability, Retrievability) 

- Retrievability (R): The probability that the person can successfully recall a piece of information at a given moment. It depends on the time elapsed since the last review and the memory stability, R(t,S). 

- Stability (S): The time, in days, required for R to decrease from 100% to 90%. 

- Difficulty (D): How difficult it is to increase memory stability after a review. In FSRS, it affects how fast stability grows after each review. 

The value of R changes daily, while D and S change only after a review. Generally, these parameters are found by looking at a user's past performance and fitting it to that data. This is again part of the "cold start" problem we'll be dealing with, and should be something looked at in the diagnostic process.  There's more details on this algorithm in its current state listed here https://expertium.github.io/Algorithm.html .


### 3.2.1 Advantages ####

One of the primary advantages of FSRS is its accuracy. FSRS makes accurate predictions about forgetting curves because it includes more nuance than the classic Ebbinghaus case. The brain retains information via several processes, this means we deal with multiple memory components. When we're dealing with multiple memory components we have more than just one exponential decay, we actually have the average of all of them. This implies rather than using an exponential curve we should be using power functions, which accurately approximate the average of exponential functions.

Another crucial advantage of FSRS is its flexibility. Not every question has the same difficulty, and FSRS allows us to account for that without limiting the study of the student to only one type of question. We need flexibility in our case, because learning mathematics is not the same as studying for a history test, it's done through learning methods rather than details. Seeing a method in different contexts is just as important as practising it over and over.

The final advantage of FSRS is simply that it integrates nicely with the BKT system. Very little extra work has to be done to implement the FSRS method into our existing BKT prototype. I'll go into more detail on this point in this section regarding the actual implementation.

### 3.2.2 Implementation ####

Firstly, we'll discuss how the DSR model interfaces nicely with the current BKT implementation.

The difficulty of a question is already something we've discussed at great length, and something we have data on. Since we already have difficulty as a descriptor for our MCQs we can use this same value to infer difficulty for the FSRS model.

Retrievability is a parameter that be quickly derived by definition from a value we have already been working with. Since retrievability in the classic card case is the chance a student will successfully recall a piece of information (get a flashcard right), in our case it's the chance a student will answer an MCQ correctly.

$R= P(Corr) = P(L_t)(1-P(S)) + (1-P(L_t))P(G)$
 
Since we want the mastery (student knowledge) to reflect that they may have forgotten a topic, we can just rearrange for mastery decay.
 
$P(L_t)= \frac{R-P(G)}{1-P(S)-P(G)}$

Finally, stability is the parameter that will actually control the forgetting process. It doesn't have any direct analogy with the BKT system because its a new parameter that we'll be using to define forgetting.

The FSRS model itself is largely empirical. This means much of the model is specifically tailored to the card memorisation use case. For this reason, it isn't as straightforward for us to just copy down the parameters used in the existing FSRS implementations. So the approach we've chosen to take for now, is instead to create a model inspired by the main components of FSRS, with our own values. 

As a sidenote, it may turn out to be more accurate to just use the existing work on FSRS, we can test this later. Self-correcting algorithms are also something we can take from the existing body of work, which will help us ensure we use correct values for each component.

The revision questions themselves should include previously covered methods. A good way to do this, is to provide them with questions of the same format with variable numbers. This ensures students aren't memorising the questions, but instead the methods. These questions should be kept simple and straightforward. We also want to test for recognition of the method, so we'll additionally include a question that calls upon the method in some unique way.

### 2.3.2 The Analyitical Approach ###

Although this is worth discussing, I don't believe we'll be able to reasonably implement the suggestion below. If you're reading the document to get an idea on where the prototype is headed this may be something to skip. I think this sidenote is worth keeping however, because having an analytical basis behind our approximations is a good idea.

Forgetting is not just a singular brain process, it differs depending on what exactly a student is forgetting. The learning difficulty is a parameter that might not be as straightforward as taking it from the BKT model.

We can define learning difficulty like so: Total cognitive load = Intrinsic load + Extraneous load + Germane load. This is one way to represent the complexity of a topic, i.e how hard it'll be to increase stability upon reviewing it.

The code below goes over how we would implement something like this into the knowledge graph we have.

D_analytical = f(intrinsic_load, extraneous_load, germane_load)

def estimate_analytical_difficulty(mcq, kg):
    # Intrinsic cognitive load
    intrinsic = concept_complexity(mcq.topic_index, kg)
    
    # Extraneous load from prerequisites
    extraneous = prerequisite_load(mcq.topic_index, kg)
    
    # Germane load from interconnections
    germane = connection_complexity(mcq.topic_index, kg)
    
    # Combine using cognitive load principles
    total_difficulty = intrinsic + extraneous * 0.7 + germane * 0.3
    return normalize_to_scale(total_difficulty, 1, 10)

def concept_complexity(topic_index, kg):
    """Analytical complexity based on graph properties"""
    node = kg.get_node_by_index(topic_index)
    
    # Mathematical complexity indicators
    abstraction_level = count_prerequisite_layers(topic_index, kg)
    notation_density = analyze_notation_complexity(node.topic)
    proof_steps = estimate_proof_length(node.topic)
    
    return weighted_sum([abstraction_level, notation_density, proof_steps])

def prerequisite_load(topic_index, kg):
    """Working memory load from prerequisite management"""
    prerequisites = kg.get_prerequisites(topic_index)
    
    # Miller's 7±2 rule: penalty for exceeding working memory
    base_load = len(prerequisites)
    memory_penalty = max(0, len(prerequisites) - 7) ** 1.5
    
    # Weight by prerequisite strength
    weighted_load = sum(weight for _, weight in prerequisites)
    
    return base_load + memory_penalty + weighted_load


There are three main types of memory we can consider: working memory, hippocampal memory, and neocortal memory. Working memory relies on temporary, active maintenance of information, while long-term memory involves the gradual consolidation and storage of memories in the hippocampus and neocortex. Generally episodic memories are maintained in the hippocampus, while generalized memories are stored in the neocortex. If we want to analytically represent memory, we can average together exponential decays in all of these areas. 


## 4 Knowledge Spread

### 2.4.1 Area of Effect Approach ###

When a certain topic is practised, similar topics on the knowledge graph should also recieve a mastery update. A kind of dispersion approach from the centre node is a simple way to compute this knowledge spread. This updates the surrounding topics in a given radius, i.e path length on the knowledge graph. The algorithm finds the node and then temporarily makes the kg undirected. Then, it looks at all paths sprouting from that node and keeps note of the distance traveled. The mastery in the surrounding nodes is updated as,

$P(L_{t+1})= P(L_t) + \Delta P(L_t)((path \ weight)*(propagation)^{(path \ length))}$

The "path weight" is the weights of all the connections in a given path multipled together. The "propagation" $\in (0,1)$ is a chosen parameter that decides how much you want a hop of distance to decay the updated mastery, eg. the current chosen value is 0.5. The mastery updates also only propagate on correct answers at the moment.

Something we may want to consider about this method is some nodes may end up getting updated far too much, without ever actually being learned, leading to much higher initial masteries. This is a problem I'm still looking at, but an idea might be to but a cap or control on how many updates an unlearned topic can actually recieve.

