/**
 * Mastery-Aware Knowledge Graph Renderer
 * Lightweight canvas-based visualization with mastery level display
 * Reads graph-data.json directly without conversion
 */

class MasteryGraph {
    constructor(canvasId, masteryData = {}) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.masteryData = masteryData; // {nodeId: masteryPercentage}
        
        // Viewport settings
        this.scale = 1;
        this.offsetX = 0;
        this.offsetY = 0;
        
        // Interaction state
        this.isDragging = false;
        this.lastX = 0;
        this.lastY = 0;
        this.hoveredNode = null;
        this.selectedNode = null;
        
        // Performance settings
        this.maxVisibleNodes = 500; // Limit rendering for performance
        this.nodeRadius = 8;
        this.edgeWidth = 1;
        
        // Visual settings
        this.nodeColors = {
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
            'Counting and Probability': '#e17055',
            'Other': '#636e72'
        };
        
        // Mastery color mapping
        this.masteryColors = {
            mastered: '#00b894',    // Green
            learning: '#fdcb6e',    // Yellow
            struggling: '#e17055',  // Red
            unknown: '#636e72'      // Gray
        };
        
        this.data = null;
        this.visibleNodes = [];
        this.visibleEdges = [];
        
        this.setupCanvas();
        this.setupEvents();
        this.loadData();
    }
    
    setupCanvas() {
        // Set canvas size
        this.canvas.width = this.canvas.offsetWidth;
        this.canvas.height = this.canvas.offsetHeight;
        
        // High DPI support
        const dpr = window.devicePixelRatio || 1;
        this.canvas.width *= dpr;
        this.canvas.height *= dpr;
        this.ctx.scale(dpr, dpr);
        this.canvas.style.width = this.canvas.offsetWidth + 'px';
        this.canvas.style.height = this.canvas.offsetHeight + 'px';
    }
    
    setupEvents() {
        // Mouse events
        this.canvas.addEventListener('mousedown', (e) => this.handleMouseDown(e));
        this.canvas.addEventListener('mousemove', (e) => this.handleMouseMove(e));
        this.canvas.addEventListener('mouseup', () => this.handleMouseUp());
        this.canvas.addEventListener('wheel', (e) => this.handleWheel(e));
        
        // Touch events for mobile
        this.canvas.addEventListener('touchstart', (e) => this.handleTouchStart(e));
        this.canvas.addEventListener('touchmove', (e) => this.handleTouchMove(e));
        this.canvas.addEventListener('touchend', () => this.handleTouchEnd());
        
        // Window resize
        window.addEventListener('resize', () => this.setupCanvas());
    }
    
    async loadData() {
        try {
            // Try multiple possible paths for the graph data
            const possiblePaths = [
                '../Ontology/ontology_builder/graph-data.json',
                'Ontology/ontology_builder/graph-data.json',
                '../../Ontology/ontology_builder/graph-data.json',
                '/Ontology/ontology_builder/graph-data.json',
                'graph-data.json',
                '../graph-data.json'
            ];
            
            let data = null;
            for (const path of possiblePaths) {
                try {
                    const response = await fetch(path);
                    if (response.ok) {
                        data = await response.json();
                        console.log(`Successfully loaded graph data from: ${path}`);
                        break;
                    }
                } catch (e) {
                    console.log(`Failed to load from ${path}:`, e.message);
                }
            }
            
            if (!data) {
                throw new Error('Could not find graph-data.json in any expected location');
            }
            
            this.data = data;
            this.initializeLayout();
            this.render();
        } catch (error) {
            console.error('Failed to load graph data:', error);
            this.renderError('Failed to load graph data. Please ensure graph-data.json exists in the Ontology/ontology_builder/ directory.');
        }
    }
    
    initializeLayout() {
        if (!this.data || !this.data.nodes) return;
        
        const nodes = this.data.nodes;
        const edges = this.data.edges || [];
        
        // Simple force-directed layout for performance
        this.nodes = nodes.map(node => ({
            ...node,
            x: Math.random() * this.canvas.width,
            y: Math.random() * this.canvas.height,
            vx: 0,
            vy: 0
        }));
        
        this.edges = edges.map(edge => ({
            ...edge,
            source: this.nodes.find(n => n.id === edge.from),
            target: this.nodes.find(n => n.id === edge.to)
        })).filter(edge => edge.source && edge.target);
        
        // Run layout simulation
        this.runLayoutSimulation(50); // Fewer iterations for speed
    }
    
    runLayoutSimulation(iterations) {
        const k = Math.sqrt((this.canvas.width * this.canvas.height) / this.nodes.length);
        const force = 0.1;
        
        for (let i = 0; i < iterations; i++) {
            // Repulsion between nodes
            for (let j = 0; j < this.nodes.length; j++) {
                for (let k = j + 1; k < this.nodes.length; k++) {
                    const dx = this.nodes[j].x - this.nodes[k].x;
                    const dy = this.nodes[j].y - this.nodes[k].y;
                    const distance = Math.sqrt(dx * dx + dy * dy);
                    
                    if (distance > 0) {
                        const repulsion = (k * k) / distance;
                        const fx = (dx / distance) * repulsion * force;
                        const fy = (dy / distance) * repulsion * force;
                        
                        this.nodes[j].vx += fx;
                        this.nodes[j].vy += fy;
                        this.nodes[k].vx -= fx;
                        this.nodes[k].vy -= fy;
                    }
                }
            }
            
            // Attraction along edges
            this.edges.forEach(edge => {
                const dx = edge.target.x - edge.source.x;
                const dy = edge.target.y - edge.source.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance > 0) {
                    const attraction = (distance * distance) / k * force;
                    const fx = (dx / distance) * attraction;
                    const fy = (dy / distance) * attraction;
                    
                    edge.source.vx += fx;
                    edge.source.vy += fy;
                    edge.target.vx -= fx;
                    edge.target.vy -= fy;
                }
            });
            
            // Update positions
            this.nodes.forEach(node => {
                node.vx *= 0.9; // Damping
                node.vy *= 0.9;
                node.x += node.vx;
                node.y += node.vy;
                
                // Keep nodes in bounds
                node.x = Math.max(50, Math.min(this.canvas.width - 50, node.x));
                node.y = Math.max(50, Math.min(this.canvas.height - 50, node.y));
            });
        }
    }
    
    getMasteryLevel(nodeId) {
        const mastery = this.masteryData[nodeId];
        if (mastery === undefined) return 'unknown';
        if (mastery >= 0.8) return 'mastered';
        if (mastery >= 0.4) return 'learning';
        return 'struggling';
    }
    
    getNodeColor(node) {
        const masteryLevel = this.getMasteryLevel(node.id);
        const baseColor = this.nodeColors[node.group] || this.nodeColors['Other'];
        
        if (masteryLevel === 'unknown') {
            return baseColor;
        }
        
        // Blend base color with mastery color
        const masteryColor = this.masteryColors[masteryLevel];
        return this.blendColors(baseColor, masteryColor, 0.3);
    }
    
    blendColors(color1, color2, ratio) {
        const hex1 = color1.replace('#', '');
        const hex2 = color2.replace('#', '');
        
        const r1 = parseInt(hex1.substr(0, 2), 16);
        const g1 = parseInt(hex1.substr(2, 2), 16);
        const b1 = parseInt(hex1.substr(4, 2), 16);
        
        const r2 = parseInt(hex2.substr(0, 2), 16);
        const g2 = parseInt(hex2.substr(2, 2), 16);
        const b2 = parseInt(hex2.substr(4, 2), 16);
        
        const r = Math.round(r1 * (1 - ratio) + r2 * ratio);
        const g = Math.round(g1 * (1 - ratio) + g2 * ratio);
        const b = Math.round(b1 * (1 - ratio) + b2 * ratio);
        
        return `rgb(${r}, ${g}, ${b})`;
    }
    
    getVisibleNodes() {
        if (!this.nodes) return [];
        
        // Simple viewport culling for performance
        const margin = 100;
        return this.nodes.filter(node => 
            node.x >= -margin && node.x <= this.canvas.width + margin &&
            node.y >= -margin && node.y <= this.canvas.height + margin
        ).slice(0, this.maxVisibleNodes);
    }
    
    getVisibleEdges() {
        if (!this.edges) return [];
        
        const visibleNodeIds = new Set(this.getVisibleNodes().map(n => n.id));
        return this.edges.filter(edge => 
            visibleNodeIds.has(edge.from) && visibleNodeIds.has(edge.to)
        );
    }
    
    render() {
        if (!this.data) return;
        
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Get visible elements
        this.visibleNodes = this.getVisibleNodes();
        this.visibleEdges = this.getVisibleEdges();
        
        // Apply viewport transform
        this.ctx.save();
        this.ctx.translate(this.offsetX, this.offsetY);
        this.ctx.scale(this.scale, this.scale);
        
        // Render edges
        this.renderEdges();
        
        // Render nodes
        this.renderNodes();
        
        this.ctx.restore();
        
        // Render UI
        this.renderUI();
    }
    
    renderEdges() {
        this.ctx.strokeStyle = '#ddd';
        this.ctx.lineWidth = this.edgeWidth;
        
        this.visibleEdges.forEach(edge => {
            if (edge.source && edge.target) {
                this.ctx.beginPath();
                this.ctx.moveTo(edge.source.x, edge.source.y);
                this.ctx.lineTo(edge.target.x, edge.target.y);
                this.ctx.stroke();
            }
        });
    }
    
    renderNodes() {
        this.visibleNodes.forEach(node => {
            const x = node.x;
            const y = node.y;
            const radius = this.nodeRadius;
            
            // Node color based on mastery
            const color = this.getNodeColor(node);
            
            // Draw node
            this.ctx.fillStyle = color;
            this.ctx.beginPath();
            this.ctx.arc(x, y, radius, 0, 2 * Math.PI);
            this.ctx.fill();
            
            // Node border
            this.ctx.strokeStyle = '#fff';
            this.ctx.lineWidth = 2;
            this.ctx.stroke();
            
            // Highlight selected/hovered nodes
            if (node === this.selectedNode || node === this.hoveredNode) {
                this.ctx.strokeStyle = '#333';
                this.ctx.lineWidth = 3;
                this.ctx.stroke();
            }
        });
    }
    
    renderUI() {
        // Render node info panel
        if (this.selectedNode) {
            this.renderNodeInfo(this.selectedNode);
        }
        
        // Render mastery legend
        this.renderMasteryLegend();
    }
    
    renderNodeInfo(node) {
        const mastery = this.masteryData[node.id];
        const masteryLevel = this.getMasteryLevel(node.id);
        
        // Create info panel
        const panel = document.getElementById('node-info') || this.createInfoPanel();
        
        panel.innerHTML = `
            <h4>${node.label}</h4>
            <p><strong>Group:</strong> ${node.group}</p>
            <p><strong>Difficulty:</strong> ${node.difficulty || 'Unknown'}</p>
            <p><strong>Grade Level:</strong> ${node.grade_level || 'Unknown'}</p>
            <p><strong>Mastery:</strong> ${mastery !== undefined ? Math.round(mastery * 100) + '%' : 'Unknown'}</p>
            <p><strong>Status:</strong> ${masteryLevel}</p>
            ${node.title ? `<p><strong>Description:</strong> ${node.title}</p>` : ''}
        `;
        
        panel.style.display = 'block';
    }
    
    createInfoPanel() {
        const panel = document.createElement('div');
        panel.id = 'node-info';
        panel.style.cssText = `
            position: absolute;
            top: 20px;
            right: 20px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            max-width: 300px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            display: none;
            z-index: 1000;
        `;
        document.body.appendChild(panel);
        return panel;
    }
    
    renderMasteryLegend() {
        const legend = document.getElementById('mastery-legend') || this.createLegend();
        
        legend.innerHTML = `
            <div style="display: flex; gap: 15px; align-items: center;">
                <div style="display: flex; align-items: center; gap: 5px;">
                    <div style="width: 12px; height: 12px; background: ${this.masteryColors.mastered}; border-radius: 50%;"></div>
                    <span>Mastered (80%+)</span>
                </div>
                <div style="display: flex; align-items: center; gap: 5px;">
                    <div style="width: 12px; height: 12px; background: ${this.masteryColors.learning}; border-radius: 50%;"></div>
                    <span>Learning (40-79%)</span>
                </div>
                <div style="display: flex; align-items: center; gap: 5px;">
                    <div style="width: 12px; height: 12px; background: ${this.masteryColors.struggling}; border-radius: 50%;"></div>
                    <span>Struggling (0-39%)</span>
                </div>
                <div style="display: flex; align-items: center; gap: 5px;">
                    <div style="width: 12px; height: 12px; background: ${this.masteryColors.unknown}; border-radius: 50%;"></div>
                    <span>Unknown</span>
                </div>
            </div>
        `;
    }
    
    createLegend() {
        const legend = document.createElement('div');
        legend.id = 'mastery-legend';
        legend.style.cssText = `
            position: absolute;
            bottom: 20px;
            left: 20px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 1000;
        `;
        document.body.appendChild(legend);
        return legend;
    }
    
    renderError(message) {
        this.ctx.fillStyle = '#e17055';
        this.ctx.font = '16px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(message, this.canvas.width / 2, this.canvas.height / 2);
    }
    
    // Event handlers
    handleMouseDown(e) {
        this.isDragging = true;
        this.lastX = e.clientX;
        this.lastY = e.clientY;
        this.canvas.style.cursor = 'grabbing';
    }
    
    handleMouseMove(e) {
        if (this.isDragging) {
            const dx = e.clientX - this.lastX;
            const dy = e.clientY - this.lastY;
            this.offsetX += dx;
            this.offsetY += dy;
            this.lastX = e.clientX;
            this.lastY = e.clientY;
            this.render();
        } else {
            // Check for node hover
            const rect = this.canvas.getBoundingClientRect();
            const x = (e.clientX - rect.left - this.offsetX) / this.scale;
            const y = (e.clientY - rect.top - this.offsetY) / this.scale;
            
            const hovered = this.visibleNodes.find(node => {
                const dx = x - node.x;
                const dy = y - node.y;
                return Math.sqrt(dx * dx + dy * dy) <= this.nodeRadius;
            });
            
            if (hovered !== this.hoveredNode) {
                this.hoveredNode = hovered;
                this.canvas.style.cursor = hovered ? 'pointer' : 'default';
                this.render();
            }
        }
    }
    
    handleMouseUp() {
        this.isDragging = false;
        this.canvas.style.cursor = 'default';
    }
    
    handleWheel(e) {
        e.preventDefault();
        const scaleFactor = 0.1;
        const newScale = this.scale + (e.deltaY > 0 ? -scaleFactor : scaleFactor);
        this.scale = Math.max(0.1, Math.min(3, newScale));
        this.render();
    }
    
    // Touch event handlers
    handleTouchStart(e) {
        e.preventDefault();
        const touch = e.touches[0];
        this.handleMouseDown({ clientX: touch.clientX, clientY: touch.clientY });
    }
    
    handleTouchMove(e) {
        e.preventDefault();
        const touch = e.touches[0];
        this.handleMouseMove({ clientX: touch.clientX, clientY: touch.clientY });
    }
    
    handleTouchEnd(e) {
        e.preventDefault();
        this.handleMouseUp();
    }
    
    // Public methods
    updateMastery(masteryData) {
        this.masteryData = { ...this.masteryData, ...masteryData };
        this.render();
    }
    
    selectNode(nodeId) {
        this.selectedNode = this.nodes.find(n => n.id === nodeId);
        this.render();
    }
    
    resetView() {
        this.scale = 1;
        this.offsetX = 0;
        this.offsetY = 0;
        this.render();
    }
    
    fitToView() {
        if (!this.nodes || this.nodes.length === 0) return;
        
        const bounds = this.nodes.reduce((acc, node) => {
            acc.minX = Math.min(acc.minX, node.x);
            acc.maxX = Math.max(acc.maxX, node.x);
            acc.minY = Math.min(acc.minY, node.y);
            acc.maxY = Math.max(acc.maxY, node.y);
            return acc;
        }, { minX: Infinity, maxX: -Infinity, minY: Infinity, maxY: -Infinity });
        
        const padding = 50;
        const scaleX = (this.canvas.width - 2 * padding) / (bounds.maxX - bounds.minX);
        const scaleY = (this.canvas.height - 2 * padding) / (bounds.maxY - bounds.minY);
        this.scale = Math.min(scaleX, scaleY, 1);
        
        this.offsetX = (this.canvas.width - (bounds.maxX - bounds.minX) * this.scale) / 2 - bounds.minX * this.scale;
        this.offsetY = (this.canvas.height - (bounds.maxY - bounds.minY) * this.scale) / 2 - bounds.minY * this.scale;
        
        this.render();
    }
}
