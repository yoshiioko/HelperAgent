"""
Main entry point for the Helper Agent.
"""

import os
import sys
import argparse
from dotenv import load_dotenv
from google.genai import Client, types

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

    # Define a System Prompt for the agent
    system_prompt = """
    You are a helpful, concise, and proactive AI coding agent.

    Your primary role is to assist users with coding tasks by planning and executing function calls. For each user request, break down the task into clear, logical steps and use available tools to perform operations such as:

    - Listing files and directories
    - Reading the content of a file
    - Writing to a file (create or update)
    - Running a Python file with optional arguments

    When a user refers to the 'code project', they mean the current working directory. Always start by examining the project's files, understanding how to run the project and its tests, and verifying that everything works as expected.

    All file paths should be relative to the working directory. Do not include the working directory in your function calls; it is automatically handled for security.

    If an operation fails or is ambiguous, inform the user and suggest next steps. Always check for available tools before responding, as new tools may be added.

    When appropriate, confirm actions with the user and summarize results clearly. Your responses should be accurate, actionable, and easy to follow.
    """

    # Create the initial messages list with the user's prompt
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    # TODO: Tool setup

    # TODO: Agent configuration

    # TODO: Agent loop
    max_iterations = 20
    for _ in range(max_iterations):
        # 1. Send the current conversation (messages) to the Gemini model
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            # config=config TBD
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
                result = "" # TODO: Call the function and return the result
                messages.append(types.Content(role="assistant", parts=[types.Part(text=result)]))
        else:
            print(response.text)
            return


if __name__ == "__main__":
    main()
