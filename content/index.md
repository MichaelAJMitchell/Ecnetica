# Ecnetica - Our curriculum

This course covers the essential Leaving Cert mathematics topics you'll encounter in your studies, from basic number systems through calculus, statistics, and probability. The content is organized into clear sections that build on each other, with interactive tools available to help you practice and understand key concepts. You can navigate through the material using the tools above or browse the full course structure below. Each section includes worked examples, practice problems, and connections to related topics, giving you multiple ways to engage with the mathematics as you learn.Our curriculum

Welcome to our comprehensive mathematics course! This page serves as your main navigation hub for all course content. The structure below is dynamically generated from our course organization system.

<div id="course-tools-bar">
  <div id="loading-message">Loading course tools...</div>
</div>

<div id="course-structure-container">
  <div id="loading-message">Loading course structure...</div>
</div>

```{raw} html
<script>
// Function to load and display course structure
async function loadCourseStructure() {
  try {
    // Load the course structure JSON file
    const response = await fetch('/_static/course_structure.json');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const courseStructure = await response.json();
    
    // Generate tools bar first
    const toolsContainer = document.getElementById('course-tools-bar');
    toolsContainer.innerHTML = generateToolsBar(courseStructure);
    
    // Generate HTML for the course structure
    const container = document.getElementById('course-structure-container');
    container.innerHTML = generateCourseHTML(courseStructure);
    
    // Add interactivity
    addNavigationFeatures();
    addToolsBarHandlers();
    
  } catch (error) {
    console.error('Error loading course structure:', error);
    document.getElementById('course-structure-container').innerHTML = 
      `<div class="course-error">Error loading course structure. Please check that course_structure.json is accessible.</div>`;
  }
}

// Function to generate HTML from course structure
function generateCourseHTML(structure) {
  let html = '<div class="course-navigator">';
  
  for (const [sectionName, sectionContent] of Object.entries(structure)) {
    html += `
      <div class="course-section" data-section="${sectionName}">
        <h2 class="course-section-header" onclick="toggleSection('${sectionName}')">
          <span class="course-toggle-icon">▼</span>
          ${sectionName}
        </h2>
        <div class="course-section-content" id="section-${sectionName}">
          ${generateSectionHTML(sectionContent)}
        </div>
      </div>
    `;
  }
  
  html += '</div>';
  return html;
}

// Function to generate HTML for section content (recursive)
function generateSectionHTML(content) {
  let html = '';
  
  if (typeof content === 'string') {
    // This is a direct link
    const pageName = content.split('/').pop().replace('.html', '').replace(/_/g, ' ');
    html += `<div class="course-content-item">
      <a href="${content}" class="course-content-link">${pageName}</a>
    </div>`;
  } else if (typeof content === 'object') {
    // This is a nested structure
    for (const [key, value] of Object.entries(content)) {
      if (typeof value === 'string') {
        // Direct link
        html += `<div class="course-content-item">
          <a href="${value}" class="course-content-link">${key}</a>
        </div>`;
      } else {
        // Nested subsection
        html += `
          <div class="course-subsection">
            <h3 class="course-subsection-header" onclick="toggleSubsection('${key.replace(/\s+/g, '-')}')" data-key="${key}">
              <span class="course-toggle-icon">▼</span>
              ${key}
            </h3>
            <div class="course-subsection-content" id="subsection-${key.replace(/\s+/g, '-')}">
              ${generateSectionHTML(value)}
            </div>
          </div>
        `;
      }
    }
  }
  
  return html;
}

// Function to toggle section visibility
function toggleSection(sectionName) {
  const content = document.getElementById(`section-${sectionName}`);
  const icon = document.querySelector(`[data-section="${sectionName}"] .course-toggle-icon`);
  
  if (content.style.display === 'none' || content.style.display === '') {
    content.style.display = 'block';
    icon.textContent = '▼';
  } else {
    content.style.display = 'none';
    icon.textContent = '▶';
  }
}

// Function to toggle subsection visibility
function toggleSubsection(subsectionId) {
  const content = document.getElementById(`subsection-${subsectionId}`);
  const icon = content.previousElementSibling.querySelector('.course-toggle-icon');
  
  if (content.style.display === 'none' || content.style.display === '') {
    content.style.display = 'block';
    icon.textContent = '▼';
  } else {
    content.style.display = 'none';
    icon.textContent = '▶';
  }
}

// Function to add navigation features
function addNavigationFeatures() {
  // Add search functionality
  const searchContainer = document.createElement('div');
  searchContainer.className = 'course-search-container';
  searchContainer.innerHTML = `
    <input type="text" id="course-search" class="course-search-input" placeholder="Search course content..." />
    <div id="search-results" class="course-search-results"></div>
  `;
  
  const navigator = document.querySelector('.course-navigator');
  navigator.insertBefore(searchContainer, navigator.firstChild);
  
  // Add search event listener
  document.getElementById('course-search').addEventListener('input', handleSearch);
  
  // Add progress tracking
  addProgressTracking();
}

// Search functionality
function handleSearch(event) {
  const searchTerm = event.target.value.toLowerCase();
  const contentLinks = document.querySelectorAll('.course-content-link');
  const results = document.getElementById('search-results');
  
  if (searchTerm === '') {
    results.innerHTML = '';
    results.style.display = 'none';
    return;
  }
  
  const matches = [];
  contentLinks.forEach(link => {
    if (link.textContent.toLowerCase().includes(searchTerm)) {
      matches.push({
        text: link.textContent,
        href: link.href,
        section: link.closest('.course-section').dataset.section
      });
    }
  });
  
  if (matches.length > 0) {
    results.innerHTML = matches.map(match => 
      `<div class="course-search-result">
        <a href="${match.href}" class="course-search-result-link">${match.text}</a>
        <span class="course-search-section">${match.section}</span>
      </div>`
    ).join('');
    results.style.display = 'block';
  } else {
    results.innerHTML = '<div class="course-no-results">No matching content found</div>';
    results.style.display = 'block';
  }
}

// Progress tracking (placeholder for future implementation)
function addProgressTracking() {
  // This could track which pages have been visited
  // and show progress indicators
  console.log('Progress tracking initialized');
}

// Load course structure when page loads
document.addEventListener('DOMContentLoaded', loadCourseStructure);

// Function to generate tools bar
function generateToolsBar(courseStructure) {
  const quickAccessTools = [
    {
      title: 'Interactive Tools',
      icon: '🔧',
      items: [
        { name: 'Python Playground', url: '/content/interactive/python_playground.html', icon: '🐍' },
        { name: 'BKT Simple Demo', url: '/content/interactive/BKT_Simple_Demo.html', icon: '🧠' },
        { name: 'BKT FSRS Demo', url: '/content/interactive/BKT_FSRS_Demo.html', icon: '⏳' },
        { name: 'MCQ Breakdown Demo', url: '/content/interactive/MCQ_Breakdown_Demo.html', icon: '❓' }
      ]
    },
    {
      title: 'Core Subjects',
      icon: '📚',
      items: [
        { name: 'Algebra', url: '#Algebra', icon: '🔢', isSection: true },
        { name: 'Functions', url: '#Functions', icon: '📈', isSection: true },
        { name: 'Calculus', url: '#Differential Calculus', icon: '∫', isSection: true },
        { name: 'Statistics', url: '#Statistics', icon: '📊', isSection: true }
      ]
    },
    {
      title: 'Study Tools',
      icon: '📖',
      items: [
        { name: 'Course Overview', url: '/content/introduction/course_overview.html', icon: '📋' },
        { name: 'Knowledge Graph', url: '/content/knowledge-graph.html', icon: '🕸️' },
        { name: 'Practice Papers', url: '/content/exam_prep/practice_papers.html', icon: '📝' },
        { name: 'Study Strategies', url: '/content/exam_prep/study_strategies.html', icon: '💡' }
      ]
    }
  ];

  let html = '<div class="course-tools-container">';
  
  quickAccessTools.forEach(category => {
    html += `
      <div class="tools-category">
        <button class="tools-category-btn" onclick="toggleToolsCategory('${category.title.replace(/\s+/g, '-').toLowerCase()}')">
          <span class="tools-category-icon">${category.icon}</span>
          <span class="tools-category-title">${category.title}</span>
          <span class="tools-category-arrow">▼</span>
        </button>
        <div class="tools-category-items" id="tools-${category.title.replace(/\s+/g, '-').toLowerCase()}">
          ${category.items.map(item => `
            <a href="${item.url}" class="tools-item-link" ${item.isSection ? `onclick="scrollToSection('${item.name}')"` : ''}>
              <span class="tools-item-icon">${item.icon}</span>
              <span class="tools-item-name">${item.name}</span>
            </a>
          `).join('')}
        </div>
      </div>
    `;
  });
  
  html += '</div>';
  return html;
}

function toggleToolsCategory(categoryId) {
  const items = document.getElementById(`tools-${categoryId}`);
  const arrow = document.querySelector(`button[onclick*="${categoryId}"] .tools-category-arrow`);
  
  if (items.style.display === 'none' || items.style.display === '') {
    items.style.display = 'block';
    arrow.textContent = '▲';
  } else {
    items.style.display = 'none';
    arrow.textContent = '▼';
  }
}

function scrollToSection(sectionName) {
  // First expand the section if it's collapsed
  const sectionElement = document.querySelector(`[data-section="${sectionName}"]`);
  if (sectionElement) {
    const content = sectionElement.querySelector('.course-section-content');
    const icon = sectionElement.querySelector('.course-toggle-icon');
    
    if (content.style.display === 'none' || content.style.display === '') {
      content.style.display = 'block';
      icon.textContent = '▼';
    }
    
    // Scroll to the section
    sectionElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  
  // Prevent the default link behavior
  return false;
}

function addToolsBarHandlers() {
  // Add hover effects and any additional interactivity
  const toolsItems = document.querySelectorAll('.tools-item-link');
  
  toolsItems.forEach(item => {
    item.addEventListener('mouseenter', function() {
      this.style.transform = 'translateX(4px)';
    });
    
    item.addEventListener('mouseleave', function() {
      this.style.transform = 'translateX(0)';
    });
  });
}
</script>
```
