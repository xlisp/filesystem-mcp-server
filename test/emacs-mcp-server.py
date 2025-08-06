#!/usr/bin/env python3
"""
Emacs MCP Server - Provides tools to interact with Emacs via emacsclient and system commands
"""

import subprocess
import os
import tempfile
import json
import shlex
from typing import Any, Optional
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("emacs-server")

def run_emacsclient(command: str, timeout: int = 10) -> tuple[bool, str]:
    """Execute emacsclient command and return success status and output."""
    try:
        # Check if emacsclient is available
        result = subprocess.run(
            ["emacsclient", "--eval", command],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout.strip() or result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except FileNotFoundError:
        return False, "emacsclient not found. Make sure Emacs server is running."
    except Exception as e:
        return False, f"Error executing command: {str(e)}"

def run_shell_command(command: str, timeout: int = 30) -> tuple[bool, str]:
    """Execute shell command safely."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        output = result.stdout.strip()
        error = result.stderr.strip()
        return result.returncode == 0, output or error
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, f"Error executing command: {str(e)}"

@mcp.tool()
async def open_file(file_path: str) -> str:
    """Open a file in Emacs.
    
    Args:
        file_path: Path to the file to open
    """
    # Expand and resolve path
    expanded_path = os.path.expanduser(file_path)
    abs_path = os.path.abspath(expanded_path)
    
    # Check if file exists (for existing files) or if directory exists (for new files)
    if not os.path.exists(abs_path):
        dir_path = os.path.dirname(abs_path)
        if not os.path.exists(dir_path):
            return f"Error: Directory {dir_path} does not exist"
    
    command = f'(find-file "{abs_path}")'
    success, output = run_emacsclient(command)
    
    if success:
        return f"Successfully opened: {abs_path}"
    else:
        return f"Failed to open file: {output}"

@mcp.tool()
async def eval_elisp(elisp_code: str) -> str:
    """Execute Emacs Lisp code in the running Emacs instance.
    
    Args:
        elisp_code: Emacs Lisp code to execute
    """
    success, output = run_emacsclient(elisp_code)
    
    if success:
        return f"Elisp executed successfully. Result: {output}"
    else:
        return f"Elisp execution failed: {output}"

@mcp.tool()
async def get_buffer_content(buffer_name: str = "") -> str:
    """Get the content of current buffer or specified buffer.
    
    Args:
        buffer_name: Name of buffer to get content from (empty for current buffer)
    """
    if buffer_name:
        command = f'(with-current-buffer "{buffer_name}" (buffer-string))'
    else:
        command = '(buffer-string)'
    
    success, output = run_emacsclient(command)
    
    if success:
        return f"Buffer content:\n{output}"
    else:
        return f"Failed to get buffer content: {output}"

@mcp.tool()
async def insert_text(text: str, position: str = "point") -> str:
    """Insert text at specified position in current buffer.
    
    Args:
        text: Text to insert
        position: Position to insert at ('point', 'beginning', 'end', or line number)
    """
    # Escape quotes in text
    escaped_text = text.replace('"', '\\"')
    
    if position == "beginning":
        command = f'(progn (goto-char (point-min)) (insert "{escaped_text}"))'
    elif position == "end":
        command = f'(progn (goto-char (point-max)) (insert "{escaped_text}"))'
    elif position.isdigit():
        line_num = int(position)
        command = f'(progn (goto-line {line_num}) (insert "{escaped_text}"))'
    else:  # default to current point
        command = f'(insert "{escaped_text}")'
    
    success, output = run_emacsclient(command)
    
    if success:
        return "Text inserted successfully"
    else:
        return f"Failed to insert text: {output}"

@mcp.tool()
async def save_buffer(buffer_name: str = "") -> str:
    """Save current buffer or specified buffer.
    
    Args:
        buffer_name: Name of buffer to save (empty for current buffer)
    """
    if buffer_name:
        command = f'(with-current-buffer "{buffer_name}" (save-buffer))'
    else:
        command = '(save-buffer)'
    
    success, output = run_emacsclient(command)
    
    if success:
        return "Buffer saved successfully"
    else:
        return f"Failed to save buffer: {output}"

@mcp.tool()
async def list_buffers() -> str:
    """List all open buffers in Emacs."""
    command = '(mapcar (lambda (buf) (buffer-name buf)) (buffer-list))'
    success, output = run_emacsclient(command)
    
    if success:
        # Parse the elisp list output and format it nicely
        try:
            # Remove parentheses and split by spaces, handling quoted strings
            buffers = output.strip('()').replace('"', '').split()
            formatted_buffers = '\n'.join(f"- {buf}" for buf in buffers if buf)
            return f"Open buffers:\n{formatted_buffers}"
        except:
            return f"Buffer list: {output}"
    else:
        return f"Failed to list buffers: {output}"

@mcp.tool()
async def search_in_buffer(pattern: str, buffer_name: str = "") -> str:
    """Search for a pattern in current buffer or specified buffer.
    
    Args:
        pattern: Pattern to search for
        buffer_name: Name of buffer to search in (empty for current buffer)
    """
    escaped_pattern = pattern.replace('"', '\\"')
    
    if buffer_name:
        command = f'''(with-current-buffer "{buffer_name}" 
                      (save-excursion 
                        (goto-char (point-min))
                        (let ((matches '()) (line 1))
                          (while (search-forward "{escaped_pattern}" nil t)
                            (push (format "Line %d: %s" line (thing-at-point 'line)) matches)
                            (forward-line 1)
                            (setq line (+ line 1)))
                          (if matches (mapconcat 'identity (reverse matches) "\\n") "No matches found"))))'''
    else:
        command = f'''(save-excursion 
                      (goto-char (point-min))
                      (let ((matches '()) (line 1))
                        (while (search-forward "{escaped_pattern}" nil t)
                          (push (format "Line %d: %s" line (thing-at-point 'line)) matches)
                          (forward-line 1)
                          (setq line (+ line 1)))
                        (if matches (mapconcat 'identity (reverse matches) "\\n") "No matches found")))'''
    
    success, output = run_emacsclient(command)
    
    if success:
        return f"Search results for '{pattern}':\n{output}"
    else:
        return f"Search failed: {output}"

@mcp.tool()
async def run_shell_in_emacs(command: str, directory: str = "") -> str:
    """Run a shell command within Emacs.
    
    Args:
        command: Shell command to execute
        directory: Working directory for the command (optional)
    """
    escaped_command = command.replace('"', '\\"')
    
    if directory:
        expanded_dir = os.path.expanduser(directory)
        elisp_command = f'(let ((default-directory "{expanded_dir}")) (shell-command-to-string "{escaped_command}"))'
    else:
        elisp_command = f'(shell-command-to-string "{escaped_command}")'
    
    success, output = run_emacsclient(elisp_command)
    
    if success:
        return f"Command output:\n{output}"
    else:
        return f"Failed to execute command: {output}"

@mcp.tool()
async def execute_script(script_path: str, args: str = "") -> str:
    """Execute a script file with optional arguments.
    
    Args:
        script_path: Path to the script file
        args: Arguments to pass to the script
    """
    expanded_path = os.path.expanduser(script_path)
    
    if not os.path.exists(expanded_path):
        return f"Error: Script file {expanded_path} does not exist"
    
    if not os.access(expanded_path, os.X_OK):
        return f"Error: Script file {expanded_path} is not executable"
    
    # Build command safely
    if args:
        command = f"{shlex.quote(expanded_path)} {args}"
    else:
        command = shlex.quote(expanded_path)
    
    success, output = run_shell_command(command)
    
    if success:
        return f"Script executed successfully:\n{output}"
    else:
        return f"Script execution failed:\n{output}"

@mcp.tool()
async def create_temp_file(content: str, extension: str = ".txt") -> str:
    """Create a temporary file with given content and open it in Emacs.
    
    Args:
        content: Content to write to the file
        extension: File extension (default: .txt)
    """
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix=extension, delete=False) as f:
            f.write(content)
            temp_path = f.name
        
        # Open the temp file in Emacs
        command = f'(find-file "{temp_path}")'
        success, output = run_emacsclient(command)
        
        if success:
            return f"Temporary file created and opened: {temp_path}"
        else:
            # Clean up if failed to open
            os.unlink(temp_path)
            return f"Failed to open temporary file: {output}"
            
    except Exception as e:
        return f"Failed to create temporary file: {str(e)}"

@mcp.tool()
async def get_emacs_info() -> str:
    """Get information about the running Emacs instance."""
    info_command = '''(format "Emacs Version: %s\\nUser Config Dir: %s\\nCurrent Buffer: %s\\nCurrent Directory: %s\\nFrame Count: %d"
                      emacs-version
                      user-emacs-directory
                      (buffer-name)
                      default-directory
                      (length (frame-list)))'''
    
    success, output = run_emacsclient(info_command)
    
    if success:
        return f"Emacs Information:\n{output}"
    else:
        return f"Failed to get Emacs info: {output}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')