/**
 * MathExplorer - Calculus Tools Module
 * 
 * An extension of the base MathExplorer framework specialized for
 * calculus concepts including derivatives, integrals, limits, and more.
 */

import MathExplorer from './base-visualization-framework.js';

class CalculusTools extends MathExplorer {
  /**
   * Create a new calculus tools environment
   * @param {Object} config - Configuration settings
   */
  constructor(config) {
    // Set default config values specific to calculus visualization
    const calculusConfig = {
      // Default range appropriate for most calculus visualizations
      range: { xMin: -5, xMax: 5, yMin: -5, yMax: 5 },
      // Enable info panel for detailed information
      infoPanel: true,
      // Calculus-specific settings
      calculusOptions: {
        // Functions
        defaultFunction: 'Math.sin(x)',
        functionColor: '#3498db',
        functionLineWidth: 2,
        
        // Derivative visualization
        showDerivative: false,
        derivativeColor: '#e74c3c',
        derivativeLineWidth: 2,
        
        // Tangent line visualization
        showTangent: false,
        tangentColor: '#2ecc71',
        tangentLineWidth: 2,
        tangentLength: 2,
        
        // Integral visualization
        showIntegral: false,
        integralColor: '#9b59b6',
        integralOpacity: 0.3,
        lowerLimit: -2,
        upperLimit: 2,
        
        // Riemann sum visualization
        showRiemannSum: false,
        riemannSumColor: '#f39c12',
        riemannSumOpacity: 0.5,
        numRectangles: 10,
        riemannSumType: 'left', // 'left', 'right', 'midpoint', 'trapezoidal'
        
        // Secant line visualization
        showSecant: false,
        secantColor: '#e67e22',
        secantLineWidth: 2,
        secantPointDistance: 1,
        
        // Limit visualization
        showLimit: false,
        limitColor: '#1abc9c',
        limitPointSize: 5,
        limitApproachDelta: 0.1,
        
        // Taylor series visualization
        showTaylorSeries: false,
        taylorSeriesColor: '#34495e',
        taylorSeriesLineWidth: 2,
        taylorSeriesCenter: 0,
        taylorSeriesTerms: 5,
        
        // Appearance settings
        smoothness: 500, // Number of points to plot function
        evaluationPrecision: 6, // Decimal places for numerical results
        highlightPoints: true,
        animationDuration: 1000, // ms
        showGrid: true
      },
      ...config
    };
    
    // Call parent constructor
    super(calculusConfig);
    
    // Initialize collections for functions and calculus objects
    this.functions = [];
    this.activeFunction = null;
    
    // Special reference points
    this.tangentPoint = null;
    this.limitPoint = null;
    
    // Secant line points
    this.secantPoints = {
      x1: 0,
      x2: 1
    };
    
    // Set up initial function
    this.addFunction({
      expression: this.config.calculusOptions.defaultFunction,
      color: this.config.calculusOptions.functionColor,
      lineWidth: this.config.calculusOptions.functionLineWidth
    });
    
    // Set up event handlers
    this.setupCalculusEventHandlers();
  }

  /**
   * Set up event handlers for calculus interactions
   */
  setupCalculusEventHandlers() {
    // Mouse move to update tangent point
    this.canvas.addEventListener('mousemove', (e) => {
      if (!this.config.calculusOptions.showTangent && 
          !this.config.calculusOptions.showSecant) return;
      
      const rect = this.canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      // Convert to math coordinates
      const mathX = this.toMathX(x);
      
      if (this.config.calculusOptions.showTangent) {
        // Update tangent point
        this.tangentPoint = mathX;
        this.render();
      }
      
      if (this.config.calculusOptions.showSecant && this.dragState && this.dragState.isDragging) {
        if (this.dragState.point === 'first') {
          this.secantPoints.x1 = mathX;
        } else if (this.dragState.point === 'second') {
          this.secantPoints.x2 = mathX;
        }
        this.render();
      }
    });
    
    // Mouse down to interact with secant points
    this.canvas.addEventListener('mousedown', (e) => {
      if (!this.config.calculusOptions.showSecant) return;
      
      const rect = this.canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      // Convert to math coordinates
      const mathX = this.toMathX(x);
      const mathY = this.toMathY(y);
      
      // Check if clicking on one of the secant points
      const func = this.activeFunction;
      if (!func) return;
      
      try {
        const y1 = func.evaluator(this.secantPoints.x1);
        const y2 = func.evaluator(this.secantPoints.x2);
        
        const distToPoint1 = Math.sqrt(
          Math.pow(mathX - this.secantPoints.x1, 2) + 
          Math.pow(mathY - y1, 2)
        );
        
        const distToPoint2 = Math.sqrt(
          Math.pow(mathX - this.secantPoints.x2, 2) + 
          Math.pow(mathY - y2, 2)
        );
        
        const threshold = 0.5;
        
        if (distToPoint1 < threshold) {
          this.dragState = {
            isDragging: true,
            point: 'first'
          };
          this.canvas.style.cursor = 'grabbing';
        } else if (distToPoint2 < threshold) {
          this.dragState = {
            isDragging: true,
            point: 'second'
          };
          this.canvas.style.cursor = 'grabbing';
        }
      } catch (error) {
        console.error('Error evaluating function for secant points:', error);
      }
    });
    
    // Mouse up to end dragging
    this.canvas.addEventListener('mouseup', () => {
      if (this.dragState && this.dragState.isDragging) {
        this.dragState.isDragging = false;
        this.dragState = null;
        this.canvas.style.cursor = 'default';
      }
    });
    
    // Mouse leave to end dragging
    this.canvas.addEventListener('mouseleave', () => {
      if (this.dragState && this.dragState.isDragging) {
        this.dragState.isDragging = false;
        this.dragState = null;
        this.canvas.style.cursor = 'default';
      }
    });
    
    // Click to set limit point
    this.canvas.addEventListener('click', (e) => {
      if (!this.config.calculusOptions.showLimit) return;
      
      const rect = this.canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      
      // Convert to math coordinates
      const mathX = this.toMathX(x);
      
      // Set the limit point
      this.limitPoint = mathX;
      this.render();
    });
  }

  /**
   * Add a function to visualize
   * @param {Object} options - Function options
   * @returns {Object} Added function
   */
  addFunction(options = {}) {
    const defaultOptions = {
      expression: this.config.calculusOptions.defaultFunction,
      color: this.config.calculusOptions.functionColor,
      lineWidth: this.config.calculusOptions.functionLineWidth,
      visible: true
    };
    
    const funcOptions = { ...defaultOptions, ...options };
    
    // Create evaluator function
    let evaluator;
    try {
      evaluator = this.createFunctionEvaluator(funcOptions.expression);
    } catch (error) {
      console.error('Error creating function evaluator:', error);
      return null;
    }
    
    const func = {
      ...funcOptions,
      evaluator
    };
    
    this.functions.push(func);
    this.activeFunction = func;
    
    // Initialize default tangent point if needed
    if (this.config.calculusOptions.showTangent && this.tangentPoint === null) {
      this.tangentPoint = 0;
    }
    
    this.render();
    return func;
  }

  /**
   * Create a function evaluator from an expression string
   * @param {string} expression - Mathematical expression
   * @returns {Function} Evaluator function
   */
  createFunctionEvaluator(expression) {
    // Basic safety measures to prevent harmful code execution
    if (
      expression.includes('document') || 
      expression.includes('window') || 
      expression.includes('eval') ||
      expression.includes('Function')
    ) {
      throw new Error('Potentially unsafe expression');
    }
    
    try {
      // Create a safe evaluator function
      return new Function('x', `
        try {
          return ${expression};
        } catch (e) {
          return NaN;
        }
      `);
    } catch (error) {
      throw new Error(`Invalid function expression: ${error.message}`);
    }
  }

  /**
   * Calculate the derivative of a function using finite difference method
   * @param {Function} func - Original function
   * @param {number} x - Point at which to calculate derivative
   * @param {number} h - Step size (defaults to a small value)
   * @returns {number} Derivative value
   */
  calculateDerivative(func, x, h = 0.0001) {
    try {
      // Use central difference method for better accuracy
      const forward = func(x + h);
      const backward = func(x - h);
      
      return (forward - backward) / (2 * h);
    } catch (error) {
      console.error('Error calculating derivative:', error);
      return NaN;
    }
  }

  /**
   * Get derivative function using numerical differentiation
   * @param {Function} func - Original function
   * @returns {Function} Derivative function
   */
  getDerivativeFunction(func) {
    return (x) => this.calculateDerivative(func, x);
  }

  /**
   * Calculate the definite integral of a function using numerical integration
   * @param {Function} func - Function to integrate
   * @param {number} a - Lower limit
   * @param {number} b - Upper limit
   * @param {number} n - Number of intervals (higher = more accurate)
   * @returns {number} Integral value
   */
  calculateIntegral(func, a, b, n = 1000) {
    if (a > b) [a, b] = [b, a];
    
    try {
      // Use Simpson's rule for numerical integration
      const h = (b - a) / n;
      
      // Ensure n is even for Simpson's rule
      if (n % 2 === 1) n += 1;
      
      let sum = func(a) + func(b);
      
      for (let i = 1; i < n; i++) {
        const x = a + i * h;
        sum += func(x) * (i % 2 === 0 ? 2 : 4);
      }
      
      return (h / 3) * sum;
    } catch (error) {
      console.error('Error calculating integral:', error);
      return NaN;
    }
  }
  
  /**
   * Calculate a specific term in the Taylor series expansion
   * @param {Function} func - Original function
   * @param {Function} derivatives - Array of derivative functions
   * @param {number} a - Center point
   * @param {number} n - Term index
   * @returns {Function} Function for the nth term
   */
  getTaylorTerm(func, derivatives, a, n) {
    if (n === 0) {
      return (x) => func(a);
    }
    
    return (x) => {
      try {
        const derivative = derivatives[n];
        return derivative(a) * Math.pow(x - a, n) / this.factorial(n);
      } catch (error) {
        return 0;
      }
    };
  }
  
  /**
   * Calculate factorial
   * @param {number} n - Input 
   * @returns {number} n!
   */
  factorial(n) {
    if (n === 0 || n === 1) return 1;
    let result = 1;
    for (let i = 2; i <= n; i++) {
      result *= i;
    }
    return result;
  }
  
  /**
   * Get Taylor series approximation function
   * @param {Function} func - Original function
   * @param {number} a - Center point
   * @param {number} terms - Number of terms
   * @returns {Function} Taylor series approximation
   */
  getTaylorSeriesFunction(func, a, terms) {
    // Generate derivative functions (using numerical differentiation)
    const derivatives = [func];
    
    for (let i = 1; i <= terms; i++) {
      derivatives.push(this.getDerivativeFunction(derivatives[i-1]));
    }
    
    // Create Taylor series function
    return (x) => {
      let sum = 0;
      for (let i = 0; i <= terms; i++) {
        try {
          const term = this.getTaylorTerm(func, derivatives, a, i)(x);
          if (isFinite(term)) {
            sum += term;
          }
        } catch (error) {
          // Skip any terms that have calculation errors
        }
      }
      return sum;
    };
  }

  /**
   * Evaluate a limit numerically
   * @param {Function} func - Function to evaluate
   * @param {number} point - Point to approach
   * @param {string} direction - 'left', 'right', or 'both'
   * @returns {Object} Limit evaluation results
   */
  evaluateLimit(func, point, direction = 'both') {
    const delta = this.config.calculusOptions.limitApproachDelta;
    const steps = 5; // Number of evaluation points
    
    const leftPoints = [];
    const rightPoints = [];
    
    try {
      // Evaluate from the left
      if (direction === 'left' || direction === 'both') {
        for (let i = 1; i <= steps; i++) {
          const x = point - delta * Math.pow(0.1, i);
          const y = func(x);
          if (isFinite(y)) {
            leftPoints.push({ x, y });
          }
        }
      }
      
      // Evaluate from the right
      if (direction === 'right' || direction === 'both') {
        for (let i = 1; i <= steps; i++) {
          const x = point + delta * Math.pow(0.1, i);
          const y = func(x);
          if (isFinite(y)) {
            rightPoints.push({ x, y });
          }
        }
      }
      
      // Try to evaluate at the point itself (if possible)
      let directValue = null;
      try {
        const y = func(point);
        if (isFinite(y)) {
          directValue = y;
        }
      } catch (error) {
        // Point not directly evaluable
      }
      
      // Extrapolate limit values
      const leftLimit = leftPoints.length > 0 ? leftPoints[leftPoints.length - 1].y : null;
      const rightLimit = rightPoints.length > 0 ? rightPoints[rightPoints.length - 1].y : null;
      
      // Determine if limit exists
      let limitExists = false;
      let limitValue = null;
      
      if (leftLimit !== null && rightLimit !== null) {
        // Check if left and right limits are close to each other
        if (Math.abs(leftLimit - rightLimit) < 0.0001) {
          limitExists = true;
          limitValue = (leftLimit + rightLimit) / 2;
        }
      } else if (leftLimit !== null) {
        limitValue = leftLimit;
        limitExists = direction === 'left';
      } else if (rightLimit !== null) {
        limitValue = rightLimit;
        limitExists = direction === 'right';
      }
      
      // Check for continuity
      const continuous = limitExists && directValue !== null && 
                         Math.abs(limitValue - directValue) < 0.0001;
      
      return {
        exists: limitExists,
        value: limitValue,
        leftPoints,
        rightPoints,
        directValue,
        continuous
      };
    } catch (error) {
      console.error('Error evaluating limit:', error);
      return {
        exists: false,
        value: null,
        leftPoints: [],
        rightPoints: [],
        directValue: null,
        continuous: false
      };
    }
  }

  /**
   * Calculate Riemann sum
   * @param {Function} func - Function to integrate
   * @param {number} a - Lower limit
   * @param {number} b - Upper limit
   * @param {number} n - Number of rectangles
   * @param {string} type - Type of Riemann sum ('left', 'right', 'midpoint', 'trapezoidal')
   * @returns {Object} Riemann sum data
   */
  calculateRiemannSum(func, a, b, n, type = 'left') {
    if (a > b) [a, b] = [b, a];
    
    const width = (b - a) / n;
    let sum = 0;
    const rectangles = [];
    
    try {
      for (let i = 0; i < n; i++) {
        const x1 = a + i * width;
        const x2 = a + (i + 1) * width;
        
        let height;
        let evaluationPoint;
        
        switch (type) {
          case 'left':
            evaluationPoint = x1;
            height = func(evaluationPoint);
            break;
          case 'right':
            evaluationPoint = x2;
            height = func(evaluationPoint);
            break;
          case 'midpoint':
            evaluationPoint = (x1 + x2) / 2;
            height = func(evaluationPoint);
            break;
          case 'trapezoidal':
            const y1 = func(x1);
            const y2 = func(x2);
            height = (y1 + y2) / 2;
            evaluationPoint = null;
            break;
        }
        
        if (isFinite(height)) {
          const area = width * height;
          sum += area;
          
          rectangles.push({
            x1,
            x2,
            height,
            area,
            evaluationPoint
          });
        }
      }
      
      return {
        sum,
        rectangles
      };
    } catch (error) {
      console.error('Error calculating Riemann sum:', error);
      return {
        sum: NaN,
        rectangles: []
      };
    }
  }

  /**
   * Render the visualization
   */
  render() {
    // Call parent render to clear canvas and draw grid/axes
    super.render();
    
    // Get active function
    const func = this.activeFunction;
    if (!func || !func.visible) return;
    
    // Draw the function
    this.drawFunction(func);
    
    // Draw derivative if enabled
    if (this.config.calculusOptions.showDerivative) {
      this.drawDerivative(func);
    }
    
    // Draw tangent line if enabled
    if (this.config.calculusOptions.showTangent && this.tangentPoint !== null) {
      this.drawTangentLine(func, this.tangentPoint);
    }
    
    // Draw integral if enabled
    if (this.config.calculusOptions.showIntegral) {
      this.drawIntegral(func, 
                       this.config.calculusOptions.lowerLimit, 
                       this.config.calculusOptions.upperLimit);
    }
    
    // Draw Riemann sum if enabled
    if (this.config.calculusOptions.showRiemannSum) {
      this.drawRiemannSum(func,
                         this.config.calculusOptions.lowerLimit,
                         this.config.calculusOptions.upperLimit,
                         this.config.calculusOptions.numRectangles,
                         this.config.calculusOptions.riemannSumType);
    }
    
    // Draw secant line if enabled
    if (this.config.calculusOptions.showSecant) {
      this.drawSecantLine(func, this.secantPoints.x1, this.secantPoints.x2);
    }
    
    // Draw limit visualization if enabled
    if (this.config.calculusOptions.showLimit && this.limitPoint !== null) {
      this.drawLimitVisualization(func, this.limitPoint);
    }
    
    // Draw Taylor series if enabled
    if (this.config.calculusOptions.showTaylorSeries) {
      this.drawTaylorSeries(func, 
                           this.config.calculusOptions.taylorSeriesCenter,
                           this.config.calculusOptions.taylorSeriesTerms);
    }
    
    // Update info panel
    this.updateInfoPanel();
  }

  /**
   * Draw a function
   * @param {Object} func - Function object
   */
  drawFunction(func) {
    const { xMin, xMax } = this.config.range;
    const smoothness = this.config.calculusOptions.smoothness;
    const step = (xMax - xMin) / smoothness;
    
    this.ctx.strokeStyle = func.color;
    this.ctx.lineWidth = func.lineWidth;
    this.ctx.beginPath();
    
    let firstPoint = true;
    let lastY = null;
    
    for (let x = xMin; x <= xMax; x += step) {
      try {
        const y = func.evaluator(x);
        
        // Skip if not a finite number
        if (!isFinite(y)) continue;
        
        // Skip if outside y range to avoid huge jumps
        if (lastY !== null && Math.abs(y - lastY) > (this.config.range.yMax - this.config.range.yMin)) {
          // End current path and start a new one
          this.ctx.stroke();
          this.ctx.beginPath();
          firstPoint = true;
          lastY = y;
          continue;
        }
        
        // Plot the point
        if (firstPoint) {
          this.ctx.moveTo(this.toCanvasX(x), this.toCanvasY(y));
          firstPoint = false;
        } else {
          this.ctx.lineTo(this.toCanvasX(x), this.toCanvasY(y));
        }
        
        lastY = y;
      } catch (error) {
        // End current path and start a new one on error
        this.ctx.stroke();
        this.ctx.beginPath();
        firstPoint = true;
      }
    }
    
    this.ctx.stroke();
  }

  /**
   * Draw the derivative of a function
   * @param {Object} func - Function object
   */
  drawDerivative(func) {
    const { xMin, xMax } = this.config.range;
    const smoothness = this.config.calculusOptions.smoothness;
    const step = (xMax - xMin) / smoothness;
    
    this.ctx.strokeStyle = this.config.calculusOptions.derivativeColor;
    this.ctx.lineWidth = this.config.calculusOptions.derivativeLineWidth;
    this.ctx.beginPath();
    
    let firstPoint = true;
    let lastY = null;
    
    // Get the derivative function
    const derivFunc = this.getDerivativeFunction(func.evaluator);
    
    for (let x = xMin; x <= xMax; x += step) {
      try {
        const y = derivFunc(x);
        
        // Skip if not a finite number
        if (!isFinite(y)) continue;
        
        // Skip if outside reasonable range
        if (lastY !== null && Math.abs(y - lastY) > (this.config.range.yMax - this.config.range.yMin)) {
          // End current path and start a new one
          this.ctx.stroke();
          this.ctx.beginPath();
          firstPoint = true;
          lastY = y;
          continue;
        }
        
        // Plot the point
        if (firstPoint) {
          this.ctx.moveTo(this.toCanvasX(x), this.toCanvasY(y));
          firstPoint = false;
        } else {
          this.ctx.lineTo(this.toCanvasX(x), this.toCanvasY(y));
        }
        
        lastY = y;
      } catch (error) {
        // End current path and start a new one on error
        this.ctx.stroke();
        this.ctx.beginPath();
        firstPoint = true;
      }
    }
    
    this.ctx.stroke();
  }

  /**
   * Draw tangent line at a specific point
   * @param {Object} func - Function object
   * @param {number} x - X-coordinate of tangent point
   */
  drawTangentLine(func, x) {
    try {
      // Evaluate function and derivative at the point
      const y = func.evaluator(x);
      const slope = this.calculateDerivative(func.evaluator, x);
      
      // Skip if not finite
      if (!isFinite(y) || !isFinite(slope)) return;
      
      // Calculate tangent line endpoints
      const tangentLength = this.config.calculusOptions.tangentLength;
      const x1 = x - tangentLength;
      const x2 = x + tangentLength;
      const y1 = y - slope * tangentLength;
      const y2 = y + slope * tangentLength;
      
      // Draw tangent line
      this.ctx.strokeStyle = this.config.calculusOptions.tangentColor;
      this.ctx.lineWidth = this.config.calculusOptions.tangentLineWidth;
      this.ctx.beginPath();
      this.ctx.moveTo(this.toCanvasX(x1), this.toCanvasY(y1));
      this.ctx.lineTo(this.toCanvasX(x2), this.toCanvasY(y2));
      this.ctx.stroke();
      
      // Draw tangent point
      if (this.config.calculusOptions.highlightPoints) {
        this.ctx.fillStyle = this.config.calculusOptions.tangentColor;
        this.ctx.beginPath();
        this.ctx.arc(
          this.toCanvasX(x), 
          this.toCanvasY(y), 
          5, 
          0, 
          2 * Math.PI
        );
        this.ctx.fill();
      }
    } catch (error) {
      console.error('Error drawing tangent line:', error);
    }
  }

  /**
   * Draw the definite integral visualization
   * @param {Object} func - Function object
   * @param {number} a - Lower limit
   * @param {number} b - Upper limit
   */
  drawIntegral(func, a, b) {
    // Ensure a < b
    if (a > b) [a, b] = [b, a];
    
    const smoothness = this.config.calculusOptions.smoothness;
    const step = (b - a) / smoothness;
    
    this.ctx.fillStyle = this.colorWithOpacity(
      this.config.calculusOptions.integralColor, 
      this.config.calculusOptions.integralOpacity
    );
    
    this.ctx.beginPath();
    
    // Start at the lower limit
    try {
      const startY = func.evaluator(a);
      this.ctx.moveTo(this.toCanvasX(a), this.toCanvasY(0));
      this.ctx.lineTo(this.toCanvasX(a), this.toCanvasY(startY));
    } catch (error) {
      // Skip if not evaluable
    }
    
    // Draw the curve
    for (let x = a; x <= b; x += step) {
      try {
        const y = func.evaluator(x);
        
        // Skip if not a finite number
        if (!isFinite(y)) continue;
        
        this.ctx.lineTo(this.toCanvasX(x), this.toCanvasY(y));
      } catch (error) {
        // Skip if not evaluable
      }
    }
    
    // Close the path
    try {
      const endY = func.evaluator(b);
      this.ctx.lineTo(this.toCanvasX(b), this.toCanvasY(endY));
      this.ctx.lineTo(this.toCanvasX(b), this.toCanvasY(0));
    } catch (error) {
      // Skip if not evaluable
    }
    
    this.ctx.closePath();
    this.ctx.fill();
    
    // Draw boundary lines
    this.ctx.strokeStyle = this.config.calculusOptions.integralColor;
    this.ctx.lineWidth = 2;
    this.ctx.setLineDash([5, 3]);
    
    // Lower limit line
    try {
      const ya = func.evaluator(a);
      this.ctx.beginPath();
      this.ctx.moveTo(this.toCanvasX(a), this.toCanvasY(0));
      this.ctx.lineTo(this.toCanvasX(a), this.toCanvasY(ya));
      this.ctx.stroke();
    } catch (error) {
      // Skip if not evaluable
    }
    
    // Upper limit line
    try {
      const yb = func.evaluator(b);
      this.ctx.beginPath();
      this.ctx.moveTo(this.toCanvasX(b), this.toCanvasY(0));
      this.ctx.lineTo(this.toCanvasX(b), this.toCanvasY(yb));
      this.ctx.stroke();
    } catch (error) {
      // Skip if not evaluable
    }
    
    this.ctx.setLineDash([]); // Reset dash pattern
    
    // Calculate and display the integral value
    const integralValue = this.calculateIntegral(
      func.evaluator, 
      a, 
      b, 
      100 // Use 100 intervals for numerical integration
    );
    
    // Draw integral value
    if (isFinite(integralValue)) {
      this.ctx.fillStyle = this.config.calculusOptions.integralColor;
      this.ctx.font = `bold 14px ${this.config.theme.fontFamily}`;
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'bottom';
      
      // Position text in the middle of the integral
      const midX = (a + b) / 2;
      try {
        const midY = func.evaluator(midX) / 2;
        this.ctx.fillText(
          `∫ = ${integralValue.toFixed(4)}`,
          this.toCanvasX(midX),
          this.toCanvasY(midY > 0 ? midY : 0.5)
        );
      } catch (error) {
        // Skip if not evaluable
        this.ctx.fillText(
          `∫ = ${integralValue.toFixed(4)}`,
          this.toCanvasX(midX),
          this.toCanvasY(0.5)
        );
      }
    }
  }

  /**
   * Draw Riemann sum visualization
   * @param {Object} func - Function object
   * @param {number} a - Lower limit
   * @param {number} b - Upper limit
   * @param {number} n - Number of rectangles
   * @param {string} type - Type of Riemann sum
   */
  drawRiemannSum(func, a, b, n, type) {
    // Calculate Riemann sum
    const riemann = this.calculateRiemannSum(
      func.evaluator,
      a,
      b,
      n,
      type
    );
    
    // Draw rectangles
    this.ctx.fillStyle = this.colorWithOpacity(
      this.config.calculusOptions.riemannSumColor,
      this.config.calculusOptions.riemannSumOpacity
    );
    this.ctx.strokeStyle = this.config.calculusOptions.riemannSumColor;
    this.ctx.lineWidth = 1;
    
    for (const rect of riemann.rectangles) {
      const { x1, x2, height } = rect;
      
      // Draw filled rectangle
      this.ctx.fillRect(
        this.toCanvasX(x1),
        this.toCanvasY(Math.max(0, height)),
        this.toCanvasX(x2) - this.toCanvasX(x1),
        this.toCanvasY(0) - this.toCanvasY(Math.max(0, height))
      );
      
      // Draw rectangle outline
      this.ctx.strokeRect(
        this.toCanvasX(x1),
        this.toCanvasY(Math.max(0, height)),
        this.toCanvasX(x2) - this.toCanvasX(x1),
        this.toCanvasY(0) - this.toCanvasY(Math.max(0, height))
      );
      
      // Draw evaluation point indicator if applicable
      if (rect.evaluationPoint !== null && this.config.calculusOptions.highlightPoints) {
        try {
          const evalY = func.evaluator(rect.evaluationPoint);
          
          this.ctx.fillStyle = this.config.calculusOptions.riemannSumColor;
          this.ctx.beginPath();
          this.ctx.arc(
            this.toCanvasX(rect.evaluationPoint),
            this.toCanvasY(evalY),
            3,
            0,
            2 * Math.PI
          );
          this.ctx.fill();
        } catch (error) {
          // Skip if not evaluable
        }
      }
    }
    
    // Draw sum value
    if (isFinite(riemann.sum)) {
      this.ctx.fillStyle = this.config.calculusOptions.riemannSumColor;
      this.ctx.font = `bold 14px ${this.config.theme.fontFamily}`;
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'bottom';
      
      // Position text at the top of the visualization
      const midX = (a + b) / 2;
      this.ctx.fillText(
        `Sum = ${riemann.sum.toFixed(4)}`,
        this.toCanvasX(midX),
        this.toCanvasY(0) + 20
      );
    }
  }

  /**
   * Draw secant line between two points
   * @param {Object} func - Function object
   * @param {number} x1 - First x-coordinate
   * @param {number} x2 - Second x-coordinate
   */
  drawSecantLine(func, x1, x2) {
    try {
      // Evaluate function at both points
      const y1 = func.evaluator(x1);
      const y2 = func.evaluator(x2);
      
      // Skip if not finite
      if (!isFinite(y1) || !isFinite(y2)) return;
      
      // Calculate secant line slope
      const slope = (y2 - y1) / (x2 - x1);
      
      // Draw secant line
      this.ctx.strokeStyle = this.config.calculusOptions.secantColor;
      this.ctx.lineWidth = this.config.calculusOptions.secantLineWidth;
      this.ctx.beginPath();
      this.ctx.moveTo(this.toCanvasX(x1), this.toCanvasY(y1));
      this.ctx.lineTo(this.toCanvasX(x2), this.toCanvasY(y2));
      this.ctx.stroke();
      
      // Draw points
      if (this.config.calculusOptions.highlightPoints) {
        this.ctx.fillStyle = this.config.calculusOptions.secantColor;
        
        // First point
        this.ctx.beginPath();
        this.ctx.arc(
          this.toCanvasX(x1), 
          this.toCanvasY(y1), 
          5, 
          0, 
          2 * Math.PI
        );
        this.ctx.fill();
        
        // Second point
        this.ctx.beginPath();
        this.ctx.arc(
          this.toCanvasX(x2), 
          this.toCanvasY(y2), 
          5, 
          0, 
          2 * Math.PI
        );
        this.ctx.fill();
      }
      
      // Display slope value
      this.ctx.fillStyle = this.config.calculusOptions.secantColor;
      this.ctx.font = `14px ${this.config.theme.fontFamily}`;
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'bottom';
      
      const midX = (x1 + x2) / 2;
      const midY = (y1 + y2) / 2;
      
      this.ctx.fillText(
        `Slope: ${slope.toFixed(4)}`,
        this.toCanvasX(midX),
        this.toCanvasY(midY) - 10
      );
    } catch (error) {
      console.error('Error drawing secant line:', error);
    }
  }

  /**
   * Draw limit visualization
   * @param {Object} func - Function object
   * @param {number} point - Point to evaluate limit at
   */
  drawLimitVisualization(func, point) {
    // Evaluate the limit
    const limitResults = this.evaluateLimit(func.evaluator, point, 'both');
    
    // Draw approach points from left
    if (limitResults.leftPoints.length > 0) {
      this.ctx.fillStyle = 'blue';
      
      for (let i = 0; i < limitResults.leftPoints.length; i++) {
        const { x, y } = limitResults.leftPoints[i];
        const size = 3 + i; // Increasing size as points get closer
        
        this.ctx.beginPath();
        this.ctx.arc(
          this.toCanvasX(x),
          this.toCanvasY(y),
          size,
          0,
          2 * Math.PI
        );
        this.ctx.fill();
      }
    }
    
    // Draw approach points from right
    if (limitResults.rightPoints.length > 0) {
      this.ctx.fillStyle = 'red';
      
      for (let i = 0; i < limitResults.rightPoints.length; i++) {
        const { x, y } = limitResults.rightPoints[i];
        const size = 3 + i; // Increasing size as points get closer
        
        this.ctx.beginPath();
        this.ctx.arc(
          this.toCanvasX(x),
          this.toCanvasY(y),
          size,
          0,
          2 * Math.PI
        );
        this.ctx.fill();
      }
    }
    
    // Draw vertical line at the limit point
    this.ctx.strokeStyle = this.config.calculusOptions.limitColor;
    this.ctx.lineWidth = 1;
    this.ctx.setLineDash([5, 3]);
    this.ctx.beginPath();
    this.ctx.moveTo(this.toCanvasX(point), this.toCanvasY(this.config.range.yMin));
    this.ctx.lineTo(this.toCanvasX(point), this.toCanvasY(this.config.range.yMax));
    this.ctx.stroke();
    this.ctx.setLineDash([]);
    
    // Draw limit value indicator
    if (limitResults.exists && limitResults.value !== null) {
      // Draw horizontal line at the limit value
      this.ctx.strokeStyle = this.config.calculusOptions.limitColor;
      this.ctx.lineWidth = 1;
      this.ctx.setLineDash([5, 3]);
      this.ctx.beginPath();
      this.ctx.moveTo(this.toCanvasX(this.config.range.xMin), this.toCanvasY(limitResults.value));
      this.ctx.lineTo(this.toCanvasX(this.config.range.xMax), this.toCanvasY(limitResults.value));
      this.ctx.stroke();
      this.ctx.setLineDash([]);
      
      // Draw limit value
      this.ctx.fillStyle = this.config.calculusOptions.limitColor;
      this.ctx.font = `bold 14px ${this.config.theme.fontFamily}`;
      this.ctx.textAlign = 'left';
      this.ctx.textBaseline = 'bottom';
      
      this.ctx.fillText(
        `Limit: ${limitResults.value.toFixed(4)}`,
        this.toCanvasX(point) + 10,
        this.toCanvasY(limitResults.value) - 10
      );
      
      // Draw direct value if it exists and different from limit
      if (limitResults.directValue !== null && 
          Math.abs(limitResults.directValue - limitResults.value) > 0.0001) {
        
        this.ctx.fillStyle = 'green';
        this.ctx.beginPath();
        this.ctx.arc(
          this.toCanvasX(point),
          this.toCanvasY(limitResults.directValue),
          6,
          0,
          2 * Math.PI
        );
        this.ctx.fill();
        
        this.ctx.fillText(
          `f(${point}) = ${limitResults.directValue.toFixed(4)}`,
          this.toCanvasX(point) + 10,
          this.toCanvasY(limitResults.directValue) - 10
        );
      }
      
      // Draw continuity status
      this.ctx.fillStyle = limitResults.continuous ? 'green' : 'red';
      this.ctx.font = `14px ${this.config.theme.fontFamily}`;
      this.ctx.textAlign = 'left';
      this.ctx.textBaseline = 'top';
      
      this.ctx.fillText(
        limitResults.continuous ? 'Continuous at this point' : 'Discontinuous at this point',
        this.toCanvasX(point) + 10,
        this.toCanvasY(limitResults.value) + 10
      );
    }
  }

  /**
   * Draw Taylor series approximation
   * @param {Object} func - Function object
   * @param {number} center - Center point of the Taylor series
   * @param {number} terms - Number of terms to include
   */
  drawTaylorSeries(func, center, terms) {
    try {
      // Get Taylor series function
      const taylorFunc = this.getTaylorSeriesFunction(
        func.evaluator,
        center,
        terms
      );
      
      // Draw the Taylor polynomial
      const { xMin, xMax } = this.config.range;
      const smoothness = this.config.calculusOptions.smoothness;
      const step = (xMax - xMin) / smoothness;
      
      this.ctx.strokeStyle = this.config.calculusOptions.taylorSeriesColor;
      this.ctx.lineWidth = this.config.calculusOptions.taylorSeriesLineWidth;
      this.ctx.beginPath();
      
      let firstPoint = true;
      let lastY = null;
      
      for (let x = xMin; x <= xMax; x += step) {
        try {
          const y = taylorFunc(x);
          
          // Skip if not a finite number
          if (!isFinite(y)) continue;
          
          // Skip if outside reasonable range
          if (lastY !== null && Math.abs(y - lastY) > (this.config.range.yMax - this.config.range.yMin)) {
            // End current path and start a new one
            this.ctx.stroke();
            this.ctx.beginPath();
            firstPoint = true;
            lastY = y;
            continue;
          }
          
          // Plot the point
          if (firstPoint) {
            this.ctx.moveTo(this.toCanvasX(x), this.toCanvasY(y));
            firstPoint = false;
          } else {
            this.ctx.lineTo(this.toCanvasX(x), this.toCanvasY(y));
          }
          
          lastY = y;
        } catch (error) {
          // End current path and start a new one on error
          this.ctx.stroke();
          this.ctx.beginPath();
          firstPoint = true;
        }
      }
      
      this.ctx.stroke();
      
      // Draw center point
      if (this.config.calculusOptions.highlightPoints) {
        try {
          const centerY = func.evaluator(center);
          
          this.ctx.fillStyle = this.config.calculusOptions.taylorSeriesColor;
          this.ctx.beginPath();
          this.ctx.arc(
            this.toCanvasX(center),
            this.toCanvasY(centerY),
            5,
            0,
            2 * Math.PI
          );
          this.ctx.fill();
          
          // Draw center point label
          this.ctx.fillStyle = this.config.calculusOptions.taylorSeriesColor;
          this.ctx.font = `14px ${this.config.theme.fontFamily}`;
          this.ctx.textAlign = 'left';
          this.ctx.textBaseline = 'bottom';
          
          this.ctx.fillText(
            `Taylor series (center: ${center}, terms: ${terms})`,
            this.toCanvasX(center) + 10,
            this.toCanvasY(centerY) - 10
          );
        } catch (error) {
          // Skip if not evaluable
        }
      }
    } catch (error) {
      console.error('Error drawing Taylor series:', error);
    }
  }

  /**
   * Add opacity to a color
   * @param {string} color - CSS color string
   * @param {number} opacity - Opacity value (0-1)
   * @returns {string} Color with opacity
   */
  colorWithOpacity(color, opacity) {
    // Check if already rgba
    if (color.startsWith('rgba')) {
      return color;
    }
    
    // Convert hex to rgba
    if (color.startsWith('#')) {
      const r = parseInt(color.slice(1, 3), 16);
      const g = parseInt(color.slice(3, 5), 16);
      const b = parseInt(color.slice(5, 7), 16);
      return `rgba(${r}, ${g}, ${b}, ${opacity})`;
    }
    
    // Convert rgb to rgba
    if (color.startsWith('rgb(')) {
      const rgb = color.slice(4, -1).split(',').map(x => x.trim());
      return `rgba(${rgb[0]}, ${rgb[1]}, ${rgb[2]}, ${opacity})`;
    }
    
    // Default fallback
    return color;
  }

  /**
   * Update information in the info panel
   */
  updateInfoPanel() {
    if (!this.infoPanel) return;
    
    // Clear existing info
    this.infoPanel.innerHTML = '';
    
    // Get active function
    const func = this.activeFunction;
    if (!func) return;
    
    // Add title
    const title = document.createElement('h3');
    title.style.margin = '0 0 10px 0';
    title.style.fontSize = '16px';
    title.textContent = 'Calculus Tools';
    this.infoPanel.appendChild(title);
    
    // Add function expression
    this.addInfo('function-expression', 'Function', func.expression);
    
    // Add derivative information if enabled
    if (this.config.calculusOptions.showDerivative) {
      // Attempt to compute a symbolic derivative (very basic for demonstration)
      let symbolicDerivative = "Not available";
      this.addInfo('derivative-expression', 'Derivative', symbolicDerivative);
    }
    
    // Add tangent information if enabled
    if (this.config.calculusOptions.showTangent && this.tangentPoint !== null) {
      try {
        const x = this.tangentPoint;
        const y = func.evaluator(x);
        const slope = this.calculateDerivative(func.evaluator, x);
        
        if (isFinite(y) && isFinite(slope)) {
          this.addInfo('tangent-point', 'Tangent Point', `(${x.toFixed(4)}, ${y.toFixed(4)})`);
          this.addInfo('tangent-slope', 'Slope', slope.toFixed(4));
          this.addInfo('tangent-equation', 'Equation', `y - ${y.toFixed(4)} = ${slope.toFixed(4)}(x - ${x.toFixed(4)})`);
        }
      } catch (error) {
        // Skip if not evaluable
      }
    }
    
    // Add integral information if enabled
    if (this.config.calculusOptions.showIntegral) {
      const a = this.config.calculusOptions.lowerLimit;
      const b = this.config.calculusOptions.upperLimit;
      
      try {
        const integralValue = this.calculateIntegral(
          func.evaluator, 
          a, 
          b, 
          100 // Use 100 intervals for numerical integration
        );
        
        if (isFinite(integralValue)) {
          this.addInfo('integral-bounds', 'Bounds', `[${a}, ${b}]`);
          this.addInfo('integral-value', 'Value', integralValue.toFixed(6));
        }
      } catch (error) {
        // Skip if not evaluable
      }
    }
    
    // Add Riemann sum information if enabled
    if (this.config.calculusOptions.showRiemannSum) {
      const a = this.config.calculusOptions.lowerLimit;
      const b = this.config.calculusOptions.upperLimit;
      const n = this.config.calculusOptions.numRectangles;
      const type = this.config.calculusOptions.riemannSumType;
      
      try {
        const riemann = this.calculateRiemannSum(
          func.evaluator,
          a,
          b,
          n,
          type
        );
        
        if (isFinite(riemann.sum)) {
          this.addInfo('riemann-bounds', 'Bounds', `[${a}, ${b}]`);
          this.addInfo('riemann-type', 'Type', type.charAt(0).toUpperCase() + type.slice(1));
          this.addInfo('riemann-rectangles', 'Rectangles', n.toString());
          this.addInfo('riemann-sum', 'Sum', riemann.sum.toFixed(6));
        }
      } catch (error) {
        // Skip if not evaluable
      }
    }
    
    // Add secant information if enabled
    if (this.config.calculusOptions.showSecant) {
      try {
        const x1 = this.secantPoints.x1;
        const x2 = this.secantPoints.x2;
        const y1 = func.evaluator(x1);
        const y2 = func.evaluator(x2);
        
        if (isFinite(y1) && isFinite(y2)) {
          const slope = (y2 - y1) / (x2 - x1);
          
          this.addInfo('secant-points', 'Points', `(${x1.toFixed(4)}, ${y1.toFixed(4)}) and (${x2.toFixed(4)}, ${y2.toFixed(4)})`);
          this.addInfo('secant-slope', 'Slope', slope.toFixed(4));
          this.addInfo('secant-equation', 'Equation', `y - ${y1.toFixed(4)} = ${slope.toFixed(4)}(x - ${x1.toFixed(4)})`);
          
          // Calculate average rate of change
          this.addInfo('secant-average-rate', 'Avg. Rate of Change', slope.toFixed(6));
        }
      } catch (error) {
        // Skip if not evaluable
      }
    }
    
    // Add limit information if enabled
    if (this.config.calculusOptions.showLimit && this.limitPoint !== null) {
      try {
        const point = this.limitPoint;
        const limitResults = this.evaluateLimit(func.evaluator, point, 'both');
        
        this.addInfo('limit-point', 'Point', point.toFixed(4));
        
        if (limitResults.exists) {
          this.addInfo('limit-value', 'Limit Value', limitResults.value.toFixed(6));
          this.addInfo('limit-exists', 'Limit Exists', 'Yes');
          
          if (limitResults.directValue !== null) {
            this.addInfo('direct-value', `f(${point.toFixed(2)})`, limitResults.directValue.toFixed(6));
            this.addInfo('continuity', 'Continuous', limitResults.continuous ? 'Yes' : 'No');
          } else {
            this.addInfo('direct-value', `f(${point.toFixed(2)})`, 'Not defined');
            this.addInfo('continuity', 'Continuous', 'No');
          }
        } else {
          this.addInfo('limit-exists', 'Limit Exists', 'No');
          
          if (limitResults.leftPoints.length > 0 && limitResults.rightPoints.length > 0) {
            const leftLimit = limitResults.leftPoints[limitResults.leftPoints.length - 1].y;
            const rightLimit = limitResults.rightPoints[limitResults.rightPoints.length - 1].y;
            
            this.addInfo('left-limit', 'Left Limit', leftLimit.toFixed(6));
            this.addInfo('right-limit', 'Right Limit', rightLimit.toFixed(6));
          }
        }
      } catch (error) {
        // Skip if not evaluable
      }
    }
    
    // Add Taylor series information if enabled
    if (this.config.calculusOptions.showTaylorSeries) {
      const center = this.config.calculusOptions.taylorSeriesCenter;
      const terms = this.config.calculusOptions.taylorSeriesTerms;
      
      this.addInfo('taylor-center', 'Center', center.toString());
      this.addInfo('taylor-terms', 'Terms', terms.toString());
      
      // Display first few terms symbolically (simplified)
      try {
        const f0 = func.evaluator(center);
        
        if (isFinite(f0)) {
          let taylorExpression = `${f0.toFixed(4)}`;
          
          // Calculate derivatives at center
          const derivatives = [func.evaluator];
          
          for (let i = 1; i <= Math.min(3, terms); i++) {
            derivatives.push(this.getDerivativeFunction(derivatives[i-1]));
            const df = derivatives[i](center);
            
            if (isFinite(df) && Math.abs(df) > 1e-10) {
              const sign = df >= 0 ? '+ ' : '- ';
              const coeff = Math.abs(df) / this.factorial(i);
              
              if (i === 1) {
                taylorExpression += ` ${sign}${coeff.toFixed(4)}(x - ${center})`;
              } else {
                taylorExpression += ` ${sign}${coeff.toFixed(4)}(x - ${center})^${i}`;
              }
            }
          }
          
          if (terms > 3) {
            taylorExpression += ` + ...`;
          }
          
          this.addInfo('taylor-expression', 'Expansion', taylorExpression);
        }
      } catch (error) {
        // Skip if not evaluable
      }
    }
  }

  /**
   * Add standard controls to the control panel
   */
  addStandardControls() {
    if (!this.controlsArea) return;
    
    // Add function input field
    this.addControl('text', {
      id: 'function-input',
      label: 'Function f(x)',
      value: this.activeFunction ? this.activeFunction.expression : this.config.calculusOptions.defaultFunction,
      onSubmit: (value) => {
        try {
          // Validate by creating an evaluator
          const evaluator = this.createFunctionEvaluator(value);
          
          // Update active function
          if (this.activeFunction) {
            this.activeFunction.expression = value;
            this.activeFunction.evaluator = evaluator;
          } else {
            this.addFunction({ expression: value });
          }
          
          this.render();
        } catch (error) {
          alert(`Invalid function: ${error.message}`);
        }
      }
    });
    
    // Add separator
    const separator1 = document.createElement('hr');
    separator1.style.margin = '15px 0';
    separator1.style.border = 'none';
    separator1.style.borderTop = `1px solid ${this.config.theme.borderColor}`;
    this.controlsArea.appendChild(separator1);
    
    // Add tools section title
    const toolsTitle = document.createElement('h3');
    toolsTitle.style.margin = '0 0 10px 0';
    toolsTitle.style.fontSize = '16px';
    toolsTitle.textContent = 'Calculus Tools';
    this.controlsArea.appendChild(toolsTitle);
    
    // Add derivative toggle
    this.addControl('checkbox', {
      id: 'show-derivative',
      text: 'Show Derivative',
      checked: this.config.calculusOptions.showDerivative,
      onChange: (checked) => {
        this.config.calculusOptions.showDerivative = checked;
        this.render();
      }
    });
    
    // Add tangent line toggle
    this.addControl('checkbox', {
      id: 'show-tangent',
      text: 'Show Tangent Line',
      checked: this.config.calculusOptions.showTangent,
      onChange: (checked) => {
        this.config.calculusOptions.showTangent = checked;
        if (checked && this.tangentPoint === null) {
          this.tangentPoint = 0;
        }
        this.render();
      }
    });
    
    // Add integral toggle
    this.addControl('checkbox', {
      id: 'show-integral',
      text: 'Show Definite Integral',
      checked: this.config.calculusOptions.showIntegral,
      onChange: (checked) => {
        this.config.calculusOptions.showIntegral = checked;
        this.render();
        
        // Show integral bounds controls if enabled
        document.getElementById('integral-bounds').style.display = 
          checked ? 'block' : 'none';
      }
    });
    
    // Add integral bounds controls (initially hidden if not enabled)
    const integralBoundsContainer = document.createElement('div');
    integralBoundsContainer.id = 'integral-bounds';
    integralBoundsContainer.style.margin = '10px 0';
    integralBoundsContainer.style.padding = '10px';
    integralBoundsContainer.style.border = `1px solid ${this.config.theme.borderColor}`;
    integralBoundsContainer.style.borderRadius = '5px';
    integralBoundsContainer.style.display = 
      this.config.calculusOptions.showIntegral ? 'block' : 'none';
    
    // Add lower bound input
    const lowerBoundLabel = document.createElement('label');
    lowerBoundLabel.textContent = 'Lower Bound:';
    lowerBoundLabel.style.display = 'block';
    lowerBoundLabel.style.marginBottom = '5px';
    
    const lowerBoundInput = document.createElement('input');
    lowerBoundInput.type = 'number';
    lowerBoundInput.value = this.config.calculusOptions.lowerLimit;
    lowerBoundInput.style.width = '100%';
    lowerBoundInput.style.marginBottom = '10px';
    lowerBoundInput.addEventListener('change', () => {
      this.config.calculusOptions.lowerLimit = parseFloat(lowerBoundInput.value);
      this.render();
    });
    
    // Add upper bound input
    const upperBoundLabel = document.createElement('label');
    upperBoundLabel.textContent = 'Upper Bound:';
    upperBoundLabel.style.display = 'block';
    upperBoundLabel.style.marginBottom = '5px';
    
    const upperBoundInput = document.createElement('input');
    upperBoundInput.type = 'number';
    upperBoundInput.value = this.config.calculusOptions.upperLimit;
    upperBoundInput.style.width = '100%';
    upperBoundInput.addEventListener('change', () => {
      this.config.calculusOptions.upperLimit = parseFloat(upperBoundInput.value);
      this.render();
    });
    
    integralBoundsContainer.appendChild(lowerBoundLabel);
    integralBoundsContainer.appendChild(lowerBoundInput);
    integralBoundsContainer.appendChild(upperBoundLabel);
    integralBoundsContainer.appendChild(upperBoundInput);
    
    this.controlsArea.appendChild(integralBoundsContainer);
    
    // Add Riemann sum toggle
    this.addControl('checkbox', {
      id: 'show-riemann-sum',
      text: 'Show Riemann Sum',
      checked: this.config.calculusOptions.showRiemannSum,
      onChange: (checked) => {
        this.config.calculusOptions.showRiemannSum = checked;
        this.render();
        
        // Show Riemann sum controls if enabled
        document.getElementById('riemann-sum-controls').style.display = 
          checked ? 'block' : 'none';
      }
    });
    
    // Add Riemann sum controls (initially hidden if not enabled)
    const riemannSumContainer = document.createElement('div');
    riemannSumContainer.id = 'riemann-sum-controls';
    riemannSumContainer.style.margin = '10px 0';
    riemannSumContainer.style.padding = '10px';
    riemannSumContainer.style.border = `1px solid ${this.config.theme.borderColor}`;
    riemannSumContainer.style.borderRadius = '5px';
    riemannSumContainer.style.display = 
      this.config.calculusOptions.showRiemannSum ? 'block' : 'none';
    
    // Add number of rectangles slider
    const rectanglesLabel = document.createElement('label');
    rectanglesLabel.textContent = 'Number of Rectangles:';
    rectanglesLabel.style.display = 'block';
    rectanglesLabel.style.marginBottom = '5px';
    
    const rectanglesSlider = document.createElement('input');
    rectanglesSlider.type = 'range';
    rectanglesSlider.min = '1';
    rectanglesSlider.max = '50';
    rectanglesSlider.value = this.config.calculusOptions.numRectangles;
    rectanglesSlider.style.width = '100%';
    rectanglesSlider.style.marginBottom = '10px';
    rectanglesSlider.addEventListener('input', () => {
      this.config.calculusOptions.numRectangles = parseInt(rectanglesSlider.value);
      rectanglesValue.textContent = rectanglesSlider.value;
      this.render();
    });
    
    const rectanglesValue = document.createElement('span');
    rectanglesValue.textContent = rectanglesSlider.value;
    rectanglesValue.style.marginLeft = '5px';
    rectanglesLabel.appendChild(rectanglesValue);
    
    // Add Riemann sum type dropdown
    const typeLabel = document.createElement('label');
    typeLabel.textContent = 'Riemann Sum Type:';
    typeLabel.style.display = 'block';
    typeLabel.style.marginBottom = '5px';
    
    const typeSelect = document.createElement('select');
    typeSelect.style.width = '100%';
    
    const typeOptions = [
      { value: 'left', text: 'Left Sum' },
      { value: 'right', text: 'Right Sum' },
      { value: 'midpoint', text: 'Midpoint Sum' },
      { value: 'trapezoidal', text: 'Trapezoidal Sum' }
    ];
    
    typeOptions.forEach(option => {
      const optElement = document.createElement('option');
      optElement.value = option.value;
      optElement.textContent = option.text;
      if (option.value === this.config.calculusOptions.riemannSumType) {
        optElement.selected = true;
      }
      typeSelect.appendChild(optElement);
    });
    
    typeSelect.addEventListener('change', () => {
      this.config.calculusOptions.riemannSumType = typeSelect.value;
      this.render();
    });
    
    riemannSumContainer.appendChild(rectanglesLabel);
    riemannSumContainer.appendChild(rectanglesSlider);
    riemannSumContainer.appendChild(typeLabel);
    riemannSumContainer.appendChild(typeSelect);
    
    this.controlsArea.appendChild(riemannSumContainer);
    
    // Add secant line toggle
    this.addControl('checkbox', {
      id: 'show-secant',
      text: 'Show Secant Line',
      checked: this.config.calculusOptions.showSecant,
      onChange: (checked) => {
        this.config.calculusOptions.showSecant = checked;
        this.render();
      }
    });
    
    // Add limit toggle
    this.addControl('checkbox', {
      id: 'show-limit',
      text: 'Show Limit',
      checked: this.config.calculusOptions.showLimit,
      onChange: (checked) => {
        this.config.calculusOptions.showLimit = checked;
        if (checked && this.limitPoint === null) {
          this.limitPoint = 0;
        }
        this.render();
      }
    });
    
    // Add Taylor series toggle
    this.addControl('checkbox', {
      id: 'show-taylor-series',
      text: 'Show Taylor Series',
      checked: this.config.calculusOptions.showTaylorSeries,
      onChange: (checked) => {
        this.config.calculusOptions.showTaylorSeries = checked;
        this.render();
        
        // Show Taylor series controls if enabled
        document.getElementById('taylor-series-controls').style.display = 
          checked ? 'block' : 'none';
      }
    });
    
    // Add Taylor series controls (initially hidden if not enabled)
    const taylorSeriesContainer = document.createElement('div');
    taylorSeriesContainer.id = 'taylor-series-controls';
    taylorSeriesContainer.style.margin = '10px 0';
    taylorSeriesContainer.style.padding = '10px';
    taylorSeriesContainer.style.border = `1px solid ${this.config.theme.borderColor}`;
    taylorSeriesContainer.style.borderRadius = '5px';
    taylorSeriesContainer.style.display = 
      this.config.calculusOptions.showTaylorSeries ? 'block' : 'none';
    
    // Add center point input
    const centerLabel = document.createElement('label');
    centerLabel.textContent = 'Center Point:';
    centerLabel.style.display = 'block';
    centerLabel.style.marginBottom = '5px';
    
    const centerInput = document.createElement('input');
    centerInput.type = 'number';
    centerInput.value = this.config.calculusOptions.taylorSeriesCenter;
    centerInput.style.width = '100%';
    centerInput.style.marginBottom = '10px';
    centerInput.addEventListener('change', () => {
      this.config.calculusOptions.taylorSeriesCenter = parseFloat(centerInput.value);
      this.render();
    });
    
    // Add number of terms slider
    const termsLabel = document.createElement('label');
    termsLabel.textContent = 'Number of Terms:';
    termsLabel.style.display = 'block';
    termsLabel.style.marginBottom = '5px';
    
    const termsSlider = document.createElement('input');
    termsSlider.type = 'range';
    termsSlider.min = '1';
    termsSlider.max = '10';
    termsSlider.value = this.config.calculusOptions.taylorSeriesTerms;
    termsSlider.style.width = '100%';
    termsSlider.addEventListener('input', () => {
      this.config.calculusOptions.taylorSeriesTerms = parseInt(termsSlider.value);
      termsValue.textContent = termsSlider.value;
      this.render();
    });
    
    const termsValue = document.createElement('span');
    termsValue.textContent = termsSlider.value;
    termsValue.style.marginLeft = '5px';
    termsLabel.appendChild(termsValue);
    
    taylorSeriesContainer.appendChild(centerLabel);
    taylorSeriesContainer.appendChild(centerInput);
    taylorSeriesContainer.appendChild(termsLabel);
    taylorSeriesContainer.appendChild(termsSlider);
    
    this.controlsArea.appendChild(taylorSeriesContainer);
    
    // Add separator
    const separator2 = document.createElement('hr');
    separator2.style.margin = '15px 0';
    separator2.style.border = 'none';
    separator2.style.borderTop = `1px solid ${this.config.theme.borderColor}`;
    this.controlsArea.appendChild(separator2);
    
    // Add display options section title
    const displayTitle = document.createElement('h3');
    displayTitle.style.margin = '0 0 10px 0';
    displayTitle.style.fontSize = '16px';
    displayTitle.textContent = 'Display Options';
    this.controlsArea.appendChild(displayTitle);
    
    // Add range controls
    this.addControl('slider', {
      id: 'x-range',
      label: 'X Range',
      min: 1,
      max: 20,
      step: 1,
      value: this.config.range.xMax,
      onChange: (value) => {
        const range = parseInt(value);
        this.setRange({
          xMin: -range,
          xMax: range
        });
        this.render();
      }
    });
    
    this.addControl('slider', {
      id: 'y-range',
      label: 'Y Range',
      min: 1,
      max: 20,
      step: 1,
      value: this.config.range.yMax,
      onChange: (value) => {
        const range = parseInt(value);
        this.setRange({
          yMin: -range,
          yMax: range
        });
        this.render();
      }
    });
    
    // Add grid toggle
    this.addControl('checkbox', {
      id: 'show-grid',
      text: 'Show Grid',
      checked: this.config.showGrid,
      onChange: (checked) => {
        this.config.showGrid = checked;
        this.render();
      }
    });
  }

  /**
   * Add a custom text input control
   * @param {Object} options - Text input options
   * @returns {HTMLDivElement} Control container
   */
  addControl(type, options) {
    if (type === 'text') {
      return this.addTextControl(options);
    }
    
    return super.addControl(type, options);
  }

  /**
   * Add a text input control
   * @param {Object} options - Text input options
   * @returns {HTMLDivElement} Control container
   */
  addTextControl(options) {
    if (!this.controlsArea) {
      throw new Error('Control panel not enabled in configuration');
    }
    
    // Create control group
    const controlGroup = document.createElement('div');
    controlGroup.style.marginBottom = '20px';
    
    // Add label if provided
    if (options.label) {
      const label = document.createElement('label');
      label.textContent = options.label;
      label.style.display = 'block';
      label.style.marginBottom = '5px';
      controlGroup.appendChild(label);
    }
    
    // Create input container for submit button layout
    const inputContainer = document.createElement('div');
    inputContainer.style.display = 'flex';
    
    // Create the text input
    const textInput = document.createElement('input');
    textInput.type = 'text';
    textInput.id = options.id;
    textInput.value = options.value || '';
    textInput.style.flex = '1';
    textInput.style.marginRight = '5px';
    textInput.style.padding = '5px';
    
    // Create submit button
    const submitButton = document.createElement('button');
    submitButton.textContent = 'Apply';
    submitButton.style.padding = '5px 10px';
    submitButton.style.backgroundColor = this.config.theme.buttonColor;
    submitButton.style.color = this.config.theme.buttonTextColor;
    submitButton.style.border = 'none';
    submitButton.style.borderRadius = '4px';
    submitButton.style.cursor = 'pointer';
    
    // Handle submission
    const handleSubmit = () => {
      if (options.onSubmit) {
        options.onSubmit(textInput.value);
      }
    };
    
    submitButton.addEventListener('click', handleSubmit);
    textInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        handleSubmit();
      }
    });
    
    // Add to containers
    inputContainer.appendChild(textInput);
    inputContainer.appendChild(submitButton);
    controlGroup.appendChild(inputContainer);
    
    this.controlsArea.appendChild(controlGroup);
    
    return controlGroup;
  }
}

export default CalculusTools;