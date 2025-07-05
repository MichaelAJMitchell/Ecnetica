
  # BKT Simple Demo

  ```{raw} html

  <!doctype html>
  <html>
    <head>
      <title>BKT Algorithm Visual Demo</title>
      <script src="https://cdn.jsdelivr.net/pyodide/v0.27.7/full/pyodide.js"></script>
      <style>
        body {
          font-family: Arial, sans-serif;
          max-width: 1200px;
          margin: 0 auto;
          padding: 20px;
          background-color: #f5f5f5;
        }
        .container {
          background: white;
          padding: 20px;
          border-radius: 10px;
          box-shadow: 0 2px 10px rgba(0,0,0,0.1);
          margin-bottom: 20px;
        }
        .controls {
          display: flex;
          gap: 10px;
          margin: 20px 0;
          flex-wrap: wrap;
        }
        button {
          padding: 12px 20px;
          font-size: 16px;
          border: none;
          border-radius: 5px;
          cursor: pointer;
          transition: background-color 0.3s;
        }
        .primary-btn {
          background-color: #2196F3;
          color: white;
        }
        .primary-btn:hover {
          background-color: #1976D2;
        }
        .success-btn {
          background-color: #4CAF50;
          color: white;
        }
        .success-btn:hover {
          background-color: #45a049;
        }
        .danger-btn {
          background-color: #f44336;
          color: white;
        }
        .danger-btn:hover {
          background-color: #da190b;
        }
        #output {
          background-color: #f8f9fa;
          border: 1px solid #dee2e6;
          border-radius: 5px;
          padding: 15px;
          margin: 15px 0;
          min-height: 100px;
          font-family: monospace;
          white-space: pre-wrap;
          overflow-x: auto;
        }
        .status {
          padding: 10px;
          border-radius: 5px;
          margin: 10px 0;
        }
        .status.success {
          background-color: #d4edda;
          color: #155724;
          border: 1px solid #c3e6cb;
        }
        .status.error {
          background-color: #f8d7da;
          color: #721c24;
          border: 1px solid #f5c6cb;
        }
        .status.info {
          background-color: #d1ecf1;
          color: #0c5460;
          border: 1px solid #bee5eb;
        }
        .mcq-container {
          background-color: #fff;
          border: 2px solid #007bff;
          border-radius: 8px;
          padding: 20px;
          margin: 15px 0;
        }
        .mcq-question {
          font-size: 18px;
          font-weight: bold;
          margin-bottom: 15px;
          color: #333;
        }
        .mcq-options {
          margin: 15px 0;
        }
        .mcq-option {
          display: block;
          margin: 8px 0;
          padding: 10px;
          background-color: #f8f9fa;
          border: 2px solid #e9ecef;
          border-radius: 5px;
          cursor: pointer;
          transition: all 0.3s;
        }
        .mcq-option:hover {
          background-color: #e9ecef;
          border-color: #007bff;
        }
        .mcq-option.selected {
          background-color: #007bff;
          color: white;
          border-color: #0056b3;
        }
        .progress-bar {
          width: 100%;
          height: 20px;
          background-color: #e9ecef;
          border-radius: 10px;
          overflow: hidden;
          margin: 10px 0;
        }
        .progress-fill {
          height: 100%;
          background-color: #28a745;
          transition: width 0.3s ease;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>🧠 BKT Algorithm Visual Demo</h1>
        <p>This demo shows how Bayesian Knowledge Tracing works with a simple knowledge graph. Students start with low mastery levels and improve through practice.</p>
        
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
                indexURL: "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/",
                packageCacheKey: "bkt-demo-v1", // This enables persistent caching
                loadPackages: false // Don't auto-load, we'll do it manually with cache check
              });
              
              updateOutput('✓ Pyodide loaded successfully');
              
              // Check what's already cached and only load missing packages
              updateOutput('Checking package cache...');
              
              const packages = ["numpy", "networkx", "matplotlib"];
              await pyodideInstance.loadPackage(packages, {
                messageCallback: (msg) => console.log(`Package loading: ${msg}`),
                errorCallback: (err) => console.error(`Package error: ${err}`)
              });
              
              updateOutput('✓ All packages loaded');
            }

            
            // Fetch and load the BKT code
            updateOutput('Fetching BKT algorithm code...');
            const response = await fetch("../../_static/mcq_algorithm_full_python.py");
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const code = await response.text();
            pyodideInstance.FS.writeFile("bkt_system.py", code);
            updateOutput('✓ BKT code loaded');
            
            // Import and initialize the system
            await pyodideInstance.runPythonAsync(`
              import sys
              sys.path.append('.')
              import bkt_system
              
              # Create a simple knowledge graph for demo
              print("Creating demo knowledge graph...")
              
              # Create a clean knowledge graph without loading from files
              kg = bkt_system.KnowledgeGraph()
              
              # Clear any existing data to start fresh
              kg.nodes = {}
              kg.topic_to_index = {}
              kg._next_index = 0
              kg.mcqs = {}
              
              print("Starting with clean knowledge graph")
              
              # Add ONLY our demo topics
              topic_0 = kg.add_node("Basic Arithmetic", "Foundation", [])
              topic_1 = kg.add_node("Linear Equations", "Algebra", [(topic_0, 1.0)])
              topic_2 = kg.add_node("Quadratic Equations", "Algebra", [(topic_1, 0.8)])
              topic_3 = kg.add_node("Functions", "Algebra", [(topic_1, 0.6)])
              topic_4 = kg.add_node("Trigonometry", "Advanced", [(topic_2, 0.7), (topic_3, 0.5)])
              
              print(f"Knowledge graph created with {len(kg.nodes)} topics")
              print(f"Topic indices: {list(kg.nodes.keys())}")
              for idx, node in kg.nodes.items():
                  print(f"  {idx}: {node.topic}")
              
              # Create some sample MCQs
              mcqs = []
              
              # MCQ for Basic Arithmetic (topic 0)
              mcqs.append(kg.create_mcqs(
                  text='What is 15 + 7?',
                  options=['20', '22', '23', '21'],
                  correctindex=1,
                  option_explanations=[
                      'This would be 15 + 5. Remember to add all digits carefully.',
                      'Correct! 15 + 7 = 22. Well done on this basic arithmetic.',
                      'This would be 15 + 8. Double-check your addition.',
                      'This would be 15 + 6. Make sure to add the correct numbers.'
                  ],
                  main_topic_index=0,
                  subtopic_weights={0: 1.0},
                  conceptual=0.2, procedural=0.8, problem_solving=0.1, communication=0.1, memory=0.3, spatial=0.0
              ))
              
              # MCQ for Linear Equations (topic 1)
              mcqs.append(kg.create_mcqs(
                  text='Solve for x: 2x + 5 = 13',
                  options=['x = 3', 'x = 4', 'x = 6', 'x = 9'],
                  correctindex=1,
                  option_explanations=[
                      'Check your algebra: 2(3) + 5 = 11, not 13.',
                      'Correct! 2x = 13 - 5 = 8, so x = 4.',
                      'This gives 2(6) + 5 = 17, which is too large.',
                      'This gives 2(9) + 5 = 23, which is much too large.'
                  ],
                  main_topic_index=1,
                  subtopic_weights={1: 0.9, 0: 0.1},
                  conceptual=0.3, procedural=0.7, problem_solving=0.4, communication=0.2, memory=0.2, spatial=0.0
              ))
              
              # MCQ for Quadratic Equations (topic 2)
              mcqs.append(kg.create_mcqs(
                  text='What is the discriminant of x² - 5x + 6 = 0?',
                  options=['1', '4', '25', '11'],
                  correctindex=0,
                  option_explanations=[
                      'Correct! Using b² - 4ac: (-5)² - 4(1)(6) = 25 - 24 = 1.',
                      'This would be 2². Remember the discriminant formula is b² - 4ac.',
                      'This is b² only. Don\\'t forget to subtract 4ac.',
                      'Check your calculation of 4ac. It should be 4(1)(6) = 24.'
                  ],
                  main_topic_index=2,
                  subtopic_weights={2: 0.8, 1: 0.2},
                  conceptual=0.5, procedural=0.6, problem_solving=0.3, communication=0.2, memory=0.4, spatial=0.0
              ))
              
              # MCQ for Functions (topic 3)
              mcqs.append(kg.create_mcqs(
                  text='If f(x) = 2x + 3, what is f(5)?',
                  options=['10', '13', '8', '15'],
                  correctindex=1,
                  option_explanations=[
                      'This would be 2×5 = 10, but you forgot to add 3.',
                      'Correct! f(5) = 2(5) + 3 = 10 + 3 = 13.',
                      'This seems to be 5 + 3, but you forgot to multiply by 2 first.',
                      'This might be 3×5, but the function is 2x + 3, not 3x.'
                  ],
                  main_topic_index=3,
                  subtopic_weights={3: 1.0},
                  conceptual=0.4, procedural=0.6, problem_solving=0.2, communication=0.3, memory=0.3, spatial=0.0
              ))
              
              # MCQ for Trigonometry (topic 4)  
              mcqs.append(kg.create_mcqs(
                  text='What is sin(90°)?',
                  options=['0', '1', '0.5', 'undefined'],
                  correctindex=1,
                  option_explanations=[
                      'This is sin(0°). Remember that sin(90°) represents the y-coordinate at the top of the unit circle.',
                      'Correct! sin(90°) = 1. At 90°, we are at the top of the unit circle where y = 1.',
                      'This is sin(30°). The sine of 90° is at the maximum value of the sine function.',
                      'Sine is defined for all angles. You might be thinking of tan(90°).'
                  ],
                  main_topic_index=4,
                  subtopic_weights={4: 0.8, 2: 0.2},
                  conceptual=0.3, procedural=0.4, problem_solving=0.1, communication=0.4, memory=0.5, spatial=0.2
              ))
              
              print(f"Created {len(mcqs)} sample MCQs")
              
              # CRITICAL DEBUG: Check if MCQs are actually stored in kg.mcqs
              print(f"MCQs stored in kg.mcqs: {len(kg.mcqs)}")
              print(f"kg.mcqs keys: {list(kg.mcqs.keys())}")
              
              # Debug each created MCQ
              for i, mcq in enumerate(mcqs):
                  print(f"MCQ {i}: ID={mcq.id}, topic={mcq.main_topic_index}, text='{mcq.text[:30]}...'")
                  print(f"  Stored in kg.mcqs? {mcq.id in kg.mcqs}")
              
              # Check if kg.mcqs is empty - if so, the MCQs weren't stored properly
              if len(kg.mcqs) == 0:
                  print("ERROR: kg.mcqs is empty! MCQs were not stored in knowledge graph.")
                  print("Manually adding MCQs to kg.mcqs...")
                  for mcq in mcqs:
                      kg.mcqs[mcq.id] = mcq
                  print(f"After manual addition: kg.mcqs has {len(kg.mcqs)} MCQs")
              
              # Initialize student manager
              student_manager = bkt_system.StudentManager()
              
              # Initialize BKT with required parameters
              bkt = bkt_system.BayesianKnowledgeTracing(kg, student_manager)
              
              # Initialize MCQ scheduler (should have done this from the start!)
              mcq_scheduler = bkt_system.MCQScheduler(kg, student_manager)
              mcq_scheduler.set_bkt_system(bkt)
              
              # Store everything globally for access
              globals()['kg'] = kg
              globals()['mcqs'] = mcqs
              globals()['student_manager'] = student_manager
              globals()['bkt'] = bkt
              globals()['mcq_scheduler'] = mcq_scheduler
              
              print("BKT system initialized successfully!")
            `);
            
            updateStatus('✅ BKT System Ready! Create a student to begin.', 'success');
            document.getElementById('createStudentBtn').disabled = false;
            updateOutput('✓ BKT system initialized successfully!');
            
          } catch (error) {
            updateStatus('❌ Failed to initialize BKT system', 'error');
            updateOutput(`Error: ${error.message}`);
            console.error('Initialization error:', error);
          }
        }
        
        async function createStudent() {
          try {
            updateStatus('👤 Creating student with low initial masteries...', 'info');
            
            const result = pyodideInstance.runPython(`
              import random
              random.seed(42)  # For reproducible results
              
              # Create student with low initial masteries (0.1 to 0.3)
              student_id = "demo_student_001"
              
              # Create the student first
              student = student_manager.create_student(student_id)
              
              # Then set initial masteries manually for ONLY our 5 topics
              for topic_index in kg.nodes.keys():
                  # Low initial mastery between 0.1 and 0.3
                  mastery = random.uniform(0.1, 0.3)
                  student.mastery_levels[topic_index] = mastery
                  # Also set as studied and initialize confidence
                  student.studied_topics[topic_index] = True
                  student.confidence_levels[topic_index] = 0.5
              
              print(f"Created student: {student_id}")
              print("Initial mastery levels:")
              for topic_index, mastery in student.mastery_levels.items():
                  topic_name = kg.nodes[topic_index].topic
                  print(f"  {topic_name}: {mastery:.3f}")
              
              # Store current student
              globals()['current_student_id'] = student_id
              
              f"Student {student_id} created successfully"
            `);
            
            currentStudent = pyodideInstance.globals.get('current_student_id');
            updateStatus('✅ Student created! Generate an MCQ to start learning.', 'success');
            document.getElementById('generateMCQBtn').disabled = false;
            document.getElementById('showGraphBtn').disabled = false;
            updateOutput(result);
            
          } catch (error) {
            updateStatus('❌ Failed to create student', 'error');
            updateOutput(`Error: ${error.message}`);
            console.error('Student creation error:', error);
          }
        }
        
        async function generateMCQ() {
          try {
            updateStatus('❓ Generating MCQ based on student mastery...', 'info');
            
            // Execute Python code to generate MCQ
            pyodideInstance.runPython(`
              print("=== DEBUGGING MCQ GENERATION ===")
              
              # Get student and check data
              student = student_manager.get_student(current_student_id)
              print(f"Student found: {student is not None}")
              print(f"Student masteries: {student.mastery_levels}")
              print(f"MCQs in kg.mcqs: {len(kg.mcqs)}")
              
              # List all available MCQs with their topics
              print("\\n=== ALL AVAILABLE MCQs ===")
              for i, (mcq_id, mcq) in enumerate(kg.mcqs.items()):
                  print(f"MCQ {i}: ID={mcq_id[:8]}, topic={mcq.main_topic_index}, text='{mcq.text[:30]}...'")
              
              # Find lowest mastery topic
              print("\\n=== FINDING LOWEST MASTERY ===")
              if student.mastery_levels:
                  lowest_mastery = min(student.mastery_levels.values())
                  print(f"Lowest mastery value: {lowest_mastery}")
                  
                  lowest_topic = None
                  for topic_idx, mastery in student.mastery_levels.items():
                      print(f"  Topic {topic_idx}: mastery {mastery}")
                      if mastery == lowest_mastery:
                          lowest_topic = topic_idx
                          print(f"  -> This is the lowest! Setting target to {topic_idx}")
                          break
                  
                  print(f"Target topic: {lowest_topic}")
                  
                  # Try to find MCQ for this topic
                  print("\\n=== SEARCHING FOR MCQ ===")
                  target_mcq = None
                  for mcq_id, mcq in kg.mcqs.items():
                      print(f"Checking MCQ {mcq_id[:8]} - has topic {mcq.main_topic_index}, want topic {lowest_topic}")
                      if mcq.main_topic_index == lowest_topic:
                          target_mcq = mcq
                          print(f"  *** MATCH FOUND! ***")
                          break
                      else:
                          print(f"  No match: {mcq.main_topic_index} != {lowest_topic}")
                  
                  if target_mcq:
                      print(f"\\n=== CREATING RESULT ===")
                      topic_name = kg.nodes[target_mcq.main_topic_index].topic
                      print(f"Topic name: {topic_name}")
                      
                      # Store current MCQ
                      globals()['current_mcq'] = target_mcq
                      
                      result_dict = {
                          'text': str(target_mcq.text),
                          'options': list(target_mcq.options),
                          'topic': str(topic_name),
                          'mastery': float(lowest_mastery),
                          'correct_index': int(target_mcq.correctindex)
                      }
                      print(f"SUCCESS! Result: {result_dict}")
                      
                      # STORE IN GLOBALS FOR JAVASCRIPT TO ACCESS
                      globals()['mcq_result'] = result_dict
                      
                  else:
                      print("\\n=== NO MCQ FOUND - USING FALLBACK ===")
                      # Just use the first MCQ as fallback
                      first_mcq = list(kg.mcqs.values())[0]
                      topic_name = kg.nodes[first_mcq.main_topic_index].topic
                      mastery = student.mastery_levels.get(first_mcq.main_topic_index, 0.2)
                      
                      globals()['current_mcq'] = first_mcq
                      
                      result_dict = {
                          'text': str(first_mcq.text),
                          'options': list(first_mcq.options),
                          'topic': str(topic_name),
                          'mastery': float(mastery),
                          'correct_index': int(first_mcq.correctindex)
                      }
                      print(f"FALLBACK! Result: {result_dict}")
                      globals()['mcq_result'] = result_dict
              else:
                  print("ERROR: Student has no masteries!")
                  # Emergency fallback
                  first_mcq = list(kg.mcqs.values())[0]
                  result_dict = {
                      'text': str(first_mcq.text),
                      'options': list(first_mcq.options),
                      'topic': 'Emergency Test',
                      'mastery': 0.1,
                      'correct_index': int(first_mcq.correctindex)
                  }
                  print(f"EMERGENCY! Result: {result_dict}")
                  globals()['mcq_result'] = result_dict
            `);
            
            // Get the result from Python globals
            const mcqData = pyodideInstance.globals.get('mcq_result');
            updateOutput('Python execution completed');
            
            updateOutput('Python execution completed');
            
            if (mcqData && typeof mcqData === 'object' && mcqData.text) {
              currentMCQ = mcqData;
              displayMCQ(mcqData);
              updateStatus('📚 MCQ ready! Select your answer.', 'info');
            } else {
              updateStatus('❌ No suitable MCQ found', 'error');
              updateOutput(`MCQ data received: ${JSON.stringify(mcqData)}`);
            }
            
          } catch (error) {
            updateStatus('❌ Failed to generate MCQ', 'error');
            updateOutput(`Error: ${error.message}`);
            console.error('MCQ generation error:', error);
          }
        }
        
        function displayMCQ(mcqData) {
          const mcqSection = document.getElementById('mcq-section');
          mcqSection.style.display = 'block';
          
          mcqSection.innerHTML = `
            <div class="mcq-container">
              <div class="mcq-question">
                📖 Topic: ${mcqData.topic} (Current Mastery: ${(mcqData.mastery * 100).toFixed(1)}%)
                <div class="progress-bar">
                  <div class="progress-fill" style="width: ${mcqData.mastery * 100}%"></div>
                </div>
                <br><strong>Question:</strong> ${mcqData.text}
              </div>
              <div class="mcq-options">
                ${mcqData.options.map((option, index) => 
                  `<label class="mcq-option" onclick="selectOption(${index})">
                    <input type="radio" name="mcq-answer" value="${index}" style="margin-right: 10px;">
                    ${String.fromCharCode(65 + index)}. ${option}
                  </label>`
                ).join('')}
              </div>
              <div class="controls">
                <button onclick="submitAnswer()" class="success-btn" id="submitBtn" disabled>✅ Submit Answer</button>
                <button onclick="skipQuestion()" class="danger-btn">⏭️ Skip Question</button>
              </div>
            </div>
          `;
        }
        
        function selectOption(index) {
          selectedOption = index;
          
          // Update visual selection
          const options = document.querySelectorAll('.mcq-option');
          options.forEach((option, i) => {
            option.classList.toggle('selected', i === index);
            const radio = option.querySelector('input[type="radio"]');
            radio.checked = (i === index);
          });
          
          document.getElementById('submitBtn').disabled = false;
        }
        
        async function submitAnswer() {
          if (selectedOption === null) return;
          
          try {
            updateStatus('🔄 Processing answer and updating mastery with BKT...', 'info');
            
            const result = pyodideInstance.runPython(`
              print("=== PROCESSING ANSWER ===")
              
              # Get the MCQ and student response
              mcq = current_mcq
              student_choice = ${selectedOption}
              is_correct = (student_choice == mcq.correctindex)
              
              print(f"Student selected option {student_choice}: {'CORRECT' if is_correct else 'INCORRECT'}")
              print(f"Correct answer was option {mcq.correctindex}")
              
              # Get mastery BEFORE BKT update
              student = student_manager.get_student(current_student_id)
              before_masteries = dict(student.mastery_levels)
              main_topic = mcq.main_topic_index
              topic_name = kg.nodes[main_topic].topic
              
              print(f"\\nBEFORE BKT UPDATE:")
              print(f"  {topic_name} (topic {main_topic}): {before_masteries[main_topic]:.4f}")
              
              # Use the proper BKT workflow via student_manager.record_attempt
              print(f"\\nApplying BKT update...")
              try:
                  bkt_updates = student_manager.record_attempt(
                      current_student_id, 
                      mcq.id, 
                      is_correct, 
                      5.0,  # simulated time
                      kg
                  )
                  print(f"BKT update successful: {len(bkt_updates) if bkt_updates else 0} updates")
              except Exception as e:
                  print(f"record_attempt failed: {e}")
                  # Fallback to direct BKT
                  attempt = bkt_system.StudentAttempt(
                      student_id=current_student_id,
                      mcq_id=mcq.id,
                      selected_option=student_choice,
                      is_correct=is_correct,
                      time_taken=5.0
                  )
                  bkt_updates = bkt.update_mastery_bkt(kg, student, mcq, attempt)
                  print(f"Direct BKT fallback: {len(bkt_updates) if bkt_updates else 0} updates")
              
              # Get mastery AFTER BKT update
              after_masteries = dict(student.mastery_levels)
              
              print(f"\\nAFTER BKT UPDATE:")
              print(f"  {topic_name} (topic {main_topic}): {after_masteries[main_topic]:.4f}")
              
              # Calculate the change
              main_change = after_masteries[main_topic] - before_masteries[main_topic]
              print(f"\\nMASTERY CHANGE:")
              print(f"  {topic_name}: {main_change:+.4f}")
              
              # Show all mastery changes
              print(f"\\nALL MASTERY CHANGES:")
              total_changes = 0
              for topic_idx in kg.nodes.keys():
                  topic_name_all = kg.nodes[topic_idx].topic
                  before = before_masteries[topic_idx]
                  after = after_masteries[topic_idx]
                  change = after - before
                  if abs(change) > 0.0001:  # Only show significant changes
                      direction = "↗️" if change > 0 else "↘️"
                      print(f"  {direction} {topic_name_all}: {before:.4f} → {after:.4f} ({change:+.4f})")
                      total_changes += 1
              
              if total_changes == 0:
                  print("  No significant changes detected")
              
              # Store results for JavaScript
              globals()['answer_result'] = {
                  'correct': is_correct,
                  'explanation': mcq.option_explanations[student_choice],
                  'correct_option': mcq.options[mcq.correctindex],
                  'selected_text': mcq.options[student_choice],
                  'main_topic': topic_name,
                  'before_mastery': float(before_masteries[main_topic]),
                  'after_mastery': float(after_masteries[main_topic]),
                  'mastery_change': float(main_change),
                  'total_changes': total_changes
              }
              
              print("\\nAnswer processing complete!")
              "Success"
            `);
            
            // Get the result
            const answerResult = pyodideInstance.globals.get('answer_result');
            
            // Display results
            displayAnswerFeedback(answerResult);
            updateStatus('✅ Answer processed! BKT mastery updated.', 'success');
            
            // Reset for next question
            selectedOption = null;
            currentMCQ = null;
            
          } catch (error) {
            updateStatus('❌ Failed to process answer', 'error');
            updateOutput(`Error: ${error.message}`);
            console.error('Answer processing error:', error);
          }
        }
        
        function displayAnswerFeedback(result) {
          const mcqSection = document.getElementById('mcq-section');
          const isCorrect = result.correct;
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
                  <div class="progress-fill" style="width: ${result.after_mastery * 100}%; background-color: ${result.after_mastery > result.before_mastery ? '#28a745' : '#dc3545'}"></div>
                </div>
              </div>
              
              <div class="controls">
                <button onclick="generateMCQ()" class="primary-btn">📚 Next Question</button>
                <button onclick="showKnowledgeGraph()" class="primary-btn">📊 View All Masteries</button>
              </div>
            </div>
          `;
        }
        
        async function showKnowledgeGraph() {
          try {
            updateStatus('📊 Generating knowledge graph visualization...', 'info');
            
            const graphInfo = pyodideInstance.runPython(`
              import matplotlib.pyplot as plt
              import numpy as np
              
              # Get current student
              student = student_manager.get_student(current_student_id)
              
              # Create a simple text-based representation
              print("Current Knowledge Graph State:")
              print("=" * 50)
              
              for topic_idx in sorted(kg.nodes.keys()):
                  node = kg.nodes[topic_idx]
                  mastery = student.mastery_levels[topic_idx]
                  
                  # Create progress bar
                  bar_length = 20
                  filled_length = int(bar_length * mastery)
                  bar = "█" * filled_length + "░" * (bar_length - filled_length)
                  
                  # Color coding
                  if mastery < 0.3:
                      status = "🔴 Needs Work"
                  elif mastery < 0.6:
                      status = "🟡 Developing"
                  elif mastery < 0.8:
                      status = "🟢 Good"
                  else:
                      status = "⭐ Mastered"
                  
                  print(f"{node.topic:20} [{bar}] {mastery:5.1%} {status}")
                  
                  # Show dependencies
                  if node.dependencies:
                      dep_names = [kg.nodes[dep_idx].topic for dep_idx, _ in node.dependencies]
                      print(f"{'':20} ↳ Depends on: {', '.join(dep_names)}")
                  print()
              
              "Graph visualization complete"
            `);
            
            updateStatus('📊 Knowledge graph displayed in output', 'success');
            updateOutput(graphInfo);
            
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