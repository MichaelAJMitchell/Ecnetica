# Mathematics Knowledge Graph

This interactive visualization shows the relationships between mathematical concepts in the Leaving Certificate curriculum. Each node represents a mathematical concept, and the connections show prerequisite relationships.

<div id="graph-container" style="width: 100%; height: 600px; border: 1px solid #ddd; border-radius: 4px;"></div>

<div id="controls" style="margin-top: 20px;">
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
  
  <button id="reset-view" style="margin-left: 10px;">Reset View</button>
  <button id="toggle-physics" style="margin-left: 10px;">Toggle Physics</button>
  <button id="load-simplified" style="margin-left: 10px;">Load Simplified (50 nodes)</button>
  <button id="load-full" style="margin-left: 10px;">Load Full (457 nodes)</button>
</div>

<div id="node-info" style="margin-top: 20px; padding: 10px; background-color: #f8f9fa; border-radius: 4px; display: none;">
  <h4 id="node-title"></h4>
  <p id="node-description"></p>
  <p><strong>Strand:</strong> <span id="node-strand"></span></p>
</div>

<div id="stats" style="margin-top: 20px; padding: 10px; background-color: #e9ecef; border-radius: 4px;">
  <strong>Graph Statistics:</strong> <span id="node-count">0</span> nodes, <span id="edge-count">0</span> edges
</div>

<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
<script>
// Global variables
let network;
let currentData = {nodes: [], edges: []};

// Group color mapping
function getGroupColor(group) {
    const colors = {
        'Algebra': '#ff7675',
        'Geometry': '#74b9ff',
        'Trigonometry': '#55a3ff',
        'Calculus': '#fd79a8',
        'Number': '#00b894',
        'Statistics': '#fdcb6e',
        'Probability': '#e17055',
        'Coordinate Geometry': '#a29bfe',
        'Functions': '#fd79a8',
        'Sequences and Series': '#00cec9',
        'Complex Numbers': '#6c5ce7',
        'Measurement': '#fdcb6e',
        'Synthetic geometry': '#74b9ff',
        'Transformation geometry': '#55a3ff',
        'Differential Calculus': '#fd79a8',
        'Integral Calculus': '#e84393',
        'Counting and Probability': '#e17055'
    };
    return colors[group] || '#636e72';
}

// Load and process the knowledge graph data
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the network
    const container = document.getElementById('graph-container');
    
    // Network options
    const options = {
        nodes: {
            shape: 'dot',
            size: 25,
            font: {
                size: 12,
                face: 'Arial'
            },
            borderWidth: 2,
            shadow: true
        },
        edges: {
            width: 1,
            shadow: true,
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
        this.textContent = physicsEnabled ? 'Disable Physics' : 'Enable Physics';
    });

    // Load simplified data
    document.getElementById('load-simplified').addEventListener('click', function() {
        loadGraphData('/_static/graph-data-simplified.json');
    });

    // Load full data
    document.getElementById('load-full').addEventListener('click', function() {
        loadGraphData('/_static/graph-data.json');
    });

    // Load full data by default
    loadGraphData('/_static/graph-data.json');
});

function loadGraphData(filename) {
    fetch(filename)
        .then(response => response.json())
        .then(data => {
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
            
            // Apply group-based positioning and colors
            data.nodes.forEach(node => {
                // Add color based on group
                node.color = getGroupColor(node.group);
                
                // Add initial positioning with some randomness
                if (groupPositions[node.group]) {
                    node.x = groupPositions[node.group].x + (Math.random() - 0.5) * 150;
                    node.y = groupPositions[node.group].y + (Math.random() - 0.5) * 150;
                } else {
                    // Random positioning for unknown groups
                    node.x = (Math.random() - 0.5) * 800;
                    node.y = (Math.random() - 0.5) * 800;
                }
            });
            
            currentData = data;
            network.setData(data);
            updateStats(data.nodes.length, data.edges.length);
            
            // Update strand filter options based on available data
            const strands = [...new Set(data.nodes.map(node => node.group))].sort();
            const filter = document.getElementById('strand-filter');
            filter.innerHTML = '<option value="">All Strands</option>';
            strands.forEach(strand => {
                if (strand && strand !== 'Unknown') {
                    filter.innerHTML += `<option value="${strand}">${strand}</option>`;
                }
            });
            
            console.log(`Loaded ${data.nodes.length} nodes and ${data.edges.length} edges from ${filename}`);
        })
        .catch(error => {
            console.error('Error loading graph data:', error);
            // Fallback to simplified data
            loadSimplifiedFallback();
        });
}

function loadSimplifiedFallback() {
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
    
    currentData = fallbackData;
    network.setData(fallbackData);
    updateStats(fallbackData.nodes.length, fallbackData.edges.length);
}

function updateStats(nodeCount, edgeCount) {
    document.getElementById('node-count').textContent = nodeCount;
    document.getElementById('edge-count').textContent = edgeCount;
}
</script> 