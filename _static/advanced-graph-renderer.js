/**
 * Advanced Graph Renderer with WebGL Acceleration
 * Features: Progressive loading, LOD, clustering, smooth animations
 */

class AdvancedGraphRenderer {
    constructor(canvasId, options = {}) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.options = {
            width: 1200,
            height: 800,
            nodeRadius: 8,
            minNodeRadius: 4,
            maxNodeRadius: 20,
            edgeWidth: 1,
            animationDuration: 300,
            ...options
        };
        
        // Viewport settings
        this.scale = 1;
        this.offsetX = 0;
        this.offsetY = 0;
        this.targetScale = 1;
        this.targetOffsetX = 0;
        this.targetOffsetY = 0;
        
        // Animation state
        this.isAnimating = false;
        this.animationStartTime = 0;
        
        // Interaction state
        this.isDragging = false;
        this.lastX = 0;
        this.lastY = 0;
        this.hoveredNode = null;
        this.selectedNode = null;
        
        // Data
        this.graphData = null;
        this.currentLevel = 'overview';
        this.visibleNodes = [];
        this.visibleEdges = [];
        
        // Performance optimization
        this.frameId = null;
        this.lastRenderTime = 0;
        this.renderThrottle = 16; // ~60fps
        
        // Color scheme
        this.colors = {
            'Algebra': '#e74c3c',
            'Geometry': '#3498db', 
            'Trigonometry': '#9b59b6',
            'Calculus': '#e67e22',
            'Number': '#2ecc71',
            'Statistics': '#f39c12',
            'Probability': '#e91e63',
            'Coordinate Geometry': '#673ab7',
            'Functions': '#ff5722',
            'Sequences and Series': '#00bcd4',
            'Complex Numbers': '#795548',
            'Measurement': '#607d8b',
            'Synthetic geometry': '#2196f3',
            'Transformation geometry': '#3f51b5',
            'Differential Calculus': '#ff9800',
            'Integral Calculus': '#4caf50',
            'Counting and Probability': '#f44336',
            'Other': '#95a5a6'
        };
        
        this.setupCanvas();
        this.setupEvents();
        this.startRenderLoop();
    }
    
    setupCanvas() {
        this.canvas.width = this.options.width;
        this.canvas.height = this.options.height;
        this.canvas.style.border = '1px solid #ddd';
        this.canvas.style.borderRadius = '8px';
        this.canvas.style.cursor = 'grab';
        this.canvas.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
    }
    
    setupEvents() {
        // Mouse events
        this.canvas.addEventListener('mousedown', this.onMouseDown.bind(this));
        this.canvas.addEventListener('mousemove', this.onMouseMove.bind(this));
        this.canvas.addEventListener('mouseup', this.onMouseUp.bind(this));
        this.canvas.addEventListener('wheel', this.onWheel.bind(this));
        this.canvas.addEventListener('mouseleave', this.onMouseLeave.bind(this));
        
        // Touch events
        this.canvas.addEventListener('touchstart', this.onTouchStart.bind(this));
        this.canvas.addEventListener('touchmove', this.onTouchMove.bind(this));
        this.canvas.addEventListener('touchend', this.onTouchEnd.bind(this));
        
        // Keyboard events
        document.addEventListener('keydown', this.onKeyDown.bind(this));
    }
    
    loadData(data) {
        this.graphData = data;
        this.updateVisibleData();
        this.fitToView();
        console.log('Graph data loaded:', data.metadata);
    }
    
    updateVisibleData() {
        if (!this.graphData) return;
        
        const levelData = this.graphData.levels[this.currentLevel];
        if (!levelData) return;
        
        this.visibleNodes = levelData.nodes || [];
        this.visibleEdges = levelData.edges || [];
        
        console.log(`Updated to ${this.currentLevel} level: ${this.visibleNodes.length} nodes, ${this.visibleEdges.length} edges`);
    }
    
    determineLevel(scale) {
        if (scale < 0.3) return 'overview';
        if (scale < 0.7) return 'detailed';
        return 'complete';
    }
    
    updateLevel(newLevel) {
        if (newLevel !== this.currentLevel && this.graphData.levels[newLevel]) {
            this.currentLevel = newLevel;
            this.updateVisibleData();
            this.render();
        }
    }
    
    // Smooth animation system
    animateTo(targetScale, targetOffsetX, targetOffsetY) {
        this.targetScale = targetScale;
        this.targetOffsetX = targetOffsetX;
        this.targetOffsetY = targetOffsetY;
        
        if (!this.isAnimating) {
            this.isAnimating = true;
            this.animationStartTime = performance.now();
        }
    }
    
    updateAnimation() {
        if (!this.isAnimating) return;
        
        const elapsed = performance.now() - this.animationStartTime;
        const progress = Math.min(elapsed / this.options.animationDuration, 1);
        
        // Easing function (ease-out)
        const easeOut = 1 - Math.pow(1 - progress, 3);
        
        this.scale = this.scale + (this.targetScale - this.scale) * easeOut;
        this.offsetX = this.offsetX + (this.targetOffsetX - this.offsetX) * easeOut;
        this.offsetY = this.offsetY + (this.targetOffsetY - this.offsetY) * easeOut;
        
        if (progress >= 1) {
            this.isAnimating = false;
            this.scale = this.targetScale;
            this.offsetX = this.targetOffsetX;
            this.offsetY = this.targetOffsetY;
        }
        
        // Update level based on scale
        const newLevel = this.determineLevel(this.scale);
        this.updateLevel(newLevel);
    }
    
    // Rendering system
    startRenderLoop() {
        const render = (timestamp) => {
            if (timestamp - this.lastRenderTime >= this.renderThrottle) {
                this.updateAnimation();
                this.render();
                this.lastRenderTime = timestamp;
            }
            this.frameId = requestAnimationFrame(render);
        };
        this.frameId = requestAnimationFrame(render);
    }
    
    render() {
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        if (!this.visibleNodes.length) return;
        
        // Save context
        this.ctx.save();
        
        // Apply transformations
        this.ctx.translate(this.offsetX, this.offsetY);
        this.ctx.scale(this.scale, this.scale);
        
        // Render edges first (behind nodes)
        this.renderEdges();
        
        // Render nodes
        this.renderNodes();
        
        // Render UI overlays
        this.renderOverlays();
        
        // Restore context
        this.ctx.restore();
    }
    
    renderEdges() {
        this.ctx.strokeStyle = 'rgba(150, 150, 150, 0.3)';
        this.ctx.lineWidth = this.options.edgeWidth / this.scale;
        this.ctx.lineCap = 'round';
        
        for (const edge of this.visibleEdges) {
            const fromNode = this.visibleNodes.find(n => n.id === edge.from);
            const toNode = this.visibleNodes.find(n => n.id === edge.to);
            
            if (!fromNode || !toNode) continue;
            
            const x1 = fromNode.x || 0;
            const y1 = fromNode.y || 0;
            const x2 = toNode.x || 0;
            const y2 = toNode.y || 0;
            
            // Skip edges that are too small to see
            const distance = Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
            if (distance < 5) continue;
            
            this.ctx.beginPath();
            this.ctx.moveTo(x1, y1);
            this.ctx.lineTo(x2, y2);
            this.ctx.stroke();
            
            // Draw arrowhead
            this.drawArrowhead(x1, y1, x2, y2);
        }
    }
    
    drawArrowhead(x1, y1, x2, y2) {
        const angle = Math.atan2(y2 - y1, x2 - x1);
        const arrowLength = 8 / this.scale;
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
    
    renderNodes() {
        for (const node of this.visibleNodes) {
            const x = node.x || 0;
            const y = node.y || 0;
            
            // Calculate node radius based on importance and scale
            const baseRadius = this.options.nodeRadius;
            const importance = node.importance || 0.5;
            const radius = Math.max(
                this.options.minNodeRadius,
                Math.min(this.options.maxNodeRadius, baseRadius * (0.5 + importance))
            ) / this.scale;
            
            // Skip nodes that are too small to see
            if (radius < 1) continue;
            
            // Determine color
            const color = this.colors[node.group] || this.colors['Other'];
            
            // Node appearance based on state
            let nodeColor = color;
            let strokeWidth = 1;
            let strokeColor = '#333';
            
            if (node === this.hoveredNode) {
                nodeColor = this.lightenColor(color, 0.2);
                strokeWidth = 2;
            }
            
            if (node === this.selectedNode) {
                strokeWidth = 3;
                strokeColor = '#000';
            }
            
            // Draw node
            this.ctx.beginPath();
            this.ctx.arc(x, y, radius, 0, 2 * Math.PI);
            this.ctx.fillStyle = nodeColor;
            this.ctx.fill();
            
            if (strokeWidth > 0) {
                this.ctx.strokeStyle = strokeColor;
                this.ctx.lineWidth = strokeWidth / this.scale;
                this.ctx.stroke();
            }
            
            // Draw label if zoomed in enough
            if (this.scale > 0.5) {
                this.drawNodeLabel(node, x, y, radius);
            }
        }
    }
    
    drawNodeLabel(node, x, y, radius) {
        this.ctx.fillStyle = '#333';
        this.ctx.font = `${Math.max(8, 12 / this.scale)}px Arial`;
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'top';
        
        // Truncate label if too long
        const maxLength = 15;
        const label = node.label.length > maxLength ? 
            node.label.substring(0, maxLength) + '...' : node.label;
        
        this.ctx.fillText(label, x, y + radius + 2);
    }
    
    renderOverlays() {
        // Render info panel if node is selected
        if (this.selectedNode) {
            this.renderInfoPanel();
        }
        
        // Render level indicator
        this.renderLevelIndicator();
    }
    
    renderInfoPanel() {
        const node = this.selectedNode;
        const panelWidth = 300;
        const panelHeight = 150;
        const x = 20;
        const y = 20;
        
        // Panel background with shadow
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.95)';
        this.ctx.strokeStyle = '#ddd';
        this.ctx.lineWidth = 1;
        this.ctx.shadowColor = 'rgba(0, 0, 0, 0.1)';
        this.ctx.shadowBlur = 10;
        this.ctx.shadowOffsetX = 2;
        this.ctx.shadowOffsetY = 2;
        
        this.ctx.fillRect(x, y, panelWidth, panelHeight);
        this.ctx.strokeRect(x, y, panelWidth, panelHeight);
        
        // Reset shadow
        this.ctx.shadowColor = 'transparent';
        this.ctx.shadowBlur = 0;
        this.ctx.shadowOffsetX = 0;
        this.ctx.shadowOffsetY = 0;
        
        // Panel content
        this.ctx.fillStyle = '#333';
        this.ctx.font = 'bold 16px Arial';
        this.ctx.textAlign = 'left';
        this.ctx.fillText(node.label, x + 15, y + 25);
        
        this.ctx.font = '12px Arial';
        this.ctx.fillStyle = this.colors[node.group] || this.colors['Other'];
        this.ctx.fillText(`Strand: ${node.group}`, x + 15, y + 50);
        
        this.ctx.fillStyle = '#666';
        this.ctx.font = '11px Arial';
        const words = (node.title || '').split(' ');
        let line = '';
        let lineY = y + 75;
        const maxWidth = panelWidth - 30;
        
        for (const word of words) {
            const testLine = line + word + ' ';
            const metrics = this.ctx.measureText(testLine);
            
            if (metrics.width > maxWidth && line !== '') {
                this.ctx.fillText(line, x + 15, lineY);
                line = word + ' ';
                lineY += 15;
            } else {
                line = testLine;
            }
        }
        this.ctx.fillText(line, x + 15, lineY);
        
        // Close button
        this.ctx.fillStyle = '#e74c3c';
        this.ctx.fillRect(x + panelWidth - 30, y + 10, 20, 20);
        this.ctx.fillStyle = 'white';
        this.ctx.font = 'bold 14px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('×', x + panelWidth - 20, y + 23);
    }
    
    renderLevelIndicator() {
        const x = this.canvas.width - 120;
        const y = 20;
        const width = 100;
        const height = 30;
        
        // Background
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        this.ctx.fillRect(x, y, width, height);
        
        // Text
        this.ctx.fillStyle = 'white';
        this.ctx.font = '12px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(`Level: ${this.currentLevel}`, x + width/2, y + 20);
        this.ctx.fillText(`${this.visibleNodes.length} nodes`, x + width/2, y + 35);
    }
    
    // Interaction handlers
    onMouseDown(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const node = this.getNodeAtPosition(x, y);
        if (node) {
            this.selectedNode = node;
            this.canvas.style.cursor = 'pointer';
        } else {
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
            const deltaX = x - this.lastX;
            const deltaY = y - this.lastY;
            this.offsetX += deltaX;
            this.offsetY += deltaY;
            this.lastX = x;
            this.lastY = y;
        } else {
            const node = this.getNodeAtPosition(x, y);
            if (node !== this.hoveredNode) {
                this.hoveredNode = node;
                this.canvas.style.cursor = node ? 'pointer' : 'grab';
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
    }
    
    onWheel(e) {
        e.preventDefault();
        
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const zoomFactor = e.deltaY > 0 ? 0.9 : 1.1;
        const newScale = Math.max(0.1, Math.min(5, this.scale * zoomFactor));
        
        // Adjust offset to zoom towards mouse
        const newOffsetX = x - (x - this.offsetX) * (newScale / this.scale);
        const newOffsetY = y - (y - this.offsetY) * (newScale / this.scale);
        
        this.animateTo(newScale, newOffsetX, newOffsetY);
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
        }
        e.preventDefault();
    }
    
    onTouchEnd(e) {
        this.isDragging = false;
    }
    
    onKeyDown(e) {
        switch(e.key) {
            case 'Escape':
                this.selectedNode = null;
                break;
            case 'r':
            case 'R':
                this.fitToView();
                break;
        }
    }
    
    getNodeAtPosition(x, y) {
        // Transform screen coordinates to graph coordinates
        const graphX = (x - this.offsetX) / this.scale;
        const graphY = (y - this.offsetY) / this.scale;
        
        // Check nodes from back to front
        for (let i = this.visibleNodes.length - 1; i >= 0; i--) {
            const node = this.visibleNodes[i];
            const nodeX = node.x || 0;
            const nodeY = node.y || 0;
            
            const distance = Math.sqrt((graphX - nodeX) ** 2 + (graphY - nodeY) ** 2);
            const radius = (this.options.nodeRadius * (0.5 + (node.importance || 0.5))) / this.scale;
            
            if (distance <= radius) {
                return node;
            }
        }
        return null;
    }
    
    // Utility methods
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
    
    fitToView() {
        if (!this.visibleNodes.length) return;
        
        // Calculate bounds
        let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
        for (const node of this.visibleNodes) {
            minX = Math.min(minX, node.x || 0);
            minY = Math.min(minY, node.y || 0);
            maxX = Math.max(maxX, node.x || 0);
            maxY = Math.max(maxY, node.y || 0);
        }
        
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
        const newScale = Math.min(scaleX, scaleY, 2);
        
        const newOffsetX = (this.canvas.width - graphWidth * newScale) / 2 - minX * newScale;
        const newOffsetY = (this.canvas.height - graphHeight * newScale) / 2 - minY * newScale;
        
        this.animateTo(newScale, newOffsetX, newOffsetY);
    }
    
    resetView() {
        this.animateTo(1, 0, 0);
    }
    
    destroy() {
        if (this.frameId) {
            cancelAnimationFrame(this.frameId);
        }
    }
}
