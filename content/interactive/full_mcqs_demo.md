```{raw} html

<!doctype html>
<html>
<head>
    <title>Comprehensive MCQ Algorithm Demo</title>
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

    <!-- Vis.js for knowledge graph -->
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>


</head>


<body>
    <div class="bkt-demo-container">
      <!-- Main two-column layout -->
      <div class="main-layout">
        <!-- Left side: MCQ content -->
        <div class="bkt-section">
          <div class="container">
            <h1>📚 Practice Questions</h1>
            <p class="subtitle">Experience how your algorithm selects and adapts questions</p>

            <div id="status" class="status loading">
              <div class="loading-spinner"></div>
              Initializing Comprehensive Demo...
            </div>

            <div id="question-selection-info" class="question-selection-info" style="display: none;">
              <h4>🎯 Why This Question Was Selected</h4>
              <div id="selection-reason"></div>
            </div>

            <div id="mcq-section" style="display: none;">
              <!-- MCQ content will be populated here -->
            </div>

            <div id="breakdown-section" class="breakdown-section" style="display: none;">
              <h3>🔍 Let's Break This Down</h3>
              <div id="breakdown-content"></div>
            </div>
          </div>
        </div>

        <!-- Right side: Knowledge Graph -->
        <div class="graph-section">
          <div class="container">
            <h1>🌐 Knowledge Graph</h1>
            <p class="subtitle">Colors show your mastery levels - watch them update as you answer questions!</p>

            <div class="mastery-legend">
              <div class="gradient-legend">
                <div class="gradient-bar"></div>
                <div class="gradient-labels">
                  <span>0% (Red)</span>
                  <span>50% (Orange)</span>
                  <span>100% (Green)</span>
                </div>
              </div>
            </div>

            <div class="graph-container" id="graph-container">
              <div id="graph-loading" class="graph-loading">
                <div class="graph-loading-spinner"></div>
                <div class="graph-loading-text">Loading Knowledge Graph...</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom section: Skills and Time controls -->
      <div class="secondary-layout">
        <div class="skills-section">
          <div class="container">
            <h1>🎯 Skills Tracking</h1>
            <div id="skills-display">
              <!-- Skills will be populated here -->
            </div>
            <button onclick="showDetailedSkills()" class="primary-btn">📊 View Detailed Skills</button>
          </div>
        </div>

        <div class="session-info">
          <div id="session-display">
            <strong>📊 Session Progress:</strong>
            <span id="session-progress">Initializing...</span>
          </div>
        </div>

        <div class="time-section">
          <div class="container">
            <h1>⏰ Time Manipulation</h1>
            <p class="subtitle">Test FSRS forgetting curves</p>

            <div class="time-controls">
              <div id="time-status">Current Time: Real Time</div>

              <button onclick="fastForward(1, 0)" class="primary-btn">⏭️ +1 Day</button>
              <button onclick="fastForward(7, 0)" class="success-btn">📅 +1 Week</button>
              <button onclick="fastForward(30, 0)" class="primary-btn">🗓️ +30 Days</button>
              <button onclick="showDecayPreview()" class="primary-btn">🔮 Preview Decay</button>
              <button onclick="resetTime()" class="danger-btn">🔄 Reset Time</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Session Complete Modal (hidden initially) -->
      <div id="session-complete-modal" style="display: none;">
        <div class="session-complete">
          <h2>🎉 Session Complete!</h2>
          <div id="final-statistics"></div>
          <button onclick="startNewSession()" class="primary-btn">Start New Session</button>
          <button onclick="reviewSession()" class="success-btn">Review Session</button>
        </div>
      </div>
    </div>


    <script type="text/javascript">
      // Global variables
      let pyodideInstance = null;
      let currentStudent = null;
      let currentMCQ = null;
      let selectedOption = null;
      let isInitialized = false;
      let sessionQuestions = [];
      let currentQuestionIndex = 0;
      let sessionStats = {
        questionsAnswered: 0,
        correctAnswers: 0,
        totalTime: 0,
        skillUpdates: [],
        masteryUpdates: []
      };

      // Knowledge graph variables
      let network;
      let currentData = {nodes: [], edges: []};
      let currentMasteryLevels = {};
      let topicIndexToNodeId = {};

      // Breakdown variables
      let isInBreakdown = false;
      let currentBreakdown = null;

      function updateStatus(message, type = 'info') {
        const statusDiv = document.getElementById('status');
        statusDiv.className = `status ${type}`;

        if (type === 'loading') {
          statusDiv.innerHTML = `<div class="loading-spinner"></div>${message}`;
        } else {
          statusDiv.textContent = message;
        }
      }

      // Initialize the comprehensive demo
      async function initializeDemo() {
        try {
          updateStatus('Loading Python environment...', 'loading');
          pyodideInstance = await loadPyodide();

          updateStatus('Setting up MCQ algorithm...', 'loading');
          await setupMCQAlgorithm();

          updateStatus('Creating student profile...', 'loading');
          await createStudent();

          updateStatus('Loading knowledge graph...', 'loading');
          await loadKnowledgeGraph();

          updateStatus('Starting session...', 'loading');
          await startSession();

          updateStatus('Ready! 🚀', 'success');
          isInitialized = true;

        } catch (error) {
          updateStatus(`❌ Initialization failed: ${error.message}`, 'error');
          console.error('Initialization error:', error);
        }
      }

      async function setupMCQAlgorithm() {
        // Load packages
        const packages = ["numpy", "networkx", "matplotlib", "sympy"];
        await pyodideInstance.loadPackage(packages);

        // Load Python code as text
        updateStatus('Loading algorithm code...', 'loading');
        const pyResponse = await fetch("../../_static/mcq_algorithm_current.py");
        if (!pyResponse.ok) {
          throw new Error(`Failed to fetch Python code: ${pyResponse.status}`);
        }
        const pythonCode = await pyResponse.text();

        // Load JSON files
        updateStatus('Loading data files...', 'loading');
        const files = [
          { name: "config.json", url: "../../_static/config.json" },
          { name: "small-graph-kg.json", url: "../../_static/small-graph-kg.json" },
          { name: "small-graph-breakdown-mcqs-computed.json", url: "../../_static/small-graph-breakdown-mcqs-computed.json" }
        ];

        for (const file of files) {
          const response = await fetch(file.url);
          if (!response.ok) {
            throw new Error(`Failed to fetch ${file.name}: ${response.status}`);
          }
          const data = await response.text();
          pyodideInstance.FS.writeFile(file.name, data);
        }

        // STEP 1: Execute the Python code first
        await pyodideInstance.runPython(pythonCode);

        // STEP 2: Then initialize the system in a separate block
        await pyodideInstance.runPythonAsync(`
      import json

      def js_export(obj):
          return json.dumps(obj)

      # Initialize the system
      kg = KnowledgeGraph(
          nodes_file='small-graph-kg.json',
          mcqs_file='small-graph-breakdown-mcqs-computed.json',
          config_file='config.json'
      )
      student_manager = StudentManager(kg.config)
      mcq_scheduler = MCQScheduler(kg, student_manager)
      bkt_instance = BayesianKnowledgeTracing(kg, student_manager)
      time_manipulator = TimeManipulator()

      # Connect systems
      mcq_scheduler.set_bkt_system(bkt_instance)
      bkt_instance.set_scheduler(mcq_scheduler)
      student_manager.set_bkt_system(bkt_instance)

      # Store globally
      globals()['kg'] = kg
      globals()['student_manager'] = student_manager
      globals()['bkt_instance'] = bkt_instance
      globals()['mcq_scheduler'] = mcq_scheduler
      globals()['time_manipulator'] = time_manipulator

      print("✅ MCQ Algorithm initialized")
        `);
      }

      async function createStudent() {
        const result = await pyodideInstance.runPythonAsync(`
          import json
          import random

          student_id = "comprehensive_demo_student"
          student = student_manager.create_student(student_id)

          # Set initial mastery levels
          for topic_idx in kg.get_all_indexes():
              mastery = random.uniform(0.1, 0.6)
              student.mastery_levels[topic_idx] = mastery
              student.confidence_levels[topic_idx] = mastery * 0.8
              student.studied_topics[topic_idx] = True

          # Initialize skills
          if hasattr(bkt_instance, 'skill_tracker') and bkt_instance.skill_tracker:
              bkt_instance.reset_student_skills(student_id)

          current_student_id = student_id
          json.dumps({"success": True, "student_id": student_id})
        `);

        const data = JSON.parse(result);
        currentStudent = data.student_id;
        updateSkillsDisplay();
      }

      async function loadKnowledgeGraph() {
        try {
          const response = await fetch('../../_static/small-graph.json');
          const graphData = await response.json();

          processGraphData(graphData);
          updateGraphWithMastery();
        } catch (error) {
          console.error('Failed to load graph:', error);
        }
      }

      async function startSession() {
        const result = await pyodideInstance.runPythonAsync(`
          import json

          # Generate session questions using select_optimal_mcqs
          selected_mcqs = mcq_scheduler.select_optimal_mcqs(current_student_id, num_questions=5)

          json.dumps({
            "success": True,
            "session_mcqs": selected_mcqs,
            "total_questions": len(selected_mcqs)
          })
        `);

        const data = JSON.parse(result);
        sessionQuestions = data.session_mcqs;
        currentQuestionIndex = 0;

        updateSessionDisplay();
        await generateCurrentMCQ();
      }


      async function generateCurrentMCQ() {
        if (currentQuestionIndex >= sessionQuestions.length) {
          await endSession();
          return;
        }

        const mcqId = sessionQuestions[currentQuestionIndex];

        try {
          const result = await pyodideInstance.runPythonAsync(`
      import json

      try:
          mcq_id = "${mcqId}"
          print(f"🔍 Looking for MCQ: {mcq_id}")

          mcq = kg.get_mcq_safely(mcq_id, need_full_text=True)
          print(f"📝 MCQ found: {mcq is not None}")

          if mcq:
              # Get question selection reasoning
              student = student_manager.get_student(current_student_id)
              topic_name = kg.get_topic_of_index(mcq.main_topic_index)
              current_mastery = student.get_mastery(mcq.main_topic_index)

              # Generate parameters if needed
              if hasattr(mcq, 'is_parameterized') and mcq.is_parameterized:
                  mcq.ensure_parameters_cached()

              # Store globally
              global current_mcq_instance
              current_mcq_instance = mcq

              result_data = {
                  "success": True,
                  "mcq_id": mcq_id,
                  "text": mcq.question_text,
                  "options": mcq.question_options,
                  "correct_index": mcq.correctindex,
                  "explanations": mcq.rendered_option_explanations,
                  "topic_name": topic_name,
                  "topic_index": mcq.main_topic_index,
                  "current_mastery": current_mastery,
                  "difficulty": getattr(mcq, 'overall_difficulty', 0.5),
                  "has_breakdown": getattr(mcq, 'has_breakdown', False),
                  "selection_reason": f"Selected due to mastery level of {current_mastery:.2f} in {topic_name}"
              }

              print(f"✅ MCQ data prepared successfully")
              final_result = json.dumps(result_data)
          else:
              error_msg = f"MCQ {mcq_id} not found"
              print(f"❌ {error_msg}")
              final_result = json.dumps({"success": False, "error": error_msg})

      except Exception as e:
          import traceback
          error_details = traceback.format_exc()
          print(f"❌ Error in generateCurrentMCQ: {error_details}")
          final_result = json.dumps({"success": False, "error": str(e)})

      final_result
          `);


          console.log('Raw result from Python:', result);

          if (!result || result.trim() === '') {
            throw new Error('Python function returned empty result');
          }

          const data = JSON.parse(result);

          if (data.success) {
            currentMCQ = data;
            displayMCQ(data);
            displaySelectionInfo(data);
          } else {
            updateStatus(`❌ Error: ${data.error}`, 'error');
            console.error('MCQ Generation Error Details:', data.details);
          }

        } catch (error) {
          updateStatus(`❌ MCQ Generation failed: ${error.message}`, 'error');
          console.error('Full error:', error);
        }
      }

      function displayMCQ(data) {
        const mcqSection = document.getElementById('mcq-section');
        document.getElementById('status').style.display = 'none';
        mcqSection.style.display = 'block';

        mcqSection.innerHTML = `
          <div class="mcq-container">
            <div class="original-question">
              <div class="mcq-question">${data.text}</div>
              <div class="mcq-meta">
                <div><strong>📚 Topic:</strong> ${data.topic_name}</div>
                <div><strong>📊 Current Mastery:</strong> ${(data.current_mastery * 100).toFixed(1)}%</div>
                <div><strong>⚡ Difficulty:</strong> ${(data.difficulty * 100).toFixed(1)}%</div>
              </div>

              <div class="mcq-options" id="original-options">
                ${data.options.map((option, index) =>
                  `<button class="mcq-option" onclick="selectOption(${index})">${option}</button>`
                ).join('')}
              </div>

              <button onclick="submitAnswer()" class="submit-btn" disabled id="submitBtn">
                ✅ Submit Answer
              </button>
            </div>
          </div>
        `;


        // Render MathJax
        if (window.MathJax) {
          MathJax.typesetPromise([mcqSection]).catch((err) => console.log('MathJax render error:', err));
        }
      }

      function displaySelectionInfo(data) {
        const infoDiv = document.getElementById('question-selection-info');
        const reasonDiv = document.getElementById('selection-reason');

        reasonDiv.innerHTML = `
          <p><strong>Topic:</strong> ${data.topic_name}</p>
          <p><strong>Current Mastery:</strong> ${(data.current_mastery * 100).toFixed(1)}%</p>
          <p><strong>Question Difficulty:</strong> ${data.difficulty.toFixed(2)}</p>
          <p><strong>Selection Reason:</strong> ${data.selection_reason}</p>
        `;

        infoDiv.style.display = 'block';
      }

      function selectOption(index) {
        selectedOption = index;

        // Update visual selection
        document.querySelectorAll('.mcq-option').forEach((btn, i) => {
          btn.classList.toggle('selected', i === index);
        });

        // Enable submit button
        const submitBtn = document.getElementById('submitBtn'); // Changed from 'submit-btn'
        if (submitBtn) {
          submitBtn.disabled = false;
        }
      }

      async function submitAnswer() {
        if (selectedOption === null) return;

        const startTime = Date.now();

        try {
          const result = await pyodideInstance.runPythonAsync(`
            import json
            import time
            from datetime import datetime

            print(f"📝 Selected option: ${selectedOption}")
            selected_option = ${selectedOption}
            mcq = current_mcq_instance
            student = student_manager.get_student(current_student_id)

            print(f"📋 MCQ found: {mcq is not None}")
            print(f"👤 Student found: {student is not None}")

            is_correct = selected_option == mcq.correctindex
            time_taken = 2.5  # Simulate time

            # Process the answer
            try:
                bkt_updates = student_manager.record_attempt(
                    current_student_id,
                    mcq.id,
                    is_correct,
                    time_taken,
                    kg
                )
                print(f"🔄 BKT updates completed: {len(bkt_updates) if bkt_updates else 0}")
            except Exception as bkt_error:
                print(f"❌ BKT processing error: {bkt_error}")
                import traceback
                print(f"📍 BKT traceback: {traceback.format_exc()}")
                bkt_updates = []  # Continue with empty updates

            # Get updated mastery
            try:
                topic_name = kg.get_topic_of_index(mcq.main_topic_index)
                mastery_after = student.get_mastery(mcq.main_topic_index)
                print(f"📊 Updated mastery: {mastery_after}")
            except Exception as mastery_error:
                print(f"❌ Mastery calculation error: {mastery_error}")
                topic_name = "Unknown Topic"
                mastery_after = 0.5

            # Check if breakdown should be triggered
            breakdown_data = None
            if not is_correct and mcq.has_breakdown:
                student_mastery = {idx: student.get_mastery(idx) for idx in kg.get_all_indexes()}
                config = {'prerequisite_skip_threshold': 0.8}

                breakdown_steps = mcq.execute_breakdown_for_student(
                    selected_option, student_mastery, config
                )

                if breakdown_steps:
                    breakdown_data = {
                        "steps": [],
                        "total_steps": len(breakdown_steps)
                    }

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

            result_data ={
                "success": True,
                "is_correct": is_correct,
                "selected_text": mcq.question_options[selected_option],
                "correct_option": mcq.question_options[mcq.correctindex],
                "explanation": mcq.rendered_option_explanations[selected_option],
                "mastery_after": mastery_after,
                "bkt_updates": len(bkt_updates),
                "has_breakdown": breakdown_data is not None,
                "breakdown": breakdown_data
            }
            final_result = json.dumps(result_data)
            print(f"📤 Final result prepared successfully")

            final_result
          `);

          const data = JSON.parse(result);
          console.log('📊 Parsed data:', data);

          // Update session stats
          sessionStats.questionsAnswered++;
          if (data.is_correct) sessionStats.correctAnswers++;
          sessionStats.totalTime += (Date.now() - startTime) / 1000;

          // Update displays
          await updateSkillsDisplay();
          await updateGraphWithMastery();
          updateSessionDisplay();
          console.log('✅ About to display result');
          if (data.has_breakdown && !data.is_correct) {
            await startBreakdown(data.breakdown);
          } else {
            displayResult(data);
          }

        } catch (error) {
          updateStatus('❌ Error submitting answer: ' + error.message, 'error');
        }
      }

      function displayResult(data) {
        const mcqSection = document.getElementById('mcq-section');

        mcqSection.innerHTML = `
          <div class="mcq-result">
            <div class="result-header ${data.is_correct ? 'correct' : 'incorrect'}">
              <h3>${data.is_correct ? '✅ Correct!' : '❌ Incorrect'}</h3>
            </div>

            <div class="result-content">
              <p><strong>Your Answer:</strong> ${data.selected_text}</p>
              <p><strong>Correct Answer:</strong> ${data.correct_option}</p>
              <p><strong>Explanation:</strong> ${data.explanation}</p>
              <p><strong>Updated Mastery:</strong> ${(data.mastery_after * 100).toFixed(1)}%</p>
            </div>

            <button onclick="nextQuestion()" class="submit-btn primary">
              ${currentQuestionIndex + 1 < sessionQuestions.length ? '➡️ Next Question' : '🏁 Complete Session'}
            </button>
          </div>
        `;
      }

      async function startBreakdown(breakdownData) {
        isInBreakdown = true;
        currentBreakdown = {
          steps: breakdownData.steps,
          currentStep: 0,
          totalSteps: breakdownData.total_steps,
          completedSteps: []
        };

        displayBreakdownStep(0);
        document.getElementById('breakdown-section').style.display = 'block';
      }

      function displayBreakdownStep(stepIndex) {
        const step = currentBreakdown.steps[stepIndex];
        const breakdownContent = document.getElementById('breakdown-content');

        breakdownContent.innerHTML = `
          <div class="step-progress">
            <h4>Step ${stepIndex + 1} of ${currentBreakdown.totalSteps}: ${step.step_type}</h4>
          </div>

          <div class="breakdown-question">
            <p>${step.text}</p>
          </div>

          <div class="breakdown-options">
            ${step.options.map((option, index) => `
              <button class="mcq-option" onclick="selectBreakdownOption(${index})" id="breakdown-option-${index}">
                <span class="option-letter">${String.fromCharCode(65 + index)}</span>
                <span class="option-text">${option}</span>
              </button>
            `).join('')}
          </div>

          <button id="breakdown-submit" class="submit-btn primary" onclick="submitBreakdownStep()" disabled>
            Submit Step
          </button>

          <div id="breakdown-result" style="display: none;"></div>
        `;

        if (window.MathJax) {
          MathJax.typesetPromise([breakdownContent]).catch((err) => console.log('MathJax render error:', err));
        }
      }

      function selectBreakdownOption(index) {
        selectedOption = index;

        document.querySelectorAll('.breakdown-options .mcq-option').forEach((btn, i) => {
          btn.classList.toggle('selected', i === index);
        });

        document.getElementById('breakdown-submit').disabled = false;
      }

      async function submitBreakdownStep() {
        const stepIndex = currentBreakdown.currentStep;
        const step = currentBreakdown.steps[stepIndex];
        const isCorrect = selectedOption === step.correctindex;

        // Record breakdown step result
        await pyodideInstance.runPythonAsync(`
          bkt_instance.process_breakdown_step_response(
              current_student_id,
              "${step.step_type}",
              ${isCorrect ? 'True' : 'False'},
              2.0
          )
        `);

        // Show result
        const resultDiv = document.getElementById('breakdown-result');
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `
          <div class="step-result ${isCorrect ? 'correct' : 'incorrect'}">
            <p><strong>${isCorrect ? '✅ Correct!' : '❌ Incorrect'}</strong></p>
            <p>${step.option_explanations[selectedOption]}</p>
            <button onclick="continueBreakdown()" class="submit-btn">
              ${stepIndex + 1 < currentBreakdown.totalSteps ? 'Next Step' : 'Complete Breakdown'}
            </button>
          </div>
        `;

        // Update skills display
        await updateSkillsDisplay();
      }

      function continueBreakdown() {
        const nextStep = currentBreakdown.currentStep + 1;

        if (nextStep < currentBreakdown.totalSteps) {
          currentBreakdown.currentStep = nextStep;
          selectedOption = null;
          displayBreakdownStep(nextStep);
        } else {
          completeBreakdown();
        }
      }

      function completeBreakdown() {
        isInBreakdown = false;
        currentBreakdown = null;
        document.getElementById('breakdown-section').style.display = 'none';

        // Show option to continue to next question
        const mcqSection = document.getElementById('mcq-section');
        mcqSection.innerHTML = `
          <div class="breakdown-complete">
            <h3>🎉 Breakdown Complete!</h3>
            <p>You've worked through all the steps. You should now understand the concept better!</p>
            <button onclick="nextQuestion()" class="submit-btn primary">
              ${currentQuestionIndex + 1 < sessionQuestions.length ? '➡️ Next Question' : '🏁 Complete Session'}
            </button>
          </div>
        `;
      }

      async function nextQuestion() {
        currentQuestionIndex++;
        selectedOption = null;
        document.getElementById('breakdown-section').style.display = 'none';

        if (currentQuestionIndex >= sessionQuestions.length) {
          await endSession();
        } else {
          await generateCurrentMCQ();
        }
      }

      async function endSession() {
        // Get final session statistics
        const result = await pyodideInstance.runPythonAsync(`
          import json

          student = student_manager.get_student(current_student_id)
          stats = student_manager.get_student_statistics(current_student_id)

          skill_summary = {}
          if hasattr(bkt_instance, 'skill_tracker') and bkt_instance.skill_tracker:
              skill_summary = bkt_instance.get_student_skill_summary(current_student_id)

          json.dumps({
              "session_stats": stats,
              "skill_summary": skill_summary,
              "questions_in_session": len(${JSON.stringify(sessionQuestions)})
          })
        `);

        const data = JSON.parse(result);
        displaySessionComplete(data);
      }

      function displaySessionComplete(data) {
        const modal = document.getElementById('session-complete-modal');
        const statsDiv = document.getElementById('final-statistics');

        const successRate = (sessionStats.correctAnswers / sessionStats.questionsAnswered * 100).toFixed(1);

        statsDiv.innerHTML = `
          <div class="session-stats">
            <div class="stat-card">
              <h4>Questions Answered</h4>
              <div class="stat-value">${sessionStats.questionsAnswered}</div>
            </div>
            <div class="stat-card">
              <h4>Success Rate</h4>
              <div class="stat-value">${successRate}%</div>
            </div>
            <div class="stat-card">
              <h4>Total Time</h4>
              <div class="stat-value">${sessionStats.totalTime.toFixed(1)}s</div>
            </div>
            <div class="stat-card">
              <h4>Average Time per Question</h4>
              <div class="stat-value">${(sessionStats.totalTime / sessionStats.questionsAnswered).toFixed(1)}s</div>
            </div>
          </div>

          <div class="skill-improvements">
            <h3>🎯 Skill Improvements This Session</h3>
            <div id="session-skill-summary"></div>
          </div>
        `;

        modal.style.display = 'block';
      }

      // Skills display functions
      async function updateSkillsDisplay() {
        const result = await pyodideInstance.runPythonAsync(`
          import json

          student = student_manager.get_student(current_student_id)

          skills = {}
          if hasattr(student, 'ability_levels'):
              skills = student.ability_levels.copy()

          json.dumps(skills)
        `);

        const skills = JSON.parse(result);
        const skillsDiv = document.getElementById('skills-display');

        if (Object.keys(skills).length === 0) {
          skillsDiv.innerHTML = '<p>No skills data available</p>';
          return;
        }

        skillsDiv.innerHTML = Object.entries(skills).map(([skill, level]) => `
          <div class="skill-item">
            <span class="skill-name">${skill.replace('_', ' ').toUpperCase()}</span>
            <div class="skill-bar">
              <div class="skill-fill" style="width: ${level * 100}%"></div>
            </div>
            <span class="skill-value">${(level * 100).toFixed(0)}%</span>
          </div>
        `).join('');
      }

      // Time manipulation functions
      async function fastForward(days, hours) {
        const result = await pyodideInstance.runPythonAsync(`
          import json

          # Fast forward time
          time_manipulator.fast_forward(days=${days}, hours=${hours})

          # Apply forgetting to student mastery
          student = student_manager.get_student(current_student_id)
          decayed_topics = 0

          if bkt_instance.fsrs_forgetting:
              for topic_idx, mastery in list(student.mastery_levels.items()):
                  if mastery > 0.05:
                      new_mastery = bkt_instance.fsrs_forgetting.apply_forgetting(
                          current_student_id, topic_idx, mastery
                      )
                      if new_mastery != mastery:
                          student.mastery_levels[topic_idx] = new_mastery
                          decayed_topics += 1

          time_info = time_manipulator.get_time_info()

          json.dumps({
              "success": True,
              "time_info": time_info,
              "decayed_topics": decayed_topics
          })
        `);

        const data = JSON.parse(result);
        updateTimeStatus(data.time_info);
        await updateGraphWithMastery();

        alert(`⏰ Fast forwarded ${days} days and ${hours} hours!\n🔄 ${data.decayed_topics} topics experienced memory decay.`);
      }

      async function resetTime() {
        await pyodideInstance.runPythonAsync(`
          time_manipulator.reset_time()
        `);

        const result = await pyodideInstance.runPythonAsync(`
          import json
          json.dumps(time_manipulator.get_time_info())
        `);

        const timeInfo = JSON.parse(result);
        updateTimeStatus(timeInfo);
        alert('⏰ Time reset to real time!');
      }

      function updateTimeStatus(timeInfo) {
        const statusDiv = document.getElementById('time-status');

        if (timeInfo.time_manipulation_active) {
          statusDiv.innerHTML = `
            <strong>Simulated Time:</strong><br>
            ${timeInfo.simulated_time}<br>
            <small>Offset: +${timeInfo.offset_days}d ${timeInfo.offset_hours}h</small>
          `;
        } else {
          statusDiv.innerHTML = `<strong>Current Time:</strong> Real Time`;
        }
      }

      async function showDecayPreview() {
        const result = await pyodideInstance.runPythonAsync(`
          import json
          preview = preview_decay_simulation(bkt_instance, current_student_id, days_ahead=7)
          json.dumps(preview)
        `);

        const preview = JSON.parse(result);

        let message = `🔮 7-Day Decay Preview:\n\n`;
        preview.topics.slice(0, 5).forEach(topic => {
          message += `${topic.topic_name}: ${(topic.current_mastery * 100).toFixed(1)}% → ${(topic.predicted_mastery * 100).toFixed(1)}% (-${topic.decay_percentage.toFixed(1)}%)\n`;
        });

        alert(message);
      }

      function updateSessionDisplay() {
        const progressDiv = document.getElementById('session-progress');
        const progress = `${currentQuestionIndex + 1} / ${sessionQuestions.length} questions`;
        const accuracy = sessionStats.questionsAnswered > 0 ?
          ` | ${(sessionStats.correctAnswers / sessionStats.questionsAnswered * 100).toFixed(1)}% accuracy` : '';

        progressDiv.textContent = progress + accuracy;
      }

      // Knowledge graph functions
      function processGraphData(graphData) {
        currentData = {
          nodes: graphData.nodes.map(node => ({
            id: node.id,
            label: node.label,
            group: node.group,
            color: getMasteryColor(null)
          })),
          edges: graphData.edges
        };

        // Create mapping from topic names to node IDs
        graphData.nodes.forEach(node => {
          topicIndexToNodeId[node.label] = node.id;
        });

        initializeNetwork();
      }

      function getMasteryColor(masteryLevel) {
        if (masteryLevel === null || masteryLevel === undefined) {
          return '#6c757d';
        }

        const clampedMastery = Math.max(0, Math.min(1, masteryLevel));
        const hue = clampedMastery * 120;
        return `hsl(${hue}, 70%, 50%)`;
      }

      function initializeNetwork() {
        const container = document.getElementById('graph-container');

        if (!container) {
          console.error('Graph container not found - delaying initialization');
          setTimeout(() => initializeNetwork(), 500);
          return;
        }
        const options = {
          nodes: {
            shape: 'dot',
            size: 25,
            font: {
              size: 12,
              face: 'Segoe UI'
            },
            borderWidth: 0,
            shadow: true
          },
          edges: {
            width: 1,
            smooth: {
              type: 'continuous'
            },
            color: '#848484'
          },
          physics: {
            stabilization: false,
            barnesHut: {
              gravitationalConstant: -50000,
              springConstant: 0.002,
              springLength: 150
            }
          },
          layout: {
            improvedLayout: false
          },
          interaction: {
            navigationButtons: true,
            keyboard: true,
            hover: true
          }
        };

        try {
          network = new vis.Network(container, currentData, options);

          // Hide loading spinner SAFELY
          const loadingDiv = document.getElementById('graph-loading');
          if (loadingDiv) {
            loadingDiv.style.display = 'none';
          }

          console.log('✅ Network initialized successfully');
        } catch (error) {
          console.error('❌ Network initialization failed:', error);
        }
      }

      async function updateGraphWithMastery() {
        if (!network || !currentStudent) return;

        try {
          const result = await pyodideInstance.runPythonAsync(`
            import json

            student = student_manager.get_student(current_student_id)
            mastery_data = {}

            for topic_idx, mastery in student.mastery_levels.items():
                topic_name = kg.get_topic_of_index(topic_idx)
                if topic_name:
                    mastery_data[topic_name] = mastery

            json.dumps(mastery_data)
          `);

          const masteryData = JSON.parse(result);
          currentMasteryLevels = masteryData;

          // Update node colors based on mastery
          const updatedNodes = currentData.nodes.map(node => ({
            ...node,
            color: getMasteryColor(masteryData[node.label])
          }));

          currentData.nodes = updatedNodes;
          network.setData(currentData);

        } catch (error) {
          console.error('Failed to update graph mastery:', error);
        }
      }

      // Utility functions
      function startNewSession() {
        location.reload(); // Simple reset for demo
      }

      function reviewSession() {
        document.getElementById('session-complete-modal').style.display = 'none';
      }

      function showDetailedSkills() {
        // Could open a detailed skills modal
        alert('Detailed skills view would open here');
      }

      // Initialize when page loads
      document.addEventListener('DOMContentLoaded', function() {
        initializeDemo();
      });
    </script>
</body>
</html>
