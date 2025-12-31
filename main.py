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
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", type=str, help="The user's prompt message.")
    parser.add_argument("--verbose", action="store_true", help="Enabled detailed output.")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = Client(api_key=api_key)

    system_prompt = """
    ...
    """

if __name__ == "__main__":
    main()
