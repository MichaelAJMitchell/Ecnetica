/**
 * MathExplorer - Data Visualization Module
 * 
 * An extension of the base MathExplorer framework specialized for statistical 
 * data visualization including histograms, box plots, scatter plots, and more.
 */

import MathExplorer from './base-visualization-framework.js';

class DataVisualizer extends MathExplorer {
  /**
   * Create a new data visualization environment
   * @param {Object} config - Configuration settings
   */
  constructor(config) {
    // Set default config values specific to data visualization
    const dataConfig = {
      // Adjust default range to be more suitable for data visualization
      range: { xMin: 0, xMax: 10, yMin: 0, yMax: 10 },
      // Enable info panel for statistical measures
      infoPanel: true,
      // Data-specific settings
      dataOptions: {
        barWidth: 0.6, // Width of bars as a fraction of available space
        histogramBins: 10, // Default number of bins for histograms
        colors: [], // Custom colors for data series
        boxPlotWhiskerType: 'iqr', // 'iqr' or 'minmax'
        scatterPointSize: 5,
        trendlineEnabled: true,
        animationDuration: 500, // ms
        axisLabels: {
          x: 'x',
          y: 'y'
        }
      },
      ...config
    };
    
    // Call parent constructor
    super(dataConfig);
    
    // Initialize collections for data
    this.datasets = [];
    this.visualizations = [];
    this.currentVisualization = null;
    
    // Set up event handlers for interactivity
    this.setupDataEventHandlers();
  }

  /**
   * Set up additional event handlers for data interactions
   */
  setupDataEventHandlers() {
    // Add hover event for showing data point details
    this.canvas.addEventListener('mousemove', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      // Convert to math coordinates
      const mathX = this.toMathX(x);
      const mathY = this.toMathY(y);
      
      // Check if mouse is over a data point
      if (this.currentVisualization) {
        const hit = this.checkDataPointHit(mathX, mathY);
        if (hit) {
          this.showTooltip(hit, { x, y });
        } else {
          this.hideTooltip();
        }
      }
    });
    
    // Hide tooltip when leaving canvas
    this.canvas.addEventListener('mouseleave', () => {
      this.hideTooltip();
    });
    
    // Click event for selecting data points
    this.canvas.addEventListener('click', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      // Convert to math coordinates
      const mathX = this.toMathX(x);
      const mathY = this.toMathY(y);
      
      // Check if clicked on a data point
      if (this.currentVisualization) {
        const hit = this.checkDataPointHit(mathX, mathY);
        if (hit) {
          this.selectDataPoint(hit);
        } else {
          this.deselectDataPoint();
        }
      }
    });
  }

  /**
   * Check if a point hits any data element
   * @param {number} x - Math X coordinate
   * @param {number} y - Math Y coordinate
   * @returns {Object|null} Hit data or null
   */
  checkDataPointHit(x, y) {
    if (!this.currentVisualization) return null;
    
    switch (this.currentVisualization.type) {
      case 'bar':
        return this.checkBarHit(x, y);
      case 'histogram':
        return this.checkHistogramHit(x, y);
      case 'scatter':
        return this.checkScatterHit(x, y);
      case 'box':
        return this.checkBoxPlotHit(x, y);
      default:
        return null;
    }
  }

  /**
   * Check if a point hits a bar in a bar chart
   * @param {number} x - Math X coordinate
   * @param {number} y - Math Y coordinate
   * @returns {Object|null} Hit data or null
   */
  checkBarHit(x, y) {
    const viz = this.currentVisualization;
    
    // Check each category
    for (let i = 0; i < viz.data.length; i++) {
      const bar = viz.data[i];
      const barX = viz.categoryPositions[i];
      const barWidth = viz.barWidth;
      
      // Check if within the bar's bounds
      if (x >= barX - barWidth / 2 && x <= barX + barWidth / 2 && 
          y >= 0 && y <= bar.value) {
        return {
          type: 'bar',
          index: i,
          category: bar.category,
          value: bar.value,
          x: barX,
          y: bar.value / 2
        };
      }
    }
    
    return null;
  }

  /**
   * Check if a point hits a bin in a histogram
   * @param {number} x - Math X coordinate
   * @param {number} y - Math Y coordinate
   * @returns {Object|null} Hit data or null
   */
  checkHistogramHit(x, y) {
    const viz = this.currentVisualization;
    const bins = viz.bins;
    
    // Check each bin
    for (let i = 0; i < bins.length; i++) {
      const bin = bins[i];
      
      // Check if within the bin's bounds
      if (x >= bin.x0 && x <= bin.x1 && 
          y >= 0 && y <= bin.frequency) {
        return {
          type: 'histogram',
          index: i,
          binStart: bin.x0,
          binEnd: bin.x1,
          frequency: bin.frequency,
          count: bin.count,
          x: (bin.x0 + bin.x1) / 2,
          y: bin.frequency / 2
        };
      }
    }
    
    return null;
  }

  /**
   * Check if a point hits a point in a scatter plot
   * @param {number} x - Math X coordinate
   * @param {number} y - Math Y coordinate
   * @returns {Object|null} Hit data or null
   */
  checkScatterHit(x, y) {
    const viz = this.currentVisualization;
    const pointSize = this.config.dataOptions.scatterPointSize;
    
    // Calculate threshold in math coordinates
    const threshold = pointSize * (this.config.range.xMax - this.config.range.xMin) / 
                      (this.canvas.width - 2 * this.config.padding);
    
    // Check each point
    for (let i = 0; i < viz.data.length; i++) {
      const point = viz.data[i];
      const dist = Math.sqrt(Math.pow(x - point.x, 2) + Math.pow(y - point.y, 2));
      
      if (dist <= threshold) {
        return {
          type: 'point',
          index: i,
          x: point.x,
          y: point.y,
          label: point.label
        };
      }
    }
    
    return null;
  }

  /**
   * Check if a point hits any part of a box plot
   * @param {number} x - Math X coordinate
   * @param {number} y - Math Y coordinate
   * @returns {Object|null} Hit data or null
   */
  checkBoxPlotHit(x, y) {
    const viz = this.currentVisualization;
    const boxPos = viz.position;
    const boxWidth = viz.boxWidth;
    
    // Check if within the overall box plot bounds
    if (x >= boxPos - boxWidth / 2 && x <= boxPos + boxWidth / 2) {
      // Check specific parts of the box plot
      if (y >= viz.q1 && y <= viz.q3) {
        return {
          type: 'boxplot-box',
          x: boxPos,
          y: (viz.q1 + viz.q3) / 2,
          q1: viz.q1,
          q3: viz.q3,
          median: viz.median
        };
      } else if (Math.abs(y - viz.median) <= 0.1) {
        return {
          type: 'boxplot-median',
          x: boxPos,
          y: viz.median,
          value: viz.median
        };
      } else if (y >= viz.min && y <= viz.q1) {
        return {
          type: 'boxplot-whisker',
          x: boxPos,
          y: (viz.min + viz.q1) / 2,
          min: viz.min,
          q1: viz.q1
        };
      } else if (y >= viz.q3 && y <= viz.max) {
        return {
          type: 'boxplot-whisker',
          x: boxPos,
          y: (viz.q3 + viz.max) / 2,
          q3: viz.q3,
          max: viz.max
        };
      }
    }
    
    return null;
  }

  /**
   * Create tooltip element if it doesn't exist
   */
  createTooltip() {
    if (!this.tooltip) {
      this.tooltip = document.createElement('div');
      this.tooltip.classList.add('data-tooltip');
      this.tooltip.style.position = 'absolute';
      this.tooltip.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
      this.tooltip.style.color = 'white';
      this.tooltip.style.padding = '5px 10px';
      this.tooltip.style.borderRadius = '3px';
      this.tooltip.style.fontSize = '12px';
      this.tooltip.style.pointerEvents = 'none';
      this.tooltip.style.zIndex = '1000';
      this.tooltip.style.display = 'none';
      
      this.canvasArea.appendChild(this.tooltip);
    }
  }

  /**
   * Show tooltip with data information
   * @param {Object} hitData - Data about what was hit
   * @param {Object} position - Canvas position {x, y}
   */
  showTooltip(hitData, position) {
    this.createTooltip();
    
    // Format tooltip content based on hit type
    let content = '';
    
    switch (hitData.type) {
      case 'bar':
        content = `<strong>${hitData.category}</strong><br>Value: ${hitData.value.toFixed(2)}`;
        break;
      case 'histogram':
        content = `<strong>Bin ${hitData.index + 1}</strong><br>` +
                  `Range: ${hitData.binStart.toFixed(2)} - ${hitData.binEnd.toFixed(2)}<br>` +
                  `Frequency: ${hitData.frequency.toFixed(2)}<br>` +
                  `Count: ${hitData.count}`;
        break;
      case 'point':
        content = `<strong>${hitData.label || `Point ${hitData.index + 1}`}</strong><br>` +
                  `x: ${hitData.x.toFixed(2)}<br>` +
                  `y: ${hitData.y.toFixed(2)}`;
        break;
      case 'boxplot-box':
        content = `<strong>Interquartile Range</strong><br>` +
                  `Q1: ${hitData.q1.toFixed(2)}<br>` +
                  `Median: ${hitData.median.toFixed(2)}<br>` +
                  `Q3: ${hitData.q3.toFixed(2)}`;
        break;
      case 'boxplot-median':
        content = `<strong>Median</strong><br>` +
                  `Value: ${hitData.value.toFixed(2)}`;
        break;
      case 'boxplot-whisker':
        if (hitData.min !== undefined) {
          content = `<strong>Lower Whisker</strong><br>` +
                    `Min: ${hitData.min.toFixed(2)}<br>` +
                    `Q1: ${hitData.q1.toFixed(2)}`;
        } else {
          content = `<strong>Upper Whisker</strong><br>` +
                    `Q3: ${hitData.q3.toFixed(2)}<br>` +
                    `Max: ${hitData.max.toFixed(2)}`;
        }
        break;
    }
    
    // Set tooltip content and position
    this.tooltip.innerHTML = content;
    this.tooltip.style.display = 'block';
    
    // Position tooltip near the cursor but not directly under it
    const tooltipRect = this.tooltip.getBoundingClientRect();
    const canvasRect = this.canvas.getBoundingClientRect();
    
    let posX = position.x + 10;
    let posY = position.y - tooltipRect.height - 10;
    
    // Adjust if tooltip would go off the canvas
    if (posX + tooltipRect.width > canvasRect.right) {
      posX = position.x - tooltipRect.width - 10;
    }
    
    if (posY < canvasRect.top) {
      posY = position.y + 10;
    }
    
    this.tooltip.style.left = `${posX}px`;
    this.tooltip.style.top = `${posY}px`;
  }

  /**
   * Hide tooltip
   */
  hideTooltip() {
    if (this.tooltip) {
      this.tooltip.style.display = 'none';
    }
  }

  /**
   * Select a data point
   * @param {Object} hitData - Data about what was hit
   */
  selectDataPoint(hitData) {
    if (this.selectedDataPoint) {
      // Deselect previous point if it's different
      if (this.selectedDataPoint.type !== hitData.type ||
          this.selectedDataPoint.index !== hitData.index) {
        this.deselectDataPoint();
      } else {
        // Same point clicked, just deselect
        this.deselectDataPoint();
        return;
      }
    }
    
    // Select new point
    this.selectedDataPoint = hitData;
    
    // Update visualization to show selection
    this.render();
    
    // Update info panel with details about selected point
    this.updateSelectedPointInfo();
  }

  /**
   * Deselect current data point
   */
  deselectDataPoint() {
    if (this.selectedDataPoint) {
      this.selectedDataPoint = null;
      this.render();
      this.updateSelectedPointInfo();
    }
  }

  /**
   * Update info panel with details about selected point
   */
  updateSelectedPointInfo() {
    if (!this.infoPanel) return;
    
    // Clear existing point-specific info
    const standardInfoCount = this.standardInfoElements ? this.standardInfoElements.length : 0;
    while (this.infoPanel.childNodes.length > standardInfoCount) {
      this.infoPanel.removeChild(this.infoPanel.lastChild);
    }
    
    // If no point selected, return
    if (!this.selectedDataPoint) return;
    
    // Add separator
    const separator = document.createElement('hr');
    separator.style.margin = '10px 0';
    separator.style.border = 'none';
    separator.style.borderTop = `1px solid ${this.config.theme.borderColor}`;
    this.infoPanel.appendChild(separator);
    
    // Add title
    const title = document.createElement('h4');
    title.style.margin = '5px 0';
    title.style.fontSize = '14px';
    title.textContent = 'Selected Point';
    this.infoPanel.appendChild(title);
    
    // Add details based on selection type
    const hit = this.selectedDataPoint;
    
    switch (hit.type) {
      case 'bar':
        this.addInfo('selected-category', 'Category', hit.category);
        this.addInfo('selected-value', 'Value', hit.value.toFixed(2));
        break;
      case 'histogram':
        this.addInfo('selected-bin', 'Bin', `${hit.index + 1}`);
        this.addInfo('selected-range', 'Range', `${hit.binStart.toFixed(2)} - ${hit.binEnd.toFixed(2)}`);
        this.addInfo('selected-frequency', 'Frequency', hit.frequency.toFixed(2));
        this.addInfo('selected-count', 'Count', hit.count.toString());
        break;
      case 'point':
        this.addInfo('selected-point', 'Point', hit.label || `Point ${hit.index + 1}`);
        this.addInfo('selected-x', 'X', hit.x.toFixed(2));
        this.addInfo('selected-y', 'Y', hit.y.toFixed(2));
        break;
      case 'boxplot-box':
      case 'boxplot-median':
      case 'boxplot-whisker':
        if (hit.min !== undefined) this.addInfo('selected-min', 'Min', hit.min.toFixed(2));
        if (hit.q1 !== undefined) this.addInfo('selected-q1', 'Q1', hit.q1.toFixed(2));
        if (hit.median !== undefined) this.addInfo('selected-median', 'Median', hit.median.toFixed(2));
        if (hit.q3 !== undefined) this.addInfo('selected-q3', 'Q3', hit.q3.toFixed(2));
        if (hit.max !== undefined) this.addInfo('selected-max', 'Max', hit.max.toFixed(2));
        break;
    }
  }

  /**
   * Add a data series
   * @param {Object} dataset - Dataset object
   * @returns {Object} Added dataset
   */
  addDataset(dataset) {
    const defaultDataset = {
      id: `data-${this.datasets.length + 1}`,
      label: `Series ${this.datasets.length + 1}`,
      color: this.getNextColor(),
      data: []
    };
    
    const newDataset = { ...defaultDataset, ...dataset };
    this.datasets.push(newDataset);
    
    return newDataset;
  }

  /**
   * Get the next color from the color palette
   * @returns {string} Color code
   */
  getNextColor() {
    const defaultColors = [
      '#3498db', // Blue
      '#e74c3c', // Red
      '#2ecc71', // Green
      '#9b59b6', // Purple
      '#f39c12', // Orange
      '#1abc9c', // Turquoise
      '#34495e', // Dark Blue
      '#d35400', // Dark Orange
      '#27ae60', // Dark Green
      '#8e44ad'  // Dark Purple
    ];
    
    const colors = this.config.dataOptions.colors.length > 0 
      ? this.config.dataOptions.colors 
      : defaultColors;
    
    return colors[this.datasets.length % colors.length];
  }

  /**
   * Create a bar chart visualization
   * @param {Array|string} data - Data array or dataset ID
   * @param {Object} options - Visualization options
   * @returns {Object} Visualization object
   */
  createBarChart(data, options = {}) {
    // Get the dataset
    const dataset = typeof data === 'string' 
      ? this.datasets.find(d => d.id === data) 
      : { data };
    
    if (!dataset || !dataset.data || dataset.data.length === 0) {
      console.error('No data available for bar chart');
      return null;
    }
    
    // Set up default options
    const defaultOptions = {
      title: 'Bar Chart',
      barWidth: this.config.dataOptions.barWidth,
      color: dataset.color || this.getNextColor(),
      showValues: true,
      sorted: false,
      ascending: true
    };
    
    const vizOptions = { ...defaultOptions, ...options };
    
    // Process data to ensure it has the right format
    let processedData = [];
    
    // Check if data contains category/value pairs
    if (dataset.data[0] && (dataset.data[0].category !== undefined && dataset.data[0].value !== undefined)) {
      processedData = [...dataset.data];
    }
    // Check if data is an array of values with indices as categories
    else if (Array.isArray(dataset.data)) {
      processedData = dataset.data.map((value, index) => ({
        category: `Category ${index + 1}`,
        value: typeof value === 'number' ? value : 0
      }));
    }
    
    // Sort data if requested
    if (vizOptions.sorted) {
      processedData.sort((a, b) => {
        return vizOptions.ascending ? a.value - b.value : b.value - a.value;
      });
    }
    
    // Calculate positions and dimensions
    const numBars = processedData.length;
    const availableWidth = this.config.range.xMax - this.config.range.xMin;
    const barWidth = (availableWidth / numBars) * vizOptions.barWidth;
    
    // Find max value for scaling
    const maxValue = Math.max(...processedData.map(d => d.value));
    
    // Adjust y-axis range if needed
    if (maxValue > this.config.range.yMax) {
      this.setRange({ yMax: maxValue * 1.1 }); // Add 10% padding
    }
    
    // Calculate category positions
    const categoryWidth = availableWidth / numBars;
    const categoryPositions = processedData.map((_, i) => 
      this.config.range.xMin + (i + 0.5) * categoryWidth
    );
    
    // Create the visualization object
    const visualization = {
      type: 'bar',
      data: processedData,
      options: vizOptions,
      barWidth,
      categoryWidth,
      categoryPositions,
      categoryLabels: processedData.map(d => d.category)
    };
    
    this.visualizations.push(visualization);
    this.currentVisualization = visualization;
    
    // Update the info panel
    this.updateStatistics();
    
    // Render the visualization
    this.render();
    
    return visualization;
  }

  /**
   * Create a histogram visualization
   * @param {Array|string} data - Data array or dataset ID
   * @param {Object} options - Visualization options
   * @returns {Object} Visualization object
   */
  createHistogram(data, options = {}) {
    // Get the dataset
    const dataset = typeof data === 'string' 
      ? this.datasets.find(d => d.id === data) 
      : { data };
    
    if (!dataset || !dataset.data || dataset.data.length === 0) {
      console.error('No data available for histogram');
      return null;
    }
    
    // Set up default options
    const defaultOptions = {
      title: 'Histogram',
      bins: this.config.dataOptions.histogramBins,
      color: dataset.color || this.getNextColor(),
      showFrequency: true,
      normalized: false
    };
    
    const vizOptions = { ...defaultOptions, ...options };
    
    // Process data to ensure it's an array of numbers
    let processedData = [];
    
    if (Array.isArray(dataset.data)) {
      // If data is an array of objects with a value property
      if (typeof dataset.data[0] === 'object' && dataset.data[0].value !== undefined) {
        processedData = dataset.data.map(d => d.value).filter(v => typeof v === 'number');
      }
      // If data is an array of numbers
      else {
        processedData = dataset.data.filter(v => typeof v === 'number');
      }
    }
    
    if (processedData.length === 0) {
      console.error('No numeric data available for histogram');
      return null;
    }
    
    // Calculate bins
    const minValue = Math.min(...processedData);
    const maxValue = Math.max(...processedData);
    const range = maxValue - minValue;
    const binWidth = range / vizOptions.bins;
    
    const bins = [];
    for (let i = 0; i < vizOptions.bins; i++) {
      const binStart = minValue + i * binWidth;
      const binEnd = minValue + (i + 1) * binWidth;
      bins.push({
        x0: binStart,
        x1: binEnd,
        count: 0,
        frequency: 0
      });
    }
    
    // Count data points in each bin
    processedData.forEach(value => {
      if (value === maxValue) {
        // Handle edge case for max value
        bins[bins.length - 1].count++;
      } else {
        const binIndex = Math.floor((value - minValue) / binWidth);
        if (binIndex >= 0 && binIndex < bins.length) {
          bins[binIndex].count++;
        }
      }
    });
    
    // Calculate frequencies
    const totalCount = processedData.length;
    bins.forEach(bin => {
      bin.frequency = vizOptions.normalized 
        ? bin.count / totalCount / binWidth 
        : bin.count / binWidth;
    });
    
    // Find max frequency for scaling
    const maxFrequency = Math.max(...bins.map(b => b.frequency));
    
    // Adjust y-axis range if needed
    if (maxFrequency > this.config.range.yMax) {
      this.setRange({ yMax: maxFrequency * 1.1 }); // Add 10% padding
    }
    
    // Adjust x-axis range to match data
    this.setRange({ 
      xMin: minValue - binWidth / 2,
      xMax: maxValue + binWidth / 2
    });
    
    // Create the visualization object
    const visualization = {
      type: 'histogram',
      data: processedData,
      bins,
      options: vizOptions,
      minValue,
      maxValue,
      binWidth
    };
    
    this.visualizations.push(visualization);
    this.currentVisualization = visualization;
    
    // Update the info panel
    this.updateStatistics();
    
    // Render the visualization
    this.render();
    
    return visualization;
  }

  /**
   * Create a scatter plot visualization
   * @param {Array|string} data - Data array or dataset ID
   * @param {Object} options - Visualization options
   * @returns {Object} Visualization object
   */
  createScatterPlot(data, options = {}) {
    // Get the dataset
    const dataset = typeof data === 'string' 
      ? this.datasets.find(d => d.id === data) 
      : { data };
    
    if (!dataset || !dataset.data || dataset.data.length === 0) {
      console.error('No data available for scatter plot');
      return null;
    }
    
    // Set up default options
    const defaultOptions = {
      title: 'Scatter Plot',
      color: dataset.color || this.getNextColor(),
      pointSize: this.config.dataOptions.scatterPointSize,
      showTrendline: this.config.dataOptions.trendlineEnabled,
      trendlineColor: '#ff0000',
      showCorrelation: true,
      showLabels: false
    };
    
    const vizOptions = { ...defaultOptions, ...options };
    
    // Process data to ensure it has the right format
    let processedData = [];
    
    // Check if data contains x/y pairs
    if (dataset.data[0] && (dataset.data[0].x !== undefined && dataset.data[0].y !== undefined)) {
      processedData = [...dataset.data];
    }
    // Check if data is an array of arrays [x, y]
    else if (Array.isArray(dataset.data) && Array.isArray(dataset.data[0]) && dataset.data[0].length >= 2) {
      processedData = dataset.data.map(point => ({
        x: point[0],
        y: point[1],
        label: point[2] || ''
      }));
    }
    
    if (processedData.length === 0) {
      console.error('Data format not suitable for scatter plot');
      return null;
    }
    
    // Find min/max values for scaling
    const xValues = processedData.map(d => d.x);
    const yValues = processedData.map(d => d.y);
    
    const minX = Math.min(...xValues);
    const maxX = Math.max(...xValues);
    const minY = Math.min(...yValues);
    const maxY = Math.max(...yValues);
    
    // Add padding to ranges
    const xPadding = (maxX - minX) * 0.1;
    const yPadding = (maxY - minY) * 0.1;
    
    // Adjust axis ranges if needed
    this.setRange({
      xMin: minX - xPadding,
      xMax: maxX + xPadding,
      yMin: Math.min(0, minY - yPadding),
      yMax: maxY + yPadding
    });
    
    // Calculate trend line if requested
    let trendline = null;
    let correlation = null;
    
    if (vizOptions.showTrendline) {
      const result = this.calculateLinearRegression(xValues, yValues);
      trendline = result.line;
      correlation = result.correlation;
    }
    
    // Create the visualization object
    const visualization = {
      type: 'scatter',
      data: processedData,
      options: vizOptions,
      trendline,
      correlation
    };
    
    this.visualizations.push(visualization);
    this.currentVisualization = visualization;
    
    // Update the info panel
    this.updateStatistics();
    
    // Render the visualization
    this.render();
    
    return visualization;
  }

  /**
   * Create a box plot visualization
   * @param {Array|string} data - Data array or dataset ID
   * @param {Object} options - Visualization options
   * @returns {Object} Visualization object
   */
  createBoxPlot(data, options = {}) {
    // Get the dataset
    const dataset = typeof data === 'string' 
      ? this.datasets.find(d => d.id === data) 
      : { data };
    
    if (!dataset || !dataset.data || dataset.data.length === 0) {
      console.error('No data available for box plot');
      return null;
    }
    
    // Set up default options
    const defaultOptions = {
      title: 'Box Plot',
      color: dataset.color || this.getNextColor(),
      boxWidth: 1,
      position: 5, // X-position of the box plot
      whiskerType: this.config.dataOptions.boxPlotWhiskerType, // 'iqr' or 'minmax'
      showOutliers: true,
      showMean: true
    };
    
    const vizOptions = { ...defaultOptions, ...options };
    
    // Process data to ensure it's an array of numbers
    let processedData = [];
    
    if (Array.isArray(dataset.data)) {
      // If data is an array of objects with a value property
      if (typeof dataset.data[0] === 'object' && dataset.data[0].value !== undefined) {
        processedData = dataset.data.map(d => d.value).filter(v => typeof v === 'number');
      }
      // If data is an array of numbers
      else {
        processedData = dataset.data.filter(v => typeof v === 'number');
      }
    }
    
    if (processedData.length === 0) {
      console.error('No numeric data available for box plot');
      return null;
    }
    
    // Sort data for percentile calculations
    processedData.sort((a, b) => a - b);
    
    // Calculate statistics
    const min = processedData[0];
    const max = processedData[processedData.length - 1];
    const q1 = this.calculatePercentile(processedData, 25);
    const median = this.calculatePercentile(processedData, 50);
    const q3 = this.calculatePercentile(processedData, 75);
    const iqr = q3 - q1;
    
    // Calculate whiskers based on type
    let whiskerMin, whiskerMax;
    let outliers = [];
    
    if (vizOptions.whiskerType === 'iqr') {
      // Use IQR method: whiskers at max 1.5*IQR from the box
      const lowerFence = q1 - 1.5 * iqr;
      const upperFence = q3 + 1.5 * iqr;
      
      // Find nearest data points within the fences
      whiskerMin = processedData.find(d => d >= lowerFence) || min;
      whiskerMax = [...processedData].reverse().find(d => d <= upperFence) || max;
      
      // Identify outliers
      if (vizOptions.showOutliers) {
        outliers = processedData.filter(d => d < lowerFence || d > upperFence);
      }
    } else {
      // Use min/max method
      whiskerMin = min;
      whiskerMax = max;
    }
    
    // Calculate mean if needed
    let mean = null;
    if (vizOptions.showMean) {
      mean = processedData.reduce((sum, value) => sum + value, 0) / processedData.length;
    }
    
    // Adjust y-axis range to fit the box plot
    const dataRange = Math.max(max, whiskerMax) - Math.min(min, whiskerMin);
    this.setRange({
      yMin: Math.min(min, whiskerMin) - dataRange * 0.1,
      yMax: Math.max(max, whiskerMax) + dataRange * 0.1
    });
    
    // Create the visualization object
    const visualization = {
      type: 'box',
      data: processedData,
      options: vizOptions,
      min: whiskerMin,
      q1,
      median,
      q3,
      max: whiskerMax,
      mean,
      outliers,
      position: vizOptions.position,
      boxWidth: vizOptions.boxWidth
    };
    
    this.visualizations.push(visualization);
    this.currentVisualization = visualization;
    
    // Update the info panel
    this.updateStatistics();
    
    // Render the visualization
    this.render();
    
    return visualization;
  }

  /**
   * Calculate the percentile of a sorted array
   * @param {Array} sortedData - Sorted array of numbers
   * @param {number} percentile - Percentile (0-100)
   * @returns {number} Percentile value
   */
  calculatePercentile(sortedData, percentile) {
    if (sortedData.length === 0) return 0;
    
    const index = (percentile / 100) * (sortedData.length - 1);
    const lower = Math.floor(index);
    const upper = Math.ceil(index);
    const weight = index - lower;
    
    if (upper >= sortedData.length) return sortedData[sortedData.length - 1];
    if (lower < 0) return sortedData[0];
    
    if (lower === upper) return sortedData[lower];
    
    return sortedData[lower] * (1 - weight) + sortedData[upper] * weight;
  }

  /**
   * Calculate linear regression line and correlation coefficient
   * @param {Array} xValues - X values
   * @param {Array} yValues - Y values
   * @returns {Object} Regression results
   */
  calculateLinearRegression(xValues, yValues) {
    if (xValues.length !== yValues.length || xValues.length === 0) {
      return { line: { slope: 0, intercept: 0 }, correlation: 0 };
    }
    
    const n = xValues.length;
    
    // Calculate means
    const sumX = xValues.reduce((sum, x) => sum + x, 0);
    const sumY = yValues.reduce((sum, y) => sum + y, 0);
    const meanX = sumX / n;
    const meanY = sumY / n;
    
    // Calculate sums for regression formula
    let sumXY = 0;
    let sumXX = 0;
    let sumYY = 0;
    
    for (let i = 0; i < n; i++) {
      const xDiff = xValues[i] - meanX;
      const yDiff = yValues[i] - meanY;
      sumXY += xDiff * yDiff;
      sumXX += xDiff * xDiff;
      sumYY += yDiff * yDiff;
    }
    
    // Calculate regression coefficients
    const slope = sumXX !== 0 ? sumXY / sumXX : 0;
    const intercept = meanY - slope * meanX;
    
    // Calculate correlation coefficient
    const correlation = (sumXX !== 0 && sumYY !== 0) ? 
      sumXY / Math.sqrt(sumXX * sumYY) : 0;
    
    return {
      line: { slope, intercept },
      correlation
    };
  }

  /**
   * Update statistical information in the info panel
   */
  updateStatistics() {
    if (!this.infoPanel) return;
    
    // Clear existing statistics
    this.infoPanel.innerHTML = '';
    
    // Get the current visualization
    const viz = this.currentVisualization;
    if (!viz) return;
    
    // Add title based on visualization type
    const title = document.createElement('h3');
    title.style.margin = '0 0 10px 0';
    title.style.fontSize = '16px';
    title.textContent = viz.options.title || 'Data Statistics';
    this.infoPanel.appendChild(title);
    
    // Add visualization-specific statistics
    this.standardInfoElements = [];
    
    switch (viz.type) {
      case 'bar':
        this.addStandardInfo('count', 'Count', viz.data.length.toString());
        this.addStandardInfo('sum', 'Sum', viz.data.reduce((sum, item) => sum + item.value, 0).toFixed(2));
        this.addStandardInfo('average', 'Average', (viz.data.reduce((sum, item) => sum + item.value, 0) / viz.data.length).toFixed(2));
        break;
        
      case 'histogram':
        this.addStandardInfo('count', 'Count', viz.data.length.toString());
        this.addStandardInfo('min', 'Min', viz.minValue.toFixed(2));
        this.addStandardInfo('max', 'Max', viz.maxValue.toFixed(2));
        
        const mean = viz.data.reduce((sum, val) => sum + val, 0) / viz.data.length;
        this.addStandardInfo('mean', 'Mean', mean.toFixed(2));
        
        // Calculate variance and standard deviation
        const variance = viz.data.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / viz.data.length;
        const stdDev = Math.sqrt(variance);
        
        this.addStandardInfo('stddev', 'Std Dev', stdDev.toFixed(2));
        break;
        
      case 'scatter':
        this.addStandardInfo('count', 'Count', viz.data.length.toString());
        
        if (viz.correlation !== null) {
          this.addStandardInfo('correlation', 'Correlation', viz.correlation.toFixed(3));
        }
        
        if (viz.trendline) {
          this.addStandardInfo('equation', 'Line Equation', 
            `y = ${viz.trendline.slope.toFixed(3)}x ${viz.trendline.intercept >= 0 ? '+' : ''} ${viz.trendline.intercept.toFixed(3)}`);
        }
        break;
        
      case 'box':
        this.addStandardInfo('count', 'Count', viz.data.length.toString());
        this.addStandardInfo('min', 'Min', viz.min.toFixed(2));
        this.addStandardInfo('q1', 'Q1', viz.q1.toFixed(2));
        this.addStandardInfo('median', 'Median', viz.median.toFixed(2));
        this.addStandardInfo('q3', 'Q3', viz.q3.toFixed(2));
        this.addStandardInfo('max', 'Max', viz.max.toFixed(2));
        this.addStandardInfo('iqr', 'IQR', (viz.q3 - viz.q1).toFixed(2));
        
        if (viz.mean !== null) {
          this.addStandardInfo('mean', 'Mean', viz.mean.toFixed(2));
        }
        
        if (viz.outliers && viz.outliers.length > 0) {
          this.addStandardInfo('outliers', 'Outliers', viz.outliers.length.toString());
        }
        break;
    }
  }

  /**
   * Add standard information to the info panel and track the element
   * @param {string} id - ID for the info
   * @param {string} label - Label text
   * @param {string} value - Value text
   */
  addStandardInfo(id, label, value) {
    const infoElement = this.addInfo(id, label, value);
    if (!this.standardInfoElements) this.standardInfoElements = [];
    this.standardInfoElements.push(infoElement);
  }

  /**
   * Render the current visualization
   */
  render() {
    // Call parent render to clear canvas and draw grid/axes
    super.render();
    
    // Check if there's a visualization to render
    if (!this.currentVisualization) return;
    
    // Draw axis labels
    this.drawAxisLabels();
    
    // Render based on visualization type
    switch (this.currentVisualization.type) {
      case 'bar':
        this.renderBarChart();
        break;
      case 'histogram':
        this.renderHistogram();
        break;
      case 'scatter':
        this.renderScatterPlot();
        break;
      case 'box':
        this.renderBoxPlot();
        break;
    }
  }

  /**
   * Draw axis labels
   */
  drawAxisLabels() {
    const viz = this.currentVisualization;
    if (!viz) return;
    
    // Get axis labels from options or defaults
    const xLabel = viz.options.xLabel || this.config.dataOptions.axisLabels.x;
    const yLabel = viz.options.yLabel || this.config.dataOptions.axisLabels.y;
    
    this.ctx.fillStyle = this.config.theme.textColor;
    this.ctx.font = `14px ${this.config.theme.fontFamily}`;
    
    // X-axis label
    this.ctx.textAlign = 'center';
    this.ctx.textBaseline = 'top';
    this.ctx.fillText(
      xLabel,
      this.canvas.width / 2,
      this.canvas.height - 15
    );
    
    // Y-axis label (rotated)
    this.ctx.save();
    this.ctx.translate(15, this.canvas.height / 2);
    this.ctx.rotate(-Math.PI / 2);
    this.ctx.textAlign = 'center';
    this.ctx.textBaseline = 'middle';
    this.ctx.fillText(yLabel, 0, 0);
    this.ctx.restore();
  }

  /**
   * Render a bar chart
   */
  renderBarChart() {
    const viz = this.currentVisualization;
    const { data, categoryPositions, barWidth, options } = viz;
    
    // Draw bars
    for (let i = 0; i < data.length; i++) {
      const item = data[i];
      const x = categoryPositions[i];
      const y = item.value;
      
      // Determine bar color
      let color = options.color;
      
      // Highlight selected bar
      if (this.selectedDataPoint && 
          this.selectedDataPoint.type === 'bar' && 
          this.selectedDataPoint.index === i) {
        color = this.config.theme.highlightColor;
      }
      
      // Draw the bar
      this.ctx.fillStyle = color;
      this.ctx.fillRect(
        this.toCanvasX(x - barWidth / 2),
        this.toCanvasY(y),
        this.toCanvasX(x + barWidth / 2) - this.toCanvasX(x - barWidth / 2),
        this.toCanvasY(0) - this.toCanvasY(y)
      );
      
      // Draw bar value if enabled
      if (options.showValues) {
        this.ctx.fillStyle = this.config.theme.textColor;
        this.ctx.font = `12px ${this.config.theme.fontFamily}`;
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'bottom';
        this.ctx.fillText(
          y.toFixed(1),
          this.toCanvasX(x),
          this.toCanvasY(y) - 5
        );
      }
      
      // Draw category labels
      this.ctx.fillStyle = this.config.theme.textColor;
      this.ctx.font = `12px ${this.config.theme.fontFamily}`;
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'top';
      
      // Rotate labels if there are many categories
      if (data.length > 8) {
        this.ctx.save();
        this.ctx.translate(this.toCanvasX(x), this.toCanvasY(0) + 5);
        this.ctx.rotate(-Math.PI / 4);
        this.ctx.fillText(item.category, 0, 0);
        this.ctx.restore();
      } else {
        this.ctx.fillText(
          item.category,
          this.toCanvasX(x),
          this.toCanvasY(0) + 5
        );
      }
    }
  }

  /**
   * Render a histogram
   */
  renderHistogram() {
    const viz = this.currentVisualization;
    const { bins, options } = viz;
    
    // Draw bins
    for (let i = 0; i < bins.length; i++) {
      const bin = bins[i];
      const x0 = bin.x0;
      const x1 = bin.x1;
      const frequency = bin.frequency;
      
      // Determine bin color
      let color = options.color;
      
      // Highlight selected bin
      if (this.selectedDataPoint && 
          this.selectedDataPoint.type === 'histogram' && 
          this.selectedDataPoint.index === i) {
        color = this.config.theme.highlightColor;
      }
      
      // Draw the bin
      this.ctx.fillStyle = color;
      this.ctx.fillRect(
        this.toCanvasX(x0),
        this.toCanvasY(frequency),
        this.toCanvasX(x1) - this.toCanvasX(x0),
        this.toCanvasY(0) - this.toCanvasY(frequency)
      );
      
      // Draw bin outline
      this.ctx.strokeStyle = this.config.theme.backgroundColor;
      this.ctx.lineWidth = 1;
      this.ctx.strokeRect(
        this.toCanvasX(x0),
        this.toCanvasY(frequency),
        this.toCanvasX(x1) - this.toCanvasX(x0),
        this.toCanvasY(0) - this.toCanvasY(frequency)
      );
      
      // Draw frequency if enabled
      if (options.showFrequency) {
        this.ctx.fillStyle = this.config.theme.textColor;
        this.ctx.font = `12px ${this.config.theme.fontFamily}`;
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'bottom';
        
        // Only show if bin is wide enough
        const binWidthPx = this.toCanvasX(x1) - this.toCanvasX(x0);
        if (binWidthPx > 30) {
          this.ctx.fillText(
            bin.count.toString(),
            this.toCanvasX((x0 + x1) / 2),
            this.toCanvasY(frequency) - 5
          );
        }
      }
    }
    
    // Draw x-axis bin labels
    this.ctx.fillStyle = this.config.theme.textColor;
    this.ctx.font = `10px ${this.config.theme.fontFamily}`;
    this.ctx.textAlign = 'center';
    this.ctx.textBaseline = 'top';
    
    // Show fewer labels if many bins
    const labelStep = bins.length > 10 ? Math.ceil(bins.length / 10) : 1;
    
    for (let i = 0; i < bins.length; i += labelStep) {
      const bin = bins[i];
      this.ctx.fillText(
        bin.x0.toFixed(1),
        this.toCanvasX(bin.x0),
        this.toCanvasY(0) + 5
      );
    }
    
    // Show last bin end
    if (bins.length > 0) {
      const lastBin = bins[bins.length - 1];
      this.ctx.fillText(
        lastBin.x1.toFixed(1),
        this.toCanvasX(lastBin.x1),
        this.toCanvasY(0) + 5
      );
    }
  }

  /**
   * Render a scatter plot
   */
  renderScatterPlot() {
    const viz = this.currentVisualization;
    const { data, options, trendline } = viz;
    
    // Draw trend line if available
    if (trendline && options.showTrendline) {
      const { slope, intercept } = trendline;
      const xMin = this.config.range.xMin;
      const xMax = this.config.range.xMax;
      const yMin = slope * xMin + intercept;
      const yMax = slope * xMax + intercept;
      
      this.ctx.strokeStyle = options.trendlineColor;
      this.ctx.lineWidth = 2;
      this.ctx.setLineDash([5, 3]);
      
      this.ctx.beginPath();
      this.ctx.moveTo(this.toCanvasX(xMin), this.toCanvasY(yMin));
      this.ctx.lineTo(this.toCanvasX(xMax), this.toCanvasY(yMax));
      this.ctx.stroke();
      
      this.ctx.setLineDash([]); // Reset dash pattern
    }
    
    // Draw points
    for (let i = 0; i < data.length; i++) {
      const point = data[i];
      const x = point.x;
      const y = point.y;
      
      // Determine point color and size
      let color = options.color;
      let size = options.pointSize;
      
      // Highlight selected point
      if (this.selectedDataPoint && 
          this.selectedDataPoint.type === 'point' && 
          this.selectedDataPoint.index === i) {
        color = this.config.theme.highlightColor;
        size += 2;
      }
      
      // Draw the point
      this.ctx.fillStyle = color;
      this.ctx.beginPath();
      this.ctx.arc(
        this.toCanvasX(x),
        this.toCanvasY(y),
        size,
        0,
        2 * Math.PI
      );
      this.ctx.fill();
      
      // Draw point label if enabled
      if (options.showLabels && point.label) {
        this.ctx.fillStyle = this.config.theme.textColor;
        this.ctx.font = `12px ${this.config.theme.fontFamily}`;
        this.ctx.textAlign = 'left';
        this.ctx.textBaseline = 'bottom';
        this.ctx.fillText(
          point.label,
          this.toCanvasX(x) + size + 2,
          this.toCanvasY(y) - 2
        );
      }
    }
  }

  /**
   * Render a box plot
   */
  renderBoxPlot() {
    const viz = this.currentVisualization;
    const { options, position, boxWidth, min, q1, median, q3, max, mean, outliers } = viz;
    
    // Draw box
    const boxLeft = position - boxWidth / 2;
    const boxRight = position + boxWidth / 2;
    
    // Determine colors
    let boxColor = options.color;
    let lineColor = this.config.theme.textColor;
    let whiskerColor = this.config.theme.textColor;
    let medianColor = this.config.theme.highlightColor;
    let meanColor = this.config.theme.secondaryColor;
    
    // Adjust colors based on selection
    if (this.selectedDataPoint && this.selectedDataPoint.type.startsWith('boxplot')) {
      if (this.selectedDataPoint.type === 'boxplot-box') {
        boxColor = this.config.theme.highlightColor;
      } else if (this.selectedDataPoint.type === 'boxplot-median') {
        medianColor = this.config.theme.tertiaryColor;
      } else if (this.selectedDataPoint.type === 'boxplot-whisker') {
        whiskerColor = this.config.theme.highlightColor;
      }
    }
    
    // Draw box
    this.ctx.fillStyle = boxColor;
    this.ctx.fillRect(
      this.toCanvasX(boxLeft),
      this.toCanvasY(q3),
      this.toCanvasX(boxRight) - this.toCanvasX(boxLeft),
      this.toCanvasY(q1) - this.toCanvasY(q3)
    );
    
    this.ctx.strokeStyle = lineColor;
    this.ctx.lineWidth = 1;
    this.ctx.strokeRect(
      this.toCanvasX(boxLeft),
      this.toCanvasY(q3),
      this.toCanvasX(boxRight) - this.toCanvasX(boxLeft),
      this.toCanvasY(q1) - this.toCanvasY(q3)
    );
    
    // Draw median line
    this.ctx.strokeStyle = medianColor;
    this.ctx.lineWidth = 2;
    this.ctx.beginPath();
    this.ctx.moveTo(this.toCanvasX(boxLeft), this.toCanvasY(median));
    this.ctx.lineTo(this.toCanvasX(boxRight), this.toCanvasY(median));
    this.ctx.stroke();
    
    // Draw mean if enabled
    if (mean !== null && options.showMean) {
      this.ctx.strokeStyle = meanColor;
      this.ctx.lineWidth = 1;
      this.ctx.setLineDash([3, 3]);
      this.ctx.beginPath();
      this.ctx.moveTo(this.toCanvasX(boxLeft), this.toCanvasY(mean));
      this.ctx.lineTo(this.toCanvasX(boxRight), this.toCanvasY(mean));
      this.ctx.stroke();
      this.ctx.setLineDash([]);
      
      // Draw mean symbol
      this.ctx.fillStyle = meanColor;
      this.ctx.beginPath();
      const meanX = this.toCanvasX(position);
      const meanY = this.toCanvasY(mean);
      const symbolSize = 3;
      this.ctx.moveTo(meanX - symbolSize, meanY - symbolSize);
      this.ctx.lineTo(meanX + symbolSize, meanY - symbolSize);
      this.ctx.lineTo(meanX, meanY + symbolSize);
      this.ctx.closePath();
      this.ctx.fill();
    }
    
    // Draw whiskers
    this.ctx.strokeStyle = whiskerColor;
    this.ctx.lineWidth = 1;
    
    // Lower whisker
    this.ctx.beginPath();
    this.ctx.moveTo(this.toCanvasX(position), this.toCanvasY(q1));
    this.ctx.lineTo(this.toCanvasX(position), this.toCanvasY(min));
    this.ctx.stroke();
    
    // Upper whisker
    this.ctx.beginPath();
    this.ctx.moveTo(this.toCanvasX(position), this.toCanvasY(q3));
    this.ctx.lineTo(this.toCanvasX(position), this.toCanvasY(max));
    this.ctx.stroke();
    
    // Whisker caps
    const capWidth = boxWidth / 3;
    
    // Lower cap
    this.ctx.beginPath();
    this.ctx.moveTo(this.toCanvasX(position - capWidth/2), this.toCanvasY(min));
    this.ctx.lineTo(this.toCanvasX(position + capWidth/2), this.toCanvasY(min));
    this.ctx.stroke();
    
    // Upper cap
    this.ctx.beginPath();
    this.ctx.moveTo(this.toCanvasX(position - capWidth/2), this.toCanvasY(max));
    this.ctx.lineTo(this.toCanvasX(position + capWidth/2), this.toCanvasY(max));
    this.ctx.stroke();
    
    // Draw outliers if available
    if (outliers && outliers.length > 0 && options.showOutliers) {
      this.ctx.fillStyle = this.config.theme.tertiaryColor;
      
      for (const outlier of outliers) {
        this.ctx.beginPath();
        this.ctx.arc(
          this.toCanvasX(position),
          this.toCanvasY(outlier),
          4,
          0,
          2 * Math.PI
        );
        this.ctx.fill();
      }
    }
    
    // Draw labels at the bottom
    this.ctx.fillStyle = this.config.theme.textColor;
    this.ctx.font = `12px ${this.config.theme.fontFamily}`;
    this.ctx.textAlign = 'center';
    this.ctx.textBaseline = 'top';
    
    if (options.showLabels) {
      this.ctx.fillText(
        options.label || 'Data',
        this.toCanvasX(position),
        this.toCanvasY(0) + 5
      );
    }
  }

  /**
   * Add a control for changing the visualization type
   */
  addVisualizationTypeControl() {
    return this.addControl('dropdown', {
      id: 'viz-type',
      label: 'Visualization Type',
      options: [
        { value: 'bar', text: 'Bar Chart' },
        { value: 'histogram', text: 'Histogram' },
        { value: 'scatter', text: 'Scatter Plot' },
        { value: 'box', text: 'Box Plot' }
      ],
      value: this.currentVisualization ? this.currentVisualization.type : 'bar',
      onChange: (value) => {
        // If we have data, switch visualization type
        if (this.datasets.length > 0) {
          const data = this.datasets[0].data;
          
          switch (value) {
            case 'bar':
              this.createBarChart(data);
              break;
            case 'histogram':
              this.createHistogram(data);
              break;
            case 'scatter':
              this.createScatterPlot(data);
              break;
            case 'box':
              this.createBoxPlot(data);
              break;
          }
        }
      }
    });
  }

  /**
   * Add dataset controls based on the current visualization
   */
  addDatasetControls() {
    if (!this.currentVisualization) return;
    
    const viz = this.currentVisualization;
    
    switch (viz.type) {
      case 'histogram':
        this.addControl('slider', {
          id: 'histogram-bins',
          label: 'Number of Bins',
          min: 1,
          max: 30,
          step: 1,
          value: viz.options.bins,
          onChange: (value) => {
            // Update histogram with new bin count
            const bins = parseInt(value);
            this.createHistogram(viz.data, {
              ...viz.options,
              bins: bins
            });
          }
        });
        
        this.addControl('checkbox', {
          id: 'normalize-histogram',
          text: 'Normalize Histogram',
          checked: viz.options.normalized,
          onChange: (checked) => {
            // Update histogram normalization
            this.createHistogram(viz.data, {
              ...viz.options,
              normalized: checked
            });
          }
        });
        break;
        
      case 'scatter':
        this.addControl('checkbox', {
          id: 'show-trendline',
          text: 'Show Trend Line',
          checked: viz.options.showTrendline,
          onChange: (checked) => {
            // Update scatter plot trendline visibility
            this.createScatterPlot(viz.data, {
              ...viz.options,
              showTrendline: checked
            });
          }
        });
        
        this.addControl('slider', {
          id: 'point-size',
          label: 'Point Size',
          min: 1,
          max: 10,
          step: 1,
          value: viz.options.pointSize,
          onChange: (value) => {
            // Update scatter plot point size
            this.createScatterPlot(viz.data, {
              ...viz.options,
              pointSize: parseInt(value)
            });
          }
        });
        break;
        
      case 'box':
        this.addControl('dropdown', {
          id: 'whisker-type',
          label: 'Whisker Type',
          options: [
            { value: 'iqr', text: 'IQR (1.5×)' },
            { value: 'minmax', text: 'Min/Max' }
          ],
          value: viz.options.whiskerType,
          onChange: (value) => {
            // Update box plot whisker type
            this.createBoxPlot(viz.data, {
              ...viz.options,
              whiskerType: value
            });
          }
        });
        
        this.addControl('checkbox', {
          id: 'show-mean',
          text: 'Show Mean',
          checked: viz.options.showMean,
          onChange: (checked) => {
            // Update box plot mean visibility
            this.createBoxPlot(viz.data, {
              ...viz.options,
              showMean: checked
            });
          }
        });
        
        this.addControl('checkbox', {
          id: 'show-outliers',
          text: 'Show Outliers',
          checked: viz.options.showOutliers,
          onChange: (checked) => {
            // Update box plot outlier visibility
            this.createBoxPlot(viz.data, {
              ...viz.options,
              showOutliers: checked
            });
          }
        });
        break;
    }
  }

  /**
   * Create a dataset from CSV data
   * @param {string} csvData - CSV string
   * @param {Object} options - CSV parsing options
   * @returns {Object} Created dataset
   */
  createDatasetFromCSV(csvData, options = {}) {
    // Parse CSV
    const defaultOptions = {
      header: true,
      skipEmptyLines: true,
      dynamicTyping: true,
      xColumn: 'x',  // For scatter plots
      yColumn: 'y',  // For scatter plots
      valueColumn: 'value',  // For histograms, box plots
      categoryColumn: 'category'  // For bar charts
    };
    
    const parseOptions = { ...defaultOptions, ...options };
    
    // Basic CSV parsing (in a real implementation, you might use a library like PapaParse)
    const lines = csvData.split('\n');
    const result = { data: [], fields: [] };
    
    // Parse header
    if (parseOptions.header && lines.length > 0) {
      result.fields = lines[0].split(',').map(field => field.trim());
      lines.shift();
    }
    
    // Parse data rows
    for (const line of lines) {
      if (line.trim() === '' && parseOptions.skipEmptyLines) continue;
      
      const values = line.split(',').map((value, i) => {
        if (parseOptions.dynamicTyping) {
          // Try to convert to number if possible
          const num = Number(value.trim());
          return isNaN(num) ? value.trim() : num;
        }
        return value.trim();
      });
      
      // Create object from values
      const row = {};
      for (let i = 0; i < result.fields.length && i < values.length; i++) {
        row[result.fields[i]] = values[i];
      }
      
      result.data.push(row);
    }
    
    // Process the data based on visualization type
    let processedData;
    
    // Determine data type based on columns
    const hasXY = result.fields.includes(parseOptions.xColumn) && 
                 result.fields.includes(parseOptions.yColumn);
    const hasCategoryValue = result.fields.includes(parseOptions.categoryColumn) && 
                            result.fields.includes(parseOptions.valueColumn);
    const hasValue = result.fields.includes(parseOptions.valueColumn);
    
    if (hasXY) {
      // Scatter plot data
      processedData = result.data.map(row => ({
        x: row[parseOptions.xColumn],
        y: row[parseOptions.yColumn],
        label: row.label || ''
      }));
    } else if (hasCategoryValue) {
      // Bar chart data
      processedData = result.data.map(row => ({
        category: row[parseOptions.categoryColumn],
        value: row[parseOptions.valueColumn]
      }));
    } else if (hasValue) {
      // Histogram/box plot data
      processedData = result.data.map(row => row[parseOptions.valueColumn]);
    } else {
      // Just use first numeric column
      const numericColumn = result.fields.find(field => 
        typeof result.data[0][field] === 'number'
      );
      
      if (numericColumn) {
        processedData = result.data.map(row => row[numericColumn]);
      } else {
        // Fallback to raw rows
        processedData = result.data;
      }
    }
    
    // Create and return dataset
    return this.addDataset({
      label: options.label || 'CSV Data',
      data: processedData
    });
  }

  /**
   * Load and visualize data from a CSV file
   * @param {File} file - CSV file
   * @param {Object} options - Options for visualization
   */
  loadCSVFile(file, options = {}) {
    const reader = new FileReader();
    
    reader.onload = (e) => {
      const csvData = e.target.result;
      const dataset = this.createDatasetFromCSV(csvData, options);
      
      // Determine visualization type based on data structure
      let visualizationType = options.visualizationType || 'auto';
      
      if (visualizationType === 'auto') {
        const firstItem = dataset.data[0];
        
        if (typeof firstItem === 'object' && firstItem.x !== undefined && firstItem.y !== undefined) {
          visualizationType = 'scatter';
        } else if (typeof firstItem === 'object' && firstItem.category !== undefined && firstItem.value !== undefined) {
          visualizationType = 'bar';
        } else if (typeof firstItem === 'number') {
          visualizationType = options.defaultType || 'histogram';
        } else {
          console.error('Could not determine visualization type from data');
          return;
        }
      }
      
      // Create visualization
      switch (visualizationType) {
        case 'bar':
          this.createBarChart(dataset.data, options);
          break;
        case 'histogram':
          this.createHistogram(dataset.data, options);
          break;
        case 'scatter':
          this.createScatterPlot(dataset.data, options);
          break;
        case 'box':
          this.createBoxPlot(dataset.data, options);
          break;
      }
      
      // Add visualization type control
      this.addVisualizationTypeControl();
      
      // Add dataset-specific controls
      this.addDatasetControls();
    };
    
    reader.onerror = (e) => {
      console.error('Error reading CSV file:', e);
    };
    
    reader.readAsText(file);
  }
}

export default DataVisualizer;