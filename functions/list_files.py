import os
from google.genai.types import FunctionDeclaration
from google.genai import types
from functions.tool_contract import ToolContract


class ListFilesTool(ToolContract):
    @property
    def name(self) -> str:
        return "list_files"

    @property
    def description(self) -> str:
        return "Lists files and directories in a given path within the working directory."

    def run(self, working_directory: str, **kwargs) -> str:
        """
        Lists files and directories at the specified path within the working directory.
        """
        # Default to current directory if no path provided
        path = kwargs.get("path", ".")
        
        # Normalize common path references (e.g., "sandbox" -> ".")
        if path.lower() in ["sandbox", "sandbox/"]:
            path = "."
        
        abs_working_directory = os.path.abspath(working_directory)
        abs_path = os.path.abspath(os.path.join(working_directory, path))

        # Security check: ensure path is within working directory
        if not abs_path.startswith(abs_working_directory):
            return f'Error: "{path}" is not in the working directory'

        # Check if path exists
        if not os.path.exists(abs_path):
            return f'Error: "{path}" does not exist'

        # Check if path is a directory
        if not os.path.isdir(abs_path):
            return f'Error: "{path}" is not a directory'

        try:
            # Get all items in the directory
            items = os.listdir(abs_path)
            
            if not items:
                return f'Directory "{path}" is empty.'

            # Separate files and directories
            files = []
            directories = []
            
            for item in sorted(items):
                item_path = os.path.join(abs_path, item)
                if os.path.isdir(item_path):
                    directories.append(f"{item}/")
                else:
                    # Get file size for files
                    size = os.path.getsize(item_path)
                    if size < 1024:
                        size_str = f"{size}B"
                    elif size < 1024 * 1024:
                        size_str = f"{size / 1024:.1f}KB"
                    else:
                        size_str = f"{size / (1024 * 1024):.1f}MB"
                    files.append(f"{item} ({size_str})")

            # Build the result string
            result_parts = [f'Contents of "{path}":']
            
            if directories:
                result_parts.append("\nDirectories:")
                for directory in directories:
                    result_parts.append(f"  {directory}")
            
            if files:
                result_parts.append("\nFiles:")
                for file in files:
                    result_parts.append(f"  {file}")
            
            result_parts.append(f"\nTotal: {len(directories)} directories, {len(files)} files")
            
            return "\n".join(result_parts)

        except Exception as e:
            return f"Exception listing directory: {e}"

    @staticmethod
    def schema() -> FunctionDeclaration:
        return FunctionDeclaration(
            name="list_files",
            description="Lists files and directories in a given path within the working directory.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "path": types.Schema(
                        type=types.Type.STRING,
                        description="The path to list from the working directory. Defaults to '.' (current directory).",
                    ),
                },
            ),
        )

