
"""
AI Coding Agent using MCP and LangChain.
"""
import os
import json
import asyncio
from typing import List, Dict, Any, Optional
import httpx
from langchain_community.chat_models.bedrock import BedrockChat
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import Tool

class AICodingAgent:
    """AI Coding Agent that uses MCP tools and LLM to solve coding tasks."""
    
    def __init__(
        self, 
        mcp_server_url: str,
        model_id: str = "us.anthropic.claude-3-5-sonnet-20240620-v1:0",
        memory_key: str = "chat_history",
        verbose: bool = False
    ):
        """
        Initialize the AI Coding Agent.
        
        Args:
            mcp_server_url: URL of the MCP server
            model_id: Bedrock model ID to use
            memory_key: Key to use for memory
            verbose: Whether to print verbose output
        """
        self.mcp_server_url = mcp_server_url
        self.model_id = model_id
        self.memory_key = memory_key
        self.verbose = verbose
        
        # Initialize the LLM
        self.llm = BedrockChat(
            model_id=self.model_id,
            region_name="us-east-1",  # Set default region to us-east-1
            streaming=True,
            model_kwargs={
                "temperature": 0.2,
                "max_tokens": 4096,
            }
        )
        
        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key=self.memory_key,
            return_messages=True
        )
        
        # Create the agent prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            MessagesPlaceholder(variable_name=self.memory_key),
            ("human", "{input}"),
            ("ai", "{agent_scratchpad}"),
        ])
        
        # Initialize tools from MCP server
        self.tools = self._create_tools_from_mcp()
        
        # Create the agent
        self.agent = create_openai_tools_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # Create the agent executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=self.verbose
        )
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the agent."""
        return """
        You are an AI coding agent that helps users with software development tasks.
        
        ## Your capabilities:
        1. You can read and write files
        2. You can list directories and create directories
        3. You can execute shell commands
        4. You can check if files or directories exist
        
        ## Your approach:
        1. Break down complex tasks into smaller, manageable steps
        2. Plan your approach before executing commands
        3. Provide clear explanations of what you're doing
        4. When you encounter errors, analyze them and try to fix them
        5. Always verify your work after completing tasks
        
        ## Guidelines:
        - Be thorough and methodical in your approach
        - Explain your reasoning and decisions
        - If you're unsure about something, ask for clarification
        - Always consider best practices for software development
        - Prioritize writing clean, maintainable code
        
        Use the tools available to you to help the user with their coding tasks.
        """
    
    def _create_tools_from_mcp(self) -> List[Tool]:
        """Create LangChain tools from MCP server tools."""
        tools = []
        
        # Get the list of tools from the MCP server
        try:
            response = httpx.get(f"{self.mcp_server_url}/tools")
            response.raise_for_status()
            mcp_tools = response.json()
            
            # Create LangChain tools from MCP tools
            for tool in mcp_tools:
                tools.append(
                    Tool(
                        name=tool["name"],
                        description=tool["description"],
                        func=lambda tool_name=tool["name"], **kwargs: self._call_mcp_tool(tool_name, kwargs)
                    )
                )
        except Exception as e:
            print(f"Error getting tools from MCP server: {str(e)}")
        
        return tools
    
    def _call_mcp_tool(self, tool_name: str, params: Dict[str, Any]) -> Any:
        """Call a tool on the MCP server."""
        try:
            response = httpx.post(
                f"{self.mcp_server_url}/tools/{tool_name}",
                json=params
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return f"Error calling tool {tool_name}: {str(e)}"
    
    async def process_input(self, user_input: str) -> str:
        """
        Process user input and return the agent's response.
        
        Args:
            user_input: User's input message
            
        Returns:
            Agent's response
        """
        response = await asyncio.to_thread(self.agent_executor.invoke, {"input": user_input})
        return response["output"]
