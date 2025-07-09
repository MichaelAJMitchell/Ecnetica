/**
 * MCQ Quiz Module with LaTeX Support
 * Creates and manages multiple-choice quizzes with explanations, scoring, and LaTeX rendering
 */
const MCQQuiz = (function() {
    /**
     * Creates a new MCQ quiz
     * @param {string} containerId - ID of the container element where the quiz will be inserted
     * @param {Object} quizData - Object containing quiz data
     * @param {string} quizData.title - Title of the quiz
     * @param {Array} quizData.questions - Array of question objects
     * @param {Object} options - Additional options for the quiz
     * @param {boolean} options.renderLatex - Whether to render LaTeX expressions (default: true)
     * @returns {Object} - Quiz control object with methods to interact with the quiz
     */
    function createQuiz(containerId, quizData, options = {}) {
        if (!containerId || !quizData || !quizData.questions || !quizData.questions.length) {
            console.error('Invalid quiz parameters');
            return null;
        }
        
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Container element with ID '${containerId}' not found`);
            return null;
        }
        
        // Default options
        const defaultOptions = {
            renderLatex: true
        };
        
        // Merge provided options with defaults
        const quizOptions = { ...defaultOptions, ...options };
        
        // Generate a random quiz ID if not provided
        const quizId = `mcq_${Math.random().toString(36).substring(2, 10)}`;
        const title = quizData.title || 'Multiple Choice Quiz';
        const questions = quizData.questions;
        const totalQuestions = questions.length;
        
        // Insert HTML structure
        container.innerHTML = generateQuizHTML(quizId, title, totalQuestions);
        
        // Get DOM elements
        const elements = {
            currentQuestion: document.getElementById(`${quizId}-current-question`),
            difficultyLevel: document.getElementById(`${quizId}-difficulty-level`),
            progressBar: document.getElementById(`${quizId}-progress-bar`),
            questionText: document.getElementById(`${quizId}-question-text`),
            optionsContainer: document.getElementById(`${quizId}-options-container`),
            explanationContainer: document.getElementById(`${quizId}-explanation-container`),
            explanationTitle: document.querySelector(`#${quizId}-explanation-container h4`),
            explanationText: document.getElementById(`${quizId}-explanation-text`),
            breakdownContainer: document.getElementById(`${quizId}-breakdown-container`),
            resultContainer: document.getElementById(`${quizId}-result-container`),
            score: document.getElementById(`${quizId}-score`),
            proficiencyLevel: document.getElementById(`${quizId}-proficiency-level`),
            prevBtn: document.getElementById(`${quizId}-prev-btn`),
            nextBtn: document.getElementById(`${quizId}-next-btn`),
            questionContainer: document.getElementById(`${quizId}-question-container`)
        };
        
        // Quiz state
        const state = {
            currentQuestionIndex: 0,
            answers: Array(questions.length).fill(null),
            answerSelected: false
        };
        
        // Initialize event listeners
        elements.prevBtn.addEventListener('click', goToPreviousQuestion);
        elements.nextBtn.addEventListener('click', goToNextQuestion);
        
        // Load the first question
        loadQuestion(0);
        
        /**
         * Handles LaTeX rendering for elements
         * @param {HTMLElement|HTMLElement[]} elements - Single element or array of elements to process
         */
        function renderLatex(elements) {
            if (!quizOptions.renderLatex) return;
            
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
                    // Typeset specific nodes if possible
                    if (MathJax.typeset) {
                        MathJax.typeset(elements);
                    } else {
                        // Fallback to document-wide typesetting
                        MathJax.Hub?.Queue(['Typeset', MathJax.Hub]);
                    }
                } catch (e) {
                    console.warn('Error rendering LaTeX:', e);
                }
            }, 0);
        }
        
        /**
         * Loads a question by index
         * @param {number} index - Index of the question to load
         */
        function loadQuestion(index) {
            const question = questions[index];
            
            // Set question text with HTML support for LaTeX
            elements.questionText.innerHTML = question.text;
            
            elements.difficultyLevel.textContent = question.difficulty || 'Basic';
            
            elements.optionsContainer.innerHTML = '';
            
            // Create options
            question.options.forEach((option, optIndex) => {
                const optionEl = document.createElement('div');
                optionEl.className = 'option';
                if (state.answers[index] === optIndex) {
                    optionEl.classList.add('selected');
                }
                
                optionEl.addEventListener('click', () => selectOption(optIndex));
                
                const optionLabel = document.createElement('label');
                optionLabel.className = 'option-label';
                
                const optionInput = document.createElement('input');
                optionInput.type = 'radio';
                optionInput.name = 'question-option';
                optionInput.checked = state.answers[index] === optIndex;
                
                optionLabel.appendChild(optionInput);
                
                // Create a span for option text to properly handle HTML/LaTeX
                const optionText = document.createElement('span');
                optionText.innerHTML = option;
                optionLabel.appendChild(optionText);
                
                optionEl.appendChild(optionLabel);
                elements.optionsContainer.appendChild(optionEl);
            });
            
            // Update UI state
            elements.currentQuestion.textContent = index + 1;
            elements.progressBar.style.width = `${((index + 1) / questions.length) * 100}%`;
            
            elements.prevBtn.style.display = index > 0 ? 'block' : 'none';
            elements.nextBtn.textContent = index === questions.length - 1 ? 'Finish' : 'Next';
            
            state.answerSelected = state.answers[index] !== null;
            elements.nextBtn.disabled = !state.answerSelected;
            
            elements.explanationContainer.style.display = 'none';
            elements.breakdownContainer.style.display = 'none';
            
            // Show explanation if answer was selected previously
            if (state.answers[index] !== null) {
                showExplanation(index);
            }
            
            // Render LaTeX in question and options
            if (quizOptions.renderLatex) {
                renderLatex([
                    elements.questionText,
                    ...Array.from(elements.optionsContainer.querySelectorAll('.option-label span'))
                ]);
            }
        }
        
        /**
         * Handles option selection
         * @param {number} optionIndex - Index of the selected option
         */
        function selectOption(optionIndex) {
            state.answers[state.currentQuestionIndex] = optionIndex;
            state.answerSelected = true;
            elements.nextBtn.disabled = false;
            
            // Mark selected option
            const options = elements.optionsContainer.querySelectorAll('.option');
            options.forEach((option, index) => {
                if (index === optionIndex) {
                    option.classList.add('selected');
                } else {
                    option.classList.remove('selected');
                }
            });
            
            // Show explanation
            showExplanation(state.currentQuestionIndex);
        }
        
        /**
         * Shows explanation for the current question
         * @param {number} index - Index of the question
         */
        function showExplanation(index) {
            const question = questions[index];
            const selectedAnswer = state.answers[index];
            
            // Use option_explanations if available, otherwise fall back to explanation
            let explanationText = '';
            if (question.option_explanations && question.option_explanations[selectedAnswer]) {
                explanationText = question.option_explanations[selectedAnswer];
            } else {
                explanationText = question.explanation || '';
            }
            
            // Use innerHTML to support LaTeX rendering
            elements.explanationText.innerHTML = explanationText;
            elements.explanationContainer.style.display = 'block';
            
            if (state.answers[index] === question.correctIndex) {
                elements.explanationContainer.classList.add('correct');
                elements.explanationContainer.classList.remove('incorrect');
                elements.explanationTitle.textContent = 'Correct!';
                elements.explanationTitle.classList.add('correct');
                elements.explanationTitle.classList.remove('incorrect');
            } else {
                elements.explanationContainer.classList.add('incorrect');
                elements.explanationContainer.classList.remove('correct');
                elements.explanationTitle.textContent = 'Incorrect';
                elements.explanationTitle.classList.add('incorrect');
                elements.explanationTitle.classList.remove('correct');
            }
            
            // Show solution breakdown if available
            if (question.solution_breakdown) {
                showSolutionBreakdown(question.solution_breakdown);
            }
            
            // Render LaTeX in explanation
            if (quizOptions.renderLatex) {
                renderLatex(elements.explanationText);
            }
        }
        
        /**
         * Shows step-by-step solution breakdown
         * @param {Array} breakdown - Array of solution steps
         */
        function showSolutionBreakdown(breakdown) {
            const breakdownContainer = document.getElementById(`${quizId}-breakdown-container`);
            if (!breakdownContainer) return;
            
            // Create solution breakdown HTML
            let breakdownHTML = '<div class="solution-breakdown"><h5>Step-by-Step Solution</h5>';
            
            breakdown.forEach((step, index) => {
                breakdownHTML += `
                    <div class="solution-step">
                        <div class="step-description">Step ${index + 1}: ${step.description}</div>
                        ${step.equation ? `<div class="step-equation">${step.equation}</div>` : ''}
                        ${step.reasoning ? `<div class="step-reasoning">${step.reasoning}</div>` : ''}
                    </div>
                `;
            });
            
            breakdownHTML += '</div>';
            
            breakdownContainer.innerHTML = breakdownHTML;
            breakdownContainer.style.display = 'block';
            
            // Render LaTeX in breakdown
            if (quizOptions.renderLatex) {
                renderLatex(breakdownContainer);
            }
        }
        
        /**
         * Navigates to the previous question
         */
        function goToPreviousQuestion() {
            if (state.currentQuestionIndex > 0) {
                state.currentQuestionIndex--;
                loadQuestion(state.currentQuestionIndex);
            }
        }
        
        /**
         * Navigates to the next question or shows results
         */
        function goToNextQuestion() {
            if (state.answerSelected) {
                if (state.currentQuestionIndex < questions.length - 1) {
                    state.currentQuestionIndex++;
                    loadQuestion(state.currentQuestionIndex);
                } else {
                    showResults();
                }
            } else {
                alert("Please select an answer.");
            }
        }
        
        /**
         * Shows quiz results
         */
        function showResults() {
            let correctAnswers = 0;
            for (let i = 0; i < questions.length; i++) {
                if (state.answers[i] === questions[i].correctIndex) {
                    correctAnswers++;
                }
            }
            
            elements.score.textContent = correctAnswers;
            
            // Determine proficiency level
            let proficiencyLevel;
            if (correctAnswers === questions.length) {
                proficiencyLevel = "Expert";
            } else if (correctAnswers >= Math.ceil(questions.length * 0.8)) {
                proficiencyLevel = "Advanced";
            } else if (correctAnswers >= Math.ceil(questions.length * 0.6)) {
                proficiencyLevel = "Intermediate";
            } else if (correctAnswers >= Math.ceil(questions.length * 0.4)) {
                proficiencyLevel = "Basic";
            } else {
                proficiencyLevel = "Novice";
            }
            
            elements.proficiencyLevel.textContent = proficiencyLevel;
            
            // Update UI
            elements.questionContainer.style.display = 'none';
            elements.explanationContainer.style.display = 'none';
            elements.resultContainer.style.display = 'block';
            
            // Update next button to restart quiz
            elements.nextBtn.textContent = 'Restart';
            const oldClickHandler = elements.nextBtn.onclick;
            elements.nextBtn.onclick = () => {
                state.currentQuestionIndex = 0;
                state.answers = Array(questions.length).fill(null);
                state.answerSelected = false;
                elements.questionContainer.style.display = 'block';
                elements.resultContainer.style.display = 'none';
                loadQuestion(0);
                elements.nextBtn.textContent = 'Next';
                elements.nextBtn.onclick = oldClickHandler;
            };
        }
        
        /**
         * Generates HTML structure for the quiz
         * @param {string} quizId - Unique ID for the quiz
         * @param {string} title - Quiz title
         * @param {number} totalQuestions - Total number of questions
         * @returns {string} - HTML structure
         */
        function generateQuizHTML(quizId, title, totalQuestions) {
            return `
                <div id="${quizId}" class="mcq-module">
                    <h2 class="quiz-title">${title}</h2>
                    
                    <div id="${quizId}-progress-container" class="progress-container">
                        <div class="progress-info">
                            <span>Question <span id="${quizId}-current-question">1</span> of ${totalQuestions}</span>
                            <span>Difficulty: <span id="${quizId}-difficulty-level">Basic</span></span>
                        </div>
                        <div class="progress-bar-bg">
                            <div id="${quizId}-progress-bar" class="progress-bar"></div>
                        </div>
                    </div>
                    
                    <div id="${quizId}-question-container" class="question-container">
                        <div id="${quizId}-question-text" class="question-text"></div>
                        <div id="${quizId}-options-container" class="options-container"></div>
                    </div>
                    
                    <div id="${quizId}-explanation-container" class="explanation-container">
                        <h4 class="explanation-title">Explanation</h4>
                        <p id="${quizId}-explanation-text" class="explanation-text"></p>
                        <div id="${quizId}-breakdown-container" class="breakdown-container"></div>
                    </div>
                    
                    <div id="${quizId}-result-container" class="result-container">
                        <h3 class="result-title">Assessment Complete!</h3>
                        <p>You scored <span id="${quizId}-score">0</span> out of ${totalQuestions}</p>
                        <p>Your estimated proficiency level: <span id="${quizId}-proficiency-level">-</span></p>
                    </div>
                    
                    <div class="button-container">
                        <button id="${quizId}-prev-btn" class="nav-button prev-button">Previous</button>
                        <button id="${quizId}-next-btn" class="nav-button next-button" disabled>Next</button>
                    </div>
                </div>
            `;
        }
        
        // Return public API
        return {
            loadQuestion,
            getCurrentQuestionIndex: () => state.currentQuestionIndex,
            getAnswers: () => [...state.answers],
            reset: () => {
                state.currentQuestionIndex = 0;
                state.answers = Array(questions.length).fill(null);
                state.answerSelected = false;
                elements.questionContainer.style.display = 'block';
                elements.resultContainer.style.display = 'none';
                loadQuestion(0);
            }
        };
    }
    
    // Public API
    return {
        create: createQuiz
    };
})();