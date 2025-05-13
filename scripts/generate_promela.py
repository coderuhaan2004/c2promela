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

def generate_context():
    with open("query/promela_queries.json", 'r') as file:
        queries = json.load(file) #queries is a list
    new_queries = set(queries)
    context = ""
    for i in new_queries:
        context += i + "\n"
    return context

def generate_prompt(c_code, context):
    prompt = f"""
    You are a helpful assistant specialized in converting C code into syntactically and semantically correct Promela code.
    The following C code represents a logic or behavior that must be accurately modeled in Promela. Along with this, you are given Promela constructs that are semantically related to the functionality of the C code.

    Input C code:
    ```c
    {c_code}
    ```

    -----

    Relevant Promela Construct (Context):

    {context}

    -----

    Task Instructions:
    - Generate equivalent Promela code for the above C code.
    - Ensure syntactic correctness in Promela. Follow the structure and keywords shown in the constructs.
    - don't print the result of a function outside the function definition. Use print statements inside the function definition.
    - Remember that Promela does NOT use curly braces for loop or conditional blocks. Use '::' conditions followed by -> and proper loop terminators (do...od, if...fi).
    - Declare all variables at the beginning of blocks/functions, not inside control structures or conditionally.
    - Try to preserve the logical behavior and semantics of the C code.
    - Use Promela's constructs such as `proctype`, `chan`, `if`, `do`, and message passing when needed.
    - If concurrency or communication is implied in the C code, reflect that in Promela using parallel processes and channels.
    - Remember that Promela inline functions cannot be recursive - convert recursive algorithms to iterative ones using loops.
    - Use global variables for sharing data between processes instead of function return values.
    - Replace C pointer operations with appropriate Promela alternatives.
    - For complex data structures, use Promela's typedef to define equivalent structures.
    - Format the code for proper readability

    Output only the translated Promela code.
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

#Generate Context
contexts = generate_context()

# Generate the prompt
prompt = generate_prompt(c_code, contexts)

#Generate promela code
# Call the inference function
response = inference(api_key, prompt)

response = response.encode().decode('unicode_escape')

# Now save it to a file with actual line breaks
with open("promela_code/promela.pml", "w") as f:
    f.write(response)

print("Code generated saving to promela.pml")
