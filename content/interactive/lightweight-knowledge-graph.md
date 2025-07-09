# Lightweight Knowledge Graph

This is a lightweight, interactive knowledge graph visualization built with pure JavaScript and HTML5 Canvas. It uses the same ontology data as the full system but with a much smaller footprint.

```{raw} html
<div style="text-align: center; margin: 20px 0;">
    <h2>🧠 Interactive Knowledge Graph</h2>
    <p>A lightweight visualization of mathematical concepts and their relationships</p>
</div>

<div style="text-align: center; margin: 20px 0;">
    <button onclick="graph.resetView()" style="background-color: #2196F3; color: white; border: none; padding: 10px 20px; margin: 5px; border-radius: 4px; cursor: pointer;">Reset View</button>
    <button onclick="graph.fitToView()" style="background-color: #4CAF50; color: white; border: none; padding: 10px 20px; margin: 5px; border-radius: 4px; cursor: pointer;">Fit to View</button>
</div>

<div style="text-align: center; margin: 20px 0;">
    <canvas id="lightweight-graph" style="border: 1px solid #ddd; border-radius: 4px;"></canvas>
</div>

<div id="graph-stats" style="background-color: #f5f5f5; border-radius: 4px; padding: 10px; margin: 10px 0; font-family: monospace; text-align: center;">
    Loading graph data...
</div>

<div style="background-color: #e3f2fd; border: 1px solid #2196F3; border-radius: 4px; padding: 15px; margin: 20px 0;">
    <strong>How to use:</strong>
    <ul>
        <li><strong>Drag:</strong> Pan around the graph</li>
        <li><strong>Scroll:</strong> Zoom in/out</li>
        <li><strong>Click:</strong> Select nodes to see details</li>
        <li><strong>Touch:</strong> Works on mobile devices</li>
    </ul>
</div>

<script src="../../_static/lightweight-graph.js"></script>
<script>
let graph;
let graphData;

// Load and initialize the graph
fetch('../../_static/lightweight-graph.json')
    .then(response => response.json())
    .then(data => {
        graphData = data;
        graph = new LightweightGraph('lightweight-graph', data);
        
        // Update stats
        updateStats();
        
        // Auto-fit to view
        setTimeout(() => graph.fitToView(), 100);
    })
    .catch(error => {
        console.error('Error loading graph data:', error);
        document.getElementById('graph-stats').innerHTML = 'Error loading graph data: ' + error.message;
    });

function updateStats() {
    if (graphData) {
        const stats = document.getElementById('graph-stats');
        stats.innerHTML = `
            <strong>Graph Statistics:</strong><br>
            Nodes: ${graphData.nodes.length} | 
            Edges: ${graphData.edges.length} | 
            Strands: ${graphData.metadata.strands.join(', ')}
        `;
    }
}
</script>
```

## Features

### ✅ **Ultra-Lightweight**
- **No external dependencies** - Pure JavaScript and HTML5 Canvas
- **~5KB total size** (vs 200KB+ for vis.js)
- **Instant loading** - No library downloads required

### ✅ **Interactive**
- **Zoom and pan** with mouse and touch
- **Node selection** with detailed information display
- **Hover effects** for better user experience
- **Mobile-friendly** touch controls

### ✅ **Data-Driven**
- Uses the same **ontology data** as the full system
- **Color-coded by math strand** (Algebra, Geometry, Calculus, etc.)
- **Directed edges** showing prerequisite relationships
- **100 nodes sampled** for optimal performance

### ✅ **Customizable**
- Easy to modify colors, sizes, and interactions
- Simple API for external control
- Can be easily integrated into any web page

## Technical Details

The visualization consists of three main components:

1. **Data Processor** (`lightweight_graph_processor.py`)
   - Reads ontology CSV files
   - Creates minimal JSON format
   - Positions nodes by strand groups

2. **Canvas Renderer** (`lightweight-graph.js`)
   - Pure JavaScript implementation
   - Handles all interactions
   - Renders nodes, edges, and UI elements

3. **Integration** (This page)
   - Simple HTML wrapper
   - Loads data and initializes visualization
   - Provides user controls

## Performance Comparison

| Feature | Vis.js | Lightweight |
|---------|--------|-------------|
| Library Size | ~200KB | ~5KB |
| Dependencies | 1 external | 0 |
| Load Time | ~2-3s | ~0.1s |
| Memory Usage | High | Low |
| Customization | Limited | Full control |

This lightweight approach provides excellent performance while maintaining all the essential features needed for knowledge graph exploration. 