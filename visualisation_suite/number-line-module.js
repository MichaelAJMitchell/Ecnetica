/**
 * MathExplorer - Number Line & Inequalities Module
 * 
 * An extension of the base MathExplorer framework specialized for number line
 * visualizations, inequalities, and interval representations.
 */

import MathExplorer from './base-visualization-framework.js';

class NumberLineVisualizer extends MathExplorer {
  /**
   * Create a new number line visualization environment
   * @param {Object} config - Configuration settings
   */
  constructor(config) {
    // Set default config values specific to number line visualization
    const numberLineConfig = {
      // Use a horizontally-focused coordinate range
      range: { xMin: -10, xMax: 10, yMin: -2, yMax: 2 },
      // Enable info panel for detailed information
      infoPanel: true,
      // Number line specific settings
      numberLineOptions: {
        lineHeight: 0.2,
        pointRadius: 5,
        tickLength: 0.3,
        showLabels: true,
        labelInterval: 1,
        minorTickInterval: 0.5,
        directionalHandles: true,
        multipleNumberLines: false,
        colorCoding: true,
        numberLinesSpacing: 1,
        showOrigin: true
      },
      ...config
    };
    
    // Call parent constructor
    super(numberLineConfig);
    
    // Initialize collections for inequalities and intervals
    this.inequalities = [];
    this.intervals = [];
    this.points = [];
    this.numberLines = [];
    
    // Reference to the current working number line
    this.activeNumberLine = null;
    
    // For dragging operations
    this.dragState = {
      isDragging: false,
      element: null,
      startX: 0,
      startY: 0
    };
    
    // Set up event handlers
    this.setupNumberLineEventHandlers();
    
    // Create default number line
    this.createNumberLine();
  }

  /**
   * Set up event handlers for number line interactions
   */
  setupNumberLineEventHandlers() {
    // Mouse down for selecting and starting drags
    this.canvas.addEventListener('mousedown', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      // Convert to math coordinates
      const mathX = this.toMathX(x);
      const mathY = this.toMathY(y);
      
      // Find if clicking on any element
      const element = this.findElementAt(mathX, mathY);
      
      if (element) {
        // Start dragging if element is draggable
        if (element.draggable) {
          this.dragState = {
            isDragging: true,
            element: element,
            startX: mathX,
            startY: mathY
          };
          
          this.canvas.style.cursor = 'grabbing';
        }
        
        // Select the element
        this.selectElement(element);
      } else {
        // Deselect if clicking on empty space
        this.deselectElement();
        
        // Create new point if in point creation mode
        if (this.currentTool === 'point') {
          this.createPoint(mathX);
        }
      }
      
      this.render();
    });
    
    // Mouse move for dragging
    this.canvas.addEventListener('mousemove', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      // Convert to math coordinates
      const mathX = this.toMathX(x);
      const mathY = this.toMathY(y);
      
      // Handle dragging
      if (this.dragState.isDragging && this.dragState.element) {
        // Update element position
        this.updateElementPosition(this.dragState.element, mathX, mathY);
        this.render();
        
        // Update info panel
        this.updateInfoPanel();
      } else {
        // Check if hovering over any element for cursor change
        const element = this.findElementAt(mathX, mathY);
        
        if (element && element.draggable) {
          this.canvas.style.cursor = 'grab';
        } else {
          this.canvas.style.cursor = 'default';
        }
      }
    });
    
    // Mouse up for ending drags
    this.canvas.addEventListener('mouseup', () => {
      if (this.dragState.isDragging) {
        this.dragState.isDragging = false;
        this.canvas.style.cursor = 'default';
      }
    });
    
    // Mouse leave for safety
    this.canvas.addEventListener('mouseleave', () => {
      if (this.dragState.isDragging) {
        this.dragState.isDragging = false;
        this.canvas.style.cursor = 'default';
      }
    });
    
    // Double click for editing elements
    this.canvas.addEventListener('dblclick', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      // Convert to math coordinates
      const mathX = this.toMathX(x);
      const mathY = this.toMathY(y);
      
      // Find if double clicking on any element
      const element = this.findElementAt(mathX, mathY);
      
      if (element) {
        // Edit element based on type
        this.editElement(element);
      }
    });
  }

  /**
   * Find an element at a specific position
   * @param {number} x - Math X coordinate
   * @param {number} y - Math Y coordinate
   * @returns {Object|null} Found element or null
   */
  findElementAt(x, y) {
    // Check points first (they're smaller)
    for (const point of this.points) {
      const distance = Math.abs(x - point.value);
      const yDistance = Math.abs(y - point.numberLine.position);
      
      if (distance <= this.config.numberLineOptions.pointRadius / 10 && 
          yDistance <= this.config.numberLineOptions.lineHeight * 2) {
        return point;
      }
    }
    
    // Check interval endpoints and handles
    for (const interval of this.intervals) {
      // Left endpoint/handle
      const leftHandleDistance = Math.abs(x - interval.start);
      const leftYDistance = Math.abs(y - interval.numberLine.position);
      
      if (leftHandleDistance <= this.config.numberLineOptions.pointRadius / 10 && 
          leftYDistance <= this.config.numberLineOptions.lineHeight * 2) {
        return {
          type: 'intervalHandle',
          interval: interval,
          side: 'left',
          draggable: true
        };
      }
      
      // Right endpoint/handle
      const rightHandleDistance = Math.abs(x - interval.end);
      const rightYDistance = Math.abs(y - interval.numberLine.position);
      
      if (rightHandleDistance <= this.config.numberLineOptions.pointRadius / 10 && 
          rightYDistance <= this.config.numberLineOptions.lineHeight * 2) {
        return {
          type: 'intervalHandle',
          interval: interval,
          side: 'right',
          draggable: true
        };
      }
      
      // Interval center (for moving the whole interval)
      const center = (interval.start + interval.end) / 2;
      const centerDistance = Math.abs(x - center);
      const centerYDistance = Math.abs(y - interval.numberLine.position);
      
      if (centerDistance <= Math.abs(interval.end - interval.start) / 2 && 
          centerYDistance <= this.config.numberLineOptions.lineHeight * 2 &&
          centerDistance > this.config.numberLineOptions.pointRadius / 8) {
        return {
          type: 'intervalCenter',
          interval: interval,
          draggable: true
        };
      }
    }
    
    // Check inequality handles
    for (const inequality of this.inequalities) {
      // Boundary point (the value where the inequality changes)
      const boundaryDistance = Math.abs(x - inequality.value);
      const boundaryYDistance = Math.abs(y - inequality.numberLine.position);
      
      if (boundaryDistance <= this.config.numberLineOptions.pointRadius / 10 && 
          boundaryYDistance <= this.config.numberLineOptions.lineHeight * 2) {
        return {
          type: 'inequalityBoundary',
          inequality: inequality,
          draggable: true
        };
      }
    }
    
    return null;
  }

  /**
   * Select an element
   * @param {Object} element - Element to select
   */
  selectElement(element) {
    // Deselect previously selected element
    this.deselectElement();
    
    // Select new element
    this.selectedElement = element;
    
    if (element.type === 'point') {
      element.selected = true;
    } else if (element.type === 'intervalHandle' || element.type === 'intervalCenter') {
      element.interval.selected = true;
    } else if (element.type === 'inequalityBoundary') {
      element.inequality.selected = true;
    }
    
    // Update info panel with element details
    this.updateInfoPanel();
  }

  /**
   * Deselect currently selected element
   */
  deselectElement() {
    if (this.selectedElement) {
      if (this.selectedElement.type === 'point') {
        this.selectedElement.selected = false;
      } else if (this.selectedElement.type === 'intervalHandle' || 
                 this.selectedElement.type === 'intervalCenter') {
        this.selectedElement.interval.selected = false;
      } else if (this.selectedElement.type === 'inequalityBoundary') {
        this.selectedElement.inequality.selected = false;
      }
      
      this.selectedElement = null;
    }
  }

  /**
   * Update an element's position based on dragging
   * @param {Object} element - Element being dragged
   * @param {number} x - New X position
   * @param {number} y - New Y position
   */
  updateElementPosition(element, x, y) {
    if (element.type === 'point') {
      // Update point value
      element.value = x;
    } else if (element.type === 'intervalHandle') {
      // Update interval endpoint
      if (element.side === 'left') {
        element.interval.start = Math.min(x, element.interval.end);
      } else {
        element.interval.end = Math.max(x, element.interval.start);
      }
    } else if (element.type === 'intervalCenter') {
      // Move entire interval
      const interval = element.interval;
      const width = interval.end - interval.start;
      const dx = x - (interval.start + interval.end) / 2;
      
      interval.start += dx;
      interval.end += dx;
    } else if (element.type === 'inequalityBoundary') {
      // Update inequality boundary value
      element.inequality.value = x;
    }
  }

  /**
   * Edit an element (on double click)
   * @param {Object} element - Element to edit
   */
  editElement(element) {
    if (element.type === 'point') {
      // Prompt for new value
      const newValue = prompt('Enter new value:', element.value);
      if (newValue !== null) {
        const parsed = parseFloat(newValue);
        if (!isNaN(parsed)) {
          element.value = parsed;
          this.render();
          this.updateInfoPanel();
        }
      }
    } else if (element.type === 'intervalHandle' || element.type === 'intervalCenter') {
      // Prompt for interval properties
      const interval = element.interval;
      
      let newStart = prompt('Enter new start value:', interval.start);
      if (newStart !== null) {
        const parsedStart = parseFloat(newStart);
        if (!isNaN(parsedStart)) {
          interval.start = parsedStart;
        }
      }
      
      let newEnd = prompt('Enter new end value:', interval.end);
      if (newEnd !== null) {
        const parsedEnd = parseFloat(newEnd);
        if (!isNaN(parsedEnd)) {
          interval.end = parsedEnd;
        }
      }
      
      // Make sure start < end
      if (interval.start > interval.end) {
        [interval.start, interval.end] = [interval.end, interval.start];
      }
      
      let newIncludeStart = confirm('Include start value? (OK for Yes, Cancel for No)');
      interval.includeStart = newIncludeStart;
      
      let newIncludeEnd = confirm('Include end value? (OK for Yes, Cancel for No)');
      interval.includeEnd = newIncludeEnd;
      
      this.render();
      this.updateInfoPanel();
    } else if (element.type === 'inequalityBoundary') {
      // Prompt for inequality properties
      const inequality = element.inequality;
      
      let newValue = prompt('Enter new boundary value:', inequality.value);
      if (newValue !== null) {
        const parsedValue = parseFloat(newValue);
        if (!isNaN(parsedValue)) {
          inequality.value = parsedValue;
        }
      }
      
      let newDirection = prompt('Enter inequality direction (< or >):', 
                               inequality.direction === 'less' ? '<' : '>');
      if (newDirection === '<') {
        inequality.direction = 'less';
      } else if (newDirection === '>') {
        inequality.direction = 'greater';
      }
      
      let newIncludeBoundary = confirm('Include boundary value? (OK for Yes, Cancel for No)');
      inequality.inclusive = newIncludeBoundary;
      
      this.render();
      this.updateInfoPanel();
    }
  }

  /**
   * Create a new number line
   * @param {Object} options - Number line options
   * @returns {Object} Created number line
   */
  createNumberLine(options = {}) {
    const defaultOptions = {
      position: 0, // Y-position of the number line
      color: this.config.theme.axisColor,
      lineWidth: 2,
      title: '',
      visible: true
    };
    
    const numberLineOptions = { ...defaultOptions, ...options };
    
    // If using multiple number lines, position them vertically
    if (this.config.numberLineOptions.multipleNumberLines && this.numberLines.length > 0) {
      numberLineOptions.position = this.numberLines[this.numberLines.length - 1].position - 
                                  this.config.numberLineOptions.numberLinesSpacing;
    }
    
    const numberLine = {
      type: 'numberLine',
      ...numberLineOptions
    };
    
    this.numberLines.push(numberLine);
    this.activeNumberLine = numberLine;
    
    this.render();
    return numberLine;
  }

  /**
   * Create a point on the number line
   * @param {number} value - Value (x-position) of the point
   * @param {Object} options - Point options
   * @returns {Object} Created point
   */
  createPoint(value, options = {}) {
    const defaultOptions = {
      color: this.config.theme.highlightColor,
      radius: this.config.numberLineOptions.pointRadius,
      label: '',
      draggable: true,
      selected: false,
      numberLine: this.activeNumberLine,
      visible: true
    };
    
    const pointOptions = { ...defaultOptions, ...options };
    
    const point = {
      type: 'point',
      value: value,
      ...pointOptions
    };
    
    this.points.push(point);
    this.render();
    return point;
  }

  /**
   * Create an interval on the number line
   * @param {number} start - Start value of the interval
   * @param {number} end - End value of the interval
   * @param {Object} options - Interval options
   * @returns {Object} Created interval
   */
  createInterval(start, end, options = {}) {
    // Ensure start < end
    if (start > end) {
      [start, end] = [end, start];
    }
    
    const defaultOptions = {
      color: this.config.theme.secondaryColor,
      includeStart: true, // Closed at start
      includeEnd: true,   // Closed at end
      label: '',
      selected: false,
      numberLine: this.activeNumberLine,
      visible: true
    };
    
    const intervalOptions = { ...defaultOptions, ...options };
    
    const interval = {
      type: 'interval',
      start: start,
      end: end,
      ...intervalOptions
    };
    
    this.intervals.push(interval);
    this.render();
    return interval;
  }

  /**
   * Create an inequality on the number line
   * @param {number} value - Boundary value of the inequality
   * @param {string} direction - Direction ('less' or 'greater')
   * @param {Object} options - Inequality options
   * @returns {Object} Created inequality
   */
  createInequality(value, direction, options = {}) {
    const defaultOptions = {
      color: this.config.theme.tertiaryColor,
      inclusive: false, // Whether to include the boundary point
      label: '',
      selected: false,
      numberLine: this.activeNumberLine,
      visible: true
    };
    
    const inequalityOptions = { ...defaultOptions, ...options };
    
    const inequality = {
      type: 'inequality',
      value: value,
      direction: direction, // 'less' or 'greater'
      ...inequalityOptions
    };
    
    this.inequalities.push(inequality);
    this.render();
    return inequality;
  }

  /**
   * Create a compound inequality (intersection of two inequalities)
   * @param {number} value1 - First boundary value
   * @param {string} direction1 - First direction ('less' or 'greater')
   * @param {number} value2 - Second boundary value
   * @param {string} direction2 - Second direction ('less' or 'greater')
   * @param {Object} options - Inequality options
   * @returns {Array} Array of created inequalities
   */
  createCompoundInequality(value1, direction1, value2, direction2, options = {}) {
    // Create both inequalities
    const inequality1 = this.createInequality(value1, direction1, options);
    const inequality2 = this.createInequality(value2, direction2, options);
    
    // Add a reference to each other for linked visualizations
    inequality1.linked = inequality2;
    inequality2.linked = inequality1;
    
    return [inequality1, inequality2];
  }

  /**
   * Create a representation of an interval in set notation
   * @param {number} start - Start value
   * @param {number} end - End value
   * @param {boolean} includeStart - Whether to include start value
   * @param {boolean} includeEnd - Whether to include end value
   * @returns {string} Interval in set notation
   */
  getIntervalNotation(start, end, includeStart, includeEnd) {
    const leftBracket = includeStart ? '[' : '(';
    const rightBracket = includeEnd ? ']' : ')';
    return `${leftBracket}${start}, ${end}${rightBracket}`;
  }

  /**
   * Create a representation of an inequality
   * @param {number} value - Boundary value
   * @param {string} direction - Direction ('less' or 'greater')
   * @param {boolean} inclusive - Whether to include the boundary
   * @returns {string} Inequality representation
   */
  getInequalityNotation(value, direction, inclusive) {
    const operator = direction === 'less' 
      ? (inclusive ? '≤' : '<') 
      : (inclusive ? '≥' : '>');
    
    return `x ${operator} ${value}`;
  }

  /**
   * Set the active tool
   * @param {string} tool - Tool name
   */
  setTool(tool) {
    this.currentTool = tool;
    
    // Update cursor based on tool
    switch (tool) {
      case 'point':
        this.canvas.style.cursor = 'crosshair';
        break;
      default:
        this.canvas.style.cursor = 'default';
    }
  }

  /**
   * Update information in the info panel
   */
  updateInfoPanel() {
    if (!this.infoPanel) return;
    
    // Clear existing info
    this.infoPanel.innerHTML = '';
    
    // Add title
    const title = document.createElement('h3');
    title.style.margin = '0 0 10px 0';
    title.style.fontSize = '16px';
    title.textContent = 'Number Line';
    this.infoPanel.appendChild(title);
    
    // Show selected element details
    if (this.selectedElement) {
      const element = this.selectedElement;
      
      if (element.type === 'point') {
        this.addInfo('point-value', 'Point Value', element.value.toFixed(2));
      } else if (element.type === 'intervalHandle' || element.type === 'intervalCenter') {
        const interval = element.interval;
        this.addInfo('interval-start', 'Start', interval.start.toFixed(2));
        this.addInfo('interval-end', 'End', interval.end.toFixed(2));
        this.addInfo('interval-width', 'Width', (interval.end - interval.start).toFixed(2));
        this.addInfo('interval-notation', 'Set Notation', 
                     this.getIntervalNotation(interval.start, interval.end, 
                                             interval.includeStart, interval.includeEnd));
      } else if (element.type === 'inequalityBoundary') {
        const inequality = element.inequality;
        this.addInfo('inequality-value', 'Boundary', inequality.value.toFixed(2));
        this.addInfo('inequality-direction', 'Direction', 
                    inequality.direction === 'less' ? 'Less Than' : 'Greater Than');
        this.addInfo('inequality-inclusive', 'Inclusive', 
                    inequality.inclusive ? 'Yes' : 'No');
        this.addInfo('inequality-notation', 'Notation', 
                    this.getInequalityNotation(inequality.value, 
                                              inequality.direction, 
                                              inequality.inclusive));
        
        // If this is part of a compound inequality, show combined notation
        if (inequality.linked) {
          const combined = this.getCombinedInequalityNotation(inequality, inequality.linked);
          this.addInfo('combined-notation', 'Combined', combined);
        }
      }
      
      // Add instructions
      const instructions = document.createElement('div');
      instructions.style.marginTop = '10px';
      instructions.style.fontSize = '12px';
      instructions.style.fontStyle = 'italic';
      instructions.textContent = 'Tip: Double-click to edit properties. Drag to move.';
      this.infoPanel.appendChild(instructions);
    } else {
      // Show global information
      const countInfo = document.createElement('div');
      countInfo.innerHTML = `
        <div><strong>Points:</strong> ${this.points.length}</div>
        <div><strong>Intervals:</strong> ${this.intervals.length}</div>
        <div><strong>Inequalities:</strong> ${this.inequalities.length}</div>
      `;
      this.infoPanel.appendChild(countInfo);
    }
  }

  /**
   * Get the combined notation for two inequalities
   * @param {Object} ineq1 - First inequality
   * @param {Object} ineq2 - Second inequality
   * @returns {string} Combined notation
   */
  getCombinedInequalityNotation(ineq1, ineq2) {
    // Check if this forms a "between" inequality
    if ((ineq1.direction === 'greater' && ineq2.direction === 'less') ||
        (ineq1.direction === 'less' && ineq2.direction === 'greater')) {
      
      // Reorder so we have the "less than" inequality second
      let [less, greater] = ineq1.direction === 'less' 
          ? [ineq1, ineq2] 
          : [ineq2, ineq1];
      
      // Check if this forms a valid bounded interval
      if (greater.value < less.value) {
        const op1 = greater.inclusive ? '≤' : '<';
        const op2 = less.inclusive ? '≤' : '<';
        return `${greater.value} ${op1} x ${op2} ${less.value}`;
      }
    }
    
    // Otherwise just show both inequalities
    const notation1 = this.getInequalityNotation(ineq1.value, ineq1.direction, ineq1.inclusive);
    const notation2 = this.getInequalityNotation(ineq2.value, ineq2.direction, ineq2.inclusive);
    return `${notation1} and ${notation2}`;
  }

  /**
   * Add standard tools to the control panel
   */
  addStandardTools() {
    if (!this.controlsArea) return;
    
    // Add title
    const title = document.createElement('h3');
    title.style.margin = '0 0 10px 0';
    title.style.fontSize = '16px';
    title.textContent = 'Tools';
    this.controlsArea.appendChild(title);
    
    // Add tool buttons
    this.addControl('button', {
      id: 'tool-point',
      text: 'Add Point',
      fullWidth: true,
      onClick: () => this.setTool('point')
    });
    
    // Add interval button - prompts for start and end values
    this.addControl('button', {
      id: 'add-interval',
      text: 'Add Interval',
      fullWidth: true,
      onClick: () => {
        let start = prompt('Enter start value:', '0');
        if (start === null) return;
        
        let end = prompt('Enter end value:', '5');
        if (end === null) return;
        
        const startValue = parseFloat(start);
        const endValue = parseFloat(end);
        
        if (!isNaN(startValue) && !isNaN(endValue)) {
          const includeStart = confirm('Include start value? (OK for Yes, Cancel for No)');
          const includeEnd = confirm('Include end value? (OK for Yes, Cancel for No)');
          
          this.createInterval(startValue, endValue, {
            includeStart: includeStart,
            includeEnd: includeEnd
          });
        }
      }
    });
    
    // Add inequality button - prompts for value and type
    this.addControl('button', {
      id: 'add-inequality',
      text: 'Add Inequality',
      fullWidth: true,
      onClick: () => {
        let value = prompt('Enter boundary value:', '0');
        if (value === null) return;
        
        const boundaryValue = parseFloat(value);
        
        if (!isNaN(boundaryValue)) {
          let type = prompt('Enter inequality type (< or >):', '<');
          const direction = type === '>' ? 'greater' : 'less';
          
          const inclusive = confirm('Include boundary value? (OK for Yes, Cancel for No)');
          
          this.createInequality(boundaryValue, direction, {
            inclusive: inclusive
          });
        }
      }
    });
    
    // Add compound inequality button
    this.addControl('button', {
      id: 'add-compound-inequality',
      text: 'Add Compound Inequality',
      fullWidth: true,
      onClick: () => {
        let value1 = prompt('Enter first boundary value:', '-2');
        if (value1 === null) return;
        
        let type1 = prompt('Enter first inequality type (< or >):', '>');
        if (type1 === null) return;
        
        let value2 = prompt('Enter second boundary value:', '3');
        if (value2 === null) return;
        
        let type2 = prompt('Enter second inequality type (< or >):', '<');
        if (type2 === null) return;
        
        const boundaryValue1 = parseFloat(value1);
        const boundaryValue2 = parseFloat(value2);
        
        if (!isNaN(boundaryValue1) && !isNaN(boundaryValue2)) {
          const direction1 = type1 === '>' ? 'greater' : 'less';
          const direction2 = type2 === '>' ? 'greater' : 'less';
          
          const inclusive1 = confirm('Include first boundary value? (OK for Yes, Cancel for No)');
          const inclusive2 = confirm('Include second boundary value? (OK for Yes, Cancel for No)');
          
          this.createCompoundInequality(
            boundaryValue1, direction1,
            boundaryValue2, direction2,
            {
              inclusive: inclusive1 // Will be overridden for the second one
            }
          );
          
          // Update the second inequality's inclusivity separately
          this.inequalities[this.inequalities.length - 1].inclusive = inclusive2;
          this.render();
        }
      }
    });
    
    // Add clear button
    this.addControl('button', {
      id: 'clear-all',
      text: 'Clear All',
      fullWidth: true,
      onClick: () => {
        if (confirm('Are you sure you want to clear all elements?')) {
          this.points = [];
          this.intervals = [];
          this.inequalities = [];
          this.render();
          this.updateInfoPanel();
        }
      }
    });
    
    // Add separator
    const separator = document.createElement('hr');
    separator.style.margin = '15px 0';
    separator.style.border = 'none';
    separator.style.borderTop = `1px solid ${this.config.theme.borderColor}`;
    this.controlsArea.appendChild(separator);
    
    // Add visualization options
    const optionsTitle = document.createElement('h3');
    optionsTitle.style.margin = '0 0 10px 0';
    optionsTitle.style.fontSize = '16px';
    optionsTitle.textContent = 'Options';
    this.controlsArea.appendChild(optionsTitle);
    
    // Toggle for showing ticks
    this.addControl('checkbox', {
      id: 'show-ticks',
      text: 'Show Tick Marks',
      checked: true,
      onChange: (checked) => {
        this.config.numberLineOptions.showLabels = checked;
        this.render();
      }
    });
    
    // Toggle for showing origin
    this.addControl('checkbox', {
      id: 'show-origin',
      text: 'Highlight Origin',
      checked: this.config.numberLineOptions.showOrigin,
      onChange: (checked) => {
        this.config.numberLineOptions.showOrigin = checked;
        this.render();
      }
    });
    
    // Zoom control
    this.addControl('slider', {
      id: 'zoom',
      label: 'Zoom',
      min: 5,
      max: 40,
      step: 5,
      value: 20,
      onChange: (value) => {
        const range = parseInt(value);
        this.setRange({ 
          xMin: -range / 2, 
          xMax: range / 2 
        });
        this.render();
      }
    });
  }

  /**
   * Add a new number line if multiple lines are enabled
   */
  addNumberLine() {
    if (!this.config.numberLineOptions.multipleNumberLines) {
      this.config.numberLineOptions.multipleNumberLines = true;
    }
    
    // Create a new number line with a different color
    const colors = [
      this.config.theme.highlightColor,
      this.config.theme.secondaryColor,
      this.config.theme.tertiaryColor,
      '#f39c12', // Orange
      '#1abc9c', // Turquoise
      '#34495e'  // Dark Blue
    ];
    
    const color = colors[this.numberLines.length % colors.length];
    this.createNumberLine({ color: color });
  }

  /**
   * Render the visualization
   */
  render() {
    // Call parent render to clear canvas and draw grid/axes
    super.clear();
    
    // We will manually handle coordinate system for number lines
    // instead of using the grid and axes
    
    // Draw all number lines
    for (const numberLine of this.numberLines) {
      if (numberLine.visible) {
        this.drawNumberLine(numberLine);
      }
    }
    
    // Draw all intervals
    for (const interval of this.intervals) {
      if (interval.visible) {
        this.drawInterval(interval);
      }
    }
    
    // Draw all inequalities
    for (const inequality of this.inequalities) {
      if (inequality.visible) {
        this.drawInequality(inequality);
      }
    }
    
    // Draw all points
    for (const point of this.points) {
      if (point.visible) {
        this.drawPoint(point);
      }
    }
  }

  /**
   * Draw a number line
   * @param {Object} numberLine - Number line object
   */
  drawNumberLine(numberLine) {
    const { xMin, xMax } = this.config.range;
    const y = numberLine.position;
    
    // Draw main horizontal line
    this.ctx.strokeStyle = numberLine.color;
    this.ctx.lineWidth = numberLine.lineWidth;
    this.ctx.beginPath();
    this.ctx.moveTo(this.toCanvasX(xMin), this.toCanvasY(y));
    this.ctx.lineTo(this.toCanvasX(xMax), this.toCanvasY(y));
    this.ctx.stroke();
    
    // Draw tick marks and labels if enabled
    if (this.config.numberLineOptions.showLabels) {
      const tickInterval = this.config.numberLineOptions.labelInterval;
      const minorTickInterval = this.config.numberLineOptions.minorTickInterval;
      const tickLength = this.config.numberLineOptions.tickLength;
      
      // Calculate appropriate range for tick marks
      const tickMin = Math.ceil(xMin / tickInterval) * tickInterval;
      const tickMax = Math.floor(xMax / tickInterval) * tickInterval;
      
      // Calculate minor tick marks range
      const minorTickMin = Math.ceil(xMin / minorTickInterval) * minorTickInterval;
      const minorTickMax = Math.floor(xMax / minorTickInterval) * minorTickInterval;
      
      // Draw minor tick marks
      this.ctx.strokeStyle = numberLine.color;
      this.ctx.lineWidth = 1;
      
      for (let x = minorTickMin; x <= minorTickMax; x += minorTickInterval) {
        // Skip major tick positions
        if (Math.abs(x % tickInterval) < 0.001) continue;
        
        this.ctx.beginPath();
        this.ctx.moveTo(this.toCanvasX(x), this.toCanvasY(y - tickLength / 2));
        this.ctx.lineTo(this.toCanvasX(x), this.toCanvasY(y + tickLength / 2));
        this.ctx.stroke();
      }
      
      // Draw major tick marks and labels
      this.ctx.strokeStyle = numberLine.color;
      this.ctx.lineWidth = 2;
      this.ctx.font = `14px ${this.config.theme.fontFamily}`;
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'top';
      this.ctx.fillStyle = this.config.theme.textColor;
      
      for (let x = tickMin; x <= tickMax; x += tickInterval) {
        // Draw major tick
        this.ctx.beginPath();
        this.ctx.moveTo(this.toCanvasX(x), this.toCanvasY(y - tickLength));
        this.ctx.lineTo(this.toCanvasX(x), this.toCanvasY(y + tickLength));
        this.ctx.stroke();
        
        // Draw label
        const label = x === 0 && this.config.numberLineOptions.showOrigin ? '0' : x.toString();
        this.ctx.fillText(label, this.toCanvasX(x), this.toCanvasY(y + tickLength * 1.5));
      }
      
      // Highlight the origin if enabled
      if (this.config.numberLineOptions.showOrigin && 
          xMin <= 0 && xMax >= 0) {
        this.ctx.fillStyle = this.config.theme.highlightColor;
        this.ctx.beginPath();
        this.ctx.arc(
          this.toCanvasX(0),
          this.toCanvasY(y),
          3,
          0,
          2 * Math.PI
        );
        this.ctx.fill();
      }
    }
    
    // Draw title if present
    if (numberLine.title) {
      this.ctx.font = `14px ${this.config.theme.fontFamily}`;
      this.ctx.textAlign = 'left';
      this.ctx.textBaseline = 'bottom';
      this.ctx.fillStyle = numberLine.color;
      this.ctx.fillText(
        numberLine.title,
        this.toCanvasX(xMin) + 10,
        this.toCanvasY(y) - 10
      );
    }
  }

  /**
   * Draw a point on the number line
   * @param {Object} point - Point object
   */
  drawPoint(point) {
    const x = point.value;
    const y = point.numberLine.position;
    
    // Determine point style
    let color = point.color;
    let radius = point.radius;
    
    if (point.selected) {
      color = this.config.theme.highlightColor;
      radius += 2;
    }
    
    // Draw the point
    this.ctx.fillStyle = color;
    this.ctx.beginPath();
    this.ctx.arc(
      this.toCanvasX(x),
      this.toCanvasY(y),
      radius,
      0,
      2 * Math.PI
    );
    this.ctx.fill();
    
    // Draw outline
    this.ctx.strokeStyle = this.config.theme.backgroundColor;
    this.ctx.lineWidth = 1;
    this.ctx.stroke();
    
    // Draw label if present
    if (point.label) {
      this.ctx.font = `14px ${this.config.theme.fontFamily}`;
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'bottom';
      this.ctx.fillStyle = this.config.theme.textColor;
      this.ctx.fillText(
        point.label,
        this.toCanvasX(x),
        this.toCanvasY(y) - radius - 5
      );
    }
  }

  /**
   * Draw an interval on the number line
   * @param {Object} interval - Interval object
   */
  drawInterval(interval) {
    const start = interval.start;
    const end = interval.end;
    const y = interval.numberLine.position;
    
    // Determine interval style
    let color = interval.color;
    let lineHeight = this.config.numberLineOptions.lineHeight;
    
    if (interval.selected) {
      color = this.config.theme.highlightColor;
      lineHeight *= 1.5;
    }
    
    // Draw the interval as a thick line
    this.ctx.strokeStyle = color;
    this.ctx.lineWidth = lineHeight * 10; // Thicker than the line height
    this.ctx.beginPath();
    this.ctx.moveTo(this.toCanvasX(start), this.toCanvasY(y));
    this.ctx.lineTo(this.toCanvasX(end), this.toCanvasY(y));
    this.ctx.stroke();
    
    // Draw endpoints
    const radius = this.config.numberLineOptions.pointRadius;
    
    // Start point
    this.ctx.fillStyle = color;
    this.ctx.beginPath();
    this.ctx.arc(
      this.toCanvasX(start),
      this.toCanvasY(y),
      radius,
      0,
      2 * Math.PI
    );
    
    if (interval.includeStart) {
      this.ctx.fill();
    } else {
      this.ctx.fillStyle = this.config.theme.backgroundColor;
      this.ctx.fill();
      this.ctx.strokeStyle = color;
      this.ctx.lineWidth = 2;
      this.ctx.stroke();
    }
    
    // End point
    this.ctx.fillStyle = color;
    this.ctx.beginPath();
    this.ctx.arc(
      this.toCanvasX(end),
      this.toCanvasY(y),
      radius,
      0,
      2 * Math.PI
    );
    
    if (interval.includeEnd) {
      this.ctx.fill();
    } else {
      this.ctx.fillStyle = this.config.theme.backgroundColor;
      this.ctx.fill();
      this.ctx.strokeStyle = color;
      this.ctx.lineWidth = 2;
      this.ctx.stroke();
    }
    
    // Draw label if present
    if (interval.label) {
      this.ctx.font = `14px ${this.config.theme.fontFamily}`;
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'bottom';
      this.ctx.fillStyle = color;
      this.ctx.fillText(
        interval.label,
        this.toCanvasX((start + end) / 2),
        this.toCanvasY(y) - lineHeight * 10 - 5
      );
    } else {
      // Draw interval notation as the label
      this.ctx.font = `14px ${this.config.theme.fontFamily}`;
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'bottom';
      this.ctx.fillStyle = color;
      
      const notation = this.getIntervalNotation(
        start, end, interval.includeStart, interval.includeEnd
      );
      
      this.ctx.fillText(
        notation,
        this.toCanvasX((start + end) / 2),
        this.toCanvasY(y) - lineHeight * 10 - 5
      );
    }
  }

  /**
   * Draw an inequality on the number line
   * @param {Object} inequality - Inequality object
   */
  drawInequality(inequality) {
    const value = inequality.value;
    const direction = inequality.direction;
    const y = inequality.numberLine.position;
    
    // Determine inequality style
    let color = inequality.color;
    let lineHeight = this.config.numberLineOptions.lineHeight;
    
    if (inequality.selected) {
      color = this.config.theme.highlightColor;
      lineHeight *= 1.5;
    }
    
    const { xMin, xMax } = this.config.range;
    
    // Draw the ray based on direction
    this.ctx.strokeStyle = color;
    this.ctx.lineWidth = lineHeight * 10; // Thicker than the line height
    this.ctx.beginPath();
    
    if (direction === 'less') {
      // Less than: draw from min to value
      this.ctx.moveTo(this.toCanvasX(xMin), this.toCanvasY(y));
      this.ctx.lineTo(this.toCanvasX(value), this.toCanvasY(y));
    } else {
      // Greater than: draw from value to max
      this.ctx.moveTo(this.toCanvasX(value), this.toCanvasY(y));
      this.ctx.lineTo(this.toCanvasX(xMax), this.toCanvasY(y));
    }
    this.ctx.stroke();
    
    // Draw boundary point
    const radius = this.config.numberLineOptions.pointRadius;
    
    this.ctx.beginPath();
    this.ctx.arc(
      this.toCanvasX(value),
      this.toCanvasY(y),
      radius,
      0,
      2 * Math.PI
    );
    
    if (inequality.inclusive) {
      this.ctx.fillStyle = color;
      this.ctx.fill();
    } else {
      this.ctx.fillStyle = this.config.theme.backgroundColor;
      this.ctx.fill();
      this.ctx.strokeStyle = color;
      this.ctx.lineWidth = 2;
      this.ctx.stroke();
    }
    
    // Draw directional arrow if enabled
    if (this.config.numberLineOptions.directionalHandles) {
      const arrowSize = radius * 1.5;
      const arrowX = direction === 'less' ? value - arrowSize * 2 : value + arrowSize * 2;
      
      this.ctx.fillStyle = color;
      this.ctx.beginPath();
      
      if (direction === 'less') {
        // Arrow pointing left
        this.ctx.moveTo(this.toCanvasX(arrowX), this.toCanvasY(y));
        this.ctx.lineTo(this.toCanvasX(arrowX + arrowSize), this.toCanvasY(y - arrowSize));
        this.ctx.lineTo(this.toCanvasX(arrowX + arrowSize), this.toCanvasY(y + arrowSize));
      } else {
        // Arrow pointing right
        this.ctx.moveTo(this.toCanvasX(arrowX), this.toCanvasY(y));
        this.ctx.lineTo(this.toCanvasX(arrowX - arrowSize), this.toCanvasY(y - arrowSize));
        this.ctx.lineTo(this.toCanvasX(arrowX - arrowSize), this.toCanvasY(y + arrowSize));
      }
      
      this.ctx.closePath();
      this.ctx.fill();
    }
    
    // Draw label or notation
    this.ctx.font = `14px ${this.config.theme.fontFamily}`;
    this.ctx.textAlign = 'center';
    this.ctx.textBaseline = 'bottom';
    this.ctx.fillStyle = color;
    
    const labelX = direction === 'less' 
      ? (xMin + value) / 2
      : (value + xMax) / 2;
    
    if (inequality.label) {
      this.ctx.fillText(
        inequality.label,
        this.toCanvasX(labelX),
        this.toCanvasY(y) - lineHeight * 10 - 5
      );
    } else {
      // Draw inequality notation
      const notation = this.getInequalityNotation(
        value, direction, inequality.inclusive
      );
      
      this.ctx.fillText(
        notation,
        this.toCanvasX(labelX),
        this.toCanvasY(y) - lineHeight * 10 - 5
      );
    }
  }
}

export default NumberLineVisualizer;