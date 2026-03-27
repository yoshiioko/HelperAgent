# Helper Agent

An AI-powered coding assistant that interacts with your files using Google's Gemini API. It can list files, read content, get file properties, write files, and execute Python scripts, all within a secure sandbox directory.

## Features

- 📁 **File Operations**: List directories, read file contents, and get file properties (size, permissions, timestamps).
- ✍️ **File Writing**: Create new files or overwrite existing ones within the sandbox.
- 🏃 **Code Execution**: Run Python scripts with arguments (coming soon).
- 🤖 **AI-Powered**: Uses Google's Gemini 2.5 Flash model with function calling.
- 🔒 **Security**: All operations are sandboxed to a dedicated directory.
- 🛠️ **Extensible**: Tool-based architecture with a contract interface for easy extension.

## Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Google Gemini API key

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yoshiioko/HelperAgent.git
   cd HelperAgent
   ```

2. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Create a .env file in the project root with your API key**:
   ```bash
   echo 'GEMINI_API_KEY="your_google_gemini_api_key"' > .env
   ```

4. **Install dependencies** (uv handles this automatically):
   ```bash
   uv sync
   ```

## Usage

Run the Helper Agent with a prompt:
```bash
uv run main.py "Your prompt here"
```

Add the `--verbose` flag for detailed output including token usage:
```bash
uv run main.py "Your prompt here" --verbose
```

### Examples

**List files in the sandbox:**
```bash
uv run main.py "List all files in the directory"
```

**Read a file:**
```bash
uv run main.py "Show me the contents of lorem.txt"
```

**Get file properties:**
```bash
uv run main.py "What are the properties of lorem.txt?"
```

**Create a new file:**
```bash
uv run main.py "Create a file called greeting.txt with the text: Hello, World!"
```

**Multi-step workflow:**
```bash
uv run main.py "List all files, then read the contents of the smallest file"
```

## Architecture

The project follows a modular, production-ready architecture:

```
HelperAgent/
├── main.py                     # Entry point and agent orchestration
├── agent/
│   ├── config.py              # Agent configuration (model, iterations)
│   └── system_prompt.py       # System prompt definition
├── functions/
│   ├── tool_contract.py       # Abstract base class for tools
│   ├── tool_registry.py       # Central tool registration
│   ├── call_function.py       # Function call routing and execution
│   ├── get_file_content.py    # Tool: Read file contents
│   ├── get_file_properties.py # Tool: Get file metadata
│   ├── write_file.py          # Tool: Create/overwrite files
│   └── list_files.py          # Tool: List directory contents
└── sandbox/                    # Secure working directory for file operations
```

### Tool Contract

All tools implement the `ToolContract` abstract base class, ensuring:
- Consistent interface (`name`, `description`, `run()` method)
- Security through working directory constraints
- Easy registration and discovery via the tool registry

## Security

- **Sandboxed Operations**: All file operations are restricted to the `sandbox/` directory.
- **Path Validation**: Absolute path resolution prevents directory traversal attacks.
- **Working Directory Enforcement**: Tools validate that all paths are within the allowed directory.
- **API Key Protection**: Sensitive credentials are loaded from environment variables.

## Development

### Adding New Tools

1. Create a new tool file in `functions/` that implements `ToolContract`:
   ```python
   from functions.tool_contract import ToolContract
   
   class MyNewTool(ToolContract):
       @property
       def name(self) -> str:
           return "my_tool"
       
       @property
       def description(self) -> str:
           return "Description of what the tool does"
       
       def run(self, working_directory: str, **kwargs) -> str:
           # Implementation here
           pass
       
       @staticmethod
       def schema():
           # Gemini function schema here
           pass
   ```

2. Register the tool in `functions/tool_registry.py`:
   ```python
   from functions.my_new_tool import MyNewTool
   
   my_new_tool = MyNewTool()
   TOOL_REGISTRY = {
       # ...existing tools...
       my_new_tool.name: my_new_tool,
   }
   ```

3. Test your tool and it's automatically available to the agent!


## License

MIT License - feel free to use this project for learning and development.

## Contributing

Contributions are welcome! Please ensure all new tools:
- Implement the `ToolContract` interface
- Include proper error handling
- Follow security best practices
- Include documentation and examples

