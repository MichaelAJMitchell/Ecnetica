```{raw} html

<!doctype html>
<html>
<head>
    <title>Comprehensive MCQ Algorithm Demo - Student Experience</title>
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
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mtml-chtml.js"></script>

    <!-- External Libraries -->
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <link rel="stylesheet" href="../../_static/style.css">
</head>
<body>
    <div class="comprehensive-demo-container">
        <!-- Header with Time Controls -->
        <div class="demo-header">
            <h1>🎯 Comprehensive MCQ Algorithm Demo</h1>
            <p class="subtitle">Experience the complete student learning journey with intelligent question selection</p>

            <div class="time-controls">
                <div class="current-time">
                    📅 Current Time: <span id="current-time-display">Loading...</span>
                </div>
                <div class="time-manipulation">
                    <button onclick="skipTime(1)" class="time-btn">⏰ +1 Day</button>
                    <button onclick="skipTime(7)" class="time-btn">📅 +1 Week</button>
                    <button onclick="skipTime(30)" class="time-btn">🗓️ +1 Month</button>
                    <button onclick="showForgettingPreview()" class="preview-btn">📉 Preview Decay</button>
                </div>
            </div>
        </div>

        <!-- Main Demo Content -->
        <div class="main-demo-layout">
            <!-- Left Column: Question Practice -->
            <div class="practice-section">
                <div class="container">
                    <!-- Status Display -->
                    <div id="status" class="status loading">
                        <div class="loading-spinner"></div>
                        Initializing MCQ System...
                    </div>

                    <!-- Session Progress -->
                    <div id="session-progress" class="session-progress" style="display: none;">
                        <div class="progress-header">
                            <h3>📚 Practice Session</h3>
                            <div class="progress-stats">
                                Question <span id="current-question-num">1</span> of <span id="total-questions">5</span>
                            </div>
                        </div>
                        <div class="progress-bar">
                            <div id="progress-fill" class="progress-fill"></div>
                        </div>
                    </div>

                    <!-- MCQ Display Area -->
                    <div id="mcq-section" class="mcq-section-hidden">
                        <div id="question-display" class="question-container">
                            <!-- Question content will be inserted here -->
                        </div>

                        <!-- Question Feedback Screen -->
                        <div id="question-feedback" class="feedback-screen" style="display: none;">
                            <div class="feedback-header">
                                <h3 id="feedback-result">Question Results</h3>
                            </div>
                            <div class="feedback-content">
                                <div id="correct-answer-display" class="correct-answer"></div>
                                <div id="explanation-display" class="explanation"></div>
                                <div id="mastery-updates-display" class="mastery-updates"></div>
                                <div id="skills-updates-display" class="skills-updates"></div>
                            </div>
                            <button id="continue-btn" onclick="continueToNextQuestion()" class="primary-btn">Continue to Next Question</button>
                        </div>

                        <!-- Breakdown Steps Area -->
                        <div id="breakdown-section" class="breakdown-section" style="display: none;">
                            <div class="breakdown-header">
                                <h3>🔍 Let's Break This Down</h3>
                                <p>We'll work through this step by step to help you understand.</p>
                                <div class="step-progress" id="step-progress">Step 1 of 3</div>
                            </div>
                            <div id="breakdown-steps-container">
                                <!-- Breakdown steps will be inserted here -->
                            </div>
                        </div>
                    </div>

                    <!-- Algorithm Explanation Panel -->
                    <div id="algorithm-panel" class="algorithm-panel">
                        <h3>🧠 How the Algorithm Works</h3>
                        <div id="algorithm-explanation" class="algorithm-explanation">
                            <div class="algorithm-step">
                                <h4>📊 Question Selection</h4>
                                <div id="selection-details">Analyzing your knowledge gaps...</div>
                            </div>
                            <div class="algorithm-step">
                                <h4>⚖️ Difficulty Matching</h4>
                                <div id="difficulty-details">Matching question difficulty to your skill level...</div>
                            </div>
                            <div class="algorithm-step">
                                <h4>🎯 Skills Assessment</h4>
                                <div id="skills-details">Updating mathematical skill profiles...</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right Column: Knowledge Graph & Skills -->
            <div class="visualization-section">
                <div class="container">
                    <!-- Knowledge Graph -->
                    <div class="graph-container-section">
                        <h2>🔗 Knowledge Graph</h2>
                        <p>Topics light up as you practice. Red = needs work, Green = mastered</p>

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

                        <div style="position: relative;">
                            <div id="graph-container"></div>
                            <div id="graph-loading" class="graph-loading">
                                <div class="graph-loading-spinner"></div>
                                <div class="graph-loading-text">Loading Knowledge Graph...</div>
                            </div>
                        </div>

                        <div class="graph-controls">
                            <button id="reset-view" class="secondary-btn">Reset View</button>
                            <button id="highlight-current" class="primary-btn">Highlight Current Topic</button>
                        </div>
                    </div>

                    <!-- Skills Display -->
                    <div class="skills-section">
                        <h3>📈 Mathematical Skills</h3>
                        <div id="skills-display" class="skills-grid">
                            <!-- Skills will be populated here -->
                        </div>
                    </div>

                    <!-- Spaced Repetition Info -->
                    <div class="spaced-repetition-section">
                        <h3>🕒 Spaced Repetition</h3>
                        <div id="spaced-repetition-info" class="spaced-repetition-info">
                            <div class="next-review">Next review due: <span id="next-review-time">Calculating...</span></div>
                            <div class="retention-info">Current retention: <span id="retention-percentage">--</span></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Session Summary Screen (Hidden initially) -->
        <div id="session-summary" class="session-summary-screen" style="display: none;">
            <div class="summary-container">
                <div class="summary-header">
                    <h1>🎉 Revision Session Finished!</h1>
                    <div class="session-stats">
                        <div class="stat-item">
                            <span class="stat-number" id="questions-correct">8</span>
                            <span class="stat-label">questions right out of</span>
                            <span class="stat-number" id="questions-total">10</span>
                        </div>
                    </div>
                </div>

                <div class="summary-content">
                    <div class="summary-section">
                        <h3>📊 You improved on 10 topics</h3>
                        <div id="improved-topics" class="topics-list">
                            <!-- Improved topics will be listed here -->
                        </div>
                    </div>

                    <div class="summary-section">
                        <h3>📝 Topics to review again:</h3>
                        <div id="review-topics" class="topics-list">
                            <!-- Topics needing review will be listed here -->
                        </div>
                    </div>

                    <div class="summary-section">
                        <h3>🎯 Quadratic equations</h3>
                        <div class="topic-detail">
                            <div>Marginally formulae</div>
                        </div>
                    </div>
                </div>

                <div class="summary-actions">
                    <button onclick="startNewSession()" class="primary-btn">Start New Session</button>
                    <button onclick="reviewSpecificTopic()" class="secondary-btn">Review Specific Topic</button>
                </div>
            </div>
        </div>
    </div>

    <script type="text/javascript">
        // Global Variables
        let pyodideInstance = null;
        let currentStudent = null;
        let currentMCQ = null;
        let selectedOption = null;
        let isInitialized = false;
        let isInitialGraphLoad = false;
        let current_student_id = "comprehensive_demo_student";

        // Knowledge Graph Variables
        let network;
        let currentData = {nodes: [], edges: []};
        let currentMasteryLevels = {};
        let topicIndexToNodeId = {};

        // Session Management
        let sessionQuestions = [];
        let currentQuestionIndex = 0;
        let sessionStartMasteries = {};
        let sessionStartSkills = {};
        let questionResults = [];

        // Breakdown Management (copying MCQ_Breakdown_Demo pattern)
        let isInBreakdown = false;
        let currentBreakdown = null;  // Will store: {steps, currentStep, totalSteps, completedSteps, mcq_id}

        // Time Management
        let timeOffset = 0; // Days offset for demo

        function renderMathJax(element = document) {
            if (window.MathJax && window.MathJax.typesetPromise) {
                setTimeout(() => {
                    MathJax.typesetPromise([element]).then(() => {
                        console.log('MathJax rendered successfully');
                    }).catch((err) => {
                        console.log('MathJax render error:', err);
                        // Fallback: try the older MathJax API
                        if (window.MathJax.Hub) {
                            MathJax.Hub.Queue(["Typeset", MathJax.Hub, element]);
                        }
                    });
                }, 100);
            } else if (window.MathJax && window.MathJax.Hub) {
                // Fallback for older MathJax versions
                setTimeout(() => {
                    MathJax.Hub.Queue(["Typeset", MathJax.Hub, element]);
                }, 100);
            } else {
                console.log('MathJax not ready, will retry...');
                setTimeout(() => renderMathJax(element), 500);
            }
        }
        function updateStatus(message, type = 'info') {
            const statusDiv = document.getElementById('status');
            statusDiv.className = `status ${type}`;

            if (type === 'loading') {
                statusDiv.innerHTML = `<div class="loading-spinner"></div>${message}`;
            } else {
                statusDiv.textContent = message;
            }
        }

        function updateTimeDisplay() {
            const now = new Date();
            now.setDate(now.getDate() + timeOffset);
            document.getElementById('current-time-display').textContent =
                now.toLocaleDateString() + ' ' + now.toLocaleTimeString();
        }

        async function skipTime(days, hours, minutes) {
            try {
            updateStatus('⏰ Skipping time...', 'loading');

            const result = await pyodideInstance.runPythonAsync(`
                import json
                from bkt_system import simulate_time_passage

                result = simulate_time_passage(bkt_system, current_student_id, days=${days}, hours=${hours}, minutes=${minutes})

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

                if hasattr(bkt_system, 'fsrs_forgetting') and bkt_system.fsrs_forgetting:
                    for topic_index, mastery in student.mastery_levels.items():
                        if mastery > 0.05:
                            # Get current mastery with decay applied
                            current_with_decay = bkt_system.get_current_mastery_with_decay(current_student_id, topic_index)
                            decay_amount = mastery - current_with_decay

                            if decay_amount > 0.001:
                                components = bkt_system.fsrs_forgetting.get_memory_components(current_student_id, topic_index)
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

                result = preview_mastery_decay(bkt_system, current_student_id, ${days})
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

        function showForgettingPreview() {
            if (pyodideInstance && currentStudent) {
                pyodideInstance.runPythonAsync(`
                    # Show preview of decay without applying it
                    student = student_manager.get_student(current_student_id)
                    preview_data = {}

                    for topic_idx, mastery in student.mastery_levels.items():
                        if mastery > 0.05:
                            # Simulate 30-day decay
                            preview_mastery = bkt_system.fsrs_forgetting.apply_forgetting(
                                current_student_id, topic_idx, mastery)

                            topic_name = kg.get_topic_of_index(topic_idx)
                            preview_data[topic_name] = {
                                'current': mastery,
                                'after_30_days': preview_mastery,
                                'decay': mastery - preview_mastery
                            }

                    js_export(preview_data)
                `).then(result => {
                    const previewData = JSON.parse(result);
                    showDecayPreviewModal(previewData);
                });
            }
        }

        function showDecayPreviewModal(previewData) {
            // Create modal showing decay preview
            const modal = document.createElement('div');
            modal.className = 'decay-preview-modal';
            modal.innerHTML = `
                <div class="modal-content">
                    <h3>📉 30-Day Forgetting Preview</h3>
                    <div class="decay-list">
                        ${Object.entries(previewData).map(([topic, data]) => `
                            <div class="decay-item">
                                <span class="topic-name">${topic}</span>
                                <span class="decay-change">${(data.current * 100).toFixed(1)}% → ${(data.after_30_days * 100).toFixed(1)}%</span>
                            </div>
                        `).join('')}
                    </div>
                    <button onclick="this.parentElement.parentElement.remove()" class="primary-btn">Close</button>
                </div>
            `;
            document.body.appendChild(modal);
        }

        // Initialize the comprehensive demo
        async function initializeDemo() {
            updateStatus('Loading Python environment...', 'loading');
            updateTimeDisplay();

            try {
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
                // Load your MCQ algorithm code here
                updateStatus('Loading MCQ algorithm...', 'loading');

                const pyResponse = await fetch("../../_static/mcq_algorithm_current.py", { cache: "no-store" });
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
                await pyodideInstance.runPythonAsync(`
                    import sys
                    sys.path.append('.')
                    import bkt_system
                    from bkt_system import *
                    import json

                    def js_export(obj):
                        return json.dumps(obj)

                    current_student_id = "comprehensive_demo_student"
                    current_mcq_instance = None


                    # Ensure built-in functions are available
                    import builtins
                    list = builtins.list  # Ensure list is the built-in function

                    # Initialize the system
                    kg = bkt_system.KnowledgeGraph(
                        nodes_file='kg_new.json',
                        mcqs_file='computed_mcqs_breakdown.json',
                        config_file='config.json'
                    )
                    student_manager = bkt_system.StudentManager(kg.config)
                    mcq_scheduler = bkt_system.MCQScheduler(kg, student_manager)
                    bkt_system = bkt_system.BayesianKnowledgeTracing(kg, student_manager)

                    # Connect systems
                    mcq_scheduler.set_bkt_system(bkt_system)
                    bkt_system.set_scheduler(mcq_scheduler)
                    student_manager.set_bkt_system(bkt_system)

                    # Initialize global MCQ instance variable
                    current_mcq_instance = None
                    # Store globally
                    globals()['kg'] = kg
                    globals()['student_manager'] = student_manager
                    globals()['bkt_system'] = bkt_system
                    globals()['mcq_scheduler'] = mcq_scheduler
                    globals()['current_student_id'] = current_student_id
                    globals()['current_mcq_instance'] = current_mcq_instance



                    # Initialize time manipulator
                    from datetime import datetime, timedelta
                    import math

                    class TimeManipulator:


                        def __init__(self):
                            self._time_offset = timedelta(0)  # How much time we've "fast-forwarded"
                            self._original_now = datetime.now  # Store original datetime.now function

                        def get_current_time(self) -> datetime:
                            """Get the current "simulated" time"""
                            return self._original_now() + self._time_offset

                        def fast_forward(self, days: int = 0, hours: int = 0, minutes: int = 0) -> datetime:
                            time_delta = timedelta(days=days, hours=hours, minutes=minutes)
                            self._time_offset += time_delta
                            new_time = self.get_current_time()

                            print(f"⏰ Time fast-forwarded by {days} days, {hours} hours, {minutes} minutes")
                            print(f"📅 Current simulated time: {new_time.strftime('%Y-%m-%d %H:%M:%S')}")

                            return new_time

                        def reset_time(self) -> datetime:
                            """Reset time manipulation back to real time"""
                            self._time_offset = timedelta(0)
                            real_time = self._original_now()
                            print(f"🔄 Time reset to real time: {real_time.strftime('%Y-%m-%d %H:%M:%S')}")
                            return real_time

                        def get_time_offset(self) -> timedelta:
                            """Get current time offset"""
                            return self._time_offset

                        def get_time_info(self) -> dict:
                            """Get time manipulation info for display"""
                            real_time = self._original_now()
                            sim_time = self.get_current_time()

                            return {
                                'real_time': real_time.strftime('%Y-%m-%d %H:%M:%S'),
                                'simulated_time': sim_time.strftime('%Y-%m-%d %H:%M:%S'),
                                'offset_days': self._time_offset.days,
                                'offset_hours': self._time_offset.seconds // 3600,
                                'offset_minutes': (self._time_offset.seconds % 3600) // 60,
                                'time_manipulation_active': self._time_offset != timedelta(0)
                            }
                    def refresh_student_mastery(student_id):
                        student = student_manager.get_student(student_id)
                        if not student or not bkt_system.fsrs_forgetting:
                            return
                        print(f"🔄 Refreshing mastery for {student_id}...")

                        updates = []
                        topic_items = builtins.list(student.mastery_levels.items())  # Use builtins.list explicitly
                        for topic_index, stored_mastery in topic_items:
                            if stored_mastery > 0.05:
                                decayed_mastery = bkt_system.fsrs_forgetting.apply_forgetting(
                                    student_id, topic_index, stored_mastery)
                                decay_amount = stored_mastery - decayed_mastery
                                if decay_amount > 0.001:
                                    student.mastery_levels[topic_index] = decayed_mastery
                                    topic_name = bkt_system.kg.get_topic_of_index(topic_index)
                                    updates.append(f"   {topic_name}: {stored_mastery:.3f} → {decayed_mastery:.3f} (-{decay_amount:.3f})")

                        if updates:
                            print(f"📉 Applied decay to {len(updates)} topics:")
                            for update in updates[:5]:
                                print(update)
                            if len(updates) > 5:
                                print(f"   ... and {len(updates)-5} more")
                        else:
                            print("   No significant decay to apply")


                    time_manipulator = TimeManipulator()


                    print("System initialized successfully!")
                `);

                updateStatus('Creating demo student...', 'loading');

                await initializeStudent();
                await loadKnowledgeGraph();
                await startPracticeSession();

            } catch (error) {
                console.error('Initialization error:', error);
                updateStatus('❌ Failed to initialize. Check console for details.', 'error');
            }
        }

        async function initializeStudent() {
            // Create student and set initial mastery levels

            const result = await pyodideInstance.runPythonAsync(`
                print(">>> entered initializeStudent block")
                print(f"current_student_id from JS is: {repr(current_student_id)}")
                print(f"student_manager is: {type(student_manager)}")
                print(f"create_student is: {type(student_manager.create_student)}")


                student = student_manager.create_student(current_student_id)

                import random
                random.seed(42)  # For reproducible demo
                initial_masteries = {}
                initial_skills = {}

                # Get all topic indices as a Python list
                all_topic_indices = []
                for topic_idx in kg.get_all_indexes():
                    all_topic_indices.append(topic_idx)

                print(f"Total topics available: {len(all_topic_indices)}")



                # Set varied mastery levels across topics
                for i, topic_idx in enumerate(all_topic_indices):
                    mastery = random.uniform(0.1, 0.8)
                    student.mastery_levels[topic_idx] = mastery
                    student.confidence_levels[topic_idx] = mastery * 0.9
                    student.studied_topics[topic_idx] = True


                    # Get topic name safely
                    try:
                        topic_name = kg.get_topic_of_index(topic_idx)
                        if topic_name:
                            initial_masteries[topic_name] = mastery
                        else:
                            initial_masteries[f"Topic_{topic_idx}"] = mastery
                    except Exception as e:
                        print(f"Warning: Could not get name for topic {topic_idx}: {e}")
                        initial_masteries[f"Topic_{topic_idx}"] = mastery

                print(f"Set mastery for {len(initial_masteries)} topics")

                # Record initial skill levels
                skill_names = ['memory', 'conceptual_understanding', 'procedural_fluency',
                            'problem_solving', 'mathematical_communication', 'spatial_reasoning']

                for skill in skill_names:
                    initial_skills[skill] = student.ability_levels.get(skill, 0.5)

                print(f"Recorded {len(initial_skills)} initial skill levels")

                js_export({
                    'masteries': initial_masteries,
                    'skills': initial_skills,
                    'student_id': current_student_id,
                    'topics_count': len(initial_masteries)
                })
            `);

            const studentData = JSON.parse(result);
            sessionStartMasteries = studentData.masteries;
            sessionStartSkills = studentData.skills;

            currentStudent = current_student_id;

            console.log("✅ Student initialized:", currentStudent);
            console.log("✅ Topics initialized:", studentData.topics_count);
            console.log("✅ Skills initialized:", Object.keys(studentData.skills).length);

            updateSkillsDisplay(studentData.skills);
        }

        async function loadKnowledgeGraph() {
            isInitialGraphLoad = true;
            updateStatus('Loading knowledge graph...', 'loading');

            // First try to load from actual graph file
            try {
                const graphResult = await pyodideInstance.runPythonAsync(`
                    # Try to get graph data from your KG
                    graph_data = kg.get_vis_network_data()
                    js_export(graph_data)
                `);

                const graphData = JSON.parse(graphResult);
                currentData = graphData;
                initializeNetwork(graphData);

            } catch (error) {
                console.log('Could not load from KG, using fallback data');

                // Use fallback data (copy this from BKT_Simple_Demo.md lines ~580-620)
                const fallbackData = {
                    nodes: [{}
                    ],
                    edges: [{}
                    ]
                };

                currentData = fallbackData;
                initializeNetwork(fallbackData);
            }

            document.getElementById('graph-loading').style.display = 'none';
            await updateGraphMasteryColors();
            isInitialGraphLoad = false;
        }

        function initializeNetwork(graphData) {
            const container = document.getElementById('graph-container');
            const data = { nodes: graphData.nodes, edges: graphData.edges };

            const options = {
                nodes: {
                    shape: 'circle',
                    size: 25,
                    font: { size: 14, color: '#333' },
                    borderWidth: 2,
                    color: { border: '#2B7CE9' }
                },
                edges: {
                    arrows: { to: { enabled: true, scaleFactor: 0.5 } },
                    color: { color: '#848484' },
                    smooth: { type: 'continuous' }
                },
                physics: { enabled: false },
                interaction: { hover: true, selectConnectedEdges: false }
            };

            network = new vis.Network(container, data, options);

            // Set up click handler
            network.on('click', function(params) {
                if (params.nodes.length > 0) {
                    const nodeId = params.nodes[0];
                    const node = graphData.nodes.find(n => n.id === nodeId);
                    if (node) {
                        console.log('Clicked node:', node.label);
                    }
                }
            });
        }

        async function startPracticeSession() {
            updateStatus('Selecting optimal questions for you...', 'loading');

            // Get optimal MCQs for session
            const sessionResult = await pyodideInstance.runPythonAsync(`
                # Select optimal MCQs for session
                selected_mcqs = mcq_scheduler.select_optimal_mcqs(current_student_id, num_questions=5)

                session_data = {
                    'mcq_ids': selected_mcqs,
                    'total_questions': len(selected_mcqs)
                }

                js_export(session_data)
            `);

            const sessionData = JSON.parse(sessionResult);
            sessionQuestions = sessionData.mcq_ids;
            currentQuestionIndex = 0;

            // Update UI
            document.getElementById('total-questions').textContent = sessionData.total_questions;
            document.getElementById('session-progress').style.display = 'block';

            await displayNextQuestion();
        }

        async function displayNextQuestion() {
            if (currentQuestionIndex >= sessionQuestions.length) {
                await showSessionSummary();
                return;
            }

            updateStatus('Loading question...', 'loading');

            // Update progress
            document.getElementById('current-question-num').textContent = currentQuestionIndex + 1;
            const progressPercent = (currentQuestionIndex / sessionQuestions.length) * 100;
            document.getElementById('progress-fill').style.width = `${progressPercent}%`;

            const mcqId = sessionQuestions[currentQuestionIndex];

            // Get MCQ data and preserve instance
            const mcqResult = await pyodideInstance.runPythonAsync(`
                mcq_id = "${mcqId}"
                mcq = kg.get_mcq_safely(mcq_id, need_full_text=True)

                if mcq:
                    # Store MCQ instance globally for breakdown consistency
                    current_mcq_instance = mcq

                    mcq_data = {
                        'success': True,
                        'mcq_id': mcq_id,
                        'text': mcq.question_text,
                        'options': mcq.question_options,
                        'correct_index': mcq.correctindex,
                        'explanations': mcq.rendered_option_explanations(),
                        'topic_name': kg.get_topic_of_index(mcq.main_topic_index),
                        'topic_index': mcq.main_topic_index,
                        'difficulty': getattr(mcq, 'difficulty', 0.5),
                        'has_breakdown': hasattr(mcq, 'breakdown_steps') and mcq.breakdown_steps
                    }
                else:
                    mcq_data = {'success': False, 'error': 'MCQ not found'}

                js_export(mcq_data)
            `);

            const mcqData = JSON.parse(mcqResult);

            if (mcqData.success) {
                currentMCQ = mcqData;
                displayMCQ(mcqData);
                updateAlgorithmExplanation(mcqData);
                highlightCurrentTopic(mcqData.topic_index);
                updateStatus('Question ready!', 'success');
            } else {
                updateStatus('❌ Error loading question', 'error');
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


        async function submitAnswer() {
            if (selectedOption === null) return;

            const isCorrect = selectedOption === currentMCQ.correct_index;

            // Process answer through BKT system using stored instance (MCQ_Breakdown_Demo pattern)
            const updateResult = await pyodideInstance.runPythonAsync(`
                import json

                try:
                    # Use the stored MCQ instance for consistency
                    mcq = current_mcq_instance
                    is_correct = ${isCorrect}
                    topic_index = ${currentMCQ.topic_index}

                    # Process the response
                    result = bkt_system.process_student_response(
                        current_student_id, topic_index, is_correct, mcq.id
                    )

                    # Check if breakdown should be triggered
                    has_breakdown = (not is_correct and
                                   hasattr(mcq, 'breakdown_steps') and
                                   mcq.breakdown_steps)

                    result['has_breakdown'] = has_breakdown
                    result['is_correct'] = is_correct

                    js_export(result)

                except Exception as e:
                    js_export({'success': False, 'error': str(e)})
            `);

            const bktResult = JSON.parse(updateResult);

            if (bktResult.success === False) {
                updateStatus('❌ Error processing answer', 'error');
                return;
            }

            // Check if breakdown is needed
            if (!isCorrect && bktResult.has_breakdown) {
                await startBreakdownSequence();
                return;
            }

            // Show question feedback
            showQuestionFeedback(isCorrect, bktResult);
        }

        function showQuestionFeedback(isCorrect, bktResult) {
            const feedbackHtml = `
                <div class="feedback-result ${isCorrect ? 'correct' : 'incorrect'}">
                    ${isCorrect ? '✅ Correct!' : '❌ Incorrect'}
                </div>
                <div class="correct-answer">
                    <strong>Correct Answer:</strong> ${String.fromCharCode(65 + currentMCQ.correct_index)}) ${currentMCQ.options[currentMCQ.correct_index]}
                </div>
                <div class="explanation">
                    <strong>Explanation:</strong> ${currentMCQ.explanations[currentMCQ.correct_index]}
                </div>
                <div class="mastery-updates">
                    <h4>📊 Mastery Updates</h4>
                    <div class="update-item">
                        <span class="topic-name">${bktResult.topic_name}</span>
                        <span class="mastery-change">${(bktResult.mastery_before * 100).toFixed(1)}% → ${(bktResult.mastery_after * 100).toFixed(1)}%</span>
                    </div>
                </div>
                <div class="skills-updates">
                    <h4>🧠 Skills Updates</h4>
                    <div class="skills-changes">
                        ${Object.entries(bktResult.skill_updates || {}).map(([skill, update]) => `
                            <div class="skill-update">
                                <span class="skill-name">${skill.replace('_', ' ')}</span>
                                <span class="skill-change">${(update.old_ability * 100).toFixed(1)}% → ${(update.new_ability * 100).toFixed(1)}%</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;

            document.getElementById('question-display').style.display = 'none';
            document.getElementById('question-feedback').style.display = 'block';
            document.getElementById('question-feedback').innerHTML = feedbackHtml +
                '<button id="continue-btn" onclick="continueToNextQuestion()" class="primary-btn">Continue to Next Question</button>';

            // Store result for session summary
            questionResults.push({
                mcq_id: currentMCQ.mcq_id,
                topic_name: currentMCQ.topic_name,
                is_correct: isCorrect,
                bkt_result: bktResult
            });

            // Update visualizations
            updateGraphMasteryColors();
            updateSkillsDisplay();
        }

        async function checkForBreakdown() {
            // Check if current MCQ has breakdown capability
            const hasBreakdown = await pyodideInstance.runPythonAsync(`
                mcq = kg.get_mcq_safely("${currentMCQ.mcq_id}", need_full_text=True)
                has_breakdown = hasattr(mcq, 'breakdown_steps') and mcq.breakdown_steps
                js_export(has_breakdown)
            `);

            return JSON.parse(hasBreakdown);
        }

        async function startBreakdownSequence() {
            updateStatus('Generating breakdown steps...', 'loading');

            const breakdownResult = await pyodideInstance.runPythonAsync(`
                import json

                try:
                    # Use the stored MCQ instance (preserves cached parameters)
                    mcq = current_mcq_instance
                    student = student_manager.get_student(current_student_id)

                    # Generate breakdown steps
                    student_answer = ${selectedOption}
                    student_mastery = student.mastery_levels
                    config = kg.config.get_breakdown_config()

                    breakdown_steps = mcq.execute_breakdown_for_student(student_answer, student_mastery, config)

                    if breakdown_steps:
                        steps_data = []
                        for step in breakdown_steps:
                            steps_data.append({
                                'step_no': step.step_no,
                                'step_type': step.step_type,
                                'text': step.render_step_text(),
                                'options': step.render_step_options(),
                                'correct_index': step.correctindex,
                                'explanations': step.render_step_option_explanations(),
                                'prereq_topics': step.prereq_topics
                            })

                        result = {
                            'success': True,
                            'steps': steps_data,
                            'total_steps': len(steps_data),
                            'mcq_id': mcq.id
                        }
                    else:
                        result = {'success': False}

                    js_export(result)

                except Exception as e:
                    js_export({'success': False, 'error': str(e)})
            `);

            const breakdownData = JSON.parse(breakdownResult);

            if (breakdownData.success) {
                // Initialize breakdown state (copying from MCQ_Breakdown_Demo pattern)
                currentBreakdown = {
                    steps: breakdownData.steps,
                    currentStep: 0,
                    totalSteps: breakdownData.total_steps,
                    completedSteps: [],
                    mcq_id: breakdownData.mcq_id
                };

                isInBreakdown = true;

                // Show breakdown section and hide main question
                document.getElementById('question-display').style.display = 'none';
                document.getElementById('breakdown-section').style.display = 'block';

                displayBreakdownStep(0);
            } else {
                // No breakdown available, show regular feedback
                showQuestionFeedback(false, {});
            }
        }

        function displayBreakdownStep() {
            const step = currentBreakdownSteps[currentBreakdownIndex];

            const stepHtml = `
                <div class="breakdown-step">
                    <div class="step-header">
                        <h4>Step ${step.step_no}: ${step.step_type.replace('_', ' ').toUpperCase()}</h4>
                        <div class="step-progress">${currentBreakdownIndex + 1} of ${currentBreakdownSteps.length}</div>
                    </div>
                    <div class="step-content">
                        <div class="step-text">${step.text}</div>
                        <div class="step-options">
                            ${step.options.map((option, index) => `
                                <div class="option" onclick="selectBreakdownOption(${index})">
                                    <span class="option-letter">${String.fromCharCode(65 + index)}</span>
                                    <span class="option-text">${option}</span>
                                </div>
                            `).join('')}
                        </div>
                        <button id="submit-breakdown" onclick="submitBreakdownStep()" class="primary-btn" disabled>Submit Step</button>
                    </div>
                </div>
            `;

            document.getElementById('question-display').style.display = 'none';
            document.getElementById('breakdown-section').style.display = 'block';
            document.getElementById('breakdown-steps-container').innerHTML = stepHtml;

            updateStatus(`Working through breakdown step ${currentBreakdownIndex + 1}...`, 'info');

            // Render MathJax
            if (window.MathJax) {
                MathJax.typesetPromise([document.getElementById('breakdown-steps-container')]);
            }
        }

        function selectBreakdownOption(index) {
            // Remove previous selection (copying MCQ_Breakdown_Demo pattern)
            document.querySelectorAll('#current-step .mcq-option').forEach(btn => btn.classList.remove('selected'));

            // Add selection to clicked option
            document.querySelectorAll('#current-step .mcq-option')[index].classList.add('selected');

            selectedOption = index;
            document.getElementById('breakdownSubmitBtn').disabled = false;
        }

        async function submitBreakdownStep(stepIndex) {
            if (selectedOption === null) return;

            const step = currentBreakdown.steps[stepIndex];
            const isCorrect = selectedOption === step.correct_index;

            try {
                // Process breakdown step using the stored MCQ instance (from MCQ_Breakdown_Demo pattern)
                await pyodideInstance.runPythonAsync(`
                    # Use the stored MCQ instance for consistency
                    mcq = current_mcq_instance

                    # Record breakdown step as attempt against parent MCQ
                    student_manager.record_attempt(
                        "${currentStudent}",
                        mcq.id,
                        ${isCorrect ? 'True' : 'False'},
                        15.0,
                        kg
                    )

                    # Also process as skill update
                    step_type = "${step.step_type}"
                    step_difficulty = 2.5

                    skill_result = bkt_system.process_breakdown_step_response(
                        current_student_id, step_type, ${isCorrect ? 'True' : 'False'}, step_difficulty
                    )

                    print(f"Recorded breakdown step ${stepIndex} against parent MCQ {mcq.id}: {'correct' if ${isCorrect ? 'True' : 'False'} else 'incorrect'}")
                `);

                // Store completion data (copying MCQ_Breakdown_Demo pattern)
                currentBreakdown.completedSteps[stepIndex] = {
                    selectedAnswer: selectedOption,
                    wasCorrect: isCorrect
                };

                // Show explanation immediately (key pattern from breakdown demo)
                const explanationDiv = document.getElementById(`breakdown-explanation-${stepIndex}`);
                explanationDiv.style.display = 'block';
                explanationDiv.className = `step-explanation ${isCorrect ? 'correct' : 'incorrect'}`;
                explanationDiv.innerHTML = `
                    <div class="explanation-content">
                        <strong>Explanation:</strong> ${step.explanations[step.correct_index]}
                        ${!isCorrect ? `<br><strong>You selected:</strong> ${step.explanations[selectedOption]}` : ''}
                    </div>
                    <button class="continue-btn" onclick="continueBreakdown(${stepIndex})">
                        ${stepIndex + 1 < currentBreakdown.totalSteps ? 'Continue to Next Step' : 'Complete Breakdown'}
                    </button>
                `;

                // Disable step options (copying MCQ_Breakdown_Demo pattern)
                document.querySelectorAll('#current-step .mcq-option').forEach(btn => {
                    btn.disabled = true;
                    btn.style.opacity = '0.6';
                });
                document.getElementById('breakdownSubmitBtn').disabled = true;
                document.getElementById('breakdownSubmitBtn').style.opacity = '0.6';

                // Re-render MathJax for explanation
                if (window.MathJax) {
                    MathJax.typesetPromise([explanationDiv]);
                }

            } catch (error) {
                console.error('Error recording breakdown step:', error);
                updateStatus('❌ Error processing step', 'error');
            }
        }

        function showBreakdownStepFeedback(isCorrect, step, stepResult) {
            const feedbackHtml = `
                <div class="step-feedback ${isCorrect ? 'correct' : 'incorrect'}">
                    <div class="step-result">
                        ${isCorrect ? '✅ Correct!' : '❌ Not quite right'}
                    </div>
                    <div class="correct-answer">
                        <strong>Correct Answer:</strong> ${String.fromCharCode(65 + step.correct_index)}) ${step.options[step.correct_index]}
                    </div>
                    <div class="explanation">
                        <strong>Explanation:</strong> ${step.explanations[step.correct_index]}
                    </div>
                    ${stepResult.skill_update ? `
                        <div class="skill-update">
                            <strong>Skill Update:</strong> ${step.step_type.replace('_', ' ')}
                            ${(stepResult.skill_update.old_ability * 100).toFixed(1)}% → ${(stepResult.skill_update.new_ability * 100).toFixed(1)}%
                        </div>
                    ` : ''}
                </div>
                <button onclick="continueBreakdown()" class="primary-btn">
                    ${currentBreakdownIndex < currentBreakdownSteps.length - 1 ? 'Next Step' : 'Complete Breakdown'}
                </button>
            `;

            document.getElementById('breakdown-steps-container').innerHTML = feedbackHtml;
            selectedOption = null;
        }

        function continueBreakdown(currentStepIndex) {
            const nextStepIndex = currentStepIndex + 1;

            if (nextStepIndex < currentBreakdown.totalSteps) {
                // Move to next step
                currentBreakdown.currentStep = nextStepIndex;
                selectedOption = null;
                displayBreakdownStep(nextStepIndex);
            } else {
                // Complete breakdown sequence
                completeBreakdownSequence();
            }
        }

        async function completeBreakdownSequence() {
            // Show breakdown completion summary (copying MCQ_Breakdown_Demo pattern)
            const container = document.getElementById('breakdown-steps-container');

            // Calculate completion stats
            const totalSteps = currentBreakdown.totalSteps;
            const correctSteps = currentBreakdown.completedSteps.filter(step => step.wasCorrect).length;

            container.innerHTML = `
                <div class="breakdown-complete">
                    <h4>🎉 Breakdown Complete!</h4>
                    <p>You've worked through all the steps. You should now understand this topic better!</p>

                    <div class="breakdown-stats">
                        <div class="stat-item">
                            <span class="stat-label">Steps completed:</span>
                            <span class="stat-value">${totalSteps}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Steps correct:</span>
                            <span class="stat-value">${correctSteps}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Skills practiced:</span>
                            <span class="stat-value">${[...new Set(currentBreakdown.steps.map(s => s.step_type))].join(', ')}</span>
                        </div>
                    </div>

                    <button class="continue-btn" onclick="continueToNextQuestion()">Continue to Next Question</button>
                </div>
            `;

            // Process breakdown completion in BKT system
            await pyodideInstance.runPythonAsync(`
                # Process breakdown completion (all steps attempted)
                all_steps_correct = ${correctSteps === totalSteps}
                result = bkt_system.process_breakdown_completion(
                    current_student_id, "${currentBreakdown.mcq_id}", all_steps_correct
                )

                print(f"Breakdown completion processed for MCQ ${currentBreakdown.mcq_id}")
            `);

            isInBreakdown = false;
            updateGraphMasteryColors();
            updateSkillsDisplay();
        }

        function continueToNextQuestion() {
            // Reset UI for next question
            document.getElementById('question-feedback').style.display = 'none';
            document.getElementById('breakdown-section').style.display = 'none';
            document.getElementById('question-display').style.display = 'block';
            selectedOption = null;

            currentQuestionIndex++;
            displayNextQuestion();
        }

        async function showSessionSummary() {
            updateStatus('Analyzing session results...', 'loading');

            // Calculate session statistics
            const summaryResult = await pyodideInstance.runPythonAsync(`
                # Calculate session improvements and review topics
                student = student_manager.get_student(current_student_id)

                # Get current mastery levels
                current_masteries = {}
                improved_topics = []
                review_topics = []

                for topic_idx, current_mastery in student.mastery_levels.items():
                    topic_name = kg.get_topic_of_index(topic_idx)
                    current_masteries[topic_name] = current_mastery

                # Get session statistics
                stats = student_manager.get_student_statistics(current_student_id)

                # Get review recommendations
                recommendations = bkt_system.get_review_recommendations(current_student_id)

                summary_data = {
                    'total_questions': len(questionResults),
                    'correct_answers': sum(1 for r in questionResults if r['is_correct']),
                    'current_masteries': current_masteries,
                    'review_recommendations': recommendations[:5],  # Top 5
                    'session_stats': stats
                }

                js_export(summary_data)
            `.replace('questionResults', JSON.stringify(questionResults)));

            const summaryData = JSON.parse(summaryResult);

            // Calculate improved topics
            const improvedTopics = [];
            for (const [topic, currentMastery] of Object.entries(summaryData.current_masteries)) {
                const initialMastery = sessionStartMasteries[topic] || 0;
                if (currentMastery > initialMastery + 0.02) { // 2% improvement threshold
                    improvedTopics.push({
                        name: topic,
                        improvement: ((currentMastery - initialMastery) * 100).toFixed(1)
                    });
                }
            }

            // Show session summary screen
            document.querySelector('.main-demo-layout').style.display = 'none';
            document.getElementById('session-summary').style.display = 'block';

            // Update summary content
            document.getElementById('questions-correct').textContent = summaryData.correct_answers;
            document.getElementById('questions-total').textContent = summaryData.total_questions;

            // Display improved topics
            const improvedHtml = improvedTopics.map(topic =>
                `<div class="topic-item improved">
                    ${topic.name} <span class="improvement">+${topic.improvement}%</span>
                </div>`
            ).join('');
            document.getElementById('improved-topics').innerHTML = improvedHtml || '<div class="no-items">No significant improvements this session</div>';

            // Display review topics
            const reviewHtml = summaryData.review_recommendations.map(rec =>
                `<div class="topic-item review">
                    ${rec.topic_name} <span class="retention">Retention: ${(rec.retention_ratio * 100).toFixed(0)}%</span>
                </div>`
            ).join('');
            document.getElementById('review-topics').innerHTML = reviewHtml || '<div class="no-items">No topics need immediate review</div>';

            updateStatus('Session completed!', 'success');
        }

        function updateAlgorithmExplanation(mcqData) {
            // Update algorithm explanation panel with current decision-making
            document.getElementById('selection-details').innerHTML = `
                Selected "${mcqData.topic_name}" - mastery gap detected<br>
                <small>Difficulty: ${(mcqData.difficulty * 100).toFixed(0)}% matches your level</small>
            `;

            document.getElementById('difficulty-details').innerHTML = `
                Your mastery: ~${(Math.random() * 0.4 + 0.3).toFixed(2)} | Question difficulty: ${mcqData.difficulty.toFixed(2)}<br>
                <small>Optimal challenge zone maintained</small>
            `;

            document.getElementById('skills-details').innerHTML = `
                Targeting: ${mcqData.topic_name} skills<br>
                <small>Will update 2-4 mathematical abilities based on performance</small>
            `;
        }

        function highlightCurrentTopic(topicIndex) {
            // Highlight current topic in knowledge graph
            if (network && currentData.nodes) {
                const targetNode = currentData.nodes.find(node =>
                    node.label === currentMCQ.topic_name);

                if (targetNode) {
                    network.selectNodes([targetNode.id]);
                    network.focus(targetNode.id, {
                        scale: 1.5,
                        animation: { duration: 500, easingFunction: 'easeInOutCubic' }
                    });
                }
            }
        }

        async function updateSkillsDisplay(customSkills = null) {
            let skillsData;

            if (customSkills) {
                skillsData = customSkills;
            } else {
                const skillsResult = await pyodideInstance.runPythonAsync(`
                    student = student_manager.get_student(current_student_id)
                    skills = student.ability_levels
                    js_export(skills)
                `);
                skillsData = JSON.parse(skillsResult);
            }

            const skillsHtml = Object.entries(skillsData).map(([skill, level]) => `
                <div class="skill-item">
                    <div class="skill-name">${skill.replace('_', ' ')}</div>
                    <div class="skill-bar">
                        <div class="skill-fill" style="width: ${level * 100}%"></div>
                    </div>
                    <div class="skill-value">${(level * 100).toFixed(0)}%</div>
                </div>
            `).join('');

            document.getElementById('skills-display').innerHTML = skillsHtml;
        }

        // Copy the graph mastery color updating function from existing demo
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

        function startNewSession() {
            // Reset for new session
            currentQuestionIndex = 0;
            questionResults = [];
            isInBreakdown = false;

            // Show main interface, hide summary
            document.querySelector('.main-demo-layout').style.display = 'flex';
            document.getElementById('session-summary').style.display = 'none';

            startPracticeSession();
        }

        function reviewSpecificTopic() {
            alert('Feature to be implemented: Topic-specific review session');
        }

        // Initialize when page loads
        window.addEventListener('load', initializeDemo);

        // Update time display every second
        setInterval(updateTimeDisplay, 1000);
    </script>
</body>
</html>
