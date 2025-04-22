/**
 * MathExplorer - Function Plotter Module
 * 
 * An extension of the base MathExplorer framework that specializes in plotting
 * mathematical functions with interactive parameters.
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
        lineWidth: 3
      },
      ...config
    };
    
    // Call parent constructor
    super(functionConfig);
    
    // Initialize function collections
    this.functions = [];
    this.parameters = {};
    this.specialPoints = []; // Initialize specialPoints array here
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
    
    this.functions.forEach(func => {
      if (!func.visible) return;
      
      const { xMin, xMax } = this.config.range;
      const resolution = this.config.plotOptions.resolution;
      const step = (xMax - xMin) / resolution;
      
      this.ctx.strokeStyle = func.color;
      this.ctx.lineWidth = func.lineWidth;
      this.ctx.beginPath();
      
      let lastX = null;
      let lastY = null;
      let isDrawing = false;
      
      for (let i = 0; i <= resolution; i++) {
        const x = xMin + i * step;
        try {
          const y = func.evaluator(x);
          
          // Skip if y is not a valid number or outside of range
          if (!isFinite(y) || y < this.config.range.yMin || y > this.config.range.yMax) {
            isDrawing = false;
            continue;
          }
          
          const canvasX = this.toCanvasX(x);
          const canvasY = this.toCanvasY(y);
          
          if (!isDrawing) {
            this.ctx.moveTo(canvasX, canvasY);
            isDrawing = true;
          } else {
            // Check for discontinuities
            const dx = x - lastX;
            const dy = y - lastY;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance > step * 10) {
              // Likely a discontinuity
              this.ctx.stroke();
              this.ctx.beginPath();
              this.ctx.moveTo(canvasX, canvasY);
            } else {
              this.ctx.lineTo(canvasX, canvasY);
            }
          }
          
          lastX = x;
          lastY = y;
        } catch (e) {
          isDrawing = false;
          console.error("Error evaluating function", e);
        }
      }
      
      this.ctx.stroke();
    });
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
    
    // Update info panel
    this.updateFunctionInfo();
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