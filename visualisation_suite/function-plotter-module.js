/**
 * MathExplorer - Function Plotter Module
 * 
 * An extension of the base MathExplorer framework that specializes in plotting
 * mathematical functions with interactive parameters and hover information.
 */

import MathExplorer from './base-visualization-framework.js';

class FunctionPlotter extends MathExplorer {
  /**
   * Create a new function plotter
   * @param {Object} config - Configuration settings
   */
  constructor(config) {
    // Set default config values specific to function plotting
    const functionConfig = {
      // Allow different default ranges for function plotting
      range: { xMin: -5, xMax: 5, yMin: -5, yMax: 5 },
      // Enable info panel for function details
      infoPanel: true,
      showCoordinates: true,
      // Additional function plotter specific settings
      plotOptions: {
        resolution: 200, // Number of points to plot
        showSpecialPoints: true, // Show intercepts, extrema, etc.
        highlightSpecialPoints: true,
        lineWidth: 3,
        showHoverInfo: true, // Show hover information
        hoverThreshold: 10, // Pixel distance threshold for hover detection
        enableAxisDrag: true, // Enable dragging axes to pan
        enablePanDrag: true   // Enable dragging anywhere to pan
      },
      ...config
    };
    
    // Call parent constructor
    super(functionConfig);
    
    // Initialize function collections
    this.functions = [];
    this.parameters = {};
    this.specialPoints = []; // Initialize specialPoints array
    this.hoverPoint = null; // Current hover point
    this.axisHoverState = null; // Track if hovering over an axis
    
    // Create hover info element
    this.createHoverInfoElement();
    
    // Always enable hover info by default
    this.config.plotOptions.showHoverInfo = true;
  }
  
  /**
   * Create the hover info element
   */
  createHoverInfoElement() {
    this.hoverInfo = document.createElement('div');
    this.hoverInfo.className = 'math-explorer-hover-info';
    this.hoverInfo.style.position = 'absolute';
    this.hoverInfo.style.backgroundColor = 'rgba(255, 255, 255, 0.9)';
    this.hoverInfo.style.border = '1px solid #ccc';
    this.hoverInfo.style.borderRadius = '4px';
    this.hoverInfo.style.padding = '8px';
    this.hoverInfo.style.pointerEvents = 'none';
    this.hoverInfo.style.boxShadow = '0 2px 5px rgba(0,0,0,0.1)';
    this.hoverInfo.style.fontSize = '14px';
    this.hoverInfo.style.zIndex = '1000';
    this.hoverInfo.style.display = 'none';
    this.canvasArea.appendChild(this.hoverInfo);
  }

  /**
   * Recalculate and store the exact canvas positions of the axes
   */
  recalculateAxisPositions() {
    // Store the exact position of the x and y axes in canvas coordinates
    // This ensures consistent and accurate hover detection
    this.axisPositions = {
      xAxis: this.toCanvasY(0),
      yAxis: this.toCanvasX(0)
    };
  }

  /**
   * Set up event handlers
   * Overrides parent method to add hover functionality
   */
  setupEventHandlers() {
    // Call parent method to set up basic events
    super.setupEventHandlers();
    
    // Initialize drag state
    this.dragState = {
      active: false,
      mode: null,  // 'axis' or 'pan'
      axis: null,  // 'x' or 'y' when mode is 'axis'
      startX: 0,
      startY: 0,
      startRange: null,
      startMathX: 0,
      startMathY: 0
    };
    
    // Determine the exact pixel position of axes for accurate hover detection
    this.recalculateAxisPositions();
    
    // Handle window resize to update axis positions
    window.addEventListener('resize', () => {
      this.recalculateAxisPositions();
    });
    
    // Add direct mouse detection for graph interaction
    this.canvas.addEventListener('mousemove', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      
      // Get exact pixel position relative to canvas
      const x = (e.clientX - rect.left) * (this.canvas.width / rect.width);
      const y = (e.clientY - rect.top) * (this.canvas.height / rect.height);
      
      this.mousePosition = { x, y };
      
      // If dragging, handle the appropriate drag mode
      if (this.dragState.active) {
        if (this.dragState.mode === 'axis') {
          this.handleAxisDrag(x, y);
        } else if (this.dragState.mode === 'pan') {
          this.handlePanDrag(x, y);
        }
        return;
      }
      
      // Convert to math coordinates
      const mathX = this.toMathX(x);
      const mathY = this.toMathY(y);
      
      this.mathMousePosition = { x: mathX, y: mathY };
      
      // Check if mouse is near an axis
      this.checkAxisHover(x, y);
      
      // Do a 2D scan of the graph for function hover
      this.scanGraphForHover();
      
      // Optional: show coordinates in info panel
      if (this.infoPanel && this.config.showCoordinates) {
        this.updateInfoPanel();
      }
    });
    
    // Handle mouse down for drag operations
    this.canvas.addEventListener('mousedown', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const x = (e.clientX - rect.left) * (this.canvas.width / rect.width);
      const y = (e.clientY - rect.top) * (this.canvas.height / rect.height);
      
      // Convert to math coordinates for pan drag
      const mathX = this.toMathX(x);
      const mathY = this.toMathY(y);
      
      // Check if near an axis - prioritize axis drag over pan
      if (this.axisHoverState) {
        // Initialize axis drag operation
        this.dragState = {
          active: true,
          mode: 'axis',
          axis: this.axisHoverState.axis,
          startX: x,
          startY: y,
          startRange: { 
            xMin: this.config.range.xMin, 
            xMax: this.config.range.xMax,
            yMin: this.config.range.yMin,
            yMax: this.config.range.yMax
          }
        };
        
        // Change cursor
        this.canvas.style.cursor = this.axisHoverState.axis === 'x' ? 'ew-resize' : 'ns-resize';
      } 
      // If not near an axis and pan drag is enabled, start pan operation
      else if (this.config.plotOptions.enablePanDrag) {
        this.dragState = {
          active: true,
          mode: 'pan',
          startX: x,
          startY: y,
          startMathX: mathX,
          startMathY: mathY,
          startRange: { 
            xMin: this.config.range.xMin, 
            xMax: this.config.range.xMax,
            yMin: this.config.range.yMin,
            yMax: this.config.range.yMax
          }
        };
        
        // Change cursor to grabbing/moving
        this.canvas.style.cursor = 'grabbing';
      }
      
      // Prevent text selection during drag
      e.preventDefault();
    });
    
    // Handle mouse up to end drag operations using our custom handler
    this.canvas.addEventListener('mouseup', (e) => this.handleMouseUp(e));
    
    // Also end drag if mouse leaves the canvas
    this.canvas.addEventListener('mouseleave', () => {
      if (this.dragState.active) {
        this.dragState.active = false;
        this.canvas.style.cursor = 'default';
        // Make sure to recalculate axis positions
        this.recalculateAxisPositions();
      }
      
      this.hoverInfo.style.display = 'none';
      this.hoverPoint = null;
      this.axisHoverState = null;
      this.render();
    });
    
    // Set default cursor for pan-enabled graphs
    if (this.config.plotOptions.enablePanDrag) {
      this.canvas.style.cursor = 'grab';
    }
  }

  /**
   * Check if mouse is hovering near an axis
   * @param {number} x - Canvas x coordinate
   * @param {number} y - Canvas y coordinate
   */
  checkAxisHover(x, y) {
    // Check if axis dragging is enabled
    if (!this.config.plotOptions.enableAxisDrag) {
      return;
    }
    
    // Calculate position of the x and y axes in canvas coordinates
    const originX = this.axisPositions.yAxis;
    const originY = this.axisPositions.xAxis;
    
    // Apply the 10% offset for axis detection as requested
    const offsetX = this.canvas.width * 0.1;  // 10% of canvas width right offset
    const offsetY = this.canvas.height * 0.1; // 10% of canvas height down offset
    
    // Define hover thresholds (in pixels)
    const threshold = 15;
    
    // Check proximity to x-axis with offset
    const isNearXAxis = Math.abs(y - (originY + offsetY)) < threshold;
    
    // Check proximity to y-axis with offset
    const isNearYAxis = Math.abs(x - (originX + offsetX)) < threshold;
    
    // Determine which axis has priority if near both
    if (isNearXAxis && isNearYAxis) {
      // If near the origin, determine by which is closer
      const distToXAxis = Math.abs(y - (originY + offsetY));
      const distToYAxis = Math.abs(x - (originX + offsetX));
      
      if (distToXAxis < distToYAxis) {
        this.axisHoverState = { 
          axis: 'x', 
          position: originY // Use original y position of x-axis
        };
        this.canvas.style.cursor = 'ew-resize';
      } else {
        this.axisHoverState = { 
          axis: 'y', 
          position: originX // Use original x position of y-axis
        };
        this.canvas.style.cursor = 'ns-resize';
      }
    } else if (isNearXAxis) {
      this.axisHoverState = { 
        axis: 'x', 
        position: originY // Use original y position of x-axis
      };
      this.canvas.style.cursor = 'ew-resize';
    } else if (isNearYAxis) {
      this.axisHoverState = { 
        axis: 'y', 
        position: originX // Use original x position of y-axis
      };
      this.canvas.style.cursor = 'ns-resize';
    } else {
      // Not near any axis
      if (this.axisHoverState && (!this.dragState || !this.dragState.active)) {
        // If pan is enabled, set cursor to grab, otherwise default
        if (this.config.plotOptions.enablePanDrag) {
          this.canvas.style.cursor = 'grab';
        } else {
          this.canvas.style.cursor = 'default';
        }
        this.axisHoverState = null;
      }
    }
  }
  
  /**
   * Handle mouseup event at the end of a drag operation
   * @param {Event} e - Mouse event
   */
  handleMouseUp(e) {
    if (this.dragState.active) {
      // Store if we were in pan mode
      const wasPanning = this.dragState.mode === 'pan';
      
      // Reset drag state
      this.dragState.active = false;
      
      // Recalculate the axis positions explicitly
      this.recalculateAxisPositions();
      
      // Reset cursor based on context
      if (this.axisHoverState) {
        this.canvas.style.cursor = this.axisHoverState.axis === 'x' ? 'ew-resize' : 'ns-resize';
      } else if (this.config.plotOptions.enablePanDrag) {
        this.canvas.style.cursor = 'grab';
      } else {
        this.canvas.style.cursor = 'default';
      }
      
      // If we were panning, do a fresh axis hover check with new positions
      if (wasPanning) {
        // Get current mouse position
        const rect = this.canvas.getBoundingClientRect();
        const x = (e.clientX - rect.left) * (this.canvas.width / rect.width);
        const y = (e.clientY - rect.top) * (this.canvas.height / rect.height);
        
        // Force a new axis hover check with updated positions
        this.checkAxisHover(x, y);
      }
    }
  }
  
  /**
   * Handle dragging of an axis for zooming
   * @param {number} x - Current mouse x position (canvas coordinates)
   * @param {number} y - Current mouse y position (canvas coordinates)
   */
  handleAxisDrag(x, y) {
    if (!this.dragState || !this.dragState.active || this.dragState.mode !== 'axis') return;
    
    if (this.dragState.axis === 'x') {
      // Calculate zoom factor based on horizontal movement
      // Dragging right = zoom in, dragging left = zoom out
      const dragDistance = x - this.dragState.startX;
      const zoomFactor = 1 - (dragDistance / this.canvas.width) * 2;
      
      // Get the original range
      const origRange = this.dragState.startRange;
      const origWidth = origRange.xMax - origRange.xMin;
      const midPoint = (origRange.xMax + origRange.xMin) / 2;
      
      // Calculate new range while keeping the midpoint fixed
      const newWidth = origWidth * zoomFactor;
      
      // Update the x range
      this.setRange({
        xMin: midPoint - newWidth / 2,
        xMax: midPoint + newWidth / 2
      });
      
    } else if (this.dragState.axis === 'y') {
      // Calculate zoom factor based on vertical movement
      // Dragging down = zoom out, dragging up = zoom in
      const dragDistance = y - this.dragState.startY;
      const zoomFactor = 1 + (dragDistance / this.canvas.height) * 2;
      
      // Get the original range
      const origRange = this.dragState.startRange;
      const origHeight = origRange.yMax - origRange.yMin;
      const midPoint = (origRange.yMax + origRange.yMin) / 2;
      
      // Calculate new range while keeping the midpoint fixed
      const newHeight = origHeight * zoomFactor;
      
      // Update the y range
      this.setRange({
        yMin: midPoint - newHeight / 2,
        yMax: midPoint + newHeight / 2
      });
    }
  }
  
  /**
   * Handle panning by dragging the graph
   * @param {number} x - Current mouse x position (canvas coordinates)
   * @param {number} y - Current mouse y position (canvas coordinates)
   */
  handlePanDrag(x, y) {
    if (!this.dragState || !this.dragState.active || this.dragState.mode !== 'pan') return;
    
    // Calculate the deltas in canvas pixels
    const deltaX = x - this.dragState.startX;
    const deltaY = y - this.dragState.startY;
    
    // Convert pixel movements to math coordinate scale
    // This calculation ensures consistent movement regardless of zoom level
    const rangeWidth = this.config.range.xMax - this.config.range.xMin;
    const rangeHeight = this.config.range.yMax - this.config.range.yMin;
    
    const canvasWidth = this.canvas.width;
    const canvasHeight = this.canvas.height;
    
    // Scale the movements by the current range/canvas ratio
    const deltaXMath = -deltaX * (rangeWidth / canvasWidth);
    const deltaYMath = deltaY * (rangeHeight / canvasHeight);
    
    // Get the original range
    const origRange = this.dragState.startRange;
    
    // Update the ranges by shifting by the delta
    this.setRange({
      xMin: origRange.xMin + deltaXMath,
      xMax: origRange.xMax + deltaXMath,
      yMin: origRange.yMin + deltaYMath,
      yMax: origRange.yMax + deltaYMath
    });
  }
  
  /**
   * Draw the axis hover state
   */
  drawAxisHoverState() {
    // If not hovering over an axis and not dragging, don't draw anything
    if (!this.axisHoverState && !(this.dragState && this.dragState.active)) return;
    
    // We will not draw any visual indicators for the hover state
    // per user's request - just maintain the cursor change in checkAxisHover
  }

  /**
   * Scan the graph in 2D to find the nearest point on any function
   */
  scanGraphForHover() {
    if (!this.config.plotOptions.showHoverInfo || !this.mathMousePosition) return;
    
    const mouseX = this.mathMousePosition.x;
    const mouseY = this.mathMousePosition.y;
    
    // We'll scan the x values near the mouse position
    // to find the closest point on any function
    const scanRange = (this.config.range.xMax - this.config.range.xMin) / 100; // 1% of x range
    const numSamples = 21; // Use an odd number to include the exact mouse x
    const stepSize = scanRange / (numSamples - 1);
    
    let bestDistance = Infinity;
    let closestPoint = null;
    
    // For each function, scan points around mouse x to find closest
    this.functions.forEach(func => {
      if (!func.visible) return;
      
      for (let i = 0; i < numSamples; i++) {
        // Calculate x value for this sample
        const x = mouseX - scanRange/2 + (i * stepSize);
        
        try {
          // Evaluate the function at this x
          const y = func.evaluator(x);
          
          if (isFinite(y)) {
            // Calculate distance to mouse in math coordinates
            const dx = x - mouseX;
            const dy = y - mouseY;
            const distance = Math.sqrt(dx*dx + dy*dy);
            
            // If this is closer than our current best, update
            if (distance < bestDistance) {
              bestDistance = distance;
              
              closestPoint = {
                function: func,
                x: x,
                y: y,
                distance: distance,
                canvasX: this.toCanvasX(x),
                canvasY: this.toCanvasY(y)
              };
            }
          }
        } catch (e) {
          // Skip error cases
          continue;
        }
      }
    });
    
    // If we found a close point, update hover
    if (closestPoint && bestDistance < (this.config.range.yMax - this.config.range.yMin) / 15) {
      // Format the hover information
      let infoHTML = `
        <div style="font-weight: bold; margin-bottom: 4px;">x = ${closestPoint.x.toFixed(4)}</div>
      `;
      
      infoHTML += `
        <div style="display: flex; align-items: center; margin: 2px 0;">
          <span style="display: inline-block; width: 12px; height: 12px; background-color: ${closestPoint.function.color}; margin-right: 5px;"></span>
          <span>y = ${closestPoint.y.toFixed(4)}</span>
        </div>
      `;
      
      // Add any special points that are nearby
      const specialPointsNearby = this.findNearbySpecialPoints(closestPoint.x, closestPoint.y);
      if (specialPointsNearby.length > 0) {
        infoHTML += `<div style="margin-top: 5px; border-top: 1px solid #ddd; padding-top: 5px;">`;
        specialPointsNearby.forEach(point => {
          infoHTML += `<div>${point.type}: (${point.x.toFixed(4)}, ${point.y.toFixed(4)})</div>`;
        });
        infoHTML += `</div>`;
      }
      
      // Update and position the hover info
      this.hoverInfo.innerHTML = infoHTML;
      this.hoverInfo.style.display = 'block';
      
      // Position the hover info - avoid edge overflow
      const infoRect = this.hoverInfo.getBoundingClientRect();
      const containerRect = this.canvasArea.getBoundingClientRect();
      
      // Position relative to the point on the curve, not the mouse cursor
      let leftPos = closestPoint.canvasX + 15; 
      let topPos = closestPoint.canvasY - infoRect.height / 2;
      
      // Check right edge
      if (leftPos + infoRect.width > containerRect.width) {
        leftPos = closestPoint.canvasX - infoRect.width - 10;
      }
      
      // Check top/bottom edges
      if (topPos < 0) {
        topPos = 0;
      } else if (topPos + infoRect.height > containerRect.height) {
        topPos = containerRect.height - infoRect.height;
      }
      
      this.hoverInfo.style.left = `${leftPos}px`;
      this.hoverInfo.style.top = `${topPos}px`;
      
      // Save hover point for rendering
      this.hoverPoint = closestPoint;
      
      // Force redraw
      this.render();
    } else {
      // No close points found
      this.hoverInfo.style.display = 'none';
      this.hoverPoint = null;
      this.render();
    }
  }

  /**
   * Find special points near the mouse position
   * @param {number} mouseX - Math X coordinate of mouse
   * @param {number} mouseY - Math Y coordinate of mouse
   * @returns {Array} Array of nearby special points
   */
  findNearbySpecialPoints(mouseX, mouseY) {
    if (!this.specialPoints) return [];
    
    // Use a more generous euclidean distance threshold 
    const thresholdInMathUnits = (this.config.range.xMax - this.config.range.xMin) / 20;
    
    return this.specialPoints.filter(point => {
      const dx = Math.abs(point.x - mouseX);
      const dy = Math.abs(point.y - mouseY);
      // Use euclidean distance instead of separate thresholds
      return Math.sqrt(dx*dx + dy*dy) < thresholdInMathUnits;
    });
  }

  /**
   * Add a function to the plotter
   * @param {Object} funcConfig - Function configuration
   * @returns {Object} Function object
   */
  addFunction(funcConfig) {
    const defaultConfig = {
      id: `func-${this.functions.length + 1}`,
      expression: 'x', // Default to y = x
      color: this.config.theme.highlightColor,
      lineWidth: this.config.plotOptions.lineWidth,
      visible: true,
      specialPoints: []
    };
    
    const func = { ...defaultConfig, ...funcConfig };
    
    // Add evaluator function
    if (typeof func.expression === 'string') {
      // Create evaluator from string expression
      try {
        // Safe function creation
        func.evaluator = this.createFunctionEvaluator(func.expression);
      } catch (error) {
        console.error(`Error creating function from: ${func.expression}`, error);
        func.evaluator = () => 0; // Default to y = 0 on error
      }
    } else if (typeof func.expression === 'function') {
      func.evaluator = func.expression;
    } else {
      throw new Error('Function expression must be a string or function');
    }
    
    this.functions.push(func);
    this.render();
    
    return func;
  }

  /**
   * Create a function evaluator from a string expression
   * @param {string} expression - Math expression string
   * @returns {Function} Function evaluator
   */
  createFunctionEvaluator(expression) {
    // This implementation uses Function constructor, which is generally not recommended
    // for user-provided input due to security concerns. In a real app, you might want
    // to use a math expression parser library like math.js
    
    // Fix: Pass Math directly to the function context to allow Math functions
    // Use a different approach for parameter replacement to avoid capturing "Math"
    const reservedWords = ['Math', 'parseInt', 'parseFloat', 'Number', 'String', 'Boolean', 'Date', 
                          'Array', 'Object', 'RegExp', 'Error', 'Symbol', 'Map', 'Set', 'Promise',
                          'x', 'NaN', 'Infinity', 'undefined', 'null', 'true', 'false'];
    
    // Create a safer parameter replacement mechanism
    let parameterizedExpression = expression;
    
    // Get all potential parameter names from the expression
    const paramRegex = /\b([a-zA-Z_][a-zA-Z0-9_]*)\b(?!\s*\()/g;
    const matches = [...expression.matchAll(paramRegex)];
    
    // Process matches from longest to shortest to avoid partial replacements
    const potentialParams = matches.map(m => m[1])
                                  .filter(name => !reservedWords.includes(name))
                                  .sort((a, b) => b.length - a.length);
    
    // Replace only actual parameter names, not built-in objects or functions
    for (const param of potentialParams) {
      // Use a more specific regex to target just this parameter name
      const specificRegex = new RegExp(`\\b(${param})\\b(?!\\s*\\()`, 'g');
      parameterizedExpression = parameterizedExpression.replace(
        specificRegex, 
        `this.parameters["${param}"]`
      );
    }
    
    // Create the function evaluator with direct Math access
    return new Function('x', `
      try {
        // Make Math available directly
        const Math = window.Math;
        return ${parameterizedExpression};
      } catch (e) {
        console.error("Error evaluating function", e);
        return NaN;
      }
    `).bind(this);
  }

  /**
   * Add a parameter control
   * @param {string} name - Parameter name
   * @param {number} initialValue - Initial value
   * @param {Object} options - Slider options
   * @returns {HTMLElement} The created slider element
   */
  addParameter(name, initialValue, options = {}) {
    // Set the parameter value
    this.parameters[name] = initialValue;
    
    // Create slider control
    const sliderOptions = {
      id: `param-${name}`,
      label: options.label || name,
      min: options.min !== undefined ? options.min : -10,
      max: options.max !== undefined ? options.max : 10,
      step: options.step !== undefined ? options.step : 0.1,
      value: initialValue,
      precision: options.precision !== undefined ? options.precision : 1,
      onChange: (value) => {
        this.parameters[name] = value;
        
        // Calculate special points if needed
        if (this.config.plotOptions.showSpecialPoints) {
          this.calculateSpecialPoints();
        }
        
        this.render();
      }
    };
    
    return this.addControl('slider', sliderOptions);
  }

  /**
   * Remove a function from the plotter
   * @param {string|Object} funcId - Function ID or function object
   */
  removeFunction(funcId) {
    const id = typeof funcId === 'object' ? funcId.id : funcId;
    const index = this.functions.findIndex(f => f.id === id);
    
    if (index !== -1) {
      this.functions.splice(index, 1);
      this.render();
    }
  }

  /**
   * Calculate special points for all functions
   */
  calculateSpecialPoints() {
    // Make sure specialPoints is initialized
    if (!this.specialPoints) {
      this.specialPoints = [];
    } else {
      // Clear existing points
      this.specialPoints = [];
    }
    
    // Make sure functions are initialized
    if (!this.functions) {
      this.functions = [];
      return;
    }
    
    this.functions.forEach(func => {
      if (!func.visible) return;
      
      // Make sure function has specialPoints array
      if (!func.specialPoints) {
        func.specialPoints = [];
      } else {
        // Clear existing special points
        func.specialPoints = [];
      }
      
      // Calculate based on function type
      // This is a simplified example - real implementation would be more complex
      
      // X-intercepts (points where y = 0)
      // For simple cases, we'll just check if the function changes sign
      this.findZeroCrossings(func);
      
      // Y-intercept (point where x = 0)
      try {
        const yIntercept = func.evaluator(0);
        if (!isNaN(yIntercept) && isFinite(yIntercept)) {
          func.specialPoints.push({
            type: 'y-intercept',
            x: 0,
            y: yIntercept
          });
        }
      } catch (e) {
        console.error("Error calculating y-intercept", e);
      }
      
      // Add function's special points to the full list
      this.specialPoints.push(...func.specialPoints);
    });
  }

  /**
   * Find zero crossings (x-intercepts) of a function
   * @param {Object} func - Function object
   */
  findZeroCrossings(func) {
    const { xMin, xMax } = this.config.range;
    const resolution = 100; // Number of segments to check
    const step = (xMax - xMin) / resolution;
    
    let prevX = xMin;
    let prevY;
    
    try {
      prevY = func.evaluator(prevX);
    } catch (e) {
      console.error("Error evaluating function", e);
      return;
    }
    
    for (let i = 1; i <= resolution; i++) {
      const x = xMin + i * step;
      let y;
      
      try {
        y = func.evaluator(x);
      } catch (e) {
        console.error("Error evaluating function", e);
        continue;
      }
      
      // Check for sign change (zero crossing)
      if (isFinite(prevY) && isFinite(y) && (prevY * y <= 0) && (prevY !== 0 || y !== 0)) {
        // Refine the zero crossing with binary search
        try {
          const root = this.refineCrossing(func, prevX, x, prevY, y);
          
          func.specialPoints.push({
            type: 'x-intercept',
            x: root,
            y: 0
          });
        } catch (e) {
          console.error("Error refining crossing", e);
        }
      }
      
      prevX = x;
      prevY = y;
    }
  }

  /**
   * Refine a zero crossing using binary search
   * @param {Object} func - Function object
   * @param {number} x1 - Left x value
   * @param {number} x2 - Right x value
   * @param {number} y1 - Left y value
   * @param {number} y2 - Right y value
   * @returns {number} Refined x value of the crossing
   */
  refineCrossing(func, x1, x2, y1, y2) {
    const tolerance = 1e-6;
    const maxIterations = 20;
    
    let a = x1;
    let b = x2;
    let fa = y1;
    let fb = y2;
    
    // If one of the endpoints is exactly zero, return it
    if (Math.abs(fa) < tolerance) return a;
    if (Math.abs(fb) < tolerance) return b;
    
    // Binary search loop
    for (let i = 0; i < maxIterations; i++) {
      const c = (a + b) / 2;
      let fc;
      
      try {
        fc = func.evaluator(c);
      } catch (e) {
        console.error("Error evaluating function", e);
        // Return the midpoint as a fallback
        return (a + b) / 2;
      }
      
      if (Math.abs(fc) < tolerance) {
        return c;
      }
      
      if (fc * fa < 0) {
        b = c;
        fb = fc;
      } else {
        a = c;
        fa = fc;
      }
      
      if (Math.abs(b - a) < tolerance) {
        return (a + b) / 2;
      }
    }
    
    return (a + b) / 2;
  }

  /**
   * Plot all active functions
   */
  plotFunctions() {
    // Make sure functions is initialized
    if (!this.functions) {
      this.functions = [];
      return;
    }
    
    // Get the actual canvas dimensions in math coordinates
    const canvasLeft = this.toMathX(0);
    const canvasRight = this.toMathX(this.canvas.width);
    const canvasTop = this.toMathY(0);
    const canvasBottom = this.toMathY(this.canvas.height);
    
    // These are the true visual boundaries of the canvas
    const visualBounds = {
      xMin: Math.min(canvasLeft, canvasRight),
      xMax: Math.max(canvasLeft, canvasRight),
      yMin: Math.min(canvasTop, canvasBottom),
      yMax: Math.max(canvasTop, canvasBottom)
    };
    
    // Use the full canvas width for plotting
    const plotXMin = this.toMathX(0);
    const plotXMax = this.toMathX(this.canvas.width);
    const plotYMin = this.toMathY(this.canvas.height);
    const plotYMax = this.toMathY(0);
    
    this.functions.forEach(func => {
      if (!func.visible) return;
      
      // Use the full canvas dimensions for plotting
      // (with a bit of padding to ensure we capture any edge behavior)
      const resolution = this.config.plotOptions.resolution * 3; // Tripled for smoother curves
      const step = (plotXMax - plotXMin) / resolution;
      
      // Save current context state
      this.ctx.save();
      
      // Set function-specific styles
      this.ctx.strokeStyle = func.color;
      this.ctx.lineWidth = func.lineWidth;
      this.ctx.beginPath();
      
      let isDrawing = false;
      let lastX = null;
      let lastY = null;
      
      // For determining function range
      let minY = Infinity;
      let maxY = -Infinity;
      
      // Calculate points for every pixel across the canvas width
      for (let i = 0; i <= resolution; i++) {
        const x = plotXMin + i * step;
        
        try {
          const y = func.evaluator(x);
          
          // Update function range tracking
          if (isFinite(y)) {
            minY = Math.min(minY, y);
            maxY = Math.max(maxY, y);
          }
          
          // Check if point is inside the visual area with some extra margin
          // Note: we plot slightly outside the visible area to ensure smooth edge behavior
          const isInRange = isFinite(y);
          
          if (isInRange) {
            const canvasX = this.toCanvasX(x);
            const canvasY = this.toCanvasY(y);
            
            // Start a new path if needed
            if (!isDrawing) {
              this.ctx.moveTo(canvasX, canvasY);
              isDrawing = true;
            } else {
              // Check for potential discontinuities or very steep changes
              if (lastY !== null) {
                const dy = Math.abs(y - lastY);
                const maxAllowedChange = (plotYMax - plotYMin) / 2; // Half the range is a reasonable threshold
                
                if (dy > maxAllowedChange) {
                  // Potential discontinuity - start a new segment
                  this.ctx.stroke();
                  this.ctx.beginPath();
                  this.ctx.moveTo(canvasX, canvasY);
                } else {
                  // Regular point - continue the line
                  this.ctx.lineTo(canvasX, canvasY);
                }
              } else {
                this.ctx.lineTo(canvasX, canvasY);
              }
            }
          } else {
            // Point not in range - end current path if we were drawing
            if (isDrawing) {
              this.ctx.stroke();
              isDrawing = false;
            }
          }
          
          lastX = x;
          lastY = y;
        } catch (e) {
          console.error("Error evaluating function", e);
          if (isDrawing) {
            this.ctx.stroke();
            isDrawing = false;
          }
        }
      }
      
      // Finish drawing the path
      if (isDrawing) {
        this.ctx.stroke();
      }
      
      // Restore context state
      this.ctx.restore();
      
      // Update function properties with calculated range
      if (isFinite(minY) && isFinite(maxY)) {
        func.calculatedRange = { min: minY, max: maxY };
      }
    });
  }

  /**
   * Set the coordinate range with extended boundaries
   * @param {Object} range - New coordinate range
   */
  setRange(range) {
    // Store previous range for transition effects if needed
    const prevRange = {...this.config.range};
    
    // Update the range
    this.config.range = { ...this.config.range, ...range };
    
    // Calculate grid boundaries that extend beyond the tick marks
    const gridPadding = 0.1; // 10% padding
    
    // Store extended ranges for plotting functions (but keep display ranges as is)
    this.config.extendedRange = {
      xMin: this.config.range.xMin - (this.config.range.xMax - this.config.range.xMin) * gridPadding,
      xMax: this.config.range.xMax + (this.config.range.xMax - this.config.range.xMin) * gridPadding,
      yMin: this.config.range.yMin - (this.config.range.yMax - this.config.range.yMin) * gridPadding,
      yMax: this.config.range.yMax + (this.config.range.yMax - this.config.range.yMin) * gridPadding
    };
    
    // Recalculate axis positions after range change
    this.recalculateAxisPositions();
    
    // Reset any hover or drag state when range changes significantly
    // This prevents unexpected behavior when axes move dramatically
    if (Math.abs(prevRange.xMin - this.config.range.xMin) > 0.5 ||
        Math.abs(prevRange.xMax - this.config.range.xMax) > 0.5 ||
        Math.abs(prevRange.yMin - this.config.range.yMin) > 0.5 ||
        Math.abs(prevRange.yMax - this.config.range.yMax) > 0.5) {
      this.axisHoverState = null;
    }
    
    this.render();
  }
  
  /**
   * Plot special points (intercepts, extrema, etc.)
   */
  plotSpecialPoints() {
    // Make sure specialPoints is initialized
    if (!this.specialPoints) {
      this.specialPoints = [];
      return;
    }
    
    if (!this.config.plotOptions.showSpecialPoints) return;
    
    // Save current context state
    this.ctx.save();
    
    // Define colors for different types of special points
    const colors = {
      'x-intercept': this.config.theme.secondaryColor,
      'y-intercept': this.config.theme.highlightColor,
      'extrema': this.config.theme.tertiaryColor
    };
    
    // Plot each special point
    this.specialPoints.forEach(point => {
      const x = this.toCanvasX(point.x);
      const y = this.toCanvasY(point.y);
      
      this.ctx.fillStyle = colors[point.type] || this.config.theme.highlightColor;
      this.ctx.beginPath();
      this.ctx.arc(x, y, 5, 0, 2 * Math.PI);
      this.ctx.fill();
    });
    
    // Restore context state
    this.ctx.restore();
  }

  /**
   * Draw hover highlight
   */
  drawHoverHighlight() {
    if (!this.hoverPoint || !this.config.plotOptions.showHoverInfo) return;
    
    this.ctx.save();
    
    // Draw vertical line at x position (full canvas height)
    this.ctx.setLineDash([5, 3]);
    this.ctx.strokeStyle = 'rgba(0, 0, 0, 0.5)';
    this.ctx.lineWidth = 1;
    this.ctx.beginPath();
    this.ctx.moveTo(this.hoverPoint.canvasX, 0);
    this.ctx.lineTo(this.hoverPoint.canvasX, this.canvas.height);
    this.ctx.stroke();
    
    // Draw horizontal line (full canvas width)
    this.ctx.beginPath();
    this.ctx.moveTo(0, this.hoverPoint.canvasY);
    this.ctx.lineTo(this.canvas.width, this.hoverPoint.canvasY);
    this.ctx.stroke();
    
    // Draw point highlight
    this.ctx.setLineDash([]);
    this.ctx.fillStyle = this.hoverPoint.function.color;
    this.ctx.strokeStyle = '#fff';
    this.ctx.lineWidth = 2;
    this.ctx.beginPath();
    this.ctx.arc(
      this.hoverPoint.canvasX, 
      this.hoverPoint.canvasY, 
      6, 0, 2 * Math.PI
    );
    this.ctx.fill();
    this.ctx.stroke();
    
    this.ctx.restore();
  }

  /**
   * Set the theme
   * @param {string|Object} theme - Theme name or theme object
   */
  setTheme(theme) {
    // Call parent setTheme method
    super.setTheme(theme);
    
    // Update hover info styles
    if (this.hoverInfo) {
      // Set hover info styles based on theme
      const isDarkTheme = theme === 'dark' || 
                         (this.config.theme && this.config.theme.backgroundColor === MathExplorer.themes.dark.backgroundColor);
      
      if (isDarkTheme) {
        this.hoverInfo.style.backgroundColor = 'rgba(44, 62, 80, 0.9)';
        this.hoverInfo.style.borderColor = '#1a2530';
        this.hoverInfo.style.color = '#ecf0f1';
      } else {
        this.hoverInfo.style.backgroundColor = 'rgba(255, 255, 255, 0.9)';
        this.hoverInfo.style.borderColor = '#cccccc';
        this.hoverInfo.style.color = '#333333';
      }
    }
  }

  /**
   * Render the function plots
   */
  render() {
    // Call parent's render method to clear and draw grid/axes
    super.render();
    
    // Initialize specialPoints if needed
    if (!this.specialPoints) {
      this.specialPoints = [];
    }
    
    // Calculate special points if needed
    if (this.config.plotOptions.showSpecialPoints && this.specialPoints.length === 0) {
      this.calculateSpecialPoints();
    }
    
    // Plot functions
    this.plotFunctions();
    
    // Plot special points
    this.plotSpecialPoints();
    
    // Draw axis hover/drag state
    this.drawAxisHoverState();
    
    // Draw hover highlight
    this.drawHoverHighlight();
    
    // Update info panel
    this.updateFunctionInfo();
    
    // In case of padding or other layout issues, debug by marking the edges
    if (this.config.debug) {
      this.debugDrawCanvasBounds();
    }
  }

  /**
   * Draw debug information about canvas boundaries
   * Only activated when config.debug is true
   */
  debugDrawCanvasBounds() {
    this.ctx.save();
    
    // Draw markers at corners and center
    this.ctx.fillStyle = 'red';
    
    // Corners
    this.ctx.beginPath();
    this.ctx.arc(0, 0, 5, 0, 2 * Math.PI); // Top-left
    this.ctx.fill();
    
    this.ctx.beginPath();
    this.ctx.arc(this.canvas.width, 0, 5, 0, 2 * Math.PI); // Top-right
    this.ctx.fill();
    
    this.ctx.beginPath();
    this.ctx.arc(0, this.canvas.height, 5, 0, 2 * Math.PI); // Bottom-left
    this.ctx.fill();
    
    this.ctx.beginPath();
    this.ctx.arc(this.canvas.width, this.canvas.height, 5, 0, 2 * Math.PI); // Bottom-right
    this.ctx.fill();
    
    // Center
    this.ctx.fillStyle = 'blue';
    this.ctx.beginPath();
    this.ctx.arc(this.canvas.width/2, this.canvas.height/2, 5, 0, 2 * Math.PI);
    this.ctx.fill();
    
    // Origin
    this.ctx.fillStyle = 'green';
    this.ctx.beginPath();
    this.ctx.arc(this.toCanvasX(0), this.toCanvasY(0), 5, 0, 2 * Math.PI);
    this.ctx.fill();
    
    this.ctx.restore();
  }

  /**
   * Update function information in the info panel
   */
  updateFunctionInfo() {
    if (!this.infoPanel) return;
    
    // Clear existing info
    this.infoPanel.innerHTML = '';
    
    // Create a title
    const title = document.createElement('h3');
    title.style.margin = '0 0 10px 0';
    title.style.fontSize = '16px';
    title.textContent = 'Function Properties';
    this.infoPanel.appendChild(title);
    
    // Show expressions
    this.functions.forEach(func => {
      if (!func.visible) return;
      
      const expressionContainer = document.createElement('div');
      expressionContainer.style.marginBottom = '5px';
      
      // Add color indicator
      const colorIndicator = document.createElement('span');
      colorIndicator.style.display = 'inline-block';
      colorIndicator.style.width = '12px';
      colorIndicator.style.height = '12px';
      colorIndicator.style.backgroundColor = func.color;
      colorIndicator.style.marginRight = '5px';
      expressionContainer.appendChild(colorIndicator);
      
      // Add function expression
      const expressionText = document.createElement('span');
      expressionText.textContent = `f(x) = ${func.expression}`;
      expressionContainer.appendChild(expressionText);
      
      this.infoPanel.appendChild(expressionContainer);
      
      // Add special points for this function
      if (func.specialPoints && func.specialPoints.length > 0) {
        const pointsContainer = document.createElement('div');
        pointsContainer.style.marginLeft = '17px';
        pointsContainer.style.marginBottom = '10px';
        pointsContainer.style.fontSize = '14px';
        
        func.specialPoints.forEach(point => {
          const pointText = document.createElement('div');
          let formattedX = '0';
          let formattedY = '0';
          
          // Safely format numbers
          try {
            formattedX = typeof point.x === 'number' ? 
              point.x.toFixed(2) : point.x.toString();
            formattedY = typeof point.y === 'number' ? 
              point.y.toFixed(2) : point.y.toString();
          } catch (e) {
            console.error("Error formatting point coordinates", e);
          }
          
          switch (point.type) {
            case 'x-intercept':
              pointText.textContent = `x-intercept: (${formattedX}, 0)`;
              break;
            case 'y-intercept':
              pointText.textContent = `y-intercept: (0, ${formattedY})`;
              break;
            default:
              pointText.textContent = `${point.type}: (${formattedX}, ${formattedY})`;
          }
          
          pointsContainer.appendChild(pointText);
        });
        
        this.infoPanel.appendChild(pointsContainer);
      }
    });
  }

  /**
   * Change the properties of a function
   * @param {string} id - Function ID
   * @param {Object} properties - New properties
   */
  updateFunction(id, properties) {
    // Make sure functions is initialized
    if (!this.functions) {
      this.functions = [];
      return;
    }
    
    const func = this.functions.find(f => f.id === id);
    
    if (func) {
      // Update properties
      Object.assign(func, properties);
      
      // If expression changed, update evaluator
      if (properties.expression) {
        try {
          func.evaluator = this.createFunctionEvaluator(properties.expression);
        } catch (error) {
          console.error(`Error updating function: ${error.message}`);
          // Keep the old evaluator
        }
      }
      
      // Recalculate special points and render
      this.calculateSpecialPoints();
      this.render();
    }
  }
}

export default FunctionPlotter;