# json
### form they can be generated in`
```
    {
      "text": "What is the discriminant of the quadratic equation $2x^2 - 5x + 3 = 0$?",
      "options": [
        "$1$",
        "$7$",
        "$13$",
        "$-1$"
      ],
      "correctindex": 0,
      "option_explanations": [
        "Correct! $\\Delta = b^2 - 4ac = (-5)^2 - 4(2)(3) = 25 - 24 = 1$",
        "Incorrect. Remember the formula is $b^2 - 4ac$, not $b + 2ac$.",
        "Incorrect. You may have calculated $b^2 + 4ac$ instead of $b^2 - 4ac$.",
        "Incorrect. Check your arithmetic: $25 - 24 = 1$, not $-1$."
      ],
      "main_topic_index": 17,
      "chapter": "algebra",
      "subtopic_weights": {
        "17": 1.0
      },
      "difficulty_breakdown": {
        "conceptual_understanding": 0.3,
        "procedural_fluency": 0.7,
        "problem_solving": 0.2,
        "mathematical_communication": 0.1,
        "memory": 0.4,
        "spatial_reasoning": 0.0
      }
    }
```
### form they will be converted to
```
{
      "id": "d8f6f656-c7d6-45a6-ab5d-c180e0e646f1",
      "text": "Using the quadratic formula, solve $x^2 + 6x + 9 = 0$.",
      "options": [
        "$x = -3$ (repeated root)",
        "$x = 3$ or $x = -3$",
        "$x = 0$ or $x = -6$",
        "No real solutions"
      ],
      "correctindex": 0,
      "option_explanations": [
        "Correct! $x = \\frac{-6 \\pm \\sqrt{36-36}}{2} = \\frac{-6}{2} = -3$ (discriminant = 0)",
        "Incorrect. The discriminant is 0, so there's only one repeated root.",
        "Incorrect. Substitute into the quadratic formula: $x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$",
        "Incorrect. The discriminant is 0, which means there is exactly one real solution."
      ],
      "main_topic_index": 15,
      "chapter": "algebra",
      "subtopic_weights": {
        "15": 0.8,
        "17": 0.2
      },
      "difficulty_breakdown": {
        "conceptual_understanding": 0.4,
        "procedural_fluency": 0.8,
        "problem_solving": 0.5,
        "mathematical_communication": 0.2,
        "memory": 0.6,
        "spatial_reasoning": 0.0
      },
      "overall_difficulty": 0.4166666666666667,
      "prerequisites": {
        "16": 0.6400000000000001,
        "17": 0.5599999999999999
      }
    }
```
if you take the mcq document and run them through the process mcqs python file, it automatically calculates the id, prerequisites and difficulty and them saves them in another json file, which is the one actually used for the mcq algorithm. it also calculates the chapter from the topic for the main node.

# python
## mcqs structure (old but explanations still the same)


```
@dataclass
class MCQ:
    text: str
    options: List[str]
    correctindex: int
    option_explanations: List[str]  #  Individual explanations for each option
    main_topic_index: int
    chapter: str
    subtopic_weights: Dict[int, float]  #Manually specified weights
    difficulty_breakdown: DifficultyBreakdown
    id: str
    _prerequisites: Optional[Dict[int, float]] = field(default=None, init=False)
    _difficulty: Optional[float] = field(default=None, init=False)
```







## mcqs explicit content
### question (text)
the question stores the information the student will see when they are asked a question. Questions should range in content from simple definitions and applications designed to test if the students have a basic understanding of the core concept, to questions testing more tricky or complex aspects of the topic, including incorporating other topics.
    variations of the questions can be made by taking a basic questions and making it more difficult using one or more of the difficulty breakdown parameters. for example, using different functions/ numbers so the algebra is more tricky, using a word problem where the first step is not clear to require more problem solving, having the question give less information or 'hints', such as say 'solve' instead of 'solve using the quadratic formula. a question can use notation or mathematical terminology instead of saying something in a way students might be more familiar with.


format: string
### options
currently four options, including the correct option. the other options should, if possible, be common mistakes a student could make on the question. Examples of mistakes include sign/ calculation errors, mixing the question up with a similar concept, an option that looks similar but is not the same. The correct answer should be roughly evenly distributed across the indexes


Formatted as an array(list) with each option.
### correct index
the index from 0-3 of the right answer
### option explanations
four explanations which are personalized to the option. For the correct one, it should emphasis the underlying theory. For the incorrect options which are possible mistakes, it should explain where it is possible the student went wrong and explained the correct answer. If the answer is not based on a common mistake, the explanation should explain why this answer is wrong and explain the correct answer.


Formatted as an array(list), with each of the four explanations for the options as they appear in options.
### main topic index
this contains the index of the main topic of the question, as corresponds to the topic in the knowledge graph. the topic name isn't actually saved with the mcq, just the index.


### subtopic weights
this contains the index of any other topics which are involved in the question. It should exclude the direct prerequisites to the main topic.  (current examples don't actually do this). It also contains the main topic index. each index has a corresponding weight (0-1) according to how much it is involved in the question. the main topic should always have the highest weight. the weights should all add up to one , so that they are comparable across questions.


Formatted as a dictionary the index : weight


### difficulty breakdown
( a better name would probably be skills breakdown)
each question has a difficulty breakdown which measures how difficult the question is with regards each skill from 0-1
1. conceptual understanding: question focuses on the why behind something rather than rote learning, requires an in depth understanding
2. procedural fluency: includes arithmetic and algebraic fluency, how tricky the computations in the questions are.
3. problem solving: eg for word problems, choosing which strategy to use from multiple, multistep questions, unfamiliar problems
4. mathematical communication skills: use of symbols, notation and mathematical language rather than names or clear language a student might be more familiar with
5. memory: recalling facts, definitions, formulas and procedures, especially ones that aren't in the formula and tables book
6. spatial reasoning: understanding, visualising and manipulating objects


in the code they are called conceptual, procedural, problem_solving, communication, memory, spatial


## calculated content
### id
each mcq has an id, which is what's used to refer to it in most of the code. It is a random string of letters and numbers: mcq_id = str(uuid.uuid4()). it is generated when the mcqs are created.


### chapter
this just stores the chapter that corresponds to the topic in the knowledge graph. it saves calculating it when it's needed. its added when the mcq is created.


### prerequisites
the prerequisites for each mcq are stored, to save calculating them every time for the algorithm. It includes the prereqs for the main topics and the subtopics, weighted by edge weight and weight in question.


### difficulty
the overall difficulty score for a question is the average of the skills in the difficulty breakdown. it is calculated automatically based on the difficulty breakdown values. There could be a better way of calculating this.



# things we'll probably add at a later point
- hints
- breaking the question down into multiple steps
- a way to vary the actual numbers of the questions
- students typing answers instead of multiple choice
- interactive stuff like graph and images
