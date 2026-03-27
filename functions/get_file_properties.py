import os
from google.genai.types import FunctionDeclaration
from google.genai import types
from functions.tool_contract import ToolContract


class GetFilePropertiesTool(ToolContract):
    @property
    def name(self) -> str:
        return "get_file_properties"

    @property
    def description(self) -> str:
        return "Gets properties of a file including size, access rights, modification time, and other metadata."

    def run(self, working_directory: str, **kwargs) -> str:
        """
        Returns metadata about a file including size, permissions, and timestamps.
        """
        file_path = kwargs.get("file_path")
        if not file_path:
            return 'Error: "file_path" argument is required'

        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Security check: ensure file is within working directory
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: "{file_path}" is not in the working directory'

        # Check if file exists
        if not os.path.exists(abs_file_path):
            return f'Error: "{file_path}" does not exist'

        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" is not a file'

        try:
            # Get file stats
            stats = os.stat(abs_file_path)
            
            # Format file size in human-readable format
            size_bytes = stats.st_size
            if size_bytes < 1024:
                size_str = f"{size_bytes} bytes"
            elif size_bytes < 1024 * 1024:
                size_str = f"{size_bytes / 1024:.2f} KB"
            elif size_bytes < 1024 * 1024 * 1024:
                size_str = f"{size_bytes / (1024 * 1024):.2f} MB"
            else:
                size_str = f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

            # Get file permissions in octal format (e.g., 0o644)
            permissions = oct(stats.st_mode)[-3:]
            
            # Format timestamps
            from datetime import datetime
            modified_time = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            accessed_time = datetime.fromtimestamp(stats.st_atime).strftime('%Y-%m-%d %H:%M:%S')
            created_time = datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')

            # Build the result string
            result = (
                f'File Properties for "{file_path}":\n'
                f'- Size: {size_str} ({size_bytes} bytes)\n'
                f'- Permissions: {permissions}\n'
                f'- Last Modified: {modified_time}\n'
                f'- Last Accessed: {accessed_time}\n'
                f'- Created/Changed: {created_time}\n'
                f'- Is Readable: {os.access(abs_file_path, os.R_OK)}\n'
                f'- Is Writable: {os.access(abs_file_path, os.W_OK)}\n'
                f'- Is Executable: {os.access(abs_file_path, os.X_OK)}'
            )

            return result

        except Exception as e:
            return f"Exception getting file properties: {e}"

    @staticmethod
    def schema() -> FunctionDeclaration:
        return FunctionDeclaration(
            name="get_file_properties",
            description="Gets properties of a file including size, access rights, modification time, and other metadata.",
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
