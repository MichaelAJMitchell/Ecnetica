# Physics Knowledge Graph

This interactive visualization shows the relationships between physics concepts in the Leaving Certificate curriculum. Each node represents a physics concept, and the connections show prerequisite relationships.

<div id="graph-container" style="width: 100%; height: 600px; border: 1px solid #ddd; border-radius: 4px;"></div>

<div id="controls" style="margin-top: 20px;">
  <label for="strand-filter">Filter by Strand: </label>
  <select id="strand-filter">
    <option value="">All Strands</option>
  </select>
  
  <button id="reset-view" style="margin-left: 10px;">Reset View</button>
  <button id="toggle-physics" style="margin-left: 10px;">Toggle Physics</button>
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

// Group color mapping for physics strands
function getGroupColor(group) {
    const colors = {
        'Mechanics': '#ff7675',
        'Heat': '#fdcb6e',
        'Waves': '#74b9ff',
        'Electricity': '#00b894',
        'Magnetism': '#a29bfe',
        'Modern Physics': '#fd79a8',
        'Atomic Physics': '#6c5ce7',
        'Nuclear Physics': '#e17055',
        'Particle Physics': '#00cec9',
        'Light': '#55a3ff',
        'Sound': '#e84393'
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
                document.getElementById('node-description').textContent = node.title || 'No description available';
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

    // Load graph data - path is relative from content/ to _static/
    loadGraphData('../_static/graph-data-physics.json');
});

function loadGraphData(filename) {
    fetch(filename)
        .then(response => response.json())
        .then(rawData => {
            // Transform the data from concepts/relationships format to nodes/edges format
            const nodes = (rawData.concepts || []).map(concept => ({
                id: concept.id,
                label: concept.name,
                group: concept.strand,
                title: concept.explanation || concept.name
            }));
            
            const edges = (rawData.relationships || []).map(rel => ({
                from: rel.prerequisite_concept_id,
                to: rel.dependent_concept_id,
                title: rel.relationship_type || ''
            }));
            
            const data = { nodes, edges };
            
            // Apply group-based positioning and colors
            data.nodes.forEach(node => {
                // Add color based on group
                node.color = getGroupColor(node.group);
                
                // Random positioning for groups
                node.x = (Math.random() - 0.5) * 800;
                node.y = (Math.random() - 0.5) * 800;
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
            loadSimplifiedFallback();
        });
}

function loadSimplifiedFallback() {
    // Fallback data if JSON files can't be loaded
    const fallbackData = {
        nodes: [
            {id: '1', label: 'Kinematics', group: 'Mechanics', title: 'Study of motion'},
            {id: '2', label: 'Forces', group: 'Mechanics', title: 'Newton\'s Laws'},
            {id: '3', label: 'Energy', group: 'Mechanics', title: 'Work and Energy'},
            {id: '4', label: 'Heat Transfer', group: 'Heat', title: 'Conduction, convection, radiation'},
            {id: '5', label: 'Wave Properties', group: 'Waves', title: 'Frequency, wavelength, amplitude'},
            {id: '6', label: 'Electric Circuits', group: 'Electricity', title: 'Current, voltage, resistance'},
            {id: '7', label: 'Magnetic Fields', group: 'Magnetism', title: 'Field lines and forces'},
            {id: '8', label: 'Atomic Structure', group: 'Modern Physics', title: 'Electrons, protons, neutrons'}
        ],
        edges: [
            {from: '1', to: '2', title: 'Motion leads to Forces'},
            {from: '2', to: '3', title: 'Forces do Work'},
            {from: '5', to: '4', title: 'Thermal radiation is a wave'},
            {from: '6', to: '7', title: 'Current creates magnetic fields'},
            {from: '6', to: '8', title: 'Atomic structure explains conductivity'}
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

