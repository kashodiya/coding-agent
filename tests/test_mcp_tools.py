


"""
Tests for the MCP tools.
"""
import os
import sys
import unittest
import tempfile
import shutil

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tools.mcp_tools import FileSystemTools, ShellTools, mcp_server

class TestFileSystemTools(unittest.TestCase):
    """Test the FileSystemTools class."""
    
    def setUp(self):
        """Set up the test environment."""
        self.tools = FileSystemTools()
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test.txt")
        with open(self.test_file, "w") as f:
            f.write("test content")
    
    def tearDown(self):
        """Clean up the test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_read_file(self):
        """Test the read_file method."""
        content = self.tools.read_file(self.test_file)
        self.assertEqual(content, "test content")
    
    def test_write_file(self):
        """Test the write_file method."""
        new_file = os.path.join(self.test_dir, "new.txt")
        result = self.tools.write_file(new_file, "new content")
        self.assertTrue("Successfully wrote" in result)
        with open(new_file, "r") as f:
            content = f.read()
        self.assertEqual(content, "new content")
    
    def test_list_directory(self):
        """Test the list_directory method."""
        files = self.tools.list_directory(self.test_dir)
        self.assertIn("test.txt", files)
    
    def test_file_exists(self):
        """Test the file_exists method."""
        self.assertTrue(self.tools.file_exists(self.test_file))
        self.assertFalse(self.tools.file_exists(os.path.join(self.test_dir, "nonexistent.txt")))
    
    def test_directory_exists(self):
        """Test the directory_exists method."""
        self.assertTrue(self.tools.directory_exists(self.test_dir))
        self.assertFalse(self.tools.directory_exists(os.path.join(self.test_dir, "nonexistent")))

class TestShellTools(unittest.TestCase):
    """Test the ShellTools class."""
    
    def setUp(self):
        """Set up the test environment."""
        self.tools = ShellTools()
    
    def test_execute_command(self):
        """Test the execute_command method."""
        result = self.tools.execute_command("echo 'hello world'")
        self.assertEqual(result["returncode"], 0)
        self.assertIn("hello world", result["stdout"])

if __name__ == "__main__":
    unittest.main()


