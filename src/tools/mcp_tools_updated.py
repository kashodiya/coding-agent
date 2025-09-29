
"""
MCP tools for common developer tasks.
"""
from typing import List, Dict, Any, Optional
import os
import glob
import json
from fastmcp import FastMCP

# Create a FastMCP server instance
mcp = FastMCP(name="AI Coding Agent MCP Server")

@mcp.tool()
def read_file(path: str) -> str:
    """
    Read the contents of a file.
    
    Args:
        path: Path to the file to read
    
    Returns:
        The contents of the file as a string
    """
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

@mcp.tool()
def write_file(path: str, content: str) -> str:
    """
    Write content to a file.
    
    Args:
        path: Path to the file to write
        content: Content to write to the file
    
    Returns:
        A success or error message
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w") as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing to file: {str(e)}"

@mcp.tool()
def list_directory(path: str, pattern: Optional[str] = None) -> List[str]:
    """
    List files and directories in a directory.
    
    Args:
        path: Path to the directory to list
        pattern: Optional glob pattern to filter files
    
    Returns:
        A list of file and directory names
    """
    try:
        if pattern:
            return glob.glob(os.path.join(path, pattern))
        else:
            return os.listdir(path)
    except Exception as e:
        return [f"Error listing directory: {str(e)}"]

@mcp.tool()
def create_directory(path: str) -> str:
    """
    Create a directory.
    
    Args:
        path: Path to the directory to create
    
    Returns:
        A success or error message
    """
    try:
        os.makedirs(path, exist_ok=True)
        return f"Successfully created directory {path}"
    except Exception as e:
        return f"Error creating directory: {str(e)}"

@mcp.tool()
def delete_file(path: str) -> str:
    """
    Delete a file.
    
    Args:
        path: Path to the file to delete
    
    Returns:
        A success or error message
    """
    try:
        os.remove(path)
        return f"Successfully deleted {path}"
    except Exception as e:
        return f"Error deleting file: {str(e)}"

@mcp.tool()
def file_exists(path: str) -> bool:
    """
    Check if a file exists.
    
    Args:
        path: Path to the file to check
    
    Returns:
        True if the file exists, False otherwise
    """
    return os.path.isfile(path)

@mcp.tool()
def directory_exists(path: str) -> bool:
    """
    Check if a directory exists.
    
    Args:
        path: Path to the directory to check
    
    Returns:
        True if the directory exists, False otherwise
    """
    return os.path.isdir(path)

@mcp.tool()
def execute_command(command: str) -> Dict[str, Any]:
    """
    Execute a shell command.
    
    Args:
        command: Command to execute
    
    Returns:
        A dictionary containing stdout, stderr, and return code
    """
    try:
        import subprocess
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "returncode": -1
        }

def create_mcp_server():
    """Create and configure the MCP server with developer tools."""
    # The server is already configured with tools via decorators
    return mcp

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
