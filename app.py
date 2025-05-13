import os
import uuid
import subprocess
import tempfile
from pathlib import Path
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuration
TEMP_DIR = Path(tempfile.gettempdir()) / "c_to_promela_temp"
CONVERTER_SCRIPT = Path("run_pipeline.bat")  # Update this path to your batch file
PROMELA_OUTPUT_DIR = Path("promela_code")  # Fixed directory for promela output
PROMELA_OUTPUT_FILE = PROMELA_OUTPUT_DIR / "promela.pml"  # Fixed output file
TIMEOUT_SECONDS = 300 # Timeout for the conversion process

# Ensure directories exist
TEMP_DIR.mkdir(parents=True, exist_ok=True)
PROMELA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

@app.route('/')
def index():
    """Render the main page."""
    return get_index_template()

@app.route('/api/convert', methods=['POST'])
def convert():
    data = request.json
    if not data or 'c_code' not in data:
        return jsonify({'success': False, 'error': 'No C code provided'}), 400
    
    c_code = data['c_code']
    
    # Create unique ID for this conversion
    job_id = str(uuid.uuid4())
    job_dir = TEMP_DIR / job_id
    job_dir.mkdir(exist_ok=True)
    
    try:
        # Write C code to input file
        c_file_path = job_dir / "input.c"
        with open(c_file_path, "w") as f:
            f.write(c_code)
        
        result = subprocess.run(
            [CONVERTER_SCRIPT, str(c_file_path)],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS
        )
        
        # Check if conversion was successful
        if result.returncode != 0:
            return jsonify({
                'success': False,
                'error': f"Conversion failed: {result.stderr}"
            }), 500
        
        # Read the Promela output from the fixed location: promela_code/promela.pml
        if PROMELA_OUTPUT_FILE.exists():
            with open(PROMELA_OUTPUT_FILE, "r") as f:
                promela_code = f.read()
            
            return jsonify({
                'success': True,
                'promela_code': promela_code
            })
        else:
            return jsonify({
                'success': False,
                'error': f"Output file not found at {PROMELA_OUTPUT_FILE}. Converter output: {result.stdout}"
            }), 500
            
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'error': "Conversion process timed out"
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"An error occurred: {str(e)}"
        }), 500
    finally:
        pass

@app.errorhandler(Exception)
def handle_exception(e):
    """Global error handler"""
    return jsonify({
        'success': False,
        'error': f"Server error: {str(e)}"
    }), 500

def get_index_template():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>C to Promela Converter</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/theme/material-darker.min.css">
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #1e1e1e;
                color: #f5f5f5;
            }
            .container {
                display: flex;
                gap: 20px;
            }
            .editor-container {
                flex: 1;
                display: flex;
                flex-direction: column;
            }
            h1, h2 {
                color: #ffffff;
            }
            button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
                margin-top: 10px;
                margin-bottom: 10px;
            }
            button:hover {
                background-color: #45a049;
            }
            .status {
                margin-top: 20px;
                padding: 10px;
                border-radius: 4px;
            }
            .error {
                background-color: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            .success {
                background-color: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .hidden {
                display: none;
            }
            .CodeMirror {
                height: 400px;
                border-radius: 4px;
            }
        </style>
    </head>
    <body>
        <h1>C to Promela Converter</h1>
        
        <div class="container">
            <div class="editor-container">
                <h2>C Code</h2>
                <textarea id="c-code" placeholder="Enter your C code here..."></textarea>
                <button id="convert-btn">Convert to Promela</button>
            </div>
            
            <div class="editor-container">
                <h2>Promela Code</h2>
                <textarea id="promela-code" readonly></textarea>
            </div>
        </div>
        
        <div id="status" class="status hidden"></div>

        <!-- CodeMirror JS and Mode -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/clike/clike.min.js"></script>

        <script>
            const cEditor = CodeMirror.fromTextArea(document.getElementById("c-code"), {
                lineNumbers: true,
                mode: "text/x-csrc",
                theme: "material-darker",
                tabSize: 4,
                indentUnit: 4
            });

            const promelaEditor = CodeMirror.fromTextArea(document.getElementById("promela-code"), {
                lineNumbers: true,
                mode: "text/plain",
                theme: "material-darker",
                readOnly: true
            });

            document.getElementById('convert-btn').addEventListener('click', async () => {
                const cCode = cEditor.getValue();
                const statusElement = document.getElementById('status');
                promelaEditor.setValue('');

                if (!cCode.trim()) {
                    statusElement.className = 'status error';
                    statusElement.textContent = 'Please enter C code';
                    statusElement.classList.remove('hidden');
                    return;
                }

                statusElement.className = 'status';
                statusElement.textContent = 'Converting...';
                statusElement.classList.remove('hidden');

                try {
                    const response = await fetch('/api/convert', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ c_code: cCode }),
                    });

                    const result = await response.json();

                    if (result.success) {
                        promelaEditor.setValue(result.promela_code);
                        statusElement.className = 'status success';
                        statusElement.textContent = 'Conversion successful!';
                    } else {
                        statusElement.className = 'status error';
                        statusElement.textContent = `Error: ${result.error}`;
                    }
                } catch (error) {
                    statusElement.className = 'status error';
                    statusElement.textContent = `Error: ${error.message}`;
                }
            });
        </script>
    </body>
    </html>
    """
    return html


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)