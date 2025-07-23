# how the mcq choosing algorithm works

mcq_algorithm_current, computed mcqs, knowledge graph and config json files

## McqLoader
the algorithm now has the option to only load in minimal data on mcqs, as things like the text and options aren't actually needed until the question is displayed. The minima loading currently loads id, main topic and subtopic, difficulty and difficulty breakdown, prerequisites and chapter. To get an mcqs, this is the function mcq = kg.get_mcq_safely(mcq_id, need_full_text=True), with the need full text set to true of false depending on which is needed. 

## defining classes
MinimalMCqData, node just define stuff. Difficulty breakdown should already be in the json, this just makes sure its the right format and calculates the overall difficulty is something is missing. StudentAttempt just is format of attempt. 

## MCQ- loading from json
the from_dict function loads in all the information in an mcq from the json file, makes sure its in the right format, has some functions to call stuff. 
## ConfigurationManager 
This deals with the fact that the variables are stored in the config file. Called with . Theres a function to get the bkt parameters. 

### student related things
student profile class has their mastery levels and other parameters like that individual to a student. also calculates confidence (our confidence in our estimate of their mastery), which changes with how often they use the website. there’s also a couple of other useful functions here  

student manager is for the creating new student, recording attempts and other things that have to do with how students interact with the system

## Knowledge graph
Theres a good bit of stuff here. This loads the nodes and mcqs with _load_nodes/mcqs_from_json. It coverts the dependencies to edges and things. Has some useful functions like get_adjacency_matrix, which also stores it if it hasn't changed, get node degree, etc. 
topics are mainly referred to by their index in the code. there's some functions to convert between topic and index and stuff. 
## Actual mcq choosing stuff
OptimizedMcqVector is just the reduced version for the algorithm. 

MCQScheduler does all the actual calculations. 

- gets all mcqs for which the main topic and all the subtopics have been studied, the student has not done that day, and has a mastery below the threshold for the main topic. 
- select_optimal_mcqs is the main function. Most of the rest are called inside it. if the number of eligible questions is over a limit, it currently just sorts them by mastery and takes the lowest ones, up to that limit. this might be necessary when we have a lot of questions, but it would be better if it wasn't
- only considers topics below mastery threshold
- calculates cost to coverage ratio for each mcq: calculates how much of the main, sub and prereq topics the mcq covers. calculates difficulty cost based on the question mastery matching the student, and importance factor. 
- the best question is chosen. the difficulty of the question is then added to a virtual mastery, along with prereqs and subtopics, as a simple way to remove topics that haven't been covered. when this puts a topic over the mastery threshold, that topic is no longer considered. 
  (this might eventually end up using what the actual bkt updates would be, this is for now anyway)
-and the whole thing goes again, until all the topics are covered, the max number of questions is reached, or you run out of mcqs
- there is also an early stopping thing currently that stops it if the coverage increase is small. im not sure yet if this is a good thing or 

## FSRS and BKT
These are the functions which update the mastery after a question is answered, and decay the mastery with time. Ameilia has more details on them in the BKT_algorithm folder. 




### testing code
The testing code is now in a different file. It isn't interactive, it just checks that everything works. 
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

```




# static versus dynamic content (old stuff)
Things that do/don't change once you've imported the knowledge graph and mcqs

## completely static stuff
- node class
- bkt config
- algorithm config

## stuff that has to be calculated once and then can be stored
- difficulty breakdown class
- mcq class
- bkt parameters class
- knowledge graph class 
- mcq vector class
- the actual mcqs 
### static packages
- matplotlib: just for visualising the graph
- also networkx 
- uuid: for generating mcq ids


## dynamic content
- student profile class
    - mastery_levels
    - confidence_levels
    - studied_topics
    - completed_questions
    - daily_completed
    - tracking fields like questions attempted, time on system, last active, etc
- student manager class
    - students
    - active sessions

- student attempt (i think)

## dynamic calculating functions
- mcq scheduler
- bayesian knowledge tracing class
### dynamic packages
- numpy: for a lot of things, bkt, mcq calculations, adjacency matrix, etc
- datetime: for recording when sessions happen to get stats and stuff
- networkx is used in the area of affect propagation
- json for importing stuff


the rest after that in the code is just testing stuff and not that important for the website
### other packages
- random only using in testing to generate random masteries
- from typing import Dict, List, Set, Tuple, Optional, from dataclasses import dataclass, field  
  these are used kind of everywhere, but for formatting rather than actually calculating things