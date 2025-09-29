# AI Coding Agent

An AI-powered coding assistant that helps with software development tasks.

## Features

- Uses FastMCP to create a server with tools for common developer tasks
- Implements an AI coding agent using mcp-agent
- Connects to Bedrock LLM (Claude 3.5 Sonnet)
- Provides a command-line chat interface
- Supports file operations, directory management, and shell command execution

## Requirements

- Python 3.8+
- FastMCP
- mcp-agent
- LangChain
- AWS Bedrock access

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/coding-agent.git
cd coding-agent
```

2. Install the required packages:
```bash
pip install fastmcp mcp-agent langchain langchain-community
```

3. Set up AWS credentials for Bedrock:
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=us-east-1  # Default region is us-east-1
```

## Usage

Run the AI coding agent (this will automatically start the MCP server):

```bash
cd coding-agent
python run.py
```

Alternatively, you can use:
```bash
cd coding-agent
python -m src.main
```

Optional arguments:
- `--host`: Host to bind the MCP server to (default: 0.0.0.0)
- `--port`: Port to bind the MCP server to (default: 8000)
- `--model-id`: Bedrock model ID to use (default: us.anthropic.claude-3-5-sonnet-20240620-v1:0)
- `--verbose`: Enable verbose output

## Example Interactions

```
> Create a simple Flask application that displays "Hello, World!"

AI Coding Agent: I'll help you create a simple Flask application. Let me break this down into steps:

1. First, I'll check if Flask is installed
2. Create a basic Flask application file
3. Run the application to test it

Let me start by checking if Flask is installed...

[Agent executes commands and creates files]

I've created a simple Flask application for you. Here's what I did:

1. Created a file named app.py with the following code:
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
```

2. You can run this application with:
```bash
python app.py
```

The application will be available at http://127.0.0.1:5000/
```

## Architecture

- **MCP Server**: Provides tools for file operations, directory management, and shell commands
- **AI Coding Agent**: Uses LangChain and Bedrock to process user requests and execute appropriate actions
- **Command-line Interface**: Allows users to interact with the agent through a simple chat interface

## License

MIT
