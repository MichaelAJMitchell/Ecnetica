# 1 Classical Bayesian Knowledge Tracing
Bayesian Knowledge tracing uses Baye's formula to assess the probability a student knows a skill given their performance on questions. It's a good choice for our purposes because it can be implemented and extended in a straightforward manner.

Classical BKT assumes:
each question relates to one skill, an answer is either right or wrong (no partial marks), students don't forget once they have learned, and the question difficulty is uniform.

To run the algorithm we must choose a set of **initial parameters**
- $P(L_0)$ probability student knows skill beforehand,
- $P(T)$ probability student will switch from knowing skill to not knowing it after doing a question,
- $P(S)$, "Slip", probability a student knows it and gets the question wrong,
- $P(G)$, "Guess", probability a student doesn't know it and gets the question right.

## 1.1 The Algorithm

Firstly, the probability that the student knows the skill is initialised.
$P(L_1)^k_{u}=P(L_0)^k$

The probability a student knows a skill at time t given they answered the question correctly, or incorrectly, can be calculated using the formulae below.

$P(L_t | Corr)=\frac {P(L_t)(1-P(S))}{P(L_t)(1-P(S))+(1-P(L_t))(P(G))}$

$P(L_t | Incorr)= \frac{ P(L_t)P(S) }{ P(L_t)P(S) + (1-P(L_t))(1-P(G)) }$
    
These conditional probabilities are then used to update the probability the student knows the skill. In the formula below, "result" is a placeholder for either correct or incorrect given the student action.

$P(L_{t+1})= P(L_t| Result) + (1-P(L_t| Result))P(T)$  &nbsp; [1.1]

We can use the above probability then to find the probability of a student getting a question correct in the future. This can be used to investigate if our model is working correctly.

$P(Corr_{t+1})= P(L_t)(1-P(S)) + (1-P(L_t))P(G)$

## 1.2 Choosing Initial Parameters

Model degeneracy is avoided by effectively choosing parameter values for Guess and Slip
(1995 Corbett, Anderson $P(G)<0.3$, $P(S)<0.1$). To choose the initial parameters, a brute force approach can be considered.

BKT-BF (Bayesian Knowledge Training Brute Force) &nbsp; [1]

- Parameter range [0,1] split into chosen intervals
- Creates grid of parameter combinations
- Runs BKT model on training data, for each combination
- Identifies which choice maximises prediction accuracy

BKT-BF is computationally intense but it finds the global optimum.

# 2 Changes to Classical BKT

## 2.1 Question Difficulty

In order to give students questions that are appropriate to their level we should consider question difficulty. For example If $P(L_t)$ is low, we should give the student "easier" questions. We can also note that if a student gets a hard question right, that shouldn't change $P(L_t)$ the same as an easy question.

There's several solutions to this problem that we can look at.

- **KT-IDEM**
Each question is given its own guess and slip values.The KT-IDEM model adds an “item” node so that question $i$ has $P(G)_i$ and $P(S)_i$. Harder questions are modeled with a lower guess probability or higher slip probability. This method has been shown to improve prediction accuracy &nbsp; [2].
- **Variable P(T)**
The motivation for this approach comes from the update formula eq[1.1] and the idea of a "learning curve". Like KIT-IDEM each question has its own $P(T)$. Here, $P(T)$ should be lower for harder questions. This is because a student is unlikely to learn a lot of new information from a hard question  &nbsp; [3].

*Note: This method is only effective if we're giving students questions of appropriate difficulty.*

The actual difficulty value itself can be measured in multiple ways. For example, we might be able to gauge the difficulty of a question by its number of prerequisites/lack of post-requisites, this lines up with the idea of a "learning curve".

## 2.2 Forgetting

We can add forgetting to the BKT model in two major ways,
- **Forgetting Parameter**
Introduce a forget probability $f$, which is the probability the student switches from knowing the skill to not knowing it. Then the latent update becomes $P(L_{t+1})= (1-f)P(L_t| Result) + (1-P(L_t| Result))P(T)$. Its been shown that enabling even a small f significantly improves fit &nbsp; [3].
    
- **Time-Dependent Decay**
First compute a decayed mastery with time since last update $\Delta t $, $P'=P(L_t)e^{-\lambda\Delta t}$, then do the usual learning update, $P(L_{t+1})= P' + (1-P')P(T)$. This models the “Ebbinghaus forgetting curve” effect and has been implemented before &nbsp; [4]. This continuous approach is a more realistic model of forgetting and is nicer to implement.

# 3 Diagnostic and Mastery

We can define a student's mastery of a certain skill as $P(L_t)$. We use a diagnostic process to choose an appropriate $P(L_0)$. There's a few routes to take here, 

- Giving a student a question on a topic and if they get it right we give $P(L_0)$ a higher value. This has been tested before and has been shown to improve the accuracy of the algorithm &nbsp; [3]. We can use this in combination with our difficulty metric, if a student gets a hard question right they likely have a high $P(L_0)$.
    
- Asking a student what topics they think they've covered. If they say they've covered it we give them a higher $P(L_0)$. Our confidence in their statement is affected by what they are expected to know (topic difficulty). The confidence affects how much we'll higher the $P(L_0)$.

Both of these implementations are feasible depending on the required level of specificity.

# References

[1] Zachary Pardos Anirudhan Badrinath Frederic Wang. pyBKT: An Accessible Python
Library of Bayesian Knowledge Tracing Models. url: https://educationaldatamining.
org / EDM2021 / virtual / static / pdf / EDM21 _ paper _ 237 . pdf# : ~ : text = of %
20prior%2C%20learn%2C%20guess%2C%20and,hybrid%20model%20using%20regression%
20to. (accessed: 15.5.2025).

[2] Baker. BKT-BF. url: https://github.com/pcla-code/BKT-BF. (accessed:
13.5.2025).

[3] Okan Bulut et al. “An Introduction to Bayesian Knowledge Tracing with pyBKT”.
In: Psych 5.3 (2023), pp. 770–786. issn: 2624-8611. doi: 10.3390/psych5030050.
url: https://www.mdpi.com/2624-8611/5/3/50.

[4] Prema Nedungadi and M.s Remya. “Incorporating forgetting in the Personalized,
Clustered, Bayesian Knowledge Tracing (PC-BKT) model”. In: Proceedings - 2015
International Conference on Cognitive Computing and Information Processing, CCIP
2015 (Apr. 2015). doi: 10.1109/CCIP.2015.7100688.
