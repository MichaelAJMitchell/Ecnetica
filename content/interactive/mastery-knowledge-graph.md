# Mastery-Aware Knowledge Graph

This is a lightweight, high-performance knowledge graph visualization that displays student mastery levels for each mathematical concept. It reads your `graph-data.json` directly without any conversion and renders quickly even with large datasets.

```{raw} html
<div style="text-align: center; margin: 20px 0;">
    <h2>🧠 Mastery-Aware Knowledge Graph</h2>
    <p>Interactive visualization showing mathematical concepts with mastery levels</p>
</div>

<div style="text-align: center; margin: 20px 0;">
    <button onclick="graph.resetView()" style="background-color: #2196F3; color: white; border: none; padding: 10px 20px; margin: 5px; border-radius: 4px; cursor: pointer;">Reset View</button>
    <button onclick="graph.fitToView()" style="background-color: #4CAF50; color: white; border: none; padding: 10px 20px; margin: 5px; border-radius: 4px; cursor: pointer;">Fit to View</button>
    <button onclick="randomizeMastery()" style="background-color: #FF9800; color: white; border: none; padding: 10px 20px; margin: 5px; border-radius: 4px; cursor: pointer;">Randomize Mastery</button>
    <button onclick="clearMastery()" style="background-color: #9E9E9E; color: white; border: none; padding: 10px 20px; margin: 5px; border-radius: 4px; cursor: pointer;">Clear Mastery</button>
</div>

<div style="text-align: center; margin: 20px 0;">
    <canvas id="mastery-graph" style="border: 1px solid #ddd; border-radius: 4px; width: 100%; height: 600px; background-color: #fafafa;"></canvas>
</div>

<div style="background-color: #e3f2fd; border: 1px solid #2196F3; border-radius: 8px; padding: 15px; margin: 20px 0;">
    <h3 style="margin-top: 0; color: #1976D2;">Mastery Level Controls</h3>
    <p>Adjust the mastery levels for different concept groups:</p>
    
    <div style="margin: 10px 0;">
        <label for="algebra-mastery" style="display: inline-block; width: 120px; font-weight: bold;">Algebra:</label>
        <input type="range" id="algebra-mastery" min="0" max="100" value="75" oninput="updateGroupMastery('Algebra', this.value)" style="width: 200px; margin: 0 10px;">
        <span id="algebra-value" style="font-weight: bold; color: #1976D2;">75%</span>
    </div>
    
    <div style="margin: 10px 0;">
        <label for="geometry-mastery" style="display: inline-block; width: 120px; font-weight: bold;">Geometry:</label>
        <input type="range" id="geometry-mastery" min="0" max="100" value="60" oninput="updateGroupMastery('Geometry', this.value)" style="width: 200px; margin: 0 10px;">
        <span id="geometry-value" style="font-weight: bold; color: #1976D2;">60%</span>
    </div>
    
    <div style="margin: 10px 0;">
        <label for="trigonometry-mastery" style="display: inline-block; width: 120px; font-weight: bold;">Trigonometry:</label>
        <input type="range" id="trigonometry-mastery" min="0" max="100" value="45" oninput="updateGroupMastery('Trigonometry', this.value)" style="width: 200px; margin: 0 10px;">
        <span id="trigonometry-value" style="font-weight: bold; color: #1976D2;">45%</span>
    </div>
    
    <div style="margin: 10px 0;">
        <label for="calculus-mastery" style="display: inline-block; width: 120px; font-weight: bold;">Calculus:</label>
        <input type="range" id="calculus-mastery" min="0" max="100" value="30" oninput="updateGroupMastery('Calculus', this.value)" style="width: 200px; margin: 0 10px;">
        <span id="calculus-value" style="font-weight: bold; color: #1976D2;">30%</span>
    </div>
</div>

<div id="graph-stats" style="background-color: #f5f5f5; border-radius: 4px; padding: 15px; margin: 10px 0; text-align: center;">
    <h3 style="margin-top: 0; color: #495057;">Graph Statistics</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-top: 15px;">
        <div style="background: white; padding: 10px; border-radius: 4px; border: 1px solid #dee2e6;">
            <div style="font-size: 24px; font-weight: bold; color: #2196F3;" id="total-nodes">0</div>
            <div style="font-size: 14px; color: #6c757d;">Total Nodes</div>
        </div>
        <div style="background: white; padding: 10px; border-radius: 4px; border: 1px solid #dee2e6;">
            <div style="font-size: 24px; font-weight: bold; color: #2196F3;" id="total-edges">0</div>
            <div style="font-size: 14px; color: #6c757d;">Total Edges</div>
        </div>
        <div style="background: white; padding: 10px; border-radius: 4px; border: 1px solid #dee2e6;">
            <div style="font-size: 24px; font-weight: bold; color: #00b894;" id="mastered-nodes">0</div>
            <div style="font-size: 14px; color: #6c757d;">Mastered</div>
        </div>
        <div style="background: white; padding: 10px; border-radius: 4px; border: 1px solid #dee2e6;">
            <div style="font-size: 24px; font-weight: bold; color: #fdcb6e;" id="learning-nodes">0</div>
            <div style="font-size: 14px; color: #6c757d;">Learning</div>
        </div>
        <div style="background: white; padding: 10px; border-radius: 4px; border: 1px solid #dee2e6;">
            <div style="font-size: 24px; font-weight: bold; color: #e17055;" id="struggling-nodes">0</div>
            <div style="font-size: 14px; color: #6c757d;">Struggling</div>
        </div>
        <div style="background: white; padding: 10px; border-radius: 4px; border: 1px solid #dee2e6;">
            <div style="font-size: 24px; font-weight: bold; color: #636e72;" id="unknown-nodes">0</div>
            <div style="font-size: 14px; color: #6c757d;">Unknown</div>
        </div>
    </div>
</div>

<div style="background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; padding: 15px; margin: 20px 0;">
    <h3 style="margin-top: 0; color: #856404;">How to use:</h3>
    <ul style="margin-bottom: 0;">
        <li><strong>Drag:</strong> Pan around the graph</li>
        <li><strong>Scroll:</strong> Zoom in/out</li>
        <li><strong>Click:</strong> Select nodes to see details</li>
        <li><strong>Adjust mastery:</strong> Use sliders above to simulate different mastery levels</li>
        <li><strong>Touch:</strong> Works on mobile devices</li>
    </ul>
</div>
```

## Features

### 🚀 **High Performance**
- **Canvas-based rendering** - No DOM manipulation overhead
- **Viewport culling** - Only renders visible nodes
- **Optimized layout** - Fast force-directed algorithm
- **Memory efficient** - Minimal data structures

### 🎯 **Mastery Visualization**
- **Color-coded nodes** - Green (mastered), yellow (learning), red (struggling)
- **Real-time updates** - Instant mastery level changes
- **Group controls** - Adjust mastery by subject area
- **Statistics panel** - Live mastery distribution

### 📊 **Rich Data Display**
- **All metadata preserved** - Uses your complete `graph-data.json`
- **Node details** - Click to see concept information
- **Mastery legend** - Clear color coding explanation
- **Interactive controls** - Reset, fit, randomize, clear

### 📱 **Mobile Friendly**
- **Touch support** - Works on tablets and phones
- **Responsive design** - Adapts to screen size
- **High DPI support** - Crisp rendering on all devices

## Technical Details

### Data Source
- **Direct loading** - Reads `Ontology/ontology_builder/graph-data.json`
- **No conversion** - Uses your data structure as-is
- **All fields preserved** - `broader_concept`, `grade_level`, `difficulty`, `strength`

### Performance Optimizations
- **Viewport culling** - Only renders nodes in view
- **Node limit** - Maximum 500 visible nodes for smooth rendering
- **Efficient layout** - 50 iterations of force simulation
- **Canvas optimization** - High DPI support, efficient drawing

### Mastery Integration
- **Flexible data** - Accepts any mastery data format
- **Real-time updates** - `updateMastery()` method for live changes
- **Color blending** - Combines subject colors with mastery colors
- **Statistics tracking** - Automatic mastery level counting

## Usage

```javascript
// Initialize with mastery data
const masteryData = {
    'node-id-1': 0.85,  // 85% mastery
    'node-id-2': 0.45,  // 45% mastery
    'node-id-3': 0.20   // 20% mastery
};

const graph = new MasteryGraph('canvas-id', masteryData);

// Update mastery levels
graph.updateMastery({
    'node-id-4': 0.90,
    'node-id-5': 0.30
});

// Select a node
graph.selectNode('node-id-1');

// Reset view
graph.resetView();
```

## Integration with BKT System

This visualization can be easily integrated with your BKT/MCQ system:

```javascript
// Get mastery data from BKT system
const bktMastery = studentManager.getStudentMastery(studentId);

// Update visualization
graph.updateMastery(bktMastery);

// Highlight struggling concepts
const strugglingNodes = Object.keys(bktMastery)
    .filter(nodeId => bktMastery[nodeId] < 0.4);
```

The mastery-aware graph provides a powerful way to visualize student progress and identify areas that need attention, all while maintaining the rich metadata from your knowledge graph.
