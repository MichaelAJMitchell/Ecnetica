// dark mode and light mode theme toggle
// with a listener for system theme changes

document.addEventListener('DOMContentLoaded', function() {
    createEnhancedThemeToggle();
    createCourseNavigator();
});

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

function createCourseNavigator() {
    // Course structure - matches your actual _toc.yml
    const courseStructure = {
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
            'BKT Simple Demo': '/content/interactive/BKT_Simple_Demo.html'
        },
        'Number Systems': {
            'Overview': {
                'Natural Numbers and Integers': '/content/number_systems/natural_integers.html',
                'Rational Numbers': '/content/number_systems/rational_numbers.html',
                'Irrational Numbers': '/content/number_systems/irrational_numbers.html',
                'Operations Properties': '/content/number_systems/operations_properties.html'
            },
            'Practical Considerations': {
                'Scientific Notation': '/content/number_systems/scientific_notation.html',
                'Estimation Approximation': '/content/number_systems/estimation_approximation.html'
            }
        },
        'Functions': {
            'Fundamentals': {
                'Definition Mappings': '/content/functions/definition_mappings.html',
                'Domain Codomain Range': '/content/functions/domain_codomain_range.html',
                'Representation Methods': '/content/functions/representation_methods.html'
            },
            'Properties': {
                'Injective Surjective Bijective': '/content/functions/injective_surjective_bijective.html',
                'Composite Functions': '/content/functions/composite_functions.html',
                'Inverse Functions': '/content/functions/inverse_functions.html'
            },
            'Types and Graphs': {
                'Linear Functions': '/content/functions/linear_functions.html',
                'Quadratic Functions': '/content/functions/quadratic_functions_gen.html',
                'Cubic Polynomial': '/content/functions/cubic_polynomial.html',
                'Exponential Functions': '/content/functions/exponential_functions.html',
                'Logarithmic Functions': '/content/functions/logarithmic_functions.html'
            },
            'Transformations': {
                'Translations': '/content/functions/translations.html',
                'Reflections': '/content/functions/reflections.html',
                'Scaling': '/content/functions/scaling.html'
            }
        },
        'Algebra': {
            'Expressions Manipulation': {
                'Algebraic Notation': '/content/algebra/algebraic_notation.html',
                'Substitution Simplification': '/content/algebra/substitution_simplification.html',
                'Important Products': '/content/algebra/important_products.html'
            }
        }
        // Add more sections as needed...
    };

    // Create the toggle button
    createNavigatorButton();
    
    // Create the navigator panel
    createNavigatorPanel(courseStructure);
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
            
            const isExpanded = level < 2; // Auto-expand first two levels
            toggle.innerHTML = `${isExpanded ? '▼' : '▶'} ${key}`;
            
            const subsection = buildNavigationTree(value, level + 1);
            subsection.style.display = isExpanded ? 'block' : 'none';
            
            toggle.addEventListener('click', () => {
                const isVisible = subsection.style.display !== 'none';
                subsection.style.display = isVisible ? 'none' : 'block';
                toggle.innerHTML = `${isVisible ? '▶' : '▼'} ${key}`;
            });
            
            item.appendChild(toggle);
            item.appendChild(subsection);
        }
        
        container.appendChild(item);
    }
    
    return container;
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
    
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        const links = navContent.querySelectorAll('.nav-item-link');
        
        links.forEach(link => {
            const text = link.textContent.toLowerCase();
            const matches = text.includes(query);
            
            // Show/hide the link
            link.style.display = matches || query === '' ? 'block' : 'none';
            
            // Show parent sections if child matches
            if (matches && query !== '') {
                let parent = link.closest('.nav-section-toggle')?.nextElementSibling;
                while (parent) {
                    parent.style.display = 'block';
                    parent = parent.parentElement?.closest('.nav-section-toggle')?.nextElementSibling;
                }
            }
        });
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