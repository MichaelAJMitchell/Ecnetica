/**
 * JSXGraph Modular Visualization Library
 * 
 * A configurable system for creating mathematical visualizations across the curriculum
 * Designed for LLM-generated content with minimal boilerplate
 */

const JSXGraphModule = (function() {
    //===========================================================================
    // CONFIGURATION SYSTEM
    //=========================================================================== 
    // Sequential color palette for automatic assignment
    const sequentialColors = [
        '#3498db',  // Blue
        '#e74c3c',  // Red
        '#2ecc71',  // Green
        '#9b59b6',  // Purple
        '#f39c12',  // Orange
        '#1abc9c',  // Teal
        '#d35400',  // Pumpkin
        '#34495e',  // Dark Blue
        '#16a085',  // Green Sea
        '#c0392b',  // Dark Red
        '#8e44ad',  // Wisteria
        '#27ae60',  // Nephritis
        '#e67e22',  // Carrot
        '#2980b9',  // Belize Hole
    ];
    
    // Element style templates for consistent styling
    const elementStyles = {
        // Point styling template
        point: {
            size: 5,
            highlightSize: 8,
            strokeWidth: 2,
            highlightStrokeWidth: 3,
            fixed: false,
            snapToGrid: false,
            snapSizeX: 1,
            snapSizeY: 1,
            label: {
                fontSize: 16,
                fontWeight: "normal",
                offset: [10, 10],
                autoPosition: true
            }
        },
        
        // Line styling template
        line: {
            straightFirst: true,
            straightLast: true,
            strokeWidth: 2.5,
            highlightStrokeWidth: 3.5,
            dash: 0,
            fixed: false,
            label: {
                fontSize: 15,
                fontWeight: "normal",
                autoPosition: true,
                position: "middle",
                offsets: [[10, -10], [10, 10]]
            }
        },
        
        // Function graph styling template
        functiongraph: {
            strokeWidth: 3,
            highlightStrokeWidth: 4,
            doAdvancedPlot: true,
            numberPointsHigh: 600, // Higher resolution curve
            numberPointsLow: 100,  // Lower resolution for performance during interactions
        },
        
        // Circle styling template
        circle: {
            strokeWidth: 2,
            highlightStrokeWidth: 3,
            fillOpacity: 0.1,
            highlightFillOpacity: 0.3,
            label: {
                fontSize: 15,
                fontWeight: "normal",
                autoPosition: true
            }
        },
        
        // Polygon styling template
        polygon: {
            borders: {
                strokeWidth: 2,
                highlightStrokeWidth: 3
            },
            fillOpacity: 0.2,
            highlightFillOpacity: 0.4,
            label: {
                fontSize: 15,
                fontWeight: "normal"
            }
        },
        
        // Text styling template
        text: {
            fontSize: 16,
            fontWeight: "normal",
            cssClass: "jsxgraph-text",
            highlightCssClass: "jsxgraph-text-highlight",
            useKatex: true,  // For math formulas
            useMathJax: false
        },
        
        // Slider styling template
        slider: {
            size: 5,
            point1: { visible: false },
            point2: { visible: false },
            baseline: { strokeColor: '#999', strokeWidth: 2 },
            ticks: { visible: true, strokeColor: '#999', strokeWidth: 1, highlightStrokeWidth: 1 },
            label: {
                fontSize: 16,
                offsets: [0, -15]
            },
            suffixLabel: '',
            snapWidth: 0.1
        }
    };
    
    //===========================================================================
    // UTILITY FUNCTIONS
    //===========================================================================
    
    // Function to get the next color from the sequence
    const getNextSequentialColor = (function() {
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
    })();
    
    // Helper function to darken/lighten colors for highlights
    function adjustColorBrightness(hex, percent) {
        // Convert hex to RGB
        let r = parseInt(hex.substring(1, 3), 16);
        let g = parseInt(hex.substring(3, 5), 16);
        let b = parseInt(hex.substring(5, 7), 16);
        
        // Adjust brightness
        r = Math.max(0, Math.min(255, r + (r * percent / 100)));
        g = Math.max(0, Math.min(255, g + (g * percent / 100)));
        b = Math.max(0, Math.min(255, b + (b * percent / 100)));
        
        // Convert back to hex
        return `#${Math.round(r).toString(16).padStart(2, '0')}${Math.round(g).toString(16).padStart(2, '0')}${Math.round(b).toString(16).padStart(2, '0')}`;
    }
    
    // Generate a unique ID
    function generateUniqueId(prefix = 'jsxgraph') {
        return `${prefix}-${Math.random().toString(36).substring(2, 11)}`;
    }
    
    //===========================================================================
    // CORE BOARD MANAGEMENT
    //===========================================================================
    
    /**
     * Creates a JSXGraph board configuration
     * @param {Object} options - Configuration options
     * @returns {Object} - JSXGraph board configuration
     */
    function createBoardConfig(options = {}) {
        // Set defaults
        const {
            colors = colorThemes.light,
            boundingBox = [-5, 5, 5, -5],
            showNavigation = false,
            showGrid = true,
            showAxes = true
        } = options;
        
        // Build configuration
        return {
            boundingbox: boundingBox,
            axis: showAxes,
            grid: showGrid,
            showNavigation: showNavigation,
            showCopyright: false,
            background: colors.background,
            
            // Axis styling
            
            
            // Grid styling
            grid: {
                strokeColor: colors.grid,
                strokeWidth: 0.8,
                majorLineColor: colors.gridMajor,
                majorLineWidth: 1
            },
            
            // Touch configuration
            pan: {
                enabled: true,
                needTwoFingers: false,
                needShift: false
            },
            zoom: {
                enabled: true,
                factorX: 1.08,
                factorY: 1.08,
                wheel: true,
                needShift: false,
                pinch: true,
                min: 0.1,
                max: 10
            }
        };
    }
    
    /**
     * Creates a styled element on the board
     * @param {Object} board - JSXGraph board
     * @param {string} type - Element type (point, line, etc.)
     * @param {Array|Function} data - Element data
     * @param {Object} customProperties - Custom properties to override defaults
     * @returns {Object} - Created JSXGraph element
     */
    function createElement(board, type, data, customProperties = {}) {
        // Get the base style for this element type
        const baseStyle = elementStyles[type] || {};
        
        // Get colors for this element type
        const themeColors = board.options.colors || colorThemes.light;
        
        // Apply color styling based on element type
        let colorProperties = {};
        
        switch (type) {
            case 'point':
                colorProperties = {
                    fillColor: customProperties.fillColor || themeColors.point,
                    strokeColor: customProperties.strokeColor || themeColors.pointStroke,
                    highlightFillColor: customProperties.highlightFillColor || themeColors.pointHighlight,
                    highlightStrokeColor: customProperties.highlightStrokeColor || themeColors.pointStroke,
                    label: {
                        color: customProperties.labelColor || themeColors.text
                    }
                };
                break;
                
            case 'line':
                colorProperties = {
                    strokeColor: customProperties.strokeColor || themeColors.line,
                    highlightStrokeColor: customProperties.highlightStrokeColor || themeColors.lineHighlight,
                    label: {
                        color: customProperties.labelColor || themeColors.text
                    }
                };
                break;
                
            case 'functiongraph':
                colorProperties = {
                    strokeColor: customProperties.strokeColor || themeColors.functionGraph,
                    highlightStrokeColor: customProperties.highlightStrokeColor || themeColors.functionGraphHighlight
                };
                break;
                
            case 'circle':
                colorProperties = {
                    strokeColor: customProperties.strokeColor || themeColors.circle,
                    highlightStrokeColor: customProperties.highlightStrokeColor || themeColors.circleHighlight,
                    fillColor: customProperties.fillColor || themeColors.circle,
                    highlightFillColor: customProperties.highlightFillColor || themeColors.circleHighlight,
                    label: {
                        color: customProperties.labelColor || themeColors.text
                    }
                };
                break;
                
            case 'polygon':
                colorProperties = {
                    fillColor: customProperties.fillColor || themeColors.polygon,
                    highlightFillColor: customProperties.highlightFillColor || themeColors.polygonHighlight,
                    borders: {
                        strokeColor: customProperties.strokeColor || themeColors.polygon,
                        highlightStrokeColor: customProperties.highlightStrokeColor || themeColors.polygonHighlight
                    },
                    label: {
                        color: customProperties.labelColor || themeColors.text
                    }
                };
                break;
                
            case 'text':
                colorProperties = {
                    color: customProperties.color || themeColors.text
                };
                break;
                
            case 'slider':
                colorProperties = {
                    fillColor: customProperties.fillColor || themeColors.slider,
                    strokeColor: customProperties.strokeColor || themeColors.slider,
                    highlightFillColor: customProperties.highlightFillColor || themeColors.sliderHighlight,
                    highlightStrokeColor: customProperties.highlightStrokeColor || themeColors.sliderHighlight,
                    label: {
                        color: customProperties.labelColor || themeColors.text
                    }
                };
                break;
                
            default:
                // Default color handling for other element types
                colorProperties = {
                    strokeColor: customProperties.strokeColor || themeColors.line,
                    highlightStrokeColor: customProperties.highlightStrokeColor || themeColors.lineHighlight
                };
        }
        
        // Merge styles with custom properties and color properties
        // Custom properties override base styles, but don't override color properties unless explicitly set
        const mergedProperties = {
            ...baseStyle,
            ...customProperties,
            ...colorProperties
        };
        
        // Special handling for label properties
        if (baseStyle.label && (customProperties.label || colorProperties.label)) {
            mergedProperties.label = {
                ...baseStyle.label,
                ...(customProperties.label || {}),
                ...(colorProperties.label || {})
            };
        }
        
        // Create the element
        return board.create(type, data, mergedProperties);
    }
    
    /**
     * Toggle the theme of a board between light and dark
     * @param {Object} board - JSXGraph board
     * @returns {Object} - Updated board
     */
    function toggleBoardTheme(board) {
        const currentTheme = board.options.currentTheme || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        const colors = colorThemes[newTheme];
        
        // Update background
        board.containerObj.style.backgroundColor = colors.background;
        
        // Update UI elements
        board.uiElements.forEach(element => {
            if (element.type === 'infoBox') {
                if (newTheme === 'dark') {
                    element.element.classList.add('dark-theme');
                } else {
                    element.element.classList.remove('dark-theme');
                }
            }
        });
        
        // Update grid and axes
        if (board.hasGrid) {
            board.highlightGridX.setAttribute({strokeColor: colors.gridMajor});
            board.highlightGridY.setAttribute({strokeColor: colors.gridMajor});
            board.gridX.setAttribute({strokeColor: colors.grid});
            board.gridY.setAttribute({strokeColor: colors.grid});
        }
        
        if (board.defaultAxes) {
            board.defaultAxes.x.setAttribute({
                strokeColor: colors.axis,
                label: { color: colors.axisLabel }
            });
            board.defaultAxes.y.setAttribute({
                strokeColor: colors.axis,
                label: { color: colors.axisLabel }
            });
        }
        
        // Update all JSXGraph elements with new theme colors
        board.objectsList.forEach(element => {
            if (element.elType === 'point') {
                element.setAttribute({
                    fillColor: colors.point,
                    strokeColor: colors.pointStroke,
                    highlightFillColor: colors.pointHighlight,
                    highlightStrokeColor: colors.pointStroke
                });
            } else if (element.elType === 'line') {
                element.setAttribute({
                    strokeColor: colors.line,
                    highlightStrokeColor: colors.lineHighlight
                });
            } else if (element.elType === 'curve') {
                element.setAttribute({
                    strokeColor: colors.functionGraph,
                    highlightStrokeColor: colors.functionGraphHighlight
                });
            } else if (element.elType === 'circle') {
                element.setAttribute({
                    strokeColor: colors.circle,
                    highlightStrokeColor: colors.circleHighlight,
                    fillColor: colors.circle,
                    highlightFillColor: colors.circleHighlight
                });
            } else if (element.elType === 'polygon') {
                element.setAttribute({
                    fillColor: colors.polygon,
                    highlightFillColor: colors.polygonHighlight
                });
                
                if (element.borders) {
                    element.borders.forEach(border => {
                        border.setAttribute({
                            strokeColor: colors.polygon,
                            highlightStrokeColor: colors.polygonHighlight
                        });
                    });
                }
            } else if (element.elType === 'text') {
                element.setAttribute({
                    color: colors.text
                });
            }
        });
        
        // Update storage
        board.options.colors = colors;
        board.options.currentTheme = newTheme;
        
        return board;
    }
    
    //===========================================================================
    // UI COMPONENT SYSTEM
    //===========================================================================
    
    /**
     * Creates an info box element for displaying information about mathematical objects
     * @param {Element|string} container - Container element or ID of the container
     * @param {Object} options - Info box options
     * @returns {Object} - Info box object with update methods
     */
    function createInfoBox(container, options = {}) {
        const {
            id = 'infoBox-' + generateUniqueId(),
            className = 'info-box',
            position = 'top-left',
            title = '',
            initialContent = [],
            theme = 'light'
        } = options;
        
        // Handle container as string ID or DOM element
        const containerElement = typeof container === 'string' 
            ? document.getElementById(container) 
            : container;
            
        if (!containerElement) {
            console.error(`Container not found: ${container}`);
            return null;
        }
        
        // Create info box element
        const infoBox = document.createElement('div');
        infoBox.id = id;
        infoBox.className = className;
        
        // Add position class
        infoBox.classList.add(`${position.replace('-', '-')}`);
        
        // Add theme class
        if (theme === 'dark') {
            infoBox.classList.add('dark-theme');
        }
        
        // Set initial HTML
        let html = '';
        
        if (title) {
            html += `<div class="info-box-title">${title}</div>`;
        }
        
        // Add initial content
        initialContent.forEach(item => {
            html += `<div id="${item.id}">${item.content}</div>`;
        });
        
        infoBox.innerHTML = html;
        
        // Add to container
        containerElement.appendChild(infoBox);
        
        // Create info box object
        const infoBoxObj = {
            element: infoBox,
            type: 'infoBox',
            
            // Update an item by ID
            updateItem: function(id, content) {
                const item = infoBox.querySelector(`#${id}`);
                if (item) {
                    item.innerHTML = content;
                } else {
                    const newItem = document.createElement('div');
                    newItem.id = id;
                    newItem.innerHTML = content;
                    infoBox.appendChild(newItem);
                }
                return this;
            },
            
            // Update multiple items at once
            updateItems: function(items) {
                items.forEach(item => {
                    this.updateItem(item.id, item.content);
                });
                return this;
            },
            
            // Clear all items
            clear: function() {
                infoBox.innerHTML = title ? `<div class="info-box-title">${title}</div>` : '';
                return this;
            },
            
            // Set visibility
            setVisible: function(visible) {
                infoBox.style.display = visible ? 'block' : 'none';
                return this;
            }
        };
        
        return infoBoxObj;
    }
    
    /**
     * Creates an HTML-based slider control panel for interactive parameters
     * @param {Element|string} container - Container element or ID of the container
     * @param {Object} options - Slider panel options
     * @returns {Object} - Slider panel object with update methods
     */
    function createSliderPanel(container, options = {}) {
        const {
            id = 'sliderPanel-' + generateUniqueId(),
            className = 'slider-container',
            position = 'bottom-left',
            sliders = [],
            theme = 'light',
            onChange = () => {}
        } = options;
        
        // Handle container as string ID or DOM element
        const containerElement = typeof container === 'string' 
            ? document.getElementById(container) 
            : container;
            
        if (!containerElement) {
            console.error(`Container not found: ${container}`);
            return null;
        }
        
        // Create slider panel element
        const sliderPanel = document.createElement('div');
        sliderPanel.id = id;
        sliderPanel.className = className;
        
        // Add position class
        sliderPanel.classList.add(`${position.replace('-', '-')}`);
        
        // Add theme class
        if (theme === 'dark') {
            sliderPanel.classList.add('dark-theme');
        }
        
        // Track slider values
        const sliderValues = {};
        
        // Create sliders
        sliders.forEach(slider => {
            const { 
                name, 
                label = name, 
                min = -5, 
                max = 5, 
                step = 0.1, 
                initial = 0,
                precision = 1 
            } = slider;
            
            // Set initial value
            sliderValues[name] = initial;
            
            // Create slider row
            const sliderRow = document.createElement('div');
            sliderRow.className = 'slider-row';
            
            // Create label
            const labelEl = document.createElement('div');
            labelEl.className = 'slider-label';
            labelEl.textContent = label + ':';
            
            // Create input
            const input = document.createElement('input');
            input.type = 'range';
            input.id = `${id}-${name}Slider`;
            input.className = 'slider-input';
            input.min = min;
            input.max = max;
            input.step = step;
            input.value = initial;
            
            // Create value display
            const valueEl = document.createElement('div');
            valueEl.id = `${id}-${name}Value`;
            valueEl.className = 'slider-value';
            valueEl.textContent = initial.toFixed(precision);
            
            // Add event listener
            input.addEventListener('input', function(e) {
                const value = parseFloat(e.target.value);
                sliderValues[name] = value;
                valueEl.textContent = value.toFixed(precision);
                
                // Call onChange with all current values
                onChange(sliderValues);
            });
            
            // Assemble row
            sliderRow.appendChild(labelEl);
            sliderRow.appendChild(input);
            sliderRow.appendChild(valueEl);
            
            // Add to panel
            sliderPanel.appendChild(sliderRow);
        });
        
        // Prevent event propagation from sliders to prevent panning
        sliderPanel.addEventListener('touchstart', function(e) {
            e.stopPropagation();
        }, true);
        
        sliderPanel.addEventListener('touchmove', function(e) {
            e.stopPropagation();
        }, true);
        
        // Add to container
        containerElement.appendChild(sliderPanel);
        
        // Create slider panel object
        const sliderPanelObj = {
            element: sliderPanel,
            type: 'sliderPanel',
            values: sliderValues,
            
            // Update a slider value
            setValue: function(name, value) {
                if (!(name in this.values)) {
                    console.error(`Slider "${name}" does not exist.`);
                    return this;
                }
                
                const slider = document.getElementById(`${id}-${name}Slider`);
                const valueEl = document.getElementById(`${id}-${name}Value`);
                
                if (slider && valueEl) {
                    // Find the slider definition to get precision
                    const sliderDef = sliders.find(s => s.name === name);
                    const precision = sliderDef ? sliderDef.precision || 1 : 1;
                    
                    this.values[name] = value;
                    slider.value = value;
                    valueEl.textContent = value.toFixed(precision);
                }
                
                return this;
            },
            
            // Get a slider value
            getValue: function(name) {
                return this.values[name];
            },
            
            // Get all slider values
            getValues: function() {
                return { ...this.values };
            },
            
            // Set visibility
            setVisible: function(visible) {
                sliderPanel.style.display = visible ? 'block' : 'none';
                return this;
            }
        };
        
        return sliderPanelObj;
    }
    
    /**
     * Creates a control button panel for common operations (e.g., reset view, toggle theme)
     * @param {Element|string} container - Container element or ID of the container
     * @param {Object} options - Button panel options
     * @returns {Object} - Button panel object
     */
    function createButtonPanel(container, options = {}) {
        const {
            id = 'buttonPanel-' + generateUniqueId(),
            className = 'control-panel',
            position = 'top-right',
            buttons = [],
            theme = 'light'
        } = options;
        
        // Handle container as string ID or DOM element
        const containerElement = typeof container === 'string' 
            ? document.getElementById(container) 
            : container;
            
        if (!containerElement) {
            console.error(`Container not found: ${container}`);
            return null;
        }
        
        // Create button panel element
        const buttonPanel = document.createElement('div');
        buttonPanel.id = id;
        buttonPanel.className = className;
        
        // Add position class
        buttonPanel.classList.add(`${position.replace('-', '-')}`);
        
        // Add theme class
        if (theme === 'dark') {
            buttonPanel.classList.add('dark-theme');
        }
        
        // Create buttons
        buttons.forEach(button => {
            const { id: btnId, label, onClick } = button;
            
            const buttonEl = document.createElement('button');
            buttonEl.id = btnId;
            buttonEl.className = 'control-btn';
            buttonEl.textContent = label;
            
            buttonEl.addEventListener('click', onClick);
            
            buttonPanel.appendChild(buttonEl);
        });
        
        // Add to container
        containerElement.appendChild(buttonPanel);
        
        // Create button panel object
        const buttonPanelObj = {
            element: buttonPanel,
            type: 'buttonPanel',
            
            // Add a new button
            addButton: function(button) {
                const { id: btnId, label, onClick } = button;
                
                const buttonEl = document.createElement('button');
                buttonEl.id = btnId;
                buttonEl.className = 'control-btn';
                buttonEl.textContent = label;
                
                buttonEl.addEventListener('click', onClick);
                
                buttonPanel.appendChild(buttonEl);
                
                return this;
            },
            
            // Remove a button by ID
            removeButton: function(id) {
                const button = buttonPanel.querySelector(`#${id}`);
                if (button) {
                    buttonPanel.removeChild(button);
                }
                
                return this;
            },
            
            // Set visibility
            setVisible: function(visible) {
                buttonPanel.style.display = visible ? 'block' : 'none';
                return this;
            }
        };
        
        return buttonPanelObj;
    }
    
    //===========================================================================
    // MATHEMATICAL OBJECT CREATORS
    //===========================================================================
    
    /**
     * Creates a function graph on the board
     * @param {Object} board - JSXGraph board
     * @param {Function|Array} func - Function or array [func, min, max]
     * @param {Object} properties - Custom properties
     * @returns {Object} - Created function graph
     */
    function createFunctionGraph(board, func, properties = {}) {
        let fn, min, max;
        
        if (Array.isArray(func)) {
            [fn, min, max] = func;
        } else {
            fn = func;
            min = -10;
            max = 10;
        }
        
        return createElement(board, 'functiongraph', [fn, min, max], properties);
    }
    
    /**
     * Creates a parametric curve on the board
     * @param {Object} board - JSXGraph board
     * @param {Function} xFunc - X component function
     * @param {Function} yFunc - Y component function
     * @param {Array} tRange - Parameter range [min, max]
     * @param {Object} properties - Custom properties
     * @returns {Object} - Created curve
     */
    function createParametricCurve(board, xFunc, yFunc, tRange = [0, 1], properties = {}) {
        return createElement(board, 'curve', [xFunc, yFunc, tRange[0], tRange[1]], properties);
    }
    
    /**
     * Creates a polygon on the board
     * @param {Object} board - JSXGraph board
     * @param {Array} points - Array of points [[x1,y1], [x2,y2], ...]
     * @param {Object} properties - Custom properties
     * @returns {Object} - Created polygon
     */
    function createPolygon(board, points, properties = {}) {
        return createElement(board, 'polygon', points, properties);
    }
    
    /**
     * Creates a circle on the board
     * @param {Object} board - JSXGraph board
     * @param {Array|Object} centerAndPoint - [center, point] or {center: [x,y], radius: r}
     * @param {Object} properties - Custom properties
     * @returns {Object} - Created circle
     */
    function createCircle(board, centerAndPoint, properties = {}) {
        if (centerAndPoint.center && centerAndPoint.radius !== undefined) {
            return createElement(board, 'circle', [centerAndPoint.center, centerAndPoint.radius], properties);
        } else {
            return createElement(board, 'circle', centerAndPoint, properties);
        }
    }
    
    //===========================================================================
    // HIGH-LEVEL GRAPH BUILDER
    //===========================================================================
    
    /**
     * Creates a JSXGraph visualization from a description object
     * @param {string} containerId - ID of the container element
     * @param {Object} description - Graph description object
     * @returns {Object} - Created board with additional methods
     */
    function createGraphFromDescription(containerId, description) {
        const {
            boundingBox = [-5, 5, 5, -5],
            theme = 'light',
            useSequentialColors = false,
            showNavigation = false,
            showGrid = true,
            showAxes = true,
            elements = [],
            sliders = [],
            infoBoxes = [],
            buttons = [
                { id: 'resetView', label: 'Reset View' },
                { id: 'toggleTheme', label: 'Toggle Theme' }
            ]
        } = description;
        
        // Reset sequential color index if needed
        if (useSequentialColors) {
            getNextSequentialColor(true);
        }
        
        // Create container structure if it doesn't exist
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Container with ID "${containerId}" not found.`);
            return null;
        }
        
        // Create the graph container
        const graphContainer = document.createElement('div');
        graphContainer.id = `${containerId}-graph-container`;
        graphContainer.className = 'graph-container';
        container.appendChild(graphContainer);
        
        // Create the graph header
        const graphHeader = document.createElement('div');
        graphHeader.className = 'graph-header';
        
        // Add title if provided
        if (description.title) {
            const graphTitle = document.createElement('h3');
            graphTitle.className = 'graph-title';
            graphTitle.textContent = description.title;
            graphHeader.appendChild(graphTitle);
        }
        
        // Add buttons container
        const controlsDiv = document.createElement('div');
        controlsDiv.className = 'controls';
        controlsDiv.id = `${containerId}-controls`;
        graphHeader.appendChild(controlsDiv);
        
        graphContainer.appendChild(graphHeader);
        
        // Create the graph box
        const jxgboxDiv = document.createElement('div');
        jxgboxDiv.id = `${containerId}-box`;
        jxgboxDiv.className = 'jxgbox';
        graphContainer.appendChild(jxgboxDiv);
        
        // Create the board
        const boardConfig = createBoardConfig({
            colors: colorThemes[theme],
            boundingBox,
            showNavigation,
            showGrid,
            showAxes
        });
        
        const board = JXG.JSXGraph.initBoard(`${containerId}-box`, boardConfig);
        
        // Store options
        board.options.colors = colorThemes[theme];
        board.options.currentTheme = theme;
        board.options.origBoundingBox = [...boundingBox];
        
        // Store parameters object for easier access to dynamic values
        board.params = {};
        
        // Store UI elements
        board.uiElements = [];
        
        // Create control buttons
        const buttonPanel = createButtonPanel(controlsDiv, {
            theme,
            buttons: buttons.map(btn => {
                if (btn.id === 'resetView') {
                    return {
                        id: 'resetView',
                        label: btn.label || 'Reset View',
                        onClick: function() {
                            board.setBoundingBox(board.options.origBoundingBox);
                            board.update();
                        }
                    };
                } else if (btn.id === 'toggleTheme') {
                    return {
                        id: 'toggleTheme',
                        label: btn.label || 'Toggle Theme',
                        onClick: function() {
                            toggleBoardTheme(board);
                        }
                    };
                } else {
                    return btn;
                }
            })
        });
        
        board.uiElements.push(buttonPanel);
        
        // Create info boxes
        board.infoBoxes = infoBoxes.map(infoBox => {
            const infoBoxObj = createInfoBox(graphContainer, {
                ...infoBox,
                theme
            });
            
            board.uiElements.push(infoBoxObj);
            return infoBoxObj;
        });
        
        // Create slider panels and initialize parameters
        board.sliderPanels = sliders.map(sliderPanel => {
            // Setup onChange wrapper function
            const onChangeWrapper = function(values) {
                // Update params object with all slider values
                Object.assign(board.params, values);
                
                // Call the original onChange handler if provided
                if (sliderPanel.onChange) {
                    sliderPanel.onChange(values, board);
                }
                
                // Update the board
                board.update();
            };
            
            // Create the slider panel
            const sliderPanelObj = createSliderPanel(graphContainer, {
                ...sliderPanel,
                theme,
                onChange: onChangeWrapper
            });
            
            // Update params with initial slider values
            Object.assign(board.params, sliderPanelObj.values);
            
            board.uiElements.push(sliderPanelObj);
            return sliderPanelObj;
        });
        
        // Create elements
        board.elements = elements.map(element => {
            const { type, data, properties = {} } = element;
            
            // Use sequential color if enabled and color not specified
            if (useSequentialColors && 
                !properties.strokeColor && 
                !properties.fillColor &&
                !properties.color) {
                
                const color = getNextSequentialColor();
                
                if (type === 'point') {
                    properties.fillColor = color;
                } else if (type === 'text') {
                    properties.color = color;
                } else {
                    properties.strokeColor = color;
                }
            }
            
            return createElement(board, type, data, properties);
        });
        
        // Add helper methods to the board
        board.resetView = function() {
            this.setBoundingBox(this.options.origBoundingBox);
            this.update();
            return this;
        };
        
        board.toggleTheme = function() {
            toggleBoardTheme(this);
            return this;
        };
        
        // Ensure touch events are properly handled
        const jxgboxEl = document.getElementById(`${containerId}-box`);
        if (jxgboxEl) {
            JXG.addEvent(jxgboxEl, 'touchstart', function(e) {
                // Only prevent default if we have multiple touches
                if (e.touches.length >= 2) {
                    e.preventDefault();
                }
            }, false);
        }
        
        return board;
    }
    
    //===========================================================================
    // SPECIALIZED MATHEMATICAL VISUALIZATION CREATORS
    //===========================================================================
    
    /**
     * Creates a quadratic function visualizer (y = ax² + bx + c)
     * @param {string} containerId - ID of the container element
     * @param {Object} options - Visualization options
     * @returns {Object} - Created board
     */
    function createQuadraticVisualizer(containerId, options = {}) {
        const {
            boundingBox = [-6, 10, 6, -6],
            theme = 'light',
            initialValues = { a: 1, b: 0, c: 0 },
            title = 'Parabola: y = ax² + bx + c'
        } = options;
        
        // Define parameter values that will be used for the quadratic function
        const params = { ...initialValues };
        
        // Create the quadratic function
        const quadraticFunction = function(x) {
            return params.a * x * x + params.b * x + params.c;
        };
        
        // Format equation text
        const formatEquation = function() {
            let equation = 'y = ';
            const a = params.a;
            const b = params.b;
            const c = params.c;
            const aRounded = a.toFixed(1);
            const bRounded = b.toFixed(1);
            const cRounded = c.toFixed(1);
            
            // Handle a term
            if (aRounded === '0.0') {
                // Skip the x² term if a = 0
            } else if (aRounded === '1.0') {
                equation += 'x²';
            } else if (aRounded === '-1.0') {
                equation += '-x²';
            } else {
                equation += aRounded + 'x²';
            }
            
            // Handle b term
            if (bRounded === '0.0') {
                // Skip the x term if b = 0
            } else {
                if (aRounded !== '0.0') {
                    // Add + or - sign based on b value
                    equation += b >= 0 ? ' + ' : ' - ';
                    // Use absolute value after the sign
                    equation += Math.abs(b) === 1 ? 'x' : Math.abs(b).toFixed(1) + 'x';
                } else {
                    // If a = 0, then just add the b term without a sign
                    equation += b === 1 ? 'x' : b === -1 ? '-x' : bRounded + 'x';
                }
            }
            
            // Handle c term
            if (cRounded === '0.0') {
                // Skip the constant term if c = 0 and we already have other terms
                if (aRounded === '0.0' && bRounded === '0.0') {
                    equation += '0';
                }
            } else {
                // Only add + sign if there are previous terms
                if (aRounded !== '0.0' || bRounded !== '0.0') {
                    equation += c >= 0 ? ' + ' : ' - ';
                    equation += Math.abs(c).toFixed(1);
                } else {
                    // If a = 0 and b = 0, then just add c without a sign
                    equation += cRounded;
                }
            }
            
            return equation;
        };
        
        // Calculate vertex coordinates
        const calculateVertex = function() {
            const a = params.a;
            const b = params.b;
            const c = params.c;
            
            // If a is close to zero, it's effectively a line, not a parabola
            if (Math.abs(a) < 0.01) {
                return null;
            }
            
            const vx = -b / (2 * a);
            const vy = a * vx * vx + b * vx + c;
            
            return { x: vx, y: vy };
        };
        
        // Create the graph description
        const graphDescription = {
            title,
            boundingBox,
            theme,
            elements: [
                {
                    type: 'functiongraph',
                    data: [quadraticFunction, -10, 10],
                    properties: {
                        name: 'Parabola'
                    }
                },
                {
                    type: 'point',
                    data: [
                        function() { 
                            const vertex = calculateVertex();
                            return vertex ? vertex.x : 0; 
                        }, 
                        function() { 
                            const vertex = calculateVertex();
                            return vertex ? vertex.y : 0; 
                        }
                    ],
                    properties: {
                        name: 'V',
                        size: 4,
                        visible: function() { return Math.abs(params.a) >= 0.01; }
                    }
                },
                {
                    type: 'line',
                    data: [
                        [function() { 
                            const vertex = calculateVertex();
                            return vertex ? vertex.x : 0; 
                        }, -10],
                        [function() { 
                            const vertex = calculateVertex();
                            return vertex ? vertex.x : 0; 
                        }, 10]
                    ],
                    properties: {
                        dash: 2,
                        strokeWidth: 1,
                        visible: function() { return Math.abs(params.a) >= 0.01; }
                    }
                }
            ],
            infoBoxes: [
                {
                    id: 'equationInfo',
                    className: 'info-box equation-info',
                    position: 'top-left',
                    initialContent: [
                        { id: 'equation', content: formatEquation() },
                        { id: 'direction', content: 'Opens upward' },
                        { id: 'vertex', content: 'Vertex: (0.00, 0.00)' },
                        { id: 'axis', content: 'Axis: x = 0.00' }
                    ]
                }
            ],
            sliders: [
                {
                    id: 'sliderContainer',
                    className: 'slider-container',
                    position: 'bottom-left',
                    sliders: [
                        { name: 'a', label: 'a', min: -5, max: 5, step: 0.1, initial: params.a, precision: 1 },
                        { name: 'b', label: 'b', min: -5, max: 5, step: 0.1, initial: params.b, precision: 1 },
                        { name: 'c', label: 'c', min: -5, max: 5, step: 0.1, initial: params.c, precision: 1 }
                    ],
                    onChange: function(values, board) {
                        // Update parameters from slider values
                        params.a = values.a;
                        params.b = values.b;
                        params.c = values.c;
                        
                        // Update equation info box
                        const infoBox = board.infoBoxes[0];
                        
                        infoBox.updateItem('equation', formatEquation());
                        
                        // Update direction display
                        if (Math.abs(params.a) < 0.01) {
                            infoBox.updateItem('direction', 'Linear function (a ≈ 0)');
                        } else {
                            infoBox.updateItem('direction', 'Opens ' + (params.a > 0 ? 'upward' : 'downward'));
                        }
                        
                        // Update vertex display
                        const vertex = calculateVertex();
                        if (vertex) {
                            infoBox.updateItem('vertex', `Vertex: (${vertex.x.toFixed(2)}, ${vertex.y.toFixed(2)})`);
                            infoBox.updateItem('axis', `Axis: x = ${vertex.x.toFixed(2)}`);
                        }
                    }
                }
            ]
        };
        
        // Create the graph
        const board = createGraphFromDescription(containerId, graphDescription);
        
        // Store parameters in the board
        board.params = params;
        
        return board;
    }
    
    /**
     * Creates a trigonometric function visualizer (y = a*sin(b*x + c) + d)
     * @param {string} containerId - ID of the container element
     * @param {Object} options - Visualization options
     * @returns {Object} - Created board
     */
    function createTrigVisualizer(containerId, options = {}) {
        const {
            boundingBox = [-6, 6, 6, -6],
            theme = 'light',
            initialValues = { a: 1, b: 1, c: 0, d: 0 },
            function: trigFunction = 'sin',
            title = `${trigFunction.charAt(0).toUpperCase() + trigFunction.slice(1)} Function: y = a*${trigFunction}(b*x + c) + d`
        } = options;
        
        // Define parameter values
        const params = { ...initialValues };
        
        // Create the function based on type
        const createFunction = function() {
            if (trigFunction === 'sin') {
                return function(x) { return params.a * Math.sin(params.b * x + params.c) + params.d; };
            } else if (trigFunction === 'cos') {
                return function(x) { return params.a * Math.cos(params.b * x + params.c) + params.d; };
            } else if (trigFunction === 'tan') {
                return function(x) { return params.a * Math.tan(params.b * x + params.c) + params.d; };
            } else {
                return function(x) { return params.a * Math.sin(params.b * x + params.c) + params.d; };
            }
        };
        
        // Format equation text
        const formatEquation = function() {
            const a = params.a;
            const b = params.b;
            const c = params.c;
            const d = params.d;
            
            let equation = 'y = ';
            
            if (a === 1) {
                equation += `${trigFunction}(`;
            } else if (a === -1) {
                equation += `-${trigFunction}(`;
            } else {
                equation += `${a.toFixed(1)}*${trigFunction}(`;
            }
            
            if (b === 1) {
                equation += 'x';
            } else if (b === -1) {
                equation += '-x';
            } else {
                equation += `${b.toFixed(1)}*x`;
            }
            
            if (c !== 0) {
                equation += c > 0 ? ` + ${c.toFixed(1)}` : ` - ${Math.abs(c).toFixed(1)}`;
            }
            
            equation += ')';
            
            if (d !== 0) {
                equation += d > 0 ? ` + ${d.toFixed(1)}` : ` - ${Math.abs(d).toFixed(1)}`;
            }
            
            return equation;
        };
        
        // Create the graph description
        const graphDescription = {
            title,
            boundingBox,
            theme,
            elements: [
                {
                    type: 'functiongraph',
                    data: [createFunction(), -10, 10],
                    properties: {
                        name: `${trigFunction} curve`
                    }
                }
            ],
            infoBoxes: [
                {
                    id: 'equationInfo',
                    className: 'info-box equation-info',
                    position: 'top-left',
                    initialContent: [
                        { id: 'equation', content: formatEquation() },
                        { id: 'amplitude', content: `Amplitude: ${Math.abs(params.a).toFixed(2)}` },
                        { id: 'period', content: `Period: ${Math.abs(params.b) < 0.01 ? 'Infinity' : (2 * Math.PI / Math.abs(params.b)).toFixed(2)}` },
                        { id: 'phase', content: `Phase Shift: ${(-params.c / params.b).toFixed(2)}` },
                        { id: 'verticalShift', content: `Vertical Shift: ${params.d.toFixed(2)}` }
                    ]
                }
            ],
            sliders: [
                {
                    id: 'sliderContainer',
                    className: 'slider-container',
                    position: 'bottom-left',
                    sliders: [
                        { name: 'a', label: 'a', min: -5, max: 5, step: 0.1, initial: params.a, precision: 1 },
                        { name: 'b', label: 'b', min: -5, max: 5, step: 0.1, initial: params.b, precision: 1 },
                        { name: 'c', label: 'c', min: -5, max: 5, step: 0.1, initial: params.c, precision: 1 },
                        { name: 'd', label: 'd', min: -5, max: 5, step: 0.1, initial: params.d, precision: 1 }
                    ],
                    onChange: function(values, board) {
                        // Update parameters
                        params.a = values.a;
                        params.b = values.b;
                        params.c = values.c;
                        params.d = values.d;
                        
                        // Update the function
                        board.elements[0].Y = createFunction();
                        
                        // Update equation info box
                        const infoBox = board.infoBoxes[0];
                        
                        infoBox.updateItem('equation', formatEquation());
                        infoBox.updateItem('amplitude', `Amplitude: ${Math.abs(params.a).toFixed(2)}`);
                        infoBox.updateItem('period', `Period: ${Math.abs(params.b) < 0.01 ? 'Infinity' : (2 * Math.PI / Math.abs(params.b)).toFixed(2)}`);
                        infoBox.updateItem('phase', `Phase Shift: ${params.b === 0 ? 'Undefined' : (-params.c / params.b).toFixed(2)}`);
                        infoBox.updateItem('verticalShift', `Vertical Shift: ${params.d.toFixed(2)}`);
                    }
                }
            ]
        };
        
        // Create the graph
        const board = createGraphFromDescription(containerId, graphDescription);
        
        // Store parameters in the board
        board.params = params;
        
        return board;
    }
    
    /**
     * Creates a circle visualizer ((x-h)² + (y-k)² = r²)
     * @param {string} containerId - ID of the container element
     * @param {Object} options - Visualization options
     * @returns {Object} - Created board
     */
    function createCircleVisualizer(containerId, options = {}) {
        const {
            boundingBox = [-6, 6, 6, -6],
            theme = 'light',
            initialValues = { h: 0, k: 0, r: 2 },
            title = 'Circle: (x-h)² + (y-k)² = r²'
        } = options;
        
        // Define parameter values
        const params = { ...initialValues };
        
        // Format equation text
        const formatEquation = function() {
            const h = params.h;
            const k = params.k;
            const r = params.r;
            
            let equation = '';
            
            if (h === 0 && k === 0) {
                equation = `x² + y² = ${r.toFixed(1)}²`;
            } else {
                equation = '(x';
                equation += h === 0 ? '' : h > 0 ? ` - ${h.toFixed(1)}` : ` + ${Math.abs(h).toFixed(1)}`;
                equation += ')² + (y';
                equation += k === 0 ? '' : k > 0 ? ` - ${k.toFixed(1)}` : ` + ${Math.abs(k).toFixed(1)}`;
                equation += `)² = ${r.toFixed(1)}²`;
            }
            
            return equation;
        };
        
        // Create the graph description
        const graphDescription = {
            title,
            boundingBox,
            theme,
            elements: [
                {
                    type: 'circle',
                    data: [
                        [function() { return params.h; }, function() { return params.k; }], 
                        function() { return params.r; }
                    ],
                    properties: {
                        name: 'Circle',
                        fillOpacity: 0.1
                    }
                },
                {
                    type: 'point',
                    data: [function() { return params.h; }, function() { return params.k; }],
                    properties: {
                        name: 'Center',
                        size: 4
                    }
                }
            ],
            infoBoxes: [
                {
                    id: 'equationInfo',
                    className: 'info-box equation-info',
                    position: 'top-left',
                    initialContent: [
                        { id: 'equation', content: formatEquation() },
                        { id: 'center', content: `Center: (${params.h.toFixed(2)}, ${params.k.toFixed(2)})` },
                        { id: 'radius', content: `Radius: ${params.r.toFixed(2)}` },
                        { id: 'area', content: `Area: ${(Math.PI * params.r * params.r).toFixed(2)}` },
                        { id: 'circumference', content: `Circumference: ${(2 * Math.PI * params.r).toFixed(2)}` }
                    ]
                }
            ],
            sliders: [
                {
                    id: 'sliderContainer',
                    className: 'slider-container',
                    position: 'bottom-left',
                    sliders: [
                        { name: 'h', label: 'h', min: -5, max: 5, step: 0.1, initial: params.h, precision: 1 },
                        { name: 'k', label: 'k', min: -5, max: 5, step: 0.1, initial: params.k, precision: 1 },
                        { name: 'r', label: 'r', min: 0.1, max: 5, step: 0.1, initial: params.r, precision: 1 }
                    ],
                    onChange: function(values, board) {
                        // Update parameters
                        params.h = values.h;
                        params.k = values.k;
                        params.r = values.r;
                        
                        // Update equation info box
                        const infoBox = board.infoBoxes[0];
                        
                        infoBox.updateItem('equation', formatEquation());
                        infoBox.updateItem('center', `Center: (${params.h.toFixed(2)}, ${params.k.toFixed(2)})`);
                        infoBox.updateItem('radius', `Radius: ${params.r.toFixed(2)}`);
                        infoBox.updateItem('area', `Area: ${(Math.PI * params.r * params.r).toFixed(2)}`);
                        infoBox.updateItem('circumference', `Circumference: ${(2 * Math.PI * params.r).toFixed(2)}`);
                    }
                }
            ]
        };
        
        // Create the graph
        const board = createGraphFromDescription(containerId, graphDescription);
        
        // Store parameters in the board
        board.params = params;
        
        return board;
    }
    
    /**
     * Creates a linear function visualizer (y = mx + b)
     * @param {string} containerId - ID of the container element
     * @param {Object} options - Visualization options
     * @returns {Object} - Created board
     */
    function createLinearVisualizer(containerId, options = {}) {
        const {
            boundingBox = [-6, 6, 6, -6],
            theme = 'light',
            initialValues = { m: 1, b: 0 },
            title = 'Linear Function: y = mx + b'
        } = options;
        
        // Define parameter values
        const params = { ...initialValues };
        
        // Create the linear function
        const linearFunction = function(x) {
            return params.m * x + params.b;
        };
        
        // Format equation text
        const formatEquation = function() {
            const m = params.m;
            const b = params.b;
            
            let equation = 'y = ';
            
            if (m === 0) {
                equation += b.toFixed(1);
            } else if (m === 1) {
                equation += 'x';
                equation += b === 0 ? '' : b > 0 ? ` + ${b.toFixed(1)}` : ` - ${Math.abs(b).toFixed(1)}`;
            } else if (m === -1) {
                equation += '-x';
                equation += b === 0 ? '' : b > 0 ? ` + ${b.toFixed(1)}` : ` - ${Math.abs(b).toFixed(1)}`;
            } else {
                equation += `${m.toFixed(1)}x`;
                equation += b === 0 ? '' : b > 0 ? ` + ${b.toFixed(1)}` : ` - ${Math.abs(b).toFixed(1)}`;
            }
            
            return equation;
        };
        
        // Create the graph description
        const graphDescription = {
            title,
            boundingBox,
            theme,
            elements: [
                {
                    type: 'functiongraph',
                    data: [linearFunction, -10, 10],
                    properties: {
                        name: 'Line'
                    }
                },
                {
                    type: 'point',
                    data: [0, function() { return params.b; }],
                    properties: {
                        name: 'y-intercept',
                        size: 4
                    }
                },
                {
                    type: 'point',
                    data: [function() { return params.m === 0 ? 0 : -params.b / params.m; }, 0],
                    properties: {
                        name: 'x-intercept',
                        size: 4,
                        visible: function() { return params.m !== 0; }
                    }
                }
            ],
            infoBoxes: [
                {
                    id: 'equationInfo',
                    className: 'info-box equation-info',
                    position: 'top-left',
                    initialContent: [
                        { id: 'equation', content: formatEquation() },
                        { id: 'slope', content: `Slope: ${params.m.toFixed(2)}` },
                        { id: 'yIntercept', content: `y-intercept: ${params.b.toFixed(2)}` },
                        { id: 'xIntercept', content: params.m === 0 ? 'x-intercept: None' : `x-intercept: ${(-params.b / params.m).toFixed(2)}` },
                        { id: 'angle', content: `Angle with x-axis: ${(Math.atan(params.m) * 180 / Math.PI).toFixed(2)}°` }
                    ]
                }
            ],
            sliders: [
                {
                    id: 'sliderContainer',
                    className: 'slider-container',
                    position: 'bottom-left',
                    sliders: [
                        { name: 'm', label: 'm', min: -5, max: 5, step: 0.1, initial: params.m, precision: 1 },
                        { name: 'b', label: 'b', min: -5, max: 5, step: 0.1, initial: params.b, precision: 1 }
                    ],
                    onChange: function(values, board) {
                        // Update parameters
                        params.m = values.m;
                        params.b = values.b;
                        
                        // Update equation info box
                        const infoBox = board.infoBoxes[0];
                        
                        infoBox.updateItem('equation', formatEquation());
                        infoBox.updateItem('slope', `Slope: ${params.m.toFixed(2)}`);
                        infoBox.updateItem('yIntercept', `y-intercept: ${params.b.toFixed(2)}`);
                        infoBox.updateItem('xIntercept', params.m === 0 ? 'x-intercept: None' : `x-intercept: ${(-params.b / params.m).toFixed(2)}`);
                        infoBox.updateItem('angle', `Angle with x-axis: ${(Math.atan(params.m) * 180 / Math.PI).toFixed(2)}°`);
                    }
                }
            ]
        };
        
        // Create the graph
        const board = createGraphFromDescription(containerId, graphDescription);
        
        // Store parameters in the board
        board.params = params;
        
        return board;
    }
    
    //===========================================================================
    // MODULE EXPORTS
    //===========================================================================
    
    return {
        // Core board management
        createBoardConfig,
        createElement,
        toggleBoardTheme,
        
        // UI components
        createInfoBox,
        createSliderPanel,
        createButtonPanel,
        
        // Mathematical object creators
        createFunctionGraph,
        createParametricCurve,
        createPolygon,
        createCircle,
        
        // High-level graph builder
        createGraphFromDescription,
        
        // Specialized visualizers
        createQuadraticVisualizer,
        createTrigVisualizer,
        createCircleVisualizer,
        createLinearVisualizer,
        
        // Themes and styles
        colorThemes,
        elementStyles,
        
        // Utility functions
        getNextSequentialColor
    };
})();

/**
 * CSS styles for the modular JSXGraph components
 */
const JSXGraphModuleStyles = `
body {
    font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background-color: #f7f9fc;
    margin: 0;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 100vh;
}

h1, h2 {
    color: #2d3748;
    text-align: center;
}

.container {
    width: 100%;
    max-width: 1200px;
    display: flex;
    flex-direction: column;
    gap: 30px;
}

.graph-container {
    width: 100%;
    border-radius: 10px;
    background-color: white;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    position: relative;
    margin-bottom: 30px;
}

.graph-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}

.graph-title {
    font-size: 18px;
    font-weight: 600;
    color: #2d3748;
    margin: 0;
}

.controls {
    display: flex;
    gap: 10px;
}

.control-btn {
    background-color: #f1f5f9;
    border: none;
    padding: 6px 12px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    color: #4a5568;
    transition: all 0.2s ease;
}

.control-btn:hover {
    background-color: #e2e8f0;
}

.control-btn:active {
    background-color: #cbd5e1;
}

.jxgbox {
    width: 100%;
    height: 450px;
    border-radius: 8px;
    touch-action: none;
}

.info-box {
    background-color: rgba(255, 255, 255, 0.9);
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 10px 15px;
    font-size: 16px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    max-width: 300px;
    position: absolute;
    z-index: 10;
}

.info-box-title {
    font-weight: bold;
    margin-bottom: 8px;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 5px;
}

.top-left {
    top: 65px;
    left: 20px;
}

.top-right {
    top: 65px;
    right: 20px;
}

.bottom-left {
    bottom: 20px;
    left: 20px;
}

.bottom-right {
    bottom: 20px;
    right: 20px;
}

.slider-container {
    position: absolute;
    z-index: 10;
    background-color: rgba(255, 255, 255, 0.85);
    padding: 10px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    user-select: none;
    touch-action: none;
}

.slider-row {
    display: flex;
    align-items: center;
    margin-bottom: 8px;
}

.slider-row:last-child {
    margin-bottom: 0;
}

.slider-label {
    width: 20px;
    font-weight: 600;
    margin-right: 10px;
}

.slider-input {
    flex-grow: 1;
    width: 120px;
}

.slider-value {
    width: 40px;
    text-align: right;
    margin-left: 10px;
}

/* Dark Theme Overrides */
.dark-theme {
    background-color: rgba(30, 39, 46, 0.85);
    border-color: #2c3e50;
    color: #ecf0f1;
}

.dark-theme .slider-label,
.dark-theme .slider-value,
.dark-theme .info-box-title {
    color: #ecf0f1;
}

.dark-theme .info-box-title {
    border-bottom-color: #2c3e50;
}

@media (max-width: 768px) {
    .jxgbox {
        height: 350px;
    }
    
    .container {
        padding: 10px;
    }
}`;



// Nuclear option: Force fix axis numbers function
function forceFixAxisNumbers() {
    // Find all JSXGraph containers
    const jxgBoxes = document.querySelectorAll('.jxgbox');
    
    jxgBoxes.forEach(box => {
        const bgColor = window.getComputedStyle(box).backgroundColor;
        
        // Determine if background is dark
        const isDark = bgColor.includes('rgb(0, 0, 0)') || 
                      bgColor.includes('0, 0, 0') ||
                      bgColor.includes('30, 39, 46') ||
                      box.style.backgroundColor === '#000000' ||
                      box.style.backgroundColor === '#1e272e';
        
        // Find all text elements and force their color
        const textElements = box.querySelectorAll('text');
        textElements.forEach(text => {
            if (isDark) {
                text.setAttribute('fill', '#ffffff');
                text.style.fill = '#ffffff';
                text.style.color = '#ffffff';
            } else {
                text.setAttribute('fill', '#333333');
                text.style.fill = '#333333';
                text.style.color = '#333333';
            }
        });
    });
}

// Run the fix every time someone clicks anywhere (aggressive approach)
document.addEventListener('click', () => {
    setTimeout(forceFixAxisNumbers, 200);
});

// Also run it on page load and periodically
document.addEventListener('DOMContentLoaded', forceFixAxisNumbers);
setInterval(forceFixAxisNumbers, 2000); // Every 2 seconds