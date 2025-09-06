# Future Stuff
# What a Successful System Looks Like
- Students should be reviewing topics just as they are about to forget them
- The system needs to balance reviewing questions often enough such that students are able to get most of them right, ie it is just before they should have forgotten the topics, but also we don't want to overwhelm the students with too many questions in a day. I feel like aiming for max ~15 minutes of review questions a day, not counting them doing the ones they have got wrong again, is appropriate, when a student has been using the website consistently.
- We want parameters to be set such that the area of affect updates prerequisite topics by the right amount. If they are updated by too small of updates, students will be prompted to do questions on perhaps basic topics that we know they know, which is not maximizing their time. If prerequisite topics are given too large of updates, too many topics will end up never being prompted for review. Most topics should fall below the mastery threshold for review sometimes, bar some very core/ basic topics such as linear equations, basic math etc. We want to ensure that students are actually explicitly tested on complex topics, but also that by doing reviews through other topics, they won't have to explicitly do questions on simple topics like solving linear questions. A lot of this can be done by how many times a topic appears in another topic. Eg linear equations is part of so many topics that even if the weighting is small, it should be updated a lot. More obscure topics will not be part of so many questions and so should eventually end up being tested explicitly. 
- Confidence parameters should be set so that when we have enough information on the student, the confidence levels on that topic are above the threshold for confidence to influence the selection algorithm. We need to determine what is 'enough questions' to say we are confident in the students mastery levels.
- The greedy algorithm weights need to be determined such that a balance is created between testing the core due topics and all the other parameters. We need to ensure that other parameters have a noticeable impact, but don't eclipse the core testing due topics. How much should covering prerequisites and subtopics actually count towards updating the mastery of that topic? 

## Parameters to be Determined
- BKT parameters
- fsrs parameters
- mastery threshold for review
- chapter mastery threshold: higher so that all bar very strong topics are tested
- confidence parameters
- the weights for the select_optimal_mcqs greedy algorithm
- how high mastery needs to be to skip a breakdown step
- the weights for updating skills
- what is the ideal mastery offset to encourage learning, but not make topics to much above a students level. 
## Future Implementations
### code
- precalculating and storing more properties of nodes such as graph depth and other graph theory things
### improvements to current features
- a scale should be defined in more depth for question difficulty to allow it to be standardised across questions. Should exam level questions come out at about 0.8, to allow harder questions to be asked if you have very capable students?
- an alternative idea i had for calculating question difficulty from the difficulty breakdown was just adding up the components, rather than averaging them. This could then be used to indicate when a question is too hard- if its score goes over 1. The averaging is better i think, but this idea could be used somewhere. 
- using the custom study option: This can be used for a number of things
    - students to select a chapter to review for eg a class test
    - buttons on content pages that allow students to do more questions on those topics
    - revision sessions focused on a specific skill
    - reviewing ahead if they can't do work the next day
    - if they want a specifically easy/ challenging review
- add a number of questions button to the demo
- have a demo for the custom study
- could exclude all the questions that have a difficulty outside of a certain range for a topic,
which is a little broad but not massive. Eg if student has mastery in a topic of 60, keep questions in range 40-80.
- importance for the mcq algorithm is currently measured by out degree, it could be calculated using other graph theory concepts one example is relevance of the topic to learning in the future. can be defined as the number of nodes x such that there exists a path between the current topic and x. This would make sure students are strong at topics which are involved in a lot of topics later on.
- identifying chapters which need a focused review- there is some theory written about it mcqs_algorithm_explanation, but it was not implemented anywhere
- the smart_number_format() function currently limits numbers to 4 decimal places, but this might not be suitable for all questions. 
- could find a way to randomise the order options appear in so students don't learn the order off if they do the same question a couple of times
### new features
- Typing keyboard- use smypy probably, but what way to we expect students to type answers? Build a math keyboard or teach a simplified version of mathjax? This would prevent the fact that students can often just figure out the answer from mcqs by process of elimination, rather than actually doing the question. 
- adding pictures to questions
- adding animations/ interactive graphs- as questions, for actually answering by moving things on the graph or as a tool to aid learning in breakdowns. 
- adding hints- to me these would be simple and aimed at prompting their memory of the first step. Also could include things like the formula for this is in the tables book, or the chapter a question is from if it is ambiguous 
- having an i don't know button or an my answer is not an option button- so they don't have to randomly choose one if their answer isn't there
- having a press to show options so that students are encouraged to do the questions before seeing the answers
- having the cards have and 'is an exam question' property so there can be exam specific custom study
- how do questions on the actual page work with the algorithm?
- the questions could store links to the page this topic is covered on, to allow the students to be linked back to that page at the end of a session if they need to revise it. Alternatively the linked could be constructed such that they can be gotten from the chapter, clustering and node names. 
- what should an ending page look like after students have done a set of questions? I think i should give a summary of topics which were answered wrong and then link back to the pages related to those topics for students to revise. It could also maybe contain summaries of those pages. 
    - if we have an ending page, should prerequisites or subtopics of incorrect questions be included, or just the main topic?
- when do you count a topic as studied? The algorithm currently disregards any questions that have a topic  or subtopic that has not been marked as studied. There will have to be an element of asking the student to update when they have covered certain topics in class. This will probably be at the chapter level, so there maybe could end up being topics that are either marked as topics before they are studied or else miss out on being marked as studied. 
    - This could be automated slightly by getting data on the order that teachers usually cover topics in, as their is probably a couple of main ways. This could be part of the initial clustering and then you could maybe prompt students with we think you're currently covering this topic is this right? Students could also be able to check of topics to unlock them to study ahead.  
    - Studied topics could also be updated when students read through the corresponding content page, either automatically or by a button

- do you have some mechanism for if a student just cannot get a topic right, do you eventually just like leave it?
- if a topic is due for review/ has low mastery, do you let students move on to new topics that depend on that one? need to take into account that they may have since done it in school/ revised it themselves

- review session after students finish questions. There should then be an option to do more questions on the topics students got wrong, ideally after they have revised the topics. I think this should have the same question (possible to do again with the same numbers and then again with new numbers), and then another question from that node of similar or slightly higher difficulty. 
## Things we could implement when we have student data
- student performance on a question could be a factor in the difficulty breakdowns. 


