import os
from google.genai.types import FunctionDeclaration
from google.genai import types
from functions.tool_contract import ToolContract


class WriteFileTool(ToolContract):
    @property
    def name(self) -> str:
        return "write_file"

    @property
    def description(self) -> str:
        return "Writes content to a file (creates new file or overwrites existing), constrained to the working directory."

    def run(self, working_directory: str, **kwargs) -> str:
        """
        Writes content to a file within the working directory.
        Creates the file if it doesn't exist, or overwrites if it does.
        """
        file_path = kwargs.get("file_path")
        content = kwargs.get("content")
        
        if not file_path:
            return 'Error: "file_path" argument is required'
        
        if content is None:  # Allow empty string but not None
            return 'Error: "content" argument is required'

        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Security check: ensure file is within working directory
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: "{file_path}" is not in the working directory'

        try:
            # Create parent directories if they don't exist
            parent_dir = os.path.dirname(abs_file_path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir)

            # Write content to file
            with open(abs_file_path, "w") as file:
                file.write(content)

            # Check if file was created or overwritten
            file_status = "created" if not os.path.exists(abs_file_path) else "overwritten"
            file_size = os.path.getsize(abs_file_path)
            
            return (
                f'Successfully wrote to "{file_path}".\n'
                f'- Bytes written: {file_size}\n'
                f'- Status: File {file_status}'
            )

        except Exception as e:
            return f"Exception writing file: {e}"

    @staticmethod
    def schema() -> FunctionDeclaration:
        return FunctionDeclaration(
            name="write_file",
            description="Writes content to a file (creates new file or overwrites existing), constrained to the working directory.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="The path to the file from the working directory.",
                    ),
                    "content": types.Schema(
                        type=types.Type.STRING,
                        description="The content to write to the file.",
                    ),
                },
                required=["file_path", "content"],
            ),
        )

