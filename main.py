"""
Main entry point for the Helper Agent.
"""

import os
import sys
import argparse
from dotenv import load_dotenv
from google.genai import Client, types
from functions.call_function import call_function
from functions.tool_registry import get_tool_schemas
from agent.system_prompt import system_prompt
from agent.config import MODEL_NAME, MAX_ITERATIONS

def main():
    """
    Runs the Helper Agent conversation loop

    Command-line Args:
        prompt: The user's prompt message (required)
        --verbose: Flag for detailed output (optional)

    Exits:
        System exits with code 0 on success, 1 on failure.
    """
    # Use argument parser for command-line arguments
    parser = argparse.ArgumentParser(
        description="Run the Helper Agent conversation loop.",
        usage='uv run main.py "User Prompt" [--verbose]'
    )
    parser.add_argument("user_prompt", type=str, help="The user's prompt message.")
    parser.add_argument("--verbose", action="store_true", help="Enabled detailed output.")
    args = parser.parse_args()

    # Check if the prompt is empty or only whitespace
    user_prompt = args.user_prompt.strip()
    if not user_prompt:
        parser.print_usage()
        print("Error: The User Prompt cannot be empty.")
        sys.exit(1)

    # Load environment variables from .env file
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # Initialize Gemini API Client with an API key
    client = Client(api_key=api_key)

    # Create the initial messages list with the user's prompt
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    # Tool setup: collect all tool schemas from the registry
    tool_schemas = get_tool_schemas()

    # Agent configuration: register tool schemas with Gemini
    available_functions = types.Tool(function_declarations=tool_schemas)
    config = types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
    )

    # Agent loop
    for _ in range(MAX_ITERATIONS):
        # 1. Send the current conversation (messages) to the Gemini model
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=messages,
            config=config
        )

        # 2. Check if the response is valid
        if response is None or response.usage_metadata is None:
            print("Response is malformed or missing usage metadata. Exiting...")
            return sys.exit(1)

        # 3. (Optional) Print verbose information if enabled
        if args.verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        # 4. Add the model's response to the messages list
        if response.candidates:
            for candidate in response.candidates:
                if candidate and candidate.content:
                    messages.append(candidate.content)

        # 5. Handle function calls if present. If not, print the final answer and exit.
        if response.function_calls:
            for function_call_part in response.function_calls:
                tool_response = call_function(
                    function_call_part,
                    verbose=args.verbose
                )
                messages.append(tool_response)
        else:
            print(response.text)
            return


if __name__ == "__main__":
    main()
