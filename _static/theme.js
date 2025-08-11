document.addEventListener('DOMContentLoaded', function() {
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
        // Check if user has a saved preference
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            return savedTheme;
        }
        
        // Otherwise, use browser's preference
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    };
    
    // Set initial theme
    const initialTheme = getPreferredTheme();
    document.documentElement.setAttribute('data-theme', initialTheme);
    
    // Create toggle button
    const themeToggle = document.createElement('button');
    themeToggle.className = 'btn theme-toggle-custom';
    themeToggle.innerHTML = initialTheme === 'dark' ? '☀️' : '🌙';
    themeToggle.setAttribute('aria-label', 'Toggle theme');
    
    // Add to navbar
    navbarEnd.appendChild(themeToggle);
    
    // Toggle functionality
    themeToggle.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        themeToggle.innerHTML = newTheme === 'dark' ? '☀️' : '🌙';
    });
    
    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
        // Only update if user hasn't manually set a preference
        if (!localStorage.getItem('theme')) {
            const newTheme = e.matches ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', newTheme);
            themeToggle.innerHTML = newTheme === 'dark' ? '☀️' : '🌙';
        }
    });
});

// Add this to your _static/theme.js file (after your existing theme toggle code)

document.addEventListener('DOMContentLoaded', function() {
    // Your existing theme toggle code stays here...
    
    // Add Course Navigator
    createCourseNavigator();
});

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
    navButton.innerHTML = '📋';
    navButton.setAttribute('aria-label', 'Open Course Navigator');
    navButton.setAttribute('title', 'Course Navigator (Ctrl+M)');
    
    // Style the button
    navButton.style.cssText = `
        background: none;
        border: 1px solid var(--pst-color-border, #dee2e6);
        border-radius: 0.375rem;
        padding: 0.375rem;
        margin-left: 0.5rem;
        color: var(--pst-color-text-base, #333);
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;
        font-size: 1rem;
    `;
    
    // Add hover effect
    navButton.addEventListener('mouseenter', () => {
        navButton.style.backgroundColor = 'var(--pst-color-surface, #f8f9fa)';
        navButton.style.transform = 'scale(1.05)';
    });
    
    navButton.addEventListener('mouseleave', () => {
        navButton.style.backgroundColor = 'transparent';
        navButton.style.transform = 'scale(1)';
    });
    
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
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        z-index: 9998;
        display: none;
        opacity: 0;
        transition: opacity 0.3s ease;
    `;
    
    // Create panel
    const panel = document.createElement('div');
    panel.id = 'course-nav-panel';
    panel.style.cssText = `
        position: fixed;
        top: 0;
        right: -400px;
        width: 400px;
        height: 100%;
        background: var(--background-primary, #fff);
        border-left: 1px solid var(--border-primary, #dee2e6);
        box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
        z-index: 9999;
        transition: right 0.3s ease;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
    `;
    
    // Create panel header
    const header = document.createElement('div');
    header.style.cssText = `
        padding: 20px;
        border-bottom: 1px solid var(--border-light, #e9ecef);
        background: var(--background-secondary, #f8f9fa);
        position: sticky;
        top: 0;
        z-index: 10;
    `;
    
    header.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h3 style="margin: 0; color: var(--text-primary, #333); font-size: 1.2rem;">📚 Course Navigator</h3>
            <button id="close-nav-panel" style="
                background: none;
                border: none;
                font-size: 1.5rem;
                cursor: pointer;
                color: var(--text-muted, #666);
                padding: 5px;
                border-radius: 4px;
                transition: background-color 0.2s;
            " title="Close (Esc)">×</button>
        </div>
        <input type="text" id="nav-search" placeholder="Search topics..." style="
            width: 100%;
            padding: 8px 12px;
            margin-top: 15px;
            border: 1px solid var(--border-primary, #dee2e6);
            border-radius: 4px;
            background: var(--background-primary, #fff);
            color: var(--text-primary, #333);
            font-size: 14px;
        ">
    `;
    
    // Create navigation content
    const content = document.createElement('div');
    content.id = 'nav-content';
    content.style.cssText = `
        padding: 20px;
        flex: 1;
    `;
    
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
            link.style.cssText = `
                display: block;
                padding: 8px 12px;
                color: var(--text-primary, #333);
                text-decoration: none;
                border-radius: 4px;
                margin: 2px 0;
                transition: all 0.2s ease;
                font-size: 14px;
            `;
            
            // Highlight current page
            if (window.location.pathname.includes(value)) {
                link.style.backgroundColor = 'var(--primary-light, #e3f2fd)';
                link.style.color = 'var(--primary, #1976d2)';
                link.style.fontWeight = 'bold';
            }
            
            link.addEventListener('mouseenter', () => {
                if (!window.location.pathname.includes(value)) {
                    link.style.backgroundColor = 'var(--background-tertiary, #f0f0f0)';
                }
            });
            
            link.addEventListener('mouseleave', () => {
                if (!window.location.pathname.includes(value)) {
                    link.style.backgroundColor = 'transparent';
                }
            });
            
            item.appendChild(link);
        } else {
            // It's a section with subsections
            const toggle = document.createElement('div');
            toggle.className = 'nav-section-toggle';
            toggle.style.cssText = `
                padding: 8px 12px;
                cursor: pointer;
                color: var(--text-primary, #333);
                font-weight: 600;
                border-radius: 4px;
                margin: 2px 0;
                transition: background-color 0.2s;
                font-size: 14px;
                user-select: none;
            `;
            
            const isExpanded = level < 2; // Auto-expand first two levels
            toggle.innerHTML = `${isExpanded ? '▼' : '▶'} ${key}`;
            
            const subsection = buildNavigationTree(value, level + 1);
            subsection.style.display = isExpanded ? 'block' : 'none';
            
            toggle.addEventListener('click', () => {
                const isVisible = subsection.style.display !== 'none';
                subsection.style.display = isVisible ? 'none' : 'block';
                toggle.innerHTML = `${isVisible ? '▶' : '▼'} ${key}`;
            });
            
            toggle.addEventListener('mouseenter', () => {
                toggle.style.backgroundColor = 'var(--background-tertiary, #f0f0f0)';
            });
            
            toggle.addEventListener('mouseleave', () => {
                toggle.style.backgroundColor = 'transparent';
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