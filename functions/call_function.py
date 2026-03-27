from functions.tool_registry import TOOL_REGISTRY
from google.genai import types


def call_function(function_call_part, working_directory, verbose=False):
    """
    Routes and executes function calls from the AI agent, returning results as tool responses.
    """
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function: {function_call_part.name}")

    tool = TOOL_REGISTRY.get(function_call_part.name)
    if tool:
        result = tool.run(working_directory, **(function_call_part.args or {}))
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

