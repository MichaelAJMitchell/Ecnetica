# python
## mcqs structure

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
an example of the current mcq format is 
```    
mcqs.append(kg.create_mcq_with_explicit_weights(
        text='Which of the following is the standard form of a quadratic equation?',
        options=[
            '\\(y = mx + c\\)',
            '\\(ax^2 + bx + c = 0\\)',
            '\\(x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}\\)',
            '\\(y = a(x - h)^2 + k\\)'
        ],
        correctindex=1,
        option_explanations=[
            'This is the slope-intercept form of a linear equation, not a quadratic. Linear equations have degree 1, while quadratics have degree 2.',
            'Correct! This is the standard form of a quadratic equation where a, b, and c are constants and a ≠ 0. This form is used for solving and analyzing quadratic equations.',
            'This is the quadratic formula used to find solutions, not the standard form of the equation itself. The formula is derived from the standard form.',
            'This is the vertex form of a quadratic function, which shows the vertex coordinates but is not the standard form used for general analysis.'
        ],
        main_topic_index=2,
        subtopic_weights={2: 1.0},
        conceptual=0.3, procedural=0.0, problem_solving=0.2, communication=0.4, memory=0.4, spatial=0.0
    ))
```



## mcqs explicit content
### question (text)
the question stores the information the student will see when they are asked a question. Questions should range in content from simple definitions and applications designed to test if the students have a basic understanding of the core conecpt, to questions testing more tricky or complex aspects of the topic, including incorportating other topics. 
    variations of the questions can be made by taking a basic questions and making it more difficult using one or more of the difficulty breakdown parameters. for example, using different functions/ numbers so the algebra is more tricky, using a word problem where the first step is not clear to require more probelm solving, having the question give less information or 'hints', such as say 'solve' instead of 'solve using the quardatic formula. a question can use notation or mathematical terinology instead of saying somethings in a way students might be more familiar with. 

format: string
### options
currently four options, including the correct option. the other options should, if possible, be common mistakes a student could make on the question. Examples of mistakes include sign/ calcualtion errors, mixing the question up with a similar concept, an option that looks similar but is not the same. The correst answer should be roughly evenly distributed across the indexs

Formatted as an array(list) with each option. 
### correct index
the index from 0-3 of the right answer
### option eplantions
four explnations which are personalised to the option. For the corrct one, it should emphasis the underlying theory. For the incorrect options which are possible mistakes, it should explain where it is possible the student went worng and exlpain the correct answer. If the answer is not based on a common mistake, the explanation should explain why this answer is wrong and explain the correct answer. 

Formatted as an array(list), with each of the four explanations for the options as they appear in options. 
### main topic index
this contains the index of the main topic of the question, as corresponds to the topic in the knowledge graph. the topic name isn't actually saved with the mcq, just the index.

### subtopic weights
this contains the index of any other topics which are involved in the question. It should exclude the direct prerequsites to the main topic.  (current examples dont actually do this). It also contains the main topic index. each index has a coreesponding weight (0-1) according too how much it is involved in the question. the main topic hould alays have the heightest weight. the weights should all add up to one , so that they are comparable across questions. 

Formatted as a dictionary the index : weight

### difficulty breakdown
( a better name would probably be skills breakdown)
each question has a difficulty breakdown which measures how difficult the question is with regrads each skill from 0-1
1. conceptual understanding: question focuses on the why behind something rather than rote learning, requires an in depth understanding
2. procedural fluency: includes arithmetic and algebraic fluency, how tricky the computations in the questions is.
3. problem solving: eg for word problems, choosing which strategy to use from multiple, multistep questions, unfamiliar problems
4. mathematical communication skills: use of symbols, notation and mathematical language rather than names or clear language a student might be more familiar with
5. memory: recalling facts, definitions, formulas and procedures, especially ones that arent in the formula and tables book
6. spatial reasoning: understanding, visualising and manipulating objects

in the code they are called conceptual, procedural, problem_solving, communication, memory, spatial

## calculated content
### id
each mcq has an id, which is whats used to refer to it in most of the code. It is a random string of letters and numbers: mcq_id = str(uuid.uuid4()). it is generated when the mcqs are created.  

### chapter
this just stores the chapter that corresponds to the topic in the knowledge graph. it saves calculating it when its needed. its added when the mcq is created.

### prerequsites
the prerequsites for each mcq are stored, to save calcualting them every time for the algorithm. It includes the prereqs for the main topics and the subtopics, wieghted by edge weight and weight in question. 

### difficulty
ythe overall difficulty score for a question is the average of the skills in the difficulty breakdown. it is caluclated automatically based on the difficulty breakdown values. 

# things we'll probably add at a later point
- hints
- breaking the question down into multiple steps
- a way to vary the actual numbers of the questions
- students typing answers instead of multiple choice
- interactive stuff like graph and images