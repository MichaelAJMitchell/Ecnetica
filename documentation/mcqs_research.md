# mcqs structure

the mcqs definitely need to store this information:

- main topic

- other topics it includes (vector)

- question id

- difficulty

- question

- answer options

- correct answer

- explanation

other possibilities:
- links
- difficulty breakdown
- chapter of main topic (for sorting mostly)
- if all topics in chapter have been covered ie can it be asked or not
- way of breaking down the question into subparts if student gets it wrong
current example layout: (dictionary)

(quizData1, {
    text: "What is the discriminant of a quadratic equation \\(ax^2 + bx + c = 0\\)?",
    options: [
        "\\(a^2 - 4bc\\)",
        "\\(b^2 - 4ac\\)",
        "\\(2a + b\\)",
        "\\(b^2 + 4ac\\)"
    ],
    correctIndex: 1,
    explanation: "The discriminant is \\(b^2 - 4ac\\), determining the nature of the roots.",
    difficulty: "Basic",
    topic: "Quadratic Equations",
    relatedTopics: ["Algebra", "Polynomial Equations", "Roots of Equations"],
    link: "https://en.wikipedia.org/wiki/Discriminant"
}, topicUuidGenerator);

-The related topics will be a vector with entries in the columns
corresponding to the topics, with the columns matching that of the
adjacency matrix. The entries will be weighted depending on how much of
each topic is in the question. The entries will add up to one for each
vector so that it is easy to compare them across questions. The entry
with the highest weight should be the main topic node.

-Specifically how to determine the difficultly also needs to be figured
out. Current ideas:

- will relate to/ determine in some way P(T) for BKT (perhaps P(T) some
  combination of difficulty of question and students ability)

- having it on a scale from 0-1 is probably the easiest for comparison,
  or 0-1000 or similar

- basic questions that are asked when the topic is introduced should
  have the lowest score, straightforward testing of knowledge of
  concept, not problem solving required

- exam-level questions should be 0.8/0.9, to allow for harder questions
  to test the knowledge of well-preforming students

- one way to determine difficulty would be to divide the score into
  subtopics. Eg amount of knowledge/memorising required, algebraic/
  technical difficulty, level of problem solving/ critical thinking
  required, level of notation used, how interconnected/multitopic the question is.
  Later how students tend to preform on the question could be a factor.
  While determining these is still not straightforward, they are less
  subjective than a simple difficulty score. Adding up these
  contributions would give an overall difficulty score which could be
  used for comparison. Questions would have to be created in such a way
  that difficulty cannot go above 1, ie this would indicate the question
  is 'too difficult'.

  -this method also allows for the creation of different forms of the
  same question. There would be a base question that asks for
  information in a relatively straightforward way. The question can then
  be made more difficult by altering more of more of the subcomponents
  of difficulty, ie requiring the student to remember more to test
  memory, rewording the question such that more problem solving is
  required/ the method to use is not as obvious, or using notation
  instead of words. Each of these adjustments would make the question
  have a higher overall difficulty, which could be tailored to match the
  students level.

  -level of interconnectedness to other topics/multisubjetness of topic could be determined by
  comparing the weight of the main topic to subtopics. If this weight is
  one, topic interconnectedness is 0. Contributions to this could be limited to subtopics outside of the main topics either chapter or topic, to avoid contributions from closely related concepts.

-question ids this is unique identifiers to keep track of questions and
to prevent repeats of questions in the same session. Two possible
methods:

- take first three letters of highest level clustering of nodes, I'll
  call it chapters for now, and combine this with a randomly generated
  uuid, ie a string of numbers and letters which is basically guaranteed
  to be unique. This allows for a level of interpretability, but to use
  topic names at any lower of a level would become to complicated due to
  long and/or similar names. Example code:

   const IdGenerator = {
    /**
     * Creates topic-prefixed UUID IDs by combining the first three letters of the topic
     * with a UUID v4 for guaranteed uniqueness.
     * @returns {Function} A function that generates an ID when provided a topic string
     */
    topicUuid: function() {
        // Return a function that creates a unique ID for a given topic
        return function(topic) {
            // Input validation
            if (!topic) {
                throw new Error("Topic is required for topicUuid ID generation");
            }

            // Extract the first 3 letters of the topic, lowercased
            const prefix = topic.substring(0, 3).  toLowerCase();

            // Generate UUID v4 using standard algorithm
            const uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.  replace(/[xy]/g, function(c) {
                const r = Math.random() * 16 | 0;
                const v = c === 'x' ? r : (r & 0x3 | 0x8);
                return v.toString(16);
            });

            // Combine prefix with UUID to create format "prefix-uuid"
            return `${prefix}-${uuid}`;
        };
    }
};

- questions could also be classes by the number of the node, followed by
  a shorter unique identifier. Sequential numbering could also be used,
  but that could raise issues if questions are not all generated in the
  same place at once

-The link may or may not need to be included in each mcq. It might be possible to generate it from the information alredy stored in the topics and subtopics. It will link
to the main topic and other included topics decided in some way that is
yet to be figured out. Should it be prerequisites or the subtopics?
Topics with a weighting below a certain threshold can definitely be left
out anyway. How many links should be included? Probably 1-3 depending on
the question- simpler questions will not have other topics but more
complicated ones will.

# basis stuff

example of projecting mcq vector onto knowledge graph basis: given
graph (just having non weighted dependencies for now):


topics algebra, differentiation, geometry, trigonometry and integration
with connections as in adjacency matrix$$\begin{matrix}
    A\\D\\G\\T\\I
\end{matrix}\begin{bmatrix}
    0&1&1&1&0\\
    0&0&0&1&1\\
    0&0&0&1&0\\
    0&1&0&0&0\\
    0&0&0&0&0\\
\end{bmatrix}$$ take a question based on geometry with some integration
and trig:$$\begin{matrix}
    A\\D\\G\\T\\I
\end{matrix}\begin{bmatrix}
    0\\0\\.5\\.3\\.2
\end{bmatrix}$$

multiplying the vector by the adjacency matrix gives: $$\begin{matrix}
    A\\D\\G\\T\\I
\end{matrix}\begin{bmatrix}
    0.8\\0.5\\0.3\\0\\0
\end{bmatrix}$$ This gives how important each of the prerequisites are.
Algebra has the highest weighting as geometry and trig both depend on
it. Note:

-the topics themselves are not included, eg integration now has a weight
of 0

-This only takes into account direct prerequisites, ie it doesn't take
into account that integration depends on algebra.

# choosing mcqs

## Factors to consider:
depends on topics to review and difficulty, how are you factoring in
breakdown of difficulty, making sure no repeats. Need to go
through the bank of questions, choose one that covers the topic that
does not contain any prerequisites the student hasn't covered. Also need
to choose one that matches the students current level of difficulty.
Also need to make sure the same question isn't
asked twice in the same session/day. How many questions do you want to
choose at a time? To what extent can topics further down be used to
cover prerequisites?- weightings. Are you choosing each question after
the one before is done, selecting them in bunches or selecting them all
in one go. One at a time would mean you could update all their knowledge
and stuff between each question, doing it with multiple at a time means
you could try and find the most efficient combination. Can you have
something that is a prereq to a prereq also be a direct prereq? eg if in
the earlier kg integration
also had a direct dependence on algebra (more important when you have
very specific subtopics). You want to try and
choose a question that will revise a few topics at once to optimise
study time.

Would it be possible to have like covered questions and not covered
questions? like either the questions are contained within two lists,
covered or not, or they have a covered property. When a topic is covered
by going through the content or ticking it etc, question moves from not
covered to covered. This gives a bank of covered questions that the mcqs
can be chosen from.
## actual ideas
Assuming spaced
repetition algorithm gives list of topics due for review, ordered based
on 'urgency' (there is probably a better word but I'll use
this for now) if possible.
Take given topics to revise, gather all relevant questions. Have a list
of the ids that a student has covered every day and compare this list to
the questions. If any of the questions are on the already studied list,
exclude them.
Look at student level of knowledge of that topic. Exclude
all the questions that have a difficulty outside of a certain range,
which is a little broad but not massive. Eg if knowledge on scale 0-100,
student has knowledge of 60, keep questions in range 40-80. (this is
very rough better numbers would definitely be needed). From these, see
how many have multiple topics. If student has very low knowledge, they
wont cause that would be above the difficulty level. Also dot the mcq topics vector with the adjacency matrix to
get prereqs.


Factors that are now being considered:

- the subtopics the question contains

- the direct prerequisites

- the overall difficulty

- the difficulty breakdown

the ideal question would have:

- to directly cover the topic being tested, of course

- an overall difficulty slightly above the students current- to allow
  them to improve without being too challenging or discouraging

- the difficulty to also be slightly above on each of the breakdowns

- to cover as many other topics due for review as possible: limited by
  difficulty so it doesn't become too much

- to cover as many other prereqs due for review as possible

two possibilities:

Give each component a score and choose the highest score?- easy option
that doesn't necessarily give the least questions needed to cover the
due topics

doting the mcq topic vector by the subtopics/ prereqs vector gives how
much of due topics are covered in the question, with higher weighting
giving a higher number.

$a(\text{subtopics}\cdot\text{due topics})+b(\text{prereqs}\cdot \text{due topics})-c(\text{student knowledge of topic+ some number eg 2 - question difficulty})-d(\text{student problem solving level + 2 - q problem solving difficulty}) -f(\text{technical difficulty})-etc$.

The constants for each would need to be determined in some way, but im
not sure how. There should probably be a higher weighting towards topics
and overall difficulty than difficulty breakdown.

or another opion is constrained set covering optimization problem

### set cover problems

Basically trying to find the smallest collection of subsets that equals
the set.

We want to optimise it, so get the questions such that they have the
minimum 'cost' and cover the set. This does happen to be an NP-hard
problem ie we are not getting an exact solution. There is an approximate
greedy algorithm that will work well enough. The basic idea of it is at
each step you see how many of the due topics each question covers and
has as prereqs. then take the difficulty stuff and divide it by the
number of topics reviewed. This gives the cost. Choose the question with
the lowest cost and add it to questions to do. Then repeat the process,
seeing how many of the remaining topics a question covers.
[reference: @setcovergfg]

there is also other things that can be considered to optimise learning:
-how important of a topic is it? you might want to cover key topics more.
this can be determined in a couple of different ways:
1. nodes that have high out-degree ie a lot of topics depend on them. This is probably the easiest way.
2. relevance of the topic to learning in the future. can be defined as the number of nodes x such that there exists a path between the current topic and x. This would make sure students are strong at topics which are involved in a lot of topics later on.


How this would look in practice:
cost function:$$\frac{\text{difficulty + difficulty breakdown - importance }}{\text{subtopics}\cdot\text{due topics}+\text{prereqs}\cdot \text{due topics}} $$
with weighting and difference between question difficulty and student mastery as in the first method

dealing with fractional reviews is an issue, how do you say a question
is 'covered' and no longer needs to be considered in the algorithm??


This does have the problem of they have to do a set number of reviews
for it to be the most effective. What way do you choose them if they
feel like doing more?? maybe select three topics with the lowest mastery levels and run it for
them or something?

# concept clustered reviews


 interleaving more efficient science of learning-wise: try to encourage it.


Assuming you have the nodes clustered into levels corresponding roughly
to chapter and concepts. Chapters are roughly textbook chapters.
Concepts would be subchapters and they are then broken down into nodes.
Eg chapter: trigonometry, concepts: trig graphs, solving trig equations,
the unit circle, etc. Nodes: the graph of sin x, the graph of cos x,
reference angles in the second quadrant, etc.

Probably just to cluster reviews at the chapter level. Concept level is
pretty specific- students probably don't care if you tell them they are
reviewing how to solve trig equations-it just gives them a hint into
what they have to do for the questions. These reviews could probably
just be covered under the normal daily reviews.

There is two steps to this: identifying chapters which can have a
cluster review applied, and given a chapter choosing questions. The
second part could also be used to choose questions if a student wants to
study a chapter that we haven't said is due, like if they have a test in
class they want to study for.
### identifying chapters
The easiest way to identify chapters would be to just take the average mastery of all the nodes in that chapter. If the average mastery is below the same threshold you use to trigger reviews for individual nodes, then the chapter is due. Issues: outliers eg very good or very bad topics could impact this. Also doesn't take importance of topic into account.

Also want to take into account:
- how important the topic is
- if it is the cause of weakness down the line
- variation in the mastery within the topic. If their his a high variation, then there is a few very weak topics bringing the score down. These should be already be a priority in the normal mcqs. If there is low variance and also low mastery, then most of the nodes in the chapter are weak and the chapter as a whole would benefit from a review.

Can compute the mastery of all nodes that depend on one node: Gather all nodes that can be reached from a node (depth first search is a method). compute the average mastery of these nodes to give the average mastery of dependant nodes.

variance is (mastery of node - average mastery of chapter)$^2$. This gives the average mastery of a chapter as $$\frac{1}{\text{number of nodes}}\cdot \sum (\text{mastery of each topic - average mastery})^2 $$

This gives a formula for calculating the priority of chapters for review.
$$ a\text{(number of outgoing nodes)(1 - average mastery of nodes in chapter})+b(\text{average of the average mastery of nodes dependant on each node })-c(\text{varience}) $$

(there might be a better way than getting a bunch of averages)

The chapter with the highest score should be prioritised for review and depending on the weightings a threshold could be set over which a chapter is due.

### choosing questions given chapter
Do we want to review all nodes in a chapter? This could end up being a lot, but also given that there is quite a lot of dependencies and interconnectedness on topics that could reduce the number of questions needed significantly.

Could use an adapted version of the scheduler for normal mcqs. Take a vector of due topics as all the topics in the chapter. Instead of ranking by 'dueness', rank from low mastery to high. This takes into account that we want to review nodes even if they are not due. The mastery limit for nodes to be counted as 'completed' should be higher than in normal reviews to ensure that the nodes tht are not due are still covered.

The multisubject nature of a question in the difficulty breakdown should have a lower weight or be disregarded in this review, as that is not what we are testing.

The questions should be ordered by graph depth. The loww levels of mastery of all the chapter might suggest a fundamental misunderstanding, so work from the basics up to build up knowledge.

Other than those, I think the normal algorithm should probably work.

# naming of nodes

There is a bunch of different ways to name the nodes, numbers, letters, strings corresponding to names. With large graphs, the easiest thing is
to just work with the indexes of the matrix and then have a mapping from
each index to the actual name of the node that can be used when needed.
All of the mcq vectors would also follow this indexing. New nodes should
be added at the end, even if they are conceptually somewhere else, as
the code doesn't care about that and rearranging the matrix is a lot
more work. A mapping is done by creating a vector where each of the
entries contains the name of the node corresponding to that index. A
function then related each index to its readable name.

# outstanding questions

- how to generate the related topics vectors- how weights are done, at
  what level is a subtopic to negligible to include

- second, third etc topics for link??

- how exactly is difficulty done: how are you updating the difficulty breakdown???

- question breakdown into subquestions for if they get a question wrong

- will there be an option for students to do more reviews than they are due to?

- taking into account students covering stuff at school/ doing their own
  study- website data isn't accurate picture of their level even after
  diagnostics. confidence depending on how much they actually use the
  website??

  -lots of weights to be determined

  -if a topic is due for review/ has low mastery, do you let students move on to new topics that depend on that one? need to take into account that they may have since done it in school/ revised it themselves

 -  how actually are the nodes going to be clustered?





# references
@online{setcovergfg,
    author = "geeks for geeks",
    title = "Greedy Approximate Algorithm for Set Cover Problem",
    url  = "https://www.geeksforgeeks.org/greedy-approximate-algorithm-for-set-cover-problem/",
    addendum = "(accessed: 28.5.2025)"}
