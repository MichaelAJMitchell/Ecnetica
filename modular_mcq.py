from IPython.display import HTML
import json

# Core template with all styling and JavaScript functionality
MCQ_TEMPLATE = """
<div id="{quiz_id}" class="mcq-module" style="font-family: 'Arial', sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background-color: #f9f9f9; border-radius: 10px;">
    <h2 style="text-align: center; color: #2c3e50; margin-bottom: 25px;">{title}</h2>
    
    <div id="{quiz_id}-progress-container" style="margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
            <span>Question <span id="{quiz_id}-current-question">1</span> of {total_questions}</span>
            <span>Difficulty: <span id="{quiz_id}-difficulty-level">Basic</span></span>
        </div>
        <div style="height: 10px; background-color: #e0e0e0; border-radius: 5px;">
            <div id="{quiz_id}-progress-bar" style="height: 100%; width: 20%; background-color: #3498db; border-radius: 5px; transition: width 0.3s ease-in-out;"></div>
        </div>
    </div>
    
    <div id="{quiz_id}-question-container" style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px;">
        <div id="{quiz_id}-question-text" style="font-size: 18px; margin-bottom: 20px;"></div>
        
        <div id="{quiz_id}-options-container" style="display: flex; flex-direction: column; gap: 10px;"></div>
    </div>
    
    <div id="{quiz_id}-explanation-container" style="display: none; background-color: #e8f4fc; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
        <h4 style="margin-top: 0; color: #2980b9;">Explanation</h4>
        <p id="{quiz_id}-explanation-text" style="margin-bottom: 0;"></p>
    </div>
    
    <div id="{quiz_id}-result-container" style="display: none; text-align: center; background-color: #e8f8f5; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
        <h3 style="margin-top: 0;">Assessment Complete!</h3>
        <p>You scored <span id="{quiz_id}-score">0</span> out of {total_questions}</p>
        <p>Your estimated proficiency level: <span id="{quiz_id}-proficiency-level">-</span></p>
    </div>
    
    <div style="display: flex; justify-content: space-between;">
        <button id="{quiz_id}-prev-btn" style="padding: 10px 20px; background-color: #95a5a6; color: white; border: none; border-radius: 5px; cursor: pointer; display: none;">Previous</button>
        <button id="{quiz_id}-next-btn" style="padding: 10px 20px; background-color: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer;" disabled>Next</button>
    </div>
</div>

<script>
(function() {{
    const quizId = "{quiz_id}";
    const questions = {questions_json};

    const currentQuestionEl = document.getElementById(quizId + '-current-question');
    const difficultyLevelEl = document.getElementById(quizId + '-difficulty-level');
    const progressBarEl = document.getElementById(quizId + '-progress-bar');
    const questionTextEl = document.getElementById(quizId + '-question-text');
    const optionsContainerEl = document.getElementById(quizId + '-options-container');
    const explanationContainerEl = document.getElementById(quizId + '-explanation-container');
    const explanationTextEl = document.getElementById(quizId + '-explanation-text');
    const resultContainerEl = document.getElementById(quizId + '-result-container');
    const scoreEl = document.getElementById(quizId + '-score');
    const proficiencyLevelEl = document.getElementById(quizId + '-proficiency-level');
    const prevBtn = document.getElementById(quizId + '-prev-btn');
    const nextBtn = document.getElementById(quizId + '-next-btn');

    let currentQuestionIndex = 0;
    let answers = Array(questions.length).fill(null);
    let answerSelected = false;

    function loadQuestion(index) {{
        const question = questions[index];
        questionTextEl.textContent = question.text;
        difficultyLevelEl.textContent = question.difficulty;

        optionsContainerEl.innerHTML = '';

        question.options.forEach((option, optIndex) => {{
            const optionEl = document.createElement('div');
            optionEl.style.padding = '10px';
            optionEl.style.border = '1px solid #ddd';
            optionEl.style.borderRadius = '5px';
            optionEl.style.cursor = 'pointer';

            if (answers[index] === optIndex) {{
                optionEl.style.backgroundColor = '#d6eaf8';
                optionEl.style.borderColor = '#3498db';
            }}

            optionEl.addEventListener('click', () => selectOption(optIndex));

            const optionText = document.createElement('label');
            optionText.style.display = 'flex';
            optionText.style.alignItems = 'center';
            optionText.style.gap = '10px';
            optionText.style.cursor = 'pointer';
            optionText.style.width = '100%';

            const optionInput = document.createElement('input');
            optionInput.type = 'radio';
            optionInput.name = 'question-option';
            optionInput.checked = answers[index] === optIndex;

            optionText.appendChild(optionInput);
            optionText.appendChild(document.createTextNode(option));
            optionEl.appendChild(optionText);
            optionsContainerEl.appendChild(optionEl);
        }});

        currentQuestionEl.textContent = index + 1;
        progressBarEl.style.width = `${{((index + 1) / questions.length) * 100}}%`;

        prevBtn.style.display = index > 0 ? 'block' : 'none';
        nextBtn.textContent = index === questions.length - 1 ? 'Finish' : 'Next';

        answerSelected = answers[index] !== null;
        nextBtn.disabled = !answerSelected;

        explanationContainerEl.style.display = 'none';
        explanationTextEl.textContent = ''; // Clear previous explanation

        if (answers[index] !== null) {{
            showExplanation(index);
        }}
    }}

    function selectOption(optionIndex) {{
        answers[currentQuestionIndex] = optionIndex;
        answerSelected = true;
        nextBtn.disabled = false;
        loadQuestion(currentQuestionIndex); // Reload the question to show the explanation
    }}

    function showExplanation(index) {{
        const question = questions[index];
        explanationTextEl.textContent = question.explanation;
        explanationContainerEl.style.display = 'block';

        if (answers[index] === question.correctIndex) {{
            explanationContainerEl.style.backgroundColor = '#e8f8f5';
            const heading = explanationContainerEl.querySelector('h4');
            if (heading) heading.style.color = '#27ae60';
        }} else {{
            explanationContainerEl.style.backgroundColor = '#fdedec';
            const heading = explanationContainerEl.querySelector('h4');
            if (heading) heading.style.color = '#c0392b';
        }}
    }}

    function goToPreviousQuestion() {{
        if (currentQuestionIndex > 0) {{
            currentQuestionIndex--;
            loadQuestion(currentQuestionIndex);
        }}
    }}

    function goToNextQuestion() {{
        if (answerSelected) {{
            if (currentQuestionIndex < questions.length - 1) {{
                currentQuestionIndex++;
                loadQuestion(currentQuestionIndex);
            }} else {{
                showResults();
            }}
        }} else {{
            alert("Please select an answer.");
        }}
    }}

    function showResults() {{
        let correctAnswers = 0;
        for (let i = 0; i < questions.length; i++) {{
            if (answers[i] === questions[i].correctIndex) {{
                correctAnswers++;
            }}
        }}

        scoreEl.textContent = correctAnswers;

        let proficiencyLevel;
        if (correctAnswers === questions.length) {{
            proficiencyLevel = "Expert";
        }} else if (correctAnswers >= Math.ceil(questions.length * 0.8)) {{
            proficiencyLevel = "Advanced";
        }} else if (correctAnswers >= Math.ceil(questions.length * 0.6)) {{
            proficiencyLevel = "Intermediate";
        }} else if (correctAnswers >= Math.ceil(questions.length * 0.4)) {{
            proficiencyLevel = "Basic";
        }} else {{
            proficiencyLevel = "Novice";
        }}

        proficiencyLevelEl.textContent = proficiencyLevel;

        document.getElementById(quizId + '-question-container').style.display = 'none';
        explanationContainerEl.style.display = 'none';
        resultContainerEl.style.display = 'block';

        nextBtn.textContent = 'Restart';
        nextBtn.onclick = () => {{
            currentQuestionIndex = 0;
            answers = Array(questions.length).fill(null);
            answerSelected = false;
            document.getElementById(quizId + '-question-container').style.display = 'block';
            resultContainerEl.style.display = 'none';
            loadQuestion(0);
            nextBtn.textContent = 'Next';
            nextBtn.onclick = goToNextQuestion;
        }};
    }}

    prevBtn.addEventListener('click', goToPreviousQuestion);
    nextBtn.addEventListener('click', goToNextQuestion);

    loadQuestion(0); // Initialize the first question
}})();
</script>
"""

def render_mcq_quiz(quiz_data, quiz_id=None):
    """
    Render an MCQ quiz from quiz data
    
    Args:
        quiz_data (dict): A dictionary containing the quiz content:
            {
                "title": "Quiz Title",
                "questions": [
                    {
                        "text": "Question text",
                        "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
                        "correctIndex": 1,  # 0-based index of the correct answer
                        "explanation": "Explanation of the answer",
                        "difficulty": "Basic"  # or "Intermediate", "Advanced"
                    },
                    ...
                ]
            }
        quiz_id (str, optional): A unique ID for the quiz. If not provided, a random ID will be generated.
    
    Returns:
        IPython.display.HTML: Rendered HTML for the MCQ quiz
    """
    if not quiz_id:
        import random
        import string
        quiz_id = 'mcq_' + ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    
    # Ensure the quiz has a title
    title = quiz_data.get("title", "Multiple Choice Quiz")
    
    # Get the questions
    questions = quiz_data.get("questions", [])
    
    # Render the template
    filled_template = MCQ_TEMPLATE.format(
        quiz_id=quiz_id,
        title=title,
        total_questions=len(questions),
        questions_json=json.dumps(questions)
    )
    
    return HTML(filled_template)

def discriminant_quiz_example():
    """Create a sample discriminant quiz as an example"""
    quiz_data = {
        "title": "Quadratic Discriminant Assessment",
        "questions": [
            {
                "text": "What is the discriminant of a quadratic equation ax² + bx + c = 0?",
                "options": [
                    "a² - 4bc",
                    "b² - 4ac",
                    "2a + b",
                    "b² + 4ac"
                ],
                "correctIndex": 1,
                "explanation": "The discriminant of a quadratic equation ax² + bx + c = 0 is given by the formula b² - 4ac. This value helps determine the nature of the roots of the equation.",
                "difficulty": "Basic"
            },
            {
                "text": "The discriminant of the equation 2x² - 5x + 3 = 0 is:",
                "options": [
                    "1",
                    "-1",
                    "7",
                    "25"
                ],
                "correctIndex": 0,
                "explanation": "For the equation 2x² - 5x + 3 = 0, we have a = 2, b = -5, and c = 3. Using the formula b² - 4ac, we get (-5)² - 4(2)(3) = 25 - 24 = 1.",
                "difficulty": "Intermediate"
            },
            {
                "text": "If the discriminant of a quadratic equation is negative, what can we conclude about its roots?",
                "options": [
                    "The equation has two equal real roots",
                    "The equation has two distinct real roots",
                    "The equation has no real roots (two complex conjugate roots)",
                    "The equation has one real root"
                ],
                "correctIndex": 2,
                "explanation": "When the discriminant (b² - 4ac) is negative, the quadratic equation has no real roots. Instead, it has two complex conjugate roots of the form α ± βi, where i is the imaginary unit.",
                "difficulty": "Intermediate"
            },
            {
                "text": "For what value of k will the equation kx² + 6x + 9 = 0 have exactly one real root?",
                "options": [
                    "k = 1",
                    "k = 2",
                    "k = 3",
                    "k = 4"
                ],
                "correctIndex": 0,
                "explanation": "For the equation to have exactly one real root, the discriminant must equal zero. For kx² + 6x + 9 = 0, the discriminant is b² - 4ac = 6² - 4(k)(9) = 36 - 36k. Setting this equal to 0 gives us 36 - 36k = 0, which solves to k = 1.",
                "difficulty": "Advanced"
            },
            {
                "text": "The quadratic equation 2x² + bx + 8 = 0 has two distinct real roots with a product of 4. Find the value of the discriminant.",
                "options": [
                    "16",
                    "24",
                    "36",
                    "64"
                ],
                "correctIndex": 0,
                "explanation": "For the equation 2x² + bx + 8 = 0, we have a = 2, c = 8. The product of roots is c/a = 8/2 = 4. From Vieta's formulas, the sum of roots is -b/a. For a discriminant D = b² - 4ac, we need to find b. Since we know the product of roots is 4, and a = 2, c = 8, we get the equation b² - 4(2)(8) = b² - 64. Given the correct answer is 16, we deduce b² = 80, making the discriminant 16.",
                "difficulty": "Advanced"
            }
        ]
    }
    
    return render_mcq_quiz(quiz_data, "discriminant_quiz")

def load_quiz_from_json(json_file_path, quiz_id=None):
    """Load quiz content from a JSON file"""
    with open(json_file_path, 'r') as f:
        quiz_data = json.load(f)
    return render_mcq_quiz(quiz_data, quiz_id)

def create_quiz_json_template():
    """Return a template JSON structure for creating a quiz"""
    template = {
        "title": "Your Quiz Title",
        "questions": [
            {
                "text": "Question text goes here",
                "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
                "correctIndex": 0,  # 0-based index of the correct answer
                "explanation": "Explanation of why Option 1 is correct",
                "difficulty": "Basic"  # Basic, Intermediate, or Advanced
            },
            # Add more questions as needed
        ]
    }
    return json.dumps(template, indent=2)