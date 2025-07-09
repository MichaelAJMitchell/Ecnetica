/**
 * Lightweight Knowledge Graph Renderer
 * Pure JavaScript canvas-based visualization with no external dependencies
 */

class LightweightGraph {
    constructor(canvasId, data) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.data = data;
        
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
        
        // Visual settings
        this.nodeRadius = 12;
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
        
        this.setupCanvas();
        this.setupEvents();
        this.render();
    }
    
    setupCanvas() {
        // Set canvas size - much larger now
        this.canvas.width = 1200;
        this.canvas.height = 900;
        
        // Set canvas style
        this.canvas.style.border = '1px solid #ddd';
        this.canvas.style.borderRadius = '4px';
        this.canvas.style.cursor = 'grab';
    }
    
    setupEvents() {
        // Mouse events
        this.canvas.addEventListener('mousedown', this.onMouseDown.bind(this));
        this.canvas.addEventListener('mousemove', this.onMouseMove.bind(this));
        this.canvas.addEventListener('mouseup', this.onMouseUp.bind(this));
        this.canvas.addEventListener('wheel', this.onWheel.bind(this));
        this.canvas.addEventListener('mouseleave', this.onMouseLeave.bind(this));
        
        // Touch events for mobile
        this.canvas.addEventListener('touchstart', this.onTouchStart.bind(this));
        this.canvas.addEventListener('touchmove', this.onTouchMove.bind(this));
        this.canvas.addEventListener('touchend', this.onTouchEnd.bind(this));
    }
    
    onMouseDown(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        // Check if clicking on a node
        const node = this.getNodeAtPosition(x, y);
        if (node) {
            this.selectedNode = node;
            this.showNodeInfo(node);
        } else {
            // Start dragging
            this.isDragging = true;
            this.lastX = x;
            this.lastY = y;
            this.canvas.style.cursor = 'grabbing';
        }
        
        e.preventDefault();
    }
    
    onMouseMove(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        if (this.isDragging) {
            // Pan the view
            const deltaX = x - this.lastX;
            const deltaY = y - this.lastY;
            this.offsetX += deltaX;
            this.offsetY += deltaY;
            this.lastX = x;
            this.lastY = y;
            this.render();
        } else {
            // Check for hover
            const node = this.getNodeAtPosition(x, y);
            if (node !== this.hoveredNode) {
                this.hoveredNode = node;
                this.canvas.style.cursor = node ? 'pointer' : 'grab';
                this.render();
            }
        }
    }
    
    onMouseUp(e) {
        this.isDragging = false;
        this.canvas.style.cursor = 'grab';
    }
    
    onMouseLeave(e) {
        this.isDragging = false;
        this.hoveredNode = null;
        this.canvas.style.cursor = 'grab';
        this.render();
    }
    
    onWheel(e) {
        e.preventDefault();
        
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        // Zoom towards mouse position
        const zoomFactor = e.deltaY > 0 ? 0.9 : 1.1;
        const newScale = Math.max(0.3, Math.min(5, this.scale * zoomFactor));
        
        // Adjust offset to zoom towards mouse
        this.offsetX = x - (x - this.offsetX) * (newScale / this.scale);
        this.offsetY = y - (y - this.offsetY) * (newScale / this.scale);
        
        this.scale = newScale;
        this.render();
    }
    
    onTouchStart(e) {
        if (e.touches.length === 1) {
            const touch = e.touches[0];
            const rect = this.canvas.getBoundingClientRect();
            const x = touch.clientX - rect.left;
            const y = touch.clientY - rect.top;
            
            const node = this.getNodeAtPosition(x, y);
            if (node) {
                this.selectedNode = node;
                this.showNodeInfo(node);
            } else {
                this.isDragging = true;
                this.lastX = x;
                this.lastY = y;
            }
        }
        e.preventDefault();
    }
    
    onTouchMove(e) {
        if (e.touches.length === 1 && this.isDragging) {
            const touch = e.touches[0];
            const rect = this.canvas.getBoundingClientRect();
            const x = touch.clientX - rect.left;
            const y = touch.clientY - rect.top;
            
            const deltaX = x - this.lastX;
            const deltaY = y - this.lastY;
            this.offsetX += deltaX;
            this.offsetY += deltaY;
            this.lastX = x;
            this.lastY = y;
            this.render();
        }
        e.preventDefault();
    }
    
    onTouchEnd(e) {
        this.isDragging = false;
    }
    
    getNodeAtPosition(x, y) {
        for (let i = this.data.nodes.length - 1; i >= 0; i--) {
            const node = this.data.nodes[i];
            const nodeX = node.x * this.scale + this.offsetX;
            const nodeY = node.y * this.scale + this.offsetY;
            
            const distance = Math.sqrt((x - nodeX) ** 2 + (y - nodeY) ** 2);
            if (distance <= this.nodeRadius) {
                return node;
            }
        }
        return null;
    }
    
    render() {
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw edges first (so they appear behind nodes)
        this.drawEdges();
        
        // Draw nodes
        this.drawNodes();
        
        // Draw info panel if node is selected
        if (this.selectedNode) {
            this.drawInfoPanel();
        }
    }
    
    drawEdges() {
        this.ctx.strokeStyle = '#ddd';
        this.ctx.lineWidth = 1;
        
        this.data.edges.forEach(edge => {
            const fromNode = this.data.nodes.find(n => n.id === edge.from);
            const toNode = this.data.nodes.find(n => n.id === edge.to);
            
            if (fromNode && toNode) {
                const x1 = fromNode.x * this.scale + this.offsetX;
                const y1 = fromNode.y * this.scale + this.offsetY;
                const x2 = toNode.x * this.scale + this.offsetX;
                const y2 = toNode.y * this.scale + this.offsetY;
                
                // Draw arrow
                this.ctx.beginPath();
                this.ctx.moveTo(x1, y1);
                this.ctx.lineTo(x2, y2);
                this.ctx.stroke();
                
                // Draw arrowhead
                const angle = Math.atan2(y2 - y1, x2 - x1);
                const arrowLength = 10;
                const arrowAngle = Math.PI / 6;
                
                this.ctx.beginPath();
                this.ctx.moveTo(x2, y2);
                this.ctx.lineTo(
                    x2 - arrowLength * Math.cos(angle - arrowAngle),
                    y2 - arrowLength * Math.sin(angle - arrowAngle)
                );
                this.ctx.moveTo(x2, y2);
                this.ctx.lineTo(
                    x2 - arrowLength * Math.cos(angle + arrowAngle),
                    y2 - arrowLength * Math.sin(angle + arrowAngle)
                );
                this.ctx.stroke();
            }
        });
    }
    
    drawNodes() {
        this.data.nodes.forEach(node => {
            const x = node.x * this.scale + this.offsetX;
            const y = node.y * this.scale + this.offsetY;
            
            // Determine node appearance
            let radius = this.nodeRadius;
            let color = this.getStrandColor(node.strand);
            
            if (node === this.hoveredNode) {
                radius = this.nodeRadius + 2;
                color = this.lightenColor(color, 0.2);
            }
            
            if (node === this.selectedNode) {
                radius = this.nodeRadius + 3;
                this.ctx.strokeStyle = '#333';
                this.ctx.lineWidth = 2;
            } else {
                this.ctx.strokeStyle = '#333';
                this.ctx.lineWidth = 1;
            }
            
            // Draw node circle
            this.ctx.beginPath();
            this.ctx.arc(x, y, radius, 0, 2 * Math.PI);
            this.ctx.fillStyle = color;
            this.ctx.fill();
            this.ctx.stroke();
            
            // Draw node label only when zoomed in enough (scale > 0.8)
            // and make text larger and more readable
            if (this.scale > 0.8) {
                this.ctx.fillStyle = '#333';
                // Larger font size - scale from 6px to 12px based on zoom level
                const fontSize = Math.max(6, Math.min(12, 6 + (this.scale - 0.8) * 8));
                this.ctx.font = `${fontSize}px Arial`;
                this.ctx.textAlign = 'center';
                this.ctx.fillText(node.name, x, y + radius + fontSize + 2);
            }
        });
    }
    
    drawInfoPanel() {
        const node = this.selectedNode;
        const panelWidth = 300;
        const panelHeight = 120;
        const x = 10;
        const y = 10;
        
        // Panel background
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.95)';
        this.ctx.strokeStyle = '#333';
        this.ctx.lineWidth = 1;
        this.ctx.fillRect(x, y, panelWidth, panelHeight);
        this.ctx.strokeRect(x, y, panelWidth, panelHeight);
        
        // Panel content
        this.ctx.fillStyle = '#333';
        this.ctx.font = 'bold 14px Arial';
        this.ctx.textAlign = 'left';
        this.ctx.fillText(node.full_name, x + 10, y + 25);
        
        this.ctx.font = '12px Arial';
        this.ctx.fillStyle = this.getStrandColor(node.strand);
        this.ctx.fillText(`Strand: ${node.strand}`, x + 10, y + 45);
        
        this.ctx.fillStyle = '#666';
        this.ctx.font = '11px Arial';
        const words = node.explanation.split(' ');
        let line = '';
        let lineY = y + 65;
        const maxWidth = panelWidth - 20;
        
        for (const word of words) {
            const testLine = line + word + ' ';
            const metrics = this.ctx.measureText(testLine);
            
            if (metrics.width > maxWidth && line !== '') {
                this.ctx.fillText(line, x + 10, lineY);
                line = word + ' ';
                lineY += 15;
            } else {
                line = testLine;
            }
        }
        this.ctx.fillText(line, x + 10, lineY);
        
        // Close button
        this.ctx.fillStyle = '#f44336';
        this.ctx.fillRect(x + panelWidth - 25, y + 5, 20, 20);
        this.ctx.fillStyle = 'white';
        this.ctx.font = 'bold 14px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('×', x + panelWidth - 15, y + 18);
    }
    
    getStrandColor(strand) {
        return this.nodeColors[strand] || this.nodeColors['Other'];
    }
    
    lightenColor(color, amount) {
        const num = parseInt(color.replace('#', ''), 16);
        const amt = Math.round(2.55 * amount * 100);
        const R = (num >> 16) + amt;
        const G = (num >> 8 & 0x00FF) + amt;
        const B = (num & 0x0000FF) + amt;
        return '#' + (0x1000000 + (R < 255 ? R < 1 ? 0 : R : 255) * 0x10000 +
            (G < 255 ? G < 1 ? 0 : G : 255) * 0x100 +
            (B < 255 ? B < 1 ? 0 : B : 255)).toString(16).slice(1);
    }
    
    showNodeInfo(node) {
        // This could be extended to show more detailed information
        console.log('Selected node:', node);
    }
    
    // Public methods for external control
    resetView() {
        this.scale = 1;
        this.offsetX = 0;
        this.offsetY = 0;
        this.selectedNode = null;
        this.render();
    }
    
    fitToView() {
        if (this.data.nodes.length === 0) return;
        
        // Calculate bounds
        let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
        this.data.nodes.forEach(node => {
            minX = Math.min(minX, node.x);
            minY = Math.min(minY, node.y);
            maxX = Math.max(maxX, node.x);
            maxY = Math.max(maxY, node.y);
        });
        
        // Add padding
        const padding = 50;
        minX -= padding;
        minY -= padding;
        maxX += padding;
        maxY += padding;
        
        // Calculate scale and offset
        const graphWidth = maxX - minX;
        const graphHeight = maxY - minY;
        const scaleX = (this.canvas.width - 100) / graphWidth;
        const scaleY = (this.canvas.height - 100) / graphHeight;
        this.scale = Math.min(scaleX, scaleY, 3); // Max scale of 3 for fit to view
        
        // Center the graph
        this.offsetX = (this.canvas.width - graphWidth * this.scale) / 2 - minX * this.scale;
        this.offsetY = (this.canvas.height - graphHeight * this.scale) / 2 - minY * this.scale;
        
        this.render();
    }
} 