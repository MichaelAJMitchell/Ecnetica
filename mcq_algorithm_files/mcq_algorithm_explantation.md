# how the mcq choosing algorithm works

mcq_algorithm_current, computed mcqs, knowledge graph and config json files

## McqLoader
the algorithm now has the option to only load in minimal data on mcqs, as things like the text and options aren't actually needed until the question is displayed. The minima loading currently loads id, main topic and subtopic, difficulty and difficulty breakdown, prerequisites and chapter. To get an mcqs, this is the function mcq = kg.get_mcq_safely(mcq_id, need_full_text=True), with the need full text set to true of false depending on which is needed.

## defining classes
MinimalMCqData, node just define stuff. Difficulty breakdown should already be in the json, this just makes sure its the right format and calculates the overall difficulty is something is missing. StudentAttempt just is format of attempt.


## BreakdownStep
This includes the functions for managing the breakdown steps, including calculating the generated parameters needed for the steps. The breakdown questions inherit all the parameters from the parent mcq, as well as calculating new ones. If a step directly tests some of the question prerequsites, then that question in the breakdown can be skipped if that topic has a high mastery. This mostly only applies to the first step in a breakdown, as you need to make sure the questions still make sense.



## MCQ- loading from json
the from_dict function loads in all the information in an mcq from the json file, makes sure its in the right format, has some functions to call stuff.
This also has the bit for generating the random parameters. Has mcq.regenerate_parameters(), mcq.get_current_parameters_safe(). mcq.question_text and mcq.options actually gets the text and options with calculated parameters of they are available.
Generated parameters are generated according to the type they are. It is then checked to make sure they are not 'exclude' values. The calculated parameters are then got based on the randomly generated ones. There is fallback parameters that are just the min values. The question expressions are calcukated if needed and then subbed in.
smart_format_number() fixes up the numbers for display, eg gets rid of 2.0, tries to convert them to fractions, else limits them to 4 dp.

## ConfigurationManager
This deals with the fact that the variables are stored in the config file. Called with . Theres a function to get the bkt parameters.

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
- The mcqs are order by grouping each one my node, ordering them by ``` skill_weights =  {
            'memory': 1.0,
            'conceptual_understanding': 1.1,
            'procedural_fluency': 2.0,
            'mathematical_communication': 3.0,
            'problem_solving': 4.0,
            'spatial_reasoning': 4.1
        }```
        The topics are then iterated through, choosing the one with the lowest score from each topic. This means that students start on questions that involve memory and background knowledge, then work through applying this information to more difficult situations. The mixing of topics also promots memeory and means that students have to make the link between the question and what topic it is, which is an important skill for exams.

## FSRS and BKT
These are the functions which update the mastery after a question is answered, and decay the mastery with time. Ameilia has more details on them in the BKT_algorithm folder.




### testing code
The testing code is now in a different file. It isn't interactive, it just checks that everything works. There is also a simple_breakdown_test(): at the bottom of the mcq_algorithm document.
## overall how it works
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

```

