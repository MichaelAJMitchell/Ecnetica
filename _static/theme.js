// Ensure the DOM is fully loaded before running scripts
document.addEventListener('DOMContentLoaded', function() {
    createEnhancedThemeToggle();
    createCourseNavigator();
    createInteractiveToolsFinder();
    autoHideSidebarForInteractive();
});

// dark mode and light mode theme toggle
// with a listener for system theme changes
function createEnhancedThemeToggle() {
    // Find the navbar end section
    const navbarEnd = document.querySelector('.navbar-nav.navbar-end') ||
                     document.querySelector('.navbar-header-items__end') ||
                     document.querySelector('nav .navbar-nav:last-child');

    if (!navbarEnd) {
        console.log('Could not find navbar end section');
        return;
    }

    // Detect browser's preferred theme
    const getPreferredTheme = () => {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            return savedTheme;
        }
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    };

    // Set initial theme
    const initialTheme = getPreferredTheme();
    document.documentElement.setAttribute('data-theme', initialTheme);

    // Create toggle button
    const themeToggle = document.createElement('button');
    themeToggle.className = 'btn theme-toggle-custom';
    themeToggle.setAttribute('aria-label', 'Toggle theme');
    themeToggle.setAttribute('title', 'Toggle light/dark theme');

    // Icon functions using navbar-icon class
    const getSunIcon = () => `<svg class="navbar-icon" viewBox="0 0 24 24">
        <path d="M12 3v2.25m6.364.386-1.591 1.591M21 12h-2.25m-.386 6.364-1.591-1.591M12 18.75V21m-4.773-4.227-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0Z" />
    </svg>`;

    const getMoonIcon = () => `<svg class="navbar-icon" viewBox="0 0 24 24">
        <path d="M21.752 15.002A9.72 9.72 0 0 1 18 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 0 0 3 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 0 0 9.002-5.998Z" />
    </svg>`;

    // Set initial icon (sun for dark theme, moon for light theme)
    themeToggle.innerHTML = initialTheme === 'dark' ? getSunIcon() : getMoonIcon();

    // Add to navbar
    navbarEnd.appendChild(themeToggle);

    // Toggle functionality with icon update
    themeToggle.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';

        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);

        // Update icon with smooth transition
        themeToggle.style.transform = 'scale(0.8)';
        setTimeout(() => {
            themeToggle.innerHTML = newTheme === 'dark' ? getSunIcon() : getMoonIcon();
            themeToggle.style.transform = 'scale(1)';
        }, 100);
    });

    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
        if (!localStorage.getItem('theme')) {
            const newTheme = e.matches ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', newTheme);
            themeToggle.innerHTML = newTheme === 'dark' ? getSunIcon() : getMoonIcon();
        }
    });
}

// course navigator creation
// This function creates a course navigator panel with a structured course outline
// It includes a toggle button, collapsible sections, and search functionality.

async function createCourseNavigator() {
    try {
        // Load course structure from JSON file
        const response = await fetch('_static/course_structure.json');
        if (!response.ok) {
            throw new Error(`Failed to load course structure: ${response.status}`);
        }
        const courseStructure = await response.json();
        
        // Create the toggle button
        createNavigatorButton();
        
        // Create the navigator panel
        createNavigatorPanel(courseStructure);
    } catch (error) {
        console.error('Error loading course structure:', error);
        
        // Fallback to hardcoded structure if JSON fails
        console.log('Falling back to hardcoded course structure');
        const fallbackStructure = {
            'Introduction': {
                'Course Overview': '/content/introduction/course_overview.html',
                'Mathematical Thinking': {
                    'Problem Solving': '/content/introduction/problem_solving.html',
                    'Proof Techniques': '/content/introduction/proof_techniques.html'
                },
                'Knowledge Graph': '/content/knowledge-graph.html'
            },
            'Interactive Tools': {
                'Python Playground': '/content/interactive/python_playground.html',
                'BKT Simple Demo': '/content/interactive/BKT_Simple_Demo.html',
                'BKT FSRS Demo': '/content/interactive/BKT_FSRS_Demo.html'
            }
        };
        
        createNavigatorButton();
        createNavigatorPanel(fallbackStructure);
    }
}

function createNavigatorButton() {
    // Find the navbar end section
    const navbarEnd = document.querySelector('.navbar-nav.navbar-end') ||
                     document.querySelector('.navbar-header-items__end') ||
                     document.querySelector('nav .navbar-nav:last-child');

    if (!navbarEnd) return;

    // Create course navigator button
    const navButton = document.createElement('button');
    navButton.id = 'course-nav-toggle';
    navButton.className = 'btn course-nav-toggle';

    navButton.innerHTML = `<svg class="navbar-icon" viewBox="0 0 24 24">
        <path d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25" />
    </svg>`;

    navButton.setAttribute('aria-label', 'Open Course Navigator');
    navButton.setAttribute('title', 'Course Navigator (Ctrl+M)');

    // Add click handler
    navButton.addEventListener('click', toggleNavigator);

    // Add to navbar
    navbarEnd.appendChild(navButton);

    // Add keyboard shortcut (Ctrl+M)
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'm') {
            e.preventDefault();
            toggleNavigator();
        }
    });
}

function createNavigatorPanel(courseStructure) {
    // Create overlay
    const overlay = document.createElement('div');
    overlay.id = 'course-nav-overlay';

    // Create panel
    const panel = document.createElement('div');
    panel.id = 'course-nav-panel';

    // Create panel header
    const header = document.createElement('div');
    header.className = 'nav-panel-header';

    header.innerHTML = `
        <div class="nav-panel-title-row">
            <h3 class="nav-panel-title">Course Navigator</h3>
            <button id="close-nav-panel" class="nav-panel-close" title="Close (Esc)">×</button>
        </div>
        <input type="text" id="nav-search" class="nav-search-input" placeholder="Search topics...">
    `;

    // Create navigation content
    const content = document.createElement('div');
    content.id = 'nav-content';
    content.className = 'nav-content';

    // Build navigation tree
    content.appendChild(buildNavigationTree(courseStructure));

    // Assemble panel
    panel.appendChild(header);
    panel.appendChild(content);

    // Add to page
    document.body.appendChild(overlay);
    document.body.appendChild(panel);

    // Add event handlers
    setupNavigatorHandlers(overlay, panel);

    // Add search functionality
    setupNavigatorSearch();
}

function buildNavigationTree(structure, level = 0) {
    const container = document.createElement('div');

    // Arrow icon functions
    const getExpandedArrow = () => `<svg class="nav-arrow-icon" viewBox="0 0 24 24">
        <path d="m19.5 8.25-7.5 7.5-7.5-7.5" />
    </svg>`;

    const getCollapsedArrow = () => `<svg class="nav-arrow-icon" viewBox="0 0 24 24">
        <path d="m8.25 4.5 7.5 7.5-7.5 7.5" />
    </svg>`;

    for (const [key, value] of Object.entries(structure)) {
        const item = document.createElement('div');
        item.style.marginLeft = `${level * 15}px`;

        if (typeof value === 'string') {
            // It's a link
            const link = document.createElement('a');
            link.href = value;
            link.textContent = key;
            link.className = 'nav-item-link';

            // Highlight current page
            if (window.location.pathname.includes(value)) {
                link.classList.add('current-page');
            }

            item.appendChild(link);
        } else {
            // It's a section with subsections
            const toggle = document.createElement('div');
            toggle.className = 'nav-section-toggle';

            // Check if this section contains the current page
            const containsCurrentPage = checkIfSectionContainsCurrentPage(value);
            const isExpanded = containsCurrentPage; // Expand if contains current page

            // Use SVG arrows instead of emoji
            toggle.innerHTML = `${isExpanded ? getExpandedArrow() : getCollapsedArrow()}${key}`;

            const subsection = buildNavigationTree(value, level + 1);
            subsection.style.display = isExpanded ? 'block' : 'none';

            toggle.addEventListener('click', () => {
                const isVisible = subsection.style.display !== 'none';
                subsection.style.display = isVisible ? 'none' : 'block';
                // Update arrow icon with SVG
                toggle.innerHTML = `${isVisible ? getCollapsedArrow() : getExpandedArrow()}${key}`;
            });

            item.appendChild(toggle);
            item.appendChild(subsection);
        }

        container.appendChild(item);
    }

    return container;
}

// Helper function to check if a section contains the current page
function checkIfSectionContainsCurrentPage(sectionData) {
    const currentPath = window.location.pathname;

    // Recursively check all values in the section
    function searchSection(data) {
        if (typeof data === 'string') {
            // It's a URL - check if it matches current page
            return currentPath.includes(data);
        } else if (typeof data === 'object') {
            // It's a nested section - check all its children
            for (const value of Object.values(data)) {
                if (searchSection(value)) {
                    return true;
                }
            }
        }
        return false;
    }

    return searchSection(sectionData);
}

function setupNavigatorHandlers(overlay, panel) {
    const closeBtn = document.getElementById('close-nav-panel');

    // Close handlers
    closeBtn.addEventListener('click', closeNavigator);
    overlay.addEventListener('click', closeNavigator);

    // Escape key to close
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && panel.style.right === '0px') {
            closeNavigator();
        }
    });
}

function setupNavigatorSearch() {
    const searchInput = document.getElementById('nav-search');
    const navContent = document.getElementById('nav-content');
    
    if (!searchInput || !navContent) return;
    
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().trim();
        const links = navContent.querySelectorAll('.nav-item-link');
        const sections = navContent.querySelectorAll('.nav-section-toggle');
        
        if (query === '') {
            // Show all items when search is empty
            links.forEach(link => {
                link.style.display = 'block';
                link.parentElement.style.display = 'block';
            });
            
            sections.forEach(section => {
                section.parentElement.style.display = 'block';
            });
        } else {
            // Filter based on search query
            links.forEach(link => {
                const text = link.textContent.toLowerCase();
                const matches = text.includes(query);
                
                // Show/hide the link
                link.style.display = matches ? 'block' : 'none';
                link.parentElement.style.display = matches ? 'block' : 'none';
                
                if (matches) {
                    // Show parent sections if child matches
                    let parent = link.parentElement;
                    while (parent && parent !== navContent) {
                        parent.style.display = 'block';
                        parent = parent.parentElement;
                    }
                }
            });
            
            // Handle sections - show if they contain visible links
            sections.forEach(section => {
                const sectionContainer = section.parentElement;
                const hasVisibleLinks = sectionContainer.querySelectorAll('.nav-item-link[style*="display: block"]').length > 0;
                
                if (hasVisibleLinks) {
                    sectionContainer.style.display = 'block';
                    // Also expand the section to show matching results
                    const subsection = section.nextElementSibling;
                    if (subsection) {
                        subsection.style.display = 'block';
                    }
                } else {
                    sectionContainer.style.display = 'none';
                }
            });
        }
    });
}

function toggleNavigator() {
    const panel = document.getElementById('course-nav-panel');
    const overlay = document.getElementById('course-nav-overlay');

    if (panel.style.right === '0px') {
        closeNavigator();
    } else {
        openNavigator();
    }
}

function openNavigator() {
    const panel = document.getElementById('course-nav-panel');
    const overlay = document.getElementById('course-nav-overlay');

    overlay.style.display = 'block';
    setTimeout(() => {
        overlay.style.opacity = '1';
        panel.style.right = '0px';
    }, 10);

    // Focus search input
    setTimeout(() => {
        document.getElementById('nav-search')?.focus();
    }, 300);
}

function closeNavigator() {
    const panel = document.getElementById('course-nav-panel');
    const overlay = document.getElementById('course-nav-overlay');

    panel.style.right = '-400px';
    overlay.style.opacity = '0';

    setTimeout(() => {
        overlay.style.display = 'none';
    }, 300);
}

// Interactive Tools Finder
// Creates a simplified finder specifically for interactive tools with a streamlined layout

function createInteractiveToolsFinder() {
    // Interactive tools structure - simplified since there are only a few tools
    const interactiveTools = {
        'BKT Simple Demo': {
            url: '/content/interactive/BKT_Simple_Demo.html',
            description: 'Bayesian Knowledge Tracing demonstration',
            icon: '🧠'
        },
        'BKT FSRS Demo': {
            url: '/content/interactive/BKT_FSRS_Demo.html',
            description: 'FSRS-based spaced repetition demo',
            icon: '⏳'
        },
        'MCQ Breakdown Demo': {
            url: '/content/interactive/MCQ_Breakdown_Demo.html',
            description: 'Multiple Choice Question breakdown tool',
            icon: '❓'
        },
        'Comprehensive MCQS Demo': {
            url: '/content/interactive/full_mcqs_demo.html',
            description: 'Revision Area showing statstics updates',
            icon: '📚'
        },
    };

    // Create the toggle button
    createToolsFinderButton();

    // Create the tools finder panel
    createToolsFinderPanel(interactiveTools);
}

function createToolsFinderButton() {
    // Find the navbar end section
    const navbarEnd = document.querySelector('.navbar-nav.navbar-end') ||
                     document.querySelector('.navbar-header-items__end') ||
                     document.querySelector('nav .navbar-nav:last-child');

    if (!navbarEnd) return;

    // Create interactive tools button
    const toolsButton = document.createElement('button');
    toolsButton.id = 'tools-finder-toggle';
    toolsButton.className = 'btn tools-finder-toggle';

    toolsButton.innerHTML = `<svg class="navbar-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
                            </svg>`;

    toolsButton.setAttribute('aria-label', 'Open Revision Area');
    toolsButton.setAttribute('title', 'Revision Area');

    // Add click handler
    toolsButton.addEventListener('click', toggleToolsFinder);

    // Add to navbar (before course navigator if it exists)
    const courseNavButton = document.getElementById('course-nav-toggle');
    if (courseNavButton) {
        navbarEnd.insertBefore(toolsButton, courseNavButton);
    } else {
        navbarEnd.appendChild(toolsButton);
    }
}

function createToolsFinderPanel(tools) {
    // Create overlay
    const overlay = document.createElement('div');
    overlay.id = 'tools-finder-overlay';
    overlay.className = 'tools-overlay';

    // Create panel
    const panel = document.createElement('div');
    panel.id = 'tools-finder-panel';
    panel.className = 'tools-panel';

    // Create panel header
    const header = document.createElement('div');
    header.className = 'tools-panel-header';

    header.innerHTML = `
        <div class="tools-panel-title-row">
            <h3 class="tools-panel-title">📚 Revision Area</h3>
            <button id="close-tools-panel" class="tools-panel-close" title="Close (Esc)">×</button>
        </div>
        <p class="tools-panel-subtitle">Quick access to revision and practice tools</p>
    `;

    // Create tools grid
    const toolsGrid = document.createElement('div');
    toolsGrid.className = 'tools-grid';

    // Build tools cards
    for (const [name, tool] of Object.entries(tools)) {
        const toolCard = document.createElement('a');
        toolCard.href = tool.url;
        toolCard.className = 'tool-card';

        // Highlight current page
        if (window.location.pathname.includes(tool.url)) {
            toolCard.classList.add('current-tool');
        }

        toolCard.innerHTML = `
            <div class="tool-icon">${tool.icon}</div>
            <div class="tool-content">
                <div class="tool-name">${name}</div>
                <div class="tool-description">${tool.description}</div>
            </div>
            <div class="tool-arrow">→</div>
        `;

        toolsGrid.appendChild(toolCard);
    }

    // Assemble panel
    panel.appendChild(header);
    panel.appendChild(toolsGrid);

    // Add to page
    document.body.appendChild(overlay);
    document.body.appendChild(panel);

    // Add event handlers
    setupToolsFinderHandlers(overlay, panel);
}

function setupToolsFinderHandlers(overlay, panel) {
    // Close button
    document.getElementById('close-tools-panel').addEventListener('click', closeToolsFinder);

    // Overlay click to close
    overlay.addEventListener('click', closeToolsFinder);

    // Escape key to close
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && panel.style.display !== 'none') {
            closeToolsFinder();
        }
    });

    // Prevent panel clicks from closing
    panel.addEventListener('click', (e) => {
        e.stopPropagation();
    });
}

function toggleToolsFinder() {
    const panel = document.getElementById('tools-finder-panel');
    const overlay = document.getElementById('tools-finder-overlay');

    if (panel.style.display === 'block') {
        closeToolsFinder();
    } else {
        openToolsFinder();
    }
}

function openToolsFinder() {
    const panel = document.getElementById('tools-finder-panel');
    const overlay = document.getElementById('tools-finder-overlay');

    overlay.style.display = 'block';
    panel.style.display = 'block';

    setTimeout(() => {
        overlay.style.opacity = '1';
        panel.style.transform = 'translate(-50%, -50%) scale(1)';
        panel.style.opacity = '1';
    }, 10);
}

function closeToolsFinder() {
    const panel = document.getElementById('tools-finder-panel');
    const overlay = document.getElementById('tools-finder-overlay');

    panel.style.transform = 'translate(-50%, -50%) scale(0.95)';
    panel.style.opacity = '0';
    overlay.style.opacity = '0';

    setTimeout(() => {
        panel.style.display = 'none';
        overlay.style.display = 'none';
    }, 200);
}

// AUTO-HIDE SIDEBAR FOR INTERACTIVE PAGES
function autoHideSidebarForInteractive() {
    const currentPath = window.location.pathname;

    if (currentPath.includes('/interactive/')) {
        // Add CSS classes
        document.body.classList.add('no-sidebar');
        document.documentElement.classList.add('no-sidebar');

        // More aggressive sidebar hiding
        setTimeout(() => {
            // Target all possible sidebar selectors
            const sidebarSelectors = [
                '.bd-sidebar-primary',
                '.bd-sidebar',
                '.pst-primary-sidebar',
                '.sidebar-primary-items__start',
                '.sidebar-primary-items__end',
                '.sidebar-primary-items',
                '[data-bs-target="#pst-primary-sidebar"]',
                'aside[class*="sidebar"]',
                'nav[class*="sidebar"]',
                'div[class*="sidebar-primary"]',
                '.sphinx-sidebar',
                '.documentwrapper .sphinxsidebar'
            ];

            // Hide all sidebar elements
            sidebarSelectors.forEach(selector => {
                const elements = document.querySelectorAll(selector);
                elements.forEach(el => {
                    el.style.display = 'none';
                    el.style.visibility = 'hidden';
                    el.style.width = '0';
                    el.style.minWidth = '0';
                    el.style.maxWidth = '0';
                    el.style.opacity = '0';
                });
            });

            // Expand main content
            const mainSelectors = [
                '.bd-main',
                '.bd-page',
                '.bd-content',
                '.bd-article',
                '.bd-article-container',
                '.bd-container',
                'main',
                '.main-content',
                '.content-wrapper'
            ];

            mainSelectors.forEach(selector => {
                const elements = document.querySelectorAll(selector);
                elements.forEach(el => {
                    el.style.marginLeft = '0';
                    el.style.width = '100%';
                    el.style.maxWidth = '100%';
                    el.style.gridColumn = '1 / -1';
                });
            });

            // Update grid layouts
            const pageElements = document.querySelectorAll('.bd-page');
            pageElements.forEach(el => {
                el.style.gridTemplateColumns = '1fr';
                el.style.gridTemplateAreas = '"main"';
            });

        }, 50);

        // Additional check after a longer delay to catch any dynamically loaded content
        setTimeout(() => {
            const visibleSidebars = document.querySelectorAll('.bd-sidebar-primary:not([style*="display: none"]), .bd-sidebar:not([style*="display: none"])');
            visibleSidebars.forEach(sidebar => {
                sidebar.style.display = 'none !important';
                sidebar.style.visibility = 'hidden !important';
                sidebar.style.width = '0 !important';
            });
        }, 500);
    }
}
