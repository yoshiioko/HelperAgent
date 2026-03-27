"""
Tool Registry: Central place to register and look up all available tools for the agent.
Add new tools here as you implement them.
"""

from functions.get_file_content import GetFileContentTool
from functions.get_file_properties import GetFilePropertiesTool
from functions.write_file import WriteFileTool

# Instantiate tool objects
get_file_content_tool = GetFileContentTool()
get_file_properties_tool = GetFilePropertiesTool()
write_file_tool = WriteFileTool()

# Central registry of tools by name
TOOL_REGISTRY = {
    get_file_content_tool.name: get_file_content_tool,
    get_file_properties_tool.name: get_file_properties_tool,
    write_file_tool.name: write_file_tool,
    # Add more tools here as you implement them
}

def get_tool(name: str):
    """Retrieve a tool by its name or None if not found."""
    return TOOL_REGISTRY.get(name)


def list_tools():
    """List all registered tool names."""
    return list(TOOL_REGISTRY.keys())


def get_tool_schemas():
    """Return a list of all registered tool schemas."""
    return [tool.schema() for tool in TOOL_REGISTRY.values()]
