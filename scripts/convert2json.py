import json 

constructs = {
    "Process Types": {
        "name": "proctype",
        "example": """
        proctype A()
        {   
            byte state;         // Local variable declaration
            state = 3;          // Assignment statement
        }

        proctype B()
        {   
            byte counter = 0;   // Local variable with initialization
            counter = counter + 1;
        }
        """,
        "scenario": "Used to define process types that specify the behavior of concurrent processes."
    },
    "Global Variables": {
        "name": "global variables",
        "example": """
        byte state = 2;          // Global variable with initialization

        proctype A()
        {   
            (state == 1) -> state = 3;  // Conditional assignment
        }

        proctype B()
        {   
            state = state - 1;          // Decrementing global variable
        }
        """,
        "scenario": "Used to define variables that can be accessed by multiple processes concurrently."
    },
    "Local Variables": {
        "name": "local variable declaration",
        "example": """
        proctype Test()
        {
            byte counter = 5;     // Local variable with initialization
            counter = counter + 1;
        }
        ",
        "scenario": "Used to declare variables that are only accessible within a specific process."
    },
    "Assignments": {
        "name": "assignment statement",
        "example": "
        proctype Example()
        {
            byte x = 1;           // Initialize variable
            x = x + 2;            // Increment by 2
        }
        """,
        "scenario": "Used to assign values to variables or update their values during process execution."
    },
    "Statement Separators": {
        "name": "semicolon and arrow",
        "example": """
        proctype Example()
        {
            byte val = 0;

            val = 1;             // Semicolon separator
            (val == 1) -> val = 2;  // Arrow separator with condition
        }
        """,
        "scenario": "Used to separate multiple statements in a process body. The arrow can indicate causality."
    },
    "Process Instantiation": {
        "name": "run statement",
        "example": """
        init 
        {
            run A();         // Instantiate process A
            run B();         // Instantiate process B
        }

        proctype A(byte state; short foo)
        {
            (state == 1) -> state = foo;
        }

        init
        {
            run A(1, 3);    // Pass parameters to process A
        }
       """,
        "scenario": "Used to create and execute instances of processes in the Promela model."
    },
    "Macro Definitions": {
    "name": "#define",
    "example": """"
    #define true    1         // Define true as constant 1
    #define false   0         // Define false as constant 0
    #define Aturn   false     // Define Aturn as false
    #define Bturn   true      // Define Bturn as true
    """,
    "scenario": "Used to define constant values or symbolic names in Promela specifications, similar to C-style macros."
    }
}

# Convert the constructs dictionary to JSON format
json_output = json.dumps(constructs, indent=4)

# Write the JSON output to a file
with open('promela_constructs.json', 'w') as json_file:
    json_file.write(json_output)
