from google import genai
import json
import argparse

#Take API key from the file named api.txt

def inference(api_key, prompt):
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    return response.text

def generate_prompt(c_code):
    prompt = f"""
    You are given a C code. Your task is to:

    1. Understand the logic of the code.
    2. Identify all possible C language constructs used in the code, such as:
    - Function definitions. Whether it has arguments.
    - Recursive functions
    - Loops (for, while, etc.)
    - Conditional blocks (if, else if, else)
    - Any dynamic memory allocation (malloc, alloc or realloc)
    - Variable declarations
    - Function calls
    - Return statements
    - Arrays
    - Pointers (if used)
    - Structs / Enums / Macros (if any)
    - Standard library usage (e.g., printf, scanf)
    - etc.

    3. For each construct, write a short natural language query describing the scenario, such as:   
    - Define a basic variable with appropriate data type   
    - Create an array to store multiple values
    - Set up a communication channel between processes
    - Define a process type with specific behavior  
    - Establish synchronous communication between processes
    - Create a reusable code block with inline function
    - Define a custom data structure using typedef 
    - Implement a loop with multiple exit conditions
    - Model non-deterministic behavior with random choices
    - Ensure atomic execution of a critical section
    - Pass values between processes using shared variables
    - Run multiple processes concurrently
    - Implement conditional branching logic
    - Initialize and manipulate array elements
    - Create a switch-case equivalent structure
    - Exit a loop when a condition is met
    - Skip to the next iteration in a loop
    - Define the main entry point process
    - Send and receive messages through channels
    - Enforce sequential execution between processes

    4. Output the result in JSON format as a list of objects with `construct` and `query`.

    Input C code:
    ```c
    {c_code}
    ```
    """
    return prompt

# Set up argument parser
parser = argparse.ArgumentParser(description="Generate queries from C code.")
parser.add_argument("--input", type=str, help="Path to the input C code file.")
args = parser.parse_args()

# Check if the input file is provided
if args.input:
    input_file = args.input
else:
    input_file = "input_c/c_code.c"

# Read C code from a file
with open(input_file, "r") as file:
    c_code = file.read()

# Read API key from a file
with open("texts/api.txt", "r") as file:
    api_key = file.read().strip()

# Generate the prompt
prompt = generate_prompt(c_code)    

# Call the inference function
response = inference(api_key, prompt)

# Remove the triple backticks and 'json' tag
clean_json_str = response.strip('`').replace("json\n", "")

# Parse the cleaned JSON string
try:
    response = json.loads(clean_json_str)
except json.JSONDecodeError as e:
    print("Error decoding JSON:", e)
    response = None

# Dump the JSON response to a file
with open("outputs/first_queries.json", "w") as json_file:
    json.dump(response, json_file, indent=4)
