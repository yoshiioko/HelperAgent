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
    ...
    """

    # Create the initial messages list with the user's prompt
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    # TODO: Tool setup

    # TODO: Agent configuration

    # TODO: Agent loop



if __name__ == "__main__":
    main()
