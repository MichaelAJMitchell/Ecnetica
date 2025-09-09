# MCQs with Random Parameter Generation and Breakdowns

```{raw} html

<!doctype html>
<html>
<head>
    <title>Revision Area</title>
    <script src="https://cdn.jsdelivr.net/pyodide/v0.27.7/full/pyodide.js"></script>

    <!-- MathJax configuration -->
    <script>
      window.MathJax = {
        tex: {
          inlineMath: [['$', '$'], ['\\(', '\\)']],
          displayMath: [['$$', '$$'], ['\\[', '\\]']],
          processEscapes: true,
          processEnvironments: true
        },
        options: {
          ignoreHtmlClass: 'tex2jax_ignore',
          processHtmlClass: 'tex2jax_process'
        }
      };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

    <!-- Include existing stylesheet -->
    <link rel="stylesheet" href="../../_static/style.css">

</head>
<body>
  <div class="bkt-demo-container">
    <div class="container">
      <h1>MCQs Demo</h1>
      <p class="subtitle">Practise questions on topics you need to revise.</p>

      <div id="status" class="status loading">
        <div class="loading-spinner"></div>
        Initializing BKT System...
      </div>

      <div id="mcq-section" style="display: none;"></div>
    </div>  <!-- Close container div -->
  </div>

    <script type="text/javascript">
      let pyodideInstance = null;
      let currentStudent = null;
      let currentMCQ = null;
      let selectedOption = null;
      let isInitialized = false;

      // Breakdown state management
      let isInBreakdown = false;
      let currentBreakdown = null; // {steps: [], currentStep: 0, totalSteps: N, completedSteps: []}

      // Improved MathJax rendering with retry logic
      function renderMathJax(element = document) {
        if (window.MathJax) {
          // Small delay to ensure DOM is updated
          setTimeout(() => {
            MathJax.typesetPromise([element]).then(() => {
              console.log('MathJax rendered successfully');
            }).catch((err) => {
              console.log('MathJax render error:', err);
              // Retry once after another delay
              setTimeout(() => {
                MathJax.typesetPromise([element]).catch((err2) =>
                  console.log('MathJax retry failed:', err2)
                );
              }, 100);
            });
          }, 50);
        }
      }

      function updateStatus(message, type = 'info') {
        const statusDiv = document.getElementById('status');
        statusDiv.className = `status ${type}`;

        if (type === 'loading') {
          statusDiv.innerHTML = `<div class="loading-spinner"></div>${message}`;
        } else {
          statusDiv.innerHTML = message;
        }

        statusDiv.style.display = 'block';
      }


      // Automated initialization function
      async function autoInitialize() {
        try {
          console.log("🔧 Starting auto-initialization...");
          updateStatus('Loading Pyodide and packages...', 'loading');

          if (!pyodideInstance) {
            pyodideInstance = await loadPyodide({
              indexURL: "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/",
              stdout: (text) => console.log("Python:", text),
              stderr: (text) => console.error("Python Error:", text)
            });

            const packages = ["numpy", "networkx", "matplotlib", "sympy"];
            await pyodideInstance.loadPackage(packages, {
              messageCallback: (msg) => console.log(`Package loading: ${msg}`),
              errorCallback: (err) => console.error(`Package error: ${err}`)
            });
          }

          // Step 2: Load BKT code and files
          updateStatus('Loading BKT algorithm...', 'loading');

          const pyResponse = await fetch("../../_static/mcq_algorithm.py", { cache: "no-store" });
          if (!pyResponse.ok) {
            throw new Error(`Failed to fetch Python code: ${pyResponse.status}`);
          }
          const code = await pyResponse.text();
          pyodideInstance.FS.writeFile("bkt_system.py", code);

          // Load JSON files
          const files = [
            { name: "config.json", url: "../../_static/config.json" },
            { name: "kg_new.json", url: "../../_static/kg_new.json" },
            { name: "mcqs_breakdown_fixed.json", url: "../../_static/mcqs_breakdown_fixed.json" },
            { name: "computed_mcqs_breakdown.json", url: "../../_static/computed_mcqs_breakdown.json" }
          ];

          for (const file of files) {
            const response = await fetch(file.url, { cache: "no-store" });
            if (!response.ok) {
              throw new Error(`Failed to fetch ${file.name}: ${response.status}`);
            }
            const data = await response.text();
            pyodideInstance.FS.writeFile(file.name, data);
          }

          // Step 3: Initialize BKT System
          updateStatus('Initializing BKT system...', 'loading');

          await pyodideInstance.runPythonAsync(`
            import sys
            sys.path.append('.')
            import bkt_system
            from bkt_system import *
            import json

            def js_export(obj):
                return json.dumps(obj)

            # Initialize the system
            kg = bkt_system.KnowledgeGraph(
                nodes_file='kg_new.json',
                mcqs_file='computed_mcqs_breakdown.json',
                config_file='config.json'
            )
            student_manager = bkt_system.StudentManager(kg.config)
            mcq_scheduler = bkt_system.MCQScheduler(kg, student_manager)
            bkt = bkt_system.BayesianKnowledgeTracing(kg, student_manager)

            # Connect systems
            mcq_scheduler.set_bkt_system(bkt)
            student_manager.set_bkt_system(bkt)

            # Initialize global MCQ instance variable
            current_mcq_instance = None
            print("✅ Global MCQ instance variable initialized")


            # Store globally
            globals()['kg'] = kg
            globals()['student_manager'] = student_manager
            globals()['bkt'] = bkt
            globals()['mcq_scheduler'] = mcq_scheduler
          `);

          // Step 4: Create Student
          updateStatus('Creating student profile...', 'loading');

          const result = await pyodideInstance.runPythonAsync(`
            import random
            random.seed(42)

            current_student_id = "demo_student"
            student = student_manager.create_student(current_student_id)

            # Set initial mastery levels
            for topic_idx in kg.get_all_indexes():
                mastery = random.uniform(0.1, 0.6)
                student.mastery_levels[topic_idx] = mastery
                student.confidence_levels[topic_idx] = mastery * 0.8
                student.studied_topics[topic_idx] = True

            js_export({"success": True, "student_id": current_student_id})
          `);

          const data = JSON.parse(result);
          if (data.success) {
            currentStudent = data.student_id;

            // Step 5: Generate first MCQ
            updateStatus('Generating your first question...', 'loading');
            await generateMCQ();

            isInitialized = true;
          }

        } catch (error) {
          updateStatus(`❌ Initialization failed: ${error.message}`, 'error');
          console.error('Auto-initialization error:', error);
        }
      }

      async function generateMCQ() {
        try {
          updateStatus('Generating personalized question...', 'loading');

          const result = await pyodideInstance.runPythonAsync(`

            import json
            result_json = None
            try:
                # Generate MCQ only once per session, store parameters
                selected_mcqs = mcq_scheduler.select_optimal_mcqs("${currentStudent}", num_questions=1)

                if selected_mcqs:
                    mcq_id = selected_mcqs[0]
                    mcq = kg.get_mcq_safely(mcq_id, need_full_text=True)

                    if mcq:
                        # Generate parameters once and store them
                        if mcq.is_parameterized:
                            mcq.ensure_parameters_cached()  # ✅ This ensures consistent parameters
                            stored_parameters = mcq.get_current_parameters_safe()
                        else:
                            stored_parameters = {}

                        # STORE MCQ INSTANCE GLOBALLY IN PYTHON
                        global current_mcq_instance
                        current_mcq_instance = mcq


                        student = student_manager.get_student("${currentStudent}")
                        topic_name = kg.get_topic_of_index(mcq.main_topic_index)
                        current_mastery = student.get_mastery(mcq.main_topic_index)

                        # Return minimal data for JavaScript (not the full MCQ)
                        response_data = {
                            "success": True,
                            "mcq_id": str(mcq.id),
                            "text": str(mcq.question_text),             # renamed
                            "options": [str(opt) for opt in mcq.question_options],
                            "correct_index": int(mcq.correctindex),
                            "topic_name": str(topic_name),              # renamed
                            "current_mastery": float(current_mastery),    # renamed
                            "chapter": str(mcq.chapter),
                            "difficulty": float(mcq.difficulty if hasattr(mcq, "difficulty") else 0.5),
                            "has_breakdown": bool(mcq.has_breakdown),
                            "stored_parameters": dict(stored_parameters)
                        }

                        result_json = json.dumps(response_data)
                    else:
                        result_json = json.dumps({"success": False, "error": "MCQ not found"})
                else:
                    result_json = json.dumps({"success": False, "error": "No eligible MCQs found"})

            except Exception as e:
                result_json= json.dumps({"success": False, "error": str(e)})

            result_json
          `);

          const data = JSON.parse(result);

          if (data.success) {
            currentMCQ = data; // Store the minimal data
            displayMCQ(data);
            updateStatus('Question ready!', 'success');
          } else {
            updateStatus(`❌ Failed to generate question: ${data.error}`, 'error');
          }

        } catch (error) {
          updateStatus(`❌ Generation failed: ${error.message}`, 'error');
          console.error('MCQ generation error:', error);
        }
      }

      function displayMCQ(mcqData) {
        const mcqSection = document.getElementById('mcq-section');
        mcqSection.style.display = 'block';

        // Hide status div when question is displayed
        document.getElementById('status').style.display = 'none';


        // Create structure for breakdown support
        mcqSection.innerHTML = `
          <div class="mcq-container">
            <!-- Original question (always visible) -->
            <div class="original-question">
              <div class="mcq-question">${mcqData.text}</div>
              <div class="mcq-meta">
                <div><strong>📚 Topic:</strong> ${mcqData.topic_name}</div>
                <div><strong>📊 Current Mastery:</strong> ${(mcqData.current_mastery * 100).toFixed(1)}%</div>
                <div><strong>⚡ Difficulty:</strong> ${(mcqData.difficulty * 100).toFixed(1)}%</div>
              </div>

              <div class="mcq-options" id="original-options">
                ${mcqData.options.map((option, index) =>
                  `<button class="mcq-option" onclick="selectOption(${index})">${option}</button>`
                ).join('')}
              </div>

              <button onclick="submitAnswer()" class="submit-btn" disabled id="submitBtn">
                ✅ Submit Answer
              </button>
            </div>

            <!-- Breakdown section (hidden initially) -->
            <div class="breakdown-section" id="breakdown-section" style="display: none;">
              <div class="breakdown-header">
                <h4 class="breakdown-title">Not quite! Time to break the question in steps</h4>
                <div class="step-progress" id="step-progress"></div>
              </div>
              <div id="breakdown-steps-container"></div>
            </div>
          </div>
        `;

        // Re-render MathJax for the new content
        renderMathJax(mcqSection);
      }

      function selectOption(index) {
        // Remove previous selection
        document.querySelectorAll('.mcq-option').forEach(btn => btn.classList.remove('selected'));

        // Add selection to clicked option
        document.querySelectorAll('.mcq-option')[index].classList.add('selected');

        selectedOption = index;
        document.getElementById('submitBtn').disabled = false;
      }

      // answer submission with breakdown support
      async function submitAnswer() {
        if (selectedOption === null || !currentMCQ) return;

        try {
          updateStatus('Processing your answer...', 'loading');

          const result = await pyodideInstance.runPythonAsync(`
            import json
            result_json = None  # Initialize result variable

            try:
                # 🔑 USE THE STORED MCQ INSTANCE (not get_mcq_safely!)
                mcq = current_mcq_instance  # This preserves cached parameters!

                selected_option = ${selectedOption}
                correct_index = ${currentMCQ.correct_index}
                is_correct = selected_option == correct_index

                # Record the attempt and get BKT updates
                bkt_updates = student_manager.record_attempt(
                    "${currentStudent}", mcq.id, is_correct, 30.0, kg
                )

                # Get response data using the SAME MCQ instance
                student = student_manager.get_student("${currentStudent}")
                topic_name = kg.get_topic_of_index(mcq.main_topic_index)

                mastery_before = None
                mastery_after = student.get_mastery(mcq.main_topic_index)
                mastery_change = 0

                if bkt_updates:
                    primary_update = next((u for u in bkt_updates if u.get('is_primary_topic', False)), None)
                    if primary_update:
                        mastery_before = primary_update['mastery_before']
                        mastery_change = primary_update['mastery_change']

                # Check for breakdown trigger
                breakdown_data = None
                if not is_correct and mcq.has_breakdown:
                    print(f"Triggering breakdown for wrong answer {selected_option}")
                    breakdown_steps = mcq.execute_breakdown_for_student(
                        selected_option, student.mastery_levels, kg.config.config
                    )
                    if breakdown_steps:
                        print(f"Generated {len(breakdown_steps)} breakdown steps")
                        # Console log for prerequisite skipping
                        for i, step in enumerate(breakdown_steps):
                            print(f"Step {i+1}: {step.step_type}")

                        breakdown_data = {
                            "steps": [],
                            "total_steps": len(breakdown_steps)
                        }

                        # Convert breakdown steps to JSON-serializable format
                        for step in breakdown_steps:
                            step_dict = {
                                "step_no": step.step_no,
                                "step_type": step.step_type,
                                "text": step.render_step_text(),
                                "options": step.render_step_options(),
                                "correctindex": step.correctindex,
                                "option_explanations": step.render_step_option_explanations()
                            }
                            breakdown_data["steps"].append(step_dict)

                response_data = {
                    "is_correct": is_correct,
                    "selected_text": mcq.question_options[selected_option],
                    "correct_option": mcq.question_options[correct_index],
                    "explanation": mcq.rendered_option_explanations[selected_option],
                    "main_topic": topic_name,
                    "before_mastery": mastery_before or mastery_after,
                    "after_mastery": mastery_after,
                    "mastery_change": mastery_change,
                    "total_changes": len(bkt_updates),
                    "has_breakdown": breakdown_data is not None,
                    "breakdown": breakdown_data
                }

                # ✅ Use json.dumps instead of js_export
                result_json = json.dumps(response_data)

            except Exception as e:
                # ✅ Handle exceptions properly
                result_json = json.dumps({"error": str(e), "success": False})

            # ✅ Return the result
            result_json
          `);


          const data = JSON.parse(result);

          // Check for errors
          if (data.error) {
            updateStatus(`❌ Error: ${data.error}`, 'error');
            return;
          }

          // Check if breakdown should be triggered
          if (!data.is_correct && data.has_breakdown) {
            await startBreakdown(data);
          } else {
            displayResult(data);
          }

          // Reset for next question
          selectedOption = null;
          const startingBreakdown = !data.is_correct && data.has_breakdown;
          if (!startingBreakdown) {
            currentMCQ = null;
          }

        } catch (error) {
          updateStatus('❌ Submission failed: ' + error.message, 'error');
          console.error('Answer submission error:', error);
        }
      }

      // Start breakdown sequence
      async function startBreakdown(resultData) {
        isInBreakdown = true;
        currentBreakdown = {
          steps: resultData.breakdown.steps,
          currentStep: 0,
          totalSteps: resultData.breakdown.total_steps,
          completedSteps: []
        };

        // Show breakdown section
        document.getElementById('breakdown-section').style.display = 'block';
        document.getElementById('status').style.display = 'none';

        // Disable original question options
        document.querySelectorAll('#original-options .mcq-option').forEach(btn => {
          btn.disabled = true;
          btn.style.opacity = '0.6';
        });
        document.getElementById('submitBtn').disabled = true;
        document.getElementById('submitBtn').style.opacity = '0.6';

        // Display first breakdown step
        displayBreakdownStep(0);

        // Re-render MathJax
        renderMathJax(document.getElementById('breakdown-section'));
      }

      // Display breakdown step
      function displayBreakdownStep(stepIndex) {
        const step = currentBreakdown.steps[stepIndex];
        const container = document.getElementById('breakdown-steps-container');

        // Update progress
        document.getElementById('step-progress').textContent =
          `Step ${stepIndex + 1} of ${currentBreakdown.totalSteps}`;

        // Build steps HTML - show completed steps and current step
        let stepsHTML = '';

        // Show all completed steps
        for (let i = 0; i < stepIndex; i++) {
          const completedStep = currentBreakdown.completedSteps[i];
          const stepData = currentBreakdown.steps[i];

          stepsHTML += `
            <div class="breakdown-step step-completed">
              <div class="step-header">
                <h4 class="step-title">Step ${i + 1}: ${stepData.step_type}</h4>
                <span class="step-type-badge">${stepData.step_type}</span>
              </div>
              <div class="step-question">${stepData.text}</div>
              <div class="step-options">
                ${stepData.options.map((option, idx) => {
                  const isSelected = idx === completedStep.selectedAnswer;
                  const isCorrect = idx === stepData.correctindex;
                  let className = 'mcq-option';
                  if (isSelected) className += ' selected';
                  if (isCorrect) className += ' correct';
                  return `<div class="${className}">${option}</div>`;
                }).join('')}
              </div>
              <div class="step-explanation ${completedStep.wasCorrect ? 'correct' : 'incorrect'}">
                <strong>Explanation:</strong> ${stepData.option_explanations[completedStep.selectedAnswer]}
              </div>
            </div>
          `;
        }

        // Show current active step
        if (stepIndex < currentBreakdown.totalSteps) {
          stepsHTML += `
            <div class="breakdown-step" id="current-step">
              <div class="step-header">
                <h4 class="step-title">Step ${stepIndex + 1}: ${step.step_type}</h4>
                <span class="step-type-badge">${step.step_type}</span>
              </div>
              <div class="step-question">${step.text}</div>
              <div class="step-options">
                ${step.options.map((option, index) =>
                  `<button class="mcq-option" onclick="selectBreakdownOption(${index})">${option}</button>`
                ).join('')}
              </div>

              <button onclick="submitBreakdownAnswer(${stepIndex})" class="submit-btn" disabled id="breakdownSubmitBtn">
                ✅ Submit Answer
              </button>

              <div id="breakdown-explanation-${stepIndex}" style="display: none;"></div>
            </div>
          `;
        }

        container.innerHTML = stepsHTML;
        // ✅ CRITICAL: Re-render MathJax for the new content
        if (window.MathJax) {
          MathJax.typesetPromise([container]).catch((err) => console.log('MathJax render error:', err));
        }

        // Reset selection
        selectedOption = null;
      }

      // Select option in breakdown step
      function selectBreakdownOption(index) {
        // Remove previous selection
        document.querySelectorAll('#current-step .mcq-option').forEach(btn => btn.classList.remove('selected'));

        // Add selection to clicked option
        document.querySelectorAll('#current-step .mcq-option')[index].classList.add('selected');

        selectedOption = index;
        document.getElementById('breakdownSubmitBtn').disabled = false;
      }

      // Submit breakdown answer
      async function submitBreakdownAnswer(stepIndex) {
      if (selectedOption === null) return;

      const step = currentBreakdown.steps[stepIndex];
      const isCorrect = selectedOption === step.correctindex;

      try {
        //  USE THE GLOBAL MCQ INSTANCE - fully consistent approach
        await pyodideInstance.runPythonAsync(`
          # Use the same global MCQ instance for consistency
          mcq = current_mcq_instance

          # Record breakdown step as attempt on parent MCQ for BKT updates
          student_manager.record_attempt(
              "${currentStudent}",
              mcq.id,  # Use the actual MCQ instance ID
              ${isCorrect ? 'True' : 'False'},
              15.0,
              kg
          )
          print(f"Recorded breakdown step ${stepIndex} against parent MCQ {mcq.id}: {'correct' if ${isCorrect ? 'True' : 'False'} else 'incorrect'}")

        `);

        // Store completion data
        currentBreakdown.completedSteps[stepIndex] = {
          selectedAnswer: selectedOption,
          wasCorrect: isCorrect
        };

        // Show explanation
        const explanationDiv = document.getElementById(`breakdown-explanation-${stepIndex}`);
        explanationDiv.style.display = 'block';
        explanationDiv.className = `step-explanation ${isCorrect ? 'correct' : 'incorrect'}`;
        explanationDiv.innerHTML = `
          <strong>Explanation:</strong> ${step.option_explanations[selectedOption]}
          <button class="continue-btn" onclick="continueBreakdown(${stepIndex})">
            ${stepIndex + 1 < currentBreakdown.totalSteps ? 'Continue to Next Step' : 'Complete Breakdown'}
          </button>
        `;

        // Disable step options
        document.querySelectorAll('#current-step .mcq-option').forEach(btn => {
          btn.disabled = true;
          btn.style.opacity = '0.6';
        });
        document.getElementById('breakdownSubmitBtn').disabled = true;
        document.getElementById('breakdownSubmitBtn').style.opacity = '0.6';

        // Re-render MathJax for explanation
        if (window.MathJax) {
          MathJax.typesetPromise([explanationDiv]).catch((err) => console.log('MathJax render error:', err));
        }

      } catch (error) {
        console.error('Error recording breakdown step:', error);
      }
    }
      // Continue to next breakdown step or complete
      function continueBreakdown(currentStepIndex) {
        const nextStepIndex = currentStepIndex + 1;

        if (nextStepIndex < currentBreakdown.totalSteps) {
          // Move to next step
          currentBreakdown.currentStep = nextStepIndex;
          selectedOption = null;
          displayBreakdownStep(nextStepIndex);
        } else {
          // Complete breakdown
          completeBreakdown();
        }
      }

      // Complete breakdown sequence
      function completeBreakdown() {
        const container = document.getElementById('breakdown-steps-container');

        // Show completion message
        container.innerHTML = `
          <div class="breakdown-complete">
            <h4>🎉 Breakdown Complete!</h4>
            <p>You've worked through all the steps. Now you should understand the concept better!</p>
            <button class="continue-btn" onclick="startNewQuestion()">Try Another Question</button>
          </div>
        `;

        // Update progress
        document.getElementById('step-progress').textContent = 'Complete!';

        // Reset breakdown state
        isInBreakdown = false;
        currentBreakdown = null;
        selectedOption = null;

        // Re-render MathJax
        renderMathJax(container);
      }

      // Start new question
      function startNewQuestion() {
        // Reset all state
        currentMCQ = null;
        selectedOption = null;

        // Hide breakdown section
        document.getElementById('breakdown-section').style.display = 'none';

        // Generate new question
        generateMCQ();
      }


      function displayResult(result) {
        const mcqSection = document.getElementById('mcq-section');
        const isCorrect = result.is_correct;
        const resultClass = isCorrect ? 'mcq-result-success' : 'mcq-result-error';
        const icon = isCorrect ? '✅' : '❌';
        const changeIcon = result.mastery_change > 0 ? '📈' : result.mastery_change < 0 ? '📉' : '➖';


        mcqSection.innerHTML = `
          <div class="mcq-container" style="border-color: ${borderColor}; background-color: ${bgColor}; color: ${textColor};">
            <h3>${icon} ${isCorrect ? 'Excellent!' : 'Not quite right, but you\'re learning!'}</h3>

            <div class="result-details">
              <p><strong>Your answer:</strong> ${result.selected_text}</p>
              <p><strong>Correct answer:</strong> ${result.correct_option}</p>
              <p><strong>Explanation:</strong> ${result.explanation}</p>
            </div>

            <div class="mastery-update">
              <h4>📊 Learning Progress</h4>
              <p><strong>Topic:</strong> ${result.main_topic}</p>
              <p><strong>Mastery Change:</strong> ${changeIcon} ${(result.mastery_change * 100).toFixed(1)}%</p>
              <p><strong>New Mastery Level:</strong> ${(result.after_mastery * 100).toFixed(1)}%</p>
              <p><em>Updated ${result.total_changes} topic(s) based on your performance</em></p>
            </div>

            <button onclick="generateMCQ()" class="primary-btn continue-btn">
              🎯 Next Question
            </button>
          </div>
        `;

        // Reset for next question
        selectedOption = null;
        currentMCQ = null;

        // Re-render MathJax
        renderMathJax(mcqSection);
      }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', autoInitialize);
    } else {
      autoInitialize();
    }
    </script>
</body>
</html>
