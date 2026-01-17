# Chemistry Knowledge Graph

This interactive visualization shows the relationships between chemistry concepts in the Leaving Certificate curriculum. Each node represents a chemistry concept, and the connections show prerequisite relationships.

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

// Group color mapping for chemistry strands
function getGroupColor(group) {
    const colors = {
        'Periodic Table and Atomic Structure': '#ff7675',
        'Chemical Bonding': '#74b9ff',
        'Stoichiometry, Formulas and Equations': '#00b894',
        'Organic Chemistry': '#fdcb6e',
        'Rates of Reaction': '#e17055',
        'Chemical Equilibrium': '#a29bfe',
        'Acids and Bases': '#fd79a8',
        'Oxidation and Reduction': '#00cec9',
        'Electrochemistry': '#6c5ce7',
        'Environmental Chemistry': '#55a3ff',
        'Industrial Chemistry': '#e84393',
        'Fuels and Thermochemistry': '#f39c12'
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
    loadGraphData('../_static/graph-data-chem.json');
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
            // Fallback to simplified data
            loadSimplifiedFallback();
        });
}

function loadSimplifiedFallback() {
    // Fallback data if JSON files can't be loaded
    const fallbackData = {
        nodes: [
            {id: '1', label: 'Atomic Structure', group: 'Periodic Table and Atomic Structure', title: 'Structure of atoms including protons, neutrons, electrons'},
            {id: '2', label: 'Electron Configuration', group: 'Periodic Table and Atomic Structure', title: 'Arrangement of electrons in atomic orbitals'},
            {id: '3', label: 'Periodic Trends', group: 'Periodic Table and Atomic Structure', title: 'Patterns in properties across the periodic table'},
            {id: '4', label: 'Chemical Bonding', group: 'Chemical Bonding', title: 'How atoms combine to form compounds'},
            {id: '5', label: 'The Mole', group: 'Stoichiometry, Formulas and Equations', title: 'Avogadro\'s number and molar calculations'},
            {id: '6', label: 'Balancing Equations', group: 'Stoichiometry, Formulas and Equations', title: 'Conservation of mass in chemical equations'},
            {id: '7', label: 'Organic Chemistry', group: 'Organic Chemistry', title: 'Chemistry of carbon compounds'},
            {id: '8', label: 'Rates of Reaction', group: 'Rates of Reaction', title: 'Factors affecting reaction speed'}
        ],
        edges: [
            {from: '1', to: '2', title: 'Atomic structure determines electron configuration'},
            {from: '2', to: '3', title: 'Electron configuration explains periodic trends'},
            {from: '2', to: '4', title: 'Electron configuration determines bonding'},
            {from: '1', to: '5', title: 'Atomic mass relates to molar calculations'},
            {from: '5', to: '6', title: 'Mole concept needed for balancing equations'},
            {from: '4', to: '7', title: 'Bonding principles apply to organic compounds'}
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