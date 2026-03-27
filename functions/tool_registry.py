"""
Tool Registry: Central place to register and look up all available tools for the agent.
Add new tools here as you implement them.
"""

from functions.get_file_content import GetFileContentTool

# Instantiate tool objects
get_file_content_tool = GetFileContentTool()

# Central registry of tools by name
TOOL_REGISTRY = {
    get_file_content_tool.name: get_file_content_tool,
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
