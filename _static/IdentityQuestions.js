/**
 * MathQuestionModule.js - A standalone library for creating interactive math resource modules with LaTeX support
 * 
 * This library provides functionality to create interactive math question modules
 * with multiple categories, question/answer pairs, and LaTeX rendering.
 */

const MathQuestionModule = (function() {

    // Default categories
    const DEFAULT_CATEGORIES = [
        {"id": "scientific", "name": "Scientific/Mathematic", "color_class": "scientific"},
        {"id": "engineering", "name": "Engineering/Mechanical", "color_class": "engineering"},
        {"id": "financial", "name": "Financial/Economic", "color_class": "financial"},
        {"id": "creative", "name": "Creative", "color_class": "creative"}
    ];

    /**
     * Handles LaTeX rendering for elements
     * @param {HTMLElement|HTMLElement[]} elements - Element(s) to process for LaTeX rendering
     */
    function renderLatex(elements) {
        // Ensure we have MathJax available
        if (typeof MathJax === 'undefined') {
            console.warn('MathJax is not available. LaTeX rendering skipped.');
            return;
        }
        
        // Handle both single elements and arrays
        if (!Array.isArray(elements)) {
            elements = [elements];
        }
        
        // Delay typesetting slightly to ensure content is in the DOM
        setTimeout(() => {
            try {
                // Use the appropriate MathJax API depending on version
                if (MathJax.typeset) {
                    // MathJax v3
                    MathJax.typeset(elements);
                } else if (MathJax.Hub) {
                    // MathJax v2
                    MathJax.Hub.Queue(['Typeset', MathJax.Hub, elements]);
                }
            } catch (e) {
                console.warn('Error rendering LaTeX:', e);
            }
        }, 10);
    }

    // Main rendering function for the module
    function render(contentData, targetElementId, options = {}) {
        // Default options
        const defaultOptions = {
            renderLatex: true
        };
        
        // Merge provided options with defaults
        const moduleOptions = { ...defaultOptions, ...options };
        
        // Ensure styles are injected
        injectStyles();
        
        // Find target element
        const targetElement = document.getElementById(targetElementId);
        if (!targetElement) {
            console.error(`Target element with ID '${targetElementId}' not found`);
            return null;
        }
        
        // Clear previous content
        targetElement.innerHTML = '';
        
        // Create main container
        const container = document.createElement('div');
        container.className = 'math-question-module';
        container.id = `${targetElementId}-module`;
        
        // Create the question container
        const questionContainer = document.createElement('div');
        questionContainer.className = 'question-container';
        
        // Add title
        const title = document.createElement('h2');
        title.innerHTML = contentData.title || 'Math Resource';
        questionContainer.appendChild(title);
        
        // Add introduction
        const topicIntro = document.createElement('div');
        topicIntro.className = 'topic-intro';
        topicIntro.innerHTML = contentData.intro_content || '';
        questionContainer.appendChild(topicIntro);
        
        // Use provided categories or fallback to defaults
        const categories = contentData.categories || DEFAULT_CATEGORIES;
        
        // Create category boxes
        const categoryBoxesContainer = document.createElement('div');
        categoryBoxesContainer.className = 'question-categories';
        
        categories.forEach(category => {
            const categoryBox = document.createElement('div');
            categoryBox.className = `category-box ${category.color_class}`;
            categoryBox.textContent = category.name;
            categoryBox.onclick = () => showQuestion(category.id, targetElementId);
            categoryBoxesContainer.appendChild(categoryBox);
        });
        
        questionContainer.appendChild(categoryBoxesContainer);
        
        // Create question content sections
        const questions = contentData.questions || [];
        questions.forEach(question => {
            const questionContent = document.createElement('div');
            questionContent.id = `${targetElementId}-${question.category}-content`;
            questionContent.className = 'question-content';
            
            const questionTitle = document.createElement('div');
            questionTitle.className = 'question-title';
            questionTitle.innerHTML = question.title;
            questionContent.appendChild(questionTitle);
            
            // Add question content
            const contentDiv = document.createElement('div');
            contentDiv.innerHTML = question.content;
            questionContent.appendChild(contentDiv);
            
            // Create answer button
            const answerButton = document.createElement('div');
            answerButton.className = 'answer-button';
            answerButton.textContent = 'Show Answer';
            answerButton.onclick = () => toggleAnswer(question.category, targetElementId);
            questionContent.appendChild(answerButton);
            
            // Create answer content
            const answerContent = document.createElement('div');
            answerContent.id = `${targetElementId}-${question.category}-answer`;
            answerContent.className = `answer-content ${question.category}-answer`;
            answerContent.innerHTML = question.answer;
            questionContent.appendChild(answerContent);
            
            questionContainer.appendChild(questionContent);
        });
        
        container.appendChild(questionContainer);
        targetElement.appendChild(container);
        
        // Render LaTeX in all content if enabled
        if (moduleOptions.renderLatex) {
            // Process all content with LaTeX
            renderLatex([
                title,
                topicIntro,
                ...Array.from(targetElement.querySelectorAll('.question-content'))
            ]);
        }
        
        // Return control object
        return {
            showQuestion: (categoryId) => showQuestion(categoryId, targetElementId),
            showAnswer: (categoryId) => {
                const answerContent = document.getElementById(`${targetElementId}-${categoryId}-answer`);
                if (answerContent) {
                    answerContent.style.display = 'block';
                    const button = answerContent.previousElementSibling;
                    if (button) button.textContent = 'Hide Answer';
                }
            },
            hideAnswer: (categoryId) => {
                const answerContent = document.getElementById(`${targetElementId}-${categoryId}-answer`);
                if (answerContent) {
                    answerContent.style.display = 'none';
                    const button = answerContent.previousElementSibling;
                    if (button) button.textContent = 'Show Answer';
                }
            }
        };
    }

    // Show a question by category ID
    function showQuestion(category, containerId) {
        // Hide all question contents first
        const contents = document.querySelectorAll(`#${containerId}-module .question-content`);
        contents.forEach(content => {
            content.style.display = 'none';
        });
        
        // Also hide all answers when switching questions
        const answers = document.querySelectorAll(`#${containerId}-module .answer-content`);
        answers.forEach(answer => {
            answer.style.display = 'none';
        });
        
        // Reset all buttons text
        const buttons = document.querySelectorAll(`#${containerId}-module .answer-button`);
        buttons.forEach(button => {
            button.textContent = 'Show Answer';
        });
        
        // Remove active class from all category boxes
        const boxes = document.querySelectorAll(`#${containerId}-module .category-box`);
        boxes.forEach(box => {
            box.classList.remove('active');
        });
        
        // Show the selected question content
        const selectedContent = document.getElementById(`${containerId}-${category}-content`);
        if (selectedContent) {
            if (selectedContent.style.display === 'block') {
                selectedContent.style.display = 'none';
            } else {
                selectedContent.style.display = 'block';
                // Add active class to the clicked box
                const activeBox = document.querySelector(`#${containerId}-module .${category}`);
                if (activeBox) activeBox.classList.add('active');
            }
        }
    }

    // Toggle answer visibility
    function toggleAnswer(category, containerId) {
        const answerContent = document.getElementById(`${containerId}-${category}-answer`);
        if (!answerContent) return;
        
        const button = answerContent.previousElementSibling;
        
        if (answerContent.style.display === 'block') {
            answerContent.style.display = 'none';
            if (button) button.textContent = 'Show Answer';
        } else {
            answerContent.style.display = 'block';
            if (button) button.textContent = 'Hide Answer';
            
            // Re-render LaTeX in the answer when shown
            if (typeof MathJax !== 'undefined') {
                renderLatex(answerContent);
            }
        }
    }

    // Return public API
    return {
        render,
        renderLatex,
        DEFAULT_CATEGORIES
    };
})();