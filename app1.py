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
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/theme/dracula.min.css">
        <style>
            /* Animated gradient background */
            body {
                min-height: 100vh;
                display: flex;
                background: linear-gradient(-45deg, #1a1a2e, #16213e, #0f3460, #53354a);
                background-size: 400% 400%;
                animation: gradientBG 15s ease infinite;
                color: white;
            }

            @keyframes gradientBG {
                0% {background-position: 0% 50%;}
                50% {background-position: 100% 50%;}
                100% {background-position: 0% 50%;}
            }

            .CodeMirror {
                height: 50vh;
                border-radius: 0.75rem;
                font-size: 0.95rem;
                box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
                transition: box-shadow 0.3s ease;
            }

            .CodeMirror:hover {
                box-shadow: 0 0 35px rgba(0, 255, 255, 0.5);
            }

            /* Particle background */
            .particles {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
                z-index: -1;
            }

            .particle {
                position: absolute;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 50%;
                animation: float 20s linear infinite;
            }

            @keyframes float {
                from {
                    transform: translateY(0) scale(1);
                    opacity: 0.5;
                }
                to {
                    transform: translateY(-200vh) scale(0.5);
                    opacity: 0;
                }
            }
        </style>
    </head>
    <body class="min-h-screen flex flex-col items-center p-6 relative overflow-hidden">

        <div class="particles">
            <!-- Generate some random "particles" -->
            <script>
                for (let i = 0; i < 40; i++) {
                    const p = document.createElement('div');
                    p.className = 'particle';
                    p.style.width = `${Math.random() * 6 + 2}px`;
                    p.style.height = p.style.width;
                    p.style.left = `${Math.random() * 100}%`;
                    p.style.top = `${Math.random() * 100}%`;
                    p.style.animationDuration = `${10 + Math.random() * 30}s`;
                    document.querySelector('.particles').appendChild(p);
                }
            </script>
        </div>

        <h1 class="text-5xl font-extrabold mb-10 animate-pulse bg-gradient-to-r from-green-400 via-blue-500 to-purple-600 bg-clip-text text-transparent">
            🚀 C to Promela Converter
        </h1>

        <div class="w-full max-w-7xl flex flex-col lg:flex-row gap-10 transition-all duration-500">
            <div class="flex-1">
                <h2 class="text-2xl font-semibold mb-3">🧠 C Code</h2>
                <textarea id="c-code" class="w-full"></textarea>
                <button id="convert-btn"
                        class="mt-4 bg-gradient-to-r from-green-500 via-blue-500 to-purple-500 hover:from-green-600 hover:via-blue-600 hover:to-purple-600 text-white px-6 py-3 rounded-lg font-semibold shadow-lg transform hover:scale-105 transition-all duration-300">
                    🔁 Convert to Promela
                </button>
            </div>

            <div class="flex-1">
                <h2 class="text-2xl font-semibold mb-3">📜 Promela Code</h2>
                <textarea id="promela-code" class="w-full" readonly></textarea>
            </div>
        </div>

        <div id="toast"
            class="fixed bottom-4 left-1/2 transform -translate-x-1/2 px-6 py-3 rounded-lg shadow-lg hidden text-white transition-all duration-300"></div>

        <!-- CodeMirror Dependencies -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/clike/clike.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/plaintext/plaintext.min.js"></script>

        <script>
            const cEditor = CodeMirror.fromTextArea(document.getElementById("c-code"), {
                lineNumbers: true,
                mode: "text/x-csrc",
                theme: "dracula",
                tabSize: 4,
                indentUnit: 4,
            });

            const promelaEditor = CodeMirror.fromTextArea(document.getElementById("promela-code"), {
                lineNumbers: true,
                mode: "text/plain",
                theme: "dracula",
                readOnly: true,
            });

            const showToast = (msg, type) => {
                const toast = document.getElementById("toast");
                toast.className = `fixed bottom-4 left-1/2 transform -translate-x-1/2 px-6 py-3 rounded-lg shadow-lg text-white transition-all duration-300 ${type === 'error' ? 'bg-red-500' : 'bg-green-500'}`;
                toast.textContent = msg;
                toast.classList.remove("hidden");
                setTimeout(() => {
                    toast.classList.add("hidden");
                }, 3000);
            };

            document.getElementById('convert-btn').addEventListener('click', async () => {
                const cCode = cEditor.getValue();
                promelaEditor.setValue('');

                if (!cCode.trim()) {
                    showToast("Please enter some C code.", "error");
                    return;
                }

                showToast("Converting...", "success");

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
                        showToast("Conversion successful!", "success");
                    } else {
                        showToast("Error: " + result.error, "error");
                    }
                } catch (error) {
                    showToast("Error: " + error.message, "error");
                }
            });
        </script>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)