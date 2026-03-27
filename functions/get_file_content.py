import os
from google.genai.types import FunctionDeclaration
from google.genai import types
from functions.tool_contract import ToolContract

MAX_CHARS = 10000  # You may want to import this from a config file

class GetFileContentTool(ToolContract):
    @property
    def name(self) -> str:
        return "get_file_content"

    @property
    def description(self) -> str:
        return "Gets the contents of the given file as a string, constrained to the working directory."

    def run(self, working_directory: str, **kwargs) -> str:
        """
        Reads and returns the contents of a file within the working directory.
        """
        file_path = kwargs.get("file_path")
        if not file_path:
            return 'Error: "file_path" argument is required'

        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: "{file_path}" is not in the working directory'

        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" is not a file'

        try:
            with open(abs_file_path, "r") as file:
                file_content_string = file.read(MAX_CHARS)
                if len(file_content_string) >= MAX_CHARS:
                    file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
        except Exception as e:
            return f"Exception reading file: {e}"

    @staticmethod
    def schema() -> FunctionDeclaration:
        return FunctionDeclaration(
            name="get_file_content",
            description="Gets the contents of the given file as a string, constrained to the working directory.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="The path to the file from the working directory.",
                    ),
                },
            ),
        )

