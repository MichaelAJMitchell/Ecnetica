// math_explorer.js - Core library for creating interactive math visualizations
class MathExplorer {
    constructor(containerId, options = {}) {
      this.container = document.getElementById(containerId);
      if (!this.container) {
        console.error(`Container with ID ${containerId} not found`);
        return;
      }
  
      // Default options
      this.options = {
        title: 'Math Function Explorer',
        xMin: -10,
        xMax: 10,
        yMin: -10, 
        yMax: 10,
        gridSpacing: 1,
        padding: 30,
        ...options
      };
  
      // Initialize the UI
      this.initUI();
      this.initCanvas();
      
      // Store controls and parameters
      this.controls = [];
      this.specialPoints = [];
      this.infoFields = [];
      
      // Create the function evaluator
      this.evaluator = () => 0;
    }
  
    initUI() {
      // Create basic structure
      this.container.innerHTML = `
        <div style="font-family: 'Arial', sans-serif; max-width: 900px; margin: 0 auto; padding: 20px;">
          <h2 style="text-align: center; color: #2c3e50;">${this.options.title}</h2>
          <div style="display: flex; flex-wrap: wrap; gap: 20px;">
            <div style="flex: 1; min-width: 300px;" id="${this.container.id}-controls">
              <!-- Controls will be added here -->
              <div style="margin-top: 30px; padding: 15px; background-color: #f8f9fa; border-radius: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);" id="${this.container.id}-info">
                <h3 style="margin-top: 0; color: #2c3e50;">Function Properties:</h3>
                <!-- Info fields will be added here -->
              </div>
            </div>
            <div style="flex: 2; min-width: 400px;">
              <div style="width: 100%; height: 400px; border: 1px solid #ddd; border-radius: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <canvas id="${this.container.id}-canvas" style="width: 100%; height: 100%;"></canvas>
              </div>
            </div>
          </div>
        </div>
      `;
      
      this.controlsContainer = document.getElementById(`${this.container.id}-controls`);
      this.infoContainer = document.getElementById(`${this.container.id}-info`);
    }
  
    initCanvas() {
      this.canvas = document.getElementById(`${this.container.id}-canvas`);
      this.ctx = this.canvas.getContext('2d');
      
      // Set canvas dimensions to match its display size
      const resizeCanvas = () => {
        const displayWidth = this.canvas.clientWidth;
        const displayHeight = this.canvas.clientHeight;
        
        if (this.canvas.width !== displayWidth || this.canvas.height !== displayHeight) {
          this.canvas.width = displayWidth;
          this.canvas.height = displayHeight;
        }
        
        // Redraw after resize
        this.updateGraph();
      };
      
      resizeCanvas();
      window.addEventListener('resize', resizeCanvas);
    }
  
    addControl(id, label, min, max, value, step) {
      const controlDiv = document.createElement('div');
      controlDiv.style.marginBottom = '20px';
      
      const controlHTML = `
        <label for="${id}">${label}: <span id="${id}-display">${value}</span></label>
        <input type="range" id="${id}" min="${min}" max="${max}" value="${value}" step="${step}" style="width: 100%;">
      `;
      
      controlDiv.innerHTML = controlHTML;
      this.controlsContainer.insertBefore(controlDiv, this.infoContainer);
      
      const slider = document.getElementById(id);
      const display = document.getElementById(`${id}-display`);
      
      // Store control info
      this.controls.push({ id, slider, display, value });
      
      // Add event listener
      slider.addEventListener('input', () => {
        const val = parseFloat(slider.value);
        display.textContent = val.toFixed(1);
        this.controls.find(c => c.id === id).value = val;
        this.updateGraph();
      });
      
      return this;
    }
  
    addInfoField(id, label) {
      const infoP = document.createElement('p');
      infoP.innerHTML = `${label}: <span id="${id}">${label}</span>`;
      this.infoContainer.appendChild(infoP);
      
      const display = document.getElementById(id);
      this.infoFields.push({ id, display, label });
      
      return this;
    }
    
    updateInfoField(id, value) {
      const field = this.infoFields.find(f => f.id === id);
      if (field && field.display) {
        field.display.textContent = value;
      }
      return this;
    }
  
    setFunction(fn) {
      this.evaluator = fn;
      this.updateGraph();
      return this;
    }
    
    addSpecialPoint(calculator, color) {
      this.specialPoints.push({ calculator, color });
      return this;
    }
  
    toCanvasX(x) {
      return ((x - this.options.xMin) / (this.options.xMax - this.options.xMin)) * 
        (this.canvas.width - 2 * this.options.padding) + this.options.padding;
    }
    
    toCanvasY(y) {
      return this.canvas.height - 
        (((y - this.options.yMin) / (this.options.yMax - this.options.yMin)) * 
        (this.canvas.height - 2 * this.options.padding) + this.options.padding);
    }
  
    drawGrid() {
      // Draw grid lines
      this.ctx.strokeStyle = '#e1e1e1';
      this.ctx.lineWidth = 1;
      
      // Vertical grid lines
      for (let x = Math.ceil(this.options.xMin); x <= this.options.xMax; x += this.options.gridSpacing) {
        this.ctx.beginPath();
        this.ctx.moveTo(this.toCanvasX(x), 0);
        this.ctx.lineTo(this.toCanvasX(x), this.canvas.height);
        this.ctx.stroke();
      }
      
      // Horizontal grid lines
      for (let y = Math.ceil(this.options.yMin); y <= this.options.yMax; y += this.options.gridSpacing) {
        this.ctx.beginPath();
        this.ctx.moveTo(0, this.toCanvasY(y));
        this.ctx.lineTo(this.canvas.width, this.toCanvasY(y));
        this.ctx.stroke();
      }
      
      // Axes
      this.ctx.strokeStyle = '#000';
      this.ctx.lineWidth = 2;
      
      // X-axis
      this.ctx.beginPath();
      this.ctx.moveTo(this.toCanvasX(this.options.xMin), this.toCanvasY(0));
      this.ctx.lineTo(this.toCanvasX(this.options.xMax), this.toCanvasY(0));
      this.ctx.stroke();
      
      // Y-axis
      this.ctx.beginPath();
      this.ctx.moveTo(this.toCanvasX(0), this.toCanvasY(this.options.yMin));
      this.ctx.lineTo(this.toCanvasX(0), this.toCanvasY(this.options.yMax));
      this.ctx.stroke();
      
      // Axis labels
      this.ctx.fillStyle = '#000';
      this.ctx.font = '12px Arial';
      this.ctx.textAlign = 'center';
      
      // X-axis labels
      for (let x = Math.ceil(this.options.xMin); x <= this.options.xMax; x += this.options.gridSpacing) {
        if (x !== 0) {  // Skip zero to avoid overlapping with y-axis label
          this.ctx.fillText(x.toString(), this.toCanvasX(x), this.toCanvasY(0) + 15);
        }
      }
      
      // Y-axis labels
      this.ctx.textAlign = 'right';
      for (let y = Math.ceil(this.options.yMin); y <= this.options.yMax; y += this.options.gridSpacing) {
        if (y !== 0) {  // Skip zero to avoid overlapping with x-axis label
          this.ctx.fillText(y.toString(), this.toCanvasX(0) - 5, this.toCanvasY(y) + 4);
        }
      }
      
      // Origin label
      this.ctx.fillText("0", this.toCanvasX(0) - 5, this.toCanvasY(0) + 15);
    }
  
    drawFunction() {
      this.ctx.strokeStyle = '#3498db';
      this.ctx.lineWidth = 3;
      this.ctx.beginPath();
      
      const step = (this.options.xMax - this.options.xMin) / this.canvas.width;
      let isFirstPoint = true;
      
      // Get control values for the evaluator
      const params = this.controls.map(c => c.value);
      
      for (let x = this.options.xMin; x <= this.options.xMax; x += step) {
        const y = this.evaluator(x, ...params);
        
        if (y >= this.options.yMin && y <= this.options.yMax) {
          if (isFirstPoint) {
            this.ctx.moveTo(this.toCanvasX(x), this.toCanvasY(y));
            isFirstPoint = false;
          } else {
            this.ctx.lineTo(this.toCanvasX(x), this.toCanvasY(y));
          }
        }
      }
      
      this.ctx.stroke();
    }
    
    drawSpecialPoints() {
      // Get control values for the calculator functions
      const params = this.controls.map(c => c.value);
      
      // Draw each special point
      this.specialPoints.forEach((point) => {
        const result = point.calculator(...params);
        
        // Skip if no point to draw
        if (!result) return;
        
        // Handle array of points or single point
        const points = Array.isArray(result) ? result : [result];
        
        points.forEach(pt => {
          if (pt && typeof pt.x === 'number' && typeof pt.y === 'number') {
            // Only draw if point is within bounds
            if (pt.x >= this.options.xMin && pt.x <= this.options.xMax &&
                pt.y >= this.options.yMin && pt.y <= this.options.yMax) {
              this.ctx.fillStyle = point.color || '#e74c3c';
              this.ctx.beginPath();
              this.ctx.arc(this.toCanvasX(pt.x), this.toCanvasY(pt.y), 5, 0, 2 * Math.PI);
              this.ctx.fill();
            }
          }
        });
      });
    }
  
    updateGraph() {
      // Clear canvas
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
      
      // Draw grid
      this.drawGrid();
      
      // Draw function
      this.drawFunction();
      
      // Draw special points
      this.drawSpecialPoints();
    }
  }
  
  // Export function to create a function explorer
  function createFunctionExplorer(containerId, options) {
    return new MathExplorer(containerId, options);
  }