# SD4D System Files

**Last Updated:** March 15, 2025 19:50 EDT

This document contains the definitive versions of critical system files for the SD4D (SideboardDashboardForDropbox) project.
These files should not be modified directly by users. If system files become corrupted,
an AI assistant or developer can use this document to restore them.

## GitHub Reference Information

**Repository:** [SD4D GitHub Repository](https://github.com/username/SD4D)  
**Directory:** `/docs`  
**Last Verified Commit:** `________`  

> **IMPORTANT NOTE FOR MAINTAINERS:**  
> The proper updating procedure is:
> 1. Make necessary changes to system files and update this document
> 2. Commit these changes to the repository
> 3. After the commit is complete, edit this document again to fill in the "Last Verified Commit" 
>    field above with the new commit hash from the previous step
> 4. Commit this update with a message like "Update commit reference in System_files.md"
>
> This two-step commit process ensures that users and AI assistants can always find a known-good 
> version of these files in the repository history, even if the current working files become corrupted.
>
> **Note for External Developers:**
> If you've forked or cloned this repository for your own development:
> - Only the original repository owner can update the main repository
> - You can maintain your own version of this document in your fork
> - Consider keeping a reference to the original repository for upstream changes

## Critical Files Overview

The following files are essential for proper system operation:
- `docs/index.html`: Main entry point and sidebar container
- `docs/js/viewer.js`: Core functionality for sidebar and content display
- `docs/css/styles.css`: Styling for the dashboard interface

## File Contents

### docs/index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta http-equiv="Cache-Control" content="no-store, no-cache, must-revalidate, max-age=0">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>Static Sidebar Dashboard</title>
    <link rel="stylesheet" href="css/styles.css">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="js/viewer.js"></script>
</head>
<body>
    <div id="sidebar"></div>
    <div id="content-area"></div>
</body>
</html>
```

### docs/js/viewer.js
```javascript
/**
 * Static Sidebar Dashboard
 * 
 * A minimal implementation that:
 * 1. Renders markdown sidebar
 * 2. Opens all links in positioned windows
 * 3. Renders markdown files directly
 * 4. Auto-refreshes sidebar content
 * 
 * Dependencies:
 * - marked.js: For Markdown rendering
 * 
 */

// Configure marked for secure rendering
marked.setOptions({
    headerIds: false,
    mangle: false,
    breaks: true
});

// Track the last modified time of sidebar.md
let lastSidebarModified = 0;

// Track the current content file and its last modified time
let currentContentFile = 'welcome.md';
let lastContentModified = 0;

/**
 * Initialize the dashboard
 * Loads and renders sidebar content
 */
async function initDashboard() {
    try {
        // Load and render sidebar
        await loadSidebar();
        
        // Check for mode and display appropriate greeting
        await checkModeAndGreet();
        
        // Load welcome content in the main area
        await loadWelcomeContent();
        
        // Setup auto-refresh for sidebar and content
        setInterval(checkSidebarUpdates, 2000);
        setInterval(checkContentUpdates, 2000);
    } catch (error) {
        console.error('Failed to initialize:', error);
        document.getElementById('sidebar').innerHTML = 
            '<div class="sidebar-title">Error</div>' +
            '<p>Failed to load sidebar content</p>';
    }
}

/**
 * Check which mode is active and display the appropriate greeting
 */
async function checkModeAndGreet() {
    try {
        // First, try to detect if we're in Author Mode by checking the window title
        const isAuthorMode = document.title.includes('Author Mode') || 
                            window.location.href.includes('author-mode') ||
                            document.documentElement.style.getPropertyValue('--theme-color') === '#4CAF50';
                            
        // If we can't determine from title, check if we're in Development Mode
        const isDevMode = document.title.includes('Development Mode') || 
                         window.location.href.includes('development-mode') ||
                         document.documentElement.style.getPropertyValue('--theme-color') === '#2196F3';
        
        // Set the greeting file based on detected mode
        let greetingFile = 'welcome.md'; // Default
        
        if (isAuthorMode) {
            greetingFile = 'author_greeting.md';
            console.log('Author Mode detected, loading author greeting');
        } else if (isDevMode) {
            greetingFile = 'dev_greeting.md';
            console.log('Development Mode detected, loading dev greeting');
        }
        
        // Load the appropriate greeting
        await loadContent(greetingFile);
        
    } catch (error) {
        console.error('Failed to check mode and greet:', error);
        // Fall back to loading welcome content
        await loadWelcomeContent();
    }
}

/**
 * Load and render the sidebar content
 */
async function loadSidebar() {
    try {
        // Add cache-busting parameter
        const timestamp = new Date().getTime();
        const response = await fetch('sidebar.md?t=' + timestamp);
        
        if (!response.ok) {
            throw new Error(`Failed to load sidebar: ${response.status} ${response.statusText}`);
        }
        
        // Get last modified time from headers if available
        const lastModified = response.headers.get('Last-Modified');
        if (lastModified) {
            lastSidebarModified = new Date(lastModified).getTime();
        } else {
            lastSidebarModified = timestamp;
        }
        
        const sidebarMd = await response.text();
        const html = marked.parse(sidebarMd);
        
        // Process HTML to add classes
        const processedHtml = html
            .replace(/<h1>(.*?)<\/h1>/g, '<div class="sidebar-title">$1</div>')
            .replace(/<h2>(.*?)<\/h2>/g, '<div class="section-title">$1</div>');
        
        
        document.getElementById('sidebar').innerHTML =  processedHtml;
        
        // Setup navigation
        setupNavigation();
        
        console.log('Sidebar loaded at:', new Date().toLocaleTimeString());
    } catch (error) {
        console.error('Failed to load sidebar:', error);
        throw error;
    }
}

/**
 * Load welcome content in the main content area
 */
async function loadWelcomeContent() {
    try {
        await loadContent('welcome.md');
    } catch (error) {
        console.error('Failed to load welcome content:', error);
        document.getElementById('content-area').innerHTML = 
            '<h1>Welcome to Static Dashboard</h1>' +
            '<p>There was an error loading the welcome content. Please check the console for details.</p>';
    }
}

/**
 * Load content in the main content area
 * @param {string} contentFile - Markdown file to load
 */
async function loadContent(contentFile) {
    try {
        const contentArea = document.getElementById('content-area');
        
        // Show loading indicator
        contentArea.innerHTML = `<p>Loading ${contentFile}...</p>`;
        
        // Set current content file
        currentContentFile = contentFile;
        
        // Add cache-busting parameter
        const timestamp = new Date().getTime();
        const response = await fetch(currentContentFile + '?t=' + timestamp);
        
        if (!response.ok) {
            throw new Error(`Failed to load content: ${response.status} ${response.statusText}`);
        }
        
        // Get last modified time from headers if available
        const lastModified = response.headers.get('Last-Modified');
        if (lastModified) {
            lastContentModified = new Date(lastModified).getTime();
        } else {
            lastContentModified = timestamp;
        }
        
        const content = await response.text();
        contentArea.innerHTML = marked.parse(content);
        
        console.log(`Content ${contentFile} loaded`);
    } catch (error) {
        console.error(`Failed to load content ${contentFile}:`, error);
        throw error;
    }
}

/**
 * Check if sidebar.md has been updated and reload if necessary
 */
async function checkSidebarUpdates() {
    try {
        // Add cache-busting parameter
        const timestamp = new Date().getTime();
        const response = await fetch('sidebar.md?t=' + timestamp, { method: 'HEAD' });
        
        if (!response.ok) {
            return;
        }
        
        // Get last modified time from headers if available
        const lastModified = response.headers.get('Last-Modified');
        if (lastModified) {
            const modifiedTime = new Date(lastModified).getTime();
            
            // If sidebar has been modified, reload it
            if (modifiedTime > lastSidebarModified) {
                console.log('Sidebar updated, reloading...');
                await loadSidebar();
            }
        }
    } catch (error) {
        console.error('Failed to check sidebar updates:', error);
    }
}

/**
 * Check if the current content file has been updated and reload if necessary
 */
async function checkContentUpdates() {
    if (!currentContentFile) return;
    
    try {
        // Add cache-busting parameter
        const timestamp = new Date().getTime();
        const response = await fetch(currentContentFile + '?t=' + timestamp, { method: 'HEAD' });
        
        if (!response.ok) {
            return;
        }
        
        // Get last modified time from headers if available
        const lastModified = response.headers.get('Last-Modified');
        if (lastModified) {
            const modifiedTime = new Date(lastModified).getTime();
            
            // If content has been modified, reload it
            if (modifiedTime > lastContentModified) {
                console.log('Content updated, reloading...');
                
                // Reload based on file type
                if (currentContentFile === 'welcome.md') {
                    await loadWelcomeContent();
                } else if (currentContentFile.endsWith('.md')) {
                    // For other markdown files, reload the content
                    const contentArea = document.getElementById('content-area');
                    const response = await fetch(currentContentFile + '?t=' + timestamp);
                    if (response.ok) {
                        const content = await response.text();
                        contentArea.innerHTML = marked.parse(content);
                        lastContentModified = modifiedTime;
                    }
                }
            }
        }
    } catch (error) {
        console.error('Failed to check content updates:', error);
    }
}

/**
 * Setup click handlers for navigation
 * All links open in positioned windows
 */
function setupNavigation() {
    document.querySelectorAll('#sidebar a').forEach(link => {
        link.addEventListener('click', e => {
            e.preventDefault();
            
            const url = link.href;
            const title = link.textContent.trim();
            
            // Check if it's a markdown file
            if (url.endsWith('.md')) {
                openMarkdownInWindow(url, title);
            } else {
                openWindow(url, title);
            }
        });
    });
}

/**
 * Open markdown file in a positioned window with rendering
 * @param {string} url - URL to the markdown file
 * @param {string} title - Window title
 */
function openMarkdownInWindow(url, title) {
    // Update current content file for auto-refresh
    currentContentFile = url;
    
    // Create a new window
    const width = 800;
    const height = Math.max(600, window.screen.height - 100); // Use most of the screen height
    const left = window.screenX + 300; // Position to the right of sidebar
    const top = window.screenY;
    
    // Generate a unique window name based on URL to prevent conflicts when
    // opening the same markdown file multiple times. This ensures we can
    // properly detect and reuse existing windows without causing blank content.
    const windowName = `markdown_${url.replace(/[^a-zA-Z0-9]/g, '_')}`;
    const newWindow = window.open('', windowName, `width=${width},height=${height},left=${left},top=${top}`);
    
    if (!newWindow) {
        alert('Popup blocked! Please allow popups for this site.');
        return;
    }
    
    // If the window already has our custom content, just focus it and return
    if (newWindow.document.querySelector('#content') && 
        newWindow.document.title === title) {
        newWindow.focus();
        return;
    }
    
    // Set window properties
    newWindow.document.title = title;
    
    // Show loading indicator
    newWindow.document.body.innerHTML = '<p>Loading...</p>';
    
    // Load and render markdown content
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Failed to load ${url}: ${response.status} ${response.statusText}`);
            }
            
            // Get last modified time from headers if available
            const lastModified = response.headers.get('Last-Modified');
            if (lastModified) {
                lastContentModified = new Date(lastModified).getTime();
            }
            
            return response.text();
        })
        .then(markdown => {
            // Create HTML content for the new window
            const htmlContent = `
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
                <meta http-equiv="Pragma" content="no-cache">
                <meta http-equiv="Expires" content="0">
                <title>${title}</title>
                <style>
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                    }
                    pre {
                        background: #f8f9fa;
                        padding: 10px;
                        border-radius: 5px;
                        overflow-x: auto;
                    }
                    code {
                        background: #f8f9fa;
                        padding: 2px 5px;
                        border-radius: 3px;
                        font-family: monospace;
                    }
                    img {
                        max-width: 100%;
                        height: auto;
                    }
                    blockquote {
                        border-left: 4px solid #ddd;
                        padding-left: 10px;
                        color: #666;
                        margin-left: 0;
                    }
                    h1, h2, h3 {
                        color: #2c3e50;
                    }
                    a {
                        color: #007bff;
                        text-decoration: none;
                    }
                    a:hover {
                        text-decoration: underline;
                    }
                    .filename {
                        color: #6c757d;
                        font-size: 0.9em;
                        margin-bottom: 20px;
                    }
                </style>
            </head>
            <body>
                <div class="filename">File: ${url.split('/').pop()}</div>
                <div id="content"></div>
                <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
                <script>
                    // Configure marked
                    marked.setOptions({
                        headerIds: false,
                        mangle: false,
                        breaks: true
                    });
                    
                    // Render markdown content
                    const markdownContent = ${JSON.stringify(markdown)};
                    document.getElementById('content').innerHTML = marked.parse(markdownContent);
                    
                    // Handle image errors
                    document.querySelectorAll('img').forEach(img => {
                        img.onerror = function() {
                            this.onerror = null;
                            this.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"%3E%3Cpath fill="%23ccc" d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z" /%3E%3C/svg%3E';
                            this.style.background = '#f8f9fa';
                            this.style.padding = '10px';
                        };
                    });
                </script>
            </body>
            </html>
            `;
            
            // Write content to the new window
            newWindow.document.open();
            newWindow.document.write(htmlContent);
            newWindow.document.close();
        })
        .catch(error => {
            console.error('Failed to open markdown:', error);
            alert(`Failed to open markdown file: ${error.message}`);
        });
}

/**
 * Open a URL in a positioned window
 * @param {string} url - URL to open
 * @param {string} title - Window title
 */
function openWindow(url, title) {
    try {
        // Calculate window size and position
        const sidebar = document.getElementById('sidebar');
        const sidebarWidth = sidebar.offsetWidth;
        const windowWidth = window.screen.width - sidebarWidth - 50;
        const windowHeight = window.screen.height - 100;
        
        // Position window next to sidebar
        const features = [
            `width=${windowWidth}`,
            `height=${windowHeight}`,
            `left=${sidebarWidth + 25}`,
            `top=50`,
            'menubar=yes',
            'toolbar=yes',
            'location=yes',
            'status=yes',
            'resizable=yes'
        ].join(',');
        
        // Open URL in new window
        window.open(url, title, features);
    } catch (error) {
        console.error('Failed to open window:', error);
        alert(`Failed to open window: ${error.message}`);
    }
}

/**
 * Publish changes to GitHub Pages
 * Executes a git add, commit, and push operation
 * 
 * IMPORTANT: This is separate from regular code updates.
 * Only this publish function will update the GitHub Pages site.
 */
function publishToGitHub() {
    // Show confirmation dialog
    if (!confirm('Are you sure you want to publish to GitHub Pages?\n\nThis will copy files from working-version/docs to docs and update the live site.')) {
        return;
    }
    
    // Create a popup window to show the publishing process
    const publishWindow = window.open('', 'Publishing to GitHub Pages', 'width=600,height=400,resizable=yes');
    publishWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Publishing to GitHub Pages</title>
            <style>
                body {
                    font-family: monospace;
                    padding: 20px;
                    background: #f8f9fa;
                }
                h2 {
                    color: #2c3e50;
                }
                #output {
                    background: #000;
                    color: #fff;
                    padding: 15px;
                    border-radius: 5px;
                    height: 250px;
                    overflow-y: auto;
                    white-space: pre-wrap;
                }
                .success {
                    color: #28a745;
                    font-weight: bold;
                }
                .error {
                    color: #dc3545;
                    font-weight: bold;
                }
                .status-button {
                    display: inline-block;
                    margin-top: 15px;
                    padding: 8px 16px;
                    background-color: #6c757d;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                    font-weight: bold;
                }
                .status-button:hover {
                    background-color: #5a6268;
                }
                .important-note {
                    margin-top: 15px;
                    padding: 10px;
                    background-color: #f8d7da;
                    border: 1px solid #f5c6cb;
                    border-radius: 4px;
                    color: #721c24;
                }
            </style>
        </head>
        <body>
            <h2>Publishing to GitHub Pages</h2>
            <div id="output">Starting publish process...</div>
        </body>
        </html>
    `);
    
    // Function to update the output in the popup window
    const updateOutput = (message, isError = false, isSuccess = false) => {
        const outputDiv = publishWindow.document.getElementById('output');
        const messageClass = isError ? 'error' : (isSuccess ? 'success' : '');
        
        if (messageClass) {
            outputDiv.innerHTML += `<div class="${messageClass}">${message}</div>`;
        } else {
            outputDiv.innerHTML += message + '\n';
        }
        
        // Scroll to bottom
        outputDiv.scrollTop = outputDiv.scrollHeight;
    };
    
    // Call the server endpoint to trigger the publish script
    updateOutput('Connecting to server...');
    
    fetch('/publish')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Show the full output
                updateOutput(data.output);
                updateOutput('Publishing complete! Your changes are now live at:', false, true);
                updateOutput(githubPagesUrl, false, true);
                
                // Add a button to check deployment status
                const body = publishWindow.document.querySelector('body');
                const statusButton = publishWindow.document.createElement('a');
                statusButton.href = githubStatusUrl;
                statusButton.target = '_blank';
                statusButton.className = 'status-button';
                statusButton.textContent = 'Check Deployment Status';
                body.appendChild(statusButton);
                
                updateOutput('\nNote: It may take a few minutes for changes to appear on GitHub Pages.', false, true);
            } else {
                // Show error
                updateOutput('Error during publishing:', true);
                updateOutput(data.error || 'Unknown error', true);
            }
        })
        .catch(error => {
            updateOutput('Failed to connect to server:', true);
            updateOutput(error.message, true);
        });
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', initDashboard);

```

### docs/css/styles.css
```css
/**
 * Static Sidebar Dashboard Styles
 * 
 * Core styles for:
 * 1. Sidebar layout and appearance
 * 2. Typography and colors
 * 3. Link handling
 * 4. Content area
 */

/* Layout */
body {
    margin: 0;
    height: 100vh;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    display: flex;
    overflow: hidden;
}

#sidebar {
    width: 300px;
    height: 100vh;
    overflow-y: auto;
    padding: 20px;
    background: #f8f9fa;
    border-right: 1px solid #dee2e6;
    box-sizing: border-box;
    flex-shrink: 0;
    position: relative;
}

#content-area {
    flex-grow: 1;
    height: 100vh;
    overflow-y: auto;
    padding: 30px;
    box-sizing: border-box;
}

/* Typography */
h1, h2, h3 {
    color: #2c3e50;
    margin-top: 0;
}

code {
    background: #f8f9fa;
    padding: 2px 5px;
    border-radius: 3px;
    font-family: monospace;
}

pre {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 5px;
    overflow-x: auto;
    border: 1px solid #dee2e6;
}

blockquote {
    border-left: 4px solid #dee2e6;
    padding-left: 15px;
    color: #6c757d;
    margin-left: 0;
}

/* Links */
a {
    color: #007bff;
    text-decoration: none;
    display: block;
    padding: 3px 0;
}

a:hover {
    text-decoration: underline;
}

/* All links get an arrow since they open in windows */
a::after {
    content: " ↗";
    font-size: 0.8em;
}

/* Content area links should be inline */
#content-area a {
    display: inline;
}

/* Sidebar specific */
.sidebar-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
    color: #2c3e50;
}

.section-title {
    font-size: 18px;
    font-weight: bold;
    margin: 15px 0;
    color: #34495e;
}

/* Publish button and related elements */
.publish-button {
    display: block;
    width: 100%;
    padding: 10px;
    background-color: #28a745;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    margin-bottom: 10px;
    text-align: center;
}

.publish-button:hover {
    background-color: #218838;
}

.publish-url {
    font-size: 14px;
    margin-bottom: 5px;
    word-break: break-all;
}

.publish-url a {
    color: #0366d6;
    text-decoration: none;
}

.publish-url a:hover {
    text-decoration: underline;
}

.status-link {
    font-size: 14px;
    margin-bottom: 15px;
    text-align: center;
}

.status-link a {
    color: #6c757d;
    text-decoration: none;
    padding: 3px 8px;
    border: 1px solid #6c757d;
    border-radius: 3px;
    background-color: #f8f9fa;
}

.status-link a:hover {
    background-color: #e9ecef;
    text-decoration: none;
}

/* Lists */
ul {
    list-style: none;
    padding-left: 0;
}

#content-area ul {
    list-style: disc;
    padding-left: 20px;
}

#content-area ol {
    padding-left: 20px;
}

li {
    margin: 5px 0;
}

/* Dividers */
hr {
    border: none;
    border-top: 1px solid #dee2e6;
    margin: 20px 0;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    body {
        flex-direction: column;
    }
    
    #sidebar {
        width: 100%;
        height: auto;
        max-height: 50vh;
    }
    
    #content-area {
        height: auto;
    }
}

```

## Restoration Instructions

If system files become corrupted, follow these steps to restore them:

1. Copy the content of each file from this document
2. Create or replace the corresponding file in the project
3. Ensure proper file encoding (UTF-8) and line endings

## Recovery Script Example

An AI assistant or developer could use the following script to restore system files:

```python
import os

def ensure_directory_exists(directory):
    """Ensure that a directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def write_file(path, content):
    """Write content to a file, creating directories if needed."""
    directory = os.path.dirname(path)
    ensure_directory_exists(directory)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Restored: {path}")

# Base directory
base_dir = "/path/to/SD4D/docs"  # Replace with actual path

# Restore index.html
index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta http-equiv="Cache-Control" content="no-store, no-cache, must-revalidate, max-age=0">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>Static Sidebar Dashboard</title>
    <link rel="stylesheet" href="css/styles.css">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="js/viewer.js"></script>
</head>
<body>
    <div id="sidebar"></div>
    <div id="content-area"></div>
</body>
</html>"""

write_file(os.path.join(base_dir, "index.html"), index_html)

# Restore viewer.js (content omitted for brevity)
# write_file(os.path.join(base_dir, "js/viewer.js"), viewer_js)

# Restore styles.css (content omitted for brevity)
# write_file(os.path.join(base_dir, "css/styles.css"), styles_css)

print("System files restoration complete!")
```

## Update Protocol (Developer Mode Only)

This document should only be updated when system files are intentionally improved.
To update:

1. Verify you are in Developer Mode
2. Request explicit permission from the project developer
3. Make necessary changes to system files
4. Update this document with the new file contents
5. Document the changes and rationale

### Recent Updates

**2025-03-15**: Initial creation of System_files.md
- Added documentation for index.html, viewer.js, and styles.css
- Included restoration instructions and update protocol
- Fixed bug where clicking the same sidebar link twice caused content to go blank
- Improved window height to use most of available screen space
