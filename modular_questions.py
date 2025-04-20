from IPython.display import HTML
import json

# Core template with all styling and JavaScript functionality
MATH_RESOURCE_TEMPLATE = """
<style>
    /* Import Computer Modern font for math expressions */
    @import url('https://cdn.jsdelivr.net/npm/computer-modern@0.1.2/fonts/Sans/cmun-sans.css');
    
    /* Scope all styles to our component while allowing font inheritance */
    .math-question-module {{
        color: #2c3e50;
        margin-bottom: 40px;
    }}
    
    /* Apply Computer Modern font to math expressions */
    .math-question-module .math-expression {{
        font-family: "Computer Modern Sans", sans-serif;
    }}
    
    .math-question-module h2 {{
        text-align: center;
        color: #2c3e50;
        margin-bottom: 30px;
    }}
    
    .math-question-module .question-container {{
        width: 100%;
        box-sizing: border-box;
    }}
    
    .math-question-module .topic-intro {{
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }}
    
    .math-question-module .question-categories {{
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        margin-bottom: 20px;
    }}
    
    .math-question-module .category-box {{
        flex: 1;
        min-width: 180px;
        padding: 15px;
        text-align: center;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        font-weight: bold;
    }}
    
    .category-box:hover {{
        transform: translateY(-3px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    
    .math-question-module .scientific {{
        background-color: #3498db;
        color: white;
    }}
    
    .math-question-module .engineering {{
        background-color: #e67e22;
        color: white;
    }}
    
    .math-question-module .financial {{
        background-color: #2ecc71;
        color: white;
    }}
    
    .math-question-module .creative {{
        background-color: #9b59b6;
        color: white;
    }}
    
    .math-question-module .question-content {{
        display: none;
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-top: 10px;
        animation: questionFadeIn 0.5s ease;
    }}
    
    @keyframes questionFadeIn {{
        from {{ opacity: 0; transform: translateY(-10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .math-question-module .question-title {{
        font-weight: bold;
        margin-bottom: 10px;
        color: #2c3e50;
    }}
    
    .math-question-module .active {{
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transform: translateY(-3px);
    }}
    
    /* Button and answer styles */
    .math-question-module .answer-button {{
        background-color: #f0f0f0;
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 8px 16px;
        margin-top: 15px;
        cursor: pointer;
        font-weight: bold;
        display: inline-block;
        transition: all 0.2s ease;
    }}
    
    .math-question-module .answer-button:hover {{
        background-color: #e0e0e0;
    }}
    
    .math-question-module .answer-content {{
        display: none;
        background-color: #f5f5f5;
        border-left: 4px solid #3498db;
        padding: 15px;
        margin-top: 10px;
        animation: answerFadeIn 0.5s ease;
    }}
    
    @keyframes answerFadeIn {{
        from {{ opacity: 0; transform: translateY(-5px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    /* For different question types, color the answer border differently */
    .math-question-module .scientific-answer {{
        border-left-color: #3498db;
    }}
    
    .math-question-module .engineering-answer {{
        border-left-color: #e67e22;
    }}
    
    .math-question-module .financial-answer {{
        border-left-color: #2ecc71;
    }}
    
    .math-question-module .creative-answer {{
        border-left-color: #9b59b6;
    }}
    
    /* For code blocks */
    .math-question-module pre {{
        background-color: #f1f1f1;
        padding: 10px;
        border-radius: 4px;
        overflow-x: auto;
    }}
    
    /* Responsive adjustments */
    @media (max-width: 768px) {{
        .math-question-module .question-categories {{
            flex-direction: column;
        }}
        
        .math-question-module .category-box {{
            width: 100%;
        }}
    }}
</style>
<div class="math-question-module">
    <div class="question-container">
    <h2>{title}</h2>
    
    <div class="topic-intro">
        {intro_content}
    </div>
    
    <div class="question-categories">
        {category_boxes}
    </div>
    
    {question_content_sections}
</div>
</div>

<script>
    function showQuestion(category) {{
        // Hide all question contents first
        const contents = document.querySelectorAll('.math-question-module .question-content');
        contents.forEach(content => {{
            content.style.display = 'none';
        }});
        
        // Also hide all answers when switching questions
        const answers = document.querySelectorAll('.math-question-module .answer-content');
        answers.forEach(answer => {{
            answer.style.display = 'none';
        }});
        
        // Reset all buttons text
        const buttons = document.querySelectorAll('.math-question-module .answer-button');
        buttons.forEach(button => {{
            button.innerText = 'Show Answer';
        }});
        
        // Remove active class from all category boxes
        const boxes = document.querySelectorAll('.math-question-module .category-box');
        boxes.forEach(box => {{
            box.classList.remove('active');
        }});
        
        // Show the selected question content
        const selectedContent = document.getElementById(category + '-content');
        if (selectedContent.style.display === 'block') {{
            selectedContent.style.display = 'none';
        }} else {{
            selectedContent.style.display = 'block';
            // Add active class to the clicked box
            document.querySelector('.math-question-module .' + category).classList.add('active');
        }}
    }}
    
    function toggleAnswer(category) {{
        const answerContent = document.getElementById(category + '-answer');
        const button = answerContent.previousElementSibling;
        
        if (answerContent.style.display === 'block') {{
            answerContent.style.display = 'none';
            button.innerText = 'Show Answer';
        }} else {{
            answerContent.style.display = 'block';
            button.innerText = 'Hide Answer';
        }}
    }}
</script>
"""

# Default categories that can be overridden if needed
DEFAULT_CATEGORIES = [
    {"id": "scientific", "name": "Scientific/Mathematic", "color_class": "scientific"},
    {"id": "engineering", "name": "Engineering/Mechanical", "color_class": "engineering"},
    {"id": "financial", "name": "Financial/Economic", "color_class": "financial"},
    {"id": "creative", "name": "Creative", "color_class": "creative"}
]

def render_math_resource(content_data):
    """
    Render a math resource module from content data.
    
    Args:
        content_data (dict): A dictionary containing the content for the math resource
            {
                "title": "Module Title",
                "intro_content": "HTML content for introduction",
                "categories": [
                    {
                        "id": "category_id",
                        "name": "Category Display Name",
                        "color_class": "css_class"
                    }
                ],
                "questions": [
                    {
                        "category": "category_id",
                        "title": "Question Title",
                        "content": "HTML content for question",
                        "answer": "HTML content for answer"
                    }
                ]
            }
    
    Returns:
        IPython.display.HTML: Rendered HTML for the math resource
    """
    # Use provided categories or fall back to defaults
    categories = content_data.get("categories", DEFAULT_CATEGORIES)
    
    # Generate category boxes
    category_boxes_html = ""
    for category in categories:
        category_boxes_html += f"""
        <div class="category-box {category['color_class']}" onclick="showQuestion('{category['id']}')">
            {category['name']}
        </div>
        """
    
    # Generate question content sections
    question_sections_html = ""
    for question in content_data.get("questions", []):
        category_id = question["category"]
        question_sections_html += f"""
        <div id="{category_id}-content" class="question-content">
            <div class="question-title">{question["title"]}</div>
            {question["content"]}
            
            <div class="answer-button" onclick="toggleAnswer('{category_id}')">Show Answer</div>
            <div id="{category_id}-answer" class="answer-content {category_id}-answer">
                {question["answer"]}
            </div>
        </div>
        """
    
    # Fill the template
    filled_template = MATH_RESOURCE_TEMPLATE.format(
        title=content_data.get("title", "Math Resource"),
        intro_content=content_data.get("intro_content", ""),
        category_boxes=category_boxes_html,
        question_content_sections=question_sections_html
    )
    
    return HTML(filled_template)

# Sample usage with a discriminant example
def discriminant_example():
    """Generate a sample discriminant module as an example"""
    content_data = {
        "title": "Quadratic Equations: The Discriminant",
        "intro_content": """
            <p>The discriminant is a key part of the quadratic formula that helps us understand the nature of the solutions to a quadratic equation. For a quadratic equation in the form <span class="math-expression">ax² + bx + c = 0</span>, the discriminant is given by:</p>
            <p style="text-align: center;" class="math-expression"><strong>Discriminant = b² - 4ac</strong></p>
            <p>The value of the discriminant tells us:</p>
            <ul>
                <li>If discriminant > 0: The equation has two different real roots</li>
                <li>If discriminant = 0: The equation has one real root (a repeated root)</li>
                <li>If discriminant < 0: The equation has two complex roots (no real roots)</li>
            </ul>
        """,
        "questions": [
            {
                "category": "scientific",
                "title": "Scientific Application:",
                "content": """
                    <p>In a physics experiment, the height h (in meters) of a projectile at time t (in seconds) is modeled by the equation:</p>
                    <p style="text-align: center;" class="math-expression">h = -4.9t² + 30t + 2</p>
                    <p>Determine the discriminant of this equation and explain what it tells you about when the projectile will be at height h = 0 (ground level).</p>
                    <p>How would changing the initial velocity affect the discriminant and what would this mean physically?</p>
                """,
                "answer": """
                    <p>To find when the projectile will be at ground level, we set h = 0:</p>
                    <p class="math-expression">-4.9t² + 30t + 2 = 0</p>
                    <p>For this quadratic equation:</p>
                    <ul>
                        <li>a = -4.9</li>
                        <li>b = 30</li>
                        <li>c = 2</li>
                    </ul>
                    <p>The discriminant is:</p>
                    <p class="math-expression">Δ = b² - 4ac = 30² - 4(-4.9)(2) = 900 + 39.2 = 939.2</p>
                    <p>Since the discriminant is positive (939.2 > 0), the projectile will hit the ground at two different times. This means the projectile rises, reaches maximum height, and then falls back to hit the ground.</p>
                    <p><strong>Effect of changing initial velocity:</strong> The initial velocity is represented by the coefficient b = 30. If we increase this value, the discriminant would increase, making the time difference between launch and landing greater. If we decrease it enough, the projectile might not reach high enough to have two ground intersections.</p>
                """
            },
            # Add other questions for engineering, financial, and creative categories...
        ]
    }
    
    return render_math_resource(content_data)

# Function to load math resource from JSON
def load_from_json(json_file_path):
    """Load math resource content from a JSON file"""
    with open(json_file_path, 'r') as f:
        content_data = json.load(f)
    return render_math_resource(content_data)