# json
## form they can be generated in`
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
## form they will be converted to
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
## Form for questions with randomised numbers
```
    {
      "text": "Factor the quadratic expression ${question_expression_expanded}$.",
      "question_expression":"(x-r_1)*(x-r_2)",
      "generated_parameters":{
        "a":{"type":"int", "min":-24,"max":24,"exclude":0},
        "b":{"type":"int", "min":-12,"max":12,"exclude":0},
        "c":{"type":"int", "min":-24,"max":24,"exclude":0},
        "d":{"type":"int","min":-12,"max":12,"exclude":0}
      },
      "calculated_parameters":{
        "r_1":"a/b",
        "r_2":"c/d"
      },
      "options": [
        "(b*x -c)*(d*x -a)",
        "(b*x -a)*(d*x -c)",
        "(27x + 1)*(2x - 12)",
        "(d*x + c)*(b*x - a)"
      ],
      "correctindex": 1,
      "option_explanations": [
        "Incorrect. Check your factors",
        "Correct! ",
        "Incorrect. ",
        "Incorrect. check your signs."
      ],
      "main_topic_index": 6,
      "subtopic_weights": {
        "6": 1.0
      },
      "difficulty_breakdown": {
        "conceptual_understanding": 0.4,
        "procedural_fluency": 0.8,
        "problem_solving": 0.6,
        "mathematical_communication": 0.2,
        "memory": 0.3,
        "spatial_reasoning": 0.0
      }
    }
```
Questions can be generated in either form, depending on the question.

## mcqs structure


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
## If the question has randomly generated parameters
This used sympy to do the substitutions.
Where the question should be in the question text is replaced with ${question_expression}, ${question_expression_factored}, ${question_expression_simplified}, ${question_expression_collected}, depending on the question. It must be one of these options, or else be a parameter defined in generated or calculated parameters as ${parameter}. (one $ for substuting parametes)

The actual expression is under question_expression. This can be multiplied out to facilitate working backward, if that is what is needed to make variables which are easy to generate. The question expression should use python notation. Don't call question expressions or parameters things that are already on Python's namespace, such as poly, func, angle.
## parameters
There is two types of parameters, generated and calculated. The generated ones are the ones which are randomly generated. But it isn't always easiest to generate the actual parameters in the question. Sometimes to get the answers to be nice numbers/ question factorisable/solvable etc, its easiest to generate numbers to base the parameters in the question of off. A lot of the time this might mean randomly generating the answers and then working back to calculate what the corresponding question should be. The calculated_parameters field if for any parameters based on the generated, or other calculated ones.
### generated_parameters
For randomized parameters
There is different types of parameters that will follow different rules when they are being randomised.
- int is just a random integer between the min and the max
- choice randomly chooses from a list of choices you give it as "choices":
- fraction generated a numerator and a denominator and then makes them a fraction. It has options numerator_min, numerator_max, denominator_min, denominator_max, exclude_numerator, exclude_denominator, reduce< proper_only, as well an normal exclude.
- decimal gives a decimal to a specified number of decimal places. It has options min, max, decimal_places, step and exclude. It is calculated by value = min_val + step_number * randomly generated step, then rounded.
- angle, which has degrees or radians. It has options type: degrees or radians, special_angles_only: true/ false, and quadrant: 1-4.
- polynomial which has options degree, variable, coefficient_min, coefficient_max, leading_coefficient_exclude, monic:true/ false, integer_coeffs: true/false.
- function which has func_type: linear/ quadratic/ exponential,  domain_min, domain_max, param_ranges. Linear functions also has "parameter_ranges": {
  "slope_min": -5,
  "slope_max": 5,
  "intercept_min": -10,
  "intercept_max": 10,
  "allow_zero_slope": false
}
Quadratic functions also have "parameter_ranges": {
  "a_min": -3,
  "a_max": 3,
  "b_min": -5,
  "b_max": 5,
  "c_min": -10,
  "c_max": 10
}
Exponential functions have "parameter_ranges": {
  "coefficient_min": 1,
  "coefficient_max": 5,
  "bases": [2, 3, 5, 10]
}

There is fields for the min and max of the parameter, and also what values should be excluded, eg 0 or another parameter.

If the parameter generation fails, it falls back to the min value.
### calculated_parameters
For anything that needs to be calculated, eg for question_expression, options, options explanations
These are formatted as "parameter_name":"rule to calculate it by". The calculations should use the python math conventions.
Don't have anything using random in calculated parameters, it won't work. there should be on logic such as "'ax^2 + bx + c = 0' if form_type == 'standard' else ('y = a(x-h)^2 + k' if form_type == 'vertex' else ('y = a(x-p)(x-q)' if form_type == 'factored' else 'y = mx + b'))".  Don't use len(). Things should not use $$ or latex syntax.


There is options that can be used in the question text and options that give more information. They can be used in calculated parameters or question expression without the $$ and {}.
For polynomials: ${param_name}_coeffs$[0] → Leading coefficient (highest degree)
${param_name}_coeffs$[1] → Second coefficient
${param_name}_coeffs$[2] → Third coefficient (etc.)
${param_name}_degree$ → Degree of polynomial (integer)
For linear functions
${param_name}_slope$ → Slope value (m)
${param_name}_y_intercept$ → Y-intercept value (b)
${param_name}_type$ → "linear"
For quadratic functions:
${param_name}_a$ → Coefficient of x²
${param_name}_b$ → Coefficient of x
${param_name}_c$ → Constant term
${param_name}_type$ → "quadratic"
For exponential functions:
${param_name}_coefficient$ → Multiplier (a in a*b^x)
${param_name}_base$ → Base (b in a*b^x)
${param_name}_type$ → "exponential"
For fractions:
${param_name}_num$ → Numerator value
${param_name}_den$ → Denominator value
${param_name}_float$ → Decimal equivalent
For angles:
${param_name}_degrees$ → Angle in degrees
${param_name}_radians$ → Angle in radians
${param_name}_unit$ → Unit string ("degrees" or "radians")

### options
This can subsitute parameters and render them for display. Any caluations than need to be done should be in calulated parameters. options should use latex formating, with an estra backslash as the mcqs are stored in json. They do not need to start and end wth $$, the code adds this. Use ```\\text{}``` for any text in the options.
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
