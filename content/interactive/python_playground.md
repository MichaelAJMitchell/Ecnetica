# Interactive Python

```{raw} html
<!doctype html>
<html>
  <head>
    <title>Pyodide Python Playground (Sphinx Compatible)</title>
    <!-- Only load Pyodide if not already loaded -->
    <script>
      if (typeof loadPyodide === 'undefined') {
        document.write('<script src="https://cdn.jsdelivr.net/pyodide/v0.27.7/full/pyodide.js"><\/script>');
      }
    </script>
  </head>
  <body>
    <h1>Pyodide Test Page</h1>
    <p>Open your browser console to see Pyodide output</p>
    
    <div id="output"></div>
    <button onclick="runPythonScript()" style="padding: 10px; margin: 10px; font-size: 16px;">
      Run Python Script
    </button>
    
    <script type="text/javascript">
      let pyodideInstance = null;
      
      async function initializePyodide() {
        if (pyodideInstance) {
          return pyodideInstance;
        }
        
        try {
          console.log("Loading Pyodide...");
          pyodideInstance = await loadPyodide();
          console.log("Pyodide loaded successfully!");

          // Test basic Python execution
          console.log("Testing basic Python:");
          pyodideInstance.runPython("print('Hello from Pyodide!')");
          pyodideInstance.runPython("print(1 + 3)");

          // Load required packages
          // we need these cause the imported file needs them

          console.log("Loading required packages...");
          await pyodideInstance.loadPackage(["numpy", "matplotlib", "scipy", "networkx"]);
          console.log("Packages loaded successfully!");
          
          return pyodideInstance;
          
        } catch (error) {
          console.error("Error initializing Pyodide:", error);
          throw error;
        }
      }
      
      async function runPythonScript() {
        try {
          const pyodide = await initializePyodide();
          
          console.log("Fetching Python file...");
          const response = await fetch("http://0.0.0.0:8000/mcq_algorithm_full_python.py");
          
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          
          const code = await response.text();
          console.log("Python file fetched successfully");
          
          // Write the file to Pyodide's filesystem
          pyodide.FS.writeFile("script.py", code);
          
          // Import and run the script
          // the sys here functions like how __init__ does on the virtual file system

          await pyodide.runPythonAsync(`
            import sys
            sys.path.append('.')
            import script
          `);
          
          // Run the test function
          const result = pyodide.runPython('script.simple_test()');
          console.log("Test result:", result);
          
          // Display result on page
          // Will be using this to run kg graph stuff with bkt

          document.getElementById('output').innerHTML = `<h3>Script executed successfully!</h3><p>Check console for details.</p><pre>Result: ${result}</pre>`;
          
        } catch (error) {
          console.error("Error running Python script:", error);
          document.getElementById('output').innerHTML = `<h3>Error:</h3><pre style="color: red;">${error.message}</pre>`;
        }
      }
      
      // Auto-initialize when page loads
      document.addEventListener('DOMContentLoaded', async function() {
        try {
          await initializePyodide();
          document.getElementById('output').innerHTML = '<p style="color: green;">✓ Pyodide ready! Click the button to run your script.</p>';
        } catch (error) {
          document.getElementById('output').innerHTML = `<p style="color: red;">✗ Failed to initialize Pyodide: ${error.message}</p>`;
        }
      });
    </script>
  </body>
</html>