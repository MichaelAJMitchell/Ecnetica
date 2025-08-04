// Minimal theme JavaScript
(function() {
    'use strict';
    
    console.log('Theme loaded');
    
    // Basic theme toggle
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const current = document.documentElement.getAttribute('data-theme');
            const newTheme = current === 'light' ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }
    
    // Basic mobile navigation
    const navToggle = document.querySelector('.navbar-toggle');
    const sidebar = document.querySelector('.theme-sidebar');
    if (navToggle && sidebar) {
        navToggle.addEventListener('click', function() {
            sidebar.classList.toggle('open');
        });
    }
    
})();
