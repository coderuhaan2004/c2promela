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

def generate_context():
    with open("query/queries.json", 'r') as file:
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
    - Try to preserve the logical behavior and semantics of the C code.
    - Use Promela's constructs such as `proctype`, `chan`, `if`, `do`, and message passing when needed.
    - If concurrency or communication is implied in the C code, reflect that in Promela using parallel processes and channels.
    - Add comments to explain your translation choices where appropriate.

    Output only the translated Promela code.
    """
    return prompt

# Read C code from a file
with open("inputs/c_code.c", "r") as file:
    c_code = file.read()

# Read API key from a file
with open("api.txt", "r") as file:
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
with open("promela_code/promela.pr", "w") as f:
    f.write(response)

print("Code generated saving to promela.pr")
