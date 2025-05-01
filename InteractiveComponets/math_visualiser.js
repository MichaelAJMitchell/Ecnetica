/**
 * Enhanced Math Visualization Module
 * This module handles visualization logic for the interactive math expression visualizer.
 * Enhanced to support multiple instances on a single page.
 */

// Create a namespace for our MathVisualizer
const MathVisualizer = (function() {
    // Color themes
    const colorThemes = {
        light: {
            background: '#ffffff',
            grid: '#dddddd',
            gridMajor: '#cccccc',
            axis: '#666666',
            axisLabel: '#444444',
            point: '#3498db',
            pointHighlight: '#2980b9',
            pointStroke: '#ffffff',
            functionGraph: '#2e86c1',
            functionGraphHighlight: '#1c638e',
            text: '#2d3436'
        },
        
        dark: {
            background: '#1e272e',
            grid: '#34495e',
            gridMajor: '#2c3e50',
            axis: '#ecf0f1',
            axisLabel: '#bdc3c7',
            point: '#3498db',
            pointHighlight: '#2ecc71',
            pointStroke: '#1e272e',
            functionGraph: '#2ecc71',
            functionGraphHighlight: '#27ae60',
            text: '#ecf0f1'
        }
    };

    // Sequential colors for automatic assignment
    const sequentialColors = [
        '#7b2cbfff',  // Purple
        '#e74c3c',  // Red
        '#2ecc71',  // Green
        '#9b59b6',  // Purple
        '#f39c12',  // Orange
        '#1abc9c',  // Teal
        '#d35400',  // Pumpkin
        '#34495e',  // Dark Blue
        '#16a085',  // Green Sea
        '#c0392b',  // Dark Red
    ];

    // Factory function to create a new color generator
    function createColorGenerator() {
        let colorIndex = 0;
        
        return function(reset = false) {
            if (reset) {
                colorIndex = 0;
                return null;
            }
            
            const color = sequentialColors[colorIndex % sequentialColors.length];
            colorIndex++;
            return color;
        };
    }

    /**
     * Helper to create or get DOM elements
     * @param {string} containerId - ID of the container element
     * @param {string} elementId - ID suffix for the element
     * @param {string} className - CSS class for the element
     * @param {string} tagName - HTML tag (defaults to div)
     * @param {Node} parentElement - Parent to append to if element doesn't exist
     * @return {HTMLElement} The found or created element
     */
    function getOrCreateElement(containerId, elementId, className, tagName = 'div', parentElement = null) {
        const fullId = `${containerId}-${elementId}`;
        let element = document.getElementById(fullId);
        
        if (!element) {
            element = document.createElement(tagName);
            element.id = fullId;
            if (className) {
                element.className = className;
            }
            
            // If parentElement is provided, append to it; otherwise try to find container
            if (parentElement) {
                parentElement.appendChild(element);
            } else {
                const container = document.getElementById(containerId);
                if (container) {
                    container.appendChild(element);
                } else {
                    console.error(`Container with ID '${containerId}' not found`);
                }
            }
        }
        
        return element;
    }

    /**
     * Create a graph instance
     * @param {string} containerId - ID of the container element
     * @return {Object} An object with methods to create and manage the graph
     */
    function createGraphInstance(containerId) {
        // Private instance variables
        let board = null;
        let currentConfig = {};
        let parameterValues = {};
        let functionGraph = null;
        let specialPoints = [];
        let specialLines = [];
        let getNextSequentialColor = createColorGenerator();
        
        // DOM elements
        let elements = {
            board: null,
            infoBox: null,
            equation: null,
            extraInfo: null,
            sliderContainer: null,
            graphTitle: null
        };

        /**
         * Set up the DOM elements for the graph
         * @param {string} theme - 'light' or 'dark'
         */
        function setupDomElements(theme) {
            const containerElement = document.getElementById(containerId);
            if (!containerElement) {
                console.error(`Container with ID '${containerId}' not found`);
                return false;
            }
            
            // Make sure position is relative if not already set
            if (window.getComputedStyle(containerElement).position === 'static') {
                containerElement.style.position = 'relative';
            }
            
            // Create the graph title if not exists
            elements.graphTitle = getOrCreateElement(
                containerId, 
                'graphTitle', 
                'graph-title', 
                'h3', 
                containerElement
            );
            
            // Create the JSXGraph board container if not exists
            elements.board = getOrCreateElement(
                containerId, 
                'board', 
                'jxgbox', 
                'div', 
                containerElement
            );
            
            // Create info box container
            elements.infoBox = getOrCreateElement(
                containerId, 
                'equationInfo', 
                `info-box equation-info ${theme === 'dark' ? 'dark-theme' : ''}`, 
                'div', 
                containerElement
            );
            
            // Create equation and extra info divs inside info box
            elements.equation = getOrCreateElement(
                containerId, 
                'equation', 
                '', 
                'div', 
                elements.infoBox
            );
            
            elements.extraInfo = getOrCreateElement(
                containerId, 
                'extraInfo', 
                '', 
                'div', 
                elements.infoBox
            );
            
            // Create slider container
            elements.sliderContainer = getOrCreateElement(
                containerId, 
                'sliderContainer', 
                `slider-container ${theme === 'dark' ? 'dark-theme' : ''}`, 
                'div', 
                containerElement
            );
            
            // Add control buttons if needed
            const controlsDiv = getOrCreateElement(
                containerId,
                'controls',
                'controls',
                'div',
                containerElement
            );
            
            // Add reset button
            const resetButton = getOrCreateElement(
                containerId,
                'resetView',
                'control-btn',
                'button',
                controlsDiv
            );
            resetButton.textContent = 'Reset View';
            resetButton.addEventListener('click', resetView);
            
            // Add theme toggle button
            const themeButton = getOrCreateElement(
                containerId,
                'toggleTheme',
                'control-btn',
                'button',
                controlsDiv
            );
            themeButton.textContent = 'Toggle Theme';
            themeButton.addEventListener('click', toggleTheme);
            
            return true;
        }

        /**
         * Create a graph from a description object
         * @param {Object} description - Description of the graph
         * @return {Object} The created board and related objects
         */
        function createGraphFromDescription(description) {
            const { boundingBox, theme, useSequentialColors, elements: customElements, parametrizedFunctions, infoBox } = description;
            
            // Set up DOM elements
            if (!setupDomElements(theme || 'light')) {
                return null;
            }
            
            // Clear any existing content
            if (board) {
                JXG.JSXGraph.freeBoard(board);
            }
            
            // Create board
            const boardElementId = `${containerId}-board`;
            board = JXG.JSXGraph.initBoard(boardElementId, {
                boundingbox: boundingBox || [-5, 5, 5, -5],
                axis: true,
                grid: true,
                showNavigation: false,
                showCopyright: false,
                pan: {
                    enabled: true,
                    needTwoFingers: false,
                    needShift: false
                },
                zoom: {
                    enabled: true,
                    factorX: 1.1,
                    factorY: 1.1,
                    wheel: true,
                    needShift: false,
                    pinch: true,
                    min: 0.15,
                    max: 10
                }
            });
            
            // Store original bounding box
            board.originalBoundingBox = boundingBox || [-5, 5, 5, -5];
            board.currentTheme = theme || 'light';
            
            // Setup theme
            if (theme === 'dark') {
                applyTheme('dark');
            }
            
            // Reset sequential color counter if needed
            if (useSequentialColors) {
                getNextSequentialColor(true);
            }
            
            // Handle parametrized functions if any
            if (parametrizedFunctions && parametrizedFunctions.length > 0) {
                // Take the first parametrized function for now
                const funcDesc = parametrizedFunctions[0];
                
                // Update title if provided
                if (funcDesc.title) {
                    elements.graphTitle.textContent = funcDesc.title;
                }
                
                // Setup parameters FIRST - before configuring info box
                parameterValues = {};
                for (const param in funcDesc.parameters) {
                    parameterValues[param] = funcDesc.parameters[param].value;
                }
                
                // NOW we can configure the info box
                if (infoBox) {
                    configureInfoBox(infoBox);
                }
                
                // Create sliders
                createParameterSliders(funcDesc.parameters);
                
                // Store current config for updates
                currentConfig = funcDesc;
                
                // Create function graph with sequential coloring if needed
                const compileExpr = Math.compile(funcDesc.expression);
                const func = function(x) {
                    const scope = { ...parameterValues, x: x };
                    return compileExpr.evaluate(scope);
                };
                
                const graphColor = useSequentialColors ? getNextSequentialColor() : '#2e86c1';
                
                functionGraph = board.create('functiongraph', [func, -30, 30], {
                    strokeWidth: 3,
                    strokeColor: graphColor
                });
                
                // Update equation display if no custom info box was provided
                if (!infoBox) {
                    updateEquationDisplay();
                }
                
                // Add special features
                if (funcDesc.features) {
                    addSpecialFeatures(func);
                }
            } else {
                // If no parametrized functions but we do have an info box
                if (infoBox) {
                    configureInfoBox(infoBox);
                }
            }
            
            // Create standard elements if provided
            if (customElements && customElements.length > 0) {
                for (const element of customElements) {
                    const { type, data, properties } = element;
                    
                    // If using sequential colors and no color specified, assign one
                    let finalProperties = { ...properties };
                    if (useSequentialColors && !properties.strokeColor) {
                        const color = getNextSequentialColor();
                        finalProperties.strokeColor = color;
                        
                        if (type === 'point') {
                            finalProperties.fillColor = color;
                        }
                    }
                    
                    // Create the element
                    board.create(type, data, finalProperties);
                }
            }
            
            // Add event listener for sliders container to prevent event propagation
            elements.sliderContainer.addEventListener('touchstart', function(e) {
                e.stopPropagation();
            }, true);
            
            elements.sliderContainer.addEventListener('touchmove', function(e) {
                e.stopPropagation();
            }, true);
            
            // Return board and related objects
            return {
                board,
                elements,
                parameterValues,
                updateFunctionVisualization,
                resetView,
                toggleTheme,
                removeAxes: function() {
                    if (board.defaultAxes) {
                        board.removeObject(board.defaultAxes.x);
                        board.removeObject(board.defaultAxes.y);
                        board.defaultAxes = null;
                    }
                },
                removeGrids: function() {
                    if (board.hasGrid) {
                        board.removeGrids();
                        board.hasGrid = false;
                    }
                }
            };
        }

        /**
         * Configure the info box based on the provided configuration
         */
        function configureInfoBox(config) {
            // Clear existing content
            elements.equation.textContent = '';
            elements.extraInfo.innerHTML = '';
            
            // Set title/header if provided
            if (config.title) {
                elements.equation.textContent = config.title;
            }
            
            // Add custom lines
            if (config.lines && Array.isArray(config.lines)) {
                config.lines.forEach(line => {
                    const lineEl = document.createElement('div');
                    
                    if (line.dynamic) {
                        // Store the template for dynamic updates
                        lineEl.dataset.template = line.text;
                        lineEl.dataset.dynamic = 'true';
                        
                        // Initial evaluation
                        lineEl.textContent = evaluateDynamicText(line.text);
                    } else {
                        lineEl.textContent = line.text;
                    }
                    
                    elements.extraInfo.appendChild(lineEl);
                });
            }
            
            // Set position if provided
            if (config.position) {
                if (config.position.top !== undefined) {
                    elements.infoBox.style.top = `${config.position.top}px`;
                }
                if (config.position.left !== undefined) {
                    elements.infoBox.style.left = `${config.position.left}px`;
                }
                if (config.position.right !== undefined) {
                    elements.infoBox.style.right = `${config.position.right}px`;
                    elements.infoBox.style.left = 'auto';
                }
                if (config.position.bottom !== undefined) {
                    elements.infoBox.style.bottom = `${config.position.bottom}px`;
                    elements.infoBox.style.top = 'auto';
                }
            }
            
            // Set custom styles if provided
            if (config.style) {
                Object.entries(config.style).forEach(([property, value]) => {
                    elements.infoBox.style[property] = value;
                });
            }
        }

        /**
         * Evaluate dynamic text with parameter values
         */
        function evaluateDynamicText(template) {
            try {
                // Replace ${expression} with evaluated value
                return template.replace(/\${([^}]+)}/g, (match, expr) => {
                    // Create a scope with current parameter values
                    const scope = { ...parameterValues, Math };
                    
                    try {
                        // Evaluate the expression
                        const result = Math.evaluate(expr, scope);
                        
                        // Format the result
                        return typeof result === 'number' ? result.toFixed(2) : result;
                    } catch (error) {
                        console.error(`Error evaluating expression: ${expr}`, error);
                        return "(calculating...)";
                    }
                });
            } catch (error) {
                console.error("Error evaluating dynamic text:", error);
                return template + " (error)";
            }
        }

        /**
         * Update dynamic info in the info box
         */
        function updateInfoBox() {
            const dynamicLines = elements.extraInfo.querySelectorAll('[data-dynamic="true"]');
            
            dynamicLines.forEach(line => {
                const template = line.dataset.template;
                line.textContent = evaluateDynamicText(template);
            });
        }

        /**
         * Create sliders for all parameters
         */
        function createParameterSliders(parameters) {
            elements.sliderContainer.innerHTML = '';
            
            for (const param in parameters) {
                const { min, max, value, step } = parameters[param];
                
                // Create slider row
                const sliderRow = document.createElement('div');
                sliderRow.className = 'slider-row';
                
                // Create label
                const label = document.createElement('div');
                label.className = 'slider-label';
                label.textContent = param + ':';
                
                // Create slider
                const slider = document.createElement('input');
                slider.type = 'range';
                slider.className = 'slider-input';
                slider.min = min;
                slider.max = max;
                slider.step = step || 0.1;
                slider.value = value;
                
                // Create value display
                const valueDisplay = document.createElement('div');
                valueDisplay.className = 'slider-value';
                valueDisplay.textContent = value.toFixed(1);
                
                // Add event listener
                slider.addEventListener('input', function() {
                    const newValue = parseFloat(this.value);
                    parameterValues[param] = newValue;
                    valueDisplay.textContent = newValue.toFixed(1);
                    updateFunctionVisualization();
                });
                
                // Add elements to row
                sliderRow.appendChild(label);
                sliderRow.appendChild(slider);
                sliderRow.appendChild(valueDisplay);
                
                // Add row to container
                elements.sliderContainer.appendChild(sliderRow);
            }
        }

        /**
         * Update the function visualization based on current parameters
         */
        function updateFunctionVisualization() {
            try {
                // Clear existing visualization
                clearVisualization();
                
                // Compile the math expression
                const expr = currentConfig.expression;
                const scope = { ...parameterValues, x: 0 }; // Add x with a dummy value
                const compiledExpression = Math.compile(expr);
                
                // Create function for JSXGraph
                const func = function(x) {
                    scope.x = x;
                    return compiledExpression.evaluate(scope);
                };
                
                // Create the function graph
                functionGraph = board.create('functiongraph', [func, -30, 30], {
                    strokeWidth: 3,
                    strokeColor: board.currentTheme === 'dark' ? colorThemes.dark.functionGraph : colorThemes.light.functionGraph
                });
                
                // Update equation display if no custom info box config is provided
                const hasDynamicContent = elements.extraInfo.querySelector('[data-dynamic="true"]');
                
                if (hasDynamicContent) {
                    updateInfoBox();
                } else {
                    updateEquationDisplay();
                }
                
                // Add special features
                if (currentConfig.features) {
                    addSpecialFeatures(func);
                }
                
                // Update the board
                board.update();
            } catch (error) {
                console.error("Error updating function:", error);
                elements.equation.textContent = "Error: " + error.message;
            }
        }

        /**
         * Clear the current visualization (remove function graph and special points)
         */
        function clearVisualization() {
            // Remove function graph
            if (functionGraph) {
                board.removeObject(functionGraph);
                functionGraph = null;
            }
            
            // Remove special points
            for (const point of specialPoints) {
                board.removeObject(point);
            }
            specialPoints = [];
            
            // Remove special lines
            for (const line of specialLines) {
                board.removeObject(line);
            }
            specialLines = [];
        }

        /**
         * Update the equation display with the current parameters
         */
        function updateEquationDisplay() {
            let displayExpr = currentConfig.expression;
            
            // Replace parameters with their values
            for (const param in parameterValues) {
                const value = parameterValues[param].toFixed(1).replace(/\.0$/, '');
                const regex = new RegExp(param, 'g');
                
                if (value === '1' && displayExpr.includes(param + '*')) {
                    // Replace "a*" with "" when a=1
                    displayExpr = displayExpr.replace(new RegExp(param + '\\*', 'g'), '');
                } else if (value === '-1' && displayExpr.includes(param + '*')) {
                    // Replace "a*" with "-" when a=-1
                    displayExpr = displayExpr.replace(new RegExp(param + '\\*', 'g'), '-');
                } else if (value === '0' && displayExpr.includes(param + '*')) {
                    // Remove terms with coefficient 0, handling "+ 0*" and "- 0*"
                    displayExpr = displayExpr.replace(new RegExp('[+\\-]\\s*' + param + '\\*[^+\\-]*', 'g'), '');
                    // Also handle the case if it's the first term
                    displayExpr = displayExpr.replace(new RegExp('^' + param + '\\*[^+\\-]*', 'g'), '0');
                } else {
                    // Normal replacement
                    displayExpr = displayExpr.replace(regex, value);
                }
            }
            
            // Simplify the display
            displayExpr = displayExpr
                .replace(/\^2/g, '²')
                .replace(/\^3/g, '³')
                .replace(/\*x/g, 'x')
                .replace(/\*\(/g, '(')
                .replace(/\+ -/g, '- ')
                .replace(/- -/g, '+ ')
                .replace(/^\s*-\s*/g, '-'); // Leading minus sign
            
            // If the expression is just 0, make sure to show that
            if (displayExpr.trim() === '') {
                displayExpr = '0';
            }
            
            elements.equation.textContent = 'y = ' + displayExpr;
        }

        /**
         * Add special features like zeros, extrema points, etc.
         */
        function addSpecialFeatures(func) {
            const features = currentConfig.features;
            
            // Helper to create a feature info line
            const addFeatureInfo = (text) => {
                const div = document.createElement('div');
                div.textContent = text;
                elements.extraInfo.appendChild(div);
            };
            
            // Check if we should skip adding feature info text
            // but STILL add the feature points to the graph
            const hasDynamicContent = elements.extraInfo.querySelector('[data-dynamic="true"]');
            
            if (features.includes('zeros')) {
                try {
                    // Try to find zeros within a reasonable range
                    const zeros = findZeros(func, -30, 30);
                    
                    if (zeros.length > 0) {
                        // Add zeros to the graph
                        for (const zero of zeros) {
                            const point = board.create('point', [zero, 0], {
                                size: 4,
                                name: '',
                                fillColor: '#e74c3c',
                                strokeColor: '#ffffff'
                            });
                            specialPoints.push(point);
                        }
                        
                        // Only add info text if we don't have dynamic content
                        if (!hasDynamicContent) {
                            const zerosText = zeros.length === 1 ? 
                                `Zero: x = ${zeros[0].toFixed(2)}` : 
                                `Zeros: x = ${zeros.map(z => z.toFixed(2)).join(', ')}`;
                                
                            addFeatureInfo(zerosText);
                        }
                    } else if (!hasDynamicContent) {
                        addFeatureInfo("No zeros found in range [-10, 10]");
                    }
                } catch (error) {
                    console.error("Error finding zeros:", error);
                }
            }
            
            if (features.includes('extrema')) {
                try {
                    // Find extrema within a reasonable range
                    const extrema = findExtrema(func, -30, 30);
                    
                    if (extrema.length > 0) {
                        // Add extrema to the graph
                        for (const point of extrema) {
                            const jsxPoint = board.create('point', [point.x, point.y], {
                                size: 4,
                                name: '',
                                fillColor: '#2ecc71',
                                strokeColor: '#ffffff'
                            });
                            specialPoints.push(jsxPoint);
                            
                            // If it's a quadratic, add axis of symmetry
                            if (currentConfig.expression.includes('x^2') && extrema.length === 1) {
                                const axis = board.create('line', 
                                    [[point.x, -20], [point.x, 20]], 
                                    {dash: 2, strokeColor: '#95a5a6', strokeWidth: 1}
                                );
                                specialLines.push(axis);
                                
                                if (!hasDynamicContent) {
                                    addFeatureInfo(`Axis of symmetry: x = ${point.x.toFixed(2)}`);
                                }
                            }
                        }
                        
                        // Only add info text if we don't have dynamic content
                        if (!hasDynamicContent) {
                            const extremaText = extrema.length === 1 ? 
                                `${extrema[0].type} at (${extrema[0].x.toFixed(2)}, ${extrema[0].y.toFixed(2)})` : 
                                `Extrema: ${extrema.map(e => `${e.type} at (${e.x.toFixed(2)}, ${e.y.toFixed(2)})`).join(', ')}`;
                                
                            addFeatureInfo(extremaText);
                        }
                    } else if (!hasDynamicContent) {
                        addFeatureInfo("No extrema found in range [-10, 10]");
                    }
                } catch (error) {
                    console.error("Error finding extrema:", error);
                }
            }
        }

        /**
         * Find zeros of a function within a range
         */
        function findZeros(func, min, max, tolerance = 0.000001) {
            const zeros = [];
            const steps = 500; // Significantly more sampling points
            const stepSize = (max - min) / steps;
            const mergeThreshold = 0.05; // Threshold to consider two zeros as the same
            
            // Sample the function at regular intervals with higher precision
            for (let i = 0; i < steps; i++) {
                const x1 = min + i * stepSize;
                const x2 = x1 + stepSize;
                const y1 = func(x1);
                const y2 = func(x2);
                
                // Check for sign change - more robust condition
                if ((y1 > 0 && y2 < 0) || (y1 < 0 && y2 > 0) || Math.abs(y1) < tolerance || Math.abs(y2) < tolerance) {
                    // Skip if both values are just numerical noise
                    if (Math.abs(y1) < 1e-10 && Math.abs(y2) < 1e-10) {
                        continue;
                    }
                    
                    // Use multiple methods to find the zero for better accuracy
                    let zeroValue = null;
                    
                    // Method 1: Binary search for more accuracy
                    if ((y1 > 0 && y2 < 0) || (y1 < 0 && y2 > 0)) {
                        let a = x1;
                        let b = x2;
                        let ya = y1;
                        let yb = y2;
                        
                        // More iterations for better precision
                        for (let j = 0; j < 20; j++) {
                            const mid = (a + b) / 2;
                            const ymid = func(mid);
                            
                            if (Math.abs(ymid) < tolerance) {
                                zeroValue = mid;
                                break;
                            }
                            
                            if ((ya > 0 && ymid < 0) || (ya < 0 && ymid > 0)) {
                                b = mid;
                                yb = ymid;
                            } else {
                                a = mid;
                                ya = ymid;
                            }
                        }
                        
                        // If we didn't find an exact zero, use linear interpolation for better estimate
                        if (zeroValue === null) {
                            // Linear interpolation for better accuracy
                            zeroValue = x1 + (x2 - x1) * (0 - y1) / (y2 - y1);
                        }
                    } 
                    // Method 2: Direct detection for values very close to zero
                    else if (Math.abs(y1) < tolerance) {
                        zeroValue = x1;
                    } else if (Math.abs(y2) < tolerance) {
                        zeroValue = x2;
                    }
                    
                    // Verification step: confirm this is actually a zero
                    if (zeroValue !== null) {
                        const yAtZero = func(zeroValue);
                        
                        // Only accept if the function value at the zero is very small
                        if (Math.abs(yAtZero) > 0.01) {
                            continue; // Not actually a zero, just numerical instability
                        }
                        
                        // Check if this zero is too close to an existing one
                        let isDuplicate = false;
                        for (const existingZero of zeros) {
                            if (Math.abs(existingZero - zeroValue) < mergeThreshold) {
                                isDuplicate = true;
                                break;
                            }
                        }
                        
                        // Only add if it's not a duplicate
                        if (!isDuplicate) {
                            zeros.push(zeroValue);
                        }
                    }
                }
            }
            
            // Final verification pass - calculate function value at each zero and
            // remove any that aren't actually zeros (y value too far from 0)
            const verifiedZeros = zeros.filter(z => Math.abs(func(z)) < 0.005);
            
            // Sort the zeros for consistent results
            return verifiedZeros.sort((a, b) => a - b);
        }

        /**
         * Find extrema of a function within a range
         */
        function findExtrema(func, min, max, samples = 400) {
            const extrema = [];
            const stepSize = (max - min) / samples;
            const mergeThreshold = 0.05; // Threshold to consider two extrema as the same
            const tolerance = 0.000001;
            
            // Helper for numerical differentiation with more precision
            const derivative = function(x, h = 0.00001) {
                return (func(x + h) - func(x - h)) / (2 * h);
            };
            
            // Helper for second derivative with more precision
            const secondDerivative = function(x, h = 0.00005) {
                return (func(x + h) - 2 * func(x) + func(x - h)) / (h * h);
            };
            
            // First, make a rough pass to identify regions of interest
            const candidateRegions = [];
            
            for (let i = 0; i < samples; i++) {
                const x1 = min + i * stepSize;
                const x2 = x1 + stepSize;
                const d1 = derivative(x1);
                const d2 = derivative(x2);
                
                // Check for sign change in the derivative
                if ((d1 > 0 && d2 < 0) || (d1 < 0 && d2 > 0) || Math.abs(d1) < tolerance || Math.abs(d2) < tolerance) {
                    candidateRegions.push([x1, x2]);
                }
            }
            
            // Now examine each candidate region more carefully
            for (const [regionStart, regionEnd] of candidateRegions) {
                // Use Newton's method for more precise root finding of the derivative
                let x = (regionStart + regionEnd) / 2; // Start in the middle
                let prevX = x;
                let iterations = 0;
                let converged = false;
                
                while (iterations < 20) {
                    const df = derivative(x);
                    const ddf = secondDerivative(x);
                    
                    // Check if we're already at an extremum
                    if (Math.abs(df) < tolerance) {
                        converged = true;
                        break;
                    }
                    
                    // Avoid division by very small numbers
                    if (Math.abs(ddf) < 1e-10) {
                        break;
                    }
                    
                    // Newton's method step
                    const newX = x - df / ddf;
                    
                    // Check if we've converged
                    if (Math.abs(newX - x) < tolerance) {
                        x = newX;
                        converged = true;
                        break;
                    }
                    
                    // Check if we're still in our region of interest
                    if (newX < regionStart || newX > regionEnd) {
                        // If outside, use bisection method instead
                        break;
                    }
                    
                    // Update for next iteration
                    prevX = x;
                    x = newX;
                    iterations++;
                }
                
                // If Newton's method didn't converge, fall back to binary search
                if (!converged) {
                    let a = regionStart;
                    let b = regionEnd;
                    let da = derivative(a);
                    let db = derivative(b);
                    
                    for (let j = 0; j < 20; j++) {
                        const mid = (a + b) / 2;
                        const dmid = derivative(mid);
                        
                        if (Math.abs(dmid) < tolerance) {
                            x = mid;
                            converged = true;
                            break;
                        }
                        
                        if ((da > 0 && dmid < 0) || (da < 0 && dmid > 0)) {
                            b = mid;
                            db = dmid;
                        } else {
                            a = mid;
                            da = dmid;
                        }
                    }
                    
                    if (!converged) {
                        x = (a + b) / 2; // Use the midpoint as an approximation
                    }
                }
                
                // Get the y-value and determine the type of extremum
                const extremumY = func(x);
                const sd = secondDerivative(x);
                
                let type;
                if (Math.abs(sd) < 0.001) {
                    type = "Inflection point";
                } else {
                    type = sd > 0 ? "Minimum" : "Maximum";
                }
                
                // Skip inflection points
                if (type === "Inflection point") {
                    continue;
                }
                
                // Verify it's actually an extremum by checking neighboring points
                const h = 0.01;
                const leftY = func(x - h);
                const rightY = func(x + h);
                
                if (type === "Maximum" && (leftY > extremumY || rightY > extremumY)) {
                    continue; // Not actually a maximum
                }
                
                if (type === "Minimum" && (leftY < extremumY || rightY < extremumY)) {
                    continue; // Not actually a minimum
                }
                
                // Check if this extremum is too close to an existing one
                let isDuplicate = false;
                for (const existing of extrema) {
                    if (Math.abs(existing.x - x) < mergeThreshold) {
                        isDuplicate = true;
                        break;
                    }
                }
                
                // Only add if it's not a duplicate
                if (!isDuplicate) {
                    extrema.push({
                        x: x,
                        y: extremumY,
                        type: type
                    });
                }
            }
            
            // Sort the extrema by x-coordinate
            return extrema.sort((a, b) => a.x - b.x);
        }
        

        /**
         * Reset the view to original state
         */
        function resetView() {
            // Reset board to original bounding box
            board.setBoundingBox(board.originalBoundingBox);
            
            // Reset parameters to default values
            for (const param in currentConfig.parameters) {
                parameterValues[param] = currentConfig.parameters[param].value;
            }
            
            // Update sliders
            const sliders = elements.sliderContainer.querySelectorAll('input[type="range"]');
            const valueDisplays = elements.sliderContainer.querySelectorAll('.slider-value');
            
            Array.from(sliders).forEach((slider, index) => {
                const param = Object.keys(currentConfig.parameters)[index];
                slider.value = currentConfig.parameters[param].value;
                valueDisplays[index].textContent = currentConfig.parameters[param].value.toFixed(1);
            });
            
            // Update visualization
            updateFunctionVisualization();
        }

        /**
         * Apply a theme to the board and UI elements
         */
        function applyTheme(theme) {
            if (theme === 'dark') {
                if (!board) return;
                
                board.containerObj.style.backgroundColor = colorThemes.dark.background;
                
                // Update axes colors
                if (board.defaultAxes) {
                    board.defaultAxes.x.setAttribute({strokeColor: colorThemes.dark.axis});
                    board.defaultAxes.y.setAttribute({strokeColor: colorThemes.dark.axis});
                }
                
                // Update grid colors
                if (board.hasGrid) {
                    board.gridX.setAttribute({strokeColor: colorThemes.dark.grid});
                    board.gridY.setAttribute({strokeColor: colorThemes.dark.grid});
                }
                
                // Update function graph color
                if (functionGraph) {
                    functionGraph.setAttribute({strokeColor: colorThemes.dark.functionGraph});
                }
                
                // Update special points
                for (const point of specialPoints) {
                    point.setAttribute({strokeColor: colorThemes.dark.background});
                }
                
                // Update UI elements
                elements.infoBox.classList.add('dark-theme');
                elements.sliderContainer.classList.add('dark-theme');
            } else {
                if (!board) return;
                
                board.containerObj.style.backgroundColor = colorThemes.light.background;
                
                // Update axes colors
                if (board.defaultAxes) {
                    board.defaultAxes.x.setAttribute({strokeColor: colorThemes.light.axis});
                    board.defaultAxes.y.setAttribute({strokeColor: colorThemes.light.axis});
                }
                
                // Update grid colors
                if (board.hasGrid) {
                    board.gridX.setAttribute({strokeColor: colorThemes.light.grid});
                    board.gridY.setAttribute({strokeColor: colorThemes.light.grid});
                }
                
                // Update function graph color
                if (functionGraph) {
                    functionGraph.setAttribute({strokeColor: colorThemes.light.functionGraph});
                }
                
                // Update special points
                for (const point of specialPoints) {
                    point.setAttribute({strokeColor: colorThemes.light.background});
                }
                
                // Update UI elements
                elements.infoBox.classList.remove('dark-theme');
                elements.sliderContainer.classList.remove('dark-theme');
            }
            
            board.update();
        }

        /**
         * Toggle between light and dark themes
         */
        function toggleTheme() {
            const isDark = board.currentTheme === 'dark';
            board.currentTheme = isDark ? 'light' : 'dark';
            
            applyTheme(board.currentTheme);
        }

        // Return the public API
        return {
            createGraphFromDescription
        };
    }

    /**
     * Main initialization function - now just returns factory functions
     */
    function initMathVisualizer() {
        console.log("Math Visualizer module initialized");
        // Nothing to do for initialization now that we use instance-based approach
    }

    /**
     * Create a graph from a description object (main API function)
     * 
     * @param {string} containerId - ID of the container element
     * @param {Object} description - Description of the graph 
     */
    function createGraphFromDescription(containerId, description) {
        const instance = createGraphInstance(containerId);
        return instance.createGraphFromDescription(description);
    }

    // Export the public API
    return {
        initMathVisualizer,
        createGraphFromDescription
    };
})();

// Initialize when the page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log("Math Visualizer module loaded");
    MathVisualizer.initMathVisualizer();
});