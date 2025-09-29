

from setuptools import setup, find_packages

setup(
    name="coding-agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastmcp>=2.6.1",
        "mcp-agent>=0.1.27",
        "langchain>=0.3.27",
        "langchain-community>=0.3.30",
        "uvicorn>=0.27.0",
        "boto3>=1.34.0",
        "pydantic>=2.5.0",
        "httpx>=0.27.0",
    ],
    entry_points={
        "console_scripts": [
            "coding-agent=src.main:main_cli",
        ],
    },
    python_requires=">=3.8",
    author="AI Coding Agent Team",
    author_email="example@example.com",
    description="An AI-powered coding assistant",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/coding-agent",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

