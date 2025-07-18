# how the mcq choosing algorithm works
more of the redundant code should be gone, but the cover functions needed in python are still currenlty also in the json version. the full python code is also there in case anything is wrong with the other. 
### defining classes
defining node, difficulty breakdown (calculates the overall difficulty from the breakdown- from the json)
mcq dataclass, with imported properties and stuff it calculates.
student attempt. from dict to create mcqs from json file
### config
in python has some bkt defining stuff, then algorithm config is where all the changeable parameters are stored so they can be changed easily. 

in json, all parameters are stored in a json file and configuration manager helps load them in. has some functions for getting them from file every time. 
all the calling parameters should be changed to the new format, but there might be one or two i have missed. 
### student related things
student profile class has their mastery levels and other parameters like that individual to a student. also calculates confidence (our confidence in our estimate of their mastery), which changes with how often they use the website. there’s also a couple of other useful functions here  

student manager is for the creating new student, recording attempts and other things that have to do with how students interact with the system

### knowledge graph
actually defining the knowledge graph. 

in python, the actual information is put in here as a list of the form (topic, chapter, dependencies[(destination node, weight)]). there is a function to actually make the proper graph based on this and assign indexes and stuff. there is also a function to add nodes to this if needed, but if the graph needs to be changed, actually putting it in here is probably best. this also has the actual function that creates the mcqs. it automatically assigns an id, calculates the overall difficulty. there’s also a function that gets only studied topics and some other filtering stuff. the in and out degree are stored for each node because they are used a lot.

it also loads the nodes from a json file. also has the function to load the mcqs from json. 

topics are mainly referred to by their index in the code. there's some functions to convert between topic and index and stuff. 

 this has some graph theory functions, including getting the adjacency matrix and visualising the graph. 

### mcq stuff
the mcq vector is a reduced version of the mcqs for running the choosing algorithm. 

the mcq scheduler class has the actual algorithm: 
- gets all mcqs for which the main topic and all the subtopics have been studied, the student has not done that day, and has a mastery below the threshold for the main topic. 
- select_mcqs_greedy is the main function. if the number of eligible questions is over a limit, it currently just sorts them by mastery and takes the lowest ones, up to that limit. this might be necessary when we have a lot of questions, but it would be better if it wasn't
- only considers topics below mastery threshold
- calculates cost to coverage ratio for each mcq: calculates how much of the main, sub and prereq topics the mcq covers. calculates difficulty cost based on the question mastery matching the student, and importance factor. 
- the best question is chosen. the difficulty of the question is then added to a virtual mastery, along with prereqs and subtopics, as a simple way to remove topics that haven't been covered. when this puts a topic over the mastery threshold, that topic is no longer considered. 
  (this might eventually end up using what the actual bkt updates would be, this is for now anyway)
-and the whole thing goes again, until all the topics are covered, the max number of questions is reached, or you run out of mcqs
- there is also an early stopping thing currently that stops it if the coverage increase is small. im not sure if this is a good thing or not, I haven't really thought about it too much yet. 


### bkt updates
this has ameilia’s bkt updates depending on if questions are answered right or wrong, along with the area of affect propagation of mastery

### mcqs (only in python)
the actual mcqs are then loaded in with the create mcqs function

### testing code
the rest is test code for various things. it creates a student with random masteries, after asking for a name for input. It asks questions and then gives a bunch of statistics. there’s also an independent test of the current mcq algorithm. bar removing some stuff, ive mostly just went with whatever claude gave me for this stuff since it most likely won't end up in the final website version. 
## overall how it works
generate mcqs and knowledge graph in json form, maybe change config parameters. run the process mcqs to calculate their properties (info in the other file). then can run the knowledge graph code, with the file names of the three json files. the core functions needed to run it:
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

  #select questions
  selected_mcqs = mcq_scheduler.select_mcqs_greedy(student_id, num_questions=1)

  #answer question

  #bkt
  bkt_updates = student_manager.record_attempt(student_id, mcq_id, is_correct, time_taken, kg)



```

# static versus dynamic content
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

## dynamic calculating funcions
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