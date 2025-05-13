from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import tempfile
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

@app.route('/api/convert', methods=['POST'])
def convert():
    try:
        # Get C code from request
        data = request.json
        c_code = data.get('c_code', '')
        
        if not c_code:
            return jsonify({
                'promela_code': '',
                'errors': ['No C code provided'],
                'warnings': []
            }), 400
        
        # Create a temporary directory for files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save C code to input file
            input_file = os.path.join(temp_dir, "input.c")
            with open(input_file, 'w') as f:
                f.write(c_code)
            
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            batch_file = os.path.join(BASE_DIR, "run_pipeline.bat")

            # Execute the batch file
            process = subprocess.run(
                f'"{batch_file}" "{input_file}"',
                capture_output=True,
                text=True,
                shell=True
            )
            
            # Check if there was an error
            if process.returncode != 0:
                return jsonify({
                    'promela_code': '',
                    'errors': [f"Conversion error: {process.stderr}"],
                    'warnings': []
                }), 400
            
            # Wait a moment for file operations to complete
            time.sleep(0.5)
            
            # Read the output Promela file
            promela_file = os.path.join(BASE_DIR, "promela_code", "promela.pml")  # Update with your output file path
            
            if not os.path.exists(promela_file):
                return jsonify({
                    'promela_code': '',
                    'errors': [f"Output file not found: {promela_file}"],
                    'warnings': [process.stdout]
                }), 400
            
            with open(promela_file, 'r') as f:
                promela_code = f.read()
            
            return jsonify({
                'promela_code': promela_code,
                'errors': [],
                'warnings': [process.stdout] if process.stdout else []
            })
        
    except Exception as e:
        return jsonify({
            'promela_code': '',
            'errors': [f"Server error: {str(e)}"],
            'warnings': []
        }), 500

if __name__ == '__main__':
    app.run(debug=True)