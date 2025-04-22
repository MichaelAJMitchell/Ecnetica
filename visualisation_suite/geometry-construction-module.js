/**
 * MathExplorer - Geometry Construction Module
 * 
 * An extension of the base MathExplorer framework that specializes in
 * geometric constructions and interactive geometric elements.
 */

import MathExplorer from './base-visualization-framework.js';

class GeometryConstruction extends MathExplorer {
  /**
   * Create a new geometry construction environment
   * @param {Object} config - Configuration settings
   */
  constructor(config) {
    // Set default config values specific to geometry construction
    const geometryConfig = {
      // Use a coordinate system better suited for geometry
      range: { xMin: -10, xMax: 10, yMin: -10, yMax: 10 },
      // Enable info panel for measurements and properties
      infoPanel: true,
      // Geometry-specific settings
      geometryOptions: {
        snapToGrid: true,
        snapThreshold: 0.5,
        pointRadius: 5,
        lineWidth: 2,
        angleUnit: 'degrees', // 'degrees' or 'radians'
        constructionHistory: true,
        labelPoints: true,
        labelDistance: 0.7
      },
      ...config
    };
    
    // Call parent constructor
    super(geometryConfig);
    
    // Initialize geometry elements collections
    this.points = [];
    this.lines = [];
    this.circles = [];
    this.angles = [];
    this.polygons = [];
    
    // Track selection state
    this.selectedElement = null;
    
    // Track drag state
    this.dragState = {
      isDragging: false,
      element: null,
      startX: 0,
      startY: 0
    };
    
    // Set up additional event handlers for geometry
    this.setupGeometryEventHandlers();
    
    // Initialize tool state
    this.currentTool = 'select'; // Default tool
    
    // Add construction history panel if enabled
    if (this.config.geometryOptions.constructionHistory) {
      this.setupConstructionHistory();
    }
    
    // Point labeling counter (for automatic labeling)
    this.pointLabelCounter = 0;
    
    // Add a measurements panel
    this.setupMeasurementsPanel();
  }

  /**
   * Set up additional event handlers for geometry interactions
   */
  setupGeometryEventHandlers() {
    // Mouse down event for selecting and starting drags
    this.canvas.addEventListener('mousedown', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      // Convert to math coordinates
      const mathX = this.toMathX(x);
      const mathY = this.toMathY(y);
      
      // Handle based on current tool
      this.handleMouseDown(mathX, mathY, e);
    });
    
    // Mouse move for dragging and hovering
    this.canvas.addEventListener('mousemove', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      // Convert to math coordinates
      const mathX = this.toMathX(x);
      const mathY = this.toMathY(y);
      
      // Handle dragging or hovering
      this.handleMouseMove(mathX, mathY, e);
    });
    
    // Mouse up for ending drags
    this.canvas.addEventListener('mouseup', (e) => {
      // End any drag operation
      if (this.dragState.isDragging) {
        this.dragState.isDragging = false;
        this.render();
        
        // Add to construction history if applicable
        if (this.config.geometryOptions.constructionHistory && this.dragState.element) {
          this.addToHistory(`Moved ${this.dragState.element.type} ${this.dragState.element.label || ''}`);
        }
      }
    });
    
    // Mouse leave for safety
    this.canvas.addEventListener('mouseleave', () => {
      // End any drag operation
      this.dragState.isDragging = false;
    });
    
    // Double click for special actions
    this.canvas.addEventListener('dblclick', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      // Convert to math coordinates
      const mathX = this.toMathX(x);
      const mathY = this.toMathY(y);
      
      // Handle double click (e.g., add a point, create a label)
      this.handleDoubleClick(mathX, mathY, e);
    });
  }

  /**
   * Set up the construction history panel
   */
  setupConstructionHistory() {
    // Create history panel
    this.historyPanel = document.createElement('div');
    this.historyPanel.classList.add('math-explorer-history');
    this.historyPanel.style.position = 'absolute';
    this.historyPanel.style.top = '10px';
    this.historyPanel.style.right = '10px';
    this.historyPanel.style.width = '200px';
    this.historyPanel.style.backgroundColor = this.config.theme.infoPanelBackground;
    this.historyPanel.style.border = `1px solid ${this.config.theme.borderColor}`;
    this.historyPanel.style.borderRadius = '5px';
    this.historyPanel.style.padding = '10px';
    this.historyPanel.style.fontSize = '14px';
    this.historyPanel.style.maxHeight = '300px';
    this.historyPanel.style.overflowY = 'auto';
    
    // Add title
    const title = document.createElement('h3');
    title.style.margin = '0 0 10px 0';
    title.style.fontSize = '16px';
    title.textContent = 'Construction History';
    this.historyPanel.appendChild(title);
    
    // Add history list
    this.historyList = document.createElement('ul');
    this.historyList.style.listStyle = 'none';
    this.historyList.style.padding = '0';
    this.historyList.style.margin = '0';
    this.historyPanel.appendChild(this.historyList);
    
    // Add to canvas area
    this.canvasArea.appendChild(this.historyPanel);
  }

  /**
   * Add an entry to the construction history
   * @param {string} action - Description of the action
   */
  addToHistory(action) {
    if (!this.config.geometryOptions.constructionHistory) return;
    
    const entry = document.createElement('li');
    entry.style.padding = '5px 0';
    entry.style.borderBottom = `1px solid ${this.config.theme.borderColor}`;
    entry.textContent = action;
    
    this.historyList.appendChild(entry);
    this.historyPanel.scrollTop = this.historyPanel.scrollHeight;
  }

  /**
   * Set up the measurements panel
   */
  setupMeasurementsPanel() {
    // Use existing info panel for measurements
    if (!this.infoPanel) return;
    
    // Clear and set up
    this.infoPanel.innerHTML = '';
    
    // Add title
    const title = document.createElement('h3');
    title.style.margin = '0 0 10px 0';
    title.style.fontSize = '16px';
    title.textContent = 'Measurements';
    this.infoPanel.appendChild(title);
    
    // We'll add measurements dynamically as elements are created or selected
  }

  /**
   * Set the current tool
   * @param {string} tool - Tool name
   */
  setTool(tool) {
    this.currentTool = tool;
    
    // Clear any temporary construction state
    this.constructionState = {};
    
    // Update cursor style based on tool
    switch (tool) {
      case 'select':
        this.canvas.style.cursor = 'default';
        break;
      case 'point':
        this.canvas.style.cursor = 'crosshair';
        break;
      case 'line':
      case 'segment':
      case 'ray':
        this.canvas.style.cursor = 'crosshair';
        break;
      case 'circle':
        this.canvas.style.cursor = 'crosshair';
        break;
      case 'angle':
        this.canvas.style.cursor = 'crosshair';
        break;
      case 'polygon':
        this.canvas.style.cursor = 'crosshair';
        break;
      case 'perpendicular':
      case 'parallel':
      case 'bisector':
        this.canvas.style.cursor = 'crosshair';
        break;
      default:
        this.canvas.style.cursor = 'default';
    }
  }

  /**
   * Handle mouse down events based on the current tool
   * @param {number} x - Math X coordinate
   * @param {number} y - Math Y coordinate
   * @param {Event} event - Original mouse event
   */
  handleMouseDown(x, y, event) {
    // Snap to grid if enabled
    if (this.config.geometryOptions.snapToGrid) {
      const snapped = this.snapToGrid(x, y);
      x = snapped.x;
      y = snapped.y;
    }
    
    // Check for existing elements at this position
    const element = this.findElementAt(x, y);
    
    switch (this.currentTool) {
      case 'select':
        if (element) {
          // Select the element
          this.selectElement(element);
          
          // Start drag if it's a point
          if (element.type === 'point') {
            this.dragState = {
              isDragging: true,
              element: element,
              startX: x,
              startY: y
            };
          }
        } else {
          // Deselect if clicking empty space
          this.selectedElement = null;
        }
        break;
        
      case 'point':
        if (!element) {
          // Create a new point if not clicking on existing element
          this.createPoint(x, y);
        }
        break;
        
      case 'line':
      case 'segment':
      case 'ray':
        // For line tools, we need to select two points
        if (element && element.type === 'point') {
          if (!this.constructionState.firstPoint) {
            // First point selection
            this.constructionState.firstPoint = element;
            // Highlight the point
            element.highlighted = true;
          } else if (element !== this.constructionState.firstPoint) {
            // Second point selection - create the line/segment/ray
            const p1 = this.constructionState.firstPoint;
            const p2 = element;
            
            switch (this.currentTool) {
              case 'line':
                this.createLine(p1, p2);
                break;
              case 'segment':
                this.createSegment(p1, p2);
                break;
              case 'ray':
                this.createRay(p1, p2);
                break;
            }
            
            // Reset construction state
            if (this.constructionState.firstPoint) {
              this.constructionState.firstPoint.highlighted = false;
            }
            this.constructionState = {};
          }
        }
        break;
        
      case 'circle':
        // For circle tool, we need to select center and a point on the circumference
        if (element && element.type === 'point') {
          if (!this.constructionState.center) {
            // First point selection (center)
            this.constructionState.center = element;
            // Highlight the point
            element.highlighted = true;
          } else if (element !== this.constructionState.center) {
            // Second point selection - create the circle
            const center = this.constructionState.center;
            const pointOnCircle = element;
            
            this.createCircle(center, pointOnCircle);
            
            // Reset construction state
            if (this.constructionState.center) {
              this.constructionState.center.highlighted = false;
            }
            this.constructionState = {};
          }
        }
        break;
        
      case 'angle':
        // For angle tool, we need three points
        if (element && element.type === 'point') {
          if (!this.constructionState.p1) {
            // First point
            this.constructionState.p1 = element;
            element.highlighted = true;
          } else if (!this.constructionState.p2) {
            // Second point (vertex)
            this.constructionState.p2 = element;
            element.highlighted = true;
          } else if (element !== this.constructionState.p1 && element !== this.constructionState.p2) {
            // Third point - create the angle
            this.createAngle(
              this.constructionState.p1,
              this.constructionState.p2,
              element
            );
            
            // Reset construction state
            if (this.constructionState.p1) this.constructionState.p1.highlighted = false;
            if (this.constructionState.p2) this.constructionState.p2.highlighted = false;
            this.constructionState = {};
          }
        }
        break;
        
      case 'polygon':
        // For polygon tool, collect points until we close the polygon
        if (element && element.type === 'point') {
          if (!this.constructionState.points) {
            // First point
            this.constructionState.points = [element];
            element.highlighted = true;
          } else if (element === this.constructionState.points[0] && this.constructionState.points.length > 2) {
            // Clicked on first point again - close the polygon
            this.createPolygon(this.constructionState.points);
            
            // Reset construction state
            this.constructionState.points.forEach(p => {
              p.highlighted = false;
            });
            this.constructionState = {};
          } else if (!this.constructionState.points.includes(element)) {
            // Add point to polygon
            this.constructionState.points.push(element);
            element.highlighted = true;
          }
        }
        break;
        
      case 'perpendicular':
        // For perpendicular line, select a line and a point
        if (element) {
          if (element.type === 'line' && !this.constructionState.line) {
            // First select a line
            this.constructionState.line = element;
            element.highlighted = true;
          } else if (element.type === 'point' && this.constructionState.line) {
            // Then select a point
            this.createPerpendicularLine(this.constructionState.line, element);
            
            // Reset construction state
            if (this.constructionState.line) {
              this.constructionState.line.highlighted = false;
            }
            this.constructionState = {};
          }
        }
        break;
        
      case 'parallel':
        // For parallel line, select a line and a point
        if (element) {
          if (element.type === 'line' && !this.constructionState.line) {
            // First select a line
            this.constructionState.line = element;
            element.highlighted = true;
          } else if (element.type === 'point' && this.constructionState.line) {
            // Then select a point
            this.createParallelLine(this.constructionState.line, element);
            
            // Reset construction state
            if (this.constructionState.line) {
              this.constructionState.line.highlighted = false;
            }
            this.constructionState = {};
          }
        }
        break;
        
      case 'bisector':
        // For angle bisector, select three points (an angle)
        if (element && element.type === 'point') {
          if (!this.constructionState.p1) {
            // First point
            this.constructionState.p1 = element;
            element.highlighted = true;
          } else if (!this.constructionState.p2) {
            // Second point (vertex)
            this.constructionState.p2 = element;
            element.highlighted = true;
          } else if (element !== this.constructionState.p1 && element !== this.constructionState.p2) {
            // Third point - create the angle bisector
            this.createAngleBisector(
              this.constructionState.p1,
              this.constructionState.p2,
              element
            );
            
            // Reset construction state
            if (this.constructionState.p1) this.constructionState.p1.highlighted = false;
            if (this.constructionState.p2) this.constructionState.p2.highlighted = false;
            this.constructionState = {};
          }
        }
        break;
    }
    
    // Render updates
    this.render();
    
    // Update measurements panel
    this.updateMeasurements();
  }

  /**
   * Handle mouse move events for dragging and hovering
   * @param {number} x - Math X coordinate
   * @param {number} y - Math Y coordinate
   * @param {Event} event - Original mouse event
   */
  handleMouseMove(x, y, event) {
    // Snap to grid if enabled
    if (this.config.geometryOptions.snapToGrid) {
      const snapped = this.snapToGrid(x, y);
      x = snapped.x;
      y = snapped.y;
    }
    
    // Handle dragging
    if (this.dragState.isDragging && this.dragState.element) {
      if (this.dragState.element.type === 'point') {
        // Update point position
        this.dragState.element.x = x;
        this.dragState.element.y = y;
        
        // Update any dependent elements (to be implemented)
        this.updateDependentElements(this.dragState.element);
        
        // Render updates
        this.render();
        
        // Update measurements
        this.updateMeasurements();
      }
    } else {
      // Hovering - find element under cursor
      const element = this.findElementAt(x, y);
      
      // Update cursor style based on what's under it
      if (element) {
        this.canvas.style.cursor = element.type === 'point' ? 'move' : 'pointer';
      } else {
        // Use tool-specific cursor
        switch (this.currentTool) {
          case 'select':
            this.canvas.style.cursor = 'default';
            break;
          case 'point':
          case 'line':
          case 'segment':
          case 'ray':
          case 'circle':
          case 'angle':
          case 'polygon':
          case 'perpendicular':
          case 'parallel':
          case 'bisector':
            this.canvas.style.cursor = 'crosshair';
            break;
          default:
            this.canvas.style.cursor = 'default';
        }
      }
      
      // Show construction preview if applicable
      this.showConstructionPreview(x, y);
    }
  }

  /**
   * Handle double click events
   * @param {number} x - Math X coordinate
   * @param {number} y - Math Y coordinate
   * @param {Event} event - Original mouse event
   */
  handleDoubleClick(x, y, event) {
    // Find element at position
    const element = this.findElementAt(x, y);
    
    if (element) {
      // Allow renaming or adding labels
      this.promptForLabel(element);
    }
  }

  /**
   * Prompt user for a label for the element
   * @param {Object} element - Geometry element
   */
  promptForLabel(element) {
    const label = prompt('Enter label:', element.label || '');
    
    if (label !== null) {  // Check for cancel button
      element.label = label;
      this.render();
      
      // Add to history
      if (this.config.geometryOptions.constructionHistory) {
        this.addToHistory(`Labeled ${element.type} as "${label}"`);
      }
    }
  }

  /**
   * Show construction preview based on current tool and state
   * @param {number} x - Current mouse X position
   * @param {number} y - Current mouse Y position
   */
  showConstructionPreview(x, y) {
    // Clear existing preview
    this.render();
    
    switch (this.currentTool) {
      case 'line':
      case 'segment':
      case 'ray':
        // Show preview line if first point is selected
        if (this.constructionState.firstPoint) {
          // Draw preview with dashed line
          this.ctx.setLineDash([5, 5]);
          this.ctx.strokeStyle = this.config.theme.highlightColor;
          this.ctx.lineWidth = this.config.geometryOptions.lineWidth;
          
          this.ctx.beginPath();
          const p1 = this.constructionState.firstPoint;
          
          if (this.currentTool === 'line') {
            // For line, extend in both directions
            const dx = x - p1.x;
            const dy = y - p1.y;
            const len = 100; // Arbitrary large value for line extension
            
            // Extend line in both directions
            const startX = p1.x - len * dx;
            const startY = p1.y - len * dy;
            const endX = p1.x + len * dx;
            const endY = p1.y + len * dy;
            
            this.ctx.moveTo(this.toCanvasX(startX), this.toCanvasY(startY));
            this.ctx.lineTo(this.toCanvasX(endX), this.toCanvasY(endY));
          } else if (this.currentTool === 'segment') {
            // For segment, just go from p1 to mouse position
            this.ctx.moveTo(this.toCanvasX(p1.x), this.toCanvasY(p1.y));
            this.ctx.lineTo(this.toCanvasX(x), this.toCanvasY(y));
          } else if (this.currentTool === 'ray') {
            // For ray, extend from p1 through mouse position
            const dx = x - p1.x;
            const dy = y - p1.y;
            const len = 100; // Arbitrary large value for ray extension
            
            // Calculate endpoint far in the direction of mouse
            const endX = p1.x + len * dx;
            const endY = p1.y + len * dy;
            
            this.ctx.moveTo(this.toCanvasX(p1.x), this.toCanvasY(p1.y));
            this.ctx.lineTo(this.toCanvasX(endX), this.toCanvasY(endY));
          }
          
          this.ctx.stroke();
          this.ctx.setLineDash([]); // Reset dash pattern
        }
        break;
        
      case 'circle':
        // Show preview circle if center is selected
        if (this.constructionState.center) {
          const center = this.constructionState.center;
          const radius = Math.sqrt(
            Math.pow(x - center.x, 2) + Math.pow(y - center.y, 2)
          );
          
          // Draw preview circle
          this.ctx.setLineDash([5, 5]);
          this.ctx.strokeStyle = this.config.theme.highlightColor;
          this.ctx.lineWidth = this.config.geometryOptions.lineWidth;
          
          this.ctx.beginPath();
          this.ctx.arc(
            this.toCanvasX(center.x),
            this.toCanvasY(center.y),
            radius * (this.canvas.width - 2 * this.config.padding) / (this.config.range.xMax - this.config.range.xMin),
            0,
            2 * Math.PI
          );
          this.ctx.stroke();
          this.ctx.setLineDash([]); // Reset dash pattern
        }
        break;
        
      case 'polygon':
        // Show preview polygon if at least one point is selected
        if (this.constructionState.points && this.constructionState.points.length > 0) {
          // Draw existing segments
          this.ctx.strokeStyle = this.config.theme.highlightColor;
          this.ctx.lineWidth = this.config.geometryOptions.lineWidth;
          this.ctx.setLineDash([]);
          
          this.ctx.beginPath();
          const firstPoint = this.constructionState.points[0];
          this.ctx.moveTo(
            this.toCanvasX(firstPoint.x),
            this.toCanvasY(firstPoint.y)
          );
          
          for (let i = 1; i < this.constructionState.points.length; i++) {
            const p = this.constructionState.points[i];
            this.ctx.lineTo(this.toCanvasX(p.x), this.toCanvasY(p.y));
          }
          
          // Draw line to current mouse position
          const lastPoint = this.constructionState.points[this.constructionState.points.length - 1];
          this.ctx.lineTo(this.toCanvasX(x), this.toCanvasY(y));
          
          // Close polygon if near first point
          const firstP = this.constructionState.points[0];
          const dist = Math.sqrt(Math.pow(x - firstP.x, 2) + Math.pow(y - firstP.y, 2));
          
          if (dist < this.config.geometryOptions.snapThreshold && this.constructionState.points.length > 2) {
            this.ctx.lineTo(
              this.toCanvasX(firstP.x),
              this.toCanvasY(firstP.y)
            );
          }
          
          this.ctx.stroke();
        }
        break;
    }
  }

  /**
   * Select a geometry element
   * @param {Object} element - Element to select
   */
  selectElement(element) {
    // Deselect previous selection
    if (this.selectedElement) {
      this.selectedElement.selected = false;
    }
    
    // Select new element
    this.selectedElement = element;
    element.selected = true;
    
    // Update measurements for the selected element
    this.updateMeasurements();
  }

  /**
   * Find a geometry element at a specific position
   * @param {number} x - Math X coordinate
   * @param {number} y - Math Y coordinate
   * @returns {Object|null} Found element or null
   */
  findElementAt(x, y) {
    // Check points first (they're smaller, so need priority)
    for (const point of this.points) {
      const dist = Math.sqrt(Math.pow(x - point.x, 2) + Math.pow(y - point.y, 2));
      if (dist <= this.config.geometryOptions.snapThreshold) {
        return point;
      }
    }
    
    // Check lines
    for (const line of this.lines) {
      if (this.isPointNearLine(x, y, line)) {
        return line;
      }
    }
    
    // Check circles
    for (const circle of this.circles) {
      if (this.isPointNearCircle(x, y, circle)) {
        return circle;
      }
    }
    
    // Check angles
    for (const angle of this.angles) {
      if (this.isPointInAngle(x, y, angle)) {
        return angle;
      }
    }
    
    // Check polygons
    for (const polygon of this.polygons) {
      if (this.isPointInPolygon(x, y, polygon)) {
        return polygon;
      }
    }
    
    return null;
  }

  /**
   * Check if a point is near a line
   * @param {number} x - Point X coordinate
   * @param {number} y - Point Y coordinate
   * @param {Object} line - Line object
   * @returns {boolean} True if point is near line
   */
  isPointNearLine(x, y, line) {
    const p1 = line.p1;
    const p2 = line.p2;
    
    // For segments, check if point is within the segment bounds
    if (line.type === 'segment') {
      // Check if point is beyond either endpoint
      const dot = (x - p1.x) * (p2.x - p1.x) + (y - p1.y) * (p2.y - p1.y);
      const len_sq = Math.pow(p2.x - p1.x, 2) + Math.pow(p2.y - p1.y, 2);
      
      // If dot < 0, point is beyond p1
      if (dot < 0) return false;
      // If dot > len_sq, point is beyond p2
      if (dot > len_sq) return false;
    }
    
    // For rays, check if point is in the correct direction
    if (line.type === 'ray') {
      const dot = (x - p1.x) * (p2.x - p1.x) + (y - p1.y) * (p2.y - p1.y);
      // If dot < 0, point is behind the ray origin
      if (dot < 0) return false;
    }
    
    // Calculate distance from point to line
    const numerator = Math.abs((p2.y - p1.y) * x - (p2.x - p1.x) * y + p2.x * p1.y - p2.y * p1.x);
    const denominator = Math.sqrt(Math.pow(p2.y - p1.y, 2) + Math.pow(p2.x - p1.x, 2));
    const distance = numerator / denominator;
    
    return distance <= this.config.geometryOptions.snapThreshold;
  }

  /**
   * Check if a point is near a circle
   * @param {number} x - Point X coordinate
   * @param {number} y - Point Y coordinate
   * @param {Object} circle - Circle object
   * @returns {boolean} True if point is near circle
   */
  isPointNearCircle(x, y, circle) {
    const center = circle.center;
    const distanceFromCenter = Math.sqrt(
      Math.pow(x - center.x, 2) + Math.pow(y - center.y, 2)
    );
    
    const distanceFromCircumference = Math.abs(distanceFromCenter - circle.radius);
    
    return distanceFromCircumference <= this.config.geometryOptions.snapThreshold;
  }

  /**
   * Check if a point is in an angle
   * @param {number} x - Point X coordinate
   * @param {number} y - Point Y coordinate
   * @param {Object} angle - Angle object
   * @returns {boolean} True if point is in angle
   */
  isPointInAngle(x, y, angle) {
    // Implementation will depend on how angles are represented
    // For now, just check if point is near the vertex
    const vertex = angle.vertex;
    const dist = Math.sqrt(Math.pow(x - vertex.x, 2) + Math.pow(y - vertex.y, 2));
    
    // For simplicity, just check if near vertex
    // A more sophisticated implementation would check if within the angle arc
    return dist <= this.config.geometryOptions.snapThreshold * 3;
  }

  /**
   * Check if a point is in a polygon
   * @param {number} x - Point X coordinate
   * @param {number} y - Point Y coordinate
   * @param {Object} polygon - Polygon object
   * @returns {boolean} True if point is in polygon
   */
  isPointInPolygon(x, y, polygon) {
    // First check if point is near any edge
    const vertices = polygon.vertices;
    for (let i = 0; i < vertices.length; i++) {
      const p1 = vertices[i];
      const p2 = vertices[(i + 1) % vertices.length];
      
      // Create a temporary segment for edge
      const edge = { type: 'segment', p1, p2 };
      
      if (this.isPointNearLine(x, y, edge)) {
        return true;
      }
    }
    
    // If not near an edge, check if inside the polygon using ray casting algorithm
    let inside = false;
    for (let i = 0, j = vertices.length - 1; i < vertices.length; j = i++) {
      const xi = vertices[i].x, yi = vertices[i].y;
      const xj = vertices[j].x, yj = vertices[j].y;
      
      const intersect = ((yi > y) !== (yj > y)) &&
        (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
      
      if (intersect) inside = !inside;
    }
    
    return inside;
  }

  /**
   * Snap coordinates to grid
   * @param {number} x - X coordinate
   * @param {number} y - Y coordinate
   * @returns {Object} Snapped coordinates
   */
  snapToGrid(x, y) {
    if (!this.config.geometryOptions.snapToGrid) {
      return { x, y };
    }
    
    const gridSize = this.config.gridSpacing || 1;
    const snapThreshold = this.config.geometryOptions.snapThreshold;
    
    // Calculate nearest grid points
    const gridX = Math.round(x / gridSize) * gridSize;
    const gridY = Math.round(y / gridSize) * gridSize;
    
    // Check if close enough to snap
    const dx = Math.abs(x - gridX);
    const dy = Math.abs(y - gridY);
    
    return {
      x: dx < snapThreshold ? gridX : x,
      y: dy < snapThreshold ? gridY : y
    };
  }

  /**
   * Create a new point
   * @param {number} x - X coordinate
   * @param {number} y - Y coordinate
   * @param {Object} options - Point options
   * @returns {Object} Created point
   */
  createPoint(x, y, options = {}) {
    // Generate label if not provided
    let label = options.label;
    if (!label && this.config.geometryOptions.labelPoints) {
      label = String.fromCharCode(65 + this.pointLabelCounter % 26);
      this.pointLabelCounter++;
    }
    
    const point = {
      type: 'point',
      x: x,
      y: y,
      label: label,
      color: options.color || this.config.theme.highlightColor,
      size: options.size || this.config.geometryOptions.pointRadius,
      highlighted: false,
      selected: false,
      depends: []
    };
    
    this.points.push(point);
    
    // Add to construction history
    if (this.config.geometryOptions.constructionHistory) {
      this.addToHistory(`Created point ${label || ''} at (${x.toFixed(1)}, ${y.toFixed(1)})`);
    }
    
    return point;
  }

  /**
   * Create a new line
   * @param {Object} p1 - First point
   * @param {Object} p2 - Second point
   * @param {Object} options - Line options
   * @returns {Object} Created line
   */
  createLine(p1, p2, options = {}) {
    const line = {
      type: 'line',
      p1: p1,
      p2: p2,
      label: options.label || '',
      color: options.color || this.config.theme.highlightColor,
      lineWidth: options.lineWidth || this.config.geometryOptions.lineWidth,
      highlighted: false,
      selected: false,
      infinite: true
    };
    
    this.lines.push(line);
    
    // Add dependencies
    p1.depends.push(line);
    p2.depends.push(line);
    
    // Add to construction history
    if (this.config.geometryOptions.constructionHistory) {
      this.addToHistory(`Created line through ${p1.label || 'point'} and ${p2.label || 'point'}`);
    }
    
    return line;
  }

  /**
   * Create a new line segment
   * @param {Object} p1 - First point
   * @param {Object} p2 - Second point
   * @param {Object} options - Segment options
   * @returns {Object} Created segment
   */
  createSegment(p1, p2, options = {}) {
    const segment = {
      type: 'segment',
      p1: p1,
      p2: p2,
      label: options.label || '',
      color: options.color || this.config.theme.highlightColor,
      lineWidth: options.lineWidth || this.config.geometryOptions.lineWidth,
      highlighted: false,
      selected: false,
      infinite: false
    };
    
    this.lines.push(segment);
    
    // Add dependencies
    p1.depends.push(segment);
    p2.depends.push(segment);
    
    // Add to construction history
    if (this.config.geometryOptions.constructionHistory) {
      this.addToHistory(`Created segment from ${p1.label || 'point'} to ${p2.label || 'point'}`);
    }
    
    return segment;
  }

  /**
   * Create a new ray
   * @param {Object} p1 - Starting point
   * @param {Object} p2 - Direction point
   * @param {Object} options - Ray options
   * @returns {Object} Created ray
   */
  createRay(p1, p2, options = {}) {
    const ray = {
      type: 'ray',
      p1: p1, // Origin
      p2: p2, // Direction
      label: options.label || '',
      color: options.color || this.config.theme.highlightColor,
      lineWidth: options.lineWidth || this.config.geometryOptions.lineWidth,
      highlighted: false,
      selected: false,
      infinite: false // One side only
    };
    
    this.lines.push(ray);
    
    // Add dependencies
    p1.depends.push(ray);
    p2.depends.push(ray);
    
    // Add to construction history
    if (this.config.geometryOptions.constructionHistory) {
      this.addToHistory(`Created ray from ${p1.label || 'point'} through ${p2.label || 'point'}`);
    }
    
    return ray;
  }

  /**
   * Create a new circle
   * @param {Object} center - Center point
   * @param {Object} pointOnCircle - Point on the circumference
   * @param {Object} options - Circle options
   * @returns {Object} Created circle
   */
  createCircle(center, pointOnCircle, options = {}) {
    const radius = Math.sqrt(
      Math.pow(pointOnCircle.x - center.x, 2) + 
      Math.pow(pointOnCircle.y - center.y, 2)
    );
    
    const circle = {
      type: 'circle',
      center: center,
      radius: radius,
      label: options.label || '',
      color: options.color || this.config.theme.highlightColor,
      lineWidth: options.lineWidth || this.config.geometryOptions.lineWidth,
      highlighted: false,
      selected: false,
      pointOnCircle: pointOnCircle
    };
    
    this.circles.push(circle);
    
    // Add dependencies
    center.depends.push(circle);
    pointOnCircle.depends.push(circle);
    
    // Add to construction history
    if (this.config.geometryOptions.constructionHistory) {
      this.addToHistory(`Created circle with center ${center.label || 'point'} and radius ${radius.toFixed(2)}`);
    }
    
    return circle;
  }

  /**
   * Create a new angle
   * @param {Object} p1 - First point
   * @param {Object} vertex - Vertex point
   * @param {Object} p3 - Third point
   * @param {Object} options - Angle options
   * @returns {Object} Created angle
   */
  createAngle(p1, vertex, p3, options = {}) {
    // Calculate angle in radians
    const angle1 = Math.atan2(p1.y - vertex.y, p1.x - vertex.x);
    const angle2 = Math.atan2(p3.y - vertex.y, p3.x - vertex.x);
    
    // Calculate the signed angle between the two
    let angleSize = angle2 - angle1;
    // Normalize to [0, 2π)
    while (angleSize < 0) angleSize += 2 * Math.PI;
    while (angleSize >= 2 * Math.PI) angleSize -= 2 * Math.PI;
    
    // Convert to degrees if needed
    const angleDegrees = this.config.geometryOptions.angleUnit === 'degrees'
      ? angleSize * 180 / Math.PI
      : angleSize;
    
    const angle = {
      type: 'angle',
      p1: p1,
      vertex: vertex,
      p3: p3,
      angle: angleSize,
      angleDegrees: angleDegrees,
      label: options.label || '',
      color: options.color || this.config.theme.highlightColor,
      lineWidth: options.lineWidth || this.config.geometryOptions.lineWidth,
      highlighted: false,
      selected: false
    };
    
    this.angles.push(angle);
    
    // Add dependencies
    p1.depends.push(angle);
    vertex.depends.push(angle);
    p3.depends.push(angle);
    
    // Add to construction history
    if (this.config.geometryOptions.constructionHistory) {
      const unit = this.config.geometryOptions.angleUnit === 'degrees' ? '°' : ' rad';
      this.addToHistory(`Created angle ${p1.label || 'p1'}-${vertex.label || 'v'}-${p3.label || 'p3'} = ${angleDegrees.toFixed(1)}${unit}`);
    }
    
    return angle;
  }

  /**
   * Create a new polygon
   * @param {Array} vertices - Array of vertex points
   * @param {Object} options - Polygon options
   * @returns {Object} Created polygon
   */
  createPolygon(vertices, options = {}) {
    const polygon = {
      type: 'polygon',
      vertices: vertices,
      label: options.label || '',
      color: options.color || this.config.theme.highlightColor,
      fillColor: options.fillColor || 'rgba(0, 0, 0, 0.1)',
      lineWidth: options.lineWidth || this.config.geometryOptions.lineWidth,
      highlighted: false,
      selected: false
    };
    
    this.polygons.push(polygon);
    
    // Add dependencies
    vertices.forEach(vertex => {
      vertex.depends.push(polygon);
    });
    
    // Add to construction history
    if (this.config.geometryOptions.constructionHistory) {
      const vertexLabels = vertices.map(v => v.label || 'point').join('-');
      this.addToHistory(`Created polygon ${vertexLabels}`);
    }
    
    return polygon;
  }

  /**
   * Create a perpendicular line
   * @param {Object} line - Reference line
   * @param {Object} point - Point not on the line
   * @param {Object} options - Line options
   * @returns {Object} Created perpendicular line
   */
  createPerpendicularLine(line, point, options = {}) {
    // Get the direction vector of the original line
    const dx = line.p2.x - line.p1.x;
    const dy = line.p2.y - line.p1.y;
    
    // Calculate perpendicular direction (-dy, dx)
    const perpDx = -dy;
    const perpDy = dx;
    
    // Find the foot of the perpendicular
    // This is the point on the original line that forms a perpendicular with the given point
    const t = ((point.x - line.p1.x) * dx + (point.y - line.p1.y) * dy) / (dx * dx + dy * dy);
    const footX = line.p1.x + t * dx;
    const footY = line.p1.y + t * dy;
    
    // Create a point at the foot of the perpendicular
    const foot = this.createPoint(footX, footY, { label: options.footLabel });
    
    // Create a line through the point and perpendicular to the original line
    const perpLine = this.createLine(point, foot, {
      label: options.label || '',
      color: options.color || this.config.theme.highlightColor
    });
    
    // Add to construction history
    if (this.config.geometryOptions.constructionHistory) {
      this.addToHistory(`Created perpendicular line from ${point.label || 'point'} to line`);
    }
    
    return perpLine;
  }

  /**
   * Create a parallel line
   * @param {Object} line - Reference line
   * @param {Object} point - Point not on the line
   * @param {Object} options - Line options
   * @returns {Object} Created parallel line
   */
  createParallelLine(line, point, options = {}) {
    // Get the direction vector of the original line
    const dx = line.p2.x - line.p1.x;
    const dy = line.p2.y - line.p1.y;
    
    // Create a second point for the parallel line
    const secondX = point.x + dx;
    const secondY = point.y + dy;
    const secondPoint = this.createPoint(secondX, secondY, { label: options.secondPointLabel });
    
    // Create a line through the point and parallel to the original line
    const parallelLine = this.createLine(point, secondPoint, {
      label: options.label || '',
      color: options.color || this.config.theme.highlightColor
    });
    
    // Add to construction history
    if (this.config.geometryOptions.constructionHistory) {
      this.addToHistory(`Created parallel line through ${point.label || 'point'} parallel to line`);
    }
    
    return parallelLine;
  }

  /**
   * Create an angle bisector
   * @param {Object} p1 - First point
   * @param {Object} vertex - Vertex point
   * @param {Object} p3 - Third point
   * @param {Object} options - Line options
   * @returns {Object} Created angle bisector
   */
  createAngleBisector(p1, vertex, p3, options = {}) {
    // Calculate angle vectors
    const v1x = p1.x - vertex.x;
    const v1y = p1.y - vertex.y;
    const v2x = p3.x - vertex.x;
    const v2y = p3.y - vertex.y;
    
    // Normalize vectors
    const len1 = Math.sqrt(v1x * v1x + v1y * v1y);
    const len2 = Math.sqrt(v2x * v2x + v2y * v2y);
    
    const n1x = v1x / len1;
    const n1y = v1y / len1;
    const n2x = v2x / len2;
    const n2y = v2y / len2;
    
    // Calculate bisector vector (add normalized vectors)
    const bisectorX = n1x + n2x;
    const bisectorY = n1y + n2y;
    
    // Create a second point on the bisector line
    const bisectorLen = Math.sqrt(bisectorX * bisectorX + bisectorY * bisectorY);
    const secondX = vertex.x + (bisectorX / bisectorLen) * 5; // Arbitrary length
    const secondY = vertex.y + (bisectorY / bisectorLen) * 5;
    
    const secondPoint = this.createPoint(secondX, secondY, { label: options.secondPointLabel });
    
    // Create the bisector line
    const bisector = this.createRay(vertex, secondPoint, {
      label: options.label || '',
      color: options.color || this.config.theme.highlightColor
    });
    
    // Add to construction history
    if (this.config.geometryOptions.constructionHistory) {
      this.addToHistory(`Created angle bisector for angle ${p1.label || 'p1'}-${vertex.label || 'v'}-${p3.label || 'p3'}`);
    }
    
    return bisector;
  }

  /**
   * Update elements that depend on a modified element
   * @param {Object} element - Modified element
   */
  updateDependentElements(element) {
    // This is just a basic implementation
    // A more sophisticated implementation would use a proper dependency graph
    
    if (element.type === 'point') {
      // Update all elements that depend on this point
      element.depends.forEach(dependent => {
        if (dependent.type === 'circle' && dependent.center === element) {
          // Center of circle moved
          // No need to update radius
        } else if (dependent.type === 'circle' && dependent.pointOnCircle === element) {
          // Point on circle moved
          // Update radius
          dependent.radius = Math.sqrt(
            Math.pow(dependent.pointOnCircle.x - dependent.center.x, 2) + 
            Math.pow(dependent.pointOnCircle.y - dependent.center.y, 2)
          );
        }
        
        // Angles, lines, etc. will automatically update since they reference the points directly
      });
    }
  }

  /**
   * Update measurements display in the info panel
   */
  updateMeasurements() {
    if (!this.infoPanel) return;
    
    // Clear existing measurements
    while (this.infoPanel.childNodes.length > 1) {
      this.infoPanel.removeChild(this.infoPanel.lastChild);
    }
    
    // Show measurements for selected element
    if (this.selectedElement) {
      const element = this.selectedElement;
      
      switch (element.type) {
        case 'point':
          this.addMeasurement('Point', `${element.label || 'Point'}`);
          this.addMeasurement('Coordinates', `(${element.x.toFixed(2)}, ${element.y.toFixed(2)})`);
          break;
          
        case 'line':
        case 'segment':
        case 'ray':
          this.addMeasurement('Line', `${element.label || (element.type === 'line' ? 'Line' : element.type === 'segment' ? 'Segment' : 'Ray')}`);
          this.addMeasurement('Points', `${element.p1.label || 'p1'} to ${element.p2.label || 'p2'}`);
          
          if (element.type === 'segment') {
            const length = Math.sqrt(
              Math.pow(element.p2.x - element.p1.x, 2) + 
              Math.pow(element.p2.y - element.p1.y, 2)
            );
            this.addMeasurement('Length', length.toFixed(2));
          }
          
          const slope = (element.p2.y - element.p1.y) / (element.p2.x - element.p1.x);
          this.addMeasurement('Slope', isFinite(slope) ? slope.toFixed(2) : 'Undefined');
          
          if (isFinite(slope)) {
            const angle = Math.atan(slope) * (this.config.geometryOptions.angleUnit === 'degrees' ? 180 / Math.PI : 1);
            const unit = this.config.geometryOptions.angleUnit === 'degrees' ? '°' : ' rad';
            this.addMeasurement('Angle with x-axis', `${angle.toFixed(2)}${unit}`);
          }
          break;
          
        case 'circle':
          this.addMeasurement('Circle', `${element.label || 'Circle'}`);
          this.addMeasurement('Center', `${element.center.label || '(unlabeled)'} (${element.center.x.toFixed(2)}, ${element.center.y.toFixed(2)})`);
          this.addMeasurement('Radius', element.radius.toFixed(2));
          this.addMeasurement('Circumference', (2 * Math.PI * element.radius).toFixed(2));
          this.addMeasurement('Area', (Math.PI * element.radius * element.radius).toFixed(2));
          break;
          
        case 'angle':
          const unit = this.config.geometryOptions.angleUnit === 'degrees' ? '°' : ' rad';
          this.addMeasurement('Angle', `${element.label || 'Angle'}`);
          this.addMeasurement('Vertex', `${element.vertex.label || '(unlabeled)'}`);
          this.addMeasurement('Measure', `${element.angleDegrees.toFixed(2)}${unit}`);
          break;
          
        case 'polygon':
          this.addMeasurement('Polygon', `${element.label || 'Polygon'}`);
          
          // Calculate perimeter
          let perimeter = 0;
          for (let i = 0; i < element.vertices.length; i++) {
            const p1 = element.vertices[i];
            const p2 = element.vertices[(i + 1) % element.vertices.length];
            perimeter += Math.sqrt(
              Math.pow(p2.x - p1.x, 2) + 
              Math.pow(p2.y - p1.y, 2)
            );
          }
          this.addMeasurement('Perimeter', perimeter.toFixed(2));
          
          // Calculate area using shoelace formula
          let area = 0;
          for (let i = 0; i < element.vertices.length; i++) {
            const p1 = element.vertices[i];
            const p2 = element.vertices[(i + 1) % element.vertices.length];
            area += p1.x * p2.y - p2.x * p1.y;
          }
          area = Math.abs(area) / 2;
          this.addMeasurement('Area', area.toFixed(2));
          
          // Number of vertices
          this.addMeasurement('Vertices', element.vertices.length.toString());
          break;
      }
      
      // Add custom measurements based on element type
      // This could be extended for specific geometric properties
    }
  }

  /**
   * Add a measurement to the info panel
   * @param {string} label - Measurement label
   * @param {string} value - Measurement value
   */
  addMeasurement(label, value) {
    const container = document.createElement('div');
    container.style.display = 'flex';
    container.style.justifyContent = 'space-between';
    container.style.marginBottom = '5px';
    
    const labelElement = document.createElement('span');
    labelElement.textContent = `${label}:`;
    labelElement.style.fontWeight = 'bold';
    
    const valueElement = document.createElement('span');
    valueElement.textContent = value;
    
    container.appendChild(labelElement);
    container.appendChild(valueElement);
    
    this.infoPanel.appendChild(container);
  }

  /**
   * Draw all geometry elements
   */
  render() {
    // Call parent render to clear canvas and draw grid/axes
    super.render();
    
    // Draw elements in order (back to front)
    this.drawPolygons();
    this.drawLines();
    this.drawCircles();
    this.drawAngles();
    this.drawPoints();
  }

  /**
   * Draw all points
   */
  drawPoints() {
    for (const point of this.points) {
      this.drawPoint(point);
    }
  }

  /**
   * Draw a single point
   * @param {Object} point - Point object
   */
  drawPoint(point) {
    const x = this.toCanvasX(point.x);
    const y = this.toCanvasY(point.y);
    
    // Determine point style
    let color = point.color;
    let size = point.size;
    
    if (point.selected) {
      color = this.config.theme.secondaryColor;
      size += 2;
    } else if (point.highlighted) {
      color = this.config.theme.highlightColor;
      size += 1;
    }
    
    // Draw point
    this.ctx.fillStyle = color;
    this.ctx.beginPath();
    this.ctx.arc(x, y, size, 0, 2 * Math.PI);
    this.ctx.fill();
    
    // Draw label if it exists
    if (point.label && this.config.geometryOptions.labelPoints) {
      const labelDist = this.config.geometryOptions.labelDistance;
      this.ctx.fillStyle = this.config.theme.textColor;
      this.ctx.font = `14px ${this.config.theme.fontFamily}`;
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'middle';
      this.ctx.fillText(point.label, x, y - (size + 10));
    }
  }

  /**
   * Draw all lines
   */
  drawLines() {
    for (const line of this.lines) {
      this.drawLine(line);
    }
  }

  /**
   * Draw a single line
   * @param {Object} line - Line object
   */
  drawLine(line) {
    const p1 = line.p1;
    const p2 = line.p2;
    
    // Determine line style
    let color = line.color;
    let lineWidth = line.lineWidth;
    let dashPattern = [];
    
    if (line.selected) {
      color = this.config.theme.secondaryColor;
      lineWidth += 1;
    } else if (line.highlighted) {
      color = this.config.theme.highlightColor;
      lineWidth += 1;
    }
    
    // Set line style
    this.ctx.strokeStyle = color;
    this.ctx.lineWidth = lineWidth;
    this.ctx.setLineDash(dashPattern);
    
    // Draw line
    this.ctx.beginPath();
    
    if (line.type === 'line') {
      // For infinite line, extend beyond endpoints
      const dx = p2.x - p1.x;
      const dy = p2.y - p1.y;
      
      // Handle vertical line
      if (Math.abs(dx) < 1e-10) {
        const x = p1.x;
        const topY = this.config.range.yMax;
        const bottomY = this.config.range.yMin;
        
        this.ctx.moveTo(this.toCanvasX(x), this.toCanvasY(bottomY));
        this.ctx.lineTo(this.toCanvasX(x), this.toCanvasY(topY));
      } else {
        const slope = dy / dx;
        const leftX = this.config.range.xMin;
        const rightX = this.config.range.xMax;
        
        const leftY = p1.y + (leftX - p1.x) * slope;
        const rightY = p1.y + (rightX - p1.x) * slope;
        
        this.ctx.moveTo(this.toCanvasX(leftX), this.toCanvasY(leftY));
        this.ctx.lineTo(this.toCanvasX(rightX), this.toCanvasY(rightY));
      }
    } else if (line.type === 'segment') {
      // For segment, just draw between the two points
      this.ctx.moveTo(this.toCanvasX(p1.x), this.toCanvasY(p1.y));
      this.ctx.lineTo(this.toCanvasX(p2.x), this.toCanvasY(p2.y));
    } else if (line.type === 'ray') {
      // For ray, start at p1 and extend through p2
      const dx = p2.x - p1.x;
      const dy = p2.y - p1.y;
      
      // Calculate a point far in the direction of p2
      const len = Math.sqrt(dx * dx + dy * dy);
      const unitX = dx / len;
      const unitY = dy / len;
      
      const farDist = Math.max(
        this.config.range.xMax - this.config.range.xMin,
        this.config.range.yMax - this.config.range.yMin
      ) * 2;
      
      const farX = p1.x + unitX * farDist;
      const farY = p1.y + unitY * farDist;
      
      this.ctx.moveTo(this.toCanvasX(p1.x), this.toCanvasY(p1.y));
      this.ctx.lineTo(this.toCanvasX(farX), this.toCanvasY(farY));
    }
    
    this.ctx.stroke();
    
    // Draw label if it exists
    if (line.label) {
      // For simplicity, place label at midpoint
      const midX = (p1.x + p2.x) / 2;
      const midY = (p1.y + p2.y) / 2;
      
      this.ctx.fillStyle = this.config.theme.textColor;
      this.ctx.font = `14px ${this.config.theme.fontFamily}`;
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'middle';
      this.ctx.fillText(line.label, this.toCanvasX(midX), this.toCanvasY(midY) - 10);
    }
  }

  /**
   * Draw all circles
   */
  drawCircles() {
    for (const circle of this.circles) {
      this.drawCircle(circle);
    }
  }

  /**
   * Draw a single circle
   * @param {Object} circle - Circle object
   */
  drawCircle(circle) {
    const center = circle.center;
    const radius = circle.radius;
    
    // Convert to canvas radius
    const canvasRadius = radius * (this.canvas.width - 2 * this.config.padding) / 
                        (this.config.range.xMax - this.config.range.xMin);
    
    // Determine circle style
    let color = circle.color;
    let lineWidth = circle.lineWidth;
    let dashPattern = [];
    
    if (circle.selected) {
      color = this.config.theme.secondaryColor;
      lineWidth += 1;
    } else if (circle.highlighted) {
      color = this.config.theme.highlightColor;
      lineWidth += 1;
    }
    
    // Set circle style
    this.ctx.strokeStyle = color;
    this.ctx.lineWidth = lineWidth;
    this.ctx.setLineDash(dashPattern);
    
    // Draw circle
    this.ctx.beginPath();
    this.ctx.arc(
      this.toCanvasX(center.x),
      this.toCanvasY(center.y),
      canvasRadius,
      0,
      2 * Math.PI
    );
    this.ctx.stroke();
    
    // Draw label if it exists
    if (circle.label) {
      this.ctx.fillStyle = this.config.theme.textColor;
      this.ctx.font = `14px ${this.config.theme.fontFamily}`;
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'middle';
      this.ctx.fillText(
        circle.label,
        this.toCanvasX(center.x),
        this.toCanvasY(center.y + radius) - 10
      );
    }
  }

  /**
   * Draw all angles
   */
  drawAngles() {
    for (const angle of this.angles) {
      this.drawAngle(angle);
    }
  }

  /**
   * Draw a single angle
   * @param {Object} angle - Angle object
   */
  drawAngle(angle) {
    const vertex = angle.vertex;
    const p1 = angle.p1;
    const p3 = angle.p3;
    
    // Calculate the two angles relative to positive x-axis
    const angle1 = Math.atan2(p1.y - vertex.y, p1.x - vertex.x);
    const angle2 = Math.atan2(p3.y - vertex.y, p3.x - vertex.x);
    
    // Determine angle style
    let color = angle.color;
    let lineWidth = angle.lineWidth;
    let dashPattern = [];
    
    if (angle.selected) {
      color = this.config.theme.secondaryColor;
      lineWidth += 1;
    } else if (angle.highlighted) {
      color = this.config.theme.highlightColor;
      lineWidth += 1;
    }
    
    // Set angle style
    this.ctx.strokeStyle = color;
    this.ctx.lineWidth = lineWidth;
    this.ctx.setLineDash(dashPattern);
    
    // Calculate radius for the angle arc
    const arcRadius = 30; // Fixed size in canvas coordinates
    
    // Draw angle arc
    this.ctx.beginPath();
    this.ctx.arc(
      this.toCanvasX(vertex.x),
      this.toCanvasY(vertex.y),
      arcRadius,
      -angle1,
      -angle2,
      angle.angle > Math.PI
    );
    this.ctx.stroke();
    
    // Draw label if it exists
    if (angle.label || this.config.geometryOptions.labelAngles) {
      // Calculate position for label
      const midAngle = (angle1 + angle2) / 2;
      const labelRadius = arcRadius + 10;
      
      const labelX = vertex.x + (labelRadius / arcRadius) * (Math.cos(midAngle) * arcRadius) / 
                    ((this.canvas.width - 2 * this.config.padding) / (this.config.range.xMax - this.config.range.xMin));
      const labelY = vertex.y - (labelRadius / arcRadius) * (Math.sin(midAngle) * arcRadius) / 
                    ((this.canvas.height - 2 * this.config.padding) / (this.config.range.yMax - this.config.range.yMin));
      
      this.ctx.fillStyle = this.config.theme.textColor;
      this.ctx.font = `14px ${this.config.theme.fontFamily}`;
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'middle';
      
      // Display the angle value or label
      const unit = this.config.geometryOptions.angleUnit === 'degrees' ? '°' : ' rad';
      const text = angle.label || `${angle.angleDegrees.toFixed(1)}${unit}`;
      
      this.ctx.fillText(text, this.toCanvasX(labelX), this.toCanvasY(labelY));
    }
  }

  /**
   * Draw all polygons
   */
  drawPolygons() {
    for (const polygon of this.polygons) {
      this.drawPolygon(polygon);
    }
  }

  /**
   * Draw a single polygon
   * @param {Object} polygon - Polygon object
   */
  drawPolygon(polygon) {
    const vertices = polygon.vertices;
    
    // Determine polygon style
    let strokeColor = polygon.color;
    let fillColor = polygon.fillColor;
    let lineWidth = polygon.lineWidth;
    let dashPattern = [];
    
    if (polygon.selected) {
      strokeColor = this.config.theme.secondaryColor;
      lineWidth += 1;
    } else if (polygon.highlighted) {
      strokeColor = this.config.theme.highlightColor;
      lineWidth += 1;
    }
    
    // Draw filled polygon
    this.ctx.fillStyle = fillColor;
    this.ctx.beginPath();
    
    // Move to first vertex
    this.ctx.moveTo(
      this.toCanvasX(vertices[0].x),
      this.toCanvasY(vertices[0].y)
    );
    
    // Draw lines to all other vertices
    for (let i = 1; i < vertices.length; i++) {
      this.ctx.lineTo(
        this.toCanvasX(vertices[i].x),
        this.toCanvasY(vertices[i].y)
      );
    }
    
    // Close the path
    this.ctx.closePath();
    this.ctx.fill();
    
    // Draw polygon outline
    this.ctx.strokeStyle = strokeColor;
    this.ctx.lineWidth = lineWidth;
    this.ctx.setLineDash(dashPattern);
    this.ctx.stroke();
    
    // Draw label if it exists
    if (polygon.label) {
      // Calculate centroid for label position
      let centroidX = 0;
      let centroidY = 0;
      
      for (const vertex of vertices) {
        centroidX += vertex.x;
        centroidY += vertex.y;
      }
      
      centroidX /= vertices.length;
      centroidY /= vertices.length;
      
      this.ctx.fillStyle = this.config.theme.textColor;
      this.ctx.font = `14px ${this.config.theme.fontFamily}`;
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'middle';
      this.ctx.fillText(
        polygon.label,
        this.toCanvasX(centroidX),
        this.toCanvasY(centroidY)
      );
    }
  }

  /**
   * Add a tool button to the control panel
   * @param {string} toolName - Name of the tool
   * @param {string} label - Button label
   * @returns {HTMLButtonElement} Created button
   */
  addToolButton(toolName, label) {
    return this.addControl('button', {
      id: `tool-${toolName}`,
      text: label,
      fullWidth: true,
      onClick: () => {
        this.setTool(toolName);
        
        // Update active tool visual cue
        const buttons = this.controlsArea.querySelectorAll('button');
        buttons.forEach(btn => {
          btn.style.backgroundColor = this.config.theme.buttonColor;
          btn.style.color = this.config.theme.buttonTextColor;
        });
        
        const button = document.getElementById(`tool-${toolName}`);
        if (button) {
          button.style.backgroundColor = this.config.theme.highlightColor;
          button.style.color = 'white';
        }
      }
    });
  }

  /**
   * Add a standard set of geometry tools
   */
  addStandardTools() {
    // Add a heading for tools
    const heading = document.createElement('h3');
    heading.textContent = 'Geometry Tools';
    heading.style.margin = '0 0 10px 0';
    heading.style.fontSize = '16px';
    this.controlsArea.appendChild(heading);
    
    // Selection tool
    this.addToolButton('select', 'Select/Move');
    
    // Basic construction tools
    this.addToolButton('point', 'Point');
    this.addToolButton('line', 'Line');
    this.addToolButton('segment', 'Segment');
    this.addToolButton('ray', 'Ray');
    this.addToolButton('circle', 'Circle');
    this.addToolButton('angle', 'Angle');
    this.addToolButton('polygon', 'Polygon');
    
    // Advanced construction tools
    this.addToolButton('perpendicular', 'Perpendicular Line');
    this.addToolButton('parallel', 'Parallel Line');
    this.addToolButton('bisector', 'Angle Bisector');
    
    // Set select as active by default
    const selectButton = document.getElementById('tool-select');
    if (selectButton) {
      selectButton.style.backgroundColor = this.config.theme.highlightColor;
      selectButton.style.color = 'white';
    }
  }

  /**
   * Clear all geometry elements
   */
  clear() {
    this.points = [];
    this.lines = [];
    this.circles = [];
    this.angles = [];
    this.polygons = [];
    this.selectedElement = null;
    this.pointLabelCounter = 0;
    
    // Clear construction history
    if (this.historyList) {
      this.historyList.innerHTML = '';
    }
    
    // Add clear action to history
    if (this.config.geometryOptions.constructionHistory) {
      this.addToHistory('Cleared all elements');
    }
    
    this.render();
    this.updateMeasurements();
  }

  /**
   * Add a clear button to the control panel
   */
  addClearButton() {
    const separator = document.createElement('hr');
    separator.style.margin = '15px 0';
    separator.style.border = 'none';
    separator.style.borderTop = `1px solid ${this.config.theme.borderColor}`;
    this.controlsArea.appendChild(separator);
    
    this.addControl('button', {
      id: 'clear-button',
      text: 'Clear All',
      fullWidth: true,
      onClick: () => {
        if (confirm('Are you sure you want to clear all elements?')) {
          this.clear();
        }
      }
    });
  }
}

export default GeometryConstruction;