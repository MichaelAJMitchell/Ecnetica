
# BKT Simple Demo


```{raw} html

<!doctype html>
<html>
<head>
    <title>BKT Algorithm Visual Demo</title>
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
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    
    <style>
      /* Override Jupyter Book styles for BKT demo */
      .bd-content .bkt-demo-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        background-color: #f5f5f5;
        font-family: Arial, sans-serif;
      }
      
      .bkt-demo-container .container {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
      }
      
      .bkt-demo-container .controls {
        display: flex;
        gap: 10px;
        margin: 20px 0;
        flex-wrap: wrap;
      }
      
      /* Original button styling - restore exact appearance */
      .bkt-demo-container button {
        padding: 12px 20px !important;
        font-size: 16px !important;
        border: none !important;
        border-radius: 5px !important;
        cursor: pointer;
        transition: background-color 0.3s;
        font-family: Arial, sans-serif !important;
        font-weight: normal !important;
        text-decoration: none !important;
        display: inline-block;
        text-align: center;
        vertical-align: middle;
        line-height: 1.4;
      }
      
      .bkt-demo-container .primary-btn {
        background-color: #2196F3 !important;
        color: white !important;
      }
      
      .bkt-demo-container .primary-btn:hover {
        background-color: #1976D2 !important;
        color: white !important;
      }
      
      .bkt-demo-container .success-btn {
        background-color: #4CAF50 !important;
        color: white !important;
      }
      
      .bkt-demo-container .success-btn:hover {
        background-color: #45a049 !important;
        color: white !important;
      }
      
      .bkt-demo-container .danger-btn {
        background-color: #f44336 !important;
        color: white !important;
      }
      
      .bkt-demo-container .danger-btn:hover {
        background-color: #da190b !important;
        color: white !important;
      }
      
      /* Original terminal/output styling */
      .bkt-demo-container #output {
        background-color: #f8f9fa !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 5px !important;
        padding: 15px !important;
        margin: 15px 0 !important;
        min-height: 100px !important;
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace !important;
        white-space: pre-wrap !important;
        overflow-x: auto !important;
        font-size: 14px !important;
        line-height: 1.4 !important;
        color: #333 !important;
      }
      
      /* Original status styling */
      .bkt-demo-container .status {
        padding: 10px !important;
        border-radius: 5px !important;
        margin: 10px 0 !important;
        font-family: Arial, sans-serif !important;
        font-size: 14px !important;
      }
      
      .bkt-demo-container .status.success {
        background-color: #d4edda !important;
        color: #155724 !important;
        border: 1px solid #c3e6cb !important;
      }
      
      .bkt-demo-container .status.error {
        background-color: #f8d7da !important;
        color: #721c24 !important;
        border: 1px solid #f5c6cb !important;
      }
      
      .bkt-demo-container .status.info {
        background-color: #d1ecf1 !important;
        color: #0c5460 !important;
        border: 1px solid #bee5eb !important;
      }
      
      /* Original MCQ container styling */
      .bkt-demo-container .mcq-container {
        background-color: #fff !important;
        border: 2px solid #007bff !important;
        border-radius: 8px !important;
        padding: 20px !important;
        margin: 15px 0 !important;
      }
      
      .bkt-demo-container .mcq-question {
        font-size: 18px !important;
        font-weight: bold !important;
        margin-bottom: 15px !important;
        color: #333 !important;
      }
      
      .bkt-demo-container .mcq-options {
        margin: 15px 0 !important;
      }
      
      .bkt-demo-container .mcq-option {
        display: block !important;
        margin: 8px 0 !important;
        padding: 10px !important;
        background-color: #f8f9fa !important;
        border: 2px solid #e9ecef !important;
        border-radius: 5px !important;
        cursor: pointer !important;
        transition: all 0.3s !important;
        font-family: Arial, sans-serif !important;
        font-size: 14px !important;
      }
      
      .bkt-demo-container .mcq-option:hover {
        background-color: #e9ecef !important;
        border-color: #007bff !important;
      }
      
      .bkt-demo-container .mcq-option.selected {
        background-color: #007bff !important;
        color: white !important;
        border-color: #0056b3 !important;
      }
      
      /* Original progress bar styling */
      .bkt-demo-container .progress-bar {
        width: 100% !important;
        height: 20px !important;
        background-color: #e9ecef !important;
        border-radius: 10px !important;
        overflow: hidden !important;
        margin: 10px 0 !important;
      }
      
      .bkt-demo-container .progress-fill {
        height: 100% !important;
        background-color: #28a745 !important;
        transition: width 0.3s ease !important;
      }
      
      /* Ensure text doesn't inherit Jupyter Book styling */
      .bkt-demo-container h1, .bkt-demo-container h2, .bkt-demo-container h3, .bkt-demo-container h4 {
        font-family: Arial, sans-serif !important;
      }
      
      .bkt-demo-container p {
        font-family: Arial, sans-serif !important;
        line-height: 1.5 !important;
      }
    </style>
</head>
<body>
    <div class="bkt-demo-container">
      <div class="container">
        <h1>🧠 BKT Algorithm Visual Demo</h1>
        <p>This demo shows how Bayesian Knowledge Tracing works with a simple knowledge graph.
           Students start with low mastery levels and improve through practice.</p>
        
        <div class="controls">
          <button onclick="initializeDemo()" class="primary-btn">🚀 Initialize BKT System</button>
          <button onclick="createStudent()" class="success-btn" id="createStudentBtn" disabled>👤 Create Student</button>
          <button onclick="generateMCQ()" class="primary-btn" id="generateMCQBtn" disabled>❓ Generate MCQ</button>
          <button onclick="showKnowledgeGraph()" class="primary-btn" id="showGraphBtn" disabled>📊 Show Knowledge Graph</button>
          <button onclick="resetDemo()" class="danger-btn">🔄 Reset Demo</button>
        </div>
        
        <div id="status" class="status info">Click "Initialize BKT System" to start the demo...</div>
        
        <div id="mcq-section" style="display: none;"></div>
        
        <div id="output"></div>
      </div>
    </div>

    
    <script type="text/javascript">
      let pyodideInstance = null;
      let currentStudent = null;
      let currentMCQ = null;
      let selectedOption = null;
      
      function updateStatus(message, type = 'info') {
        const statusDiv = document.getElementById('status');
        statusDiv.className = `status ${type}`;
        statusDiv.textContent = message;
      }
      
      function updateOutput(message) {
        const output = document.getElementById('output');
        output.textContent += message + '\n';
        output.scrollTop = output.scrollHeight;
      }
      
      async function initializeDemo() {
        try {
          updateStatus('🔄 Loading Pyodide and packages...', 'info');
          updateOutput('Initializing BKT demo...');
          
          if (!pyodideInstance) {
            pyodideInstance = await loadPyodide({
              indexURL: "../../_static/",  // Local core files
              packageCacheKey: "bkt-demo-v1",
              loadPackages: false
            });
            
            updateOutput('✓ Pyodide loaded successfully');
            updateOutput('Checking package cache...');
            
            // Override where packages come from AFTER initialization
            const originalIndexURL = pyodideInstance._api.config.indexURL;
            pyodideInstance._api.config.indexURL = "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/";
            
            const packages = ["numpy", "networkx", "matplotlib"];
            await pyodideInstance.loadPackage(packages, {
              messageCallback: (msg) => console.log(`Package loading: ${msg}`),
              errorCallback: (err) => console.error(`Package error: ${err}`)
            });
            
            // Restore original indexURL for any future core operations
            pyodideInstance._api.config.indexURL = originalIndexURL;
            
            updateOutput('✓ All packages loaded');
          }
          
          // Fetch and load the BKT code
          updateOutput('Fetching BKT algorithm code...');
          const pyResponse = await fetch("../../_static/mcq_algorithm_full_python.py");
          if (!pyResponse.ok) {
            throw new Error(`Failed to fetch Python code: ${pyResponse.status}`);
          }
          const code = await pyResponse.text();
          pyodideInstance.FS.writeFile("bkt_system.py", code);
          updateOutput('✓ BKT code loaded');
          
          // Fetch and load JSON files
          updateOutput('Fetching configuration files...');
          
          // Fetch config.json
          const configResponse = await fetch("../../_static/config.json");
          if (!configResponse.ok) {
            throw new Error(`Failed to fetch config.json: ${configResponse.status}`);
          }
          const configData = await configResponse.text();
          pyodideInstance.FS.writeFile("config.json", configData);
          updateOutput('✓ config.json loaded');
          
          // Fetch kg.json
          const kgResponse = await fetch("../../_static/kg.json");
          if (!kgResponse.ok) {
            throw new Error(`Failed to fetch kg.json: ${kgResponse.status}`);
          }
          const kgData = await kgResponse.text();
          pyodideInstance.FS.writeFile("kg.json", kgData);
          updateOutput('✓ kg.json loaded');
          
          // Fetch mcqs.json
          const mcqsResponse = await fetch("../../_static/mcqs.json");
          if (!mcqsResponse.ok) {
            throw new Error(`Failed to fetch mcqs.json: ${mcqsResponse.status}`);
          }
          const mcqsData = await mcqsResponse.text();
          pyodideInstance.FS.writeFile("mcqs.json", mcqsData);
          updateOutput('✓ mcqs.json loaded');
          
          // Fetch computed_mcqs.json
          const computedMcqsResponse = await fetch("../../_static/computed_mcqs.json");
          if (!computedMcqsResponse.ok) {
            throw new Error(`Failed to fetch computed_mcqs.json: ${computedMcqsResponse.status}`);
          }
          const computedMcqsData = await computedMcqsResponse.text();
          pyodideInstance.FS.writeFile("computed_mcqs.json", computedMcqsData);
          updateOutput('✓ computed_mcqs.json loaded');
          
          // Import and initialize the system
          await pyodideInstance.runPythonAsync(`
            import sys
            sys.path.append('.')
            import bkt_system
            import json
            
            # Create a helper function for JavaScript data transfer
            def js_export(obj):
                """Convert Python object to JSON string for JavaScript"""
                return json.dumps(obj)
            
            print("Initializing BKT system with configuration files...")
            
            # Initialize the system using Caoimhe's design
            kg = bkt_system.KnowledgeGraph()
            student_manager = bkt_system.StudentManager()
            mcq_scheduler = bkt_system.MCQScheduler(kg, student_manager)
            bkt = bkt_system.BayesianKnowledgeTracing(kg, student_manager)
            
            # Connect systems
            mcq_scheduler.set_bkt_system(bkt)
            student_manager.set_bkt_system(bkt)
            
            # Store everything globally for access
            globals()['kg'] = kg
            globals()['student_manager'] = student_manager
            globals()['bkt'] = bkt
            globals()['mcq_scheduler'] = mcq_scheduler
            
            print("BKT system initialized successfully!")
          `);
          
          updateStatus('✅ BKT System Ready! Create a student to begin.', 'success');
          document.getElementById('createStudentBtn').disabled = false;
          updateOutput('✓ BKT system initialised.');
          
        } catch (error) {
          updateStatus('❌ Failed to initialize BKT system', 'error');
          updateOutput(`Error: ${error.message}`);
          console.error('Initialization error:', error);
        }
      }
      
      async function createStudent() {
        try {
          updateStatus('👤 Creating student profile...', 'info');
          
          const result = await pyodideInstance.runPythonAsync(`
            # Create a student with realistic mastery levels
            current_student_id = "demo_student"
            student = student_manager.create_student(current_student_id)
            
            # Set initial mastery levels for demo topics
            import random
            random.seed(42)  # For consistent demo
            
            for topic_idx in kg.get_all_indexes():
                mastery = random.uniform(0.1, 0.6)  # Start with low mastery
                student.mastery_levels[topic_idx] = mastery
                student.confidence_levels[topic_idx] = mastery * 0.8
                student.studied_topics[topic_idx] = True  # Mark as studied
            
            # Show student status
            status = f"Student created with {len(student.mastery_levels)} topics\\n"
            status += f"Average mastery: {sum(student.mastery_levels.values()) / len(student.mastery_levels):.3f}\\n"
            status += f"Topics studied: {len([t for t, studied in student.studied_topics.items() if studied])}"
            
            js_export({"success": True, "status": status, "student_id": current_student_id})
          `);
          
          const data = JSON.parse(result);
          currentStudent = data.student_id;
          
          updateStatus('✅ Student created! Generate an MCQ to start learning.', 'success');
          document.getElementById('generateMCQBtn').disabled = false;
          document.getElementById('showGraphBtn').disabled = false;
          updateOutput(data.status);
          
        } catch (error) {
          updateStatus('❌ Failed to create student', 'error');
          updateOutput(`Error: ${error.message}`);
          console.error('Student creation error:', error);
        }
      }

      async function generateMCQ() {
        try {
          updateStatus('❓ Generating MCQ based on student mastery...', 'info');
          
          const result = await pyodideInstance.runPythonAsync(`
      import json

      print("=== COMPREHENSIVE ELIGIBILITY DEBUG ===")

      try:
          # 1. Basic checks
          print(f"Total MCQs loaded: {len(kg.mcqs)}")
          print(f"MCQ IDs sample: {list(kg.mcqs.keys())[:3]}")
          
          student = student_manager.get_student(current_student_id)
          print(f"Student found: {student is not None}")
          print(f"Student mastery levels: {len(student.mastery_levels)}")
          print(f"Student studied topics: {len(student.studied_topics)}")
          
          # 2. Check mastery threshold and due topics
          mastery_threshold = mcq_scheduler.get_config_value('algorithm_config.mastery_threshold', 0.7)
          print(f"Mastery threshold: {mastery_threshold}")
          
          due_topics = [idx for idx, mastery in student.mastery_levels.items() 
                        if mastery < mastery_threshold]
          print(f"Due topics (mastery < {mastery_threshold}): {len(due_topics)} out of {len(student.mastery_levels)}")
          
          # 3. Sample MCQ analysis
          sample_mcq_id = list(kg.mcqs.keys())[0]
          sample_mcq = kg.mcqs[sample_mcq_id]
          print(f"\\nSample MCQ analysis:")
          print(f"  MCQ ID: {sample_mcq_id}")
          print(f"  Main topic index: {sample_mcq.main_topic_index}")
          print(f"  Subtopic weights: {sample_mcq.subtopic_weights}")
          
          # Check if sample MCQ topics exist in student data
          mcq_topics = list(sample_mcq.subtopic_weights.keys())
          print(f"  MCQ covers topic indices: {mcq_topics}")
          
          student_topic_indices = list(student.studied_topics.keys())
          print(f"  Student topic indices: {student_topic_indices[:10]}...")
          
          # Check overlap
          mcq_topics_in_student = [t for t in mcq_topics if t in student_topic_indices]
          print(f"  Overlapping indices: {mcq_topics_in_student}")
          
          # 4. Check if MCQ vectors are computed
          print(f"\\nMCQ vectors computed: {len(mcq_scheduler.mcq_vectors)}")
          if sample_mcq_id in mcq_scheduler.mcq_vectors:
              vector = mcq_scheduler.mcq_vectors[sample_mcq_id]
              print(f"  Sample vector subtopic weights: {vector.subtopic_weights}")
          else:
              print("  Sample MCQ vector not found - computing vectors...")
              mcq_scheduler._ensure_vectors_computed()
              print(f"  MCQ vectors after computation: {len(mcq_scheduler.mcq_vectors)}")
          
          # 5. Test eligibility step by step for sample MCQ
          print(f"\\nStep-by-step eligibility check for sample MCQ:")
          
          # Check if all subtopics are studied
          all_studied = True
          for topic_idx in mcq_topics:
              is_studied = student.is_topic_studied(topic_idx)
              print(f"  Topic {topic_idx}: studied = {is_studied}")
              if not is_studied:
                  all_studied = False
          
          print(f"  All subtopics studied: {all_studied}")
          
          # Check if main topic is due
          main_mastery = student.get_mastery(sample_mcq.main_topic_index)
          is_due = main_mastery < mastery_threshold
          print(f"  Main topic {sample_mcq.main_topic_index} mastery: {main_mastery:.3f}")
          print(f"  Main topic is due: {is_due}")
          
          # Check if completed today
          in_daily = sample_mcq_id in student.daily_completed
          print(f"  Completed today: {in_daily}")
          
          # 6. Run actual eligibility methods
          print(f"\\nRunning eligibility methods:")
          all_eligible = mcq_scheduler.get_eligible_mcqs_for_student(current_student_id)
          greedy_eligible = mcq_scheduler.get_eligible_mcqs_for_greedy_selection(current_student_id)
          
          print(f"  All eligible MCQs: {len(all_eligible)}")
          print(f"  Greedy eligible MCQs: {len(greedy_eligible)}")
          
          if len(all_eligible) > 0:
              print(f"  Sample eligible MCQ: {all_eligible[0]}")
          
          if len(greedy_eligible) > 0:
              print(f"  Sample greedy eligible MCQ: {greedy_eligible[0]}")
              
              # SUCCESS - select an MCQ
              mcq_id = greedy_eligible[0]
              mcq = kg.mcqs[mcq_id]
              topic_name = kg.get_topic_of_index(mcq.main_topic_index)
              current_mastery = student.get_mastery(mcq.main_topic_index)
              
              mcq_data = {
                  "success": True,
                  "mcq_id": mcq_id,
                  "text": mcq.text,
                  "options": mcq.options,
                  "correct_index": mcq.correctindex,
                  "explanations": mcq.option_explanations,
                  "topic_name": topic_name,
                  "current_mastery": current_mastery,
                  "difficulty": getattr(mcq, 'difficulty', 0.5)
              }
              
              result_json = json.dumps(mcq_data)
          else:
              # FAILURE - no eligible MCQs
              result_json = json.dumps({
                  "success": False,
                  "error": "No eligible MCQs found after detailed analysis",
                  "debug_info": {
                      "total_mcqs": len(kg.mcqs),
                      "student_topics": len(student.studied_topics),
                      "due_topics": len(due_topics),
                      "mastery_threshold": mastery_threshold,
                      "all_eligible": len(all_eligible),
                      "greedy_eligible": len(greedy_eligible)
                  }
              })

      except Exception as e:
          print(f"ERROR in MCQ generation: {e}")
          import traceback
          traceback.print_exc()
          result_json = json.dumps({"success": False, "error": f"Python error: {str(e)}"})

      # Return the result
      result_json
      `);

          // Debug: Show what we actually got back
          console.log("Raw Python result:", result);
          console.log("Type of result:", typeof result);
          updateOutput(`Python returned: ${result ? result.substring(0, 200) : 'undefined result'}...`);
          
          if (!result) {
            throw new Error("Python code returned undefined");
          }
          
          const data = JSON.parse(result);
          
          if (data.success) {
            currentMCQ = data;
            displayMCQ(data);
            updateStatus('❓ Question ready! Select your answer.', 'info');
          } else {
            updateStatus(`❌ ${data.error}`, 'error');
            if (data.debug) {
              updateOutput(`Debug info: ${data.debug}`);
            }
          }
          
        } catch (error) {
          updateStatus('❌ Failed to generate MCQ', 'error');
          updateOutput(`Error: ${error.message}`);
          updateOutput(`Raw result: ${typeof result !== 'undefined' ? result.substring(0, 500) : 'undefined'}`);
          console.error('MCQ generation error:', error);
        }
      }
      
      function displayMCQ(mcqData) {
      const mcqSection = document.getElementById('mcq-section');
      mcqSection.style.display = 'block';
      
      mcqSection.innerHTML = `
        <div class="mcq-container">
          <div class="mcq-question">${mcqData.text}</div>
          <p><strong>Topic:</strong> ${mcqData.topic_name}</p>
          <p><strong>Current Mastery:</strong> ${(mcqData.current_mastery * 100).toFixed(1)}% | <strong>Difficulty:</strong> ${(mcqData.difficulty * 100).toFixed(1)}%</p>
          
          <div class="mcq-options">
            ${mcqData.options.map((option, index) => 
              `<button class="mcq-option" onclick="selectOption(${index})">${option}</button>`
            ).join('')}
          </div>
          
          <button onclick="submitAnswer()" style="margin-top: 15px; padding: 10px 20px; background: #28a745; color: white; border: none; border-radius: 5px;" disabled id="submitBtn">Submit Answer</button>
        </div>
      `;
      
      // Re-render MathJax for the new content
      if (window.MathJax) {
        MathJax.typesetPromise([mcqSection]).catch((err) => console.log('MathJax render error:', err));
      }
    }

      
      function selectOption(index) {
        // Remove previous selection
        document.querySelectorAll('.mcq-option').forEach(btn => btn.classList.remove('selected'));
        
        // Add selection to clicked option
        document.querySelectorAll('.mcq-option')[index].classList.add('selected');
        
        selectedOption = index;
        document.getElementById('submitBtn').disabled = false;
      }
      
      async function submitAnswer() {
        if (selectedOption === null || !currentMCQ) return;
        
        try {
          updateStatus('🔄 Processing answer and updating knowledge...', 'info');
          
          const result = await pyodideInstance.runPythonAsync(`
            # Process the student's answer using Caoimhe's BKT system
            mcq_id = "${currentMCQ.mcq_id}"
            selected_option = ${selectedOption}
            correct_index = ${currentMCQ.correct_index}
            is_correct = selected_option == correct_index
            
            # Record the attempt and get BKT updates
            bkt_updates = student_manager.record_attempt(
                current_student_id, mcq_id, is_correct, 30.0, kg
            )
            
            # Get the MCQ and student for response
            mcq = kg.mcqs[mcq_id]
            student = student_manager.get_student(current_student_id)
            topic_name = kg.get_topic_of_index(mcq.main_topic_index)
            
            # Calculate mastery change
            mastery_before = None
            mastery_after = student.get_mastery(mcq.main_topic_index)
            mastery_change = 0
            
            if bkt_updates:
                primary_update = next((u for u in bkt_updates if u.get('is_primary_topic', False)), None)
                if primary_update:
                    mastery_before = primary_update['mastery_before']
                    mastery_change = primary_update['mastery_change']
            
            response_data = {
                "is_correct": is_correct,
                "selected_text": mcq.options[selected_option],
                "correct_option": mcq.options[correct_index],
                "explanation": mcq.option_explanations[selected_option],
                "main_topic": topic_name,
                "before_mastery": mastery_before or mastery_after,
                "after_mastery": mastery_after,
                "mastery_change": mastery_change,
                "total_changes": len(bkt_updates)
            }
            
            js_export(response_data)
          `);
          
          const data = JSON.parse(result);
          displayResult(data);
          
          // Reset for next question
          selectedOption = null;
          currentMCQ = null;
          
        } catch (error) {
          updateStatus('❌ Failed to process answer', 'error');
          updateOutput(`Error: ${error.message}`);
          console.error('Answer processing error:', error);
        }
      }
      
      function displayResult(result) {
      const mcqSection = document.getElementById('mcq-section');
      const isCorrect = result.is_correct;
      const borderColor = isCorrect ? '#28a745' : '#dc3545';
      const bgColor = isCorrect ? '#d4edda' : '#f8d7da';
      const textColor = isCorrect ? '#155724' : '#721c24';
      const icon = isCorrect ? '✅' : '❌';
      const changeIcon = result.mastery_change > 0 ? '📈' : result.mastery_change < 0 ? '📉' : '➖';
      
      mcqSection.innerHTML = `
        <div class="mcq-container" style="border-color: ${borderColor}; background-color: ${bgColor}; color: ${textColor};">
          <h3>${icon} ${isCorrect ? 'Correct!' : 'Incorrect'}</h3>
          <p><strong>Your Answer:</strong> ${result.selected_text}</p>
          <p><strong>Correct Answer:</strong> ${result.correct_option}</p>
          <p><strong>Explanation:</strong> ${result.explanation}</p>
          
          <div style="background: white; padding: 15px; margin: 10px 0; border-radius: 5px; color: black;">
            <h4>🧠 BKT Mastery Update</h4>
            <p><strong>Topic:</strong> ${result.main_topic}</p>
            <p><strong>Before:</strong> ${(result.before_mastery * 100).toFixed(1)}%</p>
            <p><strong>After:</strong> ${(result.after_mastery * 100).toFixed(1)}%</p>
            <p><strong>Change:</strong> ${changeIcon} ${result.mastery_change > 0 ? '+' : ''}${(result.mastery_change * 100).toFixed(2)}%</p>
            <p><strong>Total Topics Updated:</strong> ${result.total_changes}</p>
            
            <div class="progress-bar" style="margin: 10px 0;">
              <div class="progress-fill" style="width: ${result.after_mastery * 100}%; background-color: ${result.after_mastery > result.before_mastery ? '#28a745' : '#ffc107'};"></div>
            </div>
          </div>
          
          <button onclick="generateMCQ()" style="margin-top: 15px; padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px;">Next Question</button>
        </div>
      `;
      
      // Re-render MathJax for the new content
      if (window.MathJax) {
        MathJax.typesetPromise([mcqSection]).catch((err) => console.log('MathJax render error:', err));
      }
      
      updateStatus(isCorrect ? '✅ Correct! Knowledge updated.' : '❌ Incorrect, but you still learned!', isCorrect ? 'success' : 'error');
    }
          
      async function showKnowledgeGraph() {
        try {
          updateStatus('📊 Generating knowledge graph...', 'info');
          
          const result = await pyodideInstance.runPythonAsync(`
            # Get current student mastery levels
            student = student_manager.get_student(current_student_id)
            
            graph_info = "Knowledge Graph Summary:\\n"
            graph_info += f"Total topics: {len(kg.nodes)}\\n"
            graph_info += f"Total connections: {len(kg.graph.edges())}\\n\\n"
            graph_info += "Topic Mastery Levels:\\n"
            
            for topic_idx in sorted(student.mastery_levels.keys()):
                topic_name = kg.get_topic_of_index(topic_idx)
                mastery = student.get_mastery(topic_idx)
                level = "🟢" if mastery > 0.6 else "🟡" if mastery > 0.3 else "🔴"
                graph_info += f"{level} {topic_name}: {mastery:.2f}\\n"
            
            js_export({"success": True, "info": graph_info})
          `);
          
          const data = JSON.parse(result);
          updateStatus('✅ Knowledge graph information displayed below.', 'success');
          updateOutput(data.info);
          
        } catch (error) {
          updateStatus('❌ Failed to show knowledge graph', 'error');
          updateOutput(`Error: ${error.message}`);
          console.error('Graph visualization error:', error);
        }
      }
      
      async function skipQuestion() {
        updateStatus('⏭️ Question skipped. Generate a new one!', 'info');
        document.getElementById('mcq-section').style.display = 'none';
        selectedOption = null;
        currentMCQ = null;
      }
      
      function resetDemo() {
        updateStatus('🔄 Demo reset. Click Initialize to start over.', 'info');
        document.getElementById('output').textContent = '';
        document.getElementById('mcq-section').style.display = 'none';
        
        // Reset buttons
        document.getElementById('createStudentBtn').disabled = true;
        document.getElementById('generateMCQBtn').disabled = true;
        document.getElementById('showGraphBtn').disabled = true;
        
        // Reset variables
        currentStudent = null;
        currentMCQ = null;
        selectedOption = null;
      }
    </script>

</body>
</html>