# Workflow
if you take the mcq document and run them through the process_mcqs python file, it automatically calculates the id, prerequisites and difficulty and them saves them in another json file, which is the one actually used for the mcq algorithm. it also calculates the chapter from the topic for the main node.

Ensure the correct files are imported into the knowledge graph.

# MCQs Structure
The bottom of this document has full examples for both the precomputed form for generation and the computed form for the algorithm.

Questions can have breakdowns which break the question into steps when a student gets it wrong. There can be different breakdowns for each answer. They can also have randomly generated parameters which change every time a student does the question.
## parameters
The code can generate parameters for questions, so that the numbers are different every time a student sees the question. There is two types of parameters, generated and calculated. The generated ones are the ones which are randomly generated. But it isn't always easiest to generate the actual parameters in the question. Sometimes to get the answers to be nice numbers/ question factorisable/solvable etc, its easiest to generate numbers to base the parameters in the question of off. A lot of the time this might mean randomly generating the answers and then working back to calculate what the corresponding question should be. The calculated_parameters field if for any parameters based on the generated, or other calculated ones. This used sympy to do the substitutions.
## mcqs explicit content
### text
the question stores the information the student will see when they are asked a question. Questions should range in content from simple definitions and applications designed to test if the students have a basic understanding of the core concept, to questions testing more tricky or complex aspects of the topic, including incorporating other topics.
    variations of the questions can be made by taking a basic questions and making it more difficult using one or more of the difficulty breakdown parameters. for example, using different functions/ numbers so the algebra is more tricky, using a word problem where the first step is not clear to require more problem solving, having the question give less information or 'hints', such as say 'solve' instead of 'solve using the quadratic formula. a question can use notation or mathematical terminology instead of saying something in a way students might be more familiar with.

Any math in the question should be wrapped in ```\\( \\)``` for latex, using latex notation.

Where the question should be in the question text is replaced with``` ${question_expression}, ${question_expression_factored}, ${question_expression_simplified}, ${question_expression_collected}```, depending on the question. It must be one of these options, or else be a parameter defined in generated or calculated parameters as``` ${parameter}. (one $ for substituting parameters)```. If the question is part of a breakdown, it can call on parameters from the parent mcq. Question expression always refers to the parent mcq, subquestion_expression and its variations is used for expressions defined in the subquestion.

format: string

### question/subquestion_expression
The actual expression is under question_expression. This can be multiplied out to facilitate working backward, if that is what is needed to make variables which are easy to generate. The question expression should use python notation. Don't call question expressions or parameters things that are already on Python's namespace, such as poly, func, angle.

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

If the parameter generation fails, it falls back to the min value.
### calculated_parameters
For anything that needs to be calculated, eg for question_expression, options, options explanations.

These are formatted as "parameter_name":"rule to calculate it by". The calculations should use the python math conventions.
Don't have anything using random in calculated parameters, it won't work. there should be on logic such as ```"'ax^2 + bx + c = 0' if form_type == 'standard' else ('y = a(x-h)^2 + k' if form_type == 'vertex' else ('y = a(x-p)(x-q)' if form_type == 'factored' else 'y = mx + b'))"```.  Don't use len(). Things should not use $$ or latex syntax.


There is options that can be used in the question text and options that give more information. They can be used in calculated parameters or question expression without the ${ }.
```
For fractions:
${param_name}_num$ → Numerator value
${param_name}_den$ → Denominator value
${param_name}_float$ → Decimal equivalent
For angles:
${param_name}_degrees$ → Angle in degrees
${param_name}_radians$ → Angle in radians
${param_name}_unit$ → Unit string ("degrees" or "radians")
For polynomials:
${param_name}_coeffs$[0] → Leading coefficient (highest degree)
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
```

### options
currently four options, including the correct option. the other options should, if possible, be common mistakes a student could make on the question. Examples of mistakes include sign/ calculation errors, mixing the question up with a similar concept, an option that looks similar but is not the same. The correct answer should be roughly evenly distributed across the indexes, it should not always be the first option.
This can substitute parameters and render them for display. Any calculations than need to be done should be in calculated parameters, with that parameter called in the options to be substituted. Ensure the parameter name is in the options, not the contents of the parameters. options should use latex formatting, with an extra backslash as the mcqs are stored in json. ```\\(option\\)``` should be the format. . Use ```\\text{}``` for any text in the options.

Formatted as an array(list) with each option.
### correct index
the index from 0-3 which corresponds to the right answer in the options.
### option explanations
Contains four explanations which are personalized to the option. For the correct one, it should emphasis the underlying theory, explaining why the question was right incase the student just guessed. For the incorrect options which are possible mistakes, it should explain where it is possible the student went wrong and explained the correct answer. If the answer is not based on a common mistake, the explanation should explain why this answer is wrong and explain the correct answer.
Any math should be wrapped in ```\\(\\)```, with ```${param}``` used for substituting any parameters defined in the question.


Formatted as an array(list), with each of the four explanations for the options in the order they appear in options.
### main topic index
this contains the index of the main topic of the question, as corresponds to the topic in the knowledge graph. the topic name isn't actually saved with the mcq, just the index.


### subtopic weights
this contains the index of any other topics which are involved in the question, including the main topic. It should exclude the direct prerequisites to the main topic. Each index has a corresponding weight (0-1) according to how much it is involved in the question. The main topic should always have the highest weight. The weights should all add up to one, so that they are comparable across questions.


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

#### breakdown
This property should be present if the question has steps which the question can be broken down into when a student gets the question wrong. For simple questions such as definitions or questions which only contain one step, the question does not need to contain a breakdown and this property should not be present.

For questions which can be broken down into steps, eg questions with multiple steps of calculations, which involving multiple skills such as recalling information and then applying it, or exam-style question, breakdown should be formatted as follows:
The breakdown should aim to teach the content, as it will appear when students get a question wrong. The question should be broken into approximately 2-5 steps, maybe more if it is a very complex exam-style question. The questions should first address memory of key definitions, formulas, notation, methods etc used in the question. An understanding of the topic could also be tested here too. The next questions should then target procedural fluency, eg subbing in numbers, doing algebra/ calculations, following the logic which the student should use. The questions should then move to more complex problem solving, critical thinking, and interpretation of answer, if these are applicable.

The questions should all lead into one another in a coherent way, with the answer to the previous one being the starting point to the next question where suitable. The questions should lead up to the answer the student should have got in the original question, with this answer being the answer to the final question of the breakdown.

structure of breakdown:
#### Answer Type
The breakdown contains a number of different 'breakdown chains'. These correspond to each of the incorrect options. If the incorrect option corresponds to a specific possible mistake, the breakdown should be tailored to address this. Eg if a student chooses an option that uses a different formula than correct, the breakdown should focus a lot on recalling the correct formula. However, if the mistake was just a sign, more focus should be placed on the actual calculation rather than on recalling the formula. Each step is contained within a dictionary with the name corresponding to the type of mistake the question addresses.

#### answer mapping
This is a list of indexes which indicates which answer options should trigger this breakdown. There can be a single breakdown chain for a question, or a number of different ones. This list can contain one, two or three of the indexes, as long as it is not the correct index.

#### steps
This is a list of dictionaries containing each of the steps for the breakdown chain. Each one contains the following:
#### step_no
the position of this step in the chain from 1 to the last number.

#### prereq_topics
This contains the index of nodes which are perquisites from the parent question which are directly involved in this step of the breakdown. If this property is present, then the student's mastery of the nodes in this is checked, and if they are high, this step is skipped. The questions should be  formatted in a way such that the question still make sense and still work together even with this question missing. This will mostly be used in the first question in a breakdown chain, as this is the easiest to skip. Note if the breakdown question directly contains prerequisite topics, but is a key step that the question can be done without, then this property should not be present. It should only be there for parts that are skippable.

#### step_type
This should be one of the skills breakdown fields: "conceptual_understanding","procedural_fluency", "problem_solving", "mathematical_communication", "memory",    "spatial_reasoning" . It should be the one that that step targets most. This will be used in updating these skills, as a students anser on these can pinpoint exactly why they got the question wrong, eg because they forgot the formula or had trouble with the algebra.
#### text
this should contain the text for the breakdown, following the same structure as the text for the main question outlined above. All the parameters from the parent question as well as any in that breakdown are available to the breakdown questions.
#### options
the options should follow the same structure as for the options for the parent question, as above
#### correctindex

#### option_explanations
As in the parent question, this contains an explanation corresponding to each option. Where correct, they should reinforce understanding. For incorrect options, they should working though all the steps a student should have done, allowing them to see exactly why they are wrong.


These fields are then repeated for every step in the breakdown.

## calculated content
This content will be calculated after and does not need to be generated.
### id
each mcq has an id, which is what's used to refer to it in most of the code. It is a random string of letters and numbers: mcq_id = str(uuid.uuid4()). it is generated when the mcqs are created.


### chapter
this just stores the chapter that corresponds to the topic in the knowledge graph. it saves calculating it when it's needed. its added when the mcq is created.


### prerequisites
the prerequisites for each mcq are stored, to save calculating them every time for the algorithm. It includes the prereqs for the main topics and the subtopics, weighted by edge weight and weight in question.


### difficulty
the overall difficulty score for a question is the average of the skills in the difficulty breakdown. it is calculated automatically based on the difficulty breakdown values. There could be a better way of calculating this.

# structure that questions should be generated in
Don't need to contain breakdown or parameter generation fields
```
    {
      "text": "What is the discriminant of the quadratic equation ${question_expression}?",
      "question_expression": "a*x**2 +b*x + c = 0",
      "generated_parameters": {
        "a": {
          "type": "int",
          "min": -9,
          "max": 9,
          "exclude": 0
        },
        "b": {
          "type": "int",
          "min": -9,
          "max": 9
        },
        "c": {
          "type": "int",
          "min": -50,
          "max": 50
        }
      },
        "calculated_parameters": {
          "opt1": "b**2-4*a*c",
          "opt2": "b**2+4*a*c",
          "opt3": "sqrt(b**2-4*a*c)",
          "opt4": "(-b+sqrt(b**2-4*a*c))/(2*a)"
        },
        "options": [
          "${opt1}",
          "${opt2}",
          "${opt3}",
          "${opt4}"
        ],
      "correctindex": 0,
      "option_explanations": [
        "Correct!The discriminant is $b^2 - 4ac$",
        "Incorrect. You may have calculated $b^2 + 4ac$ instead of $b^2 - 4ac$.",
        "Incorrect. Remember the formula is $b^2 - 4ac$, not $sqrt{b^2-4ac}$.",
        "Incorrect. The discriminant is just the part under square root of the quadratic question."
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
      },
      "breakdown": {
        "sign_error": {
          "answer_mapping": [
            1
          ],
      "steps": [
        {
          "step_no": 1,
          "prereq_topics": [14],
          "step_type": "memory",
          "text": "what is the formula for solving quadratic equations?",
          "options": [
            "\\(x=\\frac{-b+\\sqrt{b^2-4ac}}{2a}\\)",
            "\\(\\sqrt{b^2-4ac}\\)",
            "\\(\\frac{-b\\pm \\sqrt{b^2-4ac}}{2a}\\)",
            "\\(ax^2+bx+c\\)"
          ],
          "correctindex": 2,
          "option_explanations": [
            "not quite, there is a plus",
            "this is more like the formula for the discriminant, the question is asking for the whole formula",
            "yes! this is the formula you use when you are solving quadratic equations",
            "this is actually the form of an actual quadratic equation. we want the formula you can use to solve for x."
          ]
        },
        {
          "step_no": 2,
          "step_type": "memory",
          "text": "the discriminant is part of the quadratic formula, which bit?",
          "options": [
            "\\(\\sqrt{b^2 - 4ac}\\)",
            "\\(b^2 - 4ac\\)",
            "\\(2a\\)",
            "\\(-b \\pm \\sqrt{b^2-4ac}\\)"
          ],
          "correctindex": 1,
          "option_explanations": [
            "the discriminant is the bit under the square root, but it doesn't actually include the square root itself",
            "yep its the bit under the square root",
            "remember we only want the bit under the square root, not the whole top of the fraction",
            "no"
          ]
        },
        {
          "step_no": 3,
          "step_type": "procedural_fluency",
          "text": "now we have the formula \\(b^2-4ac\\), we want to substitute our numbers into it. remember our quadratic is ${question_expression}. our formula has a, b and c. what should each of these numbers be?",
          "options": [
            "\\(a = \\text{the number by itself}, b = \\text{the number in front of the } x, c = \\text{the number in front of the } x^2\\)",
            "\\(a = ${a}, b = ${b}, c = ${c}\\)",
            "\\(a=1,b=2,c=3\\)",
            "\\(a= \\text{the number in front of the } x^2, b = \\text{the number in front of the } x, c = \\text{the term by itself}\\)"
          ],
          "correctindex": 3,
          "option_explanations": [
            "almost you just have it the wrong way around",
            "you actually just want the numbers in front of xs, don't actually include the x",
            "no",
            "yes yay"
          ]
        },
        {
          "step_no": 4,
          "step_type": "procedural_fluency",
          "text": "we now have our formula, \\(${b}^2-4(${a})(${c})\\). time to do the math. when you calculate this sum, what do you get?",
          "calculated_parameters": {
            "opt1": "b**2-4*a*c",
            "opt2": "b**2+4*a*c",
            "opt3": "sqrt(b**2-4*a*c)",
            "opt4": "(-b+sqrt(b**2-4*a*c))/(2*a)"
          },
          "options": [
            "${opt1}",
            "${opt2}",
            "${opt3}",
            "${opt4}"
          ],
          "correctindex": 0,
          "option_explanations": [
            "yes",
            "no",
            "no",
            "no"
          ]
        }
      ]
    },
    "formula_confusion": {
      "answer_mapping": [2, 3],
      "steps": [
        {
          "step_no": 1,
          "step_type": "memory",
          "text": "the discriminant is part of the quadratic formula, which bit?",
          "options": [
            "\\(\\sqrt{b^2 - 4ac}\\)",
            "\\(b^2 - 4ac\\)",
            "\\(2a\\)",
            "\\(-b \\pm \\sqrt{b^2-4ac}\\)"
          ],
          "correctindex": 1,
          "option_explanations": [
            "the discriminant is the bit under the square root, but it doesn't actually include the square root itself",
            "yep its the bit under the square root",
            "remember we only want the bit under the square root, not the whole top of the fraction",
            "no"
          ]
        },
        {
          "step_no": 2,
          "step_type": "procedural_fluency",
          "text": "now we have the formula \\(b^2-4ac\\), we want to substitute our numbers into it. remember our quadratic is ${question_expression}. our formula has a, b and c. what should each of these numbers be?",
          "options": [
            "\\(a = \\text{the number by itself}, b = \\text{the number in front of the } x, c = \\text{the number in front of the } x^2\\)",
            "\\(a = ${a}, b = ${b}, c = ${c}\\)",
            "\\(a=1,b=2,c=3\\)",
            "\\(a= \\text{the number in front of the } x^2, b = \\text{the number in front of the } x, c = \\text{the term by itself}\\)"
          ],
          "correctindex": 3,
          "option_explanations": [
            "almost you just have it the wrong way around",
            "you actually just want the numbers in front of xs, don't actually include the x",
            "no",
            "yes yay"
          ]
        },
        {
          "step_no": 3,
          "step_type": "procedural_fluency",
          "text": "we now have our formula, ${subquestion_expression}. time to do the math. when you calculate this sum, what do you get?",
          "subquestion_expression": "b**2-4*a*c",
          "calculated_parameters": {
            "opt1": "b**2-4*a*c",
            "opt2": "b**2+4*a*c",
            "opt3": "sqrt(b**2-4*a*c)",
            "opt4": "(-b+sqrt(b**2-4*a*c))/(2*a)"
          },
          "options": [
            "${opt1}",
            "${opt2}",
            "${opt3}",
            "${opt4}"
          ],
          "correctindex": 0,
          "option_explanations": [
            "yes",
            "no",
            "no",
            "no"
          ]
        }
      ]
    }
  }
    }
```
# form they will be in after process_mcqs
    {
      "id": "5fd2fa18-963c-4473-ad47-b7ce48a44a85",
      "text": "What is the discriminant of the quadratic equation ${question_expression}?",
      "question_expression": "a*x**2 +b*x + c = 0",
      "generated_parameters": {
        "a": {
          "type": "int",
          "min": -9,
          "max": 9,
          "exclude": 0
        },
        "b": {
          "type": "int",
          "min": -9,
          "max": 9
        },
        "c": {
          "type": "int",
          "min": -50,
          "max": 50
        }
      },
      "calculated_parameters": {
        "opt1": "b**2-4*a*c",
        "opt2": "b**2+4*a*c",
        "opt3": "sqrt(b**2-4*a*c)",
        "opt4": "(-b+sqrt(b**2-4*a*c))/(2*a)"
      },
      "options": [
        "${opt1}",
        "${opt2}",
        "${opt3}",
        "${opt4}"
      ],
      "correctindex": 0,
      "option_explanations": [
        "Correct!The discriminant is $b^2 - 4ac$",
        "Incorrect. You may have calculated $b^2 + 4ac$ instead of $b^2 - 4ac$.",
        "Incorrect. Remember the formula is $b^2 - 4ac$, not $sqrt{b^2-4ac}$.",
        "Incorrect. The discriminant is just the part under square root of the quadratic question."
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
      },
      "overall_difficulty": 0.2833333333333334,
      "prerequisites": {
        "16": 0.7
      },
      "breakdown": {
        "sign_error": {
          "steps": [
            {
              "step_no": 1,
              "prereq_topics": [
                14
              ],
              "step_type": "memory",
              "text": "what is the formula for solving quadratic equations?",
              "options": [
                "\\(x=\\frac{-b+\\sqrt{b^2-4ac}}{2a}\\)",
                "\\(\\sqrt{b^2-4ac}\\)",
                "\\(\\frac{-b\\pm \\sqrt{b^2-4ac}}{2a}\\)",
                "\\(ax^2+bx+c\\)"
              ],
              "correctindex": 2,
              "option_explanations": [
                "not quite, there is a plus",
                "this is more like the formula for the discriminant, the question is asking for the whole formula",
                "yes! this is the formula you use when you are solving quadratic equations",
                "this is actually the form of an actual quadratic equation. we want the formula you can use to solve for x."
              ]
            },
            {
              "step_no": 2,
              "step_type": "memory",
              "text": "the discriminant is part of the quadratic formula, which bit?",
              "options": [
                "\\(\\sqrt{b^2 - 4ac}\\)",
                "\\(b^2 - 4ac\\)",
                "\\(2a\\)",
                "\\(-b \\pm \\sqrt{b^2-4ac}\\)"
              ],
              "correctindex": 1,
              "option_explanations": [
                "the discriminant is the bit under the square root, but it doesn't actually include the square root itself",
                "yep its the bit under the square root",
                "remember we only want the bit under the square root, not the whole top of the fraction",
                "no"
              ]
            },
            {
              "step_no": 3,
              "step_type": "procedural_fluency",
              "text": "now we have the formula \\(b^2-4ac\\), we want to substitute our numbers into it. remember our quadratic is ${question_expression}. our formula has a, b and c. what should each of these numbers be?",
              "options": [
                "\\(a = \\text{the number by itself}, b = \\text{the number in front of the } x, c = \\text{the number in front of the } x^2\\)",
                "\\(a = ${a}, b = ${b}, c = ${c}\\)",
                "\\(a=1,b=2,c=3\\)",
                "\\(a= \\text{the number in front of the } x^2, b = \\text{the number in front of the } x, c = \\text{the term by itself}\\)"
              ],
              "correctindex": 3,
              "option_explanations": [
                "almost you just have it the wrong way around",
                "you actually just want the numbers in front of xs, don't actually include the x",
                "no",
                "yes yay"
              ]
            },
            {
              "step_no": 4,
              "step_type": "procedural_fluency",
              "text": "we now have our formula, \\(${b}^2-4(${a})(${c})\\). time to do the math. when you calculate this sum, what do you get?",
              "calculated_parameters": {
                "opt1": "b**2-4*a*c",
                "opt2": "b**2+4*a*c",
                "opt3": "sqrt(b**2-4*a*c)",
                "opt4": "(-b+sqrt(b**2-4*a*c))/(2*a)"
              },
              "options": [
                "${opt1}",
                "${opt2}",
                "${opt3}",
                "${opt4}"
              ],
              "correctindex": 0,
              "option_explanations": [
                "yes",
                "no",
                "no",
                "no"
              ]
            }
          ],
          "answer_mapping": [
            1
          ]
        },
        "formula_confusion": {
          "steps": [
            {
              "step_no": 1,
              "step_type": "memory",
              "text": "the discriminant is part of the quadratic formula, which bit?",
              "options": [
                "\\(\\sqrt{b^2 - 4ac}\\)",
                "\\(b^2 - 4ac\\)",
                "\\(2a\\)",
                "\\(-b \\pm \\sqrt{b^2-4ac}\\)"
              ],
              "correctindex": 1,
              "option_explanations": [
                "the discriminant is the bit under the square root, but it doesn't actually include the square root itself",
                "yep its the bit under the square root",
                "remember we only want the bit under the square root, not the whole top of the fraction",
                "no"
              ]
            },
            {
              "step_no": 2,
              "step_type": "procedural_fluency",
              "text": "now we have the formula \\(b^2-4ac\\), we want to substitute our numbers into it. remember our quadratic is ${question_expression}. our formula has a, b and c. what should each of these numbers be?",
              "options": [
                "\\(a = \\text{the number by itself}, b = \\text{the number in front of the } x, c = \\text{the number in front of the } x^2\\)",
                "\\(a = ${a}, b = ${b}, c = ${c}\\)",
                "\\(a=1,b=2,c=3\\)",
                "\\(a= \\text{the number in front of the } x^2, b = \\text{the number in front of the } x, c = \\text{the term by itself}\\)"
              ],
              "correctindex": 3,
              "option_explanations": [
                "almost you just have it the wrong way around",
                "you actually just want the numbers in front of xs, don't actually include the x",
                "no",
                "yes yay"
              ]
            },
            {
              "step_no": 3,
              "step_type": "procedural_fluency",
              "text": "we now have our formula, ${subquestion_expression}. time to do the math. when you calculate this sum, what do you get?",
              "subquestion_expression": "b**2-4*a*c",
              "calculated_parameters": {
                "opt1": "b**2-4*a*c",
                "opt2": "b**2+4*a*c",
                "opt3": "sqrt(b**2-4*a*c)",
                "opt4": "(-b+sqrt(b**2-4*a*c))/(2*a)"
              },
              "options": [
                "${opt1}",
                "${opt2}",
                "${opt3}",
                "${opt4}"
              ],
              "correctindex": 0,
              "option_explanations": [
                "yes",
                "no",
                "no",
                "no"
              ]
            }
          ],
          "answer_mapping": [
            2,
            3
          ]
        }
      }
    }
# things we'll probably add at a later point
- hints
- breaking the question down into multiple steps
- a way to vary the actual numbers of the questions
- students typing answers instead of multiple choice
- interactive stuff like graph and images
