import os
from functions.tool_registry import TOOL_REGISTRY
from google.genai import types

# Define the sandbox directory for all tool operations
SANDBOX_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sandbox")
if not os.path.exists(SANDBOX_DIR):
    os.makedirs(SANDBOX_DIR)


def call_function(function_call_part, verbose=False):
    """
    Routes and executes function calls from the AI agent, returning results as tool responses.
    Uses SANDBOX_DIR as the working directory for all tools.
    """
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function: {function_call_part.name}")

    tool = TOOL_REGISTRY.get(function_call_part.name)
    if tool:
        result = tool.run(SANDBOX_DIR, **(function_call_part.args or {}))
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
