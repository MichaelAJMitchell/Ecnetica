# Bayesian Knowledge Tracing FSRS Demo

```{raw} html

<!doctype html>
<html>
<head>
    <title>Bayesian Knowledge Tracing Algorithm Visual Demo</title>
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
</head>

<body>
    <div class="bkt-demo-container">
      <!-- Time Controls Section - Now at the top -->
      <div class="container">
        <h1>🧠 FSRS Forgetting Curves Demo</h1>
        <p class="subtitle">Watch how memory decays over time and see FSRS in action</p>
        <div id="time-controls">
          <h3>⏰ Time Travel Controls</h3>
          <div class="time-controls-buttons">
            <button onclick="skipTime(1, 0, 0)" class="primary-btn">Skip 1 Day</button>
            <button onclick="skipTime(7, 0, 0)" class="primary-btn">Skip 1 Week</button>
            <button onclick="skipTime(30, 0, 0)" class="primary-btn">Skip 1 Month</button>
            <button onclick="resetTime()" class="danger-btn">Reset Time</button>
          </div>
          
          <div id="time-status"></div>
          
          <div class="custom-time-container">
            <h4>Custom Time Skip:</h4>
            <div class="custom-time-inputs">
              <input type="number" id="custom-days" placeholder="Days" min="0" max="365">
              <input type="number" id="custom-hours" placeholder="Hours" min="0" max="23">
              <button onclick="skipCustomTime()" class="primary-btn">Skip Time</button>
            </div>
          </div>
          
          <div class="time-controls-actions">
            <button onclick="showMasteryDecay()" class="success-btn">📊 Check Mastery Decay</button>
            <button onclick="previewDecay(30)" class="primary-btn">🔮 Preview 30-Day Decay</button>
          </div>
        </div>
      </div>

      <div class="main-layout">
        <!-- Left side: BKT Demo -->
        <div class="bkt-section">
          <div class="container">
            <h1>🎯 Quadratic Equations Practice</h1>
            <p class="subtitle">Focus on one topic to see FSRS forgetting in action</p>
            
            <div id="status" class="status loading">
              <div class="loading-spinner"></div>
              Initializing BKT System...
            </div>
            
            <div id="mcq-section" class="mcq-section-hidden"></div>
          </div>
        </div>

        <!-- Right side: Knowledge Graph -->
        <div class="graph-section">
          <div class="container">
            <h1>📊 Knowledge Graph</h1>
            <p>The graph colors reflect your current mastery levels. Practice questions to see the colors change!</p>
            
            <div class="mastery-legend">
              <strong>Mastery Level Legend:</strong><br>
              <div class="gradient-legend">
                <div class="gradient-bar"></div>
                <div class="gradient-labels">
                  <span>0% (Red)</span>
                  <span>50% (Orange)</span>
                  <span>100% (Green)</span>
                </div>
              </div>
              <div class="legend-item">
                <span class="legend-color legend-color-not-studied"></span>
                <span>Not Yet Studied</span>
              </div>
            </div>
            
            <div style="position: relative;">
              <div id="graph-container"></div>
              <div id="graph-loading" class="graph-loading">
                <div class="graph-loading-spinner"></div>
                <div class="graph-loading-text">Loading Knowledge Graph...</div>
              </div>
            </div>

            <div id="controls">
              <label for="strand-filter">Filter by Strand: </label>
              <select id="strand-filter">
                <option value="">All Strands</option>
                <option value="Algebra">Algebra</option>
                <option value="Geometry">Geometry</option>
                <option value="Trigonometry">Trigonometry</option>
                <option value="Calculus">Calculus</option>
                <option value="Number">Number</option>
                <option value="Statistics">Statistics</option>
                <option value="Probability">Probability</option>
                <option value="Coordinate Geometry">Coordinate Geometry</option>
              </select>
              
              <button id="reset-view">Reset View</button>
              <button id="toggle-physics">Toggle Physics</button>
              <button id="load-simplified">Load Small Dense Graph</button>
              <button id="load-full">Load Full</button>
            </div>

            <div id="node-info">
              <h4 id="node-title"></h4>
              <p id="node-description"></p>
              <p><strong>Strand:</strong> <span id="node-strand"></span></p>
              <p><strong>Mastery Level:</strong> <span id="node-mastery"></span></p>
            </div>

            <div id="stats">
              <strong>Graph Statistics:</strong> <span id="node-count">0</span> nodes, <span id="edge-count">0</span> edges
            </div>
          </div>
        </div>
      </div>
    </div>

    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <script type="text/javascript">
      let pyodideInstance = null;
      let currentStudent = null;
      let currentMCQ = null;
      let selectedOption = null;
      let isInitialized = false;
      let isInitialGraphLoad = false; // Flag to track initial graph load
      
      // Global variables for knowledge graph
      let network;
      let currentData = {nodes: [], edges: []};
      let currentMasteryLevels = {};
      let topicIndexToNodeId = {}; // Maps BKT topic indices to graph node IDs
      
      function updateStatus(message, type = 'info') {
        const statusDiv = document.getElementById('status');
        statusDiv.className = `status ${type}`;
        
        if (type === 'loading') {
          statusDiv.innerHTML = `<div class="loading-spinner"></div>${message}`;
        } else {
          statusDiv.textContent = message;
        }
      }

      // Function to get mastery-based color with smooth gradient
      function getMasteryColor(masteryLevel) {
        if (masteryLevel === null || masteryLevel === undefined) {
          return '#6c757d'; // Gray for not studied
        }
        
        // Ensure masteryLevel is between 0 and 1
        const clampedMastery = Math.max(0, Math.min(1, masteryLevel));
        
        // Map mastery level (0-1) to hue (0-120 degrees)
        // 0 = red (0°), 0.5 = orange/yellow (~40°), 1 = green (120°)
        const hue = clampedMastery * 120;
        
        // Use full saturation and medium lightness for vibrant colors
        return `hsl(${hue}, 80%, 50%)`;
      }

      // Function to update graph colors based on mastery levels
      async function updateGraphMasteryColors() {
        if (!network || !currentStudent || !pyodideInstance) return;
        
        try {
          //applies forgetting
          await pyodideInstance.runPythonAsync(`refresh_student_mastery(current_student_id)`);

          // Get current view position and scale to preserve user's zoom/pan
          const currentView = network.getViewPosition();
          
          // Get current mastery levels from Python
          const masteryResult = await pyodideInstance.runPythonAsync(`
            student = student_manager.get_student(current_student_id)
            mastery_data = {}
            topic_mapping = {}
            
            # Get mastery levels and topic names
            for topic_idx in student.mastery_levels:
                topic_name = kg.get_topic_of_index(topic_idx)
                mastery_level = student.get_mastery(topic_idx)
                mastery_data[topic_name] = mastery_level
                topic_mapping[topic_idx] = topic_name
            
            js_export({
                "mastery_levels": mastery_data,
                "topic_mapping": topic_mapping
            })
          `);
          
          const masteryData = JSON.parse(masteryResult);
          currentMasteryLevels = masteryData.mastery_levels;
          
          // Get current node positions to preserve them
          const positions = network.getPositions();
          
          // Update node colors based on mastery levels while preserving positions
          const updatedNodes = currentData.nodes.map(node => {
            const masteryLevel = currentMasteryLevels[node.label];
            const color = getMasteryColor(masteryLevel);
            
            // Preserve current position if it exists
            const currentPos = positions[node.id];
            
            return {
              ...node,
              // Keep current position
              x: currentPos ? currentPos.x : node.x,
              y: currentPos ? currentPos.y : node.y,
              color: {
                background: color,
                border: '#2B7CE9',
                borderWidth: 0,
                highlight: {
                  background: color,
                  border: '#2B7CE9'
                },
                hover: {
                  background: color,
                  border: '#2B7CE9'
                }
              }
            };
          });
          
          // Update the network with new colors and preserved positions
          network.setData({nodes: updatedNodes, edges: currentData.edges});
          currentData.nodes = updatedNodes;
          
          // Only restore view if this is NOT the initial load
          if (!isInitialGraphLoad) {
            // Wait a bit longer for the network to process the data update
            setTimeout(() => {
              network.moveTo({
                position: currentView.position,
                scale: currentView.scale,
                animation: false // Disable animation to make it instant
              });
            }, 150);
          }
          
          console.log('Graph colors updated based on mastery levels (zoom and position preserved)');
          
        } catch (error) {
          console.error('Error updating graph mastery colors:', error);
        }
      }
      
      // Automated initialization function
      async function autoInitialize() {
        try {
          console.log("🔧 Starting auto-initialization...");
          // Step 1: Initialize Pyodide and BKT System
          updateStatus('Loading Pyodide and packages...', 'loading');
          
          if (!pyodideInstance) {
            pyodideInstance = await loadPyodide({
              indexURL: "../../_static/",
              packageCacheKey: "bkt-demo-v1",
              loadPackages: false
            });
            
            const originalIndexURL = pyodideInstance._api.config.indexURL;
            pyodideInstance._api.config.indexURL = "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/";
            
            const packages = ["numpy", "networkx", "matplotlib", "sympy"];
            await pyodideInstance.loadPackage(packages, {
              messageCallback: (msg) => console.log(`Package loading: ${msg}`),
              errorCallback: (err) => console.error(`Package error: ${err}`)
            });
            
            pyodideInstance._api.config.indexURL = originalIndexURL;
          }
          
          // Step 2: Load BKT code and files
          updateStatus('Loading BKT algorithm...', 'loading');
          
          const pyResponse = await fetch("../../_static/mcq_algorithm_current.py");
          if (!pyResponse.ok) {
            throw new Error(`Failed to fetch Python code: ${pyResponse.status}`);
          }
          const code = await pyResponse.text();
          pyodideInstance.FS.writeFile("bkt_system.py", code);
          
          // Load JSON files
          const files = [
            { name: "config.json", url: "../../_static/config.json" },
            { name: "small-graph-kg.json", url: "../../_static/small-graph-kg.json" },
            { name: "small-graph-mcqs.json", url: "../../_static/small-graph-mcqs.json" },
            { name: "small-graph-computed_mcqs.json", url: "../../_static/small-graph-computed_mcqs.json" }
          ];
          
          for (const file of files) {
            const response = await fetch(file.url);
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
            import json
            
            def js_export(obj):
                return json.dumps(obj)
            
            # Initialize the system
            kg = bkt_system.KnowledgeGraph(
                nodes_file='small-graph-kg.json',
                mcqs_file='small-graph-computed_mcqs.json',
                config_file='config.json')
            student_manager = bkt_system.StudentManager()
            mcq_scheduler = bkt_system.MCQScheduler(kg, student_manager)
            bkt = bkt_system.BayesianKnowledgeTracing(kg, student_manager)
            
            # Connect systems
            mcq_scheduler.set_bkt_system(bkt)
            student_manager.set_bkt_system(bkt)
            
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
              
              # ADD THE REFRESH FUNCTION HERE:
              def refresh_student_mastery(student_id):
                  student = student_manager.get_student(student_id)
                  if student and bkt.fsrs_forgetting:
                      for topic_index, mastery in list(student.mastery_levels.items()):
                          if mastery > 0.05:
                              decayed = bkt.fsrs_forgetting.apply_forgetting(student_id, topic_index, mastery)
                              student.mastery_levels[topic_index] = decayed
                  return True
              
              js_export({"success": True, "student_id": current_student_id})
          `);

          const data = JSON.parse(result);
          currentStudent = data.student_id;

          // Step 5: Generate first MCQ
          updateStatus('Generating your first question...', 'loading');
          
          await generateMCQ();
          
          // Step 6: Load knowledge graph after MCQ is ready
          updateStatus('Loading knowledge graph...', 'loading');
          loadGraphData('../../_static/small-graph.json');
          
          // Mark as initialized
          isInitialized = true;
          
        } catch (error) {
          updateStatus(`❌ Initialization failed: ${error.message}`, 'error');
          console.error('Auto-initialization error:', error);
        }
      }
      
      async function generateMCQ() {
        try {
          const result = await pyodideInstance.runPythonAsync(`
            import json
            
            try:
                student = student_manager.get_student(current_student_id)

                refresh_student_mastery(current_student_id)

                # Check what MCQ loading method is available
                available_topics = {}
                all_mcqs = []
                
                if hasattr(kg, 'ultra_loader') and kg.ultra_loader:
                    # Try the optimized loader first
                    print("Using ultra_loader")
                    all_mcqs = list(kg.ultra_loader.minimal_mcq_data.keys())
                    
                    # Group MCQs by topic
                    for mcq_id in all_mcqs:
                        minimal_data = kg.ultra_loader.get_minimal_mcq_data(mcq_id)
                        if minimal_data:
                            topic_idx = minimal_data.main_topic_index
                            if topic_idx not in available_topics:
                                available_topics[topic_idx] = []
                            available_topics[topic_idx].append(mcq_id)
                            
                elif hasattr(kg, 'mcqs') and kg.mcqs:
                    # Fallback to regular MCQ storage
                    print("Using regular kg.mcqs")
                    all_mcqs = list(kg.mcqs.keys())
                    
                    # Group MCQs by topic
                    for mcq_id in all_mcqs:
                        mcq = kg.mcqs.get(mcq_id)
                        if mcq:
                            topic_idx = mcq.main_topic_index
                            if topic_idx not in available_topics:
                                available_topics[topic_idx] = []
                            available_topics[topic_idx].append(mcq_id)
                else:
                    # Last resort: try to load from files directly
                    print("Loading MCQs from file directly")
                    import json as json_module
                    
                    try:
                        with open('small-graph-computed_mcqs.json', 'r') as f:
                            mcq_data = json_module.load(f)
                        
                        if 'mcqs' in mcq_data:
                            for i, mcq_info in enumerate(mcq_data['mcqs']):
                                mcq_id = mcq_info.get('id', f'mcq_{i}')
                                topic_idx = mcq_info.get('main_topic_index', 0)
                                
                                if topic_idx not in available_topics:
                                    available_topics[topic_idx] = []
                                available_topics[topic_idx].append(mcq_id)
                                all_mcqs.append(mcq_id)
                                
                            # Store for later use
                            kg._temp_mcq_data = mcq_data['mcqs']
                            
                    except Exception as file_error:
                        print(f"Failed to load from file: {file_error}")
                        result = json.dumps({"success": False, "error": f"No MCQs could be loaded: {file_error}"})
                        
                print(f"Total MCQs found: {len(all_mcqs)}")
                print(f"Available topics with MCQs: {list(available_topics.keys())}")
                
                if not available_topics:
                    result = json.dumps({"success": False, "error": "No MCQs found in any loading method"})
                else:
                    # Try our preferred topics in order
                    target_topics_to_try = [15, 2, 6, 17, 1, 0]  # Try various indices
                    target_topic = None
                    
                    for topic_idx in target_topics_to_try:
                        if topic_idx in available_topics:
                            target_topic = topic_idx
                            break
                    
                    # If none of our preferred topics work, just pick the first available
                    if target_topic is None:
                        target_topic = list(available_topics.keys())[0]
                    
                    print(f"Selected target topic: {target_topic}")
                    
                    # Get MCQs for the chosen topic that haven't been completed today
                    topic_mcqs = [mcq_id for mcq_id in available_topics[target_topic]
                                if mcq_id not in student.daily_completed]
                    
                    if not topic_mcqs:
                        # If all MCQs for this topic completed today, reset and use them anyway
                        topic_mcqs = available_topics[target_topic]
                        student.daily_completed.clear()  # Reset for demo purposes
                    
                    if topic_mcqs:
                        mcq_id = topic_mcqs[0]  # Take first available
                        print(f"Selected MCQ: {mcq_id}")
                        
                        # Try to get the MCQ data
                        mcq = None
                        mcq_dict = None
                        
                        if hasattr(kg, 'ultra_loader') and kg.ultra_loader:
                            mcq = kg.get_mcq_safely(mcq_id, need_full_text=True)
                        elif hasattr(kg, 'mcqs') and kg.mcqs:
                            mcq = kg.mcqs.get(mcq_id)
                        elif hasattr(kg, '_temp_mcq_data'):
                            # Find in temp data
                            for mcq_info in kg._temp_mcq_data:
                                if mcq_info.get('id') == mcq_id:
                                    mcq_dict = mcq_info
                                    break
                        
                        if mcq:
                            # We have a full MCQ object
                            topic_name = kg.get_topic_of_index(target_topic) or f"Topic {target_topic}"
                            current_mastery = student.get_mastery(target_topic)
                            
                            # Ensure this topic has some mastery for FSRS demo
                            if current_mastery < 0.3:
                                student.mastery_levels[target_topic] = 0.6
                                current_mastery = 0.6
                            
                            mcq_data = {
                                "success": True,
                                "mcq_id": mcq_id,
                                "text": mcq.text,
                                "options": mcq.options,
                                "correct_index": mcq.correctindex,
                                "explanations": mcq.option_explanations,
                                "topic_name": topic_name,
                                "topic_index": target_topic,
                                "current_mastery": current_mastery,
                                "difficulty": getattr(mcq, 'difficulty', 0.5),
                                "fsrs_info": {}
                            }
                            
                        elif mcq_dict:
                            # We have dictionary data
                            topic_name = kg.get_topic_of_index(target_topic) or f"Topic {target_topic}"
                            current_mastery = student.get_mastery(target_topic)
                            
                            if current_mastery < 0.3:
                                student.mastery_levels[target_topic] = 0.6
                                current_mastery = 0.6
                            
                            mcq_data = {
                                "success": True,
                                "mcq_id": mcq_id,
                                "text": mcq_dict.get('text', 'Sample question'),
                                "options": mcq_dict.get('options', ['Option A', 'Option B', 'Option C', 'Option D']),
                                "correct_index": mcq_dict.get('correctindex', 0),
                                "explanations": mcq_dict.get('option_explanations', ['Explanation'] * 4),
                                "topic_name": topic_name,
                                "topic_index": target_topic,
                                "current_mastery": current_mastery,
                                "difficulty": mcq_dict.get('overall_difficulty', 0.5),
                                "fsrs_info": {}
                            }
                        else:
                            mcq_data = {"success": False, "error": f"Could not load MCQ data for {mcq_id}"}
                        
                        # Add FSRS info if available
                        if mcq_data.get("success") and hasattr(bkt, 'fsrs_forgetting') and bkt.fsrs_forgetting:
                            try:
                                components = bkt.fsrs_forgetting.get_memory_components(current_student_id, target_topic)
                                # Initialize with some reasonable values for demo
                                if components.review_count == 0:
                                    components.review_count = 2
                                    components.stability = 3.0
                                    components.recent_success_rate = 0.7
                                
                                mcq_data["fsrs_info"] = {
                                    "stability": components.stability,
                                    "difficulty": components.difficulty,
                                    "retrievability": components.retrievability,
                                    "review_count": components.review_count
                                }
                            except Exception as fsrs_error:
                                print(f"FSRS error: {fsrs_error}")
                                mcq_data["fsrs_info"] = {}
                        
                        result = json.dumps(mcq_data)
                    else:
                        result = json.dumps({"success": False, "error": f"No MCQs available for topic {target_topic}"})
                        
            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                print(f"Error in generateMCQ: {error_details}")
                result = json.dumps({"success": False, "error": f"Error: {str(e)}"})
            
            result
          `);
          
          const data = JSON.parse(result);
          
          if (data.success) {
            currentMCQ = data;
            displayMCQ(data);
            updateStatus('Question ready! 🎯', 'success');
          } else {
            updateStatus(`❌ ${data.error}`, 'error');
            console.error('MCQ generation error details:', data);
          }
          
        } catch (error) {
          updateStatus('❌ Failed to generate MCQ', 'error');
          console.error('MCQ generation error:', error);
        }
      }
      
      function displayMCQ(mcqData) {
        const mcqSection = document.getElementById('mcq-section');
        mcqSection.style.display = 'block';
        
        // Hide status div when question is displayed
        document.getElementById('status').style.display = 'none';
        
        mcqSection.innerHTML = `
          <div class="mcq-container">
            <div class="mcq-question">${mcqData.text}</div>
            <div class="mcq-meta">
              <div><strong>📚 Topic:</strong> ${mcqData.topic_name}</div>
              <div><strong>📊 Current Mastery:</strong> ${(mcqData.current_mastery * 100).toFixed(1)}%</div>
              <div><strong>⚡ Difficulty:</strong> ${(mcqData.difficulty * 100).toFixed(1)}%</div>
            </div>
            
            <div class="mcq-options">
              ${mcqData.options.map((option, index) => 
                `<button class="mcq-option" onclick="selectOption(${index})">${option}</button>`
              ).join('')}
            </div>
            
            <button onclick="submitAnswer()" class="submit-btn" disabled id="submitBtn">
              ✅ Submit Answer
            </button>
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
          updateStatus('Processing your answer...', 'loading');
          
          const result = await pyodideInstance.runPythonAsync(`

            refresh_student_mastery(current_student_id)

            mcq_id = "${currentMCQ.mcq_id}"
            selected_option = ${selectedOption}
            correct_index = ${currentMCQ.correct_index}
            is_correct = selected_option == correct_index
            
            # Record the attempt and get BKT updates
            bkt_updates = student_manager.record_attempt(
                current_student_id, mcq_id, is_correct, 30.0, kg
            )
            
            # Get response data
            mcq = kg.get_mcq_safely(mcq_id, need_full_text=True)
            student = student_manager.get_student(current_student_id)
            topic_name = kg.get_topic_of_index(mcq.main_topic_index)
            
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
          
          // Update graph colors after answer is processed (preserving zoom level)
          await updateGraphMasteryColors();
          
          // Reset for next question
          selectedOption = null;
          currentMCQ = null;
          
        } catch (error) {
          updateStatus('❌ Failed to process answer', 'error');
          console.error('Answer processing error:', error);
        }
      }
      
      function displayResult(result) {
        const mcqSection = document.getElementById('mcq-section');
        const isCorrect = result.is_correct;
        const resultClass = isCorrect ? 'mcq-result-success' : 'mcq-result-error';
        const icon = isCorrect ? '✅' : '❌';
        const changeIcon = result.mastery_change > 0 ? '📈' : result.mastery_change < 0 ? '📉' : '➖';
        
        mcqSection.innerHTML = `
          <div class="mcq-container ${resultClass}">
            <h3>${icon} ${isCorrect ? 'Excellent!' : 'Not quite right, but you\'re learning!'}</h3>
            <p><strong>Your Answer:</strong> ${result.selected_text}</p>
            <p><strong>Correct Answer:</strong> ${result.correct_option}</p>
            <p><strong>Explanation:</strong> ${result.explanation}</p>
            
            <div class="mcq-result-inner">

              <h4>🧠 BKT Mastery Update</h4>
              <p><strong>📚 Topic:</strong> ${result.main_topic}</p>
              <p><strong>📊 Before:</strong> ${(result.before_mastery * 100).toFixed(1)}%</p>
              <p><strong>📊 After:</strong> ${(result.after_mastery * 100).toFixed(1)}%</p>
              <p><strong>📈 Change:</strong> ${changeIcon} ${result.mastery_change > 0 ? '+' : ''}${(result.mastery_change * 100).toFixed(2)}%</p>
              <p><strong>🔄 Total Topics Updated:</strong> ${result.total_changes}</p>
              <p><em>💡 Check the knowledge graph below to see the color changes!</em></p>
              
              <div class="progress-bar">
                <div class="progress-fill" style="width: ${result.after_mastery * 100}%;"></div>
              </div>
            </div>
            
            <button onclick="nextQuestion()" class="submit-btn primary">

              🚀 Next Question
            </button>
          </div>
        `;
        
        // Re-render MathJax for the new content
        if (window.MathJax) {
          MathJax.typesetPromise([mcqSection]).catch((err) => console.log('MathJax render error:', err));
        }
      }
      
      async function nextQuestion() {
        updateStatus('Generating next question...', 'loading');
        await generateMCQ();
      }

      // Initialize the network
      document.addEventListener('DOMContentLoaded', function() {
        const container = document.getElementById('graph-container');
        
        // Network options
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
            color: {
              color: '#848484',
              highlight: '#848484',
              hover: '#848484'
            }
          },
          physics: {
            stabilization: false,
            barnesHut: {
              gravitationalConstant: -50000,
              springConstant: 0.002,
              springLength: 150
            }
          },
          interaction: {
            navigationButtons: true,
            keyboard: true,
            hover: true
          }
        };

        // Create network
        network = new vis.Network(container, currentData, options);

        // Handle node selection
        network.on('select', function(params) {
          if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            const node = currentData.nodes.find(n => n.id === nodeId);
            if (node) {
              document.getElementById('node-title').textContent = node.label;
              document.getElementById('node-description').textContent = node.label || 'No description available';
              document.getElementById('node-strand').textContent = node.group || 'Unknown';
              
              // Show mastery level
              const masteryLevel = currentMasteryLevels[node.label];
              const masteryText = masteryLevel !== undefined ? 
                `${(masteryLevel * 100).toFixed(1)}%` : 'Not studied yet';
              document.getElementById('node-mastery').textContent = masteryText;
              
              document.getElementById('node-info').style.display = 'block';
            }
          }
        });

        // Handle deselection
        network.on('deselectNode', function() {
          document.getElementById('node-info').style.display = 'none';
        });

        // Filter by strand
        document.getElementById('strand-filter').addEventListener('change', function() {
          const selectedStrand = this.value;
          const nodes = currentData.nodes.map(node => {
            if (selectedStrand === '' || node.group === selectedStrand) {
              node.hidden = false;
            } else {
              node.hidden = true;
            }
            return node;
          });
          
          const edges = currentData.edges.map(edge => {
            const fromNode = currentData.nodes.find(n => n.id === edge.from);
            const toNode = currentData.nodes.find(n => n.id === edge.to);
            if (selectedStrand === '' || 
                (fromNode && !fromNode.hidden && toNode && !toNode.hidden)) {
              edge.hidden = false;
            } else {
              edge.hidden = true;
            }
            return edge;
          });
          
          network.setData({nodes: nodes, edges: edges});
          updateStats(nodes.filter(n => !n.hidden).length, edges.filter(e => !e.hidden).length);
        });

        // Reset view
        document.getElementById('reset-view').addEventListener('click', function() {
          network.fit();
        });

        // Toggle physics
        let physicsEnabled = true;
        document.getElementById('toggle-physics').addEventListener('click', function() {
          physicsEnabled = !physicsEnabled;
          network.setOptions({physics: {enabled: physicsEnabled}});
          this.textContent = physicsEnabled ? 'Toggle Physics' : 'Toggle Physics';
        });

        // Load graph data
        document.getElementById('load-simplified').addEventListener('click', function() {
          loadGraphData('../../_static/small-graph.json');
        });

        document.getElementById('load-full').addEventListener('click', function() {
          loadGraphData('../../_static/graph-data.json');
        });

        // Start auto-initialization
        autoInitialize();
      });

      function loadGraphData(filename) {
        // Set flag for initial load
        isInitialGraphLoad = true;
        
        fetch(filename)
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return response.json();
          })
          .then(data => {
            // Hide loading spinner
            const loadingDiv = document.getElementById('graph-loading');
            if (loadingDiv) {
              loadingDiv.style.display = 'none';
            }
            
            // Add initial positioning based on groups
            const groupPositions = {
              'Algebra': {x: -400, y: -200},
              'Geometry': {x: 400, y: -200},
              'Trigonometry': {x: 0, y: -400},
              'Calculus': {x: 0, y: 400},
              'Number': {x: -400, y: 200},
              'Statistics': {x: 400, y: 200},
              'Probability': {x: 400, y: 0},
              'Coordinate Geometry': {x: 200, y: -300},
              'Functions': {x: -200, y: 300},
              'Sequences and Series': {x: -200, y: -300},
              'Complex Numbers': {x: -300, y: 0},
              'Measurement': {x: 300, y: -100},
              'Synthetic geometry': {x: 300, y: -300},
              'Transformation geometry': {x: 200, y: 300},
              'Differential Calculus': {x: -100, y: 300},
              'Integral Calculus': {x: 100, y: 300},
              'Counting and Probability': {x: 300, y: 100}
            };
            
            // Apply group-based positioning and initial colors
            data.nodes.forEach(node => {
              node.color = '#6c757d';
              
              if (groupPositions[node.group]) {
                node.x = groupPositions[node.group].x + (Math.random() - 0.5) * 150;
                node.y = groupPositions[node.group].y + (Math.random() - 0.5) * 150;
              } else {
                node.x = (Math.random() - 0.5) * 800;
                node.y = (Math.random() - 0.5) * 800;
              }
            });
            
            currentData = data;
            network.setData(data);
            updateStats(data.nodes.length, data.edges.length);

            // Update strand filter options
            const strands = [...new Set(data.nodes.map(node => node.group))].sort();
            const filter = document.getElementById('strand-filter');
            filter.innerHTML = '<option value="">All Strands</option>';
            strands.forEach(strand => {
              if (strand && strand !== 'Unknown') {
                filter.innerHTML += `<option value="${strand}">${strand}</option>`;
              }
            });
            
            // Update colors if student exists
            if (currentStudent) {
              updateGraphMasteryColors();
            }
            
            // Set default zoomed out view (after a longer delay to ensure everything is loaded)
            setTimeout(() => {
              network.moveTo({
                scale: 0.05,
                animation: false // Disable animation for instant zoom
              });
              // Clear the initial load flag after zoom is set
              isInitialGraphLoad = false;
            }, 300);
            
            console.log(`Loaded ${data.nodes.length} nodes and ${data.edges.length} edges from ${filename}`);
            if (isInitialGraphLoad) {
              updateStatus('🎉 System ready! Answer questions to see your progress.', 'success');
            }
            isInitialGraphLoad = false;
          })
          .catch(error => {
            console.error('Error loading graph data:', error);
            loadSimplifiedFallback();
          });
      }

      function loadSimplifiedFallback() {
        // Set flag for initial load
        isInitialGraphLoad = true;
        
        // Hide loading spinner
        const loadingDiv = document.getElementById('graph-loading');
        if (loadingDiv) {
          loadingDiv.style.display = 'none';
        }
        
        // Fallback data if JSON files can't be loaded
        const fallbackData = {
          nodes: [
            {id: '1', label: 'Natural Numbers', group: 'Number', title: 'Counting numbers starting from 1'},
            {id: '2', label: 'Integers', group: 'Number', title: 'Whole numbers including negatives'},
            {id: '3', label: 'Rational Numbers', group: 'Number', title: 'Numbers expressible as fractions'},
            {id: '4', label: 'Complex Numbers', group: 'Number', title: 'Numbers with real and imaginary parts'},
            {id: '5', label: 'Linear Equations', group: 'Algebra', title: 'First-degree equations'},
            {id: '6', label: 'Quadratic Equations', group: 'Algebra', title: 'Second-degree equations'},
            {id: '7', label: 'Trigonometric Functions', group: 'Trigonometry', title: 'Sine, cosine, tangent functions'},
            {id: '8', label: 'Derivatives', group: 'Calculus', title: 'Rate of change of functions'},
            {id: '9', label: 'Integration', group: 'Calculus', title: 'Antiderivatives and areas'},
            {id: '10', label: 'Probability', group: 'Probability', title: 'Likelihood of events'}
          ],
          edges: [
            {from: '1', to: '2', title: 'Natural numbers extend to integers'},
            {from: '2', to: '3', title: 'Integers extend to rational numbers'},
            {from: '3', to: '4', title: 'Rational numbers extend to complex numbers'},
            {from: '5', to: '6', title: 'Linear equations are prerequisite for quadratics'},
            {from: '6', to: '8', title: 'Quadratic functions can be differentiated'},
            {from: '8', to: '9', title: 'Integration is the reverse of differentiation'},
            {from: '7', to: '8', title: 'Trigonometric functions can be differentiated'},
            {from: '7', to: '9', title: 'Trigonometric functions can be integrated'}
          ]
        };
        
        // Apply initial gray colors
        fallbackData.nodes.forEach(node => {
          node.color = '#6c757d';
        });
        
        currentData = fallbackData;
        network.setData(fallbackData);
        updateStats(fallbackData.nodes.length, fallbackData.edges.length);
        
        // Update colors if student exists
        if (currentStudent) {
          updateGraphMasteryColors();
        }
        
        // Set default zoomed out view (after a delay to ensure everything is loaded)
        setTimeout(() => {
          network.moveTo({
            scale: 0.05,
            animation: false // Disable animation for instant zoom
          });
          // Clear the initial load flag after zoom is set
          isInitialGraphLoad = false;
        }, 300);
      }

      function updateStats(nodeCount, edgeCount) {
        document.getElementById('node-count').textContent = nodeCount;
        document.getElementById('edge-count').textContent = edgeCount;
      }

      // Time manipulation functions
      async function skipTime(days, hours, minutes) {
        try {
          updateStatus('⏰ Skipping time...', 'loading');
          
          const result = await pyodideInstance.runPythonAsync(`
            import json
            from bkt_system import simulate_time_passage
            
            result = simulate_time_passage(bkt, current_student_id, days=${days}, hours=${hours}, minutes=${minutes})

            refresh_student_mastery(current_student_id)

            json.dumps(result)
          `);
          
          const data = JSON.parse(result);
          
          if (data.error) {
            updateStatus(`❌ ${data.error}`, 'error');
            return;
          }
          
          // Update time status display
          updateTimeStatus();
          
          // Update graph colors to show decay
          await updateGraphMasteryColors();
          
          // Show decay summary
          showDecaySummary(data);
          
          updateStatus(`✅ Time skipped: ${days} days, ${hours} hours, ${minutes} minutes`, 'success');
          
        } catch (error) {
          updateStatus('❌ Failed to skip time', 'error');
          console.error('Time skip error:', error);
        }
      }

      async function resetTime() {
        try {
          const result = await pyodideInstance.runPythonAsync(`
            import json
            from bkt_system import reset_time_to_real
            
            result = reset_time_to_real()
            json.dumps(result)
          `);
          
          const data = JSON.parse(result);
          updateTimeStatus();
          updateStatus('🔄 Time reset to present', 'success');
          
        } catch (error) {
          updateStatus('❌ Failed to reset time', 'error');
          console.error('Time reset error:', error);
        }
      }

      async function skipCustomTime() {
        const days = parseInt(document.getElementById('custom-days').value) || 0;
        const hours = parseInt(document.getElementById('custom-hours').value) || 0;
        
        if (days === 0 && hours === 0) {
          updateStatus('⚠️ Please enter days or hours to skip', 'error');
          return;
        }
        
        await skipTime(days, hours, 0);
        
        // Clear inputs
        document.getElementById('custom-days').value = '';
        document.getElementById('custom-hours').value = '';
      }

      async function updateTimeStatus() {
        try {
          const result = await pyodideInstance.runPythonAsync(`
            import json
            from bkt_system import get_time_status
            
            result = get_time_status()
            json.dumps(result)
          `);
          
          const data = JSON.parse(result);
          const statusDiv = document.getElementById('time-status');
          
          if (data.time_manipulation_active) {
            statusDiv.innerHTML = `
              ⏰ <strong>Time Travel Active</strong><br>
              📅 Real time: ${data.real_time}<br>
              🚀 Simulated time: ${data.simulated_time}<br>
              ⏭️ Offset: ${data.offset_days} days, ${data.offset_hours} hours
            `;
            statusDiv.className = 'time-manipulation-active';
          } else {
            statusDiv.innerHTML = '📅 Using real time';
            statusDiv.className = 'time-manipulation-inactive';
          }
          
        } catch (error) {
          console.error('Time status update error:', error);
        }
      }

      async function showMasteryDecay() {
        try {
          updateStatus('📊 Analyzing mastery decay...', 'loading');
          
          const result = await pyodideInstance.runPythonAsync(`
            import json
            
            student = student_manager.get_student(current_student_id)
            decay_info = []
            
            if hasattr(bkt, 'fsrs_forgetting') and bkt.fsrs_forgetting:
                for topic_index, mastery in student.mastery_levels.items():
                    if mastery > 0.05:
                        # Get current mastery with decay applied
                        current_with_decay = bkt.get_current_mastery_with_decay(current_student_id, topic_index)
                        decay_amount = mastery - current_with_decay
                        
                        if decay_amount > 0.001:
                            components = bkt.fsrs_forgetting.get_memory_components(current_student_id, topic_index)
                            decay_info.append({
                                'topic_name': kg.get_topic_of_index(topic_index),
                                'original_mastery': mastery,
                                'current_mastery': current_with_decay,
                                'decay_amount': decay_amount,
                                'decay_percentage': (decay_amount / mastery) * 100,
                                'stability': components.stability,
                                'review_count': components.review_count
                            })
            
            # Sort by decay amount
            decay_info.sort(key=lambda x: x['decay_amount'], reverse=True)
            json.dumps(decay_info)
          `);
          
          const decayData = JSON.parse(result);
          displayDecayAnalysis(decayData);
          updateStatus('📊 Mastery decay analysis complete', 'success');
          
        } catch (error) {
          updateStatus('❌ Failed to analyze decay', 'error');
          console.error('Decay analysis error:', error);
        }
      }

      async function previewDecay(days) {
        try {
          updateStatus(`🔮 Previewing ${days}-day decay...`, 'loading');
          
          const result = await pyodideInstance.runPythonAsync(`
            import json
            from bkt_system import preview_mastery_decay
            
            result = preview_mastery_decay(bkt, current_student_id, ${days})
            json.dumps(result)
          `);
          
          const data = JSON.parse(result);
          displayDecayPreview(data);
          updateStatus(`🔮 ${days}-day decay preview ready`, 'success');
          
        } catch (error) {
          updateStatus('❌ Failed to preview decay', 'error');
          console.error('Decay preview error:', error);
        }
      }

      function showDecaySummary(decayData) {
        const mcqSection = document.getElementById('mcq-section');
        const summary = decayData.decay_summary;
        const changes = decayData.topic_changes.slice(0, 5); // Show top 5
        
        let changesHtml = '';
        if (changes.length > 0) {
          changesHtml = '<h4>📉 Topics Most Affected:</h4><ul>';
          changes.forEach(change => {
            changesHtml += `<li><strong>${change.topic_name}:</strong> ${(change.mastery_before * 100).toFixed(1)}% → ${(change.mastery_after * 100).toFixed(1)}% (-${change.decay_percentage.toFixed(1)}%)</li>`;
          });
          changesHtml += '</ul>';
        }
        
        mcqSection.innerHTML = `
          <div class="container decay-summary-container">
            <h3>⏰ Time Skip Results</h3>
            <p><strong>Time Advanced:</strong> ${decayData.time_advanced.days} days, ${decayData.time_advanced.hours} hours</p>
            <p><strong>Topics Affected:</strong> ${summary.topics_affected}</p>
            <p><strong>Total Mastery Lost:</strong> ${(summary.total_decay * 100).toFixed(1)}%</p>
            <p><strong>Average Decay per Topic:</strong> ${(summary.average_decay * 100).toFixed(1)}%</p>
            
            ${changesHtml}
            
            <button onclick="generateMCQ()" class="success-btn">
              🎯 Practice to Restore Memory
            </button>
          </div>
        `;
        
        // Re-render MathJax
        if (window.MathJax) {
          MathJax.typesetPromise([mcqSection]).catch((err) => console.log('MathJax render error:', err));
        }
      }

      function displayDecayAnalysis(decayData) {
        // Similar implementation to showDecaySummary but for current analysis
        // You can implement this based on your preferred display format
      }

      function displayDecayPreview(previewData) {
        // Similar implementation for decay preview
        // You can implement this based on your preferred display format
      }
    </script>
</body>
</html>
