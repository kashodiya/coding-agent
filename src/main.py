"""
Main script to run the AI coding agent with a command-line interface.
"""
import os
import sys
import asyncio
import argparse
import threading
import time
from typing import Optional

from src.tools.mcp_tools_updated import create_mcp_server
from src.agent.ai_coding_agent import AICodingAgent

def start_mcp_server(host: str = "0.0.0.0", port: int = 8000) -> threading.Thread:
    """
    Start the MCP server in a separate thread.

    Args:
        host: Host to bind the server to
        port: Port to bind the server to

    Returns:
        Thread running the MCP server
    """
    server = create_mcp_server()
    
    def run_server():
        # Run the server directly without uvicorn
        server.run(transport="streamable-http", host=host, port=port)
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Give the server a moment to start
    time.sleep(2)

    return server_thread

async def chat_loop(agent: AICodingAgent):
    """
    Run the chat loop for the AI coding agent.

    Args:
        agent: The AI coding agent
    """
    print("AI Coding Agent initialized. Type 'exit' or 'quit' to end the session.")
    print("Type your questions or coding tasks below:")

    while True:
        try:
            # Get user input
            user_input = input("\n> ")

            # Check if user wants to exit
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting AI Coding Agent. Goodbye!")
                break

            # Process user input
            print("\nAI Coding Agent is thinking...")
            response = await agent.process_input(user_input)

            # Print the response
            print(f"\nAI Coding Agent: {response}")

        except KeyboardInterrupt:
            print("\nExiting AI Coding Agent. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")

async def start_agent_cli(
    mcp_server_url: str,
    model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0",
    verbose: bool = False
) -> None:
    """
    Start the AI coding agent CLI.

    Args:
        mcp_server_url: URL of the MCP server
        model_id: Bedrock model ID to use
        verbose: Whether to print verbose output
    """
    # Create the AI coding agent
    print("Initializing AI Coding Agent...")
    agent = AICodingAgent(
        mcp_server_url=mcp_server_url,
        model_id=model_id,
        verbose=verbose
    )

    # Run the chat loop
    await chat_loop(agent)

async def main():
    """Main function to run the AI coding agent."""
    parser = argparse.ArgumentParser(description="AI Coding Agent")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind the MCP server to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind the MCP server to")
    parser.add_argument("--model-id", type=str, default="anthropic.claude-3-5-sonnet-20240620-v1:0", help="Bedrock model ID to use")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    # Start the MCP server
    mcp_server_url = f"http://{args.host}:{args.port}/mcp"
    print(f"Starting MCP server at {mcp_server_url}...")
    server_thread = start_mcp_server(host=args.host, port=args.port)

    # Start the agent CLI
    await start_agent_cli(
        mcp_server_url=mcp_server_url,
        model_id=args.model_id,
        verbose=args.verbose
    )

def main_cli():
    """Entry point for the console script."""
    asyncio.run(main())

if __name__ == "__main__":
    main_cli()
