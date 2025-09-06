# Contents
- how the code works
- system overview
- theory behind the system
# how the mcq choosing algorithm code works

mcq_algorithm, mcqs_custom_study, computed mcqs, knowledge graph and config json files

## McqLoader
the algorithm now has the option to only load in minimal data on mcqs, as things like the text and options aren't actually needed until the question is displayed. The minima loading currently loads id, main topic and subtopic, difficulty and difficulty  skills breakdown, prerequisites and chapter. To get an mcq, this is the function ```mcq = kg.get_mcq_safely(mcq_id, need_full_text=True)```, with the need full text set to true of false depending on which is needed.

## defining classes
MinimalMCqData, Node just define stuff. DifficultyBreakdown should already be in the json, this just makes sure its the right format and calculates the overall difficulty is something is missing. StudentAttempt just is format of attempt.


## BreakdownStep
This includes the functions for managing the breakdown steps, including calculating the generated parameters needed for the steps. They open when a students gets an answer wrong. It renders all the text in the correct format with math, using sympy. The breakdown questions inherit all the parameters from the parent mcq, as well as calculating new ones. If a step directly tests some of the question prerequisites, then that question in the breakdown can be skipped if that topic has a high mastery. This mostly only applies to the first step in a breakdown, as you need to make sure the questions still make sense.



## MCQ
the from_dict function loads in all the information in an mcq from the json file, makes sure its in the right format, has some functions to call stuff.
This also has the bit for generating the random parameters. Has mcq.regenerate_parameters(), mcq.get_current_parameters_safe(). mcq.question_text and mcq.options actually gets the text and options with calculated parameters of they are available.
Generated parameters are generated according to the type they are. It is then checked to make sure they are not 'exclude' values. The calculated parameters are then got based on the randomly generated ones. There is fallback parameters that are just the min values. The question expressions are calculated if needed and then subbed in.
smart_format_number() fixes up the numbers for display, eg gets rid of 2.0, tries to convert them to fractions, else limits them to 4 dp.
create_safe_math_namespace gives the math functions which should be needed in the rest. 

## ConfigurationManager
This deals with the fact that the variables are stored in the config file. Called with get, eg get('bkt_parameters.default.prior_knowledge'). Theres a function to get the bkt parameters.

### student related things
student profile class has their mastery levels and other parameters like that individual to a student. also calculates confidence (our confidence in our estimate of their mastery), which changes with how often they use the website. there’s also a couple of other useful functions here

student manager is for the creating new student, recording attempts and other things that have to do with how students interact with the system

## Knowledge graph
Theres a good bit of stuff here. This loads the nodes and mcqs with _load_nodes/mcqs_from_json. It coverts the dependencies to edges and things. Has some useful functions like get_adjacency_matrix, which also stores it if it hasn't changed, get node degree, etc.
topics are mainly referred to by their index in the code. there's some functions to convert between topic and index and stuff.
## Actual mcq choosing stuff
### OptimizedMcqVector
-just the reduced version for the algorithm.

### MCQScheduler
-does all the actual calculations.

- gets all mcqs for which the main topic and all the subtopics have been studied, the student has not done that day, and has a mastery below the threshold for the main topic.
- select_optimal_mcqs is the main function. Most of the rest are called inside it. if the number of eligible questions is over a limit, it currently just sorts them by mastery and takes the lowest ones, up to that limit. this might be necessary when we have a lot of questions, but it would be better if it wasn't
- only considers topics below mastery threshold
- calculates cost to coverage ratio for each mcq: calculates how much of the main, sub and prereq topics the mcq covers by preforming the bkt updates. calculates difficulty cost based on the question mastery matching the student, and importance factor.
- the best question is chosen. The mastery updates from the bkt are then applied. When this puts a topic over the mastery threshold, that topic is no longer considered.
  (this might eventually end up using what the actual bkt updates would be, this is for now anyway)
-and the whole thing goes again, until all the topics are covered, the max number of questions is reached, or you run out of mcqs
- there is also an early stopping thing currently that stops it if the coverage increase is small. im not sure yet if this is a good thing or not.
- The mcqs are order by grouping each one by node, ordering them by ``` skill_weights =  {
            'memory': 1.0,
            'conceptual_understanding': 1.1,
            'procedural_fluency': 2.0,
            'mathematical_communication': 3.0,
            'problem_solving': 4.0,
            'spatial_reasoning': 4.1
        }```
        The topics are then iterated through, choosing the one with the lowest score from each topic. This means that students start on questions that involve memory and background knowledge, then work through applying this information to more difficult situations. The mixing of topics also promotes memory and means that students have to make the link between the question and what topic it is, which is an important skill for exams.
## BetaInformedEloSkillTracker
This updates the skills of conceptual_understanding, procedural_fluency, problem_solving, mathematical_communication, memory and spatial_reasoning based on a system adapted from the chess elo system. It is on a 0-1 scale. The probability of a student getting a question right is calculated based on their skill level and question difficulty. An update is then applied, depending on how they answered. A more surprising result gets a higher update. Beta-Informed Uncertainty acts as a confidence in our estimate parameter. 

## FSRS and BKT
These are the functions which update the mastery after a question is answered, and decay the mastery with time. Ameilia has more details on them in the BKT_algorithm folder.


# overall how it works
generate mcqs and knowledge graph in json form, maybe change config parameters. run the process mcqs to calculate the overall difficulty, id and prerequisites for the mcqs. then can run the knowledge graph code, with the file names of the three json files. the core functions needed to run it:
```
  kg = KnowledgeGraph(
      nodes_file='kg.json',
      mcqs_file='computed_mcqs.json',
      config_file='config.json'
  )
  student_manager = StudentManager(kg.config)
  mcq_scheduler = MCQScheduler(kg, student_manager)
  bkt_system = BayesianKnowledgeTracing(kg, student_manager)

  # Connect systems
  mcq_scheduler.set_bkt_system(bkt_system)
  bkt_system.set_scheduler(mcq_scheduler)
  student_manager.set_bkt_system(bkt_system)

  #create student (example)
  student_id = "test_student"
  student = student_manager.create_student(student_id)
  import random
  # Set initial mastery levels if you want
  for topic_idx in kg.get_all_indexes():
      mastery = random.uniform(0.1, 0.6)
      student.mastery_levels[topic_idx] = mastery
      student.confidence_levels[topic_idx] = mastery * 0.8
      student.studied_topics[topic_idx] = True

  #select questions
  selected_mcqs = mcq_scheduler.select_optimal_mcqs(student_id, num_questions=1)

  #answer question
 mcq = kg.get_mcq_safely(mcq_id, need_full_text=True)

display questions by mcq.question_text, mcq.question_options. These randomly generate parameters if there is any.

after a student has answered a question process it by:
bkt_updates = student_manager.record_attempt(
    student_id,     # The student's ID
    mcq_id,         # The question ID
    is_correct,     # True/False for the answer
    time_taken,     # Time in seconds
    kg              # Knowledge graph instance
)
this prepares breakdown, applies bkt and area of affect,, fsrs

```

# Custom Study option
This allows for reviews outside of the daily reviews. 
Choices are: 
- Specific chapters
- Specific nodes 
- Specific skills
- focus on weak areas
- simple/ balanced/ challenging difficulty
- review tomorrows due topics
- interleaving: how mixed up topics are at the end
- prerequisite testing: if this is true, for all selected questions, if a prereq topic has low mastery, this is tested first.

Any combination of the above can be chosen, eg 
```
    selected_mcqs = create_custom_study_session(
        kg, student_manager, "student_123", bkt_system,
        selected_chapters=["algebra"],
        num_questions=10,
        skill_focus="procedural_fluency",
        difficulty_preference="challenge"
    )
```

# How the whole system works
A student is initialized with their current studied topics, mastery levels and skill levels. The select_optimal_mcqs algorithm chooses the set of questions the student should study that day, with the goal of getting every topic above the mastery threshold. Questions are ordered in increasing difficulty, but alternating through topics. For each chosen question, randomized parameters are generated and calculated parameters based on them are got. These are subbed back into the text. As students answer questions, their mastery is updated via bkt. Their level on each skill is also updated. If they get an answer wrong, a breakdown opens up, depending on their answer. bkt updates are applied for this, scaled by how many questions were answered correctly, and also a factor to give smaller updates. Skills are given negative updates for each step that is answered incorrectly, with none if answered correctly. If all steps are answered correct, the negative update that would have been applied if the original question was wrong is applied. 

# Theory behind the algorithm
This algorithm balances the most learning with the minimum number of questions with matching the question to the students level. It targets questions that are just above a student's current level. It also adapts to how much the student has used the website, as this changes how confident we are that our parameters match their actual knowledge levels. The parameters it takes into account for the student current mastery, their skills breakdown, our confidence in their knowledge of that topic. It also takes into account the question difficulty, the question difficulty across a range of skills, the subtopics present in the question, the prerequisite topics and the 'importance' of the topic, measured by out-degree of the node.

There is a confidence factor  which measures our confidence in our estimate of the students knowledge. It is determined by the number of questions they have attempted, the time they have used the website for, the consistency of their usage, as well as topic specific parameters number of questions attempted on that topic and time since they last did a question on that topic. This is used to influence matching question difficulty to mastery, low confidence means you prioritise this less and 'bounce students around' more to find their actual levels. 


Assuming spaced
repetition algorithm gives list of topics due for review, with their corresponding mastery levels.
Take given topics to revise, gather all relevant questions. Have a list
of the ids that a student has covered every day and compare this list to
the questions. If any of the questions are on the already studied list,
exclude them.
 Also dot the mcq topics vector with the adjacency matrix to
get prereqs.


Factors that are now being considered:

- the subtopics the question contains

- the direct prerequisites

- the overall difficulty

- the difficulty breakdown

- importance of the question, given by out degree of node 

the ideal question would have:

- to directly cover the topic being tested, of course

- an overall difficulty slightly above the students current- to allow
  them to improve without being too challenging or discouraging

- the difficulty to also be slightly above on each of the skills breakdowns

- to cover as many other topics due for review as possible: limited by
  difficulty so it doesn't become too much

- to cover as many other prereqs due for review as possible
-how important of a topic, to ensure key topics are know really well, they would get tested directly more, rather than as subtopic or prerequisite tests

two possibilities:

Give each component a score and choose the highest score?- easy option
that doesn't necessarily give the least questions needed to cover the
due topics

doting the mcq topic vector by the subtopics/ prereqs vector gives how
much of due topics are covered in the question, with higher weighting
giving a higher number.

$a(\text{subtopics}\cdot\text{due topics})+b(\text{prereqs}\cdot \text{due topics})-c(\text{student knowledge of topic+ some offset - question difficulty})-d(\text{student problem solving level + 2 - q problem solving difficulty}) -f(\text{technical difficulty})-etc$.


or the option we use is constrained set covering optimization problem

## Constrained set covering optimization problem

Basically trying to find the smallest collection of subsets that equals
the set.

We want to optimise it, so get the questions such that they have the
minimum 'cost' and cover the set. This does happen to be an NP-hard
problem ie we are not getting an exact solution. There is an approximate
greedy algorithm that will work well enough. The basic idea of it is at
each step you see how many of the due topics each question covers and
has as prereqs, then take the difficulty stuff and divide it by the
number of topics reviewed. This gives the cost. Choose the question with
the lowest cost and add it to questions to do. Then repeat the process,
seeing how many of the remaining topics a question covers.
[reference: @setcovergfg]




- get all topics with mastery below the threshold
- gather all questions that have these topics as a main topic
- disregards questions already answered that day, and any questions that have topics the student hasn't covered
How this would look in practice:
cost function:$$\frac{\text{difficulty + skills breakdown - importance }}{\text{subtopics}\cdot\text{due topics}+\text{prereqs}\cdot \text{due topics}} $$
with weighting and difference between question difficulty and student mastery as in the first method

The bkt update that would result from answering the question is simulated after each question is chosen. This ensures that questions don't cover the same topic multiple times.

This does have the problem of they have to do a set number of reviews
for it to be the most effective. What way do you choose them if they
feel like doing more?? maybe select three topics with the lowest mastery levels and run it for
them or something?

## concept clustered reviews


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
### identifying chapters (never was actually implemented)
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

The chapter with the highest score should be prioritized for review and depending on the weightings a threshold could be set over which a chapter is due.

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

Alteratively, uuids could be generated for each one. 
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

# references
@online{setcovergfg,
    author = "geeks for geeks",
    title = "Greedy Approximate Algorithm for Set Cover Problem",
    url  = "https://www.geeksforgeeks.org/greedy-approximate-algorithm-for-set-cover-problem/",
    addendum = "(accessed: 28.5.2025)"}
