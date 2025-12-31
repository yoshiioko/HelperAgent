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
    if not args.user_prompt.strip():
        parser.print_usage()
        print("Error: The User Prompt cannot be empty.")
        sys.exit(1)

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = Client(api_key=api_key)

    system_prompt = """
    ...
    """

if __name__ == "__main__":
    main()
