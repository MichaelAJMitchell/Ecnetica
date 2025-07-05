
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
            pyodideInstance = await loadPyodide();
            updateOutput('✓ Pyodide loaded successfully');
            
            // Load required packages
            updateOutput('Loading packages: numpy, networkx, matplotlib...');
            await pyodideInstance.loadPackage(["numpy", "networkx", "matplotlib"]);
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
          updateOutput('✓ BKT system initialized with Caoimhe\'s algorithms!');
          
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

print("=== DEBUG: Starting MCQ generation ===")

try:
    # Check if we have MCQs loaded
    print(f"Total MCQs in kg.mcqs: {len(kg.mcqs)}")
    
    if len(kg.mcqs) == 0:
        print("ERROR: No MCQs found in knowledge graph")
        result_json = json.dumps({"success": False, "error": "No MCQs loaded in knowledge graph"})
    else:
        print("MCQ IDs available:", list(kg.mcqs.keys())[:5])  # Show first 5
        
        # Check student
        student = student_manager.get_student(current_student_id)
        if not student:
            print("ERROR: Student not found")
            result_json = json.dumps({"success": False, "error": "Student not found"})
        else:
            print(f"Student found with {len(student.mastery_levels)} mastery levels")
            
            # Get available MCQs for the student
            print("Getting eligible MCQs...")
            eligible_mcqs = mcq_scheduler.get_eligible_mcqs_for_student(current_student_id)
            print(f"Eligible MCQs: {len(eligible_mcqs)}")
            
            if not eligible_mcqs:
                print("No eligible MCQs - checking why...")
                # Debug why no MCQs are eligible
                all_mcq_ids = list(kg.mcqs.keys())
                print(f"All MCQ IDs: {all_mcq_ids[:3]}")  # Show first 3
                
                if all_mcq_ids:
                    test_mcq = kg.mcqs[all_mcq_ids[0]]
                    print(f"Test MCQ main topic: {test_mcq.main_topic_index}")
                    print(f"Student studied topics: {list(student.studied_topics.keys())[:5]}")
                
                result_json = json.dumps({
                    "success": False, 
                    "error": "No eligible MCQs found", 
                    "debug": f"Total MCQs: {len(kg.mcqs)}, Student topics: {len(student.studied_topics)}"
                })
            else:
                print(f"Found {len(eligible_mcqs)} eligible MCQs")
                
                # Try simple selection first - just pick the first eligible MCQ
                mcq_id = eligible_mcqs[0]
                mcq = kg.mcqs[mcq_id]
                print(f"Selected MCQ: {mcq_id}")
                
                # Get student context
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
                    "difficulty": getattr(mcq, 'difficulty', 0.5)  # Safe access
                }
                
                print("MCQ data prepared successfully")
                result_json = json.dumps(mcq_data)

except Exception as e:
    print(f"ERROR in MCQ generation: {e}")
    import traceback
    traceback.print_exc()
    result_json = json.dumps({"success": False, "error": f"Python error: {str(e)}"})

# This is the return value
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