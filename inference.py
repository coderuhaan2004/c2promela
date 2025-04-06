from google import genai
import json

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
    - Function definitions
    - Recursive functions
    - Loops (for, while, etc.)
    - Conditional blocks (if, else if, else)
    - Variable declarations
    - Function calls
    - Return statements
    - Arrays
    - Pointers (if used)
    - Structs / Enums / Macros (if any)
    - Standard library usage (e.g., printf, scanf)
    - etc.

    3. For each construct, write a short natural language query describing the scenario, such as:
    - "Define a recursive procedure"
    - "Create a loop to repeat a task"
    - "Use an if-else block to handle two different conditions"
    - "Declare an integer variable"
    - "Call the factorial function"

    4. Output the result in JSON format as a list of objects with `construct` and `query`.

    Input C code:
    ```c
    {c_code}
    ```
    """
    return prompt

# Read C code from a file
with open("c_code.c", "r") as file:
    c_code = file.read()

# Read API key from a file
with open("api.txt", "r") as file:
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
with open("outputs/response.json", "w") as json_file:
    json.dump(response, json_file, indent=4)
