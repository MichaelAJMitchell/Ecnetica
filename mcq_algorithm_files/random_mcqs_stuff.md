# Where we are at
The mcq algorithm
## Pedagogy of the mcq algorithm
### Selection algorithm
This algorithm balances the most learning with the minimum number of questions with matching the question to the students level. It targets questions that are just above a student's current level. It also adapts to how much the student has used the website, as this changes how confident we are that our parameters match their actual knowledge levels. The parameters it takes into account for the student current mastery, their skills breakdown, our confidence in their knowledge of that topic. It also takes into account the question difficulty, the question difficulty across a range of skills, the subtopics present in the question, the prerequisite topics and the 'importance' of the topic, measured by out-degree of the node.

There is a confidence factor  which measures our confidence in our estimate of the students knowledge. It is determined by the number of questions they have attempted, the time they have used the website for, the consistency of their usage, as well as topic specific parameters number of questions attempted on that topic and time since they last did a question on that topic. This is used to influence




# Future Stuff
# What a Successful System Looks Like
- Students should be reviewing topics just as they are about to forget them
- The system needs to balance reviewing questions often enough such that students are able to get most of them right, ie it is just before they should have forgotten the topics, but also we don't want to overwhelm the students with too many questions in a day. I feel like aiming for max ~15 minutes of review questions a day, not counting them doing the ones they have got wrong again, is appropriate, when a student has been using the website consistently.
- We want parameters to be set such that the area of affect updates prerequisite topics by the right amount. If they are updated by too small of updates, students will be propmeted to do questions on perhaps basic topics that we know they know, which is not maximising their time. If prerequiste topics are given too large of updates, too many topics will end up never being prompted for review. Most topics should fall below the mastery threshold for review sometimes, bar some very core/ basic topics such as linear equations, basic math etc.
- Confidence parameters should be set so that when we have enough information on the student, the confidence levels on that topic are above the threshold for confidence to influence the selection algorithm. We need to determine what is 'enough questions' to say we are confident in the students mastery levels.
- The greedy algorithm weights need to be determined such that a balance is created between testing the core due topics and all the other parameters. We need to ensure that other parameters have a noticeable impact, but don't eclipse the core testing due topics.


## Parameters to be Determined


## Future Implementations
- Hide options
- Typing keyboard
-
