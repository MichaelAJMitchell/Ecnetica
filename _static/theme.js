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