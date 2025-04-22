/**
 * MathExplorer - Base Visualization Framework
 * 
 * This core module provides the foundation for all interactive mathematics
 * visualizations throughout the curriculum. It handles canvas setup, coordinate 
 * systems, interaction elements, and consistent styling.
 */

class MathExplorer {
    /**
     * Create a new math visualization environment
     * @param {Object} config - Configuration settings
     * @param {string} config.containerId - ID of container element
     * @param {Object} config.theme - Theme settings (optional)
     * @param {Object} config.dimensions - Canvas dimensions (optional)
     * @param {Object} config.range - Mathematical coordinate range (optional)
     * @param {boolean} config.showGrid - Whether to show grid (optional, default true)
     * @param {boolean} config.showAxes - Whether to show axes (optional, default true)
     * @param {Object} config.controls - Control panel settings (optional)
     */
    constructor(config) {
      // Default configuration
      this.config = {
        containerId: 'math-explorer',
        theme: MathExplorer.themes.light,
        dimensions: { width: 600, height: 400 },
        range: { xMin: -10, xMax: 10, yMin: -10, yMax: 10 },
        showGrid: true,
        showAxes: true,
        gridSpacing: 1,
        padding: 30,
        maxMajorTicks: 4,  // Maximum number of major ticks on each axis
        controls: { position: 'left', width: 200 },
        ...config
      };
  
      // Container setup
      this.container = document.getElementById(this.config.containerId);
      if (!this.container) {
        throw new Error(`Container with ID "${this.config.containerId}" not found`);
      }
      this.container.classList.add('math-explorer-container');
      this.applyContainerStyles();
  
      // Create main display areas
      this.createLayout();
  
      // Set up canvas
      this.setupCanvas();
  
      this.boundResizeCanvas = this.resizeCanvas.bind(this);

      // Set up event handlers
      this.setupEventHandlers();
  
      // Initialize storage for visualization elements
      this.elements = [];

      // Initial render
      this.render();
    }
  
    /**
     * Apply CSS styles to container
     */
    applyContainerStyles() {
      this.container.style.fontFamily = this.config.theme.fontFamily;
      this.container.style.color = this.config.theme.textColor;
      this.container.style.backgroundColor = this.config.theme.backgroundColor;
      this.container.style.border = `1px solid ${this.config.theme.borderColor}`;
      this.container.style.borderRadius = '5px';
      this.container.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)';
      this.container.style.overflow = 'hidden';
      this.container.style.display = 'flex';
      this.container.style.flexWrap = 'wrap';
      this.container.style.maxWidth = '100%';
    }
  
    /**
     * Create the main layout areas
     */
    createLayout() {
      // Create controls area if needed
      if (this.config.controls) {
        this.controlsArea = document.createElement('div');
        this.controlsArea.classList.add('math-explorer-controls');
        this.controlsArea.style.width = `${this.config.controls.width}px`;
        this.controlsArea.style.padding = '15px';
        this.controlsArea.style.boxSizing = 'border-box';
        this.controlsArea.style.borderRight = `1px solid ${this.config.theme.borderColor}`;
        this.container.appendChild(this.controlsArea);
      }
  
      // Create canvas area
      this.canvasArea = document.createElement('div');
      this.canvasArea.classList.add('math-explorer-canvas-area');
      this.canvasArea.style.flex = '1';
      this.canvasArea.style.minWidth = '300px';
      //this.canvasArea.style.height = `${this.config.dimensions.height}px`;
      this.canvasArea.style.height = '100%'; // Make it responsive
      this.canvasArea.style.position = 'relative';
      this.container.appendChild(this.canvasArea);
  
      // Create info panel if needed
      if (this.config.infoPanel) {
        this.infoPanel = document.createElement('div');
        this.infoPanel.classList.add('math-explorer-info-panel');
        this.infoPanel.style.padding = '15px';
        this.infoPanel.style.backgroundColor = this.config.theme.infoPanelBackground;
        this.infoPanel.style.borderTop = `1px solid ${this.config.theme.borderColor}`;
        this.infoPanel.style.width = '100%';
        this.container.appendChild(this.infoPanel);
      }
    }
  
    /**
     * Set up the canvas element
     */
    setupCanvas() {
      this.canvas = document.createElement('canvas');
      this.canvas.classList.add('math-explorer-canvas');
      this.canvas.style.width = '100%';
      this.canvas.style.height = '100%';
      this.canvas.style.display = 'block';
      this.canvasArea.appendChild(this.canvas);
  
      // Get context
      this.ctx = this.canvas.getContext('2d');
  
      // Make canvas responsive
      this.resizeCanvas();
    }
  
    /**
     * Resize canvas to match display size
     */
    resizeCanvas() {
      // Make sure we have the correct context
      const self = this;
      
      // Get the actual display dimensions
      const rect = this.canvasArea.getBoundingClientRect();
      
      // Handle case where canvas is not visible yet
      if (rect.width === 0 || rect.height === 0) {
        // Try again soon with a longer delay
        setTimeout(() => this.boundResizeCanvas(), 200);
        return;
      }
      
      const dpr = window.devicePixelRatio || 1;
      
      // Store previous dimensions for comparison
      const prevWidth = this.canvas.width;
      const prevHeight = this.canvas.height;
      
      // Update the canvas size to match its container
      const displayWidth = Math.floor(rect.width);
      const displayHeight = Math.floor(rect.height);
      
      // Only update if dimensions actually changed
      if (this.canvas.width !== displayWidth * dpr || this.canvas.height !== displayHeight * dpr) {
        console.log(`Resizing canvas: ${displayWidth}x${displayHeight}`);
        
        // Update internal config first
        this.config.canvasWidth = displayWidth;
        this.config.canvasHeight = displayHeight;
        
        // Set the canvas dimensions with device pixel ratio for sharpness
        this.canvas.width = displayWidth * dpr;
        this.canvas.height = displayHeight * dpr;
        
        // Set CSS size
        this.canvas.style.width = `${displayWidth}px`;
        this.canvas.style.height = `${displayHeight}px`;
        
        // Reset transform and scale context for high DPI
        this.ctx.setTransform(1, 0, 0, 1, 0, 0);
        this.ctx.scale(dpr, dpr);
        
        // Store dimensions for future comparison
        this._lastWidth = displayWidth;
        this._lastHeight = displayHeight;
        
        // Force a full redraw - Delay slightly to ensure all DOM updates are processed
        setTimeout(() => {
          this.render();
        }, 50);
      }
    }
      
  
    /**
     * Set up event handlers
     */
    setupEventHandlers() {
      // Handle window resize
      window.addEventListener('resize', this.boundResizeCanvas);
  
      // Track mouse position
      this.mousePosition = { x: 0, y: 0 };
      this.canvas.addEventListener('mousemove', (e) => {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        this.mousePosition = { x, y };
        
        // Convert to math coordinates
        this.mathMousePosition = {
          x: this.toMathX(x),
          y: this.toMathY(y)
        };
  
        // Trigger mousemove event for interactive elements
        this.handleInteraction('mousemove');
        
        // Optional: show coordinates in info panel
        if (this.infoPanel && this.config.showCoordinates) {
          this.updateInfoPanel();
        }
      });
  
      // Handle click events
      this.canvas.addEventListener('click', (e) => {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        // Trigger click event for interactive elements
        this.handleInteraction('click', { x, y });
      });

      // Add a MutationObserver to watch for changes in the container size
      if (window.MutationObserver) {
        this.containerObserver = new MutationObserver(() => {
        // If the container's size might have changed, trigger a resize
        this.boundResizeCanvas();
        });
        
        this.containerObserver.observe(this.container, {
        attributes: true,
        attributeFilter: ['style', 'class']
        });
      }
      
      // For container-parent size changes that might not trigger window resize
      // or direct style mutations
      this.resizeInterval = setInterval(() => {
        const currentWidth = this.canvas.clientWidth;
        const currentHeight = this.canvas.clientHeight;
        
        if (currentWidth !== this._lastWidth || currentHeight !== this._lastHeight) {
        this._lastWidth = currentWidth;
        this._lastHeight = currentHeight;
        this.boundResizeCanvas();
        }
      }, 250); // Check every 250ms
    }
  
    /**
     * Handle interaction events for interactive elements
     * @param {string} eventType - Type of event
     * @param {Object} position - Position of event
     */
    handleInteraction(eventType, position = this.mousePosition) {
      // Implementation will depend on specific interaction needs
      // Will be extended in specialized visualization modules
    }
  
    /**
     * Add a control element to the control panel
     * @param {string} type - Type of control ('slider', 'button', 'checkbox', etc.)
     * @param {Object} options - Options for the control
     * @returns {HTMLElement} The created control element
     */
    addControl(type, options) {
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
        
        // For sliders, add value display
        if (type === 'slider' && options.showValue !== false) {
          const valueSpan = document.createElement('span');
          valueSpan.id = `${options.id}-value-display`;
          valueSpan.textContent = options.value || options.min || 0;
          valueSpan.style.float = 'right';
          label.appendChild(valueSpan);
        }
        
        controlGroup.appendChild(label);
      }
  
      // Create the control element
      let control;
      
      switch (type) {
        case 'slider':
          control = this.createSlider(options);
          break;
        case 'button':
          control = this.createButton(options);
          break;
        case 'checkbox':
          control = this.createCheckbox(options);
          break;
        case 'dropdown':
          control = this.createDropdown(options);
          break;
        case 'radio':
          control = this.createRadioGroup(options);
          break;
        case 'colorPicker':
          control = this.createColorPicker(options);
          break;
        default:
          throw new Error(`Unsupported control type: ${type}`);
      }
      
      controlGroup.appendChild(control);
      this.controlsArea.appendChild(controlGroup);
      
      return control;
    }
  
    /**
     * Create a slider control
     * @param {Object} options - Slider options
     * @returns {HTMLInputElement} The slider element
     */
    createSlider(options) {
      const slider = document.createElement('input');
      slider.type = 'range';
      slider.id = options.id;
      slider.min = options.min || 0;
      slider.max = options.max || 100;
      slider.step = options.step || 1;
      slider.value = options.value || options.min || 0;
      slider.style.width = '100%';
      
      // Add change event
      if (options.onChange) {
        slider.addEventListener('input', () => {
          // Update value display if it exists
          const valueDisplay = document.getElementById(`${options.id}-value-display`);
          if (valueDisplay) {
            valueDisplay.textContent = parseFloat(slider.value).toFixed(
              options.precision !== undefined ? options.precision : 1
            );
          }
          
          options.onChange(parseFloat(slider.value));
          this.render();
        });
      }
      
      return slider;
    }
  
    /**
     * Create a button control
     * @param {Object} options - Button options
     * @returns {HTMLButtonElement} The button element
     */
    createButton(options) {
      const button = document.createElement('button');
      button.id = options.id;
      button.textContent = options.text || 'Button';
      button.style.padding = '8px 12px';
      button.style.backgroundColor = this.config.theme.buttonColor;
      button.style.color = this.config.theme.buttonTextColor;
      button.style.border = 'none';
      button.style.borderRadius = '4px';
      button.style.cursor = 'pointer';
      button.style.width = options.fullWidth ? '100%' : 'auto';
      
      if (options.onClick) {
        button.addEventListener('click', options.onClick);
      }
      
      return button;
    }
  
    /**
     * Create a checkbox control
     * @param {Object} options - Checkbox options
     * @returns {HTMLDivElement} Container with the checkbox
     */
    createCheckbox(options) {
      const container = document.createElement('div');
      
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.id = options.id;
      checkbox.checked = options.checked || false;
      
      const label = document.createElement('label');
      label.htmlFor = options.id;
      label.textContent = options.text || '';
      label.style.marginLeft = '5px';
      
      container.appendChild(checkbox);
      container.appendChild(label);
      
      if (options.onChange) {
        checkbox.addEventListener('change', () => {
          options.onChange(checkbox.checked);
          this.render();
        });
      }
      
      return container;
    }
  
    /**
     * Create a dropdown control
     * @param {Object} options - Dropdown options
     * @returns {HTMLSelectElement} The select element
     */
    createDropdown(options) {
      const select = document.createElement('select');
      select.id = options.id;
      select.style.width = '100%';
      select.style.padding = '5px';
      
      if (options.options) {
        options.options.forEach(opt => {
          const option = document.createElement('option');
          option.value = opt.value;
          option.textContent = opt.text;
          select.appendChild(option);
        });
      }
      
      if (options.value) {
        select.value = options.value;
      }
      
      if (options.onChange) {
        select.addEventListener('change', () => {
          options.onChange(select.value);
          this.render();
        });
      }
      
      return select;
    }
  
    /**
     * Create a radio button group
     * @param {Object} options - Radio group options
     * @returns {HTMLDivElement} Container with radio buttons
     */
    createRadioGroup(options) {
      const container = document.createElement('div');
      
      if (options.options) {
        options.options.forEach((opt, index) => {
          const radioContainer = document.createElement('div');
          radioContainer.style.marginBottom = '5px';
          
          const radio = document.createElement('input');
          radio.type = 'radio';
          radio.id = `${options.id}-${index}`;
          radio.name = options.id;
          radio.value = opt.value;
          radio.checked = opt.value === options.value;
          
          const label = document.createElement('label');
          label.htmlFor = `${options.id}-${index}`;
          label.textContent = opt.text;
          label.style.marginLeft = '5px';
          
          radioContainer.appendChild(radio);
          radioContainer.appendChild(label);
          container.appendChild(radioContainer);
          
          if (options.onChange) {
            radio.addEventListener('change', () => {
              if (radio.checked) {
                options.onChange(radio.value);
                this.render();
              }
            });
          }
        });
      }
      
      return container;
    }
  
    /**
     * Create a color picker control
     * @param {Object} options - Color picker options
     * @returns {HTMLInputElement} The color input element
     */
    createColorPicker(options) {
      const colorPicker = document.createElement('input');
      colorPicker.type = 'color';
      colorPicker.id = options.id;
      colorPicker.value = options.value || '#000000';
      
      if (options.onChange) {
        colorPicker.addEventListener('input', () => {
          options.onChange(colorPicker.value);
          this.render();
        });
      }
      
      return colorPicker;
    }
  
    /**
     * Add information to the info panel
     * @param {string} id - ID for the info element
     * @param {string} label - Label text
     * @param {string} value - Initial value
     * @returns {Object} Object with update method
     */
    addInfo(id, label, value) {
      if (!this.infoPanel) {
        throw new Error('Info panel not enabled in configuration');
      }
      
      const infoContainer = document.createElement('div');
      infoContainer.style.marginBottom = '10px';
      infoContainer.id = id;
      
      const infoLabel = document.createElement('span');
      infoLabel.textContent = `${label}: `;
      infoLabel.style.fontWeight = 'bold';
      
      const infoValue = document.createElement('span');
      infoValue.textContent = value;
      
      infoContainer.appendChild(infoLabel);
      infoContainer.appendChild(infoValue);
      this.infoPanel.appendChild(infoContainer);
      
      return {
        update: (newValue) => {
          infoValue.textContent = newValue;
        }
      };
    }
  
    /**
     * Update all info in the info panel
     */
    updateInfoPanel() {
      // This will be implemented in specialized visualizations
      // Default implementation just shows mouse coordinates
      if (this.mathMousePosition && this.config.showCoordinates) {
        const xText = this.mathMousePosition.x.toFixed(2);
        const yText = this.mathMousePosition.y.toFixed(2);
        
        if (!this.coordsInfo) {
          this.coordsInfo = this.addInfo('coords-info', 'Coordinates', `(${xText}, ${yText})`);
        } else {
          this.coordsInfo.update(`(${xText}, ${yText})`);
        }
      }
    }
  
    /**
     * Convert from canvas X coordinate to math X coordinate
     * @param {number} canvasX - X coordinate in canvas space
     * @returns {number} X coordinate in math space
     */
    toMathX(canvasX) {
      const { xMin, xMax } = this.config.range;
      const { padding } = this.config;
      return xMin + ((canvasX - padding) / (this.canvas.width - 2 * padding)) * (xMax - xMin);
    }
  
    /**
     * Convert from canvas Y coordinate to math Y coordinate
     * @param {number} canvasY - Y coordinate in canvas space
     * @returns {number} Y coordinate in math space
     */
    toMathY(canvasY) {
      const { yMin, yMax } = this.config.range;
      const { padding } = this.config;
      return yMax - ((canvasY - padding) / (this.canvas.height - 2 * padding)) * (yMax - yMin);
    }
  
    /**
     * Convert from math X coordinate to canvas X coordinate
     * @param {number} mathX - X coordinate in math space
     * @returns {number} X coordinate in canvas space
     */
    toCanvasX(mathX) {
        const { xMin, xMax } = this.config.range;
        const { padding, canvasWidth } = this.config;
        return ((mathX - xMin) / (xMax - xMin)) * (canvasWidth - 2 * padding) + padding;
    }
  
    /**
     * Convert from math Y coordinate to canvas Y coordinate
     * @param {number} mathY - Y coordinate in math space
     * @returns {number} Y coordinate in canvas space
     */
    toCanvasY(mathY) {
        const { yMin, yMax } = this.config.range;
        const { padding, canvasHeight } = this.config;
        return canvasHeight - (((mathY - yMin) / (yMax - yMin)) * (canvasHeight - 2 * padding) + padding);
    }
  
    /**
     * Calculate appropriate tick spacing for the current range
     * @param {number} min - Minimum value of the range
     * @param {number} max - Maximum value of the range
     * @returns {number} Appropriate tick spacing
     */
    calculateTickSpacing(min, max) {
      const range = max - min;
      const maxTicks = this.config.maxMajorTicks || 8;
      const targetSpacing = range / maxTicks;
      
      // Find the closest "nice" spacing value
      // Nice values follow a 1-2-5 pattern (e.g., 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50...)
      
      // Get the magnitude (power of 10) close to the target spacing
      const magnitude = Math.pow(10, Math.floor(Math.log10(targetSpacing)));
      
      // Determine which nice value is closest to the target spacing
      const normalized = targetSpacing / magnitude; // This will be between 1 and 10
      
      let niceSpacing;
      if (normalized < 1.5) {
          niceSpacing = 1;
      } else if (normalized < 3.5) {
          niceSpacing = 2;
      } else if (normalized < 7.5) {
          niceSpacing = 5;
      } else {
          niceSpacing = 10;
      }
      
      return niceSpacing * magnitude;
    }
  
    /**
     * Calculate appropriate minor tick spacing based on major spacing
     * @param {number} majorSpacing - Major tick spacing
     * @returns {number} Minor tick spacing
     */
    calculateMinorTickSpacing(majorSpacing) {
      // Common minor tick spacings based on major spacing
      if (majorSpacing === 0) return 0.5; // Failsafe
      
      // Determine the power of 10 closest to the major spacing
      const magnitude = Math.pow(10, Math.floor(Math.log10(majorSpacing)));
      
      // Calculate normalized major spacing (between 1 and 10)
      const normalized = majorSpacing / magnitude;
      
      // Set minor spacing based on normalized major spacing
      if (normalized === 1) return magnitude / 5;
      if (normalized === 2) return magnitude / 2;
      if (normalized === 5) return magnitude;
      if (normalized === 10) return magnitude * 2;
      
      // Fallback: divide major spacing by 5
      return majorSpacing / 5;
    }
  
    /**
     * Draw grid on canvas
     */
    drawGrid() {
      if (!this.config.showGrid) return;
      
      const { xMin, xMax, yMin, yMax } = this.config.range;
      
      // Calculate appropriate grid spacing based on the range
      const xSpacing = this.calculateTickSpacing(xMin, xMax);
      const ySpacing = this.calculateTickSpacing(yMin, yMax);
      
      // Calculate minor grid spacing
      const xMinorSpacing = this.calculateMinorTickSpacing(xSpacing);
      const yMinorSpacing = this.calculateMinorTickSpacing(ySpacing);
      
      // Draw minor grid lines
      this.ctx.strokeStyle = this.config.theme.gridColor;
      this.ctx.globalAlpha = 0.3; // More transparent for minor grid
      this.ctx.lineWidth = 0.5;
      
      // Vertical minor grid lines
      for (let x = Math.ceil(xMin / xMinorSpacing) * xMinorSpacing; x <= xMax; x += xMinorSpacing) {
        // Skip if this is a major grid line
        if (Math.abs(x % xSpacing) < xMinorSpacing / 2) continue;
        
        this.ctx.beginPath();
        this.ctx.moveTo(this.toCanvasX(x), 0);
        this.ctx.lineTo(this.toCanvasX(x), this.canvas.height);
        this.ctx.stroke();
      }
      
      // Horizontal minor grid lines
      for (let y = Math.ceil(yMin / yMinorSpacing) * yMinorSpacing; y <= yMax; y += yMinorSpacing) {
        // Skip if this is a major grid line
        if (Math.abs(y % ySpacing) < yMinorSpacing / 2) continue;
        
        this.ctx.beginPath();
        this.ctx.moveTo(0, this.toCanvasY(y));
        this.ctx.lineTo(this.canvas.width, this.toCanvasY(y));
        this.ctx.stroke();
      }
      
      // Draw major grid lines
      this.ctx.globalAlpha = 0.6; // Less transparent for major grid
      this.ctx.lineWidth = 1;
      
      // Vertical major grid lines
      for (let x = Math.ceil(xMin / xSpacing) * xSpacing; x <= xMax; x += xSpacing) {
        this.ctx.beginPath();
        this.ctx.moveTo(this.toCanvasX(x), 0);
        this.ctx.lineTo(this.toCanvasX(x), this.canvas.height);
        this.ctx.stroke();
      }
      
      // Horizontal major grid lines
      for (let y = Math.ceil(yMin / ySpacing) * ySpacing; y <= yMax; y += ySpacing) {
        this.ctx.beginPath();
        this.ctx.moveTo(0, this.toCanvasY(y));
        this.ctx.lineTo(this.canvas.width, this.toCanvasY(y));
        this.ctx.stroke();
      }
      
      // Reset alpha
      this.ctx.globalAlpha = 1.0;
    }
  
    /**
     * Draw coordinate axes
     */
    drawAxes() {
      if (!this.config.showAxes) return;
      
      const { xMin, xMax, yMin, yMax } = this.config.range;
      
      this.ctx.strokeStyle = this.config.theme.axisColor;
      this.ctx.lineWidth = 2;
      
      // X-axis
      this.ctx.beginPath();
      this.ctx.moveTo(this.toCanvasX(xMin), this.toCanvasY(0));
      this.ctx.lineTo(this.toCanvasX(xMax), this.toCanvasY(0));
      this.ctx.stroke();
      
      // Y-axis
      this.ctx.beginPath();
      this.ctx.moveTo(this.toCanvasX(0), this.toCanvasY(yMin));
      this.ctx.lineTo(this.toCanvasX(0), this.toCanvasY(yMax));
      this.ctx.stroke();
      
      // Draw axis labels
      this.drawAxisLabels();
    }
  
    /**
     * Draw labels on axes
     */
    drawAxisLabels() {
        const { xMin, xMax, yMin, yMax } = this.config.range;
        
        // Calculate appropriate tick spacing
        const xSpacing = this.calculateTickSpacing(xMin, xMax);
        const ySpacing = this.calculateTickSpacing(yMin, yMax);
        
        // Increase font size and use a better font
        this.ctx.fillStyle = this.config.theme.textColor;
        this.ctx.font = `bold 15px ${this.config.theme.fontFamily}`; // Increased from 12px to 14px and added bold
        
        // X-axis labels
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'top';
        
        // Apply anti-aliasing for better text resolution
        //this.ctx.imageSmoothingEnabled = true;
        //this.ctx.imageSmoothingQuality = 'high';
        
        for (let x = Math.ceil(xMin / xSpacing) * xSpacing; x <= xMax; x += xSpacing) {
          // Skip very small values near zero (to avoid showing both 0 and -0)
          if (Math.abs(x) < 0.001 * xSpacing) continue;
          
          // Format the label based on the spacing
          let label;
          if (xSpacing >= 1) {
            label = Math.round(x); // Use integers for larger spacings
          } else {
            // Use appropriate decimal places for smaller spacings
            const decimalPlaces = Math.max(0, -Math.floor(Math.log10(xSpacing)));
            label = x.toFixed(decimalPlaces);
          }
          
          // Apply a subtle background to make text more readable
          const textWidth = this.ctx.measureText(label).width;
          const textX = this.toCanvasX(x);
          const textY = this.toCanvasY(0) + 5;
          
          // Add a subtle background for better visibility
          this.ctx.fillStyle = 'rgba(255,255,255,1)';
          this.ctx.fillRect(textX - textWidth / 2 - 2, textY - 2, textWidth + 4, 18);
          
          // Draw text with increased clarity
          this.ctx.fillStyle = '#000';
          this.ctx.fillText(
            label,
            textX,
            textY
          );
        }
        
        // Always show origin (0)
        if (xMin <= 0 && xMax >= 0) {
          const textWidth = this.ctx.measureText('0').width;
          const textX = this.toCanvasX(0);
          const textY = this.toCanvasY(0) + 5;
          
          this.ctx.fillStyle = 'rgba(255,255,255, 1)';
          this.ctx.fillRect(textX - textWidth / 2 - 2, textY - 2, textWidth + 4, 18);
          
          this.ctx.fillStyle = '#000';
          this.ctx.fillText('0', textX, textY);
        }
        
        // Y-axis labels
        this.ctx.textAlign = 'right';
        this.ctx.textBaseline = 'middle';
        
        for (let y = Math.ceil(yMin / ySpacing) * ySpacing; y <= yMax; y += ySpacing) {
          // Skip very small values near zero
          if (Math.abs(y) < 0.001 * ySpacing) continue;
          
          // Format the label based on the spacing
          let label;
          if (ySpacing >= 1) {
            label = Math.round(y); // Use integers for larger spacings
          } else {
            // Use appropriate decimal places for smaller spacings
            const decimalPlaces = Math.max(0, -Math.floor(Math.log10(ySpacing)));
            label = y.toFixed(decimalPlaces);
          }
          
          const textWidth = this.ctx.measureText(label).width;
          const textX = this.toCanvasX(0) - 5;
          const textY = this.toCanvasY(y);
          
          // Add a subtle background for better visibility
          this.ctx.fillStyle = 'rgba(255,255,255, 1)';
          this.ctx.fillRect(textX - textWidth - 2, textY - 9, textWidth + 4, 18);
          
          // Draw text with increased clarity
          this.ctx.fillStyle = '#000';
          this.ctx.fillText(
            label,
            textX,
            textY
          );
        }
        
        // Always show origin (0) unless already shown
        if (yMin <= 0 && yMax >= 0 && !(xMin <= 0 && xMax >= 0)) {
          const textWidth = this.ctx.measureText('0').width;
          const textX = this.toCanvasX(0) - 5;
          const textY = this.toCanvasY(0);
          
          this.ctx.fillStyle = 'rgba(255,255,255,0.7)';
          this.ctx.fillRect(textX - textWidth - 2, textY - 9, textWidth + 4, 18);
          
          this.ctx.fillStyle = '#000';
          this.ctx.fillText('0', textX, textY);
        }
      }
  
    /**
     * Clear the canvas
     */
    clear() {
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }
  
    /**
     * Render the visualization
     */
    render() {
      this.clear();
      this.drawGrid();
      this.drawAxes();
      
      // Render specialized elements
      // This will be extended in derived classes
    }
  
    /**
     * Add a visualization element
     * @param {Object} element - Element to add
     */
    addElement(element) {
      this.elements.push(element);
      this.render();
      return element;
    }
  
    /**
     * Remove a visualization element
     * @param {Object} element - Element to remove
     */
    removeElement(element) {
      const index = this.elements.indexOf(element);
      if (index !== -1) {
        this.elements.splice(index, 1);
        this.render();
      }
    }
  
    /**
     * Set the theme
     * @param {string|Object} theme - Theme name or theme object
     */
    setTheme(theme) {
      if (typeof theme === 'string') {
        if (MathExplorer.themes[theme]) {
          this.config.theme = MathExplorer.themes[theme];
        } else {
          throw new Error(`Theme "${theme}" not found`);
        }
      } else if (typeof theme === 'object') {
        this.config.theme = { ...MathExplorer.themes.light, ...theme };
      }
      
      this.applyContainerStyles();
      this.render();
    }
  
    /**
     * Set the coordinate range
     * @param {Object} range - New coordinate range
     */
    setRange(range) {
      this.config.range = { ...this.config.range, ...range };
      this.render();
    }
  }
  
  /**
   * Predefined themes
   */
  MathExplorer.themes = {
    light: {
      fontFamily: 'Arial, sans-serif',
      backgroundColor: '#ffffff',
      textColor: '#333333',
      gridColor: '#e1e1e1',
      axisColor: '#333333',
      borderColor: '#dddddd',
      buttonColor: '#4a90e2',
      buttonTextColor: '#ffffff',
      highlightColor: '#e74c3c',
      secondaryColor: '#2ecc71',
      tertiaryColor: '#9b59b6',
      infoPanelBackground: '#f8f9fa'
    },
    dark: {
      fontFamily: 'Arial, sans-serif',
      backgroundColor: '#2c3e50',
      textColor: '#ecf0f1',
      gridColor: '#34495e',
      axisColor: '#7f8c8d',
      borderColor: '#1a2530',
      buttonColor: '#3498db',
      buttonTextColor: '#ffffff',
      highlightColor: '#e74c3c',
      secondaryColor: '#2ecc71',
      tertiaryColor: '#9b59b6',
      infoPanelBackground: '#1a2530'
    }
  };
  
  /**
   * Utility functions
   */
  MathExplorer.utils = {
    /**
     * Linear interpolation
     * @param {number} a - First value
     * @param {number} b - Second value
     * @param {number} t - Interpolation factor (0-1)
     * @returns {number} Interpolated value
     */
    lerp: (a, b, t) => a + (b - a) * t,
    
    /**
     * Format number for display
     * @param {number} value - Number to format
     * @param {number} precision - Decimal precision
     * @returns {string} Formatted number
     */
    formatNumber: (value, precision = 2) => {
      return Math.abs(value) < 0.001 ? '0' : value.toFixed(precision);
    },
    
    /**
     * Generate array of evenly spaced numbers
     * @param {number} start - Start value
     * @param {number} end - End value
     * @param {number} count - Number of points
     * @returns {Array} Array of numbers
     */
    linspace: (start, end, count) => {
      const result = [];
      const step = (end - start) / (count - 1);
      for (let i = 0; i < count; i++) {
        result.push(start + i * step);
      }
      return result;
    }
  };
  
  // Export the module
  export default MathExplorer;